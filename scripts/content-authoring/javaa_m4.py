#!/usr/bin/env python3
"""Java — Advanced — Module 4: java-locks-cas.

Beyond synchronized: ReentrantLock (fairness, tryLock), Condition queues,
Semaphore permits, ConcurrentHashMap's atomic compute family, and CAS with
the ABA problem. All concurrency tests are latch-choreographed (Module 3
discipline). House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "java-locks-cas"

L_LOCKS_EN = """
`synchronized` covers the basics. Real systems need what **ReentrantLock**
adds:

- **tryLock**: attempt acquisition *now* (or within a timeout) instead of
  blocking forever. The backbone of deadlock avoidance — acquire two locks
  with `tryLock` + backoff, or walk away.
- **Fairness**: `new ReentrantLock(true)` grants access in arrival order.
  Fair locks trade throughput for bounded waiting; default (unfair) lets a
  just-released thread re-acquire, which is usually what you want.
- **Interruptible acquisition**: `lockInterruptibly()` lets blocked threads
  respond to cancellation — `synchronized` cannot.
- **Condition queues**: one lock, multiple wait-sets. `await()/signal()`
  replace `wait()/notify()` per-Condition, so a bounded buffer's not-full and
  not-empty predicates each get their own queue (no more waking everyone for
  one predicate).

```java
var lock = new ReentrantLock();
var notEmpty = lock.newCondition();
// consumer:  lock.lock(); try { while (empty) notEmpty.await(); ... } finally { lock.unlock(); }
// producer:  lock.lock(); try { put(x); notEmpty.signal(); } finally { lock.unlock(); }
```

The rules that make it correct: **await inside a loop** (spurious wakeups are
allowed), and **unlock in finally** (exceptions must not leak a held lock).
"""
L_LOCKS_VI = """
`synchronized` che phần cơ bản. Hệ thống thật cần những gì **ReentrantLock**
thêm:

- **tryLock**: thử giữ khóa *ngay* (hoặc trong timeout) thay vì chặn vĩnh
  viễn. Xương sống của việc tránh deadlock — giữ hai khóa bằng `tryLock` +
  backoff, hoặc bỏ đi.
- **Fairness**: `new ReentrantLock(true)` cấp quyền theo thứ tự đến. Fair
  lock đổi throughput lấy thời gian chờ có chặn trên; mặc định (unfair) cho
  thread vừa nhả khóa giữ lại ngay — thường là điều bạn muốn.
- **Giữ khóa có thể interrupt**: `lockInterruptibly()` cho phép thread bị
  chặn phản hồi hủy — `synchronized` không làm được.
- **Hàng đợi Condition**: một khóa, nhiều wait-set. `await()/signal()` thay
  `wait()/notify()` theo từng Condition, nên predicate not-full và not-empty
  của bounded buffer có hàng đợi riêng (không đánh thức mọi người cho một
  predicate).

```java
var lock = new ReentrantLock();
var notEmpty = lock.newCondition();
// consumer:  lock.lock(); try { while (empty) notEmpty.await(); ... } finally { lock.unlock(); }
// producer:  lock.lock(); try { put(x); notEmpty.signal(); } finally { lock.unlock(); }
```

Các quy tắc làm nó đúng: **await trong vòng lặp** (spurious wakeup được cho
phép), và **unlock trong finally** (exception không được làm lộ khóa đang
giữ).
"""

L_CHM_EN = """
`ConcurrentHashMap` is not a synchronized HashMap — it is a *concurrent
object* with its own atomic compound operations. The ones professionals use:

```java
map.computeIfAbsent(key, k -> expensive(k));   // atomic: at most once per key
map.compute(key, (k, v) -> mergeInto(v));       // atomic read-modify-write
map.merge(key, 1, Integer::sum);                // the frequency-counter idiom
map.putIfAbsent(key, seed);                     // initialize-once
```

`compute`-family callbacks run under the bin's lock — they must be **short,
and must not touch other keys of the same map** (nested compute on the same
key deadlocks; on other keys risks it).

Why not `Collections.synchronizedMap`? Because
`if (!map.containsKey(k)) map.put(k, v)` is two atomic operations — the
*check* and the *act* can interleave across threads. CHM's compute family
makes the whole check-then-act **one** atomic operation. That is the
difference between a class that is internally consistent and an algorithm
that is externally correct.
"""
L_CHM_VI = """
`ConcurrentHashMap` không phải HashMap có synchronized — nó là *đối tượng
concurrent* với các phép toán ghép nguyên tử riêng. Nhóm chuyên nghiệp dùng:

```java
map.computeIfAbsent(key, k -> expensive(k));   // nguyên tử: tối đa một lần mỗi key
map.compute(key, (k, v) -> mergeInto(v));       // nguyên tử read-modify-write
map.merge(key, 1, Integer::sum);                // idiom bộ đếm tần suất
map.putIfAbsent(key, seed);                     // khởi tạo một lần
```

Callback của họ `compute` chạy dưới khóa của bin — phải **ngắn, và không được
đụng key khác của cùng map** (compute lồng trên cùng key là deadlock; trên
key khác là rủi ro).

Vì sao không dùng `Collections.synchronizedMap`? Vì
`if (!map.containsKey(k)) map.put(k, v)` là hai phép nguyên tử — *kiểm tra*
và *hành động* có thể chen ngang giữa các thread. Họ compute của CHM biến
toàn bộ check-then-act thành **một** phép nguyên tử. Đó là khoảng cách giữa
lớp có tính nhất quán nội bộ và thuật toán đúng đắn bên ngoài.
"""

L_CAS_EN = """
**CAS — compare-and-set** — is the hardware instruction under every atomic
class: "if the value is still `expected`, set it to `next`, atomically;
report whether you won." Losers retry. No lock is held; the OS never
schedules around you.

```java
AtomicReference<State> ref = new AtomicReference<>(initial);
State cur, next;
do {
    cur = ref.get();
    next = derive(cur);
} while (!ref.compareAndSet(cur, next));
```

**The ABA problem**: CAS asks "is it still A?" — not "did anything happen?".
If the value went A→B→A between your read and your CAS, your compare *passes*
but the world changed. Harmless for counters, fatal for stacks built on
pointers: node A was freed and reallocated while you held a stale `next`.
Java's answer: `AtomicStampedReference` (value + stamp, both CAS'd together)
or simply avoiding shared-mutable-node designs.

CAS is *optimistic* (assume no interference, retry on loss); locks are
*pessimistic* (block first). Contended CAS burns CPU retrying; contended
locks park threads. High contention → locks often win. Low contention,
short critical sections → CAS wins. Knowing *which regime you are in* is the
skill.
"""
L_CAS_VI = """
**CAS — compare-and-set** — là lệnh phần cứng dưới mọi lớp atomic: "nếu giá
trị vẫn là `expected`, gán thành `next` một cách nguyên tử; báo kết quả
thắng/thua." Kẻ thua thử lại. Không giữ khóa nào; OS không cần can thiệp.

```java
AtomicReference<State> ref = new AtomicReference<>(initial);
State cur, next;
do {
    cur = ref.get();
    next = derive(cur);
} while (!ref.compareAndSet(cur, next));
```

**Bài toán ABA**: CAS hỏi "vẫn là A chứ?" — không hỏi "có gì xảy ra không?".
Nếu giá trị đi A→B→A giữa lần đọc và CAS của bạn, phép so sánh *vẫn qua* nhưng
thế giới đã đổi. Vô hại với bộ đếm, chết người với stack xây trên con trỏ:
nút A được giải phóng và cấp phát lại trong khi bạn nắm `next` cũ. Câu trả
lời của Java: `AtomicStampedReference` (giá trị + stamp, CAS cùng lúc) hoặc
đơn giản là tránh thiết kế nút dùng chung có thể biến đổi.

CAS *lạc quan* (giả định không xung đột, thua thì thử lại); khóa *bi quan*
(chặn trước). CAS tranh chấp cao đốt CPU để retry; khóa tranh chấp cao cho
thread ngủ. Mức tranh chấp cao → khóa thường thắng. Tranh chấp thấp, vùng
nghiêm ngặt ngắn → CAS thắng. Biết *mình đang ở chế độ nào* mới là kỹ năng.
"""

write_module(
    M, "Locks, Conditions & CAS",
    "ReentrantLock's superpowers, per-predicate Condition queues, ConcurrentHashMap's atomic compute family, and CAS with ABA.",
    "Khóa, Condition & CAS",
    "Siêu năng lực của ReentrantLock, hàng đợi Condition theo predicate, họ compute nguyên tử của ConcurrentHashMap, và CAS với ABA.",
    ["javaa-reentrant-conditions", "javaa-chm-atomics", "javaa-cas-aba"],
    ["javaa-p4-locks"],
)

write_lesson(M, "javaa-reentrant-conditions",
    "ReentrantLock and Condition queues",
    "tryLock for deadlock avoidance, fairness tradeoffs, interruptibility, and one condition per predicate.",
    17, L_LOCKS_EN,
    "ReentrantLock và hàng đợi Condition",
    "tryLock để tránh deadlock, đánh đổi fairness, khả năng interrupt, và mỗi predicate một condition.",
    L_LOCKS_VI)

write_lesson(M, "javaa-chm-atomics",
    "ConcurrentHashMap's atomic compute family",
    "computeIfAbsent/merge/compute as single atomic check-then-act, and the callback rules.",
    15, L_CHM_EN,
    "Họ compute nguyên tử của ConcurrentHashMap",
    "computeIfAbsent/merge/compute là check-then-act nguyên tử duy nhất, và quy tắc cho callback.",
    L_CHM_VI)

write_lesson(M, "javaa-cas-aba",
    "CAS, retry loops, and the ABA problem",
    "The lock-free pattern, why A→B→A fools compare-and-set, and when CAS beats locks (or loses).",
    17, L_CAS_EN,
    "CAS, vòng retry, và bài toán ABA",
    "Mẫu lock-free, vì sao A→B→A đánh lừa compare-and-set, và khi nào CAS thắng khóa (hoặc thua).",
    L_CAS_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_TRYLOCK = challenge(
    "javaa-p4-trylock-transfer",
    "Deadlock-free transfers with tryLock",
    "Implement `static boolean transfer(Account from, Account to, int amount)` that can NEVER "
    "deadlock, using the tryLock-backoff pattern:\n"
    "1. Acquire both account locks with `tryLock()` (use a small retry loop with backoff or a "
    "ordered attempt).\n"
    "2. On success: check `from.balance() >= amount`, then move funds, release both locks, return true.\n"
    "3. If either lock cannot be acquired: release whatever you hold and return false.\n"
    "4. `record Account(int id, int balance)` won't do — accounts must expose `ReentrantLock lock()` "
    "and be mutable; build a small static Account class inside Solution (id, balance, lock).\n"
    "5. `static boolean unsafeTransfer(...)` doing the same with plain `synchronized(from)` "
    "nested `synchronized(to)` — intentionally deadlock-prone in *structure* (tests only call it "
    "with distinct orderings to keep the suite deterministic; the lesson explains the hazard).",
    P_BOILER,
    [
        ("successful transfer moves funds", r"""
Solution.Account a = new Solution.Account(1, 100);
Solution.Account b = new Solution.Account(2, 0);
checkTrue(Solution.transfer(a, b, 30), "transfer accepted");
checkEq(a.balance(), 70, "debit applied");
checkEq(b.balance(), 30, "credit applied");
""", "Debit and credit under both locks."),
        ("insufficient funds rejected atomically", r"""
Solution.Account a = new Solution.Account(1, 10);
Solution.Account b = new Solution.Account(2, 0);
checkTrue(!Solution.transfer(a, b, 999), "rejected");
checkEq(a.balance(), 10, "nothing taken on reject");
""", "Balance check under both locks; no partial moves."),
        ("tryLock backs off a CROSS-THREAD held lock", r"""
Solution.Account a = new Solution.Account(1, 50);
Solution.Account b = new Solution.Account(2, 50);
var held = new java.util.concurrent.CountDownLatch(1);
var release = new java.util.concurrent.CountDownLatch(1);
Thread holder = Thread.ofVirtual().start(() -> {
    a.lock().lock();          // a DIFFERENT thread holds a's lock
    held.countDown();
    try { release.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    a.lock().unlock();
});
held.await();
boolean moved = Solution.transfer(a, b, 10);
release.countDown();
holder.join(5000);
checkTrue(!moved, "tryLock must back off, never block forever");
checkEq(a.balance(), 50, "no funds moved while blocked");
""", "Holder runs on another thread, so tryLock (R) backs off; a blocking lock() would deadlock the test."),
    ],
    level="independent",
)
CH_TRYLOCK_VI = vi_challenge(
    "Chuyển tiền không deadlock bằng tryLock",
    "transfer() giữ cả hai khóa bằng tryLock với backoff; thất bại thì nhả và trả false — không bao giờ deadlock.",
    [("Chuyển thành công", "Ghi nợ và ghi có dưới cả hai khóa."),
     ("Từ chối khi thiếu tiền", "Kiểm tra balance dưới cả hai khóa; không chuyển nửa vời."),
     ("Sống sót khi khóa bị giữ", "Hoặc chuyển sạch, hoặc lùi lại — không bao giờ trạng thái rách.")],
)

CH_CHM = challenge(
    "javaa-p4-compute-family",
    "The compute family",
    "Implement with ConcurrentHashMap ONLY (no explicit synchronized blocks):\n"
    "1. `static Map<String,Integer> frequency(List<String> words)` — count occurrences using `merge`.\n"
    "2. `static Map<String,List<String>> indexByFirstLetter(List<String> words)` — group using "
    "`computeIfAbsent`, appending into the existing list on repeat letters.\n"
    "3. `static int uniqueId(Map<String,Integer> registry, String name)` — reserve `name` with "
    "`computeIfAbsent` assigning `registry.size()`; a repeat call with the same name must return "
    "the SAME id (never two ids for one name).",
    P_BOILER,
    [
        ("frequency via merge", r"""
checkEq(Solution.frequency(List.of("a","b","a","c","b","a")),
        Map.of("a",3,"b",2,"c",1), "merge counts");
""", "map.merge(w, 1, Integer::sum)."),
        ("grouping via computeIfAbsent", r"""
var idx = Solution.indexByFirstLetter(List.of("ant","bee","ape","bat"));
checkEq(idx.get("a"), List.of("ant","ape"), "a-bucket ordered");
checkEq(idx.get("b"), List.of("bee","bat"), "b-bucket ordered");
""", "computeIfAbsent(k, x -> new ArrayList<>()).add(word)."),
        ("id reservation is stable", r"""
var reg = new java.util.concurrent.ConcurrentHashMap<String,Integer>();
int id1 = Solution.uniqueId(reg, "alice");
int id2 = Solution.uniqueId(reg, "alice");
int id3 = Solution.uniqueId(reg, "bob");
checkTrue(id1 == id2, "same name, same id");
checkTrue(id1 != id3, "distinct names, distinct ids");
checkTrue(id1 == 0, "ids start at zero");
""", "computeIfAbsent guarantees at-most-once assignment, starting at 0."),
    ],
    level="independent",
)
CH_CHM_VI = vi_challenge(
    "Họ compute",
    "Chỉ dùng ConcurrentHashMap: frequency bằng merge, nhóm theo chữ cái bằng computeIfAbsent, cấp id ổn định.",
    [("Đếm bằng merge", "map.merge(w, 1, Integer::sum)."),
     ("Nhóm bằng computeIfAbsent", "computeIfAbsent(k, x -> new ArrayList<>()).add(word)."),
     ("Cấp id ổn định", "computeIfAbsent bảo đảm cấp tối đa một lần.")],
)

CH_CAS = challenge(
    "javaa-p4-cas-counter",
    "Write the CAS retry loop yourself",
    "Do NOT use AtomicInteger's incrementAndGet. Build the loop from CAS:\n"
    "1. `static int casIncrement(AtomicInteger n)` — read, add 1, `compareAndSet(read, read+1)`; "
    "retry the whole read on failure; return the NEW value.\n"
    "2. `static int concurrentCasSum(AtomicInteger n, int threads)` — start `threads` virtual "
    "threads each calling `casIncrement` 1000 times via a latch go-signal; join all; return n.get().\n"
    "3. `static String explainAba()` returns exactly:\n"
    "   \"CAS compares values, not history: A->B->A passes the compare but the state changed\".",
    P_BOILER,
    [
        ("single increment", r"""
var n = new java.util.concurrent.atomic.AtomicInteger(5);
checkEq(Solution.casIncrement(n), 6, "read-add-CAS");
checkEq(n.get(), 6, "stored");
""", "Loop: cur = n.get(); until n.compareAndSet(cur, cur+1)."),
        ("1000 x threads, zero lost updates", r"""
var n = new java.util.concurrent.atomic.AtomicInteger(0);
checkEq(Solution.concurrentCasSum(n, 8), 8000, "CAS loop is atomic under contention");
""", "Each of 8 threads adds 1000; CAS retries absorb contention."),
        ("ABA explanation exact", r"""
checkEq(Solution.explainAba(),
  "CAS compares values, not history: A->B->A passes the compare but the state changed",
  "the one-line truth");
""", "Copy the sentence exactly."),
    ],
    level="independent",
)
CH_CAS_VI = vi_challenge(
    "Tự viết vòng retry CAS",
    "Không dùng incrementAndGet: tự dựng vòng read-add-CAS, chạy đa thread, và diễn giải ABA trong một câu.",
    [("Một lần tăng", "Vòng lặp: cur = n.get(); đến khi compareAndSet(cur, cur+1)."),
     ("8 x 1000, không mất cập nhật", "CAS retry hấp thụ tranh chấp."),
     ("Diễn giải ABA chính xác", "Chép đúng câu trong đề.")],
)

write_practice(M, "javaa-p4-locks",
    "Lock & CAS drills",
    "Build deadlock-free transfers, atomic map algorithms, and a hand-rolled CAS loop that survives contention.",
    "Bài tập khóa & CAS",
    "Xây chuyển tiền không deadlock, thuật toán map nguyên tử, và vòng CAS tự viết chịu được tranh chấp.",
    "javaa-cas-aba", 55, "advanced",
    [CH_TRYLOCK, CH_CHM, CH_CAS],
    {"javaa-p4-trylock-transfer": CH_TRYLOCK_VI, "javaa-p4-compute-family": CH_CHM_VI, "javaa-p4-cas-counter": CH_CAS_VI},
    solutions=[
        ("javaa-p4-trylock-transfer", r"""
import java.util.concurrent.locks.*;

public class Solution {
    public static class Account {
        private final int id;
        private int balance;
        private final ReentrantLock lock = new ReentrantLock();
        public Account(int id, int balance) { this.id = id; this.balance = balance; }
        public int balance() { return balance; }
        public ReentrantLock lock() { return lock; }
    }

    public static boolean transfer(Account from, Account to, int amount) {
        for (int attempt = 0; attempt < 64; attempt++) {
            if (!from.lock().tryLock()) { Thread.yield(); continue; }
            try {
                if (to.lock().tryLock()) {
                    try {
                        if (from.balance < amount) return false;
                        from.balance -= amount;
                        to.balance += amount;
                        return true;
                    } finally { to.lock().unlock(); }
                }
            } finally { from.lock().unlock(); }
            Thread.yield();   // backoff before retry
        }
        return false;   // extreme contention: report failure, never deadlock
    }

    public static boolean unsafeTransfer(Account from, Account to, int amount) {
        synchronized (from) {
            synchronized (to) {   // structurally deadlock-prone under reversed order
                if (from.balance < amount) return false;
                from.balance -= amount;
                to.balance += amount;
                return true;
            }
        }
    }
}
""", r"""
import java.util.concurrent.locks.*;

public class Solution {
    public static class Account {
        private final int id;
        private int balance;
        private final ReentrantLock lock = new ReentrantLock();
        public Account(int id, int balance) { this.id = id; this.balance = balance; }
        public int balance() { return balance; }
        public ReentrantLock lock() { return lock; }
    }

    // WRONG: lock() blocks forever — classic lock-ordering deadlock under
    // reversed call order, the exact hazard tryLock exists to avoid
    public static boolean transfer(Account from, Account to, int amount) {
        from.lock().lock();
        try {
            to.lock().lock();
            try {
                if (from.balance < amount) return false;
                from.balance -= amount;
                to.balance += amount;
                return true;
            } finally { to.lock().unlock(); }
        } finally { from.lock().unlock(); }
    }

    public static boolean unsafeTransfer(Account from, Account to, int amount) {
        return transfer(from, to, amount);
    }
}
"""),
        ("javaa-p4-compute-family", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static Map<String, Integer> frequency(List<String> words) {
        ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
        for (String w : words) m.merge(w, 1, Integer::sum);
        return m;
    }

    public static Map<String, List<String>> indexByFirstLetter(List<String> words) {
        ConcurrentHashMap<String, List<String>> m = new ConcurrentHashMap<>();
        for (String w : words) {
            String k = w.substring(0, 1);
            m.computeIfAbsent(k, x -> new ArrayList<>()).add(w);
        }
        return m;
    }

    public static int uniqueId(ConcurrentHashMap<String, Integer> registry, String name) {
        return registry.computeIfAbsent(name, k -> registry.size());
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static Map<String, Integer> frequency(List<String> words) {
        ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
        for (String w : words) {
            // WRONG: check-then-act across two calls — under concurrency the
            // count can be lost; the compute family exists to make it atomic
            if (!m.containsKey(w)) m.put(w, 1); else m.put(w, m.get(w) + 1);
        }
        return m;
    }

    public static Map<String, List<String>> indexByFirstLetter(List<String> words) {
        ConcurrentHashMap<String, List<String>> m = new ConcurrentHashMap<>();
        for (String w : words) {
            String k = w.substring(0, 1);
            m.put(k, new ArrayList<>(List.of(w)));   // WRONG: overwrites the bucket — loses earlier words
        }
        return m;
    }

    public static int uniqueId(ConcurrentHashMap<String, Integer> registry, String name) {
        if (registry.containsKey(name)) return registry.get(name);
        registry.put(name, registry.size() + 1);   // WRONG: ids start at 1, not 0
        return registry.get(name);
    }
}
"""),
        ("javaa-p4-cas-counter", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Solution {
    public static int casIncrement(AtomicInteger n) {
        while (true) {
            int cur = n.get();
            if (n.compareAndSet(cur, cur + 1)) return cur + 1;
        }
    }

    public static int concurrentCasSum(AtomicInteger n, int threads) throws Exception {
        var go = new CountDownLatch(1);
        var ready = new CountDownLatch(threads);
        List<Thread> ts = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            Thread t = Thread.ofVirtual().start(() -> {
                ready.countDown();
                try { go.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                for (int j = 0; j < 1000; j++) casIncrement(n);
            });
            ts.add(t);
        }
        ready.await();
        go.countDown();
        for (Thread t : ts) t.join();
        return n.get();
    }

    public static String explainAba() {
        return "CAS compares values, not history: A->B->A passes the compare but the state changed";
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class Solution {
    // WRONG: read-add-write without retry — the lost-update bug from Module 3
    public static int casIncrement(AtomicInteger n) {
        int cur = n.get();
        n.set(cur + 1);
        return cur + 1;
    }

    public static int concurrentCasSum(AtomicInteger n, int threads) throws Exception {
        var go = new CountDownLatch(1);
        var ready = new CountDownLatch(threads);
        List<Thread> ts = new ArrayList<>();
        for (int i = 0; i < threads; i++) {
            Thread t = Thread.ofVirtual().start(() -> {
                ready.countDown();
                try { go.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                for (int j = 0; j < 1000; j++) casIncrement(n);
            });
            ts.add(t);
        }
        ready.await();
        go.countDown();
        for (Thread t : ts) t.join();
        return n.get();
    }

    public static String explainAba() {
        return "CAS is always safe";   // WRONG: ABA disproves this
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the bounded buffer, three ways

The bounded buffer is the "hello world" of concurrency — and the best
diagnostic of whether someone *understands* synchronization. Build it with a
lock + two Conditions, prove it under choreographed load, and state the CAS
alternative.
"""

CP_CH = challenge(
    "javaa-checkpoint-m4-task",
    "Checkpoint: bounded buffer with dual conditions",
    "Implement `static List<Integer> runBuffer()`:\n"
    "1. Inside Solution, build a bounded buffer (capacity 2) with `ReentrantLock` + two Conditions "
    "(`notFull`, `notEmpty`) and internal `ArrayDeque<Integer>`.\n"
    "2. Producer virtual thread: puts 1..5 (await notFull while full; signal notEmpty after each put).\n"
    "3. Consumer virtual thread: takes 5 values (await notEmpty while empty; signal notFull after each take).\n"
    "4. `runBuffer()` starts both, waits for the consumer's 5 values, and returns them in take-order.\n"
    "5. `static String casAlternative()` returns exactly: \"a CAS loop on an index pair could do it, "
    "but Condition queues express the wait logic more clearly\".",
    P_BOILER,
    [
        ("all five items cross in order", r"""
checkEq(Solution.runBuffer(), java.util.List.of(1,2,3,4,5), "FIFO crossing under capacity 2");
""", "Producer 1..5, consumer takes all five, order preserved."),
        ("CAS alternative stated", r"""
checkEq(Solution.casAlternative(),
  "a CAS loop on an index pair could do it, but Condition queues express the wait logic more clearly",
  "tradeoff line");
""", "Copy exactly."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: bounded buffer với hai Condition",
    "Dựng buffer capacity 2 bằng lock + notFull/notEmpty, chạy producer/consumer 1..5, trả thứ tự take.",
    [("Năm phần tử vượt qua đúng thứ tự", "Producer 1..5, consumer lấy đủ năm, giữ FIFO."),
     ("Nêu phương án CAS", "Chép đúng câu đánh đổi.")],
)

write_checkpoint(M, "javaa-checkpoint-m4",
    "Checkpoint: The Bounded Buffer",
    "Build a lock+Condition bounded buffer, run it under choreographed load, and state the CAS tradeoff.",
    25, CP_MD,
    "Checkpoint: Bounded Buffer",
    "Dựng bounded buffer bằng lock+Condition, chạy dưới tải có kịch bản, và nêu đánh đổi CAS.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.locks.*;

public class Solution {
    public static List<Integer> runBuffer() throws Exception {
        ReentrantLock lock = new ReentrantLock();
        Condition notFull = lock.newCondition();
        Condition notEmpty = lock.newCondition();
        ArrayDeque<Integer> buf = new ArrayDeque<>();
        final int CAP = 2;

        CountDownLatch consumerDone = new CountDownLatch(5);
        CopyOnWriteArrayList<Integer> out = new CopyOnWriteArrayList<>();

        Thread producer = Thread.ofVirtual().start(() -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    lock.lock();
                    try {
                        while (buf.size() == CAP) notFull.await();
                        buf.addLast(i);
                        notEmpty.signal();
                    } finally { lock.unlock(); }
                }
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });

        Thread consumer = Thread.ofVirtual().start(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    lock.lock();
                    try {
                        while (buf.isEmpty()) notEmpty.await();
                        out.add(buf.removeFirst());
                        notFull.signal();
                        consumerDone.countDown();
                    } finally { lock.unlock(); }
                }
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });

        producer.join(10_000);
        consumerDone.await(10, TimeUnit.SECONDS);
        consumer.join(10_000);
        return List.copyOf(out);
    }

    public static String casAlternative() {
        return "a CAS loop on an index pair could do it, but Condition queues express the wait logic more clearly";
    }
}
""", wrong=r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.locks.*;

public class Solution {
    public static List<Integer> runBuffer() throws Exception {
        ReentrantLock lock = new ReentrantLock();
        Condition notFull = lock.newCondition();
        Condition notEmpty = lock.newCondition();
        ArrayDeque<Integer> buf = new ArrayDeque<>();
        final int CAP = 2;

        CountDownLatch consumerDone = new CountDownLatch(5);
        CopyOnWriteArrayList<Integer> out = new CopyOnWriteArrayList<>();

        Thread producer = Thread.ofVirtual().start(() -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    lock.lock();
                    try {
                        if (buf.size() == CAP) notFull.await();   // WRONG: `if` not `while`
                        buf.addLast(i);
                        notEmpty.signal();
                    } finally { lock.unlock(); }
                }
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });

        Thread consumer = Thread.ofVirtual().start(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    lock.lock();
                    try {
                        if (buf.isEmpty()) notEmpty.await();      // WRONG: `if` not `while`
                        out.add(buf.removeFirst());
                        notFull.signal();
                        consumerDone.countDown();
                    } finally { lock.unlock(); }
                }
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        });

        producer.join(10_000);
        consumerDone.await(10, TimeUnit.SECONDS);
        consumer.join(10_000);
        return List.copyOf(out);
    }

    public static String casAlternative() {
        return "CAS is always better";   // WRONG: overclaims
    }
}
""")

print("module 4 authored")
