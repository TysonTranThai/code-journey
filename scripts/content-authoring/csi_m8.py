#!/usr/bin/env python3
"""C# — Intermediate — Module 8: csi-linq.

LINQ deep cuts: the operator families you actually combine in production —
grouping, joins, aggregation, set ops, windowing (Chunk/Zip) — plus the
execution model: deferred vs immediate, multiple enumeration, materialization.
Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-linq"

write_module(
    M,
    "LINQ Deep Cuts",
    "Grouping, joining, aggregating, and windowing sequences — and the execution model that decides whether it runs once or five times.",
    "LINQ Nâng cao",
    "Nhóm, nối, tổng hợp và cửa sổ hóa chuỗi — cùng mô hình thực thi quyết định query chạy một lần hay năm lần.",
    ["operator-families", "execution-model", "csi-checkpoint-m8"],
    ["csi-p8-linq"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "operator-families",
    "The Operators That Do Real Work",
    "GroupBy, Join/GroupJoin, Aggregate, Zip/Chunk, and the set operations — with the shapes they return.",
    17,
    r"""
## GroupBy produces groups of pairs

`GroupBy(keySel)` yields `IGrouping<TKey, TElement>` — a Key plus the
members in encounter order. Counts, tops, and pivots all fall out:

```csharp
var byCity = people.GroupBy(p => p.City);
foreach (var g in byCity)
    Console.WriteLine($"{g.Key}: {g.Count()}");

var topOfEach = people
    .GroupBy(p => p.City)
    .Select(g => g.OrderByDescending(p => p.Score).First());
```

`ToLookup(keySel)` is GroupBy's eager sibling: one pass, then O(1)
indexing by key, and missing keys yield EMPTY groups instead of throwing.

## Join and GroupJoin

`Join` pairs inner+outer on keys (flat rows); `GroupJoin` produces one
outer item with a group of matches — the shape of "customers with their
orders, including zero-order customers":

```csharp
var q = customers.GroupJoin(orders,
    c => c.Id, o => o.CustomerId,
    (c, cs) => (c.Name, Count: cs.Count()));
```

Left outer join = GroupJoin + SelectMany with an empty-group default.

## Aggregate: fold a sequence into one value

```csharp
int maxGap = diffs.Aggregate((acc, next) => Math.Max(acc, next));
```

Seed form `Aggregate(seed, func, resultSelector)` builds arbitrary results.
Prefer a plain foreach when the fold needs explanation — Aggregate is not a
flex.

## Windowing and sets

- `Zip(second)` pairs element-wise (stops at shorter).
- `Chunk(size)` splits into fixed-size batches (.NET 6+).
- `Distinct/Union/Intersect/Except` compare by DEFAULT equality —
  pass a comparer or project first for value semantics.

## Check your understanding

- GroupBy vs ToLookup — which is lazy? (GroupBy; ToLookup runs immediately.)
- Which join keeps customers with zero orders? (GroupJoin.)
""",
    "Những Toán tử làm việc thật",
    "GroupBy, Join/GroupJoin, Aggregate, Zip/Chunk và các phép tập hợp — cùng hình dạng kết quả chúng trả về.",
    r"""
## GroupBy sinh các nhóm cặp

`GroupBy(keySel)` yield `IGrouping<TKey, TElement>` — một Key cùng các phần
tử theo thứ tự gặp. Đếm, top, pivot đều rút ra được:

```csharp
var byCity = people.GroupBy(p => p.City);
foreach (var g in byCity)
    Console.WriteLine($"{g.Key}: {g.Count()}");

var topOfEach = people
    .GroupBy(p => p.City)
    .Select(g => g.OrderByDescending(p => p.Score).First());
```

`ToLookup(keySel)` là anh em eager của GroupBy: một lượt duyệt, sau đó truy
theo key O(1), và key thiếu trả nhóm RỖNG thay vì ném lỗi.

## Join và GroupJoin

`Join` ghép inner+outer theo key (hàng phẳng); `GroupJoin` sinh một phần tử
outer kèm nhóm khớp — hình dạng "khách hàng với đơn hàng của họ, gồm cả
khách không có đơn":

```csharp
var q = customers.GroupJoin(orders,
    c => c.Id, o => o.CustomerId,
    (c, cs) => (c.Name, Count: cs.Count()));
```

Left outer join = GroupJoin + SelectMany với mặc định nhóm rỗng.

## Aggregate: gấp chuỗi thành một giá trị

```csharp
int maxGap = diffs.Aggregate((acc, next) => Math.Max(acc, next));
```

Dạng có seed `Aggregate(seed, func, resultSelector)` dựng kết quả tùy ý.
Khi phép gấp cần được giải thích, hãy dùng foreach — Aggregate không phải
để khoe.

## Cửa sổ và tập hợp

- `Zip(second)` ghép theo cặp (dừng ở chuỗi ngắn hơn).
- `Chunk(size)` cắt thành các lô cỡ cố định (.NET 6+).
- `Distinct/Union/Intersect/Except` so sánh bằng equality MẶC ĐỊNH —
  truyền comparer hoặc project trước để có so sánh theo giá trị.

## Kiểm tra hiểu biết

- GroupBy vs ToLookup — cái nào lười? (GroupBy; ToLookup chạy ngay.)
- Join nào giữ lại khách hàng không có đơn? (GroupJoin.)
""",
    r"""
## GroupBy sinh các nhóm cặp

`GroupBy(keySel)` yield `IGrouping<TKey, TElement>` — một Key cùng các phần
tử theo thứ tự gặp. Đếm, top, pivot đều rút ra được:

```csharp
var byCity = people.GroupBy(p => p.City);
foreach (var g in byCity)
    Console.WriteLine($"{g.Key}: {g.Count()}");

var topOfEach = people
    .GroupBy(p => p.City)
    .Select(g => g.OrderByDescending(p => p.Score).First());
```

`ToLookup(keySel)` là anh em eager của GroupBy: một lượt duyệt, sau đó truy
theo key O(1), và key thiếu trả nhóm RỖNG thay vì ném lỗi.

## Join và GroupJoin

`Join` ghép inner+outer theo key (hàng phẳng); `GroupJoin` sinh một phần tử
outer kèm nhóm khớp — hình dạng "khách hàng với đơn hàng của họ, gồm cả
khách không có đơn":

```csharp
var q = customers.GroupJoin(orders,
    c => c.Id, o => o.CustomerId,
    (c, cs) => (c.Name, Count: cs.Count()));
```

Left outer join = GroupJoin + SelectMany với mặc định nhóm rỗng.

## Aggregate: gấp chuỗi thành một giá trị

```csharp
int maxGap = diffs.Aggregate((acc, next) => Math.Max(acc, next));
```

Dạng có seed `Aggregate(seed, func, resultSelector)` dựng kết quả tùy ý.
Khi phép gấp cần được giải thích, hãy dùng foreach — Aggregate không phải
để khoe.

## Cửa sổ và tập hợp

- `Zip(second)` ghép theo cặp (dừng ở chuỗi ngắn hơn).
- `Chunk(size)` cắt thành các lô cỡ cố định (.NET 6+).
- `Distinct/Union/Intersect/Except` so sánh bằng equality MẶC ĐỊNH —
  truyền comparer hoặc project trước để có so sánh theo giá trị.

## Kiểm tra hiểu biết

- GroupBy vs ToLookup — cái nào lười? (GroupBy; ToLookup chạy ngay.)
- Join nào giữ lại khách hàng không có đơn? (GroupJoin.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "execution-model",
    "Deferred, Immediate, and the Multiple-Enumeration Trap",
    "When a query runs, what re-runs it, and the materialization discipline that keeps sources honest.",
    16,
    r"""
## Two execution modes, one rule of thumb

Most operators are DEFERRED — they record a plan. `Count()`, `ToList()`,
`ToArray()`, `ToDictionary()`, `First()`, `Sum()`, `Any()` are IMMEDIATE —
they pull. Composition chains stay lazy until one of those fires:

```csharp
var big = nums.Where(n => n > 10).Select(n => n * 2);   // no work yet
var total = big.Sum();                                  // NOW the pipeline runs
```

Sources matter: an array re-iterates cheaply, but a query built on a
method with side effects re-triggers them on EVERY enumeration.

## The multiple-enumeration bug

```csharp
var expensive = LoadAndParse();          // IEnumerable — lazy
if (expensive.Any())                     // pass 1
    Render(expensive.Where(x => x.Ok)); // pass 2: LoadAndParse again!
```

Fix: materialize once at the boundary — `var data = LoadAndParse().ToList();`
— then query the list freely. Materialize EAGER data sparingly (memory),
LAZY side-effecting sources always.

## Captured variables: the plan is not a snapshot

A deferred query closes over VARIABLES, so changing them before execution
changes the result:

```csharp
int threshold = 10;
var q = nums.Where(n => n > threshold);
threshold = 100;            // q now uses 100 — queries see current state
```

This is the same capture semantics as lambdas (Module 3) applied to plans.

## IEnumerable vs IQueryable (concept)

`IEnumerable<T>` composes delegates; filtering happens in memory.
`IQueryable<T>` composes EXPRESSION TREES a provider can translate (to SQL).
You use IQueryable against a database in Advanced/data work — but the
discipline here (look at the source, know when it runs) is the same.

## Check your understanding

- Which operator makes the whole chain run? (Any immediate operator.)
- Why materialize a side-effecting source once? (Every enumeration re-runs the side effects.)
""",
    "Trì hoãn, Ngay lập tức, và Cái bẫy Nhiều lần liệt kê",
    "Query chạy khi nào, cái gì chạy lại nó, và kỷ luật hóa-rắn giữ nguồn trung thực.",
    r"""
## Hai chế độ thực thi, một quy tắc

Hầu hết toán tử là TRÌ HOÃN — chúng ghi lại kế hoạch. `Count()`, `ToList()`,
`ToArray()`, `ToDictionary()`, `First()`, `Sum()`, `Any()` là NGAY LẬP TỨC —
chúng kéo dữ liệu. Chuỗi ghép vẫn lười cho tới khi một trong những hàm đó
kích hoạt:

```csharp
var big = nums.Where(n => n > 10).Select(n => n * 2);   // chưa làm gì
var total = big.Sum();                                  // BÂY GIỜ pipeline chạy
```

Nguồn quan trọng: mảng duyệt lại rẻ, nhưng query dựng trên phương thức có
tác dụng phụ sẽ kích hoạt lại chúng ở MỌI lần liệt kê.

## Cái bẫy nhiều lần liệt kê

```csharp
var expensive = LoadAndParse();          // IEnumerable — lười
if (expensive.Any())                     // lượt 1
    Render(expensive.Where(x => x.Ok)); // lượt 2: LoadAndParse lần nữa!
```

Chữa: hóa rắn một lần ở ranh giới — `var data = LoadAndParse().ToList();`
— rồi query trên danh sách thoải mái. Hóa rắn dữ liệu EAGER hạn chế (bộ
nhớ), nguồn lười có tác dụng phụ thì luôn luôn.

## Biến bị bắt: kế hoạch không phải ảnh chụp

Query trì hoãn đóng trên BIẾN, nên đổi biến trước khi thực thi sẽ đổi kết
quả:

```csharp
int threshold = 10;
var q = nums.Where(n => n > threshold);
threshold = 100;            // q giờ dùng 100 — query thấy trạng thái hiện tại
```

Đây chính là ngữ nghĩa capture của lambda (Module 3) áp cho kế hoạch.

## IEnumerable vs IQueryable (khái niệm)

`IEnumerable<T>` ghép delegate; lọc diễn ra trong bộ nhớ. `IQueryable<T>`
ghép EXPRESSION TREE mà provider có thể dịch (sang SQL). Bạn dùng
IQueryable với database ở phần Nâng cao/dữ liệu — nhưng kỷ luật ở đây
(nhìn nguồn, biết khi nào nó chạy) thì giống hệt.

## Kiểm tra hiểu biết

- Toán tử nào khiến cả chuỗi chạy? (Bất kỳ toán tử ngay lập tức nào.)
- Vì sao hóa rắn nguồn có tác dụng phụ một lần? (Mỗi lần liệt kê chạy lại tác dụng phụ.)
""",
    r"""
## Hai chế độ thực thi, một quy tắc

Hầu hết toán tử là TRÌ HOÃN — chúng ghi lại kế hoạch. `Count()`, `ToList()`,
`ToArray()`, `ToDictionary()`, `First()`, `Sum()`, `Any()` là NGAY LẬP TỨC —
chúng kéo dữ liệu. Chuỗi ghép vẫn lười cho tới khi một trong những hàm đó
kích hoạt:

```csharp
var big = nums.Where(n => n > 10).Select(n => n * 2);   // chưa làm gì
var total = big.Sum();                                  // BÂY GIỜ pipeline chạy
```

Nguồn quan trọng: mảng duyệt lại rẻ, nhưng query dựng trên phương thức có
tác dụng phụ sẽ kích hoạt lại chúng ở MỌI lần liệt kê.

## Cái bẫy nhiều lần liệt kê

```csharp
var expensive = LoadAndParse();          // IEnumerable — lười
if (expensive.Any())                     // lượt 1
    Render(expensive.Where(x => x.Ok)); // lượt 2: LoadAndParse lần nữa!
```

Chữa: hóa rắn một lần ở ranh giới — `var data = LoadAndParse().ToList();`
— rồi query trên danh sách thoải mái. Hóa rắn dữ liệu EAGER hạn chế (bộ
nhớ), nguồn lười có tác dụng phụ thì luôn luôn.

## Biến bị bắt: kế hoạch không phải ảnh chụp

Query trì hoãn đóng trên BIẾN, nên đổi biến trước khi thực thi sẽ đổi kết
quả:

```csharp
int threshold = 10;
var q = nums.Where(n => n > threshold);
threshold = 100;            // q giờ dùng 100 — query thấy trạng thái hiện tại
```

Đây chính là ngữ nghĩa capture của lambda (Module 3) áp cho kế hoạch.

## IEnumerable vs IQueryable (khái niệm)

`IEnumerable<T>` ghép delegate; lọc diễn ra trong bộ nhớ. `IQueryable<T>`
ghép EXPRESSION TREE mà provider có thể dịch (sang SQL). Bạn dùng
IQueryable với database ở phần Nâng cao/dữ liệu — nhưng kỷ luật ở đây
(nhìn nguồn, biết khi nào nó chạy) thì giống hệt.

## Kiểm tra hiểu biết

- Toán tử nào khiến cả chuỗi chạy? (Bất kỳ toán tử ngay lập tức nào.)
- Vì sao hóa rắn nguồn có tác dụng phụ một lần? (Mỗi lần liệt kê chạy lại tác dụng phụ.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p8-linq",
    "LINQ Practice: Sales Analytics",
    "Predict grouped shapes, spot the double-enumeration bug, and write aggregate reports.",
    "Luyện LINQ: Phân tích Bán hàng",
    "Dự đoán hình dạng nhóm, bắt lỗi liệt kê kép, và viết báo cáo tổng hợp.",
    "execution-model",
    30,
    "intermediate",
    [
        challenge(
            "csi-p8-top-customers",
            "Top Customers by Revenue",
            """Given order lines (customer, amount, day), return the top N customers by total revenue, formatted "Name: total" (ties broken by name ascending).

```csharp
public record OrderLine(string Customer, decimal Amount, int Day);
static List<string> TopCustomers(IEnumerable<OrderLine> lines, int n);
```""",
            CS_PRELUDE,
            [
                (
                    "totals and ordering",
                    r"""
var lines = new[] {
    new Solution.OrderLine("ann", 100m, 1),
    new Solution.OrderLine("bob", 50m, 1),
    new Solution.OrderLine("ann", 30m, 2),
    new Solution.OrderLine("cid", 200m, 2),
};
Cj.Eq(string.Join("|", Solution.TopCustomers(lines, 2)), "cid: 200|ann: 130", "sorted by total desc");
Cj.Eq(string.Join("|", Solution.TopCustomers(lines, 1)), "cid: 200", "top 1");
""",
                    "GroupBy customer, sum amounts, order by total desc then name, take n, format.",
                ),
                (
                    "tie-break by name",
                    r"""
var tied = new[] {
    new Solution.OrderLine("zed", 100m, 1),
    new Solution.OrderLine("amy", 100m, 1),
};
Cj.Eq(string.Join("|", Solution.TopCustomers(tied, 2)), "amy: 100|zed: 100", "name asc on ties");
Cj.Eq(Solution.TopCustomers(new Solution.OrderLine[0], 3).Count, 0, "empty input");
""",
                    "ThenBy(name) after OrderByDescending(total).",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p8-group-report",
            "Daily Sales Report with GroupBy",
            """Produce a per-day report: "Day 1: 3 orders, avg 42.5" — average of amounts rounded to 1 decimal (MidpointRounding.AwayFromZero), days in ascending order, zero-padded to width 2.

```csharp
static List<string> DailyReport(IEnumerable<Solution.OrderLine> lines);
```""",
            CS_PRELUDE,
            [
                (
                    "grouping, formatting, ordering",
                    r"""
var lines = new[] {
    new Solution.OrderLine("a", 10m, 2),
    new Solution.OrderLine("b", 20m, 1),
    new Solution.OrderLine("c", 55m, 2),
    new Solution.OrderLine("d", 30m, 1),
};
Cj.Eq(string.Join("|", Solution.DailyReport(lines)), "Day 01: 2 orders, avg 25.0|Day 02: 2 orders, avg 32.5", "days ASCENDING, not encounter order");
""",
                    "GroupBy(l => l.Day), ORDER BY key (days arrive out of order), Count + Average + round, format with 2-digit padding.",
                ),
                (
                    "rounding edge",
                    r"""
var lines = new[] {
    new Solution.OrderLine("a", 10m, 3),
    new Solution.OrderLine("b", 15m, 3),
};
Cj.Eq(string.Join("|", Solution.DailyReport(lines)), "Day 03: 2 orders, avg 12.5", "12.5 stays 12.5");
var empty = Solution.DailyReport(new Solution.OrderLine[0]);
Cj.Eq(empty.Count, 0, "no orders, no days");
""",
                    "Average returns decimal; Math.Round(x, 1, MidpointRounding.AwayFromZero); day format \"dd\".",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p8-double-enum-debug",
            "Debug: The Report That Reads the File Twice",
            """The reference implementation builds a lazy query over a counting source, checks it with Any(), then iterates it again for the report — the source is read twice. Fix Run() so the source is read exactly once while behavior stays identical.

```csharp
public sealed class CountingSource : IEnumerable<int>
{
    public CountingSource(params int[] items);
    public int ReadCount { get; }      // items actually pulled
}
static string Run(IEnumerable<int> source);   // returns "count=<n>;max=<m>"
```""",
            CS_PRELUDE,
            [
                (
                    "single pass preserved",
                    r"""
var src = new Solution.CountingSource(4, 8, 15, 16, 23, 42);
Cj.Eq(Solution.Run(src), "count=6;max=42", "report correct");
Cj.Eq(src.ReadCount, 6, "source read exactly once");
""",
                    "Materialize once: var data = source.ToList(); then count/max from data.",
                ),
                (
                    "empty input",
                    r"""
var src = new Solution.CountingSource();
Cj.Eq(Solution.Run(src), "count=0;max=0", "no items -> count=0;max=0");
Cj.Eq(src.ReadCount, 0, "nothing to read");
""",
                    "Handle the empty case without throwing (default max 0).",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p8-top-customers": vi_challenge(
            "Top khách hàng theo doanh thu",
            "Cho các dòng đơn (khách hàng, số tiền, ngày), trả về top N khách hàng theo tổng doanh thu, định dạng \"Tên: tổng\" (đồng số thì xếp tên tăng dần).",
            [
                ("totals and ordering", "GroupBy khách hàng, cộng tiền, xếp tổng giảm dần rồi tên, lấy n, định dạng."),
                ("tie-break by name", "ThenBy(tên) sau OrderByDescending(tổng)."),
            ],
        ),
        "csi-p8-group-report": vi_challenge(
            "Báo cáo theo ngày với GroupBy",
            "Sinh báo cáo từng ngày: \"Day 1: 3 orders, avg 42.5\" — trung bình số tiền làm tròn 1 chữ số (MidpointRounding.AwayFromZero), ngày tăng dần, đệm zero 2 chữ số.",
            [
                ("grouping and formatting", "GroupBy(l => l.Day), xếp theo key, Count + Average + làm tròn, định dạng 2 chữ số."),
                ("rounding edge", "Average trả decimal; Math.Round(x, 1, MidpointRounding.AwayFromZero); định dạng ngày \"dd\"."),
            ],
        ),
        "csi-p8-double-enum-debug": vi_challenge(
            "Debug: Báo cáo đọc file hai lần",
            "Bản tham khảo dựng query lười trên nguồn đếm được, kiểm tra bằng Any(), rồi duyệt lần nữa để lập báo cáo — nguồn bị đọc hai lần. Sửa Run() để nguồn đọc đúng một lần trong khi hành vi giữ nguyên.",
            [
                ("single pass preserved", "Hóa rắn một lần: var data = source.ToList(); rồi đếm/max từ data."),
                ("empty input", "Xử lý trường hợp rỗng không ném lỗi (max mặc định 0)."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p8-top-customers",
            'public class Solution\n{\n    public record OrderLine(string Customer, decimal Amount, int Day);\n\n    public static List<string> TopCustomers(IEnumerable<OrderLine> lines, int n)\n    {\n        return lines\n            .GroupBy(l => l.Customer)\n            .Select(g => new { Name = g.Key, Total = g.Sum(l => l.Amount) })\n            .OrderByDescending(x => x.Total)\n            .ThenBy(x => x.Name)\n            .Take(n)\n            .Select(x => x.Name + ": " + x.Total)\n            .ToList();\n    }\n}\n',
            'public class Solution\n{\n    public record OrderLine(string Customer, decimal Amount, int Day);\n\n    public static List<string> TopCustomers(IEnumerable<OrderLine> lines, int n)\n    {\n        // near-miss: no ThenBy — OrderByDescending alone is NOT stable for\n        // equal keys in LINQ-to-objects group ordering, so the tie test fails\n        return lines\n            .GroupBy(l => l.Customer)\n            .Select(g => new { Name = g.Key, Total = g.Sum(l => l.Amount) })\n            .OrderByDescending(x => x.Total)\n            .Take(n)\n            .Select(x => x.Name + ": " + x.Total)\n            .ToList();\n    }\n}\n',
        ),
        (
            "csi-p8-group-report",
            'public class Solution\n{\n    public record OrderLine(string Customer, decimal Amount, int Day);\n\n    public static List<string> DailyReport(IEnumerable<OrderLine> lines)\n    {\n        return lines\n            .GroupBy(l => l.Day)\n            .OrderBy(g => g.Key)\n            .Select(g =>\n            {\n                decimal avg = Math.Round(g.Average(l => l.Amount), 1, MidpointRounding.AwayFromZero);\n                return "Day " + g.Key.ToString("00") + ": " + g.Count() + " orders, avg " + avg.ToString("0.0", System.Globalization.CultureInfo.InvariantCulture);\n            })\n            .ToList();\n    }\n}\n',
            'public class Solution\n{\n    public record OrderLine(string Customer, decimal Amount, int Day);\n\n    public static List<string> DailyReport(IEnumerable<OrderLine> lines)\n    {\n        // near-miss: forgot OrderBy(g => g.Key) — dictionary-group enumeration\n        // order happens to look sorted for this input but the explicit ordering\n        // contract is broken; the reversed-days test fails\n        return lines\n            .GroupBy(l => l.Day)\n            .Select(g =>\n            {\n                decimal avg = Math.Round(g.Average(l => l.Amount), 1, MidpointRounding.AwayFromZero);\n                return "Day " + g.Key.ToString("00") + ": " + g.Count() + " orders, avg " + avg.ToString("0.0", System.Globalization.CultureInfo.InvariantCulture);\n            })\n            .ToList();\n    }\n}\n',
        ),
        (
            "csi-p8-double-enum-debug",
            'public class Solution\n{\n    public sealed class CountingSource : System.Collections.Generic.IEnumerable<int>\n    {\n        private readonly int[] _items;\n        public CountingSource(params int[] items) => _items = items;\n        public int ReadCount { get; private set; }\n\n        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();\n\n        public System.Collections.Generic.IEnumerator<int> GetEnumerator()\n        {\n            foreach (int item in _items)\n            {\n                ReadCount++;\n                yield return item;\n            }\n        }\n    }\n\n    public static string Run(System.Collections.Generic.IEnumerable<int> source)\n    {\n        // fixed: ONE enumeration — materialize first, then aggregate freely\n        var data = source.ToList();\n        int count = data.Count;\n        int max = count > 0 ? data.Max() : 0;\n        return "count=" + count + ";max=" + max;\n    }\n}\n',
            'public class Solution\n{\n    public sealed class CountingSource : System.Collections.Generic.IEnumerable<int>\n    {\n        private readonly int[] _items;\n        public CountingSource(params int[] items) => _items = items;\n        public int ReadCount { get; private set; }\n\n        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();\n\n        public System.Collections.Generic.IEnumerator<int> GetEnumerator()\n        {\n            foreach (int item in _items)\n            {\n                ReadCount++;\n                yield return item;\n            }\n        }\n    }\n\n    public static string Run(System.Collections.Generic.IEnumerable<int> source)\n    {\n        // near-miss: still TWO passes over the lazy source — Count() pulls\n        // everything once, Max() pulls it all again; ReadCount == 12 for the\n        // six-item test\n        int count = source.Count();\n        int max = count > 0 ? source.Max() : 0;\n        return "count=" + count + ";max=" + max;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m8",
    "Checkpoint — The Analytics Engine",
    "Combine grouping, joining, and aggregation into one report with honest single-pass semantics.",
    25,
    r"""
## The gate (mini-build)

A tiny sales analytics engine over in-memory rows:

1. `Revenue(IEnumerable<Sale> sales)` → total revenue (decimal).
2. `BestCategory(IEnumerable<Sale> sales)` → category name with the highest
   revenue (ties: earliest alphabetically).
3. `CustomerMatrix(IEnumerable<Sale> sales, IEnumerable<string> customers)`
   → per-customer totals in the ORDER GIVEN (zero for customers with no
   sales), formatted "name=total".
4. `Run(IEnumerable<Sale> sales, IEnumerable<string> customers)` → a report
   string combining all three, computed from ONE enumeration of sales
   (graded with a counting source — a second pull fails).

Sale record: `(string Customer, string Category, decimal Amount)`.
""",
    "Checkpoint — Bộ máy Phân tích",
    "Kết hợp nhóm, nối và tổng hợp thành một báo cáo với ngữ nghĩa một-lượt trung thực.",
    r"""
## Cổng kiểm tra (mini-build)

Một bộ máy phân tích bán hàng nhỏ trên các hàng trong bộ nhớ:

1. `Revenue(IEnumerable<Sale> sales)` → tổng doanh thu (decimal).
2. `BestCategory(IEnumerable<Sale> sales)` → tên danh mục có doanh thu cao
   nhất (đồng số: đứng trước theo bảng chữ cái).
3. `CustomerMatrix(IEnumerable<Sale> sales, IEnumerable<string> customers)`
   → tổng theo từng khách hàng THEO THỨ TỰ ĐÃ CHO (khách không có đơn là 0),
   định dạng "name=total".
4. `Run(IEnumerable<Sale> sales, IEnumerable<string> customers)` → chuỗi
   báo cáo gộp cả ba, tính từ MỘT lượt liệt kê sales (chấm bằng nguồn đếm
   được — kéo lần hai là trượt).

Sale record: `(string Customer, string Category, decimal Amount)`.
""",
    challenge(
        "csi-checkpoint-m8-task",
        "Checkpoint: One-Pass Analytics",
        """Implement the analytics engine described in the checkpoint:

```csharp
public record Sale(string Customer, string Category, decimal Amount);
static decimal Revenue(IEnumerable<Sale> sales);
static string BestCategory(IEnumerable<Sale> sales);
static List<string> CustomerMatrix(IEnumerable<Sale> sales, IEnumerable<string> customers);
static string Run(IEnumerable<Sale> sales, IEnumerable<string> customers);
// Run format: "revenue=<r>;best=<c>;|name=total|name=total..."
```""",
        CS_PRELUDE,
        [
            (
                "revenue and best category",
                r"""
var sales = new[] {
    new Solution.Sale("ann", "books", 40m),
    new Solution.Sale("bob", "toys", 70m),
    new Solution.Sale("ann", "toys", 20m),
};
Cj.Eq(Solution.Revenue(sales), 130m, "total revenue");
Cj.Eq(Solution.BestCategory(sales), "toys", "90m toys beats 40m books");
""",
                    "Sum and a GroupBy-category with Sum, ordered by amount desc then name.",
                ),
                (
                    "customer matrix keeps order, zeros included",
                    r"""
var sales = new[] {
    new Solution.Sale("ann", "books", 40m),
    new Solution.Sale("cid", "toys", 10m),
};
Cj.Eq(string.Join("|", Solution.CustomerMatrix(sales, new[] { "ann", "bob", "cid" })),
      "ann=40|bob=0|cid=10", "given order, zero for no sales");
""",
                    "ToDictionary from a GroupBy, then map the customer list — do NOT sort.",
                ),
                (
                    "one pass through sales",
                    r"""
var counter = new Solution.CountingSales(
    new Solution.Sale("ann", "books", 40m),
    new Solution.Sale("bob", "toys", 70m));
string report = Solution.Run(counter, new[] { "ann", "bob" });
Cj.Eq(report.Contains("revenue=110"), true, "revenue present");
Cj.Eq(report.Contains("best=toys"), true, "best present");
Cj.Eq(report.Contains("ann=40"), true, "matrix present");
Cj.Eq(counter.ReadCount, 2, "sales enumerated exactly once");
""",
                    "Materialize sales ONCE (ToList) inside Run; derive revenue/best/matrix from the list.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Phân tích một lượt",
            "Hiện thực bộ máy phân tích: tổng doanh thu, danh mục tốt nhất (đồng số → bảng chữ cái), ma trận khách theo thứ tự cho (không có đơn = 0), và Run tính từ MỘT lượt liệt kê sales — bộ đếm chứng minh.",
            [
                ("revenue and best category", "Sum và GroupBy theo danh mục với Sum, xếp tiền giảm dần rồi tên."),
                ("customer matrix keeps order, zeros included", "ToDictionary từ GroupBy rồi map danh sách khách — KHÔNG xếp lại."),
                ("one pass through sales", "Hóa rắn sales MỘT LẦN (ToList) trong Run; cả ba số liệu từ danh sách đó."),
            ],
        ),
        solution='public class Solution\n{\n    public record Sale(string Customer, string Category, decimal Amount);\n\n    public sealed class CountingSales : System.Collections.Generic.IEnumerable<Sale>\n    {\n        private readonly Sale[] _sales;\n        public CountingSales(params Sale[] sales) => _sales = sales;\n        public int ReadCount { get; private set; }\n\n        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();\n\n        public System.Collections.Generic.IEnumerator<Sale> GetEnumerator()\n        {\n            foreach (Sale s in _sales)\n            {\n                ReadCount++;\n                yield return s;\n            }\n        }\n    }\n\n    public static decimal Revenue(System.Collections.Generic.IEnumerable<Sale> sales) =>\n        sales.Sum(s => s.Amount);\n\n    public static string BestCategory(System.Collections.Generic.IEnumerable<Sale> sales) =>\n        sales\n            .GroupBy(s => s.Category)\n            .Select(g => new { Category = g.Key, Total = g.Sum(s => s.Amount) })\n            .OrderByDescending(x => x.Total)\n            .ThenBy(x => x.Category)\n            .First()\n            .Category;\n\n    public static System.Collections.Generic.List<string> CustomerMatrix(\n        System.Collections.Generic.IEnumerable<Sale> sales,\n        System.Collections.Generic.IEnumerable<string> customers)\n    {\n        var totals = sales.GroupBy(s => s.Customer)\n            .ToDictionary(g => g.Key, g => g.Sum(s => s.Amount));\n        var rows = new System.Collections.Generic.List<string>();\n        foreach (string c in customers)\n            rows.Add(c + "=" + totals.GetValueOrDefault(c));\n        return rows;\n    }\n\n    public static string Run(\n        System.Collections.Generic.IEnumerable<Sale> sales,\n        System.Collections.Generic.IEnumerable<string> customers)\n    {\n        var data = sales.ToList();                       // single pull — everything derives from this\n        decimal revenue = Revenue(data);\n        string best = BestCategory(data);\n        string matrix = string.Join("|", CustomerMatrix(data, customers));\n        return "revenue=" + revenue + ";best=" + best + ";" + matrix;\n    }\n}\n',
        wrong='public class Solution\n{\n    public record Sale(string Customer, string Category, decimal Amount);\n\n    public sealed class CountingSales : System.Collections.Generic.IEnumerable<Sale>\n    {\n        private readonly Sale[] _sales;\n        public CountingSales(params Sale[] sales) => _sales = sales;\n        public int ReadCount { get; private set; }\n\n        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();\n\n        public System.Collections.Generic.IEnumerator<Sale> GetEnumerator()\n        {\n            foreach (Sale s in _sales)\n            {\n                ReadCount++;\n                yield return s;\n            }\n        }\n    }\n\n    public static decimal Revenue(System.Collections.Generic.IEnumerable<Sale> sales) =>\n        sales.Sum(s => s.Amount);\n\n    public static string BestCategory(System.Collections.Generic.IEnumerable<Sale> sales) =>\n        sales\n            .GroupBy(s => s.Category)\n            .Select(g => new { Category = g.Key, Total = g.Sum(s => s.Amount) })\n            .OrderByDescending(x => x.Total)\n            .ThenBy(x => x.Category)\n            .First()\n            .Category;\n\n    public static System.Collections.Generic.List<string> CustomerMatrix(\n        System.Collections.Generic.IEnumerable<Sale> sales,\n        System.Collections.Generic.IEnumerable<string> customers)\n    {\n        var totals = sales.GroupBy(s => s.Customer)\n            .ToDictionary(g => g.Key, g => g.Sum(s => s.Amount));\n        var rows = new System.Collections.Generic.List<string>();\n        foreach (string c in customers)\n            rows.Add(c + "=" + totals.GetValueOrDefault(c));\n        return rows;\n    }\n\n    public static string Run(\n        System.Collections.Generic.IEnumerable<Sale> sales,\n        System.Collections.Generic.IEnumerable<string> customers)\n    {\n        // near-miss: calls Revenue(sales) and BestCategory(sales) on the raw\n        // lazy source — two MORE pulls on top of CustomerMatrix — the counting\n        // source reports 3x reads and the one-pass test fails\n        decimal revenue = Revenue(sales);\n        string best = BestCategory(sales);\n        string matrix = string.Join("|", CustomerMatrix(sales, customers));\n        return "revenue=" + revenue + ";best=" + best + ";" + matrix;\n    }\n}\n',
    )
print("module 8 authored")
