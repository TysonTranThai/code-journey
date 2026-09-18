# Phase 24 — Course: C — Advanced — SUMMARY

Date: 2026-09-17
Status: **COMPLETE**

## Course

Track `c`, course `c-advanced` ("C — Nâng cao") — **24 modules, 77
lessons** (53 teaching + 24 checkpoint lessons), 24 practice sets, **117
challenges** (93 practice + 24 checkpoint), ~20.9 h estimated (1252 min
of lesson + practice minutes). Full EN + VI parity (77/77 lesson MDX × 2
locales, VI overlays on every module, practice set, and challenge;
both-locale loader sweep clean). Id namespace: `ca-` on every id kind;
global uniqueness enforced by the validator. Course registered in
`src/content/tracks/c/track.json` (6th course; curriculum loaders test
updated to 6 tracks by prior shared changes — c-advanced listed in the C
track's course order beginner → intermediate → advanced).

Arc (from the pinned spec in docs/COURSE-C-ADVANCED.md — 24 modules):
object model (translation units, linkage, storage duration, alignment &
padding, representations) → the C abstract machine (sequencing, lvalues,
observable behavior) → advanced pointers (provenance, one-past-the-end,
function pointers, `restrict`) → UB & optimizer assumptions (signed
overflow, invalid shifts, strict aliasing, time-travel diagnostics) →
memory allocators (bump/first-fit/free-list tradeoffs) → ownership &
cleanup discipline (cleanup-goto, arenas, refcounts) → advanced data
structures → generic programming (`_Generic`, `void *` + callbacks, X-
macros) → preprocessor/compile-time (`_Static_assert`, token pasting) →
compilation pipeline → ELF & linking (probe `nm`/`readelf`/`objdump`
inside the sandbox via `system()`) → ABI & struct layout (hand-computed
offsets vs `_Offsetof`) → reading assembly (`gcc -S` diffing) → build
engineering (Make graph discipline) → debugging forensics (bisect,
shrink, heap invariants) → sanitizer concepts (UB diagnosis without
sanitizers in the image — honest framing) → POSIX processes
(fork/exec/pipe/wait/status-decode) → concurrency deep (pthreads,
mutex/rwlock/barrier, deterministic discriminators) → C11 memory model
(`memory_order`, SC-drift discriminators via sequencing) → sockets
(loopback TCP echo, UDP, exact-read loops — probed with `--network
none`) → high-performance I/O (`writev`, `mmap`, buffering) →
performance tuning (layout, branch/measure discipline; no fabricated
benchmarks) → security (overflow/TOCTOU/format-string *prevention*,
`snprintf` truncation semantics) → portability & capstone (endianness,
width-independent code, final integration checkpoint).

## Toolchain (probed, not assumed)

- `gcc 14.2.0` / musl in `codejourney-sandbox:latest`, `-std=c23`,
  harness flags `-lm` only (pthreads link into musl libc — verified).
- Verified by direct probes in the exact sandbox image before use:
  fork/exec/pipe/wait + WEXITSTATUS decode, `sigaction`, mutex/rwlock/
  barrier, C11 atomics + CAS, loopback TCP/UDP under `--network none`,
  `writev`, `mmap` (anonymous + file), `CLOCK_MONOTONIC`, `%zu`, host
  endianness via `__BYTE_ORDER__` (little-endian aarch64).
- No sanitizers/Valgrind/debugger in image (Beginner-phase probe stands).
  Module 16 teaches sanitizer *concepts* and UB diagnosis via
  deterministic behavioral discriminators; nothing claims sanitizer runs.
- Single-TU grading: every challenge is fully self-contained; helpers a
  test needs are defined in that test's TU (cross-TU references were a
  caught-and-fixed defect class).

## Verification (all numbers from real runs)

- **Two-sided harness: 117/117** — every reference solution passes all
  its tests, every wrong solution fails at least one (0 false passes),
  run against the staged course content via `scripts/content-authoring/
  _ca_smoke.mjs` (CB_STAGE unset = real course dir). On-disk counts
  verified: 117 EN challenge files + 117 VI sidecars + 117 unique ids.
  A late audit found 5 checkpoint challenges (m7/m9/m11/m13/m16) whose
  batch runs had crashed before staging — authored from their ledger
  solutions and re-verified (24/24 checkpoints green).
- Curriculum validation: `validate-content.ts` clean for c-advanced both
  locales; global id uniqueness (no cross-kind `ca-` collisions);
  schema limits (400-char description, 200-char summary, level enum) all
  pass after fixes; reference-vs-disk audit found 4 missing checkpoint
  lesson files (m7/m9/m11/m13 — crashed batch runs) — written and green.
- Unit/integration: **166/166 across 28 files** (includes curriculum
  suite with the new course, VI-content parity suite, practices suite).
- `content:map` indexes the new MDX (2012 lessons total incl.
  c-advanced).
- Typecheck: clean. Lint: 0 errors (2 pre-existing warnings in unrelated
  C#-script files). Production build: clean (`pnpm build`).
- E2E: critical-path 2/2, axe-core WCAG 2.1 AA audits 7/7, practice-flow
  6/6 (incl. 390px mobile viewport + keyboard operability) — 15/15.

## Multi-agent safety

- `git diff` over c-beginner, c-intermediate, cpp, java tracks: zero
  modifications — all preserved (beginner 22 modules, intermediate 16,
  cpp 20/19/12, java 14/15/15 on disk, untracked-new as built by their
  agents).
- Shared tracked files modified *by other agents in parallel* (schema,
  loaders, validators, web-development track content) were never touched
  by this phase; my only tracked-file edits: one line in
  `tests/unit/curriculum-loaders.test.ts` region updating the
  collective-course expectation (6 tracks; C-track list includes
  c-advanced) — the file was already collectively modified.
- No destructive git commands used; nothing committed.

## Known limitations

- 12 batch-authoring scripts (`ca_m*.py` + `ca.py` + `ca-solutions.mjs`)
  and `_fix_ca_b*.py` patches remain as untracked files in
  `scripts/content-authoring/` — they are the reproducible source of the
  content, kept for provenance (commit strategy is a user decision, same
  as previous course phases).
- Sanitizers, Valgrind, GDB, and multi-file linking are taught
  conceptually with observed-output alternatives; the sandbox cannot run
  them (verified, not assumed).
- Networking challenges use loopback only (container runs `--network
  none`); no external network claims anywhere.

## Verdict

**COMPLETE** — all gates green, sibling courses and tracks untouched,
both locales synchronized, 117/117 two-sided verified.
