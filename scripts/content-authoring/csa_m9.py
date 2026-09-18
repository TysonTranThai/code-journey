"""Module 9 — Advanced async programming (csa-m9)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-async-deep",
        "Advanced Async",
        "State machines, ValueTask, cancellation propagation, async streams, and the failure modes async hides.",
    )

    csa.register_lesson(
        MID, "csa-m9-state-machine", "The async state machine",
        "What await compiles into: builders, MoveNext, hot vs cold paths — with a real decompilation view.",
        16, "advanced", _m9_state_machine, _m9_state_machine_vi,
    )
    csa.register_lesson(
        MID, "csa-m9-valuetask", "ValueTask: when and why",
        "The allocation-free fast path, its two-contract rules, and the bugs it enables when misused.",
        15, "advanced", _m9_valuetask, _m9_valuetask_vi,
    )
    csa.register_lesson(
        MID, "csa-m9-cancellation", "Cancellation that actually works",
        "Tokens, links, registration, timeouts — and why cooperative cancellation fails silently.",
        15, "advanced", _m9_cancellation, _m9_cancellation_vi,
    )
    csa.register_lesson(
        MID, "csa-m9-async-streams", "Async streams and IAsyncDisposable",
        "IAsyncEnumerable pipelines, await using, and backpressure between async producers and consumers.",
        15, "advanced", _m9_streams, _m9_streams_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m9", "Checkpoint: async",
        "Synthesis: ValueTask discipline and cancellation correctness under real execution.",
        12, "advanced", _m9_checkpoint, _m9_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m9-task", MID,
        title="Async checkpoint",
        prompt=(
            "Implement `static async ValueTask<int> ReadCachedAsync(int key, Func<int, Task<int>> slowFetch)`: a "
            "static ConcurrentDictionary<int,int> cache; on hit return synchronously WITHOUT awaiting (ValueTask "
            "fast path); on miss await slowFetch and store the result. Then implement `static async Task<string> "
            "WithTimeout(Task<string> work, TimeSpan timeout)` returning the work's result or throwing "
            "TimeoutException — using CancellationTokenSource with a timeout, and cancelling the linked token."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "cache-fast-path",
                "code": (
                    "await Solution.ReadCachedAsync(1, async k => { await Task.Yield(); return k * 10; });\n"
                    "var r2 = await Solution.ReadCachedAsync(1, async k => { await Task.Yield(); return -1; });\n"
                    'Cj.Eq(r2, 10, "second read served from cache, fetcher not called again");'
                ),
                "hint": "TryGetValue first — return new ValueTask<int>(value) without touching the fetcher.",
            },
            {
                "name": "timeout-fires",
                "code": (
                    "var slow = Task.Delay(60_000);\n"
                    "var ex = await Cj.ThrowsAsync<TimeoutException>(() => Solution.WithTimeout(slow, TimeSpan.FromMilliseconds(50)));\n"
                    'Cj.True(ex is not null, "timeout throws");'
                ),
                "hint": "cts.CancelAfter(timeout); await task.WaitAsync(cts.Token) then translate OperationCanceledException to TimeoutException.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    static readonly ConcurrentDictionary<int, int> Cache = new();\n\n"
            "    public static async ValueTask<int> ReadCachedAsync(int key, Func<int, Task<int>> slowFetch)\n"
            "    {\n"
            "        if (Cache.TryGetValue(key, out var hit)) return hit;\n"
            "        var v = await slowFetch(key).ConfigureAwait(false);\n"
            "        Cache[key] = v;\n"
            "        return v;\n"
            "    }\n\n"
            "    public static async Task<string> WithTimeout(Task<string> work, TimeSpan timeout)\n"
            "    {\n"
            "        using var cts = new CancellationTokenSource(timeout);\n"
            "        try\n"
            "        {\n"
            "            return await work.WaitAsync(cts.Token).ConfigureAwait(false);\n"
            "        }\n"
            "        catch (OperationCanceledException)\n"
            "        {\n"
            "            throw new TimeoutException($\"work exceeded {timeout}\");\n"
            "        }\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    static readonly ConcurrentDictionary<int, int> Cache = new();\n\n"
            "    public static async ValueTask<int> ReadCachedAsync(int key, Func<int, Task<int>> slowFetch)\n"
            "    {\n"
            "        var v = await slowFetch(key);   // WRONG: always fetches\n"
            "        Cache[key] = v;\n"
            "        return v;\n"
            "    }\n\n"
            "    public static async Task<string> WithTimeout(Task<string> work, TimeSpan timeout)\n"
            "    {\n"
            "        using var cts = new CancellationTokenSource(timeout);\n"
            "        try\n"
            "        {\n"
            "            return await work.WaitAsync(cts.Token);\n"
            "        }\n"
            "        catch (OperationCanceledException)\n"
            "        {\n"
            "            return \"\";   // WRONG: swallows the timeout\n"
            "        }\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p9-async", "Async drills",
        "State-machine reasoning, cancellation links, async streams, and async-disposal discipline.",
        45, "advanced", "csa-m9-cancellation",
        ["csa-p9-token-link", "csa-p9-async-stream", "csa-p9-value-task-bug"],
    )
    csa.register_challenge(
        "csa-p9-token-link", MID,
        title="Linked cancellation",
        prompt=(
            "Implement `static async Task<int> RaceTask(Task<int> a, Task<int> b, CancellationToken external)` "
            "returning whichever of a/b finishes first — and it must stop waiting when external cancels, throwing "
            "OperationCanceledException. Use CancellationTokenSource.CreateLinkedTokenSource and Task.WhenAny with "
            "cancellation registration."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "race-external-cancel",
                "code": (
                    "using var cts = new CancellationTokenSource(50);\n"
                    "var slow1 = Task.Delay(60_000).ContinueWith(_ => 1);\n"
                    "var slow2 = Task.Delay(60_000).ContinueWith(_ => 2);\n"
                    "var ex = await Cj.ThrowsAsync<OperationCanceledException>(() => Solution.RaceTask(slow1, slow2, cts.Token));\n"
                    'Cj.True(ex is not null, "external cancellation wins the race");'
                ),
                "hint": "Link the token; register a callback that completes a TaskCompletionSource, WhenAny over both tasks plus that TCS task.",
            },
            {
                "name": "race-fast-wins",
                "code": (
                    "var fast = Task.FromResult(7);\n"
                    "var slow = new TaskCompletionSource<int>().Task;\n"
                    'Cj.Eq(await Solution.RaceTask(slow, fast, CancellationToken.None), 7, "completed task wins");'
                ),
                "hint": "WhenAny returns the first completed; return its result.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async Task<int> RaceTask(Task<int> a, Task<int> b, CancellationToken external)\n"
            "    {\n"
            "        using var linked = CancellationTokenSource.CreateLinkedTokenSource(external);\n"
            "        var winner = await Task.WhenAny(a, b, Task.Delay(Timeout.Infinite, linked.Token)).ConfigureAwait(false);\n"
            "        if (winner == a) return await a.ConfigureAwait(false);\n"
            "        if (winner == b) return await b.ConfigureAwait(false);\n"
            "        throw new OperationCanceledException(external);\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async Task<int> RaceTask(Task<int> a, Task<int> b, CancellationToken external)\n"
            "    {\n"
            "        var winner = await Task.WhenAny(a, b);   // WRONG: ignores external token\n"
            "        if (winner == a) return await a;\n"
            "        return await b;\n"
            "    }\n}"
        ),
        level="real-world",
    )
    csa.register_challenge(
        "csa-p9-async-stream", MID,
        title="Async stream pipeline",
        prompt=(
            "Implement `static async IAsyncEnumerable<int> MultiplyAsync(IAsyncEnumerable<int> source, int factor)` "
            "yielding each element times factor, and `static async Task<List<int>> Collect(IAsyncEnumerable<int> "
            "source)` materializing a stream to a list. Build the source with an async iterator that yields 1,2,3 "
            "with `await Task.Yield()` between items."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "pipeline",
                "code": (
                    "static async IAsyncEnumerable<int> Source()\n"
                    "{\n"
                    "    foreach (var n in new[] { 1, 2, 3 }) { await Task.Yield(); yield return n; }\n"
                    "}\n"
                    "var r = await Solution.Collect(Solution.MultiplyAsync(Source(), 10));\n"
                    'Cj.Eq(string.Join(",", r), "10,20,30", "multiplied stream");'
                ),
                "hint": "await foreach (var item in source.ConfigureAwait(false)) — multiply and yield return.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async IAsyncEnumerable<int> MultiplyAsync(IAsyncEnumerable<int> source, int factor)\n"
            "    {\n"
            "        await foreach (var item in source.ConfigureAwait(false))\n"
            "            yield return item * factor;\n"
            "    }\n\n"
            "    public static async Task<List<int>> Collect(IAsyncEnumerable<int> source)\n"
            "    {\n"
            "        var r = new List<int>();\n"
            "        await foreach (var item in source.ConfigureAwait(false)) r.Add(item);\n"
            "        return r;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async IAsyncEnumerable<int> MultiplyAsync(IAsyncEnumerable<int> source, int factor)\n"
            "    {\n"
            "        await foreach (var item in source.ConfigureAwait(false))\n"
            "            yield return item + factor;   // WRONG operator\n"
            "    }\n\n"
            "    public static async Task<List<int>> Collect(IAsyncEnumerable<int> source)\n"
            "    {\n"
            "        var r = new List<int>();\n"
            "        await foreach (var item in source.ConfigureAwait(false)) r.Add(item);\n"
            "        return r;\n"
            "    }\n}"
        ),
        level="imitation",
    )
    csa.register_challenge(
        "csa-p9-value-task-bug", MID,
        title="Diagnose the ValueTask bug",
        prompt=(
            "ValueTask has strict rules: await it exactly once, never await after consuming, never await concurrently. "
            "Implement `static async ValueTask<int> SafeDouble(ValueTask<int> source)` CORRECTLY: await the source "
            "once and return the result times 2. Then implement `static async Task<int> BrokenDouble(ValueTask<int> "
            "source)` that demonstrates the forbidden pattern — await it twice (`var a = await source; var b = await "
            "source; return a + b;`). The test runs the BROKEN one against a ValueTask backed by an IValueTaskSource "
            "created via ManualResetValueTaskSourceCore to prove it throws/misbehaves."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "safe-works",
                "code": (
                    "var vt = new ValueTask<int>(21);\n"
                    'Cj.Eq(await Solution.SafeDouble(vt), 42, "safe double");'
                ),
                "hint": "var v = await source; return v * 2.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async ValueTask<int> SafeDouble(ValueTask<int> source)\n"
            "        => (await source.ConfigureAwait(false)) * 2;\n\n"
            "    public static async Task<int> BrokenDouble(ValueTask<int> source)\n"
            "    {\n"
            "        var a = await source.ConfigureAwait(false);\n"
            "        var b = await source.ConfigureAwait(false);   // forbidden: second await\n"
            "        return a + b;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async ValueTask<int> SafeDouble(ValueTask<int> source)\n"
            "        => (await source.ConfigureAwait(false)) + 2;   // WRONG math\n\n"
            "    public static async Task<int> BrokenDouble(ValueTask<int> source)\n"
            "    {\n"
            "        var a = await source.ConfigureAwait(false);\n"
            "        var b = await source.ConfigureAwait(false);\n"
            "        return a + b;\n"
            "    }\n}"
        ),
        level="debugging",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m9_state_machine = r"""## The async state machine

An `async` method is rewritten by the compiler into a **struct state
machine** implementing `IAsyncStateMachine`: your locals become fields,
each `await` becomes a state number, and the whole body lives inside one
big `MoveNext()` switch. The async method builder (`AsyncTaskMethodBuilder`)
owns a `Task` that the machine completes.

```csharp
// What you write:
async Task<int> LoadAsync() { var a = await A(); var b = await B(); return a + b; }

// What the compiler writes (conceptually):
struct LoadMachine : IAsyncStateMachine
{
    public int State;          // -1 start; 0 after first await...
    public TaskAwaiter<int> Awaitee;
    int a;                     // hoisted local
    public void MoveNext()
    {
        switch (State)
        {
            case -1: goto FIRST;
            case 0: a = Awaitee.GetResult(); goto SECOND;
        }
        FIRST: Awaitee = A().GetAwaiter();
        if (!Awaitee.IsCompleted) { State = 0; return; }   // park, resume later
        a = Awaitee.GetResult();
        SECOND: /* await B, same pattern, then builder.SetResult(a + b) */
    }
}
```

Two consequences worth internalizing:

1. **The synchronous fast path is real.** If every awaitable is already
   complete, the machine runs through all states in the original call — no
   thread switch, and with `ValueTask` no allocation either.
2. **`await` is cooperative**, not preemptive: code between awaits runs
   synchronously on the caller's thread. Long CPU loops between awaits ARE
   blocking, whatever the method says.

What you get from knowing this: you can read an async stack trace (`MoveNext`
frames), predict where an exception surfaces (the builder rethrows at the
await that failed), and understand why async methods cannot have `out`
parameters (the machine struct must survive across suspension).
"""

_m9_state_machine_vi = r"""## Máy trạng thái async

Một phương thức `async` được compiler viết lại thành **máy trạng thái
struct** cài đặt `IAsyncStateMachine`: biến cục bộ của bạn thành field, mỗi
`await` thành một số trạng thái, và toàn bộ thân nằm trong một khối `MoveNext()`
switch lớn. Async method builder (`AsyncTaskMethodBuilder`) sở hữu một `Task`
mà máy hoàn thành.

```csharp
// Bạn viết:
async Task<int> LoadAsync() { var a = await A(); var b = await B(); return a + b; }

// Compiler viết lại (khái niệm):
struct LoadMachine : IAsyncStateMachine
{
    public int State;          // -1 bắt đầu; 0 sau await đầu tiên...
    public TaskAwaiter<int> Awaitee;
    int a;                     // biến cục bộ được nâng lên
    public void MoveNext()
    {
        switch (State)
        {
            case -1: goto FIRST;
            case 0: a = Awaitee.GetResult(); goto SECOND;
        }
        FIRST: Awaitee = A().GetAwaiter();
        if (!Awaitee.IsCompleted) { State = 0; return; }   // đỗ xe, tiếp sau
        a = Awaitee.GetResult();
        SECOND: /* await B, cùng pattern, rồi builder.SetResult(a + b) */
    }
}
```

Hai hệ quả đáng thuộc:

1. **Đường nhanh đồng bộ là thật.** Nếu mọi awaitable đã hoàn thành, máy
   chạy qua mọi trạng thái ngay trong lần gọi — không đổi thread, và với
   `ValueTask` còn không cấp phát.
2. **`await` là hợp tác**, không phải chiếm quyền: code giữa các await chạy
   đồng bộ trên thread của caller. Vòng CPU dài giữa các await LÀ blocking,
   dù phương thức có chữ async.

Hiểu điều này bạn được gì: đọc được async stack trace (khung `MoveNext`),
dự đoán được exception xuất hiện ở đâu (builder rethrow tại await bị lỗi),
và hiểu vì sao async method không có được `out` (struct máy phải sống qua
mọi lần treo).
"""

_m9_valuetask = r"""## ValueTask: when and why

`Task<T>` always allocates (and boxes `T` when it is a value type).
`ValueTask<T>` is a struct that holds EITHER a `T` or a `Task<T>` — the
synchronous/hot path allocates nothing:

```csharp
// Cache-first accessor: the ideal ValueTask citizen
ValueTask<int> GetAsync(int key) =>
    _cache.TryGetValue(key, out var v)
        ? new ValueTask<int>(v)          // no allocation
        : new ValueTask<int>(FetchAsync(key));  // falls back to Task
```

The contract that keeps ValueTask safe (violating it is undefined
behavior, not just a bug):

1. **Await exactly once.** No double-await, no `.Result` after await.
2. **Never await concurrently.**
3. **Do not store it** — await before the next await point, or call
   `.AsTask()` if you must keep it.
4. Do not compose it directly (`WhenAll`) — convert with `.AsTask()` first.

When ValueTask is RIGHT: methods whose results are usually available
synchronously (caches, buffered reads, validation), or allocation-sensitive
hot paths measured to allocate. When it is WRONG: public library APIs
where callers will store/compose/await-twice — the ergonomics trap eats the
performance win. Default to `Task`, escalate to `ValueTask` with evidence.
"""

_m9_valuetask_vi = r"""## ValueTask: khi nào và vì sao

`Task<T>` luôn cấp phát (và box `T` khi là value type). `ValueTask<T>` là
struct chứa HOẶC một `T` HOẶC một `Task<T>` — đường nóng/đồng bộ không cấp
phát gì:

```csharp
// Accessor cache-first: công dân ValueTask lý tưởng
ValueTask<int> GetAsync(int key) =>
    _cache.TryGetValue(key, out var v)
        ? new ValueTask<int>(v)          // không cấp phát
        : new ValueTask<int>(FetchAsync(key));  // quay về Task
```

Hợp đồng giữ ValueTask an toàn (vi phạm là hành vi không xác định, không
chỉ là bug):

1. **Await đúng một lần.** Không double-await, không `.Result` sau await.
2. **Không bao giờ await đồng thời.**
3. **Không lưu nó** — await trước điểm await kế, hoặc gọi `.AsTask()` nếu
   buộc phải giữ.
4. Không compose trực tiếp (`WhenAll`) — convert bằng `.AsTask()` trước.

Khi nào ValueTask ĐÚNG: phương thức mà kết quả thường có sẵn đồng bộ
(cache, đọc buffer, xác thực), hoặc đường nóng nhạy cảm cấp phát đã được đo.
Khi nào SAI: API thư viện công khai nơi caller sẽ lưu/compose/await-hai-lần
— cái bẫy ergonomics nuốt chửng lợi nhuận hiệu năng. Mặc định dùng `Task`,
lên `ValueTask` khi có bằng chứng.
"""

_m9_cancellation = r"""## Cancellation that actually works

Cancellation in .NET is **cooperative**: `CancellationToken` carries the
request, your code must CHECK it. The failure mode that eats production:
operations that keep running because nobody looks at the token.

```csharp
// The four integration points:
async Task Work(CancellationToken ct)
{
    ct.ThrowIfCancellationRequested();          // 1. explicit check
    await Task.Delay(100, ct);                  // 2. async APIs honor it
    using var reg = ct.Register(() => { });     // 3. callback on cancel
    var other = otherCts.Token;                 // 4. linking:
}

using var linked = CancellationTokenSource.CreateLinkedTokenSource(a, b);
// linked.Token cancels when EITHER a or b cancels
```

Timeouts are just cancellation with a clock:
`new CancellationTokenSource(TimeSpan.FromSeconds(5))`, or on .NET 8+,
`task.WaitAsync(TimeSpan)` — which leaves the underlying work running
(WaitAsync abandons the wait, it does not stop the work; only the token
passed INTO the work does that).

The discipline that separates real cancellation from theater:

- **Pass the token everywhere** — an API that takes a token and ignores it
  is worse than one that doesn't pretend. Parameter order: token last.
- **Propagate into every layer** — a DB call without a token cannot be
  cancelled, whatever the HTTP handler did.
- **Distinguish outcomes**: `OperationCanceledException` (expected) vs
  timeouts (diagnose) vs faults (bug). Swallowing OCE hides shutdown bugs.
- **Dispose your CTS** — timers inside un-disposed sources leak.

Linked sources compose shutdown trees: request-scoped token linked to
server shutdown, linked to upstream cancels — the standard ASP.NET Core
pattern.
"""

_m9_cancellation_vi = r"""## Cancellation hoạt động thật

Cancellation trong .NET là **hợp tác**: `CancellationToken` mang yêu cầu,
code của bạn phải TỰ kiểm tra. Chế độ lỗi ăn mòn production: các thao tác
vẫn chạy vì không ai nhìn token.

```csharp
// Bốn điểm tích hợp:
async Task Work(CancellationToken ct)
{
    ct.ThrowIfCancellationRequested();          // 1. kiểm tra tường minh
    await Task.Delay(100, ct);                  // 2. async API tôn trọng nó
    using var reg = ct.Register(() => { });     // 3. callback khi cancel
    var other = otherCts.Token;                 // 4. linking:
}

using var linked = CancellationTokenSource.CreateLinkedTokenSource(a, b);
// linked.Token bị cancel khi HOẶC a hoặc b cancel
```

Timeout chỉ là cancellation có đồng hồ:
`new CancellationTokenSource(TimeSpan.FromSeconds(5))`, hoặc trên .NET 8+,
`task.WaitAsync(TimeSpan)` — cái này bỏ cuộc chờ chứ không dừng công việc
chạy; chỉ token truyền VÀO công việc mới dừng được nó.

Kỷ luật phân biệt cancellation thật với cancellation diễn:

- **Truyền token đi khắp nơi** — API nhận token mà bỏ qua thì tệ hơn API
  không giả vờ nhận. Thứ tự tham số: token cuối.
- **Lan truyền tới mọi tầng** — lời gọi DB không có token thì không thể bị
  cancel, dù HTTP handler có làm gì.
- **Phân biệt kết cục**: `OperationCanceledException` (đúng dự kiến) vs
  timeout (cần chẩn đoán) vs fault (bug). Nuốt OCE giấu bug shutdown.
- **Dispose CTS của bạn** — timer trong source chưa dispose bị rò rỉ.

Linked source ghép cây shutdown: token theo request linked với shutdown của
server, linked với cancel thượng nguồn — pattern chuẩn của ASP.NET Core.
"""

_m9_streams = r"""## Async streams and IAsyncDisposable

`IAsyncEnumerable<T>` is the async `IEnumerable`: items arrive over time,
and `await foreach` consumes them. An async iterator combines `yield return`
with `await`:

```csharp
static async IAsyncEnumerable<Trade> StreamAsync(
    IAsyncEnumerable<string> lines, [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var line in lines.WithCancellation(ct).ConfigureAwait(false))
        if (Trade.TryParse(line, out var t)) yield return t;
}
```

Backpressure is inherent: the consumer pulls; the producer only produces
when pulled (unlike `Task`-based fan-out, which produces as fast as it can).
For bounded buffering semantics, compose streams with `Channel<T>`
(Module 13).

`IAsyncDisposable` + `await using` close the lifecycle for resources whose
release is itself asynchronous (network connections, streams, DB readers):

```csharp
await using var conn = await pool.RentAsync(ct);
// DisposeAsync runs on scope exit — even on exception
```

The trap: `DisposeAsync` is NOT awaited if you use `using` instead of
`await using` — the compiler inserts a sync-over-async wait, or worse,
fire-and-forget semantics depending on the type. And `ConfigureAwait(false)`
belongs on the `await foreach` line, applied to the enumerator, not the
items.
"""

_m9_streams_vi = r"""## Async stream và IAsyncDisposable

`IAsyncEnumerable<T>` là bản async của `IEnumerable`: phần tử đến theo thời
gian, và `await foreach` tiêu thụ chúng. Async iterator kết hợp `yield return`
với `await`:

```csharp
static async IAsyncEnumerable<Trade> StreamAsync(
    IAsyncEnumerable<string> lines, [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var line in lines.WithCancellation(ct).ConfigureAwait(false))
        if (Trade.TryParse(line, out var t)) yield return t;
}
```

Backpressure có sẵn: consumer kéo; producer chỉ sản xuất khi được kéo
(khác fan-out kiểu `Task`, sản xuất hết tốc lực). Muốn ngữ nghĩa buffer giới
hạn, compose stream với `Channel<T>` (Module 13).

`IAsyncDisposable` + `await using` khép vòng đời cho tài nguyên mà việc giải
phóng cũng bất đồng bộ (kết nối mạng, stream, DB reader):

```csharp
await using var conn = await pool.RentAsync(ct);
// DisposeAsync chạy khi thoát phạm vi — kể cả khi có exception
```

Cái bẫy: `DisposeAsync` KHÔNG được await nếu bạn dùng `using` thay cho
`await using` — compiler chèn chờ sync-over-async, hoặc tệ hơn, ngữ nghĩa
fire-and-forget tùy kiểu. Và `ConfigureAwait(false)` nằm trên dòng
`await foreach`, áp vào enumerator, không phải các phần tử.
"""

_m9_checkpoint = r"""## Checkpoint: async

The graded task pairs the two disciplines that decide production async
quality: ValueTask fast-path discipline (cache hit = no allocation, no
await) and timeout-as-cancellation (translate OCE into TimeoutException,
cancel the linked source). The practice set adds linked-token races,
async-stream pipelines, and diagnosing the double-await bug live.
"""

_m9_checkpoint_vi = r"""## Checkpoint: async

Bài được chấm ghép hai kỷ luật quyết định chất lượng async production:
kỷ luật fast-path ValueTask (cache hit = không cấp phát, không await) và
timeout-là-cancellation (dịch OCE thành TimeoutException, cancel linked
source). Practice set bổ sung race token liên kết, pipeline async stream,
và chẩn đoán lỗi double-await ngay trên máy.
"""
