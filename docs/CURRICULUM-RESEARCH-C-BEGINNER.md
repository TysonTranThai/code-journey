# Curriculum Research — C — Beginner (Course: `c-beginner`)

Date: 2026-09-14. Researched before authoring. Every environment claim below was
**verified by direct probe** in the actual sandbox image on this machine — nothing
is assumed from documentation alone.

## 1. Platform reality (probed 2026-09-14, image `codejourney-sandbox:latest`)

| Probe | Result | Consequence for the course |
|---|---|---|
| `gcc --version` | **gcc (Alpine) 14.2.0** (installed as the `g++` package dependency) | No image change needed for C |
| `gcc -std=c23` full compile+run | **works** (`_Float`-era features present; `c2y` rejected) | Course baseline: **C23**, flagged explicitly |
| `gcc -std=c17`, default (gnu17) | works | Standards mentioned; all graded code is C23-clean and C17-compatible |
| ASan link (`-fsanitize=address`) | **FAILS — `libasan` not present** (Alpine splits sanitizers out) | **No sanitizer claims anywhere.** Debugging graded via compiler warnings + deterministic forensics |
| UBSan runtime | not probed beyond syntax (same missing-runtime risk) | not used |
| `setjmp.h`, `unistd.h`, pipe/dup2 | work | Test harness failure protocol + output capture |
| include-trick `#define main cj_learner_main` | works | Learner mains cannot collide with harness main |
| Compile cost, hello-grade test | ~0.04 s | Rich per-test compilation affordable |
| Default std | gnu17 | Runner passes `-std=c23` explicitly |

Runtime envelope (existing sandbox, unchanged): network `none`, read-only
rootfs, exec-able 64 MB `/tmp`, 16 MB noexec `/job`, 0.5 CPU, pids ≤ 64,
non-root. **Consequences:** no sockets/networking challenges; file-I/O graded
against `/tmp` files the challenge creates; wall-clock capped at 30 s; no
threads claims (single-threaded determinism only); no dynamic loading.

## 2. Standard baseline decision

- **Primary: C23** (`-std=c23`) — published as ISO/IEC 9899:2024; GCC 14 has
  nearly-complete C23 support (verified above). The course teaches the modern
  language: `bool` via `<stdbool.h>` noted as automatic in C23, `[[attributes]]`
  mentioned but not required, digit separators, `nullptr` mentioned as "newer C".
- **Compatibility rule:** all graded code must also compile under `-std=c17`
  (verified per batch by the QA harness for a sample; course text notes where a
  C23-only feature appears, which is prose-only, never graded).
- Sources: GCC 14 changes (gcc.gnu.org), C23 status pages, i-programmer/Seacord
  summaries of ISO/IEC 9899:2024 publication (2024). Not copied — used to set
  the baseline.

## 3. What makes a C *beginner* course (positioning)

Progression target: "never wrote C" → "can write, debug, test, compile,
organize, and build small C programs" with a memory-first mental model that
later feeds C Intermediate/Advanced, OS/systems topics, and C++.

Design decisions (practice-first, per Code Journey platform philosophy):

1. **Memory truth early, but beginner-scoped.** Null terminator, `sizeof`,
   stack vs heap, ownership ("who frees this?") are taught as first-class
   ideas; storage-duration formalism, function pointers, callbacks, custom
   allocators, `restrict`/aliasing, VLAs, `setjmp` mechanics are **excluded**
   (Intermediate/Advanced).
2. **Pointers get disproportionate practice** (the classic barrier): address
   observation, dereferencing, swap-through-pointers, pointer/array duality,
   pointer params, strings-as-pointers, struct pointers, dynamic memory,
   NULL/dangling/leak/double-free recognition — spread across modules 11–13 +
   capstone with escalating difficulty.
3. **Memory-safety habits normalized from day one:** bounds-checked loops,
   `snprintf` over `sprintf`, fgets with explicit limits, NULL checks after
   malloc, free-on-every-path, no uninitialized reads. Dangerous idioms appear
   only as *debugging targets*, never as recommended code.
4. **Grading honesty:** every executable challenge is gradeable in the probed
   sandbox. What cannot be graded deterministically (sanitizer runs, debugger
   interaction, gdb, make) is taught as prose + concept checks, never faked.

## 4. Existing platform architecture to reuse (inspected, not invented)

- Content-as-data: `module.json` → lessons (JSON+MDX, EN + `.vi.` sidecars) →
  practice sets (LEARN/DEEP-DIVE separation with `afterLesson` anchors) →
  checkpoint lessons with lesson-attached challenges. Track/course
  registration via `track.json` + course manifest. Validates via
  `scripts/content-authoring/validate-content.ts` (zod schemas, EN/VI sync,
  global-ID namespace, prerequisite resolution).
- Execution: `src/workers/execute.ts` (marker protocol `__TEST_RESULT__ <name>
  status=N`) → `src/workers/sandbox.ts` (hardening identical for every
  language; per-language job script only) → per-language runtime module.
  C++ runtime (`cpp-runtime.ts`) is the structural template: solution written
  as heredoc, syntax-check gate, per-test compile+run, educational stderr hint
  channel.
- QA: two-sided per-challenge harness pattern (`verify-challenges-*.mjs`) —
  reference solution must pass its own battery, wrong solution must fail it,
  byte-identical test files between QA and sandbox via the exported
  `buildXTestFile`.
- Deliberate-practice `level` stamping on practice-set challenges
  (imitation→mini-build), as shipped in all sibling courses.

## 5. C test-harness contract (new `c-runtime.ts`, modeled on cpp-runtime)

- Each test file: harness prelude → `#define main cj_learner_main` →
  `#include "solution.c"` → `#undef main` → static helpers → `cj_test_body()`
  inside `main`'s setjmp guard.
- Failure protocol: `CHECK`/`CHECK_EQ`(integers & doubles via `snprintf`)/
  `CHECK_STR_EQ`/`CHECK_CONTAINS`/`CHECK_NULL`/`CHECK_NOT_NULL`/`CHECK_NEAR`
  set a message and `longjmp` to the guard → stderr line (educational hint
  channel, same as Python/C++) → exit 1. **No exceptions in C.**
- `cj_capture(fn)` redirects fd 1 through a pipe+dup2 and returns what the
  learner's `printf`s wrote (the graded entry convention `void program()`).
- Solution syntax-gate first (`gcc -std=c23 -fsyntax-only`) so compile errors
  surface as verdict "error", not N confusing test failures.
- Author-side limits inside snippets: helpers are `static` free functions at
  file scope of the test TU (legal in C, unlike C++'s main-scope restriction).

## 6. Curriculum sources consulted (for design grounding, not copying)

- ISO/IEC 9899:2024 (C23) status + GCC 14 support pages — baseline selection.
- cppreference C pages (operators, conversion, string/memory headers,
  stdio semantics) — API truth for every graded snippet.
- GNU/GCC docs (options, warnings) — flags quoted in the build module.
- Exercism C track shape (84 exercises, concept-driven) — practice-density
  benchmark; original content throughout.
- OpenSSF Compiler Options Hardening Guide — warnings-as-evidence framing for
  the debugging module (adapted to "no sanitizers here" reality).
- Knuth/K&R-era idioms avoided in favor of modern C23 style
  (`int main(void)`, declarations near use, no implicit int).

## 7. Scope boundaries (deliberate exclusions → later courses)

- **Intermediate (future):** function pointers/callbacks, multi-file linking
  internals, storage-duration formalism (static/extern deep), bitfields,
  unions deep-dives, varargs, advanced preprocessor (X-macros), POSIX I/O,
  make/CMake for real, concurrency threads (C11 `<threads.h>`).
- **Advanced (future):** ABI/linking, custom allocators, aliasing/`restrict`,
  atomics/memory model, embedded/FREESTANDING, OS interfaces, security
  engineering.
- Beginner's module 20 (data structures) builds array-backed stack/queue +
  singly linked list from scratch — implementation-level, but complexity
  treated informally (counting steps, not formal Big-O proofs).

## 8. Verification protocol for this build

- Two-sided challenge harness with byte-identical sandbox files; every wrong
  solution must deterministically fail (no "accidentally correct" wrongs).
- C17 spot-compatibility on a sample per batch.
- EN/VI structure sync + VI sidecar completeness via validate-content.ts.
- Full gates: typecheck, lint, unit, E2E critical path, repo-wide build.
