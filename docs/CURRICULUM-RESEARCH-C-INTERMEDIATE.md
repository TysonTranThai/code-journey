# Curriculum Research — C — Intermediate (Course: `c-intermediate`)

Date: 2026-09-14. Researched before authoring. Every environment claim below was
**verified by direct probe in the actual sandbox container**
(`codejourney-sandbox:latest`, GCC 14.2.0, the same image the challenge runner
uses) — nothing is assumed from documentation alone. Host-JDK-style "it works on
my machine" claims are explicitly avoided.

## 1. Platform reality (probed in-container, 2026-09-14)

| Probe | Result | Consequence for the course |
|---|---|---|
| C11 `<threads.h>`: `mtx_t` + `thrd_create/join` (2 threads × 10 000 increments, harness-shaped TU) | **PASS** | Graded concurrency is real. No `-pthread` needed on musl. |
| `cnd_t`, `_Thread_local` | initialized / OK | Condition variables and thread-local storage graded. |
| ISO C signals: `signal()` + `raise()` + `volatile sig_atomic_t` | OK | ISO C signaling graded; POSIX signal APIs prose-only. |
| `_Generic` selection expression | OK | Graded. |
| C23 `constexpr` objects | OK | Graded (C23 baseline). |
| Flexible array members | OK | Graded. |
| `qsort` with nested-function comparator (GNU extension compiled under C23) | OK | Function-pointer grading is real. |
| POSIX `open/read/write/close` on `/tmp` **with** `#define _POSIX_C_SOURCE 200809L` | OK under C23 and C17 | Prose teaching (see the strict-mode finding below). |
| `dirent.h` directory listing (with macro) | OK | Prose-only. |
| `fork` + `pipe` + `waitpid` (standalone binary) | OK | Prose-only — processes are outside the graded contract. |
| **Strict `-std=c23` without feature-test macro: `strtok_r`, `open`…** | **implicit-declaration errors** | POSIX-only symbols are HIDDEN in graded TUs. |
| ASan (`-fsanitize=address`) | FAILS to link (no libasan; matches Beginner research) | No sanitizer claims anywhere. |
| Sockets / network | network `none` (sandbox envelope) | No networking course claims; TCP prose only. |
| make / gdb / valgrind | not in image | Build systems + debugger taught as prose + concept checks. |

### The decisive strict-mode finding (drives the graded-code contract)

The sandbox harness (`c-runtime.ts`, shared with Beginner — **untouched by this
course**) includes `solution.c` AFTER its own `#include <unistd.h>` block, under
`-std=c23` with no feature-test macros. Under strict C23, glibc/musl headers
hide POSIX-only declarations unless `_POSIX_C_SOURCE` is defined *before the
first system include* — and the learner's solution is compiled after the
harness's. Therefore:

- **All graded solution code is ISO C** (`stdio.h` `fopen/fseek/fgets`,
  `strtok`, `signal.h`, `threads.h`, `_Generic`, C23 core).
- Defining `_POSIX_C_SOURCE` inside `solution.c` would be too late to matter
  and is **banned** in graded code.
- POSIX material (fds, `open/read/write`, `dirent`, `fork/exec/pipe`) is taught
  in **prose lessons** — clearly labeled "POSIX, not ISO C" — with concept
  checks, never graded execution. This is an honest boundary, not a dodge:
  it is the same discipline Beginner's research established.

## 2. Beginner boundary (inspected, protected, not assumed)

The C Beginner agent is authoring concurrently (their `cb_*.py` scripts were
being written during this phase). Their research doc commits to: memory truth
early (null terminator, sizeof, stack/heap, "who frees this?"), pointer
practice across modules 11–13, safe idioms by default, array-backed
stack/queue + singly linked list at informal complexity. Their **explicit
deferral list to Intermediate** (their §7) is this course's scope: function
pointers/callbacks, storage-duration formalism (`static`/`extern` deep),
unions/bitfields, varargs, advanced preprocessor (X-macros), POSIX I/O,
make/CMake, C11 `<threads.h>`.

Prerequisites this course assumes from Beginner (and only those): compile/run
workflow, printf/scanf families, control flow, functions, arrays, basic
pointers & pointer params, structs, malloc/free basics, basic file I/O,
multi-file compilation at the "it links" level, safe-idiom habits.

Track wiring: the `c` track had **no `track.json`** when this phase began
(Beginner had not yet wired theirs). This course created it referencing **only
`c-intermediate`** — `loadTrack` re-throws for referenced-but-missing courses,
so referencing `c-beginner` before their manifest exists would break
whole-curriculum discovery (learner-facing, per the 2026-09-13 incident noted
in the loaders). Beginner appends their reference when they wire theirs;
both scripts are read-modify-write and idempotent.

## 3. Course positioning

Beginner: "I can write basic C programs." → Intermediate: **"I understand how C
actually works and can build structured, memory-safe, reusable programs."**
Not Beginner-harder: the new spine is (a) the link/translation-unit model,
(b) ownership discipline in APIs, (c) function pointers as a design tool,
(d) data structures with correct teardown, (e) generic C without pretending it
has templates, (f) undefined behavior as contract reasoning, (g) concurrency
via the ISO C threads library, (h) a capstone that composes all of it.

Reserved for C Advanced (not taught here): custom allocators, `restrict`/
strict-aliasing depth, atomics & the C11 memory model beyond `mtx`/`cnd`,
embedded/freestanding, ABI details, lock-free structures.

## 4. Curriculum architecture (16 modules — consolidation rationale)

The 24-module proposal was consolidated to 16 with every proposed topic either
taught, explicitly deferred to Advanced, or honestly marked prose-only:

| # | Module | Includes (proposal mapping) |
|---|---|---|
| 1 | `cint-translation-units` | M1: translation units, preprocessing→assembly→link, static vs extern, headers, linker errors |
| 2 | `cint-pointers` | M2: pointer arithmetic, ptr-to-ptr, arrays of pointers, const correctness |
| 3 | `cint-ownership` | M3: allocation failure, realloc pattern, leaks/UAF/double-free by contract; sanitizer absence honest |
| 4 | `cint-function-pointers` | M4: callbacks, comparators, dispatch tables + mini-build |
| 5 | `cint-struct-design` | M6: nested/self-referential/opaque structs, encapsulation |
| 6 | `cint-strings-buffers` | M5: dynamic strings, tokenization, safe parsing, binary vs text |
| 7 | `cint-generic-c` | M9: `void *`, `_Generic`, type-safe wrappers + tradeoffs (no fake templates) |
| 8 | `cint-preprocessor` | M10: function-like macros, X-macros, `_Static_assert`, hygiene |
| 9 | `cint-linear-structures` | M7: lists/stacks/queues with full memory discipline + complexity |
| 10 | `cint-hash-tables` | M8: hash tables, collision handling, resizing + mini-build |
| 11 | `cint-trees-heaps` | M21: BSTs, heaps, priority queues, graphs (adjacency), traversals |
| 12 | `cint-files-binary` | M15: binary vs text I/O, random access, serialization + binary-database mini-build |
| 13 | `cint-errors-robust-apis` | M22: error codes, errno discipline, deterministic tests, defensive APIs (POSIX fds prose) |
| 14 | `cint-undefined-behavior` | M14: UB categories + why compilers may assume; debugging without sanitizers (M13 prose) |
| 15 | `cint-concurrency` | M19: C11 threads (graded!), races, mutexes, condition variables, deadlock patterns |
| 16 | `cint-capstone` | M24: Inventory Manager — dynamic inventory, linked orders, file persistence, callbacks, tests |

Dropped with cause: M11/M12 (headers deep + build systems → headers are M1;
make/CMake is prose-only in M1 — the sandbox has no make, and faking build
gradients would violate the honesty rule), M16/M17/M18 (POSIX processes/IPC/
networking → prose in M13 + explicit Advanced deferral; sandbox has no network),
M20 (algorithms → woven into modules 9–11 complexity work), M23 (secure C →
interleaved: bounds/format-string/UB discipline IS modules 6/14; deep security
engineering is Advanced).

Practice target: ~50 two-sided-verified challenges (43 practice + 16
checkpoints ≈ 59 total including checkpoints) — every one reference-passing
and wrong-solution-failing in the real container. Deliberate-practice `level`
stamping inherited from sibling courses.

## 5. Sources consulted (design grounding, not copying)

- ISO/IEC 9899:2024 (C23) + GCC 14 changes — baseline (shared with Beginner).
- cppreference C pages — `threads.h` semantics, `qsort`, string/memory headers,
  `_Generic`, static_assert, flexible array members.
- POSIX.1-2017 (open group) — prose-only sections labeled as POSIX.
- SEI CERT C Coding Standard — UB categories and API-design rules.
- OpenSSF Compiler Options Hardening Guide — warnings-as-evidence framing.
- Beginner's research doc (their probe table) — inherited sandbox facts,
  re-verified where this course leans on them (threads, files, strict mode).

## 6. Verification protocol for this build

- Two-sided harness (`verify-challenges-cint.mjs`): every challenge's reference
  solution passes its full battery AND its wrong solution fails it — run in
  the real container with byte-identical test files (the exported
  `buildCTestFile`), 20 s per-test timeout inside the 30 s envelope.
- C17 spot-compatibility on a sample (graded code stays C17-clean).
- EN/VI structural sync via validate-content.ts; global id-collision sweep
  across all tracks (the `cint-`/`cint`-prefix namespace is disjoint from
  Beginner's `cb`/`cb2`).
- Full gates: typecheck, lint, unit+integration, production build, E2E.
- Multi-agent safety: Beginner/Java/C++/Python/Web artifacts untouched;
  shared-file edits (track.json creation, validator line) minimal + idempotent.
