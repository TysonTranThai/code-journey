#!/usr/bin/env python3
"""Append the r4 tie-break test to py-cap-summary (JSON + authoring source)."""
import ast
import io
import json

JP = "src/content/tracks/python/courses/python-beginner/modules/capstone-personal-finance-cli/practices/capstone-core-practice/challenges/py-cap-summary.json"
SP = "scripts/content-authoring/pypb_m15.py"

SUFFIX_JSON = (
    '\nr4 = finance_summary([{"amount": 2, "category": "b"}, '
    '{"amount": 3, "category": "a"}, {"amount": 2, "category": "a"}, '
    '{"amount": 3, "category": "b"}], 20)'
    '\nassert r4["top"] == "a", f"tie 5-5, a reached its 5 first: {r4}"'
)
# For the authoring source (a single-quoted Python literal, so \n as two chars):
SUFFIX_SRC = SUFFIX_JSON.replace("\n", "\\n")

# ── 1. JSON ──────────────────────────────────────────────────────────────────
ch = json.load(open(JP, encoding="utf-8"))
code = ch["tests"][0]["code"]
if "r4 = finance_summary" not in code:
    ch["tests"][0]["code"] = code + SUFFIX_JSON
    with open(JP, "w", encoding="utf-8") as f:
        json.dump(ch, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("json updated")
else:
    print("json already has r4")

# ── 2. Authoring source ─────────────────────────────────────────────────────
src = io.open(SP, encoding="utf-8").read()
if "r4 = finance_summary" not in src:
    anchor = '50 is exactly half'
    k = src.index(anchor)
    seg_end = src.index("',\n", k)
    src = src[:seg_end] + SUFFIX_SRC + src[seg_end:]
    ast.parse(src)
    io.open(SP, "w", encoding="utf-8").write(src)
    print("authoring source updated")
else:
    print("authoring source already has r4")
