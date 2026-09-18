"""Fix CP_MDX/CP_MDX_VI assignments (missing closing paren case)."""
import ast

p = "scripts/content-authoring/pypb_m2.py"
src = open(p, encoding="utf-8").read()

# CP_MDX = (  <newline> """..."""  <newline? no closing paren>  ->  CP_MDX = """..."""
src = src.replace("CP_MDX = (\n\"\"\"", "CP_MDX = \"\"\"")
src = src.replace("CP_MDX_VI = (\n\n\"\"\"", "CP_MDX_VI = \"\"\"")
src = src.replace("CP_MDX_VI = (\n\"\"\"", "CP_MDX_VI = \"\"\"")

# The blocks end with '"""' followed by blank lines and the next statement.
# For CP_MDX the original file had ') ' after the closing quotes in my intent:
# find "Module 2 is complete.\n\"\"\"\n" and add nothing — string already closed.
# For CP_MDX_VI: ends with '"""' then blank then write_checkpoint — fine.

open(p, "w", encoding="utf-8").write(src)
ast.parse(open(p, encoding="utf-8").read())
print("CP blocks fixed; parse OK")
