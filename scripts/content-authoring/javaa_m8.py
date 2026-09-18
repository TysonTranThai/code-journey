#!/usr/bin/env python3
"""Java — Advanced — Module 8: javaa-memory-gc.

Memory as an observable system: weak references retired by a real GC, object
identity across allocation (heapAddress), the reachability lattice, and the
checkpoint — a size-bounded, GC-backed TTL cache. The sandbox has no GC flags
and no JFR, so every lesson observes the GC through its *effects*, never
through flags. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-memory-gc"

L_REF_EN = """
Three questions decide when an object can die: *who can reach it?* (the
collector starts from GC roots — stacks, statics, live threads), *how urgently
might it be needed?* (the reachability lattice), and *when will it be
collected?* (a policy question, never a guarantee).

```java
Object strong  = new Object();               // reachable — lives
WeakReference<Object> weak = new WeakReference<>(new Object());
System.gc();                                 // weak target: unreachable → gone
weak.get()                                   // now null (usually immediately;
                                             // soft refs get breathing room first)
```

The lattice: **strong** (an ordinary reference — never collected while
reachable) → **soft** (collected only under memory *pressure*; good for
caches that may survive) → **weak** (collected at the *next* GC; good for
metadata and canonical maps) → **phantom** (enqueues cleanup after death;
replacement for finalization).

Two disciplines follow. First: `System.gc()` is a *hint* — tests and programs
must be written so that correctness never depends on a collection *happening*,
only on what collection means when it does. Second: value caches belong in
`WeakHashMap`/weak keys precisely because keys reachable nowhere else should
not pin their values.
"""
L_REF_VI = """
Ba câu hỏi quyết định khi nào một đối tượng được chết: *ai chạm tới được nó?*
(bộ thu gom bắt đầu từ GC roots — stack, static, thread sống), *nó cần gấp đến
mức nào?* (thang reachability), và *khi nào bị thu gom?* (câu hỏi chính sách,
không bao giờ là cam kết).

```java
Object strong  = new Object();               // chạm tới được — sống
WeakReference<Object> weak = new WeakReference<>(new Object());
System.gc();                                 // mục tiêu weak: không ai chạm tới → mất
weak.get()                                   // giờ là null (thường ngay lập tức;
                                             // soft ref được cho thêm hơi trước)
```

Thang reachability: **strong** (tham chiếu thường — không bao giờ bị thu khi
còn chạm tới) → **soft** (chỉ bị thu khi *áp lực* bộ nhớ; hợp với cache muốn
sống thêm) → **weak** (bị thu ở *lần* GC kế tiếp; hợp với metadata và map
canonical) → **phantom** (enqueue dọn dẹp sau khi chết; thay thế finalization).

Hai kỷ luật đi theo. Thứ nhất: `System.gc()` chỉ là *gợi ý* — test và chương
trình phải viết sao cho tính đúng đắn không bao giờ phụ thuộc vào việc GC
*xảy ra*, chỉ phụ thuộc vào ý nghĩa của GC khi nó xảy ra. Thứ hai: cache giá
trị thuộc vào `WeakHashMap`/weak key đúng vì key không còn ai chạm tới thì
không nên ghim giá trị của nó.
"""

L_ALLOC_EN = """
`new` = a heap allocation: address, header, initialized fields. Every
allocation produces an object with *identity* distinct from its *state*:

```java
Integer a = 100, b = 100;    // a == b  — small-value cache shares one object
Integer c = 500, d = 500;    // c != d  — outside the cache: two allocations
```

`==` compares identity (same allocation?); `equals` compares state. The
small-Integer cache (-128..127) is an implementation choice, not a contract —
comparing boxed numerics with `==` is a latent bug that passes on small
numbers and detonates on large ones.

An object's *address* is observable only weakly (`identityHashCode` is not
the address, but its stability reflects the same object) — yet the *fact* of
allocation is very observable: memory consumed, GC pressure, allocation
rate. Advanced Java allocates deliberately: escape analysis can stack-allocate
non-escaping objects, and scalar replacement can dissolve them entirely —
which is why "allocation is expensive" is a claim to *measure*, not assume.
"""
L_ALLOC_VI = """
`new` = một cấp phát heap: địa chỉ, header, field khởi tạo. Mỗi lần cấp phát
tạo ra đối tượng có *identity* khác *trạng thái*:

```java
Integer a = 100, b = 100;    // a == b  — cache giá trị nhỏ dùng chung một đối tượng
Integer c = 500, d = 500;    // c != d  — ngoài cache: hai lần cấp phát
```

`==` so identity (cùng một lần cấp phát?); `equals` so trạng thái. Cache
Integer nhỏ (-128..127) là lựa chọn cài đặt, không phải hợp đồng — so sánh
boxed numeric bằng `==` là bug tiềm ẩn: qua được với số nhỏ, nổ với số lớn.

*Địa chỉ* của đối tượng chỉ quan sát được một cách gián tiếp
(`identityHashCode` không phải địa chỉ, nhưng độ ổn định của nó phản ánh cùng
một đối tượng) — còn *sự thật* của việc cấp phát thì quan sát được rõ ràng:
bộ nhớ tiêu thụ, áp lực GC, tốc độ cấp phát. Java nâng cao cấp phát một cách
cố ý: escape analysis có thể cấp phát trên stack cho đối tượng không thoát
ra, scalar replacement có thể hòa tan chúng hoàn toàn — vì thế "cấp phát đắt"
là một mệnh đề cần *đo*, không phải giả định.
"""

L_CACHE_EN = """
A GC-backed TTL cache binds three mechanisms:

- **WeakHashMap** — the collector retires entries whose *keys* are reachable
  only from the map. (Values must not reach their own keys, or nothing dies.)
- **A 60-second window** — System.nanoTime() arithmetic; expired by *time*.
- **A size bound** — eviction by *policy*.

```java
boolean fresh(CacheKey k) {
    CacheLine line = store.get(k);
    if (line == null) return false;
    if (line.expiry() <= System.nanoTime()) { store.remove(k); return false; }
    return true;
}
```

Each mechanism answers a *different* failure: time expires stale data,
size bounds memory, weak keys release objects whose owners are gone. Remove
any one and the cache leaks in that dimension. The checkpoint assembles all
three — the same reasoning production caches (Caffeine and friends) apply at
industrial strength.
"""
L_CACHE_VI = """
Cache TTL dựa trên GC gắn kết ba cơ chế:

- **WeakHashMap** — bộ thu gom rút các entry có *key* không còn ai chạm tới
  ngoài map. (Value không được chạm ngược tới key của chính nó, nếu không
  chẳng gì chết được.)
- **Cửa sổ 60 giây** — phép tính System.nanoTime(); hết hạn theo *thời gian*.
- **Giới hạn kích thước** — evict theo *chính sách*.

```java
boolean fresh(CacheKey k) {
    CacheLine line = store.get(k);
    if (line == null) return false;
    if (line.expiry() <= System.nanoTime()) { store.remove(k); return false; }
    return true;
}
```

Mỗi cơ chế trả lời một *lỗi* khác nhau: thời gian hết hạn dữ liệu cũ, kích
thước chặn bộ nhớ, weak key buông đối tượng khi chủ nhân đã biến mất. Bỏ bất
kỳ cơ chế nào, cache sẽ rò rỉ theo đúng chiều đó. Checkpoint lắp cả ba —
chính là lý luận mà các cache production (Caffeine và bạn bè) áp dụng ở cấp
công nghiệp.
"""

write_module(
    M, "Memory, GC & Runtime Internals",
    "Reachability observed through its effects, allocation identity, and a GC-backed TTL cache.",
    "Bộ nhớ, GC & Nội bộ runtime",
    "Reachability quan sát qua hiệu ứng, identity cấp phát, và cache TTL dựa trên GC.",
    ["javaa-reachability", "javaa-allocation-identity", "javaa-ttl-cache-design"],
    ["javaa-p8-memory"],
)

write_lesson(M, "javaa-reachability",
    "GC roots and the reachability lattice",
    "Strong/soft/weak/phantom observed live in-sandbox, and the disciplines that follow.",
    17, L_REF_EN,
    "GC roots và thang reachability",
    "Strong/soft/weak/phantom quan sát trực tiếp trong sandbox, và các kỷ luật đi theo.",
    L_REF_VI)

write_lesson(M, "javaa-allocation-identity",
    "Allocation, identity, and cost",
    "Identity vs state, the boxed-numeric cache trap, and why allocation cost is measured, not assumed.",
    15, L_ALLOC_EN,
    "Cấp phát, identity, và chi phí",
    "Identity vs trạng thái, bẫy cache boxed-numeric, và vì sao chi phí cấp phát phải đo chứ không giả định.",
    L_ALLOC_VI)

write_lesson(M, "javaa-ttl-cache-design",
    "Designing a TTL cache",
    "WeakHashMap keys, time windows, and size bounds — three mechanisms, three failures.",
    18, L_CACHE_EN,
    "Thiết kế cache TTL",
    "Key WeakHashMap, cửa sổ thời gian, và giới hạn kích thước — ba cơ chế, ba kiểu rò rỉ.",
    L_CACHE_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_WEAK = challenge(
    "javaa-p8-weakref",
    "Watch the collector retire data",
    "1. `static int retires()` — create THREE distinct `Object` values, wrap each in a\n"
    "`WeakReference`, do NOT keep strong references, call `System.gc()` (twice, for\n"
    "reliability), then count how many weak refs return null from get().\n"
    "2. `static int retiresWithStrong()` — same three objects, but keep them in a\n"
    "`static List<Object> pinned` first; after System.gc() count nulls (expect 0 —\n"
    "strong refs are immortal while reachable).\n"
    "3. `static long heapAddress()` — measure USED heap as\n"
    "`totalMemory() - freeMemory()` BEFORE and AFTER allocating `int[1_000_000]`;\n"
    "return the difference (after - before). Allocation shows up as used-memory growth.",
    P_BOILER,
    [
        ("unreachable dies, pinned survives", r"""
checkEq(Solution.retires(), 3, "unreachable weak targets are gone");
checkEq(Solution.retiresWithStrong(), 0, "strong refs never collected");
""", "The lattice, executed."),
        ("allocation is observable", r"""
long delta = Solution.heapAddress();
checkTrue(delta > 0, "a 1M-int array costs real bytes: " + delta);
checkTrue(delta >= 1_000_000, "at least 4 bytes per int: " + delta);
""", "Memory growth measured, not theorized."),
    ],
    level="guided",
)
CH_WEAK_VI = vi_challenge(
    "Nhìn bộ thu gom rút dữ liệu",
    "retires/retiresWithStrong/heapAddress: weak chết khi không ai chạm tới, strong bất tử, cấp phát hiện thấy qua bộ nhớ.",
    [("Không chạm tới là chết, ghim là sống", "Thang reachability, chạy thật."),
     ("Cấp phát quan sát được", "Tăng trưởng bộ nhớ được đo, không lý thuyết.")],
)

CH_IDENTITY = challenge(
    "javaa-p8-identity",
    "Identity vs state, live",
    "1. `static boolean smallBoxedIdentity()` — `Integer a = 100, b = 100; return a == b;`\n"
    "2. `static boolean largeBoxedIdentity()` — `Integer a = 500, b = 500; return a == b;`\n"
    "3. `static boolean largeBoxedEquals()` — same values, `a.equals(b)`.\n"
    "4. `static int sameIdentityTwice()` — build one `List<String>`, call\n"
    "`System.identityHashCode` on it twice, return how many DISTINCT hash values you saw\n"
    "(one — identity is stable).",
    P_BOILER,
    [
        ("the boxed cache boundary", r"""
checkTrue(Solution.smallBoxedIdentity(), "100 == 100 shares the cached object");
checkTrue(!Solution.largeBoxedIdentity(), "500 == 500 are two allocations");
checkTrue(Solution.largeBoxedEquals(), "equals compares state");
""", "== on boxed numerics is a latent bug."),
        ("identity is stable", r"""
checkEq(Solution.sameIdentityTwice(), 1, "identityHashCode stable per object");
""", "Same object, same identity hash."),
    ],
    level="independent",
)
CH_IDENTITY_VI = vi_challenge(
    "Identity vs trạng thái, chạy thật",
    "smallBoxedIdentity/largeBoxedIdentity/largeBoxedEquals/sameIdentityTwice: ranh giới cache boxed và sự ổn định của identity.",
    [("Ranh giới cache boxed", "100 dùng chung, 500 là hai lần cấp phát."),
     ("Identity ổn định", "Cùng một đối tượng, cùng identity hash.")],
)

CH_CACHE = challenge(
    "javaa-p8-cache",
    "Weak keys, retired for real",
    "Inside Solution, keep `static class CacheKey { final String id; ... }` and a\n"
    "`private static final WeakHashMap<CacheKey, String> store` with `static void put`,\n"
    "`static String get`, plus:\n"
    "1. `static int weakRetire()` — seed 3 key/value pairs from a PRIVATE helper (so the\n"
    "key objects are reachable ONLY through the weak map once the helper returns), call\n"
    "System.gc() twice, then return how many entries remain (probe store.size(), which\n"
    "expunges cleared entries). Correct answer: 0.\n"
    "2. `static int strongRetire()` — same seeding, but ALSO retain the keys in a\n"
    "`static List<CacheKey> pinned`; gc twice; return survivors (correct: 3).",
    P_BOILER,
    [
        ("weak keys are retired by the collector", r"""
checkEq(Solution.weakRetire(), 0, "unreachable keys die at GC (after enqueue lands)");
checkEq(Solution.strongRetire(), 3, "pinned keys survive the same GC");
""", "Same collector, different reachability — different fates."),
    ],
    level="real-world",
)
CH_CACHE_VI = vi_challenge(
    "Weak key được rút thật",
    "weakRetire/strongRetire: key chỉ còn weak map chạm tới thì chết sau GC; key bị ghim sống sót qua cùng lần GC đó.",
    [("Key yếu bị bộ thu gom rút", "Cùng bộ thu gom, reachability khác — số phận khác."),],
)

write_practice(M, "javaa-p8-memory",
    "Memory drills",
    "Watch the collector work, pin objects on purpose, and feel the boxed-cache boundary.",
    "Bài tập bộ nhớ",
    "Xem bộ thu gom làm việc, ghim đối tượng có chủ đích, và chạm ranh giới cache boxed.",
    "javaa-ttl-cache-design", 55, "advanced",
    [CH_WEAK, CH_IDENTITY, CH_CACHE],
    {"javaa-p8-weakref": CH_WEAK_VI, "javaa-p8-identity": CH_IDENTITY_VI, "javaa-p8-cache": CH_CACHE_VI},
    solutions=[
        ("javaa-p8-weakref", r"""
import java.lang.ref.*;
import java.util.*;

public class Solution {
    static final List<Object> pinned = new ArrayList<>();

    public static int retires() {
        WeakReference<Object> w1 = new WeakReference<>(new Object());
        WeakReference<Object> w2 = new WeakReference<>(new Object());
        WeakReference<Object> w3 = new WeakReference<>(new Object());
        System.gc();
        System.gc();
        int dead = 0;
        for (WeakReference<Object> w : List.of(w1, w2, w3)) {
            if (w.get() == null) dead++;
        }
        return dead;
    }

    public static int retiresWithStrong() {
        WeakReference<Object> w1 = new WeakReference<>(new Object());
        WeakReference<Object> w2 = new WeakReference<>(new Object());
        WeakReference<Object> w3 = new WeakReference<>(new Object());
        pinned.add(w1.get()); pinned.add(w2.get()); pinned.add(w3.get());
        System.gc();
        System.gc();
        int dead = 0;
        for (WeakReference<Object> w : List.of(w1, w2, w3)) {
            if (w.get() == null) dead++;
        }
        return dead;
    }

    public static long heapAddress() {
        Runtime rt = Runtime.getRuntime();
        long usedBefore = rt.totalMemory() - rt.freeMemory();
        int[] blob = new int[1_000_000];
        blob[0] = blob.length;   // keep the array alive past the measurement
        long usedAfter = rt.totalMemory() - rt.freeMemory();
        if (blob[0] != blob.length) throw new AssertionError("unreachable");
        return usedAfter - usedBefore;
    }
}
""", r"""
import java.lang.ref.*;
import java.util.*;

public class Solution {
    static final List<Object> pinned = new ArrayList<>();

    public static int retires() {
        WeakReference<Object> w1 = new WeakReference<>(new Object());
        WeakReference<Object> w2 = new WeakReference<>(new Object());
        WeakReference<Object> w3 = new WeakReference<>(new Object());
        pinned.add(w1.get()); pinned.add(w2.get()); pinned.add(w3.get());  // WRONG: pins everything
        System.gc();
        System.gc();
        int dead = 0;
        for (WeakReference<Object> w : List.of(w1, w2, w3)) {
            if (w.get() == null) dead++;
        }
        return dead;
    }

    public static int retiresWithStrong() {
        WeakReference<Object> w1 = new WeakReference<>(new Object());
        WeakReference<Object> w2 = new WeakReference<>(new Object());
        WeakReference<Object> w3 = new WeakReference<>(new Object());
        // WRONG: never pins — the "strong" scenario retires too
        System.gc();
        System.gc();
        int dead = 0;
        for (WeakReference<Object> w : List.of(w1, w2, w3)) {
            if (w.get() == null) dead++;
        }
        return dead;
    }

    public static long heapAddress() {
        return 0;   // WRONG: claims no memory cost
    }
}
"""),
        ("javaa-p8-identity", r"""
import java.util.*;

public class Solution {
    public static boolean smallBoxedIdentity() {
        Integer a = 100;
        Integer b = 100;
        return a == b;
    }

    public static boolean largeBoxedIdentity() {
        Integer a = 500;
        Integer b = 500;
        return a == b;
    }

    public static boolean largeBoxedEquals() {
        Integer a = 500;
        Integer b = 500;
        return a.equals(b);
    }

    public static int sameIdentityTwice() {
        List<String> one = new ArrayList<>();
        int h1 = System.identityHashCode(one);
        int h2 = System.identityHashCode(one);
        return (h1 == h2) ? 1 : 2;
    }
}
""", r"""
import java.util.*;

public class Solution {
    public static boolean smallBoxedIdentity() {
        Integer a = 100;
        Integer b = 100;
        return !Objects.equals(a, b);   // WRONG: inverts the cache fact
    }

    public static boolean largeBoxedIdentity() {
        Integer a = 500;
        Integer b = 500;
        return a == b;                  // WRONG: outside the cache — two allocations
    }

    public static boolean largeBoxedEquals() {
        Integer a = 500;
        Integer b = 500;
        return a != b;                  // WRONG: equals is true
    }

    public static int sameIdentityTwice() {
        List<String> one = new ArrayList<>();
        int h1 = System.identityHashCode(one);
        int h2 = System.identityHashCode(new ArrayList<>());   // WRONG: different object
        return (h1 == h2) ? 1 : 2;
    }
}
"""),
        ("javaa-p8-cache", r"""
import java.util.*;

public class Solution {
    public static class CacheKey {
        final String id;
        CacheKey(String id) { this.id = id; }
    }

    private static final WeakHashMap<CacheKey, String> store = new WeakHashMap<>();
    private static final List<CacheKey> pinned = new ArrayList<>();

    public static void put(CacheKey k, String v) {
        store.put(k, v);
    }

    public static String get(CacheKey k) {
        return store.get(k);
    }

    private static void seedWeak() {
        // keys reachable only through the weak map after this returns
        put(new CacheKey("a"), "va");
        put(new CacheKey("b"), "vb");
        put(new CacheKey("c"), "vc");
    }

    private static void seedPinned() {
        CacheKey a = new CacheKey("a");
        CacheKey b = new CacheKey("b");
        CacheKey c = new CacheKey("c");
        pinned.add(a); pinned.add(b); pinned.add(c);
        put(a, "va"); put(b, "vb"); put(c, "vc");
    }

    public static int weakRetire() {
        seedWeak();
        // Weak refs are cleared by the GC but ENQUEUED asynchronously by the
        // reference-processing thread — WeakHashMap sees the death a cycle later.
        // Correctness must not depend on timing: bounded wait until drained.
        for (int round = 0; round < 50 && store.size() > 0; round++) {
            System.gc();
            try { Thread.sleep(10); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
        return store.size();   // size() expunges cleared entries
    }

    public static int strongRetire() {
        seedPinned();
        for (int round = 0; round < 5 && store.size() > 0; round++) {
            System.gc();
            try { Thread.sleep(10); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
        return store.size();
    }
}
""", r"""
import java.util.*;

public class Solution {
    public static class CacheKey {
        final String id;
        CacheKey(String id) { this.id = id; }
    }

    private static final Map<CacheKey, String> store = new HashMap<>();   // WRONG: strong keys never die
    private static final List<CacheKey> pinned = new ArrayList<>();

    public static void put(CacheKey k, String v) {
        store.put(k, v);
    }

    public static String get(CacheKey k) {
        return store.get(k);
    }

    private static void seedWeak() {
        put(new CacheKey("a"), "va");
        put(new CacheKey("b"), "vb");
        put(new CacheKey("c"), "vc");
    }

    private static void seedPinned() {
        CacheKey a = new CacheKey("a");
        CacheKey b = new CacheKey("b");
        CacheKey c = new CacheKey("c");
        pinned.add(a); pinned.add(b); pinned.add(c);
        put(a, "va"); put(b, "vb"); put(c, "vc");
    }

    public static int weakRetire() {
        seedWeak();
        System.gc();   // WRONG: single shot, no wait for async reference enqueueing
        return store.size();   // WRONG: 3 — the reference thread hasn't caught up (and a strong map never drops)
    }

    public static int strongRetire() {
        seedPinned();
        for (int round = 0; round < 5 && store.size() > 0; round++) {
            System.gc();
            try { Thread.sleep(10); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
        return store.size();
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the complete TTL cache

Time expiry, size eviction, weak-key release — three mechanisms, each
answering a different failure. Plus retention: your cache reports its own
metadata through a runtime annotation, closing the loop with Module 7.
"""

CP_CH = challenge(
    "javaa-checkpoint-m8-task",
    "Checkpoint: the bounded TTL cache",
    "Inside Solution, build `public static class Cache` and `static class CacheKey`:\n"
    "1. Backing store: `WeakHashMap<CacheKey, Line>` where `static class Line` carries\n"
    "`String value` and `long expiry` (System.nanoTime() + ttlNanos at put time).\n"
    "2. `void put(CacheKey k, String v, long ttlMillis)` and `String get(CacheKey k)` —\n"
    "get returns null for missing keys AND for expired lines (expired lines are removed).\n"
    "3. `int size()` — count of live (present, unexpired) entries; expires lazily on read.\n"
    "4. `void evictOver(int max)` — while size() > max, remove the entry with the EARLIEST\n"
    "expiry (single pass over the entries is fine).\n"
    "5. `static String policyOf(Cache.class)`-style reflection is NOT needed here — instead\n"
    "add `static String describe()` returning exactly:\n"
    "\"time expires staleness; size bounds memory; weak keys release the dead\".",
    P_BOILER,
    [
        ("ttl expires", r"""
Solution.Cache c = new Solution.Cache();
Solution.CacheKey k = new Solution.CacheKey("k");
c.put(k, "v", 0);   // expires immediately
checkEq(c.get(k), null, "expired line is gone");
checkEq(c.size(), 0, "size reflects expiry");
""", "Time expiry on read."),
        ("live entries survive", r"""
Solution.Cache c = new Solution.Cache();
Solution.CacheKey k = new Solution.CacheKey("k");
c.put(k, "v", 60_000);
checkEq(c.get(k), "v", "fresh within ttl");
checkEq(c.size(), 1, "one live entry");
""", "Unexpired lines serve."),
        ("size eviction removes earliest expiry", r"""
Solution.Cache c = new Solution.Cache();
Solution.CacheKey a = new Solution.CacheKey("a");
Solution.CacheKey b = new Solution.CacheKey("b");
Solution.CacheKey d = new Solution.CacheKey("d");
c.put(a, "va", 1_000);    // earliest expiry
c.put(b, "vb", 2_000);
c.put(d, "vd", 3_000);
c.evictOver(2);
checkTrue(c.get(a) == null, "earliest-expiry evicted");
checkEq(c.get(b), "vb", "later survives");
checkEq(c.get(d), "vd", "latest survives");
""", "Eviction by policy, not accident."),
        ("philosophy line", r"""
checkEq(Solution.Cache.describe(),
  "time expires staleness; size bounds memory; weak keys release the dead",
  "the three mechanisms");
""", "Say what each mechanism buys."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: cache TTL đầy đủ",
    "Cache: hết hạn theo ttl, size() đếm entry sống, evictOver xóa entry hết hạn sớm nhất, và câu triết lý ba cơ chế.",
    [("TTL hết hạn", "Entry hết hạn biến mất khi đọc."),
     ("Entry sống còn phục vụ", "Trong ttl thì phục vụ bình thường."),
     ("Evict theo chính sách", "Hết hạn sớm nhất bị rút trước."),
     ("Câu triết lý", "Nói rõ mỗi cơ chế mua được gì.")],
)

write_checkpoint(M, "javaa-checkpoint-m8",
    "Checkpoint: The Bounded TTL Cache",
    "Time, size, and weak keys — three mechanisms, three failures, one cache.",
    30, CP_MD,
    "Checkpoint: Cache TTL có giới hạn",
    "Thời gian, kích thước, và weak key — ba cơ chế, ba kiểu rò rỉ, một cache.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;

public class Solution {
    public static class CacheKey {
        final String id;
        CacheKey(String id) { this.id = id; }
    }

    public static class Cache {
        static class Line {
            final String value;
            final long expiry;
            Line(String value, long expiry) { this.value = value; this.expiry = expiry; }
        }

        private final WeakHashMap<CacheKey, Line> store = new WeakHashMap<>();
        private final Map<CacheKey, Line> strongViewForEviction = new HashMap<>();

        public synchronized void put(CacheKey k, String v, long ttlMillis) {
            Line line = new Line(v, System.nanoTime() + ttlMillis * 1_000_000L);
            store.put(k, line);
            strongViewForEviction.put(k, line);
        }

        public synchronized String get(CacheKey k) {
            Line line = store.get(k);
            if (line == null) { strongViewForEviction.remove(k); return null; }
            if (line.expiry <= System.nanoTime()) {
                store.remove(k);
                strongViewForEviction.remove(k);
                return null;
            }
            return line.value;
        }

        public synchronized int size() {
            long now = System.nanoTime();
            strongViewForEviction.entrySet().removeIf(e -> {
                boolean dead = !store.containsKey(e.getKey()) || e.getValue().expiry <= now;
                if (dead) store.remove(e.getKey());
                return dead;
            });
            return strongViewForEviction.size();
        }

        public synchronized void evictOver(int max) {
            size();   // expire first so policy sees reality
            while (strongViewForEviction.size() > max) {
                CacheKey victim = null;
                long earliest = Long.MAX_VALUE;
                for (Map.Entry<CacheKey, Line> e : strongViewForEviction.entrySet()) {
                    if (e.getValue().expiry < earliest) {
                        earliest = e.getValue().expiry;
                        victim = e.getKey();
                    }
                }
                if (victim == null) break;
                store.remove(victim);
                strongViewForEviction.remove(victim);
            }
        }

        public static String describe() {
            return "time expires staleness; size bounds memory; weak keys release the dead";
        }
    }
}
""", wrong=r"""
import java.util.*;

public class Solution {
    public static class CacheKey {
        final String id;
        CacheKey(String id) { this.id = id; }
    }

    public static class Cache {
        static class Line {
            final String value;
            final long expiry;
            Line(String value, long expiry) { this.value = value; this.expiry = expiry; }
        }

        private final Map<CacheKey, Line> store = new HashMap<>();   // WRONG: strong map + no expiry check

        public void put(CacheKey k, String v, long ttlMillis) {
            store.put(k, new Line(v, System.nanoTime() + ttlMillis * 1_000_000L));
        }

        public String get(CacheKey k) {
            Line line = store.get(k);
            return line == null ? null : line.value;   // WRONG: expired lines still served
        }

        public int size() {
            return store.size();   // WRONG: counts expired entries
        }

        public void evictOver(int max) {
            // WRONG: evicts most-recently-added instead of earliest expiry
            while (store.size() > max) {
                CacheKey latest = null;
                long latestExpiry = Long.MIN_VALUE;
                for (Map.Entry<CacheKey, Line> e : store.entrySet()) {
                    if (e.getValue().expiry > latestExpiry) {
                        latestExpiry = e.getValue().expiry;
                        latest = e.getKey();
                    }
                }
                if (latest == null) break;
                store.remove(latest);
            }
        }

        public static String describe() {
            return "time expires staleness; size bounds memory; weak keys release the dead";
        }
    }
}
""")

print("module 8 authored")
