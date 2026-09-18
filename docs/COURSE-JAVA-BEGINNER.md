# Course: Java — Beginner (java-beginner)

Date: 2026-09-13 · Status: **COMPLETE** (all content two-sided verified)

## Position

Track `java`, course 1. Path: **java-beginner → java-intermediate (future) →
java-advanced (future)**. Prerequisite: none — this is the track's entry
course and assumes no prior programming.

Vietnamese: **Java — Cơ bản** (`track.vi.json` / `course.vi.json` overlays).

## Toolchain (verified, not assumed)

| Component | Value |
|---|---|
| Host JDK (QA harness) | Java 25.0.2 LTS (`java -version`) |
| Sandbox JDK | `openjdk21-jdk` (Alpine 3.22, `docker/Dockerfile.sandbox`) |
| Language level | `--release 21` on BOTH host and sandbox — semantically identical |
| Build tool | none required for graded work (stdlib-only); Maven taught conceptually in Module 13 lesson content |
| Test framework | in-sandbox `CjTestBase` harness (CHECK-style, mirrors JUnit concepts); JUnit taught as the real-world shape |

Java infra added this phase (mirrors the C++ playbook): `src/workers/java-runtime.ts`,
`java` in the language unions (`schema.ts`, `execution/types.ts`, sandbox,
execute, API route), JDK in the sandbox image, `verify-challenges-java.mjs`
QA harness. Smoke-tested end-to-end in the real hardened container
(reference passes, wrong-solution fails with hint, compile-error verdict).

## Shape (verified from disk)

| Metric | Value |
|---|---|
| Modules | 14 |
| Lessons | 62 (14 checkpoints, one per module) |
| Practice sets | 14 (one per module) |
| Challenges | 45 (31 practice + 14 checkpoint) |
| Lesson time | ~23.4 h |
| Practice time | ~10.8 h |
| Total estimate | ~34 h |
| Theory:practice | ~70:30 by minutes, but every concept lands in a graded challenge |

## Modules

1. `java-first-programs` — JVM model, Hello World, printing, errors (4 ch)
2. `java-types-operators` — primitives, String, var, operators, casting (5 ch)
3. `java-conditions` — if/else, switch, boolean logic, validation (5 ch)
4. `java-loops` — for/enhanced-for/while/do-while, break/continue (5 ch)
5. `java-methods` — parameters, returns, overloading, decomposition (4 ch)
6. `java-arrays-strings` — arrays, 2-D, String methods, StringBuilder (3 ch)
7. `java-classes-objects` — fields, constructors, encapsulation, static (2 ch)
8. `java-oop-design` — composition-first, inheritance, polymorphism (2 ch)
9. `java-data-modeling` — enums, records, equality contracts (3 ch)
10. `java-collections-generics` — List/Set/Map/Deque + generics & bounds (3 ch)
11. `java-exceptions-files` — try/catch/finally, robust parsing, custom exceptions (3 ch)
12. `java-streams-optional` — lambdas, pipelines, Optional at boundaries (3 ch)
13. `java-testing-debug` — JUnit shape, edge-case discipline, debug method (2 ch)
14. `java-files-capstone` — java.nio.file + the capstone (1 ch)

Note: the proposal's ~21 modules were consolidated into 14 — merge decisions
(generics into collections, Maven into testing, git/API trimmed to lesson
content) are documented in `docs/CURRICULUM-RESEARCH-JAVA-BEGINNER.md`.
Practice-first rule kept: every module ends in a checkpoint challenge.

## Capstone

`javb-m14-cp-ledger` — a personal transaction ledger: a self-validating
`Transaction` record, signed balance queries (`net`), uppercase label
queries (`labelsSince`), a canonical pipe-format save (`saveLines`), and a
junk-proof loader (`loadLine` skips malformed lines). Composes records,
collections, streams, defensive parsing, and the module-11 exception
discipline into one artifact. Learner-visible requirements + tests; the
wrong solution (unguarded load) is shown for contrast.

## Challenge quality gate

Every challenge is **two-sided verified**: the reference solution compiles
and passes every test; the intentionally-wrong solution must fail at least
one test (proving the tests actually discriminate). The QA harness ran
clang-tight iterations: **59/59 OK** after content fixes. Real defects the
harness caught during authoring: Map iteration-order assumptions, a
dead-code wrong solution, `return`-inside-try escaping `finally`,
illegal `\d`/`\|` Java escapes, a shape-only date regex accepting
`2026-13-40` (replaced with `LocalDate.parse`).

## Localization

- 62/62 lesson MDX in EN + VI (124 MDX files), all compile via the
  generated mdx-map (1080 imports).
- 45/45 challenge VI sidecars (title/prompt/test names/hints).
- Module, course, and track VI overlays complete; `validate-content.ts`
  reports `SYNC: EN/VI structures match for java-beginner`.
- Vietnamese is authored for Vietnamese developers: JVM/JDK/class/method
  stay in English, explanations are natural Vietnamese, not machine
  translation.

## QA results (actual runs, 2026-09-13)

| Gate | Result |
|---|---|
| Two-sided challenge harness (javac `--release 21`) | **59/59 OK** |
| validate-content.ts | exit 0 — EN/VI match, 164 nodes load per locale, java linear path = 62 lessons |
| Typecheck (`pnpm typecheck`) | clean |
| Lint (`pnpm lint`) | clean |
| Unit + integration (`pnpm test`) | **160/160** (spec updated 3→4 tracks for the new java track) |
| Production build (`pnpm build`) | exit 0 |
| E2E (Playwright, full suite) | **36/36** |
| `git diff --check` | clean |

## Files

- Content: `src/content/tracks/java/**` (track, course, 14 modules)
- Runtime: `src/workers/java-runtime.ts`, union updates in `schema.ts`,
  `execution/types.ts`, `sandbox.ts`, `execute.ts`, `challenges/run/route.ts`,
  `docker/Dockerfile.sandbox`
- Authoring: `scripts/content-authoring/javb*.py`, `java-beginner-solutions.mjs`
  (59 R + 59 W pairs, deduped), `verify-challenges-java.mjs`
- Docs: this file + `docs/CURRICULUM-RESEARCH-JAVA-BEGINNER.md`
- Spec test: `tests/unit/curriculum-loaders.test.ts` (3→4 tracks)
