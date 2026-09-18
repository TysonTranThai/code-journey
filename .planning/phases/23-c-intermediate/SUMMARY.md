# Phase 23 — Course: C — Intermediate — SUMMARY

Date: 2026-09-15
Status: **COMPLETE**

## Course

Track `c`, course `c-intermediate` ("C — Trung cấp") — **16 modules, 64
lessons** (48 teaching + 16 checkpoint lessons), 32 practice sets, **84
challenges** (68 practice + 16 checkpoint), ~33.6 h estimated (1181 min
lessons + 838 min practice). Full EN + VI parity (64/64 lesson MDX × 2
locales, VI overlays on every module, practice set, and challenge —
validator: `SYNC: EN/VI structures match for c-intermediate`, 229 nodes
load clean per locale). Id namespace: `cint-` on every id kind; validator
enforces global uniqueness (cross-kind collision `cint-p4-dispatch`
practice-set-vs-challenge found and renamed to `cint-p4-dispatch-build`).

Arc (practice-first, memory as the spine): translation units & linkage →
pointers deep dive → ownership & the heap → function pointers & callbacks →
structs & data modeling (opaque types) → strings & buffers → linked data
structures → hash tables (open addressing + chaining) → generic programming
(`void *`, `qsort`, `_Generic`) → preprocessor mastery (X-macros,
`_Static_assert`) → trees & heaps → binary files & robust parsing (verified
gradeable file I/O) → error handling & robust APIs (cleanup-goto, two-phase
init) → undefined behavior (why the optimizer may assume) → C11 threads
(`threads.h`, latch-choreographed multi-threaded tests — probed working in
the sandbox) → **MiniKV capstone** (persistent key-value store integrating
the whole course: arena core, owned keys, binary log with magic+checksum,
iterator, corruption handling).

## Toolchain (probed, not assumed)

- `gcc 14.2.0` / musl in `codejourney-sandbox:latest`; `-std=c23` baseline
  (verified by the Beginner phase, re-confirmed via the shared runtime).
- Single-TU grading — multi-file linking taught via observed compiler/linker
  output, stated honestly in lessons.
- No sanitizers/Valgrind/debugger in image (Beginner-phase probe stands) —
  memory-bug challenges use deterministic behavioral discriminators:
  pointer identity, pre-dirtied buffers, checksum mismatches. No sanitizer
  claims anywhere.
- C11 `threads.h` verified executable in-sandbox (`mtx_t`, `cnd_t`, `thrd_t`,
  no `-pthread` on musl) — Module 15 grades real multi-threaded tests.
- File I/O under `/tmp` verified gradeable — Module 12 + capstone use it.

## Verification (every number machine-produced)

- **Two-sided harness** (`verify-challenges-cint.mjs`, real sandbox):
  `challenges: 84 · R tests: 102 pass / 0 fail · W tests: 90 fail / 16 pass ·
  verdicts: 84 clean, 0 ref-fail, 0 wrongly-pass`. Harness counts
  challenge-level verdicts (a W fails if it fails ≥1 test).
- **Curriculum validator** (`validate-content.ts`): schema-valid, unique ids
  across kinds/courses, `LOCALE: en — 229 nodes / vi — 229 nodes`,
  linear path (c): 148 lessons, exit 0.
- **Typecheck** PASS · **lint** PASS · **unit tests** 160/160 ·
  **build** PASS · **E2E 36/36** (incl. 390px mobile + keyboard flows; run
  against a production `next start` on :3456 because a long-lived dev server
  holds the :3000 lock — infra note, not a product change).
- **Beginner regression:** C Beginner harness **158/158 two-sided OK**;
  `c-beginner/course.json` untouched (22 modules).

## Bugs caught by the verification loop (highlights)

- The round-trip test caught a real bug in my own reference `kv_load`:
  save wrote a 4-byte count field load never read (every read shifted 4
  bytes → EBADSUM). Also: checksum read big-endian while written
  little-endian; `fgetc`-then-`fputc` corruption idiom appended instead of
  replaced (fixed by re-seeking before the write).
- A W "passing" was harness semantics, not content: per-test counting
  flagged challenges where a W failed some tests — corrected to
  challenge-level verdicts.
- Authoring-generator defects fixed at the source and re-emitted: VI
  title/description/mdx argument rotation in 10 module scripts (AST-verified
  fix), duplicated `minutes` in 4 scripts, invalid schema `level` values
  (invalid ones now dropped with a warning centrally in `challenge()`).

## Multi-agent safety

- Zero destructive git commands; no `git reset/checkout/restore/clean`.
- My footprint is purely additive (untracked new files; `git status`
  deletions in scope: 0). All `M src/lib/**` diffs predate my work
  (parallel agents / platform phases) — untouched.
- C Beginner preserved: YES (158/158 harness + course.json intact).
- C++ Advanced / Java tracks preserved: YES (no files touched; validator
  shows all five linear paths healthy).

## Files created (scope: C Intermediate)

- `docs/CURRICULUM-RESEARCH-C-INTERMEDIATE.md`,
  `docs/COURSE-C-INTERMEDIATE.md`
- `src/content/tracks/c/courses/c-intermediate/**` (course + 16 modules:
  json/mdx ×2 locales, 32 practice sets, 84 challenges, checkpoints)
- `scripts/content-authoring/cint.py`, `cint_course.py`, `cint_m1..16.py`,
  `cint-solutions.mjs`, `verify-challenges-cint.mjs`

## Shared infrastructure changes

None. The C runtime (`src/workers/c-runtime.ts`) and `"c"` schema/execute
arms shipped with the Beginner phase and were consumed as-is.

## Known limitations

- No ASan/Valgrind-based grading (image limitation, taught around honestly).
- Sandbox grades single TUs; no multi-file compilation challenges.
- Threads are C11-only (no POSIX-only APIs graded).
- E2E executed against a production server on :3456 (dev-server lock on
  :3000 held by an unattributable long-lived process — left running).

## Remaining issues

- None blocking. Repo-level: ~600 uncommitted parallel-agent files remain
  uncommitted (commit strategy is the user's call).
