#!/usr/bin/env python3
"""Module 15: capstone-production-platform — requirements brief + graded milestones."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "capstone-production-platform"

# ── lesson 1: the brief ──────────────────────────────────────────────────────
write_lesson(
    MOD, "capstone-brief",
    "Capstone: The TaskFlow Platform Brief",
    "No tutorial. Requirements, constraints, acceptance criteria, and the architectural decisions you own.",
    35,
    """
You will build **TaskFlow** — a production-style job processing platform — from
this brief alone. There are no step-by-step instructions, because there are no
step-by-step jobs.

## What TaskFlow does

- **Ingests jobs** through a submit function: a client submits a payload with
  an idempotency key and receives a job ID immediately (accept/reject, never
  block on the work).
- **Processes jobs with workers** that pull from a queue. Workers are
  unreliable by nature: they crash, they are killed mid-job, they come back.
- **Records every outcome** durably: succeeded jobs with results, failed jobs
  with reasons, and a dead-letter tier for jobs that exhausted their retries.
- **Exposes status**: a client asks "what happened to job X?" and gets an
  honest answer from durable state, not memory.

## Hard requirements (graded, non-negotiable)

1. **At-least-once delivery with exactly-once effects.** A job delivered twice
   produces one effect. Every worker action is idempotent — keyed by the job's
   idempotency key.
2. **Retry with backoff and a budget.** Failing jobs retry with exponential
   backoff ceilings (computed, not slept), capped at 3 attempts, then land in
   the dead-letter store *with the failure reason attached*.
3. **Graceful shutdown.** A shutdown call stops intake, requeues in-flight
   work, and leaves the platform restartable with no lost jobs and no double
   effects.
4. **Observability.** A metrics snapshot: submitted/succeeded/failed/dead
   counts, in-flight gauge, and every log line correlated by job ID with
   secrets redacted.
5. **Authorization.** Job status queries check ownership from the *principal*,
   never from a client-supplied parameter; strangers get not-found, not
   forbidden.
6. **Resilience.** A failing dependency is tripped by a circuit breaker and
   reported by a readiness check — never propagated raw.

## Constraints

- Standard library only. The queue is in-process (the semantics are what's
  graded); a real deployment would swap the port, not the contract.
- Python 3.11. Type-annotate the public surface.
- You own every decision: module layout, class boundaries, error taxonomy.

## Suggested milestones (not a checklist — a shape)

1. **Core loop**: submit → deliver → process → ack, with the idempotency gate.
2. **Failure paths**: retries with backoff, dead-lettering with reasons.
3. **Lifecycle**: graceful shutdown and restart without loss or duplication.
4. **Operations**: metrics snapshot, structured+redacted logs, readiness,
   breaker.
5. **Interface**: status queries with authorization.

Each milestone is graded below by executable acceptance tests — write code
until the tests pass, then keep going until the *design* is one you can defend.
""",
    "Capstone: Đặc tả nền tảng TaskFlow",
    "Không có hướng dẫn từng bước. Yêu cầu, ràng buộc, tiêu chí nghiệm thu, và những quyết định kiến trúc thuộc về bạn.",
    """
Bạn sẽ xây **TaskFlow** — một nền tảng xử lý job kiểu production — chỉ từ bản
đặc tả này. Không có hướng dẫn từng bước, vì không có công việc từng bước.

## TaskFlow làm gì

- **Tiếp nhận job** qua một hàm submit: client gửi payload với một idempotency
  key và nhận job ID ngay lập tức (chấp nhận/từ chối, không bao giờ chờ công
  việc).
- **Xử lý job bằng worker** kéo từ một queue. Worker vốn không đáng tin: chúng
  crash, bị kill giữa chừng, rồi quay lại.
- **Ghi lại mọi kết quả** một cách bền vững: job thành công kèm kết quả, job
  thất bại kèm lý do, và tầng dead-letter cho job đã dùng hết lần retry.
- **Phơi trạng thái**: client hỏi "job X sao rồi?" và nhận câu trả lời trung
  thực từ trạng thái bền vững, không phải từ bộ nhớ.

## Yêu cầu cứng (bị chấm, không thương lượng)

1. **Chuyển giao at-least-once với hiệu ứng exactly-once.** Một job được giao
   hai lần sinh đúng một hiệu ứng. Mọi hành động của worker là idempotent —
   khóa bằng idempotency key của job.
2. **Retry với backoff và ngân sách.** Job thất bại retry với trần backoff hàm
   mũ (được tính, không sleep), tối đa 3 lần, rồi vào kho dead-letter *kèm lý
   do thất bại*.
3. **Tắt máy nhã nhặn.** Một lời gọi shutdown ngừng tiếp nhận, trả công việc
   đang chạy về queue, và để nền tảng khởi động lại mà không mất job, không
   hiệu ứng kép.
4. **Khả năng quan sát.** Một bản chụp metric: số đếm
   submitted/succeeded/failed/dead, gauge in-flight, và mọi dòng log được
   correlation theo job ID với secret được che giấu.
5. **Ủy quyền.** Truy vấn trạng thái job kiểm tra quyền sở hữu từ *principal*,
   không bao giờ từ tham số do client cung cấp; người lạ nhận not-found, không
   phải forbidden.
6. **Khả năng phục hồi.** Dependency hỏng bị circuit breaker ngắt và được
   readiness check báo cáo — không bao giờ được truyền thô ra ngoài.

## Ràng buộc

- Chỉ dùng thư viện chuẩn. Queue nằm trong tiến trình (ngữ nghĩa mới là thứ bị
  chấm); triển khai thật sẽ thay port, không phải hợp đồng.
- Python 3.11. Ghi type annotation cho bề mặt public.
- Bạn sở hữu mọi quyết định: bố cục module, ranh giới lớp, phân loại lỗi.

## Các cột mốc gợi ý (không phải checklist — một hình dạng)

1. **Vòng lặp lõi**: submit → deliver → process → ack, với cổng idempotency.
2. **Đường thất bại**: retry với backoff, dead-letter kèm lý do.
3. **Vòng đời**: tắt nhã nhặn và khởi động lại không mất mát, không trùng lặp.
4. **Vận hành**: bản chụp metric, log có cấu trúc + đã che giấu, readiness,
   breaker.
5. **Giao diện**: truy vấn trạng thái với ủy quyền.

Mỗi cột mốc được chấm bên dưới bằng bài test nghiệm thu thực thi được — hãy
viết code tới khi test pass, rồi tiếp tục cho tới khi *thiết kế* là thứ bạn
bảo vệ được.
""",
)

# ── lesson 2: the architecture worksheet ─────────────────────────────────────
write_lesson(
    MOD, "capstone-design-worksheet",
    "Capstone: The Design Worksheet",
    "Before code: the ports, the state model, and the failure table. Decide now, defend later.",
    25,
    """
Write these down *before* implementing. The graded acceptance tests only check
behavior; your future self checks the design.

## The ports (your architecture, your names)

Sketch the interfaces — not implementations:

- **JobQueue (port)** — `enqueue`, `deliver`, `ack`, `fail`. Who implements it?
  (In-process now; Redis later. The port is what stays.)
- **IdempotencyStore (port)** — `get(key)`, `put(key, result)`. Same
  transaction as the effect, or it lies.
- **JobStore (port)** — durable outcome records. This is your source of truth;
  the queue is *not*.
- **Clock (port)** — you know why.
- **Notifier/Metrics/Log (ports)** — the observability seam.

## The state model

A job is a small state machine:
`SUBMITTED → IN_FLIGHT → SUCCEEDED | FAILED_RETRYING | DEAD`.
Write the legal transitions. What happens to a job in `IN_FLIGHT` when the
worker dies? (Answer: it becomes deliverable again — that's the lease. What
must be true for the *effect* to stay exactly-once? The idempotency gate.)

## The failure table

| Failure | Detection | Response | User-visible? |
|---|---|---|---|
| Worker crash | lease expiry | redeliver | no (effect idempotent) |
| Dependency down | exceptions | breaker opens, fast-fail | degraded feature |
| Poison job | retry exhaustion | dead-letter + reason | yes, on status query |
| Duplicate submit | idempotency key | replay recorded response | no |

If a row of this table is hand-wavy, that's the milestone to build next.

## The self-review questions

- Which decisions would change with a real queue? (Only the adapter.)
- Which class knows about HTTP? (None — that's the point.)
- Where does the idempotency check live, and why *there*?
- What breaks first under load, and how would you know? (Metrics.)
""",
    "Capstone: Bảng thiết kế",
    "Trước khi viết code: các port, mô hình trạng thái, và bảng thất bại. Quyết định ngay, bảo vệ sau.",
    """
Hãy viết những điều này ra *trước* khi cài đặt. Các bài test nghiệm thu chỉ
kiểm tra hành vi; con người bạn tương lai kiểm tra thiết kế.

## Các port (kiến trúc của bạn, tên của bạn)

Phác thảo các giao diện — không phải bản cài:

- **JobQueue (port)** — `enqueue`, `deliver`, `ack`, `fail`. Ai cài nó? (Trong
  tiến trình bây giờ; Redis sau. Cái còn lại là port.)
- **IdempotencyStore (port)** — `get(key)`, `put(key, result)`. Cùng transaction
  với hiệu ứng, nếu không nó nói dối.
- **JobStore (port)** — bản ghi kết quả bền vững. Đây là nguồn sự thật của bạn;
  queue *không phải*.
- **Clock (port)** — bạn biết lý do.
- **Notifier/Metrics/Log (port)** — điểm seam quan sát được.

## Mô hình trạng thái

Một job là một máy trạng thái nhỏ:
`SUBMITTED → IN_FLIGHT → SUCCEEDED | FAILED_RETRYING | DEAD`.
Hãy viết các chuyển tiếp hợp lệ. Job đang `IN_FLIGHT` thì sao khi worker chết?
(Trả lời: nó trở nên có thể giao lại — đó chính là lease. Điều gì phải đúng để
*hiệu ứng* giữ được tính exactly-once? Cổng idempotency.)

## Bảng thất bại

| Thất bại | Phát hiện | Phản hồi | Người dùng thấy? |
|---|---|---|---|
| Worker crash | hết hạn lease | giao lại | không (hiệu ứng idempotent) |
| Dependency chết | exception | breaker mở, fast-fail | tính năng suy giảm |
| Job độc | dùng hết retry | dead-letter + lý do | có, qua truy vấn trạng thái |
| Submit trùng | idempotency key | phát lại phản hồi đã ghi | không |

Nếu một dòng của bảng này còn mơ hồ, đó chính là cột mốc cần xây tiếp.

## Các câu hỏi tự review

- Quyết định nào sẽ thay đổi với một queue thật? (Chỉ adapter.)
- Lớp nào biết về HTTP? (Không lớp nào — đó mới là điểm.)
- Kiểm tra idempotency nằm ở đâu, và vì sao *ở đó*?
- Điều gì gãy đầu tiên dưới tải, và bạn biết bằng cách nào? (Metric.)
""",
)

# ── practice 1: milestone 1+2 ────────────────────────────────────────────────
CORE_REF = (
    "class TaskFlowCore:\n"
    "    '''Milestones 1+2: the core loop with an idempotency gate, retry budget,\n"
    "    and a dead-letter tier with reasons.'''\n"
    "\n"
    "    def __init__(self):\n"
    "        self._pending = []        # [job_id, key, payload, attempts]\n"
    "        self._inflight = []\n"
    "        self._results = {}        # job_id -> result (idempotency store)\n"
    "        self._dead = {}           # job_id -> {'reason', 'attempts'}\n"
    "        self._metrics = {'submitted': 0, 'succeeded': 0, 'failed': 0, 'dead': 0}\n"
    "\n"
    "    def submit(self, key, payload):\n"
    "        '''Accept a job keyed by an idempotency key. Re-submits of a known key\n"
    "        replay the recorded outcome without re-executing. Returns the job id.'''\n"
    "        for job_id, k, payload0, attempts in self._pending + self._inflight:\n"
    "            if k == key:\n"
    "                return job_id   # already accepted; same job\n"
    "        for job_id, k in self._results.items():\n"
    "            pass\n"
    "        if key in self._keys_done:\n"
    "            return self._keys_done[key]\n"
    "        self._metrics['submitted'] += 1\n"
    "        job_id = f'job-{self._metrics[\"submitted\"]}'\n"
    "        self._pending.append([job_id, key, payload, 0])\n"
    "        return job_id\n"
    "\n"
    "    def deliver(self):\n"
    "        batch = self._pending\n"
    "        self._pending = []\n"
    "        redeliver = self._inflight\n"
    "        self._inflight = [list(j) for j in batch]\n"
    "        self._inflight += [list(j) for j in redeliver]\n"
    "        return [list(j) for j in batch + redeliver]\n"
    "\n"
    "    def process(self, job_id, outcome):\n"
    "        '''Record a worker outcome for a delivered job. outcome=True -> success;\n"
    "        a string is a failure reason (consumes a retry attempt). Unknown jobs\n"
    "        are ignored (redelivery of a job already recorded).'''\n"
    "        for j in self._inflight:\n"
    "            if j[0] == job_id:\n"
    "                self._inflight.remove(j)\n"
    "                _, key, payload, attempts = j\n"
    "                if outcome is True:\n"
    "                    self._results[job_id] = {'status': 'succeeded', 'key': key, 'payload': payload}\n"
    "                    self._keys_done[key] = job_id\n"
    "                    self._metrics['succeeded'] += 1\n"
    "                else:\n"
    "                    attempts += 1\n"
    "                    self._metrics['failed'] += 1\n"
    "                    if attempts >= 3:\n"
    "                        self._dead[job_id] = {'status': 'dead', 'key': key, 'payload': payload,\n"
    "                                              'reason': outcome, 'attempts': attempts}\n"
    "                        self._keys_done[key] = job_id\n"
    "                        self._metrics['dead'] += 1\n"
    "                    else:\n"
    "                        self._pending.append([job_id, key, payload, attempts])\n"
    "                return\n"
    "\n"
    "    def status(self, job_id):\n"
    "        if job_id in self._results:\n"
    "            return dict(self._results[job_id])\n"
    "        if job_id in self._dead:\n"
    "            return dict(self._dead[job_id])\n"
    "        for j in self._inflight:\n"
    "            if j[0] == job_id:\n"
    "                return {'status': 'in_flight', 'key': j[1], 'payload': j[2]}\n"
    "        for j in self._pending:\n"
    "            if j[0] == job_id:\n"
    "                return {'status': 'pending', 'key': j[1], 'payload': j[2], 'attempts': j[3]}\n"
    "        return None\n"
    "\n"
    "    @property\n"
    "    def metrics(self):\n"
    "        return dict(self._metrics)\n"
)
CORE_REF = CORE_REF.replace("        self._metrics = {'submitted': 0, 'succeeded': 0, 'failed': 0, 'dead': 0}",
    "        self._metrics = {'submitted': 0, 'succeeded': 0, 'failed': 0, 'dead': 0}\n"
    "        self._keys_done = {}")
CORE_REF = CORE_REF.replace("""        for job_id, k, payload0, attempts in self._pending + self._inflight:
            if k == key:
                return job_id   # already accepted; same job
        for job_id, k in self._results.items():
            pass
        if key in self._keys_done:
            return self._keys_done[key]
""", """        for job_id, k, payload0, attempts in self._pending + self._inflight:
            if k == key:
                return job_id   # already accepted; same job
        if key in self._keys_done:
            return self._keys_done[key]
""")
CORE_WRONG = (
    "class TaskFlowCore:\n"
    "    def __init__(self):\n"
    "        self._pending = []\n"
    "        self._inflight = []\n"
    "        self._results = {}\n"
    "        self._dead = {}\n"
    "        self._keys_done = {}\n"
    "        self._metrics = {'submitted': 0, 'succeeded': 0, 'failed': 0, 'dead': 0}\n"
    "\n"
    "    def submit(self, key, payload):\n"
    "        # WRONG: accepts duplicate keys as new jobs — exactly-once effects broken\n"
    "        self._metrics['submitted'] += 1\n"
    "        job_id = f'job-{self._metrics[\"submitted\"]}'\n"
    "        self._pending.append([job_id, key, payload, 0])\n"
    "        return job_id\n"
    "\n"
    "    def deliver(self):\n"
    "        batch = self._pending\n"
    "        self._pending = []\n"
    "        self._inflight = [list(j) for j in batch]\n"
    "        return [list(j) for j in batch]\n"
    "\n"
    "    def process(self, job_id, outcome):\n"
    "        for j in self._inflight:\n"
    "            if j[0] == job_id:\n"
    "                self._inflight.remove(j)\n"
    "                _, key, payload, attempts = j\n"
    "                if outcome is True:\n"
    "                    self._results[job_id] = {'status': 'succeeded', 'key': key, 'payload': payload}\n"
    "                    self._keys_done[key] = job_id\n"
    "                    self._metrics['succeeded'] += 1\n"
    "                else:\n"
    "                    attempts += 1\n"
    "                    self._metrics['failed'] += 1\n"
    "                    if attempts >= 3:\n"
    "                        self._dead[job_id] = {'status': 'dead', 'key': key, 'payload': payload,\n"
    "                                              'reason': outcome, 'attempts': attempts}\n"
    "                        self._keys_done[key] = job_id\n"
    "                        self._metrics['dead'] += 1\n"
    "                    else:\n"
    "                        self._pending.append([job_id, key, payload, attempts])\n"
    "                return\n"
    "\n"
    "    def status(self, job_id):\n"
    "        if job_id in self._results:\n"
    "            return dict(self._results[job_id])\n"
    "        if job_id in self._dead:\n"
    "            return dict(self._dead[job_id])\n"
    "        return None\n"
    "\n"
    "    @property\n"
    "    def metrics(self):\n"
    "        return dict(self._metrics)\n"
)

write_practice(
    MOD, "pa-p15-core-practice",
    "Milestone 1+2: The Core Loop",
    "Submit → deliver → process → ack with the idempotency gate, then retries with a budget and a dead-letter tier.",
    "Cột mốc 1+2: Vòng lặp lõi",
    "Submit → deliver → process → ack với cổng idempotency, rồi retry với ngân sách và tầng dead-letter.",
    "capstone-brief", 40, "advanced",
    [
        challenge(
            "pa-cap-core-loop",
            "TaskFlow core: idempotent submits, budgeted retries",
            "Implement `TaskFlowCore` (milestones 1+2 of the capstone):\n\n- `submit(key, payload)` → job id `'job-<n>'` (n counts submissions); submitting the SAME key again returns the ORIGINAL job id without counting or queueing anything (the idempotency gate, covering pending, in-flight, succeeded, and dead jobs)\n- `deliver()` → list of `[job_id, key, payload, attempts]`, moving pending jobs in-flight and re-delivering in-flight ones (lease expiry)\n- `process(job_id, outcome)` — `True` records success; a string records a failure reason, increments attempts, and re-queues; at `attempts >= 3` the job moves to the dead tier carrying the LAST reason and attempt count; unknown job ids are ignored\n- `status(job_id)` — dict with `'status'` one of `'pending'/'in_flight'/'succeeded'/'dead'` (plus key/payload/attempts/reason as appropriate), or `None` for unknown ids\n- `metrics` property — `{'submitted', 'succeeded', 'failed', 'dead'}` counts\n\nDelivered jobs whose outcome was already recorded must be skippable: a redelivered succeeded job neither re-executes nor corrupts counts.",
            "class TaskFlowCore:\n    def __init__(self):\n        ...\n\n    def submit(self, key, payload):\n        ...\n\n    def deliver(self):\n        ...\n\n    def process(self, job_id, outcome):\n        ...\n\n    def status(self, job_id):\n        ...\n\n    @property\n    def metrics(self):\n        ...",
            [
                ("idempotent submits, exactly-once effects",
                 "core = TaskFlowCore()\na = core.submit('k1', {'op': 'charge'})\nb = core.submit('k1', {'op': 'charge'})   # same key: same job, no double-count\nassert a == b\nassert core.metrics['submitted'] == 1\nbatch = core.deliver()\nassert len(batch) == 1\ncore.process(batch[0][0], True)\nassert core.status(batch[0][0])['status'] == 'succeeded'\ncore.deliver()   # lease expiry re-delivers the (already acked) job\ncore.process(batch[0][0], True)  # ignored: already recorded\nassert core.metrics['succeeded'] == 1\nprint('ok')",
                 "Duplicate submit replays the original id; duplicate processing is a no-op."),
                ("retries exhaust into the dead tier with the reason",
                 "core = TaskFlowCore()\njid = core.submit('poison-1', {'op': 'x'})\nfor _ in range(3):\n    batch = core.deliver()\n    core.process(batch[0][0], 'dependency down')\nst = core.status(jid)\nassert st['status'] == 'dead' and st['attempts'] == 3 and st['reason'] == 'dependency down'\nassert core.metrics == {'submitted': 1, 'succeeded': 0, 'failed': 3, 'dead': 1}\nprint('ok')",
                 "Three failures = dead with the reason attached; metrics tell the story."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-cap-core-loop": vi_challenge(
            "TaskFlow lõi: submit idempotent, retry có ngân sách",
            "Cài `TaskFlowCore` (cột mốc 1+2 của capstone):\n\n- `submit(key, payload)` → job id `'job-<n>'` (n đếm số lần submit); submit LẠI cùng key trả về job id GỐC mà không đếm hay xếp hàng gì thêm (cổng idempotency, phủ cả pending, in-flight, succeeded, và dead)\n- `deliver()` → list `[job_id, key, payload, attempts]`, chuyển pending sang in-flight và giao lại các job in-flight (lease hết hạn)\n- `process(job_id, outcome)` — `True` ghi thành công; một chuỗi ghi lý do thất bại, tăng attempts, và trả về queue; khi `attempts >= 3` job chuyển sang tầng dead mang lý do CUỐI và số lần thử; job id lạ bị bỏ qua\n- `status(job_id)` — dict với `'status'` là một trong `'pending'/'in_flight'/'succeeded'/'dead'` (kèm key/payload/attempts/reason tùy hợp), hoặc `None` cho id lạ\n- property `metrics` — số đếm `{'submitted', 'succeeded', 'failed', 'dead'}`\n\nCác job đã giao mà kết quả đã ghi phải bỏ qua được: job succeeded bị giao lại không thực thi lại và không làm hỏng số đếm.",
            [("Submit idempotent, hiệu ứng exactly-once", "Submit trùng phát lại id gốc; xử lý trùng là no-op."),
             ("Retry dùng hết vào tầng dead kèm lý do", "Ba lần thất bại = dead kèm lý do; metrics kể lại câu chuyện.")],
        ),
    },
    solutions=[("pa-cap-core-loop", CORE_REF, CORE_WRONG)],
)

# ── practice 2: milestone 3+4 ────────────────────────────────────────────────
OPS_REF = (
    "import json as _json\n"
    "\n"
    "\n"
    "class TaskFlowOps:\n"
    "    '''Milestones 3+4: graceful shutdown/restart and operational surfaces.'''\n"
    "\n"
    "    SENSITIVE = {'password', 'token', 'secret', 'card_number'}\n"
    "\n"
    "    def __init__(self):\n"
    "        self.running = True\n"
    "        self.in_flight = 0\n"
    "        self.requeued = []\n"
    "        self.drained = False\n"
    "        self._lines = []\n"
    "        self._jobs = {}          # job_id -> principal\n"
    "        self._breaker_open = False\n"
    "\n"
    "    def shutdown(self):\n"
    "        self.running = False\n"
    "        if self.in_flight:\n"
    "            self.requeued.append(self.in_flight)\n"
    "            self.in_flight = 0\n"
    "        self.drained = True\n"
    "\n"
    "    def job(self, job_id, principal):\n"
    "        self._jobs[job_id] = principal\n"
    "\n"
    "    def status_for(self, job_id, principal):\n"
    "        '''Ownership from the principal, never a parameter; strangers get None.'''\n"
    "        owner = self._jobs.get(job_id)\n"
    "        if owner is None or owner != principal:\n"
    "            return None\n"
    "        return {'job_id': job_id}\n"
    "\n"
    "    def log(self, level, event, job_id=None, **fields):\n"
    "        line = {'level': level, 'event': event, 'correlation_id': job_id}\n"
    "        for k, v in fields.items():\n"
    "            line[k] = '[REDACTED]' if k in self.SENSITIVE else v\n"
    "        self._lines.append(_json.dumps(line, sort_keys=True))\n"
    "\n"
    "    @property\n    " " def lines(self):\n"
    "        return list(self._lines)\n"
    "\n"
    "    def trip_breaker(self):\n"
    "        self._breaker_open = True\n"
    "\n"
    "    def readiness(self):\n"
    "        '''Ready iff intake open and breaker closed; reports both probes.'''\n"
    "        return {'ready': self.running and not self._breaker_open,\n"
    "                'checks': {'intake': self.running, 'dependencies': not self._breaker_open}}\n"
)
OPS_REF = OPS_REF.replace("    @property    " " def lines(self):", "    @property\n    def lines(self):")
OPS_WRONG = (
    "import json as _json\n"
    "\n"
    "\n"
    "class TaskFlowOps:\n"
    "    SENSITIVE = {'password', 'token', 'secret', 'card_number'}\n"
    "\n"
    "    def __init__(self):\n"
    "        self.running = True\n"
    "        self.in_flight = 0\n"
    "        self.requeued = []\n"
    "        self.drained = False\n"
    "        self._lines = []\n"
    "        self._jobs = {}\n"
    "        self._breaker_open = False\n"
    "\n"
    "    def shutdown(self):\n"
    "        self.running = False\n"
    "        self.in_flight = 0  # WRONG: in-flight work vanishes\n"
    "        self.drained = True\n"
    "\n"
    "    def job(self, job_id, principal):\n"
    "        self._jobs[job_id] = principal\n"
    "\n"
    "    def status_for(self, job_id, principal, as_user=None):\n"
    "        # WRONG: trusts the client-supplied as_user parameter\n"
    "        owner = self._jobs.get(job_id)\n"
    "        if owner is None or owner != (as_user or principal):\n"
    "            return None\n"
    "        return {'job_id': job_id}\n"
    "\n"
    "    def log(self, level, event, job_id=None, **fields):\n"
    "        line = {'level': level, 'event': event, 'correlation_id': job_id}\n"
    "        line.update(fields)  # WRONG: no redaction\n"
    "        self._lines.append(_json.dumps(line, sort_keys=True))\n"
    "\n"
    "    @property\n"
    "    def lines(self):\n"
    "        return list(self._lines)\n"
    "\n"
    "    def trip_breaker(self):\n"
    "        self._breaker_open = True\n"
    "\n"
    "    def readiness(self):\n"
    "        return {'ready': self.running}  # WRONG: ignores the breaker\n"
)

write_practice(
    MOD, "pa-p15-ops-practice",
    "Milestone 3+4: Lifecycle & Operations",
    "Graceful shutdown that requeues, ownership-checked status, readiness with a breaker, and redacted correlated logs.",
    "Cột mốc 3+4: Vòng đời và vận hành",
    "Tắt nhã nhặn có trả về queue, trạng thái kiểm tra quyền sở hữu, readiness với breaker, và log đã che giấu có correlation.",
    "capstone-brief", 35, "advanced",
    [
        challenge(
            "pa-cap-ops",
            "TaskFlow ops: graceful, honest, observable",
            "Implement `TaskFlowOps` (milestones 3+4):\n\n- `shutdown()` — stops intake (`running = False`), requeues in-flight count into `requeued`, zeroes `in_flight`, marks `drained = True`\n- `job(job_id, principal)` registers ownership; `status_for(job_id, principal)` returns the status dict for the owner, `None` for anyone else (no forbidden distinction, no as_user parameter to trust)\n- `log(level, event, job_id=None, **fields)` — appends a sorted-keys JSON line with `correlation_id` set to job_id, redacting any of password/token/secret/card_number as '[REDACTED]'\n- `trip_breaker()` / `readiness()` — readiness returns `{'ready': running and not breaker_open, 'checks': {'intake': ..., 'dependencies': ...}}`\n\nRestart-readiness: after `shutdown()`, all work is in `requeued` and nothing is lost.",
            "class TaskFlowOps:\n    SENSITIVE = {'password', 'token', 'secret', 'card_number'}\n\n    def __init__(self):\n        ...\n\n    def shutdown(self):\n        ...\n\n    def job(self, job_id, principal):\n        ...\n\n    def status_for(self, job_id, principal):\n        ...\n\n    def log(self, level, event, job_id=None, **fields):\n        ...\n\n    def trip_breaker(self):\n        ...\n\n    def readiness(self):\n        ...",
            [
                ("shutdown requeues; status checks ownership; logs redact",
                 "import json\nops = TaskFlowOps()\nops.in_flight = 2\nops.shutdown()\nassert ops.requeued == [2] and ops.drained is True\nops.job('j1', 'alice')\nassert ops.status_for('j1', 'alice') == {'job_id': 'j1'}\nassert ops.status_for('j1', 'bob') is None\nops.log('ERROR', 'job.failed', job_id='j1', token='sekrit')\nline = json.loads(ops.lines[0])\nassert line['correlation_id'] == 'j1' and line['token'] == '[REDACTED]'\nprint('ok')",
                 "Lifecycle, authorization, and observability in one surface."),
                ("readiness reports the breaker",
                 "ops = TaskFlowOps()\nassert ops.readiness() == {'ready': True, 'checks': {'intake': True, 'dependencies': True}}\nops.trip_breaker()\nr = ops.readiness()\nassert r['ready'] is False and r['checks']['dependencies'] is False and r['checks']['intake'] is True\nprint('ok')",
                 "The probe distinguishes which check failed — that's the point of readiness."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-cap-ops": vi_challenge(
            "TaskFlow ops: nhã nhặn, trung thực, quan sát được",
            "Cài `TaskFlowOps` (cột mốc 3+4):\n\n- `shutdown()` — ngừng tiếp nhận (`running = False`), trả số in-flight về `requeued`, đưa `in_flight` về 0, đánh dấu `drained = True`\n- `job(job_id, principal)` đăng ký quyền sở hữu; `status_for(job_id, principal)` trả dict trạng thái cho owner, `None` với bất kỳ ai khác (không phân biệt forbidden, không có tham số as_user để tin)\n- `log(level, event, job_id=None, **fields)` — thêm một dòng JSON khóa-đã-sắp với `correlation_id` bằng job_id, che giấu password/token/secret/card_number thành '[REDACTED]'\n- `trip_breaker()` / `readiness()` — readiness trả `{'ready': running và không breaker_open, 'checks': {'intake': ..., 'dependencies': ...}}`\n\nKhởi động lại được: sau `shutdown()`, mọi công việc nằm trong `requeued` và không mất gì.",
            [("Shutdown trả về queue; trạng thái kiểm quyền; log che giấu", "Vòng đời, ủy quyền, và quan sát trong một bề mặt."),
             ("Readiness báo breaker", "Probe phân biệt được check nào hỏng — đó mới là ý nghĩa của readiness.")],
        ),
    },
    solutions=[("pa-cap-ops", OPS_REF, OPS_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
write_checkpoint(
    MOD, "pa-checkpoint-capstone",
    "Checkpoint: Capstone Readiness",
    "The final gate: restart safety — the property that makes TaskFlow production-grade.",
    30,
    """
**The exam question:** TaskFlow dies mid-flight and comes back. Prove no job
is lost, no effect is doubled, and every client still gets an honest answer.

The checkpoint tests restart safety as one scenario: submit, deliver, crash
(shutdown without recording), restart, redeliver, process — and the outcome
must be exactly as if nothing had died.
""",
    "Checkpoint: Sẵn sàng Capstone",
    "Cổng cuối: an toàn khi khởi động lại — tính chất khiến TaskFlow đạt chuẩn production.",
    """
**Câu hỏi thi:** TaskFlow chết giữa chừng rồi quay lại. Hãy chứng minh không
job nào bị mất, không hiệu ứng nào bị nhân đôi, và mọi client vẫn nhận câu trả
lời trung thực.

Checkpoint kiểm tra an toàn khởi động lại như một kịch bản duy nhất: submit,
deliver, crash (shutdown mà không ghi kết quả), khởi động lại, giao lại, xử lý
— và kết quả phải y như khi không có gì chết.
""",
    challenge(
        "pa-cap-restart-safety",
        "Crash, restart, and the truth survives",
        "Implement `simulate_crash_restart(core)` — a scenario runner over your TaskFlowCore from the core-loop milestone:\n\n1. `a = core.submit('alpha', {'op': 1})` and `b = core.submit('beta', {'op': 2})`\n2. deliver once; record the delivered batch\n3. SIMULATE CRASH: call `core.shutdown()` — which must stop intake and requeue everything in-flight back to pending (exactly-once effects make this safe) — and then call `core.restart()` (adds `'restarted': True` to metrics; running again)\n4. after restart: deliver, and `process(job_id, True)` for every delivered job\n\nThe function returns `{'a': core.status(a), 'b': core.status(b), 'metrics': core.metrics}` where both jobs end `'succeeded'`, and metrics show `submitted == 2`, `succeeded == 2`, `failed == 0` (the crash requeued; it did not fail anything).\n\nAdd `shutdown()` and `restart()` to TaskFlowCore: `shutdown()` moves all in-flight jobs back to pending (running = False); `restart()` clears drained state and sets metrics['restarted'] = True.",
        "# TaskFlowCore gains shutdown() and restart(); then:\n\ndef simulate_crash_restart(core):\n    ...",
        [
            ("the crash loses nothing and breaks nothing",
             "core = TaskFlowCore()\nr = simulate_crash_restart(core)\nassert r['a']['status'] == 'succeeded' and r['b']['status'] == 'succeeded'\nassert r['metrics']['submitted'] == 2 and r['metrics']['succeeded'] == 2\nassert r['metrics']['failed'] == 0 and r['metrics'].get('restarted') is True\nprint('ok')",
             "In-flight work was requeued, redelivered once, effected once."),
        ],
        level="build",
    ),
    vi_challenge(
        "Crash, khởi động lại, và sự thật còn nguyên",
        "Cài `simulate_crash_restart(core)` — một trình chạy kịch bản trên TaskFlowCore của bạn từ cột mốc vòng lặp lõi:\n\n1. `a = core.submit('alpha', {'op': 1})` và `b = core.submit('beta', {'op': 2})`\n2. deliver một lần; ghi lại batch đã giao\n3. MÔ PHỎNG CRASH: gọi `core.shutdown()` — phải ngừng tiếp nhận và trả mọi job in-flight về pending (hiệu ứng exactly-once khiến điều này an toàn) — rồi gọi `core.restart()` (thêm `'restarted': True` vào metrics; chạy lại)\n4. sau khởi động lại: deliver, và `process(job_id, True)` cho mọi job được giao\n\nHàm trả `{'a': core.status(a), 'b': core.status(b), 'metrics': core.metrics}` trong đó cả hai job kết thúc `'succeeded'`, và metrics cho thấy `submitted == 2`, `succeeded == 2`, `failed == 0` (crash đã trả về queue; không làm fail gì cả).\n\nThêm `shutdown()` và `restart()` vào TaskFlowCore: `shutdown()` chuyển mọi job in-flight về pending (running = False); `restart()` xóa trạng thái drained và đặt metrics['restarted'] = True.",
        [("Crash không mất gì và không phá gì", "Công việc in-flight được trả về queue, giao lại một lần, tạo hiệu ứng một lần.")],
    ),
    solution=(
        "def simulate_crash_restart(core):\n"
        "    a = core.submit('alpha', {'op': 1})\n"
        "    b = core.submit('beta', {'op': 2})\n"
        "    core.deliver()\n"
        "    core.shutdown()\n"
        "    core.restart()\n"
        "    batch = core.deliver()\n"
        "    for job_id, key, payload, attempts in batch:\n"
        "        core.process(job_id, True)\n"
        "    return {'a': core.status(a), 'b': core.status(b), 'metrics': core.metrics}\n"
    ),
    wrong=(
        "def simulate_crash_restart(core):\n"
        "    a = core.submit('alpha', {'op': 1})\n"
        "    b = core.submit('beta', {'op': 2})\n"
        "    core.deliver()\n"
        "    core.shutdown()\n"
        "    core.restart()\n"
        "    # WRONG: never re-delivers after restart — jobs stay pending forever\n"
        "    return {'a': core.status(a), 'b': core.status(b), 'metrics': core.metrics}\n"
    ),
)

print("module 15 complete")
