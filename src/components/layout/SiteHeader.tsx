"use client";

import { useSession } from "next-auth/react";

import { SiteHeaderClient } from "./SiteHeaderClient";

/**
 * Client session bridge (07-08): the root layout stays static (no server
 * `auth()`), so the header hydrates its auth state via useSession(). While
 * loading it renders a stable signed-out shell (the public default) with
 * aria-busy instead of flickering; hydration swaps in the user menu.
 *
 * This is cosmetic only — never a trust boundary. Every protected page and
 * action still enforces authorization server-side (requireUser/auth()).
 */
export function SiteHeader() {
  const { status, data } = useSession();
  const signedIn = status === "authenticated" && Boolean(data?.user);
  return (
    <SiteHeaderClient
      signedIn={signedIn}
      userName={signedIn ? (data?.user?.name ?? null) : null}
      ariaBusy={status === "loading"}
    />
  );
}
