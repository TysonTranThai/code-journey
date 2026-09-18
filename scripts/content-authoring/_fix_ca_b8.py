#!/usr/bin/env python3
"""Fix batch-8 checkpoint defects in ca_m15_16.py.
1. CHECK(diagnose(&r), "ok") -> CHECK_STR_EQ (CHECK takes one arg).
2. W returns size-corrupt before index-corrupt: add a both-corrupt case
   (head=9 AND count=9) where R says index-corrupt, W says size-corrupt.
3. Exercise ring_size_ok/ring_count_matches so the W's broken versions fail.
Idempotent. Zero typed backslashes."""
import ast

P = "ca_m15_16.py"
src = open(P, encoding="utf-8").read()
orig = src
BS2 = chr(92)  # backslash: the batch stores test strings with escaped quotes

# 1. CHECK misuse (the file stores these as Python source with escaped quotes)
old1 = 'CHECK(diagnose(&r), ' + BS2 + '"' + 'ok' + BS2 + '"' + ');'
new1 = 'CHECK_STR_EQ(diagnose(&r), ' + BS2 + '"' + 'ok' + BS2 + '"' + ');'
if old1 in src:
    src = src.replace(old1, new1)
    print('CHECK misuse fixed')
else:
    print('CHECK misuse already fixed')

# 2 + 3. extend checkpoint tests (escaped quotes via BS2)
Q2 = BS2 + '"'
old2 = (
    '("size corruption", "struct ring r3 = {{0}, 2, 3, 9};@NL@CHECK_STR_EQ(diagnose(&r3), ' + Q2 + 'size-corrupt' + Q2 + ');", '
    '"count 9 exceeds capacity 8 with valid indices — size verdict."),'
)
new2 = (
    '("size corruption", "struct ring r3 = {{0}, 2, 3, 9};@NL@CHECK_STR_EQ(diagnose(&r3), ' + Q2 + 'size-corrupt' + Q2 + ');", '
    '"count 9 exceeds capacity 8 with valid indices — size verdict."),\n'
    '            ("both corrupt: index wins", "struct ring r4 = {{0}, 9, 0, 9};@NL@CHECK_STR_EQ(diagnose(&r4), ' + Q2 + 'index-corrupt' + Q2 + ');@NL@CHECK(!ring_size_ok(&r4));@NL@CHECK(!ring_count_matches(&r4, 0));", '
    '"head 9 breaks indices AND count 9 breaks size — index is diagnosed first, and both boolean verdicts reject."),'
)
assert old2 in src, "size-corruption test not found"
src = src.replace(old2, new2)
print("both-corrupt discriminator added")

ast.parse(src)
BS = chr(92)
assert BS + "NL@" not in src and BS + "CE@" not in src
if src != orig:
    open(P, "w", encoding="utf-8").write(src)
    print("WROTE", P)
else:
    print("no changes (already applied)")
