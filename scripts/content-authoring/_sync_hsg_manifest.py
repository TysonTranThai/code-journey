#!/usr/bin/env python3
"""Sync course.json's module list with the modules emitted so far.

Modules appear in the locked 20-module plan order, whether or not they are
emitted yet — the list only includes directories that exist, so it is always
a prefix of the plan and always loadable.
"""
import json
import os

BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "src/content/tracks/hsg/courses/hsg-beginner",
)

PLAN = [
    "hsg-vao-mon", "hsg-loops", "hsg-arrays", "hsg-marking", "hsg-greedy",
    "hsg-sorting", "hsg-search", "hsg-prefix", "hsg-diff", "hsg-strings",
    "hsg-number", "hsg-stl", "hsg-recursion", "hsg-backtrack", "hsg-dp",
    "hsg-graph", "hsg-twopointers", "hsg-technique", "hsg-debug",
    "hsg-contests",
]

P = os.path.join(BASE, "course.json")
c = json.load(open(P, encoding="utf-8"))
MODDIR = os.path.join(BASE, "modules")
# a module counts as emitted when its manifest exists
have = {
    d for d in os.listdir(MODDIR)
    if os.path.isfile(os.path.join(MODDIR, d, "module.json"))
}
for d in os.listdir(MODDIR):
    if d not in PLAN:
        print("WARN: module dir not in plan:", d)
        have.add(d)
ordered = [m for m in PLAN if m in have]
missing_plan = [m for m in PLAN if m not in have]
c["modules"] = [{"reference": m} for m in ordered]
with open(P, "w", encoding="utf-8") as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("modules:", len(ordered), "of", len(PLAN))
if missing_plan:
    print("not yet emitted:", missing_plan)
