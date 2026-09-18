#!/usr/bin/env python3
"""Wire java-beginner: set course.json module order (curriculum sequence).

Track registration and the validator entry already exist. Only order is
written here; all other course.json fields preserved.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/java/courses/java-beginner/course.json")

ORDER = [
    "java-first-programs",
    "java-types-operators",
    "java-conditions",
    "java-loops",
    "java-methods",
    "java-arrays-strings",
    "java-classes-objects",
    "java-oop-design",
    "java-data-modeling",
    "java-collections-generics",
    "java-exceptions-files",
    "java-streams-optional",
    "java-testing-debug",
    "java-files-capstone",
]

with open(COURSE) as f:
    course = json.load(f)

course["modules"] = [{"reference": m} for m in ORDER]

with open(COURSE, "w") as f:
    json.dump(course, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("course.json modules wired:", len(ORDER))
