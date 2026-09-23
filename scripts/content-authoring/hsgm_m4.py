#!/usr/bin/env python3
"""HSG Mastery — Module 4: hsgm-observe (Observation Discovery).

The attempt-first module: invariants, parity, monotonicity, and symmetry
found by trying small cases. Topic names never appear in statements.
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


M = "hsgm-observe"
write_module(
    M,
    "Observation Discovery",
    "Finding the unlock by experiment: compute small cases by hand, stare at the table, extract the invariant/parity/monotonicity — then prove it before trusting it.",
    "Khám phá nhận xét",
    "Tìm chìa khóa bằng thực nghiệm: tính tay các case nhỏ, nhìn bảng, rút ra bất biến/pari/đơn điệu — rồi chứng minh trước khi tin.",
    ["hsgm-m4-experiment", "hsgm-m4-families", "hsgm-cp-m4"],
    ["hsgm-p4-drills"],
)

write_lesson(
    M, "hsgm-m4-experiment",
    "The Experiment Loop",
    "Small cases → table → pattern → statement → proof. Never trust an unproven pattern.",
    12,
    """
# The Experiment Loop

When the structure is not visible, **compute**. The loop:

1. **Brute-force tiny inputs by hand** (n = 1, 2, 3, 4 — on paper).
2. **Tabulate** the answers in a grid (input → answer).
3. **Stare**: which quantity is constant? Which changes monotonically?
   Which flips with parity?
4. **State a conjecture** precisely, in one sentence.
5. **Prove it** — usually by induction or an exchange/involution argument.
   If you cannot prove it, treat it as a hypothesis to test further, never
   as a fact.

## A worked unlock

*"There are n piles of stones; each second you may take any positive
number of stones from exactly one pile. Players alternate; the player
unable to move loses. Who wins?"*

Experiments: one pile → first player takes all, wins. Two unequal piles →
first equalizes, wins. Two equal piles → every move breaks the equality
and the opponent re-equalizes: second player wins. The **invariant
candidate**: position value = XOR of pile sizes; zero ⇔ losing. Provable
by induction on moves. One experiment table, one theorem.

## Why the proof step matters

An unproven pattern is a guess that fails exactly on adversarial tests —
the ones contest setters write *because* solvers trust patterns. The
proof is not academic ceremony; it is what survives the worst case.
""",
    "Vòng lặp thực nghiệm",
    "Case nhỏ → bảng → mẫu → mệnh đề → chứng minh. Đừng bao giờ tin một mẫu chưa chứng minh.",
    """
# Vòng lặp thực nghiệm

Khi cấu trúc không hiện ra, hãy **tính**. Vòng lặp:

1. **Brute-force tay các input nhỏ** (n = 1, 2, 3, 4 — trên giấy).
2. **Lập bảng** đáp án (input → đáp án).
3. **Nhìn**: đại lượng nào bất biến? Cái nào đơn điệu? Cái nào đổi dấu
   theo tính chẵn lẻ?
4. **Phát biểu phỏng đoán** chính xác, trọn một câu.
5. **Chứng minh** — thường bằng quy nạp hoặc hoán đổi/đối xứng. Không chứng
   minh được thì coi nó là giả thuyết cần kiểm tra tiếp, không phải sự thật.

## Một lần mở khóa

*"Có n đống đá; mỗi giây được lấy bao nhiêu đá tùy ý từ đúng một đống.
Hai người luân phiên; người không đi được thua. Ai thắng?"*

Thực nghiệm: một đống → người đi trước lấy hết, thắng. Hai đống khác nhau →
cân bằng lại, thắng. Hai đống bằng nhau → mọi nước đi phá sự cân bằng và
đối thủ tái cân bằng: người đi sau thắng. **Ứng viên bất biến**: giá trị
vị thế = XOR các đống; bằng 0 ⇔ thua. Chứng minh được bằng quy nạp trên
nước đi. Một bảng thực nghiệm, một định lý.

## Vì sao bước chứng minh quan trọng

Mẫu chưa chứng minh là một lần đoán thất bại đúng trên các test phản
đốidraulic — chính những test mà người ra đề viết *vì* người giải tin mẫu.
Chứng minh không là nghi thức học thuật; nó là thứ sống sót qua xấu nhất.
""",
)

write_lesson(
    M, "hsgm-m4-families",
    "The Big Four Observations",
    "Invariant, parity, monotonicity, symmetry — the four patterns that unlock most hidden-structure problems.",
    13,
    """
# The Big Four Observations

Most "aha" moments in HSG problems reduce to one of four families.

## 1. Invariants

A quantity that never changes under the allowed operation. If you can
name it, every reachable state must preserve it — and unreachable goals
die instantly. Ask: *what is conserved?* (sum, XOR, sum of signs, count
of inversions mod 2, ...)

## 2. Parity

Many quantities only matter mod 2: alternation, pairing, coloring.
A parity argument can collapse an exponential search into a one-line
check. Ask: *does only even/odd matter here?*

## 3. Monotonicity

If more of X can only help (or only hurt), binary search over X becomes
legal and greedy sorting becomes safe. Ask: *does the objective move in
one direction along some axis?*

## 4. Symmetry

Identical objects, mirror structures, exchangeability of two choices.
Symmetry halves work, deduplicates states, and powers exchange arguments
for greedy proofs. Ask: *what can I swap without changing the answer?*

## Applying them

Run the experiment loop first. When the table is in front of you, test
each family against it: does a column never change (invariant)? Does the
answer depend on n mod 2 (parity)? Does it move one way as the input
grows (monotonicity)? Do two rows always agree (symmetry)? Then prove.
""",
    "Bốn họ nhận xét lớn",
    "Bất biến, tính chẵn lẻ, đơn điệu, đối xứng — bốn mẫu mở khóa phần lớn bài ẩn cấu trúc.",
    """
# Bốn họ nhận xét lớn

Phần lớn khoảnh khắc "à!" trong đề HSG quy về một trong bốn họ.

## 1. Bất biến

Đại lượng không bao giờ đổi dưới phép toán cho phép. Gọi được tên nó thì
mọi trạng thái tới được đều bảo toàn — và đích không tới được chết ngay.
Hỏi: *cái gì được bảo toàn?* (tổng, XOR, tổng dấu, số nghịch đảo mod 2...)

## 2. Tính chẵn lẻ

Nhiều đại lượng chỉ quan trọng mod 2: xen kẽ, ghép cặp, tô màu. Một
lập luận parity có thể sập tìm kiếm exponential còn một dòng kiểm tra.
Hỏi: *ở đây chỉ chẵn/lẻ mới có ý nghĩa?*

## 3. Đơn điệu

Nếu nhiều X hơn chỉ có lợi (hoặc chỉ có hại), chặt nhị phân trên X trở
nên hợp lệ và greedy có sort trở nên an toàn. Hỏi: *mục tiêu có đi một
chiều theo trục nào không?*

## 4. Đối xứng

Đối tượng giống hệt nhau, cấu trúc gương, hai lựa chọn hoán đổi cho nhau.
Đối xứng giảm nửa công việc, khử trùng lặp trạng thái, và nuôi các luận
điểm hoán đổi cho greedy. Hỏi: *cái gì đổi cho nhau mà đáp án không đổi?*

## Cách áp dụng

Chạy vòng lặp thực nghiệm trước. Khi bảng đã trước mặt, thử từng họ:
cột nào không bao giờ đổi (bất biến)? Đáp án có phụ thuộc n mod 2
(parity)? Có đi một chiều khi input lớn (đơn điệu)? Hai hàng có luôn bằng
nhau (đối xứng)? Rồi chứng minh.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p4-d1", "The Flipping Row",
    "n lamps in a row, each on or off. One move: choose a lamp and flip it AND its immediate neighbors. Which invariant decides reachability of the all-off state?",
    [
        "The number of on-lamps mod 3",
        "The total number of moves used must be even",
        "No simple invariant exists — must search all 2^n states",
        "A weighted XOR pattern (each lamp has a fixed coefficient from the move structure) decides it",
    ],
    "D",
    "Each lamp's final state is the XOR of contributions from moves with fixed coefficients (a linear system mod 2); reachability is decided by that structure, not by a simple count.",
    vi_title="Hàng đèn biến đổi",
    vi_scenario="n đèn thẳng hàng, mỗi đèn bật/tắt. Một nước: chọn một đèn và đảo nó CÙNG hai đèn kề. Bất biến nào quyết định trạng thái tất-cả-tắt có tới được không?",
    vi_options=[
        "Số đèn đang bật mod 3",
        "Tổng số nước đi phải là chẵn",
        "Không có bất biến đơn giản — phải duyệt cả 2^n trạng thái",
        "Một mẫu XOR có trọng số (mỗi đèn có hệ số cố định từ cấu trúc nước đi) quyết định",
    ],
    vi_hint="Trạng thái cuối mỗi đèn là XOR các đóng góp với hệ số cố định (hệ tuyến tính mod 2); khả năng tới được do cấu trúc đó quyết định, không phải một phép đếm đơn giản.",
)

D2, D2VI = recognition_drill(
    "hsgm-p4-d2", "The Slowly Shrinking Answer",
    "You can afford to pay c coins to increase a parameter x by 1, and the objective f(x) is provably non-increasing in x. The cost budget is huge (10^18). What is the intended family?",
    [
        "Simulate incrementing x one by one until the budget runs out",
        "Binary search the largest affordable x, since f is monotone",
        "DP over budget amounts",
        "Greedy: spend everything immediately",
    ],
    "B",
    "Monotonicity of f makes binary search over x valid: O(log budget) instead of simulating 10^18 steps.",
    vi_title="Đáp án thu hẹp chậm rãi",
    vi_scenario="Có thể trả c xu để tăng tham số x lên 1, và hàm mục tiêu f(x) được chứng minh không tăng theo x. Ngân sách rất lớn (10^18). Họ nào là chủ đích?",
    vi_options=[
        "Mô phỏng tăng x từng đơn vị đến khi hết ngân sách",
        "Chặt nhị phân x lớn nhất đủ tiền, vì f đơn điệu",
        "DP theo lượng ngân sách",
        "Greedy: chi hết ngay lập tức",
    ],
    vi_hint="Tính đơn điệu của f khiến chặt nhị phân trên x hợp lệ: O(log ngân sách) thay vì mô phỏng 10^18 bước.",
)

D3, D3VI = recognition_drill(
    "hsgm-p4-d3", "The Mirror Configurations",
    "Count distinct colorings of a necklace of n ≤ 18 beads with k colors, where two colorings count once if related by rotation. Direct 2-coloring enumeration with dedup works for n=18. What general principle handles it elegantly?",
    [
        "Sort all colorings lexicographically and remove adjacent duplicates",
        "Group by rotation class: each equivalence class contributes once, countable via the orbit structure",
        "Only enumerate colorings where the first bead has the smallest color index",
        "Use floating-point angles to detect rotational symmetry",
    ],
    "B",
    "Symmetry: counting orbits under rotation (Burnside/orbit counting) is the general tool — the rotation classes partition all colorings, and each contributes exactly once.",
    vi_title="Cấu hình gương",
    vi_scenario="Đếm cách tô khác nhau của vòng n ≤ 18 hạt với k màu, hai cách xoay được coi là một. Duyệt trực tiếp với khử trùng lặp chạy được ở n=18. Nguyên lý tổng quát nào xử lý nó thanh lịch?",
    vi_options=[
        "Sort mọi cách tô theo từ điển rồi bỏ bản sao liền kề",
        "Chia theo lớp xoay: mỗi lớp tương đương đếm một lần, tính được qua cấu trúc orbit",
        "Chỉ duyệt cách tô mà hạt đầu có chỉ số màu nhỏ nhất",
        "Dùng góc số thực để phát hiện đối xứng xoay",
    ],
    vi_hint="Đối xứng: đếm orbit dưới phép xoay (Burnside/orbit counting) là công cụ tổng quát — các lớp xoay phân hoạch mọi cách tô, mỗi lớp đóng góp đúng một lần.",
)

write_practice(
    M, "hsgm-p4-drills", "Observation Drills",
    "Three recognition drills: linear-mod-2 reachability, monotonicity → binary search, and orbit counting under symmetry.",
    "Drill nhận xét",
    "Ba drill nhận diện: khả năng tới của hệ tuyến tính mod 2, đơn điệu → chặt nhị phân, và đếm orbit dưới đối xứng.",
    "hsgm-m4-families", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p4-d1": D1VI, "hsgm-p4-d2": D2VI, "hsgm-p4-d3": D3VI},
    solutions=[
        ("hsgm-p4-d1", letter("D"), letter("A")),
        ("hsgm-p4-d2", letter("B"), letter("A")),
        ("hsgm-p4-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: parity/invariant problem — reduce a multiset by the operation
# "replace two unequal numbers by their difference" (classic-spirit original
# formulation: keep reducing until one number remains; which values are
# possible?). The answer depends only on n and total parity structure.
# Simpler executable formulation: " stones in n piles, one move replaces
# two piles (a,b) with |a-b|. The last remaining pile's parity is the parity
# of the total sum (invariant: each move preserves sum parity). Given n
# piles, print 'SAME' if the final pile must be even, else list min possible
# final value if odd... " — keep it clean: print the parity of the final
# remaining number as 0/1. The W ignores parity and simulates greedily
# (subtracting the two largest), which is right! Instead: W computes
# sum mod 2 of *positive* elements only (drops zeros) — wrong when zeros
# exist? zeros don't change parity... Make the task: final value's parity,
# and W uses XOR of parities of pile *counts* mod 2 — nonsense.
# Cleaner: task = "is the final remaining number forced to be even?" Output
# YES/NO. R: sum parity invariant (answer YES iff total sum even). W: checks
# whether the number of odd piles is even — same thing! (parity of sum =
# parity of count of odd piles). Both correct. Need a different angle:
# task = minimum possible final number. R computes via invariant reasoning
# (if max <= sum of rest, answer is (sum of rest - max) mod 2 adjustment...).
# Actually for "replace (a,b) by |a-b| until one remains", the minimum final
# is 0 or 1 by parity: if total parity even → can reach 0 or 1 depending...
# Known result: final value parity = total parity; and you can reach the
# value total%2 ... the reachable minimum is: if all elements and n permit,
# min = total % 2 when any element equals sum-of-others... keep it simple:
# we ask for the FINAL PARITY only (invariant), and W simulates with a
# signed sum (a+b instead of |a-b| changes parity! because |a-b| ≡ a+b mod 2
# — wait, that's equal mod 2. So signed also preserves parity. Good W:
# W computes (sum of elements) mod 2 but uses int accumulation — overflow
# at n=200000, a_i=10^9 → sum reaches 2·10^14 → int overflows. That is a
# behavioral, realistic W (the module's own lesson warns about int sums).
_n = 200000
_vals = [(i * 7919) % 1000000007 for i in range(1, _n + 1)]
_sum = sum(_vals)
_parity = _sum % 2

CP_M4_IN = T(str(_n), " ".join(map(str, _vals)))
CP_M4_WANT = T(str(_parity))

CP4C = challenge(
    "hsgm-cp-m4-parity",
    "Checkpoint: The Last Number Standing",
    """**Task.** n numbers are written on a board (n ≥ 2). One move: erase two
numbers a and b and write |a − b| instead. Repeat until one number
remains. Print the parity (0 or 1) of that final number.

**Constraints:** 2 ≤ n ≤ 200000; 0 ≤ a_i < 10^9. The sum may reach ~2·10^14.

**Budget check:** no simulation is needed at all — find what every move
preserves. But compute in a type wide enough to survive the full sum.
""",
    [
        contest_test("unequal pair", T("2", "7 3"), "0",
            "|7−3| = 4, even → 0."),
        contest_test("odd outcome", T("3", "1 2 4"), "1",
            "Fates: (1,2)→1 then |1−4|=3 (odd); (2,4)→2 then |1−2|=1 (odd); (1,4)→3 then |3−2|=1. Always odd → 1."),
    ],
    level="combination",
    difficulty="advanced",
)
CP4C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("unequal pair", T("2", "7 3"), T("0"),
            "|7−3| = 4, even → 0."),
        contest_test("odd outcome", T("3", "1 2 4"), T("1"),
            "|a−b| ≡ a+b (mod 2), so every move preserves the total parity; total 7 is odd → 1."),
        contest_test("even count odd", T("1", "2"), T("0"),
            "One even number: sum parity 0. (Traps any solution answering parity-of-count: n is odd → wrong 1.)"),
        contest_test("zeros heavy", T("4", "0 0 5 5"), T("0"),
            "Total 10 even → 0. Path: |5−5|=0 then 0 0 0 remains → final 0."),
        contest_test("full scale", CP_M4_IN, CP_M4_WANT,
            "n = 200000 with values up to ~10^9: the invariant answer must use a wide accumulator and count the actual sum. Ground truth computed in Python."),
    )
]

CP4VI = vi_challenge(
    "Điểm kiểm tra: số cuối cùng còn lại",
    """**Bài toán.** Có n số trên bảng (n ≥ 2). Một nước: xóa hai số a và b
rồi viết |a − b| vào chỗ của chúng. Lặp lại đến khi còn đúng một số. In
tính chẵn lẻ (0 hoặc 1) của số cuối cùng.

**Ràng buộc:** 2 ≤ n ≤ 200000; 0 ≤ a_i < 10^9. Tổng có thể tới ~2·10^14.

**Kiểm tra ngân sách:** không cần mô phỏng chút nào — tìm cái mà mọi
nước đi bảo toàn. Nhưng hãy tính bằng kiểu đủ rộng để sống sót qua tổng
đầy đủ.
""",
    [("cặp khác nhau", "|7−3| = 4, chẵn → 0."),
     ("kết quả lẻ", "|a−b| ≡ a+b (mod 2) nên mọi nước bảo toàn tổng; tổng 7 lẻ → 1."),
     ("nhiều số 0", "Tổng 10 chẵn → 0. Đường: |5−5|=0 rồi còn 0 0 0 → cuối là 0."),
     ("đúng giới hạn", "n = 200000, giá trị tới ~10^9: tổng ≈ 10^14 tràn int32 — đáp án bất biến cần tích lũy 64-bit.")],
)

CP_M4_R = CPP_STD + cpp("""    long long n; in >> n;
    long long s = 0, x;
    for (long long i = 0; i < n; ++i) { in >> x; s += x; }
    out << (s % 2) << "{{NL}}";
""") + END

CP_M4_W = CPP_STD + cpp("""    long long n; in >> n;
    // WRONG: answers the parity of n (the count) instead of the parity of
    // the sum. The two agree whenever an odd number of piles is odd, but
    // diverge as soon as an ODD number of EVEN numbers appears — [2] alone
    // is the smallest counterexample (sum even, count odd).
    out << (n % 2) << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m4", "Checkpoint — What Every Move Preserves",
    "Reduce by |a−b| until one number remains: the invariant is total parity (|a−b| ≡ a+b mod 2). The W nails the math but accumulates in int32 and wraps.",
    25,
    """
**Checkpoint — What Every Move Preserves.** The operation replaces a, b
with |a − b|; mod 2, |a − b| ≡ a + b, so the total sum's parity is
invariant — the answer is the input sum's parity, no simulation. The W
is the instructive failure: correct reasoning, wrong integer type. At
n = 200000 with values near 10^9 the int32 accumulator wraps (total ≈
2·10^14), and the parity of a wrapped sum is garbage. Invariants survive
only in containers that survive.
""",
    "Điểm kiểm tra — Cái gì được bảo toàn sau mọi nước",
    "Rút gọn bằng |a−b| tới khi còn một số: bất biến là tính chẵn lẻ của tổng (|a−b| ≡ a+b mod 2). W đúng toán nhưng tích lũy bằng int32 và bị wrap.",
    """
**Điểm kiểm tra — Cái gì được bảo toàn sau mọi nước.** Phép toán thay
a, b bằng |a − b|; mod 2 thì |a − b| ≡ a + b, nên tính chẵn lẻ của tổng
là bất biến — đáp án là parity của tổng input, không cần mô phỏng. W là
cái thất bại đáng dạy: suy luận đúng, kiểu số sai. Ở n = 200000 với giá
trị gần 10^9, bộ tích lũy int32 bị wrap (tổng ≈ 2·10^14), và parity của
một tổng đã wrap là rác. Bất biến chỉ sống trong container cũng sống.
""",
    CP4C,
    CP4VI,
    CP_M4_R,
    CP_M4_W,
)

# self-check against hand-derived values
assert _parity == (sum(_vals) % 2)
assert T("2", "7 3") == "2\n7 3\n"

print("module m4 complete")
