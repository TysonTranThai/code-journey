#!/usr/bin/env python3
"""Emit the missing python-beginner module manifests + course module list.

The pypb_m*.py generators wrote lessons/practices but never called
write_module (the course.json "filled by module scripts in order" step),
leaving the tree unloadable. This script completes ONLY that missing step:
it reuses pypb.write_module (same format) and derives each module's
lesson/practice order from the m*.py call sites. No content is invented
beyond short module title/summary metadata, EN + VI.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pypb import write_module, BASE  # noqa: E402

COURSE = os.path.join(BASE, "course.json")

META = {
    "python-and-your-first-programs": (
        "Python and Your First Programs",
        "Meet Python, run your first scripts, print real output, and learn to read the errors every programmer meets.",
        "Python và những chương trình đầu tiên",
        "Làm quen Python, chạy script đầu tiên, in kết quả thật, và học đọc những lỗi mà mọi lập trình viên đều gặp.",
    ),
    "variables-and-data-types": (
        "Variables and Data Types",
        "Store and transform data: numbers, booleans, None, conversions, and operator precedence.",
        "Biến và kiểu dữ liệu",
        "Lưu trữ và biến đổi dữ liệu: số, boolean, None, chuyển đổi kiểu, và độ ưu tiên toán tử.",
    ),
    "working-with-strings": (
        "Working with Strings",
        "Index, slice, transform, and format text with confidence.",
        "Làm việc với chuỗi",
        "Index, cắt, biến đổi và định dạng văn bản một cách tự tin.",
    ),
    "making-decisions": (
        "Making Decisions",
        "Branch with if/elif/else, master truthiness and boolean logic, and validate real input.",
        "Ra quyết định",
        "Rẽ nhánh với if/elif/else, làm chủ truthiness và logic boolean, kiểm tra dữ liệu nhập thật.",
    ),
    "lists-and-collections": (
        "Lists and Collections",
        "Lists, tuples, sets, dictionaries, and nested structures — and choosing the right container.",
        "Danh sách và collection",
        "List, tuple, set, dictionary và cấu trúc lồng nhau — và cách chọn đúng kiểu chứa.",
    ),
    "loops": (
        "Loops",
        "Repeat work deliberately: for, while, range, break/continue, and accumulator patterns.",
        "Vòng lặp",
        "Lặp lại công việc có chủ đích: for, while, range, break/continue, và các mẫu tích lũy.",
    ),
    "functions": (
        "Functions",
        "Decompose problems into reusable pieces: parameters, returns, defaults, scope, docstrings.",
        "Hàm",
        "Tách bài toán thành các mảnh dùng lại được: tham số, giá trị trả về, mặc định, scope, docstring.",
    ),
    "errors-and-debugging": (
        "Errors and Debugging",
        "Read tracebacks, handle exceptions precisely, fail fast, and debug with a method — then repair real broken programs in the Bug Hunt.",
        "Lỗi và gỡ lỗi",
        "Đọc traceback, xử lý ngoại lệ chính xác, fail fast, gỡ lỗi có phương pháp — rồi sửa các chương trình hỏng thật trong Bug Hunt.",
    ),
    "files-paths-and-data": (
        "Files, Paths and Data",
        "Make work survive: read and write files, CSV, JSON persistence, and pathlib.",
        "Tệp, đường dẫn và dữ liệu",
        "Khiến công việc tồn tại bền vững: đọc ghi tệp, CSV, lưu trữ JSON, và pathlib.",
    ),
    "modules-and-standard-library": (
        "Modules and the Standard Library",
        "Import, build your own modules, and borrow power from math, random, datetime, statistics, and Counter.",
        "Module và thư viện chuẩn",
        "Import, tự xây module, và mượn sức mạnh từ math, random, datetime, statistics, và Counter.",
    ),
    "environments-and-packages": (
        "Environments and Packages",
        "Virtual environments, pip, and requirements.txt — dependency judgment for real projects.",
        "Môi trường và gói",
        "Môi trường ảo, pip, và requirements.txt — phán đoán phụ thuộc cho dự án thật.",
    ),
    "testing-and-code-quality": (
        "Testing and Code Quality",
        "Assert what must be true, test the edges, write your own tests, and write code worth testing.",
        "Kiểm thử và chất lượng mã",
        "Assert điều gì phải đúng, kiểm tra biên, tự viết bài kiểm thử, và viết mã xứng đáng được kiểm thử.",
    ),
    "problem-solving-fundamentals": (
        "Problem Solving Fundamentals",
        "Inputs, outputs, pseudocode, the accumulator toolbox, complexity intuition, and AI as a verified assistant.",
        "Nền tảng giải quyết vấn đề",
        "Đầu vào, đầu ra, pseudocode, hộp công cụ accumulator, trực giác độ phức tạp, và AI là trợ lý được kiểm chứng.",
    ),
    "command-line-applications": (
        "Command-Line Applications",
        "Menus, arguments, persistence, and the layered shape of a real CLI tool.",
        "Ứng dụng dòng lệnh",
        "Menu, tham số, lưu trữ, và hình dạng phân tầng của một công cụ CLI thật.",
    ),
    "capstone-personal-finance-cli": (
        "Capstone: Personal Finance CLI",
        "Build from requirements: design, persist, test, and ship your own expense tracker — no tutorial, your decisions.",
        "Capstone: CLI Tài chính cá nhân",
        "Xây từ yêu cầu: thiết kế, lưu trữ, kiểm thử, và đóng gói trình theo dõi chi tiêu của riêng bạn — không hướng dẫn từng bước, mọi quyết định thuộc về bạn.",
    ),
}

MODS = [
    "python-and-your-first-programs",
    "variables-and-data-types",
    "working-with-strings",
    "making-decisions",
    "lists-and-collections",
    "loops",
    "functions",
    "errors-and-debugging",
    "files-paths-and-data",
    "modules-and-standard-library",
    "environments-and-packages",
    "testing-and-code-quality",
    "problem-solving-fundamentals",
    "command-line-applications",
    "capstone-personal-finance-cli",
]


def call_order(script, fn_names):
    """Ordered first-string args of write_lesson/write_practice/write_checkpoint calls."""
    ids = []
    src = open(os.path.join(HERE, script), encoding="utf-8").read()
    pattern = re.compile(
        r"write_(lesson|practice|checkpoint)\(\s*(?:MOD,\s*)?\"([a-z0-9-]+)\""
    )
    for match in pattern.finditer(src):
        fn, ident = match.group(1), match.group(2)
        if fn in fn_names:
            ids.append(ident)
    return ids


def lesson_ids_from_emit_plan(mod):
    """Lesson ids for modules 8-15, whose lessons live in pypb_emit_lessons.py's PLAN."""
    src = open(os.path.join(HERE, "pypb_emit_lessons.py"), encoding="utf-8").read()
    ids = []
    pattern = re.compile(
        r"\(\"([a-z0-9-]+)\", \"([a-z0-9-]+)\", \"([^\"]*)\","
    )
    for match in pattern.finditer(src):
        mod_id, lid = match.group(1), match.group(2)
        if mod_id == mod:
            ids.append(lid)
    return ids


for mod in MODS:
    mfile = f"pypb_m{MODS.index(mod) + 1}.py"
    lessons = call_order(mfile, {"lesson"})
    if not lessons:
        lessons = lesson_ids_from_emit_plan(mod)
    # checkpoints live in the module scripts; merge after plan lessons, dedup
    for cp in call_order(mfile, {"checkpoint"}):
        if cp not in lessons:
            lessons.append(cp)
    practices = call_order(mfile, {"practice"})
    # keep only ids that actually exist on disk (post-_fix_ state is authoritative)
    les_dir = os.path.join(BASE, "modules", mod, "lessons")
    lessons = [l for l in lessons if os.path.exists(os.path.join(les_dir, l + ".json"))]
    pra_dir = os.path.join(BASE, "modules", mod, "practices")
    practices = [p for p in practices if os.path.exists(os.path.join(pra_dir, p + ".json"))]
    title, summary, vi_title, vi_summary = META[mod]
    print(f"manifest {mod}: {len(lessons)} lessons, {len(practices)} practices")
    write_module(mod, title, summary, vi_title, vi_summary, lessons, practices)

# fill course.json's module list, preserving every other field
course = json.load(open(COURSE, encoding="utf-8"))
course["modules"] = [{"reference": m} for m in MODS]
with open(COURSE, "w", encoding="utf-8") as f:
    json.dump(course, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("course.json modules:", [m["reference"] for m in course["modules"]])
