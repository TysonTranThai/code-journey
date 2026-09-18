#!/usr/bin/env python3
"""Python Intermediate — module 6 (files-and-data)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

M6 = "files-and-data"
L6A = "pathlib-mastery"
L6B = "csv-json-roundtrips"
L6C = "streaming-data"
L6D = "checkpoint-data-pipeline"

write_module(
    M6,
    "Files, Serialization, and Data Flow",
    "Own paths, round-trip structured data, and stream records without loading everything.",
    "Tệp, Tuần tự hóa, và Dòng dữ liệu",
    "Làm chủ đường dẫn, khép vòng dữ liệu có cấu trúc, và stream bản ghi không cần nạp tất cả.",
    [L6A, L6B, L6C, L6D],
    ["m6-path-practice", "m6-serial-practice", "m6-stream-practice"],
)

write_lesson(
    M6, L6A,
    "pathlib: Paths as Objects",
    "Build, inspect, and read paths safely — no string surgery.",
    14,
    """
Beginner file code glues strings with `/` or `os.path.join`. `pathlib` treats
a path as an **object** with behavior:

```python
from pathlib import Path

data_dir = Path("data")
config = data_dir / "settings.json"     # / operator joins safely
config.name          # "settings.json"
config.stem          # "settings"
config.suffix        # ".json"
config.parent        # data
config.exists()
```

The Killer Features:

```python
data_dir.mkdir(parents=True, exist_ok=True)   # idempotent directory creation
for csv_file in data_dir.glob("*.csv"):       # pattern matching, lazy iterator
    print(csv_file)

text = config.read_text(encoding="utf-8")     # quick read (small files!)
config.write_text("{}", encoding="utf-8")     # quick write
```

## Path safety habits

- **Never trust user-supplied paths.** `Path(user_input).resolve()` then verify it's inside the directory you expect — otherwise `../../etc/passwd` walks out of your sandbox. That's path traversal, and it's module 11's audit topic too.
- **Pass `encoding=` on every text read/write.** The default encoding varies by platform; explicit UTF-8 is the portability contract.
- **`resolve()`** turns relative into absolute (and collapses `..`) — normalize first, compare after.
""",
    "pathlib: Đường dẫn là Đối tượng",
    "Dựng, kiểm tra, và đọc đường dẫn an toàn — không ghép chuỗi thủ công.",
    """
Code tệp của người mới ghép chuỗi bằng `/` hoặc `os.path.join`. `pathlib` coi
đường dẫn là một **đối tượng** có hành vi:

```python
from pathlib import Path

data_dir = Path("data")
config = data_dir / "settings.json"     # toán tử / nối một cách an toàn
config.name          # "settings.json"
config.stem          # "settings"
config.suffix        # ".json"
config.parent        # data
config.exists()
```

Những tính năng đắt giá:

```python
data_dir.mkdir(parents=True, exist_ok=True)   # tạo thư mục không lo trùng
for csv_file in data_dir.glob("*.csv"):       # so mẫu, iterator lười biếng
    print(csv_file)

text = config.read_text(encoding="utf-8")     # đọc nhanh (tệp nhỏ!)
config.write_text("{}", encoding="utf-8")     # ghi nhanh
```

## Thói quen an toàn với đường dẫn

- **Không bao giờ tin đường dẫn do người dùng cung cấp.** `Path(user_input).resolve()` rồi xác minh nó nằm trong thư mục bạn mong đợi — nếu không, `../../etc/passwd` sẽ đi ra ngoài sandbox của bạn. Đó là path traversal, và module 11 sẽ audit lại chủ đề này.
- **Luôn truyền `encoding=` khi đọc/ghi văn bản.** Mã hóa mặc định thay đổi theo nền tảng; UTF-8 tường minh là hợp đồng tính di động.
- **`resolve()`** biến đường dẫn tương đối thành tuyệt đối (và thu gọn `..`) — chuẩn hóa trước, so sánh sau.
""",
)

write_lesson(
    M6, L6B,
    "CSV and JSON Round-Trips",
    "Serialize records to files and back — with validation at the edges.",
    15,
    """
Two serialization formats cover most day-to-day work. **CSV** is rows of
fields (spreadsheets, exports); **JSON** is nested structures (APIs, configs).

```python
import csv, json
from pathlib import Path

# CSV: always newline="" on open, always DictReader/DictWriter
with Path("people.csv").open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))          # each row: dict[str, str]

with Path("people.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)
```

```python
# JSON: dumps/loads for strings, dump/load for files
record = {"name": "An", "tags": ["admin", "staff"]}
text = json.dumps(record, ensure_ascii=False, indent=2)
back = json.loads(text)

path = Path("record.json")
path.write_text(json.dumps(record), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))
```

## Round-trip honesty

Notice what each format does NOT preserve: CSV cells are **strings** —
`"30"` must be converted back to `int` yourself. JSON has no tuples, no
dates, and no Python-specific types. A "round trip" means **designing the
schema** (what types, what's required) and **validating at the boundary**
(module 5's discipline). Never feed untrusted JSON straight into your logic:
check keys and types first.

## Security footnote

`json` is safe for untrusted data. `pickle` is NOT — loading a malicious
pickle executes code. Rule: `json` for anything that crosses a trust
boundary, `pickle` only for your own trusted, local caches.
""",
    "CSV và JSON khép vòng",
    "Tuần tự hóa bản ghi ra tệp và đọc lại — với kiểm tra hợp lệ tại ranh giới.",
    """
Hai định dạng tuần tự hóa phủ phần lớn công việc hằng ngày. **CSV** là các
dòng gồm nhiều trường (bảng tính, file xuất); **JSON** là cấu trúc lồng nhau
(API, cấu hình).

```python
import csv, json
from pathlib import Path

# CSV: luôn newline="" khi mở, luôn DictReader/DictWriter
with Path("people.csv").open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))          # mỗi dòng: dict[str, str]

with Path("people.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)
```

```python
# JSON: dumps/loads cho chuỗi, dump/load cho tệp
record = {"name": "An", "tags": ["admin", "staff"]}
text = json.dumps(record, ensure_ascii=False, indent=2)
back = json.loads(text)

path = Path("record.json")
path.write_text(json.dumps(record), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))
```

## Sự trung thực của vòng khép

Hãy để ý mỗi định dạng KHÔNG giữ lại gì: ô của CSV là **chuỗi** — `"30"`
phải tự chuyển lại thành `int`. JSON không có tuple, không có ngày tháng, và
không có kiểu riêng của Python. Một "vòng khép" nghĩa là **thiết kế schema**
(những kiểu nào, bắt buộc gì) và **kiểm tra hợp lệ tại ranh giới** (kỷ luật
của module 5). Đừng bao giờ nạp JSON không tin cậy thẳng vào logic của bạn:
hãy kiểm tra key và kiểu trước.

## Chú thích an ninh

`json` an toàn với dữ liệu không tin cậy. `pickle` thì KHÔNG — nạp một
pickle độc hại là chạy mã của kẻ tấn công. Quy tắc: `json` cho bất cứ thứ gì
vượt ranh giới tin cậy, `pickle` chỉ cho cache cục bộ tin cậy của chính bạn.
""",
)

write_lesson(
    M6, L6C,
    "Streaming Large Data",
    "Process files line by line — constant memory via iteration and generators.",
    13,
    """
`read_text()` loads everything. For a 10 GB export that's a crash. The
streaming pattern reads **one unit at a time**:

```python
from pathlib import Path

total = 0
with Path("huge.log").open(encoding="utf-8") as f:
    for line in f:                  # file objects iterate lazily, line by line
        total += len(line)
```

The file object **is** an iterator (module 3!), so it composes with
generators into pipelines that never hold more than one line plus your
accumulators:

```python
def errors(lines):
    for line in lines:
        if line.startswith("ERROR:"):
            yield line.strip()

def short_errors(lines, limit=50):
    for line in errors(lines):
        if len(line) <= limit:
            yield line

with Path("app.log").open(encoding="utf-8") as f:
    first_five = [e for e, _ in zip(short_errors(f), range(5))]
```

## Chunked binary reads

Non-text files (backups, media) stream in **chunks**:

```python
def copy_in_chunks(src, dst, chunk=64 * 1024):
    with open(src, "rb") as a, open(dst, "wb") as b:
        while block := a.read(chunk):
            b.write(block)
```

The walrus `while block := read()` idiom reads until the empty bytes signal
the end. Memory stays at one chunk, no matter the file size.
""",
    "Stream Dữ liệu Lớn",
    "Xử lý tệp theo từng dòng — bộ nhớ hằng số nhờ lặp và generator.",
    """
`read_text()` nạp tất cả. Với file xuất 10 GB, đó là một crash. Mẫu streaming
đọc **một đơn vị mỗi lần**:

```python
from pathlib import Path

total = 0
with Path("huge.log").open(encoding="utf-8") as f:
    for line in f:                  # đối tượng tệp lặp lười biếng, từng dòng
        total += len(line)
```

Đối tượng tệp **chính là** một iterator (module 3!), nên nó ghép được với
generator thành pipeline không bao giờ giữ nhiều hơn một dòng cộng các biến
tích lũy:

```python
def errors(lines):
    for line in lines:
        if line.startswith("ERROR:"):
            yield line.strip()

def short_errors(lines, limit=50):
    for line in errors(lines):
        if len(line) <= limit:
            yield line

with Path("app.log").open(encoding="utf-8") as f:
    first_five = [e for e, _ in zip(short_errors(f), range(5))]
```

## Đọc nhị phân theo chunk

Tệp không phải văn bản (backup, media) stream theo **chunk**:

```python
def copy_in_chunks(src, dst, chunk=64 * 1024):
    with open(src, "rb") as a, open(dst, "wb") as b:
        while block := a.read(chunk):
            b.write(block)
```

Cú pháp `while block := read()` đọc cho đến khi bytes rỗng báo hiệu kết thúc.
Bộ nhớ luôn ở mức một chunk, bất kể kích thước tệp.
""",
)

# --- module 6 practice sets ---
write_practice(
    M6, "m6-path-practice",
    "pathlib Drills",
    "Navigate, match, and organize paths as objects.",
    "Luyện pathlib",
    "Điều hướng, so mẫu, và tổ chức đường dẫn như đối tượng.",
    L6A, 25, "intermediate",
    [
        challenge(
            "pi6-path-parts", "Path Anatomy",
            "Implement file_info(p) receiving a Path and returning a dict with keys name, stem, suffix, and parent (as str).",
            "from pathlib import Path\n\ndef file_info(p):\n    pass\n",
            [
                ("splits a report path",
                 "from pathlib import Path\ninfo = file_info(Path('data/reports/q1.csv'))\nassert info['name'] == 'q1.csv'\nassert info['stem'] == 'q1'\nassert info['suffix'] == '.csv'",
                 "name/stem/suffix come straight from the Path API."),
                ("parent is the folder",
                 "from pathlib import Path\nassert str(file_info(Path('data/reports/q1.csv'))['parent']).endswith('reports')",
                 "parent is a Path — convert with str()."),
            ],
            level="imitation",
        ),
        challenge(
            "pi6-path-organize", "Group by Extension",
            "Implement by_suffix(paths) returning a dict mapping suffix (including the dot, lowercase) to a sorted list of path names. Files without a suffix go under ''.",
            "from pathlib import Path\n\ndef by_suffix(paths):\n    pass\n",
            [
                ("groups by suffix",
                 "ps = [Path('a.txt'), Path('b.py'), Path('c.txt')]\nassert by_suffix(ps) == {'.py': ['b.py'], '.txt': ['a.txt', 'c.txt']}",
                 "Group by p.suffix; sort each list."),
                ("no suffix bucket",
                 "ps = [Path('LICENSE'), Path('a.txt')]\nassert by_suffix(ps)[''] == ['LICENSE']",
                 "p.suffix is '' when there is no extension."),
            ],
            level="guided",
        ),
        challenge(
            "pi6-path-traversal", "Escape-Proof Join",
            "Implement safe_join(base: str, user_path: str) that joins base with user_path and raises ValueError if the resolved result escapes base (classic directory-traversal defense). Return the joined Path on success.",
            "from pathlib import Path\n\ndef safe_join(base, user_path):\n    pass\n",
            [
                ("normal subpath allowed",
                 "from pathlib import Path\nresult = safe_join('/srv/data', 'reports/q1.csv')\nassert str(result).endswith('reports/q1.csv')",
                 "Resolve and check containment."),
                ("traversal attempt rejected",
                 "try:\n    safe_join('/srv/data', '../../etc/passwd')\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
                 "resolve() collapses '..' — then verify the result is under the resolved base."),
            ],
            level="combination",
        ),
    ],
    {
        "pi6-path-parts": vi_challenge("Giải phẫu Path", "Viết file_info(p) nhận một Path và trả về dict với các key name, stem, suffix, và parent (dạng str).", [("Tách một đường dẫn báo cáo", "name/stem/suffix lấy thẳng từ API của Path."), ("parent là thư mục cha", "parent là một Path — chuyển bằng str().")]),
        "pi6-path-organize": vi_challenge("Gom theo phần mở rộng", "Viết by_suffix(paths) trả về dict ánh xạ suffix (gồm dấu chấm, chữ thường) tới list tên đường dẫn đã sắp. Tệp không có suffix nằm dưới key ''.", [("Gom theo suffix", "Gom theo p.suffix; sắp từng list."), ("Nhóm không có suffix", "p.suffix là '' khi không có phần mở rộng.")]),
        "pi6-path-traversal": vi_challenge("Chống thoát thư mục", "Viết safe_join(base: str, user_path: str) nối base với user_path và raise ValueError nếu kết quả sau khi resolve vượt ra ngoài base (phòng thủ directory-traversal kinh điển). Trả về Path đã nối khi thành công.", [("Đường dẫn con hợp lệ được chấp nhận", "Resolve rồi kiểm tra sự chứa đựng."), ("Nỗ lực traversal bị từ chối", "resolve() thu gọn '..' — sau đó xác minh kết quả nằm dưới base đã resolve.")]),
    },
    solutions=[
        ("pi6-path-parts", "from pathlib import Path\n\ndef file_info(p):\n    return {\n        'name': p.name,\n        'stem': p.stem,\n        'suffix': p.suffix,\n        'parent': str(p.parent),\n    }", "from pathlib import Path\n\ndef file_info(p):\n    parts = str(p).split('/')\n    name = parts[-1]\n    return {'name': name, 'stem': name, 'suffix': '', 'parent': '/'.join(parts[:-1])}"),
        ("pi6-path-organize", "from pathlib import Path\n\ndef by_suffix(paths):\n    groups = {}\n    for p in paths:\n        groups.setdefault(p.suffix.lower(), []).append(p.name)\n    return {s: sorted(names) for s, names in groups.items()}", "from pathlib import Path\n\ndef by_suffix(paths):\n    groups = {}\n    for p in paths:\n        groups.setdefault(p.suffix, []).append(p.name)\n    return {s: names for s, names in groups.items()}"),
        ("pi6-path-traversal", "from pathlib import Path\n\ndef safe_join(base, user_path):\n    base_resolved = Path(base).resolve()\n    candidate = (base_resolved / user_path).resolve()\n    if not str(candidate).startswith(str(base_resolved)):\n        raise ValueError('path escapes base directory')\n    return candidate", "from pathlib import Path\n\ndef safe_join(base, user_path):\n    return Path(base) / user_path"),
    ],
)

write_practice(
    M6, "m6-serial-practice",
    "Round-Trip Drills",
    "Serialize, deserialize, and validate at the edges.",
    "Luyện Khép vòng",
    "Tuần tự hóa, giải tuần tự, và kiểm tra hợp lệ tại ranh giới.",
    L6B, 30, "intermediate",
    [
        challenge(
            "pi6-json-roundtrip", "JSON Round-Trip",
            "Implement save_records(records, path) writing a JSON list (ensure_ascii=False) and load_records(path) reading it back. Both use UTF-8 explicitly.",
            "import json\nfrom pathlib import Path\n\ndef save_records(records, path):\n    pass\n\ndef load_records(path):\n    pass\n",
            [
                ("round-trips unicode safely",
                 "from pathlib import Path\nimport tempfile, os\nrecords = [{'name': 'Minh', 'note': 'xin chào'}]\np = Path(tempfile.mkdtemp()) / 'rec.json'\nsave_records(records, p)\nassert load_records(p) == records",
                 "write_text(encoding='utf-8') + json.dumps(ensure_ascii=False)."),
                ("file content is valid JSON",
                 "from pathlib import Path\nimport tempfile, json\np = Path(tempfile.mkdtemp()) / 'r.json'\nsave_records([{'a': 1}], p)\nassert json.loads(p.read_text(encoding='utf-8')) == [{'a': 1}]",
                 "The file itself must parse as JSON."),
            ],
            level="guided",
        ),
        challenge(
            "pi6-csv-rows", "CSV In, Dicts Out",
            "Implement parse_csv(text) receiving raw CSV text (with a header row) and returning a list of dicts. Then implement to_csv_text(rows, fieldnames) doing the reverse. Use csv module round-trip via io.StringIO.",
            "import csv, io\n\ndef parse_csv(text):\n    pass\n\ndef to_csv_text(rows, fieldnames):\n    pass\n",
            [
                ("parses header + rows",
                 "text = 'name,age\\nAn,30\\nBinh,25'\nrows = parse_csv(text)\nassert rows == [{'name': 'An', 'age': '30'}, {'name': 'Binh', 'age': '25'}]",
                 "csv.DictReader over io.StringIO(text)."),
                ("writes back the same shape",
                 "rows = [{'name': 'An', 'age': '30'}]\nout = to_csv_text(rows, ['name', 'age'])\nassert 'name,age' in out and 'An,30' in out",
                 "DictWriter over io.StringIO; writeheader first."),
                ("round-trip identity",
                 "text = 'name,age\\nAn,30'\nassert to_csv_text(parse_csv(text), ['name', 'age']).strip().replace(chr(13), '') == text",
                 "A faithful round-trip reproduces the original text."),
            ],
            level="independent",
        ),
        challenge(
            "pi6-validate-payload", "Boundary Validation",
            "Implement load_users(path) that reads a JSON file and VALIDATES: must be a list of dicts, each with string 'name' and int 'age' >= 0. Raise ValidationError listing the first problem found; return cleaned dicts otherwise.",
            "import json\nfrom pathlib import Path\n\nclass ValidationError(Exception):\n    pass\n\ndef load_users(path):\n    pass\n",
            [
                ("valid data passes",
                 "from pathlib import Path\nimport tempfile\np = Path(tempfile.mkdtemp()) / 'u.json'\np.write_text('[{\"name\": \"An\", \"age\": 30}]', encoding='utf-8')\nassert load_users(p) == [{'name': 'An', 'age': 30}]",
                 "Check list-of-dicts, name str, age int >= 0."),
                ("bad shape raises with a reason",
                 "from pathlib import Path\nimport tempfile\np = Path(tempfile.mkdtemp()) / 'bad.json'\np.write_text('[{\"name\": \"An\", \"age\": -5}]', encoding='utf-8')\ntry:\n    load_users(p)\n    failed = False\nexcept ValidationError:\n    failed = True\nassert failed",
                 "Negative age violates the contract — raise ValidationError."),
                ("non-list raises",
                 "from pathlib import Path\nimport tempfile\np = Path(tempfile.mkdtemp()) / 'x.json'\np.write_text('{\"name\": \"An\"}', encoding='utf-8')\ntry:\n    load_users(p)\n    failed = False\nexcept ValidationError:\n    failed = True\nassert failed",
                 "Top level must be a list."),
            ],
            level="combination",
        ),
    ],
    {
        "pi6-json-roundtrip": vi_challenge("Khép vòng JSON", "Viết save_records(records, path) ghi một list JSON (ensure_ascii=False) và load_records(path) đọc lại. Cả hai dùng UTF-8 tường minh.", [("Khép vòng unicode an toàn", "write_text(encoding='utf-8') + json.dumps(ensure_ascii=False)."), ("Nội dung tệp là JSON hợp lệ", "Bản thân tệp phải parse được bằng JSON.")]),
        "pi6-csv-rows": vi_challenge("CSV vào, Dict ra", "Viết parse_csv(text) nhận văn bản CSV thô (có dòng tiêu đề) và trả về list các dict. Sau đó viết to_csv_text(rows, fieldnames) làm chiều ngược lại. Dùng module csv khép vòng qua io.StringIO.", [("Phân tích tiêu đề + dòng", "csv.DictReader trên io.StringIO(text)."), ("Ghi lại cùng hình dạng", "DictWriter trên io.StringIO; ghi writeheader trước."), ("Khép vòng đúng bản sắc", "Vòng khép trung thực tái tạo đúng văn bản gốc.")]),
        "pi6-validate-payload": vi_challenge("Kiểm tra dữ liệu tại ranh giới", "Viết load_users(path) đọc một tệp JSON và KIỂM TRA: phải là list gồm dict, mỗi dict có 'name' là chuỗi và 'age' là int >= 0. Raise ValidationError nêu vấn đề đầu tiên tìm thấy; ngược lại trả về các dict đã làm sạch.", [("Dữ liệu hợp lệ đi qua", "Kiểm tra list-of-dicts, name str, age int >= 0."), ("Dữ liệu sai hình raise kèm lý do", "Tuổi âm vi phạm hợp đồng — raise ValidationError."), ("Không phải list sẽ raise", "Cấp trên cùng phải là list.")]),
    },
    solutions=[
        ("pi6-json-roundtrip", "import json\nfrom pathlib import Path\n\ndef save_records(records, path):\n    Path(path).write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')\n\ndef load_records(path):\n    return json.loads(Path(path).read_text(encoding='utf-8'))", "import json\nfrom pathlib import Path\n\ndef save_records(records, path):\n    Path(path).write_text(str(records), encoding='utf-8')\n\ndef load_records(path):\n    return json.loads(Path(path).read_text(encoding='utf-8'))"),
        ("pi6-csv-rows", "import csv, io\n\ndef parse_csv(text):\n    return list(csv.DictReader(io.StringIO(text)))\n\ndef to_csv_text(rows, fieldnames):\n    buf = io.StringIO()\n    writer = csv.DictWriter(buf, fieldnames=fieldnames)\n    writer.writeheader()\n    writer.writerows(rows)\n    return buf.getvalue()", "import csv, io\n\ndef parse_csv(text):\n    lines = text.splitlines()\n    header = lines[0].split(',')\n    return [dict(zip(header, l.split(','))) for l in lines[1:]]\n\ndef to_csv_text(rows, fieldnames):\n    return ','.join(fieldnames) + chr(10) + chr(10).join(','.join(str(r[f]) for f in fieldnames) for r in rows)"),
        ("pi6-validate-payload", "import json\nfrom pathlib import Path\n\nclass ValidationError(Exception):\n    pass\n\ndef load_users(path):\n    data = json.loads(Path(path).read_text(encoding='utf-8'))\n    if not isinstance(data, list):\n        raise ValidationError('expected a list of users')\n    for i, item in enumerate(data):\n        if not isinstance(item, dict):\n            raise ValidationError(f'user {i} is not an object')\n        if not isinstance(item.get('name'), str):\n            raise ValidationError(f'user {i}: name must be a string')\n        age = item.get('age')\n        if not isinstance(age, int) or isinstance(age, bool) or age < 0:\n            raise ValidationError(f'user {i}: age must be a non-negative int')\n    return data", "import json\nfrom pathlib import Path\n\nclass ValidationError(Exception):\n    pass\n\ndef load_users(path):\n    data = json.loads(Path(path).read_text(encoding='utf-8'))\n    if not isinstance(data, list):\n        raise ValidationError('expected a list of users')\n    return data"),
    ],
)

write_practice(
    M6, "m6-stream-practice",
    "Streaming Drills",
    "Process big inputs at constant memory.",
    "Luyện Streaming",
    "Xử lý input lớn với bộ nhớ hằng số.",
    L6C, 25, "intermediate",
    [
        challenge(
            "pi6-stream-longest", "Longest Line, Streaming",
            "Implement longest_line(path) returning the longest line (stripped of the trailing newline) of a text file WITHOUT loading the whole file — iterate lazily. Empty file returns ''.",
            "from pathlib import Path\n\ndef longest_line(path):\n    pass\n",
            [
                ("finds the longest",
                 "from pathlib import Path\nimport tempfile\np = Path(tempfile.mkdtemp()) / 'log.txt'\np.write_text('short' + chr(10) + 'a much longer line here' + chr(10) + 'mid', encoding='utf-8')\nassert longest_line(p) == 'a much longer line here'",
                 "Track the max while iterating the file object directly."),
                ("empty file",
                 "from pathlib import Path\nimport tempfile\np = Path(tempfile.mkdtemp()) / 'empty.txt'\np.write_text('', encoding='utf-8')\nassert longest_line(p) == ''",
                 "No lines → default ''."),
            ],
            level="guided",
        ),
        challenge(
            "pi6-stream-pipeline", "Streaming Word Count",
            "Implement count_words(paths) where paths is a list of text files. Stream every file line by line (never read_text the whole file) and return the total count of whitespace-separated tokens across all files.",
            "from pathlib import Path\n\ndef count_words(paths):\n    pass\n",
            [
                ("counts across files",
                 "from pathlib import Path\nimport tempfile\nd = Path(tempfile.mkdtemp())\na = d / 'a.txt'; a.write_text('one two three', encoding='utf-8')\nb = d / 'b.txt'; b.write_text('four' + chr(10) + 'five six', encoding='utf-8')\nassert count_words([a, b]) == 6",
                 "Iterate each file line by line; split and accumulate."),
                ("empty files contribute zero",
                 "from pathlib import Path\nimport tempfile\np = Path(tempfile.mkdtemp()) / 'e.txt'; p.write_text('', encoding='utf-8')\nassert count_words([p]) == 0",
                 "No tokens in an empty stream."),
            ],
            level="independent",
        ),
        challenge(
            "pi6-stream-chunks", "Chunked Checksum",
            "Implement file_hash(path) computing the SHA-256 hex digest of a file by reading it in 64 KB chunks (never the whole file). Return the hexdigest string.",
            "import hashlib\n\ndef file_hash(path):\n    pass\n",
            [
                ("digest of known content",
                 "import tempfile\nfrom pathlib import Path\np = Path(tempfile.mkdtemp()) / 'f.bin'\np.write_bytes(b'hello world')\nimport hashlib\nassert file_hash(p) == hashlib.sha256(b'hello world').hexdigest()",
                 "h.update(chunk) in a loop, then h.hexdigest()."),
                ("empty file has the empty digest",
                 "import hashlib, tempfile\nfrom pathlib import Path\np = Path(tempfile.mkdtemp()) / 'e.bin'\np.write_bytes(b'')\nassert file_hash(p) == hashlib.sha256(b'').hexdigest()",
                 "Zero chunks still produce a valid digest."),
            ],
            level="combination",
        ),
    ],
    {
        "pi6-stream-longest": vi_challenge("Dòng dài nhất, dạng stream", "Viết longest_line(path) trả về dòng dài nhất (đã bỏ ký tự xuống dòng) của một tệp văn bản MÀ không nạp cả tệp — lặp lười biếng. Tệp rỗng trả về ''.", [("Tìm dòng dài nhất", "Theo dõi max trong khi lặp trực tiếp đối tượng tệp."), ("Tệp rỗng", "Không có dòng → trả ''.")]),
        "pi6-stream-pipeline": vi_challenge("Đếm từ dạng stream", "Viết count_words(paths) với paths là list các tệp văn bản. Stream từng tệp theo dòng (không bao giờ read_text cả tệp) và trả về tổng số token phân tách bởi khoảng trắng trên mọi tệp.", [("Đếm trên nhiều tệp", "Lặp từng tệp theo dòng; split và tích lũy."), ("Tệp rỗng đóng góp 0", "Không token trong stream rỗng.")]),
        "pi6-stream-chunks": vi_challenge("Checksum theo chunk", "Viết file_hash(path) tính digest SHA-256 dạng hex của một tệp bằng cách đọc theo chunk 64 KB (không bao giờ đọc cả tệp). Trả về chuỗi hexdigest.", [("Digest của nội dung đã biết", "h.update(chunk) trong vòng lặp, rồi h.hexdigest()."), ("Tệp rỗng vẫn có digest", "Không chunk nào vẫn cho digest hợp lệ.")]),
    },
    solutions=[
        ("pi6-stream-longest", "from pathlib import Path\n\ndef longest_line(path):\n    best = ''\n    with Path(path).open(encoding='utf-8') as f:\n        for line in f:\n            line = line.rstrip(chr(10))\n            if len(line) > len(best):\n                best = line\n    return best", "from pathlib import Path\n\ndef longest_line(path):\n    lines = Path(path).read_text(encoding='utf-8').splitlines()\n    return max(lines, key=len) if lines else ''"),
        ("pi6-stream-pipeline", "from pathlib import Path\n\ndef count_words(paths):\n    total = 0\n    for path in paths:\n        with Path(path).open(encoding='utf-8') as f:\n            for line in f:\n                total += len(line.split())\n    return total", "from pathlib import Path\n\ndef count_words(paths):\n    total = 0\n    for path in paths:\n        total += len(Path(path).read_text(encoding='utf-8').split())\n    return total"),
        ("pi6-stream-chunks", "import hashlib\n\ndef file_hash(path):\n    h = hashlib.sha256()\n    with open(path, 'rb') as f:\n        while block := f.read(64 * 1024):\n            h.update(block)\n    return h.hexdigest()", "import hashlib\n\ndef file_hash(path):\n    h = hashlib.sha256()\n    with open(path, 'rb') as f:\n        h.update(f.read())\n    return h.hexdigest()"),
    ],
)

# --- module 6 checkpoint ---
write_checkpoint(
    M6, L6D,
    "Checkpoint: Data Processing Pipeline",
    "Read, validate, transform, and aggregate a real-shaped dataset.",
    20,
    """
Everything in this module converges here: parse structured records, validate
them, transform, aggregate, and report — the pipeline shape of every data
script worth keeping.

**Working with AI:** ask the mentor to red-team your validation ("what input
breaks this?") — boundary failures are where data pipelines actually die.
""",
    "Checkpoint: Pipeline xử lý dữ liệu",
    "Đọc, kiểm tra, biến đổi, và tổng hợp một tập dữ liệu hình dạng thật.",
    """
Mọi thứ trong module này hội tụ tại đây: parse bản ghi có cấu trúc, kiểm tra
hợp lệ, biến đổi, tổng hợp, và báo cáo — hình dạng pipeline của mọi data
script đáng giữ lại.

**Làm việc cùng AI:** nhờ mentor red-team phần kiểm tra hợp lệ của bạn
("input nào sẽ làm hỏng cái này?") — lỗi ranh giới là nơi pipeline dữ liệu
thực sự chết.
""",
    challenge(
        "pi6-ckpt-pipeline", "Sales Report Pipeline",
        "Implement report(sales) where sales is a list of dicts with keys 'region' (str) and 'amount' (int, may be negative for refunds). Return a dict mapping region to total amount, but ONLY include regions with a positive total. Also implement is_valid(sale) returning True only for dicts with str region and int amount (no bools).",
        "def is_valid(sale):\n    pass\n\ndef report(sales):\n    pass\n",
        [
            ("validator shape-checks",
             "assert is_valid({'region': 'east', 'amount': 5}) is True\nassert is_valid({'region': 3, 'amount': 5}) is False\nassert is_valid({'region': 'east', 'amount': True}) is False",
             "str region; int amount that is not a bool."),
            ("aggregates by region",
             "sales = [{'region': 'east', 'amount': 10}, {'region': 'west', 'amount': 4}, {'region': 'east', 'amount': 6}]\nassert report(sales) == {'east': 16, 'west': 4}",
             "Sum amounts per region."),
            ("non-positive totals excluded",
             "sales = [{'region': 'east', 'amount': 5}, {'region': 'west', 'amount': -9}]\nassert report(sales) == {'east': 5}",
             "Refund-heavy regions drop out entirely."),
            ("skips invalid rows",
             "sales = [{'region': 'east', 'amount': 5}, {'region': 'x'}, None]\nassert report(sales) == {'east': 5}",
             "Use is_valid to filter before aggregating."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Pipeline báo cáo bán hàng",
        "Viết report(sales) với sales là list các dict có key 'region' (str) và 'amount' (int, có thể âm cho hoàn tiền). Trả về dict ánh xạ region tới tổng amount, CHỈ gồm các region có tổng dương. Đồng thời viết is_valid(sale) trả True chỉ khi dict có region là str và amount là int (không phải bool).",
        [
            ("Bộ kiểm tra soi hình dạng", "region là str; amount là int và không phải bool."),
            ("Tổng hợp theo region", "Cộng amount theo từng region."),
            ("Loại tổng không dương", "Region nhiều hoàn tiền biến mất hoàn toàn."),
            ("Bỏ qua dòng không hợp lệ", "Dùng is_valid để lọc trước khi tổng hợp."),
        ],
    ),
    solution="def is_valid(sale):\n    return (\n        isinstance(sale, dict)\n        and isinstance(sale.get('region'), str)\n        and isinstance(sale.get('amount'), int)\n        and not isinstance(sale.get('amount'), bool)\n    )\n\ndef report(sales):\n    totals = {}\n    for sale in sales:\n        if is_valid(sale):\n            totals[sale['region']] = totals.get(sale['region'], 0) + sale['amount']\n    return {region: total for region, total in totals.items() if total > 0}",
    wrong="def is_valid(sale):\n    return (\n        isinstance(sale, dict)\n        and isinstance(sale.get('region'), str)\n        and isinstance(sale.get('amount'), int)\n    )\n\ndef report(sales):\n    totals = {}\n    for sale in sales:\n        totals[sale['region']] = totals.get(sale['region'], 0) + sale['amount']\n    return {region: total for region, total in totals.items() if total > 0}",
)

print("module 6 done")
