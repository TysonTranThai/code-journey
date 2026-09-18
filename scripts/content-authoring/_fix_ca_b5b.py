#!/usr/bin/env python3
"""Finish batch-5 repairs (stringize + variadic-log), line-based and robust."""
import ast

P = "ca_m9_10.py"
lines = open(P, encoding="utf-8").read().split(chr(10))
Q = chr(34)
B = chr(92)
DQ2 = B + Q

def find_line(pred, start=0):
    for i in range(start, len(lines)):
        if pred(lines[i]):
            return i
    raise AssertionError("line not found")

# ---- prompt line: replace wholesale -----------------------------------------
i = find_line(lambda l: "line_marker(void)` returning the current line number" in l)
lines[i] = (
    "            " + Q + "Given the classic wrapper pair already in your editor (`STR_` and `STR`) "
    "and a file-scope `#define BUILD_ID 77`, implement `const char *id_string(void)` "
    "returning STR(BUILD_ID) — the expanded value as text — and `const char *id_raw(void)` "
    "returning what STR_(BUILD_ID) yields: the bare token name." + Q + ","
)

# ---- test 1 line -------------------------------------------------------------
i = find_line(lambda l: "atoi(s), __LINE__" in l)
lines[i] = (
    "                (" + Q + "double expansion stringizes the value" + Q + ", "
    + Q + "CHECK_STR_EQ(id_string(), " + DQ2 + "77" + DQ2 + ");" + Q + ", "
    + Q + "STR(BUILD_ID) first expands BUILD_ID to 77, then stringizes it: "
    "the result is the text 77." + Q + "),"
)

# ---- test 2 line -------------------------------------------------------------
i = find_line(lambda l: "raw_marker(), " in l)
lines[i] = (
    "                (" + Q + "single expansion keeps the name" + Q + ", "
    + Q + "CHECK_STR_EQ(id_raw(), " + DQ2 + "BUILD_ID" + DQ2 + ");" + Q + ", "
    + Q + "STR_ never expands its argument, so the string is the bare token name." + Q + "),"
)

# ---- VI prompt line ----------------------------------------------------------
i = find_line(lambda l: "Cài line_marker() trả số dòng" in l)
lines[i] = (
    "            " + Q + "Có sẵn cặp STR_/STR và `#define BUILD_ID 77`. Cài id_string() trả STR(BUILD_ID) "
    "(văn bản 77), và id_raw() trả STR_(BUILD_ID) — tên token trần." + Q + ","
)

# ---- VI hint line ------------------------------------------------------------
i = find_line(lambda l: "atoi của nó bằng dòng chứa macro" in l)
lines[i] = (
    "                (" + Q + "mở rộng kép stringize giá trị" + Q + ", "
    + Q + "STR(BUILD_ID) mở rộng BUILD_ID thành 77 rồi stringize: kết quả là chữ 77." + Q + "),"
)

# ---- ledger R/W --------------------------------------------------------------
i = find_line(lambda l: "line_marker(void) { return STR(__LINE__); }" in l)
lines[i] = (
    "            + " + Q + "const char *id_string(void) { return STR(BUILD_ID); }@NL@"
    "const char *id_raw(void) { return STR_(BUILD_ID); }@NL@" + Q
)
i = find_line(lambda l: "raw_marker(void) { return STR_(__LINE__); }" in l)
lines[i] = (
    "            + " + Q + "const char *id_string(void) { return STR_(BUILD_ID); }@NL@"
    "const char *id_raw(void) { return STR_(BUILD_ID); }@NL@" + Q
)

# ---- add BUILD_ID define to ledger sources (R and W entry starts) ------------
src = chr(10).join(lines)
sol_i = src.index("solutions=[")
head, tail = src[:sol_i], src[sol_i:]
hdr = "#define STR(x) STR_(x)@NL@"
if "#define BUILD_ID 77@NL@" not in tail:
    n = tail.count(hdr)
    tail = tail.replace(hdr, hdr + "#define BUILD_ID 77@NL@")
    print("BUILD_ID added to", n, "ledger sources")
src = head + tail

# ---- variadic W: bare trailing comma (deterministic compile failure) ---------
sol_i = src.index("solutions=[")
head, tail = src[:sol_i], src[sol_i:]
old_w_def = "#define LOG(fmt, ...) snprintf(logbuf + loglen, sizeof logbuf - loglen, fmt, ##__VA_ARGS__)@NL@"
new_w_def = "#define LOG(fmt, ...) snprintf(logbuf + loglen, sizeof logbuf - loglen, fmt, __VA_ARGS__)@NL@"
if old_w_def in tail:
    tail = tail.replace(old_w_def, new_w_def)
    print("variadic W comma defect applied")
src = head + tail

open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print("AST OK — saved")
