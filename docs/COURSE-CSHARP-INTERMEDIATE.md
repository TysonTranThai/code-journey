# Course Spec — C# — Intermediate (`csharp-intermediate`, "C# — Trung cấp")

Date: 2026-09-17. Status: complete (Phase 24). Research:
`docs/CURRICULUM-RESEARCH-CSHARP-INTERMEDIATE.md`.

## Positioning

Track `csharp`, second course. Path: **C# Beginner → C# Intermediate → C#
Advanced**. Goal: "I understand C# fundamentals" → "I can design, structure,
test, debug, optimize, and build medium-sized C#/.NET applications."

- **Baseline: C# 14 on .NET 10** (SDK 10.0.401, raw Roslyn grading — verified).
- **Sandbox-shaped design** (mirrors Python Intermediate): no NuGet/network ⇒
  graded code uses BCL only. The frameworks an intermediate C# dev touches
  daily are taught through their mechanisms: learners BUILD the mini-xUnit,
  the in-memory store, the composition root, the HttpClient stub — so they
  understand what the real frameworks do before meeting them in production.
- **Determinism contract:** every graded test uses fixed inputs; HTTP via
  literal `HttpMessageHandler` stubs; concurrency via join/barrier
  choreography (never timing races); culture-invariant formatting.
- **Id namespace:** `csi-` on every id kind (lessons, challenges, practice
  sets, checkpoint challenges).

## Module plan (22 modules)

| # | dir | Title | Core content | Grading notes |
|---|-----|-------|--------------|---------------|
| 1 | `csi-modern-types` | The Type System Deep Dive | value vs reference, boxing, nullable value types, NRT annotations, pattern matching mastery, tuples/deconstruction, target-typed new | boxing identity predictions, null-state fixes, pattern exhaustiveness |
| 2 | `csi-methods` | Methods & Parameters Mastery | ref/out/in, params, optional/named args, expression-bodied, overload resolution, recursion design | overload-puzzle predictions, ref-returning counters, recursion→iteration |
| 3 | `csi-delegates` | Delegates, Lambdas & Closures | method groups, Func/Action/Predicate, composition, closure capture semantics, captured-variable bugs | closure-bug debug (loop capture), pipeline composition, callback wiring |
| 4 | `csi-events` | Events & Observer | event keyword, EventHandler<TArgs>, custom args, encapsulation, unsubscribe/lifetime, memory-leak shape | event-driven notification system project; static-event leak demonstrated via behavior |
| 5 | `csi-generics` | Generic Design | constraints (where T :), default!, generic algorithms, covariance/contravariance, IEnumerable<out T> | generic repository/store, variance compile-shape graded behaviorally |
| 6 | `csi-collections` | Collections & Complexity | Dictionary/HashSet/Queue/Stack/LinkedList tradeoffs, Big-O of ops, choosing collections, IReadOnly* surfaces | frequency maps, LRU-ish eviction via Dictionary+LinkedList, dedup strategies |
| 7 | `csi-iterators` | Iterators & Pipelines | yield return/break, iterator state machines, deferred execution, pipeline composition, eager vs lazy cost | custom data-processing pipeline (mini-build) |
| 8 | `csi-linq` | LINQ Deep Cuts | GroupBy/Join/GroupJoin/Aggregate/Zip/Chunk/except-intersect-union, deferred vs immediate, multiple enumeration, IQueryable concept | LINQ analytics engine project; multi-enumeration bug graded |
| 9 | `csi-async` | Async Programming | Task/Task<T>, async/await, exceptions in async, WhenAll/WhenAny, cancellation done right, IAsyncEnumerable, sync-over-async traps | concurrent async data aggregator project; .Result-deadlock-shape graded via cancellation |
| 10 | `csi-concurrency` | Concurrency Fundamentals | threads vs tasks, ThreadPool, lock/Monitor, race conditions, Interlocked, SemaphoreSlim, concurrent collections | thread-safe counter/queue builds; race fixed by lock graded behaviorally |
| 11 | `csi-di` | Dependency Injection | inversion, constructor injection, lifetimes (singleton/scoped/transient concepts), composition root, testability | hand-wired container + order-processing system project |
| 12 | `csi-config` | Configuration & Options | config sources, options pattern shape, env-specific config, secrets principles | configurable app graded via env-var + file config |
| 13 | `csi-http` | HTTP & API Clients | request/response anatomy, status codes, headers, HttpClient lifetime, error handling, cancellation, retry policy (hand-rolled) | public API client project over literal handler stubs |
| 14 | `csi-json` | JSON & Serialization | System.Text.Json options, naming policies, custom converters (intro), missing/null fields, round-trip fidelity, versioning care | import/export + transform builds; JsonException handling |
| 15 | `csi-data` | Data Access Fundamentals | relational concepts, connections, parameterized SQL (injection defense), transactions, mapping, repository pattern | in-memory store implementing SQL-shaped contracts; injection graded behaviorally |
| 16 | `csi-testing` | Testing & Mocking | AAA, naming, edge cases, parameterized tests, test doubles (stub/fake/mock by hand), isolation | learners BUILD mini test framework; test an existing service thoroughly |
| 17 | `csi-clean-code` | Clean Code & Refactoring | naming, cohesion/coupling, SRP, guard clauses, code smells, behavior-preserving refactoring | refactor-without-changing-behavior graded against frozen tests |
| 18 | `csi-patterns` | Design Patterns in Practice | Strategy/Factory/Builder/Adapter/Decorator/Repository/Observer — problem→naive→pattern→tradeoffs | each pattern graded as a small build/refactor |
| 19 | `csi-architecture` | Architecture Fundamentals | layers, dependency direction, DTOs, services/repositories, composition root, boundaries intro (Clean/Hexagonal concepts) | layering refactor: wrong-direction dependency graded via interface seams |
| 20 | `csi-performance` | Performance Fundamentals | Big-O review, allocations, string building, LINQ cost, collection choice, measurement-first (Stopwatch experiments) | relative-timing experiments with fixed workloads; allocation-shape reasoning |
| 21 | `csi-security` | Security Fundamentals | input validation, authn vs authz, password storage concepts (hashing shape), SQL injection, path traversal, sensitive logging, least privilege | injection/vulnerability fixes graded behaviorally |
| 22 | `csi-capstone` | Capstone: Task Management Engine | projects/tasks/users/priorities/statuses, CRUD service layer, validation, repository, DI wiring, JSON persistence, logging, error handling, reporting LINQ, async operations | milestone-graded mini-builds that compose into the engine; no copy-paste solution |

Each module: 2–3 teaching lessons + 1 checkpoint lesson (lesson-attached
challenge) + 1–2 practice sets anchored afterLesson. Every challenge carries
a reference (R) and a deliberately-wrong (W) solution verified two-sided in
the real sandbox container.

## Projects (the brief's list, adapted to the sandbox)

1. Advanced Collection Toolkit (M6 practice) — typed wrappers over the right
   structures.
2. Event-Driven Notification System (M4 checkpoint mini-build).
3. Generic Data Store (M5 + M15) — generic repository with constraints.
4. LINQ Data Analytics Engine (M8 mini-build).
5. Concurrent Async Data Aggregator (M9 mini-build).
6. Thread-Safe Processing System (M10 practice).
7. Order Processing with hand-wired DI (M11 mini-build).
8. Public API Client (M13 checkpoint) over literal handler stubs.
9. In-Memory Course Catalog with transactions (M15 practice).
10. Mini Test Framework + service test suite (M16 mini-build).
11. Refactoring projects (M17, M19) — behavior-preserving, frozen tests.
12. Capstone: Task Management Engine (M22) — milestone-graded.

## Checkpoints (7 concept gates embedded across modules)

1. M1+M2 — advanced language features (types/params puzzle).
2. M4 — delegates/events (notification system).
3. M8 — LINQ & data processing (analytics).
4. M9+M10 — async/concurrency (aggregator + thread-safe queue).
5. M13+M14 — HTTP/JSON (API client + round-trip fidelity).
6. M15+M16 — data & testing (store + test suite).
7. M19–M21 — architecture/performance/security (layered, measured, safe
   service) — folded into capstone milestones M22.

## Non-goals (explicit)

No EF Core, ASP.NET Core, DI containers, xUnit/Moq, BenchmarkDotNet, real
network, real databases, CLR/GC internals, lock-free/Channels, expression
trees, source generators, unsafe/P-Invoke — see research doc §3/§6 for the
honest substitutes and the Advanced reserve.
