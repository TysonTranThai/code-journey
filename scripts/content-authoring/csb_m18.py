#!/usr/bin/env python3
"""C# — Beginner — Module 18: csb-cli.

How real C# projects are shaped: .csproj, dotnet new/build/run, project
references, and the anatomy of a solution. Verified in-sandbox: the
hardened container runs the SDK; challenges stay single-TU with honest
simulations of project files as data. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-cli"

write_module(
    M,
    ".NET Project Structure and CLI",
    "From single files to real projects: .csproj anatomy, the dotnet CLI verbs, and how solutions bind projects together.",
    "Cấu trúc dự án .NET và CLI",
    "Từ tệp đơn lẻ tới dự án thật: giải phẫu .csproj, các động từ của dotnet CLI, và cách solution buộc các dự án lại với nhau.",
    ["csb-m18-csproj", "csb-m18-dotnet-cli", "csb-m18-solutions", "csb-checkpoint-m18"],
    ["csb-p18-cli"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m18-csproj",
    "The .csproj file",
    "A project file is data: target framework, project references, and build settings in XML.",
    12,
    r"""
## Anatomy

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

- **Sdk** — which build toolset owns the file (the modern, convention-based SDK).
- **OutputType** — `Exe` (console app) or library (the line is absent).
- **TargetFramework** — the runtime API surface your code compiles against: `net10.0` means .NET 10 APIs.
- **Nullable** — turns nullable-reference-type warnings on.
- **ImplicitUsings** — injects the common `using` lines so every file doesn't repeat them.

Source files are discovered by convention: every `.cs` under the project directory compiles. You never list them.

## What beginners touch

Almost nothing at first — `dotnet new console` writes a correct file. You'll edit it when you add a dependency (`<PackageReference>`), reference another project (`<ProjectReference>`), or flip `Nullable`.
""",
    "Tệp .csproj",
    "Tệp dự án là dữ liệu: target framework, tham chiếu dự án, và thiết lập build dưới dạng XML.",
    r"""
## Giải phẫu

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

- **Sdk** — bộ công cụ build nào sở hữu tệp (SDK hiện đại dựa trên quy ước).
- **OutputType** — `Exe` (ứng dụng console) hoặc thư viện (bỏ qua dòng này).
- **TargetFramework** — bề mặt API runtime mà mã của bạn biên dịch dựa vào: `net10.0` nghĩa là các API của .NET 10.
- **Nullable** — bật cảnh báo nullable-reference-type.
- **ImplicitUsings** — tự chèn các dòng `using` thông dụng để mỗi tệp không lặp lại.

Các tệp nguồn được phát hiện theo quy ước: mọi `.cs` dưới thư mục dự án đều được biên dịch. Bạn không bao giờ liệt kê chúng.

## Người mới chạm vào gì

Gần như không gì lúc đầu — `dotnet new console` viết sẵn một tệp đúng. Bạn sẽ sửa nó khi thêm dependency (`<PackageReference>`), tham chiếu dự án khác (`<ProjectReference>`), hoặc bật `Nullable`.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m18-dotnet-cli",
    "The dotnet CLI verbs",
    "new, build, run, test, publish — five verbs cover the daily loop of a console developer.",
    13,
    r"""
## The daily loop

```bash
dotnet new console -o MyApp    # scaffold a console project
cd MyApp
dotnet run                     # compile + execute
dotnet build                   # compile without running
dotnet test                    # run the test project(s)
dotnet publish -c Release      # ship-ready output
```

`dotnet run` is the edit–compile–execute loop; it rebuilds changed files and starts the program. `build` stops before running — use it to check compilation in CI. Outputs land in `bin/` (executables) and `obj/` (intermediate files); both are safe to delete and rebuilt on the next build — they're never committed.

## Flags worth knowing early

- `-c Release` — optimized build (the default `Debug` is slower but debugger-friendly).
- `--no-restore` — skip package re-fetch when you know nothing changed.
- `-o` — target directory when scaffolding.

The CLI is scriptable — everything a GUI does, these verbs do, which is exactly what the sandbox grading uses.
""",
    "Các động từ của dotnet CLI",
    "new, build, run, test, publish — năm động từ phủ vòng lặp hằng ngày của lập trình viên console.",
    r"""
## Vòng lặp hằng ngày

```bash
dotnet new console -o MyApp    # dựng khung dự án console
cd MyApp
dotnet run                     # biên dịch + thực thi
dotnet build                   # chỉ biên dịch, không chạy
dotnet test                    # chạy các dự án kiểm thử
dotnet publish -c Release      # kết quả sẵn-sàng-phát-hành
```

`dotnet run` là vòng lặp sửa–biên-dịch–chạy; nó dựng lại các tệp thay đổi và khởi động chương trình. `build` dừng trước khi chạy — dùng để kiểm tra biên dịch trong CI. Kết quả nằm ở `bin/` (tệp chạy) và `obj/` (tệp trung gian); cả hai đều xóa được và được dựng lại ở lần build kế — không bao giờ được commit.

## Các cờ đáng biết sớm

- `-c Release` — build tối ưu (mặc định `Debug` chậm hơn nhưng thân-thiện-debugger).
- `--no-restore` — bỏ qua tải lại package khi bạn biết không có gì đổi.
- `-o` — thư mục đích khi dựng khung.

CLI có thể kịch bản hóa — mọi thứ GUI làm được, các động từ này làm được, và chính điều đó được sandbox chấm điểm sử dụng.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m18-solutions",
    "Solutions and project references",
    "A solution binds many projects; ProjectReference wires dependencies between them.",
    12,
    r"""
## The solution file

```bash
dotnet new sln -n Shop
dotnet new console -o Shop.App
dotnet new classlib -o Shop.Core
dotnet sln add Shop.App Shop.Core
```

`.sln` is a manifest listing projects — open it in an IDE and every project loads together. The layering is a *dependency direction*: `Shop.App` uses `Shop.Core`'s code, not the reverse.

## ProjectReference

```xml
<!-- Shop.App/Shop.App.csproj -->
<ItemGroup>
  <ProjectReference Include="..\Shop.Core\Shop.Core.csproj" />
</ItemGroup>
```

With that line, `Shop.App` can `using Shop.Core;` and the build system compiles Core first, then App. The difference between `ProjectReference` and `PackageReference` matters: a project reference is *your* source, rebuilt with the solution; a package reference is someone else's published binary from NuGet, versioned and immutable.
""",
    "Solution và tham chiếu dự án",
    "Solution buộc nhiều dự án; ProjectReference đi dây phụ thuộc giữa chúng.",
    r"""
## Tệp solution

```bash
dotnet new sln -n Shop
dotnet new console -o Shop.App
dotnet new classlib -o Shop.Core
dotnet sln add Shop.App Shop.Core
```

`.sln` là một danh mục liệt kê các dự án — mở trong IDE và mọi dự án được nạp cùng nhau. Phân lớp là một *hướng phụ thuộc*: `Shop.App` dùng mã của `Shop.Core`, không ngược lại.

## ProjectReference

```xml
<!-- Shop.App/Shop.App.csproj -->
<ItemGroup>
  <ProjectReference Include="..\Shop.Core\Shop.Core.csproj" />
</ItemGroup>
```

Với dòng đó, `Shop.App` có thể `using Shop.Core;` và hệ thống build biên dịch Core trước, rồi App. Khác biệt giữa `ProjectReference` và `PackageReference` rất quan trọng: project reference là *mã nguồn của bạn*, được build cùng solution; package reference là nhị phân do người khác phát hành qua NuGet, có phiên bản và bất biến.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p18-cli",
    "Project workshop",
    "csproj parsing, dependency graphs, CLI verb effects, and release-vs-debug reasoning — project knowledge as code.",
    "Xưởng dự án",
    "Phân tích csproj, đồ thị phụ thuộc, tác động của các động từ CLI, và suy luận release-vs-debug — kiến thức dự án thành mã.",
    "csb-m18-solutions",
    40,
    "beginner",
    [
        challenge(
            "csb-p18-csproj-parse",
            "Read a .csproj as data",
            "Implement `static string? GetProperty(string csprojXml, string tag)` — return the inner text of `<tag>value</tag>` (tag without brackets), or null when absent; and `static bool IsExecutable(string csprojXml)` — true when `<OutputType>Exe</OutputType>` (case-insensitive) is present.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var xml = \"<Project><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>\";\nCj.Eq(Solution.GetProperty(xml, \"TargetFramework\"), \"net10.0\", \"tfm extracted\");\nCj.True(Solution.IsExecutable(xml), \"Exe present\");\nCj.Eq(Solution.GetProperty(xml, \"Nullable\"), null, \"absent tag -> null\");",
                    "Simple tag extraction with a defined missing contract.",
                ),
                (
                    "library",
                    "var lib = \"<Project><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>\";\nCj.False(Solution.IsExecutable(lib), \"no OutputType -> library\");\nvar lower = \"<Project><PropertyGroup><OutputType>exe</OutputType></PropertyGroup></Project>\";\nCj.True(Solution.IsExecutable(lower), \"case-insensitive match\");",
                    "Libraries lack OutputType; matching is case-insensitive.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p18-deps",
            "Build order from references",
            "Implement `static List<string> BuildOrder(List<(string Project, string DependsOn)> refs, List<string> all)` — return project names ordered so every project appears AFTER everything it depends on; deterministic: alphabetical among available projects at each step. Projects with no dependencies come first.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var refs = new List<(string, string)> { (\"app\", \"core\"), (\"tests\", \"app\"), (\"tests\", \"core\") };\nvar all = new List<string> { \"app\", \"core\", \"tests\" };\nvar order = Solution.BuildOrder(refs, all);\nCj.True(order.IndexOf(\"core\") < order.IndexOf(\"app\"), \"core before app\");\nCj.True(order.IndexOf(\"app\") < order.IndexOf(\"tests\"), \"app before tests\");\nCj.Eq(order.Count, 3, \"all projects scheduled\");",
                    "Topological order with alphabetical tie-breaking.",
                ),
                (
                    "edges",
                    "var order = Solution.BuildOrder(new List<(string, string)>(), new List<string> { \"b\", \"a\" });\nCj.Eq(string.Join(\",\", order), \"a,b\", \"no deps -> alphabetical\");",
                    "With no references, pure alphabetical order.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p18-verbs",
            "CLI verb effects",
            "Implement `static (bool Compiles, bool Runs, bool Packages) VerbEffect(string verb)` — `\"build\"` → (true, false, false); `\"run\"` → (true, true, false); `\"publish\"` → (true, true, true); `\"test\"` → (true, false, false); unknown verb → `ArgumentException`.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.True(Solution.VerbEffect(\"build\").Compiles, \"build compiles\");\nCj.False(Solution.VerbEffect(\"build\").Runs, \"build does not run\");\nvar run = Solution.VerbEffect(\"run\");\nCj.True(run.Compiles && run.Runs, \"run does both\");\nvar pub = Solution.VerbEffect(\"publish\");\nCj.True(pub.Packages, \"publish packages\");",
                    "Each verb's effect tuple pinned.",
                ),
                (
                    "test-vs-build",
                    "Cj.False(Solution.VerbEffect(\"test\").Runs, \"test does not run the app\");\nCj.True(Solution.VerbEffect(\"test\").Compiles, \"test compiles the test project\");\nbool t = false;\ntry { Solution.VerbEffect(\"deploy\"); } catch (ArgumentException) { t = true; }\nCj.True(t, \"unknown verb rejected\");",
                    "The subtle one: test compiles but never Runs the app itself.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p18-release",
            "Release vs Debug reasoning",
            "Implement `static string ConfigAdvice(string scenario)` mapping: \"shipping\" → \"Release\", \"debugging-a-crash\" → \"Debug\", \"ci-compile-check\" → \"Debug\", \"benchmarking\" → \"Release\", unknown → \"?\".",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.ConfigAdvice(\"shipping\"), \"Release\", \"ship optimized\");\nCj.Eq(Solution.ConfigAdvice(\"debugging-a-crash\"), \"Debug\", \"debug symbols matter\");\nCj.Eq(Solution.ConfigAdvice(\"benchmarking\"), \"Release\", \"benchmarks must measure optimized\");",
                    "The reasoning: optimization vs debuggability.",
                ),
                (
                    "unknown",
                    "Cj.Eq(Solution.ConfigAdvice(\"ci-compile-check\"), \"Debug\", \"compile check uses default\");\nCj.Eq(Solution.ConfigAdvice(\"mystery\"), \"?\", \"unknown scenario\");",
                    "Default config is Debug; unmatched scenarios answer honestly.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p18-csproj-parse": vi_challenge(
            "Đọc .csproj như dữ liệu",
            "Hiện thực `static string? GetProperty(string csprojXml, string tag)` — trả nội dung bên trong của `<tag>value</tag>` (tag không có ngoặc), hoặc null khi vắng; và `static bool IsExecutable(string csprojXml)` — true khi có `<OutputType>Exe</OutputType>` (không phân biệt chữ hoa/thường).",
            [
                ("normal", "Trích xuất tag đơn giản với hợp đồng thiếu-vắng được định nghĩa."),
                ("library", "Thư viện thiếu OutputType; so khớp không phân biệt chữ hoa/thường."),
            ],
        ),
        "csb-p18-deps": vi_challenge(
            "Thứ tự build từ tham chiếu",
            "Hiện thực `static List<string> BuildOrder(List<(string Project, string DependsOn)> refs, List<string> all)` — trả tên các dự án sao cho mọi dự án xuất hiện SAU tất cả những gì nó phụ thuộc; xác định: theo alphabet giữa các dự án khả-dụng ở mỗi bước. Dự án không phụ thuộc đứng trước.",
            [
                ("normal", "Thứ tự topo với phá-hòa theo alphabet."),
                ("edges", "Không có tham chiếu thì thuần alphabet."),
            ],
        ),
        "csb-p18-verbs": vi_challenge(
            "Tác động của các động từ CLI",
            "Hiện thực `static (bool Compiles, bool Runs, bool Packages) VerbEffect(string verb)` — `\"build\"` → (true, false, false); `\"run\"` → (true, true, false); `\"publish\"` → (true, true, true); `\"test\"` → (true, false, false); động từ lạ → `ArgumentException`.",
            [
                ("normal", "Bộ tuple tác động của mỗi động từ được ghim."),
                ("test-vs-build", "Điều tinh tế: test biên dịch nhưng không bao giờ Runs ứng dụng."),
            ],
        ),
        "csb-p18-release": vi_challenge(
            "Suy luận Release vs Debug",
            "Hiện thực `static string ConfigAdvice(string scenario)` ánh xạ: \"shipping\" → \"Release\", \"debugging-a-crash\" → \"Debug\", \"ci-compile-check\" → \"Debug\", \"benchmarking\" → \"Release\", lạ → \"?\".",
            [
                ("normal", "Lý do: tối ưu hóa vs khả năng gỡ lỗi."),
                ("unknown", "Cấu hình mặc định là Debug; kịch bản lạ được trả lời trung thực."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p18-csproj-parse",
            'public class Solution\n{\n    public static string? GetProperty(string csprojXml, string tag)\n    {\n        string open = "<" + tag + ">";\n        string close = "</" + tag + ">";\n        int i = csprojXml.IndexOf(open, StringComparison.Ordinal);\n        if (i < 0) return null;\n        int start = i + open.Length;\n        int end = csprojXml.IndexOf(close, start, StringComparison.Ordinal);\n        if (end < 0) return null;\n        return csprojXml.Substring(start, end - start);\n    }\n    public static bool IsExecutable(string csprojXml)\n    {\n        return csprojXml.IndexOf("<OutputType>Exe</OutputType>", StringComparison.OrdinalIgnoreCase) >= 0;\n    }\n}\n',
            'public class Solution\n{\n    public static string? GetProperty(string csprojXml, string tag)\n    {\n        string open = "<" + tag + ">";\n        string close = "</" + tag + ">";\n        int i = csprojXml.IndexOf(open, StringComparison.Ordinal);\n        if (i < 0) return null;\n        int start = i + open.Length;\n        int end = csprojXml.IndexOf(close, start, StringComparison.Ordinal);\n        if (end < 0) return null;\n        return csprojXml.Substring(start, end - start);\n    }\n    public static bool IsExecutable(string csprojXml)\n    {\n        // near-miss: case-SENSITIVE match — a hand-edited csproj with\n        // lowercase "exe" is misclassified as a library\n        return csprojXml.IndexOf("<OutputType>Exe</OutputType>", StringComparison.Ordinal) >= 0;\n    }\n}\n',
        ),
        (
            "csb-p18-deps",
            'public class Solution\n{\n    public static List<string> BuildOrder(List<(string Project, string DependsOn)> refs, List<string> all)\n    {\n        var remaining = new List<string>(all);\n        var result = new List<string>();\n        while (remaining.Count > 0)\n        {\n            var ready = remaining\n                .Where(p => !refs.Any(r => r.Project == p && remaining.Contains(r.DependsOn)))\n                .OrderBy(p => p, StringComparer.Ordinal)\n                .ToList();\n            if (ready.Count == 0) return result;   // cycle guard (not graded)\n            foreach (string p in ready)\n            {\n                result.Add(p);\n                remaining.Remove(p);\n            }\n        }\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static List<string> BuildOrder(List<(string Project, string DependsOn)> refs, List<string> all)\n    {\n        var remaining = new List<string>(all);\n        var result = new List<string>();\n        while (remaining.Count > 0)\n        {\n            var ready = remaining\n                // near-miss: picks projects whose dependencies are merely\n                // LISTED anywhere (not still remaining) — projects scheduled\n                // before their dependencies are ready\n                .Where(p => !refs.Any(r => r.Project == p))\n                .OrderBy(p => p, StringComparer.Ordinal)\n                .ToList();\n            if (ready.Count == 0) return result;\n            foreach (string p in ready)\n            {\n                result.Add(p);\n                remaining.Remove(p);\n            }\n        }\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p18-verbs",
            'public class Solution\n{\n    public static (bool Compiles, bool Runs, bool Packages) VerbEffect(string verb)\n    {\n        switch (verb)\n        {\n            case "build": return (true, false, false);\n            case "run": return (true, true, false);\n            case "publish": return (true, true, true);\n            case "test": return (true, false, false);\n            default: throw new ArgumentException("unknown verb");\n        }\n    }\n}\n',
            'public class Solution\n{\n    public static (bool Compiles, bool Runs, bool Packages) VerbEffect(string verb)\n    {\n        switch (verb)\n        {\n            // near-miss: "run" marked as not compiling — but dotnet run\n            // builds first, then executes\n            case "build": return (true, false, false);\n            case "run": return (false, true, false);\n            case "publish": return (true, true, true);\n            case "test": return (true, false, false);\n            default: throw new ArgumentException("unknown verb");\n        }\n    }\n}\n',
        ),
        (
            "csb-p18-release",
            'public class Solution\n{\n    public static string ConfigAdvice(string scenario)\n    {\n        switch (scenario)\n        {\n            case "shipping": return "Release";\n            case "debugging-a-crash": return "Debug";\n            case "ci-compile-check": return "Debug";\n            case "benchmarking": return "Release";\n            default: return "?";\n        }\n    }\n}\n',
            'public class Solution\n{\n    public static string ConfigAdvice(string scenario)\n    {\n        switch (scenario)\n        {\n            // near-miss: benchmarking on Debug — measurements of unoptimized\n            // builds mislead every performance decision\n            case "shipping": return "Release";\n            case "debugging-a-crash": return "Debug";\n            case "ci-compile-check": return "Debug";\n            case "benchmarking": return "Debug";\n            default: return "?";\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m18",
    "Checkpoint — Projects & CLI",
    "A project planner: dependency validation, scaffold commands, and a build-pipeline simulator.",
    20,
    r"""
## Checkpoint: the project planner

**Task:** implement in `Solution`:

1. `static bool HasCycle(List<(string Project, string DependsOn)> refs)` — true when the dependency graph contains a cycle (A→B→A).
2. `static string ScaffoldCommand(string kind, string name)` — `"console"` → `dotnet new console -o {name}`; `"classlib"` → `dotnet new classlib -o {name}`; unknown kind → `ArgumentException`.
3. `static List<string> FailingProjects(List<(string Project, string DependsOn)> refs, List<string> broken)` — projects that are broken or transitively depend on a broken one (alphabetical order).
""",
    "Checkpoint — Dự án & CLI",
    "Bộ lập kế hoạch dự án: kiểm tra phụ thuộc vòng, lệnh dựng khung, và mô phỏng đường ống build.",
    r"""
## Checkpoint: bộ lập kế hoạch dự án

**Nhiệm vụ:** hiện thực trong `Solution`:

1. `static bool HasCycle(List<(string Project, string DependsOn)> refs)` — true khi đồ thị phụ thuộc chứa một chu trình (A→B→A).
2. `static string ScaffoldCommand(string kind, string name)` — `"console"` → `dotnet new console -o {name}`; `"classlib"` → `dotnet new classlib -o {name}`; kind lạ → `ArgumentException`.
3. `static List<string> FailingProjects(List<(string Project, string DependsOn)> refs, List<string> broken)` — các dự án bị hỏng hoặc phụ thuộc bắc-cầu vào một dự án hỏng (thứ tự alphabet).
""",
    challenge(
        "csb-checkpoint-m18-task",
        "ProjectPlanner",
        "Implement `HasCycle`, `ScaffoldCommand`, and `FailingProjects` — graph reasoning plus honest command construction; a diamond graph converges but never cycles.",
        CS_PRELUDE,
        [
            (
                "cycle-and-scaffold",
                "Cj.False(Solution.HasCycle(new List<(string, string)> { (\"app\", \"core\") }), \"linear is fine\");\nCj.True(Solution.HasCycle(new List<(string, string)> { (\"a\", \"b\"), (\"b\", \"a\") }), \"a<->b cycles\");\nCj.False(Solution.HasCycle(new List<(string, string)> { (\"a\", \"c\"), (\"b\", \"c\") }), \"diamond convergence is not a cycle\");\nCj.Eq(Solution.ScaffoldCommand(\"console\", \"MyApp\"), \"dotnet new console -o MyApp\", \"console command\");\nCj.Eq(Solution.ScaffoldCommand(\"classlib\", \"Core\"), \"dotnet new classlib -o Core\", \"classlib command\");\nbool t = false;\ntry { Solution.ScaffoldCommand(\"winforms\", \"X\"); } catch (ArgumentException) { t = true; }\nCj.True(t, \"unknown kind rejected\");",
                "Cycle detection and exact command strings.",
            ),
            (
                "transitive",
                "var refs = new List<(string, string)> { (\"app\", \"core\"), (\"tests\", \"app\") };\nvar failing = Solution.FailingProjects(refs, new List<string> { \"core\" });\nCj.Eq(string.Join(\",\", failing), \"app,core,tests\", \"broken one included, dependents follow\");\nvar none = Solution.FailingProjects(refs, new List<string>());\nCj.Eq(none.Count, 0, \"nothing broken\");",
                "Transitive failure propagation through the reference graph — the broken project itself is in the answer too.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "ProjectPlanner",
        "Hiện thực `HasCycle`, `ScaffoldCommand`, và `FailingProjects` — suy luận đồ thị cộng dựng lệnh trung thực; đồ thị hình thoi hội tụ nhưng không bao giờ tạo chu trình.",
        [
            ("cycle-and-scaffold", "Phát hiện chu trình và các chuỗi lệnh chính xác."),
            ("transitive", "Lan truyền thất bại bắc-cầu qua đồ thị tham chiếu — chính dự án bị hỏng cũng nằm trong kết quả."),
        ],
    ),
    solution='public class Solution\n{\n    public static bool HasCycle(List<(string Project, string DependsOn)> refs)\n    {\n        var map = new Dictionary<string, List<string>>();\n        foreach (var r in refs)\n        {\n            if (!map.TryGetValue(r.Project, out var list)) map[r.Project] = list = new List<string>();\n            list.Add(r.DependsOn);\n        }\n        var visiting = new HashSet<string>();\n        var done = new HashSet<string>();\n        bool Dfs(string node)\n        {\n            if (done.Contains(node)) return false;\n            if (!visiting.Add(node)) return true;\n            if (map.TryGetValue(node, out var deps))\n            {\n                foreach (string d in deps)\n                {\n                    if (Dfs(d)) return true;\n                }\n            }\n            visiting.Remove(node);\n            done.Add(node);\n            return false;\n        }\n        foreach (string node in map.Keys)\n        {\n            if (Dfs(node)) return true;\n        }\n        return false;\n    }\n    public static string ScaffoldCommand(string kind, string name)\n    {\n        switch (kind)\n        {\n            case "console": return $"dotnet new console -o {name}";\n            case "classlib": return $"dotnet new classlib -o {name}";\n            default: throw new ArgumentException("unknown project kind");\n        }\n    }\n    public static List<string> FailingProjects(List<(string Project, string DependsOn)> refs, List<string> broken)\n    {\n        var brokenSet = new HashSet<string>(broken);\n        bool changed = true;\n        while (changed)\n        {\n            changed = false;\n            foreach (var r in refs)\n            {\n                if (brokenSet.Contains(r.DependsOn) && brokenSet.Add(r.Project)) changed = true;\n            }\n        }\n        return brokenSet.OrderBy(p => p, StringComparer.Ordinal).ToList();\n    }\n}\n',
    wrong='public class Solution\n{\n    public static bool HasCycle(List<(string Project, string DependsOn)> refs)\n    {\n        var map = new Dictionary<string, List<string>>();\n        foreach (var r in refs)\n        {\n            if (!map.TryGetValue(r.Project, out var list)) map[r.Project] = list = new List<string>();\n            list.Add(r.DependsOn);\n        }\n        var visiting = new HashSet<string>();\n        var done = new HashSet<string>();\n        bool Dfs(string node)\n        {\n            if (done.Contains(node)) return false;\n            // near-miss: marks visited without removing on exit — a diamond\n            // graph (two paths to the same node) is misreported as a cycle\n            if (!visiting.Add(node)) return true;\n            if (map.TryGetValue(node, out var deps))\n            {\n                foreach (string d in deps)\n                {\n                    if (Dfs(d)) return true;\n                }\n            }\n            return false;\n        }\n        foreach (string node in map.Keys)\n        {\n            if (Dfs(node)) return true;\n        }\n        return false;\n    }\n    public static string ScaffoldCommand(string kind, string name)\n    {\n        switch (kind)\n        {\n            case "console": return $"dotnet new console -o {name}";\n            case "classlib": return $"dotnet new classlib -o {name}";\n            default: throw new ArgumentException("unknown project kind");\n        }\n    }\n    public static List<string> FailingProjects(List<(string Project, string DependsOn)> refs, List<string> broken)\n    {\n        var brokenSet = new HashSet<string>(broken);\n        bool changed = true;\n        while (changed)\n        {\n            changed = false;\n            foreach (var r in refs)\n            {\n                if (brokenSet.Contains(r.DependsOn) && brokenSet.Add(r.Project)) changed = true;\n            }\n        }\n        return brokenSet.OrderBy(p => p, StringComparer.Ordinal).ToList();\n    }\n}\n',
)

print("module 18 authored")
