#!/usr/bin/env python3
"""HSG Intermediate — Module 1: hsgi-analysis (algorithm analysis).

Operation budgets (how many ops does 20 s of -O0 actually buy), amortized
reasoning (why repeated halving/doubling is cheap), meet-in-the-middle,
sparse tables for static RMQ, and sweep-line event triples. The one lesson
that every later module leans on: read the constraints, compute the budget,
choose the tool.

Conventions (proven in hsg m6–m20): zero literal backslashes in this source.
Test I/O strings use T() (real newlines). C++ bodies use cpp() which turns
the {{NL}} marker into a backslash-n escape inside C++ string literals.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsgi import (
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
#include <map>
#include <cmath>
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-analysis"
write_module(
    M,
    "Algorithm Analysis — Budgets, Amortized, and Meet-in-the-Middle",
    "Turn constraints into an operation budget, recognize amortized cost, split search spaces in half, preprocess static ranges, and convert intervals into events.",
    "Phân tích thuật toán — Ngân sách, khấu hao, và chia để trị tìm kiếm",
    "Biến ràng buộc thành ngân sách phép toán, nhận diện chi phí khấu hao, chia không gian tìm kiếm làm hai, tiền xử lý đoạn tĩnh, và biến đoạn thành sự kiện.",
    ["hsgi-m1-budget", "hsgi-m1-mitm", "hsgi-cp-m1"],
    ["hsgi-p1-analysis"],
)

# ---------------------------------------------------------------- lesson 1.1
write_lesson(
    M,
    "hsgi-m1-budget",
    "The Operation Budget — Reading Constraints Like a Contestant",
    "Estimate how many operations the judge actually buys, classify complexities against real limits, and pick a complexity class before writing code.",
    16,
    """## The 20-second question

At HSG provincials your program gets a time limit measured in seconds; here a
submission job gets **20 seconds for compile + all tests**. The honest skill is
not memorizing "N ≤ 10^5 means O(N log N)" — it is *computing the budget*:

```text
budget ≈ (time limit) × (operations per second your code achieves)
```

Under `-O0` (how graded tests build here) simple loops run roughly **10^7–10^8
elementary ops per second**. So for a 2-second-problem mindset, plan on
**≈ 10^8 ops** and leave slack for constants (recursion, division, map lookups).

### Constraint → complexity table

| Constraint (n) | Max acceptable | Why |
| --- | --- | --- |
| ≤ 12 | O(n!) | permutations: 12! ≈ 4.8·10^8 |
| ≤ 24 | O(2^(n/2) · poly) | meet-in-the-middle |
| ≤ 25 | O(2^n) | subsets: 2^25 = 3.3·10^7 |
| ≤ 5 000 | O(n^2) | 2.5·10^7 |
| ≤ 100 000 | O(n log n), O(n √n) | 10^6 · log |
| ≤ 10^7 | O(n) | with tiny constant |

These are planning numbers, not laws — a heavy inner loop (division, modulo,
map) costs 10–50× a simple add. When in doubt, test locally.

### Worked example — from constraint to algorithm

"Bài toán: n ≤ 100 000 điểm, q ≤ 100 000 truy vấn đoạn [l, r], mỗi truy vấn
tính tổng. Time limit 2 s."

Budget: (n + q) must fit ~10^8 → per-query work must be **O(1)** → prefix sums
(Beginner M8), or Fenwick (this course, M6) if values update.

```cpp
// The instinct to check: is there an update between queries?
//   no updates  → prefix sums O(n + q)
//   updates     → Fenwick tree O((n + q) log n)
```

### Amortized reasoning — the halving trap

How many times can you halve n until it reaches 1? ⌊log2 n⌋ + 1. For
n = 10^9 that is **30**. So:

- doubling/halving loops are O(log n), never O(n)
- building a segment tree over n leaves is O(n) total (sum of 2^k levels)
- repeatedly extracting the max n times from a heap is O(n log n), but
  *building* the heap bottom-up is O(n) — amortized, most nodes sift little

### Recognizing amortized problems

Keywords: "mỗi phần tử được thêm và xóa tối đa một lần", "queue simulated by
two stacks", "đường đi không quay lại". If each element causes O(1) work
across the whole run, the *total* is O(n) even when a single step looks
expensive.

## Practice recognition (write the answer before running code)

For each: n = 200 000, q = 200 000. Is O(nq) acceptable? What is?
(Answer: no — 4·10^10. Prefix sums / Fenwick / offline sweep, depending on
what the query asks.)

**Next:** [Meet-in-the-Middle](./hsgi-m1-mitm)""",
    "Phân tích thuật toán — Đọc ràng buộc như một thí sinh",
    "Ước lượng số phép toán máy chấm thực sự cho phép, phân loại độ phức tạp theo giới hạn thực, và chọn lớp độ phức tạp trước khi viết code.",
    """## Câu hỏi 20 giây

Ở HSG cấp tỉnh, bài của bạn có giới hạn thời gian tính bằng giây; ở đây một
lần nộp có **20 giây cho cả compile và toàn bộ test**. Kỹ năng thật không phải
là học thuộc "N ≤ 10^5 nghĩa là O(N log N)" — mà là *tính ngân sách*:

```text
ngân sách ≈ (giới hạn thời gian) × (phép toán/giây code của bạn đạt được)
```

Với `-O0` (cách test được build) vòng lặp đơn giản chạy cỡ **10^7–10^8 phép
toán cơ bản mỗi giây**. Vậy với tư duy đề 2 giây, hãy nhắm **≈ 10^8 phép
toán** và để dư cho hằng số (đệ quy, phép chia, lookup trên map).

### Bảng ràng buộc → độ phức tạp

| Ràng buộc (n) | Chấp nhận được tối đa | Vì sao |
| --- | --- | --- |
| ≤ 12 | O(n!) | hoán vị: 12! ≈ 4.8·10^8 |
| ≤ 24 | O(2^(n/2) · đa thức) | chia để trị tìm kiếm |
| ≤ 25 | O(2^n) | tập con: 2^25 = 3.3·10^7 |
| ≤ 5 000 | O(n^2) | 2.5·10^7 |
| ≤ 100 000 | O(n log n), O(n √n) | 10^6 · log |
| ≤ 10^7 | O(n) | hằng số nhỏ |

Đây là số *lập kế hoạch*, không phải định luật — một vòng trong nặng (chia,
modulo, map) tốn gấp 10–50 lần một phép cộng. Nghĩ không chắc thì tự đo.

### Ví dụ làm mẫu — từ ràng buộc đến thuật toán

"Bài toán: n ≤ 100 000 điểm, q ≤ 100 000 truy vấn đoạn [l, r], mỗi truy vấn
tính tổng. Time limit 2 s."

Ngân sách: (n + q) phải gói trong ~10^8 → mỗi truy vấn phải **O(1)** → mảng
cộng dồn (Beginner M8), hoặc cây Fenwick (khóa này, M6) nếu giá trị có cập nhật.

```cpp
// Bản năng cần kiểm tra: giữa các truy vấn có cập nhật không?
//   không cập nhật → mảng cộng dồn O(n + q)
//   có cập nhật    → Fenwick O((n + q) log n)
```

### Suy luận khấu hao — cái bẫy chia đôi

Chia n đôi bao nhiêu lần đến 1? ⌊log2 n⌋ + 1. Với n = 10^9 là **30**. Vậy:

- vòng lặp nhân đôi/chia đôi là O(log n), không bao giờ O(n)
- dựng segment tree trên n lá tốn O(n) tổng (tổng các tầng 2^k)
- n lần lấy max từ heap là O(n log n), nhưng *dựng* heap bottom-up là O(n) —
  khấu hao, vì đa số node sift rất ít

### Nhận diện bài khấu hao

Từ khóa: "mỗi phần tử được thêm và xóa tối đa một lần", "queue dựng bằng hai
stack", "đường đi không quay lại". Nếu mỗi phần tử chỉ gây O(1) công trong cả
quá trình thì *tổng* là O(n) dù một bước đơn lẻ trông đắt.

## Luyện nhận diện (viết đáp án trước khi chạy code)

Với mỗi ý: n = 200 000, q = 200 000. O(nq) được không? Thay bằng gì?
(Đáp án: không — 4·10^10. Cộng dồn / Fenwick / quét offline, tùy truy vấn.)

**Tiếp:** [Chia để trị tìm kiếm](./hsgi-m1-mitm)""",
)

# ---------------------------------------------------------------- lesson 1.2
write_lesson(
    M,
    "hsgi-m1-mitm",
    "Meet-in-the-Middle, Sparse Tables, and Sweep Events",
    "Split exponential search spaces, answer static range queries in O(1), and turn interval problems into sorted event lists.",
    18,
    """## Meet-in-the-middle — 2^n becomes 2^(n/2)

n ≤ 40 kills plain brute force (2^40 ≈ 10^12). But 2^20 ≈ 10^6 — split the
items in half, enumerate each side separately, then combine.

Classic: "choose a subset of n ≤ 40 numbers with sum closest to S".

```cpp
// enumerate all subset sums of each half, sort one side,
// for each x in side A binary-search the best partner in side B
vector<long long> sumsA, sumsB;   // 2^20 each — fits
sort(sumsB.begin(), sumsB.end());
for (long long x : sumsA) {
    // need y ≈ S - x: two binary searches bracket the best candidate
}
```

Cost: 2·2^(n/2) enumeration + 2^(n/2) · log searches. For n = 40: ~2·10^6 · 21.

### Sparse table — static RMQ in O(1)

If the array **never changes**, a segment tree is overkill. Sparse table
precomputes min over every power-of-two block: O(n log n) memory/time build,
then `min(st[k][l], st[k][r - 2^k + 1])` answers any range min in O(1)
(the two blocks may overlap — harmless for min/max, fatal for sums).

```cpp
int K = 1; while ((1 << K) <= n) ++K;
vector<vector<int>> st(K, vector<int>(n + 1));
st[0] = a;
for (int k = 1; k < K; ++k)
    for (int i = 1; i + (1 << k) - 1 <= n; ++i)
        st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))]);
// query [l, r]:
int k = __lg(r - l + 1);            // floor log2
answer = min(st[k][l], st[k][r - (1 << k) + 1]);
```

Recognition: "n, q ≤ 2·10^5, array static, query = min/max/gcd on range".
If there are updates → Fenwick/segment tree (M6–M7).

### Sweep events — intervals as ±1 triples

Any problem of the form "how many intervals cover point x / what is the max
overlap" becomes sorting 2n events: `(start, +1)`, `(end+1, −1)`, then one
prefix pass.

```cpp
vector<tuple<int,int,int>> ev;              // (coordinate, delta)
for (auto [l, r] : intervals) {
    ev.push_back({l, +1});
    ev.push_back({r + 1, -1});              // end+1: closed [l, r]
}
sort(ev.begin(), ev.end());
int cur = 0, best = 0;
for (auto [x, d] : ev) { cur += d; best = max(best, cur); }
```

Two traps worth naming:
1. **end vs end+1** — closed intervals touching at a point (r1 = l2) count as
   overlap if you add +1 at l and −1 at r. Decide the convention from the
   statement, not from habit.
2. **same-coordinate order** — if the answer must count intervals *starting*
   before others *end*, sort starts before ends at equal coordinates. The
   delta sign encodes this automatically when you use r+1 for ends.

**Next:** [Checkpoint](./hsgi-cp-m1)""",
    "Chia để trị tìm kiếm, bảng thưa, và quét sự kiện",
    "Chia nhỏ không gian tìm kiếm dạng mũ, trả lời truy vấn đoạn tĩnh trong O(1), và biến bài toán khoảng thành danh sách sự kiện có thứ tự.",
    """## Chia để trị tìm kiếm — 2^n thành 2^(n/2)

n ≤ 40 hạ gục vét cạn thường (2^40 ≈ 10^12). Nhưng 2^20 ≈ 10^6 — chia các
phần tử làm hai nửa, liệt kê từng nửa, rồi ghép.

Kinh điển: "chọn tập con của n ≤ 40 số có tổng gần S nhất".

```cpp
// liệt kê mọi tổng tập con của từng nửa, sắp xếp một phía,
// với mỗi x ở nửa A tìm nhị phân bạn tốt nhất ở nửa B
vector<long long> sumsA, sumsB;   // 2^20 mỗi nửa — vừa
sort(sumsB.begin(), sumsB.end());
for (long long x : sumsA) {
    // cần y ≈ S - x: hai chăm nhị phân giới hạn ứng viên tốt nhất
}
```

Chi phí: liệt kê 2·2^(n/2) + tìm kiếm 2^(n/2) · log. Với n = 40: ~2·10^6 · 21.

### Bảng thưa — RMQ tĩnh trong O(1)

Nếu mảng **không bao giờ đổi**, segment tree là thừa. Bảng thưa tiền xử lý min
trên mọi khối lũy thừa 2: dựng O(n log n) bộ nhớ/thời gian, rồi
`min(st[k][l], st[k][r - 2^k + 1])` trả lời bất kỳ truy vấn min đoạn nào trong
O(1) (hai khối có thể chồng nhau — vô hại với min/max, chết người với tổng).

```cpp
int K = 1; while ((1 << K) <= n) ++K;
vector<vector<int>> st(K, vector<int>(n + 1));
st[0] = a;
for (int k = 1; k < K; ++k)
    for (int i = 1; i + (1 << k) - 1 <= n; ++i)
        st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))]);
// truy vấn [l, r]:
int k = __lg(r - l + 1);            // floor log2
answer = min(st[k][l], st[k][r - (1 << k) + 1]);
```

Nhận diện: "n, q ≤ 2·10^5, mảng tĩnh, truy vấn = min/max/gcd trên đoạn".
Nếu có cập nhật → Fenwick/segment tree (M6–M7).

### Quét sự kiện — khoảng thành bộ ba ±1

Mọi bài dạng "bao nhiêu đoạn phủ điểm x / phủ trùng nhiều nhất là bao nhiêu"
đưa về sắp xếp 2n sự kiện: `(bắt_đầu, +1)`, `(kết_thúc+1, −1)`, rồi một lượt
quét cộng dồn.

```cpp
vector<tuple<int,int,int>> ev;              // (tọa độ, biến thiên)
for (auto [l, r] : intervals) {
    ev.push_back({l, +1});
    ev.push_back({r + 1, -1});              // end+1: đoạn đóng [l, r]
}
sort(ev.begin(), ev.end());
int cur = 0, best = 0;
for (auto [x, d] : ev) { cur += d; best = max(best, cur); }
```

Hai cái bẫy đáng nêu tên:
1. **end so với end+1** — các đoạn đóng chạm nhau tại một điểm (r1 = l2) bị
   tính là phủ trùng nếu bạn cộng +1 tại l và −1 tại r. Quy ước phải lấy từ đề.
2. **thứ tự cùng tọa độ** — nếu đáp án phải đếm đoạn *bắt đầu* trước khi đoạn
   khác *kết thúc*, sắp các sự kiện bắt đầu trước kết thúc tại cùng tọa độ.
   Dấu biến thiên tự mã hóa điều này khi kết thúc dùng r+1.

**Tiếp:** [Điểm kiểm tra](./hsgi-cp-m1)""",
)

# ---------------------------------------------------------------- practice
A1 = challenge(
    "hsgi-p1-budget",
    "Truy vấn tổng trên mảng tĩnh",
    """**Bài toán.** Cho mảng n phần tử và q truy vấn. Mỗi truy vấn cho l, r:
in tổng a[l..r]. Mảng **không bao giờ thay đổi**.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |a[i]| ≤ 10^9; 1 ≤ l ≤ r ≤ n.

**Định dạng vào:** dòng đầu n q; dòng hai n phần tử; q dòng tiếp: l r.

**Định dạng ra:** q dòng, mỗi dòng một tổng.

**Điểm:** 100 (bài này là bài khởi động — nhưng vẫn chấm từng byte).""",
    [
        contest_test(
            "ví dụ",
            T("5 3", "1 2 3 4 5", "1 3", "2 2", "1 5"),
            T("6", "2", "15"),
            "Prefix sums: P[0]=0, P[i]=P[i-1]+a[i]; tổng [l,r] = P[r] - P[l-1].",
        ),
        contest_test(
            "một phần tử, truy vấn biên",
            T("1 2", "-7", "1 1", "1 1"),
            T("-7", "-7"),
            "l = r phải trả về a[l]; giá trị âm hợp lệ — dùng long long cho tổng.",
        ),
        contest_test(
            "giá trị âm xen kẽ",
            T("4 2", "5 -5 5 -5", "1 4", "2 3"),
            T("0", "0"),
            "Tổng có thể bằng 0 — vẫn phải in ra dòng 0.",
        ),
        contest_test(
            "n lớn (kiểm ngân sách)",
            T("200000 2") + T(" ".join(["1"] * 200000), "1 200000", "100000 150000"),
            T("200000", "50001"),
            "n, q = 2·10^5: mỗi truy vấn phải O(1) — cộng dồn, không cộng tay từng truy vấn. (Đoạn 100000..150000 có 50001 phần tử!)",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p1-rmq",
    "Min trên đoạn tĩnh",
    """**Bài toán.** Cho mảng n phần tử và q truy vấn (l, r): in min(a[l..r]).
Mảng **tĩnh** — không có cập nhật.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |a[i]| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n phần tử; q dòng: l r.
**Ra:** q dòng, mỗi dòng một min.

**Điểm:** 100. Subtask 1 (40 điểm): n, q ≤ 5 000 — O(nq) được. Subtask 2
(60 điểm): full — cần tiền xử lý.""",
    [
        contest_test(
            "ví dụ",
            T("6 3", "3 1 4 1 5 9", "1 3", "2 4", "4 6"),
            T("1", "1", "1"),
            "Sparse table hoặc segment tree đều được — mảng tĩnh nên sparse table cho O(1)/truy vấn.",
        ),
        contest_test(
            "min ở biên",
            T("3 2", "-2 -1 0", "1 1", "3 3"),
            T("-2", "0"),
            "Đoạn độ dài 1: k = 0, khối 2^0 — công thức không được truy cập ngoài mảng.",
        ),
        contest_test(
            "min nằm ở phần tử cuối",
            T("3 1", "9 9 1", "1 3"),
            T("1"),
            "Độ dài 3 (k=1): cửa sổ đúng là [l,l+1] ∪ [r−1,r] — nếu nhóm nhầm r−2^k thì mất phần tử cuối và trả 9.",
        ),
        contest_test(
            "n lớn xen kẽ",
            T("200000 3") + T(" ".join(str(200001 - (i % 5000)) for i in range(200000)), "1 200000", "1 1", "200000 200000"),
            T("195002", "200001", "195002"),
            "Biên độ 1 và 2·10^5: mỗi truy vấn O(1); O(nq) sẽ chết ngân sách. Giá trị nhỏ nhất trong chu kỳ là 200001−4999.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p1-overlap",
    "Đoạn phủ trùng nhiều nhất",
    """**Bài toán.** Cho n đoạn [l_i, r_i] (đóng hai đầu). Điểm bị nhiều đoạn phủ
nhất được phủ bởi bao nhiêu đoạn? In số đó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ l_i ≤ r_i ≤ 10^9 (tọa độ lớn — không quét
mảng đánh dấu!).

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** một số — độ phủ lớn nhất.

**Điểm:** 100. Lưu ý: tọa độ tới 10^9 → nén tọa độ hoặc quét sự kiện, không
được dựng mảng kích thước 10^9.""",
    [
        contest_test(
            "ví dụ",
            T("3", "1 4", "2 5", "7 8"),
            T("2"),
            "Điểm 2..4 bị hai đoạn đầu phủ → 2. Nếu −1 tại r thay vì r+1, điểm r bị gỡ sớm.",
        ),
        contest_test(
            "chạm tại một điểm KHÔNG trùng",
            T("2", "1 3", "4 6"),
            T("1"),
            "Đoạn đóng [1,3] và [4,6] chạm nhau tại... không điểm nào chung — r+1 của đoạn một là 4, đúng lúc đoạn hai bắt đầu: phủ tối đa 1.",
        ),
        contest_test(
            "chạm đúng tại một điểm — TRộNG",
            T("2", "1 3", "3 5"),
            T("2"),
            "Đoạn đóng [1,3] và [3,5] cùng phủ điểm 3 → đáp án 2. Nếu −1 tại r thay vì r+1 thì điểm 3 bị gỡ sớm: ra 1.",
        ),
        contest_test(
            "n lớn, tọa độ 10^9",
            T("6", "1 1000000000", "2 999999999", "3 999999998", "4 7", "5 6", "1000000000 1000000000"),
            T("5"),
            "Điểm 5 bị cả năm đoạn phủ (ba đoạn dài + [4,7] + [5,6]); tọa độ 10^9 buộc quét sự kiện, tuyệt đối không mảng đánh dấu.",
        ),
        contest_test(
            "toàn bộ bằng nhau",
            T("3", "5 10", "5 10", "5 10"),
            T("3"),
            "Ba đoạn giống nhau: mọi điểm bị cả ba phủ.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p1-subset-sum",
    "Tập con tổng gần S nhất (chia để trị tìm kiếm)",
    """**Bài toán.** Cho n số và tổng mục tiêu S. Chọn một tập con (có thể rỗng)
có |tổng − S| nhỏ nhất. In hiệu đó.

**Ràng buộc:** 1 ≤ n ≤ 30; |a[i]| ≤ 10^9; |S| ≤ 10^12.

**Vào:** dòng đầu n S; dòng hai n số.
**Ra:** một số — min |tổng tập con − S| (tập rỗng cho 0).

**Điểm:** 100. 2^30 ≈ 10^9 — vét cạn thường quá chậm ở -O0. Chia đôi.""",
    [
        contest_test(
            "ví dụ",
            T("4 10", "3 5 7 9"),
            T("0"),
            "3 + 7 = 10. Liệt kê từng nửa 2^15, sắp một nửa, chăm nhị phân bạn của S − x.",
        ),
        contest_test(
            "tập rỗng tốt nhất",
            T("3 100", "1 2 3"),
            T("94"),
            "Không tổ hợp nào gần 100 hơn tập rỗng (hiệu 94) — đáp án có thể đến từ nửa rỗng.",
        ),
        contest_test(
            "n = 1",
            T("1 5", "8"),
            T("3"),
            "Chọn 8 (hiệu 3) hay rỗng (hiệu 5): 3. Cần xử lý cả hai nửa khi n lẻ.",
        ),
        contest_test(
            "n = 30 (kích thước thật)",
            T("30 123456789") + T(" ".join(str(10**9 - i * 7) for i in range(30))),
            T("123456789"),
            "2^15×2 = 65536 tổng + sắp xếp + 32768 chăm nhị phân: chạy ngay lập tức; 2^30 thì không. Mọi phần tử ≈ 10^9 đều vượt xa S = 1.2·10^8 nên tập rỗng thắng: hiệu = S.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p1-vacation",
    "Lịch nghỉ trùng lịch thi",
    """**Bài toán.** Một quán sách cho n học sinh mượn bàn. Học sinh i ngồi từ
ngày l_i đến ngày r_i (đóng hai đầu). Kỳ nghỉ của học sinh được tính "chật"
nếu có **quá k** học sinh cùng ngồi trong một ngày. Ngày chật **đầu tiên**
(tính từ ngày 1) là ngày nào? Nếu không có, in −1.

**Ràng buộc:** 1 ≤ n, k ≤ 200 000; 1 ≤ l_i ≤ r_i ≤ 10^9.

**Vào:** dòng đầu n k; n dòng: l r.
**Ra:** ngày chật đầu tiên hoặc −1.

**Điểm:** 100. Đề bài trừu tượng hóa từ lịch thi/lịch mượn — đọc kỹ "quá k"
(> k, không phải ≥ k) và "đầu tiên" (min tọa độ đạt ngưỡng, không phải thời
điểm sớm nhất của đoạn nào đó).""",
    [
        contest_test(
            "ví dụ",
            T("4 1", "1 3", "2 4", "5 6", "3 3"),
            T("2"),
            "Ngày 2 đã có 2 học sinh (đoạn 1..3 và 2..4) > 1 → ngày chật đầu tiên là 2, không phải 3.",
        ),
        contest_test(
            "chính xác k không phải chật",
            T("2 2", "1 5", "1 5"),
            T("-1"),
            "Quá k nghĩa là > k. Đúng 2 học sinh với k = 2: không chật, in −1.",
        ),
        contest_test(
            "không giao nhau",
            T("2 0", "1 2", "4 5"),
            T("1"),
            "k = 0: ngày đầu tiên có ≥ 1 học sinh (ngày 1) là chật → đáp án 1.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)
VI1 = {
    "hsgi-p1-budget": vi_challenge(
        "Truy vấn tổng trên mảng tĩnh",
        """**Bài toán.** Cho mảng n phần tử và q truy vấn. Mỗi truy vấn cho l, r:
in tổng a[l..r]. Mảng **không bao giờ thay đổi**.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |a[i]| ≤ 10^9; 1 ≤ l ≤ r ≤ n.

**Định dạng vào:** dòng đầu n q; dòng hai n phần tử; q dòng tiếp: l r.

**Định dạng ra:** q dòng, mỗi dòng một tổng.""",
        [("ví dụ", "Cộng dồn một lần, mỗi truy vấn O(1): P[r] − P[l−1]."),
         ("một phần tử, truy vấn biên", "l = r trả về a[l]; dùng long long."),
         ("giá trị âm xen kẽ", "Tổng 0 vẫn in dòng 0."),
         ("n lớn (kiểm ngân sách)", "2·10^5 truy vấn: cấm cộng tay.")],
    ),
    "hsgi-p1-rmq": vi_challenge(
        "Min trên đoạn tĩnh",
        """**Bài toán.** Cho mảng n phần tử và q truy vấn (l, r): in min(a[l..r]).
Mảng **tĩnh** — không có cập nhật.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |a[i]| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n phần tử; q dòng: l r.
**Ra:** q dòng, mỗi dòng một min.

**Điểm:** 100. Subtask 1 (40 điểm): n, q ≤ 5 000. Subtask 2 (60 điểm): full.""",
        [("ví dụ", "Sparse table: dựng O(n log n), trả lời O(1)."),
         ("min ở biên", "Đoạn độ dài 1: k = 0, cấm truy cập ngoài mảng."),
         ("toàn bộ bằng nhau", "Phát hiện lỗi đọc/chồng khối."),
         ("n lớn xen kẽ", "Mỗi truy vấn O(1) — O(nq) chết ngân sách.")],
    ),
    "hsgi-p1-overlap": vi_challenge(
        "Đoạn phủ trùng nhiều nhất",
        """**Bài toán.** Cho n đoạn [l_i, r_i] (đóng hai đầu). Điểm bị nhiều đoạn phủ
nhất được phủ bởi bao nhiêu đoạn? In số đó.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ l_i ≤ r_i ≤ 10^9 (tọa độ lớn!).

**Vào:** dòng đầu n; n dòng: l r.
**Ra:** một số — độ phủ lớn nhất.""",
        [("ví dụ", "Sự kiện +1 tại l, −1 tại r+1; quét lấy max."),
         ("chạm tại một điểm KHÔNG trùng", "[1,3] và [4,6]: phủ tối đa 1."),
         ("chồng hoàn toàn", "Ba đoạn giống nhau: 3."),
         ("n lớn, tọa độ 10^9", "Quét 2n sự kiện — cấm mảng đánh dấu 10^9.")],
    ),
    "hsgi-p1-subset-sum": vi_challenge(
        "Tập con tổng gần S nhất (chia để trị tìm kiếm)",
        """**Bài toán.** Cho n số và tổng mục tiêu S. Chọn một tập con (có thể rỗng)
có |tổng − S| nhỏ nhất. In hiệu đó.

**Ràng buộc:** 1 ≤ n ≤ 30; |a[i]| ≤ 10^9; |S| ≤ 10^12.

**Vào:** dòng đầu n S; dòng hai n số.
**Ra:** một số — min |tổng tập con − S| (tập rỗng cho 0).

**Điểm:** 100. 2^30 quá chậm — chia đôi.""",
        [("ví dụ", "3 + 7 = 10 → hiệu 0."),
         ("tập rỗng tốt nhất", "Hiệu 94 từ tập rỗng."),
         ("n = 1", "Xử lý cả hai nửa khi n lẻ."),
         ("n = 30 (kích thước thật)", "2×2^15 tổng + chăm nhị phân: tức thì.")],
    ),
    "hsgi-p1-vacation": vi_challenge(
        "Lịch nghỉ trùng lịch thi",
        """**Bài toán.** Một quán sách cho n học sinh mượn bàn. Học sinh i ngồi từ
ngày l_i đến ngày r_i (đóng hai đầu). Ngày "chật" nếu có **quá k** học sinh
cùng ngồi trong một ngày. Ngày chật **đầu tiên** là ngày nào? Nếu không có, in −1.

**Ràng buộc:** 1 ≤ n, k ≤ 200 000; 1 ≤ l_i ≤ r_i ≤ 10^9.

**Vào:** dòng đầu n k; n dòng: l r.
**Ra:** ngày chật đầu tiên hoặc −1.""",
        [("ví dụ", "Ngày 3 có 3 học sinh > 1 → đáp án 3."),
         ("chính xác k không phải chật", "> k, không phải ≥ k."),
         ("không giao nhau", "k = 0: ngày đầu tiên có người là chật.")],
    ),
}
write_practice(
    M,
    "hsgi-p1-analysis",
    "Analysis Problem Set",
    "Five problems drilled on budgets, static RMQ, sweep events, meet-in-the-middle, and honest statement reading.",
    "Bài tập phân tích thuật toán",
    "Năm bài luyện ngân sách phép toán, RMQ tĩnh, quét sự kiện, chia để trị tìm kiếm, và đọc đề cẩn thận.",
    "hsgi-m1-mitm",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsgi-p1-budget",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> P(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        P[i] = P[i-1] + x;
    }
    while (q--) {
        int l, r; in >> l >> r;
        out << P[r] - P[l-1] << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> P(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        P[i] = P[i-1] + x;
    }
    while (q--) {
        int l, r; in >> l >> r;
        // near-miss: P[r] - P[l] excludes a[l]
        out << P[r] - P[l] << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p1-rmq",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    int K = 1;
    while ((1 << K) <= n) ++K;
    vector<vector<int>> st(K, vector<int>(n + 2));
    for (int i = 1; i <= n; ++i) st[0][i] = a[i];
    for (int k = 1; k < K; ++k)
        for (int i = 1; i + (1 << k) - 1 <= n; ++i)
            st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))]);
    while (q--) {
        int l, r; in >> l >> r;
        int k = 31 - __builtin_clz(r - l + 1);
        out << min(st[k][l], st[k][r - (1 << k) + 1]) << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    int K = 1;
    while ((1 << K) <= n) ++K;
    vector<vector<int>> st(K, vector<int>(n + 2));
    for (int i = 1; i <= n; ++i) st[0][i] = a[i];
    for (int k = 1; k < K; ++k)
        for (int i = 1; i + (1 << k) - 1 <= n; ++i)
            st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))]);
    while (q--) {
        int l, r; in >> l >> r;
        // near-miss: r - (1 << k) instead of r - (1 << k) + 1
        // covers a shorter window — wrong whenever the true min sits
        // in the last 2^k elements
        int k = 31 - __builtin_clz(r - l + 1);
        out << min(st[k][l], st[k][r - (1 << k)]) << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p1-overlap",
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        ev.push_back({r + 1, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0, best = 0;
    for (auto& [x, d] : ev) {
        cur += d;
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<pair<long long,int>> ev;
    ev.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        // near-miss: -1 at r instead of r+1 — intervals that merely
        // touch at a point (r1 = l2) are under-counted on the overlap
        ev.push_back({r, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0, best = 0;
    for (auto& [x, d] : ev) {
        cur += d;
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p1-subset-sum",
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    int h = n / 2;
    vector<long long> L{0}, R{0};
    for (int i = 0; i < h; ++i) {
        size_t sz = L.size();
        for (size_t m = 0; m < sz; ++m) L.push_back(L[m] + a[i]);
    }
    for (int i = h; i < n; ++i) {
        size_t sz = R.size();
        for (size_t m = 0; m < sz; ++m) R.push_back(R[m] + a[i]);
    }
    sort(R.begin(), R.end());
    long long best = -1;
    for (long long x : L) {
        long long need = S - x;
        auto it = lower_bound(R.begin(), R.end(), need);
        if (it != R.end()) {
            long long d = llabs(x + *it - S);
            if (best < 0 || d < best) best = d;
        }
        if (it != R.begin()) {
            --it;
            long long d = llabs(x + *it - S);
            if (best < 0 || d < best) best = d;
            ++it;
        }
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    int h = n / 2;
    vector<long long> L{0}, R{0};
    for (int i = 0; i < h; ++i) {
        size_t sz = L.size();
        for (size_t m = 0; m < sz; ++m) L.push_back(L[m] + a[i]);
    }
    for (int i = h; i < n; ++i) {
        size_t sz = R.size();
        for (size_t m = 0; m < sz; ++m) R.push_back(R[m] + a[i]);
    }
    sort(R.begin(), R.end());
    long long best = -1;
    for (long long x : L) {
        long long need = S - x;
        // near-miss: checks only the ceiling candidate (the first sum
        // >= S - x) and never the floor — wrong whenever the closest
        // subset sum lies just BELOW the target
        auto it = lower_bound(R.begin(), R.end(), need);
        if (it == R.end()) continue;
        long long d = llabs(x + *it - S);
        if (best < 0 || d < best) best = d;
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p1-vacation",
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<pair<long long,int>> ev;
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        ev.push_back({r + 1, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0;
    long long ans = -1;
    for (auto& [x, d] : ev) {
        cur += d;
        if (cur > k) { ans = x; break; }
    }
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<pair<long long,int>> ev;
    for (int i = 0; i < n; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        ev.push_back({r + 1, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0;
    long long ans = -1;
    for (auto& [x, d] : ev) {
        cur += d;
        // near-miss: >= k instead of > k — reports the day that reaches
        // exactly k occupants, one step too eager
        if (cur >= k) { ans = x; break; }
    }
    out << ans << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH1 = challenge(
    "hsgi-cp-m1-mix",
    "Checkpoint — Ca học thêm",
    """**Bài toán.** Trung tâm có m lớp học, mỗi lớp mượn phòng từ ngày l_i đến
r_i (đóng hai đầu). Phòng học được "quá tải" trong một ngày nếu **hơn k** lớp
cùng dùng. Hãy in **số ngày quá tải** (không phải ngày đầu tiên — tổng số
ngày!).

**Ràng buộc:** 1 ≤ m, k ≤ 200 000; 1 ≤ l_i ≤ r_i ≤ 10^9.

**Vào:** dòng đầu m k; m dòng: l r.
**Ra:** một số — tổng số ngày có hơn k lớp.

**Điểm:** 100. Kết hợp cả ba kỹ thuật của module: ngân sách (m lớn cấm O(m·t)),
quét sự kiện (±1), và quy ước đóng/mở đúng (r+1).""",
    [
        contest_test(
            "ví dụ",
            T("3 1", "1 3", "2 4", "6 7"),
            T("2"),
            "Ngày 2..3 có 2 lớp (> 1): đúng 2 ngày quá tải. Ngày 6..7 chỉ có 1 lớp: không.",
        ),
        contest_test(
            "một ngày chật duy nhất",
            T("2 0", "5 5", "5 5"),
            T("1"),
            "Hai lớp cùng ngày 5: duy nhất ngày 5 quá tải (k = 0).",
        ),
        contest_test(
            "không quá tải",
            T("1 1", "1 1000000000"),
            T("0"),
            "Một lớp, k = 1: không bao giờ > 1. Đáp án 0 — và tọa độ 10^9 vẫn an toàn nhờ quét sự kiện.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)
VI_CP1 = vi_challenge(
    "Checkpoint — Ca học thêm",
    """**Bài toán.** Trung tâm có m lớp học, mỗi lớp mượn phòng từ ngày l_i đến
r_i (đóng hai đầu). Phòng "quá tải" trong một ngày nếu **hơn k** lớp cùng dùng.
In **tổng số ngày quá tải**.

**Ràng buộc:** 1 ≤ m, k ≤ 200 000; 1 ≤ l_i ≤ r_i ≤ 10^9.

**Vào:** dòng đầu m k; m dòng: l r.
**Ra:** một số — tổng số ngày có hơn k lớp.""",
    [("ví dụ", "Quét ±1, đếm số điểm có cur > k."),
     ("một ngày chật duy nhất", "Hai lớp ngày 5, k = 0 → 1 ngày."),
     ("không quá tải", "Không vượt k → 0.")],
)
write_checkpoint(
    M,
    "hsgi-cp-m1",
    "Checkpoint — Algorithm Analysis",
    "Pass the graded problem to finish the analysis module.",
    20,
    """**Checkpoint — phân tích thuật toán.** Pass the graded challenge below to
complete the module. It combines the whole module: budget (m up to 2·10^5 with
coordinates to 10^9 forbids both O(m·t) and marking arrays), sweep events
(+1/−1), and the closed-interval convention (r+1). Re-read "hơn k" — strictly
more than k — and count DAYS, not classes.

**Điểm kiểm tra — phân tích thuật toán.** Pass bài chấm bên dưới để hoàn thành
module. Bài gộp toàn bộ nội dung: ngân sách (m tới 2·10^5 với tọa độ tới 10^9
cấm cả O(m·t) lẫn mảng đánh dấu), quét sự kiện (+1/−1), và quy ước đoạn đóng
(r+1). Đọc lại "hơn k" — nghiêm ngặt hơn k — và đếm NGÀY, không phải lớp.""",
    "Checkpoint — Phân tích thuật toán",
    "Pass bài chấm để hoàn thành module phân tích thuật toán.",
    """**Điểm kiểm tra — phân tích thuật toán.** Pass bài chấm bên dưới để hoàn thành
module. Bài gộp toàn bộ nội dung: ngân sách (m tới 2·10^5 với tọa độ tới 10^9
cấm cả O(m·t) lẫn mảng đánh dấu), quét sự kiện (+1/−1), và quy ước đoạn đóng
(r+1). Đọc lại "hơn k" — nghiêm ngặt hơn k — và đếm NGÀY, không phải lớp.""",
    CH1,
    VI_CP1,
    solution=CPP_STD + cpp("""    int m, k; in >> m >> k;
    vector<pair<long long,int>> ev;
    for (int i = 0; i < m; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        ev.push_back({r + 1, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0;
    long long days = 0;
    long long prev = LLONG_MIN;
    for (auto& [x, d] : ev) {
        if (cur > k && prev != LLONG_MIN) days += x - prev;
        prev = x;
        cur += d;
    }
    out << days << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int m, k; in >> m >> k;
    vector<pair<long long,int>> ev;
    for (int i = 0; i < m; ++i) {
        long long l, r; in >> l >> r;
        ev.push_back({l, +1});
        ev.push_back({r + 1, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0;
    long long days = 0;
    // near-miss: counts EVENT POINTS with cur > k, not the number of DAYS
    // in the overloaded span — collapses runs of overloaded days to 1
    for (auto& [x, d] : ev) {
        cur += d;
        if (cur > k) ++days;
    }
    out << days << "{{NL}}";
""") + END,
)
