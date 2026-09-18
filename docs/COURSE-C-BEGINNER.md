# Course Spec — C — Beginner (`c-beginner`, "C — Cơ bản")

Date: 2026-09-14. Status: implementing (Phase 21). Research:
`docs/CURRICULUM-RESEARCH-C-BEGINNER.md`.

## Positioning

Track `c` — new, first course. Path: **C — Beginner → C Intermediate →
C Advanced** (future). Goal: "I have never programmed in C" → "I can write,
debug, test, compile, organize, and build small C programs", with a memory-first
mental model (pointers, ownership, lifetimes) that later feeds systems
programming and C++.

- **Standard baseline: C23** (GCC 14.2.0 in the sandbox, verified); graded code
  is C17-compatible; C23-only features appear in prose only, flagged as such.
- **Practice-first:** every lesson carries practice; LEARN/DEEP-DIVE separation
  via practice sets anchored `afterLesson` (platform pattern).
- **Memory truth early:** null terminator, `sizeof`, stack vs heap, ownership.
- **No fabricated support:** no sanitizers (missing in image — verified), no
  debugger grading, no threads, no networking.

## Module plan (22 modules)

| # | dir | Title | Core content | Grading notes |
|---|-----|-------|--------------|---------------|
| 1 | `first-programs` | What Is C? | compiled pipeline, main, printf, comments | output capture of `program()` |
| 2 | `variables-types` | Variables & Types | int/char/float/double, signedness, constants, sizeof | value + sizeof predictions (sizeof via `unsigned long` prints) |
| 3 | `io-formatting` | Input & Output | format specifiers, width/precision, scanf-gradeable via snprintf/sscanf on strings, reading mistakes | parse/format round-trips (no interactive stdin in sandbox) |
| 4 | `operators-expressions` | Operators & Expressions | arithmetic, comparison, logical, precedence, integer division, casts | value predictions, mixed-type division |
| 5 | `conditionals` | Conditional Logic | if/else if/else, switch/case/default/break | decision functions |
| 6 | `loops` | Loops | for/while/do-while, nested, break/continue | patterns, accumulation, table generation |
| 7 | `functions` | Functions | prototypes, params, returns, decomposition | refactor-into-functions drills |
| 8 | `scope-lifetime` | Scope, Lifetime & Storage | local/global/block, static, extern concept, globals hazard | observable value/lifetime behavior |
| 9 | `arrays` | Arrays | declare/init/index/iterate, 2-D, bounds discipline | statistics, search, counting, out-of-bounds recognition |
| 10 | `strings-chars` | Strings & Characters | char literals, C strings, null terminator, strlen/strcmp/strncpy+snprintf, buffer discipline | implement mini string functions; termination bugs |
| 11 | `pointers-fundamentals` | Pointers Fundamentals | addresses, &/*, pointer types, NULL, modify-through-pointer | swap, value surgery, address-printing (%p), NULL checks |
| 12 | `pointers-arrays` | Pointers & Arrays | duality, pointer arithmetic, array params decay, strings via pointers | reverse, sum-by-walker, custom strlen/strcmp |
| 13 | `dynamic-memory` | Dynamic Memory | malloc/calloc/realloc/free, ownership, leaks, dangling, double-free, NULL checks | dynamic arrays/grow-by-realloc with strict free audits |
| 14 | `structs` | Structs | members, init, nesting, arrays of structs, -> vs . | student-record operations |
| 15 | `enums-typedef` | Enums, Typedef & Modeling | enum, typedef, state modeling | state machines, inventory model |
| 16 | `file-io` | File I/O | fopen/fclose/fprintf/fgets/append/EOF/error checks | write→read-back round-trips on /tmp files |
| 17 | `preprocessor-headers` | Preprocessor & Headers | #include, guards, #define, conditional compilation | macro-behavior predictions; guard discipline |
| 18 | `multi-file-projects` | Multi-File Projects | .h/.c split, linking model, static functions, API boundaries | single-TU graded core (header content + usage), prose for real linking |
| 19 | `debugging-c` | Debugging C | warnings as evidence, error reading, segfault classes, forensics | find-and-fix batteries graded on the FIXED behavior (warnings verified via -Werror readouts) |
| 20 | `data-structures` | Data Structures Foundations | dynamic array, stack, queue, singly linked list | implement from scratch; exact-value + invariant audits |
| 21 | `algorithms` | Algorithms & Problem Solving | linear/binary search, selection/insertion sort, recursion basics | edge-case-complete implementations |
| 22 | `capstone-finance` | Capstone — Personal Finance Manager | integrate structs, dynamic memory, files, modules | acceptance battery: add/remove/report/persist round-trip |

Mini-projects (graded challenge sets inside modules): Calculator (M4–5),
Number Guessing logic (M6), Grade Analyzer (M9), Contact Manager (M14+M16),
Inventory Manager (M15), Notes App (M16), Dynamic Array Library (M13/M20),
Linked List (M20). Final: Personal Finance Manager (M22).

## Grading honesty notes

- Sandbox is non-interactive: `scanf`-based interactivity is taught with
  grading through `sscanf` on provided buffers and functions; "reading user
  input" is graded as parse correctness, not live stdin.
- File I/O challenges operate on files under `/tmp` (writable in-sandbox);
  no `/job` writes (noexec tmpfs conventions).
- No sanitizer or debugger claims anywhere (probed: ASan not linkable).

## QA gates (planned)

Two-sided harness `verify-challenges-c.mjs` (byte-identical via `buildCTestFile`),
validate-content (2 locales), typecheck, lint, unit suite, E2E critical path,
repo-wide `pnpm build`, live preview spot-checks (EN + VI cookie).
