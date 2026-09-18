import "server-only";

import { cookies } from "next/headers";

import { DEFAULT_LOCALE, isLocale, LOCALE_COOKIE, type Locale } from "./config";
import { createI18n, type I18n } from "./index";

/**
 * Server-side locale resolution: the `cj_locale` cookie, validated against
 * the locale list (unknown/absent → English default). Read once per request
 * by layouts/pages; also used by server actions that return user-facing
 * messages (auth, run API) so error strings follow the learner's language.
 */
export async function getServerLocale(): Promise<Locale> {
  const store = await cookies();
  const value = store.get(LOCALE_COOKIE)?.value;
  return isLocale(value) ? value : DEFAULT_LOCALE;
}

/** Server I18n helper bound to the request's locale. */
export async function getServerI18n(): Promise<I18n> {
  return createI18n(await getServerLocale());
}

/** Set the locale cookie (used by the switcher's server action). */
export async function setLocaleCookie(locale: Locale): Promise<void> {
  const store = await cookies();
  store.set(LOCALE_COOKIE, locale, {
    path: "/",
    maxAge: 60 * 60 * 24 * 365,
    sameSite: "lax",
    httpOnly: false, // client reads it for immediate optimistic UI
    secure: process.env.NODE_ENV === "production",
  });
}
