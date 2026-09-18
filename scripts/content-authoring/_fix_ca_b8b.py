#!/usr/bin/env python3
"""Repair batch-8 REF failures in ca_m15_16.py. Zero typed backslashes.

1. heap-invariant boundary test: localize the single-node array.
2. bounds-discipline tests 2-3: localize a/v.
3. ownership-ledger test 2: localize x.
4. bisect-diagnosis test 3: replace the contradictory first-stage case with a
   flip-vs-value-change discriminator consistent with the R implementation.
5. shrink-repro: add the one-element-floor guard to R; align hints + VI.
Verifies with ast.parse before writing.
"""
import ast

P = "ca_m15_16.py"
src = open(P, encoding="utf-8").read()
orig = src


def rep(s, old, new, what):
    n = s.count(old)
    assert n == 1, "not unique or missing: " + what + " (count=" + str(n) + ")"
    print("fixed:", what)
    return s.replace(old, new)


# 1. heap-invariant: boundary test must not use test-1's `good`
src = rep(
    src,
    '("boundary cases", "CHECK(heap_ok(NULL, 0));@NL@CHECK(heap_ok(good, 1));", '
    '"Empty and single-node heaps are trivially valid; NULL with n>0 is not a heap."),',
    '("boundary cases", "int good2[1] = {5};@NL@CHECK(heap_ok(NULL, 0));@NL@CHECK(heap_ok(good2, 1));", '
    '"Empty and single-node heaps are trivially valid; NULL with n>0 is not a heap."),',
    "heap-invariant boundary test",
)

# 2a. bounds-discipline: out-of-range test localizes its own array/value
src = rep(
    src,
    '("out-of-range refused", "CHECK_EQ(checked_get(a, 3, 3, &v), -1);@NL@CHECK_EQ(v, 6);", '
    '"Index n is one-past-the-end: refused, and out is untouched on failure."),',
    '("out-of-range refused", "int a2[3] = {5, 6, 7};@NL@int v2 = 6;@NL@'
    'CHECK_EQ(checked_get(a2, 3, 3, &v2), -1);@NL@CHECK_EQ(v2, 6);", '
    '"Index n is one-past-the-end: refused, and out is untouched on failure (v2 still 6)."),',
    "bounds-discipline out-of-range test",
)

# 2b. bounds-discipline: NULL-array test localizes v
src = rep(
    src,
    '("NULL array", "CHECK_EQ(checked_get(NULL, 2, 0, &v), -1);@NL@CHECK_EQ(checked_sum(NULL, 2), 0);", '
    '"NULL with nonzero n is refused per element; the sum degrades to 0."),',
    '("NULL array", "int v3 = 0;@NL@CHECK_EQ(checked_get(NULL, 2, 0, &v3), -1);@NL@CHECK_EQ(checked_sum(NULL, 2), 0);", '
    '"NULL with nonzero n is refused per element; the sum degrades to 0."),',
    "bounds-discipline NULL-array test",
)

# 3. ownership-ledger: released-entries test localizes its variable
src = rep(
    src,
    '("released entries do not leak", "own(&x);@NL@release(&x);@NL@CHECK_EQ(audit(), 0);", '
    '"Marking freed before audit yields zero leaks."),',
    '("released entries do not leak", "int y = 1;@NL@own(&y);@NL@release(&y);@NL@CHECK_EQ(audit(), 0);", '
    '"Marking freed before audit yields zero leaks."),',
    "ownership-ledger released test",
)

# 4a. bisect-diagnosis: replace the contradictory first-stage test
src = rep(
    src,
    '("first stage broken", "int in3[3] = {-5, -5, -5};@NL@CHECK_EQ((int)find_bad_stage(in3, 3), 0);", '
    '"A flip at index 0 implicates the earliest stage — bisecting finds it in one probe."),',
    '("localizes the flip, not the value change", "int in3[3] = {5, 3, -7};@NL@CHECK_EQ((int)find_bad_stage(in3, 3), 2);", '
    '"The value changed at index 1 without a sign flip — not the corruption; '
    'the sign first differs from injections[0] at index 2."),',
    "bisect-diagnosis third test",
)

# 4b. bisect-diagnosis: align the VI hint with the new case
src = rep(
    src,
    '("stage đầu lỗi", "Lật tại index 0 quy kết stage sớm nhất."),',
    '("định vị lật dấu", "Giá trị đổi ở index 1 nhưng không lật dấu — không phải hủy hoại; '
    'dấu khác injections[0] lần đầu tại index 2."),',
    "bisect-diagnosis VI hint",
)

# 5a. shrink-repro: description gains the one-element floor
src = rep(
    src,
    "Simple greedy: try removing each kept element from the highest index down; "
    'keep the removal if it still fails.",',
    "Simple greedy: try removing each kept element from the highest index down; "
    "keep the removal if it still fails. Never reduce below a single element — "
    'a repro must still exercise the failure.",',
    "shrink-repro description",
)

# 5b. shrink-repro: VI description gains the floor
src = rep(
    src,
    '"Cài shrink: thử bỏ từng phần tử được giữ từ chỉ số cao xuống; giữ phép bỏ nếu vẫn còn lỗi.",',
    '"Cài shrink: thử bỏ từng phần tử được giữ từ chỉ số cao xuống; giữ phép bỏ nếu vẫn còn lỗi. '
    'Không giảm dưới một phần tử — repro vẫn phải còn lỗi.",',
    "shrink-repro VI description",
)

# 5c. shrink-repro: EN hint now explains the survivor
src = rep(
    src,
    '"pred_all_fail always returns true, so one element suffices — the highest-index survivor."',
    '"pred_all_fail always returns true, so deletion proceeds until a single element '
    'remains — a repro keeps one; the lowest bit survives, value 1."',
    "shrink-repro EN hint",
)

# 5d. shrink-repro: VI hint aligns
src = rep(
    src,
    '("thu về tập tối tiểu", "pred_all_fail luôn true nên một phần tử đủ — survivor chỉ số cao nhất."),',
    '("thu về tập tối tiểu", "pred_all_fail luôn true nên phép xóa chạy đến khi còn đúng một phần tử '
    '— repro phải giữ lại một; bit thấp nhất còn lại, giá trị 1."),',
    "shrink-repro VI hint",
)

# 5e. shrink-repro: R gains the single-bit guard (W's loop has no `trial` line,
#     so this anchor matches only the reference)
src = rep(
    src,
    "for (size_t i = width; i-- > 0;) {@NL@        unsigned int bit = 1u << i;@NL@"
    "        if (cur & bit) {@NL@            unsigned int trial",
    "for (size_t i = width; i-- > 0;) {@NL@        if ((cur & (cur - 1)) == 0) break;@NL@"
    "        unsigned int bit = 1u << i;@NL@        if (cur & bit) {@NL@            unsigned int trial",
    "shrink-repro reference guard",
)

assert src != orig
ast.parse(src)
open(P, "w", encoding="utf-8").write(src)
print("patched", P)
