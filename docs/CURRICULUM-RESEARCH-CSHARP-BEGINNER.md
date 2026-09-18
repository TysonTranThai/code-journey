# C# — Beginner — Curriculum Research (verified environment)

Date: 2026-09-16. Every claim below was probed in the actual Code Journey sandbox
or verified against a primary source the same day. No behavior is asserted from
memory alone.

## 1. Toolchain (verified, not assumed)

| Question | Verified answer | Evidence |
| --- | --- | --- |
| .NET SDK in sandbox | **10.0.401** (vendored linux-musl tarball, per-TARGETARCH) | `dotnet --list-sdks` inside hardened container → `10.0.401 [/usr/share/dotnet/sdk]` |
| Version source | `https://builds.dotnet.microsoft.com/dotnet/release-metadata/10.0/releases.json` — `latest-sdk: 10.0.401`, active support | fetched 2026-09-16 |
| Tarball integrity | x64 + arm64 SHA512 pinned in `docker/Dockerfile.sandbox` (from the channel manifest) | build enforces `sha512sum -c` |
| Globalization | Alpine `icu-libs=76.1-r1` added; runtime now has real ICU | without it dotnet FailFasts ("Couldn't find a valid ICU package") — probed |
| Base image | node:22.17.0-alpine3.22 (arm64 host) | Dockerfile |
| Compile model | **raw Roslyn**: `dotnet /usr/share/dotnet/sdk/*/Roslyn/bincore/csc.dll` with explicit `-r:` refs from `packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0/*.dll` | probe: full compile+run in hardened container |
| Runtime model | framework-dependent dll + 2-line `*.runtimeconfig.json` (`tfm net10.0`, `rollForward LatestMinor`, framework `Microsoft.NETCore.App 10.0.0`) | probe: "hello from csharp", file I/O, threads all pass |
| Project system / `dotnet build` | **NOT usable in-sandbox** (read-only rootfs, no network, `DOTNET_CLI_HOME=/tmp`) — irrelevant: grading never uses msbuild | hardening flags identical to C/C++/Java paths |
| NuGet | **unavailable** (sandbox is `--network none`) — course uses BCL only; JSON via `System.Text.Json` (in-box) | hardening contract |
| Timing (probed, 0.5 CPU / 512 MB) | csc compile ≈ 0.5 s; dotnet run ≈ 0.2 s per test | `time` in probe run |
| Threads / async | `Parallel.For`, `lock`, `ManualResetEvent`, `ThreadPool` all verified in-sandbox | probe run |
| File I/O | `File.WriteAllText/ReadAllText` under `/tmp` verified | probe run |

Sandbox hardening for every C# run is byte-identical to the other compiled
languages: `--network none --read-only`, tmpfs `/tmp` (exec) + `/job` (noexec),
512 MB memory (no swap), 0.5 CPU, pids 64, cap-drop ALL, no-new-privileges,
non-root user `sandbox`.

## 2. Language level

C# 14 on .NET 10 (SDK 10.0.401). The course targets C# 14. Raw csc has **no
implicit usings** (`-implicitusings` is an MSBuild property, not a csc flag —
verified by probe CS2007): challenge boilerplates therefore carry explicit
`using` lines, which is also pedagogically honest — learners see the
namespaces they depend on.

## 3. Grading contract (csharp-runtime.ts)

- Solution is ONE file `Solution.cs`; each test is compiled **together** with
  it into a single assembly; entry point pinned with csc `-main:CjTest`, so a
  learner-written `Main` can never take over (no CS0017).
- Learner submissions = challenge `boilerplate` + their code; boilerplate
  carries the `using` lines and any helper declarations the tests reference.
- Syntax gate: solution compiles alone first (as a library, so a learner Main
  is legal there); failure → verdict "error" with the compiler output.
- Markers: `__TEST_RESULT__ <name> status=N` — the SAME protocol execute.ts
  already parses for every other language.
- Roslyn diagnostics print on **stdout** (verified): both streams are captured
  into the failure-hint channel.
- Graded entry convention: `public class Solution` static methods (early
  modules), instance types (OOP modules), or `static void program()` captured
  via `Cj.Capture(...)` for output challenges.

Smoke test (`scripts/content-authoring/_smoke-csharp.mts`): good solution
passes all 3 tests; wrong solution fails all graded tests with
"expected 5, got -1"; syntax-error solution yields **zero markers** + exit 1
with compiler output. All three arms verified in-container.

## 4. Sources

- .NET release metadata (SDK/runtime versions, tarball hashes): builds.dotnet.microsoft.com channel manifests, fetched 2026-09-16.
- Roslyn compiler options: probed live in-sandbox (flag support verified by attempting it).
- C# 14 language level: SDK's csc accepts `-langversion:14` (probe compiled with it).
- Alpine packages: icu-libs 76.1-r1 (pinned, from v3.22 repos).

## 5. Curriculum decisions

- Beginner scope follows the phase brief: fundamentals first — no ASP.NET,
  Unity, DI containers, or databases. Files/JSON use the in-box BCL only.
- Async module stays introductory (`Task`, `async`/`await`, `Task.WhenAll`,
  basic `CancellationToken`) — no advanced concurrency.
- Practice-heavy: every module = lessons + practice challenge sets + a
  checkpoint; every challenge two-sided verified (R passes all tests, W fails
  ≥1 test) in the real sandbox.
- EN + VI synchronized at authoring time (same ids, same structure; the
  content validator enforces it).
