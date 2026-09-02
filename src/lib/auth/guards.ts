import "server-only";

import { eq } from "drizzle-orm";
import { redirect } from "next/navigation";

import { db } from "@/lib/db";
import { users } from "@/lib/db/schema";
import { auth } from "./config";

/**
 * Authorization guards (decision D-12). Authorization is enforced SERVER-SIDE
 * only — the client never decides what it may access (PLAT-08, SECURITY.md).
 *
 * requireUser(): anonymous visitors are redirected to /login.
 * requireRole(): fetches the user's role FRESH FROM THE DB (never from the
 * JWT) so role changes take effect immediately.
 */

export type Role = "student" | "admin";

/** Redirect anonymous users to /login; return the session when authenticated. */
export async function requireUser() {
  const session = await auth();
  if (!session?.user) {
    redirect("/login");
  }
  return session;
}

/** Load the current user's role fresh from the database (null if signed out). */
export async function getCurrentRole(): Promise<Role | null> {
  const session = await auth();
  if (!session?.user?.id) return null;
  const [user] = await db
    .select({ role: users.role })
    .from(users)
    .where(eq(users.id, session.user.id))
    .limit(1);
  return user?.role ?? null;
}

/** Throw for anonymous users; throw 403-style errors for insufficient roles. */
export async function requireRole(role: Role): Promise<void> {
  const session = await auth();
  if (!session?.user) {
    redirect("/login");
  }
  const current = await getCurrentRole();
  if (current !== role) {
    throw new Error(`Forbidden: requires role "${role}"`);
  }
}
