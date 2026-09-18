#!/usr/bin/env python3
"""Course skeleton for C++ — Intermediate: course.json + VI overlay + track wiring."""
import io
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cppi import _w, _j, BASE

COURSE_ID = "cpp-intermediate"

_w(
    os.path.join(BASE, "course.json"),
    _j(
        {
            "id": COURSE_ID,
            "title": "C++ — Intermediate",
            "description": "Move from writing C++ to engineering it: memory and lifetime, object-oriented design, the STL, smart pointers, templates, and data structures — with practice at every step.",
            "modules": [],
            "audience": "Learners who finished C++ — Beginner and want to design real C++ programs: classes with clean ownership, the STL used fluently, templates, and data structures built from scratch.",
            "outcomes": [
                "Reason about memory: references, pointers, dynamic allocation, lifetime, and const correctness",
                "Design classes with proper constructors, destructors, and encapsulation",
                "Use inheritance, virtual functions, and polymorphism — and know when composition is better",
                "Overload operators and implement the Rule of Three/Five with copy and move semantics",
                "Choose and use STL containers and algorithms fluently, including with lambdas",
                "Apply modern C++: auto, constexpr, enum class, optional, variant, string_view",
                "Manage resources with unique_ptr/shared_ptr/weak_ptr under RAII",
                "Write and use function and class templates",
                "Handle errors with exceptions and exception-safe design; read and write files",
                "Implement core data structures (linked list, BST, hash table) and analyze complexity",
                "Build a substantial console application combining all of these skills",
            ],
            "prerequisites": ["cpp-beginner"],
        }
    ),
)
_w(
    os.path.join(BASE, "course.vi.json"),
    _j(
        {
            "title": "C++ — Trung cấp",
            "description": "Chuyển từ viết C++ sang thiết kế C++: bộ nhớ và vòng đời, thiết kế hướng đối tượng, STL, smart pointer, template, và cấu trúc dữ liệu — thực hành sau mỗi khái niệm.",
            "audience": "Người học đã hoàn thành C++ — Cơ bản và muốn thiết kế chương trình C++ thực thụ: class với ownership rõ ràng, dùng STL thành thạo, template, và tự xây cấu trúc dữ liệu.",
            "outcomes": [
                "Suy luận về bộ nhớ: reference, pointer, cấp phát động, vòng đời, và const correctness",
                "Thiết kế class với constructor, destructor, và đóng gói đúng cách",
                "Dùng kế thừa, hàm ảo, và đa hình — và biết khi nào composition tốt hơn",
                "Nạp chồng toán tử và thực hiện Rule of Three/Five với copy và move semantics",
                "Lựa chọn và dùng container cùng thuật toán STL thành thạo, kể cả với lambda",
                "Áp dụng C++ hiện đại: auto, constexpr, enum class, optional, variant, string_view",
                "Quản lý tài nguyên bằng unique_ptr/shared_ptr/weak_ptr dưới mô hình RAII",
                "Viết và sử dụng function template và class template",
                "Xử lý lỗi bằng exception và thiết kế exception-safe; đọc và ghi file",
                "Cài đặt cấu trúc dữ liệu cốt lõi (linked list, BST, hash table) và phân tích độ phức tạp",
                "Xây dựng ứng dụng console hoàn chỉnh kết hợp toàn bộ kỹ năng trên",
            ],
        }
    ),
)

# track wiring
TPATH = os.path.join(os.path.dirname(os.path.dirname(BASE)), "track.json")
with io.open(TPATH, encoding="utf-8") as f:
    track = json.load(f)
refs = [c["reference"] for c in track["courses"]]
if COURSE_ID not in refs:
    track["courses"].append({"reference": COURSE_ID})
    with open(TPATH, "w", encoding="utf-8") as f:
        json.dump(track, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("track.json:", COURSE_ID, "registered")
else:
    print("track.json already has", COURSE_ID)
print("course skeleton done")
