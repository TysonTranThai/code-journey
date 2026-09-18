#!/usr/bin/env python3
"""HSG — Module 9: hsg-diff (mảng hiệu — difference arrays).

Range updates in O(1) with a difference array, reconstruction by prefix
sum; 2D difference arrays for rectangle painting; exact-coverage counting.
Conventions: T() for test I/O (real newlines), cpp() for bodies.
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
using namespace std;
void solve(std::istream& in, std::ostream& out) {
""")

END = "}" + NL

M = "hsg-diff"
write_module(
    M,
    "Difference Arrays",
    "O(1) range updates: 1D difference arrays, reconstruction by prefix sum, 2D rectangle painting, exact-coverage counting.",
    "Mảng hiệu",
    "Cập nhật đoạn O(1): mảng hiệu 1D, dựng lại bằng cộng dồn, tô hình chữ nhật 2D, đếm phủ đúng k lần.",
    ["hsg-m9-basics", "hsg-m9-2d", "hsg-cp-m9"],
    ["hsg-p9-diff"],
)

write_lesson(
    M,
    "hsg-m9-basics",
    "Difference Arrays — O(1) Range Updates",
    "Flip the roles: prefix sums answered many queries after one build; difference arrays apply many updates before one build.",
    14,
    """## The complement of prefix sums

Prefix sums: read the array once, answer q range queries. Difference
arrays: apply q range updates, then read the array once. Same tool, run
backwards.

### The trick

To add v to every a[l..r], do two point updates:

```cpp
d[l] += v;
d[r + 1] -= v;   // the "stop" marker sits one past the range
```

After all updates, the real array is the prefix sum of d:

```cpp
for (int i = 1; i <= n; ++i) d[i] += d[i-1];
// now d[i] holds the final value of position i
```

Why: the running sum rises by v when it passes the `d[l]` marker and
falls back when it passes `d[r+1]`. Between them it carries exactly +v.

Worked example: add 5 to a[2..4] of a 5-array. d = [0,0,5,0,0,-5,0] (the
stop at index 5). Prefix: 0 5 5 5 5 0 — positions 2,3,4 got +5, position
5 got +5-5 = 0.

### The two classic bugs

- Writing `d[r] -= v` instead of `d[r+1]`: every range loses its last
  element. Tests with r = n often crash it (index n+1 exists in a sized
  n+2 array — remember to size it n+2 and never touch index n+1 in the
  final read).
- Forgetting the `d[r+1]` stop entirely: everything right of l is
  polluted forever.

### Cost model

Each update O(1), reconstruction O(n), memory O(n). If updates and
queries interleave (update, ask, update, ask), a difference array does
not help — you would rebuild each time. That is the signal for a segment
tree (much later).
""",
    "Mảng hiệu — Cập nhật đoạn O(1)",
    "Đảo vai: cộng dồn trả nhiều truy vấn sau một lần dựng; mảng hiệu áp nhiều cập nhật trước một lần dựng.",
    """## Phần bổ đôi của mảng cộng dồn

Cộng dồn: đọc mảng một lần, trả q truy vấn đoạn. Mảng hiệu: áp q cập
nhật đoạn, rồi đọc mảng một lần. Cùng một công cụ, chạy ngược chiều.

### Mẹo cốt lõi

Để cộng v vào mọi a[l..r], làm hai cập nhật điểm:

```cpp
d[l] += v;
d[r + 1] -= v;   // "mốc dừng" đứng ngay sau đoạn
```

Sau mọi cập nhật, mảng thật là cộng dồn của d:

```cpp
for (int i = 1; i <= n; ++i) d[i] += d[i-1];
// lúc này d[i] là giá trị cuối của vị trí i
```

Vì sao: tổng chạy tăng thêm v khi đi qua mốc `d[l]` và trở lại khi đi
qua `d[r+1]`. Giữa hai mốc nó mang đúng +v.

Ví dụ: cộng 5 vào a[2..4] của mảng 5 phần tử. d = [0,0,5,0,0,-5,0]
(mốc dừng ở chỉ số 5). Cộng dồn: 0 5 5 5 5 0 — vị trí 2,3,4 được +5,
vị trí 5 được +5-5 = 0.

### Hai bug kinh điển

- Viết `d[r] -= v` thay vì `d[r+1]`: mọi đoạn mất phần tử cuối. Test có
  r = n thường làm nó crash (mảng phải size n+2, và không bao giờ đọc
  chỉ số n+1 lúc cuối).
- Quên hẳn mốc `d[r+1]`: mọi vị trí bên phải l bị ô nhiễm vĩnh viễn.

### Mô hình chi phí

Mỗi cập nhật O(1), dựng lại O(n), bộ nhớ O(n). Nếu cập nhật và truy vấn
đan xen (cập nhật, hỏi, cập nhật, hỏi) thì mảng hiệu không giúp gì —
phải dựng lại liên tục. Đó là tín hiệu cho cây đoạn (về sau).
""",
)

write_lesson(
    M,
    "hsg-m9-2d",
    "2D Difference Arrays",
    "Paint rectangles in O(1) each: four corner updates, reconstruct with 2D prefix sums.",
    13,
    """## Four corners per rectangle

To add v to every cell of the rectangle (r1, c1) - (r2, c2):

```cpp
D[r1][c1]     += v;
D[r1][c2+1]   -= v;
D[r2+1][c1]   -= v;
D[r2+1][c2+1] += v;   // the double-cut corner goes back
```

Then a 2D prefix sum over D reconstructs the painted grid. The corner
`D[r2+1][c2+1] += v` is the inclusion-exclusion term: without it, every
cell right of c2 AND below r2 loses v twice.

Worked example: paint (1,1)-(2,2) on a 3x3 grid with v = 1. The final
grid is 1 1 0 / 1 1 0 / 0 0 0. If you forget the `+= v` corner, the
bottom-right 2x2 block (rows 2-3, cols 2-3) becomes 0 -1 / -1 0 — the
double subtraction is visible.

### Boundaries

Size D as (n+2) x (m+2) so the r2+1/c2+1 indices never go out of range,
and only read the first n x m cells after reconstruction.

### Same trade-off as 1D

All rectangles first, then one O(nm) rebuild, then answer whatever you
need (max cell, count of cells >= k, exact-k coverage). Interleaved
paint-then-ask needs a real structure — not this tool.
""",
    "Mảng hiệu 2 chiều",
    "Tô hình chữ nhật O(1) mỗi cái: bốn cập nhật góc, dựng lại bằng cộng dồn 2D.",
    """## Bốn góc cho mỗi hình chữ nhật

Để cộng v vào mọi ô của hình chữ nhật (r1, c1) - (r2, c2):

```cpp
D[r1][c1]     += v;
D[r1][c2+1]   -= v;
D[r2+1][c1]   -= v;
D[r2+1][c2+1] += v;   // góc bị cắt đôi được trả lại
```

Sau đó một cộng dồn 2D trên D dựng lại lưới đã tô. Góc
`D[r2+1][c2+1] += v` chính là số hạng bao hàm - loại trừ: thiếu nó, mọi
ô vừa bên phải c2 VỪA dưới r2 bị trừ v hai lần.

Ví dụ: tô (1,1)-(2,2) trên lưới 3x3 với v = 1. Lưới cuối là
1 1 0 / 1 1 0 / 0 0 0. Nếu quên góc `+= v`, khối 2x2 dưới-phải (hàng
2-3, cột 2-3) thành 0 -1 / -1 0 — phép trừ đôi lộ diện.

### Biên

Size D là (n+2) x (m+2) để các chỉ số r2+1/c2+1 không bao giờ vượt mảng,
và chỉ đọc n x m ô đầu sau khi dựng lại.

### Cùng một sự đánh đổi như 1D

Tất cả hình chữ nhật trước, một lần dựng O(nm), rồi trả lời tuỳ ý (ô
lớn nhất, đếm ô >= k, phủ đúng k lần). Tô-hỏi-đan-xen cần cấu trúc thật
— không phải công cụ này.
""",
)

A1 = challenge(
    "hsg-p9-stamps",
    "Stamp Collector",
    T(
        "**Description:** A strip of n positions starts at 0. Apply q updates: add v to every",
        "position in [l, r]. Print the final value of every position.",
        "",
        "**Input:** Line 1: n q (1 <= n, q <= 2*10^5). Next q lines: l r v (1 <= l <= r <= n,",
        "-10^9 <= v <= 10^9).",
        "**Output:** n integers — the final values, space-separated.",
        "",
        "**Example:** `5 2` / `2 4 5` / `1 3 -2` -> `-2 3 3 5 0`.",
    ),
    [
        contest_test("sample", T("5 2", "2 4 5", "1 3 -2"), T("-2 3 3 5 0"),
                     "Position 2,3 get +5-2; position 4 only +5; position 5 untouched."),
        contest_test("single full", T("1 1", "1 1 7"), T("7"),
                     "One position, one update."),
        contest_test("r at n", T("4 1", "1 4 3"), T("3 3 3 3"),
                     "The stop marker lands at index n+1 — must exist, must not be read."),
        contest_test("negative values", T("3 2", "1 2 -5", "2 3 -5"), T("-5 -10 -5"),
                     "Accumulating negative updates."),
    ],
    level="imitation",
    difficulty="beginner",
)

A2 = challenge(
    "hsg-p9-overlap",
    "Busiest Hour",
    T(
        "**Description:** A cafe has n chairs and q visitors; visitor i occupies the time",
        "interval [l_i, r_i] (inclusive, in minutes). What is the maximum number of visitors",
        "present at the same minute?",
        "",
        "**Input:** Line 1: n q (1 <= n <= 10^6, 1 <= q <= 2*10^5). Next q lines: l r",
        "(1 <= l <= r <= n).",
        "**Output:** One integer — the maximum concurrent visitors.",
        "",
        "**Example:** `10 2` / `1 3` / `2 5` -> `2` (minute 2 or 3).",
    ),
    [
        contest_test("sample", T("10 2", "1 3", "2 5"), T("2"),
                     "Intervals [1,3] and [2,5] overlap on 2..3."),
        contest_test("no overlap", T("10 2", "1 2", "4 5"), T("1"),
                     "Disjoint intervals never exceed 1."),
        contest_test("all same", T("5 4", "2 2", "2 2", "2 2", "2 2"), T("4"),
                     "Point intervals stack — the marker trick must handle l == r."),
        contest_test("full cover", T("3 3", "1 3", "1 3", "1 3"), T("3"),
                     "Everything overlaps everything."),
    ],
    level="guided",
    difficulty="beginner",
)

A3 = challenge(
    "hsg-p9-sensor",
    "Sensor Readings",
    T(
        "**Description:** A sensor array of n cells starts at 0. First apply q updates",
        "(add v to every cell in [l, r]), then answer p point queries: the final value",
        "of cell x.",
        "",
        "**Input:** Line 1: n q p (1 <= n <= 10^6, 1 <= q, p <= 2*10^5). Next q lines:",
        "l r v. Next p lines: x (1 <= x <= n).",
        "**Output:** p lines — the final value of each queried cell.",
        "",
        "**Example:** `5 2 3` / `1 4 3` / `3 5 -1` / `1` / `3` / `5` -> `3` / `2` / `-1`.",
    ),
    [
        contest_test("sample", T("5 2 3", "1 4 3", "3 5 -1", "1", "3", "5"), T("3", "2", "-1"),
                     "Cell 1: +3. Cell 3: +3-1. Cell 5: -1."),
        contest_test("untouched cell", T("4 1 1", "1 2 9", "4"), T("0"),
                     "Query outside every range — diff arrays give 0 for free."),
        contest_test("same cell twice", T("2 2 1", "1 2 1", "1 2 1", "2"), T("2"),
                     "Two updates stack on the queried cell."),
        contest_test("single cell updates", T("3 3 2", "2 2 5", "2 2 -3", "1 2 2", "1", "2"), T("2", "4"),
                     "Point-range updates; queried cells 1 and 2."),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p9-posters",
    "Poster Wall",
    T(
        "**Description:** A wall is an n x m grid. Stick q rectangular posters: every cell of",
        "rectangle (r1, c1) - (r2, c2) gets one layer. Print the maximum number of layers",
        "on any cell.",
        "",
        "**Input:** Line 1: n m q (1 <= n, m <= 1000, 1 <= q <= 2*10^5). Next q lines:",
        "r1 c1 r2 c2.",
        "**Output:** One integer — the maximum layer count.",
        "",
        "**Example:** `3 3 2` / `1 1 2 2` / `2 2 3 3` -> `2` (cell (2,2) gets both posters).",
    ),
    [
        contest_test("sample", T("3 3 2", "1 1 2 2", "2 2 3 3"), T("2"),
                     "Posters overlap exactly at cell (2,2)."),
        contest_test("one poster", T("2 2 1", "1 1 2 2"), T("1"),
                     "A single poster everywhere on a 2x2 wall."),
        contest_test("disjoint", T("3 3 2", "1 1 1 1", "3 3 3 3"), T("1"),
                     "Corners only — never stack."),
        contest_test("nested", T("3 3 2", "1 1 3 3", "1 1 3 3"), T("2"),
                     "Same rectangle twice: every cell has 2 layers."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p9-once",
    "Painted Exactly Once",
    T(
        "**Description:** A fence of n planks gets q paint jobs, each covering [l, r]. Count",
        "the planks painted **exactly once**.",
        "",
        "**Input:** Line 1: n q (1 <= n, q <= 2*10^5). Next q lines: l r (1 <= l <= r <= n).",
        "**Output:** One integer — planks with exactly one coat.",
        "",
        "**Example:** `5 2` / `1 2` / `2 3` -> `2` (planks 1 and 3; plank 2 got two coats).",
    ),
    [
        contest_test("sample", T("5 2", "1 2", "2 3"), T("2"),
                     "Coverage 1 2 1 0 0 — two planks with exactly one coat."),
        contest_test("no paint", T("3 0"), T("0"),
                     "q = 0: every plank has zero coats — zero is not one."),
        contest_test("all twice", T("2 2", "1 2", "1 2"), T("0"),
                     "Everything double-coated."),
        contest_test("full once", T("4 1", "1 4"), T("4"),
                     "One coat everywhere."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p9-stamps": vi_challenge(
        "Người sưu tầm tem",
        T(
            "**Đề bài:** Dải n vị trí bắt đầu bằng 0. Áp q cập nhật: cộng v vào mọi vị trí trong [l, r].",
            "In giá trị cuối của mọi vị trí.",
            "",
            "**Dữ liệu vào:** Dòng 1: n q (1 <= n, q <= 2*10^5). q dòng tiếp: l r v (1 <= l <= r <= n,",
            "-10^9 <= v <= 10^9).",
            "**Dữ liệu ra:** n số nguyên — giá trị cuối, cách nhau bởi dấu cách.",
            "",
            "**Ví dụ:** `5 2` / `2 4 5` / `1 3 -2` -> `-2 3 3 5 0`.",
        ),
        [
            ("sample", "Vị trí 2,3 được +5-2; vị trí 4 chỉ +5; vị trí 5 không đổi."),
            ("single full", "Một vị trí, một cập nhật."),
            ("r at n", "Mốc dừng rơi vào chỉ số n+1 — phải tồn tại, không được đọc."),
            ("negative values", "Cộng dồn các cập nhật âm."),
        ],
    ),
    "hsg-p9-overlap": vi_challenge(
        "Giờ đông nhất",
        T(
            "**Đề bài:** Quán có n ghế và q khách; khách i chiếm khoảng thời gian [l_i, r_i] (bao cả hai đầu, tính theo phút).",
            "Số khách có mặt đồng thời lớn nhất tại cùng một phút là bao nhiêu?",
            "",
            "**Dữ liệu vào:** Dòng 1: n q (1 <= n <= 10^6, 1 <= q <= 2*10^5). q dòng tiếp: l r",
            "(1 <= l <= r <= n).",
            "**Dữ liệu ra:** Một số nguyên — số khách đồng thời lớn nhất.",
            "",
            "**Ví dụ:** `10 2` / `1 3` / `2 5` -> `2` (phút 2 hoặc 3).",
        ),
        [
            ("sample", "Hai khoảng [1,3] và [2,5] giao nhau trên 2..3."),
            ("no overlap", "Các khoảng rời nhau không bao giờ vượt 1."),
            ("all same", "Khoảng điểm xếp chồng — mẹo mốc phải xử lý được l == r."),
            ("full cover", "Mọi khoảng giao với mọi khoảng."),
        ],
    ),
    "hsg-p9-sensor": vi_challenge(
        "Số đo cảm biến",
        T(
            "**Đề bài:** Dãy n ô cảm biến bắt đầu bằng 0. Trước tiên áp q cập nhật (cộng v vào mọi ô trong [l, r]),",
            "rồi trả lời p truy vấn điểm: giá trị cuối của ô x.",
            "",
            "**Dữ liệu vào:** Dòng 1: n q p (1 <= n <= 10^6, 1 <= q, p <= 2*10^5). q dòng tiếp:",
            "l r v. p dòng tiếp: x (1 <= x <= n).",
            "**Dữ liệu ra:** p dòng — giá trị cuối của từng ô được hỏi.",
            "",
            "**Ví dụ:** `5 2 3` / `1 4 3` / `3 5 -1` / `1` / `3` / `5` -> `3` / `2` / `-1`.",
        ),
        [
            ("sample", "Ô 1: +3. Ô 3: +3-1. Ô 5: -1."),
            ("untouched cell", "Truy vấn ngoài mọi đoạn — mảng hiệu cho 0 miễn phí."),
            ("same cell twice", "Hai cập nhật cộng dồn trên ô được hỏi."),
            ("single cell updates", "Cập nhật đoạn điểm; hỏi ô 1 và ô 2."),
        ],
    ),
    "hsg-p9-posters": vi_challenge(
        "Tường áp phích",
        T(
            "**Đề bài:** Bức tường là lưới n x m. Dán q tấm áp phích hình chữ nhật: mọi ô của hình",
            "(r1, c1) - (r2, c2) được thêm một lớp. In số lớp lớn nhất trên một ô bất kỳ.",
            "",
            "**Dữ liệu vào:** Dòng 1: n m q (1 <= n, m <= 1000, 1 <= q <= 2*10^5). q dòng tiếp:",
            "r1 c1 r2 c2.",
            "**Dữ liệu ra:** Một số nguyên — số lớp lớn nhất.",
            "",
            "**Ví dụ:** `3 3 2` / `1 1 2 2` / `2 2 3 3` -> `2` (ô (2,2) nhận cả hai tấm).",
        ),
        [
            ("sample", "Hai tấm chỉ giao nhau tại ô (2,2)."),
            ("one poster", "Một tấm phủ mọi ô của tường 2x2."),
            ("disjoint", "Chỉ hai góc — không bao giờ xếp lớp."),
            ("nested", "Cùng một hình hai lần: mọi ô có 2 lớp."),
        ],
    ),
    "hsg-p9-once": vi_challenge(
        "Sơn đúng một lần",
        T(
            "**Đề bài:** Hàng rào n thanh ván được sơn q lần, lần thứ i phủ [l, r]. Đếm số ván",
            "được sơn **đúng một lần**.",
            "",
            "**Dữ liệu vào:** Dòng 1: n q (1 <= n, q <= 2*10^5). q dòng tiếp: l r (1 <= l <= r <= n).",
            "**Dữ liệu ra:** Một số nguyên — số ván có đúng một lớp sơn.",
            "",
            "**Ví dụ:** `5 2` / `1 2` / `2 3` -> `2` (ván 1 và 3; ván 2 được sơn hai lần).",
        ),
        [
            ("sample", "Độ phủ 1 2 1 0 0 — hai ván đúng một lớp."),
            ("no paint", "q = 0: mọi ván có 0 lớp — số 0 không phải số 1."),
            ("all twice", "Mọi ván được sơn hai lớp."),
            ("full once", "Một lớp trên khắp hàng rào."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p9-diff",
    "Difference Array Problem Set",
    "Range updates, overlaps, point queries after updates, 2D painting, exact coverage.",
    "Bài tập mảng hiệu",
    "Cập nhật đoạn, chồng lấn, truy vấn điểm sau cập nhật, tô 2D, phủ chính xác.",
    "hsg-m9-2d",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p9-stamps",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; long long v; in >> l >> r >> v;
        d[l] += v; d[r + 1] -= v;
    }
    for (int i = 1; i <= n; ++i) d[i] += d[i-1];
    for (int i = 1; i <= n; ++i)
        out << d[i] << (i < n ? " " : "{{NL}}");
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; long long v; in >> l >> r >> v;
        // near-miss: stop marker at r instead of r+1 — every range
        // loses its last element
        d[l] += v; d[r] -= v;
    }
    for (int i = 1; i <= n; ++i) d[i] += d[i-1];
    for (int i = 1; i <= n; ++i)
        out << d[i] << (i < n ? " " : "{{NL}}");
""") + END,
        ),
        (
            "hsg-p9-overlap",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        d[l] += 1; d[r + 1] -= 1;
    }
    long long cur = 0, best = 0;
    for (int i = 1; i <= n; ++i) {
        cur += d[i];
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        d[l] += 1; d[r + 1] -= 1;
    }
    // near-miss: takes the max over the RAW difference array — that
    // reports the busiest boundary, not the busiest minute
    long long best = 0;
    for (int i = 1; i <= n + 1; ++i) best = max(best, d[i]);
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p9-sensor",
            CPP_STD + cpp("""    int n, q, p; in >> n >> q >> p;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; long long v; in >> l >> r >> v;
        d[l] += v; d[r + 1] -= v;
    }
    for (int i = 1; i <= n; ++i) d[i] += d[i-1];
    for (int i = 0; i < p; ++i) {
        int x; in >> x;
        out << d[x] << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int n, q, p; in >> n >> q >> p;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; long long v; in >> l >> r >> v;
        d[l] += v; d[r + 1] -= v;
    }
    // near-miss: answers from the raw difference array — only the
    // first cell of each range is correct
    for (int i = 0; i < p; ++i) {
        int x; in >> x;
        out << d[x] << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsg-p9-posters",
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<long long>> D(n + 2, vector<long long>(m + 2, 0));
    for (int i = 0; i < q; ++i) {
        int r1, c1, r2, c2; in >> r1 >> c1 >> r2 >> c2;
        D[r1][c1] += 1; D[r1][c2+1] -= 1;
        D[r2+1][c1] -= 1; D[r2+1][c2+1] += 1;
    }
    long long best = 0;
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) {
            D[i][j] += D[i-1][j] + D[i][j-1] - D[i-1][j-1];
            best = max(best, D[i][j]);
        }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m, q; in >> n >> m >> q;
    vector<vector<long long>> D(n + 2, vector<long long>(m + 2, 0));
    for (int i = 0; i < q; ++i) {
        int r1, c1, r2, c2; in >> r1 >> c1 >> r2 >> c2;
        // near-miss: stop markers at r2/c2 instead of r2+1/c2+1, and
        // the closing corner shifts accordingly — every poster shrinks
        // by one row and one column
        D[r1][c1] += 1; D[r1][c2] -= 1;
        D[r2][c1] -= 1; D[r2][c2] += 1;
    }
    long long best = 0;
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j) {
            D[i][j] += D[i-1][j] + D[i][j-1] - D[i-1][j-1];
            best = max(best, D[i][j]);
        }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p9-once",
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        d[l] += 1; d[r + 1] -= 1;
    }
    long long ans = 0;
    for (int i = 1; i <= n; ++i) {
        d[i] += d[i-1];
        if (d[i] == 1) ++ans;
    }
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, q; in >> n >> q;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        d[l] += 1; d[r + 1] -= 1;
    }
    long long ans = 0;
    for (int i = 1; i <= n; ++i) {
        d[i] += d[i-1];
        // near-miss: at least one coat instead of exactly one
        if (d[i] >= 1) ++ans;
    }
    out << ans << "{{NL}}";
""") + END,
        ),
    ],
)

CH9 = challenge(
    "hsg-cp-m9-exact",
    "Exactly K Roads",
    T(
        "**Description:** A town has n intersections in a row. q new roads open, road i",
        "serving every intersection in [l_i, r_i]. Count the intersections served by",
        "**exactly k** roads.",
        "",
        "**Input:** Line 1: n q k (1 <= n, q <= 2*10^5, 0 <= k <= q). Next q lines: l r",
        "(1 <= l <= r <= n).",
        "**Output:** One integer — intersections with exactly k roads.",
        "",
        "**Example:** `5 2 1` / `1 2` / `2 4` -> `3` (intersections 1, 3, 4).",
    ),
    [
        contest_test("sample", T("5 2 1", "1 2", "2 4"), T("3"),
                     "Coverage 1 2 1 1 0 — three intersections with exactly one road."),
        contest_test("k zero", T("4 1 0", "1 2"), T("2"),
                     "Intersections 3 and 4 get no road — exactly 0 counts when k = 0."),
        contest_test("k equals q", T("3 2 2", "1 3", "1 3"), T("3"),
                     "Both roads serve everything."),
        contest_test("k bigger than any", T("3 1 5", "1 2"), T("0"),
                     "No intersection can have 5 roads."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP9 = vi_challenge(
    "Đúng K con đường",
    T(
        "**Đề bài:** Thị trấn có n ngã tư nằm trên một đường thẳng. q con đường mới khai trương,",
        "đường i phục vụ mọi ngã tư trong [l_i, r_i]. Đếm số ngã tư được phục vụ bởi",
        "**đúng k** con đường.",
        "",
        "**Dữ liệu vào:** Dòng 1: n q k (1 <= n, q <= 2*10^5, 0 <= k <= q). q dòng tiếp: l r",
        "(1 <= l <= r <= n).",
        "**Dữ liệu ra:** Một số nguyên — số ngã tư có đúng k đường.",
        "",
        "**Ví dụ:** `5 2 1` / `1 2` / `2 4` -> `3` (các ngã tư 1, 3, 4).",
    ),
    [
        ("sample", "Độ phủ 1 2 1 1 0 — ba ngã tư có đúng một đường."),
        ("k zero", "Ngã tư 3 và 4 không có đường — đúng 0 vẫn tính khi k = 0."),
        ("k equals q", "Cả hai đường phục vụ mọi nơi."),
        ("k bigger than any", "Không ngã tư nào có thể có 5 đường."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m9",
    "Checkpoint — Difference Arrays",
    "Pass the graded problem to finish the difference-arrays module.",
    15,
    """**Checkpoint — mảng hiệu.** Pass the graded challenge below to
complete the module. The k = 0 test is the subtle one: zero coverage is
a legitimate answer only when the problem says "exactly k" and k can be
0. A solution that counts `>= k` looks identical on most tests — until
the boundary arrives.

**Điểm kiểm tra — mảng hiệu.** Pass bài chấm bên dưới để hoàn thành
module. Test k = 0 là chỗ tinh tế: độ phủ 0 là đáp án hợp lệ chỉ khi đề
bài nói "đúng k" và k có thể bằng 0. Lời giải đếm `>= k` trông giống hệt
trên phần lớn test — cho tới khi biên xuất hiện.
""",
    "Checkpoint — Difference Arrays",
    "Pass the graded problem to finish the difference-arrays module.",
    """**Checkpoint — mảng hiệu.** Pass bài chấm bên dưới để hoàn thành
module. Test k = 0 là chỗ tinh tế: độ phủ 0 là đáp án hợp lệ chỉ khi đề
bài nói "đúng k" và k có thể bằng 0. Lời giải đếm `>= k` trông giống hệt
trên phần lớn test — cho tới khi biên xuất hiện.
""",
    CH9,
    VI_CP9,
    solution=CPP_STD + cpp("""    int n, q, k; in >> n >> q >> k;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        d[l] += 1; d[r + 1] -= 1;
    }
    long long ans = 0;
    for (int i = 1; i <= n; ++i) {
        d[i] += d[i-1];
        if (d[i] == k) ++ans;
    }
    out << ans << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, q, k; in >> n >> q >> k;
    vector<long long> d(n + 2, 0);
    for (int i = 0; i < q; ++i) {
        int l, r; in >> l >> r;
        d[l] += 1; d[r + 1] -= 1;
    }
    long long ans = 0;
    for (int i = 1; i <= n; ++i) {
        d[i] += d[i-1];
        // near-miss: "at least k" instead of "exactly k" — agrees
        // everywhere except where coverage exceeds k
        if (d[i] >= k) ++ans;
    }
    out << ans << "{{NL}}";
""") + END,
)

print("M9 done")
