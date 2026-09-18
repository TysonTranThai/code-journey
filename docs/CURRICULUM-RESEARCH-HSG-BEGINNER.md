# Tuyển Học Sinh Giỏi Tin học — Beginner: Curriculum Research (verified environment)

Date: 2026-09-18. Environment claims below were probed in the actual Code
Journey sandbox the same day; competition-context claims cite the sources
listed at the end. No behavior is asserted from memory alone.

## 1. Execution environment (probed, not assumed)

| Question | Verified answer | Evidence |
| --- | --- | --- |
| Sandbox image | `codejourney-sandbox:latest` (Alpine) | `docker images`; `docker/Dockerfile.sandbox` |
| C++ compiler | **g++ (Alpine) 14.2.0** | `g++ --version` inside the container |
| C++ standard | **`-std=c++20`** (runtime `CPP_STANDARD_FLAG`) | `src/workers/cpp-runtime.ts:163` |
| Test compile flags | `-Wall -Wextra -Wpedantic` (no `-O2` — tests build at -O0) | `cpp-runtime.ts:164`, job script line 244 |
| `bits/stdc++.h` | **available and compiles** under `-std=c++20` | compile probe, 2026-09-18 |
| bits compile cost | **≈1.3 s** per translation unit | timed probe (10 runs identical) |
| Job wall-clock budget | **20 s** per challenge submission (all tests: compile + run) | `src/app/api/challenges/run/route.ts:81-86` |
| Hard ceiling | 30 s regardless of request (`MAX_TIMEOUT_MS`) | `src/workers/sandbox.ts:48` |
| Memory | **512 MB** for C/C++/C#/Java | `route.ts:88-90` |
| Network/filesystem | none (network off); writes only to /tmp (exec-able) and /job (noexec) | sandbox.ts, cpp-runtime.ts comments |
| Grading model | test file includes `solution.cpp` (learner main renamed via `#define main cj_learner_main`); tests assert via `CHECK/CHECK_EQ/CHECK_LINES/CHECK_NEAR/…` macros; verdicts parsed from PASS markers | `cpp-runtime.ts:15-18, 70-160` |
| Existing per-test-compile precedent | C++ Beginner/Intermediate/Advanced grade 5 tests/challenge at this exact cost | `src/content/tracks/cpp/**` |

**Consequences for course design (honest engineering, not fabrication):**

- Ceilings are *documented teaching data*: lesson content states the real
  limit (20 s per submission job, including compiles; 512 MB) and every
  problem's constraint ceiling is sized so the intended complexity runs
  comfortably at `-O0`. Headline constraints in problem statements use
  realistic-but-modest N (e.g. N ≤ 2·10^5 for O(N log N) work) with the
  note that the grader validates correctness at these ceilings; the
  *reasoning* taught (complexity-from-constraints) is exactly what real
  judges demand at larger official ceilings.
- Subtasks/partial scoring: the platform grades binary per-test. Subtask
  structure is therefore taught and modeled explicitly (constraint tiers
  as separate tests with tier-named hints, e.g. "Subtask 1: n ≤ 100") so
  learners experience tiered constraints and see which tier their solution
  fails — without pretending the judge awards fractional points.
- `freopen`-style file I/O (some provincial environments) is taught as a
  concept with a `solve(istream&, ostream&)` abstraction that makes both
  file and stream I/O one line — never fabricated as "supported by the
  grader".

## 2. Vietnamese HSG context (researched)

- **C++ is the dominant language** of Học sinh giỏi Tin học preparation
  and of the exams themselves ("Ngôn ngữ thường dùng: C++ (chuẩn IOI)" —
  national-stage prep material; community guidance repeats this).
- **Exam shape**: school/district stages commonly 120–150 minutes
  (THCS structure documents); **provincial THPT stage: 180 minutes**,
  typically 3–4 programming problems, partial scoring by test groups.
- **Partial scoring is the norm**: e.g. published district papers split
  each problem's tests into unconstrained and constrained groups
  ("30% số test còn lại … không có ràng buộc gì thêm"), and VNOJ contest
  archives tag `HSG Tỉnh/Thành phố` with per-problem test groups.
- **Terminology in real use** (VNOI/community): mảng đánh dấu, đếm phân
  phối, mảng cộng dồn, quay lui, quy hoạch động, tham lam, duyệt, thành
  phần liên thông, tìm kiếm nhị phân, độ phức tạp.
- **Community learning paths** (chuyentin.pro, VNOI) order the beginner
  arc as: I/O → conditions/loops → arrays → marking/counting → sort →
  binary search → prefix sums → basic number theory → STL → recursion →
  backtracking → greedy → basic DP → BFS/DFS.

Sources: chuyentin.pro (2024–2025 exam archive + bồi dưỡng tài liệu),
VNOJ problem archive category listings (oj.vnoi.info), district/provincial
papers published via studocu/violet (Quảng Trị THCS 2023–24 structure:
120–150 min + 30% unconstrained tests), HSGQG prep notes (scribd:
180–300 min, C++ IOI-standard), Gia Lai THPT 2026 (180 min).

## 3. Student topic list → verdicts (researched, not blind)

| Student topic | Verdict | Where |
| --- | --- | --- |
| Nhập xuất trong C++ | Keep — but fold into M1/M2 with contest framing | M1–M2 |
| if/else, loops, arrays, functions | Keep, compressed (learners arrive from cpp-beginner or the bridge lesson) | M1–M3 |
| Kỹ thuật mảng đánh dấu, đếm phân phối | Keep — signature beginner HSG technique; add the honest value-range rule | M4 |
| Sắp xếp | Keep (STL sort + comparators; manual sorts concept-only) | M6 |
| Tìm kiếm | Keep (linear + binary + lower/upper_bound) | M7 |
| Mảng cộng dồn, mảng hiệu | Keep, as two modules (prefix has 2D; difference has its own failure modes) | M8–M9 |
| String | Keep (contest string drills; no advanced algorithms) | M10 |
| Số học cơ bản | Keep (gcd/lcm, primes, sieve, divisibility; sieve at N ≤ 10^6 teaches real constraints) | M11 |
| STL C++ | Keep (vector/pair/set/map/priority_queue with "what problem does this solve") | M12 |
| Đệ quy quay lui | Keep, as two modules (recursion mechanics ≠ backtracking discipline) | M13–M14 |
| Quy hoạch động cơ bản | Keep (state/transition/base-case discipline on 4 classic families) | M15 |
| Lý thuyết đồ thị | Keep (representation, BFS/DFS, components, grid, unweighted shortest) | M16 |

**Additions after research (missing prerequisites the list lacked):**

- Complexity-first problem reading (Big-O vs time limits vs constraints)
  as its own early module — the single most important HSG beginner skill.
- Contest reading technique: statement/input/output/constraints/subtasks
  (M1) — real provincial format (Dữ liệu vào / Dữ liệu ra / Giới hạn).
- Greedy basics with correctness reasoning and counterexamples (M5) —
  provincial papers test it; taught with exchange argument, not vibes.
- Contest technique module (time management, subtask harvesting) (M18) —
  180-minute exams reward strategy, not just knowledge.
- Debugging competitive programs (M19) — off-by-one/overflow/comparator/
  visited-array failure classes from real contest bugs.

**Deferred to Intermediate/Advanced (documented):** two pointers/sliding
window (proper placement after sorting mastery), binary search on answer,
coordinate compression, modular arithmetic beyond basics, combinatorics,
KMP/Z/trie, DSU/MST/Dijkstra/Floyd, tree DP, bitmask/digit DP, segment/
Fenwick trees, flows. (Research shows provincial beginner problems rarely
require these; they appear in provincial *medium* problems and national
exams.)

## 4. Course identity

- Track id: **`hsg`** ("Tuyển Học Sinh Giỏi Tin học" / "Competitive Programming").
- Course id: **`hsg-beginner`** ("HSG Tin học — Cơ bản" / "Competitive Programming — High School Beginner").
- Language for all challenges: `cpp` (existing runtime; no new runtime).
- Prerequisite bridge: lesson 1.2 covers exactly the C++ slice needed
  (types, I/O, vector, loops) referencing `cpp-beginner` for depth.

## 5. Syllabus (20 modules, 100 problems target)

| # | Module | Core problems (headlines) |
| --- | --- | --- |
| 1 | Vào môn thi đấu (intro + reading statements + bridge) | a+b, max of 3, even check |
| 2 | Vòng lặp (loops as simulation) | digit sum, S(n), pattern |
| 3 | Mảng (arrays) | max/min, reverse, count > x |
| 4 | Mảng đánh dấu & đếm phân phối | freq, duplicates, missing, compare multisets |
| 5 | Tham lam cơ bản | coin change canonical, pairing, deadlines |
| 6 | Sắp xếp | sort + rank, meeting rooms, sort pairs |
| 7 | Tìm kiếm nhị phân | binary search on sorted, lower/upper_bound |
| 8 | Mảng cộng dồn | range sums, equilibrium index, 2D sums |
| 9 | Mảng hiệu | range updates, water fill, coverage |
| 10 | Xử lý xâu (strings) | palindrome, freq chars, word ops, digit strings |
| 11 | Số học cơ bản | gcd/lcm, primes, sieve, divisor sums |
| 12 | STL thực chiến | set/map/priority_queue problems |
| 13 | Đệ quy | factorial, fib (with memo insight), array recursion |
| 14 | Quay lui | permutations, combinations, n-queens small, subsets |
| 15 | Quy hoạch động cơ bản | stairs, coin min, LIS, 0/1 knapsack, grid paths |
| 16 | Lý thuyết đồ thị cơ bản | BFS/DFS, components, maze, shortest steps |
| 17 | Hai con trỏ (two pointers) | pair sum sorted, distinct window |
| 18 | Kỹ thuật thi (contest technique) | complexity selection drills, tiered problems |
| 19 | Sửa lỗi (debugging clinic) | fixed buggy programs per failure class |
| 20 | Kỳ thi thử (mock contests ×4) | mixed 4-problem contests w/ subtasks |

Each teaching module: 2 lessons (concept + worked contest problem) +
1 practice set (4–6 challenges: imitation → guided → independent →
combination/real-world → debugging where apt) + 1 checkpoint. Contests
in M20 are large practice sets. Checkpoint lesson challenge ids: `hsg-cp-mN-*`.

## 6. Grading convention (this track)

- Every challenge's boilerplate is a runnable contest skeleton:
  `bits/stdc++.h`, fast I/O, `solve(istream& in, ostream& out)` stub.
- Learner code = the whole contest logic. Tests redirect
  `std::cin`/`std::cout` (the platform's exact per-test pattern), call
  `solve`, and assert full output with `CHECK_LINES` — i.e. every test is
  a full input→output verdict on contest data, not a function probe.
- Hidden tests live in the test file (server-side only); visible examples
  match the statement's Ví dụ. Vietnamese test names (proven sanitizer).
- Reference (R) + near-miss wrong (W) solutions ledger for the two-sided
  container harness (same pattern as every existing track).
