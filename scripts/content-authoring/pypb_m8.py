#!/usr/bin/env python3
"""Module 8: errors-and-debugging — lessons + practices + Bug Hunt + checkpoint.

Project-style set: Bug Hunt gives learners four intentionally broken programs.
Each is a debugging challenge (reproduce -> diagnose -> fix). The graders check
BEHAVIOR after the fix, and the wrong solutions keep the original bug.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "errors-and-debugging"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
Not all bugs are equal. Python tells you which kind you have — learning to read
that message is the skill.

## The three error families

**Syntax errors** — Python cannot even start. It points at the line it chokes on:

```python
if x > 5
    print("big")
# SyntaxError: expected ':'
```

**Runtime errors (exceptions)** — the program starts, then crashes mid-run:

```python
ages = {"minh": 21}
print(ages["linh"])
# KeyError: 'linh'
```

**Logic errors** — the program runs to completion and gives the WRONG answer. No
error message appears. These are the most dangerous, and the reason testing
exists:

```python
average = a + b / 2   # runs fine — and is wrong
```

## The traceback: read it bottom-up

```
Traceback (most recent call last):
  File "report.py", line 4, in <module>
    total = sum(values) / count
ZeroDivisionError: division by zero
```

Read the LAST line first: the error type and message. Then the line above: where
it happened. Then follow the call chain upward to find what led there.
"""

L1_VI = """
Không phải lỗi nào cũng giống nhau. Python cho bạn biết bạn gặp loại nào — học
cách đọc thông điệp đó chính là kỹ năng.

## Ba họ lỗi

**Lỗi cú pháp (syntax)** — Python thậm chí không chạy nổi. Nó chỉ vào dòng bị vấp:

```python
if x > 5
    print("big")
# SyntaxError: expected ':'
```

**Lỗi runtime (ngoại lệ)** — chương trình chạy, rồi sập giữa đường:

```python
ages = {"minh": 21}
print(ages["linh"])
# KeyError: 'linh'
```

**Lỗi logic** — chương trình chạy trọn vẹn và đưa ra câu trả lời SAI. Không có
thông báo lỗi nào xuất hiện. Đây là loại nguy hiểm nhất, và là lý do kiểm thử
tồn tại:

```python
average = a + b / 2   # chạy êm ru — và sai
```

## Traceback: đọc từ dưới lên

```
Traceback (most recent call last):
  File "report.py", line 4, in <module>
    total = sum(values) / count
ZeroDivisionError: division by zero
```

Đọc DÒNG CUỐI trước: loại lỗi và thông điệp. Rồi dòng ngay trên: nơi nó xảy ra.
Sau đó lần theo chuỗi lời gọi ngược lên để tìm điều gì dẫn đến đó.
"""

L2 = """
```python
try:
    number = int("twelve")
except ValueError:
    print("That is not a number")
```

`try` means: run this; it may explode. `except` catches the specific explosion
you are prepared for. Catch the **narrowest** exception you can handle — a bare
`except:` swallows bugs you did not anticipate, including typos.

## The exceptions you will meet weekly

- `ValueError` — right type, impossible value (`int("abc")`)
- `TypeError` — wrong kind of object entirely (`"5" + 5`)
- `KeyError` / `IndexError` — missing dict key / list position
- `ZeroDivisionError` — you know this one already

## else and finally

```python
try:
    data = load(path)
except FileNotFoundError:
    print("missing file — using defaults")
    data = []
else:
    print("loaded", len(data), "rows")   # runs only if NO exception
finally:
    close_resources()                    # runs ALWAYS — cleanup
```

`else` keeps success-path code out of the try block; `finally` is for cleanup
that must happen either way.
"""

L2_VI = """
```python
try:
    number = int("twelve")
except ValueError:
    print("Cái này không phải số")
```

`try` nghĩa là: chạy thử; nó có thể nổ. `except` bắt đúng cú nổ mà bạn đã chuẩn
bị. Hãy bắt **ngoại lệ hẹp nhất** mà bạn xử lý được — một `except:` trần nuốt luôn
những lỗi bạn không lường trước, kể cả lỗi gõ nhầm.

## Những ngoại lệ bạn gặp hàng tuần

- `ValueError` — đúng kiểu, giá trị bất khả thi (`int("abc")`)
- `TypeError` — sai hẳn loại đối tượng (`"5" + 5`)
- `KeyError` / `IndexError` — thiếu khóa dict / vị trí list
- `ZeroDivisionError` — cái này bạn biết rồi

## else và finally

```python
try:
    data = load(path)
except FileNotFoundError:
    print("thiếu tệp — dùng dữ liệu mặc định")
    data = []
else:
    print("đã nạp", len(data), "dòng")   # chỉ chạy khi KHÔNG có ngoại lệ
finally:
    close_resources()                    # LUÔN chạy — dọn dẹp
```

`else` giữ mã thành công nằm ngoài khối try; `finally` dành cho việc dọn dẹp
bắt buộc phải diễn ra dù thành công hay thất bại.
"""

L3 = """
`raise` throws an exception deliberately — when the data is wrong, fail loudly:

```python
def set_price(price):
    if price < 0:
        raise ValueError(f"price cannot be negative, got {price}")
    return price
```

A function that fails fast with a clear message is kinder than one that returns
nonsense and lets the bug surface three layers away. Raising early converts a
silent logic error into a loud, debuggable runtime error.

## Defensive checks in practice

```python
def average(values):
    if not values:                 # None, [], empty — all falsy
        raise ValueError("average of empty data is undefined")
    return sum(values) / len(values)
```

The check is one line; the debugging time it saves is hours. As a rule: validate
at the boundary (where data enters your program), raise inside (when your own
invariants break).
"""

L3_VI = """
`raise` ném ngoại lệ một cách chủ đích — khi dữ liệu sai, hãy thất bại ầm ĩ:

```python
def set_price(price):
    if price < 0:
        raise ValueError(f"giá không thể âm, nhận được {price}")
    return price
```

Một hàm thất bại nhanh với thông điệp rõ ràng tốt hơn một hàm trả về kết quả
vô nghĩa để lỗi nổi lên ba tầng sau đó. Raise sớm biến một lỗi logic câm lặng
thành một lỗi runtime ồn ào, dễ gỡ.

## Kiểm tra phòng thủ trong thực tế

```python
def average(values):
    if not values:                 # None, [], rỗng — đều falsy
        raise ValueError("trung bình của dữ liệu rỗng là không xác định")
    return sum(values) / len(values)
```

Câu kiểm tra chỉ một dòng; thời gian gỡ lỗi nó cứu lại là hàng giờ. Quy tắc:
kiểm tra ở biên giới (nơi dữ liệu đi vào chương trình), raise bên trong (khi
bất biến của chính bạn bị vi phạm).
"""

L4 = """
Debugging is a method, not luck.

1. **Reproduce** — find the smallest input that triggers the bug.
2. **Read** — traceback? Wrong output? Start from the evidence.
3. **Locate** — narrow the search: does the bug exist in the input, the middle
   step, or the output? Print or assert along the pipeline until the region
   shrinks.
4. **Understand** — never fix what you cannot explain. "Delete this line, it
   seems to help" is how bugs become ghosts.
5. **Fix and verify** — one change at a time, then confirm the exact failure is
   gone AND nothing else broke.

## Tools you already have

- `print(type(x), repr(x))` — see the real value, not the format you assume.
- `assert condition, "message"` — state what MUST be true; Python checks it.
- Explaining the code out loud (even to a rubber duck) exposes wrong assumptions.

The Bug Hunt below is this method, drilled: each broken program is a real bug
pattern you will meet in your own code.
"""

L4_VI = """
Gỡ lỗi là một phương pháp, không phải vận may.

1. **Tái hiện** — tìm đầu vào nhỏ nhất gây ra lỗi.
2. **Đọc** — có traceback? Đầu ra sai? Hãy bắt đầu từ bằng chứng.
3. **Định vị** — thu hẹp phạm vi: lỗi nằm ở đầu vào, bước giữa, hay đầu ra?
   In hoặc assert dọc theo đường ống cho đến khi vùng nghi vấn nhỏ lại.
4. **Hiểu** — đừng sửa thứ bạn không giải thích được. "Xóa dòng này, hình như
   hết lỗi" là cách biến bug thành con ma.
5. **Sửa và kiểm chứng** — mỗi lần một thay đổi, rồi xác nhận đúng lỗi đó đã
   hết VÀ không có gì khác hỏng theo.

## Công cụ bạn đã có

- `print(type(x), repr(x))` — nhìn giá trị thật, không phải định dạng bạn đoán.
- `assert điều_kiện, "thông điệp"` — phát biểu cái PHẢI đúng; Python kiểm tra hộ.
- Giải thích mã thành tiếng (kể cả cho một chú vịt cao su) phơi bày giả định sai.

Bug Hunt bên dưới chính là phương pháp này được luyện tập: mỗi chương trình hỏng
là một mẫu lỗi thật mà bạn sẽ gặp trong mã của chính mình.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "m8-tracebacks-practice",
    "Traceback Reading",
    "Catch the right exception and raise your own.",
    "Đọc traceback",
    "Bắt đúng ngoại lệ và tự raise ngoại lệ của mình.",
    "tracebacks-try-except", 30, "beginner",
    [
        challenge(
            "py-ex-safe-int",
            "Safe Conversion",
            "The starter crashes on non-numeric text. Wrap the conversion in try/except so the program prints bad input instead of crashing.",
            'text = "42x"\nnumber = int(text)\nprint("converted:", number)\n',
            [("no crash, friendly message", 'assert printed[0] == "bad input, skipping", f"got {printed}"\nassert "except ValueError" in code, "catch ValueError specifically — a bare except hides real bugs (see lesson)"',
              "try: number = int(text) / except ValueError: print(\"bad input, skipping\")")],
            level="guided",
        ),
        challenge(
            "py-ex-specific-catch",
            "Catch the Right Thing",
            "Write fetch_score(data) that returns data[\"score\"] as an int, but returns -1 when the key is missing. Do NOT catch every exception — catch only the one that a missing key raises.",
            'def fetch_score(data):\n    pass\n',
            [("missing key handled", 'assert fetch_score({"score": 7}) == 7\nassert fetch_score({}) == -1, "missing key must give -1"\nassert "except KeyError" in code, "catch KeyError specifically"', 
              "try: return int(data[\"score\"]) / except KeyError: return -1")],
            level="guided",
        ),
        challenge(
            "py-ex-raise-negative",
            "Raise on Bad Input",
            "Write set_age(age) that returns age when it is 0..150 and raises ValueError with a message mentioning the number otherwise. The tests pass 200 and expect the raise.",
            'def set_age(age):\n    pass\n',
            [("raises with message", 'assert set_age(30) == 30\ntry:\n    set_age(200)\n    assert False, "200 must raise"\nexcept ValueError as e:\n    assert "200" in str(e), "message must mention the bad value"\ntry:\n    set_age(-5)\n    assert False, "negative must raise too"\nexcept ValueError:\n    pass',
              "if not (0 <= age <= 150): raise ValueError(f\"invalid age: {age}\") — raise, never clamp")],
            level="guided",
        ),
        challenge(
            "py-ex-average-guard",
            "Defensive Average",
            "Write average(values) that raises ValueError on empty input and returns the mean otherwise. average([2, 4, 9]) must be 5.0.",
            'def average(values):\n    pass\n',
            [("guards empty, computes mean", 'assert average([2, 4, 9]) == 5.0\ntry:\n    average([])\n    assert False, "empty must raise"\nexcept ValueError:\n    pass',
              "if not values: raise ValueError(...) / return sum(values) / len(values)")],
            level="independent",
        ),
    ],
    {
        "py-ex-safe-int": vi_challenge("Chuyển đổi an toàn", 'Phần khởi đầu sập với văn bản không phải số. Bọc phép chuyển đổi trong try/except để chương trình in thông báo thay vì sập.',
                                        [("không sập, thông điệp thân thiện", 'try: number = int(text) / except ValueError: print("bad input, skipping")')]),
        "py-ex-specific-catch": vi_challenge("Bắt đúng thứ", 'Viết fetch_score(data) trả về data["score"] dưới dạng int, nhưng trả về -1 khi thiếu khóa. ĐỪNG bắt mọi ngoại lệ — chỉ bắt cái mà khóa thiếu gây ra.',
                                        [("thiếu khóa được xử lý", 'try: return int(data["score"]) / except KeyError: return -1')]),
        "py-ex-raise-negative": vi_challenge("Raise khi đầu vào xấu", "Viết set_age(age) trả về age khi nó nằm trong 0..150 và raise ValueError kèm thông điệp nhắc đến con số trong trường hợp khác. Bài kiểm tra truyền 200 và mong đợi raise.",
                                        [("raise kèm thông điệp", 'if not (0 <= age <= 150): raise ValueError(f"invalid age: {age}")')]),
        "py-ex-average-guard": vi_challenge("Trung bình phòng thủ", "Viết average(values) raise ValueError với đầu vào rỗng và trả về giá trị trung bình trong trường hợp khác. average([2, 4, 9]) phải là 5.0.",
                                        [("chặn rỗng, tính trung bình", "if not values: raise ValueError(...) / return sum(values) / len(values)")]),
    },
    solutions=[
        ("py-ex-safe-int", 'text = "42x"\ntry:\n    number = int(text)\n    print("converted:", number)\nexcept ValueError:\n    print("bad input, skipping")',
         'text = "42x"\ntry:\n    number = int(text)\n    print("converted:", number)\nexcept:\n    print("bad input, skipping")'),
        ("py-ex-specific-catch", 'def fetch_score(data):\n    try:\n        return int(data["score"])\n    except KeyError:\n        return -1',
         'def fetch_score(data):\n    try:\n        return int(data["score"])\n    except ValueError:\n        return -1'),
        ("py-ex-raise-negative", 'def set_age(age):\n    if not (0 <= age <= 150):\n        raise ValueError(f"invalid age: {age}")\n    return age',
         'def set_age(age):\n    if age < 0:\n        age = 0\n    if age > 150:\n        age = 150\n    return age'),
        ("py-ex-average-guard", 'def average(values):\n    if not values:\n        raise ValueError("average of empty data")\n    return sum(values) / len(values)',
         'def average(values):\n    return sum(values) / len(values)'),
    ],
)

write_practice(
    MOD, "m8-bug-hunt",
    "Bug Hunt — Repair Broken Programs",
    "Four broken programs. Diagnose, fix, verify.",
    "Săn bug — Sửa các chương trình hỏng",
    "Bốn chương trình hỏng. Chẩn đoán, sửa, kiểm chứng.",
    "debugging-method", 45, "beginner",
    [
        challenge(
            "py-bug-scope",
            "Bug Hunt 1: The Missing Variable",
            "This receipt program crashes with NameError. Reproduce it mentally, find the line, and fix it with the SMALLEST change that restores the intended output (three lines).",
            'def add_item(total, price):\n    new_total = total + price\n\nitems = [120, 80, 45]\ntotal = 0\nfor price in items:\n    total = add_item(total, price)\nprint("item:", price)\nprint("total:", total)\nprint("thanks for shopping")\n',
            [("receipt restored", 'assert printed == ["item: 45", "total: 245", "thanks for shopping"], f"got {printed}"',
              "add_item computes new_total but never returns it — total becomes None after the first call. Fix: return new_total.")],
            level="debugging",
        ),
        challenge(
            "py-bug-off-by-one",
            "Bug Hunt 2: The Off-By-One",
            "A report should print the first five multiples of 3 (3, 6, 9, 12, 15). It prints the wrong range — diagnose and fix. Keep the loop a range loop.",
            'for i in range(1, 5):\n    print(i * 3)\n',
            [("first five multiples", 'assert printed == ["3", "6", "9", "12", "15"], f"got {printed}"',
              "range(1, 5) gives 1..4 — five numbers means range(1, 6); starting at 0 or 1 both change the values. Check the lesson examples.")],
            level="debugging",
        ),
        challenge(
            "py-bug-type-mix",
            "Bug Hunt 3: The Silent Type Mix",
            "This program runs without crashing — but prints 55 instead of 10. A logic error. Diagnose and fix so the total is numeric.",
            'a = "5"\nb = 5\ntotal = a + b\nprint("total:", total)\n',
            [("numeric total", 'assert printed == ["total: 10"], f"got {printed}"',
              "\"5\" is a string: \"5\" + 5 raises TypeError, but here the string wins by being first — convert with int(a).")],
            level="debugging",
        ),
        challenge(
            "py-bug-mutable-default",
            "Bug Hunt 4: The Shared Default",
            "Every call to add_task seems to remember previous calls — tasks pile up across calls. Fix WITHOUT removing the default: make each call start from a fresh list (or make the parameter required).",
            'def add_task(task, tasks=[]):\n    tasks.append(task)\n    return tasks\n\nadd_task("a")\nadd_task("b")\nresult = add_task("c")\nprint(result)\n',
            [("each call is fresh", 'assert len(printed) == 1 and "c" in printed[0] and "a" not in printed[0] and "b" not in printed[0], f"got {printed}"\nassert "[]" not in code.split("def add_task")[1].split(")")[0], "no mutable default allowed"',
              "The mutable default is created ONCE at definition time and shared. Fix: tasks=None, then tasks = [] inside the function.")],
            level="debugging",
        ),
    ],
    {
        "py-bug-scope": vi_challenge("Săn bug 1: Biến biến mất", 'Chương trình hóa đơn này sập với NameError. Tái hiện trong đầu, tìm dòng lỗi, và sửa bằng THAY ĐỔI NHỎ NHẤT khôi phục đầu ra mong muốn (ba dòng).',
                                        [("hóa đơn hoạt động lại", "add_item tính new_total nhưng không bao giờ return — total thành None sau lời gọi đầu. Fix: return new_total.")]),
        "py-bug-off-by-one": vi_challenge("Săn bug 2: Lệch một đơn vị", "Báo cáo cần in năm bội số đầu của 3 (3, 6, 9, 12, 15). Nó in sai phạm vi — chẩn đoán và sửa. Giữ vòng lặp dạng range.",
                                        [("năm bội số đầu", "range(1, 5) cho 1..4 — năm số nghĩa là range(1, 6); bắt đầu từ 0 hay 1 đều đổi giá trị. Xem ví dụ trong bài học.")]),
        "py-bug-type-mix": vi_challenge("Săn bug 3: Trộn kiểu câm lặng", "Chương trình chạy không sập — nhưng in 55 thay vì 10. Một lỗi logic. Chẩn đoán và sửa để tổng là số.",
                                        [("tổng dạng số", '"5" là chuỗi: "5" + 5 sẽ raise TypeError, nhưng ở đây chuỗi thắng vì đứng trước — chuyển bằng int(a).')]),
        "py-bug-mutable-default": vi_challenge("Săn bug 4: Mặc định dùng chung", "Mỗi lời gọi add_task dường như nhớ các lời gọi trước — task dồn cục qua các lần gọi. Sửa mà KHÔNG xóa mặc định: khiến mỗi lời gọi bắt đầu từ list mới (hoặc bắt buộc truyền tham số).",
                                        [("mỗi lời gọi là mới", "Mặc định mutable được tạo MỘT LẦN lúc định nghĩa và dùng chung. Fix: tasks=None, rồi tasks = [] bên trong hàm.")]),
    },
    solutions=[
        ("py-bug-scope", 'def add_item(total, price):\n    new_total = total + price\n    return new_total\n\nitems = [120, 80, 45]\ntotal = 0\nfor price in items:\n    total = add_item(total, price)\nprint("item:", price)\nprint("total:", total)\nprint("thanks for shopping")',
         'def add_item(total, price):\n    new_total = total + price\n\nitems = [120, 80, 45]\ntotal = 0\nfor price in items:\n    total = add_item(total, price)\nprint("item:", price)\nprint("total:", total)\nprint("thanks for shopping")'),
        ("py-bug-off-by-one", 'for i in range(1, 6):\n    print(i * 3)',
         'for i in range(1, 5):\n    print(i * 4)'),
        ("py-bug-type-mix", 'a = "5"\nb = 5\ntotal = int(a) + b\nprint("total:", total)',
         'a = "5"\nb = 5\ntotal = a + str(b)\nprint("total:", total)'),
        ("py-bug-mutable-default", 'def add_task(task, tasks=None):\n    if tasks is None:\n        tasks = []\n    tasks.append(task)\n    return tasks\n\nadd_task("a")\nadd_task("b")\nresult = add_task("c")\nprint(result)',
         'def add_task(task, tasks=[]):\n    tasks.append(task)\n    return tasks\n\nadd_task("a")\nadd_task("b")\nresult = add_task("c")\nprint(result)'),
    ],
)

write_practice(
    MOD, "m8-else-finally-practice",
    "else/finally & Fail-Fast Drills",
    "Structure error handling like a professional: narrow catches, explicit else, cleanup in finally.",
    "Bài tập else/finally & fail-fast",
    "Cấu trúc xử lý lỗi như một chuyên gia: bắt hẹp, else rõ ràng, dọn dẹp trong finally.",
    "else-finally-raise", 30, "beginner",
    [
        challenge(
            "py-ex-parse-lines",
            "Parse With Per-Line Rescue",
            "The starter crashes on the second line. Fix it so valid lines convert and invalid lines print skip: <line> — program continues to the end.",
            'lines = ["12", "abc", "7"]\nfor line in lines:\n    print(int(line) * 2)\n',
            [("rescues each line", 'assert printed == ["24", "skip: abc", "14"], f"got {printed}"',
              "Put try/except INSIDE the loop so one bad line doesn't end the program.")],
            level="guided",
        ),
        challenge(
            "py-ex-try-else",
            "Success Path in else",
            "Refactor: keep the try block containing ONLY the risky conversion, move the success print into else, and keep the error print in except. Output must stay identical for both a valid and an invalid value.",
            'value = "9"\ntry:\n    number = int(value)\n    print("ok:", number)\nexcept ValueError:\n    print("failed")\n',
            [("else used correctly", 'assert printed == ["ok: 9"], f"got {printed}"\nassert "else:" in code, "move the success print into an else block"',
              "try: number = int(value) / except ValueError: ... / else: print(\"ok:\", number)")],
            level="combination",
        ),
    ],
    {
        "py-ex-parse-lines": vi_challenge('Chực từng dòng', 'Phần khởi đầu sập ở dòng thứ hai. Sửa để các dòng hợp lệ được chuyển đổi và dòng lỗi in skip: <dòng> — chương trình chạy đến cuối.',
                                        [("cứu từng dòng", "Đặt try/except BÊN TRONG vòng lặp để một dòng xấu không kết thúc chương trình.")]),
        "py-ex-try-else": vi_challenge("Đường thành công vào else", 'Tái cấu trúc: giữ khối try CHỨA CHỈ phép chuyển đổi rủi ro, chuyển print thành công sang else, và giữ print lỗi trong except. Đầu ra phải giữ nguyên cho cả giá trị hợp lệ lẫn không hợp lệ.',
                                        [("else được dùng đúng", 'try: number = int(value) / except ValueError: ... / else: print("ok:", number)')]),
    },
    solutions=[
        ("py-ex-parse-lines", 'lines = ["12", "abc", "7"]\nfor line in lines:\n    try:\n        print(int(line) * 2)\n    except ValueError:\n        print(f"skip: {line}")',
         'lines = ["12", "abc", "7"]\nfor line in lines:\n    print(int(line) * 2)'),
        ("py-ex-try-else", 'value = "9"\ntry:\n    number = int(value)\nexcept ValueError:\n    print("failed")\nelse:\n    print("ok:", number)',
         'value = "9"\ntry:\n    number = int(value)\n    print("ok:", number)\nexcept:\n    print("failed")\nelse:\n    print("unused")'),
    ],
)

# ── Checkpoint: functions + errors ───────────────────────────────────────────
CP = """
## Checkpoint: Functions + Errors

Module 7 and 8 combined: build the small pipeline as functions, and make it
survive bad data. This is the load-bearing pattern of every file-based project
still ahead.
"""

CP_VI = """
## Checkpoint: Hàm + Lỗi

Module 7 và 8 kết hợp: xây đường ống nhỏ bằng các hàm, và khiến nó sống sót qua
dữ liệu xấu. Đây là mẫu chịu lực của mọi dự án dựa trên tệp còn phía trước.
"""

write_checkpoint(
    MOD, "checkpoint-functions-errors",
    "Checkpoint: Functions + Errors",
    "A function pipeline that fails fast and skips bad data.",
    20, CP,
    "Checkpoint: Hàm + Lỗi",
    "Đường ống hàm fail-fast và bỏ qua dữ liệu xấu.",
    CP_VI,
    challenge(
        "py-checkpoint-functions-errors",
        "Resilient Mean",
        "Write mean(texts) that receives a list of strings. Convert each to a number; strings that cannot convert are skipped. Return the mean of the converted values as a float. If NOTHING converts, raise ValueError with the word 'empty' in the message. Print mean(values) for values = [\"10\", \"x\", \"20\", \"\", \"30\"] — one line, formatted :.2f.",
        'values = ["10", "x", "20", "", "30"]\n\ndef mean(texts):\n    pass\n\nprint(f"{mean(values):.2f}")\n',
        [
            ("skips bad, returns mean",
             'assert abs(mean(["10", "x", "20", "", "30"]) - 20.0) < 1e-9, f"got {mean([\x2710\x27, \x27x\x27, \x2720\x27, \x27\x27, \x2730\x27])}"\nassert mean(["4"]) == 4.0, "single value works"\nassert abs(mean(["5", "5", "5"]) - 5.0) < 1e-9, "all valid works"',
             "int(t) in try/except; accumulate valid values then divide."),
            ("raises when nothing converts",
             'try:\n    mean(["a", "b"])\n    assert False, "nothing convertible must raise"\nexcept ValueError as e:\n    assert "empty" in str(e).lower(), "message must mention empty"',
             "count what converted; if count == 0: raise ValueError('empty ...')"),
        ],
        difficulty="beginner",
    ),
    vi_challenge("Trung bình kiên cường", 'Viết mean(texts) nhận danh sách chuỗi. Chuyển từng phần tử thành số; chuỗi không chuyển được bị bỏ qua. Trả về trung bình của các giá trị đã chuyển dưới dạng float. Nếu KHÔNG có gì chuyển được, raise ValueError có từ "empty" trong thông điệp. In mean(values) cho values = ["10", "x", "20", "", "30"] — một dòng, định dạng :.2f.',
                 [("bỏ qua lỗi, trả về trung bình", "int(t) trong try/except; cộng dồn các giá trị hợp lệ rồi chia."), 
                  ("raise khi không chuyển được gì", 'nếu count == 0: raise ValueError("empty")')]),
    solution='values = ["10", "x", "20", "", "30"]\n\ndef mean(texts):\n    nums = []\n    for t in texts:\n        try:\n            nums.append(int(t))\n        except ValueError:\n            pass\n    if not nums:\n        raise ValueError("empty input: nothing converted")\n    return sum(nums) / len(nums)\n\nprint(f"{mean(values):.2f}")',
    wrong='values = ["10", "x", "20", "", "30"]\n\ndef mean(texts):\n    nums = []\n    for t in texts:\n        nums.append(int(t))\n    return sum(nums) / len(nums)\n\nprint(f"{mean(values):.2f}")',
)

print("module 8 content written")
