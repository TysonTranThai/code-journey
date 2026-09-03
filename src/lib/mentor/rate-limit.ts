import "server-only";

import { db } from "@/lib/db";
import { mentorRequests } from "@/lib/db/schema";
import { consume, DAY_MS } from "@/lib/rate-limit/limiter";

/**
 * Mentor rate limiting (AI-03, 05-CONTEXT D-08): per-user daily quotas counted
 * server-side. Anonymous users never reach here (auth required), which doubles
 * as the first abuse-prevention layer.
 *
 * 07-03: the quota check is now an ATOMIC check-and-increment (consume) — no
 * TOCTOU race between a read and a later record. `recordMentorRequest` still
 * writes the audit trail; the LIMIT comes from the atomic counter.
 */
export const MENTOR_LIMITS = { hintsPerDay: 10, explainsPerDay: 20 } as const;

export type MentorKind = keyof typeof MENTOR_LIMITS;

export async function checkMentorQuota(
  userId: string,
  kind: MentorKind,
): Promise<{ allowed: boolean; remaining: number }> {
  return consume(`mentor:${kind}`, userId, MENTOR_LIMITS[kind], DAY_MS);
}

export async function recordMentorRequest(userId: string, kind: MentorKind): Promise<void> {
  await db.insert(mentorRequests).values({ userId, kind });
}
