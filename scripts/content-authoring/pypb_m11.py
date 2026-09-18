#!/usr/bin/env python3
"""Module 11: environments-and-packages — lessons + practices.

Sandbox has no network and no venv, so challenges verify the CONCEPTS that are
host-verifiable: dependency reasoning, requirements.txt shape, pip command
correctness (as text), and import hygiene.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "environments-and-packages"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
Your first projects used only the standard library — nothing to install. Real
projects lean on **third-party packages** (requests, rich, pytest...), and that
creates a problem: two projects on one machine often need different versions of
the same package.

## The problem

```
project-a needs requests==2.25
project-b needs requests==2.31
```

Install globally and one project silently breaks the other.

## The fix: virtual environments

A **venv** is a private, disposable Python setup for one project:

```bash
python3 -m venv .venv        # create (once per project)
source .venv/bin/activate    # activate (every shell) — Windows: .venv\\Scripts\\activate
```

With the venv active, `pip install` affects ONLY that project. Deactivate with
`deactivate`. The venv is regenerable — delete it, recreate it, nothing of
yours is lost.
"""

L1_VI = """
Những dự án đầu tiên của bạn chỉ dùng thư viện chuẩn — không cần cài gì. Dự án
thật dựa vào các **gói bên thứ ba** (requests, rich, pytest...), và đó là lúc
vấn đề xuất hiện: hai dự án trên cùng một máy thường cần khác phiên bản của
cùng một gói.

## Vấn đề

```
project-a cần requests==2.25
project-b cần requests==2.31
```

Cài toàn cục và một dự án sẽ âm thầm phá vỡ dự án kia.

## Giải pháp: môi trường ảo

Một **venv** là bộ Python riêng tư, dùng một lần rồi bỏ, cho từng dự án:

```bash
python3 -m venv .venv        # tạo (mỗi dự án một lần)
source .venv/bin/activate    # kích hoạt (mỗi phiên terminal) — Windows: .venv\\Scripts\\activate
```

Khi venv đang kích hoạt, `pip install` chỉ ảnh hưởng DUY NHẤT dự án đó. Thoát
bằng `deactivate`. Venv có thể tái tạo — xóa đi, tạo lại, không mất thứ gì của
bạn.
"""

L2 = """
**pip** is the installer; **PyPI** (pypi.org) is the public package catalog it
downloads from.

```bash
pip install rich            # latest version
pip install "requests==2.31.0"   # exact version — reproducible
pip list                    # what is installed here
```

## requirements.txt — your project's recipe

```
rich==13.7.1
requests==2.31.0
```

Freeze what you installed:

```bash
pip freeze > requirements.txt
```

Rebuild the environment anywhere (a teammate's laptop, a server):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Version pins are a kindness to your future self and your teammates: "it works
on my machine" becomes "here is the exact recipe that works."
"""

L2_VI = """
**pip** là trình cài đặt; **PyPI** (pypi.org) là danh mục gói công khai mà nó
tải về.

```bash
pip install rich            # phiên bản mới nhất
pip install "requests==2.31.0"   # đúng phiên bản — tái lập được
pip list                    # cái gì đã cài ở đây
```

## requirements.txt — công thức của dự án

```
rich==13.7.1
requests==2.31.0
```

Ghim lại những gì đã cài:

```bash
pip freeze > requirements.txt
```

Xây lại môi trường ở bất kỳ đâu (laptop của đồng đội, một máy chủ):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ghim phiên bản là một phép lịch sự với chính bạn trong tương lai và đồng đội:
"chạy trên máy tôi" trở thành "đây là công thức chính xác đã chạy."
"""

L3 = """
With great package power comes great dependency judgment:

## Questions before importing a package

1. Is it maintained? (recent releases, open issue activity)
2. Is it popular enough to have answers when you get stuck?
3. Does the standard library already do this? (`json` beats half the JSON
   packages on PyPI.)
4. What does it drag in? Every dependency has dependencies.

## Keep the tree clean

- `.venv/` belongs to the machine, not the repo — ignore it in Git.
- `requirements.txt` belongs in the repo — it is the recipe.
- One venv per project, always.

This module's habits are what Intermediate will assume you have: isolated
environments, pinned versions, and the reflex to check whether the standard
library already solved it.
"""

L3_VI = """
Sức mạnh gói lớn đi kèm khả năng phán đoán phụ thuộc lớn:

## Câu hỏi trước khi import một gói

1. Nó có được bảo trì không? (bản phát hành gần đây, hoạt động issue)
2. Nó có đủ phổ biến để có câu trả lời khi bạn mắc kẹt?
3. Thư viện chuẩn đã làm được việc này chưa? (`json` đánh bại một nửa các gói
   JSON trên PyPI.)
4. Nó kéo theo gì? Mỗi phụ thuộc lại có phụ thuộc của riêng nó.

## Giữ cây thư mục gọn

- `.venv/` thuộc về máy, không thuộc repo — hãy ignore nó trong Git.
- `requirements.txt` thuộc về repo — đó là công thức.
- Một venv cho mỗi dự án, luôn luôn.

Thói quen của module này là thứ Intermediate sẽ mặc định bạn có: môi trường cô
lập, phiên bản được ghim, và phản xạ kiểm tra xem thư viện chuẩn đã giải quyết
chưa.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "m11-venv-pip-practice",
    "Venv & Pip Drills",
    "Command fluency and the reasoning behind isolation.",
    "Bài tập venv & pip",
    "Lệnh thành thạo và lý lẽ đằng sau sự cô lập.",
    "why-dependencies", 20, "beginner",
    [
        challenge(
            "py-pkg-venv-cmds",
            "The Venv Ritual, In Order",
            "Write a function venv_steps() that returns the exact shell commands to (1) create a venv named .venv and (2) activate it on macOS/Linux — as a list of two strings, in that order.",
            "",
            [("commands in order", 'steps = venv_steps()\nassert steps == ["python3 -m venv .venv", "source .venv/bin/activate"], f"got {steps}"\nassert "venv" in steps[0] and "activate" in steps[1], "create before activate"',
              'return ["python3 -m venv .venv", "source .venv/bin/activate"]')],
            level="guided",
        ),
        challenge(
            "py-pkg-why-venv",
            "Why Isolate?",
            "Write needs_venv(python_a, req_a, python_b, req_b) that returns True when two projects on one machine would CONFLICT — i.e. they share a package name but need different versions.",
            "",
            [("conflict detection", 'assert needs_venv("requests==2.25", ["requests==2.25"], "requests==2.31", ["requests==2.31"]) is True, "same package, different versions -> conflict"\nassert needs_venv("rich", ["rich==13.7"], "rich", ["rich==13.7"]) is False, "identical pins -> no conflict"',
              "compare the version part after == for any shared package name.")],
            level="independent",
        ),
    ],
    {
        "py-pkg-venv-cmds": vi_challenge("Nghi lễ venv, đúng thứ tự", "Viết hàm venv_steps() trả về các lệnh shell chính xác để (1) tạo venv tên .venv và (2) kích hoạt nó trên macOS/Linux — dưới dạng danh sách hai chuỗi, đúng thứ tự.",
                                        [("lệnh đúng thứ tự", 'return ["python3 -m venv .venv", "source .venv/bin/activate"]')]),
        "py-pkg-why-venv": vi_challenge("Tại sao cô lập?", "Viết needs_venv(python_a, req_a, python_b, req_b) trả về True khi hai dự án trên cùng một máy sẽ XUNG ĐỘT — tức dùng chung tên gói nhưng cần khác phiên bản.",
                                        [("phát hiện xung đột", "so sánh phần phiên bản sau == với mọi tên gói dùng chung.")]),
    },
    solutions=[
        ("py-pkg-venv-cmds", 'def venv_steps():\n    return ["python3 -m venv .venv", "source .venv/bin/activate"]',
         'def venv_steps():\n    return ["source .venv/bin/activate", "python3 -m venv .venv"]'),
        ("py-pkg-why-venv", 'def needs_venv(_a, req_a, _b, req_b):\n    a = dict(r.split("==") for r in req_a)\n    b = dict(r.split("==") for r in req_b)\n    return any(a[p] != b[p] for p in a if p in b)',
         'def needs_venv(_a, req_a, _b, req_b):\n    return True'),
    ],
)

write_practice(
    MOD, "m11-requirements-practice",
    "Requirements Hygiene",
    "Write and validate a requirements file.",
    "Vệ sinh requirements",
    "Viết và kiểm tra tệp requirements.",
    "pip-requirements", 20, "beginner",
    [
        challenge(
            "py-pkg-write-reqs",
            "Pin the Recipe",
            "Write a requirements.txt with EXACTLY two lines: rich==13.7.1 and requests==2.31.0 (final newline). The test parses it back.",
            "",
            [("requirements file valid", 'lines = open("requirements.txt", encoding="utf-8").read().splitlines()\nassert lines == ["rich==13.7.1", "requests==2.31.0"], f"got {lines}"\nassert all("==" in l for l in lines), "pin every version"',
              'with open("requirements.txt", "w", encoding="utf-8") as f: f.write("rich==13.7.1\\nrequests==2.31.0\\n")')],
            level="guided",
        ),
        challenge(
            "py-pkg-parse-reqs",
            "Validate a Requirements File",
            "Write parse_requirements(text) returning a dict of package -> version from a requirements-style string. Ignore blank lines and comments (# ...). Raise ValueError on any line without a version pin.",
            "",
            [("parses and validates", 'assert parse_requirements("rich==13.7.1\\n# comment\\n\\nrequests==2.31.0") == {"rich": "13.7.1", "requests": "2.31.0"}, "pins and skips"\ntry:\n    parse_requirements("rich")\n    assert False, "unpinned must raise"\nexcept ValueError:\n    pass',
              'for line in text.splitlines(): strip, skip blanks and "#"; if "==" not in line: raise ValueError; name, ver = line.split("==")')],
            level="independent",
        ),
        challenge(
            "py-pkg-install-cmd",
            "The Restore Command",
            "Given a fresh venv and a requirements.txt, which single pip command restores everything? Write restore_cmd() returning that command as a string.",
            "",
            [("the canonical restore", 'assert restore_cmd() == "pip install -r requirements.txt", f"got {restore_cmd()}"',
              'return "pip install -r requirements.txt" — the -r flag reads the recipe.')],
            level="imitation",
        ),
    ],
    {
        "py-pkg-write-reqs": vi_challenge("Ghim công thức", "Viết requirements.txt với ĐÚNG hai dòng: rich==13.7.1 và requests==2.31.0 (có xuống dòng cuối). Bài kiểm tra phân tích lại tệp.",
                                        [("tệp requirements hợp lệ", 'with open("requirements.txt", "w", encoding="utf-8") as f: f.write("rich==13.7.1\\nrequests==2.31.0\\n")')]),
        "py-pkg-parse-reqs": vi_challenge("Kiểm tra tệp requirements", "Viết parse_requirements(text) trả về dict gói -> phiên bản từ một chuỗi kiểu requirements. Bỏ qua dòng trống và chú thích (# ...). Raise ValueError với bất kỳ dòng nào không có ghim phiên bản.",
                                        [("phân tích và kiểm tra", 'for line in text.splitlines(): strip, bỏ qua dòng trống và "#"; if "==" not in line: raise ValueError; name, ver = line.split("==")')]),
        "py-pkg-install-cmd": vi_challenge("Lệnh khôi phục", "Cho một venv mới và một requirements.txt, lệnh pip nào duy nhất khôi phục mọi thứ? Viết restore_cmd() trả về lệnh đó dưới dạng chuỗi.",
                                        [("lệnh khôi phục chuẩn", 'return "pip install -r requirements.txt" — cờ -r đọc công thức.')]),
    },
    solutions=[
        ("py-pkg-write-reqs", 'with open("requirements.txt", "w", encoding="utf-8") as f:\n    f.write("rich==13.7.1\\nrequests==2.31.0\\n")',
         'with open("requirements.txt", "w", encoding="utf-8") as f:\n    f.write("rich>=13\\nrequests latest\\n")'),
        ("py-pkg-parse-reqs", 'def parse_requirements(text):\n    pkgs = {}\n    for line in text.splitlines():\n        line = line.strip()\n        if not line or line.startswith("#"):\n            continue\n        if "==" not in line:\n            raise ValueError(f"unpinned dependency: {line}")\n        name, ver = line.split("==", 1)\n        pkgs[name.strip()] = ver.strip()\n    return pkgs',
         'def parse_requirements(text):\n    pkgs = {}\n    for line in text.splitlines():\n        line = line.strip()\n        if not line or line.startswith("#"):\n            continue\n        name, _sep, ver = line.partition("==")\n        pkgs[name.strip()] = ver.strip() or "latest"\n    return pkgs'),
        ("py-pkg-install-cmd", 'def restore_cmd():\n    return "pip install -r requirements.txt"',
         'def restore_cmd():\n    return "pip install requirements.txt"'),
    ],
)

print("module 11 content written")
