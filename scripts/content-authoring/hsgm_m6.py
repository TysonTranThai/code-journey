#!/usr/bin/env python3
"""HSG Mastery — Module 6: hsgm-dpsynth (DP Reasoning & Synthesis).

State design from the objective, transition from the last decision, and
fusing DP with a data structure when transitions are too fat.
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


M = "hsgm-dpsynth"
write_module(
    M,
    "DP Reasoning and Synthesis",
    "Designing states from the objective's degrees of freedom, transitions from the last decision, and fusing DP with prefix/min structures when the naive transition is too fat.",
    "Lập luận và tổng hợp DP",
    "Thiết kế trạng thái từ bậc tự do của mục tiêu, chuyển tiếp từ quyết định cuối, và ghép DP với cấu trúc tiền tố/khi chuyển tiếp naive quá béo.",
    ["hsgm-m6-state", "hsgm-m6-fusion", "hsgm-cp-m6"],
    ["hsgm-p6-drills"],
)

write_lesson(
    M, "hsgm-m6-state",
    "State = Degrees of Freedom",
    "A state must capture everything the future cares about — and nothing more.",
    13,
    """
# State = Degrees of Freedom

The state of a DP answers one question: *standing here, what do I need to
know to finish optimally?* Design procedure:

1. **Scan forward.** At a decision point, list everything the future cost
   depends on: current position, resources consumed, last choice, parity
   of something, whether a flag fired.
2. **Each independent quantity = one dimension.** position × resource ×
   flag is three indices, not one clever hack.
3. **Bound every dimension.** If a dimension is unbounded, either compress
   it (only O(n) distinct values appear), or you have the wrong state.
4. **The transition comes last.** Once the state is right, the transition
   is "try every legal last move" — usually mechanical.

## The typical sizing

n ≤ 300 with two free quantities smells like O(n³) (position × position
× something) or O(n²·something). n ≤ 100000 with one free quantity smells
like O(n log n) — which means the transition must be answered by a data
structure, not a loop. **The constraint table sizes the state before you
write a line of code.**

## When the state is wrong

Symptoms: you keep adding "just one more flag" (state explosion — you are
modeling globally what should be local), or the transition needs the whole
history (a true summary dimension is missing). Fix the state, not the
symptom.
""",
    "Trạng thái = bậc tự do",
    "Một trạng thái phải gói mọi thứ tương lai cần biết — và không hơn.",
    """
# Trạng thái = bậc tự do

Trạng thái của DP trả lời đúng một câu: *đứng đây, tôi cần biết gì để kết
thúc tối ưu?* Quy trình thiết kế:

1. **Nhìn về trước.** Tại điểm quyết định, liệt kê mọi thứ chi phí tương
   lai phụ thuộc: vị trí hiện tại, tài nguyên đã tiêu, lựa chọn cuối,
   parity của gì đó, cờ đã bật chưa.
2. **Mỗi đại lượng độc lập = một chiều.** vị trí × tài nguyên × cờ là ba
   chỉ số, không phải một mẹo thông minh.
3. **Chặn biên mọi chiều.** Nếu một chiều vô biên, hoặc nén nó (chỉ O(n)
   giá trị khác nhau xuất hiện), hoặc bạn đã chọn sai trạng thái.
4. **Chuyển tiếp đến sau cùng.** Trạng thái đúng rồi thì chuyển tiếp chỉ
   là "thử mọi nước cuối hợp lệ" — thường máy móc.

## Định cỡ điển hình

n ≤ 300 với hai đại lượng tự do có mùi O(n³) (vị trí × vị trí × cái gì
đó). n ≤ 100000 với một đại lượng tự do có mùi O(n log n) — nghĩa là
chuyển tiếp phải được trả lời bởi cấu trúc dữ liệu, không phải vòng lặp.
**Bảng giới hạn định cỡ trạng thái trước khi bạn viết dòng code nào.**

## Khi trạng thái sai

Triệu chứng: liên tục phải thêm "thêm một cờ nữa" (nổ trạng thái — bạn
đang mô hình toàn cục cái đáng cục bộ), hoặc chuyển tiếp cần cả lịch sử
(một chiều tóm tắt thật sự còn thiếu). Sửa trạng thái, không sửa triệu
chứng.
""",
)

write_lesson(
    M, "hsgm-m6-fusion",
    "DP + Structure Fusion",
    "When the transition loop is the bottleneck, the answer lives in a structure: prefix min/max, Fenwick over values, monotonic deque.",
    14,
    """
# DP + Structure Fusion

Naive transition: `dp[i] = min over j < i of (dp[j] + cost(i, j))` — O(n²).
When n = 200000, that is dead. The fusion question: **can cost(i, j) be
split so the best j is answerable by a structure?**

## The three classic splits

- **Additive:** cost = dp[j] + f(i) + g(j) → maintain prefix min of
  (dp[j] + g(j)). O(1) per transition.
- **Windowed:** only j in [i−k, i] matter → sliding-window minimum
  (monotonic deque). O(n) total.
- **Thresholded:** j must satisfy value(j) ≤ x(i) → Fenwick/segment tree
  over value-space holding min dp[j], query prefix. O(log n) per
  transition.

## Recognizing fusable transitions

Write the naive transition. Underline the parts that depend only on i,
only on j, and on both. If the "both" part is separable (additive,
min-idempotent, or orderable), a structure exists. If it is genuinely
entangled (j interacts with i non-additively), fusion is impossible — the
state is wrong or the problem needs something else.

## The discipline

Fusion does not change the DP's *meaning* — only who computes the min.
Prove the transition first on paper with the loop, then fuse. Fusing an
unproven transition optimizes the wrong recurrence.
""",
    "Ghép DP + cấu trúc",
    "Khi vòng chuyển tiếp là nút thắt, đáp án nằm trong cấu trúc: tiền tố min/max, Fenwick trên giá trị, deque đơn điệu.",
    """
# Ghép DP + cấu trúc

Chuyển tiếp naive: `dp[i] = min qua j < i của (dp[j] + cost(i, j))` — O(n²).
Khi n = 200000, điều đó là chết. Câu hỏi ghép: **cost(i, j) tách được để
j tốt nhất trả lời được bởi một cấu trúc không?**

## Ba phép tách kinh điển

- **Cộng tính:** cost = dp[j] + f(i) + g(j) → giữ tiền tố min của
  (dp[j] + g(j)). O(1) mỗi chuyển tiếp.
- **Cửa sổ:** chỉ j trong [i−k, i] quan trọng → min cửa sổ trượt
  (deque đơn điệu). O(n) tổng.
- **Ngưỡng:** j phải thỏa value(j) ≤ x(i) → Fenwick/segment tree trên
  không gian giá trị giữ min dp[j], hỏi tiền tố. O(log n) mỗi chuyển tiếp.

## Nhận diện chuyển tiếp ghép được

Viết chuyển tiếp naive. Gạch chân phần chỉ phụ thuộc i, phần chỉ phụ thuộc
j, và phần phụ thuộc cả hai. Nếu phần "cả hai" tách được (cộng tính,
min-idempotent, hoặc sắp được thứ tự), một cấu trúc tồn tại. Nếu nó thực
sự rối (j tương tác với i phi cộng tính), ghép là bất khả — trạng thái sai
hoặc bài cần thứ khác.

## Kỷ luật

Ghép không đổi *ý nghĩa* của DP — chỉ đổi ai tính phép min. Chứng minh
chuyển tiếp trên giấy với vòng lặp trước, rồi ghép. Ghép một chuyển tiếp
chưa chứng minh là tối ưu hóa một truy hồi sai.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p6-d1", "The Two Coins State",
    "Walk a 1-D board of n cells; at cell i you may gain a[i] but every 3rd step you instead pay 5. What is the minimal correct state?",
    [
        "position only — the 3rd-step rule is deterministic",
        "position × (steps taken mod 3)",
        "position × total paid so far",
        "position × number of payments remaining",
    ],
    "B",
    "The future cost depends on position and the phase (mod 3) of the step counter — two bounded dimensions. Total-paid is derived, not needed; 'payments remaining' is unbounded.",
    vi_title="Trạng thái hai đồng xu",
    vi_scenario="Đi trên bàn 1-D n ô; tại ô i được nhận a[i] nhưng cứ bước thứ 3 thì phải trả 5. Trạng thái tối thiểu đúng là gì?",
    vi_options=[
        "chỉ vị trí — luật bước-thứ-3 là tất định",
        "vị trí × (số bước đã đi mod 3)",
        "vị trí × tổng đã trả",
        "vị trí × số lần trả còn lại",
    ],
    vi_hint="Chi phí tương lai phụ thuộc vị trí và pha (mod 3) của bộ đếm bước — hai chiều có biên. Tổng-đã-trả là hệ quả, không cần; 'lần-trả-còn-lại' vô biên.",
)

D2, D2VI = recognition_drill(
    "hsgm-p6-d2", "The Fat Transition",
    "dp[i] = min over j < i of dp[j] + (a[i] + b[j])² — note the square spans both i and j. n = 200000. What is the true situation?",
    [
        "Prefix-min fusion works: keep min of dp[j] + b[j]",
        "The square entangles i and j (expands to a[i]² + 2·a[i]·b[j] + b[j]²); the cross term 2·a[i]·b[j] makes the best j depend on a[i] — a Li Chao/convex-hull structure, not a plain prefix min",
        "DP is impossible here; use Dijkstra",
        "Sort by a[i] + b[j] and take the first",
    ],
    "B",
    "Expanding the square exposes the entangled cross term: the optimal j depends on −2·a[i], which is exactly the line-query pattern (Li Chao tree / CHT). Plain prefix-min fusion would silently answer the wrong question.",
    vi_title="Chuyển tiếp béo",
    vi_scenario="dp[i] = min qua j < i của dp[j] + (a[i] + b[j])² — chú ý bình phương vắt qua cả i lẫn j. n = 200000. Tình huống thật là gì?",
    vi_options=[
        "Ghép tiền tố-min được: giữ min của dp[j] + b[j]",
        "Bình phương rối i và j (khai triển ra a[i]² + 2·a[i]·b[j] + b[j]²); số hạng chéo 2·a[i]·b[j] khiến j tốt nhất phụ thuộc a[i] — cần cấu trúc Li Chao/bao lồi, không phải tiền tố min thuần",
        "DP bất khả ở đây; dùng Dijkstra",
        "Sort theo a[i] + b[j] và lấy phần tử đầu",
    ],
    vi_hint="Khai triển bình phương lộ số hạng chéo rối: j tối ưu phụ thuộc −2·a[i], đúng mẫu truy vấn đường thẳng (Li Chao / CHT). Ghép tiền tố-min thuần sẽ trả lời lặng lẽ một câu hỏi sai.",
)

D3, D3VI = recognition_drill(
    "hsgm-p6-d3", "The Unbounded Dimension",
    "dp over 'number of operations used' blows up because operations can be 10^18. What is the standard repair?",
    [
        "Use long long and hope",
        "Flip the table: dp over 'value achieved' storing min operations — the value dimension is bounded",
        "Binary search the answer instead",
        "Drop the dimension; greedily apply operations",
    ],
    "B",
    "Complement-table flip: when one dimension is huge and its co-dimension is bounded, swap their roles. Classic in 'min operations to reach value' problems.",
    vi_title="Chiều vô biên",
    vi_scenario="DP theo 'số thao tác đã dùng' nổ vì thao tác có thể tới 10^18. Cách sửa chuẩn là gì?",
    vi_options=[
        "Dùng long long và hy vọng",
        "Lật bảng: DP theo 'giá trị đạt được' chứa số thao tác ít nhất — chiều giá trị là có biên",
        "Chặt nhị phân đáp án thay thế",
        "Bỏ chiều đó; greedy áp thao tác",
    ],
    vi_hint="Lật bảng bù: khi một chiều khổng lồ và chiều đối tác có biên, đổi vai cho nhau. Kinh điển trong các bài 'ít thao tác để đạt giá trị'.",
)

write_practice(
    M, "hsgm-p6-drills", "DP Synthesis Drills",
    "Three drills: minimal state design, the entangled-square trap, and the complement-table flip.",
    "Drill tổng hợp DP",
    "Ba drill: thiết kế trạng thái tối thiểu, bẫy bình phương rối, và lật bảng bù.",
    "hsgm-m6-fusion", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p6-d1": D1VI, "hsgm-p6-d2": D2VI, "hsgm-p6-d3": D3VI},
    solutions=[
        ("hsgm-p6-d1", letter("B"), letter("A")),
        ("hsgm-p6-d2", letter("B"), letter("A")),
        ("hsgm-p6-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: bounded jump DP with the windowed-min fusion (dp[i] = gain[i] +
# max dp[i-k..i-1], k up to n) at n = 200000. W: naive O(n·k) re-max.
# Python ground truth with monotonic deque.
from collections import deque as _dq


def _gt_window_gain(gain, k):
    n = len(gain)
    NEG = float("-inf")
    dp = [NEG] * n
    dq = _dq()  # indices, dp decreasing
    for i in range(n):
        best = 0 if i == 0 else NEG
        while dq and dq[0] < i - k:
            dq.popleft()
        if dq:
            best = dp[dq[0]]
        dp[i] = gain[i] + (best if best != NEG else 0)
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
    return dp[n - 1]


_gain = [(i * 911) % 100003 - 50000 for i in range(1, 21)]
_k = 3
_v1 = _gt_window_gain(_gain, _k)

# small-case cross-check vs brute
def _brutewin(gain, k):
    n = len(gain)
    dp = [float("-inf")] * n
    dp[0] = gain[0]
    for i in range(1, n):
        dp[i] = gain[i] + max(dp[max(0, i - k):i])
    return dp[n - 1]


assert _v1 == _brutewin(_gain, _k), (_v1, _brutewin(_gain, _k))

_n6 = 200000
_k6 = 2000
_gain6 = [(i * 911) % 100003 - 50000 for i in range(1, _n6 + 1)]
_cp6 = _gt_window_gain(_gain6, _k6)

CP_M6_IN = T(str(_n6), str(_k6), " ".join(map(str, _gain6)))
CP_M6_WANT = T(str(_cp6))

CP6C = challenge(
    "hsgm-cp-m6-window",
    "Checkpoint: The Widest Window",
    """**Task.** Stand on cell 1 of a strip of n cells; cell i has value
g_i (may be negative). Repeatedly jump forward at most k cells (from i to
i+1..i+k); each landing cell adds its value. Maximize the total collected
when you reach cell n (you must end exactly there). Print the maximum.

**Constraints:** 2 ≤ n ≤ 200000; 1 ≤ k ≤ min(2000, n−1); −50000 ≤ g_i ≤
50000. Totals reach ~10^10 — 64-bit.

**Budget check:** the dp[i] = g_i + max(dp[i−k..i−1]) recurrence is
O(n·k) = 4·10^8 naive — risky; the fused window-min is O(n).
""",
    [
        contest_test("small walk", T("5", "2", "3 -1 4 -2 5"), T("11",
            ), "Path 1→3→5: 3+4+5 = 12? Recompute: land on 1 (g=3), jump 2 to g=4, jump 2 to g=5 → 12... trust the checked value."),
    ],
    level="combination",
    difficulty="advanced",
)
CP6C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("small walk", T("5", "2", "3 -1 4 -2 5"), T("12"),
            "Land 1 (3), jump 2 → cell 3 (4), jump 2 → cell 5 (5): 12."),
        contest_test("k covers all", T("4", "3", "1 2 3 4"), T("10"),
            "k = 3 lets path 1→2→3→4 land on every cell: 1+2+3+4 = 10. (The full-distance 1→4 jump is exactly what the off-by-one window loses.)"),
        contest_test("starved window", T("3", "1", "2 -1 2"), T("3"),
            "Path 1→3 (a distance-2 jump, k = 1 means... no: k = 1 allows only distance 1; path 1→2→3 = 2−1+2 = 3. With k = 1 the off-by-one window can reach nothing at i = 2 → garbage."),
        contest_test("full scale", CP_M6_IN, CP_M6_WANT,
            "n = 200000, k = 2000: naive O(n·k) re-max is 4·10^8 — the fused monotonic-deque sweep is O(n). Ground truth computed in Python with the same recurrence."),
    )
]

CP6VI = vi_challenge(
    "Điểm kiểm tra: cửa sổ rộng nhất",
    """**Bài toán.** Đứng ở ô 1 trên dải n ô; ô i có giá trị g_i (có thể âm).
Nhảy tiến tối đa k ô mỗi lần (từ i tới i+1..i+k); mỗi ô đáp xuống cộng giá
trị của nó. Tối đa hóa tổng thu khi tới ô n (phải kết thúc đúng ở đó). In
tối đa.

**Ràng buộc:** 2 ≤ n ≤ 200000; 1 ≤ k ≤ min(2000, n−1); −50000 ≤ g_i ≤
50000. Tổng tới ~10^10 — 64-bit.

**Kiểm tra ngân sách:** truy hồi dp[i] = g_i + max(dp[i−k..i−1]) là
O(n·k) = 4·10^8 naive — rủi ro; ghép cửa-sổ-min là O(n).
""",
    [("đi nhỏ", "Đáp 1 (3), nhảy 2 → ô 3 (4), nhảy 2 → ô 5 (5): 12."),
     ("k phủ hết", "Giá trị quét-xác-minh: 10 nghĩa là đường 1→2→3→4 thu hết mọi ô."),
     ("đúng giới hạn", "n = 200000, k = 2000: naive O(n·k) là 4·10^8 — quét deque đơn điệu ghép là O(n).")],
)

CP_M6_R = CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> g(n + 1), dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) in >> g[i];
    deque<int> dq;                 // indices with dp decreasing
    dp[1] = g[1];
    dq.push_back(1);
    for (int i = 2; i <= n; ++i) {
        while (!dq.empty() && dq.front() < i - k) dq.pop_front();
        dp[i] = g[i] + dp[dq.front()];
        while (!dq.empty() && dp[dq.back()] <= dp[i]) dq.pop_back();
        dq.push_back(i);
    }
    out << dp[n] << "{{NL}}";
""") + END

CP_M6_W = CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> g(n + 1), dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) in >> g[i];
    // WRONG: off-by-one window — treats jumps as at most k−1 cells
    // (scans [i−k+1, i−1] instead of [i−k, i−1]). On chains whose optimal
    // path uses a full k-distance jump the answer collapses, and when no
    // positive cell is reachable within the shrunken window it underflows
    // to garbage.
    dp[1] = g[1];
    for (int i = 2; i <= n; ++i) {
        long long best = LLONG_MIN;
        for (int j = max(1, i - k + 1); j < i; ++j) best = max(best, dp[j]);
        dp[i] = g[i] + best;
    }
    out << dp[n] << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m6", "Checkpoint — Fuse the Window",
    "Bounded-jump collection: the recurrence is easy, surviving n = 200000 with k = 2000 requires the monotonic-deque fusion. The W re-scans its window and dies on budget.",
    25,
    """
**Checkpoint — Fuse the Window.** dp[i] = g_i + max over the last k dp
values is correct on paper; the naive loop is O(n·k) ≈ 4·10^8 and fails
the budget. The fused monotonic deque answers every window-max in
amortized O(1): O(n) total. The W is *algorithmically correct* — it fails
because its complexity family is wrong. That is the mastery point:
correctness and survivability are separate theorems.
""",
    "Điểm kiểm tra — Ghép cửa sổ",
    "Thu thập nhảy-có-chặn: truy hồi dễ, sống sót qua n = 200000 với k = 2000 cần ghép deque đơn điệu. W quét lại cửa sổ và chết vì ngân sách.",
    """
**Điểm kiểm tra — Ghép cửa sổ.** dp[i] = g_i + max trên k giá trị dp cuối
đúng trên giấy; vòng lặp naive là O(n·k) ≈ 4·10^8 và phá ngân sách. Deque
đơn điệu ghép trả mỗi max-cửa-sổ trong O(1) khấu trừ: tổng O(n). W *đúng
thuật toán* — nó thất bại vì họ độ phức tạp sai. Đó là điểm của bậc thầy:
tính đúng đắn và khả năng sống sót là hai định lý riêng biệt.
""",
    CP6C,
    CP6VI,
    CP_M6_R,
    CP_M6_W,
)

print("module m6 complete")
