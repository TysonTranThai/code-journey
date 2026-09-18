import type { Metadata } from "next";
import Link from "next/link";

import { noIndexMetadata } from "@/lib/seo";
import { siteConfig } from "@/lib/site-config";
import { Logo } from "@/components/brand/Logo";

// PLAT-07: auth pages are private — never indexed.
export const metadata: Metadata = noIndexMetadata("Account");

export default function AuthLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="relative flex min-h-[calc(100vh-8rem)] flex-col items-center justify-center px-4 py-12">
      {/* Ambient Halftone Emerald Aura */}
      <div
        className="pointer-events-none absolute top-1/4 left-1/2 -z-10 h-[450px] w-[550px] -translate-x-1/2 rounded-full bg-emerald-500/15 blur-[100px]"
        aria-hidden="true"
      />

      <Link
        href="/"
        className="group mb-8 flex items-center gap-2.5 text-lg font-bold tracking-tight text-white hover:text-emerald-400 transition-colors"
      >
        <Logo size="sm" />
        <span className="flex items-center gap-1.5 font-bold tracking-tight">
          <span>{siteConfig.name}</span>
          <span className="text-emerald-400 text-xs font-mono" aria-hidden="true">■</span>
        </span>
      </Link>
      <div className="conductor-window w-full max-w-md rounded-xl p-6 sm:p-8 shadow-2xl bg-[#0c101b] border border-white/[0.1]">
        {children}
      </div>
    </div>
  );
}
