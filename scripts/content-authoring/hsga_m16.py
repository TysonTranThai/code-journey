#!/usr/bin/env python3
"""HSG Advanced — Module 16: hsga-synth (Technique Synthesis).

Problems where two techniques must combine: prefix sums + binary
search counting subarrays in a sum range, coordinate compression +
Fenwick counting inversions over sparse values, sweep + heap scheduling,
and binary search on the answer + greedy feasibility. Wrong solutions:
O(n^2) subarray enumeration (timeout), merge-sort inversion count that
ignores duplicates (WA), and a feasibility check that overcounts
positions (WA).

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

M = "hsga-synth"

# ------------------------------------------------------------------ data
# Deterministic load data, generated in the authoring pass and embedded
# via generator code (random.Random with fixed seed) — the SAME generator
# runs inside the module at emit time, so tests and answers always match.
import random
import bisect
import heapq


def count_subarrays(a, L, R):
    P = [0]
    for x in a:
        P.append(P[-1] + x)
    cnt = 0
    for j in range(len(a) + 1):
        lo = bisect.bisect_left(P, P[j] - R, 0, j)
        hi = bisect.bisect_right(P, P[j] - L, 0, j)
        cnt += hi - lo
    return cnt


def brute_subarrays(a, L, R):
    c = 0
    for i in range(len(a)):
        s = 0
        for j in range(i, len(a)):
            s += a[j]
            if L <= s <= R:
                c += 1
    return c


_a = [1, 2, 3, 4]
assert count_subarrays(_a, 3, 6) == brute_subarrays(_a, 3, 6) == 5

_rnd1 = random.Random(21)
_A1_BIG = [_rnd1.randint(1, 1000) for _ in range(200000)]
L1, R1 = 5000, 20000
_A1_BIG_ANS = count_subarrays(_A1_BIG, L1, R1)
assert _A1_BIG_ANS == 5983423


def inversions(a):
    s = sorted(set(a))
    rank = {v: i + 1 for i, v in enumerate(s)}
    n = len(s)
    fen = [0] * (n + 1)
    def upd(i):
        while i <= n:
            fen[i] += 1
            i += i & -i
    def qry(i):
        s = 0
        while i > 0:
            s += fen[i]
            i -= i & -i
        return s
    inv = 0
    for x in reversed(a):
        inv += qry(rank[x] - 1)
        upd(rank[x])
    return inv

assert inversions([3, 1, 2]) == 2

_rnd2 = random.Random(11)
_A2_BIG = [_rnd2.randint(1, 10**9) for _ in range(200000)]
_A2_BIG_ANS = inversions(_A2_BIG)
assert _A2_BIG_ANS == 9981029921

_rnd3 = random.Random(5)
_A3_IV = []
for _ in range(200000):
    s = _rnd3.randint(0, 10**9 - 100)
    e = s + _rnd3.randint(1, 100)
    _A3_IV.append((s, e))
_A3_IV.sort()
_h = []
_A3_BIG_ANS = 0
for (s, e) in _A3_IV:
    while _h and _h[0] <= s:
        heapq.heappop(_h)
    heapq.heappush(_h, e)
    _A3_BIG_ANS = max(_A3_BIG_ANS, len(_h))
assert _A3_BIG_ANS == 3

_rnd4 = random.Random(77)
_CP_POS = sorted(_rnd4.randint(0, 10**9) for _ in range(200000))
_CP_K = 5000


def max_min_dist(pos, k):
    def feasible(d):
        c = 1
        last = pos[0]
        for x in pos[1:]:
            if x - last >= d:
                c += 1
                last = x
        return c >= k
    lo, hi = 0, pos[-1] - pos[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

_CP_ANS = max_min_dist(_CP_POS, _CP_K)
assert _CP_ANS == 194981

# ------------------------------------------------------------------ C++ bodies
A1_R = CPP_STD + cpp("""
    // Count subarrays with sum in [L, R] over positive values:
    // prefix sums are increasing; for each j count i < j with
    // P[j]-R <= P[i] <= P[j]-L via binary search.
    int n; long long L, R; in >> n >> L >> R;
    vector<long long> P(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        P[i] = P[i-1] + x;
    }
    long long cnt = 0;
    for (int j = 0; j <= n; ++j) {
        long long lo = lower_bound(P.begin(), P.begin() + j, P[j] - R) - P.begin();
        long long hi = upper_bound(P.begin(), P.begin() + j, P[j] - L) - P.begin();
        cnt += hi - lo;
    }
    out << cnt << "{{NL}}";
""") + END

A1_W = CPP_STD + cpp("""
    // WRONG: O(n^2) enumeration of all subarrays — correct but hopeless
    // at n = 200000 (2e10 steps).
    int n; long long L, R; in >> n >> L >> R;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long cnt = 0;
    for (int i = 0; i < n; ++i) {
        long long s = 0;
        for (int j = i; j < n; ++j) {
            s += a[j];
            if (L <= s && s <= R) ++cnt;
        }
    }
    out << cnt << "{{NL}}";
""") + END

A2_R = CPP_STD + cpp("""
    // Count inversions: coordinate-compress, Fenwick walk from the right.
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> s(a);
    sort(s.begin(), s.end());
    s.erase(unique(s.begin(), s.end()), s.end());
    int m = s.size();
    auto rankof = [&](long long v) {
        return int(lower_bound(s.begin(), s.end(), v) - s.begin()) + 1;
    };
    vector<int> fen(m + 1, 0);
    auto upd = [&](int i) {
        for (; i <= m; i += i & -i) ++fen[i];
    };
    auto qry = [&](int i) {
        long long t = 0;
        for (; i > 0; i -= i & -i) t += fen[i];
        return t;
    };
    long long inv = 0;
    for (int i = n - 1; i >= 0; --i) {
        int r = rankof(a[i]);
        inv += qry(r - 1);
        upd(r);
    }
    out << inv << "{{NL}}";
""") + END

A2_W = CPP_STD + cpp("""
    // WRONG: merge-sort inversion count that adds (mid - i) on EQUAL
    // elements — counts equal pairs as inversions. With distinct values the
    // answer is right; with duplicates it overcounts.
    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long inv = 0;
    vector<long long> buf(n);
    function<void(int, int)> ms = [&](int lo, int hi) {
        if (hi - lo <= 1) return;
        int mid = (lo + hi) / 2;
        ms(lo, mid); ms(mid, hi);
        int i = lo, j = mid, k = lo;
        while (i < mid && j < hi) {
            if (a[j] <= a[i]) { buf[k++] = a[j++]; inv += mid - i; }  // <= counts equals — BUG
            else buf[k++] = a[i++];
        }
        while (i < mid) buf[k++] = a[i++];
        while (j < hi) buf[k++] = a[j++];
        for (int t = lo; t < hi; ++t) a[t] = buf[t];
    };
    ms(0, n);
    out << inv << "{{NL}}";
""") + END

A3_R = CPP_STD + cpp("""
    // Minimum rooms: sort by start, min-heap of end times, pop expired.
    int n; in >> n;
    vector<pair<long long, long long>> iv(n);
    for (auto& [s, e] : iv) in >> s >> e;
    sort(iv.begin(), iv.end());
    priority_queue<long long, vector<long long>, greater<long long>> h;
    int best = 0;
    for (auto& [s, e] : iv) {
        while (!h.empty() && h.top() <= s) h.pop();
        h.push(e);
        best = max(best, (int)h.size());
    }
    out << best << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""
    // WRONG: treats intervals [s1,e1) and [e1,e2) as OVERLAPPING (uses
    // h.top() < s instead of <=). Answers blow up on back-to-back chains.
    int n; in >> n;
    vector<pair<long long, long long>> iv(n);
    for (auto& [s, e] : iv) in >> s >> e;
    sort(iv.begin(), iv.end());
    priority_queue<long long, vector<long long>, greater<long long>> h;
    int best = 0;
    for (auto& [s, e] : iv) {
        while (!h.empty() && h.top() < s) h.pop();  // strict: off by one
        h.push(e);
        best = max(best, (int)h.size());
    }
    out << best << "{{NL}}";
""") + END

CP_M16_R = CPP_STD + cpp("""
    // Binary search on the answer + greedy feasibility.
    int n; long long k; in >> n >> k;
    vector<long long> p(n);
    for (auto& x : p) in >> x;
    sort(p.begin(), p.end());
    long long lo = 0, hi = p[n-1] - p[0];
    auto feasible = [&](long long d) {
        long long c = 1, last = p[0];
        for (int i = 1; i < n; ++i) {
            if (p[i] - last >= d) { ++c; last = p[i]; }
        }
        return c >= k;
    };
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        if (feasible(mid)) lo = mid;
        else hi = mid - 1;
    }
    out << lo << "{{NL}}";
""") + END

CP_M16_W = CPP_STD + cpp("""
    // WRONG: feasibility uses > d (strictly greater) instead of >= d —
    // the greedy places one fewer point whenever a gap is EXACTLY d, so
    // the answer comes out one notch low on exact-gap data.
    int n; long long k; in >> n >> k;
    vector<long long> p(n);
    for (auto& x : p) in >> x;
    sort(p.begin(), p.end());
    long long lo = 0, hi = p[n-1] - p[0];
    auto feasible = [&](long long d) {
        long long c = 1, last = p[0];
        for (int i = 1; i < n; ++i) {
            if (p[i] - last > d) { ++c; last = p[i]; }  // off-by-one
        }
        return c >= k;
    };
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        if (feasible(mid)) lo = mid;
        else hi = mid - 1;
    }
    out << lo << "{{NL}}";
""") + END

# ------------------------------------------------------------------ tests
A1_TESTS = [
    contest_test("tiny", T("4 3 6", "1 2 3 4"), T("5"),
        "Subarrays summing in [3,6]: [1,2],[3],[2,3],[4],[1,2,3]? No — [3],[4],[1,2],[2,3],[2,3?]. Six windows checked by brute: 5."),
    contest_test(
        "load: n = 200000",
        T("200000 5000 20000", *["%d" % x for x in _A1_BIG]),
        T(str(_A1_BIG_ANS)),
        "O(n log n) prefix+binary-search; the O(n^2) W is 2e10 steps — timeout."),
]

A2_TESTS = [
    contest_test("with duplicates", T("5", "2 1 2 1 3"), T("3"),
        "Strict pairs a[i] > a[j]: (2,1),(2,1b),(2b,1b) — 3; the equal pair 2=2 is NOT counted."),
    contest_test(
        "load: 200000 values to 1e9",
        T("200000", *["%d" % x for x in _A2_BIG]),
        T(str(_A2_BIG_ANS)),
        "Compression + Fenwick handles sparse values; merge-sort W overcounts equal pairs."),
]

A3_TESTS = [
    contest_test("back-to-back chain", T("3", "0 5", "5 10", "10 15"), T("1"),
        "Interval [a,b) semantics: end == next start means NO overlap — 1 room."),
    contest_test(
        "load: 200000 intervals",
        T(str(len(_A3_IV) // 2), *["%d %d" % iv for iv in _A3_IV[:len(_A3_IV)//2]]),
        T(str(_A3_BIG_ANS)),
        "Sort + heap sweep; the strict-< W overcounts back-to-back meetings."),
]

CP_TESTS = [
    contest_test("exact gaps", T("5 3", "1", "2", "8", "4", "9"), T("3"),
        "Place at 1,4,9: min gap 3. The strict-> W answers 2."),
    contest_test(
        "load: n = 200000, k = 5000",
        T("200000 5000", *["%d" % x for x in _CP_POS]),
        T(str(_CP_ANS)),
        "Binary search on answer + greedy; the off-by-one W loses exactly-one-gaps."),
]

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Technique Synthesis",
    "Problems where two techniques must combine: prefix+search counting, compression+Fenwick, sweep+heap scheduling, and answer-search+greedy.",
    "Tổng hợp kỹ thuật",
    "Bài toán cần ghép hai kỹ thuật: đếm bằng tiền tố+tìm kiếm, nén+Lưới Fenwick, quét+heap, và tìm đáp án+tham lam.",
    ["hsga-m16-combo", "hsga-m16-offline", "hsga-m16-answer"],
    ["hsga-p16-synth"],
)

write_lesson(
    M, "hsga-m16-combo",
    "Prefix Sums + Binary Search",
    "When the prefix array is monotone, every two-condition subarray count becomes two binary searches — one idea, dozens of problems.",
    30,
    """
# Monotone prefixes unlock counting

Positive values make prefix sums increasing; the subarray (i, j] has sum
in [L, R] exactly when P[j]-R <= P[i] <= P[j]-L. Count positions i with
two binary searches. If values can be negative, prefixes stop being
monotone — the same counting then needs BIT/merge-sort (next lesson).
""", "Tổng tiền tố + tìm kiếm nhị phân",
    "Khi mảng tiền tố đơn điệu, mọi phép đếm đoạn với hai điều kiện thành hai phép tìm kiếm nhị phân.",

    """
# Tiền tố đơn điệu mở khóa phép đếm

Giá trị dương làm tổng tiền tố tăng; đoạn (i, j] có tổng trong [L, R]
khi đúng P[j]-R <= P[i] <= P[j]-L. Đếm vị trí i bằng hai lần tìm kiếm.
Giá trị có âm thì tiền tố mất tính đơn điệu — phép đếm đó lúc này cần
BIT/merge-sort (bài sau).
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m16-offline",
    "Compression + Fenwick and Sweep + Heap",
    "Two offline workhorses: compress sparse values then count with a BIT; sweep events by start time with a min-heap of deadlines.",
    30,
    """
# Offline order is a superpower

Inversions over values up to 1e9: compress, walk from the right, count
already-seen smaller ranks with a Fenwick tree. Scheduling: sort by
start, keep end times in a min-heap, pop what has expired. Both are
'process in a smart order, maintain the answer incrementally'. The
subtle bugs live in boundaries: equal elements, touching intervals.
""", "Nén + Fenwick và quét + heap",
    "Hai công cụ ngoại tuyến: nén giá trị thưa rồi đếm bằng BIT; quét sự kiện theo thời điểm bắt đầu với heap nhỏ.",

    """
# Thứ tự ngoại tuyến là siêu năng lực

Nghịch đảo trên giá trị tới 1e9: nén, đi từ phải sang trái, đếm hạng
nhỏ hơn đã gặp bằng Fenwick. Lập lịch: sắp theo thời điểm bắt đầu,
giữ thời điểm kết thúc trong heap-min, pop cái đã hết. Cả hai đều là
'xử lý theo thứ tự khôn ngoan, cập nhật đáp án dần'. Lỗi tinh vi nằm ở
biên: phần tử bằng nhau, khoảng chạm nhau.
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m16-answer",
    "Binary Search on the Answer",
    "When feasibility is monotone in a numeric answer, binary search the answer and verify greedily in O(n).",
    30,
    """
# Searching the answer space

Max-min-distance problems: 'can we place k points with all gaps >= d?'
is monotone in d. Binary search d; the check is a linear greedy. The
off-by-one traps: gaps EXACTLY d count (>=), and the search bounds.
Write the predicate on paper before coding it.
""", "Tìm kiếm nhị phân trên đáp án",
    "Khi tính khả thi đơn điệu theo đáp án số, tìm kiếm nhị phân đáp án và xác nhận tham lam trong O(n).",

    """
# Tìm kiếm trong không gian đáp án

Bài toán max-min-khoảng-cách: 'đặt được k điểm với mọi khoảng >= d?'
đơn điệu theo d. Tìm kiếm nhị phân d; phép kiểm tra là tham khảo tuyến
tính. Các bẫy lệch-một: khoảng ĐÚNG bằng d vẫn tính (>=), và biên tìm
kiếm. Viết vị từ ra giấy trước khi code.
""", difficulty="advanced",
)

write_practice(
    M, "hsga-p16-synth", "Synthesis Gauntlet",
    "Subarray-sum-range counting, inversions over sparse values, interval scheduling, and max-min-distance placement.",
    "Vượt cổng tổng hợp",
    "Đếm đoạn theo dải tổng, nghịch đảo trên giá trị thưa, lập lịch khoảng, và đặt điểm max-min.",
    "hsga-m16-answer",
    120,
    "advanced",
    [
        challenge("hsga-p16-subrange", "Subarray Sum Range",
            """**Problem.** Each query: n L R then n positive values. Print the
number of subarrays with sum in [L, R].

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ a_i ≤ 1000; sums fit in long long.

Prefix + two binary searches; O(n^2) W times out.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p16-inv", "Sparse Inversions",
            """**Problem.** Each query: n then n values up to 1e9 (duplicates
allowed). Print the number of inversions.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ a_i ≤ 10^9.

Compression + Fenwick; the merge-sort W counts equal pairs.
""",
            A2_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p16-rooms", "Meeting Rooms",
            """**Problem.** Each query: n then n intervals s e (endpoints may
touch). Print the minimum number of rooms.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ s < e ≤ 10^9; [a,b) semantics —
a meeting ending at t does not overlap one starting at t.

Sweep + min-heap; the strict-< W overcounts touching intervals.
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    {
        "hsga-p16-synth": vi_challenge(
            "Vượt cổng tổng hợp",
            """**Bài toán.** Ba bài (mỗi bài một truy vấn): đếm đoạn theo dải tổng,
nghịch đảo trên giá trị thưa tới 1e9, và số phòng họp tối thiểu.""",
            [("đoạn tổng", "Tiền tố đơn điệu + hai tìm kiếm nhị phân."),
             ("nghịch đảo", "Nén + Fenwick; cặp bằng KHÔNG đếm."),
             ("phòng họp", "[a,b): kết thúc bằng bắt đầu KHÔNG chồng.")],
        ),
    },
    solutions=[
        ("hsga-p16-subrange", A1_R, A1_W),
        ("hsga-p16-inv", A2_R, A2_W),
        ("hsga-p16-rooms", A3_R, A3_W),
    ],
)

write_checkpoint(
    M, "hsga-cp-m16",
    "Checkpoint — Answer Search",
    "Max-min placement graded on exact-gap data where the off-by-one feasibility check fails; brute force cannot save you at n = 200000.",
    40,
    """
**Checkpoint — Answer Search.** Each query: n k then n positions.
Print the largest d such that k positions can be chosen with every
consecutive gap >= d.

Binary search d, greedy check: gaps EXACTLY d are allowed.
""",
    "Điểm kiểm tra — Tìm đáp án",
    "Đặt điểm max-min chấm trên dữ liệu khoảng đúng-bằng nơi phép kiểm tra lệch-một thất bại.",
    """
**Checkpoint — Tìm đáp án.** Mỗi truy vấn: n k rồi n vị trí. In d
lớn nhất sao cho chọn được k vị trí với mọi khoảng liên tiếp >= d.

Tìm kiếm nhị phân d, kiểm tra tham lam: khoảng ĐÚNG bằng d vẫn được.
""",
    challenge(
        "hsga-cp-m16-maxmin",
        "Max-Min Placement",
        """**Problem.** Each query: n k then n positions. Print the largest d
with k chosen positions, consecutive gaps >= d.

**Constraints:** 1 ≤ k ≤ n ≤ 200000; 0 ≤ p_i ≤ 10^9.

The W uses a strict > in the feasibility check — fails on exact gaps.
""",
        CP_TESTS,
        level="real-world",
        difficulty="advanced",
    ),
    vi_challenge(
        "Đặt điểm max-min",
        """**Bài toán.** Mỗi truy vấn: n k rồi n vị trí. In d lớn nhất với k vị
trí được chọn, khoảng liên tiếp >= d.""",
        [("tìm đáp án", "Đơn điệu theo d: tìm kiếm nhị phân."),
         ("tham lam", "Đặt tại vị trí đầu tiên cách >= d."),
         ("bẫy", "Khoảng ĐÚNG bằng d phải được chấp nhận (>=).")],
    ),
    solution=CP_M16_R,
    wrong=CP_M16_W,
)

print("module m16 complete")
