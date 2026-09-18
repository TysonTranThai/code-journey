# Phase 19 — Course: Java — Intermediate — SUMMARY

Date: 2026-09-14
Status: **COMPLETE**

## Course

Track `java` (existing), course `java-intermediate` — **15 modules, 58
lessons** (43 teaching + 15 checkpoint lessons), 15 practice sets,
**60 challenges** (45 practice + 15 checkpoint), ~23.4 h estimated
(806 min lessons + 600 min practice). Full EN + VI parity (58/58 lesson MDX
both locales, 60/60 challenge VI sidecars, module/course overlays).
Prerequisite: java-beginner (untouched). Track path: java-beginner →
java-intermediate → java-advanced (future).

Proposal's 21 modules consolidated to 15 (merge rationale in
`docs/CURRICULUM-RESEARCH-JAVA-INTERMEDIATE.md`); practice-first rule kept —
every module ends in a graded checkpoint.

## Scope

All-Java engineering transition: equality/immutability contracts, SOLID +
dependency inversion, generics with wildcards/PECS, advanced collections,
Collectors, exception architecture, testing depth (doubles, injectable
clocks), concurrency fundamentals, async composition, persistence/repository
pattern, layered architecture + hand-rolled DI, intermediate algorithms,
clean code, and a layered Expense-Tracker capstone. No Spring (explicit
boundary); honest in-lesson treatment of sandbox boundaries (file I/O and
JDBC taught via injectable in-memory equivalents).

## Infrastructure

Zero new sandbox infrastructure. Reused Phase 18's `java-runtime.ts`
(one JVM per test, `--release 21`). New authoring-only artifacts:
`scripts/content-authoring/javi.py` (cloned from `javb.py`: course path,
`javi-` id prefix, separate ledger), `javi_m1..m15.py`, `javi_wire.py`
(surgical shared-file edits only), `verify-challenges-javi.mjs`,
`javi-intermediate-solutions.mjs` (exactly 60 R + 60 W pairs, deduped).

## QA (actual results)

| Gate | Result |
|---|---|
| Two-sided harness | **60/60 OK** |
| validate-content.ts | exit 0 — 15 modules, 58 lessons, EN/VI sync, 164 nodes/locale |
| mdx-map regen | 1266 imports |
| Typecheck / lint | clean / clean |
| Unit + integration | **150/150** (VI-content suite externally blocked, below) |
| Production build | exit 0 (`next build`, external file excluded then map restored) |
| E2E (my prod server, :3456) | **36/36** |
| git diff --check | clean |

The harness caught ~10 real defects during authoring, including
return-inside-try vs `finally` ordering, `Objects.equals` array identity,
behaviorally-equivalent "wrong" solutions (convergence trap), and two wrong
arithmetic expectations in my own tests.

## Multi-agent safety

- Java Beginner, Python, C++ files untouched; shared-file edits additive
  only (`track.json` course append, validator COURSE_TRACKS entry).
- Cross-course id collisions fixed by renaming **my** nodes only:
  `java-checkpoint-*` → `javi-checkpoint-*` (15 lessons + files + refs),
  `repository-pattern` → `javi-repository-pattern`,
  `capstone-brief` → `javi-capstone-brief` (python-intermediate owns the
  originals). Global sweep: 914 ids, 0 collisions remaining.
- Nothing committed; everything left in the working tree for review.

## Known external blocker (NOT this phase's work)

The C++ Advanced agent's untracked
`cpp-advanced/modules/architecture-production/lessons/events-and-config{,.vi}.mdx`
fail MDX compilation (unescaped `{...}` in prose). Until fixed upstream this
breaks `pnpm build` and the `curriculum-vi-content` unit suite for the whole
repo. Left untouched per the parallel-work rule; verified my own 240 MDX
files compile clean and the build passes with only those two files excluded.

## Remaining work

Intentionally none for this phase. Repo-level leftovers (prettier drift,
large uncommitted tree) remain a user decision, as recorded in STATE.md.
