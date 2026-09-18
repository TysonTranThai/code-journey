#!/usr/bin/env python3
"""Deduplicate py-cap-summary / py-checkpoint-final-readiness in py-solutions.mjs.

The ledger accumulated duplicate R/W entries from fixer scripts; load_solutions
keeps the LAST occurrence, and the last copies for these two ids are corrupt
(wrong tie-break ref; wrong challenge's solution). Keep exactly one R and one W
per id, using the verified-good content.
"""
import io
import re

P = "scripts/content-authoring/py-solutions.mjs"

GOOD_R_SUMMARY = (
    "def finance_summary(expenses, budget):\n"
    "    if not expenses:\n"
    "        return {\"total\": 0.0, \"count\": 0, \"top\": None,\n"
    "                \"remaining\": round(budget, 2), \"warning\": False}\n"
    "    totals = {}\n"
    "    last_seen = {}\n"
    "    for idx, e in enumerate(expenses):\n"
    "        cat = e[\"category\"]\n"
    "        totals[cat] = totals.get(cat, 0) + e[\"amount\"]\n"
    "        last_seen[cat] = idx\n"
    "    total = round(sum(e[\"amount\"] for e in expenses), 2)\n"
    "    top = min(totals, key=lambda c: (-totals[c], last_seen[c]))\n"
    "    return {\n"
    "        \"total\": total,\n"
    "        \"count\": len(expenses),\n"
    "        \"top\": top,\n"
    "        \"remaining\": round(budget - total, 2),\n"
    "        \"warning\": total > 0.9 * budget,\n"
    "    }"
)

GOOD_W_SUMMARY = (
    "def finance_summary(expenses, budget):\n"
    "    if not expenses:\n"
    "        return {\"total\": 0.0, \"count\": 0, \"top\": None,\n"
    "                \"remaining\": round(budget, 2), \"warning\": False}\n"
    "    totals = {}\n"
    "    for e in expenses:\n"
    "        totals[e[\"category\"]] = totals.get(e[\"category\"], 0) + e[\"amount\"]\n"
    "    total = round(sum(e[\"amount\"] for e in expenses), 2)\n"
    "    top = max(totals, key=totals.get)\n"
    "    return {\n"
    "        \"total\": total,\n"
    "        \"count\": len(expenses),\n"
    "        \"top\": top,\n"
    "        \"remaining\": round(budget - total, 2),\n"
    "        \"warning\": total > 0.9 * budget,\n"
    "    }"
)

GOOD_R_CHECKPOINT = (
    "raw = \"coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2\"\n"
    "\n"
    "\n"
    "def ingest(raw):\n"
    "    clean = []\n"
    "    for line in raw.splitlines():\n"
    "        parts = [p.strip() for p in line.split(\",\")]\n"
    "        if len(parts) < 2 or not parts[0] or not parts[1]:\n"
    "            continue\n"
    "        try:\n"
    "            amount = float(parts[1])\n"
    "        except ValueError:\n"
    "            continue\n"
    "        if amount <= 0:\n"
    "            continue\n"
    "        clean.append({\"amount\": round(amount, 2), \"category\": parts[0].lower()})\n"
    "    return clean\n"
    "\n"
    "\n"
    "clean = ingest(raw)\n"
    "total = sum(e[\"amount\"] for e in clean)\n"
    "print(f\"{total:.2f}\")"
)

GOOD_W_CHECKPOINT = (
    "raw = \"coffee,3.5\\nBOOK,12\\ncoffee,1.5\\n,,skip-me\\npen,-2\"\n"
    "\n"
    "\n"
    "def ingest(raw):\n"
    "    clean = []\n"
    "    for line in raw.splitlines():\n"
    "        parts = [p.strip() for p in line.split(\",\")]\n"
    "        if not parts or not parts[0]:\n"
    "            continue\n"
    "        try:\n"
    "            amount = float(parts[1])\n"
    "        except (ValueError, IndexError):\n"
    "            amount = 0.0\n"
    "        clean.append({\"amount\": round(amount, 2), \"category\": parts[0].lower()})\n"
    "    return clean\n"
    "\n"
    "\n"
    "clean = ingest(raw)\n"
    "total = sum(e[\"amount\"] for e in clean)\n"
    "print(f\"{total:.2f}\")"
)

# Sanity: the good solutions must behave correctly before we write them.
ns = {}
exec(GOOD_R_SUMMARY, ns)
assert ns["finance_summary"](
    [{"amount": 2, "category": "b"}, {"amount": 3, "category": "a"},
     {"amount": 2, "category": "a"}, {"amount": 3, "category": "b"}], 20
)["top"] == "a", "R summary must break ties by first-arrival"
ns2 = {}
exec(GOOD_R_CHECKPOINT, ns2)
assert ns2["ingest"]("x,abc") == [] and ns2["ingest"]("tea, 2.5 ") == [{"amount": 2.5, "category": "tea"}]
print("good solutions sanity-checked OK")

src = io.open(P, encoding="utf-8").read()
lines = src.splitlines(keepends=True)

# Remove EVERY existing entry line for the two ids, then append one clean pair.
pat = re.compile(r'^(R|W)\["(py-cap-summary|py-checkpoint-final-readiness)"\] = ')
kept = [ln for ln in lines if not pat.match(ln)]
removed = len(lines) - len(kept)
print(f"removed {removed} stale/duplicate entry lines")


def js_str(s: str) -> str:
    return __import__("json").dumps(s)


out = kept[:]
for key, val in (("R", GOOD_R_SUMMARY), ("W", GOOD_W_SUMMARY),
                 ("R", GOOD_R_CHECKPOINT), ("W", GOOD_W_CHECKPOINT)):
    cid = "py-cap-summary" if "finance_summary" in val else "py-checkpoint-final-readiness"
    out.append(f'{key}["{cid}"] = {js_str(val)};\n')

io.open(P, "w", encoding="utf-8").write("".join(out))
print("ledger rewritten: one clean R/W pair per id")
