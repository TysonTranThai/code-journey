# C# — Advanced — Course Spec

Date: 2026-09-17. Companion to `docs/CURRICULUM-RESEARCH-CSHARP-ADVANCED.md`
(every environment claim verified by probe). Track `csharp`, course
`csharp-advanced` ("C# — Nâng cao"), prerequisites `["csharp-intermediate"]`
(sibling-agent course; the course page renders the callout and tolerates a
not-yet-published prerequisite id — same precedent as cpp-advanced Phase 20).

## Philosophy

Not a longer Beginner course. Learners arrive able to build medium-sized
apps; we move them to understanding WHY the runtime behaves the way it does,
measuring before optimizing, reasoning about failure modes (races, leaks,
cancellation bugs, injection), and designing production systems. Every
challenge is executed in the real sandbox and two-sided verified.

## Baseline (verified)

C# 14 / .NET 10 (SDK 10.0.401), raw Roslyn csc, BCL-only (no NuGet),
loopback networking, in-process Roslyn APIs, unsafe + P/Invoke, no NativeAOT
toolchain. Shared-runtime change: C# compile lines gain the SDK Roslyn
assemblies as `-r:` references and `-unsafe` (≈ +0.1 s per compile, measured;
Beginner regression re-verified after the change).

## Modules (24) and coverage map

| # | id | Topic (brief §) | Projects / specials |
| - | -- | ---------------- | ------------------- |
| 1 | csa-language-semantics | execution model, value/ref semantics, boxing, null-state, overload & pattern-matching resolution (M1) | |
| 2 | csa-memory-object-model | stack/heap, structs, Span, ref returns, defensive copies (M2) | |
| 3 | csa-generics-type-system | variance, static abstracts, generic math, specialization concepts (M3) | **Checkpoint 1** |
| 4 | csa-delegates-closures | delegate representation, closures, allocation (M4) | Rule Engine |
| 5 | csa-reflection | Type/MethodInfo, caching, plugin discovery (M5) | Plugin Discovery |
| 6 | csa-attributes | custom attributes, metadata-driven validation (M6) | Validation Framework |
| 7 | csa-roslyn | syntax/semantic model, in-process compilation, analyzers (M7) | Custom Analyzer |
| 8 | csa-source-generators | incremental generators, post-init attributes (M8) | Generator from metadata |
| 9 | csa-expression-trees | building/compiling/translating (M9) | Mini Query Engine — **Checkpoint 2** |
| 10 | csa-advanced-async | state machines, ValueTask rules, IAsyncDisposable, timeouts (M10) | |
| 11 | csa-concurrency | Interlocked/Volatile, concurrent collections, deadlock forensics (M11) | |
| 12 | csa-parallel | Parallel.For/PLINQ, partitioning, measure-first (M12) | Parallel Data Engine |
| 13 | csa-channels | bounded channels, backpressure, graceful shutdown (M13) | Processing Pipeline — **Checkpoint 3** |
| 14 | csa-gc-memory | generations, finalization, leaks, ArrayPool, WeakReference (M14) | Allocation forensics |
| 15 | csa-performance | measure→profile→change→measure; allocation metrics (M15) | Optimize the slow app |
| 16 | csa-runtime-internals | IL, metadata, tiered compilation, virtual dispatch (M16) | PEReader inspection |
| 17 | csa-diagnostics | EventListener, EventCounters, crash forensics (M17) | Diagnose broken app — **Checkpoint 4** |
| 18 | csa-native-interop | P/Invoke, blittable, SafeHandle, pinning (M18) | Native Interop Wrapper |
| 19 | csa-deployment | NativeAOT/trimming/deployment models (M19) — conceptual + decision-verification (no AOT toolchain in sandbox) | |
| 20 | csa-networking | sockets, framing, Pipelines, backpressure (M20) | Async TCP Service — **Checkpoint 5** |
| 21 | csa-data-access | connection lifecycle, transactions, isolation simulations (M21) | Data Service (in-box store) |
| 22 | csa-distributed | retries/timeouts/idempotency/circuit-breaker simulations (M22) | — **Checkpoint 6** |
| 23 | csa-security | injection, deserialization, SSRF, secure randomness, threat models (M23) | — **Checkpoint 7** |
| 24 | csa-capstone | production architecture + milestones (M24) | Job Processing Platform — **Checkpoints 8 + 9** |

Scope cuts (research §4): NativeAOT/trimming conceptual only; no
BenchmarkDotNet/EF Core/dotnet-* tools — replaced by in-box, probed
equivalents; performance graded on deterministic allocation/GC counters,
never wall-clock alone.

## Shape

- ~105 lessons (≈4 per module + 9 checkpoint lessons), minutes 10–16.
- 24 practice sets (one per module, afterLesson-interleaved),
  3–4 challenges each ≈ 88 practice challenges + 9 checkpoint challenges +
  capstone milestones ≈ 100+ challenges. Target ≈ 200 total activities
  (within the 180–250 brief range; not inflated).
- Deliberate-practice levels stamped on every practice challenge;
  checkpoint challenges omit `level` (schema-legal).
- Debugging challenges ship broken-but-compiling code requiring diagnosis;
  prediction challenges ask for exact runtime behavior (boxing, closure
  capture, cancellation).
- VI: full sidecar/overlay parity per loader contract (tests/boilerplate EN).

## QA contract

1. `verify-challenges-csharp-advanced.mjs` — two-sided in the real sandbox,
   byte-identical test files via `buildCSharpTestFile` (reuse of the
   Beginner harness pattern with the advanced course dir + ledger).
2. Beginner regression: existing `verify-challenges-csharp.mjs` re-run
   (must stay ≥ its pre-change baseline; 0 wrongly-passing).
3. `validate-content.ts` extended additively with the new course; both
   locales load through the schema-validating loaders.
4. Unit/integration, typecheck, lint, production build, E2E critical path.
