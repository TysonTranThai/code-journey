"""Finish m4 strengthening: ticket boilerplate + wrong-solution swap."""
import ast

p = "scripts/content-authoring/pypb_m4.py"
src = open(p, encoding="utf-8").read()

# ticket challenge boilerplate age=17
src = src.replace(
    '            "age = 19\\nhas_id = True\\n",\n            [("decides entry"',
    '            "age = 17\\nhas_id = True\\n",\n            [("decides entry"',
)
# ticket reference: age=19 -> age=17 (and-branch ref stays)
src = src.replace(
    '("py-logic-ticket", "age = 19\\nhas_id = True\\nif age >= 18 and has_id:',
    '("py-logic-ticket", "age = 17\\nhas_id = True\\nif age >= 18 and has_id:',
)
# ticket wrong: age=19 -> age=17 (or-branch wrong)
src = src.replace(
    '         "age = 19\\nhas_id = True\\nif age >= 18 or has_id:',
    '         "age = 17\\nhas_id = True\\nif age >= 18 or has_id:',
)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("ticket fixed; parse OK")
