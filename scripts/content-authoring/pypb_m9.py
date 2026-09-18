#!/usr/bin/env python3
"""Module 9: files-paths-and-data — lessons + practices.

Grading constraint (sandbox): each test process re-executes the solution, so
graded file challenges use write-mode (idempotent) or `in`-semantics asserts.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "files-paths-and-data"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
Programs become real when their work survives after they exit. Files are the
simplest persistence.

## Reading a file

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()          # whole file as one string
print(content)
```

`open(path, mode, encoding=...)` returns a file object; `"r"` is read mode. The
`with` block closes the file automatically — even if an error happens inside.
Always use `with`.

Useful reads:

```python
with open("notes.txt", encoding="utf-8") as f:
    lines = f.readlines()       # list of lines (with trailing newlines)

with open("notes.txt", encoding="utf-8") as f:
    for line in f:              # memory-friendly: line by line
        print(line.strip())
```

A file that does not exist raises `FileNotFoundError` — you already know how to
catch it.
"""

L1_VI = """
Chương trình trở nên thật khi kết quả của nó sống sót sau khi chương trình kết
thúc. Tệp là hình thức lưu trữ đơn giản nhất.

## Đọc tệp

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()          # toàn bộ tệp như một chuỗi
print(content)
```

`open(path, mode, encoding=...)` trả về một file object; `"r"` là chế độ đọc.
Khối `with` tự đóng tệp — kể cả khi có lỗi xảy ra bên trong. Luôn dùng `with`.

Các cách đọc hữu ích:

```python
with open("notes.txt", encoding="utf-8") as f:
    lines = f.readlines()       # danh sách các dòng (có ký tự xuống dòng)

with open("notes.txt", encoding="utf-8") as f:
    for line in f:              # tiết kiệm bộ nhớ: từng dòng một
        print(line.strip())
```

Một tệp không tồn tại sẽ raise `FileNotFoundError` — bạn đã biết cách bắt nó.
"""

L2 = """
## Writing and appending

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("first line\\n")     # YOU supply the newlines
    f.write("second line\\n")
```

`"w"` **replaces** the whole file. `"a"` appends to the end:

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("2026-09-13 ran report\\n")
```

Two beginner traps: forgetting `\\n` (everything lands on one line), and using
`"w"` on a log (yesterday's data is gone). Write mode for reports, append mode
for logs.

## Paths with pathlib

```python
from pathlib import Path

p = Path("data") / "notes.txt"   # join paths portably
print(p.exists())                # False or True
print(Path.cwd())                # where the program runs
```

`Path` joins with `/`, checks existence, and gives you `.name`, `.suffix`, and
`.parent` — use it instead of gluing strings with `+`.
"""

L2_VI = """
## Ghi và nối thêm

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("dòng đầu\\n")       # CHÍNH BẠN cung cấp ký tự xuống dòng
    f.write("dòng hai\\n")
```

`"w"` **ghi đè** toàn bộ tệp. `"a"` nối vào cuối:

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("2026-09-13 chạy báo cáo\\n")
```

Hai cái bẫy của người mới: quên `\\n` (mọi thứ dồn vào một dòng), và dùng `"w"`
cho nhật ký (dữ liệu hôm qua biến mất). Chế độ ghi cho báo cáo, chế độ nối cho
nhật ký.

## Đường dẫn với pathlib

```python
from pathlib import Path

p = Path("data") / "notes.txt"   # nối đường dẫn một cách tương thích
print(p.exists())                # False hoặc True
print(Path.cwd())                # chương trình chạy ở đâu
```

`Path` nối bằng `/`, kiểm tra sự tồn tại, và cho bạn `.name`, `.suffix`,
`.parent` — dùng nó thay vì dán chuỗi bằng `+`.
"""

L3 = """
CSV (comma-separated values) is the universal export format of spreadsheets.

```python
line = "minh,21,Hanoi"
name, age, city = line.split(",")
# "minh", "21", "Hanoi"  — note age is still a STRING
```

Reading a whole CSV:

```python
rows = []
with open("people.csv", encoding="utf-8") as f:
    for line in f:
        rows.append(line.strip().split(","))
```

The first row of most CSVs is a header — skip it with slicing (`rows[1:]`) or
read it as column names. Values always arrive as strings; convert numbers
yourself.

Writing is the mirror image:

```python
with open("summary.csv", "w", encoding="utf-8") as f:
    f.write("name,total\\n")
    f.write(f"{name},{total}\\n")
```

(The real `csv` module handles quoting edge cases — meet it in Intermediate.
For well-behaved data, split/join is honest work.)
"""

L3_VI = """
CSV (giá trị phân tách bằng dấu phẩy) là định dạng xuất phổ quát của bảng tính.

```python
line = "minh,21,Hanoi"
name, age, city = line.split(",")
# "minh", "21", "Hanoi"  — lưu ý age vẫn là CHUỖI
```

Đọc cả tệp CSV:

```python
rows = []
with open("people.csv", encoding="utf-8") as f:
    for line in f:
        rows.append(line.strip().split(","))
```

Dòng đầu của phần lớn CSV là tiêu đề — bỏ qua bằng cắt lát (`rows[1:]`) hoặc đọc
nó làm tên cột. Giá trị luôn đến dưới dạng chuỗi; tự chuyển đổi số nhé.

Ghi là hình ảnh phản chiếu:

```python
with open("summary.csv", "w", encoding="utf-8") as f:
    f.write("name,total\\n")
    f.write(f"{name},{total}\\n")
```

(Mô-đun `csv` thật xử lý các trường hợp ngoặc kép phức tạp — bạn sẽ gặp trong
Intermediate. Với dữ liệu dễ bảo, split/join là công việc trung thực.)
"""

L4 = """
JSON is how programs share structured data — the same format your future APIs
will speak.

```python
import json

config = {"theme": "dark", "font_size": 14, "tags": ["work", "urgent"]}

text = json.dumps(config)        # dict -> JSON string
again = json.loads(text)         # JSON string -> dict
```

And the file versions — the save/load pattern that powers small apps:

```python
import json

def save(contacts, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
```

`ensure_ascii=False` keeps Vietnamese text readable in the file; `indent=2`
makes it human-inspectable. JSON supports dicts, lists, strings, numbers,
booleans, and null — tuples become lists, and anything else needs conversion
before saving.
"""

L4_VI = """
JSON là cách các chương trình chia sẻ dữ liệu có cấu trúc — cùng định dạng mà
những API tương lai của bạn sẽ nói.

```python
import json

config = {"theme": "dark", "font_size": 14, "tags": ["work", "urgent"]}

text = json.dumps(config)        # dict -> chuỗi JSON
again = json.loads(text)         # chuỗi JSON -> dict
```

Và phiên bản tệp — mẫu save/load tạo nên các ứng dụng nhỏ:

```python
import json

def save(contacts, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
```

`ensure_ascii=False` giữ văn bản tiếng Việt dễ đọc trong tệp; `indent=2` giúp
con người dễ xem. JSON hỗ trợ dict, list, chuỗi, số, boolean, và null — tuple
thành list, còn thứ gì khác cần chuyển đổi trước khi lưu.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "m9-read-write-practice",
    "Read & Write Drills",
    "Open, read, write, append — files that survive.",
    "Bài tập đọc & ghi",
    "Mở, đọc, ghi, nối thêm — tệp tồn tại bền vững.",
    "reading-files", 30, "beginner",
    [
        challenge(
            "py-file-write-greeting",
            "Write a Greeting File",
            "Write the text Hello, Code Journey! (exactly, no trailing newline) into greeting.txt using a with-block. The test reads the file back.",
            "",
            [("file has the right content", 'with open("greeting.txt", encoding="utf-8") as _f:\n    _c = _f.read()\nassert _c == "Hello, Code Journey!", f"file contains {_c!r}"\nassert "with open" in code, "use a with-block"', 
              'with open("greeting.txt", "w", encoding="utf-8") as f: f.write("Hello, Code Journey!") — no \\n in the text.')],
            level="guided",
        ),
        challenge(
            "py-file-count-lines",
            "Create It, Then Count It",
            "Two steps in one program: (1) write input.txt containing EXACTLY these four lines, one per line: alpha, beta, gamma, delta. (2) Read the file back and print the number of lines (just the number).",
            "",
            [("prints the line count", 'with open("input.txt", encoding="utf-8") as _f:\n    _c = _f.read()\nassert _c == "alpha\\nbeta\\ngamma\\ndelta\\n", f"file content wrong: {_c!r}"\nassert printed[0] == "4", f"got {printed}"',
              "Write the four lines with a trailing \\n each; then with open(...) as f: print(len(f.readlines())).")],
            level="guided",
        ),
        challenge(
            "py-file-append-log",
            "Append a Log Line",
            "Append the single line run complete to log.txt (append mode!). The test checks the line exists in the file. Use \"a\", not \"w\".",
            "",
            [("log contains the line", 'with open("log.txt", encoding="utf-8") as _f:\n    _c = _f.read()\nassert "run complete" in _c, f"log is {_c!r}"\nassert \'"a"\' in code, "open in append mode"',
              'with open("log.txt", "a", encoding="utf-8") as f: f.write("run complete\\n")')],
            level="guided",
        ),
        challenge(
            "py-file-report-writer",
            "Mini Build: Report Writer",
            'inventory = {"apples": 12, "bananas": 7} is given. Write summary.csv with a header line name,qty then one line per item (apples,12 then bananas,7). No trailing newline needed on the last line.',
            'inventory = {"apples": 12, "bananas": 7}\n',
            [("csv written correctly", 'with open("summary.csv", encoding="utf-8") as _f:\n    _lines = [ _l for _l in _f.read().splitlines() if _l.strip() ]\nassert _lines == ["name,qty", "apples,12", "bananas,7"], f"got {_lines}"',
              "write the header, then loop the dict writing f\"{name},{qty}\\n\" per line.")],
            level="mini-build",
        ),
    ],
    {
        "py-file-write-greeting": vi_challenge("Ghi tệp lời chào", "Ghi văn bản Hello, Code Journey! (chính xác, không xuống dòng cuối) vào greeting.txt bằng khối with. Bài kiểm tra đọc tệp lại.",
                                        [("tệp có đúng nội dung", 'with open("greeting.txt", "w", encoding="utf-8") as f: f.write("Hello, Code Journey!") — không có \\n trong văn bản.')]),
        "py-file-count-lines": vi_challenge("Đếm số dòng", "Tệp input.txt tồn tại trong thư mục chạy với vài dòng. Đếm số dòng của nó và chỉ in con số (ví dụ 4).",
                                        [("in số dòng", "with open(...) as f: lines = f.readlines() rồi print(len(lines)).")]),
        "py-file-append-log": vi_challenge("Nối dòng nhật ký", "Nối một dòng run complete vào log.txt (chế độ append!). Bài kiểm tra kiểm tra dòng đó tồn tại trong tệp. Dùng \"a\", không phải \"w\".",
                                        [("nhật ký có dòng đó", 'with open("log.txt", "a", encoding="utf-8") as f: f.write("run complete\\n")')]),
        "py-file-report-writer": vi_challenge("Mini build: Trình viết báo cáo", 'inventory = {"apples": 12, "bananas": 7} đã cho. Ghi summary.csv với dòng tiêu đề name,qty rồi mỗi mục một dòng (apples,12 rồi bananas,7). Không cần xuống dòng cuối.',
                                        [("csv ghi đúng", 'Ghi tiêu đề, rồi duyệt dict ghi f"{name},{qty}\\n" từng dòng.')]),
    },
    solutions=[
        ("py-file-write-greeting", 'with open("greeting.txt", "w", encoding="utf-8") as f:\n    f.write("Hello, Code Journey!")',
         'with open("greeting.txt", "w", encoding="utf-8") as f:\n    f.write("Hello, Code Journey!\\n")'),
        ("py-file-count-lines", 'with open("input.txt", "w", encoding="utf-8") as f:\n    f.write("alpha\\nbeta\\ngamma\\ndelta\\n")\nwith open("input.txt", encoding="utf-8") as f:\n    print(len(f.readlines()))',
         'with open("input.txt", "w", encoding="utf-8") as f:\n    f.write("alpha\\nbeta\\ngamma\\ndelta\\n")\nwith open("input.txt", encoding="utf-8") as f:\n    print(len(f.readlines()) - 1)'),
        ("py-file-append-log", 'with open("log.txt", "a", encoding="utf-8") as f:\n    f.write("run complete\\n")',
         'with open("log.txt", "w", encoding="utf-8") as f:\n    f.write("other entry\\n")'),
        ("py-file-report-writer", 'inventory = {"apples": 12, "bananas": 7}\nwith open("summary.csv", "w", encoding="utf-8") as f:\n    f.write("name,qty\\n")\n    for name, qty in inventory.items():\n        f.write(f"{name},{qty}\\n")',
         'inventory = {"apples": 12, "bananas": 7}\nwith open("summary.csv", "w", encoding="utf-8") as f:\n    f.write("name,qty\\n")\n    for name, qty in inventory.items():\n        f.write(f"{name}:{qty}\\n")'),
    ],
)

write_practice(
    MOD, "m9-json-practice",
    "JSON Persistence",
    "dumps/loads, save/load, and a tiny contact book.",
    "Lưu trữ JSON",
    "dumps/loads, save/load, và một sổ liên lạc nhỏ.",
    "json-persistence", 35, "beginner",
    [
        challenge(
            "py-json-roundtrip",
            "Roundtrip",
            "Write profile(text) that parses a JSON string into a dict and returns the value at key \"city\". json.loads is your friend.",
            'import json\n\ndef profile(text):\n    pass\n',
            [("parses and extracts", 'assert profile(chr(123) + chr(34) + "city" + chr(34) + ": " + chr(34) + "Hanoi" + chr(34) + chr(125)) == "Hanoi", "extract the city"', 
              'import json; return json.loads(text)["city"]')],
            level="imitation",
        ),
        challenge(
            "py-json-save-contacts",
            "Save Contacts",
            "contacts is given (a dict of name -> phone). Save it as JSON into contacts.json with ensure_ascii=False and indent=2. The test loads the file back and compares.",
            'contacts = {"Minh": "0901", "Lan": "0902"}\n',
            [("file round-trips", 'import json as _j\nwith open("contacts.json", encoding="utf-8") as _f:\n    _d = _j.load(_f)\nassert _d == {"Minh": "0901", "Lan": "0902"}, f"got {_d}"\nassert "json.dump" in code, "use json.dump into the open file"',
              'with open("contacts.json", "w", encoding="utf-8") as f: json.dump(contacts, f, ensure_ascii=False, indent=2)')],
            level="guided",
        ),
        challenge(
            "py-json-persist-roundtrip",
            "Mini Build: Save Then Load",
            'The persistence cycle in one program: build a list of two dicts (task, done) for tasks "write report" (done) and "send email" (not done), save it to tasks.json, then load it back and print the COUNT of unfinished tasks (one line, just the number).',
            "",
            [("unfinished count printed", 'assert printed[0] == "1", f"got {printed}"\nimport json as _j\nwith open("tasks.json", encoding="utf-8") as _f:\n    _d = _j.load(_f)\nassert isinstance(_d, list) and len(_d) == 2 and all("task" in t and "done" in t for t in _d), f"bad file {_d}"',
              "save with json.dump; load with json.load; count entries where not done.")],
            level="mini-build",
        ),
    ],
    {
        "py-json-roundtrip": vi_challenge("Vòng lặp hai chiều", 'Viết profile(text) phân tích một chuỗi JSON thành dict và trả về giá trị tại khóa "city". json.loads là bạn của bạn.',
                                        [("phân tích và trích xuất", 'import json; return json.loads(text)["city"]')]),
        "py-json-save-contacts": vi_challenge("Lưu liên lạc", 'contacts đã cho (dict tên -> điện thoại). Lưu nó thành JSON vào contacts.json với ensure_ascii=False và indent=2. Bài kiểm tra nạp tệp lại và so sánh.',
                                        [("tệp khớp khi nạp lại", 'with open("contacts.json", "w", encoding="utf-8") as f: json.dump(contacts, f, ensure_ascii=False, indent=2)')]),
        "py-json-persist-roundtrip": vi_challenge("Mini build: Lưu rồi nạp", 'Chu kỳ lưu trữ trong một chương trình: xây danh sách hai dict (task, done) cho các việc "viết báo cáo" (done) và "gửi email" (chưa done), lưu vào tasks.json, rồi nạp lại và in SỐ công việc chưa xong (một dòng, chỉ con số).',
                                        [("số chưa xong được in", "Lưu bằng json.dump; nạp bằng json.load; đếm các mục chưa done.")]),
    },
    solutions=[
        ("py-json-roundtrip", 'import json\n\ndef profile(text):\n    return json.loads(text)["city"]',
         'import json\n\ndef profile(text):\n    return text["city"]'),
        ("py-json-save-contacts", 'import json\n\ncontacts = {"Minh": "0901", "Lan": "0902"}\nwith open("contacts.json", "w", encoding="utf-8") as f:\n    json.dump(contacts, f, ensure_ascii=False, indent=2)',
         'import json\n\ncontacts = {"Minh": "0901", "Lan": "0902"}\nwith open("contacts.json", "w", encoding="utf-8") as f:\n    f.write(str(contacts))'),
        ("py-json-persist-roundtrip", 'import json\n\ntasks = [\n    {"task": "write report", "done": True},\n    {"task": "send email", "done": False},\n]\nwith open("tasks.json", "w", encoding="utf-8") as f:\n    json.dump(tasks, f, ensure_ascii=False, indent=2)\n\nwith open("tasks.json", encoding="utf-8") as f:\n    loaded = json.load(f)\nprint(sum(1 for t in loaded if not t["done"]))',
         'import json\n\ntasks = [\n    {"task": "write report", "done": True},\n    {"task": "send email", "done": False},\n]\nwith open("tasks.json", "w", encoding="utf-8") as f:\n    json.dump(tasks, f, ensure_ascii=False, indent=2)\n\nwith open("tasks.json", encoding="utf-8") as f:\n    loaded = json.load(f)\nprint(len(loaded))'),
    ],
)

write_practice(
    MOD, "m9-csv-paths-practice",
    "CSV & Path Drills",
    "Split, join, and find your way around the filesystem.",
    "Bài tập CSV & đường dẫn",
    "Split, join, và làm quen hệ thống tệp.",
    "paths-pathlib", 25, "beginner",
    [
        challenge(
            "py-csv-parse-line",
            "Parse a CSV Row",
            "Write parse_row(line) that takes one CSV line like name,age,city and returns a dict with keys name (str), age (int), city (str).",
            'def parse_row(line):\n    pass\n',
            [("parses one row", 'assert parse_row("minh,21,Hanoi") == {"name": "minh", "age": 21, "city": "Hanoi"}, f"got {parse_row(chr(109)+chr(105)+chr(110)+chr(104)+chr(44)+chr(50)+chr(49)+chr(44)+chr(72)+chr(97)+chr(110)+chr(111)+chr(105))}"\nassert parse_row("lan,19,Danang")["age"] == 19, "age must be an int"',
              'parts = line.split(","); return {"name": parts[0], "age": int(parts[1]), "city": parts[2]}')],
            level="guided",
        ),
        challenge(
            "py-csv-topline",
            "Best Row Wins",
            "Two steps: (1) create scores.csv with EXACTLY this content — header name,score, then rows minh,7 / lan,9 / bo,8 (one per line, with final newline). (2) Read it back and print the NAME of the highest scorer (one line).",
            "",
            [("prints top scorer", 'with open("scores.csv", encoding="utf-8") as _f:\n    _c = _f.read()\nassert _c == "name,score\\nminh,7\\nlan,9\\nbo,8\\n", f"file content wrong: {_c!r}"\nassert printed[0] == "lan", f"got {printed}"',
              "write with \\n per line; readlines()[1:] skips the header; track the best (name, score) while looping.")],
            level="independent",
        ),
        challenge(
            "py-path-exists",
            "Path Detective",
            'Write check(path) that returns "missing" when the path does not exist and "found" when it does. Use pathlib.',
            'from pathlib import Path\n\ndef check(path):\n    pass\n',
            [("exists vs missing", 'import os as _os\n_os.remove("temp_probe.txt") if _os.path.exists("temp_probe.txt") else None\nopen("temp_probe.txt", "w").write("x")\nassert check("temp_probe.txt") == "found", "existing file must be found"\n_os.remove("temp_probe.txt")\nassert check("definitely_not_here.bin") == "missing", "missing file must be missing"\nassert "Path" in code, "use pathlib"',
              'return "found" if Path(path).exists() else "missing"')],
            level="guided",
        ),
    ],
    {
        "py-csv-parse-line": vi_challenge("Phân tích dòng CSV", "Viết parse_row(line) nhận một dòng CSV dạng name,age,city và trả về dict với khóa name (str), age (int), city (str).",
                                        [("phân tích một dòng", 'parts = line.split(","); return {"name": parts[0], "age": int(parts[1]), "city": parts[2]}')]),
        "py-csv-topline": vi_challenge("Dòng tốt nhất thắng", "scores.csv nằm trong thư mục chạy với tiêu đề name,score và mỗi người chơi một dòng. In TÊN của người có điểm cao nhất (một dòng).",
                                        [("in người dẫn đầu", "readlines()[1:] bỏ qua tiêu đề; theo dõi cặp (tên, điểm) tốt nhất khi duyệt.")]),
        "py-path-exists": vi_challenge("Thám tử đường dẫn", 'Viết check(path) trả về "missing" khi đường dẫn không tồn tại và "found" khi tồn tại. Dùng pathlib.',
                                        [("tồn tại hay thiếu", 'return "found" if Path(path).exists() else "missing"')]),
    },
    solutions=[
        ("py-csv-parse-line", 'def parse_row(line):\n    parts = line.split(",")\n    return {"name": parts[0], "age": int(parts[1]), "city": parts[2]}',
         'def parse_row(line):\n    parts = line.split(",")\n    return {"name": parts[0], "age": parts[1], "city": parts[2]}'),
        ("py-csv-topline", 'with open("scores.csv", "w", encoding="utf-8") as f:\n    f.write("name,score\\nminh,7\\nlan,9\\nbo,8\\n")\nwith open("scores.csv", encoding="utf-8") as f:\n    rows = [line.strip().split(",") for line in f.readlines()[1:] if line.strip()]\nbest_name, best_score = "", -1\nfor name, score in rows:\n    if int(score) > best_score:\n        best_name, best_score = name, int(score)\nprint(best_name)',
         'with open("scores.csv", "w", encoding="utf-8") as f:\n    f.write("name,score\\nminh,7\\nlan,9\\nbo,8\\n")\nwith open("scores.csv", encoding="utf-8") as f:\n    rows = [line.strip().split(",") for line in f.readlines()[1:] if line.strip()]\nprint(rows[0][0])'),
        ("py-path-exists", 'from pathlib import Path\n\ndef check(path):\n    return "found" if Path(path).exists() else "missing"',
         'from pathlib import Path\n\ndef check(path):\n    return "missing" if Path(path).exists() else "found"'),
    ],
)

print("module 9 content written")
