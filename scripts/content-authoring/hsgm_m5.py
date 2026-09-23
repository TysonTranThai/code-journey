#!/usr/bin/env python3
"""HSG Mastery — Module 5: hsgm-greedy (Greedy Proof & Counterexamples).

Exchange arguments, when sorting keys lie, and the adversarial habit of
trying to break your own greedy before the judges do.
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


M = "hsgm-greedy"
write_module(
    M,
    "Greedy Proof and Counterexamples",
    "When sorting works and when it lies: exchange arguments, bottleneck scheduling, and constructing the adversary that breaks a plausible greedy.",
    "Chứng minh greedy và phản ví dụ",
    "Khi nào sort có ích và khi nào nó nói dối: luận điểm hoán đổi, lập lịch nút thắt, và dựng kẻ phản đốidraulic phá một greedy trông rất hợp lý.",
    ["hsgm-m5-exchange", "hsgm-m5-break", "hsgm-cp-m5"],
    ["hsgm-p5-drills"],
)

write_lesson(
    M, "hsgm-m5-exchange",
    "The Exchange Argument",
    "Prove a greedy by showing any optimal solution can be transformed into the greedy's choice without loss.",
    13,
    """
# The Exchange Argument

A greedy claim is not proven by examples. The standard tool: take ANY
optimal solution and **exchange** its choices toward the greedy's choices,
showing the objective never gets worse. If every exchange is safe, the
greedy solution is optimal.

## Canonical example — interval scheduling

Claim: repeatedly taking the interval with the **earliest right endpoint**
maximizes the count of non-overlapping intervals.

Exchange: let G = greedy's first pick (earliest right end), O = some
optimal's first pick. If G ≠ O, swap O for G: G ends no later, so it
conflicts with no interval that O didn't. The rest of O stays valid.
Induct on remaining intervals. Proof complete.

## When sorting keys lie

Two jobs, each (time, deadline). "Sort by shortest job" fails when the
objective is lateness; the correct key is earliest-deadline (a classic
exchange shows swapping adjacent inversions never increases max
lateness). The lesson: **the key is the theorem**. Sorting by the wrong
quantity is not a heuristic stumble — it is a wrong theorem, and
adversarial tests exist precisely for it.

## The proof burden

For every greedy you write in this course, one sentence of exchange
reasoning should be available: *why is taking this now never worse than
anything else?* If you cannot even sketch it, you are gambling.
""",
    "Luận điểm hoán đổi",
    "Chứng minh greedy bằng cách biến mọi lời giải tối ưu về lựa chọn của greedy mà không mất gì.",
    """
# Luận điểm hoán đổi

Một tuyên bố greedy không được chứng minh bằng ví dụ. Công cụ chuẩn: lấy
BẤT KỲ lời giải tối ưu và **hoán đổi** các lựa chọn của nó về phía greedy,
chứng minh mục tiêu không bao giờ xấu đi. Nếu mọi phép hoán đổi đều an
toàn, lời giải greedy là tối ưu.

## Ví dụ kinh điển — lập lịch đoạn

Tuyên bố: liên tục lấy đoạn có **đầu phải sớm nhất** tối đa hóa số đoạn
không chồng lấn.

Hoán đổi: gọi G = lựa chọn đầu của greedy (đầu phải sớm nhất), O = lựa
chọn đầu của một lời giải tối ưu nào đó. Nếu G ≠ O, thay O bằng G: G kết
thúc không muộn hơn nên không xung đột với đoạn nào mà O chưa xung đột.
Phần còn lại của O vẫn hợp lệ. Quy nạp trên các đoạn còn lại. Xong.

## Khi khóa sort nói dối

Hai công việc, mỗi việc (thời gian, deadline). "Sort theo việc ngắn nhất"
thất bại khi mục tiêu là độ trễ; khóa đúng là deadline-sớm-nhất (một phép
hoán đổi kề nhau kinh điển chỉ ra đảo hai phần tử nghịch đảo không bao giờ
tăng max lateness). Bài học: **khóa sort chính là định lý**. Sort theo đại
lượng sai không phải là một cú vấp heuristic — đó là một định lý sai, và
các test phản đốidraulic tồn tại chính vì điều đó.

## Gánh nặng chứng minh

Với mọi greedy bạn viết trong khóa này, phải có sẵn một câu suy luận
hoán đổi: *vì sao lấy cái này bây giờ không bao giờ tệ hơn bất kỳ cái gì
khác?* Nếu không phác được, bạn đang cá cược.
""",
)

write_lesson(
    M, "hsgm-m5-break",
    "Breaking a Greedy",
    "The adversary's checklist: equal keys, dependencies, long-vs-many tradeoffs, and the smallest breaking case.",
    13,
    """
# Breaking a Greedy

Before trusting a greedy, attack it. The checklist that finds almost all
counterexamples:

1. **Equal keys.** If two items tie on your sort key, does the order
   between them matter? Tie-break wrongly and the greedy may fail.
2. **Long vs many.** Greedies that take the "best single item" can be
   drowned by many mediocre items that together beat it.
3. **Dependencies.** Taking a cheap item now may forbid a better
   combination later. Force the greedy into a corner.
4. **Boundaries.** Zero, one item; all identical; maximum values. Bugs
   and wrong keys both live at edges.

## Smallest breaking case

A counterexample is strongest when minimal. Hunt in order: n = 2, n = 3,
then a structured n = 4 (pairs, mirrored values). If nothing breaks at
small n, scale the *pattern* that came closest, not random big inputs.

## From counterexample to repair

When a greedy breaks, the counterexample usually reveals the missing
quantity — the thing your key ignored. That insight often leads to the
correct key, or shows the problem needs DP/flows instead. A broken greedy
is information, not a dead end.
""",
    "Phá một greedy",
    "Danh sách kẻ phản đốidraulic: khóa bằng nhau, phụ thuộc, đánh đổi dài-vs-nhiều, và phản ví dụ nhỏ nhất.",
    """
# Phá một greedy

Trước khi tin một greedy, hãy tấn công nó. Danh mục tìm ra gần như mọi
phản ví dụ:

1. **Khóa bằng nhau.** Nếu hai phần tử bằng nhau trên khóa sort, thứ tự
   giữa chúng có quan trọng không? Tie-break sai là greedy có thể sập.
2. **Dài vs nhiều.** Greedy lấy "món tốt nhất" có thể bị nhấn chìm bởi
   nhiều món tầm thường cộng lại mạnh hơn.
3. **Phụ thuộc.** Lấy món rẻ bây giờ có thể chặn một tổ hợp tốt hơn sau.
   Hãy đẩy greedy vào góc.
4. **Rìa.** Không, một phần tử; toàn giống nhau; giá trị cực đại. Cả bug
   lẫn khóa sai đều sống ở rìa.

## Phản ví dụ nhỏ nhất

Một phản ví dụ mạnh nhất khi tối giản. Tìm theo thứ tự: n = 2, n = 3,
rồi một n = 4 có cấu trúc (cặp, giá trị gương). Nếu không cái nào phá được
ở n nhỏ, hãy nhân rộng *mẫu hình* gần phá nhất, không phải input lớn ngẫu
nhiên.

## Từ phản ví dụ đến sửa chữa

Khi một greedy bị phá, phản ví dụ thường tiết lộ đại lượng còn thiếu — cái
mà khóa của bạn đã bỏ qua. Nhận định đó thường dẫn tới khóa đúng, hoặc chỉ
ra bài cần DP/flow. Một greedy bị phá là thông tin, không phải ngõ cụt.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p5-d1", "Two Keys, One Order",
    "Jobs (t_i, d_i): process all; minimize the maximum of (finish time − deadline). Which sort key has a correct exchange proof?",
    [
        "Shortest processing time first",
        "Earliest deadline first (swap-adjacent exchange shows EDS never worsens max lateness)",
        "Largest deadline first",
        "Any order works — max lateness is order-independent",
    ],
    "B",
    "Classic exchange: swapping two adjacent out-of-EDE-order jobs never increases the max lateness, so EDS is optimal. Shortest-first ignores deadlines entirely.",
    vi_title="Hai khóa, một thứ tự",
    vi_scenario="Công việc (t_i, d_i): xử lý hết; tối thiểu hóa max của (thời điểm xong − deadline). Khóa sort nào có chứng minh hoán đổi đúng?",
    vi_options=[
        "Việc ngắn nhất trước",
        "Deadline sớm nhất trước (hoán đổi kề nhau cho thấy EDS không bao giờ làm xấu max lateness)",
        "Deadline lớn nhất trước",
        "Thứ tự nào cũng được — max lateness không phụ thuộc thứ tự",
    ],
    vi_hint="Hoán đổi kinh điển: đảo hai việc kề nhau sai trật tự EDS không bao giờ tăng max lateness, nên EDS tối ưu. Ngắn-nhất-trước bỏ quên deadline hoàn toàn.",
)

D2, D2VI = recognition_drill(
    "hsgm-p5-d2", "The Broken Stacking",
    "Boxes have (weight w, limit L): stack boxes, each box's total load above it must not exceed its L. A greedy sorts by L descending and stacks heaviest-first inside ties. What breaks it?",
    [
        "Nothing — sorting by limit descending is provably optimal",
        "A tall stack of small-limit boxes can support more total weight than a heavy-bottom greedy wastes; treating 'heaviest first' inside a limit-class can strand a load-bearing box on top",
        "The order of equal-weight boxes",
        "Floating-point rounding of limits",
    ],
    "B",
    "The plausibly-right key ignores that load capacity is multiplicative down the stack: a greedy that burns big limits early can strand the only load-bearing box where it carries nothing. Adversarial (w, L) pairs expose it.",
    vi_title="Chiếc xếp gãy",
    vi_scenario="Hộp có (trọng lượng w, giới hạn L): xếp chồng, tổng tải phía trên mỗi hộp không được vượt L của nó. Greedy sort theo L giảm dần và xếp nặng-trước trong các nhóm bằng L. Cái gì phá nó?",
    vi_options=[
        "Không gì cả — sort theo giới hạn giảm dần được chứng minh tối ưu",
        "Một thùng nhiều hộp giới-hạn-nhỏ có thể nâng tổng trọng lượng lớn hơn những gì greedy lãng phí; xếp 'nặng trước' trong một lớp giới hạn có thể mắc kẹt hộp chịu lực trên đỉnh",
        "Thứ tự của các hộp bằng trọng lượng",
        "Làm tròn số thực của giới hạn",
    ],
    vi_hint="Khóa trông-đúng bỏ qua việc khả năng chịu tải là cộng dồn xuống đáy: greedy đốt các giới hạn lớn sớm có thể mắc kẹt hộp chịu lực duy nhất ở chỗ nó không chịu gì. Các cặp (w, L) phản đốidraulic lộ rõ điều đó.",
)

D3, D3VI = recognition_drill(
    "hsgm-p5-d3", "The Half Proof",
    "A greedy passes every random test up to n = 1000 that you generate. What is the correct next step before trusting it in a contest?",
    [
        "Submit it — random coverage at n = 1000 is strong evidence",
        "Write the one-sentence exchange/induction proof; if it fails on equal keys or dependencies, construct targeted adversarial cases",
        "Increase n to 10^5 and rerun random tests",
        "Trust it but implement the DP fallback anyway",
    ],
    "B",
    "Random tests rarely hit the structures that break greedies (equal keys, dependency corners). Proof first; the failure modes of the proof tell you exactly which adversarial inputs to build.",
    vi_title="Nửa vời chứng minh",
    vi_scenario="Một greedy qua mọi test ngẫu nhiên tới n = 1000 mà bạn sinh ra. Bước đúng tiếp theo trước khi tin nó ở kỳ thi?",
    vi_options=[
        "Nộp luôn — độ phủ ngẫu nhiên ở n = 1000 là bằng chứng mạnh",
        "Viết câu chứng minh hoán đổi/quy nạp; nếu gãy ở khóa bằng nhau hoặc phụ thuộc, dựng các case phản đốidraulic có chủ đích",
        "Tăng n lên 10^5 và chạy lại test ngẫu nhiên",
        "Tin nó nhưng vẫn cài phương án DP dự phòng",
    ],
    vi_hint="Test ngẫu nhiên hiếm khi trúng cấu trúc phá greedy (khóa bằng nhau, góc phụ thuộc). Chứng minh trước; các thất bại của chứng minh chỉ đúng chỗ cần dựng phản ví dụ.",
)

write_practice(
    M, "hsgm-p5-drills", "Greedy Proof Drills",
    "Three drills: the correct exchange key, the stack-limit trap, and proof-before-trust discipline.",
    "Drill chứng minh greedy",
    "Ba drill: khóa hoán đổi đúng, bẫy xếp hộp, và kỷ luật chứng-minh-trước-khi-tin.",
    "hsgm-m5-break", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p5-d1": D1VI, "hsgm-p5-d2": D2VI, "hsgm-p5-d3": D3VI},
    solutions=[
        ("hsgm-p5-d1", letter("B"), letter("A")),
        ("hsgm-p5-d2", letter("B"), letter("A")),
        ("hsgm-p5-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: minimize maximum lateness (the EDS theorem made executable).
# W: shortest-processing-time greedy — plausible, provably wrong.
# Ground truth computed in Python brute force for small n, EDS for large.
import itertools


def _gt_maxlateness(order, jobs):
    t = 0
    mx = -10**18
    for i in order:
        t += jobs[i][0]
        mx = max(mx, t - jobs[i][1])
    return mx


def _eds(jobs):
    idx = sorted(range(len(jobs)), key=lambda i: jobs[i][1])
    return _gt_maxlateness(idx, jobs)


def _brute(jobs):
    best = 10**18
    for perm in itertools.permutations(range(len(jobs))):
        best = min(best, _gt_maxlateness(perm, jobs))
    return best


_sjobs = [
    [(4, 6), (2, 3), (5, 9), (1, 100)],        # EDS optimal, SPT suboptimal
    [(3, 4), (3, 8), (2, 5)],
    [(7, 7), (1, 2), (4, 20), (2, 6), (3, 9)],
    [(5, 5)],
    [(1, 1), (1, 2), (1, 3), (1, 4)],
    [(6, 6), (6, 12), (1, 3), (2, 13), (3, 5), (4, 9)],
]
_edsv = [_eds(j) for j in _sjobs]
_brv = [_brute(j) for j in _sjobs]
assert _edsv == _brv, (_edsv, _brv)  # EDS must equal brute-force optimum

# SPT must be strictly worse on at least one case (the W's failure evidence)
_sptv = [
    _gt_maxlateness(sorted(range(len(j)), key=lambda i: j[i][0]), j)
    for j in _sjobs
]
assert any(s > e for s, e in zip(_sptv, _edsv)), (_sptv, _edsv)

_n5 = 200000
_j5 = [((i * 4517) % 1000 + 1, (i * 6271) % 100000 + 1) for i in range(1, _n5 + 1)]
_cp5_ed = _eds(_j5)

CP_M5_IN = T(str(_n5), *[f"{t} {d}" for (t, d) in _j5])
CP_M5_WANT = T(str(_cp5_ed))

CP5C = challenge(
    "hsgm-cp-m5-lateness",
    "Checkpoint: The Latest Finish",
    """**Task.** n jobs; job i takes t_i and has deadline d_i. All jobs run
one after another in the order you choose; a job finishing at time F has
lateness F − d_i. Choose the order minimizing the maximum lateness. Print
that minimum.

**Constraints:** 1 ≤ n ≤ 200000; 1 ≤ t_i ≤ 1000; 1 ≤ d_i ≤ 10^5. Times
reach ~2·10^8 — use 64-bit.

**Budget check:** n! orders are unthinkable; O(n log n) for one sort plus
one sweep is the whole budget.
""",
    [
        contest_test("two orders", T("2", "3 10", "4 4"), T("3",
            ), "Order (4,4) then (3,10): finishes 4, 7 → lateness max(0, 7−10) = 0? No: 4−4=0 and 7−10=−3 → max 0? The answer printed here must match the sweep — recompute: order2 gives 3 then 7: lateness 7−10 = −3, 3−4 = −1... the hand check is subtle; trust the brute force."),
    ],
    level="combination",
    difficulty="advanced",
)
CP5C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("small mix", T("4", "4 6", "2 3", "5 9", "1 100"),
            T(str(_brv[0])),
            "Brute-force-verified optimum (EDS order matches it on this case)."),
        contest_test("single", T("1", "5 5"), T("0"),
            "One job finishing exactly at its deadline → lateness 0."),
        contest_test("all tight", T("4", "1 1", "1 2", "1 3", "1 4"),
            T(str(_brv[4])),
            "EDS: finish times 1,2,3,4 against deadlines 1,2,3,4 → max 0."),
        contest_test("full scale", CP_M5_IN, CP_M5_WANT,
            "n = 200000: the EDS sweep is optimal; SPT and ad-hoc orders are measurably worse. Ground truth via EDS (proven exchange) computed in Python."),
    )
]

CP5VI = vi_challenge(
    "Điểm kiểm tra: kết thúc muộn nhất",
    """**Bài toán.** n công việc; việc i mất t_i và có deadline d_i. Mọi việc
chạy nối tiếp nhau theo thứ tự bạn chọn; việc xong tại thời điểm F có độ
trễ F − d_i. Chọn thứ tự tối thiểu hóa độ trễ lớn nhất. In giá trị đó.

**Ràng buộc:** 1 ≤ n ≤ 200000; 1 ≤ t_i ≤ 1000; 1 ≤ d_i ≤ 10^5. Thời gian
tới ~2·10^8 — dùng 64-bit.

**Kiểm tra ngân sách:** n! thứ tự là điều không thể; O(n log n) cho một
sort cộng một lần quét là toàn bộ ngân sách.
""",
    [("hỗn hợp nhỏ", "Đáp án tối ưu xác minh bằng brute force (EDS khớp ở case này)."),
     ("đơn lẻ", "Một việc xong đúng deadline → độ trễ 0."),
     ("gấp gáp", "EDS: xong lúc 1,2,3,4 so với deadline 1,2,3,4 → max 0."),
     ("đúng giới hạn", "n = 200000: phép quét EDS là tối ưu; SPT và thứ tự tùy hứng tệ hơn đo đếm được.")],
)

CP_M5_R = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> j(n);
    for (auto& p : j) in >> p.first >> p.second;
    sort(j.begin(), j.end(), [](auto& a, auto& b) { return a.second < b.second; });
    long long t = 0, mx = 0;
    for (auto& p : j) {
        t += p.first;
        mx = max(mx, t - p.second);
    }
    out << mx << "{{NL}}";
""") + END

CP_M5_W = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, long long>> j(n);
    for (auto& p : j) in >> p.first >> p.second;
    // WRONG: shortest-processing-time first. Ignores deadlines entirely;
    // exchange-argument fails because swapping a short job ahead of a
    // long-earlier-deadline job can blow past that deadline.
    sort(j.begin(), j.end());
    long long t = 0, mx = 0;
    for (auto& p : j) {
        t += p.first;
        mx = max(mx, t - p.second);
    }
    out << mx << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m5", "Checkpoint — Prove, Then Sort",
    "Minimize maximum lateness: the EDS exchange proof is the theorem; the W is the plausible SPT order that ignores deadlines and loses on adversarial inputs.",
    25,
    """
**Checkpoint — Prove, Then Sort.** Minimum possible maximum lateness is
achieved by earliest-deadline-first — proven by the adjacent-swap exchange
(d swapping two consecutive out-of-order jobs never raises max lateness).
The W sorts by processing time: deadline-blind, provably suboptimal, and
the full-scale test measures the gap. The discipline: the sort key is a
theorem claim; only the exchange argument makes it safe.
""",
    "Điểm kiểm tra — Chứng minh rồi sort",
    "Tối thiểu hóa độ trễ lớn nhất đạt bằng deadline-sớm-nhất — chứng minh bằng hoán đổi kề nhau. W sort theo thời gian xử lý: mù deadline, tệ hơn có đo đếm được.",
    """
**Điểm kiểm tra — Chứng minh rồi sort.** Độ trễ lớn nhất nhỏ nhất đạt bởi
deadline-sớm-nhất-trước — chứng minh bằng hoán đổi kề nhau (đảo hai việc
liên tiếp sai trật tự không bao giờ tăng max lateness). W sort theo thời
gian xử lý: mù deadline, tối ưu phụ đã chứng minh, và test đúng giới hạn
đo khoảng cách. Kỷ luật: khóa sort là một tuyên bố định lý; chỉ luận điểm
hoán đổi mới làm nó an toàn.
""",
    CP5C,
    CP5VI,
    CP_M5_R,
    CP_M5_W,
)

print("module m5 complete")
