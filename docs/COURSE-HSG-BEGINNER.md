# Course Spec — Tuyển Học Sinh Giỏi Tin học — Beginner (`hsg-beginner`, "Tuyển Học Sinh Giỏi Tin học — Cơ bản")

Date: 2026-09-18. Status: **complete** (Phase 27). Research:
`docs/CURRICULUM-RESEARCH-HSG-BEGINNER.md`.

## Positioning

Track `hsg` — new track, distinct from the normal `cpp` curriculum. Path:
**HSG Beginner → HSG Intermediate → HSG Advanced** (future). This is a
**problem-solving / competitive-programming** course for Vietnamese
high-school students (grades 10–12) preparing for Học sinh giỏi Tin học
selection (school → district → provincial), NOT a general C++ course.
C++ is the vehicle; the subject is *how to solve contest problems*.

- **Verified toolchain (probed in the sandbox, 2026-09-18):** g++ 14.2.0
  (Alpine), `-std=c++20`, `-Wall -Wextra -Wpedantic`, no `-O2` at test
  compile, `bits/stdc++.h` available (~1.3 s per TU), 20 s per-submission
  job budget (30 s hard ceiling), 512 MB, no network. Every problem's
  constraint ceiling is sized so the intended complexity runs comfortably
  at -O0 — constraints are honest teaching data, never fabricated.
- **Practice-first:** Learn (2 teaching lessons/module) → Deep Example →
  Practice (5-challenge graded set per module) → Checkpoint (module exam
  problem). Vietnamese is the primary experience; English parity is
  structural (same ids, same counts, validator-enforced `SYNC`).
- **Problem statements mirror the real format:** Tên bài / Mô tả / Dữ liệu
  vào / Dữ liệu ra / Giới hạn / Ví dụ (+ Subtask where taught). All
  problems are original, inspired by classical formats, never copied.
- **Two-sided verification:** every challenge ships a reference solution
  (R: passes all tests) and an intentionally-wrong near-miss (W: fails
  ≥1 test for the stated reason) — verified in the real container.

## Module plan (20 modules, 65 lessons, 127 challenges)

| # | dir | Title | Core techniques | Challenges (P + CP) |
|---|-----|-------|-----------------|---------------------|
| 1 | `hsg-vao-mon` | Contest Reading & the C++ Bridge | reading Dữ liệu vào/ra + Giới hạn, verdict taxonomy, overflow (a+b), negative modulo | 5+1 |
| 2 | `hsg-loops` | Loops as Simulation | digit processing, counting, accumulation, simulation | 5+1 |
| 3 | `hsg-arrays` | Arrays | traversal, min/max, rotation, sliding windows on arrays | 5+1 |
| 4 | `hsg-marking` | Marking & Frequency Arrays | mảng đánh dấu, đếm phân phối, value-range → structure choice | 6+1 |
| 5 | `hsg-greedy` | Greedy Basics | exchange arguments, sorting + greedy, counterexamples, proof sketches | 6+1 |
| 6 | `hsg-sorting` | Sorting | `std::sort`, comparators, dense/ordinal ranking, interval merging | 6+1 |
| 7 | `hsg-search` | Searching & Binary Search | monotonic predicates, lower/upper_bound, binary search on answer | 6+1 |
| 8 | `hsg-prefix` | Prefix Sums | 1D/2D prefix sums, O(1) range queries, off-by-one discipline | 6+1 |
| 9 | `hsg-diff` | Difference Arrays | range updates in O(1), reconstruction, coverage/booking | 6+1 |
| 10 | `hsg-strings` | Strings | palindrome, frequency, distinct substrings, character classes | 6+1 |
| 11 | `hsg-number` | Basic Number Theory | gcd/lcm, primality, factorization, digit sums, modular traps | 6+1 |
| 12 | `hsg-stl` | STL for Contests | map/set/priority_queue/struct use-the-standard-library philosophy | 6+1 |
| 13 | `hsg-recursion` | Recursion | base/recursive cases, call-stack tracing, Collatz, divide & conquer intro | 6+1 |
| 14 | `hsg-backtrack` | Backtracking | subsets/permutations/grid paths with pruning, honest exponential costs | 6+1 |
| 15 | `hsg-dp` | Dynamic Programming Basics | state/transition/base/order discipline: Fibonacci, coin sums, knapsack, LIS, grid DP | 6+1 |
| 16 | `hsg-graph` | Graph Theory Fundamentals | adjacency lists, BFS/DFS, flood fill, components, grid-as-graph | 6+1 |
| 17 | `hsg-twopointers` | Two Pointers & Sliding Window | sorted pair search, window invariants, merge, fixed-size windows | 6+1 |
| 18 | `hsg-technique` | Contest Technique | complexity budgeting, subtask strategy, partial scoring, time management | 6+1 |
| 19 | `hsg-debug` | Debugging Competitive Programs | off-by-one, overflow, stale visited, unbounded search — broken code embedded in statements | 6+1 |
| 20 | `hsg-contests` | Beginner Contest Series | 3 graded mock contests (6 problems), mixed technique, contest pacing | 5+6 |

**Totals:** 65 lessons (60 teaching + 5 contest-strategy lessons +
25 checkpoint lessons with attached exam problems... counted as: 3
lessons/module × 19 + 8 in the contest module), **127 challenges**
(102 practice across 20 sets + 25 checkpoint problems including the 6
mock-contest problems), ~33.4 h estimated (932 lesson minutes +
1070 practice minutes). Full EN + VI parity — 130 MDX files
(65 × 2 locales), VI sidecar JSON for every module/practice/challenge.

## IDs & naming

- Track `hsg`, course `hsg-beginner`; id prefix `hsg-` on every id kind
  (`hsg-pN-*` practice, `hsg-cp-mN-*` module checkpoints, `hsg-cp-m20[a-c]`
  contest problems, `hsg-mN-*` lessons, `hsg-<dir>` module references).

## Verification (two-sided, real compiles in the Docker sandbox)

Final clean-ledger sweep (20 practice sets + 10 checkpoint filters,
parallel shards, all exit 0):

```
challenges: 127
R tests: 560 pass / 0 fail
W tests: 285 fail / 275 pass  → every W fails ≥1 test, none hang
```

Every R passes all its tests; every W fails for a *behavioral*,
discriminating reason (e.g. greedy trap input, stale-visited DFS query,
ascending knapsack loop reusing an item, directed-graph BFS misread) —
never compile-only, never timeout-only, never a no-op near-miss.

## Gates

- Curriculum validation (`validate-content.ts`, registered
  `{ track: "hsg", course: "hsg-beginner" }`): PASS —
  `SYNC: EN/VI structures match`; 253 nodes load clean per locale.
- `pnpm content:map`: regenerated; 130 HSG MDX entries in mdx-map.ts.
- Typecheck (`tsc --noEmit`): PASS (exit 0).
- Lint: 0 errors (pre-existing warnings only, none in HSG files).
- Unit tests: **184/184 PASS** (28 files).
- Build (`pnpm build`): PASS.
- E2E: blocked at time of writing by the Next 16 dev-server lock —
  another agent's live `next dev` on :3000 makes any second `next dev`
  in this project exit 1 (boot fails before Playwright's 60 s window).
  Content gates above are independent of E2E; re-run when the tree is
  quiet (`pnpm test:e2e`).

## Parallel-work preservation

- Only my own files were created/edited under `src/content/tracks/hsg/`,
  `scripts/content-authoring/hsg*`, `docs/`, `.planning/`.
- Shared-infrastructure change: exactly **one line** — the
  `hsg-beginner` entry in `validate-content.ts`'s `COURSE_TRACKS` list.
  The mdx-map generator auto-discovers tracks (no registry).
- No destructive git commands; no other agent's changes staged or
  committed by me. Course-agent commits began landing mid-run (25d9de3
  and neighbors); my orphaned pre-rename checkpoint JSON was removed by
  that sweep, and the ledger it referenced is deduped keep-last.

## Known limitations

- The sandbox is offline and single-job: no multi-file builds, no
  interactive stdin (problems are batch-format, as in real judges), no
  sanitizer runs in graded tests (UB topics are taught via prose +
  honest near-misses instead).
- Per-test compilation cost (~1.3 s × tests per challenge) bounds test
  counts (≤4 tests/challenge) — adversarial-test breadth is covered by
  hand-chosen discriminators, not volume.
- Beginner boundary honored: no segment/Fenwick trees, Dijkstra, DSU,
  string algorithms beyond brute-force distinct counting, advanced DP —
  reserved for HSG Intermediate/Advanced.
