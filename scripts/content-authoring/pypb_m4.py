#!/usr/bin/env python3
"""Module 4: making-decisions — lessons + practices. Direct triple-quote MDX."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "making-decisions"

L1 = """
Programs get interesting when they choose. The `if` statement runs a block only
when its condition is `True`:

```python
temperature = 31
if temperature > 30:
    print("It's hot!")
    print("Drink water")
print("(always printed)")
```

## The colon + indentation rule

The `:` ends the condition line. Every line that *belongs to* the decision is
indented (4 spaces by convention). Dedenting closes the block. **Indentation is
not decoration in Python — it is the grammar.**

```python
if temperature > 30:
    print("hot")        # inside the if
print("done")           # outside — always runs
```

## else and elif

```python
if score >= 50:
    print("pass")
else:
    print("fail")
```

For many mutually exclusive cases, `elif` chains read top to bottom and the
**first true branch wins**:

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

Note the order: checking `score >= 70` first would give wrong grades — with
`elif`, put the most specific (highest) threshold first.
"""

L1_VI = """
Chương trình trở nên thú vị khi biết chọn. Câu lệnh `if` chỉ chạy một khối khi
điều kiện của nó là `True`:

```python
temperature = 31
if temperature > 30:
    print("It's hot!")
    print("Drink water")
print("(always printed)")
```

## Quy tắc dấu hai chấm + thụt lề

Dấu `:` kết thúc dòng điều kiện. Mọi dòng *thuộc về* quyết định được thụt vào
(4 dấu cách theo quy ước). Thụt lề thụt ra là đóng khối. **Trong Python, thụt lề
không phải trang trí — nó là ngữ pháp.**

```python
if temperature > 30:
    print("hot")        # bên trong if
print("done")           # bên ngoài — luôn chạy
```

## else và elif

```python
if score >= 50:
    print("pass")
else:
    print("fail")
```

Với nhiều trường hợp loại trừ lẫn nhau, chuỗi `elif` đọc từ trên xuống và
**nhánh đúng đầu tiên sẽ thắng**:

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

Chú ý thứ tự: kiểm tra `score >= 70` trước sẽ cho điểm sai — với `elif`, hãy đặt
ngưỡng cao nhất (cụ thể nhất) lên đầu.
"""

L2 = """
Python tests **truthiness**: every value is `True` or `False` in a condition.
The falsy gang: `0`, `0.0`, `""`, `[]`, `{}`, `None`, `False`. Everything else
is truthy.

```python
name = ""
if not name:
    print("name is empty — why not falsy check instead of len?")
```

Truthiness makes conditions read like English — but be explicit when 0 is a
*meaningful value* rather than "missing".

## Boolean logic

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("enter")
```

| Expression | True when |
| --- | --- |
| `a and b` | both truthy |
| `a or b` | at least one truthy |
| `not a` | a is falsy |

## Chained comparisons

A Python treat: `18 <= age < 65` does what it says. Use it — it matches how
humans write ranges.
"""

L2_VI = """
Python kiểm tra **tính chân thực (truthiness)**: mọi giá trị đều là `True` hoặc
`False` trong điều kiện. Nhóm falsy: `0`, `0.0`, `""`, `[]`, `{}`, `None`, `False`.
Mọi thứ còn lại là truthy.

```python
name = ""
if not name:
    print("name rỗng — kiểm tra falsy thay vì len?")
```

Truthiness giúp điều kiện đọc như tiếng Anh — nhưng hãy viết tường minh khi số 0
là một *giá trị có ý nghĩa* chứ không phải "thiếu dữ liệu".

## Logic boolean

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("enter")
```

| Biểu thức | True khi nào |
| --- | --- |
| `a and b` | cả hai truthy |
| `a or b` | ít nhất một truthy |
| `not a` | a là falsy |

## So sánh chuỗi (chained comparisons)

Đặc sản Python: `18 <= age < 65` nghĩa đúng như văn bản. Hãy dùng — nó khớp với
cách con người viết khoảng giá trị.
"""

L3 = """
Real programs check inputs before trusting them. **Validation** is just
decisions with a job:

```python
hour = 25          # from user input somewhere
if not 0 <= hour <= 23:
    print("invalid hour")
```

## The validation pattern

1. Check the shape of the data (is it present? the right type?).
2. Check the range/domain (is it sensible?).
3. Fail early with a clear message; otherwise proceed.

```python
username = "ab"
if len(username) < 3:
    print("too short: need at least 3 characters")
elif " " in username:
    print("no spaces allowed")
else:
    print("welcome,", username)
```

A validator is the perfect mini project: pure decisions, immediate feedback,
and it is exactly what every real backend does before touching a database.
"""

L3_VI = """
Chương trình thực thụ kiểm tra dữ liệu vào trước khi tin tưởng. **Kiểm tra hợp lệ
(validation)** chỉ là các quyết định được giao việc:

```python
hour = 25          # từ dữ liệu người dùng ở đâu đó
if not 0 <= hour <= 23:
    print("invalid hour")
```

## Mẫu kiểm tra hợp lệ

1. Kiểm tra hình dạng dữ liệu (có tồn tại? đúng kiểu chưa?).
2. Kiểm tra khoảng/giới hạn (có hợp lý không?).
3. Thất bại sớm với thông báo rõ ràng; nếu ổn thì tiếp tục.

```python
username = "ab"
if len(username) < 3:
    print("too short: need at least 3 characters")
elif " " in username:
    print("no spaces allowed")
else:
    print("welcome,", username)
```

Bộ kiểm tra hợp lệ là mini project hoàn hảo: toàn quyết định, phản hồi tức thì,
và chính là điều mọi backend thật làm trước khi đụng vào cơ sở dữ liệu.
"""

write_lesson(MOD, "if-elif-else", "if / elif / else",
             "Branching: conditions, blocks, and the first-true-branch-wins rule.", 12,
             L1, "if / elif / else", "Rẽ nhánh: điều kiện, khối lệnh, và quy tắc nhánh đúng đầu tiên thắng.", L1_VI)

write_lesson(MOD, "truthiness-boolean-logic", "Truthiness & Boolean Logic",
             "Falsy values, and/or/not, and chained comparisons.", 10,
             L2, "Truthiness & Logic Boolean", "Giá trị falsy, and/or/not, và so sánh chuỗi.", L2_VI)

write_lesson(MOD, "validation-patterns", "Validation Patterns",
             "Decisions with a job: checking inputs before trusting them.", 10,
             L3, "Mẫu kiểm tra hợp lệ", "Quyết định có nhiệm vụ: kiểm tra dữ liệu vào trước khi tin tưởng.", L3_VI)

# ── Practices ───────────────────────────────────────────────────────────────
write_practice(
    MOD, "m4-if-practice",
    "Decision Drills",
    "Branch on values with if/elif/else.",
    "Bài tập rẽ nhánh",
    "Rẽ nhánh theo giá trị với if/elif/else.",
    "if-elif-else", 30, "beginner",
    [
        challenge(
            "py-if-positivity",
            "Positive or Not",
            "number is given. Print positive if it is greater than 0, otherwise print non-positive (one if/else).",
            "number = 7\n",
            [("branches correctly", 'assert printed == ["positive"], f"got {printed}"',
              "if number > 0: ... else: ...")],
            level="imitation",
        ),
        challenge(
            "py-if-grade",
            "Grade Letter",
            "score is given. Print A (>= 90), B (>= 80), C (>= 70), or F — using an elif chain.",
            "score = 85\n",
            [("prints B", 'assert printed == ["B"], f"got {printed}"\nassert "elif" in code, "use an elif chain"',
              "Highest threshold first — first true branch wins.")],
            level="guided",
        ),
        challenge(
            "py-if-max",
            "The Larger Value",
            "a and b are given. Print the larger one. Do not use max() — decide it yourself.",
            "a = 12\nb = 9\n",
            [("prints larger", 'assert printed == ["12"], f"got {printed}"\nassert "max(" not in code, "decide with if/else, no max()"',
              "if a > b: print(a) else: print(b).")],
            level="guided",
        ),
    ],
    {
        "py-if-positivity": vi_challenge("Dương hay không", "number đã cho. In positive nếu lớn hơn 0, ngược lại in non-positive (một if/else).",
                                           [("rẽ nhánh đúng", "if number > 0: ... else: ...")]),
        "py-if-grade": vi_challenge("Chữ cái điểm", "score đã cho. In A (>= 90), B (>= 80), C (>= 70), hoặc F — dùng chuỗi elif.",
                                      [("in B", "Ngưỡng cao nhất trước — nhánh đúng đầu tiên thắng.")]),
        "py-if-max": vi_challenge("Giá trị lớn hơn", "a và b đã cho. In giá trị lớn hơn. Đừng dùng max() — tự quyết định nhé.",
                                    [("in giá trị lớn hơn", "if a > b: print(a) else: print(b).")]),
    },
    solutions=[
        ("py-if-positivity", "number = 7\nif number > 0:\n    print(\"positive\")\nelse:\n    print(\"non-positive\")",
         "number = 7\nif number < 0:\n    print(\"positive\")\nelse:\n    print(\"non-positive\")"),
        ("py-if-grade", "score = 85\nif score >= 90:\n    print(\"A\")\nelif score >= 80:\n    print(\"B\")\nelif score >= 70:\n    print(\"C\")\nelse:\n    print(\"F\")",
         "score = 85\nif score >= 70:\n    print(\"C\")\nelif score >= 80:\n    print(\"B\")\nelif score >= 90:\n    print(\"A\")\nelse:\n    print(\"F\")"),
        ("py-if-max", "a = 12\nb = 9\nif a > b:\n    print(a)\nelse:\n    print(b)",
         "a = 12\nb = 9\nif a < b:\n    print(a)\nelse:\n    print(b)"),
    ],
)

write_practice(
    MOD, "m4-logic-practice",
    "Logic & Truthiness",
    "Combine conditions like a professional.",
    "Logic & Truthiness",
    "Kết hợp điều kiện như một lập trình viên chuyên nghiệp.",
    "truthiness-boolean-logic", 30, "beginner",
    [
        challenge(
            "py-logic-ticket",
            "Concert Entry",
            "age and has_id are given. Print allowed only if age is 18 or more AND has_id is truthy; otherwise print denied.",
            "age = 17\nhas_id = True\n",
            [("decides entry", 'assert printed == ["denied"], f"got {printed}"',
              "if age >= 18 and has_id:")],
            level="guided",
        ),
        challenge(
            "py-logic-weekend",
            "Weekend Detector",
            'day = "sat" is given. Print weekend if day is "sat" or "sun"; otherwise print weekday.',
            'day = "sat"\n',
            [("detects weekend", 'assert printed == ["weekend"], f"got {printed}"',
              'if day == "sat" or day == "sun":')],
            level="guided",
        ),
        challenge(
            "py-logic-falsy",
            "Default Value",
            'name = "" is given. If it is empty, print anonymous; otherwise print the name. Use truthiness — no len().',
            'name = ""\n',
            [("handles empty", 'assert printed == ["anonymous"], f"got {printed}"\nassert "len(" not in code, "use truthiness, not len()"',
              "if not name: is the Pythonic empty check.")],
            level="guided",
        ),
        challenge(
            "py-logic-range",
            "In Range?",
            "age is given. Print working age if 18 <= age < 65 — with one chained comparison.",
            "age = 18\n",
            [("uses chained comparison", 'assert printed == ["working age"], f"got {printed}"\nassert " and " not in code, "use 18 <= age < 65 chaining"',
              "if 18 <= age < 65: reads exactly like the requirement.")],
            level="prediction",
        ),
    ],
    {
        "py-logic-ticket": vi_challenge("Vào concert", "age và has_id đã cho. In allowed chỉ khi age từ 18 trở lên VÀ has_id là truthy; ngược lại in denied.",
                                          [("quyết định vào cửa", "if age >= 18 and has_id:")]),
        "py-logic-weekend": vi_challenge("Phát hiện ngày cuối tuần", 'day = "sat" đã cho. In weekend nếu day là "sat" hoặc "sun"; ngược lại in weekday.',
                                           [("nhận diện cuối tuần", 'if day == "sat" or day == "sun":')]),
        "py-logic-falsy": vi_challenge("Giá trị mặc định", 'name = "" đã cho. Nếu rỗng, in anonymous; ngược lại in tên. Dùng truthiness — đừng dùng len().',
                                         [("xử lý rỗng", "if not name: là cách kiểm tra rỗng chuẩn Python.")]),
        "py-logic-range": vi_challenge("Trong khoảng?", "age đã cho. In working age nếu 18 <= age < 65 — bằng một phép so sánh chuỗi.",
                                        [("dùng so sánh chuỗi", "if 18 <= age < 65: đọc đúng như yêu cầu bài toán.")]),
    },
    solutions=[
        ("py-logic-ticket", "age = 17\nhas_id = True\nif age >= 18 and has_id:\n    print(\"allowed\")\nelse:\n    print(\"denied\")",
         "age = 17\nhas_id = True\nif age >= 18 or has_id:\n    print(\"allowed\")\nelse:\n    print(\"denied\")"),
        ("py-logic-weekend", 'day = "sat"\nif day == "sat" or day == "sun":\n    print("weekend")\nelse:\n    print("weekday")',
         'day = "sat"\nif day == "sat" and day == "sun":\n    print("weekend")\nelse:\n    print("weekday")'),
        ("py-logic-falsy", 'name = ""\nif not name:\n    print("anonymous")\nelse:\n    print(name)',
         'name = ""\nif name is None:\n    print("anonymous")\nelse:\n    print(name)'),
        ("py-logic-range", 'age = 18\nif 18 <= age < 65:\n    print("working age")\nelse:\n    print("not working age")',
         'age = 18\nif 18 < age < 65:\n    print("working age")\nelse:\n    print("not working age")'),
    ],
)

write_practice(
    MOD, "m4-validation-practice",
    "Mini Builds: Validators",
    "Guard real inputs with layered checks.",
    "Mini build: Bộ kiểm tra hợp lệ",
    "Bảo vệ dữ liệu vào bằng các lớp kiểm tra.",
    "validation-patterns", 35, "beginner",
    [
        challenge(
            "py-val-password",
            "Password Validator",
            'password = "sunshine" is given (8 chars, no digit). The length check passes; print no digit if the password has no digits at all, else print ok.',
            'password = "sunshine"\n',
            [("validates password", 'assert printed == ["no digit"], f"got {printed}"',
              "Eight chars pass the length check; the digit check must fire (elif).")],
            level="guided",
        ),
        challenge(
            "py-val-shipping",
            "Shipping Calculator",
            'weight = 1.0 is given (kg — right on the boundary). Print the cost: 5.0 for up to 1kg inclusive, 9.0 for up to 5kg, 15.0 above — formatted with :.2f.',
            "weight = 1.0\n",
            [("prints cost", 'assert printed == ["5.00"], f"got {printed}"',
              "elif chain on thresholds, then print(f\"{cost:.2f}\")")],
            level="independent",
        ),
        challenge(
            "py-val-username",
            "Username Rules",
            'username = "a b" is given. Print invalid if it is shorter than 3 characters OR contains a space; otherwise print valid.',
            'username = "a b"\n',
            [("validates username", 'assert printed == ["invalid"], f"got {printed}"',
              "if len(username) < 3 or \" \" in username:")],
            level="independent",
        ),
    ],
    {
        "py-val-password": vi_challenge("Kiểm tra mật khẩu", 'password = "sun9" đã cho. In weak nếu ngắn hơn 8 ký tự; in ok nếu không. Sau đó mở rộng: in thêm no digit nếu không có chữ số nào (sau bước kiểm tra độ dài).',
                                          [("kiểm tra mật khẩu", "Kiểm tra độ dài bằng len(); elif not có ký tự .isdigit() nào.")]),
        "py-val-shipping": vi_challenge("Tính phí vận chuyển", 'weight = 2.5 đã cho (kg). In cước phí: 5.0 cho đến 1kg, 9.0 cho đến 5kg, 15.0 cho trên 5kg — định dạng với :.2f.',
                                          [("in cước phí", "Chuỗi elif theo ngưỡng, rồi print(f\"{cost:.2f}\")")]),
        "py-val-username": vi_challenge("Quy tắc tên người dùng", 'username = "a b" đã cho. In invalid nếu ngắn hơn 3 ký tự HOẶC chứa dấu cách; ngược lại in valid.',
                                          [("kiểm tra username", 'if len(username) < 3 or " " in username:')]),
    },
    solutions=[
        ("py-val-password", 'password = "sunshine"\nif len(password) < 8:\n    print("weak")\nelif not any(c.isdigit() for c in password):\n    print("no digit")\nelse:\n    print("ok")',
         'password = "sunshine"\nif len(password) <= 8:\n    print("weak")\nelif not any(c.isdigit() for c in password):\n    print("no digit")\nelse:\n    print("ok")'),
        ("py-val-shipping", "weight = 1.0\nif weight <= 1:\n    cost = 5.0\nelif weight <= 5:\n    cost = 9.0\nelse:\n    cost = 15.0\nprint(f\"{cost:.2f}\")",
         "weight = 1.0\nif weight < 1:\n    cost = 5.0\nelif weight <= 5:\n    cost = 9.0\nelse:\n    cost = 15.0\nprint(f\"{cost:.2f}\")"),
        ("py-val-username", 'username = "a b"\nif len(username) < 3 or " " in username:\n    print("invalid")\nelse:\n    print("valid")',
         'username = "a b"\nif len(username) < 3 and " " in username:\n    print("invalid")\nelse:\n    print("valid")'),
    ],
)

print("module 4 content written")
