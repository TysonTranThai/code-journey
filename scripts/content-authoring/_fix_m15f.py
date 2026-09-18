#!/usr/bin/env python3
"""cap-summary ref: tie-break by LAST index (first-to-reach-total)."""
import ast
import io
import json
import re

LEDGER = "scripts/content-authoring/py-solutions.mjs"
AP = "scripts/content-authoring/pypb_m15.py"

REF = (
    "def finance_summary(expenses, budget):\n"
    "    if not expenses:\n"
    '        return {"total": 0.0, "count": 0, "top": None,\n'
    '                "remaining": round(budget, 2), "warning": False}\n'
    "    totals = {}\n"
    "    last_seen = {}\n"
    "    for idx, e in enumerate(expenses):\n"
    '        cat = e["category"]\n'
    '        totals[cat] = totals.get(cat, 0) + e["amount"]\n'
    "        last_seen[cat] = idx\n"
    '    total = round(sum(e["amount"] for e in expenses), 2)\n'
    '    top = min(totals, key=lambda c: (-totals[c], last_seen[c]))\n'
    "    return {\n"
    '        "total": total,\n'
    '        "count": len(expenses),\n'
    '        "top": top,\n'
    '        "remaining": round(budget - total, 2),\n'
    '        "warning": total > 0.9 * budget,\n'
    "    }"
)

# 1. ledger: replace R entry (first occurrence only; id appears once)
lsrc = io.open(LEDGER, encoding="utf-8").read()
# the old entry is multi-line? No — written as one json.dumps line. Replace it.
pat = re.compile(r'R\["py-cap-summary"\] = "(?:[^"\\]|\\.)*";')
lsrc, n = pat.subn('R["py-cap-summary"] = ' + json.dumps(REF) + ";", lsrc, count=1)
assert n == 1, "ledger R entry not found"
io.open(LEDGER, "w", encoding="utf-8").write(lsrc)

# 2. authoring script: replace the solution literal between anchors
ascript = io.open(AP, encoding="utf-8").read()
# the FINAL checkpoint's solution= is the last one; cap-summary's is the earlier one.
k = ascript.index('("py-cap-summary"')
s_start = ascript.index("    solution=", k)
s_end = ascript.index("    wrong=", s_start)  # the wrong literal of the SAME tuple
new_block = "    solution=" + repr(
    "def finance_summary(expenses, budget):\n"
    '    if not expenses:\n'
    '        return {"total": 0.0, "count": 0, "top": None,\n'
    '                "remaining": round(budget, 2), "warning": False}\n'
    "    totals = {}\n"
    "    last_seen = {}\n"
    "    for idx, e in enumerate(expenses):\n"
    '        cat = e["category"]\n'
    '        totals[cat] = totals.get(cat, 0) + e["amount"]\n'
    "        last_seen[cat] = idx\n"
    '    total = round(sum(e["amount"] for e in expenses), 2)\n'
    '    top = min(totals, key=lambda c: (-totals[c], last_seen[c]))\n'
    "    return {\n"
    '        "total": total,\n'
    '        "count": len(expenses),\n'
    '        "top": top,\n'
    '        "remaining": round(budget - total, 2),\n'
    '        "warning": total > 0.9 * budget,\n'
    "    }"
) + ",\n\n"
ascript = ascript[:s_start] + new_block + ascript[s_end:]
ast.parse(ascript)
io.open(AP, "w", encoding="utf-8").write(ascript)
print("cap-summary ref fixed (last_seen tie-break) in ledger + authoring source")
