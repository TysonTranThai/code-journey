"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

import { useI18n } from "@/lib/i18n/provider";
import { logoutAction } from "@/server/actions/logout";

import { LanguageSwitcher } from "./LanguageSwitcher";
import { Logo } from "@/components/brand/Logo";

interface SiteHeaderClientProps {
  signedIn: boolean;
  userName: string | null;
  /** True while session state is hydrating client-side (07-08). */
  ariaBusy?: boolean;
}

const NAV_LINKS: readonly {
  href: string;
  labelKey: "learn" | "dashboard";
  signedInOnly?: boolean;
}[] = [
  { href: "/learn", labelKey: "learn" },
  { href: "/dashboard", labelKey: "dashboard", signedInOnly: true },
];

export function SiteHeaderClient({ signedIn, userName, ariaBusy = false }: SiteHeaderClientProps) {
  const [menuOpen, setMenuOpen] = useState(false);
  const pathname = usePathname();
  const { d } = useI18n();

  const navLabel = (key: "learn" | "dashboard") =>
    key === "learn" ? d.nav.learn : d.nav.dashboard;

  return (
    <header className="border-b border-white/[0.08] bg-[#07090e]/85 backdrop-blur-xl sticky top-0 z-40 transition-colors shadow-[0_4px_30px_rgba(0,0,0,0.6)]" aria-busy={ariaBusy || undefined}>
      <nav
        aria-label={d.nav.main}
        className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6 2xl:max-w-[1800px]"
      >
        <div className="flex items-center gap-7">
          <Link
            href="/"
            className="group flex items-center gap-2.5 text-base font-semibold tracking-tight text-white hover:text-emerald-400 transition-colors"
          >
            <Logo size="md" />
            <span className="flex items-center gap-1.5 font-bold tracking-tight">
              <span className="text-zinc-100 group-hover:text-emerald-400 transition-colors">Code Journey</span>
              <span className="text-emerald-400 text-xs font-mono" aria-hidden="true">■</span>
            </span>
          </Link>

          <div className="hidden items-center gap-1.5 sm:flex">
            {NAV_LINKS.filter((link) => !link.signedInOnly || signedIn).map((link) => {
              const active = pathname === link.href || (link.href === "/learn" && pathname.startsWith("/learn"));
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  className={`rounded-md px-3.5 py-1.5 text-sm font-medium transition-all ${
                    active
                      ? "bg-[#141d2f] text-emerald-300 border border-emerald-500/30 shadow-[0_0_15px_rgba(34,197,94,0.15)]"
                      : "text-zinc-400 hover:text-zinc-200 hover:bg-white/[0.04]"
                  }`}
                >
                  <span className="mr-1.5 text-xs text-emerald-400/80 font-mono" aria-hidden="true">
                    {link.href === "/learn" ? "→" : "⚡"}
                  </span>
                  {navLabel(link.labelKey)}
                </Link>
              );
            })}
          </div>
        </div>

        {/* Desktop auth section */}
        <div className="hidden items-center gap-3 sm:flex">
          <LanguageSwitcher />
          {signedIn ? (
            <>
              <div className="flex h-9 items-center gap-2 rounded-lg border border-white/[0.08] bg-[#0c101b] px-3 text-xs font-mono text-zinc-200 shadow-sm">
                <span className="relative flex h-2 w-2">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
                </span>
                <span className="max-w-[140px] truncate font-medium">{userName}</span>
              </div>
              <form action={logoutAction}>
                <button
                  type="submit"
                  className="btn-conductor-secondary flex h-9 items-center rounded-lg px-3.5 text-xs font-semibold text-zinc-300 hover:text-white transition-colors"
                >
                  {d.nav.logout}
                </button>
              </form>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="btn-conductor-secondary flex h-9 items-center rounded-lg px-4 text-xs font-semibold text-zinc-300 hover:text-white transition-colors"
              >
                {d.nav.login}
              </Link>
              <Link
                href="/register"
                className="btn-conductor-primary group flex h-9 items-center rounded-lg px-4 text-xs font-bold shadow-[0_0_20px_rgba(34,197,94,0.4)]"
              >
                <span>{d.nav.signup}</span>
                <span className="ml-1 text-xs font-mono transition-transform duration-150 group-hover:translate-x-0.5" aria-hidden="true">→</span>
              </Link>
            </>
          )}
        </div>

        {/* Mobile disclosure button */}
        <button
          type="button"
          className="rounded-full border border-white/[0.1] bg-white/[0.05] p-2 text-zinc-300 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 sm:hidden"
          aria-expanded={menuOpen}
          aria-controls="mobile-menu"
          aria-label={menuOpen ? d.nav.closeMenu : d.nav.openMenu}
          onClick={() => setMenuOpen((open) => !open)}
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            {menuOpen ? (
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              />
            ) : (
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
              />
            )}
          </svg>
        </button>
      </nav>

      {/* Mobile menu panel */}
      {menuOpen ? (
        <div id="mobile-menu" className="border-t border-white/[0.08] bg-[#07090e]/95 px-4 py-4 backdrop-blur-xl sm:hidden">
          <div className="flex flex-col gap-2">
            {NAV_LINKS.filter((link) => !link.signedInOnly || signedIn).map((link) => {
              const active = pathname === link.href || (link.href === "/learn" && pathname.startsWith("/learn"));
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  onClick={() => setMenuOpen(false)}
                  className={`rounded-lg px-4 py-2.5 text-sm font-medium transition-all ${
                    active
                      ? "bg-[#141d2f] text-emerald-300 border border-emerald-500/30"
                      : "text-zinc-300 hover:bg-white/[0.04]"
                  }`}
                >
                  <span className="mr-2 text-xs text-emerald-400 font-mono" aria-hidden="true">
                    {link.href === "/learn" ? "→" : "⚡"}
                  </span>
                  {navLabel(link.labelKey)}
                </Link>
              );
            })}

            {/* Mobile language switch */}
            <div className="pt-2 border-t border-white/[0.06] flex items-center justify-between px-2">
              <span className="text-xs font-mono text-zinc-400">{d.language.label}</span>
              <LanguageSwitcher />
            </div>

            {signedIn ? (
              <div className="flex flex-col gap-2 pt-2 border-t border-white/[0.06]">
                <div className="flex items-center gap-2 rounded-lg border border-white/[0.08] bg-[#0c101b] px-4 py-2.5 text-xs font-mono text-zinc-200">
                  <span className="relative flex h-2 w-2">
                    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                    <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
                  </span>
                  <span className="truncate">{userName}</span>
                </div>
                <form action={logoutAction} className="w-full">
                  <button
                    type="submit"
                    className="btn-conductor-secondary w-full py-2.5 text-sm font-semibold"
                  >
                    {d.nav.logout}
                  </button>
                </form>
              </div>
            ) : (
              <div className="flex flex-col gap-2 pt-2 border-t border-white/[0.06]">
                <Link
                  href="/login"
                  onClick={() => setMenuOpen(false)}
                  className="btn-conductor-secondary w-full py-2.5 text-sm font-semibold"
                >
                  {d.nav.login}
                </Link>
                <Link
                  href="/register"
                  onClick={() => setMenuOpen(false)}
                  className="btn-conductor-primary group w-full py-2.5 text-sm font-bold shadow-[0_0_20px_rgba(34,197,94,0.4)]"
                >
                  <span>{d.nav.signup}</span>
                  <span className="ml-1 text-xs font-mono transition-transform duration-150 group-hover:translate-x-0.5" aria-hidden="true">→</span>
                </Link>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </header>
  );
}
