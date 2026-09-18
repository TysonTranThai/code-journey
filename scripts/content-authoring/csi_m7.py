#!/usr/bin/env python3
"""C# — Intermediate — Module 7: csi-iterators.

Iterators & pipelines: yield return/break, deferred execution, iterator state
machines, pipeline composition, memory implications.
Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-iterators"

write_module(
    M,
    "Iterators & Lazy Pipelines",
    "yield as a state machine, deferred execution you can observe, and pipelines that touch data once.",
    "Iterator & Pipeline Lười",
    "yield như một máy trạng thái, thực thi trì hoãn có thể quan sát, và pipeline chạm dữ liệu đúng một lần.",
    ["yield-semantics", "lazy-pipelines", "csi-checkpoint-m7"],
    ["csi-p7-iterators"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "yield-semantics",
    "yield: The Compiler Writes Your State Machine",
    "What yield return compiles into, yield break, and the observable facts of deferred execution.",
    16,
    r"""
## An iterator method is rewritten, not called

Mark a method `IEnumerable<T>` with `yield return` and the compiler generates
a state-machine class: each `yield return` is a pause point, each MoveNext a
resume:

```csharp
static IEnumerable<int> Evens(int upto)
{
    for (int i = 0; i <= upto; i += 2)
        yield return i;          // pause: hand one value out, wait
}
```

Nothing runs when `Evens(10)` is CALLED — the method body starts only when
the first `MoveNext` happens (the first `foreach` step). Side effects before
the first yield are equally deferred:

```csharp
static IEnumerable<int> Logged()
{
    Console.WriteLine("start");        // deferred too!
    yield return 1;
    Console.WriteLine("middle");
    yield return 2;
}
```

`yield break` terminates early (an empty iterator is just `yield break`).
Inside iterator methods: no `yield return` inside try-catch (only try-
finally), no `ref`/`out` parameters, single yield path per resume.

## Deferred ≠ cached

Each `foreach` over an iterator RE-RUNS it:

```csharp
var seq = Logged();
foreach (var x in seq) { }   // prints start, middle
foreach (var x in seq) { }   // prints start, middle AGAIN
```

Materialize with `ToList()` when you need one-shot semantics or multiple
passes over expensive work — and expect the tradeoff (memory for time).

## Check your understanding

- When does the code before the first `yield` execute? (On first MoveNext, not at call.)
- Why can't iterator methods take `ref` parameters? (State machines are heap objects; ref locals can't persist across suspensions.)
""",
    "yield: Compiler viết máy trạng thái thay bạn",
    "yield return biên dịch thành gì, yield break, và các sự thật quan sát được của thực thi trì hoãn.",
    r"""
## Phương thức iterator được viết lại, không được gọi

Đánh dấu phương thức `IEnumerable<T>` với `yield return` và compiler sinh một
lớp máy-trạng-thái: mỗi `yield return` là một điểm dừng, mỗi MoveNext là một
lần tiếp diễn:

```csharp
static IEnumerable<int> Evens(int upto)
{
    for (int i = 0; i <= upto; i += 2)
        yield return i;          // dừng: đưa một giá trị ra, chờ
}
```

Không gì chạy khi `Evens(10)` được GỌI — thân phương thức chỉ bắt đầu khi
MoveNext đầu tiên xảy ra (bước foreach đầu tiên). Tác dụng phụ trước yield
đầu tiên cũng bị trì hoãn:

```csharp
static IEnumerable<int> Logged()
{
    Console.WriteLine("start");        // cũng bị trì hoãn!
    yield return 1;
    Console.WriteLine("middle");
    yield return 2;
}
```

`yield break` kết thúc sớm (một iterator rỗng chỉ là `yield break`). Bên trong
phương thức iterator: không `yield return` trong try-catch (chỉ try-finally),
không tham số `ref`/`out`, một đường yield cho mỗi lần tiếp diễn.

## Trì hoãn ≠ được cache

Mỗi `foreach` trên một iterator CHẠY LẠI nó:

```csharp
var seq = Logged();
foreach (var x in seq) { }   // in start, middle
foreach (var x in seq) { }   // in start, middle LẦN NỮA
```

Hóa rắn bằng `ToList()` khi cần ngữ nghĩa một-lần hoặc nhiều lượt qua công
việc đắt — và chấp nhận đánh đổi (bộ nhớ lấy thời gian).

## Kiểm tra hiểu biết

- Code trước `yield` đầu tiên chạy khi nào? (Ở MoveNext đầu tiên, không phải lúc gọi.)
- Vì sao phương thức iterator không nhận được tham số `ref`? (Máy trạng thái là đối tượng heap; ref local không thể tồn tại qua các lần đình chỉ.)
""",
    r"""
## Phương thức iterator được viết lại, không được gọi

Đánh dấu phương thức `IEnumerable<T>` với `yield return` và compiler sinh một
lớp máy-trạng-thái: mỗi `yield return` là một điểm dừng, mỗi MoveNext là một
lần tiếp diễn:

```csharp
static IEnumerable<int> Evens(int upto)
{
    for (int i = 0; i <= upto; i += 2)
        yield return i;          // dừng: đưa một giá trị ra, chờ
}
```

Không gì chạy khi `Evens(10)` được GỌI — thân phương thức chỉ bắt đầu khi
MoveNext đầu tiên xảy ra (bước foreach đầu tiên). Tác dụng phụ trước yield
đầu tiên cũng bị trì hoãn:

```csharp
static IEnumerable<int> Logged()
{
    Console.WriteLine("start");        // cũng bị trì hoãn!
    yield return 1;
    Console.WriteLine("middle");
    yield return 2;
}
```

`yield break` kết thúc sớm (một iterator rỗng chỉ là `yield break`). Bên trong
phương thức iterator: không `yield return` trong try-catch (chỉ try-finally),
không tham số `ref`/`out`, một đường yield cho mỗi lần tiếp diễn.

## Trì hoãn ≠ được cache

Mỗi `foreach` trên một iterator CHẠY LẠI nó:

```csharp
var seq = Logged();
foreach (var x in seq) { }   // in start, middle
foreach (var x in seq) { }   // in start, middle LẦN NỮA
```

Hóa rắn bằng `ToList()` khi cần ngữ nghĩa một-lần hoặc nhiều lượt qua công
việc đắt — và chấp nhận đánh đổi (bộ nhớ lấy thời gian).

## Kiểm tra hiểu biết

- Code trước `yield` đầu tiên chạy khi nào? (Ở MoveNext đầu tiên, không phải lúc gọi.)
- Vì sao phương thức iterator không nhận được tham số `ref`? (Máy trạng thái là đối tượng heap; ref local không thể tồn tại qua các lần đình chỉ.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "lazy-pipelines",
    "Lazy Pipelines: Touch Data Once",
    "Composing iterators, the one-pass advantage, eager sources vs lazy middles, and bounded generation.",
    15,
    r"""
## Pipelines compose for free

An iterator consuming an IEnumerable is a stage; stages chain into
pipelines where each item flows through all stages before the next item
starts:

```csharp
static IEnumerable<string> ReadLines(string path) { /* yield per line */ }
IEnumerable<string> NonEmpty(IEnumerable<string> src)
{ foreach (var l in src) if (l.Trim().Length > 0) yield return l; }
IEnumerable<int> ParseAll(IEnumerable<string> src)
{ foreach (var l in src) yield return int.Parse(l); }

var total = ParseAll(NonEmpty(ReadLines(path))).Sum();   // one pass, O(1) memory
```

The alternative — three `ToList()` calls — holds three full copies in
memory. For a million-line file that is the difference between constant and
gigabytes.

## Bounded and infinite sources

Iterators can be logically infinite because the consumer controls pace:

```csharp
static IEnumerable<long> Naturals()
{
    for (long i = 0; ; i++) yield return i;
}
var first10 = Naturals().Take(10);     // consumer bounds it
```

`Take`/`Skip`/`TakeWhile` are the consumer-side brakes. This is the shape
behind `IAsyncEnumerable` (Module 9) and every streaming API you will meet.

## The trap: multiple enumeration

A pipeline over a source with side effects (network calls, random, file
reads) re-triggers them per enumeration. If a query runs twice, the source
runs twice — materialize once at the boundary and pass the list onward.

## Check your understanding

- Why is `file.ReadLines` (lazy) usually better than `File.ReadAllLines`? (Constant memory.)
- Where SHOULD you materialize? (At boundaries: once per logical unit of work.)
""",
    "Pipeline Lười: Chạm Dữ Liệu Một Lần",
    "Ghép iterator, lợi thế một-lượt, nguồn eager vs giữa lười, và tạo sinh có chặn.",
    r"""
## Pipeline ghép miễn phí

Một iterator tiêu thụ IEnumerable là một tầng; các tầng xích thành pipeline
nơi từng phần tử chảy qua mọi tầng trước khi phần tử kế tiếp bắt đầu:

```csharp
static IEnumerable<string> ReadLines(string path) { /* yield từng dòng */ }
IEnumerable<string> NonEmpty(IEnumerable<string> src)
{ foreach (var l in src) if (l.Trim().Length > 0) yield return l; }
IEnumerable<int> ParseAll(IEnumerable<string> src)
{ foreach (var l in src) yield return int.Parse(l); }

var total = ParseAll(NonEmpty(ReadLines(path))).Sum();   // một lượt, bộ nhớ O(1)
```

Phương án thay thế — ba lần `ToList()` — giữ ba bản sao đầy đủ trong bộ nhớ.
Với file triệu dòng đó là khác biệt giữa hằng số và hàng gigabyte.

## Nguồn có chặn và nguồn vô hạn

Iterator có thể vô hạn về logic vì người tiêu dùng điều khiển nhịp:

```csharp
static IEnumerable<long> Naturals()
{
    for (long i = 0; ; i++) yield return i;
}
var first10 = Naturals().Take(10);     // người tiêu dùng chặn nó
```

`Take`/`Skip`/`TakeWhile` là phanh phía người tiêu dùng. Đây là hình dạng
đằng sau `IAsyncEnumerable` (Module 9) và mọi API streaming bạn sẽ gặp.

## Cái bẫy: nhiều lần liệt kê

Pipeline trên nguồn có tác dụng phụ (lời gọi mạng, random, đọc file) sẽ
kích hoạt lại chúng theo mỗi lần liệt kê. Query chạy hai lần thì nguồn chạy
hai lần — hóa rắn một lần ở ranh giới và truyền danh sách đi tiếp.

## Kiểm tra hiểu biết

- Vì sao `file.ReadLines` (lười) thường tốt hơn `File.ReadAllLines`? (Bộ nhớ hằng số.)
- Nên hóa rắn Ở ĐÂU? (Ở ranh giới: mỗi đơn vị công việc logic một lần.)
""",
    r"""
## Pipeline ghép miễn phí

Một iterator tiêu thụ IEnumerable là một tầng; các tầng xích thành pipeline
nơi từng phần tử chảy qua mọi tầng trước khi phần tử kế tiếp bắt đầu:

```csharp
static IEnumerable<string> ReadLines(string path) { /* yield từng dòng */ }
IEnumerable<string> NonEmpty(IEnumerable<string> src)
{ foreach (var l in src) if (l.Trim().Length > 0) yield return l; }
IEnumerable<int> ParseAll(IEnumerable<string> src)
{ foreach (var l in src) yield return int.Parse(l); }

var total = ParseAll(NonEmpty(ReadLines(path))).Sum();   // một lượt, bộ nhớ O(1)
```

Phương án thay thế — ba lần `ToList()` — giữ ba bản sao đầy đủ trong bộ nhớ.
Với file triệu dòng đó là khác biệt giữa hằng số và hàng gigabyte.

## Nguồn có chặn và nguồn vô hạn

Iterator có thể vô hạn về logic vì người tiêu dùng điều khiển nhịp:

```csharp
static IEnumerable<long> Naturals()
{
    for (long i = 0; ; i++) yield return i;
}
var first10 = Naturals().Take(10);     // người tiêu dùng chặn nó
```

`Take`/`Skip`/`TakeWhile` là phanh phía người tiêu dùng. Đây là hình dạng
đằng sau `IAsyncEnumerable` (Module 9) và mọi API streaming bạn sẽ gặp.

## Cái bẫy: nhiều lần liệt kê

Pipeline trên nguồn có tác dụng phụ (lời gọi mạng, random, đọc file) sẽ
kích hoạt lại chúng theo mỗi lần liệt kê. Query chạy hai lần thì nguồn chạy
hai lần — hóa rắn một lần ở ranh giới và truyền danh sách đi tiếp.

## Kiểm tra hiểu biết

- Vì sao `file.ReadLines` (lười) thường tốt hơn `File.ReadAllLines`? (Bộ nhớ hằng số.)
- Nên hóa rắn Ở ĐÂU? (Ở ranh giới: mỗi đơn vị công việc logic một lần.)
""",
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m7",
    "Checkpoint — The Data Processing Pipeline",
    "Build a multi-stage lazy pipeline with observable laziness, early termination, and bounded memory behavior.",
    24,
    r"""
## The gate (mini-build)

A text-processing pipeline over a fixed in-memory "log":

1. `ParseLines(IEnumerable<string> lines)` → yields `(int Level, string Msg)`
   for lines shaped `"INFO|started"` / `"WARN|disk"`.
2. `FilterLevel(IEnumerable<(int, string)>, int minLevel)` → yields entries
   with Level >= minLevel.
3. `Format(IEnumerable<(int, string)>)` → yields `"[LVL] msg"` strings.
4. `CountingSource` — a minimal IEnumerable<string> that counts how many
   lines were actually read (its enumerator increments on every MoveNext
   that yields).
5. `Run(IEnumerable<string> lines, int minLevel, int maxResults)` composes
   1→2→3 and returns at most maxResults formatted entries — and stops
   PULLING from the source the moment the cap is reached (observable: a
   CountingSource passed to Run reports how many lines were read; a capped
   run must not drain the source).
""",
    "Checkpoint — Pipeline Xử lý Dữ liệu",
    "Xây pipeline lười nhiều tầng với tính lười quan sát được, kết thúc sớm, và hành vi bộ nhớ có chặn.",
    r"""
## Cổng kiểm tra (mini-build)

Một pipeline xử lý văn bản trên "log" cố định trong bộ nhớ:

1. `ParseLines(IEnumerable<string> lines)` → yield `(int Level, string Msg)`
   cho các dòng dạng `"INFO|started"` / `"WARN|disk"`.
2. `FilterLevel(IEnumerable<(int, string)>, int minLevel)` → yield các mục
   có Level >= minLevel.
3. `Format(IEnumerable<(int, string)>)` → yield chuỗi `"[LVL] msg"`.
4. `Run(string[] lines, int minLevel, int maxResults)` ghép 1→2→3 và trả về
   tối đa maxResults mục đã định dạng — và ngừng KÉO từ nguồn ngay khi chạm
   trần (quan sát được: nguồn chấm đếm số dòng đã đọc; lượt chạy có trần
   không được đọc phần còn lại).
5. `CountingSource` — một IEnumerable<string> tối giản đếm số dòng thực sự
   được đọc (enumerator của nó tăng biến đếm trên mỗi MoveNext có yield).
""",
    challenge(
        "csi-checkpoint-m7-task",
        "Checkpoint: Lazy by Observation",
        """Implement the pipeline described in the checkpoint. Level names: DEBUG=0, INFO=1, WARN=2, ERROR=3.

```csharp
static IEnumerable<(int Level, string Msg)> ParseLines(IEnumerable<string> lines);
static IEnumerable<(int Level, string Msg)> FilterLevel(IEnumerable<(int Level, string Msg)> src, int minLevel);
static IEnumerable<string> Format(IEnumerable<(int Level, string Msg)> src);
public sealed class CountingSource : IEnumerable<string>
{
    public CountingSource(params string[] lines);
    public int ReadCount { get; }        // lines actually pulled by consumers
}
static List<string> Run(IEnumerable<string> lines, int minLevel, int maxResults);
```""",
        CS_PRELUDE,
        [
            (
                "stages compose",
                r"""
string[] lines = { "INFO|started", "DEBUG|noise", "ERROR|disk full", "WARN|slow" };
var outp = Solution.Run(lines, 1, 10);
Cj.Eq(string.Join("|", outp), "[1] started|[3] disk full|[2] slow", "levels >= 1, source order");
""",
                "Split on '|', map names to levels, filter, format — three lazy stages.",
            ),
            (
                "cap stops pulling",
                r"""
var counter = new Solution.CountingSource("INFO|a", "INFO|b", "INFO|c", "INFO|d", "INFO|e");
var capped = Solution.Run(counter, 0, 2);
Cj.Eq(capped.Count, 2, "capped at 2");
Cj.Eq(counter.ReadCount, 2, "source read exactly 2 lines — laziness proven");
""",
                "foreach + a counter; break (or return from inside foreach) the moment the cap hits — no ToList up front.",
            ),
            (
                "cap larger than data",
                r"""
string[] few = { "WARN|only" };
var all = Solution.Run(few, 0, 100);
Cj.Eq(all.Count, 1, "short pipeline fine");
var none = Solution.Run(new string[0], 0, 5);
Cj.Eq(none.Count, 0, "empty input");
""",
                "Empty and short inputs flow through the same lazy path.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: Lười bằng quan sát",
        "Hiện thực pipeline mô tả trong checkpoint: ba tầng lười ghép nhau, và trần kết quả ngừng kéo từ nguồn ngay lập tức — độ lười được chứng minh bằng bộ đếm đọc.",
        [
            ("stages compose", "Tách trên '|', ánh xạ tên sang mức, lọc, định dạng — ba tầng lười."),
            ("cap stops pulling", "foreach + bộ đếm; break (hoặc return ngay trong foreach) ngay khi chạm trần — không ToList trước."),
            ("cap larger than data", "Đầu vào rỗng và ngắn chảy qua cùng đường lười."),
        ],
    ),
    solution='public class Solution\n{\n    public static IEnumerable<(int Level, string Msg)> ParseLines(IEnumerable<string> lines)\n    {\n        foreach (string line in lines)\n        {\n            string[] parts = line.Split(\'|\');\n            int level = parts[0] switch\n            {\n                "DEBUG" => 0,\n                "INFO" => 1,\n                "WARN" => 2,\n                "ERROR" => 3,\n                _ => 0,\n            };\n            yield return (level, parts[1]);\n        }\n    }\n\n    public static IEnumerable<(int Level, string Msg)> FilterLevel(\n        IEnumerable<(int Level, string Msg)> src, int minLevel)\n    {\n        foreach (var entry in src)\n            if (entry.Level >= minLevel) yield return entry;\n    }\n\n    public static IEnumerable<string> Format(IEnumerable<(int Level, string Msg)> src)\n    {\n        foreach (var entry in src)\n            yield return "[" + entry.Level + "] " + entry.Msg;\n    }\n\n    public static List<string> Run(IEnumerable<string> lines, int minLevel, int maxResults)\n    {\n        var output = new List<string>();\n        foreach (string formatted in Format(FilterLevel(ParseLines(lines), minLevel)))\n        {\n            output.Add(formatted);\n            if (output.Count >= maxResults) break;   // stop pulling from the source\n        }\n        return output;\n    }\n\n    public sealed class CountingSource : System.Collections.Generic.IEnumerable<string>\n    {\n        private readonly string[] _lines;\n\n        public CountingSource(params string[] lines) => _lines = lines;\n\n        public int ReadCount { get; private set; }\n\n        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();\n\n        public System.Collections.Generic.IEnumerator<string> GetEnumerator()\n        {\n            foreach (string line in _lines)\n            {\n                ReadCount++;\n                yield return line;\n            }\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public static IEnumerable<(int Level, string Msg)> ParseLines(IEnumerable<string> lines)\n    {\n        foreach (string line in lines)\n        {\n            string[] parts = line.Split(\'|\');\n            int level = parts[0] switch\n            {\n                "DEBUG" => 0,\n                "INFO" => 1,\n                "WARN" => 2,\n                "ERROR" => 3,\n                _ => 0,\n            };\n            yield return (level, parts[1]);\n        }\n    }\n\n    public static IEnumerable<(int Level, string Msg)> FilterLevel(\n        IEnumerable<(int Level, string Msg)> src, int minLevel)\n    {\n        foreach (var entry in src)\n            if (entry.Level >= minLevel) yield return entry;\n    }\n\n    public static IEnumerable<string> Format(IEnumerable<(int Level, string Msg)> src)\n    {\n        foreach (var entry in src)\n            yield return "[" + entry.Level + "] " + entry.Msg;\n    }\n\n    public static List<string> Run(IEnumerable<string> lines, int minLevel, int maxResults)\n    {\n        // near-miss: materializes the WHOLE pipeline before capping — the\n        // source is drained completely, so the laziness test fails\n        var everything = Format(FilterLevel(ParseLines(lines), minLevel)).ToList();\n        return everything.Take(maxResults).ToList();\n    }\n\n    public sealed class CountingSource : System.Collections.Generic.IEnumerable<string>\n    {\n        private readonly string[] _lines;\n\n        public CountingSource(params string[] lines) => _lines = lines;\n\n        public int ReadCount { get; private set; }\n\n        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();\n\n        public System.Collections.Generic.IEnumerator<string> GetEnumerator()\n        {\n            foreach (string line in _lines)\n            {\n                ReadCount++;\n                yield return line;\n            }\n        }\n    }\n}\n',
)
print("module 7 authored")
