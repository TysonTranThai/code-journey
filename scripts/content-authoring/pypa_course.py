#!/usr/bin/env python3
"""Course skeleton for the Python — Advanced course."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import _w, _j, TRACK

_w(
    os.path.join(TRACK, "courses/python-advanced", "course.json"),
    _j(
        {
            "id": "python-advanced",
            "title": "Python — Advanced",
            "description": "Engineer serious Python systems: the data model, metaprogramming, advanced typing, concurrency and async at scale, measured performance, architecture, security, distributed fundamentals, and a production-grade capstone platform — designed, not just coded.",
            "modules": [],
            "audience": "Learners who finished Python — Intermediate and want to build, optimize, secure, and operate production-grade Python systems — making their own architecture decisions along the way.",
            "outcomes": [
                "Implement objects that fully obey Python protocols via the data model, descriptors, and MRO",
                "Use metaclasses, __init_subclass__, and decorators for registries and plugin frameworks — and when not to",
                "Design type-safe libraries with generics, variance, ParamSpec, overloads, and Protocols",
                "Choose and benchmark concurrency models: threads, processes, asyncio, and the post-GIL landscape",
                "Build structured async systems with TaskGroup, timeouts, cancellation propagation, and bounded queues",
                "Profile with cProfile and timeit and deliver verified, measured optimizations",
                "Explain bytecode, frames, refcounting/GC, and the import system — and what they mean in practice",
                "Architect with ports and adapters, dependency inversion, repositories, and dependency injection",
                "Engineer production APIs: validation, error contracts, rate limiting, idempotency, pooling",
                "Build resilient job systems: retries with backoff, idempotency keys, circuit breakers, health checks",
                "Tune databases: query plans, indexes, isolation levels, N+1 elimination, optimistic locking",
                "Threat-model and repair injection, unsafe deserialization, SSRF, path traversal, and secrets leakage",
                "Test like an engineer: property-based, contract, and deterministic concurrency tests",
                "Instrument services with structured logs, metrics, correlation IDs, and health/readiness",
            ],
            "prerequisites": ["python-intermediate"],
        }
    ),
)
_w(
    os.path.join(TRACK, "courses/python-advanced", "course.vi.json"),
    _j(
        {
            "title": "Python — Nâng cao",
            "description": "Kỹ thuật hóa Python ở mức hệ thống: data model, metaprogramming, typing nâng cao, concurrency và async ở quy mô lớn, hiệu năng đo lường được, kiến trúc, bảo mật, distributed systems và capstone platform cấp production — bạn là người ra quyết định thiết kế.",
            "audience": "Dành cho học viên đã hoàn thành Python — Intermediate và muốn xây dựng, tối ưu, bảo mật và vận hành hệ thống Python cấp production.",
        }
    ),
)
print("course skeleton written")
