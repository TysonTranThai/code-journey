"""Module 13 — Garbage collection and memory management (csa-m13)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-gc",
        "Garbage Collection and Memory Management",
        "Generations, allocation behavior, finalization, weak references, leaks, and pooling — measured, not folk wisdom.",
    )

    csa.register_lesson(
        MID, "csa-m13-generations", "Generations and allocation",
        "Gen0/1/2, the LOH, allocation rates, and why cheap allocation is the design goal, not the enemy.",
        15, "advanced", _m13_generations, _m13_generations_vi,
    )
    csa.register_lesson(
        MID, "csa-m13-lifetime", "Lifetime: finalizers, disposal, weak refs",
        "The finalizer queue's costs, Dispose patterns, weak references, and event-handler leaks.",
        15, "advanced", _m13_lifetime, _m13_lifetime_vi,
    )
    csa.register_lesson(
        MID, "csa-m13-pooling", "Pooling: ArrayPool and friends",
        "When pooling pays, how ArrayPool buckets work, and the bugs renting/returning introduce.",
        15, "advanced", _m13_pooling, _m13_pooling_vi,
    )
    csa.register_lesson(
        MID, "csa-m13-leaks", "Managed memory leaks",
        "How a GC'd language still leaks: roots, events, caches, timers — and how to find each.",
        15, "advanced", _m13_leaks, _m13_leaks_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m13", "Checkpoint: GC and memory",
        "Synthesis: measure allocations, prove a weak-reference lifetime, and count collections.",
        12, "advanced", _m13_checkpoint, _m13_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m13-task", MID,
        title="GC checkpoint",
        prompt=(
            "Implement `static long MeasureAlloc<T>(Func<T> factory, int iterations)` returning GC.GetAllocatedBytesForCurrentThread() "
            "delta across `iterations` calls of factory — the standard micro-allocation probe. Then implement "
            "`static int Gen0Collections()` returning GC.CollectionCount(0), and `static WeakReference MakeWeak()` "
            "returning a WeakReference to a freshly allocated object(). The test: 1000 iterations of `new byte[64]` "
            "must allocate MORE than 1000*64 bytes; a weak reference's Target must become null after GC.Collect + "
            "WaitForPendingFinalizers + GC.Collect (the helper-method liveness pattern the lesson teaches)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "allocation-probe",
                "code": (
                    "var before = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 1000; i++) _ = new byte[64];\n"
                    "var delta = GC.GetAllocatedBytesForCurrentThread() - before;\n"
                    'Cj.True(delta >= 64_000, $"1000x64-byte arrays allocate at least 64000 bytes (got {delta})");'
                ),
                "hint": "GC.GetAllocatedBytesForCurrentThread() is precise for the current thread — capture before/after, no other allocations between.",
            },
            {
                "name": "weak-ref-death",
                "code": (
                    "var wr = Solution.MakeWeak();\n"
                    "GC.Collect(); GC.WaitForPendingFinalizers(); GC.Collect();\n"
                    'Cj.False(wr.IsAlive, "unreferenced object was collected");'
                ),
                "hint": "MakeWeak must return the WeakReference WITHOUT keeping a local alive: `var o = new object(); var wr = new WeakReference(o); return wr;` — the object must NOT be in a register when the caller collects (helper method + return is the pattern).",
            },
            {
                "name": "gc-counts-exposed",
                "code": (
                    "var c0 = Solution.Gen0Collections();\n"
                    "for (int i = 0; i < 2_000_000; i++) _ = new byte[64];\n"
                    'Cj.True(Solution.Gen0Collections() >= c0, "collection counts never decrease");'
                ),
                "hint": "return GC.CollectionCount(0) — monotonic by definition; the loop just forces pressure.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static long MeasureAlloc<T>(Func<T> factory, int iterations)\n"
            "    {\n"
            "        GC.Collect(); GC.WaitForPendingFinalizers(); GC.Collect();\n"
            "        var before = GC.GetAllocatedBytesForCurrentThread();\n"
            "        for (int i = 0; i < iterations; i++) _ = factory();\n"
            "        return GC.GetAllocatedBytesForCurrentThread() - before;\n"
            "    }\n\n"
            "    public static int Gen0Collections() => GC.CollectionCount(0);\n\n"
            "    public static WeakReference MakeWeak()\n"
            "    {\n"
            "        var o = new object();\n"
            "        var wr = new WeakReference(o);\n"
            "        _ = o;                 // keep the read but no longer needed\n"
            "        o = null;              // drop the strong ref explicitly\n"
            "        return wr;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static long MeasureAlloc<T>(Func<T> factory, int iterations)\n"
            "    {\n"
            "        var before = GC.GetAllocatedBytesForCurrentThread();\n"
            "        for (int i = 0; i < iterations; i++) _ = factory();\n"
            "        return GC.GetAllocatedBytesForCurrentThread() + before;   // WRONG: plus instead of minus\n"
            "    }\n\n"
            "    public static int Gen0Collections() => GC.CollectionCount(2);   // WRONG generation for the loop above\n\n"
            "    public static WeakReference MakeWeak()\n"
            "    {\n"
            "        var o = new object();\n"
            "        LeakRoot = o;            // WRONG: static field roots the object\n"
            "        var wr = new WeakReference(o);\n"
            "        return wr;\n"
            "    }\n"
            "    public static object? LeakRoot;\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p13-gc", "GC drills",
        "Allocation profiling, finalizer costs, event-leak diagnosis, and pooling decisions.",
        45, "advanced", "csa-m13-leaks",
        ["csa-p13-event-leak", "csa-p13-arraypool"],
    )
    csa.register_challenge(
        "csa-p13-event-leak", MID,
        title="Diagnose the event leak",
        prompt=(
            "Event subscriptions root their subscribers: a long-lived publisher keeping short-lived subscribers "
            "alive is .NET's classic leak. Implement `static int AliveAfterUnsubscribe()` that: creates a Publisher, "
            "creates 100 Subscriber objects each subscribing to Publisher.Tick, returns 100; then implement "
            "`static void UnsubscribeAll(Publisher p, List<Subscriber> subs)` calling Dispose on each (subscribers "
            "implement IDisposable and unsubscribe in Dispose). The test verifies that after Dispose + GC.Collect x2, "
            "a WeakReference to a subscriber is dead — proving unsubscribe breaks the root."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "unsubscribe-breaks-root",
                "code": (
                    "var p = new Publisher();\n"
                    "var wr = Build(p);\n"
                    "GC.Collect(); GC.WaitForPendingFinalizers(); GC.Collect();\n"
                    'Cj.False(wr.IsAlive, "disposed subscriber is collectible");'
                    "\n"
                    "static WeakReference Build(Publisher p)\n"
                    "{\n"
                    "    var inner = new List<Subscriber>();\n"
                    "    for (int i = 0; i < 10; i++) inner.Add(new Subscriber(p));\n"
                    "    var wr = new WeakReference(inner[0]);\n"
                    "    Solution.UnsubscribeAll(p, inner);\n"
                    "    inner.Clear();\n"
                    "    return wr;   // helper scope: no strong ref to the subscriber escapes\n"
                    "}"
                ),
                "hint": "Subscriber.Dispose must do p.Tick -= OnTick; the -= is what breaks the publisher→subscriber root.",
            },
        ],
        reference=(
            "public class Publisher\n{\n"
            "    public event EventHandler? Tick;\n"
            "    public void Fire() => Tick?.Invoke(this, EventArgs.Empty);\n"
            "}\n\n"
            "public class Subscriber : IDisposable\n{\n"
            "    private readonly Publisher _p;\n"
            "    public Subscriber(Publisher p) { _p = p; _p.Tick += OnTick; }\n"
            "    private void OnTick(object? s, EventArgs e) { }\n"
            "    public void Dispose() => _p.Tick -= OnTick;\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static int AliveAfterUnsubscribe()\n"
            "    {\n"
            "        var p = new Publisher();\n"
            "        int count = 0;\n"
            "        for (int i = 0; i < 100; i++) { var s = new Subscriber(p); count++; }\n"
            "        return count;\n"
            "    }\n\n"
            "    public static void UnsubscribeAll(Publisher p, List<Subscriber> subs)\n"
            "    {\n"
            "        foreach (var s in subs) s.Dispose();\n"
            "    }\n}"
        ),
        wrong=(
            "public class Publisher\n{\n"
            "    public event EventHandler? Tick;\n"
            "    public void Fire() => Tick?.Invoke(this, EventArgs.Empty);\n"
            "}\n\n"
            "public class Subscriber : IDisposable\n{\n"
            "    private readonly Publisher _p;\n"
            "    public Subscriber(Publisher p) { _p = p; _p.Tick += OnTick; }\n"
            "    private void OnTick(object? s, EventArgs e) { }\n"
            "    public void Dispose()\n"
            "    {\n"
            "        // WRONG: no unsubscribe — the publisher keeps every subscriber alive forever\n"
            "    }\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static int AliveAfterUnsubscribe()\n"
            "    {\n"
            "        var p = new Publisher();\n"
            "        int count = 0;\n"
            "        for (int i = 0; i < 100; i++) { var s = new Subscriber(p); count++; }\n"
            "        return count;\n"
            "    }\n\n"
            "    public static void UnsubscribeAll(Publisher p, List<Subscriber> subs)\n"
            "    {\n"
            "        foreach (var s in subs) s.Dispose();\n"
            "    }\n}"
        ),
        level="debugging",
    )
    csa.register_challenge(
        "csa-p13-arraypool", MID,
        title="ArrayPool discipline",
        prompt=(
            "Implement `static byte[] RentedSum(int[] values, out byte[] rented)` — NO. Simpler and testable: implement "
            "`static long PooledSum(int[] values)` that copies `values` through a rented ArrayPool<byte[]> buffer "
            "(rent a byte[] at least 4*values.Length, sum the first values.Length ints from it as 4-byte little-"
            "endian groups, return the sum, RETURN the array to the pool in a finally). Then implement `static long "
            "DirectSum(int[] values)` that just sums. Both must return identical results; the pooled one must not "
            "allocate a new array per call (the test calls it 100x and checks GC delta is tiny)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "sums-match",
                "code": (
                    "var vals = Enumerable.Range(0, 100).ToArray();\n"
                    'Cj.Eq(Solution.PooledSum(vals), Solution.DirectSum(vals), "identical results");'
                ),
                "hint": "Buffer.BlockCopy(vals, 0, rented, 0, vals.Length * 4); then sum ints at strides of 4 bytes via BitConverter or an int[] view.",
            },
            {
                "name": "pooled-no-alloc",
                "code": (
                    "var vals = new int[100];\n"
                    "Solution.PooledSum(vals);   // warm the pool\n"
                    "var before = GC.GetAllocatedBytesForCurrentThread();\n"
                    "for (int i = 0; i < 100; i++) Solution.PooledSum(vals);\n"
                    "var delta = GC.GetAllocatedBytesForCurrentThread() - before;\n"
                    'Cj.True(delta < 10_000, $"pooled path should not allocate arrays per call (got {delta} bytes)");'
                ),
                "hint": "ArrayPool<byte>.Shared.Rent/Return inside try/finally — rent the MINIMUM bucket, return without clearing unless the pool requires it.",
            },
        ],
        reference=(
            "using System.Runtime.InteropServices;\n\n"
            "public class Solution\n{\n"
            "    public static long PooledSum(int[] values)\n"
            "    {\n"
            "        if (values.Length == 0) return 0;\n"
            "        int byteLen = values.Length * sizeof(int);\n"
            "        byte[] rented = ArrayPool<byte>.Shared.Rent(byteLen);\n"
            "        try\n"
            "        {\n"
            "            Buffer.BlockCopy(values, 0, rented, 0, byteLen);\n"
            "            var ints = MemoryMarshal.Cast<byte, int>(rented.AsSpan(0, byteLen));\n"
            "            long sum = 0;\n"
            "            foreach (var v in ints) sum += v;\n"
            "            return sum;\n"
            "        }\n"
            "        finally\n"
            "        {\n"
            "            ArrayPool<byte>.Shared.Return(rented);\n"
            "        }\n"
            "    }\n\n"
            "    public static long DirectSum(int[] values)\n"
            "    {\n"
            "        long s = 0;\n"
            "        foreach (var v in values) s += v;\n"
            "        return s;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static long PooledSum(int[] values)\n"
            "    {\n"
            "        if (values.Length == 0) return 0;\n"
            "        byte[] rented = ArrayPool<byte>.Shared.Rent(values.Length * sizeof(int));\n"
            "        // WRONG: no try/finally, no Return — the rented buffer is lost every call\n"
            "        Buffer.BlockCopy(values, 0, rented, 0, values.Length * sizeof(int));\n"
            "        var ints = new int[values.Length];\n"
            "        Buffer.BlockCopy(rented, 0, ints, 0, values.Length * sizeof(int));\n"
            "        long sum = 0;\n"
            "        foreach (var v in ints) sum += v;\n"
            "        return sum;\n"
            "    }\n\n"
            "    public static long DirectSum(int[] values)\n"
            "    {\n"
            "        long s = 0;\n"
            "        foreach (var v in values) s += v;\n"
            "        return s;\n"
            "    }\n}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m13_generations = r"""## Generations and allocation

.NET's GC is generational and tracing-based. New objects land in **Gen 0**;
survivors are promoted to **Gen 1**, then **Gen 2**. Large objects (≥85,000
bytes on CoreCLR — an implementation detail, but a stable one) go
straight to the **Large Object Heap (LOH)**. The bet: most objects die
young, so scanning a small Gen0 window collects most garbage cheaply.

```csharp
GC.CollectionCount(0 | 1 | 2);      // collections per generation
GC.GetAllocatedBytesForCurrentThread();  // precise per-thread allocation probe
GC.GetTotalMemory(false);           // current managed heap estimate
GC.Collect(2, GCCollectionMode.Aggressive);  // force (measurement only!)
```

The economics that change how you write code:

- **Allocation is cheap.** Gen0 allocation bumps a pointer — tens of
  nanoseconds. The .NET design philosophy is "allocate freely, collect
  often"; fighting every allocation with pooling everywhere is usually a
  loss.
- **Survival is expensive.** An object that survives Gen0 gets copied,
  promoted, and re-scanned every future collection. Long-lived cache
  objects are fine; long-lived objects that CHANGE generation boundaries
  under churn are the cost.
- **Gen2/LOH collections stop the world longest.** Allocation-rate spikes
  that trigger Gen2 collections are the classic latency bug: steady
  99th-percentile, then a 200ms stall every 30s. The fix is allocation
  reduction on the hot path (Span, pooling, struct iteration), not GC
  tuning first.

Measurement discipline: capture `GC.CollectionCount` per generation and
allocation bytes around a workload — the delta IS your GC story. The
checkpoint's probe methods are exactly this pattern.
"""

_m13_generations_vi = r"""## Các thế hệ và cấp phát

GC của .NET là GC thế hệ và truy vết. Object mới rơi vào **Gen 0**; kẻ
sống sót được thăng **Gen 1**, rồi **Gen 2**. Object lớn (≥85,000 byte trên
CoreCLR — chi tiết cài đặt, nhưng ổn định) đi thẳng vào **Large Object Heap
(LOH)**. Cược phẩm: phần lớn object chết trẻ, nên quét cửa sổ Gen0 nhỏ thu
hầu hết rác một cách rẻ.

```csharp
GC.CollectionCount(0 | 1 | 2);      // số lần thu mỗi thế hệ
GC.GetAllocatedBytesForCurrentThread();  // thăm dò cấp phát chính xác theo thread
GC.GetTotalMemory(false);           // ước lượng heap managed hiện tại
GC.Collect(2, GCCollectionMode.Aggressive);  // ép (chỉ để đo!)
```

Kinh tế học thay đổi cách bạn viết code:

- **Cấp phát rẻ.** Cấp phát Gen0 chỉ tăng con trỏ — vài chục nano giây.
  Triết lý thiết kế của .NET là "cấp phát thoải mái, thu thường xuyên";
  chống mọi cấp phát bằng pooling khắp nơi thường là lỗ.
- **Sống sót đắt.** Object sống qua Gen0 bị sao chép, thăng cấp, và quét
  lại ở mọi lần thu sau. Object cache sống lâu thì ổn; object sống lâu mà
  CHẠY QUA ranh giới thế hệ dưới churn mới là cái giá.
- **Thu Gen2/LOH dừng thế giới lâu nhất.** Bùng nổ tốc độ cấp phát gây các
  lần thu Gen2 là bug độ trễ kinh điển: percentile 99 ổn định, rồi một cú
  khựng 200ms mỗi 30s. Cách sửa là giảm cấp phát trên đường nóng (Span,
  pooling, lặp struct), không phải tinh chỉnh GC trước.

Kỷ luật đo đếm: chụp `GC.CollectionCount` từng thế hệ và số byte cấp phát
quanh một workload — delta CHÍNH LÀ câu chuyện GC của bạn. Các phương pháp
probe trong checkpoint đúng là pattern này.
"""

_m13_lifetime = r"""## Lifetime: finalizers, disposal, weak refs

**Finalizers are a toll booth.** An object with `~Finalizer()` is not
collected at first reachability — it is registered with the finalizer
queue, promoted at least one generation, its finalizer runs later on a
dedicated thread, and only THEN is it collectible. Every finalizable
object costs an extra GC cycle and pins a queue slot. Rule: you almost
never write a finalizer — you write `IDisposable`, and add a finalizer
only when you own a raw OS handle, and even then via `SafeHandle` which
already finalizes for you.

```csharp
public class NativeThing : IDisposable
{
    private readonly SafeFileHandle _handle;      // SafeHandle IS the finalizer
    public void Dispose() { _handle.Dispose(); GC.SuppressFinalize(this); }
}
```

**Dispose discipline**: `using` (or `await using`) everywhere, try/finally
when the sugar does not fit, `GC.SuppressFinalize` after explicit disposal.
**Finalize-Dispose pattern** is for handle owners; app code should ride
`SafeHandle`.

**WeakReference** observes an object without keeping it alive:

```csharp
var wr = new WeakReference(obj);
wr.IsAlive; wr.Target;              // Target may be null at any moment
```

The canonical use is caches/lookaside tables (`ConditionalWeakTable<K,V>`
attaches state to an object keyed by its lifetime). The liveness gotcha
this course probes: a local variable's object may stay reachable through a
JIT register until the method's last use — the "GC.Collect proves death"
demo must run the allocation in a separate helper method, exactly what the
checkpoint does.

**Event leaks** are lifetime's most common production bug — the practice
task walks it.
"""

_m13_lifetime_vi = r"""## Vòng đời: finalizer, disposal, weak ref

**Finalizer là trạm thu phí.** Object có `~Finalizer()` không được thu ngay
tại lần đầu mất khả năng tiếp cận — nó được đăng ký vào finalizer queue,
thăng cấp ít nhất một thế hệ, finalizer chạy sau trên thread riêng, và CHỈ
RỒI mới có thể thu. Mỗi object finalizable tốn thêm một chu kỳ GC và giữ
một slot queue. Quy tắc: bạn hầu như không bao giờ tự viết finalizer — bạn
viết `IDisposable`, chỉ thêm finalizer khi sở hữu handle thô của OS, và
ngay cả khi vậy cũng qua `SafeHandle` vốn finalizer hộ bạn rồi.

```csharp
public class NativeThing : IDisposable
{
    private readonly SafeFileHandle _handle;      // SafeHandle CHÍNH LÀ finalizer
    public void Dispose() { _handle.Dispose(); GC.SuppressFinalize(this); }
}
```

**Kỷ luật Dispose**: `using` (hoặc `await using`) khắp nơi, try/finally khi
đường ngọt không vừa, `GC.SuppressFinalize` sau khi dispose tường minh.
**Pattern Finalize-Dispose** dành cho chủ handle; code ứng dụng nên đi
xe `SafeHandle`.

**WeakReference** quan sát một object mà không giữ nó sống:

```csharp
var wr = new WeakReference(obj);
wr.IsAlive; wr.Target;              // Target có thể null tại mọi thời điểm
```

Công dụng kinh điển là cache/bảng tra sidebar (`ConditionalWeakTable<K,V>`
gắn trạng thái vào object theo đúng vòng đời của nó). Cạm bẫy liveness mà
khóa học probe: object của biến cục bộ có thể vẫn tiếp cận được qua thanh
ghi JIT cho đến lần dùng cuối của phương thức — demo "GC.Collect chứng
minh cái chết" phải chạy phần cấp phát trong một phương thức helper riêng,
đúng như checkpoint làm.

**Rò rỉ event** là bug production phổ biến nhất của vòng đời — task practice
sẽ đi từng bước.
"""

_m13_pooling = r"""## Pooling: ArrayPool and friends

`ArrayPool<T>.Shared` rents byte/T arrays from size-classed buckets
(powers of two; you may get a LARGER array than requested — always use
your logical length, never `rented.Length`). Rent/Return are cheap
interlocked ops; the win shows on hot paths allocating big buffers per
request.

```csharp
byte[] buf = ArrayPool<byte>.Shared.Rent(minLength: 4096);
try { Use(buf.AsSpan(0, logical)); }
finally { ArrayPool<byte>.Shared.Return(buf); }   // clearArray: true only for secrets
```

The four bugs pooling introduces (why it is opt-in, not default):

1. **Forgetting Return** — the buffer leaks from the pool (not the GC);
   the pool grows, memory balloons.
2. **Use-after-return** — a Span held past Return reads another renter's
   data. Correctness bug, possibly a security bug (cross-request data
   bleed).
3. **Wrong length assumptions** — rented.Length ≥ your need; slicing is
   mandatory.
4. **Returning dirty buffers with secrets** — `clearArray: true` when the
   content was sensitive.

When pooling PAYS: large (≥KBs) buffers on request-rate hot paths.
When it does not: small short-lived allocations (Gen0 is cheaper than
the API ceremony), anything rent/return dominated by work smaller than
the allocation itself. Measure with `GC.GetAllocatedBytesForCurrentThread`
before and after — the checkpoint's second test enforces this.

`ObjectPool<T>` (Microsoft.Extensions.ObjectPool) does the same for
polymorphic objects — same rules apply: rent, use, return, no leaks past
return.
"""

_m13_pooling_vi = r"""## Pooling: ArrayPool và bạn bè

`ArrayPool<T>.Shared` cho thuê mảng byte/T theo các bucket phân lớp kích
thước (lũy thừa hai; bạn có thể nhận mảng LỚN HƠN yêu cầu — luôn dùng độ
dài logic của bạn, không phải `rented.Length`). Rent/Return là các phép
interlocked rẻ; phần thắng hiện ra trên đường nóng cấp phát buffer lớn mỗi
request.

```csharp
byte[] buf = ArrayPool<byte>.Shared.Rent(minLength: 4096);
try { Use(buf.AsSpan(0, logical)); }
finally { ArrayPool<byte>.Shared.Return(buf); }   // clearArray: true chỉ cho dữ liệu nhạy cảm
```

Bốn bug mà pooling giới thiệu (vì sao nó là opt-in, không phải mặc định):

1. **Quên Return** — buffer rò rỉ khỏi pool (không phải khỏi GC); pool
   phình to, bộ nhớ bay màu.
2. **Dùng sau khi return** — một Span giữ quá thời điểm Return đọc dữ liệu
   của bên thuê khác. Bug tính đúng đắn, có thể là bug bảo mật (rò dữ liệu
   chéo request).
3. **Giả định độ dài sai** — rented.Length ≥ nhu cầu của bạn; slicing là
   bắt buộc.
4. **Trả buffer bẩn chứa mật mã** — `clearArray: true` khi nội dung nhạy
   cảm.

Khi nào pooling CÓ LỢI: buffer lớn (≥ vài KB) trên đường nóng tần suất
request cao. Khi nào không: cấp phát nhỏ, sống ngắn (Gen0 rẻ hơn cả các
nghi thức API), bất cứ đâu công việc nhỏ hơn chính phép cấp phát. Đo bằng
`GC.GetAllocatedBytesForCurrentThread` trước và sau — test thứ hai của
checkpoint ép điều này.

`ObjectPool<T>` (Microsoft.Extensions.ObjectPool) làm điều tương tự cho
object đa hình — cùng các quy tắc: thuê, dùng, trả, không rò rỉ sau khi
trả.
"""

_m13_leaks = r"""## Managed memory leaks

A tracing GC frees what is unreachable. "Leak" in managed code therefore
means **unreachable-when-you-thought**: something reachable holds a root
to something you considered dead. The catalog:

1. **Event subscriptions.** `publisher.Event += handler` stores the
   subscriber in the publisher's invocation list. Long-lived publisher +
   short-lived subscriber = every subscriber leaks. Fix: IDisposable
   unsubscribe, weak-event patterns, or `IObserver` with explicit
   disposal.
2. **Static caches without eviction.** `static Dictionary<string, T>`
   grows forever; every entry is rooted by the type. Fix: `MemoryCache`
   with size/time limits, `ConditionalWeakTable` for metadata, or
   bounded LRU.
3. **Timers.** A live `System.Threading.Timer` roots its callback target.
   Fire-and-forget timers in components that forget to dispose them keep
   whole object graphs alive. (The callback's TARGET, and everything it
   references.)
4. **Closures and lambdas.** A lambda capturing `this` registered into a
   long-lived service roots the whole object. Task runners holding
   closures beyond their useful life do the same.
5. **Thread-statics and captured contexts** (SynchronizationContext,
   ExecutionContext held by parked threads).

Diagnosis workflow without fancy tooling (the sandbox has no dotnet-dump):
count instances over time (a loop that allocates a probe object each
iteration and a WeakReference you can poll), force collections, and watch
`GC.GetTotalMemory` climb — climbing memory across forced full collections
is the leak signature. The checkpoint's weak-reference test IS this probe,
miniaturized.
"""

_m13_leaks_vi = r"""## Rò rỉ bộ nhớ trong thế giới managed

Tracing GC giải phóng thứ không thể tiếp cận. Vậy "rò rỉ" trong managed
code nghĩa là **vẫn tiếp cận được trong khi bạn tưởng đã chết**: một thứ
gì đó tiếp cận được đang giữ root tới thứ bạn coi đã chết. Danh mục:

1. **Đăng ký event.** `publisher.Event += handler` lưu subscriber vào
   invocation list của publisher. Publisher sống lâu + subscriber sống
   ngắn = mọi subscriber đều rò rỉ. Cách sửa: hủy đăng ký qua IDisposable,
   weak-event pattern, hoặc `IObserver` với disposal tường minh.
2. **Cache tĩnh không dọn dẹp.** `static Dictionary<string, T>` phình mãi;
   mọi entry bị root bởi kiểu. Cách sửa: `MemoryCache` với giới hạn
   kích thước/thời gian, `ConditionalWeakTable` cho metadata, hoặc LRU
   giới hạn.
3. **Timer.** Một `System.Threading.Timer` còn sống sẽ root callback target
   của nó. Timer fire-and-forget trong các component quên dispose sẽ giữ
   cả cây object sống mãi. (TARGET của callback, và mọi thứ nó tham chiếu.)
4. **Closure và lambda.** Một lambda bắt `this` rồi đăng ký vào service
   sống lâu sẽ root cả object. Task runner giữ closure vượt quá tuổi thọ
   hữu ích cũng vậy.
5. **Thread-static và context bị giữ** (SynchronizationContext,
   ExecutionContext của các thread đang đỗ).

Quy trình chẩn đoán không cần công cụ sang (sandbox không có dotnet-dump):
đếm số instance theo thời gian (một vòng lặp cấp phát probe object mỗi
lần lặp và một WeakReference có thể poll), ép thu gom, và xem
`GC.GetTotalMemory` leo dốc — bộ nhớ leo dù đã ép thu gom toàn phần là
chữ ký của rò rỉ. Test weak-reference trong checkpoint CHÍNH LÀ probe này,
thu nhỏ lại.
"""

_m13_checkpoint = r"""## Checkpoint: GC and memory

The graded task instruments allocation precisely (thread-local bytes), exposes
collection counters, and proves object death through the helper-method weak-
reference pattern. Practice walks the event-leak root chain and the ArrayPool
rent/return discipline with a no-allocation assertion.
"""

_m13_checkpoint_vi = r"""## Checkpoint: GC và bộ nhớ

Bài được chấm đo cấp phát chính xác (byte theo thread), lộ các bộ đếm thu
gom, và chứng minh cái chết của object qua pattern weak-reference với
phương thức helper. Practice đi qua chuỗi root của rò rỉ event và kỷ luật
rent/return ArrayPool với khẳng định không cấp phát.
"""
