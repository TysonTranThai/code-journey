#!/usr/bin/env python3
"""Java — Advanced: course skeleton (java track, course 3).

Creates courses/java-advanced/{course.json,course.vi.json}, ADDS a course
reference to track.json (read-modify-write; the Beginner and Intermediate
entries are preserved byte-for-byte), and appends the validator entry. Never
rewrites the other courses' files. modules starts as [] (authoring shell —
the loader skips empty courses, verified behavior from earlier builds).
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import BASE, _w, _j  # noqa: E402

TRACK_JSON = os.path.join(BASE, "..", "..", "track.json")
VALIDATOR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "scripts/content-authoring/validate-content.ts",
)

# ── course.json ──────────────────────────────────────────────────────────────
_w(
    os.path.join(BASE, "course.json"),
    _j(
        {
            "id": "java-advanced",
            "title": "Java — Advanced",
            "description": (
                "Understand Java deeply enough to optimize, secure, and operate it: the "
                "object and memory model, bytecode, reflection-driven design, the Java "
                "Memory Model, lock-free concurrency, virtual threads, GC and "
                "performance method, high-performance I/O, real loopback networking, "
                "persistence and distribution concepts, security, observability, and a "
                "production-grade capstone."
            ),
            "modules": [],
            "audience": (
                "Learners who finished Java — Intermediate and want JVM-level "
                "understanding: why Java behaves the way it does under load, "
                "concurrency, and failure — and how to engineer around it."
            ),
            "outcomes": [
                "Explain and exploit Java's object model: initialization order, identity, records, sealed types",
                "Read and reason about bytecode, constant pools, and compiler-generated constructs",
                "Design type-safe generic APIs with variance, capture, and recursive bounds",
                "Build metadata-driven systems with runtime annotations and reflection (a real mini DI container)",
                "Apply the Java Memory Model: happens-before, volatile, safe publication, final-field semantics",
                "Diagnose and fix races with locks, conditions, atomics, and CAS (including ABA)",
                "Scale I/O-bound work with virtual threads and know when they do not help",
                "Reason about allocation, reachability, and GC behavior; use weak references deliberately",
                "Profile-by-reasoning with measurement discipline: warmup, JIT, and noise awareness",
                "Implement advanced structures: tries, union-find, heaps, graph algorithms",
                "Write real TCP clients/servers over loopback with correct framing and timeouts",
                "Process files with NIO.2 channels and buffers, including memory-mapped reads",
                "Design transactional persistence with isolation levels and optimistic concurrency",
                "Apply distributed-systems primitives: idempotency, retries with backoff, circuit breaking",
                "Harden code: password hashing, secure randomness, input validation, SSRF/path-traversal defense",
                "Instrument services with structured logs, metrics, and health checks; run graceful shutdown",
                "Ship a production-grade capstone integrating every layer of the course",
            ],
            "prerequisites": ["java-intermediate"],
        }
    ),
)
_w(
    os.path.join(BASE, "course.vi.json"),
    _j(
        {
            "title": "Java — Nâng cao",
            "description": (
                "Hiểu Java sâu đến mức tối ưu, bảo mật và vận hành được: mô hình đối "
                "tượng và bộ nhớ, bytecode, thiết kế dựa trên reflection, Java Memory "
                "Model, concurrency không khóa, virtual threads, GC và phương pháp "
                "tối ưu, I/O hiệu năng cao, mạng loopback thật, persistence và phân "
                "tán, bảo mật, observability, và capstone cấp production."
            ),
            "audience": (
                "Học viên đã hoàn thành Java — Trung cấp và muốn hiểu ở tầm JVM: vì "
                "sao Java hành xử như vậy dưới tải cao, concurrency, và lỗi — và cách "
                "thiết kế quanh chúng."
            ),
            "outcomes": [
                "Giải thích và tận dụng mô hình đối tượng: thứ tự khởi tạo, identity, record, sealed type",
                "Đọc và suy luận bytecode, constant pool, và cấu trúc do compiler sinh ra",
                "Thiết kế API generic an toàn kiểu với variance, capture, và recursive bound",
                "Xây hệ thống dựa trên metadata với runtime annotation và reflection (mini DI container)",
                "Áp dụng Java Memory Model: happens-before, volatile, safe publication, final-field",
                "Chẩn đoán và sửa race với lock, condition, atomic, và CAS (kể cả ABA)",
                "Mở rộng công việc I/O với virtual threads và biết khi nào chúng không giúp",
                "Suy luận về cấp phát, reachability, GC; dùng weak reference có chủ đích",
                "Đo lường có kỷ luật: warmup, JIT, và nhiễu đo",
                "Cài cấu trúc nâng cao: trie, union-find, heap, thuật toán đồ thị",
                "Viết TCP client/server loopback thật với framing và timeout đúng",
                "Xử lý file với NIO.2 channel/buffer, kể cả memory-mapped read",
                "Thiết kế persistence giao dịch với isolation level và optimistic concurrency",
                "Áp dụng primitive hệ phân tán: idempotency, retry có backoff, circuit breaker",
                "Bảo mật: băm mật khẩu, secure random, validation, chống SSRF/path traversal",
                "Instrument dịch vụ với log có cấu trúc, metric, health check; graceful shutdown",
                "Hoàn thành capstone tích hợp mọi tầng của khóa học",
            ],
        }
    ),
)
print("course: java-advanced")

# ── track.json: additive insert after the Intermediate reference ─────────────
src = io.open(TRACK_JSON, encoding="utf-8").read()
data = json.loads(src)
refs = [c.get("reference") for c in data.get("courses", [])]
if "java-advanced" not in refs:
    assert "java-intermediate" in refs, "intermediate course missing from track.json — refusing to guess"
    data["courses"].append({"reference": "java-advanced"})
    _w(TRACK_JSON, _j(data))
    print("track.json: java-advanced appended")
else:
    print("track.json: already present")

# ── validator entry (preserve other agents' lines) ──────────────────────────
vsrc = io.open(VALIDATOR, encoding="utf-8").read()
anchor = '  { track: "java", course: "java-intermediate" },'
entry = '  { track: "java", course: "java-advanced" },'
if "java-advanced" not in vsrc:
    assert anchor in vsrc, "validator anchor missing"
    vsrc = vsrc.replace(anchor, anchor + "\n" + entry, 1)
    with io.open(VALIDATOR, "w", encoding="utf-8") as f:
        f.write(vsrc)
    print("validator: java-advanced appended")
else:
    print("validator: already present")
