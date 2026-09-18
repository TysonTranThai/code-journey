#!/usr/bin/env python3
"""Rewrite the final-readiness solution entry in the solutions ledger (py3.9-safe ending)."""
import ast
import io
import json
import re

LEDGER = "scripts/content-authoring/py-solutions.mjs"
src = io.open(LEDGER, encoding="utf-8").read()

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

entry = 'R["py-checkpoint-final-readiness"] = ' + json.dumps(sol) + ";"
pattern = re.compile(r'R\["py-checkpoint-final-readiness"\] = "(?:[^"\\]|\\.)*";')
src, n = pattern.subn(lambda m: entry, src, count=1)
assert n == 1, "ledger entry not found"

# same fix for the authoring script so a future re-run regenerates the right thing
ap = "scripts/content-authoring/pypb_m15.py"
ascript = io.open(ap, encoding="utf-8").read()
astart = ascript.index("    solution='raw = \"coffee,3.5")
aend = ascript.index("print(f\"{total:.2f}\")',", astart) + len("print(f\"{total:.2f}\")',")
ascript = ascript[:astart] + "    solution=" + repr(sol) + ascript[aend:]
ast.parse(ascript)
io.open(ap, "w", encoding="utf-8").write(ascript)

io.open(LEDGER, "w", encoding="utf-8").write(src)
print("ledger + authoring script updated; parse OK")
