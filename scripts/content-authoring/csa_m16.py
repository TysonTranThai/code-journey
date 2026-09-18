"""Module 16 — Advanced debugging and diagnostics (csa-m16)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-diagnostics",
        "Advanced Debugging and Diagnostics",
        "Reading failures: stack traces, exception analysis, health probes, and resilience patterns — with the tools the sandbox has.",
    )

    csa.register_lesson(
        MID, "csa-m16-stack-traces", "Stack traces as evidence",
        "Reading async MoveNext frames, rethrow semantics, inner exceptions, and trace truncation.",
        15, "advanced", _m16_traces, _m16_traces_vi,
    )
    csa.register_lesson(
        MID, "csa-m16-failure-forensics", "Failure forensics without a debugger",
        "Structured logging, correlation, deterministic reproduction, and the hypothesis discipline.",
        15, "advanced", _m16_forensics, _m16_forensics_vi,
    )
    csa.register_lesson(
        MID, "csa-m16-health-resilience", "Health probes and resilience primitives",
        "Liveness vs readiness, circuit breakers, retries with backoff — the runtime signals that keep systems debuggable.",
        15, "advanced", _m16_health, _m16_health_vi,
    )
    csa.register_lesson(
        MID, "csa-m16-checkpoint-lesson", "Checkpoint lesson: diagnose the broken service",
        "A worked diagnosis: from symptom to root cause through evidence, not guessing.",
        14, "advanced", _m16_diag, _m16_diag_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m16-task", MID,
        title="Diagnostics checkpoint",
        prompt=(
            "Implement `static string Describe(Exception ex)` producing a one-line diagnostic: "
            "\"<TypeName>: <Message> | caused by: <TypeName>: <Message> | ...\" walking the InnerException chain "
            "to the root, joined with \" | caused by: \". Then implement `static (int depth, string rootType) "
            "Analyze(Exception ex)` returning the inner-exception depth (0 for no inner) and the root exception's "
            "type name. The graded skill: never lose the root cause buried in AggregateException/InnerException chains."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "describe-chain",
                "code": (
                    "var root = new InvalidOperationException(\"root cause\");\n"
                    "var mid = new ApplicationException(\"layer\", root);\n"
                    "var top = new Exception(\"api boundary\", mid);\n"
                    "var s = Solution.Describe(top);\n"
                    'Cj.True(s.StartsWith("Exception: api boundary"), "top first");\n'
                    'Cj.True(s.Contains("ApplicationException: layer"), "middle present");\n'
                    'Cj.True(s.EndsWith("InvalidOperationException: root cause"), "root last");'
                ),
                "hint": "Walk ex → ex.InnerException → null, joining each \"type: message\" with \" | caused by: \".",
            },
            {
                "name": "analyze-depth",
                "code": (
                    "var root = new InvalidOperationException(\"r\");\n"
                    "var nested = new Exception(\"a\", new Exception(\"b\", root));\n"
                    "var (d, rootType) = Solution.Analyze(nested);\n"
                    'Cj.Eq(d, 3, "three levels deep");\n'
                    'Cj.Eq(rootType, "InvalidOperationException", "root type found");'
                ),
                "hint": "Count hops to InnerException == null; record the last exception's GetType().Name.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static string Describe(Exception ex)\n"
            "    {\n"
            "        var parts = new List<string>();\n"
            "        for (var e = ex; e is not null; e = e.InnerException)\n"
            "            parts.Add($\"{e.GetType().Name}: {e.Message}\");\n"
            "        return string.Join(\" | caused by: \", parts);\n"
            "    }\n\n"
            "    public static (int depth, string rootType) Analyze(Exception ex)\n"
            "    {\n"
            "        int depth = 0;\n"
            "        var cur = ex;\n"
            "        while (cur.InnerException is not null)\n"
            "        {\n"
            "            cur = cur.InnerException;\n"
            "            depth++;\n"
            "        }\n"
            "        return (depth, cur.GetType().Name);\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static string Describe(Exception ex)\n"
            "        => $\"{ex.GetType().Name}: {ex.Message}\";   // WRONG: only the top — root cause lost\n\n"
            "    public static (int depth, string rootType) Analyze(Exception ex)\n"
            "        => (0, ex.GetType().Name);   // WRONG: never walks the chain\n"
            "}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p16-diag", "Diagnostics drills",
        "Trace reading, circuit-breaker state machines, retry backoff math, and health-probe semantics.",
        45, "advanced", "csa-m16-health-resilience",
        ["csa-p16-circuit-breaker", "csa-p16-retry-backoff"],
    )
    csa.register_challenge(
        "csa-p16-circuit-breaker", MID,
        title="Circuit breaker state machine",
        prompt=(
            "Implement class `CircuitBreaker(int failureThreshold, TimeSpan openDuration)` with method `bool "
            "TryExecute(Action action)`: CLOSED executes and counts consecutive failures (resetting on success); "
            "at threshold it opens for openDuration (TryExecute returns false immediately while open); after the "
            "duration it becomes HALF-OPEN, letting one attempt through — success closes, failure re-opens. "
            "Implement `string State` returning \"closed\", \"open\", or \"half-open\"."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "opens-and-resets",
                "code": (
                    "var cb = new CircuitBreaker(2, TimeSpan.FromMilliseconds(80));\n"
                    "var ok = true;\n"
                    'Cj.True(cb.TryExecute(() => { if (!ok) throw new InvalidOperationException(); }), "first succeeds");\n'
                    "ok = false;\n"
                    'Cj.False(cb.TryExecute(() => { throw new InvalidOperationException(); }), "failure 1");\n'
                    'Cj.False(cb.TryExecute(() => { throw new InvalidOperationException(); }), "failure 2 → opens");\n'
                    'Cj.Eq(cb.State, "open", "now open");\n'
                    'Cj.False(cb.TryExecute(() => { }), "open rejects immediately");\n'
                    "await Task.Delay(120);\n"
                    "ok = true;\n"
                    'Cj.True(cb.TryExecute(() => { }), "half-open probe succeeds → closed");\n'
                    'Cj.Eq(cb.State, "closed", "recovered");'
                ),
                "hint": "Track _state, _consecutiveFailures, _openedAt. On TryExecute: if open and now < openedAt+duration → false; if open and expired → state=half-open, allow one try.",
            },
            {
                "name": "half-open-fails-reopens",
                "code": (
                    "var cb = new CircuitBreaker(1, TimeSpan.FromMilliseconds(60));\n"
                    "var ok = false;\n"
                    'cb.TryExecute(() => { if (!ok) throw new InvalidOperationException(); });\n'
                    'Cj.Eq(cb.State, "open");\n'
                    "await Task.Delay(100);\n"
                    "ok = false;\n"
                    'Cj.False(cb.TryExecute(() => { if (!ok) throw new InvalidOperationException(); }), "half-open probe fails");\n'
                    'Cj.Eq(cb.State, "open", "re-opened after failed probe");'
                ),
                "hint": "Failed half-open probe: reset _openedAt, state=open.",
            },
        ],
        reference=(
            "public class CircuitBreaker\n{\n"
            "    private readonly int _threshold;\n"
            "    private readonly TimeSpan _openDuration;\n"
            "    private int _consecutiveFailures;\n"
            "    private DateTimeOffset _openedAt;\n"
            "    private string _state = \"closed\";\n\n"
            "    public CircuitBreaker(int failureThreshold, TimeSpan openDuration)\n"
            "    {\n"
            "        _threshold = failureThreshold;\n"
            "        _openDuration = openDuration;\n"
            "    }\n\n"
            "    public string State => _state;\n\n"
            "    public bool TryExecute(Action action)\n"
            "    {\n"
            "        if (_state == \"open\")\n"
            "        {\n"
            "            if (DateTimeOffset.UtcNow - _openedAt < _openDuration) return false;\n"
            "            _state = \"half-open\";   // one probe allowed\n"
            "        }\n"
            "        try\n"
            "        {\n"
            "            action();\n"
            "            _consecutiveFailures = 0;\n"
            "            _state = \"closed\";\n"
            "            return true;\n"
            "        }\n"
            "        catch\n"
            "        {\n"
            "            _consecutiveFailures++;\n"
            "            if (_state == \"half-open\" || _consecutiveFailures >= _threshold)\n"
            "            {\n"
            "                _state = \"open\";\n"
            "                _openedAt = DateTimeOffset.UtcNow;\n"
            "                _consecutiveFailures = 0;\n"
            "            }\n"
            "            return false;\n"
            "        }\n"
            "    }\n}"
        ),
        wrong=(
            "public class CircuitBreaker\n{\n"
            "    private readonly int _threshold;\n"
            "    private readonly TimeSpan _openDuration;\n"
            "    private int _consecutiveFailures;\n"
            "    private string _state = \"closed\";\n\n"
            "    public CircuitBreaker(int failureThreshold, TimeSpan openDuration)\n"
            "    {\n"
            "        _threshold = failureThreshold;\n"
            "        _openDuration = openDuration;\n"
            "    }\n\n"
            "    public string State => _state;\n\n"
            "    public bool TryExecute(Action action)\n"
            "    {\n"
            "        if (_state == \"open\") return false;   // WRONG: never expires — breaker sticks open forever\n"
            "        try { action(); _consecutiveFailures = 0; _state = \"closed\"; return true; }\n"
            "        catch\n"
            "        {\n"
            "            _consecutiveFailures++;\n"
            "            if (_consecutiveFailures >= _threshold) { _state = \"open\"; }\n"
            "            return false;\n"
            "        }\n"
            "    }\n}"
        ),
        level="real-world",
    )
    csa.register_challenge(
        "csa-p16-retry-backoff", MID,
        title="Retry with exponential backoff",
        prompt=(
            "Implement `static async Task<int> RetryAsync(Func<int> attempt, int maxAttempts, int baseDelayMs)` "
            "calling attempt() up to maxAttempts times: on success return the value; on failure await "
            "Task.Delay(baseDelayMs * 2^attemptIndex) before the next try (attemptIndex starting at 0). After "
            "exhausting attempts throw InvalidOperationException. The test counts attempts with a counter and "
            "verifies backoff delays grow: run with maxAttempts=3 and a failing function — total elapsed must "
            "be at least baseDelayMs + 2*baseDelayMs."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "succeeds-eventually",
                "code": (
                    "int calls = 0;\n"
                    "var r = await Solution.RetryAsync(() => { calls++; if (calls < 3) throw new InvalidOperationException(); return 42; }, 5, 1);\n"
                    'Cj.Eq(r, 42, "third attempt wins");\n'
                    'Cj.Eq(calls, 3, "three attempts made");'
                ),
                "hint": "for (int i = 0; i < maxAttempts; i++) { try { return attempt(); } catch when (i < maxAttempts - 1) { await Task.Delay(baseDelayMs << i); } } — then throw.",
            },
            {
                "name": "backoff-timing",
                "code": (
                    "var sw = Stopwatch.StartNew();\n"
                    "var ex = await Cj.ThrowsAsync<InvalidOperationException>(() => Solution.RetryAsync(() => throw new InvalidOperationException(), 3, 30));\n"
                    "sw.Stop();\n"
                    'Cj.True(sw.ElapsedMilliseconds >= 90, $"3 attempts + delays 30+60 = 90ms minimum, got {sw.ElapsedMilliseconds}");'
                ),
                "hint": "Delay before retries 2 and 3: 30 * 2^0 = 30, then 30 * 2^1 = 60. Total wait 90ms.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static async Task<int> RetryAsync(Func<int> attempt, int maxAttempts, int baseDelayMs)\n"
            "    {\n"
            "        for (int i = 0; i < maxAttempts; i++)\n"
            "        {\n"
            "            try\n"
            "            {\n"
            "                return attempt();\n"
            "            }\n"
            "            catch when (i < maxAttempts - 1)\n"
            "            {\n"
            "                await Task.Delay(baseDelayMs << i);\n"
            "            }\n"
            "        }\n"
            "        throw new InvalidOperationException($\"all {maxAttempts} attempts failed\");\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static async Task<int> RetryAsync(Func<int> attempt, int maxAttempts, int baseDelayMs)\n"
            "    {\n"
            "        for (int i = 0; i < maxAttempts; i++)\n"
            "        {\n"
            "            try { return attempt(); }\n"
            "            catch { await Task.Delay(baseDelayMs); }   // WRONG: flat delay, retries after last attempt too\n"
            "        }\n"
            "        return -1;   // WRONG: sentinel instead of throwing\n"
            "    }\n}"
        ),
        level="real-world",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m16_traces = r"""## Stack traces as evidence

A stack trace is a recording of the call path at failure time. Reading it
like evidence (not like noise) is a diagnostic superpower:

```
System.InvalidOperationException: queue is empty
   at Solution.PumpAsync(ChannelReader`1 source, ...)
   at Program.<Main>$(String[] args)
   at System.Runtime.CompilerServices.AsyncTaskMethodBuilder.Start[TStateMachine](...)
```

- **Top frame = throw site.** Read DOWN for the path that led there.
  `MoveNext` frames mean an async state machine — the original method name
  is in the `<>c__DisplayClass`/`<Method>` pattern (or shows the real name
  on modern runtimes).
- **`End of stack trace from previous location`** marks an async boundary —
  above it is the awaiting side, below is where the async work ran.
- **`throw;` preserves the trace; `throw ex;` resets it** to the rethrow
  site. A trace that "starts" in your error-logging middleware is the
  signature of `throw ex` upstream.
- **InnerException is half the story.** `GetBaseException()` walks to the
  root; the checkpoint's `Describe`/`Analyze` encode that walk.

**AggregateException** carries multiple failures (parallel work). Always
`Flatten()` before analysis — nested aggregates are a maze. And catch
filters (`catch when (e is TimeoutException)`) keep the trace intact while
routing handling — preferable to catch-and-rethrow.

Trace truncation and PII: production traces are often trimmed (that
`<Module>.<PrivateImplementationDetails>` noise) or redacted. If your
diagnosis depends on seeing arguments, structured logging (next lesson) is
the durable path — the trace proves WHERE, logs prove WHAT.
"""

_m16_traces_vi = r"""## Stack trace như bằng chứng

Stack trace là bản ghi đường gọi tại thời điểm thất bại. Đọc nó như bằng
chứng (không phải nhiễu) là một siêu năng lực chẩn đoán:

```
System.InvalidOperationException: queue is empty
   at Solution.PumpAsync(ChannelReader`1 source, ...)
   at Program.<Main>$(String[] args)
   at System.Runtime.CompilerServices.AsyncTaskMethodBuilder.Start[TStateMachine](...)
```

- **Khung đầu = nơi ném.** Đọc XUỐNG để thấy đường dẫn dẫn đến đó. Các khung
  `MoveNext` nghĩa là một máy trạng thái async — tên phương thức gốc nằm
  trong pattern `<>c__DisplayClass`/`<Method>` (hoặc hiện tên thật trên
  runtime hiện đại).
- **`End of stack trace from previous location`** đánh dấu biên async — phía
  trên là bên đang await, phía dưới là nơi công việc async chạy.
- **`throw;` giữ nguyên trace; `throw ex;` reset nó** về nơi ném lại. Một
  trace "bắt đầu" trong middleware log-lỗi của bạn là chữ ký của `throw ex`
  thượng nguồn.
- **InnerException là một nửa câu chuyện.** `GetBaseException()` đi tới gốc;
  `Describe`/`Analyze` trong chính checkpoint mã hóa phép đi đó.

**AggregateException** mang nhiều thất bại (công việc song song). Luôn
`Flatten()` trước khi phân tích — aggregate lồng nhau là mê cung. Và catch
filter (`catch when (e is TimeoutException)`) giữ trace nguyên vẹn trong
khi định tuyến việc xử lý — tốt hơn catch-rồi-ném-lại.

Cắt xén và PII trong trace: trace production thường bị cắt (nhiễu
`<Module>.<PrivateImplementationDetails>` đó) hoặc xóa dữ liệu nhạy cảm.
Nếu chẩn đoán của bạn phụ thuộc vào việc thấy tham số, structured logging
(bài kế tiếp) là đường bền — trace chứng minh Ở ĐÂU, log chứng minh CÁI GÌ.
"""

_m16_forensics = r"""## Failure forensics without a debugger

Production failures rarely come with a debugger attached. The discipline
that replaces it:

**1. Structured logging over string logs.** Emit events with typed
properties, not prose:

```csharp
logger.LogInformation("Order {OrderId} processed in {ElapsedMs}ms items={Count}",
    order.Id, sw.ElapsedMilliseconds, order.Items.Count);
```

Queryable afterward (OrderId=... across services), and the correlation
chain — request ID → order ID → downstream call IDs — is what turns "it
failed somewhere" into a timeline.

**2. Deterministic reproduction.** A bug you can trigger on demand is
dead; a bug that "happens sometimes" is expensive. Techniques that force
reproduction: seed every random source; collapse concurrency (run the
suspect interleaving single-threaded first); shrink the input (find the
minimal failing case); control time (inject a clock). The failing test you
commit is the artifact that prevents regression forever.

**3. The hypothesis discipline.** Worst debugging loop: change something,
run everything, hope. The disciplined loop: write down the hypothesis
("the timeout fires because the token is linked to a long-lived source"),
predict an observable ("logs show cancellation at exactly 30s even when
work takes 2s"), then run the SMALLEST experiment that confirms or kills
it. Binary-search the suspect space — never shotgun.

**4. Evidence preservation.** When a production incident is live: capture
logs and metrics FIRST (they rotate), heap/thread state second, then fix.
Post-incident, the writeup that matters names the root cause, the detection
gap, and the prevention change — blame-free, evidence-full.
"""

_m16_forensics_vi = r"""## Pháp y lỗi mà không cần debugger

Thất bại production hiếm khi đi kèm debugger. Kỷ luật thay thế nó:

**1. Structured logging thay log dạng chuỗi.** Phát các sự kiện với thuộc
tính có kiểu, không phải văn xuôi:

```csharp
logger.LogInformation("Order {OrderId} processed in {ElapsedMs}ms items={Count}",
    order.Id, sw.ElapsedMilliseconds, order.Items.Count);
```

Có thể truy vấn sau đó (OrderId=... xuyên qua các service), và chuỗi tương
quan — request ID → order ID → ID của các lời gọi thượng nguồn — là thứ
biến "nó lỗi đâu đó" thành một dòng thời gian.

**2. Tái hiện tất định.** Bug có thể kích hoạt theo yêu cầu là bug đã chết;
bug "thi thoảng xảy ra" thì đắt đỏ. Các kỹ thuật ép tái hiện: seed mọi
nguồn random; thu gọn đồng thời (chạy kịch bản chen ngang nghi vấn
single-threaded trước); thu nhỏ input (tìm trường hợp lỗi tối thiểu); kiểm
soát thời gian (inject đồng hồ). Test lỗi bạn commit là hiện vật ngăn hồi
quy mãi mãi.

**3. Kỷ luật giả thuyết.** Vòng debug tệ nhất: sửa gì đó, chạy tất cả,
hy vọng. Vòng kỷ luật: viết giả thuyết ra giấy ("timeout bốc cháy vì
token bị link với nguồn sống lâu"), dự đoán một thứ quan sát được ("log
thấy cancel đúng giây thứ 30 dù công việc chỉ 2s"), rồi chạy THÍ NGHIỆM
NHỎ NHẤT xác nhận hoặc tiêu diệt nó. Tìm kiếm nhị phân không gian nghi
phạm — không bao giờ bắn tán loạn.

**4. Bảo toàn bằng chứng.** Khi sự cố production đang diễn ra: chụp log và
metrics TRƯỚC (chúng bị xoay vòng), trạng thái heap/thread thứ hai, rồi
sửa. Sau sự cố, bản viết quan trọng nhất nêu gốc rễ, khoảng trống phát
hiện, và thay đổi phòng ngừa — không đổ lỗi, đầy bằng chứng.
"""

_m16_health = r"""## Health probes and resilience primitives

A debuggable system exposes its own state. The signals orchestrators and
on-call engineers consume:

**Liveness vs readiness.** Liveness = "the process is not wedged" (restart
me if false). Readiness = "I can serve traffic" (route requests to me only
when true). Collapsing them causes the classic outage loop: a service that
reports not-ready because a dependency is down gets restarted — and
restarts make it worse. Readiness checks dependencies; liveness checks
self.

**Circuit breakers** (the checkpoint implements one): stop hammering a
failing dependency; fail fast while it recovers; probe before reopening.
The three states — closed, open, half-open — and their transitions are a
design pattern with a state machine you can unit-test. The knob that
matters is the OPEN DURATION: too short and you half-open into a still-
burning dependency; too long and you shed traffic you could serve.

**Retries with backoff** (the practice implements exponential): retry only
idempotent operations, cap attempts, and back off exponentially — flat
delays create synchronized retry storms. Add jitter in production (spread
retries across clients): the thundering-herd failure is retries aligned to
the dependency's recovery moment.

**Timeouts everywhere.** An operation without a timeout is a resource leak
with extra steps. Every dependency call gets a deadline; every deadline is
enforced via cancellation (Module 9), not polling.

The resilience stack composes: timeout inside retry inside breaker — but
compose them CONSCIOUSLY: retries extend effective timeouts, breakers
change retry behavior, and the combined semantics need a test, not a hope.
"""

_m16_health_vi = r"""## Health probe và các primitive chịu lỗi

Một hệ thống debuggable phải để lộ trạng thái của chính nó. Các tín hiệu
mà orchestrator và kỹ sư trực ban tiêu thụ:

**Liveness vs readiness.** Liveness = "process không bị kẹt" (restart tôi
nếu sai). Readiness = "tôi có thể phục vụ" (chỉ route request cho tôi khi
đúng). Gộp hai cái gây vòng sự cố kinh điển: service báo not-ready vì
phụ thuộc sập sẽ bị restart — và việc restart làm mọi thứ tệ hơn. Readiness
kiểm tra phụ thuộc; liveness kiểm tra bản thân.

**Circuit breaker** (checkpoint cài một cái): ngừng đập vào phụ thuộc đang
lỗi; fail fast trong khi nó hồi phục; thăm dò trước khi mở lại. Ba trạng
thái — closed, open, half-open — và các chuyển tiếp là một design pattern
có máy trạng thái test được bằng unit test. Núm vặn quan trọng là OPEN
DURATION: quá ngắn là half-open vào một phụ thuộc vẫn đang cháy; quá dài
là từ chối lượng traffic bạn vẫn có thể phục vụ.

**Retry với backoff** (practice cài backoff luỹ thừa): chỉ retry các thao
tác idempotent, chặn số lần, và backoff theo luỹ thừa — delay phẳng tạo ra
cơn bão retry đồng bộ. Thêm jitter trong production (rải retry giữa các
client): lỗi thundering-herd là các retry thẳng hàng với khoảnh khắc hồi
phục của phụ thuộc.

**Timeout khắp nơi.** Một thao tác không có timeout là rò rỉ tài nguyên có
thêm các bước dư thừa. Mọi lời gọi phụ thuộc có deadline; mọi deadline được
thi hành qua cancellation (Module 9), không phải polling.

Stack chịu lỗi kết hợp được: timeout trong retry trong breaker — nhưng
hãy kết hợp MỘT CÁCH TỰ GIÁC: retry kéo dài timeout hiệu dụng, breaker
thay đổi hành vi retry, và ngữ nghĩa kết hợp cần một bài test, không phải
một lời cầu nguyện.
"""

_m16_diag = r"""## Checkpoint lesson: diagnose the broken service

A worked diagnosis in five moves — the pattern this course keeps returning
to:

**Symptom:** "The job pipeline hangs after a few hours; restart fixes it."

**Move 1 — characterize.** Hang ≠ crash: threads parked, CPU ~0. Memory
steady or climbing slowly. That profile already excludes CPU-bound
 livelock and pure OOM.

**Move 2 — timeline.** Structured logs: what changed just before the first
hang? Correlation IDs show the last completed job and the first incomplete
one. The boundary is the evidence window.

**Move 3 — hypothesis.** Parked threads + bounded channels: the classic is
a stage whose consumer died while its writer still accepts — the channel's
backpressure then wedges every upstream writer. Prediction: logs show
producers' last entry, consumers' last entry hours earlier; thread dumps
would show `ReadAsync`/`WriteAsync` continuations parked.

**Move 4 — smallest experiment.** Reproduce at small scale: a consumer
that faults mid-run (the checkpoint's channel-drain challenge is exactly
this shape) and observe whether writers wedge. Confirm the mechanism, not
the incident.

**Move 5 — fix the protocol.** The bug is not "a consumer crashed" — it is
"the pipeline has no rule for a dead consumer." The fix: fault the channel
on consumer death (`Complete(ex)`) so producers fail fast, plus a liveness
signal per stage. The incident was one instance of a design gap; the fix
closes the gap, not the instance.

Every step is what the course's challenges force you to practice: read
evidence, form a prediction, run the smallest test, fix the protocol.
"""

_m16_diag_vi = r"""## Bài checkpoint: chẩn đoán service hỏng

Một chẩn đoán mẫu trong năm bước — pattern mà khóa học liên tục quay lại:

**Triệu chứng:** "Pipeline job bị treo sau vài giờ; restart là hết."

**Bước 1 — định dạng.** Treo ≠ sập: thread đang đỗ, CPU ~0. Bộ nhớ ổn định
hoặc leo chậm. Profile đó đã loại livelock gắn CPU và OOM thuần túy.

**Bước 2 — dòng thời gian.** Log có cấu trúc: gì vừa thay đổi ngay trước
lần treo đầu? Correlation ID cho thấy job hoàn thành cuối và job chưa xong
đầu tiên. Ranh giới đó là cửa sổ bằng chứng.

**Bước 3 — giả thuyết.** Thread đỗ + bounded channel: kinh điển là một
tầng mà consumer chết trong khi writer vẫn nhận — backpressure của channel
khiến mọi writer thượng nguồn kẹt theo. Dự đoán: log thấy entry cuối của
producer, entry cuối của consumer sớm hơn vài tiếng; thread dump sẽ thấy
các continuation `ReadAsync`/`WriteAsync` đang đỗ.

**Bước 4 — thí nghiệm nhỏ nhất.** Tái hiện ở quy mô nhỏ: một consumer gặp
lỗi giữa chừng (thử thách channel-drain trong checkpoint đúng hình dạng
này) và quan sát writer có kẹt không. Xác nhận cơ chế, không phải sự cố.

**Bước 5 — sửa giao thức.** Bug không phải "consumer crashed" — mà là
"pipeline không có luật cho consumer chết." Cách sửa: fault channel khi
consumer chết (`Complete(ex)`) để producer fail fast, cộng một tín hiệu
liveness mỗi tầng. Sự cố là một thể hiện của khoảng trống thiết kế; bản
sửa đóng khoảng trống, không phải thể hiện.

Mỗi bước là những gì các thử thách của khóa học buộc bạn luyện: đọc bằng
chứng, hình thành dự đoán, chạy test nhỏ nhất, sửa giao thức.
"""
