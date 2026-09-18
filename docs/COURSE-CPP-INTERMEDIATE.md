# C++ — Intermediate (C++ — Trung cấp)

Track: `cpp` · Course: `cpp-intermediate` · Status: **COMPLETE** (2026-09-13)

The second course in the C++ learning path. Assumes the C++ Beginner course
(`cpp-beginner`) as its only prerequisite and moves the learner from "I can
write basic C++" to "I can design classes, manage memory and lifetime, use the
STL fluently, and build a real file-persisted application."

## Positioning

| Beginner | **Intermediate (this course)** |
|---|---|
| syntax, types, control flow | ownership, classes, polymorphism, STL, templates |
| "I can write C++." | "I can design C++ programs." |

Not covered (deferred to a future C++ — Advanced): template metaprogramming,
concurrency/threads, compiler internals, advanced optimization.

## Structure

- **12 modules, 65 lessons, 24 practice sets, 60 challenges, ~28 h** estimated
- Every challenge is two-sided verified: reference solution passes all tests,
  an intentionally wrong solution fails at least one (60/60 green on the
  dedicated harness, Apple clang, C++20).
- English + Vietnamese full parity: 65/65 lesson VI overlays, 60/60 challenge
  VI sidecars, module + course overlays. All lesson MDX compiles clean.

### Modules

1. `memory-and-lifetime` — references, pointers & arithmetic, dynamic memory,
   const correctness, stack vs heap, lifetime model
2. `object-oriented-design` — classes, ctors/dtors, encapsulation, `this`,
   static members, composition
3. `inheritance-polymorphism` — inheritance, ctor/dtor order, overriding,
   virtual functions, abstract interfaces, virtual destructors
4. `operators-copy-move` — operator overloading, copy semantics, Rule of
   Three/Five, move semantics
5. `stl-fundamentals` — sequence + associative containers, choosing the right
   container
6. `iterators-algorithms` — iterators, `sort/find/count/accumulate/transform`,
   lambdas & captures
7. `modern-cpp` — `auto`/`decltype`, `constexpr`, `enum class`, structured
   bindings, `optional`/`variant`/`tuple`/`string_view`
8. `smart-pointers-raii` — RAII, `unique_ptr`/`shared_ptr`/`weak_ptr`,
   ownership design
9. `templates` — function/class templates, specialization intro, generic
   design (incl. move-only element types)
10. `errors-and-files` — exceptions, custom exception types, exception safety,
    stream/file parsing
11. `dsa` — complexity, binary search, recursion, linked lists, BSTs, graphs
    (BFS/DFS)
12. `cppi-final-project` — capstone: file-persisted Library CLI integrating
    classes, STL, `optional`-based validation, and robust record parsing

Each module ends with a checkpoint challenge (`cppi-checkpoint-*`); the course
path is Beginner → **Intermediate** → (future) Advanced.

## Authoring & verification

- Authoring pipeline: `scripts/content-authoring/cppi.py` + `cppi_m1..m12.py`,
  mirroring the Beginner `cppb.py` writers so shapes stay byte-compatible with
  the platform loaders.
- Solution ledger: `scripts/content-authoring/cpp-intermediate-solutions.mjs`
  (`R[id]` reference / `W[id]` wrong — separate file from Beginner's ledger so
  the two agents' work never interleaves).
- Harness: `node --import tsx --import ./scripts/worker-imports.mjs
  scripts/content-authoring/verify-challenges-cppi.mjs` → **60/60 two-sided OK**.
- Grading discipline learned and applied throughout: every test snippet is a
  self-contained translation unit (solution.cpp is `#included`; no cross-test
  state), and C++ code is authored in raw strings so `\n` literals stay literal.
- Validator: `validate-content.ts` exit 0; cpp track linear path = 130 lessons.

## Global-id hygiene

The platform's content ids share one global namespace. Course-specific
prefixes (`cppi-`) and renames were applied to this course's copies only —
Beginner and other tracks' files untouched: lesson `choosing-containers` →
`choosing-stl-containers`, lesson `iterators` → `cppi-iterators`, checkpoint
`advanced-checkpoint-capstone` → `cppi-checkpoint-capstone-lesson`, module
`final-project` → `cppi-final-project`.
