# Curriculum Research — Java — Beginner

Date: 2026-09-13 · Authoring agent: Java — Beginner (Phase 18)

## What was actually inspected

| Source | What was checked | Confidence |
|---|---|---|
| Oracle Java Tutorials (docs.oracle.com/javase/tutorial) — Getting Started trail | Topic inventory for first programs: JDK/JRE/JVM framing, compile/run cycle, "Hello World" anatomy | HIGH (search-verified structure) |
| dev.java/learn (official OpenJDK learning portal) | Learning-path shape: Running Your First Application → Getting to Know the Language → Mastering the API → Organizing Your Application | HIGH |
| Java SE 21 language-changes docs (docs.oracle.com/en/java/javase/21/language) | Which modern features are stable LTS baseline: switch expressions, text blocks, records, sealed classes, pattern matching for instanceof | HIGH |
| JUnit docs (docs.junit.org) + vogella JUnit 5 tutorial | Test-writing model: @Test, assertEquals family, Arrange-Act-Assert, lifecycle annotations, parameterized tests | HIGH |
| Maven Getting Started Guide + Build Lifecycle guide (maven.apache.org) | Standard layout (src/main/java, src/test/java), pom.xml coordinates, default lifecycle phases (compile → test → package) | HIGH |
| roadmap.sh/java (2026) | Community ordering consensus: basics → OOP → collections → exceptions → functional → testing/build before frameworks | HIGH |
| Baeldung / Happycoders Java 17+21 feature surveys | Which "modern Java" features belong in a beginner course vs later: records + switch expressions + text blocks yes; pattern matching for switch, sealed hierarchies, virtual threads later | MEDIUM |
| Common-beginner-mistake literature (Hyperskill, CodeRanch, Stack Overflow threads) | Mistake taxonomy: `==` vs `.equals()` on strings, NPE on chained calls, integer division surprise, missing break in switch, off-by-one in loops, exception swallowing | MEDIUM |
| Exercism Java / freeCodeCamp Java / CS-style syllabi | Practice-first sequencing and exercise density benchmarks (not copied) | MEDIUM |
| **Repository itself** | `docs/ENVIRONMENT.md` (host JDK 25.0.2 LTS), Docker `alpine:3.22` apk index (openjdk21-jdk=21.0.11_p10-r0 available; no headless JDK variant), `src/workers/{sandbox,execute}.ts` job contract, cpp-runtime.ts pattern, schema.ts language enum, API route language branching | HIGH (first-hand) |

## Toolchain decision (measured, not assumed)

- Host: JDK **25.0.2 LTS** (javac 25.0.2) — used by the content QA harness.
- Sandbox: Alpine 3.22 pin **openjdk21-jdk=21.0.11_p10-r0** in the hardened
  image (verified installable before pinning; JRE-headless lacks javac).
- Language level: **`--release 21`** on BOTH harness and sandbox. This makes
  host and sandbox enforce *identical* semantics (better than the C++ track's
  host-clang / sandbox-g++ split). We claim Java 21 features only — never 25.
- Per-test budget: fresh javac + JVM per test (measured ~3–4 s in-container on
  0.5 CPU). API route gives Java jobs 40 s (worker clamps at 30 s → effective
  30 s ceiling, ample for 3–5 tests), 512 MB, matching C++ resource sizing.
- Maven/Gradle are **not installable in the offline sandbox** (no network, and
  the image stays minimal by policy). Build-tool lessons therefore teach
  concepts + pom.xml reading/writing as knowledge challenges, and the QA
  harness validates pom XML structure + equivalent javac invocation. This is
  documented honestly rather than faked.

## What a true Java beginner needs (synthesis)

1. The compile/run mental model FIRST (source → bytecode → JVM) — unlike
   Python, the two-step model is the language's identity and explains
   class-name/file-name rules, `main`'s signature, and later classpath ideas.
2. Static typing as an ally: the compiler catching mistakes early is the
   course's recurring teaching asset.
3. Object model early-but-gradual: Java has no "script mode" — everything
   lives in classes — so classes must arrive by Module 7 (not deferred like a
   Python course can defer them), but *design* (composition vs inheritance)
   waits until Module 8.
4. Collections as the everyday toolbox; arrays kept but demoted to their real
   role (fixed-size, primitive-friendly, API boundary).
5. Exceptions as control-flow literacy: stack traces are *reading material*,
   not error noise.
6. Modern baseline idioms: `var`, records, switch expressions, text blocks —
   taught when they reduce ceremony, flagged as 14+/21 features.

## Sequencing decisions (and why)

- **No separate I/O module for stdin**: the sandbox has no interactive stdin;
  input-shaped practice uses method parameters and file-based data instead.
  Scanner is demonstrated in lessons, never required by graded challenges.
- **Strings merged with arrays** (Module 6): both are "index-and-traverse"
  data shapes; StringBuilder lands here where it is actually needed.
- **Enums/records BEFORE collections** (Module 9): records give clean element
  types (`record Book(String title, int quantity)`) that make every later
  collection exercise realistic instead of `String` soup.
- **Generics AFTER collections** (Module 11): learners first *use* `List<Book>`
  naturally, then learn what the `<…>` means and write their own generic type.
  Wildcards/variance explicitly excluded (Intermediate).
- **Streams LATE and scoped** (Module 14): only after loops are fluent, and
  always with the "when is a loop clearer?" counterpoint.
- **Networking at the END and small** (Module 18): java.net.http.HttpClient is
  taught as one honest client lesson + mockable design; the offline sandbox
  grades HTTP *concepts* via pure functions (request-model builders, response
  parsers, retry logic), never live sockets. No Spring, no servers.
- **Git/Workflow (Module 20)** kept as concept+artifact lessons (README,
  .gitignore, commit-message practice) — the platform cannot grade `git`
  usage itself, and the course says so.
- Modules 19 (problem solving) and 21 (capstone) compress the original 21-module
  proposal's overlap (two "professional repo" modules merged into 16+20).

## Intentionally excluded (deferred to Intermediate+)

Advanced generics (wildcards, variance, recursive bounds) · concurrency &
virtual threads · deep JVM tuning/GC internals · reflection & annotations
beyond an overview · sealed interfaces/pattern matching for switch · JDBC/
databases · Spring/frameworks of any kind · streams as a default style ·
serialization (replaced by explicit text formats — safer and more honest) ·
module system (JPMS) beyond a mention in packages.

## Practice philosophy

Same two-sided contract as every Code Journey track: every challenge ships a
reference solution that must PASS and an intentionally wrong solution that
must FAIL at least one test — verified by `verify-challenges-java.mjs`
against the real runtime (host JDK, `--release 21`, byte-identical generated
test files via the shared harness module). Practice sets target a visible
climb imitation → independent mini-build per module; checkpoints are
cumulative coding tasks, not quizzes.

## Theory/practice balance (planned)

~45% lesson reading (all lessons ≤ 20 min estimated), ~55% hands-on
challenges + builds. Every lesson ends in-or-next-to a graded exercise.
