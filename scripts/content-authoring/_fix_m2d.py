"""Remove duplicated VI minutes from the three write_lesson calls."""
import ast

p = "scripts/content-authoring/pypb_m2.py"
src = open(p, encoding="utf-8").read()

fixes = [
    ('"Tên gọi giúp ghi nhớ: gán, quy tắc đặt tên, gán lại.", 10, L_VAR_VI)',
     '"Tên gọi giúp ghi nhớ: gán, quy tắc đặt tên, gán lại.", L_VAR_VI)'),
    ('"Các kiểu lõi: int, float, bool, None — và chuyển đổi giữa chúng.", 12, L_TYPES_VI)',
     '"Các kiểu lõi: int, float, bool, None — và chuyển đổi giữa chúng.", L_TYPES_VI)'),
    ('"Số học, các kiểu chia, so sánh, logic boolean, và độ ưu tiên.", 12, L_OPS_VI)',
     '"Số học, các kiểu chia, so sánh, logic boolean, và độ ưu tiên.", L_OPS_VI)'),
]
for old, new in fixes:
    assert old in src, old
    src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("lesson calls fixed; parse OK")
