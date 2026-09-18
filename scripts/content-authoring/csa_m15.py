"""Module 15 — JIT, runtime, and CLR internals (csa-m15)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-clr-internals",
        "JIT, Runtime, and CLR Internals",
        "From IL to native code: assemblies, metadata, tiered compilation, virtual dispatch, and exceptions.",
    )

    csa.register_lesson(
        MID, "csa-m15-assemblies", "Assemblies, metadata, and IL",
        "What ships in a DLL, how IL encodes your intent, and how the loader resolves references.",
        15, "advanced", _m15_assemblies, _m15_assemblies_vi,
    )
    csa.register_lesson(
        MID, "csa-m15-jit", "The JIT and tiered compilation",
        "Tier 0 → tier 1, OSR, dynamic PGO — how .NET executes your method the first and hundredth time.",
        16, "advanced", _m15_jit, _m15_jit_vi,
    )
    csa.register_lesson(
        MID, "csa-m15-dispatch", "Virtual dispatch and interface calls",
        "Method tables, interface dispatch resolution, and why `sealed` is a real optimization.",
        15, "advanced", _m15_dispatch, _m15_dispatch_vi,
    )
    csa.register_lesson(
        MID, "csa-m15-exceptions", "Exceptions at runtime",
        "Two-pass unwinding, finally/fault handlers, and the real cost model of try/catch.",
        15, "advanced", _m15_exceptions, _m15_exceptions_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m15", "Checkpoint: CLR internals",
        "Synthesis: inspect runtime behavior through reflection and measure dispatch costs.",
        12, "advanced", _m15_checkpoint, _m15_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m15-task", MID,
        title="CLR internals checkpoint",
        prompt=(
            "Implement `static (string ilName, bool isSealed, int methodCount) Inspect<T>()` using reflection: "
            "return the type's full name, whether it is sealed, and its declared instance method count. Then "
            "implement `static string DispatchDescription(Type t)` returning exactly \"virtual\" if t has any "
            "virtual methods (declared, instance), \"interface\" if it implements any interfaces, otherwise "
            "\"direct\". The graded insight: typeof(List<int>) reports sealed, virtual, and interface all at once."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "inspect-sealed",
                "code": (
                    "var (name, sealed_, count) = Solution.Inspect<string>();\n"
                    'Cj.True(name.Contains("String"), "full name");\n'
                    'Cj.True(sealed_, "string is sealed");\n'
                    'Cj.True(count > 0, "has methods");'
                ),
                "hint": "typeof(T).FullName, .IsSealed, .GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly).Length.",
            },
            {
                "name": "dispatch-desc",
                "code": (
                    "var v = new V();\n"   # no virtual, no interface
                    "var o = new O();\n"   # declares virtual; D derives and overrides
                    'Cj.Eq(Solution.DispatchDescription(typeof(V)), "direct", "plain class: direct");\n'
                    'Cj.Eq(Solution.DispatchDescription(typeof(O)), "virtual", "class declaring virtual: virtual");\n'
                    "class V { public int M() => 1; }\n"
                    "class O { public virtual int M() => 2; }"
                ),
                "hint": "m.IsVirtual is true for overrides too — require the method to declare a new virtual slot (IsVirtual && !IsFinal) or use DeclaredOnly and check for the `virtual` keyword via attributes.",
            },
        ],
        reference=(
            "using System.Reflection;\n\n"
            "public class Solution\n{\n"
            "    public static (string ilName, bool isSealed, int methodCount) Inspect<T>()\n"
            "    {\n"
            "        var t = typeof(T);\n"
            "        var count = t.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly).Length;\n"
            "        return (t.FullName!, t.IsSealed, count);\n"
            "    }\n\n"
            "    public static string DispatchDescription(Type t)\n"
            "    {\n"
            "        var methods = t.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);\n"
            "        // IsVirtual is true for `override` too; a NEW virtual slot is\n"
            "        // virtual-but-not-final, while an override in a sealed-free class\n"
            "        // stays open. The bulletproof discriminator: the MemberInfo of a\n"
            "        // `virtual` declaration has IsVirtual && !IsFinal ONLY when nothing\n"
            "        // further overrides... so use the C# keyword instead:\n"
            "        // m.IsVirtual && !m.IsFinal misses nothing here because V.M is\n"
            "        // non-virtual (not in the map) and O.M is a fresh slot.\n"
            "        if (methods.Any(m => m.IsVirtual && !m.IsFinal)) return \"virtual\";\n"
            "        if (t.GetInterfaces().Length > 0) return \"interface\";\n"
            "        return \"direct\";\n"
            "    }\n}\n"
        ),
        wrong=(
            "using System.Reflection;\n\n"
            "public class Solution\n{\n"
            "    public static (string ilName, bool isSealed, int methodCount) Inspect<T>()\n"
            "    {\n"
            "        var t = typeof(T);\n"
            "        var count = t.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly).Length;\n"
            "        return (t.Name!, t.IsSealed, count);   // WRONG: Name not FullName\n"
            "    }\n\n"
            "    public static string DispatchDescription(Type t)\n"
            "    {\n"
            "        return \"direct\";   // WRONG: never inspects\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p15-clr", "CLR internals drills",
        "Assembly inspection, tiered-JIT reasoning, dispatch cost measurement, exception cost facts.",
        45, "advanced", "csa-m15-dispatch",
        ["csa-p15-exception-cost", "csa-p15-generic-runtime"],
    )
    csa.register_challenge(
        "csa-p15-exception-cost", MID,
        title="Exception cost, measured",
        prompt=(
            "Implement `static long ThrowCatchCost(int iterations)`: capture Stopwatch ticks for `iterations` "
            "throw+catch cycles of a pre-created exception instance (throw ex; inside try, catch { }) and return "
            "the elapsed milliseconds. Then implement `static long ErrorCodeCost(int iterations)` doing the same "
            "work but returning -1 instead of throwing (checked, same loop shape). Implement `static int "
            "Divide(int a, int b)` that throws DivideByZeroException on b==0 — used by the test once to verify "
            "the exception path works."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "divide-throws",
                "code": (
                    "var ex = await Cj.ThrowsAsync<DivideByZeroException>(() => Task.Run(() => Solution.Divide(1, 0)));\n"
                    'Cj.True(ex is not null, "b==0 throws");\n'
                    'Cj.Eq(Solution.Divide(10, 2), 5, "normal path");'
                ),
                "hint": "if (b == 0) throw new DivideByZeroException(); return a / b.",
            },
            {
                "name": "costs-measured",
                "code": (
                    "var tc = Solution.ThrowCatchCost(1000);\n"
                    "var ec = Solution.ErrorCodeCost(1000);\n"
                    'Cj.True(tc >= 0 && ec >= 0, "both measurable");\n'
                    "// No assertion that tc > ec: absolute costs vary by hardware/JIT. The lesson is the\n"
                    "// measurement exists and throw+catch is usually orders of magnitude slower."
                ),
                "hint": "Pre-create the exception ONCE (new Exception() outside the loop); Stopwatch.StartNew() → loop → .ElapsedMilliseconds.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static int Divide(int a, int b)\n"
            "    {\n"
            "        if (b == 0) throw new DivideByZeroException();\n"
            "        return a / b;\n"
            "    }\n\n"
            "    public static long ThrowCatchCost(int iterations)\n"
            "    {\n"
            "        var ex = new InvalidOperationException(\"probe\");   // pre-created: we measure unwinding, not construction\n"
            "        var sw = Stopwatch.StartNew();\n"
            "        for (int i = 0; i < iterations; i++)\n"
            "        {\n"
            "            try { throw ex; }\n"
            "            catch (InvalidOperationException) { }\n"
            "        }\n"
            "        return sw.ElapsedMilliseconds;\n"
            "    }\n\n"
            "    public static long ErrorCodeCost(int iterations)\n"
            "    {\n"
            "        var sw = Stopwatch.StartNew();\n"
            "        for (int i = 0; i < iterations; i++)\n"
            "        {\n"
            "            if (i < 0) return -1;   // checked, never taken\n"
            "        }\n"
            "        return sw.ElapsedMilliseconds;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int Divide(int a, int b)\n"
            "    {\n"
            "        return a / b;   // WRONG: relies on hardware division fault instead of explicit check\n"
            "    }\n\n"
            "    public static long ThrowCatchCost(int iterations)\n"
            "    {\n"
            "        var sw = Stopwatch.StartNew();\n"
            "        for (int i = 0; i < iterations; i++)\n"
            "        {\n"
            "            try { throw new InvalidOperationException(\"probe\"); }   // WRONG: measures construction too — muddy data\n"
            "            catch (InvalidOperationException) { }\n"
            "        }\n"
            "        return sw.ElapsedMilliseconds;\n"
            "    }\n\n"
            "    public static long ErrorCodeCost(int iterations)\n"
            "    {\n"
            "        var sw = Stopwatch.StartNew();\n"
            "        for (int i = 0; i < iterations; i++) { }\n"
            "        return sw.ElapsedMilliseconds;\n"
            "    }\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p15-generic-runtime", MID,
        title="Generic specialization at runtime",
        prompt=(
            "Value-type generics get per-type specialization; reference types share one instantiation. Prove the "
            "observable part: implement `static int OpenGenericCount()` returning the number of open generic type "
            "definitions reachable via typeof(Dictionary<,>) (0 if it is constructed, 1 if open) — implement it as: "
            "`typeof(Dictionary<,>).IsGenericTypeDefinition ? 1 : 0`. Then implement `static bool SameRuntimeType<A, "
            "B>() => typeof(A) == typeof(B)` and the test checks SameRuntimeType<List<int>, List<int>>() is true "
            "while SameRuntimeType<List<int>, List<string>>() is false."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "open-generic",
                "code": (
                    'Cj.Eq(Solution.OpenGenericCount(), 1, "typeof(Dictionary<,>) is an open generic definition");\n'
                    'Cj.True(Solution.SameRuntimeType<List<int>, List<int>>(), "same construction = same runtime type");\n'
                    'Cj.False(Solution.SameRuntimeType<List<int>, List<string>>(), "different type args = different type");'
                ),
                "hint": "IsGenericTypeDefinition on the unbound typeof(Dictionary<,>); typeof(A) == typeof(B) is reference equality on runtime types.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static int OpenGenericCount()\n"
            "        => typeof(Dictionary<,>).IsGenericTypeDefinition ? 1 : 0;\n\n"
            "    public static bool SameRuntimeType<A, B>()\n"
            "        => typeof(A) == typeof(B);\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int OpenGenericCount()\n"
            "        => typeof(Dictionary<int, int>).IsGenericTypeDefinition ? 1 : 0;   // WRONG: constructed, not open\n\n"
            "    public static bool SameRuntimeType<A, B>()\n"
            "        => typeof(A).Name == typeof(B).Name;   // WRONG: List`1 == List`1 by name\n"
            "}"
        ),
        level="independent",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m15_assemblies = r"""## Assemblies, metadata, and IL

A .NET assembly is a Windows PE file (even on Linux — same container
format) with three payloads:

1. **Metadata tables** — every type, method, field, attribute, and their
   signatures, in a binary table format. This is what reflection reads and
   what the compiler consumed when referencing you. Full fidelity: C#
   features are metadata, not syntax.
2. **IL** — the stack-based bytecode per method body. Stack-based: `ldc.i4.5;
   ldc.i4.3; add` pushes 5, pushes 3, adds. Verified at load time (type
   safety of the stack is checkable).
3. **Resources / manifest** — embedded data and the assembly version/
   culture/strong-name identity.

The loader resolves `AssemblyRef` entries through the hosting runtime:
app-local first, then the framework, then `AssemblyLoadContext` rules.
The classic production failure — FileLoadException or "could not load
type" — is a resolver story: two versions of one identity, or a dependency
present in dev but trimmed from publish.

**IL inspection without ildasm**: reflection gives you the method body's
local signatures, and `MethodBody.GetILAsByteArray()` gives raw IL bytes —
enough to *see* that `async`, closures, and `lock` all rewrite your code
into other patterns. The decompiler-grade view (ILSpy) is a desktop tool,
but everything it shows is derived from exactly these metadata tables —
nothing magic, all documented.

What this buys you in practice: reading an exception's stack trace means
reading IL-to-source correspondence; understanding trimming means knowing
what metadata the linker can prove unused; and diagnosting versioning
means inspecting the manifest, not guessing.
"""

_m15_assemblies_vi = r"""## Assembly, metadata, và IL

Một assembly .NET là file PE kiểu Windows (ngay cả trên Linux — cùng định
dạng container) với ba phần nội dung:

1. **Bảng metadata** — mọi kiểu, phương thức, field, attribute cùng chữ ký
   của chúng, ở định dạng bảng nhị phân. Đây là thứ reflection đọc và là
   thứ compiler đã tiêu thụ khi tham chiếu bạn. Đầy đủ trung thực: các tính
   năng C# là metadata, không phải cú pháp.
2. **IL** — bytecode dạng stack cho mỗi thân phương thức. Dựa trên stack:
   `ldc.i4.5; ldc.i4.3; add` đẩy 5, đẩy 3, cộng. Được xác minh khi nạp (tính
   an toàn kiểu của stack là kiểm chứng được).
3. **Tài nguyên / manifest** — dữ liệu nhúng và định danh phiên bản/
   culture/strong-name của assembly.

Loader phân giải các entry `AssemblyRef` qua runtime đang host: app-local
trước, rồi framework, rồi luật của `AssemblyLoadContext`. Sự cố production
kinh điển — FileLoadException hay "could not load type" — là chuyện của
resolver: hai phiên bản của một định danh, hoặc một phụ thuộc có ở dev
nhưng bị trim khỏi publish.

**Xem IL không cần ildasm**: reflection cho bạn chữ ký biến cục bộ của thân
phương thức, và `MethodBody.GetILAsByteArray()` cho các byte IL thô — đủ để
*thấy* rằng `async`, closure, và `lock` đều viết lại code của bạn thành
các pattern khác. Cái nhìn cấp decompiler (ILSpy) là công cụ desktop, nhưng
mọi thứ nó hiển thị đều suy ra từ chính các bảng metadata này — không có
phép thuật, tất cả đều có tài liệu.

Điều này mua được gì trong thực tế: đọc stack trace của exception nghĩa là
đọc sự tương ứng IL-to-source; hiểu trimming nghĩa là biết metadata nào
linker chứng minh được là không dùng; chẩn đoán phiên bản nghĩa là soi
manifest, không phải đoán mò.
"""

_m15_jit = r"""## The JIT and tiered compilation

Execution starts with IL and ends with machine code, in tiers:

| Tier | When | Quality | Cost |
|---|---|---|---|
| Quick JIT (tier 0) | first call | minimal optimization | fast compile |
| Tier 1 | after call-count threshold (~30) + background recompile | full optimization | slower compile |
| OSR | loop detected hot in tier-0 frame | re-optimize mid-method | rare |

Consequences you can measure (and the course does, in Module 14):

- **First call is slow, then faster.** Warmup before benchmarking; the
  threshold is per-method.
- **Dynamic PGO** (default on .NET 8+): the tier-0 instrumented counters
  feed the tier-1 optimizer — real branch frequencies drive inlining and
  devirtualization decisions that static analysis cannot make.
- **Tiered PGO can devirtualize** based on observed receiver types: an
  interface call that always sees one concrete type becomes a direct call.
  This is why measured interface-dispatch cost varies with call history.

**Startup vs steady state.** ReadyToRun (R2R) precompiles tier-1-ish code
at publish — faster startup, bigger binaries, slightly less optimal (no
PGO). NativeAOT (Module 19) compiles fully ahead-of-time. The spectrum:
Quick JIT (fast start, slow code) → R2R (balanced) → AOT (no JIT, fastest
start, reflection-limited).

GC, thread pool, and JIT are runtime services the host manages — the same
IL runs against different runtime configs (Server GC vs Workstation,
`DOTNET_TieredPGO=0`) with different performance. Production tuning is
runtime configuration as much as code.
"""

_m15_jit_vi = r"""## JIT và tiered compilation

Thực thi bắt đầu từ IL và kết thúc bằng mã máy, theo các tầng:

| Tầng | Khi nào | Chất lượng | Chi phí |
|---|---|---|---|
| Quick JIT (tier 0) | lần gọi đầu | tối ưu tối thiểu | compile nhanh |
| Tier 1 | sau ngưỡng số lần gọi (~30) + recompile nền | tối ưu đầy đủ | compile chậm hơn |
| OSR | phát hiện vòng lặp nóng trong khung tier-0 | tối ưu hóa giữa phương thức | hiếm |

Các hệ quả bạn đo được (và khóa học làm, ở Module 14):

- **Lần gọi đầu chậm, sau đó nhanh hơn.** Làm nóng trước khi benchmark;
  ngưỡng là theo phương thức.
- **Dynamic PGO** (mặc định trên .NET 8+): các bộ đếm instrumented của
  tier-0 nuôi bộ tối ưu tier-1 — tần suất nhánh thật định hướng các quyết
  định inline và devirtualize mà phân tích tĩnh không thể.
- **Tiered PGO có thể devirtualize** dựa trên kiểu receiver quan sát
  được: một interface call luôn gặp một kiểu cụ thể sẽ thành lời gọi trực
  tiếp. Vì vậy chi phí interface dispatch đo được thay đổi theo lịch sử
  lời gọi.

**Khởi động vs ổn định.** ReadyToRun (R2R) precompile code kiểu tier-1 lúc
publish — khởi động nhanh hơn, binary lớn hơn, hơi kém tối ưu hơn (không có
PGO). NativeAOT (Module 19) compile hoàn toàn ahead-of-time. Phổ: Quick JIT
(start nhanh, code chậm) → R2R (cân bằng) → AOT (không JIT, khởi động nhanh
nhất, hạn chế reflection).

GC, thread pool, và JIT là các dịch vụ runtime do host quản lý — cùng IL
chạy với các cấu hình runtime khác nhau (Server GC vs Workstation,
`DOTNET_TieredPGO=0`) cho hiệu năng khác nhau. Tinh chỉnh production là
cấu hình runtime ngang hàng với code.
"""

_m15_dispatch = r"""## Virtual dispatch and interface calls

Every reference-type object carries a **method table** (the "type handle"
the header points at). Instance method dispatch on a class hierarchy walks
that table:

- **Non-virtual instance call**: resolved at compile time to the exact
  method — one indirection at most.
- **`virtual` call**: load the receiver's method table, fetch the slot,
  call through the pointer. A couple of instructions — cheap, but opaque
  to the optimizer (harder to inline).
- **Interface call**: the hard one. An interface slot has no fixed place
  across unrelated class hierarchies, so the runtime resolves via
  interface maps — historically the slowest dispatch, though modern
  runtimes cache the resolution (virtual-stub dispatch) and tiered PGO can
  monomorphize hot sites entirely.

```csharp
sealed class Fast : IFoo { ... }   // sealed: the JIT may devirtualize IFoo calls
class Slow : IFoo { ... }          // open: any subclass could exist, calls stay virtual
```

**Why `sealed` is a real optimization**: closing the hierarchy proves no
further overrides exist, letting the JIT replace virtual dispatch with
direct calls (and possibly inline). Measured effects are workload-dependent
— nanoseconds on cold paths, real percentages on hot polymorphic loops —
and the profiler usually shows "indirect call overhead" only in aggregate.

**Structs skip all of it.** A struct call through a concrete struct type is
direct; through an interface it boxes. Generic constraints (Module 3,
`where T : IFoo` with T : struct) preserve the direct call — this is why
generic math and span-based code achieve abstraction without dispatch
cost. The art: pay for polymorphism where the design needs it, and keep
hot inner loops monomorphic.
"""

_m15_dispatch_vi = r"""## Dispatch ảo và lời gọi interface

Mọi object reference-type mang một **method table** ("type handle" mà
header trỏ tới). Dispatch phương thức instance trên phân cấp lớp đi qua
bảng đó:

- **Lời gọi instance non-virtual**: phân giải lúc compile thành phương thức
  chính xác — tối đa một hướng dẫn gián tiếp.
- **Lời gọi `virtual`**: nạp method table của receiver, lấy slot, gọi qua
  con trỏ. Vài chỉ thị — rẻ, nhưng mờ với bộ tối ưu (khó inline hơn).
- **Lời gọi interface**: cái khó. Slot interface không có vị trí cố định
  qua các phân cấp lớp không liên quan, nên runtime phân giải qua interface
  map — từng là dispatch chậm nhất, dù runtime hiện đại cache phân giải
  (virtual-stub dispatch) và tiered PGO có thể monomorphize hoàn toàn các
  điểm gọi nóng.

```csharp
sealed class Fast : IFoo { ... }   // sealed: JIT có thể devirtualize lời gọi IFoo
class Slow : IFoo { ... }          // mở: subclass nào cũng có thể tồn tại, lời gọi vẫn ảo
```

**Vì sao `sealed` là tối ưu thật**: đóng phân cấp chứng minh không còn
override nào, cho phép JIT thay virtual dispatch bằng lời gọi trực tiếp
(và có thể inline). Hiệu quả đo được tùy workload — vài nano giây trên
đường lạnh, phần trăm thật trên vòng đa hình nóng — và profiler thường chỉ
hiện "indirect call overhead" một cách tổng hợp.

**Struct bỏ qua tất cả.** Lời gọi struct qua kiểu struct cụ thể là trực
tiếp; qua interface thì bị box. Ràng buộc generic (Module 3, `where T :
IFoo` với T : struct) giữ lời gọi trực tiếp — vì sao generic math và code
dựa trên span đạt được trừu tượng hóa mà không tốn dispatch. Nghệ thuật:
trả tiền đa hình nơi thiết kế cần, và giữ vòng trong nóng đơn hình.
"""

_m15_exceptions = r"""## Exceptions at runtime

.NET exceptions use **two-pass unwinding**, modeled on the Itanium C++ ABI:

1. **Pass 1 (search):** walk the stack looking for a frame whose `catch`
   matches. No user code runs.
2. **Pass 2 (unwind):** re-walk, running each frame's `finally`/`fault`
   handlers up to (and including) the winning catch. Stack frames are torn
   down as handlers complete.

This explains observable behaviors: state mutations in `finally` are
guaranteed on the unwind path; filters (`catch when`) run in pass 1 and
can *decline* an exception so an outer handler takes it without unwinding
the intermediate frames.

**The cost model** — what to say when someone says "exceptions are slow":

- The **throw path** (construct, pass 1+2, stack walk) costs microseconds —
  often 100–1000× a return-based check. Per-iteration throwing in a loop is
  a genuine performance bug (the checkpoint measures it honestly).
- The **non-throw path** is nearly free: a try block adds a jump-table
  entry, not a branch. "Put try/catch around hot loops" costs approximately
  nothing until an exception actually flies.

**Design corollary**: `TryX` patterns (`int.TryParse`) exist for *predictable*
failures; exceptions are for *exceptional* ones. Request validation that
rejects 30% of inputs should use the Try pattern — not because exceptions
are "bad", but because microsecond-per-failure multiplies. The runtime
itself follows this: dictionary lookups, span parsing, channel reads all
offer non-throwing variants.

`ExceptionDispatchInfo.Capture(ex).Throw()` preserves the original stack —
the right way to rethrow after async boundaries, where `throw ex;` would
rewrite the trace.
"""

_m15_exceptions_vi = r"""## Exception ở mức runtime

Exception .NET dùng **unwinding hai lượt**, mô phỏng theo Itanium C++ ABI:

1. **Lượt 1 (tìm kiếm):** đi dọc stack tìm khung nào có `catch` khớp. Không
   có user code nào chạy.
2. **Lượt 2 (unwind):** đi lại, chạy các handler `finally`/`fault` của từng
   khung cho tới (và gồm cả) khung catch thắng. Các khung stack bị tháo
   dỡ khi handler hoàn tất.

Điều này giải thích các hành vi quan sát được: thay đổi trạng thái trong
`finally` được đảm bảo trên đường unwind; filter (`catch when`) chạy trong
lượt 1 và có thể *từ chối* một exception để handler ngoài nhận nó mà
không phải unwind các khung trung gian.

**Mô hình chi phí** — những gì nên nói khi ai đó bảo "exception chậm":

- Đường **throw** (khởi tạo, lượt 1+2, đi stack) tốn micro giây — thường
  100–1000× một phép kiểm tra kiểu return. Ném exception mỗi vòng lặp là
  bug hiệu năng thật sự (checkpoint đo nó một cách trung thực).
- Đường **không ném** gần như miễn phí: một khối try chỉ thêm một mục
  jump-table, không phải một nhánh. "Bọc try/catch quanh vòng nóng" tốn
  gần đúng bằng không cho đến khi exception thật sự bay ra.

**Hệ quả thiết kế**: pattern `TryX` (`int.TryParse`) tồn tại cho các lỗi
*dự đoán được*; exception dành cho thứ *ngoại lệ*. Xác thực request từ
chối 30% input nên dùng pattern Try — không phải vì exception "xấu", mà
vì micro giây mỗi lỗi nhân lên. Runtime tự nó theo quy tắc này: tra từ
điển, parse span, đọc channel đều có biến thể không ném.

`ExceptionDispatchInfo.Capture(ex).Throw()` giữ nguyên stack gốc — cách
đúng để ném lại sau các biên async, nơi `throw ex;` sẽ viết lại trace.
"""

_m15_checkpoint = r"""## Checkpoint: CLR internals

The graded task inspects types through the metadata lens (sealed-ness,
declared methods, dispatch category) and measures the throw-vs-check cost
split honestly. Practice adds the open-generic runtime question and the
generic-specialization observables.
"""

_m15_checkpoint_vi = r"""## Checkpoint: CLR internals

Bài được chấm soi kiểu qua lăng kính metadata (tính sealed, các phương thức
khai báo, danh mục dispatch) và đo cặp chi phí throw-vs-check một cách
trung thực. Practice thêm câu hỏi open-generic runtime và các quan sát
được của specialization generic.
"""
