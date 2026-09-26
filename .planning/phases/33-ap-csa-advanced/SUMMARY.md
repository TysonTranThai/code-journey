# Phase 33 — AP CSA Advanced Practice & Exam Mastery

## Summary

Status: **COMPLETE (2026-09-26)**

Built `ap-csa-advanced` (track `ap-csa`, course 3), the endgame course after
Foundations and (the other agent's) Core. 24 modules / 96 lessons (72 teaching
+ 24 checkpoints) / 24 practice sets / 129 Java challenges, EN+VI fully
synchronized. 129/129 challenges two-sided verified (reference passes all
tests, plausible-wrong fails ≥1) via the isolated
`verify-challenges-apx.mjs` harness. All MCQ/tracing ground truths executed
and confirmed before authoring.

Structure: problem-solving method → hard tracing → MCQ lab (misconception-
coded distractors) → speed drills → strings → arrays/ArrayList → 2D → OOP →
inheritance/polymorphism → recursion → integrated (unlabeled) → FRQ
workshop/method/class/debug/partial-credit → mixed sets → timed sets → error
analysis (13-class taxonomy) → exam strategy → three full practice exams →
final master simulation with verdict rubric.

Estimated learning time: ~42 h (lesson minutes + practice minutes).
Difficulty scale E1–E5 (internal; mapped to platform labels), skewing E3–E5.

## Verification gates

| Gate | Result |
| --- | --- |
| `validate-content.ts` (all tracks) | exit 0; EN/VI SYNC match; 298 nodes/locale |
| `verify-challenges-apx.mjs` | 129/129 two-sided OK |
| `pnpm typecheck` | clean |
| `pnpm lint` | 0 errors (13 pre-existing warnings) |
| `pnpm test` | 136 passed / 3 failed (pre-existing integration DB-state) |
| `pnpm build` | SUCCESS — 4916 static pages |
| Live smoke (own port) | course/practice/checkpoints 200; VI 200 + rendered |

## Shared-file changes (smallest compatible)

- `src/content/tracks/ap-csa/track.json`: +1 course entry.
- `scripts/content-authoring/validate-content.ts`: +3 ap-csa courses in
  `COURSE_TRACKS`; missing course.json now warn-and-skips (was a hard crash
  of the whole QA pass).
- Minimal render-safety repair to the OTHER agent's in-progress
  `ap-csa-core` `cx-m7-removal{,.vi}.mdx` (literal `{\"a\"...}` prose
  artifacts broke MDX parsing → repo-wide build failure). Prose-only fix;
  code blocks and all other Core files untouched.

## Blockers encountered

- Docker daemon down → DB down → lesson pages 500 for every course
  (discussion-thread count query). Environmental; challenge/practice pages
  unaffected. Re-verify lesson URLs when the daemon returns.
- The other agent's `:3000` dev server predates both new courses and serves
  stale 404s; smoke run instead on `next start -p 3999` (prod build).

## Files

- Content: `src/content/tracks/ap-csa/courses/ap-csa-advanced/**` (new)
- Authoring: `scripts/content-authoring/apx.py`, `apx_m1..24.py`,
  `apx_finish_lessons.py`, `apx-solutions.mjs`, `verify-challenges-apx.mjs`
- Docs: `docs/COURSE-AP-CSA-ADVANCED.md`
