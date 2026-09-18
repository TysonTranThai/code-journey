import Link from "next/link";

import type { Course, Track } from "@/lib/curriculum/schema";
import { getServerI18n } from "@/lib/i18n/server";

/** Card for a track on the /learn index (async: resolves the UI locale). */
export async function TrackCard({ track, courseCount }: { track: Track; courseCount: number }) {
  const { tp, d } = await getServerI18n();
  return (
    <Link
      href={`/learn/${track.id}`}
      className="group conductor-window card-glow-hover flex flex-col justify-between p-5 rounded-xl border border-white/[0.08] bg-[#0c101b] transition-all hover:border-emerald-500/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
    >
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <span className="badge-pixel badge-pixel-level font-mono">{d.cards.trackBranch}</span>
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-[#111624] text-emerald-400 border border-emerald-500/30 text-xs font-mono">
            🌿
          </div>
        </div>
        <h2 className="text-lg font-bold text-white group-hover:text-emerald-300 transition-colors">
          {track.title}
        </h2>
        <p className="text-sm text-zinc-400 leading-relaxed">{track.description}</p>
      </div>

      <div className="mt-6 pt-4 border-t border-white/[0.06] flex items-center justify-between">
        <span className="font-mono text-xs font-semibold text-zinc-400">
          {tp(courseCount, d.cards.courses)}
        </span>
        <span className="font-semibold text-xs text-emerald-400 group-hover:translate-x-0.5 transition-transform flex items-center gap-1.5 font-mono">
          <span>{d.cards.exploreTrack}</span>
          <span aria-hidden="true">→</span>
        </span>
      </div>
    </Link>
  );
}

/** Card for a course on a track page (async: resolves the UI locale). */
export async function CourseCard({
  trackId,
  course,
  moduleCount,
}: {
  trackId: string;
  course: Course;
  moduleCount: number;
}) {
  const { tp, d } = await getServerI18n();
  return (
    <Link
      href={`/learn/${trackId}/${course.id}`}
      className="group conductor-window card-glow-hover flex flex-col justify-between p-5 rounded-xl border border-white/[0.08] bg-[#0c101b] transition-all hover:border-emerald-500/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
    >
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <span className="badge-pixel badge-pixel-quest font-mono">{d.cards.moduleCourse}</span>
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-[#111624] text-emerald-400 border border-emerald-500/30 text-xs font-mono">
            ⚡
          </div>
        </div>
        <h2 className="text-lg font-bold text-white group-hover:text-emerald-300 transition-colors">
          {course.title}
        </h2>
        <p className="text-sm text-zinc-400 leading-relaxed">{course.description}</p>
      </div>

      <div className="mt-6 pt-4 border-t border-white/[0.06] flex items-center justify-between">
        <span className="font-mono text-xs font-semibold text-zinc-400">
          {tp(moduleCount, d.cards.modules)}
        </span>
        <span className="font-semibold text-xs text-emerald-400 group-hover:translate-x-0.5 transition-transform flex items-center gap-1.5 font-mono">
          <span>{d.cards.openModules}</span>
          <span aria-hidden="true">→</span>
        </span>
      </div>
    </Link>
  );
}
