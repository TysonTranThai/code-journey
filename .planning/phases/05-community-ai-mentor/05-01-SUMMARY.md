---
phase: 05-community-ai-mentor
plan: 01
---

# Plan 05-01 Report: Lesson Discussions

**Completed:** 2026-09-02

## What Was Built

1. **Schema + migration 0004**: `discussion_threads` (lessonId content ref, userId FK cascade, title, index (lessonId, createdAt)) and `comments` (threadId FK cascade, userId FK cascade, body, index (threadId, createdAt)). Migration applied cleanly via drizzle-kit.
2. **Read lib** (`src/lib/discussions/threads.ts`, server-only): `getLessonThreads` (with comment counts + author names via joins), `getThread` (replies asc), `getThreadLessonId` (URL-context verification), `countLessonThreads`. Public queries — no auth (COMM-03).
3. **Server actions** (`src/server/actions/discussions.ts`): `createThread` / `addReply` — requireUser() first, zod bounds (title 200, body 4000), thread existence verified, authorship from session only, revalidatePath. Comments are plain text rendered by React (escaped; no dangerouslySetInnerHTML anywhere).
4. **Pages**: discussion index (breadcrumbs + thread list + ask form; anonymous users see sign-in prompt) and thread detail (original post highlighted + replies + reply form, verifying thread belongs to the URL's lesson). Lesson page gained a "Questions & discussion" nav card with thread count.

## Verification

- typecheck 0 errors, lint clean, **tests 94/94** (3 new discussion integration tests: thread+replies readable, cross-lesson isolation, user-deletion cascade)
- `pnpm build` includes `/learn/.../[lessonId]/discussion` + `/discussion/[threadId]` routes

## Files

- `src/lib/db/schema.ts` (+discussionThreads, comments), `src/lib/db/migrations/0004_typical_captain_midlands.sql`
- `src/lib/discussions/threads.ts`, `src/server/actions/discussions.ts` (new)
- `src/components/discussion/ThreadList.tsx`, `NewThreadForm.tsx`, `ReplyForm.tsx` (new)
- `src/app/(learn)/.../[lessonId]/discussion/page.tsx`, `.../discussion/[threadId]/page.tsx` (new), lesson `page.tsx` (discussion link)

## Requirements Covered

COMM-01 (post), COMM-02 (reply), COMM-03 (visitor read).
