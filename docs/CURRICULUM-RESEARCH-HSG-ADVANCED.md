# Curriculum Research — HSG Advanced (Tuyển Học Sinh Giỏi Tin học — Nâng cao)

Date: 2026-09-19 · Phase 29 · Authoring agent for `hsg-advanced`

## Scope

This research decides the **final syllabus** for the third HSG course. It builds on
`docs/CURRICULUM-RESEARCH-HSG-BEGINNER.md` and
`docs/CURRICULUM-RESEARCH-HSG-INTERMEDIATE.md` — Beginner covered the
foundational contest layer (I/O → STL → recursion → basic DP/graphs); Intermediate
covered the provincial-HSG algorithm layer (Fenwick/segment trees, Dijkstra/0-1
BFS/Floyd, DSU/Kruskal, DAG DP, LIS, knapsack, bitmask DP, hashing+KMP, two
pointers, number theory).

Advanced targets students who clear provincial HSG and are preparing for
national-level (quốc gia) difficulty and Olympiad-style synthesis.

## Sources (actual, consulted 2026-09-19)

1. **USACO Guide — "Advanced USACO Topics"** (usaco.guide/adv): explicitly frames
   segment-tree-with-lazy, strongly connected components, max-flow, and suffix
   structures as the advanced tier beyond Gold; notes segment tree beats, treaps,
   and slope trick are *usually outside the scope of even advanced contests* —
   direct evidence for deferral decisions.
2. **USACO Guide — Digit DP** (usaco.guide/gold + vplanetcoding analysis): digit
   DP ("count integers in [A,B] with property P") is standard Gold/early-advanced;
   included here as an entry-advanced pattern.
3. **VNOI Wiki Project — Heavy-Light Decomposition** (vnoi.info wiki; announced
   via the VNOI wiki project) and Viblo "Heavy-Light Decomposition: Khi Nặng Hóa
   Nhẹ": HLD + segment tree is a normalized topic for Vietnamese chuyên-tin
   students preparing provincial→national; confirms HLD belongs in the Vietnamese
   advanced track (not deferred further).
4. **FPTOJ wiki** (wiki.fptoj.com) — curated VNOI archive reading list for
   chuyên tin: same topic ordering (trees/LCA → HLD → SCC → flow → advanced DP).
5. **Codeforces EDU** (structure only, no problems copied): advanced tier places
   suffix arrays, segment trees, and flows as the bridge from strong provincial to
   national/Olympiad contestants.

No copyrighted contest problems were copied. All challenges are original
educational problems inspired by algorithmic concepts, following the same
original-problem policy as Beginner/Intermediate.

## Progression decision (evidence → syllabus)

| Evidence | Decision |
| --- | --- |
| Lazy segtree = core of USACO Adv + VNOI chuyên-tin | **Include** (range-assign + range-add + max-subarray push/pull) |
| HLD normalized in VNOI; but heavy prerequisites | **Include** AFTER Euler tour + binary lifting/LCA + tree DP, as the tree-module finale |
| SCC/Kosaraju + condensation | **Include** (directed-graph structure recognition) |
| Max-flow (Dinic) + bipartite matching | **Include** with modeling emphasis (Kőnig's theorem as interpretation, min-cut duality) |
| Min-cost flow | **Defer** — beyond national-HSG beginner-of-advanced; rarely provincial |
| Suffix array + LCP | **Include** (O(n log² n) doubling — simple, robust, fits sandbox) |
| Suffix automaton | **Defer** (USACO Adv "usually outside scope") |
| Aho–Corasick | **Defer** (multi-pattern rarely needed at this level; trie already covers the concept) |
| Digit DP | **Include** (tight-bounds pattern) |
| Interval DP + Knuth-style reasoning | **Include interval DP; defer Knuth optimization** |
| Segment tree beats / treap / slope trick / link-cut | **Defer** (explicitly out-of-scope per USACO Adv) |
| Bridges/articulation | **Include** (natural continuation of DFS trees from Intermediate) |
| Computational geometry (integer, cross-product core) | **Include** as one module: orientation, segment intersection, convex hull (Andrew), precision discipline |
| Combinatorics (inclusion–exclusion, precomputed factorials mod p) | **Include**; generating functions **defer** |

## Sandbox calibration (verified, not assumed)

- g++ 14.2.0 (Alpine), `-std=c++20`, flags `-Wall -Wextra -Wpedantic` at test
  compile (from `src/workers/cpp-runtime.ts` via the harness).
- Docker sandbox (`src/workers/sandbox.ts`): `--network none`, read-only rootfs,
  `--cpus 0.5`, `--pids-limit 64`, cap-drop ALL, non-root, output cap 256 KB.
- Job budget for C++: **20 000 ms timeout / 512 MB memory**
  (`src/app/api/challenges/run/route.ts`), wall-clock hard cap 30 s. The budget
  covers compile + all tests, so per-test algorithmic time must stay well under
  ~1–2 s at 0.5 CPU. All Advanced reference solutions are sized for this
  (n ≤ 2·10⁵ for O(n log n) structures; flows sized n ≤ ~500, m ≤ ~2·10⁴).
- Recursion depth: pids 64 + default 512 MB stack cap — deep DFS is written
  iterative or with explicit depth control in reference solutions (HLD/LCA use
  iterative DFS or BFS ordering).

## Resulting module boundary

**In (Advanced):** lazy segment trees (range assign/add, max-subarray), Fenwick
range-update patterns, binary lifting/LCA, Euler tour + tree DP + rerooting,
HLD (+segtree), SCC (Kosaraju) + condensation, bridges/articulation, Dinic
max-flow + bipartite matching, advanced shortest-path reasoning (state graphs,
Bellman-Ford detection), digit DP, interval DP, tree DP (advanced), suffix array
+ LCP (doubling), Z-algorithm, trie, modular inverse/ext-Euclid/phi/CRT,
combinatorics mod p, computational geometry (integer core), meet-in-the-middle,
offline sweeps, synthesis.

**Deferred (documented, not silently dropped):** segment tree beats, treap/implicit
treap, slope trick, link-cut trees, persistent structures, min-cost flow, matching
beyond bipartite (Hungarian for weighted), suffix automaton, Aho–Corasick, Knuth
optimization, advanced computational geometry (rotating calipers, half-plane
intersection), generating functions.

## Difficulty ladder (actual use)

L1 introduce technique → L2 implement correctly → L3 apply to unseen data shape →
L4 combine with a second technique → L5 unfamiliar HSG-style problem → L6
Olympiad-style synthesis (mock contests). Every practice set spans ≥3 levels; no
module is all-L7.
