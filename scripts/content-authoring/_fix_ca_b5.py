#!/usr/bin/env python3
"""Repair batch-5 defects in ca_m9_10.py (stringize + variadic-log).
Idempotent: safe to run multiple times. Zero typed backslashes; quotes via chr().
"""
import ast

P = "ca_m9_10.py"
src = open(P, encoding="utf-8").read()
Q = chr(34)
B = chr(92)
DQ2 = B + Q  # escaped double quote as file bytes

# ---------------- stringize challenge: BUILD_ID-based, deterministic ----------
old_fn_a = "line_marker"
if "id_string" not in src:
    # prompt
    old_p = (
        "returning the current line number as a string via STR(__LINE__) " + chr(8212)
        + " and " + chr(96) + "const char *raw_marker(void)" + chr(96) + Q
        + " returning what STR_(__LINE__) yields: the literal text."
    )
    new_p = (
        "and a file-scope " + chr(96) + "#define BUILD_ID 77" + chr(96) + Q + ", implement "
        + chr(96) + "const char *id_string(void)" + chr(96) + Q + " returning STR(BUILD_ID) "
        + chr(8212) + " the expanded value as text " + chr(8212) + " and "
        + chr(96) + "const char *id_raw(void)" + chr(96) + Q
        + " returning what STR_(BUILD_ID) yields: the bare token name."
    )
    assert old_p in src, "prompt"
    src = src.replace(old_p, new_p)

    # boilerplate define: the challenge's boilerplate currently has STR_/STR
    # (it is added in the test call, not editable here) — BUILD_ID is provided
    # by the solution; the test only checks returned strings, so no boilerplate
    # change is needed.

    # tests
    old_t1_code = "const char *s = line_marker();@NL@CHECK_EQ((int)atoi(s), __LINE__);"
    new_t1_code = "CHECK_STR_EQ(id_string(), " + DQ2 + "77" + DQ2 + ");"
    assert old_t1_code in src, "t1 code"
    src = src.replace(old_t1_code, new_t1_code)
    src = src.replace(
        "STR(__LINE__) stringizes the expanded number; atoi of it equals the line the macro sat on.",
        "STR(BUILD_ID) first expands BUILD_ID to 77, then stringizes it: the result is the text 77.",
    )

    old_t2_code = "CHECK_STR_EQ(raw_marker(), " + DQ2 + "__LINE__" + DQ2 + ");"
    new_t2_code = "CHECK_STR_EQ(id_raw(), " + DQ2 + "BUILD_ID" + DQ2 + ");"
    assert old_t2_code in src, "t2 code"
    src = src.replace(old_t2_code, new_t2_code)
    src = src.replace(
        "so the string is the bare token." + Q + "),",
        "so the string is the bare token name." + Q + "),",
    )

    # VI
    src = src.replace(
        "STR(__LINE__) stringize số đã mở rộng; atoi của nó bằng dòng chứa macro.",
        "STR(BUILD_ID) mở rộng BUILD_ID thành 77 rồi stringize: kết quả là chữ 77.",
    )

    # ledger
    sol_i = src.index("solutions=[")
    head, tail = src[:sol_i], src[sol_i:]
    old_r = "const char *line_marker(void) { return STR(__LINE__); }@NL@"
    if old_r in tail:
        tail = tail.replace(
            old_r,
            "const char *id_string(void) { return STR(BUILD_ID); }@NL@"
            + "const char *id_raw(void) { return STR_(BUILD_ID); }@NL@",
        )
    old_w = (
        "const char *line_marker(void) { return STR_(__LINE__); }@NL@"
        + "const char *raw_marker(void) { return STR_(__LINE__); }@NL@"
    )
    if old_w in tail:
        tail = tail.replace(
            old_w,
            "const char *id_string(void) { return STR_(BUILD_ID); }@NL@"
            + "const char *id_raw(void) { return STR_(BUILD_ID); }@NL@",
        )
    src = head + tail
    print("stringize rewritten")

# BUILD_ID must exist in the ledger's R and W sources. Add after the STR define.
sol_i = src.index("solutions=[")
head, tail = src[:sol_i], src[sol_i:]
hdr = "#define STR(x) STR_(x)@NL@"
count = tail.count(hdr)
if count and "#define BUILD_ID 77@NL@" not in tail:
    tail = tail.replace(hdr, hdr + "#define BUILD_ID 77@NL@")
    print("BUILD_ID added to", count, "ledger sources")
src = head + tail

# ---------------- variadic-log W: leave the bare trailing comma ---------------
sol_i = src.index("solutions=[")
head, tail = src[:sol_i], src[sol_i:]
old_w_def = (
    "#define LOG(fmt, ...) snprintf(logbuf + loglen, sizeof logbuf - loglen, fmt, ##__VA_ARGS__)@NL@"
)
new_w_def = (
    "#define LOG(fmt, ...) snprintf(logbuf + loglen, sizeof logbuf - loglen, fmt, __VA_ARGS__)@NL@"
)
n = tail.count(old_w_def)
if n == 1:
    tail = tail.replace(old_w_def, new_w_def)
    print("variadic W comma defect applied")
src = head + tail

open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print("AST OK")
