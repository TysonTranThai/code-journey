import Link from "next/link";

import type { Difficulty, ResolvedLesson } from "@/lib/curriculum/schema";

const DIFFICULTY_STYLES: Record<Difficulty, string> = {
  beginner: "bg-emerald-950 text-emerald-300",
  intermediate: "bg-amber-950 text-amber-300",
  advanced: "bg-red-950 text-red-300",
};

export function DifficultyBadge({ level }: { level: Difficulty }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${DIFFICULTY_STYLES[level]}`}>
      {level}
    </span>
  );
}

/** Lessons of one module, in order. Pure content data — no DB calls. */
export function LessonList({ lessons }: { lessons: ResolvedLesson[] }) {
  return (
    <ul className="flex flex-col divide-y divide-zinc-800/60 rounded-xl border border-zinc-800">
      {lessons.map((lesson) => (
        <li key={lesson.id}>
          <Link
            href={`/learn/${lesson.trackId}/${lesson.courseId}/${lesson.moduleId}/${lesson.id}`}
            className="flex items-center justify-between gap-4 px-4 py-3.5 hover:bg-zinc-900/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-indigo-400"
          >
            <span className="font-medium text-zinc-100">{lesson.title}</span>
            <span className="flex shrink-0 items-center gap-3 text-sm text-zinc-400">
              <DifficultyBadge level={lesson.difficulty} />
              <span>{lesson.minutes} min</span>
              {lesson.challenges.length > 0 ? (
                <span>
                  {lesson.challenges.length} challenge
                  {lesson.challenges.length === 1 ? "" : "s"}
                </span>
              ) : null}
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}
