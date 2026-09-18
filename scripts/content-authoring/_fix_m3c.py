"""Fix trailing comma typo inside the py-fstr-multiline test code."""
import ast

p = "scripts/content-authoring/pypb_m3.py"
lines = open(p, encoding="utf-8").readlines()
for i, l in enumerate(lines):
    if "prints menu in one call" in l:
        lines[i] = (
            '            [("prints menu in one call", '
            '\'assert printed == ["1. Start", "2. Settings", "3. Quit"], f"got {printed}"\\n'
            'assert code.count("print(") == 1, "use exactly ONE print call",\',\n'
        )
        break
else:
    raise SystemExit("target not found")
open(p, "w", encoding="utf-8").writelines(lines)
ast.parse(open(p, encoding="utf-8").read())
print("menu test fixed; parse OK")
