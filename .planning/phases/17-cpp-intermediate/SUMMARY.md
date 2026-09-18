# Phase 17 — Course: C++ — Intermediate — SUMMARY

Date: 2026-09-13
Status: **COMPLETE**

## Course

Track `cpp`, course `cpp-intermediate` — **12 modules, 65 lessons (12
checkpoints), 24 practice sets, 60 challenges**, ~28 h estimated. Full EN + VI
parity (65/65 lesson VI overlays + MDX, 60/60 challenge VI sidecars, module +
course overlays). Prerequisite: `cpp-beginner`. Track path:
cpp-beginner → **cpp-intermediate** → (future advanced, not started).

Note: this platform has no separate quiz entity — knowledge checks live inside
lesson MDX per house convention; graded exercises are the 60 challenges.

## Modules

memory-and-lifetime · object-oriented-design · inheritance-polymorphism ·
operators-copy-move · stl-fundamentals · iterators-algorithms · modern-cpp ·
smart-pointers-raii · templates · errors-and-files · dsa · cppi-final-project
(capstone: file-persisted Library CLI — classes, STL, optional-based
validation, robust record parsing).

## Architecture discovered (reused, not reinvented)

- Content-as-data under `src/content/tracks/<track>/courses/<course>/`:
  `course.json` (module references) → `modules/<id>/module.json` (lesson +
  practice references) → `lessons/<id>.json` + `.mdx` (+ `.vi.json`/`.vi.mdx`),
  practice manifests at `modules/<id>/practices/<pid>.json` with
  `practices/<pid>/challenges/<cid>.json` (+ `.vi.json`), checkpoint challenges
  under `lessons/<lesson-id>/challenges/`.
- Grading contract (`src/workers/cpp-runtime.ts`): each test is its own
  translation unit that `#include "solution.cpp"`; CHECK-style macros; C++20.
- Generated MDX import map (`src/lib/curriculum/mdx-map.ts`, 884 imports;
  regenerate with `pnpm content:map` — runs prebuild/predev).

## Files created/modified (all mine; nothing committed)

- New: `src/content/tracks/cpp/courses/cpp-intermediate/**` (full course tree)
- New: `scripts/content-authoring/cppi.py`, `cppi_course.py`, `cppi_m1..m12.py`,
  `cppi_wire.py`, `cpp-intermediate-solutions.mjs` (R/W ledger, separate from
  Beginner's), `verify-challenges-cppi.mjs` (dedicated harness)
- Modified: `src/content/tracks/cpp/track.json` (course registration),
  `scripts/content-authoring/validate-content.ts` (course entry),
  `src/lib/curriculum/mdx-map.ts` (regenerated), `docs/COURSE-CPP-INTERMEDIATE.md` (new),
  `.planning/STATE.md` (session block)

## QA — actual results today

| Gate | Result |
|---|---|
| Two-sided challenge harness (clang C++20) | **60/60** (R passes all, W fails ≥1) |
| validate-content.ts | exit 0 — 12 modules, 65 lessons, EN/VI SYNC, 185 nodes/locale |
| Typecheck (`tsc --noEmit`) | clean |
| Lint (`eslint .`) | 0 errors, 0 warnings |
| Unit + integration | **160/160** (27 files) |
| Production build | exit 0 |
| E2E (Playwright, full suite) | **36/36** (vs running :3000 stack via temp config, deleted after) |
| `git diff --check` | clean |

## Defects the harness caught during authoring (all fixed)

- Test snippets are separate binaries → cross-test state broke grading
  (m2 counter tests redesigned self-contained)
- `\n` escaping bug class (literal backslash-n in JSON) — eliminated by
  raw-string authoring discipline from m5 onward
- Behaviorally-equivalent "wrong" solutions (m9 stack, m11 two) → replaced with
  genuinely wrong variants (move-only element test, BST delete bug)
- Real reference bugs: missing include, lambda capture bug (m6), ref-returned
  static counter (m3), LIFO-vs-FIFO test contradiction (m8)

## Global-id hygiene (my files only)

Cross-course namespace collisions resolved by renaming **my** copies:
`choosing-stl-containers`, `cppi-iterators`, `cppi-checkpoint-capstone-lesson`,
module `cppi-final-project`. Lesson-id `rule-of-three` reference fixed →
`copy-semantics`. Orphan ledger pair `cppi-m10-parse-records` removed
(60 R + 60 W, no duplicates). Checkpoint challenge dir renamed to match the
renamed lesson (`cppi-checkpoint-final/`), restoring module 12's challenge.

## Multi-agent safety

- No destructive git commands; nothing committed; Beginner/Intermediate-agent
  and web/python files untouched (collisions fixed on my side only).
- No Beginner defects discovered in this pass (nothing to document as broken).
- Pre-existing repo-wide state (Prettier drift, ~570 uncommitted paths) left
  for the user's coordinated commit decision, as recorded in STATE.md.

## Remaining work

- C++ — Advanced intentionally not started (per instructions).
- `mdx-map.ts` is generated: after any lesson rename, run `pnpm content:map`
  (unit tests fail against a stale map — transient, already resolved here).
