import "server-only";

import { and, eq, sql } from "drizzle-orm";

import { db } from "@/lib/db";
import { achievements, progressEvents, submissions, type StoredVerdict } from "@/lib/db/schema";
import {
  getCurriculumModule,
  getLesson,
  getLessonChallenges,
} from "@/lib/curriculum/loaders";
import { getAchievementDefs } from "./achievement-defs";

/**
 * Server-verified progress recording (PROG-02, 04-CONTEXT D-04…D-06).
 *
 * Every write derives from a server-side fact:
 *  - challenge completion ← the runner's passed verdict (DB row)
 *  - lesson completion ← passing submissions for ALL its challenges (DB)
 * The client cannot create either; the API only forwards authenticated intent.
 */

/** Thrown when the server-side verification fails (client lied or raced). */
export class ProgressVerificationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ProgressVerificationError";
  }
}

/** Record a completed lesson after verifying its challenges were passed. */
export async function recordLessonCompletion(
  userId: string,
  trackId: string,
  courseId: string,
  moduleId: string,
  lessonId: string,
): Promise<{ recorded: boolean }> {
  // (a) the lesson must exist in content-as-data
  const lesson = getLesson(trackId, courseId, moduleId, lessonId);

  // (b) all of the lesson's challenges must have a passing submission by
  // this user in the DB — the client cannot assert completion (PROG-02).
  const challenges = getLessonChallenges(trackId, courseId, moduleId, lessonId);
  for (const challenge of challenges) {
    const passed = await db
      .select({ id: submissions.id })
      .from(submissions)
      .where(
        and(
          eq(submissions.userId, userId),
          eq(submissions.challengeId, challenge.id),
          eq(submissions.verdict, "passed"),
        ),
      )
      .limit(1);
    if (passed.length === 0) {
      throw new ProgressVerificationError(
        `Lesson "${lessonId}" cannot be completed: challenge "${challenge.id}" has no passing submission`,
      );
    }
  }

  const result = await db
    .insert(progressEvents)
    .values({ userId, contentType: "lesson", contentId: lesson.id })
    .onConflictDoNothing()
    .returning({ id: progressEvents.id });

  await maybeAwardAchievements(userId);
  return { recorded: result.length > 0 };
}

/** Record a passed challenge. Called only from the verdict write path. */
export async function recordChallengeCompletion(
  userId: string,
  challengeId: string,
): Promise<void> {
  await db
    .insert(progressEvents)
    .values({ userId, contentType: "challenge", contentId: challengeId })
    .onConflictDoNothing();
  // Best-effort award evaluation; a later event re-triggers it (D-08).
  await maybeAwardAchievements(userId).catch((err: unknown) => {
    console.error("[progress] award evaluation failed:", err instanceof Error ? err.message : err);
  });
}

/**
 * Evaluate achievements for a user (04-CONTEXT D-07): pure criteria over the
 * user's progress_events + passing submissions; inserts are idempotent
 * (onConflictDoNothing). Never trusts client claims (DATA-MODEL principle 4).
 */
export async function maybeAwardAchievements(userId: string): Promise<string[]> {
  const defs = getAchievementDefs();
  const events = await db
    .select({
      contentType: progressEvents.contentType,
      contentId: progressEvents.contentId,
      createdAt: progressEvents.createdAt,
    })
    .from(progressEvents)
    .where(eq(progressEvents.userId, userId));

  const [passingCount] = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(submissions)
    .where(and(eq(submissions.userId, userId), eq(submissions.verdict, "passed")));

  const lessonsCompleted = events.filter((e) => e.contentType === "lesson");
  const challengesCompleted = events.filter((e) => e.contentType === "challenge");

  // Streak days: distinct calendar days with any event.
  const dayKeys = new Set(events.map((e) => e.createdAt.toISOString().slice(0, 10)));

  const earned: string[] = [];
  const has = (id: string) => earned.includes(id);

  if (lessonsCompleted.length >= 1) earned.push("first-lesson");
  if (lessonsCompleted.length >= 5) earned.push("five-lessons");
  if (challengesCompleted.length >= 1 || (passingCount?.count ?? 0) >= 1) {
    earned.push("first-challenge");
  }
  if (hasStreakOf3(dayKeys)) earned.push("first-streak-3");

  // Module completion: every lesson in the html-foundations module has a
  // lesson event. Lesson ids come from the curriculum (content-as-data), so
  // the achievement follows the module as it grows.
  const moduleLessonIds = getCurriculumModule(
    "web-development",
    "web-development-beginner",
    "html-foundations",
  ).lessons.map((l) => l.reference);
  const completedIds = new Set(lessonsCompleted.map((e) => e.contentId));
  if (moduleLessonIds.every((id) => completedIds.has(id))) {
    earned.push("html-foundations-complete");
  }

  void has; // (helper kept for readability in future criteria)

  const known = new Set(defs.map((d) => d.id));
  const awardable = earned.filter((id) => known.has(id));
  if (awardable.length === 0) return [];

  const inserted = await db
    .insert(achievements)
    .values(awardable.map((achievementId) => ({ userId, achievementId })))
    .onConflictDoNothing()
    .returning({ achievementId: achievements.achievementId });

  return inserted.map((row) => row.achievementId);
}

/** Distinct-day consecutive run of ≥3 ending today or yesterday (UTC days). */
function hasStreakOf3(dayKeys: Set<string>): boolean {
  const today = new Date();
  const DAY_MS = 24 * 60 * 60 * 1000;
  let run = 0;
  const cursor = new Date(
    Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()),
  );
  if (!dayKeys.has(cursor.toISOString().slice(0, 10))) {
    cursor.setTime(cursor.getTime() - DAY_MS);
  }
  while (dayKeys.has(cursor.toISOString().slice(0, 10))) {
    run += 1;
    if (run >= 3) return true;
    cursor.setTime(cursor.getTime() - DAY_MS);
  }
  return false;
}

/** Type re-export for the verdict hook (keeps queue imports minimal). */
export type { StoredVerdict };
