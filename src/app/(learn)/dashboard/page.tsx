import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { auth } from "@/lib/auth/config";
import { noIndexMetadata } from "@/lib/seo";
import { getDashboardData } from "@/lib/progress/dashboard";

export const metadata: Metadata = noIndexMetadata("Your Dashboard");

/**
 * Learner dashboard (PROG-01…04). Private page: no-index (PLAT-07),
 * authenticated access only. Server-rendered projection — the client never
 * asserts progress. Responsive: stacked cards on mobile, grid on desktop.
 */
export default async function DashboardPage() {
  const session = await auth();
  const userId = session?.user?.id;
  if (!userId) redirect("/login");

  const data = await getDashboardData(userId);
  const name = session.user?.name ?? "Learner";

  return (
    <section className="mx-auto flex w-full max-w-6xl flex-col gap-8">
      <header className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-100 sm:text-3xl">
            Welcome back, {name}
          </h1>
          <p className="text-sm text-zinc-400">
            Your progress is recorded from verified completions only.
          </p>
        </div>
        <div
          className="inline-flex items-center gap-2 self-start rounded-lg border border-amber-700/60 bg-amber-950/40 px-4 py-2 text-amber-300"
          aria-label={`Streak: ${data.streakDays} consecutive ${data.streakDays === 1 ? "day" : "days"}`}
        >
          <span aria-hidden="true">🔥</span>
          <span className="text-sm font-semibold">
            {data.streakDays} {data.streakDays === 1 ? "day" : "days"} in a row
          </span>
        </div>
      </header>

      {data.continueLearning && (
        <Link
          href={data.continueLearning.href}
          className="flex items-center justify-between gap-4 rounded-xl border border-sky-500/40 bg-sky-950/30 px-5 py-4 transition-colors hover:border-sky-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-400"
        >
          <span className="flex flex-col gap-1">
            <span className="text-xs uppercase tracking-wide text-sky-300">
              Continue where you left off
            </span>
            <span className="font-medium text-zinc-100">{data.continueLearning.title}</span>
          </span>
          <span aria-hidden="true" className="text-sky-300">
            →
          </span>
        </Link>
      )}

      <div aria-label="Overall progress" className="flex flex-col gap-2">
        <div className="flex items-center justify-between text-sm text-zinc-300">
          <span>Overall progress</span>
          <span>
            {data.overall.completed}/{data.overall.total} · {data.overall.percent}%
          </span>
        </div>
        <div
          role="progressbar"
          aria-valuenow={data.overall.percent}
          aria-valuemin={0}
          aria-valuemax={100}
          className="h-2.5 overflow-hidden rounded-full bg-zinc-800"
        >
          <div
            className="h-full rounded-full bg-sky-500 transition-[width] motion-reduce:transition-none"
            style={{ width: `${data.overall.percent}%` }}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        {data.perTrack.map((track) => (
          <div
            key={track.trackId}
            className="flex flex-col gap-3 rounded-xl border border-zinc-800 bg-zinc-900/60 p-5"
          >
            <h2 className="text-sm font-medium text-zinc-200">{track.trackTitle}</h2>
            <div
              role="progressbar"
              aria-valuenow={track.percent}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label={`${track.trackTitle}: ${track.percent}% complete`}
              className="h-2 overflow-hidden rounded-full bg-zinc-800"
            >
              <div
                className="h-full rounded-full bg-emerald-500"
                style={{ width: `${track.percent}%` }}
              />
            </div>
            <p className="text-xs text-zinc-400">
              {track.completed}/{track.total} items · {track.percent}%
            </p>
            <Link
              href={`/learn/${track.trackId}`}
              className="text-xs text-sky-400 underline underline-offset-2 hover:text-sky-300"
            >
              Open track
            </Link>
          </div>
        ))}
      </div>

      <div className="flex flex-col gap-3">
        <h2 className="text-lg font-semibold text-zinc-100">Achievements</h2>
        <ul className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {data.achievements.map((achievement) => (
            <li
              key={achievement.id}
              className={`flex items-start gap-3 rounded-xl border p-4 ${
                achievement.earned
                  ? "border-emerald-700/60 bg-emerald-950/30"
                  : "border-zinc-800 bg-zinc-900/40 opacity-60"
              }`}
              // Locked achievements: conveyed via the (locked) suffix and
              // reduced contrast rather than aria-disabled (not supported
              // on role listitem).
              data-locked={!achievement.earned || undefined}
            >
              <span className="text-2xl" aria-hidden="true">
                {achievement.icon}
              </span>
              <span className="flex flex-col gap-1">
                <span className="text-sm font-medium text-zinc-100">
                  {achievement.title}
                  {achievement.earned ? "" : " (locked)"}
                </span>
                <span className="text-xs text-zinc-400">{achievement.description}</span>
              </span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
