# Course Spec — AP CSA Beginner / Foundations

Track `ap-csa` (NEW) · Course `ap-csa-beginner` · Phase 30 · Status: **COMPLETE (2026-09-21)**

## Identity

- **Audience:** Students preparing for AP Computer Science A — complete beginners
  and programmers from other languages new to Java. No prior Java assumed;
  Algebra 1 comfort suffices.
- **Goal:** the complete Java foundation for AP CSA — read/trace/write/debug Java
  and recognize the exam's recurring patterns — ready to enter a dedicated
  AP CSA exam-preparation course.
- **Positioning:** NOT the normal Java Beginner course; NOT yet full exam prep.
  Ladder: `ap-csa-beginner` → (future) AP CSA Core/Exam Prep → (future) Mock FRQs.

## Measured numbers

| Metric | Value |
| --- | --- |
| Modules | 20 |
| Lessons | 80 (60 teaching + 20 checkpoints) |
| Practice sets | 20 (one per module) |
| Challenges | 109 (89 practice + 20 checkpoint) |
| Locales | EN + VI, synchronized |
| Estimated time | ~36.5 h (2191 min) |
| Prerequisites | none (Java-from-zero) |

## AP CSA alignment (revised Fall-2025 framework)

- Unit weighting honored: heavy Data Collections (arrays, ArrayList, 2D) and
  Selection/Iteration; Class Creation explicit; inheritance kept light
  (extends/super/one-level override only — no interfaces, abstract, protected).
- Skill emphasis: "Analyze Code" (37–53% of exam) drives the trace-table,
  output-prediction, and which-method-runs threads throughout.
- FRQ foundations: preconditions/postconditions, writing methods from prose,
  extending provided classes, spec-example tracing (Module 18).
- Four FRQ types foreshadowed: Methods/Control (M6–M8), Class Design (M8, M12,
  M20), ArrayList (M10, M19), 2D Array (M15).
- Intentionally excluded: multithreading, JVM internals, reflection, streams,
  functional style, Spring, networking, databases, design patterns beyond
  composition, advanced data structures.

## Java execution environment (verified)

- `javac --release 21`, `-nowarn`; JVM `-XX:+UseSerialGC -Xss4m`; container
  sandbox: no network, CPU/mem capped, 30 s wall cap (`src/workers/java-runtime.ts`,
  `src/workers/sandbox.ts`).
- Learner `Solution` compiles standalone first; each test compiles Solution +
  generated `Test_*.java` with injected `CjTestBase` (checkEq/checkTrue/
  checkContains/checkLines/checkNear/checkThrows/capture).
- Sources needing collections carry their own `import java.util.*;`.

## Wrong-solution methodology

Behavioral near-misses only (compile-debug challenges keep the broken source
with `// BUG:`): `==` vs `.equals()`, integer division truncation, int overflow
before widening, `remove(int)` vs `remove(Integer)`, forward-removal skipping,
off-by-one bounds, `<` vs `<=` on tie contracts, constructor-chain omission,
missing empty-input guards, reset-in-wrong-loop, unbounded tick past cap.

## Verification record (all measured this session)

- Two-sided harness **109/109**: R passes its full suite, W fails ≥ 1 test
  (`scripts/content-authoring/verify-challenges-apc.mjs`, course-agnostic filter arg).
- Ledger mirror: `apc-solutions.mjs` 109 R + 109 W ↔ 109 challenges on disk.
- Loader schema + global-ID uniqueness: all-green after fixes.
- typecheck 0 · lint 0 errors · unit 184/184 · production build PASS ·
  E2E **36/36** (incl. accessibility + mobile specs).

## Known limitations

- Projects (multi-class builds) are represented by checkpoint+practice design
  tasks but the platform's project schema was not exercised in this phase.
- Full FRQ timing/format strategy is deferred to the planned follow-up course.
- Inheritance depth deliberately minimal per revised framework.

## Files

- Content: `src/content/tracks/ap-csa/**` (track.json + .vi, course.json + .vi,
  20 × module.json + lessons + practices, EN+VI).
- Authoring: `scripts/content-authoring/apc.py`, `apc_m1..m20.py`,
  `apc_finish_manifests.py`, `apc-solutions.mjs`, `verify-challenges-apc.mjs`.
- Docs: `docs/CURRICULUM-RESEARCH-AP-CSA.md`, this file.
- Regenerated: `src/lib/curriculum/mdx-map.ts`.
