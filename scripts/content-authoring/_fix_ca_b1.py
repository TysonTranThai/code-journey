#!/usr/bin/env python3
"""Minimal repair for the six failing batch-1 challenges in ca_m1_2.py.
Zero-backslash style: embedded quotes are built with Q/APos concatenation so
the tool transport cannot corrupt anything.
"""
import ast

P = "ca_m1_2.py"
src = open(P, encoding="utf-8").read()

CE = "@CE@"
Q = chr(34)      # double quote
APOS = chr(39)   # single quote

# ------------------------------------------------------------------ A
n0 = src.count("CHECK_TRUE")
src = src.replace("CHECK_TRUE(", "CHECK(")
print("A: CHECK_TRUE -> CHECK:", n0)

# ------------------------------------------------------------------ B
old_prompt = (
    "This platform documents it. Implement `void program(void)` that prints two lines:"
    + CE + " " + CE + "```" + CE + "plain char: signed" + CE + "min value: -128" + CE
    + "```" + CE + " " + CE
    + "Derive BOTH facts at runtime, not by hard-coding text: assign `(char)-1`, "
    "compare against -1 or 255 to decide `signed` vs `unsigned`, and print "
    "`CHAR_MIN` (from `<limits.h>`) for the min value."
)
new_prompt = (
    "On a typical x86-64 Linux box plain char is signed; on this machine it is not — "
    "implementation-defined means the platform decides and your code must adapt. "
    "Implement `void program(void)` that prints two lines:" + CE + " " + CE + "```" + CE
    + "plain char: <signed|unsigned — derived>" + CE + "min value: <CHAR_MIN>" + CE
    + "```" + CE + " " + CE
    + "Derive BOTH facts at runtime: assign `(char)-1` and compare with -1 (signed) or "
    "255 (unsigned), then print `CHAR_MIN` from `<limits.h>`. Your output here may "
    "differ from x86-64 — that difference is the lesson."
)
assert old_prompt in src, "B: prompt anchor"
src = src.replace(old_prompt, new_prompt)

old_t1 = (
    '("derived signedness", '
    + APOS + "const char* out = cj_capture(program);" + CE
    + "CHECK_STR_EQ(out, " + Q + "plain char: signed" + CE + "min value: -128" + CE + Q + ");"
    + APOS + ", "
    + Q + "char probe = (char)-1; probe == -1 means signed; probe == 255 means unsigned."
    + Q + "),"
)
new_t1 = (
    '("derived signedness", '
    + APOS + "const char* out = cj_capture(program);" + CE
    + "char probe = (char)-1; CHECK_CONTAINS(out, probe == -1 ? " + Q + "signed" + Q
    + " : " + Q + "unsigned" + Q + ");"
    + APOS + ", "
    + Q + "The test derives the platform truth the same way your code must: probe == -1 "
    "means signed, probe == 255 means unsigned."
    + Q + "),"
)
assert old_t1 in src, "B: t1 anchor"
src = src.replace(old_t1, new_t1)

old_t2 = (
    '("min comes from limits.h", '
    + APOS + "CHECK_CONTAINS(cj_capture(program), " + Q + "-128" + Q + ");"
    + APOS + ", "
    + Q + "Print CHAR_MIN — the header value, not a literal."
    + Q + "),"
)
new_t2 = (
    '("exact two-line output", '
    + APOS + "char probe = (char)-1;" + CE + "char mn[64];" + CE
    + "sprintf(mn, " + Q + "plain char: %s" + CE + "min value: %d" + CE + Q + ", "
    + "probe == -1 ? " + Q + "signed" + Q + " : " + Q + "unsigned" + Q + ", CHAR_MIN);"
    + CE + "CHECK_STR_EQ(cj_capture(program), mn);"
    + APOS + ", "
    + Q + "sprintf builds the platform-truth expectation from probe and CHAR_MIN, then "
    "the program must match it exactly — hard-coding either line fails somewhere."
    + Q + "),"
)
assert old_t2 in src, "B: t2 anchor"
src = src.replace(old_t2, new_t2)

old_vi_prompt = (
    '"In hai dòng theo đúng định dạng, suy luận cả hai sự kiện lúc chạy: '
    "gán (char)-1 để biết dấu, in CHAR_MIN cho giá trị nhỏ nhất.\","
)
new_vi_prompt = (
    '"In hai dòng đúng định dạng, suy luận cả hai sự kiện lúc chạy: gán (char)-1 để biết '
    "dấu (nền tảng này là unsigned), in CHAR_MIN từ limits.h.\","
)
assert old_vi_prompt in src, "B: VI prompt anchor"
src = src.replace(old_vi_prompt, new_vi_prompt)

old_vi_h2 = (
    '("min từ limits.h", "In CHAR_MIN — giá trị từ header, không phải literal."),'
)
new_vi_h2 = (
    '("đầu ra đúng hai dòng", "Tạo kỳ vọng từ probe và CHAR_MIN rồi so khớp chính xác — hard-code chữ sẽ sai trên nền tảng khác."),'
)
assert old_vi_h2 in src, "B: VI hint2 anchor"
src = src.replace(old_vi_h2, new_vi_h2)
print("B: two-char prompt/tests/VI rewritten (ledger untouched)")

# ------------------------------------------------------------------ C
old_prompt = (
    "- `rep_bytes(1e-300)` is 1: a tiny subnormal whose only zero byte above the lowest "
    "nonzero byte is at index 6 — the scan decides, never assume."
)
new_prompt = (
    "- `rep_bytes(5e-324)` is 7: the smallest positive subnormal is 0x0000000000000001 — "
    "its single nonzero byte is index 0, so exactly the seven bytes above it are zero."
)
assert old_prompt in src, "C: prompt anchor"
src = src.replace(old_prompt, new_prompt)

old_t = (
    '("tiny subnormal", ' + APOS + "CHECK_EQ((int)rep_bytes(1e-300), 1);" + APOS + ", "
    + Q + "Scan down from index 7 and stop at the first nonzero byte; for 1e-300 exactly "
    "one top byte is zero." + Q + "),"
)
new_t = (
    '("tiny subnormal", ' + APOS + "CHECK_EQ((int)rep_bytes(5e-324), 7);" + APOS + ", "
    + Q + "0x0000000000000001: one nonzero byte at index 0, so scanning from index 7 "
    "counts seven zero bytes." + Q + "),"
)
assert old_t in src, "C: test anchor"
src = src.replace(old_t, new_t)

old_vi = (
    '("subnormal nhỏ", "Quét từ trên xuống và dừng tại byte khác 0 đầu tiên; với 1e-300 đúng một byte trên bằng 0."),'
)
new_vi = (
    '("subnormal nhỏ", "0x0000000000000001: byte khác 0 duy nhất ở chỉ số 0, nên quét từ trên xuống đếm được 7 byte 0."),'
)
assert old_vi in src, "C: VI anchor"
src = src.replace(old_vi, new_vi)
print("C: rep-copy 1e-300 -> 5e-324 (prompt/test/VI; ledger untouched)")

# ------------------------------------------------------------------ D
old_t = (
    '("correct arithmetic", '
    + APOS + "CHECK_EQ(sequenced_sum(5), 11);" + CE + "CHECK_EQ(sequenced_sum(0), 1);"
    + CE + "CHECK_EQ(sequenced_sum(-3), -7);"
    + APOS + ", "
    + Q + "Return start + (start + 1) or equivalent — the point is doing it without i++ "
    "twice in one expression." + Q + "),"
)
new_t = (
    '("correct arithmetic", '
    + APOS + "CHECK_EQ(sequenced_sum(5), 11);" + CE + "CHECK_EQ(sequenced_sum(0), 1);"
    + CE + "CHECK_EQ(sequenced_sum(-3), -5);"
    + APOS + ", "
    + Q + "start + (start + 1): for -3 that is -3 + -2 = -5 — computed via temporaries "
    "or separate statements, never two unsequenced ++." + Q + "),"
)
assert old_t in src, "D: t1 anchor"
src = src.replace(old_t, new_t)
print("D: sequenced-sum arithmetic fixed (-7 -> -5); src discriminator kept with CHECK")

# ------------------------------------------------------------------ E
old_t = (
    '("counters consistent", ' + Q + "CHECK_EQ(counters_match_sum(2), 1);" + Q + ", "
    + Q + "After exactly one call each, both counters total 2." + Q + "),"
)
new_t = (
    '("counters consistent", ' + Q + "CHECK_EQ(observed_sum(), 2);" + CE
    + "CHECK_EQ(counters_match_sum(2), 1);" + Q + ", "
    + Q + "Call observed_sum() first so each bump happens exactly once in this process; "
    "then 2 is the only consistent total." + Q + "),"
)
assert old_t in src, "E: anchor"
src = src.replace(old_t, new_t)
print("E: order-probe counters test now calls observed_sum() first")

# ------------------------------------------------------------------ save
open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print("AST OK — saved")
