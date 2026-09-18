#!/usr/bin/env python3
"""Module 5: structured-async — lessons + practices + checkpoint (graded code targets 3.11)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "structured-async"

write_module(
    MOD,
    "Structured Async Python",
    "TaskGroup, timeouts, cancellation propagation, async context managers and iterators — concurrency that composes.",
    "Async Python có cấu trúc",
    "TaskGroup, timeout, lan truyền hủy, async context manager và iterator — concurrency có thể kết hợp.",
    ["event-loop-tasks", "cancellation-timeouts", "async-protocol-patterns"],
    ["pa-p5-taskgroup-practice", "pa-p5-timeout-practice", "pa-p5-iterator-practice", "pa-p5-service-project"],
)

L1_EN = """
## Coroutines, the loop, and TaskGroup

`async def` defines a **coroutine function**; calling it creates a coroutine
object that does nothing until awaited or scheduled. The **event loop** runs
scheduled coroutines to completion, switching between them at every `await`
(suspension point).

Cooperative multitasking means one rule: **never block the loop.** A bare
`time.sleep(1)` inside a coroutine freezes every other task; `await
asyncio.sleep(1)` yields properly.

```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)          # stand-in for I/O
    return f"{name}-done"

async def main():
    results = []
    async with asyncio.TaskGroup() as tg:          # 3.11+
        t1 = tg.create_task(fetch("a", 0.1))
        t2 = tg.create_task(fetch("b", 0.2))
    return t1.result(), t2.result()    # both done when the block exits
```

`TaskGroup` (3.11+) is the structured-concurrency primitive: tasks created in
the group are guaranteed finished (or the group raised) when the `async with`
exits. If any task raises, the group cancels the others and raises
`ExceptionGroup` (unwrap single errors with `except*` or `group.exceptions`).

Legacy `asyncio.gather(*aws)` still exists and returns results in order; it
does NOT cancel siblings on failure by default. New code prefers TaskGroup.
"""

L1_VI = L1_EN.replace(
    "## Coroutines, the loop, and TaskGroup",
    "## Coroutine, event loop và TaskGroup",
).replace(
    "`async def` defines a **coroutine function**; calling it creates a coroutine\nobject that does nothing until awaited or scheduled. The **event loop** runs\nscheduled coroutines to completion, switching between them at every `await`\n(suspension point).",
    "`async def` định nghĩa một **coroutine function**; gọi nó tạo ra một coroutine\nobject không làm gì cả cho tới khi được await hoặc lên lịch. **Event loop**\nchạy các coroutine đã lên lịch tới cùng, chuyển giữa chúng tại mỗi `await`\n(điểm treo).",
).replace(
    "Cooperative multitasking means one rule: **never block the loop.** A bare\n`time.sleep(1)` inside a coroutine freezes every other task; `await\nasyncio.sleep(1)` yields properly.",
    "Đa nhiệm hợp tác nghĩa là một quy tắc: **đừng bao giờ chặn loop.**\n`time.sleep(1)` trần trụi trong coroutine đóng băng mọi task khác;\n`await asyncio.sleep(1)` nhường đúng cách.",
).replace(
    "`TaskGroup` (3.11+) is the structured-concurrency primitive: tasks created in\nthe group are guaranteed finished (or the group raised) when the `async with`\nexits. If any task raises, the group cancels the others and raises\n`ExceptionGroup` (unwrap single errors with `except*` or `group.exceptions`).",
    "`TaskGroup` (3.11+) là primitive của structured concurrency: task tạo trong\nnhóm được bảo đảm xong (hoặc nhóm raise) khi `async with` thoát. Nếu task nào\nraise, nhóm hủy các task còn lại và raise `ExceptionGroup` (bóc lỗi đơn bằng\n`except*` hay `group.exceptions`).",
).replace(
    "Legacy `asyncio.gather(*aws)` still exists and returns results in order; it\ndoes NOT cancel siblings on failure by default. New code prefers TaskGroup.",
    "`asyncio.gather(*aws)` cũ vẫn tồn tại và trả kết quả theo thứ tự; nó KHÔNG hủy\ncác task anh em khi có lỗi theo mặc định. Code mới ưu tiên TaskGroup.",
)

write_lesson(
    MOD, "event-loop-tasks",
    "The event loop and TaskGroup",
    "Schedule work that composes: tasks bounded by a scope, failures that cancel siblings.",
    22, L1_EN,
    "Event loop và TaskGroup",
    "Lên lịch công việc có thể kết hợp: task bị chặn trong scope, lỗi sẽ hủy task anh em.",
    L1_VI,
)

L2_EN = """
## Timeouts and cancellation, done properly

Cancellation in asyncio is **cooperative and exception-based**: cancelling a
task arranges `CancelledError` to be raised at its current await point.

`asyncio.timeout(seconds)` (3.11+) wraps a block:

```python
import asyncio

async def slow_api():
    await asyncio.sleep(10)

async def handler():
    try:
        async with asyncio.timeout(0.5):
            await slow_api()
    except TimeoutError:
        return "gave up"          # TimeoutError in 3.11+, asyncio.TimeoutError before
```

What professionals must know:

- **Timeouts cancel; cancellation propagates.** Inner `finally` blocks and
  async context managers still run — cleanup code must be cancellation-safe
  (no unbounded awaits inside cleanup).
- A coroutine may **shield** a critical section with
  `asyncio.shield(coro)` — the shielded await still gets CancelledError in the
  caller, but the inner operation continues.
- Swallowing `CancelledError` (bare `except Exception` does NOT catch it in
  3.8+... but `except BaseException` does) is the classic way to break
  structured concurrency. Only catch it to re-raise after cleanup.
- `asyncio.call_later`, loop-bound timers, and `asyncio.to_thread` (3.9+) for
  offloading blocking calls to a thread round out the toolkit.
"""

L2_VI = L2_EN.replace(
    "## Timeouts and cancellation, done properly",
    "## Timeout và hủy, làm cho đúng",
).replace(
    "Cancellation in asyncio is **cooperative and exception-based**: cancelling a\ntask arranges `CancelledError` to be raised at its current await point.",
    "Hủy trong asyncio là **hợp tác và dựa trên exception**: hủy một task sẽ sắp đặt\ncho `CancelledError` được raise tại điểm await hiện tại của nó.",
).replace(
    "What professionals must know:",
    "Những điều chuyên nghiệp phải biết:",
).replace(
    "- **Timeouts cancel; cancellation propagates.** Inner `finally` blocks and\n  async context managers still run — cleanup code must be cancellation-safe\n  (no unbounded awaits inside cleanup).\n- A coroutine may **shield** a critical section with\n  `asyncio.shield(coro)` — the shielded await still gets CancelledError in the\n  caller, but the inner operation continues.\n- Swallowing `CancelledError` (bare `except Exception` does NOT catch it in\n  3.8+... but `except BaseException` does) is the classic way to break\n  structured concurrency. Only catch it to re-raise after cleanup.\n- `asyncio.call_later`, loop-bound timers, and `asyncio.to_thread` (3.9+) for\n  offloading blocking calls to a thread round out the toolkit.",
    "- **Timeout hủy; sự hủy lan truyền.** Các block `finally` bên trong và async\n  context manager vẫn chạy — mã dọn dẹp phải an toàn khi bị hủy (không await\n  vô hạn trong phần cleanup).\n- Coroutine có thể **shield** một đoạn găng bằng `asyncio.shield(coro)` —\n  phía gọi vẫn nhận CancelledError, nhưng thao tác bên trong vẫn tiếp tục.\n- Nuốt `CancelledError` (`except Exception` thường KHÔNG bắt nó từ 3.8+...\n  nhưng `except BaseException` thì có) là cách kinh điển phá vỡ structured\n  concurrency. Chỉ bắt nó để re-raise sau khi dọn dẹp.\n- `asyncio.call_later`, timer gắn loop, và `asyncio.to_thread` (3.9+) để đẩy\n  call blocking sang thread — hoàn thiện bộ công cụ.",
)

write_lesson(
    MOD, "cancellation-timeouts",
    "Timeouts, cancellation, shield",
    "Bound waiting time; keep cleanup cancellation-safe; never swallow CancelledError.",
    22, L2_EN,
    "Timeout, hủy, shield",
    "Giới hạn thời gian chờ; giữ cleanup an toàn khi bị hủy; đừng nuốt CancelledError.",
    L2_VI,
)

L3_EN = """
## Async context managers, iterators, and backpressure

**Async context managers** (`async with`) allow awaits inside `__aenter__` /
`__aexit__` — connections, locks, transactions:

```python
class AsyncConnection:
    async def __aenter__(self):
        await self._connect()
        return self
    async def __aexit__(self, exc_type, exc, tb):
        await self._close()
```

`contextlib.asynccontextmanager` turns a generator into one, exactly like its
sync sibling.

**Async iterators** (`async for`) pull items across awaits; **async
generators** (`async def` with `yield`) produce them:

```python
import asyncio

async def ticker(n, delay=0.01):
    for i in range(n):
        await asyncio.sleep(delay)
        yield i

async def consume():
    async for value in ticker(3):
        print(value)
```

**Bounded queues** are async backpressure made visible:
`queue = asyncio.Queue(maxsize=10)`. `await queue.put(x)` suspends the
producer when full — the producer slows to the consumer's pace instead of
growing memory without limit. `await queue.get()` suspends the consumer when
empty. Workers + `queue.join()` + `task_done()` work exactly like the threaded
version from the previous module, but on the loop.
"""

L3_VI = L3_EN.replace(
    "## Async context managers, iterators, and backpressure",
    "## Async context manager, iterator và backpressure",
).replace(
    "**Async context managers** (`async with`) allow awaits inside `__aenter__` /\n`__aexit__` — connections, locks, transactions:",
    "**Async context manager** (`async with`) cho phép await bên trong `__aenter__`\n/ `__aexit__` — kết nối, lock, transaction:",
).replace(
    "`contextlib.asynccontextmanager` turns a generator into one, exactly like its\nsync sibling.",
    "`contextlib.asynccontextmanager` biến một generator thành async context\nmanager, y hệt người anh em đồng bộ.",
).replace(
    "**Async iterators** (`async for`) pull items across awaits; **async\ngenerators** (`async def` with `yield`) produce them:",
    "**Async iterator** (`async for`) kéo item qua các lần await; **async\ngenerator** (`async def` có `yield`) sản xuất chúng:",
).replace(
    "**Bounded queues** are async backpressure made visible:\n`queue = asyncio.Queue(maxsize=10)`. `await queue.put(x)` suspends the\nproducer when full — the producer slows to the consumer's pace instead of\ngrowing memory without limit. `await queue.get()` suspends the consumer when\nempty. Workers + `queue.join()` + `task_done()` work exactly like the threaded\nversion from the previous module, but on the loop.",
    "**Queue có giới hạn** là backpressure dạng async nhìn thấy được:\n`queue = asyncio.Queue(maxsize=10)`. `await queue.put(x)` treo producer khi\nđầy — producer chậm lại theo nhịp của consumer thay vì phình bộ nhớ vô hạn.\n`await queue.get()` treo consumer khi rỗng. Worker + `queue.join()` +\n`task_done()` hoạt động y như bản dùng thread ở module trước, nhưng ngay trên\nloop.",
)

write_lesson(
    MOD, "async-protocol-patterns",
    "Async CMs, async generators, bounded queues",
    "Compose async resources safely; let bounded queues enforce producer pace.",
    22, L3_EN,
    "Async CM, async generator, queue có giới hạn",
    "Kết hợp tài nguyên async an toàn; để queue có giới hạn ép nhịp producer.",
    L3_VI,
)

# ── practice 1: TaskGroup gather ─────────────────────────────────────────────
TG_REF = (
    "import asyncio\n\n\n"
    "async def fetch_all(jobs):\n"
    "    '''jobs: list of zero-arg async callables. Returns list of (index, value)\n"
    "    in INPUT order. Raises if any job raises (siblings cancelled by TaskGroup).'''\n"
    "    results = [None] * len(jobs)\n"
    "    async with asyncio.TaskGroup() as tg:\n"
    "        tasks = [tg.create_task(jobs[i](), name=f'job-{i}') for i in range(len(jobs))]\n"
    "    for i, t in enumerate(tasks):\n"
    "        results[i] = (i, t.result())\n"
    "    return results"
)
TG_WRONG = (
    "import asyncio\n\n\n"
    "async def fetch_all(jobs):\n"
    "    '''WRONG: sequential awaits — no concurrency at all.'''\n"
    "    results = []\n"
    "    for i, job in enumerate(jobs):\n"
    "        results.append((i, await job()))\n"
    "    return results"
)

write_practice(
    MOD, "pa-p5-taskgroup-practice",
    "TaskGroup Practice",
    "Structured fan-out: all tasks complete inside a scope, results in input order, failures cancel siblings.",
    "Luyện TaskGroup",
    "Fan-out có cấu trúc: mọi task hoàn tất trong một scope, kết quả theo thứ tự đầu vào, lỗi hủy task anh em.",
    "event-loop-tasks", 20, "advanced",
    [
        challenge(
            "pa-async-taskgroup-fanout",
            "Structured fan-out with TaskGroup",
            "Implement `async def fetch_all(jobs)` where `jobs` is a list of zero-arg async callables:\n\n- run ALL jobs concurrently inside one `asyncio.TaskGroup`\n- return a list of `(index, value)` tuples in INPUT order\n- if any job raises, fetch_all must raise (do not swallow)\n\nDeterminism note: the graded jobs sleep for staggered durations; the total wall time must reflect concurrency, and results must come back in input order regardless of completion order.",
            "import asyncio\n\n# TODO: fetch_all(jobs)",
            [
                ("concurrent execution, input-ordered results",
                 "started = []\nasync def job(i, delay):\n    started.append(i)\n    await asyncio.sleep(delay)\n    return f'v{i}'\n\njobs = [lambda: job(0, 0.05), lambda: job(1, 0.01), lambda: job(2, 0.03)]\nimport time\nloop = asyncio.new_event_loop()\nt0 = time.perf_counter()\nout = loop.run_until_complete(fetch_all(jobs))\nelapsed = time.perf_counter() - t0\nloop.close()\nassert out == [(0, 'v0'), (1, 'v1'), (2, 'v2')], f'out: {out}'\nassert elapsed < 0.075, f'ran sequentially? elapsed={elapsed:.3f}'\nprint('ok')",
                 "create_task all three inside the TaskGroup, then read .result() in index order after the block exits."),
                ("failure propagates from the group",
                 "async def bad():\n    raise ValueError('nope')\nasync def ok():\n    await asyncio.sleep(0.01)\n    return 1\n\nloop = asyncio.new_event_loop()\ntry:\n    loop.run_until_complete(fetch_all([ok, bad]))\nexcept* ValueError:\n    pass\nelse:\n    raise AssertionError('failure must propagate')\nfinally:\n    loop.close()\nprint('ok')",
                 "TaskGroup collects errors into an ExceptionGroup; use except* (3.11) in the test."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-async-taskgroup-fanout": vi_challenge(
            "Fan-out có cấu trúc với TaskGroup",
            "Cài `async def fetch_all(jobs)` với `jobs` là danh sách callable async không tham số:\n\n- chạy TẤT CẢ job đồng thời bên trong một `asyncio.TaskGroup`\n- trả về danh sách tuple `(index, value)` theo thứ tự ĐẦU VÀO\n- nếu job nào raise, fetch_all phải raise (không nuốt)\n\nGhi chú tất định: các job được chấm ngủ với thời lượng so le; tổng thời gian treo tường phải phản ánh tính đồng thời, và kết quả phải về theo thứ tự đầu vào bất kể thứ tự hoàn tất.",
            [("Chạy đồng thời, kết quả theo thứ tự đầu vào", "create_task cả ba trong TaskGroup, rồi đọc .result() theo index sau khi block thoát."),
             ("Lỗi lan truyền từ nhóm", "TaskGroup gom lỗi vào ExceptionGroup; test dùng except* (3.11).")],
        ),
    },
    solutions=[("pa-async-taskgroup-fanout", TG_REF, TG_WRONG)],
)

# ── practice 2: timeouts ─────────────────────────────────────────────────────
TIMEOUT_REF = (
    "import asyncio\n\n\n"
    "async def with_timeout(job, seconds):\n"
    "    '''Run job(); return its value, or the sentinel string 'timeout:<seconds>'\n"
    "    if it exceeds `seconds`.'''\n"
    "    try:\n"
    "        async with asyncio.timeout(seconds):\n"
    "            return await job()\n"
    "    except TimeoutError:\n"
    "        return f'timeout:{seconds}'"
)
TIMEOUT_WRONG = (
    "import asyncio\n\n\n"
    "async def with_timeout(job, seconds):\n"
    "    '''WRONG: awaits the job BEFORE entering the timeout scope —\n"
    "    the job runs unprotected and can never time out.'''\n"
    "    value = await job()\n"
    "    async with asyncio.timeout(seconds):\n"
    "        pass\n"
    "    return value"
)

write_practice(
    MOD, "pa-p5-timeout-practice",
    "Timeout Practice",
    "Bound waiting with asyncio.timeout — and time out for real, not cosmetically.",
    "Luyện Timeout",
    "Giới hạn thời gian chờ bằng asyncio.timeout — và timeout phải thật, không phải đối phó.",
    "cancellation-timeouts", 20, "advanced",
    [
        challenge(
            "pa-async-timeout-bounded",
            "Timeout-bounded job runner",
            "Implement `async def with_timeout(job, seconds)`:\n\n- run the zero-arg async callable `job` under `asyncio.timeout(seconds)`\n- return the job's value when it finishes in time\n- return exactly the string `f'timeout:{seconds}'` when it exceeds the budget",
            "import asyncio\n\n# TODO: with_timeout(job, seconds)",
            [
                ("fast job passes through",
                 "async def quick():\n    await asyncio.sleep(0.01)\n    return 7\n\nloop = asyncio.new_event_loop()\nassert loop.run_until_complete(with_timeout(quick, 1)) == 7\nloop.close()\nprint('ok')",
                 "The timeout context wraps the await of the job itself."),
                ("slow job returns the sentinel",
                 "async def slow():\n    await asyncio.sleep(5)\n    return 'late'\n\nloop = asyncio.new_event_loop()\nassert loop.run_until_complete(with_timeout(slow, 0.05)) == 'timeout:0.05', 'must return the sentinel'\nloop.close()\nprint('ok')",
                 "asyncio.timeout cancels the inner task at the deadline and raises TimeoutError inside the with."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-async-timeout-bounded": vi_challenge(
            "Job runner có giới hạn timeout",
            "Cài `async def with_timeout(job, seconds)`:\n\n- chạy callable async không tham số `job` dưới `asyncio.timeout(seconds)`\n- trả về giá trị của job nếu kịp hoàn tất\n- trả về đúng chuỗi `f'timeout:{seconds}'` nếu vượt ngân sách",
            [("Job nhanh đi xuyên qua", "Context timeout bọc chính await của job."),
             ("Job chậm trả về sentinel", "asyncio.timeout hủy task bên trong khi tới hạn và raise TimeoutError trong with.")],
        ),
    },
    solutions=[("pa-async-timeout-bounded", TIMEOUT_REF, TIMEOUT_WRONG)],
)

# ── practice 3: bounded queue pipeline ───────────────────────────────────────
BQ_REF = (
    "import asyncio\n\n\n"
    "async def pipeline(items, transform, workers=2, maxsize=3):\n"
    "    q = asyncio.Queue(maxsize=maxsize)\n"
    "    out = []\n\n"
    "    async def worker():\n"
    "        while True:\n"
    "            item = await q.get()\n"
    "            try:\n"
    "                out.append(await transform(item))\n"
    "            finally:\n"
    "                q.task_done()\n\n"
    "    tasks = []\n"
    "    for _ in range(workers):\n"
    "        tasks.append(asyncio.create_task(worker()))\n"
    "    for it in items:\n"
    "        await q.put(it)\n"
    "    await q.join()\n"
    "    for t in tasks:\n"
    "        t.cancel()\n"
    "    return sorted(out)"
)
BQ_WRONG = (
    "import asyncio\n\n\n"
    "async def pipeline(items, transform, workers=2, maxsize=3):\n"
    "    q = asyncio.Queue(maxsize=maxsize)\n"
    "    out = []\n\n"
    "    async def worker():\n"
    "        while True:\n"
    "            item = await q.get()\n"
    "            try:\n"
    "                out.append(await transform(item))\n"
    "            finally:\n"
    "                pass  # WRONG: task_done() never called — q.join() waits forever\n\n"
    "    tasks = []\n"
    "    for _ in range(workers):\n"
    "        tasks.append(asyncio.create_task(worker()))\n"
    "    for it in items:\n"
    "        await q.put(it)\n"
    "    await q.join()\n"
    "    for t in tasks:\n"
    "        t.cancel()\n"
    "    return sorted(out)"
)

write_practice(
    MOD, "pa-p5-iterator-practice",
    "Bounded Queue Practice",
    "Async producers, async workers, and a queue that makes the pipeline honest.",
    "Luyện Queue có giới hạn",
    "Producer async, worker async, và một queue buộc pipeline phải trung thực.",
    "async-protocol-patterns", 22, "advanced",
    [
        challenge(
            "pa-async-bounded-pipeline",
            "Bounded async pipeline",
            "Implement `async def pipeline(items, transform, workers=2, maxsize=3)`:\n\n- put all `items` through an `asyncio.Queue(maxsize=maxsize)`\n- `workers` async tasks consume and append `await transform(item)` results\n- the producer must NOT dump everything into the queue at once — with maxsize honored, queue backpressure applies (`await q.put` suspends when full)\n- return `sorted(results)` after `await q.join()`; cancel the workers afterwards",
            "import asyncio\n\n# TODO: pipeline(items, transform, workers=2, maxsize=3)",
            [
                ("processes all items with backpressure safe",
                 "async def dbl(x):\n    await asyncio.sleep(0.005)\n    return x * 2\n\nloop = asyncio.new_event_loop()\nout = loop.run_until_complete(pipeline([3, 1, 2, 5, 4], dbl, workers=2, maxsize=2))\nloop.close()\nassert out == [2, 4, 6, 8, 10], f'out: {out}'\nprint('ok')",
                 "q.join() releases only when every queued item has task_done() called; put() suspends when the bounded queue is full."),
                ("many items through a tiny queue",
                 "async def ident(x):\n    await asyncio.sleep(0.001)\n    return x\n\nloop = asyncio.new_event_loop()\nout = loop.run_until_complete(pipeline(list(range(60)), ident, workers=3, maxsize=2))\nloop.close()\nassert out == list(range(60))\nprint('ok')",
                 "60 items must flow through a maxsize-2 queue without deadlock."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-async-bounded-pipeline": vi_challenge(
            "Pipeline async có giới hạn",
            "Cài `async def pipeline(items, transform, workers=2, maxsize=3)`:\n\n- đưa mọi `items` qua `asyncio.Queue(maxsize=maxsize)`\n- `workers` task async tiêu thụ và append kết quả `await transform(item)`\n- producer KHÔNG được đổ hết vào queue một lúc — với maxsize được tôn trọng, backpressure có tác dụng (`await q.put` treo khi đầy)\n- trả về `sorted(results)` sau `await q.join()`; hủy worker sau đó",
            [("Xử lý hết item, an toàn backpressure", "q.join() chỉ nhả khi mọi item trong queue đã được task_done(); put() treo khi queue có giới hạn đầy."),
             ("60 item chui qua queue tí hon", "60 item phải chảy qua queue maxsize-2 mà không deadlock.")],
        ),
    },
    solutions=[("pa-async-bounded-pipeline", BQ_REF, BQ_WRONG)],
)

# ── practice 4 + project: async service ──────────────────────────────────────
SVC_REF = (
    "import asyncio\n\n\n"
    "class RateLimitedClient:\n"
    "    def __init__(self, max_concurrent=2):\n"
    "        self._sem = asyncio.Semaphore(max_concurrent)\n"
    "        self.in_flight = 0\n\n"
    "    async def request(self, name, delay, fail=False):\n"
    "        async with self._sem:\n"
    "            self.in_flight += 1\n"
    "            try:\n"
    "                await asyncio.sleep(delay)\n"
    "                if fail:\n"
    "                    raise RuntimeError(f'{name} failed')\n"
    "                return f'{name}:ok'\n"
    "            finally:\n"
    "                self.in_flight -= 1\n\n"
    "    async def run_all(self, specs, per_request_timeout=None):\n"
    "        results = [None] * len(specs)\n"
    "        async with asyncio.TaskGroup() as tg:\n"
    "            tasks = []\n"
    "            for i, (name, delay, fail) in enumerate(specs):\n"
    "                coro = self.request(name, delay, fail)\n"
    "                if per_request_timeout is not None:\n"
    "                    coro = self._guarded(coro, per_request_timeout, i, results)\n"
    "                else:\n"
    "                    coro = self._guarded(coro, None, i, results)\n"
    "                tasks.append(tg.create_task(coro))\n"
    "        return results\n\n"
    "    async def _guarded(self, coro, seconds, i, results):\n"
    "        if seconds is None:\n"
    "            results[i] = await coro\n"
    "            return\n"
    "        try:\n"
    "            async with asyncio.timeout(seconds):\n"
    "                results[i] = await coro\n"
    "        except TimeoutError:\n"
    "            results[i] = f'timeout:{seconds}'"
)
SVC_WRONG = (
    "import asyncio\n\n\n"
    "class RateLimitedClient:\n"
    "    def __init__(self, max_concurrent=2):\n"
    "        self._sem = asyncio.Semaphore(max_concurrent)\n"
    "        self.in_flight = 0\n\n"
    "    async def request(self, name, delay, fail=False):\n"
    "        # WRONG: no semaphore around the work — concurrency unbounded,\n"
    "        # and in_flight tracking happens outside any critical section\n"
    "        self.in_flight += 1\n"
    "        await asyncio.sleep(delay)\n"
    "        self.in_flight -= 1\n"
    "        if fail:\n"
    "            raise RuntimeError(f'{name} failed')\n"
    "        return f'{name}:ok'\n\n"
    "    async def run_all(self, specs, per_request_timeout=None):\n"
    "        results = [None] * len(specs)\n"
    "        async with asyncio.TaskGroup() as tg:\n"
    "            for i, (name, delay, fail) in enumerate(specs):\n"
    "                tg.create_task(self.request(name, delay, fail))\n"
    "        return results"
)

write_practice(
    MOD, "pa-p5-service-project",
    "Project: High-Concurrency Async Service",
    "A rate-limited async client: bounded concurrency, per-request timeouts, structured failure propagation.",
    "Project: Async service đồng thời cao",
    "Async client có giới hạn tỉ lệ: concurrency bị chặn, timeout từng request, lỗi lan truyền có cấu trúc.",
    "async-protocol-patterns", 30, "advanced",
    [
        challenge(
            "pa-async-rate-limited-service",
            "RateLimitedClient",
            "Implement `class RateLimitedClient`:\n\n1. `__init__(self, max_concurrent=2)` — create an `asyncio.Saphore`-guarded limit (use `asyncio.Semaphore`) and an `in_flight` counter of requests currently inside the critical section.\n2. `async def request(self, name, delay, fail=False)` — acquires the semaphore, increments `in_flight`, sleeps `delay`, raises `RuntimeError(f'{name} failed')` when `fail=True`, returns `f'{name}:ok'`, and ALWAYS decrements `in_flight` (success, failure, or cancellation).\n3. `async def run_all(self, specs, per_request_timeout=None)` — runs all `(name, delay, fail)` specs concurrently in one TaskGroup; with `per_request_timeout` set, each request is bounded and its slot receives `f'timeout:{per_request_timeout}'` instead of raising.\n\nDeterminism checks: `in_flight` never exceeds `max_concurrent` (sampled via a wrapped sleep), and all results come back positionally.",
            "import asyncio\n\n# TODO: RateLimitedClient",
            [
                ("bounded concurrency with positional results",
                 "loop = asyncio.new_event_loop()\nclient = RateLimitedClient(max_concurrent=2)\npeak = {'n': 0}\norig_sleep = asyncio.sleep\nasync def traced_sleep(d):\n    peak['n'] = max(peak['n'], client.in_flight)\n    await orig_sleep(d)\nasyncio.sleep = traced_sleep\nspecs = [('a', 0.03, False), ('b', 0.02, False), ('c', 0.04, False), ('d', 0.01, False)]\nres = loop.run_until_complete(client.run_all(specs))\nasyncio.sleep = orig_sleep\nloop.close()\nassert res == ['a:ok', 'b:ok', 'c:ok', 'd:ok'], f'res: {res}'\nassert peak['n'] <= 2, f'in_flight exceeded max_concurrent: {peak[\"n\"]}'\nprint('ok')",
                 "Hold the semaphore for the whole body (async with), count in_flight inside it, decrement in finally."),
                ("timeouts replace failures; real failures raise",
                 "loop = asyncio.new_event_loop()\nclient = RateLimitedClient(max_concurrent=1)\nasync def never():\n    await asyncio.sleep(10)\nspecs = [('slow', 0.2, False), ('bad', 0.01, True)]\ntry:\n    res = loop.run_until_complete(client.run_all(specs, per_request_timeout=0.05))\n    got = res\nexcept* RuntimeError:\n    got = 'raised'\nloop.close()\nassert got == ['timeout:0.05', 'timeout:0.05'] or got == 'raised', f'got: {got}'\nprint('ok')",
                 "With per_request_timeout, a slow request returns the timeout sentinel in its slot; failing requests may either raise (TaskGroup) or return their slot value — both accepted for fail=True slots is NOT required; the sentinel applies to timeout only."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-async-rate-limited-service": vi_challenge(
            "RateLimitedClient",
            "Cài `class RateLimitedClient`:\n\n1. `__init__(self, max_concurrent=2)` — tạo giới hạn được bảo vệ bằng `asyncio.Semaphore` và bộ đếm `in_flight` cho các request đang ở trong vùng găng.\n2. `async def request(self, name, delay, fail=False)` — lấy semaphore, tăng `in_flight`, ngủ `delay`, raise `RuntimeError(f'{name} failed')` khi `fail=True`, trả về `f'{name}:ok'`, và LUÔN giảm `in_flight` (thành công, thất bại hay bị hủy).\n3. `async def run_all(self, specs, per_request_timeout=None)` — chạy mọi spec `(name, delay, fail)` đồng thời trong một TaskGroup; khi đặt `per_request_timeout`, mỗi request bị giới hạn và slot của nó nhận `f'timeout:{per_request_timeout}'` thay vì raise.\n\nKiểm tra tất định: `in_flight` không bao giờ vượt `max_concurrent` (đo bằng sleep được bọc), và mọi kết quả về đúng vị trí.",
            [("Concurrency bị chặn, kết quả theo vị trí", "Giữ semaphore cho toàn bộ thân hàm (async with), đếm in_flight bên trong, giảm trong finally."),
             ("Timeout thay thất bại; thất bại thật thì raise", "Có per_request_timeout, request chậm trả về sentinel timeout vào slot của nó; sentinel chỉ áp dụng cho timeout.")],
        ),
    },
    solutions=[("pa-async-rate-limited-service", SVC_REF, SVC_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_REF = (
    "import asyncio\n\n\n"
    "async def fetch_all(jobs):\n"
    "    '''Run zero-arg async jobs with per-job timeout. Returns\n"
    "    [(index, value_or_'timeout:<seconds>')]; a REAL job error still raises.'''\n"
    "    results = [None] * len(jobs)\n"
    "    async with asyncio.TaskGroup() as tg:\n"
    "        for i, job in enumerate(jobs):\n"
    "            async def one(j=job, i=i):\n"
    "                try:\n"
    "                    async with asyncio.timeout(0.05):\n"
    "                        results[i] = (i, await j())\n"
    "                except TimeoutError:\n"
    "                    results[i] = (i, 'timeout:0.05')\n"
    "            tg.create_task(one())\n"
    "    return results"
)
CK_WRONG = (
    "import asyncio\n\n\n"
    "async def fetch_all(jobs):\n"
    "    '''WRONG: catches EVERYTHING including CancelledError raised by the\n"
    "    TaskGroup on sibling failure — breaking structured concurrency and\n"
    "    also masking timeouts with a blanket except.'''\n"
    "    results = [None] * len(jobs)\n"
    "    async with asyncio.TaskGroup() as tg:\n"
    "        for i, job in enumerate(jobs):\n"
    "            async def one(j=job, i=i):\n"
    "                try:\n"
    "                    async with asyncio.timeout(0.05):\n"
    "                        results[i] = (i, await j())\n"
    "                except BaseException:\n"
    "                    results[i] = (i, 'timeout:0.05')\n"
    "            tg.create_task(one())\n"
    "    return results"
)

write_checkpoint(
    MOD, "pa-checkpoint-async",
    "Checkpoint: Structured Async",
    "Per-job timeouts inside a TaskGroup — with a CancelledError-swallowing probe.",
    30,
    """
## Checkpoint — hardened fan-out

Combine the module: `async def fetch_all(jobs)` runs zero-arg async jobs under
a per-job timeout of 0.05s inside ONE TaskGroup:

- success → `(index, value)` in that slot
- job exceeding 0.05s → `(index, 'timeout:0.05')`
- a job raising a REAL error → fetch_all still raises (only timeouts are
  converted)

The wrong-probe implements this with a blanket `except BaseException` — which
also eats CancelledError and masks real errors. Your cleanup discipline is the
graded skill.
""",
    "Checkpoint: Async có cấu trúc",
    "Timeout từng job bên trong TaskGroup — kèm probe nuốt CancelledError.",
    """
## Checkpoint — fan-out bản gia cố

Kết hợp cả module: `async def fetch_all(jobs)` chạy các job async không tham số\ndưới timeout 0.05s cho từng job, bên trong MỘT TaskGroup:

- thành công → `(index, value)` vào slot đó
- job vượt 0.05s → `(index, 'timeout:0.05')`
- job raise lỗi THẬT → fetch_all vẫn raise (chỉ timeout được quy đổi)

Probe phản chủ làm điều này bằng `except BaseException` tràn lan — thứ cũng nuốt\nCancelledError và che mất lỗi thật. Kỷ luật dọn dẹp của bạn là kỹ năng được chấm.
""",
    challenge(
        "pa-checkpoint-async",
        "fetch_all with per-job timeouts",
        "Implement fetch_all per the hardened spec: TaskGroup, per-job asyncio.timeout(0.05), timeout converted to the sentinel string, real errors still raised.",
        "import asyncio\n\n# TODO: fetch_all(jobs)",
        [
            ("timeouts convert, successes pass through",
             "async def quick():\n    await asyncio.sleep(0.005)\n    return 'q'\nasync def slow():\n    await asyncio.sleep(0.5)\n    return 'never'\n\nloop = asyncio.new_event_loop()\nout = loop.run_until_complete(fetch_all([quick, slow, quick]))\nloop.close()\nassert out[0] == (0, 'q') and out[2] == (2, 'q'), f'out: {out}'\nassert out[1] == (1, 'timeout:0.05'), f'out: {out}'\nprint('ok')",
                 "Wrap each job's await in asyncio.timeout(0.05); catch ONLY TimeoutError."),
            ("real errors still raise",
             "async def bad():\n    raise ValueError('real')\n\nloop = asyncio.new_event_loop()\ntry:\n    loop.run_until_complete(fetch_all([bad]))\nexcept* ValueError:\n    pass\nelse:\n    raise AssertionError('real errors must propagate')\nfinally:\n    loop.close()\nprint('ok')",
                 "except BaseException would mask this — catch TimeoutError only."),
        ],
        level="build",
    ),
    vi_challenge(
        "fetch_all với timeout từng job",
        "Cài fetch_all theo đặc tả bản gia cố: TaskGroup, asyncio.timeout(0.05) từng job, timeout quy thành chuỗi sentinel, lỗi thật vẫn raise.",
        [("Timeout quy đổi, thành công đi xuyên qua", "Bọc await của từng job trong asyncio.timeout(0.05); chỉ bắt TimeoutError."),
         ("Lỗi thật vẫn raise", "except BaseException sẽ che mất lỗi này — chỉ bắt TimeoutError.")],
    ),
    solution=CK_REF,
    wrong=CK_WRONG,
)

print("module 5 complete")
