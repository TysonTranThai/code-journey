"""Fix three content bugs in pypb_m3.py caught by the two-sided harness."""
import ast

p = "scripts/content-authoring/pypb_m3.py"
src = open(p, encoding="utf-8").read()

# 1. vowel count is 6, not 7
old = '("prints vowel count", \'assert printed == ["7"], f"got {printed}"\','
new = '("prints vowel count", \'assert printed == ["6"], f"got {printed}"\','
assert old in src
src = src.replace(old, new)

# 2. slug keeps the exclamation mark: 'learn-python-fast!'
old = "[(\"prints slug\", 'assert printed == [\"learn-python-fast-\"], f\"got {printed}\"',"
new = "[(\"prints slug\", 'assert printed == [\"learn-python-fast!\"], f\"got {printed}\"',"
assert old in src
src = src.replace(old, new)

# 3. multiline menu must be ONE print call; test asserts a single newline-joined print
old = '("prints menu", \'assert printed == ["1. Start", "2. Settings", "3. Quit"], f"got {printed}"\','
new = ('("prints menu in one call", \'assert printed == ["1. Start", "2. Settings", "3. Quit"], f"got {printed}"\\n'
       'assert code.count("print(") == 1, "use exactly ONE print call with newline escapes",\',')
assert old in src
src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("fixed 3 bugs; parse OK")
