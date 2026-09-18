"""Fix m5 lesson VI-minutes duplicates using regex on the ", 12, L*_VI)" tail."""
import ast, re

p = "scripts/content-authoring/pypb_m5.py"
src = open(p, encoding="utf-8").read()

# pattern: `, 12, L1_VI)` etc. — drop the stray minutes before the VI mdx var
patterns = [
    (r'", 12, L1_VI\)', '", L1_VI)'),
    (r'", 10, L2_VI\)', '", L2_VI)'),
    (r'", 12, L3_VI\)', '", L3_VI)'),
    (r'", 10, L4_VI\)', '", L4_VI)'),
]
count = 0
for pat, rep in patterns:
    src, n = re.subn(pat, rep, src)
    count += n

assert count == 4, f"expected 4 replacements, got {count}"
open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("m5 lesson calls fixed; parse OK")
