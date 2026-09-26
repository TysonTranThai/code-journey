# AP CSA Core & Exam Preparation — Course Spec (ap-csa-core)

> Phase: 33 (track `ap-csa`, course 2) · Status: COMPLETE (2026-09-26) ·
> Prerequisite: `ap-csa-beginner` (AP CSA Foundations) · Language: EN + VI
> Research basis: `docs/CURRICULUM-RESEARCH-AP-CSA.md` (incl. the Core
> addendum, 2026-09-25) — no College Board questions reproduced.

## Purpose

The bridge between "I know Java" (Foundations) and "I can perform under the
real AP CSA exam" (the follow-on mastery course). Core teaches AP-style
problem solving: code tracing under pressure, specification-driven
implementation, the four FRQ question types, MCQ strategy and the trap
taxonomy, debugging clinics, timed mixed practice, and a full simulation.

Design ratio: ~30% instruction / ~70% active problem solving. Modules open
with 2–3 short lessons and spend the rest of their weight in practice sets
and checkpoints.

## Facts (measured on disk, 2026-09-26)

| Item | Count |
| --- | --- |
| Modules | 20 |
| Lessons | 42 (20 teaching + 22 checkpoints) |
| Practice sets | 26 |
| Challenges (graded, executable) | 121 (101 practice + 20 checkpoint) |
| Two-sided verification | 121/121 (R passes all tests, W fails ≥ 1) |
| Estimated learning time | ~31 h (lesson + practice minutes) |

Note: every MCQ-style item is delivered as a Java-executable challenge
(trace-and-reproduce, prediction-graded tests, or fix-the-near-miss) — the
platform schema has no native MCQ type, so "MCQ practice" here means
executable equivalents with the same reasoning load.

## Module map (4 arcs)

1. **Problem-solving arc (1–3)** — `cx-bootcamp` (contract reading, widening,
   bug hunts), `cx-tracing` (state tables, frames, aliases), `cx-flow`
   (accumulator/counter/flag/sentinel machines, five boundary traps).
2. **Topic mastery arc (4–10)** — `cx-specs` (helpers, preconditions),
   `cx-strings` (Quick Reference API edges, two pointers), `cx-arrays`
   (traversal modes, index algebra, multi-pass), `cx-arraylist` (removal
   discipline, boxing, merge), `cx-2d` (orientation, neighbors, columns),
   `cx-objects` (state transitions, aliasing, constructor traps),
   `cx-inheritance` (dispatch tables, ctor chains, polymorphic collections).
3. **Integration arc (11–13)** — `cx-recursion` (edges, frame tracing,
   branching trees), `cx-mixed` (unlabeled diagnosis, four elimination
   probes), `cx-mcq` (prediction-first protocol, trap taxonomy, error
   clinic).
4. **Exam-performance arc (14–20)** — `cx-frq-fund` (exam shape, 8-step
   workflow, answer conventions), `cx-frq-class` (Q2 spec tables),
   `cx-frq-list` (Q3 analysis methods), `cx-frq-2d` (Q4 grids),
   `cx-frq-debug` (first-error localization, salvage), `cx-timed` (four
   timed mixed sets, pacing rules, machine inventory), `cx-sim` (four-part
   simulation, rubric self-scoring, readiness checklist).

## Execution environment (verified, not assumed)

Sandbox: `src/workers/java-runtime.ts` — `javac --release 21`, JVM
`-XX:+UseSerialGC -Xss4m`, per-test compilation of `Solution.java` with
generated `Test_*` classes (`CjTestBase` helpers). Local QA uses the same
`buildJavaTestFile()` — byte-identical to the sandbox.

## Authoring toolkit (this course, isolated)

- `scripts/content-authoring/apcc.py` — course-2 clone of `apc.py`
- `scripts/content-authoring/apcc_m1..m20.py` — module emitters
- `scripts/content-authoring/apcc_finish.py`, `apcc_register.py` — manifests
- `scripts/content-authoring/apcc-solutions.mjs` — R/W ledger (119 R + 121 W
  after the two practice-mirror renames; deduped via `apcc_dedupe.py`)
- `scripts/content-authoring/verify-challenges-apc-core.mjs` — two-sided
  harness (`node --import tsx --import ./scripts/worker-imports.mjs
  scripts/content-authoring/verify-challenges-apc-core.mjs [id-filter]`)

## Verification (2026-09-26, all executed)

- Harness 121/121 two-sided OK (`verify-challenges-apc-core.mjs`)
- `pnpm typecheck` 0 errors · `pnpm lint` 0 errors (13 pre-existing warnings)
- `pnpm test` 172 passed / 0 failed / 12 skipped (skips are conditional)
- `pnpm build` SUCCESS · `pnpm content:map` 3446 lesson imports
- `scripts/content-authoring/_audit_all.mjs`: 2864 registered ids, 0 problems
- EN/VI: full sync (every lesson/challenge/practice has a `.vi` twin)

## Known platform-lesson quirks caught during authoring

- Global id uniqueness spans practice sets AND checkpoint lessons: two
  checkpoint-challenge ids were mirrored into practice sets and had to be
  renamed (`cx-m14-word-metrics-practice`, `cx-m20-fleet-practice`).
- MDX prose braces must be escaped (`\{`) or wrapped in code spans —
  bare `{...}` in prose is parsed as a JSX expression and breaks the build.
