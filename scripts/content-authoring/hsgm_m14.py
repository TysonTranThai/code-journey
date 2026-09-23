#!/usr/bin/env python3
"""HSG Mastery — Module 14: hsgm-final (Mixed Expert Sets & Simulation).

Unidentified-topic problems: no module name, no chapter label. The student
runs the full pipeline — model, budget, observe, prove, implement, attack.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgm import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test, recognition_drill,
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


def letter(l):
    return CPP_STD + cpp('    out << "' + l + '";') + END


M = "hsgm-final"
write_module(
    M,
    "Mixed Expert Sets and Simulation",
    "Problems with no topic label: the full pipeline under time discipline. The techniques are hidden; the recognition is the exam.",
    "Bộ chuyên gia hỗn hợp và mô phỏng",
    "Các bài không nhãn chủ đề: toàn bộ quy trình dưới kỷ luật thời gian. Kỹ thuật bị giấu; nhận diện chính là kỳ thi.",
    ["hsgm-m14-pipeline", "hsgm-m14-simulate", "hsgm-cp-m14"],
    ["hsgm-p14-drills"],
)

write_lesson(
    M, "hsgm-m14-pipeline",
    "The Full Pipeline, No Labels",
    "Everything the course taught, in one pass: model → budget → observe → prove → implement → attack.",
    14,
    """
# The Full Pipeline, No Labels

This module's problems announce nothing. The pipeline runs in order, and
each stage has a time box:

1. **Model (3–5 min).** Objects, quantities, objective, constraints — on
   paper. No algorithm thought yet.
2. **Budget (2 min).** Multiply the op count of the obvious approach. The
   constraint table names the allowed complexity family.
3. **Observe (10 min).** Compute small cases; run the Big Four scan
   (invariant, parity, monotonicity, symmetry).
4. **Prove (5 min).** One exchange argument, one induction, or an honest
   "unproven hypothesis" tag — which drops the plan's rank.
5. **Implement (rest).** With the complexity family chosen and the key
   observation proven, the code is usually the fast part.
6. **Attack (before submitting).** The five-shape checklist, run against
   your own solution.

## When the pipeline stalls

Stalls happen at stage 3 most often. The escape is *reformulation*
(Module 3): count the complement, reframe the object, decompose the
condition. The second escape is the constraint table: a band you can
solve is worth real points right now.

## The goal state

You know the pipeline is internalized when you can narrate it *while*
solving, without going back to read it. That narration is what the
simulations below train.
""",
    "Toàn bộ quy trình, không nhãn",
    "Mọi thứ khóa học đã dạy, trong một lượt: mô hình → ngân sách → nhận xét → chứng minh → cài đặt → tấn công.",
    """
# Toàn bộ quy trình, không nhãn

Các bài của module này không công bố gì cả. Quy trình chạy theo thứ tự,
và mỗi chặng có một khung thời gian:

1. **Mô hình (3–5 phút).** Đối tượng, đại lượng, mục tiêu, ràng buộc —
   trên giấy. Chưa nghĩ thuật toán.
2. **Ngân sách (2 phút).** Nhân số phép toán của hướng tiếp cận hiển nhiên.
   Bảng giới hạn gọi tên họ độ phức tạp được phép.
3. **Nhận xét (10 phút).** Tính các case nhỏ; chạy quét Bốn-Họ (bất biến,
   parity, đơn điệu, đối xứng).
4. **Chứng minh (5 phút).** Một luận điểm hoán đổi, một quy nạp, hoặc gắn
   nhãn trung thực "giả-thuyết-chưa-chứng-minh" — thứ hạ thứ hạng của
   phương án.
5. **Cài đặt (phần còn lại).** Với họ độ phức tạp đã chọn và nhận xét then
   chốt đã chứng minh, code thường là phần nhanh.
6. **Tấn công (trước khi nộp).** Danh mục năm-hình-dạng, chạy ngược vào
   lời giải của chính mình.

## Khi quy trình tắc

Tắc thường xảy ra ở chặng 3. Lối thoát là *phát biểu lại* (Module 3):
đếm phần bù, đổi khung đối tượng, phân rã điều kiện. Lối thoát thứ hai là
bảng giới hạn: một dải bạn giải được đáng bao nhiêu điểm thật ngay bây giờ.

## Trạng thái đích

Bạn biết quy trình đã nhuần nhuyễn khi có thể *thuật lại nó trong lúc*
giải, không cần quay lại đọc. Việc thuật lại đó là điều các mô phỏng dưới
đây rèn luyện.
""",
)

write_lesson(
    M, "hsgm-m14-simulate",
    "Running the Simulation",
    "Two full mixed problems, timed, with a post-contest review form. The review is the lesson.",
    14,
    """
# Running the Simulation

Treat this module's problems as a mini-contest: choose your own order,
allocate ~35 minutes each, and write down your decisions as you make
them. Afterward, fill the review:

1. **What did I solve, and at what time?**
2. **Where did the pipeline stall, and at which stage?**
3. **Which observation unlocked it — and how long until I found it?**
4. **Did I prove it, or trust it?**
5. **What would I attack first on my own accepted solution?**

## Reading your own review

- Stalls at *model* → vocabulary problem: re-read Module 3's
  reformulation patterns.
- Stalls at *observe* → experiment more, theorize less: your tables were
  too small or too unstructured.
- Stalls at *implement* → the complexity family was chosen before the
  observation was proven; you rewrote the code.
- Overruns at *attack* → the checklist was skipped; the fix is
  mechanical, not intellectual.

## The meta-point

Simulations are not for verifying that you know things. They are for
exposing the *sequence* you actually run under pressure — which is
almost never the sequence you believe you run. The gap between the two
is the last skill this course can give you.
""",
    "Chạy mô phỏng",
    "Hai bài hỗn hợp trọn vẹn, có bấm giờ, với biểu đánh giá sau kỳ thi. Phần đánh giá chính là bài học.",
    """
# Chạy mô phỏng

Coi các bài của module này như một kỳ-thi-nhỏ: tự chọn thứ tự, phân bổ
~35 phút mỗi bài, và ghi lại các quyết định của bạn khi đưa ra. Sau đó,
điền đánh giá:

1. **Tôi đã giải được gì, vào lúc nào?**
2. **Quy trình tắc ở đâu, ở chặng nào?**
3. **Nhận xét nào mở khóa nó — và mất bao lâu để tìm ra?**
4. **Tôi đã chứng minh nó, hay tin nó?**
5. **Tôi sẽ tấn công điều gì đầu tiên trên lời solution đã AC của chính mình?**

## Đọc đánh giá của chính mình

- Tắc ở *mô hình* → vấn đề vốn-từ: đọc lại các mẫu phát biểu lại của
  Module 3.
- Tắc ở *nhận xét* → thực nghiệm nhiều hơn, suy đoán ít hơn: các bảng của
  bạn quá nhỏ hoặc quá thiếu cấu trúc.
- Tắc ở *cài đặt* → họ độ phức tạp được chọn trước khi nhận xét được
  chứng minh; bạn viết lại code.
- Vượt giờ ở *tấn công* → danh mục bị bỏ qua; phép sửa là cơ khí, không
  phải trí tuệ.

## Điểm siêu-nghị luận

Mô phỏng không phải để xác nhận bạn biết mọi thứ. Chúng phơi bày *chuỗi*
bạn thực sự chạy dưới áp lực — thứ hầu như không bao giờ là chuỗi bạn
tin rằng mình chạy. Khoảng cách giữa hai cái là kỹ năng cuối cùng khóa
này trao cho bạn.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p14-d1", "The Unlabeled Wall",
    "A problem gives n ≤ 100000 intervals and asks for the largest set of pairwise non-overlapping ones. The statement mentions no algorithm. First move?",
    [
        "Try DP over all subsets",
        "Model it (intervals, objective = max compatible set), note n ≤ 10^5 admits O(n log n), then hunt for the exchange-argument sort key",
        "Brute force with pruning",
        "Random restarts with different orders",
    ],
    "B",
    "The pipeline in action: model first, budget names O(n log n), the known structure (earliest-end exchange) falls out of the proof habit.",
    vi_title="Bức tường vô-đề",
    vi_scenario="Một bài cho n ≤ 100000 đoạn và hỏi tập lớn nhất các đoạn đôi-một-không-chồng. Đề không nhắc thuật toán nào. Nước đi đầu?",
    vi_options=[
        "Thử DP trên mọi tập con",
        "Mô hình hóa (các đoạn, mục tiêu = tập tương thích lớn nhất), thấy n ≤ 10^5 cho phép O(n log n), rồi săn khóa sort qua luận điểm hoán đổi",
        "Brute force với tỉa",
        "Khởi động lại ngẫu nhiên với các thứ tự khác nhau",
    ],
    vi_hint="Quy trình đúng nghĩa: mô hình trước, ngân sách gọi tên O(n log n), cấu trúc đã biết (hoán đổi kết-thúc-sớm) rơi ra từ thói quen chứng minh.",
)

D2, D2VI = recognition_drill(
    "hsgm-p14-d2", "The Time Box",
    "20 minutes in, you have modeled the problem and the budget kills your only idea. What does the pipeline prescribe?",
    [
        "Code the doomed idea anyway — working code feels productive",
        "Return to observe: compute small cases and scan the Big Four; if that stalls, recheck the constraint bands for a harvestable partial",
        "Skip to another problem permanently",
        "Read the samples harder",
    ],
    "B",
    "A killed budget is not a dead end — it is a redirect to stages 3 (observe) and 2b (partial bands). Coding a known-doomed idea spends the most expensive resource on a known loss.",
    vi_title="Khung thời gian",
    vi_scenario="20 phút trôi qua, bạn đã mô hình hóa bài toán và ngân sách giết ý tưởng duy nhất của bạn. Quy trình cho phép điều gì?",
    vi_options=[
        "Vẫn code ý tưởng tuyệt vọng — code chạy được cho cảm giác năng suất",
        "Quay lại nhận xét: tính các case nhỏ và quét Bốn-Họ; nếu vẫn tắc, soát lại các dải giới hạn để thu hoạch điểm một phần",
        "Nhảy sang bài khác vĩnh viễn",
        "Nhìn kỹ các test mẫu hơn",
    ],
    vi_hint="Ngân sách bị giết không phải là ngõ cụt — đó là một sự chuyển hướng tới chặng 3 (nhận xét) và 2b (dải điểm một phần). Code một ý tưởng biết-trước-tuyệt-vọng tiêu nguồn tài nguyên đắt nhất vào một thất bại đã biết.",
)

D3, D3VI = recognition_drill(
    "hsgm-p14-d3", "The Honest Tag",
    "You found a pattern that fits all tested cases but cannot prove it. The contest clock says 2 hours left. Rank the options.",
    [
        "Trust it fully — the pattern is strong",
        "Use it, but tag it unproven: harvest any partial bands with provable approaches first, keep the unproven path as the last submission",
        "Prove it or refuse to use it",
        "Ask a teammate",
    ],
    "B",
    "Honest tagging preserves optionality: proven partials bank points; the unproven pattern is used with its true (unknown) risk — and only when nothing provable remains.",
    vi_title="Nhãn trung thực",
    vi_scenario="Bạn tìm thấy một mẫu khớp mọi case đã thử nhưng không chứng minh được. Đồng hồ thi còn 2 giờ. Xếp hạng các lựa chọn.",
    vi_options=[
        "Tin hoàn toàn — mẫu rất mạnh",
        "Dùng nó, nhưng gắn nhãn chưa-chứng-minh: thu hoạch mọi dải điểm một phần bằng hướng tiếp cận chứng-minh-được trước, giữ đường chưa-chứng-minh làm lần nộp cuối",
        "Chứng minh hoặc từ chối dùng",
        "Hỏi đồng đội",
    ],
    vi_hint="Gắn nhãn trung thực giữ lại sự lựa chọn: các phần một-phần đã-chứng-minh gửi ngân điểm; mẫu chưa-chứng-minh được dùng với rủi ro thật (chưa biết) của nó — và chỉ khi không còn gì chứng minh được.",
)

write_practice(
    M, "hsgm-p14-drills", "Pipeline Drills",
    "Three drills: the no-label first move, the killed-budget redirect, and honest tagging of unproven patterns.",
    "Drill quy trình",
    "Ba drill: nước-đi-đầu-vô-đề, chuyển-hướng-khi-ngân-sách-chết, và gắn-nhãn-trung-thực cho mẫu chưa chứng minh.",
    "hsgm-m14-simulate", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p14-d1": D1VI, "hsgm-p14-d2": D2VI, "hsgm-p14-d3": D3VI},
    solutions=[
        ("hsgm-p14-d1", letter("B"), letter("A")),
        ("hsgm-p14-d2", letter("B"), letter("A")),
        ("hsgm-p14-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoints
# Two "simulation" problems, hidden-topic, real tests, paired Ws.
# Sim 1: smallest alphabet span — given a string of n letters over an
# alphabet of k distinct letters, find the length of the shortest substring
# containing ALL k distinct letters. W: sliding window that shrinks while
# counts stay >= 1 but forgets to move the left pointer when a letter's
# count would drop to 0... make W: expands right but resets instead of
# shrinking left (O(n) but wrong on interleavings). Simulate both.
def _gt_span(s, k):
    from collections import defaultdict
    need = k
    have = defaultdict(int)
    best = 10**9
    l = 0
    for r, ch in enumerate(s):
        if have[ch] == 0:
            need -= 1
        have[ch] += 1
        while need == 0:
            best = min(best, r - l + 1)
            have[s[l]] -= 1
            if have[s[l]] == 0:
                need += 1
            l += 1
    return best if best < 10**9 else -1


def _w_span(s, k):
    # W: for each right endpoint, expands a window from the RIGHT edge only
    # back n steps... simpler behavioral W: greedy 'scan in chunks of k' —
    # only considers windows starting at multiples of k.
    from collections import defaultdict
    best = 10**9
    for start in range(0, max(1, len(s) - 0), k):
        have = defaultdict(int)
        need = k
        for r in range(start, len(s)):
            ch = s[r]
            if have[ch] == 0:
                need -= 1
            have[ch] += 1
            if need == 0:
                best = min(best, r - start + 1)
                break
    return best if best < 10**9 else -1


_s1 = "aabcaaccb"      # k=3: shortest span "caa...": check
_k1 = 3
_g1 = _gt_span(_s1, _k1)
_w1 = _w_span(_s1, _k1)
assert _w1 != _g1, (_g1, _w1)

_s2 = "bcabacbbabcaabcccbabcaacbca"
_k2 = 3
_g2 = _gt_span(_s2, _k2)
_w2 = _w_span(_s2, _k2)

# large: n=200000 random over 3 letters
import random as _r3
_r3.seed(14)
_s3 = "".join("abc"[_r3.randrange(3)] for _ in range(200000))
_k3 = 3
_g3 = _gt_span(_s3, _k3)

CP14A = challenge(
    "hsgm-cp-m14-span",
    "Simulation I: The Complete Set",
    """**Task.** A string of n lowercase letters; the alphabet is exactly the
k distinct letters that appear (given as k). Find the length of the
shortest contiguous substring containing all k distinct letters at least
once each. Print that length, or −1 if impossible.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ k ≤ 26 (with k = number of distinct
letters in the string, so −1 cannot actually occur — decide for yourself
whether to trust that).
""",
    [
        contest_test("warmup", T("6 3", "abcbca"), T("3"), "bca (or cab) covers all 3 letters in length 3."),
        contest_test("whole string", T("4 3", "accb"), T("4"), "Both endpoints occur exactly once — every proper window loses a letter."),
    ],
    level="real-world",
    difficulty="advanced",
)
CP14A["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("warmup", T("6 3", "abcbca"), T("3"),
            "bca (or cab) covers all 3 letters in length 3."),
        contest_test("whole string", T("4 3", "accb"), T("4"),
            "Both endpoints occur exactly once — every proper window loses a letter."),
        contest_test("single letters", T("3 3", "abc"), T("3"),
            "k = n: the whole string."),
        contest_test("interleaved", T("9 3", "aabcaaccb"), T(str(_g1)),
            "Sweep-verified in Python (this input also defeats chunk-greedy scans)."),
        contest_test("full scale", T("200000 3", _s3), T(str(_g3)),
            "n = 200000 over 3 letters: the honest two-pointer sweep is O(n). Ground truth in Python."),
    )
]

CP14AVI = vi_challenge(
    "Mô phỏng I: Bộ hoàn chỉnh",
    """**Bài toán.** Một xâu n chữ cái thường; bảng chữ là đúng k chữ cái
khác nhau xuất hiện (cho dưới dạng k). Tìm độ dài xâu con liên tiếp ngắn
nhất chứa tất cả k chữ cái khác nhau ít nhất mỗi chữ một lần. In độ dài
đó, hoặc −1 nếu bất khả.

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ k ≤ 26 (với k = số chữ cái khác nhau
trong xâu, nên −1 thực ra không xảy ra — quyết định xem bạn có tin điều
đó không).
""",
    [("khởi động", "bca (hoặc cab) phủ cả 3 chữ trong độ dài 3."),
     ("trọn xâu", "Cả hai đầu xuất hiện đúng một lần — mọi xâu con thật sự đều mất một chữ."),
     ("chữ đơn", "k = n: cả xâu."),
     ("xen kẽ", "Xác minh bằng quét trong Python (input này cũng hạ quét-chia-khối)."),
     ("đúng giới hạn", "n = 200000 trên 3 chữ: quét hai-con-trỏ trung thực là O(n).")],
)

CP14A_R = CPP_STD + cpp("""    long long n; int k; in >> n >> k;
    string s; in >> s;
    vector<int> cnt(26, 0);
    int need = k, l = 0;
    long long best = -1;
    for (int r = 0; r < (int)s.size(); ++r) {
        if (cnt[s[r] - 'a']++ == 0) --need;
        while (need == 0) {
            long long len = r - l + 1;
            best = (best < 0) ? len : min(best, len);
            if (--cnt[s[l] - 'a'] == 0) ++need;
            ++l;
        }
    }
    out << best << "{{NL}}";
""") + END

CP14A_W = CPP_STD + cpp("""    long long n; int k; in >> n >> k;
    string s; in >> s;
    // WRONG: chunk-greedy — only tries windows starting at multiples of k.
    // The optimal span's start position has no reason to align with k;
    // interleaved strings (like the 'interleaved' test) defeat it while
    // periodic strings flatter it.
    long long best = -1;
    for (long long start = 0; start < n; start += k) {
        vector<int> cnt(26, 0);
        int need = k;
        for (long long r = start; r < n; ++r) {
            if (cnt[s[r] - 'a']++ == 0) --need;
            if (need == 0) {
                long long len = r - start + 1;
                best = (best < 0) ? len : min(best, len);
                break;
            }
        }
    }
    out << best << "{{NL}}";
""") + END

# Sim 2: count subarrays with sum exactly 0 (prefix-counting, hidden).
def _gt_zero(a):
    from collections import defaultdict
    c = defaultdict(int)
    c[0] = 1
    s = 0
    ans = 0
    for v in a:
        s += v
        ans += c[s]
        c[s] += 1
    return ans


def _w_zero(a):
    # W: O(n²) double loop but with a subtle bug — counts subarrays of
    # length ≥ 2 only (excludes single zero elements).
    n = len(a)
    ans = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += a[j]
            if s == 0 and j > i:
                ans += 1
    return ans


_a1 = [1, -1, 0, 2, -2]   # a literal 0: the W skips single-element sums
_a2 = [0, 0, 0]
_gz1 = _gt_zero(_a1)
_wz1 = _w_zero(_a1)
assert _wz1 != _gz1, (_gz1, _wz1)

import random as _r4
_r4.seed(15)
_a3 = [_r4.randrange(-5, 6) for _ in range(200000)]
_gz3 = _gt_zero(_a3)

CP14B = challenge(
    "hsgm-cp-m14-zero",
    "Simulation II: The Vanishing Sums",
    """**Task.** An array of n integers. Count the non-empty contiguous
subarrays whose elements sum to exactly 0.

**Constraints:** 1 ≤ n ≤ 200000; −5 ≤ a_i ≤ 5 (the small value range is a
deliberate part of the puzzle). The answer can exceed 32-bit.

**No topic hints. Run the pipeline.**
""",
    [
        contest_test("pairs cancel", T("5", " ".join(map(str, _a1))), T(str(_gz1)),
            "Sweep-verified in Python."),
        contest_test("all zeros", T("3", "0 0 0"), T("6"),
            "Subarrays: [0],[0],[0],[0,0],[0,0],[0,0,0] → 6."),
    ],
    level="real-world",
    difficulty="advanced",
)
CP14B["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("pairs cancel", T("5", " ".join(map(str, _a1))), T(str(_gz1)),
            "Sweep-verified in Python."),
        contest_test("all zeros", T("3", "0 0 0"), T("6"),
            "Subarrays: [0],[0],[0],[0,0],[0,0],[0,0,0] → 6."),
        contest_test("no zeros", T("3", "1 2 3"), T("0"),
            "All positive sums → 0."),
        contest_test("full scale", T("200000", " ".join(map(str, _a3))), T(str(_gz3)),
            "n = 200000 values in [−5, 5]: O(n²) is dead; the value range is the invitation. Ground truth in Python."),
    )
]

CP14BVI = vi_challenge(
    "Mô phỏng II: Các tổng biến mất",
    """**Bài toán.** Một mảng n số nguyên. Đếm các mảng con liên tiếp khác
rỗng có tổng đúng bằng 0.

**Ràng buộc:** 1 ≤ n ≤ 200000; −5 ≤ a_i ≤ 5 (dải giá trị nhỏ là một phần
chủ đích của câu đố). Đáp án có thể vượt 32-bit.

**Không có gợi ý chủ đề. Hãy chạy quy trình.**
""",
    [("cặp triệt tiêu", "Xác minh bằng quét trong Python."),
     ("toàn số không", "Các mảng con: [0],[0],[0],[0,0],[0,0],[0,0,0] → 6."),
     ("không số không", "Mọi tổng dương → 0."),
     ("đúng giới hạn", "n = 200000 giá trị trong [−5, 5]: O(n²) chết; dải giá trị là lời mời.")],
)

CP14B_R = CPP_STD + cpp("""    long long n; in >> n;
    unordered_map<long long, long long> cnt;
    cnt.reserve(n * 2);
    cnt[0] = 1;
    long long s = 0, ans = 0, v;
    for (long long i = 0; i < n; ++i) {
        in >> v;
        s += v;
        auto it = cnt.find(s);
        if (it != cnt.end()) ans += it->second;
        ++cnt[s];
    }
    out << ans << "{{NL}}";
""") + END

CP14B_W = CPP_STD + cpp("""    long long n; in >> n;
    // WRONG: O(n²) double loop AND it skips single-element subarrays —
    // a zero on its own is a valid vanishing sum. Double death: the
    // complexity family (budget) and the boundary condition (catalog).
    long long ans = 0;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    for (long long i = 0; i < n; ++i) {
        long long s = 0;
        for (long long j = i; j < n; ++j) {
            s += a[j];
            if (s == 0 && j > i) ++ans;
        }
    }
    out << ans << "{{NL}}";
""") + END

# module.json for the final module: two simulation checkpoints
write_module(
    M,
    "Mixed Expert Sets and Simulation",
    "Problems with no topic label: the full pipeline under time discipline. The techniques are hidden; the recognition is the exam.",
    "Bộ chuyên gia hỗn hợp và mô phỏng",
    "Các bài không nhãn chủ đề: toàn bộ quy trình dưới kỷ luật thời gian. Kỹ thuật bị giấu; nhận diện chính là kỳ thi.",
    ["hsgm-m14-pipeline", "hsgm-m14-simulate", "hsgm-cp-m14", "hsgm-cp-m14b"],
    ["hsgm-p14-drills"],
)

# Emit both simulation challenges as lesson-attached challenges of two
# checkpoint lessons.
M_LESSON_A = "hsgm-cp-m14"
M_LESSON_B = "hsgm-cp-m14b"

from hsgm import write_lesson as _wl, _cid  # re-use for the B lesson

_wl(
    M, "hsgm-m14-pipeline",
    "The Full Pipeline, No Labels",
    "Everything the course taught, in one pass: model → budget → observe → prove → implement → attack.",
    14,
    """
# The Full Pipeline, No Labels

This module's problems announce nothing. The pipeline runs in order, and
each stage has a time box:

1. **Model (3–5 min).** Objects, quantities, objective, constraints — on
   paper. No algorithm thought yet.
2. **Budget (2 min).** Multiply the op count of the obvious approach. The
   constraint table names the allowed complexity family.
3. **Observe (10 min).** Compute small cases; run the Big Four scan
   (invariant, parity, monotonicity, symmetry).
4. **Prove (5 min).** One exchange argument, one induction, or an honest
   "unproven hypothesis" tag — which drops the plan's rank.
5. **Implement (rest).** With the complexity family chosen and the key
   observation proven, the code is usually the fast part.
6. **Attack (before submitting).** The five-shape checklist, run against
   your own solution.

## When the pipeline stalls

Stalls happen at stage 3 most often. The escape is *reformulation*
(Module 3): count the complement, reframe the object, decompose the
condition. The second escape is the constraint table: a band you can
solve is worth real points right now.

## The goal state

You know the pipeline is internalized when you can narrate it *while*
solving, without going back to read it. That narration is what the
simulations below train.
""",
    "Toàn bộ quy trình, không nhãn",
    "Mọi thứ khóa học đã dạy, trong một lượt: mô hình → ngân sách → nhận xét → chứng minh → cài đặt → tấn công.",
    """
# Toàn bộ quy trình, không nhãn

Các bài của module này không công bố gì cả. Quy trình chạy theo thứ tự,
và mỗi chặng có một khung thời gian:

1. **Mô hình (3–5 phút).** Đối tượng, đại lượng, mục tiêu, ràng buộc —
   trên giấy. Chưa nghĩ thuật toán.
2. **Ngân sách (2 phút).** Nhân số phép toán của hướng tiếp cận hiển nhiên.
   Bảng giới hạn gọi tên họ độ phức tạp được phép.
3. **Nhận xét (10 phút).** Tính các case nhỏ; chạy quét Bốn-Họ (bất biến,
   parity, đơn điệu, đối xứng).
4. **Chứng minh (5 phút).** Một luận điểm hoán đổi, một quy nạp, hoặc gắn
   nhãn trung thực "giả-thuyết-chưa-chứng-minh" — thứ hạ thứ hạng của
   phương án.
5. **Cài đặt (phần còn lại).** Với họ độ phức tạp đã chọn và nhận xét then
   chốt đã chứng minh, code thường là phần nhanh.
6. **Tấn công (trước khi nộp).** Danh mục năm-hình-dạng, chạy ngược vào
   lời giải của chính mình.

## Khi quy trình tắc

Tắc thường xảy ra ở chặng 3. Lối thoát là *phát biểu lại* (Module 3):
đếm phần bù, đổi khung đối tượng, phân rã điều kiện. Lối thoát thứ hai là
bảng giới hạn: một dải bạn giải được đáng bao nhiêu điểm thật ngay bây giờ.

## Trạng thái đích

Bạn biết quy trình đã nhuần nhuyễn khi có thể *thuật lại nó trong lúc*
giải, không cần quay lại đọc. Việc thuật lại đó là điều các mô phỏng dưới
đây rèn luyện.
""",
)

_wl(
    M, "hsgm-m14-simulate",
    "Running the Simulation",
    "Two full mixed problems, timed, with a post-contest review form. The review is the lesson.",
    14,
    """
# Running the Simulation

Treat this module's problems as a mini-contest: choose your own order,
allocate ~35 minutes each, and write down your decisions as you make
them. Afterward, fill the review:

1. **What did I solve, and at what time?**
2. **Where did the pipeline stall, and at which stage?**
3. **Which observation unlocked it — and how long until I found it?**
4. **Did I prove it, or trust it?**
5. **What would I attack first on my own accepted solution?**

## Reading your own review

- Stalls at *model* → vocabulary problem: re-read Module 3's
  reformulation patterns.
- Stalls at *observe* → experiment more, theorize less: your tables were
  too small or too unstructured.
- Stalls at *implement* → the complexity family was chosen before the
  observation was proven; you rewrote the code.
- Overruns at *attack* → the checklist was skipped; the fix is
  mechanical, not intellectual.

## The meta-point

Simulations are not for verifying that you know things. They are for
exposing the *sequence* you actually run under pressure — which is
almost never the sequence you believe you run. The gap between the two
is the last skill this course can give you.
""",
    "Chạy mô phỏng",
    "Hai bài hỗn hợp trọn vẹn, có bấm giờ, với biểu đánh giá sau kỳ thi. Phần đánh giá chính là bài học.",
    """
# Chạy mô phỏng

Coi các bài của module này như một kỳ-thi-nhỏ: tự chọn thứ tự, phân bổ
~35 phút mỗi bài, và ghi lại các quyết định của bạn khi đưa ra. Sau đó,
điền đánh giá:

1. **Tôi đã giải được gì, vào lúc nào?**
2. **Quy trình tắc ở đâu, ở chặng nào?**
3. **Nhận xét nào mở khóa nó — và mất bao lâu để tìm ra?**
4. **Tôi đã chứng minh nó, hay tin nó?**
5. **Tôi sẽ tấn công điều gì đầu tiên trên lời giải đã AC của chính mình?**

## Đọc đánh giá của chính mình

- Tắc ở *mô hình* → vấn đề vốn-từ: đọc lại các mẫu phát biểu lại của
  Module 3.
- Tắc ở *nhận xét* → thực nghiệm nhiều hơn, suy đoán ít hơn: các bảng của
  bạn quá nhỏ hoặc quá thiếu cấu trúc.
- Tắc ở *cài đặt* → họ độ phức tạp được chọn trước khi nhận xét được
  chứng minh; bạn viết lại code.
- Vượt giờ ở *tấn công* → danh mục bị bỏ qua; phép sửa là cơ khí, không
  phải trí tuệ.

## Điểm siêu-nghị luận

Mô phỏng không phải để xác nhận bạn biết mọi thứ. Chúng phơi bày *chuỗi*
bạn thực sự chạy dưới áp lực — thứ hầu như không bao giờ là chuỗi bạn
tin rằng mình chạy. Khoảng cách giữa hai cái là kỹ năng cuối cùng khóa
này trao cho bạn.
""",
)

# The two simulation challenges become checkpoint lessons with attached
# challenges (house pattern): lesson A and lesson B.
from hsgm import write_checkpoint as _wcp

_wcp(M, "hsgm-cp-m14",
    "Simulation I — The Complete Set",
    "Hidden-topic problem: shortest substring covering all k letters. No hints; the pipeline is the method.",
    25,
    """
**Simulation I.** No topic announced. Model it, check the budget, find
the sweep. The interleaved test defeats chunk-greedy scans — if your
first idea was 'windows aligned to k', the pipeline's observe stage just
saved your submission.
""",
    "Mô phỏng I — Bộ hoàn chỉnh",
    "Bài ẩn-chủ-đề: xâu con ngắn nhất phủ tất cả k chữ. Không gợi ý; quy trình là phương pháp.",
    """
**Mô phỏng I.** Không công bố chủ đề. Mô hình hóa, soát ngân sách, tìm
phép quét. Test xen-kẽ hạ các quét-chia-khối — nếu ý tưởng đầu của bạn là
'cửa sổ căn-theo-k', chặng nhận-xét của quy trình vừa cứu lần nộp của bạn.
""",
    CP14A,
    CP14AVI,
    CP14A_R,
    CP14A_W,
)

_wcp(M, "hsgm-cp-m14b",
    "Simulation II — The Vanishing Sums",
    "Hidden-topic problem: count zero-sum subarrays. The small value range is a deliberate gift — read the constraint table as a hint machine.",
    25,
    """
**Simulation II.** No topic announced. The value bound (−5..5) is the
invitation: some counting structure over the reachable prefix sums beats
any pairwise scan. The all-zeros test pins the empty/degenerate boundary.
""",
    "Mô phỏng II — Các tổng biến mất",
    "Bài ẩn-chủ-đề: đếm mảng con có tổng 0. Dải giá trị nhỏ là một món quà chủ đích — hãy đọc bảng giới hạn như một máy sinh gợi ý.",
    """
**Mô phỏng II.** Không công bố chủ đề. Cận giá trị (−5..5) là lời mời:
một cấu trúc đếm trên các tổng tiền tố tới-được thắng mọi phép quét theo
cặp. Test toàn-số-không neo biên thoái hóa/rỗng.
""",
    CP14B,
    CP14BVI,
    CP14B_R,
    CP14B_W,
)

print("module m14 complete")
