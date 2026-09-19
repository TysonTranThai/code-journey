# HSG Intermediate — Curriculum Research (verified environment)

Date: 2026-09-19. Environment claims probed live today in the actual sandbox;
curriculum claims grounded in the real HSG Beginner course on disk + provincial
HSG sources. Nothing from memory alone.

## 1. Execution environment (re-verified 2026-09-19, not assumed)

| Question | Verified answer | Evidence |
| --- | --- | --- |
| Compiler | **g++ (Alpine) 14.2.0** | `docker run codejourney-sandbox:latest g++ --version` today |
| Standard | **C++20** (`-std=c++20`) | live probe + `src/workers/cpp-runtime.ts` |
| Flags | `-Wall -Wextra -Wpedantic`, **no `-O2`** — tests compile at -O0 | live probe (bits TU = 1.1 s) + runtime source |
| bits/stdc++.h | available | live probe, PROBE_OK |
| Job budget | 20 s per submission (all tests: compile + run) | `src/app/api/challenges/run/route.ts:81-86` |
| Memory | 512 MB | `route.ts:88-90` |
| Network / FS | none / /tmp only | sandbox.ts |
| Grading seam | `void solve(std::istream&, std::ostream&)`, byte-exact output | hsg.py BOILERPLATE + harness |

**Consequence:** every problem's constraint ceiling sized so intended complexity
passes comfortably at **-O0** (Beginner research already established this
discipline; kept identical).

## 2. What HSG Beginner actually shipped (audited on disk, 2026-09-19)

20 modules, 65 lessons, 20 practice sets, 127 two-side-verified challenges,
3 mock contests. Challenge ids audited per module:

- DP (M15): fib, stairs, coins (greedy-count coin set), knapsack 0/1, maxrun (max subarray sum), potions (DAG longest path), checkpoint.
- Two pointers (M17): pair-sum, ksum, subsum (shortest subarray ≥ s), merge, distinct-window, checkpoint (min max-gap via shrinks).
- Number theory (M11): gcd/lcm, prime trial division, digit sum, divisor count/enumeration, sum of divisors.

**So genuinely NEW at Intermediate:** LIS, LIS-reconstruction, knapsack
variants (unbounded/count), bitmask DP, string hashing, KMP, sieve, prime
factorization, modular exponentiation, modular combinatorics, coordinate
compression, sweep-line, binary search on answer, Fenwick, segment tree, DSU,
Kruskal/Prim, Dijkstra, 0-1 BFS, Floyd–Warshall, topological sort, tree
diameter/height DP, interval greedy, meet-in-the-middle, amortized analysis,
constraint-driven algorithm selection as an explicit skill.

## 3. Provincial-level expectations (sources, 2026-09-19)

- VNOJ problem taxonomy: provincial HSG problem sets categorize by *Số học*,
  *Hashing*, *Mảng cộng dồn*, *C++ STL (Heap, Set, Map…)*, *Quy hoạch động*,
  *Đồ thị* at province level — i.e. exactly the deferred list, now due.
- Vietnamese HSG prep roadmaps (learningvn, fullhousedev, viblo writeups):
  provincial medium tier = CTDL (data structures: Fenwick/segment/DSU/heap) +
  advanced graphs (Dijkstra/MST/topo) + DP mastery + string hashing; national
  tier adds flows, HLD, suffix structures, advanced optimization.
- Exam structure (province THPT): 3–4 problems, 150–180 minutes, per-problem
  100-point subtask grading — partial scoring is a core skill.

**Curriculum decision:** teach the provincial-medium toolset with recognition
first, deriving second; flows/matching/HLD/suffix structures/digit DP stay
Advanced. Lazy propagation deferred (not a provincial-medium staple).

## 4. Course identity

- Track `hsg`, course **`hsg-intermediate`** ("HSG Tin học — Trung cấp" /
  "Competitive Programming — High School Intermediate").
- Prerequisite: `hsg-beginner`. Language `cpp` only.
- Authoring: `hsgi.py` clones `hsg.py` with BASE/SOLUTIONS pointed at
  `hsg-intermediate` + a separate `hsg-intermediate-solutions.mjs` ledger;
  harness runs as `verify-challenges-hsg.mjs <filter> <ledger>` (existing
  argv[3] support — no harness code change needed).
- Challenge-id prefix: `hsgi-` to keep ledgers and ids disjoint from Beginner.
- Difficulty progression: Level 1 recognize → L2 modify → L3 combine → L4
  derive → L5 contest-style unfamiliar (documented per module).
