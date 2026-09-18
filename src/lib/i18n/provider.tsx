"use client";

import { createContext, useContext, useMemo, type ReactNode } from "react";

import { createI18n, type I18n } from "@/lib/i18n";
import { HTML_LANG, type Locale } from "@/lib/i18n/config";

/**
 * Client i18n provider: the root layout resolves the locale server-side
 * (cookie) and seeds this context, so client components translate without
 * fetching or hydration mismatches — the server render and first client
 * render both read the same `locale` prop.
 */

const I18nContext = createContext<I18n | null>(null);

export function I18nProvider({ locale, children }: { locale: Locale; children: ReactNode }) {
  // Memoized so consumers' effects/callbacks keyed on the helper stay stable
  // (createI18n is pure per-locale; identity changes only when locale does).
  const value = useMemo(() => createI18n(locale), [locale]);
  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

/** Use inside client components; falls back to English if no provider exists. */
export function useI18n(): I18n {
  return useContext(I18nContext) ?? createI18n("en");
}

/** Re-exported for components that need the html lang for Intl formatting. */
export { HTML_LANG };
export type { Locale };
