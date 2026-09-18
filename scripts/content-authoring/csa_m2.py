"""Module 2 — Memory and object model (csa-m2)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-memory-object-model",
        "Memory and the Object Model",
        "Where values live, when copying happens, how spans avoid allocation, and how to measure all of it.",
    )

    csa.register_lesson(
        MID, "csa-m2-layout", "Stack, heap, and object layout",
        "Where data lives, what an object header costs, and which of it is a language guarantee vs runtime detail.",
        15, "advanced", _m2_layout, _m2_layout_vi,
    )
    csa.register_lesson(
        MID, "csa-m2-ref-returns", "Ref locals, ref returns, and defensive copies",
        "Aliases instead of copies: ref locals/returns, ref readonly, and when the compiler inserts a copy anyway.",
        14, "advanced", _m2_ref_returns, _m2_ref_returns_vi,
    )
    csa.register_lesson(
        MID, "csa-m2-spans", "Span<T>, ReadOnlySpan<T>, and stackalloc",
        "The safe window into memory: spans, their ref-struct rules, and stackalloc for small buffers.",
        16, "advanced", _m2_spans, _m2_spans_vi,
    )
    csa.register_lesson(
        MID, "csa-m2-allocation-measure", "Measuring allocations honestly",
        "GC.GetAllocatedBytesForCurrentThread, JIT warmup, and why a single measurement lies.",
        14, "advanced", _m2_measure, _m2_measure_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m2", "Checkpoint: memory model",
        "Synthesis: copy/alias decisions, span slicing, and a measured allocation budget.",
        12, "advanced", _m2_checkpoint, _m2_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m2-task", MID,
        title="Memory model checkpoint",
        prompt=(
            "Implement `static (int copiedX, int aliasedY) AliasVsCopy()`. Inside: create a struct `S { public int X; }` "
            "with X=1, copy it to a second local and set the copy's X=2 (original must stay 1); then create an array "
            "`int[] a = {5}`, take a ref local `ref int r = ref a[0]`, set r=7. Return (original struct X, a[0])."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "copy-independence",
                "code": (
                    "var (cx, ay) = Solution.AliasVsCopy();\n"
                    'Cj.Eq(cx, 1, "struct copy must not leak mutation");\n'
                    'Cj.Eq(ay, 7, "ref alias writes through to the array");'
                ),
                "hint": "Struct assignment copies; `ref` creates an alias that writes through.",
            },
            {
                "name": "allocation-shape",
                "code": (
                    "// One array allocation (the 1-element int[]); no other heap allocations expected:\n"
                    "long before = GC.GetAllocatedBytesForCurrentThread();\n"
                    "Solution.AliasVsCopy();\n"
                    "long after = GC.GetAllocatedBytesForCurrentThread();\n"
                    "// Tolerant: allow the tuple allocation if any, but cap it:\n"
                    "Cj.True(after - before <= 64, $\"leaked {after - before} bytes\");"
                ),
                "hint": "The whole method should allocate at most the small array (and tuple) — no boxing, no string.",
            },
        ],
        reference=(
            "public struct S { public int X; }\n\n"
            "public class Solution\n{\n"
            "    public static (int copiedX, int aliasedY) AliasVsCopy()\n    {\n"
            "        var s = new S { X = 1 };\n"
            "        var copy = s;\n"
            "        copy.X = 2;               // copy mutated; s untouched\n"
            "        int[] a = { 5 };\n"
            "        ref int r = ref a[0];\n"
            "        r = 7;                    // alias writes through\n"
            "        return (s.X, a[0]);\n"
            "    }\n}"
        ),
        wrong=(
            "public struct S { public int X; }\n\n"
            "public class Solution\n{\n"
            "    public static (int copiedX, int aliasedY) AliasVsCopy()\n    {\n"
            "        var s = new S { X = 1 };\n"
            "        ref var copy = ref s;      // WRONG: alias, not copy\n"
            "        copy.X = 2;                // mutates s\n"
            "        int[] a = { 5 };\n"
            "        int r = a[0];              // WRONG: value copy, not alias\n"
            "        r = 7;\n"
            "        return (s.X, a[0]);\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p2-memory", "Memory drills",
        "Spans, defensive copies, ref returns, and honest allocation measurement.",
        45, "advanced", "csa-m2-spans",
        ["csa-p2-span-parse", "csa-p2-defensive-copy", "csa-p2-alloc-budget"],
    )
    csa.register_challenge(
        "csa-p2-span-parse", MID,
        title="Parse without allocating",
        prompt=(
            "Implement `static (int a, int b) ParsePair(ReadOnlySpan<char> input)` that parses two "
            "comma-separated integers from the span WITHOUT allocating any string. No Split, no Substring — "
            "slice and parse the span directly. The test measures allocations to prove it."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "correctness",
                "code": (
                    'var (a, b) = Solution.ParsePair("12,345".AsSpan());\n'
                    'Cj.Eq(a, 12, "a");\n'
                    'Cj.Eq(b, 345, "b");'
                ),
                "hint": "Slice at the comma: input[..i] and input[(i+1)..], then int.Parse each slice.",
            },
            {
                "name": "zero-alloc",
                "code": (
                    "// The FIRST loop runs before JIT tiering settles and observes a small\n"
                    "// per-call overhead; after warmup the span path is byte-identical to\n"
                    "// zero. The Split path still allocates per call, so it fails the second\n"
                    "// (warmed) measurement — exactly the lesson.\n"
                    "ReadOnlySpan<char> s = \"9,10\".AsSpan();\n"
                    "for (int i = 0; i < 200; i++) Solution.ParsePair(s);   // warmup\n"
                    "long before = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 100; i++) Solution.ParsePair(s);\n"
                    "long after = GC.GetAllocatedBytesForCurrentThread();\n"
                    'Cj.True(after - before <= 96, $"100 warmed parses allocated {after - before} bytes (must be ~0)");'
                ),
                "hint": "int.Parse(ReadOnlySpan<char>) never allocates; the tuple fits in registers/stack.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static (int a, int b) ParsePair(ReadOnlySpan<char> input)\n    {\n"
            "        int i = input.IndexOf(',');\n"
            "        return (int.Parse(input[..i]), int.Parse(input[(i + 1)..]));\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static (int a, int b) ParsePair(ReadOnlySpan<char> input)\n    {\n"
            "        var parts = input.ToString().Split(',');   // allocates string + array\n"
            "        return (int.Parse(parts[0]), int.Parse(parts[1]));\n"
            "    }\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p2-defensive-copy", MID,
        title="Defensive copies in readonly members",
        prompt=(
            "A mutable struct stored in a readonly field is copied on every member access. Implement struct "
            "`Container` with `private readonly Mut _m;` and a `public int Get()` that reads `_m.Value` twice "
            "and returns their sum. Implement struct `Mut { public int Value; }`. The lesson: each `_m.Value` "
            "read copies first — implement it so the TEST (which checks the sum) passes; you cannot observe the "
            "copies from outside, which is exactly the point: they are invisible but real."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "sum",
                "code": (
                    "var c = new Container();\n"
                    'Cj.Eq(c.Get(), 0, "default Mut.Value is 0, sum 0+0");'
                ),
                "hint": "Return _m.Value + _m.Value.",
            },
        ],
        reference=(
            "public struct Mut { public int Value; }\n\n"
            "public struct Container\n{\n"
            "    private readonly Mut _m;\n"
            "    public int Get() => _m.Value + _m.Value;\n"
            "}\n\n"
            "public class Solution { }"
        ),
        wrong=(
            "public struct Mut { public int Value; }\n\n"
            "public struct Container\n{\n"
            "    private readonly Mut _m;\n"
            "    public int Get() => _m.Value * _m.Value;   // wrong operation\n"
            "}\n\n"
            "public class Solution { }"
        ),
        level="imitation",
    )
    csa.register_challenge(
        "csa-p2-alloc-budget", MID,
        title="Meet the allocation budget",
        prompt=(
            "Implement `static int[] Squares(int n)` returning the squares 0..n-1 as a NEW array, and "
            "`static int SumSquares(int n)` computing the same total with ZERO heap allocations (a plain loop, "
            "no LINQ). The test enforces: Squares allocates ≤ n*8+64 bytes; SumSquares allocates exactly 0."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "values",
                "code": (
                    "var arr = Solution.Squares(4);\n"
                    'Cj.Eq(arr.Length, 4, "length");\n'
                    'Cj.Eq(arr[3], 9, "3^2");\n'
                    'Cj.Eq(Solution.SumSquares(4), 14, "0+1+4+9");'
                ),
                "hint": "Squares: new int[n] and fill; SumSquares: accumulate in a loop.",
            },
            {
                "name": "budget",
                "code": (
                    "long b0 = GC.GetAllocatedBytesForCurrentThread();\n"
                    "Solution.Squares(1000);\n"
                    "long b1 = GC.GetAllocatedBytesForCurrentThread();\n"
                    "long sq = b1 - b0;\n"
                    "b0 = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 100; i++) Solution.SumSquares(1000);\n"
                    "b1 = GC.GetAllocatedBytesForCurrentThread();\n"
                    'Cj.True(sq <= 1000 * 8 + 64, $"Squares allocated {sq}");\n'
                    'Cj.Eq(b1 - b0, 0L, $"SumSquares allocated {b1 - b0} over 100 runs");'
                ),
                "hint": "One array of n ints ≈ 8n bytes. SumSquares must not even allocate an enumerator — no LINQ.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static int[] Squares(int n)\n    {\n"
            "        var r = new int[n];\n"
            "        for (int i = 0; i < n; i++) r[i] = i * i;\n"
            "        return r;\n"
            "    }\n\n"
            "    public static int SumSquares(int n)\n    {\n"
            "        int t = 0;\n"
            "        for (int i = 0; i < n; i++) t += i * i;\n"
            "        return t;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int[] Squares(int n)\n    {\n"
            "        var r = new int[n];\n"
            "        for (int i = 0; i < n; i++) r[i] = i * i;\n"
            "        return r;\n"
            "    }\n\n"
            "    public static int SumSquares(int n) =>\n"
            "        Enumerable.Range(0, n).Sum(i => i * i);   // allocates enumerator + closure\n"
            "}"
        ),
        level="independent",
    )


# ── Lesson bodies (EN + VI) ─────────────────────────────────────────────────

_m2_layout = r"""## Stack, heap, and object layout

Every value lives somewhere, and "somewhere" decides its lifetime:

- **Stack** (execution context): locals of value types, method frames.
  Lifetime = the scope. Gone when the method returns.
- **Managed heap**: every `class` instance, array, delegate, boxed value.
  Lifetime = reachability, decided later by the GC.
- **Registers / enregistration**: the JIT often keeps small structs entirely
  in registers — the "stack" is already an abstraction.

A heap object carries a fixed **header** (sync block index + method table
pointer) before its fields. You cannot see it in C#, but it is why 1000
tiny objects cost more than their field bytes, and why structs used only
inside a method may cost nothing at all.

| Kind | Lives | Copied on assignment | Lifetime |
|---|---|---|---|
| `struct` local | stack/registers | yes, whole value | scope |
| `class` instance | heap | reference only | GC |
| `T[]` array | heap | reference | GC |
| `ref struct` (Span) | stack only | yes | scope — by rule |
| boxed value | heap | reference | GC |

What is **guarantee vs implementation detail**: the C# spec guarantees
assignment copies value-type values and ref-structs stay on the stack. The
*exact* header size, whether a local is enregistered, and object field
ordering (`LayoutKind.Auto` default) are runtime details — you may observe
them, never rely on them.

```csharp
// Observable, but NOT contract: layout internals
Console.WriteLine(object.Header...);   // does not exist — by design
```

The professional habit: reason about **categories** (scope vs GC, copy vs
alias), measure quantities when it matters, and never hard-code observed
sizes into logic.
"""

_m2_layout_vi = r"""## Ngăn xếp, heap, và layout đối tượng

Mọi giá trị đều nằm ở đâu đó, và "ở đâu" quyết định vòng đời của nó:

- **Ngăn xếp** (bối cảnh thực thi): biến cục bộ kiểu value, khung hàm.
  Vòng đời = phạm vi. Mất khi hàm trả về.
- **Managed heap**: mọi thể hiện `class`, mảng, delegate, boxed value.
  Vòng đời = khả năng truy cập, do GC quyết định sau.
- **Thanh ghi**: JIT thường giữ struct nhỏ nguyên vẹn trong thanh ghi —
  "ngăn xếp" vốn đã là một trừu tượng hóa.

Một object trên heap mang **header** cố định (sync block index + method
table pointer) trước các field. Bạn không nhìn thấy nó trong C#, nhưng đó
là lý do 1000 object nhỏ tốn hơn tổng byte field của chúng, và vì sao
struct chỉ dùng trong một hàm có thể không tốn gì cả.

| Loại | Nằm ở | Sao chép khi gán | Vòng đời |
|---|---|---|---|
| `struct` cục bộ | stack/thanh ghi | có, toàn bộ giá trị | phạm vi |
| `class` | heap | chỉ tham chiếu | GC |
| mảng `T[]` | heap | tham chiếu | GC |
| `ref struct` (Span) | chỉ stack | có | phạm vi — theo luật |
| value đã box | heap | tham chiếu | GC |

Điều gì là **cam kết vs chi tiết triển khai**: spec C# đảm bảo phép gán sao
chép giá trị value-type và ref-struct chỉ nằm trên stack. Kích thước header
*chính xác*, việc một biến cục bộ được đưa vào thanh ghi, thứ tự field
(`LayoutKind.Auto` là mặc định) là chi tiết runtime — có thể quan sát,
không được phép dựa vào.

```csharp
// Quan sát được, NHƯNG không phải hợp đồng: nội bộ layout
Console.WriteLine(object.Header...);   // không tồn tại — vì một lý do
```

Thói quen nghề nghiệp: suy luận theo **danh mục** (phạm vi vs GC, bản sao vs
alias), đo lường khi cần, và không bao giờ hard-code kích thước quan sát
được vào logic.
"""

_m2_ref_returns = r"""## Ref locals, ref returns, and defensive copies

`ref` makes an alias: another name for existing storage. The copy that
normally happens on assignment does not happen:

```csharp
int[] xs = { 1, 2, 3 };
ref int slot = ref xs[1];   // slot IS xs[1] — same storage
slot = 99;                  // xs[1] == 99 now

// ref returns expose storage from methods:
static ref int At(int[] a, int i) => ref a[i];
At(xs, 0) = 42;             // assign THROUGH the returned ref
```

The safety rules are strict, and they all prevent escaping stack storage:
ref returns may not return a ref to a local; ref locals must be initialized
from something that outlives them; ref structs (Module 2's Span) may not
cross `await` boundaries or be captured by ordinary closures.

**Ref readonly and defensive copies.** `ref readonly int` promises the
callee will not write. But a *mutable struct* read through a
`readonly` field/member forces the compiler to insert a **defensive copy**
per access — an invisible cost. The classic bug-shaped fact: calling a
method twice on a readonly mutable struct reads two different copies, and
each copy costs a full struct copy. The fix is either `readonly struct`
(all members readonly, no defensive copies ever) or `in` parameters
passed as readonly refs.

```csharp
readonly struct Vec { public double X; public double Y; }   // zero copies
struct Bad   { public double X; }                            // copies on readonly access
```

Why care: silent per-access copies on big structs (say, 256-byte matrices)
are a classic allocation-free performance bug — the profiler shows CPU,
not allocations, because nothing is allocated; the bytes just move.
"""

_m2_ref_returns_vi = r"""## Ref local, ref return, và bản sao phòng vệ

`ref` tạo ra một alias: một tên khác cho cùng vùng nhớ. Phép sao chép vốn
xảy ra khi gán không xảy ra nữa:

```csharp
int[] xs = { 1, 2, 3 };
ref int slot = ref xs[1];   // slot CHÍNH LÀ xs[1] — cùng một vùng nhớ
slot = 99;                  // xs[1] == 99 ngay lập tức

// ref return để lộ vùng nhớ từ hàm:
static ref int At(int[] a, int i) => ref a[i];
At(xs, 0) = 42;             // gán QUA ref được trả về
```

Các luật an toàn rất nghiêm, và tất cả đều nhằm chặn việc "chui" vùng nhớ
stack ra ngoài: ref return không được trả ref trỏ vào biến cục bộ; ref local
phải khởi tạo từ thứ sống lâu hơn nó; ref struct (Span — sẽ gặp trong module
này) không được vượt biên `await` hay bị closure thường bắt giữ.

**Ref readonly và bản sao phòng vệ.** `ref readonly int` hứa rằng bên gọi
sẽ không ghi. Nhưng đọc một *struct khả biến* qua field/thành phần
`readonly` buộc compiler chèn một **bản sao phòng vệ** cho mỗi lần truy
cập — một chi phí vô hình. Sự thật hình dạng bug kinh điển: gọi phương thức
hai lần trên một readonly mutable struct là đọc hai bản sao khác nhau,
và mỗi bản sao tốn một lần sao chép toàn bộ struct. Cách sửa: hoặc
`readonly struct` (mọi thành phần readonly, không bao giờ có bản sao phòng
vệ) hoặc tham số `in` được truyền như readonly ref.

```csharp
readonly struct Vec { public double X; public double Y; }   // không sao chép
struct Bad   { public double X; }                            // sao chép khi truy cập readonly
```

Vì sao quan tâm: các bản sao vô hình mỗi lần truy cập trên struct lớn
(ví dụ ma trận 256 byte) là bug hiệu năng kinh điển mà không tạo cấp phát —
profiler chỉ thấy CPU, không thấy allocation, vì không có gì được cấp phát;
các byte chỉ di chuyển.
"""

_m2_spans = r"""## Span<T>, ReadOnlySpan<T>, and stackalloc

`Span<T>` is a stack-only window over memory: (ref T, int length). It can
slice an array, a string, a rented pool buffer, or native memory — without
copying any of it:

```csharp
int[] data = { 10, 20, 30, 40 };
Span<int> mid = data.AsSpan(1, 2);   // view of elements 1..2
mid[0] = 21;                          // writes data[1]

ReadOnlySpan<char> tail = "hello world".AsSpan(6);  // no substring allocated
```

The `ref struct` rules are not bureaucracy; they are what makes span
**safe** while pointing at the stack:

- A span cannot be a field of a class, cannot be boxed, cannot be captured
  by a closure that might outlive the frame.
- It cannot cross `await` — the frame may not exist after suspension.
- It cannot be a `readonly`-accessed mutable struct's member (defensive
  copy of a ref struct is impossible).

`stackalloc` allocates a small buffer in the current frame:

```csharp
Span<byte> scratch = stackalloc byte[256];   // deterministic, no GC
```

Budget it: a few hundred bytes to low KBs is sane; large stackallocs risk
stack overflow (default stack ~1MB). For conditional allocation, the
`stackalloc` + fallback pattern:

```csharp
char[]? rented = null;
ReadOnlySpan<char> buf = input.Length <= 128
    ? stackalloc char[128]      // stack fast path (bounded!)
    : (rented = ArrayPool<char>.Shared.Rent(input.Length)).AsSpan();
// ... use buf ...
if (rented is not null) ArrayPool<char>.Shared.Return(rented);
```

The `128` bound in the stackalloc arm is load-bearing: the compiler emits a
stack frame sized by that CONSTANT, not by `input.Length` — a variable-size
stackalloc would be the overflow. `ReadOnlySpan<char>` over a string literal
plus `int.Parse(span)` is the standard zero-allocation parse path — the
checkpoint's tests enforce it with the allocation probe.
"""

_m2_spans_vi = r"""## Span<T>, ReadOnlySpan<T>, và stackalloc

`Span<T>` là một cửa sổ chỉ-đứng-trên-stack vào vùng nhớ: (ref T, int
length). Nó có thể slice một mảng, một string, một buffer thuê từ pool, hay
bộ nhớ native — mà không sao chép bất kỳ thứ gì:

```csharp
int[] data = { 10, 20, 30, 40 };
Span<int> mid = data.AsSpan(1, 2);   // nhìn các phần tử 1..2
mid[0] = 21;                          // ghi vào data[1]

ReadOnlySpan<char> tail = "hello world".AsSpan(6);  // không cấp phát substring
```

Các luật `ref struct` không phải giấy phép lái xe; chúng là thứ làm span
**an toàn** dù có thể trỏ vào stack:

- Span không thể là field của class, không thể bị box, không thể bị closure
  có thể sống lâu hơn khung hiện tại bắt giữ.
- Nó không thể vượt qua `await` — khung có thể không tồn tại sau lần treo.
- Nó không thể là thành phần của mutable struct bị truy cập readonly
  (bản sao phòng vệ của ref struct là bất khả thi).

`stackalloc` cấp phát một buffer nhỏ trong khung hiện tại:

```csharp
Span<byte> scratch = stackalloc byte[256];   // tất định, không qua GC
```

Đặt ngân sách: vài trăm byte tới vài KB là hợp lý; stackalloc lớn có nguy
cơ tràn stack (stack mặc định ~1MB). Với cấp phát có điều kiện, dùng pattern
stackalloc + dự phòng:

```csharp
char[]? rented = null;
ReadOnlySpan<char> buf = input.Length <= 128
    ? stackalloc char[128]      // đường nhanh trên stack (CÓ CHẶN!)
    : (rented = ArrayPool<char>.Shared.Rent(input.Length)).AsSpan();
// ... dùng buf ...
if (rented is not null) ArrayPool<char>.Shared.Return(rented);
```

Số `128` trong nhánh stackalloc là gánh kết cấu: compiler sinh khung stack
theo HẰNG SỐ đó, không phải theo `input.Length` — stackalloc kích thước
biến đổi chính là lệnh tràn stack. `ReadOnlySpan<char>` trên string literal
kết hợp `int.Parse(span)` là đường parse không-cấp-phát chuẩn — các test
trong checkpoint ép điều này bằng thăm dò cấp phát.
"""

_m2_measure = r"""## Measuring allocations honestly

The probe that answers "did this allocate?":

```csharp
long before = GC.GetAllocatedBytesForCurrentThread();
Work();
long delta = GC.GetAllocatedBytesForCurrentThread() - before;
```

Per-thread is the point: background GC activity, other threads' noise, all
excluded. But two honest-measurement rules survive any probe:

1. **Warm up first.** First calls pay JIT compilation, generic dictionaries
   populate, delegates allocate. Measure call #2 onward, or loop N times
   and divide — a single cold measurement lies by orders of magnitude.
2. **Delta is the truth, not the absolute.** Absolute bytes include the
   harness. The number that matters is the DIFFERENCE between two code
   paths doing the same work.

Reading results like a performance engineer:

- **Exactly 0** — the fast path is allocation-free. Verify with a loop of
  100 iterations: a hidden 24-byte allocation per call shows up as 2400.
- **Small constant** — one fixed allocation; find and question it (a tuple?
  a boxed value? a delegate cache miss?).
- **Linear in N** — the loop allocates per iteration. Span/for-loop instead
  of LINQ is the usual fix.

What this probe CANNOT tell you: total memory pressure (other threads),
retained size (leaks — that is GC.GetTotalMemory over time), or latency
(that is a benchmark, and a dishonest one unless you follow Module 15's
rules). Allocation measurement is one instrument of several; the habit of
REACHING FOR IT before arguing is what distinguishes engineers who ship
performance from engineers who ship vibes.
"""

_m2_measure_vi = r"""## Đo cấp phát một cách trung thực

Thăm dò trả lời câu hỏi "cái này có cấp phát không?":

```csharp
long before = GC.GetAllocatedBytesForCurrentThread();
Work();
long delta = GC.GetAllocatedBytesForCurrentThread() - before;
```

Theo-thread là điểm mấu chốt: hoạt động GC nền, nhiễu từ thread khác, tất
cả bị loại. Nhưng hai luật đo trung thực vẫn đứng vững với bất kỳ probe
nào:

1. **Làm nóng trước.** Các lần gọi đầu trả chi phí JIT compile, từ điển
   generic được điền, delegate được cấp phát. Hãy đo từ lần gọi thứ hai
   trở đi, hoặc lặp N lần rồi chia — một phép đo lạnh dối bằng nhiều bậc
   độ lớn.
2. **Delta là sự thật, không phải số tuyệt đối.** Số byte tuyệt đối bao gồm
   cả harness. Con số quan trọng là HIỆU giữa hai đường code làm cùng một
   việc.

Đọc kết quả như một kỹ sư hiệu năng:

- **Đúng bằng 0** — đường nhanh không cấp phát. Xác nhận bằng vòng 100 lần
  lặp: một cấp phát ẩn 24 byte mỗi lần gọi sẽ hiện ra thành 2400.
- **Hằng số nhỏ** — một cấp phát cố định; tìm nó và chất vấn (tuple? giá
  trị bị box? một lần cache miss của delegate?).
- **Tuyến tính theo N** — vòng lặp cấp phát mỗi lần lặp. Span/vòng for thay
  LINQ là cách sửa thường gặp.

Probe này KHÔNG thể nói cho bạn: áp lực bộ nhớ tổng (thread khác), kích
thước bị giữ lại (rò rỉ — đó là GC.GetTotalMemory theo thời gian), hay độ
trễ (đó là benchmark, và là benchmark dối trá trừ khi bạn theo các luật
ở Module 15). Đo cấp phát chỉ là một trong vài nhạc cụ; thói quen VỀ PHÍA
NÓ trước khi tranh cãi mới là thứ phân biệt kỹ sư có hiệu năng thật với
kỹ sư có hiệu năng theo cảm giác.
"""

_m2_checkpoint = r"""## Checkpoint: memory model

The graded task forces the copy/alias decision explicitly (struct copy vs
ref alias, both observable), then audits the whole method with the
allocation probe — the pattern is: right answer AND right budget. Practice
adds zero-allocation span parsing, defensive-copy reasoning, and a strict
allocation budget on two competing implementations.
"""

_m2_checkpoint_vi = r"""## Checkpoint: mô hình bộ nhớ

Bài được chấm buộc bạn quyết định tường minh copy/alias (bản sao struct vs
ref alias, cả hai đều quan sát được), rồi kiểm toán toàn bộ phương thức
bằng thăm dò cấp phát — pattern là: đáp án đúng VÀ đúng ngân sách. Practice
thêm parse span không cấp phát, suy luận bản sao phòng vệ, và một ngân sách
cấp phát nghiêm ngặt trên hai bản triển khai cạnh nhau."""
