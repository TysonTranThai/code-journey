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
        "csa-m16-checkpoint-lesson-task", MID,
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
                    "var nested = new Exception(\"a\", new Exception(\"b\", new Exception(\"c\", root)));\n"
                    "var (d, rootType) = Solution.Analyze(nested);\n"
                    'Cj.Eq(d, 3, "three hops to the root");\n'
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
                    'Cj.Eq(cb.State, "open", "after threshold failure");\n'
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
        title='Retry with exponential backoff',
        prompt=(
            'Implement `static async Task<int> RetryAsync(Func<int> attempt, int maxAttempts, int baseDelayMs)` calling attempt() up to maxAttempts times: on success return the value; on failure await Task.Delay(baseDelayMs * 2^attemptIndex) before the next try (attemptIndex starting at 0). After exhausting attempts throw InvalidOperationException. The test verifies backoff timing directly: with 3 attempts and baseDelayMs=50 the total must reach at least 50 + 100 = 150ms (the exception must propagate too — no sentinel returns).'
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'succeeds-eventually',
                "code": (
                    'int calls = 0;\nvar r = await Solution.RetryAsync(() => { calls++; if (calls < 3) throw new InvalidOperationException(); return 42; }, 5, 1);\nCj.Eq(r, 42, "third attempt wins");\nCj.Eq(calls, 3, "three attempts made");'
                ),
                "hint": 'for (int i = 0; i < maxAttempts; i++) { try { return attempt(); } catch when (i < maxAttempts - 1) { await Task.Delay(baseDelayMs << i); } } — then throw.',
            },
            {
                "name": 'backoff-timing',
                "code": (
                    'var sw = Stopwatch.StartNew();\nvar ex = await Cj.ThrowsAsync<InvalidOperationException>(() => Solution.RetryAsync(() => throw new InvalidOperationException(), 3, 50));\nsw.Stop();\nCj.True(ex is not null, "the exception must propagate - no sentinel returns");\nCj.True(sw.ElapsedMilliseconds >= 145, $"exponential delays 50+100 = 150ms minimum, got {sw.ElapsedMilliseconds}ms");'
                ),
                "hint": 'Delay before retries 2 and 3: 50 * 2^0 = 50, then 50 * 2^1 = 100. Total wait 150ms.',
            },
        ],
        reference=(
            'public class Solution\n{\n    public static async Task<int> RetryAsync(Func<int> attempt, int maxAttempts, int baseDelayMs)\n    {\n        for (int i = 0; i < maxAttempts; i++)\n        {\n            try\n            {\n                return attempt();\n            }\n            catch when (i < maxAttempts - 1)\n            {\n                await Task.Delay(baseDelayMs << i);\n            }\n        }\n        throw new InvalidOperationException($"all {maxAttempts} attempts failed");\n    }\n}'
        ),
        wrong=(
            'public class Solution\n{\n    public static async Task<int> RetryAsync(Func<int> attempt, int maxAttempts, int baseDelayMs)\n    {\n        for (int i = 0; i < maxAttempts; i++)\n        {\n            try { return attempt(); }\n            catch { await Task.Delay(baseDelayMs); }   // WRONG: flat delay, no exponential growth\n        }\n        return -1;   // WRONG: sentinel instead of throwing\n    }\n}'
        ),
        level='guided',
    )


# --- recovered lesson MDX variables (regenerated from the last emit) ---
_m16_traces = '## Stack traces as evidence\n\nA stack trace is a recording of the call path at failure time. Reading it\nlike evidence (not like noise) is a diagnostic superpower:\n\n```\nSystem.InvalidOperationException: queue is empty\n   at Solution.PumpAsync(ChannelReader`1 source, ...)\n   at Program.<Main>$(String[] args)\n   at System.Runtime.CompilerServices.AsyncTaskMethodBuilder.Start[TStateMachine](...)\n```\n\n- **Top frame = throw site.** Read DOWN for the path that led there.\n  `MoveNext` frames mean an async state machine — the original method name\n  is in the `<>c__DisplayClass`/`<Method>` pattern (or shows the real name\n  on modern runtimes).\n- **`End of stack trace from previous location`** marks an async boundary —\n  above it is the awaiting side, below is where the async work ran.\n- **`throw;` preserves the trace; `throw ex;` resets it** to the rethrow\n  site. A trace that "starts" in your error-logging middleware is the\n  signature of `throw ex` upstream.\n- **InnerException is half the story.** `GetBaseException()` walks to the\n  root; the checkpoint\'s `Describe`/`Analyze` encode that walk.\n\n**AggregateException** carries multiple failures (parallel work). Always\n`Flatten()` before analysis — nested aggregates are a maze. And catch\nfilters (`catch when (e is TimeoutException)`) keep the trace intact while\nrouting handling — preferable to catch-and-rethrow.\n\nTrace truncation and PII: production traces are often trimmed (that\n`<Module>.<PrivateImplementationDetails>` noise) or redacted. If your\ndiagnosis depends on seeing arguments, structured logging (next lesson) is\nthe durable path — the trace proves WHERE, logs prove WHAT.\n'
_m16_traces_vi = '## Stack trace như bằng chứng\n\nStack trace là bản ghi đường gọi tại thời điểm thất bại. Đọc nó như bằng\nchứng (không phải nhiễu) là một siêu năng lực chẩn đoán:\n\n```\nSystem.InvalidOperationException: queue is empty\n   at Solution.PumpAsync(ChannelReader`1 source, ...)\n   at Program.<Main>$(String[] args)\n   at System.Runtime.CompilerServices.AsyncTaskMethodBuilder.Start[TStateMachine](...)\n```\n\n- **Khung đầu = nơi ném.** Đọc XUỐNG để thấy đường dẫn dẫn đến đó. Các khung\n  `MoveNext` nghĩa là một máy trạng thái async — tên phương thức gốc nằm\n  trong pattern `<>c__DisplayClass`/`<Method>` (hoặc hiện tên thật trên\n  runtime hiện đại).\n- **`End of stack trace from previous location`** đánh dấu biên async — phía\n  trên là bên đang await, phía dưới là nơi công việc async chạy.\n- **`throw;` giữ nguyên trace; `throw ex;` reset nó** về nơi ném lại. Một\n  trace "bắt đầu" trong middleware log-lỗi của bạn là chữ ký của `throw ex`\n  thượng nguồn.\n- **InnerException là một nửa câu chuyện.** `GetBaseException()` đi tới gốc;\n  `Describe`/`Analyze` trong chính checkpoint mã hóa phép đi đó.\n\n**AggregateException** mang nhiều thất bại (công việc song song). Luôn\n`Flatten()` trước khi phân tích — aggregate lồng nhau là mê cung. Và catch\nfilter (`catch when (e is TimeoutException)`) giữ trace nguyên vẹn trong\nkhi định tuyến việc xử lý — tốt hơn catch-rồi-ném-lại.\n\nCắt xén và PII trong trace: trace production thường bị cắt (nhiễu\n`<Module>.<PrivateImplementationDetails>` đó) hoặc xóa dữ liệu nhạy cảm.\nNếu chẩn đoán của bạn phụ thuộc vào việc thấy tham số, structured logging\n(bài kế tiếp) là đường bền — trace chứng minh Ở ĐÂU, log chứng minh CÁI GÌ.\n'
_m16_forensics = '## Failure forensics without a debugger\n\nProduction failures rarely come with a debugger attached. The discipline\nthat replaces it:\n\n**1. Structured logging over string logs.** Emit events with typed\nproperties, not prose:\n\n```csharp\nlogger.LogInformation("Order {OrderId} processed in {ElapsedMs}ms items={Count}",\n    order.Id, sw.ElapsedMilliseconds, order.Items.Count);\n```\n\nQueryable afterward (OrderId=... across services), and the correlation\nchain — request ID → order ID → downstream call IDs — is what turns "it\nfailed somewhere" into a timeline.\n\n**2. Deterministic reproduction.** A bug you can trigger on demand is\ndead; a bug that "happens sometimes" is expensive. Techniques that force\nreproduction: seed every random source; collapse concurrency (run the\nsuspect interleaving single-threaded first); shrink the input (find the\nminimal failing case); control time (inject a clock). The failing test you\ncommit is the artifact that prevents regression forever.\n\n**3. The hypothesis discipline.** Worst debugging loop: change something,\nrun everything, hope. The disciplined loop: write down the hypothesis\n("the timeout fires because the token is linked to a long-lived source"),\npredict an observable ("logs show cancellation at exactly 30s even when\nwork takes 2s"), then run the SMALLEST experiment that confirms or kills\nit. Binary-search the suspect space — never shotgun.\n\n**4. Evidence preservation.** When a production incident is live: capture\nlogs and metrics FIRST (they rotate), heap/thread state second, then fix.\nPost-incident, the writeup that matters names the root cause, the detection\ngap, and the prevention change — blame-free, evidence-full.\n'
_m16_forensics_vi = '## Pháp y lỗi mà không cần debugger\n\nThất bại production hiếm khi đi kèm debugger. Kỷ luật thay thế nó:\n\n**1. Structured logging thay log dạng chuỗi.** Phát các sự kiện với thuộc\ntính có kiểu, không phải văn xuôi:\n\n```csharp\nlogger.LogInformation("Order {OrderId} processed in {ElapsedMs}ms items={Count}",\n    order.Id, sw.ElapsedMilliseconds, order.Items.Count);\n```\n\nCó thể truy vấn sau đó (OrderId=... xuyên qua các service), và chuỗi tương\nquan — request ID → order ID → ID của các lời gọi thượng nguồn — là thứ\nbiến "nó lỗi đâu đó" thành một dòng thời gian.\n\n**2. Tái hiện tất định.** Bug có thể kích hoạt theo yêu cầu là bug đã chết;\nbug "thi thoảng xảy ra" thì đắt đỏ. Các kỹ thuật ép tái hiện: seed mọi\nnguồn random; thu gọn đồng thời (chạy kịch bản chen ngang nghi vấn\nsingle-threaded trước); thu nhỏ input (tìm trường hợp lỗi tối thiểu); kiểm\nsoát thời gian (inject đồng hồ). Test lỗi bạn commit là hiện vật ngăn hồi\nquy mãi mãi.\n\n**3. Kỷ luật giả thuyết.** Vòng debug tệ nhất: sửa gì đó, chạy tất cả,\nhy vọng. Vòng kỷ luật: viết giả thuyết ra giấy ("timeout bốc cháy vì\ntoken bị link với nguồn sống lâu"), dự đoán một thứ quan sát được ("log\nthấy cancel đúng giây thứ 30 dù công việc chỉ 2s"), rồi chạy THÍ NGHIỆM\nNHỎ NHẤT xác nhận hoặc tiêu diệt nó. Tìm kiếm nhị phân không gian nghi\nphạm — không bao giờ bắn tán loạn.\n\n**4. Bảo toàn bằng chứng.** Khi sự cố production đang diễn ra: chụp log và\nmetrics TRƯỚC (chúng bị xoay vòng), trạng thái heap/thread thứ hai, rồi\nsửa. Sau sự cố, bản viết quan trọng nhất nêu gốc rễ, khoảng trống phát\nhiện, và thay đổi phòng ngừa — không đổ lỗi, đầy bằng chứng.\n'
_m16_health = '## Health probes and resilience primitives\n\nA debuggable system exposes its own state. The signals orchestrators and\non-call engineers consume:\n\n**Liveness vs readiness.** Liveness = "the process is not wedged" (restart\nme if false). Readiness = "I can serve traffic" (route requests to me only\nwhen true). Collapsing them causes the classic outage loop: a service that\nreports not-ready because a dependency is down gets restarted — and\nrestarts make it worse. Readiness checks dependencies; liveness checks\nself.\n\n**Circuit breakers** (the checkpoint implements one): stop hammering a\nfailing dependency; fail fast while it recovers; probe before reopening.\nThe three states — closed, open, half-open — and their transitions are a\ndesign pattern with a state machine you can unit-test. The knob that\nmatters is the OPEN DURATION: too short and you half-open into a still-\nburning dependency; too long and you shed traffic you could serve.\n\n**Retries with backoff** (the practice implements exponential): retry only\nidempotent operations, cap attempts, and back off exponentially — flat\ndelays create synchronized retry storms. Add jitter in production (spread\nretries across clients): the thundering-herd failure is retries aligned to\nthe dependency\'s recovery moment.\n\n**Timeouts everywhere.** An operation without a timeout is a resource leak\nwith extra steps. Every dependency call gets a deadline; every deadline is\nenforced via cancellation (Module 9), not polling.\n\nThe resilience stack composes: timeout inside retry inside breaker — but\ncompose them CONSCIOUSLY: retries extend effective timeouts, breakers\nchange retry behavior, and the combined semantics need a test, not a hope.\n'
_m16_health_vi = '## Health probe và các primitive chịu lỗi\n\nMột hệ thống debuggable phải để lộ trạng thái của chính nó. Các tín hiệu\nmà orchestrator và kỹ sư trực ban tiêu thụ:\n\n**Liveness vs readiness.** Liveness = "process không bị kẹt" (restart tôi\nnếu sai). Readiness = "tôi có thể phục vụ" (chỉ route request cho tôi khi\nđúng). Gộp hai cái gây vòng sự cố kinh điển: service báo not-ready vì\nphụ thuộc sập sẽ bị restart — và việc restart làm mọi thứ tệ hơn. Readiness\nkiểm tra phụ thuộc; liveness kiểm tra bản thân.\n\n**Circuit breaker** (checkpoint cài một cái): ngừng đập vào phụ thuộc đang\nlỗi; fail fast trong khi nó hồi phục; thăm dò trước khi mở lại. Ba trạng\nthái — closed, open, half-open — và các chuyển tiếp là một design pattern\ncó máy trạng thái test được bằng unit test. Núm vặn quan trọng là OPEN\nDURATION: quá ngắn là half-open vào một phụ thuộc vẫn đang cháy; quá dài\nlà từ chối lượng traffic bạn vẫn có thể phục vụ.\n\n**Retry với backoff** (practice cài backoff luỹ thừa): chỉ retry các thao\ntác idempotent, chặn số lần, và backoff theo luỹ thừa — delay phẳng tạo ra\ncơn bão retry đồng bộ. Thêm jitter trong production (rải retry giữa các\nclient): lỗi thundering-herd là các retry thẳng hàng với khoảnh khắc hồi\nphục của phụ thuộc.\n\n**Timeout khắp nơi.** Một thao tác không có timeout là rò rỉ tài nguyên có\nthêm các bước dư thừa. Mọi lời gọi phụ thuộc có deadline; mọi deadline được\nthi hành qua cancellation (Module 9), không phải polling.\n\nStack chịu lỗi kết hợp được: timeout trong retry trong breaker — nhưng\nhãy kết hợp MỘT CÁCH TỰ GIÁC: retry kéo dài timeout hiệu dụng, breaker\nthay đổi hành vi retry, và ngữ nghĩa kết hợp cần một bài test, không phải\nmột lời cầu nguyện.\n'
_m16_diag = '## Checkpoint lesson: diagnose the broken service\n\nA worked diagnosis in five moves — the pattern this course keeps returning\nto:\n\n**Symptom:** "The job pipeline hangs after a few hours; restart fixes it."\n\n**Move 1 — characterize.** Hang ≠ crash: threads parked, CPU ~0. Memory\nsteady or climbing slowly. That profile already excludes CPU-bound\n livelock and pure OOM.\n\n**Move 2 — timeline.** Structured logs: what changed just before the first\nhang? Correlation IDs show the last completed job and the first incomplete\none. The boundary is the evidence window.\n\n**Move 3 — hypothesis.** Parked threads + bounded channels: the classic is\na stage whose consumer died while its writer still accepts — the channel\'s\nbackpressure then wedges every upstream writer. Prediction: logs show\nproducers\' last entry, consumers\' last entry hours earlier; thread dumps\nwould show `ReadAsync`/`WriteAsync` continuations parked.\n\n**Move 4 — smallest experiment.** Reproduce at small scale: a consumer\nthat faults mid-run (the checkpoint\'s channel-drain challenge is exactly\nthis shape) and observe whether writers wedge. Confirm the mechanism, not\nthe incident.\n\n**Move 5 — fix the protocol.** The bug is not "a consumer crashed" — it is\n"the pipeline has no rule for a dead consumer." The fix: fault the channel\non consumer death (`Complete(ex)`) so producers fail fast, plus a liveness\nsignal per stage. The incident was one instance of a design gap; the fix\ncloses the gap, not the instance.\n\nEvery step is what the course\'s challenges force you to practice: read\nevidence, form a prediction, run the smallest test, fix the protocol.\n'
_m16_diag_vi = '## Bài checkpoint: chẩn đoán service hỏng\n\nMột chẩn đoán mẫu trong năm bước — pattern mà khóa học liên tục quay lại:\n\n**Triệu chứng:** "Pipeline job bị treo sau vài giờ; restart là hết."\n\n**Bước 1 — định dạng.** Treo ≠ sập: thread đang đỗ, CPU ~0. Bộ nhớ ổn định\nhoặc leo chậm. Profile đó đã loại livelock gắn CPU và OOM thuần túy.\n\n**Bước 2 — dòng thời gian.** Log có cấu trúc: gì vừa thay đổi ngay trước\nlần treo đầu? Correlation ID cho thấy job hoàn thành cuối và job chưa xong\nđầu tiên. Ranh giới đó là cửa sổ bằng chứng.\n\n**Bước 3 — giả thuyết.** Thread đỗ + bounded channel: kinh điển là một\ntầng mà consumer chết trong khi writer vẫn nhận — backpressure của channel\nkhiến mọi writer thượng nguồn kẹt theo. Dự đoán: log thấy entry cuối của\nproducer, entry cuối của consumer sớm hơn vài tiếng; thread dump sẽ thấy\ncác continuation `ReadAsync`/`WriteAsync` đang đỗ.\n\n**Bước 4 — thí nghiệm nhỏ nhất.** Tái hiện ở quy mô nhỏ: một consumer gặp\nlỗi giữa chừng (thử thách channel-drain trong checkpoint đúng hình dạng\nnày) và quan sát writer có kẹt không. Xác nhận cơ chế, không phải sự cố.\n\n**Bước 5 — sửa giao thức.** Bug không phải "consumer crashed" — mà là\n"pipeline không có luật cho consumer chết." Cách sửa: fault channel khi\nconsumer chết (`Complete(ex)`) để producer fail fast, cộng một tín hiệu\nliveness mỗi tầng. Sự cố là một thể hiện của khoảng trống thiết kế; bản\nsửa đóng khoảng trống, không phải thể hiện.\n\nMỗi bước là những gì các thử thách của khóa học buộc bạn luyện: đọc bằng\nchứng, hình thành dự đoán, chạy test nhỏ nhất, sửa giao thức.\n'

"""
Authoring notes — regeneration loop: `python3 csa_emit.py` rewrites every
EN/VI JSON + MDX under the course dir, then
`node --import tsx validate-content-csa.ts` proves both locales load.
"""
