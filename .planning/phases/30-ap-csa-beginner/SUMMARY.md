# Phase 30 — AP CSA Beginner / Foundations — SUMMARY

**Status: COMPLETE (2026-09-21)** · Track `ap-csa` (NEW) · Course `ap-csa-beginner`

## What was built

A new track (`ap-csa`) and its first course (`ap-csa-beginner`): Java foundations
targeting the revised (Fall 2025) AP Computer Science A framework. 20 modules,
80 lessons (60 teaching + 20 module checkpoints), 20 practice sets, 109 challenges
(89 practice + 20 checkpoint), fully bilingual (EN + VI), ~36.5 h estimated.
Auto-discovered by the platform loaders — no platform code changes required.

## Research

`docs/CURRICULUM-RESEARCH-AP-CSA.md` — verified against AP Central (College Board):
revised Fall-2025 framework has 4 units (Using Objects and Methods 15–25%,
Selection and Iteration 25–35%, Class Creation 10–18%, Data Collections 30–40%);
"Analyze Code" is the top-weighted skill class (37–53%); four FRQ types
(Methods/Control, Class Design, ArrayList, 2D Array); inheritance de-emphasized.
No College Board questions reproduced — all original exercises.

## Course shape (20 modules)

hello → variables → expressions → conditionals → loops → methods → strings →
classes → arrays → arraylist → searchsort → oop-design → inheritance (light, per
revised framework) → recursion → 2d → testing → reasoning → frq → integration →
readiness. Every module: 3 teaching lessons + practice set + checkpoint challenge.
Wrong-solution methodology targets AP-specific misconceptions (`==` vs
`.equals()`, integer division, `remove(int)` vs `remove(Integer)`, off-by-one
bounds, constructor-chain bugs, tie-breaking with `>=`).

## Execution environment (verified, not assumed)

- Sandbox: `src/workers/java-runtime.ts` — `javac --release 21`, JVM `-XX:+UseSerialGC -Xss4m`,
  per-test compilation of `Solution.java` + generated `Test_*.java` with the
  `CjTestBase` harness (checkEq array-aware, checkLines, capture, checkThrows).
- Local QA uses the SAME `buildJavaTestFile()` — byte-identical to sandbox.

## Verification (measured)

- **Two-sided harness 109/109**: every reference solution passes its full test
  suite; every wrong solution fails ≥ 1 test (`scripts/content-authoring/verify-challenges-apc.mjs`).
- Ledger ↔ disk mirror: 109 R + 109 W ↔ 109 challenges on disk, zero orphans.
- typecheck 0 · lint 0 errors (10 pre-existing warnings in other agents' files) ·
  unit 184/184 · build PASS · E2E 36/36 (Postgres + Docker up locally).

## Defects caught by gates (fixed during build)

- Long-vs-Integer boxed equality in tests (M17) — use `15L` literals.
- Two "wrong" solutions that were actually correct code (M17 bsearch, M20 shelf) —
  replaced with genuinely behavioral near-misses.
- Global ID uniqueness across kinds: lesson `apc-m15-find` collided with practice
  challenge of the same id — renamed challenge to `apc-m15-findcell`.
- M18 argument-shift put VI text in the `difficulty` slot — caught by the loader
  schema, restructured all three `write_lesson` calls to the 9-arg house shape.
- Missing `import java.util.*;` in M19/M20 sources (Solution.java compiles
  standalone before tests) — added per javaa.py house convention.
- Pre-existing MDX hazard in the other agent's uncommitted `hsg-intensive`
  course (`i<j` in a prose table broke MDX compile for the WHOLE curriculum) —
  minimal fix: `i&lt;j` in both locales.

## Multi-agent safety

- Other agents' uncommitted work preserved untouched: `LandingLoader.tsx` +
  `dictionaries.ts` (a11y pair), `verify-challenges-csharp-advanced.mjs`.
- Untracked `hsg-intensive` course + authoring scripts belong to another agent —
  only the two MDX compile-fix lines touched (build blocker, disclosed here).
- Nothing committed; no destructive git commands.

## Files

- New: `src/content/tracks/ap-csa/**` (track + course + 20 modules, EN+VI),
  `scripts/content-authoring/apc.py`, `apc_m1..m20.py`, `apc_finish_manifests.py`,
  `apc-solutions.mjs`, `verify-challenges-apc.mjs`,
  `docs/CURRICULUM-RESEARCH-AP-CSA.md`, `docs/COURSE-AP-CSA-BEGINNER.md`.
- Regenerated: `src/lib/curriculum/mdx-map.ts` (pnpm content:map).
