# C# — Intermediate — Curriculum Research (verified environment)

Date: 2026-09-17. Every environment claim below was re-probed in the actual Code
Journey sandbox this phase (a 15-point capability matrix compiled with the real
harness toolchain and executed in the hardened container). The toolchain itself
was established by the C# Beginner phase
(`docs/CURRICULUM-RESEARCH-CSHARP-BEGINNER.md`) and re-confirmed unchanged.

## 1. Toolchain (re-verified this phase)

| Question | Verified answer | Evidence |
| --- | --- | --- |
| .NET SDK in sandbox | **10.0.401** (vendored linux-musl tarball, sha512-pinned in `docker/Dockerfile.sandbox`) | probe compile+run in the hardened container, this phase |
| Language level | **C# 14** (`-langversion:14` accepted by the vendored csc) | probe compiled with it |
| Compile model | raw Roslyn `csc.dll` 5.9.0-1.26423.113 via `dotnet <sdk>/Roslyn/bincore/csc.dll`, explicit `-r:` refs from `packs/Microsoft.NETCore.App.Ref/*/ref/net10.0/*.dll` | probe |
| Runtime model | framework-dependent dll + minimal `*.runtimeconfig.json` (tfm net10.0, rollForward LatestMinor) | probe |
| Project system / `dotnet build` | NOT usable in-sandbox (read-only rootfs, no network) — grading never uses msbuild | hardening contract |
| NuGet | **unavailable** (`--network none`) — BCL only | hardening contract |
| Threads / sync primitives | `Thread`, `Interlocked`, `Monitor` (`lock`), `SemaphoreSlim`, `ManualResetEvent` all verified in-sandbox | probe: 8-thread Interlocked counter == 8000 |
| Concurrent collections | `ConcurrentDictionary.AddOrUpdate`, `ConcurrentQueue` verified | probe |
| Async | `async`/`await`, `Task.WhenAll`, `CancellationTokenSource` timeout cancellation, `await foreach` over `IAsyncEnumerable<T>` (async streams) verified | probe |
| HttpClient — deterministic | `HttpClient` over a **literal `HttpMessageHandler`** returns canned responses with zero network: status, headers, JSON body all controllable per test | probe (this is the key Intermediate capability — real HTTP API shape, no socket) |
| System.Text.Json | serialize/deserialize, `JsonNamingPolicy.CamelCase`, `JsonException` on malformed input verified | probe |
| LINQ breadth | `GroupJoin`, `Aggregate`, `Zip`, `Chunk`, full query/composition verified | probe |
| Records + pattern matching | `record` types, property patterns with relational patterns in switch expressions verified | probe |
| File I/O under /tmp | `File.WriteAllText/ReadAllText` + JSON round-trip verified | probe |
| Variance | `IEnumerable<object> xs = new List<string>()` (covariance) verified | probe |
| Spans | `ReadOnlySpan<char>` slicing verified | probe |
| Culture-invariant formatting | `ToString("F1", CultureInfo.InvariantCulture)` verified (icu-libs present) | probe |

Sandbox hardening for every C# run is byte-identical to the other compiled
languages: `--network none --read-only`, tmpfs `/tmp` (exec) + `/job` (noexec),
512 MB memory (no swap), 0.5 CPU, pids 64, cap-drop ALL, no-new-privileges,
non-root user `sandbox`. Timing (Beginner probe, re-confirmed): csc compile
≈ 0.5 s + run ≈ 0.2 s per test at 512 MB / 0.5 CPU — the 120 s wall-clock
timeout allows multi-threaded and async challenges comfortably.

## 2. Grading contract (unchanged, consumed as-is)

- Solution is ONE file `Solution.cs` (`src/workers/csharp-runtime.ts`); each
  test compiles together with it into a single assembly; entry pinned with
  `-main:CjTest`; boilerplate + learner code form the submission; syntax gate
  first; markers `__TEST_RESULT__ <name> status=N`.
- `Cj` harness: `Cj.True/False/Eq/Near/Contains/Capture` — Intermediate tests
  use the same vocabulary; async tests `await` inside an `async` local
  function invoked with `.GetAwaiter().GetResult()` in the graded body (probed
  pattern), thread tests `Join()` before asserting.
- Raw csc has no implicit usings: boilerplates carry explicit `using` lines
  (pedagogically honest — learners see the namespaces they depend on).

## 3. What the sandbox CANNOT do (taught around honestly)

| Missing capability | Consequence for the course | The honest substitute |
| --- | --- | --- |
| NuGet / network | No xUnit/NUnit/Moq/NSubstitute, no EF Core, no ASP.NET Core, no DI containers, no real HTTP endpoints | Hand-rolled test-runner exercises (learners BUILD a mini xUnit — that's how test frameworks work); in-memory repository + hand-wired composition root (that's what a container does); `HttpMessageHandler` stubs (that's exactly how production code tests HttpClient); ADO.NET-shaped `IDbStore` interfaces; SQL taught as parameterized SQL text graded by inspection-behavior |
| Real database | No Postgres/SQLite driver | In-memory store with transaction semantics; SQL-injection defense graded as parameterization behavior (concatenated input breaks the test, parameterized passes) |
| `dotnet build`/project system | No multi-file projects, no csproj concepts graded | Single-TU grading as in Beginner; project structure taught prose-side |
| Debugger/profilers | No BenchmarkDotNet | Measurement by `Stopwatch` experiments with fixed workloads (relative comparisons only — stated in-lesson), allocation reasoning via behavior |

## 4. Version-sensitivity notes (verified, not assumed)

- `Chunk`, `Zip` (3-arg selector), `DistinctBy`, index/range patterns — .NET 6+
  LINQ, all present in the net10.0 ref pack (probe).
- `required` members, collection expressions `[1, 2, 3]`, primary constructors
  — C# 12+ features accepted by C# 14 csc; used sparingly and only where they
  aid readability (records already cover most modeling needs).
- `IAsyncEnumerable<T>` + `await foreach` — verified working in-sandbox.
- `CancellationTokenSource(TimeSpan)` ctor — verified.
- `Interlocked` on `long`, `SemaphoreSlim.WaitAsync` — verified available.
- English-only culture outputs in graded tests: culture-invariant formatting
  used in tests where number/date formatting could vary (probe confirmed ICU
  present, but tests pin `CultureInfo.InvariantCulture` for determinism).

## 5. Beginner boundary (what csb-* already taught — do not reteach)

Per `src/content/tracks/csharp/courses/csharp-beginner` (21 modules, read
2026-09-17): syntax/types, operators, control flow, methods/overloads (basic
ref/out exposure), strings/DateTime, arrays, List/Dictionary basics, classes/
records/inheritance/interfaces basics, generics basics (`List<T>`, one
`Repo<T>` style exercise), exceptions/try-catch, file I/O, LINQ **intro**
(Where/Select/OrderBy/Sum), delegates/Func/Action/lambdas/closures intro
(one event-bus mini), unit-test mindset intro, CLI capstone (JSON files,
LINQ statements), git workflow, basic algorithms.

## 6. Advanced boundary (reserved for csharp-advanced — kept OUT)

CLR/JIT/GC internals, Span<T>/Memory<T> deep dive, lock-free programming,
Channels, TPL Dataflow, expression trees, Roslyn/source generators, unsafe
code, P/Invoke, NativeAOT, distributed systems, advanced performance
engineering, ASP.NET Core internals.

## 7. Sources

- Probes in the real sandbox (this phase; see §1) — primary evidence.
- Beginner-phase research: `docs/CURRICULUM-RESEARCH-CSHARP-BEGINNER.md`
  (SDK version sourcing, release-metadata channel, icu-libs pin).
- Microsoft Learn C# language reference / .NET API surface (System.Linq,
  System.Text.Json, System.Net.Http, System.Threading, System.Threading.Tasks)
  — feature availability cross-checked against the net10.0 ref pack present in
  the image (the pack IS the API surface, verified by compile).
- Exercism C# practice catalog — exercise-shape inspiration (transforming,
  complex-requirements, debugging tracks), original content only.

## 8. Curriculum decisions

- 22 modules, ~64 lessons (20 checkpoint lessons), ~38 practice sets,
  ~150 challenges — Intermediate band of the 20–24 module brief, sized like
  the C Intermediate (16m/64l/84c) and Web Intermediate (13m/80l/181c)
  siblings.
- Practice-first: every module = lessons + practice sets anchored
  `afterLesson` + checkpoint challenge; deliberate-practice levels stamped.
- Deterministic grading everywhere: fixed inputs in tests, literal handlers
  for HTTP, seeded/fixed schedules for async/concurrency (barriers + events,
  never timing races), culture-invariant formatting.
- Concurrency graded via join/barrier choreography (probed pattern), never
  via wall-clock assumptions.
- No fabricated support: EF Core, DI containers, xUnit, ASP.NET, real
  network, real databases — all absent from graded code, each replaced by a
  hand-built equivalent that teaches the mechanism under the framework name.
