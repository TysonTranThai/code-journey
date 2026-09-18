"""One-shot fixer for hsg_m6.py verification defects.

1. desc-median R: drop the trailing space (byte-exact contest grading).
2. rank: expectations/prompts must state dense ranks 3 1 2 1 (R was right).
3. scoreboard: W near-miss becomes an alphabetical tie-break (deterministic),
   and tie test data uses non-alphabetical input order.
Idempotent-ish: aborts without writing if any anchor is missing.
"""
import io

P = "scripts/content-authoring/hsg_m6.py"
s = io.open(P, encoding="utf-8").read()
orig = s

# --- 1. desc-median R: separator only between values -------------------
old = r'out << a[i] << \" \";\n    out << \"\n\";'
new = r'out << a[i] << (i + 1 < n ? \" \" : \"\n\");'
assert s.count(old) == 1, "desc-median anchor: %d" % s.count(old)
s = s.replace(old, new)

# --- 2. rank: dense-rank expectations -----------------------------------
assert s.count("4 1 3 1") == 3, "rank anchor: %d" % s.count("4 1 3 1")
s = s.replace("4 1 3 1", "3 1 2 1")
s = s.replace("30 is 4th", "30 is 3rd distinct")  # not present, harmless

# --- 3. scoreboard tie data + W comparator ------------------------------
# EN sample test data + hint
old = '"3\\nan 50\\nbinh 80\\ncuong 50\\n", "binh 80\\nan 50\\ncuong 50\\n", "Tie 50: an entered first."'
new = '"3\\ntrang 50\\nbinh 80\\nan 50\\n", "binh 80\\ntrang 50\\nan 50\\n", "Tie 50: trang entered first."'
assert s.count(old) == 1, "sb sample: %d" % s.count(old)
s = s.replace(old, new)

# EN prompt example
old = "`3` / `an 50` / `binh 80` / `cuong 50` →\n`binh 80` / `an 50` / `cuong 50` (an before cuong: input order)."
new = "`3` / `trang 50` / `binh 80` / `an 50` →\n`binh 80` / `trang 50` / `an 50` (trang before an: input order)."
assert s.count(old) == 1, "sb en prompt: %d" % s.count(old)
s = s.replace(old, new)

# VI prompt example
old = "`3` / `an 50` / `binh 80` / `cuong 50` → `binh 80` / `an 50` / `cuong 50`."
new = "`3` / `trang 50` / `binh 80` / `an 50` → `binh 80` / `trang 50` / `an 50`."
assert s.count(old) == 1, "sb vi prompt: %d" % s.count(old)
s = s.replace(old, new)

# VI sample hint
old = '("ví dụ đề bài", "Hòa 50: an nhập trước.")'
new = '("ví dụ đề bài", "Hòa 50: trang nhập trước.")'
assert s.count(old) == 1, "sb vi hint: %d" % s.count(old)
s = s.replace(old, new)

# all-tie test data (alphabetical names hid the defect)
old = '"3\\na 5\\nb 5\\nc 5\\n", "a 5\\nb 5\\nc 5\\n"'
new = '"3\\nnam 5\\nanh 5\\nbinh 5\\n", "nam 5\\nanh 5\\nbinh 5\\n"'
assert s.count(old) == 1, "sb all-tie: %d" % s.count(old)
s = s.replace(old, new)

# W comparator: alphabetical tie-break (patch the SECOND identical line)
ret = "        return a.first > b.first;"
first = s.find(ret)
second = s.find(ret, first + 1)
assert first != -1 and second != -1, "comparator anchors missing"
w_ret = "        return a.first > b.first || (a.first == b.first && a.second < b.second);"
s = s[:second] + w_ret + s[second + len(ret):]

# W comment: describe the actual near-miss
old = ("// near-miss: plain sort is NOT stable — equal scores may be reordered\n"
       "    // away from input order (implementation-defined here, and the tie\n"
       "    // contract is genuinely broken for equal keys)")
new = ("// near-miss: breaks score ties ALPHABETICALLY by name — the\n"
       "    // scoreboard contract requires ties to keep input order, which\n"
       "    // this silently violates whenever the input order differs")
assert s.count(old) == 1, "sb w comment: %d" % s.count(old)
s = s.replace(old, new)

assert s != orig
io.open(P, "w", encoding="utf-8").write(s)

import ast
ast.parse(s)
print("fixer ok")
