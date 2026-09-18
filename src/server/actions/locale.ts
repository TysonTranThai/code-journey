"use server";

import { revalidatePath } from "next/cache";

import { isLocale, type Locale } from "@/lib/i18n/config";
import { setLocaleCookie } from "@/lib/i18n/server";

/**
 * Persist the learner's language choice. Called from the header switcher;
 * `revalidatePath("/")` refreshes server-rendered UI in the current locale.
 */
export async function setLocaleAction(next: string): Promise<void> {
  if (!isLocale(next)) return;
  const locale: Locale = next;
  await setLocaleCookie(locale);
  revalidatePath("/", "layout");
}
