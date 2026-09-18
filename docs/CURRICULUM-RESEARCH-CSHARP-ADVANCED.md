# C# — Advanced — Curriculum Research (probe-verified environment)

Date: 2026-09-17. Every capability claim below was probed in the actual Code
Journey sandbox container on 2026-09-17 (probes `probe.cs`/`probe2.cs`, run
under the production hardening flags). Language features are verified against
Microsoft Learn (fetched 2026-09-17). Nothing is asserted from memory alone.

## 1. Verified toolchain (inherited from C# — Beginner, re-verified today)

| Question | Verified answer | Evidence |
| --- | --- | --- |
| .NET SDK in sandbox | **10.0.401** (vendored linux-musl tarball) | `dotnet --list-sdks` in hardened container |
| Target framework | net10.0 (runtimeconfig rollForward LatestMinor) | CS_RUNTIMECONFIG_JSON / probe runs |
| C# language level | **14** (csc `-langversion:14`) | probe compiled and ran with it |
| C# 14 features available | extension members, null-conditional assignment, `field` backed properties, partial events/ctors, user-defined compound assignment, lambda param modifiers, span implicit conversions, `nameof` unbound generics | Microsoft Learn "history of C#" (2026-09-17) |
| Compiler model | raw Roslyn `csc.dll` + explicit `-r:` ref-pack refs | existing csharp-runtime.ts |
| Project system / msbuild | NOT usable in-sandbox (read-only rootfs, `--network none`) | hardening contract |
| NuGet | unavailable — BCL-only content | hardening contract |
| Limits | 512 MB, 0.5 CPU, pids 64, wall-clock ≤30 s (production run), ≤900 s batch QA harness | sandbox.ts |
| Read-only rootfs | yes; writes only to tmpfs `/tmp` (exec) and `/job` (noexec) | sandbox.ts |

## 2. NEW capability probes for the Advanced course (all run 2026-09-17)

Under the exact production hardening set (`--network none --read-only`,
tmpfs /tmp exec, memory 512m, cpus 0.5, pids 64, cap-drop ALL,
no-new-privileges, non-root):

| Capability | Verdict | Probe evidence |
| --- | --- | --- |
| `-unsafe` + pointers, `fixed`, `stackalloc` | **OK** (needs the `-unsafe` flag on the compile line) | `arr0=99 sum=14` |
| P/Invoke to libc (`[DllImport]`) | **OK** — native interop teachable in-sandbox | `pid=18` |
| **In-process Roslyn** (parse → compile → emit → load → invoke) | **OK** once the assembly-resolving handler points at `/usr/share/dotnet/sdk/*/Roslyn/bincore` | `from-roslyn`; emit ≈ 90–125 ms |
| Analyzer API (`DiagnosticAnalyzer` + `WithAnalyzers`) | **OK** | `diags=2 first=CJ0001` |
| **Incremental source generators** (`IIncrementalGenerator`, `ForAttributeWithMetadataName`, `RegisterPostInitializationOutput`) | **OK** — generated type resolved in the output compilation | `trees=2 hasHello=True symbolResolved=True`; the 3 output errors were my own snippet using bare `Attribute` (teaching moment: generated code must fully qualify types) |
| Loopback TCP (client+server, async, echo) | **OK** | `echo=42,43` |
| UDP loopback | **OK** | `udp=9,8` |
| `HttpClient` against loopback listener | **OK** | `json={"ok":true}` |
| `System.IO.Pipelines` | **OK** | `bytes=3` |
| `System.Threading.Channels` bounded + backpressure | **OK** | `sum=55 produced=10` |
| `EventListener` on `Microsoft-Windows-DotNETRuntime` (GC keyword) | **OK** — 60+ GC events observed | `gcEvents=63/64` |
| `Meter`/`MeterListener` (EventCounters-style) | **OK** | `received=12` |
| `PEReader`/`MetadataReader` IL+metadata inspection | **OK** (own assembly) | `firstOpcodeByte=114` |
| `Reflection.Emit` (`AssemblyBuilderAccess.Run`) | **OK** | `dyn(2,3)=5` |
| `Assembly.LoadFrom` from /tmp | **OK** (Roslyn-path resolution needed) | plug=42 pattern |
| `Expression.Compile()`, expression-tree APIs | **OK** | `sq(7)=49` |
| `where T : unmanaged` | **OK** | probe |
| Static abstract members in interfaces (generic math) | **OK** | `circle=circle area=3.14` |
| `WeakReference` + deterministic GC | **OK** with the helper-method pattern — see §3 | `dead=True spins=0` after fix |
| Crypto (`RandomNumberGenerator`, `SHA256`) | **OK** | `sha256len=32` |

## 3. Runtime findings that shaped the curriculum (all reproduced, not assumed)

1. **Tier0/QuickJIT liveness**: a `WeakReference` created in the same
   method that also holds the last strong reference stays alive until the
   method returns under the sandbox's default (quick) JIT — the classic
   `new WeakReference(new object())` demo is unreliable. The reliable
   pattern: return the `WeakReference` from a non-inlined helper, collect
   in the caller. Encoded in the GC module challenges (both arms verified).
2. **Roslyn loading**: `Microsoft.CodeAnalysis.dll` (5.9.0) is NOT in the
   default TPA list. Challenges that compile code in-process MUST register
   `AssemblyLoadContext.Default.Resolving` pointing at the SDK's Roslyn
   bincore dir, or face `FileNotFoundException` at first `CSharpCompilation`
   use. This becomes the Module 7 lesson content itself.
3. **Generated-code hygiene**: a generator's emitted snippet that uses bare
   type names (`Attribute`) fails the OUTPUT compilation with CS0246 —
   generated code must fully qualify types (verified: 3 output errors).
4. **`GeneratorDriver` immutability**: `RunGeneratorsAndUpdateCompilation`
   returns the driver; `GetRunResult()` must be called on the RETURNED
   driver. (Probe initially printed trees=0 on the un-run driver.)
5. **`-unsafe` semantics**: the flag must be on the csc command line;
   pointer ops outside unsafe contexts are CS0214 regardless.
6. **Instrument.MeterName**: the correct API surface is `inst.Meter.Name`
   (probe compile error caught this).
7. Compile cost with Roslyn refs appended: ≈ +0.1 s per compile
   (0.42–0.56 s basic vs 0.51–0.58 s full) — acceptable for the shared
   runtime change.

## 4. Teaching boundaries (scope cuts, decided from the probes)

- **NativeAOT / trimming**: cannot compile or measure in-sandbox (no
  msbuild, no crossgen/AOT toolchain in the image). Taught conceptually
  with reflection-limit reasoning + deployment-model decision exercises;
  no fake "AOT build" challenges.
- **BenchmarkDotNet**: unavailable (NuGet offline). Course builds its own
  deterministic measurement methodology: `Stopwatch` + multi-rep medians +
  `GC.GetAllocatedBytesForCurrentThread()` deltas + `GC.CollectionCount`
  deltas. Allocation-counting exercises are graded on the counters, not on
  wall-clock (0.5 CPU is too noisy for latency grading).
- **EF Core**: unavailable (NuGet offline). Data-access module teaches
  ADO.NET against in-box primitives with an embedded (file-based)
  database-shaped store, plus query-translation concepts via expression
  trees. Isolation levels/concurrency taught through deterministic
  simulations of the same failure classes.
- **dotnet-counters / dotnet-trace / dotnet-dump**: not in the image and
  unverifiable under hardening. Observability taught via in-process
  `EventListener`, `EventSource`, `Meter`, and `PEReader` — all probed.
- **Unsafe native memory**: P/Invoke verified; lesson content stays on
  libc-style calls the image actually links, `SafeHandle` discipline, and
  pinning rules — no native compilation.

## 5. C# 14 / .NET 10 baseline decisions

- Baseline is C# 14 on .NET 10 (SDK 10.0.401) — verified in §1/§2. The
  course may USE C# 14 features (field-backed properties, extension
  members, user-defined compound assignment) and must teach the C# 13
  `System.Threading.Lock` type (in-box) where lock semantics are discussed.
- Raw csc has no implicit usings (probe CS2007 from the Beginner research):
  every boilerplate carries explicit `using` lines — kept, pedagogically
  visible dependencies.

## 6. Sources

- Probe runs in the production sandbox container, 2026-09-17 (§2, §3).
- Microsoft Learn — "The history of C#" (C# 13/14 feature lists), fetched
  2026-09-17.
- .NET release metadata: SDK 10.0.401 (per Beginner research, channel
  manifest); verified in-container via `dotnet --list-sdks` 2026-09-17.
- Existing platform contract: `src/workers/csharp-runtime.ts`,
  `src/workers/sandbox.ts`, `docs/CURRICULUM-RESEARCH-CSHARP-BEGINNER.md`.
