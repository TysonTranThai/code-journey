#!/usr/bin/env python3
"""HSG Advanced — Module 14: hsga-combi (Combinatorics).

Catalan numbers via the binomial identity, inclusion-exclusion over up to
4 divisibility conditions, and lattice paths avoiding a forbidden cell.
Wrong solutions: Pascal-recursion Catalan (timeout), per-query sieve
double counting, and an inclusion-exclusion that forgets the pairwise
LCM correction terms (behavioral).

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

M = "hsga-combi"

MOD = 10**9 + 7

# ------------------------------------------------------------------ data
# Factorial tables to 2e6 (largest n+m used is 2*10^6 for A3 load).
# Values computed here by the same closed-form model verified against
# brute force below; the asserts are the authoring-time cross-check.
NMAX = 2 * 10**6 + 1
fact = [1] * NMAX
for i in range(1, NMAX):
    fact[i] = fact[i - 1] * i % MOD
inv_fact = [1] * NMAX
inv_fact[NMAX - 1] = pow(fact[NMAX - 1], MOD - 2, MOD)
for i in range(NMAX - 1, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD


def C(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD


def catalan(n):
    if n == 0:
        return 1
    return (C(2 * n, n) - C(2 * n, n + 1)) % MOD

# cross-check small Catalans against the classic sequence
assert [catalan(n) for n in range(6)] == [1, 1, 2, 5, 14, 42]
assert catalan(10) == 16796

# A1 load: n = 1..500000
_CAT_ANS = [catalan(n) for n in range(1, 500001)]
assert len(_CAT_ANS) == 500000

# A2 inclusion-exclusion: divisor sets, verified against brute force
def cnt_ie(N, ds):
    from itertools import combinations
    import math
    total = 0
    for r in range(1, len(ds) + 1):
        for comb in combinations(ds, r):
            l = math.lcm(*comb)
            total += (-1) ** (r + 1) * (N // l)
    return total

assert cnt_ie(1000, (2, 3, 5)) == sum(1 for x in range(1, 1001) if x % 2 == 0 or x % 3 == 0 or x % 5 == 0)
assert cnt_ie(100, (2, 3)) == 67

# Query line format: "N k d1 .. dk" (k explicit, then k divisors).
_A2_QUERIES = [
    ("1000 3", "2 3 5"),
    ("100 2", "2 3"),
    ("999999999999 4", "2 3 5 7"),
    ("1000000000000 3", "4 6 9"),
    ("123456789 3", "7 11 13"),
    ("500000000 4", "3 5 7 11"),
]
_A2_ANS = [str(cnt_ie(int(n.split()[0]), tuple(map(int, d.split())))) for (n, d) in _A2_QUERIES]

# A3 lattice paths n x m avoiding one cell (verified vs brute force)
def paths(n, m, bad):
    bx, by = bad
    if bx > n or by > m:
        return C(n + m, n) % MOD
    return (C(n + m, n) - C(bx + by, bx) * C(n + m - bx - by, n - bx)) % MOD


def brute_paths(n, m, bad):
    from functools import lru_cache

    @lru_cache(None)
    def f(x, y):
        if (x, y) == bad:
            return 0
        if x == n and y == m:
            return 1
        t = 0
        if x < n:
            t += f(x + 1, y)
        if y < m:
            t += f(x, y + 1)
        return t

    return f(0, 0)

assert paths(3, 3, (1, 1)) == brute_paths(3, 3, (1, 1))
assert paths(2, 2, (9, 9)) == C(4, 2) == 6

_A3_QUERIES = [
    ("3 3", "1 1"),
    ("2 2", "9 9"),   # outside grid: total C(4,2)=6
    ("1000 1000", "500 333"),
    ("500000 500000", "1 1"),
    ("1000000 1000000", "500000 500000"),
]
_A3_ANS = []
for (nm, b) in _A3_QUERIES:
    n, m = map(int, nm.split())
    bx, by = map(int, b.split())
    if bx > n or by > m:
        _A3_ANS.append(str(C(n + m, n) % MOD))
    else:
        _A3_ANS.append(str(paths(n, m, (bx, by))))

# CP: balanced brackets count == Catalan, plus one combinatorial identity
_CP_ANS = [
    str(catalan(3)),           # n=3 -> 5
    str(catalan(1)),           # n=1 -> 1
    str(catalan(19)),          # under 64-bit but big
    str(catalan(500000)),      # load
    str(catalan(499999)),
]
assert catalan(19) == 767263183  # C_19 = 1767263190 mod 1e9+7

# ------------------------------------------------------------------ C++ bodies
A1_R = CPP_STD + cpp("""
    const long long P = 1000000007LL;
    const int NMAX = 1000001;
    static long long f[NMAX], inv[NMAX];
    auto pw = [](long long a, long long e, long long m) {
        long long r = 1 % m; a %= m;
        while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; }
        return r;
    };
    f[0] = 1;
    for (int i = 1; i < NMAX; ++i) f[i] = f[i-1] * i % P;
    inv[NMAX-1] = pw(f[NMAX-1], P - 2, P);
    for (int i = NMAX - 1; i > 0; --i) inv[i-1] = inv[i] * i % P;
    auto bin = [&](long long n, long long r) -> long long {
        if (r < 0 || r > n) return 0;
        return f[n] * inv[r] % P * inv[n-r] % P;
    };
    int q; in >> q;
    while (q--) {
        int n; in >> n;
        long long v = (bin(2LL*n, n) - bin(2LL*n, n + 1) % P + P) % P;
        out << v << "{{NL}}";
    }
""") + END

A1_W = CPP_STD + cpp("""
    // WRONG: recomputes Catalan by the O(n^2) Pascal-style recurrence
    // cat(n) = sum cat(i)*cat(n-1-i) per query — 500000 queries at n = 5e5
    // is astronomically slow; even the tiny tests crawl past the limit.
    const long long P = 1000000007LL;
    int q; in >> q;
    while (q--) {
        int n; in >> n;
        // O(n^2) per query: correct but 500000 queries at n = 5e5 is
        // 2.5e11 multiply-mods — minutes, not seconds. The trap: it even
        // gives RIGHT answers on small n.
        static long long cat[500001];
        static bool done = false;
        if (!done) {
            cat[0] = 1;
            for (int k = 1; k <= 500000; ++k) {
                long long s = 0;
                for (int i = 0; i < k; ++i)
                    s = (s + cat[i] * cat[k-1-i]) % P;
                cat[k] = s;
            }
            done = true;
        }
        out << cat[n] << "{{NL}}";
    }
""") + END

A2_R = CPP_STD + cpp("""
    auto gcd2 = [](long long a, long long b) {
        while (b) { long long t = a % b; a = b; b = t; }
        return a;
    };
    int q; in >> q;
    while (q--) {
        long long N; int k; in >> N >> k;
        vector<long long> d(k);
        for (auto& x : d) in >> x;
        long long total = 0;
        for (int mask = 1; mask < (1 << k); ++mask) {
            long long l = 1; int bits = 0; bool ok = true;
            for (int i = 0; i < k; ++i) if (mask & (1 << i)) {
                ++bits;
                long long g = gcd2(l, d[i]);
                l = l / g * d[i];
                if (l > N) { ok = false; break; }
            }
            if (!ok) continue;
            long long term = N / l;
            total += (bits & 1) ? term : -term;
        }
        out << total << "{{NL}}";
    }
""") + END

A2_W = CPP_STD + cpp("""
    // WRONG: adds N/d for every divisor but forgets the pairwise LCM
    // subtraction terms (and beyond) — double counts multiples of two or
    // more divisors.
    int q; in >> q;
    while (q--) {
        long long N; int k; in >> N >> k;
        long long total = 0;
        for (int i = 0; i < k; ++i) {
            long long d; in >> d;
            total += N / d;
        }
        out << total << "{{NL}}";
    }
""") + END

A3_R = CPP_STD + cpp("""
    const long long P = 1000000007LL;
    const int NMAX = 2000001;
    static long long f[NMAX], inv[NMAX];
    auto pw = [](long long a, long long e, long long m) {
        long long r = 1 % m; a %= m;
        while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; }
        return r;
    };
    f[0] = 1;
    for (int i = 1; i < NMAX; ++i) f[i] = f[i-1] * i % P;
    inv[NMAX-1] = pw(f[NMAX-1], P - 2, P);
    for (int i = NMAX - 1; i > 0; --i) inv[i-1] = inv[i] * i % P;
    auto bin = [&](long long n, long long r) -> long long {
        if (r < 0 || r > n) return 0;
        return f[n] * inv[r] % P * inv[n-r] % P;
    };
    int q; in >> q;
    while (q--) {
        long long n, m, bx, by; in >> n >> m >> bx >> by;
        if (bx > n || by > m) { out << bin(n + m, n) << "{{NL}}"; continue; }
        long long bad = bin(bx + by, bx) * bin(n + m - bx - by, n - bx) % P;
        long long total = ((bin(n + m, n) - bad) % P + P) % P;
        out << total << "{{NL}}";
    }
""") + END

A3_W = CPP_STD + cpp("""
    // WRONG: prints (total - bad) % P WITHOUT the +P fix-up — whenever the
    // reduced bad-product exceeds the reduced total, the printed value is
    // negative (or the raw wrap), a real mod-arithmetic trap.
    const long long P = 1000000007LL;
    const int NMAX = 2000001;
    static long long f[NMAX], inv[NMAX];
    auto pw = [](long long a, long long e, long long m) {
        long long r = 1 % m; a %= m;
        while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; }
        return r;
    };
    f[0] = 1;
    for (int i = 1; i < NMAX; ++i) f[i] = f[i-1] * i % P;
    inv[NMAX-1] = pw(f[NMAX-1], P - 2, P);
    for (int i = NMAX - 1; i > 0; --i) inv[i-1] = inv[i] * i % P;
    auto bin = [&](long long n, long long r) -> long long {
        if (r < 0 || r > n) return 0;
        return f[n] * inv[r] % P * inv[n-r] % P;
    };
    int q; in >> q;
    while (q--) {
        long long n, m, bx, by; in >> n >> m >> bx >> by;
        if (bx > n || by > m) { out << bin(n + m, n) << "{{NL}}"; continue; }
        long long bad = bin(bx + by, bx) * bin(n + m - bx - by, n - bx) % P;
        long long total = (bin(n + m, n) - bad) % P;  // NO +P: can go negative
        out << total << "{{NL}}";
    }
""") + END

CP_M14_R = CPP_STD + cpp("""
    const long long P = 1000000007LL;
    const int NMAX = 1000001;
    static long long f[NMAX], inv[NMAX];
    auto pw = [](long long a, long long e, long long m) {
        long long r = 1 % m; a %= m;
        while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; }
        return r;
    };
    f[0] = 1;
    for (int i = 1; i < NMAX; ++i) f[i] = f[i-1] * i % P;
    inv[NMAX-1] = pw(f[NMAX-1], P - 2, P);
    for (int i = NMAX - 1; i > 0; --i) inv[i-1] = inv[i] * i % P;
    auto bin = [&](long long n, long long r) -> long long {
        if (r < 0 || r > n) return 0;
        return f[n] * inv[r] % P * inv[n-r] % P;
    };
    int q; in >> q;
    while (q--) {
        long long n; in >> n;
        long long v = ((bin(2LL*n, n) - bin(2LL*n, n + 1)) % P + P) % P;
        out << v << "{{NL}}";
    }
""") + END

CP_M14_W = CPP_STD + cpp("""
    // WRONG: answers bin(2n, n) (the CENTRAL binomial) instead of the
    // Catalan number — looks plausible, passes nothing but n=1.
    const long long P = 1000000007LL;
    const int NMAX = 1000001;
    static long long f[NMAX], inv[NMAX];
    auto pw = [](long long a, long long e, long long m) {
        long long r = 1 % m; a %= m;
        while (e) { if (e & 1) r = r * a % m; a = a * a % m; e >>= 1; }
        return r;
    };
    f[0] = 1;
    for (int i = 1; i < NMAX; ++i) f[i] = f[i-1] * i % P;
    inv[NMAX-1] = pw(f[NMAX-1], P - 2, P);
    for (int i = NMAX - 1; i > 0; --i) inv[i-1] = inv[i] * i % P;
    auto bin = [&](long long n, long long r) -> long long {
        if (r < 0 || r > n) return 0;
        return f[n] * inv[r] % P * inv[n-r] % P;
    };
    int q; in >> q;
    while (q--) {
        long long n; in >> n;
        out << bin(2LL*n, n) << "{{NL}}";
    }
""") + END

# ------------------------------------------------------------------ tests
_C20 = catalan(20)
A1_TESTS = [
    contest_test("small", T("5", "1", "2", "3", "4", "5"), T("1", "2", "5", "14", "42"),
        "The Catalan sequence 1, 2, 5, 14, 42."),
    contest_test("n = 20", T("1", "20"), T(str(_C20)),
        "C_20 = 6564120420 mod 1e9+7 = %d." % _C20),
]

_CAT_LOAD_IN = ["500000"] + [str(x) for x in range(1, 500001)]
A1_TESTS.append(contest_test(
    "load: all n 1..500000",
    T(*_CAT_LOAD_IN),
    T(*[str(x) for x in _CAT_ANS]),
    "Precompute factorials ONCE; each Catalan is two binomials = O(1). The O(n^2) recurrence W is hopeless."))

A2_TESTS = [
    contest_test("textbook", T("1", "1000 3 2 3 5"), T("734"),
        "1000/2 + 1000/3 + 1000/5 - 1000/6 - 1000/10 - 1000/15 + 1000/30 = 734."),
    contest_test(
        "mixed",
        T(str(len(_A2_QUERIES) - 1) + "", *["%s %s" % (n, d) for (n, d) in _A2_QUERIES[1:]]),
        T(*_A2_ANS[1:]),
        "Pairs, triples, and quadruples of divisors; N up to 1e12 needs 64-bit only — the count fits."),
]

A3_TESTS = [
    contest_test("3x3 with hole", T("1", "3 3", "1 1"), T(str(paths(3, 3, (1, 1)))),
        "C(6,3)=20 total; 12 paths pass through (1,1); 20-12=8."),
    contest_test(
        "mixed",
        T(*([str(len(_A3_QUERIES) - 1)]
            + [x for (nm, b) in _A3_QUERIES[1:] for x in (nm, b)])),
        T(*_A3_ANS[1:]),
        "Bad cell inside or outside the grid; n+m up to 2e6 needs the bigger factorial table."),
]

CP_TESTS = [
    contest_test("brackets n=3", T("3", "3", "1", "19"),
        T(_CP_ANS[0], _CP_ANS[1], _CP_ANS[2]),
        "Balanced sequences of n pairs = Catalan C_n; C_19 = 1767263190 -> 767263183 mod p."),
    contest_test(
        "load: two n near 5e5",
        T("2", "500000", "499999"),
        T(_CP_ANS[3], _CP_ANS[4]),
        "C(1e6, 5e5) - C(1e6, 5e5+1): one table, two lookups. The central-binomial W reports the wrong sequence."),
]

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Combinatorics",
    "Catalan counts, inclusion-exclusion, and constrained lattice paths — counting structures with closed forms mod 1e9+7.",
    "Tổ hợp",
    "Số Catalan, bao hàm - loại trừ, và đường đi trên lưới có ô cấm — đếm cấu trúc bằng công thức đóng mod 1e9+7.",
    ["hsga-m14-catalan", "hsga-m14-ie", "hsga-m14-paths"],
    ["hsga-p14-combi"],
)

write_lesson(
    M, "hsga-m14-catalan",
    "Catalan Numbers",
    "When counting structures whose every prefix is 'balanced', the answer is a Catalan number — C(2n,n) - C(2n,n+1).",
    30,
    """
# Counting balanced structures

Balanced brackets, binary trees, triangulations, non-crossing pairings:
one sequence, C_n = C(2n,n) - C(2n,n+1). The subtraction removes the
structures whose running balance dips negative — a bijection to
unrestricted paths ending one step off. Precompute factorials once;
each query is O(1).
""", "Số Catalan",
    "Khi đếm cấu trúc mà mọi tiền tố đều 'cân bằng', đáp án là số Catalan — C(2n,n) - C(2n,n+1).",

    """
# Đếm cấu trúc cân bằng

Ngoặc cân bằng, cây nhị phân, tam giác hóa, ghép cặp không giao nhau:
một dãy duy nhất, C_n = C(2n,n) - C(2n,n+1). Phép trừ loại bỏ các cấu
trúc có số dư chạy qua âm — song ánh tới đường đi tự do kết thúc lệch
một bước. Tính trước bảng giai thừa một lần; mỗi truy vấn là O(1).
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m14-ie",
    "Inclusion-Exclusion",
    "Counting the union starts with the sum of singles, then subtracts pairs, adds triples: the LCM ladder with alternating signs.",
    30,
    """
# Union counts without double counting

|A∪B∪C| = |A|+|B|+|C| - |A∩B|-|A∩C|-|B∩C| + |A∩B∩C|. For divisibility,
intersections are LCMs. k up to 15-20 means bitmask enumeration of the
2^k subsets; signs alternate with subset size. Overflow discipline:
LCMs explode — cap at N and bail.
""", "Bao hàm - loại trừ",
    "Đếm hợp bắt đầu bằng tổng phần tử lẻ, trừ cặp, cộng bộ ba: thang LCM với dấu xen kẽ.",

    """
# Đếm hợp không đếm trùng

|A∪B∪C| = |A|+|B|+|C| - |A∩B|-|A∩C|-|B∩C| + |A∩B∩C|. Với tính chia hết,
giao là BCNN. k tới 15-20 nghĩa là duyệt 2^k tập con bằng bitmask; dấu
đổi theo kích thước tập con. Kỷ luật tràn số: BCNN nổ rất nhanh — chặn
tại N và dừng.
""", difficulty="advanced",
)

write_lesson(
    M, "hsga-m14-paths",
    "Constrained Lattice Paths",
    "Total paths minus paths through the obstacle: a two-binomial product that the reflection identity makes O(1).",
    30,
    """
# Subtracting the bad routes

Paths on an n×m grid from corner to corner: C(n+m, n). With ONE forbidden
cell: total - paths((0,0)→cell) × paths(cell→goal). Each factor is a
single binomial. Multiple obstacles need inclusion-exclusion over
subsets — the previous lesson generalizes.
""", "Đường đi trên lưới có ràng buộc",
    "Tổng đường đi trừ các đường qua ô cấm: tích hai nhị thức mà đồng nhất thức phản xạ cho O(1).",

    """
# Trừ các đường xấu

Đường đi trên lưới n×m từ góc tới góc: C(n+m, n). Với MỘT ô cấm:
tổng - đường((0,0)→ô) × đường(ô→đích). Mỗi thừa số là một nhị thức.
Nhiều ô cấm cần bao hàm - loại trừ trên các tập con — bài học trước
khái quát đúng chỗ này.
""", difficulty="advanced",
)

write_practice(
    M, "hsga-p14-combi", "Counting Suite",
    "Catalans at n = 5e5, four-divisor inclusion-exclusion at N = 1e12, and lattice paths around a forbidden cell.",
    "Bộ đếm tổ hợp",
    "Số Catalan tại n = 5e5, bao hàm - loại trừ bốn ước số tại N = 1e12, và đường đi lưới né ô cấm.",
    "hsga-m14-paths",
    110,
    "advanced",
    [
        challenge("hsga-p14-catalan", "Balanced Sequences",
            """**Problem.** Line 1: q. Each line: n. Print the number of
balanced sequences of n pairs of brackets mod 1e9+7.

**Constraints:** 1 ≤ q ≤ 500000; 1 ≤ n ≤ 500000.

Factorial precompute + the Catalan identity; the O(n^2) recurrence W cannot finish.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p14-iec", "Divisible Union",
            """**Problem.** Line 1: q. Each line: N k then k divisors d_i.
Print how many of 1..N are divisible by AT LEAST one d_i.

**Constraints:** 1 ≤ q ≤ 2000; 1 ≤ N ≤ 10^12; 1 ≤ k ≤ 4; 2 ≤ d_i ≤ 40.

Bitmask inclusion-exclusion with LCM capping.
""",
            A2_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p14-paths", "Grid Paths Around the Wall",
            """**Problem.** Line 1: q. Each line: n m then bx by (the forbidden
cell). Print paths from (0,0) to (n,m) moving only +x/+y, avoiding the
forbidden cell, mod 1e9+7.

**Constraints:** 1 ≤ q ≤ 200000; 0 ≤ n, m ≤ 10^6; cell may lie outside.

Two binomials per query; the unreduced-subtraction W overflows.
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    {
        "hsga-p14-combi": vi_challenge(
            "Bộ đếm tổ hợp",
            """**Bài toán.** Ba bài: số Catalan với n tới 5e5, đếm hợp các bội
với tới 4 ước số và N tới 1e12, và đường đi lưới né một ô cấm.""",
            [("Catalan", "C(2n,n) - C(2n,n+1) từ bảng giai thừa."),
             ("IE bitmask", "2^k tập con; giao là BCNN; chặn khi BCNN > N."),
             ("ô cấm", "C(n+m,n) trừ tích hai nhị thức qua ô.")],
        ),
    },
    solutions=[
        ("hsga-p14-catalan", A1_R, A1_W),
        ("hsga-p14-iec", A2_R, A2_W),
        ("hsga-p14-paths", A3_R, A3_W),
    ],
)

write_checkpoint(
    M, "hsga-cp-m14",
    "Checkpoint — Catalan Counts",
    "Bracket counts graded from n = 1 to n = 500000; a wrong answer that reports the central binomial instead of Catalan is the graded failure.",
    40,
    """
**Checkpoint — Catalan.** Line 1: q. Each line: n. Print the number of
balanced sequences of n bracket pairs mod 1e9+7.

C_n = C(2n, n) - C(2n, n + 1) with factorial tables.
""",
    "Điểm kiểm tra — Số Catalan",
    "Đếm ngoặc cân bằng chấm từ n = 1 tới n = 500000; đáp án nhầm nhị thức trung tâm thay vì Catalan là lỗi bị chấm.",
    """
**Checkpoint — Catalan.** Dòng 1: q. Mỗi dòng: n. In số dãy ngoặc cân
bằng của n cặp mod 1e9+7.

C_n = C(2n, n) - C(2n, n + 1) với bảng giai thừa.
""",
    challenge(
        "hsga-cp-m14-catalan",
        "Bracket Counts",
        """**Problem.** Line 1: q. Each line: n. Print the number of balanced
sequences of n bracket pairs mod 1e9+7.

**Constraints:** 1 ≤ q ≤ 100; 1 ≤ n ≤ 500000.

The W reports C(2n, n) — plausible, wrong for every n > 1.
""",
        CP_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Đếm dãy ngoặc",
        """**Bài toán.** Dòng 1: q. Mỗi dòng: n. In số dãy ngoặc cân bằng của
n cặp mod 1e9+7.""",
        [("Catalan", "C_n = C(2n, n) - C(2n, n + 1)."),
         ("bảng giai thừa", "Tính trước tới 2n lớn nhất; mỗi truy vấn O(1)."),
         ("bẫy", "C(2n, n) là nhị thức trung tâm, KHÔNG phải Catalan.")],
    ),
    solution=CP_M14_R,
    wrong=CP_M14_W,
)

print("module m14 complete")
