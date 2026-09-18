#!/usr/bin/env python3
"""Python Intermediate — modules 3 (data-model-iteration) and 4 (structure-and-typing)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 3: data-model-iteration ============================
M3 = "data-model-iteration"
L3A = "iterators"
L3B = "generators"
L3C = "context-managers"
L3D = "checkpoint-streams"

write_module(
    M3,
    "The Data Model: Iteration and Resources",
    "Make your objects work with for-loops, stream data with generators, and manage resources with with.",
    "Mô hình dữ liệu: Lặp và Tài nguyên",
    "Khiến đối tượng của bạn hoạt động với vòng for, phát dữ liệu bằng generator, và quản lý tài nguyên bằng with.",
    [L3A, L3B, L3C, L3D],
    ["m3-iter-practice", "m3-gen-practice", "m3-ctx-practice"],
)

write_lesson(
    M3, L3A,
    "Iterators: How for Really Works",
    "The iteration protocol: iter(), next(), StopIteration, and custom iterators.",
    13,
    """
`for x in thing` is not magic. Python asks `thing` for an **iterator**
(`iter(thing)`), then calls `next()` on it repeatedly until `StopIteration`:

```python
nums = [10, 20]
it = iter(nums)      # an iterator object
next(it)             # 10
next(it)             # 20
next(it)             # raises StopIteration — the for-loop's exit signal
```

Any object with `__iter__` returning an iterator is **iterable**; an
iterator carries `__next__`. Lists, dicts, files, ranges — all just implement
this one protocol. That's why `for` works identically over all of them.

## Your own iterator

```python
class Countdown:
    def __init__(self, start):
        self.n = start

    def __iter__(self):
        return self            # the object IS its own iterator

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for n in Countdown(3):
    print(n)                   # 3, 2, 1
```

A subtlety worth knowing: an iterator is **exhausted after one pass** — a
second `for` over the same iterator sees nothing. Iterables (like lists)
produce a fresh iterator each time; that's why you can loop over a list twice
but not over a generator twice.
""",
    "Iterator: vòng for thực sự hoạt động thế nào",
    "Giao thức lặp: iter(), next(), StopIteration, và iterator tự viết.",
    """
`for x in thing` không phải phép màu. Python hỏi `thing` lấy một **iterator**
(`iter(thing)`), rồi gọi `next()` liên tục cho đến khi gặp `StopIteration`:

```python
nums = [10, 20]
it = iter(nums)      # một đối tượng iterator
next(it)             # 10
next(it)             # 20
next(it)             # raise StopIteration — tín hiệu kết thúc của vòng for
```

Bất kỳ đối tượng nào có `__iter__` trả về một iterator đều là **iterable**;
iterator mang `__next__`. List, dict, tệp, range — tất cả chỉ đơn giản là
cài đặt đúng một giao thức này. Vì vậy `for` hoạt động giống nhau trên tất cả.

## Iterator của riêng bạn

```python
class Countdown:
    def __init__(self, start):
        self.n = start

    def __iter__(self):
        return self            # chính đối tượng này là iterator của nó

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for n in Countdown(3):
    print(n)                   # 3, 2, 1
```

Một chi tiết đáng nhớ: iterator **cạn sau một lượt** — vòng `for` thứ hai
trên cùng một iterator không còn gì để duyệt. Iterable (như list) sinh một
iterator mới mỗi lần; vì vậy bạn có thể duyệt một list hai lần nhưng không
thể duyệt một generator hai lần.
""",
)

write_lesson(
    M3, L3B,
    "Generators: Lazy Sequences",
    "yield turns a function into a streaming factory — memory-friendly by design.",
    14,
    """
A **generator function** contains `yield`. Calling it doesn't run the body —
it returns a generator that produces values **lazily**, one at a time:

```python
def read_numbers(lines):
    for line in lines:
        line = line.strip()
        if line.isdigit():
            yield int(line)        # pause here, hand out one value

gen = read_numbers(["1", "oops", "3"])
next(gen)      # 1
next(gen)      # 3 — the bad line was skipped inside the function
```

Two superpowers come from this laziness:

- **Constant memory**: a generator never materializes the whole sequence. This streams a 10 GB log through a 1 MB loop without breaking a sweat.
- **Composable pipelines**: generators feed generators, and each stage stays simple.

```python
def sum_big_sales(rows):
    big = (r for r in rows if r["amount"] > 1000)   # generator expression
    return sum(r["amount"] for r in big)
```

## yield from and delegation

A generator can delegate to another iterable with `yield from`:

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)     # recursively hand out each element
        else:
            yield item
```

## When NOT to use generators

If you need the data more than once (len(), indexing, re-iteration), build a
list. Generators are single-use streams — reach for them when data is large,
infinite, or produced on demand.
""",
    "Generator: Chuỗi lười",
    "yield biến một hàm thành nhà máy dữ liệu dạng stream — tiết kiệm bộ nhớ ngay từ thiết kế.",
    """
Một **generator function** chứa `yield`. Gọi nó không chạy thân hàm — nó trả
về một generator phát giá trị **lười biếng**, từng giá trị một:

```python
def read_numbers(lines):
    for line in lines:
        line = line.strip()
        if line.isdigit():
            yield int(line)        # dừng ở đây, phát một giá trị

gen = read_numbers(["1", "oops", "3"])
next(gen)      # 1
next(gen)      # 3 — dòng lỗi bị bỏ qua bên trong hàm
```

Hai siêu năng lực đến từ sự lười này:

- **Bộ nhớ hằng số**: generator không bao giờ dựng cả dãy trong bộ nhớ. Nó stream một log 10 GB qua vòng lặp 1 MB không hề khó thở.
- **Pipeline ghép được**: generator nối vào generator, mỗi tầng vẫn đơn giản.

```python
def sum_big_sales(rows):
    big = (r for r in rows if r["amount"] > 1000)   # generator expression
    return sum(r["amount"] for r in big)
```

## yield from và ủy quyền

Generator có thể ủy quyền cho một iterable khác bằng `yield from`:

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)     # đệ quy phát từng phần tử
        else:
            yield item
```

## Khi nào KHÔNG dùng generator

Nếu cần dữ liệu nhiều lần (len(), indexing, duyệt lại), hãy dựng list.
Generator là stream dùng một lần — dùng khi dữ liệu lớn, vô hạn, hoặc sinh
theo nhu cầu.
""",
)

write_lesson(
    M3, L3C,
    "Context Managers: with Done Right",
    "Guarantee cleanup with __enter__/__exit__ and @contextmanager.",
    13,
    """
`with` guarantees cleanup **even when an exception flies through**. You use
it daily with files — now build your own:

```python
class Timer:
    def __enter__(self):
        self.start = time.monotonic()
        return self                    # bound to the as-variable

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.monotonic() - self.start
        return False                   # do not swallow exceptions

with Timer() as t:
    do_work()
print(t.elapsed)
```

`__exit__` receives the exception details (or None). Returning `True`
suppresses the exception; returning `False` (the usual choice) lets it
propagate. That decision is the whole error-handling story of context
managers: **cleanup always runs; failures stay visible.**

## The lightweight way: @contextmanager

For simple cases, a generator with `@contextmanager` reads better than a
class:

```python
from contextlib import contextmanager

@contextmanager
def indent_log(depth):
    print("  " * depth + ">")
    yield                        # everything before = __enter__, after = __exit__
    print("  " * depth + "<")
```

## Why not try/finally?

`with` **is** try/finally with a name and a protocol. The advantage is
reusability: write the cleanup once, use it at fifty call sites, and nothing
forgets it. Resource discipline — connections, locks, temp files — should be
invisible to callers, and context managers are the tool that makes it so.
""",
    "Context Manager: with đúng chuẩn",
    "Đảm bảo dọn dẹp với __enter__/__exit__ và @contextmanager.",
    """
`with` đảm bảo việc dọn dẹp **ngay cả khi exception bay xuyên qua**. Bạn dùng
nó hằng ngày với tệp — giờ tự viết một cái:

```python
class Timer:
    def __enter__(self):
        self.start = time.monotonic()
        return self                    # gắn vào biến sau as

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.monotonic() - self.start
        return False                   # không nuốt exception

with Timer() as t:
    do_work()
print(t.elapsed)
```

`__exit__` nhận thông tin exception (hoặc None). Trả `True` sẽ nuốt exception;
trả `False` (lựa chọn thường dùng) cho nó lan tiếp. Quyết định đó là toàn bộ
câu chuyện xử lý lỗi của context manager: **dọn dẹp luôn chạy; lỗi vẫn hiện
hữu.**

## Cách nhẹ nhàng: @contextmanager

Với trường hợp đơn giản, một generator với `@contextmanager` dễ đọc hơn class:

```python
from contextlib import contextmanager

@contextmanager
def indent_log(depth):
    print("  " * depth + ">")
    yield                        # trước yield = __enter__, sau yield = __exit__
    print("  " * depth + "<")
```

## Vì sao không try/finally?

`with` **chính là** try/finally có tên riêng và giao thức. Lợi thế là khả
năng tái sử dụng: viết dọn dẹp một lần, dùng ở năm mươi chỗ gọi, và không
chỗ nào quên nó. Kỷ luật tài nguyên — connection, lock, tệp tạm — nên vô hình
với người gọi, và context manager là công cụ làm được điều đó.
""",
)

# --- module 3 practice sets ---
write_practice(
    M3, "m3-iter-practice",
    "Iterator Drills",
    "Implement the protocol by hand, once, so you never fear it again.",
    "Luyện Iterator",
    "Tự cài đặt giao thức một lần để không bao giờ sợ nó nữa.",
    L3A, 25, "intermediate",
    [
        challenge(
            "pi3-iter-range-step", "RangeIterator",
            "Create a class RangeIter(start, stop, step) that is iterable and yields start, start+step, ... below stop. Implement __iter__ and __next__ (return self from __iter__).",
            "class RangeIter:\n    def __init__(self, start, stop, step):\n        pass\n",
            [
                ("yields the right values",
                 "assert list(RangeIter(0, 10, 3)) == [0, 3, 6, 9]",
                 "Stop when the next value would be >= stop."),
                ("works with step 1",
                 "assert list(RangeIter(2, 5, 1)) == [2, 3, 4]",
                 "Ordinary ascending range."),
                ("empty range",
                 "assert list(RangeIter(5, 5, 1)) == []",
                 "start >= stop means nothing to yield."),
            ],
            level="guided",
        ),
        challenge(
            "pi3-iter-cycles", "Finite Cycler",
            "Create a class Cycler(items) that loops over a finite list forever when used with next() directly, BUT supports it = iter(c) producing an iterator that cycles. Implement it as an iterator whose __next__ wraps around using modulo.",
            "class Cycler:\n    def __init__(self, items):\n        pass\n",
            [
                ("wraps around",
                 "from itertools import islice\nc = Cycler(['a', 'b'])\nassert list(islice(c, 5)) == ['a', 'b', 'a', 'b', 'a']",
                 "index % len(items) — StopIteration never fires."),
                ("empty cycler is iterable but yields nothing",
                 "from itertools import islice\nassert list(islice(Cycler([]), 3)) == []",
                 "Guard the empty case to avoid ZeroDivisionError."),
            ],
            level="independent",
        ),
    ],
    {
        "pi3-iter-range-step": vi_challenge("RangeIterator", "Tạo class RangeIter(start, stop, step) là iterable và phát start, start+step, ... dưới stop. Cài __iter__ và __next__ (__iter__ trả về self).", [("Phát đúng các giá trị", "Dừng khi giá trị kế tiếp sẽ là >= stop."), ("Hợp với step 1", "Range tăng dần thông thường."), ("Range rỗng", "start >= stop nghĩa là không phát gì.")]),
        "pi3-iter-cycles": vi_challenge("Cycler hữu hạn", "Tạo class Cycler(items) lặp qua một list hữu hạn mãi mãi khi dùng next() trực tiếp, đồng thời it = iter(c) cho ra iterator xoay vòng. Cài __next__ quay vòng bằng modulo.", [("Quay vòng", "index % len(items) — StopIteration không bao giờ nổ."), ("Cycler rỗng vẫn iterable nhưng không phát gì", "Chặn trường hợp rỗng để tránh ZeroDivisionError.")]),
    },
    solutions=[
        ("pi3-iter-range-step", "class RangeIter:\n    def __init__(self, start, stop, step):\n        self.cur = start\n        self.stop = stop\n        self.step = step\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.cur >= self.stop:\n            raise StopIteration\n        value = self.cur\n        self.cur += self.step\n        return value", "class RangeIter:\n    def __init__(self, start, stop, step):\n        self.cur = start\n        self.stop = stop\n        self.step = step\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.cur > self.stop:\n            raise StopIteration\n        value = self.cur\n        self.cur += self.step\n        return value"),
        ("pi3-iter-cycles", "class Cycler:\n    def __init__(self, items):\n        self.items = items\n        self.index = 0\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if not self.items:\n            raise StopIteration\n        value = self.items[self.index % len(self.items)]\n        self.index += 1\n        return value", "class Cycler:\n    def __init__(self, items):\n        self.items = items\n        self.index = 0\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        value = self.items[self.index % len(self.items)]\n        self.index += 1\n        return value"),
    ],
)

write_practice(
    M3, "m3-gen-practice",
    "Generator Drills",
    "Stream, filter lazily, and flatten nested data.",
    "Luyện Generator",
    "Stream, lọc lười biếng, và làm phẳng dữ liệu lồng nhau.",
    L3B, 30, "intermediate",
    [
        challenge(
            "pi3-gen-evens", "Even Stream",
            "Implement evens(limit) as a generator function yielding even numbers from 0 up to and including limit (if it is even).",
            "def evens(limit):\n    pass\n",
            [
                ("yields evens",
                 "assert list(evens(10)) == [0, 2, 4, 6, 8, 10]",
                 "step 2 from 0 while n <= limit."),
                ("odd limit stops below",
                 "assert list(evens(9)) == [0, 2, 4, 6, 8]",
                 "9 itself is not even — exclude it."),
                ("is lazy (a generator)",
                 "g = evens(100)\nimport types\nassert isinstance(g, types.GeneratorType)",
                 "Use yield — the function must return a generator, not a list."),
            ],
            level="imitation",
        ),
        challenge(
            "pi3-gen-parse", "Parsing Stream",
            "Implement parse_scores(lines) yielding int values for lines that are pure digits (after stripping whitespace), silently skipping anything else.",
            "def parse_scores(lines):\n    pass\n",
            [
                ("skips bad lines",
                 "assert list(parse_scores(['10', ' oops ', '42'])) == [10, 42]",
                 "strip() then str.isdigit() guards each line."),
                ("empty input",
                 "assert list(parse_scores([])) == []",
                 "Nothing in, nothing out."),
                ("all bad lines",
                 "assert list(parse_scores(['x', 'y'])) == []",
                 "A stream of garbage yields an empty stream."),
            ],
            level="guided",
        ),
        challenge(
            "pi3-gen-flatten", "Flatten One Level",
            "Implement flatten_once(nested) yielding items of a list of lists, one level deep, using yield from.",
            "def flatten_once(nested):\n    pass\n",
            [
                ("flattens one level",
                 "assert list(flatten_once([[1, 2], [3], [], [4, 5]])) == [1, 2, 3, 4, 5]",
                 "yield from sublist for each sublist."),
                ("handles empty outer",
                 "assert list(flatten_once([])) == []",
                 "No sublists, nothing yielded."),
            ],
            level="independent",
        ),
    ],
    {
        "pi3-gen-evens": vi_challenge("Stream số chẵn", "Viết evens(limit) là generator function phát các số chẵn từ 0 đến và gồm cả limit (nếu nó chẵn).", [("Phát số chẵn", "Bước 2 từ 0 trong khi n <= limit."), ("Limit lẻ dừng dưới nó", "9 không chẵn — loại nó ra."), ("Phải lười (là generator)", "Dùng yield — hàm phải trả về generator, không phải list.")]),
        "pi3-gen-parse": vi_challenge("Stream phân tích", "Viết parse_scores(lines) phát các giá trị int cho những dòng thuần chữ số (sau khi strip khoảng trắng), lặng lẽ bỏ qua dòng khác.", [("Bỏ qua dòng lỗi", "strip() rồi str.isdigit() chặn từng dòng."), ("Input rỗng", "Không vào, không ra."), ("Toàn dòng lỗi", "Stream rác cho ra stream rỗng.")]),
        "pi3-gen-flatten": vi_challenge("Làm phẳng một mức", "Viết flatten_once(nested) phát các phần tử của list chứa list, sâu một mức, dùng yield from.", [("Làm phẳng một mức", "yield from sublist cho từng sublist."), ("Xử lý list ngoài rỗng", "Không có sublist, không phát gì.")]),
    },
    solutions=[
        ("pi3-gen-evens", "def evens(limit):\n    n = 0\n    while n <= limit:\n        yield n\n        n += 2", "def evens(limit):\n    n = 0\n    while n < limit:\n        yield n\n        n += 2"),
        ("pi3-gen-parse", "def parse_scores(lines):\n    for line in lines:\n        cleaned = line.strip()\n        if cleaned.isdigit():\n            yield int(cleaned)", "def parse_scores(lines):\n    for line in lines:\n        cleaned = line.strip()\n        try:\n            yield int(cleaned)\n        except ValueError:\n            continue"),
        ("pi3-gen-flatten", "def flatten_once(nested):\n    for sublist in nested:\n        yield from sublist", "def flatten_once(nested):\n    for sublist in nested:\n        yield sublist"),
    ],
)

write_practice(
    M3, "m3-ctx-practice",
    "Context Manager Drills",
    "Guarantee cleanup with both class-based and generator-based managers.",
    "Luyện Context Manager",
    "Đảm bảo dọn dẹp với cả hai dạng: class và generator.",
    L3C, 25, "intermediate",
    [
        challenge(
            "pi3-ctx-tracker", "Session Tracker",
            "Create a class Session with __enter__ returning the string 'open' and appending 'open' to a module-level list EVENTS; __exit__ appends 'closed' and returns False. After a with block, EVENTS must be ['open', 'closed'] even if the body raises.",
            "EVENTS = []\n\nclass Session:\n    pass\n",
            [
                ("normal flow",
                 "global EVENTS\nEVENTS.clear()\nwith Session() as s:\n    assert s == 'open'\nassert EVENTS == ['open', 'closed']",
                 "__enter__ appends and returns 'open'; __exit__ appends 'closed'."),
                ("cleanup on exception",
                 "global EVENTS\nEVENTS.clear()\ntry:\n    with Session():\n        raise RuntimeError('boom')\nexcept RuntimeError:\n    pass\nassert EVENTS == ['open', 'closed']",
                 "__exit__ must run even when the body raises — return False so the error still propagates."),
            ],
            level="guided",
        ),
        challenge(
            "pi3-ctx-suppress", "Quiet Zone",
            "Create a context manager using @contextmanager named quiet that SUPPRESSES ValueError raised in its body but lets other exceptions propagate. The with-body must run.",
            "from contextlib import contextmanager\n\n@contextmanager\ndef quiet():\n    pass\n",
            [
                ("suppresses ValueError",
                 "with quiet():\n    raise ValueError('ignored')\nprint('ok')",
                 "Catch ValueError inside the generator after yield; do not re-raise."),
                ("propagates others",
                 "try:\n    with quiet():\n        raise KeyError('boom')\n    failed = False\nexcept KeyError:\n    failed = True\nassert failed",
                 "Only ValueError is caught — everything else re-raises."),
            ],
            level="independent",
        ),
    ],
    {
        "pi3-ctx-tracker": vi_challenge("Tracked Session", "Tạo class Session với __enter__ trả về chuỗi 'open' và thêm 'open' vào list toàn cục EVENTS; __exit__ thêm 'closed' và trả về False. Sau khối with, EVENTS phải là ['open', 'closed'] ngay cả khi thân khối raise.", [("Luồng bình thường", "__enter__ thêm và trả về 'open'; __exit__ thêm 'closed'."), ("Dọn dẹp khi có exception", "__exit__ phải chạy cả khi thân khối raise — trả False để lỗi vẫn lan ra ngoài.")]),
        "pi3-ctx-suppress": vi_challenge("Vùng im lặng", "Tạo context manager bằng @contextmanager tên quiet NUỐT ValueError ném ra trong thân khối nhưng cho các exception khác lan truyền. Thân khối vẫn phải chạy.", [("Nuốt ValueError", "Bắt ValueError trong generator sau yield; không ném lại."), ("Các lỗi khác vẫn lan", "Chỉ bắt ValueError — mọi thứ khác ném lại.")]),
    },
    solutions=[
        ("pi3-ctx-tracker", "EVENTS = []\n\nclass Session:\n    def __enter__(self):\n        EVENTS.append('open')\n        return 'open'\n\n    def __exit__(self, exc_type, exc, tb):\n        EVENTS.append('closed')\n        return False", "EVENTS = []\n\nclass Session:\n    def __enter__(self):\n        EVENTS.append('open')\n        return 'open'\n\n    def __exit__(self, exc_type, exc, tb):\n        EVENTS.append('closed')\n        return True"),
        ("pi3-ctx-suppress", "from contextlib import contextmanager\n\n@contextmanager\ndef quiet():\n    try:\n        yield\n    except ValueError:\n        pass", "from contextlib import contextmanager\n\n@contextmanager\ndef quiet():\n    try:\n        yield\n    except Exception:\n        pass"),
    ],
)

# --- module 3 checkpoint ---
write_checkpoint(
    M3, L3D,
    "Checkpoint: Streaming Pipeline",
    "Compose generators into a memory-safe pipeline over a big input.",
    20,
    """
Streams everywhere: logs, exports, sensor feeds. Your checkpoint: build a
**pipeline** of generator stages over a list of log lines — filter, parse,
transform — without ever materializing the whole result.

**Working with AI:** a good prompt is "review my pipeline for stages that
accidentally build full lists in memory" — asking AI to find the lazy/eager
boundary is a real skill.
""",
    "Checkpoint: Pipeline dạng Stream",
    "Ghép các generator thành pipeline tiết kiệm bộ nhớ trên input lớn.",
    """
Stream ở khắp nơi: log, file xuất, dữ liệu cảm biến. Checkpoint của bạn:
dựng **pipeline** các tầng generator trên một list dòng log — lọc, phân tích,
biến đổi — mà không bao giờ dựng toàn bộ kết quả trong bộ nhớ.

**Làm việc cùng AI:** một prompt tốt là "review pipeline của tôi và chỉ ra
tầng nào vô tình dựng cả list trong bộ nhớ" — nhờ AI tìm ranh giới
lười/chăm là một kỹ năng thật.
""",
    challenge(
        "pi3-ckpt-pipeline", "Log Pipeline",
        "Implement error_rate(lines) — lines are strings like 'ERROR: disk full' or 'INFO: ok'. Yield-free helper allowed. Return the fraction (round to 2 decimals) of lines that start with 'ERROR: ', ignoring blank/whitespace-only lines. Use a generator pipeline internally (no full-list copies of filtered results). Empty/blank-only input returns 0.0.",
        "def error_rate(lines):\n    pass\n",
        [
            ("computes the fraction",
             "lines = ['ERROR: a', 'INFO: b', 'ERROR: c', 'INFO: d']\nassert error_rate(lines) == 0.5",
             "2 of 4 lines are errors → 0.5."),
            ("ignores blank lines",
             "lines = ['ERROR: a', '   ', '', 'INFO: b']\nassert error_rate(lines) == 0.5",
             "Blank lines are not denominator food."),
            ("empty input",
             "assert error_rate([]) == 0.0",
             "No lines → 0.0, never ZeroDivisionError."),
            ("rounds to two decimals",
             "lines = ['ERROR: a'] + ['INFO: x'] * 3\nassert error_rate(lines) == 0.25",
             "round(value, 2)."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Pipeline log",
        "Viết error_rate(lines) — lines là các chuỗi dạng 'ERROR: disk full' hoặc 'INFO: ok'. Trả về tỉ lệ (làm tròn 2 chữ số) các dòng bắt đầu bằng 'ERROR: ', bỏ qua dòng rỗng/chỉ-whitespace. Dùng pipeline generator bên trong (không sao chép cả list kết quả lọc). Input rỗng/toàn rỗng trả 0.0.",
        [
            ("Tính đúng tỉ lệ", "2/4 dòng là lỗi → 0.5."),
            ("Bỏ qua dòng rỗng", "Dòng rỗng không được tính vào mẫu số."),
            ("Input rỗng", "Không dòng nào → 0.0, không bao giờ ZeroDivisionError."),
            ("Làm tròn 2 chữ số", "round(giá trị, 2)."),
        ],
    ),
    solution="def error_rate(lines):\n    total = 0\n    hit = 0\n    for l in (l for l in lines if l.strip()):\n        total += 1\n        if l.startswith('ERROR: '):\n            hit += 1\n    return round(hit / total, 2) if total else 0.0",
    wrong="def error_rate(lines):\n    meaningful = [l for l in lines if l.strip()]\n    if not meaningful:\n        return 0.0\n    errors = [l for l in meaningful if not l.startswith('ERROR: ')]\n    return round(len(errors) / len(meaningful), 2)",
)

print("modules 3 done")
