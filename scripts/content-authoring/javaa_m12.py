#!/usr/bin/env python3
"""Java — Advanced — Module 12: javaa-async-deadlines.

Async orchestration with explicit executors (never commonPool by accident),
exception-combinators (exceptionally/handle/whenComplete), time-bounded
futures (orTimeout/completeOnTimeout), and the checkpoint — a deadline-scoped
fan-out where every branch is individually bounded and the whole is bounded
again. Deterministic via injected executors. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "javaa-async-deadlines"

L_EXEC_EN = """
`CompletableFuture.supplyAsync(fn)` runs on the **ForkJoinPool.commonPool** —
a shared, sized-to-cores pool you did not configure and cannot tune from
inside the task. Under load, unrelated features share (and starve) it. The
advanced move: **inject the executor**.

```java
CompletableFuture.supplyAsync(() -> fetch(id), executor);
```

Now the pipeline's concurrency is a *deployment decision*, visible at the
construction site. In tests, inject an executor you control (a fixed pool of
2 makes "these two ran concurrently" observable and deterministic). In
production, inject a pool sized for the workload. The anti-pattern is a
library that hard-wires commonPool deep inside and gives the caller no say.

Executor choice is *also* where virtual threads re-enter: for
blocking-dominated fan-outs, `Executors.newVirtualThreadPerTaskExecutor()`
is the injected executor that scales.
"""
L_EXEC_VI = """
`CompletableFuture.supplyAsync(fn)` chạy trên **ForkJoinPool.commonPool** —
một pool dùng chung, kích thước theo số nhân, mà bạn không cấu hình và không
tune được từ bên trong tác vụ. Dưới tải, các tính năng không liên quan chia sẻ
(và đói) lẫn nhau. Nước đi nâng cao: **tiêm executor**.

```java
CompletableFuture.supplyAsync(() -> fetch(id), executor);
```

Giờ mức đồng thời của pipeline là một *quyết định triển khai*, hiện rõ tại
nơi dựng. Trong test, tiêm một executor bạn điều khiển (pool cố định 2 làm cho
"hai cái này chạy đồng thời" quan sát được và tất định). Trong production,
tiêm pool có kích thước theo workload. Anti-pattern là một thư viện gắn chặt
commonPool sâu bên trong và không cho người gọi tiếng nói.

Lựa chọn executor *cũng* là nơi virtual thread trở lại: cho fan-out阻塞 là
chính, `Executors.newVirtualThreadPerTaskExecutor()` là executor được tiêm
mà mở rộng được.
""".replace("阻塞 là chính", "blocking là chính")

L_COMB_EN = """
Exception-combinators differ in *what* they pass and *what* they return:

- `exceptionally(fn)` — runs only on failure; fn receives the throwable,
  returns a replacement RESULT. Skipped on success.
- `handle(fn)` — runs ALWAYS; fn receives `(result, throwable)` — exactly one
  is null. The universal transform.
- `whenComplete(fn)` — runs always; fn observes `(result, throwable)` but
  CANNOT replace the outcome (returns the same future). Observability.

```java
future.handle((ok, err) -> err == null ? ok : fallback);
```

Chaining recovery on a *dependent* stage: `future.thenApply(...).exceptionally(...)`
recovers failures from BOTH stages — attach recovery at the level you want to
recover from. Attaching `exceptionally` before `thenApply` leaves the map
step exposed.

**Time bounds**: `orTimeout(500, MILLISECONDS)` completes the future
exceptionally (TimeoutException) if it takes longer; `completeOnTimeout(fallback, 500, MILLISECONDS)`
substitutes a value instead. Both schedule internally — no sleeping threads.
"""
L_COMB_VI = """
Các exception-combinator khác nhau ở *cái gì* được truyền và *cái gì* được trả:

- `exceptionally(fn)` — chỉ chạy khi thất bại; fn nhận throwable, trả về RESULT
  thay thế. Bỏ qua khi thành công.
- `handle(fn)` — luôn chạy; fn nhận `(result, throwable)` — đúng một cái là
  null. Phép biến đổi phổ quát.
- `whenComplete(fn)` — luôn chạy; fn quan sát `(result, throwable)` nhưng
  KHÔNG THỂ thay kết quả (trả về chính future đó). Dành cho quan sát.

```java
future.handle((ok, err) -> err == null ? ok : fallback);
```

Gắn phục hồi lên một stage *phụ thuộc*: `future.thenApply(...).exceptionally(...)`
phục hồi thất bại từ CẢ HAI stage — gắn phục hồi ở đúng tầng bạn muốn phục hồi.
Gắn `exceptionally` trước `thenApply` để lộ bước map không được bảo vệ.

**Chặn trên thời gian**: `orTimeout(500, MILLISECONDS)` hoàn thành future một
cách exceptional (TimeoutException) nếu nó chạy quá lâu;
`completeOnTimeout(fallback, 500, MILLISECONDS)` thay bằng một giá trị. Cả hai
lên lịch nội bộ — không có thread nào phải ngủ.
"""

L_DEAD_EN = """
A deadline-scoped fan-out composes three bounds:

1. **Per-branch**: each remote call gets `orTimeout` — one slow dependency
   degrades to ITS fallback, not the whole request's.
2. **Aggregate**: `allOf(...).orTimeout(total, ...)` bounds the *sum* —
   branches can be individually fine while the composition (join order,
   queueing) still overruns.
3. **Join with recovery**: collect with `handle` per future, then join in
   submission order — a map of branch→result where every entry is present
   and every failure is a *value* (\"timeout\", \"error\"), never a thrown
   exception escaping the aggregator.

```java
List<CompletableFuture<String>> branches = ids.stream()
    .map(id -> supplyAsync(() -> call(id), exec)
        .orTimeout(50, MILLISECONDS)
        .handle((r, e) -> e == null ? r : "down"))
    .toList();
allOf(branches).join();           // bounded aggregate
return branches.stream().map(CompletableFuture::join).toList();
```

The result: partial success is a *structured outcome* the caller can reason
about, not a lottery between one caller's timeout policy and another's.

One JDK subtlety the aggregator must survive: a task's own exception reaches
`handle` **wrapped** in `CompletionException`, while `orTimeout`'s
`TimeoutException` arrives **raw**. Robust code unwraps one level before
classifying:

```java
Throwable ex = (e instanceof CompletionException && e.getCause() != null)
    ? e.getCause() : e;
```
"""
L_DEAD_VI = """
Fan-out có hạn chót ghép ba chặn trên:

1. **Theo nhánh**: mỗi lời gọi từ xa nhận `orTimeout` — một dependency chậm
   suy biến thành fallback CỦA CHÍNH NÓ, không phải của cả yêu cầu.
2. **Tổng hợp**: `allOf(...).orTimeout(total, ...)` chặn trên *tổng* — từng
   nhánh có thể ổn trong khi composition (thứ tự join, xếp hàng) vẫn vượt hạn.
3. **Join kèm phục hồi**: thu thập bằng `handle` cho từng future, rồi join theo
   thứ tự nộp — một danh sách kết quả mà mọi phần tử đều có mặt, mọi thất bại
   là một *giá trị* (\"timeout\", \"error\"), không bao giờ là exception thoát ra
   khỏi bộ tổng hợp.

```java
List<CompletableFuture<String>> branches = ids.stream()
    .map(id -> supplyAsync(() -> call(id), exec)
        .orTimeout(50, MILLISECONDS)
        .handle((r, e) -> e == null ? r : "down"))
    .toList();
allOf(branches).join();           // tổng hợp có chặn trên
return branches.stream().map(CompletableFuture::join).toList();
```

Kết quả: thành công một phần là *kết quả có cấu trúc* mà người gọi lý giải
được, không phải một trò xổ số giữa chính sách timeout của người gọi này với
người gọi kia.

Một chi tiết tinh vi của JDK mà bộ tổng hợp phải sống sót qua: exception của
chính tác vụ tới `handle` được **bọc** trong `CompletionException`, trong khi
`TimeoutException` của `orTimeout` tới **trần trụi**. Code vững chắc mở bọc
một tầng trước khi phân loại:

```java
Throwable ex = (e instanceof CompletionException && e.getCause() != null)
    ? e.getCause() : e;
```
"""

write_module(
    M, "Async & Deadlines",
    "Injected executors, exception-combinators, time-bounded futures, and deadline-scoped fan-outs.",
    "Async & Hạn chót",
    "Executor được tiêm, exception-combinator, future có chặn trên thời gian, và fan-out có hạn chót.",
    ["javaa-async-executors", "javaa-exception-combinators", "javaa-deadline-fanout"],
    ["javaa-p12-async"],
)

write_lesson(M, "javaa-async-executors",
    "Inject the executor",
    "Why commonPool is not yours, and how injected executors make concurrency a deployment decision.",
    15, L_EXEC_EN,
    "Tiêm executor",
    "Vì sao commonPool không phải của bạn, và executor được tiém biến mức đồng thời thành quyết định triển khai.".replace("tiém", "tiêm"),
    L_EXEC_VI)

write_lesson(M, "javaa-exception-combinators",
    "Exception-combinators",
    "exceptionally vs handle vs whenComplete, recovery placement, and orTimeout/completeOnTimeout.",
    16, L_COMB_EN,
    "Exception-combinator",
    "exceptionally vs handle vs whenComplete, vị trí gắn phục hồi, và orTimeout/completeOnTimeout.",
    L_COMB_VI)

write_lesson(M, "javaa-deadline-fanout",
    "Deadline-scoped fan-outs",
    "Per-branch bounds, aggregate bounds, and failures collected as values.",
    17, L_DEAD_EN,
    "Fan-out có hạn chót",
    "Chặn trên theo nhánh, chặn trên tổng hợp, và thất bại được thu thập thành giá trị.",
    L_DEAD_VI)

P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_COMB = challenge(
    "javaa-p12-combinators",
    "The three recoveries",
    "1. `static CompletableFuture<String> recovered()` — async throwing IllegalStateException;\n"
    "recover with `exceptionally` returning \"fallback\".\n"
    "2. `static CompletableFuture<String> handled()` — same failing async; recover with\n"
    "`handle` returning \"fallback\" on error, \"ok:\" + result on success.\n"
    "3. `static CompletableFuture<String> observed()` — a SUCCEEDING async (\"value\"), with\n"
    "`whenComplete` appending to a `static List<String> observations` (add \"saw-value\" on\n"
    "success) — return the future; the observation must exist after join.\n"
    "4. `static CompletableFuture<String> onTimeoutFallback()` — async sleeping 200ms then\n"
    "returning \"late\"; bound with `completeOnTimeout(\"fast-fail\", 20, MILLISECONDS)`.",
    P_BOILER,
    [
        ("each combinator does its one job", r"""
checkEq(Solution.recovered().join(), "fallback", "exceptionally replaces");
checkEq(Solution.handled().join(), "fallback", "handle maps the error");
checkEq(Solution.observed().join(), "value", "whenComplete cannot replace");
checkTrue(Solution.observations.contains("saw-value"), "observation recorded");
checkEq(Solution.onTimeoutFallback().join(), "fast-fail", "timeout replaced by value");
""", "Recovery placement is the lesson."),
    ],
    level="independent",
)
CH_COMB_VI = vi_challenge(
    "Ba kiểu phục hồi",
    "recovered/handled/observed/onTimeoutFallback: exceptionally thay thế, handle ánh xạ, whenComplete chỉ quan sát, timeout thành giá trị.",
    [("Mỗi combinator đúng một vai", "Vị trí gắn phục hồi chính là bài học.")],
)

CH_ORDER = challenge(
    "javaa-p12-order",
    "Ordered results from unordered work",
    "1. `static List<Integer> fanout(List<Integer> inputs, Executor executor)` — for each\n"
    "input, `supplyAsync(() -> input * 2, executor)`; after ALL complete (allOf + join),\n"
    "return the results IN SUBMISSION ORDER (join each future in list order).\n"
    "2. `static List<Integer> withFailures(List<Integer> inputs, Executor executor)` — same,\n"
    "but odd inputs THROW; recover per-branch with handle → -1 for failed branches;\n"
    "submission order preserved throughout.\n"
    "Use `var f = CompletableFuture.supplyAsync(...)` per input; never trust join order\n"
    "to equal completion order.",
    P_BOILER,
    [
        ("submission order, per-branch recovery", r"""
java.util.concurrent.Executor e = java.util.concurrent.Executors.newFixedThreadPool(3,
    r -> { Thread t = new Thread(r); t.setDaemon(true); return t; });   // daemon: JVM may exit
checkEq(Solution.fanout(java.util.List.of(1, 2, 3), e), java.util.List.of(2, 4, 6), "ordered doubles");
checkEq(Solution.withFailures(java.util.List.of(1, 2, 3), e), java.util.List.of(-1, 4, -1), "odds recovered");
""", "Results ordered by submission, not by chance."),
    ],
    level="real-world",
)
CH_ORDER_VI = vi_challenge(
    "Kết quả có thứ tự từ công việc không thứ tự",
    "fanout/withFailures: allOf + join theo thứ tự nộp; phục hồi theo nhánh bằng handle; thứ tự không bao giờ trông chờ may mắn.",
    [("Thứ tự nộp, phục hồi theo nhánh", "Kết quả theo thứ tự nộp, không theo may rủi.")],
)

write_practice(M, "javaa-p12-async",
    "Async drills",
    "Recovery placement, ordered collection, and value-shaped timeouts.",
    "Bài tập async",
    "Vị trí phục hồi, thu thập có thứ tự, và timeout có hình giá trị.",
    "javaa-deadline-fanout", 55, "advanced",
    [CH_COMB, CH_ORDER],
    {"javaa-p12-combinators": CH_COMB_VI, "javaa-p12-order": CH_ORDER_VI},
    solutions=[
        ("javaa-p12-combinators", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static final List<String> observations =
        Collections.synchronizedList(new ArrayList<>());

    public static CompletableFuture<String> recovered() {
        return CompletableFuture.<String>supplyAsync(() -> {
            throw new IllegalStateException("boom");
        }).exceptionally(e -> "fallback");
    }

    public static CompletableFuture<String> handled() {
        return CompletableFuture.<String>supplyAsync(() -> {
            throw new IllegalStateException("boom");
        }).handle((ok, err) -> err == null ? "ok:" + ok : "fallback");
    }

    public static CompletableFuture<String> observed() {
        return CompletableFuture.supplyAsync(() -> "value")
            .whenComplete((r, e) -> observations.add("saw-value"));
    }

    public static CompletableFuture<String> onTimeoutFallback() {
        return CompletableFuture.<String>supplyAsync(() -> {
            try { Thread.sleep(200); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            return "late";
        }).completeOnTimeout("fast-fail", 20, TimeUnit.MILLISECONDS);
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public static final List<String> observations =
        Collections.synchronizedList(new ArrayList<>());

    public static CompletableFuture<String> recovered() {
        return CompletableFuture.<String>supplyAsync(() -> {
            throw new IllegalStateException("boom");
        }).whenComplete((r, e) -> { });   // WRONG: whenComplete observes but cannot recover
    }

    public static CompletableFuture<String> handled() {
        return CompletableFuture.<String>supplyAsync(() -> {
            throw new IllegalStateException("boom");
        }).handle((ok, err) -> err == null ? "ok:" + ok : err.getMessage());  // WRONG: leaks the message
    }

    public static CompletableFuture<String> observed() {
        return CompletableFuture.supplyAsync(() -> "value")
            .handle((r, e) -> { observations.add("saw-value"); return "REPLACED"; });  // WRONG: handle replaces the value
    }

    public static CompletableFuture<String> onTimeoutFallback() {
        return CompletableFuture.<String>supplyAsync(() -> "late")
            .orTimeout(20, TimeUnit.MILLISECONDS);   // WRONG: orTimeout makes it EXCEPTIONAL, not a fallback value
    }
}
"""),
        ("javaa-p12-order", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public static List<Integer> fanout(List<Integer> inputs, Executor executor) {
        List<CompletableFuture<Integer>> futures = inputs.stream()
            .map(i -> CompletableFuture.supplyAsync(() -> i * 2, executor))
            .collect(Collectors.toList());
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        return futures.stream().map(CompletableFuture::join).collect(Collectors.toList());
    }

    public static List<Integer> withFailures(List<Integer> inputs, Executor executor) {
        List<CompletableFuture<Integer>> futures = inputs.stream()
            .map(i -> CompletableFuture.<Integer>supplyAsync(() -> {
                if (i % 2 == 1) throw new IllegalStateException("odd");
                return i * 2;
            }, executor).handle((r, e) -> e == null ? r : -1))
            .collect(Collectors.toList());
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
        return futures.stream().map(CompletableFuture::join).collect(Collectors.toList());
    }
}
""", r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public static List<Integer> fanout(List<Integer> inputs, Executor executor) {
        List<CompletableFuture<Integer>> futures = inputs.stream()
            .map(i -> CompletableFuture.supplyAsync(() -> i * 2, executor))
            .collect(Collectors.toList());
        return futures.stream()
            .map(f -> f.join())
            .collect(Collectors.toList());   // WRONG: joins without allOf is fine for order,
    }                                        // but no aggregate bound — see withFailures

    public static List<Integer> withFailures(List<Integer> inputs, Executor executor) {
        List<CompletableFuture<Integer>> futures = inputs.stream()
            .map(i -> CompletableFuture.<Integer>supplyAsync(() -> {
                if (i % 2 == 1) throw new IllegalStateException("odd");
                return i * 2;
            }, executor))                 // WRONG: no per-branch recovery — the first odd id
            .collect(Collectors.toList()); // rethrows at join and the whole fan-out collapses
        return futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());
    }
}
"""),
    ],
)

CP_MD = """
## Checkpoint: the deadline-scoped aggregator

Every branch individually bounded, the whole bounded again, every failure a
value — partial success as a structured outcome.
"""

CP_CH = challenge(
    "javaa-checkpoint-m12-task",
    "Checkpoint: bounded fan-out, collected as values",
    "Inside Solution, implement the deadline aggregator:\n"
    "1. `static List<String> aggregate(List<Integer> ids, Executor executor)` — for each\n"
    "id, run a task that sleeps `id` ms (simulated work) and returns \"id-<id>-ok\" IF\n"
    "id is even; odd ids sleep then throw. Bound EACH branch with\n"
    "`orTimeout(80, MILLISECONDS)` and recover with handle → failure mode string:\n"
    "\"id-<id>-timeout\" for timeouts, \"id-<id>-error\" for other exceptions.\n"
    "2. Aggregate with allOf(...).orTimeout(500, MILLISECONDS), then join in submission\n"
    "order and return the list. Every id must appear exactly once — failures included.\n"
    "3. `static String philosophy()` returns exactly:\n"
    "\"per-branch bounds degrade dependencies; the aggregate bound protects the caller;\n"
    "failures are values\".",
    P_BOILER,
    [
        ("every branch yields a value", r"""
java.util.concurrent.Executor e = java.util.concurrent.Executors.newVirtualThreadPerTaskExecutor();
java.util.List<String> out = Solution.aggregate(java.util.List.of(10, 30, 200, 7), e);
checkEq(out.size(), 4, "one entry per id");
checkEq(out.get(0), "id-10-ok", "fast even succeeds");
checkEq(out.get(1), "id-30-ok", "medium even succeeds");
checkTrue(out.get(2).equals("id-200-timeout"), "200ms exceeds 80ms bound: " + out.get(2));
checkEq(out.get(3), "id-7-error", "odd id errors");
""", "Timeouts and errors are values, in submission order."),
        ("philosophy", r"""
checkEq(Solution.philosophy(),
  "per-branch bounds degrade dependencies; the aggregate bound protects the caller;\nfailures are values",
  "the deadline contract");
""", "Say the three-part contract."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: fan-out có chặn trên, thu thành giá trị",
    "aggregate: mỗi nhánh orTimeout 80ms, handle ánh xạ timeout/error thành chuỗi, allOf + join theo thứ tự nộp; philosophy nêu hợp đồng ba phần.",
    [("Mỗi nhánh cho ra một giá trị", "Timeout và lỗi là giá trị, đúng thứ tự nộp."),
     ("Triết lý", "Nói hợp đồng ba phần.")],
)

write_checkpoint(M, "javaa-checkpoint-m12",
    "Checkpoint: The Deadline-Scoped Aggregator",
    "Per-branch bounds, an aggregate bound, and failures as values.",
    30, CP_MD,
    "Checkpoint: Bộ tổng hợp có hạn chót",
    "Chặn trên theo nhánh, chặn trên tổng hợp, và thất bại thành giá trị.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public static List<String> aggregate(List<Integer> ids, Executor executor) {
        List<CompletableFuture<String>> branches = ids.stream()
            .map(id -> CompletableFuture.<String>supplyAsync(() -> {
                try { Thread.sleep(id); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                if (id % 2 == 1) throw new IllegalStateException("odd " + id);
                return "id-" + id + "-ok";
            }, executor)
                .orTimeout(80, TimeUnit.MILLISECONDS)
                .handle((r, e) -> {
                    if (e == null) return r;
                    Throwable ex = e;
                    if (ex instanceof CompletionException && ex.getCause() != null) {
                        ex = ex.getCause();   // task failures arrive wrapped; orTimeout is raw
                    }
                    return (ex instanceof TimeoutException)
                        ? "id-" + id + "-timeout"
                        : "id-" + id + "-error";
                }))
            .collect(Collectors.toList());
        try {
            CompletableFuture.allOf(branches.toArray(new CompletableFuture[0]))
                .orTimeout(500, TimeUnit.MILLISECONDS).join();
        } catch (CompletionException e) {
            // aggregate bound tripped: leave entries as their handled state
        }
        return branches.stream().map(f -> {
            try { return f.join(); }
            catch (CompletionException e) { return "id-?-error"; }
        }).collect(Collectors.toList());
    }

    public static String philosophy() {
        return "per-branch bounds degrade dependencies; the aggregate bound protects the caller;\nfailures are values";
    }
}
""", wrong=r"""
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class Solution {
    public static List<String> aggregate(List<Integer> ids, Executor executor) {
        List<CompletableFuture<String>> branches = ids.stream()
            .map(id -> CompletableFuture.<String>supplyAsync(() -> {
                try { Thread.sleep(id); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                if (id % 2 == 1) throw new IllegalStateException("odd " + id);
                return "id-" + id + "-ok";
            }, executor)
                .orTimeout(80, TimeUnit.MILLISECONDS)
                .exceptionally(e -> "id-" + id + "-failed"))   // WRONG: one generic label — timeout vs error lost
            .collect(Collectors.toList());
        return branches.stream()
            .map(f -> f.join())
            .collect(Collectors.toList());   // WRONG: no aggregate bound at all
    }

    public static String philosophy() {
        return "timeouts propagate; callers race their own deadlines";   // WRONG: the anti-contract
    }
}
""")

print("module 12 authored")
