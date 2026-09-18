#!/usr/bin/env python3
"""HSG — Module 7: hsg-search (linear search, binary search, lower/upper bound).

Binary search as an invariant, not a recipe: half-open bounds, overflow-safe
midpoint, and the first-true / last-true formulations that map onto
lower_bound / upper_bound. Closest-value and answer-search applications.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

Q = chr(92)
NL = chr(10)
CPP_STD = (
    "#include <iostream>" + NL +
    "#include <algorithm>" + NL +
    "using namespace std;" + NL +
    "void solve(std::istream& in, std::ostream& out) {" + NL
)

M = "hsg-search"
write_module(
    M, "Searching & Binary Search", "Linear search, binary search as an invariant, lower_bound/upper_bound, and binary search on the answer.",
    "Tìm kiếm & tìm kiếm nhị phân", "Tìm tuyến tính, tìm kiếm nhị phân như một bất biến, lower_bound/upper_bound, và tìm kiếm nhị phân trên đáp án.",
    ["hsg-m7-basics", "hsg-m7-answer", "hsg-cp-m7"], ["hsg-p7-search"],
)

# ------------------------------------------------------------------ lessons
write_lesson(
    M, "hsg-m7-basics",
    "Binary Search Done Right",
    "The loop invariant, the overflow-safe midpoint, and lower_bound/upper_bound.",
    13,
    """## Linear search and when it suffices

```cpp
int pos = -1;
for (int i = 0; i < n; ++i) if (a[i] == x) { pos = i; break; }
```

O(n). For one query on unsorted data, that is optimal — sorting for a
single lookup (O(n log n)) is slower. Binary search pays off with many
queries or pre-sorted data.

### The invariant formulation

Search the half-open range [lo, hi) for the first index with a[i] >= x:

```cpp
int lo = 0, hi = n;                 // answer is in [lo, hi]
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;   // overflow-safe midpoint
    if (a[mid] < x) lo = mid + 1;   // a[lo..mid] all < x
    else hi = mid;                  // answer is mid or left of it
}
// lo == n means every element is < x
```

The loop keeps one promise: **everything left of `lo` is too small,
everything at or right of `hi` is big enough**. The range shrinks every
iteration, so it terminates; when `lo == hi` the answer is pinned. This is
exactly `lower_bound(a.begin(), a.end(), x) - a.begin()`.

### lower_bound vs upper_bound

```cpp
int lb = lower_bound(b.begin(), b.end(), x) - b.begin();  // first index with b[i] >= x
int ub = upper_bound(b.begin(), b.end(), x) - b.begin();  // first index with b[i] > x
int count = ub - lb;                                      // occurrences of x
```

- Is x present? `lb < n && b[lb] == x`.
- How many times? `ub - lb`.
- Predecessor (largest value < x)? `lb - 1`, if `lb > 0`.

### The classic fatal bugs

- `mid = (lo + hi) / 2` — overflows for lo, hi near 2·10^9. Use
  `lo + (hi - lo) / 2`.
- `hi = n - 1` with `while (lo <= hi)` and `hi = mid` — infinite loop when
  the range is 2 elements. Prefer the half-open form above; it cannot hang.
- Binary search on **unsorted** data — the invariant silently means
  nothing. Sort first (and remember sorting permutes indices).""",
    "Tìm kiếm nhị phân chuẩn",
    "Bất biến của vòng lặp, điểm giữa an toàn tràn số, và lower_bound/upper_bound.",
    """## Tìm tuyến tính và khi nào là đủ

```cpp
int pos = -1;
for (int i = 0; i < n; ++i) if (a[i] == x) { pos = i; break; }
```

O(n). Với một truy vấn trên dữ liệu chưa sắp, đó là tối ưu — sắp xếp chỉ
để tra một lần (O(n log n)) còn chậm hơn. Tìm kiếm nhị phân có lợi khi có
nhiều truy vấn hoặc dữ liệu đã sắp sẵn.

### Dạng bất biến

Tìm chỉ số đầu tiên với a[i] >= x trong đoạn nửa mở [lo, hi):

```cpp
int lo = 0, hi = n;                 // đáp án nằm trong [lo, hi]
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;   // điểm giữa an toàn tràn số
    if (a[mid] < x) lo = mid + 1;   // a[lo..mid] đều < x
    else hi = mid;                  // đáp án là mid hoặc bên trái
}
// lo == n nghĩa là mọi phần tử đều < x
```

Vòng lặp giữ một lời hứa: **mọi thứ bên trái `lo` đều quá nhỏ, mọi thứ từ
`hi` trở đi đều đủ lớn**. Đoạn thu hẹp mỗi vòng nên chắc chắn dừng; khi
`lo == hi` đáp án được khoanh đúng. Đây chính là
`lower_bound(a.begin(), a.end(), x) - a.begin()`.

### lower_bound vs upper_bound

```cpp
int lb = lower_bound(b.begin(), b.end(), x) - b.begin();  // chỉ số đầu với b[i] >= x
int ub = upper_bound(b.begin(), b.end(), x) - b.begin();  // chỉ số đầu với b[i] > x
int count = ub - lb;                                      // số lần xuất hiện của x
```

- x có mặt? `lb < n && b[lb] == x`.
- Bao nhiêu lần? `ub - lb`.
- Tiền nhiệm (giá trị lớn nhất < x)? `lb - 1`, nếu `lb > 0`.

### Các lỗi chí mạng kinh điển

- `mid = (lo + hi) / 2` — tràn số khi lo, hi gần 2·10^9. Dùng
  `lo + (hi - lo) / 2`.
- `hi = n - 1` với `while (lo <= hi)` và `hi = mid` — vòng lặp vô hạn khi
  đoạn còn 2 phần tử. Hãy dùng dạng nửa mở ở trên; nó không thể treo.
- Tìm kiếm nhị phân trên dữ liệu **chưa sắp** — bất biến im lặng mất nghĩa.
  Sắp trước (và nhớ rằng sắp làm xáo trộn chỉ số).""",
)
write_lesson(
    M, "hsg-m7-answer",
    "Binary Search on the Answer",
    "When the answer itself can be guessed and checked: the strongest beginner-level technique.",
    14,
    """## Guess, check, narrow

Some problems do not ask "find this value in an array" — they ask for the
best feasible value of something. If feasibility is **monotone** (once
feasible at value v, feasible at every easier value), you can binary
search the answer itself:

```
lo = smallest possible answer, hi = largest possible answer
while (lo < hi) {
    mid = lo + (hi - lo + 1) / 2;      // round UP for last-true search
    if (feasible(mid)) lo = mid;       // mid works — try bigger
    else hi = mid - 1;                 // mid fails — go smaller
}
// lo is the largest feasible value
```

`feasible(v)` is a greedy/checker function you write — often O(n). Total:
O(n log(range)).

### Worked example — maximum minimum distance

n positions on a line, place k cows so the **smallest** gap is as large
as possible. Feasibility of gap d: greedily place a cow every time the
distance since the last placement reaches d.

```cpp
bool feasible(const vector<long long>& pos, int k, long long d) {
    int used = 1;
    long long last = pos[0];
    for (int i = 1; i < (int)pos.size(); ++i)
        if (pos[i] - last >= d) { ++used; last = pos[i]; }
    return used >= k;
}
// binary search d in [1, pos.back() - pos.front()]
```

Why greedy is right inside the checker: placing each cow as early as
possible never hurts — any valid placement can be shifted left.

### Rounding direction is everything

- Searching **first true** (smallest feasible): `mid = lo + (hi-lo)/2`,
  `if feasible: hi = mid else lo = mid + 1`.
- Searching **last true** (largest feasible): `mid = lo + (hi-lo+1)/2`,
  `if feasible: lo = mid else hi = mid - 1`.

Mixing the two directions is the most common way binary search silently
returns a neighbor of the true answer. When unsure, hand-simulate a range
of size 2 and size 3.

### Real contest signal

If the statement says "minimize the maximum ..." or "maximize the
minimum ...", that phrasing is a huge hint: those objectives are monotone
in the answer — binary search on the answer is the standard attack.""",
    "Tìm kiếm nhị phân trên đáp án",
    "Khi chính đáp án có thể đoán và kiểm tra: kỹ thuật mạnh nhất của trình mới bắt đầu.",
    """## Đoán, kiểm tra, thu hẹp

Một số bài không hỏi "tìm giá trị này trong mảng" — chúng hỏi giá trị tốt
nhất khả thi của một đại lượng. Nếu tính khả thi **đơn điệu** (một khi khả
thi tại giá trị v thì khả thi ở mọi giá trị dễ hơn), bạn có thể tìm kiếm
nhị phân chính đáp án:

```
lo = đáp án nhỏ nhất có thể, hi = đáp án lớn nhất có thể
while (lo < hi) {
    mid = lo + (hi - lo + 1) / 2;      // làm tròn LÊN cho dạng last-true
    if (feasible(mid)) lo = mid;       // mid ổn — thử lớn hơn
    else hi = mid - 1;                 // mid hỏng — về nhỏ hơn
}
// lo là giá trị khả thi lớn nhất
```

`feasible(v)` là hàm kiểm tra bạn tự viết — thường O(n). Tổng: O(n log(miền)).

### Ví dụ mẫu — khoảng cách tối thiểu lớn nhất

n vị trí trên một đường thẳng, đặt k con bò sao cho **khoảng cách nhỏ
nhất** càng lớn càng tốt. Khả thi với khoảng cách d: tham lam đặt con bò
mỗi khi khoảng cách từ lần đặt trước chạm d.

```cpp
bool feasible(const vector<long long>& pos, int k, long long d) {
    int used = 1;
    long long last = pos[0];
    for (int i = 1; i < (int)pos.size(); ++i)
        if (pos[i] - last >= d) { ++used; last = pos[i]; }
    return used >= k;
}
// tìm kiếm nhị phân d trong [1, pos.back() - pos.front()]
```

Vì sao tham lam đúng trong hàm kiểm tra: đặt mỗi con sớm nhất có thể
không bao giờ gây hại — mọi cách đặt hợp lệ đều dịch được sang trái.

### Hướng làm tròn là tất cả

- Tìm **first true** (khả thi nhỏ nhất): `mid = lo + (hi-lo)/2`,
  `if feasible: hi = mid else lo = mid + 1`.
- Tìm **last true** (khả thi lớn nhất): `mid = lo + (hi-lo+1)/2`,
  `if feasible: lo = mid else hi = mid - 1`.

Trộn hai hướng là cách phổ biến nhất để tìm kiếm nhị phân im lặng trả về
một đáp án láng giềng. Khi không chắc, mô phỏng tay đoạn kích thước 2 và 3.

### Tín hiệu đề bài thật

Nếu đề nói "tối thiểu hóa giá trị lớn nhất ..." hoặc "tối đa hóa giá trị
nhỏ nhất ...", đó là gợi ý rất lớn: các mục tiêu đó đơn điệu theo đáp án —
tìm kiếm nhị phân trên đáp án là hướng tấn công chuẩn.""",
)

# ------------------------------------------------------------------ practice
B1 = challenge(
    "hsg-p7-count-x",
    "Count Occurrences",
    """**Description:** Given a sorted array of n integers and q queries, for
each query value x print how many times x appears in the array.

**Input:** Line 1: n q (1 <= n, q <= 10^5). Line 2: n integers in
non-decreasing order (|a_i| <= 10^9). Next q lines: x (|x| <= 10^9).
**Output:** q lines — the count for each query (0 if absent).

**Example:** `6 2` / `1 2 2 2 5 9` / `2` / `7` -> `3`, `0`.""",
    [
        contest_test("sample", "6 2\\n1 2 2 2 5 9\\n2\\n7\\n", "3\\n0\\n", "2 appears three times; 7 is absent."),
        contest_test("all same", "5 1\\n4 4 4 4 4\\n4\\n", "5\\n", "Every element equals the query."),
        contest_test("edges", "4 2\\n1 2 3 4\\n1\\n4\\n", "1\\n1\\n", "First and last elements."),
        contest_test("big queries", "3 2\\n-5 -5 0\\n-5\\n1\\n", "2\\n0\\n", "Negative values count too."),
    ],
    level="imitation",
)
B2 = challenge(
    "hsg-p7-closest",
    "Closest Value",
    """**Description:** Given a sorted array of n integers and q queries, for
each query x print the array value closest to x. If two values are
equally close, print the **smaller** one.

**Input:** Line 1: n q (1 <= n, q <= 10^5). Line 2: n distinct sorted
integers (|a_i| <= 10^9). Next q lines: x (|x| <= 10^9).
**Output:** q lines — the closest value.

**Example:** `4 2` / `1 4 8 12` / `5` / `10` -> `4`, `8`
(5 is 1 away from 4 and 3 from 8 -> 4; 10 ties 8 and 12 -> smaller, 8).""",
    [
        contest_test("sample", "4 2\\n1 4 8 12\\n5\\n10\\n", "4\\n8\\n", "5 ties 4 vs 8 -> smaller (4); 10 is closer to 8."),
        contest_test("below all", "3 1\\n10 20 30\\n1\\n", "10\\n", "Everything is above; nearest is the first."),
        contest_test("above all", "3 1\\n10 20 30\\n99\\n", "30\\n", "Everything is below; nearest is the last."),
        contest_test("exact hit", "4 1\\n2 6 7 20\\n7\\n", "7\\n", "Distance 0 wins outright."),
    ],
    level="guided",
    difficulty="intermediate",
)
B3 = challenge(
    "hsg-p7-cows",
    "Aggressive Cows (Beginner)",
    """**Description:** Given n stall positions on a line and k cows, place all
cows in distinct stalls so the minimum distance between any two cows is
as large as possible. Print that distance.

**Input:** Line 1: n k (2 <= k <= n <= 10^5). Line 2: n distinct
positions (0 <= p_i <= 10^9).
**Output:** One integer — the largest achievable minimum distance.

**Example:** `5 3` / `1 2 8 4 9` -> `3` (place at 1, 4, 8 or 1, 4, 9).""",
    [
        contest_test("sample", "5 3\\n1 2 8 4 9\\n", "3\\n", "1, 4, 8 gives min gap 3."),
        contest_test("two cows", "2 2\\n0 1000000000\\n", "1000000000\\n", "Max separation — int would overflow at 2·10^9? no, but keep long long."),
        contest_test("crowded", "4 4\\n1 2 3 4\\n", "1\\n", "All stalls used; adjacent gaps are 1."),
        contest_test("sparse", "3 2\\n0 5 10\\n", "10\\n", "Two cows at the extremes."),
    ],
    level="guided",
    difficulty="intermediate",
)
B4 = challenge(
    "hsg-p7-router",
    "Maximum Segment Sum Limit",
    """**Description:** Split an array of n non-negative values into k
consecutive segments so that the **largest segment sum** is as small as
possible. Print that sum.

**Input:** Line 1: n k (1 <= k <= n <= 10^5). Line 2: n values
(0 <= a_i <= 10^4).
**Output:** One integer — the minimal possible maximum segment sum.

**Example:** `5 2` / `1 2 3 4 5` -> `9` (segments [1 2 3] and [4 5]).""",
    [
        contest_test("sample", "5 2\\n1 2 3 4 5\\n", "9\\n", "Split after 3: sums 6 and 9."),
        contest_test("one segment", "4 1\\n3 1 4 1\\n", "9\\n", "k = 1 forces the whole array."),
        contest_test("each own", "5 5\\n2 2 2 2 2\\n", "2\\n", "k = n: every segment is a single element."),
        contest_test("zeros", "3 2\\n0 0 5\\n", "5\\n", "Zeros pad any segment."),
    ],
    level="combination",
    difficulty="intermediate",
)
B5 = challenge(
    "hsg-p7-sub-sum",
    "Subarray With Sum",
    """**Description:** Given a sorted (non-decreasing) array of n positive
integers and a target s, print `YES` if some **contiguous** subarray
sums to exactly s, else `NO`.

**Input:** Line 1: n s (1 <= n <= 10^5, 1 <= s <= 10^14). Line 2: n
sorted positive integers (1 <= a_i <= 10^9).
**Output:** `YES` or `NO`.

**Example:** `5 9` / `1 2 3 4 9` -> `YES` (2+3+4).""",
    [
        contest_test("sample", "5 9\\n1 2 3 4 9\\n", "YES\\n", "2+3+4 = 9."),
        contest_test("single element", "1 7\\n7\\n", "YES\\n", "The element itself."),
        contest_test("impossible", "4 20\\n1 2 3 4\\n", "NO\\n", "Total is 10 < 20."),
        contest_test("whole array", "3 6\\n1 2 3\\n", "YES\\n", "The full array sums to s."),
    ],
    level="independent",
    difficulty="intermediate",
)

write_practice(
    M, "hsg-p7-search", "Search Set", "Five search problems: occurrence counting, closest value, aggressive cows, segment-sum minimization, and subarray sum verification.",
    "Bộ đề tìm kiếm", "Năm bài tìm kiếm: đếm lần xuất hiện, giá trị gần nhất, aggressive cows, cực tiểu tổng đoạn lớn nhất, và kiểm tra đoạn con có tổng s.",
    "hsg-m7-answer", 70, "beginner",
    [B1, B2, B3, B4, B5],
    {
        "hsg-p7-count-x": vi_challenge("Đếm lần xuất hiện", "**Mô tả:** Cho mảng n số nguyên đã sắp không giảm và q truy vấn, với mỗi giá trị x in số lần x xuất hiện trong mảng." + NL + NL + "**Dữ liệu vào:** Dòng 1: n q (1 <= n, q <= 10^5). Dòng 2: n số đã sắp (|a_i| <= 10^9). q dòng: x." + NL + "**Dữ liệu ra:** q dòng — số lần xuất hiện (0 nếu vắng)." + NL + NL + "**Ví dụ:** `6 2` / `1 2 2 2 5 9` / `2` / `7` -> `3`, `0`.", [("ví dụ đề bài", "2 xuất hiện ba lần; 7 vắng mặt."), ("toàn giống", "Mọi phần tử bằng truy vấn."), ("hai đầu", "Phần tử đầu và cuối."), ("âm", "Giá trị âm cũng được đếm.")]),
        "hsg-p7-closest": vi_challenge("Giá trị gần nhất", "**Mô tả:** Cho mảng n số nguyên **phân biệt** đã sắp và q truy vấn, với mỗi x in giá trị trong mảng gần x nhất. Nếu hai giá trị gần bằng nhau, in giá trị **nhỏ hơn**." + NL + NL + "**Dữ liệu vào:** Dòng 1: n q. Dòng 2: n số phân biệt đã sắp (|a_i| <= 10^9). q dòng: x." + NL + "**Dữ liệu ra:** q dòng — giá trị gần nhất." + NL + NL + "**Ví dụ:** `4 2` / `1 4 8 12` / `5` / `10` -> `4`, `8`.", [("ví dụ đề bài", "5 cách 4 một đơn vị, cách 8 ba đơn vị -> 4; 10 hòa 8 với 12 -> chọn nhỏ (8)."), ("nhỏ hơn tất cả", "Mọi phần tử ở trên; gần nhất là phần tử đầu."), ("lớn hơn tất cả", "Mọi phần tử ở dưới; gần nhất là phần tử cuối."), ("trúng đích", "Khoảng cách 0 thắng tuyệt đối.")]),
        "hsg-p7-cows": vi_challenge("Aggressive Cows (cơ bản)", "**Mô tả:** Cho n vị trí chuồng trên đường thẳng và k con bò, đặt mọi con bò vào các chuồng khác nhau sao cho khoảng cách nhỏ nhất giữa hai con bò càng lớn càng tốt. In khoảng cách đó." + NL + NL + "**Dữ liệu vào:** Dòng 1: n k (2 <= k <= n <= 10^5). Dòng 2: n vị trí phân biệt (0 <= p_i <= 10^9)." + NL + "**Dữ liệu ra:** Một số nguyên — khoảng cách tối thiểu lớn nhất đạt được." + NL + NL + "**Ví dụ:** `5 3` / `1 2 8 4 9` -> `3` (đặt 1, 4, 8).", [("ví dụ đề bài", "1, 4, 8 cho khoảng cách nhỏ nhất 3."), ("hai con", "Tách xa tối đa — nhớ long long."), ("chật chội", "Dùng hết chuồng; khoảng cách kề nhau là 1."), ("thưa", "Hai con ở hai đầu cực.")]),
        "hsg-p7-router": vi_challenge("Cực tiểu tổng đoạn lớn nhất", "**Mô tả:** Chia mảng n giá trị không âm thành k đoạn liên tiếp sao cho **tổng đoạn lớn nhất** nhỏ nhất có thể. In tổng đó." + NL + NL + "**Dữ liệu vào:** Dòng 1: n k (1 <= k <= n <= 10^5). Dòng 2: n giá trị (0 <= a_i <= 10^4)." + NL + "**Dữ liệu ra:** Một số nguyên — tổng đoạn lớn nhất nhỏ nhất." + NL + NL + "**Ví dụ:** `5 2` / `1 2 3 4 5` -> `9` (đoạn [1 2 3] và [4 5]).", [("ví dụ đề bài", "Cắt sau 3: tổng 6 và 9."), ("một đoạn", "k = 1 ép cả mảng thành một đoạn."), ("từng phần", "k = n: mỗi đoạn một phần tử."), ("có số không", "Số 0 lấp đầy đoạn nào cũng được.")]),
        "hsg-p7-sub-sum": vi_challenge("Đoạn con có tổng s", "**Mô tả:** Cho mảng đã sắp không giảm gồm n số nguyên dương và đích s, in `YES` nếu tồn tại **đoạn liên tiếp** có tổng đúng s, ngược lại `NO`." + NL + NL + "**Dữ liệu vào:** Dòng 1: n s (1 <= n <= 10^5, 1 <= s <= 10^14). Dòng 2: n số dương đã sắp (1 <= a_i <= 10^9)." + NL + "**Dữ liệu ra:** `YES` hoặc `NO`." + NL + NL + "**Ví dụ:** `5 9` / `1 2 3 4 9` -> `YES` (2+3+4).", [("ví dụ đề bài", "2+3+4 = 9."), ("một phần tử", "Chính phần tử đó."), ("không thể", "Tổng cả mảng là 10 < 20."), ("cả mảng", "Toàn bộ mảng ra đúng s.")]),
    },
    solutions=[
        ("hsg-p7-count-x",
         CPP_STD + '    int n, q; in >> n >> q;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    while (q--) {\n        long long x; in >> x;\n        int lb = int(lower_bound(a.begin(), a.end(), x) - a.begin());\n        int ub = int(upper_bound(a.begin(), a.end(), x) - a.begin());\n        out << ub - lb << "\\n";\n    }\n}'),
        ("hsg-p7-closest",
         CPP_STD + '    int n, q; in >> n >> q;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    while (q--) {\n        long long x; in >> x;\n        int lb = int(lower_bound(a.begin(), a.end(), x) - a.begin());\n        long long best;\n        if (lb == n) best = a[n-1];\n        else if (lb == 0) best = a[0];\n        else {\n            long long hi = a[lb], lo = a[lb-1];\n            long long dh = hi - x, dl = x - lo;\n            best = (dh < dl) ? hi : lo;   // tie -> smaller (lo)\n        }\n        out << best << "\\n";\n    }\n}'),
        ("hsg-p7-cows",
         CPP_STD + '    int n, k; in >> n >> k;\n    vector<long long> p(n);\n    for (long long& x : p) in >> x;\n    sort(p.begin(), p.end());\n    long long lo = 1, hi = p[n-1] - p[0];\n    auto feasible = [&](long long d) {\n        int used = 1; long long last = p[0];\n        for (int i = 1; i < n; ++i)\n            if (p[i] - last >= d) { ++used; last = p[i]; }\n        return used >= k;\n    };\n    while (lo < hi) {\n        long long mid = lo + (hi - lo + 1) / 2;\n        if (feasible(mid)) lo = mid; else hi = mid - 1;\n    }\n    out << lo << "\\n";\n}'),
        ("hsg-p7-router",
         CPP_STD + '    int n, k; in >> n >> k;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    long long lo = *max_element(a.begin(), a.end()), hi = 0;\n    for (long long x : a) hi += x;\n    auto feasible = [&](long long cap) {\n        int segs = 1; long long cur = 0;\n        for (long long x : a) {\n            if (cur + x > cap) { ++segs; cur = x; }\n            else cur += x;\n        }\n        return segs <= k;\n    };\n    while (lo < hi) {\n        long long mid = lo + (hi - lo) / 2;\n        if (feasible(mid)) hi = mid; else lo = mid + 1;\n    }\n    out << lo << "\\n";\n}'),
        ("hsg-p7-sub-sum",
         CPP_STD + '    int n; long long s; in >> n >> s;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    // two pointers over sorted positive values: window sum == s?\n    long long cur = 0; int l = 0;\n    bool ok = false;\n    for (int r = 0; r < n && !ok; ++r) {\n        cur += a[r];\n        while (l <= r && cur > s) { cur -= a[l]; ++l; }\n        if (cur == s) ok = true;\n    }\n    out << (ok ? "YES" : "NO") << "\\n";\n}'),
    ],
)
write_checkpoint(
    M, "hsg-cp-m7", "Checkpoint — Search", "Pass the graded problem to finish the search module.", 15,
    "**Checkpoint — search.** Pass the graded challenge below to finish the module.",
    "Checkpoint — tìm kiếm", "Vượt qua bài chấm cuối module để hoàn thành phần tìm kiếm.",
    "**Checkpoint — tìm kiếm.** Vượt qua challenge có chấm bên dưới để hoàn thành module.",
    challenge(
        "hsg-cp-m7-climb", "Plank the Trail", "**Description:** A trail has n checkpoints with heights h_1..h_n. Between checkpoint i-1 and i the climbers face an upward step of max(0, h_i - h_{i-1}). You may install wooden planks: one plank reduces the upward step along one gap by 1 (any number per gap). With at most k planks, minimize the **largest remaining upward step**. Print that step.\n\n**Input:** Line 1: n k (2 <= n <= 10^5, 0 <= k <= 10^14). Line 2: n heights (0 <= h_i <= 10^9).\n**Output:** One integer.\n\n**Example:** `4 2` / `1 5 5 9` -> up-steps 4, 0, 4; two planks on one gap leave 2 -> `2`.",
        [contest_test("sample", "4 2\\n1 5 5 9\\n", "2\\n", "Up-steps 4, 0, 4; 2 planks on a 4-step gap leave 2."), contest_test("no planks", "3 0\\n1 3 2\\n", "2\\n", "k = 0: the max up-step stays 2."), contest_test("flatten", "3 100\\n1 10 5\\n", "0\\n", "Plenty of planks: the 9-step gap is erased entirely."), contest_test("single gap", "2 3\\n0 7\\n", "4\\n", "One gap of 7 with 3 planks leaves 4.")],
        difficulty="intermediate",
    ),
    vi_challenge("Lắp ván cho đường leo", "**Mô tả:** Đường trail có n điểm cao h_1..h_n. Giữa điểm i-1 và i người leo phải bậc lên max(0, h_i - h_{i-1}). Mỗi ván gỗ giảm bậc lên của một khoảng đi 1 (mỗi khoảng bao nhiêu ván cũng được). Với tối đa k ván, cực tiểu **bậc lên lớn nhất còn lại**. In giá trị đó.\n\n**Dữ liệu vào:** Dòng 1: n k (2 <= n <= 10^5, 0 <= k <= 10^14). Dòng 2: n chiều cao.\n**Dữ liệu ra:** Một số nguyên.\n\n**Ví dụ:** `4 2` / `1 5 5 9` -> các bậc lên 4, 0, 4; hai ván vào khoảng 4 bậc còn 2 -> `2`.", [("ví dụ đề bài", "Bậc lên 4, 0, 4; 2 ván vào khoảng 4 bậc còn 2."), ("không ván", "k = 0: bậc lên lớn nhất giữ nguyên 2."), ("san phẳng", "Ván dư dùng: khoảng 9 bậc bị xóa hẳn."), ("một khoảng", "Một khoảng 7 bậc với 3 ván còn 4.")]),
    solution="#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long k; in >> n >> k;\n    vector<long long> h(n);\n    for (long long& x : h) in >> x;\n    // feasible(d): keep every up-step <= d using k planks; a gap with\n    // up-step u needs max(0, u - d) planks\n    auto feasible = [&](long long d) {\n        long long need = 0;\n        for (int i = 1; i < n; ++i)\n            if (h[i] - h[i-1] > d) need += h[i] - h[i-1] - d;\n        return need <= k;\n    };\n    long long lo = 0, hi = 0;\n    for (int i = 1; i < n; ++i) hi = max(hi, h[i] - h[i-1]);\n    while (lo < hi) {\n        long long mid = lo + (hi - lo) / 2;\n        if (feasible(mid)) hi = mid; else lo = mid + 1;\n    }\n    out << lo << \"\\n\";\n}",
    wrong="#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long k; in >> n >> k;\n    vector<long long> h(n);\n    for (long long& x : h) in >> x;\n    // near-miss: counts how many GAPS exceed d, not how many PLANKS\n    // are needed — a gap 5 above the limit needs 5 planks, not 1,\n    // so this undercounts and accepts too-large d\n    auto feasible = [&](long long d) {\n        long long bad = 0;\n        for (int i = 1; i < n; ++i)\n            if (h[i] - h[i-1] > d) ++bad;\n        return bad <= k;\n    };\n    long long lo = 0, hi = 0;\n    for (int i = 1; i < n; ++i) hi = max(hi, h[i] - h[i-1]);\n    while (lo < hi) {\n        long long mid = lo + (hi - lo) / 2;\n        if (feasible(mid)) hi = mid; else lo = mid + 1;\n    }\n    out << lo << \"\\n\";\n}",
)

print("M7 done")
