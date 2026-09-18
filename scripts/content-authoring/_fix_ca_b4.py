#!/usr/bin/env python3
"""Repair batch-4 defects in ca_m7_8.py. Zero-backslash style."""
import ast

P = "ca_m7_8.py"
src = open(P, encoding="utf-8").read()
Q = chr(34)

def qq(s):
    return Q + s + Q

# ---- CSR: isolated-vertex expectations were transposed
old = (
    '("isolated vertex", '
    + qq("int e2[2][2] = {{0, 1}, {0, 2}};@NL@int off2[4];@NL@int adj2[2];@NL@csr_build(3, e2, 2, off2, adj2);@NL@CHECK_EQ(off2[1], 1);@NL@CHECK_EQ(off2[2], 2);@NL@CHECK_EQ(off2[3], 2);") + ", "
    + qq("Vertex 1 has no outgoing edges: offset[2] == offset[1+1].. the empty range encodes isolation.") + "),"
)
new = (
    '("isolated vertex", '
    + qq("int e2[2][2] = {{0, 1}, {0, 2}};@NL@int off2[4];@NL@int adj2[2];@NL@csr_build(3, e2, 2, off2, adj2);@NL@CHECK_EQ(off2[1], 2);@NL@CHECK_EQ(off2[2], 2);@NL@CHECK_EQ(off2[3], 2);") + ", "
    + qq("Both edges leave vertex 0: offset[1] is 2; vertex 1 has an empty range [offset[2], offset[2]) — isolation is an empty span.") + "),"
)
assert old in src, "csr isolated"
src = src.replace(old, new)

old_vi = '("đỉnh cô lập", "Đỉnh không có cạnh ra: offset trống mã hóa sự cô lập."),'
new_vi = '("đỉnh cô lập", "Cả hai cạnh rời đỉnh 0: offset[1] là 2; đỉnh 1 có khoảng rỗng — cô lập là span rỗng."),'
assert old_vi in src, "csr VI"
src = src.replace(old_vi, new_vi)

# ---- bytesort: rec_t has key/seq, not id
old = (
    "CHECK_EQ(r[0].id, 1);@NL@"
)
assert old in src, "bytesort member"
src = src.replace(old, "CHECK_EQ(r[0].seq, 11);@NL@")
print("bytesort test member fixed")

# ---- generic-dispatch: drop the overload (C has none); single to_int
i0 = src.index("solutions=[")
head, tail = src[:i0], src[i0:]

# prompt rewrite for the dispatch challenge
old_p = (
    "Then implement `long long to_int(value_t v)` using _Generic on a *literal* to prove compile-time selection: `to_int(5)` and `to_int(5.5)` must both compile against the same name."
)
new_p = (
    "Then implement `long long to_int(long long x)` (identity) — and note in the test "
    "that a _Generic macro selects the *type* of its argument at compile time, which is "
    "how C keeps type-safety at such doors without overloads."
)
assert old_p in src, "to_int prompt"
src = src.replace(old_p, new_p)

old_t = (
    '("_Generic picks at compile time", '
    + qq("CHECK_EQ(to_int(5), 5);@NL@CHECK_EQ(to_int(7), 7);") + ", "
    + qq("to_int(5) goes through the int arm (identity); the double arm would round-trip through truncation.") + "),"
)
new_t = (
    '("identity plus _Generic proof", '
    + qq("CHECK_EQ(to_int(5), 5);@NL@CHECK_STR_EQ(_Generic(5, int: \"int\", default: \"other\"), \"int\");") + ", "
    + qq("to_int is identity; the _Generic expression proves compile-time type selection by naming int's arm.") + "),"
)
assert old_t in src, "to_int test"
src = src.replace(old_t, new_t)
print("dispatch challenge reworded to single function + _Generic test")

# ---- hash-linear W: tombstones demoted to empty
sol_i = src.index("solutions=[")
head, tail = src[:sol_i], src[sol_i:]
old_w_tomb = (
    '"int ht_del(ht_ent_t *t, int key) {@NL@'
    '    int h = ht_hash(key);@NL@'
    '    for (int i = 0; i < HT_CAP; i++) {@NL@'
    '        int idx = (h + i) % HT_CAP;@NL@'
    '        if (t[idx].state == 0) return 0;@NL@'
    '        if (t[idx].state == 1 && t[idx].key == key) { t[idx].state = 0; return 1; }@NL@'
    '    }@NL@'
    '    return 0;@NL@}@NL@"'
)
new_w_tomb = (
    '"int ht_del(ht_ent_t *t, int key) {@NL@'
    '    int h = ht_hash(key);@NL@'
    '    for (int i = 0; i < HT_CAP; i++) {@NL@'
    '        int idx = (h + i) % HT_CAP;@NL@'
    '        if (t[idx].state == 1 && t[idx].key == key) { t[idx].state = 0; return 1; }@NL@'
    '    }@NL@'
    '    return 0;@NL@}@NL@"'
)
assert old_w_tomb in tail, "hash W del"
tail = tail.replace(old_w_tomb, new_w_tomb)
src = head + tail
print("hash W: delete empties the slot (no tombstone) — deterministic defect")

# ---- union-find W: union attaches blindly (a under b), breaking rank + root test
sol_i = src.index("solutions=[")
head, tail = src[:sol_i], src[sol_i:]
old_uf = (
    '"void uf_union(int *parent, int *rank_, int a, int b) {@NL@'
    '    int ra = uf_find(parent, a);@NL@'
    '    int rb = uf_find(parent, b);@NL@'
    '    if (ra == rb) return;@NL@'
    '    parent[rb] = ra;@NL@'
    '    (void)rank_;@NL@}@NL@"'
)
new_uf = (
    '"void uf_union(int *parent, int *rank_, int a, int b) {@NL@'
    '    (void)rank_;@NL@'
    '    parent[a] = b;@NL@}@NL@"'
)
assert old_uf in tail, "uf W union"
tail = tail.replace(old_uf, new_uf)
src = head + tail
print("union-find W: blind union(a under b) — deterministic defect")

open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print("AST OK — saved")
