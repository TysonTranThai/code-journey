import Link from "next/link";

import { getServerI18n } from "@/lib/i18n/server";
import { getTracks } from "@/lib/curriculum/loaders";
import { Logo } from "@/components/brand/Logo";
import { LandingLoader } from "@/components/landing/LandingLoader";
import { FloatingHeroChips } from "@/components/landing/FloatingHeroChips";
import { HowItWorksSection } from "@/components/landing/HowItWorksSection";
import { QuestRoadmapSection } from "@/components/landing/QuestRoadmapSection";

export default async function HomePage() {
  const { d, tp, t, locale } = await getServerI18n();
  const tracks = getTracks(undefined, locale);

  return (
    <main
      id="main-content"
      className="relative mx-auto flex w-full max-w-6xl flex-1 flex-col items-center gap-20 px-4 py-12 sm:px-6 sm:py-20 2xl:max-w-[1800px] overflow-x-clip"
    >
      {/* Cyberpunk Developer Terminal Loading Screen Animation */}
      <LandingLoader dict={d.loader} />

      {/* Radiant Emerald Halftone Atmosphere Backdrop with Feathered Mask */}
      <div
        className="pointer-events-none absolute -top-32 left-1/2 -z-10 h-[900px] w-screen max-w-[100vw] -translate-x-1/2 bg-halftone-atmosphere opacity-90 overflow-hidden"
        aria-hidden="true"
      />

      {/* Hero Section */}
      <section className="relative flex flex-col items-center text-center gap-6 max-w-4xl pt-2">
        {/* Floating Gamified Tech & Quest Chips */}
        <FloatingHeroChips dict={d.heroChips} />

        {/* Subtle Stardust Ambient Twinkles */}
        <div className="pointer-events-none absolute inset-0 -top-8 overflow-hidden" aria-hidden="true">
          <span className="star-particle h-1.5 w-1.5 bg-emerald-400/80 top-8 left-[12%]" style={{ animationDelay: "0s", animationDuration: "3.5s" }} />
          <span className="star-particle h-1 w-1 bg-teal-300/70 top-24 right-[15%]" style={{ animationDelay: "1.2s", animationDuration: "4.2s" }} />
          <span className="star-particle h-2 w-2 bg-emerald-300/60 top-48 left-[5%]" style={{ animationDelay: "2.1s", animationDuration: "5s" }} />
          <span className="star-particle h-1.5 w-1.5 bg-lime-400/70 top-60 right-[8%]" style={{ animationDelay: "0.7s", animationDuration: "3.8s" }} />
          <span className="star-particle h-1 w-1 bg-emerald-200/90 top-[360px] left-[20%]" style={{ animationDelay: "1.8s", animationDuration: "4.5s" }} />
          <span className="star-particle h-1.5 w-1.5 bg-teal-400/70 top-[420px] right-[22%]" style={{ animationDelay: "2.6s", animationDuration: "4s" }} />
        </div>

        {/* Brand Logo Emblem with Radar Beacon */}
        <div className="animate-hero-logo">
          <Logo size="xl" />
        </div>

        <div className="animate-hero-badge inline-flex items-center gap-2 rounded-md border border-emerald-500/30 bg-[#0d1424] px-3.5 py-1 text-xs font-mono font-medium text-emerald-300 shadow-[0_0_20px_rgba(34,197,94,0.2)]">
          <span className="flex h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#22c55e]" aria-hidden="true" />
          <span>{d.home.taglinePlatform}</span>
          <span className="text-zinc-400" aria-hidden="true">·</span>
          <span>{d.home.taglineAi}</span>
        </div>

        <h1 className="animate-hero-title text-4xl font-extrabold tracking-tight text-white sm:text-6xl sm:leading-[1.12]">
          {d.home.heroPrefix}{" "}
          <span className="text-aurora-glow font-extrabold">
            {d.home.heroAccent}
          </span>
        </h1>

        <p className="animate-hero-desc max-w-2xl text-base text-zinc-300 sm:text-lg leading-relaxed font-normal">
          {d.home.description}
        </p>

        <div className="animate-hero-actions flex flex-col items-center gap-4 pt-2 sm:flex-row">
          <Link
            href="/learn"
            className="btn-conductor-primary group px-8 py-3 text-sm font-bold shadow-[0_0_25px_rgba(34,197,94,0.45)] min-h-11"
          >
            <span>{d.home.startLearning}</span>
            <span className="ml-1.5 font-mono transition-transform duration-200 group-hover:translate-x-1" aria-hidden="true">→</span>
          </Link>
          <Link
            href="/learn/web-development/web-development-beginner"
            className="btn-conductor-secondary px-6 py-3 text-sm font-medium min-h-11"
          >
            {d.home.jumpInto}
          </Link>
        </div>

        <div className="animate-hero-actions flex items-center gap-2 text-xs text-zinc-400 font-mono pt-1">
          <span className="text-emerald-400">●</span>
          <span>{d.home.featureLine}</span>
        </div>
      </section>

      {/* Full-Fidelity Conductor 3-Pane + Terminal IDE Mockup */}
      <section aria-label={d.home.mockupAria} className="relative w-full max-w-5xl animate-ide-window">
        {/* Radiant Emerald Ambient Backlight with Slow Breathing Pulse */}
        <div
          className="pointer-events-none absolute -inset-4 -z-10 rounded-3xl bg-gradient-to-r from-emerald-500/25 via-teal-500/20 to-lime-500/20 blur-3xl opacity-80 ambient-glow-pulse"
          aria-hidden="true"
        />

        <div className="border-beam-container shadow-[0_25px_60px_-15px_rgba(0,0,0,0.9),0_0_50px_rgba(34,197,94,0.18)]">
          <div className="conductor-window relative z-10 w-full overflow-hidden rounded-xl !border-0 bg-[#0c101b]">
          {/* Conductor Window Titlebar */}
          <div className="flex items-center justify-between border-b border-white/[0.08] bg-[#080c14] px-4 py-2.5">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5" aria-hidden="true">
                <span className="h-3 w-3 rounded-full bg-rose-500/80 inline-block" />
                <span className="h-3 w-3 rounded-full bg-amber-500/80 inline-block" />
                <span className="h-3 w-3 rounded-full bg-emerald-500/80 inline-block" />
              </div>
              <div className="h-4 w-px bg-white/10" />
              <div className="flex items-center gap-2 text-xs font-mono text-zinc-300">
                <span className="text-emerald-400 font-semibold flex items-center gap-1">
                  <span>🌿</span>
                  <span>{d.home.mockupBranch}</span>
                </span>
                <span className="text-zinc-600" aria-hidden="true">/</span>
                <span className="text-zinc-400 hidden sm:inline">{d.home.mockupPath}</span>
                <span className="text-zinc-400 text-[10px]" aria-hidden="true">{d.home.mockupOpen}</span>
              </div>
            </div>
            <div className="flex items-center gap-2.5">
              <span className="hidden sm:inline-flex items-center gap-1.5 rounded-full bg-[#111726] border border-white/10 px-2.5 py-0.5 text-[11px] font-mono text-zinc-300">
                <span className="text-emerald-400">{d.home.mockupPr}</span>
                <span className="text-zinc-400" aria-hidden="true">·</span>
                <span className="text-emerald-300">{d.home.mockupReady}</span>
              </span>
              <button
                type="button"
                className="btn-conductor-primary px-3 py-1 text-xs font-bold shadow-[0_0_15px_rgba(34,197,94,0.3)]"
                aria-label={d.home.mockupRunAria}
              >
                <span>{d.home.mockupRun}</span>
              </button>
            </div>
          </div>

          {/* Conductor 3-Column Body */}
          <div className="grid grid-cols-1 md:grid-cols-12 min-h-[380px]">
            {/* Left Column: Explorer & Workspaces */}
            <div className="conductor-sidebar md:col-span-3 p-3 flex flex-col justify-between border-b md:border-b-0">
              <div className="flex flex-col gap-3">
                <div className="flex items-center justify-between text-xs font-semibold text-zinc-400">
                  <span className="flex items-center gap-1.5">
                    <span>🏠</span> {d.home.mockupHome}
                  </span>
                </div>

                <div className="flex flex-col gap-1">
                  <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400 uppercase tracking-wider px-1">
                    <span>{d.home.mockupWorkspaces}</span>
                    <span className="text-zinc-400">▾</span>
                  </div>

                  {/* Active Challenge Workspace Card */}
                  <div className="rounded-lg bg-[#141d2e] border border-emerald-500/30 p-2 shadow-sm">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono font-semibold text-white truncate">
                        {d.home.mockupBranch}
                      </span>
                      <div className="flex items-center gap-1">
                        <span className="badge-diff-add">+18</span>
                        <span className="badge-diff-del">-2</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-zinc-400 font-mono mt-1">
                      <span>{d.home.mockupTagAlgorithms} · {d.home.mockupInProgress}</span>
                      <span className="text-zinc-400">⌘1</span>
                    </div>
                  </div>

                  {/* Inactive Workspace 2 */}
                  <div className="rounded-lg hover:bg-white/[0.03] p-2 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono text-zinc-300 truncate">
                        two-sum-hashmap
                      </span>
                      <span className="badge-diff-add">+24 -4</span>
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-zinc-400 font-mono mt-0.5">
                      <span>{d.home.mockupTagArrays} · {d.home.mockupVerified}</span>
                      <span className="text-zinc-400">⌘2</span>
                    </div>
                  </div>

                  {/* Inactive Workspace 3 */}
                  <div className="rounded-lg hover:bg-white/[0.03] p-2 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono text-zinc-400 truncate">
                        lru-cache-impl
                      </span>
                      <span className="text-[10px] text-zinc-400">{d.home.mockupLocked}</span>
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-zinc-400 font-mono mt-0.5">
                      <span>{d.home.mockupTagStructures}</span>
                      <span className="text-zinc-400">⌘3</span>
                    </div>
                  </div>
                </div>

                <div className="flex flex-col gap-1 pt-1 border-t border-white/[0.06]">
                  <div className="flex items-center justify-between text-[11px] font-mono text-zinc-400 uppercase tracking-wider px-1">
                    <span>{d.home.mockupCurriculum}</span>
                    <span className="text-zinc-400">▾</span>
                  </div>
                  <div className="text-xs text-zinc-300 px-1 py-0.5 flex items-center justify-between">
                    <span>{d.home.mockupWebDev}</span>
                    <span className="text-[10px] font-mono text-zinc-400">{t(d.home.mockupModulesUnit, { count: 12 })}</span>
                  </div>
                  <div className="text-xs text-zinc-300 px-1 py-0.5 flex items-center justify-between">
                    <span>{d.home.mockupPython}</span>
                    <span className="text-[10px] font-mono text-zinc-400">{t(d.home.mockupModulesUnit, { count: 8 })}</span>
                  </div>
                  <div className="text-xs text-zinc-300 px-1 py-0.5 flex items-center justify-between">
                    <span>{d.home.mockupSystems}</span>
                    <span className="text-[10px] font-mono text-zinc-400">{t(d.home.mockupModulesUnit, { count: 14 })}</span>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-white/[0.06] text-[11px] text-zinc-400 flex items-center justify-between font-mono">
                <span>{d.home.mockupNewChallenge}</span>
                <span className="text-emerald-400">{d.home.mockupOnline}</span>
              </div>
            </div>

            {/* Center Column: Interactive Coding & AI Pairing Session */}
            <div className="md:col-span-6 p-3 flex flex-col justify-between border-b md:border-b-0 border-r border-white/[0.07] bg-[#090d17]">
              {/* Tab Header */}
              <div className="flex items-center gap-2 border-b border-white/[0.07] pb-2 text-xs font-mono">
                <span className="text-zinc-400">{d.home.mockupAllChanges}</span>
                <span className="rounded bg-[#141d2f] border border-emerald-500/30 text-emerald-300 px-2.5 py-0.5 font-semibold flex items-center gap-1.5">
                  <span>✨</span>
                  <span>{d.home.mockupDebugTopic}</span>
                </span>
                <span className="text-zinc-400 hidden lg:inline" aria-hidden="true">+</span>
              </div>

              {/* Diagnostic Box */}
              <div className="my-2 rounded-lg border border-rose-500/30 bg-rose-950/20 p-2.5 text-xs font-mono text-rose-300 leading-snug">
                <span className="text-rose-400 font-bold">AssertionError:</span> expected false to be true in @isPalindrome(&quot;race a car&quot;)
              </div>

              {/* Collapsible Activity Pill */}
              <div className="rounded-md border border-white/10 bg-[#0e1320] px-2.5 py-1.5 text-[11px] font-mono text-zinc-300 flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-emerald-400">›</span>
                  <span>{d.home.mockupActivity}</span>
                </div>
                <span className="badge-diff-add">+4 -1</span>
              </div>

              {/* Sensei AI Dialogue Card */}
              <div className="rounded-lg border border-emerald-500/25 bg-[#0b1222]/80 p-3 text-xs text-zinc-300 leading-relaxed shadow-sm">
                <div className="flex items-center gap-2 mb-1.5 font-mono text-emerald-300 font-semibold text-[11px]">
                  <span className="flex h-2 w-2 rounded-full bg-emerald-400" />
                  <span>{d.home.mockupSenseiRole}</span>
                </div>
                <p>
                  &quot;{d.home.mockupSenseiText}&quot;
                </p>
              </div>

              {/* Learner Follow-up */}
              <div className="my-2 rounded-lg border border-white/[0.08] bg-[#0d1220] p-2.5 text-xs font-mono text-zinc-300">
                <p className="text-zinc-400 text-[10px] uppercase tracking-wider mb-1 font-semibold">{d.home.mockupLearnerRole}</p>
                <p>&quot;{d.home.mockupLearnerText}&quot;</p>
              </div>

              {/* Summary telemetry */}
              <div className="rounded-md border border-emerald-500/30 bg-emerald-950/20 px-2.5 py-1 text-[11px] font-mono text-emerald-300 flex items-center justify-between">
                <span>{d.home.mockupSummaryTitle}</span>
                <span className="font-bold">{d.home.mockupTestsPassed}</span>
              </div>
            </div>

            {/* Right Column: Changes & Test Suite Inspector */}
            <div className="md:col-span-3 p-3 flex flex-col justify-between bg-[#080c14]">
              <div className="flex flex-col gap-2.5">
                <div className="flex items-center justify-between border-b border-white/[0.07] pb-2 text-xs font-mono text-zinc-300">
                  <span className="font-semibold">{d.home.mockupTestsCount}</span>
                  <span className="text-emerald-400 text-[11px]">{d.home.mockupAllPassing}</span>
                </div>

                <div className="flex flex-col gap-1.5 text-xs font-mono">
                  <div className="flex items-center justify-between text-zinc-300 py-0.5">
                    <span className="truncate">src/Solution.ts</span>
                    <span className="badge-diff-add">+12 -2</span>
                  </div>
                  <div className="flex items-center justify-between text-zinc-400 py-0.5">
                    <span className="truncate">src/types.ts</span>
                    <span className="badge-diff-add">+4</span>
                  </div>

                  <div className="mt-2 pt-2 border-t border-white/[0.06] flex flex-col gap-1.5 text-[11px]">
                    <div className="flex items-center gap-1.5 text-emerald-400">
                      <span>✓</span>
                      <span className="text-zinc-300 truncate">{d.home.mockupTest1}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-emerald-400">
                      <span>✓</span>
                      <span className="text-zinc-300 truncate">{d.home.mockupTest2}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-emerald-400">
                      <span>✓</span>
                      <span className="text-zinc-300 truncate">{d.home.mockupTest3}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-emerald-400">
                      <span>✓</span>
                      <span className="text-zinc-300 truncate">{d.home.mockupTest4}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-white/[0.06] text-[11px] font-mono text-zinc-400 flex items-center justify-between">
                <span>{d.home.mockupCoverage}</span>
                <span className="text-emerald-400 font-semibold">{d.home.mockupSandboxOk}</span>
              </div>
            </div>
          </div>

          {/* Bottom Dock: Docked Terminal */}
          <div className="conductor-terminal px-4 py-2.5 flex items-center justify-between text-xs text-zinc-300">
            <div className="flex items-center gap-2 font-mono">
              <span className="text-emerald-400" aria-hidden="true">→</span>
              <span className="text-sky-300">code-journey</span>
              <span className="text-zinc-400" aria-hidden="true">git:(</span>
              <span className="text-emerald-300">{d.home.mockupBranch}</span>
              <span className="text-zinc-400" aria-hidden="true">)</span>
              <span className="text-zinc-200">pnpm test:sandbox</span>
              <span className="terminal-cursor h-3.5 w-1.5 bg-emerald-400" aria-hidden="true" />
            </div>
            <div className="hidden sm:flex items-center gap-3 text-[11px] font-mono text-zinc-400">
              <span className="text-emerald-400">{d.home.mockupTerminalPassed}</span>
              <span>11ms</span>
              <span className="text-zinc-400">{d.home.mockupTerminalEnv}</span>
            </div>
          </div>
        </div>
      </div>
      </section>

      {/* Interactive 4-Step How It Works Flow */}
      <div className="w-full animate-realms">
        <HowItWorksSection dict={d.howItWorks} />
      </div>

      {/* Featured Learning Realms / Tracks Section */}
      <section aria-labelledby="realms-heading" className="w-full flex flex-col gap-8 pt-4 animate-realms">
        <div className="flex flex-col items-center text-center gap-2">
          <span className="badge-pixel badge-pixel-quest">{d.home.realmsBadge}</span>
          <h2 id="realms-heading" className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
            {d.home.realmsTitle}
          </h2>
          <p className="max-w-xl text-sm text-zinc-400">
            {d.home.realmsSubtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {tracks.map((track) => (
            <div
              key={track.id}
              className="glass-card flex flex-col justify-between p-6 group rounded-xl"
            >
              <div className="flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <span className="badge-pixel badge-pixel-level">{d.home.realmsTrackBadge}</span>
                  <span className="font-mono text-xs font-semibold text-zinc-400">
                    {tp(track.courses.length, d.cards.courses)}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white group-hover:text-emerald-400 transition-colors">
                  {track.title}
                </h3>
                <p className="text-sm text-zinc-400 leading-relaxed">
                  {track.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-white/[0.06] flex items-center justify-between">
                <span className="text-xs font-mono text-zinc-400">{d.home.realmsBeginner}</span>
                <Link
                  href={`/learn/${track.id}`}
                  className="btn-conductor-secondary group/btn px-4 py-1.5 text-xs font-semibold hover:border-emerald-400/40"
                >
                  <span>{d.cards.exploreTrack}</span>
                  <span className="ml-1 font-mono transition-transform duration-150 group-hover/btn:translate-x-0.5" aria-hidden="true">→</span>
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Gamified RPG Campaign Roadmap Tree */}
      <div className="w-full animate-pillars">
        <QuestRoadmapSection dict={d.questMap} />
      </div>

      {/* Bento Grid: Why Code Journey */}
      <section aria-labelledby="why-heading" className="w-full flex flex-col gap-8 pt-4 animate-pillars">
        <div className="flex flex-col items-center text-center gap-2">
          <span className="badge-pixel badge-pixel-streak">{d.home.pillarsBadge}</span>
          <h2 id="why-heading" className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
            {d.home.pillarsTitle}
          </h2>
          <p className="max-w-xl text-sm text-zinc-400">
            {d.home.pillarsSubtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div className="glass-card card-glow-hover p-6 flex flex-col gap-3.5 rounded-xl">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 text-lg shadow-[0_0_12px_rgba(34,197,94,0.2)]">
              ⚡
            </div>
            <h3 className="font-semibold text-base text-zinc-100">{d.home.pillar1Title}</h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              {d.home.pillar1Desc}
            </p>
          </div>

          <div className="glass-card card-glow-hover p-6 flex flex-col gap-3.5 rounded-xl">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 text-lg shadow-[0_0_12px_rgba(34,197,94,0.2)]">
              🛡️
            </div>
            <h3 className="font-semibold text-base text-zinc-100">{d.home.pillar2Title}</h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              {d.home.pillar2Desc}
            </p>
          </div>

          <div className="glass-card card-glow-hover p-6 flex flex-col gap-3.5 rounded-xl">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 text-lg shadow-[0_0_12px_rgba(34,197,94,0.2)]">
              🤖
            </div>
            <h3 className="font-semibold text-base text-zinc-100">{d.home.pillar3Title}</h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              {d.home.pillar3Desc}
            </p>
          </div>

          <div className="glass-card card-glow-hover p-6 flex flex-col gap-3.5 rounded-xl">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 text-lg shadow-[0_0_12px_rgba(34,197,94,0.2)]">
              💎
            </div>
            <h3 className="font-semibold text-base text-zinc-100">{d.home.pillar4Title}</h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              {d.home.pillar4Desc}
            </p>
          </div>
        </div>
      </section>

      {/* Bottom CTA Card with Ambient Spotlight */}
      <section className="relative w-full overflow-hidden rounded-2xl border border-white/[0.1] bg-gradient-to-b from-[#0c1222] to-[#070912] p-8 sm:p-14 flex flex-col items-center text-center gap-6 shadow-2xl animate-pillars">
        <div
          className="pointer-events-none absolute -bottom-20 left-1/2 -z-10 h-[300px] w-[500px] -translate-x-1/2 rounded-full bg-emerald-500/20 blur-[100px]"
          aria-hidden="true"
        />
        <Logo size="lg" />
        <div className="flex flex-col gap-2 max-w-xl">
          <h2 className="text-2xl font-bold tracking-tight text-white sm:text-4xl">
            {d.home.ctaTitle}
          </h2>
          <p className="text-sm text-zinc-300 leading-relaxed">
            {d.home.ctaSubtitle}
          </p>
        </div>
        <Link
          href="/learn"
          className="btn-conductor-primary group px-8 py-3 text-sm font-bold shadow-xl min-h-11"
        >
          <span>{d.home.startLearning}</span>
          <span className="ml-1.5 font-mono transition-transform duration-200 group-hover:translate-x-1" aria-hidden="true">→</span>
        </Link>
      </section>
    </main>
  );
}

