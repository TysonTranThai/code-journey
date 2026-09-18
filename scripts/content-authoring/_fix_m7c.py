"""Wrap remaining flat VI hint lists in pypb_m7.py as (name, hint) tuples."""
import ast

p = "scripts/content-authoring/pypb_m7.py"
src = open(p, encoding="utf-8").read()

flat = [
    '["vị từ hoạt động", "return n % 2 == 0 — phép so sánh đã tạo ra boolean sẵn."]',
    '["chuyển đổi đúng", "Công thức có trong bài học; docstring là một dòng ba dấu ngoặc kép."]',
    '["tỉ lệ mặc định và tùy chọn", "return amount * (1 + rate) — mặc định làm đối số thứ hai trở nên tùy chọn."]',
    '["logic viết một nơi", "def is_ok(age, member): return age >= 18 and member — và cả hai wrapper gọi nó."]',
    '["kết quả đường ống", "150 >= 100 → 135 + 5 = 140; 50 → không giảm → 50 + 5 = 55."]',
]
for f in flat:
    assert f in src, f
    src = src.replace(f, "[" + f[1:-1] + "]")

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("flat VI lists wrapped; parse OK")
