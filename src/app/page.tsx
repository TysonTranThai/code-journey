import Link from "next/link";
import { siteConfig } from "@/lib/site-config";

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col bg-zinc-950 text-zinc-100">
      <header className="border-b border-zinc-800">
        <nav
          aria-label="Main"
          className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4"
        >
          <span className="text-lg font-semibold tracking-tight">{siteConfig.name}</span>
          <span className="text-sm text-zinc-400">v0.1.0 — foundation</span>
        </nav>
      </header>

      <main
        id="main-content"
        className="mx-auto flex w-full max-w-6xl flex-1 flex-col items-center justify-center gap-6 px-6 py-24 text-center"
      >
        <h1 className="max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
          Learn to code. <span className="text-indigo-400">Free, forever.</span>
        </h1>
        <p className="max-w-2xl text-lg text-zinc-400">{siteConfig.description}</p>
        <p className="text-sm text-zinc-500">
          Under active development — Phase 1 (development foundation). The curriculum, challenges,
          and AI mentor ship in upcoming phases.
        </p>
        <Link
          href="/health"
          className="rounded-lg bg-indigo-500 px-5 py-2.5 font-medium text-white transition-colors hover:bg-indigo-400"
        >
          View health check
        </Link>
      </main>

      <footer className="border-t border-zinc-800">
        <div className="mx-auto max-w-6xl px-6 py-6 text-sm text-zinc-500">
          Free and open education. Built in the open.
        </div>
      </footer>
    </div>
  );
}
