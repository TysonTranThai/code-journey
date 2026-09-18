"""Remaining m4 strengthenings with exact matches (range, password, shipping)."""
import ast

p = "scripts/content-authoring/pypb_m4.py"
src = open(p, encoding="utf-8").read()

fixes = [
    # ── range: boilerplate age=30 -> age=18 (boundary), ref age 30->18, wrong uses strict
    ('            "age = 30\\n",\n',
     '            "age = 18\\n",\n'),
    ('("py-logic-range", \'age = 30\\nif 18 <= age < 65:',
     '("py-logic-range", \'age = 18\\nif 18 <= age < 65:'),
    # wrong solution currently: age=30 + chained-strict; becomes age=18 + chained-strict
    ('         \'age = 30\\nif 18 < age < 65:\\n    print("working age")\\nelse:\\n    print("not working age")\'),',
     '         \'age = 18\\nif 18 < age < 65:\\n    print("working age")\\nelse:\\n    print("not working age")\'),'),
    # ── password: boilerplate + ref + wrong use "sunshine"
    ("            'password = \"sun9\"\\n',\n",
     "            'password = \"sunshine\"\\n',\n"),
    ('\'password = "sun9" is given. Print weak if it has fewer than 8 characters; print ok otherwise. Then extend: also print no digit if it has no digits at all (after the length check).\'',
     '\'password = "sunshine" is given (8 chars, no digit). The length check passes; print no digit if the password has no digits at all, else print ok.\''),
    ('("py-val-password", \'password = "sun9"\\nif len(password) < 8:',
     '("py-val-password", \'password = "sunshine"\\nif len(password) < 8:'),
    ('         \'password = "sun9"\\nif len(password) <= 8:',
     '         \'password = "sunshine"\\nif len(password) <= 8:'),
    # test expects "no digit" now (length check passes at 8)
    ('("validates password", \'assert printed == ["weak"], f"got {printed}"\',',
     '("validates password", \'assert printed == ["no digit"], f"got {printed}"\','),
    ("              \"First check length with len(); elif not any character.isdigit().\")",
     "              \"Eight chars pass the length check; the digit check must fire (elif).\")"),
    # ── shipping: boilerplate weight=2.5 -> 1.0 (boundary), ref keeps <=, wrong uses <
    ('            "weight = 2.5\\n",\n',
     '            "weight = 1.0\\n",\n'),
    ('("py-val-shipping", "weight = 2.5\\nif weight <= 1:',
     '("py-val-shipping", "weight = 1.0\\nif weight <= 1:'),
    ('         "weight = 2.5\\nif weight < 1:',
     '         "weight = 1.0\\nif weight < 1:'),
    # prompt updated to mention boundary
    ('\'weight = 2.5 is given (kg). Print the cost: 5.0 for up to 1kg, 9.0 for up to 5kg, 15.0 above — formatted with :.2f.\'',
     '\'weight = 1.0 is given (kg — right on the boundary). Print the cost: 5.0 for up to 1kg inclusive, 9.0 for up to 5kg, 15.0 above — formatted with :.2f.\''),
]
for old, new in fixes:
    assert old in src, "MISS: " + old[:70]
    src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("remaining m4 fixes applied; parse OK")
