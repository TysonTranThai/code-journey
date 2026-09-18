"""Fix m6 lesson VI-minutes duplicates + one stray word in VI MDX."""
import ast, re

p = "scripts/content-authoring/pypb_m6.py"
src = open(p, encoding="utf-8").read()

patterns = [
    (r'", 10, L1_VI\)', '", L1_VI)'),
    (r'", 12, L2_VI\)', '", L2_VI)'),
    (r'", 12, L3_VI\)', '", L3_VI)'),
]
count = 0
for pat, rep in patterns:
    src, n = re.subn(pat, rep, src)
    count += n
assert count == 3, f"expected 3, got {count}"

# stray word in the Vietnamese accumulator lesson ("плеч" -> proper phrase)
src = src.replace("Các mẫu tích lũy — плеч lưng của lập trình", "Các mẫu tích lũy — xương sống của lập trình")

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("m6 lesson calls fixed; parse OK")
