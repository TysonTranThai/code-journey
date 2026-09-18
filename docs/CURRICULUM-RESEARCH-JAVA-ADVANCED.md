# Curriculum Research — Java — Advanced

Date: 2026-09-14 · Authoring agent: Java — Advanced (Phase 20)

## What was actually inspected (repository evidence, not assumptions)

| Evidence | Finding | Consequence for the course |
|---|---|---|
| `src/workers/java-runtime.ts` | `JAVA_RELEASE_FLAG = "--release 21"`; test prelude imports (now extended, Phase 20) `java.util.concurrent(.atomic/.locks)`, `java.net`, `java.nio.file`, `java.lang.annotation`, `java.lang.reflect`, `java.io` on-demand | Language baseline is **Java 21 exactly**. Every challenge must compile under `--release 21`; no preview features. |
| In-container smoke test (this phase, `codejourney-sandbox:latest`, full hardening: `--network none`, read-only rootfs, 16 MB tmpfs `/tmp`, `--pids-limit`, non-root) | `Executors.newVirtualThreadPerTaskExecutor()` works (JEP 444, standard in 21); `Thread.ofVirtual()` factory works; real tmpfs file I/O works; **loopback TCP sockets work** (`ServerSocket(0, loopback)` + client round-trip); reflection + RUNTIME annotations work; `Thread.currentThread()` prints `Thread` (no per-thread type in `toString`) | The course can honestly teach: virtual threads, structured task execution, lock-free/atomics, reflection/annotation systems, real file processing, **real loopback socket programming**. It must NOT claim: external HTTP (no egress), JFR/async-profiler (no tooling), jdwp (no debug agent), JPMS module-path runs (harness compiles unnamed-package single TUs). |
| Sandbox caps (`src/workers/sandbox.ts`) | 30 s wall ceiling, output caps, memory ceilings, fork-bomb containment | Timing-based challenges must be deterministic by *design* (injectable clocks/schedulers), never by wall-clock measurement. |
| `java-beginner`, `java-intermediate` on disk (Phases 18–19) | Beginner: fundamentals→collections→records→JUnified basics→capstone ledger. Intermediate: contracts→SOLID→generics/PECS→Collectors→exception architecture→testing depth→executors/Futures→CompletableFuture→repositories→layered architecture→algorithms→capstone | Advanced assumes BOTH and does not reteach them. The Intermediate exit point (executors + CF + repository + layering) is the Advanced entry point (JMM, lock-free, virtual threads, distribution). |

## Sources consulted (topic-level, current as of 2026-09)

- **JEP 444** (Virtual Threads — final in JDK 21) and JEP 453 (Structured Concurrency — *preview* in 21, therefore taught conceptually, not executed): virtual-thread scheduling, pinning (synchronized blocks), carrier threads. dev.java/learn "virtual threads" guidance.
- **Java Language Specification (Java SE 21)**: initialization order (§12.2–12.4), definite assignment, records (§8.10), sealed classes (§8.1.1.2), pattern matching for switch (JEP 441, final in 21).
- **JVM Specification (Java SE 21)**: class-file structure, constant pool, method bytecode, `invokedynamic`, stack-based operand model — grounds the bytecode-inspection lessons (`javap` is demonstrated in lesson prose since the sandbox has no shell, but the *observable* behaviors are verified by executing Java).
- **Java Memory Model (JLS §17.4)**: happens-before, `volatile` semantics, safe publication, final-field semantics (§17.5). Doug Lea's "The JSR-133 Cookbook" for the cookbook-style explanations.
- **java.util.concurrent docs (JDK 21 API)**: `ReentrantLock` fairness, `Condition`, `Semaphore`, `CountDownLatch`, `CompletableFuture` (JDK 9+ timeout/delay methods), `ConcurrentHashMap` compute atomics, `AtomicReference.compareAndSet` (CAS/ABA), `VarHandle` (JDK 9+).
- **GC references**: Oracle "Garbage Collector Ergonomics", "The Garbage-First Garbage Collector" (Javaone/Oracle technical paper), JEP 333 (ZGC) / JEP 379 (Shenandoah) status notes. All GC content is conceptual + diagnosable-in-code (reference reachability, `WeakReference`, `Cleaner`), because GC tunables are not observable in the sandbox.
- **Java Object Layout (JOL)** concept: object header/mark-word ideas taught conceptually; JOL itself is not on the classpath (verified: JDK-only sandbox), so no false claims.
- **Security**: OWASP Java-specific guidance (deserialization, SSRF, path traversal), `MessageDigest`/`SecureRandom`/PBKDF2 (`javax.crypto`) for password storage, `SecureRandom` vs `Random` (predictability), TLS/mTLS concepts (JSSE reference guide) — taught via safe in-process exercises.
- **NIO.2**: `Files`, `Path`, `FileChannel`, `ByteBuffer`, `MappedByteBuffer` (`FileChannel.map` — verified executable on tmpfs), `StandardOpenOption`, `Charset` handling.
- **Socket/HTTP**: JDK's `HttpClient` cannot reach external hosts in the sandbox (no egress, verified) — networking is taught with real **loopback** sockets (verified working) plus protocol-level HTTP parsing over loopback; external API behavior is concept-only and labeled.

## Version/feature honesty table

| Feature | In course? | Why |
|---|---|---|
| Virtual threads (JEP 444) | YES — executed | Final in 21, verified in-container |
| Pattern matching for switch (JEP 441) | YES — executed | Final in 21 |
| Record patterns (JEP 440) | YES — executed | Final in 21 |
| Structured concurrency (JEP 453) | CONCEPT ONLY | Preview in 21 — not enabled (`--enable-preview` is not set); taught from the JEP text, never "executed" |
| String templates | NO | Never standardized; withdrawn (JEP 465 preview→withdrawn) |
| `javap`/JFR/JMC/jdwp tooling | PROSE ONLY | No shell/tooling in sandbox; behaviors taught via executable Java equivalents |
| JPMS (`module-info`) | CONCEPT ONLY | Harness compiles unnamed-package TUs; module system taught conceptually with real classpath behavior |
| External HTTP, real DB | SIMULATED | No egress; teach protocol over loopback + in-memory persistence engines |
| Benchmark numbers | NONE fabricated | Performance lessons teach methodology (warmup, JIT, measurement noise) and use relative assertions; no hardware-specific claims |

## Curriculum decision: 20 modules (proposal had 24)

Consolidation rationale (keeping the proposal's full topic coverage):

- Proposal M1 (object model) + M3 (bytecode/compilation) stay separate — both are substantial.
- Proposal M5 (reflection) + M6 (annotations) merged into **one metaprogramming module with a DI-container mini-build** — annotations without reflection is a fragment; the mini-build needs both at once.
- Proposal M8 (lock-free) folded into **M7 (advanced concurrency)** as its CAS/ABA submodule — JMM-first then CAS is one coherent arc.
- Proposal M10 (virtual threads) + M9 (advanced async/CF) merged into **one modern-concurrency module** — CF composition then VT scale-out is the natural teaching sequence.
- Proposal M11 (GC) + M12 (performance engineering) merged into **one memory & performance module** — measurement discipline frames the GC material.
- Proposal M14 (networking) + M15 (high-performance I/O) merged into **one I/O & networking module** (both are NIO/ByteBuffer/socket arcs over the same verified primitives).
- Proposal M20 (advanced testing) + M23 (debugging/incident) merged into **one verification & diagnosis module** — flake diagnosis IS incident practice at this level.
- Proposal M22 (production engineering) + M19 (security) merged into **one production & security module** (secrets, least privilege, and observability are one operational story).
- Kept distinct: M2 JVM architecture, M4 advanced generics, M13 advanced structures/algorithms, M16 persistence, M17 distributed concepts, M18 architecture patterns, M21 capstone — these are irreplaceable centers of gravity.

Final: **20 modules × (3 teaching lessons + 1 practice set + 1 checkpoint) = 60 lessons, 20 practice sets, 40 practice challenges + 20 checkpoint challenges = 60 challenges.**

## Practice-first rule (unchanged from Phases 18–19)

Every teaching lesson ends in runnable practice; every module ends in a graded
checkpoint challenge that is diagnosed/repaired behavior, not definition
recall. Every challenge ships R (reference passes) + W (behavioral near-miss
that must fail) — the two-sided rule that caught ~25 content defects across
Phases 18–19.
