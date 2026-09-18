#!/usr/bin/env python3
"""Module 2: variables-and-data-types — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "variables-and-data-types"

L_VAR = """
A **variable** is a name that refers to a value. Assignment uses `=` (read it as
"becomes", not "equals"):

```python
age = 21
name = "Minh"
```

Variables let programs *remember*. Once assigned, use the name anywhere below:

```python
price = 5
quantity = 3
total = price * quantity   # 15
print(total)
```

## Naming rules (and taste)

- Names may contain letters, digits, and underscores: `user_name`, `score2`.
- They cannot *start* with a digit or contain spaces.
- Case matters: `total` and `Total` are different names.
- Style: use `snake_case` — lowercase with underscores. Future-you reads names
  as documentation.

## Reassignment

Variables point to values; pointing can change:

```python
score = 10
score = score + 5   # now 15
```

Python evaluates the right side first (`10 + 5`), then re-points the name.
"""


L_VAR_VI = """
Một **biến** (variable) là một cái tên tham chiếu đến một giá trị. Phép gán dùng `=`
(đọc là "becomes" — "trở thành", không phải "bằng"):

```python
age = 21
name = "Minh"
```

Biến giúp chương trình *ghi nhớ*. Sau khi gán, dùng tên đó ở bất kỳ đâu phía dưới:

```python
price = 5
quantity = 3
total = price * quantity   # 15
print(total)
```

## Quy tắc đặt tên (và khẩu vị)

- Tên có thể chứa chữ cái, chữ số, và dấu gạch dưới: `user_name`, `score2`.
- Tên không được *bắt đầu* bằng chữ số hoặc chứa dấu cách.
- Phân biệt chữ hoa/thường: `total` và `Total` là hai tên khác nhau.
- Phong cách: dùng `snake_case` — chữ thường với dấu gạch dưới. Cái tên chính là tài liệu.

## Gán lại

Biến trỏ đến giá trị; việc trỏ có thể thay đổi:

```python
score = 10
score = score + 5   # giờ là 15
```

Python đánh giá vế phải trước (`10 + 5`), rồi mới trỏ lại tên.
"""


L_TYPES = """
Python values have **types**. The five you will use constantly:

| Type | Meaning | Example |
| --- | --- | --- |
| `int` | whole numbers | `42`, `-7` |
| `float` | decimal numbers | `3.14`, `-0.5` |
| `str` | text | `"hello"`, `'a'` |
| `bool` | truth values | `True`, `False` |
| `NoneType` | "no value" | `None` |

## Type inspection

`type(x)` returns a value's type — indispensable while learning:

```python
type(42)        # <class 'int'>
type(42.0)      # <class 'float'>
type("42")      # <class 'str'>
```

Note `42` vs `42.0` vs `"42"` — three different types. Python cares.

## Conversion

Convert explicitly with `int()`, `float()`, `str()`:

```python
int("42")       # 42
float("3.5")    # 3.5
str(99)         # "99"
int("3.5")      # ValueError! int() refuses decimal text
```

Conversions between numbers and text are how programs talk to humans: input
arrives as text; math needs numbers; output goes back to text.

## Why None exists

`None` means "nothing here yet" — the placeholder for a result you do not have.
You will meet it constantly once functions arrive.
"""


L_TYPES_VI = """
Giá trị trong Python có **kiểu** (type). Năm kiểu bạn sẽ dùng liên tục:

| Kiểu | Ý nghĩa | Ví dụ |
| --- | --- | --- |
| `int` | số nguyên | `42`, `-7` |
| `float` | số thập phân | `3.14`, `-0.5` |
| `str` | văn bản | `"hello"`, `'a'` |
| `bool` | giá trị chân lý | `True`, `False` |
| `NoneType` | "không có giá trị" | `None` |

## Kiểm tra kiểu

`type(x)` trả về kiểu của giá trị — cực kỳ hữu ích khi học:

```python
type(42)        # <class 'int'>
type(42.0)      # <class 'float'>
type("42")      # <class 'str'>
```

Chú ý `42` khác `42.0` khác `"42"` — ba kiểu khác nhau. Python phân biệt rõ.

## Chuyển đổi kiểu

Chuyển đổi tường minh với `int()`, `float()`, `str()`:

```python
int("42")       # 42
float("3.5")    # 3.5
str(99)         # "99"
int("3.5")      # ValueError! int() từ chối văn bản có dấu thập phân
```

Chuyển đổi giữa số và văn bản là cách chương trình nói chuyện với con người:
dữ liệu vào là văn bản; tính toán cần số; kết quả trả về văn bản.

## Tại sao có None

`None` nghĩa là "chưa có gì ở đây" — chỗ trống cho một kết quả bạn chưa có. Bạn sẽ
gặp nó rất thường xuyên khi đến bài hàm.
"""


L_OPS = """
## Arithmetic

| Operator | Does | Example |
| --- | --- | --- |
| `+` `-` `*` | add, subtract, multiply | `2 * 3` → `6` |
| `/` | true division (always float) | `7 / 2` → `3.5` |
| `//` | floor division (drops remainder) | `7 // 2` → `3` |
| `%` | modulo (remainder) | `7 % 2` → `1` |
| `**` | power | `2 ** 10` → `1024` |

`//` and `%` are a pair: how many whole times does 2 fit into 7 (`3`), and what
is left over (`1`). Even/odd checks, cycling through positions, splitting items
into groups — modulo is everywhere.

## Comparison operators

```python
age == 18    # equals (two signs — one sign is assignment!)
age != 18    # not equals
age < 18     # less than
age >= 18    # greater or equal
```

Comparisons produce **booleans**: `True` or `False`.

## Combining conditions

```python
age >= 13 and age <= 19   # both must hold
day == "sat" or day == "sun"
not is_empty
```

## Precedence

`**` beats `* / // %` which beat `+ -`; parentheses win over everything:

```python
2 + 3 * 4     # 14 — not 20
(2 + 3) * 4   # 20
```

## Augmented assignment

```python
score += 5    # same as score = score + 5
count -= 1
name *= 2
```
"""


L_OPS_VI = """
## Số học

| Toán tử | Tác dụng | Ví dụ |
| --- | --- | --- |
| `+` `-` `*` | cộng, trừ, nhân | `2 * 3` → `6` |
| `/` | chia thực (luôn ra float) | `7 / 2` → `3.5` |
| `//` | chia lấy nguyên (bỏ phần dư) | `7 // 2` → `3` |
| `%` | chia lấy dư (modulo) | `7 % 2` → `1` |
| `**` | lũy thừa | `2 ** 10` → `1024` |

`//` và `%` là một cặp: số 2 vào trọn vẹn trong 7 bao nhiêu lần (`3`), và còn dư
bao nhiêu (`1`). Kiểm tra chẵn/lẻ, xoay vòng vị trí, chia nhóm — modulo có ở khắp nơi.

## Toán tử so sánh

```python
age == 18    # bằng (hai dấu = — một dấu là phép gán!)
age != 18    # khác
age < 18     # nhỏ hơn
age >= 18    # lớn hơn hoặc bằng
```

Phép so sánh tạo ra **boolean**: `True` hoặc `False`.

## Kết hợp điều kiện

```python
age >= 13 and age <= 19   # cả hai phải đúng
day == "sat" or day == "sun"
not is_empty
```

## Độ ưu tiên

`**` mạnh hơn `* / // %` mạnh hơn `+ -`; dấu ngoặc luôn thắng tất cả:

```python
2 + 3 * 4     # 14 — không phải 20
(2 + 3) * 4   # 20
```

## Gán mở rộng

```python
score += 5    # giống score = score + 5
count -= 1
name *= 2
```
"""


write_lesson(MOD, "variables-assignment", "Variables & Assignment",
             "Names that remember: assignment, naming, reassignment.", 10,
             L_VAR, "Biến & Gán", "Tên gọi giúp ghi nhớ: gán, quy tắc đặt tên, gán lại.", L_VAR_VI)

write_lesson(MOD, "numbers-booleans-none", "Numbers, Booleans & None",
             "The core types: int, float, bool, None — and conversions between them.", 12,
             L_TYPES, "Số, Boolean & None", "Các kiểu lõi: int, float, bool, None — và chuyển đổi giữa chúng.", L_TYPES_VI)

write_lesson(MOD, "operators-precedence", "Operators & Precedence",
             "Arithmetic, division flavors, comparisons, boolean logic, and precedence.", 12,
             L_OPS, "Toán tử & Độ ưu tiên", "Số học, các kiểu chia, so sánh, logic boolean, và độ ưu tiên.", L_OPS_VI)

# ── Practices ───────────────────────────────────────────────────────────────
write_practice(
    MOD, "m2-variables-practice",
    "Variable Drills",
    "Assign, combine, and update variables.",
    "Bài tập biến",
    "Gán, kết hợp, và cập nhật biến.",
    "variables-assignment", 30, "beginner",
    [
        challenge(
            "py-var-swap",
            "Swap Two Variables",
            "a is 1 and b is 2. Swap their values using a third variable, then print them as: a=2 then b=1 (two prints).",
            "a = 1\nb = 2\n",
            [
                ("values swapped", 'assert printed == ["a=2", "b=1"], f"got {printed}"',
                 "Store a in temp before overwriting: temp = a; a = b; b = temp."),
            ],
            level="guided",
        ),
        challenge(
            "py-var-total",
            "Receipt Total",
            "Variables price = 4.5 and quantity = 3 are given. Compute total cost and print exactly: Total: 13.5",
            "price = 4.5\nquantity = 3\n",
            [
                ("prints total", 'assert printed == ["Total: 13.5"], f"got {printed}"',
                 "total = price * quantity, then print(\"Total:\", total)."),
            ],
            level="imitation",
        ),
        challenge(
            "py-var-counter",
            "Update the Counter",
            "Start from the given counter. Increase it by 1 three times using +=, then print the final value.",
            "count = 0\n",
            [
                ("counter is 3", 'assert printed == ["3"], f"got {printed}"',
                 "count += 1 three times — not count = +1."),
            ],
            level="guided",
        ),
    ],
    {
        "py-var-swap": vi_challenge("Hoán đổi hai biến", "a là 1 và b là 2. Hoán đổi giá trị bằng một biến thứ ba, rồi in: a=2 rồi b=1 (hai lần print).",
                                     [("đã hoán đổi", "Lưu a vào temp trước khi ghi đè: temp = a; a = b; b = temp.")]),
        "py-var-total": vi_challenge("Tổng hóa đơn", "Biến price = 4.5 và quantity = 3 đã cho. Tính tổng tiền và in chính xác: Total: 13.5",
                                      [("in tổng", "total = price * quantity, rồi print(\"Total:\", total).")]),
        "py-var-counter": vi_challenge("Cập nhật bộ đếm", "Bắt đầu từ bộ đếm đã cho. Tăng lên 1 ba lần bằng +=, rồi in giá trị cuối.",
                                        [("bộ đếm là 3", "count += 1 ba lần — không phải count = +1.")]),
    },
    solutions=[
        ("py-var-swap", "a = 1\nb = 2\ntemp = a\na = b\nb = temp\nprint(\"a=\" + str(a))\nprint(\"b=\" + str(b))",
         "a = 1\nb = 2\na = b\nprint(\"a=\" + str(a))\nprint(\"b=\" + str(b))"),
        ("py-var-total", "price = 4.5\nquantity = 3\ntotal = price * quantity\nprint(\"Total:\", total)",
         "price = 4.5\nquantity = 3\nprint(\"Total:\", price)"),
        ("py-var-counter", "count = 0\ncount += 1\ncount += 1\ncount += 1\nprint(count)",
         "count = 0\ncount = 1\nprint(count)"),
    ],
)

write_practice(
    MOD, "m2-conversions-practice",
    "Type Conversions",
    "Numbers, text, and the bridges between them.",
    "Chuyển đổi kiểu",
    "Số, văn bản, và cây cầu nối giữa chúng.",
    "numbers-booleans-none", 30, "beginner",
    [
        challenge(
            "py-conv-parse",
            "Parse the Number",
            "total_text holds a number as text (\"120\"). Convert it to int, add 30, and print the numeric result.",
            "total_text = \"120\"\n",
            [
                ("prints 150", 'assert printed == ["150"], f"got {printed}"',
                 "int(total_text) + 30 — then print the result."),
            ],
            level="guided",
        ),
        challenge(
            "py-conv-float-trap",
            "The int() Trap",
            "rating_text is \"4.6\". Convert it to a float and print its integer part using int().",
            "rating_text = \"4.6\"\n",
            [
                ("prints 4", 'assert printed == ["4"], f"got {printed}"',
                 "int() cannot parse \"4.6\" directly — go through float first."),
            ],
            level="guided",
        ),
        challenge(
            "py-conv-str-build",
            "Build a Label",
            "Given code = 7 and prefix = \"CJ-\", produce the label CJ-7 by converting the number to text.",
            "code = 7\nprefix = \"CJ-\"\n",
            [
                ("prints CJ-7", 'assert printed == ["CJ-7"], f"got {printed}"',
                 "str(code) converts the number so + can join the strings."),
            ],
            level="guided",
        ),
    ],
    {
        "py-conv-parse": vi_challenge("Phân tích số", "total_text chứa một số dưới dạng văn bản (\"120\"). Chuyển sang int, cộng 30, và in kết quả số.",
                                       [("in 150", "int(total_text) + 30 — rồi in kết quả.")]),
        "py-conv-float-trap": vi_challenge("Bẫy int()", "rating_text là \"4.6\". Chuyển sang float và in phần nguyên bằng int().",
                                            [("in 4", "int() không phân tích trực tiếp \"4.6\" — đi qua float trước.")]),
        "py-conv-str-build": vi_challenge("Tạo nhãn", "Cho code = 7 và prefix = \"CJ-\", tạo nhãn CJ-7 bằng cách chuyển số thành văn bản.",
                                            [("in CJ-7", "str(code) chuyển số thành văn bản để + nối được chuỗi.")]),
    },
    solutions=[
        ("py-conv-parse", "total_text = \"120\"\nnumber = int(total_text)\nprint(number + 30)",
         "total_text = \"120\"\nprint(total_text + 30)"),
        ("py-conv-float-trap", "rating_text = \"4.6\"\nprint(int(float(rating_text)))",
         "rating_text = \"4.6\"\nprint(int(rating_text))"),
        ("py-conv-str-build", "code = 7\nprefix = \"CJ-\"\nprint(prefix + str(code))",
         "code = 7\nprefix = \"CJ-\"\nprint(prefix + code)"),
    ],
)

write_practice(
    MOD, "m2-operators-practice",
    "Operator Drills",
    "Division flavors, modulo tricks, and precedence.",
    "Bài tập toán tử",
    "Các kiểu chia, mẹo modulo, và độ ưu tiên.",
    "operators-precedence", 35, "beginner",
    [
        challenge(
            "py-op-divide",
            "Three Divisions",
            "For 17 cookies shared by 5 friends, print three lines: whole cookies each (floor), leftover cookies (modulo), and exact share per friend (true division).",
            "cookies = 17\nfriends = 5\n",
            [
                ("prints all three", 'assert printed == ["3", "2", "3.4"], f"got {printed}"',
                 "17 // 5, 17 % 5, and 17 / 5 — print each."),
            ],
            level="guided",
        ),
        challenge(
            "py-op-even",
            "Even or Odd",
            "Print True if the given number is even, False otherwise. One comparison with modulo.",
            "number = 8\n",
            [
                ("uses modulo parity", 'assert printed == ["True"], f"got {printed}"\nassert "%" in code, "use % to test parity"',
                 "number % 2 == 0 is True for even numbers."),
            ],
            level="guided",
        ),
        challenge(
            "py-op-precedence",
            "Precedence Prediction",
            "Add parentheses to make this expression evaluate to 20 — keep the numbers and operators in the same order: 2 + 3 * 4",
            "result = 2 + 3 * 4\nprint(result)\n",
            [
                ("result is 20", 'assert printed == ["20"], f"got {printed}"',
                 "(2 + 3) * 4 — parentheses beat multiplication."),
            ],
            level="prediction",
        ),
        challenge(
            "py-op-power",
            "Doubling Grains",
            "A chessboard legend: 1 grain on square 1, doubling each square. Print the grains on square 10 using the power operator.",
            "",
            [
                ("prints 512", 'assert printed == ["512"], f"got {printed}"',
                 "2 ** 9 — square 1 has 2**0 grains."),
            ],
            level="independent",
        ),
    ],
    {
        "py-op-divide": vi_challenge("Ba phép chia", "17 chiếc bánh chia cho 5 người bạn, in ba dòng: mỗi người được trọn vẹn bao nhiêu (chia nguyên), còn dư bao nhiêu (chia lấy dư), và phần chính xác mỗi người (chia thực).",
                                      [("in cả ba", "17 // 5, 17 % 5, và 17 / 5 — in từng cái.")]),
        "py-op-even": vi_challenge("Chẵn hay lẻ", "In True nếu số đã cho chẵn, False nếu lẻ. Một phép so sánh với modulo.",
                                    [("dùng modulo kiểm tra chẵn lẻ", "number % 2 == 0 cho kết quả True với số chẵn.")]),
        "py-op-precedence": vi_challenge("Dự đoán độ ưu tiên", "Thêm dấu ngoặc để biểu thức có giá trị 20 — giữ nguyên số và toán tử theo thứ tự: 2 + 3 * 4",
                                          [("kết quả là 20", "(2 + 3) * 4 — dấu ngoặc mạnh hơn phép nhân.")]),
        "py-op-power": vi_challenge("Hạt gấp đôi", "Truyền thuyết bàn cờ: 1 hạt ở ô 1, mỗi ô gấp đôi. In số hạt ở ô 10 bằng toán tử lũy thừa.",
                                     [("in 512", "2 ** 9 — ô 1 có 2**0 hạt.")]),
    },
    solutions=[
        ("py-op-divide", "cookies = 17\nfriends = 5\nprint(cookies // friends)\nprint(cookies % friends)\nprint(cookies / friends)",
         "cookies = 17\nfriends = 5\nprint(cookies // friends)\nprint(cookies % friends)\nprint(cookies // friends)"),
        ("py-op-even", "number = 8\nprint(number % 2 == 0)",
         "number = 8\nprint(number % 3 == 0)"),
        ("py-op-precedence", "result = (2 + 3) * 4\nprint(result)",
         "result = 2 + 3 * 4\nprint(result)"),
        ("py-op-power", "print(2 ** 9)",
         "print(2 * 9)"),
    ],
)

# ── Checkpoint: fundamentals ────────────────────────────────────────────────
CP_MDX = """
## Checkpoint: Python Fundamentals

Prove the Module 1–2 mental models at a problem level — combine variables,
conversion, arithmetic, and printing in one small program.

You will build a **receipt line**: given prices stored as text, compute a real
total and print a formatted line. This is exactly the shape of boring daily
programming: parse, compute, print.

When the checkpoint challenge passes, Module 2 is complete.
"""


CP_MDX_VI = """
## Checkpoint: Nền tảng Python

Chứng minh các mô hình tinh thần của Module 1–2 ở mức bài toán — kết hợp biến,
chuyển đổi kiểu, số học, và in dữ liệu trong một chương trình nhỏ.

Bạn sẽ xây dựng một **dòng hóa đơn**: với các giá tiền lưu dưới dạng văn bản, tính
tổng thật và in một dòng có định dạng. Đây chính xác là hình dạng của lập trình
hằng ngày: phân tích, tính toán, in kết quả.

Khi thử thách checkpoint đạt, Module 2 hoàn thành.
"""


write_checkpoint(
    MOD, "checkpoint-fundamentals",
    "Checkpoint: Python Fundamentals",
    "Variables, types, conversions, and operators — combined into one small program.",
    20, CP_MDX,
    "Checkpoint: Nền tảng Python",
    "Biến, kiểu, chuyển đổi, và toán tử — kết hợp trong một chương trình nhỏ.",
    CP_MDX_VI,
    challenge(
        "py-checkpoint-fundamentals",
        "Receipt Line",
        "price_a_text = \"4.5\" and price_b_text = \"6\" are given. Convert both to numbers, compute their sum, and print exactly: Sum: 10.5",
        'price_a_text = "4.5"\nprice_b_text = "6"\n',
        [
            ("prints formatted sum",
             'assert printed == ["Sum: 10.5"], f"got {printed}"',
             "float(price_a_text) + float(price_b_text), then print(\"Sum:\", total)."),
        ],
        difficulty="beginner",
    ),
    vi_challenge("Dòng hóa đơn", 'price_a_text = "4.5" và price_b_text = "6" đã cho. Chuyển cả hai sang số, tính tổng, và in chính xác: Sum: 10.5',
                 [("in tổng có định dạng", "float(price_a_text) + float(price_b_text), rồi print(\"Sum:\", total).")]),
    solution='price_a_text = "4.5"\nprice_b_text = "6"\ntotal = float(price_a_text) + float(price_b_text)\nprint("Sum:", total)',
    wrong='price_a_text = "4.5"\nprice_b_text = "6"\nprint("Sum:", price_a_text + price_b_text)',
)

print("module 2 content written")
