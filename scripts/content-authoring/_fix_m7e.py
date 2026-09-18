"""Strengthen py-fn-refactor-greeting + py-fn-pipeline graders (return contract, boundary)."""
import ast, json, re

p = "scripts/content-authoring/pypb_m7.py"
src = open(p, encoding="utf-8").read()

# 1. greeting: require greet to RETURN the string (test calls greet directly and
#    checks the value, so print-only implementations fail).
old = '''("same output, now factored", 'assert printed == ["Welcome Minh, your balance is 120", "Welcome Lan, your balance is 90", "Welcome Bo, your balance is 0"], f"got {printed}"\\nassert "def greet" in code and code.count("Welcome") <= 1, "one greet() function, one Welcome string"','''
new = '''("same output, now factored", 'assert printed == ["Welcome Minh, your balance is 120", "Welcome Lan, your balance is 90", "Welcome Bo, your balance is 0"], f"got {printed}"\\nassert "def greet" in code, "define greet(name, balance)"\\nassert greet("Test", 5) == "Welcome Test, your balance is 5", "greet must RETURN the string, not print it"','''
assert old in src, "greeting test drifted"
src = src.replace(old, new)

# 2. pipeline: wrong uses price > 100 (fails at exactly 100). Add a boundary call
#    requirement: process_order(100) must equal 95.00 printed as third line.
old = '''("pipeline results", 'assert printed == ["140.00", "55.00"], f"got {printed}"','''
new = '''("pipeline results", 'assert printed == ["140.00", "55.00", "95.00"], f"got {printed}"\\nassert process_order(100) == 95.0, "at exactly 100 the discount applies (>= 100)"','''
assert old in src, "pipeline test drifted"
src = src.replace(old, new)
# and the challenge prompt + wrong solution stay: wrong prints only two lines and
# uses > 100 — third line missing AND direct call fails. Update ref to print 3 lines.
old = '("py-fn-pipeline", "def process_order(price):\\n    if price >= 100:\\n        price *= 0.9\\n    return price + 5\\n\\nprint(f\\"{process_order(150):.2f}\\")\\nprint(f\\"{process_order(50):.2f}\\")",'
new = '("py-fn-pipeline", "def process_order(price):\\n    if price >= 100:\\n        price *= 0.9\\n    return price + 5\\n\\nprint(f\\"{process_order(150):.2f}\\")\\nprint(f\\"{process_order(50):.2f}\\")\\nprint(f\\"{process_order(100):.2f}\\")",'
assert old in src, "pipeline ref drifted"
src = src.replace(old, new)
old = '         "def process_order(price):\\n    if price > 100:\\n        price *= 0.9\\n    return price + 5\\n\\nprint(f\\"{process_order(150):.2f}\\")\\nprint(f\\"{process_order(50):.2f}\\")"),'
new = '         "def process_order(price):\\n    if price > 100:\\n        price *= 0.9\\n    return price + 5\\n\\nprint(f\\"{process_order(150):.2f}\\")\\nprint(f\\"{process_order(50):.2f}\\")\\nprint(f\\"{process_order(100):.2f}\\")"),'
assert old in src, "pipeline wrong drifted"
src = src.replace(old, new)
# prompt mentions the third check
old = "Xây process_order(price): giảm 10% nếu price >= 100, rồi cộng 5 tiền ship, và trả về tổng cuối. In process_order(150) và process_order(50) — hai dòng với định dạng :.2f."
new = "Xây process_order(price): giảm 10% nếu price >= 100 (biên 100 cũng được giảm!), rồi cộng 5 tiền ship, và trả về tổng cuối. In process_order(150), process_order(50), và process_order(100) — ba dòng với định dạng :.2f."
assert old in src
src = src.replace(old, new)

open(p, "w", encoding="utf-8").write(src)
ast.parse(src)
print("m7 graders strengthened; parse OK")
