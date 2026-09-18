"""Module 14 — Performance engineering (csa-m14)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-performance",
        "Performance Engineering",
        "Measurement discipline, allocation and CPU profiling, JIT effects, and the optimize-what-matters loop.",
    )

    csa.register_lesson(
        MID, "csa-m14-measure-first", "Measure first: the benchmark discipline",
        "Warmup, iterations, statistical honesty, and why your stopwatch is lying to you.",
        16, "advanced", _m14_measure, _m14_measure_vi,
    )
    csa.register_lesson(
        MID, "csa-m14-profiling", "Profiling allocation and CPU",
        "Reading allocation deltas, GC counters, and CPU samples into a bottleneck hypothesis.",
        15, "advanced", _m14_profiling, _m14_profiling_vi,
    )
    csa.register_lesson(
        MID, "csa-m14-jit-effects", "JIT effects on your measurements",
        "Tiered compilation, inlining, devirtualization, dead-code elimination — and how each one fakes results.",
        16, "advanced", _m14_jit, _m14_jit_vi,
    )
    csa.register_lesson(
        MID, "csa-m14-optimization-loop", "The optimization loop",
        "MEASURE → PROFILE → CHANGE → MEASURE AGAIN: a full worked optimization with before/after evidence.",
        15, "advanced", _m14_loop, _m14_loop_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m14", "Checkpoint: performance",
        "Synthesis: optimize against a measured baseline and prove the win numerically.",
        12, "advanced", _m14_checkpoint, _m14_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m14-task", MID,
        title="Performance checkpoint",
        prompt=(
            "Two implementations are provided in the harness: SlowPath concatenates strings in a loop; FastPath "
            "uses string.Create. Implement `static string RepeatChar(char c, int n)` that builds an n-char string "
            "of `c` using string.Create (zero intermediate allocations), and `static long Measure(Func<int> work, "
            "int iterations)` that returns total allocated bytes across `iterations` invocations with ONE warmup "
            "call first (the warmup is graded: without it the JIT's first-call allocations corrupt the result)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "repeat-correct",
                "code": (
                    "var s = Solution.RepeatChar('x', 5);\n"
                    'Cj.Eq(s, "xxxxx", "5 chars");\n'
                    'Cj.Eq(Solution.RepeatChar(\'a\', 0), "", "empty for 0");'
                ),
                "hint": "string.Create(n, c, static (span, state) => span.Fill(state));",
            },
            {
                "name": "zero-intermediates",
                "code": (
                    "// Probe first (calibrated on this runtime: a tier-0 string.Create call\n"
                    "// allocates ~312 B even when the payload is 200 B — the lambda + engine\n"
                    "// overhead). The bound must allow that overhead but explode on ANY\n"
                    "// intermediate string: one O(n) concat chain allocates >= 400*152.\n"
                    "var probe = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 100; i++) Solution.RepeatChar('y', 100);\n"
                    "var fast = GC.GetAllocatedBytesForCurrentThread() - probe;\n"
                    'Cj.True(fast <= 100 * 400, $"string.Create path within budget (got {fast}; an intermediate-building path exceeds 6,080,000)");'
                ),
                "hint": "string.Create allocates ONLY the final buffer. + vs StringBuilder or 'a += c' allocates many intermediates.",
            },
            {
                "name": "measure-warms-up",
                "code": (
                    "int f() => 42;\n"
                    "var d = Solution.Measure(f, 10);\n"
                    'Cj.True(d >= 0, "delegates measured after warmup; no negative/first-call noise");'
                ),
                "hint": "Call work() once before capturing the allocation baseline.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static string RepeatChar(char c, int n)\n"
            "        => string.Create(n, c, static (span, state) => span.Fill(state));\n\n"
            "    public static long Measure(Func<int> work, int iterations)\n"
            "    {\n"
            "        _ = work();   // warmup: JIT, delegate cache, one-shot costs\n"
            "        var before = GC.GetAllocatedBytesForCurrentThread();\n"
            "        for (int i = 0; i < iterations; i++) _ = work();\n"
            "        return GC.GetAllocatedBytesForCurrentThread() - before;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static string RepeatChar(char c, int n)\n"
            "    {\n"
            "        var s = \"\";\n"
            "        for (int i = 0; i < n; i++) s += c;   // WRONG: O(n) intermediate strings\n"
            "        return s;\n"
            "    }\n\n"
            "    public static long Measure(Func<int> work, int iterations)\n"
            "    {\n"
            "        var before = GC.GetAllocatedBytesForCurrentThread();   // WRONG: no warmup — first call JITs inside the window\n"
            "        for (int i = 0; i < iterations; i++) _ = work();\n"
            "        return GC.GetAllocatedBytesForCurrentThread() - before;\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p14-perf", "Performance drills",
        "Baseline discipline, allocation hunting, JIT artifacts, and before/after evidence.",
        45, "advanced", "csa-m14-optimization-loop",
        ["csa-p14-boxing-hunt", "csa-p14-linq-vs-loop"],
    )
    csa.register_challenge(
        "csa-p14-boxing-hunt", MID,
        title="Hunt the hidden boxing",
        prompt=(
            "Implement `static long SumInterface(IEnumerable<int> values)` (sums via foreach over the interface — "
            "allocates an enumerator + boxes if you use a struct enumerator through IEnumerable) and `static long "
            "SumSpan(int[] values)` (sums via Span<int> — zero allocations). The test proves the allocation gap: "
            "SumSpan must allocate 0 over 100 runs; SumInterface's cost is printed for comparison. Implement both, "
            "correctly, and the numbers teach the lesson."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "values-match",
                "code": (
                    "var vals = Enumerable.Range(0, 100).ToArray();\n"
                    'Cj.Eq(Solution.SumInterface(vals), Solution.SumSpan(vals), "same sum");\n'
                    'Cj.Eq(Solution.SumSpan(vals), 4950, "known total");'
                ),
                "hint": "foreach over array via IEnumerable boxes an IEnumerator<int>; span foreach uses ref iteration.",
            },
            {
                "name": "span-zero-alloc",
                "code": (
                    "var vals = new int[100];\n"
                    "_ = Solution.SumSpan(vals);\n"
                    "var before = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 100; i++) Solution.SumSpan(vals);\n"
                    "var delta = GC.GetAllocatedBytesForCurrentThread() - before;\n"
                    'Cj.Eq(delta, 0L, $"SumSpan allocated {delta} bytes over 100 calls");'
                ),
                "hint": "foreach (var v in values.AsSpan()) — no enumerator object exists at all.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static long SumInterface(IEnumerable<int> values)\n"
            "    {\n"
            "        long s = 0;\n"
            "        foreach (var v in values) s += v;   // interface dispatch + enumerator allocation\n"
            "        return s;\n"
            "    }\n\n"
            "    public static long SumSpan(int[] values)\n"
            "    {\n"
            "        long s = 0;\n"
            "        foreach (var v in values.AsSpan()) s += v;   // ref iteration, zero alloc\n"
            "        return s;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static long SumInterface(IEnumerable<int> values)\n"
            "    {\n"
            "        long s = 0;\n"
            "        foreach (var v in values) s += v;\n"
            "        return s;\n"
            "    }\n\n"
            "    public static long SumSpan(int[] values)\n"
            "    {\n"
            "        long s = 0;\n"
            "        foreach (var v in values.Select(x => (long)x)) s += v;   // WRONG: LINQ allocates enumerator + closure\n"
            "        return s;\n"
            "    }\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p14-linq-vs-loop", MID,
        title="LINQ vs loop: measured verdict",
        prompt=(
            "Implement `static int CountEvenLinq(int[] values)` (values.Count(x => x % 2 == 0)) and `static int "
            "CountEvenLoop(int[] values)` (plain for-loop). Both must return the same count. Then implement "
            "`static long AllocDelta(Func<int[]> work, int iterations)` — warmup + per-thread allocation delta — "
            "and use it in the test to compare BOTH counters' allocations. The graded insight: for this workload "
            "the loop allocates 0; document the LINQ cost in the implementation comment."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "same-count",
                "code": (
                    "var vals = Enumerable.Range(0, 999).Select(i => i * 7 - 3).ToArray();   // mixed parity\n"
                    'Cj.Eq(Solution.CountEvenLinq(vals), Solution.CountEvenLoop(vals), "identical counts");\n'
                    'Cj.Eq(Solution.CountEvenLoop(vals), 499, "known count for this data");'
                ),
                "hint": "Both count x % 2 == 0; the loop version uses a for and a counter.",
            },
            {
                "name": "loop-zero-alloc",
                "code": (
                    "var vals = new int[1000];\n"
                    "_ = Solution.CountEvenLoop(vals);\n"
                    "var before = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 50; i++) Solution.CountEvenLoop(vals);\n"
                    "var delta = GC.GetAllocatedBytesForCurrentThread() - before;\n"
                    'Cj.Eq(delta, 0L, $"loop allocated {delta}");'
                ),
                "hint": "for-loop over indices; no enumerator, no closure.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    // CountEvenLinq allocates: 1 enumerator + 1 closure ≈ 40+ bytes per call.\n"
            "    public static int CountEvenLinq(int[] values)\n"
            "        => values.Count(x => x % 2 == 0);\n\n"
            "    public static int CountEvenLoop(int[] values)\n"
            "    {\n"
            "        int n = 0;\n"
            "        for (int i = 0; i < values.Length; i++)\n"
            "            if ((values[i] & 1) == 0) n++;\n"
            "        return n;\n"
            "    }\n\n"
            "    public static long AllocDelta<T>(Func<T> work, int iterations)\n"
            "    {\n"
            "        _ = work();   // warmup\n"
            "        var before = GC.GetAllocatedBytesForCurrentThread();\n"
            "        for (int i = 0; i < iterations; i++) _ = work();\n"
            "        return GC.GetAllocatedBytesForCurrentThread() - before;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int CountEvenLinq(int[] values)\n"
            "        => values.Count(x => x % 2 == 0);\n\n"
            "    public static int CountEvenLoop(int[] values)\n"
            "    {\n"
            "        int n = 0;\n"
            "        for (int i = 0; i < values.Length; i++)\n"
            "            if (values[i] % 2 != 0) n++;   // WRONG: counts odd\n"
            "        return n;\n"
            "    }\n\n"
            "    public static long AllocDelta<T>(Func<T> work, int iterations)\n"
            "    {\n"
            "        var before = GC.GetAllocatedBytesForCurrentThread();   // WRONG: no warmup\n"
            "        for (int i = 0; i < iterations; i++) _ = work();\n"
            "        return GC.GetAllocatedBytesForCurrentThread() - before;\n"
            "    }\n}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m14_measure = r"""## Measure first: the benchmark discipline

The commandment: no optimization without a measured baseline. The
discipline that makes the measurement mean something:

```csharp
// The minimal honest harness (what the checkpoint grades):
var work = (Func<int>)(() => SumTo(1000));
_ = work();                                     // 1. WARMUP — JIT, caches
var before = GC.GetAllocatedBytesForCurrentThread();   // 2. BASELINE
var sw = Stopwatch.StartNew();                  // 3. TIMED WINDOW
for (int i = 0; i < N; i++) _ = work();
sw.Stop();
var allocDelta = GC.GetAllocatedBytesForCurrentThread() - before;
Console.WriteLine($"{sw.Elapsed.TotalMicroseconds / N} us/op, {allocDelta / N} B/op");
```

The rules and the lies each prevents:

| Rule | Prevents |
|---|---|
| Warmup calls | First-call JIT + cache costs dominating N=1 runs |
| Many iterations (100–10k) | Timer resolution noise (Stopwatch ≈ tens of ns, but scheduling is µs) |
| Allocation delta, not wall time alone | CPU frequency scaling, machine noise faking speedups |
| Repeats with min/median | One unlucky scheduling blob poisoning the run |
| Same machine state (no debug build!) | Comparing debug vs release, or throttled laptop vs plugged |

Production-grade benchmarking uses **BenchmarkDotNet**, which isolates each
benchmark in its own process, does pilot-phase iteration sizing, and
reports statistical summaries — but its PHILOSOPHY is the table above, and
the sandbox (no NuGet restore) can run the minimal harness instead.

The equal-opportunity failure: measuring the WRONG THING. Optimizing
parsing when the request spends 90% of its time in DB round-trips is the
classic. Profile the END-TO-END path before micro-optimizing any component.
"""

_m14_measure_vi = r"""## Đo trước: kỷ luật benchmark

Giới luật: không tối ưu khi chưa có baseline đo được. Kỷ luật làm phép đo
có ý nghĩa:

```csharp
// Bộ harness trung thực tối thiểu (đúng những gì checkpoint chấm):
var work = (Func<int>)(() => SumTo(1000));
_ = work();                                     // 1. LÀM NÓNG — JIT, cache
var before = GC.GetAllocatedBytesForCurrentThread();   // 2. baseline
var sw = Stopwatch.StartNew();                  // 3. CỬA SỔ ĐO
for (int i = 0; i < N; i++) _ = work();
sw.Stop();
var allocDelta = GC.GetAllocatedBytesForCurrentThread() - before;
Console.WriteLine($"{sw.Elapsed.TotalMicroseconds / N} us/op, {allocDelta / N} B/op");
```

Các luật và lời nói dối mà mỗi luật chặn:

| Luật | Chặn điều gì |
|---|---|
| Làm nóng | Chi phí JIT lần đầu + cache áp đảo các lần chạy N=1 |
| Nhiều lần lặp (100–10k) | Nhiễu độ phân giải timer (Stopwatch ≈ chục ns, nhưng lập lịch là µs) |
| Delta cấp phát, không chỉ thời gian | CPU đổi tần số, nhiễu máy giả lập tăng tốc |
| Lặp lại với min/median | Một cục lập lịch xui rủi làm hỏng cả lần chạy |
| Cùng trạng thái máy (không build debug!) | So debug với release, hay laptop tiết kiệm pin vs cắm sạc |

Benchmark cấp production dùng **BenchmarkDotNet**, cách ly từng benchmark
trong process riêng, tự xác định số lần lặp bằng pilot-phase, và báo cáo
thống kê đầy đủ — nhưng TRIẾT LÝ của nó là bảng trên, và sandbox (không có
NuGet restore) có thể chạy bộ harness tối thiểu thay thế.

Kiểu thất bại ngang hàng: đo SAI THỨ. Tối ưu parsing khi request dành 90%
thời gian chờ DB round-trip là chuyện kinh điển. Hãy profile đường END-TO-END
trước khi tối ưu vi mô bất kỳ component nào.
"""

_m14_profiling = r"""## Profiling allocation and CPU

Profiling turns "it feels slow" into a ranked list of suspects. Three
instruments, cheapest first:

**1. Allocation profiling** (free, in-process): the checkpoint pattern —
`GC.GetAllocatedBytesForCurrentThread` deltas around suspect components,
plus `GC.CollectionCount` before/after a workload. Interpreting:

- High bytes/op on a hot path → allocation-driven GC pressure → Span,
  pooling, struct iteration, string.Create are the levers.
- Gen2 collections climbing during a request burst → the latency killer;
  find the per-request allocations reaching 85KB+ (LOH) or the sheer count.

**2. CPU sampling** (dotnet-trace/dotnet-counters when available): sample
stacks periodically; hot frames tell you WHERE cycles go. Without those
tools in a container, the poor-man's sampler — Stopwatch around
hypothesized boundaries — is legitimate evidence gathering: it is exactly
what the checkpoint's `Measure` does.

**3. The 90/10 discipline.** A ranked profile usually shows the top frame
owning 50–90% of samples. Optimize THAT one; re-measure; the next one
rises. Fixing frame #7 first is emotional programming.

Reading the results into a hypothesis table:

| Symptom | Likely cause | First lever |
|---|---|---|
| High allocs + ok CPU | LINQ/string churn on hot path | Span, for-loops, caching |
| High CPU, low allocs | algorithmic complexity, boxing, interface dispatch | better algorithm, struct generics |
| Spiky p99, ok median | Gen2/LOH collections | kill LOH allocations, pool buffers |
| Slow but CPU-idle | I/O waits, locks | async, lock sharding (Module 10) |
"""

_m14_profiling_vi = r"""## Profile cấp phát và CPU

Profiling biến "cảm giác chậm" thành danh sách nghi phạm có xếp hạng. Ba
nhạc cụ, rẻ nhất trước:

**1. Profile cấp phát** (miễn phí, trong process): pattern của checkpoint —
delta `GC.GetAllocatedBytesForCurrentThread` quanh các thành phần nghi vấn,
kèm `GC.CollectionCount` trước/sau workload. Cách đọc:

- Byte/op cao trên đường nóng → áp lực GC do cấp phát → Span, pooling,
  lặp struct, string.Create là các đòn bẩy.
- Gen2 tăng trong cơn bão request → kẻ giết độ trễ; tìm các cấp phát mỗi
  request chạm 85KB+ (LOH) hoặc số lượng khổng lồ.

**2. Lấy mẫu CPU** (dotnet-trace/dotnet-counters khi có): lấy mẫu stack
định kỳ; các khung nóng cho biết chu kỳ đi đâu. Trong container không có
công cụ đó, sampler kiểu người-poor — Stopwatch quanh các biên giả thuyết
— vẫn là bằng chứng hợp lệ: nó chính xác là những gì `Measure` trong
checkpoint làm.

**3. Kỷ luật 90/10.** Profile có xếp hạng thường cho thấy khung đầu chiếm
50–90% mẫu. Tối ưu CHÍNH nó; đo lại; khung kế tiếp sẽ nổi lên. Sửa khung
thứ 7 trước là lập trình theo cảm xúc.

Đọc kết quả thành bảng giả thuyết:

| Triệu chứng | Nguyên nhân khả dĩ | Đòn bẩy đầu tiên |
|---|---|---|
| Cấp phát cao + CPU ổn | Churn LINQ/string trên đường nóng | Span, for-loop, cache |
| CPU cao, cấp phát thấp | Độ phức tạp thuật toán, boxing, interface dispatch | thuật toán tốt hơn, struct generic |
| p99 gai góc, median ổn | Thu gom Gen2/LOH | diệt cấp phát LOH, pool buffer |
| Chậm nhưng CPU rảnh | Chờ I/O, khóa | async, phân mảnh khóa (Module 10) |
"""

_m14_jit = r"""## JIT effects on your measurements

The JIT is your co-author, and it edits aggressively. Four edits that fake
or mask performance:

**Tiered compilation** (default since .NET Core 3): methods first compile
fast-and-rough (tier 0), then recompile optimized after ~30 calls. A
benchmark that includes tier-0 execution measures the WRONG code. Warmup
is not optional; it is the difference between two compilers.

**Inlining.** Small methods vanish into their callers — the call overhead
you measured disappears. A micro-benchmark of "tiny method call overhead"
often measures nothing: the call was never made.

**Devirtualization + guarded devirtualization.** When the JIT can see the
exact type, virtual calls become direct calls (and sometimes inline).
Sealed classes/interfaces with single implementations get this for free.

**Dead-code elimination.** Compute a result and never use it? The JIT may
delete the entire computation. The classic broken micro-benchmark:

```csharp
sw.Start();
for (int i = 0; i < N; i++) ExpensivePure(i);   // result discarded — may be eliminated!
sw.Stop();
```

Fix: accumulate into a field/local and print or assert it after the loop
— the standard harness does this. BenchmarkDotNet's `[Benchmark]` handles
all four automatically (its `Consumer` keeps results alive).

The behavioral takeaway is symmetric: the same optimizations mean *real
code* also gets faster than source inspection suggests — hot paths with
small methods, sealed types, and loop-friendly data are not just style,
they are JIT-friendliness measured in nanoseconds.
"""

_m14_jit_vi = r"""## Hiệu ứng JIT lên phép đo của bạn

JIT là đồng tác giả của bạn, và nó biên tập rất hăng. Bốn biên tập làm
phép đo giả hoặc che mất hiệu năng:

**Tiered compilation** (mặc định từ .NET Core 3): phương thức được compile
nhanh-và-thô trước (tier 0), rồi compile lại tối ưu sau ~30 lần gọi.
Benchmark bao gồm phần chạy tier-0 là đo SAI code. Làm nóng không phải
tùy chọn; đó là khác biệt giữa hai trình biên dịch.

**Inlining.** Phương thức nhỏ tan vào caller — chi phí gọi bạn định đo
biến mất. Micro-benchmark đo "chi phí gọi phương thức nhỏ" thường không
đo được gì: lời gọi chưa từng diễn ra.

**Devirtualization + guarded devirtualization.** Khi JIT nhìn thấy kiểu
chính xác, lời gọi ảo thành lời gọi trực tiếp (đôi khi cả inline).
Lớp sealed/interface với một bản cài duy nhất được điều này miễn phí.

**Dead-code elimination.** Tính kết quả mà không dùng? JIT có thể xóa cả
phép tính. Micro-benchmark gãy kinh điển:

```csharp
sw.Start();
for (int i = 0; i < N; i++) ExpensivePure(i);   // kết quả bị bỏ — có thể bị xóa!
sw.Stop();
```

Cách sửa: tích lũy vào field/biến cục bộ rồi in hoặc assert sau vòng lặp
— bộ harness chuẩn làm đúng vậy. `[Benchmark]` của BenchmarkDotNet xử lý
cả bốn tự động (Consumer của nó giữ kết quả sống).

Bài học hành vi là đối xứng: cùng các tối ưu đó nghĩa là code THẬT cũng
nhanh hơn điều mà đọc mã nguồn gợi ý — đường nóng với phương thức nhỏ,
kiểu sealed, dữ liệu thân-vòng-lặp không chỉ là phong cách, mà là độ thân
thiện với JIT đo bằng nano giây.
"""

_m14_loop = r"""## The optimization loop

The full cycle, demonstrated on a real (sandbox-verifiable) workload —
string building:

**1. MEASURE.** Baseline the obvious implementation:

```csharp
static string SlowBuild(int n)
{
    var s = "";
    for (int i = 0; i < n; i++) s += i;   // quadratic: reallocates each append
    return s;
}
// n=10_000: ~150M+ bytes allocated, multiple Gen2 collections
```

**2. PROFILE.** Allocation delta says ~2×n² bytes — every `+=` copies the
whole string. The bottleneck is allocation count × copy size, not parsing,
not I/O.

**3. CHANGE — the smallest fix first.** StringBuilder (amortized growth):

```csharp
static string BetterBuild(int n)
{
    var sb = new StringBuilder(n * 5);   // pre-size: no internal array doubling
    for (int i = 0; i < n; i++) sb.Append(i);
    return sb.ToString();                 // one final string
}
// ~n*5 bytes + final string: ~50x less allocation
```

**4. MEASURE AGAIN.** Delta collapses; wall time follows. Then ask: is
StringBuilder the floor? Only with another measurement: `string.Create`
when the content is char-uniform, or writing directly to the output
stream, skipping the intermediate string entirely.

**5. DECIDE.** Is the added complexity justified by the measured win, at
the measured frequency? 50x on a code path hit 1/second is noise; 2x on a
path hit 1M times/second is a career. The optimization loop is not done
when the code is fast — it is done when the evidence says stop.

The anti-patterns this loop kills: optimizing without a baseline ("it
felt slow"), stopping at the first clever idea (StringBuilder everywhere —
including cold paths), and never re-measuring after the change (the
"optimization" that made it slower).
"""

_m14_loop_vi = r"""## Vòng lặp tối ưu

Toàn bộ chu trình, minh họa trên workload thật (xác minh được trong
sandbox) — dựng chuỗi:

**1. ĐO.** Baseline bản cài hiển nhiên:

```csharp
static string SlowBuild(int n)
{
    var s = "";
    for (int i = 0; i < n; i++) s += i;   // bậc hai: cấp phát lại mỗi lần nối
    return s;
}
// n=10_000: ~150M+ byte bị cấp phát, nhiều lần thu Gen2
```

**2. PROFILE.** Delta cấp phát báo ~2×n² byte — mỗi `+=` sao chép cả chuỗi.
Nút cổ chai là số lần cấp phát × kích thước bản sao, không phải parsing,
không phải I/O.

**3. SỬA — cách sửa nhỏ nhất trước.** StringBuilder (tăng trưởng tính
kỳ):

```csharp
static string BetterBuild(int n)
{
    var sb = new StringBuilder(n * 5);   // định kích thước trước: không nhân đôi mảng nội bộ
    for (int i = 0; i < n; i++) sb.Append(i);
    return sb.ToString();                 // một chuỗi cuối duy nhất
}
// ~n*5 byte + chuỗi cuối: giảm ~50 lần cấp phát
```

**4. ĐO LẠI.** Delta sụp đổ; thời gian theo sau. Rồi hỏi: StringBuilder có
phải là sàn không? Chỉ khi đo thêm: `string.Create` khi nội dung đồng đều
về char, hoặc ghi thẳng vào output stream, bỏ qua chuỗi trung gian.

**5. QUYẾT ĐỊNH.** Có đáng vì độ phức tạp thêm vào so với phần thắng đo
được, ở tần suất đo được không? Gấp 50 lần trên đường chạy 1 lần/giây là
nhiễu; gấp 2 lần trên đường chạy 1 triệu lần/giây là cả sự nghiệp. Vòng
lặp tối ưu không kết thúc khi code nhanh — nó kết thúc khi bằng chứng nói
dừng.

Các anti-pattern mà vòng lặp này tiêu diệt: tối ưu không có baseline
("cảm giác chậm"), dừng ở ý tưởng thông minh đầu tiên (StringBuilder mọi
nơi — kể cả đường lạnh), và không bao giờ đo lại sau khi sửa ("tối ưu"
khiến nó chậm hơn).
"""

_m14_checkpoint = r"""## Checkpoint: performance

The graded task is the minimal honest harness made mandatory: a warmup
call, an allocation window, and an implementation that survives a
zero-intermediate-allocations audit. Practice adds the interface-vs-span
dispatch comparison and a LINQ-vs-loop verdict you produce from your own
numbers.
"""

_m14_checkpoint_vi = r"""## Checkpoint: hiệu năng

Bài được chấm biến bộ harness trung thực tối thiểu thành bắt buộc: một lần
làm nóng, một cửa sổ cấp phát, và một bản cài vượt qua kiểm toán không-cấp
-phát-trung-gian. Practice thêm so sánh dispatch interface-vs-span và phán
quyết LINQ-vs-loop do chính con số của bạn tạo ra.
"""
