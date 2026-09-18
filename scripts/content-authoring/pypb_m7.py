#!/usr/bin/env python3
"""Module 7: functions — lessons + practices. Direct triple-quote MDX."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "functions"

L1 = """
A **function** is a named, reusable block of code:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Minh")     # Hello, Minh!
greet("Lan")      # Hello, Lan!
```

Anatomy: `def` starts the definition; the name follows the same rules as
variables; **parameters** (`name`) are inputs the function receives; the body
is indented under the `def` line. **Defining does not run the code — calling
does.**

## Why functions exist

- **Reuse**: write once, call anywhere.
- **Naming**: `send_report()` documents intent better than 30 loose lines.
- **Testing**: a function is a unit you can check in isolation.
- **Decomposition**: big problems become small named steps.

## return: produce a result

`print` shows a human something; `return` hands a value back to the program:

```python
def add(a, b):
    return a + b

total = add(2, 3)     # total is now 5
print(add(10, 5) * 2) # return values compose into expressions
```

`return` also **exits** the function immediately. A function with no return
statement returns `None`.
"""

L1_VI = """
Một **hàm (function)** là một khối mã được đặt tên, dùng lại được:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Minh")     # Hello, Minh!
greet("Lan")      # Hello, Lan!
```

Giải phẫu: `def` bắt đầu định nghĩa; tên theo cùng quy tắc với biến; **tham số**
(`name`) là đầu vào mà hàm nhận; thân hàm được thụt vào dưới dòng `def`.
**Định nghĩa không chạy mã — lời gọi mới chạy.**

## Tại sao hàm tồn tại

- **Dùng lại**: viết một lần, gọi mọi nơi.
- **Đặt tên**: `send_report()` thể hiện ý đồ rõ hơn 30 dòng lỏng lẻo.
- **Kiểm thử**: một hàm là một đơn vị có thể kiểm tra riêng lẻ.
- **Phân rã**: bài toán lớn trở thành các bước nhỏ có tên.

## return: tạo ra kết quả

`print` hiển thị thứ gì đó cho con người; `return` trao một giá trị trả về cho
chương trình:

```python
def add(a, b):
    return a + b

total = add(2, 3)     # total giờ là 5
print(add(10, 5) * 2) # giá trị trả về kết hợp thành biểu thức được
```

`return` cũng **thoát khỏi hàm ngay lập tức**. Một hàm không có return sẽ trả
về `None`.
"""

L2 = """
## Default arguments

```python
def power(base, exponent=2):
    return base ** exponent

power(5)        # 25 — exponent defaults to 2
power(5, 3)     # 125
```

Defaults make optional behavior explicit. Never use a mutable default (a list
or dict) — it is shared across calls, a famous Python trap you will meet again
in Intermediate.

## Keyword arguments

Call with `name=value` — order stops mattering and calls become readable:

```python
def make_coffee(size, milk, sugar):
    return f"{size}, milk={milk}, sugar={sugar}"

make_coffee("L", milk=False, sugar=True)
```

## Scope: local by default

Names created inside a function exist only inside it:

```python
def calc():
    result = 42     # local
calc()
print(result)       # NameError — result is gone
```

Parameters are local too. Functions get information **in** through parameters
and **out** through return values — not through globals. That discipline is
what keeps larger programs sane.

## Docstrings

A triple-quoted first line documents the function; `help(name)` shows it:

```python
def celsius_to_f(c):
    '''Convert a Celsius temperature to Fahrenheit.'''
    return c * 9 / 5 + 32
```
"""

L2_VI = """
## Tham số mặc định

```python
def power(base, exponent=2):
    return base ** exponent

power(5)        # 25 — exponent mặc định là 2
power(5, 3)     # 125
```

Giá trị mặc định làm cho hành vi tùy chọn trở nên tường minh. Đừng bao giờ dùng
mặc định có thể thay đổi (list hoặc dict) — nó được chia sẻ qua các lần gọi, một
cái bẫy Python nổi tiếng bạn sẽ gặp lại ở Intermediate.

## Đối số theo tên (keyword arguments)

Gọi với `name=value` — thứ tự không còn quan trọng và lời gọi trở nên dễ đọc:

```python
def make_coffee(size, milk, sugar):
    return f"{size}, milk={milk}, sugar={sugar}"

make_coffee("L", milk=False, sugar=True)
```

## Phạm vi (scope): cục bộ theo mặc định

Tên được tạo bên trong hàm chỉ tồn tại bên trong nó:

```python
def calc():
    result = 42     # cục bộ
calc()
print(result)       # NameError — result đã biến mất
```

Tham số cũng là cục bộ. Hàm nhận thông tin **vào** qua tham số và đưa **ra**
qua giá trị trả về — không phải qua biến toàn cục. Kỷ luật này giữ cho các
chương trình lớn không trở nên điên loạn.

## Docstring

Một dòng ba dấu ngoặc kép đầu tiên tài liệu hóa hàm; `help(tên_hàm)` hiển thị nó:

```python
def celsius_to_f(c):
    '''Chuyển nhiệt độ Celsius sang Fahrenheit.'''
    return c * 9 / 5 + 32
```
"""

L3 = """
**Refactoring** is improving code without changing what it does. The most
common beginner refactor: copy-pasted code → functions.

Before:

```python
print("Welcome Minh, your balance is 120")
print("Welcome Lan, your balance is 90")
print("Welcome Bo, your balance is 0")
```

After:

```python
def welcome(name, balance):
    print(f"Welcome {name}, your balance is {balance}")

for who, amount in [("Minh", 120), ("Lan", 90), ("Bo", 0)]:
    welcome(who, amount)
```

Same output — but now one place to change the message, and a name that says
what the line does.

## How to spot refactor targets

- The same 2+ lines appear more than once → extract a function.
- A block does one identifiable job → give that job a name.
- A condition so long it needs a comment → name it (`is_valid_order(order)`).

## Decomposition in practice

Build programs as pipelines of small functions:

```python
def read_input(): ...
def process(data): ...
def format_output(result): ...
def main():
    data = read_input()
    print(format_output(process(data)))
```

Each function is testable alone; `main` reads like the problem statement.
That is the shape every remaining project in this course uses.
"""

L3_VI = """
**Tái cấu trúc (refactoring)** là cải tiến mã mà không đổi hành vi. Phép tái
cấu trúc phổ biến nhất của người mới: code copy-dán → hàm.

Trước:

```python
print("Welcome Minh, your balance is 120")
print("Welcome Lan, your balance is 90")
print("Welcome Bo, your balance is 0")
```

Sau:

```python
def welcome(name, balance):
    print(f"Welcome {name}, your balance is {balance}")

for who, amount in [("Minh", 120), ("Lan", 90), ("Bo", 0)]:
    welcome(who, amount)
```

Cùng một đầu ra — nhưng giờ có một nơi duy nhất để đổi thông điệp, và một cái
tên nói lên dòng lệnh làm gì.

## Cách phát hiện điểm cần tái cấu trúc

- Cùng 2+ dòng xuất hiện nhiều lần → tách thành hàm.
- Một khối làm đúng một việc nhận diện được → đặt tên cho việc đó.
- Một điều kiện dài đến mức cần chú thích → đặt tên cho nó (`is_valid_order(order)`).

## Phân rã trong thực tế

Xây chương trình như những đường ống gồm các hàm nhỏ:

```python
def read_input(): ...
def process(data): ...
def format_output(result): ...
def main():
    data = read_input()
    print(format_output(process(data)))
```

Mỗi hàm kiểm thử được độc lập; `main` đọc như một đề bài. Đó là hình dạng mà mọi
dự án còn lại trong khóa học sử dụng.
"""

write_lesson(MOD, "defining-functions", "Defining Functions",
             "def, parameters, calling, and return — functions that give answers.", 12,
             L1, "Định nghĩa hàm", "def, tham số, lời gọi, và return — hàm trả lời được.", L1_VI)

write_lesson(MOD, "defaults-scope-docstrings", "Defaults, Scope & Docstrings",
             "Optional parameters, keyword calls, local scope, and documentation.", 12,
             L2, "Mặc định, Phạm vi & Docstring", "Tham số tùy chọn, lời gọi theo tên, phạm vi cục bộ, và tài liệu hóa.", L2_VI)

write_lesson(MOD, "refactoring-decomposition", "Refactoring & Decomposition",
             "Turn copy-paste into named functions; build programs as pipelines.", 12,
             L3, "Tái cấu trúc & Phân rã", "Biến copy-dán thành hàm có tên; xây chương trình như đường ống.", L3_VI)

# ── Practices ───────────────────────────────────────────────────────────────
write_practice(
    MOD, "m7-def-practice",
    "Function Drills",
    "Write functions that return — not print.",
    "Bài tập hàm",
    "Viết hàm trả về — không phải in.",
    "defining-functions", 30, "beginner",
    [
        challenge(
            "py-fn-add",
            "The add Function",
            "Write a function add(a, b) that RETURNS the sum. The tests call it — printing is not enough.",
            "def add(a, b):\n    pass\n",
            [("returns sums", "assert add(2, 3) == 5, f\"add(2,3) should be 5, got {add(2, 3)}\"\nassert add(-1, 1) == 0, \"add(-1, 1) should be 0\"",
              "return a + b — the tests need the value, not the console.")],
            level="imitation",
        ),
        challenge(
            "py-fn-is-even",
            "is_even Predicate",
            "Write is_even(n) returning True when n is even.",
            "def is_even(n):\n    pass\n",
            [("predicate works", "assert is_even(4) is True and is_even(7) is False, \"is_even must return booleans\"",
              "return n % 2 == 0 — comparisons already produce booleans.")],
            level="guided",
        ),
        challenge(
            "py-fn-celsius",
            "Temperature Converter",
            "Write celsius_to_f(c) returning the Fahrenheit equivalent (c * 9 / 5 + 32). Give it a docstring.",
            "def celsius_to_f(c):\n    pass\n",
            [("converts", "assert abs(celsius_to_f(100) - 212) < 0.001, \"100C is 212F\"\nassert abs(celsius_to_f(0) - 32) < 0.001, \"0C is 32F\"\nassert (celsius_to_f.__doc__ or \"\").strip(), \"add a docstring\"",
              "The formula is in the lesson; the docstring is one triple-quoted line.")],
            level="guided",
        ),
        challenge(
            "py-fn-apply-tax",
            "Price With Tax",
            "Write price_with_tax(amount, rate=0.1) returning the amount plus tax. The default rate is 10%.",
            "def price_with_tax(amount, rate=0.1):\n    pass\n",
            [("default and custom rates", "assert abs(price_with_tax(100) - 110) < 0.001, \"default 10%\"\nassert abs(price_with_tax(100, 0.2) - 120) < 0.001, \"custom 20%\"",
              "return amount * (1 + rate) — the default makes the second argument optional.")],
            level="guided",
        ),
    ],
    {
        "py-fn-add": vi_challenge("Hàm add", "Viết hàm add(a, b) TRẢ VỀ tổng. Bài kiểm tra sẽ gọi nó — chỉ in ra là không đủ.",
                                    [("trả về tổng đúng", "return a + b — bài kiểm tra cần giá trị, không phải console.")]),
        "py-fn-is-even": vi_challenge("Vị từ is_even", "Viết is_even(n) trả về True khi n chẵn.",
                                        [("vị từ hoạt động", "return n % 2 == 0 — phép so sánh đã tạo ra boolean sẵn.")]),
        "py-fn-celsius": vi_challenge("Bộ chuyển nhiệt độ", "Viết celsius_to_f(c) trả về nhiệt độ Fahrenheit tương ứng (c * 9 / 5 + 32). Thêm docstring.",
                                        [("chuyển đổi đúng", "Công thức có trong bài học; docstring là một dòng ba dấu ngoặc kép.")]),
        "py-fn-apply-tax": vi_challenge("Giá có thuế", "Viết price_with_tax(amount, rate=0.1) trả về giá kèm thuế. Tỉ lệ mặc định là 10%.",
                                          [("tỉ lệ mặc định và tùy chọn", "return amount * (1 + rate) — mặc định làm đối số thứ hai trở nên tùy chọn.")]),
    },
    solutions=[
        ("py-fn-add", "def add(a, b):\n    return a + b",
         "def add(a, b):\n    print(a + b)"),
        ("py-fn-is-even", "def is_even(n):\n    return n % 2 == 0",
         "def is_even(n):\n    return n % 3 == 0"),
        ("py-fn-celsius", 'def celsius_to_f(c):\n    """Convert a Celsius temperature to Fahrenheit."""\n    return c * 9 / 5 + 32',
         'def celsius_to_f(c):\n    """Convert a Celsius temperature to Fahrenheit."""\n    return c * 5 / 9 + 32'),
        ("py-fn-apply-tax", "def price_with_tax(amount, rate=0.1):\n    return amount * (1 + rate)",
         "def price_with_tax(amount, rate=0.1):\n    return amount + rate"),
    ],
)

write_practice(
    MOD, "m7-refactor-practice",
    "Refactoring Drills",
    "De-duplicate and decompose given code.",
    "Bài tập tái cấu trúc",
    "Khử trùng lặp và phân rã mã cho trước.",
    "refactoring-decomposition", 35, "beginner",
    [
        challenge(
            "py-fn-refactor-greeting",
            "Extract the Greeting",
            "Three print lines greet three people. Refactor: write greet(name, balance) that returns the greeting string, and use it for all three people. Keep the printed lines IDENTICAL (three lines).",
            'print("Welcome Minh, your balance is 120")\nprint("Welcome Lan, your balance is 90")\nprint("Welcome Bo, your balance is 0")\n',
            [("same output, now factored", 'assert printed == ["Welcome Minh, your balance is 120", "Welcome Lan, your balance is 90", "Welcome Bo, your balance is 0"], f"got {printed}"\nassert "def greet" in code, "define greet(name, balance)"\nassert greet("Test", 5) == "Welcome Test, your balance is 5", "greet must RETURN the string, not print it"',
              "The function returns f\"Welcome {name}, your balance is {balance}\"; the loop prints each.")],
            level="mini-build",
        ),
        challenge(
            "py-fn-refactor-validate",
            "Name the Condition",
            "is_ok(age, member) is needed by two different checks in the starter. Write it: True when age >= 18 AND member is truthy. Use it from both call sites — do not duplicate the logic.",
            "def check_ticket(age, member):\n    return age >= 18 and member\n\ndef check_entry(age, member):\n    return age >= 18 and member\n",
            [("logic written once", "assert check_ticket(19, True) is True\nassert check_entry(17, True) is False\nassert \"age >= 18 and member\" not in code.split(\"def is_ok\")[-1] or True\nassert code.count(\"age >= 18 and member\") == 1, \"the condition should live in ONE place\"",
              "def is_ok(age, member): return age >= 18 and member — and both wrappers call it.")],
            level="mini-build",
        ),
        challenge(
            "py-fn-pipeline",
            "Three-Step Pipeline",
            "Build process_order(price): apply 10% discount if price >= 100, then add 5 shipping, and return the final total. Then print process_order(150) and process_order(50) — two lines with :.2f formatting.",
            "",
            [("pipeline results", 'assert printed == ["140.00", "55.00", "95.00"], f"got {printed}"\nassert process_order(100) == 95.0, "at exactly 100 the discount applies (>= 100)"',
              "150 >= 100 → 135 + 5 = 140; 50 → no discount → 50 + 5 = 55.")],
            level="mini-build",
        ),
    ],
    {
        "py-fn-refactor-greeting": vi_challenge("Tách lời chào", "Ba dòng print chào ba người. Tái cấu trúc: viết greet(name, balance) trả về chuỗi chào, và dùng nó cho cả ba người. Giữ các dòng in NGUYÊN VẸN (ba dòng).",
                                                   [("cùng đầu ra, đã gọn", "Hàm trả về f\"Welcome {name}, your balance is {balance}\"; vòng lặp in từng cái.")]),
        "py-fn-refactor-validate": vi_challenge("Đặt tên cho điều kiện", "is_ok(age, member) được hai chỗ kiểm tra khác nhau trong phần khởi đầu cần dùng. Hãy viết nó: True khi age >= 18 VÀ member là truthy. Dùng nó từ cả hai nơi gọi — đừng nhân bản logic.",
                                                     [("logic viết một nơi", "def is_ok(age, member): return age >= 18 and member — và cả hai wrapper gọi nó.")]),
        "py-fn-pipeline": vi_challenge("Đường ống ba bước", "Xây process_order(price): giảm 10% nếu price >= 100 (biên 100 cũng được giảm!), rồi cộng 5 tiền ship, và trả về tổng cuối. In process_order(150), process_order(50), và process_order(100) — ba dòng với định dạng :.2f.",
                                         [("kết quả đường ống", "150 >= 100 → 135 + 5 = 140; 50 → không giảm → 50 + 5 = 55.")]),
    },
    solutions=[
        ("py-fn-refactor-greeting", 'def greet(name, balance):\n    return f"Welcome {name}, your balance is {balance}"\n\nprint(greet("Minh", 120))\nprint(greet("Lan", 90))\nprint(greet("Bo", 0))',
         'def greet(name, balance):\n    print(f"Welcome {name}, your balance is {balance}")\n\ngreet("Minh", 120)\ngreet("Lan", 90)\ngreet("Bo", 0)'),
        ("py-fn-refactor-validate", "def is_ok(age, member):\n    return age >= 18 and member\n\ndef check_ticket(age, member):\n    return is_ok(age, member)\n\ndef check_entry(age, member):\n    return is_ok(age, member)",
         "def is_ok(age, member):\n    return age >= 18 or member\n\ndef check_ticket(age, member):\n    return is_ok(age, member)\n\ndef check_entry(age, member):\n    return is_ok(age, member)"),
        ("py-fn-pipeline", "def process_order(price):\n    if price >= 100:\n        price *= 0.9\n    return price + 5\n\nprint(f\"{process_order(150):.2f}\")\nprint(f\"{process_order(50):.2f}\")\nprint(f\"{process_order(100):.2f}\")",
         "def process_order(price):\n    if price > 100:\n        price *= 0.9\n    return price + 5\n\nprint(f\"{process_order(150):.2f}\")\nprint(f\"{process_order(50):.2f}\")\nprint(f\"{process_order(100):.2f}\")"),
    ],
)

print("module 7 content written")
