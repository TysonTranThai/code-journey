# Curriculum Research — C — Advanced

Date: 2026-09-15 · Author: Buffy (autonomous phase 23)
Status: COMPLETE

## 1. What this course is

C — Advanced takes a learner who can build structured C applications (the
Beginner + Intermediate path) to the level where they can **reason about C the
way compiler and runtime engineers do**: object representation, the abstract
machine and its undefined behaviors, allocators, ABI and linking, systems
programming against real OS interfaces, concurrency with a memory model,
performance measurement, security engineering, and portability discipline.

It is NOT "Intermediate with harder exercises." Intermediate (cint-*, 16
modules, shipped in parallel by another agent) already covers: linkage and
translation units, pointer arithmetic and const-correctness, ownership
contracts, opaque handles, function pointers and dispatch tables, generic
containers via void* and _Generic, macro basics and X-macros, linked
lists/hash-table/BST/heap basics, robust file reading, layered error handling
and goto-cleanup, threads/mutexes/condition variables basics, and a UB catalog
introduction.

C Advanced therefore starts **where Intermediate's catalog ends**: from
"C the language" into "C the compiled artifact running on real hardware and an
OS", and treats Intermediate's topics as assumed vocabulary.

## 2. Environment (probed in the real sandbox image, 2026-09-15)

Every claim below was verified by compiling and running code inside
`codejourney-sandbox:latest` (Alpine, musl):

| Capability | Result | Course consequence |
| --- | --- | --- |
| gcc | **14.2.0** (`Alpine 14.2.0`), `-std=c23` accepted | C23 is the course baseline (same as Beginner/Intermediate) |
| POSIX symbols under `-std=c23` | **hidden** unless `_POSIX_C_SOURCE` defined; defining it in solution.c before includes works even though the test harness includes headers first (musl re-guards declarations at each include point — probed with a harness-simulation TU) | Every systems-module challenge boilerplate opens with `#define _POSIX_C_SOURCE 200809L` + its include set (encoded in `ca.py` preludes) |
| pthreads | work with **no `-pthread` flag** (musl: pthreads in libc); 4 threads × 10k atomic increments → 40000 | Concurrency modules are executable |
| `<stdatomic.h>` | works; atomics + thread pool verified | Memory-model module is executable |
| `threads.h` (C11 threads) | works (`thrd_create/join` → 42) | Standard-vs-POSIX comparison is executable |
| fork/waitpid/pipe/exec | verified (child "hi" over pipe; `execlp` exit 3) | Process module + mini-shell are executable |
| loopback TCP | **works even with `--network none`** (bind/listen/connect on 127.0.0.1) | Sockets module is executable; WAN/network claims avoided |
| mmap (MAP_ANONYMOUS) | works | mmap lesson executable |
| popen/system | work | Modules that drive **binutils from tests** are executable |
| binutils | nm, objdump, readelf, ar, ranlib, strip, ldd present | ELF/linking modules use real tool output via `system()` |
| make / cmake | **absent** | Build-engineering module teaches concepts + portable-sh exercises; NO Makefile claims in graded challenges |
| gdb / valgrind | **absent** | Debugging module uses compiler forensics + instrumented reasoning; no GDB claims |
| Sanitizers (ASan/UBSan) | **link fails** (Alpine splits them; musl) | NO sanitizer execution in graded challenges; they are taught conceptually with honest framing |
| clock_gettime | needs feature macro (see above); works with it | Timing/benchmarking lessons executable |
| memset_explicit | macro absent in this musl/gcc combo | Use `memset` + volatile sink idiom; noted honestly |
| Host arch | **aarch64** (`uname -m`) | Assembly module reads compiler output property-based (no exact mnemonics), arch-guarded examples |
| Limits | 64 MB alloc ok; `nproc`=10; uid 100 (non-root) | Concurrency/allocator sizes sized accordingly |

Sandbox job budgets for `c` (shared route): 20 s, 512 MB — fine for all
designed challenges (verified heaviest: 4-thread pool + loops compile+run).

## 3. Sources consulted

- GCC C standards support (gcc.gnu.org/projects/c-status.html): GCC 15 makes
  C23 default; GCC 14 honors `-std=c23` — matches our probed 14.2.0 behavior.
- cppreference C pages (declarations/linkage/storage duration/object
  representation/effective type, atomics memory ordering, threading support)
  for semantics vocabulary.
- POSIX.1-2017 (IEEE Std 1003.1) man-page structure for processes/signals/
  sockets chapters (features taught are the portable POSIX subset; Linux-only
  behaviors are labeled as Linux-specific and avoided in graded code).
- musl libc feature-test behavior (`features.h`) — explains the probed
  `_POSIX_C_SOURCE` gating.
- CSA/auditing practice for the security module (buffer overflows, format
  strings, TOCTOU, integer overflow) framed strictly as **prevention and
  detection**; no exploit-development content, per platform policy.
- Prior platform art: cb.py/cppa.py authoring systems, c-runtime.ts harness
  (setjmp/longjmp, dup2 capture), verify-challenges-c.mjs two-sided harness —
  all reused, not reinvented.

Original Code Journey material: every lesson, challenge, hint, and solution is
written fresh for this course; external sources informed scope and accuracy,
not text.

## 4. Curriculum design (24 modules)

Design rules:

1. Beyond Intermediate: every module touches what Intermediate only names.
2. Practice-first: each lesson → challenges; each module → checkpoint.
3. Honest environment labeling: ISO C vs POSIX vs Linux vs GCC-specific is
   explicit in lesson text and challenge prompts.
4. Deliberate-practice `level` stamped on practice-set challenges (sibling
   courses' convention); checkpoint challenges omit it.
5. Id namespace `ca*`/`caN-*`/`ca-pN*` (course-unique; global sweep checked).

Modules (id — focus):

1. `ca-object-model` — object representation, effective type, alignment/
   padding, integer representations, TBAA concepts, predict-the-layout drills
2. `ca-abstract-machine` — sequencing, side effects, observable behavior,
   lvalue/value semantics, why reasonable code can be invalid
3. `ca-pointer-semantics` — provenance, one-past-the-end, restrict, aliasing
   contracts, pointer-to-pointer, opaque handles at depth
4. `ca-ub-optimization` — UB classes the optimizer exploits (signed overflow,
   OOB, invalid shifts, uninit reads, strict aliasing, data races) with
   deterministic diagnosis exercises
5. `ca-allocators` — malloc internals concepts, alignment, fragmentation,
   arena/pool/free-list engineering → **Project: custom fixed-pool allocator**
6. `ca-ownership-patterns` — region/pool lifetime, error-safe cleanup,
   RAII-like guard patterns in C, ownership contracts at API level
7. `ca-advanced-ds` — open-addressing hash table, trie, union-find, LRU cache,
   adjacency-list graph — complexity + memory layout focus
8. `ca-generic-techniques` — void* + metadata descriptors, callback tables,
   macro + _Generic hybrids, type-safety seams, limits vs templates (honest)
9. `ca-meta-macros` — token pasting, stringification, variadic macros,
   feature detection, _Static_assert, when NOT to macro
10. `ca-compilation-pipeline` — -E/-S/-c stages, preprocessed output reading,
    symbols, ar archives — executable via system()-driven gcc/ar probes
11. `ca-elf-linking` — nm/readelf sections/symbols, static archive linking,
    dynamic-linking concepts, symbol resolution/visibility (tool-verified)
12. `ca-abi` — calling conventions (arch-aware), struct layout/alignment vs
    ABI, binary compatibility, extern "C"-style boundary thinking (C: name
    mangling absence)
13. `ca-assembly-reading` — read compiler -S output, map C constructs to
    machine operations, arch-guarded (aarch64 + x86-64), property assertions
14. `ca-build-engineering` — build graphs, incremental concepts, flags/
    warning hygiene, debug vs release, reproducibility (no make/cmake claims;
    portable-sh verified where executable)
15. `ca-debugging-forensics` — warnings-driven triage, invariant logging,
    core-concept forensics without gdb: bisecting UB, printf-instrumented
    state dumps, deterministic failure reproduction
16. `ca-sanitizers-concepts` — what ASan/UBSan/TSan detect, redzones,
    shadow memory concepts, how to read their reports (conceptual — verified
    unavailable in sandbox), plus deterministic in-code detection drills
17. `ca-posix-processes` — fork/exec/wait, pipes, signals (Portability:
    POSIX-labeled), environment, exit statuses → **Project: mini shell core**
18. `ca-concurrency-deep` — thread pools, read/write locks, barriers,
    races/deadlocks diagnosis, C11 threads vs pthreads (both verified)
19. `ca-memory-model` — stdatomic, seq_cst/acquire/release/relaxed, CAS,
    ABA, false sharing — carefully scoped exercises
20. `ca-sockets` — loopback TCP client/server, UDP datagrams, binary protocol
    framing, timeouts/non-blocking concepts (network=none-safe loopback)
21. `ca-performance-io` — buffered vs raw I/O, writev, mmap I/O, measurement
    with clock_gettime, throughput vs latency framing (measure, don't fabricate)
22. `ca-performance-tuning` — cache locality, data-oriented layout,
    allocation/system-call overhead, -O0/-O2 concepts, benchmark honesty
23. `ca-security` — overflow/format-string/TOCTOU/UAF detection & prevention,
    hardening flags concepts, safe parsing discipline
24. `ca-portability-capstone` — implementation-defined/endian/width
    discipline, feature detection, portability layers → **Final capstone:
    modular systems utility service** (allocator + DS + file persistence +
    concurrency + tests), milestones across the module's lessons

Challenge counts (practice + checkpoint) are engineered to land ~190–210
total, all two-sided verified.

## 5. Localization

EN + VI per the platform's overlay system: every module, lesson, practice set,
and challenge carries a `.vi.json`/`.vi.mdx` overlay; VI is written as real
teaching prose (same discipline as the Beginner phase), not machine word
swaps. Course title: "C — Nâng cao".

## 6. Verification plan (per platform convention)

- Per-batch two-sided smoke (R passes all tests, W fails ≥1) inside the real
  sandbox image via the batched single-container design proven in Beginner.
- Formal harness `verify-challenges-ca.mjs` → target 100%.
- `validate-content.ts` exit 0 (all courses × 2 locales).
- typecheck / lint / unit / E2E critical path / repo build.
- Global id sweep across ALL tracks (single namespace, all id kinds).
