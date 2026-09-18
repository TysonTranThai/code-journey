import type { Metadata } from "next";

import { TrackCard } from "@/components/learn/CourseCard";
import { getServerI18n } from "@/lib/i18n/server";
import { getTracks } from "@/lib/curriculum/loaders";
import { siteConfig } from "@/lib/site-config";
import { Logo } from "@/components/brand/Logo";

export async function generateMetadata(): Promise<Metadata> {
  const { d } = await getServerI18n();
  return {
    title: d.learnIndex.seoTitle,
    description: d.learnIndex.seoDescription,
    alternates: { canonical: `${siteConfig.url}/learn` },
  };
}

export default async function LearnIndexPage() {
  const { d, locale } = await getServerI18n();
  const tracks = getTracks(undefined, locale);
  return (
    <div className="flex flex-col gap-10">
      <header className="flex flex-col gap-4">
        <div className="inline-flex items-center gap-2 self-start rounded-md border border-emerald-500/30 bg-[#0d1424] px-3.5 py-1 text-xs font-mono font-medium text-emerald-300 shadow-[0_0_12px_rgba(34,197,94,0.2)]">
          <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-400" aria-hidden="true" />
          <span>{d.learnIndex.hubBadge}</span>
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-5xl">
          {d.learnIndex.title}
        </h1>
        <p className="max-w-2xl text-base text-zinc-300 leading-relaxed font-normal">
          {d.learnIndex.subtitle}
        </p>

        {/* Sensei Welcome Note */}
        <div className="conductor-window mt-2 flex items-center gap-3.5 rounded-xl border border-white/[0.08] bg-[#0c101b] p-4 max-w-2xl shadow-lg">
          <Logo size="sm" />
          <p className="text-xs text-zinc-300 leading-relaxed font-mono">
            <strong className="text-emerald-300 font-semibold">{d.learnIndex.senseiRole}</strong>{" "}
            <span>{d.learnIndex.senseiNote}</span>
          </p>
        </div>
      </header>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {tracks.map((track) => (
          <TrackCard key={track.id} track={track} courseCount={track.courses.length} />
        ))}
      </div>
    </div>
  );
}
