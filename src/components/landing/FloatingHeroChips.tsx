"use client";

interface FloatingHeroChipsProps {
  dict: {
    pythonChip: string;
    pythonChipSub: string;
    streakChip: string;
    streakChipSub: string;
    sandboxChip: string;
    sandboxChipSub: string;
    webChip: string;
    webChipSub: string;
  };
}

export function FloatingHeroChips({ dict }: FloatingHeroChipsProps) {
  return (
    <>
      {/* Floating Left Top Chip: Python */}
      <div
        className="hidden xl:flex items-center gap-2.5 absolute -left-12 top-16 z-10 rounded-xl border border-emerald-500/30 bg-[#0a1020]/90 px-3.5 py-2 text-xs font-mono text-zinc-200 shadow-[0_0_30px_rgba(16,185,129,0.18)] backdrop-blur-md animate-float-slow hover:border-emerald-400 hover:shadow-[0_0_35px_rgba(34,197,94,0.35)] transition-all cursor-default select-none"
        aria-hidden="true"
      >
        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-500/15 text-emerald-400 font-bold border border-emerald-500/30 shadow-[0_0_12px_rgba(34,197,94,0.3)]">
          🐍
        </span>
        <div className="flex flex-col">
          <span className="font-semibold text-emerald-300 tracking-tight">{dict.pythonChip}</span>
          <span className="text-[10px] text-zinc-400 font-mono">{dict.pythonChipSub}</span>
        </div>
      </div>

      {/* Floating Left Bottom Chip: Streak & XP */}
      <div
        className="hidden xl:flex items-center gap-2.5 absolute -left-16 bottom-10 z-10 rounded-xl border border-amber-500/30 bg-[#120e0a]/90 px-3.5 py-2 text-xs font-mono text-zinc-200 shadow-[0_0_30px_rgba(245,158,11,0.15)] backdrop-blur-md animate-float-delayed hover:border-amber-400 hover:shadow-[0_0_35px_rgba(245,158,11,0.3)] transition-all cursor-default select-none"
        aria-hidden="true"
      >
        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-500/15 text-amber-400 font-bold border border-amber-500/30 shadow-[0_0_12px_rgba(245,158,11,0.3)]">
          🔥
        </span>
        <div className="flex flex-col">
          <span className="font-semibold text-amber-300 tracking-tight">{dict.streakChip}</span>
          <span className="text-[10px] text-zinc-400 font-mono">{dict.streakChipSub}</span>
        </div>
      </div>

      {/* Floating Right Top Chip: Docker Linux Sandbox */}
      <div
        className="hidden xl:flex items-center gap-2.5 absolute -right-12 top-14 z-10 rounded-xl border border-cyan-500/30 bg-[#081320]/90 px-3.5 py-2 text-xs font-mono text-zinc-200 shadow-[0_0_30px_rgba(6,182,212,0.18)] backdrop-blur-md animate-float-delayed hover:border-cyan-400 hover:shadow-[0_0_35px_rgba(6,182,212,0.35)] transition-all cursor-default select-none"
        aria-hidden="true"
      >
        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-cyan-500/15 text-cyan-400 font-bold border border-cyan-500/30 shadow-[0_0_12px_rgba(6,182,212,0.3)]">
          🛡️
        </span>
        <div className="flex flex-col">
          <span className="font-semibold text-cyan-300 tracking-tight">{dict.sandboxChip}</span>
          <span className="text-[10px] text-zinc-400 font-mono">{dict.sandboxChipSub}</span>
        </div>
      </div>

      {/* Floating Right Bottom Chip: Web Mastery */}
      <div
        className="hidden xl:flex items-center gap-2.5 absolute -right-16 bottom-12 z-10 rounded-xl border border-purple-500/30 bg-[#120a1d]/90 px-3.5 py-2 text-xs font-mono text-zinc-200 shadow-[0_0_30px_rgba(168,85,247,0.18)] backdrop-blur-md animate-float-slow hover:border-purple-400 hover:shadow-[0_0_35px_rgba(168,85,247,0.35)] transition-all cursor-default select-none"
        aria-hidden="true"
      >
        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-purple-500/15 text-purple-400 font-bold border border-purple-500/30 shadow-[0_0_12px_rgba(168,85,247,0.3)]">
          🌐
        </span>
        <div className="flex flex-col">
          <span className="font-semibold text-purple-300 tracking-tight">{dict.webChip}</span>
          <span className="text-[10px] text-zinc-400 font-mono">{dict.webChipSub}</span>
        </div>
      </div>
    </>
  );
}
