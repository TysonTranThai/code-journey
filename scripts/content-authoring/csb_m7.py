#!/usr/bin/env python3
"""C# — Beginner — Module 7: csb-arrays.

Arrays as fixed-size, typed blocks: declaration and iteration, bounds,
then Array.Sort/IndexOf and copying — with the aliasing trap as the
behavioral near-miss. House conventions: ISO boilerplate carries usings,
Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-arrays"

write_module(
    M,
    "Arrays",
    "Fixed-size, typed collections: declare, iterate, copy, search, and sort — plus the aliasing trap that starts every reference-type discussion.",
    "Mảng",
    "Tập hợp cố định, có kiểu: khai báo, duyệt, sao chép, tìm kiếm, sắp xếp — cùng bẫy aliasing mở đầu mọi cuộc thảo luận về kiểu tham chiếu.",
    ["csb-m7-declare", "csb-m7-iterate", "csb-m7-stdlib", "csb-checkpoint-m7"],
    ["csb-p7-arrays"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m7-declare",
    "Declaring arrays",
    "Fixed length, typed elements, one allocation — and what `new int[5]` really gives you.",
    13,
    r"""
## One block, many values

```csharp
int[] scores = new int[5];              // 5 zeros
int[] primes = { 2, 3, 5, 7, 11 };      // infer from initializer
string[] names = new[] { "an", "binh" };
```

An array is a **fixed-size** block of elements of one type. `new int[5]` allocates 5 elements and fills value-type arrays with the type's default (`0`, `false`); element-type arrays (`string[]`) fill with `null`. Length is chosen at creation and never changes — need more room later, you allocate a new array (Module 10's `List<T>` exists precisely for that).

## Indexing and bounds

```csharp
primes[0]      // 2 — first
primes[^1]     // 11 — last (hat counts from the end)
primes[5]      // throws IndexOutOfRangeException — valid indices are 0..4
```

The bounds check is real and immediate. Off-by-one errors (`<=` in a loop, `arr[arr.Length]`) are the classic crash; `Length` is the size, the last valid index is `Length - 1`.

## Reference semantics: the aliasing trap

```csharp
int[] a = { 1, 2, 3 };
int[] b = a;          // b is ANOTHER NAME for the same array
b[0] = 99;
Console.WriteLine(a[0]);   // 99 — a changed too
```

Arrays are **reference types**. Assignment copies the *reference*, not the elements — two variables pointing at one block. This is the model for classes (Module 11) met early, where it can hurt: pass an array to a method and the method can mutate your data. To get an independent copy: `a.Clone()`, `a.ToArray()` (LINQ), or copy in a loop.
""",
    "Khai báo mảng",
    "Độ dài cố định, phần tử có kiểu, một lần cấp phát — và `new int[5]` thực sự cho bạn gì.",
    r"""
## Một khối, nhiều giá trị

```csharp
int[] scores = new int[5];              // 5 số 0
int[] primes = { 2, 3, 5, 7, 11 };      // suy từ bộ khởi tạo
string[] names = new[] { "an", "binh" };
```

Một mảng là khối phần tử **cố định kích thước** cùng một kiểu. `new int[5]` cấp phát 5 phần tử và điền kiểu giá trị bằng mặc định của kiểu (`0`, `false`); mảng kiểu tham chiếu (`string[]`) điền bằng `null`. Độ dài được chọn lúc tạo và không bao giờ thay đổi — cần thêm chỗ, bạn cấp phát mảng mới (`List<T>` ở Module 10 tồn tại chính vì điều đó).

## Chỉ số và biên

```csharp
primes[0]      // 2 — đầu
primes[^1]     // 11 — cuối (mũ đếm từ cuối)
primes[5]      // ném IndexOutOfRangeException — chỉ số hợp lệ là 0..4
```

Việc kiểm tra biên là thật và tức thời. Lỗi lệch-một (`<=` trong vòng lặp, `arr[arr.Length]`) là crash kinh điển; `Length` là kích thước, chỉ số hợp lệ cuối là `Length - 1`.

## Ngữ nghĩa tham chiếu: bẫy aliasing

```csharp
int[] a = { 1, 2, 3 };
int[] b = a;          // b là TÊN KHÁC của cùng mảng
b[0] = 99;
Console.WriteLine(a[0]);   // 99 — a cũng đổi
```

Mảng là **kiểu tham chiếu**. Phép gán sao chép *tham chiếu*, không phải các phần tử — hai biến trỏ vào một khối. Đây là mô hình cho class (Module 11) gặp sớm, nơi nó có thể gây hại: đưa một mảng cho phương thức và phương thức có thể biến đổi dữ liệu của bạn. Để có bản sao độc lập: `a.Clone()`, `a.ToArray()` (LINQ), hoặc sao chép trong vòng lặp.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m7-iterate",
    "Iterating and accumulating",
    "for vs foreach, accumulation patterns, and the loop invariants behind min/max and counting.",
    13,
    r"""
## foreach: visit everything

```csharp
foreach (int p in primes)
    Console.WriteLine(p);
```

`foreach` walks every element in order, no index, no bounds risk. It cannot modify the array structure, and you don't get a position. When you need the position — `for`:

```csharp
for (int i = 0; i < primes.Length; i++)
    Console.WriteLine($"{i}: {primes[i]}");
```

Note `i < Length`, not `<=`. This loop shape appears in every challenge you'll ship.

## Accumulation: the four patterns

Almost every array exercise is one of these loops in disguise:

```csharp
int sum = 0;                    // 1. fold: one running value
foreach (int p in primes) sum += p;

int max = primes[0];            // 2. best-so-far
foreach (int p in primes) if (p > max) max = p;

int count = 0;                  // 3. counter with predicate
foreach (int p in primes) if (p % 2 == 0) count++;

int[] copy = new int[primes.Length];   // 4. transform
for (int i = 0; i < primes.Length; i++) copy[i] = primes[i] * 2;
```

The best-so-far loop assumes a non-empty array — on empty input `primes[0]` throws. Guard with `Length == 0` (or seed from `int.MinValue` when a sentinel is honest). These four shapes plus a guard clause cover min/max/average/count/filter/map — the entire Module 7 practice set is them, and LINQ (Module 17) later names them.
""",
    "Duyệt và tích lũy",
    "for hay foreach, các mẫu tích lũy, và bất biến vòng lặp đằng sau min/max và đếm.",
    r"""
## foreach: thăm mọi phần tử

```csharp
foreach (int p in primes)
    Console.WriteLine(p);
```

`foreach` đi qua từng phần tử theo thứ tự, không chỉ số, không rủi ro biên. Nó không thể thay đổi cấu trúc mảng, và bạn không có vị trí. Khi cần vị trí — dùng `for`:

```csharp
for (int i = 0; i < primes.Length; i++)
    Console.WriteLine($"{i}: {primes[i]}");
```

Chú ý `i < Length`, không phải `<=`. Dạng vòng lặp này xuất hiện trong mọi thử thách bạn sẽ làm.

## Tích lũy: bốn mẫu

Hầu hết mọi bài tập mảng là một trong các vòng lặp này cải trang:

```csharp
int sum = 0;                    // 1. gộp: một giá trị chạy dần
foreach (int p in primes) sum += p;

int max = primes[0];            // 2. tốt-nhất-tính-đến-nay
foreach (int p in primes) if (p > max) max = p;

int count = 0;                  // 3. bộ đếm với vị từ
foreach (int p in primes) if (p % 2 == 0) count++;

int[] copy = new int[primes.Length];   // 4. biến đổi
for (int i = 0; i < primes.Length; i++) copy[i] = primes[i] * 2;
```

Vòng best-so-far giả định mảng khác rỗng — với input rỗng `primes[0]` ném exception. Bảo vệ bằng `Length == 0` (hoặc khởi đầu từ `int.MinValue` khi giá trị cờ giả là trung thực). Bốn dạng này cộng một guard clause phủ min/max/trung bình/đếm/lọc/ánh xạ — toàn bộ bộ bài tập Module 7 là chúng, và LINQ (Module 17) sau này sẽ đặt tên cho chúng.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m7-stdlib",
    "Array helper methods",
    "Array.Sort, Array.IndexOf, Array.Reverse, CopyTo — what the standard library already wrote for you.",
    12,
    r"""
## Sorting in place

```csharp
int[] nums = { 5, 3, 9, 1 };
Array.Sort(nums);            // nums is now { 1, 3, 5, 9 }
Array.Reverse(nums);         // { 9, 5, 3, 1 }
```

`Array.Sort` mutates the array — **in place** — using an introsort; average O(n log n). There's no "sorted copy" overload; if you must keep the original, copy first (`(int[])nums.Clone()`). Strings sort with culture-aware comparison by default — for code-like ordering say `Array.Sort(names, StringComparer.Ordinal)`.

## Searching

```csharp
int at = Array.IndexOf(nums, 5);      // index or -1 when absent
bool has = Array.Exists(nums, n => n > 8);   // predicate search
int first = Array.Find(nums, n => n > 8);    // element or 0/""/null default
```

`IndexOf` returns **-1 when absent** — a sentinel you must check before indexing with it. The predicate family (`Exists`/`Find`/`FindAll`) takes a lambda; you met lambdas briefly, they get a full module later.

## Copying without aliasing

```csharp
int[] src = { 1, 2, 3, 4 };
int[] dst = new int[src.Length];
src.CopyTo(dst, 0);          // dst is independent
int[] head = new int[2];
src.CopyTo(head, 0);         // first two elements only
```

`CopyTo(target, startInTarget)` writes elements into an existing array (which must be long enough). Now aliasing and copying are two visible paths: `b = a` shares, `CopyTo`/`Clone` duplicates. Every time you hand an array to a method or store it in a field, ask: do I want the alias or a copy?
""",
    "Các phương thức trợ giúp mảng",
    "Array.Sort, Array.IndexOf, Array.Reverse, CopyTo — những gì thư viện chuẩn đã viết sẵn cho bạn.",
    r"""
## Sắp xếp tại chỗ

```csharp
int[] nums = { 5, 3, 9, 1 };
Array.Sort(nums);            // nums giờ là { 1, 3, 5, 9 }
Array.Reverse(nums);         // { 9, 5, 3, 1 }
```

`Array.Sort` biến đổi mảng — **tại chỗ** — bằng introsort; trung bình O(n log n). Không có overload "bản sao đã sắp"; nếu phải giữ bản gốc, sao chép trước (`(int[])nums.Clone()`). Chuỗi mặc định sắp theo so sánh phụ thuộc văn hóa — với thứ tự kiểu code hãy nói `Array.Sort(names, StringComparer.Ordinal)`.

## Tìm kiếm

```csharp
int at = Array.IndexOf(nums, 5);      // chỉ số hoặc -1 khi vắng
bool has = Array.Exists(nums, n => n > 8);   // tìm theo vị từ
int first = Array.Find(nums, n => n > 8);    // phần tử hoặc mặc định 0/""/null
```

`IndexOf` trả **-1 khi vắng** — một giá trị cờ bạn phải kiểm tra trước khi dùng làm chỉ số. Họ vị từ (`Exists`/`Find`/`FindAll`) nhận một lambda; bạn đã chạm qua lambda, sau này sẽ có nguyên một module.

## Sao chép không aliasing

```csharp
int[] src = { 1, 2, 3, 4 };
int[] dst = new int[src.Length];
src.CopyTo(dst, 0);          // dst độc lập
int[] head = new int[2];
src.CopyTo(head, 0);         // chỉ hai phần tử đầu
```

`CopyTo(target, startInTarget)` ghi các phần tử vào một mảng có sẵn (phải đủ dài). Giờ aliasing và sao chép là hai con đường nhìn thấy được: `b = a` chia sẻ, `CopyTo`/`Clone` nhân bản. Mỗi lần đưa mảng cho một phương thức hay lưu vào field, hãy hỏi: tôi muốn alias hay bản sao?
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p7-arrays",
    "Array workout",
    "The accumulation patterns under pressure: empty guards, ties, and a max-index scan done right.",
    "Luyện tập mảng",
    "Các mẫu tích lũy dưới áp lực: guard rỗng, hòa nhau, và quét max-index đúng cách.",
    "csb-m7-stdlib",
    38,
    "beginner",
    [
        challenge(
            "csb-p7-stats",
            "Array statistics",
            "Implement `static (int Max, int Min) Bounds(int[] values)` — the largest and smallest elements in one pass. Throw `ArgumentException` when the array is null or empty.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var b = Solution.Bounds(new[] {3, -1, 4, -1, 5});\nCj.Eq(b.Max, 5, \"max\");\nCj.Eq(b.Min, -1, \"min\");\nvar c = Solution.Bounds(new[] {7});\nCj.Eq(c.Max, 7, \"single max\");\nCj.Eq(c.Min, 7, \"single min\");",
                    "One pass can track both ends; a single element is both its own max and min.",
                ),
                (
                    "guards",
                    "bool t1 = false;\ntry { Solution.Bounds(null); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { Solution.Bounds(new int[0]); } catch (ArgumentException) { t2 = true; }\nCj.True(t1 && t2, \"null and empty throw\");",
                    "No data — no answer. Both must throw, not return a sentinel.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p7-maxindex",
            "Index of the maximum",
            "Implement `static int MaxIndex(int[] values)` — the **index** of the largest element. Ties resolve to the *first* occurrence. Null or empty returns -1.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.MaxIndex(new[] {2, 9, 4}), 1, \"middle max\");\nCj.Eq(Solution.MaxIndex(new[] {9, 9}), 0, \"tie picks first\");\nCj.Eq(Solution.MaxIndex(new[] {-5}), 0, \"single\");",
                    "The tie rule is the discriminator: the first occurrence wins.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.MaxIndex(null), -1, \"null\");\nCj.Eq(Solution.MaxIndex(new int[0]), -1, \"empty\");\nCj.Eq(Solution.MaxIndex(new[] {-8, -3, -3}), 1, \"first of tied maxima\");",
                    "-1 for no data (not 0 — 0 would be a lie for arrays whose max sits at index 0); negatives and ties together.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p7-rotate",
            "Rotate left",
            "Implement `static int[] RotateLeft(int[] values, int k)` — a NEW array with elements shifted left `k` positions, wrapping around. `RotateLeft({1,2,3,4,5}, 2)` is `{3,4,5,1,2}`. `k` larger than the length must still work; null input throws `ArgumentException`.",
            CS_PRELUDE,
            [
                (
                    "basic",
                    "var r = Solution.RotateLeft(new[] {1, 2, 3, 4, 5}, 2);\nCj.Eq(string.Join(\",\", r), \"3,4,5,1,2\", \"k=2\");\nvar z = Solution.RotateLeft(new[] {1, 2}, 0);\nCj.Eq(string.Join(\",\", z), \"1,2\", \"k=0\");",
                    "Wrap-around placement: target[(i - k mod n + n) mod n] = source[i].",
                ),
                (
                    "wrap-and-alias",
                    "var w = Solution.RotateLeft(new[] {1, 2, 3}, 7);\nCj.Eq(string.Join(\",\", w), \"2,3,1\", \"k > length wraps\");\nvar src = new[] {1, 2, 3};\nvar same = Solution.RotateLeft(src, 3);\nCj.Eq(string.Join(\",\", same), \"1,2,3\", \"k == length is identity\");\nsame[0] = 99;\nCj.Eq(src[0], 1, \"result is a copy, not an alias\");",
                    "k is taken modulo length; and the result must be independent — mutating it may not touch the input.",
                ),
            ],
            level="real-world",
        ),
        challenge(
            "csb-p7-reverse",
            "Reverse in place",
            "Implement `static void ReverseInPlace(int[] values)` — reverse the array **without allocating a new one** (two indices walking inward and swapping). Null must be tolerated silently.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var a = new[] {1, 2, 3, 4};\nSolution.ReverseInPlace(a);\nCj.Eq(string.Join(\",\", a), \"4,3,2,1\", \"even count\");\nvar b = new[] {1, 2, 3};\nSolution.ReverseInPlace(b);\nCj.Eq(string.Join(\",\", b), \"3,2,1\", \"odd count\");",
                    "The middle element of an odd-length array stays put.",
                ),
                (
                    "edges",
                    "var e = new[] {42};\nSolution.ReverseInPlace(e);\nCj.Eq(e[0], 42, \"single untouched\");\nint[] nothing = null;\nSolution.ReverseInPlace(nothing);   // must not throw\nCj.True(true, \"null tolerated\");",
                    "One-element and null inputs must not crash — the swap loop simply never runs.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p7-stats": vi_challenge(
            "Thống kê mảng",
            "Hiện thực `static (int Max, int Min) Bounds(int[] values)` — phần tử lớn nhất và nhỏ nhất trong một lượt duyệt. Ném `ArgumentException` khi mảng null hoặc rỗng.",
            [
                ("normal", "Một lượt duyệt theo dõi cả hai đầu; phần tử đơn là max lẫn min của chính nó."),
                ("guards", "Không có dữ liệu — không có câu trả lời. Cả hai phải ném, không trả giá trị cờ."),
            ],
        ),
        "csb-p7-maxindex": vi_challenge(
            "Chỉ số của giá trị lớn nhất",
            "Hiện thực `static int MaxIndex(int[] values)` — **chỉ số** của phần tử lớn nhất. Bằng nhau thì chọn lần *đầu tiên*. Null hoặc rỗng trả -1.",
            [
                ("normal", "Luật hòa là điểm phân biệt: lần xuất hiện đầu thắng."),
                ("edges", "-1 khi không có dữ liệu (không phải 0 — 0 sẽ là lời nói dối với mảng có max tại chỉ số 0); số âm và hòa cùng lúc."),
            ],
        ),
        "csb-p7-rotate": vi_challenge(
            "Xoay trái",
            "Hiện thực `static int[] RotateLeft(int[] values, int k)` — mảng MỚI với các phần tử dịch trái `k` vị trí, quay vòng. `RotateLeft({1,2,3,4,5}, 2)` là `{3,4,5,1,2}`. `k` lớn hơn độ dài vẫn phải chạy; input null ném `ArgumentException`.",
            [
                ("basic", "Vị trí quay vòng: target[(i - k mod n + n) mod n] = source[i]."),
                ("wrap-and-alias", "k lấy modulo độ dài; và kết quả phải độc lập — biến đổi nó không được chạm vào input."),
            ],
        ),
        "csb-p7-reverse": vi_challenge(
            "Đảo ngược tại chỗ",
            "Hiện thực `static void ReverseInPlace(int[] values)` — đảo ngược mảng **mà không cấp phát mảng mới** (hai chỉ số đi vào trong và hoán đổi). Null phải được chấp nhận im lặng.",
            [
                ("normal", "Phần tử giữa của mảng lẻ giữ nguyên vị trí."),
                ("edges", "Input một phần tử và null không được crash — vòng hoán đổi đơn giản là không chạy."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p7-stats",
            'public class Solution\n{\n    public static (int Max, int Min) Bounds(int[] values)\n    {\n        if (values == null || values.Length == 0)\n            throw new ArgumentException("no data");\n        int max = values[0], min = values[0];\n        for (int i = 1; i < values.Length; i++)\n        {\n            if (values[i] > max) max = values[i];\n            if (values[i] < min) min = values[i];\n        }\n        return (max, min);\n    }\n}\n',
            'public class Solution\n{\n    public static (int Max, int Min) Bounds(int[] values)\n    {\n        if (values == null || values.Length == 0)\n            throw new ArgumentException("no data");\n        int max = values[0], min = values[0];\n        for (int i = 1; i < values.Length; i++)\n        {\n            if (values[i] > max) max = values[i];\n            // near-miss: second branch uses > instead of < — min tracks max\n            if (values[i] > min) min = values[i];\n        }\n        return (max, min);\n    }\n}\n',
        ),
        (
            "csb-p7-maxindex",
            'public class Solution\n{\n    public static int MaxIndex(int[] values)\n    {\n        if (values == null || values.Length == 0) return -1;\n        int best = 0;\n        for (int i = 1; i < values.Length; i++)\n            if (values[i] > values[best]) best = i;   // strict > keeps first tie\n        return best;\n    }\n}\n',
            'public class Solution\n{\n    public static int MaxIndex(int[] values)\n    {\n        if (values == null || values.Length == 0) return -1;\n        int best = 0;\n        for (int i = 1; i < values.Length; i++)\n            // near-miss: >= — a later tie overwrites, breaking first-occurrence\n            if (values[i] >= values[best]) best = i;\n        return best;\n    }\n}\n',
        ),
        (
            "csb-p7-rotate",
            'public class Solution\n{\n    public static int[] RotateLeft(int[] values, int k)\n    {\n        if (values == null) throw new ArgumentException("null input");\n        int n = values.Length;\n        int[] result = new int[n];\n        for (int i = 0; i < n; i++)\n            result[(i - k % n + n) % n] = values[i];\n        return result;\n    }\n}\n',
            'public class Solution\n{\n    public static int[] RotateLeft(int[] values, int k)\n    {\n        if (values == null) throw new ArgumentException("null input");\n        int n = values.Length;\n        // near-miss: returns the input itself for k % n == 0 — an alias, so\n        // mutating the "result" corrupts the caller\'s array\n        if (k % n == 0) return values;\n        int[] result = new int[n];\n        for (int i = 0; i < n; i++)\n            result[(i - k % n + n) % n] = values[i];\n        return result;\n    }\n}\n',
        ),
        (
            "csb-p7-reverse",
            'public class Solution\n{\n    public static void ReverseInPlace(int[] values)\n    {\n        if (values == null) return;\n        for (int i = 0, j = values.Length - 1; i < j; i++, j--)\n        {\n            (values[i], values[j]) = (values[j], values[i]);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public static void ReverseInPlace(int[] values)\n    {\n        if (values == null) return;\n        // near-miss: looping the FULL length swaps each pair twice — the\n        // second pass undoes the first, so the array comes back unchanged\n        for (int i = 0; i < values.Length; i++)\n        {\n            (values[i], values[values.Length - 1 - i]) = (values[values.Length - 1 - i], values[i]);\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m7",
    "Checkpoint — Arrays",
    "A moving average and a palindrome probe: transform loops and in-place two-pointer work.",
    20,
    r"""
## Checkpoint: signal tools

**Task:** implement two methods:

1. `static double[] MovingAverage(int[] readings, int window)` — the average of each contiguous `window`-sized slice: `results[i]` is the mean of `readings[i..i+window]`. The result has `readings.Length - window + 1` entries; when that count is ≤ 0 (window bigger than the input) return an empty array. `window` must be ≥ 1 or throw `ArgumentException`.
2. `static bool IsPalindrome(int[] values)` — true when the array reads the same forwards and backwards (compare element `i` with element `Length-1-i`, no new array). Null is **not** a palindrome; empty **is**.
""",
    "Checkpoint — Mảng",
    "Trung bình trượt và thăm dò palindrome: vòng biến đổi và công việc hai con trỏ tại chỗ.",
    r"""
## Checkpoint: công cụ tín hiệu

**Nhiệm vụ:** hiện thực hai phương thức:

1. `static double[] MovingAverage(int[] readings, int window)` — trung bình của mỗi lát liên tiếp cỡ `window`: `results[i]` là trung bình của `readings[i..i+window]`. Kết quả có `readings.Length - window + 1` phần tử; khi số đó ≤ 0 (window lớn hơn input) trả mảng rỗng. `window` phải ≥ 1 hoặc ném `ArgumentException`.
2. `static bool IsPalindrome(int[] values)` — true khi mảng đọc xuôi bằng đọc ngược (so phần tử `i` với `Length-1-i`, không tạo mảng mới). Null **không phải** palindrome; rỗng **có**.
""",
    challenge(
        "csb-checkpoint-m7-task",
        "Signal tools",
        "Implement `MovingAverage` and `IsPalindrome` as described. Watch the window contract (≥1 or throw; result length is Length - window + 1) and the palindrome null/empty distinction.",
        CS_PRELUDE,
        [
            (
                "moving-average",
                'var m = Solution.MovingAverage(new[] {1, 2, 3, 4}, 2);\nCj.Eq(m.Length, 3, "three windows");\nCj.Near(m[0], 1.5, 1e-9, "first");\nCj.Near(m[2], 3.5, 1e-9, "last");\nCj.Eq(Solution.MovingAverage(new[] {5}, 3).Length, 0, "window too big");\nbool threw = false;\ntry { Solution.MovingAverage(new[] {1, 2}, 0); } catch (ArgumentException) { threw = true; }\nCj.True(threw, "window 0 throws");',
                "Length contract, exact window means, the too-big-window rule, and the guard.",
            ),
            (
                "palindrome",
                'Cj.True(Solution.IsPalindrome(new[] {1, 2, 1}), "odd palindrome");\nCj.True(Solution.IsPalindrome(new[] {1, 2, 2, 1}), "even palindrome");\nCj.False(Solution.IsPalindrome(new[] {1, 2, 3}), "not palindrome");\nCj.True(Solution.IsPalindrome(new int[0]), "empty IS");\nCj.False(Solution.IsPalindrome(null), "null is NOT");',
                "The null/empty asymmetry is the trap: empty is trivially a palindrome, null is no data at all.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Công cụ tín hiệu",
        "Hiện thực `MovingAverage` và `IsPalindrome` như mô tả. Chú ý hợp đồng window (≥1 hoặc ném; độ dài kết quả là Length - window + 1) và phân biệt null/rỗng của palindrome.",
        [
            ("moving-average", "Hợp đồng độ dài, trung bình cửa sổ chính xác, luật window-qua-lớn, và guard."),
            ("palindrome", "Bất đối xứng null/rỗng là cái bẫy: rỗng hiển nhiên là palindrome, null là không có dữ liệu."),
        ],
    ),
    solution='public class Solution\n{\n    public static double[] MovingAverage(int[] readings, int window)\n    {\n        if (window < 1) throw new ArgumentException("window must be >= 1");\n        if (readings == null) throw new ArgumentException("null readings");\n        int n = readings.Length - window + 1;\n        if (n <= 0) return new double[0];\n        var result = new double[n];\n        for (int i = 0; i < n; i++)\n        {\n            long sum = 0;\n            for (int j = i; j < i + window; j++) sum += readings[j];\n            result[i] = (double)sum / window;\n        }\n        return result;\n    }\n\n    public static bool IsPalindrome(int[] values)\n    {\n        if (values == null) return false;\n        for (int i = 0, j = values.Length - 1; i < j; i++, j--)\n            if (values[i] != values[j]) return false;\n        return true;\n    }\n}\n',
    wrong='public class Solution\n{\n    public static double[] MovingAverage(int[] readings, int window)\n    {\n        if (window < 1) throw new ArgumentException("window must be >= 1");\n        if (readings == null) throw new ArgumentException("null readings");\n        int n = readings.Length - window + 1;\n        if (n <= 0) return new double[0];\n        var result = new double[n];\n        for (int i = 0; i < n; i++)\n        {\n            long sum = 0;\n            // near-miss: j <= i + window reads one element past the window —\n            // for the last window this walks off the array and throws\n            for (int j = i; j <= i + window; j++) sum += readings[j];\n            result[i] = (double)sum / window;\n        }\n        return result;\n    }\n\n    public static bool IsPalindrome(int[] values)\n    {\n        // near-miss: null treated as palindrome — the contract says false\n        if (values == null) return true;\n        for (int i = 0, j = values.Length - 1; i < j; i++, j--)\n            if (values[i] != values[j]) return false;\n        return true;\n    }\n}\n',
)

print("module 7 authored")
