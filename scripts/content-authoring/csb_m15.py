#!/usr/bin/env python3
"""C# — Beginner — Module 15: csb-linq.

LINQ as query methods over IEnumerable<T>: Where/Select/OrderBy/GroupBy/
aggregates — what actually runs, deferred execution, and choosing method
syntax. House conventions: Ws are behavioral near-misses, tests discriminate.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-linq"

write_module(
    M,
    "LINQ Fundamentals",
    "Queries as method calls: filter, project, order, group, aggregate — and the deferred-execution rule that surprises everyone once.",
    "LINQ Cơ bản",
    "Truy vấn như lời gọi phương thức: lọc, chiếu, sắp, nhóm, tổng hợp — và luật thực-thi-hoãn khiến ai cũng ngạc nhiên một lần.",
    ["csb-m15-where-select", "csb-m15-order-group", "csb-m15-aggregates", "csb-checkpoint-m15"],
    ["csb-p15-linq"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m15-where-select",
    "Where and Select",
    "Two methods cover most data work: keep some elements, transform the rest.",
    13,
    r"""
## Filter with Where

```csharp
var nums = new List<int> { 1, 2, 3, 4, 5, 6 };
var evens = nums.Where(n => n % 2 == 0);   // 2, 4, 6
```

`Where` takes a **predicate** — a function from element to bool — and yields elements where it returns true. The source is unchanged; the result is a *query* over it.

## Project with Select

```csharp
var names = new[] { "an", "binh" };
var upper = names.Select(s => s.ToUpperInvariant());   // "AN", "BINH"
var lengths = names.Select(s => s.Length);             // 2, 4
```

`Select` transforms each element into something else — same count in, same count out, new shape out. Together they compose:

```csharp
var longUpper = names.Where(s => s.Length > 2).Select(s => s.ToUpperInvariant());
```

Read the chain left to right: filter first, then transform. Chaining is the everyday LINQ style; each stage's output is the next stage's input.

## What LINQ actually is

No magic: `Where`/`Select` are ordinary extension methods on `IEnumerable<T>` from `System.Linq`. The lambda you pass is a delegate that runs per element. Deferred execution is the one surprise — covered two lessons ahead.
""",
    "Where và Select",
    "Hai phương thức phủ phần lớn công việc dữ liệu: giữ lại một số phần tử, biến đổi phần còn lại.",
    r"""
## Lọc với Where

```csharp
var nums = new List<int> { 1, 2, 3, 4, 5, 6 };
var evens = nums.Where(n => n % 2 == 0);   // 2, 4, 6
```

`Where` nhận một **predicate** — hàm từ phần tử sang bool — và trả các phần tử mà nó trả true. Nguồn không đổi; kết quả là một *truy vấn* trên nguồn đó.

## Chiếu với Select

```csharp
var names = new[] { "an", "binh" };
var upper = names.Select(s => s.ToUpperInvariant());   // "AN", "BINH"
var lengths = names.Select(s => s.Length);             // 2, 4
```

`Select` biến đổi từng phần tử thành thứ khác — vào bao nhiêu ra bấy nhiêu, nhưng hình dạng mới. Kết hợp lại:

```csharp
var longUpper = names.Where(s => s.Length > 2).Select(s => s.ToUpperInvariant());
```

Đọc chuỗi từ trái sang phải: lọc trước, biến đổi sau. Chuỗi hóa là phong cách LINQ hằng ngày; đầu ra của mỗi mắt xích là đầu vào của mắt xích kế.

## LINQ thật ra là gì

Không phép màu: `Where`/`Select` là các extension method bình thường trên `IEnumerable<T>` từ `System.Linq`. Lambda bạn truyền là một delegate chạy trên từng phần tử. Thực-thi-hoãn là bất ngờ duy nhất — ở bài thứ ba.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m15-order-group",
    "OrderBy, ThenBy, GroupBy",
    "Ordering chains and grouping — plus the sort-stability fact that makes ThenBy choices safe.",
    13,
    r"""
## Ordering

```csharp
var words = new[] { "pear", "fig", "apple" };
var sorted = words.OrderBy(w => w.Length).ThenBy(w => w);
// fig(3), apple(5), pear(4)? no: fig, apple, pear sorted by length: fig, pear, apple
```

`OrderBy(key)` sorts ascending by the key; `OrderByDescending` flips it. `ThenBy` breaks ties: first by `Length`, equals sorted alphabetically. **Replace, don't re-order**: calling `OrderBy` twice replaces the first ordering — the second call's keys become primary. Chains read: primary, then tie-breakers.

## Grouping

```csharp
var byLength = words.GroupBy(w => w.Length);
foreach (var g in byLength)
{
    Console.WriteLine($"length {g.Key}: {string.Join(",", g)}");
}
// length 3: pear,fig — no: 3: fig  5: apple,pear
```

`GroupBy(key)` yields a sequence of groups, each with a `Key` and the elements sharing it — a `Dictionary` in fluent form. Group order is encounter order; element order within a group is source order.
""",
    "OrderBy, ThenBy, GroupBy",
    "Chuỗi sắp xếp và nhóm — cộng sự thật về độ ổn định của sắp-xếp làm lựa chọn ThenBy an toàn.",
    r"""
## Sắp xếp

```csharp
var words = new[] { "pear", "fig", "apple" };
var sorted = words.OrderBy(w => w.Length).ThenBy(w => w);
// sắp theo độ dài: fig(3), pear(4), apple(5)
```

`OrderBy(key)` sắp tăng dần theo khóa; `OrderByDescending` đảo chiều. `ThenBy` phá hòa: trước theo `Length`, bằng nhau sắp theo alphabet. **Thay thế, không xếp-lại**: gọi `OrderBy` hai lần là thay thế thứ tự đầu — khóa của lần gọi sau thành chính. Chuỗi đọc: chính, rồi các phá-hòa.

## Nhóm

```csharp
var byLength = words.GroupBy(w => w.Length);
foreach (var g in byLength)
{
    Console.WriteLine($"độ dài {g.Key}: {string.Join(",", g)}");
}
// 3: fig  5: apple,pear
```

`GroupBy(key)` trả một chuỗi các nhóm, mỗi nhóm có `Key` và các phần tử dùng chung nó — một `Dictionary` dạng fluent. Thứ tự nhóm là thứ tự gặp; thứ tự phần tử trong nhóm là thứ tự nguồn.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m15-aggregates",
    "Aggregates and deferred execution",
    "Count/Sum/Min/Max/Average/Any/All collapse sequences to answers — and queries run when you look, not when you write.",
    14,
    r"""
## The collapse methods

```csharp
var nums = new[] { 3, 1, 4, 1, 5 };
nums.Count();          // 5
nums.Sum();            // 14
nums.Min(); nums.Max(); // 1, 5
nums.Average();        // 2.8
nums.Any(n => n > 4);  // true  — "at least one"
nums.All(n => n > 0);  // true  — "every one"
```

`Any`/`All` are predicates over the whole set; `Count()` with a predicate counts matches. On empty sequences `Min`/`Max`/`Average` throw `InvalidOperationException` — guard or use `FirstOrDefault`-style handling.

## Deferred execution

```csharp
var query = nums.Where(n => n > 2);   // NOTHING runs yet
nums.Add(10);
foreach (var n in query) ...          // NOW it runs — and sees the 10!
```

A query is a *recipe*, not a result. It executes when enumerated — `foreach`, `ToList()`, an aggregate like `Sum()`. Each enumeration re-runs it. Pin a snapshot when the source might change: `var pinned = query.ToList();`.

First-or-default family:

```csharp
nums.FirstOrDefault(n => n > 100);    // 0 (int default) — no throw
nums.First(n => n > 100);             // throws InvalidOperationException
```

`...OrDefault` returns the type's default instead of throwing — the polite variant for "might not exist".
""",
    "Tổng hợp và thực-thi-hoãn",
    "Count/Sum/Min/Max/Average/Any/All gộp chuỗi thành câu trả lời — và truy vấn chạy khi bạn nhìn, không phải khi bạn viết.",
    r"""
## Các phương thức gộp

```csharp
var nums = new[] { 3, 1, 4, 1, 5 };
nums.Count();          // 5
nums.Sum();            // 14
nums.Min(); nums.Max(); // 1, 5
nums.Average();        // 2.8
nums.Any(n => n > 4);  // true  — "tồn tại ít nhất một"
nums.All(n => n > 0);  // true  — "tất cả đều"
```

`Any`/`All` là predicate trên toàn tập; `Count(predicate)` đếm phần khớp. Với chuỗi rỗng, `Min`/`Max`/`Average` ném `InvalidOperationException` — hãy chặn hoặc xử lý kiểu FirstOrDefault.

## Thực-thi-hoãn

```csharp
var query = nums.Where(n => n > 2);   // CHƯA có gì chạy
nums.Add(10);
foreach (var n in query) ...          // GIỜ mới chạy — và thấy cả số 10!
```

Truy vấn là một *công thức*, không phải kết quả. Nó thực thi khi được liệt kê — `foreach`, `ToList()`, một phép gộp như `Sum()`. Mỗi lần liệt kê chạy lại từ đầu. Ghim ảnh chụp khi nguồn có thể đổi: `var pinned = query.ToList();`.

Họ first-or-default:

```csharp
nums.FirstOrDefault(n => n > 100);    // 0 (default của int) — không ném
nums.First(n => n > 100);             // ném InvalidOperationException
```

`...OrDefault` trả giá trị default của kiểu thay vì ném — biến phiên bản lịch sự cho "có thể không tồn tại".
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p15-linq",
    "LINQ workout",
    "Filters, projections, orderings, groupings, aggregates — pipelines under discriminating tests.",
    "Luyện tập LINQ",
    "Lọc, chiếu, sắp, nhóm, tổng hợp — các đường ống dưới các bài kiểm tra phân biệt.",
    "csb-m15-aggregates",
    40,
    "beginner",
    [
        challenge(
            "csb-p15-filter-shape",
            "Filter and shape",
            "Implement `static List<string> LongUpper(IEnumerable<string> words)` — words of length ≥ 3, uppercased, original order; and `static List<int> Lengths(IEnumerable<string> words)` — just the lengths, same order. Null input → empty lists.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var w = new[] { \"hi\", \"pear\", \"fig\", \"apple\" };\nCj.Eq(string.Join(\",\", Solution.LongUpper(w)), \"PEAR,FIG,APPLE\", \"len>=3 uppercase\");\nCj.Eq(string.Join(\",\", Solution.Lengths(w)), \"2,4,3,5\", \"lengths in order\");",
                    "Where then Select vs Select alone — same source, two shapes.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.LongUpper(null).Count, 0, \"null long\");\nCj.Eq(Solution.Lengths(new string[0]).Count, 0, \"empty lengths\");\nCj.Eq(string.Join(\",\", Solution.LongUpper(new[] { \"ab\", \"cd\" })), \"\", \"nothing survives the filter\");",
                    "Empty results are empty lists, never null or exceptions.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p15-ranking",
            "Ranking with tie-breakers",
            "Implement `static List<string> Rank(List<(string Name, int Score)> rows)` — names ordered by score descending, ties broken by name ascending; and `static (string Name, int Score)? Top(List<(string Name, int Score)> rows)` — the first-ranked row or null for an empty/null list.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var rows = new List<(string, int)> { (\"an\", 80), (\"binh\", 90), (\"chi\", 80) };\nCj.Eq(string.Join(\",\", Solution.Rank(rows)), \"binh,an,chi\", \"score desc, name asc\");\nvar top = Solution.Top(rows);\nCj.Eq(top.Value.Item1, \"binh\", \"highest score\");",
                    "OrderByDescending(score).ThenBy(name) is the whole ranking algorithm.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.Rank(null).Count, 0, \"null rank\");\nCj.False(Solution.Top(null).HasValue, \"null top\");\nCj.False(Solution.Top(new List<(string, int)>()).HasValue, \"empty top\");\nvar one = new List<(string, int)> { (\"solo\", 1) };\nCj.True(Solution.Top(one).HasValue, \"single has a top\");",
                    "Nullable return type makes \"no row\" explicit instead of a crash.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p15-groupcount",
            "Group and count",
            "Implement `static Dictionary<string, int> CountByFirstLetter(IEnumerable<string> words)` — group words by `char.ToLowerInvariant(word[0])` as key; and `static Dictionary<int, int> CountByLength(IEnumerable<string> words)` — group by length. Null/empty input → empty dictionaries.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var w = new[] { \"An\", \"apple\", \"binh\", \"bear\", \"cat\" };\nvar byLetter = Solution.CountByFirstLetter(w);\nCj.Eq(byLetter[\"a\"], 2, \"An + apple\");\nCj.Eq(byLetter[\"b\"], 2, \"binh + bear\");\nvar byLen = Solution.CountByLength(w);\nCj.Eq(byLen[2], 1, \"only An is 2 letters\");\nCj.Eq(byLen[4], 2, \"two 4-letter words\");",
                    "GroupBy the normalized key, then ToDictionary(g => g.Key, g => g.Count()).",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.CountByFirstLetter(null).Count, 0, \"null\");\nCj.Eq(Solution.CountByLength(new string[0]).Count, 0, \"empty\");",
                    "Both null and empty normalize to empty dictionaries.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p15-aggregates",
            "Aggregate dashboard",
            "Implement `static (int Count, int Total, double Average) Stats(IEnumerable<int> nums)` (empty/null → (0, 0, 0.0)), `static bool AllPositive(IEnumerable<int> nums)` (empty → true — vacuous truth), and `static int FirstBig(IEnumerable<int> nums, int threshold)` — first element > threshold or -1 when none.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var nums = new[] { 3, -1, 7, 2 };\nvar s = Solution.Stats(nums);\nCj.Eq(s.Count, 4, \"count\");\nCj.Eq(s.Total, 11, \"sum\");\nCj.Near(s.Average, 2.75, 1e-9, \"mean\");\nCj.False(Solution.AllPositive(nums), \"has a negative\");\nCj.Eq(Solution.FirstBig(nums, 5), 7, \"first over 5\");",
                    "The three collapse families: whole-set stats, a universal predicate, a first-match.",
                ),
                (
                    "edges",
                    "var e = Solution.Stats(new int[0]);\nCj.Eq(e.Count, 0, \"empty count\");\nCj.Eq(e.Total, 0, \"empty total\");\nCj.Eq(e.Average, 0.0, \"empty average — no throw\");\nCj.True(Solution.AllPositive(new int[0]), \"vacuous truth\");\nCj.Eq(Solution.FirstBig(new[] { 1, 2 }, 100), -1, \"nothing over 100\");",
                    "Empty contracts are explicit: zeroed stats, vacuous true, -1 sentinel.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p15-filter-shape": vi_challenge(
            "Lọc và định hình",
            "Hiện thực `static List<string> LongUpper(IEnumerable<string> words)` — từ có độ dài ≥ 3, viết hoa, giữ thứ tự gốc; và `static List<int> Lengths(IEnumerable<string> words)` — chỉ các độ dài, cùng thứ tự. Input null → danh sách rỗng.",
            [
                ("normal", "Where rồi Select so với Select một mình — cùng nguồn, hai hình dạng."),
                ("edges", "Kết quả rỗng là danh sách rỗng, không bao giờ null hay ngoại lệ."),
            ],
        ),
        "csb-p15-ranking": vi_challenge(
            "Xếp hạng với phá-hòa",
            "Hiện thực `static List<string> Rank(List<(string Name, int Score)> rows)` — tên sắp theo điểm giảm dần, hòa thì theo tên tăng dần; và `static (string Name, int Score)? Top(List<(string Name, int Score)> rows)` — hàng xếp đầu hoặc null cho danh sách rỗng/null.",
            [
                ("normal", "OrderByDescending(điểm).ThenBy(tên) là toàn bộ thuật toán xếp hạng."),
                ("edges", "Kiểu trả về nullable làm \"không có hàng\" trở nên tường minh thay vì sập."),
            ],
        ),
        "csb-p15-groupcount": vi_challenge(
            "Nhóm và đếm",
            "Hiện thực `static Dictionary<string, int> CountByFirstLetter(IEnumerable<string> words)` — nhóm từ theo `char.ToLowerInvariant(word[0])` làm khóa; và `static Dictionary<int, int> CountByLength(IEnumerable<string> words)` — nhóm theo độ dài. Null/rỗng → dictionary rỗng.",
            [
                ("normal", "GroupBy theo khóa đã chuẩn hóa, rồi ToDictionary(g => g.Key, g => g.Count())."),
                ("edges", "Cả null và rỗng chuẩn hóa thành dictionary rỗng."),
            ],
        ),
        "csb-p15-aggregates": vi_challenge(
            "Bảng điều khiển tổng hợp",
            "Hiện thực `static (int Count, int Total, double Average) Stats(IEnumerable<int> nums)` (rỗng/null → (0, 0, 0.0)), `static bool AllPositive(IEnumerable<int> nums)` (rỗng → true — chân lý ngụy_biện), và `static int FirstBig(IEnumerable<int> nums, int threshold)` — phần tử đầu > threshold hoặc -1 khi không có.",
            [
                ("normal", "Ba họ gộp: thống kê toàn tập, predicate phổ quát, tìm-khớp-đầu."),
                ("edges", "Hợp đồng rỗng là tường minh: thống kê bằng không, true ngụy_biện, giá trị canh -1."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p15-filter-shape",
            'public class Solution\n{\n    public static List<string> LongUpper(IEnumerable<string> words)\n    {\n        if (words == null) return new List<string>();\n        return words.Where(w => w.Length >= 3).Select(w => w.ToUpperInvariant()).ToList();\n    }\n    public static List<int> Lengths(IEnumerable<string> words)\n    {\n        if (words == null) return new List<int>();\n        return words.Select(w => w.Length).ToList();\n    }\n}\n',
            'public class Solution\n{\n    public static List<string> LongUpper(IEnumerable<string> words)\n    {\n        if (words == null) return new List<string>();\n        // near-miss: filters on the UPPERCASED length — same length, but the\n        // Select runs BEFORE Where, breaking the documented order\n        // near-miss: strict > excludes exactly-3-letter words like "fig"\n        return words.Where(w => w.Length > 3).Select(w => w.ToUpperInvariant()).ToList();\n    }\n    public static List<int> Lengths(IEnumerable<string> words)\n    {\n        if (words == null) return new List<int>();\n        return words.Select(w => w.Length).ToList();\n    }\n}\n',
        ),
        (
            "csb-p15-ranking",
            'public class Solution\n{\n    public static List<string> Rank(List<(string Name, int Score)> rows)\n    {\n        if (rows == null) return new List<string>();\n        return rows.OrderByDescending(r => r.Score).ThenBy(r => r.Name).Select(r => r.Name).ToList();\n    }\n    public static (string Name, int Score)? Top(List<(string Name, int Score)> rows)\n    {\n        if (rows == null || rows.Count == 0) return null;\n        return rows.OrderByDescending(r => r.Score).ThenBy(r => r.Name).First();\n    }\n}\n',
            'public class Solution\n{\n    public static List<string> Rank(List<(string Name, int Score)> rows)\n    {\n        if (rows == null) return new List<string>();\n        // near-miss: ThenBy FIRST — names become the primary key and scores\n        // only break alphabetical ties, inverting the ranking\n        return rows.ThenBy(r => r.Name).OrderByDescending(r => r.Score).Select(r => r.Name).ToList();\n    }\n    public static (string Name, int Score)? Top(List<(string Name, int Score)> rows)\n    {\n        if (rows == null || rows.Count == 0) return null;\n        return rows.OrderByDescending(r => r.Score).ThenBy(r => r.Name).First();\n    }\n}\n',
        ),
        (
            "csb-p15-groupcount",
            'public class Solution\n{\n    public static Dictionary<string, int> CountByFirstLetter(IEnumerable<string> words)\n    {\n        if (words == null) return new Dictionary<string, int>();\n        return words.GroupBy(w => char.ToLowerInvariant(w[0]).ToString())\n                    .ToDictionary(g => g.Key, g => g.Count());\n    }\n    public static Dictionary<int, int> CountByLength(IEnumerable<string> words)\n    {\n        if (words == null) return new Dictionary<int, int>();\n        return words.GroupBy(w => w.Length).ToDictionary(g => g.Key, g => g.Count());\n    }\n}\n',
            'public class Solution\n{\n    public static Dictionary<string, int> CountByFirstLetter(IEnumerable<string> words)\n    {\n        if (words == null) return new Dictionary<string, int>();\n        // near-miss: keys keep ORIGINAL casing — "An" and "apple" split into\n        // "A" and "a" groups instead of merging under "a"\n        return words.GroupBy(w => w[0].ToString())\n                    .ToDictionary(g => g.Key, g => g.Count());\n    }\n    public static Dictionary<int, int> CountByLength(IEnumerable<string> words)\n    {\n        if (words == null) return new Dictionary<int, int>();\n        return words.GroupBy(w => w.Length).ToDictionary(g => g.Key, g => g.Count());\n    }\n}\n',
        ),
        (
            "csb-p15-aggregates",
            'public class Solution\n{\n    public static (int Count, int Total, double Average) Stats(IEnumerable<int> nums)\n    {\n        if (nums == null) return (0, 0, 0.0);\n        var list = nums.ToList();\n        if (list.Count == 0) return (0, 0, 0.0);\n        return (list.Count, list.Sum(), list.Average());\n    }\n    public static bool AllPositive(IEnumerable<int> nums)\n    {\n        if (nums == null) return true;\n        return nums.All(n => n > 0);\n    }\n    public static int FirstBig(IEnumerable<int> nums, int threshold)\n    {\n        if (nums == null) return -1;\n        foreach (int n in nums)\n        {\n            if (n > threshold) return n;\n        }\n        return -1;\n    }\n}\n',
            'public class Solution\n{\n    public static (int Count, int Total, double Average) Stats(IEnumerable<int> nums)\n    {\n        if (nums == null) return (0, 0, 0.0);\n        var list = nums.ToList();\n        // near-miss: empty check missing — Average() on zero rows throws\n        // InvalidOperationException instead of returning (0, 0, 0.0)\n        return (list.Count, list.Sum(), list.Average());\n    }\n    public static bool AllPositive(IEnumerable<int> nums)\n    {\n        if (nums == null) return true;\n        return nums.All(n => n > 0);\n    }\n    public static int FirstBig(IEnumerable<int> nums, int threshold)\n    {\n        if (nums == null) return -1;\n        foreach (int n in nums)\n        {\n            if (n > threshold) return n;\n        }\n        return -1;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m15",
    "Checkpoint — LINQ",
    "A sales report: filter, project, order, group, and aggregate in one pipeline over transaction rows.",
    20,
    r"""
## Checkpoint: the sales report

**Task:** given `record Sale(string Region, string Product, int Amount)` and a `List<Sale>`, implement in `Solution`:

1. `static List<string> BigSales(List<Sale> sales, int min)` — `"Product:Amount"` for sales with `Amount >= min`, ordered by amount descending then product ascending.
2. `static Dictionary<string, int> TotalByRegion(List<Sale> sales)` — sum of amounts per region.
3. `static (string Product, int Total)? TopProduct(List<Sale> sales)` — product with the highest total amount; null when sales is null/empty. Ties: any.
4. `static double AverageSale(List<Sale> sales, string region)` — mean amount for that region; 0.0 when no sales for it. Case-insensitive region match.
""",
    "Checkpoint — LINQ",
    "Báo cáo bán hàng: lọc, chiếu, sắp, nhóm, và tổng hợp trong một đường ống trên các dòng giao dịch.",
    r"""
## Checkpoint: báo cáo bán hàng

**Nhiệm vụ:** cho `record Sale(string Region, string Product, int Amount)` và một `List<Sale>`, hiện thực trong `Solution`:

1. `static List<string> BigSales(List<Sale> sales, int min)` — `"Product:Amount"` cho các bán hàng với `Amount >= min`, sắp theo số lượng giảm dần rồi sản phẩm tăng dần.
2. `static Dictionary<string, int> TotalByRegion(List<Sale> sales)` — tổng số lượng theo vùng.
3. `static (string Product, int Total)? TopProduct(List<Sale> sales)` — sản phẩm có tổng số lượng cao nhất; null khi sales null/rỗng. Hòa: bên nào cũng được.
4. `static double AverageSale(List<Sale> sales, string region)` — số lượng trung bình của vùng đó; 0.0 khi không có bán hàng nào. Khớp vùng không phân biệt chữ hoa/thường.
""",
    challenge(
        "csb-checkpoint-m15-task",
        "SalesReport",
        "Implement `BigSales`, `TotalByRegion`, `TopProduct`, and `AverageSale` over the Sale record — every contract (ordering, ties, empty, case) is graded.",
        CS_PRELUDE,
        [
            (
                "big-sales",
                "var sales = new List<Solution.Sale>\n{\n    new Solution.Sale(\"north\", \"tea\", 50),\n    new Solution.Sale(\"south\", \"tea\", 80),\n    new Solution.Sale(\"north\", \"mug\", 30),\n    new Solution.Sale(\"south\", \"mug\", 50),\n};\nCj.Eq(string.Join(\"|\", Solution.BigSales(sales, 50)), \"tea:80|mug:50|tea:50\", \"desc amount, asc product\");\nCj.Eq(Solution.BigSales(sales, 100).Count, 0, \"nothing that big\");",
                "Projection, filter, and the two-level ordering: ties on amount break by product A→Z.",
            ),
            (
                "region-and-top",
                "var sales = new List<Solution.Sale>\n{\n    new Solution.Sale(\"North\", \"tea\", 50),\n    new Solution.Sale(\"north\", \"mug\", 30),\n    new Solution.Sale(\"South\", \"tea\", 80),\n};\nvar byRegion = Solution.TotalByRegion(sales);\nCj.Eq(byRegion[\"North\"], 80, \"north merged case-insensitively\");\nCj.Eq(byRegion[\"South\"], 80, \"south\");\nvar top = Solution.TopProduct(sales);\nCj.Eq(top.Value.Item1, \"tea\", \"tea totals 130\");\nCj.Eq(Solution.AverageSale(sales, \"north\"), 40.0, \"north mean\");\nCj.Eq(Solution.AverageSale(sales, \"west\"), 0.0, \"no west sales\");\nCj.Eq(Solution.TopProduct(null), null, \"null sales\");",
                "Region grouping preserves the key as first written; the top product and guarded averages follow.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "SalesReport",
        "Hiện thực `BigSales`, `TotalByRegion`, `TopProduct`, và `AverageSale` trên record Sale — mọi hợp đồng (thứ tự, hòa, rỗng, chữ hoa/thường) đều được chấm.",
        [
            ("big-sales", "Chiếu, lọc, và thứ tự hai cấp: hòa về số lượng thì xếp theo sản phẩm A→Z."),
            ("region-and-top", "Nhóm vùng gộp không phân biệt chữ hoa/thường; sản phẩm trội và trung bình có bảo vệ theo sau."),
        ],
    ),
    solution='public class Solution\n{\n    public sealed record Sale(string Region, string Product, int Amount);\n    public static List<string> BigSales(List<Sale> sales, int min)\n    {\n        if (sales == null) return new List<string>();\n        return sales.Where(s => s.Amount >= min)\n                    .OrderByDescending(s => s.Amount).ThenBy(s => s.Product)\n                    .Select(s => $"{s.Product}:{s.Amount}")\n                    .ToList();\n    }\n    public static Dictionary<string, int> TotalByRegion(List<Sale> sales)\n    {\n        var result = new Dictionary<string, int>();\n        if (sales == null) return result;\n        foreach (Sale s in sales)\n        {\n            // merge case-insensitively, keep the first-seen casing as the key\n            string key = result.Keys.FirstOrDefault(k => string.Equals(k, s.Region, StringComparison.OrdinalIgnoreCase)) ?? s.Region;\n            result[key] = result.GetValueOrDefault(key) + s.Amount;\n        }\n        return result;\n    }\n    public static (string Product, int Total)? TopProduct(List<Sale> sales)\n    {\n        if (sales == null || sales.Count == 0) return null;\n        return sales.GroupBy(s => s.Product)\n                    .Select(g => (Product: g.Key, Total: g.Sum(x => x.Amount)))\n                    .OrderByDescending(x => x.Total)\n                    .Select(x => ((string Product, int Total)?)x)\n                    .First();\n    }\n    public static double AverageSale(List<Sale> sales, string region)\n    {\n        if (sales == null) return 0.0;\n        var match = sales.Where(s => string.Equals(s.Region, region, StringComparison.OrdinalIgnoreCase)).ToList();\n        if (match.Count == 0) return 0.0;\n        return match.Average(s => (double)s.Amount);\n    }\n}\n',
    wrong='public class Solution\n{\n    public sealed record Sale(string Region, string Product, int Amount);\n    public static List<string> BigSales(List<Sale> sales, int min)\n    {\n        if (sales == null) return new List<string>();\n        // near-miss: strict > instead of >= — a sale exactly at min is\n        // silently excluded from "big"\n        return sales.Where(s => s.Amount > min)\n                    .OrderByDescending(s => s.Amount).ThenBy(s => s.Product)\n                    .Select(s => $"{s.Product}:{s.Amount}")\n                    .ToList();\n    }\n    public static Dictionary<string, int> TotalByRegion(List<Sale> sales)\n    {\n        var result = new Dictionary<string, int>();\n        if (sales == null) return result;\n        foreach (Sale s in sales)\n        {\n            // near-miss: case-sensitive region keys — "North" and "north"\n            // become separate regions\n            result[s.Region] = result.GetValueOrDefault(s.Region) + s.Amount;\n        }\n        return result;\n    }\n    public static (string Product, int Total)? TopProduct(List<Sale> sales)\n    {\n        if (sales == null || sales.Count == 0) return null;\n        return sales.GroupBy(s => s.Product)\n                    .Select(g => (Product: g.Key, Total: g.Sum(x => x.Amount)))\n                    .OrderByDescending(x => x.Total)\n                    .Select(x => ((string Product, int Total)?)x)\n                    .First();\n    }\n    public static double AverageSale(List<Sale> sales, string region)\n    {\n        if (sales == null) return 0.0;\n        var match = sales.Where(s => string.Equals(s.Region, region, StringComparison.OrdinalIgnoreCase)).ToList();\n        if (match.Count == 0) return 0.0;\n        return match.Average(s => (double)s.Amount);\n    }\n}\n',
)

print("module 15 authored")
