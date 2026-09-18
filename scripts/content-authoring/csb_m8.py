#!/usr/bin/env python3
"""C# — Beginner — Module 8: csb-collections.

List<T>, Dictionary<TKey,TValue>, HashSet<T> and choosing between them:
capacity vs length, TryGetValue over indexer+ContainsKey, and the
foreach-modification trap. House conventions: Ws are behavioral
near-misses, tests discriminate.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-collections"

write_module(
    M,
    "Collections",
    "Lists, dictionaries, and sets: dynamic containers, key-value lookups, uniqueness — and when each is the right shape.",
    "Bộ sưu tập",
    "List, Dictionary, HashSet: bộ chứa động, tra cứu theo khóa, tính duy nhất — và khi nào dạng nào là đúng.",
    ["csb-m8-list", "csb-m8-dict", "csb-m8-set", "csb-checkpoint-m8"],
    ["csb-p8-collections"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m8-list",
    "List<T> — the growing array",
    "Add, Count, indexing, Remove, Contains — and Count vs Capacity.",
    13,
    r"""
## Arrays that grow

```csharp
var names = new List<string>();     // empty
names.Add("an");
names.Add("binh");
Console.WriteLine(names.Count);     // 2 — actual elements
names[0] = "An";                    // index like an array
names.Remove("binh");               // removes first equal element
Console.WriteLine(names.Contains("An"));   // True
```

`List<T>` wraps an array it reallocates behind your back: `Add` is amortized O(1), `Count` is the real element count. `Capacity` is the internal array's size — you almost never need to touch it. **`Count`, not `Length`,** is the beginner tell that a list isn't an array.

## Removal, insertion, searching

```csharp
names.Insert(0, "cuong");       // O(n) — everything shifts
names.RemoveAt(names.Count - 1);   // remove last
int at = names.IndexOf("An");   // -1 when absent, like arrays
names.Sort();                   // in-place, same contract as Array.Sort
```

`Remove` and `RemoveAt` shift everything after the removed slot — cheap at the end, expensive at the front. If you find yourself doing front-heavy insertion, the list may be the wrong shape (a deque/stack model fits better).

## Iterating safely

`foreach` over a list while `Add`/`Remove`-ing throws `InvalidOperationException` — the list is being modified during enumeration. Collect the changes and apply after the loop, or use a `for` loop backwards when removing by index.
""",
    "List<T> — mảng tự lớn",
    "Add, Count, truy chỉ số, Remove, Contains — và Count khác Capacity.",
    r"""
## Mảng tự lớn

```csharp
var names = new List<string>();     // rỗng
names.Add("an");
names.Add("binh");
Console.WriteLine(names.Count);     // 2 — số phần tử thật
names[0] = "An";                    // truy chỉ số như mảng
names.Remove("binh");               // xóa phần tử đầu bằng nhau
Console.WriteLine(names.Contains("An"));   // True
```

`List<T>` bọc một mảng mà nó tự cấp phát lại phía sau: `Add` là O(1) khấu trừ, `Count` là số phần tử thật. `Capacity` là kích thước mảng nội bộ — gần như không bao giờ cần đụng. **`Count`, không phải `Length`,** là dấu hiệu nhận biết list không phải mảng.

## Xóa, chèn, tìm kiếm

```csharp
names.Insert(0, "cuong");       // O(n) — mọi thứ dịch chuyển
names.RemoveAt(names.Count - 1);   // xóa cuối
int at = names.IndexOf("An");   // -1 khi vắng, như mảng
names.Sort();                   // tại chỗ, cùng hợp đồng Array.Sort
```

`Remove` và `RemoveAt` dịch mọi thứ sau vị trí xóa — rẻ ở cuối, đắt ở đầu. Nếu bạn cứ chèn ở đầu hoài, list có thể là dạng sai (mô hình deque/stack hợp hơn).

## Duyệt an toàn

`foreach` trên một list đang `Add`/`Remove` sẽ ném `InvalidOperationException` — list bị biến đổi trong khi liệt kê. Thu thập thay đổi rồi áp dụng sau vòng lặp, hoặc dùng `for` đi ngược khi xóa theo chỉ số.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m8-dict",
    "Dictionary<TKey, TValue> — lookup by key",
    "Add, indexing, TryGetValue, ContainsKey — and why the indexer throws on a missing key.",
    13,
    r"""
## Keys map to values

```csharp
var ages = new Dictionary<string, int>();
ages["an"] = 30;               // insert or overwrite
ages.Add("binh", 25);          // THROWS if "binh" already exists
Console.WriteLine(ages["an"]); // 30 — THROWS if "an" is absent
```

The indexer **creates or overwrites**; `Add` refuses duplicates. Reading `ages["missing"]` throws `KeyNotFoundException` — the single most common dictionary crash. Two safe reads:

```csharp
if (ages.TryGetValue("missing", out int age))
    Console.WriteLine(age);    // out param set only when found

if (ages.ContainsKey("missing")) { ... }   // check without reading
```

`TryGetValue` is preferred: one lookup instead of two (`ContainsKey` then indexer), and it gives you the value.

## Counting things — the classic pattern

```csharp
var votes = new Dictionary<string, int>();
foreach (string ballot in ballots)
{
    votes.TryGetValue(ballot, out int n);
    votes[ballot] = n + 1;      // read-modify-write
}
```

`TryGetValue` with `out` conveniently yields `0` when the key is absent, so the pattern handles first-votes without a branch. Counting, grouping, and deduplicating (next lesson) are the three dictionary superpowers — every practice challenge here is one of them.

## Iteration

`foreach (var kv in ages)` yields `KeyValuePair<string,int>` — read `kv.Key`/`kv.Value`. Dictionaries have **no defined order**; never write logic that depends on enumeration order.
""",
    "Dictionary<TKey, TValue> — tra cứu theo khóa",
    "Add, truy chỉ số, TryGetValue, ContainsKey — và vì sao indexer ném khi thiếu khóa.",
    r"""
## Khóa ánh xạ giá trị

```csharp
var ages = new Dictionary<string, int>();
ages["an"] = 30;               // chèn hoặc ghi đè
ages.Add("binh", 25);          // NÉM nếu "binh" đã tồn tại
Console.WriteLine(ages["an"]); // 30 — NÉM nếu "an" vắng mặt
```

Indexer **tạo hoặc ghi đè**; `Add` từ chối trùng lặp. Đọc `ages["missing"]` ném `KeyNotFoundException` — crash dictionary phổ biến nhất. Hai cách đọc an toàn:

```csharp
if (ages.TryGetValue("missing", out int age))
    Console.WriteLine(age);    // out param chỉ được gán khi thấy

if (ages.ContainsKey("missing")) { ... }   // kiểm tra mà không đọc
```

`TryGetValue` được ưa chuộng: một lần tra cứu thay vì hai (`ContainsKey` rồi indexer), và nó cho luôn giá trị.

## Đếm — mẫu kinh điển

```csharp
var votes = new Dictionary<string, int>();
foreach (string ballot in ballots)
{
    votes.TryGetValue(ballot, out int n);
    votes[ballot] = n + 1;      // đọc-biến đổi-ghi
}
```

`TryGetValue` với `out` tiện lợi vì cho `0` khi khóa vắng, nên mẫu này xử lý phiếu đầu tiên mà không cần rẽ nhánh. Đếm, nhóm, và khử trùng lặp (bài sau) là ba siêu năng lực của dictionary — mọi thử thách ở đây là một trong ba.

## Duyệt

`foreach (var kv in ages)` cho `KeyValuePair<string,int>` — đọc `kv.Key`/`kv.Value`. Dictionary **không có thứ tự xác định**; đừng viết logic dựa vào thứ tự duyệt.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m8-set",
    "HashSet<T> and choosing the right shape",
    "Uniqueness and set math, plus a decision table for List, Dictionary, and HashSet.",
    12,
    r"""
## One of each, no order

```csharp
var seen = new HashSet<string>();
seen.Add("a");          // True  — new
bool dup = seen.Add("a");   // False — already there
Console.WriteLine(seen.Count);   // 1
```

`Add` returns **whether anything changed** — a one-call duplicate check. `Contains` is O(1) (hash-based), unlike `List.Contains`'s O(n) scan. Set math is built in: `seen.UnionWith(other)`, `IntersectWith`, `ExceptWith` mutate the set; `Overlaps`/`IsSubsetOf` answer questions.

## The dedup-and-count pair

```csharp
var distinct = new HashSet<string>(words);   // copies + dedups
Console.WriteLine(distinct.Count);           // number of unique words
```

Constructing from an existing collection is the fastest dedup in the language — and combining a `HashSet` (uniqueness) with a `Dictionary` (counts) covers frequency tables.

## Choosing the shape

| Need | Shape |
| --- | --- |
| Ordered values, duplicates OK, index access | `List<T>` |
| Unique values, fast membership | `HashSet<T>` |
| Look up by a key | `Dictionary<TKey,TValue>` |
| Fixed size, index access | array |

The wrong shape forces manual workarounds — deduping a List by hand, or searching a Dictionary's Values. Decide from the *operations* you need, not habit: "do I need duplicates? do I need positions? do I need keys?" Those three questions pick the container in almost every beginner program.
""",
    "HashSet<T> và chọn đúng dạng",
    "Tính duy nhất và toán tập, cộng bảng quyết định cho List, Dictionary, HashSet.",
    r"""
## Mỗi thứ một cái, không thứ tự

```csharp
var seen = new HashSet<string>();
seen.Add("a");          // True  — mới
bool dup = seen.Add("a");   // False — đã có
Console.WriteLine(seen.Count);   // 1
```

`Add` trả **có gì thay đổi không** — kiểm tra trùng lặp trong một lệnh. `Contains` là O(1) (dựa trên băm), khác với quét O(n) của `List.Contains`. Toán tập có sẵn: `seen.UnionWith(other)`, `IntersectWith`, `ExceptWith` biến đổi tập; `Overlaps`/`IsSubsetOf` trả lời câu hỏi.

## Cặp khử trùng-lặp và đếm

```csharp
var distinct = new HashSet<string>(words);   // sao chép + khử trùng lặp
Console.WriteLine(distinct.Count);           // số từ duy nhất
```

Khởi tạo từ bộ sưu tập có sẵn là cách khử trùng lặp nhanh nhất trong ngôn ngữ — và ghép một `HashSet` (duy nhất) với một `Dictionary` (đếm) phủ các bảng tần suất.

## Chọn dạng

| Nhu cầu | Dạng |
| --- | --- |
| Giá trị có thứ tự, cho phép trùng, truy chỉ số | `List<T>` |
| Giá trị duy nhất, kiểm tra thành viên nhanh | `HashSet<T>` |
| Tra cứu theo khóa | `Dictionary<TKey,TValue>` |
| Kích thước cố định, truy chỉ số | mảng |

Dạng sai buộc bạn viết workaround thủ công — khử trùng lặp List bằng tay, hay quét Values của Dictionary. Quyết định từ các *thao tác* bạn cần, không phải thói quen: "cần trùng lặp không? cần vị trí không? cần khóa không?" Ba câu hỏi ấy chọn đúng bộ chứa trong hầu hết chương trình beginner.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p8-collections",
    "Collection workout",
    "Counting, dedup, and index maps — the dictionary trio under discriminating tests.",
    "Luyện tập bộ sưu tập",
    "Đếm, khử trùng lặp, và bản đồ chỉ số — bộ ba dictionary dưới các bài kiểm tra phân biệt.",
    "csb-m8-set",
    40,
    "beginner",
    [
        challenge(
            "csb-p8-wordcount",
            "Word frequency",
            "Implement `static Dictionary<string, int> WordCounts(IEnumerable<string> words)` — each distinct word (case-**insensitive**, store lowercased) mapped to its count. Null or empty input returns an empty dictionary.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var wc = Solution.WordCounts(new[] {\"a\", \"B\", \"a\", \"b\", \"c\"});\nCj.Eq(wc.Count, 3, \"three distinct\");\nCj.Eq(wc[\"a\"], 2, \"a twice\");\nCj.Eq(wc[\"b\"], 2, \"B counted with b\");\nCj.Eq(wc[\"c\"], 1, \"c once\");",
                    "Case folding means \"B\" and \"b\" are one word.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.WordCounts(new string[0]).Count, 0, \"empty\");\nCj.Eq(Solution.WordCounts(null).Count, 0, \"null\");\nvar one = Solution.WordCounts(new[] {\"Solo\"});\nCj.Eq(one[\"solo\"], 1, \"keys stored lowercase\");",
                    "No input, no entries — and the stored keys must be lowercase so later lookups compose.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p8-dedupe",
            "Deduplicate preserving order",
            "Implement `static List<string> Dedupe(IEnumerable<string> items)` — first occurrences only, **original order**, original casing kept. Null input returns an empty list.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var d = Solution.Dedupe(new[] {\"a\", \"b\", \"a\", \"A\", \"b\"});\nCj.Eq(string.Join(\",\", d), \"a,b,A\", \"order and case kept\");",
                    "\"A\" ≠ \"a\" — this is a set-membership filter, not case-insensitive dedup.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.Dedupe(new string[0]).Count, 0, \"empty\");\nCj.Eq(Solution.Dedupe(null).Count, 0, \"null\");\nvar s = Solution.Dedupe(new[] {\"x\"});\nCj.Eq(string.Join(\",\", s), \"x\", \"single\");",
                    "Trivial inputs must pass through intact.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p8-indexmap",
            "Last-occurrence index map",
            "Implement `static Dictionary<string, int> LastIndex(IEnumerable<string> items)` — each distinct item mapped to the index of its **last** occurrence. Null/empty yields an empty dictionary.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var m = Solution.LastIndex(new[] {\"a\", \"b\", \"a\", \"c\", \"b\"});\nCj.Eq(m[\"a\"], 2, \"a last at 2\");\nCj.Eq(m[\"b\"], 4, \"b last at 4\");\nCj.Eq(m[\"c\"], 3, \"c only at 3\");\nCj.Eq(m.Count, 3, \"three keys\");",
                    "Walk once with the running index; each assignment naturally overwrites with the latest position.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.LastIndex(new string[0]).Count, 0, \"empty\");\nCj.Eq(Solution.LastIndex(null).Count, 0, \"null\");\nvar m = Solution.LastIndex(new[] {\"z\"});\nCj.Eq(m[\"z\"], 0, \"single at index 0\");",
                    "Zero is a real index here — the empty-dictionary contract keeps 0 from meaning \"missing\".",
                ),
            ],
            level="real-world",
        ),
        challenge(
            "csb-p8-inventory",
            "Stock adjustments",
            "Implement `static Dictionary<string, int> ApplySales(Dictionary<string, int> stock, IEnumerable<(string Sku, int Qty)> sales)` — subtract each sale's quantity from the matching SKU; a sale for an unknown SKU or one that would push stock negative must throw `InvalidOperationException`. Return the same dictionary instance, mutated.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var stock = new Dictionary<string, int> { [\"pen\"] = 10, [\"ink\"] = 3 };\nvar out_ = Solution.ApplySales(stock, new[] { (\"pen\", 4), (\"ink\", 3) });\nCj.Eq(out_[\"pen\"], 6, \"pen sold\");\nCj.Eq(out_[\"ink\"], 0, \"ink to exactly zero is fine\");\nCj.True(ReferenceEquals(stock, out_), \"same instance mutated\");",
                    "Selling to exactly zero is legal; the contract is the same instance back.",
                ),
                (
                    "failures",
                    "var stock = new Dictionary<string, int> { [\"pen\"] = 2 };\nbool t1 = false, t2 = false;\ntry { Solution.ApplySales(stock, new[] { (\"pen\", 3) }); } catch (InvalidOperationException) { t1 = true; }\ntry { Solution.ApplySales(stock, new[] { (\"ghost\", 1) }); } catch (InvalidOperationException) { t2 = true; }\nCj.True(t1 && t2, \"negative and unknown both throw\");\nCj.Eq(stock[\"pen\"], 2, \"failed sale leaves stock untouched\");",
                    "A rejected sale must not have half-applied — the stock dict is unchanged after the throw.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p8-wordcount": vi_challenge(
            "Tần suất từ",
            "Hiện thực `static Dictionary<string, int> WordCounts(IEnumerable<string> words)` — mỗi từ phân biệt (không phân biệt **chữ hoa/thường**, lưu chữ thường) ánh xạ số lần xuất hiện. Input null hoặc rỗng trả dictionary rỗng.",
            [
                ("normal", "Gấp chữ nghĩa \"B\" và \"b\" là một từ."),
                ("edges", "Không input, không phần tử — và khóa lưu phải chữ thường để tra cứu sau hợp thành."),
            ],
        ),
        "csb-p8-dedupe": vi_challenge(
            "Khử trùng lặp giữ thứ tự",
            "Hiện thực `static List<string> Dedupe(IEnumerable<string> items)` — chỉ lần xuất hiện đầu, giữ **thứ tự gốc**, giữ nguyên chữ hoa/thường gốc. Input null trả list rỗng.",
            [
                ("normal", "\"A\" ≠ \"a\" — đây là bộ lọc thành viên tập, không phải khử trùng lặp không phân biệt chữ."),
            ],
        ),
        "csb-p8-indexmap": vi_challenge(
            "Bản đồ chỉ số lần cuối",
            "Hiện thực `static Dictionary<string, int> LastIndex(IEnumerable<string> items)` — mỗi phần tử phân biệt ánh xạ tới chỉ số lần xuất hiện **cuối**. Null/rỗng cho dictionary rỗng.",
            [
                ("normal", "Duyệt một lần với chỉ số chạy dần; mỗi phép gán tự nhiên ghi đè bằng vị trí mới nhất."),
                ("edges", "Số 0 là chỉ số thật ở đây — hợp đồng dictionary-rỗng khiến 0 không có nghĩa là \"vắng\"."),
            ],
        ),
        "csb-p8-inventory": vi_challenge(
            "Điều chỉnh tồn kho",
            "Hiện thực `static Dictionary<string, int> ApplySales(Dictionary<string, int> stock, IEnumerable<(string Sku, int Qty)> sales)` — trừ số lượng mỗi đơn khỏi SKU khớp; đơn cho SKU lạ hoặc sẽ đẩy tồn kho âm phải ném `InvalidOperationException`. Trả chính dictionary ban đầu, đã biến đổi.",
            [
                ("normal", "Bán về đúng 0 là hợp lệ; hợp đồng là chính instance đó trả lại."),
                ("failures", "Đơn bị từ chối không được áp dụng một nửa — dictionary tồn kho không đổi sau khi ném."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p8-wordcount",
            'public class Solution\n{\n    public static Dictionary<string, int> WordCounts(IEnumerable<string> words)\n    {\n        var result = new Dictionary<string, int>();\n        if (words == null) return result;\n        foreach (string w in words)\n        {\n            string key = w.ToLowerInvariant();\n            result.TryGetValue(key, out int n);\n            result[key] = n + 1;\n        }\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static Dictionary<string, int> WordCounts(IEnumerable<string> words)\n    {\n        var result = new Dictionary<string, int>();\n        if (words == null) return result;\n        foreach (string w in words)\n        {\n            // near-miss: stores the ORIGINAL casing as the key, so "B" and\n            // "b" become separate entries and lowercase lookups miss\n            result.TryGetValue(w, out int n);\n            result[w] = n + 1;\n        }\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p8-dedupe",
            'public class Solution\n{\n    public static List<string> Dedupe(IEnumerable<string> items)\n    {\n        var result = new List<string>();\n        if (items == null) return result;\n        var seen = new HashSet<string>();\n        foreach (string s in items)\n        {\n            if (seen.Add(s)) result.Add(s);   // Add returns false on duplicate\n        }\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static List<string> Dedupe(IEnumerable<string> items)\n    {\n        var result = new List<string>();\n        if (items == null) return result;\n        // near-miss: case-INSENSITIVE membership — "A" gets swallowed as a\n        // duplicate of "a", breaking the keep-original-casing contract\n        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);\n        foreach (string s in items)\n        {\n            if (seen.Add(s)) result.Add(s);\n        }\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p8-indexmap",
            'public class Solution\n{\n    public static Dictionary<string, int> LastIndex(IEnumerable<string> items)\n    {\n        var result = new Dictionary<string, int>();\n        if (items == null) return result;\n        int i = 0;\n        foreach (string s in items)\n        {\n            result[s] = i;   // later occurrence overwrites\n            i++;\n        }\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static Dictionary<string, int> LastIndex(IEnumerable<string> items)\n    {\n        var result = new Dictionary<string, int>();\n        if (items == null) return result;\n        int i = 0;\n        foreach (string s in items)\n        {\n            // near-miss: Add instead of indexer — a duplicate key throws\n            // ArgumentException, so any repeated item crashes the build\n            result.Add(s, i);\n            i++;\n        }\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p8-inventory",
            'public class Solution\n{\n    public static Dictionary<string, int> ApplySales(Dictionary<string, int> stock, IEnumerable<(string Sku, int Qty)> sales)\n    {\n        foreach (var sale in sales)\n        {\n            if (!stock.TryGetValue(sale.Sku, out int have))\n                throw new InvalidOperationException($"unknown sku {sale.Sku}");\n            if (sale.Qty > have)\n                throw new InvalidOperationException($"insufficient stock for {sale.Sku}");\n            stock[sale.Sku] = have - sale.Qty;\n        }\n        return stock;\n    }\n}\n',
            'public class Solution\n{\n    public static Dictionary<string, int> ApplySales(Dictionary<string, int> stock, IEnumerable<(string Sku, int Qty)> sales)\n    {\n        foreach (var sale in sales)\n        {\n            if (!stock.TryGetValue(sale.Sku, out int have))\n                throw new InvalidOperationException($"unknown sku {sale.Sku}");\n            // near-miss: no sufficiency check at all - stock silently goes\n            // negative instead of refusing the sale\n            stock[sale.Sku] = have - sale.Qty;\n        }\n        return stock;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m8",
    "Checkpoint — Collections",
    "A gradebook: per-student averages, a class ranking, and honors detection — Dictionary, List, and a little LINQ-free aggregation.",
    20,
    r"""
## Checkpoint: the gradebook

**Task:** implement three methods against `Dictionary<string, List<int>>` (student → scores):

1. `static Dictionary<string, double> Averages(Dictionary<string, List<int>> gradebook)` — each student's mean score (double division!). A student with an empty score list must NOT appear.
2. `static List<string> Honors(Dictionary<string, List<int>> gradebook)` — students whose average is ≥ 90, ordered **by descending average then ascending name**.
3. `static string TopStudent(Dictionary<string, List<int>> gradebook)` — the name with the highest average; on a tie, alphabetically first. Null/empty gradebook returns `""`.
""",
    "Checkpoint — Bộ sưu tập",
    "Sổ điểm: trung bình từng học sinh, xếp hạng lớp, và phát hiện danh dự — Dictionary, List, và một chút tổng hợp không-LINQ.",
    r"""
## Checkpoint: sổ điểm

**Nhiệm vụ:** hiện thực ba phương thức trên `Dictionary<string, List<int>>` (học sinh → điểm):

1. `static Dictionary<string, double> Averages(Dictionary<string, List<int>> gradebook)` — điểm trung bình của từng học sinh (chia double!). Học sinh có danh sách điểm rỗng KHÔNG được xuất hiện.
2. `static List<string> Honors(Dictionary<string, List<int>> gradebook)` — học sinh trung bình ≥ 90, sắp theo **trung bình giảm dần rồi tên tăng dần**.
3. `static string TopStudent(Dictionary<string, List<int>> gradebook)` — tên có trung bình cao nhất; hòa thì tên theo alphabet trước. Null/rỗng trả `""`.
""",
    challenge(
        "csb-checkpoint-m8-task",
        "Gradebook",
        "Implement `Averages`, `Honors`, and `TopStudent` as described. The empty-list exclusion, the double division, and both tie rules are the contract.",
        CS_PRELUDE,
        [
            (
                "averages",
                'var gb = new Dictionary<string, List<int>>\n{\n    ["an"] = new List<int> { 90, 90 },\n    ["binh"] = new List<int> { 80 },\n    ["empty"] = new List<int>(),\n};\nvar av = Solution.Averages(gb);\nCj.False(av.ContainsKey("empty"), "empty list excluded");\nCj.Near(av["an"], 90.0, 1e-9, "an avg");\nCj.Near(av["binh"], 80.0, 1e-9, "binh avg");\nCj.Eq(Solution.Averages(new Dictionary<string, List<int>>()).Count, 0, "empty book");\nCj.Eq(Solution.Averages(null).Count, 0, "null book");',
                "Exclusion rule, exact means, and the null/empty contracts.",
            ),
            (
                "honors-and-top",
                'var gb = new Dictionary<string, List<int>>\n{\n    ["an"] = new List<int> { 95, 95 },\n    ["binh"] = new List<int> { 90, 90 },\n    ["chi"] = new List<int> { 90, 90 },\n    ["duan"] = new List<int> { 70 },\n};\nvar h = Solution.Honors(gb);\nCj.Eq(string.Join(",", h), "an,binh,chi", "desc avg, asc name");\nCj.Eq(Solution.TopStudent(gb), "an", "top");\nvar tie = new Dictionary<string, List<int>> { ["mai"] = new List<int> { 85 }, ["hoa"] = new List<int> { 85 } };\nCj.Eq(Solution.TopStudent(tie), "hoa", "tie -> alphabetical");\nCj.Eq(Solution.TopStudent(null), "", "null top");',
                "Both orderings in Honors, the top pick, and the alphabetical tie.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Sổ điểm",
        "Hiện thực `Averages`, `Honors`, `TopStudent` như mô tả. Quy tắc loại-list-rỗng, phép chia double, và cả hai luật hòa là hợp đồng.",
        [
            ("averages", "Quy tắc loại, trung bình chính xác, và hợp đồng null/rỗng."),
            ("honors-and-top", "Cả hai thứ tự trong Honors, lựa chọn top, và hòa theo alphabet."),
        ],
    ),
    solution='public class Solution\n{\n    public static Dictionary<string, double> Averages(Dictionary<string, List<int>> gradebook)\n    {\n        var result = new Dictionary<string, double>();\n        if (gradebook == null) return result;\n        foreach (var kv in gradebook)\n        {\n            if (kv.Value == null || kv.Value.Count == 0) continue;\n            long sum = 0;\n            foreach (int s in kv.Value) sum += s;\n            result[kv.Key] = (double)sum / kv.Value.Count;\n        }\n        return result;\n    }\n\n    public static List<string> Honors(Dictionary<string, List<int>> gradebook)\n    {\n        var av = Averages(gradebook);\n        var names = new List<string>(av.Keys);\n        names.Sort((a, b) =>\n        {\n            int byAvg = av[b].CompareTo(av[a]);\n            return byAvg != 0 ? byAvg : string.CompareOrdinal(a, b);\n        });\n        return names.Where(n => av[n] >= 90.0).ToList();\n    }\n\n    public static string TopStudent(Dictionary<string, List<int>> gradebook)\n    {\n        var av = Averages(gradebook);\n        if (av.Count == 0) return "";\n        string best = null;\n        foreach (var kv in av)\n        {\n            if (best == null\n                || kv.Value > av[best]\n                || (kv.Value == av[best] && string.CompareOrdinal(kv.Key, best) < 0))\n                best = kv.Key;\n        }\n        return best;\n    }\n}\n',
    wrong='public class Solution\n{\n    public static Dictionary<string, double> Averages(Dictionary<string, List<int>> gradebook)\n    {\n        var result = new Dictionary<string, double>();\n        if (gradebook == null) return result;\n        foreach (var kv in gradebook)\n        {\n            // near-miss: does NOT skip empty score lists — an empty list makes\n            // sum 0 / count 0, which throws DivideByZeroException\n            long sum = 0;\n            foreach (int s in kv.Value) sum += s;\n            result[kv.Key] = (double)sum / kv.Value.Count;\n        }\n        return result;\n    }\n\n    public static List<string> Honors(Dictionary<string, List<int>> gradebook)\n    {\n        // near-miss: ascending name only, ignoring the average ordering\n        var av = Averages(gradebook);\n        var names = new List<string>(av.Keys);\n        names.Sort(string.CompareOrdinal);\n        return names.Where(n => av[n] >= 90.0).ToList();\n    }\n\n    public static string TopStudent(Dictionary<string, List<int>> gradebook)\n    {\n        // near-miss: breaks ties by REVERSE alphabetical — "mai" beats "hoa"\n        var av = Averages(gradebook);\n        if (av.Count == 0) return "";\n        string best = null;\n        foreach (var kv in av)\n        {\n            if (best == null\n                || kv.Value > av[best]\n                || (kv.Value == av[best] && string.CompareOrdinal(kv.Key, best) > 0))\n                best = kv.Key;\n        }\n        return best;\n    }\n}\n',
)

print("module 8 authored")
