"""Strip the trailing comma left on the five L_* closing triple-quote lines."""
import ast

p = "scripts/content-authoring/pypb_m2.py"
lines = open(p, encoding="utf-8").readlines()
fixed = 0
for i, l in enumerate(lines):
    if l.rstrip("\n") == '""",':
        lines[i] = '"""\n'
        fixed += 1
open(p, "w", encoding="utf-8").writelines(lines)
ast.parse(open(p, encoding="utf-8").read())
print("fixed", fixed, "closing lines; parse OK")
