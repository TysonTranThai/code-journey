/**
 * C# execution support for the sandbox (C# — Beginner and Advanced courses).
 *
 * Mirrors the C/C++/Java job contracts: the student solution and the
 * challenge's test snippets are written into /job as heredoc data (never
 * interpreted by sh), then each test is compiled and run as its own process
 * and exits 0 (pass) or non-zero (fail). The marker-line protocol is the
 * SAME one execute.ts already parses (`__TEST_RESULT__ <name> status=N`).
 *
 * C# test contract (challenge authoring):
 *  - The solution is one file `Solution.cs` compiled TOGETHER with each test
 *    into a single assembly (single-translation-unit semantics, like the C
 *    `#include "solution.c"` contract): solution types are visible to the
 *    test, and helper types may be declared in either file. A learner-written
 *    `Main` never takes over: every test file's entry class `CjTest` is pinned
 *    as the entry point with csc's `-main:` flag (without it, two Mains would
 *    be CS0017).
 *  - The graded entry convention (same as the Java runtime): challenges grade
 *    named public members of `public class Solution` (static methods for
 *    early modules; instance types in the OOP modules), or `static void
 *    program()` captured via `Cj.Capture(() => Solution.program())` for
 *    output challenges.
 *  - The solution is syntax-gated first (library compile — a Main inside a
 *    library is legal, so the gate never CS0017s): a solution that does not
 *    compile produces NO markers, so execute.ts maps the job to verdict
 *    "error" with the compiler output — an educational compile error, not N
 *    confusing per-test failures.
 *
 * Toolchain (probed 2026-09-16 under FULL sandbox hardening — see
 * docs/CURRICULUM-RESEARCH-CSHARP-BEGINNER.md):
 *  - .NET SDK 10.0.401 (linux-musl, per-TARGETARCH) at /usr/share/dotnet,
 *    Alpine icu-libs 76.1 for faithful globalization; both pinned in
 *    docker/Dockerfile.sandbox.
 *  - Raw Roslyn `csc.dll` invoked via `dotnet <sdk>/Roslyn/bincore/csc.dll`
 *    with explicit `-r:` references from the NETCore.App REF pack — no
 *    project/obj/restore, so the read-only-rootfs + tmpfs sandbox model is
 *    unchanged from C/C++/Java.
 *  - Apps run framework-dependent with a minimal `*.runtimeconfig.json`
 *    (rollForward LatestMinor) placed next to the compiled dll.
 *  - Probed: ~0.5 s compile + ~0.2 s run per test at 512 MB / 0.5 CPU;
 *    threads/Parallel/ThreadPool and file I/O under /tmp all work.
 *
 * Exported as raw module text (same pattern as the other runtimes) so the
 * worker and the content QA harness cannot drift.
 */

import { sanitizeTestName } from "./sanitize-name";

/**
 * The C# harness injected at the top of every generated test file. Defined
 * once here so the sandbox worker and the QA harness build byte-identical
 * test files. One static class `Cj` (helper) — the per-test entry class
 * `CjTest` is added by buildCSharpTestFile.
 */
export const CS_TEST_HARNESS = String.raw`// Code Journey C# test harness (injected; do not modify).
using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Collections.Immutable;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Linq.Expressions;
using System.Net;
using System.Net.Sockets;
using System.Numerics;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Channels;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

// Runs when the test assembly loads — before any JIT token resolution, so
// compiler-API tests can bind the SDK's Roslyn assemblies at runtime.
internal static class CjModuleInit
{
    [System.Runtime.CompilerServices.ModuleInitializer]
    internal static void Run() => Cj.InitRoslynResolver();
}

static class Cj
{
    // Roslyn-at-runtime resolver: compiler-API challenges compile against the
    // SDK's Roslyn assemblies but execute outside that directory, so the
    // framework resolver cannot find them. Probe the SDK layout once and
    // satisfy unresolved Roslyn loads from it. Additive for Beginner: never
    // fires unless a test actually binds Microsoft.CodeAnalysis.*.
    static Cj()
    {
        InitRoslynResolver();
    }

    // Registered via [ModuleInitializer] below — assembly-load time, BEFORE
    // Main or any test method is JIT-compiled (JIT resolves referenced
    // assemblies up front, so a static ctor alone fires too late for tests
    // whose bodies use Roslyn types). Idempotent.
    internal static bool _roslynResolverReady;
    internal static void InitRoslynResolver()
    {
        if (_roslynResolverReady) return;
        _roslynResolverReady = true;
        try
        {
            string? roslyn = null;
            foreach (var sdk in Directory.GetDirectories("/usr/share/dotnet/sdk"))
            {
                var cand = Path.Combine(sdk, "Roslyn", "bincore");
                if (Directory.Exists(cand) && File.Exists(Path.Combine(cand, "Microsoft.CodeAnalysis.dll")))
                {
                    roslyn = cand;
                    break;
                }
            }
            if (roslyn is not null)
            {
                System.Runtime.Loader.AssemblyLoadContext.Default.Resolving += (_, name) =>
                {
                    var p = Path.Combine(roslyn, name.Name + ".dll");
                    return File.Exists(p)
                        ? System.Runtime.Loader.AssemblyLoadContext.Default.LoadFromAssemblyPath(p)
                        : null;
                };
            }
        }
        catch { }
    }
    public sealed class CjFail : Exception
    {
        public CjFail(string message) : base(message) { }
    }

    static void Fail(string label, string detail) =>
        throw new CjFail(label + ": " + detail);

    static string Show<T>(T v)
    {
        if (v is null) return "null";
        if (v is string s) return "\"" + s + "\"";
        return v.ToString() ?? "";
    }

    public static void True(bool condition, string label)
    {
        if (!condition) Fail(label, "expected true, got false");
    }

    public static void False(bool condition, string label)
    {
        if (condition) Fail(label, "expected false, got true");
    }

    public static void Eq<T>(T actual, T expected, string label)
    {
        if (!EqualityComparer<T>.Default.Equals(actual, expected))
            Fail(label, "expected " + Show(expected) + ", got " + Show(actual));
    }

    public static void Near(double actual, double expected, double epsilon, string label)
    {
        if (!(Math.Abs(actual - expected) <= epsilon))
            Fail(label, "expected ~" + expected + ", got " + actual);
    }

    public static void Contains(string haystack, string needle, string label)
    {
        if (haystack is null || !haystack.Contains(needle))
            Fail(label, "expected output to contain \"" + (needle ?? "null") + "\"");
    }

    public static string Capture(Action action)
    {
        var buffer = new StringWriter();
        var original = Console.Out;
        Console.SetOut(buffer);
        try { action(); }
        finally { Console.SetOut(original); }
        return buffer.ToString();
    }

    // ── Async/exception helpers (C# — Advanced; additive for Beginner) ────

    public static void Throws(Action action, string label)
    {
        try { action(); }
        catch (Exception) { return; }
        Fail(label, "expected an exception, but none was thrown");
    }

    public static async Task ThrowsAsync(Task task, string label)
    {
        try { await task.ConfigureAwait(false); }
        catch (Exception) { return; }
        Fail(label, "expected an exception, but none was thrown");
    }

    // Generic forms: return the thrown exception (typed) or the result so a
    // test can assert on both the throw and surrounding values in one await.
    public static async Task<Exception?> ThrowsAsync<TEx>(Func<Task> action) where TEx : Exception
    {
        try { await action().ConfigureAwait(false); return null; }
        catch (TEx ex) { return ex; }
    }

    public static async Task<T?> ThrowsAsync<TEx, T>(Func<Task<T>> action) where TEx : Exception
    {
        try { return await action().ConfigureAwait(false); }
        catch (TEx) { return default; }
    }

    public static async Task NoThrowAsync(Task task, string label)
    {
        try { await task.ConfigureAwait(false); }
        catch (Exception ex)
        {
            Fail(label, "expected no exception, got " + ex.GetType().Name);
        }
    }
}
`;

export const CS_LANG_VERSION = "14";
/** .NET 10 (LTS-era current line) — matches the SDK pinned in the Dockerfile. */
export const CS_TFM = "net10.0";
/** Reference pack glob fragment used by both the worker and the QA harness. */
export const CS_REF_GLOB = "/usr/share/dotnet/packs/Microsoft.NETCore.App.Ref/*/ref/net10.0/*.dll";
/**
 * Extra compile flags for C# — Advanced (probed 2026-09-17, see
 * docs/CURRICULUM-RESEARCH-CSHARP-ADVANCED.md): the SDK's Roslyn managed
 * assemblies as references (in-process compilation/analyzers/generators
 * teach and GRADE against the real compiler APIs) and `-unsafe` (pointer,
 * `fixed`, `stackalloc`, P/Invoke marshaling content). Both are additive
 * for Beginner: referencing an assembly changes nothing unless a type from
 * it is used, and `-unsafe` only unlocks explicit unsafe contexts. Measured
 * cost ≈ +0.1 s per compile at 0.5 CPU. The harness code itself stays
 * safe/managed — unsafe code can only appear in learner/author snippets.
 */
export const CS_ADV_EXTRA_REFS_GLOB =
  "/usr/share/dotnet/sdk/*/Roslyn/bincore/Microsoft.CodeAnalysis*.dll";
export const CS_ADV_EXTRA_FLAGS = "-unsafe";

/** Minimal framework-dependent runtimeconfig (roll-forward to installed minor). */
export const CS_RUNTIMECONFIG_JSON =
  '{"runtimeOptions":{"tfm":"' + CS_TFM + '","rollForward":"LatestMinor","framework":{"name":"Microsoft.NETCore.App","version":"10.0.0"}}}';

export type CSharpJobInput = {
  code: string;
  testFiles: { name: string; code: string }[];
};

/** Sanitize a test name into a safe file fragment (mirrors the worker). */
export function csSanitizeName(name: string): string {
  return sanitizeTestName(name);
}

/**
 * Build one test compilation unit: harness + the author's snippet (as the
 * body of CjTest.Body) + PASS/exit-code protocol.
 */
export function buildCSharpTestFile(test: { name: string; code: string }): string {
  const indented = test.code
    .split("\n")
    .map((line) => (line.trim().length > 0 ? `        ${line}` : line))
    .join("\n");
  // Tests that await need an async entry point. async Task<int> Main is valid
  // C#; sync tests keep the original signature so existing courses are
  // byte-for-byte unaffected.
  const isAsync = /\bawait\b/.test(test.code);
  const bodySig = isAsync ? "static async Task<int> Body()" : "static void Body()";
  const bodyCall = isAsync ? "await Body();" : "Body();";
  const bodyClose = isAsync ? "        return 0;\n    }" : "    }";
  return [
    CS_TEST_HARNESS,
    "static class CjTest",
    "{",
    `    ${bodySig}`,
    "    {",
    indented,
    bodyClose,
    "",
    "    static async Task<int> Main()",
    "    {",
    "        try",
    "        {",
    `            ${bodyCall}`,
    '            Console.Out.WriteLine("PASS");',
    "            return 0;",
    "        }",
    "        catch (Cj.CjFail fail)",
    "        {",
    "            Console.Error.WriteLine(fail.Message);",
    "            return 1;",
    "        }",
    "        catch (Exception ex)",
    "        {",
    "            Console.Error.WriteLine(ex.Message);",
    "            return 1;",
    "        }",
    "    }",
    "}",
  ].join("\n");
}

/** Quoted-delimiter heredoc (no interpolation) — same as sandbox.ts. */
function heredoc(name: string, content: string, delim: string): string {
  return `cat > "${name}" << '${delim}'\n${content}\n${delim}`;
}

/**
 * Full POSIX sh job script for a C# run. Same heredoc strategy, same marker
 * protocol, same per-test isolation as the other compiled runtimes.
 */
export function buildCSharpJobScript(job: CSharpJobInput, delim: string): string {
  const parts: string[] = [
    "set -u",
    "cd /job",
    "export DOTNET_ROOT=/usr/share/dotnet DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1 DOTNET_CLI_HOME=/tmp HOME=/tmp",
    `CSC="dotnet /usr/share/dotnet/sdk/*/Roslyn/bincore/csc.dll"`,
    `REFS=""; for f in ${CS_REF_GLOB}; do REFS="$REFS -r:$f"; done`,
    `for r in ${CS_ADV_EXTRA_REFS_GLOB}; do REFS="$REFS -r:$r"; done`,
    `EXTRA="${CS_ADV_EXTRA_FLAGS}"`,
  ];
  parts.push(heredoc("Solution.cs", job.code, delim));
  // Solution must compile on its own (as a library, so a learner-written
  // Main is legal here) before any test runs — the educational syntax gate.
  // Raw csc has no implicit-usings feature: challenge boilerplates carry the
  // `using` lines (visible to learners, mirrors real .csproj ExplicitUsings
  // content). Roslyn prints diagnostics on STDOUT — capture both streams.
  parts.push(
    [
      `dotnet /usr/share/dotnet/sdk/*/Roslyn/bincore/csc.dll -nologo -langversion:${CS_LANG_VERSION} $EXTRA -t:library -out:/tmp/_cj_gate.dll $REFS Solution.cs > /job/_syntax.log 2>&1`,
      "if [ $? -ne 0 ]; then",
      '  echo "Your code did not compile. Compiler output:" >&2',
      "  cat /job/_syntax.log >&2",
      "  exit 1",
      "fi",
    ].join("\n"),
  );
  for (const test of job.testFiles) {
    const name = csSanitizeName(test.name);
    parts.push(heredoc(`test-${name}.cs`, buildCSharpTestFile(test), delim));
  }
  for (const test of job.testFiles) {
    const name = csSanitizeName(test.name);
    parts.push(
      [
        // -main pins the entry point: a learner Main inside Solution.cs can
        // never take over (without this, two Mains would be CS0017).
        // Diagnostics go to stdout+stderr — capture both for the hint channel.
        `dotnet /usr/share/dotnet/sdk/*/Roslyn/bincore/csc.dll -nologo -langversion:${CS_LANG_VERSION} $EXTRA -out:"/tmp/t-${name}.dll" $REFS -main:CjTest Solution.cs "test-${name}.cs" > "/job/_build-${name}.log" 2>&1`,
        `if [ $? -ne 0 ]; then echo "__TEST_RESULT__ ${name} status=1"; cat "/job/_build-${name}.log" >&2; continue; fi`,
        `cat > "/tmp/t-${name}.runtimeconfig.json" << 'CJ_RC'\n${CS_RUNTIMECONFIG_JSON}\nCJ_RC`,
        `dotnet "/tmp/t-${name}.dll" 2> "/job/_run-${name}.log"`,
        `status=$?`,
        `echo "__TEST_RESULT__ ${name} status=$status"`,
        `if [ $status -ne 0 ] && [ -s "/job/_run-${name}.log" ]; then cat "/job/_run-${name}.log" >&2; fi`,
        `if [ $status -ne 0 ] && [ -s "/job/_build-${name}.log" ]; then cat "/job/_build-${name}.log" >&2; fi`,
      ].join("\n"),
    );
  }
  return parts.join("\n") + "\n";
}
