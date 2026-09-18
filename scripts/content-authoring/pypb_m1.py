#!/usr/bin/env python3
"""Module 1: python-and-your-first-programs — lessons + practices."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "python-and-your-first-programs"

# ── Lesson 1: what-python-is ────────────────────────────────────────────────
write_lesson(
    MOD, "what-python-is",
    "What Python Is",
    "Meet the language, what it is good at, and how this course works.",
    8,
    """
Python is a programming language — a precise set of rules for writing instructions
that a computer can follow. It is one of the most popular languages in the world
because it reads almost like English and it is genuinely useful from day one:
small scripts, web backends, automation, data work, and AI tooling are all built
with it.

## What Python is good at

- **Automating boring things** — renaming a thousand files, sending a report, scraping a page.
- **Building the "back end"** — the server side of websites and apps.
- **Working with data** — reading files, counting things, crunching numbers.
- **Learning to think like a programmer** — Python hides the noise so you can focus on ideas.

## How a computer runs Python

Your computer does not understand Python directly. A program called the
**interpreter** reads your code line by line and performs the instructions.
That is the whole loop of this course:

```
you write code  →  the interpreter reads it  →  the computer does it
```

This course has two kinds of pages, and you should treat them differently:

- **Learn** pages (this one) build your mental model. Read them actively.
- **Practice** pages are where you actually type code. Every practice set is
  verified: you run your code, and tests check it. You cannot read your way
  through this course — and that is the point.

> Rule of thumb from every experienced developer: **you learn programming with
> your fingers, not your eyes.**
""",
    "Python là gì",
    "Gặp gỡ ngôn ngữ Python, những điểm mạnh của nó, và cách khóa học vận hành.",
    """
Python là một ngôn ngữ lập trình — một bộ quy tắc chặt chẽ để viết các chỉ thị
mà máy tính có thể thực hiện. Đây là một trong những ngôn ngữ phổ biến nhất thế
giới vì nó đọc gần như tiếng Anh và thực sự hữu ích ngay từ ngày đầu: các đoạn
script nhỏ, backend cho website, tự động hóa, xử lý dữ liệu và công cụ AI đều
được xây dựng bằng Python.

## Python giỏi những gì

- **Tự động hóa việc nhàm chán** — đổi tên hàng nghìn tệp, gửi báo cáo, lấy dữ liệu trang web.
- **Xây dựng "phần backend"** — phía máy chủ của website và ứng dụng.
- **Làm việc với dữ liệu** — đọc tệp, đếm, tính toán.
- **Học cách suy nghĩ như lập trình viên** — Python che bớt nhiễu để bạn tập trung vào ý tưởng.

## Máy tính chạy Python thế nào

Máy tính không hiểu trực tiếp Python. Một chương trình gọi là **trình thông dịch**
(interpreter) sẽ đọc từng dòng mã và thực hiện các chỉ thị. Đó là toàn bộ vòng lặp
của khóa học này:

```
bạn viết code  →  trình thông dịch đọc  →  máy tính thực hiện
```

Khóa học có hai loại trang, và bạn nên đối xử với chúng khác nhau:

- **Learn** (bài học như trang này) xây dựng nền tảng tư duy. Đọc một cách chủ động.
- **Practice** là nơi bạn thực sự gõ code. Mỗi bài thực hành đều được chấm tự động:
  bạn chạy code của mình, và các bài kiểm tra sẽ chấm. Bạn không thể học xong khóa
  này chỉ bằng cách đọc — và đó chính là chủ đích.

> Quy tắc từ mọi lập trình viên giàu kinh nghiệm: **bạn học lập trình bằng đôi tay,
> không phải bằng đôi mắt.**
""",
)

# ── Lesson 2: running-python ────────────────────────────────────────────────
write_lesson(
    MOD, "running-python",
    "Running Python",
    "Three ways to run Python code — and when to use each.",
    10,
    """
There are three everyday ways to run Python. You will use all three.

## 1. The REPL — instant experiments

Open a terminal and type `python3` (Windows often accepts `python`). You will see
the `>>>` prompt: the **REPL** (Read–Evaluate–Print–Loop). You type one expression;
Python immediately evaluates it and shows the result:

```
>>> 2 + 3
5
>>> "py" * 3
'pypypy'
```

The REPL is a calculator on steroids and your first debugging tool — use it to test
a tiny idea before putting it in a program.

## 2. Script files — real programs

Save your instructions in a file ending in `.py`, then run the whole file:

```
python3 hello.py
```

Scripts run from top to bottom. Files are how real programs live; every challenge
in this course is one file you write and run.

## 3. From inside other programs

Python also runs *inside* this course's code editor. When you press **Run** here,
your code is executed in a sandbox and the tests are checked. Same idea, safer place.

> The editor in this course grades functions, return values, and printed output —
> challenges never need you to type input while they run. You will build interactive
> programs locally and test them in your own terminal.
""",
    "Chạy Python",
    "Ba cách chạy mã Python — và khi nào dùng cách nào.",
    """
Có ba cách thường dùng để chạy Python. Bạn sẽ dùng cả ba.

## 1. REPL — thử nghiệm tức thì

Mở terminal và gõ `python3` (trên Windows thường gõ `python`). Bạn sẽ thấy dấu nhắc
`>>>`: đó là **REPL** (Read–Evaluate–Print–Loop). Bạn gõ một biểu thức; Python đánh
giá ngay lập tức và hiển thị kết quả:

```
>>> 2 + 3
5
>>> "py" * 3
'pypypy'
```

REPL là một chiếc máy tính siêu phàm và là công cụ gỡ lỗi đầu tiên của bạn — dùng nó
để thử một ý tưởng nhỏ trước khi đưa vào chương trình.

## 2. Tệp script — chương trình thật

Lưu các chỉ thị vào một tệp có đuôi `.py`, rồi chạy cả tệp:

```
python3 hello.py
```

Script chạy từ trên xuống dưới. Tệp là nơi chương trình thật sự tồn tại; mọi thử thách
trong khóa học này là một tệp bạn viết và chạy.

## 3. Chạy bên trong chương trình khác

Python cũng chạy *bên trong* trình soạn thảo của khóa học. Khi bạn bấm **Run**, mã của
bạn được thực thi trong một sandbox và các bài kiểm tra được chấm. Cùng một ý tưởng,
nơi an toàn hơn.

> Trình soạn thảo ở đây chấm hàm, giá trị trả về, và kết quả in ra — thử thách không
> bao giờ yêu cầu bạn nhập dữ liệu trong khi chạy. Bạn sẽ xây dựng các chương trình
> tương tác cục bộ và thử chúng trong terminal của riêng mình.
""",
)

# ── Lesson 3: first-programs ────────────────────────────────────────────────
write_lesson(
    MOD, "first-programs",
    "Your First Programs",
    "print, comments, and the shape of a program.",
    10,
    """
The smallest useful instruction in Python prints text on the screen:

```python
print("Hello, world!")
```

`print` is a **function**: a named action you can invoke. The parentheses hold the
**arguments** — here, the text to show. Text inside quotes is a **string**;
numbers work too, and print can show several things at once:

```python
print(42)
print("Age:", 42)
```

## Comments — notes to humans

Anything after `#` on a line is ignored by the interpreter. Comments explain *why*:

```python
# convert minutes to seconds
seconds = minutes * 60
```

## Programs run top to bottom

```python
print("first")
print("second")
print("third")
```

Always prints in that order. That simple fact is your first mental model of
program flow: **execution is a sequence.**

## Try it now

In the practice set that follows this lesson you will print formatted output,
do small calculations, and predict what broken programs print. Reading is fine;
**now you type.**
""",
    "Chương trình đầu tiên",
    "print, chú thích, và hình hài của một chương trình.",
    """
Chỉ thị nhỏ nhất nhưng hữu ích nhất trong Python là in văn bản ra màn hình:

```python
print("Hello, world!")
```

`print` là một **hàm** (function): một hành động được đặt tên mà bạn có thể gọi. Dấu
ngoặc đơn chứa các **đối số** (arguments) — ở đây là văn bản cần hiển thị. Văn bản trong
dấu ngoặc kép là một **chuỗi** (string); số cũng được, và print có thể hiển thị nhiều thứ
cùng lúc:

```python
print(42)
print("Age:", 42)
```

## Chú thích — ghi chú cho người

Mọi thứ sau `#` trên một dòng đều bị trình thông dịch bỏ qua. Chú thích giải thích *tại sao*:

```python
# chuyển phút thành giây
seconds = minutes * 60
```

## Chương trình chạy từ trên xuống

```python
print("first")
print("second")
print("third")
```

Luôn in theo đúng thứ tự đó. Sự thật đơn giản này là mô hình tinh thần đầu tiên của bạn
về luồng chương trình: **thực thi là một chuỗi tuần tự.**

## Thử ngay bây giờ

Trong bộ bài tập theo sau bài học này, bạn sẽ in kết quả có định dạng, thực hiện vài phép
tính nhỏ, và dự đoán chương trình bị lỗi in ra gì. Đọc thì tốt; **bây giờ bạn hãy gõ.**
""",
)

# ── Lesson 4: reading-errors ────────────────────────────────────────────────
write_lesson(
    MOD, "reading-errors",
    "Errors Are Instructions",
    "Meet your first error messages and learn the habit every developer has.",
    8,
    """
You WILL make mistakes — every professional does, constantly. The difference between
frustration and progress is treating errors as instructions, not insults.

## A first syntax error

```python
print("Hello)
```

Python refuses to run this and prints something like:

```
SyntaxError: unterminated string literal (detected at line 1)
```

Read it slowly. It tells you: **what** went wrong (an unterminated string — a quote
never closed) and **where** (line 1). Most error messages are exactly this: a diagnosis
and a location.

## A first runtime error

```python
print(5 / 0)
```

Syntax is fine; the failure happens *while running*:

```
ZeroDivisionError: division by zero
```

The error's name (`ZeroDivisionError`) is a category you will learn to recognize.
The message is the specific reason.

## The habit that changes everything

When code fails:

1. **Read the last line first** — error type and message.
2. **Look at the line number** it points to (the real bug is often just above it).
3. **Fix one thing, run again.** Small steps.

From this lesson on, when a practice challenge fails, the console shows you real
error output. That output is not the platform being mean — it is exactly what your
own terminal will show you. Learn to like it.
""",
    "Lỗi là chỉ dẫn",
    "Gặp gỡ những thông báo lỗi đầu tiên và hình thành thói quen của mọi lập trình viên.",
    """
Bạn SẼ mắc lỗi — mọi lập trình viên chuyên nghiệp đều vậy, liên tục. Sự khác biệt giữa
thất vọng và tiến bộ là coi lỗi như chỉ dẫn, không phải như lời sỉ nhăng.

## Một lỗi cú pháp đầu tiên

```python
print("Hello)
```

Python từ chối chạy và in ra đại loại như:

```
SyntaxError: unterminated string literal (detected at line 1)
```

Đọc chậm lại. Nó cho bạn biết: **cái gì** sai (chuỗi không đóng — dấu ngoặc kép chưa
được kết thúc) và **ở đâu** (dòng 1). Đa số thông báo lỗi đều như vậy: một chẩn đoán
và một vị trí.

## Một lỗi khi chạy (runtime error)

```python
print(5 / 0)
```

Cú pháp ổn; lỗi xảy ra *khi đang chạy*:

```
ZeroDivisionError: division by zero
```

Tên lỗi (`ZeroDivisionError`) là một loại bạn sẽ dần nhận diện được. Thông điệp là lý
do cụ thể.

## Thói quen thay đổi tất cả

Khi code thất bại:

1. **Đọc dòng cuối cùng trước** — loại lỗi và thông điệp.
2. **Nhìn số dòng** nó chỉ tới (bug thật thường nằm ngay phía trên).
3. **Sửa một thứ, chạy lại.** Bước nhỏ một chút.

Từ bài học này, khi một thử thách thực hành thất bại, console sẽ hiện lỗi thật. Đó
không phải là nền tảng đang ác ý — đó chính xác là điều terminal của bạn sẽ hiện. Hãy
học cách quý nó.
""",
)

# ── Practices ───────────────────────────────────────────────────────────────
write_practice(
    MOD, "m1-print-practice",
    "Printing Basics",
    "First contact: print text and numbers exactly as asked.",
    "Thực hành in dữ liệu",
    "Tiếp xúc đầu tiên: in văn bản và số đúng như yêu cầu.",
    "first-programs", 25, "beginner",
    [
        challenge(
            "py-print-hello",
            "Say Hello",
            "Print exactly: Hello, Code Journey!",
            'print("")',
            [("prints greeting", 'assert printed == ["Hello, Code Journey!"], f"expected [\'Hello, Code Journey!\'], got {printed}"',
              "Use print with the exact text in quotes.")],
            level="imitation",
        ),
        challenge(
            "py-print-two-lines",
            "Two Lines",
            "Print two lines: first line Learning, second line Python.",
            'print("")',
            [("prints two lines", 'assert printed == ["Learning", "Python"], f"got {printed}"',
              "Call print twice — each call ends with a newline.")],
            level="imitation",
        ),
        challenge(
            "py-print-combined",
            "Text and Number Together",
            'Print: Count: 7 — one print call, the number as a number.',
            "",
            [("one print call with both",
              'assert printed == ["Count: 7"], f"got {printed}"\nassert code.count(",") >= 1, "pass 7 as a number argument"',
              'print("Count:", 7) - print joins arguments with spaces.')],
            level="guided",
        ),
    ],
    {
        "py-print-hello": vi_challenge("In lời chào", "In chính xác: Hello, Code Journey!",
                                        [("in lời chào", "Dùng print với văn bản chính xác trong dấu ngoặc kép.")]),
        "py-print-two-lines": vi_challenge("Hai dòng", "In hai dòng: dòng đầu Learning, dòng hai Python.",
                                            [("in hai dòng", "Gọi print hai lần — mỗi lần gọi kết thúc bằng một dòng mới.")]),
        "py-print-combined": vi_challenge("Văn bản và số cùng nhau", "In: Count: 7 — một lần gọi print, số ở dạng số.",
                                           [("một lần gọi print gồm cả hai", 'print("Count:", 7) — print nối các đối số bằng dấu cách.')]),
    },
    solutions=[
        ("py-print-hello", 'print("Hello, Code Journey!")', 'print("hello")'),
        ("py-print-two-lines", 'print("Learning")\nprint("Python")', 'print("Learning Python")'),
        ("py-print-combined", 'print("Count:", 7)', 'print("Count: 7")'),
    ],
)

write_practice(
    MOD, "m1-errors-practice",
    "Fix the Broken Programs",
    "Each snippet fails. Read the error, repair the line, run again.",
    "Sửa các chương trình bị lỗi",
    "Mỗi đoạn mã đều lỗi. Đọc lỗi, sửa dòng lỗi, chạy lại.",
    "reading-errors", 30, "beginner",
    [
        challenge(
            "py-fix-quote",
            "Fix the Quote",
            'This program should print Python rocks! but crashes. Fix it.',
            'print("Python rocks!)',
            [("prints after fix", 'assert printed == ["Python rocks!"], f"got {printed}"',
              "The closing quote is missing.")],
            level="debugging",
        ),
        challenge(
            "py-fix-print-case",
            "Fix the Missing P",
            "rint should be a function call — this code has a broken name. Fix it so it prints 99.",
            "Print(99)",
            [("prints 99", 'assert printed == ["99"], f"got {printed}"',
              "Python is case-sensitive: print, not Print.")],
            level="debugging",
        ),
        challenge(
            "py-predict-order",
            "Predict the Order",
            "Without running: three prints are about to execute. The tests check the exact order of output lines. Print first, second, third in that order using three calls.",
            'print("third")\nprint("first")\nprint("second")',
            [("correct order", 'assert printed == ["first", "second", "third"], f"got {printed}"',
              "Execution is top to bottom — reorder the calls.")],
            level="prediction",
        ),
    ],
    {
        "py-fix-quote": vi_challenge("Sửa dấu ngoặc kép", "Chương trình này lẽ ra in Python rocks! nhưng lại lỗi. Hãy sửa.",
                                      [("in ra sau khi sửa", "Dấu ngoặc kép đóng bị thiếu.")]),
        "py-fix-print-case": vi_challenge("Sửa chữ P bị thiếu", "print là một lời gọi hàm — mã này viết sai tên hàm. Sửa để in 99.",
                                           [("in 99", "Python phân biệt chữ hoa/thường: print, không phải Print.")]),
        "py-predict-order": vi_challenge("Dự đoán thứ tự", "Không cần chạy: ba lệnh print sắp thực thi. Bài kiểm tra kiểm tra đúng thứ tự các dòng. In first, second, third theo đúng thứ tự bằng ba lệnh gọi.",
                                          [("thứ tự đúng", "Thực thi chạy từ trên xuống — hãy đổi thứ tự các lệnh gọi.")]),
    },
    solutions=[
        ("py-fix-quote", 'print("Python rocks!")', 'print("Python rocks)'),
        ("py-fix-print-case", "print(99)", "Print(99)"),
        ("py-predict-order", 'print("first")\nprint("second")\nprint("third")', 'print("third")\nprint("first")'),
    ],
)

print("module 1 content written")
