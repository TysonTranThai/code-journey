#!/usr/bin/env python3
"""Java — Intermediate — Module 9: java-concurrency.

Concurrency fundamentals without overreach: threads and runnables, why
shared mutable state races, visibility with Atomic*/synchronized, and
deterministic-challenge design (joined threads, latched completion). The
sandbox gives each test its own JVM with a 15s cap — challenges are
designed to terminate deterministically. House conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-concurrency"

# ── lesson 9.1 — threads & runnables ────────────────────────────────────────
L_THREADS_EN = r"""
## Threads, Runnables, and what the JVM promises

A `Thread` runs a `Runnable` concurrently; `start()` begins it, `join()`
waits for completion:

```java
Thread worker = new Thread(() -> System.out.println("work"));
worker.start();
worker.join();   // deterministic again — everything before join happened-before after
```

After `join()` returns, you may read everything the thread wrote — that
is the *happens-before* edge you'll use in every deterministic exercise.

The classic beginner bug is calling `run()` instead of `start()`: that
executes the Runnable on the *current* thread — sequential, no
concurrency at all.

Threads are expensive (each carries ~1MB stack by default); that is why
executors exist — Module-level coverage, Advanced goes deeper.
"""

L_THREADS_VI = r"""
## Thread, Runnable, và JVM hứa gì

Một `Thread` chạy một `Runnable` đồng thời; `start()` khởi động, `join()`
chờ hoàn tất:

```java
Thread worker = new Thread(() -> System.out.println("work"));
worker.start();
worker.join();   // xác định trở lại — mọi thứ trước join đã xảy ra trước mọi thứ sau
```

Sau khi `join()` trả về, bạn được đọc mọi thứ thread đã ghi — đó là cạnh
*happens-before* bạn sẽ dùng trong mọi bài tập xác định.

Bug kinh điển của người mới là gọi `run()` thay vì `start()`: lệnh đó chạy
Runnable trên thread *hiện tại* — tuần tự, không có concurrency nào cả.

Thread đắt đỏ (mỗi thread mang stack ~1MB theo mặc định); vì vậy mới có
executor — được.cover ở mức module, Advanced sẽ sâu hơn.
"""

# ── lesson 9.2 — races & visibility ────────────────────────────────────────
L_RACES_EN = r"""
## Race conditions and visibility

Two problems plague shared mutable state:

**Interference** — `count++` is read-modify-write; two threads can read
the same value and lose an increment:

```java
class Counter { int count; void inc() { count++; } }
// 2 threads × 10_000 increments → often < 20_000
```

**Visibility** — without synchronization, one thread's writes may never
become visible to another (the JIT may hoist the read out of a loop):

```java
boolean stop = false;          // plain field — may never be seen!
// Thread A: while (!stop) work();
// Thread B: stop = true;
```

Fixes, weakest to strongest:
- `volatile` — visibility only; fine for flags, wrong for count++
- `AtomicLong`/`AtomicInteger` — atomic read-modify-write
  (`incrementAndGet()`)
- `synchronized` blocks — mutual exclusion for compound actions

```java
class SafeCounter {
    private final AtomicLong count = new AtomicLong();
    void inc() { count.incrementAndGet(); }
    long value() { return count.get(); }
}
```

Rule of thumb: make shared state immutable, or confine it to one thread,
or protect every access consistently — pick one and document it.
"""

L_RACES_VI = r"""
## Race condition và visibility

Hai vấn đề đe dọa trạng thái khả biến dùng chung:

**Can thiệp** — `count++` là đọc-sửa-ghi; hai thread có thể đọc cùng một
giá trị và mất một phép tăng:

```java
class Counter { int count; void inc() { count++; } }
// 2 thread × 10_000 lần tăng → thường < 20_000
```

**Visibility** — không đồng bộ hóa, ghi của thread này có thể không bao
giờ được thread kia nhìn thấy (JIT có thể kéo phép đọc ra khỏi vòng lặp):

```java
boolean stop = false;          // field thường — có thể không bao giờ được thấy!
// Thread A: while (!stop) work();
// Thread B: stop = true;
```

Cách sửa, từ yếu đến mạnh:
- `volatile` — chỉ visibility; ổn cho cờ, sai cho count++
- `AtomicLong`/`AtomicInteger` — đọc-sửa-ghi nguyên tử
  (`incrementAndGet()`)
- Khối `synchronized` — loại trừ tương hỗ cho hành động ghép

```java
class SafeCounter {
    private final AtomicLong count = new AtomicLong();
    void inc() { count.incrementAndGet(); }
    long value() { return count.get(); }
}
```

Kinh nghiệm: biến trạng thái dùng chung thành bất biến, hoặc giam giữ nó
trong một thread, hoặc bảo vệ mọi truy cập nhất quán — chọn một và tài
liệu hóa nó.
"""

# ── lesson 9.3 — executors & futures ───────────────────────────────────────
L_EXEC_EN = r"""
## ExecutorService and Futures

Executors decouple *task submission* from *thread management*:

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> expensive());
Integer result = f.get();      // blocks until done
pool.shutdown();               // always — or the JVM won't exit
```

Key behaviors:
- `submit` returns a `Future` immediately; `get()` joins that one task
- tasks run on pool threads — exceptions inside them do NOT crash your
  thread; `get()` rethrows them wrapped in `ExecutionException`
- `invokeAll` submits a batch; the returned Futures complete in order
- always `shutdown()` — try/finally or `close()` (ExecutorService is
  AutoCloseable since Java 19)

Deterministic testing pattern: submit N tasks, `get()` each — after all
gets return, every side effect is visible. Latches are the tool when
tasks must *all finish* before an assertion:

```java
CountDownLatch done = new CountDownLatch(n);
// each task: work(); done.countDown();
done.await();   // wait for all n countDowns
```
"""

L_EXEC_VI = r"""
## ExecutorService và Future

Executor tách *việc nộp task* khỏi *quản lý thread*:

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> expensive());
Integer result = f.get();      // chặn đến khi xong
pool.shutdown();               // luôn luôn — nếu không JVM không thoát
```

Hành vi then chốt:
- `submit` trả `Future` ngay lập tức; `get()` chờ đúng task đó
- task chạy trên thread của pool — ngoại lệ bên trong KHÔNG làm vỡ thread
  của bạn; `get()` ném lại chúng bọc trong `ExecutionException`
- `invokeAll` nộp một lô; các Future trả về hoàn tất theo thứ tự
- luôn luôn `shutdown()` — try/finally hoặc `close()` (ExecutorService
  là AutoCloseable từ Java 19)

Mẫu kiểm thử xác định: nộp N task, `get()` từng cái — sau khi mọi get
trả về, mọi side effect đã visible. Latch là công cụ khi các task phải
*hoàn tất hết* trước một assertion:

```java
CountDownLatch done = new CountDownLatch(n);
// mỗi task: work(); done.countDown();
done.await();   // chờ đủ n countDown
```
"""

write_module(
    MOD,
    "Concurrency Fundamentals",
    "Threads and happens-before, race conditions and the visibility ladder, and executors with deterministic completion.",
    "Nền tảng concurrency",
    "Thread và happens-before, race condition và thang visibility, và executor với sự hoàn tất xác định.",
    ["threads-happens-before", "races-visibility", "executors-futures", "javi-checkpoint-concurrency"],
    ["javi-p9-concurrency"],
)

write_lesson(MOD, "threads-happens-before", "Threads & Happens-Before", "start/join semantics, the run() vs start() trap, and the memory edge join() gives deterministic tests.", 13, L_THREADS_EN, "Thread & Happens-Before", "Ngữ nghĩa start/join, bẫy run() so với start(), và cạnh bộ nhớ mà join() cho phép test xác định.", L_THREADS_VI)

write_lesson(MOD, "races-visibility", "Races & Visibility", "Lost updates, invisible writes, and the volatile → atomic → synchronized ladder with when each is correct.", 15, L_RACES_EN, "Race & Visibility", "Cập nhật thất lạc, ghi vô hình, và thang volatile → atomic → synchronized với thời điểm nào đúng cho cái nào.", L_RACES_VI)

write_lesson(MOD, "executors-futures", "Executors & Futures", "Submitting tasks, rethrowing ExecutionExceptions, and latch-based completion for deterministic assertions.", 14, L_EXEC_EN, "Executor & Future", "Nộp task, ném lại ExecutionException, và hoàn tất kiểu latch cho assertion xác định.", L_EXEC_VI)

# ── practice set ────────────────────────────────────────────────────────────
P9_BOILER = r"""
import java.util.*;
import java.util.concurrent.atomic.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P9_COUNTER = challenge(
    "javi-p9-safe-counter",
    "The Thread-Safe Counter",
    r"""Implement inside `Solution`:
- `static class RacyCounter` with `void inc()` (`count++` on a plain
  field) and `long value()`.
- `static class SafeCounter` with the same API backed by an
  `AtomicLong`.
- `static long hammer(Object counter, int threads, int perThread)`:
  starts `threads` threads, each calling `inc()` perThread times via
  reflection (RacyCounter or SafeCounter), joins them, then returns
  `value()` via reflection.

With hammer(c, 4, 1000): RacyCounter usually loses updates (< 4000);
SafeCounter must ALWAYS return exactly 4000. The safe test runs the
hammer five times to make flakiness visible.""",
    P9_BOILER,
    [
        (
            "safe counter exact under contention",
            r"""
for (int round = 0; round < 5; round++) {
    Object c = new Solution.SafeCounter();
    checkEq(Solution.hammer(c, 4, 1000), 4000L, "exact after round " + round);
}
""",
            "AtomicLong read-modify-write never loses an update.",
        ),
        (
            "racy counter exists (control)",
            r"""
Object c = new Solution.RacyCounter();
long v = Solution.hammer(c, 2, 10);
checkTrue(v >= 0 && v <= 20, "racy result within loose bounds");
""",
            "The racy version runs but gets no exactness guarantee — that's the lesson.",
        ),
    ],
    level="guided",
)

CH_P9_PARALLEL = challenge(
    "javi-p9-parallel-sum",
    "Deterministic Parallel Sum",
    r"""Implement `static long parallelSum(int[] data, int parts)`:
- split the array into `parts` contiguous chunks (distribute remainder
  to earlier chunks)
- compute each chunk's sum on its own thread (plain `Thread` + `join()`
  is fine)
- combine and return the total

After joining, the combine step is deterministic — that happens-before
edge is the exercise. Empty array or parts <= 0 → 0.""",
    P9_BOILER,
    [
        (
            "even split",
            r"""
int[] data = {1, 2, 3, 4, 5, 6, 7, 8};
checkEq(Solution.parallelSum(data, 4), 36L, "8 elems in 4 parts");
""",
            "Each part sums 2 elements: 6+6+... total 36.",
        ),
        (
            "remainder chunks",
            r"""
int[] data = {1, 2, 3, 4, 5};
checkEq(Solution.parallelSum(data, 2), 15L, "remainder goes to earlier chunk");
""",
            "Chunk sizes 3 and 2 — total unchanged.",
        ),
        (
            "more parts than elements",
            r"""
checkEq(Solution.parallelSum(new int[]{7}, 4), 7L, "empty parts contribute 0");
""",
            "Empty chunks sum to 0.",
        ),
        (
            "empty input",
            r"""
checkEq(Solution.parallelSum(new int[]{}, 3), 0L, "empty → 0");
""",
            "Guard clause returns 0.",
        ),
    ],
    level="independent",
)

CH_P9_LATCH = challenge(
    "javi-p9-latch-fanout",
    "Latch-Synchronized Fan-Out",
    r"""Implement `static List<String> fanOut(int n)`:
- create a `CountDownLatch(n)` and a thread-safe list
  (`Collections.synchronizedList` or `CopyOnWriteArrayList`)
- start n threads; each appends `"t" + its_index` to the list, then
  counts down the latch
- the main thread awaits the latch, SORTS the list, and returns it

Every returned list must contain exactly `t0..t(n-1)` — the latch
guarantees completion before the read. n <= 0 returns an empty list.""",
    P9_BOILER,
    [
        (
            "all workers complete",
            r"""
List<String> out = Solution.fanOut(5);
checkEq(out.size(), 5, "five results");
checkEq(out, List.of("t0", "t1", "t2", "t3", "t4"), "sorted complete set");
""",
            "The latch + sort makes the result deterministic.",
        ),
        (
            "single worker",
            r"""
checkEq(Solution.fanOut(1), List.of("t0"), "one result");
""",
            "n=1 edge.",
        ),
        (
            "zero or negative",
            r"""
checkEq(Solution.fanOut(0), List.of(), "zero → empty");
""",
            "n <= 0 → empty list.",
        ),
    ],
    level="independent",
)

VI_CH_P9_COUNTER = vi_challenge(
    "Bộ đếm an toàn luồng",
    r"""Cài bên trong `Solution`:
- `static class RacyCounter` với `void inc()` (`count++` trên field
  thường) và `long value()`.
- `static class SafeCounter` cùng API nhưng dùng `AtomicLong` làm điểm
  tựa.
- `static long hammer(Object counter, int threads, int perThread)`:
  khởi động `threads` thread, mỗi thread gọi `inc()` perThread lần qua
  reflection (RacyCounter hoặc SafeCounter), join chúng, rồi trả
  `value()` qua reflection.

Với hammer(c, 4, 1000): RacyCounter thường mất cập nhật (< 4000);
SafeCounter phải LUÔN trả đúng 4000. Test an toàn chạy hammer năm lần
để làm lộ tính chập chờn.""",
    [
        ("Bộ đếm an toàn chính xác dưới contention", "Đọc-sửa-ghi của AtomicLong không bao giờ mất cập nhật."),
        ("Bộ đếm racy tồn tại (đối chứng)", "Bản racy vẫn chạy nhưng không được bảo đảm chính xác — đó chính là bài học."),
    ],
)

VI_CH_P9_PARALLEL = vi_challenge(
    "Tổng song song xác định",
    r"""Cài `static long parallelSum(int[] data, int parts)`:
- chia mảng thành `parts` đoạn liền kề (phần dư chia cho các đoạn đầu)
- tính tổng từng đoạn trên thread riêng (Thread + join() thuần là đủ)
- gộp và trả tổng

Sau khi join, bước gộp là xác định — cạnh happens-before đó chính là bài
tập. Mảng rỗng hoặc parts <= 0 → 0.""",
    [
        ("Chia đều", "Mỗi đoạn tổng 2 phần tử: tổng 36."),
        ("Đoạn có phần dư", "Kích thước đoạn 3 và 2 — tổng không đổi."),
        ("Nhiều đoạn hơn phần tử", "Đoạn rỗng cộng vào 0."),
        ("Input rỗng", "Guard clause trả 0."),
    ],
)

VI_CH_P9_LATCH = vi_challenge(
    "Fan-Out đồng bộ bằng latch",
    r"""Cài `static List<String> fanOut(int n)`:
- tạo `CountDownLatch(n)` và một list an toàn luồng
  (`Collections.synchronizedList` hoặc `CopyOnWriteArrayList`)
- khởi động n thread; mỗi thread nối `"t" + index_của_nó` vào list, rồi
  countDown latch
- thread chính await latch, SORT list, rồi trả về

Mỗi list trả về phải chứa đúng `t0..t(n-1)` — latch bảo đảm hoàn tất
trước khi đọc. n <= 0 trả list rỗng.""",
    [
        ("Mọi worker hoàn tất", "Latch + sort khiến kết quả xác định."),
        ("Một worker", "Biên n=1."),
        ("Không hoặc âm", "n <= 0 → list rỗng."),
    ],
)

write_practice(
    MOD,
    "javi-p9-concurrency",
    "Concurrency Lab",
    "Prove the atomic fix under contention, parallel sums that rejoin deterministically, and latch-synchronized fan-out.",
    "Xưởng concurrency",
    "Chứng minh bản vá atomic dưới contention, tổng song song rejoin xác định, và fan-out đồng bộ latch.",
    "executors-futures",
    40,
    "intermediate",
    [CH_P9_COUNTER, CH_P9_PARALLEL, CH_P9_LATCH],
    {CH_P9_COUNTER["id"]: VI_CH_P9_COUNTER, CH_P9_PARALLEL["id"]: VI_CH_P9_PARALLEL, CH_P9_LATCH["id"]: VI_CH_P9_LATCH},
    solutions=[
        (
            CH_P9_COUNTER["id"],
            r"""
import java.lang.reflect.*;
import java.util.concurrent.atomic.*;

public class Solution {
    public static class RacyCounter {
        long count = 0;
        public void inc() { count++; }
        public long value() { return count; }
    }

    public static class SafeCounter {
        private final AtomicLong count = new AtomicLong();
        public void inc() { count.incrementAndGet(); }
        public long value() { return count.get(); }
    }

    public static long hammer(Object counter, int threads, int perThread) throws Exception {
        Thread[] ts = new Thread[threads];
        for (int i = 0; i < threads; i++) {
            ts[i] = new Thread(() -> {
                try {
                    Method inc = counter.getClass().getMethod("inc");
                    for (int j = 0; j < perThread; j++) inc.invoke(counter);
                } catch (Exception e) { throw new RuntimeException(e); }
            });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        Method value = counter.getClass().getMethod("value");
        return (Long) value.invoke(counter);
    }
}
""",
            r"""
import java.lang.reflect.*;
import java.util.concurrent.atomic.*;

public class Solution {
    public static class RacyCounter {
        long count = 0;
        public void inc() { count++; }
        public long value() { return count; }
    }

    public static class SafeCounter {
        private final AtomicLong count = new AtomicLong();
        // W: get-then-set is two atomic ops, not one — under contention
        // two threads read the same value and one increment is lost.
        public void inc() { count.set(count.get() + 1); }
        public long value() { return count.get(); }
    }

    public static long hammer(Object counter, int threads, int perThread) throws Exception {
        Thread[] ts = new Thread[threads];
        for (int i = 0; i < threads; i++) {
            ts[i] = new Thread(() -> {
                try {
                    Method inc = counter.getClass().getMethod("inc");
                    for (int j = 0; j < perThread; j++) inc.invoke(counter);
                } catch (Exception e) { throw new RuntimeException(e); }
            });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        Method value = counter.getClass().getMethod("value");
        return (Long) value.invoke(counter);
    }
}
""",
        ),
        (
            CH_P9_PARALLEL["id"],
            r"""
public class Solution {
    public static long parallelSum(int[] data, int parts) {
        if (data == null || data.length == 0 || parts <= 0) return 0L;
        int n = data.length;
        int base = n / parts, rem = n % parts;
        long[] sums = new long[parts];
        Thread[] ts = new Thread[parts];
        int offset = 0;
        for (int p = 0; p < parts; p++) {
            int len = base + (p < rem ? 1 : 0);
            final int start = offset, end = offset + len;
            final int idx = p;
            ts[p] = new Thread(() -> {
                long s = 0;
                for (int i = start; i < end; i++) s += data[i];
                sums[idx] = s;
            });
            ts[p].start();
            offset += len;
        }
        long total = 0;
        for (int p = 0; p < parts; p++) {
            try { ts[p].join(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            total += sums[p];
        }
        return total;
    }
}
""",
            r"""
public class Solution {
    // W: reads sums[] without joining first — the combine loop races the
    // workers, so totals are often short. The join-before-read edge is
    // exactly what was missing.
    public static long parallelSum(int[] data, int parts) {
        if (data == null || data.length == 0 || parts <= 0) return 0L;
        int n = data.length;
        int base = n / parts, rem = n % parts;
        long[] sums = new long[parts];
        Thread[] ts = new Thread[parts];
        int offset = 0;
        for (int p = 0; p < parts; p++) {
            int len = base + (p < rem ? 1 : 0);
            final int start = offset, end = offset + len;
            final int idx = p;
            ts[p] = new Thread(() -> {
                long s = 0;
                for (int i = start; i < end; i++) s += data[i];
                sums[idx] = s;
            });
            ts[p].start();
            offset += len;
        }
        long total = 0;
        for (int p = 0; p < parts; p++) total += sums[p];
        return total;
    }
}
""",
        ),
        (
            CH_P9_LATCH["id"],
            r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static List<String> fanOut(int n) {
        if (n <= 0) return new ArrayList<>();
        CountDownLatch done = new CountDownLatch(n);
        List<String> out = Collections.synchronizedList(new ArrayList<>());
        for (int i = 0; i < n; i++) {
            final int idx = i;
            new Thread(() -> {
                out.add("t" + idx);
                done.countDown();
            }).start();
        }
        try { done.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        Collections.sort(out);
        return out;
    }
}
""",
            r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    // W: awaits a latch that only decrements n-1 times — await() blocks
    // forever and the test times out. Off-by-one in synchronization is a
    // deadlock class of bug.
    public static List<String> fanOut(int n) {
        if (n <= 0) return new ArrayList<>();
        CountDownLatch done = new CountDownLatch(n);
        List<String> out = Collections.synchronizedList(new ArrayList<>());
        for (int i = 0; i < n; i++) {
            final int idx = i;
            new Thread(() -> {
                out.add("t" + idx);
                if (idx > 0) done.countDown();
            }).start();
        }
        try { done.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        Collections.sort(out);
        return out;
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — concurrency

You can now: use joins as happens-before edges, fix races with atomics,
and synchronize completion with latches. Prove it with a parallel word
counter that must return exact totals.
"""

CP_MDX_VI = r"""
## Checkpoint — concurrency

Giờ bạn có thể: dùng join làm cạnh happens-before, sửa race bằng atomic,
và đồng bộ hoàn tất bằng latch. Chứng minh bằng một bộ đếm từ song song
phải trả tổng chính xác.
"""

CH_CP9 = challenge(
    "javi-checkpoint-m9-concurrency",
    "Parallel Word Counter",
    r"""Build `Solution`:
- `static Map<String, Integer> countWords(List<String> chunks, int threads)`:
  - split the chunk list into `threads` sublists (like parallelSum)
  - each thread counts words in its chunks into its OWN local
    `HashMap<String, Integer>`
  - after joining all threads, MERGE the maps into one
  - return the merged map

The merge must happen after every join — before that, thread-local maps
are confined and safe. threads <= 0 → empty map; empty chunks fine.""",
    r"""
import java.util.*;
import java.util.concurrent.atomic.*;

public class Solution {
    // Provide countWords here.
}
""",
    [
        (
            "exact counts across threads",
            r"""
List<String> chunks = List.of("a b", "b c", "c a");
Map<String, Integer> out = Solution.countWords(chunks, 3);
checkEq(out.get("a"), 2, "a count");
checkEq(out.get("b"), 2, "b count");
checkEq(out.get("c"), 2, "c count");
""",
            "Three threads, then merge — totals must be exact.",
        ),
        (
            "chunk order does not matter",
            r"""
List<String> chunks = List.of("x", "x y", "y");
Map<String, Integer> out = Solution.countWords(chunks, 2);
checkEq(out.get("x"), 2, "x");
checkEq(out.get("y"), 2, "y");
""",
            "Same totals regardless of the split.",
        ),
        (
            "guards",
            r"""
checkEq(Solution.countWords(List.of(), 4).size(), 0, "empty input");
checkEq(Solution.countWords(List.of("w"), 0).size(), 0, "no threads");
""",
            "Empty input or threads <= 0 → empty map.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP9 = vi_challenge(
    "Bộ đếm từ song song",
    r"""Xây `Solution`:
- `static Map<String, Integer> countWords(List<String> chunks, int threads)`:
  - chia list chunk thành `threads` sublist (như parallelSum)
  - mỗi thread đếm từ trong các chunk của nó vào một
    `HashMap<String, Integer>` CỤC BỘ riêng
  - sau khi join hết thread, MERGE các map thành một
  - trả map đã merge

Merge phải xảy ra sau mọi join — trước đó, map cục bộ của thread được
giam giữ và an toàn. threads <= 0 → map rỗng; chunk rỗng thì ok.""",
    [
        ("Số đếm chính xác qua các thread", "Ba thread, rồi merge — tổng phải chính xác."),
        ("Thứ tự chunk không quan trọng", "Cùng tổng bất kể cách chia."),
        ("Guard", "Input rỗng hoặc threads <= 0 → map rỗng."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-concurrency",
    "Checkpoint: Concurrency",
    "Graded checkpoint: thread-local counting with a post-join merge — exact totals, no shared mutable maps.",
    15,
    CP_MDX,
    "Checkpoint: Concurrency",
    "Checkpoint chấm điểm: đếm cục bộ theo thread với merge sau join — tổng chính xác, không map khả biến dùng chung.",
    CP_MDX_VI,
    CH_CP9,
    VI_CH_CP9,
    solution=r"""
import java.util.*;

public class Solution {
    public static Map<String, Integer> countWords(List<String> chunks, int threads) {
        Map<String, Integer> out = new HashMap<>();
        if (chunks == null || chunks.isEmpty() || threads <= 0) return out;
        int n = chunks.size();
        int t = Math.min(threads, n);
        int base = n / t, rem = n % t;
        List<Map<String, Integer>> locals = new ArrayList<>();
        Thread[] ts = new Thread[t];
        int offset = 0;
        for (int i = 0; i < t; i++) {
            int len = base + (i < rem ? 1 : 0);
            final int start = offset, end = offset + len;
            locals.add(new HashMap<>());
            final Map<String, Integer> local = locals.get(i);
            ts[i] = new Thread(() -> {
                for (int c = start; c < end; c++) {
                    for (String w : chunks.get(c).split("\\s+")) {
                        local.merge(w, 1, Integer::sum);
                    }
                }
            });
            ts[i].start();
            offset += len;
        }
        for (Thread th : ts) {
            try { th.join(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
        for (Map<String, Integer> local : locals)
            local.forEach((k, v) -> out.merge(k, v, Integer::sum));
        return out;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    // W: the final merge uses put() instead of merge-with-sum — when two
    // thread-local maps share a key, the second OVERWRITES the first
    // instead of adding. Deterministic loss whenever a word spans chunks.
    public static Map<String, Integer> countWords(List<String> chunks, int threads) {
        Map<String, Integer> out = new HashMap<>();
        if (chunks == null || chunks.isEmpty() || threads <= 0) return out;
        int n = chunks.size();
        int t = Math.min(threads, n);
        int base = n / t, rem = n % t;
        List<Map<String, Integer>> locals = new ArrayList<>();
        Thread[] ts = new Thread[t];
        int offset = 0;
        for (int i = 0; i < t; i++) {
            int len = base + (i < rem ? 1 : 0);
            final int start = offset, end = offset + len;
            locals.add(new HashMap<>());
            final Map<String, Integer> local = locals.get(i);
            ts[i] = new Thread(() -> {
                for (int c = start; c < end; c++) {
                    for (String w : chunks.get(c).split("\\s+")) {
                        local.merge(w, 1, Integer::sum);
                    }
                }
            });
            ts[i].start();
            offset += len;
        }
        for (Thread th : ts) {
            try { th.join(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
        for (Map<String, Integer> local : locals) out.putAll(local);
        return out;
    }
}
""",
)
