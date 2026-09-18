"""Fix the stray comma that leaked into the py-fstr-multiline test message."""
import ast, json

# 1. fix the generated JSON
jp = "src/content/tracks/python/courses/python-beginner/modules/working-with-strings/practices/m3-fstring-practice/challenges/py-fstr-multiline.json"
d = json.load(open(jp, encoding="utf-8"))
code = d["tests"][0]["code"]
bad = '"use exactly ONE print call",'
assert bad in code
d["tests"][0]["code"] = code.replace(bad, '"use exactly ONE print call"')
open(jp, "w", encoding="utf-8").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

# 2. fix the source line so future re-runs stay correct
p = "scripts/content-authoring/pypb_m3.py"
lines = open(p, encoding="utf-8").readlines()
for i, l in enumerate(lines):
    if "prints menu in one call" in l:
        lines[i] = (
            '            [("prints menu in one call", '
            '\'assert printed == ["1. Start", "2. Settings", "3. Quit"], f"got {printed}"\\n'
            'assert code.count("print(") == 1, "use exactly ONE print call"\',\n'
        )
        break
open(p, "w", encoding="utf-8").writelines(lines)
ast.parse(open(p, encoding="utf-8").read())

# 3. verify the JSON test code now parses as valid Python
compile(d["tests"][0]["code"], "<test>", "exec")
print("JSON + source fixed; test code compiles")
