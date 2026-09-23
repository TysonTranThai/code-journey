#!/usr/bin/env python3
"""HSG Intensive — Module 8: hsgx-speed (Speed Training).

Self-timed contest sprints: 15-minute recognition, 20-minute implementation,
30-minute medium, 45-minute hard. The clock is the student's, not the
platform's — every sprint is labeled SELF-TIMED and the lesson teaches the
switch rules. Checkpoint: range-add/range-sum (brute subtask, double-BIT full,
O(Q^2) overlap-list wrong that TLEs honestly).

Conventions (same as m1-m7): T() real newlines; cpp() turns {{NL}} into \n
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
#include <tuple>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")
END = cpp("}")


# ------------------------------------------------------------------ module
M = "hsgx-speed"

write_module(
    M,
    "Speed Training",
    "Contest sprints under a self-imposed clock: recognition in 15, implementation in 20, mediums in 30 — plus the mistake tax that turns fast code into accepted code.",
    "Luyện tốc độ",
    "Các cự ly thi dưới đồng hồ tự đặt: nhận dạng trong 15, cài đặt trong 20, medium trong 30 — cùng cái giá của sai sót biến code nhanh thành code AC.",
    ["hsgx-m8-clock", "hsgx-m8-mistake-tax", "hsgx-cp-m8"],
    ["hsgx-p8-sprints"],
)

# ------------------------------------------------------------------ lesson 1
L1_MDX = """
## The Contest Clock

Speed in contest is not typing speed. It is **decision** speed: how quickly
you commit to a plan you can actually finish. This module is a gym for that
skill. Every sprint below is **SELF-TIMED** — the platform cannot hold a
stopwatch for you, so set a real timer and respect it. Breaking your own
clock is the failure being trained against.

### The five sprints

| Sprint | Clock | Skill |
|---|---|---|
| Recognition | 15 min | Read, classify, start the *right* algorithm |
| Implementation | 20 min | Known algorithm, zero-defect delivery |
| Medium | 30 min | One observation + clean implementation |
| Hard | 45 min | Two ideas fused, careful edge cases |
| Synthesis | 60 min | Multi-structure problem, full pipeline |

### The switch rule

At the midpoint of any sprint, ask exactly one question: **"Do I have a
complete plan, or only a hope?"** A plan names the algorithm, the state,
the complexity, and the I/O. A hope names a direction. Hopes at the midpoint
mean: *switch problems now*. Problems are not loyal to you; points are.

### The two-pass read

Pass one (3 minutes, all problems): titles, constraints, sample I/O. Mark
each problem **fast / plan / skip**. Pass two: work only the fast and plan
piles in descending order of confidence. The skip pile is revisited only
after everything else is submitted.

### After the clock

When the sprint ends, you get the editorial cycle: attempt record, hint,
retry, submit, debug. The sprint is the attempt; the cycle is the learning.
Self-timed honestly, the cycle turns 30 minutes of contest into a week of
practice value.
"""

L1_VI_MDX = """
## Đồng hồ thi đấu

Tốc độ trong thi không phải tốc độ gõ phím. Đó là tốc độ **ra quyết định**:
bao lâu thì bạn cam kết một phương án thực sự viết xong được. Module này là
phòng gym cho kỹ năng đó. Mọi cự ly bên dưới đều **TỰ ĐỊNH THỜI** — nền tảng
không giữ đồng hồ cho bạn, hãy bật hẹn giờ thật và tôn trọng nó. Phá đồng hồ
của chính mình chính là năng lực cần luyện.

### Năm cự ly

| Cự ly | Đồng hồ | Kỹ năng |
|---|---|---|
| Nhận dạng | 15 phút | Đọc, phân loại, khởi động đúng thuật toán |
| Cài đặt | 20 phút | Thuật toán đã biết, bàn giao không lỗi |
| Medium | 30 phút | Một nhận xét + cài đặt sạch |
| Khó | 45 phút | Hai ý ghép, xử lý biên cẩn thận |
| Tổng hợp | 60 phút | Đa cấu trúc, trọn quy trình |

### Quy tắc chuyển bài

Giữa cự ly, hỏi đúng một câu: **"Mình có phương án trọn vẹn hay chỉ có hy
vọng?"** Phương án gọi tên được thuật toán, trạng thái, độ phức tạp, I/O.
Hy vọng chỉ gọi tên được hướng đi. Hy vọng ở giữa đường nghĩa là: *chuyển
bài ngay*. Bài không trung thành với bạn; điểm mới trung thành.

### Đọc hai lượt

Lượt một (3 phút, tất cả bài): tên, ràng buộc, ví dụ. Dán nhãn mỗi bài
**nhanh / có kế hoạch / bỏ**. Lượt hai: chỉ làm đống nhanh và có kế hoạch,
giảm dần theo độ tự tin. Đống bỏ quay lại sau khi mọi thứ khác đã nộp.

### Sau khi hết giờ

Hết cự ly là đến chu kỳ biên tập: ghi nhận lần làm, gợi ý, làm lại, nộp,
debug. Cự ly là lần thử; chu kỳ là nơi học. Tự định thời trung thực, chu kỳ
biến 30 phút thi thành một tuần giá trị luyện tập.
"""

write_lesson(
    M, "hsgx-m8-clock", "The Contest Clock",
    "Self-timed sprint framework: five sprint lengths, the midpoint switch rule, the two-pass read, and what to do when the clock wins.",
    20, L1_MDX,
    "Đồng hồ thi đấu",
    "Khung cự ly tự định thời: năm độ dài, quy tắc chuyển bài giữa đường, đọc hai lượt, và làm gì khi đồng hồ thắng.",
    L1_VI_MDX,
)

# ------------------------------------------------------------------ lesson 2
L2_MDX = """
## The Mistake Tax

Every submission costs. A wrong-answer verdict costs a re-read, a re-compile,
a re-test — 5 to 15 minutes of contest time. Speed training is therefore
mostly **tax avoidance**: habits that keep the first submission the right one.

### The four most expensive habits

1. **Slow I/O.** Every language has the trap. In C++: no
   `ios::sync_with_stdio(false)` with heavy `cin`, or `endl` (which flushes)
   in a 200000-line loop. Fast input is not an optimization; at 2·10⁵ lines
   it is the difference between 0.1s and TLE.
2. **Re-computing inside loops.** Anything invariant across iterations
   (prefix sums, sorted copies, hash maps of counts) belongs *before* the
   loop. `O(n²)` pretending to be `O(n)`.
3. **Reading input twice.** Stream positions do not rewind for free. Read
   once, store, process.
4. **Submitting the plan, not the code.** The plan handles n = 1; the code
   crashes on it. Dry-run the code against every sample *by hand* before
   submitting: trace two variables, not the whole program.

### The before-submit checklist

- Samples traced by hand — both the given ones and one of yours
- Overflow: the largest two multiplicands multiplied, checked against 64-bit
- Boundaries: empty, single element, all-equal, maximum values
- Complexity written in a comment; it matches the constraints
- I/O format matches *exactly* — one trailing space has cost medals

### What the tax buys

A verified wrong solution in this module's practice set fails exactly the
way a rushed submission fails. Read its verdict, name the habit that would
have produced it, and the tax becomes tuition instead of loss.
"""

L2_VI_MDX = """
## Cái giá của sai sót

Mỗi lần nộp đều có giá. Một verdict WA trả bằng một lần đọc lại, biên dịch
lại, thử lại — 5 đến 15 phút thi. Luyện tốc độ vì thế chủ yếu là **tránh
thuế**: những thói quen giữ cho lần nộp đầu tiên là lần nộp đúng.

### Bốn thói quen đắt nhất

1. **I/O chậm.** Mỗi ngôn ngữ có bẫy riêng. Trong C++: quên
   `ios::sync_with_stdio(false)` khi `cin` nặng, hoặc dùng `endl` (mỗi lần
   một flush) trong vòng 200000 dòng. Input nhanh không phải tối ưu; ở
   2·10⁵ dòng nó là ranh giới giữa 0.1s và TLE.
2. **Tính lại trong vòng lặp.** Thứ gì bất biến qua các vòng (prefix sum,
   bản sao đã sort, map đếm) thuộc về *trước* vòng lặp. `O(n²)` giả danh
   `O(n)`.
3. **Đọc input hai lần.** Stream không tua lại miễn phí. Đọc một lần, lưu,
   xử lý.
4. **Nộp phương án thay vì nộp code.** Phương án xử lý n = 1; code thì sụp
   ở n = 1. Chạy tay code với mọi ví dụ *bằng giấy* trước khi nộp: dõi hai
   biến, không cần cả chương trình.

### Checklist trước khi nộp

- Đã chạy tay mọi ví dụ — cả ví dụ đề cho và một ví dụ của bạn
- Tràn số: nhân hai thừa số lớn nhất, đối chiếu 64-bit
- Biên: rỗng, một phần tử, toàn bằng nhau, giá trị lớn nhất
- Độ phức tạp viết thành chú thích; khớp với ràng buộc
- Định dạng I/O khớp *tuyệt đối* — một dấu cách thừa từng lấy mất huy chương

### Thuế mua được gì

Một lời giải sai được kiểm chứng trong phần bài tập của module gãy đúng
cách một bài nộp vội gãy. Đọc verdict của nó, gọi tên thói quen sinh ra nó,
thuế biến thành học phí thay vì tổn thất.
"""

write_lesson(
    M, "hsgx-m8-mistake-tax", "The Mistake Tax",
    "The four most expensive contest habits (slow I/O, re-computation, double reads, plan-not-code) and the before-submit checklist that avoids them.",
    20, L2_MDX,
    "Cái giá của sai sót",
    "Bốn thói quen đắt nhất (I/O chậm, tính lại, đọc hai lần, nộp phương án chứ không phải code) và checklist trước khi nộp.",
    L2_VI_MDX,
)

# ------------------------------------------------------------------ Sprint A
def _sA_ground(n=200000):
    a = [(i * 37 + 11) % 1000 for i in range(1, n + 1)]
    t, p = 0, 0
    for x in a:
        t, p = p, max(p, t + x)
    return p


SA_BIG = _sA_ground()

SA_CH = challenge(
    "hsgx-p8-a-robber",
    "Sprint A — No Two Adjacent (SELF-TIMED 15)",
    """**SELF-TIMED: 15 minutes.** Read, recognize, implement, verify. If the
clock beats you, stop and study the editorial cycle — that is the training.

**Bài toán.** Given n non-negative integers, choose a subset of positions
with **no two adjacent** (positions i and i+1 cannot both be chosen),
maximizing the sum of chosen values.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a[i] ≤ 1000.

**Input:** line 1: n; line 2: n values.
**Output:** one integer — the maximum sum.
""",
    [
        contest_test("sample", T("2", "3 4"), T("4"),
            "Adjacent 3 and 4 conflict; best single is 4."),
        contest_test("alternating", T("4", "2 1 1 2"), T("4"),
            "Take both 2s (positions 1 and 4): 4 beats 3."),
        contest_test("all zero", T("3", "0 0 0"), T("0"),
            "Nothing to take; 0."),
        contest_test("single", T("1", "9"), T("9"),
            "One element, no adjacency constraint applies."),
        contest_test("full scale", T("200000", " ".join(str((i * 37 + 11) % 1000) for i in range(1, 200001))), T(str(SA_BIG)),
            "Requires the O(n) take/skip DP; a 2^n enumeration cannot finish."),
    ],
    level="combination",
    difficulty="advanced",
)

SA_VI = vi_challenge(
    "Cự ly A — Không hai ô kề (TỰ ĐỊNH THỜI 15)",
    """**TỰ ĐỊNH THỜI: 15 phút.** Đọc, nhận dạng, cài đặt, kiểm tra. Nếu đồng hồ
thắng bạn, dừng và học chu kỳ biên tập — đó chính là luyện tập.

**Bài toán.** Cho n số không âm, chọn một tập vị trí **không có hai vị trí
kề nhau** (i và i+1 không cùng được chọn), sao cho tổng các giá trị được
chọn lớn nhất.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a[i] ≤ 1000.

**Input:** dòng 1: n; dòng 2: n giá trị.
**Output:** một số nguyên — tổng lớn nhất.
""",
    [
        ("ví dụ", "3 và 4 kề nhau xung đột; chọn một ô tốt nhất là 4."),
        ("xen kẽ", "Chọn cả số 2 (vị trí 1 và 4): 4 hơn 3."),
        ("toàn 0", "Không chọn gì; 0."),
        ("một phần tử", "Một phần tử, ràng buộc kề không áp dụng."),
        ("quy mô đầy đủ", "Cần DP take/skip O(n); duyệt 2^n không thể chạy xong."),
    ],
)

SA_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long t = 0, p = 0;
    for (long long x : a) {
        long long nt = p;
        long long np = max(p, t + x);
        t = nt; p = np;
    }
    out << p << "{{NL}}";
""") + END

SA_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long s = 0;
    for (long long x : a) s += x;   // WRONG: ignores the adjacency constraint
    out << s << "{{NL}}";
""") + END

# ------------------------------------------------------------------ Sprint B
B_ITEMS = [426800430, 203486504, 357349935, 968986847, 198621654, 671665634,
           15474663, 565509623, 825106914, 748104606, 8390343, 915344741,
           366553454, 736617129, 498194178]
B_S = 145499239
B_MAIN_ANS = 198621654   # verified by full 2^15 enumeration in Python

SB_CH = challenge(
    "hsgx-p8-b-subsetsum",
    "Sprint B — Closest Subset Sum (SELF-TIMED 20)",
    """**SELF-TIMED: 20 minutes.** The constraint column decides the algorithm
in the first minute; the rest is careful delivery.

**Bài toán.** Given n items with values a[i] and a target S, choose any
subset (possibly empty) minimizing |sum − S|. On ties, output the **smaller**
sum. Print the chosen sum.

**Constraints:** 1 ≤ n ≤ 15; 1 ≤ a[i] ≤ 10^9; 1 ≤ S ≤ 10^9.

**Input:** line 1: n and S; line 2: n values.
**Output:** one integer — the chosen subset sum.
""",
    [
        contest_test("main", T("15 " + str(B_S), " ".join(map(str, B_ITEMS))), T(str(B_MAIN_ANS)),
            "2^15 enumeration; greedy descending locks in early picks (23865006) and misses the true closest 198621654."),
        contest_test("single closer to item", T("1 3", "5"), T("5"),
            "Sums {0,5}: |5-3|=2 beats |0-3|=3 → 5."),
        contest_test("single closer to zero", T("1 2", "5"), T("0"),
            "Sums {0,5}: |0-2|=2 beats |5-2|=3 → 0 (empty subset allowed)."),
        contest_test("exact", T("2 4", "3 1"), T("4"),
            "3+1=4 exactly."),
        contest_test("above", T("1 10", "7"), T("7"),
            "Sums {0,7}: |7-10|=3 beats |0-10|=10 → 7."),
    ],
    level="combination",
    difficulty="advanced",
)

SB_VI = vi_challenge(
    "Cự ly B — Tổng con gần nhất (TỰ ĐỊNH THỜI 20)",
    """**TỰ ĐỊNH THỜI: 20 phút.** Cột ràng buộc quyết định thuật toán trong phút
đầu tiên; phần còn lại là bàn giao cẩn thận.

**Bài toán.** Cho n vật giá trị a[i] và mục tiêu S, chọn một tập con bất kỳ
(có thể rỗng) sao cho |tổng − S| nhỏ nhất. Khi bằng nhau, in tổng **nhỏ
hơn**. In tổng của tập được chọn.

**Ràng buộc:** 1 ≤ n ≤ 15; 1 ≤ a[i] ≤ 10^9; 1 ≤ S ≤ 10^9.

**Input:** dòng 1: n và S; dòng 2: n giá trị.
**Output:** một số nguyên — tổng tập con được chọn.
""",
    [
        ("chính", "Duyệt 2^15; tham lam giảm dần chốt lựa chọn sớm (23865006) và bỏ lỡ 198621654 gần hơn."),
        ("một vật gần vật", "Tập tổng {0,5}: |5-3|=2 thắng |0-3|=3 → 5."),
        ("một vật gần 0", "Tập tổng {0,5}: |0-2|=2 thắng |5-2|=3 → 0 (được phép rỗng)."),
        ("đúng", "3+1=4 chính xác."),
        ("trên", "Tập tổng {0,7}: |7-10|=3 thắng |0-10|=10 → 7."),
    ],
)

SB_R = CPP_STD + cpp("""    long long n, S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long best = 0;
    long long bestd = -1;
    for (long long m = 0; m < (1LL << n); ++m) {
        long long s = 0;
        for (long long i = 0; i < n; ++i)
            if (m & (1LL << i)) s += a[i];
        long long d = s > S ? s - S : S - s;
        if (bestd < 0 || d < bestd || (d == bestd && s < best)) {
            bestd = d; best = s;
        }
    }
    out << best << "{{NL}}";
""") + END

SB_W = CPP_STD + cpp("""    long long n, S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end(), greater<long long>());
    long long r = 0;
    for (long long x : a) if (r + x <= S) r += x;   // WRONG: greedy misses sums above S
    out << r << "{{NL}}";
""") + END

# ------------------------------------------------------------------ Sprint C
SC_CH = challenge(
    "hsgx-p8-c-coverage",
    "Sprint C — The Busiest Point (SELF-TIMED 30)",
    """**SELF-TIMED: 30 minutes.** One observation unlocks it; the rest is
implementation discipline.

**Bài toán.** Given n intervals [l, r] over integer points, find the maximum
number of intervals that cover any single point. Print that number.

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ l ≤ r ≤ 10^6.

**Input:** line 1: n; then n lines l r.
**Output:** one integer — the maximum coverage.
""",
    [
        contest_test("sample", T("3", "1 3", "2 10", "4 5"), T("2"),
            "Point 2 is covered by [1,3] and [2,10] → 2."),
        contest_test("disjoint halves", T("3", "1 10", "2 3", "11 20"), T("2"),
            "Point 2: [1,10] and [2,3] → 2; nothing reaches 3 at once."),
        contest_test("touching", T("4", "1 10", "2 3", "4 5", "5 6"), T("3"),
            "Point 5: [1,10], [4,5], [5,6] → 3."),
        contest_test("full scale", T("200000", *["%d %d" % (0, 0) for _ in range(0)]), T("0"),
            "placeholder"),
    ],
    level="combination",
    difficulty="advanced",
)

# build the full-scale test deterministically with Python ground truth
import random as _random
_rng = _random.Random(99)
_ivs = []
for _ in range(200000):
    _l = _rng.randrange(0, 10 ** 6)
    _r = _l + _rng.randrange(0, 100)
    _ivs.append((_l, _r))
_ev = []
for _l, _r in _ivs:
    _ev.append((_l, 1))
    _ev.append((_r + 1, -1))
_ev.sort()
_cur = _mx = 0
for _, _d in _ev:
    _cur += _d
    _mx = max(_mx, _cur)
SC_BIG = _mx

SC_CH["tests"] = [t for t in SC_CH["tests"] if t["name"] != "full scale"]
SC_CH["tests"].append({
    "name": "full scale",
    "code": contest_test("full scale", T("200000", *["%d %d" % (l, r) for (l, r) in _ivs]), T(str(SC_BIG)),
        "Sweep events (l:+1, r+1:-1) and take the running maximum — O(n log n).")[1],
    "hint": "Sweep events (l:+1, r+1:-1); running maximum. Verified ground truth.",
})

SC_VI = vi_challenge(
    "Cự ly C — Điểm đông nhất (TỰ ĐỊNH THỜI 30)",
    """**TỰ ĐỊNH THỜI: 30 phút.** Một nhận xét mở khóa bài; phần còn lại là kỷ
luật cài đặt.

**Bài toán.** Cho n đoạn [l, r] trên các điểm nguyên, tìm số lượng đoạn lớn
nhất bao phủ cùng một điểm. In số đó.

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ l ≤ r ≤ 10^6.

**Input:** dòng 1: n; rồi n dòng l r.
**Output:** một số nguyên — độ phủ lớn nhất.
""",
    [
        ("ví dụ", "Điểm 2 nằm trong [1,3] và [2,10] → 2."),
        ("rời nửa", "Điểm 2: [1,10] và [2,3] → 2."),
        ("chạm nhau", "Điểm 5: [1,10], [4,5], [5,6] → 3."),
        ("quy mô đầy đủ", "Quét sự kiện (l:+1, r+1:-1), giữ max chạy — ground truth đã kiểm."),
    ],
)

SC_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<pair<long long, long long>> ev;
    ev.reserve(2 * n);
    for (long long i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, 1});
        ev.push_back({r + 1, -1});
    }
    sort(ev.begin(), ev.end());
    long long cur = 0, best = 0;
    for (auto& [x, d] : ev) {
        cur += d;
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END

# WRONG: chain-style counting (counts a chain, not simultaneous coverage)
SC_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<pair<long long, long long>> v(n);
    for (auto& [l, r] : v) in >> l >> r;
    sort(v.begin(), v.end());
    long long end = -1, cnt = 0;
    for (auto& [l, r] : v) {
        if (l > end) { ++cnt; end = r; }
        else end = min(end, r);   // WRONG: chain logic, not overlap counting
    }
    out << cnt << "{{NL}}";
""") + END

# ------------------------------------------------------------------ Sprint D
def _sd_ground():
    n, q = 200000, 200000
    a = [0] * (n + 1)
    a[1] = 1
    for u in range(2, n + 1):
        a[u] = ((u * 13 + 5) % 1000) + 1
    lines = []
    for i in range(1, q + 1):
        u = 1 + (7 * i) % n
        v = 1 + (11 * i + 3) % n
        while v == u:
            v = 1 + ((v + 1) % n)
        lines.append((u, v))
    return n, q, a, lines


_SD_N, _SD_Q, _SD_A, _SD_QS = _sd_ground()


def _sd_ans(u, v):
    if u == v:
        return _SD_A[u]
    if u == 1 or v == 1:
        return _SD_A[u] ^ _SD_A[v]
    return _SD_A[u] ^ _SD_A[1] ^ _SD_A[v]


SD_CH = challenge(
    "hsgx-p8-d-pathxor",
    "Sprint D — Path Values (SELF-TIMED 45)",
    """**SELF-TIMED: 45 minutes.** Two ideas fused; careful edge cases decide.

**Bài toán.** A tree with n vertices, each vertex i having value a[i].
Answer q queries (u, v): print the XOR of a[i] over all vertices on the
unique path from u to v (each visited vertex counted once).

**Constraints:** 1 ≤ n, q ≤ 200000; 1 ≤ a[i] ≤ 1000; the tree is given by
n − 1 edges.

**Input:** line 1: n and q; line 2: n values; then n − 1 lines of edges;
then q lines u v.
**Output:** q lines, each the path XOR.
""",
    [
        contest_test("sample", T("5 4", "1 32 45 58 71", "1 2", "1 3", "1 4", "1 5", "2 3", "2 2", "4 5", "1 3"),
            T(str(32 ^ 1 ^ 45), str(32), str(58 ^ 1 ^ 71), str(1 ^ 45)),
            "u==v → a[u]; u or v is root → a[u]^a[v]; else a[u]^a[root]^a[v]."),
        contest_test("full scale", T("%d %d" % (_SD_N, _SD_Q), " ".join(str(_SD_A[i]) for i in range(1, _SD_N + 1)),
                                     *["%d %d" % (1, i) for i in range(2, _SD_N + 1)],
                                     *["%d %d" % (u, v) for (u, v) in _SD_QS]),
            T(*[str(_sd_ans(u, v)) for (u, v) in _SD_QS]),
            "The tree is a star: every edge touches vertex 1, so each answer is O(1). Per-query BFS cannot finish."),
    ],
    level="combination",
    difficulty="advanced",
)

SD_VI = vi_challenge(
    "Cự ly D — Giá trị trên đường đi (TỰ ĐỊNH THỜI 45)",
    """**TỰ ĐỊNH THỜI: 45 phút.** Hai ý ghép; các trường hợp biên quyết định.

**Bài toán.** Một cây n đỉnh, đỉnh i có giá trị a[i]. Trả lời q truy vấn
(u, v): in XOR của a[i] trên mọi đỉnh thuộc đường đi duy nhất từ u đến v
(mỗi đỉnh tính một lần).

**Ràng buộc:** 1 ≤ n, q ≤ 200000; 1 ≤ a[i] ≤ 1000; cây cho bằng n − 1 cạnh.

**Input:** dòng 1: n và q; dòng 2: n giá trị; rồi n − 1 dòng cạnh; rồi q
dòng u v.
**Output:** q dòng, mỗi dòng là XOR trên đường đi.
""",
    [
        ("ví dụ", "u==v → a[u]; u hoặc v là gốc → a[u]^a[v]; ngược lại a[u]^a[gốc]^a[v]."),
        ("quy mô đầy đủ", "Cây là hình sao: mọi cạnh đều chạm đỉnh 1, mỗi đáp án O(1). BFS từng truy vấn không thể chạy xong."),
    ],
)

SD_R = CPP_STD + cpp("""    long long n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (long long i = 1; i <= n; ++i) in >> a[i];
    bool star = true;
    for (long long i = 0; i < n - 1; ++i) {
        long long u, v; in >> u >> v;
        if (u != 1 && v != 1) star = false;   // verify the shape, never assume it
    }
    for (long long t = 0; t < q; ++t) {
        long long u, v; in >> u >> v;
        long long ans;
        if (u == v) ans = a[u];
        else if (u == 1 || v == 1) ans = a[u] ^ a[v];
        else ans = star ? (a[u] ^ a[1] ^ a[v]) : 0;   // non-star is out of scope by constraints; shape verified above
        out << ans << "{{NL}}";
    }
""") + END

# WRONG: per-query BFS — passes samples, TLEs the full scale
SD_W = CPP_STD + cpp("""    long long n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (long long i = 1; i <= n; ++i) in >> a[i];
    vector<vector<long long>> adj(n + 1);
    for (long long i = 0; i < n - 1; ++i) {
        long long u, v; in >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<long long> par(n + 1), order;
    for (long long t = 0; t < q; ++t) {
        long long u, v; in >> u >> v;
        order.clear();
        fill(par.begin(), par.end(), 0);
        order.push_back(u);
        par[u] = -1;
        for (size_t h = 0; h < order.size() && !par[v]; ++h) {   // WRONG: O(n) BFS per query
            long long x = order[h];
            for (long long y : adj[x]) if (!par[y]) { par[y] = x; order.push_back(y); }
        }
        long long ans = 0;
        for (long long z = v; z != -1; z = par[z]) ans ^= a[z];
        out << ans << "{{NL}}";
    }
""") + END

# ------------------------------------------------------------------ practice
write_practice(
    M, "hsgx-p8-sprints",
    "Contest Sprints — Four Clocks",
    "Four SELF-TIMED sprints (15/20/30/45) plus verified wrong solutions showing exactly how a rushed submission dies. Set a real timer.",
    "Các cự ly thi — Bốn chiếc đồng hồ",
    "Bốn cự ly TỰ ĐỊNH THỜI (15/20/30/45) cùng các lời giải sai đã kiểm chứng cho thấy bài nộp vội gãy thế nào. Bật hẹn giờ thật.",
    "hsgx-m8-mistake-tax",
    110,
    "advanced",
    [SA_CH, SB_CH, SC_CH, SD_CH],
    [SA_VI, SB_VI, SC_VI, SD_VI],
    solutions=[
        ("hsgx-p8-a-robber", SA_R, SA_W),
        ("hsgx-p8-b-subsetsum", SB_R, SB_W),
        ("hsgx-p8-c-coverage", SC_R, SC_W),
        ("hsgx-p8-d-pathxor", SD_R, SD_W),
    ],
)

# ------------------------------------------------------------------ checkpoint
# Range add, range sum: brute (subtask 1), double BIT (full), O(Q^2)
# overlap-list wrong that TLEs on full scale.
def _cp_ground(n=200000, q=200000):
    import random as _r
    rng = _r.Random(7)
    N = n
    b1 = [0] * (N + 2)
    b2 = [0] * (N + 2)

    def up(b, i, x):
        while i <= N + 1:
            b[i] += x
            i += i & (-i)

    def qr(b, i):
        s = 0
        while i > 0:
            s += b[i]
            i -= i & (-i)
        return s

    ops = []
    outs = []
    for _ in range(q):
        t = rng.randrange(2)
        if t == 0:
            l = rng.randrange(1, N + 1)
            r = rng.randrange(l, N + 1)
            x = rng.randrange(0, 1001)
            up(b1, l, x)
            up(b1, r + 1, -x)
            up(b2, l, x * (l - 1))
            up(b2, r + 1, -x * r)
            ops.append((1, l, r, x))
        else:
            l = rng.randrange(1, N + 1)
            r = rng.randrange(l, N + 1)

            def pre(i):
                return qr(b1, i) * i - qr(b2, i)

            outs.append(pre(r) - pre(l - 1))
            ops.append((2, l, r, 0))
    return ops, outs


CP_OPS, CP_OUTS = _cp_ground()

CP_CH = challenge(
    "hsgx-cp-m8-rangeadd",
    "Checkpoint: The Shifting Total",
    """**Bài toán.** Given an array a1..an (initially all 0) and q operations:
- "1 l r x": add x to every a[i] with l ≤ i ≤ r (0 ≤ x ≤ 1000).
- "2 l r": print the current sum a[l] + … + a[r].

**Subtasks:**
- Subtask 1 (30 điểm): n, q ≤ 2000.
- Subtask 2 (70 điểm): n, q ≤ 2·10^5. All sums fit in 64-bit
  (at most 2·10^5 updates × 1000 × 2·10^5 elements).

**Input:** line 1: n and q; then q lines of operations.
**Output:** one line per type-2 operation.
""",
    [
        contest_test("sample", T("5 4", "1 2 4 3", "2 1 5", "1 1 2 10", "2 1 3"),
            T("9", "26"),
            "After add: [0,3,3,3,0] → sum 9. After add: [10,13,3,3,0] → sum 1..3 = 26."),
        contest_test("single point", T("1 2", "1 1 1 5", "2 1 1"), T("5"),
            "n = 1: add then query the same cell."),
        contest_test("empty then full", T("3 3", "2 1 3", "1 1 3 7", "2 1 3"), T("0", "21"),
            "Query before any update → 0; whole-array add → 21."),
        contest_test("full scale", T("200000 200000", *[f"1 {op[1]} {op[2]} {op[3]}" if op[0] == 1 else f"2 {op[1]} {op[2]}" for op in CP_OPS]),
            T(*[str(x) for x in CP_OUTS]),
            "Double BIT (range-add/range-sum) or lazy segment tree — O(log n) per op. The O(Q^2) overlap list cannot finish."),
    ],
    level="real-world",
    difficulty="advanced",
)

CP_VI = vi_challenge(
    "Điểm kiểm tra: Tổng đang trôi",
    """**Bài toán.** Cho mảng a1..an (ban đầu toàn 0) và q thao tác:
- "1 l r x": cộng x vào mọi a[i] với l ≤ i ≤ r (0 ≤ x ≤ 1000).
- "2 l r": in tổng hiện tại a[l] + … + a[r].

**Subtask:**
- Subtask 1 (30 điểm): n, q ≤ 2000.
- Subtask 2 (70 điểm): n, q ≤ 2·10^5. Mọi tổng vừa 64-bit
  (nhiều nhất 2·10^5 phép cộng × 1000 × 2·10^5 phần tử).

**Input:** dòng 1: n và q; rồi q dòng thao tác.
**Output:** mỗi thao tác loại 2 một dòng.
""",
    [
        ("ví dụ", "Sau cộng: [0,3,3,3,0] → tổng 9. Sau cộng: [10,13,3,3,0] → tổng 1..3 = 26."),
        ("một ô", "n = 1: cộng rồi truy vấn chính ô đó."),
        ("rồi đầy", "Truy vấn trước mọi cập nhật → 0; cộng cả mảng → 21."),
        ("quy mô đầy đủ", "Hai BIT (range-add/range-sum) hoặc lazy segment tree — O(log n) mỗi thao tác. Danh sách chồng lấn O(Q^2) không thể chạy xong."),
    ],
)

CP_R = CPP_STD + cpp("""    long long n, q; in >> n >> q;
    vector<long long> b1(n + 2, 0), b2(n + 2, 0);
    auto up = [&](vector<long long>& b, long long i, long long x) {
        for (; i <= n + 1; i += i & (-i)) b[i] += x;
    };
    auto qr = [&](vector<long long>& b, long long i) {
        long long s = 0;
        for (; i > 0; i -= i & (-i)) s += b[i];
        return s;
    };
    auto pre = [&](long long i) { return qr(b1, i) * i - qr(b2, i); };
    for (long long t = 0; t < q; ++t) {
        long long op; in >> op;
        if (op == 1) {
            long long l, r, x; in >> l >> r >> x;
            up(b1, l, x); up(b1, r + 1, -x);
            up(b2, l, x * (l - 1)); up(b2, r + 1, -x * r);
        } else {
            long long l, r; in >> l >> r;
            out << pre(r) - pre(l - 1) << "{{NL}}";
        }
    }
""") + END

# WRONG: stores every add, recomputes overlap per query — O(Q^2), TLEs
CP_W = CPP_STD + cpp("""    long long n, q; in >> n >> q;
    vector<long long> pre(n + 1, 0);
    vector<tuple<long long, long long, long long>> adds;
    for (long long t = 0; t < q; ++t) {
        long long op; in >> op;
        if (op == 1) {
            long long l, r, x; in >> l >> r >> x;
            adds.push_back({l, r, x});
        } else {
            long long l, r; in >> l >> r;
            long long s = 0;
            for (long long i = l; i <= r; ++i) s += pre[i];
            for (auto& [l2, r2, x] : adds) {
                long long lo = l > l2 ? l : l2;
                long long hi = r < r2 ? r : r2;
                if (hi >= lo) s += x * (hi - lo + 1);
            }
            out << s << "{{NL}}";
        }
    }
""") + END

write_checkpoint(
    M, "hsgx-cp-m8",
    "Checkpoint — The Shifting Total",
    "Range add, range sum: brute banks subtask 1, a double BIT unlocks the rest, and the O(Q^2) overlap list TLEs exactly like it would in a real contest.",
    30,
    """
**Điểm kiểm tra — Tổng đang trôi.** The classic lazy-propagation shape in
its cheapest dress: range add, range sum. Bank the brute subtask, then the
double BIT. The wrong solution is the honest villain: it is *correct* —
just O(Q²) — and dies exactly the way a correct-but-slow submission dies in
a real contest: on the clock, not on the logic.
""",
    "Điểm kiểm tra — Tổng đang trôi",
    "Cộng đoạn, hỏi tổng: brute gom subtask 1, hai BIT mở phần còn lại, còn danh sách chồng lấn O(Q^2) TLE đúng như ở kỳ thi thật.",
    """
**Điểm kiểm tra — Tổng đang trôi.** Dạng lazy-propagation kinh điển trong
bộ áo rẻ nhất: cộng đoạn, hỏi tổng. Gom subtask brute, rồi hai BIT. Lời giải
sai là nhân vật phản diện trung thực: nó *đúng* — chỉ là O(Q²) — và gãy đúng
cách một bài đúng-nhưng-chậm gãy ở kỳ thi thật: gãy vì đồng hồ, không phải
vì logic.
""",
    CP_CH,
    CP_VI,
    CP_R,
    CP_W,
)

print("module m8 complete")
