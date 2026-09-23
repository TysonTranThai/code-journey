#!/usr/bin/env python3
"""HSG Mastery — Module 2: hsgm-budget (Constraint → Complexity).

The budget law: constraints are the problem's confession about its intended
complexity. Includes the n ≤ 20 law, the O(n·q) death sentence, value-range
reasoning (10^18 → log-scale), and honest op-count multiplication.
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

M = "hsgm-budget"
write_module(
    M,
    "Constraint to Complexity",
    "Reading the constraint table as the setter's confession: n ≤ 20 means brute force is intended, n·q at 2·10^5 is a death sentence, values ≤ 10^18 mean log-scale. Honest op-count arithmetic first.",
    "Giới hạn thành độ phức tạp",
    "Đọc bảng giới hạn như lời thú nhận của người ra đề: n ≤ 20 nghĩa là brute force được chủ đích, n·q ở 2·10^5 là bản án tử, giá trị ≤ 10^18 nghĩa là thang log. Nhân phép toán trung thực trước bất kỳ dòng code nào.",
    ["hsgm-m2-law", "hsgm-m2-valuemedium", "hsgm-cp-m2"],
    ["hsgm-p2-drills"],
)

write_lesson(
    M, "hsgm-m2-law",
    "The Budget Law",
    "Every constraint is information. Multiply honestly; then pick the only family that fits.",
    12,
    """
# The Budget Law

A constraint line is not a nuisance — it is the setter telling you which
solutions are allowed to exist. The discipline: **multiply out the op
count before writing any code.**

## The standard ladder (≈ 10^8 ops per second ceiling; ~3·10^8 is the
"code it now" edge from exam-room experience)

| Constraint | Budget | Families that fit |
|---|---|---|
| n ≤ 20 (or n ≤ 24) | 2^n–2^n·n | brute force, bitmask DP, meet-in-the-middle above that |
| n ≤ 500 | n^3 | Floyd–Warshall, assignment DP, dense graph passes |
| n ≤ 5000 | n^2 | pairwise DP, O(n^2) sweeps, LIS bottom-up |
| n ≤ 10^5 – 2·10^5 | n log n (or n·√n) | sorting, heaps, segment trees, DSU, Dijkstra |
| n ≤ 5·10^6+ | n (tiny constant) | two pointers, sieve, prefix sums, KMP |
| value ≤ 10^18 | log(value) | binary search on answer, digit DP, matrix power |
| n ≤ 40, subset sums | n/2 · 2^(n/2) | meet in the middle |
| q ≤ 10^5, values ≤ 10^5 | (n + q) log | offline sorting + Fenwick sweeps |

## Multiplying honestly

O(n·q) with n = q = 2·10^5 is **4·10^10** — a hundred times past the
ceiling, not "a bit slow". O(n√n) with n = 10^5 is 3·10^7 — comfortable.
O(2^n) with n = 24 is 1.7·10^7 — fine; with n = 30 it is 10^9 — dead.
Write the number down; do not eyeball it.

## The two-sided error

- **Under-budgeting** (picking n^2 for n = 2·10^5) = guaranteed TLE on the
  big test.
- **Over-budgeting** (inventing an O(n log n) solution for n ≤ 500) =
  wasted hours and bug surface. When n ≤ 20, brute force IS the intended
  solution — code it with confidence.

## Worked reflex

`n ≤ 10^5, q ≤ 10^5, "for each query, the nearest j > i with a[j] > a[i]"`:
budget n log n; shape = per-index nearest-right-greater; families = sorted
sweep with a monotonic stack of seen values (process right to left with a
stack, or coordinate-compressed Fenwick scanning from the right). Two
candidates, both fit — pick the one with less code. That's the whole
decision.
""",
    "Định luật ngân sách",
    "Mọi giới hạn đều là thông tin. Nhân trung thực; rồi chọn họ duy nhất vừa.",
    """
# Định luật ngân sách

Dòng giới hạn không phải chuyện phiền — đó là người ra đề nói cho bạn biết
những lời giải nào được phép tồn tại. Kỷ luật: **nhân ra số phép toán
trước khi viết bất kỳ dòng code nào.**

## Thang chuẩn (trần ≈ 10^8 phép/giây; ~3·10^8 là mép "code ngay" theo kinh
nghiệm phòng thi)

| Giới hạn | Ngân sách | Các họ vừa |
|---|---|---|
| n ≤ 20 (hoặc n ≤ 24) | 2^n–2^n·n | brute force, DP bitmask, meet-in-the-middle cho lớn hơn |
| n ≤ 500 | n^3 | Floyd–Warshall, DP phân công, quét đồ thị dày |
| n ≤ 5000 | n^2 | DP theo cặp, quét O(n^2), LIS bottom-up |
| n ≤ 10^5 – 2·10^5 | n log n (hoặc n·√n) | sắp xếp, heap, segment tree, DSU, Dijkstra |
| n ≤ 5·10^6+ | n (hằng số nhỏ) | two pointers, sàng, tổng tiền tố, KMP |
| giá trị ≤ 10^18 | log(giá trị) | tìm kiếm nhị phân đáp án, digit DP, lũy thừa ma trận |
| n ≤ 40, tổng tập con | n/2 · 2^(n/2) | meet in the middle |
| q ≤ 10^5, giá trị ≤ 10^5 | (n + q) log | sắp xếp offline + quét Fenwick |

## Nhân trung thực

O(n·q) với n = q = 2·10^5 là **4·10^10** — gấp trăm lần trần, không phải
"chậm một chút". O(n√n) với n = 10^5 là 3·10^7 — thoải mái. O(2^n) với
n = 24 là 1.7·10^7 — ổn; với n = 30 là 10^9 — chết. Viết số ra giấy; đừng
ước lượng bằng mắt.

## Hai chiều sai

- **Ngân sách thấp hơn thật** (chọn n^2 cho n = 2·10^5) = TLE chắc chắn
  trên test lớn.
- **Ngân sách cao hơn cần** (nghĩ ra O(n log n) cho n ≤ 500) = phí giờ và
  mở diện tích lỗi. Khi n ≤ 20, brute force CHÍNH LÀ lời giải chủ đích —
  code tự tin.

## Phản xạ mẫu

`n ≤ 10^5, q ≤ 10^5, "với mỗi truy vấn, j gần nhất > i với a[j] > a[i]"`:
ngân sách n log n; dạng = gần-phải-lớn-hơn theo từng chỉ số; các họ = quét
có sắp xếp với stack đơn điệu các giá trị đã thấy (xử lý phải sang trái với
stack, hoặc Fenwick nén tọa độ quét từ phải). Hai ứng cử viên, cùng vừa —
chọn cái ít code hơn. Toàn bộ quyết định là vậy.
""",
)

write_lesson(
    M, "hsgm-m2-valuemedium",
    "Value Ranges Are Constraints Too",
    "Why 10^18 means log-scale, why small-n-big-values means compression or binary search, and how answer bounds reveal algorithms.",
    10,
    """
# Value Ranges Are Constraints Too

n is not the only number that chooses the algorithm. The **value range**
confesses just as loudly.

## Big values, small positions

Values up to 10^9 or 10^18 with n ≤ 2·10^5 means the *values* cannot be
array indices. Your options: coordinate compression (if only relative order
matters), hashing (if only equality matters), or binary search on the value
domain (if feasibility is monotone in the answer).

## 10^18 means log

Any state that walks the value 10^18 itself (1-indexed loops over it,
arrays of its size) is dead on arrival. If a problem says "count numbers
≤ 10^18 with property P", the count must live on the **19 digits** — digit
DP — or on a monotone predicate over the value — binary search.

## The answer's own bound

"Print the answer modulo 10^9 + 7" warns you the answer is astronomically
large — count with DP/combinatorics, never enumerate. An explicit small
bound ("the answer fits in 32 bits") is the setter's gift — it often means
a direct constructive or greedy exists.

## Sum bounds

"Σn ≤ 2·10^5 over all test cases" is a gift: per-test-case complexity can
be near-linear *summed*, so expensive precomputation per case is fine when
cases are few, and vice versa. Misreading this is a classic TLE.
""",
    "Dải giá trị cũng là giới hạn",
    "Vì sao 10^18 nghĩa là thang log, vì sao n-nhỏ-giá-trị-lớn nghĩa là nén hoặc tìm nhị phân, và cách chặn đáp án hé lộ thuật toán.",
    """
# Dải giá trị cũng là giới hạn

n không phải con số duy nhất chọn thuật toán. **Dải giá trị** cũng thú nhận
không kém.

## Giá trị lớn, vị trí nhỏ

Giá trị tới 10^9 hoặc 10^18 với n ≤ 2·10^5 nghĩa là *giá trị* không thể
làm chỉ số mảng. Lựa chọn của bạn: nén tọa độ (nếu chỉ thứ tự tương đối
quan trọng), băm (nếu chỉ bằng/khác quan trọng), hoặc tìm kiếm nhị phân
trên miền giá trị (nếu tính khả thi đơn điệu theo đáp án).

## 10^18 nghĩa là log

Bất kỳ trạng thái nào đi bộ trên chính giá trị 10^18 (vòng lặp 1-indexed
trên nó, mảng cỡ nó) chết ngay khi sinh ra. Nếu đề nói "đếm số ≤ 10^18 có
tính chất P", con đếm phải sống trên **19 chữ số** — digit DP — hoặc trên
một vị từ đơn điệu theo giá trị — tìm kiếm nhị phân.

## Chặn của chính đáp án

"In đáp án theo modulo 10^9 + 7" cảnh báo đáp án khổng lồ — đếm bằng
DP/tổ hợp, đừng liệt kê. Một chặn nhỏ tường minh ("đáp án vừa 32 bit") là
món quà của người ra đề — thường nghĩa là có thuật dựng trực tiếp hoặc
greedy.

## Chặn tổng

"Σn ≤ 2·10^5 trên mọi test" là món quà: độ phức tạp mỗi test chỉ cần vừa
*tính theo tổng*, nên tiền xử lý đắt mỗi test vẫn ổn khi test ít, và ngược
lại. Đọc nhầm chỗ này là một dạng TLE kinh điển.
""",
)

# ----------------------------------------------------------------- practice
def letter(l):
    return CPP_STD + cpp('    out << "' + l + '";') + END


D1, D1VI = recognition_drill(
    "hsgm-p2-d1", "The 10^18 Count",
    "Count integers in [1, N], N ≤ 10^18, whose digit sum is divisible by 9. Which family is forced by the value bound?",
    ["Sieve every number up to N",
     "Digit DP over the ≤ 19 digits, tracking sum mod 9",
     "Segment tree over the value axis",
     "DSU on digits"],
    "B",
    "Walking the value is impossible at 10^18; the state must live on the 19 digit positions plus a mod-9 residue — digit DP.",
    vi_title="Cái đếm 10^18",
    vi_scenario="Đếm các số trong [1, N], N ≤ 10^18, có tổng chữ số chia hết cho 9. Dải giá trị ép buộc họ nào?",
    vi_options=["Sàng từng số tới N",
                "Digit DP trên ≤ 19 chữ số, theo dõi tổng mod 9",
                "Segment tree trên trục giá trị",
                "DSU trên các chữ số"],
    vi_hint="Đi bộ trên giá trị là bất khả ở 10^18; trạng thái phải sống trên 19 vị trí chữ số cộng phần dư mod 9 — digit DP.",
)
D2, D2VI = recognition_drill(
    "hsgm-p2-d2", "Σn Discipline",
    "T test cases (T ≤ 1000) with per-test n; the statement guarantees Σn ≤ 200000. Your per-test algorithm is O(n^2). Which is true?",
    ["Fine: per-test n is small, so O(n^2) per test is safe",
     "Unsafe in general: one test with n = 200000 costs 4·10^10; only the SUM is bounded",
     "Fine because T ≤ 1000 caps everything",
     "Unsafe only if values are large"],
    "B",
    "Σn ≤ 200000 bounds the total, so a single test may carry all of it: per-test quadratic explodes on exactly that test. Complexity must be stated against Σn.",
    vi_title="Kỷ luật Σn",
    vi_scenario="T test (T ≤ 1000), mỗi test có n riêng; đề bảo đảm Σn ≤ 200000. Thuật của bạn mỗi test là O(n^2). Câu nào đúng?",
    vi_options=["Ổn: n mỗi test nhỏ nên O(n^2) mỗi test an toàn",
                "Không an toàn nói chung: một test n = 200000 tốn 4·10^10; chỉ TỔNG bị chặn",
                "Ổn vì T ≤ 1000 chặn mọi thứ",
                "Không an toàn chỉ khi giá trị lớn"],
    vi_hint="Σn ≤ 200000 chặn tổng, nên một test có thể gánh trọn: bậc hai mỗi test nổ đúng trên test đó. Độ phức tạp phải phát biểu theo Σn.",
)
D3, D3VI = recognition_drill(
    "hsgm-p2-d3", "Modulo Confession",
    "A counting problem says the answer can be huge and must be printed modulo 10^9 + 7, with n ≤ 10^6. What does this confess?",
    ["The answer is small; brute force works",
     "The count must be computed by DP/combinatorics — enumeration is impossible",
     "The problem is actually about primes",
     "n must be smaller in real tests"],
    "B",
    "Modulo output exists because the true answer overflows everything — you must derive it structurally (DP, combinatorics, matrix power), never enumerate it.",
    vi_title="Lời thú nhận của modulo",
    vi_scenario="Một bài đếm nói đáp án rất lớn, phải in theo modulo 10^9 + 7, với n ≤ 10^6. Điều đó thú nhận điều gì?",
    vi_options=["Đáp án nhỏ; brute force chạy được",
                "Phải đếm bằng DP/tổ hợp — liệt kê là bất khả",
                "Bài thật ra về số nguyên tố",
                "n sẽ nhỏ hơn trong test thật"],
    vi_hint="Modulo tồn tại vì đáp án thật tràn mọi kiểu dữ liệu — phải suy ra cấu trúc (DP, tổ hợp, lũy thừa ma trận), không bao giờ liệt kê.",
)

write_practice(
    M, "hsgm-p2-drills", "Budget Drills",
    "Three drills: the forced-by-values family, the Σn trap, and the modulo confession.",
    "Drill ngân sách",
    "Ba bài: họ bị ép bởi dải giá trị, bẫy Σn, và lời thú nhận của modulo.",
    "hsgm-m2-valuemedium", 25, "advanced",
    [D1, D2, D3],
    {"hsgm-p2-d1": D1VI, "hsgm-p2-d2": D2VI, "hsgm-p2-d3": D3VI},
    solutions=[
        ("hsgm-p2-d1", letter("B"), letter("A")),
        ("hsgm-p2-d2", letter("B"), letter("A")),
        ("hsgm-p2-d3", letter("B"), letter("A")),
    ],
)

# --------------------------------------------------------------- checkpoint
# Real task: two-query budget problem where the O(n·q) W times out and the
# O((n+q) log n) R survives. Static: prefix sums + (for the interleaved
# variant) Fenwick. Task: point updates + prefix sums under a checksum
# protocol at full scale (n = q = 200000).
# Ground truth computed in Python below.
_n = 200000
_q = 200000
_vals = [(i * 6997) % 1000003 for i in range(1, _n + 1)]
# queries: type 1 p x (set a[p] = x), type 2 p (prefix sum through p)
_qops = []
for i in range(1, _q + 1):
    if i % 2 == 1:
        _p = (i * 17) % _n + 1
        _qops.append((1, _p, (i * 911) % 1000000))
    else:
        _p = (i * 23) % _n + 1
        _qops.append((2, _p, 0))

# Fenwick in Python for ground truth
_bit = [0] * (_n + 1)


def _upd(i, d):
    while i <= _n:
        _bit[i] += d
        i += i & (-i)


def _qry(i):
    s = 0
    while i > 0:
        s += _bit[i]
        i -= i & (-i)
    return s


_arr = [0] * (_n + 1)
for i, v in enumerate(_vals, start=1):
    _arr[i] = v
    _upd(i, v)

_xor = 0
_lsum = 0
_out = []
for op, p, x in _qops:
    if op == 1:
        _upd(p, x - _arr[p])
        _arr[p] = x
    else:
        s = _qry(p)
        _out.append(str(s))
        _xor ^= s
        _lsum = (_lsum + s) % 1000000007

CP_M2_IN = T(
    f"{_n} {_q}",
    " ".join(map(str, _vals)),
    *[f"{op} {p} {x}" if op == 1 else f"2 {p}" for (op, p, x) in _qops],
)
CP_M2_WANT = T(*(_out + [str(_xor) + " " + str(_lsum)]))

CP2C = challenge(
    "hsgm-cp-m2-fenwick",
    "Checkpoint: Point Set, Prefix Ask",
    """**Task.** An array of n ≤ 200000 integers. q ≤ 200000 operations:
`1 p x` sets a[p] = x; `2 p` prints the prefix sum a[1..p]. After all
operations, print the XOR of all answers from type-2 operations and their
total modulo 1 000 000 007 (folded as "X S" on one line).

**Constraints:** 1 ≤ p ≤ n; 0 ≤ a[i], x < 10^6.

**Budget check:** n·q naive re-summing is ~4·10^10 — dead. The interleaved
update/query pattern names the structure.
""",
    [
        contest_test("set then ask", T("3 3", "5 1 4", "2 2", "1 2 10", "2 3"), T("6", "19", "21 25"),
            "Prefix 2 = 6; after a[2] = 10, prefix 3 = 19. XOR(6,19) = 21, sum = 25 → '21 25'."),
    ],
    level="combination",
    difficulty="advanced",
)
# Fix the want after recomputing by hand: answers 6 and 19; XOR = 6^19 = 21; sum = 25.
CP2C["tests"] = [
    dict(zip(("name", "code", "hint"), t))
    for t in (
        contest_test(
            "set then ask", T("3 3", "5 1 4", "2 2", "1 2 10", "2 3"), T("6", "19", "21 25"),
            "Prefix 2 = 6; after a[2] = 10, prefix 3 = 19. XOR(6,19) = 21, sum = 25 → '21 25'."),
        contest_test("single element overflow probe", T("2 2", "1000000 1000000", "2 2", "2 2"), T("2000000", "2000000", "0 4000000"),
            "Prefix 2 = 2·10^6 each time. XOR of equal values cancels to 0; sum = 4·10^6 → '0 4000000'."),
        contest_test("full scale", CP_M2_IN, CP_M2_WANT,
            "n = q = 200000 interleaved: naive re-summing is ~4·10^10 ops and dies; a Fenwick tree answers each op in O(log n). Ground truth computed independently in Python."),
    )
]

CP2VI = vi_challenge(
    "Điểm kiểm tra: gán điểm, hỏi tiền tố",
    """**Bài toán.** Mảng n ≤ 200000 số nguyên. q ≤ 200000 thao tác:
`1 p x` gán a[p] = x; `2 p` in tổng tiền tố a[1..p]. Sau tất cả, in XOR của
mọi đáp án từ thao tác loại 2 và tổng của chúng modulo 1 000 000 007 (gộp
thành "X S" trên một dòng).

**Ràng buộc:** 1 ≤ p ≤ n; 0 ≤ a[i], x < 10^6.

**Kiểm tra ngân sách:** tính lại naive mỗi lần là ~4·10^10 — chết. Mẫu
cập nhật/truy vấn xen kẽ gọi tên cấu trúc.
""",
    [("gán rồi hỏi", "Tiền tố 2 là 6; sau khi a[2]=10, tiền tố 3 là 19. XOR(6,19)=21, tổng=25 → '21 25'."),
     ("dò tràn một phần tử", "Tiền tố 2 = 2·10^6 mỗi lần. XOR hai giá trị bằng nhau triệt tiêu thành 0; tổng = 4·10^6 → '0 4000000'."),
     ("đúng giới hạn", "n = q = 200000 xen kẽ: tính lại naive ~4·10^10 phép và chết; cây Fenwick trả mỗi thao tác trong O(log n).")],
)

CP_M2_R = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> bit(n + 1, 0), a(n + 1, 0);
    auto upd = [&](int i, long long d) {
        for (; i <= n; i += i & (-i)) bit[i] += d;
    };
    auto qry = [&](int i) {
        long long s = 0;
        for (; i > 0; i -= i & (-i)) s += bit[i];
        return s;
    };
    for (int i = 1; i <= n; ++i) { in >> a[i]; upd(i, a[i]); }
    long long X = 0, S = 0;
    for (int t = 0; t < q; ++t) {
        int op; in >> op;
        if (op == 1) {
            int p; long long x; in >> p >> x;
            upd(p, x - a[p]); a[p] = x;
        } else {
            int p; in >> p;
            long long s = qry(p);
            out << s << "{{NL}}";
            X ^= s;
            S = (S + s % 1000000007 + 1000000007) % 1000000007;
        }
    }
    out << X << " " << S << "{{NL}}";
""") + END

CP_M2_W = CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    long long X = 0, S = 0;
    for (int t = 0; t < q; ++t) {
        int op; in >> op;
        if (op == 1) {
            int p; long long x; in >> p >> x;
            a[p] = x;
        } else {
            int p; in >> p;
            // WRONG: re-sums in O(p) AND accumulates in int — the prefix
            // reaches ~2·10^11, overflowing int32 long before the end. Two
            // flaws the budget law flags: the wrong complexity family AND
            // the wrong integer type. (The O(p) loop also cannot survive
            // n = q = 200000 within contest limits.)
            int s = 0;
            for (int i = 1; i <= p; ++i) s += (int)a[i];
            out << s << "{{NL}}";
            X ^= (long long)s;
            S = (S + (long long)s % 1000000007 + 1000000007) % 1000000007;
        }
    }
    out << X << " " << S << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgm-cp-m2", "Checkpoint — The Structure the Budget Names",
    "Point-set + prefix-sum at full scale: the constraint table admits exactly one family. The W is the honest-looking O(p) re-sum.",
    25,
    """
**Checkpoint — The Structure the Budget Names.** n = q = 200000 interleaved
sets and prefix asks. The budget law kills re-summing (~10^10 ops) and
leaves exactly one comfortable family. Note the folded "X S" checksum on
the full-scale test: it verifies the *whole* answer stream, not just a
line — the standard trick used throughout this course's big tests.
""",
    "Điểm kiểm tra — Cấu trúc mà ngân sách gọi tên",
    "Gán điểm + tổng tiền tố ở đúng giới hạn: bảng giới hạn chỉ cho phép đúng một họ. W là phép tính lại O(p) trông rất chính đáng.",
    """
**Điểm kiểm tra — Cấu trúc mà ngân sách gọi tên.** n = q = 200000 xen kẽ
giữa gán và hỏi tiền tố. Định luật ngân sách hạ phép tính lại (~10^10 phép)
và chừa lại đúng một họ thoải mái. Chú ý checksum "X S" gộp ở test đúng
giới hạn: nó xác minh *toàn bộ* dòng đáp án, không chỉ một dòng — mẹo chuẩn
dùng xuyên suốt các test lớn của khóa này.
""",
    CP2C,
    CP2VI,
    CP_M2_R,
    CP_M2_W,
)

print("module m2 complete")
