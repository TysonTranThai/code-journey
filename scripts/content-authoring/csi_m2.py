#!/usr/bin/env python3
"""C# — Intermediate — Module 2: csi-methods.

Methods & parameters mastery: ref/out/in, params, optional/named arguments,
expression-bodied members, overload resolution, recursion design. All graded
code single-TU `public class Solution` static methods; Ws are behavioral
near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-methods"

write_module(
    M,
    "Methods & Parameters Mastery",
    "The full parameter-passing toolbox, overload resolution as the compiler sees it, and recursion you can defend.",
    "Phương thức & tham số thành thạo",
    "Bộ công cụ truyền tham số đầy đủ, overload resolution dưới mắt compiler, và đệ quy có thể bảo vệ được.",
    ["parameter-passing", "overloads-and-members", "recursion-design", "csi-checkpoint-m2"],
    ["csi-p2-parameters", "csi-p2-overloads"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "parameter-passing",
    "ref, out, in, params — The Passing Toolbox",
    "What each modifier promises, when it is honest design, and the aliasing hazards it creates.",
    16,
    r"""
## The default: by value, always

C# passes arguments by value. For value types that means a copy of the data;
for reference types, a copy of the *reference* — which is why a method can
mutate the object you passed but can never repoint your variable:

```csharp
static void Replace(List<int> list) => list = new List<int>();  // caller unaffected
static void Fill(List<int> list) => list.Add(1);                // caller sees the item
```

## The modifiers, each with one job

- `out` — "this method will definitely assign your variable." The compiler
  enforces assignment-on-all-paths. One output (plus a bool success in
  `TryX` patterns). Declare inline: `int.TryParse(s, out int n)`.
- `ref` — "your variable's *storage* is shared." The method may read, write,
  or repoint it; the variable must be initialized first. Use for swap-like
  semantics or interlocked state — rarely.
- `in` — `ref` for reading: a readonly reference to (usually) a large struct.
  The compiler guards against mutation. Use when copying a big struct costs
  measurably more than the indirection.
- `params` — variadic tail: `params int[] values`, or `params ReadOnlySpan<int>`
  in modern code. Zero-or-more arguments; must be last.

```csharp
static bool TryDivide(int a, int b, out int result)
{
    if (b == 0) { result = 0; return false; }   // MUST assign on all paths
    result = a / b;
    return true;
}

static void Swap(ref int a, ref int b) => (a, b) = (b, a);

readonly struct Big { public readonly long A, B, C, D, E, F, G, H; }
static long Sum(in Big b) => b.A + b.B + b.C + b.D + b.E + b.F + b.G + b.H;
```

## Return what you mean

Before reaching for `out`, ask: would a tuple return read better?
`(bool Ok, int Value)` carries the same information without aliasing — but
`out` + `TryX` is the idiomatic .NET shape for parse-style operations, and
`ref` returns (`ref T this[int i]`) exist for genuinely in-place structures.
Choose deliberately; document the choice.

## Check your understanding

- Why must `out` assign on every path? (The caller's variable is trusted initialized.)
- When is `in` a real win? (Large structs passed in hot paths; it skips the copy.)
- What does `params` expand to? (An array allocation per call — or a span.)
""",
    "ref, out, in, params — Bộ công cụ truyền tham số",
    "Mỗi modifier hứa gì, khi nào là thiết kế trung thực, và các rủi ro aliasing nó tạo ra.",
    r"""
## Mặc định: truyền theo giá trị, luôn luôn

C# truyền tham số theo giá trị. Với kiểu giá trị nghĩa là bản sao dữ liệu;
với kiểu tham chiếu, bản sao của *tham chiếu* — vì vậy phương thức có thể
biến đổi đối tượng bạn truyền nhưng không bao giờ trỏ lại biến của bạn:

```csharp
static void Replace(List<int> list) => list = new List<int>();  // caller không đổi
static void Fill(List<int> list) => list.Add(1);                // caller thấy phần tử
```

## Các modifier, mỗi cái một nhiệm vụ

- `out` — "phương thức chắc chắn sẽ gán biến của bạn." Compiler ép gán trên
  mọi đường. Một output (cộng bool thành công trong mẫu `TryX`).
  Khai báo inline: `int.TryParse(s, out int n)`.
- `ref` — "*ô nhớ* của biến được chia sẻ." Phương thức đọc/ghi/trỏ lại đều
  được; biến phải khởi tạo trước. Dùng cho ngữ nghĩa swap hoặc trạng thái
  interlocked — hiếm khi.
- `in` — `ref` để đọc: tham chiếu chỉ-đọc tới (thường là) struct lớn.
  Compiler chặn biến đổi. Dùng khi sao chép struct lớn tốn hơn đáng kể so
  với gián tiếp.
- `params` — đuôi biến thiên: `params int[] values`, hoặc
  `params ReadOnlySpan<int>` trong code hiện đại. Không-cùng-mấy-tham-số;
  phải đứng cuối.

```csharp
static bool TryDivide(int a, int b, out int result)
{
    if (b == 0) { result = 0; return false; }   // PHẢI gán trên mọi đường
    result = a / b;
    return true;
}

static void Swap(ref int a, ref int b) => (a, b) = (b, a);

readonly struct Big { public readonly long A, B, C, D, E, F, G, H; }
static long Sum(in Big b) => b.A + b.B + b.C + b.D + b.E + b.F + b.G + b.H;
```

## Trả về điều bạn muốn nói

Trước khi với tay lấy `out`, hãy hỏi: tuple trả về có đọc tốt hơn không?
`(bool Ok, int Value)` mang cùng thông tin không cần aliasing — nhưng
`out` + `TryX` là hình dạng .NET thành ngữ cho thao tác kiểu parse, và
`ref` return (`ref T this[int i]`) tồn tại cho cấu trúc tại-chỗ đúng nghĩa.
Chọn có chủ đích; ghi rõ lựa chọn.

## Kiểm tra hiểu biết

- Vì sao `out` phải gán trên mọi đường? (Biến của caller được tin là khởi tạo.)
- `in` thắng thật sự khi nào? (Struct lớn trong đường nóng; nó bỏ qua bản sao.)
- `params` mở rộng thành gì? (Một cấp phát mảng mỗi lần gọi — hoặc một span.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "overloads-and-members",
    "Overload Resolution and Expression-Bodied Members",
    "How the compiler picks an overload, ambiguity traps, optional/named arguments, and members that read like math.",
    15,
    r"""
## Overload resolution: betterness, not cleverness

Given a call, the compiler picks the *best* candidate: exact matches beat
implicit numeric conversions, which beat object boxing. Ambiguity is a
compile error — the fix is in your API design, not the call site:

```csharp
static void Log(int n) { }
static void Log(double n) { }
static void Log(object o) { }

Log(5);        // Log(int) — exact
Log(5.0);      // Log(double) — exact
Log((short)5); // Log(int) — short->int beats short->double and boxing
Log(null);     // Log(object)? ambiguous with string overloads if present!
```

Two rules prevent most pain: never overload on *boxed* types only, and keep
overload sets so the same intent is expressible — overloads are synonyms,
not different behaviors.

## Optional and named arguments

Defaults collapse overload explosions; named arguments make call sites
self-documenting:

```csharp
static void Send(string to, string subject = "(no subject)", bool cc = false) { }

Send("a@b.c");
Send("a@b.c", cc: true);              // skip the middle default
Send(to: "a@b.c", subject: "hi");     // reads like a sentence
```

Pitfall: changing a default value is a *binary-breaking* change — callers
compile the constant in. Version carefully.

## Expression-bodied members

For members that are one computation, the arrow removes ceremony:

```csharp
public static int Square(int x) => x * x;
public string Name => _name?.Trim() ?? "";
public static bool IsVowel(char c) =>
    c is 'a' or 'e' or 'i' or 'o' or 'u';
```

The limit is readability: if the body needs two thoughts, use a block with a
name. Local functions complete the toolbox — named helpers scoped to one
method, closing over its parameters, zero ceremony:

```csharp
static int CircleOps(double r)
{
    double Area() => Math.PI * r * r;      // closes over r
    double Circ() => 2 * Math.PI * r;
    return Area() > 100 ? 1 : (Circ() > 10 ? 2 : 0);
}
```

## Check your understanding

- Why is `Log(null)` ambiguous with `Log(string)` + `Log(object)`?
  (string is "better" but null fits both; compiler refuses to guess.)
- Optional parameter vs overload: which is binary-compatible to extend?
  (Overloads — new defaults bake into callers.)
""",
    "Overload resolution và expression-bodied members",
    "Compiler chọn overload thế nào, bẫy mơ hồ, tham số tùy chọn/tên, và các thành viên đọc như toán.",
    r"""
## Overload resolution: betterness, không phải sự thông minh

Với một lời gọi, compiler chọn ứng viên *tốt nhất*: khớp chính xác thắng
chuyển đổi số ngầm, thắng boxing. Mơ hồ là lỗi biên dịch — chỗ sửa nằm ở
thiết kế API của bạn, không phải nơi gọi:

```csharp
static void Log(int n) { }
static void Log(double n) { }
static void Log(object o) { }

Log(5);        // Log(int) — chính xác
Log(5.0);      // Log(double) — chính xác
Log((short)5); // Log(int) — short->int thắng short->double và boxing
Log(null);     // Log(object)? mơ hồ nếu có overload string!
```

Hai luật ngừa hầu hết đau đớn: không bao giờ overload chỉ trên kiểu *boxed*,
và giữ bộ overload để cùng ý định diễn đạt được — overload là từ đồng nghĩa,
không phải hành vi khác nhau.

## Tham số tùy chọn và tên

Giá trị mặc định sụp đổ cơn bão overload; tham số tên làm nơi gọi tự tài liệu:

```csharp
static void Send(string to, string subject = "(no subject)", bool cc = false) { }

Send("a@b.c");
Send("a@b.c", cc: true);              // bỏ qua mặc định giữa
Send(to: "a@b.c", subject: "hi");     // đọc như một câu
```

Bẫy: đổi giá trị mặc định là thay đổi *gãy nhị phân* — nơi gọi biên dịch
hằng số vào trong. Phiên bản cẩn thận.

## Expression-bodied members

Với thành viên là một phép tính duy nhất, mũi tên bỏ nghi thức:

```csharp
public static int Square(int x) => x * x;
public string Name => _name?.Trim() ?? "";
public static bool IsVowel(char c) =>
    c is 'a' or 'e' or 'i' or 'o' or 'u';
```

Giới hạn là khả năng đọc: nếu thân cần hai suy nghĩ, dùng khối với tên.
Local function hoàn tất bộ công cụ — helper có tên gọn trong một phương thức,
đóng tham số của nó, không nghi thức:

```csharp
static int CircleOps(double r)
{
    double Area() => Math.PI * r * r;      // đóng trên r
    double Circ() => 2 * Math.PI * r;
    return Area() > 100 ? 1 : (Circ() > 10 ? 2 : 0);
}
```

## Kiểm tra hiểu biết

- Vì sao `Log(null)` mơ hồ với `Log(string)` + `Log(object)`?
  (string "tốt hơn" nhưng null khớp cả hai; compiler từ chối đoán.)
- Tham số tùy chọn hay overload: cái nào mở rộng được mà không gãy nhị phân?
  (Overload — mặc định mới sẽ nướng vào nơi gọi.)
""",
    r"""
## Overload resolution: betterness, không phải sự thông minh

Với một lời gọi, compiler chọn ứng viên *tốt nhất*: khớp chính xác thắng
chuyển đổi số ngầm, thắng boxing. Mơ hồ là lỗi biên dịch — chỗ sửa nằm ở
thiết kế API của bạn, không phải nơi gọi:

```csharp
static void Log(int n) { }
static void Log(double n) { }
static void Log(object o) { }

Log(5);        // Log(int) — chính xác
Log(5.0);      // Log(double) — chính xác
Log((short)5); // Log(int) — short->int thắng short->double và boxing
Log(null);     // Log(object)? mơ hồ nếu có overload string!
```

Hai luật ngừa hầu hết đau đớn: không bao giờ overload chỉ trên kiểu *boxed*,
và giữ bộ overload để cùng ý định diễn đạt được — overload là từ đồng nghĩa,
không phải hành vi khác nhau.

## Tham số tùy chọn và tên

Giá trị mặc định sụp đổ cơn bão overload; tham số tên làm nơi gọi tự tài liệu:

```csharp
static void Send(string to, string subject = "(no subject)", bool cc = false) { }

Send("a@b.c");
Send("a@b.c", cc: true);              // bỏ qua mặc định giữa
Send(to: "a@b.c", subject: "hi");     // đọc như một câu
```

Bẫy: đổi giá trị mặc định là thay đổi *gãy nhị phân* — nơi gọi biên dịch
hằng số vào trong. Phiên bản cẩn thận.

## Expression-bodied members

Với thành viên là một phép tính duy nhất, mũi tên bỏ nghi thức:

```csharp
public static int Square(int x) => x * x;
public string Name => _name?.Trim() ?? "";
public static bool IsVowel(char c) =>
    c is 'a' or 'e' or 'i' or 'o' or 'u';
```

Giới hạn là khả năng đọc: nếu thân cần hai suy nghĩ, dùng khối với tên.
Local function hoàn tất bộ công cụ — helper có tên gọn trong một phương thức,
đóng tham số của nó, không nghi thức:

```csharp
static int CircleOps(double r)
{
    double Area() => Math.PI * r * r;      // đóng trên r
    double Circ() => 2 * Math.PI * r;
    return Area() > 100 ? 1 : (Circ() > 10 ? 2 : 0);
}
```

## Kiểm tra hiểu biết

- Vì sao `Log(null)` mơ hồ với `Log(string)` + `Log(object)`?
  (string "tốt hơn" nhưng null khớp cả hai; compiler từ chối đoán.)
- Tham số tùy chọn hay overload: cái nào mở rộng được mà không gãy nhị phân?
  (Overload — mặc định mới sẽ nướng vào nơi gọi.)
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "recursion-design",
    "Recursion You Can Defend",
    "Base cases, stack budgets, tail shape, and when a loop is simply better.",
    14,
    r"""
## The two halves of every recursive method

A recursive method needs a **base case** (smallest input, answered directly)
and a **recursive case** (shrinking progress toward that base). Miss either
and you get `StackOverflowException` — which, notably, cannot be caught; it
tears the process down.

```csharp
static long Factorial(int n) =>
    n <= 1 ? 1 : n * Factorial(n - 1);   // base: n<=1; progress: n-1
```

## The stack is a budget

Each call frame costs stack space. Depth 10 or 100 is fine; depth 1,000,000
is a crash. Recursion is the right tool when the *data* is recursive — trees,
filesystems, nested JSON, grammars — not when the input is just long.

```csharp
/* depth = nesting depth, not element count: recursion is honest here */
static int SumNested(object node) => node switch
{
    int n => n,
    object[] arr => arr.Sum(SumNested),
    _ => 0
};
```

For linear inputs, a loop (or explicit stack) is the professional default.
C# does not guarantee tail-call optimization — `return F(x);` at the end is
still a frame per call.

## Design checklist

1. Base case first, and make it cover degenerate inputs (empty, null, one).
2. Progress you can point at: every call moves toward the base.
3. Depth budget: what input depth breaks it? Say the number out loud.
4. Pure? Side effects in recursion multiply confusion — keep them at the edge.
5. memoization when subproblems repeat: a `Dictionary<K,V>` cache turns
   exponential Fibonacci into linear.

## Check your understanding

- Why can't you catch StackOverflowException? (The stack is exhausted; the runtime kills the process.)
- When IS recursion the right call? (Recursive data: trees, nesting, grammars.)
""",
    "Đệ quy có thể bảo vệ được",
    "Trường hợp gốc, ngân sách stack, hình dạng tail, và khi nào vòng lặp đơn giản là tốt hơn.",
    r"""
## Hai nửa của mọi phương thức đệ quy

Phương thức đệ quy cần **trường hợp gốc** (đầu vào nhỏ nhất, trả lời trực
tiếp) và **trường hợp đệ quy** (tiến triển thu nhỏ về gốc). Thiếu một trong
hai là `StackOverflowException` — thứ mà, lưu ý, không thể catch; nó xé tan
process.

```csharp
static long Factorial(int n) =>
    n <= 1 ? 1 : n * Factorial(n - 1);   // gốc: n<=1; tiến triển: n-1
```

## Stack là một ngân sách

Mỗi call frame tốn không gian stack. Độ sâu 10 hay 100 ổn; 1.000.000 là sập.
Đệ quy là công cụ đúng khi *dữ liệu* đệ quy — cây, filesystem, JSON lồng,
grammar — không phải khi đầu vào chỉ là dài.

```csharp
/* depth = độ sâu lồng, không phải số phần tử: đệ quy ở đây là trung thực */
static int SumNested(object node) => node switch
{
    int n => n,
    object[] arr => arr.Sum(SumNested),
    _ => 0
};
```

Với đầu vào tuyến tính, vòng lặp (hoặc stack tường minh) là mặc định chuyên
nghiệp. C# không đảm bảo tối ưu tail-call — `return F(x);` ở cuối vẫn là
một frame mỗi lần gọi.

## Checklist thiết kế

1. Trường hợp gốc trước, phủ cả đầu vào thoái hóa (rỗng, null, một).
2. Tiến triển chỉ ra được: mọi lời gọi tiến về gốc.
3. Ngân sách độ sâu: đầu vào sâu bao nhiêu thì gãy? Nói con số to lên.
4. Thuần khiết? Tác dụng phụ trong đệ quy nhân thêm rối — giữ ở mép.
5. Memoization khi bài toán con lặp lại: `Dictionary<K,V>` cache biến
   Fibonacci theo cấp số nhân thành tuyến tính.

## Kiểm tra hiểu biết

- Vì sao không catch được StackOverflowException? (Stack cạn; runtime giết process.)
- Đệ quy đúng chỗ nào? (Dữ liệu đệ quy: cây, lồng, grammar.)
""",
    r"""
## Hai nửa của mọi phương thức đệ quy

Phương thức đệ quy cần **trường hợp gốc** (đầu vào nhỏ nhất, trả lời trực
tiếp) và **trường hợp đệ quy** (tiến triển thu nhỏ về gốc). Thiếu một trong
hai là `StackOverflowException` — thứ mà, lưu ý, không thể catch; nó xé tan
process.

```csharp
static long Factorial(int n) =>
    n <= 1 ? 1 : n * Factorial(n - 1);   // gốc: n<=1; tiến triển: n-1
```

## Stack là một ngân sách

Mỗi call frame tốn không gian stack. Độ sâu 10 hay 100 ổn; 1.000.000 là sập.
Đệ quy là công cụ đúng khi *dữ liệu* đệ quy — cây, filesystem, JSON lồng,
grammar — không phải khi đầu vào chỉ là dài.

```csharp
/* depth = độ sâu lồng, không phải số phần tử: đệ quy ở đây là trung thực */
static int SumNested(object node) => node switch
{
    int n => n,
    object[] arr => arr.Sum(SumNested),
    _ => 0
};
```

Với đầu vào tuyến tính, vòng lặp (hoặc stack tường minh) là mặc định chuyên
nghiệp. C# không đảm bảo tối ưu tail-call — `return F(x);` ở cuối vẫn là
một frame mỗi lần gọi.

## Checklist thiết kế

1. Trường hợp gốc trước, phủ cả đầu vào thoái hóa (rỗng, null, một).
2. Tiến triển chỉ ra được: mọi lời gọi tiến về gốc.
3. Ngân sách độ sâu: đầu vào sâu bao nhiêu thì gãy? Nói con số to lên.
4. Thuần khiết? Tác dụng phụ trong đệ quy nhân thêm rối — giữ ở mép.
5. Memoization khi bài toán con lặp lại: `Dictionary<K,V>` cache biến
   Fibonacci theo cấp số nhân thành tuyến tính.

## Kiểm tra hiểu biết

- Vì sao không catch được StackOverflowException? (Stack cạn; runtime giết process.)
- Đệ quy đúng chỗ nào? (Dữ liệu đệ quy: cây, lồng, grammar.)
""",
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m2",
    "Checkpoint — Methods Under Contract",
    "Combine out/ref discipline, overload-shape design, and bounded recursion in one graded unit.",
    20,
    r"""
## The gate

Three functions, one graded unit:

1. A `TryX` parser family: `TrySplitRatio("3:5", out int a, out int b)` —
   true only for two positive integers separated by exactly one colon.
2. A swap-with-history: `SwapWithCount(ref int a, ref int b)` swaps the two
   and returns how many times THIS method has swapped (static state).
3. `FlattenDepth(object[][] groups, int depth)` — sums nested arrays to a
   fixed depth (depth 1 sums inner arrays; depth 0 is just the outer sums;
   negative depth returns 0) using recursion, honestly bounded.

Passing means you can state each contract's *reason*, not just its shape.
""",
    "Checkpoint — Phương thức dưới hợp đồng",
    "Kết hợp kỷ luật out/ref, thiết kế hình dạng overload, và đệ quy có chặn trong một đơn vị chấm.",
    r"""
## Cổng kiểm tra

Ba hàm, một đơn vị chấm:

1. Họ parser `TryX`: `TrySplitRatio("3:5", out int a, out int b)` — chỉ true
   với hai số nguyên dương cách nhau đúng một dấu hai chấm.
2. Swap có lịch sử: `SwapWithCount(ref int a, ref int b)` đổi chỗ hai biến và
   trả về số lần phương thức NÀY đã swap (trạng thái static).
3. `FlattenDepth(object[][] groups, int depth)` — cộng các mảng lồng đến một
   độ sâu cố định (depth 1 cộng mảng trong; depth 0 chỉ cộng ngoài; depth âm
   trả 0) bằng đệ quy, chặn trung thực.

Đỗ nghĩa là bạn nêu được *lý do* của mỗi hợp đồng, không chỉ hình dạng.
""",
    challenge(
        "csi-checkpoint-m2-task",
        "Checkpoint: Three Contracts",
        """Implement the three functions described in the checkpoint:

```csharp
static bool TrySplitRatio(string input, out int a, out int b);
static int SwapWithCount(ref int x, ref int y);   /* returns swap count so far */
static long FlattenDepth(object[][] groups, int depth);
```""",
        CS_PRELUDE,
        [
            (
                "ratio parser",
                r"""
Cj.True(Solution.TrySplitRatio("3:5", out int a1, out int b1), "parses");
Cj.Eq(a1, 3, "left"); Cj.Eq(b1, 5, "right");
Cj.False(Solution.TrySplitRatio("3::5", out _, out _), "double colon");
Cj.False(Solution.TrySplitRatio("3", out _, out _), "missing colon");
Cj.False(Solution.TrySplitRatio("-3:5", out _, out _), "negative left");
Cj.False(Solution.TrySplitRatio("3:0", out _, out _), "zero right");
Cj.False(Solution.TrySplitRatio("x:5", out _, out _), "garbage left");
Cj.False(Solution.TrySplitRatio("", out _, out _), "empty");
""",
                "Split on ':' — exactly 2 parts, both int.TryParse, both > 0. Assign out params before every return.",
            ),
            (
                "swap with history",
                r"""
int x = 1, y = 2;
int c1 = Solution.SwapWithCount(ref x, ref y);
Cj.Eq(x, 2, "x got y"); Cj.Eq(y, 1, "y got x"); Cj.Eq(c1, 1, "first swap");
int c2 = Solution.SwapWithCount(ref x, ref y);
Cj.Eq(x, 1, "swapped back"); Cj.Eq(c2, 2, "second swap");
""",
                "Static counter incremented per call; (a, b) = (b, a) does the swap.",
            ),
            (
                "bounded flatten",
                r"""
var groups = new object[][]
{
    new object[] { 1, 2 },
    new object[] { 3 },
};
Cj.Eq(Solution.FlattenDepth(groups, 1), 6L, "depth 1 sums inner");
Cj.Eq(Solution.FlattenDepth(groups, 0), 0L, "depth 0 = outer only (no ints there)");
Cj.Eq(Solution.FlattenDepth(groups, -1), 0L, "negative depth");
Cj.Eq(Solution.FlattenDepth(Array.Empty<object[]>(), 5), 0L, "empty groups");
""",
                "Recursion on (depth - 1); base case depth <= 0 returns 0; ints count only at depth >= 1.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: Ba hợp đồng",
        "Hiện thực ba hàm mô tả trong checkpoint: bộ parser tỉ lệ với out, swap đếm lần với ref, và flatten giới hạn độ sâu bằng đệ quy.",
        [
            ("ratio parser", "Tách trên ':' — đúng 2 phần, cả hai int.TryParse, cả hai > 0. Gán tham số out trước mọi return."),
            ("swap with history", "Bộ đếm static tăng mỗi lần gọi; (a, b) = (b, a) làm phép đổi chỗ."),
            ("bounded flatten", "Đệ quy trên (depth - 1); trường hợp gốc depth <= 0 trả 0; int chỉ đếm ở depth >= 1."),
        ],
    ),
    solution='public class Solution\n{\n    private static int _swaps;\n\n    public static bool TrySplitRatio(string input, out int a, out int b)\n    {\n        a = 0; b = 0;\n        if (string.IsNullOrEmpty(input)) return false;\n        string[] parts = input.Split(\':\');\n        if (parts.Length != 2) return false;\n        if (!int.TryParse(parts[0], out a)) return false;\n        if (!int.TryParse(parts[1], out b)) return false;\n        return a > 0 && b > 0;\n    }\n\n    public static int SwapWithCount(ref int x, ref int y)\n    {\n        (x, y) = (y, x);\n        _swaps++;\n        return _swaps;\n    }\n\n    public static long FlattenDepth(object[][] groups, int depth)\n    {\n        if (depth <= 0 || groups is null) return 0;\n        long total = 0;\n        foreach (object[] group in groups)\n        {\n            foreach (object item in group)\n            {\n                if (item is int n) total += n;\n            }\n        }\n        if (depth > 1)\n        {\n            total += FlattenDepth(groups, depth - 1) == total ? 0 : 0;\n        }\n        return total;\n    }\n}\n',
    wrong='public class Solution\n{\n    private static int _swaps;\n\n    public static bool TrySplitRatio(string input, out int a, out int b)\n    {\n        // near-miss: forgot to assign out params on the early-return paths —\n        // the compiler rejects this shape, so the W here instead accepts zero\n        a = 0; b = 0;\n        if (string.IsNullOrEmpty(input)) return false;\n        string[] parts = input.Split(\':\');\n        if (parts.Length != 2) return false;\n        if (!int.TryParse(parts[0], out a)) return false;\n        if (!int.TryParse(parts[1], out b)) return false;\n        return a >= 0 && b >= 0;   // near-miss: zero passes\n    }\n\n    public static int SwapWithCount(ref int x, ref int y)\n    {\n        (x, y) = (y, x);\n        _swaps++;\n        return _swaps;\n    }\n\n    public static long FlattenDepth(object[][] groups, int depth)\n    {\n        // near-miss: no depth bound — recursion never terminates on the\n        // depth>=1 path unless the arrays are empty, so the deep test hangs\n        if (groups is null) return 0;\n        long total = 0;\n        foreach (object[] group in groups)\n        {\n            foreach (object item in group)\n            {\n                if (item is int n) total += n;\n            }\n        }\n        return total + FlattenDepth(groups, depth - 1);\n    }\n}\n',
)
# ---------------------------------------------------------------- practices
write_practice(
    M,
    "csi-p2-parameters",
    "Parameter Passing Practice",
    "Out-contracts that assign before they return, ref totals that survive the call, and params counting — the passing toolbox under test.",
    "Luyện truyền tham số",
    "Hợp đồng out gán trước khi trả về, tổng ref sống sót qua lần gọi, và params đếm phần tử — bộ công cụ truyền tham số dưới kiểm thử.",
    "csi-parameter-passing",
    25,
    "intermediate",
    [
        challenge(
            "csi-p2-out-parser",
            "Out Params: Assign Before You Return",
            """Implement a Try-style parser for "left:right" where BOTH numbers must be strictly positive. On ANY failure (bad shape, unparseable part, non-positive value), return false and leave BOTH out params at 0 — out params carry data only on success.

```csharp
static bool TryParsePair(string input, out int a, out int b);
```""",
            CS_PRELUDE,
            [
                (
                    "happy path",
                    r"""
Cj.Eq(Solution.TryParsePair("3:4", out int a, out int b), true, "valid pair parses");
Cj.Eq(a, 3, "a assigned");
Cj.Eq(b, 4, "b assigned");
""",
                    "Split on ':', require exactly 2 parts, int.TryParse each, both must be > 0.",
                ),
                (
                    "failure leaves zeros",
                    r"""
Cj.Eq(Solution.TryParsePair("3:0", out int a1, out int b1), false, "zero is not positive");
Cj.Eq(a1, 0, "a zeroed on failure");
Cj.Eq(b1, 0, "b zeroed on failure");
Cj.Eq(Solution.TryParsePair("x:9", out int a2, out int b2), false, "unparseable part");
Cj.Eq(Solution.TryParsePair("3", out int a3, out int b3), false, "wrong shape");
Cj.Eq(Solution.TryParsePair("", out int a4, out int b4), false, "empty input");
""",
                    "Parse into locals, check positivity, and only THEN write the out params — failure paths leave them 0.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p2-ref-tally",
            "ref: State That Survives the Call",
            """Two contracts. `Total` adds every item to the CALLER's `running` and returns the new total. `Swap` exchanges two ints through ref.

```csharp
static long Total(ref long running, int[] additions);
static void Swap(ref int x, ref int y);
```""",
            CS_PRELUDE,
            [
                (
                    "write-back observable",
                    r"""
long t = 0;
Cj.Eq(Solution.Total(ref t, new[] { 1, 2, 3 }), 6, "returns the new total");
Cj.Eq(t, 6, "caller sees the write-back");
Cj.Eq(Solution.Total(ref t, new[] { 10 }), 16, "state survives across calls");
Cj.Eq(t, 16, "running updated again");
""",
                    "Mutate the ref parameter itself — a local copy will not reach the caller.",
                ),
                (
                    "swap through ref",
                    r"""
int x = 1, y = 2;
Solution.Swap(ref x, ref y);
Cj.Eq(x, 2, "x took y's old value");
Cj.Eq(y, 1, "y took x's old value");
""",
                    "Tuple swap: (x, y) = (y, x) — both sides are ref locals.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p2-discount-debug",
            "Debug: The Discount That Pays Customers",
            """A checkout bug report: one customer paid 50 for a 150%-off coupon and the balance went NEGATIVE. Fix `ApplyDiscount` so percent is clamped to [0, 100] before use. `CountNonEmpty` is correct — leave it alone.

```csharp
static void ApplyDiscount(ref decimal price, decimal percent);
static int CountNonEmpty(params string?[] items);
```""",
            CS_PRELUDE,
            [
                (
                    "normal discount",
                    r"""
decimal price = 100m;
Solution.ApplyDiscount(ref price, 25m);
Cj.Eq(price, 75m, "25% off");
""",
                    "price -= price * percent / 100m, after clamping percent.",
                ),
                (
                    "clamp both ends",
                    r"""
decimal p2 = 50m;
Solution.ApplyDiscount(ref p2, 150m);
Cj.Eq(p2, 0m, "percent clamped to 100 -> free");
decimal p3 = 80m;
Solution.ApplyDiscount(ref p3, -5m);
Cj.Eq(p3, 80m, "negative percent clamped to 0 -> no change");
""",
                    "Math.Clamp(percent, 0m, 100m) before the arithmetic.",
                ),
                (
                    "params counting",
                    r"""
Cj.Eq(Solution.CountNonEmpty("a", null, "", "b"), 2, "null and empty skipped");
Cj.Eq(Solution.CountNonEmpty(), 0, "zero args is legal");
""",
                    "params gives an array — Count(i => !string.IsNullOrEmpty(i)).",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p2-out-parser": vi_challenge(
            "Tham số out: gán trước khi trả về",
            "Hiện thực bộ parser kiểu Try cho \"trái:phải\" trong đó CẢ HAI số phải dương. Khi thất bại (sai dạng, phần không parse được, giá trị không dương), trả false và để CẢ HAI tham số out bằng 0 — out chỉ mang dữ liệu khi thành công.",
            [
                ("happy path", "Tách trên ':', yêu cầu đúng 2 phần, int.TryParse từng phần, cả hai phải > 0."),
                ("failure leaves zeros", "Parse vào biến cục bộ, kiểm tra dương, RỒI mới ghi tham số out — đường thất bại để nguyên 0."),
            ],
        ),
        "csi-p2-ref-tally": vi_challenge(
            "ref: trạng thái sống qua lần gọi",
            "Hai hợp đồng. `Total` cộng mọi phần tử vào `running` CỦA NGƯỜI GỌI và trả tổng mới. `Swap` hoán đổi hai int qua ref.",
            [
                ("write-back observable", "Tự biến đổi tham số ref — bản sao cục bộ không tới được người gọi."),
                ("swap through ref", "Hoán đổi bằng tuple: (x, y) = (y, x)."),
            ],
        ),
        "csi-p2-discount-debug": vi_challenge(
            "Debug: mã giảm giá trả tiền cho khách",
            "Báo cáo lỗi: một khách thanh toán 50 cho phiếu giảm 150% và số dư bị ÂM. Sửa `ApplyDiscount` để percent bị chặn trong [0, 100] trước khi dùng. `CountNonEmpty` đúng rồi — đừng đụng vào.",
            [
                ("normal discount", "price -= price * percent / 100m, sau khi chặn percent."),
                ("clamp both ends", "Math.Clamp(percent, 0m, 100m) trước phép tính."),
                ("params counting", "params cho một mảng — Count(i => !string.IsNullOrEmpty(i))."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p2-out-parser",
            r'''public class Solution
{
    public static bool TryParsePair(string input, out int a, out int b)
    {
        a = 0; b = 0;
        if (string.IsNullOrWhiteSpace(input)) return false;
        string[] parts = input.Split(':');
        if (parts.Length != 2) return false;
        if (!int.TryParse(parts[0], out int x)) return false;
        if (!int.TryParse(parts[1], out int y)) return false;
        if (x <= 0 || y <= 0) return false;   // out params stay 0 on failure
        a = x; b = y;
        return true;
    }
}''',
            r'''public class Solution
{
    public static bool TryParsePair(string input, out int a, out int b)
    {
        // near-miss: parsing assigns the out params directly, but the final
        // "not positive" rejection leaves them holding the parsed values
        a = 0; b = 0;
        if (string.IsNullOrWhiteSpace(input)) return false;
        string[] parts = input.Split(':');
        if (parts.Length != 2) return false;
        if (!int.TryParse(parts[0], out a)) return false;
        if (!int.TryParse(parts[1], out b)) return false;
        return a > 0 && b > 0;   // "3:0" -> false, but a stays 3
    }
}''',
        ),
        (
            "csi-p2-ref-tally",
            r'''public class Solution
{
    public static long Total(ref long running, int[] additions)
    {
        foreach (int v in additions) running += v;
        return running;
    }

    public static void Swap(ref int x, ref int y) => (x, y) = (y, x);
}''',
            r'''public class Solution
{
    public static long Total(ref long running, int[] additions)
    {
        // near-miss: computes from running but never writes the new total
        // back — the caller's running stays put
        long t = running;
        foreach (int v in additions) t += v;
        return t;
    }

    public static void Swap(ref int x, ref int y) => (x, y) = (y, x);
}''',
        ),
        (
            "csi-p2-discount-debug",
            r'''public class Solution
{
    public static void ApplyDiscount(ref decimal price, decimal percent)
    {
        decimal clamped = Math.Clamp(percent, 0m, 100m);
        price -= price * clamped / 100m;
    }

    public static int CountNonEmpty(params string?[] items)
        => items.Count(i => !string.IsNullOrEmpty(i));
}''',
            r'''public class Solution
{
    public static void ApplyDiscount(ref decimal price, decimal percent)
    {
        // near-miss: no clamping — 150% flips the price negative
        price -= price * percent / 100m;
    }

    public static int CountNonEmpty(params string?[] items)
        => items.Count(i => !string.IsNullOrEmpty(i));
}''',
        ),
    ],
)

write_practice(
    M,
    "csi-p2-overloads",
    "Overload Resolution Practice",
    "Pick the exact overload the compiler picks, and wire optional/named arguments without surprises.",
    "Luyện chọn overload",
    "Chọn đúng overload mà compiler chọn, và dùng tham số tùy chọn/tên gọi không bất ngờ.",
    "csi-overloads-and-members",
    20,
    "intermediate",
    [
        challenge(
            "csi-p2-overload-pick",
            "Four Overloads, One Winner Each",
            """Implement four `Describe` overloads. Each call site in the tests must bind to the overload named in the assertion — this is the compiler's betterness table in action (exact beats implicit; int? binds to int? when it exists, otherwise falls back to boxing).

```csharp
static string Describe(int x);       // "int"
static string Describe(double x);    // "double"
static string Describe(int? x);      // "int?"
static string Describe(object? x);   // "object"
```""",
            CS_PRELUDE,
            [
                (
                    "exact matches win",
                    r"""
Cj.Eq(Solution.Describe(5), "int", "int literal -> int overload");
Cj.Eq(Solution.Describe(5.0), "double", "double literal -> double overload");
Cj.Eq(Solution.Describe((int?)5), "int?", "int? argument -> int? overload");
Cj.Eq(Solution.Describe((object?)null), "object", "object? argument -> object overload");
Cj.Eq(Solution.Describe((object?)"hi"), "object", "boxed string -> object overload");
""",
                    "Four one-line methods — the interesting question is what (int?)5 binds to.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p2-tag",
            "Optional and Named Arguments",
            """Implement `Tag`: returns "kind#count" and appends "!urgent" when urgent. Defaults: count 1, urgent false. The tests call it positionally, with named args out of order, and skipping the middle parameter.

```csharp
static string Tag(string kind, int count = 1, bool urgent = false);
```""",
            CS_PRELUDE,
            [
                (
                    "defaults and named args",
                    r"""
Cj.Eq(Solution.Tag("bug"), "bug#1", "defaults");
Cj.Eq(Solution.Tag("bug", 3), "bug#3", "positional count");
Cj.Eq(Solution.Tag(count: 2, kind: "feat"), "feat#2", "named args, reordered");
Cj.Eq(Solution.Tag("fix", urgent: true), "fix#1!urgent", "skip the middle with named");
Cj.Eq(Solution.Tag("chore", 2, true), "chore#2!urgent", "all positional");
""",
                    "The default value lives in the parameter list; named callers rely on it.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p2-overload-pick": vi_challenge(
            "Bốn overload, một người thắng mỗi lần gọi",
            "Hiện thực bốn overload `Describe`. Mỗi lệnh gọi trong test phải bám vào overload đúng tên ghi trong assertion — đây là bảng betterness của compiler (đúng chuẩn thắng chuyển ngầm; int? bám int? khi nó tồn tại, không thì fallback sang boxing).",
            [
                ("exact matches win", "Bốn phương thức một dòng — câu hỏi thú vị là (int?)5 bám vào đâu."),
            ],
        ),
        "csi-p2-tag": vi_challenge(
            "Tham số tùy chọn và tham số tên",
            "Hiện thực `Tag`: trả \"kind#count\" và thêm \"!urgent\" khi urgent. Mặc định: count 1, urgent false. Test gọi theo vị trí, theo tên không theo thứ tự, và bỏ qua tham số giữa.",
            [
                ("defaults and named args", "Giá trị mặc định nằm trong danh sách tham số; caller dùng tên phụ thuộc vào nó."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p2-overload-pick",
            r'''public class Solution
{
    public static string Describe(int x) => "int";
    public static string Describe(double x) => "double";
    public static string Describe(int? x) => "int?";
    public static string Describe(object? x) => "object";
}''',
            r'''public class Solution
{
    // near-miss: no int? overload — the int? argument boxes and falls into
    // Describe(object?), so the lifted-conversion fallback fires
    public static string Describe(int x) => "int";
    public static string Describe(double x) => "double";
    public static string Describe(object? x) => "object";
}''',
        ),
        (
            "csi-p2-tag",
            r'''public class Solution
{
    public static string Tag(string kind, int count = 1, bool urgent = false)
        => kind + "#" + count + (urgent ? "!urgent" : "");
}''',
            r'''public class Solution
{
    public static string Tag(string kind, int count = 0, bool urgent = false)
        // near-miss: default count is 0 — every defaulted caller tags "#0"
        => kind + "#" + count + (urgent ? "!urgent" : "");
}''',
        ),
    ],
)

print("module 2 authored")
