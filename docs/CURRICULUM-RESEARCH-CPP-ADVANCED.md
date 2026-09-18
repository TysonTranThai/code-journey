# Curriculum Research — C++ Advanced (Course: cpp-advanced)

**Status:** research doc for Course 3 of the C++ track
**Created:** 2026-09-13 (authored against these sources; toolchain probed the same day)
**Siblings:** CURRICULUM-RESEARCH-CPP-BEGINNER.md (Course 1); C++ Intermediate is authored by an independent agent (Course 2, in progress during this research)
**Rule applied throughout:** sources inform scope and pedagogy; every explanation, example, and challenge is original Code Journey content. Nothing is copied from any source.

## Sources

| Source | Role | Confidence |
| --- | --- | --- |
| en.cppreference.com — language/library references (`/w/cpp/language/coroutines`, `/w/cpp/atomic/memory_order`, `/w/cpp/coroutine/generator`, `/w/cpp/language/templates`, `/w/cpp/ranges`) | normative behavior reference for every language/library topic | HIGH |
| ISO C++ Core Guidelines (isocpp.github.io/CppCoreGuidelines) — philosophy, Per. (performance), CP. (concurrency), T. (templates), ES. (expressions/statements) rules | pedagogy and stance: "don't optimize without reason", concurrency rules, "no raw owning pointers" carry-over | HIGH |
| D. M. Kohlhoff (Stanford), "My tutorial and take on C++20 coroutines" (scs.stanford.edu/~dm/blog) | deepest accurate public walkthrough of the promise/handle machinery; used to structure Module 7 (we teach our own minimal generator, not his code) | MEDIUM-HIGH |
| CppCon / CppWeekly talks on C++23 `std::generator` (via CppWeekly Ep 428) | context that hand-rolled generators remain the C++20 baseline skill | MEDIUM |
| GCC 14.2 release notes / libstdc++ C++20/23 status pages | exact sandbox feature support (below) | HIGH (probed locally) |
| Learncpp.com chapter ordering (memory, templates, moves) | curriculum sequencing comparison only | MEDIUM |
| Exercism C++ track | difficulty calibration for practice items | MEDIUM |

Live web checks 2026-09-13: Core Guidelines section map (Per.1–Per.3 "don't optimize without reason / prematurely / something not performance critical" as the performance module's stance), cppreference coroutine and memory_order pages, `std::generator` status (C++23 — NOT used as the teaching baseline; GCC 14.2's libstdc++ ships it only partially, and we teach the hand-rolled promise_type because that is the real skill).

## Toolchain reality (probed on this machine, 2026-09-13)

The platform has exactly two compilers, and the course may use only what both support:

| Environment | Compiler | Baseline used by the platform |
| --- | --- | --- |
| QA harness (runs on the dev machine) | Apple clang 21.0.0 | `-std=c++20` |
| Sandbox (grades learner runs) | GCC **g++ 14.2.0** (Alpine 3.22, pinned in `docker/Dockerfile.sandbox`) | `-std=c++20` |

Probe results (both compilers, `-std=c++20`):

- **OK and used:** `<concepts>`, `<ranges>`, `<coroutine>` (a real `co_return` program compiled and ran), `<thread>`, `<atomic>`, `<memory_resource>`, `<span>`, `<stop_token>`, `<barrier>`, `<latch>`, `<semaphore>`, `<syncstream>`, `std::jthread`, `std::format` (header exists on clang; GCC 14.2 also ships `<format>` — but to stay identical on both we format output manually in graded code and treat `std::format` as reading material)
- **Deliberately NOT the teaching vehicle:** C++23 `std::generator` (taught as "what C++23 adds", not used in graded code), C++23 `std::expected` (GCC 14.2 ships it, clang probe OK — used in one reading exercise only, not required in graded snippets), modules (`import std;` — neither target compiles it reliably in the pinned images), network TS / executors (not in any standard library)
- Consequence: everything below is **C++20-maximal, C++23-aware**. No graded challenge uses a feature outside the probed set.

Sanitizers: the QA harness can run `-fsanitize=address,undefined` locally; the sandbox runtime compiles with fixed flags (`-Wall -Wextra -Wpedantic`, no sanitizers — latency). UB teaching (Module 12) therefore uses **static reasoning + harness-visible behavior**, not runtime sanitizer grading. Honest limitation, documented rather than faked.

## What the sibling courses cover (boundary inputs)

- **C++ Beginner (mine, complete):** compilation model, types, control flow, functions, strings, collections, STL algorithms, structs/enums, classes, pointers/references, RAII & smart pointers, files, errors/debugging/tests, multi-file CMake, architecture refactoring, Git, problem solving, capstone CLI.
- **C++ Intermediate (other agent, in progress — read from disk, never modified):** `modern-cpp` (move semantics entry), `templates`, `smart-pointers-raii`, `operators-copy-move`, `memory-and-lifetime`, `stl-fundamentals`, `iterators-algorithms`, `inheritance-polymorphism`, `object-oriented-design`, `errors-and-files`, `dsa`, `cppi-final-project`.

**Hard boundary decisions caused by this overlap:**

| Topic | Where it lives | Advanced's move |
| --- | --- | --- |
| Move semantics, copy/move operators | Intermediate `operators-copy-move`, `modern-cpp` | Advanced does **perfect forwarding / reference collapsing / RVO mechanics** only, opening with a "you know moves; now here is what the compiler actually does" bridge |
| Basic templates | Intermediate `templates` | Advanced does specialization, variadics, fold expressions, `if constexpr`, deduction — no "what is a template" |
| Smart pointers / RAII | Beginner M11–12 + Intermediate `smart-pointers-raii` | Advanced never re-teaches; allocators/pmr assume it |
| Iterators/algorithms basics | Intermediate `iterators-algorithms` | Advanced goes straight to **ranges/views/projections** |
| Threads/intro concurrency | (neither course teaches it) | Advanced owns the entire concurrency arc from zero |
| Coroutines | nobody | Advanced owns it |
| DSA | Intermediate `dsa` | Advanced uses complexity only as an input to performance engineering |

## Sequencing findings

1. Value categories and lifetime come first: every later topic (forwarding, views, coroutines, atomics) is defined in terms of them; misordered courses teach these as sidebars.
2. Templates → concepts → compile-time as one arc: constraints before metaprogramming, so `if constexpr` replaces SFINAE rather than succeeding it (Core Guidelines T.-stance: prefer concepts).
3. Ranges before coroutines: a lazy view is the conceptual on-ramp to a suspended frame.
4. Concurrency arc is model-first: memory model and atomics *before* threads, so the memory_order discussion happens when there is a formal backdrop (cppreference memory_order structure: seq_cst → acquire/release → relaxed, teach in reverse order of rigor).
5. Performance engineering sits after memory/allocators (you cannot reason about cache lines before arenas) and before security/production (measured claims are the engineering ethic being graded).
6. ABI/build systems near the end: they are systems knowledge that only pays off once the learner writes systems code.
7. Networking before security so the audit project has a real attack surface to audit; production engineering last before capstone so the capstone can demand its vocabulary.

## Deliberate exclusions (recorded, with reasons)

- Template metaprogramming in the Boost.Spirit sense, deep CRTP theory, SFINAE archaeology beyond "recognize it in legacy code" — obsolete style, concepts supersede.
- Lock-free data structures as graded implementation work — CP.200+ guidelines treat these as expert-only; the module teaches CAS/ABA/reclamation *reasoning* and has learners **evaluate** implementations, not ship them.
- Custom allocators as raw `std::allocator_traits` exercises — `std::pmr` is the modern interface; classic allocator plumbing appears only as reading.
- Modules (`import std;`), executors/networking TS, C++26 anything — not supported in the pinned toolchain (probed).
- Sanitizer-graded challenges — sandbox compile flags are fixed; documented limitation, replaced by reasoning-based and harness-based checks.
- Kernel/driver, GPU/SIMD-intrinsics programming — different discipline; explicitly out of Code Journey's web platform scope.

## Practice-first structure

Same shape as Beginner/Intermediate: short lessons (7–13 min reads), every lesson followed by graded practice or a mini-build, module checkpoints with attached challenges, two-sided QA (reference passes, wrong fails). Advanced adds two activity verbs used throughout: **predict** (state exact behavior before running — value categories, memory ordering) and **measure** (timing comparisons with tolerance bands, not eyeballing).

## Sources consulted but not copied

Everything above; no content copied. All examples, narratives, projects, hints, and Vietnamese text are original.
