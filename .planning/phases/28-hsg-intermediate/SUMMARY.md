# Phase 28 — Course: HSG Intermediate — SUMMARY

Date: 2026-09-19
Status: **COMPLETE**

## Course

Track `hsg`, course `hsg-intermediate` ("Tuyển Học Sinh Giỏi Tin học — Trung cấp") — **18
modules, 58 lessons** (36 teaching + 18 checkpoint lessons + 4 contest-checkpoint
lessons), 18 practice sets, **110 challenges** (89 practice + 18 module checkpoints +
4 mock-contest checkpoints), ~34.5 h estimated (1178 min lessons + 890 min practice).
Full EN + VI parity (58/58 lesson MDX × 2 locales; VI overlays on every module,
practice set, challenge, checkpoint).

## Research

`docs/CURRICULUM-RESEARCH-HSG-INTERMEDIATE.md` — Vietnamese provincial HSG Tin học
progression research (VNOI, Codeforces educational rounds, CSES problem-set ladder as
non-copyrighted reference points; no contest problems copied). Key decisions vs the
student-provided proposal list:

- Included at Intermediate (validated against Beginner's deferrals): Fenwick/segment
  tree (point-update + range-max/subarray variants), Dijkstra + 0-1 BFS, Floyd-Warshall,
  MST (Kruskal with DSU), DAG/topo + longest-path DP, LIS in O(n log n), knapsack
  variants (0/1, unbounded, counting), bitmask DP (assignment, Hamiltonian paths,
  bin packing), extended number theory (sieve, modular exponentiation, phi, counting),
  string hashing + KMP prefix-function, two pointers/monotonic window mastery,
  greedy with exchange arguments + priority queues.
- Deferred to HSG Advanced: lazy propagation, binary lifting, LCA, heavy-light
  decomposition, flows, suffix structures (Z/suffix array/automaton), digit DP,
  advanced tree DP, matching, computational geometry.

## Modules (18)

hsgi-vao-mon2 (complexity + constraint-driven selection), hsgi-bsearch2 (binary search
mastery + on-answer), hsgi-greedy2 (exchange argument, priority queues), hsgi-fenwick
(BIT: point-update/range-sum, kth-order), hsgi-segtree (segment tree: sum + max-subarray),
hsgi-compress (coordinate compression + sweep events), hsgi-dsu (DSU + Kruskal MST),
hsgi-dijkstra (Dijkstra, 0-1 BFS, Floyd-Warshall), hsgi-dag (topo sort + DAG DP),
hsgi-trees (tree DFS: diameter, pre/post-order, subtree DP), hsgi-seqdp (LIS O(n log n),
Kadane, LCS rolling), hsgi-knapsack (0/1, unbounded, counting variants), hsgi-bitmask
(assignment, Hamiltonian paths, bin packing), hsgi-numtheory (sieve, modpow, phi,
counting), hsgi-strings (double hashing + KMP), hsgi-synthesis (two pointers, state BFS,
EDF scheduling, weighted intervals — combining techniques), hsgi-debugging (5 fix-the-bug
challenges: binary-search boundary, negative mod, missing visited, prefix off-by-one,
wrong DP transition), hsgi-contests (4 mock contests: brute+greedy, DSU/town, rain
water + valid parentheses, balanced-window final).

## Method

Same pipeline as HSG Beginner (phase 27-hsg-beginner): authoring library
`scripts/content-authoring/hsgi.py` (clone of hsg.py shapes), per-module generators
`hsgi_m1..m18.py`, two-sided local verifier `_hsg_local_verify.py`, real container
harness `verify-challenges-hsgi.mjs` (g++ 14.2.0, C++20, `-O0`-style sandbox limits —
same config as Beginner; 10 s CPU / 512 MB), ledger
`scripts/content-authoring/hsgi-intermediate-solutions.mjs` (110 R / 110 W after
keep-last dedupe; JS module semantics = last-wins matches harness import).

Verification loop per module: write generator → local two-sided verify (R passes all
tests; every W fails ≥ 1 test, behavioral near-misses preferred over accidental
compile errors) → emit JSON/MDX → run real harness on the emitted set → fix → re-emit.
Ground-truth expectations computed independently in Python before locking tests; all
hand-counts re-checked (several were wrong and fixed — e.g. Hamiltonian count,
knapsack 3000-item totals, Josephus Fenwick simulation).

## Harness results (real container, full sweep)

- Practice: 89/89 clean — R 460/460 test cases pass; every wrong solution fails ≥ 1
  test (behavioral FAIL or intentional TIMEOUT for O(n²) near-misses).
- Checkpoints: 21/21 clean (18 module + 4 contest; contest = 4 problems × 5 tests).
- Perf probe: 12 largest inputs (2.5–4.8 MB) — reference solutions ≤ 1.5 s each at the
  sandbox's optimization level, well inside the 10 s limit; memory within 512 MB
  (rolling-array and 1D-dp used where 2D would exceed).

## QA gates

- Curriculum/content validators: PASS (loaders smoke: 18 modules, 58 lessons, 18
  practice sets, 110 challenges; schema validator green for hsg-intermediate).
- EN/VI sync: PASS (every module/lesson/practice/challenge has both locales).
- Typecheck: PASS (0 errors). Lint: PASS (0 errors; 6 pre-existing warnings, not mine).
- Unit tests: 184/184 PASS. Build: PASS (after fixing 6 MDX raw `<`/`{` JSX-escape
  defects in lis/hamilton/zero-one/exchange/heaps lessons, EN + VI).
- E2E: 36/36 PASS (Playwright, port 3456 — includes HSG Intermediate course +
  module/lesson navigation in both locales and a real sandbox run/submit flow).
- C++ Beginner/Intermediate/Advanced, C, C#, Java, Python, Web tracks: untouched
  (verified via git status scope; HSG Beginner loaders re-smoked clean).

## Known limitations

- Mock-contest *timed* lifecycle (countdown, lock) is represented as checkpoint
  problems with contest framing; no dedicated timed-contest E2E spec exists in the
  platform yet — same limitation as Beginner.
- Sandbox is `-O0`-equivalent: time limits sized accordingly (verified by probe), but
  an `-O2` deployment could allow tighter limits later.
- 4 contest checkpoints reuse the checkpoint schema (no separate contest schema in the
  platform); scoring/subtask metadata is embedded in statements, not structured fields.

## Files

- `scripts/content-authoring/hsgi.py`, `hsgi_m1..m18.py`, `_hsg_local_verify.py`,
  `verify-challenges-hsgi.mjs`, `hsgi-intermediate-solutions.mjs`, `_dedupe_hsgi_ledger.py`,
  `_finish_hsgi_manifests.py`, `_hsgi_smoke.mts`, probe/fix helpers (`_probe_m10.py`,
  `_probe_m11.py`, `_fix_m18.py`)
- `src/content/tracks/hsg/courses/hsg-intermediate/**` (course.json, 18 modules:
  module.json, lessons EN/VI MDX, practice JSON, checkpoint JSON ×2 locales)
- `src/content/tracks/hsg/track.json` (registered hsg-intermediate — additive)
- `docs/CURRICULUM-RESEARCH-HSG-INTERMEDIATE.md`, `docs/COURSE-HSG-INTERMEDIATE.md`
- `.planning/phases/28-hsg-intermediate/SUMMARY.md`, `.planning/ROADMAP.md` (row 28),
  `.planning/STATE.md` (session-continuity block)
