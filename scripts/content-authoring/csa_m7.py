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
        title='Verify the pipeline compiles',
        prompt=(
            'Implement `static bool GeneratedCatalogCompiles(string userSource)`: build a generator pipeline where a Gen2Attribute (emitted by the generator itself via RegisterPostInitializationOutput, AttributeTargets.Class) marks classes, and a generated static class GenCatalog2 exposes one method per marked class. Return true only when the OUTPUT compilation — user code AND generated code — has zero error diagnostics. The test proves the output check matters: a user class named GenCatalog2 collides with the generated type and must yield false.'
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'end-to-end',
                "code": (
                    'Cj.True(Solution.GeneratedCatalogCompiles("[Gen2] public class A { }"), "valid input");\n// A user class named exactly like the GENERATED catalog collides in the output\n// compilation - user source alone is valid, so only the output check can catch it:\nCj.False(Solution.GeneratedCatalogCompiles("[Gen2] public class GenCatalog2 { }"), "collision with generated GenCatalog2 -> false");\nCj.True(Solution.GeneratedCatalogCompiles("[Gen2] public class A { } [Gen2] public class B { }"), "two marked classes");'
                ),
                "hint": 'RunGeneratorsAndUpdateCompilation hands you the OUTPUT compilation — GetDiagnostics() on it covers the generated trees. genDiags alone does not.',
            },
        ],
        reference=(
            'using Microsoft.CodeAnalysis;\nusing Microsoft.CodeAnalysis.CSharp;\nusing Microsoft.CodeAnalysis.Text;\nusing System.Collections.Immutable;\nusing System.Text;\n\n[Generator]\npublic class CatGen2 : IIncrementalGenerator\n{\n    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n    {\n        ctx.RegisterPostInitializationOutput(static init =>\n            init.AddSource("Gen2Attribute.g.cs",\n                "[System.AttributeUsage(System.AttributeTargets.Class)]\\n"\n                + "public sealed class Gen2Attribute : System.Attribute { }"));\n        var marked = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n            "Gen2Attribute",\n            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n            static (ctx2, _) => ctx2.TargetSymbol.Name);\n        ctx.RegisterSourceOutput(marked.Collect(), static (spc, names) =>\n        {\n            var sb = new StringBuilder("public static class GenCatalog2\\n{\\n");\n            foreach (var n in names)\n                sb.AppendLine($"    public static string Name_{n}() => \\"{n}\\";");\n            sb.Append(\'}\');\n            spc.AddSource("GenCatalog2.g.cs", SourceText.From(sb.ToString(), Encoding.UTF8));\n        });\n    }\n}\n\npublic class Solution\n{\n    public static bool GeneratedCatalogCompiles(string userSource)\n    {\n        var tree = CSharpSyntaxTree.ParseText(userSource);\n        var refs = AppDomain.CurrentDomain.GetAssemblies()\n            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n            .Select(a => MetadataReference.CreateFromFile(a.Location));\n        var comp = CSharpCompilation.Create("genc", new[] { tree }, refs,\n            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n        var driver = CSharpGeneratorDriver.Create(new CatGen2().AsSourceGenerator());\n        driver.RunGeneratorsAndUpdateCompilation(comp, out var output, out var genDiags);\n        if (genDiags.Any(d => d.Severity == DiagnosticSeverity.Error)) return false;\n        var outDiags = ((CSharpCompilation)output).GetDiagnostics();\n        return !outDiags.Any(d => d.Severity == DiagnosticSeverity.Error);\n    }\n}'
        ),
        wrong=(
            'using Microsoft.CodeAnalysis;\nusing Microsoft.CodeAnalysis.CSharp;\nusing Microsoft.CodeAnalysis.Text;\nusing System.Collections.Immutable;\nusing System.Text;\n\n[Generator]\npublic class CatGen2 : IIncrementalGenerator\n{\n    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n    {\n        ctx.RegisterPostInitializationOutput(static init =>\n            init.AddSource("Gen2Attribute.g.cs",\n                "[System.AttributeUsage(System.AttributeTargets.Class)]\\n"\n                + "public sealed class Gen2Attribute : System.Attribute { }"));\n        var marked = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n            "Gen2Attribute",\n            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n            static (ctx2, _) => ctx2.TargetSymbol.Name);\n        ctx.RegisterSourceOutput(marked.Collect(), static (spc, names) =>\n        {\n            var sb = new StringBuilder("public static class GenCatalog2\\n{\\n");\n            foreach (var n in names)\n                sb.AppendLine($"    public static string Name_{n}() => \\"{n}\\";");\n            sb.Append(\'}\');\n            spc.AddSource("GenCatalog2.g.cs", SourceText.From(sb.ToString(), Encoding.UTF8));\n        });\n    }\n}\n\npublic class Solution\n{\n    public static bool GeneratedCatalogCompiles(string userSource)\n    {\n        var tree = CSharpSyntaxTree.ParseText(userSource);\n        var refs = AppDomain.CurrentDomain.GetAssemblies()\n            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n            .Select(a => MetadataReference.CreateFromFile(a.Location));\n        var comp = CSharpCompilation.Create("genc", new[] { tree }, refs,\n            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n        var driver = CSharpGeneratorDriver.Create(new CatGen2().AsSourceGenerator());\n        driver.RunGeneratorsAndUpdateCompilation(comp, out var output, out var genDiags);\n        return genDiags.Length == 0;   // WRONG: ignores output-compilation errors in generated code\n    }\n}'
        ),
        level='guided',
    )


# --- recovered lesson MDX variables (regenerated from the last emit) ---
_m7_model = '## The source generator model\n\nA source generator is a Roslyn extension that runs DURING compilation: it\nreads the code being compiled and adds new syntax trees to the same\ncompilation. The generated code compiles alongside yours — one assembly,\nno runtime reflection, no code after build.\n\n```csharp\n[Generator]\npublic sealed class HelloGen : IIncrementalGenerator\n{\n    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n    {\n        ctx.RegisterPostInitializationOutput(static init =>\n            init.AddSource("Marker.g.cs",\n                "public sealed class HelloAttribute : System.Attribute { }"));\n\n        var targets = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n            "HelloAttribute",\n            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n            static (ctx2, _) => ctx2.TargetSymbol.Name);\n\n        ctx.RegisterSourceOutput(targets, static (spc, name) =>\n            spc.AddSource($"{name}.g.cs",\n                $"public static class Hello_{name} {{ public const string Who = \\"{name}\\"; }}"));\n    }\n}\n```\n\nWhat this changes architecturally: anything built with runtime reflection\n(DI registries, serializers, mappers, enum-to-string tables) can instead be\n*computed once at compile time*. That removes startup cost, becomes\ntrim/AOT-safe (Module 19), and surfaces errors at build time.\n\nWhat generators CANNOT do: modify existing user code (they only ADD\nsources), run arbitrary per-user logic from configuration files at dev\ntime, or replace the build. They see the same compilation the compiler\nsees — nothing more.\n'
_m7_model_vi = '## Mô hình source generator\n\nSource generator là một extension Roslyn chạy TRONG lúc biên dịch: nó đọc\ncode đang được biên dịch và thêm các syntax tree mới vào cùng compilation.\nCode sinh ra biên dịch cùng code của bạn — một assembly, không reflection\nlúc chạy, không code sau build.\n\n```csharp\n[Generator]\npublic sealed class HelloGen : IIncrementalGenerator\n{\n    public void Initialize(IncrementalGeneratorInitializationContext ctx)\n    {\n        ctx.RegisterPostInitializationOutput(static init =>\n            init.AddSource("Marker.g.cs",\n                "public sealed class HelloAttribute : System.Attribute { }"));\n\n        var targets = ctx.SyntaxProvider.ForAttributeWithMetadataName(\n            "HelloAttribute",\n            static (node, _) => node is Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax,\n            static (ctx2, _) => ctx2.TargetSymbol.Name);\n\n        ctx.RegisterSourceOutput(targets, static (spc, name) =>\n            spc.AddSource($"{name}.g.cs",\n                $"public static class Hello_{name} {{ public const string Who = \\"{name}\\"; }}"));\n    }\n}\n```\n\nĐiều này thay đổi kiến trúc thế nào: mọi thứ từng xây bằng runtime reflection\n(registry DI, serializer, mapper, bảng enum-to-string) giờ có thể được *tính\nmột lần lúc biên dịch*. Điều đó xóa chi phí startup, trở nên thân thiện\ntrim/AOT (Module 19), và đẩy lỗi về lúc build.\n\nGenerator KHÔNG làm được gì: sửa code hiện có của người dùng (chỉ THÊM\nsource), chạy logic tùy ý từ file cấu hình lúc dev, hay thay thế build. Nó\nnhìn thấy cùng compilation mà compiler thấy — không hơn.\n'
_m7_incremental = '## Incremental generators\n\nThe classic `ISourceGenerator` re-runs everything on every change — fine\nfor tiny tools, brutal for IDEs. `IIncrementalGenerator` instead builds a\n**pipeline** of transformations the compiler tracks by value equality: a\nkeystroke re-runs only the steps whose inputs actually changed.\n\n```csharp\nvar provider = ctx.SyntaxProvider.ForAttributeWithMetadataName(...)\n    .Select(static (name, _) => name.ToUpperInvariant())   // pure transform\n    .Collect();                                            // gather into ImmutableArray\n\nctx.RegisterSourceOutput(provider, static (spc, names) => { /* emit once */ });\n```\n\nThe performance contract, from the Roslyn team\'s own guidance:\n\n1. **Transformations must be pure and cheap** — they may run many times;\n   their results are cached by equality.\n2. **`ForAttributeWithMetadataName` first.** It is a heavily-optimized\n   provider for the dominant pattern (find types with attribute X); hand-\n   rolled `CreateSyntaxProvider` predicates run more often and do more work.\n3. **`Collect()` deliberately** — collecting defeats incrementalism for the\n   steps after it; do per-item work before collecting, then emit once.\n4. **Lambda hygiene**: all pipeline lambdas must be `static` (no captured\n   variables) — capturing silently breaks the caching contract.\n\nWhen generators go wrong in production, it is almost always a pipeline\nthat recomputes a whole-project model per keystroke — the fix is always\n"push work later, make steps cheap, cache by value".\n'
_m7_incremental_vi = '## Incremental generators\n\n`ISourceGenerator` cổ điển chạy lại mọi thứ sau mỗi thay đổi — ổn với công\ncụ tí hon, tàn bạo với IDE. `IIncrementalGenerator` thay vào đó dựng một\n**pipeline** các phép biến đổi mà compiler theo dõi bằng so sánh giá trị:\nmột phím gõ chỉ chạy lại các bước mà input thật sự thay đổi.\n\n```csharp\nvar provider = ctx.SyntaxProvider.ForAttributeWithMetadataName(...)\n    .Select(static (name, _) => name.ToUpperInvariant())   // biến đổi thuần\n    .Collect();                                            // gom thành ImmutableArray\n\nctx.RegisterSourceOutput(provider, static (spc, names) => { /* phát một lần */ });\n```\n\nHợp đồng hiệu năng, theo đúng hướng dẫn của đội Roslyn:\n\n1. **Phép biến đổi phải thuần và rẻ** — chúng có thể chạy nhiều lần; kết\n   quả được cache theo so sánh giá trị.\n2. **`ForAttributeWithMetadataName` trước tiên.** Đây là provider được tối\n   ưu mạnh cho pattern chủ đạo (tìm kiểu có attribute X); predicate\n   `CreateSyntaxProvider` viết tay chạy thường hơn và làm nhiều việc hơn.\n3. **`Collect()` có chủ đích** — collect phá tính tăng dần cho các bước\n   sau nó; làm việc từng phần tử trước khi collect, rồi phát một lần.\n4. **Vệ sinh lambda**: mọi lambda pipeline phải `static` (không bắt biến) —\n   capture âm thầm phá hợp đồng caching.\n\nKhi generator lỗi trong production, gần như luôn là pipeline tính lại mô\nhình toàn dự án cho mỗi phím gõ — cách sửa luôn là "đẩy việc về sau, làm\ncho từng bước rẻ, cache theo giá trị".\n'
_m7_rules = "## Rules of generated code\n\nGenerated source has one reader that never forgives: the compiler. The\ncontracts that keep generators shippable:\n\n- **Fully qualify everything.** Generated code cannot rely on the user's\n  `using` directives — `System.DateTime`, not `DateTime`; or emit explicit\n  `using` blocks scoped in a namespace. The classic failure: a generated\n  DTO using `DateTime` compiles in your test project and fails in the\n  user's namespace where `DateTime` means something else.\n- **Emit diagnostics, not exceptions.** A generator that throws breaks the\n  build with an incomprehensible error; a generator that reports a proper\n  diagnostic points at the user's actual mistake.\n- **Namespace your output** — generated types colliding with user types is\n  a name-resolution bug users cannot debug.\n- **Mark partial, extend nothing**: generate `partial` classes the user\n  opts into extending, never edit their declared members.\n- **Debuggability**: `#line` directives or clean, formatted output so the\n  generated file reads sanely when a stack trace points into it.\n\nTesting generators happens exactly like the checkpoint does it: drive\n`CSharpGeneratorDriver`, inspect the generated trees, compile the OUTPUT,\nand assert zero error diagnostics. That is also how CI guards a generator\nagainst Roslyn version upgrades.\n"
_m7_rules_vi = '## Luật của generated code\n\nGenerated source có một người đọc không bao giờ thứ thứ: compiler. Những\nhợp đồng giữ generator đáng ship:\n\n- **Fully qualify mọi thứ.** Generated code không thể dựa vào `using` của\n  người dùng — `System.DateTime`, không phải `DateTime`; hoặc phát khối\n  `using` tường minh trong namespace. Thất bại kinh điển: một DTO sinh ra\n  dùng `DateTime` biên dịch ổn trong dự án test của bạn nhưng hỏng trong\n  namespace của người dùng, nơi `DateTime` là thứ khác.\n- **Phát diagnostic, không phải exception.** Generator ném exception phá\n  build với lỗi khó hiểu; generator báo diagnostic đúng cách trỏ vào lỗi\n  thật của người dùng.\n- **Namespace cho output** — kiểu sinh ra va chạm với kiểu của người dùng là\n  bug phân giải tên mà người dùng không thể debug.\n- **Đánh dấu partial, không mở rộng gì**: sinh lớp `partial` mà người dùng\n  chủ động chọn để mở rộng, không bao giờ sửa member họ khai báo.\n- **Khả năng debug**: directive `#line` hoặc output sạch, có format để file\n  sinh ra đọc được khi stack trace trỏ vào đó.\n\nKiểm thử generator diễn ra đúng như checkpoint làm: chạy\n`CSharpGeneratorDriver`, soi các tree sinh ra, biên dịch OUTPUT, và khẳng\nđịnh không có diagnostic lỗi. Đó cũng là cách CI bảo vệ generator trước các\nbản nâng cấp Roslyn.\n'
_m7_checkpoint = '## Checkpoint: source generators\n\nThe graded task drives a real incremental generator end to end: marker\nattribute via post-initialization, `ForAttributeWithMetadataName` discovery,\ncatalog emission, symbol resolution in the output compilation. Passing it\nmeans you can build and VERIFY a generator — the same loop CI uses.\n'
_m7_checkpoint_vi = '## Checkpoint: source generators\n\nBài được chấm chạy một incremental generator thật từ đầu tới cuối: marker\nattribute qua post-initialization, khám phá bằng `ForAttributeWithMetadataName`,\nphát catalog, resolve symbol trong output compilation. Pass nghĩa là bạn\nxây và XÁC MINH được generator — đúng vòng lặp mà CI dùng.\n'

"""
Authoring notes — regeneration loop: `python3 csa_emit.py` rewrites every
EN/VI JSON + MDX under the course dir, then
`node --import tsx validate-content-csa.ts` proves both locales load.
"""
