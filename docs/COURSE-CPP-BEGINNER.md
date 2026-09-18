# Course — C++ Beginner (`cpp-beginner`)

**Track:** cpp · **Prerequisites:** none (entry course) · **Locales:** EN + VI
**Spec status:** reconciled to shipped reality at the end of the phase (numbers below are measured on disk).
**Research:** see CURRICULUM-RESEARCH-CPP-BEGINNER.md (baseline C++20, modern-ownership-first pedagogy, sandbox grading contract).

## Identity

- **Audience:** complete beginners to programming, and learners coming from Python/web development who want C++'s mental model (compiled, statically typed, explicit lifetime). The course explicitly calls out the C++-vs-Python differences where they matter, without assuming Python knowledge.
- **Goal:** write, compile, run, debug, and structure modern C++ programs; understand ownership/lifetime/RAII; build and test real command-line applications; be ready for C++ Intermediate (templates, deeper OOP, build systems, concurrency).
- **Baseline:** C++20 on GCC 14 (sandbox-pinned). Warnings treated as guidance from day one.

## Learning outcomes

By the end a learner can:
1. Write, compile, and run single- and multi-file C++ programs; read real compiler errors.
2. Use variables, primitive types, `const`, `auto`, operators, and `std::string` fluently.
3. Control flow: `if/else`, `switch`, `for`, range-based `for`, `while`, `do/while`, `break`/`continue`.
4. Decompose problems into functions with value/`const&` parameters and overloads.
5. Use `std::vector`, `std::array`, `std::map`, `std::set`, `std::pair`; choose a container deliberately.
6. Use STL algorithms (`sort`, `find`, `count_if`, `accumulate`, `reverse`, `min_element`/`max_element`) with introductory lambdas.
7. Model data with `struct`s and `enum class`; write classes with constructors, encapsulation, and `const`-correct methods; use composition-first design with inheritance/polymorphism only where it fits.
8. Explain and apply ownership: stack vs heap, lifetime, RAII, smart pointers (`unique_ptr`/`shared_ptr`), and why raw owning pointers/new/delete are not written in modern code.
9. Read/write text and CSV files; parse with `istringstream`; light `std::filesystem`.
10. Debug systematically (compile → warning → assert → exception → logic) and write basic tests (assert-style checks, edge cases).
11. Explain how headers/translation units/linking fit together; build a multi-file program with CMake.
12. Ship a repository: structure, README, `.gitignore` for build dirs, Git workflow basics.

## Curriculum (shipped)

19 modules, learn/practice interleaved (`afterLesson`), checkpoints as lesson-attached graded challenges, capstone with acceptance-criteria tests and no provided solution.

| # | Module | Focus | Practice sets |
| --- | --- | --- | --- |
| 1 | first-programs | compile/run loop, `main`, iostream, errors-as-feedback | 4 |
| 2 | variables-and-types | types, const/auto, operators, conversions | 4 |
| 3 | conditions | if/else, switch, boolean logic | 3 |
| 4 | loops | for/range-for/while/do-while, accumulation, nesting | 4 |
| 5 | functions | parameters, returns, const&, overloads, decomposition | 4 |
| 6 | strings | std::string ops, parsing with istringstream, validation | 3 |
| 7 | collections | vector/array/map/set/pair, choosing containers | 4 |
| 8 | stl-algorithms | iterators conceptually, sort/find/count_if/accumulate, lambdas | 3 |
| 9 | structs-enums | aggregates, enum class, data modeling | 3 |
| 10 | classes-oop | encapsulation, ctors, const methods, composition-first, polymorphism | 4 |
| 11 | pointers-references | references, pointers as non-owning, nullptr, lifetime | 3 |
| 12 | memory-raii | stack/heap, RAII, unique_ptr/shared_ptr, the new/delete lesson | 3 |
| 13 | files-persistence | ifstream/ofstream, stringstream parsing, light filesystem | 3 |
| 14 | errors-debugging-tests | compile vs runtime vs logic, asserts, exceptions at boundaries, testing | 4 |
| 15 | multi-file-cmake | headers, translation units, linking, one CMake build | 3 |
| 16 | architecture-refactoring | responsibilities, naming, const-correctness, refactor legacy shape | 2 |
| 17 | git-professional-workflow | repo hygiene for C++ (build dirs ignored), README, review basics | 2 |
| 18 | problem-solving | decomposition, edge cases, complexity intuition, choosing structures | 3 |
| 19 | capstone-finance-cli | Personal Finance Manager: persistence, validation, tests, multi-file | 1 + capstone |

Checkpoints: 8 (after modules 1, 4, 7, 10, 12, 14, 15, 18) — coding/debugging tasks, not quizzes.

## Projects

Progression from guided to independent: Personal Introduction (M1) → Temperature Converter & mini-calculator (M2) → Number-Guessing Game (M4) → Text Analyzer (M6) → Inventory Manager (M7) → Data Analysis CLI (M8) → Student Record System (M9) → Library Management System (M10) → Memory-Safe Resource Manager (M12) → Persistent CLI Application (M13) → Debug & Repair Lab (M14) → Multi-File C++ Application (M15) → Refactor a Growing App (M16) → Professional Repository (M17) → **Capstone: Personal Finance Manager** (M19; requirements + acceptance tests + milestones; no solution provided).

## Practice-first balance

Practice sets are interleaved after lessons (never pooled at module end), levels climb imitation → guided → independent → debugging → real-world → mini-build, and every module ends with a checkpoint challenge. Measured split: ≈ 55–60% hands-on / 40–45% reading.

## Grading contract (platform constraints)

- Graded solutions are single translation units; tests `#include "solution.cpp"` via the platform C++ harness (CHECK macros + `capture()`); compile errors surface as verdict `error` with GCC output; interactive input is not graded (programs expose functions or `void program()`).
- Challenges never require `new`/`delete`/C-strings; memory-safety challenges are graded on *modern* rewrites.

## Localization

Vietnamese (`cpp-beginner` → "C++ — Cơ bản") is a full rendering, not a summary: every lesson `.vi.mdx`, practice-set VI overlay, and per-challenge VI overlay (title/prompt/hints; test code shared so grading is identical across locales). Terminology follows the platform's VI corpus rules (biến, hàm, con trỏ, tham chiếu, lớp, đối tượng, kế thừa, đa hình, gỡ lỗi, kiểm thử; compiler/RAII/STL/CMake kept in English where that is the natural technical usage).

## Verification gates (this phase)

- Two-sided challenge harness (reference passes / wrong fails) — see phase SUMMARY for final counts.
- `validate-content.ts`: cpp track loads schema-valid in both locales; EN/VI structures synchronized.
- Regression: web + python courses untouched; full unit/integration, E2E, typecheck, lint, production build green.
