import type { HTMLAttributes } from "react";

interface LogoProps extends HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg" | "xl";
  beacon?: boolean;
}

const SIZE_MAP = {
  sm: {
    container: "h-6 w-6 rounded-md",
    svg: "h-4 w-4",
    beacon: "h-2 w-2 -bottom-0.5 -right-0.5",
  },
  md: {
    container: "h-8 w-8 rounded-lg",
    svg: "h-5 w-5",
    beacon: "h-2.5 w-2.5 -bottom-0.5 -right-0.5",
  },
  lg: {
    container: "h-11 w-11 rounded-xl",
    svg: "h-7 w-7",
    beacon: "h-3 w-3 -bottom-0.5 -right-0.5",
  },
  xl: {
    container: "h-14 w-14 rounded-2xl",
    svg: "h-9 w-9",
    beacon: "h-3.5 w-3.5 -bottom-1 -right-1",
  },
} as const;

/**
 * Code Journey Vector Brand Mark:
 * Merges terminal code chevrons (< / >) into an interlocking, upward-moving
 * "C" and "J" trajectory path with neon emerald to cyan gradients and an
 * ambient radar beacon.
 */
export function Logo({ size = "md", beacon = true, className = "", ...props }: LogoProps) {
  const config = SIZE_MAP[size];

  return (
    <div
      className={`relative inline-flex shrink-0 items-center justify-center bg-gradient-to-b from-[#0e1626] to-[#080d17] border border-emerald-500/40 shadow-[0_0_20px_rgba(34,197,94,0.35)] transition-all ${config.container} ${className}`}
      {...props}
    >
      <svg
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={`${config.svg} transition-transform duration-300 group-hover:scale-105`}
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="cj-grad-emerald" x1="2" y1="4" x2="30" y2="28" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#4ade80" />
            <stop offset="50%" stopColor="#22c55e" />
            <stop offset="100%" stopColor="#06b6d4" />
          </linearGradient>
          <filter id="cj-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="1.5" floodColor="#22c55e" floodOpacity="0.6" />
          </filter>
        </defs>

        {/* Left code bracket flowing into 'C' */}
        <path
          d="M13 8L6.5 14.5C5.7 15.3 5.7 16.7 6.5 17.5L13 24"
          stroke="url(#cj-grad-emerald)"
          strokeWidth="3.2"
          strokeLinecap="round"
          strokeLinejoin="round"
          filter="url(#cj-glow)"
        />

        {/* Dynamic journey trajectory slash connecting into 'J' curve */}
        <path
          d="M19 8L15.5 17.5C14.8 19.5 16 22 18.5 22H21C23.2 22 25 20.2 25 18V13.5"
          stroke="url(#cj-grad-emerald)"
          strokeWidth="3.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Code dot pulse */}
        <circle cx="21" cy="9" r="2" fill="#38bdf8" />
      </svg>

      {beacon && (
        <span className={`absolute ${config.beacon}`} aria-hidden="true">
          <span className="beacon-pulse" />
          <span className="relative block h-full w-full rounded-full bg-emerald-400 shadow-[0_0_8px_#22c55e]" />
        </span>
      )}
    </div>
  );
}
