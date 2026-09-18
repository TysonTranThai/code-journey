#!/usr/bin/env python3
"""C# — Beginner: course skeleton (csharp track, course 1).

Creates src/content/tracks/csharp/{track.json,track.vi.json} and courses/
csharp-beginner/{course.json,course.vi.json}, and registers the course in
track.json. The track dir does not exist yet — created fresh, so no other
agent's work can be touched. modules starts as [] (authoring shell — the
loader skips empty courses, verified behavior from the other courses).
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import BASE, TRACK, ROOT, _w, _j, write_course  # noqa: E402

TRACK_JSON = os.path.join(TRACK, "track.json")
TRACK_VI = os.path.join(TRACK, "track.vi.json")

track = {
    "id": "csharp",
    "title": "C#",
    "description": (
        "Learn C# from zero to genuinely useful: a practice-first path where every "
        "concept is drilled in real code, every challenge is executed and graded in a "
        "locked-down sandbox against the real .NET SDK, and debugging is taught as a "
        "skill — not an afterthought."
    ),
    "courses": [{"reference": "csharp-beginner"}],
}
_w(TRACK_JSON, _j(track))
_w(
    TRACK_VI,
    _j(
        {
            "title": "C#",
            "description": (
                "Học C# từ con số 0 đến thực sự dùng được: lộ trình thực hành trước — "
                "mọi khái niệm đều được luyện bằng code thật, mọi thử thách được thực thi "
                "và chấm điểm trong sandbox khoá kín bằng .NET SDK thật, và gỡ lỗi được "
                "dạy như một kỹ năng thực thụ."
            ),
            "courses": [{"reference": "csharp-beginner"}],
        }
    ),
)

write_course(
    "csharp-beginner",
    "C# — Beginner",
    (
        "Build real C# from your first program to working applications: variables, "
        "control flow, methods, collections, classes, LINQ, files, exceptions, and an "
        "introduction to async — every step practiced and graded in a sandbox running "
        "the real .NET SDK."
    ),
    "Absolute beginners and developers from other languages who want a rigorous, practice-first start in C# and .NET.",
    [
        "Read and write idiomatic modern C# with confidence",
        "Model data with classes, records, and collections",
        "Debug and test C# programs systematically",
        "Use LINQ and the core .NET libraries productively",
        "Build and persist small real applications",
    ],
    [],
    [
        "csb-welcome",
        "csb-types",
        "csb-io",
        "csb-flow",
        "csb-methods",
        "csb-strings",
        "csb-arrays",
        "csb-collections",
        "csb-classes",
        "csb-oop",
        "csb-models",
        "csb-generics",
        "csb-exceptions",
        "csb-files",
        "csb-linq",
        "csb-delegates",
        "csb-testing",
        "csb-cli",
        "csb-git",
        "csb-algorithms",
        "csb-capstone",
    ],
    "C# — Cơ bản",
    (
        "Xây dựng C# thực thụ từ chương trình đầu tiên đến ứng dụng hoàn chỉnh: biến, "
        "luồng điều khiển, phương thức, collection, class, LINQ, tệp, exception và bước "
        "đầu với async — mỗi bước đều được thực hành và chấm điểm trong sandbox chạy "
        ".NET SDK thật."
    ),
)
print("track + course skeleton written:", os.path.relpath(TRACK_JSON, ROOT), os.path.relpath(BASE, ROOT))
