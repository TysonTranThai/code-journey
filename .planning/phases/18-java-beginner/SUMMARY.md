# Phase 18 — Course: Java — Beginner — SUMMARY

Date: 2026-09-13
Status: **COMPLETE**

## Course

Track `java` (new), course `java-beginner` — **14 modules, 62 lessons**
(incl. 14 checkpoint lessons), 14 practice sets, **45 challenges**
(31 practice + 14 checkpoint), ~34 h estimated (23.4 h lessons + 10.8 h
practice). Full EN + VI parity (62/62 lesson MDX both locales, 45/45
challenge VI sidecars, module/course/track overlays). Prerequisite: none
(track entry). Track path: java-beginner → java-intermediate (future) →
java-advanced (future).

Proposal's ~21 modules consolidated to 14 (merge rationale in
`docs/CURRICULUM-RESEARCH-JAVA-BEGINNER.md`); practice-first rule kept —
every module ends in a graded checkpoint.

## Java runtime (new language in the sandbox)

Mirrored the C++ integration playbook: `src/workers/java-runtime.ts`
(heredoc-written `/job` files, one JVM per test, `__TEST_RESULT__` marker
protocol, `Solution` compiled in the unnamed package with each test),
`java` in the language unions (schema, JobPayload, sandbox, execute, API
route), JDK in the sandbox image. Baseline: **`--release 21` on both the
host QA harness (JDK 25) and the sandbox (openjdk21-jdk)** — semantically
identical compilation. Smoke-tested in the real hardened container:
reference 3/3, wrong-solution fails with educational hint, compile error →
verdict "error".

## QA — actual results

| Gate | Result |
|---|---|
| Two-sided challenge harness (javac `--release 21`) | **59/59 OK** — reference passes, wrong-solution fails |
| validate-content.ts | exit 0 — `SYNC: EN/VI structures match`, 164 nodes/locale, java linear path 62 lessons |
| Typecheck / Lint | clean / clean |
| Unit + integration | **160/160** (spec 3→4 tracks updated for the new track) |
| Production build | exit 0 |
| E2E (full Playwright suite vs live :3000 stack) | **36/36** |
| Sandbox smoke (in-container, worker-exact flags) | 3/3 contracts |
| `git diff --check` | clean |

Harness-caught content defects during authoring (all fixed): Map
iteration-order assumptions, behaviorally-equivalent wrong solutions
(×2), `return`-inside-try escaping `finally`, illegal Java escapes
(`\d`, `\|`), shape-only date regex (→ `LocalDate.parse`), a
static-factory call targeting the wrong class, `Solution.Box.of` vs
`Solution.of`, integer-division expectations, 97-cent coin-change
arithmetic, unique-word semantics (`hello,hello` is ONE unique word),
a dead-code wrong-solution condition, and platform difficulty-schema
mismatches (`normal`/`hard` → `intermediate`/`advanced`).

## Multi-agent safety

- No destructive git commands; nothing committed; all work uncommitted in
  the tree for review.
- Id collisions with cpp/python/web tracks resolved by renaming **my**
  copies (`java-` prefix on 9 lessons); other agents' files untouched.
- Shared-file edits kept additive: `validate-content.ts` (+1 course
  entry, shell-tolerant getCourse), `curriculum-loaders.test.ts`
  (track-count spec 3→4 with the file's own concurrency comment honored),
  `Dockerfile.sandbox` (JDK added alongside existing toolchains), language
  unions (additive `"java"` member).
- Ledger deduped to exactly 59 R + 59 W pairs.

## Files

- Content: `src/content/tracks/java/**` (new track, 14 modules)
- Runtime: `src/workers/java-runtime.ts` + 5 union files +
  `docker/Dockerfile.sandbox`
- Authoring: `scripts/content-authoring/javb*.py` (library + 14 modules +
  wiring), `java-beginner-solutions.mjs`, `verify-challenges-java.mjs`,
  `_smoke-java.mts`
- Docs: `docs/COURSE-JAVA-BEGINNER.md`,
  `docs/CURRICULUM-RESEARCH-JAVA-BEGINNER.md`
- Tests: `tests/unit/curriculum-loaders.test.ts` (track count)

## Remaining work

None for this phase. Java Intermediate is the next level (not started,
per instructions). Repo-level leftovers unchanged (prettier drift,
~570 uncommitted files — user decision).
