import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { auth } from "@/lib/auth/config";
import { noIndexMetadata } from "@/lib/seo";
import { getServerI18n } from "@/lib/i18n/server";
import { getDashboardData } from "@/lib/progress/dashboard";

export async function generateMetadata(): Promise<Metadata> {
  const { d } = await getServerI18n();
  return noIndexMetadata(d.dashboard.title);
}

/**
 * Learner dashboard (PROG-01…04). Private page: no-index (PLAT-07),
 * authenticated access only. Server-rendered projection — the client never
 * asserts progress. Responsive: stacked cards on mobile, grid on desktop.
 */
export default async function DashboardPage() {
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) redirect("/login");

  const { d, t } = await getServerI18n();
  const { locale } = await getServerI18n();
  const data = await getDashboardData(userId, locale);
  const name = session.user?.name ?? d.dashboard.learner;
  const dayUnit = d.dashboard.day.other;

  return (
    <section className="mx-auto flex w-full max-w-6xl flex-col gap-8">
      {/* Adventurer Profile Header */}
      <header className="conductor-window rounded-xl flex flex-col gap-4 p-6 sm:flex-row sm:items-center sm:justify-between sm:p-7 shadow-xl bg-[#0c101b] border border-white/[0.1]">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <span className="badge-pixel badge-pixel-level font-mono">{d.dashboard.profileBadge}</span>
            <span className="badge-pixel badge-pixel-xp font-mono">{d.dashboard.levelBadge}</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            {t(d.dashboard.welcome, { name })}
          </h1>
          <p className="text-sm text-zinc-300 font-normal font-mono">{d.dashboard.progressNote}</p>
        </div>
        <div
          className="inline-flex items-center gap-2.5 self-start rounded-lg border border-orange-500/40 bg-orange-950/20 px-4 py-2 text-sm font-mono font-semibold text-orange-300 shadow-[0_0_20px_rgba(249,115,22,0.25)] cursor-default sm:self-center"
          aria-label={t(d.dashboard.streakAria, { count: data.streakDays, unit: dayUnit })}
        >
          <span className="text-xl" aria-hidden="true">🔥</span>
          <span className="font-semibold text-orange-200">
            {t(d.dashboard.inARow, { count: data.streakDays, unit: dayUnit })}
          </span>
        </div>
      </header>

      {data.continueLearning && (
        <Link
          href={data.continueLearning.href}
          className="conductor-window group rounded-xl flex items-center justify-between gap-4 p-5 border border-emerald-500/30 bg-[#0d1424] transition-all hover:border-emerald-400/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 shadow-xl"
        >
          <span className="flex flex-col gap-1.5">
            <span className="badge-pixel badge-pixel-quest self-start text-[10px] font-mono">
              {d.dashboard.continueLabel}
            </span>
            <span className="text-lg font-semibold text-white group-hover:text-emerald-300 transition-colors">
              {data.continueLearning.title}
            </span>
          </span>
          <span className="btn-conductor-primary group/btn inline-flex items-center gap-1.5 px-5 py-2.5 text-xs font-bold shadow-[0_0_15px_rgba(34,197,94,0.3)]">
            <span>{d.dashboard.resumeWorkspace}</span>
            <span className="font-mono transition-transform duration-150 group-hover/btn:translate-x-0.5" aria-hidden="true">→</span>
          </span>
        </Link>
      )}

      {/* Overall Progression Bar */}
      <div aria-label={d.dashboard.overallAria} className="conductor-window rounded-xl flex flex-col gap-3.5 p-5 shadow-xl bg-[#0c101b] border border-white/[0.08]">
        <div className="flex items-center justify-between text-xs font-mono font-semibold">
          <span className="uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
            <span>●</span> {d.dashboard.overallProgress}
          </span>
          <span className="text-zinc-300">
            {data.overall.completed}/{data.overall.total} · {data.overall.percent}%
          </span>
        </div>
        <div
          role="progressbar"
          aria-valuenow={data.overall.percent}
          aria-valuemin={0}
          aria-valuemax={100}
          className="h-2.5 overflow-hidden rounded-full border border-white/[0.08] bg-[#07090e] p-0.5"
        >
          <div
            className="h-full rounded-full bg-[#22c55e] transition-[width] motion-reduce:transition-none shadow-[0_0_12px_rgba(34,197,94,0.6)]"
            style={{ width: `${data.overall.percent}%` }}
          />
        </div>
      </div>

      {/* Per Track Realms Progress */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
        {data.perTrack.map((track) => (
          <div
            key={track.trackId}
            className="conductor-window rounded-xl flex flex-col justify-between gap-4 p-5 shadow-lg bg-[#0c101b] border border-white/[0.08]"
          >
            <div className="flex flex-col gap-3">
              <div className="flex items-center justify-between">
                <span className="badge-pixel badge-pixel-quest text-[10px] font-mono">{d.dashboard.trackBranchBadge}</span>
                <span className="font-mono text-xs font-semibold text-emerald-400">
                  {track.percent}%
                </span>
              </div>
              <h2 className="text-lg font-bold text-white">{track.trackTitle}</h2>
              <div
                role="progressbar"
                aria-valuenow={track.percent}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={t(d.dashboard.trackComplete, {
                  title: track.trackTitle,
                  percent: track.percent,
                })}
                className="h-2 overflow-hidden rounded-full border border-white/[0.08] bg-[#07090e]"
              >
                <div
                  className="h-full rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(34,197,94,0.4)]"
                  style={{ width: `${track.percent}%` }}
                />
              </div>
              <p className="font-mono text-xs text-zinc-400">
                {t(d.dashboard.itemsDone, {
                  done: track.completed,
                  total: track.total,
                  percent: track.percent,
                })}
              </p>
            </div>
            <Link
              href={`/learn/${track.trackId}`}
              className="btn-conductor-secondary group/btn inline-flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold self-start mt-2"
            >
              <span>{d.dashboard.openTrack}</span>
              <span className="font-mono transition-transform duration-150 group-hover/btn:translate-x-0.5" aria-hidden="true">→</span>
            </Link>
          </div>
        ))}
      </div>

      {/* Trophy Room & Collectible Achievements */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center gap-2">
          <span className="badge-pixel badge-pixel-level">{d.dashboard.trophyRoomBadge}</span>
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-white">{d.dashboard.achievements}</h2>
        <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data.achievements.map((achievement) => (
            <li
              key={achievement.id}
              className={`conductor-window rounded-xl flex items-start gap-4 p-5 transition-all ${
                achievement.earned
                  ? "border-amber-500/40 bg-amber-950/20 shadow-[0_0_20px_rgba(245,158,11,0.15)]"
                  : "border-white/[0.05] bg-[#0c101b]/50 opacity-40 grayscale"
              }`}
              data-locked={!achievement.earned || undefined}
            >
              <span className={`text-2xl ${achievement.earned ? "sparkle-icon" : ""}`} aria-hidden="true">
                {achievement.icon}
              </span>
              <span className="flex flex-col gap-1">
                <span className={`text-sm font-semibold ${achievement.earned ? "text-amber-200" : "text-zinc-400"}`}>
                  {achievement.title}
                  {achievement.earned ? "" : ` ${d.dashboard.locked}`}
                </span>
                <span className="text-xs text-zinc-400 leading-relaxed">{achievement.description}</span>
              </span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
