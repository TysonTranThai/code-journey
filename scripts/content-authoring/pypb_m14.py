#!/usr/bin/env python3
"""Module 14: command-line-applications — lessons + practices."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import write_module, write_lesson, write_practice, challenge, vi_challenge

MOD = "command-line-applications"

# ── Lessons ──────────────────────────────────────────────────────────────────
L1 = """
A command-line application is a loop: show options, read a choice, act, repeat.

```python
while True:
    choice = menu()          # in real apps: input("> ")
    if choice == "list":
        show_tasks()
    elif choice == "add":
        add_task()
    elif choice == "quit":
        break
    else:
        print("unknown choice")
```

`input()` reads a line from the user — but the sandbox (and any automated
grader) cannot type at your program. That is why graded challenges isolate
**functions** with parameters and returns, and menus are wired around them:

```python
def add_task(tasks, text):
    tasks.append({"text": text, "done": False})
    return tasks
```

Separate the *deciding* from the *doing* and your CLI becomes testable — the
same lesson the capstone will grade you on.
"""

L1_VI = """
Một ứng dụng dòng lệnh là một vòng lặp: hiện các lựa chọn, đọc lựa chọn, hành
động, lặp lại.

```python
while True:
    choice = menu()          # ứng dụng thật: input("> ")
    if choice == "list":
        show_tasks()
    elif choice == "add":
        add_task()
    elif choice == "quit":
        break
    else:
        print("lựa chọn không rõ")
```

`input()` đọc một dòng từ người dùng — nhưng sandbox (và bất kỳ bộ chấm tự động
nào) không thể gõ vào chương trình của bạn. Vì thế các thử thách được chấm tách
**hàm** có tham số và giá trị trả về, và menu được nối quanh chúng:

```python
def add_task(tasks, text):
    tasks.append({"text": text, "done": False})
    return tasks
```

Tách *quyết định* khỏi *hành động* và CLI của bạn trở nên kiểm thử được — cùng
bài học mà capstone sẽ chấm bạn.
"""

L2 = """
Menus hard-code the conversation. **Arguments** let users speak first:

```bash
python todo.py add "buy milk"
python todo.py list
```

The stdlib module for this is `argparse` — here is the beginner slice:

```python
import argparse

parser = argparse.ArgumentParser(description="Todo CLI")
parser.add_argument("action", choices=["add", "list", "done"])
parser.add_argument("text", nargs="?")     # optional extra word(s)
args = parser.parse_args()

print(args.action, args.text)
```

`parse_args()` reads `sys.argv` for you, validates choices, and even prints
usage help with `-h`. Wrong usage exits with a clear error instead of crashing
with a traceback — professional behavior for free.
"""

L2_VI = """
Menu ép cứng cuộc hội thoại. **Tham số dòng lệnh** cho phép người dùng nói trước:

```bash
python todo.py add "mua sữa"
python todo.py list
```

Module thư viện chuẩn cho việc này là `argparse` — đây là phần cơ bản:

```python
import argparse

parser = argparse.ArgumentParser(description="Todo CLI")
parser.add_argument("action", choices=["add", "list", "done"])
parser.add_argument("text", nargs="?")     # từ/cụm từ bổ sung tùy chọn
args = parser.parse_args()

print(args.action, args.text)
```

`parse_args()` đọc `sys.argv` giúp bạn, kiểm tra choices, và thậm chí in hướng
dẫn với `-h`. Dùng sai thoát với thông báo lỗi rõ ràng thay vì sập với
traceback — hành vi chuyên nghiệp miễn phí.
"""

L3 = """
Everything you have learned converges into an application shape:

```
todo/
  app.py        # menu loop, argparse — the "controller"
  storage.py    # load_tasks() / save_tasks() — JSON file I/O
  models.py     # the task dict shape + validation helpers
  tests.py      # asserts over add/complete/delete logic
```

Rules that keep it sane:

- **Functions take data in and return data out** — `add_task(tasks, text)`,
  never a function that reaches into globals.
- **All file access lives in storage.** Swap JSON for a database later; nothing
  else changes.
- **Validate at the edges.** Bad input is rejected once, at the boundary, with
  a clear message.
- **The menu loop is the dumbest part of the program.** Logic belongs below.

The capstone asks you to invent this structure yourself. This module is the
rehearsal.
"""

L3_VI = """
Mọi thứ bạn đã học hội tụ thành một hình dạng ứng dụng:

```
todo/
  app.py        # vòng lặp menu, argparse — "bộ điều khiển"
  storage.py    # load_tasks() / save_tasks() — I/O tệp JSON
  models.py     # hình dạng dict task + các hàm kiểm tra hợp lệ
  tests.py      # assert trên logic add/complete/delete
```

Các quy tắc giữ cho nó tỉnh táo:

- **Hàm nhận dữ liệu vào và trả dữ liệu ra** — `add_task(tasks, text)`, không
  bao giờ là hàm với tay vào biến toàn cục.
- **Mọi truy cập tệp nằm trong storage.** Đổi JSON sang cơ sở dữ liệu sau này;
  không gì khác thay đổi.
- **Kiểm tra hợp lệ ở biên giới.** Đầu vào xấu bị từ chối một lần, tại biên,
  với thông báo rõ ràng.
- **Vòng lặp menu là phần ngu nhất của chương trình.** Logic nằm bên dưới.

Capstone yêu cầu bạn tự nghĩ ra cấu trúc này. Module này là buổi diễn tập.
"""

# ── Practices ────────────────────────────────────────────────────────────────
write_practice(
    MOD, "m14-task-functions-practice",
    "Task-Function Drills",
    "The pure logic of a task manager — no menu, just functions.",
    "Bài tập hàm task",
    "Logic thuần của trình quản lý công việc — không menu, chỉ hàm.",
    "cli-input-menus", 30, "beginner",
    [
        challenge(
            "py-cli-add-task",
            "add_task",
            "Write add_task(tasks, text) that APPENDS {\"text\": text, \"done\": False} to a copy of tasks and returns the new list. Do not mutate the input list.",
            "",
            [("adds without mutating", 'original = []\nresult = add_task(original, "buy milk")\nassert result == [{"text": "buy milk", "done": False}], f"got {result}"\nassert original == [], "input list must NOT be mutated"\nassert add_task(result, "walk dog")[-1]["text"] == "walk dog", "chains on the result"',
              'new = list(tasks); new.append({...}); return new — or tasks + [item].')],
            level="imitation",
        ),
        challenge(
            "py-cli-complete-task",
            "complete_task",
            "Write complete_task(tasks, index) marking the task at index done, on a COPY, and returning it. Out-of-range index: return the copy unchanged.",
            "",
            [("completes safely", 'tasks = [{"text": "a", "done": False}, {"text": "b", "done": False}]\nr = complete_task(tasks, 1)\nassert r[1]["done"] is True and r[0]["done"] is False, f"got {r}"\nassert tasks[1]["done"] is False, "input unchanged"\nassert complete_task(tasks, 99) == tasks, "out of range -> unchanged copy"\nassert complete_task(tasks, -1) == tasks, "negative index is out of range here"',
              "if not (0 <= index < len(tasks)): return list(tasks) — then copy-and-modify.")],
            level="guided",
        ),
        challenge(
            "py-cli-delete-task",
            "delete_task",
            "Write delete_task(tasks, index) returning (new_list, deleted_task). Out-of-range: ([], None) when tasks is empty, otherwise (copy unchanged, None).",
            "",
            [("deletes and reports", 'tasks = [{"text": "a", "done": False}, {"text": "b", "done": False}]\nnew, gone = delete_task(tasks, 0)\nassert gone == {"text": "a", "done": False} and new == [{"text": "b", "done": False}], f"got {new}, {gone}"\nnew2, gone2 = delete_task(tasks, 5)\nassert gone2 is None and new2 == tasks, "out of range -> (unchanged, None)"',
              "guard the index first; pop from a copy and return both values.")],
            level="guided",
        ),
        challenge(
            "py-cli-summary",
            "task_summary",
            "Write task_summary(tasks) returning the string 'X done / Y total'. Zero tasks: '0 done / 0 total'.",
            "",
            [("counts correctly", 'tasks = [{"text": "a", "done": True}, {"text": "b", "done": False}, {"text": "c", "done": True}]\nassert task_summary(tasks) == "2 done / 3 total", f"got {task_summary(tasks)}"\nassert task_summary([]) == "0 done / 0 total"',
              'done = sum(1 for t in tasks if t["done"]); f"{done} done / {len(tasks)} total"')],
            level="imitation",
        ),
    ],
    {
        "py-cli-add-task": vi_challenge("add_task", 'Viết add_task(tasks, text) nối thêm {"text": text, "done": False} vào một BẢN SAO của tasks và trả về danh sách mới. Không thay đổi danh sách đầu vào.',
                                        [("thêm mà không đổi bản gốc", 'new = list(tasks); new.append({...}); return new — hoặc tasks + [item].')]),
        "py-cli-complete-task": vi_challenge("complete_task", "Viết complete_task(tasks, index) đánh dấu task tại index là done, trên một BẢN SAO, và trả về nó. Index ngoài phạm vi: trả về bản sao không đổi.",
                                        [("hoàn thành an toàn", "if not (0 <= index < len(tasks)): return list(tasks) — rồi sao chép-và-sửa.")]),
        "py-cli-delete-task": vi_challenge("delete_task", "Viết delete_task(tasks, index) trả về (danh_sách_mới, task_bị_xóa). Ngoài phạm vi: ([], None) khi tasks rỗng, còn không (bản sao không đổi, None).",
                                        [("xóa và báo cáo", "chặn index trước; pop từ bản sao và trả về cả hai giá trị.")]),
        "py-cli-summary": vi_challenge("task_summary", "Viết task_summary(tasks) trả về chuỗi 'X done / Y total'. Không có task: '0 done / 0 total'.",
                                        [('đếm đúng', 'done = sum(1 for t in tasks if t["done"]); f"{done} done / {len(tasks)} total"')]),
    },
    solutions=[
        ("py-cli-add-task", 'def add_task(tasks, text):\n    return tasks + [{"text": text, "done": False}]',
         'def add_task(tasks, text):\n    tasks.append({"text": text, "done": False})\n    return tasks'),
        ("py-cli-complete-task", 'def complete_task(tasks, index):\n    if not (0 <= index < len(tasks)):\n        return list(tasks)\n    new = [dict(t) for t in tasks]\n    new[index]["done"] = True\n    return new',
         'def complete_task(tasks, index):\n    new = [dict(t) for t in tasks]\n    new[index]["done"] = True\n    return new'),
        ("py-cli-delete-task", 'def delete_task(tasks, index):\n    if not (0 <= index < len(tasks)):\n        return list(tasks), None\n    new = list(tasks)\n    return new, new.pop(index)',
         'def delete_task(tasks, index):\n    new = list(tasks)\n    return new, new.pop(index)'),
        ("py-cli-summary", 'def task_summary(tasks):\n    done = sum(1 for t in tasks if t["done"])\n    return f"{done} done / {len(tasks)} total"',
         'def task_summary(tasks):\n    done = sum(1 for t in tasks)\n    return f"{done} done / {len(tasks)} total"'),
    ],
)

write_practice(
    MOD, "m14-persistence-menu-practice",
    "Mini Build: Persistent Task Manager Core",
    "Load, mutate, save — the storage half of every CLI app.",
    "Mini build: Lõi trình quản lý công việc có lưu trữ",
    "Nạp, thay đổi, lưu — nửa lưu trữ của mọi ứng dụng CLI.",
    "persistence-errors", 40, "beginner",
    [
        challenge(
            "py-cli-load-or-default",
            "load_tasks with a Default",
            "Write load_tasks(path) that returns the parsed JSON list when the file exists and [] when it does not (use pathlib + json).",
            "",
            [            ("missing file tolerated", 'import json as _j, os as _os\nif _os.path.exists("tm_probe.json"):\n    _os.remove("tm_probe.json")\nassert load_tasks("tm_probe.json") == [], "missing file -> []"\n_j.dump([{"text": "x", "done": True}], open("tm_probe.json", "w"))\nassert load_tasks("tm_probe.json") == [{"text": "x", "done": True}], "existing file is parsed"\n_os.remove("tm_probe.json")\nassert "Path" in code or "os.path" in code or "exists" in code, "check existence"',
              'from pathlib import Path; if not Path(path).exists(): return []; then json.load.'),
            ("bad json tolerated (stretch)", 'import os as _os\nopen("tm_bad.json", "w").write("{not json")\n_ok = False\ntry:\n    r = load_tasks("tm_bad.json")\n    _ok = r == []\nexcept Exception:\n    _ok = True\n_os.remove("tm_bad.json")\nassert _ok, "corrupt file must either fall back to [] or raise a handled json error"',
              "wrap json.load in try/except and return [] — a strict load is also acceptable.")],
            level="guided",
        ),
        challenge(
            "py-cli-save-roundtrip",
            "save_tasks Roundtrip",
            "Write save_tasks(path, tasks) writing JSON (ensure_ascii=False, indent=2), then a test-visible roundtrip: after calling save_tasks(\"tm_rt.json\", tasks) with tasks = [{\"text\": \"viết báo cáo\", \"done\": False}], load_tasks(\"tm_rt.json\") must equal tasks. Print the loaded task count (one line).",
            "",
            [("roundtrip holds", 'import json as _j\nwith open("tm_rt.json", encoding="utf-8") as _f:\n    _d = _j.load(_f)\nassert _d == [{"text": "viết báo cáo", "done": False}], f"got {_d}"\nassert printed[0] == "1", f"got {printed}"\nassert "ensure_ascii=False" in code, "keep Vietnamese readable"',
              "save with json.dump(..., ensure_ascii=False, indent=2); load and print len().")],
            level="guided",
        ),
        challenge(
            "py-cli-menu-step",
            "The Menu Step Function",
            "Write handle(tasks, choice, arg) — one iteration of a task-manager menu: 'add' -> add arg (default 'untitled'), 'done' -> complete index int(arg) (invalid int or range: unchanged), 'clear' -> remove all done tasks, anything else -> unchanged. handle NEVER prints. Returns the (possibly new) list.",
            "",
            [("one menu iteration", 't0 = [{"text": "a", "done": False}]\nt1 = handle(t0, "add", "email")\nassert t1[-1] == {"text": "email", "done": False}, f"add: {t1}"\nassert handle(t0, "add")[-1]["text"] == "untitled", "missing arg -> untitled"\nt2 = handle(t1, "done", "0")\nassert t2[0]["done"] is True, f"done: {t2}"\nassert handle(t1, "done", "99") == t1, "bad index -> unchanged"\nassert handle(t1, "done", "x") == t1, "bad int -> unchanged"\nt3 = handle(t2, "clear", "")\nassert t3 == [{"text": "email", "done": False}], f"clear removes done only: {t3}"\nassert handle(t0, "nonsense", "") == t0, "unknown choice -> unchanged"',
              "int(arg) in try/except ValueError; reuse complete-style logic; 'clear' filters not t['done'].")],
            level="mini-build",
        ),
    ],
    {
        "py-cli-load-or-default": vi_challenge("load_tasks với mặc định", "Viết load_tasks(path) trả về danh sách JSON đã phân tích khi tệp tồn tại và [] khi không tồn tại (dùng pathlib + json).",
                                        [("tha thứ tệp thiếu", "from pathlib import Path; if not Path(path).exists(): return []; rồi json.load."),
                                         ("tha thứ json hỏng (nâng cao)", "bọc json.load trong try/except và trả về [] — bản load nghiêm ngặt cũng được chấp nhận.")]),
        "py-cli-save-roundtrip": vi_challenge("save_tasks khép kín", 'Viết save_tasks(path, tasks) ghi JSON (ensure_ascii=False, indent=2), rồi vòng lặp khép kín nhìn thấy được: sau khi gọi save_tasks("tm_rt.json", tasks) với tasks = [{"text": "viết báo cáo", "done": False}], load_tasks("tm_rt.json") phải bằng tasks. In số task đã nạp (một dòng).',
                                        [("vòng lặp khép kín", "lưu với json.dump(..., ensure_ascii=False, indent=2); nạp và in len().")]),
        "py-cli-menu-step": vi_challenge("Hàm một bước menu", "Viết handle(tasks, choice, arg) — một vòng lặp menu của trình quản lý task: 'add' -> thêm arg (mặc định 'untitled'), 'done' -> hoàn thành index int(arg) (int sai hoặc ngoài phạm vi: không đổi), 'clear' -> xóa mọi task đã done, ngoài ra -> không đổi. handle KHÔNG BAO GIỜ print. Trả về danh sách (có thể mới).",
                                        [("một vòng menu", "int(arg) trong try/except ValueError; dùng lại logic kiểu complete; 'clear' lọc các task chưa done.")]),
    },
    solutions=[
        ("py-cli-load-or-default", 'import json\nfrom pathlib import Path\n\n\ndef load_tasks(path):\n    p = Path(path)\n    if not p.exists():\n        return []\n    try:\n        with open(p, encoding="utf-8") as f:\n            return json.load(f)\n    except json.JSONDecodeError:\n        return []',
         'import json\n\n\ndef load_tasks(path):\n    with open(path, encoding="utf-8") as f:\n        return json.load(f)'),
        ("py-cli-save-roundtrip", 'import json\n\ntasks = [{"text": "viết báo cáo", "done": False}]\n\n\ndef save_tasks(path, ts):\n    with open(path, "w", encoding="utf-8") as f:\n        json.dump(ts, f, ensure_ascii=False, indent=2)\n\n\ndef load_tasks(path):\n    with open(path, encoding="utf-8") as f:\n        return json.load(f)\n\n\nsave_tasks("tm_rt.json", tasks)\nloaded = load_tasks("tm_rt.json")\nprint(len(loaded))',
         'import json\n\ntasks = [{"text": "viết báo cáo", "done": False}]\n\n\ndef save_tasks(path, ts):\n    with open(path, "w", encoding="utf-8") as f:\n        json.dump(ts, f, ensure_ascii=True, indent=2)\n\n\ndef load_tasks(path):\n    with open(path, encoding="utf-8") as f:\n        return json.load(f)\n\n\nsave_tasks("tm_rt.json", tasks)\nloaded = load_tasks("tm_rt.json")\nprint(len(loaded))'),
        ("py-cli-menu-step", 'def handle(tasks, choice, arg=""):\n    if choice == "add":\n        return tasks + [{"text": arg or "untitled", "done": False}]\n    if choice == "done":\n        try:\n            idx = int(arg)\n        except ValueError:\n            return list(tasks)\n        if not (0 <= idx < len(tasks)):\n            return list(tasks)\n        new = [dict(t) for t in tasks]\n        new[idx]["done"] = True\n        return new\n    if choice == "clear":\n        return [t for t in tasks if not t["done"]]\n    return list(tasks)',
         'def handle(tasks, choice, arg=""):\n    if choice == "add":\n        return tasks + [{"text": arg or "untitled", "done": False}]\n    if choice == "done":\n        idx = int(arg)\n        new = [dict(t) for t in tasks]\n        new[idx]["done"] = True\n        return new\n    if choice == "clear":\n        return [t for t in tasks if not t["done"]]\n    return list(tasks)'),
    ],
)

print("module 14 content written")
