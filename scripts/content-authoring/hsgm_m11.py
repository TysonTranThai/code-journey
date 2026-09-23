#!/usr/bin/env python3
"""HSG Mastery — Module 11: hsgm-clinic (Wrong Solution Clinic).

Reading plausible-but-wrong code: locating the flaw, constructing the
smallest counterexample, and naming the category of bug.
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


M = "hsgm-clinic"
write_module(
    M,
    "Wrong Solution Clinic",
    "The debugging discipline: localize by bisecting the input space, name the bug category, build the minimal counterexample — the skill of reading code that lies politely.",
    "Phòng khám lời giải sai",
    "Kỷ luật gỡ lỗi: khoanh vùng bằng chặt nhị phân không gian input, gọi tên loại bug, dựng phản ví dụ nhỏ nhất — kỹ năng đọc code nói dối một cách lịch sự.",
    ["hsgm-m11-localize", "hsgm-m11-catalog", "hsgm-cp-m11"],
    ["hsgm-p11-drills"],
)

write_lesson(
    M, "hsgm-m11-localize",
    "Localize by Bisection",
    "A failing code is a function with a broken region: find it by halving suspects, not by rereading.",
    12,
    """
# Localize by Bisection

When your code passes the sample and dies on the hidden test, rereading
is the slowest tool. Instead, **bisect the space of suspects**:

1. **Bisect the input.** Take the smallest failing family you can imagine
   (n = 1? 2? 3?). If nothing fails small, double until it does — the
   first failing n brackets the bug's scale.
2. **Bisect the code path.** Comment out a half (or force an early return
   with a known-good answer). Does the failure move? The bug lives in the
   half that flipped the outcome.
3. **Bisect the state.** Print invariants at the midpoint (sortedness,
   sum, monotonicity). The first checkpoint whose invariant is false is
   upstream of the bug.

## The catalog habit

Every located bug gets a **category name** (see the next lesson). Naming
converts a one-off fix into a reusable detection: "this is an
off-by-one-at-boundary; check both endpoints" is a *class* of future bugs
caught before they cost a submission.

## The counterexample bonus

The minimal failing input is not just diagnostic — it is the test that
pins the fix. Add it to your personal stress harness (Module 13 makes
that harness systematic) before repairing, so the repair can be verified
against the exact evidence.
""",
    "Khoanh vùng bằng chặt nhị phân",
    "Một code gãy là một hàm có vùng hỏng: tìm nó bằng cách chia đôi nghi phạm, không phải bằng cách đọc đi đọc lại.",
    """
# Khoanh vùng bằng chặt nhị phân

Khi code của bạn qua test mẫu nhưng chết ở test ẩn, đọc lại là công cụ
chậm nhất. Thay vào đó, **chia đôi không gian nghi phạm**:

1. **Chia đôi input.** Lấy họ input gãy nhỏ nhất bạn tưởng tượng được
   (n = 1? 2? 3?). Không gãy ở n nhỏ thì nhân đôi tới khi gãy — n gãy đầu
   tiên giới hạn thang của bug.
2. **Chia đôi đường đi code.** Vô hiệu hóa một nửa (hoặc ép return sớm với
   đáp án biết-trước là đúng). Lỗi có dịch chuyển không? Bug nằm ở nửa đã
   lật kết quả.
3. **Chia đôi trạng thái.** In các bất biến tại điểm giữa (tính có thứ tự,
   tổng, tính đơn điệu). Checkpoint đầu tiên có bất invariant sai nằm
   phía thượng nguồn của bug.

## Thói quen danh mục

Mọi bug được khoanh vùng đều được **gọi tên loại** (bài sau). Việc gọi
tên biến một lần vá lẻ thành một phép phát hiện tái sử dụng: "đây là
off-by-one-tại-biên; kiểm tra cả hai đầu mút" là một *lớp* bug tương lai
được bắt trước khi nó lấy mất một lần nộp.

## Phần thưởng phản ví dụ

Input gãy tối giản không chỉ để chẩn đoán — nó là test neo vá lỗi. Thêm
nó vào stress harness cá nhân (Module 13 hệ thống hóa harness đó) trước
khi vá, để phép vá được xác minh chống lại đúng bằng chứng.
""",
)

write_lesson(
    M, "hsgm-m11-catalog",
    "The Bug Catalog",
    "Seven recurring categories cover most wrong solutions — each with its signature and its smallest counterexample shape.",
    13,
    """
# The Bug Catalog

Almost every plausible-but-wrong solution falls into one of seven
categories. Learn the signatures; recognition beats re-derivation.

1. **Boundary off-by-one.** Exclusive/inclusive endpoints, `hi = n` vs
   `hi = n−1`, empty-range handling. Signature: fails on tests whose
   answer sits AT a boundary.
2. **Tie-breaking.** Comparison uses `>` where `>=` is required (or vice
   versa) — or the sort key ignores a secondary criterion. Signature:
   fails when equal keys exist; passes on all-distinct data.
3. **Signed/type overflow.** int32 accumulation over 2·10^9. Signature:
   fails only at scale, and the wrapped value is often negative.
4. **Ordered/unordered counting.** x·(x−1) vs x·(x−1)/2. Signature:
   exactly double (or half) on inputs with ≥ 2 relevant items.
5. **Greedy exchange violation.** A sort key missing the term the exchange
   proof needs. Signature: fails on an adversarial small case with two
   "competing" items.
6. **State staleness.** A visited-set or memo reused across queries, or
   updated too early/late. Signature: the *second* query in a batch is
   wrong while the first is right.
7. **Direction confusion.** Undirected edges added one-way; rows/columns
   transposed; parent/child flipped. Signature: asymmetric inputs break,
   symmetric ones pass.

The discipline: when you locate a bug, name its category AND write its
smallest counterexample. Both together are the vaccine.
""",
    "Danh mục bug",
    "Bảy loại tái diễn phủ phần lớn lời giải sai — mỗi loại có chữ ký và hình dạng phản ví dụ nhỏ nhất riêng.",
    """
# Danh mục bug

Hầu hết mọi lời giải sai-nhưng-hợp-lý rơi vào một trong bảy loại. Học
chữ ký; nhận diện thắng suy luận lại.

1. **Off-by-one tại biên.** Đầu mút đóng/mở, `hi = n` với `hi = n−1`,
   xử lý miền rỗng. Chữ ký: gãy ở test có đáp án nằm ĐÚNG tại biên.
2. **Phá hòa.** So sánh dùng `>` nơi cần `>=` (hoặc ngược) — hoặc khóa
   sort bỏ sót tiêu chí phụ. Chữ ký: gãy khi có khóa bằng nhau; qua trên
   dữ liệu đôi-một-khác.
3. **Tràn dấu/kiểu.** Tích lũy int32 vượt 2·10^9. Chữ ký: chỉ gãy ở thang
   lớn, và giá trị bị wrap thường thành âm.
4. **Đếm có-thứ-tự/không-thứ-tự.** x·(x−1) với x·(x−1)/2. Chữ ký: đúng
   gấp đôi (hoặc một nửa) trên input có ≥ 2 phần tử liên quan.
5. **Vi phạm hoán đổi greedy.** Khóa sort thiếu số hạng mà luận điểm hoán
   đổi cần. Chữ ký: gãy ở một case phản đốidraulic nhỏ với hai phần tử
   "cạnh tranh".
6. **Trạng thái cũ.** Tập visited hoặc memo dùng lại giữa các truy vấn,
   hoặc cập nhật quá sớm/muộn. Chữ ký: truy vấn *thứ hai* trong lô sai
   trong khi thứ nhất đúng.
7. **Nhầm hướng.** Cạnh vô hướng chỉ thêm một chiều; hàng/cột bị hoán vị;
   cha/con bị lật. Chữ ký: input bất đối xứng gãy, đối xứng thì qua.

Kỷ luật: khi khoanh vùng được một bug, gọi tên loại VÀ viết phản ví dụ
nhỏ nhất của nó. Cả hai cùng nhau là vắc-xin.
""",
)

# ---------------------------------------------------------------- practice
D1, D1VI = recognition_drill(
    "hsgm-p11-d1", "The Second Query Lies",
    "A solution answers 100 range queries. Query 1 is always right; later queries drift. Which catalog category?",
    [
        "Boundary off-by-one",
        "State staleness — a structure is reused or updated across queries",
        "Signed overflow",
        "Direction confusion",
    ],
    "B",
    "First-right-then-wrong is the staleness signature: shared state mutated by earlier queries. Off-by-one would fail regardless of position; overflow only at scale.",
    vi_title="Câu hỏi thứ hai nói dối",
    vi_scenario="Một lời giải trả 100 truy vấn đoạn. Truy vấn 1 luôn đúng; các truy vấn sau lệch dần. Loại bug nào trong danh mục?",
    vi_options=[
        "Off-by-one tại biên",
        "Trạng thái cũ — một cấu trúc được dùng lại hoặc cập nhật xuyên truy vấn",
        "Tràn số có dấu",
        "Nhầm hướng",
    ],
    vi_hint="Đúng-rồi-sai là chữ ký của staleness: trạng thái dùng chung bị các truy vấn trước làm biến dạng. Off-by-one gãy bất kể vị trí; tràn số chỉ gãy ở thang lớn.",
)

D2, D2VI = recognition_drill(
    "hsgm-p11-d2", "All-Distinct Lullaby",
    "A candidate solution passed 500 random tests, all with distinct values. Which category should you test FIRST?",
    [
        "Signed overflow — always first",
        "Tie-breaking — all-distinct data cannot exercise equal-key branches, so those paths are completely untested",
        "Direction confusion",
        "Ordered/unordered counting",
    ],
    "B",
    "Random distinct data never generates ties: the >=/ > and secondary-key branches ran zero times. That is the biggest untested surface.",
    vi_title="Khúc ru các phần tử khác nhau",
    vi_scenario="Một lời giải ứng viên qua 500 test ngẫu nhiên, toàn phần tử khác nhau. Bạn nên kiểm tra loại nào ĐẦU TIÊN?",
    vi_options=[
        "Tràn số có dấu — luôn là số một",
        "Phá hòa — dữ liệu khác-nhau-không-thể sinh khóa bằng nhau nên các nhánh đó chưa từng chạy",
        "Nhầm hướng",
        "Đếm có-thứ-tự/không-thứ-tự",
    ],
    vi_hint="Dữ liệu ngẫu nhiên khác nhau không bao giờ sinh hòa: các nhánh >=/> và khóa phụ chạy đúng 0 lần. Đó là bề mặt chưa kiểm thử lớn nhất.",
)

D3, D3VI = recognition_drill(
    "hsgm-p11-d3", "The Doubled Answer",
    "A counting solution returns exactly twice the expected answer on every non-trivial input. Which catalog category?",
    [
        "Boundary off-by-one",
        "Ordered/unordered counting — counted (i,j) and (j,i) as distinct",
        "State staleness",
        "Greedy exchange violation",
    ],
    "B",
    "Exact-doubling is the ordered-pair signature: x·(x−1) instead of x·(x−1)/2. Off-by-one shifts by one item, not a factor of two.",
    vi_title="Đáp án gấp đôi",
    vi_scenario="Một lời giải đếm trả về đúng gấp đôi đáp án mong đợi trên mọi input không tầm thường. Loại nào trong danh mục?",
    vi_options=[
        "Off-by-one tại biên",
        "Đếm có-thứ-tự/không-thứ-tự — đếm (i,j) và (j,i) như hai cặp khác nhau",
        "Trạng thái cũ",
        "Vi phạm hoán đổi greedy",
    ],
    vi_hint="Gấp-đôi-chính-xác là chữ ký của đếm có thứ tự: x·(x−1) thay vì x·(x−1)/2. Off-by-one lệch một phần tử, không phải hệ số hai.",
)

write_practice(
    M, "hsgm-p11-drills", "Clinic Drills",
    "Three drills: staleness signatures, the all-distinct blind spot, and exact-doubling diagnosis.",
    "Drill phòng khám",
    "Ba drill: chữ ký staleness, điểm mù khác-nhau-each-other, và chẩn đoán gấp-đôi-chính-xác.",
    "hsgm-m11-catalog", 20, "advanced",
    [D1, D2, D3],
    {"hsgm-p11-d1": D1VI, "hsgm-p11-d2": D2VI, "hsgm-p11-d3": D3VI},
    solutions=[
        ("hsgm-p11-d1", letter("B"), letter("A")),
        ("hsgm-p11-d2", letter("B"), letter("A")),
        ("hsgm-p11-d3", letter("B"), letter("A")),
    ],
)

# ---------------------------------------------------------------- checkpoint
# Real task: find the FIRST index where a[i] >= x (lower_bound) in a sorted
# array — the boundary-stumble magnet. W: the hi=n exclusive variant with
# `if (a[mid] < x) lo = mid + 1; else hi = mid - 1;` — the classic mix that
# skips the boundary answer when it sits at hi and loops wrong on empty.
# Ground truth: bisect_left in Python.
def _gt_lower(a, x):
    import bisect
    return bisect.bisect_left(a, x)


def _w_lower(a, x):
    # the W as code (see below) — simulate its behavior: this is the
    # upper_bound mix-up (strict <=), which answers bisect_right−like
    # positions and wrongly reports −1 when x equals the last element.
    lo, hi = 0, len(a) - 1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            ans = mid
            hi = mid - 1
    return ans


_ta = [
    ([1, 3, 5, 7], 4),
    ([1, 3, 5, 7], 7),      # x at last element — boundary case
    ([1, 3, 5, 7], 0),
    ([1, 3, 5, 7], 8),
    ([5], 5),
    ([5], 6),
    ([2, 2, 2, 2], 2),      # all-equal ties
    ([1, 2, 4, 8, 16], 3),
    ([1, 2, 4, 8, 16], 1),
]
_ok, _ow = zip(*((_gt_lower(a, x), _w_lower(a, x)) for a, x in _ta))
assert any(o != w for o, w in zip(_ok, _ow)), (_ok, _ow)  # W diverges
# The diverging case is ([1,3,5,7], 7): GT=3, W skips the boundary answer.

import random as _r
_r.seed(7)
_a11 = sorted(_r.randrange(0, 10**9) for _ in range(200000))
_xs11 = [_r.randrange(0, 10**9) for _ in range(1)]
_cp11 = _gt_lower(_a11, _xs11[0])

CP_M11_IN = T("200000 1", " ".join(map(str, _a11)), str(_xs11[0]))
CP_M11_WANT = T(str(_cp11))

CP11C = challenge(
    "hsgm-cp-m11-lower",
    "Checkpoint: The Missing Boundary",
    """**Task.** A sorted array of n distinct values; one query value x.
Print the smallest index i (0-indexed) with a[i] >= x, or −1 if none.

**The code under test** (fix it mentally, then submit the CORRECT
version): the shipped binary search tests `a[mid] <= x` and records the
answer only in the else branch. Trace what happens when x EQUALS a
qualifying element (e.g., x is the last element of the array).

**Constraints:** 1 ≤ n ≤ 200000; 0 ≤ a_i, x < 10^9.
""",
    [
        contest_test("middle", T("4 1", "1 3 5 7", "4"), T("2"), "a[2] = 5 is the first ≥ 4."),
        contest_test("absent", T("4 1", "1 3 5 7", "8"), T("-1"), "Nothing qualifies → −1."),
    ],
    level="debugging",
    difficulty="advanced",
)
CP11C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test("middle", T("4 1", "1 3 5 7", "4"), T("2"),
            "a[2] = 5 is the first ≥ 4."),
        contest_test("absent", T("4 1", "1 3 5 7", "8"), T("-1"),
            "Nothing qualifies → −1."),
        contest_test("boundary last", T("4 1", "1 3 5 7", "7"),
            T("3"), "The answer IS the last index — the exact case the strict-comparison bug loses."),
        contest_test("all equal", T("4 1", "2 2 2 2", "2"), T("0"),
            "Every element ties: the first qualifying index is 0."),
        contest_test("full scale", CP_M11_IN, CP_M11_WANT,
            "n = 200000 random sorted values, one random x. Ground truth via bisect_left."),
    )
]

CP11VI = vi_challenge(
    "Điểm kiểm tra: biên bị mất",
    """**Bài toán.** Một mảng đã sort n giá trị khác nhau; một giá trị truy vấn x.
In chỉ số nhỏ nhất i (đánh từ 0) sao cho a[i] >= x, hoặc −1 nếu không có.

**Code đang bị kiểm tra** (sửa trong đầu, rồi nộp bản ĐÚNG): phép tìm kiếm
nhị phân kiểm tra `a[mid] <= x` và chỉ ghi đáp án ở nhánh else. Truy vết
diều gì xảy ra khi x BẰNG một phần tử đủ điều kiện (ví dụ x là phần tử
cuối của mảng).

**Ràng buộc:** 1 ≤ n ≤ 200000; 0 ≤ a_i, x < 10^9.
""",
    [("giữa", "a[2] = 5 là phần tử đầu ≥ 4."),
     ("vắng mặt", "Không phần tử nào đủ → −1."),
     ("biên cuối", "Đáp án CHÍNH LÀ chỉ số cuối — đúng case mà bug so-sánh-chặt làm mất."),
     ("toàn bằng nhau", "Mọi phần tử hòa: chỉ số đầu đủ điều kiện là 0."),
     ("đúng giới hạn", "n = 200000 giá trị ngẫu nhiên đã sort, một x ngẫu nhiên. Đáp án chuẩn bằng bisect_left.")],
)

CP_M11_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& v : a) in >> v;
    for (int t = 0; t < q; ++t) {
        long long x; in >> x;
        int lo = 0, hi = n;          // [lo, hi) — the honest half-open frame
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (a[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        out << (lo < n && a[lo] >= x ? lo : -1) << "{{NL}}";
    }
""") + END

CP_M11_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n);
    for (auto& v : a) in >> v;
    // WRONG: answers 'first index with a[i] > x' (upper_bound) instead of
    // 'first index with a[i] >= x' — the strict/non-strict stumble. When x
    // equals qualifying elements (last-element boundary, all-equal arrays)
    // it wrongly reports −1.
    for (int t = 0; t < q; ++t) {
        long long x; in >> x;
        int lo = 0, hi = n - 1;
        int ans = -1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (a[mid] <= x) lo = mid + 1;
            else { ans = mid; hi = mid - 1; }
        }
        out << ans << "{{NL}}";
    }
""") + END

# Sanity: verify the W actually loses the boundary case (simulate in Python)
assert _ow[_ta.index(([1, 3, 5, 7], 7))] == -1 and _ok[_ta.index(([1, 3, 5, 7], 7))] == 3

write_checkpoint(
    M, "hsgm-cp-m11", "Checkpoint — The Lost Boundary",
    "Lower-bound binary search: the shipped code loses the answer when it is the last index (closed-interval + early hi shrink). Fix it; the tests pin the boundary and the all-tie case.",
    25,
    """
**Checkpoint — The Lost Boundary.** The provided binary search *looks*
canonical but answers the wrong predicate: `a[mid] <= x` makes it return
the first index strictly GREATER than x (upper_bound), so when x equals
qualifying elements — the last-element boundary, or an all-equal array —
it reports −1. The repair is one character: `<` instead of `<=`, with the
post-loop existence check intact. The boundary and all-tie tests are
exactly the shapes the stumble cannot survive.
""",
    "Điểm kiểm tra — Biên bị mất",
    "Tìm kiếm nhị phân lower-bound: code đang có *trông* kinh điển nhưng trộn khung: miền đóng [lo, hi] với `hi = mid − 1` sau khi ghi đáp án âm thầm bỏ chỉ số cuối đủ điều kiện. Phép sửa là khung nửa-mở trung thực [lo, hi) với `hi = mid` và phép kiểm tra tồn tại sau vòng lặp.",
    """
**Điểm kiểm tra — Biên bị mất.** Phép tìm kiếm nhị phân được cấp *trông*
rất kinh điển nhưng trả sai vị từ: `a[mid] <= x` khiến nó trả về chỉ số
đầu tiên LỚN HƠN chặt x (upper_bound), nên khi x bằng phần tử đủ điều
kiện — biên phần-tử-cuối, hoặc mảng toàn-bằng — nó báo −1. Phép sửa chỉ
một ký tự: `<` thay cho `<=`, giữ nguyên phép kiểm tra tồn tại sau vòng
lặp. Test biên và test toàn-bằng là đúng các hình dạng mà cú vấp không
thể sống sót.
""",
    CP11C,
    CP11VI,
    CP_M11_R,
    CP_M11_W,
)

print("module m11 complete")
