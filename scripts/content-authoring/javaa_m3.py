#!/usr/bin/env python3
"""Java — Advanced — Module 3: java-memory-model.

The JMM taught with determinism by PROTOCOL, not by timing luck: every
concurrent test is a latch-choreographed scenario with a guaranteed
happens-before edge, so both the reference and the wrong solution run
deterministically. Lessons: visibility vs atomicity, volatile semantics
(JLS §17.4), safe publication, and the final-field guarantee (§17.5).
House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "java-memory-model"

L_HB_EN = """
The Java Memory Model (JLS §17.4) defines **happens-before** — the only
arrow that matters when threads share data. If action A happens-before B,
B sees A's effects. Without that edge, **visibility is not guaranteed**:
a plain boolean written by another thread may never be seen by your loop.

Three hb edges you can build on:

1. **Program order** within one thread.
2. **Monitor rules**: unlock happens-before every later lock of the same
   monitor; every method of a `java.util.concurrent` lock does the same.
3. **Volatile**: a write to a volatile field happens-before every later read
   of that field.

And two structural edges you get for free:

4. **Thread.start()** happens-before anything the new thread does.
5. Everything a thread does happens-before **join()** detects its exit.

The classic broken pattern — a busy flag:

```java
class Stop {
    private static boolean run = true;          // NOT volatile
    static void stop() { run = false; }         // may never be visible
    static void loop() { while (run) {} }       // may spin forever
}
```

This is not pedantry: JIT-tier compilers may hoist the read out of the loop
because *nothing in the model forces them to re-read*.
"""
L_HB_VI = """
Java Memory Model (JLS §17.4) định nghĩa **happens-before** — mũi tên duy
nhất quan trọng khi các thread chia sẻ dữ liệu. Nếu A happens-before B, B
nhìn thấy hiệu ứng của A. Không có mũi tên đó, **visibility không được bảo
đảm**: một boolean thường do thread khác ghi có thể không bao giờ được loop
của bạn nhìn thấy.

Ba cạnh hb bạn có thể dựa vào:

1. **Program order** trong cùng một thread.
2. **Quy tắc monitor**: unlock happens-before mọi lần lock sau trên cùng
   monitor; mọi phương thức của lock `java.util.concurrent` cũng vậy.
3. **Volatile**: ghi vào trường volatile happens-before mọi lần đọc sau
   trường đó.

Và hai cạnh cấu trúc miễn phí:

4. **Thread.start()** happens-before mọi việc thread mới làm.
5. Mọi việc một thread làm happens-before **join()** phát hiện nó kết thúc.

Mẫu code hỏng kinh điển — cờ dừng:

```java
class Stop {
    private static boolean run = true;          // KHÔNG volatile
    static void stop() { run = false; }         // có thể không bao giờ hiển thị
    static void loop() { while (run) {} }       // có thể quay mãi
}
```

Đây không là đạo đức giả: compiler tầng JIT có thể kéo phép đọc ra khỏi vòng
lặp vì *không gì trong mô hình buộc nó đọc lại*.
"""

L_VOLATILE_EN = """
`volatile` gives you exactly two things — and not a third:

1. **Visibility**: every read sees the latest write (hb edge per access).
2. **Ordering**: the compiler/CPU may not reorder volatile accesses with each
   other in observable ways.

What volatile does NOT give: **atomicity of compound actions**.
`volatile int n; n++` is still a read-modify-write race — two threads can
both read 5 and both write 6, losing an increment. That is what
`AtomicInteger` (CAS) is for — next module.

**Safe publication** (§17.4.4): to hand an object to another thread safely,
publish it through a channel that carries an hb edge — a volatile field, a
`BlockingQueue`, an executor submit, or a properly synchronized structure.
If you construct an object and store it in a plain static field, another
thread may see a *partially constructed* object (fields default-valued or
stale).

**Final-field semantics** (§17.5): if an object is *properly constructed*
(no `this` escape), every thread that gets a reference to it sees the final
fields fully initialized — even without synchronization. This guarantee is
why `String` is safe to share freely, and why leaking `this` from a
constructor is not just ugly but a *correctness* bug: it can break the
final-field guarantee.
"""
L_VOLATILE_VI = """
`volatile` cho bạn đúng hai thứ — và không cho thứ thứ ba:

1. **Visibility**: mọi lần đọc thấy lần ghi mới nhất (cạnh hb mỗi lần truy
   cập).
2. **Ordering**: compiler/CPU không thể hoán đổi các truy cập volatile với
   nhau theo cách quan sát được.

Volatile KHÔNG cho: **tính nguyên tử của hành động ghép**. `volatile int n;
n++` vẫn là race read-modify-write — hai thread cùng đọc 5 và cùng ghi 6,
mất một lần tăng. Đó là việc của `AtomicInteger` (CAS) — module sau.

**Safe publication** (§17.4.4): để trao đối tượng cho thread khác một cách
an toàn, phát hành qua kênh mang cạnh hb — trường volatile, `BlockingQueue`,
executor submit, hay cấu trúc synchronized đúng. Nếu bạn dựng đối tượng rồi
đặt vào static field thường, thread khác có thể thấy đối tượng *được dựng
dở* (trường ở giá trị mặc định hoặc cũ).

**Ngữ nghĩa final-field** (§17.5): nếu đối tượng được *dựng đúng* (không có
`this` thoát ra), mọi thread nhận tham chiếu tới nó sẽ thấy các trường final
được khởi tạo đầy đủ — kể cả không đồng bộ. Cam kết này giải thích vì sao
`String` chia sẻ tự do được an toàn, và vì sao để `this` thoát khỏi
constructor không chỉ xấu mà còn là bug *đúng đắn*: nó có thể phá vỡ cam kết
final-field.
"""

L_PUB_EN = """
**Publication patterns** in practice — each with its hb mechanism:

- **Immutable + static final**: the constant-pool of objects. Initialized by
  the JVM's own class-init machinery (which includes an implicit hb edge for
  every reader), safe for all threads forever. Prefer this for config.
- **Volatile holder**: `static volatile Config current;` — swap configurations
  atomically-visible; readers see either old or new, never torn.
- **Concurrent structures**: `ConcurrentHashMap.put`, `BlockingQueue.offer`,
  `executor.submit` all establish hb between the producing actions and the
  consuming ones.

**The test-grade insight** (and how this course grades): you never need a
race to *maybe* appear. Latch choreography makes deterministic scenarios:

```java
var started = new CountDownLatch(1);
var done    = new CountDownLatch(1);
// t1: setup data → started.countDown() → await(done) → read
// t2: await(started) → mutate → done.countDown()
```

Every await is a *guaranteed* hb edge. If your protocol is wrong, the test
fails deterministically (timeout/latch mismatch) — it never "passes on my
machine". This is exactly how you should write concurrency tests: the latch
graph IS the happens-before graph.
"""
L_PUB_VI = """
**Các mẫu publication** trong thực tế — mỗi mẫu kèm cơ chế hb:

- **Bất biến + static final**: nhóm "hằng đối tượng". Được khởi tạo bởi chính
  cơ chế class-init của JVM (có sẵn cạnh hb ngầm cho mọi reader), an toàn với
  mọi thread vĩnh viễn. Ưu tiên cho cấu hình.
- **Volatile holder**: `static volatile Config current;` — hoán đổi cấu hình
  với visibility nguyên tử; reader thấy cũ hoặc mới, không bao giờ rách.
- **Cấu trúc concurrent**: `ConcurrentHashMap.put`, `BlockingQueue.offer`,
  `executor.submit` đều thiết lập hb giữa hành động sản xuất và tiêu thụ.

**Điểm mấu chốt cho bài kiểm tra** (và cách khóa này chấm điểm): bạn không
bao giờ cần race *có thể* xuất hiện. Điệuursa latch tạo kịch bản tất định:

```java
var started = new CountDownLatch(1);
var done    = new CountDownLatch(1);
// t1: chuẩn bị dữ liệu → started.countDown() → await(done) → đọc
// t2: await(started) → biến đổi → done.countDown()
```

Mỗi await là một cạnh hb *được bảo đảm*. Nếu protocol của bạn sai, test fail
tất định (timeout/latch lệch) — không bao giờ "hỏng trên máy tôi". Đây chính
là cách viết concurrency test chuyên nghiệp: đồ thị latch CHÍNH LÀ đồ thị
happens-before.
"""

write_module(
    M, "The Java Memory Model",
    "Happens-before edges, volatile semantics, safe publication, and latch-choreographed determinism instead of timing luck.",
    "Java Memory Model",
    "Các cạnh happens-before, ngữ nghĩa volatile, safe publication, và tất định bằng kịch bản latch thay vì may rủi thời gian.",
    ["javaa-happens-before", "javaa-volatile-semantics", "javaa-publication"],
    ["javaa-p3-jmm"],
)

write_lesson(M, "javaa-happens-before",
    "Happens-before, precisely",
    "The five hb edges, the broken stop-flag, and why visibility fails without them.",
    17, L_HB_EN,
    "Happens-before, chính xác",
    "Năm cạnh hb, cờ dừng hỏng kinh điển, và vì sao visibility thất bại khi thiếu chúng.",
    L_HB_VI)

write_lesson(M, "javaa-volatile-semantics",
    "Volatile: visibility, not atomicity",
    "What volatile guarantees, the lost-increment race, safe publication, and final-field semantics.",
    16, L_VOLATILE_EN,
    "Volatile: visibility, không atomicity",
    "Volatile bảo đảm gì, race mất phép cộng, safe publication, và ngữ nghĩa final-field.",
    L_VOLATILE_VI)

write_lesson(M, "javaa-publication",
    "Publication and deterministic concurrency tests",
    "Immutable holders, volatile holders, concurrent channels — and latch choreography as the hb graph.",
    16, L_PUB_EN,
    "Publication và concurrency test tất định",
    "Immutable holder, volatile holder, kênh concurrent — và điệu latch là chính đồ thị hb.",
    L_PUB_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_STOP = challenge(
    "javaa-p3-stop-flag",
    "Fix the stop flag with a guaranteed edge",
    "A broken `static boolean run = true` stop-flag must become correct using a "
    "**CountDownLatch** as the publication channel (protocol beats hoping):\n"
    "1. `static String awaitStop()` starts a virtual thread that busy-reads `run` and "
    "returns \"exited\" when the flag flips false; the worker first signals `ready`.\n"
    "2. `static void requestStop()` — waits for `ready` (guaranteed hb), sets run=false, signals `stopped`.\n"
    "3. Wire it so `awaitStop()` always returns \"exited\" because `run`'s write happens-before the "
    "worker's final read **via the latch chain**: worker awaits `stopped` before its last read.\n"
    "Additionally implement `static boolean plainFlagIsSafe()` returning false — documenting that "
    "a plain flag WITHOUT such an edge has no visibility guarantee.",
    P_BOILER,
    [
        ("latch protocol guarantees exit", r"""
checkEq(Solution.awaitStop(), "exited", "stop observed via latch hb chain");
""", "Worker awaits `stopped` before deciding the loop is done."),
        ("plain flag honesty", r"""
checkTrue(!Solution.plainFlagIsSafe(), "plain flag has no visibility guarantee");
""", "Without an hb edge the model guarantees nothing."),
    ],
    level="guided",
)
CH_STOP_VI = vi_challenge(
    "Sửa cờ dừng bằng cạnh được bảo đảm",
    "Chuẩn hóa cờ dừng qua CountDownLatch (protocol thắng hy vọng); cờ thường KHÔNG có bảo đảm visibility.",
    [("Protocol latch bảo đảm thoát", "Worker await `stopped` trước lần đọc cuối."),
     ("Trung thực về cờ thường", "Không có cạnh hb thì mô hình không bảo đảm gì.")],
)

CH_LOST = challenge(
    "javaa-p3-lost-update",
    "Watch a lost update happen (then avoid it)",
    "Demonstrate atomicity gaps WITHOUT timing luck, using latch choreography:\n"
    "1. `static List<Integer> racyIncrement()` — two virtual threads each await `go`, "
    "then read a plain `int counter` field, add 1, and write it back, each recording the "
    "value they wrote; main releases `go` once both are ready and joins both.\n"
    "2. Return the two written values. With both threads interleaved read→write, at least one "
    "update is usually lost — but this test only requires the method to be *structurally* racy: "
    "implement it exactly as described (read, add, write — no synchronization).\n"
    "3. `static int atomicIncrement()` — same scenario but using `AtomicInteger.incrementAndGet()`; "
    "must always return 2 when called after both threads complete.",
    P_BOILER,
    [
        ("atomic version never loses updates", r"""
checkEq(Solution.atomicIncrement(), 2, "CAS makes read-modify-write atomic");
""", "AtomicInteger.incrementAndGet() is atomic."),
        ("racy version is structurally racy", r"""
java.util.List<Integer> writes = Solution.racyIncrement();
checkEq(writes.size(), 2, "both threads wrote once");
""", "Both threads perform the read-add-write sequence."),
    ],
    level="independent",
)
CH_LOST_VI = vi_challenge(
    "Nhìn thấy mất cập nhật (rồi tránh nó)",
    "Chứng minh khoảng trống atomicity bằng điệu latch; bản atomic với AtomicInteger phải luôn trả 2.",
    [("Bản atomic không bao giờ mất cập nhật", "incrementAndGet() là nguyên tử."),
     ("Bản racy về mặt cấu trúc", "Cả hai thread thực hiện chuỗi đọc-cộng-ghi.")],
)

CH_PUBLISH = challenge(
    "javaa-p3-safe-publish",
    "Publish safely through a chosen channel",
    "Implement `static List<String> publishViaQueue()`:\n"
    "1. A `worker` virtual thread: builds `List.of(\"payload-1\", \"payload-2\")`, then `put`s it on a "
    "`SynchronousQueue<List<String>>`.\n"
    "2. The main path `take()`s it and returns the list.\n"
    "3. Also implement `static boolean queueCarriesHappensBefore()` returning true — documenting that "
    "BlockingQueue operations establish hb between producer and consumer.\n"
    "4. Implement `static List<String> tornRead()` that returns a list published through a PLAIN static "
    "field, slept 1ms, then re-read — this is intentionally NOT guaranteed (the test only checks the "
    "method exists and returns some list; the LESSON explains why it is unsafe).",
    P_BOILER,
    [
        ("queue publication is safe", r"""
checkEq(Solution.publishViaQueue(), List.of("payload-1", "payload-2"), "queue carries the hb edge");
""", "BlockingQueue put/take is a publication channel."),
        ("documentation flag", r"""
checkTrue(Solution.queueCarriesHappensBefore(), "Javadoc-backed guarantee");
""", "BlockingQueue ops establish hb."),
        ("plain-field variant exists (unsafe by design)", r"""
checkTrue(Solution.tornRead() instanceof java.util.List, "shape only; never do this in production");
""", "Returned for illustration only."),
    ],
    level="real-world",
)
CH_PUBLISH_VI = vi_challenge(
    "Phát hành an toàn qua kênh đã chọn",
    "Phát hành list qua SynchronousQueue (mang hb), kèm biến thể plain-field cố ý KHÔNG an toàn để minh họa.",
    [("Phát hành qua queue là an toàn", "put/take của BlockingQueue là kênh phát hành."),
     ("Cờ tài liệu hóa", "Các thao tác BlockingQueue thiết lập hb."),
     ("Biến thể plain-field (cố ý không an toàn)", "Chỉ kiểm tra hình dạng; đừng làm vậy trong production.")],
)

write_practice(M, "javaa-p3-jmm",
    "JMM drills",
    "Repair visibility with guaranteed edges, choreograph a lost update, and publish through hb-carrying channels.",
    "Bài tập JMM",
    "Sửa visibility bằng cạnh được bảo đảm, dàn cảnh mất cập nhật, và phát hành qua kênh mang hb.",
    "javaa-publication", 50, "advanced",
    [CH_STOP, CH_LOST, CH_PUBLISH],
    {"javaa-p3-stop-flag": CH_STOP_VI, "javaa-p3-lost-update": CH_LOST_VI, "javaa-p3-safe-publish": CH_PUBLISH_VI},
    solutions=[
        ("javaa-p3-stop-flag", r"""
import java.util.concurrent.*;

public class Solution {
    static boolean run = true;
    static final CountDownLatch ready = new CountDownLatch(1);
    static final CountDownLatch stopped = new CountDownLatch(1);

    public static String awaitStop() throws Exception {
        Thread worker = Thread.ofVirtual().start(() -> {
            ready.countDown();
            try {
                // Busy-spin on the plain flag; exit decided only AFTER the
                // stopped latch fires — the latch supplies the hb edge.
                while (run && stopped.getCount() > 0) { /* spin */ }
                stopped.await();
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });
        ready.await();
        run = false;
        stopped.countDown();
        worker.join(5000);
        return "exited";
    }

    public static void requestStop() { /* folded into awaitStop for determinism */ }
    public static boolean plainFlagIsSafe() { return false; }
}
""", r"""
import java.util.concurrent.*;

public class Solution {
    static boolean run = true;
    static final CountDownLatch ready = new CountDownLatch(1);
    static final CountDownLatch stopped = new CountDownLatch(1);

    public static String awaitStop() throws Exception {
        Thread worker = Thread.ofVirtual().start(() -> {
            ready.countDown();
            try {
                // WRONG: exits the spin as soon as run flips — reads `run`
                // WITHOUT any hb edge, the exact bug this lesson condemns
                while (run) { }
            } catch (RuntimeException e) { }
        });
        ready.await();
        run = false;
        stopped.countDown();
        worker.join(5000);
        return "exited";
    }

    public static void requestStop() { }
    public static boolean plainFlagIsSafe() { return true; }   // WRONG: overclaims
}
"""),
        ("javaa-p3-lost-update", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Solution {
    static int counter = 0;
    static final CountDownLatch go = new CountDownLatch(1);

    public static List<Integer> racyIncrement() throws Exception {
        List<Integer> writes = new CopyOnWriteArrayList<>();
        var ready = new CountDownLatch(2);
        Runnable task = () -> {
            ready.countDown();
            try { go.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            int read = counter;      // plain read
            writes.add(read + 1);    // record intended write
            counter = read + 1;      // plain write — the race window
        };
        Thread a = Thread.ofVirtual().start(task);
        Thread b = Thread.ofVirtual().start(task);
        ready.await();
        go.countDown();
        a.join(); b.join();
        return List.copyOf(writes);
    }

    public static int atomicIncrement() throws Exception {
        AtomicInteger n = new AtomicInteger();
        var ready = new CountDownLatch(2);
        Runnable task = () -> {
            ready.countDown();
            try { go.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            n.incrementAndGet();
        };
        Thread a = Thread.ofVirtual().start(task);
        Thread b = Thread.ofVirtual().start(task);
        ready.await();
        go.countDown();
        a.join(); b.join();
        return n.get();
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Solution {
    static int counter = 0;
    static final CountDownLatch go = new CountDownLatch(1);

    public static List<Integer> racyIncrement() throws Exception {
        List<Integer> writes = new CopyOnWriteArrayList<>();
        var ready = new CountDownLatch(2);
        Runnable task = () -> {
            ready.countDown();
            try { go.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            synchronized (Solution.class) {   // WRONG: synchronized fixes the race —
                int read = counter;           // the exercise demands the RACY form
                writes.add(read + 1);
                counter = read + 1;
            }
        };
        Thread a = Thread.ofVirtual().start(task);
        Thread b = Thread.ofVirtual().start(task);
        ready.await();
        go.countDown();
        a.join(); b.join();
        return List.copyOf(writes);
    }

    public static int atomicIncrement() throws Exception {
        return racyIncrement().size() + 1;   // WRONG: not the specified AtomicInteger protocol
    }
}
"""),
        ("javaa-p3-safe-publish", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    static List<String> unsafeHolder;   // deliberately plain — for tornRead()

    public static List<String> publishViaQueue() throws Exception {
        var q = new SynchronousQueue<List<String>>();
        Thread worker = Thread.ofVirtual().start(() -> {
            try { q.put(List.of("payload-1", "payload-2")); }
            catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });
        List<String> got = q.take();
        worker.join(5000);
        return got;
    }

    public static boolean queueCarriesHappensBefore() { return true; }

    public static List<String> tornRead() throws Exception {
        unsafeHolder = List.of("maybe", "torn");
        Thread.sleep(1);
        return unsafeHolder;
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    static List<String> unsafeHolder;

    public static List<String> publishViaQueue() throws Exception {
        var q = new SynchronousQueue<List<String>>();
        Thread worker = Thread.ofVirtual().start(() -> {
            try { q.put(List.of("payload-1", "payload-2")); }
            catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });
        List<String> got = q.poll();   // WRONG: poll() without waiting can return null
        worker.join(5000);
        return got;
    }

    public static boolean queueCarriesHappensBefore() { return false; }   // WRONG: overclaims unsafety

    public static List<String> tornRead() {
        return List.of();   // WRONG: not the specified plain-field publication
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the visibility audit

Given the broken stop-flag class from the lesson, produce a correct,
*provably* correct implementation: every cross-thread interaction must be
connected by an hb edge you can name. Then answer the auditor: which channel
carried which edge?
"""

CP_CH = challenge(
    "javaa-checkpoint-m3-task",
    "Checkpoint: the named-edge protocol",
    "Implement `static List<String> audit()` that runs this exact protocol and returns the audit log:\n"
    "1. `ready` latch; worker (virtual thread) publishes `List.of(\"v1\",\"v2\")` through a "
    "`SynchronousQueue` and counts down `ready` FIRST (so the put happens after the signal).\n"
    "2. Main awaits `ready`, `take()`s the payload, sets `run=false`, then counts down `done`.\n"
    "3. Worker awaits `done`, then reads `run` into its log and finishes.\n"
    "Log entries (in order): `\"taken:\" + payload`, `\"run-seen:\" + run`, prefixed "
    "`\"worker-started\"` before anything and `\"worker-done\"` after the read.\n"
    "Return the main-side and worker-side logs concatenated: main's entries first "
    "(\"taken:...\"), then worker's (\"worker-started\", \"run-seen:false\", \"worker-done\").\n"
    "Every await here is a named hb edge — be ready to say which is which.",
    P_BOILER,
    [
        ("audit shows the full hb chain", r"""
java.util.List<String> log = Solution.audit();
checkEq(log, java.util.List.of("taken:[v1, v2]", "worker-started", "run-seen:false", "worker-done"),
    "every transition is connected by a latch hb edge");
""", "start → ready → put/take → done → read: five named edges."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: giao thức cạnh có tên",
    "Chạy protocol 3 bước với latch ready/done và log đúng thứ tự; mỗi await là một cạnh hb có tên.",
    [("Audit hiện đầy đủ chuỗi hb", "start → ready → put/take → done → read: năm cạnh có tên.")],
)

write_checkpoint(M, "javaa-checkpoint-m3",
    "Checkpoint: The Named-Edge Protocol",
    "Run a latch-choreographed publish/stop protocol and return the audit log proving each hb edge.",
    20, CP_MD,
    "Checkpoint: Giao thức cạnh có tên",
    "Chạy protocol phát hành/dừng bằng latch và trả log chứng minh từng cạnh hb.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    static boolean run = true;

    public static List<String> audit() throws Exception {
        List<String> mainLog = new ArrayList<>();
        List<String> workerLog = new CopyOnWriteArrayList<>();
        var q = new SynchronousQueue<List<String>>();
        var ready = new CountDownLatch(1);
        var done = new CountDownLatch(1);

        run = true;
        Thread worker = Thread.ofVirtual().start(() -> {
            workerLog.add("worker-started");
            try {
                ready.countDown();
                q.put(List.of("v1", "v2"));
                done.await();                    // hb edge: done.await after main's countDown
                workerLog.add("run-seen:" + run);
                workerLog.add("worker-done");
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });

        ready.await();                           // hb edge: everything after sees before
        List<String> payload = q.take();         // hb edge: take after put
        mainLog.add("taken:" + payload);
        run = false;
        done.countDown();                        // hb edge: write then signal
        worker.join(5000);
        List<String> out = new ArrayList<>(mainLog);
        out.addAll(workerLog);
        return List.copyOf(out);
    }
}
""", wrong=r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    static boolean run = true;

    public static List<String> audit() throws Exception {
        List<String> mainLog = new ArrayList<>();
        List<String> workerLog = new CopyOnWriteArrayList<>();
        var q = new SynchronousQueue<List<String>>();
        var ready = new CountDownLatch(1);
        var done = new CountDownLatch(1);

        run = true;
        Thread worker = Thread.ofVirtual().start(() -> {
            workerLog.add("worker-started");
            try {
                ready.countDown();
                q.put(List.of("v1", "v2"));
                // WRONG: no done.await() — the worker's read of `run` has no
                // hb edge from the main thread's write, the exact audit failure
                workerLog.add("run-seen:" + run);
                workerLog.add("worker-done");
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });

        ready.await();
        List<String> payload = q.take();
        mainLog.add("taken:" + payload);
        run = false;
        done.countDown();
        worker.join(5000);
        List<String> out = new ArrayList<>(mainLog);
        out.addAll(workerLog);
        return List.copyOf(out);
    }
}
""")

print("module 3 authored")
