import Link from "next/link";

import type { ResolvedLesson } from "@/lib/curriculum/schema";
import { getServerI18n } from "@/lib/i18n/server";

/**
 * Linear lesson navigation (CURR-03). Prev/next cross module boundaries via
 * the loaders' linear track order.
 */
export async function LessonPager({
  trackId,
  prev,
  next,
}: {
  trackId: string;
  prev: ResolvedLesson | null;
  next: ResolvedLesson | null;
}) {
  const { d } = await getServerI18n();
  const href = (lesson: ResolvedLesson) =>
    `/learn/${trackId}/${lesson.courseId}/${lesson.moduleId}/${lesson.id}`;

  return (
    <nav
      aria-label={d.pager.aria}
      className="mt-12 flex items-stretch justify-between gap-4 border-t border-white/[0.08] pt-8"
    >
      {prev ? (
        <Link
          href={href(prev)}
          className="group conductor-window flex-1 p-5 rounded-xl border border-white/[0.08] bg-[#0c101b] transition-all hover:border-emerald-400/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 shadow-md"
        >
          <span className="block font-mono text-xs font-semibold uppercase tracking-wider text-emerald-400">
            {d.pager.previous}
          </span>
          <span className="mt-1.5 block font-semibold text-zinc-100 group-hover:text-emerald-300 transition-colors">
            {prev.title}
          </span>
        </Link>
      ) : (
        <span className="flex-1" />
      )}
      {next ? (
        <Link
          href={href(next)}
          className="group conductor-window flex-1 p-5 rounded-xl text-right border border-white/[0.08] bg-[#0c101b] transition-all hover:border-emerald-400/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 shadow-md"
        >
          <span className="block font-mono text-xs font-semibold uppercase tracking-wider text-emerald-400">
            {d.pager.next}
          </span>
          <span className="mt-1.5 block font-semibold text-zinc-100 group-hover:text-emerald-300 transition-colors">
            {next.title}
          </span>
        </Link>
      ) : (
        <div className="conductor-window flex-1 p-5 rounded-xl text-right self-center border border-emerald-500/30 bg-emerald-950/20 text-emerald-300 font-semibold text-sm shadow-md">
          {d.pager.courseComplete}
        </div>
      )}
    </nav>
  );
}
