# Phase 15 — C++ Beginner — SUMMARY

Date: 2026-09-13
Status: **CONTENT COMPLETE — all gates green**
Authoring agent: independent session; ran alongside the active Python Advanced agent (their content untouched; my work is a brand-new `cpp/` track with zero file overlap).

## What was built

**Course `cpp-beginner`** (track: cpp) — modern C++ (C++20 baseline, GCC 14.2 in sandbox) taught ownership-first, aimed at true beginners *and* Python/Web converts who need C++'s different mental model.

| Metric | Actual |
|---|---|
| Modules | 19 (incl. capstone) |
| Lessons | 66 (17 of them checkpoint lessons) |
| Practice sets | 27 |
| Challenges | 46 — two-sided verified **46/46** (R passes, W fails) |
| Time | 1447 min ≈ 24 h — practice 640 min (44%) + theory 807 min (56%); every lesson contains micro-practice, so hands-on share is higher than the manifest split |
| Locales | EN complete, VI complete (184 nodes load clean per locale; EN/VI structures match) |

Module arc: first-programs → variables-and-types → conditions → cpp-loops → cpp-functions → strings → collections → stl-algorithms → structs-enums → classes-oop → pointers-references → memory-raii → files-persistence → errors-debugging-tests → multi-file-cmake → architecture-refactoring → git-professional-workflow → problem-solving → capstone-finance-cli.

Memory-safety spine (per prompt requirements): RAII and ownership are taught as core concepts (module 11–12), raw `new`/`delete` framed as what smart pointers exist to avoid, pointers as non-owning access, `const`-correctness threaded throughout, `-Wall -Wextra -Wpedantic` always on.

## Platform capability added (the big piece)

The sandbox previously executed only `javascript | python`. A C++ course with auto-graded challenges required extending the execution platform, following the Phase 13 Python precedent exactly:

- `src/workers/cpp-runtime.ts` — new runtime: solution + tests written as heredoc data into /job; solution syntax-checked first (non-compiling solution → single educational compiler error, not N confusing failures); each test compiled with `#include "solution.cpp"` + `#define main cj_learner_main` (learner main can't collide with the harness); CHECK/CHECK_EQ/CHECK_NEAR/CHECK_CONTAINS/CHECK_LINES/CHECK_THROWS macros throw with educational messages; `capture(fn)` captures stdout.
- `docker/Dockerfile.sandbox` — added `g++` (GCC 14.2.0, Alpine 3.22 pin).
- `src/workers/sandbox.ts` — `/tmp` tmpfs mount changed from `noexec` to `exec` (explicit; Docker's `--tmpfs` defaults to noexec — empirically proven). Security model: arbitrary student code already executed in-container via interpreters, so noexec never prevented that; network-off, read-only rootfs, caps-drop, non-root, memory/cpu/pids ceilings untouched. `/job` stays noexec.
- Dispatch points widened additively: schema language enum, execution types, execute.ts, sandbox.ts, challenge run route (per-language timeout/memory: C++ 120s — compile headroom).
- Proven end-to-end through the real `runSandboxed` path (full hardening): pass, fail-with-message, compile-error, learner-main-collision — 4/4 probes.

## The QA story (failures root-caused, never papered over)

First full harness run: 35/46. Every failure diagnosed with real compiler/runtime output:

- **Preprocessor insight (root cause of 3 compile failures):** macro arguments split at *top-level commas* — braces do NOT protect them. `CHECK_LINES(h, {"a","b"})` was a hard error → harness macro made variadic (`CHECK_LINES(h, "a", "b")` → helper + `{__VA_ARGS__}`); the two authored brace-form tests migrated.
- **CHECK_THROWS(fn)** expanded as `fn()` — calling the RESULT of the author's expression. Made a variadic statement macro.
- **cpp19 capstone R/W were missing `};`** after the class body (would fail for learners too) — fixed.
- **3 wrong solutions were accidentally correct:** `<=` comparator (UB that happened to sort correctly), `>=` descending (passes on distinct values), comment-only W (= R). Replaced with genuinely wrong implementations; one test gained a tie-breaking probe (with VI overlay mirror).
- **cpp12 bump test collided with R's own increment** (expected 1, R produced 2); W had matched only by copying. Test fixed, W replaced with forget-the-increment.
- **2 authored test snippets were broken C++** (`program()` missing `;` inside a test lambda; bare newline inside `[]{ }`) — the same code learners would have failed against — fixed.
- **Systemic over-escaping (caught by byte inspection before any harness run):** all code strings carried `\\n` instead of real newlines / `\n` escapes. Fixed with a C++-aware state machine (literal-aware) across 48 challenge JSONs + solutions ledger; ledger rebuilt from authoring source (46 R/W pairs, dedup of 88 duplicate appends from re-runs).
- **MDX compile traps in build:** `pair<iterator,bool>` parsed as a JSX tag with `,` in the name; bare `{4, 9, 2, 9}` set literals parsed as JSX expressions (both EN+VI) — all fenced/backticked.
- **Global ID uniqueness (loader-enforced):** 7 of my ids collided with Python ids (e.g. `first-programs`) — renamed mechanically on my side only.

Final: **46/46 two-sided OK** (`scripts/content-authoring/verify-challenges-cpp.mjs`, which imports `buildCppTestFile` from the runtime so QA test files are byte-identical to what the sandbox compiles).

## Gates

| Gate | Result |
|---|---|
| validate-content.ts (full tree, zod loaders, EN+VI) | ✅ 3 tracks, 6 courses; cpp: 19 modules/65 linear lessons; `SYNC: EN/VI structures match`; web 143 / python 106 / cpp 65 |
| Two-sided C++ harness | ✅ 46/46 |
| Unit + integration (vitest) | ✅ 160/160 (track-count test updated 2→3 tracks with explicit cpp assertions — legitimate) |
| Typecheck | ✅ |
| Lint | ✅ 0 errors (3 warnings in the Python Advanced agent's WIP harness file — untouched) |
| E2E (Playwright) | ✅ 36/36 |
| Production build | ✅ 1125 static pages (was 986; +139 from the C++ course) |
| Live routes (restarted :3000 preview) | ✅ /learn/cpp, course, lesson 200; VI cookie page renders "Cơ bản" |

## Multi-agent safety

- Python Advanced agent active throughout (532 files, authoring mid-modules-6-8 when checked). Zero writes to `python-advanced/`; shared-file edits (schema, types, execute.ts, sandbox.ts, run route, Dockerfile, validate-content.ts, loaders test) were additive `str_replace` on files idle since the Python phases, verified with `git diff` + mtime checks first.
- No destructive git commands. No reverts, no resets, no deletes of others' work.
- One deliberate, documented platform change: `/tmp` tmpfs `noexec` → `exec` (required for compiled binaries; security boundaries unchanged).
- Their 3 lint warnings in `verify-challenges-py.mjs` left as-is.
- User's :3000 preview server was stopped briefly for the E2E run (Next 16 allows one dev server per project dir) and restarted afterwards with fresh content; routes verified live.
- Temporary one-off fix scripts deleted; kept: `cppb*.py` (regeneratable content source), `cpp-solutions.mjs` + `verify-challenges-cpp.mjs` (the QA harness pair).

## C++ Beginner status: COMPLETE (all gates green)

C++ Intermediate / Advanced: intentionally NOT started (out of scope). The research doc records the boundary (templates depth, concepts, ranges, coroutines, concurrency, allocators → Intermediate/Advanced).
