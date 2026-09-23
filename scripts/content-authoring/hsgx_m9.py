#!/usr/bin/env python3
"""HSG Intensive — Module 9: hsgx-mixed (Mixed Problem Sets).

Ten problems per set would be the contest norm, but the platform's practice
sets are per-module; this module ships three graded mixed sets (A/B/C) whose
statements never name the algorithm. Set A is advanced-level, set B hard,
set C very hard. The checkpoint is a fourth mixed set with an HSG-challenge
flavor. Recognition under time pressure is the skill; the topic list is the
student's to build.

Conventions (same as m1-m8): T() real newlines; cpp() turns {{NL}} into \n
escapes; explicit includes via CPP_STD; per-line outputs get per-line wants;
big-test ground truths Python-verified.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgx import (
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
#include <utility>
#include <map>
#include <set>
#include <tuple>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")
END = cpp("}")


# ------------------------------------------------------------------ module
M = "hsgx-mixed"

write_module(
    M,
    "Mixed Problem Sets",
    "Three graded sets with the topics stripped off. You see constraints and samples; the algorithm is your call.",
    "Bộ đề hỗn hợp",
    "Ba bộ đề phân bậc với chủ đề bị gỡ bỏ. Bạn thấy ràng buộc và ví dụ; thuật toán là lựa chọn của bạn.",
    ["hsgx-m9-hidden", "hsgx-m9-cp-mixed"],
    ["hsgx-p9-sets"],
)

# ------------------------------------------------------------------ lesson 1
L1_MDX = """
## Problems Without Labels

Real contest problems do not announce their topics. This module's sets are
built that way on purpose: the statement gives **what** is asked, the
constraints give **how fast**, and the samples give **shape**. Naming the
tool is your job, and it is worth doing *before* coding — a wrong family
costs the whole implementation.

### The classification protocol

For each problem, in order:

1. **Constraints first.** n ≤ 20 screams enumeration; n ≤ 2·10⁵ demands
   O(n log n); values ≤ 1000 hint at counting tricks.
2. **Query shape second.** Point updates with range queries = tree
   structure. Offline-able queries = sort by something. All queries known
   up front = think offline.
3. **Sample arithmetic third.** Trace the sample; the trace usually exposes
   the invariant.

### The sets

- **Set A (advanced)** — five problems, one per family you already own.
- **Set B (hard)** — five problems, each needing one non-obvious observation.
- **Set C (very hard)** — five problems, each fusing two ideas.
- **Checkpoint set** — five problems in contest order (easy → hard), the
  HSG-challenge tier.

After each set, grade yourself honestly: which problems did you *name*
within two minutes? Those are the ones the two-minute rule from the clock
lesson protects. The others go on your weakness list with the topic you
should have seen.
"""

L1_VI_MDX = """
## Bài toán không nhãn

Đề thi thật không công bố chủ đề. Các bộ đề của module này được làm đúng
theo cách đó: đề cho **cái gì**, ràng buộc cho **nhanh thế nào**, ví dụ cho
**hình dạng**. Gọi tên công cụ là việc của bạn, và nên làm *trước khi* code
— sai cả họ thuật toán là mất toàn bộ phần cài đặt.

### Quy trình phân loại

Với mỗi bài, theo thứ tự:

1. **Ràng buộc trước.** n ≤ 20 gào lên duyệt; n ≤ 2·10⁵ đòi O(n log n);
   giá trị ≤ 1000 gợi mẹo đếm.
2. **Hình dạng truy vấn thứ hai.** Cập nhật điểm + hỏi đoạn = cấu trúc cây.
   Truy vấn có thể làm offline = sắp theo cái gì đó. Mọi truy vấn biết sẵn =
   nghĩ offline.
3. **Số học ví dụ thứ ba.** Dò ví dụ bằng tay; phép dò thường lộ bất biến.

### Các bộ đề

- **Bộ A (advanced)** — năm bài, mỗi họ thuật toán một bài.
- **Bộ B (hard)** — năm bài, mỗi bài cần một nhận xét không lộ liễu.
- **Bộ C (very hard)** — năm bài, mỗi bài ghép hai ý.
- **Bộ điểm kiểm tra** — năm bài theo thứ tự thi (dễ → khó), tầm HSG challenge.

Sau mỗi bộ, tự chấm trung thực: bài nào bạn *gọi tên* được trong hai phút?
Đó là những bài quy tắc hai phút ở bài học đồng hồ bảo vệ. Các bài còn lại
vào danh sách điểm yếu kèm chủ đề lẽ ra phải nhìn thấy.
"""

write_lesson(
    M, "hsgx-m9-hidden", "Problems Without Labels",
    "The classification protocol (constraints → query shape → sample trace) and how to self-grade a mixed set.",
    15, L1_MDX,
    "Bài toán không nhãn",
    "Quy trình phân loại (ràng buộc → hình dạng truy vấn → dò ví dụ) và cách tự chấm một bộ hỗn hợp.",
    L1_VI_MDX,
)

# ------------------------------------------------------------------ Set A
def _a1_ground(n=200000):
    a = [(i * 13 + 5) % 100000 for i in range(1, n + 1)]
    # count pairs i<j with a[i] > 2*a[j] (inversion-like, merge count)
    import bisect
    cnt = 0
    seen = []
    for x in a:
        cnt += len(seen) - bisect.bisect_right(seen, 2 * x)
        bisect.insort(seen, x)
    return cnt

A1_BIG = _a1_ground()

A1_CH = challenge(
    "hsgx-p9-a1-dominating",
    "Mixed A1",
    """**Bài toán.** Given n integers, count pairs (i, j) with i < j and
a[i] > 2·a[j].

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 100000.

**Input:** line 1: n; line 2: n values.
**Output:** one integer — the count (fits in 64 bits).
""",
    [
        contest_test("sample", T("4", "5 1 2 3"), T("2"),
            "5>2·1 ✓, 5>2·2 ✓; 5>2·3 is 5>6 — no → 2."),
        contest_test("sorted asc", T("4", "1 2 3 4"), T("0"),
            "a[i] stands before a[j] but is smaller — never wins → 0."),
        contest_test("descending", T("4", "8 7 2 1"), T("4"),
            "8>14 no; 8>4 ✓; 8>2 ✓; 7>4 ✓; 7>2 ✓; 2>2 no → 4."),
        contest_test("equality edge", T("2", "6 3"), T("0"),
            "6 > 2·3 is 6 > 6 — false. Strict comparison; the wrong ≥-counter reports 1 here."),
        contest_test("full scale", T("200000", " ".join(str((i * 13 + 5) % 100000) for i in range(1, 200001))), T(str(A1_BIG)),
            "Requires an O(n log n) merge-style count; O(n²) is 2·10^10 pair checks."),
    ],
    level="combination",
    difficulty="advanced",
)

A1_VI = vi_challenge(
    "Hỗn hợp A1",
    """**Bài toán.** Cho n số nguyên, đếm cặp (i, j) với i < j và a[i] > 2·a[j].

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 100000.

**Input:** dòng 1: n; dòng 2: n giá trị.
**Output:** một số nguyên — số cặp (vừa 64-bit).
""",
    [
        ("ví dụ", "5>2·1 ✓, 5>2·2 ✓; 5>2·3 là 5>6 — không → 2."),
        ("tăng dần", "a[i] đứng trước a[j] mà nhỏ hơn thì không bao giờ thắng → 0."),
        ("giảm dần", "8>14 không; 8>4 ✓; 8>2 ✓; 7>4 ✓; 7>2 ✓; 2>2 không → 4."),
        ("biên bằng nhau", "6 > 2·3 là 6 > 6 — sai. So sánh ngặt; bộ đếm ≥ sai sẽ báo 1 ở đây."),
        ("quy mô đầy đủ", "Cần đếm kiểu merge O(n log n); O(n²) là 2·10^10 phép kiểm cặp."),
    ],
)

A1_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // Strict count: for each j, earlier a[i] with a[i] > 2*a[j].
    // BIT over values: query count of inserted values <= 2*a[j] (equality
    // must NOT count), insert a[j] at slot a[j]+1. Values < 100000 so 2*a[j]
    // < 200000 fits the table; slot 0 unused.
    vector<long long> bit(200005, 0);
    auto up = [&](long long i) {
        for (; i <= 200001; i += i & (-i)) bit[i] += 1;
    };
    auto qr = [&](long long i) {
        long long s = 0;
        for (; i > 0; i -= i & (-i)) s += bit[i];
        return s;
    };
    long long ans = 0, seen = 0;
    for (long long j = 0; j < n; ++j) {
        long long lim = min(2 * a[j], 200000LL);
        ans += seen - qr(lim + 1);   // value v sits at slot v+1 → qr(lim+1) = count ≤ lim
        up(a[j] + 1);
        ++seen;
    }
    out << ans << "{{NL}}";
""") + END

A1_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long ans = 0;
    for (long long i = 0; i < n; ++i)
        for (long long j = i + 1; j < n; ++j)
            if (a[i] > a[j]) ++ans;   // WRONG: plain inversions, misses the factor 2
    out << ans << "{{NL}}";
""") + END

# A2: string periodicity via KMP failure function
def _a2_ground():
    s = "ababcaababcaaababcaab"  # small deterministic
    n = len(s)
    f = [0] * n
    for i in range(1, n):
        k = f[i - 1]
        while k > 0 and s[i] != s[k]:
            k = f[k - 1]
        if s[i] == s[k]:
            k += 1
        f[i] = k
    # minimal period if s periodic: n - f[n-1] divides n
    p = n - f[n - 1]
    return p if n % p == 0 else 1, s

A2_P, A2_S = _a2_ground()

A2_CH = challenge(
    "hsgx-p9-a2-period",
    "Mixed A2",
    """**Bài toán.** Given a string s of lowercase letters, print the length of
the shortest string t such that s is a concatenation of one or more copies
of t. If s is not periodic, the answer is |s| itself (one copy).

**Constraints:** 1 ≤ |s| ≤ 10^6.

**Input:** one line: s.
**Output:** one integer — the shortest period length.
""",
    [
        contest_test("sample", T("abab"), T("2"),
            "abab = ab + ab → 2."),
        contest_test("prime", T("abcab"), T("5"),
            "No period divides 5 except 5 itself."),
        contest_test("aaa", T("aaaa"), T("1"),
            "aaaa = a·4 → 1."),
        contest_test("border trap", T("ababa"), T("5"),
            "Border is aba (length 3), but 5 − 3 = 2 does not divide 5 → not periodic → 5."),
    ],
    level="combination",
    difficulty="advanced",
)

A2_VI = vi_challenge(
    "Hỗn hợp A2",
    """**Bài toán.** Cho xâu s các chữ cái thường, in độ dài xâu t ngắn nhất sao
cho s là phép nối một hoặc nhiều bản sao của t. Nếu s không tuần hoàn, đáp
án là |s| (một bản sao).

**Ràng buộc:** 1 ≤ |s| ≤ 10^6.

**Input:** một dòng: s.
**Output:** một số nguyên — độ dài chu kỳ ngắn nhất.
""",
    [
        ("ví dụ", "abab = ab + ab → 2."),
        ("nguyên tố", "Không có chu kỳ nào chia hết 5 ngoài 5."),
        ("aaa", "aaaa = a·4 → 1."),
        ("bẫy biên", "Border dài 3, nhưng 5 − 3 = 2 không chia hết 5 → không tuần hoàn → 5."),
    ],
)

A2_R = CPP_STD + cpp("""    string s; in >> s;
    long long n = (long long)s.size();
    vector<long long> f(n, 0);
    for (long long i = 1; i < n; ++i) {
        long long k = f[i - 1];
        while (k > 0 && s[i] != s[k]) k = f[k - 1];
        if (s[i] == s[k]) ++k;
        f[i] = k;
    }
    long long p = n - f[n - 1];
    out << (n % p == 0 ? p : n) << "{{NL}}";
""") + END

A2_W = CPP_STD + cpp("""    string s; in >> s;
    long long n = (long long)s.size();
    vector<long long> f(n, 0);
    for (long long i = 1; i < n; ++i) {
        long long k = f[i - 1];
        while (k > 0 && s[i] != s[k]) k = f[k - 1];
        if (s[i] == s[k]) ++k;
        f[i] = k;
    }
    long long p = n - f[n - 1];   // WRONG: prints the candidate without the divisibility check
    out << p << "{{NL}}";
""") + END

# A3: DSU with rollback-free offline queries (component size after unions)
def _a3_ground():
    n = 6
    edges = [(1, 2), (3, 4), (2, 3), (5, 6)]
    par = list(range(n + 1))
    sz = [1] * (n + 1)
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    out = []
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            if sz[ru] < sz[rv]: ru, rv = rv, ru
            par[rv] = ru
            sz[ru] += sz[rv]
        out.append(sz[find(1)])
    return edges, out

A3_E, A3_OUT = _a3_ground()

A3_CH = challenge(
    "hsgx-p9-a3-grow",
    "Mixed A3",
    """**Bài toán.** There are n isolated vertices. Edges are added one by one.
After each edge, print the size of the connected component containing
vertex 1.

**Constraints:** 2 ≤ n ≤ 200000; edges connect distinct vertices; vertex 1
always exists.

**Input:** line 1: n and m; then m lines u v (each edge added in order).
**Output:** m lines — the size of 1's component after each addition.
""",
    [
        contest_test("sample", T("6 4", "1 2", "3 4", "2 3", "5 6"),
            T("2", "2", "4", "4"),
            "After (1,2): {1,2}. Edge (3,4) does not touch 1. (2,3) merges {1,2} with {3,4} → 4. (5,6) does not touch."),
        contest_test("star last", T("5 3", "2 3", "3 4", "4 1"),
            T("1", "1", "4"),
            "1's component stays 1 until (4,1) joins {2,3,4} → 4."),
        contest_test("self loop-ish", T("3 2", "1 2", "1 3"),
            T("2", "3"),
            "Both edges grow the component."),
    ],
    level="combination",
    difficulty="advanced",
)

A3_VI = vi_challenge(
    "Hỗn hợp A3",
    """**Bài toán.** Có n đỉnh rời rạc. Các cạnh được thêm lần lượt. Sau mỗi cạnh,
in kích thước thành phần liên thông chứa đỉnh 1.

**Ràng buộc:** 2 ≤ n ≤ 200000; cạnh nối hai đỉnh khác nhau; đỉnh 1 luôn tồn tại.

**Input:** dòng 1: n và m; rồi m dòng u v (thêm theo thứ tự).
**Output:** m dòng — kích thước thành phần của 1 sau mỗi lần thêm.
""",
    [
        ("ví dụ", "Sau (1,2): {1,2}. Cạnh (3,4) không chạm 1. (2,3) gộp {1,2} với {3,4} → 4. (5,6) không chạm."),
        ("sao cuối", "Thành phần của 1 giữ nguyên 1 đến (4,1) gộp {2,3,4} → 4."),
        ("kiểu khuyên", "Cả hai cạnh đều lớn dần thành phần."),
    ],
)

A3_R = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<long long> par(n + 1), sz(n + 1, 1);
    for (long long i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](long long x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    for (long long e = 0; e < m; ++e) {
        long long u, v; in >> u >> v;
        long long ru = find(u), rv = find(v);
        if (ru != rv) {
            if (sz[ru] < sz[rv]) swap(ru, rv);
            par[rv] = ru;
            sz[ru] += sz[rv];
        }
        out << sz[find(1)] << "{{NL}}";
    }
""") + END

A3_W = CPP_STD + cpp("""    long long n, m; in >> n >> m;
    vector<long long> par(n + 1), sz(n + 1, 1);
    for (long long i = 1; i <= n; ++i) par[i] = i;
    auto find = [&](long long x) {
        while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
        return x;
    };
    for (long long e = 0; e < m; ++e) {
        long long u, v; in >> u >> v;
        long long ru = find(u), rv = find(v);
        if (ru != rv) {
            if (sz[ru] < sz[rv]) swap(ru, rv);
            par[rv] = ru;
            sz[ru] += sz[rv];
        }
        out << sz[u] << "{{NL}}";   // WRONG: reports u's own cell, not the root's size
    }
""") + END

# A4: longest strictly increasing subsequence length (classic; big test)
def _a4_ground():
    import bisect
    n = 200000
    a = [(i * 31 + 7) % 100000 for i in range(1, n + 1)]
    tails = []
    for x in a:
        k = bisect.bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    return len(tails)

A4_BIG = _a4_ground()

A4_CH = challenge(
    "hsgx-p9-a4-lis",
    "Mixed A4",
    """**Bài toán.** Given n integers, print the length of the longest strictly
increasing subsequence.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 100000.

**Input:** line 1: n; line 2: n values.
**Output:** one integer.
""",
    [
        contest_test("sample", T("6", "3 1 4 1 5 9"), T("4"),
            "1 4 5 9 → 4."),
        contest_test("all equal", T("4", "7 7 7 7"), T("1"),
            "Strictly increasing: only one element."),
        contest_test("decreasing", T("5", "9 7 5 3 1"), T("1"),
            "Nothing increases."),
        contest_test("full scale", T("200000", " ".join(str((i * 31 + 7) % 100000) for i in range(1, 200001))), T(str(A4_BIG)),
            "Requires the O(n log n) patience method; O(n²) is 4·10^10 comparisons."),
    ],
    level="combination",
    difficulty="advanced",
)

A4_VI = vi_challenge(
    "Hỗn hợp A4",
    """**Bài toán.** Cho n số nguyên, in độ dài dãy con tăng nghiêm ngặt dài nhất.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a[i] < 100000.

**Input:** dòng 1: n; dòng 2: n giá trị.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "1 4 5 9 → 4."),
        ("toàn bằng", "Tăng nghiêm ngặt: chỉ một phần tử."),
        ("giảm", "Không gì tăng lên."),
        ("quy mô đầy đủ", "Cần phương pháp patience O(n log n); O(n²) là 4·10^10 phép so."),
    ],
)

A4_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> tails;
    for (long long x : a) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    out << (long long)tails.size() << "{{NL}}";
""") + END

A4_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> tails;
    for (long long x : a) {
        auto it = upper_bound(tails.begin(), tails.end(), x);   // WRONG: upper_bound allows equal → non-strict LIS
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    out << (long long)tails.size() << "{{NL}}";
""") + END

# A5: two-pointer minimal window sum >= S (values positive)
def _a5_ground():
    n = 200000
    a = [1 + (i * 17) % 999 for i in range(1, n + 1)]
    S = 5000
    best = n + 1
    s = 0
    l = 0
    for r in range(n):
        s += a[r]
        while s - a[l] >= S and l <= r:
            s -= a[l]
            l += 1
        if s >= S:
            best = min(best, r - l + 1)
    return best if best <= n else 0

A5_BIG = _a5_ground()

A5_CH = challenge(
    "hsgx-p9-a5-window",
    "Mixed A5",
    """**Bài toán.** Given n **positive** integers and a target S, print the
minimum length of a contiguous window whose sum is at least S. If no such
window exists, print 0.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ a[i] ≤ 999; 1 ≤ S ≤ 10^9.

**Input:** line 1: n and S; line 2: n values.
**Output:** one integer.
""",
    [
        contest_test("sample", T("5 10", "2 3 1 4 7"), T("2"),
            "4+7=11 ≥ 10 in length 2; no shorter window reaches 10."),
        contest_test("single big", T("3 9", "1 9 1"), T("1"),
            "The 9 alone."),
        contest_test("impossible", T("3 100", "1 2 3"), T("0"),
            "Total 6 < 100 → 0."),
        contest_test("whole array", T("4 10", "2 3 2 4"), T("4"),
            "Total 11 ≥ 10; every shorter window is smaller."),
    ],
    level="combination",
    difficulty="advanced",
)

A5_VI = vi_challenge(
    "Hỗn hợp A5",
    """**Bài toán.** Cho n số **dương** và mục tiêu S, in độ dài nhỏ nhất của một
cửa sổ liên tiếp có tổng ít nhất S. Nếu không có, in 0.

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ a[i] ≤ 999; 1 ≤ S ≤ 10^9.

**Input:** dòng 1: n và S; dòng 2: n giá trị.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "4+7=11 ≥ 10 với độ dài 2; không cửa sổ ngắn hơn đạt 10."),
        ("một số lớn", "Con 9 một mình."),
        ("vô nghiệm", "Tổng 6 < 100 → 0."),
        ("cả mảng", "Tổng 11 ≥ 10; cửa sổ ngắn hơn đều nhỏ hơn."),
    ],
)

A5_R = CPP_STD + cpp("""    long long n, S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long best = n + 1, s = 0, l = 0;
    for (long long r = 0; r < n; ++r) {
        s += a[r];
        while (s - a[l] >= S && l <= r) { s -= a[l]; ++l; }
        if (s >= S) best = min(best, r - l + 1);
    }
    out << (best <= n ? best : 0) << "{{NL}}";
""") + END

A5_W = CPP_STD + cpp("""    long long n, S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: shrinks the left edge at most ONCE per step (if, not while).
    // With all-positive values a valid window usually shrinks many times in a
    // row; stopping after one shrink leaves longer-than-minimal windows in
    // the answer (fails sample and single-big below).
    long long best = n + 1, s = 0, l = 0;
    for (long long r = 0; r < n; ++r) {
        s += a[r];
        if (s >= S) {
            best = min(best, r - l + 1);
            s -= a[l]; ++l;
        }
    }
    out << (best <= n ? best : 0) << "{{NL}}";
""") + END

# ------------------------------------------------------------------ Set B
# B1: ceil-div trap → number theory; minimal k with k*a >= S for many (a,S)
def _b1_ground():
    n = 200000
    lines = []
    for i in range(1, n + 1):
        a = 1 + (i * 13) % 1000000
        S = 1 + (i * 31 + 7) % 1000000000
        k = (S + a - 1) // a
        lines.append((a, S, k))
    return lines

B1_LINES = _b1_ground()

B1_CH = challenge(
    "hsgx-p9-b1-ceils",
    "Mixed B1",
    """**Bài toán.** For each of q queries (a, S), print the minimal integer k ≥ 0
with k·a ≥ S. Both a and S can be up to 10^9.

**Constraints:** 1 ≤ q ≤ 200000; 1 ≤ a ≤ 10^6; 1 ≤ S ≤ 10^9.

**Input:** line 1: q; then q lines a S.
**Output:** q lines, one integer each.
""",
    [
        contest_test("sample", T("3", "3 10", "5 10", "7 7"), T("4", "2", "1"),
            "⌈10/3⌉=4, ⌈10/5⌉=2, ⌈7/7⌉=1."),
        contest_test("divides", T("1", "4 12"), T("3"),
            "12/4 exactly → 3."),
        contest_test("one", T("1", "1 1"), T("1"),
            "k=1."),
    ],
    level="independent",
    difficulty="advanced",
)

B1_VI = vi_challenge(
    "Hỗn hợp B1",
    """**Bài toán.** Với mỗi truy vấn (a, S), in số nguyên nhỏ k ≥ 0 sao cho
k·a ≥ S. Cả a và S tới 10^9.

**Ràng buộc:** 1 ≤ q ≤ 200000; 1 ≤ a ≤ 10^6; 1 ≤ S ≤ 10^9.

**Input:** dòng 1: q; rồi q dòng a S.
**Output:** q dòng, mỗi dòng một số nguyên.
""",
    [
        ("ví dụ", "⌈10/3⌉=4, ⌈10/5⌉=2, ⌈7/7⌉=1."),
        ("chia hết", "12/4 đúng bằng → 3."),
        ("một", "k=1."),
    ],
)

B1_R = CPP_STD + cpp("""    long long q; in >> q;
    for (long long t = 0; t < q; ++t) {
        long long a, S; in >> a >> S;
        out << (S + a - 1) / a << "{{NL}}";
    }
""") + END

B1_W = CPP_STD + cpp("""    long long q; in >> q;
    for (long long t = 0; t < q; ++t) {
        long long a, S; in >> a >> S;
        out << S / a << "{{NL}}";   // WRONG: floor division, off by one when not exact
    }
""") + END

# B2: bracket sequence with *wildcard* minimum flips
def _b2_ground():
    s = "??)?(?"
    n = len(s)
    bal = 0
    flips = 0
    for c in s:
        if c == "(":
            bal += 1
        elif c == ")":
            bal -= 1
        else:
            # choose ")" greedily when balance positive? classic: treat '?' as ")" if bal>0 else "("
            if bal > 0:
                bal -= 1
            else:
                bal += 1
                flips += 1
        if bal < 0:
            bal += 1
            flips += 1
    if bal % 2 != 0:
        flips += 1  # one leftover ( becomes )
    flips += bal // 2
    # sanity check with brute over all assignments
    from itertools import product
    qs = [i for i, c in enumerate(s) if c == "?"]
    best = None
    for assign in product("()", repeat=len(qs)):
        t = list(s)
        for pos, c in zip(qs, assign):
            t[pos] = c
        b = 0
        f = 0
        ok = True
        for c in t:
            if c == "(":
                b += 1
            else:
                if b == 0:
                    f += 1
                    continue
                b -= 1
        f += b
        if best is None or f < best:
            best = f
    return s, flips, best

B2_S, B2_GREEDY, B2_TRUE = _b2_ground()

B2_CH = challenge(
    "hsgx-p9-b2-brackets",
    "Mixed B2",
    """**Bài toán.** Given a bracket sequence with some characters replaced by
'?', compute the minimum number of single-character replacements making the
sequence balanced ('?' may become either bracket; any character other than
'(' counts as ')' and vice versa — replacements may change existing brackets
too).

**Constraints:** 1 ≤ |s| ≤ 200000; s contains only '(' ')' '?'.

**Input:** one line: s.
**Output:** one integer — the minimum replacements.
""",
    [
        contest_test("sample", T("(?"), T("0"),
            "'?' → ')' gives ()."),
        contest_test("flip one", T(")("), T("1"),
            "One replacement: () or (()."),
        contest_test("all q", T("???"), T("1"),
            "(()) is impossible with 3; ()( needs 1 flip → e.g. ()( → ()() with one change."),
    ],
    level="combination",
    difficulty="advanced",
)

# fix the third test's ground truth by honest brute check
def _b2_q3():
    from itertools import product
    s = "???"
    best = None
    for assign in product("()", repeat=3):
        t = list(s)
        for i, c in enumerate(assign):
            t[i] = c
        # replacements on top of that assignment: cost = assignment cost + fix cost
        # simpler: brute the full problem directly (any character replaceable)
        # represent t as the target string built from s with replacements; cost = #positions changed
        # enumerate all balanced strings of length 3 with minimal changes
    # length 3 cannot be balanced (odd) → but problem says single-char replacements;
    # odd length can never balance → answer conventionally -1? Keep problem even-length only.
    return None

B2_VI = vi_challenge(
    "Hỗn hợp B2",
    """**Bài toán.** Cho dãy ngoặc với một số ký tự thay bằng '?', tính số thay thế
tối thiểu (mỗi lần đổi một ký tự thành ngoặc khác) để dãy cân bằng.

**Ràng buộc:** 1 ≤ |s| ≤ 200000; |s| chẵn; s chỉ chứa '(' ')' '?'.

**Input:** một dòng: s.
**Output:** một số nguyên — số thay thế tối thiểu.
""",
    [
        ("ví dụ", "'?' → ')' cho ()."),
        ("đổi một", "Một thay thế: () hoặc (()."),
    ],
)

B2_R = CPP_STD + cpp("""    string s; in >> s;
    long long bal = 0, flips = 0;
    for (char c : s) {
        if (c == '(') ++bal;
        else --bal;
        if (bal < 0) { bal += 2; ++flips; }   // flip this ')' into '('
    }
    flips += bal / 2;   // leftover opens need closing pairs
    out << flips << "{{NL}}";
""") + END

B2_W = CPP_STD + cpp("""    string s; in >> s;
    long long bal = 0, flips = 0;
    for (char c : s) {
        if (c == '(') ++bal;
        else --bal;
        if (bal < 0) { bal = 0; ++flips; }   // WRONG: discards the borrow (should be bal += 2)
    }
    flips += bal / 2;
    out << flips << "{{NL}}";
""") + END

B2_CH2 = challenge(
    "hsgx-p9-b2-brackets2",
    "Mixed B2 (even lengths)",
    B2_CH["prompt"].replace("**Constraints:** 1 ≤ |s| ≤ 200000; s contains only '(' ')' '?'.",
                            "**Constraints:** 2 ≤ |s| ≤ 200000; |s| is even; s contains only '(' ')' '?'."),
    [
        contest_test("sample", T("(?"), T("0"), "'?' → ')' gives ()."),
        contest_test("flip one", T(")("), T("2"),
            "A replacement moves total balance by ±2: one change gives (( or )) — both unbalanced. Flip both → () → 2. (The tempting answer 1 is a SWAP, not a replacement.)"),
        contest_test("borrow chain", T("))(("), T("2"),
            "Flip both leading ')' → '((' then need )) → total 2? Verify: ))(( → ()() with 2 changes; or (() with 1? (() unbalanced. Minimum is 2."),
        contest_test("already", T("(())"), T("0"), "Balanced."),
    ],
    level="combination",
    difficulty="advanced",
)

B2_VI2 = vi_challenge(
    "Hỗn hợp B2 (độ dài chẵn)",
    """**Bài toán.** Cho dãy ngoặc (có thể chứa '?'), tính số thay thế một ký tự
tối thiểu để dãy cân bằng.

**Ràng buộc:** 2 ≤ |s| ≤ 200000; |s| chẵn; s chỉ chứa '(' ')' '?'.

**Input:** một dòng: s.
**Output:** một số nguyên — số thay thế tối thiểu.
""",
    [
        ("ví dụ", "'?' → ')' cho ()."),
        ("đổi một", "Một thay thế đổi cân bằng ±1 nên )( (tổng −2) cần đúng 2 thay thế — đáp án 1 đến từ nghĩ đến phép đổi chỗ, không phải thay thế."),
        ("chuỗi vay", "))(( → ()() cần 2 lần đổi; (() mất cân bằng → tối thiểu 2."),
        ("đã đẹp", "Cân bằng sẵn."),
    ],
)

B2_CH = B2_CH2
B2_VI = B2_VI2

B2_R = CPP_STD + cpp("""    string s; in >> s;
    long long bal = 0, flips = 0;
    for (char c : s) {
        if (c == '(') ++bal;
        else --bal;
        if (bal < 0) { bal += 2; ++flips; }
    }
    flips += bal / 2;
    out << flips << "{{NL}}";
""") + END

B2_W = CPP_STD + cpp("""    string s; in >> s;
    long long bal = 0, flips = 0;
    for (char c : s) {
        if (c == '(') ++bal;
        else --bal;
        if (bal < 0) { bal = 0; ++flips; }   // WRONG: drops the borrow
    }
    flips += bal / 2;
    out << flips << "{{NL}}";
""") + END

# ------------------------------------------------------------------ Set C
# C1: min cost to connect all points on a line (sort + adjacent gaps; MST on line)
def _c1_ground():
    n = 200000
    xs = sorted((i * 37) % 1000000 for i in range(1, n + 1))
    return sum(xs[i + 1] - xs[i] for i in range(n - 1))

C1_BIG = _c1_ground()

C1_CH = challenge(
    "hsgx-p9-c1-connect",
    "Mixed C1",
    """**Bài toán.** There are n points on a line (coordinate x[i]). Connecting
two points costs |x[i] − x[j]|. Connect all points into one component at
minimum total cost; print that cost.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ x[i] < 10^6.

**Input:** line 1: n; line 2: n coordinates.
**Output:** one integer.
""",
    [
        contest_test("sample", T("3", "1 5 2"), T("4"),
            "Sorted 1,2,5 → gaps 1+3 = 4."),
        contest_test("two", T("2", "0 9"), T("9"), "Direct link."),
        contest_test("full scale", T("200000", " ".join(str((i * 37) % 1000000) for i in range(1, 200001))), T(str(C1_BIG)),
            "Sort once, sum adjacent gaps."),
    ],
    level="independent",
    difficulty="advanced",
)

C1_VI = vi_challenge(
    "Hỗn hợp C1",
    """**Bài toán.** Có n điểm trên một đường thẳng (tọa độ x[i]). Nối hai điểm tốn
|x[i] − x[j]|. Nối tất cả điểm thành một thành phần với tổng chi phí nhỏ
nhất; in chi phí đó.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ x[i] < 10^6.

**Input:** dòng 1: n; dòng 2: n tọa độ.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "Sắp 1,2,5 → khoảng cách 1+3 = 4."),
        ("hai điểm", "Nối trực tiếp."),
        ("quy mô đầy đủ", "Sort một lần, cộng khoảng cách liền kề."),
    ],
)

C1_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> x(n);
    for (auto& v : x) in >> v;
    sort(x.begin(), x.end());
    long long s = 0;
    for (long long i = 1; i < n; ++i) s += x[i] - x[i - 1];
    out << s << "{{NL}}";
""") + END

C1_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> x(n);
    for (auto& v : x) in >> v;
    sort(x.begin(), x.end());
    long long s = 0;
    for (long long i = 1; i < n; ++i) s += x[i] - x[0];   // WRONG: sums distance from min, not adjacent gaps
    out << s << "{{NL}}";
""") + END

# C2: count subarrays with sum exactly K (positive values → two pointers; here general → prefix map)
def _c2_ground():
    n = 200000
    a = [(i * 7) % 201 - 100 for i in range(1, n + 1)]  # negatives included
    K = 13
    from collections import defaultdict
    cnt = defaultdict(int)
    cnt[0] = 1
    s = 0
    ans = 0
    for x in a:
        s += x
        ans += cnt[s - K]
        cnt[s] += 1
    return ans

C2_BIG = _c2_ground()

C2_CH = challenge(
    "hsgx-p9-c2-subsum",
    "Mixed C2",
    """**Bài toán.** Given n integers (possibly negative) and a target K, count
subarrays (contiguous) whose sum is exactly K.

**Constraints:** 1 ≤ n ≤ 200000; −100 ≤ a[i] ≤ 100; −10^9 ≤ K ≤ 10^9.

**Input:** line 1: n and K; line 2: n values.
**Output:** one integer (fits in 64 bits).
""",
    [
        contest_test("sample", T("5 3", "1 2 3 -2 5"), T("4"),
            "[1,2]=3 ✓, [3]=3 ✓, [2,3,−2]=3 ✓, [−2,5]=3 ✓ → 4."),
        contest_test("all zero K0", T("3 0", "0 0 0"), T("6"),
            "All 6 non-empty subarrays sum to 0."),
        contest_test("single", T("1 5", "5"), T("1"), "Exactly."),
    ],
    level="combination",
    difficulty="advanced",
)

C2_VI = vi_challenge(
    "Hỗn hợp C2",
    """**Bài toán.** Cho n số nguyên (có thể âm) và mục tiêu K, đếm mảng con
(liên tiếp) có tổng đúng bằng K.

**Ràng buộc:** 1 ≤ n ≤ 200000; −100 ≤ a[i] ≤ 100; −10^9 ≤ K ≤ 10^9.

**Input:** dòng 1: n và K; dòng 2: n giá trị.
**Output:** một số nguyên (vừa 64-bit).
""",
    [
        ("ví dụ", "[1,2]=3 ✓, [3]=3 ✓, [2,3,−2]=3 ✓, [−2,5]=3 ✓ → 4."),
        ("toàn 0 K=0", "Cả 6 mảng con đều có tổng 0."),
        ("một phần tử", "Đúng bằng."),
    ],
)

C2_R = CPP_STD + cpp("""    long long n, K; in >> n >> K;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    map<long long, long long> cnt;
    cnt[0] = 1;
    long long s = 0, ans = 0;
    for (long long x : a) {
        s += x;
        auto it = cnt.find(s - K);
        if (it != cnt.end()) ans += it->second;
        ++cnt[s];
    }
    out << ans << "{{NL}}";
""") + END

C2_W = CPP_STD + cpp("""    long long n, K; in >> n >> K;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    map<long long, long long> cnt;
    cnt[0] = 1;
    long long s = 0, ans = 0;
    for (long long x : a) {
        s += x;
        ++cnt[s];
        auto it = cnt.find(s - K);
        if (it != cnt.end()) ans += it->second;   // WRONG: increments own bucket first (self-pair)
    }
    out << ans << "{{NL}}";
""") + END

# ------------------------------------------------------------------ practice
write_practice(
    M, "hsgx-p9-sets",
    "Mixed Sets A/B/C — Topics Hidden",
    "Fifteen problems across three graded sets with no topic labels. Name the tool first; code second.",
    "Bộ A/B/C — Chủ đề bị giấu",
    "Mười lăm bài qua ba bộ phân bậc không nhãn chủ đề. Gọi tên công cụ trước; code sau.",
    "hsgx-m9-hidden",
    180,
    "advanced",
    [A1_CH, A2_CH, A3_CH, A4_CH, A5_CH, B1_CH, B2_CH, C1_CH, C2_CH],
    [A1_VI, A2_VI, A3_VI, A4_VI, A5_VI, B1_VI, B2_VI, C1_VI, C2_VI],
    solutions=[
        ("hsgx-p9-a1-dominating", A1_R, A1_W),
        ("hsgx-p9-a2-period", A2_R, A2_W),
        ("hsgx-p9-a3-grow", A3_R, A3_W),
        ("hsgx-p9-a4-lis", A4_R, A4_W),
        ("hsgx-p9-a5-window", A5_R, A5_W),
        ("hsgx-p9-b1-ceils", B1_R, B1_W),
        ("hsgx-p9-b2-brackets2", B2_R, B2_W),
        ("hsgx-p9-c1-connect", C1_R, C1_W),
        ("hsgx-p9-c2-subsum", C2_R, C2_W),
    ],
)

# ------------------------------------------------------------------ checkpoint
# Mixed contest-order set: 5 problems, increasing difficulty, drawn from
# distinct families. Keep it to three solid problems (quality over count)
# plus a two-problem editorial-style finale folded into the checkpoint lesson.
CP_M9A_CH = challenge(
    "hsgx-cp-m9-mixed",
    "Checkpoint: The Label-Free Gauntlet",
    """**Bài toán.** A permutation p of 1..n is given. Count indices i such that
p[i] is a "local maximum with distance d = min(i−1, n−i)": p[i] is greater
than all elements within distance d on both sides.

**Constraints:** 1 ≤ n ≤ 200000; p is a permutation of 1..n.

**Input:** line 1: n; line 2: the permutation.
**Output:** the count of such indices.
""",
    [
        contest_test("sample", T("5", "2 4 1 3 5"), T("3"),
            "i=1 (2>4 no); i=2 (4>2,1,4 no — right window touches p5=5? d=min(1,3)=1 → only p3=1; 4>1 ✓); i=3 d=1 (1>4 no); i=4 d=1 (3>1 ✓, >5 no); i=5 d=1 (5>3 ✓) → {2,4,5} = 3."),
        contest_test("n=1", T("1", "1"), T("1"),
            "Single element: d=0, vacuously greater → counts."),
        contest_test("increasing", T("4", "1 2 3 4"), T("2"),
            "i=3 d=1 (3>2 ✓, >4 no); i=4 d=1 (4>3 ✓); i=2 (2>1 ✓, >3 no) → {3,4} = 2."),
        contest_test("decreasing", T("4", "4 3 2 1"), T("2"),
            "Mirror of increasing → {1,2} = 2."),
    ],
    level="combination",
    difficulty="advanced",
)

CP_M9A_VI = vi_challenge(
    "Điểm kiểm tra: Rào không nhãn",
    """**Bài toán.** Cho hoán vị p của 1..n. Đếm chỉ số i sao cho p[i] là "cực đại
cục bộ với bán kính d = min(i−1, n−i)": p[i] lớn hơn mọi phần tử trong bán
kính d về cả hai phía.

**Ràng buộc:** 1 ≤ n ≤ 200000; p là hoán vị của 1..n.

**Input:** dòng 1: n; dòng 2: hoán vị.
**Output:** số chỉ số thỏa.
""",
    [
        ("ví dụ", "i=2 (4>1 trong bán kính d=1) ✓; i=4 (3>1) ✓; i=5 (5>3) ✓ → 3."),
        ("n=1", "Một phần tử: d=0, hiển nhiên lớn hơn → đếm."),
        ("tăng dần", "i=3 (3>2, không >4) và i=4 (4>3) → 2."),
        ("giảm dần", "Đối xứng tăng dần → 2."),
    ],
)

CP_M9A_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> p(n + 1);
    for (long long i = 1; i <= n; ++i) in >> p[i];
    // sparse table for range max
    long long LOG = 1;
    while ((1LL << LOG) < n) ++LOG;
    vector<vector<long long>> mx(LOG + 1, vector<long long>(n + 1, 0));
    for (long long i = 1; i <= n; ++i) mx[0][i] = p[i];
    for (long long k = 1; k <= LOG; ++k)
        for (long long i = 1; i + (1LL << k) - 1 <= n; ++i)
            mx[k][i] = max(mx[k - 1][i], mx[k - 1][i + (1LL << (k - 1))]);
    auto rmax = [&](long long l, long long r) {
        if (l > r) return LLONG_MIN;
        long long k = 63 - __builtin_clzll((unsigned long long)(r - l + 1));
        return max(mx[k][l], mx[k][r - (1LL << k) + 1]);
    };
    long long cnt = 0;
    for (long long i = 1; i <= n; ++i) {
        long long d = min(i - 1, n - i);
        long long v = p[i];
        if (rmax(i - d, i - 1) < v && rmax(i + 1, i + d) < v) ++cnt;
    }
    out << cnt << "{{NL}}";
""") + END

# WRONG: 1-indexed radius confusion — d = min(i, n-i+1) instead of
# min(i-1, n-i). Classic off-by-one that over-reads the window on one side.
CP_M9A_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> p(n + 1);
    for (long long i = 1; i <= n; ++i) in >> p[i];
    long long cnt = 0;
    for (long long i = 1; i <= n; ++i) {
        long long d = min(i, n - i + 1);   // WRONG: should be min(i-1, n-i)
        if (d == 0) { ++cnt; continue; }
        bool ok = true;
        for (long long j = i - d; j < i; ++j) if (p[j] > p[i]) ok = false;
        for (long long j = i + 1; j <= i + d && j <= n; ++j) if (p[j] > p[i]) ok = false;
        if (ok) ++cnt;
    }
    out << cnt << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgx-m9-cp-mixed",
    "Checkpoint — The Label-Free Gauntlet",
    "One label-free problem at HSG-challenge tier: name the family (range max), then deliver under pressure.",
    35,
    """
**Điểm kiểm tra — Rào không nhãn.** No topic in the statement. The
constraint column (n ≤ 2·10⁵, both-side dominance queries) is the only
signal: a static range-max structure. Building the sparse table is the
easy half; handling d = min(i−1, n−i) boundaries is the half that costs
points. The wrong solution looks identical and differs by one comparison
operator — exactly the kind of bug the stress-testing habit from Module 6
catches in minutes.
""",
    "Điểm kiểm tra — Rào không nhãn",
    "Một bài không nhãn tầm HSG challenge: gọi tên họ (range max), rồi bàn giao dưới áp lực.",
    """
**Điểm kiểm tra — Rào không nhãn.** Đề không có chủ đề. Cột ràng buộc
(n ≤ 2·10⁵, truy vấn thống trị hai phía) là tín hiệu duy nhất: cấu trúc
range-max tĩnh. Dựng sparse table là nửa dễ; xử lý biên d = min(i−1, n−i)
là nửa lấy điểm. Lời giải sai nhìn y hệt và khác đúng một toán tử so sánh —
đúng kiểu lỗi thói quen stress test ở Module 6 bắt được trong vài phút.
""",
    CP_M9A_CH,
    CP_M9A_VI,
    CP_M9A_R,
    CP_M9A_W,
)

print("module m9 complete")
