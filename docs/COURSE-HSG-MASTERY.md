# Course Spec — HSG Mastery

Track `hsg` · Course `hsg-mastery` · Phase 31 · Status: **COMPLETE (2026-09-22)**

## Identity

- **Audience:** Vietnamese high-school students who finished HSG Advanced (and
  can use HSG Intensive as parallel practice) and are preparing for difficult
  provincial HSG, national-level, and Olympiad-style tasks.
- **Goal:** the transition from *"I know advanced algorithms"* to *"I can
  independently discover, select, combine, prove, optimize, implement, debug,
  and defend a solution to an unfamiliar problem."*
- **Positioning:** the capstone of the HSG ladder
  (`hsg-beginner` → `hsg-intermediate` → `hsg-advanced` → `hsg-mastery`);
  NOT an algorithm encyclopedia and NOT Advanced-2.0.

## What makes it different: process-first

There are **no algorithm-teaching lessons**. Every skill area is taught inside
original problems whose solutions embed the technique. The fourteen modules
each drill one stage of the mastery loop:

| # | Module (`hsgm-*`) | Stage drilled |
| --- | --- | --- |
| 1 | `hsgm-process` | the solve pipeline: model → budget → idea → verify → implement |
| 2 | `hsgm-budget` | constraint → complexity → candidate algorithm; op-count arithmetic |
| 3 | `hsgm-decompose` | prose → formal model; reformulation; state design |
| 4 | `hsgm-observe` | attempt-first observation discovery (parity, invariants, monotonicity) |
| 5 | `hsgm-greedy` | greedy proof (exchange arguments) and counterexample construction |
| 6 | `hsgm-dpsynth` | DP state/transition reasoning, DP + structure synthesis |
| 7 | `hsgm-graphsyn` | graph/tree technique composition |
| 8 | `hsgm-offline` | reading queries before answering; sweeps; offline processing |
| 9 | `hsgm-optlab` | optimization: bottleneck naming, acceleration, proving the new bound |
| 10 | `hsgm-partial` | partial-scoring ladder: subtask harvesting, score strategy |
| 11 | `hsgm-clinic` | wrong-solution diagnosis: plausible-but-wrong code, bug + counterexample |
| 12 | `hsgm-adversary` | adversarial thinking: break your own solution |
| 13 | `hsgm-stress` | 3-program stress harness (brute + candidate + generator) + contest decisions |
| 14 | `hsgm-final` | mixed expert sets with **unidentified topics** + final simulations |

## Measured numbers

| Metric | Value |
| --- | --- |
| Modules | 14 |
| Lessons | 43 (28 teaching + 15 checkpoints) |
| Practice sets | 14 (one per module) |
| Challenges | 57 (42 practice + 15 checkpoint), unique IDs |
| Locales | EN + VI, synchronized (43/43 lessons, 14/14 practice sets) |
| Estimated time | ~17.1 h (1025 min: 735 lesson + 290 practice) |
| Prerequisites | `hsg-advanced` (ladder enforced in track order) |

## Verification (all executed 2026-09-22)

- **Two-sided container harness 57/57** (`scripts/content-authoring/verify-challenges-hsgm.mjs`):
  every reference solution passes all its tests (101/101), every intentionally
  wrong solution fails ≥ 1 test (71 W-failures / 30 W-passes). The harness uses
  the same `buildCppTestFile()` as the production sandbox — no QA drift.
- **Ledger mirror 57/57** (`hsg-mastery-solutions.mjs`).
- **Loaders**: track loads 4 courses (intensive authoring shell excluded by
  design); 14 modules load; global ID uniqueness green.
- **QA gates**: typecheck 0 · lint 0 errors (12 pre-existing warnings, house
  pattern) · unit+integration 172 passed / 12 skipped / 0 failed · build PASS ·
  E2E 36/36 (sandbox verdicts, mobile, keyboard a11y).
- **Sandbox**: g++ 14.2.0 C++20, 0.5 CPU / 512 MB / 20 s — same environment the
  earlier HSG courses were verified against; constraints written to it.

## Authoring discipline notes

- Wrong solutions are **behavioral**, not cosmetic: TLE-based Ws were rejected
  where the local box proved too fast (M-series measured ~5·10⁹ ops/s); every W
  carries a real logic bug with a discriminating test (e.g. parity-of-count vs
  parity-of-sum, half-open range stumble, reverse-edge graph reading).
- Hand-written test wants were only trusted after execution; the harness caught
  several wrong ground-truths (interval-removal counts, span tests that cannot
  force the whole string, index slips) — each fixed against computed truth.
- Module summaries are kept ≤ 200 chars (loader schema limit).

## Intentionally excluded

- New algorithm lectures (the ladder already covers them; Intensive adds drills).
- Implementation of Mo's algorithm/suffix automaton etc. as topics — synthesis
  problems reference techniques conceptually; the ladder's Advanced course owns
  the algorithmic treatments.
- Registration of `hsg-intensive` in `track.json` — it is another agent's
  unregistered work-in-progress; only MDX parse-blocking typos in it were
  minimally fixed (backticked `i<j`, `{0..10}`), disclosed in the phase summary.

## Known limitations

- 57 challenges is deliberately compact (quality-first mandate); scale can grow
  by adding module scripts following the same two-sided discipline.
- Contest simulations are single-checkpoint problems, not a multi-problem
  timed contest format (the platform has no contest-session schema yet).
- W-solution counts are per-challenge single Ws, not libraries of many Ws.
