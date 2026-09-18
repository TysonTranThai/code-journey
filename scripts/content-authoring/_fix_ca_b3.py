#!/usr/bin/env python3
"""Repair batch-3 (module 5) test defects in ca_m5_6.py: tests are separate
programs and must not share locals across tests. Zero-backslash style."""
import ast

P = "ca_m5_6.py"
src = open(P, encoding="utf-8").read()
Q = chr(34)
NL = "@NL@"

def qq(s):
    return Q + s + Q

# ---- arena: exhaustion + reset tests rebuild their own state
old = (
    '("exhaustion is NULL", '
    + qq("CHECK_NULL(arena_alloc(&a, 16));") + ", "
    + qq("56 of 64 bytes are used; 16 more do not fit — return NULL, never overrun.") + "),"
)
new = (
    '("exhaustion is NULL", '
    + qq("unsigned char buf[64];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc(&a, 56);@NL@CHECK_NULL(arena_alloc(&a, 16));") + ", "
    + qq("56 of 64 bytes used; 16 more do not fit — return NULL, never overrun.") + "),"
)
assert old in src, "arena exhaustion"
src = src.replace(old, new)

old = (
    '("reset rewinds", '
    + qq("arena_reset(&a);@NL@CHECK_NOT_NULL(arena_alloc(&a, 64));") + ", "
    + qq("After reset the full capacity is available again in one slice.") + "),"
)
new = (
    '("reset rewinds", '
    + qq("unsigned char buf[64];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc(&a, 32);@NL@arena_reset(&a);@NL@CHECK_NOT_NULL(arena_alloc(&a, 64));") + ", "
    + qq("After reset the full capacity is available again in one slice.") + "),"
)
assert old in src, "arena reset"
src = src.replace(old, new)

# ---- pool: LIFO test rebuilds its own pool
old = (
    '("LIFO reuse", '
    + qq("pool_put(p, b1);@NL@void *b3 = pool_get(p);@NL@CHECK_EQ((int)(b3 == b1), 1);") + ", "
    + qq("A returned block goes to the head of the free list and is handed out first.") + "),"
)
new = (
    '("LIFO reuse", '
    + qq("pool_t *p = pool_create(2, 16);@NL@void *b1 = pool_get(p);@NL@pool_put(p, b1);@NL@void *b3 = pool_get(p);@NL@CHECK_EQ((int)(b3 == b1), 1);") + ", "
    + qq("A returned block goes to the head of the free list and is handed out first.") + "),"
)
assert old in src, "pool LIFO"
src = src.replace(old, new)

# ---- align-up: uintptr needs stdint.h (fix ledger R and W), W loses dead stmt
i0 = src.index("solutions=[")
head, tail = src[:i0], src[i0:]

old_r = (
    '"unsigned char *align_up(unsigned char *p, size_t align) {@NL@'
    '    size_t off = (size_t)((p - (unsigned char *)0) & 0); (void)off;@NL@'
    '    uintptr_t u = (uintptr_t)p;@NL@'
    '    uintptr_t m = align - 1;@NL@'
    '    return (unsigned char *)((u + m) & ~m);@NL@}@NL@"'
)
new_r = (
    '"#include <stdint.h>@NL@"'
    + '"unsigned char *align_up(unsigned char *p, size_t align) {@NL@'
    '    uintptr_t u = (uintptr_t)p;@NL@'
    '    uintptr_t m = align - 1;@NL@'
    '    return (unsigned char *)((u + m) & ~m);@NL@}@NL@"'
)
assert old_r in tail, "align R ledger"
tail = tail.replace(old_r, new_r)

old_w = (
    '"unsigned char *align_up(unsigned char *p, size_t align) {@NL@'
    '    uintptr_t u = (uintptr_t)p;@NL@'
    '    return (unsigned char *)(u + align);@NL@}@NL@"'
)
new_w = (
    '"#include <stdint.h>@NL@"'
    + '"unsigned char *align_up(unsigned char *p, size_t align) {@NL@'
    '    uintptr_t u = (uintptr_t)p;@NL@'
    '    return (unsigned char *)(u + align);@NL@}@NL@"'
)
assert old_w in tail, "align W ledger"
tail = tail.replace(old_w, new_w)
src = head + tail
print("align_up ledger: stdint include added, dead stmt dropped")

# ---- checkpoint: exhaustion/used/reset tests rebuild their own state
old = (
    '("used counts padding", '
    + qq("CHECK_EQ((long long)arena_used(&a), 9);") + ", "
    + qq("used is the next free offset: 1 byte at offset 8 means 9 total.") + "),"
)
new = (
    '("used counts padding", '
    + qq("unsigned char buf[128];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc_aligned(&a, 3, 8);@NL@arena_alloc_aligned(&a, 1, 8);@NL@CHECK_EQ((long long)arena_used(&a), 9);") + ", "
    + qq("used is the next free offset: 1 byte at offset 8 means 9 total.") + "),"
)
assert old in src, "cp used"
src = src.replace(old, new)

old = (
    '("exhaustion respects align", '
    + qq("CHECK_NULL(arena_alloc_aligned(&a, 200, 8));") + ", "
    + qq("A request larger than the whole buffer must fail even when the offset is aligned.") + "),"
)
new = (
    '("exhaustion respects align", '
    + qq("unsigned char buf[128];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@CHECK_NULL(arena_alloc_aligned(&a, 200, 8));") + ", "
    + qq("A request larger than the whole buffer must fail even when the offset is aligned.") + "),"
)
assert old in src, "cp exhaustion"
src = src.replace(old, new)

old = (
    '("reset rewinds", '
    + qq("arena_reset(&a);@NL@CHECK_EQ((long long)arena_used(&a), 0);@NL@CHECK_NOT_NULL(arena_alloc_aligned(&a, 128, 16));") + ", "
    + qq("After reset the entire buffer serves one maximally aligned slice.") + "),"
)
new = (
    '("reset rewinds", '
    + qq("unsigned char buf[128];@NL@arena_t a;@NL@arena_init(&a, buf, sizeof buf);@NL@arena_alloc_aligned(&a, 40, 8);@NL@arena_reset(&a);@NL@CHECK_EQ((long long)arena_used(&a), 0);@NL@CHECK_NOT_NULL(arena_alloc_aligned(&a, 128, 16));") + ", "
    + qq("After reset the entire buffer serves one maximally aligned slice.") + "),"
)
assert old in src, "cp reset"
src = src.replace(old, new)

open(P, "w", encoding="utf-8").write(src)
ast.parse(src)
print("AST OK — saved")
