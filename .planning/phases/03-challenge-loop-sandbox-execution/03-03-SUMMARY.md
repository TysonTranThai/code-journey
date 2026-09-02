---
phase: 03-challenge-loop-sandbox-execution
plan: 03
---

# Plan 03-03 Report: Challenge Content Model + Run API

**Completed:** 2026-09-02

## What Was Built

1. **Challenge content schema** (`src/lib/curriculum/schema.ts`): `challengeTestSchema` (name, code assertion snippet, educational `hint`) and `challengeSchema` (id, title, prompt, difficulty, boilerplate, ≥1 test) with `ResolvedChallenge` location type.
2. **Loader integration** (`src/lib/curriculum/loaders.ts`): lessons load challenges from `…/lessons/<lessonId>/challenges/<challengeId>.json`; dangling references, duplicates, and invalid JSON throw at load time → fail the build (CURR-04). Global id uniqueness extended to challenges. New accessors: `getLessonChallenges()` (declared order), `getChallenge()` (fully resolved).
3. **Seed challenges** (content-as-data, real test code):
   - `fix-the-heading` on introduction-to-html — 3 tests (uses `<h1>`, no leftover `<p>`, text preserved) with educational hints
   - `add-the-missing-link` on html-links — 3 tests (anchor present, href exact, visible text exact)
4. **Run API** — `POST /api/challenges/run`: zod-validated body, challenge resolved server-side (client never supplies tests), submission snapshot recorded (userId null when anonymous per CHAL-03), execution job enqueued, returns `202 { submissionId, jobId }`.
5. **Verdict polling API** — `GET /api/challenges/run/[submissionId]`: `202 { status }` while pending, `200` with verdict/per-test results/runtime/output once the worker writes it.
6. **Negative fixture** — `tests/fixtures/content-invalid/challenge-unknown-lesson/` proves dangling challenge references fail loudly.

## Verification

- `pnpm typecheck` — 0 errors
- `pnpm test` — 52/52 (3 new: challenge loading/resolution, unknown-challenge error, dangling-reference fixture throw)
- Live loader check: both seed challenges resolve with correct lesson linkage and test counts

## Files

- `src/lib/curriculum/schema.ts`, `src/lib/curriculum/loaders.ts` (extended)
- `src/app/api/challenges/run/route.ts`, `src/app/api/challenges/run/[submissionId]/route.ts` (new)
- 2 challenge JSON files + 2 lesson JSON updates (new)
- `tests/fixtures/content-invalid/challenge-unknown-lesson/**` (new)
- `tests/unit/curriculum-loaders.test.ts` (+3 tests)

## Requirements Covered

CHAL-01, CHAL-02, CHAL-03, CURR-04.
