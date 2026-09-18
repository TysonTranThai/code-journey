import Link from "next/link";

import type { ResolvedLesson } from "@/lib/curriculum/schema";
import { getServerI18n } from "@/lib/i18n/server";

/** Difficulty type (local — schema exposes it via the enum values). */
type Difficulty = ResolvedLesson["difficulty"];

const DIFFICULTY_STYLES: Record<Difficulty, string> = {
  beginner: "badge-pixel-emerald",
  intermediate: "badge-pixel-xp",
  advanced: "badge-pixel-streak",
};

export async function DifficultyBadge({ level }: { level: Difficulty }) {
  const { d } = await getServerI18n();
  return (
    <span className={`badge-pixel ${DIFFICULTY_STYLES[level]}`}>
      {level === "beginner" ? "⭐ " : level === "intermediate" ? "⭐⭐ " : "⭐⭐⭐ "}
      {d.difficulty[level]}
    </span>
  );
}

/** One lesson plus everything the learner does right after it. */
export interface LessonFlowGroup {
  lesson: ResolvedLesson;
  /** Practice sets anchored to this lesson (rendered directly below it). */
  practices: Array<{
    id: string;
    title: string;
    description: string;
    minutes: number;
    challenges: string[];
  }>;
  /** Lesson-attached challenges (checkpoints only since the revision). */
  challenges: Array<{ id: string; title: string }>;
}

/**
 * Lessons of one module in order; each lesson carries its practice sets (and
 * checkpoint challenge) as sub-rows directly below it, so the module list
 * shows the full Learn → Practice flow at a glance.
 * Pure content data — no DB calls.
 */
export async function LessonList({
  groups,
  trackId,
  courseId,
  moduleId,
}: {
  groups: LessonFlowGroup[];
  trackId: string;
  courseId: string;
  moduleId: string;
}) {
  const { d, tp, t } = await getServerI18n();
  return (
    <ul className="glass-panel overflow-hidden rounded-2xl divide-y divide-white/[0.06]">
      {groups.map(({ lesson, practices, challenges }) => (
        <li key={lesson.id} className="flex flex-col">
          <Link
            href={`/learn/${trackId}/${courseId}/${moduleId}/${lesson.id}`}
            className="group flex items-center justify-between gap-4 px-5 py-4 hover:bg-white/[0.04] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-emerald-400"
          >
            <div className="flex items-center gap-3.5 min-w-0">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-white/[0.08] bg-white/[0.04] text-xs font-mono text-emerald-400" aria-hidden="true">
                📜
              </span>
              <span className="font-semibold text-zinc-100 group-hover:text-emerald-300 transition-colors truncate">
                {lesson.title}
              </span>
            </div>
            <span className="flex shrink-0 items-center gap-3 text-xs text-zinc-400">
              <DifficultyBadge level={lesson.difficulty} />
              <span className="font-mono text-zinc-400">⏳ {t(d.lesson.minRead, { count: lesson.minutes })}</span>
            </span>
          </Link>

          {(practices.length > 0 || challenges.length > 0) && (
            <ul className="flex flex-col gap-2 border-t border-white/[0.06] bg-[#070a1a]/60 px-5 py-3">
              {practices.map((set) => (
                <li key={set.id}>
                  <Link
                    href={`/learn/${trackId}/${courseId}/${moduleId}/practice/${set.id}`}
                    className="group flex items-center justify-between gap-4 rounded-xl border border-emerald-500/20 bg-emerald-500/[0.04] py-2 pl-3.5 pr-3 hover:border-emerald-500/40 hover:bg-emerald-500/[0.08] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
                  >
                    <span className="flex min-w-0 items-center gap-2.5">
                      <span className="text-emerald-400 text-sm" aria-hidden="true">⚡</span>
                      <span className="shrink-0 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[10px] font-mono font-semibold uppercase tracking-wide text-emerald-300">
                        {d.lessonList.practice}
                      </span>
                      <span className="truncate text-xs font-medium text-zinc-300 group-hover:text-emerald-200">
                        {set.title}
                      </span>
                    </span>
                    <span className="shrink-0 font-mono text-[11px] text-zinc-400">
                      {tp(set.challenges.length, d.lessonList.challengeCount)}·{" "}
                      {t(d.lesson.minutes, { count: set.minutes })}
                    </span>
                  </Link>
                </li>
              ))}
              {challenges.map((challenge) => (
                <li key={challenge.id}>
                  <Link
                    href={`/learn/${trackId}/${courseId}/${moduleId}/${lesson.id}/challenge/${challenge.id}`}
                    className="group flex items-center justify-between gap-4 rounded-xl border border-indigo-500/25 bg-indigo-500/[0.05] py-2 pl-3.5 pr-3 hover:border-indigo-500/50 hover:bg-indigo-500/[0.1] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
                  >
                    <span className="flex min-w-0 items-center gap-2.5">
                      <span className="text-indigo-400 text-sm" aria-hidden="true">🏆</span>
                      <span className="shrink-0 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-2 py-0.5 text-[10px] font-mono font-semibold uppercase tracking-wide text-indigo-300">
                        {d.lessonList.checkpoint}
                      </span>
                      <span className="truncate text-xs font-medium text-zinc-300 group-hover:text-indigo-200">
                        {challenge.title}
                      </span>
                    </span>
                    <span className="badge-pixel badge-pixel-level text-[10px]">
                      {d.lessonList.checkpoint}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ul>
  );
}
