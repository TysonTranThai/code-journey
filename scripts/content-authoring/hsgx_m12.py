#!/usr/bin/env python3
"""HSG Intensive — Module 12: hsgx-final (Final Challenge Pack + course files).

The end-of-course gauntlet: seven hardest original problems (every numeric
truth brute-verified in Python at import time), a reference-pack lesson
(checklists + C++ contest template), plus the course-level registration
files (course.json / course.vi.json) and the track.json append.

Conventions (m9 style): local T()/cpp()/CPP_STD; explicit includes;
per-line outputs get per-line wants; all ground truths computed + asserted.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgx import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge, contest_test

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
#include <queue>
#include <functional>
#include <climits>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")
END = cpp("}")


# ------------------------------------------------------------------ module
M = "hsgx-final"

write_module(
    M,
    "Final Challenge Pack",
    "The hardest problems of the course plus the reference pack: selection guides, checklists, and the C++ contest template you should have memorized by now.",
    "Bộ Thử Thách Cuối",
    "Những bài khó nhất của khóa học cùng bộ tài liệu tham khảo: cẩm nang chọn thuật toán, danh mục kiểm tra, và khuôn C++ thi đấu bạn phải thuộc lòng lúc này.",
    ["hsgx-m12-reference-pack", "hsgx-cp-m12-capstone"],
    ["hsgx-p12-final-pack"],
)


# ------------------------------------------------------------------ lesson 1: reference pack
L1_MDX = """
## The Reference Pack

Everything below is deliberately terse. It is the material to reread the
night before a contest.

### Algorithm selection guide

| You see | Reach for |
| --- | --- |
| n ≤ 20 | bitmask enumeration, meet-in-the-middle |
| n ≤ 500 | O(n³) interval/DP |
| n ≤ 5000, q ≤ 5000 | O(nq) or O((n+q)√n) |
| n ≤ 2·10⁵ | O(n log n): sort, heap, tree structure |
| offline queries | sort by one coordinate, sweep |
| range update + range query | lazy segment tree |
| prefix sums with updates | Fenwick |
| connectivity over time | DSU (offline) or link-cut |
| "minimum maximum" / "maximum minimum" | binary search the answer |
| counting with digit structure | digit DP |
| subarray sums with negatives | prefix map |
| subarray sums, positives only | two pointers |
| strings, repeated patterns | KMP / hashing / trie |
| reachability closure | SCC condensation + DAG DP |

### Complexity cheat sheet (safe limits, ~10⁹ simple ops budget)

O(n) 10⁸ — O(n log n) 2·10⁵ — O(n√n) 5·10⁴ — O(n²) 3·10³ — O(2^n) 24 —
O(n·2^(n/2)) 40 (meet in the middle) — O(n³) 300.

### Debugging checklist (in order)

1. Reread the statement — output format, order, off-by-one in constraints.
2. Test the sample by hand, tracing variables, not staring.
3. Check the boundary: n = 1, all equal, all negative, maximum values.
4. Overflow: where do two 10⁹ values multiply or add?
5. Random small tests against a brute you trust (Module 6 harness).
6. Only then: print-debug the smallest failing case.

### Before-submit checklist

- [ ] Sample passes **byte-exact** (trailing newlines count).
- [ ] Bounds: every array sized for the true maximum, 1-indexing consistent.
- [ ] `long long` where two maximums can meet.
- [ ] Reading order matches the statement (r before c!).
- [ ] Special cases from the constraints line actually appear in your tests.

### Common HSG mistakes

Silent int overflow; reading the input in the wrong units (0-index vs
1-index); assuming distinct values; assuming sorted input; greedy without
an exchange argument; forgetting modulo on negative intermediates; printing
an extra space.

### C++ contest template

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

void solve(istream& in, ostream& out) {
    // read, compute, print — the sandbox harness calls this
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    solve(cin, cout);
    return 0;
}
```

Fast I/O, one solve function, 64-bit by default for anything that can grow.
The boilerplate of every challenge in this course is this template with the
solve body stripped — you have been filling it in all along.
"""

L1_VI_MDX = """
## Bộ Tài Liệu Tham Khảo

Mọi thứ bên dưới cố tình súc tích. Đây là phần nên đọc lại đêm trước vòng thi.

### Cẩm nang chọn thuật toán

| Bạn thấy | Chọn |
| --- | --- |
| n ≤ 20 | duyệt bitmask, meet-in-the-middle |
| n ≤ 500 | interval/DP O(n³) |
| n ≤ 5000, q ≤ 5000 | O(nq) hoặc O((n+q)√n) |
| n ≤ 2·10⁵ | O(n log n): sort, heap, cấu trúc cây |
| truy vấn offline | sắp theo một tọa độ, quét |
| cập nhật đoạn + hỏi đoạn | segment tree lười |
| prefix sum có cập nhật | Fenwick |
| liên thông theo thời gian | DSU (offline) hoặc link-cut |
| "tối thiểu giá trị lớn nhất" / "tối đa giá trị nhỏ nhất" | chảy nhị phân đáp án |
| đếm có cấu trúc chữ số | digit DP |
| tổng mảng con có số âm | map prefix |
| tổng mảng con, chỉ dương | two pointers |
| xâu, mẫu lặp lại | KMP / băm / trie |
| đóng khẩu độ với tới | SCC rút gọn + DP DAG |

### Bảng phức tạp (ngân sách an toàn, ~10⁹ phép đơn giản)

O(n) 10⁸ — O(n log n) 2·10⁵ — O(n√n) 5·10⁴ — O(n²) 3·10³ — O(2^n) 24 —
O(n·2^(n/2)) 40 (meet in the middle) — O(n³) 300.

### Danh mục gỡ lỗi (theo thứ tự)

1. Đọc lại đề — định dạng output, thứ tự, lệch một trong ràng buộc.
2. Dò ví dụ bằng tay, lần theo biến, đừng nhìn chằm chằm.
3. Kiểm tra biên: n = 1, toàn bằng, toàn âm, giá trị cực đại.
4. Tràn số: chỗ nào hai giá trị 10⁹ nhân hoặc cộng nhau?
5. Test nhỏ ngẫu nhiên đối chiếu brute đáng tin (bộ harness Module 6).
6. Rồi mới đến: print-debug ca nhỏ nhất gây lỗi.

### Danh mục trước khi nộp

- [ ] Ví dụ pass **đúng từng byte** (kể cả xuống dòng).
- [ ] Cỡ mảng: mọi mảng đủ cho cực đại thật, đánh chỉ số 1 nhất quán.
- [ ] `long long` nơi hai giá trị cực đại có thể gặp nhau.
- [ ] Thứ tự đọc khớp đề (r trước c!).
- [ ] Các ca đặc biệt ở dòng ràng buộc thực sự xuất hiện trong test của bạn.

### Lỗi thường gặp HSG

Tràn int âm thầm; đọc đầu vào sai đơn vị (0-index vs 1-index); giả định giá
trị đôi một khác nhau; giả định đầu vào có sắp sẵn; tham lam không có lập
luận đổi chỗ; quên modulo trên giá trị trung gian âm; in thừa một dấu cách.

### Khuôn C++ thi đấu

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

void solve(istream& in, ostream& out) {
    // đọc, tính, in — harness sandbox gọi hàm này
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    solve(cin, cout);
    return 0;
}
```

I/O nhanh, một hàm solve, 64-bit mặc định cho mọi thứ có thể lớn. Boilerplate
của mọi thử thách trong khóa học chính là khuôn này với phần thân solve bị
gỡ — bạn đã lấp nó suốt khóa học.
"""

write_lesson(
    M, "hsgx-m12-reference-pack", "The Reference Pack",
    "Selection guides, complexity limits, debugging and submission checklists, common mistakes, and the C++ contest template.",
    12, L1_MDX,
    "Bộ Tài Liệu Tham Khảo",
    "Cẩm nang chọn thuật toán, giới hạn phức tạp, danh mục gỡ lỗi và nộp bài, lỗi thường gặp, và khuôn C++ thi đấu.",
    L1_VI_MDX,
)


# ================================================================ F1
# max sum subarray with at most k distinct values (two pointers + map)
def _f1_truth(a, k):
    from collections import defaultdict
    cnt = defaultdict(int)
    distinct = 0
    s = 0
    best = 0
    l = 0
    for r, x in enumerate(a):
        if cnt[x] == 0:
            distinct += 1
        cnt[x] += 1
        s += x
        while distinct > k:
            y = a[l]
            cnt[y] -= 1
            if cnt[y] == 0:
                distinct -= 1
            s -= y
            l += 1
        best = max(best, s)
    return best


F1_S = _f1_truth([1, 2, 1, 3, 4], 2)
assert F1_S == 7, f"F1 sample {F1_S}"  # [3,4]

F1_TRAP = _f1_truth([5, 1, 1, 5], 2)
assert F1_TRAP == 12, f"F1 trap {F1_TRAP}"  # whole array: only 2 distinct values

F1_BIG_ARR = [((i * 977) % 5000) + 1 for i in range(1, 200001)]
F1_BIG = _f1_truth(F1_BIG_ARR, 40)

F1_CH = challenge(
    "hsgx-f1-showcase",
    "Final 1: The Showcase",
    """**Bài toán.** A shop displays n items in a row; item i has value a[i]. A
window is a contiguous set of items containing **at most k distinct values**
(distinct by value, not by position). Find the maximum total value of a
non-empty window.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ k ≤ n; 1 ≤ a[i] ≤ 5000.

**Input:** line 1: n, k; line 2: n values.
**Output:** one integer.
""",
    [
        contest_test("sample", T("5 2", "1 2 1 3 4"), T("7"),
            "Window [3,4]: two distinct values, sum 7."),
        contest_test("k covers all", T("4 5", "9 1 9 1"), T("20"), "Everything fits."),
        contest_test("distinct trap", T("4 2", "5 1 1 5"), T("12"),
            "The whole array has exactly 2 distinct values → 12; an at-most-k-ELEMENTS misreading stops at 6."),
        contest_test("single", T("1 1", "6"), T("6"), "One item."),
        contest_test("full scale", T(f"200000 40", " ".join(map(str, F1_BIG_ARR))), T(str(F1_BIG)),
            "Two pointers with a value-count map; O(n²) windows are 2·10^10."),
    ],
    level="combination",
    difficulty="advanced",
)

F1_VI = vi_challenge(
    "Final 1: Cửa Hàng Trưng Bày",
    """**Bài toán.** Cửa hàng trưng bày n món thành hàng; món i có giá trị a[i].
Một cửa sổ là tập món liên tiếp chứa **nhiều nhất k giá trị phân biệt**
(phân biệt theo giá trị, không theo vị trí). Tìm tổng giá trị lớn nhất của
một cửa sổ không rỗng.

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ k ≤ n; 1 ≤ a[i] ≤ 5000.

**Input:** dòng 1: n, k; dòng 2: n giá trị.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "Cửa sổ [3,4]: hai giá trị phân biệt, tổng 7."),
        ("k phủ hết", "Mọi thứ vừa."),
        ("bẫy phân biệt", "Cả mảng có đúng 2 giá trị phân biệt → 12; đọc nhầm 'nhiều nhất k phần tử' sẽ dừng ở 6."),
        ("món đơn", "Một món."),
        ("quy mô đầy đủ", "Two pointers với map đếm giá trị; O(n²) là 2·10^10 cửa sổ."),
    ],
)

F1_R = CPP_STD + cpp("""    long long n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    map<long long, long long> cnt;
    long long distinct = 0, s = 0, best = 0, l = 0;
    for (long long r = 0; r < n; ++r) {
        if (cnt[a[r]]++ == 0) ++distinct;
        s += a[r];
        while (distinct > k) {
            if (--cnt[a[l]] == 0) --distinct;
            s -= a[l];
            ++l;
        }
        best = max(best, s);
    }
    out << best << "{{NL}}";
""") + END

F1_W = CPP_STD + cpp("""    long long n, k; in >> n >> k;
    // WRONG: reads the window as holding at most k ELEMENTS (a plain max
    // over length-k windows) — the distinctness constraint goes unseen.
    // Fails the distinct trap: whole array has 2 distinct values (sum 12)
    // but this stops after 6.
    vector<long long> a(n), pre(n + 1, 0);
    for (long long i = 0; i < n; ++i) { long long x; in >> x; a[i] = x; pre[i + 1] = pre[i] + x; }
    long long best = 0;
    for (long long i = k; i <= n; ++i) best = max(best, pre[i] - pre[i - k]);
    out << best << "{{NL}}";
""") + END


# ================================================================ F2
# longest regular bracket subsequence
def _f2_truth(s):
    depth = 0
    matched = 0
    for c in s:
        if c == "(":
            depth += 1
        else:
            if depth > 0:
                depth -= 1
                matched += 1
    return 2 * matched


F2_S = _f2_truth("(()())())")
assert F2_S == 8, f"F2 sample {F2_S}"

F2_CH = challenge(
    "hsgx-f2-chains",
    "Final 2: The Chains",
    """**Bài toán.** A necklace workshop throws bracket characters onto a bench in
order. Find the length of the longest contiguous... no: longest
**subsequence** (not necessarily contiguous) that forms a regular bracket
sequence; print its length.

**Constraints:** 1 ≤ |s| ≤ 200000; s contains only '(' and ')'.

**Input:** one line: s.
**Output:** one integer — the length.
""",
    [
        contest_test("sample", T("(()())())"), T("8"),
            "Drop one character to leave (()())() → length 8."),
        contest_test("all close", T(")))"), T("0"), "No opener ever."),
        contest_test("simple", T("()"), T("2"), "Already regular."),
        contest_test("big mixed", T("(" * 100000 + ")" * 100000), T("200000"), "Perfect balance."),
    ],
    level="independent",
    difficulty="advanced",
)

F2_VI = vi_challenge(
    "Final 2: Dây Chuyền",
    """**Bài toán.** Xưởng trang sức thả các ký tự ngoặc lên bàn theo thứ tự. Tìm độ
dài **dãy con** (không nhất thiết liên tiếp) dài nhất tạo thành dãy ngoặc
cân bằng; in độ dài đó.

**Ràng buộc:** 1 ≤ |s| ≤ 200000; s chỉ chứa '(' và ')'.

**Input:** một dòng: s.
**Output:** một số nguyên — độ dài.
""",
    [
        ("ví dụ", "Xóa ký tự để lại (()())() → 8."),
        ("toàn đóng", "Không có mở nào."),
        ("đơn giản", "Chính nó."),
        ("hỗn hợp lớn", "Cân bằng hoàn hảo."),
    ],
)

F2_R = CPP_STD + cpp("""    string s; in >> s;
    long long depth = 0, matched = 0;
    for (char c : s) {
        if (c == '(') ++depth;
        else if (depth > 0) { --depth; ++matched; }
    }
    out << 2 * matched << "{{NL}}";
""") + END

F2_W = CPP_STD + cpp("""    string s; in >> s;
    // WRONG: counts 2·min(opens, closes) — position-blind. A ')' before any
    // '(' can never be matched; the order trap below exposes it.
    long long opens = 0, closes = 0;
    for (char c : s) (c == '(' ? opens : closes)++;
    out << 2 * min(opens, closes) << "{{NL}}";
""") + END

_t = contest_test(
    "order trap", T(")()("), T("2"),
    "min(opens,closes) would say 4 — but ) before any ( is dead. Truth 2.",
)
F2_CH["tests"].append({"name": _t[0], "code": _t[1], "hint": _t[2]})
F2_VI["tests"].append(("bẫy thứ tự", "min(mở,đóng) sẽ nói 4 — nhưng ) đứng trước mọi ( là chết. Đáp án 2."))


# ================================================================ F3
# minimize the maximum block sum when splitting into k contiguous blocks
def _f3_truth(a, k):
    lo, hi = max(a), sum(a)
    def ok(cap):
        blocks = 1
        s = 0
        for x in a:
            if s + x > cap:
                blocks += 1
                s = x
            else:
                s += x
        return blocks <= k
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


F3_S = _f3_truth([7, 2, 5, 10, 8], 2)
assert F3_S == 18, f"F3 sample {F3_S}"  # [7,2,5] / [10,8]

F3_BIG_ARR = [1 + (i * 131) % 999983 for i in range(1, 200001)]
F3_BIG = _f3_truth(F3_BIG_ARR, 42)

F3_CH = challenge(
    "hsgx-f3-painters",
    "Final 3: The Painters",
    """**Bài toán.** A fence of n boards in a row; board i takes a[i] minutes. You
hire k painters who must each paint a **contiguous** block of boards (every
board exactly one painter, blocks do not interleave). Minimize the time of
the busiest painter; print it.

**Constraints:** 1 ≤ k ≤ n ≤ 200000; 1 ≤ a[i] ≤ 10^6.

**Input:** line 1: n, k; line 2: n values.
**Output:** one integer.
""",
    [
        contest_test("sample", T("5 2", "7 2 5 10 8"), T("18"),
            "Split [7,2,5] / [10,8] → max(14, 18) = 18; no split does better."),
        contest_test("one painter", T("3 1", "4 5 6"), T("15"), "Everything on one."),
        contest_test("k equals n", T("4 4", "3 1 4 1"), T("4"), "Every board its own painter."),
        contest_test("full scale", T(f"200000 42", " ".join(map(str, F3_BIG_ARR))), T(str(F3_BIG)),
            "Binary search the answer + greedy feasibility; O(n·sum) checking is impossible."),
    ],
    level="combination",
    difficulty="advanced",
)

F3_VI = vi_challenge(
    "Final 3: Thợ Sơn",
    """**Bài toán.** Hàng rào n tấm vách liền nhau; tấm i mất a[i] phút. Bạn thuê k
thợ, mỗi người sơn một **đoạn vách liên tiếp** (mỗi tấm đúng một thợ, các
đoạn không cài vào nhau). Tối thiểu hóa thời gian của thợ bận nhất; in ra.

**Ràng buộc:** 1 ≤ k ≤ n ≤ 200000; 1 ≤ a[i] ≤ 10^6.

**Input:** dòng 1: n, k; dòng 2: n giá trị.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "Chia [7,2,5] / [10,8] → max(14, 18) = 18; không cách chia nào tốt hơn."),
        ("một thợ", "Tất cả cho một người."),
        ("k bằng n", "Mỗi tấm một thợ."),
        ("quy mô đầy đủ", "Chảy nhị phân đáp án + kiểm tra tham gia khả thi; duyệt O(n·sum) là bất khả thi."),
    ],
)

F3_R = CPP_STD + cpp("""    long long n, k; in >> n >> k;
    vector<long long> a(n);
    long long lo = 0, hi = 0;
    for (auto& x : a) { in >> x; hi += x; lo = max(lo, x); }
    auto ok = [&](long long cap) {
        long long blocks = 1, s = 0;
        for (long long x : a) {
            if (s + x > cap) { ++blocks; s = x; }
            else s += x;
        }
        return blocks <= k;
    };
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (ok(mid)) hi = mid;
        else lo = mid + 1;
    }
    out << lo << "{{NL}}";
""") + END

F3_W = CPP_STD + cpp("""    long long n, k; in >> n >> k;
    // WRONG: splits into k blocks of nearly EQUAL COUNT (n/k boards each) —
    // ignores the values, fails whenever values are uneven.
    long long per = (n + k - 1) / k;
    long long best = 0, i = 0;
    for (long long b = 0; b < k; ++b) {
        long long s = 0;
        for (long long j = 0; j < per && i < n; ++j, ++i) { long long x; in >> x; s += x; }
        best = max(best, s);
    }
    out << best << "{{NL}}";
""") + END


# ================================================================ F4
# minimize maximum lateness (classic exchange argument: sort by deadline)
def _f4_truth(jobs):
    # jobs: (t, d) — processing time, deadline; single machine from minute 0
    time = 0
    worst = 0
    for t, d in sorted(jobs, key=lambda j: j[1]):
        time += t
        worst = max(worst, time - d)
    return worst


F4_S = _f4_truth([(4, 6), (2, 8), (3, 6)])
# sorted by deadline: (4,6),(3,6),(2,8) → finish 4,7,9 → lateness 0,1,1 → 1
assert F4_S == 1, f"F4 sample {F4_S}"

F4_BIG_JOBS = [(1 + (i * 17) % 1000, 1 + (i * 41 + 13) % 20000) for i in range(1, 200001)]
F4_BIG = _f4_truth(F4_BIG_JOBS)

F4_CH = challenge(
    "hsgx-f4-deadlines",
    "Final 4: The Deadlines",
    """**Bài toán.** A single barber has n clients; client i needs t[i] minutes and
must be finished by minute d[i] (clients start at minute 0, one at a time,
no gaps). Client i is *late* by max(0, finish − d[i]). Schedule to minimize
the maximum lateness; print it.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ t[i] ≤ 10^3; 1 ≤ d[i] ≤ 2·10^4.

**Input:** line 1: n; then n lines: t, d.
**Output:** one integer.
""",
    [
        contest_test("sample", T("3", "4 6", "2 8", "3 6"), T("1"),
            "Order by deadline: (4,6),(3,6),(2,8) → finishes 4,7,9 → lateness 0,1,1 → 1."),
        contest_test("all late", T("2", "5 1", "5 1"), T("9"), "First finishes 5 (late 4), second 10 (late 9) → 9."),
        contest_test("none late", T("3", "1 10", "2 10", "3 10"), T("0"), "Everything fits."),
        contest_test("full scale", T("200000", *(f"{t} {d}" for t, d in F4_BIG_JOBS)), T(str(F4_BIG)),
            "Exchange argument: earliest deadline first is optimal."),
    ],
    level="combination",
    difficulty="advanced",
)

F4_VI = vi_challenge(
    "Final 4: Hạn Chót",
    """**Bài toán.** Một thợ cắt tóc có n khách; khách i cần t[i] phút và phải xong
trước phút d[i] (khách bắt đầu từ phút 0, lần lượt, không trống). Khách i
*bị trễ* max(0, xong − d[i]). Sắp lịch để tối thiểu độ trễ lớn nhất; in ra.

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ t[i] ≤ 10^3; 1 ≤ d[i] ≤ 2·10^4.

**Input:** dòng 1: n; rồi n dòng: t, d.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "Sắp theo hạn: (4,6),(3,6),(2,8) → xong 4,7,9 → trễ 0,1,1 → 1."),
        ("trễ hết", "Người đầu xong 5 (trễ 4), người sau 10 (trễ 9) → 9."),
        ("không trễ", "Mọi thứ vừa."),
        ("quy mô đầy đủ", "Lập luận đổi chỗ: hạn sớm nhất trước là tối ưu."),
    ],
)

F4_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& [t, d] : v) in >> t >> d;
    sort(v.begin(), v.end(), [](const auto& A, const auto& B) { return A.second < B.second; });
    long long time = 0, worst = 0;
    for (auto& [t, d] : v) {
        time += t;
        worst = max(worst, time - d);
    }
    out << worst << "{{NL}}";
""") + END

F4_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& [t, d] : v) in >> t >> d;
    // WRONG: shortest job first — the classic anti-optimality for max
    // lateness; a short job with a far deadline jumps ahead of a long job
    // with a near deadline and detonates the long one's lateness.
    sort(v.begin(), v.end());
    long long time = 0, worst = 0;
    for (auto& [t, d] : v) {
        time += t;
        worst = max(worst, time - d);
    }
    out << worst << "{{NL}}";
""") + END

_t = contest_test(
    "sjf trap", T("3", "1 100", "10 10", "1 100"), T("0"),
    "Shortest-first runs the 10-minute job last: finishes 12 → late 2. Deadline order: (10,10) first → 0.",
)
F4_CH["tests"].append({"name": _t[0], "code": _t[1], "hint": _t[2]})
F4_VI["tests"].append(("bẫy việc ngắn", "Việc-ngắn-trước chạy việc 10 phút cuối: xong 12 → trễ 2. Theo hạn: (10,10) trước → 0."))


# ================================================================ F5
# count x in [1..N] with digit sum divisible by 7 (digit DP)
def _f5_truth_dp(N_str):
    # counts 1..N with digit sum % 7 == 0
    from functools import lru_cache
    digs = [int(c) for c in N_str]
    @lru_cache(maxsize=None)
    def go(i, mod, tight):
        if i == len(digs):
            return 1 if mod == 0 else 0
        limit = digs[i] if tight else 9
        total = 0
        for d in range(0, limit + 1):
            total += go(i + 1, (mod + d) % 7, tight and d == limit)
        return total
    r = go(0, 0, True)
    go.cache_clear()
    return r - 1  # exclude x = 0 (digit sum 0 counts as divisible)


def _f5_brute(N):
    return sum(1 for x in range(1, N + 1) if sum(int(c) for c in str(x)) % 7 == 0)


# mirror sanity on smalls
import random as _random
_rng = _random.Random(20260922)
for _ in range(60):
    _N = _rng.randint(1, 50000)
    assert _f5_truth_dp(str(_N)) == _f5_brute(_N), f"F5 mirror mismatch at {_N}"

F5_BIG_N = "9" * 18
F5_BIG = _f5_truth_dp(F5_BIG_N)

F5_CH = challenge(
    "hsgx-f5-lucky",
    "Final 5: The Lucky Tickets",
    """**Bài toán.** Count the integers x with 1 ≤ x ≤ N whose decimal digit sum is
divisible by 7.

**Constraints:** 1 ≤ N < 10^18 (up to 18 digits).

**Input:** one line: N.
**Output:** one integer — the count (fits in 64 bits).
""",
    [
        contest_test("small", T("20"), T("3"),
            "Digit sums divisible by 7 in 1..20: 7 (7), 14 (5)? no — the editorial lists them; brute count 3."),
        contest_test("one", T("7"), T("1"), "Just 7."),
        contest_test("big", T(F5_BIG_N), T(str(F5_BIG)), "18 nines — digit DP with mod-7 state."),
    ],
    level="combination",
    difficulty="advanced",
)

F5_VI = vi_challenge(
    "Final 5: Vé May Mắn",
    """**Bài toán.** Đếm số nguyên x với 1 ≤ x ≤ N có tổng chữ số chia hết cho 7.

**Ràng buộc:** 1 ≤ N < 10^18 (tới 18 chữ số).

**Input:** một dòng: N.
**Output:** một số nguyên — số lượng (vừa 64-bit).
""",
    [
        ("nhỏ", "Liệt kê bên dưới."),
        ("một", "Chỉ có 7."),
        ("lớn", "18 chữ số 9 — digit DP với trạng thái mod 7."),
    ],
)

# fix the small test's want after honest enumeration
F5_S20 = _f5_brute(20)
_t5 = contest_test("small", T("20"), T(str(F5_S20)),
    f"Brute enumeration: {F5_S20} numbers in 1..20 have digit sum divisible by 7.")
F5_CH["tests"][0] = {"name": _t5[0], "code": _t5[1], "hint": _t5[2]}
F5_VI["tests"][0] = ("nhỏ", f"Liệt kê vét cạn: {F5_S20} số trong 1..20 có tổng chữ số chia hết cho 7.")

F5_R = CPP_STD + cpp("""    string N; in >> N;
    long long dp[2][7] = {};
    dp[1][0] = 1;   // tight, empty prefix, mod 0
    for (char c : N) {
        int d = c - '0';
        long long ndp[2][7] = {};
        for (int tight = 0; tight < 2; ++tight)
            for (int m = 0; m < 7; ++m) {
                long long cur = dp[tight][m];
                if (!cur) continue;
                int lim = tight ? d : 9;
                for (int dig = 0; dig <= lim; ++dig) {
                    int nt = (tight && dig == lim) ? 1 : 0;
                    ndp[nt][(m + dig) % 7] += cur;
                }
            }
        for (int t = 0; t < 2; ++t)
            for (int m = 0; m < 7; ++m) dp[t][m] = ndp[t][m];
    }
    long long ans = dp[0][0] + dp[1][0] - 1;   // exclude x = 0
    out << ans << "{{NL}}";
""") + END

F5_W = CPP_STD + cpp("""    string N; in >> N;
    long long dp[2][7] = {};
    dp[1][0] = 1;
    for (char c : N) {
        int d = c - '0';
        long long ndp[2][7] = {};
        for (int tight = 0; tight < 2; ++tight)
            for (int m = 0; m < 7; ++m) {
                long long cur = dp[tight][m];
                if (!cur) continue;
                int lim = tight ? d : 9;
                for (int dig = 0; dig <= lim; ++dig) {
                    int nt = (tight && dig == lim) ? 1 : 0;
                    ndp[nt][(m + dig) % 7] += cur;
                }
            }
        for (int t = 0; t < 2; ++t)
            for (int m = 0; m < 7; ++m) dp[t][m] = ndp[t][m];
    }
    // WRONG: forgets to subtract x = 0 — the empty number has digit sum 0,
    // which the DP counts as divisible; every answer is exactly one too big.
    out << dp[0][0] + dp[1][0] << "{{NL}}";
""") + END


# ================================================================ F6
# weighted interval scheduling (max weight, no overlaps; end <= start OK)
def _f6_truth(intervals):
    # intervals: (start, end, weight)
    ivs = sorted(intervals, key=lambda x: x[1])
    import bisect
    ends = [e for _, e, _ in ivs]
    dp = [0] * (len(ivs) + 1)
    for i, (s, e, w) in enumerate(ivs, start=1):
        j = bisect.bisect_right(ends, s)  # count of intervals with end <= s
        dp[i] = max(dp[i - 1], dp[j] + w)
    return dp[-1]


F6_S = _f6_truth([(1, 3, 5), (2, 5, 6), (4, 7, 5), (6, 9, 4)])
assert F6_S == 10, f"F6 sample {F6_S}"  # (1,3,5)+(4,7,5) → 10 beats 6+4=10? also 10; and (2,5,6)+(6,9,4)=10 — all 10

F6_BIG_IVS = [((i * 13) % 1000000, 0, 0) for i in range(1, 100001)]
F6_BIG_IVS = [((i * 13) % 1000000, ((i * 13) % 1000000) + 1 + ((i * 7) % 5000), 1 + ((i * 31) % 1000)) for i in range(1, 100001)]
F6_BIG = _f6_truth(F6_BIG_IVS)

F6_CH = challenge(
    "hsgx-f6-bookings",
    "Final 6: The Bookings",
    """**Bài toán.** A hall accepts booking requests i = (s[i], e[i], w[i]): the
event would occupy the half-open interval [s, e) and pays w. Accept any
subset of pairwise non-overlapping bookings (one event may start exactly
when another ends); maximize total payment.

**Constraints:** 1 ≤ n ≤ 100000; 0 ≤ s < e ≤ 10^6; 1 ≤ w ≤ 1000.

**Input:** line 1: n; then n lines: s, e, w.
**Output:** one integer.
""",
    [
        contest_test("sample", T("4", "1 3 5", "2 5 6", "4 7 5", "6 9 4"), T("10"),
            "Several optimal picks reach 10 — e.g. (1,3,5)+(4,7,5)."),
        contest_test("single", T("1", "0 1000000 777"), T("777"), "Take it."),
        contest_test("chain", T("3", "1 2 10", "2 3 10", "3 4 10"), T("30"),
            "Touching endpoints are compatible."),
        contest_test("full scale", T("100000", *(f"{s} {e} {w}" for s, e, w in F6_BIG_IVS)), T(str(F6_BIG)),
            "Sort by end + binary search predecessor; O(n²) chains are 10^10."),
    ],
    level="combination",
    difficulty="advanced",
)

F6_VI = vi_challenge(
    "Final 6: Đặt Địa Điểm",
    """**Bài toán.** Một hội trường nhận các yêu cầu đặt i = (s[i], e[i], w[i]): sự
kiện chiếm nửa-khe [s, e) và trả w. Chấp nhận một tập yêu cầu đôi một không
giao nhau (sự kiện có thể bắt đầu đúng lúc khác kết thúc); tối đa hóa tổng
tiền.

**Ràng buộc:** 1 ≤ n ≤ 100000; 0 ≤ s < e ≤ 10^6; 1 ≤ w ≤ 1000.

**Input:** dòng 1: n; rồi n dòng: s, e, w.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", "Vài cách chọn đều đạt 10 — ví dụ (1,3,5)+(4,7,5)."),
        ("đơn", "Lấy buổi duy nhất."),
        ("chuỗi", "Đầu mút chạm nhau vẫn tương thích."),
        ("quy mô đầy đủ", "Sắp theo end + chảy nhị phân tiền nhiệm; chuỗi O(n²) là 10^10."),
        ("bẫy trọng lượng", "Greedy chọn (2,4,25) nặng nhất chặn cả hai buổi (3,5,14) — tối ưu là 28 qua (1,3,14)+(3,5,14)."),
    ],
)

F6_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<array<long long, 3>> v(n);
    for (auto& x : v) in >> x[0] >> x[1] >> x[2];
    sort(v.begin(), v.end(), [](const auto& A, const auto& B) { return A[1] < B[1]; });
    vector<long long> ends(n);
    for (long long i = 0; i < n; ++i) ends[i] = v[i][1];
    vector<long long> dp(n + 1, 0);
    for (long long i = 1; i <= n; ++i) {
        long long s = v[i - 1][0], w = v[i - 1][2];
        long long j = (long long)(upper_bound(ends.begin(), ends.begin() + i - 1, s) - ends.begin());
        dp[i] = max(dp[i - 1], dp[j] + w);
    }
    out << dp[n] << "{{NL}}";
""") + END

F6_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<array<long long, 3>> v(n);
    for (auto& x : v) in >> x[0] >> x[1] >> x[2];
    // WRONG: greedy by weight — the heaviest booking first, compatible or
    // not afterwards. A heavy middle booking can block two medium ones that
    // jointly pay more.
    sort(v.begin(), v.end(), [](const auto& A, const auto& B) { return A[2] > B[2]; });
    vector<array<long long, 2>> taken;
    long long total = 0;
    for (auto& [s, e, w] : v) {
        bool ok = true;
        for (auto& [ts, te] : taken)
            if (s < te && ts < e) { ok = false; break; }
        if (ok) { taken.push_back({s, e}); total += w; }
    }
    out << total << "{{NL}}";
""") + END

# greedy-by-weight trap: heaviest booking overlaps BOTH mediums, which are
# mutually compatible — greedy takes 25 and stalls; truth is 14+14 = 28.
def _f6_trap():
    ivs = [(1, 3, 14), (3, 5, 14), (2, 4, 25)]
    import bisect
    srt = sorted(ivs, key=lambda x: x[1])
    ends = [e for _, e, _ in srt]
    dp = [0] * (len(srt) + 1)
    for i, (s, e, w) in enumerate(srt, start=1):
        j = bisect.bisect_right(ends, s)
        dp[i] = max(dp[i - 1], dp[j] + w)
    return dp[-1]

F6_TRAP = _f6_trap()
assert F6_TRAP == 28, f"F6 trap truth {F6_TRAP}"  # 14+14 beats 25

_t = contest_test(
    "weight trap", T("3", "1 3 14", "3 5 14", "2 4 25"), T("28"),
    "The heaviest (2,4,25) overlaps both mediums, which touch at 3 and pay 14+14 = 28 — greedy-by-weight stalls at 25.",
)
F6_CH["tests"].append({"name": _t[0], "code": _t[1], "hint": _t[2]})
F6_VI["tests"].append(("bẫy trọng số", "Cái nặng nhất (2,4,25) giao cả hai cái trung bình, vốn chạm nhau tại 3 và trả 14+14 = 28 — tham lam theo trọng số dừng ở 25."))


# ================================================================ checkpoint
# Capstone: max path sum right/down where the drone may zero out one cell
# it passes through (2-state DP). The W zeroes the global min unconditionally.
def _cp_truth(grid):
    n = len(grid)
    m = len(grid[0])
    NEG = float("-inf")
    # dp[i][j][used]
    dp = [[[NEG] * 2 for _ in range(m)] for _ in range(n)]
    dp[0][0][0] = grid[0][0]
    dp[0][0][1] = 0  # zero out the start cell itself
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                continue
            best_from = NEG
            best_used = NEG
            if i > 0:
                best_from = max(best_from, dp[i - 1][j][0])
                best_used = max(best_used, dp[i - 1][j][1])
            if j > 0:
                best_from = max(best_from, dp[i][j - 1][0])
                best_used = max(best_used, dp[i][j - 1][1])
            dp[i][j][0] = best_from + grid[i][j] if best_from != NEG else NEG
            zero_here = (best_from + 0) if best_from != NEG else NEG
            dp[i][j][1] = max(best_used + grid[i][j], zero_here)
    return max(dp[n - 1][m - 1][0], dp[n - 1][m - 1][1])


CP_GRID = [
    [10, -50, 20],
    [30, 40, -50],
    [-50, 50, 60],
]
CP_S = _cp_truth(CP_GRID)

# brute-check the truth by enumeration on the small grid
def _cp_brute(grid):
    n, m = len(grid), len(grid[0])
    best = float("-inf")
    def paths(i, j, cells):
        nonlocal best
        cells = cells + [(i, j)]
        if i == n - 1 and j == m - 1:
            total_plain = sum(grid[a][b] for a, b in cells)
            zero_gain = max(0, -min(grid[a][b] for a, b in cells))
            best = max(best, total_plain + zero_gain)
            return
        if i + 1 < n:
            paths(i + 1, j, cells)
        if j + 1 < m:
            paths(i, j + 1, cells)
    paths(0, 0, [])
    return best

CP_B = _cp_brute(CP_GRID)
assert CP_S == CP_B == 190, f"CP sample dp={CP_S} brute={CP_B}"

# big test: 300x300 deterministic grid
def _cp_big():
    n = 300
    grid = [[((i * 31 + j * 17) % 200) - 100 for j in range(n)] for i in range(n)]
    return _cp_truth(grid)

CP_BIG = _cp_big()

CP_CH = challenge(
    "hsgx-cp-m12-drone",
    "Capstone: The Relief Drone",
    """**Bài toán.** A relief drone flies from the top-left cell to the
bottom-right cell of an n×n grid of supply values, moving only right or
down. It collects the value of every cell it enters. Its cargo bay can
**discard exactly one cell's haul** along the way (turn one entered cell's
value into 0; at most once per trip, optional). Maximize the collected
total; print it.

**Constraints:** 2 ≤ n ≤ 300; −100 ≤ grid[i][j] ≤ 100.

**Input:** line 1: n; then n lines of n values.
**Output:** one integer.
""",
    [
        contest_test("sample", T("3", "10 -50 20", "30 40 -50", "-50 50 60"), T(str(CP_S)),
            f"Inner route 10→30→40→50→60 = {CP_S} — no discard needed there. (Subtracting the GLOBAL −50 invents 240.)"),
        contest_test("all positive", T("2", "1 2", "3 4"), T("8"), "Best plain path 1→3→4 = 8; the optional discard is worthless here."),
        contest_test("big", T(f"300", *[" ".join(str(((i * 31 + j * 17) % 200) - 100) for j in range(300)) for i in range(300)]), T(str(CP_BIG)),
            "Two-state DP over (cell, discard-used)."),
    ],
    level="combination",
    difficulty="advanced",
)

CP_VI = vi_challenge(
    "Điểm kiểm tra: Máy Bay Cứu Trợ",
    """**Bài toán.** Máy bay cứu trợ bay từ ô trên trái đến ô dưới phải của lưới
n×n giá trị tiếp tế, chỉ đi phải hoặc xuống. Nó thu giá trị của mọi ô đi
vào. Khoang hàng có thể **bỏ đúng một ô** trên đường (đưa giá trị một ô đã
đi vào về 0; tối đa một lần, không bắt buộc). Tối đa hóa tổng thu được; in ra.

**Ràng buộc:** 2 ≤ n ≤ 300; −100 ≤ grid[i][j] ≤ 100.

**Input:** dòng 1: n; rồi n dòng n giá trị.
**Output:** một số nguyên.
""",
    [
        ("ví dụ", f"Đường trong 10→30→40→50→60 = {CP_S} — không cần bỏ gì trên đường này. (Trừ GIÁ TRỊ NHỎ NHẤT toàn cục −50 sẽ bịa ra 240.)"),
        ("toàn dương", "Đường thường tốt nhất 1→3→4 = 8; lần bỏ không đáng giá ở đây."),
        ("lớn", "DP hai trạng thái (ô, đã-bỏ)."),
    ],
)

CP_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<vector<long long>> g(n, vector<long long>(n));
    for (auto& row : g) for (auto& x : row) in >> x;
    const long long NEG = LLONG_MIN / 4;
    // dp[used][j]: max sum reaching column j of the current row with
    // `used` = 0/1 discards spent. Rolled over row by row.
    vector<vector<long long>> dp0(n, vector<long long>(n, NEG));
    vector<vector<long long>> dp1(n, vector<long long>(n, NEG));
    dp0[0][0] = g[0][0];
    dp1[0][0] = 0;   // discard the start cell's haul
    for (long long i = 0; i < n; ++i) {
        for (long long j = 0; j < n; ++j) {
            if (i == 0 && j == 0) continue;
            long long bf = NEG, bu = NEG;
            if (i > 0) { bf = max(bf, dp0[i - 1][j]); bu = max(bu, dp1[i - 1][j]); }
            if (j > 0) { bf = max(bf, dp0[i][j - 1]); bu = max(bu, dp1[i][j - 1]); }
            if (bf == NEG) { dp0[i][j] = NEG; dp1[i][j] = NEG; continue; }
            dp0[i][j] = bf + g[i][j];
            dp1[i][j] = max(bu + g[i][j], bf);   // spend the discard here
        }
    }
    out << max(dp0[n - 1][n - 1], dp1[n - 1][n - 1]) << "{{NL}}";
""") + END

CP_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<vector<long long>> g(n, vector<long long>(n));
    for (auto& row : g) for (auto& x : row) in >> x;
    // WRONG: computes the plain best path, then subtracts the globally most
    // negative cell — even when that cell is not on the path at all.
    long long best = LLONG_MIN, gmin = 0;
    for (long long i = 0; i < n; ++i)
        for (long long j = 0; j < n; ++j) gmin = min(gmin, g[i][j]);
    vector<vector<long long>> dp(n, vector<long long>(n, LLONG_MIN));
    dp[0][0] = g[0][0];
    for (long long i = 0; i < n; ++i)
        for (long long j = 0; j < n; ++j) {
            if (i == 0 && j == 0) continue;
            long long bf = LLONG_MIN;
            if (i > 0) bf = max(bf, dp[i - 1][j]);
            if (j > 0) bf = max(bf, dp[i][j - 1]);
            dp[i][j] = bf + g[i][j];
        }
    best = dp[n - 1][n - 1];
    if (gmin < 0) best -= gmin;
    out << best << "{{NL}}";
""") + END

# off-path-min trap: 3x3, the -9 is never on any monotone optimal path —
# R discards only what it carries (truth 5); W subtracts the global min (14).
def _cp_trap_grid():
    return [[1, -9, 1], [1, 1, 1], [1, 1, 1]]

CP_TRAP = _cp_truth(_cp_trap_grid())
assert CP_TRAP == 5, f"CP trap truth {CP_TRAP}"

_t = contest_test(
    "off-path min", T("3", "1 -9 1", "1 1 1", "1 1 1"), T("5"),
    "The best path avoids -9 entirely: plain path sum 5, nothing worth discarding → 5. A solution that subtracts the GLOBAL minimum invents a 14.",
)
CP_CH["tests"].append({"name": _t[0], "code": _t[1], "hint": _t[2]})
CP_VI["tests"].append(("min ngoài đường", "Đường tốt né hẳn -9: tổng đường thường 5, không đáng bỏ gì → 5. Lời giải trừ GIÁ TRỊ NHỎ NHẤT toàn cục sẽ bịa ra 14."))


# ------------------------------------------------------------------ practice
write_practice(
    M, "hsgx-p12-final-pack",
    "The Final Pack",
    "Six hardest-course problems: distinct-value windows, bracket subsequences, painter partition, deadline scheduling, digit-DP counting, weighted booking selection. No topic labels.",
    "Bộ Cuối",
    "Sáu bài khó nhất khóa học: cửa sổ giá trị phân biệt, dãy con ngoặc, chia thợ, lịch hạn chót, đếm digit-DP, chọn đặt chỗ có trọng số. Không nhãn chủ đề.",
    "hsgx-m12-reference-pack",
    150,
    "advanced",
    [F1_CH, F2_CH, F3_CH, F4_CH, F5_CH, F6_CH],
    [F1_VI, F2_VI, F3_VI, F4_VI, F5_VI, F6_VI],
    solutions=[
        ("hsgx-f1-showcase", F1_R, F1_W),
        ("hsgx-f2-chains", F2_R, F2_W),
        ("hsgx-f3-painters", F3_R, F3_W),
        ("hsgx-f4-deadlines", F4_R, F4_W),
        ("hsgx-f5-lucky", F5_R, F5_W),
        ("hsgx-f6-bookings", F6_R, F6_W),
    ],
)


# ------------------------------------------------------------------ checkpoint
CP_MDX = """
**Điểm kiểm tra — Capstone.** The Relief Drone fuses the two states you
trained all course: a grid DP (Module 3's classic) with an extra boolean
dimension for the one-shot discard — the same "state expansion" move behind
Module 4's coupon Dijkstra. Write the two-state transition yourself before
looking at anything; if the transition for "spend the discard here" reads
`max(bu + g[i][j], bf)` naturally, the course landed.
"""

CP_VI_MDX = """
**Điểm kiểm tra — Capstone.** Máy Bay Cứu Trợ ghép hai trạng thái bạn rèn cả
khóa học: DP lưới (kinh điển của Module 3) với thêm một chiều boolean cho
lần bỏ duy nhất — chính nước "mở rộng trạng thái" đứng sau Dijkstra phiếu
giảm giá của Module 4. Tự viết công thức chuyển hai trạng thái trước khi xem
bất cứ thứ gì; nếu nhánh "bỏ ngay đây" đọc tự nhiên như
`max(bu + g[i][j], bf)` thì khóa học đã vào người.
"""

write_checkpoint(
    M, "hsgx-cp-m12-capstone",
    "Capstone — The Relief Drone",
    "A two-state grid DP fusing the course's core moves; the final graded problem of HSG Intensive.",
    60,
    CP_MDX,
    "Điểm kiểm tra — Máy Bay Cứu Trợ",
    "DP lưới hai trạng thái ghép các nước lõi của khóa học; bài chấm cuối cùng của HSG Intensive.",
    CP_VI_MDX,
    CP_CH, CP_VI,
    CP_R, CP_W,
)


# ------------------------------------------------------------------ course.json
# Write the course-level registration (idempotent; mirrors hsg-advanced's shape).
import json as _json

COURSE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                          "src", "content", "tracks", "hsg", "courses", "hsg-intensive")

COURSE_EN = {
    "id": "hsg-intensive",
    "title": "Competitive Programming — High School Intensive",
    "description": "The mastery stage of the Vietnamese competitive-programming path: problem recognition without labels, constraint budgeting, key observations, algorithm combinations, optimization and wrong-solution clinics, stress testing, subtask strategy, timed and mixed sets, mock contests, and editorial study with re-solve and variation transfer — all graded in the C++20 sandbox.",
    "audience": "Students who finished the HSG Advanced course (or equivalent) and are preparing for high-level provincial and national HSG Tin hoc rounds — the stage where knowing algorithms must turn into solving unfamiliar problems under a clock.",
    "outcomes": [
        "Recognize the hidden algorithmic family of an unlabeled problem from constraints, query shape, and samples",
        "Convert constraint budgets into algorithm choices and reject infeasible complexities on sight",
        "Find and prove the key observation that unlocks brute-force bottlenecks, then optimize to fit the clock",
        "Diagnose wrong solutions by failure class — WA, TLE, overflow, precision — and build stress harnesses that catch them",
        "Bank partial credit with subtask strategy and manage a contest clock with the A-first policy",
        "Study editorials the strong way: stall, re-derive, re-implement clean, and transfer the insight to variations",
    ],
    "prerequisites": ["hsg-advanced"],
    "modules": [
        {"reference": "hsgx-recognition"},
        {"reference": "hsgx-budget"},
        {"reference": "hsgx-observation"},
        {"reference": "hsgx-combinations"},
        {"reference": "hsgx-wrong"},
        {"reference": "hsgx-stress"},
        {"reference": "hsgx-subtask"},
        {"reference": "hsgx-speed"},
        {"reference": "hsgx-mixed"},
        {"reference": "hsgx-contests"},
        {"reference": "hsgx-editorials"},
        {"reference": "hsgx-final"},
    ],
}

COURSE_VI = {
    "title": "Lập trình thi đấu — Trung học Cường hóa",
    "description": "Bậc cường hóa của lộ trình lập trình thi đấu Việt Nam: nhận diện bài toán không nhãn, ngân sách ràng buộc, bài tập tìm nhận xét then chốt, kết hợp thuật toán, phòng tối ưu, phòng lời giải sai, stress test, chiến lược subtask và lấy điểm một phần, bộ đề có giới hạn thời gian, bộ đề hỗn hợp, vòng thi giả định đầy đủ, đọc lời giải với giải lại và chuyển giao biến thể — chấm trong sandbox C++20.",
}

with open(os.path.join(COURSE_DIR, "course.json"), "w", encoding="utf-8") as f:
    f.write(_json.dumps(COURSE_EN, indent=2, ensure_ascii=False) + "\n")
with open(os.path.join(COURSE_DIR, "course.vi.json"), "w", encoding="utf-8") as f:
    f.write(_json.dumps(COURSE_VI, indent=2, ensure_ascii=False) + "\n")
print("course.json + course.vi.json written")

print("module m12 complete")
