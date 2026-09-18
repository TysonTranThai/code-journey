"""Regex-wrap every remaining flat vi_challenge hint list as a tuple."""
import ast, re

p = "scripts/content-authoring/pypb_m7.py"
src = open(p, encoding="utf-8").read()

pat = re.compile(r'(vi_challenge\((?:[^()"]|"[^"]*")*\[\s*)("(?:[^"\\]|\\.)*"),\s*("(?:[^"\\]|\\.)*")(\s*\]\))')


def wrap(m):
    return m.group(1) + "(" + m.group(2) + ", " + m.group(3) + ")" + m.group(4)


src, n = pat.subn(wrap, src)
print("wrapped", n, "flat lists")
open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("parse OK")
