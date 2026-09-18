# Curriculum Research — C++ Beginner (Course: cpp-beginner)

**Status:** living research doc for the C++ learning path, Course 1 — C++ Beginner
**Created:** 2026-09-13 (authored against these sources; sandbox capability probed the same day)
**Siblings:** CURRICULUM-RESEARCH-WEB-DEVELOPMENT-*.md (web track), CURRICULUM-RESEARCH-PYTHON-*.md (Python track)
**Rule applied throughout:** sources inform scope and pedagogy; every explanation, example, and challenge is original Code Journey content. No source text is copied.

## 1. Sources consulted

| Source | What it informed |
| --- | --- |
| isocpp.org "Get Started" FAQ (a beginner-devoted page maintained by Standard C++ Foundation) | The three-treatment framing of beginners (yes-C-background / no-C-background / after-another-language), the recommendation to learn modern C++ first, and which resources are considered sound |
| C++ Core Guidelines (isocpp/CppCoreGuidelines, living document) | Ownership philosophy (R rules: "a raw pointer is non-owning", "never a owning raw pointer"), RAII (R.1), `const` correctness (Con), naming, and the "prefer standard library over hand-rolled" stance |
| learncpp.com (structure and topic ordering; pedagogical comparison only) | Ordering evidence: modern sites teach `std::cout`, objects, and the standard library early; C-with-classes habits explicitly deprecated. Also their object-size/lifetime sequencing |
| cppreference.com | Library truth for every construct we teach (`std::vector`, `std::string`, `std::map`, algorithms, streams, `std::filesystem` in C++17) |
| GCC 14.2 release/docs + Alpine 3.22 package pins | Baseline compiler capability: `-std=c++20`, `-Wall -Wextra -Wpedantic` are fully supported on the pinned sandbox toolchain |
| CMake documentation (cmake.org) | Beginner-level targets and `CMakeLists.txt` shape (deferred mostly to Intermediate; Beginner teaches the mental model + one worked build) |
| Exercism C++ track (pedagogical comparison) | Exercise difficulty ladder and the value of tiny, single-concept exercises with hidden tests |
| freeCodeCamp C++ curriculum (comparison) | What large-scale platforms teach beginners; where they drift into C-with-classes habits we deliberately avoid |
| roadmap.sh C++ (comparison) | Community mental model of beginner→advanced scope; used for boundary sanity, not ordering |
| Microsoft C++ docs (learn.microsoft.com, MSVC/C++ conformance pages) | Cross-compiler awareness: content stays standard-portable; nothing taught is GCC-specific |

## 2. Key findings that shaped the course

### 2.1 Baseline standard: C++20

- GCC 14.2 (pinned in the sandbox image) fully implements C++20 core + library; C++23 support is partial on Alpine's build, so C++20 is the last standard that is *safe to assume everywhere*.
- C++20 features that measurably improve beginner ergonomics are used where they help: designated initializers for structs, `std::ranges`-adjacent mental model (taught as algorithms + iterators, with ranges named but not required), `starts_with`/`ends_with` on strings, `std::u8string` awareness (not taught).
- The course never uses a feature merely because it is new; every C++20ism taught is justified by reduced beginner footgun surface.

### 2.2 Modern C++ first — the anti-C-with-classes stance (Core Guidelines)

Findings consistently support what the prompt mandates: beginners should learn resource ownership as **RAII + smart pointers**, not `new`/`delete` fluency.

Concretely adopted:
- **R.11 / R.3**: raw `new`/`delete` appear only once, in a dedicated "why we don't write this" lesson (memory bugs are *shown*, then *fixed* with RAII).
- **R.4**: containers (`std::vector`, `std::string`, `std::map`) are the default; C-style arrays and `malloc`/`free` are never taught as tools.
- **I.23 / R.32**: raw pointers and references are taught as **non-owning access**, with `const std::string&` as the everyday parameter style.
- **ES**: `const` correctness introduced with variables (Module 2), not retrofitted late.
- The ownership arc: value semantics first → references → (much later) pointers → smart pointers as *the* owning pattern → RAII as the principle behind all of it.

### 2.3 What actually separates a C++ beginner from other languages' beginners

1. **The compile/run/link loop.** Dynamic-language learners have never seen translation errors as a distinct class from runtime errors. Module 1 makes the compiler a friendly daily tool: read the first error, fix, recompile.
2. **Static types as a feature.** Declared types catch whole bug classes; `auto` is taught *after* explicit types so it reads as convenience, not magic.
3. **Value semantics + lifetime.** Python learners must learn that `std::vector v2 = v1;` copies. This is taught in Modules 2/7 and reinforced in the memory module.
4. ** UB awareness without UB paranoia.** Beginners are taught: out-of-bounds indexing, uninitialized reads, and dangling references are *not errors you can catch* — prevention (`.at()`, initialize everything, RAII) is the only defense. `vector::at` is preferred in graded code precisely because its exception is catchable.
5. **Deterministic destruction.** File streams close, memory frees, logs flush — at scope exit, in reverse order. This is C++'s superpower and it is taught *before* exceptions.

### 2.4 Ordering decisions (and the evidence for each)

| Decision | Rationale |
| --- | --- |
| Strings taught via `std::string` only (Module 6) | learncpp + Core Guidelines both deprecate C-strings for application code; `std::string_view` is named but deferred to Intermediate |
| `std::vector` before raw arrays; `std::array` shown once for fixed-size needs | Modern-first mandate; raw arrays appear only as "what you will see in older code" |
| Functions before OOP (5 before 10) | Decomposition must precede abstraction; mirrors every reputable beginner ordering |
| Lambdas introduced with algorithms (Module 8), not as a language deep-dive | Their beginner use case is `std::sort` comparators and predicates; syntax depth deferred |
| Structs (9) before classes (10) | Aggregate structs teach data modeling without access-control ceremony; classes then add encapsulation *as the new idea* |
| Composition taught before inheritance; polymorphism last in Module 10 | Core Guidelines and modern pedagogy agree: inheritance is not the default tool; virtual functions arrive as "one tool among several", with composition demonstrated first |
| File I/O (13) after RAII (12) | `std::ifstream` is itself an RAII showcase; teaching files after RAII lets the lesson *use* the principle instead of hand-waving |
| Exceptions taught in the errors module (14) with the "boundary" rule only (throw in failures, catch at main/edges) | Exception-safety depth (guarantees) is Intermediate material |
| `std::filesystem` introduced lightly (13) | C++17 standard library; beginner scope is paths, directory iteration, file size — nothing more |
| CMake taught as one worked build in Module 15 | The prompt's own boundary: full build systems are Intermediate; a beginner needs `cmake -B build && cmake --build build` literacy |

### 2.5 Explicitly deferred to Intermediate/Advanced (out of scope here)

Templates beyond "the standard library uses them" (writing your own), concepts, ranges pipelines, coroutines, concurrency/atomics, custom allocators, operator overloading beyond `operator<<` usage, move semantics as a manual tool (used implicitly by the library), `string_view` ownership subtleties, multiple/virtual inheritance, exception guarantees, ABI, build internals.

### 2.6 Pedagogy: practice density

Course 1 (Web Beginner) landed at ~38% hands-on after the deliberate-practice revision; Python Beginner/Intermediate at ~59%. C++ Beginner targets **≥55% practice** because the language's difficulty is precisely in *writing it*: every module interleaves a practice set after each lesson (learn → micro-practice → learn), with debugging ("Fix the build", "Fix the crash"), output-prediction, and real-world challenge levels per the platform's deliberate-practice model.

## 3. Grading-environment findings (measured, 2026-09-13)

These facts were established by probing the platform, not assumed:

1. The sandbox worker supports `javascript` and `python`; **C++ required a new runtime**. Built this phase: `src/workers/cpp-runtime.ts` mirrors the Python contract (heredoc-data files, quoted random delimiters, same `__TEST_RESULT__` marker protocol).
2. Sandbox image is Alpine 3.22; `g++=14.2.0-r6` pinned and verified (`g++ (Alpine 14.2.0) 14.2.0`).
3. Docker `--tmpfs` defaults include `noexec`; compiled test binaries require an explicit `exec` on the `/tmp` mount (done, with nosuid/nodev retained and the reasoning documented at the call site). `/job` remains noexec.
4. Verified end-to-end through `runSandboxed` (full hardening: network none, read-only rootfs, cap-drop ALL, non-root, memory/cpu/pids ceilings): reference solution passes, wrong solution fails with an educational message, compile errors surface as verdict `error` with the real GCC diagnostic, and a learner-written `main()` cannot collide with the harness (renamed at preprocessing).
5. Graded contract for authors: tests `#include "solution.cpp"` with a CHECK-macro harness (`CHECK`, `CHECK_EQ`, `CHECK_NE`, `CHECK_CONTAINS`, `CHECK_NEAR`, `CHECK_THROWS`, `capture()`). Solutions must be **self-contained single translation units** (includes allowed; no project headers). Interactive input is not graded — programs expose `void program()` or plain functions, mirroring the Python "no input()" rule.
6. `std::cin` is therefore never available in graded runs; lessons teach it for local use, challenges grade parameters/returns/captured output.
