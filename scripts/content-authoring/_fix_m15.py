#!/usr/bin/env python3
"""Fix py-checkpoint-final-readiness (boilerplate/solution/wrong) + cap-summary tie test."""
import ast
import io

p = "scripts/content-authoring/pypb_m15.py"
src = io.open(p, encoding="utf-8").read()

RAW = 'raw = "coffee,3.5'

# ── 1. Boilerplate: py3.9-safe f-string (no backslash in expression) ────────
start = src.index("        '" + RAW)
end = src.index("',\n", start) + 3
boiler = (
    'raw = "coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2"\n\n'
    "def ingest(raw):\n    pass\n\n"
    "clean = ingest(raw)\n"
    'total = sum(e["amount"] for e in clean)\n'
    'print(f"{total:.2f}")\n'
)
src = src[:start] + "        " + repr(boiler) + src[end:]

# ── 2. Solution: correct filtering + safe ending ────────────────────────────
start = src.index("    solution='" + RAW)
end = src.index("',\n", start) + 3
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
src = src[:start] + "    solution=" + repr(sol) + src[end:]

# ── 3. Wrong: keeps non-positive amounts and zero-fills unparseable ─────────
start = src.index("    wrong='" + RAW)
end = src.index("',\n", start) + 3
wrong = (
    'raw = "coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2"\n\n\n'
    "def ingest(raw):\n"
    "    clean = []\n"
    "    for line in raw.splitlines():\n"
    '        parts = [p.strip() for p in line.split(",")]\n'
    "        if not parts or not parts[0]:\n"
    "            continue\n"
    "        try:\n"
    "            amount = float(parts[1])\n"
    "        except (ValueError, IndexError):\n"
    "            amount = 0.0\n"
    '        clean.append({"amount": round(amount, 2), "category": parts[0].lower()})\n'
    "    return clean\n\n\n"
    "clean = ingest(raw)\n"
    'total = sum(e["amount"] for e in clean)\n'
    'print(f"{total:.2f}")'
)
src = src[:start] + "    wrong=" + repr(wrong) + src[end:]

# ── 4. cap-summary: add an insertion-order≠tie-break discriminator ──────────
i = src.index("no warning")
j = src.index("',\n", i)
insert = (
    "\\nr4 = finance_summary([{\"amount\": 2, \"category\": \"b\"}, "
    "{\"amount\": 3, \"category\": \"a\"}, {\"amount\": 2, \"category\": \"a\"}, "
    "{\"amount\": 3, \"category\": \"b\"}], 20)"
    "\\nassert r4[\"top\"] == \"a\", f\"tie 5-5, a reached its 5 first: {r4}\""
)
src = src[:j] + insert + src[j:]

ast.parse(src)
io.open(p, "w", encoding="utf-8").write(src)
print("m15 checkpoint + summary test fixed; parse OK")
