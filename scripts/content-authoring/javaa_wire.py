#!/usr/bin/env python3
"""Wire java-advanced: course.json modules (curriculum order).

Only modifies the course's own modules list; track.json already carries
the course reference. Preserves everything else byte-for-byte.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "src/content/tracks/java/courses/java-advanced/course.json")

ORDER = [
    "java-object-model",
    "java-jvm-bytecode",
    "java-memory-model",
    "java-locks-cas",
    "java-executors-vt",
    "javaa-generics-type-system",
    "javaa-reflection-di",
    "javaa-memory-gc",
    "javaa-perf-measure",
    "javaa-files-nio",
    "javaa-sockets-wire",
    "javaa-async-deadlines",
    "javaa-security-threats",
    "javaa-observability",
    "javaa-capstone",
]

with open(COURSE, encoding="utf-8") as f:
    data = json.load(f)

data["modules"] = [{"reference": m} for m in ORDER]

with open(COURSE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("course.json modules wired:", len(ORDER))
