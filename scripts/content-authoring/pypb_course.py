#!/usr/bin/env python3
"""Track + course skeleton for the Python — Beginner course."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypb import _w, _j, TRACK, BASE

_w(
    os.path.join(TRACK, "track.json"),
    _j(
        {
            "id": "python",
            "title": "Python",
            "description": "Learn to program with Python — from your very first script to real command-line applications. A practice-first path: write code from lesson one, debug real programs, and build tools you can actually use.",
            "courses": [{"reference": "python-beginner"}],
        }
    ),
)
_w(
    os.path.join(TRACK, "track.vi.json"),
    _j(
        {
            "title": "Python",
            "description": "Học lập trình với Python — từ đoạn mã đầu tiên đến các ứng dụng dòng lệnh thực dụng. Lộ trình tập trung vào thực hành: viết code ngay từ bài học đầu tiên, gỡ lỗi chương trình thật, và xây dựng công cụ dùng được.",
        }
    ),
)

_w(
    os.path.join(BASE, "course.json"),
    _j(
        {
            "id": "python-beginner",
            "title": "Python — Beginner",
            "description": "Go from never having programmed to writing real Python: variables, strings, collections, loops, functions, files, modules, testing, and your own command-line applications — with practice at every step.",
            "modules": [],  # filled by module scripts in order
            "audience": "Absolute beginners who want to learn programming through Python — no prior experience needed. If you can use a computer, you can start here; by the end you will write small, useful programs on your own.",
            "outcomes": [
                "Run Python three ways: the interpreter, the REPL, and .py script files",
                "Use variables and core data types — int, float, str, bool, None — with confident conversions",
                "Manipulate text: indexing, slicing, string methods, and f-string formatting",
                "Make decisions with if/elif/else, truthiness, and boolean logic",
                "Work with lists, tuples, sets, and dictionaries — and pick the right container",
                "Write loops: for, while, range, break/continue, and accumulator patterns",
                "Decompose problems into functions with parameters, returns, and docstrings",
                "Read tracebacks, debug systematically, and handle errors with try/except",
                "Read and write files, work with paths (pathlib), CSV, and JSON",
                "Import and create modules; use math, random, datetime, statistics, and Counter",
                "Create virtual environments and install packages with pip",
                "Write assertions and basic automated tests; make broken tests pass",
                "Break problems into inputs → processing → outputs and solve them step by step",
                "Build and organize your own command-line applications with persistence",
            ],
            "prerequisites": [],
            "estimatedMinutes": 2280,
            "nextCourse": "python-intermediate (coming soon)",
        }
    ),
)
_w(
    os.path.join(BASE, "course.vi.json"),
    _j(
        {
            "title": "Python — Cơ bản",
            "description": "Từ người chưa từng lập trình đến việc viết Python thực thụ: biến, chuỗi, danh sách, vòng lặp, hàm, tệp, module, kiểm thử, và ứng dụng dòng lệnh của riêng bạn — với bài tập thực hành ở mỗi bước.",
            "audience": "Người mới hoàn toàn muốn học lập trình qua Python — không cần kinh nghiệm trước đó. Bạn chỉ cần biết sử dụng máy tính; đến cuối khóa bạn sẽ tự viết được những chương trình nhỏ, hữu ích.",
            "outcomes": [
                "Chạy Python theo ba cách: trình thông dịch, REPL, và tệp .py",
                "Dùng biến và các kiểu dữ liệu cơ bản — int, float, str, bool, None — chuyển đổi tự tin",
                "Xử lý văn bản: indexing, slicing, phương thức chuỗi, và định dạng f-string",
                "Ra quyết định với if/elif/else, truthiness, và logic boolean",
                "Làm việc với list, tuple, set, dictionary — và chọn đúng kiểu chứa dữ liệu",
                "Viết vòng lặp: for, while, range, break/continue, và mẫu tích lũy (accumulator)",
                "Tách bài toán thành các hàm với tham số, giá trị trả về, và docstring",
                "Đọc traceback, gỡ lỗi có hệ thống, và xử lý ngoại lệ với try/except",
                "Đọc/ghi tệp, làm việc với đường dẫn (pathlib), CSV, và JSON",
                "Import và tự tạo module; dùng math, random, datetime, statistics, Counter",
                "Tạo môi trường ảo (venv) và cài đặt gói bằng pip",
                "Viết assertion và kiểm thử cơ bản; sửa các bài kiểm thử bị lỗi",
                "Phân tích bài toán thành đầu vào → xử lý → đầu ra và giải quyết từng bước",
                "Xây dựng và tổ chức ứng dụng dòng lệnh có lưu trữ dữ liệu",
            ],
            "prerequisites": [],
            "nextCourse": "python-intermediate (sắp ra mắt)",
        }
    ),
)
print("track + course skeleton written")
