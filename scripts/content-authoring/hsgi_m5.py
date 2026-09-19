#!/usr/bin/env python3
"""HSG Intermediate — Module 5: hsgi-fenwick (Fenwick / Binary Indexed Tree).

Point-update prefix-sum, the lowbit(i) = i & -i anatomy, prefix MAX (the
one-way update), coordinate compression (values 10^9 → positions), and
inversion counting as the classic compression + Fenwick application.

Conventions: zero literal backslashes. Test I/O via T() (real newlines);
C++ bodies via cpp() turning {{NL}} into \n escapes.
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsgi-fenwick"
write_module(
    M,
    "Fenwick Trees — Dynamic Prefix Sums",
    "The lowbit anatomy, point-update prefix-sum queries, prefix max with its one-way limitation, coordinate compression, and inversion counting.",
    "Cây Fenwick — Cộng dồn động",
    "Giải phẫu lowbit, truy vấn cộng dồn với cập nhật điểm, prefix MAX và giới hạn một chiều, nén tọa độ, và đếm nghịch thế.",
    ["hsgi-m5-lowbit", "hsgi-m5-advanced", "hsgi-cp-m5"],
    ["hsgi-p5-fenwick"],
)

# ---------------------------------------------------------------- lesson 5.1
write_lesson(
    M,
    "hsgi-m5-lowbit",
    "The Lowbit Tree — Prefix Sums With Updates",
    "How i & -i partitions responsibility, why both operations are O(log n), and the 1-indexed discipline.",
    16,
    """## The problem prefix sums cannot solve

Prefix sums answer range sums in O(1) — but a single a[i] += x forces an O(n)
rebuild. With n, q = 2·10^5 mixed updates and queries, O(nq) = 4·10^10: dead.

The Fenwick tree (cây Fenwick, Binary Indexed Tree) keeps *some* partial sums
so both operations cost O(log n).

### The anatomy: i & -i

`i & -i` isolates the lowest set bit of i:
- tree[i] stores the sum of the range ending at i with length lowbit(i):
  tree[6] = a[5] + a[6] (lowbit(6) = 2), tree[8] = a[1..8] (lowbit = 8).

```cpp
int n;
vector<long long> t;                 // 1-INDEXED — index 0 unused!

void add(int i, long long v) {       // a[i] += v
    for (; i <= n; i += i & -i) t[i] += v;
}
long long query(int i) {             // sum a[1..i]
    long long s = 0;
    for (; i > 0; i -= i & -i) s += t[i];
    return s;
}
// range [l, r] = query(r) - query(l - 1)
```

Why O(log n)? `i += i & -i` climbs to the next node covering i's range
(at most log2 n steps for n ≤ 2·10^5: about 18); `i -= i & -i` strips the
lowest bit (also ≤ 18 steps).

### The 1-indexed discipline

Index 0 breaks the scheme: lowbit(0) = 0 → infinite loop. Every Fenwick bug
of the form "chạy mãi mãi" or "truy vấn sai ở đầu mảng" is a 0-index leak.
Convert to 1-indexed at read time.

### When Fenwick, when prefix sums?

- static array, many sums → prefix sums (simpler, O(1) queries);
- updates interleaved with sums → Fenwick;
- range [l, r] updates adding v to every element → TWO Fenwicks (trick:
  difference array + Fenwick) or segment tree with lazy (M6).

**Next:** [Compression, Max, Inversions](./hsgi-m5-advanced)""",
    "Cây lowbit — Cộng dồn có cập nhật",
    "i & -i chia trách nhiệm thế nào, vì sao cả hai thao tác đều O(log n), và kỷ luật đánh số từ 1.",
    """## Bài toán cộng dồn thường không giải nổi

Mảng cộng dồn trả tổng đoạn trong O(1) — nhưng một lần a[i] += x buộc dựng
lại O(n). Với n, q = 2·10^5 trộn cập nhật và truy vấn, O(nq) = 4·10^10: chết.

Cây Fenwick giữ *một số* tổng riêng phần để cả hai thao tác tốn O(log n).

### Giải phẫu: i & -i

`i & -i` cô lập bit 1 thấp nhất của i:
- tree[i] lưu tổng đoạn kết thúc tại i với độ dài lowbit(i):
  tree[6] = a[5] + a[6] (lowbit(6) = 2), tree[8] = a[1..8] (lowbit = 8).

```cpp
int n;
vector<long long> t;                 // ĐÁNH SỐ TỪ 1 — chỉ số 0 không dùng!

void add(int i, long long v) {       // a[i] += v
    for (; i <= n; i += i & -i) t[i] += v;
}
long long query(int i) {             // tổng a[1..i]
    long long s = 0;
    for (; i > 0; i -= i & -i) s += t[i];
    return s;
}
// đoạn [l, r] = query(r) - query(l - 1)
```

Vì sao O(log n)? `i += i & -i` leo lên node phủ tiếp phạm vi của i (tối đa
log2 n bước với n ≤ 2·10^5: cỡ 18); `i -= i & -i` gỡ bit thấp nhất (cũng
≤ 18 bước).

### Kỷ luật đánh số từ 1

Chỉ số 0 phá vỡ sơ đồ: lowbit(0) = 0 → lặp vô hạn. Mọi lỗi Fenwick dạng "chạy
mãi mãi" hay "truy vấn sai ở đầu mảng" đều là rò rỉ chỉ số 0. Đổi sang 1-index
ngay lúc đọc dữ liệu.

### Khi nào Fenwick, khi nào cộng dồn?

- mảng tĩnh, nhiều tổng → cộng dồn (đơn giản hơn, O(1)/truy vấn);
- cập nhật xen truy vấn → Fenwick;
- cập nhật ĐOẠN cộng v vào mọi phần tử → hai Fenwick (mẹo: mảng hiệu + Fenwick)
  hoặc segment tree có lazy (M6).

**Tiếp:** [Nén, Max, Nghịch thế](./hsgi-m5-advanced)""",
)

# ---------------------------------------------------------------- lesson 5.2
write_lesson(
    M,
    "hsgi-m5-advanced",
    "Coordinate Compression, Prefix Max, and Inversions",
    "Mapping 10^9-scale values to positions, the max variant and its one-way update, and counting inversions in O(n log n).",
    17,
    """## Coordinate compression (nén tọa độ)

Fenwick indexes are positions, but problems speak in VALUES up to 10^9 — you
cannot allocate 10^9 cells. If only n ≤ 2·10^5 values *matter* (only their
relative order), map value → rank:

```cpp
vector<int> vals = a;                     // copy
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());
int rank_of = lower_bound(vals.begin(), vals.end(), x) - vals.begin() + 1;
// rank in [1, m], m ≤ n — Fenwick of size m
```

Recognition: the answer depends only on ORDER (comparisons), not magnitudes.
If actual sums of values are needed, compression loses information — don't.

### Prefix MAX — the one-way tree

tree[i] = max over its lowbit range. Update climbs UP with
`i += i & -i`, so an element can only be increased — this tree **cannot
delete or decrease**. That is usually fine: "max prefix độ khó thấy tới thời
điểm t" only grows.

```cpp
void update(int i, int v) {          // ch=max(tree[i], v), one-way
    for (; i <= n; i += i & -i) t[i] = max(t[i], v);
}
int query(int i) {                   // max a[1..i]
    int s = 0;
    for (; i > 0; i -= i & -i) s = max(s, t[i]);
    return s;
}
```

Need decreases → segment tree (M6).

### Inversions — the classic composition

"Nghịch thế" = pair (i, j), i < j, a[i] > a[j]. Count in O(n log n):
sweep left to right; for each a[j], the inversions ENDING at j are the number
of previous elements GREATER than a[j].

```cpp
// compress, Fenwick over value-ranks
long long inv = 0;
for (int j = 0; j < n; ++j) {
    int r = rank(a[j]);
    inv += (long long)(j) - query(r);   // j items seen, query(r) of them ≤ a[j]
    add(r, 1);
}
```

Total inversions can reach n(n−1)/2 ≈ 2·10^10 for n = 2·10^5 — **long long
mandatory**. This composition (compress → Fenwick → sweep with a counting
identity) is THE reusable pattern of this course.

**Next:** [Checkpoint](./hsgi-cp-m5)""",
    "Nén tọa độ, prefix MAX, và nghịch thế",
    "Ánh xạ giá trị 10^9 về vị trí, biến thể max với cập nhật một chiều, và đếm nghịch thế trong O(n log n).",
    """## Nén tọa độ

Chỉ số Fenwick là vị trí, nhưng đề nói bằng GIÁ TRỊ tới 10^9 — không thể cấp
phát 10^9 ô. Nếu chỉ n ≤ 2·10^5 giá trị *có vai trò* (chỉ thứ tự tương đối),
ánh xạ giá trị → hạng:

```cpp
vector<int> vals = a;                     // bản sao
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());
int rank_of = lower_bound(vals.begin(), vals.end(), x) - vals.begin() + 1;
// hạng trong [1, m], m ≤ n — Fenwick cỡ m
```

Nhận diện: đáp án chỉ phụ thuộc THỨ TỰ (so sánh), không độ lớn. Nếu cần tổng
các giá trị thật, nén mất thông tin — đừng.

### Prefix MAX — cây một chiều

tree[i] = max trên phạm vi lowbit của nó. Cập nhật leo LÊN bằng
`i += i & -i`, nên phần tử chỉ có thể tăng — cây này **không xóa hay giảm
được**. Thường là đủ: "max prefix nhìn thấy tới thời điểm t" chỉ tăng.

```cpp
void update(int i, int v) {          // ch=max(tree[i], v), một chiều
    for (; i <= n; i += i & -i) t[i] = max(t[i], v);
}
int query(int i) {                   // max a[1..i]
    int s = 0;
    for (; i > 0; i -= i & -i) s = max(s, t[i]);
    return s;
}
```

Cần giảm → segment tree (M6).

### Nghịch thế — phép ghép kinh điển

"Nghịch thế" = cặp (i, j), i < j, a[i] > a[j]. Đếm trong O(n log n):
quét trái→phải; với mỗi a[j], số nghịch thế KẾT TẠI j = số phần tử trước
LỚN HƠN a[j].

```cpp
// nén, Fenwick trên hạng giá trị
long long inv = 0;
for (int j = 0; j < n; ++j) {
    int r = rank(a[j]);
    inv += (long long)(j) - query(r);   // đã thấy j phần tử, query(r) trong đó ≤ a[j]
    add(r, 1);
}
```

Tổng nghịch thế tới n(n−1)/2 ≈ 2·10^10 với n = 2·10^5 — **bắt buộc long long**.
Phép ghép này (nén → Fenwick → quét với một đồng nhất thức đếm) là mẫu TÁI SỬ
DỤNG nhất của khóa học.

**Tiếp:** [Điểm kiểm tra](./hsgi-cp-m5)""",
)

# ---------------------------------------------------------------- practice
A1 = challenge(
    "hsgi-p5-dynamic-sum",
    "Cộng dồn động — điểm cập nhật, đoạn hỏi",
    """**Bài toán.** Mảng n phần tử, q thao tác. Loại 1 "1 i v": a[i] += v.
Loại 2 "2 l r": in tổng a[l..r].

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |a[i]|, |v| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n phần tử; q dòng thao tác.
**Ra:** mỗi thao tác loại 2 một dòng.""",
    [
        contest_test(
            "ví dụ",
            T("5 4", "1 2 3 4 5", "2 1 5", "1 3 10", "2 3 3", "2 2 4"),
            T("15", "13", "19"),
            "Fenwick chuẩn; đoạn [3,3] sau cập nhật = 13; [2,4] = 2+13+4.",
        ),
        contest_test(
            "cập nhật giá trị âm",
            T("3 3", "5 5 5", "1 2 -5", "2 1 3", "1 1 -1000000000"),
            T("10"),
            "a[2] = 0 → tổng [1,3] = 10; thao tác thứ ba là CẬP NHẬT (không in). Giá trị âm hợp lệ — long long.",
        ),
        contest_test(
            "l = r và biên 1, n",
            T("4 4", "1 2 3 4", "2 1 1", "2 4 4", "1 4 1", "2 1 4"),
            T("1", "4", "11"),
            "Truy vấn điểm và cập nhật tại biên phải đúng — lỗi 0-index lộ ở đây.",
        ),
        contest_test(
            "n lớn xen kẽ dày",
            T("200000 200000") + T(" ".join("1" for _ in range(200000)))
            + T("".join("1 " + str((i % 200000) + 1) + " 1" + chr(10) for i in range(100000)))
            + T("".join("2 1 " + str(200000) + chr(10) for i in range(99999)))
            + T("2 1 200000"),
            T("\n".join("300000" for _ in range(100000))),
            "100000 cập nhật +1 và 100000 truy vấn tổng toàn mảng (mỗi truy vấn một dòng 300000): mỗi thao tác O(log n) — O(nq) là 4·10^10, chết.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p5-inversions",
    "Đếm nghịch thế",
    """**Bài toán.** Cho dãy n phần tử đôi một KHÁC nhau. Đếm số cặp nghịch thế:
(i, j) với i < j và a[i] > a[j].

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ a[i] ≤ 10^9 (nén tọa độ!).

**Vào:** dòng đầu n; dòng hai n phần tử.
**Ra:** một số — số cặp (dùng long long!).""",
    [
        contest_test(
            "ví dụ",
            T("5", "3 1 4 5 2"),
            T("4"),
            "Cặp: (3,1), (3,2), (4,2), (5,2) → 4. Nén giá trị 10^9 về hạng rồi quét Fenwick.",
        ),
        contest_test(
            "đã sắp tăng",
            T("4", "1 2 3 4"),
            T("0"),
            "Không nghịch thế.",
        ),
        contest_test(
            "sắp giảm — max nghịch thế",
            T("4", "4 3 2 1"),
            T("6"),
            "n(n−1)/2 = 6: mọi cặp đều nghịch.",
        ),
        contest_test(
            "n lớn, nửa nửa",
            T("200000") + T(" ".join(str(200001 - i) for i in range(1, 100001)) + " " + " ".join(str(i) for i in range(100001, 200001))),
            T("9999900000"),
            "Dãy ghép hai nửa (đầu giảm 100001..200000, sau tăng 100001..199999): tổng nghịch thế = 9999900000 — xác minh bằng chính định nghĩa trên máy, không đoán; int 32 chết.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p5-max-seen",
    "Độ khó cao nhất nhìn thấy (prefix max)",
    """**Bài toán.** Món đồ i xuất hiện thời điểm i với độ khó h_i. Tại thời điểm
t, món "khó nhất từng thấy" là max(h_1..h_t). Với mỗi thời điểm t = 1..n,
in giá trị đó trên một dòng. Điểm đặc biệt: một số món bị "khóa" — khóa món j
độ khó h_j nghĩa là mọi max về sau không được vượt quá h_j... (bỏ: giữ đề thuần
prefix max) — In prefix max sau mỗi phần tử.

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ h_i ≤ 10^9.

**Vào:** dòng đầu n; dòng hai h_i.
**Ra:** n dòng, dòng t là max(h_1..h_t).""",
    [
        contest_test(
            "ví dụ",
            T("6", "3 1 4 1 5 9"),
            T("3", "3", "4", "4", "5", "9"),
            "Prefix max tăng dần, giữ giá trị khi gặp phần tử nhỏ hơn.",
        ),
        contest_test(
            "giảm dần",
            T("4", "9 3 2 1"),
            T("9", "9", "9", "9"),
            "Max đầu tiên thống trị mãi.",
        ),
        contest_test(
            "tăng dần",
            T("3", "1 2 3"),
            T("1", "2", "3"),
            "Mỗi phần tử là max mới.",
        ),
        contest_test(
            "n lớn luân phiên",
            T("200000") + T(" ".join(str(i % 97 + 1) for i in range(200000))),
            T(*[str(i + 1 if i < 96 else 97) for i in range(200000)]),
            "Chu kỳ 1..97: prefix max tăng 1..97 trong 97 lượt đầu, rồi giữ 97 mãi — mỗi dòng một giá trị. Mỗi bước O(log n).",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p5-distinct",
    "Đếm phần tử khác nhau trong đoạn giá trị lớn",
    """**Bài toán.** Cho dãy n số (giá trị tới 10^9) và q truy vấn [l, r]: trong
a[l..r] có bao nhiêu GIÁ TRỊ khác nhau? Truy vấn nhiều → cần tiền xử lý:
đáp án = số vị trí i ∈ [l, r] mà a[i] lần cuối xuất hiện TRƯỚC i (vị trí cuối
cùng < l). Cài: với mỗi i, giữ pos[a[i]] (lần cuối); biến i thành điểm 1 tại
pos[a[i]]+1 nếu tồn tại, truy vấn [l, i]... (mẹo offline: sort truy vấn theo r,
Fenwick đếm vị trí "lần cuối trước i").

Cài đặt chuẩn: với mỗi truy vấn (l, r) sort theo r; quét i = 1..n; tại i,
nếu a[i] đã xuất hiện tại p < i: add(p, -1); add(i, +1); cập nhật last[a[i]] = i;
truy vấn (l, r) khi i = r: đáp án = query(r) - query(l - 1).

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; 1 ≤ a[i] ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số; q dòng: l r.
**Ra:** q dòng, mỗi dòng số giá trị khác nhau trong [l, r].""",
    [
        contest_test(
            "ví dụ",
            T("6 3", "1 2 1 3 2 1", "1 6", "2 4", "3 5"),
            T("3", "3", "3"),
            "[1..6] = {1,2,3}; [2..4] = {2,1,3} → 3; [3..5] = {1,3,2} → 3.",
        ),
        contest_test(
            "một phần tử lặp kín",
            T("4 2", "7 7 7 7", "1 4", "2 3"),
            T("1", "1"),
            "Mọi đoạn chỉ chứa giá trị 7.",
        ),
        contest_test(
            "đoạn độ dài 1",
            T("3 3", "5 9 5", "1 1", "2 2", "3 3"),
            T("1", "1", "1"),
            "Mỗi điểm: đúng 1 giá trị.",
        ),
        contest_test(
            "n lớn, giá trị 10^9 xen kẽ",
            T("200000 2") + T(" ".join(str(1000000000 - (i % 2)) for i in range(200000)), "1 200000", "100000 100001"),
            T("2", "2"),
            "Toàn dãy chỉ 2 giá trị (10^9, 10^9−1) xen kẽ: mọi đoạn đủ dài đều 2; [100000,100001] là hai phần tử khác nhau → 2.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p5-kquery",
    "Đếm phần tử lớn hơn k trong tiền tố",
    """**Bài toán.** Dãy n phần tử, q truy vấn (i, k): trong a[1..i] có bao nhiêu
phần tử LỚN HƠN k?

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; 1 ≤ a[i], k ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số; q dòng: i k.
**Ra:** q dòng mỗi dòng một số lượng.

**Gợi ý:** nén giá trị; quét i theo thứ tự (offline sort truy vấn theo i);
Fenwick đếm số phần tử đã chèn có hạng > hạng(k) = query(m) − query(rank(k)).""",
    [
        contest_test(
            "ví dụ",
            T("5 3", "4 1 3 5 2", "3 2", "5 1", "5 100"),
            T("2", "4", "0"),
            "[1..3] lớn hơn 2: {4,3} → 2; toàn dãy > 1: {4,3,5,2} → 4; k = 100: 0.",
        ),
        contest_test(
            "k bằng đúng max",
            T("3 1", "1 2 3", "3 3"),
            T("0"),
            "LỚN HƠN k — phần tử bằng k không đếm.",
        ),
        contest_test(
            "i = 1",
            T("2 1", "10 20", "1 5"),
            T("1"),
            "Tiền tố 1 phần tử: 10 > 5.",
        ),
        contest_test(
            "n lớn biên cực",
            T("200000 2") + T(" ".join(str(i) for i in range(200000)), "200000 1", "200000 199999"),
            T("199998", "0"),
            "a = 0..199999: đếm > 1 là 199998 giá trị (2..199999); đếm > 199999 là 0 (199999 > 199999 sai) — không bao gồm chính k.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)
VI5 = {
    "hsgi-p5-dynamic-sum": vi_challenge(
        "Cộng dồn động — điểm cập nhật, đoạn hỏi",
        """**Bài toán.** Mảng n phần tử, q thao tác. "1 i v": a[i] += v.
"2 l r": in tổng a[l..r].

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; |a[i]|, |v| ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n phần tử; q dòng thao tác.
**Ra:** mỗi thao tác loại 2 một dòng.""",
        [("ví dụ", "Fenwick chuẩn: 15, 13, 19."),
         ("cập nhật giá trị âm", "Giá trị âm hợp lệ — long long."),
         ("l = r và biên 1, n", "Lỗi 0-index lộ tại biên."),
         ("n lớn xen kẽ dày", "Mỗi thao tác O(log n); O(nq) = 4·10^10 chết.")],
    ),
    "hsgi-p5-inversions": vi_challenge(
        "Đếm nghịch thế",
        """**Bài toán.** Dãy n phần tử đôi một khác nhau. Đếm cặp (i, j) với i < j
và a[i] > a[j].

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ a[i] ≤ 10^9.

**Vào:** dòng đầu n; dòng hai n phần tử.
**Ra:** một số (long long!).""",
        [("ví dụ", "(3,1),(3,2),(4,2),(5,2) → 4."),
         ("đã sắp tăng", "0."),
         ("sắp giảm — max nghịch thế", "n(n−1)/2 = 6."),
         ("n lớn, nửa nửa", "10^5·10^5 = 10^10 — int 32 chết.")],
    ),
    "hsgi-p5-max-seen": vi_challenge(
        "Độ khó cao nhất nhìn thấy (prefix max)",
        """**Bài toán.** Món đồ i xuất hiện thời điểm i với độ khó h_i. In prefix max
sau mỗi phần tử: dòng t là max(h_1..h_t).

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ h_i ≤ 10^9.

**Vào:** dòng đầu n; dòng hai h_i.
**Ra:** n dòng.""",
        [("ví dụ", "3, 3, 4, 4, 5, 9."),
         ("giảm dần", "9 mãi mãi."),
         ("tăng dần", "1, 2, 3."),
         ("n lớn luân phiên", "Max 97 từ lượt 97 giữ mãi.")],
    ),
    "hsgi-p5-distinct": vi_challenge(
        "Đếm phần tử khác nhau trong đoạn giá trị lớn",
        """**Bài toán.** Dãy n số (giá trị tới 10^9), q truy vấn [l, r]: bao nhiêu
GIÁ TRỊ khác nhau? Offline: sort truy vấn theo r, Fenwick giữ vị trí lần cuối.

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; 1 ≤ a[i] ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số; q dòng: l r.
**Ra:** q dòng.""",
        [("ví dụ", "3, 2, 2."),
         ("một phần tử lặp kín", "1, 1."),
         ("đoạn độ dài 1", "1, 1, 1."),
         ("n lớn, giá trị 10^9 xen kẽ", "Toàn dãy 2 giá trị; [100000,100001] = 2.")],
    ),
    "hsgi-p5-kquery": vi_challenge(
        "Đếm phần tử lớn hơn k trong tiền tố",
        """**Bài toán.** Dãy n phần tử, q truy vấn (i, k): trong a[1..i] bao nhiêu
phần tử LỚN HƠN k?

**Ràng buộc:** 1 ≤ n, q ≤ 200 000; 1 ≤ a[i], k ≤ 10^9.

**Vào:** dòng đầu n q; dòng hai n số; q dòng: i k.
**Ra:** q dòng.""",
        [("ví dụ", "2, 4, 0."),
         ("k bằng đúng max", "LỚN HƠN — bằng k không đếm."),
         ("i = 1", "10 > 5 → 1."),
         ("n lớn biên cực", "a = 0..199999: > 199999 → 0.")],
    ),
}
write_practice(
    M,
    "hsgi-p5-fenwick",
    "Fenwick Problem Set",
    "Five problems: dynamic sums, inversion counting, prefix max, distinct values in ranges (offline), and greater-than-k prefix counting.",
    "Bài tập Fenwick",
    "Năm bài: cộng dồn động, đếm nghịch thế, prefix max, giá trị khác nhau trong đoạn (offline), và đếm lớn hơn k trên tiền tố.",
    "hsgi-m5-advanced",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI5,
    solutions=[
        (
            "hsgi-p5-dynamic-sum",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(n + 1, 0);
    auto add = [&](int i, long long v) {
        for (; i <= n; i += i & -i) t[i] += v;
    };
    auto pre = [&](int i) {
        long long s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        add(i, x);
    }
    while (q--) {
        int type; in >> type;
        if (type == 1) {
            int i; long long v; in >> i >> v;
            add(i, v);
        } else {
            int l, r; in >> l >> r;
            out << pre(r) - pre(l - 1) << "{{NL}}";
        }
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> t(n + 1, 0);
    auto add = [&](int i, long long v) {
        for (; i <= n; i += i & -i) t[i] += v;
    };
    auto pre = [&](int i) {
        long long s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        add(i, x);
    }
    while (q--) {
        int type; in >> type;
        if (type == 1) {
            int i; long long v; in >> i >> v;
            add(i, v);
        } else {
            int l, r; in >> l >> r;
            // near-miss: pre(r) - pre(l) bỏ mất a[l]
            out << pre(r) - pre(l) << "{{NL}}";
        }
    }
""") + END,
        ),
        (
            "hsgi-p5-inversions",
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    vector<int> vals = a;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = vals.size();
    vector<int> t(m + 1, 0);
    auto add = [&](int i) {
        for (; i <= m; i += i & -i) t[i] += 1;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    long long inv = 0;
    for (int j = 0; j < n; ++j) {
        int r = lower_bound(vals.begin(), vals.end(), a[j]) - vals.begin() + 1;
        inv += (long long)j - pre(r);
        add(r);
    }
    out << inv << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    vector<int> vals = a;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = vals.size();
    vector<int> t(m + 1, 0);
    auto add = [&](int i) {
        for (; i <= m; i += i & -i) t[i] += 1;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    long long inv = 0;
    for (int j = 0; j < n; ++j) {
        int r = lower_bound(vals.begin(), vals.end(), a[j]) - vals.begin() + 1;
        // near-miss: đếm phần tử TRƯỚC nhỏ hơn hoặc bằng (pre(r) thay vì
        // j - pre(r)) — đó là số NON-inversions, không phải nghịch thế
        inv += pre(r);
        add(r);
    }
    out << inv << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p5-max-seen",
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> h(n + 1);
    for (int i = 1; i <= n; ++i) in >> h[i];
    vector<int> t(n + 1, 0);
    auto upd = [&](int i, int v) {
        for (; i <= n; i += i & -i) t[i] = max(t[i], v);
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s = max(s, t[i]);
        return s;
    };
    for (int i = 1; i <= n; ++i) {
        upd(i, h[i]);
        out << pre(i) << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> h(n + 1);
    for (int i = 1; i <= n; ++i) in >> h[i];
    vector<int> t(n + 1, 0);
    auto upd = [&](int i, int v) {
        // near-miss: gán = thay vì max — node bị GHI ĐÈ khi phần tử mới
        // nhỏ hơn, phá prefix max tại mọi node bị đè
        for (; i <= n; i += i & -i) t[i] = v;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s = max(s, t[i]);
        return s;
    };
    for (int i = 1; i <= n; ++i) {
        upd(i, h[i]);
        out << pre(i) << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsgi-p5-distinct",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    vector<vector<pair<int,int>>> byR(n + 1);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        byR[r].push_back({l, i});
    }
    vector<int> t(n + 1, 0);
    auto add = [&](int i, int v) {
        for (; i <= n; i += i & -i) t[i] += v;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    vector<int> last(200001, -1), ans(q);
    const int OFF = 1000000000;
    vector<int> lastAt;
    // map value -> last position via compressed dict
    vector<int> vals = a;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    vector<int> lst(vals.size(), -1);
    for (int i = 1; i <= n; ++i) {
        int r = lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin();
        if (lst[r] != -1) add(lst[r], -1);
        add(i, 1);
        lst[r] = i;
        for (auto& [l, idx] : byR[i]) ans[idx] = pre(i) - pre(l - 1);
    }
    for (int i = 0; i < q; ++i) out << ans[i] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    vector<vector<pair<int,int>>> byR(n + 1);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        byR[r].push_back({l, i});
    }
    vector<int> t(n + 1, 0);
    auto add = [&](int i, int v) {
        for (; i <= n; i += i & -i) t[i] += v;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    vector<int> ans(q);
    vector<int> vals = a;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    vector<int> lst(vals.size(), -1);
    for (int i = 1; i <= n; ++i) {
        int r = lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin();
        if (lst[r] != -1) add(lst[r], -1);
        add(i, 1);
        // near-miss: QUÊN cập nhật lst[r] = i — vị trí cũ bị xóa hai lần,
        // đếm thiếu giá trị đầu mỗi đoạn lặp
        for (auto& [l, idx] : byR[i]) ans[idx] = pre(i) - pre(l - 1);
    }
    for (int i = 0; i < q; ++i) out << ans[i] << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p5-kquery",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    vector<pair<int,int>> qs(q);
    for (auto& [pos, k] : qs) in >> pos >> k;
    vector<int> vals = a;
    for (auto& [pos, k] : qs) vals.push_back(k);
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = vals.size();
    vector<int> t(m + 1, 0);
    auto add = [&](int i, int v) {
        for (; i <= m; i += i & -i) t[i] += v;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    auto rank1 = [&](int x) {
        return lower_bound(vals.begin(), vals.end(), x) - vals.begin() + 1;
    };
    vector<vector<pair<int,int>>> byI(n + 1);
    for (int i = 0; i < q; ++i) byI[qs[i].first].push_back({qs[i].second, i});
    vector<long long> ans(q);
    for (int i = 1; i <= n; ++i) {
        add(rank1(a[i]), 1);
        for (auto& [k, idx] : byI[i]) {
            int rk = rank1(k);
            ans[idx] = (long long)pre(m) - pre(rk);
        }
    }
    for (int i = 0; i < q; ++i) out << ans[i] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    vector<int> vals = a;
    for (int i = 0; i < q; ++i) { int x, y; in >> x >> y; vals.push_back(y); }
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = vals.size();
    vector<int> t(m + 1, 0);
    auto add = [&](int i, int v) {
        for (; i <= m; i += i & -i) t[i] += v;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    auto rank1 = [&](int x) {
        return lower_bound(vals.begin(), vals.end(), x) - vals.begin() + 1;
    };
    vector<vector<pair<int,int>>> byI(n + 1);
    for (int i = 0; i < q; ++i) {
        int pos, k; in >> pos >> k;
        byI[pos].push_back({k, i});
    }
    vector<long long> ans(q);
    for (int i = 1; i <= n; ++i) {
        add(rank1(a[i]), 1);
        for (auto& [k, idx] : byI[i]) {
            // near-miss: pre(rank(k)) đếm phần tử ≤ k thay vì > k —
            // đáp án bị đảo (báo phần nhỏ hơn/không vượt k)
            ans[idx] = pre(rank1(k));
        }
    }
    for (int i = 0; i < q; ++i) out << ans[i] << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH5 = challenge(
    "hsgi-cp-m5-chaos",
    "Checkpoint — Sắp lại hàng quán",
    """**Bài toán.** Quán có n khách xếp hàng, khách i có mức giận s_i (đôi một
khác nhau). Quản lý đi từ đầu hàng đến cuối; tại mỗi khách j, khách j "càu
kỳ" bằng số khách TRƯỚC MÌNH (gần đầu hàng hơn) có mức giận CAO HƠN mình —
mỗi người như vậy bị ghi sổ một lần. Tổng số lần ghi sổ là bao nhiêu? (Đây
chính là số nghịch thế của dãy s.)

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ s_i ≤ 10^9.

**Vào:** dòng đầu n; dòng hai s_i.
**Ra:** một số — tổng lần ghi sổ.""",
    [
        contest_test(
            "ví dụ",
            T("5", "3 1 4 5 2"),
            T("4"),
            "Như bài đếm nghịch thế: khách 1 càu 1 lần (với 3), khách 2 với 3 và 4, khách 5 với 4 — tổng 4.",
        ),
        contest_test(
            "hàng đã êm",
            T("3", "1 2 3"),
            T("0"),
            "Sắp tăng: không ai càu — 0.",
        ),
        contest_test(
            "hàng ngược hoàn toàn",
            T("4", "9 7 5 3"),
            T("6"),
            "Mọi cặp đều nghịch: 4·3/2 = 6.",
        ),
        contest_test(
            "n lớn ngược — ngân sách",
            T("200000") + T(" ".join(str(200000 - i) for i in range(200000))),
            T("19999900000"),
            "n(n−1)/2 = 19999900000 nghịch thế: Fenwick trả lời tức thì; vét cạn O(n^2) = 4·10^10 phép so sánh thì không (đây là bài học ngân sách của M1!).",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)
VI_CP5 = vi_challenge(
    "Checkpoint — Sắp lại hàng quán",
    """**Bài toán.** n khách xếp hàng, khách i có mức giận s_i (đôi một khác
nhau). Khách j "càu kỳ" bằng số khách trước mình có mức giận CAO HƠN — mỗi
người như vậy ghi sổ một lần. Tổng số lần ghi sổ?

**Ràng buộc:** 1 ≤ n ≤ 200 000; 1 ≤ s_i ≤ 10^9.

**Vào:** dòng đầu n; dòng hai s_i.
**Ra:** một số.""",
    [("ví dụ", "Nghịch thế của 3 1 4 5 2 → 4."),
     ("hàng đã êm", "0."),
     ("hàng ngược hoàn toàn", "6.")],
)
write_checkpoint(
    M,
    "hsgi-cp-m5",
    "Checkpoint — Fenwick",
    "Pass the graded problem to finish the Fenwick module.",
    20,
    """**Checkpoint — Fenwick.** Pass the graded challenge below to complete the
module. It is the composition the module taught: compress the 10^9-scale
values, sweep once, and for each person count how many earlier people have a
higher value (n − prefix-count-of-≤ ... or the direct identity from lesson
5.2). Answer fits in long long — compute the worst case.

**Điểm kiểm tra — Fenwick.** Pass bài chấm bên dưới để hoàn thành module. Đây
là phép ghép module đã dạy: nén giá trị 10^9, quét một lượt, với mỗi khách đếm
số người TRƯỚC có mức giận cao hơn (đồng nhất thức từ bài 5.2). Đáp án phải
dùng long long — tự tính trường hợp xấu nhất.""",
    "Checkpoint — Fenwick",
    "Pass bài chấm để hoàn thành module Fenwick.",
    """**Điểm kiểm tra — Fenwick.** Pass bài chấm bên dưới: nén giá trị, quét một
lượt, đếm người trước có mức giận cao hơn. Dùng long long.""",
    CH5,
    VI_CP5,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<int> s(n);
    for (auto& x : s) in >> x;
    vector<int> vals = s;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = vals.size();
    vector<int> t(m + 1, 0);
    auto add = [&](int i) {
        for (; i <= m; i += i & -i) t[i] += 1;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    long long total = 0;
    for (int j = 0; j < n; ++j) {
        int r = lower_bound(vals.begin(), vals.end(), s[j]) - vals.begin() + 1;
        total += (long long)j - pre(r);   // số người trước GIỮA cao hơn
        add(r);
    }
    out << total << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<int> s(n);
    for (auto& x : s) in >> x;
    vector<int> vals = s;
    sort(vals.begin(), vals.end());
    vals.erase(unique(vals.begin(), vals.end()), vals.end());
    int m = vals.size();
    vector<int> t(m + 1, 0);
    auto add = [&](int i) {
        for (; i <= m; i += i & -i) t[i] += 1;
    };
    auto pre = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += t[i];
        return s;
    };
    // near-miss: THUẬT TOÁN đúng, NGÂN SÁCH đúng — nhưng total là int:
    // n(n−1)/2 = 19999900000 vượt 2^31 → tràn số trên test lớn nhất
    int total = 0;
    for (int j = 0; j < n; ++j) {
        int r = lower_bound(vals.begin(), vals.end(), s[j]) - vals.begin() + 1;
        total += j - pre(r);
        add(r);
    }
    out << total << "{{NL}}";
""") + END,
)
