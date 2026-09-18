"""Align the two remaining test expectations with boundary boilerplates."""
import ast

p = "scripts/content-authoring/pypb_m4.py"
src = open(p, encoding="utf-8").read()

fixes = [
    # ticket: age=17 + has_id=True -> correct answer is denied (needs BOTH)
    ('[(\'decides entry\', \'assert printed == ["allowed"], f"got {printed}"\',',
     '[("decides entry", \'assert printed == ["denied"], f"got {printed}"\','),
    # shipping: weight=1.0 boundary -> correct answer is 5.00 (up to 1kg inclusive)
    ('[("prints cost", \'assert printed == ["9.00"], f"got {printed}"\',',
     '[("prints cost", \'assert printed == ["5.00"], f"got {printed}"\','),
]
for old, new in fixes:
    assert old in src, "MISS: " + old[:60]
    src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("expectations aligned; parse OK")
