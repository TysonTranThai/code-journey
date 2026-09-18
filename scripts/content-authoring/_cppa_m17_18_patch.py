#!/usr/bin/env python3
"""Fix m17_18: decoder-W endian misread, sandboxer root pre-seed, hints."""
import ast
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
p = "cppa_m17_18.py"
src = open(p).read()

# 1) frame-decoder W: LE->BE misread (deterministically fails normal frames)
BS = chr(92)  # backslash
Q = chr(39)   # single quote
# The W-solution line is a single-quoted python literal containing \'x\' —
# locate it by its unique comment instead of reconstructing escapes.
marker = "// WRONG: allocates the unvalidated claim"
i = src.find(marker)
assert i > 0, "decoder W marker"
line_start = src.rfind(BS + "n", 0, i) + 2          # start of the C++ line within the literal
line_end = src.find(BS + "n", i)
old_line = src[line_start:line_end]
assert "payload(len" in old_line, repr(old_line)
new_line = (
    "        std::uint32_t len = std::uint32_t(buf_[3]) | std::uint32_t(buf_[2]) << 8 |"
    + BS + "n                            std::uint32_t(buf_[1]) << 16 | std::uint32_t(buf_[0]) << 24;"
    + "   // WRONG: big-endian misread"
)
src = src[:line_start] + new_line + src[line_end:]
c = 1

# 2) sandboxPath: remove root pre-seed + weaken guard (4 copies)
o1 = (BS + "n    std::vector<std::string> stack;" + BS + 'n    stack.push_back("data");')
n1 = BS + "n    std::vector<std::string> stack;"
c1 = src.count(o1)
src = src.replace(o1, n1)

o2 = (BS + 'n        if (seg == "..") {' + BS + "n            if (stack.size() <= 1) return std::nullopt;"
      + BS + "n            stack.pop_back();")
n2 = (BS + 'n        if (seg == "..") {' + BS + "n            if (stack.empty()) return std::nullopt;"
      + BS + "n            stack.pop_back();")
c2 = src.count(o2)
src = src.replace(o2, n2)

# 3) hints (EN x2, VI x1)
o3 = 'Stack of segments; start with {"data"}.'
n3 = "Stack of segments, empty to start."
c3 = src.count(o3)
src = src.replace(o3, n3)
o4 = 'The stack starts with exactly {"data"}; every'
n4 = "The stack starts empty; every"
c4 = src.count(o4)
src = src.replace(o4, n4)
o5 = 'Stack segment; khởi đầu {"data"}.'
n5 = "Stack segment; khởi đầu rỗng."
c5 = src.count(o5)
src = src.replace(o5, n5)

open(p, "w").write(src)
ast.parse(src)
print(f"decoder W ok; preseed {c1}; guard {c2}; hints {c3}/{c4}/{c5}; SYNTAX OK")
