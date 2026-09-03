import type { Metadata } from "next";

import { TrackCard } from "@/components/learn/CourseCard";
import { getTracks } from "@/lib/curriculum/loaders";
import { siteConfig } from "@/lib/site-config";

export const metadata: Metadata = {
  title: "Learn to code — free curriculum",
  description:
    "Browse free, structured coding courses with auto-graded challenges and an AI mentor. Web development foundations available now — no account needed to start learning.",
  alternates: { canonical: `${siteConfig.url}/learn` },
};

export default function LearnIndexPage() {
  const tracks = getTracks();
  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight text-zinc-100 sm:text-4xl">
          Start learning
        </h1>
        <p className="max-w-2xl text-zinc-400">
          Free, structured courses — read every lesson without an account. Create a free account
          when you&apos;re ready to save progress, earn achievements, and ask the mentor.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {tracks.map((track) => (
          <TrackCard key={track.id} track={track} courseCount={track.courses.length} />
        ))}
      </div>
    </div>
  );
}
