import { index, integer, pgEnum, pgTable, primaryKey, text, timestamp } from "drizzle-orm/pg-core";
import { randomUUID } from "node:crypto";

/**
 * Phase 2 identity schema.
 *
 * The database stores USER-GENERATED STATE ONLY (docs/DATA-MODEL.md principle 2):
 * auth tables + profiles. Curriculum is content-as-data under src/content/ —
 * deliberately NOT database rows. Progress/submissions/discussions tables land
 * in Phases 3–5.
 *
 * users/accounts/sessions/verification_tokens follow the Auth.js Drizzle
 * adapter's expected shape (https://authjs.dev/getting-started/adapters/drizzle).
 */

export const userRole = pgEnum("user_role", ["student", "admin"]);

export const users = pgTable(
  "users",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    name: text("name"),
    email: text("email").notNull().unique(),
    emailVerified: timestamp("email_verified", { withTimezone: true }),
    image: text("image"),
    role: userRole("role").notNull().default("student"),
    /** bcrypt hash; null for OAuth-only users. */
    passwordHash: text("password_hash"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index("users_email_idx").on(t.email)],
);

export const accounts = pgTable(
  "accounts",
  {
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    type: text("type").notNull(),
    provider: text("provider").notNull(),
    providerAccountId: text("provider_account_id").notNull(),
    refreshToken: text("refresh_token"),
    accessToken: text("access_token"),
    expiresAt: integer("expires_at"),
    tokenType: text("token_type"),
    scope: text("scope"),
    idToken: text("id_token"),
    sessionState: text("session_state"),
  },
  (t) => [
    primaryKey({
      name: "accounts_provider_provider_account_id_pk",
      columns: [t.provider, t.providerAccountId],
    }),
    index("accounts_user_id_idx").on(t.userId),
  ],
);

export const sessions = pgTable(
  "sessions",
  {
    sessionToken: text("session_token").primaryKey(),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    expires: timestamp("expires", { withTimezone: true }).notNull(),
  },
  (t) => [index("sessions_user_id_idx").on(t.userId)],
);

export const verificationTokens = pgTable(
  "verification_tokens",
  {
    identifier: text("identifier").notNull(),
    token: text("token").notNull(),
    expires: timestamp("expires", { withTimezone: true }).notNull(),
  },
  (t) => [
    primaryKey({
      name: "verification_tokens_identifier_token_pk",
      columns: [t.identifier, t.token],
    }),
  ],
);

/**
 * Password reset tokens (AUTH-05). Raw tokens are NEVER stored — only the
 * sha256 hex of the raw token. Single-use via usedAt; 1-hour expiry enforced
 * by src/lib/auth/reset-token.ts.
 */
export const passwordResetTokens = pgTable(
  "password_reset_tokens",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    tokenHash: text("token_hash").notNull().unique(),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
    usedAt: timestamp("used_at", { withTimezone: true }),
  },
  (t) => [index("password_reset_tokens_user_id_idx").on(t.userId)],
);

export const profiles = pgTable("profiles", {
  userId: text("user_id")
    .primaryKey()
    .references(() => users.id, { onDelete: "cascade" }),
  displayName: text("display_name").notNull(),
  bio: text("bio"),
  avatarUrl: text("avatar_url"),
});

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type Profile = typeof profiles.$inferSelect;
