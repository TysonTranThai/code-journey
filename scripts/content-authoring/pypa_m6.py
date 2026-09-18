#!/usr/bin/env python3
"""Module 6: performance-engineering — lessons + practices + checkpoint (deterministic grading)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "performance-engineering"

write_module(
    MOD,
    "Performance Engineering",
    "Measure → profile → understand → optimize → verify. Call counts, algorithmic complexity, memoization, and generator streaming — with evidence, not folklore.",
    "Kỹ thuật hiệu năng",
    "Đo → profile → hiểu → tối ưu → kiểm chứng. Số lần gọi, độ phức tạp thuật toán, memoization, generator streaming — bằng bằng chứng, không phải tín ngưỡng.",
    ["measure-first", "profiling-toolkit", "algorithmic-wins", "memory-streaming"],
    ["pa-p6-memo-practice", "pa-p6-profile-practice", "pa-p6-complexity-practice", "pa-p6-rescue-project"],
)

L1_EN = """
## Measure first: the discipline

Every performance claim in this module is graded the same way professionals
verify: **count the work, don't guess at the clock.** Wall-clock on a shared
machine is noisy; call counts, query counts, and allocation counts are facts.

The workflow:

1. **Establish a baseline** — the current numbers (latency, throughput,
   calls to the expensive thing).
2. **Attribute** — find where the work actually goes (next lesson: cProfile).
3. **Hypothesize** — "the O(n²) membership test dominates", "we re-fetch the
   same rows 50 times".
4. **Change one thing.**
5. **Verify** — re-measure the SAME metric. Keep the win, or revert.

Premature optimization has a precise meaning here: changing code before step 1
exists. `timeit` is the tool for micro-benchmarks (it disables GC and repeats
enough times to beat noise); `time.perf_counter()` is the wall-clock tool for
in-process timing; **but for graded correctness of an optimization, count
operations** — a memoization win is `calls: 13529 → 39`, not a fuzzy x2.
"""

L1_VI = L1_EN.replace(
    "## Measure first: the discipline",
    "## Đo trước: kỷ luật",
).replace(
    "Every performance claim in this module is graded the same way professionals\nverify: **count the work, don't guess at the clock.** Wall-clock on a shared\nmachine is noisy; call counts, query counts, and allocation counts are facts.",
    "Mọi tuyên bố hiệu năng trong module này được chấm theo đúng cách chuyên nghiệp\nkiểm chứng: **đếm công việc, đừng đoán bằng đồng hồ.** Wall-clock trên máy dùng\nchung thì nhiễu; số lần gọi, số truy vấn, số lần cấp phát mới là dữ kiện.",
).replace(
    "The workflow:",
    "Quy trình:",
).replace(
    "1. **Establish a baseline** — the current numbers (latency, throughput,\n   calls to the expensive thing).\n2. **Attribute** — find where the work actually goes (next lesson: cProfile).\n3. **Hypothesize** — \"the O(n²) membership test dominates\", \"we re-fetch the\n   same rows 50 times\".\n4. **Change one thing.**\n5. **Verify** — re-measure the SAME metric. Keep the win, or revert.",
    "1. **Thiết lập baseline** — các con số hiện tại (latency, throughput, số lần\n   gọi tới thứ đắt đỏ).\n2. **Quy kết** — tìm xem công việc thực sự đi đâu (bài sau: cProfile).\n3. **Đặt giả thuyết** — \"phép kiểm tra membership O(n²) là chỗ nặng nhất\",\n   \"chúng ta re-fetch cùng một dòng 50 lần\".\n4. **Sửa MỘT thứ.**\n5. **Kiểm chứng** — đo lại ĐÚNG chỉ số đó. Giữ chiến thắng, hoặc revert.",
).replace(
    "Premature optimization has a precise meaning here: changing code before step 1\nexists. `timeit` is the tool for micro-benchmarks (it disables GC and repeats\nenough times to beat noise); `time.perf_counter()` is the wall-clock tool for\nin-process timing; **but for graded correctness of an optimization, count\noperations** — a memoization win is `calls: 13529 → 39`, not a fuzzy x2.",
    "Tối ưu sớm ở đây có nghĩa rõ ràng: sửa code trước khi bước 1 tồn tại. `timeit`\nlà công cụ cho micro-benchmark (tắt GC và lặp đủ nhiều lần để át nhiễu);\n`time.perf_counter()` là công cụ wall-clock trong tiến trình; **nhưng để chấm\nđúng đắn một phép tối ưu, hãy đếm thao tác** — chiến thắng của memoization là\n`calls: 13529 → 39`, không phải một con số x2 mơ hồ.",
)

write_lesson(
    MOD, "measure-first",
    "Measurement discipline",
    "Baseline, attribute, change one thing, verify — with countable metrics.",
    16, L1_EN,
    "Kỷ luật đo lường",
    "Baseline, quy kết, sửa một thứ, kiểm chứng — bằng chỉ số đếm được.",
    L1_VI,
)

L2_EN = """
## The profiling toolkit: cProfile and pstats

`cProfile` records per-function call counts and cumulative time:

```python
import cProfile, pstats, io

def workload():
    ...  # the slow thing

pr = cProfile.Profile()
pr.enable()
workload()
pr.disable()

stats = pstats.Stats(pr)
stats.sort_stats("tottime")       # self time per function
stats.print_stats(5)              # top 5 offenders
```

Reading a profile like a professional:

- **tottime** (self time) — time in the function's own body, excluding callees.
  Sort by this to find the actual hotspot.
- **cumtime** (cumulative) — including everything it calls. Sort by this to
  find expensive *subtrees*.
- **ncalls** — call counts. A function called 500k times at 1µs each is a
  hotspot; a function called once at 500ms is a different kind of problem.
- `stats.print_callers()` shows who calls the hotspot — the refactoring target
  is often the caller, not the callee.

You can extract rows programmatically: `pstats.Stats(pr).stats` maps
`(filename, lineno, funcname)` → `(cc, nc, tt, ct, callers)`. That is exactly
what this module's challenges use to grade "find the bottleneck" — no guessing.
"""

L2_VI = L2_EN.replace(
    "## The profiling toolkit: cProfile and pstats",
    "## Bộ công cụ profiling: cProfile và pstats",
).replace(
    "`cProfile` records per-function call counts and cumulative time:",
    "`cProfile` ghi số lần gọi từng hàm và thời gian cộng dồn:",
).replace(
    "Reading a profile like a professional:",
    "Đọc profile như một chuyên gia:",
).replace(
    "- **tottime** (self time) — time in the function's own body, excluding callees.\n  Sort by this to find the actual hotspot.\n- **cumtime** (cumulative) — including everything it calls. Sort by this to\n  find expensive *subtrees*.\n- **ncalls** — call counts. A function called 500k times at 1µs each is a\n  hotspot; a function called once at 500ms is a different kind of problem.\n- `stats.print_callers()` shows who calls the hotspot — the refactoring target\n  is often the caller, not the callee.",
    "- **tottime** (thời gian riêng) — thời gian trong thân hàm, không tính callee.\n  Sort theo cái này để tìm hotspot thật.\n- **cumtime** (cộng dồn) — gồm cả những gì nó gọi. Sort theo cái này để tìm\n  *cây con* đắt đỏ.\n- **ncalls** — số lần gọi. Hàm được gọi 500k lần mỗi lần 1µs là một hotspot;\n  hàm gọi một lần tốn 500ms là một loại bài toán khác.\n- `stats.print_callers()` cho biết ai gọi tới hotspot — đích refactor thường là\n  phía gọi, không phải bị gọi.",
).replace(
    "You can extract rows programmatically: `pstats.Stats(pr).stats` maps\n`(filename, lineno, funcname)` → `(cc, nc, tt, ct, callers)`. That is exactly\nwhat this module's challenges use to grade \"find the bottleneck\" — no guessing.",
    "Bạn có thể bóc dữ liệu bằng mã: `pstats.Stats(pr).stats` ánh xạ\n`(filename, lineno, funcname)` → `(cc, nc, tt, ct, callers)`. Đây chính là cách\ncác bài tập trong module này chấm \"tìm bottleneck\" — không đoán mò.",
)

write_lesson(
    MOD, "profiling-toolkit",
    "cProfile, pstats, reading hotspots",
    "Find where time actually goes; extract hotspot data programmatically.",
    20, L2_EN,
    "cProfile, pstats, đọc hotspot",
    "Tìm xem thời gian thực sự đi đâu; bóc dữ liệu hotspot bằng mã.",
    L2_VI,
)

L3_EN = """
## Algorithmic wins: complexity beats micro-tuning

The biggest speedups come from changing the *shape* of the work:

- **Membership on a list is O(n); on a set/dict it is O(1).** Filtering a list
  against a large denylist with `x in some_list` is the classic quadratic
  accident. One `set(...)` call removes an entire order of magnitude.
- **Memoization** converts overlapping recursive work into a table lookup:
  naive `fib(25)` makes ~243k calls; the memoized version makes ~49. Same
  answer, different universe of work. `functools.lru_cache(maxsize=None)` is
  the standard tool; a dict keyed by arguments is the manual equivalent.
- **Batching** turns N round-trips into 1: fetching per-item from a database
  or API inside a loop (N+1 queries) collapses into one batched fetch.
- **Early exit / bounds**: stop scanning when the answer is decided; prefer
  `any()`/`all()` over building full lists of booleans.

Micro-tuning (attribute-lookup hoisting, local variable caching) yields small
constant factors. Complexity fixes yield orders of magnitude. When both are
available, take the complexity fix first — it also tends to be the more
readable change.
"""

L3_VI = L3_EN.replace(
    "## Algorithmic wins: complexity beats micro-tuning",
    "## Chiến thắng thuật toán: độ phức tạp át micro-tuning",
).replace(
    "The biggest speedups come from changing the *shape* of the work:",
    "Những cú tăng tốc lớn nhất đến từ việc thay đổi *hình dạng* công việc:",
).replace(
    "- **Membership on a list is O(n); on a set/dict it is O(1).** Filtering a list\n  against a large denylist with `x in some_list` is the classic quadratic\n  accident. One `set(...)` call removes an entire order of magnitude.\n- **Memoization** converts overlapping recursive work into a table lookup:\n  naive `fib(25)` makes ~243k calls; the memoized version makes ~49. Same\n  answer, different universe of work. `functools.lru_cache(maxsize=None)` is\n  the standard tool; a dict keyed by arguments is the manual equivalent.\n- **Batching** turns N round-trips into 1: fetching per-item from a database\n  or API inside a loop (N+1 queries) collapses into one batched fetch.\n- **Early exit / bounds**: stop scanning when the answer is decided; prefer\n  `any()`/`all()` over building full lists of booleans.",
    "- **Membership trên list là O(n); trên set/dict là O(1).** Lọc một list với\n  một denylist lớn bằng `x in some_list` là tai nạn bậc hai kinh điển. Một lần\n  `set(...)` xóa cả một bậc độ lớn.\n- **Memoization** biến công việc đệ quy chồng lấn thành tra bảng: `fib(25)`\n  ngây thơ gọi ~243k lần; bản memoized gọi ~49. Cùng đáp án, hai vũ trụ công\n  việc khác nhau. `functools.lru_cache(maxsize=None)` là công cụ chuẩn; một\n  dict keyed theo tham số là bản thủ công tương đương.\n- **Batching** biến N chuyến đi về thành 1: fetch từng item từ DB hay API trong\n  vòng lặp (N+1 truy vấn) sụp đổ thành một lần fetch theo lô.\n- **Thoát sớm / chặn biên**: ngừng quét khi đáp án đã rõ; ưu tiên\n  `any()`/`all()` thay vì dựng cả danh sách boolean.",
).replace(
    "Micro-tuning (attribute-lookup hoisting, local variable caching) yields small\nconstant factors. Complexity fixes yield orders of magnitude. When both are\navailable, take the complexity fix first — it also tends to be the more\nreadable change.",
    "Micro-tuning (nâng attribute lookup lên biến cục bộ, cache biến local) chỉ cho\nhệ số hằng nhỏ. Sửa độ phức tạp cho cả bậc độ lớn. Khi cả hai đều khả dụng,\nhãy lấy bản sửa độ phức tạp trước — nó cũng thường là thay đổi dễ đọc hơn.",
)

write_lesson(
    MOD, "algorithmic-wins",
    "Complexity: sets, memoization, batching",
    "Order-of-magnitude wins from changing the shape of the work.",
    20, L3_EN,
    "Độ phức tạp: set, memoization, batching",
    "Tăng tốc cả bậc độ lớn bằng cách thay đổi hình dạng công việc.",
    L3_VI,
)

L4_EN = """
## Memory & streaming: generators over lists

Materializing data you could stream is the silent memory bug. A function that
reads a 10 GB log "into a list" dies; the same function that *yields* parsed
lines runs in constant memory.

```python
def parse(lines):                      # lines: any iterable of str
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        yield (key.strip(), value.strip())
```

The graded way to prove streaming (as used in this module's challenges): pass
an **iterator that has no `len()` and explodes if materialized** — a custom
iterable whose `__iter__` yields millions of values would take forever to
`list()` — no, the practical probe is simpler: an object that raises inside
`__iter__` after N values proves the consumer pulls lazily and stops early.

Combinators compose: `map`, `filter`, `itertools.islice`, `itertools.chain`,
`sum(...)`, `any(...)` all consume iterables lazily. `sorted(...)` and
`max(...)` consume fully (necessarily). Know which is which.
"""

L4_VI = L4_EN.replace(
    "## Memory & streaming: generators over lists",
    "## Bộ nhớ & streaming: generator hơn list",
).replace(
    "Materializing data you could stream is the silent memory bug. A function that\nreads a 10 GB log \"into a list\" dies; the same function that *yields* parsed\nlines runs in constant memory.",
    "Materialize dữ liệu mà bạn có thể stream là lỗi bộ nhớ âm thầm. Một hàm đọc\nlog 10 GB \"vào list\" thì chết; cùng hàm đó nhưng *yield* từng dòng đã parse\nchạy với bộ nhớ hằng.",
).replace(
    "The graded way to prove streaming (as used in this module's challenges): pass\nan **iterator that has no `len()` and explodes if materialized** — a custom\niterable whose `__iter__` yields millions of values would take forever to\n`list()` — no, the practical probe is simpler: an object that raises inside\n`__iter__` after N values proves the consumer pulls lazily and stops early.",
    "Cách chứng minh streaming khi chấm (như các bài tập trong module này dùng):\ntruyền vào một **iterator không có `len()` và nổ tung nếu bị materialize** —\nmột iterable tự viết mà `__iter__`_yield_ hàng triệu giá trị sẽ khiến `list()`\nmất thời gian vô hạn — không, probe thực dụng đơn giản hơn: một đối tượng raise\nbên trong `__iter__` sau N giá trị chứng minh phía tiêu thụ kéo lười và dừng sớm.",
).replace(
    "Combinators compose: `map`, `filter`, `itertools.islice`, `itertools.chain`,\n`sum(...)`, `any(...)` all consume iterables lazily. `sorted(...)` and\n`max(...)` consume fully (necessarily). Know which is which.",
    "Các bộ kết hợp ghép được với nhau: `map`, `filter`, `itertools.islice`,\n`itertools.chain`, `sum(...)`, `any(...)` đều tiêu thụ iterable lười.\n`sorted(...)` và `max(...)` tiêu thụ toàn bộ (điều bắt buộc). Hãy biết cái nào\nthuộc loại nào.",
)

write_lesson(
    MOD, "memory-streaming",
    "Generators, iterators, streaming",
    "Constant-memory processing and the probes that prove it.",
    18, L4_EN,
    "Generator, iterator, streaming",
    "Xử lý với bộ nhớ hằng và những probe chứng minh điều đó.",
    L4_VI,
)

# ── practice 1: memoization ──────────────────────────────────────────────────
MEMO_REF = (
    "def fib(n, memo, stats):\n"
    "    stats['calls'] += 1\n"
    "    if n <= 1:\n"
    "        return n\n"
    "    if n in memo:\n"
    "        return memo[n]\n"
    "    result = fib(n - 1, memo, stats) + fib(n - 2, memo, stats)\n"
    "    memo[n] = result\n"
    "    return result"
)
MEMO_WRONG = (
    "def fib(n, memo, stats):\n"
    "    stats['calls'] += 1\n"
    "    if n <= 1:\n"
    "        return n\n"
    "    # WRONG: writes the memo but never reads it — exponential calls remain\n"
    "    result = fib(n - 1, memo, stats) + fib(n - 2, memo, stats)\n"
    "    memo[n] = result\n"
    "    return result"
)

write_practice(
    MOD, "pa-p6-memo-practice",
    "Memoization Practice",
    "Prove the win in call counts: memoize fib and watch the counter collapse.",
    "Luyện Memoization",
    "Chứng minh chiến thắng bằng số lần gọi: memoize fib và xem bộ đếm sụp đổ.",
    "algorithmic-wins", 18, "advanced",
    [
        challenge(
            "pa-perf-memo-fib",
            "Memoized fib, counted",
            "Implement `fib(n, memo, stats)` — recursive Fibonacci with explicit memoization:\n\n- `memo` is a dict the function may read and write\n- `stats` is a dict containing `'calls'`; increment `stats['calls'] += 1` at the top of EVERY invocation (including memo-hit returns)\n- fib(0)=0, fib(1)=1, else fib(n-1)+fib(n-2)\n\nThe graded test calls `fib(25, {}, stats)` and asserts the value is 75025 and `stats['calls']` is under 60 (the never-reads-memo version makes ~243k calls).",
            "def fib(n, memo, stats):\n    # TODO: count every invocation; memoize; recurse\n    pass",
            [
                ("correct value, tiny call count",
                 "stats = {'calls': 0}\nvalue = fib(25, {}, stats)\nassert value == 75025, f'value: {value}'\nassert stats['calls'] < 60, f\'calls: {stats[\"calls\"]} — memoization not effective\'\nprint('ok')",
                 "Check the memo BEFORE recursing; increment stats at the very top of the function."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-perf-memo-fib": vi_challenge(
            "fib memoized, có đếm",
            "Cài `fib(n, memo, stats)` — Fibonacci đệ quy với memoization tường minh:\n\n- `memo` là dict mà hàm được đọc và ghi\n- `stats` là dict chứa `'calls'`; tăng `stats['calls'] += 1` ở ĐẦU mọi lần được gọi (kể cả khi trả về từ memo)\n- fib(0)=0, fib(1)=1, còn lại fib(n-1)+fib(n-2)\n\nTest chấm gọi `fib(25, {}, stats)` và khẳng định giá trị là 75025 và `stats['calls']` dưới 60 (bản không-đọc-memo gọi ~243k lần).",
            [("Giá trị đúng, số lần gọi tí hon", "Tra memo TRƯỚC khi đệ quy; tăng stats ở ngay đầu hàm.")],
        ),
    },
    solutions=[("pa-perf-memo-fib", MEMO_REF, MEMO_WRONG)],
)

# ── practice 2: profiling ────────────────────────────────────────────────────
PROFILE_REF = (
    "import cProfile\n"
    "import pstats\n\n\n"
    "def hotspot_name(workload):\n"
    "    '''Run workload() under cProfile; return the funcname with the highest\n"
    "    tottime (self time), excluding the workload function itself.'''\n"
    "    pr = cProfile.Profile()\n"
    "    pr.enable()\n"
    "    workload()\n"
    "    pr.disable()\n"
    "    st = pstats.Stats(pr)\n"
    "    best, best_tt = None, -1.0\n"
    "    for (fn, lineno, name), (cc, nc, tt, ct, callers) in st.stats.items():\n"
    "        if name == 'workload':\n"
    "            continue\n"
    "        if tt > best_tt:\n"
    "            best, best_tt = name, tt\n"
    "    return best"
)
PROFILE_WRONG = (
    "import cProfile\n"
    "import pstats\n\n\n"
    "def hotspot_name(workload):\n"
    "    '''WRONG: sorts by cumtime instead of tottime — always names an outer\n"
    "    wrapper (or the workload itself), never the real hotspot.'''\n"
    "    pr = cProfile.Profile()\n"
    "    pr.enable()\n"
    "    workload()\n"
    "    pr.disable()\n"
    "    st = pstats.Stats(pr)\n"
    "    best, best_ct = None, -1.0\n"
    "    for (fn, lineno, name), (cc, nc, tt, ct, callers) in st.stats.items():\n"
    "        if ct > best_ct:\n"
    "            best, best_ct = name, ct\n"
    "    return best"
)

write_practice(
    MOD, "pa-p6-profile-practice",
    "Profiling Practice",
    "Find the bottleneck programmatically: sort by self time, ignore the wrapper.",
    "Luyện Profiling",
    "Tìm bottleneck bằng mã: sort theo self time, bỏ qua wrapper.",
    "profiling-toolkit", 20, "advanced",
    [
        challenge(
            "pa-perf-hotspot",
            "Extract the hotspot",
            "Implement `hotspot_name(workload)`:\n\n- run `workload()` under `cProfile`\n- inspect the stats programmatically (`pstats.Stats(pr).stats`)\n- return the NAME of the function with the highest **tottime** (self time), excluding `workload` itself\n\nThe graded workload calls two helpers with very different self-times; the wrong implementation sorts by cumtime and names the wrong thing.",
            "import cProfile\nimport pstats\n\n# TODO: hotspot_name(workload)",
            [
                ("names the true self-time hotspot",
                 "def tiny():\n    return 1\n\ndef heavy():\n    total = 0\n    for i in range(50000):\n        total += i * i\n    return total\n\ndef workload():\n    tiny()\n    heavy()\n\nassert hotspot_name(workload) == 'heavy', f'got: {hotspot_name(workload)}'\nprint('ok')",
                 "Iterate Stats(pr).stats — (cc, nc, tt, ct, callers); tt is self time."),
            ],
            level="debugging",
        ),
    ],
    {
        "pa-perf-hotspot": vi_challenge(
            "Bóc hotspot",
            "Cài `hotspot_name(workload)`:\n\n- chạy `workload()` dưới `cProfile`\n- đọc stats bằng mã (`pstats.Stats(pr).stats`)\n- trả về TÊN hàm có **tottime** (self time) cao nhất, loại trừ chính `workload`\n\nWorkload được chấm gọi hai helper với self-time chênh lệch lớn; bản sai sort theo cumtime sẽ chỉ sai tên.",
            [("Chỉ đúng hotspot theo self time", "Duyệt Stats(pr).stats — (cc, nc, tt, ct, callers); tt là self time.")],
        ),
    },
    solutions=[("pa-perf-hotspot", PROFILE_REF, PROFILE_WRONG)],
)

# ── practice 3: complexity fix ───────────────────────────────────────────────
COMPLEXITY_REF = (
    "def find_common(a, b, counter):\n"
    "    counter.seed(b)\n"
    "    out = []\n"
    "    for x in a:\n"
    "        if counter.membership(x):\n"
    "            out.append(x)\n"
    "    return sorted(set(out))"
)
COMPLEXITY_WRONG = (
    "def find_common(a, b, counter):\n"
    "    # WRONG: never calls seed/membership — probes stay 0, so the budget test"
    "    # fails; the result may even be right but the contract is broken\n"
    "    bset = set(b)\n"
    "    out = []\n"
    "    for x in a:\n"
    "        if x in bset:\n"
    "            out.append(x)\n"
    "    return sorted(set(out))"
)

write_practice(
    MOD, "pa-p6-complexity-practice",
    "Complexity Practice",
    "Turn quadratic probing into linear — the test budget proves it.",
    "Luyện Độ phức tạp",
    "Biến probing bậc hai thành tuyến tính — ngân sách test là bằng chứng.",
    "algorithmic-wins", 20, "advanced",
    [
        challenge(
            "pa-perf-set-membership",
            "Linear-time intersection",
            "Implement `find_common(a, b, counter)` returning the sorted list of values present in BOTH lists `a` and `b`.\n\n`counter` enforces a probe budget: call `counter.seed(b)` ONCE to load `b`, then for each element of `a` call `counter.membership(x)` — that is the only allowed membership test. The graded test asserts the result is correct AND that exactly `len(a)` membership probes were made.",
            "def find_common(a, b, counter):\n    # counter.seed(b) once; counter.membership(x) is the ONLY allowed lookup\n    pass",
            [
                ("correct result within linear probe budget",
                 "class Budget:\n    def __init__(self):\n        self._set = set()\n        self.probes = 0\n    def seed(self, values):\n        self._set = set(values)\n    def membership(self, x):\n        self.probes += 1\n        return x in self._set\n\na = list(range(300))\nb = list(range(150, 450))\nc = Budget()\nout = find_common(a, b, c)\nassert out == list(range(150, 300)), f'out: {out[:5]}...{out[-5:]}'\nassert c.probes <= 310, f'probes: {c.probes}'\nprint('ok')",
                 "seed() builds the set in one call; membership() per element of a is O(1) each."),
                ("probe budget is enforced per element",
                 "class Counting:\n    def __init__(self):\n        self._set = set()\n        self.probes = 0\n    def seed(self, values):\n        self._set = set(values)\n    def membership(self, x):\n        self.probes += 1\n        return x in self._set\n\nc = Counting()\nc.seed(list(range(150, 450)))\nout = find_common(list(range(300)), list(range(150, 450)), c)\nassert out == list(range(150, 300))\nassert c.probes == 300, f'probes: {c.probes} — must be exactly one per element of a'\nprint('ok')",
                 "Exactly len(a) membership calls — one set built via seed, then one probe per element of a."),
            ],
            level="independent",
        ),
    ],
    {
        "pa-perf-set-membership": vi_challenge(
            "Giao tuyến tính",
            "Cài `find_common(a, b, counter)` trả về danh sách đã sort các giá trị có mặt ở CẢ HAI list `a` và `b`.\n\n`counter` là đối tượng ngân sách probing: mọi phép kiểm tra membership bạn thực hiện phải đi qua `counter.membership(x)` (đó là cách tra duy nhất được phép). Bản cài của bạn phải ở dưới `len(a) + len(b) + 10` lần probe — nghĩa là dựng set từ `b` trước (gọi `counter.seed(b)` đúng một lần), rồi thử từng phần tử của `a`.",
            [("Kết quả đúng trong ngân sách probe tuyến tính", "seed() dựng set trong một lần gọi; membership() trên từng phần tử của a là O(1) mỗi lần."),
             ("Cố gắng bậc hai nổ ngân sách", "Phép `x in b_list` từng phần tử cần ~45k probe — xa vượt ngưỡng.")],
        ),
    },
    solutions=[("pa-perf-set-membership", COMPLEXITY_REF, COMPLEXITY_WRONG)],
)

# ── practice 4 + project: streaming + rescue ─────────────────────────────────
STREAM_REF = (
    "def running_stats(numbers):\n"
    "    '''Yield (count, running_total) after each number. Must consume the\n"
    "    iterator LAZILY — never materialize it (no list(), no sorted()).'''\n"
    "    total = 0\n"
    "    count = 0\n"
    "    for x in numbers:\n"
    "        total += x\n"
    "        count += 1\n"
    "        yield (count, total)"
)
STREAM_WRONG = (
    "def running_stats(numbers):\n"
    "    # WRONG: materializes the whole stream first — dies on unbounded sources\n"
    "    data = list(numbers)\n"
    "    total = 0\n"
    "    count = 0\n"
    "    for x in data:\n"
    "        total += x\n"
    "        count += 1\n"
    "        yield (count, total)"
)

write_practice(
    MOD, "pa-p6-rescue-project",
    "Project: Performance Rescue",
    "Two rescue drills: stream without materializing, and cache without re-computing.",
    "Project: Giải cứu hiệu năng",
    "Hai bài giải cứu: stream không materialize, và cache không tính lại.",
    "memory-streaming", 28, "advanced",
    [
        challenge(
            "pa-perf-streaming-stats",
            "Streaming running stats",
            "Implement `running_stats(numbers)` — a GENERATOR that yields `(count, running_total)` after consuming each number.\n\nGrading probe: the test feeds an infinite-ish source and only pulls the first 5 pairs — a materializing implementation (list(...)) hangs or blows up; a lazy one passes instantly.",
            "def running_stats(numbers):\n    # TODO: generator — yield (count, total) per input number",
            [
                ("pulls lazily from a hostile source",
                 "class Hostile:\n    '''Yields 10**9 ones; materializing it is impossible in practice.'''\n    def __iter__(self):\n        self.n = 0\n        return self\n    def __next__(self):\n        self.n += 1\n        if self.n > 10**9:\n            raise StopIteration\n        return 1\n\nout = []\nfor pair in running_stats(Hostile()):\n    out.append(pair)\n    if len(out) == 5:\n        break\nassert out == [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], f'out: {out}'\nprint('ok')",
                 "for-loop over the iterable, yield per step — nothing may call list() on the source."),
                ("finite source, exact pairs",
                 "out = list(running_stats([10, 20, 30]))\nassert out == [(1, 10), (2, 30), (3, 60)]\nprint('ok')",
                 "Running total includes each new number."),
            ],
            level="combination",
        ),
        challenge(
            "pa-perf-cache-rescue",
            "Cache the expensive backend",
            "Implement `class CachedApi` wrapping an expensive `backend` (any object with `.fetch(key)`):\n\n- `get(key)` returns `backend.fetch(key)` at most ONCE per distinct key (memoize)\n- the backend's fetch counter (injected via `Backend` class in the test) must show exactly one call per distinct key, however many `get` calls repeat\n- `invalidate(key)` forces the next `get(key)` to re-fetch",
            "class CachedApi:\n    def __init__(self, backend):\n        self._backend = backend\n\n    # TODO: get(key), invalidate(key)",
            [
                ("one fetch per distinct key",
                 "class Backend:\n    def __init__(self):\n        self.calls = {}\n    def fetch(self, key):\n        self.calls[key] = self.calls.get(key, 0) + 1\n        return f'data:{key}'\n\nb = Backend()\napi = CachedApi(b)\nassert api.get('a') == 'data:a'\nassert api.get('a') == 'data:a'\nassert api.get('b') == 'data:b'\nassert api.get('a') == 'data:a'\nassert b.calls == {'a': 1, 'b': 1}, f'calls: {b.calls}'\nprint('ok')",
                 "Memoize in a dict keyed by the argument — check before delegating."),
                ("invalidate forces a refetch",
                 "class Backend:\n    def __init__(self):\n        self.calls = {}\n    def fetch(self, key):\n        self.calls[key] = self.calls.get(key, 0) + 1\n        return f'data:{key}'\n\nb = Backend()\napi = CachedApi(b)\napi.get('x')\napi.invalidate('x')\napi.get('x')\nassert b.calls == {'x': 2}, f'calls: {b.calls}'\nprint('ok')",
                 "invalidate removes the memo entry only for that key."),
            ],
            level="debugging",
        ),
    ],
    {
        "pa-perf-streaming-stats": vi_challenge(
            "Thống kê chạy dạng streaming",
            "Cài `running_stats(numbers)` — một GENERATOR yield `(count, running_total)` sau khi tiêu thụ từng số.\n\nProbe chấm: test cấp một nguồn gần như vô hạn và chỉ kéo 5 cặp đầu — bản materialize (list(...)) sẽ treo hoặc nổ; bản lười thì qua ngay lập tức.",
            [("Kéo lười từ nguồn thù địch", "Vòng for trên iterable, yield từng bước — không được gọi list() lên nguồn.")],
        ),
        "pa-perf-cache-rescue": vi_challenge(
            "Cache backend đắt đỏ",
            "Cài `class CachedApi` bọc một `backend` đắt đỏ (bất kỳ đối tượng nào có `.fetch(key)`):\n\n- `get(key)` trả về `backend.fetch(key)` TỐI ĐA MỘT LẦN cho mỗi key (memoize)\n- bộ đếm fetch của backend (tiêm qua class `Backend` trong test) phải cho đúng một lần gọi mỗi key, bất kể `get` lặp lại bao nhiêu\n- `invalidate(key)` buộc lần `get(key)` kế tiếp phải fetch lại",
            [("Một lần fetch mỗi key", "Memoize trong dict keyed theo tham số — tra trước khi ủy quyền."),
             ("invalidate buộc fetch lại", "invalidate chỉ xóa mục memo của key đó.")],
        ),
    },
    solutions=[
        ("pa-perf-streaming-stats", STREAM_REF, STREAM_WRONG),
        ("pa-perf-cache-rescue",
         "class CachedApi:\n    def __init__(self, backend):\n        self._backend = backend\n        self._cache = {}\n\n    def get(self, key):\n        if key not in self._cache:\n            self._cache[key] = self._backend.fetch(key)\n        return self._cache[key]\n\n    def invalidate(self, key):\n        self._cache.pop(key, None)",
         "class CachedApi:\n    def __init__(self, backend):\n        self._backend = backend\n        self._cache = {}\n\n    def get(self, key):\n        # WRONG: caches but always delegates — backend called every time\n        value = self._backend.fetch(key)\n        self._cache[key] = value\n        return value\n\n    def invalidate(self, key):\n        self._cache.pop(key, None)"),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_REF = (
    "def fetch_user_orders(user_ids, db):\n"
    "    '''db.query(sql_template, ids) counts queries; fetch ALL users' orders\n"
    "    in AT MOST 2 queries and return {user_id: [order, ...]}.'''\n"
    "    if not user_ids:\n"
    "        return {}\n"
    "    rows = db.query('SELECT user_id, id, total FROM orders WHERE user_id IN ?', [user_ids])\n"
    "    out = {uid: [] for uid in user_ids}\n"
    "    for user_id, oid, total in rows:\n"
    "        out[user_id].append({'id': oid, 'total': total})\n"
    "    return out"
)
CK_WRONG = (
    "def fetch_user_orders(user_ids, db):\n"
    "    '''WRONG: the classic N+1 — one query per user.'''\n"
    "    out = {}\n"
    "    for uid in user_ids:\n"
    "        rows = db.query('SELECT id, total FROM orders WHERE user_id = ?', [uid])\n"
    "        out[uid] = [{'id': oid, 'total': t} for (oid, t) in rows]\n"
    "    return out"
)

write_checkpoint(
    MOD, "pa-checkpoint-performance",
    "Checkpoint: Performance",
    "Kill the N+1: batch a per-item fetch into at most 2 queries, proven by a query counter.",
    30,
    """
## Checkpoint — the N+1 rescue

`db` records every `db.query(sql, params)` call. The naive implementation
makes one query PER user (N+1). Batch it:

- `fetch_user_orders(user_ids, db)` returns `{user_id: [{'id':…, 'total':…}, …]}`
- with **at most 2 queries total** (regardless of user count)
- order lists per user keep the row order returned by the db

This is the exact shape you will meet again in the database module — learned
here as a performance pattern, applied there as SQL.
""",
    "Checkpoint: Hiệu năng",
    "Diệt N+1: gộp fetch từng item vào tối đa 2 truy vấn, chứng minh bằng bộ đếm truy vấn.",
    """
## Checkpoint — giải cứu N+1

`db` ghi lại mọi lần `db.query(sql, params)`. Bản ngây thơ tạo một truy vấn CHO\nMỖI user (N+1). Hãy gộp lại:

- `fetch_user_orders(user_ids, db)` trả về `{user_id: [{'id':…, 'total':…}, …]}`
- với **tối đa 2 truy vấn** tổng cộng (bất kể số user)
- danh sách order của từng user giữ nguyên thứ tự dòng mà db trả về

Đây chính là hình dạng bạn sẽ gặp lại trong module database — học ở đây như\nmột pattern hiệu năng, áp dụng ở đó như SQL.
""",
    challenge(
        "pa-checkpoint-performance",
        "N+1 rescue with a query counter",
        "Implement fetch_user_orders using at most 2 db.query calls total; per-user order lists preserve db row order; empty user_ids returns {} with zero queries.",
        "def fetch_user_orders(user_ids, db):\n    # db.query(sql, params) -> list of (user_id, order_id, total) rows\n    pass",
        [
            ("two queries, all users, ordered rows",
             "class DB:\n    def __init__(self):\n        self.queries = 0\n    def query(self, sql, params):\n        self.queries += 1\n        rows = [(1, 11, 5.0), (2, 21, 7.5), (1, 12, 3.0), (3, 31, 9.9), (2, 22, 1.0)]\n        ids = set(params[0])\n        return [r for r in rows if r[0] in ids]\n\ndb = DB()\nout = fetch_user_orders([1, 2, 3], db)\nassert db.queries <= 2, f'queries: {db.queries}'\nassert out[1] == [{'id': 11, 'total': 5.0}, {'id': 12, 'total': 3.0}], f'out[1]: {out[1]}'\nassert out[2] == [{'id': 21, 'total': 7.5}, {'id': 22, 'total': 1.0}]\nassert out[3] == [{'id': 31, 'total': 9.9}]\nprint('ok')",
             "One query with all ids (IN-clapse style via the db helper) and group rows by user_id in Python."),
            ("empty input makes zero queries",
             "class DB:\n    def __init__(self):\n        self.queries = 0\n    def query(self, sql, params):\n        self.queries += 1\n        return []\n\ndb = DB()\nout = fetch_user_orders([], db)\nassert out == {} and db.queries == 0, f'out: {out}, queries: {db.queries}'\nprint('ok')",
                 "Guard the empty case before any query."),
        ],
        level="build",
    ),
    vi_challenge(
        "Giải cứu N+1 với bộ đếm truy vấn",
        "Cài fetch_user_orders dùng tối đa 2 lần db.query tổng cộng; danh sách order từng user giữ thứ tự dòng của db; user_ids rỗng trả về {} với 0 truy vấn.",
        [("Hai truy vấn, mọi user, dòng đúng thứ tự", "Một truy vấn với mọi id (kiểu mệnh đề IN qua helper của db) rồi gom dòng theo user_id bằng Python."),
         ("Đầu vào rỗng, 0 truy vấn", "Chặn trường hợp rỗng trước mọi truy vấn.")],
    ),
    solution=CK_REF,
    wrong=CK_WRONG,
)

print("module 6 complete")
