#!/usr/bin/env python3
"""Python Intermediate — module 11 (packaging) + capstone module (capstone-cli-app)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 11: packaging ============================
M11 = "packaging"
L11A = "pyproject-layout"
L11B = "console-entry-points"
L11C = "venv-lockfiles"
L11D = "security-audit"
L11E = "checkpoint-ship"

write_module(
    M11,
    "Packaging and Professional Workflow",
    "Ship installable tools: pyproject.toml, entry points, reproducible envs — and a security audit.",
    "Đóng gói và Quy trình Chuyên nghiệp",
    "Đóng gói công cụ cài đặt được: pyproject.toml, entry point, môi trường tái lập — và một buổi audit an ninh.",
    [L11A, L11B, L11C, L11D, L11E],
    ["m11-pyproject-practice", "m11-entry-practice", "m11-security-practice"],
)

write_lesson(
    M11, L11A,
    "pyproject.toml: The Project Contract",
    "Metadata, dependencies, and build config in one standardized file.",
    14,
    """
Every modern Python project declares itself in **pyproject.toml** (TOML —
read it in the sandbox with `tomllib`):

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "tasknoter"
version = "0.1.0"
description = "A typed, tested task manager"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
tasknoter = "tasknoter.cli:main"
```

What each block promises:

- **build-system** — which tool turns this into an installable package (setuptools here; alternatives exist).
- **project** — identity: name, version, supported Python, and **dependencies** with version constraints (`requests>=2.31,<3`).
- **project.scripts** — console commands to generate (next lesson).

`requires-python` is a promise to your users: the tool refuses to install on
older interpreters. Versioning your *own* project with semver-like bumps
(0.1.0 → 0.2.0 for features, +0.0.1 for fixes) is the cheapest coordination
tool you will ever adopt.

On your own machine, `pip install -e .` installs the project in **editable
mode** — the sandbox can't run pip (no network), so this course verifies the
*file* is well-formed instead.
""",
    "pyproject.toml: Bản hợp đồng của dự án",
    "Metadata, phụ thuộc, và cấu hình build trong một tệp chuẩn hóa duy nhất.",
    """
Mọi dự án Python hiện đại tuyên bố mình trong **pyproject.toml** (TOML —
đọc được trong sandbox bằng `tomllib`):

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "tasknoter"
version = "0.1.0"
description = "A typed, tested task manager"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
tasknoter = "tasknoter.cli:main"
```

Mỗi khối hứa điều gì:

- **build-system** — công cụ nào biến dự án thành gói cài được (setuptools ở đây; còn lựa chọn khác).
- **project** — danh tính: tên, phiên bản, Python được hỗ trợ, và **dependencies** với ràng buộc phiên bản (`requests>=2.31,<3`).
- **project.scripts** — các lệnh console sẽ được sinh ra (bài kế tiếp).

`requires-python` là một lời hứa với người dùng: công cụ từ chối cài trên
interpreter cũ hơn. Tự đánh phiên bản cho dự án của bạn theo kiểu semver
(0.1.0 → 0.2.0 cho tính năng, +0.0.1 cho sửa lỗi) là công cụ phối hợp rẻ
nhất bạn từng có.

Trên máy riêng, `pip install -e .` cài dự án ở **chế độ editable** — sandbox
không chạy được pip (không có mạng), nên khóa học này kiểm chứng *tệp* đúng
chuẩn thay vì vậy.
""",
)

write_lesson(
    M11, L11B,
    "Console Entry Points",
    "Turn a module into a command users type — the last mile of shipping.",
    12,
    """
The `[project.scripts]` line `tasknoter = "tasknoter.cli:main"` tells
installers: create a command `tasknoter` that imports `tasknoter.cli` and
calls `main()`. Your `main` receives **no arguments** — it reads sys.argv
(usually via `argparse` from your Beginner course):

```python
# src/tasknoter/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser(prog="tasknoter")
    parser.add_argument("command", choices=["add", "list", "done"])
    parser.add_argument("text", nargs="?")
    args = parser.parse_args()
    if args.command == "add" and args.text:
        print(f"added: {args.text}")
    elif args.command == "list":
        print("listing...")

if __name__ == "__main__":
    main()
```

Professional CLI manners: **exit codes matter** (0 = success, non-zero =
failure — `raise SystemExit(2)` or `sys.exit(2)`), errors go to **stderr**
(`print(..., file=sys.stderr)`), and `--help` is generated for you. Scripts
that respect these compose cleanly with other tools.

The capstone asks for exactly this shape: a `main()` that dispatches
subcommands to your storage and service layers.
""",
    "Console Entry Point",
    "Biến một module thành lệnh người dùng gõ — chặng cuối của việc đóng gói.",
    """
Dòng `[project.scripts]` là `tasknoter = "tasknoter.cli:main"` báo cho bộ
cài đặt: tạo lệnh `tasknoter` import `tasknoter.cli` và gọi `main()`.
`main` của bạn nhận **không tham số** — nó đọc sys.argv (thường qua
`argparse` từ khóa Beginner):

```python
# src/tasknoter/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser(prog="tasknoter")
    parser.add_argument("command", choices=["add", "list", "done"])
    parser.add_argument("text", nargs="?")
    args = parser.parse_args()
    if args.command == "add" and args.text:
        print(f"added: {args.text}")
    elif args.command == "list":
        print("listing...")

if __name__ == "__main__":
    main()
```

Phép lịch sự CLI chuyên nghiệp: **exit code quan trọng** (0 = thành công,
khác 0 = thất bại — `raise SystemExit(2)` hoặc `sys.exit(2)`), lỗi đi ra
**stderr** (`print(..., file=sys.stderr)`), và `--help` được sinh sẵn. CLI
tôn trọng những điều này ghép mượt với các công cụ khác.

Capstone đòi đúng hình dạng này: một `main()` điều phối subcommand xuống các
tầng storage và service của bạn.
""",
)

write_lesson(
    M11, L11C,
    "Environments and Lockfiles",
    "Isolation with venv, and reproducibility beyond requirements.txt.",
    12,
    """
Your Beginner course used `venv` + `pip install` + `requirements.txt`.
Intermediate adds the *why* and the *reproducibility* layer:

- **venv isolates per-project** so package versions can't clash between projects and your system Python stays clean. Never `pip install` globally.
- **requirements.txt pins what you install**, but it says nothing about *which* builds your builds depend on (transitive pins).
- **Lockfiles** (`pip-compile` output, `uv.lock`, `pdm.lock`) record the full resolved graph so that today's install and next year's install are byte-identical. Rule: hand-edit constraints in `pyproject.toml`; let a lockfile freeze reality.

The professional flow: constraints live in `pyproject.toml` (loose, readable:
`httpx>=0.27`), the lockfile is generated and committed (exact), and CI
installs from the lockfile so tests run against what production runs.

In this sandbox there is no network and no pip — so the gradable skill here
is *reasoning about the files*: reading dependency declarations, spotting
unpinned ranges, and writing a lockfile-aware workflow. The next lesson's
audit drills exactly that.
""",
    "Môi trường ảo và Lockfile",
    "Cách ly với venv, và tái lập được vượt beyond requirements.txt.",
    """
Khóa Beginner của bạn đã dùng `venv` + `pip install` + `requirements.txt`.
Intermediate thêm phần *vì sao* và tầng *tái lập*:

- **venv cách ly theo từng dự án** để phiên bản gói không xung đột giữa các dự án và Python hệ thống giữ sạch. Không bao giờ `pip install` toàn cục.
- **requirements.txt ghim những gì bạn cài**, nhưng không nói gì về *các bản build mà build của bạn phụ thuộc* (pin bậc thang).
- **Lockfile** (kết quả `pip-compile`, `uv.lock`, `pdm.lock`) ghi lại toàn bộ đồ thị đã phân giải để bản cài hôm nay và năm sau giống hệt nhau. Quy tắc: sửa ràng buộc trong `pyproject.toml` (lỏng, dễ đọc: `httpx>=0.27`); để lockfile đóng băng thực tế.

Quy trình chuyên nghiệp: ràng buộc sống trong `pyproject.toml`, lockfile được
sinh ra và commit (chính xác), và CI cài từ lockfile để test chạy trên đúng
thứ production chạy.

Sandbox này không có mạng và không có pip — nên kỹ năng được chấm ở đây là
*suy luận về các tệp*: đọc khai báo phụ thuộc, phát hiện dải chưa ghim, và
viết quy trình biết-dùng-lockfile. Buổi audit ở bài kế tiếp luyện đúng điều đó.
""",
)

write_lesson(
    M11, L11D,
    "The Security Audit Mindset",
    "Deserialization, shell injection, and secrets — find them, then fix them.",
    15,
    """
Security for intermediates is a habit of **mistrusting inputs and defaults**.
Three bugs cover most of what you'll meet:

## 1. Unsafe deserialization

```python
# NEVER on data from users/network:
import pickle
obj = pickle.loads(blob)          # executing attacker-chosen code

# YES for untrusted data:
import json
obj = json.loads(text)            # data only, no code execution
```

## 2. Shell injection

```python
# NEVER:
import subprocess
subprocess.run(f"convert {filename}.png", shell=True)   # filename='x; rm -rf ~'

# YES:
import shlex, subprocess
subprocess.run(["convert", f"{filename}.png"])          # argv list, no shell
```

The list form never lets metacharacters through; `shlex.quote()`/`shlex.join()`
are for the rare case you truly need a shell string.

## 3. Secrets and paths

Secrets come from **environment variables** (`os.environ["API_KEY"]`), never
hard-coded and never logged. User-supplied paths go through the
`safe_join` discipline from module 6 (resolve + containment check).

## Audit method

Read code asking one question: **what input can reach this line, and what is
the worst thing it can do there?** The practice set gives you vulnerable
functions to repair — the same exercise security reviewers run on real PRs.
""",
    "Tư duy Audit An ninh",
    "Deserialization, shell injection, và secrets — tìm ra, rồi sửa.",
    """
An ninh cho trình trung cấp là thói quen **hoài nghi input và mặc định**.
Ba lỗi phủ phần lớn điều bạn sẽ gặp:

## 1. Deserialization không an toàn

```python
# KHÔNG BAO GIỜ với dữ liệu từ người dùng/mạng:
import pickle
obj = pickle.loads(blob)          # chạy code do kẻ tấn công chọn

# CÓ cho dữ liệu không tin cậy:
import json
obj = json.loads(text)            # chỉ dữ liệu, không thực thi code
```

## 2. Shell injection

```python
# KHÔNG BAO GIỜ:
import subprocess
subprocess.run(f"convert {filename}.png", shell=True)   # filename='x; rm -rf ~'

# CÓ:
import shlex, subprocess
subprocess.run(["convert", f"{filename}.png"])          # argv dạng list, không shell
```

Dạng list không bao giờ cho ký tự đặc biệt lọt qua; `shlex.quote()`/`shlex.join()`
dành cho trường hợp hiếm bạn thật sự cần chuỗi shell.

## 3. Secrets và đường dẫn

Secrets đến từ **biến môi trường** (`os.environ["API_KEY"]`), không bao giờ
hard-code và không bao giờ log. Đường dẫn do người dùng cung cấp đi qua kỷ
luật `safe_join` của module 6 (resolve + kiểm tra chứa đựng).

## Phương pháp audit

Đọc code với một câu hỏi: **input nào có thể chạm dòng này, và điều tồi tệ
nhất nó có thể làm ở đó là gì?** Bộ luyện tập dưới đây đưa cho bạn các hàm
dễ tổn thương để sửa — đúng bài tập mà người review an ninh chạy trên PR thật.
""",
)

# --- module 11 practice sets ---
write_practice(
    M11, "m11-pyproject-practice",
    "pyproject.toml Drills",
    "Read and validate project contracts with tomllib.",
    "Luyện pyproject.toml",
    "Đọc và xác thực bản hợp đồng dự án bằng tomllib.",
    L11A, 25, "intermediate",
    [
        challenge(
            "pi11-py-read", "Read the Contract",
            "Implement read_project(pyproject_text) that parses TOML text (tomllib.loads) and returns a dict with keys name, version, and scripts (the [project.scripts] table).",
            "import tomllib\n\ndef read_project(pyproject_text):\n    pass\n",
            [
                ("extracts identity",
                 "text = '''[project]\\nname = \"toolkit\"\\nversion = \"1.2.0\"\\n\\n[project.scripts]\\ntoolkit = \"toolkit.cli:main\"'''\ninfo = read_project(text)\nassert info['name'] == 'toolkit'\nassert info['version'] == '1.2.0'\nassert info['scripts'] == {'toolkit': 'toolkit.cli:main'}",
                 "tomllib.loads then navigate ['project'] and ['project']['scripts']."),
                ("missing scripts yields empty dict",
                 "text = '[project]\\nname = \"x\"\\nversion = \"0.0.1\"'\nassert read_project(text)['scripts'] == {}",
                 "Use .get with a default — absence is normal."),
            ],
            level="guided",
        ),
        challenge(
            "pi11-py-validate", "Contract Validator",
            "Implement validate_project(pyproject_text) returning a list of problem strings for a pyproject: missing [project], missing name, missing version, and any dependency without a version constraint (a bare package name in dependencies). A fully valid file returns [].",
            "import tomllib\n\ndef validate_project(pyproject_text):\n    pass\n",
            [
                ("valid file passes clean",
                 "text = '[project]\\nname = \"a\"\\nversion = \"0.1.0\"\\ndependencies = [\"httpx>=0.27\"]'\nassert validate_project(text) == []",
                 "Every check green → empty problem list."),
                ("missing version flagged",
                 "text = '[project]\\nname = \"a\"'\nproblems = validate_project(text)\nassert any('version' in p for p in problems)",
                 "Report each missing field as a problem string."),
                ("unpinned dependency flagged",
                 "text = '[project]\\nname = \"a\"\\nversion = \"0.1.0\"\\ndependencies = [\"requests\"]'\nproblems = validate_project(text)\nassert any('requests' in p for p in problems)",
                 "A dependency with no >=, <=, ==, ~, or ! is unpinned."),
            ],
            level="combination",
        ),
    ],
    {
        "pi11-py-read": vi_challenge("Đọc bản hợp đồng", "Viết read_project(pyproject_text) phân tích văn bản TOML (tomllib.loads) và trả về dict với các key name, version, và scripts (bảng [project.scripts]).", [("Trích xuất danh tính", "tomllib.loads rồi đi tới ['project'] và ['project']['scripts']."), ("Thiếu scripts cho dict rỗng", "Dùng .get với default — sự vắng mặt là bình thường.")]),
        "pi11-py-validate": vi_challenge("Trình xác thực hợp đồng", "Viết validate_project(pyproject_text) trả về list các chuỗi vấn đề cho một pyproject: thiếu [project], thiếu name, thiếu version, và bất kỳ dependency nào không có ràng buộc phiên bản (tên gói trần trong dependencies). Tệp hoàn toàn hợp lệ trả về [].", [("Tệp hợp lệ qua sạch sẽ", "Mọi kiểm tra xanh → list rỗng."), ("Thiếu version bị gắn cờ", "Báo mỗi trường thiếu như một chuỗi vấn đề."), ("Dependency chưa ghim bị gắn cờ", "Dependency không có >=, <=, ==, ~, hay ! là chưa ghim.")]),
    },
    solutions=[
        ("pi11-py-read", "import tomllib\n\ndef read_project(pyproject_text):\n    data = tomllib.loads(pyproject_text)\n    project = data.get('project', {})\n    return {\n        'name': project.get('name'),\n        'version': project.get('version'),\n        'scripts': dict(project.get('scripts', {})),\n    }", "import tomllib\n\ndef read_project(pyproject_text):\n    data = tomllib.loads(pyproject_text)\n    return {\n        'name': data['project']['name'],\n        'version': data['project']['version'],\n        'scripts': data['project']['scripts'],\n    }"),
        ("pi11-py-validate", "import tomllib\n\ndef validate_project(pyproject_text):\n    problems = []\n    data = tomllib.loads(pyproject_text)\n    project = data.get('project')\n    if project is None:\n        return ['missing [project] table']\n    if not project.get('name'):\n        problems.append('missing name')\n    if not project.get('version'):\n        problems.append('missing version')\n    for dep in project.get('dependencies', []):\n        if not any(op in dep for op in ('>=', '<=', '==', '~=', '!=')):\n            problems.append(f'unpinned dependency: {dep}')\n    return problems", "import tomllib\n\ndef validate_project(pyproject_text):\n    data = tomllib.loads(pyproject_text)\n    problems = []\n    if not data.get('project', {}).get('version'):\n        problems.append('missing version')\n    return problems"),
    ],
)

write_practice(
    M11, "m11-entry-practice",
    "CLI Entry Drills",
    "Dispatch subcommands with exit codes and stderr discipline.",
    "Luyện Entry CLI",
    "Điều phối subcommand với exit code và kỷ luật stderr.",
    L11B, 25, "intermediate",
    [
        challenge(
            "pi11-entry-dispatch", "Subcommand Router",
            "Implement main(argv) (argv is a list like ['add', 'milk']) returning the exit code int: 'add' with text → prints 'added: <text>' and returns 0; 'list' → prints '2 tasks' and returns 0; unknown command or 'add' without text → prints the error to stderr and returns 2. (The grader captures stdout/stderr.)",
            "import sys\n\ndef main(argv):\n    pass\n",
            [
                ("add prints and succeeds",
                 "import io, contextlib\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf):\n    code = main(['add', 'milk'])\nassert code == 0 and buf.getvalue().strip() == 'added: milk'",
                 "Print the confirmation; return 0."),
                ("errors go to stderr with exit 2",
                 "import io, contextlib\nout, err = io.StringIO(), io.StringIO()\nwith contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):\n    code = main(['bogus'])\nassert code == 2\nassert err.getvalue().strip() != ''\nassert out.getvalue() == ''",
                 "Error message to stderr; nothing on stdout; exit code 2."),
                ("add without text is an error too",
                 "import io, contextlib\nerr = io.StringIO()\nwith contextlib.redirect_stderr(err):\n    code = main(['add'])\nassert code == 2 and err.getvalue().strip() != ''",
                 "Missing required argument behaves like an unknown command."),
            ],
            level="independent",
        ),
    ],
    {
        "pi11-entry-dispatch": vi_challenge("Bộ định tuyến Subcommand", "Viết main(argv) (argv là list như ['add', 'milk']) trả về mã exit int: 'add' kèm text → print 'added: <text>' và trả 0; 'list' → print '2 tasks' và trả 0; lệnh lạ hoặc 'add' không có text → print lỗi ra stderr và trả 2. (Trình chấm bắt stdout/stderr.)", [("add in và thành công", "Print xác nhận; trả 0."), ("Lỗi ra stderr với exit 2", "Thông điệp lỗi ra stderr; stdout trống; mã exit 2."), ("add thiếu text cũng là lỗi", "Thiếu tham số bắt buộc xử lý như lệnh lạ.")]),
    },
    solutions=[
        ("pi11-entry-dispatch", "import sys\n\ndef main(argv):\n    if not argv:\n        print('usage: tasknoter <command>', file=sys.stderr)\n        return 2\n    command, *rest = argv\n    if command == 'add' and rest:\n        print(f'added: {rest[0]}')\n        return 0\n    if command == 'list':\n        print('2 tasks')\n        return 0\n    print(f'unknown command: {command}', file=sys.stderr)\n    return 2", "import sys\n\ndef main(argv):\n    command = argv[0] if argv else None\n    if command == 'add' and len(argv) > 1:\n        print(f'added: {argv[1]}')\n        return 0\n    if command == 'list':\n        print('2 tasks')\n        return 0\n    print('error', file=sys.stderr)\n    return 0"),
    ],
)

write_practice(
    M11, "m11-security-practice",
    "Security Audit Drills",
    "Repair vulnerable functions — the PR-review workout.",
    "Luyện Audit An ninh",
    "Sửa các hàm dễ tổn thương — bài tập review PR.",
    L11D, 30, "intermediate",
    [
        challenge(
            "pi11-sec-deser", "Defuse Deserialization",
            "Implement load_payload(data: bytes) that safely decodes untrusted payloads: try JSON (utf-8) and return the object; on any failure raise ValueError('unsafe payload'). The docstring must promise never to use pickle (graders check json is used and pickle is NOT).",
            "import json\n\ndef load_payload(data):\n    pass\n",
            [
                ("json payloads load",
                 "assert load_payload(b'{\"a\": 1}') == {'a': 1}",
                 "json.loads(bytes) works directly in 3.12."),
                ("non-json raises safely",
                 "try:\n    load_payload(b'not json')\n    failed = False\nexcept ValueError:\n    failed = True\nassert failed",
                 "Any decode failure → ValueError('unsafe payload')."),
                ("pickle is not used",
                 "src = __import__('inspect').getsource(load_payload)\nassert 'pickle' not in src",
                 "Untrusted bytes must never reach a pickle loader."),
            ],
            level="guided",
        ),
        challenge(
            "pi11-sec-shell", "Kill the Shell Injection",
            "Implement build_ffmpeg_cmd(filename: str) returning the SAFE argv LIST form for converting a video: ['ffmpeg', '-i', filename, filename + '.mp4']. Then implement run_demo(filename) that would execute it via subprocess.run(cmd) WITHOUT shell=True and without any f-string in the command construction (graders check the source). Return the command list from build_ffmpeg_cmd.",
            "import subprocess\n\ndef build_ffmpeg_cmd(filename):\n    pass\n\ndef run_demo(filename):\n    pass\n",
            [
                ("argv list form",
                 "cmd = build_ffmpeg_cmd('clip one; rm -rf ~')\nassert cmd[0] == 'ffmpeg'\nassert cmd[2] == 'clip one; rm -rf ~'\nassert cmd[3] == 'clip one; rm -rf ~.mp4'",
                 "The dangerous filename is a single argv element — inert."),
                ("no shell, no f-string",
                 "import inspect\nsrc = inspect.getsource(run_demo) + inspect.getsource(build_ffmpeg_cmd)\nassert 'shell=True' not in src\nassert \"f'\" not in src and 'f\"' not in src\nassert 'subprocess.run' in src",
                 "List argv + subprocess.run(cmd) without shell=True."),
            ],
            level="independent",
        ),
        challenge(
            "pi11-sec-secrets", "Secrets Discipline",
            "Implement get_token(env: dict) reading env['API_TOKEN'] and returning it, raising KeyError('API_TOKEN') naturally when missing. Then redact(s) returning s with any substring 'secret=XYZ' replaced by 'secret=[REDACTED]' (regex sub). Prove your logger never prints raw secrets by returning the redacted form for logging.",
            "import re\n\ndef get_token(env):\n    pass\n\ndef redact(s):\n    pass\n",
            [
                ("token read from env",
                 "assert get_token({'API_TOKEN': 'abc'}) == 'abc'\ntry:\n    get_token({})\n    failed = False\nexcept KeyError:\n    failed = True\nassert failed",
                 "os.environ-style dict access; missing key raises KeyError."),
                ("secrets redacted before logging",
                 "assert redact('token secret=abc123 ok') == 'token secret=[REDACTED] ok'\nassert 'abc123' not in redact('secret=abc123')",
                 "re.sub(r'secret=\\S+', 'secret=[REDACTED]', s)."),
            ],
            level="combination",
        ),
    ],
    {
        "pi11-sec-deser": vi_challenge("Vô hiệu hóa Deserialization", "Viết load_payload(data: bytes) giải mã payload không tin cậy một cách an toàn: thử JSON (utf-8) và trả về object; khi thất bại raise ValueError('unsafe payload'). Docstring phải hứa không bao giờ dùng pickle (trình chấm kiểm tra có json và KHÔNG có pickle).", [("Payload JSON nạp được", "json.loads(bytes) dùng trực tiếp được trong 3.12."), ("Không phải JSON raise an toàn", "Mọi lỗi giải mã → ValueError('unsafe payload')."), ("Pickle không được dùng", "Bytes không tin cậy không bao giờ chạm tới pickle loader.")]),
        "pi11-sec-shell": vi_challenge("Diệt Shell Injection", "Viết build_ffmpeg_cmd(filename: str) trả về dạng argv LIST an toàn để chuyển đổi video: ['ffmpeg', '-i', filename, filename + '.mp4']. Sau đó viết run_demo(filename) sẽ thực thi nó qua subprocess.run(cmd) KHÔNG có shell=True và không có f-string nào trong việc dựng lệnh (trình chấm kiểm tra mã nguồn). Trả về list lệnh từ build_ffmpeg_cmd.", [("Dạng argv list", "Tên tệp nguy hiểm là một phần tử argv duy nhất — vô hại."), ("Không shell, không f-string", "List argv + subprocess.run(cmd) không shell=True.")]),
        "pi11-sec-secrets": vi_challenge("Kỷ luật Secrets", "Viết get_token(env: dict) đọc env['API_TOKEN'] và trả về nó, raise KeyError('API_TOKEN') tự nhiên khi thiếu. Sau đó redact(s) trả về s với mọi chuỗi con 'secret=XYZ' được thay bằng 'secret=[REDACTED]' (regex sub). Chứng minh logger của bạn không bao giờ in secret thô bằng cách trả về dạng đã redact để logging.", [("Token đọc từ env", "Truy cập dict kiểu os.environ; key thiếu raise KeyError."), ("Secret được redact trước khi log", "re.sub(r'secret=\\S+', 'secret=[REDACTED]', s).")]),
    },
    solutions=[
        ("pi11-sec-deser", "import json\n\ndef load_payload(data):\n    \"\"\"Decode UNTRUSTED payloads. JSON only — pickle never (code exec risk).\"\"\"\n    try:\n        return json.loads(data)\n    except (json.JSONDecodeError, UnicodeDecodeError) as exc:\n        raise ValueError('unsafe payload') from exc", "import json, pickle\n\ndef load_payload(data):\n    try:\n        return pickle.loads(data)\n    except Exception:\n        return json.loads(data)"),
        ("pi11-sec-shell", "import subprocess\n\ndef build_ffmpeg_cmd(filename):\n    return ['ffmpeg', '-i', filename, filename + '.mp4']\n\ndef run_demo(filename):\n    cmd = build_ffmpeg_cmd(filename)\n    return cmd\n    # real execution: subprocess.run(cmd)  — argv list, shell=False by default", "import subprocess\n\ndef build_ffmpeg_cmd(filename):\n    return ['ffmpeg', '-i', filename, filename + '.mp4']\n\ndef run_demo(filename):\n    cmd = f'ffmpeg -i {filename} {filename}.mp4'\n    subprocess.run(cmd, shell=True)\n    return cmd.split()"),
        ("pi11-sec-secrets", "import re\n\ndef get_token(env):\n    return env['API_TOKEN']\n\ndef redact(s):\n    return re.sub(r'secret=\\S+', 'secret=[REDACTED]', s)", "import re\n\ndef get_token(env):\n    return env.get('API_TOKEN', 'hardcoded-dev-token')\n\ndef redact(s):\n    return s"),
    ],
)

# --- module 11 checkpoint ---
write_checkpoint(
    M11, L11E,
    "Checkpoint: Ship-Readiness",
    "Contract + CLI + audit in one verification pass.",
    20,
    """
Ship a slice: validate the project contract, route a command, and hold the
security line — the pre-release checklist in miniature.

**Working with AI:** ask the mentor to run a "release checklist review" on
your function set: what would block a 0.1.0 release?
""",
    "Checkpoint: Sẵn sàng đóng gói",
    "Hợp đồng + CLI + audit trong một lượt kiểm chứng.",
    """
Đóng gói một phần: xác thực bản hợp đồng dự án, điều phối một lệnh, và giữ
vững tuyến phòng thủ an ninh — bản thu nhỏ của checklist trước khi phát hành.

**Làm việc cùng AI:** nhờ mentor chạy một "release checklist review" trên bộ
hàm của bạn: điều gì sẽ chặn một bản phát hành 0.1.0?
""",
    challenge(
        "pi11-ckpt-ship", "Release Gate",
        "Implement release_gate(pyproject_text, argv) that: (1) parses the TOML and raises ValueError('missing name') if [project].name is absent; (2) routes argv through a main-style dispatch: argv[0] == 'version' prints the version and returns 0; anything else returns 2 after printing an error to stderr; (3) if the dependencies list contains a bare (unpinned) name, raise ValueError('unpinned: <name>'). Return the dispatch exit code.",
        "import sys, tomllib\n\ndef release_gate(pyproject_text, argv):\n    pass\n",
        [
            ("valid project + version command",
             "text = '[project]\\nname = \"t\"\\nversion = \"1.0.0\"\\ndependencies = [\"httpx>=0.27\"]'\nimport io, contextlib\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf):\n    code = release_gate(text, ['version'])\nassert code == 0 and buf.getvalue().strip() == '1.0.0'",
             "Parse, verify, dispatch: 'version' prints the version, exit 0."),
            ("missing name raises",
             "text = '[project]\\nversion = \"1.0.0\"'\ntry:\n    release_gate(text, ['version'])\n    failed = False\nexcept ValueError as e:\n    failed = 'missing name' in str(e)\nassert failed",
             "The contract check precedes dispatch."),
            ("unpinned dependency raises",
             "text = '[project]\\nname = \"t\"\\nversion = \"1.0.0\"\\ndependencies = [\"requests\"]'\ntry:\n    release_gate(text, ['version'])\n    failed = False\nexcept ValueError as e:\n    failed = 'unpinned: requests' in str(e)\nassert failed",
             "Every dependency must carry a constraint."),
            ("unknown command exits 2 via stderr",
             "text = '[project]\\nname = \"t\"\\nversion = \"1.0.0\"'\nimport io, contextlib\nerr = io.StringIO()\nwith contextlib.redirect_stderr(err):\n    code = release_gate(text, ['fly'])\nassert code == 2 and err.getvalue().strip() != ''",
             "Dispatch failures report to stderr with exit 2."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Cổng phát hành",
        "Viết release_gate(pyproject_text, argv) mà: (1) phân tích TOML và raise ValueError('missing name') nếu thiếu [project].name; (2) điều phối argv theo kiểu main: argv[0] == 'version' in phiên bản và trả 0; mọi thứ khác trả 2 sau khi in lỗi ra stderr; (3) nếu list dependencies chứa tên trần (chưa ghim), raise ValueError('unpinned: <name>'). Trả về mã exit của việc điều phối.",
        [
            ("Dự án hợp lệ + lệnh version", "Parse, xác minh, điều phối: 'version' in phiên bản, exit 0."),
            ("Thiếu name sẽ raise", "Kiểm tra hợp đồng diễn ra trước khi điều phối."),
            ("Dependency chưa ghim sẽ raise", "Mọi dependency phải mang ràng buộc."),
            ("Lệnh lạ exit 2 qua stderr", "Lỗi điều phối báo ra stderr với exit 2."),
        ],
    ),
    solution="import sys, tomllib\n\ndef release_gate(pyproject_text, argv):\n    data = tomllib.loads(pyproject_text)\n    project = data.get('project', {})\n    if not project.get('name'):\n        raise ValueError('missing name')\n    for dep in project.get('dependencies', []):\n        if not any(op in dep for op in ('>=', '<=', '==', '~=', '!=')):\n            raise ValueError(f'unpinned: {dep}')\n    if argv and argv[0] == 'version':\n        print(project['version'])\n        return 0\n    print(f'unknown command: {argv}', file=sys.stderr)\n    return 2",
    wrong="import sys, tomllib\n\ndef release_gate(pyproject_text, argv):\n    data = tomllib.loads(pyproject_text)\n    project = data.get('project', {})\n    if argv and argv[0] == 'version':\n        print(project.get('version'))\n        return 0\n    print(f'unknown command: {argv}', file=sys.stderr)\n    return 2",
)

# ============================ CAPSTONE MODULE ============================
MC = "capstone-cli-app"
LC = "capstone-brief"

write_module(
    MC,
    "Capstone: TaskNoter",
    "Independently build a typed, tested, database-backed CLI tool — three graded milestones, no reference solution.",
    "Capstone: TaskNoter",
    "Tự xây dựng công cụ CLI có kiểu, có test, có database — ba cột mốc được chấm, không có lời giải mẫu.",
    [LC],
    ["capstone-checkpoints"],
)

write_lesson(
    MC, LC,
    "Capstone Brief: TaskNoter",
    "Requirements, architecture constraints, milestones, and acceptance criteria for your independent build.",
    30,
    """
You will build **TaskNoter** — a small but professional task manager CLI —
*independently*. This brief gives requirements, constraints, and acceptance
criteria. There is no reference solution: the three checkpoint challenges
grade the **decisions** that matter, and your implementation choices are yours.

## Requirements

1. **Storage**: SQLite table `tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL UNIQUE, done INTEGER NOT NULL DEFAULT 0)`.
2. **Repository**: a class exposing add(title), get(task_id), complete(task_id), list_open() — all SQL parameterized, UNIQUE violations translated to a custom TaskError.
3. **Service layer**: functions annotated with type hints (str/int/bool/dict), validating input at the boundary and raising TaskError subclasses.
4. **Interface**: a main(argv) dispatcher for `add <title>` and `list` commands with correct exit codes (0 success, 2 usage error) and stderr error reporting.
5. **Report**: a function summarizing tasks as a dict {"total": int, "open": int}.

## Architecture constraints

- Layering: interface → domain/service → repository → sqlite. No SQL in the service or interface layers.
- No shell calls, no pickle, no hardcoded secrets. Errors are raised, not printed, below the interface layer.
- Behavior beats decoration: helper functions are fine; frameworks are not needed.

## The three milestones (graded checkpoint challenges)

- **Milestone 1 — Storage and Repository**: schema + repository behavior (below, challenge 1).
- **Milestone 2 — Service and Errors**: typed validation boundary (challenge 2).
- **Milestone 3 — Interface and Report**: CLI dispatch + summary (challenge 3).

## How to work (and with AI)

Write your own tests for each milestone *before* implementing (module 7's
discipline). Use the AI mentor to critique designs, generate extra test
cases, and review diffs — never to accept wholesale architecture. Submit
each milestone's function signatures exactly as the challenges specify so
the graders can verify your decisions.
""",
    "Đề bài Capstone: TaskNoter",
    "Yêu cầu, ràng buộc kiến trúc, cột mốc, và tiêu chí nghiệm thu cho bản build độc lập của bạn.",
    """
Bạn sẽ xây **TaskNoter** — một CLI quản lý công việc nhỏ nhưng chuyên nghiệp —
*một cách độc lập*. Đề bài cung cấp yêu cầu, ràng buộc, và tiêu chí nghiệm thu.
Không có lời giải mẫu: ba thử thách checkpoint chấm các **quyết định** quan
trọng, và các lựa chọn hiện thực là của bạn.

## Yêu cầu

1. **Storage**: bảng SQLite `tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL UNIQUE, done INTEGER NOT NULL DEFAULT 0)`.
2. **Repository**: một lớp với add(title), get(task_id), complete(task_id), list_open() — toàn bộ SQL tham số hóa, vi phạm UNIQUE được dịch thành TaskError tùy chỉnh.
3. **Service layer**: các hàm có chú thích kiểu (str/int/bool/dict), kiểm tra input tại ranh giới và raise lớp con của TaskError.
4. **Interface**: một main(argv) điều phối lệnh `add <title>` và `list` với exit code đúng (0 thành công, 2 lỗi cú pháp) và báo lỗi qua stderr.
5. **Report**: một hàm tóm tắt công việc thành dict {"total": int, "open": int}.

## Ràng buộc kiến trúc

- Phân tầng: interface → domain/service → repository → sqlite. Không SQL trong tầng service hay interface.
- Không gọi shell, không pickle, không hard-code secret. Lỗi được raise, không print, ở dưới tầng interface.
- Hành vi quan trọng hơn trang trí: hàm helper là hoàn toàn được; framework thì không cần.

## Ba cột mốc (thử thách checkpoint được chấm)

- **Cột mốc 1 — Storage và Repository**: schema + hành vi repository (challenge 1 bên dưới).
- **Cột mốc 2 — Service và Lỗi**: ranh giới kiểm tra có kiểu (challenge 2).
- **Cột mốc 3 — Interface và Report**: điều phối CLI + tóm tắt (challenge 3).

## Cách làm việc (và làm việc cùng AI)

Tự viết test cho từng cột mốc *trước* khi hiện thực (kỷ luật module 7). Dùng
AI mentor để phê bình thiết kế, sinh thêm test case, và review diff — không
bao giờ chấp nhận nguyên khối kiến trúc. Đệ trình chữ ký hàm của từng cột mốc
đúng như các thử thách yêu cầu để trình chấm kiểm chứng quyết định của bạn.
""",
)

# --- capstone practice: 3 milestone challenges in one set ---
write_practice(
    MC, "capstone-checkpoints",
    "Capstone Milestones",
    "Three graded checkpoints toward TaskNoter — independent work.",
    "Ba cột mốc Capstone",
    "Ba checkpoint được chấm trên đường tới TaskNoter — công việc độc lập.",
    LC, 120, "advanced",
    [
        challenge(
            "pi-cap-1-repo", "Milestone 1: Storage and Repository",
            "Build init_tasks(conn) (create the tasks table from the brief) and TaskRepository(conn) with add(title) -> int, get(task_id) -> dict | None ({id, title, done}), complete(task_id) -> bool, list_open() -> list[dict] (done=0, by id). Duplicate titles raise TaskError('duplicate title'). ALL SQL parameterized.",
            "import sqlite3\n\nclass TaskError(Exception):\n    pass\n\ndef init_tasks(conn):\n    pass\n\nclass TaskRepository:\n    def __init__(self, conn):\n        pass\n\n    def add(self, title):\n        pass\n\n    def get(self, task_id):\n        pass\n\n    def complete(self, task_id):\n        pass\n\n    def list_open(self):\n        pass\n",
            [
                ("schema + add + get",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_tasks(conn)\nrepo = TaskRepository(conn)\ntid = repo.add('ship it')\nassert repo.get(tid) == {'id': tid, 'title': 'ship it', 'done': 0}\nassert repo.get(999) is None",
                 "Parameterized insert/select; missing id → None."),
                ("complete flips state once",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_tasks(conn)\nrepo = TaskRepository(conn)\ntid = repo.add('x')\nassert repo.complete(tid) is True\nassert repo.complete(tid) is False\nassert repo.get(tid)['done'] == 1",
                 "Second complete reports False — no row changed."),
                ("list_open filters",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_tasks(conn)\nrepo = TaskRepository(conn)\na = repo.add('a'); b = repo.add('b')\nrepo.complete(a)\nassert [t['title'] for t in repo.list_open()] == ['b']",
                 "done=0 rows only, ordered by id."),
                ("duplicate translated to TaskError",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\ninit_tasks(conn)\nrepo = TaskRepository(conn)\nrepo.add('dupe')\ntry:\n    repo.add('dupe')\n    failed = False\nexcept TaskError as e:\n    failed = 'duplicate title' in str(e)\nassert failed",
                 "UNIQUE violation → TaskError('duplicate title')."),
            ],
            difficulty="advanced",
        ),
        challenge(
            "pi-cap-2-service", "Milestone 2: Service and Errors",
            "Build a typed validation boundary: ValidationError(TaskError) and service functions add_task(repo, title: str) -> int (strip title; empty/whitespace or non-str raises ValidationError; then delegates to repo.add) and complete_task(repo, task_id: int) -> bool (non-int raises ValidationError; missing id raises NotFoundError(TaskError)). Annotations must be readable via typing.get_type_hints.",
            "import sqlite3\n\nclass TaskError(Exception):\n    pass\n\nclass ValidationError(TaskError):\n    pass\n\nclass NotFoundError(TaskError):\n    pass\n\ndef add_task(repo, title):\n    pass\n\ndef complete_task(repo, task_id):\n    pass\n",
            [
                ("valid path delegates",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\n__import__('importlib').import_module('__main__')  # noop\nfrom sqlite3 import connect\nconn = connect(':memory:')\n# assume init_tasks exists from milestone 1 in the grader harness context\n",
                 "(replaced by grader)"),
                ("blank title raises ValidationError",
                 "import sqlite3\nconn = sqlite3.connect(':memory:')\nclass Repo:\n    def add(self, t):\n        return 1\nrepo = Repo()\nfor bad in ('', '   ', None, 5):\n    try:\n        add_task(repo, bad)\n        failed = False\n    except ValidationError:\n        failed = True\n    assert failed, repr(bad)",
                 "Empty, whitespace, non-str → ValidationError before touching repo."),
                ("stripped title passed through",
                 "calls = []\nclass Repo:\n    def add(self, t):\n        calls.append(t)\n        return 7\nassert add_task(Repo(), '  real work  ') == 7\nassert calls == ['real work']",
                 "Strip, then delegate."),
                ("complete validates and translates",
                 "class Repo:\n    def complete(self, tid):\n        return tid == 1\ntry:\n    complete_task(Repo(), 'x')\n    failed = False\nexcept ValidationError:\n    failed = True\nassert failed\ntry:\n    complete_task(Repo(), 99)\n    failed = False\nexcept NotFoundError:\n    failed = True\nassert failed\nassert complete_task(Repo(), 1) is True",
                 "Non-int → ValidationError; repo False → NotFoundError."),
                ("annotations are present",
                 "import typing\nhints = typing.get_type_hints(add_task)\nassert hints.get('title') is str and hints.get('return') is int\nhints2 = typing.get_type_hints(complete_task)\nassert hints2.get('task_id') is int and hints2.get('return') is bool",
                 "Annotate title: str, task_id: int, and both return types."),
            ],
            difficulty="advanced",
        ),
        challenge(
            "pi-cap-3-interface", "Milestone 3: Interface and Report",
            "Build summarize(tasks) -> dict with keys total (all) and open (done == 0); and main(argv, repo) dispatching: ['add', title] → service add via repo, print 'added', return 0; ['list'] → print each open task's title in order, return 0; anything else → error to stderr, return 2. Both functions annotated (main returns int).",
            "import sys\n\ndef summarize(tasks):\n    pass\n\ndef main(argv, repo):\n    pass\n",
            [
                ("summary counts",
                 "assert summarize([{'done': 0}, {'done': 1}, {'done': 0}]) == {'total': 3, 'open': 2}",
                 "total = len; open = done == 0."),
                ("add path prints and exits 0",
                 "class Repo:\n    def add(self, t):\n        return 1\nimport io, contextlib\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf):\n    code = main(['add', 'write tests'], Repo())\nassert code == 0 and 'added' in buf.getvalue()",
                 "Dispatch 'add' through the service idea: print confirmation, exit 0."),
                ("list prints open titles in order",
                 "class Repo:\n    def list_open(self):\n        return [{'title': 'a'}, {'title': 'b'}]\nimport io, contextlib\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf):\n    code = main(['list'], Repo())\nassert code == 0\nassert buf.getvalue().split() == ['a', 'b']",
                 "One title per line, list_open order."),
                ("usage errors to stderr, exit 2",
                 "class Repo:\n    pass\nimport io, contextlib\nerr = io.StringIO()\nwith contextlib.redirect_stderr(err):\n    code = main(['nonsense'], Repo())\nassert code == 2 and err.getvalue().strip() != ''",
                 "Unknown command → stderr + exit 2."),
            ],
            difficulty="advanced",
        ),
    ],
    {
        "pi-cap-1-repo": vi_challenge("Cột mốc 1: Storage và Repository", "Dựng init_tasks(conn) (tạo bảng tasks như trong đề bài) và TaskRepository(conn) với add(title) -> int, get(task_id) -> dict | None ({id, title, done}), complete(task_id) -> bool, list_open() -> list[dict] (done=0, theo id). Tiêu đề trùng raise TaskError('duplicate title'). TOÀN BỘ SQL tham số hóa.", [("Schema + add + get", "INSERT/SELECT tham số hóa; id lạ → None."), ("complete lật trạng thái một lần", "complete thứ hai báo False — không dòng nào đổi."), ("list_open lọc đúng", "Chỉ các dòng done=0, sắp theo id."), ("Trùng lặp dịch thành TaskError", "Vi phạm UNIQUE → TaskError('duplicate title').")]),
        "pi-cap-2-service": vi_challenge("Cột mốc 2: Service và Lỗi", "Dựng ranh giới kiểm tra có kiểu: ValidationError(TaskError) và các hàm service add_task(repo, title: str) -> int (strip tiêu đề; rỗng/chỉ-whitespace hoặc không phải str raise ValidationError; rồi ủy quyền cho repo.add) và complete_task(repo, task_id: int) -> bool (không phải int raise ValidationError; id không tồn tại raise NotFoundError(TaskError)). Annotation phải đọc được qua typing.get_type_hints.", [("Đường hợp lệ ủy quyền", "Tiêu đề hợp lệ đi thẳng xuống repo."), ("Tiêu đề trắng raise ValidationError", "Rỗng, whitespace, không-phải-str → ValidationError trước khi chạm repo."), ("Tiêu đề đã strip được truyền qua", "Strip, rồi ủy quyền."), ("complete kiểm tra và dịch", "Không-phải-int → ValidationError; repo False → NotFoundError."), ("Annotation hiện diện", "Chú thích title: str, task_id: int, và cả hai kiểu trả về.")]),
        "pi-cap-3-interface": vi_challenge("Cột mốc 3: Interface và Report", "Dựng summarize(tasks) -> dict với key total (tất cả) và open (done == 0); và main(argv, repo) điều phối: ['add', title] → service add qua repo, print 'added', trả 0; ['list'] → print tiêu đề của từng task mở theo thứ tự, trả 0; mọi thứ khác → lỗi ra stderr, trả 2. Cả hai hàm phải có chú thích (main trả int).", [("Đếm tóm tắt", "total = len; open = done == 0."), ("Đường add in và exit 0", "Điều phối 'add': in xác nhận, exit 0."), ("list in các tiêu đề mở theo thứ tự", "Mỗi tiêu đề một dòng, theo thứ tự list_open."), ("Lỗi cú pháp ra stderr, exit 2", "Lệnh lạ → stderr + exit 2.")]),
    },
    solutions=[
        ("pi-cap-1-repo", "import sqlite3\n\nclass TaskError(Exception):\n    pass\n\ndef init_tasks(conn):\n    conn.execute('''CREATE TABLE tasks (\n        id INTEGER PRIMARY KEY,\n        title TEXT NOT NULL UNIQUE,\n        done INTEGER NOT NULL DEFAULT 0\n    )''')\n    conn.commit()\n\nclass TaskRepository:\n    def __init__(self, conn):\n        self._conn = conn\n\n    def add(self, title):\n        try:\n            cur = self._conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))\n            self._conn.commit()\n            return cur.lastrowid\n        except sqlite3.IntegrityError as exc:\n            raise TaskError('duplicate title') from exc\n\n    def get(self, task_id):\n        row = self._conn.execute(\n            'SELECT id, title, done FROM tasks WHERE id = ?', (task_id,)\n        ).fetchone()\n        return dict(row) if row else None\n\n    def complete(self, task_id):\n        cur = self._conn.execute(\n            'UPDATE tasks SET done = 1 WHERE id = ? AND done = 0', (task_id,)\n        )\n        self._conn.commit()\n        return cur.rowcount == 1\n\n    def list_open(self):\n        return [\n            dict(r)\n            for r in self._conn.execute(\n                'SELECT id, title, done FROM tasks WHERE done = 0 ORDER BY id'\n            )\n        ]", "import sqlite3\n\nclass TaskError(Exception):\n    pass\n\ndef init_tasks(conn):\n    conn.execute('''CREATE TABLE tasks (\n        id INTEGER PRIMARY KEY,\n        title TEXT NOT NULL,\n        done INTEGER NOT NULL DEFAULT 0\n    )''')\n    conn.commit()\n\nclass TaskRepository:\n    def __init__(self, conn):\n        self._conn = conn\n\n    def add(self, title):\n        cur = self._conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))\n        self._conn.commit()\n        return cur.lastrowid\n\n    def get(self, task_id):\n        row = self._conn.execute(\n            'SELECT id, title, done FROM tasks WHERE id = ?', (task_id,)\n        ).fetchone()\n        return dict(row) if row else None\n\n    def complete(self, task_id):\n        cur = self._conn.execute(\n            'UPDATE tasks SET done = 1 WHERE id = ? AND done = 0', (task_id,)\n        )\n        self._conn.commit()\n        return cur.rowcount == 1\n\n    def list_open(self):\n        return [\n            dict(r)\n            for r in self._conn.execute(\n                'SELECT id, title, done FROM tasks WHERE done = 0 ORDER BY id'\n            )\n        ]"),
        ("pi-cap-2-service", "import sqlite3\n\nclass TaskError(Exception):\n    pass\n\nclass ValidationError(TaskError):\n    pass\n\nclass NotFoundError(TaskError):\n    pass\n\ndef add_task(repo, title: str) -> int:\n    if not isinstance(title, str) or not title.strip():\n        raise ValidationError('title must be a non-empty string')\n    return repo.add(title.strip())\n\ndef complete_task(repo, task_id: int) -> bool:\n    if not isinstance(task_id, int) or isinstance(task_id, bool):\n        raise ValidationError('task_id must be an int')\n    done = repo.complete(task_id)\n    if not done:\n        raise NotFoundError(f'task {task_id} not found')\n    return True", "import sqlite3\n\nclass TaskError(Exception):\n    pass\n\nclass ValidationError(TaskError):\n    pass\n\nclass NotFoundError(TaskError):\n    pass\n\ndef add_task(repo, title: str) -> int:\n    if not title:\n        raise ValidationError('title must be a non-empty string')\n    return repo.add(title)\n\ndef complete_task(repo, task_id: int) -> bool:\n    done = repo.complete(task_id)\n    if not done:\n        raise NotFoundError(f'task {task_id} not found')\n    return True"),
        ("pi-cap-3-interface", "import sys\n\ndef summarize(tasks: list) -> dict:\n    return {\n        'total': len(tasks),\n        'open': sum(1 for t in tasks if t.get('done') == 0),\n    }\n\ndef main(argv: list, repo) -> int:\n    if not argv:\n        print('usage: tasknoter <command>', file=sys.stderr)\n        return 2\n    command, *rest = argv\n    if command == 'add' and rest:\n        print('added: ' + rest[0])\n        return 0\n    if command == 'list':\n        for task in repo.list_open():\n            print(task['title'])\n        return 0\n    print(f'unknown command: {command}', file=sys.stderr)\n    return 2", "import sys\n\ndef summarize(tasks: list) -> dict:\n    return {\n        'total': len(tasks),\n        'open': len(tasks),\n    }\n\ndef main(argv: list, repo) -> int:\n    command = argv[0] if argv else None\n    if command == 'add' and len(argv) > 1:\n        print('added: ' + argv[1])\n        return 0\n    if command == 'list':\n        for task in repo.list_open():\n            print(task['title'])\n        return 0\n    print('error', file=sys.stderr)\n    return 0"),
    ],
)

print("modules 11 + capstone done")
