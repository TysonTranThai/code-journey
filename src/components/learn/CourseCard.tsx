import Link from "next/link";

import type { Course, Track } from "@/lib/curriculum/schema";

/** Card for a track on the /learn index. */
export function TrackCard({ track, courseCount }: { track: Track; courseCount: number }) {
  return (
    <Link
      href={`/learn/${track.id}`}
      className="group flex flex-col gap-2 rounded-xl border border-zinc-800 bg-zinc-900/40 p-6 transition-colors hover:border-indigo-500/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
    >
      <h2 className="text-lg font-semibold text-zinc-100 group-hover:text-white">{track.title}</h2>
      <p className="text-sm text-zinc-400">{track.description}</p>
      <span className="mt-auto pt-2 text-sm font-medium text-indigo-400">
        {courseCount} course{courseCount === 1 ? "" : "s"} · Start learning →
      </span>
    </Link>
  );
}

/** Card for a course on a track page. */
export function CourseCard({
  trackId,
  course,
  moduleCount,
}: {
  trackId: string;
  course: Course;
  moduleCount: number;
}) {
  return (
    <Link
      href={`/learn/${trackId}/${course.id}`}
      className="group flex flex-col gap-2 rounded-xl border border-zinc-800 bg-zinc-900/40 p-6 transition-colors hover:border-indigo-500/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
    >
      <h2 className="text-lg font-semibold text-zinc-100 group-hover:text-white">{course.title}</h2>
      <p className="text-sm text-zinc-400">{course.description}</p>
      <span className="mt-auto pt-2 text-sm font-medium text-indigo-400">
        {moduleCount} module{moduleCount === 1 ? "" : "s"} · Continue →
      </span>
    </Link>
  );
}
