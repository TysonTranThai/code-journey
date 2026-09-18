#!/usr/bin/env python3
"""Module 10: distributed-systems — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "distributed-systems"

# ── lesson 1 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "why-distributed-fails",
    "Why Distributed Systems Fail",
    "The network is not a function call: messages drop, arrive twice, arrive late, and arrive out of order — design for delivery, not for hope.",
    30,
    """
Everything you learned about calling functions breaks when the call crosses a
network. A remote call can:

- **succeed** — the work happened and you hear about it,
- **fail visibly** — the work didn't happen and you get an error,
- **fail invisibly** — the work happened but the *response was lost*, or the
  work didn't happen and the *request was lost*. From where you sit, these look
  **identical**: a timeout.

A timeout is not an answer; it is the *absence* of an answer. That single fact
drives most of this module.

## At-least-once delivery forces idempotency

If the network can lose your response, the only safe retry policy is
**at-least-once**: send again until you hear back. But retrying a non-idempotent
operation ("charge the card") means doing it twice. Conclusion:

> **at-least-once delivery + exactly-once effect = idempotency keys**

The receiver remembers processed keys and replays the recorded result. The
effect is exactly-once even though delivery is not.

## Retries need backoff and jitter

Retrying immediately into an overloaded system is a denial-of-service attack on
yourself. Exponential backoff (`1s, 2s, 4s, ...` capped) gives the system room
to recover. Pure backoff on many clients synchronizes into **thundering herds**
— everyone retries at the 8-second mark together. **Jitter** (randomizing each
delay within a band) desynchronizes them:

```python
delay = min(cap, base * 2 ** attempt)
sleep(random.uniform(0, delay))   # full jitter
```

## Timeouts, retries, and their budget

A total request budget (`5s`) must be divided among attempts. Three attempts
with a 5s timeout each is a 15s worst case — usually wrong. Give each attempt a
timeout that fits the budget, and track retries with a *deadline* (an absolute
time after which you give up), not just a count.

## Failure isolation: bulkheads and fallbacks

One slow dependency should not consume every worker thread of a healthy part of
the system (thread-pool exhaustion — the bulkhead pattern isolates pools per
dependency). And where a feature has a degraded mode, degrade: serve a cached
price rather than an error page. **Graceful degradation is a design decision
made before the incident, not during it.**
""",
    "Vì sao hệ phân tán hỏng",
    "Network không phải một lời gọi hàm: message có thể rơi, đến hai lần, đến muộn, và đến lệch thứ tự — hãy thiết kế cho việc chuyển giao, đừng hy vọng.",
    """
Mọi thứ bạn biết về việc gọi hàm đều gãy khi lời gọi đi qua mạng. Một lời gọi
từ xa có thể:

- **thành công** — công việc xảy ra và bạn nghe được tin,
- **thất bại hữu hình** — công việc không xảy ra và bạn nhận được lỗi,
- **thất bại vô hình** — công việc đã xảy ra nhưng *response bị mất*, hoặc công
  việc không xảy ra và *request bị mất*. Từ vị trí của bạn, hai điều này trông
  **giống hệt nhau**: một timeout.

Timeout không phải là một câu trả lời; nó là *sự vắng mặt* của câu trả lời.
Một sự thật duy nhất đó chi phối phần lớn module này.

## Chuyển giao at-least-once ép buộc tính idempotent

Nếu mạng có thể làm mất response của bạn, chính sách retry an toàn duy nhất
là **at-least-once**: gửi lại cho tới khi nghe được tin. Nhưng retry một thao
tác không idempotent ("trừ thẻ") nghĩa là trừ hai lần. Kết luận:

> **chuyển giao at-least-once + hiệu ứng exactly-once = idempotency key**

Bên nhận ghi nhớ các key đã xử lý và phát lại kết quả đã ghi. Hiệu ứng là
exactly-once dù việc chuyển giao không phải vậy.

## Retry cần backoff và jitter

Retry ngay lập tức vào một hệ thống đang quá tải là một cuộc tấn công
denial-of-service nhắm vào chính bạn. Exponential backoff (`1s, 2s, 4s, ...` có
trần) cho hệ thống thời gian hồi phục. Backoff thuần trên nhiều client khiến
chúng đồng bộ hóa thành **thundering herd** — tất cả cùng retry vào mốc 8 giây.
**Jitter** (ngẫu nhiên hóa mỗi độ trễ trong một dải) phá sự đồng bộ đó:

```python
delay = min(cap, base * 2 ** attempt)
sleep(random.uniform(0, delay))   # full jitter
```

## Timeout, retry, và ngân sách của chúng

Tổng ngân sách của một request (`5s`) phải được chia cho các lần thử. Ba lần
thử, mỗi lần timeout 5s, nghĩa là xấu nhất 15s — thường là sai. Cho mỗi lần thử
một timeout vừa với ngân sách, và theo dõi retry bằng một *deadline* (một mốc
thời gian tuyệt đối sau đó bạn từ bỏ), không chỉ bằng số đếm.

## Cô lập lỗi: bulkhead và fallback

Một dependency chậm không được phép ngốn hết mọi worker thread của phần lành
mạnh trong hệ thống (kiệt kết thread-pool — pattern bulkhead cô lập pool theo
từng dependency). Và nơi một tính năng có chế độ suy giảm, hãy suy giảm: phục
vụ giá cached thay vì trang lỗi. **Graceful degradation là quyết định thiết kế
đưa ra trước sự cố, không phải trong lúc sự cố.**
""",
)

# ── lesson 2 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "queues-and-workers",
    "Queues, Workers, and At-Least-Once",
    "A queue turns 'do it now, reliably' into 'do it eventually, visibly' — the worker contract, retries, dead letters, and exactly-once effects.",
    32,
    """
A queue decouples *accepting* work from *doing* work. The API enqueues a job
and returns 202; workers pull jobs and process them. The trade: you now run a
distributed system, so the queue's semantics matter more than its features.

## The delivery-semantics spectrum

- **At-most-once:** fire and forget. Losses are silent.
- **At-least-once:** redeliver until acknowledged. Nothing is silently lost —
  but duplicates arrive, so consumers **must be idempotent**. This is what most
  production queues offer.
- **Exactly-once:** the marketing dream; in practice it means at-least-once
  delivery plus idempotent processing achieved at the receiver.

## The worker contract

A worker processing a job must honor three rules:

1. **Acknowledge only after the effect is durable.** If you ack-then-crash, the
   job is lost; if you crash-then-ack, the job is redelivered (fine — see
   idempotency).
2. **Make the effect idempotent.** Key the work on a job ID: `(INSERT ... ON
   CONFLICT DO NOTHING)`-style, or a processed-keys table checked inside the
   same transaction as the effect.
3. **Bound the work.** A job that can loop forever will. Set internal timeouts
   and give up explicitly.

## Retry, backoff, and the dead-letter queue

Redelivery comes from visibility timeouts (the lease on an in-flight job
expires). After N failed attempts, the job moves to a **dead-letter queue**
(DLQ) — a humanInspectable pile of poison messages. Two properties make DLQs
useful: the *failure reason* travels with the message, and replaying from the
DLQ is a deliberate operation, not an accident.

## Heartbeats, leases, and poisoned workers

A crashed worker must not hold a job hostage. Leases expire; heartbeats renew
them. A job whose lease lapses becomes visible to other workers — which is
exactly why the processing must be idempotent: two workers may race on the same
job, and the second one's effect must be a no-op.

## Simulating all of this in-process

You don't need infrastructure to *learn* the semantics. An in-process queue
with explicit `deliver()` (a redelivery sweep) and a `_done` idempotency store
reproduces every behavior above deterministically — that's how the challenges
in this module work.
""",
    "Queue, worker, và at-least-once",
    "Một queue biến 'làm ngay, đáng tin' thành 'làm muộn hơn, nhìn thấy được' — hợp đồng của worker, retry, dead letter, và hiệu ứng exactly-once.",
    """
Một queue tách rời việc *nhận* công việc khỏi việc *làm* công việc. API đẩy một
job vào queue và trả 202; worker kéo job về xử lý. Cái giá: từ giờ bạn vận hành
một hệ phân tán, nên ngữ nghĩa của queue quan trọng hơn các tính năng của nó.

## Phổ ngữ nghĩa chuyển giao

- **At-most-once:** bắn và quên. Mất mát là vô hình.
- **At-least-once:** chuyển giao lại cho đến khi được xác nhận. Không có gì bị
  mất âm thầm — nhưng bản sao sẽ đến, nên consumer **bắt buộc idempotent**. Đây
  là điều hầu hết queue production cung cấp.
- **Exactly-once:** giấc mơ marketing; trên thực tế nó nghĩa là chuyển giao
  at-least-once cộng với xử lý idempotent đạt được ở phía người nhận.

## Hợp đồng của worker

Một worker xử lý một job phải tuân ba quy tắc:

1. **Chỉ acknowledge sau khi hiệu ứng đã bền vững.** Ack-xong-rồi-crash thì job
   bị mất; crash-xong-rồi-ack thì job được chuyển giao lại (ổn thôi — xem
   idempotency).
2. **Khiến hiệu ứng idempotent.** Khóa công việc theo job ID: kiểu
   `(INSERT ... ON CONFLICT DO NOTHING)`, hoặc bảng processed-keys được kiểm
   tra trong cùng transaction với hiệu ứng.
3. **Chặn giới hạn công việc.** Một job có thể lặp vô hạn thì sẽ lặp vô hạn. Đặt
   timeout bên trong và từ bỏ một cách tường minh.

## Retry, backoff, và dead-letter queue

Chuyển giao lại xuất phát từ visibility timeout (kỳ hạn thuê job đang xử lý
hết hạn). Sau N lần thử thất bại, job chuyển sang **dead-letter queue**
(DLQ) — một đống tin nhắn độc để con người kiểm tra. Hai đặc tính khiến DLQ hữu
ích: *lý do thất bại* đi cùng message, và phát lại từ DLQ là một thao tác chủ
động, không phải một tai nạn.

## Heartbeat, lease, và worker bị độc

Một worker crash không được phép giữ job làm con tin. Lease hết hạn; heartbeat
hồi renewed chúng. Job có lease hết hạn sẽ hiện thấy trở lại với các worker
khác — chính vì vậy mà xử lý phải idempotent: hai worker có thể cùng chạy trên
một job, và hiệu ứng của worker thứ hai phải là no-op.

## Mô phỏng tất cả trong tiến trình

Bạn không cần hạ tầng để *học* các ngữ nghĩa này. Một queue trong tiến trình
với `deliver()` tường minh (một lượt quét chuyển giao lại) và kho idempotency
`_done` tái hiện mọi hành vi trên một cách xác định — các thử thách trong
module này hoạt động đúng như vậy.
""",
)

# ── lesson 3 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "resilience-patterns",
    "Circuit Breakers and Consistency",
    "Stop calling dependencies that are already dying, and learn to reason about data that is temporarily wrong.",
    30,
    """
## The circuit breaker

Calling a dead service has a cost: each call burns a timeout, a thread, and
user patience. The **circuit breaker** (borrowed from electrical engineering)
tracks recent failures and trips OPEN after a threshold:

- **CLOSED** — normal; calls pass through; failures increment the count.
- **OPEN** — calls fail *instantly* (fast-fail) without touching the network;
  this also gives the dependency room to recover. After a cool-down, allow one
  probe through.
- **HALF-OPEN** — the probe call decides: success closes the circuit, failure
  re-opens it.

```python
class CircuitBreaker:
    def __init__(self, threshold=5, cooldown=30.0):
        ...
    def allow(self, now): ...      # may we call right now?
    def record(self, now, ok): ... # outcome of a real call
```

Notice both methods take `now` — deterministic, testable, injectable time.
That's a recurring theme: every resilience mechanism is a state machine whose
transitions depend on time, so make time a parameter.

## Consistency: the cost of copying

Once data lives on two machines, updates take time to propagate. During that
window reads disagree: **eventual consistency**. Three everyday consequences:

1. **Read-your-writes:** after a user updates their profile, the very next read
   should reflect it — route that read to the primary, or version reads.
2. **Stale reads are a product decision:** a slightly-old follower count is
   fine; a slightly-old account balance is not. Classify data by staleness
   tolerance.
3. **Optimistic concurrency:** instead of locking, write with a version: `UPDATE
   ... WHERE version = :seen` — 0 rows updated means someone raced you; re-read
   and retry. Cheap, and correct under contention.

## Distributed locks: necessary, and dangerous

A lock service can grant the same lock twice (GC pause, network partition). So:
never let correctness depend solely on a distributed lock — pair it with an
idempotency token or fencing token (a number that increases with each grant;
older holders get rejected). The lock is an optimization; the fencing is the
correctness.

## Health checks and graceful shutdown (service hygiene)

- `/readyz` reflecting real dependency state lets the load balancer drain a
  sick instance instead of feeding it traffic.
- On SIGTERM: stop accepting new work, finish (or re-queue) in-flight jobs,
  *then* exit. Kill-9 mid-job is only safe when jobs are idempotent — which is
  the design you already have.
""",
    "Circuit breaker và tính nhất quán",
    "Ngừng gọi những dependency đang chết dần, và học cách suy luận về dữ liệu tạm thời sai.",
    """
## Circuit breaker

Gọi một dịch vụ đã chết có cái giá: mỗi lời gọi đốt một timeout, một thread,
và sự kiên nhẫn của người dùng. **Circuit breaker** (mượn từ kỹ thuật điện)
theo dõi các lỗi gần đây và nhảy sang OPEN sau một ngưỡng:

- **CLOSED** — bình thường; lời gọi đi qua; lỗi tăng bộ đếm.
- **OPEN** — lời gọi fail *ngay lập tức* (fast-fail) không đụng vào mạng; điều
  này cũng cho dependency thời gian hồi phục. Sau một giai đoạn nguội, cho một
  lời gọi thăm dò đi qua.
- **HALF-OPEN** — lời gọi thăm dò quyết định: thành công đóng mạch lại, thất
  bại mở lại mạch.

```python
class CircuitBreaker:
    def __init__(self, threshold=5, cooldown=30.0):
        ...
    def allow(self, now): ...      # chúng ta có được gọi ngay lúc này không?
    def record(self, now, ok): ... # kết quả của một lời gọi thật
```

Chú ý cả hai method đều nhận `now` — thời gian xác định được, test được, tiêm
được. Đó là chủ đề lặp lại: mọi cơ chế resilience là một máy trạng thái mà các
chuyển tiếp phụ thuộc vào thời gian, vậy hãy biến thời gian thành tham số.

## Nhất quán: cái giá của việc sao chép

Khi dữ liệu nằm trên hai máy, việc lan truyền bản cập nhật cần thời gian. Trong
cửa sổ đó, các lần đọc không đồng tình: **eventual consistency**. Ba hệ quả
thường ngày:

1. **Read-your-writes:** sau khi người dùng cập nhật hồ sơ, lần đọc ngay sau đó
   phải phản ánh điều đó — route lần đọc đó tới primary, hoặc đánh phiên bản
   cho lần đọc.
2. **Đọc cũ là một quyết định sản phẩm:** số người theo dõi hơi cũ thì được;
   số dư tài khoản hơi cũ thì không. Phân loại dữ liệu theo mức chịu được độ
   cũ.
3. **Optimistic concurrency:** thay vì khóa, hãy ghi kèm phiên bản: `UPDATE ...
   WHERE version = :seen` — 0 dòng được cập nhật nghĩa là có người vừa tranh
   chấp với bạn; đọc lại và thử lại. Rẻ, và đúng dưới tranh chấp.

## Distributed lock: cần thiết, và nguy hiểm

Một dịch vụ khóa có thể cấp cùng một khóa hai lần (GC pause, phân vùng mạng).
Vì vậy: đừng bao giờ để tính đúng đắn phụ thuộc chỉ riêng vào distributed lock
— ghép nó với idempotency token hoặc fencing token (một số tăng dần theo mỗi
lần cấp; holder cũ hơn sẽ bị từ chối). Khóa là một tối ưu hóa; fencing mới là
tính đúng đắn.

## Health check và graceful shutdown (vệ sinh dịch vụ)

- `/readyz` phản ánh trạng thái dependency thật cho phép load balancer rút một
  instance ốm thay vì tiếp tục cho nó ăn traffic.
- Nhận SIGTERM: ngừng nhận công việc mới, hoàn tất (hoặc trả job về queue) các
  job đang chạy, *rồi* thoát. Kill-9 giữa chừng job chỉ an toàn khi job là
  idempotent — vốn là thiết kế bạn đã có sẵn.
""",
)

# ── practice 1: retries ──────────────────────────────────────────────────────
BACKOFF_REF = (
    "import random as _random\n"
    "\n"
    "\n"
    "class RetryPolicy:\n"
    "    def __init__(self, max_attempts=5, base=0.5, cap=8.0):\n"
    "        self.max_attempts = max_attempts\n"
    "        self.base = base\n"
    "        self.cap = cap\n"
    "\n"
    "    def schedule(self, attempt, rnd=None):\n"
    "        '''Delay before retry `attempt` (0-based). Pure backoff ceiling + full jitter.'''\n"
    "        rnd = rnd or _random.random\n"
    "        ceiling = min(self.cap, self.base * (2 ** attempt))\n"
    "        return rnd() * ceiling\n"
    "\n"
    "    def run(self, fn, rnd=None, clock=None):\n"
    "        '''Call fn() until success (truthy) or attempts exhausted.\n"
    "        Returns (result, attempts_used). No real sleeping: the schedule is computed,\n"
    "        not executed — keeps tests deterministic.'''\n"
    "        rnd = rnd or _random.random\n"
    "        for attempt in range(self.max_attempts):\n"
    "            result = fn(attempt)\n"
    "            if result:\n"
    "                return result, attempt + 1\n"
    "        return None, self.max_attempts\n"
)
BACKOFF_WRONG = (
    "import random as _random\n"
    "\n"
    "\n"
    "class RetryPolicy:\n"
    "    def __init__(self, max_attempts=5, base=0.5, cap=8.0):\n"
    "        self.max_attempts = max_attempts\n"
    "        self.base = base\n"
    "        self.cap = cap\n"
    "\n"
    "    def schedule(self, attempt, rnd=None):\n"
    "        rnd = rnd or _random.random\n"
    "        ceiling = min(self.cap, self.base * (2 ** attempt))\n"
    "        return rnd() * ceiling\n"
    "\n"
    "    def run(self, fn, rnd=None, clock=None):\n"
    "        # WRONG: swallows the final failure and pretends one attempt was enough\n"
    "        for attempt in range(1):\n"
    "            result = fn(attempt)\n"
    "            if result:\n"
    "                return result, attempt + 1\n"
    "        return 'gave up', 1\n"
)

QUEUE_REF = (
    "class InProcessQueue:\n"
    "    '''At-least-once queue with an idempotent worker. Deterministic: redelivery\n"
    "    happens only when deliver() is called explicitly.'''\n"
    "\n"
    "    def __init__(self):\n"
    "        self._pending = []      # [job_id, payload, attempts]\n"
    "        self._inflight = []\n"
    "        self._done = {}         # job_id -> result (idempotency store)\n"
    "        self._dead = []         # [job_id, payload, attempts]\n"
    "\n"
    "    def enqueue(self, job_id, payload):\n"
    "        self._pending.append([job_id, payload, 0])\n"
    "\n"
    "    def deliver(self):\n"
    "        '''Move pending (and expired inflight) jobs to the delivery list.'''\n"
    "        batch = self._pending + self._inflight\n"
    "        self._pending, self._inflight = [], []\n"
    "        return [list(j) for j in batch]\n"
    "\n"
    "    def ack(self, job_id, result):\n"
    "        self._done[job_id] = result\n"
    "\n"
    "    def fail(self, job_id, max_attempts=3):\n"
    "        for j in self._inflight:\n"
    "            if j[0] == job_id:\n"
    "                j[2] += 1\n"
    "                if j[2] >= max_attempts:\n"
    "                    self._dead.append(j)\n"
    "                else:\n"
    "                    self._pending.append(j)\n"
    "                self._inflight.remove(j)\n"
    "                return\n"
    "\n"
    "    @property\n"
    "    def done(self):\n"
    "        return dict(self._done)\n"
    "\n"
    "    @property\n"
    "    def dead(self):\n"
    "        return list(self._dead)\n"
    "\n"
    "\n"
    "def process(queue, jobs, max_attempts=3):\n"
    "    '''Deliver every batch until the queue is drained; process idempotently.\n"
    "    Returns (done, dead). A job's effect runs at most once even if delivered twice.'''\n"
    "    effects = []\n"
    "    dead = []\n"
    "    while True:\n"
    "        batch = queue.deliver()\n"
    "        if not batch:\n"
    "            break\n"
    "        for job_id, payload, attempts in batch:\n"
    "            if job_id in queue._done:\n"
    "                continue                      # idempotent: already effected\n"
    "            if payload == 'poison':\n"
    "                queue.fail(job_id, max_attempts)\n"
    "                if job_id in [d[0] for d in queue.dead] and job_id not in [d[0] for d in dead]:\n"
    "                    dead.append([job_id, payload, attempts + 1])\n"
    "                continue\n"
    "            effects.append(job_id)\n"
    "            queue.ack(job_id, f\"done:{job_id}\")\n"
    "    return {jid: f\"done:{jid}\" for jid in effects}, dead\n"
)
QUEUE_WRONG = (
    "class InProcessQueue:\n"
    "    def __init__(self):\n"
    "        self._pending = []\n"
    "        self._inflight = []\n"
    "        self._done = {}\n"
    "        self._dead = []\n"
    "\n"
    "    def enqueue(self, job_id, payload):\n"
    "        self._pending.append([job_id, payload, 0])\n"
    "\n"
    "    def deliver(self):\n"
    "        batch = self._pending + self._inflight\n"
    "        self._pending, self._inflight = [], []\n"
    "        return [list(j) for j in batch]\n"
    "\n"
    "    def ack(self, job_id, result):\n"
    "        self._done[job_id] = result\n"
    "\n"
    "    def fail(self, job_id, max_attempts=3):\n"
    "        for j in self._inflight:\n"
    "            if j[0] == job_id:\n"
    "                self._dead.append(j)  # WRONG: straight to DLQ, no retry budget\n"
    "                self._inflight.remove(j)\n"
    "                return\n"
    "\n"
    "    @property\n"
    "    def done(self):\n"
    "        return dict(self._done)\n"
    "\n"
    "    @property\n"
    "    def dead(self):\n"
    "        return list(self._dead)\n"
    "\n"
    "\n"
    "def process(queue, jobs, max_attempts=3):\n"
    "    effects = []\n"
    "    dead = []\n"
    "    while True:\n"
    "        batch = queue.deliver()\n"
    "        if not batch:\n"
    "            break\n"
    "        for job_id, payload, attempts in batch:\n"
    "            if job_id in queue._done:\n"
    "                continue\n"
    "            if payload == 'poison':\n"
    "                queue.fail(job_id, max_attempts)\n"
    "                if job_id in [d[0] for d in queue.dead] and job_id not in [d[0] for d in dead]:\n"
    "                    dead.append([job_id, payload, attempts + 1])\n"
    "                continue\n"
    "            effects.append(job_id)\n"
    "            queue.ack(job_id, f\"done:{job_id}\")\n"
    "    return {jid: f\"done:{jid}\" for jid in effects}, dead\n"
)

write_practice(
    MOD, "pa-p10-retry-practice",
    "Retry & Redelivery Drills",
    "Backoff with jitter computed, not slept; and an at-least-once queue whose duplicate deliveries are harmless.",
    "Bài tập retry và chuyển giao lại",
    "Backoff với jitter được tính chứ không sleep; và một queue at-least-once mà các bản chuyển giao trùng lặp là vô hại.",
    "why-distributed-fails", 26, "advanced",
    [
        challenge(
            "pa-dist-backoff",
            "Backoff schedule, computed not slept",
            "Implement `RetryPolicy(max_attempts=5, base=0.5, cap=8.0)` with two methods:\n\n- `schedule(attempt, rnd=None)` — the delay before retry number `attempt` (0-based): the exponential ceiling `min(cap, base * 2**attempt)` multiplied by a jitter factor from `rnd` (a zero-arg callable returning floats in [0, 1); default `random.random`) — i.e. full jitter: `rnd() * ceiling`\n- `run(fn, rnd=None, clock=None)` — call `fn(attempt)` up to `max_attempts` times; stop at the first truthy result and return `(result, attempts_used)`; if all attempts fail return `(None, max_attempts)`\n\nDeterministic requirement: `run` computes the schedule but must not actually sleep — tests pass their own `rnd`.",
            "import random\n\n\nclass RetryPolicy:\n    def __init__(self, max_attempts=5, base=0.5, cap=8.0):\n        ...\n\n    def schedule(self, attempt, rnd=None):\n        ...\n\n    def run(self, fn, rnd=None, clock=None):\n        ...",
            [
                ("exponential ceiling with full jitter",
                 "import random\nrnd = random.Random(42)\np = RetryPolicy(base=0.5, cap=8.0)\nfor attempt, ceiling in [(0, 0.5), (1, 1.0), (2, 2.0), (3, 4.0), (4, 8.0), (5, 8.0), (10, 8.0)]:\n    vals = [p.schedule(attempt, rnd) for _ in range(50)]\n    assert all(0 <= v <= ceiling + 1e-9 for v in vals), (attempt, max(vals))\nprint('ok')",
                 "Ceiling doubles and caps; jitter multiplies it by rnd() in [0, 1)."),
                ("retry loop honors attempts and truthiness",
                 "calls = []\ndef flaky(attempt):\n    calls.append(attempt)\n    return attempt >= 2\nresult, used = RetryPolicy(max_attempts=5).run(flaky)\nassert result is True and used == 3 and calls == [0, 1, 2]\ncalls.clear()\ndef always_fails(attempt):\n    calls.append(attempt)\n    return False\nres, used = RetryPolicy(max_attempts=4).run(always_fails)\nassert res is None and used == 4 and calls == [0, 1, 2, 3]\nprint('ok')",
                 "Stop at first truthy; exhaust otherwise."),
            ],
            level="guided",
        ),
        challenge(
            "pa-dist-queue",
            "The idempotent at-least-once queue",
            "Implement two pieces:\n\n`InProcessQueue` — an at-least-once queue:\n- `enqueue(job_id, payload)`; `deliver()` moves all pending jobs (plus anything previously delivered but not acked — simulate lease expiry by re-delivering inflight jobs on the next deliver) and returns the batch as a list of `[job_id, payload, attempts]`\n- `ack(job_id, result)` records completion; `fail(job_id, max_attempts=3)` increments the attempt counter and re-queues the job, or moves it to the dead-letter list once `attempts >= max_attempts`\n- `done` (dict of results) and `dead` (list of [job_id, payload, attempts]) expose state\n\n`process(queue, jobs, max_attempts=3)` — a worker loop:\n- repeatedly `deliver()` until the queue stays empty\n- for each job: skip jobs already in `done` (idempotency!), process `'poison'` payloads by calling `queue.fail(...)`, otherwise record the effect and `ack(job_id, 'done:' + job_id)`\n- returns `(done_dict, dead_list)`\n\nThe discriminating scenario: a job delivered twice must produce exactly one effect; a poison job must be retried until `max_attempts` then land in `dead`.",
            "class InProcessQueue:\n    def __init__(self):\n        ...\n\n    def enqueue(self, job_id, payload):\n        ...\n\n    def deliver(self):\n        ...\n\n    def ack(self, job_id, result):\n        ...\n\n    def fail(self, job_id, max_attempts=3):\n        ...\n\n\n# done/dead as properties\n\n\ndef process(queue, jobs, max_attempts=3):\n    ...",
            [
                ("duplicate delivery, single effect",
                 "q = InProcessQueue()\nq.enqueue('j1', 'work')\nbatch = q.deliver()\nq.ack('j1', 'done:j1')\nq.enqueue('j2', 'work')   # new work forces another deliver sweep\nq.enqueue('j1', 'work')   # duplicate redelivery of an already-done job\nprocessed, dead = process(q, ['j1', 'j2'])\nassert processed == {'j1': 'done:j1', 'j2': 'done:j2'} and dead == []\nprint('ok')",
                 "Check the done-store before effecting anything."),
                ("poison retried to the DLQ, not forever",
                 "q = InProcessQueue()\nq.enqueue('p1', 'poison')\nprocessed, dead = process(q, ['p1'], max_attempts=3)\nassert processed == {} and len(dead) == 1 and dead[0][0] == 'p1' and dead[0][2] == 3\nprint('ok')",
                 "fail() increments attempts; at max_attempts the job stops cycling."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-dist-backoff": vi_challenge(
            "Lịch backoff được tính chứ không sleep",
            "Cài `RetryPolicy(max_attempts=5, base=0.5, cap=8.0)` với hai method:\n\n- `schedule(attempt, rnd=None)` — độ trễ trước lần retry thứ `attempt` (tính từ 0): trần theo hàm mũ `min(cap, base * 2**attempt)` nhân với hệ số jitter từ `rnd` (callable không tham số trả float trong [0, 1); mặc định `random.random`) — tức full jitter: `rnd() * ceiling`\n- `run(fn, rnd=None, clock=None)` — gọi `fn(attempt)` tối đa `max_attempts` lần; dừng ở kết quả truthy đầu tiên và trả `(result, attempts_used)`; nếu mọi lần thử đều fail trả `(None, max_attempts)`\n\nYêu cầu xác định: `run` tính lịch nhưng không được sleep thật — test tự truyền `rnd` của họ.",
            [("Trần mũ với full jitter", "Trần nhân đôi rồi chặn; jitter nhân nó với rnd() trong [0, 1)."),
             ("Vòng retry tôn trọng số lần thử", "Dừng ở truthy đầu tiên; dùng hết nếu không bao giờ thành công.")],
        ),
        "pa-dist-queue": vi_challenge(
            "Queue at-least-once idempotent",
            "Cài hai phần:\n\n`InProcessQueue` — một queue at-least-once:\n- `enqueue(job_id, payload)`; `deliver()` chuyển mọi job đang chờ (cộng cả những job đã deliver mà chưa ack — mô phỏng lease hết hạn bằng cách deliver lại job inflight ở lần deliver kế tiếp) và trả batch dưới dạng list `[job_id, payload, attempts]`\n- `ack(job_id, result)` ghi hoàn thành; `fail(job_id, max_attempts=3)` tăng bộ đếm lần thử và trả job về queue, hoặc chuyển nó vào dead-letter khi `attempts >= max_attempts`\n- `done` (dict kết quả) và `dead` (list [job_id, payload, attempts]) phơi trạng thái\n\n`process(queue, jobs, max_attempts=3)` — vòng lặp worker:\n- gọi `deliver()` liên tục cho tới khi queue giữ nguyên rỗng\n- với mỗi job: bỏ qua job đã có trong `done` (idempotency!), xử lý payload `'poison'` bằng cách gọi `queue.fail(...)`, còn lại ghi hiệu ứng và `ack(job_id, 'done:' + job_id)`\n- trả `(done_dict, dead_list)`\n\nKịch bản phân biệt: một job được deliver hai lần phải sinh đúng một hiệu ứng; job poison phải được retry tới `max_attempts` rồi nằm trong `dead`.",
            [("Chuyển giao trùng lặp, hiệu ứng đơn lẻ", "Kiểm tra kho done trước khi tạo hiệu ứng."),
             ("Poison được retry tới DLQ, không mãi mãi", "fail() tăng số lần thử; đến max_attempts thì job ngừng quay vòng.")],
        ),
    },
    solutions=[("pa-dist-backoff", BACKOFF_REF, BACKOFF_WRONG),
               ("pa-dist-queue", QUEUE_REF, QUEUE_WRONG)],
)

# ── practice 2: circuit breaker ──────────────────────────────────────────────
BREAKER_REF = (
    "class CircuitBreaker:\n"
    "    def __init__(self, threshold=3, cooldown=30.0):\n"
    "        self.threshold = threshold\n"
    "        self.cooldown = cooldown\n"
    "        self.state = 'closed'\n"
    "        self._failures = 0\n"
    "        self._opened_at = None\n"
    "\n"
    "    def allow(self, now):\n"
    "        if self.state == 'open':\n"
    "            if now - self._opened_at >= self.cooldown:\n"
    "                self.state = 'half-open'\n"
    "                return True            # single probe\n"
    "            return False\n"
    "        return True\n"
    "\n"
    "    def record(self, now, ok):\n"
    "        if ok:\n"
    "            self._failures = 0\n"
    "            self.state = 'closed'\n"
    "            self._opened_at = None\n"
    "            return\n"
    "        if self.state == 'half-open':\n"
    "            self.state = 'open'\n"
    "            self._opened_at = now\n"
    "            return\n"
    "        self._failures += 1\n"
    "        if self._failures >= self.threshold:\n"
    "            self.state = 'open'\n"
    "            self._opened_at = now\n"
)
BREAKER_WRONG = (
    "class CircuitBreaker:\n"
    "    def __init__(self, threshold=3, cooldown=30.0):\n"
    "        self.threshold = threshold\n"
    "        self.cooldown = cooldown\n"
    "        self.state = 'closed'\n"
    "        self._failures = 0\n"
    "        self._opened_at = None\n"
    "\n"
    "    def allow(self, now):\n"
    "        return True  # WRONG: never trips open — calls the dead dependency forever\n"
    "\n"
    "    def record(self, now, ok):\n"
    "        if ok:\n"
    "            self._failures = 0\n"
    "            self.state = 'closed'\n"
    "            self._opened_at = None\n"
    "            return\n"
    "        self._failures += 1\n"
    "        if self._failures >= self.threshold:\n"
    "            self.state = 'open'\n"
    "            self._opened_at = now\n"
)

write_practice(
    MOD, "pa-p10-breaker-practice",
    "Trip the Breaker",
    "A circuit breaker as a deterministic state machine: CLOSED, OPEN at threshold, HALF-OPEN probe after cooldown.",
    "Chặn mạch",
    "Một circuit breaker như một máy trạng thái xác định: CLOSED, OPEN khi đạt ngưỡng, HALF-OPEN thăm dò sau thời gian nguội.",
    "resilience-patterns", 20, "advanced",
    [
        challenge(
            "pa-dist-breaker",
            "CLOSED → OPEN → HALF-OPEN → CLOSED",
            "Implement `CircuitBreaker(threshold=3, cooldown=30.0)` with `allow(now)` and `record(now, ok)`:\n\n- starts CLOSED; `allow` returns True\n- each `record(now, False)` in CLOSED increments failures; reaching `threshold` trips state to OPEN and stamps `_opened_at = now`\n- while OPEN, `allow` returns False until `now - _opened_at >= cooldown`, then switches to HALF-OPEN and returns True exactly once (the probe)\n- `record(now, True)` in any state: resets failures and closes the circuit\n- `record(now, False)` in HALF-OPEN: re-opens (stamp `_opened_at = now`)\n\n`now` is always a float parameter — no time functions inside.",
            "class CircuitBreaker:\n    def __init__(self, threshold=3, cooldown=30.0):\n        ...\n\n    def allow(self, now):\n        ...\n\n    def record(self, now, ok):\n        ...",
            [
                ("trips at threshold, blocks during cooldown",
                 "b = CircuitBreaker(threshold=3, cooldown=30.0)\nfor t in (1.0, 2.0, 3.0):\n    assert b.allow(t) is True\n    b.record(t, False)\nassert b.state == 'open'\nassert b.allow(10.0) is False\nassert b.allow(32.9) is False   # 32.9 - 3.0 < 30\nassert b.allow(33.0) is True    # probe\nassert b.state == 'half-open'\nb.record(33.0, False)           # probe failed -> re-open\nassert b.state == 'open' and b.allow(40.0) is False\nprint('ok')",
                 "The breaker is a little clock-driven state machine."),
                ("success closes and resets",
                 "b = CircuitBreaker(threshold=2, cooldown=10.0)\nb.record(0, False)\nb.record(0, False)\nassert b.state == 'open'\nassert b.allow(10.0) is True\nb.record(10.0, True)\nassert b.state == 'closed' and b.allow(11.0) is True\nb.record(11.0, False)\nassert b.state == 'closed'  # failures reset: one failure alone doesn't trip\nprint('ok')",
                 "A success clears the failure count, not just the state."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-dist-breaker": vi_challenge(
            "CLOSED → OPEN → HALF-OPEN → CLOSED",
            "Cài `CircuitBreaker(threshold=3, cooldown=30.0)` với `allow(now)` và `record(now, ok)`:\n\n- khởi tạo CLOSED; `allow` trả True\n- mỗi `record(now, False)` khi CLOSED tăng số lỗi; đạt `threshold` thì chuyển sang OPEN và ghi `_opened_at = now`\n- khi OPEN, `allow` trả False cho tới `now - _opened_at >= cooldown`, rồi chuyển sang HALF-OPEN và trả True đúng một lần (lời thăm dò)\n- `record(now, True)` ở bất kỳ trạng thái nào: reset số lỗi và đóng mạch\n- `record(now, False)` khi HALF-OPEN: mở lại mạch (ghi `_opened_at = now`)\n\n`now` luôn là tham số float — không dùng hàm thời gian bên trong.",
            [("Chạm ngưỡng là bật mạch, chặn trong thời gian nguội", "Circuit breaker là một máy trạng thái nhỏ dẫn động bằng đồng hồ."),
             ("Thành công đóng mạch và reset", "Một lần thành công xóa bộ đếm lỗi, không chỉ đổi trạng thái.")],
        ),
    },
    solutions=[("pa-dist-breaker", BREAKER_REF, BREAKER_WRONG)],
)

# ── practice 3: distributed project ──────────────────────────────────────────
WORKER_REF = (
    "import time as _time\n"
    "\n"
    "\n"
    "class FlakyQueue:\n"
    "    '''Deterministic unreliable dependency: fails the first `fail_times`\n"
    "    calls, then succeeds.'''\n"
    "\n"
    "    def __init__(self, fail_times=2):\n"
    "        self.fail_times = fail_times\n"
    "        self.calls = 0\n"
    "\n"
    "    def put(self, payload):\n"
    "        self.calls += 1\n"
    "        if self.calls <= self.fail_times:\n"
    "            raise ConnectionError('queue unreachable')\n"
    "\n"
    "\n"
    "def enqueue_with_retry(queue, payload, max_attempts=5, base=0.01, cap=0.1):\n"
    "    '''Try queue.put(payload) up to max_attempts with exponential backoff ceilings\n"
    "    (no sleeping). Returns attempts_used (>= 1) on success; raises RuntimeError\n"
    "    mentioning 'exhausted' if all attempts fail.'''\n"
    "    last = None\n"
    "    for attempt in range(max_attempts):\n"
    "        try:\n"
    "            queue.put(payload)\n"
    "            return attempt + 1\n"
    "        except ConnectionError as err:\n"
    "            last = err\n"
    "            _ = min(cap, base * (2 ** attempt))  # schedule computed; not slept\n"
    "    raise RuntimeError(f'retries exhausted after {max_attempts} attempts: {last}')\n"
)
WORKER_WRONG = (
    "import time as _time\n"
    "\n"
    "\n"
    "class FlakyQueue:\n"
    "    def __init__(self, fail_times=2):\n"
    "        self.fail_times = fail_times\n"
    "        self.calls = 0\n"
    "\n"
    "    def put(self, payload):\n"
    "        self.calls += 1\n"
    "        if self.calls <= self.fail_times:\n"
    "            raise ConnectionError('queue unreachable')\n"
    "\n"
    "\n"
    "def enqueue_with_retry(queue, payload, max_attempts=5, base=0.01, cap=0.1):\n"
    "    # WRONG: retries once, then gives up by swallowing the error\n"
    "    for attempt in range(2):\n"
    "        try:\n"
    "            queue.put(payload)\n"
    "            return attempt + 1\n"
    "        except ConnectionError:\n"
    "            pass\n"
    "    return 2\n"
)

write_practice(
    MOD, "pa-p10-distributed-project",
    "Distributed Job System Mini-Project",
    "Push a job through an unreliable network to an unreliable queue, with retry budgets and honest failure.",
    "Dự án mini hệ job phân tán",
    "Đẩy một job qua mạng không đáng tin tới một queue không đáng tin, với ngân sách retry và sự thất bại trung thực.",
    "resilience-patterns", 30, "advanced",
    [
        challenge(
            "pa-dist-reliable-enqueue",
            "Reliable enqueue over an unreliable network",
            "Implement `enqueue_with_retry(queue, payload, max_attempts=5, base=0.01, cap=0.1)`:\n\n- call `queue.put(payload)`; `ConnectionError` means the attempt failed\n- between attempts, the backoff ceiling `min(cap, base * 2**attempt)` must be computed (you may sleep or not — tests measure calls, not time)\n- succeed → return `attempts_used` (1-based)\n- exhaust all attempts → raise `RuntimeError` whose message contains 'exhausted'\n\n`queue` may be any object with `.put` — the test uses one that fails a fixed number of times then succeeds.",
            "def enqueue_with_retry(queue, payload, max_attempts=5, base=0.01, cap=0.1):\n    ...",
            [
                ("recovers within the budget",
                 "class Flaky:\n    def __init__(self, fails):\n        self.fails = fails\n        self.calls = 0\n    def put(self, p):\n        self.calls += 1\n        if self.calls <= self.fails:\n            raise ConnectionError('down')\n\nq = Flaky(3)\nattempts = enqueue_with_retry(q, {'job': 1})\nassert attempts == 4 and q.calls == 4\nprint('ok')",
                 "Each ConnectionError consumes one attempt; the 4th succeeds."),
                ("honest exhaustion",
                 "class Always:\n    def __init__(self):\n        self.calls = 0\n    def put(self, p):\n        self.calls += 1\n        raise ConnectionError('down')\n\nq = Always()\ntry:\n    enqueue_with_retry(q, 'x', max_attempts=3)\nexcept RuntimeError as e:\n    assert 'exhausted' in str(e) and q.calls == 3\nelse:\n    raise AssertionError('must raise after exhausting')\nprint('ok')",
                 "Give up loudly after the budget; no fake success."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-dist-reliable-enqueue": vi_challenge(
            "Enqueue đáng tin trên mạng không đáng tin",
            "Cài `enqueue_with_retry(queue, payload, max_attempts=5, base=0.01, cap=0.1)`:\n\n- gọi `queue.put(payload)`; `ConnectionError` nghĩa là lần thử thất bại\n- giữa các lần thử, trần backoff `min(cap, base * 2**attempt)` phải được tính (bạn có thể sleep hay không — test đo số lần gọi, không đo thời gian)\n- thành công → trả `attempts_used` (bắt đầu từ 1)\n- dùng hết các lần thử → raise `RuntimeError` với message chứa 'exhausted'\n\n`queue` có thể là bất kỳ đối tượng nào có `.put` — test dùng một cái fail đúng số lần cố định rồi thành công.",
            [("Hồi phục trong ngân sách", "Mỗi ConnectionError tốn một lần thử; lần thứ 4 thành công."),
             ("Dùng hết một cách trung thực", "Từ bỏ ầm ĩ sau khi hết ngân sách; không có thành công giả.")],
        ),
    },
    solutions=[("pa-dist-reliable-enqueue", WORKER_REF, WORKER_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
write_checkpoint(
    MOD, "pa-checkpoint-distributed",
    "Checkpoint: Distributed Systems",
    "Prove you can reason about redelivery, idempotency, and breakers under an injected clock.",
    25,
    """
**The exam question:** a job was delivered, the worker crashed before
acknowledging, and the queue delivered it again. Walk through what your system
does — in code.

The checkpoint challenge: an idempotency-gated processor over an
at-least-once stream. Jobs arrive twice by design; effects must happen once;
`'poison'` jobs must exhaust their retry budget into the dead-letter list; and
a failing dependency is recorded, never propagated.
""",
    "Checkpoint: Hệ phân tán",
    "Chứng minh bạn suy luận được về chuyển giao lại, idempotency, và circuit breaker dưới một đồng hồ được tiêm vào.",
    """
**Câu hỏi thi:** một job đã được chuyển giao, worker crash trước khi
acknowledge, và queue chuyển giao nó lần nữa. Hãy đi qua hệ thống của bạn sẽ
làm gì — bằng code.

Thử thách checkpoint: một bộ xử lý có cổng idempotency trên một dòng
at-least-once. Job đến hai lần một cách chủ đích; hiệu ứng phải xảy ra một
lần; job `'poison'` phải dùng hết ngân sách retry rồi nằm vào dead-letter; và
một dependency hỏng được ghi nhận, không bao giờ được truyền ra ngoài.
""",
    challenge(
        "pa-dist-idempotent-processor",
        "Exactly-once effects on at-least-once delivery",
        "Implement `process_stream(jobs, max_attempts=3)` where `jobs` is a list of `[job_id, payload, attempts]` batches over time (concatenate them in order):\n\n- maintain `done` (dict job_id → 'done:' + job_id) and `dead` (list of [job_id, payload, attempts])\n- a job already in `done` is skipped — its effect happened once, redelivery is a no-op\n- a `'poison'` payload increments its attempt counter each time it is seen; when attempts reach `max_attempts` it moves to `dead` (as [job_id, payload, max_attempts]) and is never processed again\n- any other payload is effected exactly once (added to `done`) the first time it is seen\n- return `{'done': {...}, 'dead': [...]}`\n\nExample: `[[('j1','work',0)], [('j1','work',0), ('p','poison',0)], [('p','poison',1)]]` with max_attempts=3 → j1 done once, p dead at attempts 3.",
        "def process_stream(jobs, max_attempts=3):\n    ...",
        [
            ("redelivery is a no-op, poison dies at budget",
             "batches = [[['j1', 'work', 0]], [['j1', 'work', 0], ['p', 'poison', 0]], [['p', 'poison', 1]]]\nr = process_stream(batches, max_attempts=3)\nassert r['done'] == {'j1': 'done:j1'}\nassert r['dead'] == [['p', 'poison', 3]]\nprint('ok')",
             "The done-gate short-circuits duplicates; attempts accumulate across batches."),
        ],
        level="build",
    ),
    vi_challenge(
        "Hiệu ứng exactly-once trên chuyển giao at-least-once",
        "Cài `process_stream(jobs, max_attempts=3)` với `jobs` là danh sách các batch `[job_id, payload, attempts]` theo thời gian (nối chúng lại theo thứ tự):\n\n- giữ `done` (dict job_id → 'done:' + job_id) và `dead` (list [job_id, payload, attempts])\n- job đã có trong `done` bị bỏ qua — hiệu ứng của nó đã xảy ra một lần, chuyển giao lại là no-op\n- payload `'poison'` tăng bộ đếm lần thử mỗi khi xuất hiện; khi attempts đạt `max_attempts` nó chuyển sang `dead` (dạng [job_id, payload, max_attempts]) và không bao giờ được xử lý nữa\n- payload khác được tạo hiệu ứng đúng một lần (thêm vào `done`) ở lần thấy đầu tiên\n- trả `{'done': {...}, 'dead': [...]}`\n\nVí dụ: `[[('j1','work',0)], [('j1','work',0), ('p','poison',0)], [('p','poison',1)]]` với max_attempts=3 → j1 xong một lần, p chết ở attempts 3.",
        [("Chuyển giao lại là no-op, poison chết đúng ngân sách", "Cổng done chặn đứng bản trùng lặp; số lần thử cộng dồn qua các batch.")],
    ),
    solution=(
        "def process_stream(jobs, max_attempts=3):\n"
        "    done = {}\n"
        "    dead = {}\n"
        "    for batch in jobs:\n"
        "        for job_id, payload, attempts in batch:\n"
        "            if job_id in done or job_id in dead:\n"
        "                continue\n"
        "            if payload == 'poison':\n"
        "                attempts += 1\n"
        "                if attempts >= max_attempts:\n"
        "                    dead[job_id] = [job_id, payload, max_attempts]\n"
        "                continue\n"
        "            done[job_id] = 'done:' + job_id\n"
        "    return {'done': done, 'dead': list(dead.values())}\n"
    ),
    wrong=(
        "def process_stream(jobs, max_attempts=3):\n"
        "    done = {}\n"
        "    dead = {}\n"
        "    for batch in jobs:\n"
        "        for job_id, payload, attempts in batch:\n"
        "            if payload == 'poison':\n"
        "                dead[job_id] = [job_id, payload, max_attempts]  # WRONG: no retry budget, ignores done-gate\n"
        "                continue\n"
        "            done[job_id] = 'done:' + job_id  # WRONG: re-effects on every redelivery\n"
        "    return {'done': done, 'dead': list(dead.values())}\n"
    ),
)

print("module 10 complete")
