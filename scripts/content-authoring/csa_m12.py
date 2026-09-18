"""Module 12 — Channels and producer/consumer systems (csa-m12)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-channels",
        "Channels and Producer/Consumer Systems",
        "System.Threading.Channels: bounded buffering, backpressure, completion, and graceful shutdown pipelines.",
    )

    csa.register_lesson(
        MID, "csa-m12-channel-model", "The Channel<T> model",
        "Reader/Writer halves, bounded vs unbounded, full-mode behavior — the vocabulary of backpressure.",
        15, "advanced", _m12_model, _m12_model_vi,
    )
    csa.register_lesson(
        MID, "csa-m12-backpressure", "Backpressure as a design tool",
        "Why bounded channels are the default: load shedding, latency floors, and unbounded queues eating memory.",
        15, "advanced", _m12_backpressure, _m12_backpressure_vi,
    )
    csa.register_lesson(
        MID, "csa-m12-completion", "Completion and graceful shutdown",
        "TryComplete, ReadAllAsync termination, draining strategies, and shutdown ordering across pipeline stages.",
        15, "advanced", _m12_completion, _m12_completion_vi,
    )
    csa.register_lesson(
        MID, "csa-m12-pipelines", "Multi-stage pipeline architecture",
        "Stage-per-channel composition, fan-out/fan-in, and where Channels beat Task collections.",
        15, "advanced", _m12_pipelines, _m12_pipelines_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m12", "Checkpoint: channels",
        "Synthesis: build a bounded producer/consumer with drain-on-shutdown semantics.",
        12, "advanced", _m12_checkpoint, _m12_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m12-task", MID,
        title="Channels checkpoint",
        prompt=(
            "Implement `static async Task<int> PumpAsync(ChannelReader<int> source, ChannelWriter<int> sink, int factor, "
            "CancellationToken ct)` reading every item from source, writing item*factor to sink, and completing the "
            "sink when done — propagating cancellation. Then implement `static async Task<List<int>> RunBounded(int count)`: "
            "create a bounded channel (capacity 8), a producer writing 0..count-1 then completing, and a single consumer "
            "collecting via ReadAllAsync. The test verifies end-to-end flow and that the consumer's output is complete."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "pump",
                "code": (
                    "var c = Channel.CreateBounded<int>(4);\n"
                    "var prod = Task.Run(async () => { foreach (var n in new[] { 1, 2, 3 }) await c.Writer.WriteAsync(n); c.Writer.Complete(); });\n"
                    "var outC = Channel.CreateUnbounded<int>();\n"
                    "await Solution.PumpAsync(c.Reader, outC.Writer, 10, CancellationToken.None);\n"
                    "var got = new List<int>();\n"
                    "await foreach (var n in outC.Reader.ReadAllAsync()) got.Add(n);\n"
                    'Cj.Eq(string.Join(",", got), "10,20,30", "pumped and multiplied, sink completed");'
                ),
                "hint": "await foreach (var item in source.ReadAllAsync(ct)) await sink.WriteAsync(item * factor, ct); finally sink.Complete().",
            },
            {
                "name": "bounded-drain",
                "code": (
                    "var r = await Solution.RunBounded(100);\n"
                    'Cj.Eq(r.Count, 100, "all 100 items drained");\n'
                    'Cj.Eq(r[0], 0, "bounded channel keeps order"); Cj.Eq(r[99], 99, "in order");'
                ),
                "hint": "Bounded(capacity: 8); producer: for-loop WriteAsync then TryComplete; consumer: await foreach ReadAllAsync into list.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async Task<int> PumpAsync(ChannelReader<int> source, ChannelWriter<int> sink, int factor, CancellationToken ct)\n"
            "    {\n"
            "        try\n"
            "        {\n"
            "            await foreach (var item in source.ReadAllAsync(ct).ConfigureAwait(false))\n"
            "                await sink.WriteAsync(item * factor, ct).ConfigureAwait(false);\n"
            "            sink.TryComplete();\n"
            "            return 0;\n"
            "        }\n"
            "        catch (OperationCanceledException)\n"
            "        {\n"
            "            sink.TryComplete();\n"
            "            throw;\n"
            "        }\n"
            "    }\n\n"
            "    public static async Task<List<int>> RunBounded(int count)\n"
            "    {\n"
            "        var ch = Channel.CreateBounded<int>(8);\n"
            "        var prod = Task.Run(async () =>\n"
            "        {\n"
            "            for (int i = 0; i < count; i++) await ch.Writer.WriteAsync(i);\n"
            "            ch.Writer.TryComplete();\n"
            "        });\n"
            "        var result = new List<int>();\n"
            "        await foreach (var n in ch.Reader.ReadAllAsync()) result.Add(n);\n"
            "        await prod;\n"
            "        return result;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async Task<int> PumpAsync(ChannelReader<int> source, ChannelWriter<int> sink, int factor, CancellationToken ct)\n"
            "    {\n"
            "        await foreach (var item in source.ReadAllAsync())\n"
            "            await sink.WriteAsync(item + factor);   // WRONG operator, no ct, no completion\n"
            "        return 0;                                    // WRONG: sink never completed\n"
            "    }\n\n"
            "    public static async Task<List<int>> RunBounded(int count)\n"
            "    {\n"
            "        var ch = Channel.CreateBounded<int>(8);\n"
            "        var prod = Task.Run(async () =>\n"
            "        {\n"
            "            for (int i = 0; i < count; i++) await ch.Writer.WriteAsync(i);\n"
            "            ch.Writer.TryComplete();\n"
            "        });\n"
            "        var result = new List<int>();\n"
            "        await foreach (var n in ch.Reader.ReadAllAsync()) result.Add(n);\n"
            "        await prod;\n"
            "        return result;\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p12-ch", "Channel drills",
        "Bounded backpressure, shutdown draining, fan-out workers, and completion semantics.",
        45, "advanced", "csa-m12-pipelines",
        ["csa-p12-fanout", "csa-p12-drain"],
    )
    csa.register_challenge(
        "csa-p12-fanout", MID,
        title="Fan-out workers",
        prompt=(
            "Implement `static async Task<int[]> FanOut(int itemCount, int workers)` where itemCount jobs (value = "
            "index) flow through a channel and `workers` concurrent consumer tasks each pull items and compute "
            "index * 2, writing results into a shared thread-safe list. All items must be processed exactly once "
            "(competing consumers on one channel), and the method returns the sorted results. The test runs workers=4 "
            "over 1000 items and asserts completeness and uniqueness."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "exactly-once",
                "code": (
                    "var r = await Solution.FanOut(1000, 4);\n"
                    'Cj.Eq(r.Length, 1000, "every item processed");\n'
                    'Cj.Eq(r.Distinct().Count(), 1000, "no item processed twice");\n'
                    'Cj.Eq(r[500], 1000, "value = index * 2");'
                ),
                "hint": "One channel, N consumers each doing `await foreach (var i in reader.ReadAllAsync())` — the channel guarantees each item goes to exactly one reader.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async Task<int[]> FanOut(int itemCount, int workers)\n"
            "    {\n"
            "        var ch = Channel.CreateUnbounded<int>();\n"
            "        var results = new ConcurrentBag<int>();\n"
            "        var consumers = Enumerable.Range(0, workers).Select(_ => Task.Run(async () =>\n"
            "        {\n"
            "            await foreach (var i in ch.Reader.ReadAllAsync())\n"
            "                results.Add(i * 2);\n"
            "        })).ToArray();\n"
            "        for (int i = 0; i < itemCount; i++) await ch.Writer.WriteAsync(i);\n"
            "        ch.Writer.TryComplete();\n"
            "        await Task.WhenAll(consumers);\n"
            "        return results.OrderBy(x => x).ToArray();\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async Task<int[]> FanOut(int itemCount, int workers)\n"
            "    {\n"
            "        var results = new ConcurrentBag<int>();\n"
            "        var consumers = Enumerable.Range(0, workers).Select(_ => Task.Run(async () =>\n"
            "        {\n"
            "            for (int i = 0; i < itemCount; i++)   // WRONG: every worker processes every item\n"
            "                results.Add(i * 2);\n"
            "        })).ToArray();\n"
            "        await Task.WhenAll(consumers);\n"
            "        return results.OrderBy(x => x).ToArray();\n"
            "    }\n}"
        ),
        level="real-world",
    )
    csa.register_challenge(
        "csa-p12-drain", MID,
        title="Graceful shutdown drain",
        prompt=(
            "A worker must stop ACCEPTING new work immediately on shutdown, but finish what it already accepted. "
            "Implement `static async Task<List<int>> ShutdownDrain(int feedCount, int shutdownAfter)`: a producer "
            "writes integers 0..feedCount-1; after `shutdownAfter` items have been WRITTEN, the producer calls "
            "TryComplete (no more accepts) — but every item written before completion must still be consumed by a "
            "background reader collecting them via ReadAllAsync. Return the collected list. The test asserts "
            "shutdownAfter items arrive, nothing more."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "drain-exact",
                "code": (
                    "var r = await Solution.ShutdownDrain(100, 30);\n"
                    'Cj.Eq(r.Count, 30, "exactly the accepted items processed");\n'
                    'Cj.Eq(r.Min(), 0, "every item present"); Cj.Eq(r.Max(), 29, "the first 30, in order");'
                ),
                "hint": "In the producer loop: if (i == shutdownAfter) writer.TryComplete(); then WriteAsync(i) — but TryComplete BEFORE the writes you want accepted... order: write i, then when i == shutdownAfter-1, TryComplete after the write. Items already buffered are still delivered to ReadAllAsync after completion.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async Task<List<int>> ShutdownDrain(int feedCount, int shutdownAfter)\n"
            "    {\n"
            "        var ch = Channel.CreateUnbounded<int>();\n"
            "        var collected = new List<int>();\n"
            "        var reader = Task.Run(async () =>\n"
            "        {\n"
            "            await foreach (var n in ch.Reader.ReadAllAsync())\n"
            "                lock (collected) collected.Add(n);\n"
            "        });\n"
            "        for (int i = 0; i < feedCount && i < shutdownAfter; i++)\n"
            "            await ch.Writer.WriteAsync(i);\n"
            "        ch.Writer.TryComplete();   // stop accepting; buffered items still delivered\n"
            "        await reader;\n"
            "        lock (collected) return collected.OrderBy(x => x).ToList();\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async Task<List<int>> ShutdownDrain(int feedCount, int shutdownAfter)\n"
            "    {\n"
            "        var ch = Channel.CreateUnbounded<int>();\n"
            "        var collected = new List<int>();\n"
            "        var reader = Task.Run(async () =>\n"
            "        {\n"
            "            await foreach (var n in ch.Reader.ReadAllAsync())\n"
            "                lock (collected) collected.Add(n);\n"
            "        });\n"
            "        for (int i = 0; i < feedCount; i++)\n"
            "        {\n"
            "            if (i >= shutdownAfter) ch.Writer.TryComplete();   // WRONG: completes but keeps writing\n"
            "            await ch.Writer.WriteAsync(i);                      // WRONG: writes after completion throw\n"
            "        }\n"
            "        await reader;\n"
            "        lock (collected) return collected.OrderBy(x => x).ToList();\n"
            "    }\n}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m12_model = r"""## The `Channel<T>` model

`Channel<T>` splits into two halves with deliberately different
capabilities: `ChannelWriter<T>` can write and complete; `ChannelReader<T>`
can read, count, and observe completion. The split is the design: consumers
cannot sneak writes, producers cannot complete the channel out from under
a reader's contract.

```csharp
var ch = Channel.CreateBounded<int>(capacity: 100);
// or Channel.CreateUnbounded<int>();

await ch.Writer.WriteAsync(item, ct);        // async write; WAITS when full
if (ch.Reader.TryRead(out var v)) { }        // sync poll
await ch.Reader.ReadAsync(ct);               // async read; WAITS when empty
await foreach (var v in ch.Reader.ReadAllAsync(ct)) { }   // drain to completion
```

Two options shape everything else:

- **Bounded vs unbounded.** An unbounded channel accepts every write
  instantly — memory grows without limit under producer>consumer load. A
  bounded channel makes `WriteAsync` WAIT when full. That wait is
  backpressure, and it is a feature, not a bug.
- **Full modes** (`BoundedChannelFullMode`): `Wait` (default — writers
  wait), `DropOldest`/`DropNewest` (ring-buffer semantics, lose data but
  never stall), `DropWrite`. Telemetry pipelines love DropOldest; order
  processing must never use it.

`SingleReader`/`SingleWriter` options let the implementation skip
synchronization — a measurable speedup for the single-pump case.

Channels exist because `Queue<T>` + `lock` + `SemaphoreSlim` hand-rolled
poorly: no async waiting, no completion, no backpressure. `Task` collections
have no flow control at all. Channel is the standard library's answer to
"go-like pipelines in C#".
"""

_m12_model_vi = r"""## Mô hình `Channel<T>`

`Channel<T>` tách thành hai nửa với năng lực khác nhau một cách cố ý:
`ChannelWriter<T>` có thể ghi và complete; `ChannelReader<T>` có thể đọc,
đếm, và quan sát completion. Sự tách là thiết kế: consumer không thể lén
ghi, producer không thể complete phá hợp đồng của reader.

```csharp
var ch = Channel.CreateBounded<int>(capacity: 100);
// hoặc Channel.CreateUnbounded<int>();

await ch.Writer.WriteAsync(item, ct);        // ghi bất đồng bộ; CHỜ khi đầy
if (ch.Reader.TryRead(out var v)) { }        // poll đồng bộ
await ch.Reader.ReadAsync(ct);               // đọc bất đồng bộ; CHỜ khi rỗng
await foreach (var v in ch.Reader.ReadAllAsync(ct)) { }   // rút cạn tới khi hoàn thành
```

Hai tùy chọn định hình mọi thứ còn lại:

- **Bounded vs unbounded.** Unbounded nhận mọi write ngay lập tức — bộ nhớ
  tăng không giới hạn khi producer nhanh hơn consumer. Bounded làm `WriteAsync`
  CHỜ khi đầy. Sự chờ đó là backpressure, và nó là tính năng, không phải lỗi.
- **Full modes** (`BoundedChannelFullMode`): `Wait` (mặc định — writer chờ),
  `DropOldest`/`DropNewest` (ngữ nghĩa ring-buffer, mất dữ liệu nhưng không
  bao giờ ùn tắc), `DropWrite`. Pipeline telemetry mê DropOldest; xử lý đơn
  hàng tuyệt đối không dùng nó.

Các tùy chọn `SingleReader`/`SingleWriter` cho phép implementation bỏ qua
đồng bộ hóa — tăng tốc đo đếm được cho trường hợp một-pump.

Channels tồn tại vì `Queue<T>` + `lock` + `SemaphoreSlim` tự viết thì kém:
không chờ bất đồng bộ, không completion, không backpressure. Bộ sưu tập
`Task` không có kiểm soát luồng gì cả. Channel là câu trả lời chuẩn của thư
viện chuẩn cho "pipeline kiểu go trong C#".
"""

_m12_backpressure = r"""## Backpressure as a design tool

Unbounded queues are the silent killer of services under load. The
sequence is always the same: producer outpaces consumer → queue grows →
memory grows → GC pressure rises → latency rises → timeouts → retries →
MORE load. The queue did not cause the failure; the *absence of
backpressure* did.

A bounded channel turns overload into an explicit, survivable signal:

```csharp
var ch = Channel.CreateBounded<Job>(new BoundedChannelOptions(1_000)
{
    FullMode = BoundedChannelFullMode.Wait,   // writers feel the load
    SingleReader = false,
});

// Producer:
try { await ch.Writer.WriteAsync(job, ct); }
catch (ChannelClosedException) { /* shutting down: shed */ }
```

With `Wait`, the producer's latency rises as the queue fills — the system
degrades toward the consumer's true throughput instead of dying. The
callers upstream (HTTP handlers, message pumps) experience the pressure
and can shed, return 503, or slow down — the correct system behavior.

Design decisions bounded channels force you to make (all good questions):

1. **Capacity** = maximum tolerated burst. 0 = pure rendezvous; small =
   latency-sensitive; large = burst-absorbing (and memory-hungry).
2. **Drop or wait?** Dropping is correct for metrics/logs (stale data is
   worthless); waiting is correct for work items (data loss is a bug).
3. **Who observes the wait?** If nobody upstream can react to backpressure,
   you have only moved the cliff.

The measurement that matters: producer wait time distribution. A healthy
bounded pipeline shows near-zero waits at normal load and graceful growth
under stress — the channel is your load gauge.
"""

_m12_backpressure_vi = r"""## Backpressure như một công cụ thiết kế

Queue không giới hạn là kẻ giết người âm thầm của service dưới tải. Trình
tự luôn như vậy: producer vượt consumer → queue phình → bộ nhớ phình → áp
lực GC tăng → độ trễ tăng → timeout → retry → THÊM tải. Queue không gây ra
sự cố; *sự vắng mặt của backpressure* mới gây ra.

Một bounded channel biến quá tải thành tín hiệu tường minh, sống sót được:

```csharp
var ch = Channel.CreateBounded<Job>(new BoundedChannelOptions(1_000)
{
    FullMode = BoundedChannelFullMode.Wait,   // writer cảm nhận được tải
    SingleReader = false,
});

// Producer:
try { await ch.Writer.WriteAsync(job, ct); }
catch (ChannelClosedException) { /* đang shutdown: shed */ }
```

Với `Wait`, độ trễ phía producer tăng khi queue đầy — hệ thống suy giảm về
đúng throughput thật của consumer thay vì chết. Các caller thượng nguồn
(handler HTTP, message pump) cảm nhận áp lực và có thể shed, trả 503, hoặc
chậm lại — hành vi hệ thống đúng đắn.

Các quyết định thiết kế mà bounded channel buộc bạn đưa ra (tất cả đều là
câu hỏi tốt):

1. **Capacity** = burst tối đa chấp nhận được. 0 = rendezvous thuần; nhỏ =
   nhạy độ trễ; lớn = hấp thụ burst (và ngốn bộ nhớ).
2. **Drop hay wait?** Drop đúng cho metrics/log (dữ liệu cũ vô giá trị);
   wait đúng cho work item (mất dữ liệu là bug).
3. **Ai quan sát sự chờ?** Nếu không ai thượng nguồn phản ứng được với
   backpressure, bạn chỉ dời vách núi đi chỗ khác.

Phép đo quan trọng nhất: phân bố thời gian chờ của producer. Pipeline
bounded khỏe mạnh cho thấy chờ gần bằng 0 dưới tải thường và tăng duyên
dáng dưới tải nặng — channel chính là đồng hồ đo tải của bạn.
"""

_m12_completion = r"""## Completion and graceful shutdown

Completion is the channel's way of saying "no more items, ever":
`ch.Writer.Complete()` (or `TryComplete`, or `Complete(exception)` to fault
it). After completion:

- `WriteAsync` throws `ChannelClosedException` — the producer's signal to
  stop accepting.
- `ReadAllAsync` drains remaining buffered items, THEN ends. This drain
  semantics is what makes graceful shutdown almost free.
- `ReadAsync` throws `ChannelClosedException` once empty.

```csharp
// Producer side
ch.Writer.TryComplete();                       // stop accepting, keep delivering

// Consumer side — drains then exits
await foreach (var item in ch.Reader.ReadAllAsync())
    Process(item);
```

Graceful shutdown of a multi-stage pipeline has a strict order — reverse
of the data flow:

1. Stop the ingest (stop writing to stage 1's input, or close the source).
2. Stage 1 drains its input, finishes, completes its OUTPUT channel.
3. Stage 2's `ReadAllAsync` ends because its input completed; it drains,
   completes its output... and so on down the chain.

Each stage needs the same skeleton: `try { drain } finally { complete
output }`. Forgetting the finally orphans the next stage (its reader
waits forever) — the classic hung-shutdown bug.

Error propagation: `Complete(new SomeException(...))` makes readers throw
that exception after draining — the pipeline equivalent of a fault. And
cancellation is NOT completion: cancelling the token aborts readers/writers
mid-flight (a rude stop), while completion is a clean stop. Production
systems usually want: cancel-then-drain with a deadline.
"""

_m12_completion_vi = r"""## Completion và graceful shutdown

Completion là cách channel nói "không còn gì nữa, mãi mãi":
`ch.Writer.Complete()` (hoặc `TryComplete`, hoặc `Complete(exception)` để
làm nó lỗi). Sau completion:

- `WriteAsync` ném `ChannelClosedException` — tín hiệu cho producer ngừng
  nhận.
- `ReadAllAsync` rút cạn các phần tử còn buffer, RỒI kết thúc. Ngữ nghĩa
  rút cạn này khiến graceful shutdown gần như miễn phí.
- `ReadAsync` ném `ChannelClosedException` một khi rỗng.

```csharp
// Phía producer
ch.Writer.TryComplete();                       // ngừng nhận, vẫn giao tiếp

// Phía consumer — rút cạn rồi thoát
await foreach (var item in ch.Reader.ReadAllAsync())
    Process(item);
```

Graceful shutdown của pipeline nhiều tầng có thứ tự nghiêm ngặt — ngược
chiều dữ liệu:

1. Ngừng ingest (ngừng ghi vào input của tầng 1, hoặc đóng nguồn).
2. Tầng 1 rút cạn input của mình, hoàn tất, complete kênh OUTPUT của nó.
3. `ReadAllAsync` của tầng 2 kết thúc vì input của nó đã complete; tầng 2
   rút cạn, complete output của nó... và cứ thế dọc theo chuỗi.

Mỗi tầng cần cùng một khung: `try { drain } finally { complete output }`.
Quên finally là bỏ rơi tầng kế (reader của nó chờ mãi mãi) — bug treo
shutdown kinh điển.

Lan truyền lỗi: `Complete(new SomeException(...))` khiến reader ném
exception đó sau khi rút cạn — tương đương fault trong pipeline. Và
cancellation KHÔNG phải completion: hủy token chặn ngang reader/writer
(dừng thô), còn completion là dừng sạch. Hệ production thường muốn:
cancel-rồi-rút-cạn với deadline.
"""

_m12_pipelines = r"""## Multi-stage pipeline architecture

Real pipelines chain stages, each with its own channel input and output:

```csharp
var raw     = Channel.CreateBounded<Line>(2_000);
var parsed  = Channel.CreateBounded<Trade>(2_000);
var scored  = Channel.CreateBounded<Score>(2_000);

var s1 = Task.Run(() => IngestAsync(raw.Writer));           // write raw, complete it
var s2 = Task.Run(() => StageAsync(raw.Reader, parsed.Writer,
                                   Parse, "parse"));         // pump raw → parsed
var s3 = Task.Run(() => StageAsync(parsed.Reader, scored.Writer,
                                   Score, "score"));         // pump parsed → scored
var s4 = Task.Run(() => SinkAsync(scored.Reader));          // final consumer
await Task.WhenAll(s1, s2, s3, s4);
```

Each stage is the same `PumpAsync` shape the checkpoint tests: read all →
transform → write all → complete output. Composition properties you get
for free:

- **Concurrency between stages** — parsing overlaps scoring; each stage is
  also internally parallelizable (fan-out N consumers per channel).
- **Isolation** — one slow stage backs up only its input channel; the
  backpressure propagates upstream instead of collapsing the process.
- **Testability** — test each stage with an in-memory channel; no mocking
  framework needed.

When channels beat `Task`-based fan-out (`Task.WhenAll` over all items):
streaming/bounded memory (items flow, nothing accumulates), dynamic rates
(producer/consumer speeds differ), and exactly-once competing consumers.
When Tasks win: fixed, known item sets where you want per-item results —
`Task.WhenAll` + `Select` is simpler and has no infrastructure.

Sizing note: capacity per stage should reflect that stage's burst
tolerance; a chain of unbounded channels is just a distributed way to run
out of memory.
"""

_m12_pipelines_vi = r"""## Kiến trúc pipeline nhiều tầng

Pipeline thật xâu chuỗi các tầng, mỗi tầng có kênh input và output riêng:

```csharp
var raw     = Channel.CreateBounded<Line>(2_000);
var parsed  = Channel.CreateBounded<Trade>(2_000);
var scored  = Channel.CreateBounded<Score>(2_000);

var s1 = Task.Run(() => IngestAsync(raw.Writer));           // ghi raw, complete nó
var s2 = Task.Run(() => StageAsync(raw.Reader, parsed.Writer,
                                   Parse, "parse"));         // bơm raw → parsed
var s3 = Task.Run(() => StageAsync(parsed.Reader, scored.Writer,
                                   Score, "score"));         // bơm parsed → scored
var s4 = Task.Run(() => SinkAsync(scored.Reader));          // consumer cuối
await Task.WhenAll(s1, s2, s3, s4);
```

Mỗi tầng là cùng hình dạng `PumpAsync` mà checkpoint kiểm thử: đọc hết →
transform → ghi hết → complete output. Các tính chất kết hợp bạn được
miễn phí:

- **Đồng thời giữa các tầng** — parse đè lên score; mỗi tầng cũng song song
  hóa được bên trong (fan-out N consumer mỗi kênh).
- **Cách ly** — một tầng chậm chỉ làm ùn input channel của nó; backpressure
  lan ngược thượng nguồn thay vì sập cả process.
- **Kiểm thử được** — test từng tầng bằng channel trong bộ nhớ; không cần
  mocking framework.

Khi nào channels thắng fan-out kiểu `Task` (`Task.WhenAll` trên mọi phần
tử): streaming/bộ nhớ giới hạn (phần tử chảy, không tích tụ), tốc độ động
(producer/consumer chênh nhau), và consumer cạnh tranh exactly-once. Khi
nào Task thắng: tập phần tử cố định, đã biết, muốn kết quả từng phần tử —
`Task.WhenAll` + `Select` đơn giản hơn và không cần hạ tầng.

Ghi chú kích thước: capacity mỗi tầng nên phản ánh khả năng chịu burst của
tầng đó; chuỗi các channel unbounded chỉ là cách chạy hết bộ nhớ một cách
phân tán.
"""

_m12_checkpoint = r"""## Checkpoint: channels

The graded task exercises the full lifecycle: async pump with completion
propagation, bounded-channel draining, and in-order output. Practice adds
competing-consumer fan-out (exactly-once processing) and the
stop-accepting-drain-what-you-have shutdown pattern.
"""

_m12_checkpoint_vi = r"""## Checkpoint: channels

Bài được chấm luyện toàn vòng đời: bơm bất đồng bộ với lan truyền completion,
rút cạn bounded channel, và output đúng thứ tự. Practice thêm fan-out
consumer cạnh tranh (xử lý exactly-once) và pattern shutdown ngừng-nhận-
rút-cạn-đã-nhận.
"""
