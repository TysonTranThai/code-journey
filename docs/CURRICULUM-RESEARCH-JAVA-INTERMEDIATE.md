# Curriculum Research — Java — Intermediate

Date: 2026-09-14 · Authoring agent: Java — Intermediate (Phase 19)

## What was actually inspected (this repo, before any design)

| Artifact | What it establishes for Intermediate |
|---|---|
| `src/content/tracks/java/courses/java-beginner/` (14 modules, 62 lessons) | The prerequisite boundary: syntax, control flow, methods, arrays/strings, classes/objects, OOP design (interfaces, composition, inheritance tradeoffs), records/enums, collections + basic generics, exceptions + files, streams/Optional, testing + Maven, HTTP client, capstone |
| `src/workers/java-runtime.ts` | Sandbox Java execution contract: `javac --release 21`, unnamed-package `Solution` class, one JVM per test, `CjTestBase` helpers (`checkEq`, `checkTrue`, `checkContains`, `checkLines`, `checkNear`, `checkThrows`, `capture`), 30s job cap |
| `scripts/content-authoring/javb.py` | The authoring-library contract to clone (declarative module writers, per-course solution ledger, two-sided QA) |
| `scripts/content-authoring/verify-challenges-java.mjs` | Two-sided harness: reference passes, intentionally-wrong fails; mirrors sandbox compilation exactly |
| `docs/COURSE-JAVA-BEGINNER.md` | Beginner's verified final state (45 challenges, 14 practice sets) |

## What Beginner actually covers (verified from course.json + module dirs)

1. java-first-programs — JVM model, compilation, main, packages basics
2. java-types-operators — primitives, String, casting, final
3. java-conditions — if/switch, modern switch
4. java-loops — for/while/do-while, break/continue
5. java-methods — parameters, returns, overloading
6. java-arrays-strings — arrays, String methods, StringBuilder
7. java-classes-objects — fields, constructors, encapsulation, static
8. java-oop-design — interfaces, abstract classes, composition over inheritance, polymorphism
9. java-data-modeling — enums, records, equals/hashCode/toString, immutability basics
10. java-collections-generics — ArrayList/HashMap/HashSet, generic types, basic type parameters
11. java-exceptions-files — try/catch/finally, checked/unchecked, custom exceptions, Path/Files
12. java-streams-optional — lambdas, method references, stream pipeline, Optional
13. java-testing-debug — JUnit shape, assertions, debugging method
14. java-files-capstone — file persistence, capstone ledger application

## Prerequisite gap analysis (Beginner → Intermediate)

Beginner already touches most Module-1 topics of the original proposal (equality,
immutability via records). Gaps that Intermediate must own:

- **equals/hashCode contracts beyond records** (hand-written classes, hashing pitfalls)
- **Wildcards/bounded types/PECS** — Beginner only has fixed type parameters
- **Comparator/Comparable, sorted collections, deque/queue** — Beginner covers the big three collections only
- **Collectors (groupingBy/partitioningBy/teeing)** — Beginner streams stop at map/filter/collect(toList)
- **try-with-resources** — Beginner teaches try/catch/finally but not AutoCloseable resource management
- **JUnit parameterized tests, test doubles, AAA discipline** — Beginner testing is assertion basics
- **ExecutorService/Futures/CompletableFuture** — not touched at all
- **JDBC/SQL** — not touched
- **Maven dependency/scope/lifecycle depth** — Beginner only scaffolds a pom

## External research (sources actually consulted, 2026-09-14)

- **PECS / wildcards**: Oracle Java Tutorials (Wildcard Use, Generics Inheritance);
  Baeldung "Java Generics PECS" (2024); Stack Overflow canonical PECS answer.
  Decision: teach `? extends` / `? super` via producer/consumer method signatures
  (copy/filter patterns), explicitly NO capture-helper tricks at this level.
- **ExecutorService vs CompletableFuture**: Oracle Java Tutorials "Executors"
  trail; java.util.concurrent ExecutorService javadoc; concurrencydeepdives.com
  CompletableFuture guide (2024). Decision: ExecutorService first (mental model:
  task → Future), then CompletableFuture as composition layer; structured
  concurrency and virtual threads are noted as Advanced topics.
- **JDBC**: Oracle "High-Performance Oracle JDBC" (pooling rationale); Ask TOM
  bind-variable guidance; jOOQ blog on resource leaks. Decision: teach
  try-with-resources + PreparedStatement + manual commit/rollback transactions;
  connection pooling explained conceptually, not wired (no external pool deps in
  sandbox); H2-style in-memory concepts taught via the repository pattern with a
  fake in-memory store, honest that real DB drivers cannot run in the challenge
  sandbox (documented infrastructure limitation, not faked).
- **JUnit 5/6 parameterized tests**: docs.junit.org (6.1.3 current); Baeldung
  parameterized-tests guide (2026). Decision: teach AAA + @Nested + parameterized
  concepts conceptually in sandbox lessons; graded challenges use the platform's
  CjTestBase harness (honest about the difference).
- **SOLID + composition**: covered in Beginner's OOP-design module at intro
  level; Intermediate deepens via dependency inversion + testable design, not by
  repeating definitions.

## Course design decisions (original content, informed by sources)

1. **15 modules, consolidated from the 21-module proposal** — same consolidation
   rationale as the Beginner course (Maven folded into build/release module,
   Git into professional practice, security folded into exception/data modules,
   algorithms into a dedicated module). Documented here, not silently.
2. **`javi-` challenge-id prefix, `javi` authoring prefix** — the loaders enforce
   global id uniqueness across tracks (verified during the Beginner build: 9
   collisions required renaming). Prefixing by construction avoids colliding with
   `javb-*`, cpp/python/web tracks, and the concurrently-running C++ Advanced
   agent's content.
3. **Separate solution ledger** (`javi-intermediate-solutions.mjs`) — Beginner's
   ledger is never appended to by this course.
4. **Sandbox-honest design** — no network in challenges (HTTP module teaches
   client construction against injectable transport interfaces); no real JDBC
   (persistence module teaches repository pattern + in-memory stores + SQL
   reasoning in lessons); no external Maven execution (build module teaches
   pom/lifecycle reasoning + structure by inspection). Every graded challenge is
   a pure-Java deterministic test under the existing java-runtime contract.
5. **Practice-first**: every module = lessons + one practice set + a graded
   checkpoint challenge (the platform's established shape).
6. **`--release 21` baseline** — matches both host JDK 25 and sandbox openjdk21;
   text blocks, records, sealed interfaces, pattern matching for switch are all
   available and fair game at Intermediate level.

## Module plan (15 modules)

1. java-equality-immutability — identity vs equality, contracts, defensive copies, final
2. java-oop-solid — dependency inversion, composition design, sealed hierarchies
3. java-generics-deep — bounds, wildcards, PECS, erasure
4. java-collections-advanced — Comparable/Comparator, deque/queue, immutable collections
5. java-functional-deep — Collectors (grouping/partitioning/teeing), composition
6. java-exception-architecture — try-with-resources, exception boundaries, custom hierarchies
7. java-io-formats — NIO.2 depth, CSV/JSON (hand-rolled, no deps), encoding
8. java-testing-deep — AAA, parameterized concepts, test doubles, regression discipline
9. java-build-release — Maven lifecycle/scope/dependency reasoning, structure by inspection
10. java-concurrency — Thread/Runnable, executors, Futures, race conditions, Atomic* basics
11. java-async-http — CompletableFuture composition, HTTP Client behind injectable transport
12. java-persistence — repository pattern, in-memory stores, SQL/JDBC concepts in lessons
13. java-architecture — layering, DTO vs domain, dependency injection by hand, package design
14. java-algorithms-inter — Big-O reasoning, two pointers, sliding window, prefix sums, maps
15. java-inter-capstone — layered expense-tracker backend capstone (records, generics, streams, repos, tests)
