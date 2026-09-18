#!/usr/bin/env python3
"""Wire cpp-intermediate: course.json modules (curriculum order) +
validate-content.ts course entry. Track registration already exists.
Preserves all other file content untouched."""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/cpp/courses/cpp-intermediate/course.json")
VALIDATOR = os.path.join(ROOT, "scripts/content-authoring/validate-content.ts")

ORDER = [
    "memory-and-lifetime",
    "object-oriented-design",
    "inheritance-polymorphism",
    "operators-copy-move",
    "stl-fundamentals",
    "iterators-algorithms",
    "modern-cpp",
    "smart-pointers-raii",
    "templates",
    "errors-and-files",
    "dsa",
    "final-project",
]

# 1) course.json — fill the empty modules array, keep everything else as-is
course = json.load(io.open(COURSE, encoding="utf-8"))
assert course["modules"] == [], "modules already wired; refusing to double-write"
course["modules"] = [{"reference": m} for m in ORDER]
io.open(COURSE, "w", encoding="utf-8").write(json.dumps(course, indent=2, ensure_ascii=False) + "\n")
print(f"course.json: {len(ORDER)} modules wired")

# 2) validator — add the course line after the cpp-beginner entry
src = io.open(VALIDATOR, encoding="utf-8").read()
entry = '{ track: "cpp", course: "cpp-intermediate" },'
if "cpp-intermediate" in src:
    print("validator: entry already present")
elif '{ track: "cpp", course: "cpp-beginner" },' in src:
    anchor = '{ track: "cpp", course: "cpp-beginner" },'
    src = src.replace(anchor, anchor + "\n  " + entry, 1)
    io.open(VALIDATOR, "w", encoding="utf-8").write(src)
    print("validator: cpp-intermediate entry added")
else:
    raise SystemExit("validator anchor not found — inspect manually")
