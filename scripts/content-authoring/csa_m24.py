"""Module 24 — Production architecture and final capstone (csa-m24)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-capstone",
        "Production Architecture and Capstone",
        "Modular monoliths, dependency direction, observability, resilience — and a job-processing platform that assembles everything.",
    )

    csa.register_lesson(
        MID, "csa-m24-architecture", "Modular monoliths and dependency direction",
        "Boundaries you can enforce, the cost ladder of distribution, and why the dependency arrows decide the architecture.",
        15, "advanced", _m24_architecture, _m24_architecture_vi,
    )
    csa.register_lesson(
        MID, "csa-m24-observability", "Observability: logs, metrics, traces",
        "Structured logs for the what, metrics for the how-much, traces for the where — and SLOs to make any of it matter.",
        15, "advanced", _m24_observability, _m24_observability_vi,
    )
    csa.register_lesson(
        MID, "csa-m24-reliability", "Reliability: retries, idempotency, backpressure",
        "The failure-handling stack assembled: timeouts inside retries inside breakers, idempotent handlers, bounded work.",
        15, "advanced", _m24_reliability, _m24_reliability_vi,
    )
    csa.register_lesson(
        MID, "csa-m24-capstone-brief", "Capstone: the job-processing platform",
        "The full brief: acceptance API with idempotency keys, bounded queue, retrying worker, DLQ, metrics — milestones and grading.",
        16, "advanced", _m24_capstone, _m24_capstone_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m24", "Checkpoint: production architecture",
        "Final synthesis — idempotent, backpressured, retrying job intake under a deterministic request schedule.",
        12, "advanced", _m24_checkpoint, _m24_checkpoint_vi,
    )

    csa.register_challenge(
        "csa-checkpoint-m24-task", MID,
        title="Capstone checkpoint",
        prompt=(
            "Assemble the platform core as `class JobPlatform`. Constructor: `JobPlatform(int capacity)`. Methods: "
            "`(bool accepted) Submit(string jobId, Func<int> work)` — accepts only if the jobId was never seen AND"            "in-flight count < capacity (idempotency + backpressure; duplicates and over-capacity return false and "
            "count as rejected); `int RunAll()` — executes every accepted job exactly once (chronologically), returns "
            "the work-counter delta (equals accepted count — proving each job ran once); `int Pending` property. Then "
            "`static (int accepted, int rejected, int executed) SubmitSchedule(JobPlatform p, List<string> jobIds, int "
            "duplicatesPerJob)` — submits each id (1 + duplicatesPerJob) times, returns accepted/rejected counts and "
            "executed = RunAll()."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "idempotent-and-bounded",
                "code": (
                    "var p = new JobPlatform(2);\n"
                    'Cj.Eq(p.Submit("a", () => 1), true, "first submit accepted");\n'
                    'Cj.Eq(p.Submit("a", () => 1), false, "duplicate rejected");\n'
                    'Cj.Eq(p.Submit("b", () => 1), true, "second slot used");\n'
                    'Cj.Eq(p.Submit("c", () => 1), false, "capacity exceeded");\n'
                    'Cj.Eq(p.Pending, 2, "two jobs pending");'
                ),
                "hint": "HashSet<string> seen + a pending list; accept when !seen.Contains && pending.Count < capacity.",
            },
            {
                "name": "schedule-runs-once",
                "code": (
                    "var p = new JobPlatform(20);\n"
                    "var ids = Enumerable.Range(0, 12).Select(i => $\"job-{i}\").ToList();\n"
                    "var (accepted, rejected, executed) = JobPlatform.SubmitSchedule(p, ids, 2);\n"
                    'Cj.Eq(accepted, 12, "12 unique ids accepted");\n'
                    'Cj.Eq(rejected, 24, "36 deliveries − 12 uniques rejected as duplicates");\n'
                    'Cj.Eq(executed, 12, "each job executed exactly once");'
                ),
                "hint": "SubmitSchedule: deliver each id (1+duplicates) times; executed = p.RunAll(); work counter shared.",
            },
        ],
        reference=(
            "public class JobPlatform\n{\n"
            "    private readonly HashSet<string> _seen = new();\n"
            "    private readonly List<Func<int>> _pending = new();\n"
            "    private static int _executed;\n"
            "    private readonly int _capacity;\n\n"
            "    public JobPlatform(int capacity) => _capacity = capacity;\n\n"
            "    public int Pending => _pending.Count;\n\n"
            "    public bool Submit(string jobId, Func<int> work)\n"
            "    {\n"
            "        if (_seen.Contains(jobId) || _pending.Count >= _capacity) return false;\n"
            "        _seen.Add(jobId);\n"
            "        _pending.Add(() => { _ = work(); System.Threading.Interlocked.Increment(ref _executed); return 0; });\n"
            "        return true;\n"
            "    }\n\n"
            "    public int RunAll()\n"
            "    {\n"
            "        int before = _executed;\n"
            "        foreach (var job in _pending) job();\n"
            "        _pending.Clear();\n"
            "        return _executed - before;\n"
            "    }\n\n"
            "    public static (int accepted, int rejected, int executed) SubmitSchedule(JobPlatform p, List<string> jobIds, int duplicatesPerJob)\n"
            "    {\n"
            "        int accepted = 0, rejected = 0;\n"
            "        for (int d = 0; d <= duplicatesPerJob; d++)\n"
            "            foreach (var id in jobIds)\n"
            "            {\n"
            "                if (p.Submit(id, () => 0)) accepted++; else rejected++;\n"
            "            }\n"
            "        int executed = p.RunAll();\n"
            "        return (accepted, rejected, executed);\n"
            "    }\n}"
        ),
        wrong=(
            "public class JobPlatform\n{\n"
            "    private readonly HashSet<string> _seen = new();\n"
            "    private readonly List<Func<int>> _pending = new();\n"
            "    private static int _executed;\n"
            "    private readonly int _capacity;\n\n"
            "    public JobPlatform(int capacity) => _capacity = capacity;\n\n"
            "    public int Pending => _pending.Count;\n\n"
            "    public bool Submit(string jobId, Func<int> work)\n"
            "    {\n"
            "        if (_pending.Count >= _capacity) return false;   // WRONG: no idempotency — duplicates re-queued\n"
            "        _seen.Add(jobId);\n"
            "        _pending.Add(() => { _ = work(); System.Threading.Interlocked.Increment(ref _executed); return 0; });\n"
            "        return true;\n"
            "    }\n\n"
            "    public int RunAll()\n"
            "    {\n"
            "        int before = _executed;\n"
            "        foreach (var job in _pending) job();\n"
            "        _pending.Clear();\n"
            "        return _executed - before;\n"
            "    }\n\n"
            "    public static (int accepted, int rejected, int executed) SubmitSchedule(JobPlatform p, List<string> jobIds, int duplicatesPerJob)\n"
            "    {\n"
            "        int accepted = 0, rejected = 0;\n"
            "        for (int d = 0; d <= duplicatesPerJob; d++)\n"
            "            foreach (var id in jobIds)\n"
            "            {\n"
            "                if (p.Submit(id, () => 0)) accepted++; else rejected++;\n"
            "            }\n"
            "        int executed = p.RunAll();\n"
            "        return (accepted, rejected, executed);\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p24-production", "Production drills",
        "Capacity arithmetic, SLO error budgets, and DLQ promotion rules — deterministic decision tables.",
        45, "advanced", "csa-m24-reliability",
        ["csa-p24-slo-budget", "csa-p24-dlq-promotion"],
    )
    csa.register_challenge(
        "csa-p24-slo-budget", MID,
        title="SLO error budget",
        prompt=(
            "An SLO of 99.9% availability over a 30-day window (2,592,000 s) grants an error budget of "
            "`budgetSeconds = window × (1 − slo)`. Implement `static double BudgetSeconds(double windowSeconds, double "
            "slo)` and `static (double remaining, bool within) Spend(double windowSeconds, double slo, double "
            "downtimeSeconds)` returning remaining budget and whether downtime is still within it (within = downtime ≤ "
            "budget)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "budget-math",
                "code": (
                    'Cj.Eq(Slo.BudgetSeconds(2592000, 0.999), 2592.0, "0.1% of 30 days");\n'
                    'var (rem, ok) = Slo.Spend(2592000, 0.999, 1500);\n'
                    'Cj.Eq(rem, 1092.0, "2592 − 1500");\n'
                    'Cj.Eq(ok, true, "within budget");\n'
                    'var (rem2, ok2) = Slo.Spend(2592000, 0.999, 3000);\n'
                    'Cj.Eq(ok2, false, "over budget");'
                ),
                "hint": "budget = window × (1 − slo); remaining = budget − downtime; within = downtime ≤ budget.",
            },
        ],
        reference=(
            "public static class Slo\n{\n"
            "    public static double BudgetSeconds(double windowSeconds, double slo) =>\n"
            "        windowSeconds * (1 - slo);\n\n"
            "    public static (double remaining, bool within) Spend(double windowSeconds, double slo, double downtimeSeconds)\n"
            "    {\n"
            "        double budget = BudgetSeconds(windowSeconds, slo);\n"
            "        return (budget - downtimeSeconds, downtimeSeconds <= budget);\n"
            "    }\n}"
        ),
        wrong=(
            "public static class Slo\n{\n"
            "    public static double BudgetSeconds(double windowSeconds, double slo) =>\n"
            "        windowSeconds * slo;   // WRONG: budgets the good time, not the bad\n\n"
            "    public static (double remaining, bool within) Spend(double windowSeconds, double slo, double downtimeSeconds)\n"
            "    {\n"
            "        double budget = BudgetSeconds(windowSeconds, slo);\n"
            "        return (budget - downtimeSeconds, downtimeSeconds <= budget);\n"
            "    }\n}"
        ),
        level="real-world",
    )
    csa.register_challenge(
        "csa-p24-dlq-promotion", MID,
        title="DLQ promotion rule",
        prompt=(
            "A job lands in the dead-letter queue when failures reach the threshold. Implement `static (bool dead, int "
            "failures) OnFailure(int currentFailures, int threshold, int maxAttempts)` — increments failures; dead = "
            "failures ≥ threshold OR attempts exhausted (maxAttempts), and failures saturate at threshold (never grow "
            "past it once dead)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "promotion-rules",
                "code": (
                    'var r1 = Dlq.OnFailure(0, 3, 5);\n'
                    'Cj.Eq(r1.failures, 1, "one failure");\n'
                    'Cj.Eq(r1.dead, false, "below threshold");\n'
                    'var r2 = Dlq.OnFailure(2, 3, 5);\n'
                    'Cj.Eq(r2.dead, true, "threshold reached");\n'
                    'Cj.Eq(r2.failures, 3, "saturated at threshold");\n'
                    'var r3 = Dlq.OnFailure(1, 10, 5);\n'
                    'Cj.Eq(r3.dead, false, "attempts not yet exhausted");\n'
                    'var r4 = Dlq.OnFailure(1, 10, 1);\n'
                    'Cj.Eq(r4.dead, true, "attempts exhausted promotes");'
                ),
                "hint": "failures = min(current+1, threshold); dead = failures ≥ threshold || maxAttempts ≤ current+1... decide your exact exhaustion semantics and match the tests.",
            },
        ],
        reference=(
            "public static class Dlq\n{\n"
            "    public static (bool dead, int failures) OnFailure(int currentFailures, int threshold, int maxAttempts)\n"
            "    {\n"
            "        int failures = Math.Min(currentFailures + 1, threshold);\n"
            "        bool dead = failures >= threshold || currentFailures + 1 >= maxAttempts;\n"
            "        return (dead, failures);\n"
            "    }\n}"
        ),
        wrong=(
            "public static class Dlq\n{\n"
            "    public static (bool dead, int failures) OnFailure(int currentFailures, int threshold, int maxAttempts)\n"
            "    {\n"
            "        int failures = currentFailures + 1;   // WRONG: unsaturated counter grows unbounded\n"
            "        bool dead = failures > threshold;\n"
            "        return (dead, failures);\n"
            "    }\n}"
        ),
        level="real-world",
    )

    # ── Lesson bodies ────────────────────────────────────────────────────────


_m24_architecture = r"""## Modular monoliths and dependency direction

Every architecture decision here reduces to one question: **which way do the
arrows point?** A modular monolith is one deployable with *enforced* internal
boundaries: modules communicate through interfaces, and the dependency arrows
point from feature code toward abstractions — never sideways into another
module's internals, never from domain logic toward infrastructure details.

The cost ladder of distribution (module 20's lesson, restated
architecturally): a method call is nanoseconds and always works; a network
call is milliseconds, fails in new ways, and needs a version story. **Do not
pay the network's tax until a boundary genuinely demands it** — independent
scaling, independent deployment, or organizational ownership. "Microservices"
chosen for resume reasons are a modular monolith with a distributed-systems
incident generator bolted on.

Enforcement beats aspiration: compiler-visible boundaries (separate projects,
`internal` types, dependency-checking analyzers) survive deadlines; comments
on an architecture diagram do not. The capstone keeps everything in one
process but demands the *discipline* — one `JobPlatform` seam through which
all work enters, exactly like one API gateway in a real system.
"""


_m24_architecture_vi = r"""## Modular monolith và hướng phụ thuộc

Mọi quyết định kiến trúc ở đây quy về một câu hỏi: **các mũi tên chỉ về đâu?**
Một modular monolith là một deployable với ranh giới nội bộ *được thi hành*:
các module giao tiếp qua interface, và các mũi tên phụ thuộc chỉ từ code tính
năng hướng về trừu tượng — không bao giờ ngang sang nội bộ module khác, không
bao giờ từ logic miền hướng về chi tiết hạ tầng.

Bậc thang chi phí của việc phân tán (bài học module 20, nói lại theo kiến
trúc): một lời gọi phương thức là nano-giây và luôn hoạt động; một lời gọi
mạng là mili-giây, thất bại theo những cách mới, và cần câu chuyện phiên bản.
**Đừng trả thuế của mạng cho đến khi một ranh giới thật sự đòi hỏi** — scale
độc lập, deploy độc lập, hoặc quyền sở hữu theo tổ chức. "Microservice" chọn
vì lý do CV là một modular monolith gắn thêm một máy phát sự cố hệ phân tán.

Thi hành thắng khát vọng: ranh giới nhìn thấy được bởi compiler (project
riêng, kiểu `internal`, analyzer kiểm tra phụ thuộc) sống sót qua deadline;
chú thích trên sơ đồ kiến trúc thì không. Capstone giữ mọi thứ trong một tiến
trình nhưng đòi hỏi *kỷ luật* — một đường seam `JobPlatform` mà mọi công việc
đi qua, đúng như một API gateway trong hệ thống thật.
"""


_m24_observability = r"""## Observability: logs, metrics, traces

Three signals, three questions:

- **Structured logs** answer *what happened* — events with fields, not
  strings. `Log.Information("Job {JobId} failed after {Attempts}", jobId,
  attempts)` is queryable; string interpolation is not. One correlation id per
  request, propagated everywhere (module 17), turns logs into a story.
- **Metrics** answer *how much / how fast* — cheap numbers you can alert on:
  request rate, error rate, duration histograms, queue depth, GC counts
  (module 14's counters become production dashboards).
- **Traces** answer *where did the time go* — spans stitched by shared ids
  across services. The trace tree is the only honest answer to "which of
  these four calls is slow?"

The discipline that makes any of it useful: define **SLOs** first. An SLO
("99.9% of job submissions accepted in < 200 ms") plus a measured window gives
an **error budget** — the arithmetic the drill encodes. Budget remaining →
ship features; budget burned → reliability work takes priority. Without an
SLO, "observability" is just expensive logging.

Anti-pattern to reject: logging PII (emails, tokens) into systems whose
access you do not control. Observability data is a security surface (module
23) — redact at the boundary.
"""


_m24_observability_vi = r"""## Khả năng quan sát: log, metric, trace

Ba tín hiệu, ba câu hỏi:

- **Structured log** trả lời *chuyện gì xảy ra* — sự kiện có trường, không
  phải chuỗi. `Log.Information("Job {JobId} failed after {Attempts}", jobId,
  attempts)` truy vấn được; string interpolation thì không. Một correlation id
  cho mỗi request, truyền khắp nơi (module 17), biến log thành một câu chuyện.
- **Metric** trả lời *bao nhiêu / nhanh cỡ nào* — những con số rẻ để bật cảnh
  báo: tốc độ request, tỉ lệ lỗi, histogram thời lượng, độ sâu hàng đợi, số
  đếm GC (các bộ đếm module 14 thành dashboard production).
- **Trace** trả lời *thời gian đi đâu* — các span nối bằng id chung qua các
  service. Cây trace là câu trả lời trung thực duy nhất cho "trong bốn lời
  gọi này cái nào chậm?"

Kỷ luật khiến mọi thứ hữu ích: định nghĩa **SLO** trước. Một SLO ("99,9% lần
gửi job được chấp nhận trong < 200 ms") cộng cửa sổ đo cho ra một **ngân sách
lỗi** — phép tính bài tập mã hóa. Ngân sách còn → ship tính năng; ngân sách
cháy → việc độ tin cậy ưu tiên. Không có SLO, "observability" chỉ là ghi log
đắt tiền.

Anti-pattern cần từ chối: log PII (email, token) vào hệ thống mà bạn không
kiểm soát quyền truy cập. Dữ liệu observability là một bề mặt bảo mật
(module 23) — redact ngay tại biên.
"""


_m24_reliability = r"""## Reliability: retries, idempotency, backpressure

The stack from module 20 returns, assembled: **timeout** inside **retry**
(with exponential backoff and jitter) inside a **circuit breaker**, all
wrapped around operations that are **idempotent** — because a retry after an
ambiguous failure is indistinguishable from a duplicate delivery, and the
handler must make duplicates harmless (the checkpoint of module 20, now
load-bearing).

Backpressure closes the loop: an unbounded queue is a slow-motion crash — it
converts "we are overloaded" into "we are overloaded *and* out of memory,
*and* every latency SLO is dead." A bounded queue with an explicit admission
decision (reject fast, return `429`-style responses, let callers decide) keeps
the system honest. The capstone's `Submit` returns `false` over capacity:
that is the whole production posture in one boolean.

Failure injection is the teaching method here: the platform is graded by a
*deterministic schedule* of duplicate deliveries and over-capacity submits,
so every acceptance/rejection/executed count is a contract you can reason
about — the same way you reason about a load test before black Friday.
"""


_m24_reliability_vi = r"""## Độ tin cậy: retry, idempotency, backpressure

Ngăn xếp từ module 20 quay lại, được lắp ráp: **timeout** bên trong **retry**
(với exponential backoff và jitter) bên trong một **circuit breaker**, tất cả
bao quanh các thao tác **idempotent** — vì một retry sau một thất bại mơ hồ
không thể phân biệt với một lần gửi trùng, và handler phải làm cho bản trùng
vô hại (checkpoint module 20, giờ chịu lực).

Backpressure khép vòng: một hàng đợi không giới hạn là một vụ sập trong slow
motion — nó biến "chúng ta quá tải" thành "chúng ta quá tải *và* hết bộ nhớ,
*và* mọi SLO độ trễ đã chết". Một hàng đợi có giới hạn với quyết định tiếp
nhận tường minh (từ chối nhanh, trả phản hồi kiểu `429`, để caller tự quyết)
giữ cho hệ thống trung thực. `Submit` của capstone trả `false` khi vượt quá
sức chứa: đó là toàn bộ tư thế production trong một boolean.

Fault injection là phương pháp dạy ở đây: nền tảng được chấm điểm bằng một
*lịch* deterministic gồm các lần gửi trùng và vượt sức chứa, nên mọi con số
chấp nhận/từ chối/thực-thi đều là một hợp đồng bạn có thể suy luận — giống
hệt cách bạn suy luận về một bài load test trước black Friday.
"""


_m24_capstone = r"""## Capstone: the job-processing platform

Everything from 21 modules converges into one design brief:

- **Acceptance API** — idempotency keys (`jobId` seen-set), admission control
  against a capacity limit (backpressure), fast rejections.
- **Work store** — the pending set, drained by `RunAll` exactly-once
  (deterministic stand-in for the Channels pipeline of module 13).
- **Retrying worker** — per-job attempt tracking with a failure threshold and
  DLQ promotion (the drill's rule table, now real code in the exercises).
- **Observability hooks** — work counters, rejected/accepted metrics, and an
  SLO arithmetic layer (drill 1).
- **The architecture discipline** — one seam, dependency arrows toward
  abstractions, no sideways pokes into another concept's internals.

The in-sandbox graded portion (the checkpoint) verifies the three contracts
that matter most and are most often broken in production: *duplicates are
absorbed* (idempotency), *overload is rejected* (backpressure), and *accepted
work executes exactly once* (exactly-once semantics, achieved via idempotent
intake + tracked execution). Extensions for self-study: wire the platform to
a real `Channel<T>` with bounded capacity, add a `Polly`-style policy pipeline
around `Submit`, and write the SLO dashboard queries you would run.

Ship it with the module-14 discipline: measure allocations and counters for
your implementation, and be able to say *why* each design decision — not just
that it works.
"""


_m24_capstone_vi = r"""## Capstone: nền tảng xử lý job

Mọi thứ từ 21 module hội tụ vào một bản thiết kế:

- **API tiếp nhận** — idempotency key (seen-set `jobId`), kiểm soát tiếp nhận
  theo giới hạn sức chứa (backpressure), từ chối nhanh.
- **Kho công việc** — tập pending, được `RunAll` rút cạn exactly-once (bản
  thay thế deterministic cho pipeline Channels của module 13).
- **Worker retry** — theo dõi số lần thử theo từng job với ngưỡng thất bại và
  thăng hạng DLQ (bảng quy tắc của bài tập, giờ là code thật trong exercise).
- **Hook quan sát** — bộ đếm công việc, metric bị từ chối/được chấp nhận, và
  một lớp số học SLO (bài tập 1).
- **Kỷ luật kiến trúc** — một seam, mũi tên phụ thuộc hướng về trừu tượng,
  không tự ý giắc vào nội bộ của khái niệm khác.

Phần được chấm điểm trong sandbox (checkpoint) xác minh ba hợp đồng quan
trọng nhất và thường bị vi phạm nhất trong production: *bản trùng được hấp
thụ* (idempotency), *quá tải bị từ chối* (backpressure), và *công việc đã
chấp nhận thực thi đúng một lần* (exactly-once, đạt được qua intake
idempotent + thực thi có theo dõi). Phần mở rộng tự học: nối nền tảng vào một
`Channel<T>` thật có giới hạn, thêm pipeline policy kiểu `Polly` quanh
`Submit`, và viết các truy vấn dashboard SLO bạn sẽ chạy.

Trả bài với kỷ luật module 14: đo cấp phát và bộ đếm cho bản hiện thực của
bạn, và có thể nói *vì sao* với từng quyết định thiết kế — chứ không chỉ
"nó chạy".
"""


_m24_checkpoint = r"""## Checkpoint: production architecture

The last gate. Submit duplicates, exceed capacity, run everything: if all
three counters come out exactly as the tests demand, you have implemented the
core contracts of a production job platform — idempotency, backpressure, and
exactly-once execution — in a form you can defend line by line.

Common failures: accepting duplicates (the seen-set came after the capacity
check), counting rejections wrong (duplicates are rejected *twice* in the
schedule: once per extra delivery), or double-executing because `RunAll` did
not clear pending. Each maps to a real production bug with a real outage
story.
"""


_m24_checkpoint_vi = r"""## Checkpoint: kiến trúc production

Cổng cuối. Gửi bản trùng, vượt sức chứa, chạy tất cả: nếu cả ba bộ đếm ra
đúng như các bài kiểm tra đòi hỏi, bạn đã hiện thực các hợp đồng cốt lõi của
một nền tảng job production — idempotency, backpressure, và thực thi
exactly-once — dưới một hình dạng bạn có thể bảo vệ từng dòng một.

Các lỗi thường gặp: chấp nhận bản trùng (seen-set đứng sau kiểm tra sức chứa),
đếm sai số lần từ chối (mỗi bản trùng bị từ chối *một lần cho mỗi lần gửi
thừa*), hoặc thực thi hai lần vì `RunAll` không dọn pending. Mỗi lỗi ánh xạ
với một bug production thật với một câu chuyện sự cố thật.
"""
