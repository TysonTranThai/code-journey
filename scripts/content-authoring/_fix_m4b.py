"""Strengthen 4 Module 4 challenges whose wrong solutions were behaviorally identical.

Strategy per challenge:
- py-logic-range: boilerplate age = 18 (the boundary) — chaining bug shows.
- py-logic-ticket: boilerplate age = 17, has_id = True — `or` wrongly admits.
- py-val-password: boilerplate "sunshine" (8 chars, no digit) — length check
  passes so the elif branch is exercised; wrong solution with <= rejects 8.
- py-val-shipping: boilerplate weight = 1.0 (boundary) — `< 1` vs `<= 1` differ.
"""
import ast, json

p = "scripts/content-authoring/pypb_m4.py"
src = open(p, encoding="utf-8").read()

# 1. range: age = 18 + assertion that wrong chaining fails at boundary
src = src.replace(
    '            "age = 30\\n",\n            [("uses chained comparison"',
    '            "age = 18\\n",\n            [("uses chained comparison"',
)
# 2. ticket: age = 17
src = src.replace(
    '            "age = 19\\nhas_id = True\\n",\n            [("decides entry"',
    '            "age = 17\\nhas_id = True\\n",\n            [("decides entry"',
)
# 3. password: password = "sunshine" (8 chars, no digit)
src = src.replace(
    '            \'password = "sun9"\\n\',\n            [("validates password"',
    '            \'password = "sunshine"\\n\',\n            [("validates password"',
)
# 4. shipping: weight = 1.0
src = src.replace(
    '            "weight = 2.5\\n",\n            [("prints cost"',
    '            "weight = 1.0\\n",\n            [("prints cost"',
)

# Update wrong solutions + expected outputs to match new boilerplates.
wrong_fixes = [
    # range: wrong = strict both sides; at age=18 it wrongly says not working age
    ('("py-logic-range", \'age = 30\\nif 18 <= age < 65:\\n    print("working age")\\nelse:\\n    print("not working age")\',',
     '("py-logic-range", \'age = 18\\nif 18 < age < 65:\\n    print("working age")\\nelse:\\n    print("not working age")\','),
    ('         \'age = 30\\nif 18 < age < 65:\\n    print("working age")\\nelse:\\n    print("not working age")\'),',
     '         \'age = 18\\nif 18 < age < 65:\\n    print("working age")\\nelse:\\n    print("not working age")\'),'),
    # ticket: wrong uses or; at age=17 wrongly allows
    ('("py-logic-ticket", "age = 19\\nhas_id = True\\nif age >= 18 or has_id:\\n    print(\\"allowed\\")\\nelse:\\n    print(\\"denied\\")",',
     '("py-logic-ticket", "age = 17\\nhas_id = True\\nif age >= 18 or has_id:\\n    print(\\"allowed\\")\\nelse:\\n    print(\\"denied\\")",'),
    ('         "age = 19\\nhas_id = True\\nif age >= 18 or has_id:\\n    print(\\"allowed\\")\\nelse:\\n    print(\\"denied\\")"),',
     '         "age = 17\\nhas_id = True\\nif age >= 18 or has_id:\\n    print(\\"allowed\\")\\nelse:\\n    print(\\"denied\\")"),'),
    # password: wrong uses <= 8; at 8 chars it wrongly says weak (expected branch: no digit not reached, printed == "weak"? no)
    # password "sunshine": correct = len>=8 -> check digits -> none -> "no digit"; wrong (<=) says "weak"
    ('\'assert printed == ["weak"], f"got {printed}"\',\n              "First check length with len(); elif not any character.isdigit().")',
     '\'assert printed == ["no digit"], f"got {printed}"\',\n              "Length check passes at 8 chars; then the digit check must fire (elif).")'),
    ('("py-val-password", \'password = "sun9"\\nif len(password) < 8:\\n    print("weak")\\nelif not any(c.isdigit() for c in password):\\n    print("no digit")\\nelse:\\n    print("ok")\',',
     '("py-val-password", \'password = "sunshine"\\nif len(password) < 8:\\n    print("weak")\\nelif not any(c.isdigit() for c in password):\\n    print("no digit")\\nelse:\\n    print("ok")\','),
    ('         \'password = "sun9"\\nif len(password) <= 8:\\n    print("weak")\\nelif not any(c.isdigit() for c in password):\\n    print("no digit")\\nelse:\\n    print("ok")\'),',
     '         \'password = "sunshine"\\nif len(password) <= 8:\\n    print("weak")\\nelif not any(c.isdigit() for c in password):\\n    print("no digit")\\nelse:\\n    print("ok")\'),'),
    # shipping: weight = 1.0 => 5.00 both correct and wrong (<1 fails at exactly 1) — wrong now differs
    ('("py-val-shipping", "weight = 2.5\\nif weight <= 1:',
     '("py-val-shipping", "weight = 1.0\\nif weight <= 1:'),
    ('         "weight = 2.5\\nif weight < 1:',
     '         "weight = 1.0\\nif weight < 1:'),
]
for old, new in wrong_fixes:
    assert old in src, "MISS: " + old[:70]
    src = src.replace(old, new)

# challenge prompt text updates for clarity at new boilerplates
src = src.replace(
    '"age is given. Print working age if 18 <= age < 65 — with one chained comparison."',
    '"age = 18 is given (the boundary!). Print working age if 18 <= age < 65 — with one chained comparison."',
)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("m4 strengthened; parse OK")
