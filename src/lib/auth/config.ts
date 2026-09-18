import "server-only";

import { DrizzleAdapter } from "@auth/drizzle-adapter";
import { eq } from "drizzle-orm";
import NextAuth, { type NextAuthConfig } from "next-auth";
import Credentials from "next-auth/providers/credentials";
import GitHub from "next-auth/providers/github";

import { db } from "@/lib/db";
import { accounts, sessions, users, verificationTokens } from "@/lib/db/schema";
import { touchLastActive } from "@/lib/auth/activity";
import { verifyPassword } from "./password";

/**
 * Auth.js v5 configuration (decision D-01..D-05).
 *
 * - Credentials provider (email + bcrypt password) is always available.
 * - GitHub OAuth is env-gated: registered only when both GITHUB_CLIENT_ID and
 *   GITHUB_CLIENT_SECRET are set. Dev never needs fabricated credentials.
 * - Session strategy is "jwt" — REQUIRED while a Credentials provider exists
 *   (Auth.js cannot issue database sessions for Credentials sign-ins).
 */

/** GitHub provider is only registered when real credentials exist (D-05). */
export function githubProviderEnabled(): boolean {
  return Boolean(process.env.GITHUB_CLIENT_ID && process.env.GITHUB_CLIENT_SECRET);
}

function buildProviders(): NextAuthConfig["providers"] {
  const providers: NextAuthConfig["providers"] = [
    Credentials({
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      authorize: async (credentials) => {
        const email = credentials?.email;
        const password = credentials?.password;
        if (typeof email !== "string" || typeof password !== "string") {
          return null;
        }
        const [user] = await db
          .select()
          .from(users)
          .where(eq(users.email, email.toLowerCase()))
          .limit(1);
        if (!user?.passwordHash) return null;
        const valid = await verifyPassword(password, user.passwordHash);
        if (!valid) return null;
        // Never return the password hash to the session machinery.
        return { id: user.id, name: user.name, email: user.email, role: user.role };
      },
    }),
  ];

  if (githubProviderEnabled()) {
    providers.push(GitHub);
  }
  return providers;
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: DrizzleAdapter(db, {
    usersTable: users,
    accountsTable: accounts,
    sessionsTable: sessions,
    verificationTokensTable: verificationTokens,
  }),
  providers: buildProviders(),
  session: { strategy: "jwt" },
  pages: {
    signIn: "/login",
    error: "/login",
  },
  trustHost: true,
  callbacks: {
    jwt({ token, user }) {
      if (user?.id) {
        // Persist the user id — progress/authz checks key off session.user.id.
        token.id = user.id;
      }
      if (user?.role) {
        token.role = user.role;
      }
      return token;
    },
    session({ session, token }) {
      if (session.user) {
        if (typeof token.id === "string") {
          session.user.id = token.id;
        }
        if (
          typeof token.role === "string" &&
          (token.role === "student" || token.role === "admin")
        ) {
          session.user.role = token.role;
        }
      }
      // Qualifying account activity: any authenticated request that resolves
      // a session. Fire-and-forget + internally throttled (see activity.ts);
      // never awaited so session resolution stays fast.
      if (typeof token.id === "string" && token.id) {
        void touchLastActive(token.id);
      }
      return session;
    },
  },
});
