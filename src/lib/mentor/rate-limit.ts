import "server-only";

import { and, eq, gte, sql } from "drizzle-orm";

import { db } from "@/lib/db";
import { mentorRequests } from "@/lib/db/schema";

/**
 * Mentor rate limiting (AI-03, 05-CONTEXT D-08): per-user daily quotas
 * counted server-side. Anonymous users never reach here (auth required),
 * which doubles as the first abuse-prevention layer.
 */
export const MENTOR_LIMITS = { hintsPerDay: 10, explainsPerDay: 20 } as const;

export type MentorKind = keyof typeof MENTOR_LIMITS;

function startOfTodayUtc(): Date {
  const now = new Date();
  return new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
}

export async function checkMentorQuota(
  userId: string,
  kind: MentorKind,
): Promise<{ allowed: boolean; remaining: number }> {
  const [row] = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(mentorRequests)
    .where(
      and(
        eq(mentorRequests.userId, userId),
        eq(mentorRequests.kind, kind),
        gte(mentorRequests.createdAt, startOfTodayUtc()),
      ),
    );
  const used = row?.count ?? 0;
  const limit = MENTOR_LIMITS[kind];
  return { allowed: used < limit, remaining: Math.max(0, limit - used) };
}

export async function recordMentorRequest(userId: string, kind: MentorKind): Promise<void> {
  await db.insert(mentorRequests).values({ userId, kind });
}
