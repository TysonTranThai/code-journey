"use client";

import { useTransition } from "react";

import { useI18n } from "@/lib/i18n/provider";
import { setLocaleAction } from "@/server/actions/locale";

/**
 * Language switcher (EN ⇄ VI). The server action persists the `cj_locale`
 * cookie and revalidates, so every server component re-renders in the new
 * locale. `useTransition` keeps the button responsive during the refresh;
 * aria-pressed + a visible label keep it accessible (WCAG 2.1 AA).
 */
export function LanguageSwitcher() {
  const { locale, d } = useI18n();
  const [pending, startTransition] = useTransition();

  const nextLocale = locale === "en" ? "vi" : "en";
  const label = locale === "en" ? d.language.switchTo : d.language.switchToEn;

  return (
    <button
      type="button"
      onClick={() => startTransition(() => void setLocaleAction(nextLocale))}
      disabled={pending}
      aria-pressed={locale === "vi"}
      title={label}
      className="group inline-flex h-9 items-center gap-2 rounded-lg border border-white/[0.1] bg-[#0c101b] px-3 text-xs font-medium text-zinc-300 transition-all hover:border-emerald-500/40 hover:bg-[#111726] hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 disabled:opacity-60 shadow-sm"
    >
      <span aria-hidden="true" className="text-sm opacity-80 group-hover:opacity-100">🌐</span>
      <span aria-hidden="true" className="flex items-center gap-1 font-mono text-xs">
        <span className={locale === "en" ? "text-emerald-400 font-bold" : "text-zinc-300"}>EN</span>
        <span className="text-zinc-400 font-normal">/</span>
        <span className={locale === "vi" ? "text-emerald-400 font-bold" : "text-zinc-300"}>VI</span>
      </span>
      <span className="sr-only">{label}</span>
    </button>
  );
}
