/**
 * i18n configuration (Site language feature).
 *
 * Model: a single `cj_locale` cookie decides the UI language for the whole
 * site. The root layout reads it (server), seeds a client provider, and the
 * language switcher updates it via a server action — no URL changes, so
 * existing links/bookmarks stay valid and SEO stays single-locale (course
 * content itself is English; UI chrome translates).
 *
 * Deliberately dependency-free: two typed dictionaries + a tiny formatter,
 * maintained in-repo. If a third locale arrives, add it to LOCALES + a
 * dictionary file; the compiler enforces completeness via `Dictionary`.
 */

export const LOCALES = ["en", "vi"] as const;
export type Locale = (typeof LOCALES)[number];

export const DEFAULT_LOCALE: Locale = "en";

/** Cookie that persists the learner's language choice (1 year, SameSite=Lax). */
export const LOCALE_COOKIE = "cj_locale";

/** BCP 47 tag for <html lang> and Intl date formatting. */
export const HTML_LANG: Record<Locale, string> = {
  en: "en",
  vi: "vi",
};

/** Locale tag for Intl/toLocaleDateString. */
export const INTL_TAG: Record<Locale, string> = {
  en: "en-US",
  vi: "vi-VN",
};

export function isLocale(value: string | undefined | null): value is Locale {
  return value === "en" || value === "vi";
}

/** Replace `{name}` placeholders in a dictionary template. Missing keys stay visible. */
export function fmt(template: string, vars: Record<string, string | number>): string {
  return template.replace(/\{(\w+)\}/g, (match, key: string) =>
    key in vars ? String(vars[key]) : match,
  );
}
