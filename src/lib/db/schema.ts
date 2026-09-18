import {
  boolean,
  index,
  integer,
  jsonb,
  pgEnum,
  pgTable,
  primaryKey,
  text,
  timestamp,
  unique,
} from "drizzle-orm/pg-core";
import { randomUUID } from "node:crypto";

/**
 * Verdict written once by the runner worker (shape of
 * src/lib/execution/types.ts VerdictPayload). Typed on both execution_jobs
 * and submissions so queue/verdict code gets end-to-end types.
 */
export type StoredVerdict = {
  verdict: "passed" | "failed" | "timeout" | "error";
  perTestResults: { name: string; passed: boolean; message: string }[];
  runtimeMs: number | null;
  output: string;
};

/**
 * Phase 2 identity schema.
 *
 * The database stores USER-GENERATED STATE ONLY (docs/DATA-MODEL.md principle 2):
 * auth tables + profiles. Curriculum is content-as-data under src/content/ —
 * deliberately NOT database rows. Execution/submission tables (Phase 3) store
 * grading state; progress/discussions land in Phases 4–5.
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
    /**
     * Last qualifying account activity (sign-in / authenticated session
     * usage), written throttled by src/lib/auth/activity.ts. Nullable: NULL
     * means "no confidently-known activity" and the inactive-account cleanup
     * NEVER deletes such accounts (conservative default).
     */
    lastActiveAt: timestamp("last_active_at", { withTimezone: true }),
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
    // Property names follow the Auth.js adapter's expected schema shape.
    refresh_token: text("refresh_token"),
    access_token: text("access_token"),
    expires_at: integer("expires_at"),
    token_type: text("token_type"),
    scope: text("scope"),
    id_token: text("id_token"),
    session_state: text("session_state"),
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

/**
 * Immutable submission snapshots (03-CONTEXT D-07, DATA-MODEL principle 3).
 * No updatedAt — verdict fields are written once by the worker, never edited.
 * Anonymous runs record userId = null (CHAL-03: only logged-in submits count).
 */
export const submissions = pgTable(
  "submissions",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    /** Null for anonymous runs. */
    userId: text("user_id").references(() => users.id, { onDelete: "cascade" }),
    challengeId: text("challenge_id").notNull(),
    code: text("code").notNull(),
    verdict: text("verdict"),
    perTestResults: jsonb("per_test_results").$type<StoredVerdict["perTestResults"]>(),
    runtimeMs: integer("runtime_ms"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index("submissions_user_challenge_idx").on(t.userId, t.challengeId)],
);

/**
 * Execution lifecycle (03-CONTEXT D-03). One row per sandbox run request.
 * Workers claim via SELECT … FOR UPDATE SKIP LOCKED so multiple runner
 * processes can share the queue safely. Payload carries ONLY code + tests +
 * limits — never env vars or secrets.
 */
export const executionStatus = pgEnum("execution_status", [
  "queued",
  "claimed",
  "running",
  "completed",
  "failed",
]);

export const executionJobs = pgTable(
  "execution_jobs",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    submissionId: text("submission_id").references(() => submissions.id, {
      onDelete: "cascade",
    }),
    status: executionStatus("status").notNull().default("queued"),
    /** JobPayload — code + tests + limits only. */
    payload: jsonb("payload").notNull(),
    /** Final verdict, written once by the runner worker. */
    verdictPayload: jsonb("verdict_payload").$type<StoredVerdict>(),
    claimedBy: text("claimed_by"),
    claimedAt: timestamp("claimed_at", { withTimezone: true }),
    startedAt: timestamp("started_at", { withTimezone: true }),
    finishedAt: timestamp("finished_at", { withTimezone: true }),
    attempts: integer("attempts").notNull().default(0),
    error: text("error"),
    /** True once a worker wrote a final verdict into verdictPayload. */
    hasVerdict: boolean("has_verdict").notNull().default(false),
    // Millisecond precision: claimJob orders by created_at, so same-second
    // inserts must not collide (default clock_timestamp() is µs in PG16, but
    // be explicit for portability).
    createdAt: timestamp("created_at", { withTimezone: true, precision: 3 }).notNull().defaultNow(),
  },
  (t) => [index("execution_jobs_status_idx").on(t.status, t.createdAt)],
);

export type ExecutionJob = typeof executionJobs.$inferSelect;
export type NewExecutionJob = typeof executionJobs.$inferInsert;
export type Submission = typeof submissions.$inferSelect;
export type NewSubmission = typeof submissions.$inferInsert;

/**
 * Progress events (PROG-01/02): append-only, server-verified completions.
 * The UNIQUE constraint IS the completion flag — re-completing is a no-op.
 * No updatedAt: events are never edited. contentId references the
 * content-as-data id (lesson or challenge), not a DB row.
 */
export const progressContentType = pgEnum("progress_content_type", ["lesson", "challenge"]);

export const progressEvents = pgTable(
  "progress_events",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    contentType: progressContentType("content_type").notNull(),
    contentId: text("content_id").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true, precision: 3 }).notNull().defaultNow(),
  },
  (t) => [
    // Idempotency: one completion per (user, content). UNIQUE (not a second
    // PK — a table can only have one; this defect broke fresh deployments,
    // found in the Phase 9 deploy rehearsal).
    unique("progress_events_user_content_unique").on(t.userId, t.contentType, t.contentId),
    index("progress_events_user_created_idx").on(t.userId, t.createdAt),
  ],
);

/**
 * Achievement awards (PROG-04): rows are written ONLY by server-side award
 * evaluation (never client claims). Definitions live as content-as-data
 * (src/content/achievements.json); this table stores who earned what.
 */
export const achievements = pgTable(
  "achievements",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    achievementId: text("achievement_id").notNull(),
    awardedAt: timestamp("awarded_at", { withTimezone: true, precision: 3 }).notNull().defaultNow(),
  },
  (t) => [unique("achievements_user_achievement_unique").on(t.userId, t.achievementId)],
);

export type ProgressEvent = typeof progressEvents.$inferSelect;
export type NewProgressEvent = typeof progressEvents.$inferInsert;
export type Achievement = typeof achievements.$inferSelect;
export type NewAchievement = typeof achievements.$inferInsert;

/**
 * Discussion threads (COMM-01…03): anchored to a content-as-data lesson id.
 * Public read; authenticated write (enforced in server actions).
 */
export const discussionThreads = pgTable(
  "discussion_threads",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    lessonId: text("lesson_id").notNull(),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    title: text("title").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true, precision: 3 }).notNull().defaultNow(),
  },
  (t) => [index("discussion_threads_lesson_idx").on(t.lessonId, t.createdAt)],
);

export const comments = pgTable(
  "comments",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    threadId: text("thread_id")
      .notNull()
      .references(() => discussionThreads.id, { onDelete: "cascade" }),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    body: text("body").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true, precision: 3 }).notNull().defaultNow(),
  },
  (t) => [index("comments_thread_idx").on(t.threadId, t.createdAt)],
);

export type DiscussionThread = typeof discussionThreads.$inferSelect;
export type NewDiscussionThread = typeof discussionThreads.$inferInsert;
export type Comment = typeof comments.$inferSelect;
export type NewComment = typeof comments.$inferInsert;

/**
 * Mentor request log (AI-03): per-user daily quotas counted server-side.
 * Doubles as the audit trail for mentor usage (DATA-MODEL principle 5).
 */
export const mentorRequests = pgTable(
  "mentor_requests",
  {
    id: text("id")
      .primaryKey()
      .$defaultFn(() => randomUUID()),
    userId: text("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    kind: text("kind").notNull(), // 'hintsPerDay' | 'explainsPerDay'
    createdAt: timestamp("created_at", { withTimezone: true, precision: 3 }).notNull().defaultNow(),
  },
  (t) => [index("mentor_requests_user_idx").on(t.userId, t.createdAt)],
);

export type MentorRequest = typeof mentorRequests.$inferSelect;
export type NewMentorRequest = typeof mentorRequests.$inferInsert;

/**
 * Generic rate-limit counter (07-03). One row per (scope:key:window-bucket).
 * The count is incremented atomically via INSERT ... ON CONFLICT DO UPDATE, so
 * a check-and-increment is a single statement (no TOCTOU race). `expiresAt`
 * bounds the row so stale windows can be pruned.
 */
export const rateLimitEvents = pgTable("rate_limit_events", {
  key: text("key").primaryKey(),
  count: integer("count").notNull().default(1),
  windowStart: timestamp("window_start", { withTimezone: true }).notNull(),
  expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
});

export type RateLimitEvent = typeof rateLimitEvents.$inferSelect;
export type NewRateLimitEvent = typeof rateLimitEvents.$inferInsert;
