"""Module 7 — Source generators (csa-m7)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-source-generators",
        "Source Generators",
        "Compile-time code generation: incremental pipelines, generated code rules, and the reflection-free future.",
    )

    csa.register_lesson(
        MID, "csa-m7-generator-model", "The source generator model",
        "What a generator is, when it runs, what it can and cannot do — and why 'compile-time' changes design.",
        15, "advanced", _m7_model, _m7_model_vi,
    )
    csa.register_lesson(
        MID, "csa-m7-incremental", "Incremental generators",
        "IIncrementalGenerator pipelines: caching, equality, and not re-running the world per keystroke.",
        16, "advanced", _m7_incremental, _m7_incremental_vi,
    )
    csa.register_lesson(
        MID, "csa-m7-generated-code", "Rules of generated code",
        "Generated code must fully qualify, compile cleanly, and be debuggable — the contracts that keep generators useful.",
        14, "advanced", _m7_rules, _m7_rules_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m7", "Checkpoint: source generators",
        "Synthesis: drive a generator programmatically and verify its output compiles.",
        12, "advanced", _m7_checkpoint, _m7_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m7-task", MID,
        title="Source generator checkpoint",
        prompt=(
            "Implement `static (int trees, bool symbolResolved) RunGenerator(string userSource)`: build a generator "
            "that reads classes marked `[Gen]` (an attribute the generator itself creates via "
            "RegisterPostInitializationOutput) and emits a static class `GenCatalog` with one method per marked "
            "class: `public static string Name_X() => \"X\";`. Parse userSource, add the attribute source, run "
            "CSharpGeneratorDriver, and return (generated tree count including the init output, whether symbol "
            "`GenCatalog` resolves in the output compilation)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "generation",
                "code": (
                    "var (trees, ok) = Solution.RunGenerator(\"[Gen] public class Widget { }\");\n"
                    'Cj.True(ok, "GenCatalog resolves");\n'
                    "Cj.True(trees >= 2, $\"expected init + generated trees, got {trees}\");"
                ),
                "hint": "CSharpGeneratorDriver.Create(gen).RunGeneratorsAndUpdateCompilation(comp, out var output, out _); check output.GetTypeByMetadataName(\"GenCatalog\").",
            },
        ],
        reference=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.Text;\n"
            "using System.Collections.Immutable;\n"
            "using System.Text;\n\n"
            "[Generator]\n"
            "public class CatalogGen : IIncrementalGenerator\n{\n"
            "    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n"
            "    {\n"
            "        ctx.RegisterPostInitializationOutput(static init =>\n"
            "            init.AddSource(\"GenAttribute.g.cs\",\n"
            "                \"[System.AttributeUsage(System.AttributeTargets.Class)]\\n\"\n"
            "                + \"public sealed class GenAttribute : System.Attribute { }\"));\n\n"
            "        var marked = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n"
            "            \"GenAttribute\",\n"
            "            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n"
            "            static (ctx2, _) => ctx2.TargetSymbol.Name);\n\n"
            "        ctx.RegisterSourceOutput(marked.Collect(), static (spc, names) =>\n"
            "        {\n"
            "            var sb = new StringBuilder(\"public static class GenCatalog\\n{\\n\");\n"
            "            foreach (var n in names.Distinct())\n"
            "                sb.AppendLine($\"    public static string Name_{n}() => \\\"{n}\\\";\");\n"
            "            sb.Append('}');\n"
            "            spc.AddSource(\"GenCatalog.g.cs\", SourceText.From(sb.ToString(), Encoding.UTF8));\n"
            "        });\n"
            "    }\n}\n\n"
            "public class Solution\n{\n"
            "    public static (int trees, bool symbolResolved) RunGenerator(string userSource)\n"
            "    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(userSource);\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"gen\", new[] { tree }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        var driver = CSharpGeneratorDriver.Create(new CatalogGen().AsSourceGenerator());\n"
            "        driver = (CSharpGeneratorDriver)driver.RunGeneratorsAndUpdateCompilation(comp, out var output, out _);\n"
            "        var run = driver.GetRunResult();\n"
            "        var sym = ((CSharpCompilation)output).GetTypeByMetadataName(\"GenCatalog\");\n"
            "        return (run.GeneratedTrees.Length, sym is not null);\n"
            "    }\n}"
        ),
        wrong=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.Text;\n"
            "using System.Collections.Immutable;\n"
            "using System.Text;\n\n"
            "[Generator]\n"
            "public class CatalogGen : IIncrementalGenerator\n{\n"
            "    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n"
            "    {\n"
            "        ctx.RegisterPostInitializationOutput(static init =>\n"
            "            init.AddSource(\"GenAttribute.g.cs\",\n"
            "                \"[System.AttributeUsage(System.AttributeTargets.Class)]\\n\"\n"
            "                + \"public sealed class GenAttribute : System.Attribute { }\"));\n\n"
            "        var marked = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n"
            "            \"GenAttribute\",\n"
            "            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n"
            "            static (ctx2, _) => ctx2.TargetSymbol.Name);\n\n"
            "        ctx.RegisterSourceOutput(marked.Collect(), static (spc, names) =>\n"
            "        {\n"
            "            var sb = new StringBuilder(\"public static class GenCatalog\\n{\\n\");\n"
            "            foreach (var n in names.Distinct())\n"
            "                sb.AppendLine($\"    public static string Name_{n}() => \\\"{n}\\\";\");\n"
            "            sb.Append('}');\n"
            "            spc.AddSource(\"GenCatalog.g.cs\", SourceText.From(sb.ToString(), Encoding.UTF8));\n"
            "        });\n"
            "    }\n}\n\n"
            "public class Solution\n{\n"
            "    public static (int trees, bool symbolResolved) RunGenerator(string userSource)\n"
            "    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(userSource);\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"gen\", new[] { tree }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        var driver = CSharpGeneratorDriver.Create(new CatalogGen().AsSourceGenerator());\n"
            "        driver = (CSharpGeneratorDriver)driver.RunGeneratorsAndUpdateCompilation(comp, out var output, out _);\n"
            "        var run = driver.GetRunResult();\n"
            "        var sym = ((CSharpCompilation)output).GetTypeByMetadataName(\"GenWidget\");   // wrong symbol name\n"
            "        return (run.GeneratedTrees.Length, sym is not null);\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p7-generators", "Generator drills",
        "Pipeline building, generated-code contracts, generator diagnostics, and compile-verification.",
        45, "advanced", "csa-m7-incremental",
        ["csa-p7-emitted-source", "csa-p7-generator-compile"],
    )
    csa.register_challenge(
        "csa-p7-emitted-source", MID,
        title="Emit clean generated source",
        prompt=(
            "Implement `static string EmitDto(string className, (string Name, string Type)[] fields)` returning a "
            "complete, compilable C# source string for `public sealed record {className}(...)` with the given "
            "fields — using FULLY QUALIFIED types for non-primitives (e.g. System.DateTime) so the output compiles "
            "without any usings. Primitives (int, string, bool, double) stay as-is."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "compiles-without-usings",
                "code": (
                    "var src = Solution.EmitDto(\"Order\", new[] { (\"Id\", \"int\"), (\"Placed\", \"System.DateTime\") });\n"
                    'Cj.True(src.Contains("record Order("), "record declared");\n'
                    "// The emitted source must compile standalone (no usings available):\n"
                    'Cj.True(Solution.CompilesStandalone(src), "emitted source compiles");'
                ),
                "hint": "Generated code must not depend on ambient usings — emit fully qualified names for anything not a primitive keyword.",
            },
            {
                "name": "primitives-stay-short",
                "code": (
                    "var src = Solution.EmitDto(\"P\", new[] { (\"Age\", \"int\"), (\"Name\", \"string\") });\n"
                    'Cj.True(src.Contains("int Age"), "primitive stays keyword");\n'
                    'Cj.False(src.Contains("System.Int32 Age"), "no verbose primitives");'
                ),
                "hint": "Keep a keyword map for primitives; qualify only the rest.",
            },
        ],
        reference=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n\n"
            "public class Solution\n{\n"
            "    static readonly System.Collections.Generic.Dictionary<string, string> Keywords = new()\n"
            "    { [\"int\"] = \"int\", [\"string\"] = \"string\", [\"bool\"] = \"bool\", [\"double\"] = \"double\" };\n\n"
            "    public static string EmitDto(string className, (string Name, string Type)[] fields)\n"
            "    {\n"
            "        var parts = fields.Select(f =>\n"
            "            Keywords.TryGetValue(f.Type, out var kw) ? $\"{kw} {f.Name}\" : $\"{f.Type} {f.Name}\");\n"
            "        return $\"public sealed record {className}({string.Join(\", \", parts)});\";\n"
            "    }\n\n"
            "    public static bool CompilesStandalone(string source)\n    {\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"emit\", new[] { CSharpSyntaxTree.ParseText(source) }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        return !comp.GetDiagnostics().Any(d => d.Severity == DiagnosticSeverity.Error);\n"
            "    }\n}"
        ),
        wrong=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n\n"
            "public class Solution\n{\n"
            "    public static string EmitDto(string className, (string Name, string Type)[] fields)\n"
            "    {\n"
            "        var parts = fields.Select(f => $\"System.{f.Type} {f.Name}\");\n"
            "        return $\"public sealed record {className}({string.Join(\", \", parts)});\";\n"
            "    }\n\n"
            "    public static bool CompilesStandalone(string source)\n    {\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"emit\", new[] { CSharpSyntaxTree.ParseText(source) }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        return !comp.GetDiagnostics().Any(d => d.Severity == DiagnosticSeverity.Error);\n"
            "    }\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p7-generator-compile", MID,
        title="Verify the pipeline compiles",
        prompt=(
            "Implement `static bool GeneratedCatalogCompiles(string userSource)`: run the same catalog generator "
            "pattern as the checkpoint (attribute + GenCatalog class) but ALSO verify the OUTPUT compilation has "
            "zero error diagnostics (generated code included). Return false both when generation fails and when the "
            "generated source does not compile."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "end-to-end",
                "code": (
                    'Cj.True(Solution.GeneratedCatalogCompiles("[Gen2] public class A { }"), "valid input");\n'
                    "// A struct marked [Gen2] is skipped by the class-only filter; catalog is empty but the\n"
                    "// generated file must still compile:\n"
                    'Cj.True(Solution.GeneratedCatalogCompiles("[Gen2] public struct S { }"), "no marked classes still compiles");'
                ),
                "hint": "Reuse the driver pattern; additionally run comp.GetDiagnostics() on the OUTPUT compilation.",
            },
        ],
        reference=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.Text;\n"
            "using System.Collections.Immutable;\n"
            "using System.Text;\n\n"
            "[Generator]\n"
            "public class CatGen2 : IIncrementalGenerator\n{\n"
            "    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n"
            "    {\n"
            "        ctx.RegisterPostInitializationOutput(static init =>\n"
            "            init.AddSource(\"GenAttribute2.g.cs\",\n"
            "                \"[System.AttributeUsage(System.AttributeTargets.Class)]\\n\"\n"
            "                + \"public sealed class GenAttribute2 : System.Attribute { }\"));\n"
            "        var marked = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n"
            "            \"GenAttribute2\",\n"
            "            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n"
            "            static (ctx2, _) => ctx2.TargetSymbol.Name);\n"
            "        ctx.RegisterSourceOutput(marked.Collect(), static (spc, names) =>\n"
            "        {\n"
            "            var sb = new StringBuilder(\"public static class GenCatalog2\\n{\\n\");\n"
            "            foreach (var n in names.Distinct())\n"
            "                sb.AppendLine($\"    public static string Name_{n}() => \\\"{n}\\\";\");\n"
            "            sb.Append('}');\n"
            "            spc.AddSource(\"GenCatalog2.g.cs\", SourceText.From(sb.ToString(), Encoding.UTF8));\n"
            "        });\n"
            "    }\n}\n\n"
            "public class Solution\n{\n"
            "    public static bool GeneratedCatalogCompiles(string userSource)\n    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(userSource);\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"genc\", new[] { tree }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        var driver = CSharpGeneratorDriver.Create(new CatGen2().AsSourceGenerator());\n"
            "        driver.RunGeneratorsAndUpdateCompilation(comp, out var output, out var genDiags);\n"
            "        if (genDiags.Any(d => d.Severity == DiagnosticSeverity.Error)) return false;\n"
            "        var outDiags = ((CSharpCompilation)output).GetDiagnostics();\n"
            "        return !outDiags.Any(d => d.Severity == DiagnosticSeverity.Error);\n"
            "    }\n}"
        ),
        wrong=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.Text;\n"
            "using System.Collections.Immutable;\n"
            "using System.Text;\n\n"
            "[Generator]\n"
            "public class CatGen2 : IIncrementalGenerator\n{\n"
            "    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n"
            "    {\n"
            "        ctx.RegisterPostInitializationOutput(static init =>\n"
            "            init.AddSource(\"GenAttribute2.g.cs\",\n"
            "                \"[System.AttributeUsage(System.AttributeTargets.Class)]\\n\"\n"
            "                + \"public sealed class GenAttribute2 : System.Attribute { }\"));\n"
            "        var marked = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n"
            "            \"GenAttribute2\",\n"
            "            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n"
            "            static (ctx2, _) => ctx2.TargetSymbol.Name);\n"
            "        ctx.RegisterSourceOutput(marked.Collect(), static (spc, names) =>\n"
            "        {\n"
            "            var sb = new StringBuilder(\"public static class GenCatalog2\\n{\\n\");\n"
            "            foreach (var n in names.Distinct())\n"
            "                sb.AppendLine($\"    public static string Name_{n}() => \\\"{n}\\\";\");\n"
            "            sb.Append('}');\n"
            "            spc.AddSource(\"GenCatalog2.g.cs\", SourceText.From(sb.ToString(), Encoding.UTF8));\n"
            "        });\n"
            "    }\n}\n\n"
            "public class Solution\n{\n"
            "    public static bool GeneratedCatalogCompiles(string userSource)\n    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(userSource);\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"genc\", new[] { tree }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        var driver = CSharpGeneratorDriver.Create(new CatGen2().AsSourceGenerator());\n"
            "        driver.RunGeneratorsAndUpdateCompilation(comp, out var output, out var genDiags);\n"
            "        return genDiags.Length == 0;   // WRONG: ignores output-compilation errors and info diags\n"
            "    }\n}"
        ),
        level="independent",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m7_model = r"""## The source generator model

A source generator is a Roslyn extension that runs DURING compilation: it
reads the code being compiled and adds new syntax trees to the same
compilation. The generated code compiles alongside yours — one assembly,
no runtime reflection, no code after build.

```csharp
[Generator]
public sealed class HelloGen : IIncrementalGenerator
{
    public void Initialize(IncrementalGeneratorInitializationContext ctx)
    {
        ctx.RegisterPostInitializationOutput(static init =>
            init.AddSource("Marker.g.cs",
                "public sealed class HelloAttribute : System.Attribute { }"));

        var targets = ctx.SyntaxProvider.ForAttributeWithMetadataName(
            "HelloAttribute",
            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,
            static (ctx2, _) => ctx2.TargetSymbol.Name);

        ctx.RegisterSourceOutput(targets, static (spc, name) =>
            spc.AddSource($"{name}.g.cs",
                $"public static class Hello_{name} {{ public const string Who = \"{name}\"; }}"));
    }
}
```

What this changes architecturally: anything built with runtime reflection
(DI registries, serializers, mappers, enum-to-string tables) can instead be
*computed once at compile time*. That removes startup cost, becomes
trim/AOT-safe (Module 19), and surfaces errors at build time.

What generators CANNOT do: modify existing user code (they only ADD
sources), run arbitrary per-user logic from configuration files at dev
time, or replace the build. They see the same compilation the compiler
sees — nothing more.
"""

_m7_model_vi = r"""## Mô hình source generator

Source generator là một extension Roslyn chạy TRONG lúc biên dịch: nó đọc
code đang được biên dịch và thêm các syntax tree mới vào cùng compilation.
Code sinh ra biên dịch cùng code của bạn — một assembly, không reflection
lúc chạy, không code sau build.

```csharp
[Generator]
public sealed class HelloGen : IIncrementalGenerator
{
    public void Initialize(IncrementalGeneratorInitializationContext ctx)
    {
        ctx.RegisterPostInitializationOutput(static init =>
            init.AddSource("Marker.g.cs",
                "public sealed class HelloAttribute : System.Attribute { }"));

        var targets = ctx.SyntaxProvider.ForAttributeWithMetadataName(
            "HelloAttribute",
            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,
            static (ctx2, _) => ctx2.TargetSymbol.Name);

        ctx.RegisterSourceOutput(targets, static (spc, name) =>
            spc.AddSource($"{name}.g.cs",
                $"public static class Hello_{name} {{ public const string Who = \"{name}\"; }}"));
    }
}
```

Điều này thay đổi kiến trúc thế nào: mọi thứ từng xây bằng runtime reflection
(registry DI, serializer, mapper, bảng enum-to-string) giờ có thể được *tính
một lần lúc biên dịch*. Điều đó xóa chi phí startup, trở nên thân thiện
trim/AOT (Module 19), và đẩy lỗi về lúc build.

Generator KHÔNG làm được gì: sửa code hiện có của người dùng (chỉ THÊM
source), chạy logic tùy ý từ file cấu hình lúc dev, hay thay thế build. Nó
nhìn thấy cùng compilation mà compiler thấy — không hơn.
"""

_m7_incremental = r"""## Incremental generators

The classic `ISourceGenerator` re-runs everything on every change — fine
for tiny tools, brutal for IDEs. `IIncrementalGenerator` instead builds a
**pipeline** of transformations the compiler tracks by value equality: a
keystroke re-runs only the steps whose inputs actually changed.

```csharp
var provider = ctx.SyntaxProvider.ForAttributeWithMetadataName(...)
    .Select(static (name, _) => name.ToUpperInvariant())   // pure transform
    .Collect();                                            // gather into ImmutableArray

ctx.RegisterSourceOutput(provider, static (spc, names) => { /* emit once */ });
```

The performance contract, from the Roslyn team's own guidance:

1. **Transformations must be pure and cheap** — they may run many times;
   their results are cached by equality.
2. **`ForAttributeWithMetadataName` first.** It is a heavily-optimized
   provider for the dominant pattern (find types with attribute X); hand-
   rolled `CreateSyntaxProvider` predicates run more often and do more work.
3. **`Collect()` deliberately** — collecting defeats incrementalism for the
   steps after it; do per-item work before collecting, then emit once.
4. **Lambda hygiene**: all pipeline lambdas must be `static` (no captured
   variables) — capturing silently breaks the caching contract.

When generators go wrong in production, it is almost always a pipeline
that recomputes a whole-project model per keystroke — the fix is always
"push work later, make steps cheap, cache by value".
"""

_m7_incremental_vi = r"""## Incremental generators

`ISourceGenerator` cổ điển chạy lại mọi thứ sau mỗi thay đổi — ổn với công
cụ tí hon, tàn bạo với IDE. `IIncrementalGenerator` thay vào đó dựng một
**pipeline** các phép biến đổi mà compiler theo dõi bằng so sánh giá trị:
một phím gõ chỉ chạy lại các bước mà input thật sự thay đổi.

```csharp
var provider = ctx.SyntaxProvider.ForAttributeWithMetadataName(...)
    .Select(static (name, _) => name.ToUpperInvariant())   // biến đổi thuần
    .Collect();                                            // gom thành ImmutableArray

ctx.RegisterSourceOutput(provider, static (spc, names) => { /* phát một lần */ });
```

Hợp đồng hiệu năng, theo đúng hướng dẫn của đội Roslyn:

1. **Phép biến đổi phải thuần và rẻ** — chúng có thể chạy nhiều lần; kết
   quả được cache theo so sánh giá trị.
2. **`ForAttributeWithMetadataName` trước tiên.** Đây là provider được tối
   ưu mạnh cho pattern chủ đạo (tìm kiểu có attribute X); predicate
   `CreateSyntaxProvider` viết tay chạy thường hơn và làm nhiều việc hơn.
3. **`Collect()` có chủ đích** — collect phá tính tăng dần cho các bước
   sau nó; làm việc từng phần tử trước khi collect, rồi phát một lần.
4. **Vệ sinh lambda**: mọi lambda pipeline phải `static` (không bắt biến) —
   capture âm thầm phá hợp đồng caching.

Khi generator lỗi trong production, gần như luôn là pipeline tính lại mô
hình toàn dự án cho mỗi phím gõ — cách sửa luôn là "đẩy việc về sau, làm
cho từng bước rẻ, cache theo giá trị".
"""

_m7_rules = r"""## Rules of generated code

Generated source has one reader that never forgives: the compiler. The
contracts that keep generators shippable:

- **Fully qualify everything.** Generated code cannot rely on the user's
  `using` directives — `System.DateTime`, not `DateTime`; or emit explicit
  `using` blocks scoped in a namespace. The classic failure: a generated
  DTO using `DateTime` compiles in your test project and fails in the
  user's namespace where `DateTime` means something else.
- **Emit diagnostics, not exceptions.** A generator that throws breaks the
  build with an incomprehensible error; a generator that reports a proper
  diagnostic points at the user's actual mistake.
- **Namespace your output** — generated types colliding with user types is
  a name-resolution bug users cannot debug.
- **Mark partial, extend nothing**: generate `partial` classes the user
  opts into extending, never edit their declared members.
- **Debuggability**: `#line` directives or clean, formatted output so the
  generated file reads sanely when a stack trace points into it.

Testing generators happens exactly like the checkpoint does it: drive
`CSharpGeneratorDriver`, inspect the generated trees, compile the OUTPUT,
and assert zero error diagnostics. That is also how CI guards a generator
against Roslyn version upgrades.
"""

_m7_rules_vi = r"""## Luật của generated code

Generated source có một người đọc không bao giờ thứ thứ: compiler. Những
hợp đồng giữ generator đáng ship:

- **Fully qualify mọi thứ.** Generated code không thể dựa vào `using` của
  người dùng — `System.DateTime`, không phải `DateTime`; hoặc phát khối
  `using` tường minh trong namespace. Thất bại kinh điển: một DTO sinh ra
  dùng `DateTime` biên dịch ổn trong dự án test của bạn nhưng hỏng trong
  namespace của người dùng, nơi `DateTime` là thứ khác.
- **Phát diagnostic, không phải exception.** Generator ném exception phá
  build với lỗi khó hiểu; generator báo diagnostic đúng cách trỏ vào lỗi
  thật của người dùng.
- **Namespace cho output** — kiểu sinh ra va chạm với kiểu của người dùng là
  bug phân giải tên mà người dùng không thể debug.
- **Đánh dấu partial, không mở rộng gì**: sinh lớp `partial` mà người dùng
  chủ động chọn để mở rộng, không bao giờ sửa member họ khai báo.
- **Khả năng debug**: directive `#line` hoặc output sạch, có format để file
  sinh ra đọc được khi stack trace trỏ vào đó.

Kiểm thử generator diễn ra đúng như checkpoint làm: chạy
`CSharpGeneratorDriver`, soi các tree sinh ra, biên dịch OUTPUT, và khẳng
định không có diagnostic lỗi. Đó cũng là cách CI bảo vệ generator trước các
bản nâng cấp Roslyn.
"""

_m7_checkpoint = r"""## Checkpoint: source generators

The graded task drives a real incremental generator end to end: marker
attribute via post-initialization, `ForAttributeWithMetadataName` discovery,
catalog emission, symbol resolution in the output compilation. Passing it
means you can build and VERIFY a generator — the same loop CI uses.
"""

_m7_checkpoint_vi = r"""## Checkpoint: source generators

Bài được chấm chạy một incremental generator thật từ đầu tới cuối: marker
attribute qua post-initialization, khám phá bằng `ForAttributeWithMetadataName`,
phát catalog, resolve symbol trong output compilation. Pass nghĩa là bạn
xây và XÁC MINH được generator — đúng vòng lặp mà CI dùng.
"""
