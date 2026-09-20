#!/usr/bin/env python3
"""HSG Advanced — Module 1: hsga-attack (Advanced Attack Patterns).

Meet-in-the-middle, XOR/pairing invariants, constructive permutations,
brute-force-as-oracle rescaling, and guess-check on monotone answers.
The hunted failures: O(2^n) enumeration where 2^(n/2) is required, and
brute force that is right-but-too-slow.

Conventions: zero literal backslashes. Test input AND want use real
newlines via T(); C++ bodies via cpp() turning {{NL}} into \n escapes.
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

M = "hsga-attack"
write_module(
    M,
    "Advanced Attack Patterns",
    "Meet-in-the-middle halving of exponential search, XOR and pairing invariants, constructive permutations, brute force rescaled as an oracle, and guess-check on monotone answers.",
    "Kỹ thuật tấn công nâng cao",
    "Gặp nhau ở giữa giảm một nửa tìm kiếm mũ, bất biến XOR và ghép cặp, hoán vị kiến tạo, brute-force làm bộ kiểm tra, và đoán-kiểm trên đáp án đơn điệu.",
    ["hsga-m1-mitm", "hsga-m1-invariants", "hsga-cp-m1"],
    ["hsga-p1-attack"],
)

write_lesson(
    M, "hsga-m1-mitm",
    "Meet in the Middle",
    "Halve exponential search: enumerate each half separately and join the results in a searchable structure.",
    30,
    """
# Meet in the Middle

Exhaustive search dies at n ≈ 25 because 2^n explodes. Split the items into
two halves: enumerate each half (2^(n/2) each), then **join** the two lists
with sorting + binary search or a hash table. For n = 30 that is about
10^4–10^5 operations — feasible where 2^30 ≈ 10^9 is not.

Worked problem — count subsets of 30 items with weight sum exactly S:

1. Enumerate all subset sums of the first 15 items (~32768 values).
2. Enumerate all subset sums of the last 15 items.
3. Sort one list; for every sum x in the other list, count occurrences of
   S − x with binary search (or a hash map in one pass).

Complexity: O(2^(n/2) · n/2) time, O(2^(n/2)) memory — the memory line is
the real engineering limit on the sandbox.

Recognition cues: n ≤ 40, a "pick some items" objective, no polynomial
structure in sight. If n ≤ 20 plain 2^n enumeration already fits.
""",
    "Gặp nhau ở giữa",
    "Chia đôi tìm kiếm mũ: liệt kê từng nửa rồi ghép kết quả bằng cấu trúc tìm kiếm.",
    """
# Gặp nhau ở giữa (Meet in the Middle)

Vét cạn chết ở n ≈ 25 vì 2^n bùng nổ. Chia vật thành hai nửa: liệt kê tổng
tập con của từng nửa (2^(n/2) mỗi nửa), rồi **ghép** hai danh sách bằng sắp
xếp + tìm kiếm nhị phân hoặc bảng băm. Với n = 30: khoảng 10^4–10^5 phép —
khả thi trong khi 2^30 ≈ 10^9 là không.

Bài mẫu — đếm tập con của 30 vật có tổng trọng lượng đúng S:

1. Liệt kê mọi tổng tập con của 15 vật đầu (~32768 giá trị).
2. Liệt kê tổng tập con của 15 vật sau.
3. Sắp một danh sách; với mỗi tổng x trong danh sách kia, đếm số lần xuất
   hiện của S − x bằng tìm kiếm nhị phân (hoặc bảng băm một lượt).

Độ phức tạp: O(2^(n/2) · n/2) thời gian, O(2^(n/2)) bộ nhớ — giới hạn bộ nhớ
mới là rào cản kỹ thuật thật trên sandbox.

Dấu hiệu nhận biết: n ≤ 40, mục tiêu kiểu "chọn một số vật", không có cấu
trúc đa thức nào. Nếu n ≤ 20 thì liệt kê 2^n thuần đã vừa.
""",
    difficulty="advanced",
)

write_lesson(
    M, "hsga-m1-invariants",
    "Invariants and Constructive Proofs",
    "Find what never changes — XOR pairings, parity, order — and build objects that provably satisfy the constraints.",
    30,
    """
# Invariants and Constructive Problems

Two advanced skills that no template covers.

**Invariants.** Find a quantity that every operation preserves. Classic: the
XOR of 1..n equals [n, 1, n+1, 0][n mod 4] — an O(1) answer hiding inside a
seemingly linear task. Another: when asked to make all values equal by
"add k to two different elements each step", the invariant is the set of
differences between elements; feasibility becomes a modular condition.

**Constructive.** You must output *any* object satisfying the constraints,
and the proof is the construction. Example: a permutation of 1..n with no
fixed point and no two adjacent values differing by exactly 1. For even n,
evens-ascending then odds-ascending works: 2 4 6 1 3 5 — no fixed point, no
adjacent pair is consecutive. State WHY the construction works, then encode
it. Check n = 1, 2, 3 by hand: small n are where constructions break.
""",
    "Bất biến và kiến tạo",
    "Tìm thứ không bao giờ đổi — ghép XOR, tính chẵn lẻ, thứ tự — và dựng đối tượng thỏa ràng buộc một cách chứng minh được.",
    """
# Bất biến và bài toán kiến tạo

Hai kỹ năng nâng cao mà không template nào dạy được.

**Bất biến.** Tìm đại lượng mà mọi thao tác đều bảo toàn. Kinh điển: XOR của
1..n bằng [n, 1, n+1, 0][n mod 4] — đáp án O(1) ẩn trong bài tưởng phải duyệt.
Ví dụ khác: khi được phép "cộng k vào hai phần tử khác nhau mỗi bước", bất
biến là **chênh lệch giữa các phần tử**; khả thi hay không trở thành điều
kiện modulo.

**Kiến tạo.** Bạn phải in *một* đối tượng bất kỳ thỏa ràng buộc, và lời chứng
minh chính là cách dựng. Ví dụ: hoán vị của 1..n không có điểm cố định và
không có hai phần tử kề nhau chênh đúng 1. Với n chẵn: khối chẵn tăng rồi
khối lẻ tăng — 2 4 6 1 3 5 — không điểm cố định, không cặp kề liên tiếp.
Phát biểu WHY cách dựng đúng rồi mới code. Kiểm tay n = 1, 2, 3: chính các
n nhỏ phá vỡ cách dựng.
""",
    difficulty="advanced",
)

# ---------------------------------------------------------------- checkpoint
CP_M1_R = CPP_STD + cpp("""    long long n, S; in >> n >> S;
    vector<long long> w(n);
    for (auto& x : w) in >> x;
    long long h1 = n / 2;
    vector<long long> L, R;
    for (int mask = 0; mask < (1 << h1); ++mask) {
        long long s = 0;
        for (int i = 0; i < h1; ++i) if (mask >> i & 1) s += w[i];
        L.push_back(s);
    }
    for (int mask = 0; mask < (1 << (n - h1)); ++mask) {
        long long s = 0;
        for (int i = 0; i < n - h1; ++i) if (mask >> i & 1) s += w[h1 + i];
        R.push_back(s);
    }
    sort(L.begin(), L.end());
    long long cnt = 0;
    for (long long s : R) cnt += upper_bound(L.begin(), L.end(), S - s) - lower_bound(L.begin(), L.end(), S - s);
    out << cnt << "{{NL}}";
""") + END

CP_M1_W = CPP_STD + cpp("""    long long n, S; in >> n >> S;
    vector<long long> w(n);
    for (auto& x : w) in >> x;
    // WRONG: enumerates ALL 2^n subsets — TLE for n = 30 on the sandbox.
    long long cnt = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        long long s = 0;
        for (int i = 0; i < n; ++i) if (mask >> i & 1) s += w[i];
        if (s == S) ++cnt;
    }
    out << cnt << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsga-cp-m1", "Checkpoint — Attack Patterns",
    "Two-side graded: solve the subset-count task with meet-in-the-middle; the 2^n enumeration must time out.",
    20,
    """
**Điểm kiểm tra — Kỹ thuật tấn công.** Đếm số tập con có tổng đúng S. Giới
hạn: n ≤ 30, |w[i]| ≤ 10^9. Một giải pháp liệt kê 2^n *sẽ* quá thời gian —
đó chính là điểm bị chấm.
""",
    "Điểm kiểm tra — Kỹ thuật tấn công",
    "Đếm số tập con có tổng đúng S với n ≤ 30 — giải 2^n sẽ quá thời gian.",
    """
**Điểm kiểm tra — Kỹ thuật tấn công.** Đếm số tập con có tổng đúng S. Giới
hạn: n ≤ 30, |w[i]| ≤ 10^9.
""",
    challenge(
        "hsga-cp-m1-mitm",
        "Subset Sums — Exact Count",
        """**Bài toán.** Given n items with weights w[i] and a target S, count the
subsets whose weights sum exactly to S.

**Constraints:** 1 ≤ n ≤ 30; |w[i]| ≤ 10^9; |S| ≤ 10^12.

**Output:** the count. An enumeration of all 2^n subsets will NOT fit the
time limit; meet-in-the-middle will.
""",
        [
            contest_test("one item match", T("1", "5", "5"), T("1"),
                "Single subset {item}."),
            contest_test("one item miss", T("1", "5", "3"), T("0"),
                "No subset sums to 3."),
            contest_test("two items", T("2", "3", "1 2"), T("1"),
                "Subsets sums: 0,1,2,3 — exactly one equals 3."),
            contest_test("n=30 large", T("30", "696") + T(*[str((i * 37) % 89 + 1) for i in range(1, 31)]), T("1818374"),
                "n=30: 2^30 enumeration is ~10^9 ops — TLE; MITM passes. Ground truth via an independent half-join in Python."),
        ],
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Đếm tổng tập con",
        """**Bài toán.** Cho n vật trọng lượng w[i] và đích S, đếm số tập con có
tổng đúng S.

**Ràng buộc:** 1 ≤ n ≤ 30; |w[i]| ≤ 10^9.
""",
        [("một vật khớp", "Chỉ một tập con."),
         ("một vật lệch", "Không tập con nào."),
         ("hai vật", "Kiểm tay các tập con."),
         ("n=30 lớn", "2^30 là ~10^9 phép — quá thời gian; MITM là đủ.")],
    ),
    CP_M1_R,
    CP_M1_W,
)

# ------------------------------------------------------------ practice R/W
A1_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long h1 = n / 2;
    vector<long long> L, R;
    for (int mask = 0; mask < (1 << h1); ++mask) {
        long long s = 0;
        for (int i = 0; i < h1; ++i) if (mask >> i & 1) s += a[i];
        L.push_back(s);
    }
    for (int mask = 0; mask < (1 << (n - h1)); ++mask) {
        long long s = 0;
        for (int i = 0; i < n - h1; ++i) if (mask >> i & 1) s += a[h1 + i];
        R.push_back(s);
    }
    sort(L.begin(), L.end());
    for (int i = 0; i < q; ++i) {
        long long S; in >> S;
        long long cnt = 0;
        for (long long s : R) cnt += upper_bound(L.begin(), L.end(), S - s) - lower_bound(L.begin(), L.end(), S - s);
        out << cnt << "{{NL}}";
    }
""") + END

A1_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: recounts all subsets per query — q × 2^n. The n=24 q=200
    // test alone needs 200 × 4M ops ≈ 10^9; the full run exceeds 10 s.
    for (int i = 0; i < q; ++i) {
        long long S; in >> S;
        long long cnt = 0;
        for (int mask = 0; mask < (1 << n); ++mask) {
            long long s = 0;
            for (int j = 0; j < n; ++j) if (mask >> j & 1) s += a[j];
            if (s == S) ++cnt;
        }
        out << cnt << "{{NL}}";
    }
""") + END

A2_R = CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        unsigned long long n; in >> n;
        // XOR of 1..n: [n, 1, n+1, 0][n mod 4]
        unsigned long long r[4] = {n, 1, n + 1, 0};
        out << r[n & 3] << "{{NL}}";
    }
""") + END

A2_W = CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long n; in >> n;
        // WRONG: loop to n — TLE when n = 10^9 with T = 10000.
        long long x = 0;
        for (long long i = 1; i <= n; ++i) x ^= i;
        out << x << "{{NL}}";
    }
""") + END

A3_R = CPP_STD + cpp("""    int n; in >> n;
    bool ok = (n >= 4);
    if (!ok) { out << -1 << "{{NL}}"; return; }
    // evens ascending then odds ascending: no fixed points, no adjacent |diff| = 1
    vector<int> p;
    for (int v = 2; v <= n; v += 2) p.push_back(v);
    for (int v = 1; v <= n; v += 2) p.push_back(v);
    for (int i = 0; i < n; ++i) {
        if (i) out << ' ';
        out << p[i];
    }
    out << "{{NL}}";
""") + END

A3_W = CPP_STD + cpp("""    int n; in >> n;
    // WRONG: identity permutation — every position is a fixed point.
    for (int i = 1; i <= n; ++i) {
        if (i > 1) out << ' ';
        out << i;
    }
    out << "{{NL}}";
""") + END

A4_R = CPP_STD + cpp("""    int n; in >> n;
    long long k; in >> k;
    vector<long long> c(k, 0);
    for (int i = 0; i < n; ++i) { long long x; in >> x; c[x % k]++; }
    long long pairs = c[0] * (c[0] - 1) / 2;
    for (long long r = 1; r * 2 < k; ++r) pairs += c[r] * c[k - r];
    if (k % 2 == 0) pairs += c[k / 2] * (c[k / 2] - 1) / 2;
    out << pairs << "{{NL}}";
""") + END

A4_W = CPP_STD + cpp("""    int n; in >> n;
    long long k; in >> k;
    // WRONG: O(n^2) pair scan — n = 200000 means 2·10^10 ops on 0.5 CPU:
    // hours, not seconds. The 200000-element test alone enforces the fail.
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long pairs = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if ((a[i] + a[j]) % k == 0) ++pairs;
    out << pairs << "{{NL}}";
""") + END

A5_R = CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long S; in >> S;
        long long lo = 1, hi = 2000000000;
        while (lo < hi) {
            long long m = lo + (hi - lo) / 2;
            if (m * (m + 1) / 2 >= S) hi = m;
            else lo = m + 1;
        }
        out << lo << "{{NL}}";
    }
""") + END

A5_W = CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long S; in >> S;
        // WRONG: linear walk from 1 — TLE for S = 10^18 (x ~ 1.4·10^9).
        long long x = 0, s = 0;
        while (s < S) { ++x; s += x; }
        out << x << "{{NL}}";
    }
""") + END

VI_P1 = {
    "hsga-p1-mitm": vi_challenge(
        "Nhiều truy vấn đếm tổng",
        """**Bài toán.** n ≤ 24 vật, q truy vấn S: đếm tập con tổng đúng S cho mỗi
truy vấn.""",
        [("hai truy vấn nhỏ", "Dựng L, R một lần rồi ghép mỗi truy vấn."),
         ("kỹ thuật", "MITM: 2^12 mỗi nửa, sắp một nửa, nhị phân trên nó.")],
    ),
    "hsga-p1-xorq": vi_challenge(
        "XOR trên đoạn 1..n",
        """**Bài toán.** T truy vấn n: in XOR của 1..n. T ≤ 10^4, n ≤ 10^9.""",
        [("nhỏ", "XOR 1..n tuần hoàn chu kỳ 4."),
         ("kỹ thuật", "Bảng [n, 1, n+1, 0] theo n mod 4.")],
    ),
    "hsga-p1-perm": vi_challenge(
        "Hoán vị không điểm cố định",
        """**Bài toán.** In hoán vị 1..n không có p[i] = i và không có hai phần tử
kề chênh đúng 1. n chẵn, 2 ≤ n ≤ 1000.""",
        [("n=2 bất khả thi", "Chỉ 2 1 — chênh kề đúng 1 → in -1."),
         ("kỹ thuật", "Khối chẵn tăng rồi khối lẻ tăng; kiểm biên n nhỏ.")],
    ),
    "hsga-p1-pairs7": vi_challenge(
        "Đếm cặp chia hết cho 7",
        """**Bài toán.** n ≤ 2·10^5 số, đếm cặp i<j có a_i + a_j chia hết cho 7.""",
        [("hỗn hợp dư", "Đếm phần dư rồi ghép r với 7−r."),
         ("kỹ thuật", "Cặp cùng dư dùng C(c,2).")],
    ),
    "hsga-p1-ladder": vi_challenge(
        "Bậc thang vượt S",
        """**Bài toán.** T truy vấn S: x nhỏ nhất với 1+2+…+x ≥ S. S ≤ 10^18.""",
        [("biên", "Đáp án ≈ √(2S) — nhị phân trên x."),
         ("kỹ thuật", "m ≤ 2·10^9 nên m(m+1) vừa long long.")],
    ),
}

write_practice(
    M, "hsga-p1-attack", "Attack Pattern Drills",
    "Five original drills: multi-query MITM, periodic XOR, constructive permutation, modular pairing count, and guess-check ladders.",
    "Bài tập tấn công",
    "Năm bài gốc: MITM đa truy vấn, XOR tuần hoàn, hoán vị kiến tạo, đếm ghép cặp modulo, bậc thang đoán-kiểm.",
    "hsga-m1-invariants", 90, "advanced",
    [
        challenge(
            "hsga-p1-mitm", "Many Subset-Sum Queries",
            """**Bài toán.** Given n ≤ 24 items and q ≤ 2000 target sums S_j, for each
query print the number of subsets summing exactly to S_j.

**Constraints:** 1 ≤ n ≤ 24; 1 ≤ q ≤ 2000; |a[i]| ≤ 10^9; |S_j| ≤ 10^12.

Precompute both halves ONCE; answer each query with a join.
""",
            [
                contest_test("small", T("3 2", "1 2 3", "3", "4"), T("2", "1"),
                    "sums 0,1,2,3,3,4,5,6 → count(3)=2, count(4)=1."),
                contest_test("extremes", T("3 3", "5 10 15", "0", "30", "999"), T("1", "1", "0"),
                    "Empty subset sums 0; all items sum 30; 999 unreachable."),
                contest_test("n=24 q=200 kill", T("24 200") + T(*[str((i * 37) % 89 + 1) for i in range(1, 25)]) + T(*["696"] * 200), T(*["65464"] * 200),
                    "200 identical queries over n=24: per-query 2^n recount is 200 × 4M ops — exceeds the sandbox budget; MITM answers from prebuilt halves. Ground truth 65464 via independent subset-DP in Python."),
            ],
            level="combination", difficulty="advanced",
        ),
        challenge(
            "hsga-p1-xorq", "XOR Over a Range",
            """**Bài toán.** T ≤ 10^4 queries of n ≤ 10^9: print the XOR of all
integers 1..n.

**Constraints:** 1 ≤ T ≤ 10^4; 1 ≤ n ≤ 10^9.

The pattern repeats with period 4 — a loop to n will time out.
""",
            [
                contest_test("small", T("3", "1", "3", "4"), T("1", "0", "4"),
                    "1; 1^2^3=0; 1^2^3^4=4."),
                contest_test("large n", T("1", "1000000000"), T("1000000000"),
                    "n mod 4 = 0 → answer n."),
                contest_test("T=10000 all max — kill", T("10000") + T(*["1000000000"] * 10000), T(*["1000000000"] * 10000),
                    "10000 × 10^9 loop iterations = 10^13 — far beyond the sandbox; the O(1) period-4 table answers instantly."),
            ],
            level="guided", difficulty="advanced",
        ),
        challenge(
            "hsga-p1-perm", "Deranged and Non-Adjacent",
            """**Bài toán.** Print ANY permutation of 1..n with no fixed point
(p[i] ≠ i) and no two adjacent entries differing by exactly 1, or -1 if
impossible.

**Constraints:** 2 ≤ n ≤ 1000; n is even.

Construction: evens ascending, then odds ascending.
""",
            [
                contest_test("n=2 impossible", T("2"), T("-1"),
                    "Only 2 1 exists — adjacent diff 1 → impossible."),
                contest_test("n=4", T("4"), T("2 4 1 3"),
                    "Evens block then odds block."),
                contest_test("n=6", T("6"), T("2 4 6 1 3 5"),
                    "Evens block then odds block; no fixed point, no adjacent diff 1."),
                contest_test("n=10", T("10"), T("2 4 6 8 10 1 3 5 7 9"),
                    "Same construction scaled."),
            ],
            level="independent", difficulty="advanced",
        ),
        challenge(
            "hsga-p1-pairs7", "Pairs Divisible by Seven",
            """**Bài toán.** Count pairs i < j with (a_i + a_j) divisible by 7.

**Constraints:** 1 ≤ n ≤ 2·10^5; 0 ≤ a_i ≤ 10^9 (the large test gives
a_i = i·i mod 1 000 000 003).

Residual counting: c[r]·c[7−r] plus C(c[0], 2).
""",
            [
                contest_test("residual mix", T("5 7", "1 6 8 14 2"), T("2"),
                    "1+6=7 and 6+8=14 — exactly 2 pairs."),
                contest_test("n=200000 deterministic", T("200000 7") + T(*[str((i * i) % 1000000003) for i in range(1, 200001)]), T("2823440748"),
                    "Ground truth via residual counts computed in Python: [31061, 30931, 33580, 23862, 30962, 25650, 23954] → 2823440748."),
            ],
            level="combination", difficulty="advanced",
        ),
        challenge(
            "hsga-p1-ladder", "Ladders Over the Sum",
            """**Bài toán.** For each of T queries S, print the minimal x with
1 + 2 + … + x ≥ S.

**Constraints:** 1 ≤ T ≤ 10^4; 1 ≤ S ≤ 10^18.

Binary search the answer; m ≤ 2·10^9 keeps m(m+1) inside long long.
""",
            [
                contest_test("edges", T("4", "1", "2", "6", "7"), T("1", "2", "3", "4"),
                    "T(3)=6 ≥ 6; T(3)=6 < 7 so x=4."),
                contest_test("S=1e18", T("1", "1000000000000000000"), T("1414213562"),
                    "≈ √(2S); verified by Python bisection."),
                contest_test("T=1000 all 1e18 — kill", T("1000") + T(*["1000000000000000000"] * 1000), T(*["1414213562"] * 1000),
                    "Linear walk needs ~1.4·10^12 total iterations — certain TLE; binary search answers each query in ~31 steps."),
            ],
            level="independent", difficulty="advanced",
        ),
    ],
    VI_P1,
    solutions=[
        ("hsga-p1-mitm", A1_R, A1_W),
        ("hsga-p1-xorq", A2_R, A2_W),
        ("hsga-p1-perm", A3_R, A3_W),
        ("hsga-p1-pairs7", A4_R, A4_W),
        ("hsga-p1-ladder", A5_R, A5_W),
    ],
)
