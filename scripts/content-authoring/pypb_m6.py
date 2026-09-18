#!/usr/bin/env python3
"""Module 6: loops — lessons + practices + checkpoint. Direct triple-quote MDX."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "loops"

L1 = """
Loops repeat work — the difference between typing 100 print statements and one.

## for: walk a collection

```python
fruits = ["apple", "pear", "plum"]
for fruit in fruits:
    print(f"today: {fruit}")
```

Read it as a sentence: "**for each** fruit **in** fruits, do the indented
block". The loop variable (`fruit`) takes each value in turn. Note: `fruit`
sensibly singular vs `fruits` plural — name loop variables like you mean it.

## Strings are walkable too

```python
for ch in "abc":
    print(ch)      # a, b, c
```

## Indentation again

The indented block runs once per item. Dedent to run *after* the loop:

```python
for fruit in fruits:
    print(fruit)
print("done")      # runs once, after all fruit
```
"""

L1_VI = """
Vòng lặp lặp lại công việc — đó là khác biệt giữa gõ 100 câu print và một câu.

## for: đi qua một collection

```python
fruits = ["apple", "pear", "plum"]
for fruit in fruits:
    print(f"today: {fruit}")
```

Đọc như một câu: "**for mỗi** fruit **in** fruits, làm khối lệnh thụt vào".
Biến lặp (`fruit`) lần lượt nhận từng giá trị. Chú ý: `fruit` số ít hợp lý so
với `fruits` số nhiều — hãy đặt tên biến lặp cho có ý nghĩa.

## Chuỗi cũng đi qua được

```python
for ch in "abc":
    print(ch)      # a, b, c
```

## Thụt lề lần nữa

Khối thụt vào chạy một lần cho mỗi phần tử. Thụt ra để chạy *sau* vòng lặp:

```python
for fruit in fruits:
    print(fruit)
print("done")      # chạy một lần, sau tất cả fruit
```
"""

L2 = """
`range()` produces a sequence of numbers — how you count in Python:

```python
range(5)         # 0, 1, 2, 3, 4        (stop excluded!)
range(1, 6)      # 1, 2, 3, 4, 5        (start, stop)
range(0, 10, 2)  # 0, 2, 4, 6, 8        (start, stop, step)
range(10, 0, -1) # 10, 9, ..., 1        (counting down)
```

`range(stop)` never includes `stop` — the half-open rule again, same as
slicing. Combine with `list()` to see it: `list(range(4))` → `[0, 1, 2, 3]`.

## enumerate: value AND position

```python
for i, fruit in enumerate(fruits):
    print(i, fruit)     # 0 apple, 1 pear, 2 plum
```

## zip: walk two lists together

```python
names = ["a", "b"]
scores = [9, 7]
for name, score in zip(names, scores):
    print(name, score)
```

## while: loop while a condition holds

```python
count = 3
while count > 0:
    print(count)
    count -= 1
print("liftoff")
```

`while` re-checks the condition each round. **If nothing inside makes the
condition false, the loop never ends** — the infinite loop, the classic
beginner trap. When a loop must end, something in the body must move toward
the exit (decrement a counter, change a flag...).
"""

L2_VI = """
`range()` tạo ra một dãy số — cách bạn đếm trong Python:

```python
range(5)         # 0, 1, 2, 3, 4        (stop bị loại trừ!)
range(1, 6)      # 1, 2, 3, 4, 5        (start, stop)
range(0, 10, 2)  # 0, 2, 4, 6, 8        (start, stop, step)
range(10, 0, -1) # 10, 9, ..., 1        (đếm ngược)
```

`range(stop)` không bao giờ chứa `stop` — quy tắc nửa mở lần nữa, giống slicing.
Kết hợp với `list()` để nhìn thấy nó: `list(range(4))` → `[0, 1, 2, 3]`.

## enumerate: giá trị VÀ vị trí

```python
for i, fruit in enumerate(fruits):
    print(i, fruit)     # 0 apple, 1 pear, 2 plum
```

## zip: đi hai list cùng nhau

```python
names = ["a", "b"]
scores = [9, 7]
for name, score in zip(names, scores):
    print(name, score)
```

## while: lặp khi điều kiện còn đúng

```python
count = 3
while count > 0:
    print(count)
    count -= 1
print("liftoff")
```

`while` kiểm tra lại điều kiện mỗi vòng. **Nếu không có gì trong thân vòng lặp
khiến điều kiện sai, vòng lặp không bao giờ kết thúc** — vòng lặp vô hạn, cái
bẫy kinh điển của người mới. Khi một vòng lặp phải kết thúc, phải có thứ gì đó
trong thân tiến về lối ra (giảm bộ đếm, đổi cờ...).
"""

L3 = """
## break: leave early

```python
for n in [3, 7, 0, 9]:
    if n == 0:
        break            # stop the whole loop now
    print(n)             # 3, 7
```

## continue: skip this round

```python
for n in range(6):
    if n % 2 == 0:
        continue         # jump to the next round
    print(n)             # 1, 3, 5
```

## Accumulator patterns — the bread and butter

Most real loops update a running result:

```python
total = 0
for price in [5, 8, 12]:
    total += price          # summing
print(total)                # 25

hits = 0
for n in [1, 7, 4, 9]:
    if n > 5:
        hits += 1           # counting matches
print(hits)                 # 2

biggest = None
for n in [1, 7, 4]:
    if biggest is None or n > biggest:
        biggest = n          # tracking a maximum
print(biggest)               # 7
```

Three shapes to memorize through practice: **sum**, **count**, **best-so-far**.
Every data report you will ever write is built from these.
"""

L3_VI = """
## break: rời đi sớm

```python
for n in [3, 7, 0, 9]:
    if n == 0:
        break            # dừng toàn bộ vòng lặp ngay bây giờ
    print(n)             # 3, 7
```

## continue: bỏ qua vòng này

```python
for n in range(6):
    if n % 2 == 0:
        continue         # nhảy sang vòng kế tiếp
    print(n)             # 1, 3, 5
```

## Các mẫu tích lũy — xương sống của lập trình

Hầu hết vòng lặp thật cập nhật một kết quả đang chạy:

```python
total = 0
for price in [5, 8, 12]:
    total += price          # cộng dồn
print(total)                # 25

hits = 0
for n in [1, 7, 4, 9]:
    if n > 5:
        hits += 1           # đếm số khớp
print(hits)                 # 2

biggest = None
for n in [1, 7, 4]:
    if biggest is None or n > biggest:
        biggest = n          # theo dõi giá trị lớn nhất
print(biggest)               # 7
```

Ba mẫu hình cần nhớ qua thực hành: **tổng**, **đếm**, **kỷ lục tạm thời**.
Mọi báo cáo dữ liệu bạn sẽ viết đều được xây từ ba mẫu này.
"""

write_lesson(MOD, "for-loops", "for Loops",
             "Walk collections with for — and the rules of the loop block.", 10,
             L1, "Vòng lặp for", "Đi qua collection với for — và quy tắc của khối lặp.", L1_VI)

write_lesson(MOD, "range-while", "range() & while",
             "Counting with range, enumerate, zip — and while with its infinite-loop trap.", 12,
             L2, "range() & while", "Đếm với range, enumerate, zip — và while với cái bẫy lặp vô hạn.", L2_VI)

write_lesson(MOD, "break-continue-accumulators", "break, continue & Accumulators",
             "Leaving early, skipping rounds, and the sum/count/best patterns.", 12,
             L3, "break, continue & Tích lũy", "Rời sớm, bỏ qua vòng, và các mẫu tổng/đếm/kỷ lục.", L3_VI)

# ── Practices ───────────────────────────────────────────────────────────────
write_practice(
    MOD, "m6-for-practice",
    "for-Loop Drills",
    "Walk collections and produce output per item.",
    "Bài tập vòng lặp for",
    "Đi qua collection và tạo đầu ra cho từng phần tử.",
    "for-loops", 30, "beginner",
    [
        challenge(
            "py-loop-print-items",
            "Numbered Shopping List",
            'items = ["milk", "bread", "eggs"] is given. Print each on its own line as 1. milk / 2. bread / 3. eggs — use enumerate so numbering is automatic.',
            'items = ["milk", "bread", "eggs"]\n',
            [("numbered output", 'assert printed == ["1. milk", "2. bread", "3. eggs"], f"got {printed}"\nassert "enumerate(" in code, "use enumerate() for numbering"',
              "for i, item in enumerate(items, start=1): print(f\"{i}. {item}\")")],
            level="guided",
        ),
        challenge(
            "py-loop-chars",
            "Vertical Word",
            'word = "hi!" is given. Print each character on its own line.',
            'word = "hi!"\n',
            [("one char per line", 'assert printed == ["h", "i", "!"], f"got {printed}"',
              "Strings are walkable: for ch in word:")],
            level="imitation",
        ),
        challenge(
            "py-loop-times-table",
            "Times Table Row",
            "n = 7 is given. Print the 7-times table from 1x to 3x as three lines: 7 / 14 / 21 — with range().",
            "n = 7\n",
            [("three multiples", 'assert printed == ["7", "14", "21"], f"got {printed}"\nassert "range(" in code, "use range()"',
              "for i in range(1, 4): print(n * i)")],
            level="guided",
        ),
    ],
    {
        "py-loop-print-items": vi_challenge("Danh sách mua có số", 'items = ["milk", "bread", "eggs"] đã cho. In từng mục một dòng: 1. milk / 2. bread / 3. eggs — dùng enumerate để đánh số tự động.',
                                               [("đầu ra có số", "for i, item in enumerate(items, start=1): print(f\"{i}. {item}\")")]),
        "py-loop-chars": vi_challenge("Từ dọc", 'word = "hi!" đã cho. In từng ký tự một dòng.',
                                        [("một ký tự mỗi dòng", "Chuỗi đi qua được: for ch in word:")]),
        "py-loop-times-table": vi_challenge("Dòng bảng cửu chương", "n = 7 đã cho. In bảng nhân 7 từ 1x đến 3x thành ba dòng: 7 / 14 / 21 — với range().",
                                              [("ba bội số", "for i in range(1, 4): print(n * i)")]),
    },
    solutions=[
        ("py-loop-print-items", 'items = ["milk", "bread", "eggs"]\nfor i, item in enumerate(items, start=1):\n    print(f"{i}. {item}")',
         'items = ["milk", "bread", "eggs"]\nfor item in items:\n    print(item)'),
        ("py-loop-chars", 'word = "hi!"\nfor ch in word:\n    print(ch)',
         'word = "hi!"\nprint(word)'),
        ("py-loop-times-table", "n = 7\nfor i in range(1, 4):\n    print(n * i)",
         "n = 7\nfor i in range(4):\n    print(n * i)"),
    ],
)

write_practice(
    MOD, "m6-accumulator-practice",
    "Accumulator Drills",
    "Sum, count, and best-so-far — the three core patterns.",
    "Bài tập tích lũy",
    "Tổng, đếm, và kỷ lục — ba mẫu hình cốt lõi.",
    "break-continue-accumulators", 35, "beginner",
    [
        challenge(
            "py-acc-sum",
            "Running Total",
            "prices is given. Print the total of all prices.",
            "prices = [5, 8, 12]\n",
            [("prints 25", 'assert printed == ["25"], f"got {printed}"\nassert "for " in code, "use a loop — sum() is next module\'s tool"',
              "Start total at 0 and add each price inside the loop.")],
            level="guided",
        ),
        challenge(
            "py-acc-count",
            "Count the Passes",
            "scores is given. Print how many scores are 50 or higher.",
            "scores = [40, 55, 80, 49, 50]\n",
            [("prints 3", 'assert printed == ["3"], f"got {printed}"',
              "Count inside an if score >= 50 branch. Note 50 counts!")],
            level="guided",
        ),
        challenge(
            "py-acc-best",
            "Best So Far",
            "times (race results) is given. Print the fastest (smallest) time using a best-so-far loop — no min().",
            "times = [12.5, 9.8, 11.2, 9.9]\n",
            [("prints 9.8", 'assert printed == ["9.8"], f"got {printed}"\nassert "min(" not in code, "track the best with an if, no min()"',
              "best = None; if best is None or t < best: best = t")],
            level="independent",
        ),
        challenge(
            "py-acc-skip",
            "Skip the Zeros",
            "readings is given. Print the sum of non-zero readings only — continue earns its keep here.",
            "readings = [4, 0, 6, 0, 1]\n",
            [("prints 11", 'assert printed == ["11"], f"got {printed}"\nassert "continue" in code, "use continue to skip zeros"',
              "if r == 0: continue, then add r.")],
            level="guided",
        ),
    ],
    {
        "py-acc-sum": vi_challenge("Tổng chạy dần", "prices đã cho. In tổng tất cả giá tiền.",
                                     [("in 25", "Khởi tạo total bằng 0 và cộng từng giá tiền trong vòng lặp.")]),
        "py-acc-count": vi_challenge("Đếm số đạt", "scores đã cho. In bao nhiêu điểm từ 50 trở lên.",
                                       [("in 3", "Đếm trong nhánh if score >= 50. Chú ý 50 cũng được tính!")]),
        "py-acc-best": vi_challenge("Kỷ lục tạm thời", "times (kết quả chạy đua) đã cho. In thời gian nhanh nhất (nhỏ nhất) bằng vòng lặp kỷ lục — không dùng min().",
                                      [("in 9.8", "best = None; if best is None or t < best: best = t")]),
        "py-acc-skip": vi_challenge("Bỏ qua số 0", "readings đã cho. Chỉ in tổng các số đọc khác 0 — continue phát huy tác dụng ở đây.",
                                      [("in 11", "if r == 0: continue, rồi cộng r.")]),
    },
    solutions=[
        ("py-acc-sum", "prices = [5, 8, 12]\ntotal = 0\nfor p in prices:\n    total += p\nprint(total)",
         "prices = [5, 8, 12]\nprint(prices)"),
        ("py-acc-count", "scores = [40, 55, 80, 49, 50]\npasses = 0\nfor s in scores:\n    if s >= 50:\n        passes += 1\nprint(passes)",
         "scores = [40, 55, 80, 49, 50]\npasses = 0\nfor s in scores:\n    if s > 50:\n        passes += 1\nprint(passes)"),
        ("py-acc-best", "times = [12.5, 9.8, 11.2, 9.9]\nbest = None\nfor t in times:\n    if best is None or t < best:\n        best = t\nprint(best)",
         "times = [12.5, 9.8, 11.2, 9.9]\nbest = None\nfor t in times:\n    if best is None or t > best:\n        best = t\nprint(best)"),
        ("py-acc-skip", "readings = [4, 0, 6, 0, 1]\ntotal = 0\nfor r in readings:\n    if r == 0:\n        continue\n    total += r\nprint(total)",
         "readings = [4, 0, 6, 0, 1]\ntotal = 0\nfor r in readings:\n    if r == 0:\n        break\n    total += r\nprint(total)"),
    ],
)

write_practice(
    MOD, "m6-while-practice",
    "while & Game Logic",
    "Mini build: the classic number guessing game — loop until found.",
    "while & Logic trò chơi",
    "Mini build: trò chơi đoán số kinh điển — lặp đến khi trúng.",
    "range-while", 35, "beginner",
    [
        challenge(
            "py-while-countdown",
            "Countdown",
            "start = 3 is given. Print a countdown: 3, 2, 1, then liftoff — a while loop with a decrement.",
            "start = 3\n",
            [("countdown then liftoff", 'assert printed == ["3", "2", "1", "liftoff"], f"got {printed}"\nassert "while" in code, "use a while loop"',
              "while start > 0: print(start); start -= 1 — then print liftoff after the loop.")],
            level="guided",
        ),
        challenge(
            "py-while-halve",
            "Halving Loop",
            "n = 40 is given. Print n after each halving (40, 20, 10, 5, 2) while it is at least 2 — using integer division and a while loop.",
            "n = 40\n",
            [("halving sequence", 'assert printed == ["40", "20", "10", "5", "2"], f"got {printed}"\nassert "while" in code, "use a while loop"',
              "while n >= 2: print(n); n //= 2 — //= is augmented floor division.")],
            level="guided",
        ),
        challenge(
            "py-while-guess-steps",
            "Guessing Steps (deterministic)",
            "secret = 7 is given, and guesses = [4, 9, 7] simulates the player. Walk the guesses in order with a for loop and print each guess, stopping (break) the moment the secret is found. The winning guess must be printed too.",
            "secret = 7\nguesses = [4, 9, 7]\n",
            [("walks and stops at the hit", 'assert printed == ["4", "9", "7"], f"got {printed}"\nassert "break" in code, "break once the secret is found"',
              "for g in guesses: print(g); if g == secret: break — print before checking.")],
            level="mini-build",
        ),
    ],
    {
        "py-while-countdown": vi_challenge("Đếm ngược", "start = 3 đã cho. In đếm ngược: 3, 2, 1, rồi liftoff — vòng lặp while với phép giảm.",
                                             [("đếm ngược rồi liftoff", "while start > 0: print(start); start -= 1 — rồi in liftoff sau vòng lặp.")]),
        "py-while-halve": vi_challenge("Vòng lặp chia đôi", "n = 40 đã cho. In n sau mỗi lần chia đôi (40, 20, 10, 5, 2) trong khi nó còn ≥ 2 — dùng chia lấy nguyên và vòng lặp while.",
                                         [("dãy chia đôi", "while n >= 2: print(n); n //= 2 — //= là chia lấy nguyên dạng gán mở rộng.")]),
        "py-while-guess-steps": vi_challenge("Các bước đoán (xác định)", "secret = 7 đã cho, và guesses = [4, 9, 7] mô phỏng người chơi. Đi qua các đoán theo thứ tự bằng vòng lặp for và in từng đoán, dừng lại (break) ngay khi tìm ra bí mật. Đoán trúng cũng phải được in.",
                                               [("đi qua và dừng khi trúng", "for g in guesses: print(g); if g == secret: break — in trước khi kiểm tra.")]),
    },
    solutions=[
        ("py-while-countdown", "start = 3\nwhile start > 0:\n    print(start)\n    start -= 1\nprint(\"liftoff\")",
         "start = 3\nwhile start > 0:\n    print(start)\n    start += 1\nprint(\"liftoff\")"),
        ("py-while-halve", "n = 40\nwhile n >= 2:\n    print(n)\n    n //= 2",
         "n = 40\nwhile n > 2:\n    print(n)\n    n //= 2"),
        ("py-while-guess-steps", "secret = 7\nguesses = [4, 9, 7]\nfor g in guesses:\n    print(g)\n    if g == secret:\n        break",
         "secret = 7\nguesses = [4, 9, 7]\nfor g in guesses:\n    if g == secret:\n        break\n    print(g)"),
    ],
)

# ── Checkpoint: collections + control flow ──────────────────────────────────
CP = """
## Checkpoint: Collections + Control Flow

Modules 5–6 in one program: walk a nested structure, accumulate a result, and
branch on what you find. This is the shape of a real data report — and the
exact skill the file-processing modules will ask you to apply.
"""

CP_VI = """
## Checkpoint: Collection + Luồng điều khiển

Module 5–6 trong một chương trình: đi qua cấu trúc lồng nhau, tích lũy kết quả,
và rẽ nhánh theo những gì bạn tìm thấy. Đây là hình dạng của một báo cáo dữ liệu
thật — và kỹ năng chính xác mà các module xử lý tệp sẽ yêu cầu bạn vận dụng.
"""

write_checkpoint(
    MOD, "checkpoint-collections-control",
    "Checkpoint: Collections + Control Flow",
    "Nested data, loops, and decisions combined into one report program.",
    20, CP,
    "Checkpoint: Collection + Luồng điều khiển",
    "Dữ liệu lồng nhau, vòng lặp, và quyết định kết hợp thành một chương trình báo cáo.",
    CP_VI,
    challenge(
        "py-checkpoint-collections",
        "Department Report",
        'departments = {"sales": [120, 80, 150], "it": [200, 180]} is given (spending per month). Print each department and its total as sales: 350 / it: 380 — two lines. Then print the name of the department with the higher total: top: it',
        'departments = {"sales": [120, 80, 150], "it": [200, 180]}\n',
        [
            ("prints per-department totals",
             'assert printed[0] == "sales: 350" and printed[1] == "it: 380", f"got {printed}"',
             "Loop over departments.items(); sum(d) each."),
            ("prints the top department",
             'assert printed[2] == "top: it", f"got {printed}"',
             "Track best-so-far across departments while summing."),
        ],
        difficulty="beginner",
    ),
    vi_challenge("Báo cáo phòng ban", 'departments = {"sales": [120, 80, 150], "it": [200, 180]} đã cho (chi tiêu theo tháng). In từng phòng ban và tổng của nó: sales: 350 / it: 380 — hai dòng. Sau đó in tên phòng có tổng cao hơn: top: it',
                 [("in tổng từng phòng", "Duyệt departments.items(); sum(d) từng cái."),
                  ("in phòng dẫn đầu", "Theo dõi kỷ lục tạm thời qua các phòng trong khi cộng dồn.")]),
    solution='departments = {"sales": [120, 80, 150], "it": [200, 180]}\nbest_name = None\nbest_total = None\nfor name, spends in departments.items():\n    total = sum(spends)\n    print(f"{name}: {total}")\n    if best_total is None or total > best_total:\n        best_name = name\n        best_total = total\nprint(f"top: {best_name}")',
    wrong='departments = {"sales": [120, 80, 150], "it": [200, 180]}\nbest_name = None\nbest_total = None\nfor name, spends in departments.items():\n    total = sum(spends)\n    print(f"{name}: {total}")\n    if best_total is None or total > best_total:\n        best_name = name\n        best_total = total\nprint(f"top: {best_total}")',
)

print("module 6 content written")
