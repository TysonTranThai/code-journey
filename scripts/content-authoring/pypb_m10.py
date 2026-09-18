#!/usr/bin/env python3
"""Module 10: modules-and-standard-library — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "modules-and-standard-library"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
An **import** makes code from another file available in yours:

```python
import math

print(math.sqrt(144))    # 12.0 — note the module NAME prefix
```

The prefix is the point: every use shows where the function came from. `from
import` copies specific names out:

```python
from math import sqrt

print(sqrt(144))         # 12.0 — no prefix, but the origin is less visible
```

For a beginner, prefer plain `import math`: readers can trace every name, and
imports at the top of the file form a table of contents. Reserve `from import`
for long module names or very frequent use.
"""

L1_VI = """
Một **import** làm cho mã từ tệp khác khả dụng trong tệp của bạn:

```python
import math

print(math.sqrt(144))    # 12.0 — lưu ý tiền tố TÊN module
```

Tiền tố chính là điểm mấu chốt: mỗi lần dùng cho thấy hàm đến từ đâu. `from
import` chép các tên cụ thể ra:

```python
from math import sqrt

print(sqrt(144))         # 12.0 — không tiền tố, nhưng nguồn gốc ít rõ hơn
```

Với người mới, hãy ưu tiên `import math` thuần: người đọc truy vết được từng
tên, và các import đầu tệp tạo thành mục lục. Dành `from import` cho tên module
dài hoặc dùng rất thường xuyên.
"""

L2 = """
Any `.py` file is a **module**. Create `geometry.py`:

```python
PI_APPROX = 3.14159

def circle_area(r):
    return PI_APPROX * r * r
```

Now `import geometry` from a file in the same folder and call
`geometry.circle_area(2)`.

## __name__: script or import?

Every module has a `__name__`. When run directly it is `"__main__"`; when
imported it is the module's name. This powers the standard guard:

```python
def main():
    print("running demo")

if __name__ == "__main__":
    main()
```

Import `geometry` and `main()` stays quiet; run `python geometry.py` and it
prints. One file, two behaviors — reusable by others, runnable by you.
"""

L2_VI = """
Mọi tệp `.py` đều là một **module**. Tạo `geometry.py`:

```python
PI_APPROX = 3.14159

def circle_area(r):
    return PI_APPROX * r * r
```

Giờ `import geometry` từ một tệp cùng thư mục và gọi
`geometry.circle_area(2)`.

## __name__: script hay import?

Mỗi module có một `__name__`. Khi chạy trực tiếp nó là `"__main__"`; khi được
import nó là tên module. Đây là nguồn gốc của lớp bảo vệ chuẩn:

```python
def main():
    print("chạy demo")

if __name__ == "__main__":
    main()
```

Import `geometry` và `main()` vẫn im lặng; chạy `python geometry.py` và nó in.
Một tệp, hai hành vi — người khác dùng lại được, bạn chạy trực tiếp được.
"""

L3 = """
The standard library is the toolbox that ships with Python. Four workhorses:

## random — simulations and games

```python
import random

roll = random.randint(1, 6)          # 1..6 inclusive
pick = random.choice(["a", "b", "c"])
random.seed(42)                      # reproducible "randomness"
```

`seed` pins the generator: same seed, same sequence — essential for tests and
debugging.

## datetime — timestamps and durations

```python
from datetime import date

today = date(2026, 9, 13)
print(today.year, today.month)       # 2026 9
print(date(2026, 9, 13) - date(2026, 1, 1))   # 255 days, 0:00:00
```

## statistics — one-line averages

```python
import statistics

statistics.mean([2, 4, 9])   # 5
statistics.median([1, 9, 5]) # 5
```

The lesson here is bigger than any one module: **before writing a helper,
suspect the standard library already has it.**
"""

L3_VI = """
Thư viện chuẩn là hộp công cụ đi kèm Python. Bốn con ngựa thợ:

## random — mô phỏng và trò chơi

```python
import random

roll = random.randint(1, 6)          # 1..6 bao gồm hai đầu
pick = random.choice(["a", "b", "c"])
random.seed(42)                      # "ngẫu nhiên" tái lập được
```

`seed` ghim bộ sinh: cùng seed, cùng chuỗi — thiết yếu cho kiểm thử và gỡ lỗi.

## datetime — dấu thời gian và khoảng thời gian

```python
from datetime import date

today = date(2026, 9, 13)
print(today.year, today.month)       # 2026 9
print(date(2026, 9, 13) - date(2026, 1, 1))   # 255 days, 0:00:00
```

## statistics — trung bình một dòng

```python
import statistics

statistics.mean([2, 4, 9])   # 5
statistics.median([1, 9, 5]) # 5
```

Bài học lớn hơn bất kỳ module nào: **trước khi viết một hàm trợ giúp, hãy nghi
ngờ thư viện chuẩn đã có sẵn nó.**
"""

L4 = """
Three more tools that appear constantly in real code:

## pathlib — filesystem paths as objects

```python
from pathlib import Path

data_dir = Path("data")
print(data_dir / "notes.txt")   # data/notes.txt
print(Path("report.pdf").suffix)  # .pdf
```

## json — data interchange

```python
import json

json.dumps({"ok": True})      # '{"ok": true}'
json.loads('{"ok": true}')    # {"ok": True}
```

## collections.Counter — counting, done right

```python
from collections import Counter

votes = ["anh", "binh", "anh", "cuong", "anh"]
c = Counter(votes)
print(c.most_common(1))       # [('anh', 3)]
print(c["binh"])              # 1 — missing keys count as 0
```

Notice what Counter replaces: a manual loop with a dict of tallies and a
missing-key branch. Standard-library tools are usually shorter AND clearer.
"""

L4_VI = """
Ba công cụ nữa xuất hiện liên tục trong mã thật:

## pathlib — đường dẫn hệ thống tệp dưới dạng đối tượng

```python
from pathlib import Path

data_dir = Path("data")
print(data_dir / "notes.txt")   # data/notes.txt
print(Path("report.pdf").suffix)  # .pdf
```

## json — trao đổi dữ liệu

```python
import json

json.dumps({"ok": True})      # '{"ok": true}'
json.loads('{"ok": true}')    # {"ok": True}
```

## collections.Counter — đếm, đúng chuẩn

```python
from collections import Counter

votes = ["anh", "binh", "anh", "cuong", "anh"]
c = Counter(votes)
print(c.most_common(1))       # [('anh', 3)]
print(c["binh"])              # 1 — khóa thiếu được tính là 0
```

Để ý xem Counter thay thế gì: một vòng lặp thủ công với dict đếm và nhánh xử
lý khóa thiếu. Công cụ thư viện chuẩn thường ngắn hơn VÀ rõ hơn.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "m10-import-practice",
    "Import & Module Drills",
    "Prefix discipline and the __main__ guard.",
    "Bài tập import & module",
    "Kỷ luật tiền tố và lớp bảo vệ __main__.",
    "imports-modules", 25, "beginner",
    [
        challenge(
            "py-mod-prefix",
            "Use the Prefix",
            "Compute the square root of 225 using the math module and print it (one line).",
            "",
            [("sqrt via math", 'assert printed[0] == "15.0", f"got {printed}"\nassert "import math" in code, "import the math module"\nassert "math.sqrt" in code, "use math.sqrt — the canonical square-root function"',
              "import math then print(math.sqrt(225)).")],
            level="imitation",
        ),
        challenge(
            "py-mod-own-module",
            "Import Your Own",
            "Create two-module structure in ONE source: define area(r) (circle area, using 3.14159) inside a simulated module namespace... actually simpler: define area(r) and a main() that prints area(2) — but call main() ONLY under an if __name__ == \"__main__\": guard. The grader imports your definitions without running main(); printed must be EMPTY.",
            "",
            [("definitions available, main silent", 'assert callable(area), "define area(r)"\nassert abs(area(2) - 12.56636) < 1e-3, f"area(2) should be ~12.566, got {area(2)}"\nassert printed == [], f"main() must NOT run on import — guard it. got {printed}"\nassert (chr(105)+chr(102)+chr(32)+chr(95)*2+"name"+chr(95)*2) in code.replace(" ", "") or "__main__" in code, "add the __main__ guard"',
              "def area(r): return 3.14159 * r * r / def main(): print(area(2)) / if __name__ == \"__main__\": main()")],
            level="guided",
        ),
        challenge(
            "py-mod-from-import",
            "from import, Judged",
            "Import sqrt from math via from-import and print sqrt(256).",
            "",
            [("from-import works", 'assert printed[0] == "16.0", f"got {printed}"\nassert "from math import" in code, "use from math import sqrt"',
              "from math import sqrt / print(sqrt(256))")],
            level="imitation",
        ),
    ],
    {
        "py-mod-prefix": vi_challenge("Dùng tiền tố", "Tính căn bậc hai của 225 bằng module math và in ra (một dòng).",
                                        [("sqrt qua math", "import math rồi print(math.sqrt(225)).")]),
        "py-mod-own-module": vi_challenge('Import module của bạn', 'Xây cấu trúc hai module trong MỘT nguồn: định nghĩa area(r) (diện tích hình tròn, dùng 3.14159) và main() in area(2) — nhưng CHỈ gọi main() dưới lớp bảo vệ if __name__ == "__main__":. Bộ chấm import định nghĩa của bạn mà không chạy main(); printed phải RỖNG.',
                                        [("định nghĩa sẵn sàng, main im lặng", 'def area(r): return 3.14159 * r * r / def main(): print(area(2)) / if __name__ == "__main__": main()')]),
        "py-mod-from-import": vi_challenge("from import, có bị đánh giá", "Import sqrt từ math bằng from-import và in sqrt(256).",
                                        [("from-import hoạt động", "from math import sqrt / print(sqrt(256))")]),
    },
    solutions=[
        ("py-mod-prefix", "import math\n\nprint(math.sqrt(225))",
         "import math\n\nprint(math.pow(225, 0.5))"),
        ("py-mod-own-module", 'def area(r):\n    return 3.14159 * r * r\n\n\ndef main():\n    print(area(2))\n\n\nif __name__ == "__main__":\n    main()',
         'def area(r):\n    return 3.14159 * r * r\n\n\ndef main():\n    print(area(2))\n\n\nmain()'),
        ("py-mod-from-import", "from math import sqrt\n\nprint(sqrt(256))",
         "import math\n\nprint(sqrt(256))"),
    ],
)

write_practice(
    MOD, "m10-stdlib-practice",
    "Standard Library Tour",
    "random, datetime, statistics, Counter — borrowed power.",
    "Tham quan thư viện chuẩn",
    "random, datetime, statistics, Counter — sức mạnh mượn được.",
    "stdlib-tour", 30, "beginner",
    [
        challenge(
            "py-std-seeded-roll",
            "Seeded Roll",
            "Seed the random generator with 42, then print random.randint(1, 10). The value is deterministic — tests know it.",
            "",
            [("deterministic output", 'assert printed[0] == "2", f"seed 42 gives 2, got {printed}"\nassert "seed(42)" in code, "seed with 42"\nassert "import random" in code, "import random"',
              "import random / random.seed(42) / print(random.randint(1, 10))")],
            level="guided",
        ),
        challenge(
            "py-std-date-diff",
            "Days Between",
            "Using datetime.date, print the number of days between 2026-01-01 and 2026-09-13 (one line, just the number; subtracting dates gives a timedelta with .days).",
            "",
            [("prints day count", 'assert printed[0] == "255", f"got {printed}"\nassert "date" in code, "use datetime.date"',
              "from datetime import date / d = date(2026, 9, 13) - date(2026, 1, 1) / print(d.days)")],
            level="guided",
        ),
        challenge(
            "py-std-stats",
            "One-Line Statistics",
            "Print two lines: the mean of [2, 4, 9] and the median of [1, 2, 9], using the statistics module.",
            "",
            [("mean then median", 'assert printed == ["5", "2"], f"got {printed}"\nassert "statistics" in code, "use the statistics module"',
              "import statistics / print(statistics.mean([2, 4, 9])) / print(statistics.median([1, 2, 9]))")],
            level="imitation",
        ),
        challenge(
            "py-std-counter",
            "Counting with Counter",
            "votes = [\"anh\", \"binh\", \"anh\", \"cuong\", \"anh\"] is given. Print the winner's name using collections.Counter (one line).",
            'votes = ["anh", "binh", "anh", "cuong", "anh"]\n',
            [("winner via Counter", 'assert printed[0] == "anh", f"got {printed}"\nassert "Counter" in code, "use Counter"',
              "from collections import Counter / print(Counter(votes).most_common(1)[0][0])")],
            level="guided",
        ),
    ],
    {
        "py-std-seeded-roll": vi_challenge("Xúc xắc có seed", "Seed bộ sinh ngẫu nhiên với 42, rồi in random.randint(1, 10). Giá trị là tất định — bài kiểm tra biết trước.",
                                        [("kết quả tất định", "import random / random.seed(42) / print(random.randint(1, 10))")]),
        "py-std-date-diff": vi_challenge("Số ngày giữa hai mốc", "Dùng datetime.date, in số ngày giữa 2026-01-01 và 2026-09-13 (một dòng, chỉ con số; hiệu hai ngày cho một timedelta có .days).",
                                        [("in số ngày", "from datetime import date / d = date(2026, 9, 13) - date(2026, 1, 1) / print(d.days)")]),
        "py-std-stats": vi_challenge("Thống kê một dòng", "In hai dòng: trung bình của [2, 4, 9] và trung vị của [1, 2, 9], dùng module statistics.",
                                        [("rồi trung vị", "import statistics / print(statistics.mean([2, 4, 9])) / print(statistics.median([1, 2, 9]))")]),
        "py-std-counter": vi_challenge("Đếm bằng Counter", 'votes = ["anh", "binh", "anh", "cuong", "anh"] đã cho. In tên người thắng bằng collections.Counter (một dòng).',
                                        [("người thắng qua Counter", "from collections import Counter / print(Counter(votes).most_common(1)[0][0])")]),
    },
    solutions=[
        ("py-std-seeded-roll", "import random\n\nrandom.seed(42)\nprint(random.randint(1, 10))",
         "import random\n\nrandom.seed(42)\nprint(random.random())"),
        ("py-std-date-diff", "from datetime import date\n\nspan = date(2026, 9, 13) - date(2026, 1, 1)\nprint(span.days)",
         "from datetime import date\n\nspan = date(2026, 9, 13) - date(2026, 1, 1)\nprint(span.days + 1)"),
        ("py-std-stats", "import statistics\n\nprint(statistics.mean([2, 4, 9]))\nprint(statistics.median([1, 2, 9]))",
         "import statistics\n\nprint(statistics.mean([2, 4, 9]))\nprint(statistics.mean([1, 2, 9]))"),
        ("py-std-counter", 'from collections import Counter\n\nvotes = ["anh", "binh", "anh", "cuong", "anh"]\nprint(Counter(votes).most_common(1)[0][0])',
         'from collections import Counter\n\nvotes = ["anh", "binh", "anh", "cuong", "anh"]\nprint(Counter(votes).most_common(1)[0][1])'),
    ],
)

write_practice(
    MOD, "m10-toolkit-build",
    "Mini Build: Utility Toolkit",
    "One program, four tools — organized like a real module.",
    "Mini build: Bộ công cụ tiện ích",
    "Một chương trình, bốn công cụ — tổ chức như một module thật.",
    "stdlib-tour-2", 40, "beginner",
    [
        challenge(
            "py-toolkit-clipboard",
            "Toolkit: Text Stats",
            "Build analyze(text) returning a dict with keys words (word count), longest (the longest word — ties: the EARLIEST), and upper (the text in uppercase). Print analyze(sample) for sample = \\\"Code Journey teaches real Python skills\\\" as three lines: words / longest / upper value.",
            "",
            [("stats computed", 'result_keys = ["words", "longest", "upper"]\nassert len(printed) == 3, f"print three lines, got {printed}"\nassert printed[0] == "6", f"word count, got {printed}"\nassert printed[1] == "Journey", f"longest word (earliest tie), got {printed}"\nassert printed[2] == "CODE JOURNEY TEACHES REAL PYTHON SKILLS", f"upper, got {printed}"\nassert "def analyze" in code, "write analyze(text)"',
              'max(words, key=len) returns the FIRST longest on ties; .upper() for the shout.')],
            level="mini-build",
        ),
        challenge(
            "py-toolkit-counter-report",
            "Toolkit: Frequency Report",
            "Using Counter, write top_words(text, n) that returns the n most common lowercase words as a list of (word, count) tuples (ties: higher count first, then insertion order — Counter handles it). Print top_words(text, 2) for text = \\\"to be or not to be\\\" as two lines in the form: word=4",
            "",
            [("top words in order", 'assert printed == ["to=2", "be=2"], f"got {printed}"\nassert "Counter" in code and "def top_words" in code, "use Counter inside top_words"',
              "Counter(text.split()).most_common(n) is already ordered; format f\"{w}={c}\".")],
            level="mini-build",
        ),
    ],
    {
        "py-toolkit-clipboard": vi_challenge("Bộ công cụ: Thống kê văn bản", 'Xây analyze(text) trả về dict với khóa words (số từ), longest (từ dài nhất — hòa thì lấy từ XUẤT HIỆN TRƯỚC), và upper (văn bản IN HOA). In analyze(sample) cho sample = "Code Journey teaches real Python skills" thành ba dòng: words / longest / giá trị upper.',
                                        [("thống kê được tính", 'max(words, key=len) trả về từ dài nhất ĐẦU TIÊN khi hòa; .upper() để in hoa.')]),
        "py-toolkit-counter-report": vi_challenge("Bộ công cụ: Báo cáo tần suất", 'Dùng Counter, viết top_words(text, n) trả về n từ phổ biến nhất (viết thường) dưới dạng danh sách bộ (từ, số lần). In top_words(text, 2) cho text = "to be or not to be" thành hai dòng dạng: word=4',
                                        [("từ hàng đầu theo thứ tự", 'Counter(text.split()).most_common(n) đã có thứ tự; định dạng f"{w}={c}".')]),
    },
    solutions=[
        ("py-toolkit-clipboard", 'def analyze(text):\n    words = text.split()\n    longest = max(words, key=len)\n    return {"words": len(words), "longest": longest, "upper": text.upper()}\n\n\nsample = "Code Journey teaches real Python skills"\nresult = analyze(sample)\nprint(result["words"])\nprint(result["longest"])\nprint(result["upper"])',
         'def analyze(text):\n    words = text.split()\n    longest = max(words, key=len)\n    return {"words": len(words), "longest": longest, "upper": text.upper()}\n\n\nsample = "Code Journey teaches real Python skills"\nresult = analyze(sample)\nprint(result["words"])\nprint(result["longest"].upper())\nprint(result["upper"])'),
        ("py-toolkit-counter-report", 'from collections import Counter\n\n\ndef top_words(text, n):\n    return Counter(text.split()).most_common(n)\n\n\ntext = "to be or not to be"\nfor word, count in top_words(text, 2):\n    print(f"{word}={count}")',
         'from collections import Counter\n\n\ndef top_words(text, n):\n    return Counter(text.split()).most_common(n)\n\n\ntext = "to be or not to be"\nfor word, count in top_words(text, 2):\n    print(f"{word}:{count}")'),
    ],
)

# ── Checkpoint: files + modules ──────────────────────────────────────────────
CP = """
## Checkpoint: Files + Modules

Module 9 and 10 combined: parse a real data string, aggregate it, and organize
the logic as a reusable function — the exact shape of the toolkit you will ship
in the capstone.
"""

CP_VI = """
## Checkpoint: Tệp + Module

Module 9 và 10 kết hợp: phân tích một chuỗi dữ liệu thật, tổng hợp kết quả, và
tổ chức logic thành hàm dùng lại được — chính là hình dạng của bộ công cụ bạn
sẽ đóng gói trong capstone.
"""

write_checkpoint(
    MOD, "checkpoint-files-modules",
    "Checkpoint: Files + Modules",
    "CSV parsing plus Counter, wrapped in reusable functions.",
    20, CP,
    "Checkpoint: Tệp + Module",
    "Phân tích CSV cùng Counter, bọc trong các hàm dùng lại được.",
    CP_VI,
    challenge(
        "py-checkpoint-files-modules",
        "Inventory Aggregator",
        'csv_text = "apple,fruit\\ncarrot,veg\\nbanana,fruit\\nleek,veg\\ncherry,fruit" is given. Write count_categories(text) that parses the CSV (comma-separated, one item per line) and returns a dict mapping each category (column 2) to how many items it has. Print the dict — one line.',
        'csv_text = "apple,fruit\\ncarrot,veg\\nbanana,fruit\\nleek,veg\\ncherry,fruit"\n\ndef count_categories(text):\n    pass\n\nprint(count_categories(csv_text))\n',
        [
            ("categories counted",
             'assert count_categories("a,f\\nb,f") == {"f": 2}, "two-line case"\nassert count_categories(csv_text) == {"fruit": 3, "veg": 2}, f"main case: {count_categories(csv_text)}"', 
             "split lines, split commas, tally column 2 in a dict — or use Counter."),
        ],
        difficulty="beginner",
    ),
    vi_challenge("Tổng hợp kho hàng", 'csv_text = "apple,fruit\\ncarrot,veg\\nbanana,fruit\\nleek,veg\\ncherry,fruit" đã cho. Viết count_categories(text) phân tích CSV (phân tách bởi dấu phẩy, mỗi dòng một mục) và trả về dict ánh xạ từng danh mục (cột 2) với số lượng mục. In dict đó — một dòng.',
                 [("danh mục được đếm", "Tách dòng, tách dấu phẩy, đếm cột 2 vào một dict — hoặc dùng Counter.")]),
    solution='csv_text = "apple,fruit\\ncarrot,veg\\nbanana,fruit\\nleek,veg\\ncherry,fruit"\n\n\ndef count_categories(text):\n    counts = {}\n    for line in text.splitlines():\n        if not line.strip():\n            continue\n        _name, cat = line.split(",")\n        counts[cat] = counts.get(cat, 0) + 1\n    return counts\n\n\nprint(count_categories(csv_text))',
    wrong='csv_text = "apple,fruit\\ncarrot,veg\\nbanana,fruit\\nleek,veg\\ncherry,fruit"\n\n\ndef count_categories(text):\n    counts = {}\n    for line in text.splitlines():\n        if not line.strip():\n            continue\n        _name, cat = line.split(",")\n        counts[cat] = counts.get(cat, 0) + 1\n    return len(counts)\n\n\nprint(count_categories(csv_text))',
)

print("module 10 content written")
