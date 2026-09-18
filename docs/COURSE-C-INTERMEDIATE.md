# Course Spec — C — Intermediate (`c-intermediate`, "C — Trung cấp")

Date: 2026-09-15. Status: complete (Phase 23). Research:
`docs/CURRICULUM-RESEARCH-C-INTERMEDIATE.md`.

## Positioning

Track `c`, second course. Path: **C Beginner → C Intermediate → C Advanced**
(future). Goal: "I can write basic C programs" → "I understand how C actually
works and can build structured, memory-safe, reusable programs."

- **Standard baseline: C23** (GCC 14.2.0 / musl in the sandbox, verified).
  Graded code is strict ISO C; POSIX/threads taught through C11 `threads.h`
  (probed working in-sandbox: `mtx_t`, `cnd_t`, `thrd_t`; no `-pthread` needed).
- **Memory is the spine:** every module revisits "who owns this memory, how
  long does it live, who frees it, what happens if allocation fails?".
- **No fabricated support:** no sanitizers (absent in image — verified), no
  Valgrind, no debugger grading, no networking, no multi-file TUs (single-TU
  grading; multi-file topics taught via observed compiler/linker output in
  prose and simulated-symbol challenges).
- **File I/O is gradeable** (sandbox `/tmp` writes verified) — used by the
  binary-files module and the capstone.

## Module plan (16 modules)

| # | dir | Title | Core content | Grading notes |
|---|-----|-------|--------------|---------------|
| 1 | `cint-translation-units` | Translation Units, Linkage & the Build | preprocessing→compile→link, static/extern, tentative definitions, ODR/linker errors | static visibility across "TUs", linker-output interpretation |
| 2 | `cint-pointers` | Pointers Deep Dive | arithmetic & one-past-the-end, the four const placements, pointer-to-pointer, arrays of pointers | span walking, const-swap table, out-params |
| 3 | `cint-ownership` | Ownership & the Heap | alloc failure paths, realloc growth, arena discipline, dangling/double-free as *contracts* (no sanitizers — behavioral discriminators only) | ownership transfer, balanced alloc/free paths, arena zeroing over pre-dirtied storage |
| 4 | `cint-function-pointers` | Function Pointers & Callbacks | syntax/typedefs, comparators, dispatch tables, closures-with-context | dispatch builders, context callbacks, stable sorted partition |
| 5 | `cint-structs` | Structs & Data Modeling | padding/offsets, nested/self-referential, opaque types, encapsulation | offsetof/sizeof predictions, graph free-order, opaque counters |
| 6 | `cint-strings` | Strings & Buffers | buffer vs string, bounded copies, dynamic strbuf, span tokenization, binary-vs-text | exact-fit truncation semantics, span split with trailing separators |
| 7 | `cint-linked` | Linked Data Structures | slist/dlist/circular, stacks/queues/deques, ring consistency | structural ring checks, splice/rotate, ownership cleanup |
| 8 | `cint-hash` | Hash Tables | open addressing (linear probing), separate chaining, tombstones, load factor | probe walks, borrowed-key lifetime traps, rehash |
| 9 | `cint-generic` | Generic Programming | `void *` math, `qsort`/`bsearch`, `_Generic` facades, type-safe macro wrappers | generic sort/dedup, typed facades, cross-type dispatch rejection |
| 10 | `cint-preproc` | Preprocessor Mastery | evaluation hazards, hygiene, token pasting, X-macros, `_Static_assert` | single-source enum/dispatch/lookup generation |
| 11 | `cint-trees` | Trees & Heaps | BST invariants, traversals, binary heap, heapsort, streaming top-k | invariant verification, heap eviction order, heapsort |
| 12 | `cint-files` | Binary Files & Robust Parsing | `fwrite`/`fread`, endianness, magic + checksum records, CSV parsing | byte-exact round-trips, corrupt-input rejection |
| 13 | `cint-errors` | Error Handling & Robust APIs | return codes, errno, cleanup-goto, two-phase init, error propagation | full-table overflow, three-valued logic, layered cleanup |
| 14 | `cint-ub` | Undefined Behavior | OOB, signed overflow, shifts, invalid pointers, unsequenced ops — *why* the optimizer may assume | bounded/saturating alternatives that provably avoid UB |
| 15 | `cint-threads` | C11 Threads | `thrd_t`/`mtx_t`/`cnd_t`, bounded queue, race visibility, producer/consumer | latch-choreographed multi-threaded tests in-sandbox |
| 16 | `cint-capstone` | MiniKV Capstone | persistent key-value store: arena core, owned keys, binary log with magic+checksum, iterator, tests | full-stack integration: core + persistence + iteration + corruption handling |

Every module: 3 teaching lessons + 1 checkpoint lesson (challenge-attached),
2 practice sets (`afterLesson` anchored). 84 challenges total
(68 practice + 16 checkpoint), each with EN + VI sidecars, a reference
solution, and an intentionally-wrong near-miss solution.

## Verification (all numbers machine-produced)

- **Two-sided harness** (`scripts/content-authoring/verify-challenges-cint.mjs`,
  real sandbox image): reference solutions pass **102/102** tests; wrong
  solutions fail ≥1 test for **84/84** challenges ("wrongly-pass: 0").
- **Curriculum validator** (`validate-content.ts`): schema-valid; EN/VI
  structures match; 229 nodes load clean per locale; unique ids across all
  kinds/courses; c linear path = 148 lessons.
- **QA gates:** typecheck PASS · lint PASS · unit tests 160/160 ·
  production build PASS · E2E 36/36 (incl. 390px mobile + keyboard flows).
- **Beginner regression:** C Beginner two-sided harness **158/158 OK** after
  all shared-infra touches.

## Conventions

- Id namespace: `cint-` prefix on lessons, practice sets, challenges,
  checkpoints (`cint-pN-*`, `cint-checkpoint-mN-task`).
- Authoring pipeline: `scripts/content-authoring/cint.py` (shared helpers) +
  `cint_m1..16.py` (modules) + `cint_course.py` (manifest) →
  `src/content/tracks/c/courses/c-intermediate/`.
- R/W ledger: `scripts/content-authoring/cint-solutions.mjs` (append-only,
  last-write-wins per id).

## Known limitations

- No ASan/Valgrind in the image: leak/UAF teaching uses deterministic
  behavioral discriminators (pointer identity, pre-dirtied buffers), never
  sanitizer output.
- Sandbox grades single TUs: multi-file linking is observed, not practiced.
- Threads are C11-standard only; no POSIX-only APIs are graded.
