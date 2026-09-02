import Link from "next/link";

import { siteConfig } from "@/lib/site-config";

export default function HomePage() {
  return (
    <main
      id="main-content"
      className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center justify-center gap-6 px-6 py-24 text-center"
    >
      <h1 className="max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
        Learn to code. <span className="text-indigo-400">Free, forever.</span>
      </h1>
      <p className="max-w-2xl text-lg text-zinc-400">{siteConfig.description}</p>
      <div className="flex flex-col items-center gap-3 sm:flex-row">
        <Link
          href="/learn"
          className="rounded-lg bg-indigo-500 px-6 py-3 font-medium text-white transition-colors hover:bg-indigo-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
        >
          Start learning →
        </Link>
        <Link
          href="/learn/web-development/web-development-foundations"
          className="rounded-lg border border-zinc-700 px-6 py-3 font-medium text-zinc-200 transition-colors hover:border-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
        >
          Jump into HTML Foundations
        </Link>
      </div>
      <p className="text-sm text-zinc-500">
        Curriculum browsing is live. Auto-graded challenges, progress tracking, and the AI mentor
        ship in upcoming phases.
      </p>
    </main>
  );
}
