# Course Spec — HSG Intermediate (Tuyển Học Sinh Giỏi Tin học — Trung cấp)

Track `hsg` · Course `hsg-intermediate` · Phase 28 · Status: **COMPLETE (2026-09-19)**

## Identity

- **Audience:** Vietnamese high-school students (Grades 10–12) who finished HSG
  Beginner (`hsg-beginner`, prerequisite) and are preparing for stronger
  provincial-level HSG Tin học competitions.
- **Goal:** move from *can implement a known technique* → *can recognize which
  technique applies* → *can derive an algorithm from constraints and structure* →
  *can solve unfamiliar HSG-style problems under contest pressure*.
- **Language:** Vietnamese is the primary experience; English synchronized
  (every module, lesson, practice set, challenge exists in both locales).

## Shape (actual, verified)

| Metric | Value |
| --- | --- |
| Modules | 18 |
| Lessons | 58 (36 teaching + 18 checkpoint lessons + 4 contest-checkpoint lessons) |
| Practice sets | 18 |
| Challenges | 110 (89 practice + 18 module checkpoints + 4 mock-contest checkpoints) |
| Estimated time | ~34.5 h (1178 min lessons + 890 min practice) |
| Harness | 110/110 two-sided clean; 460/460 reference tests pass; every wrong solution fails ≥ 1 test |
| Toolchain | g++ 14.2.0, -std=c++20, sandbox 10 s CPU / 512 MB, offline |

## Module map

| # | Module | Topic | Signature techniques |
| --- | --- | --- | --- |
| 1 | hsgi-vao-mon2 | Complexity & constraint-driven selection | reading constraints → complexity budget; brute-force rescue |
| 2 | hsgi-bsearch2 | Binary search mastery | monotonic predicates, search-on-answer |
| 3 | hsgi-greedy2 | Greedy recognition | exchange argument, priority queues, counterexamples |
| 4 | hsgi-fenwick | Fenwick tree | point-update/range-sum, kth-order statistics |
| 5 | hsgi-segtree | Segment tree | range sum, max-subarray merge (Kadane node) |
| 6 | hsgi-compress | Coordinate compression & sweep | value ranking, event processing |
| 7 | hsgi-dsu | DSU + MST | union by size + path compression, Kruskal |
| 8 | hsgi-dijkstra | Shortest paths | Dijkstra, 0-1 BFS, Floyd-Warshall |
| 9 | hsgi-dag | DAGs & topological sort | Kahn's algorithm, longest-path DP, path counting |
| 10 | hsgi-trees | Tree algorithms | diameter, pre/post-order, subtree aggregation |
| 11 | hsgi-seqdp | Sequence DP | LIS O(n log n), Kadane, LCS with rolling rows |
| 12 | hsgi-knapsack | Knapsack variants | 0/1, unbounded, counting subsets |
| 13 | hsgi-bitmask | Bitmask DP | assignment, Hamiltonian paths, bin packing |
| 14 | hsgi-numtheory | Number theory | sieve, modular exponentiation, φ, prime counting |
| 15 | hsgi-strings | String algorithms | double hashing, KMP prefix function |
| 16 | hsgi-synthesis | Combining techniques | two pointers, state BFS, EDF scheduling, weighted intervals |
| 17 | hsgi-debugging | Debugging practice | 5 fix-the-bug challenges (binary-search boundary, negative mod, missing visited, prefix off-by-one, wrong DP transition) |
| 18 | hsgi-contests | Mock contests | 4 contest checkpoints × 5 tests (trap-problem, flood/town, rain-water + parentheses, balanced-window final) |

## Pedagogy

Problem-solving-first: every module follows concept → why it works → complexity →
recognition patterns → worked example → guided practice → debugging → mixed/contest
problems. Each practice challenge ships a reference solution (R) **and** an
intentionally wrong solution (W) that fails for a *behavioral* reason (wrong
invariant, off-by-one, missed edge case, stale state) or an intentional O(n²)
timeout — teaching *why* solutions fail, not just that they do. Expectations are
computed independently (Python ground-truth) before tests are locked; large inputs
are perf-probed in the real sandbox (largest: 2.5–4.8 MB inputs run ≤ 1.5 s at the
sandbox's optimization level).

## Deferred to HSG Advanced (intentional boundary)

Lazy propagation, binary lifting / LCA, heavy-light decomposition, max-flow /
min-cost flow, matching, suffix arrays/automaton, Z-function at depth, digit DP,
advanced tree DP, advanced bitmask/ state-compression DP, computational geometry,
Olympiad-level synthesis.

## Known limitations

- Mock contests are checkpoint-schema problems with contest framing (time/memory
  limits + subtask-style difficulty ramp embedded in statements); the platform has
  no dedicated timed-contest schema yet — same limitation as HSG Beginner.
- Sandbox optimization level is -O0-equivalent; limits are sized and verified for
  that. An -O2 deployment could allow tighter limits later.

## Files

- Content: `src/content/tracks/hsg/courses/hsg-intermediate/`
- Research: `docs/CURRICULUM-RESEARCH-HSG-INTERMEDIATE.md`
- Authoring: `scripts/content-authoring/hsgi.py`, `hsgi_m1..m18.py`,
  `verify-challenges-hsgi.mjs`, `hsgi-intermediate-solutions.mjs`
- Phase record: `.planning/phases/28-hsg-intermediate/SUMMARY.md`
