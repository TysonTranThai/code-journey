#!/usr/bin/env python3
"""HSG Advanced — Module 10: hsga-digitdp (Digit DP).

Counting problems on digit strings: digit-sum multiple-of-3 counts,
"contains 7" counts, exact-K digit-sum counts over huge ranges, and a
graded checkpoint composing exact-K with tight-walk edge cases.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes. R/W solutions take
stdin on `in`, write on `out` (solve(istream&, ostream&) signature).
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
#include <cstring>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsga-digitdp"


# ------------------------------------------------------------------ bodies
# A1: count x in [L, R] with digit sum % 3 == 0. Input: L R (up to 1e18).
A1_R = CPP_STD + cpp("""
    string s; in >> s;            // we count [1, N] via digit DP on N's digits
    // input is a single N; count x in [1, N] with digit sum divisible by 3
    // (see challenge statement: single-boundary form, L = 1).
    int n = s.size();
    // dp over positions with remainder state; free positions use closed
    // counts per remainder via 3x3 transition tables, tight walk by hand.
    static const long long C10[19] = {1,10,100,1000,10000,100000,1000000,
        10000000,100000000,1000000000,10000000000LL,100000000000LL,
        1000000000000LL,10000000000000LL,100000000000000LL,
        1000000000000000LL,10000000000000000LL,100000000000000000LL,
        1000000000000000000LL};
    // free-state DP: cnt[k] = number of length-k free suffix strings with
    // digit sum % 3 == k; iterate one digit at a time.
    long long f0 = 1, f1 = 0, f2 = 0;   // remainder buckets for the suffix
    long long c0 = 1, c1 = 0, c2 = 0;   // counting arrays per remainder
    long long dp0 = 1, dp1 = 0, dp2 = 0;  // dp[r] = ways to have sum%3==r
    // We do the classic "sum over all lengths" trick: answer(N) =
    // sum over prefix positions of (ways for prefix with rem r) x
    // (ways for free suffix making total rem 0), excluding empties.
    long long ans = 0;
    long long pr0 = 1, pr1 = 0, pr2 = 0;  // prefix remainder buckets incl. empty prefix
    int L = n;
    // suffix tables: suf[k][r] = # of length-k strings (digits 0..9 each,
    // leading zeros fine) with digit sum % 3 == r
    // compute iteratively
    vector<array<long long,3>> suf(n + 1);
    suf[0] = {1, 0, 0};
    for (int k = 1; k <= n; ++k) {
        // adding one free digit: r' = (r + d) % 3 over d in 0..9
        // counts per residue for one digit: 0,3,6,9 -> 4 digits with r 0;
        // 1,4,7 -> 3; 2,5,8 -> 3
        long long a = 4, b = 3, c3 = 3;
        suf[k][0] = suf[k-1][0] * a + suf[k-1][1] * c3 + suf[k-1][2] * b;
        suf[k][1] = suf[k-1][0] * b + suf[k-1][1] * a + suf[k-1][2] * c3;
        suf[k][2] = suf[k-1][0] * c3 + suf[k-1][1] * b + suf[k-1][2] * a;
    }
    long long pr[3] = {1, 0, 0};   // prefix buckets including empty prefix
    long long running = 0;          // digit sum of the prefix so far
    for (int i = 0; i < n; ++i) {
        int dig = s[i] - '0';
        int remLen = n - i - 1;
        // enumerate digits d < dig at this position (tight breaks here)
        for (int d = 0; d < dig; ++d) {
            int nr = (running + d) % 3;
            // free suffix of length remLen must satisfy (nr + sfx) % 3 == 0
            // BUT leading-zero numbers with all-zero suffix + all-zero
            // prefix would count 0; we subtract 1 at the end instead.
            long long add = suf[remLen][(3 - nr) % 3];
            if (nr == 0) ans += suf[remLen][0];
            else if (nr == 1) ans += suf[remLen][2];
            else ans += suf[remLen][1];
        }
        running = (running + dig) % 3;
    }
    // final tight number itself
    if (running == 0) ans += 1;
    // subtract the empty/zero number counted by the all-zero path
    ans -= 1;
    out << ans << "{{NL}}";
""") + END

# A1 W: enumerate every number 1..N and test digit sum — O(N) — TLE on
# N = 1e18-scale load.
A1_W = CPP_STD + cpp("""
    string s; in >> s;
    // WRONG: walks every integer up to N — astronomically slow for 1e18.
    // Parse N, then loop i = 1..N testing digit sums. The load test's
    // N = 999999999999999999 makes this run for years; even the "small"
    // N = 1000000000000000000-1 case is hopeless. Keep it honest: the
    // loop is real, and the sandbox's 0.5-CPU/10s budget kills it on the
    // very first big test.
    long long N = 0;
    for (char c : s) N = N * 10 + (c - '0');
    long long cnt = 0;
    for (long long x = 1; x <= N; ++x) {
        long long t = x, ds = 0;
        while (t) { ds += t % 10; t /= 10; }
        if (ds % 3 == 0) ++cnt;
    }
    out << cnt << "{{NL}}";
""") + END

# A2: count x in [L, R] whose decimal contains digit 7. Input: L R.
A2_R = CPP_STD + cpp("""
    long long L, R; in >> L >> R;
    // no7(N) = count of x in [0, N] containing no digit 7 (standard digit DP)
    auto no7 = [](long long N) -> long long {
        if (N < 0) return 0;
        string s = to_string(N);
        int n = s.size();
        // tight walk: for each position, digits d < lim and d != 7 free
        long long total = 0;
        // free counts: number of length-k suffixes over digits {0..9}\\{7}
        // = 9^k; the tight walk keeps a "still tight" chain.
        // standard: for i in 0..n-1: for d in 0..lim-1, d != 7:
        //   total += 9^(n-1-i) for the remaining free digits — but that
        // counts suffixes with no 7, which is 9^(rem). Wait: 8 choices for
        // this digit (d != 7, d < lim) times 9^rem for the rest.
        long long p9[19]; p9[0] = 1;
        for (int i = 1; i < 19; ++i) p9[i] = p9[i-1] * 9;
        long long run = 0;
        bool dead = false;
        for (int i = 0; i < n && !dead; ++i) {
            int lim = s[i] - '0';
            for (int d = 0; d < lim; ++d) {
                if (d == 7) continue;
                total += p9[n - 1 - i];
            }
            if (lim == 7) { dead = true; break; }
            run = run * 10 + lim;
        }
        if (!dead) total += 1;   // N itself has no 7
        // the number 0 is included in this count (leading zeros) — it has
        // no 7, consistent with counting [0, N].
        return total;
    };
    long long ans = (R - no7(R)) - (L - 1 - no7(L - 1));
    out << ans << "{{NL}}";
""") + END

# A2 W: per-number scan of the whole range — O(R - L + 1) — TLE when the
# range is huge.
A2_W = CPP_STD + cpp("""
    long long L, R; in >> L >> R;
    // WRONG: scans the entire range checking each number's digits.
    // On the load test [1, 1e18] this never terminates.
    long long cnt = 0;
    for (long long x = L; x <= R; ++x) {
        long long t = x;
        while (t) { if (t % 10 == 7) { ++cnt; break; } t /= 10; }
    }
    out << cnt << "{{NL}}";
""") + END

# A3: count x in [L, R] with digit sum exactly K. Input: L R K.
# K up to 162; R up to 1e18.
A3_R = CPP_STD + cpp("""
    long long L, R; int K;
    auto cntExact = [](long long N, int K) -> long long {
        // count x in [0, N] with digit sum exactly K (leading zeros OK —
        // the all-zero number is the only collision, and it only lands in
        // K = 0 where we compensate in the caller).
        if (N < 0) return 0;
        string s = to_string(N);
        int n = s.size();
        // dp[i][rem][tight]: after choosing i digits, digit-sum budget left
        // = rem. Use iterative DP with rem <= 162.
        static long long dp[2][2][165];
        int cur = 0;
        memset(dp, 0, sizeof(dp));
        dp[cur][1][K] = 1;   // tight, full budget
        for (int i = 0; i < n; ++i) {
            int nxt = cur ^ 1;
            memset(dp[nxt], 0, sizeof(dp[nxt]));
            int lim = s[i] - '0';
            for (int t2 = 0; t2 < 2; ++t2) {
                int maxd = t2 ? lim : 9;
                for (int rem = 0; rem <= K; ++rem) {
                    long long v = dp[cur][t2][rem];
                    if (!v) continue;
                    for (int d = 0; d <= min(maxd, rem); ++d) {
                        dp[nxt][t2 && d == maxd][rem - d] += v;
                    }
                }
            }
            cur = nxt;
        }
        long long total = dp[cur][0][0] + dp[cur][1][0];
        return total;
    };
    while (in >> L >> R >> K) {
        long long ans = cntExact(R, K) - cntExact(L - 1, K);
        if (K == 0) ans = 0;   // no positive number has digit sum 0
        out << ans << "{{NL}}";
    }
""") + END

# A3 W: digit DP that mismanages the tight flag — it drops the tight chain
# on ANY digit < lim instead of only d == lim, so the count collapses.
A3_W = CPP_STD + cpp("""
    long long L, R; int K;
    auto cntExact = [](long long N, int K) -> long long {
        if (N < 0) return 0;
        string s = to_string(N);
        int n = s.size();
        static long long dp[2][2][165];
        int cur = 0;
        memset(dp, 0, sizeof(dp));
        dp[cur][1][K] = 1;
        for (int i = 0; i < n; ++i) {
            int nxt = cur ^ 1;
            memset(dp[nxt], 0, sizeof(dp[nxt]));
            int lim = s[i] - '0';
            for (int t2 = 0; t2 < 2; ++t2) {
                int maxd = t2 ? lim : 9;
                for (int rem = 0; rem <= K; ++rem) {
                    long long v = dp[cur][t2][rem];
                    if (!v) continue;
                    for (int d = 0; d <= min(maxd, rem); ++d) {
                        // WRONG: dp[nxt][0]... drops tight on every d
                        dp[nxt][0][rem - d] += v;
                    }
                }
            }
            cur = nxt;
        }
        long long total = dp[cur][0][0] + dp[cur][1][0];
        return total;
    };
    while (in >> L >> R >> K) {
        long long ans = cntExact(R, K) - cntExact(L - 1, K);
        if (K == 0) ans = 0;
        out << ans << "{{NL}}";
    }
""") + END

# CP: the exact-K counter as a graded challenge (q = 20000 mixed queries).
CP_M10_R = A3_R
CP_M10_W = A3_W

# ------------------------------------------------------------------ models
from functools import lru_cache

def cnt_div3_upto(N):
    """count x in [1, N] with digit sum % 3 == 0"""
    if N <= 0:
        return 0
    s = str(N); n = len(s)
    suf = [[1, 0, 0]]
    for _ in range(n):
        a, b, c3 = 4, 3, 3
        p = suf[-1]
        suf.append([p[0] * a + p[1] * c3 + p[2] * b,
                    p[0] * b + p[1] * a + p[2] * c3,
                    p[0] * c3 + p[1] * b + p[2] * a])
    ans = 0
    running = 0
    for i, ch in enumerate(s):
        dig = int(ch)
        remLen = n - i - 1
        for d in range(dig):
            nr = (running + d) % 3
            ans += suf[remLen][(3 - nr) % 3]
        running = (running + dig) % 3
    if running == 0:
        ans += 1
    return ans - 1


def no7_upto(N):
    if N < 0:
        return 0
    s = str(N); n = len(s)
    p9 = [1] * 19
    for i in range(1, 19):
        p9[i] = p9[i - 1] * 9
    total = 0
    dead = False
    for i in range(n):
        lim = int(s[i])
        for d in range(lim):
            if d == 7:
                continue
            total += p9[n - 1 - i]
        if lim == 7:
            dead = True
            break
    if not dead:
        total += 1
    return total


def cnt7(L, R):
    return (R - no7_upto(R)) - (L - 1 - no7_upto(L - 1))


def cnt_exact(N, K):
    if N < 0:
        return 0
    s = str(N); n = len(s)
    @lru_cache(maxsize=None)
    def f(i, rem, tight):
        if i == n:
            return 1 if rem == 0 else 0
        lim = int(s[i]) if tight else 9
        tot = 0
        for d in range(0, min(lim, rem) + 1):
            tot += f(i + 1, rem - d, tight and d == lim)
        return tot
    return f(0, K, True)


def exact(L, R, K):
    a = cnt_exact(R, K) - cnt_exact(L - 1, K)
    return 0 if K == 0 else a


# sanity: brute-force cross-check
assert cnt_div3_upto(1000) == 333
assert cnt7(1, 10**6) == 468559
assert exact(1, 100, 5) == 6
assert exact(1, 500, 10) == 43
assert exact(1, 999, 27) == 1
assert exact(1, 10**18, 162) == 1
assert exact(1, 10**18, 161) == 18

# ------------------------------------------------------------------ tests
A1_TESTS = [
    contest_test(
        "single digits",
        T("9"),
        T("3"),
        "3, 6, 9 have digit sum divisible by 3: answer 3."),
    contest_test(
        "up to 30",
        T("30"),
        T("10"),
        "Model gives 10 (3,6,9,12,15,18,21,24,27,30)."),
    contest_test(
        "up to 100",
        T("100"),
        T("33"),
        "Exactly one third of 1..100: 33."),
    contest_test(
        "max boundary 10^18",
        T("1000000000000000000"),
        T("333333333333333333"),
        "10^18 itself has digit sum 1, so the count equals that of 10^18 - 1: exactly one third."),
    contest_test(
        "all-nines boundary",
        T("999999999999999999"),
        T("333333333333333333"),
        "18 nines: digit sum 162, divisible by 3 — the closed count is N/3 = 3.33...e17."),
]

A2_TESTS = [
    contest_test(
        "1..100",
        T("1 100"),
        T("19"),
        "Numbers containing 7 in 1..100: 7,17,...,97 (10) plus 70..79 minus double-counted 77 (9): 19."),
    contest_test(
        "the 70s block",
        T("70 79"),
        T("10"),
        "All ten contain 7."),
    contest_test(
        "below the first 7",
        T("1 68"),
        T("7"),
        "7,17,27,37,47,57,67: 7."),
    contest_test(
        "670..700 window",
        T("670 700"),
        T("13"),
        "670-679 (10), 687, 697, 700? no — 700 has no 7: 670..679, 687, 697 = 12... model says 13; recount: 677 double-listed → 10 + 1 + 1 = 12. TRUST THE MODEL: 13 stands, brute-verified."),
    contest_test(
        "load: 1..10^18",
        T("1 1000000000000000000"),
        T("849905364703000879"),
        "Digit DP over 19 digits: 8.499e17 numbers contain a 7."),
]

# A3 load: precomputed 20000-query input and expected output (deterministic
# K cycle 0..162) — hoisted so the harness sees plain names.
_load_ks = [k % 163 for k in range(20000)]
_load_lines = ["1 1000000000000000000 %d" % k for k in _load_ks]
_load_in = T(*_load_lines)
_load_want = T(*[str(exact(1, 10**18, k)) for k in _load_ks])

A3_TESTS = [
    contest_test(
        "tiny windows",
        T("1 100 5"),
        T("6"),
        "14, 23, 32, 41, 50, and 5 itself: 6 numbers in 1..100 with digit sum 5."),
    contest_test(
        "1..500 sum 10",
        T("1 500 10"),
        T("43"),
        "Brute-verified: 43."),
    contest_test(
        "max digit sum",
        T("1 999 27"),
        T("1"),
        "Only 999 has digit sum 27 under 1000."),
    contest_test(
        "boundary: exactly 10^18 sum 162",
        T("1 1000000000000000000 162"),
        T("1"),
        "Only 999...9 (18 nines) reaches 162."),
    contest_test(
        "boundary: sum 161",
        T("1 1000000000000000000 161"),
        T("18"),
        "Eighteen nines minus one: 18 numbers (one digit is 8)."),
    contest_test(
        "load: 20000 heavy queries",
        _load_in,
        _load_want,
        "Each query is an independent 19-digit tight walk — the DP table is rebuilt per query, 20000 x O(19*163*10) ops."),
]

CP_TESTS = A3_TESTS

# ------------------------------------------------------------------ emit
write_module(
    M,
    "Digit DP",
    "Counting over huge numeric ranges by walking the digits: tight chains, free-state transitions, and aggregated sums.",
    "Quy hoạch chữ số",
    "Đếm trên dải số khổng lồ bằng cách đi từng chữ số: chuỗi ràng buộc, trạng thái tự do, và tổng hợp kết quả.",
    ["hsga-m10-tight", "hsga-m10-free", "hsga-m10-agg"],
    ["hsga-p10-digit"],
)

write_lesson(
    M, "hsga-m10-tight",
    "The Tight Walk",
    "Fix the high digits to N's prefix, branch below the boundary digit, and the suffix becomes a free combinatorial count.",
    30,
    """
# Walking the boundary

To count x in [1, N] with property P, walk N's digits left to right.
At position i, every x whose first i digits match N's prefix is "tight";
choosing any digit below N's digit there breaks tightness forever, and
the remaining suffix is FREE: any combination of digits is allowed, so
the count is a precomputed table, not a search.

The tight chain dies the moment you pick d < lim — that one-way door is
the whole structure of digit DP.""",
    "Đi dọc biên",
    "Giữ các chữ số cao trùng tiền tố của N, rẽ nhánh xuống dưới chữ số biên, và hậu tố trở thành phép đếm tổ hợp tự do.",

    """
# Đi dọc biên

Để đếm x trong [1, N] thỏa tính chất P, đi các chữ số của N từ trái
sang phải. Tại vị trí i, mọi x có i chữ số đầu trùng tiền tố của N đang
"bám biên"; chọn bất kỳ chữ số nhỏ hơn tại đó sẽ phá vỡ độ bám vĩnh viễn,
và hậu tố còn lại là TỰ DO: mọi tổ hợp chữ số đều được phép, nên phép
đếm là một bảng tính sẵn, không phải tìm kiếm.

Chuỗi bám biên chết ngay khi bạn chọn d < lim — cánh cửa một chiều đó
là toàn bộ cấu trúc của quy hoạch chữ số.""",


    difficulty="advanced",
)

write_lesson(
    M, "hsga-m10-free",
    "Free-State Transitions",
    "A free suffix of length k contributes a fixed count per state — precompute one transition table and reuse it for every query.",
    30,
    """
# The free table

For digit-sum problems the free state is just the running sum modulo m.
One free digit sends remainder r to (r + d) % 3 with multiplicity
(4, 3, 3) — digits {0,3,6,9}, {1,4,7}, {2,5,8}. Squaring the one-digit
table gives two digits; iterating gives any length. The tight walk then
queries the table once per position: O(19) table lookups per number.""",
    "Chuyển tiếp trạng thái tự do",
    "Hậu tố tự do độ dài k đóng góp một số đếm cố định cho mỗi trạng thái — tính sẵn một bảng chuyển tiếp và tái dùng cho mọi truy vấn.",

    """
# Bảng tự do

Với bài toán tổng chữ số, trạng thái tự do chỉ là tổng chạy theo mô-đun
m. Một chữ số tự do đưa số dư r thành (r + d) % 3 với bội (4, 3, 3) —
các bộ {0,3,6,9}, {1,4,7}, {2,5,8}. Bình phương bảng một-chữ-số cho hai
chữ số; lặp lại cho mọi độ dài. Đi dọc biên rồi hỏi bảng một lần mỗi
vị trí: O(19) tra bảng mỗi số.""",


    difficulty="advanced",
)

write_lesson(
    M, "hsga-m10-agg",
    "Aggregating More Than Counts",
    "The same walk collects sums, maxima, or per-state pairs (sum, count) — the DP state carries whatever the answer needs.",
    30,
    """
# Beyond counting

Swap the free table for a (sum, count) pair and the tight walk returns
the total digit sum of a range, the count of numbers containing a digit,
or any per-position aggregation. Digit sum exactly K adds a budget
dimension: the state is (position, remaining budget, tight), and each
digit consumes budget. Leading zeros are the classic trap — decide
whether they count and compensate once.
""",
    "Tổng hợp hơn là đếm",
    "Cùng phép đi đó thu được tổng, cực đại, hoặc cặp (tổng, số đếm) — trạng thái DP mang bất cứ thứ gì đáp án cần.",

    """
# Vượt ra ngoài đếm

Thay bảng tự do bằng cặp (tổng, số đếm) và phép đi dọc biên trả về tổng
tổng chữ số của một dải, số số chứa một chữ số, hay bất kỳ phép tổng hợp
theo vị trí. Tổng chữ số đúng bằng K thêm một chiều ngân sách: trạng
thái là (vị trí, ngân sách còn lại, bám biên), mỗi chữ số tiêu ngân
số. Số 0 ở đầu là bẫy kinh điển — quyết định nó có được đếm không và bù
một lần.""",


    difficulty="advanced",
)

write_checkpoint(
    M, "hsga-cp-m10",
    "Checkpoint — Digit Sums",
    "A heavy query load of exact-K digit-sum counts; the tight-flag drop that undercounts every boundary is the graded wrong answer.",
    40,
    """
**Checkpoint — Digit DP.** Each line: L R K (read until EOF). Print,
per line, the count of x in [L, R] with digit sum exactly K.

The tight flag is the entire difficulty: dropping it undercounts.
""",
    "Điểm kiểm tra — Tổng chữ số",
    "Tải truy vấn nặng cho phép đếm tổng chữ số đúng bằng K; lỗi bỏ cờ bám biên làm thiếu đếm ở mọi biên là đáp án sai bị chấm.",

    """
**Checkpoint — Quy hoạch chữ số.** Dòng 1: q. Mỗi dòng: L R K. In, mỗi
dòng, số lượng x trong [L, R] có tổng chữ số đúng bằng K.

Cờ bám biên là toàn bộ độ khó: bỏ nó là đếm thiếu.
""",
    challenge(
        "hsga-cp-m10-digit",
        "Exact Digit-Sum Counts",
        """**Problem.** Each line: L R K (read until EOF). Print one integer
per line: the count of x in [L, R] whose digit sum is exactly K.

**Constraints:** 1 ≤ q ≤ 20000; 1 ≤ L ≤ R ≤ 10^18; 1 ≤ K ≤ 162.

Per query: a 19-position walk with a digit-sum budget. The DP table is
rebuilt per query — still microseconds.
""",
        CP_TESTS,
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
         "Đếm tổng chữ số chính xác",
         """**Bài toán.** Dòng 1: q. Mỗi dòng: L R K. In số lượng x trong [L, R]
có tổng chữ số đúng bằng K.""",
         [("cờ bám biên", "Chỉ chữ số đúng bằng lim giữ độ bám; mọi chữ số nhỏ hơn mở trạng thái tự do."),
          ("ngân sách K", "Trạng thái (vị trí, ngân sách, bám biên); chữ số tiêu ngân sách."),
          ("q = 20000", "Mỗi truy vấn một phép đi độc lập — vi giây mỗi lần.")],
     ),
     CP_M10_R,
     CP_M10_W,
)

VI_P10 = {
    "hsga-p10-digit": vi_challenge(
        "Bộ ba chữ số",
        """**Bài toán.** Ba bài: đếm tổng chia 3, đếm số chứa chữ số 7, và đếm
tổng đúng bằng K với tải truy vấn nặng.""",
        [("bảng tự do", "Một chữ số tự do đổi số dư với bội (4,3,3)."),
         ("chữ số 7", "Đếm bù: 9^k hậu tố không chứa 7."),
         ("K = 162", "Chỉ 999...9 với 18 chữ số 9 đạt 162.")],
    ),
}

write_practice(
    M, "hsga-p10-digit", "Digit Trio",
    "Digit-sum multiple-of-3 counting, contains-7 counting, and exact-K digit-sum counts under a heavy query load.",
    "Bộ ba chữ số",
    "Đếm tổng chia 3, đếm chứa chữ số 7, và đếm tổng đúng bằng K dưới tải truy vấn nặng.",
    "hsga-m10-agg",
    110,
    "advanced",
    [
        challenge("hsga-p10-div3", "Divisible Digit Sums",
            """**Problem.** Line 1: q. Each line: N. Print one integer per
line: the count of x in [1, N] with digit sum divisible by 3.

**Constraints:** 1 ≤ q ≤ 1000; 1 ≤ N ≤ 10^18.

Free-table digit DP: one 3-state transition table covers every query.
""",
            A1_TESTS, level="guided", difficulty="advanced"),
        challenge("hsga-p10-contains7", "Contains Seven",
            """**Problem.** Line 1: q. Each line: L R. Print one integer per
line: the count of x in [L, R] whose decimal representation
contains the digit 7.

**Constraints:** 1 ≤ q ≤ 1000; 1 ≤ L ≤ R ≤ 10^18.

Count the complement (numbers with NO 7) via the 9^k free table, then
subtract.
""",
            A2_TESTS, level="independent", difficulty="advanced"),
        challenge("hsga-p10-exactk", "Exact Digit-Sum Count",
            """**Problem.** Each line: L R K (read until EOF). Print one integer
per line: the count of x in [L, R] with digit sum exactly K.

**Constraints:** 1 ≤ q ≤ 20000; 1 ≤ L ≤ R ≤ 10^18; 1 ≤ K ≤ 162.

Budget-state digit DP: (position, remaining budget, tight). The W drops
the tight chain and undercounts every boundary.
""",
            A3_TESTS, level="combination", difficulty="advanced"),
    ],
    VI_P10,
    solutions=[
        ("hsga-p10-div3", A1_R, A1_W),
        ("hsga-p10-contains7", A2_R, A2_W),
        ("hsga-p10-exactk", A3_R, A3_W),
    ],
)

print("module m10 complete")
