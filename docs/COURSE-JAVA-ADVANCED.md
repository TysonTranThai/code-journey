# Course: Java — Advanced (java-advanced)

Date: 2026-09-14 · Status: **COMPLETE** (all content two-sided verified)

## Position

Track `java`, course 3 — the track's summit. Path: **java-beginner →
java-intermediate → java-advanced**. Prerequisites: both prior Java courses;
the course assumes Intermediate's contracts, generics, concurrency basics,
executors, and architecture material and goes *under* them.

Vietnamese: **Java — Nâng cao** (`track.vi.json` / `course.vi.json` overlays,
per-lesson `.vi.mdx`, per-challenge `.vi.json`).

## Toolchain (verified, not assumed)

| Component | Value |
|---|---|
| JDK (host + sandbox container) | 21 (`javac --release 21`), verified in the hardened Alpine container |
| New sandbox capability used | virtual threads (JEP 444, standard in 21), loopback sockets, real `/tmp` file I/O, reflection + runtime annotations |
| Shared-infrastructure change | **one additive prelude extension** in `src/workers/java-runtime.ts` (test snippet imports: `java.util.concurrent.*`, `java.net.*`, `java.nio.file.*`, `java.lang.annotation.*`, `java.lang.reflect.*`) — unused imports are legal Java, so no existing challenge is affected; verified by full Beginner/Intermediate harness re-runs |

What is *deliberately not taught as executable*: JFR/JMC, GC flags, `javap`
(no arbitrary JVM flags in the sandbox). Where the sandbox cannot observe a
mechanism directly, the lessons teach it through observable effects —
weak-reference retirement, inversion-count arithmetic as optimizer-proof
bytecode claims, and bounded inversion counts instead of bytecode dumps.

## Shape (verified from disk)

- **15 modules, 60 lessons** (45 teaching + 15 checkpoint lessons),
  **15 practice sets, 53 challenges** (38 practice + 15 checkpoint),
  ~32.0 h estimated (1121 min lessons + 800 min practice)
- Full **EN + VI parity**: 60/60 lesson MDX both locales, 53/53 challenge VI
  sidecars — validator reports `SYNC: EN/VI structures match`, 159 nodes load
  clean in both locales
- 13/15 modules follow the house rhythm (3 teaching lessons + practice set +
  checkpoint); Modules 10–11 add a second practice-style challenge set
  (files/sockets) because I/O and wire protocols need more reps

## Curriculum

| # | Module | Under-the-surface focus |
|---|---|---|
| 1 | The Object Model, Beneath the Surface | initialization order (JLS §12 executed), records/sealed as design tools, defensive copying, hostile-reviewer Session checkpoint |
| 2 | JVM Architecture & Class Loading | class literals silent vs `forName` loud, string-pool canonicalization, `<clinit>` tracing |
| 3 | The Java Memory Model | happens-by-construction (latch choreography, never timing), visibility, safe publication |
| 4 | Locks, CAS & Lock-Free | ReentrantLock fairness/tryLock, Conditions, ConcurrentHashMap compute, ABA |
| 5 | Executors & Virtual Threads | lifecycle rules, CF composition, JEP 444 executed at 10k-task fan-out, pinning, honest CPU-bound limits |
| 6 | Generics & the Type System | erasure vs reified arrays, wildcard capture, self-types, Class-token container |
| 7 | Reflection & the Mini-DI Container | metadata inventories, runtime annotations, recursive constructor injection + cycle detection |
| 8 | Memory, GC & Runtime Internals | reachability lattice observed live, boxed-identity trap, TTL cache (time/size/weak keys) |
| 9 | Performance Measurement | nanoTime/warmup/JIT threshold, median+epsilon harness, DCE defense |
| 10 | Files & NIO | path semantics, tree walking, JSONL journal (append/rotate/replay, torn tails) |
| 11 | Sockets & the Wire | loopback TCP, framing, timeouts, KV protocol served end-to-end |
| 12 | Async & Deadlines | injected executors, exception-combinators, deadline-scoped fan-out, raw-vs-wrapped TimeoutException |
| 13 | Security & Threat Modeling | canonical containment, SSRF allowlists, salted hashing, constant-time compare, STRIDE |
| 14 | Observability & Diagnosis | structured logs, percentiles vs averages, cardinality, incident triage with refutable hypotheses |
| 15 | Capstone: The Ledger Service | pluggable engines (memory + JSONL), byte-identical polymorphic reports, restart replay |

The original 24-module proposal was consolidated to 15 with documented
rationale (see `docs/CURRICULUM-RESEARCH-JAVA-ADVANCED.md`): every sandbox-
unobservable module (JFR, GC tuning, distributed systems lecture material) was
either folded into an observable sibling or cut rather than faked.

## QA — actual results

| Gate | Result |
|---|---|
| Two-sided challenge harness (`verify-challenges-javaa.mjs`) | **53/53** (reference passes; intentionally-wrong fails) |
| Beginner + Intermediate harnesses (prelude regression proof) | **59/59** and **60/60** |
| `validate-content.ts` | exit 0 — 15 modules, 60 lessons, 53 challenges, EN/VI sync, java linear path 165 lessons |
| Global id-collision sweep | 0 collisions across 2212 ids |
| mdx-map regen | 1392 imports |
| Typecheck / lint | clean / 0 errors (2 pre-existing warnings) |
| Unit + integration | **160/160** (incl. sandbox-isolation suite) |
| Production build | exit 0 (2078 static pages) |
| E2E (Playwright vs isolated production server) | **36/36** |

## Authoring pipeline

`scripts/content-authoring/javaa.py` (library) + `javaa_m1..m15.py` (content)
+ `javaa_course.py` (skeleton) + `javaa_wire.py` (module order) +
`javaa-advanced-solutions.mjs` (106→deduped 53+53 R/W ledger) +
`verify-challenges-javaa.mjs` (two-sided harness with id filter).

The harness caught ~10 real defects during this build, including: a
`double-unlock` IllegalMonitorStateException, the JLS §12.4.1
"reading a static field is active use" subtlety, weak-reference
clear-vs-enqueue asynchrony, `orTimeout`'s raw TimeoutException vs wrapped
task exceptions, and two behaviorally-equivalent "wrong" solutions
(convergence traps).

## Known limitations

- GC/JFR tools are taught conceptually; the sandbox cannot host them (no JVM
  flags). All executable alternatives are honest about this in-lesson.
- Structured concurrency (JEP 453) is preview in 21 — taught conceptually only.
- Python Beginner/Intermediate harnesses are currently broken by another
  agent's in-flight ledger refactor (unrelated to Java; not touched).
