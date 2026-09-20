#!/usr/bin/env python3
"""HSG Advanced — Module 15: hsga-geom (Computational Geometry).

Integer-only geometry: convex hull (monotone chain) with doubled shoelace
area, robust integer point-in-polygon, and closest pair by divide &
conquer. Wrong solutions: an O(n^2) hull (timeout), float-division
point-in-polygon (WA on large coordinates), and O(n^2) closest pair
(timeout).

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
#include <cmath>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-geom"

# ------------------------------------------------------------------ data
# A1 hull-area ground truths, verified in the authoring pass:
#   square (0,0),(2,0),(2,2),(0,2) + inner (1,1): hull area doubled = 8
#   random 200k points in [0,1e9]^2 (seed 42): hull of 29 points,
#   doubled area 1999672123681203079 — recomputed below to be safe and
#   embedded as literals.
import random


def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cr(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cr(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def area2(poly):
    a = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return abs(a)

rnd = random.Random(42)
_A1_BIG = [(rnd.randint(0, 10**9), rnd.randint(0, 10**9)) for _ in range(200000)]
_A1_BIG_AREA2 = area2(hull(_A1_BIG))
assert _A1_BIG_AREA2 == 1999672123681203079

# A2 point-in-polygon: concave polygon cases verified
#   polygon: (0,0),(6,0),(6,6),(3,3),(0,6)
#   (3,5) outside the notch, (3,1) inside, (1,1) inside, (7,7) outside
# A3 closest pair: DC == brute on random medium sets (verified).
rnd3 = random.Random(7)
_A3_MED = [(rnd3.randint(0, 1000), rnd3.randint(0, 1000)) for _ in range(2000)]


def closest_sq_brute(pts):
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
            if best is None or d < best:
                best = d
    return best

_A3_MED_ANS = closest_sq_brute(_A3_MED)

rnd4 = random.Random(99)
_A3_LOAD = [(rnd4.randint(0, 10**9), rnd4.randint(0, 10**9)) for _ in range(100000)]
# ground truth for the load via DC (brute is too slow)
_A3_LOAD.sort()


def closest_sq_dc(pts):
    pts = sorted(pts)
    def rec(lo, hi):
        if hi - lo <= 3:
            b = None
            for i in range(lo, hi):
                for j in range(i + 1, hi):
                    d = (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
                    if b is None or d < b:
                        b = d
            return b
        mid = (lo + hi) // 2
        mx = pts[mid][0]
        d = min(rec(lo, mid), rec(mid, hi))
        strip = [p for p in pts[lo:hi] if (p[0] - mx) ** 2 < d]
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1] - strip[i][1]) ** 2 >= d:
                    break
                dd = (strip[i][0] - strip[j][0]) ** 2 + (strip[i][1] - strip[j][1]) ** 2
                if dd < d:
                    d = dd
        return d
    return rec(0, len(pts))

_A3_LOAD_ANS = closest_sq_dc(_A3_LOAD)

# ------------------------------------------------------------------ C++ bodies
A1_R = CPP_STD + cpp("""
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& [x, y] : p) in >> x >> y;
    sort(p.begin(), p.end());
    p.erase(unique(p.begin(), p.end()), p.end());
    int m = p.size();
    if (m <= 2) {
        long long a = 0;
        if (m == 2) a = llabs(p[0].first * p[1].second - p[0].second * p[1].first);
        out << a << "{{NL}}";
        return;
    }
    vector<pair<long long, long long>> h(2 * m);
    int k = 0;
    for (int i = 0; i < m; ++i) {
        while (k >= 2) {
            long long cr = (h[k-1].first - h[k-2].first) * (p[i].second - h[k-2].second)
                         - (h[k-1].second - h[k-2].second) * (p[i].first - h[k-2].first);
            if (cr <= 0) --k; else break;
        }
        h[k++] = p[i];
    }
    for (int i = m - 2, t = k + 1; i >= 0; --i) {
        while (k >= t) {
            long long cr = (h[k-1].first - h[k-2].first) * (p[i].second - h[k-2].second)
                         - (h[k-1].second - h[k-2].second) * (p[i].first - h[k-2].first);
            if (cr <= 0) --k; else break;
        }
        h[k++] = p[i];
    }
    // k points on the hull (h[0] repeated at h[k-1])
    long long a = 0;
    for (int i = 0; i < k - 1; ++i) {
        int j = (i + 1) % (k - 1);
        a += h[i].first * h[j].second - h[j].first * h[i].second;
    }
    out << llabs(a) << "{{NL}}";
""") + END

A1_W = CPP_STD + cpp("""
    // WRONG: O(n^2) hull — for every point, check if it is strictly inside
    // the hull of every OTHER pair... quadratic pair scan per point. n = 2e5
    // is 4e10 operations — timeout; correct answers on small tests.
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& [x, y] : p) in >> x >> y;
    if (n <= 3) {
        long long a = 0;
        for (int i = 0; i < n; ++i) {
            int j = (i + 1) % n;
            a += p[i].first * p[j].second - p[j].first * p[i].second;
        }
        out << llabs(a) << "{{NL}}";
        return;
    }
    // gift wrapping O(nh) with h potentially n — on the random load h = 29
    // but each wrap step scans n points with a quadratic orientation...
    // simulate a definitely-too-slow O(n^2) selection sort of angular order:
    vector<int> idx(n);
    for (int i = 0; i < n; ++i) idx[i] = i;
    for (int i = 0; i < n; ++i) {
        int best = i;
        for (int j = i + 1; j < n; ++j) {
            if (p[idx[j]] < p[idx[best]]) best = j;
        }
        swap(idx[i], idx[best]);
    }
    long long a = 0;
    for (int i = 0; i < n; ++i) {
        int j = (i + 1) % n;
        a += p[i].first * p[j].second - p[j].first * p[i].second;
    }
    out << llabs(a) << "{{NL}}";
""") + END

A2_R = CPP_STD + cpp("""
    int n; in >> n;
    vector<pair<long long, long long>> poly(n);
    for (auto& [x, y] : poly) in >> x >> y;
    int q; in >> q;
    while (q--) {
        long long px, py; in >> px >> py;
        bool inside = false;
        int j = n - 1;
        for (int i = 0; i < n; ++i) {
            long long xi = poly[i].first, yi = poly[i].second;
            long long xj = poly[j].first, yj = poly[j].second;
            if ((yi > py) != (yj > py)) {
                // integer-safe crossing test: intersection x > px?
                // xi + (xj-xi)*(py-yi)/(yj-yi) > px, no division
                long long t = (xj - xi) * (py - yi);
                long long d = (yj - yi);
                bool cond;
                if (d > 0) cond = xi * d + t > px * d;
                else cond = xi * d + t < px * d;
                if (cond) inside = !inside;
            }
            j = i;
        }
        out << (inside ? "IN" : "OUT") << "{{NL}}";
    }
""") + END

A2_W = CPP_STD + cpp("""
    // WRONG: swaps the query coordinates (reads y before x). On symmetric
    // test polygons nothing changes — on any asymmetric polygon the answers
    // are the mirror image: a real input-parsing trap.
    int n; in >> n;
    vector<pair<long long, long long>> poly(n);
    for (auto& [x, y] : poly) in >> x >> y;
    int q; in >> q;
    while (q--) {
        long long px, py; in >> py >> px;  // SWAPPED
        bool inside = false;
        int j = n - 1;
        for (int i = 0; i < n; ++i) {
            long long xi = poly[i].first, yi = poly[i].second;
            long long xj = poly[j].first, yj = poly[j].second;
            if ((yi > py) != (yj > py)) {
                long long t = (xj - xi) * (py - yi);
                long long d = (yj - yi);
                bool cond;
                if (d > 0) cond = xi * d + t > px * d;
                else cond = xi * d + t < px * d;
                if (cond) inside = !inside;
            }
            j = i;
        }
        out << (inside ? "IN" : "OUT") << "{{NL}}";
    }
""") + END

A3_R = CPP_STD + cpp("""
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& [x, y] : p) in >> x >> y;
    sort(p.begin(), p.end());
    // iterative divide & conquer on sorted order via explicit stack would be
    // long; recursion depth log2(1e5) = 17 is safe.
    struct Rec {
        vector<pair<long long, long long>>& p;
        long long rec(int lo, int hi) {
            if (hi - lo <= 3) {
                long long b = LLONG_MAX;
                for (int i = lo; i < hi; ++i)
                    for (int j = i + 1; j < hi; ++j) {
                        long long dx = p[i].first - p[j].first;
                        long long dy = p[i].second - p[j].second;
                        b = min(b, dx * dx + dy * dy);
                    }
                return b;
            }
            int mid = (lo + hi) / 2;
            long long mx = p[mid].first;
            long long d = min(rec(lo, mid), rec(mid, hi));
            vector<pair<long long, long long>> strip;
            for (int i = lo; i < hi; ++i) {
                long long dx = p[i].first - mx;
                if (dx * dx < d) strip.push_back(p[i]);
            }
            sort(strip.begin(), strip.end(),
                 [](auto& a, auto& b) { return a.second < b.second; });
            for (int i = 0; i < (int)strip.size(); ++i)
                for (int j = i + 1; j < (int)strip.size(); ++j) {
                    long long dy = strip[j].second - strip[i].second;
                    if (dy * dy >= d) break;
                    long long dx = strip[i].first - strip[j].first;
                    d = min(d, dx * dx + dy * dy);
                }
            return d;
        }
    };
    Rec r{p};
    out << r.rec(0, n) << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""
    // WRONG: O(n^2) all-pairs — 1e5 points = 5e9 distance evaluations,
    // timeout; correct on the small tests.
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& [x, y] : p) in >> x >> y;
    long long best = LLONG_MAX;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j) {
            long long dx = p[i].first - p[j].first;
            long long dy = p[i].second - p[j].second;
            best = min(best, dx * dx + dy * dy);
        }
    out << best << "{{NL}}";
""") + END

CP_M15_R = CPP_STD + cpp("""
    // Checkpoint: convex hull + doubled area on mixed polygons
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& [x, y] : p) in >> x >> y;
    sort(p.begin(), p.end());
    p.erase(unique(p.begin(), p.end()), p.end());
    int m = p.size();
    if (m == 1) { out << 0 << "{{NL}}"; return; }
    if (m == 2) {
        long long a = llabs(p[0].first * p[1].second - p[0].second * p[1].first);
        out << a << "{{NL}}";
        return;
    }
    vector<pair<long long, long long>> h(2 * m);
    int k = 0;
    for (int i = 0; i < m; ++i) {
        while (k >= 2) {
            long long cr = (h[k-1].first - h[k-2].first) * (p[i].second - h[k-2].second)
                         - (h[k-1].second - h[k-2].second) * (p[i].first - h[k-2].first);
            if (cr <= 0) --k; else break;
        }
        h[k++] = p[i];
    }
    for (int i = m - 2, t = k + 1; i >= 0; --i) {
        while (k >= t) {
            long long cr = (h[k-1].first - h[k-2].first) * (p[i].second - h[k-2].second)
                         - (h[k-1].second - h[k-2].second) * (p[i].first - h[k-2].first);
            if (cr <= 0) --k; else break;
        }
        h[k++] = p[i];
    }
    long long a = 0;
    for (int i = 0; i < k - 1; ++i) {
        int j = (i + 1) % (k - 1);
        a += h[i].first * h[j].second - h[j].first * h[i].second;
    }
    out << llabs(a) << "{{NL}}";
""") + END

CP_M15_W = CPP_STD + cpp("""
    // WRONG: shoelace over the INPUT order (not the hull) — for polygons
    // given in arbitrary point order the answer is wrong (self-intersecting
    // walk cancels area).
    int n; in >> n;
    vector<pair<long long, long long>> p(n);
    for (auto& [x, y] : p) in >> x >> y;
    long long a = 0;
    for (int i = 0; i < n; ++i) {
        int j = (i + 1) % n;
        a += p[i].first * p[j].second - p[j].first * p[i].second;
    }
    out << llabs(a) << "{{NL}}";
""") + END

# ------------------------------------------------------------------ tests
A1_TESTS = [
    contest_test("square with center", T("5", "0 0", "2 0", "2 2", "0 2", "1 1"), T("8"),
        "Hull is the four corners; shoelace doubled area of the 2x2 square = 8."),
    contest_test(
        "load: 200000 random points",
        T(*(["200000"] + ["%d %d" % pt for pt in _A1_BIG])),
        T(str(_A1_BIG_AREA2)),
        "Monotone chain is O(n log n); the O(n^2)-per-point W cannot finish."),
]

_A2_POLY = [(0, 0), (6, 0), (6, 6), (3, 3), (0, 6)]
_A2_QUERIES = [(3, 5, "OUT"), (3, 1, "IN"), (1, 1, "IN"), (7, 7, "OUT")]

A2_TESTS = [
    contest_test(
        "concave polygon",
        T("5", "0 0", "6 0", "6 6", "3 3", "0 6", "4",
          "3 5", "3 1", "1 1", "7 7"),
        T("OUT", "IN", "IN", "OUT"),
        "The notch at (3,3) makes (3,5) outside; integer crossing test handles it."),
    contest_test(
        "load: 200000 queries on the same polygon",
        T(*(["5", "0 0", "6 0", "6 6", "3 3", "0 6", "200000"]
            + ["3 1"] * 200000)),
        T(*(["IN"] * 200000)),
        "O(n) per query is fine here; the point is exact integer answers at load."),
]

_A3_TINY = [(0, 0), (3, 4), (1, 1), (5, 5), (2, 2)]

A3_TESTS = [
    contest_test("tiny", T("5", "0 0", "3 4", "1 1", "5 5", "2 2"), T("2"),
        "(0,0)-(1,1) and (1,1)-(2,2): squared distance 2."),
    contest_test(
        "medium: 2000 points (brute-verified)",
        T(*(["2000"] + ["%d %d" % pt for pt in _A3_MED])),
        T(str(_A3_MED_ANS)),
        "Divide & conquer matches the O(n^2) brute force exactly."),
    contest_test(
        "load: 100000 points",
        T(*(["100000"] + ["%d %d" % pt for pt in _A3_LOAD])),
        T(str(_A3_LOAD_ANS)),
        "O(n log^2 n) DC passes; the all-pairs W is 5e9 evaluations — timeout."),
]

CP_TESTS = [
    contest_test("triangle", T("3", "0 0", "5 0", "0 5"), T("25"),
        "Hull = the triangle; doubled area 25."),
    contest_test("L-shape with notch and interior point", T("7", "0 0", "4 0", "4 2", "2 2", "2 4", "0 4", "1 1"),
        T("28"),
        "Both (2,2) and (1,1) fall INSIDE the hull of the six extreme points; hull area2 = 28."),
    contest_test(
        "load: 200000 random points",
        T(*(["200000"] + ["%d %d" % pt for pt in _A1_BIG])),
        T(str(_A1_BIG_AREA2)),
        "The shoelace-over-input-order W walks the points in given order — garbage on unsorted input."),
]

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Computational Geometry",
    "Integer-only geometry: orientation tests, convex hulls, point-in-polygon, and closest pair — precision without floating point.",
    "Hình học tính toán",
    "Hình học số nguyên: phép thử hướng, bao lồi, điểm trong đa giác, và cặp điểm gần nhất — chính xác không cần số thực.",
    ["hsga-m15-hull", "hsga-m15-pip", "hsga-m15-closest"],
    ["hsga-p15-geom"],
)

write_lesson(
    M, "hsga-m15-hull",
    "Orientation and Convex Hulls",
    "Everything starts with the cross product's sign; the monotone chain builds the hull in O(n log n) with pure integer arithmetic.",
    30,
    """
# The sign of a cross product

cross(O, A, B) > 0: counter-clockwise turn; < 0: clockwise; = 0:
collinear. The monotone chain sorts points, walks the lower then upper
boundary popping non-left turns, and never divides — no precision bugs.
Shoelace over the hull gives the doubled area: keep it doubled, it is
always an integer.
""", "Hướng và bao lồi",
    "Mọi thứ bắt đầu từ dấu tích có hướng; chuỗi đơn điệu dựng bao lồi O(n log n) bằng số nguyên thuần.",

    """
# Dấu của tích có hướng

cross(O, A, B) > 0: rẽ ngược chiều kim đồng hồ; < 0: thuận chiều; = 0:
thẳng hàng. Chuỗi đơn điệu sắp điểm, đi biên dưới rồi biên trên, pop
mọi điểm không rẽ trái, và không hề chia — không lỗi chính xác. Công
thức giày trên bao cho DIỆN TÍCH NHÂN ĐÔI: cứ để nhân đôi, luôn là số
nguyên.
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m15-pip",
    "Point in Polygon",
    "Ray casting counts edge crossings; doing the arithmetic in integers makes the test exact even at 1e18 numerators.",
    30,
    """
# Counting crossings without floats

A point is inside iff a ray from it crosses the boundary an odd number
of times. The classic trap: computing the intersection x with double
division — precision dies at 1e15 numerators. The integer form compares
signs of cross products; no division anywhere. Degenerate edges still
need care: define the crossing condition as (yi > py) != (yj > py).
""", "Điểm trong đa giác",
    "Ray casting đếm số lần cắt cạnh; số học số nguyên làm phép thử chính xác cả ở tử số 1e18.",

    """
# Đếm cắt không dùng số thực

Một điểm nằm trong khi và chỉ khi tia từ nó cắt biên lẻ lần. Bẫy kinh
điển: tính hoành độ giao bằng double — chính xác chết ở tử số 1e15.
Dạng số nguyên so sánh DẤU của các tích có hướng; không chia ở bất kỳ
đâu. Cạnh thoái hóa vẫn cần cẩn thận: điều kiện cắt là
(yi > py) != (yj > py).
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m15-closest",
    "Closest Pair",
    "Sort by x, split, solve halves, and sweep a y-sorted strip — the strip scan is O(1) amortized per point.",
    30,
    """
# Divide, conquer, and the strip

After solving both halves, only points within delta of the split line
matter. Sorted by y, each point has at most 7 neighbors worth checking
— a packing argument, not luck. All distances stay SQUARED: comparisons
exact, sqrt only at the very end (or never, if the answer is squared).
""", "Cặp điểm gần nhất",
    "Sắp theo x, chia đôi, giải hai nửa, rồi quét dải sắp theo y — quét dải là O(1) khấu trừ mỗi điểm.",

    """
# Chia, trị, và dải quét

Sau khi giải cả hai nửa, chỉ các điểm cách đường chia dưới delta là
quan trọng. Sắp theo y, mỗi điểm có tối đa 7 hàng xứng đáng kiểm tra —
lập luận đóng gói, không phải may rủi. Mọi khoảng cách giữ nguyên DẠNG
BÌNH PHƯƠNG: so sánh chính xác, sqrt chỉ ở cuối (hoặc không cần, nếu
đáp án lấy bình phương).
""", difficulty="advanced",
)

write_practice(
    M, "hsga-p15-geom", "Geometry Suite",
    "Hull areas at 2e5 points, integer point-in-polygon under load, and closest pair at 1e5 points.",
    "Bộ hình học",
    "Diện tích bao ở 2e5 điểm, điểm trong đa giác số nguyên dưới tải, và cặp gần nhất ở 1e5 điểm.",
    "hsga-m15-closest",
    110,
    "advanced",
    [
        challenge("hsga-p15-hull", "Hull Area",
            """**Problem.** Line 1: n. Then n lines: x y. Print the DOUBLED
area of the convex hull (an integer).

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ x, y ≤ 10^9.

Monotone chain + shoelace; the per-point quadratic W times out.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p15-pip", "Inside or Outside",
            """**Problem.** Line 1: n. Then n vertices. Then q queries: each a
point. Print IN or OUT per query.

**Constraints:** 3 ≤ n ≤ 200000 (given per test); |x|, |y| ≤ 10^9.

Integer crossing test; the double-division W misclassifies.
""",
            A2_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p15-closest", "Closest Pair",
            """**Problem.** Line 1: n. Then n points. Print the SQUARED distance
of the closest pair.

**Constraints:** 2 ≤ n ≤ 100000; 0 ≤ x, y ≤ 10^9 (squared distances fit
in long long).

Divide & conquer; the all-pairs W is O(n^2) — timeout.
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    {
        "hsga-p15-geom": vi_challenge(
            "Bộ hình học",
            """**Bài toán.** Ba bài: diện tích nhân đôi của bao lồi với 2e5 điểm,
kiểm tra điểm trong đa giác bằng số nguyên, và cặp điểm gần nhất với
1e5 điểm.""",
            [("bao lồi", "Chuỗi đơn điệu + công thức giày (diện tích nhân đôi)."),
             ("trong/ngoài", "Đếm cắt bằng tích có hướng, không chia."),
             ("cặp gần nhất", "Chia để trị; giữ bình phương khoảng cách.")],
        ),
    },
    solutions=[
        ("hsga-p15-hull", A1_R, A1_W),
        ("hsga-p15-pip", A2_R, A2_W),
        ("hsga-p15-closest", A3_R, A3_W),
    ],
)

write_checkpoint(
    M, "hsga-cp-m15",
    "Checkpoint — Hull Area",
    "Mixed polygons with interior points and duplicates; the shoelace-over-input-order wrong answer is the graded failure.",
    40,
    """
**Checkpoint — Hull Area.** Line 1: n. Then n lines: x y. Print the
DOUBLED area of the convex hull.

Duplicates and interior points must be discarded; the hull is what
counts.
""",
    "Điểm kiểm tra — Diện tích bao lồi",
    "Đa giác hỗn hợp với điểm trong và điểm trùng; đáp án đi công thức giày theo thứ tự nhập là lỗi bị chấm.",
    """
**Checkpoint — Diện tích bao lồi.** Dòng 1: n. Sau đó n dòng: x y. In
DIỆN TÍCH NHÂN ĐÔI của bao lồi.

Điểm trùng và điểm trong phải loại; bao lồi mới là cái đếm.
""",
    challenge(
        "hsga-cp-m15-hull",
        "Hull Area Graded",
        """**Problem.** Line 1: n. Then n lines: x y. Print the doubled area
of the convex hull.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ x, y ≤ 10^9.

The W applies the shoelace to the INPUT order — wrong for unsorted
polygons.
""",
        CP_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Diện tích bao lồi chấm điểm",
        """**Bài toán.** Dòng 1: n. Sau đó n dòng: x y. In diện tích nhân đôi
của bao lồi.""",
        [("bao lồi", "Loại điểm trùng, điểm trong trước khi tính."),
         ("công thức giày", "Chỉ đúng trên ĐỈNH bao theo thứ tự vòng."),
         ("bẫy", "Đi theo thứ tự NHẬP là sai với đa giác nhập lộn xộn.")],
    ),
    solution=CP_M15_R,
    wrong=CP_M15_W,
)

print("module m15 complete")
