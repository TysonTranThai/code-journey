#!/usr/bin/env python3
"""Fix ca_m17_18.py for single-pass execution.

1. Remove the exec-machinery block (placeholder expansion via exec) entirely.
2. Expand remaining @T1@..@LV1@ placeholders into ESCAPED string-literal text
   (placeholder sits inside a Python "..." string; inserting backslash-quote
   content keeps the source valid).
3. AST-validate the result and assert no target placeholders remain.

Idempotent: safe to run repeatedly. Zero typed backslashes (built via chr()).
"""
import ast
import re

P = "ca_m17_18.py"
src = open(P, encoding="utf-8").read()
Q = chr(34)
BS = chr(92)
NL = chr(10)

orig = src

# ---- 1. strip exec machinery (from its marker comment to EOF) --------------
MACHINE_START = "# ---------------- placeholder expansion ----------------"
if MACHINE_START in src:
    src = src[: src.index(MACHINE_START)].rstrip() + NL
    print("exec machinery stripped")

# ---- 2. expand placeholders into escaped literals --------------------------
CONTENT = {
    "@T10@": "A",
    "@T1@": "echo pipe-ok",
    "@T2@": "pipe-ok",
    "@T3@": "exit 3",
    "@T4@": "exit 0",
    "@T5@": "CJ_DEFINITELY_UNSET_XYZ",
    "@T6@": "fallback",
    "@T7@": "PATH",
    "@T8@": "none",
    "@T9@": "x",
    "@J1@": "true",
    "@J2@": "true",
    "@J3@": "exit 5",
    "@LV0@": "deadlock-risk",
    "@LV1@": "safe",
}
for k in sorted(CONTENT, key=len, reverse=True):
    v = BS + Q + CONTENT[k] + Q  # e.g. \"echo pipe-ok\"
    if k in src:
        n = src.count(k)
        src = src.replace(k, v)
        print("expanded", k, "x", n)

# ---- 3. validate ------------------------------------------------------------
leftover = re.findall(r"@(?:T\d+|J\d+|LV\d)@", src)
assert not leftover, "leftover placeholders: " + repr(leftover)
ast.parse(src)
assert "@FDNULL@" in src and "@FDSH@" in src, "runtime fill_given tokens missing"

if src != orig:
    open(P, "w", encoding="utf-8").write(src)
    print("written")
else:
    print("no changes")
print("OK: ast valid, placeholders expanded")
