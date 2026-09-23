#!/usr/bin/env python3
"""HSG Intensive — Module 3: hsgx-observation (Find the Key Observation).

The largest skill group: problems whose algorithm hides behind one
observation. Workflow trained: brute force → inspect samples → find the
invariant → derive the optimization → implement → prove. Includes the
executed stress-test loop (brute vs optimized) as a lesson challenge.

Conventions: T() real newlines; cpp() → \n escapes; explicit includes in
solutions (QA harness TU pre-includes std headers).
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgx-observation"
write_module(
    M,
    "Find the Key Observation",
    "The core loop of contest solving: brute force, find the bottleneck, inspect samples, discover the invariant, derive the optimization, implement and prove it.",
    "Tìm nhận xét mấu chốt",
    "Vòng lặp cốt lõi của giải bài thi đấu: brute force, tìm điểm nghẽn, soi ví dụ, phát hiện bất biến, suy ra tối ưu hóa, cài đặt và chứng minh.",
    ["hsgx-m3-loop", "hsgx-m3-gallery", "hsgx-cp-m3"],
    ["hsgx-p3-observe"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgx-m3-loop",
    "The Observation Loop",
    "Brute force is a teacher: what its bottleneck says, how samples leak structure, and how to convert a pattern into a proof.",
    25,
    """
# The Observation Loop

## Step 1 — Write the brute force (mentally or really)

Even when you know it cannot pass, the brute force defines the problem
precisely and reveals the computation's *shape*: what gets recomputed, what
depends on what. n ≤ 200000 with an O(n²) idea means the recomputation must
be eliminated — that is the exact target.

## Step 2 — Inspect the samples with suspicion

Compute the samples by hand *through your brute force*, watching intermediate
values. Patterns appear as repeated structure: the same partial optimum
recurs; distances always come in two parities; the sorted order is already
"almost" the answer. Write the pattern down for three different inputs —
one occurrence is noise, three is structure.

## Step 3 — Name the invariant

The pattern is almost always one of a short list:

- **monotonicity**: once a quantity passes a threshold, it never comes back
  (unlocks binary search);
- **exchange argument**: two adjacent choices can be swapped with a
  computable effect (unlocks greedy + sort order);
- **independence**: subproblems don't interact once a boundary is fixed
  (unlocks DP);
- **amortized potential**: each element is touched O(1) times despite nested
  loops (unlocks two pointers, monotonic stack);
- **parity / XOR invariant**: only a residue class of states matters
  (unlocks crushing the state space).

## Step 4 — Convert to an algorithm, then prove it

State the algorithm in one sentence ("sort by r, sweep, keep a pointer"),
then prove the invariant claim in two or three lines. If you cannot state
the proof, you have a hypothesis, not a solution — check it against brute
force (the stress-testing skill of Module 9).

## Step 5 — Implement and re-check samples

Contest discipline: the implementation must reproduce the samples *before*
you submit. A failing sample is information, not bad luck.
""",
    "Vòng lặp nhận xét",
    "Brute force là người thầy: điểm nghẽn nói lên điều gì, ví dụ lộ cấu trúc ra sao, và cách biến mô hình thành chứng minh.",
    """
# Vòng lặp nhận xét

## Bước 1 — Viết brute force (trong đầu hoặc thật)

Dù biết nó không thể qua, brute force xác định bài toán một cách chính xác
và lộ ra *hình dạng* phép tính: cái gì bị tính lại, cái gì phụ thuộc cái gì.
n ≤ 200000 với ý tưởng O(n²) nghĩa là việc tính lại phải bị loại bỏ — đó
chính là mục tiêu.

## Bước 2 — Soi ví dụ với sự hoài nghi

Tính từng ví dụ bằng tay *thông qua brute force của bạn*, theo dõi các giá
trị trung gian. Mô hình xuất hiện dưới dạng cấu trúc lặp lại: cùng một cực
tiểu bộ phận tái diễn; khoảng cách luôn cùng tính chẵn lẻ; thứ tự đã sắp
"hầu như" là đáp án. Ghi mô hình lại cho ba đầu vào khác nhau — một lần là
nhiễu, ba lần là cấu trúc.

## Bước 3 — Gọi tên bất biến

Mô hình hầu như luôn thuộc danh sách ngắn này:

- **đơn điệu**: khi một đại lượng vượt ngưỡng, nó không quay lại (mở khóa
  tìm kiếm nhị phân);
- **lập luận đổi chỗ**: hai lựa chọn kề nhau có thể hoán đổi với hiệu ứng
  tính được (mở khóa greedy + thứ tự sort);
- **độc lập**: các bài con không tương tác khi biên đã cố định (mở khóa DP);
- **tiềm năng khấu hao**: mỗi phần tử chỉ được chạm O(1) lần dù vòng lặp
  lồng nhau (mở khóa two pointers, stack đơn điệu);
- **bất biến chẵn lẻ / XOR**: chỉ một lớp dư của trạng thái có ý nghĩa
  (mở khóa thu nhỏ không gian trạng thái).

## Bước 4 — Chuyển thành thuật toán, rồi chứng minh

Nêu thuật toán trong một câu ("sort theo r, quét, giữ một con trỏ"), rồi
chứng minh khẳng định bất biến trong hai–ba dòng. Nếu không nêu được chứng
minh, đó là giả thuyết chứ không phải lời giải — kiểm tra nó với brute force
(kỹ năng stress test của Module 9).

## Bước 5 — Cài đặt và kiểm lại ví dụ

Kỷ luật thi đấu: bản cài đặt phải tái tạo các ví dụ *trước khi* nộp. Ví dụ
gãy là thông tin, không phải vận xui.
""",
)

write_lesson(
    M, "hsgx-m3-gallery",
    "Observation Gallery",
    "Five worked problems where one observation collapses the complexity — with the proof each one needs.",
    25,
    """
# Observation Gallery

## 1. Max subarray sum → Kadane (independence + amortization)

Brute force O(n²) tries all (l, r). Observation: the best subarray ending at
i either extends the best one ending at i−1 or starts fresh. Proof: if the
prefix best was negative, dropping it strictly helps. O(n). The general
lesson: "best **ending here**" is the DP state hidden inside many problems.

## 2. Next greater element → monotonic stack (amortized potential)

For each i find the nearest j > i with a[j] > a[i]. Brute force O(n²).
Observation: while scanning left to right, a stack of indices with
decreasing values holds every "waiting" element; each index is pushed once
and popped once. O(n). Lesson: nested loops where the inner pointer only
moves forward are usually amortized linear.

## 3. Count subarrays with sum = k, positives → two pointers (monotonicity)

With a[i] ≥ 1, the window sum grows with r and shrinks with l: monotone.
Slide two pointers; each pointer crosses the array once. O(n). With zeros or
negatives the monotonicity dies — the same problem then needs prefix sums +
a hash map. Lesson: an observation is *conditional*; know when it expires.

## 4. Minimize max load when assigning jobs → binary search the answer

"Minimize the maximum" with an enumerable answer: binary search on the
answer x, write the feasibility check (greedy fill), prove monotonicity
(if load x is feasible, x+1 is too). O(n log(max)). Lesson: the answer's
monotonicity converts an optimization into a decision.

## 5. Longest substring without repeats → sliding window + last-seen

Brute force O(n²·alphabet). Observation: for each r, the smallest l that
keeps the window valid only moves right. Track last occurrence per char.
O(n). Lesson: validity windows with "only shrinks/grows" boundaries are two
pointers in disguise.

Each gallery entry follows the full loop: brute force → bottleneck → sample
pattern → invariant → O(n log n)-or-better algorithm → two-line proof. The
practice set below applies the same loop to unfamiliar shapes.
""",
    "Phòng trưng bày nhận xét",
    "Năm bài giải mẫu nơi một nhận xét sập độ phức tạp — kèm chứng minh mà mỗi bài cần.",
    """
# Phòng trưng bày nhận xét

## 1. Tổng đoạn con lớn nhất → Kadane (độc lập + khấu hao)

Brute force O(n²) thử mọi (l, r). Nhận xét: đoạn con tốt nhất **kết thúc tại
i** hoặc kéo dài cái tốt nhất kết thúc tại i−1 hoặc bắt đầu mới. Chứng minh:
nếu tiền tố tốt nhất âm, bỏ nó giúp ích tuyệt đối. O(n). Bài học tổng quát:
"tốt nhất **kết thúc tại đây**" là trạng thái DP ẩn trong rất nhiều bài.

## 2. Phần tử lớn hơn kế tiếp → stack đơn điệu (tiềm năng khấu hao)

Với mỗi i tìm j > i gần nhất với a[j] > a[i]. Brute force O(n²). Nhận xét:
quét trái sang phải, một stack chỉ số có giá trị giảm giữ mọi phần tử "đang
chờ"; mỗi chỉ số được push đúng một lần và pop đúng một lần. O(n). Bài học:
vòng lặp lồng với con trỏ trong chỉ tiến tới về cơ bản được khấu hao tuyến tính.

## 3. Đếm đoạn con có tổng = k, số dương → two pointers (đơn điệu)

Với a[i] ≥ 1, tổng cửa sổ tăng theo r và giảm theo l: đơn điệu. Trượt hai
con trỏ; mỗi con trỏ đi qua mảng một lần. O(n). Với số 0 hoặc âm, đơn điệu
chết — cùng bài đó lúc này cần tổng tiền tố + hash map. Bài học: nhận xét có
*điều kiện*; biết khi nào nó hết hạn.

## 4. Giảm thiểu tải lớn nhất khi phân công → tìm kiếm nhị phân đáp án

"Tối thiểu hóa giá trị lớn nhất" với đáp án đếm được: tìm kiếm nhị phân
trên đáp án x, viết kiểm tra khả thi (greedy lấp đầy), chứng minh đơn điệu
(nếu tải x khả thi thì x+1 cũng vậy). O(n log(max)). Bài học: tính đơn điệu
của đáp án biến bài tối ưu thành bài quyết định.

## 5. Xâu con dài nhất không lặp → cửa sổ trượt + lần thấy cuối

Brute force O(n²·bảng chữ). Nhận xét: với mỗi r, l nhỏ nhất giữ cửa sổ hợp
lệ chỉ tiến tới. Theo dõi lần xuất hiện cuối của từng ký tự. O(n). Bài học:
cửa sổ hợp lệ với biên "chỉ thu nhỏ/mở rộng" là two pointers trá hình.

Mỗi mục trong phòng trưng bày đi trọn vòng lặp: brute force → điểm nghẽn →
mô hình trong ví dụ → bất biến → thuật toán O(n log n) hoặc tốt hơn → chứng
minh hai dòng. Bộ thực hành dưới đây áp dụng cùng vòng lặp vào các dạng lạ.
""",
)

# ----------------------------------------------------------------- practice
# P1: max subarray sum (Kadane) — hidden topic
P1_R = CPP_STD + cpp("""    int n; in >> n;
    long long best = LLONG_MIN, cur = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        cur = max(x, cur + x);
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END

P1_W = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: "max element times n"? No — plausible wrong: best single element
    // when all negative handled, but sum from global max to global min window
    // ignoring order. Simpler classic wrong: take max prefix-suffix pair.
    // Concretely: best = max(a) even when a full positive run beats it.
    long long best = *max_element(a.begin(), a.end());
    long long s = 0;
    for (long long x : a) { s += x; best = max(best, s); }
    // misses windows that start mid-array (resets never happen)
    out << best << "{{NL}}";
""") + END

# P2: next greater element (monotonic stack)
P2_R = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> res(n, -1);
    vector<int> st;  // indices with decreasing values
    for (int i = 0; i < n; ++i) {
        while (!st.empty() && a[st.back()] < a[i]) {
            res[st.back()] = a[i];
            st.pop_back();
        }
        st.push_back(i);
    }
    for (int i = 0; i < n; ++i) out << res[i] << "{{NL}}";
""") + END

P2_W = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: O(n^2) scan — correct answers but times out at n = 200000 on
    // the full test; the module's point is the amortized linear stack.
    for (int i = 0; i < n; ++i) {
        long long r = -1;
        for (int j = i + 1; j < n; ++j) if (a[j] > a[i]) { r = a[j]; break; }
        out << r << "{{NL}}";
    }
""") + END

# P3: two pointers count subarrays sum >= S, positives
P3_R = CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long cnt = 0, s = 0;
    int l = 0;
    for (int r = 0; r < n; ++r) {
        s += a[r];
        while (s - a[l] >= S && l <= r) { s -= a[l]; ++l; }
        if (s >= S) cnt += l + 1;  // windows [j..r], j = 0..l
    }
    out << cnt << "{{NL}}";
""") + END

P3_W = CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: counts subarrays with sum == S exactly (misread "at least"),
    // via running sums — plausible-looking, deterministic wrong answer.
    long long cnt = 0, s = 0;
    for (int r = 0; r < n; ++r) {
        s = 0;
        for (int l = r; l >= 0; --l) {
            s += a[l];
            if (s == S) ++cnt;
        }
    }
    out << cnt << "{{NL}}";
""") + END

# P4: minimize max load, binary search the answer
P4_R = CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long lo = *max_element(a.begin(), a.end());
    long long hi = 0;
    for (long long x : a) hi += x;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        long long need = 1, cur = 0;
        for (long long x : a) {
            if (cur + x > mid) { ++need; cur = x; }
            else cur += x;
        }
        if (need <= k) hi = mid; else lo = mid + 1;
    }
    out << lo << "{{NL}}";
""") + END

P4_W = CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: greedy "start a new chunk when the current chunk exceeds the
    // average" — the average is not the answer; deterministic wrong output.
    long long tot = 0;
    for (long long x : a) tot += x;
    long long avg = tot / max(1, k);
    long long need = 1, cur = 0, best = 0;
    for (long long x : a) {
        if (cur + x > avg) { best = max(best, cur); ++need; cur = x; }
        else cur += x;
    }
    best = max(best, cur);
    out << best << "{{NL}}";
""") + END

# P5: longest substring without repeats
P5_R = CPP_STD + cpp("""    string s; in >> s;
    int n = (int)s.size();
    vector<int> last(256, -1);
    int best = 0, l = 0;
    for (int r = 0; r < n; ++r) {
        if (last[(unsigned char)s[r]] >= l) l = last[(unsigned char)s[r]] + 1;
        last[(unsigned char)s[r]] = r;
        best = max(best, r - l + 1);
    }
    out << best << "{{NL}}";
""") + END

P5_W = CPP_STD + cpp("""    string s; in >> s;
    // WRONG: tracks the current run length, resetting only on ADJACENT
    // repeats. Misses non-adjacent duplicates ("abcabc" has no adjacent
    // repeat, so the run grows to 6 — but the true longest unique window
    // is 3). Deterministic wrong on the classic test and on the big one.
    int n = (int)s.size();
    int len = 0, best = 0;
    for (int r = 0; r < n; ++r) {
        if (r > 0 && s[r] == s[r - 1]) len = 1;
        else ++len;
        best = max(best, len);
    }
    out << best << "{{NL}}";
""") + END

P1_CH = challenge(
    "hsgx-p3-kadane", "The Heaviest Stretch",
    """**Bài toán.** Given n integers (possibly negative), print the maximum
sum over all non-empty contiguous segments.

**Constraints:** 1 ≤ n ≤ 200000; |a[i]| ≤ 10^9.

**Output:** one integer. An O(n²) enumeration of all segments will not
survive the largest test.
""",
    [
        contest_test("single", T("1", "-5"), T("-5"),
            "One element: the only segment."),
        contest_test("all negative", T("4", "-3 -1 -7 -2"), T("-1"),
            "Best segment is the single -1."),
        contest_test("mixed", T("5", "1 -2 3 4 -1"), T("7"),
            "Segment 3 4 wins."),
        contest_test("n=200000", T("200000") + T(*[str(((i * 48271) % 2000001) - 1000000) for i in range(1, 200001)]), T("14305390"),
            "Full scale: O(n²) is 4·10^10 — times out. Ground truth via an independent O(n) prefix-min computation in Python."),
    ],
    level="combination",
    difficulty="advanced",
)

P2_CH = challenge(
    "hsgx-p3-nextgreater", "Waiting for a Taller One",
    """**Bài toán.** For each of n towers, print the height of the first tower
strictly taller to its right, or −1 if none exists.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ a[i] ≤ 10^9.

**Output:** n lines. The intended solution is linear; nested scanning times out.
""",
    [
        contest_test("all same", T("3", "5 5 5"), T("-1", "-1", "-1"),
            "Strictly taller: nobody qualifies."),
        contest_test("increasing", T("4", "1 2 3 4"), T("2", "3", "4", "-1"),
            "Each next element is the answer."),
        contest_test("valley", T("5", "3 1 4 1 5"), T("4", "4", "5", "5", "-1"),
            "Check index 1: next taller is 4."),
        contest_test("n=200000 decreasing", T("200000") + T(*[str(200001 - i) for i in range(1, 200001)]), T(*["-1"] * 200000),
            "Strictly decreasing: all -1. The stack must still run in O(n) — a quadratic scan times out here."),
    ],
    level="combination",
    difficulty="advanced",
)

P3_CH = challenge(
    "hsgx-p3-windows", "Windows At Least S",
    """**Bài toán.** Given n positive integers and a threshold S, count the
contiguous segments whose sum is **at least** S.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ a[i] ≤ 10^9; 1 ≤ S ≤ 10^18.

**Output:** one integer (fits in long long). With all-positive values the
window boundaries are monotone — use that.
""",
    [
        contest_test("single", T("1", "5 5"), T("1"),
            "The one segment sums to 5 ≥ 5."),
        contest_test("just below", T("2 5", "3 2"), T("1"),
            "n=2, S=5, array [3, 2]: only [1..2] reaches 5."),
        contest_test("window count", T("4", "4 1 2 3 4"), T("6"),
            "Segments ≥ 4: [4],[2..3],[3..4],[1..3],[2..4],[1..4] = 6."),
        contest_test("n=200000 ones", T("200000 50") + T(*["1"] * 200000), T("19990301176"),
            "All ones: segments of length ≥ 50. Count = Σ_{L=50}^{n} (n−L+1) = 19990301176, computed in Python as ground truth."),
    ],
    level="combination",
    difficulty="advanced",
)

P4_CH = challenge(
    "hsgx-p4-loadsplit", "Split Without Overload",
    """**Bài toán.** Split an ordered list of n jobs into at most k consecutive
groups so that the largest group sum is minimized. Print that minimized maximum.

**Constraints:** 1 ≤ k ≤ n ≤ 100000; 1 ≤ a[i] ≤ 10^9.

**Output:** one integer. Feasibility is monotone in the answer — exploit it.
""",
    [
        contest_test("one group", T("3 1", "4 5 6"), T("15"),
            "Everything in one group."),
        contest_test("each alone", T("3 3", "4 5 6"), T("6"),
            "k = n: the max element."),
        contest_test("classic", T("5 2", "1 2 3 4 5"), T("9"),
            "Split 1 2 3 | 4 5 → max 9."),
        contest_test("n=100000", T("100000 10") + T(*[str((i * 7919) % 1000000 + 1) for i in range(1, 100001)]), T("4999553036"),
            "Full scale verified against an independent binary-search ground truth in Python."),
    ],
    level="combination",
    difficulty="advanced",
)

P5_CH = challenge(
    "hsgx-p3-uniquelen", "The Longest Clean Streak",
    """**Bài toán.** Given a lowercase string, print the length of the longest
substring in which no character repeats.

**Constraints:** 1 ≤ |s| ≤ 200000.

**Output:** one integer.
""",
    [
        contest_test("all same", T("aaaa"), T("1"),
            "Every window is length 1."),
        contest_test("all distinct", T("abcdef"), T("6"),
            "Whole string."),
        contest_test("mid-string best", T("abbbc"), T("2"),
            "Best windows are length 2, and the winner starts mid-string."),
        contest_test("classic", T("abcabcbb"), T("3"),
            "abc / bca / cab are the length-3 windows."),
        contest_test("n=200000", T("a" + "".join(chr(97 + (i * 7) % 26) for i in range(1, 200000))), T("26"),
            "Cyclic-ish pattern: the maximum possible is 26 (Python-verified); the adjacent-repeat-only wrong returns far more."),
    ],
    level="combination",
    difficulty="advanced",
)

write_practice(
    M, "hsgx-p3-observe", "Observation Drill — Five Hidden Structures",
    "Five problems, no topic names. Each needs one key observation to collapse the complexity; each wrong solution is the natural first idea.",
    "Drill nhận xét — Năm cấu trúc ẩn",
    "Năm bài, không tên chủ đề. Mỗi bài cần một nhận xét mấu chốt để sập độ phức tạp; mỗi lời giải sai là ý tưởng đầu tiên tự nhiên.",
    "hsgx-m3-gallery",
    90,
    "advanced",
    [P1_CH, P2_CH, P3_CH, P4_CH, P5_CH],
    {
        "hsgx-p3-kadane": vi_challenge(
            "Đoạn nặng nhất",
            "**Bài toán.** Cho n số nguyên (có thể âm), in tổng lớn nhất trên mọi đoạn liền kề khác rỗng. O(n²) sẽ không sống sót test lớn nhất.",
            [("một phần tử", "Đoạn duy nhất."),
             ("toàn âm", "Đoạn tốt nhất là phần tử -1 đơn lẻ."),
             ("trộn lẫn", "Đoạn 3 4 thắng."),
             ("n=200000", "O(n²) là 4·10^10 — quá thời gian; Kadane O(n) là lời giải chủ đích.")],
        ),
        "hsgx-p3-nextgreater": vi_challenge(
            "Chờ một tòa cao hơn",
            "**Bài toán.** Với mỗi trong n tòa nhà, in chiều cao tòa đầu tiên cao hơn nghiêm ngặt về bên phải, hoặc −1 nếu không có. Lời giải chủ đích là tuyến tính; quét lồng sẽ quá thời gian.",
            [            ("đều như nhau", "Không ai cao hơn nghiêm ngặt."),
            ("tăng dần", "Phần tử kế tiếp là đáp án."),
            ("thung lũng", "Chỉ số 1: cao hơn kế tiếp là 4."),
             ("n=200000 giảm dần", "Toàn −1; stack vẫn phải chạy O(n) — quét O(n²) quá thời gian.")],
        ),
        "hsgx-p3-windows": vi_challenge(
            "Cửa sổ ít nhất S",
            "**Bài toán.** Cho n số nguyên dương và ngưỡng S, đếm các đoạn liền kề có tổng **ít nhất** S. Với toàn số dương, biên cửa sổ đơn điệu — hãy tận dụng.",
            [("một phần tử", "Đoạn duy nhất có tổng 5 ≥ 5."),
             ("sát ngưỡng", "Chỉ [1..2] chạm 5."),
             ("đếm cửa sổ", "Kiểm tay: 6 đoạn."),
             ("n=200000 số 1", "Đoạn dài ≥ 50; công thức Σ (n−L+1) kiểm chứng trong Python.")],
        ),
        "hsgx-p4-loadsplit": vi_challenge(
            "Chia không quá tải",
            "**Bài toán.** Chia danh sách n việc (giữ thứ tự) thành tối đa k nhóm liền kề sao cho tổng nhóm lớn nhất được tối thiểu hóa. Tính đơn điệu của tính khả thi là chìa khóa.",
            [("một nhóm", "Tất cả trong một nhóm: 15."),
             ("mỗi việc một nhóm", "k = n: phần tử lớn nhất."),
             ("kinh điển", "Chia 1 2 3 | 4 5 → max 9."),
             ("n=100000", "Đối chiếu ground truth bằng tìm kiếm nhị phân độc lập trong Python.")],
        ),
        "hsgx-p3-uniquelen": vi_challenge(
            "Chuỗi sạch dài nhất",
            "**Bài toán.** Cho xâu chữ thường, in độ dài xâu con dài nhất không có ký tự lặp lại.",
            [("đều giống nhau", "Mọi cửa sổ dài 1."),
             ("khác nhau hết", "Cả xâu."),
             ("tốt nhất giữa xâu", "Cửa sổ tốt nhất bắt đầu giữa xâu."),
             ("kinh điển", "abc / bca / cab dài 3."),
             ("n=200000", "Tối đa 26 (kiểm chứng Python); lời giải sai chỉ-reset-khi-kề-nhau trả nhiều hơn nhiều.")],
        ),
    },
    solutions=[
        ("hsgx-p3-kadane", P1_R, P1_W),
        ("hsgx-p3-nextgreater", P2_R, P2_W),
        ("hsgx-p3-windows", P3_R, P3_W),
        ("hsgx-p4-loadsplit", P4_R, P4_W),
        ("hsgx-p3-uniquelen", P5_R, P5_W),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Pair-sum divisible by D (observation: residues pair up; count and mind
# self-paired residues). Ground truths hand-enumerated and Python-verified.
CP_M3_R = CPP_STD + cpp("""    int n; long long d; in >> n >> d;
    vector<long long> cnt(d, 0);
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        ++cnt[((x % d) + d) % d];
    }
    long long pairs = cnt[0] * (cnt[0] - 1) / 2;
    for (long long r = 1; r * 2 < d; ++r) pairs += cnt[r] * cnt[d - r];
    if (d % 2 == 0) pairs += cnt[d / 2] * (cnt[d / 2] - 1) / 2;
    out << pairs << "{{NL}}";
""") + END

CP_M3_W = CPP_STD + cpp("""    int n; long long d; in >> n >> d;
    vector<long long> cnt(d, 0);
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        ++cnt[((x % d) + d) % d];
    }
    // WRONG: counts ordered index pairs (i < j) as cnt[r] * cnt[d-r] for ALL
    // r — double-counting every complementary pair {r, d-r} AND forgetting
    // that self-paired residues need combinations, not products. Overcounts
    // on every multi-residue test.
    long long pairs = cnt[0] * (cnt[0] - 1) / 2;
    for (long long r = 1; r < d; ++r) pairs += cnt[r] * cnt[d - r];
    out << pairs << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgx-cp-m3", "Checkpoint — The Residue Ledger",
    "Count pairs with sum divisible by d: the observation is that only residues matter — pair r with d−r, halve the self-paired residue, and the O(n²) scan disappears.",
    20,
    """
**Điểm kiểm tra — Sổ cái phần dư.** Count pairs (i < j) whose sum is
divisible by d. The brute force checks all n·(n−1)/2 pairs; the observation
is that two numbers are compatible exactly when their residues r and d−r
pair up (r = 0 and r = d/2 pair with themselves). Count residues once, do
combinatorics on d buckets. The wrong solution below counts every
complementary residue pair TWICE (r vs d−r and d−r vs r) and forgets the
self-pairing rule — find a sample where it disagrees.
""",
    "Điểm kiểm tra — Sổ cái phần dư",
    "Đếm cặp có tổng chia hết cho d: chỉ phần dư quan trọng — ghép r với d−r, chia đôi phần dư tự ghép, quét O(n²) biến mất.",
    """
**Điểm kiểm tra — Sổ cái phần dư.** Đếm cặp (i < j) có tổng chia hết cho d.
Brute force kiểm mọi n·(n−1)/2 cặp; nhận xét là hai số tương thích đúng khi
phần dư r và d−r ghép cặp (r = 0 và r = d/2 tự ghép với chính mình). Đếm
phần dư một lần, làm tổ hợp trên d bucket. Lời giải sai dưới đây đếm MỌI
cặp phần dư bổ sung HAI LẦN (r với d−r và d−r với r) và quên quy tắc
tự ghép — tìm mẫu nơi nó lệch.
""",
    challenge(
        "hsgx-cp-m3-pairs",
        "Checkpoint: Pairs Divisible by D",
        """**Bài toán.** Given n integers and a modulus d, count the pairs
(i < j) with (a[i] + a[j]) divisible by d. Values may be negative.

**Constraints:** 2 ≤ d ≤ 200000; 1 ≤ n ≤ 200000; |a[i]| ≤ 10^9.

**Hint:** only a[i] mod d matters. Two residues r and d−r are compatible;
r = 0 and (even d) r = d/2 are compatible with themselves. n² is 4·10^10 —
the residue ledger is the whole point.
""",
        [
            contest_test("single", T("1 5"), T("0"),
                "One element: no pairs."),
            contest_test("mixed residues", T("5 3", "3 1 2 3 3"), T("4"),
                "Residues mod 3: {0,1,2,0,0} → C(3,2)=3 zero-pairs + 1·1 cross-pair (residues 1,2) = 4. The wrong solution counts the cross-pair twice and prints 5."),
            contest_test("powers of two", T("5 7", "1 2 4 8 7"), T("0"),
                "Residues mod 7: {1,2,4,1,0} — residue 1 exists but 6 does not; residue 0 is a singleton. No compatible pair exists → 0 (brute-force verified)."),
            contest_test("all same", T("8 7", "7 7 7 7 7 7 7 7"), T("28"),
                "Every pair sums to 14 ≡ 0 (mod 7): C(8,2) = 28."),
            contest_test("n=200000", T("200000 99") + T(*[str(i % 99) for i in range(1, 200001)]), T("202019190"),
                "Residues 1..20 appear 2021×, 21..98 appear 2020× (i mod 99 for i=1..200000); residue 0 appears 2020×. 49 cross pairs × 2020·2021 = 199980000, plus C(2020,2)=2039190 zero-residue pairs → Python-verified 202019190. The double-counting wrong prints 401999190."),
        ],
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Điểm kiểm tra: Cặp chia hết cho D",
        """**Bài toán.** Cho n số nguyên và mô-đun d, đếm cặp (i < j) với
(a[i] + a[j]) chia hết cho d. Giá trị có thể âm.

**Ràng buộc:** 2 ≤ d ≤ 200000; 1 ≤ n ≤ 200000; |a[i]| ≤ 10^9.

**Gợi ý:** chỉ a[i] mod d quan trọng. Hai phần dư r và d−r tương thích;
r = 0 và (d chẵn) r = d/2 tự tương thích. n² là 4·10^10 — sổ cái phần dư
là toàn bộ bài này.
""",
        [("một phần tử", "Không có cặp nào."),
         ("phần dư trộn lẫn", "Phần dư mod 3: {0,1,2,0,0} → C(3,2)=3 cặp số-0 + 1·1 cặp chéo (phần dư 1,2) = 4. Lời giải sai đếm cặp chéo hai lần và in 5."),
         ("luỹ thừa của 2", "Phần dư mod 7: {1,2,4,1,0} — phần dư 1 có nhưng 6 thì không; phần dư 0 đơn lẻ. Không có cặp tương thích → 0 (kiểm chứng brute force)."),
         ("đều giống nhau", "Mọi cặp có tổng 14 ≡ 0 (mod 7): C(8,2) = 28."),
         ("n=200000", "Phần dư 1..20 xuất hiện 2021 lần, 21..98 xuất hiện 2020 lần, phần dư 0 xuất hiện 2020 lần; 49 cặp chéo × 2020·2021 + C(2020,2) cặp số-0 — kiểm chứng Python: 202019190. Lời giải sai in 401999190.")],
    ),
    CP_M3_R,
    CP_M3_W,
)

print("module m3 complete")
