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
