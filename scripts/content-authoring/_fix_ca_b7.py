#!/usr/bin/env python3
"""Repair batch-7 defects in ca_m13_14.py.
1. flag-taxonomy tests: single-quoted '-Wall' is a multi-char int constant,
   not a string - use double quotes.
2. rebuild-model: add the equal-timestamp discriminator (needs_rebuild must
   return 0 when the newest prereq EQUALS the target) so the >= wrong answer
   is caught.
Idempotent. Zero typed backslashes."""
import ast

P = "ca_m13_14.py"
src = open(P, encoding="utf-8").read()
orig = src
BS = chr(92)

# ---------- 1. flag-taxonomy: single quotes -> double quotes ----------------
DQ2 = BS + chr(34)  # backslash + doublequote: what the file needs inside a Python string literal
pairs = [
    ("CHECK_STR_EQ(flag_intent('-Wall'), ", "CHECK_STR_EQ(flag_intent(" + DQ2 + "-Wall" + DQ2 + "), "),
    ("CHECK_STR_EQ(flag_intent('-Werror'), ", "CHECK_STR_EQ(flag_intent(" + DQ2 + "-Werror" + DQ2 + "), "),
    ("CHECK_STR_EQ(flag_intent('-c'), ", "CHECK_STR_EQ(flag_intent(" + DQ2 + "-c" + DQ2 + "), "),
    ("CHECK_STR_EQ(flag_intent('-O2'), ", "CHECK_STR_EQ(flag_intent(" + DQ2 + "-O2" + DQ2 + "), "),
    ("CHECK_STR_EQ(flag_intent('-fsanitize=address'), ", "CHECK_STR_EQ(flag_intent(" + DQ2 + "-fsanitize=address" + DQ2 + "), "),
    ("CHECK_STR_EQ(flag_intent('-g'), ", "CHECK_STR_EQ(flag_intent(" + DQ2 + "-g" + DQ2 + "), "),
]
n_hits = 0
for old, new in pairs:
    if old in src:
        src = src.replace(old, new)
        n_hits += 1
print("flag_intent quote fixes applied:", n_hits)

# ---------- 2. rebuild-model: equal-timestamp discriminator -----------------
old_t = (
    '("newer prerequisite triggers", "long long deps[2] = {100, 105};@NL@CHECK_EQ(needs_rebuild(102, deps, 2), 1);@NL@CHECK_EQ(needs_rebuild(106, deps, 2), 0);", '
    '"One newer prerequisite (105 > 102) is enough; all older means up to date."),'
)
new_t = (
    '("newer prerequisite triggers", "long long deps[2] = {100, 105};@NL@CHECK_EQ(needs_rebuild(102, deps, 2), 1);@NL@CHECK_EQ(needs_rebuild(106, deps, 2), 0);@NL@CHECK_EQ(needs_rebuild(105, deps, 2), 0);", '
    '"One newer prerequisite (105 > 102) is enough; all older means up to date. Equal timestamps mean up to date (strictly-newer semantics)."),'
)
assert old_t in src, "rebuild-model newer-prereq test not found"
src = src.replace(old_t, new_t)
print("rebuild-model discriminator added")

ast.parse(src)
assert chr(92) + "NL@" not in src and chr(92) + "CE@" not in src
if src != orig:
    open(P, "w", encoding="utf-8").write(src)
    print("WROTE", P)
else:
    print("no changes (already applied)")
