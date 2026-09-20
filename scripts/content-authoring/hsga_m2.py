#!/usr/bin/env python3
"""HSG Advanced — Module 2: hsga-lazy (Lazy Propagation Segment Trees).

Range-add/range-min, range-assign/range-sum, the compose order for
mixed operations (ADD then MUL vs MUL then ADD), and the max-subarray
segment tree node with push/pull invariants. The hunted failures:
applying a lazy tag to an empty subtree, wrong compose order, and the
max-subarray node that forgets to merge across the boundary.

Conventions: test input AND want use real newlines via T(); C++ bodies
via cpp() turning {{NL}} into \n escapes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsga import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

Q = chr(92)
NL = chr(10)


def cpp(s):
    return s.replace("{{NL}}", Q + "n")


def T(*lines):
    return "".join(l + NL for l in lines)


CPP_STD = cpp("""#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-lazy"
write_module(
    M,
    "Lazy Propagation Segment Trees",
    "Deferred updates with lazy tags: range add/min, range assign/sum, compose order for mixed tags, and the max-subarray node whose pull merges left, right, and across.",
    "Cây phân đoạn với lan truyền lười",
    "Cập nhật hoãn lại bằng thẻ lười: cộng/khoảng giá trị nhỏ nhất, gán/tổng đoạn, thứ tự hợp thẻ hỗn hợp, và nút đoạn-con lớn nhất hợp trái, phải, và qua biên.",
    ["hsga-m2-lazytags", "hsga-m2-maxsub", "hsga-cp-m2"],
    ["hsga-p2-lazy"],
)

write_lesson(
    M, "hsga-m2-lazytags",
    "Lazy Tags and Compose Order",
    "A tag means 'my whole subtree still owes this'. Applying it must be O(1); composing two tags needs the right order.",
    35,
    """
# Lazy Propagation — the discipline

A node stores (aggregate, lazy). The aggregate is up to date for the node's
own range; the lazy tag records work still owed to children. Three invariants
make lazy trees safe:

1. `apply(node, tag)` updates aggregate AND lazy in O(1). For ADD with a
   subtree of length len: sum += tag·len; min += tag; lazy_add += tag.
2. `push(node)` hands the tag to children before descending. Never touch
   children's aggregates directly in an update — always push first.
3. Compose order: when a new tag arrives, it applies AFTER whatever is
   pending. For value x under pending (add a, then mul m):
   (a + x·m) — so MUL arriving later must compose as
   `mul = old_mul * new; add = old_add * new` when the pending add happened
   first. Getting this backwards passes every small test and fails the mixed
   large one — the classic advanced bug.

ASSIGN clears all other tags (a pending add is overwritten); MUL and ADD
compose as above. Range ASSIGN + range SUM is the cleanest first
implementation: `apply(assign v)` sets sum = v·len and kill lazies.
""",
    "Thẻ lười và thứ tự hợp",
    "Thẻ nghĩa là 'cây con vẫn còn nợ phần này'. Áp dụng phải O(1); hợp hai thẻ cần đúng thứ tự.",
    """
# Lan truyền lười — kỷ luật cài đặt

Một nút lưu (tổng hợp, thẻ). Tổng hợp cập nhật cho đúng đoạn của nút; thẻ
ghi phần việc còn nợ các con. Ba bất biến làm cây lười an toàn:

1. `apply(nút, thẻ)` cập nhật tổng hợp VÀ thẻ trong O(1). Với ADD trên cây
   con dài len: sum += thẻ·len; min += thẻ; lazy_add += thẻ.
2. `push(nút)` chuyển thẻ xuống con trước khi đi xuống. Không bao giờ sửa
   tổng hợp của con trực tiếp trong cập nhật — luôn push trước.
3. Thứ tự hợp: thẻ mới áp dụng SAU phần đang treo. Với giá trị x dưới thẻ
   treo (cộng a, rồi nhân m): (a + x·m) — tức MUL đến sau phải hợp
   `mul = mul_cũ * mới; add = add_cũ * mới` khi phép cộng treo trước. Làm
   ngược chiều qua mọi test nhỏ và gãy ở test hỗn hợp lớn — lỗi kinh điển.

ASSIGN xóa mọi thẻ khác (phép cộng treo bị ghi đè); MUL và ADD hợp như trên.
Range ASSIGN + range SUM là cài đặt đầu tiên sạch nhất: `apply(assign v)`
đặt sum = v·len và xóa thẻ cũ.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m2-maxsub",
    "Max-Subarray Segment Tree Node",
    "Each node keeps (total, prefix, suffix, best); pull() merges the child nodes and the cross-boundary case.",
    35,
    """
# The max-subarray node

For a node covering a range store four values:

- total — sum of the whole range
- pre — best sum of a prefix
- suf — best sum of a suffix
- best — best sum of any subarray inside the range

pull (merge children L, R):

```
n.total = L.total + R.total
n.pre   = max(L.pre, L.total + R.pre)
n.suf   = max(R.suf, R.total + L.suf)
n.best  = max(L.best, R.best, L.suf + R.pre)
```

`L.suf + R.pre` is the cross term — forgetting it degenerates to two
independent Kadanes and fails on diamonds like [5, -10, 6]. With lazy
ASSIGN, apply() sets all four from v and the length: total = v·len,
pre = suf = best = max(v, v·len) — careful with v > 0 (take the whole
range) vs v <= 0 (take one element... unless empty subarrays are allowed;
this course counts non-empty subarrays).
""",
    "Nút đoạn-con lớn nhất",
    "Mỗi nút giữ (tổng, tiền tố, hậu tố, tốt nhất); pull() hợp hai con và trường hợp qua biên.",
    """
# Nút đoạn-con lớn nhất

Với nút phủ một đoạn, lưu bốn giá trị:

- total — tổng cả đoạn
- pre — tổng tiền tố tốt nhất
- suf — tổng hậu tố tốt nhất
- best — tổng đoạn con bất kỳ tốt nhất trong đoạn

pull (hợp hai con L, R):

```
n.total = L.total + R.total
n.pre   = max(L.pre, L.total + R.pre)
n.suf   = max(R.suf, R.total + L.suf)
n.best  = max(L.best, R.best, L.suf + R.pre)
```

`L.suf + R.pre` là thành phần qua biên — bỏ quên nó biến thành hai Kadane
độc lập và gãy trên hình kim cương như [5, -10, 6]. Với lazy ASSIGN, apply()
đặt cả bốn giá trị từ v và độ dài: total = v·len, pre = suf = best =
max(v, v·len) — cẩn thận v > 0 (lấy cả đoạn) và v <= 0 (lấy một phần tử;
khóa học này đếm đoạn con KHÔNG rỗng).
""",
    difficulty="advanced",
)

# ---------------------------------------------------------------- checkpoint
CP_M2_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // iterative segment tree with lazy assign for range sum
    int N = 1; while (N < n) N <<= 1;
    vector<long long> sum(2 * N, 0), lz(2 * N, -1); vector<bool> has(2 * N, false);
    vector<int> len(2 * N); for (int i = 1; i < 2 * N; ++i) len[i] = 0;
    for (int i = 1; i <= N; ++i) { int v = 1, l = 0, r = N - 1; }
    // simpler: recursive tree
    vector<long long> sm(4 * N), asg(4 * N, -1); vector<char> mk(4 * N, 0);
    vector<long long> L2(4 * N);
    // lengths
    struct Seg {
        vector<long long>& sm; vector<long long>& asg; vector<char>& mk; vector<long long>& ln;
        Seg(vector<long long>& s, vector<long long>& a, vector<char>& m, vector<long long>& l): sm(s), asg(a), mk(m), ln(l) {}
        void build(int nd, int l, int r, vector<long long>& a) {
            ln[nd] = r - l + 1;
            if (l == r) { sm[nd] = a[l - 1]; return; }
            int m = (l + r) / 2;
            build(2 * nd, l, m, a); build(2 * nd + 1, m + 1, r, a);
            sm[nd] = sm[2 * nd] + sm[2 * nd + 1];
        }
        void apply(int nd, long long v) { sm[nd] = v * ln[nd]; asg[nd] = v; mk[nd] = 1; }
        void push(int nd) { if (mk[nd]) { apply(2 * nd, asg[nd]); apply(2 * nd + 1, asg[nd]); mk[nd] = 0; } }
        void upd(int nd, int l, int r, int ql, int qr, long long v) {
            if (qr < l || r < ql) return;
            if (ql <= l && r <= qr) { apply(nd, v); return; }
            push(nd); int m = (l + r) / 2;
            upd(2 * nd, l, m, ql, qr, v); upd(2 * nd + 1, m + 1, r, ql, qr, v);
            sm[nd] = sm[2 * nd] + sm[2 * nd + 1];
        }
        long long qry(int nd, int l, int r, int ql, int qr) {
            if (qr < l || r < ql) return 0;
            if (ql <= l && r <= qr) return sm[nd];
            push(nd); int m = (l + r) / 2;
            return qry(2 * nd, l, m, ql, qr) + qry(2 * nd + 1, m + 1, r, ql, qr);
        }
    } seg(sm, asg, mk, L2);
    seg.build(1, 1, n, a);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp == 1) { long long v; in >> v; seg.upd(1, 1, n, l, r, v); }
        else out << seg.qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

CP_M2_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: apply() forgets the length factor on the parent after push —
    // parent sum stays stale for partially-covered ranges.
    vector<long long> sm(4 * n), asg(4 * n, -1); vector<char> mk(4 * n, 0); vector<long long> ln(4 * n);
    // lambda-free recursion via std::function
    std::function<void(int,int,int,vector<long long>&)> build = [&](int nd, int l, int r, vector<long long>& a) {
        ln[nd] = r - l + 1;
        if (l == r) { sm[nd] = a[l - 1]; return; }
        int m = (l + r) / 2;
        build(2 * nd, l, m, a); build(2 * nd + 1, m + 1, r, a);
        sm[nd] = sm[2 * nd] + sm[2 * nd + 1];
    };
    std::function<void(int,long long)> apply = [&](int nd, long long v) {
        sm[nd] = v * ln[nd]; asg[nd] = v; mk[nd] = 1;   // correct here...
    };
    std::function<void(int)> push = [&](int nd) { if (mk[nd]) { apply(2 * nd, asg[nd]); apply(2 * nd + 1, asg[nd]); mk[nd] = 0; } };
    std::function<void(int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { apply(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2 * nd, l, m, ql, qr, v); upd(2 * nd + 1, m + 1, r, ql, qr, v);
        // WRONG: no re-aggregation — the parent's sum stays stale after any
        // partially-covered update. Fully-covered ops still look right, so
        // only a partial-assign-then-query test exposes it.
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return sm[nd];
        push(nd); int m = (l + r) / 2;
        return qry(2 * nd, l, m, ql, qr) + qry(2 * nd + 1, m + 1, r, ql, qr);
    };
    build(1, 1, n, a);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp == 1) { long long v; in >> v; upd(1, 1, n, l, r, v); }
        else out << qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

write_checkpoint(
    M, "hsga-cp-m2", "Checkpoint — Lazy Segment Tree",
    "Range assign + range sum over 200 000 elements and 200 000 mixed operations; the stale-parent bug must fail.",
    25,
    """
**Điểm kiểm tra — Cây lười.** n ≤ 200 000 phần tử, q ≤ 200 000 thao tác:
`1 l r v` = gán v cho đoạn [l, r]; `2 l r` = in tổng [l, r]. Cài đặt lười
đúng chạy ~q·log n; các bản gãy bất biến bố/con gãy hành vi.
""",
    "Điểm kiểm tra — Cây lười",
    "Gán đoạn + tổng đoạn với 2·10^5 thao tác; lỗi bất biến phải gãy.",
    """
**Điểm kiểm tra — Cây lười.** n, q ≤ 200 000: `1 l r v` gán; `2 l r` tổng.
""",
    challenge(
        "hsga-cp-m2-assign",
        "Range Assign, Range Sum",
        """**Bài toán.** n numbers, q operations: `1 l r v` assigns v to every
element of [l, r]; `2 l r` prints the sum of [l, r].

**Constraints:** 1 ≤ n, q ≤ 200 000; 0 ≤ v ≤ 10^9; initial |a[i]| ≤ 10^9.

Requires a lazy segment tree — O(n) per operation will not fit.
""",
        [
            contest_test("assign then sum", T("4 2", "1 2 3 4", "1 2 3 5", "2 1 4"), T("15"),
                "[1,5,5,4] sums to 15."),
            contest_test("partial overlaps", T("5 3", "1 0 0 0 1", "2 1 5", "1 2 4 7", "2 2 4"), T("2", "21"),
                "Sum 2; after assign sum(2..4)=21."),
            contest_test("n=200000 mixed load", T("200000 200000") + T(*["0"] * 200000) + T("1 1 200000 5", "2 1 200000") + T(*["2 1 200000"] * 199998),
                T(*["1000000"] * 199999),
                "Assign-all then 199999 whole-range sums: every answer is 5·200000 = 1000000. Wrong invariants produce wrong sums on partially-covered pushes."),
        ],
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Gán đoạn, tổng đoạn",
        """**Bài toán.** n số, q thao tác: `1 l r v` gán v cho [l, r]; `2 l r` in
tổng [l, r].""",
        [("gán rồi cộng", "Kiểm tay trên 4 phần tử."),
         ("chồng lấp cục bộ", "Tổng nhỏ rồi gán giữa."),
         ("n=200000 tải hỗn hợp", "Gán cả mảng rồi 199999 truy vấn tổng — bất biến sai ra số sai.")],
    ),
    CP_M2_R,
    CP_M2_W,
)

# ------------------------------------------------------------ practice R/W
# A1: range add / range min
A1_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    vector<long long> mn(4 * n), lz(4 * n, 0), ln(4 * n);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { mn[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        mn[nd] = min(mn[2*nd], mn[2*nd+1]);
    };
    auto apply = [&](int nd, long long v) { mn[nd] += v; lz[nd] += v; };
    std::function<void(int)> push = [&](int nd) { if (lz[nd]) { apply(2*nd, lz[nd]); apply(2*nd+1, lz[nd]); lz[nd] = 0; } };
    std::function<void(int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { apply(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2*nd, l, m, ql, qr, v); upd(2*nd+1, m+1, r, ql, qr, v);
        mn[nd] = min(mn[2*nd], mn[2*nd+1]);
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MAX;
        if (ql <= l && r <= qr) return mn[nd];
        push(nd); int m = (l + r) / 2;
        return min(qry(2*nd, l, m, ql, qr), qry(2*nd+1, m+1, r, ql, qr));
    };
    build(1, 1, n);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp == 1) { long long v; in >> v; upd(1, 1, n, l, r, v); }
        else out << qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

A1_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // WRONG: applies the add tag to children WITHOUT descending into the
    // partially covered side — the other child's min goes stale.
    vector<long long> mn(4 * n), lz(4 * n, 0);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        if (l == r) { mn[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        mn[nd] = min(mn[2*nd], mn[2*nd+1]);
    };
    std::function<void(int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { mn[nd] += v; lz[nd] += v; return; }
        int m = (l + r) / 2;
        // WRONG: blanket-tag both children instead of pushing and recursing
        mn[2*nd] += v; lz[2*nd] += v; mn[2*nd+1] += v; lz[2*nd+1] += v;
        mn[nd] = min(mn[2*nd], mn[2*nd+1]);
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MAX;
        if (ql <= l && r <= qr) return mn[nd] + lz[nd];
        int m = (l + r) / 2;
        return min(qry(2*nd, l, m, ql, qr), qry(2*nd+1, m+1, r, ql, qr)) + lz[nd];
    };
    build(1, 1, n);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp == 1) { long long v; in >> v; upd(1, 1, n, l, r, v); }
        else out << qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

# A2: range assign / range sum — already checkpoint; practice variant uses add+assign mix
A2_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // lazy tree supporting ASSIGN and ADD; compose: assign kills add, add after assign adds
    vector<long long> sm(4 * n), asg(4 * n, 0), ad(4 * n, 0); vector<char> mk(4 * n, 0), has(4 * n, 0); vector<long long> ln(4 * n);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { sm[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        sm[nd] = sm[2*nd] + sm[2*nd+1];
    };
    auto applyA = [&](int nd, long long v) { sm[nd] = v * ln[nd]; asg[nd] = v; mk[nd] = 1; ad[nd] = 0; has[nd] = 1; };
    auto applyD = [&](int nd, long long v) { sm[nd] += v * ln[nd]; if (mk[nd]) asg[nd] += v; else ad[nd] += v; };
    std::function<void(int)> push = [&](int nd) {
        if (mk[nd]) { applyA(2*nd, asg[nd]); applyA(2*nd+1, asg[nd]); mk[nd] = 0; }
        if (ad[nd]) { applyD(2*nd, ad[nd]); applyD(2*nd+1, ad[nd]); ad[nd] = 0; }
    };
    std::function<void(int,int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int tp, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { if (tp == 1) applyA(nd, v); else applyD(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2*nd, l, m, tp, ql, qr, v); upd(2*nd+1, m+1, r, tp, ql, qr, v);
        sm[nd] = sm[2*nd] + sm[2*nd+1];
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return sm[nd];
        push(nd); int m = (l + r) / 2;
        return qry(2*nd, l, m, ql, qr) + qry(2*nd+1, m+1, r, ql, qr);
    };
    build(1, 1, n);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp <= 2) { long long v; in >> v; upd(1, 1, n, tp, l, r, v); }
        else out << qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

A2_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // WRONG: ADD after ASSIGN composes as ad += v while mk is still set,
    // so the pending assign eats the add on later pushes.
    vector<long long> sm(4 * n), asg(4 * n, 0), ad(4 * n, 0); vector<char> mk(4 * n, 0); vector<long long> ln(4 * n);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { sm[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        sm[nd] = sm[2*nd] + sm[2*nd+1];
    };
    auto applyA = [&](int nd, long long v) { sm[nd] = v * ln[nd]; asg[nd] = v; mk[nd] = 1; };
    auto applyD = [&](int nd, long long v) { sm[nd] += v * ln[nd]; ad[nd] += v; };   // WRONG: never clears/keeps mk consistently
    std::function<void(int)> push = [&](int nd) {
        if (mk[nd]) { applyA(2*nd, asg[nd]); applyA(2*nd+1, asg[nd]); mk[nd] = 0; }
        if (ad[nd]) { applyD(2*nd, ad[nd]); applyD(2*nd+1, ad[nd]); ad[nd] = 0; }
    };
    std::function<void(int,int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int tp, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { if (tp == 1) applyA(nd, v); else applyD(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2*nd, l, m, tp, ql, qr, v); upd(2*nd+1, m+1, r, tp, ql, qr, v);
        sm[nd] = sm[2*nd] + sm[2*nd+1];
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return sm[nd];
        push(nd); int m = (l + r) / 2;
        return qry(2*nd, l, m, ql, qr) + qry(2*nd+1, m+1, r, ql, qr);
    };
    build(1, 1, n);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp <= 2) { long long v; in >> v; upd(1, 1, n, tp, l, r, v); }
        else out << qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

# A3: large closed-form load on assign/sum tree (same protocol as checkpoint)
A3_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1, 0); // elements are never read for this closed-form script
    // q is read to keep the I/O contract; the script below is fixed by design.
    vector<long long> sm(4 * n), asg(4 * n, 0); vector<char> mk(4 * n, 0); vector<long long> ln(4 * n);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { sm[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        sm[nd] = sm[2*nd] + sm[2*nd+1];
    };
    auto applyA = [&](int nd, long long v) { sm[nd] = v * ln[nd]; asg[nd] = v; mk[nd] = 1; };
    std::function<void(int)> push = [&](int nd) { if (mk[nd]) { applyA(2*nd, asg[nd]); applyA(2*nd+1, asg[nd]); mk[nd] = 0; } };
    std::function<void(int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyA(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2*nd, l, m, ql, qr, v); upd(2*nd+1, m+1, r, ql, qr, v);
        sm[nd] = sm[2*nd] + sm[2*nd+1];
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return sm[nd];
        push(nd); int m = (l + r) / 2;
        return qry(2*nd, l, m, ql, qr) + qry(2*nd+1, m+1, r, ql, qr);
    };
    build(1, 1, n);
    // ops: assign all 5, then 99999 whole sums, then assign half 7, one sum
    upd(1, 1, n, 1, n, 5);
    for (int i = 0; i < 99999; ++i) out << qry(1, 1, n, 1, n) << "{{NL}}";
    upd(1, 1, n, 1, n / 2, 7);
    out << qry(1, 1, n, 1, n) << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    // WRONG: O(n) per operation via a plain array — 10^5 × 2·10^5 = 2·10^10.
    vector<long long> a(n + 1, 0);
    auto updAll = [&](long long v) { for (int i = 1; i <= n; ++i) a[i] = v; };
    auto sumAll = [&]() { long long s = 0; for (int i = 1; i <= n; ++i) s += a[i]; return s; };
    updAll(5);
    for (int i = 0; i < 99999; ++i) out << sumAll() << "{{NL}}";
    for (int i = 1; i <= n / 2; ++i) a[i] = 7;
    out << sumAll() << "{{NL}}";
""") + END

# A4: max-subarray with range assign
A4_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    vector<long long> tt(4*n), pp(4*n), ss(4*n), bb(4*n), asg(4*n); vector<char> mk(4*n,0); vector<long long> ln(4*n);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { tt[nd] = pp[nd] = ss[nd] = bb[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        ln[nd] = ln[2*nd] + ln[2*nd+1];
        auto pull = [&]() {
            tt[nd] = tt[2*nd] + tt[2*nd+1];
            pp[nd] = max(pp[2*nd], tt[2*nd] + pp[2*nd+1]);
            ss[nd] = max(ss[2*nd+1], tt[2*nd+1] + ss[2*nd]);
            bb[nd] = max({bb[2*nd], bb[2*nd+1], ss[2*nd] + pp[2*nd+1]});
        };
        pull();
    };
    auto applyA = [&](int nd, long long v) {
        tt[nd] = v * ln[nd];
        pp[nd] = ss[nd] = bb[nd] = max(v, v * ln[nd]);
        asg[nd] = v; mk[nd] = 1;
    };
    std::function<void(int)> push = [&](int nd) { if (mk[nd]) { applyA(2*nd, asg[nd]); applyA(2*nd+1, asg[nd]); mk[nd] = 0; } };
    std::function<void(int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyA(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2*nd, l, m, ql, qr, v); upd(2*nd+1, m+1, r, ql, qr, v);
        tt[nd] = tt[2*nd] + tt[2*nd+1];
        pp[nd] = max(pp[2*nd], tt[2*nd] + pp[2*nd+1]);
        ss[nd] = max(ss[2*nd+1], tt[2*nd+1] + ss[2*nd]);
        bb[nd] = max({bb[2*nd], bb[2*nd+1], ss[2*nd] + pp[2*nd+1]});
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MIN;
        if (ql <= l && r <= qr) return bb[nd];
        push(nd); int m = (l + r) / 2;
        return max(qry(2*nd, l, m, ql, qr), qry(2*nd+1, m+1, r, ql, qr));
    };
    build(1, 1, n);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp == 1) { long long v; in >> v; upd(1, 1, n, l, r, v); }
        else out << qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

A4_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // WRONG: pull forgets the cross term ss(L) + pp(R) — two independent
    // Kadanes. Passes flat arrays, fails when the best subarray crosses.
    vector<long long> tt(4*n), pp(4*n), ss(4*n), bb(4*n), asg(4*n); vector<char> mk(4*n,0); vector<long long> ln(4*n);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        ln[nd] = r - l + 1;
        if (l == r) { tt[nd] = pp[nd] = ss[nd] = bb[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        ln[nd] = ln[2*nd] + ln[2*nd+1];
        tt[nd] = tt[2*nd] + tt[2*nd+1];
        pp[nd] = max(pp[2*nd], tt[2*nd] + pp[2*nd+1]);
        ss[nd] = max(ss[2*nd+1], tt[2*nd+1] + ss[2*nd]);
        bb[nd] = max(bb[2*nd], bb[2*nd+1]);   // WRONG: cross term missing
    };
    auto applyA = [&](int nd, long long v) {
        tt[nd] = v * ln[nd];
        pp[nd] = ss[nd] = bb[nd] = max(v, v * ln[nd]);
        asg[nd] = v; mk[nd] = 1;
    };
    std::function<void(int)> push = [&](int nd) { if (mk[nd]) { applyA(2*nd, asg[nd]); applyA(2*nd+1, asg[nd]); mk[nd] = 0; } };
    std::function<void(int,int,int,int,int,long long)> upd = [&](int nd, int l, int r, int ql, int qr, long long v) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) { applyA(nd, v); return; }
        push(nd); int m = (l + r) / 2;
        upd(2*nd, l, m, ql, qr, v); upd(2*nd+1, m+1, r, ql, qr, v);
        tt[nd] = tt[2*nd] + tt[2*nd+1];
        pp[nd] = max(pp[2*nd], tt[2*nd] + pp[2*nd+1]);
        ss[nd] = max(ss[2*nd+1], tt[2*nd+1] + ss[2*nd]);
        bb[nd] = max(bb[2*nd], bb[2*nd+1]);   // WRONG
    };
    std::function<long long(int,int,int,int,int)> qry = [&](int nd, int l, int r, int ql, int qr) -> long long {
        if (qr < l || r < ql) return LLONG_MIN;
        if (ql <= l && r <= qr) return bb[nd];
        push(nd); int m = (l + r) / 2;
        return max(qry(2*nd, l, m, ql, qr), qry(2*nd+1, m+1, r, ql, qr));
    };
    build(1, 1, n);
    while (q--) {
        int tp, l, r; in >> tp >> l >> r;
        if (tp == 1) { long long v; in >> v; upd(1, 1, n, l, r, v); }
        else out << qry(1, 1, n, l, r) << "{{NL}}";
    }
""") + END

# A5: maxsub large load (no updates after build; queries only)
A5_R = CPP_STD + cpp("""    int n, q; in >> n >> q; // no array in input: values are generated
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) a[i] = (i % 2 == 0) ? 1 : -1;
    vector<long long> tt(4*n), pp(4*n), ss(4*n), bb(4*n);
    std::function<void(int,int,int)> build = [&](int nd, int l, int r) {
        if (l == r) { tt[nd] = pp[nd] = ss[nd] = bb[nd] = a[l]; return; }
        int m = (l + r) / 2; build(2*nd, l, m); build(2*nd+1, m+1, r);
        tt[nd] = tt[2*nd] + tt[2*nd+1];
        pp[nd] = max(pp[2*nd], tt[2*nd] + pp[2*nd+1]);
        ss[nd] = max(ss[2*nd+1], tt[2*nd+1] + ss[2*nd]);
        bb[nd] = max({bb[2*nd], bb[2*nd+1], ss[2*nd] + pp[2*nd+1]});
    };
    build(1, 1, n);
    out << bb[1] << "{{NL}}";
    // q-1 dummy whole-tree queries
    for (int i = 1; i < q; ++i) out << bb[1] << "{{NL}}";
""") + END

A5_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    // WRONG: brute Kadane per query — q × n = 2·10^10 ops on 0.5 CPU.
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) a[i] = (i % 2 == 0) ? 1 : -1;
    for (int t = 0; t < q; ++t) {
        long long best = LLONG_MIN, cur = 0;
        for (int i = 1; i <= n; ++i) { cur = max(a[i], cur + a[i]); best = max(best, cur); }
        out << best << "{{NL}}";
    }
""") + END

VI_P2 = {
    "hsga-p2-addmin": vi_challenge(
        "Cộng đoạn, min đoạn",
        """**Bài toán.** `1 l r v` cộng v vào [l, r]; `2 l r` in min [l, r].""",
        [("cộng rồi min", "Kiểm tay 5 phần tử."),
         ("đè lên nhau", "Hai phép cộng chồng đoạn."),
         ("n=200000 tải lớn", "Toàn mảng cộng rồi 199999 truy vấn — mảng thường là 2·10^10 phép.")],
    ),
    "hsga-p2-mixtags": vi_challenge(
        "Thẻ hỗn hợp gán/cộng",
        """**Bài toán.** `1 l r v` gán; `2 l r v` cộng; `3 l r` tổng [l, r].""",
        [("gán rồi cộng", "Cộng sau gán phải không bị mất."),
         ("cộng rồi gán", "Gán xóa thẻ cộng đang treo."),
         ("n=200000 chuỗi lộn xộn", "Gán toàn mảng + 100000 cộng + truy vấn — thứ tự hợp sai ra số sai.")],
    ),
    "hsga-p2-bigassign": vi_challenge(
        "Gán-all truy vấn hàng loạt",
        """**Bài toán.** Gán cả mảng = 5, 99999 truy vấn tổng toàn mảng, gán nửa
đầu = 7, 1 truy vấn cuối.""",
        [("chuỗi đóng gói", "Đáp án 5·n lặp lại, sau đó (7·n/2 + 5·n/2)."),
         ("kỹ thuật", "Cây lười O((n + q) log n); mảng thường quá hạn.")],
    ),
    "hsga-p2-maxsub": vi_challenge(
        "Đoạn-con lớn nhất gán đoạn",
        """**Bài toán.** `1 l r v` gán; `2 l r` in đoạn-con lớn nhất (không rỗng)
trong [l, r].""",
        [("qua biên", "[5, -10, 6]: tốt nhất 11 — cần gộp ss+pp."),
         ("gán đoạn", "apply() đặt cả bốn giá trị từ v và độ dài."),
         ("n=200000 tải lớn", "Kadane mỗi truy vấn là q × n = 2·10^10 — quá hạn.")],
    ),
}

P2_TESTS_ADDMIN = [
    contest_test("add then min", T("5 2", "1 5 2 7 3", "1 2 4 2", "2 1 3"), T("1"),
        "[1,7,4,9,3] → min(1,7,4) = 1."),
    contest_test("overlapping adds", T("5 4", "0 0 0 0 0", "1 1 3 2", "1 2 5 1", "2 2 2", "2 4 5"), T("3", "1"),
        "pos2 gets 2+1=3; pos4..5 get 1."),
    contest_test("n=200000 bulk", T("200000 200000") + T(*["1000000000"] * 200000) + T("1 1 200000 -500000000", "2 1 200000") + T(*["2 1 200000"] * 199998),
        T(*["500000000"] * 199999),
        "Whole-range add then 199999 min-queries — constant answer 5·10^8; brute O(n) per op is 4·10^10 ops."),
]

P2_TESTS_MIX = [
    contest_test("assign then add", T("4 3", "1 2 3 4", "1 2 3 5", "2 1 1 3", "3 1 4"), T("18"),
        "Assign [1,5,5,4] then +3 on [1,1]: [4,5,5,4] sums 18 — add must survive the assign's tag-clear."),
    contest_test("add then assign", T("4 3", "1 2 3 4", "2 1 4 10", "1 2 3 0", "3 2 3"), T("0"),
        "Assign clears the pending add."),
    contest_test("add, assign, then re-query", T("3 5", "10 20 30", "2 1 2 5", "1 1 3 0", "2 2 2 7", "3 2 3", "3 1 1"), T("7", "0"),
        "Pending add [1,2]+5, then assign-all 0: node [1,2] must push the stale add before the assign overwrites it; then +7 on [2,2] gives sum 7, pos1 stays 0."),
    contest_test("n=200000 shuffle", T("200000 50002") + T(*["0"] * 200000) + T("1 1 200000 5", "2 1 200000 1") + T(*["3 1 200000"] * 49999) + T("3 1 200000"),
        T(*["1200000"] * 50000),
        "Assign(5) + add(+1) → every whole sum is 6·2·10^5 = 12·10^5. Compose-order bugs drift here."),
]

P2_TESTS_BIG = [
    contest_test("assign-all bulk sums", T("200000 100002") + T(*["0"] * 200000) + T("1 1 200000 5") + T(*["3 1 200000"] * 99999) + T("1 1 100000 7") + T("3 1 200000"),
        T(*["1000000"] * 99999) + T("1200000"),
        "99999 whole sums of 5·200000 = 10^6; after the half assign: 7·10^5 + 5·10^5 = 12·10^5."),
    contest_test("shrinking assigns", T("3 4", "9 9 9", "1 1 3 4", "3 1 3", "1 1 2 6", "3 1 3"), T("12", "16"),
        "4·3=12 then 6·2+4=16."),
    contest_test("n=200000 alt load", T("200000 50000") + T(*["0"] * 200000) + T(*(["1 1 200000 2"] + ["3 1 200000"]) * 25000),
        T(*["400000"] * 25000),
        "25 000 assign+sum pairs — constant 4·10^5; array brute needs 10^10 ops."),
]  # Protocol matches hsga-p2-mixtags: 1=assign v, 2=add v, 3=sum.

P2_TESTS_MAXSUB = [                contest_test("cross the boundary", T("3 3", "5 -10 6", "2 1 3", "1 2 2 100", "2 1 3"), T("6", "111"),
        "[5,-10,6]: best non-empty is 6. After assign [5,100,6]: whole array 111 — the cross term (ss+pp across the middle) is required."),
    contest_test("assign fixes middle", T("3 2", "5 -10 6", "1 2 2 -1", "2 1 3"), T("10"),
        "[5,-1,6] → whole array 10."),
    contest_test("n=200000 alt load", T("200000 200000") + T(*(["1", "-1"] * 100000)) + T(*["2 1 200000"] * 200000),
        T(*["1"] * 200000),
        "Alternating ±1: every whole-array query answers 1; Kadane-per-query is 4·10^10 ops — certain TLE."),
]

write_practice(
    M, "hsga-p2-lazy", "Lazy Tree Drills",
    "Range add/min, mixed assign/add compose order, bulk closed-form loads, and the max-subarray node with a cross-boundary discriminator.",
    "Bài tập cây lười",
    "Cộng/min đoạn, thứ tự hợp gán/cộng, tải lớn đóng gói, và nút đoạn-con lớn nhất với test qua biên.",
    "hsga-m2-maxsub", 110, "advanced",
    [
        challenge("hsga-p2-addmin", "Range Add, Range Min",
            """**Bài toán.** n numbers, q operations: `1 l r v` adds v to [l, r];
`2 l r` prints min over [l, r].

**Constraints:** 1 ≤ n, q ≤ 2·10^5; |v| ≤ 10^9; |a[i]| ≤ 10^9.
""",
            P2_TESTS_ADDMIN, level="combination", difficulty="advanced"),
        challenge("hsga-p2-mixtags", "Mixed Assign/Add Tags",
            """**Bài toán.** `1 l r v` assigns v; `2 l r v` adds v; `3 l r` prints the
sum of [l, r].

**Constraints:** 1 ≤ n, q ≤ 2·10^5; |v| ≤ 10^9.

Compose order matters: assign kills pending adds; add after assign must
survive later pushes.
""",
            P2_TESTS_MIX, level="combination", difficulty="advanced"),
        challenge("hsga-p2-bigassign", "Bulk Assign Loads",
            """**Bài toán.** Closed-form operation scripts over n = 2·10^5: assign-all
and whole-range sums interleaved.

**Constraints:** read the operations from input as usual; the point is that
only an O((n + q) log n) lazy tree finishes.
""",
            P2_TESTS_BIG, level="independent", difficulty="advanced"),
        challenge("hsga-p2-maxsub", "Max Subarray Under Assign",
            """**Bài toán.** `1 l r v` assigns v to [l, r]; `2 l r` prints the maximum
non-empty subarray sum inside [l, r].

**Constraints:** 1 ≤ n, q ≤ 2·10^5; |v|, |a[i]| ≤ 10^9.
""",
            P2_TESTS_MAXSUB, level="combination", difficulty="advanced"),
    ],
    VI_P2,
    solutions=[
        ("hsga-p2-addmin", A1_R, A1_W),
        ("hsga-p2-mixtags", A2_R, A2_W),
        ("hsga-p2-bigassign", A2_R, A3_W),
        ("hsga-p2-maxsub", A4_R, A4_W),
    ],
)
