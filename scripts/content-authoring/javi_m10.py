#!/usr/bin/env python3
"""Java — Intermediate — Module 10: java-async-http.

CompletableFuture composition (supplyAsync/thenApply/thenCombine/
exceptionally, allOf) and the HTTP client taught behind an injectable
transport interface — the sandbox has no network, so the transport is a
test double by design, exactly like professional HTTP testing. House
conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-async-http"

# ── lesson 10.1 — CompletableFuture composition ────────────────────────────
L_CF_EN = r"""
## CompletableFuture: composing async work

A `Future` only *waits*. A `CompletableFuture` *composes*:

```java
CompletableFuture<Integer> price =
    CompletableFuture.supplyAsync(() -> fetchPrice("USD"))
        .thenApply(p -> p * 100)               // transform
        .thenCombine(otherFuture, Integer::sum) // join two pipelines
        .exceptionally(ex -> -1);               // fallback value
```

Mental model: a chain of stages; each runs when its inputs complete.
- `supplyAsync` — start from a value produced on another thread
- `thenApply` — map the value
- `thenCompose` — chain a *dependent* async call (flatMap)
- `thenCombine` — merge two independent chains
- `allOf` / `anyOf` — wait for many / first
- `exceptionally` / `handle` — recover or transform failures

Golden rule: an exception skips forward to the nearest recovery stage —
one `exceptionally` at the end of a chain covers every step above it.
Default executor is the common ForkJoinPool; pass your own executor when
task isolation matters.
"""

L_CF_VI = r"""
## CompletableFuture: soạn async work

`Future` chỉ *chờ*. `CompletableFuture` *soạn đồ*:

```java
CompletableFuture<Integer> price =
    CompletableFuture.supplyAsync(() -> fetchPrice("USD"))
        .thenApply(p -> p * 100)               // biến đổi
        .thenCombine(otherFuture, Integer::sum) // nối hai pipeline
        .exceptionally(ex -> -1);               // giá trị dự phòng
```

Mô hình tâm trí: một chuỗi stage; mỗi stage chạy khi đầu vào của nó hoàn
tất.
- `supplyAsync` — bắt đầu từ giá trị sinh trên thread khác
- `thenApply` — map giá trị
- `thenCompose` — nối một async call *phụ thuộc* (flatMap)
- `thenCombine` — trộn hai chuỗi độc lập
- `allOf` / `anyOf` — chờ nhiều / cái đầu tiên
- `exceptionally` / `handle` — phục hồi hoặc biến đổi thất bại

Quy tắc vàng: ngoại lệ nhảy cóc tới stage phục hồi gần nhất — một
`exceptionally` cuối chuỗi phủ mọi bước phía trên.
Executor mặc định là ForkJoinPool chung; truyền executor riêng khi cần
cô lập task.
"""

# ── lesson 10.2 — HTTP client, transport-injected ───────────────────────────
L_HTTP_EN = r"""
## The HTTP client behind a seam

`java.net.http.HttpClient` (Java 11+) is the modern client:

```java
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(5))
    .build();

HttpRequest req = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users/1"))
    .header("Accept", "application/json")
    .timeout(Duration.ofSeconds(3))
    .GET()
    .build();

HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
if (res.statusCode() == 200) { /* body via res.body() */ }
```

But this course *never* puts a live client in a test — no network in the
sandbox, and unit tests shouldn't need one anyway. The professional shape
is the same as Module 8's Clock seam:

```java
public interface HttpTransport {
    HttpResponse<String> send(HttpRequest req) throws Exception;
}
```

The service takes a transport; tests inject a canned-response transport.
Everything about HTTP — status codes, headers, timeouts, retries — is
then exercised deterministically. Real `HttpClient` usage belongs in
integration tests on machines with a network.
"""

L_HTTP_VI = r"""
## HTTP client sau một seam

`java.net.http.HttpClient` (Java 11+) là client hiện đại:

```java
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(5))
    .build();

HttpRequest req = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users/1"))
    .header("Accept", "application/json")
    .timeout(Duration.ofSeconds(3))
    .GET()
    .build();

HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
if (res.statusCode() == 200) { /* body qua res.body() */ }
```

Nhưng khóa học này *không bao giờ* đặt client thật vào test — sandbox
không có mạng, và unit test vốn không cần. Dáng nghề nghiệp giống seam
Clock của Module 8:

```java
public interface HttpTransport {
    HttpResponse<String> send(HttpRequest req) throws Exception;
}
```

Service nhận một transport; test tiêm transport trả phản hồi đóng gói
sẵn. Mọi khía cạnh HTTP — status code, header, timeout, retry — đều được
tập một cách xác định. `HttpClient` thật thuộc về integration test trên
máy có mạng.
"""

# ── lesson 10.3 — timeouts, retries, backoff ───────────────────────────────
L_RETRY_EN = r"""
## Timeouts, retries, and backoff

Distributed calls fail; the professional questions are *how long to
wait* and *when to try again*:

- **Timeout every call** — a missing timeout turns a slow dependency
  into a stopped service. `HttpRequest.timeout()`, `Future.get(3, SECONDS)`,
  or `orTimeout()` on a CompletableFuture stage.
- **Retry idempotent operations** — GETs, yes; POST payments, only with
  idempotency keys.
- **Exponential backoff with cap** — 100ms, 200ms, 400ms… capped at a
  few seconds; retry storms make outages worse.
- **Distinguish error classes** — 4xx (your fault) usually isn't
  retryable; 5xx and timeouts usually are; 429 means *slow down*
  (respect Retry-After).

```java
static String getWithRetry(HttpTransport t, HttpRequest req) throws Exception {
    int[] delays = {100, 200, 400};
    for (int attempt = 0; ; attempt++) {
        try {
            HttpResponse<String> res = t.send(req);
            if (res.statusCode() < 500) return res.body();  // don't retry 4xx
            if (attempt == delays.length) throw new IllegalStateException("gave up");
        } catch (java.io.IOException e) {
            if (attempt == delays.length) throw e;
        }
        Thread.sleep(delays[attempt]);
    }
}
```
"""

L_RETRY_VI = r"""
## Timeout, retry, và backoff

Call phân tán thì hỏng; câu hỏi chuyên nghiệp là *chờ bao lâu* và *khi nào
thử lại*:

- **Đặt timeout cho mọi call** — thiếu timeout biến một phụ thuộc chậm
  thành dịch vụ đứng hình. `HttpRequest.timeout()`,
  `Future.get(3, SECONDS)`, hoặc `orTimeout()` trên stage
  CompletableFuture.
- **Retry thao tác idempotent** — GET thì có; POST thanh toán chỉ khi có
  idempotency key.
- **Exponential backoff có trần** — 100ms, 200ms, 400ms… trần vài giây;
  bão retry khiến sự cố tệ hơn.
- **Phân loại lỗi** — 4xx (lỗi của bạn) thường không retry được; 5xx và
  timeout thì có; 429 nghĩa là *chậm lại* (tôn trọng Retry-After).

```java
static String getWithRetry(HttpTransport t, HttpRequest req) throws Exception {
    int[] delays = {100, 200, 400};
    for (int attempt = 0; ; attempt++) {
        try {
            HttpResponse<String> res = t.send(req);
            if (res.statusCode() < 500) return res.body();  // đừng retry 4xx
            if (attempt == delays.length) throw new IllegalStateException("gave up");
        } catch (java.io.IOException e) {
            if (attempt == delays.length) throw e;
        }
        Thread.sleep(delays[attempt]);
    }
}
```
"""

write_module(
    MOD,
    "Async Composition & HTTP",
    "CompletableFuture pipelines, the HTTP client behind an injectable transport, and timeout/retry discipline.",
    "Composition bất đồng bộ & HTTP",
    "Pipeline CompletableFuture, HTTP client sau transport khả tiêm, và kỷ luật timeout/retry.",
    ["completablefuture-composition", "http-transport-seam", "timeouts-retries", "javi-checkpoint-async"],
    ["javi-p10-async"],
)

write_lesson(MOD, "completablefuture-composition", "CompletableFuture Composition", "Stage chains, thenCompose vs thenCombine, allOf, and the exception-skips-forward rule.", 15, L_CF_EN, "Composition CompletableFuture", "Chuỗi stage, thenCompose so với thenCombine, allOf, và quy tắc ngoại lệ nhảy cóc tới nơi phục hồi.", L_CF_VI)

write_lesson(MOD, "http-transport-seam", "HTTP Behind a Transport Seam", "java.net.http essentials — and why the service under test takes a transport interface instead.", 14, L_HTTP_EN, "HTTP sau seam transport", "Những điều cốt lõi của java.net.http — và vì sao service được test nhận một interface transport thay thế.", L_HTTP_VI)

write_lesson(MOD, "timeouts-retries", "Timeouts, Retries & Backoff", "Which errors deserve retries, exponential backoff with a cap, and respecting 429/Retry-After.", 14, L_RETRY_EN, "Timeout, Retry & Backoff", "Lỗi nào đáng retry, exponential backoff có trần, và tôn trọng 429/Retry-After.", L_RETRY_VI)

# ── practice set ────────────────────────────────────────────────────────────
P10_BOILER = r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    // Implement methods below.
}
"""

CH_P10_CF = challenge(
    "javi-p10-cf-chain",
    "Compose a Pipeline",
    r"""Implement inside `Solution` (synchronous executor is fine —
`CompletableFuture.completedFuture` chains run inline):
- `static CompletableFuture<Integer> pipeline(int base)`:
  completedFuture(base) → thenApply(x -> x * 2) → thenApply(x -> x + 1)
- `static CompletableFuture<Integer> combine(int a, int b)`:
  thenCombine of two completed pipelines, summed
- `static CompletableFuture<Integer> safeDivide(int a, int b)`:
  completedFuture of a/b inside the chain, `exceptionally` returning -1
  on ArithmeticException

Join results with `.join()` in the tests — completed chains return
immediately.""",
    P10_BOILER,
    [
        (
            "chain transforms in order",
            r"""
checkEq(Solution.pipeline(10).join(), 21, "10*2+1");
""",
            "thenApply stages run in declaration order.",
        ),
        (
            "combine merges two chains",
            r"""
checkEq(Solution.combine(10, 5).join(), 32, "pipeline(10)+pipeline(5)");
""",
            "Each side runs pipeline(), then the results sum.",
        ),
        (
            "exceptionally recovers",
            r"""
checkEq(Solution.safeDivide(7, 0).join(), -1, "div by zero → -1");
checkEq(Solution.safeDivide(8, 2).join(), 4, "normal divide");
""",
            "ArithmeticException routes to the recovery stage.",
        ),
    ],
    level="guided",
)

CH_P10_TRANSPORT = challenge(
    "javi-p10-transport",
    "Service Over a Fake Transport",
    r"""Model in `Solution`:
- `record HttpReply(int status, String body)`
- `interface HttpTransport { HttpReply send(String url); }`
- `static class ApiClient` with constructor `(HttpTransport t)` and
  `String fetchUser(String id)`:
  - sends to `"https://api.test/users/" + id`
  - 200 → returns body
  - 404 → throws NoSuchElementException("user " + id)
  - 5xx → throws IllegalStateException("server error " + status)
- `static HttpTransport fakeTransport(Map<String, HttpReply> replies)` —
  a transport returning the canned reply for the matching URL.

The tests never open a socket; the fake IS the point.""",
    P10_BOILER,
    [
        (
            "happy path returns body",
            r"""
Map<String, Solution.HttpReply> canned = Map.of(
    "https://api.test/users/u1", new Solution.HttpReply(200, "{\"id\":\"u1\"}"));
Solution.ApiClient api = new Solution.ApiClient(Solution.fakeTransport(canned));
checkEq(api.fetchUser("u1"), "{\"id\":\"u1\"}", "body returned");
""",
            "The client must call the transport with the composed URL.",
        ),
        (
            "404 becomes NoSuchElementException",
            r"""
Map<String, Solution.HttpReply> canned = Map.of(
    "https://api.test/users/ghost", new Solution.HttpReply(404, ""));
Solution.ApiClient api = new Solution.ApiClient(Solution.fakeTransport(canned));
try { api.fetchUser("ghost"); checkTrue(false, "must throw"); }
catch (java.util.NoSuchElementException e) { checkTrue(true, "translated"); }
""",
            "404 → NoSuchElementException carrying the id.",
        ),
        (
            "5xx becomes IllegalStateException",
            r"""
Map<String, Solution.HttpReply> canned = Map.of(
    "https://api.test/users/x", new Solution.HttpReply(503, ""));
Solution.ApiClient api = new Solution.ApiClient(Solution.fakeTransport(canned));
try { api.fetchUser("x"); checkTrue(false, "must throw"); }
catch (IllegalStateException e) { checkTrue(e.getMessage().contains("503"), "status in message"); }
""",
            "Server errors surface as IllegalStateException with the status.",
        ),
    ],
    level="independent",
)

CH_P10_RETRY = challenge(
    "javi-p10-retry",
    "Retry with Backoff (Counted, Not Slept)",
    r"""Implement `static int attemptsToSucceed(FlakyTransport t, String url)`
in `Solution`:
- `interface FlakyTransport { int attempt(String url); }` — returns the
  HTTP status it "got": 200, or a 5xx.
- attemptsToSucceed calls attempt() repeatedly until it returns 200
  (immediately retryable: 5xx), with a MAX of 3 retries (4 calls total);
  return the attempt number (1-based) on which 200 arrived, or -1 if
  still failing.
- 4xx stops immediately with -1 (client errors are not retryable).

No Thread.sleep — backoff timing is infrastructure; the *policy* is what
you're implementing.""",
    P10_BOILER,
    [
        (
            "first-try success",
            r"""
Solution.FlakyTransport t = url -> 200;
checkEq(Solution.attemptsToSucceed(t, "x"), 1, "succeeds immediately");
""",
            "One attempt, done.",
        ),
        (
            "retries 5xx then succeeds",
            r"""
int[] calls = {0};
Solution.FlakyTransport t = url -> (calls[0]++ < 2) ? 503 : 200;
checkEq(Solution.attemptsToSucceed(t, "x"), 3, "third attempt");
""",
            "503, 503, 200 → attempt 3.",
        ),
        (
            "gives up after 4 calls",
            r"""
Solution.FlakyTransport t = url -> 500;
checkEq(Solution.attemptsToSucceed(t, "x"), -1, "exhausted");
""",
            "1 initial + 3 retries max.",
        ),
        (
            "4xx never retried",
            r"""
int[] calls = {0};
Solution.FlakyTransport t = url -> { calls[0]++; return 404; };
checkEq(Solution.attemptsToSucceed(t, "x"), -1, "no retry on 404");
checkEq(calls[0], 1, "exactly one call");
""",
            "Client error → immediate -1, one call only.",
        ),
    ],
    level="independent",
)

VI_CH_P10_CF = vi_challenge(
    "Soạn một pipeline",
    r"""Cài bên trong `Solution` (executor đồng bộ là đủ — chuỗi
`CompletableFuture.completedFuture` chạy inline):
- `static CompletableFuture<Integer> pipeline(int base)`:
  completedFuture(base) → thenApply(x -> x * 2) → thenApply(x -> x + 1)
- `static CompletableFuture<Integer> combine(int a, int b)`:
  thenCombine của hai pipeline đã hoàn tất, lấy tổng
- `static CompletableFuture<Integer> safeDivide(int a, int b)`:
  completedFuture của a/b trong chuỗi, `exceptionally` trả -1 khi gặp
  ArithmeticException

Join kết quả bằng `.join()` trong test — chuỗi hoàn tất trả về ngay.""",
    [
        ("Chuỗi biến đổi theo thứ tự", "Các stage thenApply chạy theo thứ tự khai báo."),
        ("combine trộn hai chuỗi", "Mỗi phía chạy pipeline(), rồi hai kết quả cộng lại: 21 + 11 = 32."),
        ("exceptionally phục hồi", "ArithmeticException chuyển tới stage phục hồi."),
    ],
)

VI_CH_P10_TRANSPORT = vi_challenge(
    "Service qua fake transport",
    r"""Mô hình trong `Solution`:
- `record HttpReply(int status, String body)`
- `interface HttpTransport { HttpReply send(String url); }`
- `static class ApiClient` với constructor `(HttpTransport t)` và
  `String fetchUser(String id)`:
  - gửi tới `"https://api.test/users/" + id`
  - 200 → trả body
  - 404 → ném NoSuchElementException("user " + id)
  - 5xx → ném IllegalStateException("server error " + status)
- `static HttpTransport fakeTransport(Map<String, HttpReply> replies)` —
  transport trả phản hồi đóng gói cho URL khớp.

Test không mở socket nào; fake chính là điểm nhấn.""",
    [
        ("Hướng vui trả body", "Client phải gọi transport với URL đã soạn."),
        ("404 thành NoSuchElementException", "404 → NoSuchElementException mang theo id."),
        ("5xx thành IllegalStateException", "Lỗi server lộ ra như IllegalStateException kèm status."),
    ],
)

VI_CH_P10_RETRY = vi_challenge(
    "Retry với backoff (đếm, không ngủ)",
    r"""Cài `static int attemptsToSucceed(FlakyTransport t, String url)`
trong `Solution`:
- `interface FlakyTransport { int attempt(String url); }` — trả status
  HTTP "nhận được": 200, hoặc 5xx.
- attemptsToSucceed gọi attempt() lặp lại cho đến khi nhận 200 (retry
  ngay được: 5xx), TỐI ĐA 3 lần retry (4 call); trả số lần thử (tính từ 1)
  khi 200 xuất hiện, hoặc -1 nếu vẫn hỏng.
- 4xx dừng ngay với -1 (lỗi client không retry).

Không Thread.sleep — thời gian backoff là hạ tầng; *chính sách* mới là
thứ bạn cài.""",
    [
        ("Thành công lần đầu", "Một lần thử, xong."),
        ("Retry 5xx rồi thành công", "503, 503, 200 → lần thử 3."),
        ("Bỏ cuộc sau 4 call", "1 lần đầu + 3 retry tối đa."),
        ("4xx không bao giờ retry", "Lỗi client → -1 ngay, chỉ một call."),
    ],
)

write_practice(
    MOD,
    "javi-p10-async",
    "Async & HTTP Lab",
    "Composable CF pipelines, a client that runs entirely on a fake transport, and counted retry policy.",
    "Xưởng async & HTTP",
    "Pipeline CF có thể soạn, client chạy hoàn toàn trên fake transport, và chính sách retry đếm được.",
    "timeouts-retries",
    40,
    "intermediate",
    [CH_P10_CF, CH_P10_TRANSPORT, CH_P10_RETRY],
    {CH_P10_CF["id"]: VI_CH_P10_CF, CH_P10_TRANSPORT["id"]: VI_CH_P10_TRANSPORT, CH_P10_RETRY["id"]: VI_CH_P10_RETRY},
    solutions=[
        (
            CH_P10_CF["id"],
            r"""
import java.util.concurrent.*;

public class Solution {
    public static CompletableFuture<Integer> pipeline(int base) {
        return CompletableFuture.completedFuture(base)
            .thenApply(x -> x * 2)
            .thenApply(x -> x + 1);
    }

    public static CompletableFuture<Integer> combine(int a, int b) {
        return pipeline(a).thenCombine(pipeline(b), Integer::sum);
    }

    public static CompletableFuture<Integer> safeDivide(int a, int b) {
        return CompletableFuture.completedFuture(a)
            .thenApply(x -> x / b)
            .exceptionally(ex -> -1);
    }
}
""",
            r"""
import java.util.concurrent.*;

public class Solution {
    public static CompletableFuture<Integer> pipeline(int base) {
        return CompletableFuture.completedFuture(base)
            .thenApply(x -> x * 2)
            .thenApply(x -> x + 1);
    }

    public static CompletableFuture<Integer> combine(int a, int b) {
        return pipeline(a).thenCombine(pipeline(b), Integer::sum);
    }

    // W: division happens OUTSIDE the chain — ArithmeticException escapes
    // the pipeline entirely, so exceptionally never runs and join() throws.
    public static CompletableFuture<Integer> safeDivide(int a, int b) {
        return CompletableFuture.completedFuture(a / b)
            .exceptionally(ex -> -1);
    }
}
""",
        ),
        (
            CH_P10_TRANSPORT["id"],
            r"""
import java.util.*;

public class Solution {
    public record HttpReply(int status, String body) {}
    public interface HttpTransport { HttpReply send(String url); }

    public static class ApiClient {
        private final HttpTransport t;
        public ApiClient(HttpTransport t) { this.t = t; }

        public String fetchUser(String id) {
            HttpReply res = t.send("https://api.test/users/" + id);
            if (res.status() == 200) return res.body();
            if (res.status() == 404) throw new java.util.NoSuchElementException("user " + id);
            throw new IllegalStateException("server error " + res.status());
        }
    }

    public static HttpTransport fakeTransport(Map<String, HttpReply> replies) {
        return url -> replies.getOrDefault(url, new HttpReply(404, ""));
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public record HttpReply(int status, String body) {}
    public interface HttpTransport { HttpReply send(String url); }

    public static class ApiClient {
        private final HttpTransport t;
        public ApiClient(HttpTransport t) { this.t = t; }

        // W: treats any non-404 as success and returns the raw status as
        // the body — 200 responses lose their real body and 5xx never
        // becomes an error.
        public String fetchUser(String id) {
            HttpReply res = t.send("https://api.test/users/" + id);
            if (res.status() == 404) throw new java.util.NoSuchElementException("user " + id);
            return String.valueOf(res.status());
        }
    }

    public static HttpTransport fakeTransport(Map<String, HttpReply> replies) {
        return url -> replies.getOrDefault(url, new HttpReply(404, ""));
    }
}
""",
        ),
        (
            CH_P10_RETRY["id"],
            r"""
public class Solution {
    public interface FlakyTransport { int attempt(String url); }

    public static int attemptsToSucceed(FlakyTransport t, String url) {
        int maxCalls = 4;   // 1 initial + 3 retries
        for (int attempt = 1; attempt <= maxCalls; attempt++) {
            int status = t.attempt(url);
            if (status == 200) return attempt;
            if (status >= 400 && status < 500) return -1;   // client error, no retry
        }
        return -1;
    }
}
""",
            r"""
public class Solution {
    public interface FlakyTransport { int attempt(String url); }

    // W: retries 4xx like 5xx — burns all four calls on a permanent
    // client error before giving up. Policy bug the call-count test
    // catches instantly.
    public static int attemptsToSucceed(FlakyTransport t, String url) {
        int maxCalls = 4;
        for (int attempt = 1; attempt <= maxCalls; attempt++) {
            int status = t.attempt(url);
            if (status == 200) return attempt;
        }
        return -1;
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — async & HTTP

You can now: compose async pipelines that recover in the right place,
build clients that run entirely on fake transports, and implement retry
policy that respects error classes. Prove it with an aggregator.
"""

CP_MDX_VI = r"""
## Checkpoint — async & HTTP

Giờ bạn có thể: soạn pipeline async phục hồi đúng chỗ, xây client chạy
hoàn toàn trên fake transport, và cài chính sách retry tôn trọng loại
lỗi. Chứng minh bằng một bộ tổng hợp.
"""

CH_CP10 = challenge(
    "javi-checkpoint-m10-async",
    "Parallel Aggregator",
    r"""Build `Solution`:
- `interface Shard { int fetch(String key); }` — a data shard.
- `static int totalFromAll(List<Shard> shards, String key)` — call every
  shard (sequentially is fine), treating a shard that throws
  RuntimeException as contributing 0 (fault isolation).
- `static CompletableFuture<Integer> asyncTotal(List<Shard> shards,
  String key)` — same semantics via completedFuture/thenApply chains with
  one exceptionally per shard, joined with allOf + sum.

Failures in one shard must not poison the others — that's the contract.""",
    r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public interface Shard { int fetch(String key); }
    // Provide totalFromAll + asyncTotal here.
}
""",
    [
        (
            "healthy shards sum",
            r"""
List<Solution.Shard> shards = List.of(
    k -> 10, k -> 20, k -> 12);
checkEq(Solution.totalFromAll(shards, "k"), 42, "sum of all");
""",
            "10 + 20 + 12.",
        ),
        (
            "failing shard contributes 0",
            r"""
List<Solution.Shard> shards = List.of(
    k -> 10, k -> { throw new RuntimeException("down"); }, k -> 12);
checkEq(Solution.totalFromAll(shards, "k"), 22, "fault isolated");
""",
            "The broken shard is skipped, others still count.",
        ),
        (
            "async version matches",
            r"""
List<Solution.Shard> shards = List.of(
    k -> 10, k -> { throw new RuntimeException("down"); }, k -> 12);
checkEq(Solution.asyncTotal(shards, "k").join(), 22, "async == sync");
""",
            "Same contract through CompletableFuture chains.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP10 = vi_challenge(
    "Bộ tổng hợp song song",
    r"""Xây `Solution`:
- `interface Shard { int fetch(String key); }` — một data shard.
- `static int totalFromAll(List<Shard> shards, String key)` — gọi mọi
  shard (tuần tự là đủ), coi shard ném RuntimeException đóng góp 0 (cô
  lập lỗi).
- `static CompletableFuture<Integer> asyncTotal(List<Shard> shards,
  String key)` — cùng ngữ nghĩa qua chuỗi completedFuture/thenApply với
  một exceptionally mỗi shard, join bằng allOf + tổng.

Lỗi của một shard không được đầu độc shard khác — đó là hợp đồng.""",
    [
        ("Shard khỏe cộng vào", "10 + 20 + 12."),
        ("Shard hỏng đóng góp 0", "Shard lỗi bị bỏ qua, shard khác vẫn được đếm."),
        ("Bản async trùng khớp", "Cùng hợp đồng qua chuỗi CompletableFuture."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-async",
    "Checkpoint: Async & HTTP",
    "Graded checkpoint: fault-isolated aggregation over shards, in both synchronous and CompletableFuture forms.",
    15,
    CP_MDX,
    "Checkpoint: Async & HTTP",
    "Checkpoint chấm điểm: tổng hợp cô lập lỗi qua các shard, ở cả dạng đồng bộ lẫn CompletableFuture.",
    CP_MDX_VI,
    CH_CP10,
    VI_CH_CP10,
    solution=r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public interface Shard { int fetch(String key); }

    public static int totalFromAll(List<Shard> shards, String key) {
        int total = 0;
        for (Shard s : shards) {
            try { total += s.fetch(key); } catch (RuntimeException ignored) { }
        }
        return total;
    }

    public static CompletableFuture<Integer> asyncTotal(List<Shard> shards, String key) {
        List<CompletableFuture<Integer>> futures = new ArrayList<>();
        for (Shard s : shards) {
            futures.add(CompletableFuture.completedFuture(s)
                .thenApply(sh -> sh.fetch(key))
                .exceptionally(ex -> 0));
        }
        return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
            .thenApply(v -> futures.stream().mapToInt(CompletableFuture::join).sum());
    }
}
""",
    wrong=r"""
import java.util.*;
import java.util.concurrent.*;

public class Solution {
    public interface Shard { int fetch(String key); }

    // W: one bad shard aborts the whole aggregation — no fault isolation,
    // so a single failure poisons every result.
    public static int totalFromAll(List<Shard> shards, String key) {
        int total = 0;
        for (Shard s : shards) total += s.fetch(key);
        return total;
    }

    public static CompletableFuture<Integer> asyncTotal(List<Shard> shards, String key) {
        List<CompletableFuture<Integer>> futures = new ArrayList<>();
        for (Shard s : shards) {
            futures.add(CompletableFuture.completedFuture(s)
                .thenApply(sh -> sh.fetch(key))
                .exceptionally(ex -> 0));
        }
        return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
            .thenApply(v -> futures.stream().mapToInt(CompletableFuture::join).sum());
    }
}
""",
)
