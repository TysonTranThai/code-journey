import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { CourseCard } from "@/components/learn/CourseCard";
import { getCourse, getTrack, getTracks } from "@/lib/curriculum/loaders";
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
  let track;
  try {
    track = getTrack(trackId);
  } catch {
    notFound();
  }

  const courses = track.courses.map((ref) => getCourse(trackId, ref.reference));

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight text-zinc-100 sm:text-4xl">
          {track.title}
        </h1>
        <p className="max-w-2xl text-zinc-400">{track.description}</p>
      </header>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
