#!/usr/bin/env python3
"""Rewrite py-checkpoint-problem-solving's solution with the correct tie-break."""
import io

p = "scripts/content-authoring/pypb_m13.py"
src = io.open(p, encoding="utf-8").read()

start = src.find("    solution='sales = [(\"mon\", \"pen\", 4)")
assert start != -1, "solution line not found"
end = src.find("print(report(sales))'", start)
assert end != -1, "solution end not found"
end += len("print(report(sales))',")

NEW = (
    "    solution='sales = [(\"mon\", \"pen\", 4), (\"mon\", \"book\", 2), "
    "(\"tue\", \"pen\", 3), (\"wed\", \"bag\", 5), (\"wed\", \"book\", 7)]\\n\\n\\n"
    "def report(sales):\\n"
    "    per_item = {}\\n"
    "    item_last = {}\\n"
    "    per_day = {}\\n"
    "    total = 0\\n"
    "    for idx, (day, item, qty) in enumerate(sales):\\n"
    "        per_item[item] = per_item.get(item, 0) + qty\\n"
    "        item_last[item] = idx\\n"
    "        per_day[day] = per_day.get(day, 0) + qty\\n"
    "        total += qty\\n"
    "    best_item = min(per_item, key=lambda it: (-per_item[it], item_last[it]))\\n"
    "    best_day = sorted(per_day, key=lambda d: (-per_day[d], d))[0]\\n"
    "    return {\"total\": total, \"best_item\": best_item, \"busiest_day\": best_day}\\n\\n\\n"
    "print(report(sales))',"
)

src = src[:start] + NEW + src[end:]
io.open(p, "w", encoding="utf-8").write(src)

import ast
ast.parse(src)
print("checkpoint solution rewritten; parse OK")
