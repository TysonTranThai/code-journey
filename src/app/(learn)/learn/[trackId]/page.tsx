import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { CourseCard } from "@/components/learn/CourseCard";
import { getLoadedCourses, getTrack, getTracks } from "@/lib/curriculum/loaders";
import { getServerI18n } from "@/lib/i18n/server";
import { siteConfig } from "@/lib/site-config";

interface TrackPageProps {
  params: Promise<{ trackId: string }>;
}

export function generateStaticParams() {
  return getTracks().map((track) => ({ trackId: track.id }));
}

export async function generateMetadata({ params }: TrackPageProps): Promise<Metadata> {
  const { trackId } = await params;
  const track = getTracks().find((t) => t.id === trackId);
  if (!track) return { title: "Track not found" };
  return {
    title: track.title,
    description: track.description,
    alternates: { canonical: `${siteConfig.url}/learn/${track.id}` },
  };
}

export default async function TrackPage({ params }: TrackPageProps) {
  const { trackId } = await params;
  const { d, locale } = await getServerI18n();
  let track;
  try {
    track = getTrack(trackId, undefined, locale);
  } catch {
    notFound();
  }

  // Loaded courses only: a concurrently scaffolded course with an empty
  // modules list is excluded by the loader (authoring shell) and must not
  // crash this page with CurriculumNotFoundError (2026-09-13 report).
  const courses = getLoadedCourses(trackId, undefined, locale);

  return (
    <div className="flex flex-col gap-8">
      <Breadcrumbs
        items={[
          { label: d.breadcrumb.learn, href: "/learn" },
          { label: track.title },
        ]}
      />

      <header className="conductor-window flex flex-col gap-4 rounded-2xl border border-white/[0.08] bg-[#0c101b] p-6 sm:p-8 shadow-xl">
        <div className="flex items-center gap-2">
          <span className="badge-pixel badge-pixel-level font-mono">{d.track.expeditionBadge}</span>
          <span className="text-emerald-400 text-sm font-mono" aria-hidden="true">✦</span>
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-5xl">
          {track.title}
        </h1>
        <p className="max-w-2xl text-base text-zinc-300 leading-relaxed font-normal">{track.description}</p>
      </header>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {courses.map((course) => (
          <CourseCard
            key={course.id}
            trackId={trackId}
            course={course}
            moduleCount={course.modules.length}
          />
        ))}
      </div>
    </div>
  );
}
