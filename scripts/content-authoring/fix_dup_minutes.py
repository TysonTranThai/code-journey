#!/usr/bin/env python3
"""Remove duplicate standalone-int arguments from write_lesson(...) calls.

The legit call shape is:
    write_lesson(MOD, "id", "Title", "Desc", 13, MDX_EN, "vi_t", "vi_d", MDX_VI,)

A buggy call carries an extra int between vi_desc and the VI mdx block.
Robust rule: inside one write_lesson( call there must be at most ONE line that
is only an integer + comma. Keep the first, drop any later ones.
"""
import re
import sys

path = sys.argv[1]
lines = open(path).read().split("\n")

out = []
in_call = 0          # nesting depth of write_lesson( calls we track (flat: 0 or 1)
in_tq = False        # inside a triple-quoted block
seen_int_in_call = False

for line in lines:
    s = line.strip()
    if not in_tq:
        if re.match(r"write_lesson\s*\(", s) or (in_call and s.startswith('write_lesson')):
            in_call = 1
            seen_int_in_call = False
        elif in_call and re.match(r'^\d+,\s*$', s):
            if seen_int_in_call:
                continue  # drop duplicate
            seen_int_in_call = True
        elif in_call and '"""' in s:
            # triple-quote opener/closer line
            pass
        elif in_call and (s == ")" or s.startswith(")")):
            in_call = 0
    # toggle triple-quote state on lines containing triple-quote markers
    if '"""' in line:
        n = line.count('"""')
        for _ in range(n):
            in_tq = not in_tq
    out.append(line)

open(path, "w").write("\n".join(out))
print(f"fixed {path}")
