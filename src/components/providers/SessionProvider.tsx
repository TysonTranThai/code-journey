"use client";

import { SessionProvider as NextAuthSessionProvider } from "next-auth/react";

/**
 * Client session context (07-08): lets the header hydrate auth state via
 * next-auth/react without a server `auth()` call in the root layout — which
 * would force every route (including static public content) to render
 * dynamically. Authorization itself is never derived from this context;
 * protected pages/actions still enforce server-side via requireUser/auth().
 */
export function SessionProvider({ children }: { children: React.ReactNode }) {
  return <NextAuthSessionProvider>{children}</NextAuthSessionProvider>;
}
