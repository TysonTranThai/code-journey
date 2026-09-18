# Phase 21 — Course: Java — Advanced — SUMMARY

Date: 2026-09-14
Status: **COMPLETE**

## Course

Track `java` (existing), course `java-advanced` — **15 modules, 60 lessons**
(45 teaching + 15 checkpoint lessons), 15 practice sets, **53 challenges**
(38 practice + 15 checkpoint), ~32.0 h estimated (1121 min lessons +
800 min practice). Full EN + VI parity (60/60 lesson MDX both locales,
53/53 challenge VI sidecars, module/course overlays — validator: `SYNC:
EN/VI structures match`, 159 nodes load clean per locale).
Prerequisites: java-beginner + java-intermediate (both untouched). Track
path complete: java-beginner → java-intermediate → **java-advanced**.

The proposal's 24 modules were consolidated to 15 with documented rationale
(`docs/CURRICULUM-RESEARCH-JAVA-ADVANCED.md`): everything the sandbox cannot
execute (JFR/JMC, GC flags, `javap`) is taught through observable effects or
cut rather than faked. No Spring anywhere; the mini-DI container is built
from the JDK alone.

## Curriculum arc

Object model (JLS §12 initialization executed) → JVM/class loading →
Java Memory Model (latch-choreographed, never timing-based) → locks/CAS/ABA →
executors + virtual threads (JEP 444 verified in-sandbox at 10k fan-out) →
generics/erasure/Class tokens → reflection + mini-DI (cycle detection) →
memory/GC reachability observed live → performance measurement (median +
epsilon harness, DCE defense) → NIO + JSONL journal → loopback sockets +
KV protocol → async deadlines → security/threat modeling → observability/
incident triage → capstone: pluggable Ledger engines with byte-identical
polymorphic reports and restart replay.

## Toolchain & shared infrastructure

Zero new sandbox capabilities required: `--release 21` already runs virtual
threads, loopback sockets, temp-file I/O, and runtime-reflection
(host + hardened-container verified before authoring). **One additive
shared-infra change**: `src/workers/java-runtime.ts` test-prelude imports
(`java.util.concurrent.*`, `java.net.*`, `java.nio.file.*`,
`java.lang.annotation.*`, `java.lang.reflect.*`). Unused imports are legal
Java, so existing challenges are unaffected — proven by full re-runs:
Beginner harness **59/59**, Intermediate harness **60/60**.

## QA — actual results

| Gate | Result |
|---|---|
| Two-sided harness (`verify-challenges-javaa.mjs`) | **53/53** |
| validate-content.ts | exit 0 — 15 modules, 60 lessons, 53 challenges, EN/VI sync; java linear path 165 lessons |
| Global id-collision sweep | 0 collisions across 2212 ids |
| mdx-map regen | 1392 imports |
| Typecheck / lint | clean / 0 errors (2 pre-existing warnings) |
| Unit + integration | **160/160** (incl. sandbox-isolation suite; VI-content suite now passes — C++ agent fixed their MDX) |
| Production build | exit 0 (2078 static pages) |
| E2E (isolated production server, canonical specs) | **36/36** |

The harness caught ~10 real defects during authoring: a double-unlock
IllegalMonitorStateException, the JLS §12.4.1 active-use subtlety, weak-ref
clear-vs-enqueue asynchrony, `orTimeout`'s raw TimeoutException vs wrapped
task exceptions (now taught in Module 12), two arithmetic errors in my own
test expectations, and three behaviorally-equivalent "wrong" solutions
(convergence traps).

## Multi-agent safety

Beginner, Intermediate, Python, C++, and Web content untouched. Shared-file
edits: validator entry + track.json course reference (additive only),
mdx-map regenerated. The web track.json / Python ledger changes visible in
`git status` belong to other agents — preserved, not committed. Nothing
committed; no stray listeners; temp Playwright config deleted.

Known repo-level items (not mine): Python Beginner/Intermediate harnesses
temporarily broken by another agent's in-flight ledger refactor
(`py-solutions.mjs` missing exports); left untouched per the parallel-work
rule.
