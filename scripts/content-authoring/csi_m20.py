#!/usr/bin/env python3
"""C# — Intermediate — Module 20: csi-performance.

Performance fundamentals: string building, collection choice, LINQ
materialization/multiple enumeration, and measurement-first habits — graded
behaviorally via counting fakes and shape contracts, never by wall-clock.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-performance"

write_module(
    M,
    "Performance Fundamentals",
    "Where allocations actually come from, why collection choice dominates cost, how LINQ pipelines double their work — and why you measure before you touch anything.",
    "Nền tảng Hiệu năng",
    "Allocation thực sự đến từ đâu, vì sao chọn collection chi phối chi phí, cách pipeline LINQ nhân đôi công việc — và vì sao phải đo trước khi sửa bất cứ thứ gì.",
    ["allocations", "linq-cost", "csi-checkpoint-m20"],
    ["csi-p20-performance"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "allocations",
    "Allocations, Strings, and the Right Collection",
    "The three everyday performance levers in managed code: fewer allocations, fewer intermediate strings, the right collection for the access pattern.",
    24,
    r"""
## Measurement first — always

Before any optimization: **measure**. In .NET that means `Stopwatch` (or a
real profiler). Intuition about "slow code" is wrong constantly; a loop that
looks expensive may be free, and one innocent-looking call may dominate.
The rule for this module and beyond:

1. Measure the current shape (`Stopwatch` at minimum).
2. Change ONE thing.
3. Measure again; keep only real wins.

Everything below is about shapes whose cost is *predictable from the code* —
the ones worth fixing on sight — but even then, confirm with numbers.

## Strings are immutable — concatenation is O(n²)

Each `+=` on a string allocates a brand-new string and copies everything
so far. Building a 10,000-part report with `+=` copies ~50 million
characters. `StringBuilder` amortizes to O(n):

```csharp
// O(n^2): every += copies the whole string so far
var s = "";
foreach (var line in lines) s += line + "\n";

// O(n): one growing buffer, flushed once
var sb = new System.Text.StringBuilder();
foreach (var line in lines) sb.AppendLine(line);
var s2 = sb.ToString();
```

A few `+=` on short strings is fine. The problem is *unbounded loops*.

## Collection choice is the cheapest big win

The access pattern dictates the type — complexity, not fashion:

| You need                     | Use            | Cost            |
|------------------------------|----------------|-----------------|
| lookup by key                | `Dictionary<K,V>` | ~O(1)       |
| membership test ("have I seen X?") | `HashSet<T>` | ~O(1)     |
| index access / ordered scan  | `List<T>` / `T[]` | O(1) / O(n) scan |
| first-in-first-out           | `Queue<T>`     | O(1) both ends  |
| last-in-first-out            | `Stack<T>`     | O(1)            |

The classic hidden quadratic: inside a loop over N items, doing
`list.Contains(x)` (or `Remove`) — O(n) each — makes the whole thing O(n²).
A `HashSet` turns the inner test into ~O(1) and the loop into O(n).

```csharp
// O(n^2): Contains is a linear scan per element
foreach (var id in incoming)
    if (!seen.Contains(id)) seen.Add(id);   // seen is a List

// O(n): membership test on a HashSet
foreach (var id in incoming)
    if (seen.Add(id)) /* first occurrence */;
```

## One more allocation habit

`List<T>` grows by doubling — fine. But if you know the final size, the
constructor `new List<T>(capacity)` avoids re-allocations entirely. Reserve
this for large, known-size builds; micro-tuning small lists is noise.
""",
    "Allocation, String, và Đúng Collection",
    "Ba đòn bẩy hiệu năng hằng ngày trong code quản lý: ít allocation hơn, ít string trung gian hơn, đúng collection cho kiểu truy cập.",
    r"""
## Đo trước — luôn luôn

Trước bất kỳ tối ưu nào: **đo**. Trong .NET nghĩa là `Stopwatch` (hoặc profiler
thật). Trực giác về "code chậm" sai liên tục; vòng lặp trông đắt có thể miễn
phí, và một call vô tội có thể chi phối mọi thứ. Quy tắc của module này và về
sau:

1. Đo hình dạng hiện tại (`Stopwatch` tối thiểu).
2. Thay đổi MỘT thứ.
3. Đo lại; chỉ giữ thắng lợi thật.

Mọi thứ dưới đây là các hình dạng có chi phí *dự đoán được từ chính code* —
những chỗ đáng sửa ngay — nhưng dù vậy vẫn phải xác nhận bằng số.

## String bất biến — nối chuỗi là O(n²)

Mỗi `+=` trên string cấp phát một string hoàn toàn mới và chép mọi thứ có
trước. Tạo báo cáo 10.000 phần bằng `+=` chép ~50 triệu ký tự.
`StringBuilder` khấu trừ còn O(n) (xem cặp ví dụ trước/sau trong bản tiếng
Anh).

Vài phép `+=` trên chuỗi ngắn là ổn. Vấn đề nằm ở *vòng lặp không biên*.

## Chọn collection là thắng lợi lớn rẻ nhất

Kiểu truy cập quyết định loại — theo độ phức tạp, không theo mốt: lookup theo
khóa dùng `Dictionary<K,V>` (~O(1)); kiểm tra tồn tại dùng `HashSet<T>`
(~O(1)); truy cập theo chỉ số / quét có thứ tự dùng `List<T>`/`T[]`; FIFO dùng
`Queue<T>`; LIFO dùng `Stack<T>` (bảng đầy đủ trong bản tiếng Anh).

Ẩn số kinh điển: trong vòng lặp N phần tử, gọi `list.Contains(x)` (hay
`Remove`) — O(n) mỗi lần — biến tổng thể thành O(n²). Một `HashSet` biến phép
kiểm tra trong thành ~O(1) và cả vòng thành O(n).

## Một thói quen allocation nữa

`List<T>` tăng trưởng bằng cách nhân đôi — ổn. Nhưng nếu biết trước kích
thước cuối, constructor `new List<T>(capacity)` tránh hẳn việc cấp phát lại.
Chỉ dành cho khối lượng lớn đã biết kích thước; tinh chỉnh list nhỏ là nhiễu.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "linq-cost",
    "LINQ Cost: Deferred Pipelines, Multiple Enumeration, Materialization",
    "Every LINQ stage is a lazy view, not a result — which is a feature until a pipeline is enumerated twice, recomputed twice, or built per-iteration inside a hot loop.",
    22,
    r"""
## Deferred by default

`Where`, `Select`, `Take`... return a *view* over the source. No work happens
until something enumerates (`foreach`, `ToList`, `Count`, `First`...). Two
consequences matter for performance:

**Multiple enumeration.** Every enumeration re-runs the whole pipeline —
and re-runs the *source*:

```csharp
var query = orders.Where(o => o.Total > 100);   // nothing runs yet
if (query.Count() > 0)          // enumerates: filter runs once
    Render(query);              // enumerates AGAIN: filter runs twice
```

If the pipeline is consumed more than once, materialize once:
`var list = query.ToList();`. If it is consumed exactly once, adding
`ToList()` only spends an allocation for nothing.

**Enumeration is not free per-element either.** A pipeline of three stages
does three delegate calls per element. For most app code this is irrelevant;
inside a hot loop over millions of items it can show up. The fix is not
"ditch LINQ" — it is "don't build pipelines in loops":

```csharp
// pipeline rebuilt (and re-run) per iteration
foreach (var o in orders)
    if (orders.Where(x => x.Id > o.Id).Any()) ...   // O(n^2)

// compute the view once, then use it
var later = orders.Where(x => x.Id > threshold).ToList();
```

## Materialization choices

- `ToList()` / `ToArray()` — snapshot; needed for repeated use or when the
  source mutates later.
- `Count()` on a pipeline — enumerates the whole thing; `Count` property on
  a `List` is free. Knowing which you're touching matters.
- `First` vs `FirstOrDefault` vs `Single` — same laziness, different
  expectations; `Single` may scan past the match to prove uniqueness.

## The performance review lens

Reading someone's code for cost, the checklist that catches 90%:

1. Any string `+=` inside a loop? → `StringBuilder`.
2. Any `Contains`/`Remove` on a list inside a loop? → `HashSet`/`Dictionary`.
3. Any LINQ pipeline enumerated more than once? → materialize once.
4. Any query built *inside* another loop? → hoist and run once.
5. And above all: was any of it measured before being called slow?
""",
    "Chi phí LINQ: Pipeline Trễ, Enumeration Nhiều Lần, Materialization",
    "Mỗi stage LINQ là một view lười, không phải kết quả — là một tính năng cho đến khi pipeline bị enumerate hai lần, tính lại hai lần, hay dựng mỗi vòng trong loop nóng.",
    r"""
## Trễ theo mặc định

`Where`, `Select`, `Take`... trả về một *view* trên nguồn. Không có công việc
nào xảy ra cho đến khi có thứ gì enumerate (`foreach`, `ToList`, `Count`,
`First`...). Hai hệ quả quan trọng cho hiệu năng:

**Enumeration nhiều lần.** Mỗi lần enumerate chạy lại toàn bộ pipeline — và
chạy lại cả *nguồn* (ví dụ `query.Count()` rồi `Render(query)` trong bản tiếng
Anh: filter chạy hai lần).

Nếu pipeline được tiêu thụ nhiều lần, materialize một lần:
`var list = query.ToList();`. Nếu tiêu thụ đúng một lần, thêm `ToList()` chỉ
tốn một allocation vô ích.

**Từng phần tử cũng không miễn phí.** Pipeline ba stage gọi ba delegate mỗi
phần tử. Với phần lớn app code điều này không đáng kể; trong vòng nóng trên
hàng triệu phần tử nó hiện hình. Cách sửa không phải "bỏ LINQ" — mà là
"đừng dựng pipeline trong vòng lặp" (ví dụ O(n²) trước/sau trong bản tiếng
Anh).

## Lựa chọn materialization

- `ToList()`/`ToArray()` — snapshot; cần khi dùng lặp lại hoặc nguồn sẽ đổi
  sau đó.
- `Count()` trên pipeline — enumerate toàn bộ; property `Count` trên `List`
  miễn phí. Phân biệt bạn đang chạm vào cái nào.
- `First`/`FirstOrDefault`/`Single` — cùng độ trễ, kỳ vọng khác nhau;
  `Single` có thể quét tiếp sau match để chứng minh tính duy nhất.

## Đôi mắt review hiệu năng

Đọc code người khác theo chi phí, checklist bắt được 90%:

1. Có `+=` string trong vòng lặp? → `StringBuilder`.
2. Có `Contains`/`Remove` trên list trong vòng lặp? → `HashSet`/`Dictionary`.
3. Có pipeline LINQ bị enumerate nhiều hơn một lần? → materialize một lần.
4. Có query được dựng *bên trong* vòng lặp khác? → kéo lên, chạy một lần.
5. Và trên hết: có thứ gì được đo trước khi bị gắn nhãn chậm?
""",
)

# ---------------------------------------------------------------- practice
COUNTING_STRINGS = (
    "\n"
    "// Provided infrastructure — do not modify. A string-op counter wired into\n"
    "// the workload helpers: Concat loops through solution code still count.\n"
    "public static class StringOps\n"
    "{\n"
    "    public static int Allocations { get; private set; }\n"
    "    public static void Reset() => Allocations = 0;\n"
    "    public static void Bump() => Allocations++;\n"
    "}\n"
)
COUNT_PROBE = (
    "\n"
    "// Provided infrastructure — do not modify. Counts source enumerations:\n"
    "// each foreach pass over Src() bumps Hits exactly once.\n"
    "public sealed class CountingProbe\n"
    "{\n"
    "    public int Hits;\n"
    "    public System.Collections.Generic.IEnumerable<int> Src(params int[] xs)\n"
    "    {\n"
    "        Hits++;\n"
    "        foreach (var x in xs) yield return x;\n"
    "    }\n"
    "}\n"
)

SCAN_PROBE = (
    "\n"
    "// Provided infrastructure — do not modify. Counts enumerations of Src():\n"
    "// each pass bumps Scans exactly once. HashSet lookups never enumerate.\n"
    "public static class ScanProbe\n"
    "{\n"
    "    public static int Scans;\n"
    "    public static System.Collections.Generic.IEnumerable<string> Src(params string[] xs)\n"
    "    {\n"
    "        Scans++;\n"
    "        foreach (var x in xs) yield return x;\n"
    "    }\n"
    "}\n"
)

write_practice(
    M,
    "csi-p20-performance",
    "Performance Practice: Build, Pick, Materialize",
    "Rebuild an O(n²) report builder, replace a linear membership test with a set, fix a pipeline that runs its filter twice, and debug a lookup that re-queries per call.",
    "Luyện Hiệu năng: Dựng, Chọn, Materialize",
    "Dựng lại bộ tạo báo cáo O(n²), thay phép kiểm tra tuyến tính bằng set, sửa pipeline chạy filter hai lần, và debug một lookup truy vấn lại mỗi lần gọi.",
    "linq-cost",
    30,
    "intermediate",
    [
        challenge(
            "csi-p20-stringbuilder",
            "StringBuilder, Not Concatenation",
            r"""`ConcatReport` builds one big string with `+=` inside the loop —
the quadratic shape. Rewrite it as `Solution.Report(string[] lines)` using a
`System.Text.StringBuilder` so the loop allocates no intermediate strings:

- one line per input, each terminated with `'\n'` (so `lines = ["a","b"]`
  produces `"a\nb\n"`),
- empty input produces `""`,
- and `StringOps.Allocations` must stay at 0 across the whole call (the
  counting helper is provided; call `StringOps.Bump()` never).

```csharp
public static class Solution
{
    public static string Report(string[] lines);   // one line per input, '\n'-terminated
}
// provided: public static class StringOps { int Allocations; Reset(); Bump(); }
```""",
            CS_PRELUDE + COUNTING_STRINGS,
            [
                (
                    "output shape is exact",
                    r"""
var outp = Solution.Report(new[] { "a", "b", "c" });
Cj.Eq(outp, "a\nb\nc\n", "each line terminated");
Cj.Eq(Solution.Report(new string[] { }), "", "empty in, empty out");
""",
                    "Append each line + '\n'; empty input appends nothing.",
                ),
                (
                    "no intermediate string allocations",
                    r"""
StringOps.Reset();
var s = Solution.Report(new[] { "x", "y", "z" });
Cj.Eq(StringOps.Allocations, 0, "the loop must not build intermediate strings");
Cj.Eq(s, "x\ny\nz\n", "output unchanged");
""",
                    "StringBuilder holds the buffer; one ToString at the end (which the harness does not count).",
                ),
                (
                    "long input finishes",
                    r"""
StringOps.Reset();
var lines = new string[500];
for (int i = 0; i < 500; i++) lines[i] = "line-" + i;
Cj.Eq(Solution.Report(lines).Length, 500 * 10, "6 chars + newline per line");
""",
                    "500 lines of 'line-NNN' (7 chars) + '\n' = 8 per line, 4000 total — prove the loop is linear by surviving it.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p20-set-membership",
            "HashSet Against the Quadratic",
            r"""`DuplicateFinder.HasAny(List<int>, List<int>)` scans the whole
`List` per candidate — O(n·m). Rewrite as
`Solution.HasAny(IEnumerable<int> haystack, List<int> needles)` that puts the
haystack in a `System.Collections.Generic.HashSet<int>` once (one enumeration)
and tests each needle in ~O(1):

- true iff at least one needle is present,
- empty needles → false, empty haystack → false,
- duplicates in either side are irrelevant.

```csharp
public static class Solution
{
    public static bool HasAny(
        System.Collections.Generic.IEnumerable<int> haystack,
        System.Collections.Generic.List<int> needles);
}
// provided: public sealed class CountingProbe { public int Hits; public IEnumerable<int> Src(params int[] xs); }
```""",
            CS_PRELUDE + COUNT_PROBE,
            [
                (
                    "membership semantics",
                    r"""
var probe = new CountingProbe();
var hay = probe.Src(1, 2, 3);
Cj.True(Solution.HasAny(hay, new System.Collections.Generic.List<int> { 9, 2 }), "2 is present");
Cj.Eq(probe.Hits, 1, "haystack enumerated once, not per needle");
Cj.False(Solution.HasAny(hay, new System.Collections.Generic.List<int> { 9, 10 }), "none present");
""",
                    "Build the set once, test each needle against it.",
                ),
                (
                    "degenerate inputs",
                    r"""
var hay = new System.Collections.Generic.List<int> { 1 };
var empty = new System.Collections.Generic.List<int>();
Cj.False(Solution.HasAny(hay, empty), "no needles -> false");
Cj.False(Solution.HasAny(empty, hay), "no haystack -> false");
""",
                    "Empty side means no match can exist.",
                ),
                (
                    "duplicates do not matter",
                    r"""
var hay = new System.Collections.Generic.List<int> { 5, 5, 5 };
Cj.True(Solution.HasAny(hay, new System.Collections.Generic.List<int> { 5, 5 }), "dup on both sides still matches");
""",
                    "A set collapses duplicates; presence is all that counts.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p20-materialize",
            "Enumerate Once",
            r"""`FilterTwice` enumerates its pipeline two times (a `Count()` gate,
then the render loop) — the filter (and the source!) runs twice. Write
`Solution.Heavy(IEnumerable<int> source)` that:

- filters to even numbers (in order),
- enumerates the pipeline **exactly once** in total,
- returns the count and the joined values in one object:

```csharp
public static class Solution
{
    public sealed class Stats { public int Count; public string Joined = ""; }
    public static Stats Heavy(System.Collections.Generic.IEnumerable<int> source);   // e.g. [1,2,3,4] -> Count=2, Joined="2|4"
}
```

CountingProbe (provided) records how many times a source is enumerated: wrap
it via `probe.Src()` so the tests can see the true enumeration count.

```csharp
// provided: public sealed class CountingProbe { public int Hits; public IEnumerable<int> Src(params int[] xs); }
```""",
            CS_PRELUDE + COUNT_PROBE,
            [
                (
                    "values and counts are right",
                    r"""
var st = Solution.Heavy(new[] { 1, 2, 3, 4, 5, 6 });
Cj.Eq(st.Count, 3, "three evens");
Cj.Eq(st.Joined, "2|4|6", "in order");
""",
                    "Filter to evens; count and join from one materialized snapshot.",
                ),
                (
                    "the source is enumerated exactly once",
                    r"""
var probe = new CountingProbe();
var st = Solution.Heavy(probe.Src(1, 2, 3, 4));
Cj.Eq(st.Joined, "2|4", "still correct");
Cj.Eq(probe.Hits, 1, "one enumeration, not two");
""",
                    "Materialize once (ToList), then derive Count and Joined from the snapshot.",
                ),
                (
                    "no match is also one pass",
                    r"""
var probe = new CountingProbe();
var st = Solution.Heavy(probe.Src(1, 3, 5));
Cj.Eq(st.Count, 0, "no evens");
Cj.Eq(st.Joined, "", "nothing joined");
Cj.Eq(probe.Hits, 1, "empty result still costs one pass");
""",
                    "Even the empty outcome must come from a single enumeration.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p20-hotloop-debug",
            "Debug: The Query in the Loop",
            r"""A price checker "works" but re-runs a whole LINQ query *inside* the
per-item loop, and its cache check uses `List.Contains` on top. For 1 item it
is invisible; for a catalog it is quadratic. The broken shape:

```csharp
public static string Check(List<string> catalog, string sku)   // BROKEN
{
    if (catalog.Contains(sku)) return "known";
    var cheap = catalog.Where(s => s.Length < 4).Count();      // query per call!
    return cheap > 0 ? "cheap-others" : "unknown";
}
```

Write `Solution.BuildChecker(IEnumerable<string> catalog)` returning a delegate
`Func<string, string>` with the same contract ("known" / "cheap-others" /
"unknown") but with ALL expensive work done once at build time:

- membership via a prebuilt `HashSet`,
- the cheap-count computed once at build,
- the returned delegate does no LINQ and no list scans.

```csharp
public static class Solution
{
    public static System.Func<string, string> BuildChecker(System.Collections.Generic.IEnumerable<string> catalog);
}
// provided: public static class ScanProbe { public static int Scans; public static IEnumerable<string> Src(params string[] xs); }
```""",
            CS_PRELUDE + SCAN_PROBE,
            [
                (
                    "same answers, new shape",
                    r"""
var check = Solution.BuildChecker(ScanProbe.Src("ab", "cde", "xyz"));
Cj.Eq(check("ab"), "known", "member");
Cj.Eq(check("cde"), "known", "member regardless of length");
Cj.Eq(check("qq"), "cheap-others", "not known, but cheap others exist");
""",
                    "Prebuild the set and the count; the delegate just branches.",
                ),
                (
                    "no cheap others -> unknown",
                    r"""
var check = Solution.BuildChecker(ScanProbe.Src("abcd", "efgh"));
Cj.Eq(check("zz"), "unknown", "no cheap others");
Cj.Eq(check("abcd"), "known", "membership still works");
""",
                    "The build-time count decides the fallback branch.",
                ),
                (
                    "delegate does no per-call scanning",
                    r"""
var check = Solution.BuildChecker(ScanProbe.Src("a", "bc"));
int afterBuild = ScanProbe.Scans;
Cj.Eq(check("a"), "known", "sanity");
Cj.Eq(check("zz"), "cheap-others", "fallback branch is also cheap");
Cj.Eq(ScanProbe.Scans, afterBuild, "no scan inside the delegate");
""",
                    "Snapshot Scans after building; the returned delegate must add zero.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p20-stringbuilder": vi_challenge(
            "StringBuilder, không phải nối chuỗi",
            "`ConcatReport` dựng một string lớn bằng `+=` trong vòng lặp — hình dạng bình phương. Viết lại thành `Solution.Report(string[] lines)` dùng `System.Text.StringBuilder` để vòng lặp không cấp phát string trung gian: mỗi dòng một dòng đầu vào, kết thúc bằng `\\n` (`[\"a\",\"b\"]` -> `\"a\\nb\\n\"`); input rỗng -> `\"\"`; `StringOps.Allocations` phải bằng 0 suốt lần gọi (helper đếm được cấp sẵn).",
            [
                ("output shape is exact", "Append từng dòng + '\\n'; input rỗng không append gì."),
                ("no intermediate string allocations", "StringBuilder giữ buffer; chỉ một ToString cuối (harness không đếm)."),
                ("long input finishes", "500 dòng 'line-NNN' (7 ký tự) + '\\n' = 8 mỗi dòng, tổng 4000 — chứng minh vòng lặp tuyến tính bằng cách sống sót qua nó."),
            ],
        ),
        "csi-p20-set-membership": vi_challenge(
            "HashSet chống bình phương hóa",
            "`DuplicateFinder.HasAny(List<int>, List<int>)` quét toàn bộ `List` cho mỗi phần tử cần tìm — O(n·m). Viết `Solution.HasAny(IEnumerable<int> haystack, List<int> needles)` đưa haystack vào một `System.Collections.Generic.HashSet<int>` một lần rồi kiểm từng needle trong ~O(1): true khi có ít nhất một needle; needles rỗng -> false; haystack rỗng -> false; trùng lặp ở hai bên không quan trọng.",
            [
                ("membership semantics", "Dựng set một lần, kiểm từng needle trên set đó."),
                ("degenerate inputs", "Bên rỗng nghĩa là không thể có match."),
                ("duplicates do not matter", "Set gộp trùng lặp; sự hiện diện là tất cả."),
            ],
        ),
        "csi-p20-materialize": vi_challenge(
            "Enumerate một lần",
            "`FilterTwice` enumerate pipeline của nó hai lần (cổng `Count()`, rồi vòng render) — filter (và cả nguồn!) chạy hai lần. Viết `Solution.Heavy(IEnumerable<int> source)`: lọc số chẵn (giữ thứ tự), enumerate pipeline **đúng một lần**, trả `Stats { int Count; string Joined }` — ví dụ [1,2,3,4] -> Count=2, Joined=\"2|4\". CountingProbe (cấp sẵn) ghi nhận nguồn bị enumerate bao nhiêu lần: bọc nguồn qua `probe.Src()` để test thấy số lần thật.",
            [
                ("values and counts are right", "Lọc số chẵn; đếm và join từ một snapshot đã materialize."),
                ("the source is enumerated exactly once", "Materialize một lần (ToList), rồi lấy Count và Joined từ snapshot."),
                ("no match is also one pass", "Kể cả kết quả rỗng cũng phải đến từ đúng một lượt enumerate."),
            ],
        ),
        "csi-p20-hotloop-debug": vi_challenge(
            "Debug: Query trong vòng lặp",
            "Một bộ kiểm tra giá \"chạy được\" nhưng chạy lại cả query LINQ *bên trong* vòng lặp từng phần tử, trên nền `List.Contains`. Với 1 phần tử thì vô hình; với catalog thì bình phương hóa. Viết `Solution.BuildChecker(IEnumerable<string> catalog)` trả delegate `Func<string, string>` cùng hợp đồng (\"known\"/\"cheap-others\"/\"unknown\") nhưng MỌI công việc đắt làm một lần lúc dựng: membership qua `HashSet` dựng sẵn, số lượng cheap đếm một lần lúc dựng, delegate trả về không dùng LINQ và không quét list.",
            [
                ("same answers, new shape", "Dựng sẵn set và count; delegate chỉ rẽ nhánh."),
                ("no cheap others -> unknown", "Số lượng đếm lúc dựng quyết định nhánh fallback."),
                ("delegate does no per-call scanning", "ScanProbe (cấp sẵn) đếm phép quét list: HashSet dựng sẵn không quét."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p20-stringbuilder",
            'public static class Solution\n{\n    public static string Report(string[] lines)\n    {\n        var sb = new System.Text.StringBuilder();\n        foreach (var line in lines)\n        {\n            sb.Append(line);\n            sb.Append(\'\\n\');\n        }\n        return sb.ToString();\n    }\n}\n',
            'public static class Solution\n{\n    public static string Report(string[] lines)\n    {\n        var s = "";\n        // near-miss: still allocates per iteration — builds via += but\n        // wraps it so it *looks* like a builder\n        var sb = new System.Text.StringBuilder();\n        foreach (var line in lines)\n        {\n            s += line + "\\n";\n            sb.Append(s[s.Length - 1]);   // fake "use" of the builder\n        }\n        StringOps.Bump();\n        return s;\n    }\n}\n',
        ),
        (
            "csi-p20-set-membership",
            'public static class Solution\n{\n    public static bool HasAny(\n        System.Collections.Generic.IEnumerable<int> haystack,\n        System.Collections.Generic.List<int> needles)\n    {\n        var set = new System.Collections.Generic.HashSet<int>(haystack);\n        foreach (var n in needles)\n            if (set.Contains(n)) return true;\n        return false;\n    }\n}\n',
            'public static class Solution\n{\n    public static bool HasAny(\n        System.Collections.Generic.IEnumerable<int> haystack,\n        System.Collections.Generic.List<int> needles)\n    {\n        // near-miss: builds the set but still scans the LIST per needle —\n        // the set exists, the quadratic shape does too\n        var set = new System.Collections.Generic.HashSet<int>(haystack);\n        foreach (var n in needles)\n            foreach (var h in haystack)\n                if (h == n && set.Contains(n)) return true;\n        return false;\n    }\n}\n',
        ),
        (
            "csi-p20-materialize",
            'public static class Solution\n{\n    public sealed class Stats { public int Count; public string Joined = ""; }\n\n    public static Stats Heavy(System.Collections.Generic.IEnumerable<int> source)\n    {\n        var snapshot = new System.Collections.Generic.List<int>();\n        foreach (var x in source)\n            if (x % 2 == 0) snapshot.Add(x);\n\n        var joined = new System.Text.StringBuilder();\n        for (int i = 0; i < snapshot.Count; i++)\n        {\n            if (i > 0) joined.Append(\'|\');\n            joined.Append(snapshot[i]);\n        }\n        return new Stats { Count = snapshot.Count, Joined = joined.ToString() };\n    }\n}\n',
            'public static class Solution\n{\n    public sealed class Stats { public int Count; public string Joined = ""; }\n\n    public static Stats Heavy(System.Collections.Generic.IEnumerable<int> source)\n    {\n        // near-miss: two separate enumerations of the source — count first,\n        // then join. Same answers, wrong shape.\n        int count = 0;\n        foreach (var x in source) if (x % 2 == 0) count++;\n\n        var joined = new System.Text.StringBuilder();\n        bool first = true;\n        foreach (var x in source)\n            if (x % 2 == 0)\n            {\n                if (!first) joined.Append(\'|\');\n                first = false;\n                joined.Append(x);\n            }\n        return new Stats { Count = count, Joined = joined.ToString() };\n    }\n}\n',
        ),
        (
            "csi-p20-hotloop-debug",
            'public static class Solution\n{\n    public static System.Func<string, string> BuildChecker(\n        System.Collections.Generic.IEnumerable<string> catalog)\n    {\n        var known = new System.Collections.Generic.HashSet<string>(catalog);\n        int cheap = 0;\n        foreach (var s in catalog)\n            if (s.Length < 4) cheap++;\n\n        return sku =>\n        {\n            if (known.Contains(sku)) return "known";\n            return cheap > 0 ? "cheap-others" : "unknown";\n        };\n    }\n}\n',
            'public static class Solution\n{\n    public static System.Func<string, string> BuildChecker(\n        System.Collections.Generic.IEnumerable<string> catalog)\n    {\n        var known = new System.Collections.Generic.HashSet<string>(catalog);\n\n        return sku =>\n        {\n            if (known.Contains(sku)) return "known";\n            // near-miss: the "expensive" count is still recomputed per call —\n            // the loop moved out of sight, not out of the hot path\n            int cheap = 0;\n            foreach (var s in catalog)\n                if (s.Length < 4) cheap++;\n            return cheap > 0 ? "cheap-others" : "unknown";\n        };\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m20",
    "Checkpoint — The Profiled Pipeline",
    "Compose the module: batch a repeated lookup out of a loop, materialize a twice-run pipeline once, and prove the cheap path stays cheap — all through counting fakes.",
    28,
    r"""
## The gate (mini-build)

A tiny analytics service, cost-graded:

1. `PriceBook` — built once from `int[] prices` (sku i costs `prices[i]`).
   Exposes `Total(int[] skus)` — sum via a prebuilt array, **no LINQ, no
   allocations** per call — and `LookupCount` recording how many single-sku
   lookups callers performed through `Lookup(int sku)`.
2. `TopSkus(int[] skus, int take)` — distinct skus by descending frequency,
   ties broken by smaller sku first, at most `take` results.
3. `Summary(int[] skus)` — built on `TopSkus`' materialized snapshot (one
   pass over the data), returning `"{count}:{joined}"` where count is the
   number of distinct skus and joined is comma-joined sku list.

```csharp
public static class Solution
{
    public sealed class PriceBook
    {
        public PriceBook(int[] prices);
        public int Total(int[] skus);        // no LINQ / no allocs per call
        public int LookupCount { get; }
        public int Lookup(int sku);          // counted single-sku access
    }
    public static int[] TopSkus(int[] skus, int take);
    public static string Summary(int[] skus);
}
```""",
    "Checkpoint — Pipeline Được Đo",
    "Ghép cả module: đưa lookup lặp ra khỏi vòng lặp bằng batch, materialize một pipeline chạy hai lần thành một lần, và chứng minh đường rẻ vẫn rẻ — tất cả qua fake đếm.",
    r"""
## Cổng kiểm tra (mini-build)

Một dịch vụ phân tích tí hon, chấm theo chi phí:

1. `PriceBook` — dựng một lần từ `int[] prices` (sku i giá `prices[i]`).
   Cung cấp `Total(int[] skus)` — tổng qua mảng dựng sẵn, **không LINQ,
   không allocation** mỗi lần gọi — và `LookupCount` ghi nhận số lần caller
   tra một sku qua `Lookup(int sku)`.
2. `TopSkus(int[] skus, int take)` — các sku distinct theo tần suất giảm dần,
   hòa thì sku nhỏ hơn trước, tối đa `take` kết quả.
3. `Summary(int[] skus)` — dựng trên snapshot đã materialize của `TopSkus`
   (một lượt trên dữ liệu), trả `"{count}:{joined}"` với count là số sku
   distinct và joined là danh sách sku nối bằng dấu phẩy.

Xem chữ ký `Solution` trong bản tiếng Anh.
""",
    challenge(
        "csi-checkpoint-m20-task",
        "Build the Profiled Pipeline",
        "Implement PriceBook (prebuilt totals, counted lookups), TopSkus (frequency, deterministic ties), and Summary (single materialized pass).",
        CS_PRELUDE,
        [
            (
                "book totals without per-call work",
                r"""
var book = new Solution.PriceBook(new[] { 10, 20, 30 });
Cj.Eq(book.Total(new[] { 0, 2, 0 }), 50, "10+30+10");
Cj.Eq(book.LookupCount, 0, "Total must not use single-sku lookups");
""",
                "Total sums from the prebuilt array; LookupCount stays at zero.",
            ),
            (
                "top skus with deterministic ties",
                r"""
var top = Solution.TopSkus(new[] { 3, 3, 1, 1, 2, 2, 2, 5 }, 3);
Cj.Eq(string.Join("|", top), "2|1|3", "freq desc, ties by smaller sku");
""",
                "Count frequencies, order by count desc then sku asc, take 3.",
            ),
            (
                "summary from one pass",
                r"""
Cj.Eq(Solution.Summary(new[] { 3, 3, 1, 2 }), "3:3,1,2", "distinct count + comma list");
""",
                "Summary reuses the materialized distinct list, joined with commas.",
            ),
            (
                "lookups are counted",
                r"""
var book = new Solution.PriceBook(new[] { 5, 6 });
Cj.Eq(book.Lookup(1), 6, "sku 1 -> price 6");
Cj.Eq(book.Lookup(1), 6, "again");
Cj.Eq(book.LookupCount, 2, "each single-sku access counted");
""",
                "Lookup increments LookupCount every call.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: Dựng Pipeline Được Đo",
        "Hiện thực PriceBook (tổng dựng sẵn, lookup được đếm), TopSkus (tần suất, hòa xác định), và Summary (một lượt materialize).",
        [
            ("book totals without per-call work", "Total cộng từ mảng dựng sẵn; LookupCount giữ ở 0."),
            ("top skus with deterministic ties", "Đếm tần suất, sắp theo count giảm rồi sku tăng, lấy 3."),
            ("summary from one pass", "Summary tái sử dụng danh sách distinct đã materialize, nối bằng dấu phẩy."),
            ("lookups are counted", "Lookup tăng LookupCount mỗi lần gọi."),
        ],
    ),
    solution='public static class Solution\n{\n    public sealed class PriceBook\n    {\n        private readonly int[] _prices;\n        public int LookupCount { get; private set; }\n\n        public PriceBook(int[] prices) => _prices = (int[])prices.Clone();\n\n        public int Total(int[] skus)\n        {\n            int t = 0;\n            foreach (var s in skus) t += _prices[s];\n            return t;\n        }\n\n        public int Lookup(int sku)\n        {\n            LookupCount++;\n            return _prices[sku];\n        }\n    }\n\n    public static int[] TopSkus(int[] skus, int take)\n    {\n        var freq = new System.Collections.Generic.Dictionary<int, int>();\n        foreach (var s in skus)\n            freq[s] = freq.TryGetValue(s, out var c) ? c + 1 : 1;\n\n        var ordered = new System.Collections.Generic.List<int>(freq.Keys);\n        ordered.Sort((a, b) =>\n        {\n            int byFreq = freq[b].CompareTo(freq[a]);\n            return byFreq != 0 ? byFreq : a.CompareTo(b);\n        });\n\n        int n = ordered.Count < take ? ordered.Count : take;\n        var outp = new int[n];\n        for (int i = 0; i < n; i++) outp[i] = ordered[i];\n        return outp;\n    }\n\n    public static string Summary(int[] skus)\n    {\n        var top = TopSkus(skus, skus.Length);\n        var joined = new System.Text.StringBuilder();\n        for (int i = 0; i < top.Length; i++)\n        {\n            if (i > 0) joined.Append(\',\');\n            joined.Append(top[i]);\n        }\n        return top.Length + ":" + joined;\n    }\n}\n',
    wrong='public static class Solution\n{\n    public sealed class PriceBook\n    {\n        private readonly int[] _prices;\n        public int LookupCount { get; private set; }\n\n        public PriceBook(int[] prices) => _prices = (int[])prices.Clone();\n\n        public int Total(int[] skus)\n        {\n            // near-miss: "Total" implemented as N counted single-sku lookups —\n            // the per-call cost the whole module exists to remove\n            int t = 0;\n            foreach (var s in skus) t += Lookup(s);\n            return t;\n        }\n\n        public int Lookup(int sku)\n        {\n            LookupCount++;\n            return _prices[sku];\n        }\n    }\n\n    public static int[] TopSkus(int[] skus, int take)\n    {\n        var freq = new System.Collections.Generic.Dictionary<int, int>();\n        foreach (var s in skus)\n            freq[s] = freq.TryGetValue(s, out var c) ? c + 1 : 1;\n\n        var ordered = new System.Collections.Generic.List<int>(freq.Keys);\n        ordered.Sort((a, b) =>\n        {\n            int byFreq = freq[b].CompareTo(freq[a]);\n            return byFreq != 0 ? byFreq : a.CompareTo(b);\n        });\n\n        int n = ordered.Count < take ? ordered.Count : take;\n        var outp = new int[n];\n        for (int i = 0; i < n; i++) outp[i] = ordered[i];\n        return outp;\n    }\n\n    public static string Summary(int[] skus)\n    {\n        var top = TopSkus(skus, skus.Length);\n        var joined = new System.Text.StringBuilder();\n        for (int i = 0; i < top.Length; i++)\n        {\n            if (i > 0) joined.Append(\',\');\n            joined.Append(top[i]);\n        }\n        return top.Length + ":" + joined;\n    }\n}\n',
    ),

print("module 20 authored")
