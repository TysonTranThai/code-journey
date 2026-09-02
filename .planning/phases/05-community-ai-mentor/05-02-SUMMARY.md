---
phase: 05-community-ai-mentor
plan: 02
---

# Plan 05-02 Report: Pedagogy-First AI Mentor

**Completed:** 2026-09-02

## What Was Built

1. **Adapter seam** (`src/lib/mentor/types.ts`): `MentorAdapter` (hint/explainError), `MentorContext`, `MentorResponse`, `HintLevel` 1..3, `mentorAvailable()` env check. Provider-agnostic — a real adapter plugs in when `MENTOR_API_KEY` + provider choice exist; nothing else changes.
2. **NullMentor** (`null-mentor.ts`, AI-04): the no-key adapter composes graduated hints FROM the challenge's own content test-hints (real value, no fabricated API); error explanation surfaces the failing test + its hint with static debugging guidance.
3. **Guardrails** (`guardrails.ts`): `refuseIfSolution` regex heuristics (complete html documents, "here's the solution" framings, copy-paste directives, long fenced code dumps) returning a teach-first refusal; `frameHint` ladder framing. Enforced server-side before display.
4. **Rate limiting** (`rate-limit.ts` + `mentor_requests` table, migration 0005, AI-03): per-user daily quotas (10 hints / 20 explains, UTC-day windows), independent counters per kind.
5. **Server actions** (`src/server/actions/mentor.ts`): requireUser → quota → adapter → refusal filter → record. Anonymous users cannot invoke the mentor.
6. **MentorPanel UI** on the challenge page: hint button with level progression (1→3), "Explain my error" wired to the latest failing test from the verdict, refusal notice, sign-in prompt for anonymous users, disabled states; mentor section is part of the responsive workspace.

## Verification

- Refusal suite (ROADMAP Phase 5 criterion 2): 4 adversarial classes refused; 4 legitimate hint styles pass; NullMentor's own outputs asserted non-solution — **94/94 tests** overall (11 new mentor/discussion tests this plan-phase batch)
- Rate-limit integration: quota fills → blocked with friendly error; kinds independent; DB-gated skips clean
- Gates: typecheck 0 errors, lint clean, format clean, build green with all routes

## Files

- `src/lib/mentor/types.ts`, `null-mentor.ts`, `guardrails.ts`, `rate-limit.ts` (new)
- `src/lib/db/schema.ts` (+mentorRequests), `src/lib/db/migrations/0005_thankful_psynapse.sql`
- `src/server/actions/mentor.ts` (new)
- `src/components/challenge/MentorPanel.tsx` (new), `ChallengeWorkspace.tsx` (wiring), challenge page (props)
- `tests/unit/mentor-guardrails.test.ts`, `tests/integration/mentor-rate-limit.test.ts` (new)

## Requirements Covered

AI-01 (graduated hints, never solutions — proven), AI-02 (error explanation), AI-03 (per-user rate limits), AI-04 (graceful no-key degradation), PLAT-08 (server-side only).
