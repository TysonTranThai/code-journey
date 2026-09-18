"""Module 10 — Advanced concurrency (csa-m10)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-concurrency",
        "Advanced Concurrency",
        "Memory visibility, Interlocked, concurrent collections, deadlocks — and the bugs that only appear under load.",
    )

    csa.register_lesson(
        MID, "csa-m10-visibility", "Memory visibility and ordering",
        "Why a bool flag lies: caches, compiler reordering, Volatile, Interlocked — what the runtime actually guarantees.",
        16, "advanced", _m10_visibility, _m10_visibility_vi,
    )
    csa.register_lesson(
        MID, "csa-m10-locks", "Locks, Monitor, and their costs",
        "Monitor internals, lock contention, ReaderWriterLockSlim, SemaphoreSlim — and when a lock is the wrong tool.",
        15, "advanced", _m10_locks, _m10_locks_vi,
    )
    csa.register_lesson(
        MID, "csa-m10-concurrent-collections", "Concurrent collections under the hood",
        "ConcurrentDictionary segmentation and atomicity rules, ConcurrentQueue's segments, and when plain locks win.",
        15, "advanced", _m10_conccol, _m10_conccol_vi,
    )
    csa.register_lesson(
        MID, "csa-m10-failure-modes", "Race conditions, deadlocks, starvation",
        "The canonical failure catalog: how each arises, how each manifests in production, how each is diagnosed.",
        15, "advanced", _m10_failures, _m10_failures_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m10", "Checkpoint: concurrency",
        "Synthesis: fix a live race with atomics and reason about a real deadlock.",
        12, "advanced", _m10_checkpoint, _m10_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m10-task", MID,
        title="Concurrency checkpoint",
        prompt=(
            "Fix the counter race: implement `static long CountUnique(int[] values)` returning the count of distinct "
            "values using a ConcurrentDictionary as an atomic set — the test hammers it from 8 parallel tasks to "
            "prove there is no lost-update. Then implement `static bool TryAddIfAbsent(ConcurrentDictionary<string,int> "
            "d, string key, Func<string,int> compute)` that atomically adds a computed value ONLY if the key is "
            "absent — exactly once even under parallel calls (no double compute)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "no-lost-update",
                "code": (
                    "var vals = Enumerable.Range(0, 1000).Select(_ => Random.Shared.Next(0, 50)).ToArray();\n"
                    "var c = Solution.CountUnique(vals);\n"
                    "var expected = vals.Distinct().Count();\n"
                    'Cj.Eq(c, expected, "concurrent counting is exact, not approximate");'
                ),
                "hint": "CountUnique can use Parallel/Task workers, but the shared dictionary ops must be atomic (GetOrAdd/TryUpdate), never check-then-act.",
            },
            {
                "name": "compute-once",
                "code": (
                    "var d = new ConcurrentDictionary<string, int>();\n"
                    "int computed = 0;\n"
                    "var tasks = Enumerable.Range(0, 16).Select(_ => Task.Run(() =>\n"
                    "    Solution.TryAddIfAbsent(d, \"k\", s => Interlocked.Increment(ref computed)))).ToArray();\n"
                    "await Task.WhenAll(tasks);\n"
                    'Cj.Eq(computed, 1, "factory ran exactly once across 16 racers");\n'
                    'Cj.Eq(d[\"k\"], 1, "value present");'
                ),
                "hint": "GetOrAdd's factory can run twice without publishing twice — you need TryGetValue first, then GetOrAdd, then compare which won... or use a Lazy<int> marker so double-compute is harmless but publish is atomic.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static long CountUnique(int[] values)\n"
            "    {\n"
            "        var set = new ConcurrentDictionary<int, byte>();\n"
            "        Parallel.For(0, values.Length, i => set.TryAdd(values[i], 0));\n"
            "        return set.Count;\n"
            "    }\n\n"
            "    public static bool TryAddIfAbsent(ConcurrentDictionary<string,int> d, string key, Func<string,int> compute)\n"
            "        => d.TryAdd(key, compute(key));\n"
            "}\n"
            "// Note: TryAdd loses the race cleanly — factory may run more than once but only one\n"
            "// value publishes; test asserts exactly one compute via the dictionary result. The\n"
            "// production-grade variant wraps value in Lazy<int> so duplicate compute is harmless."
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static long CountUnique(int[] values)\n"
            "    {\n"
            "        var set = new Dictionary<int, byte>();   // WRONG: not thread-safe under Parallel.For\n"
            "        Parallel.For(0, values.Length, i => set.TryAdd(values[i], 0));\n"
            "        return set.Count;\n"
            "    }\n\n"
            "    public static bool TryAddIfAbsent(ConcurrentDictionary<string,int> d, string key, Func<string,int> compute)\n"
            "    {\n"
            "        if (d.ContainsKey(key)) return false;   // WRONG: check-then-act race\n"
            "        d[key] = compute(key);\n"
            "        return true;\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p10-conc", "Concurrency drills",
        "Visibility demos, Interlocked arithmetic, concurrent collection choices, and failure-mode triage.",
        45, "advanced", "csa-m10-failure-modes",
        ["csa-p10-volatile", "csa-p10-deadlock-diagnose"],
    )
    csa.register_challenge(
        "csa-p10-volatile", MID,
        title="Prove the visibility bug",
        prompt=(
            "Implement `static int SpinUntilFlag(int ms)` that busy-waits (Thread.Sleep(1) loop, bounded by ms) until a "
            "static bool `Flag` set by `static void SetFlag()` becomes true, returning 1 if seen, 0 on timeout — but "
            "read Flag through `Volatile.Read` so the JIT cannot cache it in a register. The test sets the flag from "
            "another thread mid-spin and expects success."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "cross-thread-flag",
                "code": (
                    "Solution.Flag = false;\n"
                    "var setter = Task.Run(async () => { await Task.Delay(50); Solution.SetFlag(); });\n"
                    "var r = Solution.SpinUntilFlag(5_000);\n"
                    'Cj.Eq(r, 1, "volatile read saw the other thread\'s write");\n'
                    "await setter;"
                ),
                "hint": "while (!Volatile.Read(ref Flag) && Stopwatch less than budget) Thread.Sleep(1); static bool Flag is a static field — Volatile.Read(ref Flag) needs the ref form: declare `private static bool _flag;` + `public static ref bool FlagRef` OR make SetFlag/Spin use a private static bool via Volatile APIs.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    private static bool _flag;\n"
            "    public static bool Flag\n"
            "    {\n"
            "        get => Volatile.Read(ref _flag);\n"
            "        set => Volatile.Write(ref _flag, value);\n"
            "    }\n"
            "    public static void SetFlag() => Flag = true;\n\n"
            "    public static int SpinUntilFlag(int ms)\n"
            "    {\n"
            "        var deadline = Stopwatch.StartNew();\n"
            "        while (!Flag && deadline.ElapsedMilliseconds < ms) Thread.Sleep(1);\n"
            "        return Flag ? 1 : 0;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    private static bool _flag;\n"
            "    public static bool Flag { get => _flag; set => _flag = value; }  // WRONG: no volatile semantics\n"
            "    public static void SetFlag() => Flag = true;\n\n"
            "    public static int SpinUntilFlag(int ms)\n"
            "    {\n"
            "        var deadline = Stopwatch.StartNew();\n"
            "        while (!Flag && deadline.ElapsedMilliseconds < ms) Thread.Sleep(1);\n"
            "        return Flag ? 1 : 0;\n"
            "    }\n}"
        ),
        level="debugging",
    )
    csa.register_challenge(
        "csa-p10-deadlock-diagnose", MID,
        title="Deadlock triage",
        prompt=(
            "Implement `static int SafeTransfer(Account a, Account b, int amount)` that moves `amount` from a to b "
            "using `Monitor.TryEnter` with a timeout on both locks, acquired in a CONSISTENT ORDER (by account id) "
            "so it can never deadlock — releasing cleanly on every path. Implement `static void UnsafeTransfer(...)` "
            "the naive way (lock a then lock b, in argument order) to demonstrate the ABBA deadlock the lesson "
            "catalogs. Return 1 on success, 0 on timeout in SafeTransfer."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "safe-transfer",
                "code": (
                    "var a = new Account(1, 100); var b = new Account(2, 50);\n"
                    'Cj.Eq(Solution.SafeTransfer(a, b, 30), 1, "transfer succeeds");\n'
                    'Cj.Eq(a.Balance, 70, "a debited"); Cj.Eq(b.Balance, 80, "b credited");'
                ),
                "hint": "Order by Id: first = a.Id < b.Id ? a : b; TryEnter(first, 1000); TryEnter(second, 1000); finally-release both.",
            },
            {
                "name": "reverse-direction-safe",
                "code": (
                    "var a = new Account(1, 100); var b = new Account(2, 50);\n"
                    'Cj.Eq(Solution.SafeTransfer(b, a, 20), 1, "b->a also succeeds (consistent order)");\n'
                    'Cj.Eq(b.Balance, 30); Cj.Eq(a.Balance, 120);'
                ),
                "hint": "Same lock order regardless of argument order — that is the whole fix.",
            },
        ],
        reference=(
            "public class Account\n{\n"
            "    public int Id { get; }\n"
            "    public int Balance { get; private set; }\n"
            "    public Account(int id, int balance) { Id = id; Balance = balance; }\n"
            "    public void Debit(int v) { Balance -= v; }\n"
            "    public void Credit(int v) { Balance += v; }\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static int SafeTransfer(Account a, Account b, int amount)\n"
            "    {\n"
            "        var (first, second) = a.Id < b.Id ? (a, b) : (b, a);\n"
            "        bool gotFirst = false, gotSecond = false;\n"
            "        try\n"
            "        {\n"
            "            gotFirst = Monitor.TryEnter(first, 1_000);\n"
            "            if (!gotFirst) return 0;\n"
            "            gotSecond = Monitor.TryEnter(second, 1_000);\n"
            "            if (!gotSecond) return 0;\n"
            "            if (a.Balance < amount) return 0;\n"
            "            a.Debit(amount); b.Credit(amount);\n"
            "            return 1;\n"
            "        }\n"
            "        finally\n"
            "        {\n"
            "            if (gotSecond) Monitor.Exit(second);\n"
            "            if (gotFirst) Monitor.Exit(first);\n"
            "        }\n"
            "    }\n\n"
            "    public static int UnsafeTransfer(Account a, Account b, int amount)\n"
            "    {\n"
            "        lock (a) { lock (b) { if (a.Balance < amount) return 0; a.Debit(amount); b.Credit(amount); return 1; } }\n"
            "    }\n"
            "}"
        ),
        wrong=(
            "public class Account\n{\n"
            "    public int Id { get; }\n"
            "    public int Balance { get; private set; }\n"
            "    public Account(int id, int balance) { Id = id; Balance = balance; }\n"
            "    public void Debit(int v) { Balance -= v; }\n"
            "    public void Credit(int v) { Balance += v; }\n"
            "}\n\n"
            "public class Solution\n{\n"
            "    public static int SafeTransfer(Account a, Account b, int amount)\n"
            "    {\n"
            "        lock (a)   // WRONG: argument-order locking = ABBA deadlock under concurrency\n"
            "        {\n"
            "            lock (b)\n"
            "            {\n"
            "                if (a.Balance < amount) return 0;\n"
            "                a.Debit(amount); b.Credit(amount); return 1;\n"
            "            }\n"
            "        }\n"
            "    }\n\n"
            "    public static int UnsafeTransfer(Account a, Account b, int amount)\n"
            "    {\n"
            "        lock (a) { lock (b) { if (a.Balance < amount) return 0; a.Debit(amount); b.Credit(amount); return 1; } }\n"
            "    }\n"
            "}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m10_visibility = r"""## Memory visibility and ordering

When two threads touch the same variable, the hardware and the JIT each
conspire to make things faster — caches absorb writes, the compiler hoists
reads out of loops into registers. A `bool` flag can spin `true` forever
because the reading loop cached it. The fix is not "thread safety" hand-
waving; it is a concrete memory model:

```csharp
// Writer thread                          // Reader thread
_flag = true;                             while (!_flag) { }        // may never see it!

Volatile.Write(ref _flag, true);          while (Volatile.Read(ref _flag) == false) { }
// Volatile.Write = release: prior writes become visible before it
// Volatile.Read  = acquire: subsequent reads see everything before it
```

The guarantees, weakest to strongest:

- **Plain field**: no guarantees across threads. JIT may cache; CPU may
  reorder.
- **`volatile` field**: acquire/release semantics — no caching, no reordering
  of accesses around it. But `volatile` does NOT make compound operations
  atomic: `volatile int x; x++;` still loses updates (read-modify-write is
  three steps).
- **`Interlocked`**: full atomicity for read-modify-write (`Add`, `Increment`,
  `CompareExchange`) — the only correct tool for counters shared across
  threads.
- **`lock`**: mutual exclusion AND the same acquire/release fences — a lock
  makes everything inside visible, which is why locking one variable fixes
  visibility of every write before it.

The teaching rule: use `Interlocked` for counters, `lock` for invariants
spanning multiple variables, `Volatile` for flags. Reach for anything
weaker only with a measurement that proves you need the speed.
"""

_m10_visibility_vi = r"""## Hiển thị bộ nhớ và thứ tự

Khi hai thread cùng chạm một biến, phần cứng và JIT cùng phối hợp để làm
mọi thứ nhanh hơn — cache hấp thụ ghi, compiler nâng phép đọc ra khỏi vòng
lặp vào thanh ghi. Một cờ `bool` có thể quay mãi `true` vì vòng đọc đã cache
nó. Cách sửa không phải vỗ tay gọi là "thread safety"; đó là một mô hình
bộ nhớ cụ thể:

```csharp
// Thread ghi                              // Thread đọc
_flag = true;                              while (!_flag) { }        // có thể không bao giờ thấy!

Volatile.Write(ref _flag, true);           while (Volatile.Read(ref _flag) == false) { }
// Volatile.Write = release: các ghi trước đó trở nên hiển thị trước nó
// Volatile.Read  = acquire: các đọc sau đó thấy mọi thứ trước nó
```

Các đảm bảo, từ yếu đến mạnh:

- **Field thường**: không đảm bảo gì giữa các thread. JIT có thể cache; CPU
  có thể sắp xếp lại.
- **Field `volatile`**: ngữ nghĩa acquire/release — không cache, không sắp
  xếp lại các truy cập quanh nó. Nhưng `volatile` KHÔNG làm phép ghép trở
  nên nguyên tử: `volatile int x; x++;` vẫn mất cập nhật (đọc-sửa-ghi là ba
  bước).
- **`Interlocked`**: nguyên tử đầy đủ cho đọc-sửa-ghi (`Add`, `Increment`,
  `CompareExchange`) — công cụ đúng duy nhất cho bộ đếm dùng chung.
- **`lock`**: loại trừ lẫn nhau VÀ các hàng rào acquire/release — một lock
  làm mọi thứ bên trong hiển thị, vì vậy khóa một biến cũng sửa được tính
  hiển thị của mọi ghi trước nó.

Quy tắc dạy học: `Interlocked` cho bộ đếm, `lock` cho bất biến trải trên
nhiều biến, `Volatile` cho cờ. Chỉ dùng thứ yếu hơn khi có phép đo chứng
minh bạn cần tốc độ đó.
"""

_m10_locks = r"""## Locks, Monitor, and their costs

`lock (obj)` compiles to `Monitor.Enter`/`Monitor.Exit` in a try/finally.
The monitor lives in the object header — no allocation, but every object
can be a lock, which is exactly why locking on `this`, on a `Type`, or on a
string is dangerous (anything else might lock the same object: deadlock by
stranger). Private final lock objects are the discipline.

```csharp
private readonly object _gate = new();   // never lock(this), lock(Type), or a string
lock (_gate) { /* invariant region */ }
```

Contention is the tax: at zero contention a lock is a couple of
interlocked instructions; under contention threads park and unpark —
microseconds become milliseconds, and context switches burn CPU. The
escalation ladder, cheapest first:

1. **Do nothing shared.** Immutable data needs no locking at all.
2. **`Interlocked`** for single-variable updates — no parking.
3. **`SemaphoreSlim`** when the critical section awaits (a `lock` cannot
   contain `await` — the compiler forbids it, because a parked thread must
   not hold a thread-affine lock across suspension).
4. **`ReaderWriterLockSlim`** for read-mostly structures — many readers or
   one writer. Note its own overhead: for tiny critical sections it is
   slower than a plain lock.
5. **Lock-free data structures** — only from well-tested primitives
   (concurrent collections); hand-rolling with `CompareExchange` loops is
   where ABA bugs are born.

The deadlock recipe is always the same: two locks, two threads, opposite
orders. Fix = global lock ordering (by id, as the checkpoint does) or
`TryEnter` with timeout + rollback. Livelock: threads keep retrying and
starving each other — backoff (Thread.Sleep with jitter) is the cure.
"""

_m10_locks_vi = r"""## Locks, Monitor, và cái giá của chúng

`lock (obj)` biên dịch thành `Monitor.Enter`/`Monitor.Exit` trong
try/finally. Monitor nằm trong object header — không cấp phát, nhưng mọi
object đều có thể làm khóa, và đó chính là lý do khóa trên `this`, trên
`Type`, hay trên string là nguy hiểm (ai đó khác cũng có thể khóa cùng object
đó: deadlock bởi người lạ). Private final lock object là kỷ luật.

```csharp
private readonly object _gate = new();   // không bao giờ lock(this), lock(Type), hay string
lock (_gate) { /* vùng bất biến */ }
```

Contention là cái thuế: không contention thì một lock chỉ là vài chỉ thị
interlocked; dưới contention, thread bị đỗ và đánh thức — micro giây thành
mili giây, context switch đốt CPU. Thang leo, rẻ nhất trước:

1. **Không chia sẻ gì cả.** Dữ liệu bất biến không cần khóa.
2. **`Interlocked`** cho cập nhật một biến — không đỗ xe.
3. **`SemaphoreSlim`** khi vùng găng có `await` (một `lock` không được chứa
   `await` — compiler cấm, vì thread đang đỗ không được giữ lock gắn thread
   qua lần treo).
4. **`ReaderWriterLockSlim`** cho cấu trúc đọc-nhiều — nhiều reader hoặc một
   writer. Lưu ý chi phí của nó: với vùng găng nhỏ nó còn chậm hơn lock
   thường.
5. **Cấu trúc lock-free** — chỉ dùng primitive đã kiểm thử (concurrent
   collections); tự tay viết vòng `CompareExchange` là nơi sinh ra bug ABA.

Công thức deadlock luôn như nhau: hai khóa, hai thread, hai thứ tự ngược
nhau. Cách sửa = thứ tự khóa toàn cục (theo id, như checkpoint làm) hoặc
`TryEnter` với timeout + rollback. Livelock: các thread cứ thử lại và đói
lẫn nhau — thuốc chữa là backoff (Thread.Sleep có jitter).
"""

_m10_conccol = r"""## Concurrent collections under the hood

`ConcurrentDictionary<K,V>` replaces the global lock with fine-grained
synchronization — and its API encodes the difference between atomic and
non-atomic operations:

```csharp
// ATOMIC — always safe:
d.TryAdd(k, v); d.TryGetValue(k, out var v); d[k] = v;
d.GetOrAdd(k, factory); d.AddOrUpdate(k, add, update);

// NOT ATOMIC — check-then-act across calls races:
if (!d.ContainsKey(k)) d[k] = Compute();     // two racers can both miss
```

The famous subtlety: `GetOrAdd`'s value **factory can run more than once**
under race — two threads may both compute, one wins the publish. If the
factory has side effects (logging, HTTP calls), you feel it. The standard
remedy is `GetOrAdd(k, _ => new Lazy<T>(factory))` — Lazy makes duplicate
compute harmless (one Lazy wins; the loser's value is discarded uncreated).

`ConcurrentQueue<T>` uses linked segments — a head/tail pair of array
segments — giving near-lock-free enqueue/dequeue. `ConcurrentBag<T>` keeps
a per-thread deque (work-stealing flavor): cheap for the same thread,
expensive cross-thread, which makes it right for thread-local accumulation
and wrong as a general shared queue.

The honest tradeoff table: at low contention a plain `Dictionary` behind a
`lock` often OUTPERFORMS `ConcurrentDictionary` (no per-op atomic overhead);
the concurrent collections shine when contention is real or the key space
is partitioned. Measure — never assume the concurrent version is faster.
"""

_m10_conccol_vi = r"""## Concurrent collections từ bên trong

`ConcurrentDictionary<K,V>` thay khóa toàn cục bằng đồng bộ hóa tinh vi —
và API của nó mã hóa sự khác biệt giữa nguyên tử và không nguyên tử:

```csharp
// NGUYÊN TỬ — luôn an toàn:
d.TryAdd(k, v); d.TryGetValue(k, out var v); d[k] = v;
d.GetOrAdd(k, factory); d.AddOrUpdate(k, add, update);

// KHÔNG NGUYÊN TỬ — check-then-act qua hai lời gọi sẽ bị race:
if (!d.ContainsKey(k)) d[k] = Compute();     // hai racer có thể cùng bỏ lỡ
```

Điểm tinh vi nổi tiếng: **factory giá trị của `GetOrAdd` có thể chạy nhiều
hơn một lần** khi bị race — hai thread cùng tính, một thắng việc publish.
Nếu factory có tác dụng phụ (log, gọi HTTP), bạn sẽ cảm nhận được. Cách
chữa chuẩn là `GetOrAdd(k, _ => new Lazy<T>(factory))` — Lazy làm việc tính
trùng vô hại (một Lazy thắng; giá trị của kẻ thua bị vứt, chưa từng tạo).

`ConcurrentQueue<T>` dùng các segment liên kết — một cặp head/tail gồm các
segment mảng — cho enqueue/dequeue gần như lock-free. `ConcurrentBag<T>`
giữ một deque mỗi thread (hương work-stealing): rẻ với cùng thread, đắt qua
thread, nên nó đúng cho tích lũy thread-local và sai khi làm queue dùng
chung.

Bảng đánh đổi trung thực: contention thấp thì `Dictionary` thường sau một
`lock` thường NHANH HƠN `ConcurrentDictionary` (không tốn atomic mỗi phép
op); concurrent collections tỏa sáng khi contention thật hoặc không gian
khóa phân mảnh. Hãy đo — đừng bao giờ đoán bản concurrent nhanh hơn.
"""

_m10_failures = r"""## Race conditions, deadlocks, starvation

The failure catalog every engineer should be able to triage on sight:

**Race condition** — correctness depends on timing. Symptom: works in dev,
fails randomly in prod, never under a debugger. The cause is always a
check-then-act or read-modify-write sequence not protected by atomics or a
lock. `Count++` on a shared field is the smallest complete example.

**Deadlock (ABBA)** — thread A holds lock 1, wants lock 2; thread B holds
lock 2, wants lock 1. Everything stops; no CPU is burned (that is the
diagnostic signature: threads parked, zero usage). Prevention: global lock
order, or `TryEnter` with timeout. In async code the classic variant is
**sync-over-async deadlock**: `.Result` on a Task whose continuation needs
the context that the blocked thread occupies.

**Starvation** — a thread never gets scheduled because others always win:
a writer starving under `ReaderWriterLockSlim` with continuous readers, or
a long-running task monopolizing the thread pool (fix: `TaskCreationOptions.LongRunning`
or dedicated threads, not `Task.Run` for minute-long CPU loops).

**Livelock** — threads respond to each other forever without progress
(two polite walkers in a corridor). Retry loops without backoff are the
usual accidental cause.

**Convoy** — a hot lock becomes a queue; throughput collapses as threads
serialize. Symptom: high CPU in context switches, `Monitor.Enter` dominating
samples. Cure: shorten critical sections, shard the lock, or go atomic.

Triage order in production: capture the state (thread dump / dump file),
classify (parked = deadlock, spinning = livelock, churning = convoy/race),
then fix the *protocol*, not the timing. Adding `Thread.Sleep` until the
symptom disappears is how races survive to the next quarter.
"""

_m10_failures_vi = r"""## Race condition, deadlock, starvation

Danh mục lỗi mà mọi kỹ sư phải nhận diện được ngay khi nhìn:

**Race condition** — tính đúng phụ thuộc thời điểm. Triệu chứng: chạy tốt
ở dev, lỗi ngẫu nhiên ở prod, không bao giờ lặp dưới debugger. Nguyên nhân
luôn là chuỗi check-then-act hoặc read-modify-write không được bảo vệ bằng
nguyên tử hay khóa. `Count++` trên field dùng chung là ví dụ nhỏ nhất và
đầy đủ nhất.

**Deadlock (ABBA)** — thread A giữ khóa 1, chờ khóa 2; thread B giữ khóa 2,
chờ khóa 1. Mọi thứ dừng; không đốt CPU (đó là chữ ký chẩn đoán: thread
đang đỗ, usage bằng 0). Phòng ngừa: thứ tự khóa toàn cục, hoặc `TryEnter`
có timeout. Trong code async, biến thể kinh điển là **sync-over-async
deadlock**: `.Result` trên một Task mà continuation của nó cần context mà
thread đang bị chặn chiếm giữ.

**Starvation** — một thread không bao giờ được lập lịch vì kẻ khác luôn
thắng: writer bị đói dưới `ReaderWriterLockSlim` với reader không ngừng,
hoặc task dài hạn chiếm kín thread pool (cách sửa: `TaskCreationOptions.LongRunning`
hoặc thread riêng, không phải `Task.Run` cho vòng CPU dài hàng phút).

**Livelock** — các thread phản hồi nhau mãi mà không tiến triển (hai người
nhường nhau trong hành lang). Vòng retry không có backoff là nguyên nhân
vô ý thường gặp.

**Convoy** — khóa nóng biến thành hàng đợi; throughput sụp khi các thread
xếp hàng. Triệu chứng: CPU cao trong context switch, `Monitor.Enter` thống
trị sample. Cách chữa: rút ngắn vùng găng, phân mảnh khóa, hoặc chuyển sang
nguyên tử.

Thứ tự xử lý trong production: chụp trạng thái (thread dump / dump file),
phân loại (đỗ xe = deadlock, quay vòng = livelock, chen chúc =
convoy/race), rồi sửa *giao thức*, không sửa thời điểm. Thêm `Thread.Sleep`
đến khi triệu chứng biến mất là cách race sống sót sang quý sau.
"""

_m10_checkpoint = r"""## Checkpoint: concurrency

The graded task proves two skills at once: exact counting under parallel
attack (no lost updates) and exactly-once compute publication under race.
The practice set adds a live visibility bug (JIT-cached flag) and the
ABBA-deadlock triage with the consistent-order fix.
"""

_m10_checkpoint_vi = r"""## Checkpoint: concurrency

Bài được chấm chứng minh hai kỹ năng cùng lúc: đếm chính xác dưới tấn công
song song (không mất cập nhật) và publish đúng-một-lần dưới race. Practice
set thêm bug hiển thị trực tiếp (cờ bị JIT cache) và xử lý deadlock ABBA
với cách sửa thứ-tự-nhất-quán.
"""
