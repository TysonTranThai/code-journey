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
