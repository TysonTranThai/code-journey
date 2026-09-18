#!/usr/bin/env python3
"""Redesign ca2-dangling: tests must never depend on UB outcomes.
The old tests dereferenced/compared an indeterminate dangling pointer
(GCC folds `leak_local() != 0` to false; the deref segfaulted). New design:
implement safe_read() — the lifetime-correct counterpart — which is fully
defined and deterministic.
Zero-backslash style (quotes built via chr()).
"""
import ast

P = "ca_m1_2.py"
src = open(P, encoding="utf-8").read()

CE = "@CE@"
Q = chr(34)

START = 'challenge(\n            "ca2-dangling",'
i0 = src.index(START)
END_ANCHOR = 'level="debugging",\n        ),'
i1 = src.index(END_ANCHOR, i0) + len(END_ANCHOR)

new_block = (
    'challenge(\n'
    '            "ca2-dangling",\n'
    '            "Read Inside the Lifetime",\n'
    '            "The helper below is already in your editor — and it is deliberately buggy:'
    + CE + " " + CE + "```c" + CE
    + "static int g_probe = 7;" + CE
    + "static int *leak_local(void) { int local = g_probe; return &local; }" + CE
    + "```" + CE + " " + CE
    + "The pointer it returns is *indeterminate* the moment `local` dies: dereferencing it "
    "is UB, and even *comparing* it (say, `leak_local() != 0`) is UB — the optimizer "
    "exploits that and folds the check away. Never touch a dangling value. Implement "
    "`int safe_read(void)`: the defined counterpart — take the address of an automatic "
    "`int` initialized from `g_probe`, dereference the pointer *while the object is "
    'alive*, and return the value it reads.",\n'
    '            GIVEN_LEAK,\n'
    '            [\n'
    '                ("defined read", "CHECK_EQ(safe_read(), 7);", '
    '"p = &local; return *p; — the read happens before the block ends, so it is '
    'perfectly defined."),\n'
    '                ("matches the probe", "CHECK_EQ(safe_read(), g_probe);", '
    '"The defined path must observe exactly g_probe — the same value leak_local '
    '*would* have dangled with."),\n'
    '                ("repeatable", "CHECK_EQ(safe_read(), safe_read());", '
    '"A lifetime-correct read is stable; UB is the thing that comes and goes."),\n'
    '            ],\n'
    '            level="debugging",\n'
    '        ),'
)
src = src[:i0] + new_block + src[i1:]
print("challenge block replaced")

# VI entry
VSTART = '"ca2-dangling": vi_challenge('
j0 = src.index(VSTART)
VEND = "\n        ),"
j1 = src.index(VEND, j0) + len(VEND)
new_vi = (
    VSTART + "\n"
    '            "Đọc trong vòng đời",\n'
    '            "Con trỏ từ leak_local là *không xác định* sau khi local chết: hủy tham '
    'chiếu là UB, kể cả so sánh cũng là UB. Cài `int safe_read(void)`: lấy địa chỉ một '
    'biến tự động khởi tạo từ g_probe, hủy tham chiếu *khi đối tượng còn sống*, trả về '
    'giá trị.",\n'
    "            [\n"
    '                ("đọc hợp lệ", "p = &local; return *p; — phép đọc xảy ra trước khi '
    'khối kết thúc."),\n'
    '                ("khớp probe", "Đường hợp lệ phải quan sát đúng g_probe."),\n'
    '                ("lặp lại ổn định", "Đọc đúng vòng đời thì ổn định; UB mới là thứ '
    'đến rồi đi."),\n'
    "            ],"
)
src = src[:j0] + new_vi + src[j1:]
print("VI entry replaced")

# Ledger pair
LSTART = '        (\n            "ca2-dangling",'
k0 = src.index(LSTART)
LEND = "\n        ),\n"
k1 = src.index(LEND, k0) + len(LEND)
GL = "GIVEN_LEAK\n            + "
new_led = (
    "        (\n"
    '            "ca2-dangling",\n'
    "            " + GL
    + "'int safe_read(void) {@NL@    int local = g_probe;@NL@    int *p = &local;@NL@"
    + "    return *p;@NL@}@NL@int main(void) { return 0; }',\n"
    "            " + GL
    + "'int safe_read(void) {@NL@    return g_probe + 1;@NL@}@NL@int main(void) "
    + "{ return 0; }',\n"
    + "        ),\n"
)
src = src[:k0] + new_led + src[k1:]
print("ledger pair replaced")

open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print("AST OK — saved")
