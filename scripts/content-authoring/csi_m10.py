#!/usr/bin/env python3
"""C# — Intermediate — Module 10: csi-concurrency.

Concurrency fundamentals: threads vs parallelism, races, lock/Monitor,
Interlocked, ConcurrentDictionary, and deadlock avoidance by lock ordering.

Determinism strategy (CPU-limited sandbox): the boilerplate provides
CjConcurrency.Pause() — a required "simulated work" call learners place
between read and write. Non-atomic read-modify-write then loses updates
reliably; Interlocked/lock versions stay exact. Deadlock tests force the
interleaving the same way and use Thread.Join(timeout) so the harness never
hangs.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-concurrency"

CJCONC_BOILERPLATE = CS_PRELUDE + (
    "using System.Threading;\n"
    "\n"
    "// Provided infrastructure — do not modify.\n"
    "public static class CjConcurrency\n"
    "{\n"
    "    // Simulated work: every long-enough operation calls this so the\n"
    "    // scheduler can interleave threads. Tests rely on it being called\n"
    "    // exactly where the task says.\n"
    "    public static void Pause()\n"
    "    {\n"
    "        Thread.Sleep(5);\n"
    "    }\n"
    "}\n"
)

write_module(
    M,
    "Concurrency Fundamentals",
    "Threads, races, locks, and atomic operations — the vocabulary of code that does several things at once, without the data corruption.",
    "Nền tảng Đồng thời",
    "Thread, race condition, lock và phép toán nguyên tử — từ vựng của code làm nhiều việc cùng lúc, không xào nucson dữ liệu.",
    ["threads-and-locks", "synchronization-patterns", "csi-checkpoint-m10"],
    ["csi-p10-concurrency"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "threads-and-locks",
    "Threads, Races, and the lock Keyword",
    "What a race condition is, why ++ isn't atomic, and how lock and Interlocked make shared state safe.",
    18,
    r"""
## Concurrency vs parallelism, threads vs pool

CONCURRENCY is about structure (dealing with many things at once);
PARALLELISM is about execution (doing many things literally simultaneously).
A `Thread` is an OS execution lane; the `ThreadPool` reuses a pool of them so
you don't pay thread-creation costs per work item — `Task.Run` queues onto
the pool (Module 9's tasks ran there).

## The race: read-modify-write is three steps

`_count++` compiles to read, add, write. Two threads interleaving can both
read 5 and both write 6 — one increment vanishes:

```csharp
int v = _count;      // thread A reads 5
// ...thread B reads 5, writes 6...
_count = v + 1;      // thread A writes 6 — B's increment is gone
```

Races are intermittent and machine-dependent — the nastiest bug class. Any
shared mutable state touched by two threads without synchronization is a
race by definition, even if tests never catch it.

## lock: mutual exclusion

```csharp
private readonly object _gate = new();
lock (_gate)
{
    _count = _count + 1;   // only one thread inside at a time
}
```

`lock` is `Monitor.Enter/Exit` sugar. Rules: lock on a PRIVATE readonly
object (locking `this` or a Type lets strangers block you); keep the
critical section SMALL; every thread that touches the state must use the
SAME gate — one unsynchronized accessor reopens the race.

## Interlocked: atomic micro-operations

For single-variable updates, `Interlocked.Increment/Decrement/Add/Exchange/
CompareExchange` make read-modify-write atomic without a lock:

```csharp
Interlocked.Increment(ref _count);   // exact under any contention
```

Prefer Interlocked for counters; `lock` for multi-step invariants.

## Visibility (concept)

Each thread may cache field values; without synchronization a thread can see
stale data. `lock` and Interlocked both imply memory barriers — writes
become visible on exit. Don't sprinkle `volatile`; synchronize properly and
visibility follows.

## Check your understanding

- Why can `++` lose updates? (Read-modify-write interleaves between threads.)
- What's wrong with `lock(this)`? (External code can lock the same object — deadlock/blocking risk.)
""",
    "Thread, Race Condition, và Từ khóa lock",
    "Race condition là gì, vì sao ++ không nguyên tử, và lock cùng Interlocked làm state chia sẻ an toàn thế nào.",
    r"""
## Đồng thời vs song song, thread vs pool

ĐỒNG THỜI là về cấu trúc (xử lý nhiều việc cùng lúc); SONG SONG là về thực
thi (làm nhiều việc thật sự cùng một lúc). `Thread` là một làn thực thi của
OS; `ThreadPool` tái sử dụng một bể thread để không trả phí tạo thread cho
từng work item — `Task.Run` xếp hàng vào bể (task ở Module 9 chạy ở đó).

## Race: read-modify-write là ba bước

`_count++` biên dịch thành đọc, cộng, ghi. Hai thread chen nhau có thể cùng
đọc 5 và cùng ghi 6 — một lần tăng biến mất:

```csharp
int v = _count;      // thread A đọc 5
// ...thread B đọc 5, ghi 6...
_count = v + 1;      // thread A ghi 6 — lần tăng của B mất
```

Race không đều và phụ thuộc máy — lớp bug khó chịu nhất. Bất kỳ state chia
sẻ mutable nào bị hai thread chạm mà không đồng bộ đều là race theo định
nghĩa, kể cả khi test chưa bắt được.

## lock: loại trừ lẫn nhau

```csharp
private readonly object _gate = new();
lock (_gate)
{
    _count = _count + 1;   // mỗi lúc chỉ một thread ở trong
}
```

`lock` là đường của `Monitor.Enter/Exit`. Nguyên tắc: lock trên object
PRIVATE readonly (lock `this` hoặc Type cho phép người lạ chặn bạn); giữ
vùng tối giản; mọi thread chạm state phải dùng CÙNG gate — một accessor
không đồng bộ là mở lại race.

## Interlocked: phép toán nguyên tử nhỏ

Với cập nhật một biến, `Interlocked.Increment/Decrement/Add/Exchange/
CompareExchange` làm read-modify-write nguyên tử không cần lock:

```csharp
Interlocked.Increment(ref _count);   // chính xác dưới bất kỳ tranh chấp nào
```

Ưu tiên Interlocked cho bộ đếm; `lock` cho bất biến nhiều bước.

## Tầm nhìn bộ nhớ (khái niệm)

Mỗi thread có thể cache giá trị field; không đồng bộ thì một thread có thể
thấy dữ liệu cũ. `lock` và Interlocked đều ngầm memory barrier — ghi trở
nên hiển thị khi thoát. Đừng rắc `volatile`; đồng bộ đúng way thì tầm nhìn
theo đúng.

## Kiểm tra hiểu biết

- Vì sao `++` có thể mất cập nhật? (Read-modify-write chen nhau giữa các thread.)
- `lock(this)` sai ở đâu? (Code ngoài có thể lock cùng object — nguy cơ chặn/deadlock.)
""",
    r"""
## Đồng thời vs song song, thread vs pool

ĐỒNG THỜI là về cấu trúc (xử lý nhiều việc cùng lúc); SONG SONG là về thực
thi (làm nhiều việc thật sự cùng một lúc). `Thread` là một làn thực thi của
OS; `ThreadPool` tái sử dụng một bể thread để không trả phí tạo thread cho
từng work item — `Task.Run` xếp hàng vào bể (task ở Module 9 chạy ở đó).

## Race: read-modify-write là ba bước

`_count++` biên dịch thành đọc, cộng, ghi. Hai thread chen nhau có thể cùng
đọc 5 và cùng ghi 6 — một lần tăng biến mất:

```csharp
int v = _count;      // thread A đọc 5
// ...thread B đọc 5, ghi 6...
_count = v + 1;      // thread A ghi 6 — lần tăng của B mất
```

Race không đều và phụ thuộc máy — lớp bug khó chịu nhất. Bất kỳ state chia
sẻ mutable nào bị hai thread chạm mà không đồng bộ đều là race theo định
nghĩa, kể cả khi test chưa bắt được.

## lock: loại trừ lẫn nhau

```csharp
private readonly object _gate = new();
lock (_gate)
{
    _count = _count + 1;   // mỗi lúc chỉ một thread ở trong
}
```

`lock` là đường của `Monitor.Enter/Exit`. Nguyên tắc: lock trên object
PRIVATE readonly (lock `this` hoặc Type cho phép người lạ chặn bạn); giữ
vùng tối giản; mọi thread chạm state phải dùng CÙNG gate — một accessor
không đồng bộ là mở lại race.

## Interlocked: phép toán nguyên tử nhỏ

Với cập nhật một biến, `Interlocked.Increment/Decrement/Add/Exchange/
CompareExchange` làm read-modify-write nguyên tử không cần lock:

```csharp
Interlocked.Increment(ref _count);   // chính xác dưới bất kỳ tranh chấp nào
```

Ưu tiên Interlocked cho bộ đếm; `lock` cho bất biến nhiều bước.

## Tầm nhìn bộ nhớ (khái niệm)

Mỗi thread có thể cache giá trị field; không đồng bộ thì một thread có thể
thấy dữ liệu cũ. `lock` và Interlocked đều ngầm memory barrier — ghi trở
nên hiển thị khi thoát. Đừng rắc `volatile`; đồng bộ đúng way thì tầm nhìn
theo đúng.

## Kiểm tra hiểu biết

- Vì sao `++` có thể mất cập nhật? (Read-modify-write chen nhau giữa các thread.)
- `lock(this)` sai ở đâu? (Code ngoài có thể lock cùng object — nguy cơ chặn/deadlock.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "synchronization-patterns",
    "Semaphores, Concurrent Collections, and Deadlocks",
    "SemaphoreSlim for limits, ConcurrentDictionary for shared maps, and why lock ordering kills deadlocks.",
    17,
    r"""
## SemaphoreSlim: limiting access

A semaphore counts DOWN slots. `Wait()` takes one, `Release()` returns it —
with initial count 0 it's a signaling gate; with `new SemaphoreSlim(3)` it
caps concurrency at 3:

```csharp
private readonly SemaphoreSlim _slots = new(3);
await _slots.WaitAsync();
try { await UseResourceAsync(); }
finally { _slots.Release(); }
```

Always release in `finally`. (Module 9: `WaitAsync` is the async flavor;
sync `Wait()` blocks a thread.)

## Concurrent collections: don't lock the map yourself

`ConcurrentDictionary<TKey, TValue>` is thread-safe per operation, and its
special methods are ATOMIC — the whole point:

```csharp
int now = _counts.AddOrUpdate(path, 1, (key, old) => old + 1);
```

The classic mistake is check-then-act on top of it
(`if (!dict.ContainsKey(k)) dict[k] = v;` — two operations, a race between
them). Also `ConcurrentQueue<T>`, `ConcurrentStack<T>`, `ConcurrentBag<T>`
for producer/consumer shapes; `BlockingCollection<T>` wraps them with
bounding and blocking. Read a `ConcurrentDictionary` while another thread
writes is safe; multi-step invariants across entries still need your own
lock.

## Deadlock: the circular wait

Two threads each hold a lock the other needs; neither proceeds:

```
A: lock(a) ... lock(b)     B: lock(b) ... lock(a)
```

The standard cure is lock ORDERING: acquire multiple locks in a global
consistent order (e.g., by Id) — a cycle becomes impossible. Other rules:
never call unknown code while holding a lock; keep lock scope tight; prefer
the smallest number of locks that protect the invariant.

## Interlocked + lock in one design

Counters → Interlocked. Multi-field invariants (move money between
accounts, pop one work item) → lock around the WHOLE check-and-act.

## Check your understanding

- Is `dict[k] = v` on a ConcurrentDictionary enough for "add if missing"? (No — use GetOrAdd/AddOrUpdate; indexer+check is two operations.)
- How does lock ordering prevent deadlock? (No cycle can form if everyone acquires in the same global order.)
""",
    "Semaphore, Concurrent Collection, và Deadlock",
    "SemaphoreSlim giới hạn truy cập, ConcurrentDictionary cho map chia sẻ, và vì sao thứ tự lock diệt deadlock.",
    r"""
## SemaphoreSlim: giới hạn truy cập

Semaphore đếm NGƯỢC số slot. `Wait()` lấy một, `Release()` trả lại — khởi
tạo 0 thì là cổng tín hiệu; `new SemaphoreSlim(3)` giới hạn đồng thời tối
đa 3:

```csharp
private readonly SemaphoreSlim _slots = new(3);
await _slots.WaitAsync();
try { await UseResourceAsync(); }
finally { _slots.Release(); }
```

Luôn release trong `finally`. (Module 9: `WaitAsync` là bản async; `Wait()`
đồng bộ chặn thread.)

## Concurrent collection: đừng tự lock cái map

`ConcurrentDictionary<TKey, TValue>` an toàn luồng theo từng thao tác, và
các phương thức đặc biệt của nó là NGUYÊN TỬ — đó mới là điểm nhấn:

```csharp
int now = _counts.AddOrUpdate(path, 1, (key, old) => old + 1);
```

Lỗi kinh điển là check-then-act đặt lên trên nó
(`if (!dict.ContainsKey(k)) dict[k] = v;` — hai thao tác, một race nằm giữa).
Còn `ConcurrentQueue<T>`, `ConcurrentStack<T>`, `ConcurrentBag<T>` cho các
shape producer/consumer; `BlockingCollection<T>` bọc chúng với giới hạn và
chặn. Đọc `ConcurrentDictionary` khi thread khác đang ghi là an toàn; bất
biến nhiều bước qua nhiều entry vẫn cần lock của bạn.

## Deadlock: vòng chờ tròn

Hai thread mỗi bên giữ lock mà bên kia cần; không bên nào tiến được:

```
A: lock(a) ... lock(b)     B: lock(b) ... lock(a)
```

Chữa chuẩn là THỨ TỰ LOCK: lấy nhiều lock theo một thứ tự toàn cục nhất quán
(ví dụ theo Id) — không thể tạo thành chu kỳ. Nguyên tắc khác: không gọi
code lạ khi đang giữ lock; giữ vùng lock gọn; ưu tiên số lock tối thiểu bảo
vệ bất biến.

## Interlocked + lock trong một thiết kế

Bộ đếm → Interlocked. Bất biến nhiều trường (chuyển tiền giữa tài khoản,
lấy một work item) → lock quanh TOÀN BỘ check-and-act.

## Kiểm tra hiểu biết

- `dict[k] = v` trên ConcurrentDictionary đủ cho "thêm nếu chưa có"? (Không — dùng GetOrAdd/AddOrUpdate; check + indexer là hai thao tác.)
- Thứ tự lock phòng deadlock thế nào? (Không thể có chu kỳ nếu mọi người lấy lock theo cùng thứ tự toàn cục.)
""",
    r"""
## SemaphoreSlim: giới hạn truy cập

Semaphore đếm NGƯỢC số slot. `Wait()` lấy một, `Release()` trả lại — khởi
tạo 0 thì là cổng tín hiệu; `new SemaphoreSlim(3)` giới hạn đồng thời tối
đa 3:

```csharp
private readonly SemaphoreSlim _slots = new(3);
await _slots.WaitAsync();
try { await UseResourceAsync(); }
finally { _slots.Release(); }
```

Luôn release trong `finally`. (Module 9: `WaitAsync` là bản async; `Wait()`
đồng bộ chặn thread.)

## Concurrent collection: đừng tự lock cái map

`ConcurrentDictionary<TKey, TValue>` an toàn luồng theo từng thao tác, và
các phương thức đặc biệt của nó là NGUYÊN TỬ — đó mới là điểm nhấn:

```csharp
int now = _counts.AddOrUpdate(path, 1, (key, old) => old + 1);
```

Lỗi kinh điển là check-then-act đặt lên trên nó
(`if (!dict.ContainsKey(k)) dict[k] = v;` — hai thao tác, một race nằm giữa).
Còn `ConcurrentQueue<T>`, `ConcurrentStack<T>`, `ConcurrentBag<T>` cho các
shape producer/consumer; `BlockingCollection<T>` bọc chúng với giới hạn và
chặn. Đọc `ConcurrentDictionary` khi thread khác đang ghi là an toàn; bất
biến nhiều bước qua nhiều entry vẫn cần lock của bạn.

## Deadlock: vòng chờ tròn

Hai thread mỗi bên giữ lock mà bên kia cần; không bên nào tiến được:

```
A: lock(a) ... lock(b)     B: lock(b) ... lock(a)
```

Chữa chuẩn là THỨ TỰ LOCK: lấy nhiều lock theo một thứ tự toàn cục nhất quán
(ví dụ theo Id) — không thể tạo thành chu kỳ. Nguyên tắc khác: không gọi
code lạ khi đang giữ lock; giữ vùng lock gọn; ưu tiên số lock tối thiểu bảo
vệ bất biến.

## Interlocked + lock trong một thiết kế

Bộ đếm → Interlocked. Bất biến nhiều trường (chuyển tiền giữa tài khoản,
lấy một work item) → lock quanh TOÀN BỘ check-and-act.

## Kiểm tra hiểu biết

- `dict[k] = v` trên ConcurrentDictionary đủ cho "thêm nếu chưa có"? (Không — dùng GetOrAdd/AddOrUpdate; check + indexer là hai thao tác.)
- Thứ tự lock phòng deadlock thế nào? (Không thể có chu kỳ nếu mọi người lấy lock theo cùng thứ tự toàn cục.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p10-concurrency",
    "Concurrency Practice: Counters, Limits, Deadlocks",
    "Build thread-safe state, cap resource use, and defuse a lock-ordering deadlock.",
    "Luyện Đồng thời: Bộ đếm, Giới hạn, Deadlock",
    "Dựng state an toàn luồng, giới hạn tài nguyên, và tháo ngòi deadlock do thứ tự lock.",
    "synchronization-patterns",
    32,
    "intermediate",
    [
        challenge(
            "csi-p10-atomic-counter",
            "The Counter That Loses Nothing",
            """Implement a Counter that stays EXACT under concurrent callers. Increment must call CjConcurrency.Pause() once (simulated work) — where you put it relative to the update decides everything. Also implement Drain() returning the count and resetting to 0 atomically.

```csharp
public sealed class Counter
{
    public void Increment();   // calls CjConcurrency.Pause(); exact under contention
    public int Value { get; }  // completed increments so far
    public int Drain();        // returns count, resets to 0
}
```""",
            CJCONC_BOILERPLATE,
            [
                (
                    "single-threaded baseline",
                    r"""
var c = new Solution.Counter();
c.Increment(); c.Increment(); c.Increment();
Cj.Eq(c.Value, 3, "three increments");
Cj.Eq(c.Drain(), 3, "drain returns count");
Cj.Eq(c.Value, 0, "drain resets");
""",
                    "Interlocked.Increment(ref _count) for Increment; Drain via Interlocked.Exchange(ref _count, 0).",
                ),
                (
                    "exact under 4 concurrent workers",
                    r"""
var c = new Solution.Counter();
var threads = new System.Collections.Generic.List<System.Threading.Thread>();
for (int w = 0; w < 4; w++)
{
    var t = new System.Threading.Thread(() =>
    {
        for (int i = 0; i < 500; i++) c.Increment();
    });
    t.IsBackground = true;
    threads.Add(t);
    t.Start();
}
foreach (var t in threads) t.Join(15000);
Cj.Eq(c.Value, 2000, "no update lost, none double-counted");
""",
                    "With Pause() between a plain read and write, other threads read the same stale value — Interlocked keeps read-modify-write atomic.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p10-bounded-channel",
            "The Bounded Channel",
            """Implement a FIFO channel with a capacity: TryProduce returns false when full, TryConsume returns null when empty, Count reports items waiting.

```csharp
public sealed class BoundedChannel
{
    public BoundedChannel(int capacity);
    public bool TryProduce(string item);   // false when at capacity
    public string? TryConsume();           // oldest item, or null when empty
    public int Count { get; }
}
```""",
            CS_PRELUDE,
            [
                (
                    "capacity enforced",
                    r"""
var ch = new Solution.BoundedChannel(3);
Cj.Eq(ch.TryProduce("a"), true, "1st fits");
Cj.Eq(ch.TryProduce("b"), true, "2nd fits");
Cj.Eq(ch.TryProduce("c"), true, "3rd fits");
Cj.Eq(ch.TryProduce("d"), false, "4th rejected at capacity");
Cj.Eq(ch.Count, 3, "count unchanged after rejected produce");
""",
                    "Queue<string> + count check before enqueue (lock-protected if you like — behavior is what's graded).",
                ),
                (
                    "FIFO drain",
                    r"""
var ch = new Solution.BoundedChannel(2);
ch.TryProduce("first"); ch.TryProduce("second");
Cj.Eq(ch.TryConsume(), "first", "oldest first");
Cj.Eq(ch.TryConsume(), "second", "then next");
Cj.Eq(ch.TryConsume() is null, true, "null when empty");
Cj.Eq(ch.TryProduce("after"), true, "capacity freed by consumes");
""",
                    "Dequeue when Count > 0; freed capacity allows new produces.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p10-deadlock-debug",
            "Debug: The Transfer That Freezes",
            """Transfer must call CjConcurrency.Pause() AFTER acquiring its first lock and BEFORE the second (a simulated FX check). The current implementation deadlocks when two transfers run in opposite directions. Fix it so both transfers always complete — without removing the Pause.

```csharp
public sealed class Account { public int Id; public int Balance; }
static void Transfer(Account from, Account to, int amount);
```""",
            CJCONC_BOILERPLATE,
            [
                (
                    "opposite transfers both complete",
                    r"""
var a = new Solution.Account { Id = 1, Balance = 100 };
var b = new Solution.Account { Id = 2, Balance = 50 };
var t1 = new System.Threading.Thread(() => Solution.Transfer(a, b, 30));
var t2 = new System.Threading.Thread(() => Solution.Transfer(b, a, 20));
t1.IsBackground = true; t2.IsBackground = true;
t1.Start(); t2.Start();
var done = t1.Join(3000) && t2.Join(3000);
Cj.True(done, "no deadlock — both transfers finish");
Cj.Eq(a.Balance, 90, "a: 100 - 30 + 20");
Cj.Eq(b.Balance, 60, "b: 50 + 30 - 20");
""",
                    "Acquire both locks in a GLOBAL order (e.g., lower Id first) — a cycle can't form; keep Pause() between first and second acquisition.",
                ),
                (
                    "same-direction transfer still works",
                    r"""
var a = new Solution.Account { Id = 1, Balance = 100 };
var b = new Solution.Account { Id = 2, Balance = 50 };
Solution.Transfer(a, b, 40);
Cj.Eq(a.Balance, 60, "from debited");
Cj.Eq(b.Balance, 90, "to credited");
""",
                    "Ordered locking handles the normal case identically.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p10-visitor-stats",
            "Atomic Visitor Counts",
            """Implement VisitorStats on a ConcurrentDictionary: RecordVisit returns the count AFTER this visit (first visit returns 1), Visits returns the current count.

```csharp
public sealed class VisitorStats
{
    public int RecordVisit(string path);   // atomic; returns post-visit count
    public int Visits(string path);        // 0 for unknown paths
}
```""",
            CS_PRELUDE,
            [
                (
                    "post-visit counts",
                    r"""
var s = new Solution.VisitorStats();
Cj.Eq(s.RecordVisit("home"), 1, "first visit -> 1");
Cj.Eq(s.RecordVisit("home"), 2, "second visit -> 2");
Cj.Eq(s.RecordVisit("docs"), 1, "independent paths");
Cj.Eq(s.Visits("home"), 2, "Visits reads current");
Cj.Eq(s.Visits("nope"), 0, "unknown path -> 0");
""",
                    "_counts.AddOrUpdate(path, 1, (key, old) => old + 1) returns the NEW value — return it.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p10-atomic-counter": vi_challenge(
            "Bộ đếm không mất góp",
            "Hiện thực Counter CHÍNH XÁC dưới tranh chấp đồng thời. Increment phải gọi CjConcurrency.Pause() một lần (công việc mô phỏng) — vị trí của nó so với phép cập nhật quyết định tất cả. Thêm Drain() trả số đếm và reset về 0 nguyên tử.",
            [
                ("single-threaded baseline", "Interlocked.Increment(ref _count) cho Increment; Drain bằng Interlocked.Exchange(ref _count, 0)."),
                ("exact under 4 concurrent workers", "Với Pause() giữa đọc và ghi trần, thread khác đọc cùng giá trị cũ — Interlocked giữ read-modify-write nguyên tử."),
            ],
        ),
        "csi-p10-bounded-channel": vi_challenge(
            "Kênh có giới hạn",
            "Hiện thực kênh FIFO có dung lượng: TryProduce trả false khi đầy, TryConsume trả null khi rỗng, Count báo số phần tử đang chờ.",
            [
                ("capacity enforced", "Queue<string> + kiểm tra count trước khi enqueue (bọc lock nếu muốn — hành vi mới là thứ được chấm)."),
                ("FIFO drain", "Dequeue khi Count > 0; dung lượng được nhả ra cho phép produce mới."),
            ],
        ),
        "csi-p10-deadlock-debug": vi_challenge(
            "Debug: Lệnh chuyển tiền bị đóng băng",
            "Transfer phải gọi CjConcurrency.Pause() SAU khi lấy lock đầu và TRƯỚC lock hai (kiểm tra tỷ giá mô phỏng). Bản hiện tại deadlock khi hai lệnh chuyển chạy ngược chiều. Sửa để cả hai luôn hoàn thành — không được bỏ Pause.",
            [
                ("opposite transfers both complete", "Lấy cả hai lock theo THỨ TỰ TOÀN CỤC (ví dụ Id nhỏ trước) — không thể tạo chu kỳ; giữ Pause() giữa lock một và lock hai."),
                ("same-direction transfer still works", "Thứ tự lock xử lý trường hợp thường giống hệt."),
            ],
        ),
        "csi-p10-visitor-stats": vi_challenge(
            "Số lượt truy cập nguyên tử",
            "Hiện thực VisitorStats trên ConcurrentDictionary: RecordVisit trả số lượt SAU lần truy cập này (lần đầu trả 1), Visits trả số hiện tại.",
            [
                ("post-visit counts", "_counts.AddOrUpdate(path, 1, (key, old) => old + 1) trả giá trị MỚI — hãy return nó."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p10-atomic-counter",
            'public class Solution\n{\n    public sealed class Counter\n    {\n        private int _count;\n\n        public void Increment()\n        {\n            CjConcurrency.Pause();   // simulated work — atomicity comes from Interlocked\n            System.Threading.Interlocked.Increment(ref _count);\n        }\n\n        public int Value => System.Threading.Volatile.Read(ref _count);\n\n        public int Drain()\n        {\n            return System.Threading.Interlocked.Exchange(ref _count, 0);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class Counter\n    {\n        private int _count;\n\n        public void Increment()\n        {\n            // near-miss: the required Pause() lands BETWEEN the plain read\n            // and the plain write — every concurrent caller reads the same\n            // stale value and updates vanish by the hundreds\n            int v = _count;\n            CjConcurrency.Pause();\n            _count = v + 1;\n        }\n\n        public int Value => _count;\n\n        public int Drain()\n        {\n            int v = _count;\n            _count = 0;\n            return v;\n        }\n    }\n}\n',
        ),
        (
            "csi-p10-bounded-channel",
            'public class Solution\n{\n    public sealed class BoundedChannel\n    {\n        private readonly int _capacity;\n        private readonly System.Collections.Generic.Queue<string> _items = new();\n\n        public BoundedChannel(int capacity) => _capacity = capacity;\n\n        public bool TryProduce(string item)\n        {\n            if (_items.Count >= _capacity) return false;\n            _items.Enqueue(item);\n            return true;\n        }\n\n        public string? TryConsume()\n        {\n            if (_items.Count == 0) return null;\n            return _items.Dequeue();\n        }\n\n        public int Count => _items.Count;\n    }\n}\n',
            'public class Solution\n{\n    public sealed class BoundedChannel\n    {\n        private readonly System.Collections.Generic.List<string> _items = new();\n\n        public BoundedChannel(int capacity) { }\n\n        // near-miss: capacity accepted but never enforced — the 4th produce\n        // into a 3-slot channel succeeds and the capacity test fails\n        public bool TryProduce(string item)\n        {\n            _items.Add(item);\n            return true;\n        }\n\n        public string? TryConsume()\n        {\n            if (_items.Count == 0) return null;\n            var first = _items[0];\n            _items.RemoveAt(0);\n            return first;\n        }\n\n        public int Count => _items.Count;\n    }\n}\n',
        ),
        (
            "csi-p10-deadlock-debug",
            'public class Solution\n{\n    public sealed class Account\n    {\n        public int Id;\n        public int Balance;\n    }\n\n    public static void Transfer(Account from, Account to, int amount)\n    {\n        // fixed: global lock order — lower Id first — makes the cycle impossible\n        var first = from.Id < to.Id ? from : to;\n        var second = from.Id < to.Id ? to : from;\n        lock (first)\n        {\n            CjConcurrency.Pause();   // simulated FX check, still honored\n            lock (second)\n            {\n                if (from.Balance < amount)\n                    throw new System.InvalidOperationException("insufficient funds");\n                from.Balance -= amount;\n                to.Balance += amount;\n            }\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class Account\n    {\n        public int Id;\n        public int Balance;\n    }\n\n    public static void Transfer(Account from, Account to, int amount)\n    {\n        // near-miss: always locks "from" then "to" — with opposite-direction\n        // transfers each thread holds its first lock, sits in Pause(), and\n        // waits forever on the other\'s lock (circular wait = deadlock)\n        lock (from)\n        {\n            CjConcurrency.Pause();\n            lock (to)\n            {\n                from.Balance -= amount;\n                to.Balance += amount;\n            }\n        }\n    }\n}\n',
        ),
        (
            "csi-p10-visitor-stats",
            'public class Solution\n{\n    public sealed class VisitorStats\n    {\n        private readonly System.Collections.Concurrent.ConcurrentDictionary<string, int> _counts = new();\n\n        public int RecordVisit(string path)\n        {\n            return _counts.AddOrUpdate(path, 1, (key, old) => old + 1);\n        }\n\n        public int Visits(string path)\n        {\n            return _counts.TryGetValue(path, out int v) ? v : 0;\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class VisitorStats\n    {\n        private readonly System.Collections.Concurrent.ConcurrentDictionary<string, int> _counts = new();\n\n        public int RecordVisit(string path)\n        {\n            // near-miss: returns the count BEFORE the increment — the classic\n            // read-modify-write return bug; the first-visit test expects 1\n            _counts.AddOrUpdate(path, 1, (key, old) => old + 1);\n            return _counts.TryGetValue(path, out int v) ? v - 1 : 0;\n        }\n\n        public int Visits(string path)\n        {\n            return _counts.TryGetValue(path, out int v) ? v : 0;\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m10",
    "Checkpoint — The Thread-Safe Job Queue",
    "Combine locking, atomic updates, and worker coordination into a queue that never loses or duplicates work.",
    25,
    r"""
## The gate (mini-build)

A job queue drained by concurrent workers — the producer/consumer core:

1. `Enqueue(string job)` → adds a job.
2. `RunAll(int workers)` → starts `workers` threads; each worker repeatedly
   takes one job (if any) and processes it: call `CjConcurrency.Pause()`
   (the simulated work), then record `"done:" + job` into the results.
3. Every job is processed EXACTLY ONCE — no losses, no duplicates — even
   though workers take jobs one at a time from a shared queue.
4. `Results` exposes the recorded entries; `RunAll` returns after all
   workers finish (join your threads).

The graded test runs 20 jobs across 4 workers with 5 ms simulated work and
asserts exact counts and no duplicates.
""",
    "Checkpoint — Hàng đợi công việc an toàn luồng",
    "Kết hợp lock, cập nhật nguyên tử, và phối hợp worker thành một hàng đợi không mất cũng không nhân đôi công việc.",
    r"""
## Cổng kiểm tra (mini-build)

Hàng đợi công việc được các worker đồng thời rút cạn — lõi producer/consumer:

1. `Enqueue(string job)` → thêm một job.
2. `RunAll(int workers)` → khởi động `workers` thread; mỗi worker lặp: lấy
   một job (nếu còn) và xử lý: gọi `CjConcurrency.Pause()` (công việc mô
   phỏng), rồi ghi `"done:" + job` vào kết quả.
3. Mỗi job được xử lý ĐÚNG MỘT LẦN — không mất, không nhân đôi — dù các
   worker lấy job từng cái một từ hàng đợi chung.
4. `Results` đưa ra các bản ghi; `RunAll` trả về sau khi mọi worker kết thúc
   (join các thread của bạn).

Test chấm điểm chạy 20 job trên 4 worker với công việc mô phỏng 5 ms và
assert số lượng chính xác, không trùng.
""",
    challenge(
        "csi-checkpoint-m10-task",
        "Checkpoint: Exactly-Once Workers",
        """Implement the queue described in the checkpoint:

```csharp
public sealed class JobQueue
{
    public void Enqueue(string job);
    public List<string> RunAll(int workers);   // joins its workers, returns results
    public List<string> Results { get; }
}
```""",
        CJCONC_BOILERPLATE,
        [
            (
                "every job exactly once",
                r"""
var q = new Solution.JobQueue();
string[] jobs = { "alpha", "beta", "gamma", "delta" };
foreach (var j in jobs) q.Enqueue(j);
var results = q.RunAll(3);
Cj.Eq(results.Count, 4, "no losses, no duplicates");
var unique = new System.Collections.Generic.HashSet<string>(results);
Cj.Eq(unique.Count, 4, "all distinct");
Cj.True(results.Contains("done:alpha") && results.Contains("done:beta") && results.Contains("done:gamma") && results.Contains("done:delta"), "all jobs present");
""",
                    "Pop under lock (whole check-and-act), process outside the lock — Pause() then record.",
                ),
                (
                    "more jobs than workers",
                    r"""
var q = new Solution.JobQueue();
for (int i = 0; i < 20; i++) q.Enqueue("job-" + i);
var results = q.RunAll(4);
Cj.Eq(results.Count, 20, "20 jobs, 4 workers, exactly 20 results");
var unique = new System.Collections.Generic.HashSet<string>(results);
Cj.Eq(unique.Count, 20, "each job recorded once");
""",
                    "Workers loop until the queue is empty; the pop is atomic under the gate.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Worker đúng một lần",
            "Hiện thực hàng đợi: Enqueue thêm job; RunAll(workers) khởi các thread, mỗi worker lấy một job (lock quanh toàn bộ check-and-act), gọi CjConcurrency.Pause() rồi ghi \"done:job\"; join xong mới trả kết quả. Mỗi job đúng một lần.",
            [
                ("every job exactly once", "Lấy job dưới lock (toàn bộ check-and-act), xử lý ngoài lock — Pause() rồi ghi kết quả."),
                ("more jobs than workers", "Worker lặp tới khi hàng đợi rỗng; lần lấy job là nguyên tử dưới gate."),
            ],
        ),
        solution='public class Solution\n{\n    public sealed class JobQueue\n    {\n        private readonly object _gate = new();\n        private readonly System.Collections.Generic.Queue<string> _jobs = new();\n        private readonly System.Collections.Generic.List<string> _results = new();\n\n        public System.Collections.Generic.List<string> Results => _results;\n\n        public void Enqueue(string job)\n        {\n            lock (_gate) { _jobs.Enqueue(job); }\n        }\n\n        public System.Collections.Generic.List<string> RunAll(int workers)\n        {\n            var threads = new System.Collections.Generic.List<System.Threading.Thread>();\n            for (int w = 0; w < workers; w++)\n            {\n                var t = new System.Threading.Thread(Work);\n                t.IsBackground = true;\n                threads.Add(t);\n                t.Start();\n            }\n            foreach (var t in threads) t.Join(30000);\n            return _results;\n        }\n\n        private void Work()\n        {\n            while (true)\n            {\n                string job;\n                lock (_gate)                    // whole check-and-act is atomic\n                {\n                    if (_jobs.Count == 0) return;\n                    job = _jobs.Dequeue();\n                }\n                CjConcurrency.Pause();          // simulated work, OUTSIDE the lock\n                lock (_gate) { _results.Add("done:" + job); }\n            }\n        }\n    }\n}\n',
        wrong='public class Solution\n{\n    public sealed class JobQueue\n    {\n        private readonly object _gate = new();\n        private readonly System.Collections.Generic.Queue<string> _jobs = new();\n        private readonly System.Collections.Generic.List<string> _results = new();\n\n        public System.Collections.Generic.List<string> Results => _results;\n\n        public void Enqueue(string job)\n        {\n            lock (_gate) { _jobs.Enqueue(job); }\n        }\n\n        public System.Collections.Generic.List<string> RunAll(int workers)\n        {\n            var threads = new System.Collections.Generic.List<System.Threading.Thread>();\n            for (int w = 0; w < workers; w++)\n            {\n                var t = new System.Threading.Thread(Work);\n                t.IsBackground = true;\n                threads.Add(t);\n                t.Start();\n            }\n            // near-miss: workers started but NEVER JOINED — RunAll returns\n            // immediately, before any worker has processed anything; the\n            // caller sees zero results and no completion guarantee\n            return _results;\n        }\n\n        private void Work()\n        {\n            while (true)\n            {\n                string job;\n                lock (_gate)\n                {\n                    if (_jobs.Count == 0) return;\n                    job = _jobs.Dequeue();\n                }\n                CjConcurrency.Pause();\n                lock (_gate) { _results.Add("done:" + job); }\n            }\n        }\n    }\n}\n',
    )
print("module 10 authored")
