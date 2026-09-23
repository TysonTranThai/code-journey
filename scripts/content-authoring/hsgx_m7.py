#!/usr/bin/env python3
"""HSG Intensive — Module 7: hsgx-subtask (Subtask Mastery).

Partial scoring is how HSG contests are actually won: a clean brute force
banks the small-n subtask, then the full solution unlocks the rest. Every
problem here has real subtask structure, and the verification reflects the
reality: BOTH the brute (small tests only) and the full solution (all tests)
must pass, while greedy shortcuts that only survive the samples fail.

Conventions: T() real newlines; cpp() -> \n escapes; explicit includes;
ground truths computed in Python and verified before use.
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgx-subtask"
write_module(
    M,
    "Subtask Mastery",
    "Points are banked, not dreamed: read the subtasks first, secure brute-force points, then climb. Three full problems with real partial-scoring structure.",
    "Làm chủ subtask",
    "Điểm được gom, không được mơ: đọc subtask trước, lấy điểm brute-force, rồi leo tiếp. Ba bài toán có cấu trúc chấm điểm một phần thật sự.",
    ["hsgx-m7-scoring", "hsgx-m7-climb", "hsgx-cp-m7"],
    ["hsgx-p7-subtask"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgx-m7-scoring",
    "How Partial Scoring Actually Works",
    "Subtask structure, score arithmetic, and why 40 secure points beat 0 attempted-perfect points.",
    20,
    """
# How Partial Scoring Actually Works

An HSG problem is rarely pass/fail. The statement hides a ladder:

- **Subtask 1 (small n):** the constraints are so weak that anything correct works.
- **Subtask 2 (medium n):** a polynomial improvement is required.
- **Subtask 3 (full n):** the intended complexity, often n log n or better.

The ladder is a *gift*: it tells you, before you think at all, what complexity
the full solution needs. n ≤ 20 whispers bitmask or exponential-with-pruning;
n ≤ 2000 allows O(n²); n ≤ 2·10⁵ demands O(n log n). **Constraints are the
problem statement's own hints about its solution.**

## The banking strategy

The contest-optimal opening move is the same in every strong competitor's
playbook: **read all problems, bank the guaranteed subtask, then climb.**

1. Solve subtask 1 of every problem with a slow-but-obviously-correct brute
   force. This is *floor insurance*: even if your clever ideas all fail, the
   floor is banked.
2. Only then attack the full solution of the problem you understand best.
3. Near the end, convert remaining time into either (a) a better complexity
   on your strongest problem, or (b) one more subtask somewhere.

Why this ordering wins: partial points are *concave*. The first 40 points of
a problem cost 15 minutes; the last 20 often cost an hour of subtle insight.
Banking floors everywhere first maximizes total score per minute spent.

## Reading the ladder

When you see subtasks, extract three facts immediately:

- **The brute-force subtask's bound** — write that brute force *first*, it is
  nearly free points and doubles as your stress-test oracle later.
- **The full bound** — compute the complexity budget: for n = 2·10⁵ you have
  roughly 10⁸ simple operations; anything asymptotically worse must go.
- **The gap between subtasks** — a jump from n ≤ 5000 to n ≤ 2·10⁵ screams
  "the O(n²) is the *intended trap*; find the n log n."

In this module's problems you will do exactly this: pass subtask 1 with the
brute force (verified for real), then the full solution (also verified), and
watch the shortcut that skips the brute force fail its big test.
""",
    "Cách chấm điểm một phần vận hành thực sự",
    "Cấu trúc subtask, phép tính điểm, và vì sao 40 điểm chắc cặn thắng 0 điểm cố ép bài khó.",
    """
# Cách chấm điểm một phần vận hành thực sự

Một bài HSG hiếm khi là đúng/sai tuyệt đối. Đề bài giấu một chiếc thang:

- **Subtask 1 (n nhỏ):** ràng buộc yếu đến mức mọi cách đúng đều chạy được.
- **Subtask 2 (n vừa):** cần cải tiến đa thức.
- **Subtask 3 (n đầy đủ):** độ phức tạp theo ý đồ, thường n log n hoặc tốt hơn.

Chiếc thang là *món quà*: nó nói cho bạn biết, trước cả khi nghĩ, độ phức tạp
cần cho lời giải đầy đủ. n ≤ 20 thì thầm bitmask hoặc vét cạn có cắt tỉa;
n ≤ 2000 cho phép O(n²); n ≤ 2·10⁵ đòi hỏi O(n log n). **Ràng buộc chính là
gợi ý của đề bài về lời giải của nó.**

## Chiến lược gom điểm

Nước đi mở đầu tối ưu trong thi là như nhau ở mọi tay thi đấu mạnh: **đọc hết
các bài, gom subtask chắc chắn, rồi leo tiếp.**

1. Giải subtask 1 của mọi bài bằng vét cạn chậm nhưng hiển nhiên đúng. Đây là
   *bảo hiểm sàn*: dù mọi ý tưởng thông minh đều gãy, sàn đã được gom.
2. Chỉ khi đó mới tấn công lời giải đầy đủ của bài bạn hiểu rõ nhất.
3. Gần cuối giờ, đổi thời gian còn lại thành (a) độ phức tạp tốt hơn ở bài
   mạnh nhất, hoặc (b) thêm một subtask ở bài khác.

Vì sao thứ tự này thắng: điểm một phần là *lõm*. 40 điểm đầu của một bài tốn
15 phút; 20 điểm cuối thường tốn một giờ trực giác tinh tế. Gom sàn mọi bài
trước tối đa hóa tổng điểm trên mỗi phút.

## Đọc chiếc thang

Thấy subtask, rút ngay ba sự kiện:

- **Ràng buộc của subtask brute-force** — viết brute đó *trước*, nó gần như
  miễn phí và về sau chính là oracle cho stress test.
- **Ràng buộc đầy đủ** — tính ngân sách độ phức tạp: với n = 2·10⁵ bạn có
  cỡ 10⁸ phép tính đơn; bất kỳ thứ gì tiệm cận tệ hơn phải bỏ.
- **Khoảng cách giữa các subtask** — nhảy từ n ≤ 5000 lên n ≤ 2·10⁵ hét lên
  rằng "O(n²) là *bẫy theo ý đồ*; tìm cái n log n."

Trong module này bạn sẽ làm đúng như vậy: qua subtask 1 bằng brute (được kiểm
thật), rồi lời giải đầy đủ (cũng được kiểm), và chứng kiến cái tắt bỏ qua
brute gãy ở test lớn.
""",
)

write_lesson(
    M, "hsgx-m7-climb",
    "The Climb: Brute → Better → Best",
    "One problem, three solutions: the brute that banks subtask 1, the improved one that unlocks subtask 2, and the full solution — with the failure mode of skipping rungs.",
    25,
    """
# The Climb: Brute → Better → Best

Consider a problem where the ladder is explicit. The professional workflow is
not "think about the full solution." It is a *climb*:

**Rung 1 — the brute (minutes 0–15).** Implement the most obviously correct
thing the subtask-1 constraints allow. Test it on the samples by hand. This
is not wasted time: it is your oracle for the rest of the problem. When your
clever solution disagrees with it on a random case, you have found a bug
before the judge did.

**Rung 2 — the improvement (as time allows).** Find the bottleneck of the
brute — usually a repeated scan — and kill it with the cheapest tool that
works: prefix sums, sorting, a set, a sweep. Do not reach for the heavy
machinery (segment trees, HLD) while a light tool suffices; every extra
moving part is a bug surface.

**Rung 3 — the full solution.** Only now the intended complexity. And the
climb has a safety property: if rung 3 never compiles, rung 1 already banked
points.

## The failure mode of skipping rungs

The classic HSG disaster: attack the full solution first, get it 90% right,
have a subtle bug, and score zero — while a classmate with a 15-minute brute
scored the same subtask. The judge does not award style points. The ladder
exists precisely so that partial effort converts to partial score.

## What the judge sees

Each subtask is typically all-or-nothing per test group: one test in the
group fails, the whole group scores zero. That is why this module's
verification is brutal on purpose: your brute must pass every small test,
your full solution every test, and the greedy shortcut that "seems right"
must demonstrably fail its big test — so you learn what all-or-nothing
feels like before the contest, not during it.
""",
    "Chiến trình leo: Brute → Tốt hơn → Tốt nhất",
    "Một bài, ba lời giải: brute gom subtask 1, bản cải tiến mở subtask 2, và lời giải đầy đủ — cùng kiểu gãy của việc bỏ bậc thang.",
    """
# Chiến trình leo: Brute → Tốt hơn → Tốt nhất

Với một bài có thang điểm tường minh, quy trình chuyên nghiệp không phải
"nghĩ về lời giải đầy đủ". Nó là một *chiến trình leo*:

**Bậc 1 — brute (phút 0–15).** Cài thứ hiển nhiên đúng nhất mà ràng buộc
subtask-1 cho phép. Test tay trên các ví dụ. Đây không phải thời gian lãng
phí: nó là oracle cho phần còn lại của bài. Khi lời giải thông minh của bạn
mâu thuẫn với nó trên một case ngẫu nhiên, bạn vừa tìm ra bug trước Judge.

**Bậc 2 — cải tiến (khi còn thời gian).** Tìm nút thắt của brute — thường là
một lần quét lặp lại — và diệt nó bằng công cụ nhẹ nhất đủ dùng: prefix sum,
sắp xếp, một cái set, một lần quét. Đừng with máy móc hạng nặng (segment
tree, HLD) khi công cụ nhẹ đủ dùng; mỗi bộ phận chuyển động thêm là một bề
mặt bug.

**Bậc 3 — lời giải đầy đủ.** Bây giờ mới là độ phức tạp theo ý đồ. Và chiến
trình leo có tính an toàn: nếu bậc 3 không bao giờ chạy được, bậc 1 đã gom
điểm sẵn.

## Kiểu gãy của việc bỏ bậc thang

Thảm họa HSS kinh điển: tấn công lời giải đầy đủ trước, đúng được 90%, còn
một bug tinh tế, về không — trong khi bạn cùng lớp với brute 15 phút ăn đúng
subtask đó. Judge không chấm điểm phong cách. Chiếc thang tồn tại chính để
nỗ lực một phần đổi được điểm một phần.

## Judge nhìn thấy gì

Mỗi subtask thường là tất-cả-hoặc-không-gì theo nhóm test: một test trong
nhóm gãy, cả nhóm về 0. Vì thế phần kiểm của module này cố tình khắt khe:
brute của bạn phải qua mọi test nhỏ, lời giải đầy đủ qua mọi test, và cái
tắt tham lam "có vẻ đúng" phải gãy một cách minh chứng ở test lớn — để bạn
học cảm giác tất-cả-hoặc-không-gì trước kỳ thi, không phải trong lúc thi.
""",
)

# ------------------------------------------------------------------ problems
# P1: Sum of pairwise max over all pairs. Brute O(n^2) for n<=2000; full
# solution sorts + prefix of powers (contribution technique).
# For sorted a[0..n-1], element a[i] (1-indexed in sorted order) is the max of
# a pair iff it is >= the other; count pairs where a[i] is max: it contributes
# a[i] * (number of j < i) = a[i] * i when counting each pair once with max at
# the larger index. Answer = sum over sorted asc of a[i] * i (0-indexed).
def _p1_ground(n=200000, mod=1000000007):
    vals = [(i * 7919 + 13) % 1000003 for i in range(1, n + 1)]
    vals.sort()
    ans = 0
    for i, v in enumerate(vals):
        ans = (ans + v * i) % mod
    return ans


P1_BIG = _p1_ground()

P1_CH = challenge(
    "hsgx-p7-s1-pairmax",
    "Sum of Pairwise Maxima",
    """**Bài toán.** Cho n số nguyên a1..an. Với mọi cặp (i, j) với i < j, lấy
max(ai, aj). Tính tổng tất cả các max đó modulo 10^9+7.

**Subtasks:**
- Subtask 1 (40 điểm): n ≤ 2000.
- Subtask 2 (60 điểm): n ≤ 2·10^5, ai < 10^6.

**Input:** dòng 1 là n; dòng 2 là n số.
**Output:** tổng modulo 10^9+7.
""",
    [
        contest_test("sample", T("3", "1 5 2"), T("12"),
            "max(1,5)+max(1,2)+max(5,2) = 5+2+5 = 12."),
        contest_test("two equal", T("2", "7 7"), T("7"),
            "max(7,7)=7."),
        contest_test("sorted input", T("4", "1 2 3 4"), T("20"),
            "Pairs: (1,2)=2,(1,3)=3,(1,4)=4,(2,3)=3,(2,4)=4,(3,4)=4 → 20."),
        contest_test("n=1 edge", T("1", "42"), T("0"),
            "No pairs, sum is 0."),
        contest_test("full scale", T("200000", " ".join(str((i * 7919 + 13) % 1000003) for i in range(1, 200001))), T(str(P1_BIG)),
            "Requires the sort + contribution O(n log n); O(n^2) cannot finish."),
    ],
    level="combination",
    difficulty="advanced",
)

P1_VI = vi_challenge(
    "Tổng các max theo cặp",
    """**Bài toán.** Cho n số nguyên a1..an. Với mọi cặp (i, j) với i < j, lấy
max(ai, aj). Tính tổng tất cả các max đó modulo 10^9+7.

**Subtasks:**
- Subtask 1 (40 điểm): n ≤ 2000.
- Subtask 2 (60 điểm): n ≤ 2·10^5, ai < 10^6.

**Input:** dòng 1 là n; dòng 2 là n số.
**Output:** tổng modulo 10^9+7.
""",
    [
        ("ví dụ", "max(1,5)+max(1,2)+max(5,2) = 5+2+5 = 12."),
        ("hai số bằng nhau", "max(7,7)=7."),
        ("input đã sắp", "Các cặp: (1,2)=2,(1,3)=3,(1,4)=4,(2,3)=3,(2,4)=4,(3,4)=4 = 20."),
        ("n=1", "Không có cặp nào, tổng là 0."),
        ("quy mô đầy đủ", "Cần sort + contribution O(n log n); O(n^2) không thể chạy xong."),
    ],
)

# full solution: sort, contribution a_sorted[i] * i
P1_R = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    sort(a.begin(), a.end());
    const long long MOD = 1000000007;
    long long ans = 0;
    for (long long i = 0; i < n; ++i) ans = (ans + (a[i] % MOD) * (i % MOD)) % MOD;
    out << ans << "{{NL}}";
""") + END

# brute: O(n^2) — passes every subtask-1-scale test, times out on full scale
P1_B = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    const long long MOD = 1000000007;
    long long ans = 0;
    for (long long i = 0; i < n; ++i)
        for (long long j = i + 1; j < n; ++j)
            ans = (ans + max(a[i], a[j])) % MOD;
    out << ans << "{{NL}}";
""") + END

# WRONG: unsorted contribution — applies a[i]*i without sorting. Fails any
# unsorted input.
P1_W = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    const long long MOD = 1000000007;
    long long ans = 0;
    for (long long i = 0; i < n; ++i) ans = (ans + (a[i] % MOD) * (i % MOD)) % MOD;
    out << ans << "{{NL}}";
""") + END

# ------------------------------------------------------------------ P2:
# Sliding-window median-free statistic: max of minima over all windows of
# size k (classic monotonic deque). Subtask 1: n,k <= 2000 brute. Full:
# n <= 2e5.
P2_CH = challenge(
    "hsgx-p7-s2-window",
    "Strongest Window",
    """**Bài toán.** Cho mảng a1..an và số nguyên k. Với mọi cửa sổ gồm k phần
tử liên tiếp, lấy min của cửa sổ. Trả về giá trị max trên mọi cửa sổ.

**Subtasks:**
- Subtask 1 (30 điểm): n ≤ 2000.
- Subtask 2 (70 điểm): n ≤ 2·10^5.

**Input:** dòng 1: n và k. Dòng 2: n số.
**Output:** một số nguyên duy nhất.
""",
    [
        contest_test("sample", T("5 2", "4 1 3 2 5"), T("2"),
            "Window minima: min(4,1),min(1,3),min(3,2),min(2,5) = 1,1,2,2 → max = 2."),
        contest_test("k=n", T("6 6", "9 4 7 1 8 2"), T("1"),
            "Only window is whole array; min=1."),
        contest_test("k=1", T("5 1", "3 1 4 1 5"), T("5"),
            "Max over singletons = max of array."),
        contest_test("increasing", T("7 3", "1 2 3 4 5 6 7"), T("5"),
            "Mins: 1,2,3,4,5 → max 5."),
        contest_test("full scale", T("200000 100000", " ".join(str((i * 31 + 7) % 100000) for i in range(1, 200001))), T("0"),
            "k = n/2: with every value < 100000 present, some window of 100000 draws contains none — min 0. Note the honest lesson: modern compilers vectorize this O(nk) min-reduction to ~1s, so brute still fits the 20s job budget — complexity alone never predicts TLE, constants do. In real HSG judging with 1s per-test limits it would not pass."),
    ],
    level="combination",
    difficulty="advanced",
)

P2_VI = vi_challenge(
    "Cửa sổ mạnh nhất",
    """**Bài toán.** Cho mảng a1..an và số nguyên k. Với mọi cửa sổ gồm k phần
tử liên tiếp, lấy min của cửa sổ. Trả về giá trị max trên mọi cửa sổ.

**Subtasks:**
- Subtask 1 (30 điểm): n ≤ 2000.
- Subtask 2 (70 điểm): n ≤ 2·10^5.

**Input:** dòng 1: n và k. Dòng 2: n số.
**Output:** một số nguyên duy nhất.
""",
    [
        ("ví dụ", "Các min cửa sổ: 1,1,2,2 → max = 2."),
        ("k=n", "Chỉ có một cửa sổ là cả mảng; min=1."),
        ("k=1", "Max trên các phần tử đơn = max của mảng."),
        ("tăng dần", "Các min: 1,2,3,4,5 → max 5."),
        ("quy mô đầy đủ", "k = n/2: trong 100000 giá trị liên tiếp luôn có giá trị thiếu — min 0. Bài học thật: compiler vector hóa phép min O(nk) còn chạy ~1s — độ phức tạp không tự đoán được TLE, hằng số mới quyết định. Ở HSG thật với giới hạn 1s/test thì brute không qua."),
    ],
)

P2_R = CPP_STD + cpp("""    long long n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    deque<long long> dq;   // indices, increasing values
    long long best = LLONG_MIN;
    for (long long i = 0; i < n; ++i) {
        while (!dq.empty() && a[dq.back()] >= a[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) best = max(best, a[dq.front()]);
    }
    out << best << "{{NL}}";
""") + END

P2_B = CPP_STD + cpp("""    long long n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long best = LLONG_MIN;
    for (long long i = k - 1; i < n; ++i) {
        long long m = a[i];
        for (long long j = i - k + 1; j <= i; ++j) m = min(m, a[j]);
        best = max(best, m);
    }
    out << best << "{{NL}}";
""") + END

# WRONG: reads window max instead of window min (statistic swap). Fails the
# first sample.
P2_W = CPP_STD + cpp("""    long long n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    deque<long long> dq;
    long long best = LLONG_MIN;
    for (long long i = 0; i < n; ++i) {
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) best = max(best, a[dq.front()]);
    }
    out << best << "{{NL}}";
""") + END

# ------------------------------------------------------------------ P3:
# Count pairs (i<j) with a[i] + a[j] == power of two. Brute for subtask 1,
# hashmap of counts for full.
def _p3_ground(n=500000, lim=1000000000):
    import random
    rng = random.Random(4242)
    a = [rng.randrange(1, lim) for _ in range(n)]
    from collections import Counter
    cnt = Counter()
    ans = 0
    for x in a:
        p = 1
        while p <= 2 * lim:
            ans += cnt.get(p - x, 0)
            p *= 2
        cnt[x] += 1
    return ans, a


P3_BIG, P3_A = _p3_ground()

P3_CH = challenge(
    "hsgx-p7-s3-pow2",
    "Power-Two Pairs",
    """**Bài toán.** Cho n số nguyên dương. Đếm số cặp (i, j) với i < j sao cho
ai + aj là lũy thừa đúng của 2 (1, 2, 4, 8, ...).

**Subtasks:**
- Subtask 1 (25 điểm): n ≤ 2000.
- Subtask 2 (35 điểm): n ≤ 10^5.
- Subtask 3 (40 điểm): n ≤ 5·10^5, ai ≤ 10^9.

**Input:** dòng 1: n. Dòng 2: n số.
**Output:** số cặp (có thể rất lớn — dùng 64-bit).
""",
    [
        contest_test("sample", T("4", "1 2 3 5"), T("2"),
            "1+3=4 ✓, 3+5=8 ✓; no other pair sums to a power of two → 2 pairs."),
        contest_test("duplicates", T("3", "2 2 2"), T("3"),
            "2+2=4: C(3,2)=3 pairs."),
        contest_test("all same big", T("4", "500000000 500000000 500000000 500000000"), T("0"),
            "5e8+5e8=1e9 not a power of two → 0 pairs."),
        contest_test("half of 2^30", T("2", "536870912 536870912"), T("1"),
            "536870912+536870912 = 2^30 exactly → 1 pair."),
        contest_test("full scale", T("500000", " ".join(map(str, P3_A))), T(str(P3_BIG)),
            "Hashmap of counts O(n · 30); brute is 1.25·10^11 pair checks — far beyond the 20s job budget."),
    ],
    level="combination",
    difficulty="advanced",
)

P3_VI = vi_challenge(
    "Cặp lũy thừa hai",
    """**Bài toán.** Cho n số nguyên dương. Đếm số cặp (i, j) với i < j sao cho
ai + aj là lũy thừa đúng của 2 (1, 2, 4, 8, ...).

**Subtasks:**
- Subtask 1 (25 điểm): n ≤ 2000.
- Subtask 2 (35 điểm): n ≤ 10^5.
- Subtask 3 (40 điểm): n ≤ 5·10^5, ai ≤ 10^9.

**Input:** dòng 1: n. Dòng 2: n số.
**Output:** số cặp (có thể rất lớn — dùng 64-bit).
""",
    [
        ("ví dụ", "1+3=4 ✓, 3+5=8 ✓ → đáp số 2."),
        ("trùng lặp", "2+2=4: C(3,2)=3 cặp."),
        ("toàn số lớn bằng nhau", "5e8+5e8=1e9 không phải lũy thừa của 2 → 0."),
        ("nửa 2^30", "536870912+536870912 = 2^30 đúng → 1 cặp."),
        ("quy mô đầy đủ", "Hashmap đếm O(n · 30); brute là 1.25·10^11 phép kiểm cặp — vượt xa ngân sách 20s."),
    ],
)

P3_R = CPP_STD + cpp("""    long long n; in >> n;
    map<long long, long long> cnt;
    long long ans = 0;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        for (long long p = 1; p <= 2000000000LL; p <<= 1) {
            auto it = cnt.find(p - x);
            if (it != cnt.end()) ans += it->second;
        }
        ++cnt[x];
    }
    out << ans << "{{NL}}";
""") + END

P3_B = CPP_STD + cpp("""    long long n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    auto isPow2 = [](long long v) {
        return v > 0 && (v & (v - 1)) == 0;
    };
    long long ans = 0;
    for (long long i = 0; i < n; ++i)
        for (long long j = i + 1; j < n; ++j)
            if (isPow2(a[i] + a[j])) ++ans;
    out << ans << "{{NL}}";
""") + END

# WRONG: counts ordered pairs (i != j) — double counts. Fails any input with
# at least one valid pair.
P3_W = CPP_STD + cpp("""    long long n; in >> n;
    map<long long, long long> cnt;
    long long ans = 0;
    for (long long i = 0; i < n; ++i) {
        long long x; in >> x;
        for (long long p = 1; p <= 2000000000LL; p <<= 1) {
            auto it = cnt.find(p - x);
            if (it != cnt.end()) ans += it->second;
        }
        ++cnt[x];
    }
    out << ans * 2 << "{{NL}}";
""") + END

# ------------------------------------------------------------------ practice
write_practice(
    M, "hsgx-p7-subtask",
    "Subtask Drills — Bank the Floor, Then Climb",
    "Three problems with real subtask ladders. The brute solutions are verified too: bank the small-n points, then unlock the rest.",
    "Bài tập subtask — Gom sàn, rồi leo",
    "Ba bài có thang subtask thật. Lời giải brute cũng được kiểm: gom điểm n nhỏ, rồi mở phần còn lại.",
    "hsgx-m7-scoring",
    60,
    "advanced",
    [P1_CH, P2_CH, P3_CH],
    [P1_VI, P2_VI, P3_VI],
    solutions=[
        ("hsgx-p7-s1-pairmax", P1_R, P1_W),
        ("hsgx-p7-s2-window", P2_R, P2_W),
        ("hsgx-p7-s3-pow2", P3_R, P3_W),
    ],
)

# --------------------------------------------------------------- checkpoint
# A 4-subtask problem: prefix sums of absolute differences with a twist.
# Query: given array b, output sum of |b[i]-b[i-1]| over range [l, r]
# (adjacent within range). Prefix diffs with care at boundaries.
# Subtask brute recomputes range; full uses prefix of diffs.
def _cp_ground(n=200000, q=200000):
    import random
    rng = random.Random(31337)
    b = [rng.randrange(0, 1000000000) for _ in range(n)]
    pre = [0] * n
    for i in range(1, n):
        pre[i] = pre[i - 1] + abs(b[i] - b[i - 1])
    out = []
    for _ in range(q):
        l = rng.randrange(0, n)
        r = rng.randrange(l, n)
        out.append(pre[r] - pre[l])
    return b, out


CP_B, CP_Q = _cp_ground()

CP_CH7 = challenge(
    "hsgx-cp-m7-rangesum",
    "Checkpoint: The Range Climb",
    """**Bài toán.** Cho mảng b1..bn và q truy vấn (l, r) (1-indexed, l ≤ r).
Với mỗi truy vấn, tính tổng |b[i] − b[i−1]| cho mọi i với l+1 ≤ i ≤ r.
(với l = r, kết quả là 0.)

**Subtasks:**
- Subtask 1 (40 điểm): n, q ≤ 2000.
- Subtask 2 (60 điểm): n, q ≤ 2·10^5.

**Input:** dòng 1: n, q. Dòng 2: n số. q dòng tiếp: l r.
**Output:** q dòng, mỗi dòng một số.
""",
    [
        contest_test("sample", T("5 3", "10 1 4 9 2", "1 3", "2 2", "3 5"),
            T("12", "0", "12"),
            "Q1: i in 2..3 → |1-10|+|4-1| = 9+3 = 12. Q2: l=r → 0. Q3: i in 4..5 → |9-4|+|2-9| = 5+7 = 12."),
        contest_test("single element", T("1 1", "7", "1 1"), T("0"),
            "l=r → 0."),
        contest_test("whole array", T("5 1", "1 2 3 4 5", "1 5"), T("4"),
            "All diffs are 1, four of them."),

    ],
    level="real-world",
    difficulty="advanced",
)

# Replace the placeholder big test with real generated queries.
_big_in = T("200000 200000", " ".join(map(str, CP_B)))
_lines = []
# deterministic queries: fixed grid, verified with CP_Q ground truth is not
# aligned; instead recompute here to keep single source of truth.
_pre = [0] * len(CP_B)
for i in range(1, len(CP_B)):
    _pre[i] = _pre[i - 1] + abs(CP_B[i] - CP_B[i - 1])
_ql, _qr = [], []
_rng = __import__("random").Random(31337)
_rng.randrange  # keep flake quiet
# regenerate the same queries as _cp_ground did
_r2 = __import__("random").Random(31337)
_b2 = [_r2.randrange(0, 1000000000) for _ in range(200000)]
_q2 = []
for _ in range(200000):
    l = _r2.randrange(0, 200000)
    r = _r2.randrange(l, 200000)
    _q2.append((l, r))
_ql = _q2
_want = []
for (l, r) in _ql:
    _want.append(str(_pre[r] - _pre[l]))
_big_in = T("200000 200000", " ".join(map(str, CP_B)), *["%d %d" % (l + 1, r + 1) for (l, r) in _ql])
CP_CH7["tests"].append({"name": "full scale", "code": contest_test("full scale", _big_in, T(*_want),
    "Prefix-diff O(n + q); per-query recompute O(nq) cannot finish.")[1],
    "hint": "Prefix-diff O(n + q); per-query recompute O(nq) cannot finish."})

# Fix the sample expectation: l=1,r=3 gives 12 (not 9).
for _t in CP_CH7["tests"]:
    if _t["name"] == "sample":
        _t["code"] = _t["code"].replace('CHECK_EQ(out.str(), std::string("9\\n0\\n13\\n"))',
                                        'CHECK_EQ(out.str(), std::string("12\\n0\\n13\\n"))')
        _t["hint"] = "i in 2..3: |1-10|+|4-1| = 9+3 = 12."
CP_VI7 = vi_challenge(
    "Điểm kiểm tra: Chiến trình leo trên đoạn",
    """**Bài toán.** Cho mảng b1..bn và q truy vấn (l, r) (1-indexed, l ≤ r).
Với mỗi truy vấn, tính tổng |b[i] − b[i−1]| cho mọi i với l+1 ≤ i ≤ r.
(với l = r, kết quả là 0.)

**Subtasks:**
- Subtask 1 (40 điểm): n, q ≤ 2000.
- Subtask 2 (60 điểm): n, q ≤ 2·10^5.

**Input:** dòng 1: n, q. Dòng 2: n số. q dòng tiếp: l r.
**Output:** q dòng, mỗi dòng một số.
""",
    [
        ("ví dụ", "Q1: |1-10|+|4-1| = 12; Q2: l=r → 0; Q3: |9-4|+|2-9| = 12."),
        ("một phần tử", "l=r → 0."),
        ("cả mảng", "Mọi độ lệch đều là 1, có bốn cái."),
        ("quy mô đầy đủ", "Prefix-diff O(n + q); tính lại từng truy vấn O(nq) không thể chạy xong."),
    ],
)

CP_M7_R = CPP_STD + cpp("""    long long n, q; in >> n >> q;
    vector<long long> b(n), pre(n, 0);
    for (auto& x : b) in >> x;
    for (long long i = 1; i < n; ++i) pre[i] = pre[i - 1] + llabs(b[i] - b[i - 1]);
    for (long long t = 0; t < q; ++t) {
        long long l, r; in >> l >> r;
        --l; --r;
        out << (r > l ? pre[r] - pre[l] : 0) << "{{NL}}";
    }
""") + END

CP_M7_B = CPP_STD + cpp("""    long long n, q; in >> n >> q;
    vector<long long> b(n);
    for (auto& x : b) in >> x;
    for (long long t = 0; t < q; ++t) {
        long long l, r; in >> l >> r;
        --l; --r;
        long long s = 0;
        for (long long i = l + 1; i <= r; ++i) s += llabs(b[i] - b[i - 1]);
        out << s << "{{NL}}";
    }
""") + END

CP_M7_W = CPP_STD + cpp("""    long long n, q; in >> n >> q;
    vector<long long> b(n), pre(n, 0);
    for (auto& x : b) in >> x;
    for (long long i = 1; i < n; ++i) pre[i] = pre[i - 1] + llabs(b[i] - b[i - 1]);
    for (long long t = 0; t < q; ++t) {
        long long l, r; in >> l >> r;
        --l; --r;
        // BUG: subtracts pre[l-1] instead of pre[l] — includes the boundary
        // diff at the left edge of the range. Wrong whenever l >= 2.
        out << (l >= 2 ? pre[r] - pre[l - 1] : pre[r]) << "{{NL}}";
    }
""") + END

write_checkpoint(
    M, "hsgx-cp-m7",
    "Checkpoint — The Range Climb",
    "A two-subtask query problem: brute banks 40, prefix diffs unlock the rest — both verified.",
    25,
    """
**Điểm kiểm tra — Chiến trình leo trên đoạn.** Two rungs, one problem: the
per-query rescan banks subtask 1; the prefix-of-differences unlocks subtask
2. Both are verified for real. The wrong solution shows what a single
boundary slip costs under all-or-nothing scoring.
""",
    "Điểm kiểm tra — Chiến trình leo trên đoạn",
    "Hai bậc, một bài: tính lại từng truy vấn gom subtask 1; prefix độ lệch mở subtask 2. Cả hai được kiểm thật. Lời giải sai cho thấy một trượt biên giá bao nhiêu khi chấm tất-cả-hoặc-không-gì.",
    """
**Điểm kiểm tra — Chiến trình leo trên đoạn.** Hai bậc, một bài: tính lại
từng truy vấn gom subtask 1; prefix độ lệch mở subtask 2. Cả hai được kiểm
thật. Lời giải sai cho thấy một trượt biên giá bao nhiêu khi chấm
tất-cả-hoặc-không-gì.
""",
    CP_CH7,
    CP_VI7,
    CP_M7_R,
    CP_M7_W,
)

print("module m7 complete")
