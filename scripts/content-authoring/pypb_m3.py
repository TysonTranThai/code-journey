#!/usr/bin/env python3
"""Module 3: working-with-strings — lessons + practices. Direct triple-quote MDX."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "working-with-strings"

L1 = """
A string is a sequence of characters. Each position has an **index** — and Python
counts from **zero**:

```python
word = "Python"
word[0]    # 'P'  (first!)
word[5]    # 'n'  (last)
word[6]    # IndexError — only 0..5 exist
```

Negative indices count from the end: `word[-1]` is `'n'`, `word[-2]` is `'o'`.

## Length

`len()` counts characters: `len("Python")` is `6`.

## Strings are immutable

You cannot change a character in place: `word[0] = "J"` raises `TypeError`.
Instead, build a **new** string — the next lesson shows slicing, and methods
give you more tools.
"""

L1_VI = """
Chuỗi (string) là một dãy các ký tự. Mỗi vị trí có một **chỉ số** (index) — và
Python đếm bắt đầu từ **số 0**:

```python
word = "Python"
word[0]    # 'P'  (đầu tiên!)
word[5]    # 'n'  (cuối cùng)
word[6]    # IndexError — chỉ có 0..5
```

Chỉ số âm đếm từ cuối: `word[-1]` là `'n'`, `word[-2]` là `'o'`.

## Độ dài

`len()` đếm số ký tự: `len("Python")` là `6`.

## Chuỗi là bất biến (immutable)

Bạn không thể thay đổi một ký tự tại chỗ: `word[0] = "J"` gây `TypeError`.
Thay vào đó, hãy tạo một chuỗi **mới** — bài sau giới thiệu slicing, và các
phương thức sẽ cho bạn nhiều công cụ hơn.
"""

L2 = """
**Slicing** takes a piece of a string: `name[start:stop]` — characters from
`start` up to but **not including** `stop`:

```python
word = "Python"
word[0:2]    # 'Py'
word[2:6]    # 'thon'
word[:3]     # 'Pyt'  (start defaults to 0)
word[3:]     # 'hon'  (stop defaults to end)
word[-3:]    # 'hon'  (negatives work too)
```

The half-open rule `[start:stop)` is the single most reused convention in
Python — memorize it once, use it everywhere.

## Step

An optional third number skips characters: `word[::2]` is `'Pto'` (every second
character). A step of `-1` reverses: `word[::-1]` is `'nohtyP'`.
"""

L2_VI = """
**Slicing** lấy một phần của chuỗi: `name[start:stop]` — các ký tự từ `start`
đến nhưng **không bao gồm** `stop`:

```python
word = "Python"
word[0:2]    # 'Py'
word[2:6]    # 'thon'
word[:3]     # 'Pyt'  (start mặc định là 0)
word[3:]     # 'hon'  (stop mặc định là cuối)
word[-3:]    # 'hon'  (chỉ số âm cũng được)
```

Quy tắc nửa mở `[start:stop)` là quy ước được dùng lại nhiều nhất trong Python —
học một lần, dùng ở khắp nơi.

## Bước nhảy

Số thứ ba tùy chọn nhảy cóc qua các ký tự: `word[::2]` là `'Pto'` (mỗi ký tự thứ hai).
Bước `-1` đảo ngược chuỗi: `word[::-1]` là `'nohtyP'`.
"""

L3 = """
Methods are functions attached to values — call them with a dot. The everyday
string toolkit:

```python
s = "  Hello, Python  "

s.strip()          # remove surrounding spaces
s.upper()          # '  HELLO, PYTHON  '
s.lower()
s.replace("l", "L")
s.count("l")       # count occurrences
s.find("Py")       # index of first match, or -1
"py".upper()
```

Methods **return new strings** — they never change the original (immutability):

```python
name = "minh"
name.upper()       # 'MINH' — but name is still 'minh'!
name = name.upper()   # re-assign to keep the result
```

## Splitting and joining

The workhorse pair for text data:

```python
"do-re-mi".split("-")     # ['do', 're', 'mi']
"-".join(["a", "b"])      # 'a-b'
"line1,line2".split(",")  # ['line1', 'line2']
```

`split()` with no argument splits on any whitespace — perfect for sentences.
"""

L3_VI = """
Phương thức (method) là hàm gắn liền với giá trị — gọi bằng dấu chấm. Bộ công cụ
chuỗi hằng ngày:

```python
s = "  Hello, Python  "

s.strip()          # bỏ khoảng trắng hai đầu
s.upper()          # '  HELLO, PYTHON  '
s.lower()
s.replace("l", "L")
s.count("l")       # đếm số lần xuất hiện
s.find("Py")       # vị trí khớp đầu tiên, hoặc -1
"py".upper()
```

Phương thức **trả về chuỗi mới** — không bao giờ đổi chuỗi gốc (bất biến):

```python
name = "minh"
name.upper()          # 'MINH' — nhưng name vẫn là 'minh'!
name = name.upper()   # gán lại để giữ kết quả
```

## Tách và nối

Cặp công cụ chủ lực cho dữ liệu văn bản:

```python
"do-re-mi".split("-")     # ['do', 're', 'mi']
"-".join(["a", "b"])      # 'a-b'
"line1,line2".split(",")  # ['line1', 'line2']
```

`split()` không đối số tách theo mọi khoảng trắng — hoàn hảo cho câu chữ.
"""

L4 = """
**f-strings** embed values inside text — the modern standard for output:

```python
name = "Minh"
age = 21
print(f"{name} is {age}")     # Minh is 21
print(f"Next year: {age + 1}")  # expressions allowed!
```

The `f` prefix turns the string into a template: anything inside `{}` is
evaluated. This one feature replaces a whole zoo of older formatting tricks.

## Formatting numbers

Add a format spec after `:`:

```python
price = 7.5
print(f"{price:.2f}")     # 7.50  (2 decimals)
ratio = 0.876
print(f"{ratio:.0%}")     # 88%
n = 1234567
print(f"{n:,}")           # 1,234,567
```

## Escapes and multiline

`\\n` is a newline, `\\t` a tab, `\\\\` a literal backslash. For text with both
quote styles or many lines, use triple quotes:

```python
menu = '''1. Start
2. Settings
3. Quit'''
```
"""

L4_VI = """
**f-string** nhúng giá trị vào trong văn bản — chuẩn hiện đại cho đầu ra:

```python
name = "Minh"
age = 21
print(f"{name} is {age}")     # Minh is 21
print(f"Next year: {age + 1}")  # cho phép biểu thức!
```

Tiền tố `f` biến chuỗi thành một khuôn mẫu: mọi thứ trong `{}` đều được đánh giá.
Một tính năng này thay thế cả một "vườn thú" mẹo định dạng cũ.

## Định dạng số

Thêm đặc tả định dạng sau dấu `:`:

```python
price = 7.5
print(f"{price:.2f}")     # 7.50  (2 chữ số thập phân)
ratio = 0.876
print(f"{ratio:.0%}")     # 88%
n = 1234567
print(f"{n:,}")           # 1,234,567
```

## Ký tự escape và chuỗi nhiều dòng

`\\n` là xuống dòng, `\\t` là tab, `\\\\` là dấu gạch chéo thật. Với văn bản chứa cả
hai kiểu ngoặc hoặc nhiều dòng, dùng ba dấu ngoặc kép:

```python
menu = '''1. Start
2. Settings
3. Quit'''
```
"""

write_lesson(MOD, "string-basics-indexing", "Strings: Indexing & Length",
             "Characters by position, zero-based indexing, and immutability.", 10,
             L1, "Chuỗi: Indexing & Độ dài", "Ký tự theo vị trí, chỉ số từ số 0, và tính bất biến.", L1_VI)

write_lesson(MOD, "slicing", "Slicing",
             "Extract pieces of text with [start:stop] — and the half-open rule.", 10,
             L2, "Slicing", "Trích phần văn bản với [start:stop] — và quy tắc nửa mở.", L2_VI)

write_lesson(MOD, "string-methods", "String Methods",
             "strip, upper, replace, split, join — the everyday text toolkit.", 12,
             L3, "Phương thức chuỗi", "strip, upper, replace, split, join — bộ công cụ văn bản hằng ngày.", L3_VI)

write_lesson(MOD, "f-strings-formatting", "f-strings & Formatting",
             "Embed values in text, format numbers, escapes, and multiline strings.", 12,
             L4, "f-string & Định dạng", "Nhúng giá trị vào văn bản, định dạng số, escape, và chuỗi nhiều dòng.", L4_VI)

# ── Practices ───────────────────────────────────────────────────────────────
write_practice(
    MOD, "m3-indexing-practice",
    "Indexing & Slicing Drills",
    "Pull exact characters and pieces out of text.",
    "Bài tập indexing & slicing",
    "Trích ký tự và phần văn bản chính xác.",
    "string-basics-indexing", 25, "beginner",
    [
        challenge(
            "py-str-first-last",
            "First and Last",
            'word = "Python" is given. Print its first character and its last character on two lines.',
            'word = "Python"\n',
            [("prints P then n", 'assert printed == ["P", "n"], f"got {printed}"',
              "word[0] and word[-1].")],
            level="imitation",
        ),
        challenge(
            "py-str-slice-domain",
            "Extract the Domain",
            'email = "minh@example.com" is given. Print only the domain: example.com',
            'email = "minh@example.com"\n',
            [("prints domain", 'assert printed == ["example.com"], f"got {printed}"',
              'Find the @ with email.find("@"), then slice from there + 1.')],
            level="guided",
        ),
        challenge(
            "py-str-reverse",
            "Reverse It",
            'Print the word "stressed" reversed — slicing can do it in one expression.',
            "",
            [("prints reversed", 'assert printed == ["desserts"], f"got {printed}"',
              's[::-1] reverses a string.')],
            level="guided",
        ),
    ],
    {
        "py-str-first-last": vi_challenge("Ký tự đầu và cuối", 'word = "Python" đã cho. In ký tự đầu tiên và ký tự cuối cùng trên hai dòng.',
                                           [("in P rồi n", "word[0] và word[-1].")]),
        "py-str-slice-domain": vi_challenge("Trích tên miền", 'email = "minh@example.com" đã cho. Chỉ in phần tên miền: example.com',
                                              [("in tên miền", 'Tìm @ bằng email.find("@"), rồi slice từ đó + 1.')]),
        "py-str-reverse": vi_challenge("Đảo ngược", 'In từ "stressed" theo chiều ngược — slicing làm được trong một biểu thức.',
                                        [("in chuỗi đảo", "s[::-1] đảo ngược một chuỗi.")]),
    },
    solutions=[
        ("py-str-first-last", 'word = "Python"\nprint(word[0])\nprint(word[-1])',
         'word = "Python"\nprint(word[1])\nprint(word[-1])'),
        ("py-str-slice-domain", 'email = "minh@example.com"\nprint(email[email.find("@") + 1:])',
         'email = "minh@example.com"\nprint(email[email.find("@"):])'),
        ("py-str-reverse", 'print("stressed"[::-1])',
         'print("stressed"[::1])'),
    ],
)

write_practice(
    MOD, "m3-methods-practice",
    "Method Drills",
    "Transform text with the everyday toolkit.",
    "Bài tập phương thức",
    "Biến đổi văn bản với bộ công cụ hằng ngày.",
    "string-methods", 30, "beginner",
    [
        challenge(
            "py-str-username",
            "Username Generator",
            'first = "Bao" and last = "Nguyen" are given. Build the username: lowercase first name, a dot, lowercase last name (bao.nguyen). Print it.',
            'first = "Bao"\nlast = "Nguyen"\n',
            [("prints username", 'assert printed == ["bao.nguyen"], f"got {printed}"',
              "Lowercase both, then join with + or f-string.")],
            level="guided",
        ),
        challenge(
            "py-str-clean",
            "Clean the Input",
            'raw = "   Hello World   " is given. Print it with surrounding spaces removed and all lowercase.',
            'raw = "   Hello World   "\n',
            [("prints cleaned", 'assert printed == ["hello world"], f"got {printed}"',
              "Chain methods: raw.strip().lower()")],
            level="imitation",
        ),
        challenge(
            "py-str-vowels",
            "Count the Vowels",
            'sentence = "Practice makes Python" is given. Print how many vowels (a, e, i, o, u — lowercase only) it contains.',
            'sentence = "Practice makes Python"\n',
            [("prints vowel count", 'assert printed == ["6"], f"got {printed}"',
              "Loop is coming later — for now count each vowel with .count().")],
            level="independent",
        ),
        challenge(
            "py-str-split-join",
            "CSV Line Flip",
            'line = "apple,banana,cherry" is given. Print the items joined with " | " instead of commas.',
            'line = "apple,banana,cherry"\n',
            [("prints joined", 'assert printed == ["apple | banana | cherry"], f"got {printed}"',
              'line.split(",") then " | ".join(...).')],
            level="guided",
        ),
    ],
    {
        "py-str-username": vi_challenge("Tạo tên người dùng", 'first = "Bao" và last = "Nguyen" đã cho. Tạo username: tên viết thường, dấu chấm, họ viết thường (bao.nguyen). In ra.',
                                          [("in username", "Viết thường cả hai, rồi nối bằng + hoặc f-string.")]),
        "py-str-clean": vi_challenge("Làm sạch dữ liệu vào", 'raw = "   Hello World   " đã cho. In nó sau khi bỏ khoảng trắng hai đầu và viết thường toàn bộ.',
                                       [("in đã làm sạch", "Gắn chuỗi phương thức: raw.strip().lower()")]),
        "py-str-vowels": vi_challenge("Đếm nguyên âm", 'sentence = "Practice makes Python" đã cho. In số nguyên âm (a, e, i, o, u — chỉ chữ thường) trong câu.',
                                        [("in số nguyên âm", "Vòng lặp sẽ học sau — tạm thời đếm từng nguyên âm bằng .count().")]),
        "py-str-split-join": vi_challenge("Lật dòng CSV", 'line = "apple,banana,cherry" đã cho. In các mục nối bằng " | " thay vì dấu phẩy.',
                                            [("in chuỗi đã nối", 'line.split(",") rồi " | ".join(...).')]),
    },
    solutions=[
        ("py-str-username", 'first = "Bao"\nlast = "Nguyen"\nprint(first.lower() + "." + last.lower())',
         'first = "Bao"\nlast = "Nguyen"\nprint(first + "." + last)'),
        ("py-str-clean", 'raw = "   Hello World   "\nprint(raw.strip().lower())',
         'raw = "   Hello World   "\nprint(raw.lower())'),
        ("py-str-vowels", 'sentence = "Practice makes Python"\ncount = 0\ncount += sentence.count("a")\ncount += sentence.count("e")\ncount += sentence.count("i")\ncount += sentence.count("o")\ncount += sentence.count("u")\nprint(count)',
         'sentence = "Practice makes Python"\nprint(sentence.count("z"))'),
        ("py-str-split-join", 'line = "apple,banana,cherry"\nprint(" | ".join(line.split(",")))',
         'line = "apple,banana,cherry"\nprint(" | ".join(line))'),
    ],
)

write_practice(
    MOD, "m3-fstring-practice",
    "Formatting Drills",
    "Produce polished output with f-strings.",
    "Bài tập định dạng",
    "Tạo đầu ra chỉn chu với f-string.",
    "f-strings-formatting", 25, "beginner",
    [
        challenge(
            "py-fstr-receipt",
            "Formatted Receipt",
            'item = "coffee" and price = 2.5 are given. Print exactly: coffee costs $2.50 — use an f-string with 2 decimals.',
            'item = "coffee"\nprice = 2.5\n',
            [("prints formatted", 'assert printed == ["coffee costs $2.50"], f"got {printed}"',
              'f"{item} costs ${price:.2f}"')],
            level="guided",
        ),
        challenge(
            "py-fstr-table",
            "Aligned Column",
            'The list of names ["Ana", "Bruno", "Chi"] is given as three variables. Print each right-aligned in a 6-character column (three lines) using f-string alignment.',
            'a = "Ana"\nb = "Bruno"\nc = "Chi"\n',
            [("right aligned", 'assert printed == ["   Ana", " Bruno", "   Chi"], f"got {printed}"',
              'f"{a:>6}" right-aligns in width 6.')],
            level="guided",
        ),
        challenge(
            "py-fstr-multiline",
            "Menu Card",
            "Print a three-line menu exactly: 1. Start / 2. Settings / 3. Quit — one print call, using \\n escapes or a triple-quoted string.",
            "",
            [("prints menu in one call", 'assert printed == ["1. Start", "2. Settings", "3. Quit"], f"got {printed}"\nassert code.count("print(") == 1, "use exactly ONE print call"',
              'print("1. Start\\n2. Settings\\n3. Quit")')],
            level="independent",
        ),
    ],
    {
        "py-fstr-receipt": vi_challenge("Hóa đơn có định dạng", 'item = "coffee" và price = 2.5 đã cho. In chính xác: coffee costs $2.50 — dùng f-string với 2 chữ số thập phân.',
                                          [("in có định dạng", 'f"{item} costs ${price:.2f}"')]),
        "py-fstr-table": vi_challenge("Cột căn đều", 'Danh sách tên ["Ana", "Bruno", "Chi"] được cho thành ba biến. In từng tên căn phải trong cột 6 ký tự (ba dòng) bằng căn lề f-string.',
                                        [("căn phải", 'f"{a:>6}" căn phải trong bề rộng 6.')]),
        "py-fstr-multiline": vi_challenge("Thực đơn", "In thực đơn ba dòng chính xác: 1. Start / 2. Settings / 3. Quit — một lần gọi print, dùng ký tự \\n hoặc chuỗi ba dấu ngoặc kép.",
                                            [("in thực đơn", 'print("1. Start\\n2. Settings\\n3. Quit")')]),
    },
    solutions=[
        ("py-fstr-receipt", 'item = "coffee"\nprice = 2.5\nprint(f"{item} costs ${price:.2f}")',
         'item = "coffee"\nprice = 2.5\nprint(f"{item} costs ${price}")'),
        ("py-fstr-table", 'a = "Ana"\nb = "Bruno"\nc = "Chi"\nprint(f"{a:>6}")\nprint(f"{b:>6}")\nprint(f"{c:>6}")',
         'a = "Ana"\nb = "Bruno"\nc = "Chi"\nprint(f"{a}")\nprint(f"{b}")\nprint(f"{c}")'),
        ("py-fstr-multiline", 'print("1. Start\\n2. Settings\\n3. Quit")',
         'print("1. Start")\nprint("2. Settings")\nprint("3. Quit")'),
    ],
)

write_practice(
    MOD, "m3-mini-build-formatter",
    "Mini Build: Text Formatter",
    "Combine slicing, methods, and f-strings into a small text tool.",
    "Mini build: Trình định dạng văn bản",
    "Kết hợp slicing, phương thức, và f-string thành một công cụ văn bản nhỏ.",
    "f-strings-formatting", 35, "beginner",
    [
        challenge(
            "py-fmt-titlecase-name",
            "Name Formatter",
            'full_name = "nguyen van anh" is given (three words). Produce the display form "Nguyen Van Anh" — each word capitalized — and print it.',
            'full_name = "nguyen van anh"\n',
            [("prints display name", 'assert printed == ["Nguyen Van Anh"], f"got {printed}"',
              ".title() capitalizes each word — or split, capitalize, join.")],
            level="independent",
        ),
        challenge(
            "py-fmt-initials",
            "Initials",
            'full_name = "nguyen van anh" is given. Print the initials with dots: N.V.A',
            'full_name = "nguyen van anh"\n',
            [("prints initials", 'assert printed == ["N.V.A"], f"got {printed}"',
              "Split into words, take [0] of each, upper(), join with dots.")],
            level="mini-build",
        ),
        challenge(
            "py-fmt-slug",
            "URL Slug Maker",
            'title = "  Learn Python FAST! " is given. Convert it to a slug: trim, lowercase, spaces to dashes: learn-python-fast-',
            'title = "  Learn Python FAST! "\n',
            [("prints slug", 'assert printed == ["learn-python-fast!"], f"got {printed}"',
              "title.strip().lower().replace(\" \", \"-\") — punctuation stays for now.")],
            level="mini-build",
        ),
    ],
    {
        "py-fmt-titlecase-name": vi_challenge("Định dạng tên", 'full_name = "nguyen van anh" đã cho (ba từ). Tạo dạng hiển thị "Nguyen Van Anh" — mỗi từ viết hoa chữ đầu — và in ra.',
                                                [("in tên hiển thị", ".title() viết hoa từng từ — hoặc split, capitalize, join.")]),
        "py-fmt-initials": vi_challenge("Viết tắt", 'full_name = "nguyen van anh" đã cho. In các chữ cái đầu kèm dấu chấm: N.V.A',
                                          [("in viết tắt", "Tách thành từ, lấy [0] của mỗi từ, upper(), nối bằng dấu chấm.")]),
        "py-fmt-slug": vi_challenge("Tạo slug URL", 'title = "  Learn Python FAST! " đã cho. Chuyển thành slug: cắt khoảng trắng, viết thường, khoảng trắng thành gạch ngang: learn-python-fast-',
                                      [("in slug", 'title.strip().lower().replace(" ", "-") — tạm thời giữ dấu câu.')]),
    },
    solutions=[
        ("py-fmt-titlecase-name", 'full_name = "nguyen van anh"\nprint(full_name.title())',
         'full_name = "nguyen van anh"\nprint(full_name)'),
        ("py-fmt-initials", 'full_name = "nguyen van anh"\nwords = full_name.split()\nprint(f"{words[0][0].upper()}.{words[1][0].upper()}.{words[2][0].upper()}")',
         'full_name = "nguyen van anh"\nwords = full_name.split()\nprint(f"{words[0]}.{words[1]}.{words[2]}")'),
        ("py-fmt-slug", 'title = "  Learn Python FAST! "\nprint(title.strip().lower().replace(" ", "-"))',
         'title = "  Learn Python FAST! "\nprint(title.lower())'),
    ],
)

print("module 3 content written")
