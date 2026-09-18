#!/usr/bin/env python3
"""Python Intermediate — modules 1 (pythonic-toolkit) and 2 (objects-and-modeling)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 1: pythonic-toolkit ============================
M1 = "pythonic-toolkit"
L1A = "comprehensions-and-unpacking"
L1B = "functions-as-values"
L1C = "sorting-with-key"
L1D = "checkpoint-pipelines"

write_module(
    M1,
    "Pythonic Toolkit",
    "Transform data the way working Python developers do: comprehensions, first-class functions, and key-based sorting.",
    "Bộ công cụ Pythonic",
    "Biến đổi dữ liệu như lập trình viên Python thực thụ: comprehension, hàm là giá trị, và sắp xếp theo key.",
    [L1A, L1B, L1C, L1D],
    ["m1-comp-practice", "m1-func-practice", "m1-sort-practice"],
)

write_lesson(
    M1, L1A,
    "Comprehensions and Unpacking",
    "Build lists, dicts, and sets declaratively — and unpack data in assignments.",
    14,
    """
Python can **build a collection from a rule** in one readable line. A list
comprehension reads like the sentence "for each item, keep/transform it":

```python
nums = [1, 2, 3, 4, 5]
squares = [n * n for n in nums]          # [1, 4, 9, 16, 25]
evens    = [n for n in nums if n % 2 == 0]  # filter with a trailing if
labels   = [f"id-{n}" for n in nums]     # transform each element
```

Dict and set comprehensions follow the same shape:

```python
words = ["tea", "coffee", "cola"]
lengths = {w: len(w) for w in words}     # dict: word -> length
unique  = {w[0] for w in words}          # set of first letters
```

Rule of thumb: if the comprehension needs more than one `if` or nested loops
that hurt to read, use a normal `for` loop instead. **Readability wins.**

## Unpacking

Assign multiple targets at once — Python destructures the right-hand side:

```python
point = (3, 8)
x, y = point                # x=3, y=8
a, b = b, a                 # the idiomatic swap
first, *rest = [10, 20, 30, 40]   # first=10, rest=[20, 30, 40]
*init, last = range(5)            # init=[0, 1, 2, 3], last=4
```

Star-unpacking also **merges** collections: `[*xs, *ys]` concatenates lists,
`{**d1, **d2}` merges dicts (later keys win).

## Why this matters at work

Data-shaped code is everywhere: cleaning rows, reshaping API payloads,
building lookup tables. Comprehensions make that intent visible instead of
 burying it in append-and-index bookkeeping.
""",
    "Comprehension và Unpacking",
    "Dựng list, dict, set một cách khai báo — và gán dữ liệu nhiều biến cùng lúc.",
    """
Python có thể **dựng một collection từ một quy tắc** chỉ trong một dòng dễ
đọc. List comprehension đọc như câu "với mỗi phần tử, giữ lại/biến đổi nó":

```python
nums = [1, 2, 3, 4, 5]
squares = [n * n for n in nums]          # [1, 4, 9, 16, 25]
evens    = [n for n in nums if n % 2 == 0]  # lọc bằng if phía sau
labels   = [f"id-{n}" for n in nums]     # biến đổi từng phần tử
```

Dict và set comprehension cũng cùng hình dạng đó:

```python
words = ["tea", "coffee", "cola"]
lengths = {w: len(w) for w in words}     # dict: từ -> độ dài
unique  = {w[0] for w in words}          # set các chữ cái đầu
```

Nguyên tắc: nếu comprehension cần hơn một `if` hoặc các vòng lặp lồng nhau
khó đọc, hãy dùng vòng `for` thường. **Tính dễ đọc thắng.**

## Unpacking (gán nhiều biến)

Gán nhiều đích cùng lúc — Python tự phân rã vế phải:

```python
point = (3, 8)
x, y = point                # x=3, y=8
a, b = b, a                 # cách hoán đổi chuẩn Python
first, *rest = [10, 20, 30, 40]   # first=10, rest=[20, 30, 40]
*init, last = range(5)            # init=[0, 1, 2, 3], last=4
```

Star-unpacking còn dùng để **gộp** collection: `[*xs, *ys]` nối list,
`{**d1, **d2}` gộp dict (key phía sau thắng).

## Vì sao điều này quan trọng

Mã xử lý dữ liệu ở khắp nơi: làm sạch từng dòng, định hình lại payload từ
API, dựng bảng tra cứu. Comprehension thể hiện ý định rõ ràng thay vì chôn
nó dưới các dòng append và đánh chỉ số.
""",
)

write_lesson(
    M1, L1B,
    "Functions as Values",
    "Pass behavior around: higher-order functions, lambdas, zip, enumerate, and closures.",
    14,
    """
In Python, a function is a **value** — you can store it, pass it, return it:

```python
def shout(text):
    return text.upper() + "!"

def whisper(text):
    return text.lower() + "..."

actions = [shout, whisper]          # functions in a list
for act in actions:
    print(act("hello"))             # call through the variable
```

A function that takes or returns another function is **higher-order** — the
foundation of callbacks, decorators, and plugin systems:

```python
def apply_twice(fn, value):
    return fn(fn(value))

apply_twice(lambda n: n * 2, 3)     # 12
```

`lambda` is a one-expression anonymous function — perfect as a tiny throwaway
behavior, never for complex logic.

## zip and enumerate: the pair-programming duo

```python
names = ["An", "Binh", "Chi"]
scores = [8, 9, 7]
for name, score in zip(names, scores):      # walk two sequences together
    print(name, score)

for i, name in enumerate(names, start=1):   # index + value, cleanly
    print(i, name)
```

## Closures: functions that remember

An inner function can capture variables from the function that built it:

```python
def make_adder(n):
    def add(x):
        return x + n        # remembers n
    return add

add5 = make_adder(5)
add5(10)                    # 15
```

This "factory returning a configured function" pattern powers configuration,
middleware, and dependency wiring in real codebases.
""",
    "Hàm là Giá trị",
    "Truyền hành vi đi khắp nơi: hàm bậc cao, lambda, zip, enumerate, và closure.",
    """
Trong Python, hàm là một **giá trị** — bạn có thể lưu nó, truyền đi, trả về:

```python
def shout(text):
    return text.upper() + "!"

def whisper(text):
    return text.lower() + "..."

actions = [shout, whisper]          # hàm nằm trong list
for act in actions:
    print(act("hello"))             # gọi qua biến
```

Hàm nhận hoặc trả về hàm khác gọi là **hàm bậc cao** — nền tảng của callback,
decorator, và hệ thống plugin:

```python
def apply_twice(fn, value):
    return fn(fn(value))

apply_twice(lambda n: n * 2, 3)     # 12
```

`lambda` là hàm ẩn danh một biểu thức — hợp với hành vi nhỏ dùng một lần,
không dùng cho logic phức tạp.

## zip và enumerate: bộ đôi đi cùng nhau

```python
names = ["An", "Binh", "Chi"]
scores = [8, 9, 7]
for name, score in zip(names, scores):      # đi hai dãy song song
    print(name, score)

for i, name in enumerate(names, start=1):   # chỉ số + giá trị, sạch sẽ
    print(i, name)
```

## Closure: hàm nhớ bối cảnh của nó

Hàm bên trong có thể "bắt" biến từ hàm đã tạo ra nó:

```python
def make_adder(n):
    def add(x):
        return x + n        # nhớ n
    return add

add5 = make_adder(5)
add5(10)                    # 15
```

Mẫu "nhà máy trả về hàm đã cấu hình sẵn" này là nền của cấu hình, middleware,
và lắp ráp phụ thuộc trong codebase thật.
""",
)

write_lesson(
    M1, L1C,
    "Sorting with key",
    "Sort anything by any rule: the key= parameter, multi-level sorts, and stability.",
    12,
    """
`sorted()` never compares your objects directly — it compares the value your
**`key=` function** produces. One idea, and you can sort anything:

```python
words = ["banana", "fig", "cherry"]
sorted(words, key=len)              # by length: fig, banana, cherry

people = [
    {"name": "An", "age": 30},
    {"name": "Binh", "age": 25},
]
sorted(people, key=lambda p: p["age"])
```

**Descending and multi-level sorting** come free:

```python
scores = [("An", 8), ("Binh", 9), ("Chi", 8)]
sorted(scores, key=lambda p: p[1], reverse=True)      # highest first

# sort by age, then by name — return a tuple from key:
sorted(people, key=lambda p: (p["age"], p["name"]))
```

Two facts professionals rely on:

- **`sorted()` returns a new list; `list.sort()` mutates in place** (and returns `None` — a classic bug).
- **Sorts are stable**: equal keys keep their original order, so you can sort by secondary key first, then primary key.

## Why not compare functions?

`key=` decouples "what to compare" from "how to compare". Sorting records by
a field, files by size, tasks by deadline — all become one-liners instead of
hand-rolled comparison logic.
""",
    "Sắp xếp với key",
    "Sắp xếp bất kỳ thứ gì theo bất kỳ quy tắc nào: tham số key=, sắp nhiều mức, và tính ổn định.",
    """
`sorted()` không so sánh trực tiếp các đối tượng của bạn — nó so sánh giá trị
mà **hàm `key=`** trả về. Một ý tưởng duy nhất, và bạn sắp được mọi thứ:

```python
words = ["banana", "fig", "cherry"]
sorted(words, key=len)              # theo độ dài: fig, banana, cherry

people = [
    {"name": "An", "age": 30},
    {"name": "Binh", "age": 25},
]
sorted(people, key=lambda p: p["age"])
```

**Giảm dần và sắp nhiều mức** có sẵn luôn:

```python
scores = [("An", 8), ("Binh", 9), ("Chi", 8)]
sorted(scores, key=lambda p: p[1], reverse=True)      # cao trước

# sắp theo tuổi rồi theo tên — key trả về một tuple:
sorted(people, key=lambda p: (p["age"], p["name"]))
```

Hai điều lập trình viên siempre dựa vào:

- **`sorted()` trả list mới; `list.sort()` sửa tại chỗ** (và trả `None` — lỗi kinh điển).
- **Sắp xếp ổn định (stable)**: key bằng nhau giữ thứ tự gốc, nên có thể sắp key phụ trước rồi sắp key chính sau.

## Vì sao không tự viết hàm so sánh?

`key=` tách "so sánh cái gì" khỏi "so sánh thế nào". Sắp bản ghi theo trường,
tệp theo kích thước, công việc theo hạn chót — tất cả thành một dòng thay vì
tự viết logic so sánh thủ công.
""",
)

# --- module 1 practice sets ---
write_practice(
    M1, "m1-comp-practice",
    "Comprehension Drills",
    "Build, filter, and reshape collections in one line.",
    "Luyện Comprehension",
    "Dựng, lọc, và định hình lại collection chỉ trong một dòng.",
    L1A, 35, "intermediate",
    [
        challenge(
            "pi1-comp-squares", "Squares, One Line",
            "Implement squares(n) that returns the squares of 1..n as a list, using a list comprehension (no append, no loop variable bookkeeping).",
            "def squares(n):\n    pass\n",
            [
                ("squares first five",
                 "assert squares(5) == [1, 4, 9, 16, 25]",
                 "Each element should be i*i for i in 1..n."),
                ("squares of one",
                 "assert squares(1) == [1]",
                 "Edge case: n=1 → [1]."),
                ("squares of zero",
                 "assert squares(0) == []",
                 "Edge case: n=0 → empty list. A comprehension over an empty range yields []."),
            ],
            level="imitation",
        ),
        challenge(
            "pi1-comp-filter", "Keep the Long Words",
            "Implement long_words(words, min_len) returning only words with length >= min_len, using a comprehension with a filter.",
            "def long_words(words, min_len):\n    pass\n",
            [
                ("filters short words",
                 'assert long_words(["tea", "coffee", "cola"], 5) == ["coffee"]',
                 "Keep only words whose len() is at least min_len."),
                ("keeps everything when min_len is 1",
                 'assert long_words(["a", "bb"], 1) == ["a", "bb"]',
                 "min_len=1 keeps all non-empty words."),
                ("empty input gives empty output",
                 "assert long_words([], 3) == []",
                 "An empty input list must produce an empty list."),
            ],
            level="guided",
        ),
        challenge(
            "pi1-comp-dict", "Word Length Lookup",
            "Implement length_lookup(words) returning a dict mapping each word to its length, using a dict comprehension.",
            "def length_lookup(words):\n    pass\n",
            [
                ("maps words to lengths",
                 'assert length_lookup(["tea", "cola"]) == {"tea": 3, "cola": 4}',
                 "{w: len(w) for w in words}."),
                ("handles duplicates by keeping one entry",
                 'assert length_lookup(["hi", "hi"]) == {"hi": 2}',
                 "Dict keys are unique; duplicates collapse to one entry."),
                ("empty list gives empty dict",
                 "assert length_lookup([]) == {}",
                 "Edge case: no words → {}."),
            ],
            level="guided",
        ),
        challenge(
            "pi1-unpack-head-tail", "Head and Tail",
            "Implement head_tail(items) that returns a tuple (first, rest) where rest is a list of everything after the first item. Use unpacking, not slicing, and return (None, []) for an empty input.",
            "def head_tail(items):\n    pass\n",
            [
                ("splits a list",
                 "assert head_tail([1, 2, 3]) == (1, [2, 3])",
                 "first, *rest = items does exactly this."),
                ("single element",
                 "assert head_tail([7]) == (7, [])",
                 "With one element, rest is empty."),
                ("empty input",
                 "assert head_tail([]) == (None, [])",
                 "Handle the empty case explicitly before unpacking."),
            ],
            level="independent",
        ),
    ],
    {
        "pi1-comp-squares": vi_challenge("Bình phương một dòng", "Viết squares(n) trả về list các bình phương từ 1..n, dùng list comprehension (không append, không quản lý biến vòng lặp).", [("Năm bình phương đầu", "Mỗi phần tử là i*i với i chạy 1..n."), ("Một phần tử", "Trường hợp n=1 → [1]."), ("Không phần tử", "Trường hợp n=0 → list rỗng. Comprehension trên range rỗng cho ra [].")]),
        "pi1-comp-filter": vi_challenge("Giữ từ dài", "Viết long_words(words, min_len) trả về các từ có độ dài >= min_len, dùng comprehension có lọc.", [("Lọc từ ngắn", "Chỉ giữ từ có len() ít nhất min_len."), ("min_len = 1 giữ tất cả", "min_len=1 giữ mọi từ khác rỗng."), ("Vào rỗng ra rỗng", "List rỗng phải cho list rỗng.")]),
        "pi1-comp-dict": vi_challenge("Bảng tra độ dài", "Viết length_lookup(words) trả về dict ánh xạ mỗi từ với độ dài của nó, dùng dict comprehension.", [("Ánh xạ từ -> độ dài", "{w: len(w) for w in words}."), ("Trùng lặp gộp một entry", "Key của dict là duy nhất; từ trùng chỉ còn một entry."), ("List rỗng cho dict rỗng", "Trường hợp đặc biệt: không có từ → {}.")]),
        "pi1-unpack-head-tail": vi_challenge("Đầu và Đuôi", "Viết head_tail(items) trả về tuple (first, rest) trong đó rest là list mọi phần tử sau phần tử đầu. Dùng unpacking, không dùng slicing; với input rỗng trả (None, []).", [("Tách một list", "first, *rest = items làm đúng việc này."), ("Một phần tử", "Với một phần tử, rest là list rỗng."), ("Input rỗng", "Xử lý trường hợp rỗng rõ ràng trước khi unpack.")]),
    },
    solutions=[
        ("pi1-comp-squares", "def squares(n):\n    return [i * i for i in range(1, n + 1)]", "def squares(n):\n    return [i * i for i in range(n)]"),
        ("pi1-comp-filter", "def long_words(words, min_len):\n    return [w for w in words if len(w) >= min_len]", "def long_words(words, min_len):\n    return [w for w in words if len(w) > min_len]"),
        ("pi1-comp-dict", "def length_lookup(words):\n    return {w: len(w) for w in words}", "def length_lookup(words):\n    return [len(w) for w in words]"),
        ("pi1-unpack-head-tail", "def head_tail(items):\n    if not items:\n        return (None, [])\n    first, *rest = items\n    return (first, rest)", "def head_tail(items):\n    if not items:\n        return (None, [])\n    first, *rest = items\n    return (rest, first)"),
    ],
)

write_practice(
    M1, "m1-func-practice",
    "Higher-Order Function Drills",
    "Write functions that accept, return, and remember.",
    "Luyện Hàm Bậc Cao",
    "Viết hàm nhận hàm, trả về hàm, và ghi nhớ bối cảnh.",
    L1B, 30, "intermediate",
    [
        challenge(
            "pi1-fn-apply-twice", "Apply Twice",
            "Implement apply_twice(fn, value) that applies fn two times: fn(fn(value)).",
            "def apply_twice(fn, value):\n    pass\n",
            [
                ("doubles twice",
                 'assert apply_twice(lambda n: n * 2, 3) == 12',
                 "fn(fn(3)) with doubling: 3 → 6 → 12."),
                ("works with string functions",
                 'assert apply_twice(str.strip, "  hi  ") == "hi"',
                 "str.strip works as a first-class function value."),
            ],
            level="guided",
        ),
        challenge(
            "pi1-fn-compose", "Compose",
            "Implement compose(f, g) returning a new function h where h(x) == f(g(x)) — g runs first, then f.",
            "def compose(f, g):\n    pass\n",
            [
                ("g first then f",
                 'h = compose(lambda n: n + 1, lambda n: n * 2)\nassert h(5) == 11',
                 "g(5)=10 first, then f(10)=11."),
                ("returns a callable",
                 "h = compose(str, len)\nassert h('abcd') == '4'",
                 "len('abcd')=4 first, then str(4)='4'."),
            ],
            level="independent",
        ),
        challenge(
            "pi1-fn-make-adder", "Adder Factory",
            "Implement make_adder(n) returning a function that adds n to its argument. This is a closure: the returned function remembers n.",
            "def make_adder(n):\n    pass\n",
            [
                ("remembers its n",
                 "add3 = make_adder(3)\nassert add3(10) == 13",
                 "The inner function must capture n from make_adder."),
                ("independent adders",
                 "a = make_adder(1)\nb = make_adder(100)\nassert a(0) == 1 and b(0) == 100",
                 "Each returned function keeps its own captured n."),
            ],
            level="independent",
        ),
    ],
    {
        "pi1-fn-apply-twice": vi_challenge("Áp dụng hai lần", "Viết apply_twice(fn, value) áp dụng fn hai lần: fn(fn(value)).", [("Nhân đôi hai lần", "fn(fn(3)) với phép nhân đôi: 3 → 6 → 12."), ("Hợp với hàm chuỗi", "str.strip là một giá trị hàm chính danh.")]),
        "pi1-fn-compose": vi_challenge("Compose", "Viết compose(f, g) trả về hàm mới h sao cho h(x) == f(g(x)) — g chạy trước, f chạy sau.", [("g trước, f sau", "g(5)=10 trước, rồi f(10)=11."), ("Trả về một hàm gọi được", "len('abcd')=4 trước, rồi str(4)='4'.")]),
        "pi1-fn-make-adder": vi_challenge("Nhà máy Adder", "Viết make_adder(n) trả về một hàm cộng n vào tham số của nó. Đây là closure: hàm trả về phải nhớ n.", [("Nhớ n của nó", "Hàm bên trong phải bắt n từ make_adder."), ("Các adder độc lập", "Mỗi hàm trả về giữ n riêng của nó.")]),
    },
    solutions=[
        ("pi1-fn-apply-twice", "def apply_twice(fn, value):\n    return fn(fn(value))", "def apply_twice(fn, value):\n    return fn(value)"),
        ("pi1-fn-compose", "def compose(f, g):\n    def h(x):\n        return f(g(x))\n    return h", "def compose(f, g):\n    def h(x):\n        return g(f(x))\n    return h"),
        ("pi1-fn-make-adder", "def make_adder(n):\n    def add(x):\n        return x + n\n    return add", "def make_adder(n):\n    def add(x):\n        return x + n\n    return add(n)"),
    ],
)

write_practice(
    M1, "m1-sort-practice",
    "Sorting with key",
    "Sort records, multi-level, and top-N with key functions.",
    "Sắp xếp với key",
    "Sắp bản ghi, nhiều mức, và top-N bằng key function.",
    L1C, 30, "intermediate",
    [
        challenge(
            "pi1-sort-by-len", "By Length",
            "Implement by_length(words) returning a NEW list sorted by word length (shortest first). Use sorted with key=len. Do not modify the input list.",
            "def by_length(words):\n    pass\n",
            [
                ("sorts by length",
                 'assert by_length(["ccc", "a", "bb"]) == ["a", "bb", "ccc"]',
                 "sorted(words, key=len) — shortest first."),
                ("does not mutate input",
                 'src = ["bb", "a"]\nby_length(src)\nassert src == ["bb", "a"]',
                 "Use sorted() (returns new list), not list.sort()."),
                ("stable for equal lengths",
                 'assert by_length(["bb", "aa"]) == ["bb", "aa"]',
                 "Python sorts are stable: equal keys keep original order."),
            ],
            level="imitation",
        ),
        challenge(
            "pi1-sort-records", "Sort Records by Field",
            "Given a list of product dicts with 'name' and 'price', implement cheapest_first(products) returning a new list sorted by ascending price.",
            "def cheapest_first(products):\n    pass\n",
            [
                ("sorts by price",
                 'ps = [{"name": "B", "price": 9}, {"name": "A", "price": 3}]\nassert [p["name"] for p in cheapest_first(ps)] == ["A", "B"]',
                 "Sort with key=lambda p: p['price']."),
                ("input order preserved on ties (stable)",
                 'ps = [{"name": "X", "price": 5}, {"name": "Y", "price": 5}]\nassert [p["name"] for p in cheapest_first(ps)] == ["X", "Y"]',
                 "Equal prices keep original order — stable sort."),
            ],
            level="guided",
        ),
        challenge(
            "pi1-sort-top", "Top N by Score",
            "Implement top_n(players, n) where players is a list of (name, score) tuples. Return a list of the n highest scores' names, highest first. Break ties by keeping the earlier player first (stable sort).",
            "def top_n(players, n):\n    pass\n",
            [
                ("top scores first",
                 'ps = [("An", 8), ("Binh", 9), ("Chi", 7)]\nassert top_n(ps, 2) == ["Binh", "An"]',
                 "Sort by score descending, then take the first n names."),
                ("n larger than list",
                 'ps = [("An", 8)]\nassert top_n(ps, 5) == ["An"]',
                 "Slicing beyond the end is safe: it returns everything available."),
                ("ties keep original order",
                 'ps = [("Chi", 8), ("An", 8)]\nassert top_n(ps, 2) == ["Chi", "An"]',
                 "Do not reverse the list — use reverse=True in sorted to keep stability."),
            ],
            level="combination",
        ),
    ],
    {
        "pi1-sort-by-len": vi_challenge("Theo độ dài", "Viết by_length(words) trả về list MỚI được sắp theo độ dài từ (ngắn trước). Dùng sorted với key=len. Không được sửa list gốc.", [("Sắp theo độ dài", "sorted(words, key=len) — ngắn trước."), ("Không làm biến đổi input", "Dùng sorted() (trả list mới), không phải list.sort()."), ("Ổn định với độ dài bằng nhau", "Sắp xếp của Python ổn định: key bằng nhau giữ thứ tự gốc.")]),
        "pi1-sort-records": vi_challenge("Sắp bản ghi theo trường", "Cho list các dict sản phẩm có 'name' và 'price', viết cheapest_first(products) trả về list mới sắp theo giá tăng dần.", [("Sắp theo giá", "Sắp với key=lambda p: p['price']."), ("Giá bằng nhau giữ thứ tự gốc (ổn định)", "Giá bằng nhau giữ thứ tự ban đầu — sắp ổn định.")]),
        "pi1-sort-top": vi_challenge("Top N theo điểm", "Viết top_n(players, n) với players là list các tuple (name, score). Trả về list tên của n điểm cao nhất, cao trước. Điểm bằng nhau thì người xuất hiện trước đứng trước (sắp ổn định).", [("Điểm cao trước", "Sắp theo điểm giảm dần rồi lấy n tên đầu."), ("n lớn hơn list", "Cắt vượt quá cuối là an toàn: trả về mọi thứ có sẵn."), ("Điểm bằng nhau giữ thứ tự", "Không dùng [::-1] — hãy dùng reverse=True trong sorted để giữ tính ổn định.")]),
    },
    solutions=[
        ("pi1-sort-by-len", "def by_length(words):\n    return sorted(words, key=len)", "def by_length(words):\n    result = words[:]\n    result.sort(key=len, reverse=True)\n    return result"),
        ("pi1-sort-records", "def cheapest_first(products):\n    return sorted(products, key=lambda p: p['price'])", "def cheapest_first(products):\n    return sorted(products, key=lambda p: p['name'])"),
        ("pi1-sort-top", "def top_n(players, n):\n    ranked = sorted(players, key=lambda p: p[1], reverse=True)\n    return [name for name, score in ranked[:n]]", "def top_n(players, n):\n    ranked = sorted(players, key=lambda p: p[1])\n    return [name for name, score in ranked[-n:]]"),
    ],
)

# --- module 1 checkpoint ---
write_checkpoint(
    M1, L1D,
    "Checkpoint: Data Pipelines",
    "Combine comprehensions, closures, and key-based sorting into one pipeline.",
    20,
    """
One checkpoint challenge — no new theory. You will build a small **data
pipeline**: filter → transform → aggregate → rank. This is the daily shape of
real data work, and it exercises everything in this module.

Write `summarize(transactions)` where each transaction is a dict with
`category` and `amount`. Return a list of `(category, total)` tuples for
**positive amounts only**, sorted by total descending (ties: alphabetical
category). Aim for a solution built from comprehensions and `sorted(key=)` —
no manual index bookkeeping.

**Working with AI:** ask a mentor for *test cases you might be missing*
(negative amounts? empty input? one category?) before you look at any
generated solution — generating tests first is an engineering skill, not a
shortcut.
""",
    "Checkpoint: Đường ống dữ liệu",
    "Kết hợp comprehension, closure, và sắp xếp theo key thành một pipeline.",
    """
Một thử thách checkpoint — không có lý thuyết mới. Bạn sẽ dựng một **đường
ống dữ liệu** nhỏ: lọc → biến đổi → tổng hợp → xếp hạng. Đây là hình dạng
hàng ngày của công việc dữ liệu thật, và nó sử dụng mọi thứ trong module này.

Viết `summarize(transactions)` trong đó mỗi giao dịch là một dict có
`category` và `amount`. Trả về list các tuple `(category, total)` cho
**chỉ các amount dương**, sắp theo tổng giảm dần (bằng nhau: category theo
alphabet). Hãy hướng tới lời giải dựng từ comprehension và `sorted(key=)` —
không quản lý chỉ số thủ công.

**Làm việc cùng AI:** hãy hỏi mentor *những test case bạn còn thiếu*
(amount âm? input rỗng? một category?) trước khi xem bất kỳ lời giải nào do
AI tạo — tự sinh test trước là một kỹ năng kỹ thuật, không phải lối tắt.
""",
    challenge(
        "pi1-ckpt-pipeline", "Transaction Summarizer",
        "Implement summarize(transactions) — each item is a dict with 'category' and 'amount'. Return a list of (category, total) tuples counting ONLY positive amounts, sorted by total descending; ties broken alphabetically by category.",
        "def summarize(transactions):\n    pass\n",
        [
            ("aggregates positive amounts only",
             'tx = [{"category": "food", "amount": 10}, {"category": "food", "amount": 5}, {"category": "fun", "amount": -3}]\nassert summarize(tx) == [("food", 15)]',
             "Skip negative amounts, then sum per category."),
            ("sorted by total descending",
             'tx = [{"category": "a", "amount": 1}, {"category": "b", "amount": 9}]\nassert summarize(tx) == [("b", 9), ("a", 1)]',
             "Rank by total, highest first."),
            ("ties are alphabetical",
             'tx = [{"category": "b", "amount": 5}, {"category": "a", "amount": 5}]\nassert summarize(tx) == [("a", 5), ("b", 5)]',
             "Sort key should be (-total, category) or two passes."),
            ("empty input",
             "assert summarize([]) == []",
             "No transactions → empty summary."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Bộ tổng hợp giao dịch",
        "Viết summarize(transactions) — mỗi phần tử là dict có 'category' và 'amount'. Trả về list tuple (category, total) chỉ tính amount dương, sắp theo tổng giảm dần; bằng nhau thì theo alphabet của category.",
        [
            ("Chỉ tổng hợp amount dương", "Bỏ qua amount âm, rồi cộng theo category."),
            ("Sắp theo tổng giảm dần", "Xếp hạng theo tổng, cao trước."),
            ("Bằng nhau thì theo alphabet", "Key sắp nên là (-total, category) hoặc sắp hai lượt."),
            ("Input rỗng", "Không có giao dịch → danh sách rỗng."),
        ],
    ),
    solution="def summarize(transactions):\n    totals = {}\n    for tx in transactions:\n        if tx['amount'] > 0:\n            totals[tx['category']] = totals.get(tx['category'], 0) + tx['amount']\n    return sorted(totals.items(), key=lambda item: (-item[1], item[0]))",
    wrong="def summarize(transactions):\n    totals = {}\n    for tx in transactions:\n        totals[tx['category']] = totals.get(tx['category'], 0) + tx['amount']\n    return sorted(totals.items(), key=lambda item: (item[1], item[0]))",
)

# ============================ MODULE 2: objects-and-modeling ============================
M2 = "objects-and-modeling"
L2A = "classes-basics"
L2B = "properties-validation"
L2C = "dataclasses"
L2D = "composition-over-inheritance"
L2E = "checkpoint-modeling"

write_module(
    M2,
    "Objects and Modeling",
    "Model the domain with classes, validated properties, dataclasses — and composition over inheritance.",
    "Đối tượng và Mô hình hóa",
    "Mô hình hóa bài toán bằng class, property có kiểm tra, dataclass — và ưu tiên composition hơn inheritance.",
    [L2A, L2B, L2C, L2D, L2E],
    ["m2-cls-practice", "m2-prop-practice", "m2-dc-practice", "m2-comp-practice"],
)

write_lesson(
    M2, L2A,
    "Classes: State plus Behavior",
    "Define your own types with __init__, methods, __str__, and __repr__.",
    15,
    """
A **class** bundles state (attributes) with the behavior that operates on it
(methods). `__init__` runs at creation; `self` is the instance being worked on:

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def reading_time(self, minutes_per_page=2):
        return self.pages * minutes_per_page

book = Book("Fluent Python", 780)
book.reading_time()        # 1560 — method call binds book as self
```

## Two dunders every serious class defines

- `__repr__`: **unambiguous**, for developers — ideally code that rebuilds the object.
- `__str__`: **readable**, for end users (falls back to `__repr__` if absent).

```python
class Book:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Book({self.title!r})"

    def __str__(self):
        return self.title
```

In a REPL or traceback you see the `repr`; in `print()` you see the `str`.
Without them you get `<Book object at 0x...>` — useless when debugging.

## Class attributes vs instance attributes

An attribute assigned at class level is **shared** by all instances
(constants, counters). Instance attributes (assigned via `self.`) belong to
one object. Default to instance attributes; reach for class attributes only
for genuinely shared data.
""",
    "Class: Trạng thái cộng Hành vi",
    "Tự định nghĩa kiểu dữ liệu với __init__, method, __str__, và __repr__.",
    """
**Class** gói trạng thái (attribute) cùng với hành vi thao tác trên nó
(method). `__init__` chạy khi tạo đối tượng; `self` là thực thể đang được
xử lý:

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def reading_time(self, minutes_per_page=2):
        return self.pages * minutes_per_page

book = Book("Fluent Python", 780)
book.reading_time()        # 1560 — lời gọi method gắn book vào self
```

## Hai dunder mà mọi class nghiêm túc nên định nghĩa

- `__repr__`: **không mơ hồ**, cho lập trình viên — tốt nhất là đoạn code dựng lại được đối tượng.
- `__str__`: **dễ đọc**, cho người dùng cuối (nếu thiếu, Python dùng `__repr__` thay).

```python
class Book:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Book({self.title!r})"

    def __str__(self):
        return self.title
```

Trong REPL hay traceback bạn thấy `repr`; trong `print()` bạn thấy `str`.
Không có chúng, bạn nhận được `<Book object at 0x...>` — vô dụng khi gỡ lỗi.

## Class attribute và instance attribute

Attribute gán ở mức class được **chia sẻ** giữa mọi thực thể (hằng số, bộ
đếm). Instance attribute (gán qua `self.`) thuộc về một đối tượng. Mặc định
dùng instance attribute; chỉ dùng class attribute cho dữ liệu thực sự chung.
""",
)

write_lesson(
    M2, L2B,
    "Properties: Controlled Attributes",
    "Validate on assignment with @property — keep the simple attribute syntax.",
    13,
    """
Beginners write `obj.age = 300` and hope for the best. Intermediate
developers make **invalid states impossible** — without giving up the simple
attribute syntax. That is exactly what `@property` is for:

```python
class Person:
    def __init__(self, age):
        self.age = age          # goes through the setter below!

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not (0 <= value <= 150):
            raise ValueError(f"age must be 0..150, got {value}")
        self._age = value
```

Now `Person(-5)` raises immediately, and so does `p.age = -1`. The
convention: the public name `age` is a property; the raw value lives in
`_age` (single underscore = internal).

## Read-only computed properties

A property with only a getter is **read-only** — perfect for values derived
from real state:

```python
class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h

    @property
    def area(self):
        return self.w * self.h      # no setter: cannot assign
```

`r.area = 99` now raises `AttributeError` — a good kind of error, because
area was never independent state.

## Why properties instead of get_x()/set_x()?

Python style is to expose attributes directly and *upgrade to properties
later if rules appear* — callers never change. Java-style getters/setters on
every field are noise. Validate at the boundary where bad data enters, and
keep the rest plain.
""",
    "Property: Thuộc tính có kiểm soát",
    "Kiểm tra dữ liệu khi gán bằng @property — vẫn giữ cú pháp attribute đơn giản.",
    """
Người mới viết `obj.age = 300` rồi cầu may. Lập trình viên trung cấp làm cho
**trạng thái sai trở nên bất khả thi** — mà không từ bỏ cú pháp attribute đơn
giản. `@property` sinh ra chính cho việc đó:

```python
class Person:
    def __init__(self, age):
        self.age = age          # đi qua setter bên dưới!

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not (0 <= value <= 150):
            raise ValueError(f"age must be 0..150, got {value}")
        self._age = value
```

Giờ `Person(-5)` báo lỗi ngay lập tức, và `p.age = -1` cũng vậy. Quy ước:
tên công khai `age` là một property; giá trị thô nằm trong `_age` (một gạch
dưới = nội bộ).

## Property chỉ đọc

Property chỉ có getter là **chỉ đọc** — hoàn hảo cho giá trị suy ra từ trạng
thái thật:

```python
class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h

    @property
    def area(self):
        return self.w * self.h      # không setter: không thể gán
```

`r.area = 99` giờ raises `AttributeError` — một lỗi tốt, vì area chưa bao giờ
là trạng thái độc lập.

## Vì sao dùng property thay vì get_x()/set_x()?

Phong cách Python là để lộ attribute trực tiếp và *nâng cấp thành property
sau nếu có quy tắc xuất hiện* — code gọi không phải thay đổi. Kiểu
getter/setter Java trên mọi trường chỉ là nhiễu. Hãy kiểm tra dữ liệu tại
ranh giới nơi dữ liệu xấu đi vào, và giữ phần còn lại thuần túy.
""",
)

write_lesson(
    M2, L2C,
    "Dataclasses: Model Data Fast",
    "@dataclass generates __init__, __repr__, and __eq__ so you model, not boilerplate.",
    13,
    """
Most classes are mostly **data**. Writing `__init__`, `__repr__`, and
`__eq__` by hand for each one is boilerplate with bug surface. `@dataclass`
generates all three from your field declarations:

```python
from dataclasses import dataclass, field

@dataclass
class Task:
    title: str
    priority: int = 1
    tags: list = field(default_factory=list)   # safe mutable default

task = Task("ship release", 2)
task == Task("ship release", 2)     # True — __eq__ compares fields
repr(task)                          # Task(title='ship release', ...)
```

Three details professionals know:

- **Mutable defaults need `field(default_factory=list)`** — a bare `tags=[]` would share one list across all instances (same trap as `def f(x=[])`).
- **`frozen=True`** makes instances immutable and hashable — great for value objects like `Money` or `Point`.
- **`__post_init__`** runs after `__init__` for cross-field validation.

## When to use which

Plain class → behavior-heavy objects with complex lifecycle. Dataclass →
data records: rows, configs, messages, DTOs. Reaching for a dataclass first
is a signal you're thinking about **data shape**, which usually makes better
designs than thinking about inheritance hierarchies.
""",
    "Dataclass: Mô hình hóa dữ liệu nhanh",
    "@dataclass sinh sẵn __init__, __repr__, __eq__ để bạn mô tả dữ liệu thay vì viết code mẫu.",
    """
Phần lớn class chủ yếu là **dữ liệu**. Tự viết `__init__`, `__repr__`, và
`__eq__` cho từng lớp là code mẫu với đầy đủ chỗ phát sinh lỗi. `@dataclass`
sinh ra cả ba từ chính khai báo trường của bạn:

```python
from dataclasses import dataclass, field

@dataclass
class Task:
    title: str
    priority: int = 1
    tags: list = field(default_factory=list)   # default mutable an toàn

task = Task("ship release", 2)
task == Task("ship release", 2)     # True — __eq__ so từng trường
repr(task)                          # Task(title='ship release', ...)
```

Ba chi tiết lập trình viên cần biết:

- **Default mutable cần `field(default_factory=list)`** — `tags=[]` trần trụi sẽ chia sẻ một list cho mọi thực thể (cùng bẫy với `def f(x=[])`).
- **`frozen=True`** khiến thực thể bất biến và hashable — hợp với value object như `Money` hay `Point`.
- **`__post_init__`** chạy sau `__init__` để kiểm tra chéo giữa các trường.

## Chọn cái nào khi nào

Class thường → đối tượng nặng hành vi với vòng đời phức tạp. Dataclass →
bản ghi dữ liệu: dòng dữ liệu, cấu hình, message, DTO. Ưu tiên dataclass
trước là tín hiệu bạn đang nghĩ về **hình dạng dữ liệu** — thứ thường cho ra
thiết kế tốt hơn là nghĩ về cây thừa kế.
""",
)

write_lesson(
    M2, L2D,
    "Composition over Inheritance",
    "Build objects from parts you can swap — has-a beats is-a in most real designs.",
    14,
    """
Inheritance is the most misused tool in OOP. Before reaching for `class
Admin(User)`, ask: **is Admin really *a kind of* User in every behavior —
forever?** Often what you want is *has-a*: the object **uses** a part.

```python
class Engine:
    def start(self):
        return "vroom"

class Car:                      # Car HAS-An Engine — no inheritance
    def __init__(self, engine):
        self.engine = engine    # injected from outside

    def start(self):
        return self.engine.start()

Car(Engine()).start()           # "vroom"
Car(LoudEngine()).start()       # swap parts freely — duck typing
```

The engine is **injected**, so tests can pass a fake engine, and new engine
types work without touching `Car`. That is composition: small parts, wired
together, each replaceable.

## When inheritance IS right

True taxonomies that must flow through all behavior: `windows.XyzError →
AppError → Exception` in your own exception hierarchies, framework base
classes, `enum.Enum`. Notice the pattern: the relationship is permanent and
everywhere-code depends on it. Data-record reuse ("Student and Teacher both
have names, so one inherits the other") is usually **not** that.

## Duck typing: the Python alternative to interfaces

Python doesn't ask "what is it?" but "what can it do?" Any object with a
`start()` works as an engine. Small protocols like this are why composition
is so cheap in Python — and they set up the next module's `Protocol` typing.
""",
    "Composition hơn Inheritance",
    "Dựng đối tượng từ các phần có thể hoán đổi — has-a thắng is-a trong phần lớn thiết kế thật.",
    """
Inheritance là công cụ bị lạm dụng nhất trong OOP. Trước khi viết `class
Admin(User)`, hãy hỏi: **Admin có thật sự là *một loại* User trong mọi hành
vi — mãi mãi không?** Thường điều bạn cần là *has-a*: đối tượng **sử dụng**
một bộ phận.

```python
class Engine:
    def start(self):
        return "vroom"

class Car:                      # Car HAS-An Engine — không kế thừa
    def __init__(self, engine):
        self.engine = engine    # tiêm từ bên ngoài

    def start(self):
        return self.engine.start()

Car(Engine()).start()           # "vroom"
Car(LoudEngine()).start()       # hoán đổi bộ phận thoải mái — duck typing
```

Engine được **tiêm vào**, nên test có thể thay bằng engine giả, và loại
engine mới hoạt động không cần sửa `Car`. Đó là composition: các phần nhỏ,
lắp với nhau, mỗi phần thay thế được.

## Khi nào inheritance ĐÚNG

Các phân loại thật mà mọi hành vi đều phải chảy qua: `AppError → Exception`
trong hệ thống exception của bạn, base class của framework, `enum.Enum`.
Hãy để ý mẫu chung: quan hệ là vĩnh viễn và mã ở khắp nơi phụ thuộc vào nó.
Việc tái dùng bản ghi ("Sinh viên và Giáo viên đều có tên nên một bên kế
thừa bên kia") thường **không phải** trường hợp đó.

## Duck typing: phương án của Python thay cho interface

Python không hỏi "nó là gì?" mà hỏi "nó làm được gì?" Bất kỳ đối tượng nào
có `start()` đều dùng được như engine. Các protocol nhỏ như vậy là lý do
composition rẻ đến thế trong Python — và nó dẫn thẳng tới `Protocol` trong
module typing kế tiếp.
""",
)

# --- module 2 practice sets ---
write_practice(
    M2, "m2-cls-practice",
    "Class Fundamentals",
    "Define types with state, methods, and clean reprs.",
    "Nền tảng Class",
    "Định nghĩa kiểu dữ liệu với trạng thái, method, và repr sạch sẽ.",
    L2A, 35, "intermediate",
    [
        challenge(
            "pi2-cls-counter", "Step Counter",
            "Create a class Counter with a method tick() that returns the number of ticks so far (1 on the first call). Use an instance attribute, not a global.",
            "class Counter:\n    def __init__(self):\n        pass\n\n    def tick(self):\n        pass\n",
            [
                ("ticks increment",
                 "c = Counter()\nassert [c.tick(), c.tick(), c.tick()] == [1, 2, 3]",
                 "Store the count in __init__ and increment in tick."),
                ("independent counters",
                 "a, b = Counter(), Counter()\na.tick(); a.tick()\nassert b.tick() == 1",
                 "Each instance owns its own state."),
            ],
            level="guided",
        ),
        challenge(
            "pi2-cls-book", "Book with Methods",
            "Create a class Book(title, pages) with a method reading_time(minutes_per_page=2) returning pages * minutes_per_page. Also give it a __repr__ like Book('Title', 100).",
            "class Book:\n    pass\n",
            [
                ("reading time default",
                 "b = Book('Dune', 400)\nassert b.reading_time() == 800",
                 "Default 2 minutes per page."),
                ("reading time custom",
                 "b = Book('Dune', 400)\nassert b.reading_time(3) == 1200",
                 "The parameter overrides the default."),
                ("repr shows fields",
                 "b = Book('Dune', 400)\nassert repr(b) == \"Book('Dune', 400)\"",
                 "Return an f-string with the two values; use !r for the title if you like."),
            ],
            level="independent",
        ),
        challenge(
            "pi2-cls-basket", "Basket Totals",
            "Create a class Basket that starts empty, add(item, price) appends items, and total() returns the sum of prices. add returns the new item count.",
            "class Basket:\n    pass\n",
            [
                ("empty basket totals zero",
                 "assert Basket().total() == 0",
                 "Initialize prices to an empty list in __init__."),
                ("add and total",
                 "b = Basket()\nassert b.add('tea', 3) == 1\nassert b.add('cup', 4) == 2\nassert b.total() == 7",
                 "add returns len of items after appending."),
            ],
            level="independent",
        ),
    ],
    {
        "pi2-cls-counter": vi_challenge("Bộ đếm bước", "Tạo class Counter với method tick() trả về số lần tick tính đến hiện tại (lần đầu là 1). Dùng instance attribute, không dùng biến global.", [("Tick tăng dần", "Lưu số đếm trong __init__ và tăng trong tick."), ("Các counter độc lập", "Mỗi thực thể giữ trạng thái riêng.")]),
        "pi2-cls-book": vi_challenge("Book với Method", "Tạo class Book(title, pages) với method reading_time(minutes_per_page=2) trả về pages * minutes_per_page. Thêm __repr__ dạng Book('Title', 100).", [("Thời gian đọc mặc định", "Mặc định 2 phút mỗi trang."), ("Thời gian đọc tùy chọn", "Tham số ghi đè mặc định."), ("repr hiện các trường", "Trả về f-string với hai giá trị; dùng !r cho title nếu muốn.")]),
        "pi2-cls-basket": vi_challenge("Giỏ hàng", "Tạo class Basket khởi tạo rỗng, add(item, price) thêm mặt hàng, total() trả về tổng giá. add trả về số mặt hàng mới hiện có.", [("Giỏ rỗng tổng bằng 0", "Khởi tạo danh sách giá rỗng trong __init__."), ("Thêm và tính tổng", "add trả về len sau khi thêm.")]),
    },
    solutions=[
        ("pi2-cls-counter", "class Counter:\n    def __init__(self):\n        self.count = 0\n\n    def tick(self):\n        self.count += 1\n        return self.count", "class Counter:\n    count = 0\n\n    def tick(self):\n        self.count += 1\n        return self.count"),
        ("pi2-cls-book", "class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n    def reading_time(self, minutes_per_page=2):\n        return self.pages * minutes_per_page\n\n    def __repr__(self):\n        return f'Book({self.title!r}, {self.pages})'", "class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n    def reading_time(self, minutes_per_page=2):\n        print(self.pages * minutes_per_page)\n        return None\n\n    def __repr__(self):\n        return self.title"),
        ("pi2-cls-basket", "class Basket:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, item, price):\n        self.prices.append(price)\n        return len(self.prices)\n\n    def total(self):\n        return sum(self.prices)", "class Basket:\n    def __init__(self):\n        self.prices = []\n\n    def add(self, item, price):\n        self.prices.append(price)\n        return price\n\n    def total(self):\n        return len(self.prices)"),
    ],
)

write_practice(
    M2, "m2-prop-practice",
    "Property Drills",
    "Make invalid states impossible with @property.",
    "Luyện Property",
    "Làm cho trạng thái sai trở nên bất khả thi với @property.",
    L2B, 25, "intermediate",
    [
        challenge(
            "pi2-prop-temp", "Validated Temperature",
            "Create a class Temperature with a celsius property. The setter must raise ValueError for values below -273.15 (absolute zero). Reading celsius returns the stored value.",
            "class Temperature:\n    def __init__(self, celsius):\n        pass\n",
            [
                ("accepts valid values",
                 "t = Temperature(25)\nassert t.celsius == 25\nt.celsius = -10\nassert t.celsius == -10",
                 "Store in _celsius via the property setter."),
                ("rejects below absolute zero",
                 "import unittest\ntry:\n    Temperature(-300)\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
                 "The setter must raise ValueError below -273.15."),
                ("rejects bad reassignment too",
                 "t = Temperature(0)\ntry:\n    t.celsius = -999\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
                 "Assignment goes through the same setter as __init__."),
            ],
            level="guided",
        ),
        challenge(
            "pi2-prop-readonly", "Read-Only Area",
            "Create a class Rect(w, h) with a read-only property area (no setter). Assigning to area must raise AttributeError.",
            "class Rect:\n    def __init__(self, w, h):\n        pass\n",
            [
                ("computes area",
                 "assert Rect(3, 4).area == 12",
                 "@property returning w * h."),
                ("assignment raises",
                 "r = Rect(2, 2)\ntry:\n    r.area = 10\n    failed = False\nexcept AttributeError:\n    failed = True\nassert failed",
                 "A property without a setter cannot be assigned."),
            ],
            level="independent",
        ),
    ],
    {
        "pi2-prop-temp": vi_challenge("Nhiệt độ có kiểm tra", "Tạo class Temperature với property celsius. Setter phải raise ValueError cho giá trị dưới -273.15 (không tuyệt đối). Đọc celsius trả về giá trị đã lưu.", [("Nhận giá trị hợp lệ", "Lưu vào _celsius qua property setter."), ("Từ chối dưới không tuyệt đối", "Setter phải raise ValueError dưới -273.15."), ("Gán sai sau đó cũng bị chặn", "Phép gán đi qua cùng setter như trong __init__.")]),
        "pi2-prop-readonly": vi_challenge("Diện tích chỉ đọc", "Tạo class Rect(w, h) với property chỉ đọc area (không setter). Gán cho area phải raise AttributeError.", [("Tính diện tích", "@property trả về w * h."), ("Gán sẽ raise", "Property không có setter thì không thể gán.")]),
    },
    solutions=[
        ("pi2-prop-temp", "class Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    @property\n    def celsius(self):\n        return self._celsius\n\n    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError('below absolute zero')\n        self._celsius = value", "class Temperature:\n    def __init__(self, celsius):\n        self._celsius = celsius\n\n    @property\n    def celsius(self):\n        return self._celsius"),
        ("pi2-prop-readonly", "class Rect:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    @property\n    def area(self):\n        return self.w * self.h", "class Rect:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    @property\n    def area(self):\n        return self.w * self.h\n\n    @area.setter\n    def area(self, value):\n        self.w = value // self.h"),
    ],
)

write_practice(
    M2, "m2-dc-practice",
    "Dataclass Drills",
    "Model records with @dataclass — defaults, frozen, and equality.",
    "Luyện Dataclass",
    "Mô hình hóa bản ghi bằng @dataclass — default, frozen, và so sánh bằng.",
    L2C, 25, "intermediate",
    [
        challenge(
            "pi2-dc-point", "Point Dataclass",
            "Define a dataclass Point with float fields x and y. Two points with the same coordinates must be equal, and repr(Point(1, 2)) must contain 'Point' and the values.",
            "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    pass\n",
            [
                ("equality by fields",
                 "assert Point(1.0, 2.0) == Point(1.0, 2.0)\nassert Point(1.0, 2.0) != Point(2.0, 1.0)",
                 "@dataclass generates field-wise __eq__ automatically."),
                ("repr is useful",
                 "r = repr(Point(1.0, 2.0))\nassert 'Point' in r and '1.0' in r",
                 "The generated __repr__ shows the class name and fields."),
            ],
            level="guided",
        ),
        challenge(
            "pi2-dc-config", "Frozen Config",
            "Define a frozen dataclass Config(host='localhost', port=8080). Verify: two defaults are equal, and attempting to set config.port raises an exception (dataclasses.FrozenInstanceError).",
            "from dataclasses import dataclass\n\n@dataclass\nclass Config:\n    pass\n",
            [
                ("defaults are equal",
                 "assert Config() == Config()\nassert Config(host='api.example.com').host == 'api.example.com'",
                 "Give host and port defaults in the class body."),
                ("frozen cannot be mutated",
                 "import dataclasses\nc = Config()\ntry:\n    c.port = 9999\n    failed = False\nexcept dataclasses.FrozenInstanceError:\n    failed = True\nassert failed",
                 "frozen=True makes assignment raise FrozenInstanceError."),
            ],
            level="independent",
        ),
        challenge(
            "pi2-dc-tasks", "Task Records",
            "Define a dataclass Task(title, done=False). Then implement finish(tasks) that returns a NEW list where every task is replaced by a copy with done=True. Use dataclasses.replace.",
            "from dataclasses import dataclass, replace\n\n@dataclass\nclass Task:\n    pass\n\ndef finish(tasks):\n    pass\n",
            [
                ("all tasks done in the new list",
                 "ts = [Task('a'), Task('b', True)]\nout = finish(ts)\nassert all(t.done for t in out)",
                 "replace(t, done=True) copies with the field changed."),
                ("original list untouched",
                 "ts = [Task('a')]\nfinish(ts)\nassert ts[0].done is False",
                 "Build a new list; do not mutate the input tasks."),
            ],
            level="combination",
        ),
    ],
    {
        "pi2-dc-point": vi_challenge("Point Dataclass", "Định nghĩa dataclass Point với hai trường float x và y. Hai điểm cùng tọa độ phải bằng nhau, và repr(Point(1, 2)) phải chứa 'Point' và các giá trị.", [("Bằng nhau theo trường", "@dataclass tự sinh __eq__ so từng trường."), ("repr hữu ích", "__repr__ tự sinh hiện tên class và các trường.")]),
        "pi2-dc-config": vi_challenge("Config bất biến", "Định nghĩa frozen dataclass Config(host='localhost', port=8080). Kiểm chứng: hai giá trị mặc định bằng nhau, và cố gắng gán config.port raise exception (dataclasses.FrozenInstanceError).", [("Mặc định bằng nhau", "Cho host và port giá trị mặc định trong thân class."), ("Frozen không thể sửa", "frozen=True khiến phép gán raise FrozenInstanceError.")]),
        "pi2-dc-tasks": vi_challenge("Bản ghi Task", "Định nghĩa dataclass Task(title, done=False). Sau đó viết finish(tasks) trả về list MỚI trong đó mọi task được thay bằng bản sao với done=True. Dùng dataclasses.replace.", [("List mới tất cả done", "replace(t, done=True) sao chép với trường đã đổi."), ("List gốc không đổi", "Dựng list mới; không sửa các task trong input.")]),
    },
    solutions=[
        ("pi2-dc-point", "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: float\n    y: float", "from dataclasses import dataclass\n\nclass Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y"),
        ("pi2-dc-config", "from dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Config:\n    host: str = 'localhost'\n    port: int = 8080", "from dataclasses import dataclass\n\n@dataclass\nclass Config:\n    host: str = 'localhost'\n    port: int = 8080"),
        ("pi2-dc-tasks", "from dataclasses import dataclass, replace\n\n@dataclass\nclass Task:\n    title: str\n    done: bool = False\n\ndef finish(tasks):\n    return [replace(t, done=True) for t in tasks]", "from dataclasses import dataclass, replace\n\n@dataclass\nclass Task:\n    title: str\n    done: bool = False\n\ndef finish(tasks):\n    for t in tasks:\n        t.done = True\n    return tasks"),
    ],
)

write_practice(
    M2, "m2-comp-practice",
    "Composition Drills",
    "Build objects from injected parts.",
    "Luyện Composition",
    "Dựng đối tượng từ các bộ phận được tiêm vào.",
    L2D, 25, "intermediate",
    [
        challenge(
            "pi2-comp-car", "Car Has-An Engine",
            "Given the Engine class, create Car(engine) that stores the engine and delegates start() to it. Do NOT inherit — compose.",
            "class Engine:\n    def start(self):\n        return 'vroom'\n\nclass Car:\n    pass\n",
            [
                ("delegates to its engine",
                 "assert Car(Engine()).start() == 'vroom'",
                 "Car.start calls self.engine.start()."),
                ("works with any engine",
                 "class Loud:\n    def start(self):\n        return 'ROAR'\nassert Car(Loud()).start() == 'ROAR'",
                 "Duck typing: whatever has start() works."),
            ],
            level="guided",
        ),
        challenge(
            "pi2-comp-reporter", "Reporter Injection",
            "Create a class Order totals calculator: Order(items) where items is a list of prices. Its total() returns the sum. Add a constructor parameter reporter=None; if provided, total() must call reporter(total_value) once. This is dependency injection for observability.",
            "class Order:\n    def __init__(self, items, reporter=None):\n        pass\n",
            [
                ("totals without a reporter",
                 "assert Order([10, 20]).total() == 30",
                 "reporter defaults to None; total works without it."),
                ("calls the reporter once with the total",
                 "calls = []\nOrder([10, 20], reporter=calls.append).total()\nassert calls == [30]",
                 "A list's append is a function — pass it as the reporter."),
            ],
            level="independent",
        ),
    ],
    {
        "pi2-comp-car": vi_challenge("Car Has-An Engine", "Cho class Engine, tạo Car(engine) lưu engine và ủy quyền start() cho nó. KHÔNG kế thừa — hãy compose.", [("Ủy quyền cho engine", "Car.start gọi self.engine.start()."), ("Hợp với mọi engine", "Duck typing: cái gì có start() đều dùng được.")]),
        "pi2-comp-reporter": vi_challenge("Tiêm Reporter", "Tạo class tính tổng Order: Order(items) với items là list giá. total() trả về tổng. Thêm tham số khởi tạo reporter=None; nếu được cung cấp, total() phải gọi reporter(tong) đúng một lần. Đây là dependency injection cho observability.", [("Tổng không cần reporter", "reporter mặc định None; total vẫn chạy không có nó."), ("Gọi reporter đúng một lần với tổng", "append của một list là một hàm — truyền nó làm reporter.")]),
    },
    solutions=[
        ("pi2-comp-car", "class Engine:\n    def start(self):\n        return 'vroom'\n\nclass Car:\n    def __init__(self, engine):\n        self.engine = engine\n\n    def start(self):\n        return self.engine.start()", "class Engine:\n    def start(self):\n        return 'vroom'\n\nclass Car(Engine):\n    pass"),
        ("pi2-comp-reporter", "class Order:\n    def __init__(self, items, reporter=None):\n        self.items = items\n        self.reporter = reporter\n\n    def total(self):\n        total = sum(self.items)\n        if self.reporter is not None:\n            self.reporter(total)\n        return total", "class Order:\n    def __init__(self, items, reporter=None):\n        self.items = items\n        self.reporter = reporter\n\n    def total(self):\n        total = sum(self.items)\n        if self.reporter is not None:\n            self.reporter('total=' + str(total))\n        return total"),
    ],
)

# --- module 2 checkpoint ---
write_checkpoint(
    M2, L2E,
    "Checkpoint: Domain Modeling",
    "Design a small domain model combining classes, properties, and composition.",
    20,
    """
Model a slice of a real shop: an `Order` that holds `OrderLine` records.
You will combine class design, validation, composition, and a clean repr —
the daily modeling work of every backend.

**Working with AI:** before writing code, try asking a mentor to critique
your *design* (fields? invariants? what should raise?) — design review is a
higher-value AI use than code generation.
""",
    "Checkpoint: Mô hình hóa miền dữ liệu",
    "Thiết kế một mô hình miền nhỏ kết hợp class, property, và composition.",
    """
Mô hình hóa một phần của cửa hàng thật: một `Order` giữ các bản ghi
`OrderLine`. Bạn sẽ kết hợp thiết kế class, kiểm tra dữ liệu, composition,
và repr sạch sẽ — công việc mô hình hóa hàng ngày của mọi backend.

**Làm việc cùng AI:** trước khi viết code, hãy nhờ mentor phê bình *thiết kế*
của bạn (các trường? bất biến? cái gì nên raise?) — review thiết kế là cách
dùng AI giá trị hơn việc sinh code.
""",
    challenge(
        "pi2-ckpt-order", "Order with OrderLines",
        "Define a dataclass OrderLine(sku, quantity, unit_price) and a class Order that starts empty. add_line(sku, quantity, unit_price) appends an OrderLine and returns the line count (raise ValueError if quantity <= 0). total() sums quantity * unit_price. repr(Order()) must contain 'Order'.",
        "from dataclasses import dataclass\n\n@dataclass\nclass OrderLine:\n    pass\n\nclass Order:\n    pass\n",
        [
            ("orderline equality and fields",
             "assert OrderLine('tea', 2, 3) == OrderLine('tea', 2, 3)",
             "A dataclass gives field equality for free."),
            ("add returns count; total computes",
             "o = Order()\nassert o.add_line('tea', 2, 3) == 1\nassert o.add_line('cup', 1, 10) == 2\nassert o.total() == 16",
             "2*3 + 1*10 = 16."),
            ("invalid quantity raises",
             "o = Order()\ntry:\n    o.add_line('x', 0, 5)\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
             "Validate quantity at the boundary: raise ValueError when <= 0."),
            ("repr mentions Order",
             "assert 'Order' in repr(Order())",
             "Define __repr__ or reuse a readable default."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Order với OrderLines",
        "Định nghĩa dataclass OrderLine(sku, quantity, unit_price) và class Order khởi tạo rỗng. add_line(sku, quantity, unit_price) thêm một OrderLine và trả về số dòng (raise ValueError nếu quantity <= 0). total() cộng quantity * unit_price. repr(Order()) phải chứa 'Order'.",
        [
            ("OrderLine bằng nhau theo trường", "Dataclass cho phép so bằng theo trường miễn phí."),
            ("add trả số dòng; total tính đúng", "2*3 + 1*10 = 16."),
            ("quantity sai sẽ raise", "Kiểm tra quantity tại ranh giới: raise ValueError khi <= 0."),
            ("repr nhắc đến Order", "Tự định nghĩa __repr__ hoặc dùng mặc định dễ đọc."),
        ],
    ),
    solution="from dataclasses import dataclass\n\n@dataclass\nclass OrderLine:\n    sku: str\n    quantity: int\n    unit_price: float\n\nclass Order:\n    def __init__(self):\n        self.lines = []\n\n    def add_line(self, sku, quantity, unit_price):\n        if quantity <= 0:\n            raise ValueError('quantity must be positive')\n        self.lines.append(OrderLine(sku, quantity, unit_price))\n        return len(self.lines)\n\n    def total(self):\n        return sum(l.quantity * l.unit_price for l in self.lines)\n\n    def __repr__(self):\n        return f'Order({len(self.lines)} lines)'",
    wrong="from dataclasses import dataclass\n\n@dataclass\nclass OrderLine:\n    sku: str\n    quantity: int\n    unit_price: float\n\nclass Order:\n    def __init__(self):\n        self.lines = []\n\n    def add_line(self, sku, quantity, unit_price):\n        self.lines.append(OrderLine(sku, quantity, unit_price))\n        return len(self.lines)\n\n    def total(self):\n        return sum(l.quantity * l.unit_price for l in self.lines)",
)

print("modules 1-2 done")
