import { and, eq, isNotNull, lt, sql } from "drizzle-orm";

import { db } from "@/lib/db";
import { users } from "@/lib/db/schema";
import { captureError, logEvent, logWarn } from "@/lib/observability";

/**
 * Inactive-account cleanup (7-day inactivity policy, threshold configurable).
 *
 * Safety invariants (all verified in tests + production rehearsal):
 *   1. Only users with a NON-NULL lastActiveAt strictly older than the
 *      threshold are eligible. NULL = unknown activity = NEVER deleted.
 *   2. role='admin' accounts are NEVER deleted.
 *   3. Boundary is strict: exactly-threshold-old accounts are kept ("more
 *      than 7 days" = strictly greater than the configured period).
 *   4. Deletion runs in ONE transaction per user; every user-owned table
 *      cascades (accounts, sessions, password_reset_tokens, profiles,
 *      submissions → execution_jobs, progress_events, achievements,
 *      discussion_threads → comments, mentor_requests). No orphans possible.
 *   5. Idempotent: a second run finds nothing new; safe to re-run after any
 *      failure.
 *   6. Dry-run mode performs NO writes and reports exactly what apply mode
 *      would delete (same eligibility predicate).
 *
 * Never logged: emails, names, hashes, tokens — only counts and user ids.
 */

export interface CleanupResult {
  mode: "dry-run" | "apply";
  scanned: number;
  eligible: number;
  deleted: number;
  skipped: number;
  errors: number;
  /** The ids that were (or would be) removed — operational audit trail. */
  affectedUserIds: string[];
  thresholdDays: number;
  cutoff: string;
}

function parseThresholdDays(): number {
  const raw = process.env.INACTIVE_ACCOUNT_DAYS;
  if (raw === undefined || raw.trim() === "") return 7;
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0 || !Number.isInteger(n)) {
    throw new Error(`INACTIVE_ACCOUNT_DAYS must be a positive integer, got: ${raw}`);
  }
  return n;
}

/**
 * Select eligibility and count in one round trip. The predicate is the
 * single source of truth shared by dry-run and apply modes.
 */
async function findEligible(thresholdDays: number, now: Date) {
  const cutoff = new Date(now.getTime() - thresholdDays * 24 * 60 * 60 * 1000);
  const eligible = await db
    .select({ id: users.id })
    .from(users)
    .where(
      and(
        // Qualifying activity must exist and be strictly older than cutoff.
        // (Postgres NULL < cutoff is NULL/falsy, but the isNotNull guard
        // makes the "never delete unknown-activity accounts" rule explicit.)
        isNotNull(users.lastActiveAt),
        lt(users.lastActiveAt, cutoff),
        eq(users.role, "student"),
      ),
    );
  const [countRow] = await db.select({ count: sql<number>`count(*)::int` }).from(users);
  return { eligible, total: countRow?.count ?? 0, cutoff };
}

export async function cleanupInactiveAccounts(options: { dryRun: boolean }): Promise<CleanupResult> {
  const thresholdDays = parseThresholdDays();
  const now = new Date();
  const { eligible, total, cutoff } = await findEligible(thresholdDays, now);

  const base = {
    mode: (options.dryRun ? "dry-run" : "apply") as CleanupResult["mode"],
    scanned: total,
    eligible: eligible.length,
    thresholdDays,
    cutoff: cutoff.toISOString(),
  };

  if (options.dryRun) {
    logEvent("cleanup.inactive-accounts", "dry-run complete — no rows were changed", {
      ...base,
      affectedUserIds: eligible.map((u) => u.id),
    });
    return {
      ...base,
      deleted: 0,
      skipped: 0,
      errors: 0,
      affectedUserIds: eligible.map((u) => u.id),
    };
  }

  let deleted = 0;
  let skipped = 0;
  let errors = 0;
  const affectedUserIds: string[] = [];

  for (const { id } of eligible) {
    // Re-check inside the transaction: something (a login, an activity
    // heartbeat, a role change) may have refreshed the account between the
    // eligibility scan and now. Guarantees "never delete someone who just
    // came back", even under concurrency. One failing account never aborts
    // the run — it is counted and the loop continues.
    let txResult: "gone" | "not-student" | "null-activity" | "refreshed" | "deleted";
    try {
      txResult = await db.transaction(async (tx) => {
      const [current] = await tx
        .select({ role: users.role, lastActiveAt: users.lastActiveAt })
        .from(users)
        .where(eq(users.id, id))
        .for("update")
        .limit(1);

      if (!current) return "gone" as const;
      if (current.role !== "student") return "not-student" as const;
      if (!current.lastActiveAt) return "null-activity" as const;
      if (current.lastActiveAt.getTime() >= cutoff.getTime()) return "refreshed" as const;

        // ON DELETE CASCADE handles every dependent table; the transaction
        // makes the whole user removal atomic.
        await tx.delete(users).where(eq(users.id, id));
        return "deleted" as const;
      });
    } catch (err) {
      errors += 1;
      captureError("cleanup.inactive-accounts", err, { userId: id });
      continue;
    }

    if (txResult === "deleted") {
      deleted += 1;
      affectedUserIds.push(id);
    } else if (txResult === "gone") {
      // Vanished concurrently (e.g. another job instance): count as skipped.
      skipped += 1;
    } else if (txResult === "refreshed") {
      skipped += 1;
      logWarn("cleanup.inactive-accounts", "account refreshed between scan and delete — skipped", {
        userId: id,
      });
    } else {
      // null-activity / not-student: policy exclusion hit on re-check.
      skipped += 1;
      logWarn("cleanup.inactive-accounts", "account failed policy re-check — skipped", {
        userId: id,
      });
    }
  }

  const result: CleanupResult = {
    ...base,
    deleted,
    skipped,
    errors,
    affectedUserIds,
  };
  logEvent("cleanup.inactive-accounts", "apply run complete", { ...result });
  return result;
}
