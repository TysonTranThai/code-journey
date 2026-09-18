#!/usr/bin/env python3
"""Java — Beginner: track + course skeleton (java track, course 1).

Creates src/content/tracks/java/{track.json,track.vi.json} and
courses/java-beginner/{course.json,course.vi.json} following the exact shape
of the cpp/python tracks, and appends the course to
scripts/content-authoring/validate-content.ts's COURSE_TRACKS list
(read-modify-write; other agents' entries preserved).
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import TRACK, BASE, _w, _j  # noqa: E402

VALIDATOR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "scripts/content-authoring/validate-content.ts",
)

# ── track.json ───────────────────────────────────────────────────────────────
_w(
    os.path.join(TRACK, "track.json"),
    _j(
        {
            "id": "java",
            "title": "Java",
            "description": (
                "Learn Java from your very first compiled program to real, tested "
                "command-line applications. A practice-first path: write Java from "
                "lesson one, read real compiler errors and stack traces, and build a "
                "foundation of object-oriented design, collections, and modern Java "
                "idioms that scales to professional codebases."
            ),
            "courses": [{"reference": "java-beginner"}],
        }
    ),
)
_w(
    os.path.join(TRACK, "track.vi.json"),
    _j(
        {
            "title": "Java",
            "description": (
                "Học Java từ chương trình được biên dịch đầu tiên đến các ứng dụng "
                "dòng lệnh thực thụ, có kiểm thử. Lộ trình tập trung thực hành: viết "
                "Java ngay từ bài học đầu, đọc thông báo lỗi của compiler và stack "
                "trace, và xây nền tảng thiết kế hướng đối tượng, collection, và "
                "thành ngữ Java hiện đại để tiến tới code chuyên nghiệp."
            ),
        }
    ),
)
print("track: java")

# ── course.json ──────────────────────────────────────────────────────────────
_w(
    os.path.join(BASE, "course.json"),
    _j(
        {
            "id": "java-beginner",
            "title": "Java — Beginner",
            "description": (
                "Start programming with Java: the compile-run model, types and "
                "control flow, methods, classes and objects, collections, generics, "
                "exceptions, files, streams, tests, and Maven — writing real Java "
                "from the first lesson to a full capstone application."
            ),
            "modules": [],
            "audience": (
                "New programmers and developers from other languages who want a solid, "
                "modern Java foundation — no prior Java, OOP, or build-tool experience "
                "assumed."
            ),
            "outcomes": [
                "Explain the JVM model: source, bytecode, compilation, and execution",
                "Write, compile, and run Java programs with confidence in the standard toolchain",
                "Use Java's primitive types, String, operators, and control flow fluently",
                "Decompose problems into well-designed methods with clear parameters and returns",
                "Work with arrays, String APIs, and StringBuilder for real text and data tasks",
                "Model problems with classes, encapsulation, inheritance, interfaces, and polymorphism",
                "Choose between classes, records, and enums for modern data modeling",
                "Use the Collections Framework (List, Set, Map, Deque) and pick the right one",
                "Write and use generic classes and methods for type-safe reusable code",
                "Handle failures with exceptions: try/catch/finally, custom types, stack traces",
                "Read and write files with java.nio.file and persist application data",
                "Use lambdas, method references, and streams where they beat plain loops",
                "Test code with JUnit-style assertions, cover edge cases, and debug systematically",
                "Read and write pom.xml, explain the Maven lifecycle, and structure a professional project",
                "Organize code into packages with clean visibility and call HTTP APIs from Java",
            ],
            "prerequisites": [],
        }
    ),
)
_w(
    os.path.join(BASE, "course.vi.json"),
    _j(
        {
            "title": "Java — Cơ bản",
            "description": (
                "Bắt đầu lập trình với Java: mô hình biên dịch–chạy, kiểu dữ liệu và "
                "luồng điều khiển, phương thức, class và đối tượng, collection, "
                "generic, exception, file, stream, kiểm thử, và Maven — viết Java "
                "thật từ bài học đầu đến ứng dụng capstone hoàn chỉnh."
            ),
            "audience": (
                "Người mới lập trình và dev chuyển từ ngôn ngữ khác muốn có nền tảng "
                "Java hiện đại vững chắc — không yêu cầu biết trước Java, OOP, hay "
                "build tool."
            ),
            "outcomes": [
                "Giải thích mô hình JVM: mã nguồn, bytecode, biên dịch, và thực thi",
                "Viết, biên dịch, và chạy chương trình Java tự tin với công cụ chuẩn",
                "Dùng thành thạo kiểu primitive, String, toán tử, và luồng điều khiển của Java",
                "Phân rã bài toán thành phương thức gọn với tham số và giá trị trả về rõ ràng",
                "Xử lý mảng, API của String, và StringBuilder cho các tác vụ văn bản, dữ liệu thật",
                "Mô hình hóa bài toán bằng class, đóng gói, kế thừa, interface, và đa hình",
                "Chọn giữa class, record, và enum để mô hình hóa dữ liệu hiện đại",
                "Dùng Collections Framework (List, Set, Map, Deque) và chọn đúng loại",
                "Viết và dùng generic class/method để tái sử dụng code an toàn kiểu",
                "Xử lý lỗi bằng exception: try/catch/finally, kiểu riêng, đọc stack trace",
                "Đọc và ghi file bằng java.nio.file, lưu dữ liệu ứng dụng",
                "Dùng lambda, method reference, và stream ở nơi chúng tốt hơn vòng lặp thường",
                "Kiểm thử bằng assertion kiểu JUnit, phủ cạnh biên, và gỡ lỗi có hệ thống",
                "Đọc và viết pom.xml, giải thích vòng đời Maven, cấu trúc project chuyên nghiệp",
                "Tổ chức code thành package với phạm vi truy cập sạch, và gọi HTTP API từ Java",
            ],
        }
    ),
)
print("course: java-beginner")

# ── validator entry (preserve other agents' lines) ──────────────────────────
src = io.open(VALIDATOR, encoding="utf-8").read()
anchor = '  { track: "cpp", course: "cpp-intermediate" },'
entry = '  { track: "java", course: "java-beginner" },'
if "java-beginner" not in src:
    assert anchor in src, "validator anchor missing"
    src = src.replace(anchor, anchor + "\n" + entry, 1)
    _w(VALIDATOR, src)
    print("validator: java-beginner added")
else:
    print("validator: java-beginner already present")
