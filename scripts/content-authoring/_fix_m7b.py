"""Fix m7: VI-minutes duplicates + the level ternary hack + EN docstring check."""
import ast, re

p = "scripts/content-authoring/pypb_m7.py"
src = open(p, encoding="utf-8").read()

# VI minutes duplicates in lesson calls
src, n1 = re.subn(r'", 12, L1_VI\)', '", L1_VI)', src)
src, n2 = re.subn(r'", 12, L2_VI\)', '", L2_VI)', src)
src, n3 = re.subn(r'", 12, L3_VI\)', '", L3_VI)', src)
assert n1 == 1 and n2 == 1 and n3 == 1, (n1, n2, n3)

# clean the level ternary
src = src.replace('level="refactor" if False else "mini-build",', 'level="mini-build",')

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("m7 fixed; parse OK")
