import Link from "next/link";

import type { ResolvedLesson } from "@/lib/curriculum/schema";

/**
 * Linear lesson navigation (CURR-03). Prev/next cross module boundaries via
 * the loaders' linear track order.
 */
export function LessonPager({
  trackId,
  prev,
  next,
}: {
  trackId: string;
  prev: ResolvedLesson | null;
  next: ResolvedLesson | null;
}) {
  const href = (lesson: ResolvedLesson) =>
    `/learn/${trackId}/${lesson.courseId}/${lesson.moduleId}/${lesson.id}`;

  return (
    <nav
      aria-label="Lesson navigation"
      className="mt-12 flex items-stretch justify-between gap-4 border-t border-zinc-800 pt-6"
    >
      {prev ? (
        <Link
          href={href(prev)}
          className="group flex-1 rounded-lg border border-zinc-800 px-4 py-3 hover:border-zinc-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
        >
          <span className="block text-xs uppercase tracking-wider text-zinc-400">← Previous</span>
          <span className="mt-1 block font-medium text-zinc-200 group-hover:text-white">
            {prev.title}
          </span>
        </Link>
      ) : (
        <span className="flex-1" />
      )}
      {next ? (
        <Link
          href={href(next)}
          className="group flex-1 rounded-lg border border-zinc-800 px-4 py-3 text-right hover:border-zinc-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
        >
          <span className="block text-xs uppercase tracking-wider text-zinc-400">Next →</span>
          <span className="mt-1 block font-medium text-zinc-200 group-hover:text-white">
            {next.title}
          </span>
        </Link>
      ) : (
        <span className="flex-1 text-right text-sm text-zinc-400 self-center">
          Course complete 🎉
        </span>
      )}
    </nav>
  );
}
