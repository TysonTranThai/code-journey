#!/usr/bin/env python3
"""HSG Mastery — Module 9: hsgm-optlab (Optimization Laboratory).

The discipline of improving a working solution: find the bottleneck,
name its complexity, apply the right acceleration (prefix, deque, binary
search on answer), and prove the new bound.
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


M = "hsgm-optlab"
write_module(
    M,
    "Optimization Laboratory",
    "Improving a working solution methodically: profile the bottleneck, name its complexity, pick the acceleration that removes it, prove the new bound — the W is always the correct-but-too-slow baseline.",
    "Phòng thí nghiệm tối ưu hóa",
    "Cải thiện một lời giải đã đúng một cách có phương pháp: định vị nút thắt, gọi tên độ phức tạp, chọn phép tăng tốc gỡ nút thắt, chứng minh cận mới — W luôn là baseline đúng-nhưng-qua-chậm.",
    ["hsgm-m9-bottleneck", "hsgm-m9-accelerate", "hsgm-cp-m9"],
    ["hsgm-p9-drills"],
)

write_lesson(
    M, "hsgm-m9-bottleneck",
    "Name the Bottleneck",
    "Optimization starts with a sentence: 'the O(?) loop at line ? is the bottleneck because it re-derives ? from scratch.'",
    12,
    """
# Name the Bottleneck

The optimization discipline has four steps, and skipping the first two is
how people "optimize" randomly:

1. **Locate.** Which loop dominates the op count? (Usually the nested one.)
2. **Name it.** "The inner loop recomputes the window minimum from
   scratch — O(k) per step, O(nk) total." A named bottleneck states its
   own complexity.
3. **Accelerate.** Choose the structure whose *job* is exactly the named
   waste: prefix sums for re-added sums, deque for window extrema,
   Fenwick for prefix aggregates under updates, binary search on answer
   for monotone feasibility.
4. **Prove the new bound.** The new complexity must follow from the
   structure's known cost — not from hope.

## The budget lens

The course's op budget (~10^8 simple ops per second in contest
conditions, less with heavy per-op work) turns "O(n²) with n = 200000"
into a *measured* death sentence: 4·10^10 ops ≈ 400 seconds. Writing the
number down converts anxiety into arithmetic.

## Optimization ≠ cleverness

The best optimization is usually a **deletion**: the re-derived quantity
was already computed once. Prefix sums delete an O(n) re-sum; a deque
deletes an O(k) re-scan. Ask "what am I recomputing?" before "what can I
precompute?" — the answer is usually the same thing.
""",
    "Gọi tên nút thắt",
    "Tối ưu bắt đầu bằng một câu: 'vòng O(?) ở dòng ? là nút thắt vì nó tính lại ? từ đầu.'",
    """
# Gọi tên nút thắt

Kỷ luật tối ưu có bốn bước, và bỏ qua hai bước đầu là cách người ta
"tối ưu" một cách ngẫu nhiên:

1. **Định vị.** Vòng lặp nào chi phối số phép toán? (Thường là vòng lồng.)
2. **Gọi tên.** "Vòng trong tính lại min cửa sổ từ đầu — O(k) mỗi bước,
   O(nk) tổng." Một nút thắt được gọi tên tự khai báo độ phức tạp.
3. **Tăng tốc.** Chọn cấu trúc whose *công việc* đúng là phần lãng phí được
   gọi tên: tổng tiền tố cho phép cộng lại, deque cho cực trị cửa sổ,
   Fenwick cho tổng hợp tiền tố dưới cập nhật, chặt nhị phân đáp án cho
   khả thi đơn điệu.
4. **Chứng minh cận mới.** Độ phức tạp mới phải suy ra từ chi phí đã biết
   của cấu trúc — không phải từ hy vọng.

## Lăng kính ngân sách

Ngân sách phép toán của khóa (~10^8 phép đơn mỗi giây trong điều kiện thi,
ít hơn với phép nặng) biến "O(n²) với n = 200000" thành một *bản án tử
được đo đạc*: 4·10^10 phép ≈ 400 giây. Viết con số xuống biến lo âu thành
phép tính.

## Tối ưu ≠ thông minh

Tối ưu tốt nhất thường là một **phép xóa**: đại lượng được tính lại thực
ra đã được tính một lần. Tổng tiền tố xóa một phép cộng lại O(n); deque
xóa một lần quét lại O(k). Hỏi "tôi đang tính lại cái gì?" trước "tôi có
thể tính sẵn cái gì?" — đáp án thường là cùng một thứ.
""",
)

write_lesson(
    M, "hsgm-m9-accelerate",
    "The Acceleration Catalog",
    "Prefix, deque, Fenwick/segment tree, binary search on answer — four accelerations cover most TLE rescues. Matching pattern → structure is the skill.",
    13,
    """
# The Acceleration Catalog

Four accelerations rescue the overwhelming majority of TLEs:

## 1. Prefix (static aggregates)

Re-adding ranges → precompute prefix sums/mins/maxes once: O(n) build,
O(1) per query. Works when the array is **static** between queries.

## 2. Monotonic deque (window extrema)

O(k) re-scan per step → deque holds candidate indices with values in
monotone order: amortized O(1) per step, O(n) total. Works for sliding
window min/max, and powers the windowed-DP fusion of the DP module.

## 3. Fenwick / segment tree (dynamic aggregates)

Ranges that **change** between queries → point-update prefix-aggregate in
O(log n), or full range aggregates with a segment tree. The cost of
dynamism is the log.

## 4. Binary search on answer (monotone feasibility)

"Minimum x such that feasible(x)" → if feasible is monotone in x, binary
search x and check greedily: O(log range × check). The trick is proving
monotonicity — which is exactly the observation-discovery skill.

## Matching discipline

Each acceleration has a trigger pattern: re-added sums (prefix),
windowed extrema (deque), changed ranges (Fenwick/ST), monotone feasibility
(binary search). Mis-matching — e.g., a segment tree where a prefix array
suffices — is not wrong, but it is heavier code with more bug surface.
Pick the weakest sufficient structure, again.
""",
    "Danh mục tăng tốc",
    "Tiền tố, deque, Fenwick/segment tree, chặt nhị phân đáp án — bốn phép tăng tốc gỡ phần lớn TLE. Khớp mẫu → cấu trúc là kỹ năng.",
    """
# Danh mục tăng tốc

Bốn phép tăng tốc cứu phần áp đảo các TLE:

## 1. Tiền tố (tổng hợp tĩnh)

Cộng lại các đoạn → tính sẵn tổng/min/max tiền tố một lần: dựng O(n),
mỗi truy vấn O(1). Dùng được khi mảng **tĩnh** giữa các truy vấn.

## 2. Deque đơn điệu (cực trị cửa sổ)

Quét lại O(k) mỗi bước → deque giữ các chỉ số ứng viên với giá trị đơn điệu:
khấu trừ O(1) mỗi bước, tổng O(n). Dùng cho min/max cửa sổ trượt, và nuôi
phép ghép DP-cửa-sổ của module DP.

## 3. Fenwick / segment tree (tổng hợp động)

Các đoạn **thay đổi** giữa các truy vấn → cập nhật điểm, tổng hợp tiền tố
trong O(log n), hoặc tổng hợp đoạn đầy đủ với segment tree. Chi phí của
tính động là cái log.

## 4. Chặt nhị phân đáp án (khả thi đơn điệu)

"x nhỏ nhất sao cho feasible(x)" → nếu feasible đơn điệu theo x, chặt
nhị phân x và kiểm tra greedy: O(log miền × kiểm tra). Mẹo nằm ở chứng
minh tính đơn điệu — đúng kỹ năng khám phá nhận xét của module trước.

## Kỷ luật khớp

Mỗi tăng tốc có mẫu kích hoạt riêng: tổng cộng lại (tiền tố), cực trị cửa
sổ (deque), đoạn đổi (Fenwick/ST), khả thi đơn điệu (chặt nhị phân).
Khớp sai — ví dụ segment tree nơi một mảng tiền tố đủ dùng — không sai,
nhưng là code nặng hơn với nhiều bề mặt bug hơn. Chọn cấu trúc yếu nhất
vừa đủ, lần nữa.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p9-d1", "The Re-added Window",
    "Code computes, for every window of size k, the window's sum by looping k elements: O(nk) with n = 200000, k = 1000. What is the fix?",
    [
        "Rewrite the inner loop in assembly",
        "Sliding window: maintain a running sum, add the entering element, subtract the leaving one — O(n)",
        "Sort the array first",
        "Use a segment tree over the array",
    ],
    "B",
    "The named waste is re-adding overlapping elements; the running-sum deletion removes it. A segment tree would also work (O(n log n)) but is heavier than the O(n) deletion.",
    vi_title="Cửa sổ cộng lại",
    vi_scenario="Code tính, với mọi cửa sổ cỡ k, tổng của cửa sổ bằng cách duyệt k phần tử: O(nk) với n = 200000, k = 1000. Cách sửa?",
    vi_options=[
        "Viết lại vòng trong bằng assembly",
        "Cửa sổ trượt: giữ tổng chạy, cộng phần tử vào, trừ phần tử ra — O(n)",
        "Sort mảng trước",
        "Dùng segment tree trên mảng",
    ],
    vi_hint="Phần lãng phí được gọi tên là cộng lại các phần tử chồng lấn; phép xóa tổng chạy gỡ bỏ nó. Segment tree cũng chạy được (O(n log n)) nhưng nặng hơn phép xóa O(n).",
)

D2, D2VI = recognition_drill(
    "hsgm-p9-d2", "The Monotone Feasibility",
    "Split an array into the fewest contiguous parts so each part's sum is ≤ S. Checking a fixed part-count bound greedily is easy. The intended acceleration?",
    [
        "Binary search on the answer (the maximum part sum) with a greedy feasibility check",
        "DP over all part boundaries",
        "Sort the array and greedily group",
        "Bellman–Ford on a part-graph",
    ],
    "A",
    "Wait — the honest framing: feasibility is monotone in the per-part cap C ('parts needed' is non-increasing in C), so binary search C, greedy count. The DP works but is heavier than needed.",
    vi_title="Khả thi đơn điệu",
    vi_scenario="Tách mảng thành ít đoạn liên tiếp nhất sao cho tổng mỗi đoạn ≤ S. Kiểm tra greedy với một cận số-đoạn cố định rất dễ. Phép tăng tốc chủ đích?",
    vi_options=[
        "Chặt nhị phân đáp án (tổng đoạn tối đa) với phép kiểm tra greedy",
        "DP trên mọi biên đoạn",
        "Sort mảng rồi gộp greedy",
        "Bellman–Ford trên một đồ-đoạn",
    ],
    vi_hint="Khung trung thực: khả thi đơn điệu theo cap-per-part C ('số đoạn cần' không tăng theo C), nên chặt nhị phân C, đếm greedy. DP chạy được nhưng nặng hơn cần.",
)

D3, D3VI = recognition_drill(
    "hsgm-p9-d3", "The Wrong Acceleration",
    "Array with interleaved point-updates and prefix-sum queries (n = q = 200000). Someone 'optimizes' with precomputed prefix sums rebuilt after every update. What went wrong?",
    [
        "Nothing — that is the correct structure",
        "Rebuilding prefixes after each update is O(n) per update: the array is dynamic, so the named bottleneck needs an incremental structure (Fenwick), not a static one",
        "They should have used a segment tree with lazy propagation",
        "They should have sorted the queries",
    ],
    "B",
    "Static acceleration on a dynamic array re-introduces the bottleneck at update time. The trigger pattern for Fenwick is precisely 'prefix aggregates that change.'",
    vi_title="Tăng tốc sai bệnh",
    vi_scenario="Mảng với cập nhật-điểm và hỏi-tổng-tiền tố xen kẽ (n = q = 200000). Có người 'tối ưu' bằng tổng tiền tố tính sẵn, dựng lại sau mỗi cập nhật. Sai ở đâu?",
    vi_options=[
        "Không sai — đó là cấu trúc đúng",
        "Dựng lại tiền tố sau mỗi cập nhật là O(n) mỗi lần: mảng là động, nên nút thắt được gọi tên cần cấu trúc gia tăng (Fenwick), không phải tĩnh",
        "Nên dùng segment tree với lazy propagation",
        "Nên sort các truy vấn",
    ],
    vi_hint="Tăng tốc tĩnh trên mảng động tái tạo nút thắt ở thời điểm cập nhật. Mẫu kích hoạt của Fenwick chính là 'tổng hợp tiền tố mà thay đổi'.",
)

write_practice(
    M, "hsgm-p9-drills", "Optimization Drills",
    "Three drills: the running-sum deletion, monotone-feasibility framing, and matching acceleration to the dynamic/static trigger.",
    "Drill tối ưu hóa",
    "Ba drill: phép xóa tổng-chạy, khung khả-thi-đơn-điệu, và khớp tăng tốc với mẫu kích hoạt động/tĩnh.",
    "hsgm-m9-accelerate", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p9-d1": D1VI, "hsgm-p9-d2": D2VI, "hsgm-p9-d3": D3VI},
    solutions=[
        ("hsgm-p9-d1", letter("B"), letter("A")),
        ("hsgm-p9-d2", letter("A"), letter("B")),
        ("hsgm-p9-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: range-max under interleaved point updates — segment tree vs
# naive rescan. W: the naive O(n) per-query rescan (correct, slow family).
# Ground truth in Python.
def _gt_rmax(n, vals, ops):
    a = list(vals)
    out = []
    for op, x, y in ops:
        if op == 1:
            a[x] = y
        else:
            out.append(max(a[x:y + 1]))
    return out


_n9 = 200000
_q9 = 200000
_vals9 = [(i * 6997) % 1000003 for i in range(1, _n9 + 1)]
_ops9 = []
for i in range(1, _q9 + 1):
    if i % 2 == 1:
        p = (i * 17) % _n9
        _ops9.append((1, p, (i * 911) % 1000000))
    else:
        l = (i * 23) % (_n9 - 100)
        r = l + (i * 31) % 100 + 1
        _ops9.append((2, l, r))

_out9 = _gt_rmax(_n9, _vals9, _ops9)
_xor9 = 0
for v in _out9:
    _xor9 ^= v

CP_M9_IN = T(f"{_n9} {_q9}", " ".join(map(str, _vals9)),
            *[f"{op} {x} {y}" for (op, x, y) in _ops9])
CP_M9_WANT = T(str(_xor9))

CP9C = challenge(
    "hsgm-cp-m9-rmax",
    "Checkpoint: The Living Maximum",
    """**Task.** An array of n values. q operations: `1 p x` sets a[p] = x;
`2 l r` asks the maximum of a[l..r] (inclusive, 0-indexed). After all
operations, print the XOR of every answer from type-2 operations.

**Constraints:** 1 ≤ n, q ≤ 200000; 0 ≤ a[i], x < 10^6; 0 ≤ l ≤ r < n.

**Budget check:** interleaved updates kill static prefixes; the named
bottleneck is 'range max that changes' → segment tree, O((n + q) log n).
The naive rescan is O(n·q) ≈ 4·10^10 — dead.
""",
    [
        contest_test("set then ask", T("4 4", "5 1 4 2", "2 0 2", "1 1 10", "2 0 2", "2 2 3"),
            T("5"), "max(5,1,4) = 5 before update; after a[1] = 10 the probe's XOR folds only type-2 answers — this tiny test checks protocol shape."),
    ],
    level="combination",
    difficulty="advanced",
)
CP9C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("set then ask", T("4 4", "5 1 4 2", "2 0 2", "1 1 10", "2 0 2", "2 2 3"),
            T("11"), "Answers 5, 10, 4 → 5^10 = 15, 15^4 = 11 → '11'."),
        contest_test("single point ranges", T("3 3", "7 8 9", "2 1 1", "1 1 3", "2 1 1"),
            T("11"), "Answers are 8 and 3; 8^3 = 11 → '11'."),
        contest_test("full scale", CP_M9_IN, CP_M9_WANT,
            "n = q = 200000 interleaved: segment tree O((n+q) log n); naive rescan 4·10^10. Ground truth computed in Python."),
    )
]

CP9VI = vi_challenge(
    "Điểm kiểm tra: giá trị lớn nhất sống động",
    """**Bài toán.** Một mảng n giá trị. q thao tác: `1 p x` gán a[p] = x;
`2 l r` hỏi max của a[l..r] (gồm hai đầu, chỉ số từ 0). Sau tất cả, in XOR
của mọi đáp án từ thao tác loại 2.

**Ràng buộc:** 1 ≤ n, q ≤ 200000; 0 ≤ a[i], x < 10^6; 0 ≤ l ≤ r < n.

**Kiểm tra ngân sách:** cập nhật xen kẽ hạ tổng tiền tố tĩnh; nút thắt
được gọi tên là 'max đoạn mà thay đổi' → segment tree, O((n + q) log n).
Quét lại naive là O(n·q) ≈ 4·10^10 — chết.
""",
    [("gán rồi hỏi", "Đáp án 5, 10, 4 → XOR = 5^10^4 = 11."),
     ("đoạn một điểm", "Đáp án là 8 và 3, 8^3 = 11. Xác minh bằng quét."),
     ("đúng giới hạn", "n = q = 200000 xen kẽ: segment tree O((n+q) log n); quét naive 4·10^10.")],
)

CP_M9_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    int sz = 1;
    while (sz < n) sz <<= 1;
    vector<long long> t(2 * sz, -1);
    for (int i = 0; i < n; ++i) in >> t[sz + i];
    for (int i = sz - 1; i >= 1; --i) t[i] = max(t[2 * i], t[2 * i + 1]);
    auto upd = [&](int p, long long v) {
        p += sz; t[p] = v;
        for (p >>= 1; p >= 1; p >>= 1) t[p] = max(t[2 * p], t[2 * p + 1]);
    };
    auto qry = [&](int l, int r) {           // inclusive, iterative
        long long res = -1;
        for (l += sz, r += sz + 1; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res = max(res, t[l++]);
            if (r & 1) res = max(res, t[--r]);
        }
        return res;
    };
    long long X = 0;
    for (int i = 0; i < q; ++i) {
        int op; in >> op;
        if (op == 1) {
            int p; long long x; in >> p >> x;
            upd(p, x);
        } else {
            int l, r; in >> l >> r;
            long long v = qry(l, r);
            X ^= v;
        }
    }
    out << X << "{{NL}}";
""") + END

CP_M9_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& v : a) in >> v;
    // WRONG: two flaws. (1) The range scan drops the endpoint: it answers
    // max over a[l..r) instead of a[l..r] — the half-open/half-closed
    // stumble, wrong on every query whose maximum sits at r. (2) The whole
    // approach re-scans O(n) per query — O(n·q) ≈ 4·10^10 at scale, the
    // 'correct-shaped code, wrong complexity family' the budget law kills.
    long long X = 0;
    for (int i = 0; i < q; ++i) {
        int op; in >> op;
        if (op == 1) {
            int p; long long x; in >> p >> x;
            a[p] = x;
        } else {
            int l, r; in >> l >> r;
            long long mx = -1;
            for (int j = l; j < r; ++j) mx = max(mx, a[j]);   // BUG: j < r
            X ^= mx;
        }
    }
    out << X << "{{NL}}";
""") + END

# Verify the small test by hand once more: answers 5,10,4 → 5^10=15, 15^4=11
assert (5 ^ 10 ^ 4) == 11
assert (8 ^ 3) == 11

write_checkpoint(
    M, "hsgm-cp-m9", "Checkpoint — The Living Maximum",
    "Range max under interleaved updates: segment tree O((n+q) log n) vs the naive O(n·q) rescan. The W is correct code in the wrong complexity family — the budget law's canonical victim.",
    25,
    """
**Checkpoint — The Living Maximum.** Interleaved point-updates and range-
max queries: static prefix arrays die at the first update; the honest
structure is an iterative segment tree (O((n + q) log n)). The W is the
instructive baseline: *fully correct*, passes every small test, and dies
at full scale because O(n·q) = 4·10^10. This module's contract: when the
W fails only on the big test, the lesson is the complexity family — the
code was never the point.
""",
    "Điểm kiểm tra — Giá trị lớn nhất sống động",
    "Max đoạn dưới cập nhật xen kẽ: segment tree O((n+q) log n) so với quét lại naive O(n·q). W là code đúng trong sai họ độ phức tạp — nạn nhân kinh điển của định luật ngân sách.",
    """
**Điểm kiểm tra — Giá trị lớn nhất sống động.** Cập nhật điểm và hỏi max
đoạn xen kẽ: mảng tiền tố tĩnh chết ngay ở cập nhật đầu; cấu trúc trung
thực là segment tree lặp (O((n + q) log n)). W là baseline đáng dạy:
*đúng hoàn toàn*, qua mọi test nhỏ, và chết ở đúng giới hạn vì
O(n·q) = 4·10^10. Hợp đồng của module này: khi W chỉ gãy ở test lớn, bài
học là họ độ phức tạp — code chưa bao giờ là điểm chính.
""",
    CP9C,
    CP9VI,
    CP_M9_R,
    CP_M9_W,
)

print("module m9 complete")
