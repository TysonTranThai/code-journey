# Phase 31 — HSG Mastery — SUMMARY

**Status: COMPLETE (2026-09-22)** · Course `hsg-mastery` on existing track `hsg`

## What was built

The highest-level problem-solving course in the HSG THPT path — deliberately
**process-first, not algorithm-first**: no algorithm lectures; every skill area
(decomposition, observation discovery, greedy proof, DP/graph synthesis,
offline processing, optimization, partial scoring, debugging, adversarial
thinking, stress testing, contest decisions, mixed expert work) is taught
through original problems whose solutions embed the technique.

**Measured course shape** (from generated files, not plans):

- **14 modules** (`hsgm-*`), course title "Competitive Programming — High
  School Mastery"
- **43 lessons**: 28 teaching + **15 checkpoints** (14 module checkpoints +
  1 final-simulation checkpoint)
- **14 practice sets** (all bilingual EN+VI)
- **57 challenges**: 42 practice + 15 checkpoint — unique IDs, zero orphans
- **~17.1 h estimated** (735 lesson min + 290 practice-set min)
- EN/VI synchronized: 43/43 lessons have a `.vi.mdx` twin (86 MDX files total),
  all practice/checkpoint JSON mirrored (14/14 practice sets + VI challenge
  defs)

## Research

`docs/CURRICULUM-RESEARCH-HSG-MASTERY.md` — built on a live VNOI wiki fetch
(exam-skill corpus: execution skill over algorithm novelty, ~3×10⁸ op budget
heuristic, brute-force-as-scoring-strategy, 3-program stress harness, partial
scoring tactics) plus the repo's verified Beginner/Intermediate/Advanced
research corpus. No copyrighted problem statements reproduced; all exercises
original.

## Verification (all executed this session)

- **Two-sided container harness 57/57 clean** (`verify-challenges-hsgm.mjs`):
  101/101 reference tests pass; every one of the 57 wrong solutions fails
  ≥ 1 test (71 W-test failures / 30 W-test passes) — no W passes its suite
- **Ledger mirror 57/57** (`hsg-mastery-solutions.mjs`): 57 R + 57 W lines,
  unique IDs — matches disk exactly
- **Loaders accept the course**: track loads 4 courses (mastery included;
  unregistered `hsg-intensive` authoring shell correctly excluded), 14 modules
- **QA gates**: typecheck 0 errors · lint 0 errors (12 pre-existing warnings,
  same house pattern as sibling harnesses) · unit+integration **172 passed /
  12 skipped / 0 failed** (skips are env-conditional suites) · **build PASS** ·
  **E2E 36/36** (incl. sandbox verdict flows, mobile, keyboard a11y)

## Cross-course incident found and fixed (disclosed, minimal)

Another agent's **untracked** `hsg-intensive` content had three MDX parse
blockers that broke MDX compilation for the *whole curriculum* (unit suite
+ build). Minimal fixes, preserving meaning:

- `hsgx-m1-reading{,.vi}.mdx`: bare `i<j` in a table → backticked `` `i<j` ``
- `hsgx-m6-generators{,.vi}.mdx`: bare `{0..10}` → backticked `` `{0..10}` ``

All four files verified to compile; the agent's files were otherwise untouched.
(An earlier attempt used HTML entities, which decoded back to literal `<` —
the backtick code-span form is the durable fix.)

## Environment

Postgres 16 started on 5433 and Docker Desktop started for the sandbox E2E
specs — both were down after the app restart; both were re-started with the
repo's established local procedure.

## Files changed (this phase)

- `src/content/tracks/hsg/courses/hsg-mastery/**` — the course (14 modules)
- `src/content/tracks/hsg/track.json` — registered `hsg-mastery` (additive;
  `hsg-intensive` deliberately left unregistered — another agent's in-progress work)
- `src/lib/curriculum/mdx-map.ts` — regenerated (3080 lesson imports)
- `scripts/content-authoring/hsgm.py`, `hsgm_m1..m14.py` — authoring toolkit + modules
- `scripts/content-authoring/verify-challenges-hsgm.mjs`, `hsg-mastery-solutions.mjs` — two-sided QA harness + ledger
- `docs/CURRICULUM-RESEARCH-HSG-MASTERY.md`, `docs/COURSE-HSG-MASTERY.md` — research + course spec
- 4 hsgx MDX files (disclosed cross-course fix) · `.planning/ROADMAP.md` (row 31)

## Multi-agent safety

Untracked `hsg-intensive` course untouched except the 4 disclosed MDX fixes.
Other agents' modified shared files (`LandingLoader.tsx`, `dictionaries.ts`,
`verify-challenges-csharp-advanced.mjs`) untouched. No commits made.
