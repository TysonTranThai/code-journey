---
phase: 04-progress-achievements
plan: 01
---

# Plan 04-01 Report: Progress Backbone (Verified Events + Achievements)

**Completed:** 2026-09-02

## What Was Built

1. **Schema + migration 0003**: `progress_events` (append-only; PK on (userId, contentType, contentId) doubles as the idempotency constraint; index on (userId, createdAt)) and `achievements` (PK on (userId, achievementId)). No updatedAt columns anywhere.
2. **Pure streak util** (`src/lib/progress/streak.ts`): consecutive-day runs anchored on today/yesterday, UTC day keys, gap reset, duplicate-day tolerance.
3. **Achievement defs as content-as-data** (`src/content/achievements.json` + zod loader): first-lesson, five-lessons, first-challenge, first-streak-3, html-foundations-complete.
4. **Recording lib** (`src/lib/progress/recording.ts`):
   - `recordLessonCompletion` verifies server-side: lesson exists + EVERY attached challenge has a passing submission by this user (ProgressVerificationError otherwise) → idempotent insert (PROG-02)
   - `recordChallengeCompletion` inserts the event idempotently (only called from the verdict path)
   - `maybeAwardAchievements` derives awards from events + passing submissions, inserts with onConflictDoNothing, errors never propagate (D-08)
5. **Verdict hook** (`src/lib/execution/queue.ts` completeJob): a `passed` verdict on an attributed (non-anonymous) submission triggers challenge completion recording — progress derives from the sandbox verdict, not client claims. Anonymous runs record nothing.
6. **Lesson API** (`POST /api/progress/lesson`): 401 anonymous / 400 invalid / 403 unverified / 404 unknown / 201 recorded / 200 idempotent-repeat.

## Note on Migrations

`drizzle-kit migrate` hit a known failure mode applying 0003 (CREATE TYPE from an aborted prior attempt). The migration SQL was applied manually via psql with the migration hash registered in `drizzle.__drizzle_migrations`; `pnpm db:migrate` verified green afterward. Fresh environments (`pnpm db:reset`) are unaffected.

## Verification

- typecheck 0 errors; **tests 67/67** (8 streak + 8 achievements/verification new; PROG-02 negative + idempotency tests present)
- Verified behaviors: forged completion → ProgressVerificationError; double completion → 1 row; challenge event derived from recordChallengeCompletion; award idempotency

## Files

- `src/lib/db/schema.ts` (+progressEvents, achievements), `src/lib/db/migrations/0003_gigantic_karnak.sql`
- `src/lib/progress/streak.ts`, `achievement-defs.ts`, `recording.ts`, `src/content/achievements.json` (new)
- `src/lib/execution/queue.ts` (verdict hook), `src/app/api/progress/lesson/route.ts` (new)
- `tests/unit/streak.test.ts`, `tests/unit/achievements.test.ts` (new)

## Requirements Covered

PROG-01 (event model), PROG-02 (server-verified writes + negative tests), PROG-03 (streak computation), PROG-04 (defs + idempotent server awards).
