#!/usr/bin/env python3
"""C++ Beginner course shell: cpp track registration + course manifests (EN+VI)."""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK_DIR = os.path.join(ROOT, "src/content/tracks/cpp")
BASE = os.path.join(TRACK_DIR, "courses/cpp-beginner")


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


# Track description must respect descriptionSchema max 400 chars (VI < 400,
# learned from the Course 2 VI 404 bug where an oversized VI field 404'd).
TRACK_EN = {
    "id": "cpp",
    "title": "C++",
    "description": (
        "Learn modern C++ from your very first compiled program to real, tested "
        "command-line applications. A practice-first path: write C++ from lesson "
        "one, read real compiler errors, and build a foundation of safe ownership "
        "and RAII habits that scales to professional codebases."
    ),
    "courses": [{"reference": "cpp-beginner"}],
}
TRACK_VI = {
    "title": "C++",
    "description": (
        "Học C++ hiện đại từ chương trình được biên dịch đầu tiên đến các ứng dụng "
        "dòng lệnh thực thụ, có kiểm thử. Lộ trình tập trung thực hành: viết C++ "
        "ngay từ bài học đầu, đọc thông báo lỗi của compiler, và xây nền tảng về "
        "sở hữu bộ nhớ an toàn cùng RAII để tiến tới code chuyên nghiệp."
    ),
}

COURSE_EN = {
    "id": "cpp-beginner",
    "title": "C++ Beginner",
    "description": (
        "Your first course in modern C++: compile and run real programs, master "
        "variables, control flow, functions, collections and the STL, model data "
        "with structs and classes, tame pointers safely, and finish by building a "
        "tested, multi-file Personal Finance Manager."
    ),
    "modules": [],  # filled by cppb_m*.py scripts in order
    "audience": (
        "Complete beginners who want a serious foundation, and Python or web "
        "developers who want C++'s compiled, statically typed, explicit-lifetime "
        "mental model explained from zero."
    ),
    "outcomes": [
        "Write, compile, run and debug modern C++ programs confidently",
        "Use variables, types, control flow, functions and const correctness",
        "Choose and use std::vector, std::map, std::set and STL algorithms",
        "Model data with structs, enum class and well-encapsulated classes",
        "Explain ownership, lifetime, RAII and smart pointers — and avoid raw new/delete",
        "Read and write files, test your code, and build a multi-file CMake project",
    ],
    "prerequisites": [],
}

COURSE_VI = {
    "title": "C++ — Cơ bản",
    "description": (
        "Khóa đầu tiên về C++ hiện đại: biên dịch và chạy chương trình thật, nắm "
        "vững biến, luồng điều khiển, hàm, collection và STL, mô hình hóa dữ liệu "
        "với struct và class, làm chủ con trỏ một cách an toàn, và kết thúc bằng "
        "cách xây ứng dụng Personal Finance Manager nhiều file, có kiểm thử."
    ),
    "audience": (
        "Người mới bắt đầu hoàn toàn, và lập trình viên Python/web muốn hiểu mô "
        "hình tư duy của C++: biên dịch, kiểu tĩnh và vòng đời tài nguyên tường minh."
    ),
    "outcomes": [
        "Tự tin viết, biên dịch, chạy và gỡ lỗi chương trình C++ hiện đại",
        "Dùng biến, kiểu dữ liệu, luồng điều khiển, hàm và const đúng cách",
        "Lựa chọn và sử dụng std::vector, std::map, std::set cùng thuật toán STL",
        "Mô hình hóa dữ liệu với struct, enum class và class đóng gói tốt",
        "Giải thích ownership, lifetime, RAII và smart pointer — tránh new/delete thô",
        "Đọc/ghi file, viết kiểm thử và xây dự án CMake nhiều file",
    ],
}

if __name__ == "__main__":
    _w(os.path.join(TRACK_DIR, "track.json"), _j(TRACK_EN))
    _w(os.path.join(TRACK_DIR, "track.vi.json"), _j(TRACK_VI))
    _w(os.path.join(BASE, "course.json"), _j(COURSE_EN))
    _w(os.path.join(BASE, "course.vi.json"), _j(COURSE_VI))
    print("cpp track + cpp-beginner course shell written")
