#!/usr/bin/env python3
"""C# — Beginner — Module 21: csb-capstone.

The beginner capstone: a personal finance ledger built as pure functions
over collections (the sandbox is stateless — the persistent app lives in
the project guide). Milestone 1 models the domain; the checkpoint drills
the monthly statement report. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-capstone"

# Domain model shipped in the boilerplate: the learner's Solution is
# graded against tests that construct these types directly.
CS_CAP = CS_PRELUDE + (
    "public enum Direction { Income, Expense }\n\n"
    "public record Transaction(int Id, Direction Dir, decimal Amount, string Category, string Description, DateTime Date);\n\n"
    "public record AddResult(bool Ok, string Error);\n\n"
)

write_module(
    M,
    "Beginner Capstone",
    "One domain, every tool: model transactions, validate them, aggregate them, and produce a statement — the shape of every real C# program.",
    "Capstone Cơ bản",
    "Một miền dữ liệu, mọi công cụ: mô hình hóa giao dịch, xác thực, tổng hợp, và xuất sao kê — hình dạng của mọi chương trình C# thật.",
    ["csb-m21-plan", "csb-m21-model", "csb-m21-report", "csb-checkpoint-m21"],
    ["csb-p21-capstone"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m21-plan",
    "The capstone plan",
    "Decompose the finance app into milestones — and learn which parts a stateless sandbox can grade.",
    12,
    r"""
## The product

A personal finance ledger: record income and expenses, keep a running balance, and produce a monthly statement. The full build sequence:

1. **Model** — a `Transaction` type: amount, category, description, date.
2. **Validate** — an `AddResult` that explains rejected entries instead of throwing.
3. **Aggregate** — running balance, category totals, month filtering.
4. **Report** — a monthly statement: totals, biggest category, top entries.
5. **Persist** — files (Module 14) and a project guide for assembling the real app locally.

Milestones 1–4 are graded here as pure functions over collections; milestone 5 exercises `File`/`Path` on disk in the challenges, and the project guide walks you through the full app with `dotnet` locally. Same domain, both worlds.
""",
    "Kế hoạch capstone",
    "Phân rã ứng dụng tài chính thành các cột mốc — và biết phần nào sandbox không trạng thái chấm được.",
    r"""
## Sản phẩm

Một sổ tài chính cá nhân: ghi thu và chi, giữ số dư luỹ kế, và xuất sao kê tháng. Trình tự xây dựng:

1. **Mô hình** — kiểu `Transaction`: số tiền, danh mục, mô tả, ngày.
2. **Xác thực** — `AddResult` giải thích vì sao từ chối thay vì ném exception.
3. **Tổng hợp** — số dư luỹ kế, tổng theo danh mục, lọc theo tháng.
4. **Báo cáo** — sao kê tháng: tổng, danh mục lớn nhất, các mục nổi bật.
5. **Lưu trữ** — tệp (Module 14) và hướng dẫn dự án để lắp ứng dụng thật tại chỗ.

Cột mốc 1–4 được chấm tại đây dưới dạng hàm thuần trên collection; cột mốc 5 thao tác `File`/`Path` trên đĩa trong thử thách, và hướng dẫn dự án dẫn bạn qua ứng dụng đầy đủ với `dotnet` cục bộ. Cùng một miền dữ liệu, cả hai thế giới.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m21-model",
    "Modeling the domain",
    "A record for Transaction, an enum for direction, validation that returns reasons — a small domain model done right.",
    13,
    r"""
## The types

```csharp
public enum Direction { Income, Expense }

public record Transaction(int Id, Direction Dir, decimal Amount,
                          string Category, string Description, DateTime Date);

public record AddResult(bool Ok, string Error);
```

The `record` gives value equality for free (Module 11); the enum makes invalid directions unrepresentable — `Direction.Expense` beats a magic `"out"` string the compiler can't check. `decimal` for money (Module 2): exact base-10 arithmetic, no binary-rounding surprises.

## Validation as data

`AddResult` returns *why* an entry was rejected instead of throwing: `Ok = false, Error = "amount-must-be-positive"`. Callers branch on the result; no exception cost, no control flow by crash. The error strings are the API — tests pin them.
""",
    "Mô hình hóa miền dữ liệu",
    "Một record cho Transaction, một enum cho hướng, xác thực trả về lý do — một mô hình miền nhỏ làm đúng cách.",
    r"""
## Các kiểu

```csharp
public enum Direction { Income, Expense }

public record Transaction(int Id, Direction Dir, decimal Amount,
                          string Category, string Description, DateTime Date);

public record AddResult(bool Ok, string Error);
```

`record` cho đẳng-thức-giá trị miễn phí (Module 11); enum biến hướng sai không-có-thể-diễn-đạt — `Direction.Expense` đánh bại chuỗi thần chú `"out"` mà trình biên dịch không kiểm được. `decimal` cho tiền (Module 2): số học cơ-số-10 chính xác, không bất ngờ làm tròn nhị phân.

## Xác thực thành dữ liệu

`AddResult` trả *lý do* từ chối thay vì ném: `Ok = false, Error = "amount-must-be-positive"`. Người gọi rẽ nhánh trên kết quả; không chi phí exception, không điều khiển luồng bằng tai nạn. Các chuỗi lỗi chính là API — test ghim chúng.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m21-report",
    "Aggregation and the statement",
    "LINQ folds a list of transactions into balances, category totals, and the monthly statement.",
    13,
    r"""
## Balances and totals

```csharp
decimal balance = ledger.Sum(t => t.Dir == Direction.Income ? t.Amount : -t.Amount);

var byCategory = ledger
    .GroupBy(t => t.Category)
    .Select(g => new { Category = g.Key, Total = g.Sum(t => t.Amount) })
    .OrderByDescending(x => x.Total)
    .ToList();
```

The signed fold gives the running balance; the GroupBy pipeline is the category report. Both are one pass over data — the aggregation lesson's patterns applied to a real domain.

## The statement

A monthly statement composes them: filter the month, compute income/expense/balance, find the biggest category, take the top 3 entries by amount descending. Nothing new — Module 15's `Where`/`Sum`/`GroupBy`/`OrderByDescending` in combination, which is the point: capstones verify that earlier modules became reflexes.
""",
    "Tổng hợp và sao kê",
    "LINQ gập danh sách giao dịch thành số dư, tổng theo danh mục, và sao kê tháng.",
    r"""
## Số dư và tổng

```csharp
decimal balance = ledger.Sum(t => t.Dir == Direction.Income ? t.Amount : -t.Amount);

var byCategory = ledger
    .GroupBy(t => t.Category)
    .Select(g => new { Category = g.Key, Total = g.Sum(t => t.Amount) })
    .OrderByDescending(x => x.Total)
    .ToList();
```

Phép gập có dấu cho số dư luỹ kế; pipeline GroupBy là báo cáo danh mục. Cả hai đều một lượt qua dữ liệu — các mẫu của bài tổng hợp áp dụng vào miền thật.

## Sao kê

Sao kê tháng ghép chúng lại: lọc tháng, tính thu/chi/số dư, tìm danh mục lớn nhất, lấy 3 mục nổi bật theo số tiền giảm dần. Không gì mới — `Where`/`Sum`/`GroupBy`/`OrderByDescending` của Module 15 phối hợp, và đó là ý nghĩa: capstone kiểm chứng các module trước đã thành phản xạ.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p21-capstone",
    "Capstone workshop",
    "The ledger's milestones as graded challenges: validate, aggregate, categorize, filter — plus the File-based CSV persistence from the plan's milestone 5.",
    "Xưởng capstone",
    "Các cột mốc của sổ làm thử thách có chấm điểm: xác thực, tổng hợp, phân loại, lọc — cộng lưu-trữ CSV qua File từ cột mốc 5 của kế hoạch.",
    "csb-m21-report",
    50,
    "beginner",
    [
        challenge(
            "csb-p21-validate",
            "Validate with reasons",
            "Implement `static AddResult Validate(Transaction t)` — reject when Amount <= 0 (\"amount-must-be-positive\"), when Category is null/whitespace (\"category-required\"), or when Description exceeds 100 characters (\"description-too-long\"); otherwise Ok with Error null.",
            CS_CAP,
            [
                (
                    "normal",
                    "var ok = new Transaction(1, Direction.Income, 100m, \"salary\", \"pay\", new DateTime(2026, 5, 1));\nvar r = Solution.Validate(ok);\nCj.True(r.Ok, \"valid passes\");\nCj.Eq(r.Error, null, \"no error on success\");",
                    "All clean — Error stays null.",
                ),
                (
                    "rejections",
                    "var bad = new Transaction(2, Direction.Expense, 0m, \"food\", \"x\", new DateTime(2026, 5, 2));\nvar r1 = Solution.Validate(bad);\nCj.False(r1.Ok, \"zero amount\");\nCj.Eq(r1.Error, \"amount-must-be-positive\", \"reason pinned\");\nvar r2 = Solution.Validate(bad with { Amount = -5m, Category = \" \" });\nCj.False(r2.Ok, \"blank category\");\nCj.Eq(r2.Error, \"amount-must-be-positive\", \"first failure wins\");\nvar r3 = Solution.Validate(bad with { Amount = 5m, Category = \"food\", Description = new string('d', 60) });\nCj.True(r3.Ok, \"60-char description stays valid\");\nvar r4 = Solution.Validate(bad with { Amount = 5m, Description = new string('d', 101) });\nCj.False(r4.Ok, \"101-char description rejected\");\nCj.Eq(r4.Error, \"description-too-long\", \"length reason pinned\");",
                    "Each rejection reason is pinned; rule order matters (amount first); a 60-char description must stay valid while 101 chars must not.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p21-balance",
            "Running balance",
            "Implement `static List<decimal> RunningBalance(List<Transaction> ledger)` — the balance after each transaction in order (income adds, expense subtracts). Empty ledger → empty list.",
            CS_CAP,
            [
                (
                    "normal",
                    "var ledger = new List<Transaction>\n{\n    new(1, Direction.Income, 100m, \"w\", \"a\", new DateTime(2026, 5, 1)),\n    new(2, Direction.Expense, 30m, \"f\", \"b\", new DateTime(2026, 5, 2)),\n    new(3, Direction.Income, 20m, \"g\", \"c\", new DateTime(2026, 5, 3)),\n};\nCj.Eq(string.Join(\",\", Solution.RunningBalance(ledger)), \"100,70,90\", \"accumulates in order\");",
                    "A signed fold — carry the running total through.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.RunningBalance(new List<Transaction>()).Count, 0, \"empty\");\nvar single = new List<Transaction> { new(1, Direction.Expense, 5m, \"f\", \"x\", new DateTime(2026, 5, 1)) };\nCj.Eq(Solution.RunningBalance(single)[0], -5m, \"can go negative\");",
                    "Empty contract and an overdrawn account — both legal.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p21-categories",
            "Category report",
            "Implement `static List<string> TopCategories(List<Transaction> ledger, int n)` — the category names by total (expenses and incomes alike), descending; ties alphabetical; return at most n names.",
            CS_CAP,
            [
                (
                    "normal",
                    "var ledger = new List<Transaction>\n{\n    new(1, Direction.Expense, 50m, \"food\", \"a\", new DateTime(2026, 5, 1)),\n    new(2, Direction.Expense, 80m, \"rent\", \"b\", new DateTime(2026, 5, 2)),\n    new(3, Direction.Expense, 20m, \"food\", \"c\", new DateTime(2026, 5, 3)),\n};\nCj.Eq(string.Join(\",\", Solution.TopCategories(ledger, 2)), \"rent,food\", \"rent 80 > food 70\");",
                    "Totals must accumulate before ranking.",
                ),
                (
                    "ties",
                    "var ledger = new List<Transaction>\n{\n    new(1, Direction.Expense, 60m, \"zoo\", \"a\", new DateTime(2026, 5, 1)),\n    new(2, Direction.Expense, 60m, \"art\", \"b\", new DateTime(2026, 5, 2)),\n};\nCj.Eq(string.Join(\",\", Solution.TopCategories(ledger, 5)), \"art,zoo\", \"tie alphabetical\");\nCj.Eq(Solution.TopCategories(ledger, 1).Count, 1, \"capped at n\");",
                    "The tie rule and the cap — both part of the contract.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p21-csv",
            "CSV persistence",
            "Implement `static string SaveCsv(List<Transaction> ledger, string dir)` — write each transaction as one CSV line `id,dir,amount,category` (dir as \"income\"/\"expense\", amount invariant) into `<dir>/ledger.csv`, creating the directory; return the full path.",
            CS_CAP,
            [
                (
                    "normal",
                    "string dir = Path.Combine(Path.GetTempPath(), \"csb-capstone-\" + Guid.NewGuid().ToString(\"N\"));\nvar ledger = new List<Transaction>\n{\n    new(1, Direction.Income, 100m, \"w\", \"a\", new DateTime(2026, 5, 1)),\n    new(2, Direction.Expense, 30m, \"f\", \"b\", new DateTime(2026, 5, 2)),\n};\nstring p = Solution.SaveCsv(ledger, dir);\nvar lines = File.ReadAllLines(p);\nCj.Eq(lines.Length, 2, \"one line per transaction\");\nCj.Eq(lines[0], \"1,income,100,w\", \"format pinned\");\nCj.Eq(lines[1], \"2,expense,30,f\", \"amounts are plain\");",
                    "Directory creation, line format, and plain decimal output.",
                ),
                (
                    "edges",
                    "string dir = Path.Combine(Path.GetTempPath(), \"csb-capstone-\" + Guid.NewGuid().ToString(\"N\"));\nstring p = Solution.SaveCsv(new List<Transaction>(), dir);\nCj.True(File.Exists(p), \"file exists even when empty\");\nCj.Eq(File.ReadAllLines(p).Length, 0, \"empty ledger, empty file\");\nvar one = new List<Transaction> { new(9, Direction.Expense, 12.5m, \"f\", \"x\", new DateTime(2026, 5, 1)) };\nCj.Eq(File.ReadAllLines(Solution.SaveCsv(one, dir))[0], \"9,expense,12.5,f\", \"fractional amount\");",
                    "Empty file, directory creation, and fractional amounts — invariant culture keeps the dot.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p21-validate": vi_challenge(
            "Xác thực kèm lý do",
            "Hiện thực `static AddResult Validate(Transaction t)` — từ chối khi Amount <= 0 (\"amount-must-be-positive\"), khi Category null/toàn-khoảng-trắng (\"category-required\"), hoặc khi Description vượt 100 ký tự (\"description-too-long\"); nếu hợp lệ thì Ok với Error null.",
            [
                ("normal", "Mọi thứ sạch — Error giữ null."),
                ("rejections", "Mỗi lý do từ chối được ghim; thứ tự luật quan trọng (amount trước); mô tả 60 ký tự vẫn hợp lệ còn 101 ký tự thì không."),
            ],
        ),
        "csb-p21-balance": vi_challenge(
            "Số dư luỹ kế",
            "Hiện thực `static List<decimal> RunningBalance(List<Transaction> ledger)` — số dư sau mỗi giao dịch theo thứ tự (thu cộng, chi trừ). Sổ rỗng → danh sách rỗng.",
            [
                ("normal", "Một phép gập có dấu — mang tổng luỹ kế xuyên suốt."),
                ("edges", "Hợp đồng rỗng và tài khoản âm — đều hợp lệ."),
            ],
        ),
        "csb-p21-categories": vi_challenge(
            "Báo cáo danh mục",
            "Hiện thực `static List<string> TopCategories(List<Transaction> ledger, int n)` — tên danh mục theo tổng (cả chi lẫn thu), giảm dần; hòa thì theo alphabet; trả tối đa n tên.",
            [
                ("normal", "Tổng phải tích lũy trước khi xếp hạng."),
                ("ties", "Luật hòa và giới hạn n — đều thuộc hợp đồng."),
            ],
        ),
        "csb-p21-csv": vi_challenge(
            "Lưu trữ CSV",
            "Hiện thực `static string SaveCsv(List<Transaction> ledger, string dir)` — ghi mỗi giao dịch một dòng CSV `id,dir,amount,category` (dir là \"income\"/\"expense\", amount theo invariant) vào `<dir>/ledger.csv`, tự tạo thư mục; trả đường dẫn đầy đủ.",
            [
                ("normal", "Tạo thư mục, định dạng dòng, và decimal thô."),
                ("edges", "Tệp rỗng, tạo thư mục, và số lẻ — invariant culture giữ dấu chấm."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p21-validate",
            'public class Solution\n{\n    public static AddResult Validate(Transaction t)\n    {\n        if (t.Amount <= 0m) return new AddResult(false, "amount-must-be-positive");\n        if (string.IsNullOrWhiteSpace(t.Category)) return new AddResult(false, "category-required");\n        if (t.Description != null && t.Description.Length > 100)\n            return new AddResult(false, "description-too-long");\n        return new AddResult(true, null);\n    }\n}\n',
            'public class Solution\n{\n    public static AddResult Validate(Transaction t)\n    {\n        if (t.Amount <= 0m) return new AddResult(false, "amount-must-be-positive");\n        // near-miss: checks the description against 10 chars instead of\n        // 100 — perfectly good descriptions get rejected\n        if (t.Description != null && t.Description.Length > 10)\n            return new AddResult(false, "description-too-long");\n        if (string.IsNullOrWhiteSpace(t.Category)) return new AddResult(false, "category-required");\n        return new AddResult(true, null);\n    }\n}\n',
        ),
        (
            "csb-p21-balance",
            'public class Solution\n{\n    public static List<decimal> RunningBalance(List<Transaction> ledger)\n    {\n        var result = new List<decimal>();\n        decimal balance = 0m;\n        foreach (var t in ledger)\n        {\n            balance += t.Dir == Direction.Income ? t.Amount : -t.Amount;\n            result.Add(balance);\n        }\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static List<decimal> RunningBalance(List<Transaction> ledger)\n    {\n        var result = new List<decimal>();\n        // near-miss: never CARRIES the balance — every entry reports the\n        // effect of its own transaction only\n        foreach (var t in ledger)\n        {\n            result.Add(t.Dir == Direction.Income ? t.Amount : -t.Amount);\n        }\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p21-categories",
            'public class Solution\n{\n    public static List<string> TopCategories(List<Transaction> ledger, int n)\n    {\n        return ledger\n            .GroupBy(t => t.Category)\n            .Select(g => new { Category = g.Key, Total = g.Sum(t => t.Amount) })\n            .OrderByDescending(x => x.Total)\n            .ThenBy(x => x.Category, StringComparer.Ordinal)\n            .Select(x => x.Category)\n            .Take(n)\n            .ToList();\n    }\n}\n',
            'public class Solution\n{\n    public static List<string> TopCategories(List<Transaction> ledger, int n)\n    {\n        // near-miss: ranks by COUNT of transactions instead of the SUM\n        // of amounts\n        return ledger\n            .GroupBy(t => t.Category)\n            .Select(g => new { Category = g.Key, Count = g.Count() })\n            .OrderByDescending(x => x.Count)\n            .ThenBy(x => x.Category, StringComparer.Ordinal)\n            .Select(x => x.Category)\n            .Take(n)\n            .ToList();\n    }\n}\n',
        ),
        (
            "csb-p21-csv",
            'public class Solution\n{\n    public static string SaveCsv(List<Transaction> ledger, string dir)\n    {\n        Directory.CreateDirectory(dir);\n        string path = Path.Combine(dir, "ledger.csv");\n        var lines = new List<string>();\n        foreach (var t in ledger)\n        {\n            lines.Add($"{t.Id},{(t.Dir == Direction.Income ? "income" : "expense")},{t.Amount.ToString(System.Globalization.CultureInfo.InvariantCulture)},{t.Category}");\n        }\n        File.WriteAllLines(path, lines);\n        return path;\n    }\n}\n',
            'public class Solution\n{\n    public static string SaveCsv(List<Transaction> ledger, string dir)\n    {\n        // near-miss: forgets to create the directory — throws\n        // DirectoryNotFoundException on a fresh dir\n        string path = Path.Combine(dir, "ledger.csv");\n        var lines = new List<string>();\n        foreach (var t in ledger)\n        {\n            lines.Add($"{t.Id},{(t.Dir == Direction.Income ? "income" : "expense")},{t.Amount.ToString(System.Globalization.CultureInfo.InvariantCulture)},{t.Category}");\n        }\n        File.WriteAllLines(path, lines);\n        return path;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m21",
    "Checkpoint — Monthly statement",
    "The capstone deliverable: a monthly statement with signed totals, the dominant category, and the top entries.",
    25,
    r"""
## Checkpoint: the monthly statement

**Task:** implement in `Solution`:

1. `static Statement MonthStatement(List<Transaction> ledger, int year, int month)` — statement for the transactions in that calendar month; `Income`/`Expense` are signed totals (income positive, expenses as their amounts), `Balance = Income − Expense`, and `Top` holds at most 3 descriptions of that month's transactions ordered by amount descending (ties in stable ledger order). A month with no transactions yields zeroed totals and an empty `Top`.
2. Supporting type `public record Statement(decimal Income, decimal Expense, decimal Balance, List<string> Top);` may be declared inside `Solution` or alongside it.
""",
    "Checkpoint — Sao kê tháng",
    "Sản phẩm cuối của capstone: sao kê tháng với tổng có dấu, danh mục trội, và các mục nổi bật.",
    r"""
## Checkpoint: sao kê tháng

**Nhiệm vụ:** hiện thực trong `Solution`:

1. `static Statement MonthStatement(List<Transaction> ledger, int year, int month)` — sao kê cho các giao dịch trong tháng dương lịch đó; `Income`/`Expense` là tổng có dấu (thu dương, chi tính theo số tiền của chúng), `Balance = Income − Expense`, và `Top` chứa tối đa 3 mô tả của giao dịch tháng đó xếp theo số tiền giảm dần (hòa giữ thứ tự sổ ổn định). Tháng không có giao dịch cho tổng bằng 0 và `Top` rỗng.
2. Kiểu hỗ trợ `public record Statement(decimal Income, decimal Expense, decimal Balance, List<string> Top);` có thể khai báo trong `Solution` hoặc cạnh nó.
""",
    challenge(
        "csb-checkpoint-m21-task",
        "MonthlyStatement",
        "Implement `MonthStatement` — filter the month, sign the totals, rank the entries.",
        CS_CAP,
        [
            (
                "totals",
                "var ledger = new List<Transaction>\n{\n    new(1, Direction.Income, 300m, \"w\", \"salary\", new DateTime(2026, 5, 1)),\n    new(2, Direction.Expense, 100m, \"food\", \"groceries\", new DateTime(2026, 5, 3)),\n    new(3, Direction.Expense, 50m, \"fun\", \"cinema\", new DateTime(2026, 5, 10)),\n    new(4, Direction.Income, 999m, \"w\", \"other month\", new DateTime(2026, 4, 30)),\n    new(5, Direction.Income, 500m, \"w\", \"May of last year\", new DateTime(2025, 5, 20)),\n};\nvar s = Solution.MonthStatement(ledger, 2026, 5);\nCj.Eq(s.Income, 300m, \"only May 2026 income — May 2025 excluded\");\nCj.Eq(s.Expense, 150m, \"only May expenses\");\nCj.Eq(s.Balance, 150m, \"signed difference\");",
                "The April transaction must be excluded — so must May of *last year*: filter by both month and year.",
            ),
            (
                "top-and-empty",
                "var ledger = new List<Transaction>\n{\n    new(1, Direction.Expense, 10m, \"a\", \"small\", new DateTime(2026, 5, 1)),\n    new(2, Direction.Expense, 90m, \"b\", \"big\", new DateTime(2026, 5, 2)),\n    new(3, Direction.Expense, 40m, \"c\", \"mid\", new DateTime(2026, 5, 3)),\n    new(4, Direction.Expense, 20m, \"d\", \"tiny\", new DateTime(2026, 5, 4)),\n    new(5, Direction.Expense, 30m, \"e\", \"small2\", new DateTime(2026, 5, 5)),\n};\nvar s = Solution.MonthStatement(ledger, 2026, 5);\nCj.Eq(string.Join(\",\", s.Top), \"big,mid,small2\", \"top 3 by amount desc\");\nvar empty = Solution.MonthStatement(ledger, 2026, 12);\nCj.Eq(empty.Income, 0m, \"no income\");\nCj.Eq(empty.Top.Count, 0, \"no entries\");",
                "Top 3 selection, the empty-month contract, zeroed totals.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "MonthlyStatement",
        "Hiện thực `MonthStatement` — lọc tháng, gắn dấu cho tổng, xếp hạng các mục.",
        [
            ("totals", "Giao dịch tháng Tư phải bị loại — tháng Năm *năm ngoái* cũng vậy: lọc cả tháng lẫn năm."),
            ("top-and-empty", "Chọn Top 3, hợp đồng tháng-rỗng, tổng bằng 0."),
        ],
    ),
    solution='public class Solution\n{\n    public record Statement(decimal Income, decimal Expense, decimal Balance, List<string> Top);\n    public static Statement MonthStatement(List<Transaction> ledger, int year, int month)\n    {\n        var inMonth = ledger\n            .Where(t => t.Date.Year == year && t.Date.Month == month)\n            .ToList();\n        decimal income = inMonth.Where(t => t.Dir == Direction.Income).Sum(t => t.Amount);\n        decimal expense = inMonth.Where(t => t.Dir == Direction.Expense).Sum(t => t.Amount);\n        var top = inMonth\n            .OrderByDescending(t => t.Amount)\n            .Select(t => t.Description)\n            .Take(3)\n            .ToList();\n        return new Statement(income, expense, income - expense, top);\n    }\n}\n',
    wrong='public class Solution\n{\n    public record Statement(decimal Income, decimal Expense, decimal Balance, List<string> Top);\n    public static Statement MonthStatement(List<Transaction> ledger, int year, int month)\n    {\n        // near-miss: checks only the MONTH — April (month 4) leaks into\n        // a May (month 5) statement of a different year\n        var inMonth = ledger\n            .Where(t => t.Date.Month == month)\n            .ToList();\n        decimal income = inMonth.Where(t => t.Dir == Direction.Income).Sum(t => t.Amount);\n        decimal expense = inMonth.Where(t => t.Dir == Direction.Expense).Sum(t => t.Amount);\n        var top = inMonth\n            .OrderByDescending(t => t.Amount)\n            .Select(t => t.Description)\n            .Take(3)\n            .ToList();\n        return new Statement(income, expense, income - expense, top);\n    }\n}\n',
)
print("module 21 authored")
