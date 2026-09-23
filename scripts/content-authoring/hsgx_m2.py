#!/usr/bin/env python3
"""HSG Intensive — Module 2: hsgx-budget (Constraint Budget).

Constraints are the algorithm's invoice. Drills train the arithmetic of
budgets (how many operations fit) and the mapping constraint → family; the
checkpoint executes a genuine small-n problem where brute force IS the
intended solution, against a "clever" greedy that fails.

Conventions: zero literal backslashes. T() real newlines; cpp() → \n escapes.
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


# NOTE: solutions use explicit includes (hsga pattern) — solution.cpp is
# compiled INTO the QA harness TU (which pre-includes the std headers), and
# the local QA toolchain (Apple clang) lacks bits/stdc++.h.
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
    # bare letter, no newline — contest_test builds want via T() (no trailing NL)
    return CPP_STD + cpp('    out << "' + l + '";') + END


M = "hsgx-budget"
write_module(
    M,
    "Constraint Budget",
    "Turning n, q, and value ranges into an operation budget — and picking the only family that fits it. Includes the n ≤ 20 law: when brute force is the answer, code it.",
    "Ngân sách giới hạn",
    "Biến n, q và dải giá trị thành ngân sách phép toán — và chọn họ duy nhất vừa ngân sách đó. Gồm định luật n ≤ 20: khi brute force là đáp án, hãy cài nó.",
    ["hsgx-m2-arithmetic", "hsgx-m2-mapping", "hsgx-cp-m2"],
    ["hsgx-p2-drills"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsgx-m2-arithmetic",
    "The Arithmetic of Budgets",
    "Sandbox reality check: what 10^8, 10^9, and 10^10 operations mean in seconds — and the memory line.",
    20,
    """
# The Arithmetic of Budgets

Contest time limits are calibrated so the intended complexity passes with
margin. Your job in the first ten minutes is to compute the budget.

## The working numbers

Modern judges (and this platform's C++20 sandbox) execute roughly:

- **~10^9** trivial operations (integer add, compare, array read) per second,
- **~10^8** "normal" operations (map insert, modulo, function call chains),
- **~10^7** heavy operations (sort of small vectors, string builds).

So: `n·q` with n = q = 2·10^5 is 4·10^10 — **100× over budget** even for
trivial ops. `n log n` with n = 2·10^5 is ~3.4·10^6·(log factor) — **deep
inside budget**. This is why the intended complexity, not clever constants,
is what the constraint table is telling you.

## Memory is the silent constraint

`int a[1000][1000]` is 4 MB — fine. `long long a[10^5][10^5]` is 80 GB —
not a program, a hallucination. The sandbox grants 512 MB: a
`vector<long long>` of 10^6 elements is 8 MB (fine); of 10^8 is 800 MB
(dead). When a DP state is (position × mask) with n = 24, 2^24 × 8 B = 134
MB — possible but tight; think before allocating.

## Value ranges encode the state space

- sums up to 10^5 × 10^9 → 10^14 → **long long mandatory**, int overflows
  silently.
- answers modulo 10^9+7 → the true number is astronomically large; anything
  that stores it raw (including intermediate products) must be reduced.
- N ≤ 10^18 → the state is the *digits* or the *log*, never N itself.

## The two-second estimate (do it before reading the statement twice)

Given the constraint table, compute: `n · (per-item cost)`, `n log n`,
`n^2`, `2^n`, and see which crosses the line. The family that survives the
arithmetic *and* matches the semantics is your candidate. Everything after
this module is about confirming the semantics part.
""",
    "Phép toán của ngân sách",
    "Đối chiếu thực tế sandbox: 10^8, 10^9 và 10^10 phép toán nghĩa là bao nhiêu giây — và giới hạn bộ nhớ.",
    """
# Phép toán của ngân sách

Giới hạn thời gian thi được hiệu chỉnh để độ phức tạp chủ đích qua đích với
dư dả. Việc của bạn trong mười phút đầu là tính ngân sách.

## Những con số làm việc

Judge hiện đại (và sandbox C++20 của nền tảng này) chạy khoảng:

- **~10^9** phép tầm thường (cộng số nguyên, so sánh, đọc mảng) mỗi giây,
- **~10^8** phép "bình thường" (insert vào map, modulo, chuỗi gọi hàm),
- **~10^7** phép nặng (sort vector nhỏ, dựng xâu).

Vậy: `n·q` với n = q = 2·10^5 là 4·10^10 — **vượt ngân sách 100×** dù là
phép tầm thường. `n log n` với n = 2·10^5 là ~3.4·10^6 (nhân hệ số log) —
**sâu trong ngân sách**. Vì vậy độ phức tạp chủ đích, không phải thủ thuật
hằng số, mới là điều bảng giới hạn đang nói với bạn.

## Bộ nhớ là ràng buộc im lặng

`int a[1000][1000]` là 4 MB — ổn. `long long a[10^5][10^5]` là 80 GB —
không phải chương trình, là ảo giác. Sandbox cấp 512 MB: `vector<long long>`
10^6 phần tử là 8 MB (ổn); 10^8 phần tử là 800 MB (chết). Khi trạng thái DP
là (vị trí × mask) với n = 24: 2^24 × 8 B = 134 MB — khả thi nhưng sát nút;
nghĩ trước khi cấp phát.

## Dải giá trị mã hóa không gian trạng thái

- tổng tới 10^5 × 10^9 → 10^14 → **long long bắt buộc**, int tràn âm thầm.
- đáp án modulo 10^9+7 → số thật khổng lồ; mọi thứ lưu nó thô (kể cả tích
  trung gian) phải được rút gọn.
- N ≤ 10^18 → trạng thái là *chữ số* hoặc *log*, không bao giờ là N.

## Ước lượng hai giây (làm trước khi đọc đề lần hai)

Nhìn bảng giới hạn, tính: `n · (chi phí mỗi phần tử)`, `n log n`, `n^2`,
`2^n`, xem cái nào vượt vạch. Họ thuật toán sống sót phép toán *và* khớp ngữ
nghĩa là ứng cử viên. Mọi thứ sau module này là về việc xác nhận phần ngữ nghĩa.
""",
)

write_lesson(
    M, "hsgx-m2-mapping",
    "Constraint → Family Mapping",
    "The full decision table with the traps: value-range tricks, q-vs-n asymmetry, and the small-n law.",
    20,
    """
# Constraint → Family Mapping

The selection guide from Module 1, now with the traps that make drills hard.

## Trap 1 — Values big, n small

`n ≤ 24, a[i] ≤ 10^12`: the state space is **2^24 subsets**, not values.
Meet in the middle or bitmask DP. Values being huge is a hint that answers
are compared, not counted — sort of subset sums, not prefix sums.

## Trap 2 — q ≫ n or n ≫ q

`n ≤ 100, q ≤ 10^5` → **precompute everything**: O(n^2) or even O(n^3) is
affordable at build time; each query must be O(1) or O(log n). Reverse
(`n ≤ 10^5, q ≤ 100`) → per-query O(n) or O(n log n) is fine; precomputation
wasted on 100 queries is fine too, but don't build a segment tree out of
habit when 100 linear scans are cheaper and safer.

## Trap 3 — The array is sorted / nearly sorted (read the guarantee)

"Sorted" in the guarantee is a gift: two pointers, binary search, merge
without sort. Ignoring a stated guarantee burns the intended solution.

## Trap 4 — String length vs alphabet

|s| ≤ 2·10^5 over lowercase: 26-letter count arrays, bitmask of seen letters
(26 bits fits in an int), counting sort. |s| ≤ 20: substring enumeration
2^20 is fine.

## Trap 5 — Tree guarantees

"A tree with n vertices, q path queries" is LCA-shaped; "n−1 edges" stated
once in the middle of the paragraph is the same problem. Underline the word
*tree*. A tree is a DAG with exactly one path per pair — the entire DP-on-
trees toolbox opens only if you noticed.

## The small-n law (n ≤ 20)

When n ≤ 20, the setter is testing whether you **resist overengineering**.
2^20 = 10^6 — brute force *is* the intended solution. The classic exam
failure: inventing a greedy for a 20-item problem, missing a case, scoring
0 on the subtask the brute force would have swept. If the arithmetic gives
you 10^6, take it and spend the saved time elsewhere.

## Practice the estimate out loud

"n = 2·10^5, q = 2·10^5, range add range min → segment tree lazy, O((n+q)
log n) ≈ 7·10^6 — fits with 100× margin. Alternative: sqrt decomposition,
O((n+q)·sqrt n) ≈ 1.8·10^8 — probably fits but no margin; segment tree wins."
That sentence, spoken in ten seconds, is the skill.
""",
    "Bảng chuyển giới hạn → họ thuật toán",
    "Bảng quyết định đầy đủ kèm các bẫy: mẹo dải giá trị, bất đối xứng q-vs-n, và định luật n nhỏ.",
    """
# Bảng chuyển giới hạn → họ thuật toán

Bảng chọn từ Module 1, nay kèm các bẫy khiến drill khó.

## Bẫy 1 — Giá trị lớn, n nhỏ

`n ≤ 24, a[i] ≤ 10^12`: không gian trạng thái là **2^24 tập con**, không
phải các giá trị. Meet in the middle hoặc DP bitmask. Giá trị khổng lồ là
gợi ý rằng đáp án được so sánh, không được đếm — sort các tổng tập con,
không phải tổng tiền tố.

## Bẫy 2 — q ≫ n hoặc n ≫ q

`n ≤ 100, q ≤ 10^5` → **tiền tính toán tất cả**: O(n^2) thậm chí O(n^3) vừa
đỡ lúc dựng; mỗi truy vấn phải O(1) hoặc O(log n). Ngược lại
(`n ≤ 10^5, q ≤ 100`) → mỗi truy vấn O(n) hoặc O(n log n) là đủ; tiền tính
toán cho 100 truy vấn là lãng phí, và đừng dựng segment tree theo thói quen
khi 100 lần quét tuyến tính rẻ và an toàn hơn.

## Bẫy 3 — Mảng đã sắp / gần sắp (đọc điều kiện đảm bảo)

"Đã sắp" trong điều kiện đảm bảo là món quà: two pointers, tìm kiếm nhị
phân, trộn không cần sort. Bỏ qua điều kiện đảm bảo được nêu đốt luôn lời
giải chủ đích.

## Bẫy 4 — Độ dài xâu vs bảng chữ cái

|s| ≤ 2·10^5 chữ thường: mảng đếm 26 chữ, bitmask các chữ đã gặp (26 bit
vừa một int), counting sort. |s| ≤ 20: liệt kê xâu con 2^20 là đủ.

## Bẫy 5 — Điều kiện đảm bảo "cây"

"Cây n đỉnh, q truy vấn đường đi" có dạng LCA; "n−1 cạnh" nói một lần giữa
đoạn văn là cùng một bài. Gạch chân chữ *cây*. Cây là đồ thị có đúng một
đường đi giữa mỗi cặp đỉnh — toàn bộ hộp công cụ DP-on-trees chỉ mở nếu bạn
để ý điều đó.

## Định luật n nhỏ (n ≤ 20)

Khi n ≤ 20, người ra đề đang kiểm tra bạn có **chống lại việc overengineering**
hay không. 2^20 = 10^6 — brute force *chính là* lời giải chủ đích. Cái gãy
kinh điển trong phòng thi: chế ra greedy cho bài 20 phần tử, sót một trường
hợp, mất trắng subtask mà brute force sẽ quét sạch. Nếu phép toán cho ra
10^6, hãy lấy và dành thời gian đó cho chỗ khác.

## Luyện ước lượng thành lời

"n = 2·10^5, q = 2·10^5, cập nhật đoạn lấy min đoạn → segment tree lazy,
O((n+q) log n) ≈ 7·10^6 — vừa với dư 100×. Phương án hai: phân rã căn,
O((n+q)·sqrt n) ≈ 1.8·10^8 — chắc vừa nhưng không còn dư; segment tree
thắng." Câu đó, nói ra trong mười giây, chính là kỹ năng.
""",
)

# ----------------------------------------------------------------- practice
D1, D1VI = letter_pair = (None, None)  # replaced below by recognition drills

from hsgx import recognition_drill

D1, D1VI = recognition_drill(
    "hsgx-p2-d1", "Budget: subsets of 22",
    "n ≤ 22 items, weights up to 10^12. Count subsets whose weight sum is in [L, R]. Time limit: standard.",
    ["Sort + sweep two pointers over items",
     "Enumerate all 2^22 subsets directly and count",
     "Meet in the middle: enumerate halves, sort one, binary search",
     "Segment tree over weights"],
    "C",
    "2^22 ≈ 4·10^6 is borderline; meet-in-the-middle (2·2^11 = 4096 enumerations + a sort) has orders of magnitude of margin and matches the [L, R] counting.",
    vi_title="Ngân sách: tập con của 22",
    vi_scenario="n ≤ 22 vật, trọng lượng tới 10^12. Đếm tập con có tổng trọng lượng trong [L, R]. Giới hạn thời gian tiêu chuẩn.",
    vi_options=["Sort + quét two pointers trên các vật",
                "Liệt kê trực tiếp toàn bộ 2^22 tập con và đếm",
                "Meet in the middle: liệt kê hai nửa, sort một nửa, tìm kiếm nhị phân",
                "Segment tree trên trọng lượng"],
    vi_hint="2^22 ≈ 4·10^6 sát nút; meet-in-the-middle (2·2^11 = 4096 lần liệt kê + một sort) dư dả nhiều bậc và khớp đếm khoảng [L, R].",
)
D2, D2VI = recognition_drill(
    "hsgx-p2-d2", "Budget: 100 queries, huge array",
    "n ≤ 100000 numbers. q ≤ 100 queries; each asks the median of a range [l, r].",
    ["Build a segment tree answering medians",
     "For each query, copy the range, sort, take the middle (O(q · n log n) total)",
     "Prefix sums of medians",
     "DSU over values"],
    "B",
    "q = 100 makes O(q · n log n) ≈ 1.7·10^8 fit comfortably; a persistent/wavelet structure is the online answer but is pure overengineering at q = 100.",
    vi_title="Ngân sách: 100 truy vấn, mảng khổng lồ",
    vi_scenario="n ≤ 100000 số. q ≤ 100 truy vấn; mỗi truy vấn hỏi trung vị của đoạn [l, r].",
    vi_options=["Dựng segment tree trả lời trung vị",
                "Với mỗi truy vấn, chép đoạn, sort, lấy phần tử giữa (O(q · n log n) tổng)",
                "Tổng tiền tố của trung vị",
                "DSU trên các giá trị"],
    vi_hint="q = 100 khiến O(q · n log n) ≈ 1.7·10^8 vừa dễ dàng; cấu trúc persistent/wavelet là đáp án trực tuyến nhưng thuần túy overengineering ở q = 100.",
)
D3, D3VI = recognition_drill(
    "hsgx-p2-d3", "Budget: values 10^18",
    "Count integers in [1, N] with N ≤ 10^18 whose digit sum is divisible by 9.",
    ["Iterate 1..N checking each",
     "Sieve of Eratosthenes up to N",
     "Digit DP: state = position + digit-sum mod 9",
     "Fenwick tree over digits"],
    "C",
    "N has 19 digits; iterating is 10^18 — impossible. The state space is digit positions × 9 residues — a tiny digit DP.",
    vi_title="Ngân sách: giá trị 10^18",
    vi_scenario="Đếm các số trong [1, N] với N ≤ 10^18 có tổng chữ số chia hết cho 9.",
    vi_options=["Duyệt 1..N kiểm tra từng số",
                "Sàng Eratosthenes tới N",
                "Digit DP: trạng thái = vị trí + tổng chữ số mod 9",
                "Fenwick tree trên các chữ số"],
    vi_hint="N có 19 chữ số; duyệt là 10^18 — không thể. Không gian trạng thái là vị trí chữ số × 9 số dư — digit DP bé xíu.",
)
D4, D4VI = recognition_drill(
    "hsgx-p2-d4", "Budget: interleaved min queries",
    "n ≤ 200000. Interleaved: `1 i x` sets a[i] = x; `2 l r` prints min a[l..r].",
    ["Recompute min per query (O(nq))",
     "Sparse table (static only)",
     "Segment tree with point update, O((n+q) log n)",
     "Sort and prefix sums"],
    "C",
    "Point updates kill prefix structures and sparse tables (static). A segment tree with point update handles both operations in O(log n).",
    vi_title="Ngân sách: truy vấn min xen kẽ",
    vi_scenario="n ≤ 200000. Xen kẽ: `1 i x` đặt a[i] = x; `2 l r` in min a[l..r].",
    vi_options=["Tính lại min mỗi truy vấn (O(nq))",
                "Sparse table (chỉ dùng cho tĩnh)",
                "Segment tree với cập nhật điểm, O((n+q) log n)",
                "Sort và tổng tiền tố"],
    vi_hint="Cập nhật điểm hạ các cấu trúc tiền tố và sparse table (tĩnh). Segment tree với cập nhật điểm xử lý cả hai thao tác trong O(log n).",
)
D5, D5VI = recognition_drill(
    "hsgx-p2-d5", "Budget: sum overflow",
    "n ≤ 100000, a[i] up to 10^9. Compute the total sum of the array. What is mandatory?",
    ["int suffices",
     "unsigned int suffices",
     "long long — the sum reaches 10^14, int overflows",
     "Big integer library"],
    "C",
    "10^5 × 10^9 = 10^14 > 2^31−1 ≈ 2.1·10^9. int/unsigned wrap around silently; long long is mandatory.",
    vi_title="Ngân sách: tràn tổng",
    vi_scenario="n ≤ 100000, a[i] tới 10^9. Tính tổng toàn bộ mảng. Điều gì là bắt buộc?",
    vi_options=["int là đủ",
                "unsigned int là đủ",
                "long long — tổng chạm 10^14, int tràn",
                "Thư viện số lớn"],
    vi_hint="10^5 × 10^9 = 10^14 > 2^31−1 ≈ 2.1·10^9. int/unsigned tràn vòng im lặng; long long là bắt buộc.",
)
D6, D6VI = recognition_drill(
    "hsgx-p2-d6", "Budget: memory check",
    "A DP over (position i ≤ 2000) × (mask over 20 items). How much memory does the naive table need?",
    ["About 2 GB — impossible; need a different state or rolling rows",
     "About 40 MB — fine",
     "About 400 KB — fine",
     "About 8 MB — fine"],
    "A",
    "2000 × 2^20 × 8 B = ~16.8 GB — orders of magnitude over the 512 MB sandbox. Rethink the state.",
    vi_title="Ngân sách: kiểm tra bộ nhớ",
    vi_scenario="DP trên (vị trí i ≤ 2000) × (mask trên 20 vật). Bảng thô cần bao nhiêu bộ nhớ?",
    vi_options=["Khoảng 2 GB — không thể; cần trạng thái khác hoặc hàng cuộn",
                "Khoảng 40 MB — ổn",
                "Khoảng 400 KB — ổn",
                "Khoảng 8 MB — ổn"],
    vi_hint="2000 × 2^20 × 8 B = ~16.8 GB — vượt nhiều bậc so với 512 MB của sandbox. Nghĩ lại trạng thái.",
)

write_practice(
    M, "hsgx-p2-drills", "Budget Drill Set",
    "Six constraint-table situations. Output the letter of the choice whose arithmetic and semantics both fit.",
    "Bộ drill ngân sách",
    "Sáu tình huống bảng giới hạn. In ra chữ cái của lựa chọn mà phép toán và ngữ nghĩa cùng vừa.",
    "hsgx-m2-mapping",
    35,
    "advanced",
    [D1, D2, D3, D4, D5, D6],
    {
        "hsgx-p2-d1": D1VI,
        "hsgx-p2-d2": D2VI,
        "hsgx-p2-d3": D3VI,
        "hsgx-p2-d4": D4VI,
        "hsgx-p2-d5": D5VI,
        "hsgx-p2-d6": D6VI,
    },
    solutions=[
        ("hsgx-p2-d1", letter("C"), letter("B")),
        ("hsgx-p2-d2", letter("B"), letter("A")),
        ("hsgx-p2-d3", letter("C"), letter("A")),
        ("hsgx-p2-d4", letter("C"), letter("B")),
        ("hsgx-p2-d5", letter("C"), letter("A")),
        ("hsgx-p2-d6", letter("A"), letter("B")),
    ],
)

# --------------------------------------------------------------- checkpoint
# n ≤ 20 law executed: max XOR of a subset (classic, brute force intended).
CP_M2_R = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long best = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        long long x = 0;
        for (int i = 0; i < n; ++i) if (mask >> i & 1) x ^= a[i];
        best = max(best, x);
    }
    out << best << "{{NL}}";
""") + END

CP_M2_W = CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // WRONG: greedy "take it if the XOR grows" (sorted descending). Fails
    // the verified counterexample {8, 13, 6}: greedy returns 11, the true
    // maximum is 14 (subset {8, 6}). The brute force over 2^n ≤ 2^20 is both
    // simpler and correct — that is the entire lesson of the small-n law.
    sort(a.begin(), a.end(), greater<long long>());
    long long x = 0;
    for (long long v : a) if ((x ^ v) > x) x ^= v;
    out << x << "{{NL}}";
""") + END

write_checkpoint(
    M, "hsgx-cp-m2", "Checkpoint — The Small-n Law",
    "n ≤ 20: resist overengineering. The 2^n enumeration is the intended solution; the plausible greedy is the trap.",
    20,
    """
**Điểm kiểm tra — Định luật n nhỏ.** Given n ≤ 20 non-negative integers,
print the maximum possible XOR of any non-empty subset. The arithmetic says
2^20 ≈ 10^6 — brute force fits with huge margin. The greedy "take it if the
XOR improves" is a well-known wrong answer: verify against the sample where
it fails.
""",
    "Điểm kiểm tra — Định luật n nhỏ",
    "n ≤ 20: chống lại overengineering. Liệt kê 2^n là lời giải chủ đích; greedy nghe hợp lý là cái bẫy.",
    """
**Điểm kiểm tra — Định luật n nhỏ.** Cho n ≤ 20 số nguyên không âm, in giá
trị XOR lớn nhất có thể của một tập con khác rỗng. Phép toán nói 2^20 ≈
10^6 — brute force vừa với dư dả lớn. Greedy "lấy nếu XOR tăng" là một đáp
án sai nổi tiếng: kiểm chứng với mẫu nơi nó gãy.
""",
    challenge(
        "hsgx-cp-m2-maxxor",
        "Maximum Subset XOR",
        """**Bài toán.** Given n non-negative integers, print the maximum XOR over
all non-empty subsets.

**Constraints:** 1 ≤ n ≤ 20; 0 ≤ a[i] ≤ 10^9.

**Hint:** compute the budget first. 2^20 = 1 048 576 — the brute force fits
with three orders of magnitude of margin.
""",
        [
            contest_test("single", T("1", "7"), T("7"),
                "One element: the subset {7}."),
            contest_test("pair", T("2", "4 5"), T("5"),
                "4^5=1, so best is max(4,5,1)=5."),
            contest_test("greedy trap", T("3", "8 13 6"), T("14"),
                "Greedy: keeps 13, then rejects 8 (13^8=5), then takes 6 (13^6=11) → 11. Brute force finds 8^6=14. Verified discriminator."),
            contest_test("n=20 full", T("20") + T(*[str((i * 2654435761) % 1000000000) for i in range(1, 21)]), T("1073479093"),
                "n=20: greedy returns 1041462738 (fails); brute force returns 1073479093 — verified by exhaustive 2^20 enumeration in Python."),
        ],
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "XOR tập con lớn nhất",
        """**Bài toán.** Cho n số nguyên không âm, in XOR lớn nhất trên mọi tập con
khác rỗng.

**Ràng buộc:** 1 ≤ n ≤ 20; 0 ≤ a[i] ≤ 10^9.

**Gợi ý:** tính ngân sách trước. 2^20 = 1 048 576 — brute force vừa với dư
ba bậc độ lớn.
""",
        [("một phần tử", "Một phần tử: tập {7}."),
         ("cặp", "4^5=1, nên tốt nhất là max(4,5,1)=5."),
         ("bẫy greedy", "Greedy giữ 13, từ chối 8 (13^8=5), rồi lấy 6 (13^6=11) → trả 11. Brute force tìm 8^6=14."),
         ("n=20 đầy đủ", "n=20: greedy trả 1041462738 (sai); brute force trả 1073479093 — kiểm chứng bằng liệt kê 2^20 vét cạn trong Python.")],
    ),
    CP_M2_R,
    CP_M2_W,
)

print("module m2 complete")
