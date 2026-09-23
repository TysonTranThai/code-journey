#!/usr/bin/env python3
"""Write the ap-csa-beginner course manifest (EN + VI) and the ap-csa track registration files."""
import io
import json
import os

BASE = os.path.join("src", "content", "tracks", "ap-csa", "courses", "ap-csa-beginner")
TRACK = os.path.join("src", "content", "tracks", "ap-csa")


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def _w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)


course = {
    "id": "ap-csa-beginner",
    "title": "AP CSA Foundations",
    "description": "Build the complete Java foundation for AP Computer Science A: syntax, types, control flow, methods, strings, classes and objects, arrays, ArrayList, 2D arrays, recursion, testing and debugging, and the reading-and-writing habits the exam's four free-response types reward. Aligned to the revised (Fall 2025) AP CSA framework.",
    "audience": "Students preparing for AP Computer Science A, including complete beginners and programmers from other languages who are new to Java. No prior Java assumed; Algebra 1 comfort is enough.",
    "outcomes": [
        "Read and trace unfamiliar Java programs, predicting output and state",
        "Write methods from prose specifications, honoring preconditions and postconditions",
        "Design classes with private fields, constructors, accessors, and behavior methods",
        "Use arrays, ArrayList, and 2D arrays with correct traversal and mutation discipline",
        "Implement searching, sorting, and accumulation algorithms and reason about their cost",
        "Apply recursion with correct base cases and progress",
        "Classify and debug compile-time, runtime, and logical errors systematically",
        "Recognize the exam's recurring patterns: accumulator, state machine, select-transform",
    ],
    "prerequisites": [],
    "modules": [{"reference": m} for m in [
        "apc-hello", "apc-variables", "apc-expressions", "apc-conditionals",
        "apc-loops", "apc-methods", "apc-strings", "apc-classes",
        "apc-arrays", "apc-arraylist", "apc-searchsort", "apc-oop-design",
        "apc-inheritance", "apc-recursion", "apc-2d", "apc-testing",
        "apc-reasoning", "apc-frq", "apc-integration", "apc-readiness",
    ]],
}

course_vi = {
    "title": "Nền tảng AP CSA",
    "description": "Xây nền tảng Java đầy đủ cho AP Computer Science A: cú pháp, kiểu dữ liệu, luồng điều khiển, phương thức, chuỗi, lớp và đối tượng, mảng, ArrayList, mảng hai chiều, đệ quy, kiểm thử và gỡ lỗi, cùng thói quen đọc-viết mã mà bốn dạng tự luận của kỳ thi thưởng thức. Bám khung AP CSA sửa đổi (mùa thu 2025).",
    "audience": "Học sinh chuẩn bị thi AP Computer Science A, gồm cả người mới bắt đầu hoàn toàn và người đã biết ngôn ngữ khác nhưng mới với Java. Không đòi hỏi biết Java trước; thoải mái Đại số 1 là đủ.",
    "outcomes": [
        "Đọc và truy vết mã Java lạ, đoán trước đầu ra và trạng thái",
        "Viết phương thức từ đặc tả văn bản, tôn trọng điều kiện tiền và hậu",
        "Thiết kế lớp với trường private, hàm dựng, accessor, và phương thức hành vi",
        "Dùng mảng, ArrayList, mảng hai chiều với kỷ luật duyệt và biến đổi đúng",
        "Cài thuật toán tìm kiếm, sắp xếp, cộng dồn và lý giải chi phí của chúng",
        "Áp dụng đệ quy với điều kiện dừng và bước tiến đúng",
        "Phân loại và gỡ lỗi biên dịch, runtime, logic một cách có hệ thống",
        "Nhận ra các mẫu hình lặp lại của đề: bộ tích lũy, máy trạng thái, chọn-biến-đổi",
    ],
}

assert len(course["description"]) <= 400, len(course["description"])
assert len(course["audience"]) <= 400, len(course["audience"])
assert len(course_vi["description"]) <= 400, len(course_vi["description"])
assert len(course_vi["audience"]) <= 400, len(course_vi["audience"])
for o in course["outcomes"] + course_vi["outcomes"]:
    assert len(o) <= 200, o

_w(os.path.join(BASE, "course.json"), _j(course))
_w(os.path.join(BASE, "course.vi.json"), _j(course_vi))

track = {
    "id": "ap-csa",
    "title": "AP Computer Science A",
    "description": "Java programming for the AP Computer Science A exam: foundations, object-oriented design, data collections, and exam-shape problem solving — aligned to the revised (Fall 2025) AP CSA framework.",
    "courses": [{"reference": "ap-csa-beginner"}],
}

track_vi = {
    "title": "AP Computer Science A",
    "description": "Lập trình Java cho kỳ thi AP Computer Science A: nền tảng, thiết kế hướng đối tượng, bộ sưu tập dữ liệu, và giải bài đúng hình dạng đề thi — bám khung AP CSA sửa đổi (mùa thu 2025).",
}

assert len(track["description"]) <= 400, len(track["description"])
assert len(track_vi["description"]) <= 400, len(track_vi["description"])

_w(os.path.join(TRACK, "track.json"), _j(track))
_w(os.path.join(TRACK, "track.vi.json"), _j(track_vi))

print("course + track manifests written")
