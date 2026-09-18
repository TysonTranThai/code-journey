#!/usr/bin/env python3
"""HSG — Module 8: hsg-prefix (mảng cộng dồn — prefix sums).

O(1) range sums after an O(n) build; 2D prefix sums for grid regions;
prefix counting; zero-sum subarray counting with a map; fixed-window max.
Byte-exact contest tests; verified R/W pairs.

Conventions (proven in m6/m7): zero literal backslashes in this source.
Test I/O strings use T() (real newlines). C++ bodies use cpp() which turns
the {{NL}} marker into a backslash-n escape inside C++ string literals.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsg-prefix"
write_module(
    M,
    "Prefix Sums",
    "Answer range-sum queries in O(1): 1D and 2D prefix sums, prefix counting, zero-sum subarrays, fixed-window maximum.",
    "Mảng cộng dồn",
    "Trả lời truy vấn tổng đoạn trong O(1): mảng cộng dồn 1D và 2D, đếm bằng cộng dồn, đếm đoạn con tổng 0, cửa sổ cố định.",
    ["hsg-m8-basics", "hsg-m8-2d", "hsg-cp-m8"],
    ["hsg-p8-prefix"],
)

write_lesson(
    M,
    "hsg-m8-basics",
    "Prefix Sums — Range Queries in O(1)",
    "Build the prefix array once, answer every range-sum query with one subtraction.",
    14,
    """## Why naive range sums fail

q queries, each summing up to n elements, is O(nq). With n, q at 10^5 that
is 10^10 operations — far beyond the limit. The fix: pay once, answer free.

### The prefix array (1-based)

```cpp
P[0] = 0;
for (int i = 1; i <= n; ++i) P[i] = P[i-1] + a[i];
// P[i] = a[1] + a[2] + ... + a[i]
```

Then the sum of a[l..r] collapses to a single subtraction:

```cpp
long long sum = P[r] - P[l-1];
```

Worked example: a = [3, -1, 4, 1, -5] gives
P = [0, 3, 2, 6, 7, 2]. sum(2..5) = P[5] - P[1] = 2 - 3 = -1. Check by
hand: -1 + 4 + 1 - 5 = -1.

### The two off-by-one traps

- `P[r] - P[l]` **excludes** a[l] — one of the most common Wrong Answers
  in beginner contests.
- If you build a 0-based running sum `s` and push it after each element,
  the answer is `s_after_r - s_before_l`. Mixing the two conventions in
  one solution is a bug factory. Pick one, write it as a comment.

### Overflow

n up to 10^5 values of |a_i| up to 10^9 make prefix sums reach 10^14 —
beyond int. Use `long long` for P and for the answers. This is not a
style choice; `int` here is a guaranteed WA on big tests.

## When prefix sums apply

Any quantity that can be accumulated left to right and **subtracted**:
sums, counts (how many elements in range are even), occurrences of a
value. Quantities like max/min do **not** subtract — prefix max cannot
answer range max. That needs a different structure (later modules).
""",
    "Mảng cộng dồn — Truy vấn tổng đoạn O(1)",
    "Dựng mảng cộng dồn một lần, trả lời mọi truy vấn tổng đoạn bằng một phép trừ.",
    """## Vì sao cộng dồn từng truy vấn là thất bại

q truy vấn, mỗi truy vấn cộng tối đa n phần tử, là O(nq). Với n, q bằng
10^5 thì là 10^10 phép tính — vượt xa giới hạn. Cách sửa: trả giá một
lần, trả lời miễn phí.

### Mảng cộng dồn (chỉ số từ 1)

```cpp
P[0] = 0;
for (int i = 1; i <= n; ++i) P[i] = P[i-1] + a[i];
// P[i] = a[1] + a[2] + ... + a[i]
```

Khi đó tổng a[l..r] gọn thành một phép trừ:

```cpp
long long sum = P[r] - P[l-1];
```

Ví dụ: a = [3, -1, 4, 1, -5] cho P = [0, 3, 2, 6, 7, 2].
sum(2..5) = P[5] - P[1] = 2 - 3 = -1. Kiểm tra tay: -1 + 4 + 1 - 5 = -1.

### Hai bẫy lệch một

- `P[r] - P[l]` **bỏ sót** a[l] — một trong những WA phổ biến nhất của
  người mới.
- Nếu dùng tổng chạy kiểu 0-based (sau mỗi phần tử), đáp án là
  `s_sau_r - s_trước_l`. Trộn hai quy ước trong một lời giải là nhà máy
  lỗi. Chọn một, ghi rõ thành chú thích.

### Tràn số

n tới 10^5 phần tử |a_i| tới 10^9 đưa cộng dồn tới 10^14 — vượt int.
Dùng `long long` cho P và đáp án. Không phải chuyện phong cách; `int` ở
đây là WA chắc chắn trên test lớn.

## Khi nào mảng cộng dồn áp dụng được

Mọi đại lượng cộng tích lũy được từ trái sang phải và **trừ được**:
tổng, số lượng (bao nhiêu phần tử chẵn trong đoạn), số lần xuất hiện.
Đại lượng như max/min **không trừ được** — max cộng dồn không trả lời
được max trên đoạn. Cần cấu trúc khác (module sau).
""",
)

write_lesson(
    M,
    "hsg-m8-2d",
    "2D Prefix Sums",
    "Extend the idea to grids: any rectangle sum with four lookups.",
    13,
    """## From line to grid

Given an n x m grid, build P where `P[i][j]` = sum of the rectangle from
(1,1) to (i,j):

```cpp
for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j) {
        long long x; cin >> x;
        P[i][j] = x + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
    }
```

The `- P[i-1][j-1]` corrects the top-left quadrant being added twice.

### Rectangle sum by inclusion-exclusion

Sum of rows r1..r2, columns c1..c2:

```cpp
long long s = P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1];
```

Read it as: big rectangle, cut off the strip above, cut off the strip on
the left, put the double-cut corner back. A wrong sign on the last term
passes every query with r1 = c1 = 1 and fails the rest — exactly the
kind of bug hidden tests are built to catch.

Worked example: grid [[1,2,3],[4,5,6]]. P[2][3] = 21. Region
(1,1)-(1,2): P[1][2] - P[0][2] - P[1][0] + P[0][0] = 3. Single cell
(2,2) in [[1,2],[3,4]]: P[2][2] - P[1][2] - P[2][1] + P[1][1]
= 10 - 3 - 4 + 1 = 4.

### Costs

Build O(nm), each query O(1), memory O(nm) longs. For n = m = 1000 that
is 8 MB — usually fine, but state it when the memory limit is tight.
""",
    "Mảng cộng dồn 2 chiều",
    "Mở rộng ý tưởng lên lưới: tổng mọi hình chữ nhật bằng bốn lần tra bảng.",
    """## Từ đường thẳng tới lưới

Cho lưới n x m, dựng P với `P[i][j]` = tổng hình chữ nhật từ (1,1) tới
(i,j):

```cpp
for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j) {
        long long x; cin >> x;
        P[i][j] = x + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
    }
```

Số `- P[i-1][j-1]` sửa chỗ góc trên-trái bị cộng hai lần.

### Tổng hình chữ nhật bằng bao hàm - loại trừ

Tổng hàng r1..r2, cột c1..c2:

```cpp
long long s = P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1];
```

Đọc là: hình lớn, cắt dải phía trên, cắt dải bên trái, trả lại góc bị
cắt hai lần. Sai dấu ở số hạng cuối vẫn pass mọi truy vấn có r1 = c1 = 1
và fail phần còn lại — đúng kiểu bug mà test ẩn được thiết kế để bắt.

Ví dụ: lưới [[1,2,3],[4,5,6]]. P[2][3] = 21. Vùng (1,1)-(1,2):
P[1][2] - P[0][2] - P[1][0] + P[0][0] = 3. Ô đơn (2,2) trong
[[1,2],[3,4]]: P[2][2] - P[1][2] - P[2][1] + P[1][1] = 10 - 3 - 4 + 1 = 4.

### Chi phí

Dựng O(nm), mỗi truy vấn O(1), bộ nhớ O(nm) số long. Với n = m = 1000
là 8 MB — thường ổn, nhưng hãy nêu ra khi giới hạn bộ nhớ chật.
""",
)

A1 = challenge(
    "hsg-p8-range-sum",
    "Range Sums",
    T(
        "**Description:** Given n integers and q queries, each query gives indices l and r (1-based).",
        "Print the sum a[l] + a[l+1] + ... + a[r] for every query.",
        "",
        "**Input:** Line 1: n q (1 <= n, q <= 2*10^5). Line 2: n integers (-10^9 <= a_i <= 10^9).",
        "Next q lines: l r (1 <= l <= r <= n).",
        "**Output:** q lines — the range sums.",
        "",
        "**Example:** `5 2` / `3 -1 4 1 -5` / `1 3` / `2 5` -> `6` / `-1`.",
    ),
    [
        contest_test("sample", T("5 2", "3 -1 4 1 -5", "1 3", "2 5"), T("6", "-1"),
                     "P = 0 3 2 6 7 2; sums 6 and -1."),
        contest_test("single element", T("1 1", "7", "1 1"), T("7"),
                     "One element, one query."),
        contest_test("whole array", T("4 1", "1 2 3 4", "1 4"), T("10"),
                     "P[4] - P[0] = 10."),
        contest_test("negatives", T("3 2", "-5 -5 -5", "1 2", "3 3"), T("-10", "-5"),
                     "All negative sums — int would still hold these, the prefix pattern must not break."),
    ],
    level="imitation",
    difficulty="beginner",
)

A2 = challenge(
    "hsg-p8-even-count",
    "Even Count in Range",
    T(
        "**Description:** Given n integers and q queries l r, count how many elements",
        "in a[l..r] are even.",
        "",
        "**Input:** Line 1: n q (1 <= n, q <= 2*10^5). Line 2: n integers (-10^9 <= a_i <= 10^9).",
        "Next q lines: l r (1 <= l <= r <= n).",
        "**Output:** q lines — the counts.",
        "",
        "**Example:** `6 2` / `2 3 4 5 6 7` / `1 6` / `2 4` -> `3` / `1`.",
    ),
    [
        contest_test("sample", T("6 2", "2 3 4 5 6 7", "1 6", "2 4"), T("3", "1"),
                     "Evens overall: 2, 4, 6. In positions 2..4 only 4."),
        contest_test("all odd", T("3 1", "1 3 5", "1 3"), T("0"),
                     "No evens anywhere — prefix of zeros."),
        contest_test("all even", T("4 2", "2 2 2 2", "1 4", "2 3"), T("4", "2"),
                     "Counts subtract like sums."),
        contest_test("single", T("1 1", "8", "1 1"), T("1"),
                     "Smallest case."),
    ],
    level="guided",
    difficulty="beginner",
)

A3 = challenge(
    "hsg-p8-grid-sum",
    "Rectangle Sums",
    T(
        "**Description:** Given an n x m grid and q queries (r1 c1 r2 c2), print the sum of",
        "the rectangle with top-left corner (r1, c1) and bottom-right corner (r2, c2),",
        "1-based.",
        "",
        "**Input:** Line 1: n m q (1 <= n, m <= 1000, 1 <= q <= 10^5).",
        "Next n lines: m integers each (|a_ij| <= 10^9).",
        "Next q lines: r1 c1 r2 c2 (1 <= r1 <= r2 <= n, 1 <= c1 <= c2 <= m).",
        "**Output:** q lines — the rectangle sums.",
        "",
        "**Example:** `2 3 2` / `1 2 3` / `4 5 6` / `1 1 2 3` / `1 1 1 2` -> `21` / `3`.",
    ),
    [
        contest_test("sample", T("2 3 2", "1 2 3", "4 5 6", "1 1 2 3", "1 1 1 2"), T("21", "3"),
                     "Whole grid 21; top row first two cells 3."),
        contest_test("single cell", T("1 1 1", "9", "1 1 1 1"), T("9"),
                     "One cell is its own rectangle."),
        contest_test("corner cell", T("2 2 1", "1 2", "3 4", "2 2 2 2"), T("4"),
                     "P22 - P12 - P21 + P11 = 10 - 3 - 4 + 1. A sign error here passes r1=c1=1 queries and fails this one."),
        contest_test("middle region", T("3 3 1", "1 2 3", "4 5 6", "7 8 9", "2 2 3 3"), T("28"),
                     "5 + 6 + 8 + 9 = 28."),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p8-zero-sum",
    "Zero-Sum Subarrays",
    T(
        "**Description:** Count the subarrays a[l..r] whose elements sum to exactly 0.",
        "The answer can reach n*(n+1)/2 — use 64-bit integers.",
        "",
        "**Input:** Line 1: n (1 <= n <= 2*10^5). Line 2: n integers (-10^9 <= a_i <= 10^9).",
        "**Output:** One integer — the number of zero-sum subarrays.",
        "",
        "**Example:** `5` / `1 -1 2 -2 3` -> `3` (the subarrays 1..2, 3..4, 1..4).",
    ),
    [
        contest_test("sample", T("5", "1 -1 2 -2 3"), T("3"),
                     "Prefixes 0 1 0 2 0 3 — three zeros, C(3,2) = 3 pairs."),
        contest_test("all zeros", T("3", "0 0 0"), T("6"),
                     "Four equal prefixes 0 0 0 0 -> C(4,2) = 6."),
        contest_test("none", T("3", "1 2 3"), T("0"),
                     "Strictly growing prefixes, no repeats."),
        contest_test("single zero", T("1", "0"), T("1"),
                     "The element itself is a zero-sum subarray — this is where forgetting the empty prefix shows."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p8-max-window",
    "Maximum Window",
    T(
        "**Description:** Given n integers and a window length k, find the maximum possible",
        "sum of k consecutive elements.",
        "",
        "**Input:** Line 1: n k (1 <= k <= n <= 2*10^5). Line 2: n integers (-10^9 <= a_i <= 10^9).",
        "**Output:** One integer — the maximum window sum.",
        "",
        "**Example:** `6 3` / `2 -1 4 3 -2 5` -> `6` (window -1 4 3 or 3 -2 5...",
        "compute: -1+4+3 = 6).",
    ),
    [
        contest_test("sample", T("6 3", "2 -1 4 3 -2 5"), T("6"),
                     "Windows: 5, 6, 5, 6."),
        contest_test("all negative", T("4 2", "-5 -3 -8 -1"), T("-8"),
                     "Best window is -5 -3 = -8; a solution defaulting best to 0 fails here."),
        contest_test("whole array", T("3 3", "1 2 3"), T("6"),
                     "k = n: one window."),
        contest_test("k equals 1", T("5 1", "4 -2 7 -9 1"), T("7"),
                     "Window of one — just the maximum element."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p8-range-sum": vi_challenge(
        "Tổng đoạn",
        T(
            "**Đề bài:** Cho n số nguyên và q truy vấn, mỗi truy vấn cho chỉ số l và r (cơ sở 1).",
            "In tổng a[l] + a[l+1] + ... + a[r] của mỗi truy vấn.",
            "",
            "**Dữ liệu vào:** Dòng 1: n q (1 <= n, q <= 2*10^5). Dòng 2: n số nguyên (-10^9 <= a_i <= 10^9).",
            "q dòng tiếp: l r (1 <= l <= r <= n).",
            "**Dữ liệu ra:** q dòng — các tổng đoạn.",
            "",
            "**Ví dụ:** `5 2` / `3 -1 4 1 -5` / `1 3` / `2 5` -> `6` / `-1`.",
        ),
        [
            ("sample", "P = 0 3 2 6 7 2; các tổng 6 và -1."),
            ("single element", "Một phần tử, một truy vấn."),
            ("whole array", "P[4] - P[0] = 10."),
            ("negatives", "Tổng toàn âm — mẫu số cộng dồn phải giữ nguyên vẹn."),
        ],
    ),
    "hsg-p8-even-count": vi_challenge(
        "Đếm số chẵn trong đoạn",
        T(
            "**Đề bài:** Cho n số nguyên và q truy vấn l r, đếm bao nhiêu phần tử trong a[l..r] là số chẵn.",
            "",
            "**Dữ liệu vào:** Dòng 1: n q (1 <= n, q <= 2*10^5). Dòng 2: n số nguyên (-10^9 <= a_i <= 10^9).",
            "q dòng tiếp: l r (1 <= l <= r <= n).",
            "**Dữ liệu ra:** q dòng — số lượng.",
            "",
            "**Ví dụ:** `6 2` / `2 3 4 5 6 7` / `1 6` / `2 4` -> `3` / `1`.",
        ),
        [
            ("sample", "Số chẵn toàn mảng: 2, 4, 6. Trong vị trí 2..4 chỉ có 4."),
            ("all odd", "Không có số chẵn nào — cộng dồn toàn 0."),
            ("all even", "Số lượng trừ nhau giống như tổng."),
            ("single", "Trường hợp nhỏ nhất."),
        ],
    ),
    "hsg-p8-grid-sum": vi_challenge(
        "Tổng hình chữ nhật",
        T(
            "**Đề bài:** Cho lưới n x m và q truy vấn (r1 c1 r2 c2), in tổng hình chữ nhật có góc trên-trái (r1, c1)",
            "và góc dưới-phải (r2, c2), cơ sở 1.",
            "",
            "**Dữ liệu vào:** Dòng 1: n m q (1 <= n, m <= 1000, 1 <= q <= 10^5).",
            "n dòng tiếp: mỗi dòng m số nguyên (|a_ij| <= 10^9).",
            "q dòng tiếp: r1 c1 r2 c2 (1 <= r1 <= r2 <= n, 1 <= c1 <= c2 <= m).",
            "**Dữ liệu ra:** q dòng — các tổng hình chữ nhật.",
            "",
            "**Ví dụ:** `2 3 2` / `1 2 3` / `4 5 6` / `1 1 2 3` / `1 1 1 2` -> `21` / `3`.",
        ),
        [
            ("sample", "Cả lưới 21; hai ô đầu hàng trên 3."),
            ("single cell", "Một ô là hình chữ nhật của chính nó."),
            ("corner cell", "P22 - P12 - P21 + P11 = 10 - 3 - 4 + 1. Sai dấu ở đây vẫn pass truy vấn r1=c1=1 và fail test này."),
            ("middle region", "5 + 6 + 8 + 9 = 28."),
        ],
    ),
    "hsg-p8-zero-sum": vi_challenge(
        "Đoạn con tổng 0",
        T(
            "**Đề bài:** Đếm các đoạn con a[l..r] có tổng đúng bằng 0.",
            "Đáp án có thể tới n*(n+1)/2 — dùng số nguyên 64 bit.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 2*10^5). Dòng 2: n số nguyên (-10^9 <= a_i <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — số đoạn con tổng 0.",
            "",
            "**Ví dụ:** `5` / `1 -1 2 -2 3` -> `3` (các đoạn 1..2, 3..4, 1..4).",
        ),
        [
            ("sample", "Cộng dồn 0 1 0 2 0 3 — ba số 0, C(3,2) = 3 cặp."),
            ("all zeros", "Bốn cộng dồn bằng nhau 0 0 0 0 -> C(4,2) = 6."),
            ("none", "Cộng dồn tăng ngặt, không lặp."),
            ("single zero", "Bản phần tử đó là một đoạn tổng 0 — đây là chỗ quên tiền tố rỗng sẽ lộ."),
        ],
    ),
    "hsg-p8-max-window": vi_challenge(
        "Cửa sổ lớn nhất",
        T(
            "**Đề bài:** Cho n số nguyên và độ dài cửa sổ k, tìm tổng lớn nhất của k phần tử liên tiếp.",
            "",
            "**Dữ liệu vào:** Dòng 1: n k (1 <= k <= n <= 2*10^5). Dòng 2: n số nguyên (-10^9 <= a_i <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — tổng cửa sổ lớn nhất.",
            "",
            "**Ví dụ:** `6 3` / `2 -1 4 3 -2 5` -> `6` (cửa sổ -1 4 3).",
        ),
        [
            ("sample", "Các cửa sổ: 5, 6, 5, 6."),
            ("all negative", "Cửa sổ tốt nhất là -5 -3 = -8; lời giải khởi tạo best = 0 sẽ fail test này."),
            ("whole array", "k = n: đúng một cửa sổ."),
            ("k equals 1", "Cửa sổ một phần tử — chính là phần tử lớn nhất."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p8-prefix",
    "Prefix Sum Problem Set",
    "Five contest problems drilled on 1D/2D prefixes, counting, and windows — byte-exact grading.",
    "Bài tập mảng cộng dồn",
    "Năm bài thi đấu luyện cộng dồn 1D/2D, đếm, và cửa sổ — chấm đúng từng byte.",
    "hsg-m8-2d",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p8-range-sum",
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
            "hsg-p8-even-count",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> C(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        C[i] = C[i-1] + (x % 2 == 0);
    }
    while (q--) {
        int l, r; in >> l >> r;
        out << C[r] - C[l-1] << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> C(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        C[i] = C[i-1] + (x % 2 == 0);
    }
    while (q--) {
        int l, r; in >> l >> r;
        // near-miss: never subtracts the prefix before l
        out << C[r] << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsg-p8-grid-sum",
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<long long>> P(n + 1, vector<long long>(m + 1, 0));
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) {
            long long x; in >> x;
            P[i][j] = x + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
        }
    while (q--) {
        int r1, c1, r2, c2; in >> r1 >> c1 >> r2 >> c2;
        out << P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1] << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<long long>> P(n + 1, vector<long long>(m + 1, 0));
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) {
            long long x; in >> x;
            P[i][j] = x + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
        }
    while (q--) {
        int r1, c1, r2, c2; in >> r1 >> c1 >> r2 >> c2;
        // near-miss: the correction corner is SUBTRACTED, not added back
        out << P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] - P[r1-1][c1-1] << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsg-p8-zero-sum",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    map<long long, long long> cnt;
    cnt[0] = 1;  // empty prefix: subarrays starting at index 1
    long long pre = 0, ans = 0;
    for (int i = 0; i < n; ++i) {
        pre += a[i];
        ans += cnt[pre];
        ++cnt[pre];
    }
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    map<long long, long long> cnt;
    // near-miss: no cnt[0] = 1 — subarrays starting at index 1 are lost
    long long pre = 0, ans = 0;
    for (int i = 0; i < n; ++i) {
        pre += a[i];
        ans += cnt[pre];
        ++cnt[pre];
    }
    out << ans << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p8-max-window",
            CPP_STD + cpp("""    int n; long long k; in >> n >> k;
    vector<long long> P(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        P[i] = P[i-1] + x;
    }
    long long best = P[k] - P[0];
    for (int i = 1; i + k <= n; ++i)
        best = max(best, P[i+k] - P[i]);
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long k; in >> n >> k;
    vector<long long> P(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        long long x; in >> x;
        P[i] = P[i-1] + x;
    }
    // near-miss: window length k-1 instead of k
    long long best = P[k-1] - P[0];
    for (int i = 1; i + k - 1 <= n; ++i)
        best = max(best, P[i+k-1] - P[i]);
    out << best << "{{NL}}";
""") + END,
        ),
    ],
)

CH8 = challenge(
    "hsg-cp-m8-split",
    "Three Equal Parts",
    T(
        "**Description:** Count the ways to cut the array a[1..n] into three contiguous,",
        "non-empty parts with equal sums. Cuts are after position i and after position j",
        "(1 <= i < j <= n-1... precisely: part 1 is a[1..i], part 2 is a[i+1..j], part 3 is",
        "a[j+1..n]). Print the number of valid (i, j) pairs. The answer fits in 64 bits.",
        "",
        "**Input:** Line 1: n (3 <= n <= 2*10^5). Line 2: n integers (-10^9 <= a_i <= 10^9).",
        "**Output:** One integer — the number of ways.",
        "",
        "**Example:** `5` / `1 2 3 0 3` -> `2` (cuts after 2 and 3; after 2 and 4).",
    ),
    [
        contest_test("sample", T("5", "1 2 3 0 3"), T("2"),
                     "need = 3; j = 3 and j = 4 have P_j = 6; each sees one earlier P = 3."),
        contest_test("zeros three", T("3", "0 0 0"), T("1"),
                     "Only cuts (1, 2) work — the classic zero-counting trap."),
        contest_test("zeros four", T("4", "0 0 0 0"), T("3"),
                     "C(3,2) = 3 pairs of cuts."),
        contest_test("not divisible", T("3", "1 1 2"), T("0"),
                     "Total 4 is not divisible by 3."),
        contest_test("negatives", T("6", "-1 -1 -1 -1 -1 -1"), T("1"),
                     "Parts of two elements each."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP8 = vi_challenge(
    "Chia ba phần bằng nhau",
    T(
        "**Đề bài:** Đếm số cách cắt mảng a[1..n] thành ba phần liên tiếp, khác rỗng, có tổng bằng nhau.",
        "Cắt sau vị trí i và sau vị trí j: phần 1 là a[1..i], phần 2 là a[i+1..j], phần 3 là a[j+1..n].",
        "In số cặp (i, j) hợp lệ. Đáp án vừa 64 bit.",
        "",
        "**Dữ liệu vào:** Dòng 1: n (3 <= n <= 2*10^5). Dòng 2: n số nguyên (-10^9 <= a_i <= 10^9).",
        "**Dữ liệu ra:** Một số nguyên — số cách cắt.",
        "",
        "**Ví dụ:** `5` / `1 2 3 0 3` -> `2` (cắt sau 2 và 3; sau 2 và 4).",
    ),
    [
        ("sample", "need = 3; j = 3 và j = 4 có P_j = 6; mỗi chỗ thấy một P = 3 đứng trước."),
        ("zeros three", "Chỉ cặp cắt (1, 2) thỏa — bẫy đếm số 0 kinh điển."),
        ("zeros four", "C(3,2) = 3 cặp cắt."),
        ("not divisible", "Tổng 4 không chia hết cho 3."),
        ("negatives", "Ba phần mỗi phần hai phần tử."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m8",
    "Checkpoint — Prefix Sums",
    "Pass the graded problem to finish the prefix-sums module.",
    15,
    """**Checkpoint — mảng cộng dồn.** Pass the graded challenge below to
complete the module. It combines everything: a divisibility pre-check,
prefix counting from both directions, and the non-empty-parts boundary
conditions. Solve it on paper first: what must P[i], P[j], and the total
satisfy for cuts (i, j) to be valid?

**Điểm kiểm tra — mảng cộng dồn.** Pass bài chấm bên dưới để hoàn thành
module. Bài gộp mọi nội dung: kiểm tra chia hết trước, đếm cộng dồn hai
chiều, và điều kiện biên phần khác rỗng. Giải trên giấy trước: P[i], P[j]
và tổng phải thỏa gì để cặp cắt (i, j) hợp lệ?
""",
    "Checkpoint — Prefix Sums",
    "Pass the graded problem to finish the prefix-sums module.",
    """**Checkpoint — mảng cộng dồn.** Pass bài chấm bên dưới để hoàn thành
module. Bài gộp mọi nội dung: kiểm tra chia hết trước, đếm cộng dồn hai
chiều, và điều kiện biên phần khác rỗng. Giải trên giấy trước: P[i], P[j]
và tổng phải thỏa gì để cặp cắt (i, j) hợp lệ?
""",
    CH8,
    VI_CP8,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    long long total = 0;
    for (int i = 1; i <= n; ++i) total += a[i];
    if (total % 3 != 0) { out << 0 << "{{NL}}"; return; }
    long long need = total / 3;
    vector<long long> P(n + 1, 0);
    for (int i = 1; i <= n; ++i) P[i] = P[i-1] + a[i];
    // cnt[i] = number of first-cut positions p <= i with P[p] == need
    vector<long long> cnt(n + 1, 0);
    for (int i = 1; i <= n; ++i) cnt[i] = cnt[i-1] + (P[i] == need);
    long long ans = 0;
    // second cut j: part 2 non-empty (j >= 2), part 3 non-empty (j <= n-1)
    for (int j = 2; j <= n - 1; ++j)
        if (P[j] == 2 * need) ans += cnt[j-1];
    out << ans << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; ++i) in >> a[i];
    long long total = 0;
    for (int i = 1; i <= n; ++i) total += a[i];
    if (total % 3 != 0) { out << 0 << "{{NL}}"; return; }
    long long need = total / 3;
    vector<long long> P(n + 1, 0);
    for (int i = 1; i <= n; ++i) P[i] = P[i-1] + a[i];
    vector<long long> cnt(n + 1, 0);
    for (int i = 1; i <= n; ++i) cnt[i] = cnt[i-1] + (P[i] == need);
    long long ans = 0;
    // near-miss: j runs 1..n — allows an EMPTY first or third part,
    // which inflates the count on arrays of zeros
    for (int j = 1; j <= n; ++j)
        if (P[j] == 2 * need) ans += cnt[j-1];
    out << ans << "{{NL}}";
""") + END,
)

print("M8 done")
