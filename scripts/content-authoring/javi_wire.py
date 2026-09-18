#!/usr/bin/env python3
"""Wire java-intermediate: course.json modules (curriculum order).

Only modifies the course's own modules list; track.json already carries
the course reference. Preserves everything else byte-for-byte.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/java/courses/java-intermediate/course.json")

ORDER = [
    "java-equality-immutability",
    "java-oop-solid",
    "java-generics-deep",
    "java-collections-advanced",
    "java-functional-deep",
    "java-exception-architecture",
    "java-io-formats",
    "java-testing-deep",
    "java-concurrency",
    "java-async-http",
    "java-persistence",
    "java-architecture",
    "java-algorithms-inter",
    "java-clean-code",
    "java-inter-capstone",
]

with open(COURSE, encoding="utf-8") as f:
    data = json.load(f)

data["modules"] = [{"reference": m} for m in ORDER]

with open(COURSE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("course.json modules wired:", len(ORDER))
