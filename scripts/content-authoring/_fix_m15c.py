#!/usr/bin/env python3
"""Anchor-to-anchor replacement of the final-readiness solution literal."""
import ast
import io
import json
import re

LEDGER = "scripts/content-authoring/py-solutions.mjs"
AP = "scripts/content-authoring/pypb_m15.py"

sol = (
    'raw = "coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2"\n\n\n'
    "def ingest(raw):\n"
    "    clean = []\n"
    "    for line in raw.splitlines():\n"
    '        parts = [p.strip() for p in line.split(",")]\n'
    "        if len(parts) < 2 or not parts[0] or not parts[1]:\n"
    "            continue\n"
    "        try:\n"
    "            amount = float(parts[1])\n"
    "        except ValueError:\n"
    "            continue\n"
    "        if amount <= 0:\n"
    "            continue\n"
    '        clean.append({"amount": round(amount, 2), "category": parts[0].lower()})\n'
    "    return clean\n\n\n"
    "clean = ingest(raw)\n"
    'total = sum(e["amount"] for e in clean)\n'
    'print(f"{total:.2f}")'
)

# 1. ledger
lsrc = io.open(LEDGER, encoding="utf-8").read()
entry = 'R["py-checkpoint-final-readiness"] = ' + json.dumps(sol) + ";"
pattern = re.compile(r'R\["py-checkpoint-final-readiness"\] = "(?:[^"\\]|\\.)*";')
lsrc, n = pattern.subn(lambda m: entry, lsrc, count=1)
assert n == 1, "ledger entry not found"
io.open(LEDGER, "w", encoding="utf-8").write(lsrc)

# 2. authoring script: replace from `    solution=` up to (not incl.) `    wrong=`
ascript = io.open(AP, encoding="utf-8").read()
astart = ascript.index("    solution=")
aend = ascript.index("    wrong=", astart)
ascript = ascript[:astart] + "    solution=" + repr(sol) + ",\n\n" + ascript[aend:]
ast.parse(ascript)
io.open(AP, "w", encoding="utf-8").write(ascript)
print("ledger + authoring solution span replaced; parse OK")
