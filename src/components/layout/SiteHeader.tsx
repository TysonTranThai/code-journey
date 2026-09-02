import { SiteHeaderClient } from "./SiteHeaderClient";
import { auth } from "@/lib/auth/config";

/**
 * Server shell: reads the session server-side (PLAT-08 — the client never
 * decides auth state) and renders the responsive header (PLAT-06).
 */
export async function SiteHeader() {
  const session = await auth();
  return (
    <SiteHeaderClient signedIn={Boolean(session?.user)} userName={session?.user?.name ?? null} />
  );
}
