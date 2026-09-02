import type { Metadata } from "next";
import Link from "next/link";

import { noIndexMetadata } from "@/lib/seo";
import { siteConfig } from "@/lib/site-config";

// PLAT-07: auth pages are private — never indexed.
export const metadata: Metadata = noIndexMetadata("Account");

export default function AuthLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="flex min-h-[calc(100vh-8rem)] flex-col items-center justify-center px-4 py-12">
      <Link
        href="/"
        className="mb-8 text-lg font-semibold tracking-tight text-zinc-100 hover:text-white"
      >
        {siteConfig.name}
      </Link>
      <div className="w-full max-w-md rounded-xl border border-zinc-800 bg-zinc-900/60 p-6 sm:p-8">
        {children}
      </div>
    </div>
  );
}
