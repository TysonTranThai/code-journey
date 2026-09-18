# Course Spec — C — Advanced ("C — Nâng cao")

Track: `c` (third course) · Course id: `c-advanced` · Phase 23
Prerequisites: `c-beginner`, `c-intermediate` (both resolve; Intermediate is
shipped concurrently and loads clean in the validator)

## Promise

A learner finishing this course can read C the way tools see it (objects,
representations, ABI, symbols), reason about UB and optimization like a
compiler engineer, build and defend allocators and data structures, drive
POSIX processes/threads/sockets, measure performance instead of guessing, and
ship a modular systems utility with memory discipline and tests.

## Module map (24)

| # | id | Focus | Project/output |
|---|----|-------|----------------|
| 1 | ca-object-model | object repr, effective type, alignment, padding, integer reprs | layout predictor drills |
| 2 | ca-abstract-machine | sequencing, observable behavior, value semantics | UB prediction drills |
| 3 | ca-pointer-semantics | provenance, one-past-end, restrict, aliasing | aliasing contract API |
| 4 | ca-ub-optimization | optimizer-exploited UB classes | diagnosis clinic |
| 5 | ca-allocators | pool/arena/free-list engineering | **allocator project** |
| 6 | ca-ownership-patterns | regions, guards, error-safe cleanup | guard-macro library |
| 7 | ca-advanced-ds | open-addressing hash, trie, union-find, LRU, graph | ds library |
| 8 | ca-generic-techniques | void*+descriptors, callbacks, _Generic hybrids | generic container |
| 9 | ca-meta-macros | pasting, stringification, _Static_assert | assert library |
| 10 | ca-compilation-pipeline | -E/-S/-c, ar, symbols | tool-driver exercises |
| 11 | ca-elf-linking | nm/readelf, archives, dynamic linking | tool-verified ELF lab |
| 12 | ca-abi | calling conv (arch-aware), struct layout vs ABI | layout-vs-ABI lab |
| 13 | ca-assembly-reading | compiler output reading, arch-guarded | asm mapping lab |
| 14 | ca-build-engineering | graphs, flags, configs, reproducibility | build-audit exercise |
| 15 | ca-debugging-forensics | warnings triage, invariants, repro | forensics clinic |
| 16 | ca-sanitizers-concepts | ASan/UBSan/TSan concepts (honest: unavailable) | detection drills |
| 17 | ca-posix-processes | fork/exec/wait, pipes, signals | **mini-shell core** |
| 18 | ca-concurrency-deep | pools, rwlocks, barriers, deadlock clinic | thread pool |
| 19 | ca-memory-model | atomics, orderings, CAS/ABA, false sharing | spsc ring buffer |
| 20 | ca-sockets | loopback TCP/UDP, framing, timeouts | echo server/client |
| 21 | ca-performance-io | buffered vs raw, writev, mmap, measurement | file processor |
| 22 | ca-performance-tuning | cache locality, layout, overhead, -O levels | benchmark clinic |
| 23 | ca-security | overflow/format/TOCTOU/UAF detection+prevention | hardened parser |
| 24 | ca-portability-capstone | impl-defined, endianness, feature detection | **capstone: systems utility service** |

## Practice distribution (target ~200)

Per module: 2 practice sets (2–4 challenges each) + 1 checkpoint challenge.
Challenges emphasize: predict-then-verify (layout/UB), implement-and-test
(allocators/DS/concurrency), diagnose-and-fix (debugging/security), tool-drive
(pipeline/ELF via system() with gcc/ar/nm/readelf), measure-and-explain
(performance). Memory-sensitive challenges always exercise NULL/empty/
boundary/large/invalid paths per the platform's challenge-quality bar.

## Environment honesty rules (enforced in content)

- ISO C vs POSIX vs Linux vs GCC-specific labeled in every lesson that touches
  them; POSIX code always shows its feature macro.
- No sanitizer/gdb/make/cmake/valgrind claims in graded challenges (verified
  absent); sanitizer and build modules are conceptual with honest framing.
- Loopback networking only (verified with `--network none`); no external
  network claims.
- Assembly is arch-guarded (aarch64 host; x86-64 shown as comparison),
  property-asserted, never exact-mnemonic-dependent.
- No exploit-development content in security (prevention/detection only).

## QA plan

Same proven pipeline as C Beginner: `ca.py` + per-batch two-sided smokes in
the real image → formal `verify-challenges-ca.mjs` (R all-pass, W ≥1-fail,
byte-identical test files via `buildCTestFile`) → validate-content →
typecheck/lint/unit/E2E/build → global id sweep → cross-agent diff review.
