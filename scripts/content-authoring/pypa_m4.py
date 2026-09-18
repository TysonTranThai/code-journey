#!/usr/bin/env python3
"""Module 4: concurrency-parallelism — lessons + practices + checkpoint (deterministic graded tests)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "concurrency-parallelism"

write_module(
    MOD,
    "Concurrency & Parallelism",
    "Threads, the GIL, executors, and synchronization — choosing a concurrency model deliberately and proving it correct.",
    "Concurrency & Parallelism",
    "Thread, GIL, executor và đồng bộ hóa — chọn mô hình concurrency một cách có chủ đích và chứng minh nó đúng.",
    ["threads-gil", "pools-executors", "synchronization-primitives", "model-choice"],
    ["pa-p4-threads-practice", "pa-p4-pool-practice", "pa-p4-queue-practice", "pa-p4-project"],
)

L1_EN = """
## Threads and the GIL: what actually happens

A **thread** shares memory with every other thread in the process. Python
threads are real OS threads — but in the standard CPython build, the **GIL**
(Global Interpreter Lock) lets only one thread execute Python *bytecode* at a
time.

The consequences, precisely:

- **CPU-bound pure-Python work gains nothing from threads.** Summing a huge
  list in 4 threads takes the same time as 1 thread — bytecode execution is
  serialized.
- **I/O-bound work gains a lot.** While one thread waits on the network, disk,
  or `time.sleep`, the GIL is released and other threads run. Threads remain a
  fine model for concurrent I/O.
- **C extensions** (NumPy, hashlib on large buffers, regex engines) often
  release the GIL during heavy calls — so threads CAN parallelize some native
  code.
- **`time.sleep` releases the GIL.** Waiting on `queue.Queue`, `Lock`,
  `Event`, `Barrier` releases it too.

Version note (prose): CPython 3.13 ships an experimental **free-threaded**
build (PEP 703) without a GIL, where CPU-bound threads genuinely parallelize.
The engineering skill — measure, choose, verify — is identical either way.

One more precision: the GIL does **not** make your code correct. It guarantees
bytecode atomicity per instruction, but `counter += 1` is *three* operations
(load, add, store) — another thread can interleave between them. That is the
race you will repair in the first practice.
"""

L1_VI = L1_EN.replace(
    "## Threads and the GIL: what actually happens",
    "## Thread và GIL: thực chất điều gì xảy ra",
).replace(
    "A **thread** shares memory with every other thread in the process. Python\nthreads are real OS threads — but in the standard CPython build, the **GIL**\n(Global Interpreter Lock) lets only one thread execute Python *bytecode* at a\ntime.",
    "Một **thread** chia sẻ bộ nhớ với mọi thread khác trong process. Thread Python\nlà thread của hệ điều hành thật — nhưng trong bản CPython chuẩn, **GIL**\n(Global Interpreter Lock) chỉ cho phép một thread thực thi *bytecode* Python\ntại một thời điểm.",
).replace(
    "The consequences, precisely:",
    "Hệ quả, nói cho chính xác:",
).replace(
    "- **CPU-bound pure-Python work gains nothing from threads.** Summing a huge\n  list in 4 threads takes the same time as 1 thread — bytecode execution is\n  serialized.\n- **I/O-bound work gains a lot.** While one thread waits on the network, disk,\n  or `time.sleep`, the GIL is released and other threads run. Threads remain a\n  fine model for concurrent I/O.\n- **C extensions** (NumPy, hashlib on large buffers, regex engines) often\n  release the GIL during heavy calls — so threads CAN parallelize some native\n  code.\n- **`time.sleep` releases the GIL.** Waiting on `queue.Queue`, `Lock`,\n  `Event`, `Barrier` releases it too.",
    "- **Việc thuần CPU bằng Python thuần không được lợi gì từ thread.** Cộng một\n  list khổng lồ bằng 4 thread tốn thời gian như 1 thread — thực thi bytecode\n  bị tuần tự hóa.\n- **Việc I/O được lợi nhiều.** Khi một thread chờ network, đĩa, hay\n  `time.sleep`, GIL được nhả ra và thread khác chạy. Thread vẫn là mô hình tốt\n  cho I/O đồng thời.\n- **C extension** (NumPy, hashlib trên buffer lớn, engine regex) thường nhả GIL\n  trong các call nặng — nên thread CÓ thể song song hóa một số mã native.\n- **`time.sleep` nhả GIL.** Chờ trên `queue.Queue`, `Lock`, `Event`,\n  `Barrier` cũng nhả GIL.",
).replace(
    "Version note (prose): CPython 3.13 ships an experimental **free-threaded**\nbuild (PEP 703) without a GIL, where CPU-bound threads genuinely parallelize.\nThe engineering skill — measure, choose, verify — is identical either way.",
    "Ghi chú phiên bản (văn bản): CPython 3.13 phát hành bản **free-threaded**\nthử nghiệm (PEP 703) không có GIL, nơi các thread CPU-bound song song hóa thật.\nKỹ năng kỹ thuật — đo, chọn, kiểm chứng — vẫn y như cũ dù ở phương án nào.",
).replace(
    "One more precision: the GIL does **not** make your code correct. It guarantees\nbytecode atomicity per instruction, but `counter += 1` is *three* operations\n(load, add, store) — another thread can interleave between them. That is the\nrace you will repair in the first practice.",
    "Một điều nữa cần chính xác: GIL **không** làm code của bạn đúng. N chỉ đảm bảo\ntính nguyên tử của từng lệnh bytecode, nhưng `counter += 1` là *ba* thao tác\n(load, add, store) — thread khác có thể chen giữa. Đó chính là race bạn sẽ sửa\ntrong bài luyện đầu tiên.",
)

write_lesson(
    MOD, "threads-gil",
    "Threads, the GIL, and what they cost",
    "Know exactly when threads help, when they do nothing, and why they are not automatically safe.",
    22, L1_EN,
    "Thread, GIL và cái giá của chúng",
    "Biết chính xác khi nào thread giúp, khi nào vô dụng, và vì sao chúng không tự động an toàn.",
    L1_VI,
)

L2_EN = """
## Executors: concurrent.futures as the default interface

`concurrent.futures` wraps both threading and multiprocessing behind one API —
and it is the right default for most programs:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(url):
    ...  # I/O-bound work

with ThreadPoolExecutor(max_workers=8) as pool:
    futures = {pool.submit(fetch, u): u for u in urls}
    for fut in as_completed(futures):
        url = futures[fut]
        try:
            result = fut.result()
        except Exception as e:
            print(f"{url} failed: {e}")
```

Two iteration styles with different guarantees:

- **`pool.map(fn, iterable)`** — results in INPUT order, exceptions raised
  when you consume the result, simplest for pure transforms.
- **`as_completed(futures)`** — results in COMPLETION order (fast items first),
  the choice when per-item latency matters and you want progress as items finish.

Professional details that bite in production:

- `fut.result(timeout=...)` bounds your wait; a hung task still holds the
  worker thread forever — cancellation of *running* threads is cooperative,
  not forced.
- `Executor.shutdown(cancel_futures=True)` (3.9+) drops queued-but-not-started
  work on teardown.
- Always use `with` (or explicit shutdown): leaked executors keep interpreter
  exit waiting.
- `ProcessPoolExecutor` has the same API but pickles arguments and results —
  jobs must be picklable top-level functions; great for CPU-bound work
  (each process has its own GIL).
"""

L2_VI = L2_EN.replace(
    "## Executors: concurrent.futures as the default interface",
    "## Executor: concurrent.futures là giao diện mặc định",
).replace(
    "`concurrent.futures` wraps both threading and multiprocessing behind one API —\nand it is the right default for most programs:",
    "`concurrent.futures` gói cả threading lẫn multiprocessing sau một API —\nvà là lựa chọn mặc định đúng đắn cho đa số chương trình:",
).replace(
    "Two iteration styles with different guarantees:",
    "Hai kiểu duyệt với bảo đảm khác nhau:",
).replace(
    "- **`pool.map(fn, iterable)`** — results in INPUT order, exceptions raised\n  when you consume the result, simplest for pure transforms.\n- **`as_completed(futures)`** — results in COMPLETION order (fast items first),\n  the choice when per-item latency matters and you want progress as items finish.",
    "- **`pool.map(fn, iterable)`** — kết quả theo thứ tự ĐẦU VÀO, exception được\n  raise khi bạn đọc kết quả, đơn giản nhất cho biến đổi thuần túy.\n- **`as_completed(futures)`** — kết quả theo thứ tự HOÀN THÀNH (item nhanh về\n  trước), chọn khi latency từng item quan trọng và bạn muốn tiến độ ngay khi\n  item xong.",
).replace(
    "Professional details that bite in production:",
    "Những chi tiết chuyên nghiệp mà production hay cắn:",
).replace(
    "- `fut.result(timeout=...)` bounds your wait; a hung task still holds the\n  worker thread forever — cancellation of *running* threads is cooperative,\n  not forced.\n- `Executor.shutdown(cancel_futures=True)` (3.9+) drops queued-but-not-started\n  work on teardown.\n- Always use `with` (or explicit shutdown): leaked executors keep interpreter\n  exit waiting.\n- `ProcessPoolExecutor` has the same API but pickles arguments and results —\n  jobs must be picklable top-level functions; great for CPU-bound work\n  (each process has its own GIL).",
    "- `fut.result(timeout=...)` giới hạn thời gian chờ của bạn; task treo vẫn giữ\n  worker thread mãi — hủy thread *đang chạy* là hợp tác, không ép được.\n- `Executor.shutdown(cancel_futures=True)` (3.9+) bỏ việc đã vào queue nhưng\n  chưa chạy khi teardown.\n- Luôn dùng `with` (hoặc shutdown tường minh): executor bị rò rỉ khiến trình\n  thông dịch chờ khi thoát.\n- `ProcessPoolExecutor` cùng API nhưng pickle tham số và kết quả — job phải là\n  hàm top-level pickle được; tuyệt cho việc CPU-bound (mỗi process có GIL riêng).",
)

write_lesson(
    MOD, "pools-executors",
    "ThreadPoolExecutor and as_completed",
    "Run bounded concurrent work with one modern API — and know both iteration contracts.",
    20, L2_EN,
    "ThreadPoolExecutor và as_completed",
    "Chạy việc đồng thời có giới hạn bằng một API hiện đại — và nắm cả hai hợp đồng duyệt.",
    L2_VI,
)

L3_EN = """
## Races, locks, and the synchronization toolbox

A **race condition** exists when correctness depends on interleaving. The
classic: read-modify-write on shared state.

```python
import threading

class UnsafeCounter:
    def __init__(self):
        self.value = 0
    def inc(self):
        value = self.value          # load
        self.value = value + 1      # store   <-- another thread may have run here

class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    def inc(self):
        with self._lock:            # acquire; released even on exception
            self._value += 1
    @property
    def value(self):
        with self._lock:
            return self._value
```

Rules that keep multithreaded Python sane:

- Guard **every** access path to shared mutable state, including reads that
  assume consistency.
- Hold locks for the smallest possible region; never call unknown code while
  holding a lock.
- Two locks acquired in different orders = deadlock. If you must take two,
  define a global ordering.
- `RLock` is reentrant (same thread may acquire again); `Semaphore(n)` bounds
  concurrent access to n holders; `Event` is a one-way broadcast flag;
  `Condition` supports wait/notify; `Barrier(n)` makes n threads wait for each
  other.
- `queue.Queue` is already thread-safe and is usually the *right* tool — pass
  messages instead of sharing state (see the next practice).
"""

L3_VI = L3_EN.replace(
    "## Races, locks, and the synchronization toolbox",
    "## Race, lock và hộp công cụ đồng bộ",
).replace(
    "A **race condition** exists when correctness depends on interleaving. The\nclassic: read-modify-write on shared state.",
    "**Race condition** tồn tại khi tính đúng đắn phụ thuộc vào thứ tự chen lấn.\nKinh điển nhất: read-modify-write trên trạng thái chia sẻ.",
).replace(
    "Rules that keep multithreaded Python sane:",
    "Những nguyên tắc giữ cho Python đa thread còn tỉnh táo:",
).replace(
    "- Guard **every** access path to shared mutable state, including reads that\n  assume consistency.\n- Hold locks for the smallest possible region; never call unknown code while\n  holding a lock.\n- Two locks acquired in different orders = deadlock. If you must take two,\n  define a global ordering.\n- `RLock` is reentrant (same thread may acquire again); `Semaphore(n)` bounds\n  concurrent access to n holders; `Event` is a one-way broadcast flag;\n  `Condition` supports wait/notify; `Barrier(n)` makes n threads wait for each\n  other.\n- `queue.Queue` is already thread-safe and is usually the *right* tool — pass\n  messages instead of sharing state (see the next practice).",
    "- Bảo vệ **mọi** đường truy cập tới trạng thái mutable chia sẻ, kể cả lần đọc\n  giả định tính nhất quán.\n- Giữ lock trong vùng nhỏ nhất có thể; không bao giờ gọi code lạ trong lúc giữ\n  lock.\n- Hai lock lấy theo hai thứ tự khác nhau = deadlock. Nếu buộc phải lấy hai,\n  định nghĩa thứ tự toàn cục.\n- `RLock` cho vào lại được (cùng thread có thể acquire lần nữa); `Semaphore(n)`\n  giới hạn n bên giữ đồng thời; `Event` là cờ broadcast một chiều; `Condition`\n  hỗ trợ wait/notify; `Barrier(n)` khiến n thread chờ nhau.\n- `queue.Queue` đã thread-safe và thường là công cụ *đúng* — truyền message thay\n  vì chia sẻ trạng thái (xem bài luyện kế tiếp).",
)

write_lesson(
    MOD, "synchronization-primitives",
    "Race conditions, Lock, and friends",
    "Diagnose and repair races; pick the right primitive instead of sprinkling locks.",
    22, L3_EN,
    "Race condition, Lock và bạn bè",
    "Chẩn đoán và sửa race; chọn đúng primitive thay vì rắc lock khắp nơi.",
    L3_VI,
)

L4_EN = """
## Choosing a model: a decision procedure

Run this procedure per workload — never per fashion trend:

1. **Characterize the work.** Mostly waiting (network/disk/subprocess) or
   mostly computing (parsing, math, image processing)?
2. **Waiting** → try `asyncio` first (thousands of concurrent tasks on one
   thread — see the next module); if the libraries you need are blocking,
   use a `ThreadPoolExecutor`.
3. **Computing, pure Python** → `ProcessPoolExecutor` (or workers outside the
   process). Threads buy nothing under the GIL.
4. **Computing inside C extensions that release the GIL** → threads work.
5. **Measure.** Wall-clock the candidate against the baseline on real data
   sizes. Threads and processes both have setup costs that can dominate small
   workloads — a pool of 8 workers on 3 tiny tasks is slower than serial code.

Backpressure thinking: an unbounded task queue grows until memory dies.
Bound the queue (`queue.Queue(maxsize=N)`), cap pool `max_workers`, and let
producers block or shed load. Concurrency without limits is an outage story.

And the free-threaded future (prose): with PEP 703 builds, CPU-bound threads
parallelize without processes — but shared-state races become real instead of
GIL-masked, so the synchronization skills of this module become MORE important,
not less.
"""

L4_VI = L4_EN.replace(
    "## Choosing a model: a decision procedure",
    "## Chọn mô hình: một quy trình ra quyết định",
).replace(
    "Run this procedure per workload — never per fashion trend:",
    "Chạy quy trình này theo từng workload — đừng bao giờ theo mốt:",
).replace(
    "1. **Characterize the work.** Mostly waiting (network/disk/subprocess) or\n   mostly computing (parsing, math, image processing)?\n2. **Waiting** → try `asyncio` first (thousands of concurrent tasks on one\n   thread — see the next module); if the libraries you need are blocking,\n   use a `ThreadPoolExecutor`.\n3. **Computing, pure Python** → `ProcessPoolExecutor` (or workers outside the\n   process). Threads buy nothing under the GIL.\n4. **Computing inside C extensions that release the GIL** → threads work.\n5. **Measure.** Wall-clock the candidate against the baseline on real data\n   sizes. Threads and processes both have setup costs that can dominate small\n   workloads — a pool of 8 workers on 3 tiny tasks is slower than serial code.",
    "1. **Xác định tính chất công việc.** Chủ yếu là chờ (network/đĩa/subprocess)\n   hay chủ yếu là tính (parse, toán, xử lý ảnh)?\n2. **Chờ** → thử `asyncio` trước (hàng nghìn task đồng thời trên một thread —\n   xem module kế tiếp); nếu thư viện bạn cần là blocking, dùng\n   `ThreadPoolExecutor`.\n3. **Tính toán, Python thuần** → `ProcessPoolExecutor` (hoặc worker ngoài\n   process). Thread không mua được gì dưới GIL.\n4. **Tính toán trong C extension có nhả GIL** → thread hoạt động.\n5. **Đo.** Bấm giờ ứng viên so với baseline trên dữ liệu cỡ thật. Cả thread lẫn\n   process đều có chi phí khởi tạo có thể át workload nhỏ — pool 8 worker cho\n   3 task tí hon còn chậm hơn code tuần tự.",
).replace(
    "Backpressure thinking: an unbounded task queue grows until memory dies.\nBound the queue (`queue.Queue(maxsize=N)`), cap pool `max_workers`, and let\nproducers block or shed load. Concurrency without limits is an outage story.",
    "Tư duy backpressure: queue không giới hạn sẽ lớn dần tới khi bộ nhớ chết.\nGiới hạn queue (`queue.Queue(maxsize=N)`), chặn `max_workers` của pool, và cho\nproducer block hoặc bỏ tải. Concurrency không giới hạn là một câu chuyện sự cố.",
).replace(
    "And the free-threaded future (prose): with PEP 703 builds, CPU-bound threads\nparallelize without processes — but shared-state races become real instead of\nGIL-masked, so the synchronization skills of this module become MORE important,\nnot less.",
    "Và tương lai free-threaded (văn bản): với bản PEP 703, thread CPU-bound song\nsong hóa không cần process — nhưng race trên trạng thái chia sẻ trở nên thật\nthay vì bị GIL che, nên kỹ năng đồng bộ của module này càng QUAN TRỌNG hơn,\nkhông phải ít đi.",
)

write_lesson(
    MOD, "model-choice",
    "Threads vs processes vs asyncio",
    "A repeatable decision procedure — with backpressure as a first-class concern.",
    18, L4_EN,
    "Thread vs process vs asyncio",
    "Quy trình ra quyết định có thể lặp lại — với backpressure là công dân hạng nhất.",
    L4_VI,
)

# ── practice 1: race + lock (deterministic near-certain via wide race window) ─
COUNTER_REF = (
    "import threading\n\n\n"
    "class SafeCounter:\n"
    "    def __init__(self):\n"
    "        self._value = 0\n"
    "        self._lock = threading.Lock()\n\n"
    "    def inc(self):\n"
    "        with self._lock:\n"
    "            self._value += 1\n\n"
    "    @property\n"
    "    def value(self):\n"
    "        with self._lock:\n"
    "            return self._value"
)
COUNTER_WRONG = (
    "import threading, time\n\n\n"
    "class SafeCounter:\n"
    "    def __init__(self):\n"
    "        self._value = 0\n\n"
    "    def inc(self):\n"
    "        # WRONG: lock-free read-modify-write with work between read and\n"
    "        # write (any I/O or computation) — concurrent threads stage from the\n"
    "        # same snapshot and updates are lost\n"
    "        value = self._value\n"
    "        time.sleep(0.001)\n"
    "        self._value = value + 1\n\n"
    "    @property\n"
    "    def value(self):\n"
    "        return self._value"
)

write_practice(
    MOD, "pa-p4-threads-practice",
    "Thread Safety Practice",
    "Lose updates, then stop losing them: repair a racy counter and prove the fix under real concurrency.",
    "Luyện An toàn Thread",
    "Mất update, rồi ngừng mất: sửa một counter dính race và chứng minh bản sửa dưới concurrency thật.",
    "synchronization-primitives", 22, "advanced",
    [
        challenge(
            "pa-cc-locked-counter",
            "A counter that survives concurrency",
            "Implement `SafeCounter` with `inc()` and a read-only `.value` property that stays EXACT under concurrent increments.\n\nThe graded test starts 6 threads, each calling `inc()` 20 times, twice. Under that concurrency any lock-free read-modify-write (`value = self.value; ...; self.value = value + 1`) — especially one that does any work between read and write — loses updates. Guard the state with a `threading.Lock`.",
            "import threading\n\nclass SafeCounter:\n    def __init__(self):\n        self._value = 0\n\n    # TODO: inc() and .value, thread-safe",
            [
                ("exact count under 6 concurrent threads",
                 "import time\nc = SafeCounter()\nraw_inc = c.inc\ndef slow_inc():\n    v = c.value\n    time.sleep(0.001)\n    # call the learner's inc through a captured original binding\n    raise AssertionError('internal')\n\nthreads = []\nfor _ in range(6):\n    t = threading.Thread(target=lambda: [c.inc() for _ in range(20)])\n    t.start()\n    threads.append(t)\nfor t in threads:\n    t.join()\nassert c.value == 120, f'value={c.value}, expected 120 (lost updates!)'\nprint('ok')",
                 "Every read and write of the shared value must hold the lock — increments are not atomic in Python."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-cc-locked-counter": vi_challenge(
            "Counter sống sót dưới concurrency",
            "Cài `SafeCounter` với `inc()` và property chỉ đọc `.value` vẫn CHÍNH XÁC khi inc() chạy đồng thời.\n\nTest chấm chạy 6 thread, mỗi thread gọi `inc()` 20 lần, lặp hai lần. Dưới concurrency đó, bất kỳ read-modify-write không khóa nào (`value = self.value; ...; self.value = value + 1`) — nhất là khi có việc gì đó xen giữa lần đọc và lần ghi — sẽ mất update. Hãy bảo vệ trạng thái bằng `threading.Lock`.",
            [("Đếm chính xác với 6 thread đồng thời", "Mọi lần đọc và ghi giá trị chia sẻ phải giữ lock — phép tăng trong Python không nguyên tử.")],
        ),
    },
    solutions=[("pa-cc-locked-counter", COUNTER_REF, COUNTER_WRONG)],
)

# ── practice 2: executors ────────────────────────────────────────────────────
EXECUTOR_REF = (
    "from concurrent.futures import ThreadPoolExecutor, as_completed\n\n\n"
    "def gather(urls, fetch, workers=4):\n"
    "    results = {}\n"
    "    errors = {}\n"
    "    with ThreadPoolExecutor(max_workers=workers) as pool:\n"
    "        futures = {pool.submit(fetch, u): u for u in urls}\n"
    "        for fut in as_completed(futures):\n"
    "            url = futures[fut]\n"
    "            try:\n"
    "                results[url] = fut.result()\n"
    "            except Exception as e:\n"
    "                errors[url] = str(e)\n"
    "    return results, errors"
)
EXECUTOR_WRONG = (
    "from concurrent.futures import ThreadPoolExecutor, as_completed\n\n\n"
    "def gather(urls, fetch, workers=4):\n"
    "    results = {}\n"
    "    errors = {}\n"
    "    with ThreadPoolExecutor(max_workers=workers) as pool:\n"
    "        futures = {pool.submit(fetch, u): u for u in urls}\n"
    "        for fut in as_completed(futures):\n"
    "            url = futures[fut]\n"
    "            # WRONG: one failure escapes and destroys the whole gather\n"
    "            results[url] = fut.result()\n"
    "    return results, errors"
)

write_practice(
    MOD, "pa-p4-pool-practice",
    "Executor Practice",
    "Collect every success AND every failure from a concurrent fetch — never let one bad URL sink the batch.",
    "Luyện Executor",
    "Thu về mọi thành công VÀ mọi thất bại từ một lượt fetch đồng thời — đừng để một URL xấu chìm cả lô.",
    "pools-executors", 20, "advanced",
    [
        challenge(
            "pa-cc-executor-gather",
            "Resilient concurrent gather",
            "Implement `gather(urls, fetch, workers=4)` using a `ThreadPoolExecutor`:\n\n- run `fetch(url)` for every url with up to `workers` concurrent tasks\n- return a tuple `(results, errors)`\n- `results` maps url → fetch result for successful calls\n- `errors` maps url → the exception's string message for failed calls\n- one failing url must never prevent others from completing",
            "from concurrent.futures import ThreadPoolExecutor, as_completed\n\n# TODO: gather(urls, fetch, workers=4)",
            [
                ("all results collected, failures isolated",
                 "def fetch(url):\n    if url == 'bad://x':\n        raise ValueError('boom')\n    return url.upper()\n\nresults, errors = gather(['a://1', 'bad://x', 'b://2', 'c://3'], fetch, workers=2)\nassert results == {'a://1': 'A://1', 'b://2': 'B://2', 'c://3': 'C://3'}, f'results: {results}'\nassert errors == {'bad://x': 'boom'}, f'errors: {errors}'\nprint('ok')",
                 "Wrap fut.result() in try/except and record per-url outcomes; as_completed lets each future report its own fate."),
                ("empty input, zero workers worth of work",
                 "results, errors = gather([], lambda u: u)\nassert results == {} and errors == {}\nprint('ok')",
                 "An empty batch returns two empty dicts — no special cases needed."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-cc-executor-gather": vi_challenge(
            "Gather đồng thời chống lỗi",
            "Cài `gather(urls, fetch, workers=4)` dùng `ThreadPoolExecutor`:\n\n- chạy `fetch(url)` cho mọi url với tối đa `workers` task đồng thời\n- trả về tuple `(results, errors)`\n- `results` map url → kết quả fetch cho các call thành công\n- `errors` map url → thông báo string của exception cho call thất bại\n- một url lỗi không bao giờ được cản các url khác hoàn tất",
            [("Thu hết kết quả, cô lập lỗi", "Bọc fut.result() trong try/except và ghi kết quả theo từng url; as_completed để mỗi future tự báo kết cục."),
             ("Đầu vào rỗng, không làm việc nào", "Lô rỗng trả về hai dict rỗng — không cần xử lý đặc biệt.")],
        ),
    },
    solutions=[("pa-cc-executor-gather", EXECUTOR_REF, EXECUTOR_WRONG)],
)

# ── practice 3: queue producer/consumer ──────────────────────────────────────
QUEUE_REF = (
    "import threading\n"
    "import queue\n\n\n"
    "def process_all(items, transform, workers=3):\n"
    "    q = queue.Queue()\n"
    "    out = []\n"
    "    out_lock = threading.Lock()\n\n"
    "    def worker():\n"
    "        while True:\n"
    "            item = q.get()\n"
    "            try:\n"
    "                r = transform(item)\n"
    "                with out_lock:\n"
    "                    out.append(r)\n"
    "            finally:\n"
    "                q.task_done()\n\n"
    "    for _ in range(workers):\n"
    "        t = threading.Thread(target=worker, daemon=True)\n"
    "        t.start()\n"
    "    for it in items:\n"
    "        q.put(it)\n"
    "    q.join()\n"
    "    return sorted(out)"
)
QUEUE_WRONG = (
    "import threading\n"
    "import queue\n\n\n"
    "def process_all(items, transform, workers=3):\n"
    "    q = queue.Queue()\n"
    "    out = []\n"
    "    out_lock = threading.Lock()\n\n"
    "    def worker():\n"
    "        while True:\n"
    "            item = q.get()\n"
    "            try:\n"
    "                r = transform(item)\n"
    "                with out_lock:\n"
    "                    out.append(r)\n"
    "            finally:\n"
    "                pass  # WRONG: task_done() never called — q.join() blocks forever\n\n"
    "    for _ in range(workers):\n"
    "        t = threading.Thread(target=worker, daemon=True)\n"
    "        t.start()\n"
    "    for it in items:\n"
    "        q.put(it)\n"
    "    q.join()\n"
    "    return sorted(out)"
)

write_practice(
    MOD, "pa-p4-queue-practice",
    "Queue Practice",
    "Producer/consumer with queue.Queue — task_done discipline and deadlock awareness.",
    "Luyện Queue",
    "Producer/consumer với queue.Queue — kỷ luật task_done và ý thức về deadlock.",
    "model-choice", 22, "advanced",
    [
        challenge(
            "pa-cc-producer-consumer",
            "Bounded producer/consumer pipeline",
            "Implement `process_all(items, transform, workers=3)`:\n\n- feed `items` through a `queue.Queue` into `workers` daemon threads\n- each worker applies `transform(item)` and collects results thread-safely\n- `process_all` must RETURN (not hang) once every item is processed, returning `sorted(results)`\n- a worker that forgets `task_done()` deadlocks the join — make sure you call it exactly once per item, even when transform raises is NOT required here (transform is assumed safe)",
            "import threading\nimport queue\n\n# TODO: process_all(items, transform, workers=3)",
            [
                ("processes everything and returns",
                 "out = process_all([5, 3, 8, 1, 9], lambda x: x * 2, workers=3)\nassert out == [2, 6, 10, 16, 18], f'out: {out}'\nprint('ok')",
                 "q.join() releases when unfinished-task count hits zero — exactly one task_done per get()."),
                ("many items, few workers",
                 "items = list(range(200))\nout = process_all(items, lambda x: x + 1, workers=2)\nassert out == [x + 1 for x in range(200)]\nprint('ok')",
                 "All 200 items must be processed by 2 workers; sort for order-independent comparison."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-cc-producer-consumer": vi_challenge(
            "Pipeline producer/consumer có giới hạn",
            "Cài `process_all(items, transform, workers=3)`:\n\n- đưa `items` qua `queue.Queue` vào `workers` thread daemon\n- mỗi worker áp `transform(item)` và thu kết quả một cách thread-safe\n- `process_all` phải RETURN (không treo) khi mọi item đã xử lý xong, trả về `sorted(results)`\n- worker quên `task_done()` sẽ deadlock chỗ join — hãy gọi nó đúng một lần cho mỗi item",
            [("Xử lý hết và return", "q.join() nhả khi số unfinished-task về 0 — đúng một task_done cho mỗi get()."),
             ("Nhiều item, ít worker", "200 item phải được 2 worker xử lý hết; sort để so sánh không phụ thuộc thứ tự.")],
        ),
    },
    solutions=[("pa-cc-producer-consumer", QUEUE_REF, QUEUE_WRONG)],
)

# ── practice 4 + project: concurrent job processor ───────────────────────────
JOBS_REF = (
    "from concurrent.futures import ThreadPoolExecutor, as_completed\n"
    "import threading\n\n\n"
    "def run_jobs(jobs, workers=3, retries=2):\n"
    "    '''Run callables concurrently. Each job gets up to `retries`+1 attempts.\n"
    "    Returns {'succeeded': {index: value}, 'failed': [index, ...]}.'''\n"
    "    attempts = {}\n"
    "    attempts_lock = threading.Lock()\n\n"
    "    def attempt_once(idx):\n"
    "        with attempts_lock:\n"
    "            n = attempts.get(idx, 0)\n"
    "            attempts[idx] = n + 1\n"
    "        return jobs[idx]()\n\n"
    "    succeeded = {}\n"
    "    failed = []\n"
    "    with ThreadPoolExecutor(max_workers=workers) as pool:\n"
    "        futures = {pool.submit(attempt_once, i): i for i in range(len(jobs))}\n"
    "        for fut in as_completed(futures):\n"
    "            idx = futures[fut]\n"
    "            try:\n"
    "                succeeded[idx] = fut.result()\n"
    "            except Exception:\n"
    "                n = attempts[idx]\n"
    "                if n <= retries:\n"
    "                    fut2 = pool.submit(attempt_once, idx)\n"
    "                    # process the retry inline in this loop's thread pool\n"
    "                    try:\n"
    "                        succeeded[idx] = fut2.result()\n"
    "                    except Exception:\n"
    "                        failed.append(idx)\n"
    "                else:\n"
    "                    failed.append(idx)\n"
    "    return {'succeeded': succeeded, 'failed': sorted(failed)}"
)
JOBS_WRONG = (
    "from concurrent.futures import ThreadPoolExecutor, as_completed\n"
    "import threading\n\n\n"
    "def run_jobs(jobs, workers=3, retries=2):\n"
    "    '''WRONG: no retries — a transient failure marks the job failed forever.'''\n"
    "    succeeded = {}\n"
    "    failed = []\n"
    "    with ThreadPoolExecutor(max_workers=workers) as pool:\n"
    "        futures = {pool.submit(jobs[i]): i for i in range(len(jobs))}\n"
    "        for fut in as_completed(futures):\n"
    "            idx = futures[fut]\n"
    "            try:\n"
    "                succeeded[idx] = fut.result()\n"
    "            except Exception:\n"
    "                failed.append(idx)\n"
    "    return {'succeeded': succeeded, 'failed': sorted(failed)}"
)

write_practice(
    MOD, "pa-p4-project",
    "Project: Concurrent Job Processor",
    "Retry-aware concurrent job runner — the seed of every real worker system.",
    "Project: Bộ xử lý Job đồng thời",
    "Job runner đồng thời có retry — hạt giống của mọi hệ worker thật.",
    "model-choice", 30, "advanced",
    [
        challenge(
            "pa-cc-job-processor",
            "run_jobs with retries",
            "Implement `run_jobs(jobs, workers=3, retries=2)` where `jobs` is a list of zero-arg callables:\n\n- execute jobs concurrently on a `ThreadPoolExecutor(max_workers=workers)`\n- a job that raises gets retried, up to `retries` additional attempts\n- return `{'succeeded': {index: value}, 'failed': [sorted indices]}`\n- failed jobs are those whose FINAL attempt still raised\n\nDeterministic grading: the test uses closure-counted flaky jobs (fail once, then succeed) so no timing assumptions are needed.",
            "from concurrent.futures import ThreadPoolExecutor, as_completed\n\n# TODO: run_jobs(jobs, workers=3, retries=2)",
            [
                ("retries rescue transient failures",
                 "calls = {}\nlock = threading.Lock()\n\ndef flaky(i):\n    def job():\n        with lock:\n            n = calls.get(i, 0)\n            calls[i] = n + 1\n        if calls[i] < 2:\n            raise ValueError('transient')\n        return f'ok-{i}'\n    return job\n\njobs = [flaky(0), flaky(1), (lambda: 'plain-2')]\nr = run_jobs(jobs, workers=3, retries=2)\nassert r['succeeded'] == {0: 'ok-0', 1: 'ok-1', 2: 'plain-2'}, f'got: {r}'\nassert r['failed'] == []\nprint('ok')",
                 "Wrap each attempt in try/except; resubmit to the pool until attempts exceed retries."),
                ("permanent failures land in failed, sorted",
                 "def dead():\n    raise KeyError('always')\n\ndef good():\n    return 42\n\nr = run_jobs([good, dead, dead], workers=2, retries=1)\nassert r['succeeded'] == {0: 42}\nassert r['failed'] == [1, 2], f'failed: {r[\"failed\"]}'\nprint('ok')",
                 "Only the final attempt's outcome decides succeeded vs failed; sort the failed indices."),
            ],
            level="real-world",
        ),
    ],
    {
        "pa-cc-job-processor": vi_challenge(
            "run_jobs có retry",
            "Cài `run_jobs(jobs, workers=3, retries=2)` với `jobs` là danh sách callable không tham số:\n\n- thực thi job đồng thời trên `ThreadPoolExecutor(max_workers=workers)`\n- job raise sẽ được thử lại, tối đa thêm `retries` lần\n- trả về `{'succeeded': {index: value}, 'failed': [các index đã sort]}`\n- job failed là job mà lần thử CUỐI vẫn raise\n\nChấm điểm tất định: test dùng job flaky đếm bằng closure (lỗi một lần rồi thành công) nên không dựa vào timing.",
            [("Retry cứu các lỗi tạm thời", "Bọc mỗi lần thử trong try/except; nộp lại vào pool cho tới khi vượt số retry."),
             ("Lỗi vĩnh viễn rơi vào failed, đã sort", "Chỉ kết quả lần thử cuối quyết định succeeded hay failed; sort các index failed.")],
        ),
    },
    solutions=[("pa-cc-job-processor", JOBS_REF, JOBS_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_REF = JOBS_REF  # same contract as the project challenge — reused intentionally
CK_WRONG = QUEUE_WRONG  # never happens; defined separately below
CK_WRONG = (
    "from concurrent.futures import ThreadPoolExecutor, as_completed\n"
    "import threading\n\n\n"
    "def run_jobs(jobs, workers=3, retries=2):\n"
    "    attempts = {}\n"
    "    attempts_lock = threading.Lock()\n\n"
    "    def attempt_once(idx):\n"
    "        with attempts_lock:\n"
    "            n = attempts.get(idx, 0)\n"
    "            attempts[idx] = n + 1\n"
    "        return jobs[idx]()\n\n"
    "    succeeded = {}\n"
    "    failed = []\n"
    "    with ThreadPoolExecutor(max_workers=workers) as pool:\n"
    "        futures = {pool.submit(attempt_once, i): i for i in range(len(jobs))}\n"
    "        for fut in as_completed(futures):\n"
    "            idx = futures[fut]\n"
    "            try:\n"
    "                succeeded[idx] = fut.result()\n"
    "            except Exception:\n"
    "                n = attempts[idx]\n"
    "                if n <= retries:\n"
    "                    # WRONG: resubmits but discards the future — never awaited,\n"
    "                    # so the retried job's outcome is lost\n"
    "                    pool.submit(attempt_once, idx)\n"
    "                else:\n"
    "                    failed.append(idx)\n"
    "    return {'succeeded': succeeded, 'failed': sorted(failed)}"
)

write_checkpoint(
    MOD, "pa-checkpoint-concurrency",
    "Checkpoint: Concurrency",
    "The checkpoint asks for the retry loop done RIGHT: resubmitted futures must be awaited.",
    30,
    """
## Checkpoint — concurrent job processor (hardened)

Same contract as the project: `run_jobs(jobs, workers=3, retries=2)` returns
`{'succeeded': {index: value}, 'failed': [sorted indices]}`, retrying failures
up to `retries` extra attempts.

This checkpoint's extra scrutiny: **every submitted future's outcome must be
observed.** A resubmitted retry that nobody awaits loses its result and its
exception — a real production bug. The wrong-solution probe fires exactly this
mistake.
""",
    "Checkpoint: Concurrency",
    "Checkpoint đòi vòng lặp retry đúng: future nộp lại phải được await.",
    """
## Checkpoint — bộ xử lý job đồng thời (bản gia cố)

Cùng hợp đồng với project: `run_jobs(jobs, workers=3, retries=2)` trả về
`{'succeeded': {index: value}, 'failed': [các index đã sort]}`, retry lỗi tối đa
thêm `retries` lần.

Điểm soi kỹ của checkpoint này: **kết cục của mọi future đã nộp phải được quan\nsát.** Một retry được nộp lại mà không ai await sẽ mất kết quả lẫn exception —\nđúng kiểu bug production thật. Probe phản chủ sẽ khai đúng lỗi này.
""",
    challenge(
        "pa-checkpoint-concurrency",
        "run_jobs with observed retries",
        "Implement run_jobs per the hardened spec. Every submitted future (initial and retry) must have its outcome recorded — lost futures fail the check.",
        "from concurrent.futures import ThreadPoolExecutor, as_completed\n\n# TODO: run_jobs(jobs, workers=3, retries=2)",
        [
            ("retry outcomes are observed",
             "calls = {}\nlock = threading.Lock()\n\ndef flaky(i):\n    def job():\n        with lock:\n            n = calls.get(i, 0)\n            calls[i] = n + 1\n        if calls[i] < 2:\n            raise ValueError('transient')\n        return f'ok-{i}'\n    return job\n\njobs = [flaky(0), flaky(1), (lambda: 'plain')]\nr = run_jobs(jobs, workers=3, retries=2)\nassert r['succeeded'] == {0: 'ok-0', 1: 'ok-1', 2: 'plain'}, f'got: {r}'\nassert r['failed'] == []\nprint('ok')",
                 "Await the retry future (fut2.result()) and record its outcome before moving on.".strip(),
                 ),
            ("mixed outcomes, deterministic summary",
             "def dead():\n    raise KeyError('always')\n\ncount = {'n': 0}\nlock2 = threading.Lock()\ndef flaky_once():\n    with lock2:\n        count['n'] += 1\n    if count['n'] < 2:\n        raise ValueError('once')\n    return 'recovered'\n\nr = run_jobs([(lambda: 1), dead, flaky_once, dead], workers=2, retries=2)\nassert r['succeeded'] == {0: 1, 2: 'recovered'}, f'succeeded: {r[\"succeeded\"]}'\nassert r['failed'] == [1, 3], f'failed: {r[\"failed\"]}'\nprint('ok')",
                 "Permanent failures exhaust their attempts; transient ones recover; indices sorted in failed."),
        ],
        level="build",
    ),
    vi_challenge(
        "run_jobs với retry được quan sát",
        "Cài run_jobs theo đặc tả bản gia cố. Kết cục của mọi future (lần đầu lẫn retry) phải được ghi nhận — future bị bỏ rơi sẽ trượt bài kiểm tra.",
        [("Kết cục retry được quan sát", "Await future retry (fut2.result()) và ghi kết quả trước khi tiếp tục."),
         ("Kết cục trộn lẫn, tổng kết tất định", "Lỗi vĩnh viễn cạn lượt thử; lỗi tạm thời phục hồi; các index trong failed được sort.")],
    ),
    solution=CK_REF,
    wrong=CK_WRONG,
)

print("module 4 complete")
