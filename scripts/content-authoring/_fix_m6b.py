"""Fix flat hint list in py-loop-times-table vi_challenge call."""
import ast

p = "scripts/content-authoring/pypb_m6.py"
src = open(p, encoding="utf-8").read()

old = 'vi_challenge("Dòng bảng cửu chương", "n = 7 đã cho. In bảng nhân 7 từ 1x đến 3x thành ba dòng: 7 / 14 / 21 — với range().",\n                                          "ba bội số", "for i in range(1, 4): print(n * i)"))'
new = 'vi_challenge("Dòng bảng cửu chương", "n = 7 đã cho. In bảng nhân 7 từ 1x đến 3x thành ba dòng: 7 / 14 / 21 — với range().",\n                                          [("ba bội số", "for i in range(1, 4): print(n * i)")]))'
assert old in src, "pattern drifted"
src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("times-table vi fixed; parse OK")
