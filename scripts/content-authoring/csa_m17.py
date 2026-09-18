"""Module 17 — Native interop and unsafe C# (csa-m17)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-unsafe-interop",
        "Native Interop and Unsafe C#",
        "Pointers within managed memory, pinning, P/Invoke concepts, blittable types — the managed/unmanaged boundary, safely taught.",
    )

    csa.register_lesson(
        MID, "csa-m17-boundary", "Managed, unmanaged, unsafe: the boundary",
        "The three worlds and their rules — what unsafe code actually lifts, and what it never lifts.",
        15, "advanced", _m17_boundary, _m17_boundary_vi,
    )
    csa.register_lesson(
        MID, "csa-m17-pointers", "Unsafe pointers, fixed, and pinning",
        "The fixed statement, pointer arithmetic, and why pinning fights the GC (and how to stop fighting).",
        16, "advanced", _m17_pointers, _m17_pointers_vi,
    )
    csa.register_lesson(
        MID, "csa-m17-pin-stories", "Interop without native libraries: Unsafe, MemoryMarshal",
        "Unsafe.As, MemoryMarshal.Cast — the managed-memory pointer tricks that need no P/Invoke.",
        15, "advanced", _m17_marshal, _m17_marshal_vi,
    )
    csa.register_lesson(
        MID, "csa-m17-pinvoke-concepts", "P/Invoke concepts and the security bill",
        "Marshaling, blittable types, function pointers, SafeHandle — and the attack surface unsafe code opens.",
        15, "advanced", _m17_pinvoke, _m17_pinvoke_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m17", "Checkpoint: unsafe and interop",
        "Synthesis: pointer arithmetic within managed memory, done safely and measured.",
        12, "advanced", _m17_checkpoint, _m17_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m17-task", MID,
        title="Unsafe checkpoint",
        prompt=(
            "Implement `static int UnsafeSum(ReadOnlySpan<int> values)` that sums an int span using unsafe pointer "
            "arithmetic: `fixed (int* p = values)` (or inside an unsafe method on a span via GetPinnableReference), "
            "walk with p[i], accumulate. The test verifies correctness AND that it compiles only because the "
            "harness adds -unsafe (the same flag real projects configure). Also implement `static byte[] "
            "Reinterpret(long value)` that reinterprets a long's bytes as a 4-element ushort array copy using "
            "Unsafe/MemoryMarshal — demonstrating reinterpretation without pointers."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "unsafe-sum",
                "code": (
                    "int[] vals = { 1, 2, 3, 4, 5 };\n"
                    'Cj.Eq(Solution.UnsafeSum(vals.AsSpan()), 15, "pointer walk sums correctly");\n'
                    'Cj.Eq(Solution.UnsafeSum(ReadOnlySpan<int>.Empty), 0, "empty span");'
                ),
                "hint": "unsafe { fixed (int* p = values) { for (int i = 0; i < values.Length; i++) sum += p[i]; } }",
            },
            {
                "name": "reinterpret",
                "code": (
                    "long v = 0x0001_0002_0003_0004;   // little-endian bytes: 04 03 02 01\n"
                    "var us = Solution.Reinterpret(v);\n"
                    'Cj.Eq(us.Length, 4, "long = 4 ushorts");\n'
                    'Cj.Eq(us[0], 4, "low ushort first (LE)");\n'
                    'Cj.Eq(us[3], 1, "high ushort last");'
                ),
                "hint": "var src = MemoryMarshal.CreateReadOnlySpan(ref value, 1); var dst = MemoryMarshal.AsBytes(src); then two ushort reads — or simpler: MemoryMarshal.Cast<long, ushort>(new Span<long>(ref value, 1)).ToArray()",
            },
        ],
        reference=(
            "using System.Runtime.InteropServices;\n\n"
            "public class Solution\n{\n"
            "    public static unsafe int UnsafeSum(ReadOnlySpan<int> values)\n"
            "    {\n"
            "        int sum = 0;\n"
            "        fixed (int* p = values)   // pin during the walk — scoped, minimal\n"
            "        {\n"
            "            for (int i = 0; i < values.Length; i++) sum += p[i];\n"
            "        }\n"
            "        return sum;\n"
            "    }\n\n"
            "    public static ushort[] Reinterpret(long value)\n"
            "    {\n"
            "        var span = MemoryMarshal.CreateSpan(ref value, 1);\n"
            "        var cast = MemoryMarshal.Cast<long, ushort>(span);\n"
            "        return cast.ToArray();\n"
            "    }\n}"
        ),
        wrong=(
            "using System.Runtime.InteropServices;\n\n"
            "public class Solution\n{\n"
            "    public static int UnsafeSum(ReadOnlySpan<int> values)\n"
            "    {\n"
            "        int sum = 0;\n"
            "        foreach (var v in values) sum += v * 2;   // WRONG: not pointer walk, wrong math\n"
            "        return sum;\n"
            "    }\n\n"
            "    public static ushort[] Reinterpret(long value)\n"
            "        => new[] { (ushort)value, (ushort)(value >> 32) };   // WRONG: 2 elements, not a true reinterpretation\n"
            "}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p17-unsafe", "Unsafe drills",
        "Scoped pinning, struct reinterpretation, and the safety reasoning that makes unsafe code defensible.",
        45, "advanced", "csa-m17-pointers",
        ["csa-p17-pointer-copy", "csa-p17-marshal-cast"],
    )
    csa.register_challenge(
        "csa-p17-pointer-copy", MID,
        title="Pointer copy with scoped pinning",
        prompt=(
            "Implement `static void CopyBytes(byte[] src, int srcOffset, byte[] dst, int dstOffset, int count)` "
            "using unsafe pointer arithmetic with `fixed` — pinning BOTH arrays for the copy. Correctness test "
            "does overlapping-free copies at offsets; the lesson: pin narrowly (only the fixed block), never "
            "store the pointers, never let them escape."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "copy-correct",
                "code": (
                    "var src = new byte[] { 1, 2, 3, 4, 5, 6 };\n"
                    "var dst = new byte[6];\n"
                    "Solution.CopyBytes(src, 2, dst, 1, 3);\n"
                    'Cj.Eq(string.Join(",", dst), "0,3,4,5,0,0", "3 bytes from src[2..] into dst[1..]");'
                ),
                "hint": "fixed (byte* ps = src) fixed (byte* pd = dst) { for (int i = 0; i < count; i++) pd[dstOffset + i] = ps[srcOffset + i]; }",
            },
            {
                "name": "empty-count",
                "code": (
                    "var src = new byte[] { 9 };\n"
                    "var dst = new byte[1];\n"
                    "Solution.CopyBytes(src, 0, dst, 0, 0);\n"
                    'Cj.Eq(dst[0], 0, "count=0 copies nothing");'
                ),
                "hint": "The for-loop condition handles it; fixed on an empty segment is legal.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static unsafe void CopyBytes(byte[] src, int srcOffset, byte[] dst, int dstOffset, int count)\n"
            "    {\n"
            "        fixed (byte* ps = src)\n"
            "        fixed (byte* pd = dst)\n"
            "        {\n"
            "            for (int i = 0; i < count; i++)\n"
            "                pd[dstOffset + i] = ps[srcOffset + i];\n"
            "        }\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static unsafe void CopyBytes(byte[] src, int srcOffset, byte[] dst, int dstOffset, int count)\n"
            "    {\n"
            "        fixed (byte* ps = src)\n"
            "        fixed (byte* pd = dst)\n"
            "        {\n"
            "            for (int i = 0; i < count; i++)\n"
            "                pd[i] = ps[srcOffset + i];   // WRONG: ignores dstOffset — writes from the start\n"
            "        }\n"
            "    }\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p17-marshal-cast", MID,
        title="Struct reinterpretation",
        prompt=(
            "Implement struct `Packet { public uint Header; public uint Payload; }` and `static uint[] "
            "ReadPacketBytes(byte[] bytes)` that reinterprets an 8-byte segment as a Packet via "
            "MemoryMarshal.Read<Packet> — returning [Header, Payload] as a uint array. The test feeds "
            "little-endian bytes and verifies field values; the lesson: reinterpretation is layout-dependent "
            "and never a substitute for a real parser."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "packet-fields",
                "code": (
                    "var bytes = new byte[] { 0x78, 0x56, 0x34, 0x12, 0xEF, 0xCD, 0xAB, 0x89 };\n"
                    "var fields = Solution.ReadPacketBytes(bytes);\n"
                    'Cj.Eq(fields[0], 0x12345678u, "little-endian header");\n'
                    'Cj.Eq(fields[1], 0x89ABCDEFu, "little-endian payload");'
                ),
                "hint": "MemoryMarshal.Read<Packet>(bytes.AsSpan(0, 8)) then return [p.Header, p.Payload].",
            },
        ],
        reference=(
            "using System.Runtime.InteropServices;\n\n"
            "[StructLayout(LayoutKind.Sequential)]\n"
            "public struct Packet\n{\n"
            "    public uint Header;\n"
            "    public uint Payload;\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static uint[] ReadPacketBytes(byte[] bytes)\n"
            "    {\n"
            "        var p = MemoryMarshal.Read<Packet>(bytes.AsSpan(0, 8));\n"
            "        return new[] { p.Header, p.Payload };\n"
            "    }\n}"
        ),
        wrong=(
            "using System.Runtime.InteropServices;\n\n"
            "[StructLayout(LayoutKind.Sequential)]\n"
            "public struct Packet\n{\n"
            "    public uint Header;\n"
            "    public uint Payload;\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static uint[] ReadPacketBytes(byte[] bytes)\n"
            "    {\n"
            "        // WRONG: reads big-endian order manually instead of matching struct layout semantics\n"
            "        var header = (uint)(bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3]);\n"
            "        var payload = (uint)(bytes[4] << 24 | bytes[5] << 16 | bytes[6] << 8 | bytes[7]);\n"
            "        return new[] { header, payload };\n"
            "    }\n}"
        ),
        level="independent",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m17_boundary = r"""## Managed, unmanaged, unsafe: the boundary

Three adjectives, three different things:

- **Managed**: memory the GC owns and can move; code the runtime verifies.
  All ordinary C#.
- **Unmanaged**: memory the GC does not control (native malloc, OS
  handles, file mappings). Reached via interop APIs.
- **Unsafe**: code regions where the compiler permits *pointer*
  operations — required only when you want C-style access INSIDE the
  managed world (or at its edge). Unsafe does not mean unmanaged: most
  unsafe code operates on perfectly managed arrays.

```csharp
unsafe int Sum(int[] values)
{
    fixed (int* p = values)   // pin: promise the GC not to move it while scoped
    {
        int s = 0;
        for (int i = 0; i < values.Length; i++) s += p[i];
        return s;
    }   // unpin here — the pointer is invalid after this line
}
```

What `unsafe` lifts: pointer types (`int*`), `&address-of`, `->` member
access, `stackalloc` into pointers, direct indexing through pointers.
What it NEVER lifts: memory safety of the GC's contract (you can corrupt
anything you can address — that is the price), type-system guarantees
(pointer reinterpretation is on you), or sandbox rules (Code Journey
allows unsafe code INSIDE its hardened container; the container is the
boundary that matters).

The discipline this course demands: unsafe blocks are *small, scoped, and
non-escaping*. Pointers never become fields, never cross `await`, never
outlive their `fixed`. If you cannot draw the box around the unsafe region,
the design is wrong. `Span<T>` (Module 2) covers most of what unsafe used to
be needed for — reach for `unsafe` when spans genuinely cannot express it.
"""

_m17_boundary_vi = r"""## Managed, unmanaged, unsafe: biên giới

Ba tính từ, ba thứ khác nhau:

- **Managed**: bộ nhớ GC sở hữu và có thể di chuyển; code runtime xác minh.
  Toàn bộ C# thông thường.
- **Unmanaged**: bộ nhớ GC không kiểm soát (native malloc, handle OS, file
  mapping). Tiếp cận qua các API interop.
- **Unsafe**: vùng code nơi compiler cho phép thao tác *con trỏ* — chỉ cần
  khi bạn muốn truy cập kiểu C BÊN TRONG thế giới managed (hoặc tại rìa
  của nó). Unsafe không có nghĩa là unmanaged: phần lớn unsafe code thao
  tác trên mảng managed chính hiệu.

```csharp
unsafe int Sum(int[] values)
{
    fixed (int* p = values)   // pin: hứa với GC đừng di chuyển nó trong phạm vi này
    {
        int s = 0;
        for (int i = 0; i < values.Length; i++) s += p[i];
        return s;
    }   // unpin tại đây — con trỏ vô hiệu sau dòng này
}
```

`unsafe` nới lỏng gì: các kiểu con trỏ (`int*`), `&lấy-địa-chỉ`, truy cập
thành phần `->`, `stackalloc` vào con trỏ, đánh chỉ mục trực tiếp qua con
trỏ. Nó KHÔNG BAO GIỜ nới lỏng: tính an toàn bộ nhớ của hợp đồng GC (bạn
có thể làm hỏng bất cứ gì bạn đánh địa chỉ được — đó là cái giá), đảm bảo
hệ thống kiểu (việc diễn giải lại con trỏ là trách nhiệm của bạn), hay luật
sandbox (Code Journey cho phép unsafe code BÊN TRONG container đã gia cố
của nó; container là biên giới quan trọng).

Kỷ luật khóa học yêu cầu: khối unsafe phải *nhỏ, có phạm vi, không thoát
ra ngoài*. Con trỏ không bao giờ thành field, không bao giờ vượt `await`,
không bao giờ sống lâu hơn `fixed` của nó. Nếu bạn không vẽ được cái hộp
quanh vùng unsafe, thiết kế đã sai. `Span<T>` (Module 2) phủ được phần lớn
những gì unsafe từng cần — hãy dùng `unsafe` khi span thật sự không diễn
đạt nổi.
"""

_m17_pointers = r"""## Unsafe pointers, fixed, and pinning

The GC moves objects during compaction. A raw pointer into a managed
object would dangle after a move — so `fixed` creates a contract: within
this block, the object will not move. That is **pinning**, and pinning is
not free:

- Pinned objects fragment the heap (the GC must route compaction around
  them).
- Long pins across Gen0/1 collections degrade every collection.
- The danger window is exactly the `fixed` body — which is why the rule
  "pin narrowly" is also a performance rule, not just a safety rule.

```csharp
byte[] buffer = ...;
fixed (byte* p = buffer)          // pin: GC avoids relocating buffer
{
    NativeWrite(p, buffer.Length);   // native code reads/writes it
}   // scope ends: GC may move buffer again
```

Pointer arithmetic rules worth internalizing:

- `p[i]` on `int*` advances by 4 bytes per index — pointer arithmetic is
  element-typed, not byte-typed.
- `void*` has no element size — cast to a typed pointer before indexing.
- `&arr[0]`, `&local`, `&struct.Field` are all legal on unmanaged types.
- `stackalloc int[64]` yields an `int*` (or `Span<int>`) — stack memory, no
  pinning needed, freed on frame exit.

The modern hierarchy: spans first (`buffer.AsSpan()` — safe, optimizes to
the same code), then pointers where spans are awkward (interleaved
multi-array indexing, native interop edges). Measure before assuming the
pointer version is faster: tier-1 JIT usually compiles span code to
identical machine code — the bounds checks get eliminated by range
analysis the same way your manual checks replace them.
"""

_m17_pointers_vi = r"""## Con trỏ unsafe, fixed, và pinning

GC di chuyển object khi nén. Con trỏ thô trỏ vào managed object sẽ lơ lửng
sau một lần di chuyển — nên `fixed` tạo ra hợp đồng: trong khối này, object
sẽ không bị di chuyển. Đó là **pinning**, và pinning không miễn phí:

- Object bị pin gây phân mảnh heap (GC phải luồn nén quanh chúng).
- Pin lâu xuyên qua các lần thu Gen0/1 làm xấu mọi lần thu.
- Cửa sổ nguy hiểm đúng bằng thân `fixed` — vì thế luật "pin hẹp" cũng là
  luật hiệu năng, không chỉ luật an toàn.

```csharp
byte[] buffer = ...;
fixed (byte* p = buffer)          // pin: GC tránh dời buffer
{
    NativeWrite(p, buffer.Length);   // code native đọc/ghi nó
}   // phạm vi kết thúc: GC có thể dời buffer trở lại
```

Các luật số học con trỏ đáng thuộc:

- `p[i]` trên `int*` tiến 4 byte mỗi chỉ mục — số học con trỏ theo kiểu
  phần tử, không phải theo byte.
- `void*` không có kích thước phần tử — cast sang con trỏ có kiểu trước khi
  đánh chỉ mục.
- `&arr[0]`, `&local`, `&struct.Field` đều hợp lệ trên kiểu unmanaged.
- `stackalloc int[64]` cho một `int*` (hoặc `Span<int>`) — bộ nhớ stack,
  không cần pin, giải phóng khi thoát khung.

Phân cấp hiện đại: span trước (`buffer.AsSpan()` — an toàn, tối ưu thành
cùng code), rồi con trỏ nơi span lúng túng (đánh chỉ mục nhiều mảng xen
kẽ, rìa interop native). Hãy đo trước khi cho rằng bản con trỏ nhanh hơn:
JIT tier-1 thường compile code span thành mã máy giống hệt — việc kiểm tra
biên bị loại bởi phân tích phạm vi theo cùng cách mà các kiểm tra thủ công
của bạn thay thế nó.
"""

_m17_marshal = r"""## Interop without native libraries: Unsafe, MemoryMarshal

Most "unsafe-flavored" work happens entirely inside managed memory, with
two libraries that need no P/Invoke:

**`Unsafe`** — the light abstraction over pointers:

```csharp
// Reinterpret without copying, no pointers in sight:
int i = 42;
ref float f = ref Unsafe.As<int, float>(ref i);   // same bits, new type
```

`Unsafe.As<TFrom, TTo>` reinterprets a ref — zero cost, zero checks. It is
the expert tool: wrong type = silent garbage. Use only with proven
layouts.

**`MemoryMarshal`** — the safer face of the same tricks:

```csharp
var shorts = MemoryMarshal.Cast<long, ushort>(span);   // reinterpret a span
var bytes  = MemoryMarshal.AsBytes(span);              // any T as raw bytes
var packet = MemoryMarshal.Read<Packet>(bytes);        // struct from bytes
```

`Cast<TFrom, TTo>` views one span as another element type (same buffer,
new lens); `Read<T>/Write<T>` overlay a struct on bytes; `GetReference`
gives a managed ref to buffer element 0. All bounds-checked except the
explicitly unchecked variants.

The classic application this course drills: **zero-copy protocol
parsing**. A wire format lands as bytes; instead of allocating field
objects, you reinterpret fixed-layout segments — struct layouts declared
with `[StructLayout(LayoutKind.Sequential)]`. The technique's dangers
are the lesson: layout is platform-dependent (endianness for multi-byte
fields is the layout of the RUNNING machine — the test shows
little-endian), padding must match (`Sequential` honors declared packing),
and a version mismatch between writer and reader silently reinterprets
the wrong bytes. Real protocols ship explicit field parsing; the
reinterpret trick is for measured hot paths and proven-stable formats.

**`GCHandle`/pinned handles** complete the picture: `GCHandle.Alloc(obj,
GCHandleType.Pinned)` pins beyond a fixed block (for handing buffers to
async native work) — and must be `Free()`d, or the object stays pinned
for the process lifetime. The same leak discipline as everything else.
"""

_m17_marshal_vi = r"""## Interop không cần thư viện native: Unsafe, MemoryMarshal

Phần lớn công việc "hương unsafe" diễn ra hoàn toàn bên trong bộ nhớ
managed, với hai thư viện không cần P/Invoke:

**`Unsafe`** — lớp trừu tượng mỏng trên con trỏ:

```csharp
// Diễn giải lại mà không sao chép, không thấy con trỏ:
int i = 42;
ref float f = ref Unsafe.As<int, float>(ref i);   // cùng bit, kiểu mới
```

`Unsafe.As<TFrom, TTo>` diễn giải lại một ref — không tốn kém, không kiểm
tra. Đó là công cụ chuyên gia: sai kiểu = rác thầm lặng. Chỉ dùng với
layout đã được chứng minh.

**`MemoryMarshal`** — gương mặt an toàn hơn của cùng những thủ thuật:

```csharp
var shorts = MemoryMarshal.Cast<long, ushort>(span);   // diễn giải lại span
var bytes  = MemoryMarshal.AsBytes(span);              // T bất kỳ thành byte thô
var packet = MemoryMarshal.Read<Packet>(bytes);        // struct từ byte
```

`Cast<TFrom, TTo>` nhìn một span dưới kiểu phần tử khác (cùng buffer, kiếng
mới); `Read<T>/Write<T>` phủ một struct lên các byte; `GetReference` cho
một ref managed tới phần tử 0 của buffer. Tất cả có kiểm tra biên trừ các
biến thể tường minh không kiểm tra.

Ứng dụng kinh điển mà khóa học luyện: **parse giao thức không sao chép**.
Định dạng dây đến dưới dạng byte; thay vì cấp phát object cho từng field,
bạn diễn giải lại các đoạn layout cố định — các struct khai báo với
`[StructLayout(LayoutKind.Sequential)]`. Những nguy hiểm của kỹ thuật này
chính là bài học: layout phụ thuộc nền tảng (endianness cho field nhiều
byte là layout của máy ĐANG CHẠY — test cho thấy little-endian), padding
phải khớp (`Sequential` tôn trọng packing khai báo), và lệch phiên bản giữa
người ghi và người đọc sẽ âm thầm diễn giải nhầm byte. Giao thức thật vận
chuyển phần parse field tường minh; thủ thuật diễn giải dành cho đường nóng
đã đo và định dạng đã chứng minh ổn định.

**`GCHandle`/pinned handle** khép bức tranh: `GCHandle.Alloc(obj,
GCHandleType.Pinned)` pin vượt ra ngoài khối fixed (để đưa buffer cho công
việc native bất đồng bộ) — và phải được `Free()`, nếu không object bị pin
suốt đời process. Cùng kỷ luật rò rỉ như mọi thứ khác.
"""

_m17_pinvoke = r"""## P/Invoke concepts and the security bill

P/Invoke declares native functions for managed callers:

```csharp
[LibraryImport("libc", SetLastError = true)]   // modern source-generated interop
private static partial int chmod(string path, uint mode);
```

The mechanics worth knowing even where the sandbox forbids native calls:

- **Marshaling**: the runtime converts managed arguments to native
  representations — strings to UTF-8/UTF-16 pointers, delegates to
  function pointers, structs by value/reference per layout. Blittable
  types (int, double, fixed-layout structs of those) need NO conversion —
  they pass through unchanged, which is why blittable-heavy signatures
  are the fast ones.
- **Function pointers**: `delegate* unmanaged<int, int>` (C# 9+) gives
  C-level function pointers for callbacks; `unmanaged` callers cannot
  throw into managed code — the boundary rules work both directions.
- **Lifetime**: every native handle you receive must have exactly one
  owner. `SafeHandle` wraps the handle, increments a reference count
  across the call, and finalizes to release if you forget — the pattern
  that prevents double-free and handle-leak bugs.
- **Calling conventions and ABI**: sizes, alignment, and struct passing
  differ by platform. Cross-platform interop code declares per-platform
  signatures (`LibraryImport` + partial methods) rather than assuming.

**The security bill** — what unsafe/interop code owes the rest of the
system:

1. **Input validation moves INTO native**: a C function with a buffer
   length trusts you; the classic overflow becomes YOUR bug the moment
   you pass unchecked lengths.
2. **No sandbox inside unsafe**: the Code Journey container isolates at
   the OS level; within it, unsafe code can corrupt the process. The
   boundary is the container, not the type system — never confuse the
   two.
3. **Attack surface**: every native entry point is un-auditable by the
   C# compiler — dependency/supply-chain review (Module 23) applies
   double to native dependencies.
4. **Trimming/AOT**: dynamic P/Invoke resolves at runtime; AOT-friendly
   interop declares everything statically so the linker can see it.

The professional default: managed, spans, source-generated interop when
native is unavoidable, and a wrapper type (`SafeHandle`-shaped) owning
every handle. Unsafe code is a measured, reviewed, documented exception.
"""

_m17_pinvoke_vi = r"""## Khái niệm P/Invoke và hóa đơn bảo mật

P/Invoke khai báo các hàm native cho bên gọi managed:

```csharp
[LibraryImport("libc", SetLastError = true)]   // interop sinh mã hiện đại
private static partial int chmod(string path, uint mode);
```

Cơ chế đáng biết dù sandbox cấm gọi native:

- **Marshaling**: runtime chuyển tham số managed sang biểu diễn native —
  string thành con trỏ UTF-8/UTF-16, delegate thành function pointer,
  struct theo giá trị/tham chiếu tùy layout. Kiểu blittable (int, double,
  struct layout-cố định của những kiểu đó) KHÔNG cần chuyển đổi — chúng đi
  qua nguyên vẹn, vì sao chữ ký nhiều blittable là những chữ ký nhanh.
- **Function pointer**: `delegate* unmanaged<int, int>` (C# 9+) cho con
  trỏ hàm cấp C cho callback; caller `unmanaged` không được ném exception
  vào managed code — luật biên giới hoạt động cả hai chiều.
- **Vòng đời**: mọi handle native bạn nhận phải có đúng một chủ sở hữu.
  `SafeHandle` bọc handle, tăng ref count trong suốt lời gọi, và finalize
  để giải phóng nếu bạn quên — pattern ngăn bug double-free và rò handle.
- **Quy ước gọi và ABI**: kích thước, căn chỉnh, và cách truyền struct khác
  nhau theo nền tảng. Code interop đa nền tảng khai báo chữ ký riêng từng
  nền tảng (`LibraryImport` + partial method) thay vì giả định.

**Hóa đơn bảo mật** — những gì code unsafe/interop nợ phần còn lại của hệ
thống:

1. **Xác thực input chuyển VÀO native**: một hàm C nhận độ dài buffer sẽ
   tin bạn; lỗi tràn bộ nhớ kinh điển trở thành bug CỦA BẠN ngay khi bạn
   truyền độ dài chưa kiểm tra.
2. **Không sandbox bên trong unsafe**: container Code Journey cách ly ở
   cấp OS; trong đó, unsafe code có thể làm hỏng process. Biên giới là
   container, không phải hệ thống kiểu — đừng bao giờ nhầm lẫn.
3. **Bề mặt tấn công**: mọi điểm vào native là thứ compiler C# không kiểm
   soát được — rà soát phụ thuộc/chuỗi cung ứng (Module 23) áp dụng gấp
   đôi cho phụ thuộc native.
4. **Trimming/AOT**: P/Invoke động phân giải lúc runtime; interop thân
   thiện AOT khai báo mọi thứ tĩnh để linker nhìn thấy.

Mặc định nghề nghiệp: managed, span, interop sinh mã khi native là bất khả
kháng, và một kiểu wrapper (hình dạng `SafeHandle`) sở hữu mọi handle. Code
unsafe là một ngoại lệ đã đo, đã rà, đã ghi tài liệu.
"""

_m17_checkpoint = r"""## Checkpoint: unsafe and interop

The graded task exercises the two legitimate faces of unsafe code:
pointer arithmetic over managed memory with narrow pinning, and
reinterpretation via MemoryMarshal (no pointers at all). Practice adds the
escaping-pointer anti-pattern and struct-overlay parsing with endianness
made observable.
"""

_m17_checkpoint_vi = r"""## Checkpoint: unsafe và interop

Bài được chấm luyện hai mặt chính đáng của unsafe code: số học con trỏ
trên bộ nhớ managed với pin hẹp, và diễn giải lại qua MemoryMarshal
(hoàn toàn không cần con trỏ). Practice thêm anti-pattern con trỏ thoát
ra ngoài và phần parse phủ struct với endianness trở nên quan sát được.
"""
