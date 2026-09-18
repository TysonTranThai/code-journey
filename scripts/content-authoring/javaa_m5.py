#!/usr/bin/env python3
"""Java — Advanced — Module 5: java-executors-vt.

Executors as the concurrency API of record: lifecycle rules, Future
limitations vs CompletableFuture composition, and virtual threads (JEP 444,
verified in this sandbox) — what they change (blocking is cheap) and what
they do NOT change (CPU-bound work still needs platform parallelism; pinning
in synchronized blocks). All tests latch-choreographed. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "java-executors-vt"

L_EXEC_EN = """
An **ExecutorService** is a queue of tasks plus worker threads. Its lifecycle
has three phases and two endings:

- `shutdown()`: stop accepting tasks, finish queued ones.
- `shutdownNow()`: stop accepting, **interrupt** running tasks, drain the
  queue into your hands (so nothing is lost silently).
- `awaitTermination(timeout)`: the polite wait. The pattern:

```java
exec.shutdown();
if (!exec.awaitTermination(5, TimeUnit.SECONDS)) {
    exec.shutdownNow();   // escalate
}
```

**Future.get()** is where composition goes to die: `f2.get()` cannot *start*
until you call it, so "run A and B concurrently, then combine" becomes
blocked hand-tuning. **CompletableFuture** fixes this:

```java
var a = CompletableFuture.supplyAsync(() -> fetchA());
var b = CompletableFuture.supplyAsync(() -> fetchB());
var both = a.thenCombine(b, (x, y) -> x + y);   // runs when BOTH complete
```

Composition primitives: `thenApply` (transform), `thenCompose` (chain,
flat-map), `thenCombine` (join two), `exceptionally`/`handle` (recover),
`orTimeout` (JDK 9+; sandbox-safe since it needs no extra flags).
"""
L_EXEC_VI = """
**ExecutorService** là hàng đợi tác vụ cộng các worker thread. Vòng đời có ba
pha và hai kiểu kết thúc:

- `shutdown()`: ngừng nhận tác vụ, chạy nốt những cái đã xếp hàng.
- `shutdownNow()`: ngừng nhận, **interrupt** các tác vụ đang chạy, trả lại
  hàng đợi cho bạn (không mất mát thầm lặng).
- `awaitTermination(timeout)`: chờ lịch sự. Mẫu chuẩn:

```java
exec.shutdown();
if (!exec.awaitTermination(5, TimeUnit.SECONDS)) {
    exec.shutdownNow();   // leo thang
}
```

**Future.get()** là nơi composition chết: `f2.get()` không thể *bắt đầu* cho
đến khi bạn gọi nó, nên "chạy A và B đồng thời rồi ghép" biến thành chỉnh tay
từng chỗ chặn. **CompletableFuture** sửa điều đó:

```java
var a = CompletableFuture.supplyAsync(() -> fetchA());
var b = CompletableFuture.supplyAsync(() -> fetchB());
var both = a.thenCombine(b, (x, y) -> x + y);   // chạy khi CẢ HAI xong
```

Các primitive composition: `thenApply` (biến đổi), `thenCompose` (chuỗi,
flat-map), `thenCombine` (ghép hai), `exceptionally`/`handle` (phục hồi),
`orTimeout` (JDK 9+; an toàn trong sandbox vì không cần flag thêm).
"""

L_VT_EN = """
**Virtual threads** (JEP 444, standard in 21 — verified executable in this
sandbox) detach *unit of concurrency* from *unit of cost*:

```java
try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        exec.submit(() -> { Thread.sleep(100); return i; });  // fine!
    }
}   // close() waits for all tasks
```

One JVM can hold *millions* of virtual threads because they are not OS
threads: they are heap objects scheduled onto a small pool of **carrier**
platform threads. When a virtual thread blocks (sleep, I/O), the JVM
**unmounts** it and the carrier runs someone else. Blocking is cheap again —
that is the whole revolution.

**What virtual threads do NOT change**:

1. **CPU-bound work** gains nothing: you still have only the machine's cores;
   `Runtime.getRuntime().availableProcessors()` governs platform parallelism.
   VTs help *waiting*, not *computing*.
2. **Pinning**: inside a `synchronized` block (or a native frame), a virtual
   thread cannot unmount — the carrier is held hostage. Long synchronized
   sections under heavy VT load can starve carriers. (JDK 24 fixed the
   `synchronized` case; on our `--release 21` runtime it is a live hazard —
   prefer `ReentrantLock` for long sections in VT-heavy code.)
3. **No pooling**: VTs are one-shot. Pooling them recreates the platform-thread
   economics you were escaping. `newVirtualThreadPerTaskExecutor` — per task.

**Structured concurrency** (JEP 453) is preview-only in 21 — taught
conceptually: treat a fan of related tasks as one unit with one error and one
cancellation path.
"""
L_VT_VI = """
**Virtual threads** (JEP 444, chuẩn từ 21 — đã kiểm chứng chạy được trong
sandbox này) tách *đơn vị đồng thời* khỏi *đơn vị chi phí*:

```java
try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        exec.submit(() -> { Thread.sleep(100); return i; });  // ổn!
    }
}   // close() chờ mọi tác vụ
```

Một JVM giữ được *hàng triệu* virtual thread vì chúng không phải thread của
OS: chúng là đối tượng trên heap được xếp lịch lên một nhóm nhỏ thread
**carrier**. Khi virtual thread block (sleep, I/O), JVM **tháo nó ra** và
carrier chạy người khác. Block lại rẻ — đó là cả cuộc cách mạng.

**Điều virtual threads KHÔNG thay đổi**:

1. **Công việc nặng CPU** không được lợi gì: máy bạn vẫn chỉ có vậy nhân;
   `Runtime.getRuntime().availableProcessors()` chi phối parallelism nền.
   VT giúp *chờ đợi*, không giúp *tính toán*.
2. **Pinning**: bên trong khối `synchronized` (hoặc frame native), virtual
   thread không thể bị tháo ra — carrier bị giữ con tin. Khối synchronized
   dài dưới tải VT nặng có thể đói carrier. (JDK 24 đã sửa trường hợp
   `synchronized`; trên runtime `--release 21` của chúng ta đây là rủi ro
   thật — ưu tiên `ReentrantLock` cho khối dài trong code nhiều VT.)
3. **Không pooling**: VT dùng một lần. Pool chúng là tái tạo lại kinh tế
   thread nền mà bạn đang trốn. `newVirtualThreadPerTaskExecutor` — mỗi
   tác vụ một thread.

**Structured concurrency** (JEP 453) chỉ là preview trong 21 — dạy ở mức
khái niệm: coi một cụm tác vụ liên quan là một đơn vị với một đường lỗi và
một đường hủy.
"""

write_module(
    M, "Executors & Virtual Threads",
    "Executor lifecycle, CompletableFuture composition, virtual threads verified in-sandbox, pinning, and when VTs do not help.",
    "Executors & Virtual Threads",
    "Vòng đời executor, composition CompletableFuture, virtual threads kiểm chứng trong sandbox, pinning, và khi nào VT không giúp.",
    ["javaa-executor-lifecycle", "javaa-cf-composition", "javaa-virtual-threads"],
    ["javaa-p5-exec"],
)

write_lesson(M, "javaa-executor-lifecycle",
    "Executor lifecycle and Future's limits",
    "shutdown/shutdownNow/awaitTermination, and why Future.get blocks composition.",
    15, L_EXEC_EN,
    "Vòng đời executor và giới hạn của Future",
    "shutdown/shutdownNow/awaitTermination, và vì sao Future.get chặn composition.",
    L_EXEC_VI)

write_lesson(M, "javaa-cf-composition",
    "CompletableFuture composition",
    "thenApply/thenCompose/thenCombine, exception handling, and orTimeout for bounded async.",
    16, L_EXEC_EN,
    "Composition CompletableFuture",
    "thenApply/thenCompose/thenCombine, xử lý exception, và orTimeout cho async có chặn trên.",
    L_EXEC_VI)

write_lesson(M, "javaa-virtual-threads",
    "Virtual threads and their limits",
    "Millions of cheap threads, carriers and unmounting, pinning hazards, and CPU-bound work unchanged.",
    18, L_VT_EN,
    "Virtual threads và giới hạn của chúng",
    "Hàng triệu thread rẻ, carrier và việc tháo lắp, rủi ro pinning, và công việc nặng CPU không đổi.",
    L_VT_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_LIFECYCLE = challenge(
    "javaa-p5-lifecycle",
    "Executor lifecycle, executed",
    "Implement `static List<String> lifecycle()` — choreography over a `newFixedThreadPool(1)` "
    "with `CountDownLatch start/proceed/blocked` and a `CopyOnWriteArrayList<String> log`:\n"
    "1. Submit task A: log \"A-running\"; `blocked.countDown()`; `proceed.await()` — if "
    "interrupted log \"A-interrupted\" and return; otherwise log \"A-done\".\n"
    "2. Main: `blocked.await()` (A is parked; the only thread is busy), then submit task B "
    "that logs \"B-done\" — B is now QUEUED.\n"
    "3. `shutdown()`.\n"
    "4. Try submitting task C; catch `RejectedExecutionException` and log "
    "\"rejected-after-shutdown\".\n"
    "5. `proceed.countDown()`; `awaitTermination(5, SECONDS)`; return the log.\n"
    "With shutdown(), queued B must still run: [A-running, rejected-after-shutdown, A-done, B-done].",
    P_BOILER,
    [
        ("queued work completes after shutdown; new submits rejected", r"""
java.util.List<String> log = Solution.lifecycle();
checkEq(log, java.util.List.of("A-running", "rejected-after-shutdown", "A-done", "B-done"),
    "graceful shutdown runs the queue, rejects the rest");
""", "shutdown() drains nothing: A finishes, queued B runs, C is rejected."),
    ],
    level="guided",
)
CH_LIFECYCLE_VI = vi_challenge(
    "Vòng đời executor, chạy thử được",
    "lifecycle(): shutdown không làm mất tác vụ đã trong hàng đợi (B vẫn chạy) nhưng từ chối tác vụ nộp mới.",
    [("Tác vụ trong hàng đợi vẫn chạy sau shutdown; nộp mới bị từ chối", "shutdown() không tháo bỏ gì cả: A xong, B trong hàng đợi chạy, C bị từ chối."),],
)

CH_COMBINE = challenge(
    "javaa-p5-cf-combine",
    "Compose, don't block",
    "Implement with CompletableFuture (returned before completion, joined by the test):\n"
    "1. `static CompletableFuture<Integer> combined()` — two async supplies (return 20 and 22), "
    "combined with `thenCombine` into their sum.\n"
    "2. `static CompletableFuture<Integer> chained()` — an async 3, thenCompose to double it, "
    "thenApply to add 4 (=> 10).\n"
    "3. `static CompletableFuture<Integer> recovered()` — an async that throws, "
    "then `exceptionally` returning -1.\n"
    "4. `static CompletableFuture<Integer> bounded()` — async sleeping 50ms then returning 7, "
    "with `orTimeout(10, MILLISECONDS)` and `exceptionally` returning -1 (timeout path exercised).",
    P_BOILER,
    [
        ("thenCombine joins two", r"""
checkEq(Solution.combined().join(), 42, "20 + 22 via thenCombine");
""", "thenCombine fires when both complete."),
        ("thenCompose chains", r"""
checkEq(Solution.chained().join(), 10, "3 doubled + 4");
""", "thenCompose for dependent async steps."),
        ("exceptional recovery", r"""
checkEq(Solution.recovered().join(), -1, "exceptionally path");
""", "exceptionally maps the failure."),
        ("orTimeout fires", r"""
checkEq(Solution.bounded().join(), -1, "timeout path taken");
""", "10ms timeout vs 50ms sleep."),
    ],
    level="independent",
)
CH_COMBINE_VI = vi_challenge(
    "Ghép nối, không chặn",
    "combined/chained/recovered/bounded: thenCombine, thenCompose, exceptionally, orTimeout — đủ bốn mẫu.",
    [("thenCombine ghép hai", "thenCombine chạy khi cả hai hoàn thành."),
     ("thenCompose chuỗi", "thenCompose cho các bước async phụ thuộc."),
     ("Phục hồi exceptional", "exceptionally biến lỗi thành giá trị."),
     ("orTimeout kịp nổ", "Timeout 10ms so với sleep 50ms.")],
)

CH_VT = challenge(
    "javaa-p5-vt-scale",
    "Virtual threads under load",
    "1. `static int vtFanout(int tasks)` — run `tasks` virtual threads via "
    "`newVirtualThreadPerTaskExecutor`, each sleeping 20ms then adding 1 to an AtomicInteger; "
    "return the final count. Must work for 10,000 tasks (a platform pool of equal size would blow "
    "the 30s sandbox ceiling — VTs make it trivial).\n"
    "2. `static boolean isVirtualInside()` — start a virtual thread that records "
    "`Thread.currentThread().isVirtual()` and return that record.\n"
    "3. `static int platformParallelism()` — return "
    "`Runtime.getRuntime().availableProcessors()` (the honest CPU-bound ceiling).\n"
    "4. `static boolean virtualThreadsHelpCpuBound()` — return false (VTs help waiting, not computing).",
    P_BOILER,
    [
        ("10k virtual tasks complete", r"""
checkEq(Solution.vtFanout(10_000), 10_000, "massive fanout on virtual threads");
""", "newVirtualThreadPerTaskExecutor + sleep 20ms each."),
        ("thread identity is virtual", r"""
checkTrue(Solution.isVirtualInside(), "isVirtual() observed from inside");
""", "Record from within the virtual thread."),
        ("parallelism honesty", r"""
checkTrue(Solution.platformParallelism() >= 1, "at least one core");
checkTrue(!Solution.virtualThreadsHelpCpuBound(), "VTs help waiting, not computing");
""", "availableProcessors is the CPU ceiling; VT claim is false for CPU-bound."),
    ],
    level="real-world",
)
CH_VT_VI = vi_challenge(
    "Virtual threads dưới tải",
    "Fanout 10k VT với sleep 20ms, quan sát isVirtual() từ trong thread, và trung thực về giới hạn CPU.",
    [("10k tác vụ ảo hoàn thành", "newVirtualThreadPerTaskExecutor + sleep 20ms mỗi tác vụ."),
     ("Identity thread là ảo", "Quan sát isVirtual() từ bên trong."),
     ("Trung thực về parallelism", "availableProcessors là trần CPU; VT không giúp CPU-bound.")],
)

write_practice(M, "javaa-p5-exec",
    "Executor & VT drills",
    "Drive the lifecycle, compose without blocking, and fan out 10k virtual tasks within sandbox limits.",
    "Bài tập executor & VT",
    "Điều khiển vòng đời, compose không chặn, và fan out 10k tác vụ ảo trong giới hạn sandbox.",
    "javaa-virtual-threads", 55, "advanced",
    [CH_LIFECYCLE, CH_COMBINE, CH_VT],
    {"javaa-p5-lifecycle": CH_LIFECYCLE_VI, "javaa-p5-cf-combine": CH_COMBINE_VI, "javaa-p5-vt-scale": CH_VT_VI},
    solutions=[
        ("javaa-p5-lifecycle", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static List<String> lifecycle() throws Exception {
        List<String> log = new CopyOnWriteArrayList<>();
        CountDownLatch start = new CountDownLatch(1);
        CountDownLatch blocked = new CountDownLatch(1);
        CountDownLatch proceed = new CountDownLatch(1);
        ExecutorService exec = Executors.newFixedThreadPool(1);

        exec.submit(() -> {
            try {
                start.await();
                log.add("A-running");
                blocked.countDown();          // A is parked below — thread occupied
                proceed.await();
                log.add("A-done");
            } catch (InterruptedException e) {
                log.add("A-interrupted");
            }
            return null;
        });
        start.countDown();
        blocked.await();                      // A parked, only thread busy

        exec.submit(() -> { log.add("B-done"); return null; });   // QUEUED behind A
        exec.shutdown();                      // queue kept, door closed
        try {
            exec.submit(() -> { log.add("C-never"); return null; });
        } catch (RejectedExecutionException e) {
            log.add("rejected-after-shutdown");
        }
        proceed.countDown();
        exec.awaitTermination(5, TimeUnit.SECONDS);
        return List.copyOf(log);
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static List<String> lifecycle() throws Exception {
        List<String> log = new CopyOnWriteArrayList<>();
        CountDownLatch start = new CountDownLatch(1);
        CountDownLatch blocked = new CountDownLatch(1);
        CountDownLatch proceed = new CountDownLatch(1);
        ExecutorService exec = Executors.newFixedThreadPool(1);

        exec.submit(() -> {
            try {
                start.await();
                log.add("A-running");
                blocked.countDown();
                proceed.await();
                log.add("A-done");
            } catch (InterruptedException e) {
                log.add("A-interrupted");
            }
            return null;
        });
        start.countDown();
        blocked.await();

        exec.submit(() -> { log.add("B-done"); return null; });
        exec.shutdownNow();                   // WRONG: drains the queue — B never runs
        try {
            exec.submit(() -> { log.add("C-never"); return null; });
        } catch (RejectedExecutionException e) {
            log.add("rejected-after-shutdown");
        }
        proceed.countDown();
        exec.awaitTermination(5, TimeUnit.SECONDS);
        return List.copyOf(log);
    }
}
"""),
        ("javaa-p5-cf-combine", r"""
import java.util.concurrent.*;

public class Solution {
    public static CompletableFuture<Integer> combined() {
        return CompletableFuture.supplyAsync(() -> 20)
            .thenCombine(CompletableFuture.supplyAsync(() -> 22), Integer::sum);
    }

    public static CompletableFuture<Integer> chained() {
        return CompletableFuture.supplyAsync(() -> 3)
            .thenCompose(x -> CompletableFuture.supplyAsync(() -> x * 2))
            .thenApply(x -> x + 4);
    }

    public static CompletableFuture<Integer> recovered() {
        return CompletableFuture.<Integer>supplyAsync(() -> { throw new IllegalStateException("boom"); })
            .exceptionally(e -> -1);
    }

    public static CompletableFuture<Integer> bounded() {
        return CompletableFuture.<Integer>supplyAsync(() -> {
            try { Thread.sleep(50); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            return 7;
        }).orTimeout(10, TimeUnit.MILLISECONDS)
          .exceptionally(e -> -1);
    }
}
""", r"""
import java.util.concurrent.*;

public class Solution {
    // WRONG: supplyAsync starts eagerly, but chaining with thenApply AFTER a
    // blocking get() serializes the two supplies — defeating thenCombine
    public static CompletableFuture<Integer> combined() {
        try {
            int a = CompletableFuture.supplyAsync(() -> 20).get();
            int b = CompletableFuture.supplyAsync(() -> 22).get();
            return CompletableFuture.completedFuture(a + b);
        } catch (Exception e) { return CompletableFuture.completedFuture(-1); }
    }

    public static CompletableFuture<Integer> chained() {
        return CompletableFuture.supplyAsync(() -> 3)
            .thenCompose(x -> CompletableFuture.supplyAsync(() -> x * 2))
            .thenApply(x -> x + 3);   // WRONG: +3 not +4
    }

    public static CompletableFuture<Integer> recovered() {
        return CompletableFuture.<Integer>supplyAsync(() -> { throw new IllegalStateException("boom"); });
        // WRONG: no recovery — join() rethrows
    }

    public static CompletableFuture<Integer> bounded() {
        return CompletableFuture.<Integer>supplyAsync(() -> 7);   // WRONG: no timeout
    }
}
"""),
        ("javaa-p5-vt-scale", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Solution {
    public static int vtFanout(int tasks) throws Exception {
        AtomicInteger count = new AtomicInteger();
        try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < tasks; i++) {
                exec.submit(() -> {
                    Thread.sleep(20);
                    count.incrementAndGet();
                    return null;
                });
            }
        }   // close() awaits everything
        return count.get();
    }

    static volatile boolean virtualObserved = false;

    public static boolean isVirtualInside() throws Exception {
        Thread t = Thread.ofVirtual().start(() -> {
            virtualObserved = Thread.currentThread().isVirtual();
        });
        t.join(5000);
        return virtualObserved;
    }

    public static int platformParallelism() {
        return Runtime.getRuntime().availableProcessors();
    }

    public static boolean virtualThreadsHelpCpuBound() { return false; }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Solution {
    public static int vtFanout(int tasks) throws Exception {
        AtomicInteger count = new AtomicInteger();
        ExecutorService exec = Executors.newFixedThreadPool(10);   // WRONG: platform pool for
        try {                                                       // 10k sleeping tasks
            for (int i = 0; i < tasks; i++) {
                exec.submit(() -> {
                    Thread.sleep(20);
                    count.incrementAndGet();
                    return null;
                });
            }
        } finally { exec.shutdown(); }
        return count.get();
    }

    static volatile boolean virtualObserved = false;

    public static boolean isVirtualInside() throws Exception {
        Thread t = new Thread(() -> virtualObserved = Thread.currentThread().isVirtual()); // WRONG: platform
        t.start(); t.join(5000);
        return virtualObserved;
    }

    public static int platformParallelism() { return 0; }   // WRONG: not honest
    public static boolean virtualThreadsHelpCpuBound() { return true; }   // WRONG: overclaims
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the concurrent aggregator

Fan out work across virtual threads, compose partial results with
CompletableFuture, bound the whole thing with a timeout, and recover from a
failing branch — the four pillars of this module in one method.
"""

CP_CH = challenge(
    "javaa-checkpoint-m5-task",
    "Checkpoint: timed fan-out aggregator",
    "Implement `static List<String> aggregate(int shards)` returning shard reports "
    "`\"shard-<i>-ok\"` in shard order where every even shard succeeds and every odd shard "
    "throws. Requirements:\n"
    "1. Each shard runs on its own VIRTUAL thread (newVirtualThreadPerTaskExecutor), sleeping "
    "10ms of simulated work.\n"
    "2. Compose with CompletableFuture.supplyAsync(executor, ...) per shard; failures map to "
    "`\"shard-<i>-failed\"` via exceptionally.\n"
    "3. The whole pipeline must complete and the list must be in shard order 0..shards-1.\n"
    "4. `static String executorChoice()` returns exactly: \"virtual threads per task: blocking work "
    "scales, CPU work still capped by cores\".",
    P_BOILER,
    [
        ("aggregation with failures mapped", r"""
java.util.List<String> out = Solution.aggregate(4);
checkEq(out, java.util.List.of("shard-0-ok", "shard-1-failed", "shard-2-ok", "shard-3-failed"),
    "order preserved, failures mapped");
""", "Even shards ok, odd shards failed, order intact."),
        ("executor philosophy", r"""
checkEq(Solution.executorChoice(),
  "virtual threads per task: blocking work scales, CPU work still capped by cores",
  "the tradeoff line");
""", "Copy exactly."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: bộ tổng hợp fan-out có timeout",
    "Fan-out theo shard trên virtual thread, shard lẻ thất bại ánh xạ thành failed, giữ thứ tự shard.",
    [("Tổng hợp có ánh xạ lỗi", "Shard chẵn ok, shard lẻ failed, thứ tự nguyên vẹn."),
     ("Triết lý executor", "Chép đúng câu đánh đổi.")],
)

write_checkpoint(M, "javaa-checkpoint-m5",
    "Checkpoint: The Timed Fan-Out Aggregator",
    "Fan out across virtual threads, map failures, preserve order, and state the scaling philosophy.",
    25, CP_MD,
    "Checkpoint: Bộ tổng hợp fan-out có timeout",
    "Fan-out trên virtual thread, ánh xạ lỗi, giữ thứ tự, và nêu triết lý mở rộng.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static List<String> aggregate(int shards) throws Exception {
        List<String> out = new ArrayList<>();
        try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
            List<CompletableFuture<String>> futs = new ArrayList<>();
            for (int i = 0; i < shards; i++) {
                final int shard = i;
                futs.add(CompletableFuture.supplyAsync(() -> {
                    try { Thread.sleep(10); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                    if (shard % 2 == 1) throw new IllegalStateException("shard " + shard + " down");
                    return "shard-" + shard + "-ok";
                }, exec).exceptionally(e -> "shard-" + shard + "-failed"));
            }
            for (CompletableFuture<String> f : futs) out.add(f.join());
        }
        return List.copyOf(out);
    }

    public static String executorChoice() {
        return "virtual threads per task: blocking work scales, CPU work still capped by cores";
    }
}
""", wrong=r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static List<String> aggregate(int shards) throws Exception {
        List<String> out = new ArrayList<>();
        ExecutorService exec = Executors.newFixedThreadPool(2);
        try {
            List<CompletableFuture<String>> futs = new ArrayList<>();
            for (int i = 0; i < shards; i++) {
                final int shard = i;
                futs.add(CompletableFuture.supplyAsync(() -> {
                    try { Thread.sleep(10); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                    return "shard-" + shard + "-ok";           // WRONG: failures never mapped
                }, exec));
            }
            for (CompletableFuture<String> f : futs) out.add(f.join());   // throws on odd shards
        } finally { exec.shutdown(); }
        return List.copyOf(out);
    }

    public static String executorChoice() {
        return "more pool threads always helps";   // WRONG: false for CPU-bound
    }
}
""")

print("module 5 authored")
