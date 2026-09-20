# Course Spec — HSG Advanced (Tuyển Học Sinh Giỏi Tin học — Nâng cao)

Track `hsg` · Course `hsg-advanced` · Phase 29 · Status: **COMPLETE (2026-09-20)**

## Identity

- **Audience:** Vietnamese high-school students (Grades 10–12) who finished HSG
  Intermediate (`hsg-intermediate`, prerequisite) and are preparing for difficult
  provincial HSG problems, national-level HSG preparation, and Olympiad-style tasks.
- **Goal:** move from *can derive an algorithm from constraints* to *can prove why it
  works, modify it for unusual constraints, and combine techniques under contest
  pressure*.
- **Language:** Vietnamese is the primary experience; English synchronized (every
  module, lesson, practice set, and challenge exists in both locales).

## Shape (actual, verified)

| Metric | Value |
| --- | --- |
| Modules | 20 |
| Lessons | 83 (54 teaching + 17 module checkpoints + 12 contest checkpoints) |
| Practice sets | 20 |
| Challenges | 92 (63 practice + 29 checkpoint) |
| Estimated time | ~77 h (4620 min of lesson/practice minutes) |
| Harness | 92/92 two-sided clean (solution passes every reference test; every wrong solution fails ≥ 1 test), verified module-by-module in the real container |
| Toolchain | g++ 14.2.0, -std=c++20, sandbox 10 s CPU / 512 MB, offline |

## Module map

| # | Module | Topic | Signature techniques |
| --- | --- | --- | --- |
| 1 | hsga-attack | Advanced attack patterns | meet-in-the-middle, XOR invariants, constructive permutations |
| 2 | hsga-lazy | Lazy propagation segment trees | range-assign / range-max with lazy tags |
| 3 | hsga-fenwick2 | Fenwick variants & offline power | range-update point-query, offline sweep |
| 4 | hsga-lift | Binary lifting & LCA | 2^k ancestor tables, kth-ancestor, path sums |
| 5 | hsga-euler | Euler tour queries | tin/tout flattening, subtree aggregates via BIT |
| 6 | hsga-treedp | Tree DP | take/skip, rerooting, max matching on trees |
| 7 | hsga-hld | Heavy-light decomposition | chain decomposition, path queries with segment trees |
| 8 | hsga-scc | Strongly connected components | Tarjan SCC, condensation DAG, 2-SAT |
| 9 | hsga-flow | Max flow & matching | Dinic, König's theorem, bipartite matching |
| 10 | hsga-digitdp | Digit DP | tight/free states, digit-sum divisibility counting |
| 11 | hsga-intervaldp | Interval DP | matrix-chain style merges, burst balloons, expected values |
| 12 | hsga-suffix | String structures | rolling hash, Z-function, suffix arrays, LCP |
| 13 | hsga-numth2 | Number theory II | extended Euclid, CRT, Möbius, Euler phi, Miller–Rabin |
| 14 | hsga-combi | Combinatorics | factorials/inverses, stars & bars, Catalan, inclusion–exclusion |
| 15 | hsga-geom | Computational geometry | cross products, convex hull (Andrew), shoelace, point-in-hull |
| 16 | hsga-synth | Technique synthesis | multi-technique composites (hash + DP, geometry + sweep + flow-style reasoning) |
| 17 | hsga-debug | Debugging under contest load | RE/WA/TLE triage, minimizing failing cases, stress-testing patterns |
| 18 | hsga-contests | Contest Series I | 2 strategy lessons + 4-checkpoint 120-min mock contest (structures & graphs) |
| 19 | hsga-contests2 | Contest Series II | mock contest on trees & strings |
| 20 | hsga-contests3 | Final HSG Simulation | capstone mock contest mixing all course techniques |

## Verification (2026-09-20)

- Two-sided container harness: **92/92 challenges clean**, run per-module in the real
  sandbox (`scripts/content-authoring/verify-challenges-hsga.mjs`); every solution
  passes its full reference suite and every wrong solution fails at least one test.
- Ledger ↔ content mirror check: **92/92** solution/wrong bodies match
  `scripts/content-authoring/hsg-advanced-solutions.mjs`.
- Curriculum unit suite: 48/48 (schema, prerequisite, locale, Learn→Practice flow).
- Full unit suite: 184/184; typecheck 0 errors; lint 0 errors; production build PASS.
- E2E: 36/36 (incl. critical path with real sandbox run; local Postgres + Docker were
  started for the run — failures observed before that were infra-only).
- QA fix during build: 8 checkpoint lessons (hsga-cp-m10 … hsga-cp-m17) existed on disk
  but were missing from their `module.json` lesson refs (loader reads refs only) — refs
  added, curriculum suite re-verified.

## Artifacts

- Research: `docs/CURRICULUM-RESEARCH-HSG-ADVANCED.md`
- Authoring scripts: `scripts/content-authoring/hsga.py` + `hsga_m1.py … hsga_m20.py`
- Solution ledger: `scripts/content-authoring/hsg-advanced-solutions.mjs`
- Local two-sided verifier: `scripts/content-authoring/_hsg_local_verify.py`
- Container harness: `scripts/content-authoring/verify-challenges-hsga.mjs`
