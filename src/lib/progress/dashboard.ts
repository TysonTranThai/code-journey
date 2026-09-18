import "server-only";

import { desc, eq } from "drizzle-orm";

import { db } from "@/lib/db";
import { achievements, progressEvents } from "@/lib/db/schema";
import {
  getLinearLessons,
  getModulePractices,
  getPracticeChallenges,
  getTracks,
} from "@/lib/curriculum/loaders";
import type { Locale } from "@/lib/i18n/config";
import { getAchievementDefs } from "./achievement-defs";
import { computeStreak } from "./streak";

/**
 * Dashboard projection (04-CONTEXT D-09): a read-only view over progress
 * events + passing submissions + content-as-data. No write paths here.
 */

export interface TrackProgress {
  trackId: string;
  trackTitle: string;
  completed: number;
  total: number;
  percent: number;
}

export interface DashboardData {
  overall: { completed: number; total: number; percent: number };
  perTrack: TrackProgress[];
  streakDays: number;
  achievements: {
    id: string;
    title: string;
    description: string;
    icon: string;
    earned: boolean;
    awardedAt: Date | null;
  }[];
  continueLearning: {
    href: string;
    title: string;
    kind: "lesson" | "challenge";
  } | null;
}

export async function getDashboardData(
  userId: string,
  locale: Locale = "en",
): Promise<DashboardData> {
  const [events, awarded] = await Promise.all([
    db
      .select()
      .from(progressEvents)
      .where(eq(progressEvents.userId, userId))
      .orderBy(desc(progressEvents.createdAt)),
    db.select().from(achievements).where(eq(achievements.userId, userId)),
  ]);

  const completedLessons = new Set(
    events.filter((e) => e.contentType === "lesson").map((e) => e.contentId),
  );
  const completedChallenges = new Set(
    events.filter((e) => e.contentType === "challenge").map((e) => e.contentId),
  );

  // Per-track + overall projection from content-as-data totals.
  const perTrack: TrackProgress[] = [];
  let totalDone = 0;
  let totalAll = 0;

  for (const track of getTracks(undefined, locale)) {
    const lessons = getLinearLessons(track.id, undefined, locale);
    // Course 1 revision: coding progress counts practice-set challenges.
    // (Lesson-attached checkout challenges are included via their practice
    // sets when they exist; checkpoints are covered by their own lessons.)
    const practiceChallenges = lessons.flatMap((lesson) =>
      getModulePractices(track.id, lesson.courseId, lesson.moduleId, undefined, locale)
        .filter((p) => p.afterLesson === lesson.id)
        .flatMap((p) =>
          getPracticeChallenges(track.id, lesson.courseId, lesson.moduleId, p.id, undefined, locale).map(
            (challenge) => ({ lesson, challenge }),
          ),
        ),
    );
    const challenges = practiceChallenges;
    const total = lessons.length + challenges.length;
    const done =
      lessons.filter((l) => completedLessons.has(l.id)).length +
      challenges.filter((c) => completedChallenges.has(c.challenge.id)).length;
    totalDone += done;
    totalAll += total;
    perTrack.push({
      trackId: track.id,
      trackTitle: track.title,
      completed: done,
      total,
      percent: total === 0 ? 0 : Math.round((done / total) * 100),
    });
  }

  // Achievements: earned (joined with awardedAt) + locked defs.
  const awardedMap = new Map(awarded.map((a) => [a.achievementId, a.awardedAt]));
  const achievementRows = getAchievementDefs(locale).map((def) => ({
    ...def,
    earned: awardedMap.has(def.id),
    awardedAt: awardedMap.get(def.id) ?? null,
  }));

  // Continue-learning: latest event's position in the linear order → next
  // item; with no history, the first lesson.
  const continueLearning = deriveContinueTarget(events, locale);

  return {
    overall: {
      completed: totalDone,
      total: totalAll,
      percent: totalAll === 0 ? 0 : Math.round((totalDone / totalAll) * 100),
    },
    perTrack,
    streakDays: computeStreak(
      events.map((e) => e.createdAt),
      new Date(),
    ),
    achievements: achievementRows,
    continueLearning,
  };
}

function deriveContinueTarget(
  events: { contentType: "lesson" | "challenge"; contentId: string }[],
  locale: Locale,
): DashboardData["continueLearning"] {
  const tracks = getTracks(undefined, locale);
  if (tracks.length === 0) return null;

  const linearOfFirst = getLinearLessons(tracks[0]!.id, undefined, locale);
  if (linearOfFirst.length === 0) return null;

  // Find the earliest linear lesson that is NOT completed.
  const firstIncomplete = linearOfFirst.find(
    (lesson) => !completedLessonSet(events).has(lesson.id),
  );
  const target = firstIncomplete ?? linearOfFirst[linearOfFirst.length - 1]!;
  const href = `/learn/${target.trackId}/${target.courseId}/${target.moduleId}/${target.id}`;

  // If that lesson has an un-passed practice challenge, point at it
  // (deeper into the loop); otherwise the lesson itself.
  const practiceSet = getModulePractices(
    target.trackId,
    target.courseId,
    target.moduleId,
    undefined,
    locale,
  ).find((p) => p.afterLesson === target.id);
  const challenges = practiceSet
    ? getPracticeChallenges(target.trackId, target.courseId, target.moduleId, practiceSet.id, undefined, locale)
    : [];
  const nextChallenge = challenges.find((c) => !completedChallengeSet(events).has(c.id));
  if (nextChallenge) {
    return {
      href: `${href}/practice/${practiceSet!.id}/${nextChallenge.id}`,
      title: nextChallenge.title,
      kind: "challenge" as const,
    };
  }
  return { href, title: target.title, kind: "lesson" as const };
}

function completedLessonSet(
  events: { contentType: "lesson" | "challenge"; contentId: string }[],
): Set<string> {
  return new Set(events.filter((e) => e.contentType === "lesson").map((e) => e.contentId));
}

function completedChallengeSet(
  events: { contentType: "lesson" | "challenge"; contentId: string }[],
): Set<string> {
  return new Set(events.filter((e) => e.contentType === "challenge").map((e) => e.contentId));
}
