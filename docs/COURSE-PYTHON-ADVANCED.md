# Course — Python — Advanced (Python — Nâng cao)

Track: `python` · Course: `python-advanced` · Status: implementation phase
Prerequisites: `python-intermediate` (which itself requires `python-beginner`).

## Positioning

- Beginner: "I can write Python."
- Intermediate: "I can build Python applications."
- **Advanced: "I can design, optimize, secure, scale, test, maintain, and reason about serious Python systems."**

Advanced is not a bigger syntax course. Every module is engineering-flavored:
implement protocols, register plugins, benchmark concurrency models, profile
before optimizing, harden insecure code, instrument services, and finally
architect a platform from requirements alone.

## Audience

Learners who completed Python — Intermediate: comfortable with OOP, typing
annotations, pytest, SQL, HTTP clients, asyncio basics, and packaging basics.
They can build an application; they cannot yet reason about one under load,
failure, and team-scale change.

## Learning outcomes

1. Implement custom objects that obey Python protocols (containers, callables,
   context managers) via the data model, descriptors, and MRO.
2. Use metaclasses, `__init_subclass__`, and class decorators for registries and
   plugin frameworks — and articulate when *not* to.
3. Make real libraries type-safe: generics, variance, ParamSpec, overloads,
   Protocols, TypedDict; wire static analysis into a project.
4. Choose and benchmark concurrency models (threads, processes, asyncio) for
   I/O- vs CPU-bound work; find and fix races and deadlocks.
5. Write structured async systems with TaskGroup, timeouts, cancellation
   propagation, async context managers/iterators, and bounded queues.
6. Profile with cProfile/timeit and deliver measured, verified optimizations.
7. Explain practical CPython internals: bytecode, frames, refcounting/GC, the
   import system — and how they explain real behavior.
8. Architect with ports & adapters, dependency inversion, repositories, and DI;
   refactor tangles without breaking behavior.
9. Engineer production APIs: validation, error contracts, rate limiting,
   idempotency, connection pooling, background work.
10. Build resilient distributed pieces: workers, retries with backoff,
    idempotency keys, circuit breakers, health checks.
11. Use relational databases the advanced way: query plans, indexes,
    transactions/isolation, N+1 elimination, optimistic concurrency.
12. Threat-model and repair real vulnerabilities (injection, unsafe
    deserialization, SSRF, path traversal, secrets leakage).
13. Test like an engineer: fixtures architecture, property-based testing,
    contract tests, deterministic concurrency tests, flake elimination.
14. Observe services: structured logs, metrics, correlation IDs, health/readiness, SLOs.
15. Ship a modern package: pyproject.toml, wheels, entry points, lockfiles.
16. Rescue and maintain unfamiliar, messy codebases without breaking behavior.

## Module map (14 modules)

| # | Module | Anchor project |
|---|---|---|
| 1 | data-model-protocols — data model, attribute lookup, descriptors, MRO, `__slots__` | Python-compatible custom collection |
| 2 | metaprogramming — `type`, metaclasses, `__init_subclass__`, decorators, registries | Plugin registration framework |
| 3 | advanced-typing — generics, variance, ParamSpec, overloads, Protocols, TypedDict | Typed library component |
| 4 | concurrency-parallelism — threads, GIL, pools, races, locks, multiprocessing | Concurrent job processor (benchmarked) |
| 5 | structured-async — TaskGroup, timeouts, cancellation, async CMs/iterators, queues | High-concurrency async service |
| 6 | performance-engineering — cProfile, timeit, memory, cache discipline | Performance rescue |
| 7 | cpython-internals — bytecode, frames, GC, import system | Internals investigation |
| 8 | architecture-patterns — ports/adapters, DI, repositories, refactoring | Tangled-app refactor |
| 9 | production-apis — validation, errors, rate limits, idempotency, pooling | Production-style API |
| 10 | distributed-fundamentals — queues, workers, retries/backoff, circuit breakers | Distributed job system |
| 11 | database-engineering — plans, indexes, isolation, N+1, optimistic locking | High-performance data service |
| 12 | security-engineering — threat modeling, injection, deserialization, SSRF, secrets | Security hardening lab |
| 13 | advanced-testing — property-based, contract, concurrency tests, flake triage | Unreliable-app test suite |
| 14 | production-engineering — observability, packaging, systems programming, legacy rescue | Instrumented service + capstone readiness |
| — | capstone-platform — production-grade job-processing platform | Capstone (requirements only) |

## Practice structure

Learn → Deep Dive → Practice (challenge sets after each lesson) → Debug →
Benchmark/Test → Build → Project. All graded challenges are Python-language
sandbox challenges with two-sided verification. Checkpoints are engineering
tasks (implement/repair/benchmark), not quizzes: modules 1, 3, 4, 6, 9, 12, 14,
plus final-readiness.

## Localization

Full EN/VI parity (`python-advanced` / `Python — Nâng cao`), same IDs
everywhere; Vietnamese reads naturally with technical terms kept recognizable
(descriptor, metaclass, event loop, profiling…).

## Estimated effort

~48 h total: ≈13 h lessons (theory + deep dives), ≈29 h practice/challenges
(~60%), ≈6 h projects/checkpoints beyond challenge time. Practice-dominant by
design.

## QA gate

Every challenge: reference PASS + plausible-wrong FAIL on the shared harness
(host python3.11, sandbox python3.12, graded code 3.11-compatible).
`validate-content.ts` extended to the new course; full platform regression
(typecheck, lint, unit, E2E, build) after authoring.
