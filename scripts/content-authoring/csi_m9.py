#!/usr/bin/env python3
"""C# — Intermediate — Module 9: csi-async.

Task/async/await done properly: exception flow, Task.WhenAll fan-out,
cancellation, timeouts, and async streams. Ws are the canonical mistakes:
blocking on Result, dropped tasks, cancellation not propagated.

Harness notes: test bodies run inside sync `CjTest.Body()` — async results
are observed with `.GetAwaiter().GetResult()` (safe in the sandbox: no
synchronization context, thread-pool continuations). The FlakyApi simulator
ships in the challenge boilerplate, not the shared worker harness.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-async"

# Boilerplate additions: the provided flaky-API simulator learners code
# against (visible in Solution.cs, so tests see it too).
FLAKY_BOILERPLATE = CS_PRELUDE + (
    "using System.Threading;\n"
    "using System.Threading.Tasks;\n"
    "\n"
    "// Provided infrastructure — do not modify.\n"
    "public static class CjFlaky\n"
    "{\n"
    "    // Completes after delayMs. Keys starting with \"slow\" simulate a\n"
    "    // hung backend (5 s) regardless of delayMs.\n"
    "    public static async Task<string> FetchAsync(string key, int delayMs, CancellationToken ct)\n"
    "    {\n"
    "        int wait = key.StartsWith(\"slow\", StringComparison.Ordinal) ? 5000 : delayMs;\n"
    "        await Task.Delay(wait, ct);\n"
    "        return \"payload:\" + key;\n"
    "    }\n"
    "}\n"
)

SAVE_TRAP_BOILERPLATE = CS_PRELUDE + (
    "using System.Threading.Tasks;\n"
    "\n"
    "// Provided infrastructure — do not modify.\n"
    "public sealed class SaveTrap\n"
    "{\n"
    "    private readonly string[] _failing;\n"
    "    public SaveTrap(params string[] failingKeys) => _failing = failingKeys;\n"
    "\n"
    "    // Fails ASYNCHRONOUSLY for keys listed in the constructor.\n"
    "    public Task SaveAsync(string key)\n"
    "    {\n"
    "        foreach (string f in _failing)\n"
    "            if (f == key)\n"
    "                return Task.FromException(new System.InvalidOperationException(\"save failed: \" + key));\n"
    "        return Task.CompletedTask;\n"
    "    }\n"
    "}\n"
)

write_module(
    M,
    "Asynchronous Programming",
    "Tasks, async/await, fan-out with WhenAll, cancellation, timeouts, and async streams — without the classic traps.",
    "Lập trình bất đồng bộ",
    "Task, async/await, fan-out với WhenAll, hủy, timeout và async stream — không dính các bẫy kinh điển.",
    ["async-basics", "cancellation-timeouts", "async-streams", "csi-checkpoint-m9"],
    ["csi-p9-async"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "async-basics",
    "async/await: What Actually Happens",
    "Tasks as futures, await as suspension, exceptions flying through, and the sync-over-async tax.",
    18,
    r"""
## Task is a future; await is a suspension point

`async` marks a method as awaitable-composing; `await` yields the thread
until the awaited Task completes. The method state (locals) is captured and
resumed — code after `await` runs LATER, possibly on a different thread:

```csharp
async Task<string> FetchNameAsync(HttpClient http, string url)
{
    string body = await http.GetStringAsync(url);  // thread released here
    return body.Trim();                            // resumed after completion
}
```

`Task` = async operation with no result; `Task<T>` = with a result. Methods
named `*Async` returning Task follow the convention.

## Exceptions flow through the Task

An exception inside `async Task` is stored ON the Task and re-thrown at the
`await` — unwrapped, as the original type:

```csharp
try { await DivideAsync(1, 0); }
catch (DivideByZeroException ex) { /* caught here, unwrapped */ }
```

`async void` has nowhere to route exceptions except the thread pool — it can
crash the process. Use `async void` ONLY for event handlers (Module 4).

## Blocking on a Task: .Result and its friends

`.Result` / `.Wait()` / `.GetAwaiter().GetResult()` block the calling
thread until the task completes. In app code with a synchronization context
that deadlocks; even without one it burns a thread and WRAPS exceptions:

```csharp
string s = FetchAsync().Result;   // throws AggregateException, not the real type
```

`await` unwraps — that's why production code goes async all the way, and
why a test harness (like this one) may block on tasks: `FetchAsync()
.GetAwaiter().GetResult()` observes the same unwrapping? No — only `await`
unwraps. Blocking surfaces `AggregateException`. The habit to build: async
callers await; sync callers who must block expect the wrapper.

## Check your understanding

- Where does an exception thrown in an async method surface? (At the awaiting await, unwrapped.)
- What does `.Result` throw when the task fails? (AggregateException wrapping the real exception.)
""",
    "async/await: Thực sự Chuyện gì xảy ra",
    "Task là future, await là điểm treo, exception bay qua, và cái giá của sync-over-async.",
    r"""
## Task là future; await là điểm treo

`async` đánh dấu phương thức có thể ghép await; `await` nhả thread cho tới
khi Task được awaited hoàn tất. Trạng thái phương thức (biến cục bộ) được
chụp lại và tiếp tục — code sau `await` chạy SAU, có thể trên thread khác:

```csharp
async Task<string> FetchNameAsync(HttpClient http, string url)
{
    string body = await http.GetStringAsync(url);  // nhả thread tại đây
    return body.Trim();                            // tiếp tục sau khi xong
}
```

`Task` = thao tác async không kết quả; `Task<T>` = có kết quả. Phương thức
`*Async` trả Task theo đúng quy ước.

## Exception đi qua Task

Exception trong `async Task` được lưu TRÊN Task và ném lại tại `await` —
đã bóc vỏ, giữ nguyên kiểu gốc:

```csharp
try { await DivideAsync(1, 0); }
catch (DivideByZeroException ex) { /* bắt tại đây, đã bóc vỏ */ }
```

`async void` không có nơi nào đưa exception đi except thread pool — có thể
làm sập tiến trình. Chỉ dùng `async void` cho event handler (Module 4).

## Chặn trên Task: .Result và bạn bè

`.Result` / `.Wait()` / `.GetAwaiter().GetResult()` chặn thread gọi cho tới
khi task xong. Trong code ứng dụng có synchronization context thì deadlock;
dù không có vẫn đốt một thread và BỌC exception:

```csharp
string s = FetchAsync().Result;   // ném AggregateException, không phải kiểu gốc
```

`await` bóc vỏ — vì vậy production code async trọn độ, còn test harness
(như harness này) có thể chặn task: caller async thì await; caller đồng bộ
bắt buộc chặn phải ngờ lớp bọc AggregateException.

## Kiểm tra hiểu biết

- Exception trong phương thức async nổi lên ở đâu? (Tại await, đã bóc vỏ.)
- `.Result` ném gì khi task thất bại? (AggregateException bọc exception gốc.)
""",
    r"""
## Task là future; await là điểm treo

`async` đánh dấu phương thức có thể ghép await; `await` nhả thread cho tới
khi Task được awaited hoàn tất. Trạng thái phương thức (biến cục bộ) được
chụp lại và tiếp tục — code sau `await` chạy SAU, có thể trên thread khác:

```csharp
async Task<string> FetchNameAsync(HttpClient http, string url)
{
    string body = await http.GetStringAsync(url);  // nhả thread tại đây
    return body.Trim();                            // tiếp tục sau khi xong
}
```

`Task` = thao tác async không kết quả; `Task<T>` = có kết quả. Phương thức
`*Async` trả Task theo đúng quy ước.

## Exception đi qua Task

Exception trong `async Task` được lưu TRÊN Task và ném lại tại `await` —
đã bóc vỏ, giữ nguyên kiểu gốc:

```csharp
try { await DivideAsync(1, 0); }
catch (DivideByZeroException ex) { /* bắt tại đây, đã bóc vỏ */ }
```

`async void` không có nơi nào đưa exception đi except thread pool — có thể
làm sập tiến trình. Chỉ dùng `async void` cho event handler (Module 4).

## Chặn trên Task: .Result và bạn bè

`.Result` / `.Wait()` / `.GetAwaiter().GetResult()` chặn thread gọi cho tới
khi task xong. Trong code ứng dụng có synchronization context thì deadlock;
dù không có vẫn đốt một thread và BỌC exception:

```csharp
string s = FetchAsync().Result;   // ném AggregateException, không phải kiểu gốc
```

`await` bóc vỏ — vì vậy production code async trọn độ, còn test harness
(như harness này) có thể chặn task: caller async thì await; caller đồng bộ
bắt buộc chặn phải ngờ lớp bọc AggregateException.

## Kiểm tra hiểu biết

- Exception trong phương thức async nổi lên ở đâu? (Tại await, đã bóc vỏ.)
- `.Result` ném gì khi task thất bại? (AggregateException bọc exception gốc.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "cancellation-timeouts",
    "Fan-out, Cancellation, and Timeouts",
    "Task.WhenAll for concurrency, CancellationToken through every layer, and time-boxing with WhenAny + Task.Delay.",
    17,
    r"""
## Sequential awaits vs WhenAll fan-out

Awaits in sequence run one after another. Start all tasks FIRST, then await
them — they overlap:

```csharp
Task<int> a = ComputeAsync(1);          // starts now
Task<int> b = ComputeAsync(2);          // starts now
int[] both = await Task.WhenAll(a, b);  // total wait = max, not sum
```

Calling `ComputeAsync` runs the method synchronously until its first
`await`, then returns the running Task. That's why "start then await" is
not the same as "await then start" — a fan-out where the first await comes
before the last start is mostly sequential.

WhenAll re-throws the FIRST exception; inspect each task's status if
partial results matter.

## CancellationToken: the cooperative contract

Cancellation is COOPERATIVE — the token signals, your code checks:

```csharp
async Task WorkAsync(CancellationToken ct)
{
    for (int i = 0; i < 1000; i++)
    {
        ct.ThrowIfCancellationRequested();     // or ct.IsCancellationRequested
        await StepAsync(i, ct);                // pass the token DOWN
    }
}
```

Pass the token into every async call; a cancellation that never reaches the
innermost operation is not cancellation. Throwing
`OperationCanceledException` (the token's job) is the convention callers
expect.

## Timeouts: WhenAny + Task.Delay, or WaitAsync

```csharp
string body = await FetchAsync(ct).WaitAsync(TimeSpan.FromSeconds(2), ct);
```

`Task.WaitAsync(timeout, ct)` (.NET 8+) throws `TimeoutException` when the
deadline passes — the modern single-task time-box. The classic shape is
`Task.WhenAny(work, Task.Delay(timeout, ct))` and comparing the winner.
Either way the underlying operation should also receive the token so it can
actually STOP.

## Fire-and-forget is a bug factory

An un-awaited Task drops exceptions and races process shutdown. If you
truly can't await, capture the task and observe its completion explicitly
with internal try/catch — never a bare discarded call around something that
can fail.

## Check your understanding

- When does `ComputeAsync(1)` actually begin running? (Synchronously, up to its first await.)
- Who performs cancellation? (Your code, cooperatively — the token only signals.)
""",
    "Fan-out, Hủy, và Timeout",
    "Task.WhenAll cho đồng thời, CancellationToken xuyên suốt mọi tầng, và time-box bằng WhenAny + Task.Delay.",
    r"""
## Await tuần tự vs fan-out WhenAll

Await nối tiếp nhau chạy lần lượt. Khởi động TẤT CẢ task TRƯỚC, rồi await —
chúng chồng lên nhau:

```csharp
Task<int> a = ComputeAsync(1);          // bắt đầu ngay
Task<int> b = ComputeAsync(2);          // bắt đầu ngay
int[] both = await Task.WhenAll(a, b);  // tổng thời gian = max, không phải tổng
```

Gọi `ComputeAsync` chạy phương thức đồng bộ cho tới `await` đầu tiên, rồi
trả Task đang chạy. Vì sao "start rồi await" khác "await rồi start" — một
fan-out mà await đầu đến trước start cuối thì gần như tuần tự.

WhenAll ném lại exception ĐẦU TIÊN; xem trạng thái từng task nếu cần kết
quả một phần.

## CancellationToken: hợp đồng hợp tác

Hủy là HỢP TÁC — token phát tín hiệu, code của bạn kiểm tra:

```csharp
async Task WorkAsync(CancellationToken ct)
{
    for (int i = 0; i < 1000; i++)
    {
        ct.ThrowIfCancellationRequested();     // hoặc ct.IsCancellationRequested
        await StepAsync(i, ct);                // truyền token XUỐNG
    }
}
```

Truyền token vào mọi lời gọi async; một lệnh hủy không chạm tới thao tác
sau cùng thì không phải là hủy. Ném `OperationCanceledException` (việc của
token) là quy ước callers mong đợi.

## Timeout: WhenAny + Task.Delay, hoặc WaitAsync

```csharp
string body = await FetchAsync(ct).WaitAsync(TimeSpan.FromSeconds(2), ct);
```

`Task.WaitAsync(timeout, ct)` (.NET 8+) ném `TimeoutException` khi hết hạn —
time-box hiện đại cho một task. Dạng kinh điển là
`Task.WhenAny(work, Task.Delay(timeout, ct))` rồi so winner. Cách nào cũng
phải đưa token cho thao tác gốc để nó DỪNG thật.

## Fire-and-forget là nhà máy bug

Task không được await làm rơi exception và đua với shutdown. Nếu thật sự
không thể await, hãy giữ task và quan sát hoàn thành tường minh với
try/catch bên trong — không bao giờ vứt gọi trần quanh thứ có thể lỗi.

## Kiểm tra hiểu biết

- `ComputeAsync(1)` bắt đầu chạy khi nào? (Đồng bộ, cho tới await đầu tiên.)
- Ai thực hiện việc hủy? (Code của bạn, hợp tác — token chỉ phát tín hiệu.)
""",
    r"""
## Await tuần tự vs fan-out WhenAll

Await nối tiếp nhau chạy lần lượt. Khởi động TẤT CẢ task TRƯỚC, rồi await —
chúng chồng lên nhau:

```csharp
Task<int> a = ComputeAsync(1);          // bắt đầu ngay
Task<int> b = ComputeAsync(2);          // bắt đầu ngay
int[] both = await Task.WhenAll(a, b);  // tổng thời gian = max, không phải tổng
```

Gọi `ComputeAsync` chạy phương thức đồng bộ cho tới `await` đầu tiên, rồi
trả Task đang chạy. Vì sao "start rồi await" khác "await rồi start" — một
fan-out mà await đầu đến trước start cuối thì gần như tuần tự.

WhenAll ném lại exception ĐẦU TIÊN; xem trạng thái từng task nếu cần kết
quả một phần.

## CancellationToken: hợp đồng hợp tác

Hủy là HỢP TÁC — token phát tín hiệu, code của bạn kiểm tra:

```csharp
async Task WorkAsync(CancellationToken ct)
{
    for (int i = 0; i < 1000; i++)
    {
        ct.ThrowIfCancellationRequested();     // hoặc ct.IsCancellationRequested
        await StepAsync(i, ct);                // truyền token XUỐNG
    }
}
```

Truyền token vào mọi lời gọi async; một lệnh hủy không chạm tới thao tác
sau cùng thì không phải là hủy. Ném `OperationCanceledException` (việc của
token) là quy ước callers mong đợi.

## Timeout: WhenAny + Task.Delay, hoặc WaitAsync

```csharp
string body = await FetchAsync(ct).WaitAsync(TimeSpan.FromSeconds(2), ct);
```

`Task.WaitAsync(timeout, ct)` (.NET 8+) ném `TimeoutException` khi hết hạn —
time-box hiện đại cho một task. Dạng kinh điển là
`Task.WhenAny(work, Task.Delay(timeout, ct))` rồi so winner. Cách nào cũng
phải đưa token cho thao tác gốc để nó DỪNG thật.

## Fire-and-forget là nhà máy bug

Task không được await làm rơi exception và đua với shutdown. Nếu thật sự
không thể await, hãy giữ task và quan sát hoàn thành tường minh với
try/catch bên trong — không bao giờ vứt gọi trần quanh thứ có thể lỗi.

## Kiểm tra hiểu biết

- `ComputeAsync(1)` bắt đầu chạy khi nào? (Đồng bộ, cho tới await đầu tiên.)
- Ai thực hiện việc hủy? (Code của bạn, hợp tác — token chỉ phát tín hiệu.)
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "async-streams",
    "async Streams: await foreach",
    "IAsyncEnumerable<T> for data that arrives over time, producing and consuming async sequences.",
    12,
    r"""
## Producing: async iterator with yield return

```csharp
async IAsyncEnumerable<int> PollAsync(CancellationToken ct = default)
{
    for (int i = 0; i < 10; i++)
    {
        await Task.Delay(10, ct);
        yield return i;
    }
}
```

`yield return` inside an `async` method makes an async iterator (.NET Core
3.0+). Items stream out as they're produced — the consumer starts before
the producer finishes.

## Consuming: await foreach

```csharp
await foreach (int item in PollAsync(ct))
    Console.WriteLine(item);
```

`await foreach` awaits each MoveNextAsync — the loop suspends while waiting
for the next item instead of blocking a thread.

## Why not Task<List<T>>?

`Task<List<T>>` says "everything, eventually" — the caller waits for the
END before processing item one. `IAsyncEnumerable<T>` says "items over
time" — process as they arrive, cancel mid-stream, keep memory flat. Choose
by arrival pattern, not style.

## CancellationToken flows through

`WithCancellation(ct)` attaches the caller's token to the stream; inside
the producer, honor the token you were given. The
`[EnumeratorCancellation]` attribute on the default parameter merges caller
and local tokens — the pattern used by the BCL.

## Check your understanding

- Which type for a log tail? (IAsyncEnumerable — items arrive over time.)
- What does await foreach await? (Each item's availability.)
""",
    "async Stream: await foreach",
    "IAsyncEnumerable<T> cho dữ liệu đến theo thời gian, sản xuất và tiêu thụ chuỗi bất đồng bộ.",
    r"""
## Sản xuất: async iterator với yield return

```csharp
async IAsyncEnumerable<int> PollAsync(CancellationToken ct = default)
{
    for (int i = 0; i < 10; i++)
    {
        await Task.Delay(10, ct);
        yield return i;
    }
}
```

`yield return` trong phương thức `async` tạo async iterator (.NET Core
3.0+). Phần tử chảy ra khi được sản xuất — consumer bắt đầu trước khi
producer kết thúc.

## Tiêu thụ: await foreach

```csharp
await foreach (int item in PollAsync(ct))
    Console.WriteLine(item);
```

`await foreach` await từng MoveNextAsync — vòng lặp treo chờ phần tử kế
thay vì chặn thread.

## Vì sao không Task<List<T>>?

`Task<List<T>>` nghĩa là "tất cả, sau này" — caller chờ tới HẾT mới xử lý
phần tử đầu. `IAsyncEnumerable<T>` nghĩa là "phần tử theo thời gian" — xử
lý khi đến, hủy giữa dòng, giữ bộ nhớ phẳng. Chọn theo kiểu dữ liệu đến,
không phải phong cách.

## CancellationToken chảy xuyên suốt

`WithCancellation(ct)` gắn token của caller vào stream; bên trong producer,
tôn trọng token bạn nhận. Thuộc tính `[EnumeratorCancellation]` trên tham
số mặc định gộp token của caller và cục bộ — pattern BCL dùng.

## Kiểm tra hiểu biết

- Kiểu nào cho log tail? (IAsyncEnumerable — phần tử đến theo thời gian.)
- await foreach await cái gì? (Sự sẵn có của từng phần tử.)
""",
    r"""
## Sản xuất: async iterator với yield return

```csharp
async IAsyncEnumerable<int> PollAsync(CancellationToken ct = default)
{
    for (int i = 0; i < 10; i++)
    {
        await Task.Delay(10, ct);
        yield return i;
    }
}
```

`yield return` trong phương thức `async` tạo async iterator (.NET Core
3.0+). Phần tử chảy ra khi được sản xuất — consumer bắt đầu trước khi
producer kết thúc.

## Tiêu thụ: await foreach

```csharp
await foreach (int item in PollAsync(ct))
    Console.WriteLine(item);
```

`await foreach` await từng MoveNextAsync — vòng lặp treo chờ phần tử kế
thay vì chặn thread.

## Vì sao không Task<List<T>>?

`Task<List<T>>` nghĩa là "tất cả, sau này" — caller chờ tới HẾT mới xử lý
phần tử đầu. `IAsyncEnumerable<T>` nghĩa là "phần tử theo thời gian" — xử
lý khi đến, hủy giữa dòng, giữ bộ nhớ phẳng. Chọn theo kiểu dữ liệu đến,
không phải phong cách.

## CancellationToken chảy xuyên suốt

`WithCancellation(ct)` gắn token của caller vào stream; bên trong producer,
tôn trọng token bạn nhận. Thuộc tính `[EnumeratorCancellation]` trên tham
số mặc định gộp token của caller và cục bộ — pattern BCL dùng.

## Kiểm tra hiểu biết

- Kiểu nào cho log tail? (IAsyncEnumerable — phần tử đến theo thời gian.)
- await foreach await cái gì? (Sự sẵn có của từng phần tử.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p9-async",
    "Async Practice: Fetch, Fan-out, Cancel",
    "Write cooperative async pipelines, prove fan-out ordering, unwrap exceptions, and time-box flaky work.",
    "Luyện Async: Fetch, Fan-out, Hủy",
    "Viết pipeline async hợp tác, chứng minh thứ tự fan-out, bóc exception, và time-box công việc hay lỗi.",
    "cancellation-timeouts",
    30,
    "intermediate",
    [
        challenge(
            "csi-p9-sequence-total",
            "Sequential vs Concurrent: Prove It",
            """Two ways to await three simulated fetches. `SumSequential` awaits one at a time; `SumConcurrent` starts all three, then awaits together. The simulator logs an event per transition — prove the difference by EVENT ORDER, not the clock:

```csharp
public sealed class EventIo
{
    public EventIo();                            // provided
    public List<string> Log { get; }             // "start:N" / "done:N" entries
    public Task<int> FetchAsync(int step);       // provided: logs start, yields, logs done
}
static Task<int> SumSequential(EventIo io);     // sum of steps+1
static Task<int> SumConcurrent(EventIo io);     // same total, different order
```""",
            CS_PRELUDE + "using System.Threading.Tasks;\n",
            [
                (
                    "concurrent starts overlap",
                    r"""
var io = new Solution.EventIo();
Cj.Eq(Solution.SumConcurrent(io).GetAwaiter().GetResult(), 1 + 2 + 3, "sum of steps");
Cj.Eq(string.Join(",", io.Log.GetRange(0, 3)), "start:0,start:1,start:2", "all three start before any completes");
""",
                    "Start all FetchAsync tasks into variables BEFORE awaiting — Task.WhenAll after start.",
                ),
                (
                    "sequential interleaves strictly",
                    r"""
var io = new Solution.EventIo();
Cj.Eq(Solution.SumSequential(io).GetAwaiter().GetResult(), 6, "same total");
Cj.Eq(string.Join(",", io.Log.GetRange(0, 4)), "start:0,done:0,start:1,done:1", "each starts only after the previous finishes");
""",
                    "await inside the loop: each fetch begins after the previous completes.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p9-unwrap-debug",
            "Debug: The Wrapped Exception",
            """`LoadConfigAsync` fails with `InvalidOperationException("no config")`. `GetSetting` — the sync entry point — surfaces it wrongly: callers catch `InvalidOperationException` and never see it. Fix `GetSetting` so the REAL exception type reaches callers (not AggregateException), while staying synchronous.

```csharp
static Task<string> LoadConfigAsync();   // provided: throws InvalidOperationException
static string GetSetting();              // fix me
```""",
            CS_PRELUDE + "using System.Threading.Tasks;\n",
            [
                (
                    "real type surfaces",
                    r"""
try
{
    Solution.GetSetting();
    Cj.True(false, "should have thrown");
}
catch (System.InvalidOperationException ex)
{
    Cj.Eq(ex.Message, "no config", "original exception, unwrapped");
}
""",
                    "await the task, then unwrap: catch AggregateException and throw ex.InnerException, or use GetAwaiter().GetResult() which... no — blocking does NOT unwrap. Unwrap explicitly.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p9-cancel-token",
            "Cooperative Cancellation",
            """Implement a worker that honors cancellation: it processes items one at a time, checks the token BEFORE each item, and returns how many it completed. When cancelled mid-way, throw OperationCanceledException with the token.

```csharp
static Task<int> ProcessAsync(IEnumerable<int> items, Func<int, Task> work, CancellationToken ct);
```""",
            CS_PRELUDE + "using System.Threading;\nusing System.Threading.Tasks;\n",
            [
                (
                    "completes when not cancelled",
                    r"""
int ran = 0;
Cj.Eq(Solution.ProcessAsync(new[] { 1, 2, 3 }, i => { ran++; return System.Threading.Tasks.Task.CompletedTask; }, System.Threading.CancellationToken.None).GetAwaiter().GetResult(), 3, "all items");
Cj.Eq(ran, 3, "work ran for each");
""",
                    "Loop items, check ct.ThrowIfCancellationRequested() first, await work(item).",
                ),
                (
                    "pre-cancelled token aborts immediately",
                    r"""
var cts = new System.Threading.CancellationTokenSource();
cts.Cancel();
int ran = 0;
try
{
    Solution.ProcessAsync(new[] { 1, 2, 3 }, i => { ran++; return System.Threading.Tasks.Task.CompletedTask; }, cts.Token).GetAwaiter().GetResult();
    Cj.True(false, "should have thrown");
}
catch (System.OperationCanceledException) { }
Cj.Eq(ran, 0, "nothing ran on a pre-cancelled token");
""",
                    "Check BEFORE the first item — a pre-cancelled token runs zero items.",
                ),
                (
                    "stops promptly on cancel",
                    r"""
var cts = new System.Threading.CancellationTokenSource();
int ran = 0;
var t = Solution.ProcessAsync(
    new[] { 1, 2, 3, 4, 5 },
    i => { ran++; if (i == 2) cts.Cancel(); return System.Threading.Tasks.Task.CompletedTask; },
    cts.Token);
try { t.GetAwaiter().GetResult(); Cj.True(false, "should have thrown"); }
catch (System.OperationCanceledException) { }
Cj.Eq(ran, 2, "cancelled before item 3");
""",
                    "ThrowIfCancellationRequested BEFORE each work call — item 3 never runs.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p9-timeout",
            "Time-box a Flaky Operation",
            """Wrap an arbitrary task with a timeout: return its result if it finishes in time, otherwise throw TimeoutException. Use Task.WhenAny + Task.Delay (or Task.WaitAsync — .NET 8+).

```csharp
static Task<string> WithTimeout(Task<string> work, int timeoutMs);
```""",
            CS_PRELUDE + "using System.Threading.Tasks;\n",
            [
                (
                    "fast path wins",
                    r"""
Cj.Eq(Solution.WithTimeout(System.Threading.Tasks.Task.FromResult("fast"), 500).GetAwaiter().GetResult(), "fast", "completes in time");
""",
                    "Task.WhenAny(work, Task.Delay(timeoutMs)); if winner != work throw TimeoutException, else await work.",
                ),
                (
                    "slow path times out",
                    r"""
var slow = System.Threading.Tasks.Task.Run(async () => { await System.Threading.Tasks.Task.Delay(2000); return "slow"; });
try { Solution.WithTimeout(slow, 50).GetAwaiter().GetResult(); Cj.True(false, "should timeout"); }
catch (System.TimeoutException) { }
""",
                    "Task.Delay(50) beats the 2s work — WhenAny returns the delay; throw TimeoutException.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p9-dropped-task-debug",
            "Debug: The Exception That Vanished",
            """SaveAllAsync fires SaveAsync for each item but never awaits the tasks — one throws and the failure disappears (the harness detects faults left unobserved). Fix: fan out AND observe every completion, rethrowing the first failure after all settle.

```csharp
public sealed class SaveTrap
{
    public SaveTrap(params string[] failingKeys);   // provided
    public Task SaveAsync(string key);              // provided: throws for failingKeys
}
static Task SaveAllAsync(SaveTrap trap, IEnumerable<string> keys);
```""",
            SAVE_TRAP_BOILERPLATE,
            [
                (
                    "first failure surfaces",
                    r"""
var trap = new SaveTrap("b", "d");
try
{
    Solution.SaveAllAsync(trap, new[] { "a", "b", "c", "d" }).GetAwaiter().GetResult();
    Cj.True(false, "should have thrown");
}
catch (System.InvalidOperationException) { }
Cj.True(true, "first fault propagated");
""",
                    "var tasks = keys.Select(trap.SaveAsync).ToList(); await Task.WhenAll(tasks) — WhenAll observes all faults and rethrows the first.",
                ),
                (
                    "clean run stays clean",
                    r"""
var trap = new SaveTrap();
Solution.SaveAllAsync(trap, new[] { "x", "y" }).GetAwaiter().GetResult();
Cj.True(true, "clean run completes");
""",
                    "WhenAll with zero failures completes normally.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p9-sequence-total": vi_challenge(
            "Tuần tự vs Đồng thời: Chứng minh",
            "Hai cách await ba fetch mô phỏng. `SumSequential` await từng cái; `SumConcurrent` khởi tạo cả ba rồi await cùng nhau. Simulator ghi event cho mỗi bước chuyển — chứng minh bằng THỨ TỰ EVENT, không phải đồng hồ:",
            [
                ("concurrent starts overlap", "Khởi tạo mọi FetchAsync vào biến TRƯỚC khi await — Task.WhenAll sau khi start."),
                ("sequential interleaves strictly", "await trong vòng lặp: fetch sau chỉ bắt đầu khi fetch trước xong."),
            ],
        ),
        "csi-p9-unwrap-debug": vi_challenge(
            "Debug: Exception bị bọc",
            "`LoadConfigAsync` lỗi với `InvalidOperationException(\"no config\")`. `GetSetting` — điểm vào đồng bộ — để lộ sai: callers bắt `InvalidOperationException` nhưng không bao giờ thấy. Sửa `GetSetting` để kiểu exception GỐC tới được callers (không phải AggregateException), vẫn đồng bộ.",
            [
                ("real type surfaces", "await task rồi bóc vỏ: bắt AggregateException và ném ex.InnerException — chặn bằng .Result không tự bóc."),
            ],
        ),
        "csi-p9-cancel-token": vi_challenge(
            "Hủy hợp tác",
            "Hiện thực worker tôn trọng hủy: xử lý từng phần tử, kiểm tra token TRƯỚC mỗi phần tử, trả về số phần tử đã hoàn thành. Khi bị hủy giữa chừng, ném OperationCanceledException kèm token.",
            [
                ("completes when not cancelled", "Duyệt items, kiểm tra ct.ThrowIfCancellationRequested() trước, await work(item)."),
                ("stops promptly on cancel", "ThrowIfCancellationRequested TRƯỚC mỗi work — phần tử 3 không bao giờ chạy."),
            ],
        ),
        "csi-p9-timeout": vi_challenge(
            "Time-box thao tác hay lỗi",
            "Bọc một task tùy ý với timeout: trả kết quả nếu xong đúng hạn, ngược lại ném TimeoutException. Dùng Task.WhenAny + Task.Delay (hoặc Task.WaitAsync — .NET 8+).",
            [
                ("fast path wins", "Task.WhenAny(work, Task.Delay(timeoutMs)); nếu winner != work ném TimeoutException, else await work."),
                ("slow path times out", "Task.Delay(50) thắng task 2s — WhenAny trả delay; ném TimeoutException."),
            ],
        ),
        "csi-p9-dropped-task-debug": vi_challenge(
            "Debug: Exception biến mất",
            "SaveAllAsync bắn SaveAsync cho từng phần tử nhưng không await — một cái ném lỗi và thất bại biến mất (harness phát hiện fault không được quan sát). Sửa: fan-out VÀ quan sát mọi completion, ném lại lỗi đầu tiên sau khi tất cả kết thúc.",
            [
                ("first failure surfaces", "var tasks = keys.Select(trap.SaveAsync).ToList(); await Task.WhenAll(tasks) — WhenAll quan sát mọi fault và ném lại lỗi đầu."),
                ("clean run stays clean", "WhenAll không lỗi hoàn thành bình thường."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p9-sequence-total",
            'public class Solution\n{\n    public sealed class EventIo\n    {\n        public System.Collections.Generic.List<string> Log { get; } = new();\n\n        public async System.Threading.Tasks.Task<int> FetchAsync(int step)\n        {\n            Log.Add("start:" + step);\n            await System.Threading.Tasks.Task.Yield();\n            Log.Add("done:" + step);\n            return step + 1;\n        }\n    }\n\n    public static async System.Threading.Tasks.Task<int> SumSequential(EventIo io)\n    {\n        int total = 0;\n        for (int step = 0; step < 3; step++)\n            total += await io.FetchAsync(step);\n        return total;\n    }\n\n    public static async System.Threading.Tasks.Task<int> SumConcurrent(EventIo io)\n    {\n        var t0 = io.FetchAsync(0);\n        var t1 = io.FetchAsync(1);\n        var t2 = io.FetchAsync(2);\n        int[] all = await System.Threading.Tasks.Task.WhenAll(t0, t1, t2);\n        return all[0] + all[1] + all[2];\n    }\n}\n',
            'public class Solution\n{\n    public sealed class EventIo\n    {\n        public System.Collections.Generic.List<string> Log { get; } = new();\n\n        public async System.Threading.Tasks.Task<int> FetchAsync(int step)\n        {\n            Log.Add("start:" + step);\n            await System.Threading.Tasks.Task.Yield();\n            Log.Add("done:" + step);\n            return step + 1;\n        }\n    }\n\n    public static async System.Threading.Tasks.Task<int> SumSequential(EventIo io)\n    {\n        int total = 0;\n        for (int step = 0; step < 3; step++)\n            total += await io.FetchAsync(step);\n        return total;\n    }\n\n    public static async System.Threading.Tasks.Task<int> SumConcurrent(EventIo io)\n    {\n        // near-miss: awaits the first fetch BEFORE starting the next two —\n        // the "concurrent" method is actually sequential: start:0,done:0,\n        // start:1 — the overlap test fails\n        int a = await io.FetchAsync(0);\n        var t1 = io.FetchAsync(1);\n        var t2 = io.FetchAsync(2);\n        int[] rest = await System.Threading.Tasks.Task.WhenAll(t1, t2);\n        return a + rest[0] + rest[1];\n    }\n}\n',
        ),
        (
            "csi-p9-unwrap-debug",
            'public class Solution\n{\n    public static System.Threading.Tasks.Task<string> LoadConfigAsync()\n    {\n        return System.Threading.Tasks.Task.FromException<string>(new System.InvalidOperationException("no config"));\n    }\n\n    public static string GetSetting()\n    {\n        // fixed: block AND unwrap — AggregateException\'s InnerException keeps\n        // the caller-facing contract\n        try\n        {\n            return LoadConfigAsync().GetAwaiter().GetResult();\n        }\n        catch (System.AggregateException ag)\n        {\n            System.Runtime.ExceptionServices.ExceptionDispatchInfo.Capture(ag.GetBaseException()).Throw();\n            throw;   // unreachable\n        }\n    }\n}\n',
            'public class Solution\n{\n    public static System.Threading.Tasks.Task<string> LoadConfigAsync()\n    {\n        return System.Threading.Tasks.Task.FromException<string>(new System.InvalidOperationException("no config"));\n    }\n\n    public static string GetSetting()\n    {\n        // near-miss: blocking surfaces the WRAPPED exception — callers\n        // catching InvalidOperationException never match AggregateException\n        return LoadConfigAsync().Result;\n    }\n}\n',
        ),
        (
            "csi-p9-cancel-token",
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task<int> ProcessAsync(\n        System.Collections.Generic.IEnumerable<int> items,\n        Func<int, System.Threading.Tasks.Task> work,\n        System.Threading.CancellationToken ct)\n    {\n        int done = 0;\n        foreach (int item in items)\n        {\n            ct.ThrowIfCancellationRequested();\n            await work(item);\n            done++;\n        }\n        return done;\n    }\n}\n',
            'public class Solution\n{\n    // near-miss: the token is accepted but NEVER checked — a pre-cancelled\n    // token still processes every item and returns normally instead of\n    // throwing OperationCanceledException\n    public static async System.Threading.Tasks.Task<int> ProcessAsync(\n        System.Collections.Generic.IEnumerable<int> items,\n        Func<int, System.Threading.Tasks.Task> work,\n        System.Threading.CancellationToken ct)\n    {\n        int done = 0;\n        foreach (int item in items)\n        {\n            await work(item);\n            done++;\n        }\n        return done;\n    }\n}\n',
        ),
        (
            "csi-p9-timeout",
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task<string> WithTimeout(\n        System.Threading.Tasks.Task<string> work, int timeoutMs)\n    {\n        var done = await System.Threading.Tasks.Task.WhenAny(\n            work, System.Threading.Tasks.Task.Delay(timeoutMs));\n        if (done != work)\n            throw new System.TimeoutException("operation timed out");\n        return await work;\n    }\n}\n',
            'public class Solution\n{\n    // near-miss: awaits the work FIRST — a hung task never returns and the\n    // timeout path is unreachable; the slow-path test waits forever instead\n    // of throwing TimeoutException\n    public static async System.Threading.Tasks.Task<string> WithTimeout(\n        System.Threading.Tasks.Task<string> work, int timeoutMs)\n    {\n        string result = await work;\n        _ = System.Threading.Tasks.Task.Delay(timeoutMs);\n        return result;\n    }\n}\n',
        ),
        (
            "csi-p9-dropped-task-debug",
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task SaveAllAsync(SaveTrap trap, System.Collections.Generic.IEnumerable<string> keys)\n    {\n        var tasks = new System.Collections.Generic.List<System.Threading.Tasks.Task>();\n        foreach (string key in keys)\n            tasks.Add(trap.SaveAsync(key));\n        await System.Threading.Tasks.Task.WhenAll(tasks);\n    }\n}\n',
            'public class Solution\n{\n    // near-miss: fire-and-forget — SaveAsync tasks are started but never\n    // awaited, so faults are unobserved (SaveTrap records the escape) and\n    // SaveAllAsync "succeeds" despite failing saves\n    public static System.Threading.Tasks.Task SaveAllAsync(SaveTrap trap, System.Collections.Generic.IEnumerable<string> keys)\n    {\n        foreach (string key in keys)\n            _ = trap.SaveAsync(key);\n        return System.Threading.Tasks.Task.CompletedTask;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m9",
    "Checkpoint — The Parallel Fetcher",
    "Combine fan-out, per-call timeouts, cooperative cancellation, and honest failure aggregation into one resilient pipeline.",
    25,
    r"""
## The gate (mini-build)

A resilient concurrent fetch pipeline over `CjFlaky.FetchAsync(key, delayMs,
ct)` (provided in your starter code; `slow*` keys hang for 5 s):

1. `FetchAll(IEnumerable<string> keys, TimeSpan perCall, CancellationToken ct)`
   → starts EVERY simulated fetch at once (fan-out).
2. Each call is time-boxed with `perCall` — a hung backend is ABANDONED,
   not waited out. Outcomes: `"key=ok"` or `"key=timeout"`.
3. Caller cancellation aborts immediately with
   `OperationCanceledException` even if fetches are still pending.
4. `Report(results)` formats results sorted by key: `"a=ok|b=timeout"`.

Tests observe timing generously (< 1 s for a 5 s hang) — the discipline is
structural: start-all-then-await, WaitAsync per call, token through.
""",
    "Checkpoint — Bộ fetch song song",
    "Kết hợp fan-out, timeout từng lời gọi, hủy hợp tác, và tổng hợp thất bại trung thực thành một pipeline bền bỉ.",
    r"""
## Cổng kiểm tra (mini-build)

Pipeline fetch đồng thời bền bỉ trên `CjFlaky.FetchAsync(key, delayMs, ct)`
(có sẵn trong code khởi đầu; key `slow*` treo 5 s):

1. `FetchAll(IEnumerable<string> keys, TimeSpan perCall, CancellationToken ct)`
   → khởi tạo MỌI fetch mô phỏng cùng lúc (fan-out).
2. Mỗi lời gọi được time-box bằng `perCall` — backend treo bị BỎ, không chờ.
   Kết quả: `"key=ok"` hoặc `"key=timeout"`.
3. Caller hủy thì dừng ngay với `OperationCanceledException` dù fetch vẫn
   đang treo.
4. `Report(results)` định dạng kết quả xếp theo key: `"a=ok|b=timeout"`.

Test đo thời gian hào phóng (< 1 s cho treo 5 s) — cái được chấm là cấu
trúc: start-all-then-await, WaitAsync từng lời gọi, token xuyên suốt.
""",
    challenge(
        "csi-checkpoint-m9-task",
        "Checkpoint: Resilient Fetch Pipeline",
        """Implement the pipeline described in the checkpoint:

```csharp
static Task<List<string>> FetchAll(IEnumerable<string> keys, TimeSpan perCall, CancellationToken ct);
static string Report(List<string> results);   // "a=ok|b=timeout" sorted by key
```""",
        FLAKY_BOILERPLATE,
        [
            (
                "fan-out with per-call timeout",
                r"""
var sw = System.Diagnostics.Stopwatch.StartNew();
var results = Solution.FetchAll(new[] { "fast1", "fast2", "slow" }, System.TimeSpan.FromMilliseconds(150), System.Threading.CancellationToken.None).GetAwaiter().GetResult();
sw.Stop();
Cj.True(sw.ElapsedMilliseconds < 1000, "slow call abandoned, not waited out (5s hang skipped)");
Cj.True(results.Contains("fast1=ok") && results.Contains("fast2=ok"), "fast calls ok");
Cj.True(results.Contains("slow=timeout"), "slow call marked timeout");
""",
                    "Start all CjFlaky.FetchAsync tasks; await each with task.WaitAsync(perCall, ct) catching TimeoutException -> record \"key=timeout\".",
                ),
                (
                    "caller cancel aborts",
                    r"""
var cts = new System.Threading.CancellationTokenSource();
var t = Solution.FetchAll(new[] { "k1", "k2" }, System.TimeSpan.FromSeconds(10), cts.Token);
cts.Cancel();
try { t.GetAwaiter().GetResult(); Cj.True(false, "should cancel"); }
catch (System.OperationCanceledException) { }
""",
                    "ct.ThrowIfCancellationRequested() before the fan-out AND pass ct to each WaitAsync — cancel lands promptly.",
                ),
                (
                    "report sorted by key",
                    r"""
var results = new System.Collections.Generic.List<string> { "b=timeout", "a=ok", "c=ok" };
Cj.Eq(Solution.Report(results), "a=ok|b=timeout|c=ok", "sorted join");
""",
                    "results.OrderBy(r => key part).Join with '|'.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Pipeline fetch bền bỉ",
            "Hiện thực pipeline: fan-out mọi fetch, timeout từng lời gọi (abandon), ghi \"key=ok\"/\"key=timeout\", hủy caller dừng ngay với OperationCanceledException, Report xếp theo key.",
            [
                ("fan-out with per-call timeout", "Khởi tạo mọi CjFlaky.FetchAsync; await từng cái với task.WaitAsync(perCall, ct), bắt TimeoutException -> \"key=timeout\"."),
                ("caller cancel aborts", "ct.ThrowIfCancellationRequested() trước fan-out VÀ truyền ct cho mỗi WaitAsync — hủy đến ngay."),
                ("report sorted by key", "results.OrderBy(phần key).Join bằng '|'."),
            ],
        ),
        solution='public class Solution\n{\n    public static async System.Threading.Tasks.Task<System.Collections.Generic.List<string>> FetchAll(\n        System.Collections.Generic.IEnumerable<string> keys,\n        System.TimeSpan perCall,\n        System.Threading.CancellationToken ct)\n    {\n        ct.ThrowIfCancellationRequested();\n        var tasks = new System.Collections.Generic.Dictionary<string, System.Threading.Tasks.Task<string>>();\n        foreach (string key in keys)\n            tasks[key] = CjFlaky.FetchAsync(key, 30, ct);\n\n        var results = new System.Collections.Generic.List<string>();\n        foreach (var pair in tasks)\n        {\n            try\n            {\n                await pair.Value.WaitAsync(perCall, ct);\n                results.Add(pair.Key + "=ok");\n            }\n            catch (System.TimeoutException)\n            {\n                results.Add(pair.Key + "=timeout");\n            }\n        }\n        return results;\n    }\n\n    public static string Report(System.Collections.Generic.List<string> results)\n    {\n        return string.Join("|", results\n            .OrderBy(r => r.Substring(0, r.IndexOf(\'=\')))\n            .ToList());\n    }\n}\n',
        wrong='public class Solution\n{\n    // near-miss: awaits each fetch SEQUENTIALLY — no fan-out, and the slow\n    // fetch waits its full 5 s inside the per-call window, so the <1000 ms\n    // timing test fails\n    public static async System.Threading.Tasks.Task<System.Collections.Generic.List<string>> FetchAll(\n        System.Collections.Generic.IEnumerable<string> keys,\n        System.TimeSpan perCall,\n        System.Threading.CancellationToken ct)\n    {\n        var results = new System.Collections.Generic.List<string>();\n        foreach (string key in keys)\n        {\n            try\n            {\n                await CjFlaky.FetchAsync(key, 30, ct);\n                results.Add(key + "=ok");\n            }\n            catch (System.TimeoutException)\n            {\n                results.Add(key + "=timeout");\n            }\n        }\n        return results;\n    }\n\n    public static string Report(System.Collections.Generic.List<string> results)\n    {\n        return string.Join("|", results);\n    }\n}\n',
    )
print("module 9 authored")
