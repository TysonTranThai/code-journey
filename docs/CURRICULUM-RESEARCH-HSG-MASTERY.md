# HSG Mastery — Curriculum Research (Vietnamese HSG THPT / Olympiad problem-solving)

Date: 2026-09-21. Sources: live VNOI wiki fetch (see §Sources), the repo's own
research corpus (`docs/CURRICULUM-RESEARCH-HSG-*.md` — verified material from the
Beginner/Intermediate/Advanced builds, re-checked against loaders/schema this
session), and repository inspection. No copyrighted problem statements are
reproduced; all exercises are original.

## 1. What "Mastery" means here (and what it must not be)

The HSG ladder already teaches: C++ fundamentals (Beginner), the standard
toolkit — complexity, greedy, binary search, Fenwick/segment trees, DSU,
Dijkstra, DP families, hashing/KMP, number theory (Intermediate), and the
advanced machinery — flows, SCC/2-SAT, LCA/HLD, lazy structures, suffix
structures, geometry, combinatorics (Advanced). A fourth course that re-lectures
any of these is dead weight.

What the ecosystem says separates strong contestants is NOT more algorithm
knowledge. From VNOI Wiki's exam-skill corpus (Phạm Văn Hạnh's HSGQG advice
series, fetched live this session):

- "VOI là kì thi đòi hỏi kĩ năng hơn là tư duy thuật toán" — the exam demands
  **execution skill** over algorithm novelty; "cứ trâu hết là vào vòng hai"
  (bug-free brute force carries you) is community consensus.
- The **complexity budget heuristic**: an algorithm whose op-count at max-n is
  ≲ 3×10⁸ is code-it-now territory; optimizing further often costs more points
  in implementation risk than it gains in TLE tests.
- **Read all problems, rank them, harvest partials**: OI partial scoring means
  subtask points are real points; "duyệt trâu" (brute force) is a scoring
  strategy, not a failure state.
- **Stress testing (3-program harness)**: candidate + trusted brute + random
  generator, looped until mismatch, is the standard taught technique
  (2School Guideline's exam-room guide: "Stress test bao gồm 3 code").
- Time allocation: 180 min / 3 problems makes read-think-code-check a budgeted
  activity; post-contest self-review is explicitly part of the method.

So Mastery's mandate: **problem-solving process** — decomposition, constraint
reasoning, observation discovery, synthesis, optimization, proof, adversarial
analysis, partial scoring, decision-making — trained almost entirely through
problems, with no new algorithm lectures.

## 2. Failure modes documented in the community (drives the wrong-solution library)

Recurring traps cited across VNOI/2School material and reflected in the prior
courses' verified challenge corpora: wrong greedy accepted on samples but
failing exchange-argument edge cases; DP with a wrong state definition that
passes small tests; stale/reset-in-wrong-place DP accumulators; graph direction
errors (treating undirected as directed); assuming Dijkstra-like greedy on
graphs with negative edges; int overflow on n·(n−1)/2-scale answers; modulo
sign errors on subtraction; off-by-one on boundary conditions; double-counting
symmetric pairs; missing a case class (e.g., "all equal", "n = 1"); solutions
that pass samples but die on adversarial orderings (star graphs, sorted-vs-
shuffled input, duplicate-heavy arrays); correct-but-too-slow solutions where
the constraint line forbids the chosen complexity.

## 3. Difficulty system (schema-verified)

The platform exposes `difficulty: beginner | intermediate | advanced` (schema.ts
line 24) and practice `level: imitation | guided | independent | combination |
real-world | debugging | mini-build`. Mastery maps its internal ladder onto
these real schema values — it does NOT invent new enums:

| Mastery stage | difficulty | level | Meaning |
|---|---|---|---|
| Guided | advanced | guided/imitation | Scaffolded; the observation is named in the prompt |
| Standard | advanced | independent | Unfamiliar包装; topic unnamed; single technique |
| Unfamiliar | advanced | combination | Topic unnamed; synthesis of 2 techniques |
| Hard | advanced | real-world | Multi-step reasoning; proof demanded in hints |
| Expert | advanced | debugging/mini-build | Wrong-solution hunting, optimization, adversarial work |
| Olympiad-style | advanced | combination/real-world | Full pipeline: model → observe → prove → implement |

All challenges use `difficulty: "advanced"` (this is the top of the real schema)
with the process burden expressed through level choice, prompt design, and
test design — not through fabricated difficulty strings.

## 4. What the repo enables (inspected this session)

- C++20 sandbox (`-std=c++20`, 0.5 CPU, 512 MB, 20 s, no network) — same as
  Intermediate/Advanced; constraints in this course respect it (measured: the
  harness compiles + runs each test locally the same way).
- Two-sided QA harness pattern (`verify-challenges-hsga.mjs`): R must pass all
  tests, W must fail ≥ 1; per-course ledger (`*-solutions.mjs`); challenge-id
  filter argv for fast scoped re-runs. Mastery gets its own harness clone +
  `hsg-mastery-solutions.mjs` so no other course's ledger is touched.
- ID prefixes are course-owned (`hsg`, `hsgi`, `hsga`, `hsgx` in-flight by
  another agent) — Mastery uses **`hsgm-`** prefix; no collisions possible.
- Courses are referenced from `track.json`; the loader enforces global ID
  uniqueness, EN/VI overlay completeness, and course.json presence.
- `hsg-intensive` (hsgx) is untracked work by another agent — Mastery does not
  depend on it, does not touch it, and assumes no shared state.

## 5. Course design derived from the research

- **Problem-first**: every module is 3 lessons + 1 practice set + 1 checkpoint;
  lessons are short (8–14 min) and end in executable work; the practice sets
  carry the load. Topic names never appear in problem statements — recognition
  is the student's job.
- **Mixed identification sets**: at least three practice sets present problems
  with NO thematic module label (their module ids are process-themed, not
  technique-themed), forcing technique identification.
- **Wrong-solution clinic**: dedicated module where most challenges embed a
  plausible-but-buggy R/W pair — the challenge is to make the FIXED version
  pass; the W encodes the classic trap.
- **Optimization lab**: challenges ship a correct-but-too-slow algorithm as the
  W and demand the passing complexity as R (a W that TLEs on the big test but
  passes small ones — verified by test design).
- **Counterexample lab**: recognition-style challenges where the answer encodes
  the smallest breaking input for a given wrong claim.
- **Partial-scoring lab**: challenges whose big test is the "full solution"
  gate while smaller tests reward the subtask solution — the prompt teaches
  scoring the partials.
- **Two full mock contests** (module-format contests like Advanced's) plus a
  final synthesis module.

## 6. Sources

- VNOI Wiki — "Tổng hợp các lời khuyên cho các kỳ thi" (fetched live 2026-09-21;
  Phạm Văn Hạnh's HSGQG advice series) — HIGH: complexity budget (~3×10⁸),
  brute-force-as-strategy, execution > novelty, mock-exam discipline.
- 2School Guideline — "Những kinh nghiệm trong phòng thi Tin học" (search
  snippet verified; stress-test 3-code harness) — HIGH.
- docs/CURRICULUM-RESEARCH-HSG-{BEGINNER,INTERMEDIATE,ADVANCED,INTENSIVE}.md —
  repo-verified format facts (180 min × 2 days, OI partial scoring, subtask
  structure) carried forward with their source grades.
- Repository inspection: schema.ts, loaders.ts, sandbox.ts, cpp-runtime.ts,
  verify-challenges-hsga.mjs, existing course corpora — ground truth.
- USACO Guide / Codeforces community practice-methodology threads (search
  results reviewed; general practice-workflow corroboration) — MEDIUM.
