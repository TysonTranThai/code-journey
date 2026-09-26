# Phase 33 — AP CSA Core & Exam Preparation — SUMMARY

**Status: COMPLETE (2026-09-26)** · Track `ap-csa` · Course `ap-csa-core`
(course 2, after `ap-csa-beginner`)

## What was built

`ap-csa-core`: the AP-exam-performance bridge between Foundations and the
follow-on mastery course. 20 modules / 42 lessons (20 teaching + 22
checkpoints) / 26 practice sets / 121 Java challenges (EN + VI), ~31 h
estimated. ~30% instruction / ~70% problems. Four arcs: problem-solving →
topic mastery → integration → exam performance (FRQ per type, debugging
clinic, timed sets, full simulation).

Distinct from Foundations by design: no Java-syntax teaching; every module
trains exam behaviors (tracing, spec translation, trap recognition, timing,
partial credit). MCQ-style practice is delivered as executable trace/
predict/repair challenges (platform has no native MCQ schema — documented).

## Verification (measured 2026-09-26)

- **Two-sided harness 121/121** (`verify-challenges-apc-core.mjs`, same
  `buildJavaTestFile()` as the sandbox, `javac --release 21`); ledger mirror
  119 R + 121 W (the two extra W pairs are the renamed practice mirrors of
  `cx-cp-m14-word-metrics` → `cx-m14-word-metrics-practice` and
  `cx-m20-sim-q3` → `cx-m20-fleet-practice`, shared by design).
- typecheck 0 · lint 0 errors (13 pre-existing warnings) ·
  **test 172/172 executed, 0 failures** (12 conditional skips) · build PASS ·
  content map regenerated (3446 imports) · `_audit_all.mjs`: 2864 ids,
  0 problems. EN/VI fully synchronized.

## Defects caught by gates (fixed during build)

- Duplicate global ids from checkpoint-vs-practice mirroring (2 cases, renamed).
- MDX prose braces breaking curriculum-wide MDX compile (8 files escaped; one
  pair of `cx-m7-removal` artifacts repaired — see multi-agent note).
- Numerous authoring arithmetic/trace errors caught by the two-sided harness
  before ship (each documented in-loop; tests are ground truth).

## Multi-agent safety

- Another agent built `ap-csa-advanced` (course 3) in parallel and edited
  shared files (`track.json` row, `validate-content.ts` warn-and-skip,
  ROADMAP/STATE rows). All additive; preserved.
- Their agent repaired two literal-artifact lines in this course's
  `cx-m7-removal{,.vi}.mdx` (build-breaking); verified and kept.
- This phase touched only: `ap-csa-core/**` (new), `apcc*.py`,
  `apcc-solutions.mjs`, `verify-challenges-apc-core.mjs`,
  `docs/COURSE-AP-CSA-CORE.md`, `docs/CURRICULUM-RESEARCH-AP-CSA.md`
  (append), `track.json` (additive row), regenerated `mdx-map.ts`.
- No destructive git commands; nothing committed.

## Files

- New: `src/content/tracks/ap-csa/courses/ap-csa-core/**`,
  `scripts/content-authoring/apcc.py`, `apcc_m1..m20.py`,
  `apcc_finish.py`, `apcc_register.py`, `apcc_dedupe.py`,
  `apcc-solutions.mjs`, `verify-challenges-apc-core.mjs`,
  `docs/COURSE-AP-CSA-CORE.md`.
- Modified: `docs/CURRICULUM-RESEARCH-AP-CSA.md` (Core addendum),
  `src/content/tracks/ap-csa/track.json` (+1 course row),
  `src/lib/curriculum/mdx-map.ts` (regenerated).
