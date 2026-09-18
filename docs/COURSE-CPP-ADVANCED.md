# Course Spec — C++ Advanced (C++ — Nâng cao)

**Track:** C++ (course 3 of 3 — final course in the track)
**Status:** spec for Phase 17 build
**Prerequisite:** C++ — Intermediate (authored in parallel by an independent agent; this course treats its on-disk scope as the boundary — see research doc)
**Audience:** learners who can build and debug multi-file C++ programs, use the STL fluently, and understand RAII, smart pointers, basic templates, and move semantics — and who now want to build serious systems.

## Positioning

Beginner taught "how to write correct C++." Intermediate teaches "how to structure real programs with the standard library." Advanced teaches **"how to reason about what the machine, the compiler, and other threads are actually doing"** — the competencies that separate a C++ developer from a C++ engineer: lifetime/value-category mechanics, generic libraries, compile-time programming, the memory model, performance engineering, ABI/build mastery, security, and production operation.

Not "more syntax." Every module answers an engineering question, and every practice block makes the learner write, predict, debug, measure, or design.

## Learning outcomes

By the end, a learner can:

1. Predict object lifetime, value category, and initialization outcomes exactly — and debug code that violates them.
2. Implement perfect forwarding, resource wrappers, and exception-safe moves; explain RVO/copy elision mechanically.
3. Write generic libraries with specialization, variadics, fold expressions, `if constexpr`, and CTAD.
4. Design concept-constrained APIs and read constraint-failure diagnostics like clues, not noise.
5. Move computation to compile time with `constexpr`/`consteval`/`constinit` and type traits.
6. Build and debug range pipelines, write custom views, and reason about view lifetime hazards.
7. Implement a coroutine generator from `promise_type` primitives — not use a magic async keyword.
8. Explain the C++ memory model and choose memory orderings with justification.
9. Build thread pools, task runtimes, and concurrent queues with the right synchronization primitives; evaluate lock-free designs for ABA and reclamation hazards.
10. Design memory layouts: arenas, pools, `std::pmr`, data-oriented design, cache-line reasoning.
11. Optimize with evidence: measure → hypothesize → change → re-measure, with benchmark rigor.
12. Diagnose undefined behavior by class (dangling, overflow, aliasing, races) and repair it defensively.
13. Debug like an operator: symbols, stack traces, core dumps, minimization, logging and tracing design.
14. Test like a sceptic: property-based, fuzz-style, deterministic concurrency, performance regression tests.
15. Build and link like a professional: modern CMake targets, presets, visibility, LTO, cross-platform matrices.
16. Design for binary compatibility and plugin boundaries (ODR, ABI, versioning).
17. Write a network service: framing, timeouts, backpressure, graceful degradation.
18. Audit and harden a C++ service: memory safety, parsing, injection, hardening flags, secrets.
19. Architect at scale: boundaries, dependency direction, API stability, migration strategies.
20. Operate a service: config, observability, graceful shutdown, rollout and rollback.

## Module plan (21 modules, 73 lessons, 7–13 min each; ~24.5 h)

| # | Module id | Title | Core topics | Practice emphasis |
| --- | --- | --- | --- | --- |
| 1 | `object-model` | Advanced Object Model | value categories (lvalue/xvalue/prvalue), storage duration, temporary materialization, lifetime extension, initialization forms | predict-the-behavior drills |
| 2 | `move-forwarding` | Move Semantics Under the Hood | forwarding refs, reference collapsing, `std::forward`, RVO/NRVO, noexcept moves, Rule of Zero/Five | forwarding + elision debugging |
| 3 | `templates-deep` | Advanced Templates | specialization, variadics, packs, fold expressions, NTTPs, `if constexpr`, CTAD, deduction | generic library building |
| 4 | `concepts` | Concepts & Constrained APIs | `requires`, ad-hoc constraints, subsumption, constrained overloads, diagnostic reading | concept design drills |
| 5 | `compile-time` | Compile-Time C++ | `constexpr`/`consteval`/`constinit`, traits, `integral_constant`, compile-time algorithms, NTTP classes | compile-time validation |
| 6 | `ranges-views` | Ranges & Lazy Pipelines | views, adaptors, projections, `views::` composition, custom view, dangling hazards | pipeline + dangling debugging |
| 7 | `coroutines` | Coroutines from First Principles | `co_await/co_yield/co_return`, `promise_type`, handles, suspension/resumption, generator<T> | build a generator from scratch |
| 8 | `memory-model` | The C++ Memory Model | data races, happens-before, `std::atomic`, memory_order (seq_cst/acq_rel/relaxed), fences | predict-reordering drills |
| 9 | `concurrency` | Advanced Concurrency | threads, jthread/stop_token, mutexes, condition_variable, future/promise, thread pool design | task runtime building |
| 10 | `lockfree-lowlevel` | Lock-Free & Low-Level | CAS loops, ABA, false sharing, cache lines, reclamation concepts, evaluating lock-free claims | correctness evaluation + benchmark |
| 11 | `memory-architecture` | Memory Architecture & Allocators | stack/heap costs, fragmentation, arenas, pools, `std::pmr`, data-oriented design | pmr + layout engineering |
| 12 | `performance` | Performance Engineering | measure→profile→hypothesize→verify, benchmark design, branch/data layout, copies vs moves, complexity vs constant factors | evidence-based optimization |
| 13 | `ub-defensive` | Undefined Behavior & Defensive C++ | UB taxonomy: OOB, dangling, overflow, aliasing, invalid iterators, races; contract-first APIs | UB diagnosis clinic |
| 14 | `debugging-diagnostics` | Advanced Debugging & Diagnostics | symbols, stack traces, core dumps, conditional breakpoints, minimization, logging/tracing design | crash investigation lab |
| 15 | `testing-verification` | Advanced Testing & Verification | property-based, fuzz-style, deterministic concurrency tests, stress, perf-regression tests, test architecture | verifying a concurrent system |
| 16 | `build-systems` | Advanced Build Systems | CMake targets/props, presets, static/shared, visibility, LTO, flags, CI matrices, reproducibility | build engineering |
| 17 | `abi-linking` | ABI, Linking & Compatibility | API vs ABI, mangling, ODR, visibility, versioning, plugin boundaries | plugin system design |
| 18 | `networking` | Networking & Systems | sockets, framing, timeouts, protocol design, backpressure, graceful degradation | protocol implementation |
| 19 | `security` | Secure Systems Programming | memory-safety classes, parsing, injection, hardening flags, secrets, supply chain | service audit + repair |
| 20 | `architecture-production` | Architecture & Production | module boundaries, dependency inversion, API stability, config, observability, graceful shutdown | production readiness review |
| 21 | `capstone-hpc-service` | Capstone — High-Performance Service | integrate all of it in an open-ended build | open-ended engineering |

Practice separation: lessons ≤13 min; each followed by graded practice sets (3–8 challenges) or a mini-build; 1 checkpoint per module arc with an attached graded challenge; 4 named projects and a capstone.

**Projects:** Object Lifetime Investigation Lab (M1–2 mini-builds culminating), Generic Library with Concept-Constrained API (M3–5), Coroutine Task Pipeline (M6–8), Thread Pool + Benchmarked Concurrent Queue (M9–11), Performance Optimization Challenge with evidence (M12), Production Crash Investigation (M14), Cross-Platform Build System (M16), Binary-Compatible Plugin System (M17), Network Service (M18), Secure Service Audit (M19), Production-Ready Service (M20), High-Performance Service Capstone (M21).

## Checkpoints (with attached graded challenges)

1. M2 — Object model & move mechanics
2. M5 — Templates, concepts, compile-time
3. M7 — Ranges & coroutines
4. M10 — Memory model & concurrency
5. M11 — Memory architecture (arena/pmr)
6. M13 — UB & defensive C++
7. M15 — Testing & verification
8. M17 — Build/ABI
9. M19 — Networking & security
10. M20 — Architecture & production
11. M21 — Capstone readiness

## Theory/practice budget

~24.5 h total: lesson reading ≈ 11.4 h (46%), graded coding (practice sets, checkpoints, projects, capstone) ≈ 13.1 h (54%). Advanced keeps Code Journey's practice-first contract: no learner goes more than one lesson without writing code.

## Grading limits (honest)

- Sandbox compiles with fixed `-std=c++20 -Wall -Wextra -Wpedantic` (no sanitizers, no -O2 toggles): UB/security modules grade via deterministic harness checks and reasoning prompts, not runtime sanitizer output. Documented, not faked.
- Wall-clock benchmark thresholds use wide tolerance bands (≥3× margins) so CI noise cannot flip a verdict; the teaching point is the measurement workflow.
- `std::format` is reading material; graded code formats output manually (toolchain parity, see research doc).

## Localization

Full parity: every lesson, practice, challenge title/prompt/hint, and test name authored in English and Vietnamese; VI is natural-language (technical terms kept recognizable: template, concept, coroutine, atomic, memory order, lock-free, allocator, ABI, linker, profiling, benchmarking, sanitizer). Structure synchronized by shared IDs; `validate-content` must report EN/VI SYNC for the course.
