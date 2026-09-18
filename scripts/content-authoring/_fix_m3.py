"""Remove duplicated VI minutes from write_lesson calls in pypb_m3.py."""
import ast

p = "scripts/content-authoring/pypb_m3.py"
src = open(p, encoding="utf-8").read()

fixes = [
    ('"Ký tự theo vị trí, chỉ số từ số 0, và tính bất biến.", 10, L1_VI)',
     '"Ký tự theo vị trí, chỉ số từ số 0, và tính bất biến.", L1_VI)'),
    ('"Trích phần văn bản với [start:stop] — và quy tắc nửa mở.", 10, L2_VI)',
     '"Trích phần văn bản với [start:stop] — và quy tắc nửa mở.", L2_VI)'),
    ('"strip, upper, replace, split, join — bộ công cụ văn bản hằng ngày.", 12, L3_VI)',
     '"strip, upper, replace, split, join — bộ công cụ văn bản hằng ngày.", L3_VI)'),
    ('"Nhúng giá trị vào văn bản, định dạng số, escape, và chuỗi nhiều dòng.", 12, L4_VI)',
     '"Nhúng giá trị vào văn bản, định dạng số, escape, và chuỗi nhiều dòng.", L4_VI)'),
]
for old, new in fixes:
    assert old in src, old[:50]
    src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("fixed; parse OK")
