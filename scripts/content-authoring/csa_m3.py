"""Module 3 — Advanced generics and the type system (csa-m3)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-generics-deep",
        "Advanced Generics and the Type System",
        "Variance, static abstracts, generic math, and constraints that compile into proofs — plus their runtime cost.",
    )

    csa.register_lesson(
        MID, "csa-m3-variance", "Variance: co, contra, in",
        "Why IEnumerable<T> is out, Action<in T> is in, IList<T> is neither — and what that buys you.",
        14, "advanced", _m3_variance, _m3_variance_vi,
    )
    csa.register_lesson(
        MID, "csa-m3-static-abstracts", "Static abstract members and generic math",
        "Interfaces with static abstracts: the type argument itself becomes the polymorphic dispatch target.",
        15, "advanced", _m3_static_abs, _m3_static_abs_vi,
    )
    csa.register_lesson(
        MID, "csa-m3-generics-runtime", "What generics cost at runtime",
        "Code sharing for reference types, specialization for value types, and where that shows up.",
        13, "advanced", _m3_runtime, _m3_runtime_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m3", "Checkpoint: generics",
        "Synthesis: variance legality, static-abstract dispatch, and generic allocation reasoning.",
        12, "advanced", _m3_checkpoint, _m3_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m3-task", MID,
        title="Generics checkpoint",
        prompt=(
            "Define `interface IShape<TSelf> where TSelf : IShape<TSelf>` with `static abstract string Name { get; }` "
            "and `static abstract double Area(double side);`. Implement `struct Square : IShape<Square>` "
            "(Area = side*side) and `struct Circle : IShape<Circle>` (Area = π·side² using Math.PI). Then implement "
            "`static double AreaOf<T>(double side) where T : IShape<T> => T.Area(side);` in class `Solution`."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "static-dispatch",
                "code": (
                    'Cj.Eq(Solution.AreaOf<Square>(5), 25.0, "Square");\n'
                    'Cj.True(Math.Abs(Solution.AreaOf<Circle>(2) - 4 * Math.PI) < 1e-9, "Circle");'
                ),
                "hint": "The type argument supplies the static members — no instance, no reflection.",
            },
            {
                "name": "no-instantiation",
                "code": (
                    "// AreaOf<T> must not create anything:\n"
                    "long b0 = GC.GetAllocatedBytesForCurrentThread();\n"
                    "double d = Solution.AreaOf<Square>(3);\n"
                    "long b1 = GC.GetAllocatedBytesForCurrentThread();\n"
                    'Cj.True(b1 - b0 == 0, $"allocated {b1 - b0}");'
                ),
                "hint": "Static abstract dispatch is compile-time — zero allocations, zero instances.",
            },
        ],
        reference=(
            "public interface IShape<TSelf> where TSelf : IShape<TSelf>\n{\n"
            "    static abstract string Name { get; }\n"
            "    static abstract double Area(double side);\n}\n\n"
            "public struct Square : IShape<Square>\n{\n"
            "    public static string Name => \"Square\";\n"
            "    public static double Area(double side) => side * side;\n}\n\n"
            "public struct Circle : IShape<Circle>\n{\n"
            "    public static string Name => \"Circle\";\n"
            "    public static double Area(double side) => Math.PI * side * side;\n}\n\n"
            "public class Solution\n{\n"
            "    public static double AreaOf<T>(double side) where T : IShape<T> => T.Area(side);\n}"
        ),
        wrong=(
            "public interface IShape<TSelf> where TSelf : IShape<TSelf>\n{\n"
            "    static abstract string Name { get; }\n"
            "    static abstract double Area(double side);\n}\n\n"
            "public struct Square : IShape<Square>\n{\n"
            "    public static string Name => \"Square\";\n"
            "    public static double Area(double side) => side * side;\n}\n\n"
            "public struct Circle : IShape<Circle>\n{\n"
            "    public static string Name => \"Circle\";\n"
            "    public static double Area(double side) => side * side;   // WRONG: square formula\n}\n\n"
            "public class Solution\n{\n"
            "    public static double AreaOf<T>(double side) where T : IShape<T> => T.Area(side);\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p3-generics", "Generic machinery",
        "Variance drills, static-abstract abstractions, and allocation reasoning for generic code.",
        45, "advanced", "csa-m3-variance",
        ["csa-p3-variance-legality", "csa-p3-comparer-contravariance", "csa-p3-generic-math-sum"],
    )
    csa.register_challenge(
        "csa-p3-variance-legality", MID,
        title="Variance legality",
        prompt=(
            "Implement `static string Variance(IEnumerable<object> xs)` returning \"ok\", and prove contravariance: "
            "implement `static Action<string> AsObjectAction(Action<object> a) => a;` (assigning Action<object> to "
            "Action<string> is legal because T is contravariant in Action<in T>). Also implement "
            "`static string First(IReadOnlyList<string> list)` returning list[0] — IReadOnlyList<out T> is covariant."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "variance-works",
                "code": (
                    "Action<object> print = o => { };\n"
                    "Action<string> ps = Solution.AsObjectAction(print);\n"
                    "ps(\"hello\");   // must compile and run\n"
                    'Cj.Eq(Solution.Variance(new[] { "a", "b" }), "ok", "covariant read");'
                ),
                "hint": "Action<in T>: an object-consumer can consume strings. IReadOnlyList<out T>: reads widen.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static Action<string> AsObjectAction(Action<object> a) => a;\n\n"
            "    public static string Variance(IEnumerable<object> xs) => \"ok\";\n\n"
            "    public static string First(IReadOnlyList<string> list) => list[0];\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static Action<object> AsObjectAction(Action<string> a) => a;  // WRONG direction\n\n"
            "    public static string Variance(IEnumerable<object> xs) => \"ok\";\n\n"
            "    public static string First(IReadOnlyList<string> list) => list[0];\n}"
        ),
        level="imitation",
    )
    csa.register_challenge(
        "csa-p3-comparer-contravariance", MID,
        title="A comparer for anything smaller",
        prompt=(
            "Implement `class Box { public int Weight; }` and a contravariant comparer adapter: "
            "`static IComparer<Box> ByWeight() => Comparer<Box>.Create((x, y) => x.Weight.CompareTo(y.Weight));` "
            "in class `Solution`. Then use it: `static void Sort(List<Box> boxes)` sorts by Weight ascending "
            "in place using the comparer."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "sort",
                "code": (
                    "var boxes = new List<Box> { new Box { Weight = 3 }, new Box { Weight = 1 }, new Box { Weight = 2 } };\n"
                    "Solution.Sort(boxes);\n"
                    'Cj.Eq(boxes[0].Weight, 1, "first");\n'
                    'Cj.Eq(boxes[2].Weight, 3, "last");'
                ),
                "hint": "Comparer<T>.Create builds an IComparer<T> from a lambda; List<T>.Sort(comparer) sorts in place.",
            },
        ],
        reference=(
            "public class Box { public int Weight; }\n\n"
            "public class Solution\n{\n"
            "    public static IComparer<Box> ByWeight() =>\n"
            "        Comparer<Box>.Create((x, y) => x.Weight.CompareTo(y.Weight));\n\n"
            "    public static void Sort(List<Box> boxes) => boxes.Sort(ByWeight());\n}"
        ),
        wrong=(
            "public class Box { public int Weight; }\n\n"
            "public class Solution\n{\n"
            "    public static IComparer<Box> ByWeight() =>\n"
            "        Comparer<Box>.Create((x, y) => y.Weight.CompareTo(x.Weight));   // descending\n\n"
            "    public static void Sort(List<Box> boxes) => boxes.Sort(ByWeight());\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p3-generic-math-sum", MID,
        title="Sum any numeric type",
        prompt=(
            "Implement `static T Sum<T>(T[] values) where T : INumber<T>` summing all elements starting from T.Zero, "
            "and `static T Average<T>(T[] values) where T : INumber<T>` returning Sum / count (use T.CreateTruncating "
            "for the count). Works for int, double, decimal — one implementation."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "int",
                "code": (
                    'Cj.Eq(Solution.Sum(new[] { 1, 2, 3 }), 6, "int sum");\n'
                    'Cj.Eq(Solution.Average(new[] { 1, 2, 3, 4 }), 2, "int avg (truncated)");'
                ),
                "hint": "T.Zero starts the fold; use += via operators on INumber<T>.",
            },
            {
                "name": "double",
                "code": (
                    "var d = Solution.Sum(new[] { 0.5, 0.25 });\n"
                    'Cj.True(Math.Abs(d - 0.75) < 1e-9, "double sum");\n'
                    "var a = Solution.Average(new[] { 1.0, 2.0 });\n"
                    'Cj.True(Math.Abs(a - 1.5) < 1e-9, "double avg");'
                ),
                "hint": "Same generic code; the type argument brings its own arithmetic.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static T Sum<T>(T[] values) where T : INumber<T>\n    {\n"
            "        T total = T.Zero;\n"
            "        foreach (var v in values) total += v;\n"
            "        return total;\n"
            "    }\n\n"
            "    public static T Average<T>(T[] values) where T : INumber<T>\n"
            "        => Sum(values) / T.CreateTruncating(values.Length);\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static T Sum<T>(T[] values) where T : INumber<T>\n    {\n"
            "        T total = T.Zero;\n"
            "        foreach (var v in values) total -= v;   // WRONG operator\n"
            "        return total;\n"
            "    }\n\n"
            "    public static T Average<T>(T[] values) where T : INumber<T>\n"
            "        => Sum(values) / T.CreateTruncating(values.Length);\n}"
        ),
        level="independent",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m3_variance = r"""## Variance: co, contra, in

Variance answers one question: **when is `C<Derived>` usable as `C<Base>`?**
The direction follows data flow, and the compiler enforces safety:

- **Covariant** (`out T`): T only *exits*. `IEnumerable<out T>`,
  `IReadOnlyList<out T>`. A sequence of cats is a sequence of animals.
- **Contravariant** (`in T`): T only *enters*. `Action<in T>`,
  `IComparer<in T>`, `Predicate<in T>`. A consumer of animals can consume
  cats.
- **Invariant** (plain `T`): T both enters and exits. `IList<T>`,
  `Dictionary<TKey,TValue>` (keys enter, values exit). Variance would be
  unsound the moment a value could flow both ways through the same slot.

```csharp
IEnumerable<object> animals = new List<Cat>();     // OK: out
Action<Cat> feedCat = c => c.Eat();
Action<Animal> feedAny = a => a.Eat();
feedCat = feedAny;                                  // OK: in — an Animal-consumer handles Cats
// feedAny = feedCat;                               // compile error — would feed a Dog to Cat code
```

Two habits worth keeping forever:

1. **Design your own interfaces with variance in mind.** A read-only
   repository `IRead<out T>` composes with base-type handlers; an invariant
   one forces casts at every boundary.
2. **Variance is interface/delegate only.** Classes are invariant — wrap a
   covariant view over internal storage instead of fighting it.

The trap that survives review: `IEnumerable<object> xs = strings` is fine,
but `xs.Add`-style mutation doesn't exist there — the moment you need
*write* access you need an invariant type, and pretending otherwise is how
`InvalidCastException` at a distance happens (arrays are the legacy
exception — covariant but checked at write time, at runtime cost).
"""

_m3_variance_vi = r"""## Variance: co, contra, in

Variance trả lời một câu hỏi: **khi nào `C<Derived>` dùng được như
`C<Base>`?** Chiều variance đi theo dòng dữ liệu, và compiler bắt buộc an
toàn:

- **Covariant** (`out T`): T chỉ *đi ra*. `IEnumerable<out T>`,
  `IReadOnlyList<out T>`. Một dãy mèo là một dãy động vật.
- **Contravariant** (`in T`): T chỉ *đi vào*. `Action<in T>`,
  `IComparer<in T>`, `Predicate<in T>`. Bộ tiêu thụ Animal tiêu thụ được
  Cat.
- **Invariant** (`T` thường): T vừa vào vừa ra. `IList<T>`,
  `Dictionary<TKey,TValue>` (key vào, value ra). Variance sẽ mất an toàn
  ngay khi một giá trị có thể chảy cả hai chiều qua cùng một chỗ.

```csharp
IEnumerable<object> animals = new List<Cat>();     // OK: out
Action<Cat> feedCat = c => c.Eat();
Action<Animal> feedAny = a => a.Eat();
feedCat = feedAny;                                  // OK: in — bộ tiêu thụ Animal xử lý được Cat
// feedAny = feedCat;                               // lỗi biên dịch — sẽ cho Dog vào code của Cat
```

Hai thói quen đáng giữ mãi mãi:

1. **Thiết kế interface của riêng mình có chủ đích về variance.** Một
   repository chỉ đọc `IRead<out T>` kết hợp tự nhiên với handler của kiểu
   cơ sở; bản invariant buộc cast ở mọi ranh giới.
2. **Variance chỉ có ở interface/delegate.** Class luôn invariant — hãy bọc
   một view covariant trên kho lưu trữ nội bộ thay vì chống lại nó.

Cái bẫy sống sót qua review: `IEnumerable<object> xs = strings` ổn, nhưng
mutation kiểu `xs.Add` không tồn tại ở đó — kho cần quyền *ghi* là lúc bạn
cần kiểu invariant, và pretend ngược lại chính là cách `InvalidCastException`
xảy ra ở xa (mảng là ngoại lệ lịch sử — covariant nhưng bị kiểm tra lúc ghi,
với chi phí runtime).
"""

_m3_static_abs = r"""## Static abstract members and generic math

Since C# 11 / .NET 7, interface members can be **static abstract**. The
consequence is bigger than the syntax: the *type argument itself* becomes
the dispatch target. No instances, no reflection, no boxing:

```csharp
public interface IShape<TSelf> where TSelf : IShape<TSelf>
{
    static abstract double Area(double side);
}

public struct Square : IShape<Square>
{
    public static double Area(double side) => side * side;
}

static double AreaOf<T>(double side) where T : IShape<T> => T.Area(side);
// AreaOf<Square>(5) → 25, resolved at compile time per T
```

This is the machinery under **generic math**: `INumber<T>`,
`IAdditionOperators<T,T,T>`, `IParsable<T>` — so one algorithm serves
`int`, `double`, `decimal`, and any numeric type anyone defines later,
with operators resolved statically. The JIT specializes per value type,
so the arithmetic compiles down to the same machine code as hand-written
`double` math.

The self-constraining pattern (`TSelf : IShape<TSelf>`) is the CRTP of C#:
it lets instance/static members refer to "my own type". When to reach for
it: abstraction over *kinds* (shapes, numeric types, parsers) where the
operations belong to the type, not to instances. When NOT: anything that
needs runtime-chosen behavior — that is what normal virtual dispatch is
for. Static abstracts are compile-time structure, not a performance button.
"""

_m3_static_abs_vi = r"""## Static abstract members và generic math

Từ C# 11 / .NET 7, member của interface có thể là **static abstract**. Hệ
quả lớn hơn cú pháp: *tham số kiểu* trở thành đích dispatch. Không cần thể
hiện, không reflection, không boxing:

```csharp
public interface IShape<TSelf> where TSelf : IShape<TSelf>
{
    static abstract double Area(double side);
}

public struct Square : IShape<Square>
{
    public static double Area(double side) => side * side;
}

static double AreaOf<T>(double side) where T : IShape<T> => T.Area(side);
// AreaOf<Square>(5) → 25, resolved lúc biên dịch theo từng T
```

Đây chính là cơ khí đằng sau **generic math**: `INumber<T>`,
`IAdditionOperators<T,T,T>`, `IParsable<T>` — một thuật toán phục vụ
`int`, `double`, `decimal`, và bất kỳ kiểu số nào định nghĩa sau này, với
toán tử được resolve tĩnh. JIT chuyên biệt hóa theo từng value type, nên
phép toán biên dịch xuống cùng mã máy như toán `double` viết tay.

Pattern tự-ràng-buộc (`TSelf : IShape<TSelf>`) là CRTP của C#: nó cho phép
member tĩnh/thể hiện tham chiếu "kiểu của chính mình". Khi nào dùng: trừu
tượng hóa trên *loại* (shape, kiểu số, parser) nơi phép toán thuộc về kiểu,
không thuộc về thể hiện. Khi nào KHÔNG: mọi thứ cần hành vi chọn lúc chạy —
đó là việc của virtual dispatch thông thường. Static abstract là cấu trúc
lúc biên dịch, không phải nút tăng hiệu năng.
"""

_m3_runtime = r"""## What generics cost at runtime

The CLR implements generics with two different strategies, and knowing
which is in play explains real performance:

- **Reference types share code.** `List<string>`, `List<object>`,
  `List<YourClass>` all execute ONE specialized-for-references body. The
  runtime creates it once per generic type. You pay nothing extra per
  instantiation — that is why generic collections of classes are free.
- **Value types get specialized code.** `List<int>` compiles its own
  version with the element type embedded — no boxing, direct indexing,
  better cache locality. Cost: more native code per distinct T (code bloat)
  — normally a fine trade.

What this means in practice:

```csharp
// Same source, different runtime story:
var a = new List<string>();  // shared ref-type body
var b = new List<int>();     // specialized: no boxing, tight layout
var c = new List<MyStruct>(); // specialized: copies whole structs on add
```

Bigger elements = more copying on every insert/remove — a large struct in a
`List<T>` copies bytes; if that hurts, store references (`List<Ref>`), or
restructure as arrays of primitives (data-oriented layout, Module 15).

Where constraints matter to cost: `where T : class` keeps the shared
ref-type path; unconstrained `T` with value types means specialization.
`default(T)` in shared code, interface calls through generic `T`, and
reflection over open generics (`typeof(List<>).MakeGenericType(...)`) each
have their own story — measure before believing any of it.
"""

_m3_runtime_vi = r"""## Generics tốn gì lúc chạy

CLR cài đặt generics bằng hai chiến lược khác nhau, và biết chiến lược nào
đang chạy sẽ giải thích hiệu năng thật:

- **Kiểu tham chiếu dùng chung mã.** `List<string>`, `List<object>`,
  `List<YourClass>` đều chạy MỘT thân hàm chuyên biệt cho reference. Runtime
  tạo nó một lần cho mỗi generic type. Không tốn thêm gì cho mỗi lần khởi
  tạo — vì thế collection generic của class gần như miễn phí.
- **Value type được chuyên biệt hóa.** `List<int>` biên dịch phiên bản riêng
  với phần tử nhúng sẵn — không boxing, đánh chỉ mục trực tiếp, cache locality
  tốt hơn. Chi phí: nhiều mã máy hơn cho mỗi T khác nhau (code bloat) —
  thường là sự đánh đổi hợp lý.

Ý nghĩa thực hành:

```csharp
// Cùng mã nguồn, câu chuyện runtime khác nhau:
var a = new List<string>();   // thân dùng chung cho ref-type
var b = new List<int>();      // chuyên biệt: không boxing, layout chặt
var c = new List<MyStruct>(); // chuyên biệt: copy cả struct khi add
```

Phần tử càng lớn = càng nhiều byte copy khi insert/remove — struct lớn
trong `List<T>` sao chép từng byte; nếu điều đó đau, lưu tham chiếu
(`List<Ref>`), hoặc tái cấu trúc thành mảng primitive (data-oriented
layout, Module 15).

Ràng buộc ảnh hưởng thế nào tới chi phí: `where T : class` giữ đường dùng
chung ref-type; `T` không ràng buộc với value type nghĩa là chuyên biệt hóa.
`default(T)` trong mã dùng chung, lời gọi interface qua generic `T`, và
reflection trên open generics (`typeof(List<>).MakeGenericType(...)`) mỗi
cái có câu chuyện riêng — hãy đo trước khi tin điều nào đó.
"""

_m3_checkpoint = r"""## Checkpoint: generics

One graded task verifies three ideas at once:

1. **Static abstract dispatch** — the type argument supplies `Area`, no
   instance created, zero allocations.
2. **Variance legality** — contravariant assignment of delegates.
3. **Generic math** — one `INumber<T>` implementation for several numeric
   types.

Passing means you can design abstractions where the compiler does the
runtime's work ahead of time. Next: delegates and closures — the other half
of "code as data".
"""

_m3_checkpoint_vi = r"""## Checkpoint: generics

Một bài được chấm xác nhận ba ý tưởng cùng lúc:

1. **Static abstract dispatch** — tham số kiểu cung cấp `Area`, không tạo
   thể hiện, không cấp phát.
2. **Tính hợp lệ của variance** — gán delegate theo chiều contravariant.
3. **Generic math** — một cài đặt `INumber<T>` cho nhiều kiểu số.

Pass nghĩa là bạn thiết kế được trừu tượng mà compiler làm sẵn phần việc
của runtime. Tiếp theo: delegate và closure — nửa còn lại của "code as
data".
"""
