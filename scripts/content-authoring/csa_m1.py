"""Module 1 — Advanced language semantics (csa-m1)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-language-semantics",
        "Advanced Language Semantics",
        "Execution model, value vs reference behavior, boxing, null-state, and how the compiler resolves your code.",
    )

    csa.register_lesson(
        MID, "csa-m1-execution-model", "From source to executing IL",
        "Compilation, assemblies, metadata, and the JIT pipeline — what actually happens before your code runs.",
        14, "advanced", _m1_execution_model, _m1_execution_model_vi,
    )
    csa.register_lesson(
        MID, "csa-m1-value-reference", "Value semantics vs reference semantics",
        "Copy behavior, assignment, equality, and why two structs are never the same object.",
        13, "advanced", _m1_value_reference, _m1_value_reference_vi,
    )
    csa.register_lesson(
        MID, "csa-m1-boxing", "Boxing, unboxing, and hidden allocations",
        "Where values cross into the heap silently: interfaces, non-generic APIs, structs in delegates.",
        14, "advanced", _m1_boxing, _m1_boxing_vi,
    )
    csa.register_lesson(
        MID, "csa-m1-null-state", "Null-state analysis and the nullable contract",
        "Flow-based nullability, attributes that shape warnings, and the costs of pretending null can't happen.",
        15, "advanced", _m1_null_state, _m1_null_state_vi,
    )
    csa.register_lesson(
        MID, "csa-m1-resolution", "Overload resolution, conversions, and patterns",
        "How the compiler picks a member: betterness rules, user-defined conversions, pattern matching mechanics.",
        16, "advanced", _m1_resolution, _m1_resolution_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m1", "Checkpoint: language semantics",
        "Synthesis: predict compiler and runtime behavior across the module's traps.",
        12, "advanced", _m1_checkpoint, _m1_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m1-task", MID,
        title="Language semantics checkpoint",
        prompt=(
            "Implement `static string Classify(int input)` in class `Solution`. Rules: "
            "return \"default\" for 0, \"negative\" below 0, \"small\" for 1–99, otherwise \"large\". "
            "Then decide the boxing behavior questions in the second test by returning the exact values shown."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "classification",
                "code": (
                    'Cj.Eq(Solution.Classify(-5), "negative", "negative");\n'
                    'Cj.Eq(Solution.Classify(0), "default", "zero");\n'
                    'Cj.Eq(Solution.Classify(42), "small", "small");\n'
                    'Cj.Eq(Solution.Classify(1000), "large", "large");'
                ),
                "hint": "Four ranges in order: negative, zero, 1–99, 100+.",
            },
            {
                "name": "boxing-truth",
                "code": (
                    "object a = 5;\n"
                    "int b = (int)a;\n"
                    "b = 9;\n"
                    "// After unboxing to b and reassigning, `a` must still be 5 (copy semantics).\n"
                    'Cj.Eq((int)a, 5, "unboxed copy independent");\n'
                    "// Boxed value types never compare by identity against boxed copies via Equals chain:\n"
                    "object c = 5;\n"
                    "Cj.True(a.Equals(c), \"Equals compares boxed values\");\n"
                    "Cj.False(ReferenceEquals(a, c), \"distinct boxes\");"
                ),
                "hint": "Unboxing copies the value; Equals on boxed value types compares values; boxes are distinct objects.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static string Classify(int input)\n    {\n"
            "        if (input < 0) return \"negative\";\n"
            "        if (input == 0) return \"default\";\n"
            "        if (input <= 99) return \"small\";\n"
            "        return \"large\";\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static string Classify(int input)\n    {\n"
            "        if (input <= 0) return \"negative\";\n"
            "        if (input < 100) return \"small\";\n"
            "        return \"large\";\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p1-semantics", "Semantics under the microscope",
        "Predict-and-verify exercises: copies, boxes, null-state, and resolution traps.",
        40, "advanced", "csa-m1-value-reference",
        ["csa-p1-copy-vs-ref", "csa-p1-box-counter", "csa-p1-null-gate", "csa-p1-resolution-prediction"],
    )
    csa.register_challenge(
        "csa-p1-copy-vs-ref", MID,
        title="Copy vs reference",
        prompt=(
            "Implement `static (int, int) Twist()` that: creates a struct point (3,4), assigns it to a second "
            "variable, mutates the second to (10,20), and returns the FIRST point's coordinates. Structs copy on "
            "assignment — the first must be untouched."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "struct-copy",
                "code": (
                    "var (x, y) = Solution.Twist();\n"
                    'Cj.Eq(x, 3, "x unchanged");\n'
                    'Cj.Eq(y, 4, "y unchanged");'
                ),
                "hint": "Mutating the copy must not touch the original — return the original's fields.",
            },
        ],
        reference=(
            "public struct Pt { public int X; public int Y; }\n\n"
            "public class Solution\n{\n"
            "    public static (int, int) Twist()\n    {\n"
            "        var first = new Pt { X = 3, Y = 4 };\n"
            "        var second = first;\n"
            "        second.X = 10; second.Y = 20;\n"
            "        return (first.X, first.Y);\n"
            "    }\n}"
        ),
        wrong=(
            "public struct Pt { public int X; public int Y; }\n\n"
            "public class Solution\n{\n"
            "    public static (int, int) Twist()\n    {\n"
            "        var first = new Pt { X = 3, Y = 4 };\n"
            "        var second = first;\n"
            "        second.X = 10; second.Y = 20;\n"
            "        return (second.X, second.Y);\n"
            "    }\n}"
        ),
        level="imitation",
    )
    csa.register_challenge(
        "csa-p1-box-counter", MID,
        title="Count the boxes",
        prompt=(
            "Implement `static int Sum(ReadOnlySpan<int> values)` that sums a span WITHOUT boxing, and "
            "`static object BoxSum(ReadOnlySpan<int> values)` that returns the sum as object (this one boxes "
            "exactly once, at the return). The test verifies both values AND that BoxSum returns a boxed int."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "sum-unboxed",
                "code": (
                    "int[] data = { 1, 2, 3, 4 };\n"
                    'Cj.Eq(Solution.Sum(data), 10, "sum");\n'
                    'Cj.Eq(Solution.Sum(ReadOnlySpan<int>.Empty), 0, "empty");'
                ),
                "hint": "Span iteration never allocates — just accumulate.",
            },
            {
                "name": "box-once",
                "code": (
                    "int[] data = { 7 };\n"
                    "var boxed = Solution.BoxSum(data);\n"
                    'Cj.True(boxed.GetType() == typeof(int), "boxed int");\n'
                    'Cj.Eq((int)boxed, 7, "value survives the box");'
                ),
                "hint": "Return the sum converted to object — one box at the boundary.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static int Sum(ReadOnlySpan<int> values)\n    {\n"
            "        int total = 0;\n"
            "        foreach (var v in values) total += v;\n"
            "        return total;\n"
            "    }\n\n"
            "    public static object BoxSum(ReadOnlySpan<int> values) => Sum(values);\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int Sum(ReadOnlySpan<int> values)\n    {\n"
            "        int total = 0;\n"
            "        foreach (var v in values) total += v;\n"
            "        return total;\n"
            "    }\n\n"
            "    public static object BoxSum(ReadOnlySpan<int> values) => Sum(values) + 1;\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p1-null-gate", MID,
        title="Null-state gate",
        prompt=(
            "Implement `static int LengthOrMinus(string? text)`: return -1 when text is null, else its Length. "
            "Then implement `static string Coalesce(string? a, string? b)`: first non-null of a and b, or "
            "\"<empty>\". The tests exercise the null-state contract with nullable reference types in mind."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "length-or-minus",
                "code": (
                    'Cj.Eq(Solution.LengthOrMinus(null), -1, "null path");\n'
                    'Cj.Eq(Solution.LengthOrMinus("abc"), 3, "value path");'
                ),
                "hint": "Pattern-match null first, then Length is safe.",
            },
            {
                "name": "coalesce-chain",
                "code": (
                    'Cj.Eq(Solution.Coalesce(null, "b"), "b", "second wins");\n'
                    'Cj.Eq(Solution.Coalesce("a", "b"), "a", "first wins");\n'
                    'Cj.Eq(Solution.Coalesce(null, null), "<empty>", "fallback");'
                ),
                "hint": "?? chains left to right; a constant fallback covers the all-null case.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static int LengthOrMinus(string? text) => text is null ? -1 : text.Length;\n\n"
            "    public static string Coalesce(string? a, string? b) => a ?? b ?? \"<empty>\";\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int LengthOrMinus(string? text) => text.Length;\n\n"
            "    public static string Coalesce(string? a, string? b) => a ?? b ?? \"empty\";\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p1-resolution-prediction", MID,
        title="Resolution prediction",
        prompt=(
            "Overload pairs teach betterness. Implement class `Solution` with `static string Pick(int v)` "
            "returning \"int\", `static string Pick(long v)` returning \"long\", `static string Pick(object v)` "
            "returning \"object\", and `static string Pick<T>(T v)` returning \"generic\". Callers in the tests "
            "pass literals of different static types; your implementation just labels which overload is chosen "
            "by the test's own calls."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "literal-types",
                "code": (
                    'Cj.Eq(Solution.Pick(5), "int", "int literal beats generic");\n'
                    'Cj.Eq(Solution.Pick(5L), "long", "long literal");\n'
                    'Cj.Eq(Solution.Pick<object>(5), "generic", "explicit generic wins when T fixed");\n'
                    'Cj.Eq(Solution.Pick((object)5), "object", "object-typed argument");'
                ),
                "hint": "Exact-type match beats generic inference; T fixed by the call site beats object.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static string Pick(int v) => \"int\";\n"
            "    public static string Pick(long v) => \"long\";\n"
            "    public static string Pick(object v) => \"object\";\n"
            "    public static string Pick<T>(T v) => \"generic\";\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static string Pick(int v) => \"object\";\n"
            "    public static string Pick(long v) => \"long\";\n"
            "    public static string Pick(object v) => \"int\";\n"
            "    public static string Pick<T>(T v) => \"generic\";\n}"
        ),
        level="independent",
    )


# ── Lesson bodies (EN) ──────────────────────────────────────────────────────

_m1_execution_model = r"""## From source to executing IL

Your `.cs` file is never run. The compiler (Roslyn) parses it into a syntax
tree, binds every identifier against referenced assemblies, and emits an
**assembly**: a PE file whose payload is **IL** (stack-based instructions)
plus **metadata** tables describing every type and member. At run time, each
method's IL is translated to native machine code by the **JIT** — once per
method per process, cached, and (in .NET's default tiered mode) re-compiled
later with optimizations if the method turns hot.

```csharp
// Statics and literals are metadata; logic is IL:
static int Add(int a, int b) => a + b;
// IL: ldarg.0, ldarg.1, add, ret
```

Three layers matter for debugging real systems:

| Layer | What it decides | Where you feel it |
|---|---|---|
| Roslyn (compile) | language errors, overload choice, nullability warnings | build output |
| JIT (run) | native code quality, inlining, devirtualization | latency, throughput |
| CLR runtime | GC, layout, type loading, exceptions, threads | memory & failure modes |

**Single-translation-unit grading**: in this course your solution and each
test compile into ONE assembly, exactly how you should mentally model
"internal" visibility and type identity: same assembly, same types.

The environment you are graded in runs .NET 10 (SDK 10.0.401) with C# 14.
The same three-layer model explains why some bugs are compile-time (Roslyn
found them), some are startup-time (type load), and some only appear under
memory pressure (runtime policy) — different layers, different tools.
"""

_m1_execution_model_vi = r"""## Từ mã nguồn tới IL đang thực thi

Tệp `.cs` của bạn không bao giờ được "chạy" trực tiếp. Trình biên dịch
(Roslyn) phân tích cú pháp thành syntax tree, "bind" từng định danh với các
assembly được tham chiếu, rồi phát ra một **assembly**: tệp PE chứa **IL**
(các lệnh dạng stack) và **metadata** mô tả mọi type và member. Khi chạy, IL
của từng phương thức được JIT dịch thành mã máy — một lần mỗi phương thức
mỗi tiến trình, được cache, và (ở chế độ tiered mặc định của .NET) được biên
dịch lại với tối ưu nếu phương thức trở nên "hot".

```csharp
// Static và literal là metadata; logic là IL:
static int Add(int a, int b) => a + b;
// IL: ldarg.0, ldarg.1, add, ret
```

Ba tầng quyết định khi debug hệ thống thật:

| Tầng | Quyết định điều gì | Bạn cảm thấy ở đâu |
|---|---|---|
| Roslyn (biên dịch) | lỗi ngôn ngữ, chọn overload, cảnh báo nullability | build output |
| JIT (chạy) | chất lượng mã máy, inlining, devirtualization | latency, throughput |
| CLR runtime | GC, layout, nạp type, exception, thread | bộ nhớ & chế độ lỗi |

**Grading đơn-đơn-vị-dịch**: trong khóa này solution và từng test được biên
dịch thành MỘT assembly — đúng cách bạn nên hình dung về visibility
"internal" và định danh type: cùng assembly, cùng type.

Môi trường chấm điểm chạy .NET 10 (SDK 10.0.401) với C# 14. Cùng mô hình ba
tầng giải thích vì sao một số lỗi là lỗi biên dịch (Roslyn bắt được), một số
xuất hiện khi nạp type (startup), và một số chỉ lộ dưới áp lực bộ nhớ
(chính sách runtime) — tầng khác nhau, công cụ khác nhau.
"""

_m1_value_reference = r"""## Value semantics vs reference semantics

A **value type** variable *is* the data; a **reference type** variable is an
address *to* the data. Everything else follows:

```csharp
var a = new Counter();   // struct
var b = a;               // full copy — two independent objects
b.Increment();
// a unchanged

var s1 = new Service();  // class
var s2 = s1;             // address copy — ONE object, two names
s2.Tick();
// s1 observed the tick
```

The trap is not the definition — it is the **blast radius**. Copies stay
local: mutation can't leak. References spread: every alias can observe every
mutation, which is why shared mutable references are the root cause of most
"impossible state" bugs. Equality follows the same split: value types
compare contents (`a.Equals(b)`), reference types compare identity unless
the author overrode `Equals`.

Decision rule for modeling: default to **immutable value or record** when
the thing is data (`Money`, `Coordinates`); use a class when the thing has
**identity** that outlives its values (`UserSession`, `OrderPipeline`) —
identity, not size, is the real axis.
"""

_m1_value_reference_vi = r"""## Ngữ nghĩa value so với reference

Biến **value type** *chính là* dữ liệu; biến **reference type** là một địa
chỉ *trỏ tới* dữ liệu. Mọi thứ khác đều suy ra từ đó:

```csharp
var a = new Counter();   // struct
var b = a;               // sao chép toàn bộ — hai đối tượng độc lập
b.Increment();
// a không đổi

var s1 = new Service();  // class
var s2 = s1;             // sao chép địa chỉ — MỘT đối tượng, hai tên
s2.Tick();
// s1 cũng thấy tick
```

Cái bẫy không phải định nghĩa — mà là **bán kính tác động**. Bản sao dừng ở
phạm vi cục bộ: mutation không thể rò rỉ. Reference lan tỏa: mọi alias đều
quan sát được mọi mutation — vì thế tham chiếu khả biến dùng chung là gốc
của phần lớn lỗi "trạng thái không thể xảy ra". Equality cũng tách theo cùng
trục: value type so nội dung (`a.Equals(b)`), reference type so định danh
trừ khi tác giả override `Equals`.

Quy tắc mô hình hóa: mặc định dùng **value hoặc record bất biến** khi thứ
đó là dữ liệu (`Money`, `Coordinates`); dùng class khi thứ đó có **định
danh** tồn tại lâu hơn giá trị của nó (`UserSession`, `OrderPipeline`) —
trục thật là định danh, không phải kích thước.
"""

_m1_boxing = r"""## Boxing, unboxing, and hidden allocations

**Boxing** wraps a value type in a heap object so it can travel as
`object`, through an interface, or into a non-generic collection. Unboxing
copies it back out. The box is a real allocation — gen0 pressure, not
theoretical cost:

```csharp
int x = 42;
object o = x;          // BOX: 24-byte heap object (header + value)
int y = (int)o;        // UNBOX: copy back out
```

The silent ones are what bite in production:

```csharp
IComparable c = 5;          // box at the interface
string.Join(",", list);     // boxes each struct element
Func<int> f = s.GetHashCode; // struct receiver copied/captured
list.Add(structPoint);      // ArrayList: box per element
```

Where boxing is EXPECTED in this course: `object` boundaries you design
deliberately (serialization, homogeneous storage), and once per logical
operation — not per element in a hot loop. `ToString()` on a struct boxes if
not overridden. Watch for `enum` boxed into `Enum.HasFlag` patterns on hot
paths.

Grade your own code the way the runtime does: `GC.GetAllocatedBytesForCurrentThread()`
before and after the loop. Bytes that grow per iteration are the truth; your
intention is not.
"""

_m1_boxing_vi = r"""## Boxing, unboxing, và các cấp phát ẩn

**Boxing** bọc một value type vào một object trên heap để nó đi được dưới
dạng `object`, qua interface, hoặc vào collection không generic. Unboxing
sao chép nó ra ngoài. Box là một cấp phát thật — áp lực gen0, không phải chi
phí lý thuyết:

```csharp
int x = 42;
object o = x;          // BOX: object heap 24 byte (header + value)
int y = (int)o;        // UNBOX: sao chép ra
```

Những trường hợp âm thầm mới là thứ cắn bạn trong production:

```csharp
IComparable c = 5;           // box tại interface
string.Join(",", list);      // box từng phần tử struct
Func<int> f = s.GetHashCode; // struct receiver bị sao chép/bắt giữ
list.Add(structPoint);       // ArrayList: box mỗi phần tử
```

Ở khóa này, boxing CHẤP NHẬN được khi: ranh giới `object` bạn cố ý thiết kế
(serialization, lưu trữ đồng nhất), và một lần mỗi phép toán hợp lý — không
phải mỗi phần tử trong vòng lặp nóng. `ToString()` trên struct sẽ box nếu
không được override. Coi chừng pattern `enum` bị box qua `Enum.HasFlag` trên
đường nóng.

Hãy chấm code của mình như runtime làm: `GC.GetAllocatedBytesForCurrentThread()`
trước và sau vòng lặp. Số byte tăng theo vòng lặp là sự thật; ý định của bạn
không phải.
"""

_m1_null_state = r"""## Null-state analysis and the nullable contract

Since C# 8, `string` and `string?` are the same runtime type — nullability
is **flow analysis** the compiler performs, not a runtime guard. Inside a
method, the compiler tracks each reference's state: *maybe-null* or
*not-null*. Warnings fire when a maybe-null value is dereferenced or flows
into a not-null slot.

```csharp
string? name = FindUser();
Console.WriteLine(name.Length);      // warning: maybe-null
if (name is null) return;
Console.WriteLine(name.Length);      // OK: not-null after the check
```

The contract becomes explicit at boundaries with attributes:

```csharp
[return: NotNullIfNotNull(nameof(input))]
static string? Clean(string? input) => input?.Trim();

bool TryParse(string s, [NotNullWhen(true)] out Order? order);
```

`NotNullWhen` is how `TryX` patterns stop lying: the compiler learns that
`order` is safe exactly when the method returned true. `[MemberNotNull]`
tells the compiler a helper method established a field's non-nullness —
preferring that over `!` (the null-forgiving operator) is the difference
between a contract and a silenced check.

What null-state does NOT do: it is not validation. A non-null `string` can
still be `""`. Null-state removes a class of *crashes*; domain invariants
still need explicit checks. And at runtime, `default` (e.g. `default(string)`)
is still null — flow analysis cannot see across reflection, deserialization,
or `Unsafe` code, which is precisely where production NREs hide.
"""

_m1_null_state_vi = r"""## Phân tích null-state và hợp đồng nullable

Từ C# 8, `string` và `string?` là cùng một kiểu lúc chạy — nullability là
**phân tích luồng** trình biên dịch thực hiện, không phải cơ chế bảo vệ lúc
chạy. Trong một phương thức, compiler theo dõi trạng thái từng tham chiếu:
*có-thể-null* hoặc *không-null*. Cảnh báo vang khi giá trị maybe-null bị
dereference hoặc chảy vào chỗ not-null.

```csharp
string? name = FindUser();
Console.WriteLine(name.Length);      // cảnh báo: maybe-null
if (name is null) return;
Console.WriteLine(name.Length);      // OK: not-null sau kiểm tra
```

Hợp đồng trở nên tường minh ở ranh giới nhờ attribute:

```csharp
[return: NotNullIfNotNull(nameof(input))]
static string? Clean(string? input) => input?.Trim();

bool TryParse(string s, [NotNullWhen(true)] out Order? order);
```

`NotNullWhen` giúp pattern `TryX` không còn "nói dối": compiler hiểu rằng
`order` an toàn đúng khi phương thức trả về true. `[MemberNotNull]` báo cho
compiler biết một phương thức phụ đã thiết lập trường không-null — thích nó
hơn `!` (toán tử null-forgiving) chính là khác biệt giữa một hợp đồng và một
cảnh báo bị tắt.

Null-state KHÔNG làm gì: nó không phải xác thực. Một `string` không-null vẫn
có thể là `""`. Null-state xóa một lớp *crash*; bất biến miền nghiệp vụ vẫn
cần kiểm tra tường minh. Và lúc chạy, `default` (ví dụ `default(string)`) vẫn
là null — phân tích luồng không nhìn xuyên qua reflection, deserialization,
hay `Unsafe` — chính là nơi NRE production trú ẩn.
"""

_m1_resolution = r"""## Overload resolution, conversions, and patterns

When you call a method, Roslyn runs a deterministic search: find applicable
candidates, then apply the **betterness** rules. You do not need the spec in
your head — you need the handful of rules that decide real bugs:

1. **Exact type beats implicit conversion.** `Pick(5)` prefers `Pick(int)`
   over `Pick(long)`.
2. **Non-generic beats generic** when both apply without conversion;
   a *fixed* type argument beats both (`Pick<object>(5)` calls the generic).
3. **Implicit numeric widening** never happens implicitly in overload choice
   between `int` and `long` arguments — the int literal binds to `int`.
4. **User-defined conversions** are consulted last and never chain.

Pattern matching is compiled to type checks and value extraction:

```csharp
static string Describe(object o) => o switch
{
    int n when n < 0         => "negative",
    int and > 100            => "big int",
    string { Length: 0 }     => "empty string",
    Point(_, 0)              => "on the X axis",
    null                     => "null",
    _                        => "other",
};
```

`switch` expressions compile to a decision tree — `isinst`/`unbox` for type
patterns, comparisons for relational patterns. Recursive patterns nest
declarations, not behavior. The design win: exhaustive-looking shapes push
state decisions out of `if`-ladders into one declaration the compiler can
check (add a case for a new enum member and the `_` discards it silently —
that silence is the tax).

When patterns go wrong: matching on `object` erases generic type info
(rely on `when` guards, not on runtime surprises), and `is` type patterns
on value types *box* the operand — one more silent allocation on hot paths.
"""

_m1_resolution_vi = r"""## Overload resolution, chuyển đổi, và pattern matching

Khi bạn gọi một phương thức, Roslyn chạy một quy trình tất định: tìm các
ứng viên khả dụng, rồi áp luật **betterness**. Bạn không cần thuộc spec —
bạn cần vài luật quyết định bug thật:

1. **Kiểu chính xác thắng chuyển đổi ngầm.** `Pick(5)` ưu tiên `Pick(int)`
   hơn `Pick(long)`.
2. **Non-generic thắng generic** khi cả hai áp dụng mà không cần chuyển đổi;
   tham số kiểu *cố định* thắng cả hai (`Pick<object>(5)` gọi generic).
3. **Mở rộng số học ngầm** không xảy ra giữa tham số `int`/`long` khi chọn
   overload — literal int bám vào `int`.
4. **Chuyển đổi do người dùng định nghĩa** được xét cuối cùng và không bao
   giờ chuỗi nhau.

Pattern matching được biên dịch thành kiểm tra kiểu và trích xuất giá trị:

```csharp
static string Describe(object o) => o switch
{
    int n when n < 0         => "negative",
    int and > 100            => "big int",
    string { Length: 0 }     => "empty string",
    Point(_, 0)              => "on the X axis",
    null                     => "null",
    _                        => "other",
};
```

`switch` expression được biên dịch thành cây quyết định — `isinst`/`unbox`
cho type pattern, so sánh cho relational pattern. Recursive pattern lồng
*khai báo*, không lồng hành vi. Lợi ích thiết kế: các dạng "có vẻ đầy đủ"
đẩy quyết định trạng thái ra khỏi thang `if` về một chỗ mà compiler kiểm
tra được (thêm một enum member mới và `_` nuốt im lặng — sự im lặng ấy là
cái giá).

Khi pattern sai: so khớp trên `object` xóa thông tin kiểu generic (hãy dựa
vào guard `when`, không dựa vào bất ngờ runtime), và type pattern `is` trên
value type sẽ *box* toán hạng — thêm một cấp phát ẩn nữa trên đường nóng.
"""

_m1_checkpoint = r"""## Checkpoint: language semantics

Two graded challenges verify synthesis of the whole module:

1. **Classify** — a pure function over integer ranges (precision first).
2. **Boxing truth** — after `(int)a` unboxing and reassigning the local, the
   box must still hold 5; two boxes of the same value are distinct objects
   but `Equals` compares values.

If both pass, you can *predict* — not just use — value semantics. Move on
to the practice set for prediction drills, then to Module 2 where these
copies and boxes become measurable memory behavior.
"""

_m1_checkpoint_vi = r"""## Checkpoint: ngữ nghĩa ngôn ngữ

Hai challenge được chấm điểm xác nhận tổng hợp của cả module:

1. **Classify** — hàm thuần trên các khoảng số nguyên (độ chính xác trước).
2. **Boxing truth** — sau `(int)a` (unbox) và gán lại biến cục bộ, box phải
   vẫn giữ 5; hai box của cùng giá trị là hai object khác nhau nhưng
   `Equals` so sánh giá trị.

Nếu cả hai pass, bạn đã *dự đoán được* — không chỉ *sử dụng được* — ngữ
nghĩa value. Sang practice set để luyện dự đoán, rồi tới Module 2 nơi các
bản sao và box trở thành hành vi bộ nhớ đo lường được.
"""
