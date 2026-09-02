"use server";

import { redirect } from "next/navigation";

import { signOut } from "@/lib/auth/config";

/** Sign the user out everywhere (AUTH-04) and return to the landing page. */
export async function logoutAction(): Promise<void> {
  await signOut({ redirectTo: "/" });
}
