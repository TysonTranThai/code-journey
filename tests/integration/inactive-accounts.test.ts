import { eq, inArray } from "drizzle-orm";
import { afterAll, describe, expect, it } from "vitest";

import { db } from "@/lib/db";
import { submissions, users } from "@/lib/db/schema";
import { cleanupInactiveAccounts } from "@/lib/maintenance/inactive-accounts";

/**
 * Inactive-account cleanup integration tests — run ONLY when Postgres is
 * reachable (same skipIf probe as execution-jobs.test.ts). Uses disposable
 * test accounts with a dedicated email prefix; every account these tests
 * create is removed in afterAll.
 *
 * Boundary note: the cutoff is computed at cleanup time (a moving clock), so
 * "exactly at the threshold" cannot be tested race-free. The strict `<`
 * comparison is instead verified from both sides with a safe margin:
 *   - 7d − 60s of inactivity  → INSIDE  → kept
 *   - 7d + 1h  of inactivity  → OUTSIDE → eligible
 */

const PREFIX = "cj-cleanup-test-";
const day = 24 * 60 * 60 * 1000;

async function makeUser(opts: {
  /** Exact inactivity age in ms, or null for lastActiveAt = NULL. */
  ageMs: number | null;
  role?: "student" | "admin";
}) {
  const email = `${PREFIX}${Date.now()}-${Math.random().toString(36).slice(2, 8)}@example.invalid`;
  const lastActiveAt = opts.ageMs === null ? null : new Date(Date.now() - opts.ageMs);
  const [user] = await db
    .insert(users)
    .values({
      name: "Cleanup Test",
      email,
      passwordHash: "x".repeat(60),
      role: opts.role ?? "student",
      lastActiveAt,
    })
    .returning();
  return user!;
}

const d = (days: number, extraMs = 0) => days * day + extraMs;

const createdIds: string[] = [];
async function track(id: string) {
  createdIds.push(id);
  return id;
}

afterAll(async () => {
  // Remove every account this suite created (cascades handle dependents).
  if (createdIds.length > 0) {
    await db.delete(users).where(inArray(users.id, createdIds));
  }
});

const dbUp = await (async () => {
  try {
    await db.execute("select 1");
    return true;
  } catch {
    return false;
  }
})();

describe.skipIf(!dbUp)("inactive-account cleanup (Postgres-backed)", () => {
  it("identifies only strictly-older-than-threshold student accounts in dry-run", async () => {
    const inactive = await track((await makeUser({ ageMs: d(8) })).id);
    const justOver = await track((await makeUser({ ageMs: d(7, 3_600_000) })).id);
    const justUnder = await track((await makeUser({ ageMs: d(7, -60_000) })).id);
    const recent = await track((await makeUser({ ageMs: d(6) })).id);
    const active = await track((await makeUser({ ageMs: d(0) })).id);
    const never = await track((await makeUser({ ageMs: null })).id);
    const admin = await track((await makeUser({ ageMs: d(30), role: "admin" })).id);

    const before = new Set((await db.select({ id: users.id }).from(users)).map((u) => u.id));

    const result = await cleanupInactiveAccounts({ dryRun: true });

    expect(result.mode).toBe("dry-run");
    expect(result.thresholdDays).toBe(7);
    expect(result.deleted).toBe(0);
    expect(result.affectedUserIds).toContain(inactive); // 8d → eligible
    expect(result.affectedUserIds).toContain(justOver); // 7d+1h → eligible
    expect(result.affectedUserIds).not.toContain(justUnder); // 7d−60s → kept
    expect(result.affectedUserIds).not.toContain(recent); // 6d → kept
    expect(result.affectedUserIds).not.toContain(active); // now → kept
    expect(result.affectedUserIds).not.toContain(never); // NULL → never deleted
    expect(result.affectedUserIds).not.toContain(admin); // admin → never deleted
    // Dry-run wrote nothing: user set identical before/after.
    const after = new Set((await db.select({ id: users.id }).from(users)).map((u) => u.id));
    expect(after.size).toBe(before.size);
  });

  it("apply mode deletes the eligible account and cascades dependent rows", async () => {
    const doomed = await makeUser({ ageMs: d(8) });
    await track(doomed.id);
    const survivor = await makeUser({ ageMs: d(1) });
    await track(survivor.id);

    // Dependent row proves cascade + no-orphans behavior.
    const [submission] = await db
      .insert(submissions)
      .values({
        userId: doomed.id,
        challengeId: "cj-cleanup-test-challenge",
        code: "// cleanup test",
      })
      .returning();

    const result = await cleanupInactiveAccounts({ dryRun: false });
    expect(result.mode).toBe("apply");
    expect(result.affectedUserIds).toContain(doomed.id);
    expect(result.affectedUserIds).not.toContain(survivor.id);
    expect(result.deleted).toBeGreaterThanOrEqual(1);

    // User gone…
    const [gone] = await db.select().from(users).where(eq(users.id, doomed.id));
    expect(gone).toBeUndefined();
    // …with its dependent data (cascade verified).
    const [dep] = await db.select().from(submissions).where(eq(submissions.id, submission!.id));
    expect(dep).toBeUndefined();

    // Survivor untouched.
    const [kept] = await db.select().from(users).where(eq(users.id, survivor.id));
    expect(kept).toBeDefined();
  });

  it("apply mode never deletes NULL-activity or admin accounts", async () => {
    const never = await makeUser({ ageMs: null });
    await track(never.id);
    const admin = await makeUser({ ageMs: d(30), role: "admin" });
    await track(admin.id);

    const result = await cleanupInactiveAccounts({ dryRun: false });
    expect(result.affectedUserIds).not.toContain(never.id);
    expect(result.affectedUserIds).not.toContain(admin.id);
    const [stillThere] = await db.select().from(users).where(eq(users.id, never.id));
    expect(stillThere).toBeDefined();
  });

  it("is idempotent: a second apply run deletes nothing new", async () => {
    await cleanupInactiveAccounts({ dryRun: false });
    const second = await cleanupInactiveAccounts({ dryRun: false });
    expect(second.deleted).toBe(0);
    expect(second.affectedUserIds).toHaveLength(0);
  });

  it("INACTIVE_ACCOUNT_DAYS env override changes the threshold", async () => {
    // 14d − 1h of inactivity: inside the 14-day threshold → kept.
    const staleFor14 = await makeUser({ ageMs: d(14, -3_600_000) });
    await track(staleFor14.id);
    process.env.INACTIVE_ACCOUNT_DAYS = "14";
    try {
      const result = await cleanupInactiveAccounts({ dryRun: true });
      expect(result.thresholdDays).toBe(14);
      expect(result.affectedUserIds).not.toContain(staleFor14.id);
    } finally {
      delete process.env.INACTIVE_ACCOUNT_DAYS;
    }
  });

  it("threshold override of 10 keeps an 8-day-stale account", async () => {
    const u = await makeUser({ ageMs: d(8) });
    await track(u.id);
    process.env.INACTIVE_ACCOUNT_DAYS = "10";
    try {
      const result = await cleanupInactiveAccounts({ dryRun: true });
      expect(result.affectedUserIds).not.toContain(u.id);
    } finally {
      delete process.env.INACTIVE_ACCOUNT_DAYS;
    }
  });
});
