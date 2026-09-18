# Course: Java — Intermediate (java-intermediate)

Date: 2026-09-14 · Status: **COMPLETE** (all content two-sided verified)

## Position

Track `java`, course 2. Path: **java-beginner (complete) → java-intermediate
(this course) → java-advanced (future)**. Prerequisite: Java — Beginner —
the course opens from the Beginner exit point (collections, lambdas/streams
intro, exceptions, files, JUnit basics, Maven basics) and moves the learner
from "I can write Java programs" to "I can design, test, debug, structure,
and ship maintainable Java applications."

Vietnamese: **Java — Trung cấp** (`course.vi.json` + per-node `.vi.json` /
`.vi.mdx` overlays, all validator-verified in sync).

## Verified shape (from disk)

| Metric | Value |
|---|---|
| Modules | **15** |
| Lessons | **58** (43 teaching + 15 checkpoint lessons) |
| Practice sets | **15** (one per module) |
| Challenges | **60** (45 practice + 15 checkpoint) — unique IDs, all `javi-` namespaced |
| Estimated time | **~23.4 h** (806 min lessons + 600 min practice) |
| EN/VI parity | 58/58 lesson MDX both locales, 60/60 challenge VI sidecars, module/course overlays |
| Solution ledger | `scripts/content-authoring/javi-intermediate-solutions.mjs` — exactly **60 R + 60 W** pairs (deduped) |

## Modules

1. `java-equality-immutability` — identity vs equality, equals/hashCode contract, defensive copying, immutability by construction (mutable-key trap checkpoint)
2. `java-oop-solid` — programming to contracts, sealed hierarchies + pattern matching, dependency inversion by hand (constructor injection), composition over inheritance
3. `java-generics-deep` — bounded type parameters, wildcards, PECS, type erasure
4. `java-collections-advanced` — Comparator chains, deques, immutable views, structure choice by complexity
5. `java-functional-deep` — Collectors (grouping/partitioning), functional composition, when streams lose to loops
6. `java-exception-architecture` — try-with-resources semantics (return-once idiom), exception boundaries, custom hierarchies, fail-fast validation
7. `java-io-formats` — NIO.2 concepts, hand-rolled CSV/JSON parsing with honest escaping rules
8. `java-testing-deep` — AAA, test doubles by hand, regression discipline, deterministic-time design (injectable clocks)
9. `java-concurrency` — executors, Futures, race conditions, atomic visibility, merge-vs-put collection races
10. `java-async-http` — CompletableFuture composition, injectable HTTP transport, error propagation
11. `java-persistence` — repository pattern, the JDBC shape it wraps (placeholders, transactions, exception translation), index maintenance
12. `java-architecture` — layered architecture, hand-rolled DI, refactoring a monolith
13. `java-algorithms-inter` — frequency maps, prefix sums, binary search, two pointers
14. `java-clean-code` — naming, guard clauses, code smells, refactoring discipline
15. `java-inter-capstone` — layered Expense Tracker: self-validating records, repository + service layers, reporting streams, money-safe arithmetic

## Toolchain (inherited from Phase 18, unmodified)

- Sandbox: `src/workers/java-runtime.ts` — one JVM per test, marker protocol,
  `--release 21` on host (JDK 25) and sandbox (openjdk21-jdk); no new
  infrastructure was added for this course.
- Authoring: `scripts/content-authoring/javi.py` (cloned from `javb.py`,
  course path + `javi-` prefix + separate ledger), modules `javi_m1..m15.py`,
  wiring `javi_wire.py` (surgical: appends course to `track.json`, validator
  entry; never rewrites Beginner's files).
- Harness: `scripts/content-authoring/verify-challenges-javi.mjs` —
  **60/60 two-sided OK** (every reference passes every test; every
  intentionally-wrong solution fails at least one).

## Notable content decisions

- **Honest sandbox boundaries taught in-lesson**: file I/O and JDBC are
  taught via injectable in-memory equivalents (string-content grading,
  `AutoCloseable` with in-memory closeables) rather than faking disk/network
  access; the MDX says exactly what is simulated and why.
- **Every "wrong" solution is a behavioral near-miss** (compile-clean,
  passes some tests) — the convergence trap (a W identical to R on all tests)
  was caught and fixed for several challenges during the build.
- **Real Java semantics surfaced by the harness**: `return`-inside-try
  escaping `finally` appends, `Objects.equals` on arrays comparing identity,
  `List.copyOf` defensive-copy semantics, map merge-vs-put races.

## QA (actual results, this session)

| Gate | Result |
|---|---|
| `validate-content.ts` | exit 0 — 15 modules, 58 lessons, `SYNC: EN/VI structures match`, 164 nodes clean per locale; java linear path 120 lessons |
| Two-sided harness | **60/60 OK** |
| mdx-map regen | 1266 lesson imports |
| Typecheck / lint | clean / clean |
| Unit + integration | **150/150** (the `curriculum-vi-content` suite is blocked by the C++ Advanced agent's untracked MDX — see below) |
| Production build | exit 0 via `next build` (only after excluding the same external file from the generated map; canonical map restored) |
| E2E (Playwright vs my own prod server on :3456) | **36/36** |
| `git diff --check` | clean |

## Multi-agent safety

- Java Beginner files untouched (verified via `git status` scope checks);
  all shared-file edits additive and surgical.
- ID collisions with other courses found by a global sweep and fixed by
  renaming **my** nodes only: `java-checkpoint-*` → `javi-checkpoint-*`
  (Beginner owns the generic prefix), `repository-pattern` →
  `javi-repository-pattern`, `capstone-brief` → `javi-capstone-brief`
  (python-intermediate owns those names).
- Known external issue (NOT mine, not fixed): the C++ Advanced agent's
  untracked `events-and-config{,.vi}.mdx` contain unescaped `{...}` in MDX
  prose, which breaks the `curriculum-vi-content` test suite and `pnpm build`
  until fixed. Left untouched per the parallel-work rule.
