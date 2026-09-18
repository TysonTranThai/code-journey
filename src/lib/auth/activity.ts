import { and, eq, isNull, lt, or } from "drizzle-orm";

import { db } from "@/lib/db";
import { users } from "@/lib/db/schema";
import { logWarn } from "@/lib/observability";

/**
 * Account-activity tracking for the inactive-account cleanup policy.
 *
 * Qualifying activity (defined here, one place):
 *   - a live authenticated session performing ANY server-side request that
 *     reads the session (page render, API call, server action) — the JWT
 *     session callback routes through touchLastActive, so every authenticated
 *     request counts and multiple devices/sessions each keep the account
 *     fresh while ANY of them is in use;
 *   - account creation (registration) seeds lastActiveAt so a brand-new
 *     account starts its 7-day window from a real event, never "immediately
 *     stale" (see the register action).
 *
 * Throttling: the UPDATE carries its own WHERE guard — the row is only
 * written when the stored timestamp is older than HEARTBEAT_MS (or NULL).
 * Requests inside the window match zero rows: one cheap indexed statement,
 * no write. Normal browsing therefore costs at most one tiny UPDATE per user
 * per window, not per request.
 */

/** Minimum interval between two lastActiveAt writes for the same user. */
const HEARTBEAT_MS = 5 * 60 * 1000;

export function heartbeatCutoff(now: Date = new Date()): Date {
  return new Date(now.getTime() - HEARTBEAT_MS);
}

/**
 * Record qualifying activity for `userId`. Never throws — activity tracking
 * must not break authentication or rendering. Fire-and-forget safe.
 */
export async function touchLastActive(userId: string): Promise<void> {
  try {
    await db
      .update(users)
      .set({ lastActiveAt: new Date() })
      .where(
        and(
          eq(users.id, userId),
          or(isNull(users.lastActiveAt), lt(users.lastActiveAt, heartbeatCutoff())),
        ),
      );
  } catch {
    // Never let telemetry break auth; warn with the user id only (no PII).
    logWarn("auth.activity", "lastActiveAt update failed");
  }
}
