"use client";

import { useEffect, useState } from "react";
import { Logo } from "@/components/brand/Logo";

interface LandingLoaderProps {
  dict: {
    bootTitle: string;
    phase1: string;
    phase2: string;
    phase3: string;
    phase4: string;
    statusDone: string;
    memory: string;
    sandbox: string;
    progressLabel: string;
    ping: string;
    ready: string;
    ariaLabel: string;
    execRuntime: string;
    sysLoad: string;
  };
}

const TOTAL_PHOSPHOR_BLOCKS = 22;

export function LandingLoader({ dict }: LandingLoaderProps) {
  const [phaseIndex, setPhaseIndex] = useState(0);
  const [filledBlocks, setFilledBlocks] = useState(2);
  const [percent, setPercent] = useState(8);
  const [scrambleText, setScrambleText] = useState(dict.phase1);
  const [isExiting, setIsExiting] = useState(false);
  const [isFinished, setIsFinished] = useState(false);

  const phases = [dict.phase1, dict.phase2, dict.phase3, dict.phase4];

  // Scramble / Decrypt text animator
  useEffect(() => {
    const target = phases[phaseIndex] || dict.phase4;
    const chars = "01#_*/[]<>&$%!?~+=";
    let iteration = 0;
    const interval = setInterval(() => {
      setScrambleText(
        target
          .split("")
          .map((letter, idx) => {
            if (idx < iteration) return target[idx];
            if (letter === " " || letter === "/" || letter === "_") return letter;
            return chars[Math.floor(Math.random() * chars.length)];
          })
          .join(""),
      );

      if (iteration >= target.length) {
        clearInterval(interval);
      }
      iteration += 1;
    }, 28);

    return () => clearInterval(interval);
  }, [phaseIndex, dict]);

  // Orchestrated Timeline (~2.9s duration before iris reveal)
  useEffect(() => {
    // Prevent browser auto-scroll restoration and pin viewport to top
    if (typeof window !== "undefined") {
      if ("scrollRestoration" in window.history) {
        window.history.scrollRestoration = "manual";
      }
      window.scrollTo(0, 0);
    }

    if (
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      document.documentElement.dataset.pageReady = "true";
      const timer = setTimeout(() => setIsFinished(true), 0);
      return () => clearTimeout(timer);
    }

    // Mark page as waiting for loader sequence
    document.documentElement.dataset.pageReady = "false";

    // Step 1: Tracing AST (0 - 700ms)
    const t1 = setTimeout(() => {
      setFilledBlocks(6);
      setPercent(28);
    }, 400);

    // Step 2: Spawning Sandbox (750ms - 1450ms)
    const t2 = setTimeout(() => {
      setPhaseIndex(1);
      setFilledBlocks(11);
      setPercent(52);
    }, 750);

    // Step 3: Socratic Sensei Neural Sync (1500ms - 2200ms)
    const t3 = setTimeout(() => {
      setPhaseIndex(2);
      setFilledBlocks(17);
      setPercent(82);
    }, 1500);

    // Step 4: Final charge to 100% (2250ms - 2650ms)
    const t4 = setTimeout(() => {
      setPhaseIndex(3);
      setFilledBlocks(TOTAL_PHOSPHOR_BLOCKS);
      setPercent(100);
    }, 2250);

    // Step 5: Cinematic Lens Flash & Trigger Page Power-On Cascade (2750ms)
    const tExit = setTimeout(() => {
      window.scrollTo(0, 0);
      document.documentElement.dataset.pageReady = "true";
      setIsExiting(true);
    }, 2750);

    // Step 6: Complete Unmount (3250ms)
    const tFinish = setTimeout(() => {
      setIsFinished(true);
      window.scrollTo(0, 0);
      if ("scrollRestoration" in window.history) {
        window.history.scrollRestoration = "auto";
      }
    }, 3250);

    return () => {
      document.documentElement.dataset.pageReady = "true";
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      clearTimeout(t4);
      clearTimeout(tExit);
      clearTimeout(tFinish);
    };
  }, []);

  if (isFinished) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      aria-label={dict.ariaLabel}
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#05070d] px-4 select-none overflow-hidden transition-all duration-500 ease-out ${
        isExiting
          ? "opacity-0 scale-105 pointer-events-none filter blur-[2px]"
          : "opacity-100 scale-100"
      }`}
    >
      {/* CRT Scanline & Phosphor Overlay */}
      <div
        className="crt-scanlines pointer-events-none absolute inset-0 opacity-40 z-10"
        aria-hidden="true"
      />

      {/* Sweeping Laser Beam */}
      <div
        className="scanline-beam pointer-events-none absolute inset-x-0 h-24 bg-gradient-to-b from-transparent via-emerald-500/10 to-transparent z-10"
        aria-hidden="true"
      />

      {/* Ambient Celestial Glow */}
      <div
        className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[550px] w-[550px] rounded-full bg-emerald-500/15 blur-[140px]"
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[280px] w-[280px] rounded-full bg-teal-400/20 blur-[80px]"
        aria-hidden="true"
      />

      {/* Centerpiece: Brand Logo & Rotating Radar Gyro */}
      <div className="relative mb-8 flex items-center justify-center">
        {/* Outer Orbit Radar */}
        <div
          className="animate-radar-sweep pointer-events-none absolute h-36 w-36 rounded-full border border-dashed border-emerald-500/30"
          aria-hidden="true"
        >
          <span className="absolute -top-1 left-1/2 -translate-x-1/2 h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#22c55e]" />
        </div>

        {/* Secondary Concentric Gyro */}
        <div
          className="pointer-events-none absolute h-44 w-44 rounded-full border border-white/[0.04]"
          aria-hidden="true"
        />

        {/* Brand Logo - 100% Identical to Site & Favicon */}
        <Logo size="xl" className="shadow-[0_0_40px_rgba(34,197,94,0.55)] scale-110" />
      </div>

      {/* Developer Compiler Terminal Console */}
      <div className="relative z-20 w-full max-w-lg rounded-xl border border-emerald-500/40 bg-[#080d19]/95 p-5 shadow-[0_0_60px_rgba(16,185,129,0.22)] backdrop-blur-xl">
        {/* Terminal Header */}
        <div className="flex items-center justify-between border-b border-white/[0.08] pb-3 mb-4">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_6px_#22c55e]" />
            <span className="font-mono text-xs font-bold tracking-wider text-emerald-300">
              {dict.bootTitle}
            </span>
          </div>
          <span className="font-mono text-[10px] text-zinc-400 tracking-widest uppercase">
            {percent === 100 ? dict.statusDone : dict.execRuntime}
          </span>
        </div>

        {/* Matrix Scrambled Phase Log */}
        <div className="min-h-[46px] flex flex-col justify-center">
          <div className="flex items-center gap-2 font-mono text-sm font-semibold text-white">
            <span className="text-emerald-400" aria-hidden="true">
              &gt;
            </span>
            <span className="tracking-wide text-zinc-100">{scrambleText}</span>
            <span className="h-4 w-2 bg-emerald-400 animate-pulse ml-0.5" aria-hidden="true" />
          </div>
        </div>

        {/* Tactile 22-Segment Phosphor Gauge */}
        <div className="mt-4 flex flex-col gap-2">
          <div className="flex items-center justify-between font-mono text-[11px]">
            <span className="text-zinc-400 tracking-wider">
              {percent === 100
                ? dict.ready
                : dict.sysLoad.replace("{current}", String(phaseIndex + 1))}
            </span>
            <span className="font-bold text-emerald-400 tracking-widest">{percent}%</span>
          </div>

          <div
            className="flex items-center gap-1.5 rounded-lg border border-white/[0.08] bg-black/60 p-1.5"
            role="progressbar"
            aria-label={dict.progressLabel}
            aria-valuenow={percent}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            {Array.from({ length: TOTAL_PHOSPHOR_BLOCKS }).map((_, i) => {
              const isFilled = i < filledBlocks;
              return (
                <div
                  key={i}
                  className={`h-3.5 flex-1 rounded-sm transition-all duration-150 ${
                    isFilled
                      ? "bg-gradient-to-t from-emerald-500 to-teal-300 shadow-[0_0_8px_rgba(52,211,153,0.85)]"
                      : "bg-zinc-800/40"
                  }`}
                />
              );
            })}
          </div>
        </div>

        {/* Real-Time Telemetry Ticker */}
        <div className="mt-4 pt-3 border-t border-white/[0.06] flex items-center justify-between text-[10px] font-mono text-zinc-400">
          <span className="flex items-center gap-1.5 text-zinc-400">
            <span className="h-1.5 w-1.5 rounded-full bg-teal-400/80" />
            {dict.memory}
          </span>
          <span className="hidden sm:inline-block text-zinc-400">{dict.sandbox}</span>
          <span className="text-emerald-400 font-medium">{dict.ping}</span>
        </div>
      </div>
    </div>
  );
}
