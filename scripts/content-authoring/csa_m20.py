"""Module 20 — Distributed systems (csa-m20)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-distributed",
        "Distributed Systems",
        "Failure, retries, idempotency, eventual consistency — the concepts and the simulations, deterministic in the sandbox.",
    )

    csa.register_lesson(
        MID, "csa-m20-boundaries", "Service boundaries and distributed state",
        "What makes a boundary, why network calls are different, and the fallacies that keep producing outages.",
        15, "advanced", _m20_boundaries, _m20_boundaries_vi,
    )
    csa.register_lesson(
        MID, "csa-m20-idempotency", "Idempotency and exactly-once",
        "Why exactly-once delivery is a lie, and the idempotency-key pattern that makes retries safe.",
        16, "advanced", _m20_idempotency, _m20_idempotency_vi,
    )
    csa.register_lesson(
        MID, "csa-m20-resilience", "Retries, timeouts, and failure budgets",
        "Composing the resilience stack: timeout inside retry inside breaker, with failure budgets and backoff.",
        15, "advanced", _m20_resilience, _m20_resilience_vi,
    )
    csa.register_lesson(
        MID, "csa-m20-consistency", "Consistency models and eventual state",
        "Strong vs eventual consistency, convergence, and the read-after-write trap.",
        15, "advanced", _m20_consistency, _m20_consistency_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m20", "Checkpoint: distributed systems",
        "Synthesis: build an idempotent message processor with simulated faults.",
        12, "advanced", _m20_checkpoint, _m20_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m20-task", MID,
        title="Distributed checkpoint",
        prompt=(
            "Simulated message bus, deterministic: implement class `IdempotentProcessor` with `int Process(string "
            "messageId, Func<int> work)` — processes work once per messageId, caches the result, returns it on "
            "repeats WITHOUT re-running work (work has a side-effect counter the test watches). Then implement "
            "`static int[] DeliverAll(List<string> messageIds, Func<string, int> handler, int duplicates)` that "
            "delivers every message `duplicates` times (out of order, shuffled deterministically by index) and "
            "returns the work-counter delta — which must be exactly messageIds.Count because duplicates are "
            "absorbed idempotently."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "process-once",
                "code": (
                    "var p = new IdempotentProcessor();\n"
                    "int runs = 0;\n"
                    "int r1 = p.Process(\"m1\", () => ++runs);\n"
                    "int r2 = p.Process(\"m1\", () => ++runs);   // duplicate delivery\n"
                    'Cj.Eq(r1, 1, "first run");\n'
                    'Cj.Eq(r2, 1, "repeat returns cached result");\n'
                    'Cj.Eq(runs, 1, "work executed exactly once");'
                ),
                "hint": "Dictionary<string,int> cache: TryGetValue → return; else compute, store, return.",
            },
            {
                "name": "duplicates-absorbed",
                "code": (
                    "var ids = Enumerable.Range(0, 20).Select(i => $\"msg-{i}\").ToList();\n"
                    "int runs = 0;\n"
                    "var delta = IdempotentProcessor.DeliverAll(ids, id => IdempotentProcessor.RunTracked(id, () => ++runs), 3);\n"
                    'Cj.Eq(delta, 20, "20 unique messages = 20 runs despite 60 deliveries");'
                ),
                "hint": "DeliverAll: one shared IdempotentProcessor; deliver each id `duplicates` times; count runs before/after.",
            },
        ],
        reference=(
            "public class IdempotentProcessor\n{\n"
            "    private readonly Dictionary<string, int> _results = new();\n"
            "    private static readonly Dictionary<string, int> _tracked = new();\n"
            "    private static int _runs;\n\n"
            "    public int Process(string messageId, Func<int> work)\n"
            "    {\n"
            "        if (_results.TryGetValue(messageId, out var cached)) return cached;\n"
            "        var r = work();\n"
            "        _results[messageId] = r;\n"
            "        return r;\n"
            "    }\n\n"
            "    public static int RunTracked(string key, Func<int> work)\n"
            "    {\n"
            "        if (_tracked.TryGetValue(key, out var c)) return c;\n"
            "        var r = work();\n"
            "        _tracked[key] = r;\n"
            "        return r;\n"
            "    }\n\n"
            "    public static int[] DeliverAll(List<string> messageIds, Func<string, int> handler, int duplicates)\n"
            "    {\n"
            "        var before = _runs;\n"
            "        var seq = new List<string>();\n"
            "        for (int d = 0; d < duplicates; d++)\n"
            "            foreach (var id in messageIds) seq.Add(id);\n"
            "        // deterministic interleave: round-robin, not shuffled\n"
            "        foreach (var id in seq) handler(id);\n"
            "        return new[] { _runs - before };\n"
            "    }\n}"
        ),
        wrong=(
            "public class IdempotentProcessor\n{\n"
            "    private readonly Dictionary<string, int> _results = new();\n"
            "    private static readonly Dictionary<string, int> _tracked = new();\n"
            "    private static int _runs;\n\n"
            "    public int Process(string messageId, Func<int> work)\n"
            "    {\n"
            "        var r = work();   // WRONG: no cache — duplicates re-run side effects\n"
            "        _results[messageId] = r;\n"
            "        return r;\n"
            "    }\n\n"
            "    public static int RunTracked(string key, Func<int> work)\n"
            "    {\n"
            "        if (_tracked.TryGetValue(key, out var c)) return c;\n"
            "        var r = work();\n"
            "        _tracked[key] = r;\n"
            "        return r;\n"
            "    }\n\n"
            "    public static int[] DeliverAll(List<string> messageIds, Func<string, int> handler, int duplicates)\n"
            "    {\n"
            "        var before = _runs;\n"
            "        var seq = new List<string>();\n"
            "        for (int d = 0; d < duplicates; d++)\n"
            "            foreach (var id in messageIds) seq.Add(id);\n"
            "        foreach (var id in seq) handler(id);\n"
            "        return new[] { _runs - before };\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p20-dist", "Distributed drills",
        "Retry storms, backpressure contracts, and consistency reasoning under simulated faults.",
        45, "advanced", "csa-m20-resilience",
        ["csa-p20-retry-budget", "csa-p20-eventual-read"],
    )
    csa.register_challenge(
        "csa-p20-retry-budget", MID,
        title="Failure budget",
        prompt=(
            "Retries amplify load exactly when the system can least afford it. Implement `static int "
            "AmplifiedLoad(int clients, int baseAttempts, int retryMultiplier)` returning total requests: "
            "clients × baseAttempts × (1 + retryMultiplier). Then implement `static bool WithinBudget(int total, "
            "int budget)` and a `static string Verdict(int clients, int baseAttempts, int retryMultiplier, int "
            "budget)` returning \"ok\" if within, \"overload\" otherwise. The graded insight: 1000 clients × 1 "
            "call × 5 retries = 6000 requests — the retry storm is arithmetic, not bad luck."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "amplification",
                "code": (
                    'Cj.Eq(Solution.AmplifiedLoad(1000, 1, 5), 6000, "1000 clients, 5 retries = 6000 requests");\n'
                    'Cj.Eq(Solution.Verdict(1000, 1, 5, 5000), "overload", "exceeds budget");\n'
                    'Cj.Eq(Solution.Verdict(1000, 1, 5, 6000), "ok", "exactly at budget");'
                ),
                "hint": "AmplifiedLoad = clients * baseAttempts * (1 + retryMultiplier); Verdict compares against budget.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static int AmplifiedLoad(int clients, int baseAttempts, int retryMultiplier)\n"
            "        => clients * baseAttempts * (1 + retryMultiplier);\n\n"
            "    public static bool WithinBudget(int total, int budget) => total <= budget;\n\n"
            "    public static string Verdict(int clients, int baseAttempts, int retryMultiplier, int budget)\n"
            "        => WithinBudget(AmplifiedLoad(clients, baseAttempts, retryMultiplier), budget) ? \"ok\" : \"overload\";\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int AmplifiedLoad(int clients, int baseAttempts, int retryMultiplier)\n"
            "        => clients * baseAttempts + retryMultiplier;   // WRONG: retries multiply, not add\n\n"
            "    public static bool WithinBudget(int total, int budget) => total <= budget;\n\n"
            "    public static string Verdict(int clients, int baseAttempts, int retryMultiplier, int budget)\n"
            "        => WithinBudget(AmplifiedLoad(clients, baseAttempts, retryMultiplier), budget) ? \"ok\" : \"overload\";\n}"
        ),
        level="independent",
    )
    csa.register_challenge(
        "csa-p20-eventual-read", MID,
        title="Read-after-write under eventual consistency",
        prompt=(
            "Implement class `EventualStore(int replicationDelayMs)` with `void Write(string key, int value)` "
            "(primary immediately; replica after the delay via Task.Run) and `int? ReadStale(string key)` (reads "
            "the replica, may miss recent writes) plus `int? ReadPrimary(string key)` (always current). Implement "
            "`static async Task<bool> ReadAfterWriteHolds(EventualStore store, string key)` that writes 42, reads "
            "the replica IMMEDIATELY — and returns whether the read saw the write (it must NOT, with a real "
            "delay; the test then waits past the delay and requires the replica to converge)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "stale-then-converged",
                "code": (
                    "var store = new EventualStore(60);\n"
                    "var holdsImmediately = await EventualStore.ReadAfterWriteHolds(store, \"k\");\n"
                    'Cj.False(holdsImmediately, "immediate replica read misses the write (eventual consistency)");\n'
                    "await Task.Delay(120);\n"
                    'Cj.Eq(store.ReadStale("k"), 42, "replica converged after the delay");\n'
                    'Cj.Eq(store.ReadPrimary("k"), 42, "primary always current");'
                ),
                "hint": "Write: dict[key]=v on primary; Task.Run(async { await Task.Delay(replicationDelayMs); replica[key]=v; }). ReadAfterWriteHolds: Write, then ReadStale != null.",
            },
        ],
        reference=(
            "public class EventualStore\n{\n"
            "    private readonly int _delayMs;\n"
            "    private readonly Dictionary<string, int> _primary = new();\n"
            "    private readonly Dictionary<string, int> _replica = new();\n\n"
            "    public EventualStore(int replicationDelayMs) { _delayMs = replicationDelayMs; }\n\n"
            "    public void Write(string key, int value)\n"
            "    {\n"
            "        _primary[key] = value;\n"
            "        var k = key;\n"
            "        var v = value;\n"
            "        Task.Run(async () =>\n"
            "        {\n"
            "            await Task.Delay(_delayMs);\n"
            "            _replica[k] = v;\n"
            "        });\n"
            "    }\n\n"
            "    public int? ReadStale(string key) => _replica.TryGetValue(key, out var v) ? v : null;\n"
            "    public int? ReadPrimary(string key) => _primary.TryGetValue(key, out var v) ? v : null;\n\n"
            "    public static async Task<bool> ReadAfterWriteHolds(EventualStore store, string key)\n"
            "    {\n"
            "        store.Write(key, 42);\n"
            "        return store.ReadStale(key) == 42;\n"
            "    }\n}"
        ),
        wrong=(
            "public class EventualStore\n{\n"
            "    private readonly int _delayMs;\n"
            "    private readonly Dictionary<string, int> _primary = new();\n"
            "    private readonly Dictionary<string, int> _replica = new();\n\n"
            "    public EventualStore(int replicationDelayMs) { _delayMs = replicationDelayMs; }\n\n"
            "    public void Write(string key, int value)\n"
            "    {\n"
            "        _primary[key] = value;\n"
            "        _replica[key] = value;   // WRONG: synchronous replication — hides the consistency gap\n"
            "    }\n\n"
            "    public int? ReadStale(string key) => _replica.TryGetValue(key, out var v) ? v : null;\n"
            "    public int? ReadPrimary(string key) => _primary.TryGetValue(key, out var v) ? v : null;\n\n"
            "    public static async Task<bool> ReadAfterWriteHolds(EventualStore store, string key)\n"
            "    {\n"
            "        store.Write(key, 42);\n"
            "        return store.ReadStale(key) == 42;\n"
            "    }\n}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m20_boundaries = r"""## Service boundaries and distributed state

A service boundary is where your process ends and someone else's begins —
different deployment, different failure domain, different upgrade
schedule. Once a call crosses one, every assumption changes:

| In-process call | Cross-network call |
|---|---|
| failure = exception | failure = exception OR timeout OR partial result OR silence |
| latency = ns | latency = ms, variable, occasionally seconds |
| memory is coherent | the remote state moved on without you |
| transactions work | distributed transactions are a research paper |

The **eight fallacies of distributed computing** remain the best debugging
checklist: the network is reliable; latency is zero; bandwidth is
infinite; the network is secure; topology doesn't change; there is one
administrator; transport cost is zero; the network is homogeneous. Every
production outage story includes at least one fallacy being violated.

The boundary design rules that follow:

1. **A boundary needs a contract** — versioned, explicit, with failure
   semantics documented ("this endpoint may return 503; treat 503 as
   retry-safe").
2. **Remote state is only a hypothesis.** Your cache, your read model, the
   response you got 200ms ago — all may be stale. Design reads that can
   tolerate staleness or declare that they cannot.
3. **No synchronous chains.** A→B→C→D synchronous calls compound latencies
   and failure rates multiplicatively (0.99⁴ ≈ 0.96). Async messaging or
   pre-computation beats deep chains.
4. **The boundary owns its failures.** Callers get domain errors, not
   stack traces from your database.

This module simulates boundaries deterministically in-process — but the
failures simulated (duplicate delivery, stale reads, retry amplification)
are the real ones, miniaturized until they are testable in milliseconds.
"""

_m20_boundaries_vi = r"""## Ranh giới service và trạng thái phân tán

Ranh giới service là nơi process của bạn kết thúc và của người khác bắt
đầu — triển khai khác, miền lỗi khác, lịch nâng cấp khác. Một khi lời gọi
vượt qua nó, mọi giả định đổi thay:

| Lời gọi trong process | Lời gọi qua mạng |
|---|---|
| lỗi = exception | lỗi = exception HOẶC timeout HOẶC kết quả một phần HOẶC im lặng |
| độ trễ = ns | độ trễ = ms, biến động, thi thoảng cả giây |
| bộ nhớ nhất quán | trạng thái xa đã đi tiếp mà không có bạn |
| transaction hoạt động | transaction phân tán là một bài báo nghiên cứu |

**Tám ảo tưởng của điện toán phân tán** vẫn là checklist debug tốt nhất:
mạng tin cậy; độ trễ bằng không; băng thông vô hạn; mạng an toàn; topo
không đổi; chỉ có một quản trị viên; chi phí vận chuyển bằng không; mạng
đồng nhất. Mọi câu chuyện sự cố production đều có ít nhất một ảo tưởng bị
vi phạm.

Các luật thiết kế ranh giới hệ quả của nó:

1. **Ranh giới cần hợp đồng** — có phiên bản, tường minh, ghi rõ ngữ nghĩa
   lỗi ("endpoint này có thể trả 503; coi 503 là an-toàn-để-retry").
2. **Trạng thái xa chỉ là giả thuyết.** Cache của bạn, read model của bạn,
   response nhận được cách đây 200ms — tất cả có thể đã cũ. Thiết kế phép
   đọc chịu được độ cũ, hoặc tuyên bố không chịu được.
3. **Không chuỗi đồng bộ.** Lời gọi đồng bộ A→B→C→D nhân chồng độ trễ và
   tỷ lệ lỗi theo cấp số nhân (0.99⁴ ≈ 0.96). Messaging bất đồng bộ hoặc
   tiền tính toán đánh bại chuỗi sâu.
4. **Ranh giới sở hữu lỗi của nó.** Caller nhận lỗi domain, không phải
   stack trace từ database của bạn.

Module này mô phỏng ranh giới một cách tất định trong process — nhưng các
lỗi được mô phỏng (giao trùng lặp, đọc cũ, khuếch đại retry) là những lỗi
thật, thu nhỏ đến mức test được bằng mili giây.
"""

_m20_idempotency = r"""## Idempotency and exactly-once

The messaging truth table everyone eventually learns: networks offer
**at-most-once** (drop on failure) and **at-least-once** (retry until
acknowledged — which duplicates). **Exactly-once** delivery across a
network is not achievable as a transport property; it is achievable as an
*effect* — exactly-once processing — and idempotency is how.

```csharp
// The pattern the checkpoint implements:
public int Process(string messageId, Func<int> work)
{
    if (_results.TryGetValue(messageId, out var cached)) return cached;   // duplicate absorbed
    var result = work();
    _results[messageId] = result;    // remember — before acknowledging!
    return result;
}
```

The production-grade version stores the key and result **atomically with
the side effect** (same DB transaction, or a dedupe table the write
checks). The broken version caches in memory and side-effects in the
database: crash between them = duplicate side effect on redelivery.

Where idempotency keys come from: the producer stamps every message with a
unique ID at creation; consumers dedupe. Payment APIs (Stripe et al.) made
this famous — client-generated idempotency keys make double-click
double-charges impossible.

The vocabulary that keeps design conversations honest:

- **At-least-once + idempotent consumer = effectively exactly-once.** The
  standard architecture.
- **Duplicate suppression window**: dedupe state is finite; keys expire.
  "At least once within a 24h window" is the real contract — document it.
- **Ordered delivery**: at-least-once + retries also reorder. If order
  matters, include sequence numbers and buffer/hold at the consumer.

The checkpoint's `DeliverAll` proves the math: 20 messages delivered 3
times each = 60 deliveries, 20 side effects. The practice drill shows what
happens when a team forgets: the retry storm is not bad luck, it is
arithmetic.
"""

_m20_idempotency_vi = r"""## Idempotency và exactly-once

Bảng sự thật messaging mà mọi người sớm muộn cũng học: mạng cung cấp
**at-most-once** (mất khi lỗi) và **at-least-once** (retry đến khi được xác
nhận — mà điều đó tạo ra bản sao). **Exactly-once** trên mạng không phải là
tính chất vận chuyển khả thi; nó khả thi như một *hiệu ứng* — xử lý
exactly-once — và idempotency là cách.

```csharp
// Pattern mà checkpoint cài:
public int Process(string messageId, Func<int> work)
{
    if (_results.TryGetValue(messageId, out var cached)) return cached;   // bản sao bị hấp thụ
    var result = work();
    _results[messageId] = result;    // ghi nhớ — TRƯỚC khi xác nhận!
    return result;
}
```

Bản production lưu key và kết quả **nguyên tử với tác dụng phụ** (cùng
transaction DB, hoặc bảng dedupe mà phép ghi kiểm tra). Bản gãy: cache
trong bộ nhớ còn tác dụng phụ trong database — sập giữa hai cái = tác dụng
phụ trùng lặp khi giao lại.

Idempotency key đến từ đâu: producer đóng dấu mọi tin nhắn một ID duy nhất
tại lúc tạo; consumer dedupe. Các API thanh toán (Stripe v.v.) làm pattern
này nổi tiếng — key do client sinh khiến double-click không thể sinh
double-charge.

Từ vựng giữ các cuộc thảo luận thiết kế trung thực:

- **At-least-once + consumer idempotent = effectively exactly-once.** Kiến
  trúc chuẩn.
- **Cửa sổ khử trùng lặp**: trạng thái dedupe là hữu hạn; key hết hạn.
  "At least once trong cửa sổ 24h" mới là hợp đồng thật — hãy ghi tài liệu.
- **Thứ tự giao**: at-least-once + retry còn làm mất thứ tự. Nếu thứ tự
  quan trọng, gắn số trình tự và buffer/giữ ở consumer.

`DeliverAll` trong checkpoint chứng minh phép tính: 20 tin nhắn giao 3 lần
mỗi cái = 60 lần giao, 20 tác dụng phụ. Drill practice cho thấy điều gì xảy
ra khi một đội quên: cơn bão retry không phải vận xui, nó là phép tính.
"""

_m20_resilience = r"""## Retries, timeouts, and failure budgets

The resilience stack composes — and each layer changes the others'
behavior. Getting the composition right is the skill:

```
call ──> [retry: 3 attempts, backoff 100/200/400ms]
              └──> each attempt ──> [timeout: 2s, via cancellation]
                                         └──> the real dependency
[breaker: opens after 5 consecutive failures, half-open after 30s]
```

The interaction rules:

1. **Timeout ⊂ Retry.** Each retry attempt carries its own deadline; a
   retry without a timeout can outlive the total request budget.
2. **Retry ⊂ Breaker.** The breaker counts a failed *attempt sequence* as
   one failure. Without the breaker, 1000 clients × 3 retries = 3000
   requests against a dying dependency — the amplification the practice
   drill computes.
3. **Budget = total latency.** If the caller's SLA is 3s and each attempt
   can take 2s, three retries cannot fit — cap attempts by remaining
   budget, not by policy count.
4. **Idempotency or bust.** Retrying a non-idempotent operation (charge,
   insert) duplicates effects. Idempotency keys (previous lesson) make the
   retry safe.

Backoff details that matter under load: exponential (each wait doubles)
plus **jitter** (random ±50%) so thousands of clients don't synchronize
their retries into waves — the thundering herd that turns one dependency's
hiccup into a platform-wide outage. The failure budget framing: define how
much failure your SLO absorbs (say, 0.1% of requests may fail), spend it
deliberately (fail fast when the budget is spent rather than queueing
requests nobody will wait for) — resilience is a budget, not a virtue.
"""

_m20_resilience_vi = r"""## Retry, timeout, và ngân sách thất bại

Stack chịu lỗi kết hợp được — và mỗi tầng thay đổi hành vi của các tầng
khác. Đưacomposition đúng là kỹ năng:

```
call ──> [retry: 3 lần, backoff 100/200/400ms]
              └──> mỗi lần ──> [timeout: 2s, qua cancellation]
                                         └──> phụ thuộc thật
[breaker: mở sau 5 thất bại liên tiếp, half-open sau 30s]
```

Các luật tương tác:

1. **Timeout ⊂ Retry.** Mỗi lần retry mang deadline riêng; một retry không
   có timeout có thể sống lâu hơn tổng ngân sách request.
2. **Retry ⊂ Breaker.** Breaker đếm một *chuỗi lần thử* thất bại là một lỗi.
   Không có breaker, 1000 client × 3 retry = 3000 request đánh vào một phụ
   thuộc đang chết — sự khuếch đại mà drill practice tính ra.
3. **Ngân sách = tổng độ trễ.** Nếu SLA của caller là 3s và mỗi lần thử có
   thể mất 2s, ba lần retry không thể vừa — chặn số lần theo ngân sách còn
   lại, không phải theo số chính sách.
4. **Idempotency hoặc là chết.** Retry một thao tác không idempotent
   (charge, insert) nhân đôi hiệu ứng. Idempotency key (bài trước) làm cho
   retry an toàn.

Chi tiết backoff quan trọng dưới tải: luỹ thừa (mỗi lần chờ gấp đôi) cộng
**jitter** (random ±50%) để hàng nghìn client không đồng bộ retry thành
các đợt sóng — thundering herd biến một cú hích của một phụ thuộc thành sự
cố toàn nền tảng. Khung ngân sách thất bại: định nghĩa hệ thống chịu được
bao nhiêu thất bại trong SLO (ví dụ 0.1% request có thể lỗi), tiêu nó một
cách chủ ý (fail fast khi ngân sách cạn thay vì xếp hàng những request không
ai chờ) — resilience là một ngân sách, không phải một đức tính.
"""

_m20_consistency = r"""## Consistency models and eventual state

Once state replicates, reads become interesting. The models, in the
vocabulary system designers actually use:

- **Strong / linearizable**: every read sees every completed write, as if
  one copy existed. Costs: coordination on every read/write, availability
  drops under partitions.
- **Read-your-writes (session)**: a client sees its own writes; others may
  lag. The pragmatic web default ("I edited my profile and I see my edit").
- **Eventual**: replicas converge given time and no new writes. Reads may
  be stale; the STALENESS is the contract to reason about.
- **Causal**: reads see all writes they causally depend on — comment sees
  the post it replies to.

The **read-after-write trap** (the practice drill, miniaturized): write to
the primary, immediately read from a replica, and the read misses the
write. Real systems hit this when load-balancers route a read to a replica
after a POST. Fixes, in cost order: session pinning (route that user's
reads to the primary for N seconds after a write), version checks (client
sends the version it wrote; replica blocks/tells-stale), or accept and
design for it (show "just saved" states optimistically).

Convergence is the other half: eventual systems need a well-defined
convergence rule (last-write-wins by timestamp — with clock-skew hazards —
or CRDTs for merge-able state). The checkpoint's `EventualStore` makes the
delay explicit and observable: primary immediately, replica after a delay
you control. The lesson is not the toy; it is the design habit — every
distributed read/write decision should be able to name its consistency
model and its staleness bound. If nobody can, that is the finding.
"""

_m20_consistency_vi = r"""## Mô hình nhất quán và trạng thái hiện tại dần

Khi trạng thái nhân bản, phép đọc trở nên thú vị. Các mô hình, theo từ
vựng mà người thiết kế hệ thống thực sự dùng:

- **Strong / linearizable**: mọi phép đọc thấy mọi phép ghi đã hoàn thành,
  như thể chỉ có một bản sao. Chi phí: phối hợp cho mọi đọc/ghi, availability
  giảm dưới phân vùng.
- **Read-your-writes (session)**: một client thấy chính phép ghi của mình;
  người khác có thể trễ. Mặc định web thực dụng ("tôi sửa profile và thấy
  sự sửa của mình").
- **Eventual**: các bản sao hội tụ nếu có thời gian và không có ghi mới.
  Phép đọc có thể cũ; ĐỘ CŨ chính là hợp đồng cần suy luận.
- **Causal**: phép đọc thấy mọi phép ghi mà nó nhân quả phụ thuộc — bình
  luận thấy bài viết mà nó trả lời.

**Cái bẫy read-after-write** (drill practice, bản thu nhỏ): ghi vào
primary, đọc ngay từ replica, phép đọc không thấy phép ghi. Hệ thống thật
dính lỗi này khi load-balancer điều route một phép đọc tới replica sau một
POST. Cách sửa, theo thứ tự chi phí: ghim session (route phép đọc của user
đó về primary trong N giây sau ghi), kiểm tra phiên bản (client gửi phiên
bản nó ghi; replica chặn/báo-cũ), hoặc chấp nhận và thiết kế cho nó (hiển
thị trạng thái "vừa lưu" một cách lạc quan).

Hội tụ là nửa còn lại: hệ eventual cần quy tắc hội tụ được định nghĩa rõ
(last-write-wins theo timestamp — với các mối nguy lệch đồng hồ — hoặc
CRDT cho trạng thái gộp được). `EventualStore` trong checkpoint làm độ trễ
trở nên tường minh và quan sát được: primary ngay lập tức, replica sau một
độ trễ bạn kiểm soát. Bài học không phải món đồ chơi; đó là thói quen thiết
kế — mọi quyết định đọc/ghi phân tán phải gọi được tên mô hình nhất quán
và biên độ cũ của nó. Nếu không ai gọi được, đó chính là phát hiện.
"""

_m20_checkpoint = r"""## Checkpoint: distributed systems

The graded task builds the idempotent consumer — the pattern that makes
at-least-once delivery behave like exactly-once processing — and proves
duplicate absorption arithmetically. Practice adds retry-amplification
math and the read-after-write gap made observable.
"""

_m20_checkpoint_vi = r"""## Checkpoint: hệ phân tán

Bài được chấm xây consumer idempotent — pattern biến giao at-least-once
thành xử lý effectively-exactly-once — và chứng minh sự hấp thụ trùng lặp
bằng phép tính. Practice bổ sung phép tính khuếch đại retry và khoảng hở
read-after-write trở nên quan sát được."""
