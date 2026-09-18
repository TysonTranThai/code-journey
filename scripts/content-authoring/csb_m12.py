#!/usr/bin/env python3
"""C# — Beginner — Module 12: csb-generics.

Generic methods and classes: type parameters as a compile-time promise.
Ws lose the promise (object/boxing) or violate constraints. House
conventions: Ws are behavioral near-misses, tests discriminate.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-generics"

write_module(
    M,
    "Generics",
    "Type parameters: writing an algorithm once and letting the compiler stamp it out for every type — safely.",
    "Generics (Kiểu tổng quát)",
    "Tham số kiểu: viết thuật toán một lần và để trình biên dịch đóng dấu cho mọi kiểu — một cách an toàn.",
    ["csb-m12-generics", "csb-m12-constraints", "csb-m12-generic-collections", "csb-checkpoint-m12"],
    ["csb-p12-generics"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m12-generics",
    "Generic methods and classes",
    "A type parameter is a placeholder the caller fills in; the compiler checks every use against it.",
    13,
    r"""
## The duplication problem

Swap two values, find the max, reverse a list — for `int`, then `string`, then `Money`... The logic is identical; only the type changes. Copy-pasting per type is how bugs breed.

## `<T>` writes it once

```csharp
static T Max<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) >= 0 ? a : b;
}

Max(3, 7);            // T = int
Max("apple", "pear"); // T = string
```

`T` is a **type parameter**: the caller's argument type fills it in, and the compiler enforces every operation on `T` against what the constraint allows. Inside the method there is no casting, no boxing, and no way to sneak in the wrong type.

Generic classes work the same way:

```csharp
class Box<T>
{
    public T Content { get; set; }
}

var ib = new Box<int> { Content = 42 };
var sb = new Box<string> { Content = "hi" };
// ib.Content is int, sb.Content is string — statically
```

You already use generics everywhere: `List<T>`, `Dictionary<TKey, TValue>` — now you can write your own.
""",
    "Phương thức và lớp generic",
    "Tham số kiểu là chỗ trống người gọi điền vào; trình biên dịch kiểm tra mọi thao tác dựa trên nó.",
    r"""
## Bài toán lặp mã

Đổi chỗ hai giá trị, tìm max, đảo danh sách — cho `int`, rồi `string`, rồi `Money`... Logic giống hệt nhau; chỉ có kiểu là khác. Copy-paste theo từng kiểu là cách bug sinh sôi.

## `<T>` viết một lần

```csharp
static T Max<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) >= 0 ? a : b;
}

Max(3, 7);            // T = int
Max("apple", "pear"); // T = string
```

`T` là một **tham số kiểu**: kiểu của đối số người gọi điền vào, và trình biên dịch kiểm tra mọi thao tác trên `T` theo những gì ràng buộc cho phép. Trong phương thức không có ép kiểu, không boxing, không cách nào lén đưa kiểu sai vào.

Lớp generic cũng vậy:

```csharp
class Box<T>
{
    public T Content { get; set; }
}

var ib = new Box<int> { Content = 42 };
var sb = new Box<string> { Content = "hi" };
// ib.Content là int, sb.Content là string — tĩnh
```

Bạn đã dùng generic ở khắp nơi: `List<T>`, `Dictionary<TKey, TValue>` — giờ bạn tự viết được.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m12-constraints",
    "Constraints: what `T` can do",
    "`where` clauses declare the capabilities a type argument must have — and unlock exactly those operations.",
    12,
    r"""
## Operations need permissions

Inside a generic method, `T` starts with no abilities — you can't call `a.CompareTo(b)` without promising `T` supports comparison. **Constraints** are that promise:

```csharp
where T : IComparable<T>   // T knows how to compare to itself
where T : class            // T is a reference type
where T : struct           // T is a value type (non-nullable)
where T : new()            // T has a parameterless constructor
where T : SomeBase         // T is (or derives from) SomeBase
```

With `where T : IComparable<T>`, the compiler *unlocks* `CompareTo` on every `T` — and *rejects* type arguments that lack it. Constraints both restrict callers and enable the method body.

## The honest rule

Add a constraint only when the body needs that capability. An empty `where T : class` "for safety" restricts callers for no reason. Start from the operations the algorithm needs; the constraint list writes itself.
""",
    "Ràng buộc: `T` làm được gì",
    "Mệnh đề `where` khai báo năng lực mà tham số kiểu bắt buộc phải có — và mở khóa đúng những năng lực đó.",
    r"""
## Thao tác cần sự cho phép

Trong một phương thức generic, `T` ban đầu không có năng lực nào — không thể gọi `a.CompareTo(b)` nếu chưa hứa `T` hỗ trợ so sánh. **Ràng buộc** chính là lời hứa đó:

```csharp
where T : IComparable<T>   // T biết so sánh với chính nó
where T : class            // T là kiểu tham chiếu
where T : struct           // T là kiểu giá trị (không nullable)
where T : new()            // T có constructor không tham số
where T : SomeBase         // T là (hoặc kế thừa) SomeBase
```

Với `where T : IComparable<T>`, trình biên dịch *mở khóa* `CompareTo` trên mọi `T` — và *từ chối* các tham số kiểu thiếu nó. Ràng buộc vừa giới hạn người gọi, vừa cấp quyền cho thân phương thức.

## Quy tắc trung thực

Chỉ thêm ràng buộc khi thân phương thức cần năng lực đó. Một `where T : class` "cho an toàn" chỉ giới hạn người gọi vô ích. Hãy bắt đầu từ các thao tác thuật toán cần; danh sách ràng buộc tự viết ra.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m12-generic-collections",
    "Generic collections are the payoff",
    "`List<T>`, `Dictionary<TKey, TValue>`, `Queue<T>`, `Stack<T>` — the BCL is built from the same tool you just learned.",
    11,
    r"""
## Reading the signatures

```csharp
public class List<T> { ... }
public class Dictionary<TKey, TValue> { ... }
```

The collections you've used since module 8 are generic classes. Their type parameters are why `list[0]` returns `T` — not `object` you must cast — and why putting a `string` into a `List<int>` is a compile error, not a runtime surprise.

## Why not `object`?

Pre-generics collections stored `object` (the base of everything):

```csharp
// the old disease, still legal:
var list = new ArrayList();
list.Add(42);
int x = (int)list[0];          // cast needed, checked at RUNTIME
list.Add("oops");              // compiles fine — boom later
```

Value types stored in `object` also box (heap-allocate) on every add. Generics eliminate the casts, move errors to compile time, and skip the boxing. That trio — no casts, compile-time safety, no boxing — is the entire point.
""",
    "Bộ sưu tập generic là phần thưởng",
    "`List<T>`, `Dictionary<TKey, TValue>`, `Queue<T>`, `Stack<T>` — thư viện chuẩn được dựng từ chính công cụ bạn vừa học.",
    r"""
## Đọc chữ ký

```csharp
public class List<T> { ... }
public class Dictionary<TKey, TValue> { ... }
```

Các bộ sưu tập bạn dùng từ module 8 là những lớp generic. Tham số kiểu là lý do `list[0]` trả về `T` — không phải `object` phải ép kiểu — và vì sao đưa `string` vào `List<int>` là lỗi biên dịch, không phải bất ngờ lúc chạy.

## Tại sao không dùng `object`?

Các bộ sưu tập tiền-generic lưu `object` (gốc của mọi kiểu):

```csharp
// căn bệnh cũ, vẫn hợp lệ:
var list = new ArrayList();
list.Add(42);
int x = (int)list[0];          // phải ép kiểu, kiểm tra lúc CHẠY
list.Add("oops");              // biên dịch được — nổ sau
```

Kiểu giá trị lưu trong `object` còn bị boxing (cấp phát heap) mỗi lần thêm. Generics xóa bỏ ép kiểu, đẩy lỗi về lúc biên dịch, và bỏ qua boxing. Bộ ba đó — không ép kiểu, an toàn lúc biên dịch, không boxing — là toàn bộ ý nghĩa.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p12-generics",
    "Generics workout",
    "Swaps, stacks, pair stores, and a count-if — type parameters under discriminating tests.",
    "Luyện tập generics",
    "Đổi chỗ, ngăn xếp, kho cặp giá trị, và đếm-điều-kiện — tham số kiểu dưới các bài kiểm tra phân biệt.",
    "csb-m12-generic-collections",
    40,
    "beginner",
    [
        challenge(
            "csb-p12-swap",
            "Generic swap and reverse",
            "Implement in `Solution`: `static void Swap<T>(T[] items, int i, int j)` swapping in place (throws `ArgumentOutOfRangeException` for out-of-range indices), and `static T[] Reversed<T>(T[] items)` returning a NEW array in reverse order (null/empty → empty array, never null).",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var a = new[] { 1, 2, 3 };\nSolution.Swap(a, 0, 2);\nCj.Eq(string.Join(\",\", a), \"3,2,1\", \"swap in place\");\nvar r = Solution.Reversed(a);\nCj.Eq(string.Join(\",\", r), \"1,2,3\", \"new reversed array\");\nCj.Eq(string.Join(\",\", a), \"3,2,1\", \"original untouched by Reversed\");",
                    "Swap mutates the caller's array; Reversed must not.",
                ),
                (
                    "edges",
                    "bool t = false;\ntry { Solution.Swap(new[] { 1, 2 }, 0, 5); } catch (ArgumentOutOfRangeException) { t = true; }\nCj.True(t, \"out-of-range index rejected\");\nCj.Eq(Solution.Reversed(new string[0]).Length, 0, \"empty -> empty\");\nCj.False(Solution.Reversed<string>(null) == null, \"null input never yields null\");",
                    "Both contracts: indices validated, null-input normalized to an empty array.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p12-countif",
            "CountIf with a predicate",
            "Implement `static int CountIf<T>(IEnumerable<T> items, Func<T, bool> predicate)` counting matching elements; null items → 0.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.CountIf(new[] { 1, 2, 3, 4 }, x => x % 2 == 0), 2, \"two evens\");\nCj.Eq(Solution.CountIf(new[] { \"a\", \"bb\", \"c\" }, s => s.Length > 1), 1, \"one long string\");",
                    "The delegate decides membership; the method just counts.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.CountIf(new int[0], _ => true), 0, \"empty\");\nCj.Eq(Solution.CountIf<int>(null, x => true), 0, \"null items\");\nCj.Eq(Solution.CountIf(new[] { 1, 2 }, _ => false), 0, \"predicate rejects all\");",
                    "Empty, null, and reject-all all return 0 without exceptions.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p12-pairstore",
            "A generic PairStore<T>",
            "Implement nested generic class `Solution.PairStore<T>`: `Add(T item)` appends; `Count` read-only; `Get(int index)` returns the item at index and throws `ArgumentOutOfRangeException` when out of range; `Clear()` empties. All state private behind properties/methods.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var ps = new Solution.PairStore<string>();\nps.Add(\"a\");\nps.Add(\"b\");\nCj.Eq(ps.Count, 2, \"two items\");\nCj.Eq(ps.Get(0), \"a\", \"first\");\nCj.Eq(ps.Get(1), \"b\", \"second\");\nps.Clear();\nCj.Eq(ps.Count, 0, \"cleared\");",
                    "Add/Count/Get/Clear behave like a minimal List<T>.",
                ),
                (
                    "bounds",
                    "var ps = new Solution.PairStore<int>();\nbool t = false;\ntry { ps.Get(0); } catch (ArgumentOutOfRangeException) { t = true; }\nCj.True(t, \"empty store has no index 0\");\nps.Add(7);\nCj.Eq(ps.Get(0), 7, \"item retrievable after add\");",
                    "Bounds are enforced even before the first Add.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p12-maxof",
            "Max with a constraint",
            "Implement `static T MaxOf<T>(IEnumerable<T> items) where T : IComparable<T>` returning the largest element; throws `InvalidOperationException` for null or empty input.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.MaxOf(new[] { 3, 9, 2 }), 9, \"int max\");\nCj.Eq(Solution.MaxOf(new[] { \"pear\", \"apple\" }), \"pear\", \"string max (ordinal)\");\nCj.Eq(Solution.MaxOf(new[] { 2.5, 2.75, 2.5 }), 2.75, \"double max\");",
                    "One method, three types — the constraint unlocks CompareTo for each.",
                ),
                (
                    "edges",
                    "bool t1 = false;\ntry { Solution.MaxOf<int>(null); } catch (InvalidOperationException) { t1 = true; }\nbool t2 = false;\ntry { Solution.MaxOf(new int[0]); } catch (InvalidOperationException) { t2 = true; }\nCj.True(t1 && t2, \"null and empty both rejected\");\nCj.Eq(Solution.MaxOf(new[] { 42 }), 42, \"single element\");",
                    "Empty input has no max — that's an exceptional condition, not a default value.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p12-swap": vi_challenge(
            "Đổi chỗ và đảo mảng generic",
            "Hiện thực trong `Solution`: `static void Swap<T>(T[] items, int i, int j)` đổi chỗ tại chỗ (ném `ArgumentOutOfRangeException` với chỉ số ngoài khoảng), và `static T[] Reversed<T>(T[] items)` trả mảng MỚI theo thứ tự ngược (null/rỗng → mảng rỗng, không bao giờ null).",
            [
                ("normal", "Swap biến đổi mảng của người gọi; Reversed thì không."),
                ("edges", "Cả hai hợp đồng: chỉ số được kiểm tra, đầu vào null được chuẩn hóa thành mảng rỗng."),
            ],
        ),
        "csb-p12-countif": vi_challenge(
            "CountIf với một predicate",
            "Hiện thực `static int CountIf<T>(IEnumerable<T> items, Func<T, bool> predicate)` đếm các phần tử khớp; items null → 0.",
            [
                ("normal", "Delegate quyết định thành viên; phương thức chỉ việc đếm."),
                ("edges", "Rỗng, null, và từ-chối-tất-cả đều trả 0 mà không ném ngoại lệ."),
            ],
        ),
        "csb-p12-pairstore": vi_challenge(
            "PairStore<T> generic",
            "Hiện thực lớp generic lồng `Solution.PairStore<T>`: `Add(T item)` thêm vào; `Count` chỉ-đọc; `Get(int index)` trả phần tử tại chỉ số và ném `ArgumentOutOfRangeException` khi ngoài khoảng; `Clear()` dọn sạch. Toàn bộ trạng thái là private, phơi ra qua thuộc tính/phương thức.",
            [
                ("normal", "Add/Count/Get/Clear hành xử như một List<T> tối giản."),
                ("bounds", "Khoảng được thực thi ngay cả trước lần Add đầu tiên."),
            ],
        ),
        "csb-p12-maxof": vi_challenge(
            "Max với ràng buộc",
            "Hiện thực `static T MaxOf<T>(IEnumerable<T> items) where T : IComparable<T>` trả phần tử lớn nhất; ném `InvalidOperationException` với đầu vào null hoặc rỗng.",
            [
                ("normal", "Một phương thức, ba kiểu — ràng buộc mở khóa CompareTo cho từng kiểu."),
                ("edges", "Đầu vào rỗng không có max — đó là điều kiện ngoại lệ, không phải giá trị mặc định."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p12-swap",
            'public class Solution\n{\n    public static void Swap<T>(T[] items, int i, int j)\n    {\n        if (i < 0 || i >= items.Length || j < 0 || j >= items.Length)\n            throw new ArgumentOutOfRangeException("index out of range");\n        T tmp = items[i];\n        items[i] = items[j];\n        items[j] = tmp;\n    }\n    public static T[] Reversed<T>(T[] items)\n    {\n        if (items == null || items.Length == 0)\n            return new T[0];\n        var result = new T[items.Length];\n        for (int i = 0; i < items.Length; i++)\n            result[i] = items[items.Length - 1 - i];\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static void Swap<T>(T[] items, int i, int j)\n    {\n        if (i < 0 || i >= items.Length || j < 0 || j >= items.Length)\n            throw new ArgumentOutOfRangeException("index out of range");\n        T tmp = items[i];\n        items[i] = items[j];\n        items[j] = tmp;\n    }\n    public static T[] Reversed<T>(T[] items)\n    {\n        if (items == null || items.Length == 0)\n            return new T[0];\n        // near-miss: reverses IN PLACE and returns the same array — the\n        // caller\'s data is silently mutated, breaking the new-array contract\n        for (int i = 0; i < items.Length / 2; i++)\n        {\n            T tmp = items[i];\n            items[i] = items[items.Length - 1 - i];\n            items[items.Length - 1 - i] = tmp;\n        }\n        return items;\n    }\n}\n',
        ),
        (
            "csb-p12-countif",
            'public class Solution\n{\n    public static int CountIf<T>(IEnumerable<T> items, Func<T, bool> predicate)\n    {\n        if (items == null) return 0;\n        int count = 0;\n        foreach (T item in items)\n        {\n            if (predicate(item)) count++;\n        }\n        return count;\n    }\n}\n',
            'public class Solution\n{\n    public static int CountIf<T>(IEnumerable<T> items, Func<T, bool> predicate)\n    {\n        if (items == null) return 0;\n        int count = 0;\n        foreach (T item in items)\n        {\n            // near-miss: inverted predicate — counts NON-matching elements\n            if (!predicate(item)) count++;\n        }\n        return count;\n    }\n}\n',
        ),
        (
            "csb-p12-pairstore",
            'public class Solution\n{\n    public sealed class PairStore<T>\n    {\n        private readonly List<T> items = new List<T>();\n        public int Count { get { return items.Count; } }\n        public void Add(T item) { items.Add(item); }\n        public T Get(int index)\n        {\n            if (index < 0 || index >= items.Count)\n                throw new ArgumentOutOfRangeException("index out of range");\n            return items[index];\n        }\n        public void Clear() { items.Clear(); }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class PairStore<T>\n    {\n        private readonly List<T> items = new List<T>();\n        public int Count { get { return items.Count; } }\n        public void Add(T item) { items.Add(item); }\n        public T Get(int index)\n        {\n            if (index < 0 || index >= items.Count)\n                throw new ArgumentOutOfRangeException("index out of range");\n            // near-miss: off-by-one — reads the slot AFTER the requested\n            // index, so Get(0) yields the second item\n            return items[index + 1];\n        }\n        public void Clear() { items.Clear(); }\n    }\n}\n',
        ),
        (
            "csb-p12-maxof",
            'public class Solution\n{\n    public static T MaxOf<T>(IEnumerable<T> items) where T : IComparable<T>\n    {\n        if (items == null)\n            throw new InvalidOperationException("no elements");\n        bool any = false;\n        T best = default;\n        foreach (T item in items)\n        {\n            if (!any) { best = item; any = true; }\n            else if (item.CompareTo(best) > 0) best = item;\n        }\n        if (!any)\n            throw new InvalidOperationException("no elements");\n        return best;\n    }\n}\n',
            'public class Solution\n{\n    public static T MaxOf<T>(IEnumerable<T> items) where T : IComparable<T>\n    {\n        if (items == null)\n            throw new InvalidOperationException("no elements");\n        bool any = false;\n        T best = default;\n        foreach (T item in items)\n        {\n            if (!any) { best = item; any = true; }\n            // near-miss: comparison flipped — returns the MINIMUM, not the\n            // maximum; a discriminating test catches it immediately\n            else if (item.CompareTo(best) < 0) best = item;\n        }\n        if (!any)\n            throw new InvalidOperationException("no elements");\n        return best;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m12",
    "Checkpoint — Generics",
    "A typed in-memory repository: add, get, remove, and a constraint-driven query — one class, every type.",
    20,
    r"""
## Checkpoint: the generic repository

**Task:** implement nested generic class `Solution.Repository<T> where T : IComparable<T>`:

1. `void Add(T item)` — appends.
2. `int Count { get; }`
3. `T Get(int index)` — `ArgumentOutOfRangeException` when out of range.
4. `bool Remove(T item)` — removes the first equal element; returns false when absent.
5. `T? Min()` — the smallest element; `InvalidOperationException` when empty.
6. `List<T> Sorted()` — a NEW list sorted ascending; the store's own order must not change.
""",
    "Checkpoint — Generics",
    "Một repository in-memory có kiểu: thêm, lấy, xóa, và truy vấn theo ràng buộc — một lớp, mọi kiểu.",
    r"""
## Checkpoint: repository generic

**Nhiệm vụ:** hiện thực lớp generic lồng `Solution.Repository<T> where T : IComparable<T>`:

1. `void Add(T item)` — thêm vào.
2. `int Count { get; }`
3. `T Get(int index)` — ném `ArgumentOutOfRangeException` khi ngoài khoảng.
4. `bool Remove(T item)` — xóa phần tử bằng nhau đầu tiên; trả false khi không có.
5. `T? Min()` — phần tử nhỏ nhất; ném `InvalidOperationException` khi rỗng.
6. `List<T> Sorted()` — một danh sách MỚI sắp tăng dần; thứ tự riêng của kho phải không đổi.
""",
    challenge(
        "csb-checkpoint-m12-task",
        "Repository",
        "Implement `Repository<T>` exactly as specified — bounds on Get, remove-by-value semantics, Min's empty contract, and Sorted's copy-not-mutate rule.",
        CS_PRELUDE,
        [
            (
                "lifecycle",
                "var r = new Solution.Repository<int>();\nr.Add(3);\nr.Add(1);\nr.Add(2);\nCj.Eq(r.Count, 3, \"three items\");\nCj.Eq(r.Get(1), 1, \"get by index\");\nCj.True(r.Remove(1), \"remove existing\");\nCj.False(r.Remove(99), \"remove absent\");\nCj.Eq(r.Count, 2, \"one removed\");",
                "Add/Count/Get/Remove form the basic lifecycle.",
            ),
            (
                "min-and-sorted",
                "var r = new Solution.Repository<int>();\nr.Add(3);\nr.Add(1);\nr.Add(2);\nCj.Eq(r.Min(), 1, \"min\");\nvar sorted = r.Sorted();\nCj.Eq(string.Join(\",\", sorted), \"1,2,3\", \"sorted copy\");\nCj.Eq(string.Join(\",\", new[] { r.Get(0), r.Get(1) }), \"3,1\", \"store order unchanged\");\nvar empty = new Solution.Repository<string>();\nbool t = false;\ntry { empty.Min(); } catch (InvalidOperationException) { t = true; }\nCj.True(t, \"empty Min throws\");",
                "Min works via the constraint; Sorted must copy — the store keeps insertion order.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Repository",
        "Hiện thực `Repository<T>` đúng như đặc tả — kiểm tra khoảng cho Get, ngữ nghĩa xóa-theo-giá-trị, hợp đồng rỗng của Min, và luật sao-chép-không-biến-đổi của Sorted.",
        [
            ("lifecycle", "Add/Count/Get/Remove tạo thành vòng đời cơ bản."),
            ("min-and-sorted", "Min hoạt động nhờ ràng buộc; Sorted phải sao chép — kho giữ thứ tự chèn."),
        ],
    ),
    solution='public class Solution\n{\n    public sealed class Repository<T> where T : IComparable<T>\n    {\n        private readonly List<T> items = new List<T>();\n        public int Count { get { return items.Count; } }\n        public void Add(T item) { items.Add(item); }\n        public T Get(int index)\n        {\n            if (index < 0 || index >= items.Count)\n                throw new ArgumentOutOfRangeException("index out of range");\n            return items[index];\n        }\n        public bool Remove(T item)\n        {\n            for (int i = 0; i < items.Count; i++)\n            {\n                if (EqualityComparer<T>.Default.Equals(items[i], item))\n                {\n                    items.RemoveAt(i);\n                    return true;\n                }\n            }\n            return false;\n        }\n        public T Min()\n        {\n            if (items.Count == 0)\n                throw new InvalidOperationException("empty");\n            T best = items[0];\n            foreach (T item in items)\n            {\n                if (item.CompareTo(best) < 0) best = item;\n            }\n            return best;\n        }\n        public List<T> Sorted()\n        {\n            var copy = new List<T>(items);\n            copy.Sort();\n            return copy;\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public sealed class Repository<T> where T : IComparable<T>\n    {\n        private readonly List<T> items = new List<T>();\n        public int Count { get { return items.Count; } }\n        public void Add(T item) { items.Add(item); }\n        public T Get(int index)\n        {\n            if (index < 0 || index >= items.Count)\n                throw new ArgumentOutOfRangeException("index out of range");\n            return items[index];\n        }\n        public bool Remove(T item)\n        {\n            for (int i = 0; i < items.Count; i++)\n            {\n                if (EqualityComparer<T>.Default.Equals(items[i], item))\n                {\n                    items.RemoveAt(i);\n                    return true;\n                }\n            }\n            return false;\n        }\n        public T Min()\n        {\n            if (items.Count == 0)\n                throw new InvalidOperationException("empty");\n            T best = items[0];\n            foreach (T item in items)\n            {\n                if (item.CompareTo(best) < 0) best = item;\n            }\n            return best;\n        }\n        public List<T> Sorted()\n        {\n            // near-miss: sorts the backing list in place — the store\'s\n            // insertion order is destroyed as a side effect\n            items.Sort();\n            return items;\n        }\n    }\n}\n',
)

print("module 12 authored")
