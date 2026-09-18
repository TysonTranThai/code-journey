#!/usr/bin/env python3
"""Java — Intermediate: course skeleton (java track, course 2).

Creates courses/java-intermediate/{course.json,course.vi.json}, ADDS a course
reference to track.json (read-modify-write; the Beginner entry is preserved
byte-for-byte), and appends the validator entry. Never rewrites Beginner's
course files. modules starts as [] (authoring shell — the loader skips empty
courses, verified behavior from the Beginner build).
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import BASE, _w, _j  # noqa: E402

TRACK_JSON = os.path.join(BASE, "..", "..", "track.json")
TRACK_VI_JSON = os.path.join(BASE, "..", "..", "track.vi.json")
VALIDATOR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "scripts/content-authoring/validate-content.ts",
)

# ── course.json ──────────────────────────────────────────────────────────────
_w(
    os.path.join(BASE, "course.json"),
    _j(
        {
            "id": "java-intermediate",
            "title": "Java — Intermediate",
            "description": (
                "Move from writing Java to engineering it: equality and immutability "
                "contracts, SOLID design, generics with wildcards, advanced collections, "
                "Collectors, exception architecture, testing depth, concurrency, async "
                "composition, repositories, layered architecture, and algorithms — "
                "capped by a layered expense-tracker capstone."
            ),
            "modules": [],
            "audience": (
                "Learners who finished Java — Beginner (or know its scope) and want to "
                "design, test, and structure maintainable Java applications — not just "
                "write more syntax."
            ),
            "outcomes": [
                "Design types with correct equals/hashCode contracts, immutability, and defensive copying",
                "Apply dependency inversion, composition, and sealed hierarchies to real design tradeoffs",
                "Write generic APIs with bounded types, wildcards, and PECS confidently",
                "Choose and combine collections with Comparable/Comparator and immutable views",
                "Transform data with Collectors: groupingBy, partitioningBy, toMap, teeing",
                "Architect errors with try-with-resources, exception boundaries, and custom hierarchies",
                "Read and write NIO.2 file code and hand-parse CSV/JSON safely",
                "Test like a professional: AAA, parameterized thinking, test doubles, regression nets",
                "Reason about Maven lifecycles, dependency scopes, and multi-module structure",
                "Write concurrent code with executors, Futures, and atomic visibility primitives",
                "Compose async pipelines with CompletableFuture and injectable HTTP transports",
                "Structure applications in layers with repositories and hand-rolled DI",
                "Solve algorithm problems with maps, two pointers, sliding windows, and prefix sums",
                "Ship a layered capstone integrating records, generics, streams, repositories, and tests",
            ],
            "prerequisites": ["java-beginner"],
        }
    ),
)
_w(
    os.path.join(BASE, "course.vi.json"),
    _j(
        {
            "title": "Java — Trung cấp",
            "description": (
                "Chuyển từ viết Java sang kỹ thuật hóa Java: hợp đồng equals/hashCode "
                "và tính bất biến, thiết kế SOLID, generic với wildcard, collection "
                "nâng cao, Collectors, kiến trúc exception, kiểm thử chuyên sâu, "
                "concurrency, composition bất đồng bộ, repository, kiến trúc phân "
                "lớp, và thuật toán — kết bằng capstone quản lý chi tiêu phân lớp."
            ),
            "audience": (
                "Học viên đã hoàn thành Java — Cơ bản (hoặc nắm được phạm vi tương "
                "đương) và muốn thiết kế, kiểm thử, cấu trúc ứng dụng Java bảo trì "
                "được — không chỉ học thêm cú pháp."
            ),
            "outcomes": [
                "Thiết kế kiểu với hợp đồng equals/hashCode đúng, tính bất biến, và bản sao phòng thủ",
                "Áp dụng dependency inversion, composition, và sealed hierarchy vào các tradeoff thiết kế thật",
                "Viết API generic với bounded type, wildcard, và PECS tự tin",
                "Chọn và kết hợp collection với Comparable/Comparator và view bất biến",
                "Biến đổi dữ liệu với Collectors: groupingBy, partitioningBy, toMap, teeing",
                "Kiến trúc hóa lỗi với try-with-resources, ranh giới exception, và hệ thống exception riêng",
                "Đọc viết file với NIO.2 và tự phân tích CSV/JSON an toàn",
                "Kiểm thử như dev chuyên nghiệp: AAA, tư duy parameterized, test double, lưới hồi quy",
                "Suy luận về vòng đời Maven, dependency scope, và cấu trúc multi-module",
                "Viết code đồng thời với executor, Future, và primitive atomic về visibility",
                "Dựng pipeline bất đồng bộ với CompletableFuture và transport HTTP khả tiêm",
                "Cấu trúc ứng dụng thành các lớp với repository và DI tự viết",
                "Giải bài toán thuật toán với map, two pointers, sliding window, và prefix sum",
                "Hoàn thành capstone phân lớp tích hợp record, generic, stream, repository, và kiểm thử",
            ],
        }
    ),
)
print("course: java-intermediate")

# ── track.json: additive insert after the Beginner reference ────────────────
src = io.open(TRACK_JSON, encoding="utf-8").read()
data = json.loads(src)
refs = [c.get("reference") for c in data.get("courses", [])]
if "java-intermediate" not in refs:
    assert "java-beginner" in refs, "beginner course missing from track.json — refusing to guess"
    data["courses"].append({"reference": "java-intermediate"})
    _w(TRACK_JSON, _j(data))
    print("track.json: java-intermediate appended")
else:
    print("track.json: already present")

# ── validator entry (preserve other agents' lines) ──────────────────────────
vsrc = io.open(VALIDATOR, encoding="utf-8").read()
anchor = '  { track: "java", course: "java-beginner" },'
entry = '  { track: "java", course: "java-intermediate" },'
if "java-intermediate" not in vsrc:
    assert anchor in vsrc, "validator anchor missing"
    vsrc = vsrc.replace(anchor, anchor + "\n" + entry, 1)
    with io.open(VALIDATOR, "w", encoding="utf-8") as f:
        f.write(vsrc)
    print("validator: java-intermediate appended")
else:
    print("validator: already present")
