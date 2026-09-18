#!/usr/bin/env python3
"""Add the tie-break discriminator test to py-cap-summary (JSON + authoring source)."""
import ast
import io
import json

JP = "src/content/tracks/python/courses/python-beginner/modules/capstone-personal-finance-cli/practices/capstone-core-practice/challenges/py-cap-summary.json"
SP = "scripts/content-authoring/pypb_m15.py"

ANCHOR = 'unused'
EXTRA = (
    '\\nr4 = finance_summary([{"amount": 2, "category": "b"}, '
    '{"amount": 3, "category": "a"}, {"amount": 2, "category": "a"}, '
    '{"amount": 3, "category": "b"}], 20)'
    '\\nassert r4["top"] == "a", f"tie 5-5, a reached its 5 first: {r4}"'
)

# ── 1. Challenge JSON (the graded artifact) ─────────────────────────────────
ch = json.load(open(JP, encoding="utf-8"))
code = ch["tests"][0]["code"]
if "r4 = finance_summary" not in code:
    idx = code.rindex('50 is exactly half')
    line_end = code.index("\n", idx)
    ch["tests"][0]["code"] = code[:line_end] + EXTRA.replace("\\n", "\n") + code[line_end:]
    json.dump(ch, open(JP, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(JP + ".vi", "w", encoding="utf-8").close() if False else None
    print("json updated")
else:
    print("json already has r4")

# ── 2. Authoring source (so re-runs keep it) ────────────────────────────────
src = io.open(SP, encoding="utf-8").read()
if "r4 = finance_summary" not in src:
    # find the cap-summary test literal: after 'no warning' occurrence in m15 source
    k = src.index("no warning")
    # the literal is a single-quoted python string containing \n escapes; find the
    # closing quote of that test tuple line
    line_start = src.rindex("\n", 0, k) + 1
    line_end = src.index("'),\n", k) + 1
    line = src[line_start:line_end]
    parts = line.rsplit('", "', 1) if '", "' in line else None
    # simpler: insert before the closing quote of the test-code segment
    seg_end = src.index("',\n", k)  # end of the test-code string literal
    insertion = (
        '\\nr4 = finance_summary([{"amount": 2, "category": "b"}, '
        '{"amount": 3, "category": "a"}, {"amount": 2, "category": "a"}, '
        '{"amount": 3, "category": "b"}], 20)'
        '\\nassert r4["top"] == "a", f"tie 5-5, a reached its 5 first: {r4}"'
    )
    src = src[:seg_end] + insertion + src[seg_end:]
    ast.parse(src)
    io.open(SP, "w", encoding="utf-8").write(src)
    print("authoring source updated")
else:
    print("authoring source already has r4")
