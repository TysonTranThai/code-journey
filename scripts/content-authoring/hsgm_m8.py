#!/usr/bin/env python3
"""HSG Mastery — Module 8: hsgm-offline (Offline & Query Synthesis).

Reading all queries before answering: sorting queries to unlock sweeps,
processing events in the right order, and contribution counting.
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


M = "hsgm-offline"
write_module(
    M,
    "Offline and Query Synthesis",
    "The offline superpower: read everything, sort events, sweep once. Turning q independent questions into one ordered pass, and counting contributions instead of configurations.",
    "Tổng hợp offline và truy vấn",
    "Sức mạnh offline: đọc hết, sort sự kiện, quét một lần. Biến q câu hỏi độc lập thành một lượt có thứ tự, và đếm đóng góp thay vì đếm cấu hình.",
    ["hsgm-m8-sweep", "hsgm-m8-contribute", "hsgm-cp-m8"],
    ["hsgm-p8-drills"],
)

write_lesson(
    M, "hsgm-m8-sweep",
    "Sort the Events, Sweep Once",
    "Most query batches hide an ordering that makes one pass answer everything.",
    13,
    """
# Sort the Events, Sweep Once

If all queries are known in advance (offline!), you are free to **reorder
the world**. The pattern:

1. **Convert to events.** Every interval becomes (position, ±delta); every
   query becomes a marked position; every update becomes a timestamped
   event.
2. **Sort events by the axis that governs causality** — time, coordinate,
   or threshold.
3. **Sweep once**, maintaining a running structure (counter, multiset,
   Fenwick). Answer each query when the sweep reaches its mark.

## The classic conversion

"How many intervals [l, r] contain point p?" for many p: events (l, +1),
(r+1, −1) sorted by position; the running sum at p is the answer for that
p. Each interval costs O(1) to register, each query O(1) to read:
O((n + q) log(n + q)) for the sort, and the log is usually unavoidable
only because of sorting.

## Online vs offline

Online = must answer before seeing the next query (forces heavier
structures). Offline = may batch and reorder (lighter structures win).
When a problem does not demand online behavior, choosing an online
structure is self-inflicted complexity. Ask early: **do the answers
interact, or can I reorder?**
""",
    "Sort sự kiện, quét một lần",
    "Phần lớn lô truy vấn giấu một thứ tự khiến một lượt trả lời hết.",
    """
# Sort sự kiện, quét một lần

Nếu mọi truy vấn đều biết trước (offline!), bạn được quyền **sắp lại thế
giới**. Mẫu hình:

1. **Chuyển thành sự kiện.** Mỗi đoạn thành (vị trí, ±delta); mỗi truy vấn
   thành một vị trí có đánh dấu; mỗi cập nhật thành sự kiện có dấu thời gian.
2. **Sort sự kiện theo trục chi phối quan hệ nhân quả** — thời gian, tọa
   độ, hoặc ngưỡng.
3. **Quét một lần**, giữ một cấu trúc chạy (bộ đếm, multiset, Fenwick).
   Trả lời mỗi truy vấn khi lượt quét chạm dấu của nó.

## Phép chuyển kinh điển

"Máy đoạn [l, r] chứa điểm p?" với nhiều p: sự kiện (l, +1), (r+1, −1)
sort theo vị trí; tổng chạy tại p là đáp án của p đó. Mỗi đoạn tốn O(1)
để đăng ký, mỗi truy vấn O(1) để đọc: O((n + q) log(n + q)) cho phép sort,
và cái log thường bất khả kháng chỉ vì có sort.

## Online vs offline

Online = phải trả lời trước khi thấy truy vấn kế (ép dùng cấu trúc nặng).
Offline = được gộp và sắp lại (cấu trúc nhẹ thắng). Khi đề không đòi hỏi
online, chọn cấu trúc online là tự gây độ phức tạp cho chính mình. Hỏi
sớm: **các đáp án có tương tác không, hay tôi sắp lại được?**
""",
)

write_lesson(
    M, "hsgm-m8-contribute",
    "Count Contributions, Not Configurations",
    "Flip the loop: for each element, ask where it participates — one pass instead of enumerating every answer.",
    14,
    """
# Count Contributions, Not Configurations

"Sum over all pairs/subsets/positions of f(chosen set)" screams
enumeration — but usually decomposes into **per-element contributions**:

    Σ_sets f(S) = Σ_element e (contribution of e to every set containing it)

## The canonical pair-sum flip

Sum of min(a_i, a_j) over all pairs i < j, n = 200000. Enumerating pairs
is 2·10^10 — dead. Flip: sort; element at sorted index k (0-based) is the
min for exactly k pairs (with each smaller element): its contribution is
a[k]·k. One sort, one loop: O(n log n).

## The same flip everywhere

- Counting pairs with difference ≥ d: sort, two pointers, count per element.
- Sum over all subarrays of the max: monotonic stack finds the span where
  each element is the max — contribution = value × span.
- Expected value over random subsets: linearity of expectation is the
  probabilistic version of the same idea.

## When the flip is illegal

Contributions must be **independent**: if f(S) is not additive/separable
over elements (e.g., f = "1 if S has even size" interacts with the count,
not the values), a naive contribution split double-counts or misses. Check
separability before flipping — that check *is* the problem's difficulty.
""",
    "Đếm đóng góp, không đếm cấu hình",
    "Lật vòng lặp: với mỗi phần tử, hỏi nó tham gia ở đâu — một lượt thay vì liệt kê mọi đáp án.",
    """
# Đếm đóng góp, không đếm cấu hình

"Tổng trên mọi cặp/tập con/vị trí của f(bộ đã chọn)" gào lên sự liệt kê —
nhưng thường phân rã thành **đóng góp theo từng phần tử**:

    Σ_tập f(S) = Σ_phần tử e (đóng góp của e vào mọi tập chứa nó)

## Phép lật tổng-cặp kinh điển

Tổng min(a_i, a_j) trên mọi cặp i < j, n = 200000. Liệt kê cặp là
2·10^10 — chết. Lật: sort; phần tử ở chỉ số k (0-based) là min cho đúng k
cặp (với mỗi phần tử nhỏ hơn): đóng góp của nó là a[k]·k. Một sort, một
vòng lặp: O(n log n).

## Cùng một phép lật ở khắp nơi

- Đếm cặp chênh lệch ≥ d: sort, two pointers, đếm theo từng phần tử.
- Tổng trên mọi mảng con của max: stack đơn điệu tìm vùng mà mỗi phần tử
  là max — đóng góp = giá trị × độ dài vùng.
- Kỳ vọng trên tập con ngẫu nhiên: tính tuyến tính của kỳ vọng chính là
  phiên bản xác suất của cùng ý tưởng.

## Khi phép lật bất hợp lệ

Các đóng góp phải **độc lập**: nếu f(S) không cộng tính/tách được theo
phần tử (ví dụ f = "1 nếu |S| chẵn" tương tác với số lượng, không phải
giá trị), phép tách đóng góp naive sẽ đếm đôi hoặc bỏ sót. Kiểm tra tính
tách trước khi lật — chính phép kiểm tra đó là độ khó của bài.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p8-d1", "The Batch of Asks",
    "q ≤ 200000 queries: 'how many of the n given intervals contain point p?' No updates. What is the intended structure?",
    [
        "A segment tree over coordinates storing interval counts",
        "Offline sweep: +1 at each l, −1 at each r+1, sort, running sum answers each p in order",
        "For each query, loop over all intervals",
        "A balanced BST of interval endpoints",
    ],
    "B",
    "Pure offline counting: event sweep with a running sum. A segment tree works but is a heavier tool than needed (no updates between independent asks).",
    vi_title="Lô câu hỏi",
    vi_scenario="q ≤ 200000 truy vấn: 'n đoạn đã cho chứa điểm p?' Không có cập nhật. Cấu trúc chủ đích là gì?",
    vi_options=[
        "Segment tree trên tọa độ chứa số đoạn",
        "Quét offline: +1 tại mỗi l, −1 tại mỗi r+1, sort, tổng chạy trả mỗi p theo thứ tự",
        "Với mỗi truy vấn, duyệt qua mọi đoạn",
        "BST cân bằng các đầu mút đoạn",
    ],
    vi_hint="Đếm offline thuần: quét sự kiện với tổng chạy. Segment tree cũng được nhưng là công cụ nặng hơn cần thiết (không có cập nhật giữa các câu hỏi độc lập).",
)

D2, D2VI = recognition_drill(
    "hsgm-p8-d2", "The Pair Sum Flip",
    "Sum of max(a_i, a_j) over all pairs i < j, n = 200000, values up to 10^9. What is the key insight?",
    [
        "Sort descending; the element at sorted index k is the max for exactly k pairs, contributing a[k]·k",
        "Use a Fenwick tree over values while inserting elements one by one",
        "Divide and conquer on the value range",
        "The sum is (Σa)²/2 — a pure formula",
    ],
    "A",
    "Contribution counting after sorting: each element is the pair-max with exactly the elements before it. (Fenwick works but re-derives the same counting the hard way.)",
    vi_title="Phép lật tổng cặp",
    vi_scenario="Tổng max(a_i, a_j) trên mọi cặp i < j, n = 200000, giá trị tới 10^9. Nhận xét then chốt là gì?",
    vi_options=[
        "Sort giảm dần; phần tử ở chỉ số k là max cho đúng k cặp, đóng góp a[k]·k",
        "Dùng Fenwick trên giá trị trong khi chèn từng phần tử",
        "Chia để trị trên dải giá trị",
        "Tổng là (Σa)²/2 — một công thức thuần",
    ],
    vi_hint="Đếm đóng góp sau khi sort: mỗi phần tử là max của cặp với đúng các phần tử trước nó. (Fenwick chạy được nhưng tái suy ra cùng phép đếm theo cách nặng hơn.)",
)

D3, D3VI = recognition_drill(
    "hsgm-p8-d3", "The Entangled Condition",
    "Count subsets S with (sum of S) divisible by 3 AND |S| even. Why does a per-element contribution flip fail here?",
    [
        "It doesn't fail — sums and parities are always separable",
        "The two conditions interact through the same elements: an element's effect on parity and on sum-mod-3 cannot be counted independently of the set's other members, so the joint condition resists a single per-element split",
        "Because 3 is prime",
        "Because subsets can be empty",
    ],
    "B",
    "Joint conditions on overlapping statistics (sum mod 3 × count mod 2) need a joint state DP (position × sum%3 × parity), not a separable contribution flip. Knowing when NOT to flip is the skill.",
    vi_title="Điều kiện rối",
    vi_scenario="Đếm tập con S có (tổng của S) chia hết cho 3 VÀ |S| chẵn. Vì sao phép lật đóng góp theo phần tử thất bại ở đây?",
    vi_options=[
        "Nó không thất bại — tổng và tính chẵn luôn tách được",
        "Hai điều kiện tương tác qua cùng các phần tử: tác động của một phần tử lên parity và lên tổng-mod-3 không thể đếm độc lập với các thành viên khác của tập, nên điều kiện kép kháng lại phép tách theo phần tử",
        "Vì 3 là số nguyên tố",
        "Vì tập con có thể rỗng",
    ],
    vi_hint="Điều kiện kép trên các thống kê chồng lấn (tổng mod 3 × count mod 2) cần DP trạng thái ghép (vị trí × tổng%3 × parity), không phải phép lật đóng góp tách được. Biết khi nào KHÔNG lật chính là kỹ năng.",
)

write_practice(
    M, "hsgm-p8-drills", "Offline Synthesis Drills",
    "Three drills: the event sweep, the sorted contribution flip, and when contribution counting is illegal.",
    "Drill tổng hợp offline",
    "Ba drill: quét sự kiện, phép lật đóng góp sau sort, và khi nào đếm đóng góp bất hợp lệ.",
    "hsgm-m8-contribute", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p8-d1": D1VI, "hsgm-p8-d2": D2VI, "hsgm-p8-d3": D3VI},
    solutions=[
        ("hsgm-p8-d1", letter("B"), letter("A")),
        ("hsgm-p8-d2", letter("A"), letter("B")),
        ("hsgm-p8-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: maximum number of simultaneous intervals (max overlap) at scale
# — events sweep. W: sorts by interval START and greedily closes on END
# without the +1/−1 delta discipline (it decrements coverage at r instead of
# r+1 for closed intervals [l, r] — the touching-intervals off-by-one that
# the M3 lesson flagged; here it changes the answer when intervals share
# endpoints).
def _gt_max_overlap(ivs):
    events = []
    for l, r in ivs:
        events.append((l, 1))
        events.append((r + 1, -1))  # [l, r] closed: coverage ends after r
    events.sort()
    cur = mx = 0
    for _, d in events:
        cur += d
        mx = max(mx, cur)
    return mx


_iv8 = [
    [(1, 3), (2, 5), (4, 7)],
    [(1, 10), (2, 3), (4, 5), (6, 7), (8, 9)],
    [(1, 1), (1, 1), (1, 1)],
    [(5, 7), (1, 2), (3, 4), (1, 9), (2, 8), (6, 10), (1, 3), (4, 6), (7, 9), (2, 5)],
    [(1, 4), (4, 8), (8, 12)],  # touching at endpoints — the delta discipline shows
    [(1, 100)],
    [(1, 2), (1, 2), (1, 2), (2, 3), (2, 3), (3, 4), (3, 4), (3, 4)],
    [(1000000000 - 5, 1000000000), (1000000000 - 3, 1000000000), (1, 2)],
]
_ans8 = [_gt_max_overlap(p) for p in _iv8]

# W simulation: sort by start; sweep endpoints but decrement at r (not r+1)
# and count max AFTER processing each event — this mis-orders ties at the
# same coordinate (should process −1 before +1 at shared endpoint for closed
# intervals ending exactly where others start: coverage is NOT simultaneous).
def _w_max_overlap(ivs):
    events = []
    for l, r in ivs:
        events.append((l, 1))
        events.append((r, -1))  # BUG: decrement AT r
    events.sort()
    cur = mx = 0
    for _, d in events:
        cur += d
        mx = max(mx, cur)
    return mx


_w8 = [_w_max_overlap(p) for p in _iv8]
assert any(w != a for w, a in zip(_w8, _ans8)), (_w8, _ans8)  # W must diverge

_n8 = 200000
_ivs8 = []
_x = 1
for i in range(_n8):
    l = (i * 7919) % 900000 + 1
    length = (i * 4517) % 50000 + 1
    _ivs8.append((l, l + length))
_cp8 = _gt_max_overlap(_ivs8)

CP_M8_IN = T(str(_n8), *[f"{l} {r}" for (l, r) in _ivs8])
CP_M8_WANT = T(str(_cp8))

CP8C = challenge(
    "hsgm-cp-m8-overlap",
    "Checkpoint: The Busiest Moment",
    """**Task.** n intervals [l, r] with integer endpoints (1 ≤ l ≤ r ≤ 10^9).
The intervals are closed: [1,3] and [3,5] both contain point 3. Print the
maximum number of intervals sharing a single point.

**Constraints:** 1 ≤ n ≤ 200000.

**Budget check:** one sort of 2n events plus one sweep: O(n log n). Any
per-point probing of the coordinate space is a wrong family (coordinates
reach 10^9).
""",
    [
        contest_test("basic overlap", T("3", "1 3", "2 5", "4 7"), T("2"),
            "Points 2–3 sit in two intervals; no point sits in three."),
        contest_test("touching chain", T("3", "1 4", "4 8", "8 12"), T("1",
            ), "Closed intervals [1,4] and [4,8] share point 4 → 2. Careful with the delta discipline."),
    ],
    level="combination",
    difficulty="advanced",
)
CP8C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("basic overlap", T("3", "1 3", "2 5", "4 7"), T("2"),
            "Points 2–3 sit in two intervals; no point sits in three."),
        contest_test("touching chain", T("3", "1 4", "4 8", "8 12"), T("2"),
            "Closed intervals [1,4] and [4,8] share point 4 → 2; [8,12] joins at 8 → max 2."),
        contest_test("stacked identical", T("3", "1 1", "1 1", "1 1"), T("3"),
            "Three identical single-point intervals → 3."),
        contest_test("full scale", CP_M8_IN, CP_M8_WANT,
            "n = 200000 random intervals: the sweep with +1 at l and −1 at r+1 (closed-interval discipline) is O(n log n). Ground truth computed in Python."),
    )
]

CP8VI = vi_challenge(
    "Điểm kiểm tra: khoảnh khắc đông nhất",
    """**Bài toán.** n đoạn [l, r] với đầu mút nguyên (1 ≤ l ≤ r ≤ 10^9). Các
đoạn là đóng: [1,3] và [3,5] đều chứa điểm 3. In số đoạn tối đa cùng chia
sẻ một điểm.

**Ràng buộc:** 1 ≤ n ≤ 200000.

**Kiểm tra ngân sách:** một sort 2n sự kiện cộng một lần quét: O(n log n).
Bất kỳ cách dò từng điểm nào trên không gian tọa độ đều là họ sai (tọa độ
tới 10^9).
""",
    [("chồng cơ bản", "Điểm 2–3 nằm trong hai đoạn; không điểm nào nằm trong ba đoạn."),
     ("chuỗi chạm", "Đoạn đóng [1,4] và [4,8] cùng chứa điểm 4 → 2; [8,12] tham gia tại 8 → max 2."),
     ("xếp chồng identical", "Ba đoạn trùng nhau một điểm → 3."),
     ("đúng giới hạn", "n = 200000 đoạn ngẫu nhiên: quét với +1 tại l và −1 tại r+1 (kỷ luật đoạn đóng) là O(n log n).")],
)

CP_M8_R = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        ev.push_back({r + 1, -1});   // closed interval: coverage dies after r
    }
    sort(ev.begin(), ev.end(), [](auto& a, auto& b) {
        if (a.first != b.first) return a.first < b.first;
        return a.second < b.second;  // at ties, −1 first (points shared end/start)
    });
    long long cur = 0, mx = 0;
    for (auto& [pos, d] : ev) {
        cur += d;
        mx = max(mx, cur);
    }
    out << mx << "{{NL}}";
""") + END

CP_M8_W = CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long, int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        // WRONG: decrements AT r instead of r+1, and processes +1 before −1
        // at equal coordinates. For closed intervals this undercounts the
        // shared endpoints ([1,4],[4,8] should both cover 4) and shifts
        // every boundary one unit early.
        ev.push_back({r, -1});
    }
    sort(ev.begin(), ev.end());
    long long cur = 0, mx = 0;
    for (auto& [pos, d] : ev) {
        cur += d;
        mx = max(mx, cur);
    }
    out << mx << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m8", "Checkpoint — The Sweep Discipline",
    "Max simultaneous closed intervals: +1 at l, −1 at r+1, ties resolved −1-first. The W decrements at r and mis-orders ties — every shared endpoint undercounts.",
    25,
    """
**Checkpoint — The Sweep Discipline.** Closed intervals make the delta
placement a real theorem: coverage of [l, r] means +1 at l and −1 at r+1,
and at a shared coordinate the −1 must process before the +1 (an interval
ending at x stops covering x the instant another begins there — both
cover x, so order ties as −1 first to count the junction correctly).
The W decrements at r and sorts +1/−1 naively: plausible, clean code,
wrong at every junction point.
""",
    "Điểm kiểm tra — Kỷ luật quét",
    "Số đoạn đóng đồng thời nhiều nhất: +1 tại l, −1 tại r+1, hòa giải bằng −1-trước. W trừ tại r và sai thứ tự hòa — mọi điểm giáp ranh đều bị đếm thiếu.",
    """
**Điểm kiểm tra — Kỷ luật quét.** Đoạn đóng biến vị trí delta thành một
định lý thật: phủ của [l, r] nghĩa là +1 tại l và −1 tại r+1, và tại một
tọa độ chung, −1 phải xử lý trước +1 (đoạn kết thúc tại x ngừng phủ x đúng
lúc đoạn khác bắt đầu tại đó — cả hai cùng phủ x, nên xếp hòa −1 trước để
đếm đúng điểm giáp ranh). W trừ tại r và sort +1/−1 ngây thơ: code sạch,
trông hợp lý, sai ở mọi điểm giáp ranh.
""",
    CP8C,
    CP8VI,
    CP_M8_R,
    CP_M8_W,
)

print("module m8 complete")
