#!/usr/bin/env python3
"""Repair the six batch-2 defects in ca_m3_4.py. Zero-backslash style."""
import ast

P = "ca_m3_4.py"
src = open(P, encoding="utf-8").read()
Q = chr(34)

def qq(s):
    return Q + s + Q

# ------------------------------------------------ A: cache tests self-contained
old = (
    '("miss is NULL", ' + qq("CHECK_NULL(cache_get(c, 999));") + ", "
    + qq("Absent keys must return NULL, not garbage.") + "),"
)
new = (
    '("miss is NULL", '
    + qq("cache_t *c = cache_create(4);@NL@CHECK_NULL(cache_get(c, 999));") + ", "
    + qq("A fresh cache; absent keys must return NULL, not garbage.") + "),"
)
assert old in src, "A1"
src = src.replace(old, new)

old = (
    '("full is rejected", '
    + qq("for (int k = 0; k < 4; k++) cache_put(c, k, k);@NL@CHECK_EQ(cache_put(c, 99, 99), 0);") + ", "
    + qq("cap is respected: the fifth insert reports 0.") + "),"
)
new = (
    '("full is rejected", '
    + qq("cache_t *c = cache_create(4);@NL@for (int k = 0; k < 4; k++) cache_put(c, k, k);@NL@CHECK_EQ(cache_put(c, 99, 99), 0);") + ", "
    + qq("cap is respected: the fifth insert reports 0.") + "),"
)
assert old in src, "A2"
src = src.replace(old, new)

old = (
    '("capacity boundary", '
    + qq("CHECK_EQ(cache_put(c, 98, 98), 0);") + ", "
    + qq("Still full after the failed insert — failed puts must not corrupt state.") + "),"
)
new = (
    '("update keeps capacity", '
    + qq("cache_t *c = cache_create(2);@NL@cache_put(c, 1, 10);@NL@cache_put(c, 2, 20);@NL@CHECK_EQ(cache_put(c, 1, 99), 1);@NL@CHECK_EQ(*cache_get(c, 1), 99);") + ", "
    + qq("Updating an existing key must succeed on a FULL cache — an update must not consume a new slot.") + "),"
)
assert old in src, "A3"
src = src.replace(old, new)

# VI text for the renamed test
old = '("biên năng lực", "Chèn thất bại không được làm hỏng trạng thái."),'
new = '("cập nhật giữ năng lực", "Cập nhật khóa tồn tại phải thành công cả khi cache ĐẦY — cập nhật không được tiêu thụ slot mới."),'
assert old in src, "A4"
src = src.replace(old, new)
print("A: cache tests self-contained + update discriminator")

# ------------------------------------------------ B: restrict tests use bytes
old = (
    '("overlap detection", '
    + qq("int v[4] = {0, 0, 0, 0};@NL@CHECK_EQ(ranges_overlap(v, 3, v + 2, 2), 1);@NL@CHECK_EQ(ranges_overlap(v, 2, v + 2, 2), 0);") + ", "
    + qq("Ranges [p, p+n) intersect iff p1 < p2+n2 && p2 < p1+n1 — pure pointer comparisons, no dereference.") + "),"
)
new = (
    '("overlap detection", '
    + qq("int v[4] = {0, 0, 0, 0};@NL@CHECK_EQ(ranges_overlap(v, 3 * sizeof(int), v + 2, 2 * sizeof(int)), 1);@NL@CHECK_EQ(ranges_overlap(v, 2 * sizeof(int), v + 2, 2 * sizeof(int)), 0);") + ", "
    + qq("Byte counts, memcpy-style: [v, v+12) vs [v+8, v+16) intersect; [v, v+8) vs [v+8, v+16) do not.") + "),"
)
assert old in src, "B1"
src = src.replace(old, new)

old = '("phát hiện chồng", "Hai vùng [p, p+n) giao nhau khi p1 < p2+n2 và p2 < p1+n1 — so sánh con trỏ thuần, không hủy tham chiếu."),'
new = '("phát hiện chồng", "Đếm theo BYTE kiểu memcpy: [v, v+12) giao [v+8, v+16); [v, v+8) không giao [v+8, v+16)."),'
assert old in src, "B2"
src = src.replace(old, new)
print("B: restrict tests now byte-based")

# ------------------------------------------------ C: ctx-foreach W loop defect
sol_i = src.index("solutions=[")
head, tail = src[:sol_i], src[sol_i:]
foreach_line = (
    "void foreach_int(const int *a, size_t n, void (*fn)(int v, void *ctx), void *ctx) {@NL@"
    "    for (size_t i = 0; i < n; i++) fn(a[i], ctx);@NL@}@NL@"
)
assert tail.count(foreach_line) == 2, "C: expected two identical foreach lines"
first = tail.index(foreach_line)
second = tail.index(foreach_line, first + 1)
buggy = foreach_line.replace("fn(a[i], ctx)", "fn(a[0], ctx)")
tail = tail[:second] + buggy + tail[second + len(foreach_line):]
src = head + tail
print("C: ctx-foreach W forwards the wrong element")

# ------------------------------------------------ D: memcpy-bits W byteswap
cast_line = (
    "unsigned int float_bits(float f) {@NL@    return *(unsigned int *)&f;@NL@}@NL@"
)
assert src.count(cast_line) == 1, "D: W cast line not found uniquely"
swap_line = (
    "unsigned int float_bits(float f) {@NL@    unsigned int u;@NL@    memcpy(&u, &f, sizeof u);@NL@"
    "    return ((u & 0xFFu) << 24) | ((u & 0xFF00u) << 8) | ((u >> 8) & 0xFF00u) | (u >> 24);@NL@}@NL@"
)
src = src.replace(cast_line, swap_line)
print("D: memcpy-bits W now byte-swaps (deterministic)")

# ------------------------------------------------ E: FNV expectations exact
old = (
    '("known FNV step", '
    + qq("CHECK_EQ(fnv1a_step(2166136261u, 0x61), (unsigned int)2166136261u ^ 0x61u);") + ", "
    + qq("The multiply result is defined modular 2^32; verify the xor step and that the multiply is well-defined for unsigned.") + "),"
)
new = (
    '("known FNV step", '
    + qq("CHECK_EQ(fnv1a_step(2166136261u, 0x61), 3826002220u);") + ", "
    + qq("xor 0x61 into the offset basis, then multiply by 16777619 — defined modular 2^32.") + "),"
)
assert old in src, "E1"
src = src.replace(old, new)

old = (
    '("wrap is deterministic", '
    + qq("unsigned int h = 4294967295u;@NL@h = fnv1a_step(h, 1);@NL@CHECK_EQ(h > 0, 1);") + ", "
    + qq("Wrapping produces a stable value — defined behavior, every run identical.") + "),"
)
new = (
    '("wrap is deterministic", '
    + qq("unsigned int h = 4294967295u;@NL@h = fnv1a_step(h, 1);@NL@CHECK_EQ(h, 4261412058u);") + ", "
    + qq("0xFFFFFFFF ^ 1 = 0xFFFFFFFE; times the prime mod 2^32 = 4261412058 — the same value every run, by definition.") + "),"
)
assert old in src, "E2"
src = src.replace(old, new)
print("E: FNV expectations exact full-round values")

# ------------------------------------------------ F: checkpoint ctx test
old = (
    '("ctx callback counting", '
    + qq("counter_t *c = counter_create();@NL@static int hits = 0;@NL@counter_visit(c, bump_ctx_probe, &hits);@NL@counter_visit(c, bump_ctx_probe, &hits);@NL@CHECK_EQ(counter_count(c), 2);@NL@CHECK_EQ(hits, 2);") + ", "
    + qq("fn runs once per visit and the counter tracks visits; the ctx pointer carries the caller's state.") + "),"
)
new = (
    '("ctx callback counting", '
    + qq("counter_t *c = counter_create();@NL@counter_visit(c, bump_ctx_probe, &hits);@NL@counter_visit(c, bump_ctx_probe, &hits);@NL@CHECK_EQ(counter_count(c), 2);@NL@CHECK_EQ(hits, 2);") + ", "
    + qq("fn runs once per visit; hits lives at file scope in your source and the ctx pointer carries it in.") + "),"
)
assert old in src, "F1"
src = src.replace(old, new)
print("F: checkpoint test no longer shadows hits")

open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print("AST OK — saved")
