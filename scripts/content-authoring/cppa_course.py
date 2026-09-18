#!/usr/bin/env python3
"""C++ Advanced — course.json + course.vi.json (module references only; details live in modules)."""
import json
import os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    "src/content/tracks/cpp/courses/cpp-advanced")

MODULES = [
    "object-model",
    "move-forwarding",
    "templates-deep",
    "concepts",
    "compile-time",
    "ranges-views",
    "coroutines",
    "memory-model",
    "concurrency",
    "memory-allocators",
    "performance",
    "ub-defensive",
    "debugging",
    "testing",
    "build-systems",
    "abi-linking",
    "networking",
    "security",
    "architecture-production",
    "capstone-hpc-service",
]

# Keep in sync with the module directories on disk.
_on_disk = set(os.listdir(os.path.join(BASE, "modules")))
_missing = [m for m in MODULES if m not in _on_disk]
_extra = sorted(_on_disk - set(MODULES))
assert not _missing, f"course.json references missing modules: {_missing}"
assert not _extra, f"modules on disk not in course.json: {_extra}"

course = {
    "id": "cpp-advanced",
    "title": "C++ Advanced",
    "description": "Reason about what the machine, the compiler, and other threads are actually doing: lifetime mechanics, generic library design, compile-time computation, lazy pipelines, hand-built coroutines — onward to the memory model, concurrency, allocators, performance, and production practice.",
    "audience": "Engineers who finished C++ Intermediate (STL, RAII, move-semantics basics, introductory templates) and now want systems-level reasoning: the memory model, concurrency, performance engineering, and library architecture.",
    "outcomes": [
        "Predict object lifetime, value category, and initialization outcomes exactly, and debug code that violates them",
        "Implement perfect forwarding, resource wrappers, and exception-safe moves; explain RVO and copy elision mechanically",
        "Write generic libraries with specialization, variadic folds, if constexpr, NTTPs, and CTAD",
        "Design concept-constrained APIs and read constraint-failure diagnostics efficiently",
        "Move computation to compile time with constexpr/consteval/constinit and type traits",
        "Build and debug range pipelines, write custom iterator-backed views, and avoid view-dangling bugs",
        "Implement a coroutine generator from promise_type primitives and reason about coroutine lifetimes",
        "Explain the C++ memory model and choose memory orderings with justification",
        "Build thread pools, task runtimes, and concurrent queues with appropriate synchronization",
        "Engineer memory layouts: arenas, pools, std::pmr, and data-oriented design",
        "Optimize with evidence: measure, hypothesize, change, re-measure — with benchmark rigor",
        "Diagnose and repair undefined behavior by class: dangling, overflow, aliasing, races",
        "Debug like an operator: symbols, stack traces, minimization, logging and tracing design",
        "Test like a sceptic: property-based, fuzz-style, deterministic concurrency, performance-regression tests",
        "Build and link professionally: modern CMake targets, presets, visibility, LTO, CI matrices",
        "Design for binary compatibility: ODR, ABI, symbol visibility, plugin boundaries",
        "Write network services with framing, timeouts, and backpressure; audit and harden them",
        "Architect at scale and operate services: boundaries, observability, graceful shutdown",
        "Audit and harden systems code: injection-proof parsers, integer-overflow-safe arithmetic, hardened builds",
        "Ship an integrated service core against an acceptance battery, deterministically verified",
    ],
    "prerequisites": ["cpp-intermediate"],
    "modules": [{"reference": m} for m in MODULES],
}

course_vi = {
    "title": "C++ Nâng cao",
    "description": "Suy luận về những gì máy, compiler và các thread khác thực sự làm: phân loại giá trị và cơ chế vòng đời, thiết kế thư viện generic với concepts, tính toán lúc biên dịch, pipeline lười, coroutine tự tay dựng — rồi tiếp tới mô hình bộ nhớ, concurrency, allocator, kỹ thuật hiệu năng và thực hành production. Mọi khái niệm đều được luyện qua các thử thách có chấm điểm, biên dịch trên toolchain thật.",
}


def _w(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


_w(os.path.join(BASE, "course.json"), course)
_w(os.path.join(BASE, "course.vi.json"), course_vi)
print("course.json written with", len(MODULES), "modules")
