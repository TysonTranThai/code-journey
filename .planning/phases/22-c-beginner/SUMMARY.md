# Phase 22 — Course: C — Beginner — SUMMARY

Date: 2026-09-15
Status: **COMPLETE**

## Course

Track `c`, course `c-beginner` ("C — Cơ bản") — **22 modules, 84 lessons**
(including 22 checkpoints), 44 practice sets, **158 challenges** (136 practice +
22 checkpoint), **469 test cases** (all with educational per-test hints), full
EN + VI parity (84 lesson MDX bodies × 2 locales, VI overlays on every module,
practice set, and challenge). Course metadata: first course in the track, so
`prerequisites: []`. Id namespace: `cb-`/`cbN-`/`cb-pN-` prefixes; global id
sweep shows **0 collisions** across the whole curriculum (loader enforces a
single global namespace across all id kinds — cross-kind collisions with
cpp/python lessons were found by sweep and renamed).

Arc (practice-first, per the phase spec): what is C / anatomy → variables &
types → I/O & formatting (sscanf-based, sandbox is non-interactive — honesty
noted in lessons) → operators & conversions → conditionals → loops → functions
→ scope/lifetime/static → arrays → strings as memory (NUL terminator never
hidden) → **pointers fundamentals (10 lessons — the largest module)** →
pointers & arrays/pointer arithmetic → dynamic memory & ownership → structs →
enums/typedef → file I/O (verified executable in the sandbox: fopen/fgets/fputs
under /tmp and CWD) → preprocessor & headers → multi-file patterns (static,
declaration/definition discipline, API boundaries — single-TU sandbox stated
honestly) → debugging (compiler-warnings-driven + deterministic forensics; no
sanitizer claims — ASan verified unavailable in the image) → data structures
from scratch (dynamic array, linked list, stack, queue) → searching/sorting/
recursion with Big-O intuition → project engineering & capstone.

## Toolchain (probed in the real sandbox image, not assumed)

- `gcc 14.2.0` inside `codejourney-sandbox:latest` (pulled in by the g++ package)
- `-std=c23` accepted → course standard is **C23** (default `gnu17`, C17 available)
- Compile of a harness test: ~0.04 s; sandbox runs `--network none`
- **ASan/UBSan linking fails** (Alpine splits sanitizers; musl limitation) →
  debugging module graded via warnings + forensics, zero sanitizer claims
- File I/O verified working (fopen/fgets/fputs, /tmp + CWD)

## Runtime (shared infrastructure — additive)

New `src/workers/c-runtime.ts` modeled on `cpp-runtime.ts`: C test harness with
`setjmp/longjmp` failure protocol (each failed test exits 1 with an educational
hint on stderr), `dup2`-based output capture helper `cj_capture`, `main`
renaming via include-trick, `C_STANDARD_FLAG = -std=c23`. One C23 correctness
constraint baked in: `cj_test_body` defined **before** `main` (implicit
function declarations are illegal in C23; GCC 14 enforces).

Shared files extended additively (all prior agents' diffs preserved):
- `src/lib/curriculum/schema.ts`: `"c"` added to the challenge language union
- `src/lib/execution/types.ts`: `"c"` unions (4 touchpoints)
- `src/workers/execute.ts`: C dispatch
- `src/workers/sandbox.ts`: C compile/run pipeline
- `src/app/api/challenges/run/route.ts`: C budgets (merged cleanly with
  parallel agents' pending changes)
UI needed no change (Monaco supports `language: "c"` natively).

## QA gates (all green, all evidence real)

- **Formal harness** `verify-challenges-c.mjs`: **158/158 two-sided OK** in the
  real sandbox image — every reference solution passes every test (469 total),
  every intentionally-wrong solution fails ≥1 test. Batched single-container
  design (per-test docker spawns timed out at 600 s; batching mirrors
  `_cb_smoke.mjs`)
- **Per-batch two-sided smokes** (modules 1–2, 3–4, … 20–22): every batch
  driven to R-all-pass / W-all-fail before the next batch was authored. Defects
  found and fixed this way include behaviorally-identical W solutions (literal
  pooling, no-op swaps), missed C23 rules (implicit declarations, digit
  separators), and test batteries not separating R from W
- **validate-content.ts: exit 0** — 11 courses × 2 locales synchronized
  (web-dev 3 + python 3 + cpp 3 + java 2 shells→1 finished + c-beginner;
  `c` linear path 84 lessons)
- Unit/integration **160/160** (loader test extended 4→5 tracks, following the
  cpp agent's precedent); E2E critical path **2/2** (run against the live dev
  server because Next 16 refuses a second dev instance per project);
  typecheck clean, lint clean (0 errors, 0 warnings)
- **Repo-wide `pnpm build`: PASS, 2366 pages** (up from 2078)
- Live route QA: course/lesson/practice/checkpoint/challenge routes 200;
  sitemap lists the course; data-layer locale probe: VI titles, VI lesson
  bodies, 84/84 linear lessons in BOTH locales

## Multi-agent safety

No destructive git commands; no resets/cleans. Untracked parallel-agent work
(c-intermediate shell, web-development-beginner migration deletions, javaa
files) untouched and verified loading. Shared-file edits were minimal additive
unions/dispatch arms merged on top of agents' pending diffs. One repo-level
discovery recorded: **lesson/module ids are globally unique across ALL courses
and kinds** — 11 of my ids collided with cpp/python/c-intermediate ids and were
renamed with a `cb-` prefix (mechanical rename incl. contentPath, module refs,
afterLesson anchors — 28 lesson files, 4+2 module dirs).

## Artifacts

- `docs/CURRICULUM-RESEARCH-C-BEGINNER.md` (GCC 14/C23, Exercism/K&R-informed
  design decisions, sandbox probe log)
- `docs/COURSE-C-BEGINNER.md` (course spec)
- `scripts/content-authoring/cb.py` + `cb_m*.py` batches + `cb-solutions.mjs`
  ledger + `_cb_smoke.mjs` + `verify-challenges-c.mjs` formal harness
- `.planning/phases/22-c-beginner/SUMMARY.md` (this file)

## Known limitations

- Sandbox is single-translation-unit: multi-file Make/CMake workflows are
  taught conceptually with single-TU-verifiable exercises (honest framing in
  lessons); no Make claims in graded challenges
- No sanitizers in the sandbox (verified): debugging is warnings/forensics
- Graded I/O is `sscanf`-based (non-interactive sandbox); interactive `scanf`
  habits taught in prose with width-limit safety rules
- VI language is in-page via `cj_locale` cookie; the long-running dev server
  (started before this course existed) caches per-URL locale for first-request
  locale — data-layer locale correctness proven directly (both locales load)
