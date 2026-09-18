"""Module 6 — Roslyn and compiler APIs (csa-m6)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-roslyn",
        "Roslyn and Compiler APIs",
        "Syntax trees, semantic models, symbols, diagnostics — and analyzers that read your code like the compiler does.",
    )

    csa.register_lesson(
        MID, "csa-m6-roslyn-architecture", "Roslyn's two views of code",
        "SyntaxTree vs SemanticModel: green/red trees, symbols, and why the split enables IDEs.",
        15, "advanced", _m6_architecture, _m6_architecture_vi,
    )
    csa.register_lesson(
        MID, "csa-m6-analyzers", "Writing analyzers and diagnostics",
        "Analyzer architecture, diagnostic descriptors, incremental registration, and fixing instead of failing.",
        16, "advanced", _m6_analyzers, _m6_analyzers_vi,
    )
    csa.register_lesson(
        MID, "csa-m6-compilation-api", "The Compilation API",
        "CSharpCompilation end to end: references, diagnostics, emitting assemblies — all inside this sandbox.",
        15, "advanced", _m6_compilation, _m6_compilation_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m6", "Checkpoint: Roslyn",
        "Synthesis: walk syntax, resolve symbols, and drive a compilation programmatically.",
        12, "advanced", _m6_checkpoint, _m6_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m6-task", MID,
        title="Roslyn checkpoint",
        prompt=(
            "Implement `static string[] PublicMethodNames(string source)`: parse `source` with CSharpSyntaxTree."
            "ParseText, find all MethodDeclarationSyntax nodes, and return their identifiers sorted. Then implement "
            "`static bool Compiles(string source)`: build a CSharpCompilation (OutputKind.DynamicallyLinkedLibrary) "
            "over that source with the references from AppDomain.CurrentDomain.GetAssemblies() filtered to "
            "IsDynamic == false && Location != string.Empty, and return it has zero error diagnostics."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "syntax-walk",
                "code": (
                    "var src = \"public class A { public void Run() { } public void Stop() { } private void X() { } }\";\n"
                    "var names = Solution.PublicMethodNames(src);\n"
                    'Cj.True(names.Contains("Run") && names.Contains("Stop"), "public methods found");\n'
                    "// Syntax-only view sees ALL methods regardless of accessibility:\n"
                    'Cj.True(names.SequenceEqual(names.OrderBy(n => n)), "sorted");'
                ),
                "hint": "tree.GetRoot().DescendantNodes().OfType<MethodDeclarationSyntax>() — collect Identifier.ValueText.",
            },
            {
                "name": "semantic-verify",
                "code": (
                    "Cj.True(Solution.Compiles(\"public class A { public int X { get; set; } }\"), \"valid compiles\");\n"
                    "Cj.False(Solution.Compiles(\"public class A { void M() { this is not valid } }\"), \"garbage fails\");"
                ),
                "hint": "CSharpCompilation.Create with syntax trees + references; check diags where Severity == DiagnosticSeverity.Error.",
            },
        ],
        reference=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.CSharp.Syntax;\n\n"
            "public class Solution\n{\n"
            "    public static string[] PublicMethodNames(string source)\n    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(source);\n"
            "        return tree.GetRoot().DescendantNodes().OfType<MethodDeclarationSyntax>()\n"
            "            .Select(m => m.Identifier.ValueText)\n"
            "            .OrderBy(n => n, StringComparer.Ordinal)\n"
            "            .ToArray();\n"
            "    }\n\n"
            "    public static bool Compiles(string source)\n    {\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"check\",\n"
            "            new[] { CSharpSyntaxTree.ParseText(source) }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        return !comp.GetDiagnostics().Any(d => d.Severity == DiagnosticSeverity.Error);\n"
            "    }\n}"
        ),
        wrong=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.CSharp.Syntax;\n\n"
            "public class Solution\n{\n"
            "    public static string[] PublicMethodNames(string source)\n    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(source);\n"
            "        return tree.GetRoot().DescendantNodes().OfType<MethodDeclarationSyntax>()\n"
            "            .Select(m => m.Identifier.ValueText)\n"
            "            .ToArray();                     // WRONG: unsorted\n"
            "    }\n\n"
            "    public static bool Compiles(string source)\n    {\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"check\",\n"
            "            new[] { CSharpSyntaxTree.ParseText(source) }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        return comp.GetDiagnostics().Any(d => d.Severity == DiagnosticSeverity.Error);   // inverted\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p6-roslyn", "Roslyn drills",
        "Syntax walking, semantic resolution, diagnostic analysis, and in-process compilation.",
        45, "advanced", "csa-m6-analyzers",
        ["csa-p6-syntax-count", "csa-p6-semantic-resolve", "csa-p6-diagnostic-scan"],
    )
    csa.register_challenge(
        "csa-p6-syntax-count", MID,
        title="Syntax metrics",
        prompt=(
            "Implement `static (int methods, int classes, int invocations) Metrics(string source)`: parse the source "
            "and count MethodDeclarationSyntax nodes, ClassDeclarationSyntax nodes, and InvocationExpressionSyntax "
            "nodes. This is the code-metric tool every linter starts with."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "counts",
                "code": (
                    "var src = \"\"\"\n"
                    "public class A\n{\n"
                    "    public void M()\n    {\n"
                    "        Console.WriteLine(\"hi\");\n"
                    "        Do();\n"
                    "    }\n"
                    "    void Do() { }\n"
                    "}\n"
                    "\"\"\";\n"
                    "var (m, c, i) = Solution.Metrics(src);\n"
                    "Cj.Eq(m, 2, \"methods\");\n"
                    "Cj.Eq(c, 1, \"classes\");\n"
                    "Cj.Eq(i, 2, \"invocations\");"
                ),
                "hint": "DescendantNodes().OfType<T>().Count() for each node kind.",
            },
        ],
        reference=(
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.CSharp.Syntax;\n\n"
            "public class Solution\n{\n"
            "    public static (int methods, int classes, int invocations) Metrics(string source)\n"
            "    {\n"
            "        var root = CSharpSyntaxTree.ParseText(source).GetRoot();\n"
            "        return (\n"
            "            root.DescendantNodes().OfType<MethodDeclarationSyntax>().Count(),\n"
            "            root.DescendantNodes().OfType<ClassDeclarationSyntax>().Count(),\n"
            "            root.DescendantNodes().OfType<InvocationExpressionSyntax>().Count());\n"
            "    }\n}"
        ),
        wrong=(
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.CSharp.Syntax;\n\n"
            "public class Solution\n{\n"
            "    public static (int methods, int classes, int invocations) Metrics(string source)\n"
            "    {\n"
            "        var root = CSharpSyntaxTree.ParseText(source).GetRoot();\n"
            "        return (\n"
            "            root.DescendantNodes().OfType<MethodDeclarationSyntax>().Count(),\n"
            "            root.DescendantNodes().OfType<ClassDeclarationSyntax>().Count(),\n"
            "            root.DescendantNodes().OfType<ObjectCreationExpressionSyntax>().Count());   // wrong node kind\n"
            "    }\n}"
        ),
        level="imitation",
    )
    csa.register_challenge(
        "csa-p6-semantic-resolve", MID,
        title="Semantic resolution",
        prompt=(
            "Implement `static string TypeOfExpression(string source)`: parse the source (a single statement or "
            "expression), get the SemanticModel from a CSharpCompilation, find the first InvocationExpressionSyntax, "
            "and return the fully-qualified type name of its resolved method's ContainingType, or \"?\" when it "
            "does not resolve."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "resolution",
                "code": (
                    "var src = \"System.Console.WriteLine(42);\";\n"
                    "var t = Solution.TypeOfExpression(src);\n"
                    'Cj.Eq(t, "System.Console", "receiver resolves to Console");'
                ),
                "hint": "compilation.GetSemanticModel(tree); symbol = model.GetSymbolInfo(invocation).Symbol as IMethodSymbol; use symbol.ContainingType.ToDisplayString().",
            },
        ],
        reference=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.CSharp.Syntax;\n\n"
            "public class Solution\n{\n"
            "    public static string TypeOfExpression(string source)\n    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(source);\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"sem\", new[] { tree }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        var inv = tree.GetRoot().DescendantNodes().OfType<InvocationExpressionSyntax>().FirstOrDefault();\n"
            "        if (inv is null) return \"?\";\n"
            "        var model = comp.GetSemanticModel(tree);\n"
            "        var sym = model.GetSymbolInfo(inv).Symbol as IMethodSymbol;\n"
            "        return sym?.ContainingType?.ToDisplayString() ?? \"?\";\n"
            "    }\n}"
        ),
        wrong=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n"
            "using Microsoft.CodeAnalysis.CSharp.Syntax;\n\n"
            "public class Solution\n{\n"
            "    public static string TypeOfExpression(string source)\n    {\n"
            "        var tree = CSharpSyntaxTree.ParseText(source);\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"sem\", new[] { tree }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        var inv = tree.GetRoot().DescendantNodes().OfType<ObjectCreationExpressionSyntax>().FirstOrDefault();\n"
            "        if (inv is null) return \"?\";\n"
            "        var model = comp.GetSemanticModel(tree);\n"
            "        var sym = model.GetDeclaredSymbol((TypeDeclarationSyntax)tree.GetRoot().ChildNodes().First()) as INamedTypeSymbol;\n"
            "        return sym?.ToDisplayString() ?? \"?\";   // WRONG node and wrong symbol kind\n"
            "    }\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p6-diagnostic-scan", MID,
        title="Diagnostic scan",
        prompt=(
            "Implement `static List<string> CompilerWarnings(string source)`: compile the source as a library and "
            "return the IDs (d.Id) of all WARNING-severity diagnostics (no errors expected in the given inputs), "
            "deduplicated and sorted. Example input that warns: \"public class A { public int X; }\" — CS0169 "
            "(unused field) only appears when the field is private and never used; public fields do not warn, so "
            "use \"public class A { int y; }\" for the warning case."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "warnings",
                "code": (
                    "var w = Solution.CompilerWarnings(\"public class A { int y; }\");\n"
                    'Cj.True(w.Contains("CS0169"), $"unused field warns: [{string.Join(\",\", w)}]");\n'
                    "var clean = Solution.CompilerWarnings(\"public class A { public int X { get; set; } }\");\n"
                    'Cj.Eq(clean.Count, 0, "no warnings for auto-property");'
                ),
                "hint": "GetDiagnostics() returns warnings and errors; filter Severity == Warning; Distinct().OrderBy().ToList().",
            },
        ],
        reference=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n\n"
            "public class Solution\n{\n"
            "    public static List<string> CompilerWarnings(string source)\n    {\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"warn\", new[] { CSharpSyntaxTree.ParseText(source) }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        return comp.GetDiagnostics()\n"
            "            .Where(d => d.Severity == DiagnosticSeverity.Warning)\n"
            "            .Select(d => d.Id)\n"
            "            .Distinct()\n"
            "            .OrderBy(id => id, StringComparer.Ordinal)\n"
            "            .ToList();\n"
            "    }\n}"
        ),
        wrong=(
            "using Microsoft.CodeAnalysis;\n"
            "using Microsoft.CodeAnalysis.CSharp;\n\n"
            "public class Solution\n{\n"
            "    public static List<string> CompilerWarnings(string source)\n    {\n"
            "        var refs = AppDomain.CurrentDomain.GetAssemblies()\n"
            "            .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))\n"
            "            .Select(a => MetadataReference.CreateFromFile(a.Location));\n"
            "        var comp = CSharpCompilation.Create(\"warn\", new[] { CSharpSyntaxTree.ParseText(source) }, refs,\n"
            "            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));\n"
            "        return comp.GetDiagnostics()\n"
            "            .Where(d => d.Severity == DiagnosticSeverity.Error)   // WRONG severity\n"
            "            .Select(d => d.Id)\n"
            "            .Distinct()\n"
            "            .OrderBy(id => id, StringComparer.Ordinal)\n"
            "            .ToList();\n"
            "    }\n}"
        ),
        level="independent",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m6_architecture = r"""## Roslyn's two views of code

Roslyn is the compiler-as-a-service: the same engine that builds your code
is a library you reference. It exposes two cooperating layers:

- **Syntax layer** (`SyntaxTree`, `CSharpSyntaxWalker`): the exact text as
  a tree — every brace, every keyword, including trivia (comments,
  whitespace). Purely lexical: an unresolvable typo still parses.
- **Semantic layer** (`SemanticModel`, `ISymbol`): what the identifiers
  MEAN — resolved types, method overloads, accessibility, nullable flow.
  Needs a `Compilation` with references.

```csharp
var tree = CSharpSyntaxTree.ParseText("int x = 1;");
var comp = CSharpCompilation.Create("scratch", new[] { tree },
    new[] { MetadataReference.CreateFromFile(typeof(object).Assembly.Location) });
var model = comp.GetSemanticModel(tree);
```

Two design decisions make the IDE world possible: syntax trees are
**immutable** (share and cache freely) and **repirseparable** (a tree
remembers how to re-create its exact text, so round-tripping is lossless).
Roslyn's red/green tree makes incremental edits cheap — you mostly notice
this as "analyzers don't reanalyze the whole file per keystroke".

When to use which: linting shape (naming, structure, forbidden patterns) is
syntax; correctness rules (null-ability, type mismatches, symbol misuse)
are semantic. Analyzers that need semantic info get it lazily — the
registration API takes a predicate deciding whether a node is worth
resolving at all.
"""

_m6_architecture_vi = r"""## Hai góc nhìn của Roslyn về mã nguồn

Roslyn là compiler-as-a-service: chính engine biên dịch code của bạn là một
thư viện bạn tham chiếu. Nó phơi hai tầng phối hợp:

- **Tầng syntax** (`SyntaxTree`, `CSharpSyntaxWalker`): chính xác văn bản
  dưới dạng cây — từng ngoặc, từng keyword, kể cả trivia (comment,
  whitespace). Thuần từ vựng: một lỗi chính tả không resolve được vẫn parse
  bình thường.
- **Tầng semantic** (`SemanticModel`, `ISymbol`): định danh NGHĨA là gì —
  kiểu đã resolve, overload, khả năng truy cập, nullable flow. Cần một
  `Compilation` với các tham chiếu.

```csharp
var tree = CSharpSyntaxTree.ParseText("int x = 1;");
var comp = CSharpCompilation.Create("scratch", new[] { tree },
    new[] { MetadataReference.CreateFromFile(typeof(object).Assembly.Location) });
var model = comp.GetSemanticModel(tree);
```

Hai quyết định thiết kế làm nên thế giới IDE: syntax tree **bất biến**
(chia sẻ và cache tự do) và **repirseparable** (cây nhớ cách tái tạo chính
xác văn bản của nó, nên round-trip không mất dữ liệu). Cây đỏ/xanh của
Roslyn giúp chỉnh sửa tăng dần rẻ — bạn chủ yếu thấy điều đó ở chỗ "analyzer
không phân tích lại cả file cho mỗi phím gõ".

Khi nào dùng tầng nào: linting hình dạng (đặt tên, cấu trúc, pattern bị cấm)
là syntax; luật đúng-sai (null-ability, sai kiểu, dùng symbol sai) là
semantic. Analyzer cần thông tin semantic sẽ lấy lười — API đăng ký nhận một
predicate quyết định node có đáng resolve hay không.
"""

_m6_analyzers = r"""## Writing analyzers and diagnostics

An analyzer is a Roslyn `DiagnosticAnalyzer`: register callbacks per syntax
node kind, inspect, and report `Diagnostic`s against a
`DiagnosticDescriptor` (id, severity, message template). The runtime
pattern that keeps analyzers fast:

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class EmptyCatchAnalyzer : DiagnosticAnalyzer
{
    static readonly DiagnosticDescriptor Rule = new(
        "CJ0001", "Empty catch block", "Catch of '{0}' swallows everything",
        "Reliability", DiagnosticSeverity.Warning, isEnabledByDefault: true);

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics
        => [Rule];

    public override void Initialize(AnalysisContext ctx)
    {
        ctx.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
        ctx.EnableConcurrentExecution();
        ctx.RegisterSyntaxNodeAction(Analyze, SyntaxKind.CatchClause);
    }

    static void Analyze(SyntaxNodeAnalysisContext c)
    {
        var node = (CatchClauseSyntax)c.Node;
        if (node.Block?.Statements.Count == 0)
            c.ReportDiagnostic(Diagnostic.Create(Rule, node.CatchKeyword.GetLocation(), node.Declaration));
    }
}
```

The discipline that separates useful analyzers from noise:

1. **Register narrowly** — per node kind or symbol kind, never walk the
   whole tree per compilation.
2. **Skip generated code** — `GeneratedCodeAnalysisFlags.None` avoids
   fighting the compiler's own output.
3. **Report with a location and arguments** — the message template fills
   in; the IDE can offer a code fix at that exact span.

Analyzers ship as NuGet packages and run inside the compiler — your rules
execute at build time, not in CI scripts after the fact. Code fixes are a
separate layer (`CodeFixProvider`) that offers replacements; the analyzer
only reports.
"""

_m6_analyzers_vi = r"""## Viết analyzer và diagnostic

Analyzer là một `DiagnosticAnalyzer` của Roslyn: đăng ký callback theo loại
syntax node, kiểm tra, và báo `Diagnostic` dựa trên `DiagnosticDescriptor`
(id, mức nghiêm trọng, template thông báo). Pattern runtime giúp analyzer
nhanh:

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class EmptyCatchAnalyzer : DiagnosticAnalyzer
{
    static readonly DiagnosticDescriptor Rule = new(
        "CJ0001", "Empty catch block", "Catch of '{0}' swallows everything",
        "Reliability", DiagnosticSeverity.Warning, isEnabledByDefault: true);

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics
        => [Rule];

    public override void Initialize(AnalysisContext ctx)
    {
        ctx.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
        ctx.EnableConcurrentExecution();
        ctx.RegisterSyntaxNodeAction(Analyze, SyntaxKind.CatchClause);
    }

    static void Analyze(SyntaxNodeAnalysisContext c)
    {
        var node = (CatchClauseSyntax)c.Node;
        if (node.Block?.Statements.Count == 0)
            c.ReportDiagnostic(Diagnostic.Create(Rule, node.CatchKeyword.GetLocation(), node.Declaration));
    }
}
```

Kỷ luật phân biệt analyzer hữu ích với analyzer nhiễu:

1. **Đăng ký hẹp** — theo loại node hoặc symbol, không bao giờ đi cả cây
   cho mỗi lần biên dịch.
2. **Bỏ qua generated code** — `GeneratedCodeAnalysisFlags.None` tránh đánh
   nhau với output của compiler.
3. **Báo kèm vị trí và tham số** — template thông báo được điền; IDE có thể
   đề nghị code fix ngay đúng span đó.

Analyzer được đóng gói thành package NuGet và chạy bên trong compiler — luật
của bạn thực thi lúc build, không phải script CI chạy sau. Code fix là tầng
riêng (`CodeFixProvider`) đề nghị thay thế; analyzer chỉ báo cáo.
"""

_m6_compilation = r"""## The Compilation API

`CSharpCompilation` is Roslyn's build in a function call: trees +
references + options → diagnostics + a pe-stream you can emit. Everything
in this module runs **inside the sandbox** — no dotnet CLI needed:

```csharp
var comp = CSharpCompilation.Create(
    "policy",
    new[] { CSharpSyntaxTree.ParseText(policySource) },
    references,   // MetadataReference.CreateFromFile(assembly.Location)
    new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));

var diags = comp.GetDiagnostics()
    .Where(d => d.Severity == DiagnosticSeverity.Error);

using var pe = new MemoryStream();
var result = comp.Emit(pe);
// result.Success, result.Diagnostics — the real compiler verdict
```

What the platform's own grader does for every challenge you submit: stage
your code, reference the framework assemblies, compile, run the test
harness — exactly this API shape, executed in a hardened container.

Three practical notes from real use:

- **References come from loaded assemblies**: filter
  `AppDomain.CurrentDomain.GetAssemblies()` to non-dynamic assemblies with
  a `Location` on disk. The Roslyn dlls themselves need explicit refs when
  you compile code that *uses* Roslyn (as the harness does for this course).
- `GetDiagnostics()` vs `Emit()`: emit also validates — some errors (missing
  types at link time) appear only when emitting.
- Compilation is expensive (~tens of ms per small program); batch work or
  keep compilations long-lived instead of rebuilding per request.
"""

_m6_compilation_vi = r"""## Compilation API

`CSharpCompilation` là quá trình build của Roslyn trong một lần gọi hàm:
tree + reference + option → diagnostic + pe-stream có thể emit. Mọi thứ
trong module này chạy **ngay trong sandbox** — không cần dotnet CLI:

```csharp
var comp = CSharpCompilation.Create(
    "policy",
    new[] { CSharpSyntaxTree.ParseText(policySource) },
    references,   // MetadataReference.CreateFromFile(assembly.Location)
    new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));

var diags = comp.GetDiagnostics()
    .Where(d => d.Severity == DiagnosticSeverity.Error);

using var pe = new MemoryStream();
var result = comp.Emit(pe);
// result.Success, result.Diagnostics — phán quyết của compiler thật
```

Điều mà grader của chính nền tảng này làm cho mỗi challenge bạn nộp: stage
code của bạn, tham chiếu các assembly framework, biên dịch, chạy harness
test — đúng hình dạng API này, thực thi trong container được gia cố.

Ba ghi chú thực dụng từ việc dùng thật:

- **Reference đến từ các assembly đã nạp**: lọc
  `AppDomain.CurrentDomain.GetAssemblies()` lấy assembly không động và có
  `Location` trên đĩa. Bản thân các dll Roslyn cần ref tường minh khi bạn
  biên dịch code *sử dụng* Roslyn (như harness của khóa này đã làm).
- `GetDiagnostics()` vs `Emit()`: emit cũng xác thực — một số lỗi (thiếu
  kiểu lúc link) chỉ xuất hiện khi emit.
- Biên dịch đắt (cỡ chục ms mỗi chương trình nhỏ); gom việc hoặc giữ
  compilation sống lâu thay vì dựng lại cho mỗi request.
"""

_m6_checkpoint = r"""## Checkpoint: Roslyn

Two capabilities prove compiler literacy:

1. **Syntax walk** — enumerate method declarations from raw source.
2. **Semantic verification** — a real `CSharpCompilation` answering "does
   this compile?" with diagnostics you can name.

You now hold the tools that IDEs, linters, and this platform's grader are
built from. Module 7 turns the same machinery from *reading* code to
*writing* it: source generators.
"""

_m6_checkpoint_vi = r"""## Checkpoint: Roslyn

Hai năng lực chứng minh hiểu compiler:

1. **Đi cây syntax** — liệt kê khai báo phương thức từ mã nguồn thô.
2. **Xác thực semantic** — một `CSharpCompilation` thật trả lời "cái này
   biên dịch được không?" với diagnostic gọi tên được.

Bạn giờ nắm các công cụ mà IDE, linter, và grader của chính nền tảng này
được dựng lên từ đó. Module 7 biến cùng bộ máy từ *đọc* code sang *viết*
code: source generator.
"""
