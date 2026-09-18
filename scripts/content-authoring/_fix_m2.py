"""One-off fixer: remove orphan ')' lines left after unwrapping L_* strings."""
import ast

p = "scripts/content-authoring/pypb_m2.py"
lines = open(p, encoding="utf-8").readlines()
out = []
removed = 0
for i, l in enumerate(lines):
    if l.strip() == ")" and i + 1 < len(lines) and lines[i + 1].strip() == "":
        # orphan closing paren after an unwrapped triple-quoted assignment
        out.append("\n")
        removed += 1
        continue
    out.append(l)
open(p, "w", encoding="utf-8").writelines(out)
ast.parse(open(p, encoding="utf-8").read())
print("removed", removed, "orphan parens; parse OK")
