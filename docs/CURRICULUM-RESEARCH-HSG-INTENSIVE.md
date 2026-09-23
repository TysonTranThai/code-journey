# HSG Intensive — Curriculum Research (Vietnamese HSG Tin học ecosystem)

Date: 2026-09-21. Sources fetched live (see Sources at bottom); repository patterns
inspected directly. This course is deliberately NOT a new algorithm catalogue —
HSG Advanced already teaches the algorithms. This stage trains **application**:
recognition, constraint→complexity mapping, debugging, optimization, subtask
strategy, and contest execution.

## 1. The Vietnamese HSG THPT context (verified)

- **Format.** Provincial (`HSG cấp tỉnh`) → National (`HSG quốc gia`, 2 days × 180
  minutes per session, per the 2025 rules: 3 problems per day, 100-point scale,
  OI-style grading — test-by-test scoring, subtasks explicitly named in the
  official structure). Sources: the 2025 HSGQG format writeups and vnoi.wiki.
- **Scoring.** OI-style partial credit: every test passed earns its share; a
  subtask is earned only if ALL its tests pass. This is the single most
  important strategic fact: **a partial solution is worth real points**, so
  course problems are built with subtask-shaped practice from day one.
- **C++ is the standard language**; contestants compile with GCC-style
  toolchains and read problems in Vietnamese with tight time limits designed
  so that the intended complexity is required (an O(n²) pass on n = 2·10⁵ is
  not a coincidence — it's the exam's design).

## 2. Exam-room strategy (from the Vietnamese CP community)

From VNOI Wiki's "Kinh nghiệm thi cử", 2School Guideline's exam-room guide, and
multiple HSG-prep writeups, the recurring advice is consistent:

1. **Read all problems first** and rank by expected difficulty; the first
   problem is usually a "cho điểm" (points-gift) problem — but test it carefully
   (a trivial-looking A1 that fails is the classic tragedy).
2. **Duyệt trâu (brute force) is a scoring strategy**, not a failure: when the
   optimal idea doesn't come, harvest partial points from small-n subtasks.
   Community advice: give a hard problem 10–15 minutes of thought; if no
   optimal solution appears, code the brute force and secure subtask points,
   then return if time remains.
3. **Chia subtask** — split your implementation so each subtask is solvable
   independently, avoiding the all-or-nothing trap.
4. **Stress testing with a 3-program harness** (candidate + trusted brute +
   random generator, compared in a loop) is the standard technique taught in
   Vietnamese CP circles (VNOI "viết trình chấm"; 2SG video guides). This is
   exactly what Module 9 teaches, executed for real in the sandbox.
5. **Debugging in the exam room**: binary-search your program with early
   returns, print intermediate values, keep a personal bug checklist.

## 3. What the first three HSG courses already teach (so Intensive must not)

Inspected from the repo (not assumed):

- **hsg-beginner**: 6 modules — C++ foundations, flow control, loops,
  1-D arrays, functions, 2-D arrays; final C++ review + practice.
- **hsg-intermediate**: 12 modules — complexity, STL, sorting/searching, prefix
  sums, greedy, binary search, recursion, bit manipulation, two pointers,
  strings, DS intro, recap.
- **hsg-advanced**: 12 modules — graphs, trees, DP, data structures, string
  algorithms, math, geometry, flow, LCA, DSU, segment trees, and a "mixed
  problems, exhaustive practice" capstone.

So Intensive's mandate is: **no new algorithm lectures**. Every module
re-uses those tools in unfamiliar, combined, or adversarial forms. Review
content is limited to short reference material (cheat sheets, templates,
checklists), explicitly framed as recall aids.

## 4. Course design derived from the research

- **20% review / 80% practice** by design; most activities are executable C++
  challenges, not reading.
- Problems are **original**, inspired by well-known structures (no copyrighted
  statements). Constraints mirror real HSG tables (1 ≤ n ≤ 2·10⁵ etc.).
- The **hidden-topic** discipline: recognition problems give constraints and
  behavior, never the algorithm's name.
- **Subtask-thinking** is embedded: optimization challenges start from a
  deliberately slow but CORRECT program and require making it pass; a wrong
  solution that produces wrong answers is not an "optimization".
- **Editorial workflow** mirrors the community's teaching order: brute force →
  why it fails → key insight → optimization → proof → complexity →
  implementation → common wrong approaches.

## 5. Difficulty system (repo-verified)

The platform schema exposes `level: "core" | "advanced" | "challenge"`. Mapping
used in this course:

| Course label | Schema value |
|---|---|
| Advanced | `advanced` |
| Hard / Very Hard | `challenge` |
| HSG Challenge / Olympiad-style | `challenge` (with note in text) |

The brief's suggested labels ("HSG Hard", "HSG Extreme") do not exist in the
schema; the schema's three levels are used as-is (constraint: use real schema).

## 6. Platform capabilities used (inspected, verified)

- C++ sandbox execution with deterministic per-challenge tests — verified live
  during hsg-advanced's QA; re-verified for Intensive via the same harness.
- Practice sets are **module-local** (loader inspection: practices resolve
  challenge ids within their module only) — so mock contests and daily/weekly
  packs are authored as practices inside their owning module.
- VI is the primary locale (Vietnamese-first statements, EN mirrors); the emit
  pipeline enforces a VI overlay for every EN node, and the sync validator
  checks both locales.

## 7. Sources

- HSGQG 2025 format/rules writeups (2-day × 180-min, 3 problems/day, OI
  partial scoring, subtasks) — MEDIUM-HIGH
- vnoi.wiki — "Kinh nghiệm thi cử", "Viết trình chấm" (stress-test harness
  technique) — HIGH (community-standard)
- 2School Guideline — "Những kinh nghiệm trong phòng thi Tin học" (đọc đề,
  duyệt trâu, chia subtask, sinh test, trình chấm) — HIGH
- USACO Guide / Codeforces community on problem recognition and speed
  training — MEDIUM
- Repository inspection: hsg-beginner/intermediate/advanced content, schema
  (`src/lib/curriculum/schema.ts`), loaders, prior HSG verify harness —
  ground truth for architecture claims.
