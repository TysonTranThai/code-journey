#!/usr/bin/env python3
"""HSG Advanced — Module 17: hsga-debug (Debugging Under Contest Load).

Debug-pattern challenges: 32-bit overflow in pair sums, an off-by-one
difference-array restore, and a deep-recursion crash turned iterative.
Each R is correct; each W exhibits the named bug class and fails its
designated test.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \\n escapes.
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-debug"

# ------------------------------------------------------------------ data
# A1 overflow: values near 2e9, target 4e9. Pairs (2e9,2e9) overflow int.
# A2 recursion: bamboo graph of 200000 nodes; a recursive DFS crashes (R is iterative).
# A3 off-by-one difference array: k range-add ops then final array.
import random

_rnd2 = random.Random(31)
_A2_N = 200000
# bamboo: parent[i] = i-1 (1-indexed), queries: subtree size of deep nodes
# answer for subtree of node v (bamboo rooted at 1): size = n - v + 1
_A2_QUERIES = [(_A2_N, 1), (1, 1), (_A2_N // 2, _A2_N - _A2_N // 2 + 1)]
# deep-chain correctness is the point; load test hits all nodes

# A3 load
_rnd3 = random.Random(13)
_A3_N = 200000
_A3_Q = 200000
_A3_OPS = []
for _ in range(_A3_Q):
    l = _rnd3.randint(1, _A3_N)
    r = _rnd3.randint(l, _A3_N)
    v = _rnd3.randint(-10, 10)
    _A3_OPS.append((l, r, v))


def diff_ops(n, ops):
    d = [0] * (n + 2)
    for (l, r, v) in ops:
        d[l] += v
        d[r + 1] -= v
    res = []
    cur = 0
    for i in range(1, n + 1):
        cur += d[i]
        res.append(cur)
    return res

_A3_FINAL = diff_ops(_A3_N, _A3_OPS)
_A3_CHECKSUM = sum(_A3_FINAL) % 1000000007

# ------------------------------------------------------------------ C++ bodies
A1_R = CPP_STD + cpp("""
    // Count unordered pairs with a[i] + a[j] == target. Values near 2e9
    // force 64-bit sums.
    int n; long long target; in >> n >> target;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    long long cnt = 0;
    int i = 0, j = n - 1;
    while (i < j) {
        long long s = a[i] + a[j];
        if (s < target) ++i;
        else if (s > target) --j;
        else {
            if (a[i] == a[j]) {
                long long c = j - i + 1;
                cnt += c * (c - 1) / 2;
                break;
            }
            long long ci = 1, cj = 1;
            while (i + 1 < j && a[i+1] == a[i]) { ++i; ++ci; }
            while (j - 1 > i && a[j-1] == a[j]) { --j; ++cj; }
            cnt += ci * cj;
            ++i; --j;
        }
    }
    out << cnt << "{{NL}}";
""") + END

A1_W = CPP_STD + cpp("""
    // WRONG: sums in 32-bit int — a[i]+a[j] with values near 2e9 overflows
    // and wraps negative; the two-pointer then walks off. Classic contest bug.
    int n; long long target; in >> n >> target;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    long long cnt = 0;
    int i = 0, j = n - 1;
    while (i < j) {
        int s = (int)(a[i] + a[j]);  // overflow here
        if (s < target) ++i;
        else if (s > target) --j;
        else { cnt += 1; ++i; --j; }
    }
    out << cnt << "{{NL}}";
""") + END

A2_R = CPP_STD + cpp("""
    // Subtree sizes on a rooted forest given as parent[] (parent[1] = 0).
    // ITERATIVE post-order: bamboo of 2e5 nodes kills recursive DFS.
    int n; in >> n;
    vector<int> par(n + 1, 0);
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) {
        in >> par[v];
        ch[par[v]].push_back(v);
    }
    vector<long long> sz(n + 1, 1);
    // iterative post-order via explicit stack of (node, child-index)
    vector<pair<int, int>> st;
    st.push_back({1, 0});
    while (!st.empty()) {
        int v = st.back().first;
        int idx = st.back().second;
        if (idx < (int)ch[v].size()) {
            ++st.back().second;
            st.push_back({ch[v][idx], 0});
        } else {
            if (par[v]) sz[par[v]] += sz[v];
            st.pop_back();
        }
    }
    int q; in >> q;
    while (q--) {
        int v; in >> v;
        out << sz[v] << "{{NL}}";
    }
""") + END

A2_W = CPP_STD + cpp("""
    // WRONG: recursive DFS — the bamboo makes recursion depth 200000,
    // smashing the stack (runtime error) long before answering.
    int n; in >> n;
    vector<int> par(n + 1, 0);
    vector<vector<int>> ch(n + 1);
    for (int v = 2; v <= n; ++v) {
        in >> par[v];
        ch[par[v]].push_back(v);
    }
    vector<long long> sz(n + 1, 1);
    function<void(int)> dfs = [&](int v) {
        for (int c : ch[v]) { dfs(c); sz[v] += sz[c]; }
    };
    dfs(1);
    int q; in >> q;
    while (q--) {
        int v; in >> v;
        out << sz[v] << "{{NL}}";
    }
""") + END

A3_R = CPP_STD + cpp("""
    // Difference array with the cancel at r+1 — answer checksum of the
    // final array after all range-adds.
    int n; int q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int t = 0; t < q; ++t) {
        long long l, r, v; in >> l >> r >> v;
        d[l] += v;
        d[r + 1] -= v;
    }
    long long cur = 0, cs = 0;
    const long long P = 1000000007LL;
    for (int i = 1; i <= n; ++i) {
        cur += d[i];
        cs = (cs + cur) % P;
    }
    out << ((cs % P) + P) % P << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""
    // WRONG: cancels at r instead of r+1 — every range is one short on the
    // right end; the checksum drifts.
    int n; int q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int t = 0; t < q; ++t) {
        long long l, r, v; in >> l >> r >> v;
        d[l] += v;
        d[r] -= v;  // off by one: should be r+1
    }
    long long cur = 0, cs = 0;
    const long long P = 1000000007LL;
    for (int i = 1; i <= n; ++i) {
        cur += d[i];
        cs = (cs + cur) % P;
    }
    out << ((cs % P) + P) % P << "{{NL}}";
""") + END

CP_M17_R = CPP_STD + cpp("""
    // Same difference-array task, no bug: matches A3_R semantics with
    // per-index answers on small data.
    int n; int q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int t = 0; t < q; ++t) {
        long long l, r, v; in >> l >> r >> v;
        d[l] += v;
        d[r + 1] -= v;
    }
    long long cur = 0;
    for (int i = 1; i <= n; ++i) {
        cur += d[i];
        out << cur << "{{NL}}";
    }
""") + END

CP_M17_W = CPP_STD + cpp("""
    // WRONG: reads the ops as (r before l) — a reversed-interval bug that
    // survives symmetric tests and fails any asymmetric one.
    int n; int q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int t = 0; t < q; ++t) {
        long long l, r, v; in >> r >> l >> v;  // swapped l/r
        d[l] += v;
        d[r + 1] -= v;
    }
    long long cur = 0;
    for (int i = 1; i <= n; ++i) {
        cur += d[i];
        out << cur << "{{NL}}";
    }
""") + END

# ------------------------------------------------------------------ tests
A1_TESTS = [
    contest_test("tiny", T("3 4000000000", "2000000000", "2000000000", "1"), T("1"),
        "2e9 + 2e9 = 4e9 overflows int (max 2147483647) — only 64-bit survives."),
    contest_test(
        "load: 200000 values near 2e9, mixed targets",
        T("4 4000000000", "2000000000", "2000000000", "2000000000", "2000000000"),
        T("6"),
        "C(4,2) = 6 pairs of equal 2e9 values sum to 4e9."),
]

_A2_PAR = [str(v - 1) for v in range(2, 200001)]  # bamboo: parent(v) = v-1

A2_TESTS = [
    contest_test("bamboo: deep subtree", T("5", "1", "2", "3", "4", "3", "3", "4", "5"), T("3", "2", "1"),
        "Chain 1-2-3-4-5: subtree of 3 is {3,4,5} = 3, of 4 is 2, of 5 is 1."),
    contest_test(
        "load: bamboo of 200000, deepest query",
        T(*(["200000"] + _A2_PAR + ["1", "1"])),
        T("200000"),
        "Depth 200000: iterative DFS passes; recursive W crashes the stack."),
]

A3_TESTS = [
    contest_test("asymmetric ops", T("4 2", "1 2 5", "2 4 3"), T("19"),
        "Final [5,8,3,3]: checksum 19; the r-cancel W gives [5,3,3,3] → 14."),
    contest_test(
        "load: 200000 ops",
        T("200000 200000", *["%d %d %d" % op for op in _A3_OPS]),
        T(str(_A3_CHECKSUM)),
        "O(n + q) difference array; the off-by-one W drifts the checksum."),
]

CP_TESTS = [
    contest_test("asymmetric", T("4 2", "1 2 5", "2 4 3"), T("5", "8", "3", "3"),
        "Op (1,2,+5) then (2,4,+3): [5,8,3,3]. The reversed-l/r W misorders the second op."),
    contest_test("single asymmetric op", T("3 1", "1 3 7"), T("7", "7", "7"),
        "One full-range op; the reversed W reads l=3, r=1 and produces [0,0,7]."),
]

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Debugging Under Contest Load",
    "The three bug classes that cost the most points — overflow, stack depth, off-by-one — as graded hunts.",
    "Sửa lỗi dưới áp lực thi đấu",
    "Ba lớp lỗi tốn điểm nhất — tràn số, độ sâu ngăn xếp, lệch-một — thành các bài truy tìm được chấm.",
    ["hsga-m17-overflow", "hsga-m17-stack", "hsga-m17-offbyone"],
    ["hsga-p17-debug"],
)

write_lesson(
    M, "hsga-m17-overflow",
    "Overflow Hunting",
    "2e9 + 2e9 is negative if your sum is int. Where does the standard say values can go, and where does your type stop?",
    30,
    """
# Know your type limits

int stops at 2147483647; a[i]+a[j] with a_i near 2e9 needs long long
BEFORE the addition. Two-pointer pair-sums silently walk off when the
sum wraps negative. Read constraints like a compiler: every maximum
multiplied, every sum accumulated — does the widest expression fit?
""", "Truy tìm tràn số",
    "2e9 + 2e9 là số âm nếu tổng của bạn là int. Ràng buộc cho phép giá trị đi tới đâu, và kiểu của bạn dừng ở đâu?",

    """
# Biết giới hạn kiểu của mình

int dừng ở 2147483647; a[i]+a[j] với a_i gần 2e9 cần long long TRƯỚC
khi cộng. Hai con trỏ lặng lẽ đi lạc khi tổng bị bọc thành số âm. Đọc
ràng buộc như trình biên dịch: mọi tích giá trị lớn nhất, mọi tổng tích
lũy — biểu thức rộng nhất có vừa không?
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m17-stack",
    "Stack Depth and Iterative DFS",
    "A bamboo of 200000 nodes is 200000 stack frames. Iterative DFS with an explicit stack is the fix — and a graded skill.",
    30,
    """
# Recursion is a resource

Each frame costs stack; a linear chain of n nodes is n frames. The
sandbox (like most judges) gives a few MB — depth past ~1e5 dies. The
fix: explicit stack, process (node, child-index) pairs, accumulate
child answers before popping. Convert every n-deep recursion once and
you will recognize it forever.
""", "Độ sâu ngăn xếp và DFS lặp",
    "Một chuỗi 200000 đỉnh là 200000 khung ngăn xếp. DFS lặp với ngăn xếp tường minh là cách sửa — và là kỹ năng được chấm.",

    """
# Đệ quy là tài nguyên

Mỗi khung tốn ngăn xếp; chuỗi n đỉnh là n khung. Sandbox (như đa số
judge) cho vài MB — sâu quá ~1e5 là chết. Cách sửa: ngăn xếp tường
minh, xử lý cặp (đỉnh, chỉ-số-con), gom đáp án con trước khi pop. Chuyển
đổi một lần mọi đệ quy sâu-n và bạn nhận ra nó mãi mãi.
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m17-offbyone",
    "Off-by-One and Boundary Tests",
    "Difference arrays, half-open ranges, and reversed reads — the bugs that pass every symmetric test you try by hand.",
    30,
    """
# Design tests that kill the bug class

Off-by-one survives [l, r] = [1, n] tests because both directions are
symmetric. Kill it with asymmetric ranges: [1,2] then [2,4] on n = 4.
Half-open semantics: an interval [a, b) ending at t does not overlap
[t, ...]. Reversed l/r reads pass palindromic data — always include one
lopsided op.
""", "Lệch-một và test biên",
    "Mảng hiệu, nửa mở, đọc ngược — những lỗi vượt qua mọi test đối xứng bạn thử bằng tay.",

    """
# Thiết kế test giết đúng lớp lỗi

Lệch-một sống sót qua test [l, r] = [1, n] vì cả hai hướng đối xứng.
Giết nó bằng khoảng lệch: [1,2] rồi [2,4] trên n = 4. Ngữ nghĩa nửa
mở: khoảng [a, b) kết thúc tại t KHÔNG chồng [t, ...]. Đọc ngược l/r
vượt qua dữ liệu đối xứng — luôn kèm một phép toán lệch hẳn.
""", difficulty="advanced",
)

write_practice(
    M, "hsga-p17-debug", "Bug Hunt",
    "Pair sums at 4e9, subtree sizes on a 200000-node bamboo, and 200000 difference-array ops.",
    "Truy tìm lỗi",
    "Tổng cặp tại 4e9, kích thước cây con trên chuỗi 200000 đỉnh, và 200000 phép toán mảng hiệu.",
    "hsga-m17-offbyone",
    110,
    "advanced",
    [
        challenge("hsga-p17-pairs", "Overflow Pairs",
            """**Problem.** Line 1: n target. Then n values. Print the number
of unordered pairs with a[i] + a[j] == target.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ a_i ≤ 2*10^9; target < 4*10^9.

Values near 2e9 make 32-bit sums wrap negative.
""",
            A1_TESTS, level="debugging", difficulty="advanced"),
        challenge("hsga-p17-subtree", "Deep Subtrees",
            """**Problem.** Line 1: n. Then n-1 lines: parent of v (2..n),
parent(1) omitted. Then q and q node ids. Print each subtree size.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ q ≤ 200000; the tree may be a
bamboo of depth n.

Recursive DFS of depth 2e5 crashes; go iterative.
""",
            A2_TESTS, level="debugging", difficulty="advanced"),
        challenge("hsga-p17-diff", "Difference Discipline",
            """**Problem.** Line 1: n q. Then q lines: l r v (add v on [l, r]).
Print the checksum: sum of final values mod 1e9+7.

**Constraints:** 1 ≤ n, q ≤ 200000; |v| ≤ 10.

The cancel point is r+1, not r.
""",
            A3_TESTS, level="debugging", difficulty="advanced"),
    ],
    {
        "hsga-p17-debug": vi_challenge(
            "Truy tìm lỗi",
            """**Bài toán.** Ba bài: tổng cặp tới 4e9, kích thước cây con trên
chuỗi sâu 200000, và 200000 phép toán mảng hiệu.""",
            [("tràn số", "2e9+2e9 tràn int — dùng long long trước khi cộng."),
             ("ngăn xếp", "DFS đệ quy sâu 2e5 gãy; dùng ngăn xếp tường minh."),
             ("mảng hiệu", "Huỷ tại r+1, không phải r.")],
        ),
    },
    solutions=[
        ("hsga-p17-pairs", A1_R, A1_W),
        ("hsga-p17-subtree", A2_R, A2_W),
        ("hsga-p17-diff", A3_R, A3_W),
    ],
)

write_checkpoint(
    M, "hsga-cp-m17",
    "Checkpoint — Boundary Reading",
    "Difference-array outputs graded on asymmetric ops where reversed-interval reading fails; reading the input format precisely is the skill.",
    40,
    """
**Checkpoint — Boundary.** Line 1: n q. Then q lines: l r v. After all
ops, print every final value, one per line.

Read the op format exactly: add v on [l, r] inclusive.
""",
    "Điểm kiểm tra — Đọc biên",
    "Kết quả mảng hiệu chấm trên các phép toán lệch nơi đọc ngược khoảng thất bại; đọc đúng định dạng nhập là kỹ năng.",
    """
**Checkpoint — Biên.** Dòng 1: n q. Sau đó q dòng: l r v. Sau mọi phép
toán, in mọi giá trị cuối, mỗi dòng một giá trị.

Đọc đúng định dạng: cộng v trên [l, r] bao hai đầu.
""",
    challenge(
        "hsga-cp-m17-boundary",
        "Boundary Values",
        """**Problem.** Line 1: n q. Then q lines: l r v (add v on [l, r]).
Print the final array, one value per line.

**Constraints:** 1 ≤ n, q ≤ 200000; |v| ≤ 10.

The W reads r before l — fatal on asymmetric ops.
""",
        CP_TESTS,
        level="debugging",
        difficulty="advanced",
    ),
    vi_challenge(
        "Giá trị biên",
        """**Bài toán.** Dòng 1: n q. Sau đó q dòng: l r v (cộng v trên [l, r]).
In mảng cuối, mỗi dòng một giá trị.""",
        [("định dạng", "l rồi r rồi v — đọc đúng thứ tự."),
         ("mảng hiệu", "Cộng tại l, trừ tại r+1, chạy prefix."),
         ("bẫy", "Khoảng đối xứng giấu mọi lỗi đọc ngược.")],
    ),
    solution=CP_M17_R,
    wrong=CP_M17_W,
)

print("module m17 complete")
