"""Remove duplicated VI minutes from write_lesson calls in pypb_m5.py."""
import ast

p = "scripts/content-authoring/pypb_m5.py"
src = open(p, encoding="utf-8").read()

fixes = [
    ('"Ordered, mutable collections: append, insert, remove, sort.", 12, L1, "Danh sách (List)", "Collections có thứ tự, có thể thay đổi: append, insert, remove, sort.", 12, L1_VI)',
     '"Ordered, mutable collections: append, insert, remove, sort.", 12, L1, "Danh sách (List)", "Collections có thứ tự, có thể thay đổi: append, insert, remove, sort.", L1_VI)'),
    ('"Fixed-shape tuples and uniqueness-driven sets — when each wins.", 10, L2, "Tuple & Set", "Tuple hình dạng cố định và set dựa trên tính duy nhất — khi nào cái nào thắng.", 10, L2_VI)',
     '"Fixed-shape tuples and uniqueness-driven sets — when each wins.", 10, L2, "Tuple & Set", "Tuple hình dạng cố định và set dựa trên tính duy nhất — khi nào cái nào thắng.", L2_VI)'),
    ('"Key→value lookups, safe .get(), and iterating pairs.", 12, L3, "Từ điển (Dictionary)", "Tra cứu khóa→giá trị, .get() an toàn, và duyệt các cặp.", 12, L3_VI)',
     '"Key→value lookups, safe .get(), and iterating pairs.", 12, L3, "Từ điển (Dictionary)", "Tra cứu khóa→giá trị, .get() an toàn, và duyệt các cặp.", L3_VI)'),
    ('"Lists of dicts, dicts with lists — the shape of real data.", 10, L4, "Collection lồng nhau", "List của dict, dict chứa list — hình dạng của dữ liệu thật.", 10, L4_VI)',
     '"Lists of dicts, dicts with lists — the shape of real data.", 10, L4, "Collection lồng nhau", "List của dict, dict chứa list — hình dạng của dữ liệu thật.", L4_VI)'),
]
for old, new in fixes:
    assert old in src, "MISS: " + old[:60]
    src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("m5 lesson calls fixed; parse OK")
