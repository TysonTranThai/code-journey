"""One-off fixer: repair the cursed py-print-combined test tuple in pypb_m1.py."""
import ast

p = "scripts/content-authoring/pypb_m1.py"
lines = open(p, encoding="utf-8").readlines()

start = None
for i, l in enumerate(lines):
    if l.lstrip().startswith('[("one print call'):
        start = i
        break
assert start is not None, "target tuple not found"
end = start + 3  # current block is 3 lines after prior partial fixes

test_code = (
    'assert printed == ["Count: 7"], f"got {printed}"\n'
    'assert code.count(",") >= 1, "pass 7 as a number argument"'
)
hint = 'print("Count:", 7) - print joins arguments with spaces.'

# Build the source line using repr() so quoting is guaranteed correct.
tuple_lines = [
    '            [("one print call with both",\n',
    "              " + repr(test_code) + ",\n",
    "              " + repr(hint) + ")],\n",
]
lines[start:end] = tuple_lines
open(p, "w", encoding="utf-8").writelines(lines)
ast.parse(open(p, encoding="utf-8").read())
print("parse OK; replaced lines", start + 1, "to", end)
