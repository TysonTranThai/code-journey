"""Fix two m5 test assertions (list repr vs membership checks)."""
import ast

p = "scripts/content-authoring/pypb_m5.py"
src = open(p, encoding="utf-8").read()

fixes = [
    # append: printed[0] is a repr string; check with plain substring tests
    (
        '("prints mutated list", \'assert printed == "[\\\'green\\\', \\\'red\\\', \\\'blue\\\']" in str(printed), f"got {printed}"\\nassert printed and "green" in printed[0] and "red" in printed[0] and "blue" in printed[0], f"expected all three colors, got {printed}"\',',
        '("prints mutated list", \'assert len(printed) == 1 and "green" in printed[0] and "red" in printed[0] and "blue" in printed[0], f"expected [green, red, blue], got {printed}"\\nassert printed[0].find("green") < printed[0].find("red") < printed[0].find("blue"), f"order must be green, red, blue, got {printed[0]}"\',',
    ),
    # sorted-vs-sort: printed[1] is a repr "[7, 10, 8]" — "10" IS a substring of it!
    # assert on the first char ordering instead: starts with "[7"
    (
        'assert "7" in printed[1] and "10" not in printed[1], f"second line must be the original order, got {printed[1]}"',
        'assert printed[1].strip().startswith("[7, 10"), f"second line must be the original order, got {printed[1]}"',
    ),
]
for old, new in fixes:
    assert old in src, "MISS: " + old[:70]
    src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("m5 tests fixed; parse OK")
