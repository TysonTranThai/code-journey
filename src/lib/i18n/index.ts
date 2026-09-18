import { fmt, type Locale } from "./config";
import { getDictionary, pluralForm, type Dictionary, type Plural } from "./dictionaries";

/**
 * Shared translation helpers (client-safe; the server wrapper adds cookie
 * reading). `t` translates a template with `{var}` interpolation; `tp`
 * resolves a plural entry for a count.
 */
export interface I18n {
  locale: Locale;
  /** The full dictionary — useful for records/maps (e.g. difficulty labels). */
  d: Dictionary;
  /** Translate: t("dashboard.welcome", { name }) or t.d.welcome — dot paths resolve via d. */
  t: (template: string, vars?: Record<string, string | number>) => string;
  /** Plural translate: tp(count, d.cards.trackCta) */
  tp: (count: number, forms: Plural, vars?: Record<string, string | number>) => string;
}

/**
 * Build an I18n helper for a locale. Templates are resolved through `fmt`
 * against the FLAT template string passed in — for dot-path convenience the
 * client provider and server helper both pre-resolve via `d` records.
 */
export function createI18n(locale: Locale): I18n {
  const d = getDictionary(locale);
  return {
    locale,
    d,
    t: (template, vars) => (vars ? fmt(template, vars) : template),
    tp: (count, forms, vars) => {
      const template = pluralForm(locale, count, forms);
      return fmt(template, { count, ...vars });
    },
  };
}
