#!/usr/bin/env python3
"""HSG Advanced — Module 3: hsga-fenwick2 (Fenwick Variants).

kth-order Fenwick descent, offline distinct-count sweep, range-add/point-query
difference BIT, and inversion counting via BIT over compressed ranks.
Checkpoint composes descent + prefix-difference on one tree.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes.
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

M = "hsga-fenwick2"
write_module(
    M,
    "Fenwick Variants and Offline Power",
    "The BIT beyond prefix sums: kth-order descent in O(log n), offline sweeps that reorder hard online problems into easy sorted ones, difference tricks for range updates, and inversion counting.",
    "Fenwick nâng cao và sức mạnh ngoại tuyến",
    "BIT vượt ngoài tổng tiền tố: đi xuống tìm phần tử thứ k trong O(log n), quét ngoại tuyến biến bài khó thành bài dễ, mẹo sai phân cho cập nhật đoạn, và đếm nghịch thế.",
    ["hsga-m3-kth", "hsga-m3-offline", "hsga-m3-diffbit", "hsga-m3-inversions", "hsga-cp-m3"],
    ["hsga-p3-fenwick"],
)

write_lesson(
    M, "hsga-m3-kth",
    "Fenwick Binary-Lifting Descent",
    "One O(log n) walk finds the smallest position whose prefix reaches k — no extra memory, just the tree's own block structure.",
    30,
    """
# Finding the k-th one

A Fenwick tree stores prefix sums. Given a target k, we want the smallest
index `pos` with `prefix(pos) >= k` — the position of the k-th one in a
0/1 array. Scanning is O(n); the classic trick is a single top-down walk:

```
int pos = 0; long long rem = k;
for (int pw = LOG; pw >= 0; --pw) {
    int np = pos + (1 << pw);
    if (np <= n && fen[np] < rem) { pos = np; rem -= fen[np]; }
}
return pos + 1;   // 1-based answer
```

Why it works: `fen[np]` covers exactly the block `(pos, np]`. If that
block's count fits inside `rem`, jump over it in one step; otherwise do
not. After the loop, `pos` is the largest index whose prefix is still
`< k`, so the answer is `pos + 1`. Each level is inspected once — O(log n)
total. Binary-searching over `prefix(i)` instead would be O(log^2 n).

Guard rails:

- `k` must satisfy `1 <= k <= prefix(n)`; check at the call site.
- The same descent finds the k-th **empty** slot: walk on the occupied
  BIT and compare `len - occupied` (empties in the block) against `rem`.
- Multiset rank queries: insert v as `upd(v, 1)`; the k-th smallest is the
  descent with k.

## Common bug

Forgetting `rem -= fen[np]` after a jump. The walk then overshoots and can
even return `n + 1` — always test with k = 1 on an empty tree.

""",
    "Đi xuống Fenwick bằng luỹ thừa 2",
    "Một lần đi O(log n) tìm vị trí nhỏ nhất có tiền tố đạt k — không cần bộ nhớ thêm, chỉ dùng cấu trúc khối của cây.",
    """
# Đi xuống Fenwick tìm phần tử thứ k

Cây Fenwick lưu tổng tiền tố. Cho k, tìm vị trí nhỏ nhất sao cho
`prefix(pos) >= k` — vị trí phần tử thứ k trong mảng 0/1. Mẹo kinh điển:
đi từ trên xuống theo luỹ thừa 2; nếu khối `fen[np]` vừa trong `rem` thì
nhảy qua và trừ đi. Sau vòng lặp, `pos` là chỉ số lớn nhất có tiền tố
`< k`, đáp án là `pos + 1`. Tổng O(log n) — nhanh hơn tìm kiếm nhị phân
trên `prefix(i)` (O(log² n)).

Lỗi hay gặp: quên trừ `rem -= fen[np]` sau khi nhảy — phép đi vượt đích,
thậm chí trả về n + 1. Luôn thử k = 1 trên cây rỗng.

Cùng phép đi này tìm ô trống thứ k: đi trên BIT "đã chiếm" và so sánh
`len − occupied` (số ô trống trong khối) với `rem`. Truy vấn hạng multiset:
chèn v là `upd(v, 1)`; phần tử nhỏ thứ k là phép đi với k.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m3-offline",
    "Offline Sweeps: Sort Queries by Right End",
    "If the queries can be reordered, one sweep with a Fenwick solves 'distinct values in range' in O((n + q) log n) — impossible online without heavier machinery.",
    35,
    """
# Distinct values in a range, offline

Count distinct values among `a[l..r]` for many queries. Online, this needs
a persistent structure or a merge-sort tree. Offline there is a beautiful
sweep: sort queries by `r`, scan `r` from 1 to n, and keep in the Fenwick
a 1 at each position that is the **last occurrence so far** of its value:

- when `r` visits value x with previous occurrence p: `upd(p, -1)`, then
  `upd(r, +1)`, and `last[x] = r`;
- a query `(l, r)` answered at sweep time r is
  `prefix(r) - prefix(l-1)`: the number of last-occurrences inside
  `[l, r]`, which equals the number of distinct values there.

Invariant: at any moment, every value seen so far contributes exactly one
1 — at its most recent position. Any subarray `[l, r]` therefore contains
the 1s of precisely the values occurring in it.

The general pattern: **if query order does not matter, sort by one
endpoint and sweep.** The same skeleton handles offline 2D dominance
counts and "how many distinct colors on a path" (after an Euler tour).
Mo's algorithm is the heavier sibling when updates force online order —
not needed here.
""",
    "Quét ngoại tuyến: sắp truy vấn theo đầu phải",
    "Nếu được sắp lại truy vấn, một phép quét + Fenwick giải 'số giá trị phân biệt trong đoạn' với O((n + q) log n).",
    """
# Quét ngoại tuyến: đếm giá trị phân biệt trong đoạn

Đếm giá trị phân biệt trên [l, r] với nhiều truy vấn: sắp truy vấn theo r
tăng dần rồi quét; Fenwick đánh dấu 1 tại **lần xuất hiện gần nhất** của
mỗi giá trị. Khi gặp x có lần trước p: trừ 1 ở p, cộng 1 ở r. Trả lời
truy vấn (l, r) đúng lúc quét tới r: `prefix(r) − prefix(l−1)`.

Bất biến: mỗi giá trị đã gặp đóng góp đúng một số 1 ở vị trí mới nhất —
nên đoạn [l, r] chứa đúng các số 1 của các giá trị xuất hiện trong đó.

Mẫu tổng quát: **thứ tự truy vấn không quan trọng → sắp theo một đầu mút
rồi quét**. Cùng khung này giải bài trội 2 chiều ngoại tuyến và "số màu
phân biệt trên đường đi" (sau Euler tour).
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m3-diffbit",
    "Difference Fenwicks: Range Add, Point Query",
    "Two one-line identities — a difference array over a BIT, and the two-BIT formula for range add + range sum — cover most update/query mixes without a segment tree.",
    30,
    """
# Range updates through differences

**Range add, point query.** Adding v to [l, r] is `upd(l, v)` and
`upd(r+1, -v)` on a plain Fenwick of the difference array; the value at
position i is `prefix(i)`. O(log n) per operation, ten lines total.

**Range add, range sum.** The prefix sum of a range-updated array needs
two BITs holding the coefficients of an expanded formula. After adding v
to [l, r]:

```
sum(1..i) = i * B1(i) - B2(i)
B1: upd(l, v), upd(r+1, -v)
B2: upd(l, v*(l-1)), upd(r+1, -v*r)
```

Derivation: write the array as a sum of ramps (the difference array
integrated once). If a problem mixes range-add with range-sum but has no
min/max or assign, this is lighter than a lazy segment tree — fewer
invariants, smaller constants, fewer bugs.

When NOT to bother: any operation pair involving min/max or assignment
breaks differences — go straight to lazy propagation (Module 2).
""",
    "Fenwick sai phân: cộng đoạn, truy vấn điểm",
    "Hai đẳng thức một dòng — sai phân trên BIT, và công thức hai-BIT cho cộng đoạn + tổng đoạn — phủ phần lớn cặp cập nhật/truy vấn không cần cây segment.",
    """
# Fenwick sai phân: cộng đoạn, truy vấn điểm

Cộng đoạn, truy vấn điểm: thêm v vào [l, r] là `upd(l, v), upd(r+1, −v)`
trên Fenwick của mảng sai phân; giá trị tại i là `prefix(i)`. O(log n)
mỗi thao tác, chưa tới mười dòng.

Cộng đoạn + tổng đoạn: hai BIT theo công thức `sum(1..i) = i·B1(i) − B2(i)`.
Nếu bài chỉ có cộng đoạn và tổng đoạn — nhẹ hơn cây lười, ít lỗi hơn,
hằng số nhỏ hơn. Nhưng min/max hoặc gán sẽ phá sai phân — chuyển thẳng
sang cây lười (Module 2).
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m3-inversions",
    "Counting Inversions with a BIT",
    "Merge sort counts inversions; a Fenwick over compressed ranks counts them in one pass — and the same pass reports 'how many greater elements to my left' per position.",
    30,
    """
# Inversions in one sweep

An inversion is a pair `i < j` with `a[i] > a[j]`. Compress values to
ranks, scan left to right, keep a BIT of seen ranks; for each new element
the number of already-seen strictly-greater elements is
`i - prefix(rank)` (prefix(rank) counts seen elements <= a[i], inserted
after counting). Summing gives the total in O(n log n) with O(n) memory —
compression is what makes `a[i] <= 10^9` harmless.

Equal elements are NOT inversions: `prefix(rank)` with the element's own
rank correctly excludes them. A `>=` comparison double-counts them — a
classic wrong answer on arrays with duplicates.

The same pattern counts **cross-inversions** in divide and conquer: while
merging two sorted halves, count pairs (left, right) with left > right.
That is exactly merge sort's inversion count — the bridge to CDQ divide
and conquer for 3D dominance problems.
""",
    "Đếm nghịch thế bằng BIT",
    "Merge sort đếm được nghịch thế; BIT trên hạng đã nén đếm trong một lượt — và mỗi vị trí còn cho biết 'bên trái có bao nhiêu phần tử lớn hơn'.",
    """
# Đếm nghịch thế bằng BIT

Nghịch thế là cặp `i < j` với `a[i] > a[j]`. Nén giá trị thành hạng, quét
trái → phải, BIT lưu các hạng đã gặp; với phần tử mới, số phần tử đã gặp
lớn hơn là `i − prefix(rank)` (prefix đếm các phần tử ≤ a[i], chèn sau
khi đếm). Tổng O(n log n), bộ nhớ O(n) nhờ nén.

Phần tử bằng nhau KHÔNG là nghịch thế — so sánh ≥ sẽ đếm thừa, lỗi kinh
diển trên mảng có trùng giá trị.

Cùng mẫu này đếm nghịch thế chéo trong chia để trị: khi trộn hai nửa đã
sắp, đếm cặp (trái, phải) với trái > phải — chính là đếm nghịch thế của
merge sort, cầu nối sang CDQ chia để trị cho bài trội 3 chiều.
""",
    difficulty="advanced",
)

# ---------------------------------------------------------------- checkpoint
CP_M3_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    // op 1 k: occupy the k-th empty slot, print its position
    // op 2 l r: print occupied count in [l, r]
    vector<long long> fen(n + 1, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    auto kthEmpty = [&](long long k) {
        int pos = 0; long long rem = k;
        for (int pw = 17; pw >= 0; --pw) {
            int np = pos + (1 << pw);
            if (np <= n) {
                long long len = np - pos;
                long long empties = len - fen[np];
                if (empties < rem) { pos = np; rem -= empties; }
            }
        }
        return pos + 1;
    };
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) { long long k; in >> k; int p = kthEmpty(k); upd(p, 1); out << p << "{{NL}}"; }
        else { int l, r; in >> l >> r; out << pref(r) - pref(l - 1) << "{{NL}}"; }
    }
""") + END

CP_M3_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> fen(n + 1, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    // WRONG descent: never subtracts the jumped block from rem, so the walk
    // overshoots on the very first occupy (returns n+1 on an empty tree).
    auto kthEmpty = [&](long long k) {
        int pos = 0; long long rem = k;
        for (int pw = 17; pw >= 0; --pw) {
            int np = pos + (1 << pw);
            if (np <= n) {
                long long len = np - pos;
                long long empties = len - fen[np];
                if (empties < rem) { pos = np; }
            }
        }
        return pos + 1;
    };
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) { long long k; in >> k; int p = kthEmpty(k); if (p >= 1 && p <= n) upd(p, 1); out << p << "{{NL}}"; }
        else { int l, r; in >> l >> r; out << pref(r) - pref(l - 1) << "{{NL}}"; }
    }
""") + END

CK_TESTS = [
    contest_test("first three", T("5 5", "1 1", "1 1", "1 1", "2 3 3", "2 4 4"), T("1", "2", "3", "1", "0"),
        "Occupy 1,2,3; slot 3 occupied, slot 4 empty."),
    contest_test("gaps", T("10 4", "1 10", "1 1", "2 9 10", "2 9 9"), T("10", "1", "1", "0"),
        "Occupy 10 then 1; [9,10] has one occupied (10), [9,9] none."),
    contest_test("n=200000 mixed load",
        T("200000 150000")
        + T(*["1 1"] * 50000)
        + T(*["1 2"] * 50000)
        + T(*["2 1 100001"] * 50000),
        T(*[str(i) for i in range(1, 50001)])
        + T(*[str(50001 + i) for i in range(1, 50001)])
        + T(*["100000"] * 50000),
        "50000 first-empties fill 1..50000; then each k=2 fills 50002..100001; every [1,100001] count is 100000. O(n) per occupy cannot finish."),
]

write_checkpoint(
    M, "hsga-cp-m3", "Checkpoint — Fenwick Mastery",
    "Two jobs on one tree: find the k-th empty slot by binary-lifting descent, then answer range-occupancy counts by prefix difference. The broken descent overshoots on the very first op.",
    25,
    """
**Checkpoint — Fenwick.** n ≤ 200 000 ô trống, q ≤ 200 000 thao tác:
`1 k` = chiếm ô trống thứ k (in vị trí); `2 l r` = in số ô đã chiếm trong
[l, r]. Một cây Fenwick làm cả hai: đi xuống luỹ thừa 2 cho op 1, hiệu
tiền tố cho op 2. Lỗi đi xuống (quên trừ rem) vượt đích ngay thao tác đầu.
""",
    "Điểm kiểm tra — Fenwick thành thạo",
    "Hai việc trên một cây: tìm ô trống thứ k bằng đi xuống luỹ thừa 2, đếm ô đã chiếm trong đoạn bằng hiệu tiền tố.",
    """
**Checkpoint — Fenwick.** n, q ≤ 200 000: `1 k` chiếm ô trống thứ k (in vị
trí); `2 l r` in số ô đã chiếm trong [l, r].
""",
    challenge(
        "hsga-cp-m3-fenwick",
        "Slots: kth Empty and Range Count",
        """**Bài toán.** n empty slots in a row, q operations:
`1 k` — occupy the k-th still-empty slot and print its 1-based position;
`2 l r` — print the number of occupied slots in [l, r].

**Constraints:** 1 ≤ n, q ≤ 200 000; for op 1, k never exceeds the number
of empty slots.

One Fenwick serves both jobs: descent on empty counts for op 1
(block empties = len − occupied), prefix difference for op 2.
""",
        CK_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Ô trống thứ k và đếm đoạn",
        """**Bài toán.** n ô trống, q thao tác: `1 k` chiếm ô trống thứ k (in vị
trí); `2 l r` in số ô đã chiếm trong [l, r].""",
        [("ba ô đầu", "Kiểm tay 1, 2, 3."),
         ("khe hở", "Chiếm 10 rồi 1 — đoạn [9,10] có 1 ô."),
         ("n=200000 tải hỗn hợp", "50000 lần chiếm ô đầu + 50000 lần chiếm ô thứ hai + 50000 truy vấn đếm — mỗi thao tác phải O(log n).")],
    ),
    solution=CP_M3_R,
    wrong=CP_M3_W,
)

# ------------------------------------------------------------ practice R/W
# A1: kth-empty slots + occupancy probe
A1_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> fen(n + 1, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    vector<char> occ(n + 1, 0);
    auto kthEmpty = [&](long long k) {
        int pos = 0; long long rem = k;
        for (int pw = 17; pw >= 0; --pw) {
            int np = pos + (1 << pw);
            if (np <= n) {
                long long len = np - pos;
                long long empties = len - fen[np];
                if (empties < rem) { pos = np; rem -= empties; }
            }
        }
        return pos + 1;
    };
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) { long long k; in >> k; int p = kthEmpty(k); occ[p] = 1; upd(p, 1); out << p << "{{NL}}"; }
        else { int p; in >> p; out << (occ[p] ? 1 : 0) << "{{NL}}"; }
    }
""") + END

A1_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<char> occ(n + 1, 0);
    // WRONG: scans from the last answered position instead of position 1 —
    // any empty slot BEFORE the cursor is skipped, and large k forces an
    // O(n) scan per op that also times out.
    int cursor = 1;
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) {
            long long k; in >> k;
            long long cnt = 0; int p = cursor;
            for (; p <= n; ++p) {
                if (!occ[p]) { ++cnt; if (cnt == k) break; }
            }
            occ[p] = 1; cursor = p;
            out << p << "{{NL}}";
        } else { int p; in >> p; out << (occ[p] ? 1 : 0) << "{{NL}}"; }
    }
""") + END

A1_TESTS = [
    contest_test("first three", T("5 5", "1 1", "1 1", "1 1", "2 3", "2 4"), T("1", "2", "3", "1", "0"),
        "Occupy 1,2,3; slot 3 occupied, slot 4 empty."),
    contest_test("cursor trap", T("10 4", "1 2", "1 1", "2 1", "2 3"), T("2", "1", "1", "0"),
        "Occupy 2nd empty = 2, then 1st empty = 1 (an empty BEFORE the cursor). A scan-from-cursor wrongly returns 3."),
    contest_test("n=200000 heavy k",
        T("200000 100000") + T(*["1 100000"] * 100000),
        T(*[str(100000 + i) for i in range(100000)]),
        "Each op takes the 100000th empty: 100000, then 100001, ... Skipped-behind empties accumulate — linear scans die here."),
]

# A2: distinct values in range (offline sweep + BIT)
A2_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    vector<int> L(q), Rr(q), ord(q);
    for (int i = 0; i < q; ++i) { in >> L[i] >> Rr[i]; ord[i] = i; }
    sort(ord.begin(), ord.end(), [&](int x, int y){ return Rr[x] < Rr[y]; });
    vector<int> fen(n + 1, 0);
    auto upd = [&](int i, int d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { int s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    vector<int> last(1000001, 0), ans(q);
    int r = 0;
    for (int qi = 0; qi < q; ++qi) {
        int id = ord[qi];
        while (r < Rr[id]) {
            ++r;
            int x = a[r];
            if (last[x]) upd(last[x], -1);
            upd(r, 1);
            last[x] = r;
        }
        ans[id] = pref(Rr[id]) - pref(L[id] - 1);
    }
    for (int i = 0; i < q; ++i) out << ans[i] << "{{NL}}";
""") + END

A2_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    // WRONG: copies the range, sorts, and uniques per query — correct
    // output, but 5·10^4 × (n log n) costs far beyond the budget.
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        vector<int> s(a.begin() + l, a.begin() + r + 1);
        sort(s.begin(), s.end());
        s.erase(unique(s.begin(), s.end()), s.end());
        out << (int)s.size() << "{{NL}}";
    }
""") + END

A2_TESTS = [
    contest_test("mixed array", T("5 4", "1 2 1 3 2", "1 5", "2 4", "1 3", "3 5"), T("3", "3", "2", "3"),
        "[1..5]={1,2,3}; [2..4]={2,1,3}; [1..3]={1,2}; [3..5]={1,3,2}."),
    contest_test("all equal", T("4 2", "7 7 7 7", "1 4", "2 3"), T("1", "1"),
        "Duplicates count once."),
    contest_test("n=50000 full-range queries",
        T("50000 50000") + T(*[str(i % 500 + 1) for i in range(50000)]) + T(*["1 50000"] * 50000),
        T(*["500"] * 50000),
        "500 distinct values cycling; every full-range answer is 500. A per-query scan is 2.5·10^9 ops — timeout."),
]

# A3: range add, point query with a difference BIT
A3_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> fen(n + 2, 0);
    auto upd = [&](int i, long long d) { for (; i <= n; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { long long s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long v; in >> l >> r >> v; upd(l, v); if (r + 1 <= n) upd(r + 1, -v); }
        else { int p; in >> p; out << pref(p) << "{{NL}}"; }
    }
""") + END

A3_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1, 0);
    // WRONG: applies each add element-by-element — O(r - l) per op;
    // 10^5 whole-array adds cost 2·10^10 ops and time out.
    for (int i = 0; i < q; ++i) {
        int tp; in >> tp;
        if (tp == 1) { int l, r; long long v; in >> l >> r >> v; for (int j = l; j <= r; ++j) a[j] += v; }
        else { int p; in >> p; out << a[p] << "{{NL}}"; }
    }
""") + END

A3_TESTS = [
    contest_test("overlapping adds", T("4 5", "1 1 4 10", "2 2", "1 2 3 5", "2 2", "2 4"), T("10", "15", "10"),
        "a=[10,10,10,10] then a=[10,15,15,10]."),
    contest_test("negative add", T("3 2", "1 1 3 -5", "2 3"), T("-5"),
        "Whole-array negative add."),
    contest_test("n=200000 bulk adds",
        T("200000 200000") + T(*["1 1 200000 1"] * 100000) + T(*["2 7"] * 100000),
        T(*["100000"] * 100000),
        "10^5 whole-range adds of +1 then 10^5 point reads of position 7: every answer is 100000."),
]

# A4: inversion count
A4_R = CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    vector<int> vals(a);
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    auto rk = [&](int x) { return int(lower_bound(vals.begin(), vals.end(), x) - vals.begin()) + 1; };
    int m = (int)vals.size();
    vector<int> fen(m + 1, 0);
    auto upd = [&](int i, int d) { for (; i <= m; i += i & (-i)) fen[i] += d; };
    auto pref = [&](int i) { int s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; };
    long long inv = 0;
    for (int i = 0; i < n; ++i) {
        int r = rk(a[i]);
        inv += (long long)i - pref(r);   // seen strictly greater than a[i]
        upd(r, 1);
    }
    out << inv << "{{NL}}";
""") + END

A4_W = CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    // WRONG: counts pairs with a[i] >= a[j] — equal elements are treated
    // as inversions (double-counted), and O(n^2) blows the limit anyway.
    long long inv = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (a[i] >= a[j]) ++inv;
    out << inv << "{{NL}}";
""") + END

A4_TESTS = [
    contest_test("small", T("4", "3 1 2 4"), T("2"),
        "Pairs (3,1) and (3,2)."),
    contest_test("duplicates are not inversions", T("3", "2 2 2"), T("0"),
        "A >= comparison would report 3."),
    contest_test("n=200000 decreasing", T("200000") + T(*[str(200000 - i) for i in range(200000)]), T("19999900000"),
        "Strictly decreasing: n(n-1)/2 = 19999900000. O(n^2) enumeration cannot finish."),
]

VI_P3 = {
    "hsga-p3-kthempty": vi_challenge(
        "Chiếm ô trống thứ k",
        """**Bài toán.** n ô trống, q thao tác: `1 k` chiếm ô trống thứ k (in vị
trí); `2 p` in 1 nếu ô p đã chiếm, 0 nếu chưa.""",
        [("k=1 luôn ô trống đầu", "Sau các lần chiếm, ô trống đầu dịch chuyển."),
         ("bẫy con trỏ", "Chiếm ô trống thứ 2 rồi thứ nhất: ô trống NẰM TRƯỚC con trỏ bị bỏ sót nếu quét từ vị trí cũ."),
         ("n=200000 k lớn", "Mỗi lần lấy ô trống thứ 100000 — quét tuyến tính là O(n·q), quá chậm.")],
    ),
    "hsga-p3-distcnt": vi_challenge(
        "Số giá trị phân biệt trong đoạn",
        """**Bài toán.** n phần tử (giá trị ≤ 10^6), q truy vấn (l, r): in số giá
trị phân biệt trong a[l..r].""",
        [("mảng trộn", "Phần tử lặp chỉ đếm một lần."),
         ("toàn bằng nhau", "Đáp án luôn 1."),
         ("n=50000 truy vấn toàn mảng", "Quét mỗi truy vấn là 2,5·10^9 phép — quá chậm; phải quét ngoại tuyến + Fenwick.")],
    ),
    "hsga-p3-rangeadd": vi_challenge(
        "Cộng đoạn, truy vấn điểm",
        """**Bài toán.** Mảng n phần tử (khởi tạo 0), q thao tác: `1 l r v` cộng v
vào [l, r]; `2 p` in giá trị hiện tại của phần tử p.""",
        [("cộng chồng", "Hai lần cộng chồng nhau phải cộng dồn đúng."),
         ("cộng âm", "Giá trị có thể âm."),
         ("n=200000", "Cộng trực tiếp từng phần tử là O(r−l) mỗi thao tác — quá chậm; dùng BIT sai phân.")],
    ),
    "hsga-p3-inversions": vi_challenge(
        "Đếm nghịch thế",
        """**Bài toán.** Mảng n phần tử, giá trị tới 10^9. In số cặp i < j với
a[i] > a[j]. Đáp án dùng long long.""",
        [("nhỏ", "Kiểm tay trên 4 phần tử."),
         ("trùng giá trị", "Cặp bằng nhau KHÔNG là nghịch thế."),
         ("n=200000 giảm dần", "n(n−1)/2 nghịch thế — O(n²) quá chậm; nén + BIT là O(n log n).")],
    ),
}

write_practice(
    M, "hsga-p3-fenwick", "Fenwick Variant Drills",
    "Four problems stretching the same tree in four directions: order statistics, offline sweeps, difference tricks, and inversion counting.",
    "Bài tập biến thể Fenwick",
    "Bốn bài kéo dài cùng một cây theo bốn hướng: thống kê thứ tự, quét ngoại tuyến, mẹo sai phân, và đếm nghịch thế.",
    "hsga-m3-inversions",
    120,
    "advanced",
    [
        challenge("hsga-p3-kthempty", "Occupy the k-th Empty Slot",
            """**Bài toán.** n empty slots, q operations: `1 k` — occupy the k-th
still-empty slot and print its position; `2 p` — print 1 if slot p is
occupied, else 0.

**Constraints:** 1 ≤ n, q ≤ 200 000; k never exceeds the number of empty
slots. Op 1 must be O(log n) — the descent walk on empty counts.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p3-distcnt", "Distinct Values in a Range",
            """**Bài toán.** An array of n integers (values up to 10^6), q queries
`l r`: print the number of distinct values in a[l..r].

**Constraints:** 1 ≤ n, q ≤ 50 000. Offline sweep by right end + Fenwick:
O((n + q) log n).
""",
            A2_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p3-rangeadd", "Range Add, Point Query",
            """**Bài toán.** Zero-initialized array of size n, q operations:
`1 l r v` adds v to [l, r]; `2 p` prints a[p].

**Constraints:** 1 ≤ n, q ≤ 200 000; |v| ≤ 10^9; answers fit in long long.
""",
            A3_TESTS, level="independent", difficulty="intermediate"),
        challenge("hsga-p3-inversions", "Count the Inversions",
            """**Bài toán.** An array of n integers (up to 10^9): print the number of
pairs i < j with a[i] > a[j]. Use 64-bit for the answer.

**Constraints:** 1 ≤ n ≤ 200 000. Coordinate compression + BIT: O(n log n).
""",
            A4_TESTS, level="independent", difficulty="intermediate"),
    ],
    VI_P3,
    solutions=[
        ("hsga-p3-kthempty", A1_R, A1_W),
        ("hsga-p3-distcnt", A2_R, A2_W),
        ("hsga-p3-rangeadd", A3_R, A3_W),
        ("hsga-p3-inversions", A4_R, A4_W),
    ],
)
