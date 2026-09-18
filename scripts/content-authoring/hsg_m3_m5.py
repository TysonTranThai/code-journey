#!/usr/bin/env python3
"""HSG — Modules 3-5: hsg-arrays, hsg-marking, hsg-greedy."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

# ================================================================ M3 ARRAYS
M = "hsg-arrays"
write_module(
    M, "Arrays", "Indexing, traversal, min/max, counting, reverse and rotate — the array mechanics behind half of all easy HSG problems.",
    "Mảng", "Chỉ số, duyệt, min/max, đếm, đảo và xoay — cơ chế mảng đứng sau một nửa bài HSG dễ.",
    ["hsg-m3-basics", "hsg-m3-classic", "hsg-cp-m3"], ["hsg-p3-arrays"],
)
write_lesson(
    M, "hsg-m3-basics",
    "Array Mechanics",
    "Declaration, indexing from 0, traversal, and the bounds rule that prevents runtime errors.",
    11,
    """## Declaration and indexing

```cpp
int n; in >> n;
vector<long long> a(n);          // indices 0 .. n-1
for (long long& x : a) in >> x;
```

Indices run **0 to n-1**. Accessing `a[n]` is undefined behavior — the
#1 cause of Runtime Error. When a problem says "the i-th element" with
1-based counting, translate: element i lives at `a[i-1]`.

### Traversal styles

```cpp
for (int i = 0; i < n; ++i) ...     // when you need the index
for (long long x : a) ...           // values only
for (int i = n - 1; i >= 0; --i)    // backwards
```

### min/max with a running best

```cpp
long long best = a[0];              // NOT 0 — values may be negative!
for (long long x : a) best = max(best, x);
```

Initializing `best = 0` fails the moment all values are negative. Start
from the first element (or -infinity).

### Reverse and rotate

```cpp
reverse(a.begin(), a.end());                    // in place
rotate(a.begin(), a.begin() + k, a.end());      // left-rotate by k
```""",
    "Cơ chế mảng", "Khai báo, chỉ số từ 0, duyệt, và quy tắc biên chống runtime error.",
    """## Khai báo và chỉ số

```cpp
int n; in >> n;
vector<long long> a(n);          // chỉ số 0 .. n-1
for (long long& x : a) in >> x;
```

Chỉ số chạy **từ 0 đến n-1**. Truy cập `a[n]` là hành vi không xác định —
nguyên nhân Runtime Error số một. Khi đề nói "phần tử thứ i" (đếm từ 1),
dịch sang chỉ số: phần tử i nằm ở `a[i-1]`.

### Các kiểu duyệt

```cpp
for (int i = 0; i < n; ++i) ...     // cần chỉ số
for (long long x : a) ...           // chỉ giá trị
for (int i = n - 1; i >= 0; --i)    // duyệt ngược
```

### min/max với biến giữ kỷ lục

```cpp
long long best = a[0];              // KHÔNG phải 0 — giá trị có thể âm!
for (long long x : a) best = max(best, x);
```

Khởi tạo `best = 0` sai ngay khi mọi giá trị đều âm. Hãy bắt đầu từ phần
tử đầu tiên (hoặc -infinity).

### Đảo và xoay

```cpp
reverse(a.begin(), a.end());                    // tại chỗ
rotate(a.begin(), a.begin() + k, a.end());      // xoay trái k bước
``""",
)
write_lesson(
    M, "hsg-m3-classic",
    "The Classic Array Problems",
    "Count elements above a threshold, second maximum, remove duplicates from a sorted array, and the two-pointer reverse.",
    12,
    """## Five problems, five transferable tricks

### Count above threshold — O(n), one pass

```cpp
int cnt = 0;
for (long long x : a) if (x > t) ++cnt;
```

### Second maximum — track two values

```cpp
long long best = LLONG_MIN, second = LLONG_MIN;
for (long long x : a) {
    if (x > best) { second = best; best = x; }
    else if (x > second && x != best) second = x;
}
```

The order matters: promote before comparing the newcomer to `second`.
Duplicates make `x != best` necessary.

### Unique-in-sorted — the write pointer

For a **sorted** array, keep unique values in place with a write index:

```cpp
sort(a.begin(), a.end());
int w = 0;
for (int i = 0; i < n; ++i)
    if (i == 0 || a[i] != a[w - 1]) a[w++] = a[i];
// a[0 .. w-1] are the unique values; w = distinct count
```

This is the in-place core of many "count distinct" answers (module 4
shows the marking alternative).

### Two-pointer reverse

```cpp
for (int i = 0, j = n - 1; i < j; ++i, --j) swap(a[i], a[j]);
```

Two indices closing in — the pattern returns in module 17.

### Prefix max — the running champion

`pre[i] = max(pre[i-1], a[i])` — a one-line loop that becomes a building
block for many harder problems.""",
    "Các bài mảng kinh điển", "Đếm vượt ngưỡng, max thứ hai, loại trùng trong mảng đã sắp, và đảo hai con trỏ.",
    """## Năm bài, năm thủ thuật chuyển giao được

### Đếm vượt ngưỡng — O(n), một lượt

```cpp
int cnt = 0;
for (long long x : a) if (x > t) ++cnt;
```

### Max thứ hai — theo dõi hai giá trị

```cpp
long long best = LLONG_MIN, second = LLONG_MIN;
for (long long x : a) {
    if (x > best) { second = best; best = x; }
    else if (x > second && x != best) second = x;
}
```

Thứ tự quan trọng: thăng hạng trước, rồi mới so với `second`. Trùng giá
trị khiến `x != best` cần thiết.

### Loại trùng trong mảng đã sắp — con trỏ ghi

Với mảng **đã sắp**, giữ giá trị duy nhất tại chỗ bằng chỉ số ghi:

```cpp
sort(a.begin(), a.end());
int w = 0;
for (int i = 0; i < n; ++i)
    if (i == 0 || a[i] != a[w - 1]) a[w++] = a[i];
// a[0 .. w-1] là các giá trị duy nhất; w = số phần tử khác nhau
```

Đây là lõi "đếm phân biệt" tại chỗ (module sau có cách mảng đánh dấu).

### Đảo bằng hai con trỏ

```cpp
for (int i = 0, j = n - 1; i < j; ++i, --j) swap(a[i], a[j]);
```

Hai chỉ số tiến vào nhau — mẫu hình này quay lại ở module hai con trỏ.

### Prefix max — nhà vô địch đang chạy

`pre[i] = max(pre[i-1], a[i])` — một dòng lặp trở thành viên gạch cho
nhiều bài khó hơn.""",
)

A1 = challenge(
    "hsg-p3-threshold",
    "Above the Threshold",
    """**Description:** Given n numbers and a threshold t, print how many
numbers are strictly greater than t.

**Input:** Line 1: n t (1 ≤ n ≤ 10^5, −10^9 ≤ t ≤ 10^9). Line 2: n numbers.
**Output:** One integer.

**Example:** `5 3` / `1 4 3 7 2` → `2` (4 and 7).""",
    [
        contest_test("sample", "5 3\n1 4 3 7 2\n", "2\n", "4 and 7 exceed 3; 3 itself does not (strictly greater)."),
        contest_test("all above", "3 0\n5 5 5\n", "3\n", "Every 5 > 0."),
        contest_test("none above", "3 10\n1 2 3\n", "0\n", "Nothing exceeds 10."),
        contest_test("boundary equal", "2 5\n5 6\n", "1\n", "Equal to t does not count."),
    ],
    level="imitation",
)
A2 = challenge(
    "hsg-p3-second-max",
    "Second Maximum",
    """**Description:** Print the second largest **distinct** value in an array.

**Input:** Line 1: n (2 ≤ n ≤ 10^5). Line 2: n numbers (−10^9 ≤ each ≤ 10^9).
**Output:** One integer, or `NONE` if all values are equal.

**Example:** `4` / `3 7 7 5` → `5` (7 is largest; 5 is second distinct).""",
    [
        contest_test("sample", "4\n3 7 7 5\n", "5\n", "Largest distinct is 7, second is 5."),
        contest_test("all equal", "3\n2 2 2\n", "NONE\n", "No second distinct value exists."),
        contest_test("negatives", "4\n-1 -5 -1 -3\n", "-3\n", "Works with negatives: -1 then -3."),
        contest_test("two values", "2\n9 4\n", "4\n", "With two distinct values the smaller is second."),
    ],
    level="guided",
    difficulty="intermediate",
)
A3 = challenge(
    "hsg-p3-count-distinct",
    "Count Distinct Values",
    """**Description:** Given n numbers, print how many **distinct** values appear.

**Input:** Line 1: n (1 ≤ n ≤ 10^5). Line 2: n integers (−10^9 ≤ each ≤ 10^9).
**Output:** One integer.

**Example:** `6` / `2 7 2 9 7 2` → `3` (values 2, 7, 9).

*Hint:* sort, then count positions where `a[i] != a[i-1]`.""",
    [
        contest_test("sample", "6\n2 7 2 9 7 2\n", "3\n", "Distinct values are 2, 7, 9."),
        contest_test("all same", "4\n5 5 5 5\n", "1\n", "One distinct value."),
        contest_test("all distinct", "3\n1 2 3\n", "3\n", "Nothing repeats."),
        contest_test("single", "1\n42\n", "1\n", "One element → one distinct value."),
    ],
    level="guided",
)
A4 = challenge(
    "hsg-p3-rotate",
    "Rotate Left",
    """**Description:** Given n numbers and k, rotate the array left by k
positions and print it. Values may wrap multiple times (k can exceed n).

**Input:** Line 1: n k (1 ≤ n ≤ 10^5, 0 ≤ k ≤ 10^9). Line 2: n numbers.
**Output:** The rotated array, space-separated.

**Example:** `5 2` / `1 2 3 4 5` → `3 4 5 1 2`.""",
    [
        contest_test("sample", "5 2\n1 2 3 4 5\n", "3 4 5 1 2\n", "Left by 2: start at index 2."),
        contest_test("k zero", "3 0\n7 8 9\n", "7 8 9\n", "No rotation."),
        contest_test("k equals n", "3 3\n7 8 9\n", "7 8 9\n", "Rotating by n is the identity."),
        contest_test("k huge", "3 1000000000\n7 8 9\n", "8 9 7\n", "10^9 mod 3 = 1 → left-rotate by 1 → 8 9 7."),
    ],
    level="independent",
    difficulty="intermediate",
)
A5 = challenge(
    "hsg-p3-max-k-sum",
    "Maximum k-Sum Window",
    """**Description:** Given n numbers, find the maximum sum of any k **consecutive**
numbers (a fixed window, not any subset).

**Input:** Line 1: n k (1 ≤ k ≤ n ≤ 10^5). Line 2: n numbers (−10^9..10^9).
**Output:** One integer.

**Example:** `5 2` / `3 -1 4 2 0` → `6` (window 4+2).

*Note:* an O(n·k) double loop passes only small n here — but the sliding
sum (add the new element, drop the old) is O(n). Try both; one times out
at n = 10^5.""",
    [
        contest_test("sample", "5 2\n3 -1 4 2 0\n", "6\n", "The best 2-window is 4+2 = 6."),
        contest_test("k equals n", "3 3\n1 2 3\n", "6\n", "Whole array: 1+2+3."),
        contest_test("all negative", "4 2\n-5 -2 -9 -1\n", "-7\n", "Best 2-window is -5 + -2 = -7 — must allow negative sums."),
        contest_test("k one", "4 1\n-3 8 -6 2\n", "8\n", "Single best element."),
        contest_test("large window", "100000 50000\n" + " ".join(["1"] * 100000) + "\n", "50000\n", "n = 10^5 with k = 5·10^4 — the sliding sum answers instantly; an O(n·k) double loop cannot finish."),
    ],
    level="combination",
    difficulty="intermediate",
)

write_practice(
    M, "hsg-p3-arrays", "Array Mechanics Set", "Five array problems: threshold counting, second maximum, distinct counting, rotation, and the sliding window preview.",
    "Bộ đề mảng", "Năm bài mảng: đếm ngưỡng, max thứ hai, đếm phân biệt, xoay, và nhìn trước cửa sổ trượt.",
    "hsg-m3-classic", 65, "beginner",
    [A1, A2, A3, A4, A5],
    {
        "hsg-p3-threshold": vi_challenge("Vượt ngưỡng", "**Mô tả:** Cho n số và ngưỡng t, in bao nhiêu số lớn hơn t.\n\n**Dữ liệu vào:** Dòng 1: n t. Dòng 2: n số.\n**Dữ liệu ra:** Một số nguyên.\n\n**Ví dụ:** `5 3` / `1 4 3 7 2` → `2`.", [("ví dụ đề bài", "4 và 7 vượt 3; chính 3 thì không (lớn hơn hoàn toàn)."), ("tất cả vượt", "Mọi số 5 > 0."), ("không ai vượt", "Không số nào vượt 10."), ("biên bằng", "Bằng t không được đếm.")]),
        "hsg-p3-second-max": vi_challenge("Max thứ hai", "**Mô tả:** In giá trị lớn thứ hai **khác nhau** trong mảng.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n số.\n**Dữ liệu ra:** Một số nguyên, hoặc `NONE` nếu mọi giá trị bằng nhau.\n\n**Ví dụ:** `4` / `3 7 7 5` → `5`.", [("ví dụ đề bài", "Lớn nhất là 7, nhì là 5."), ("tất cả bằng", "Không có giá trị khác nhau thứ hai."), ("số âm", "Với số âm: -1 rồi -3."), ("hai giá trị", "Hai giá trị khác nhau thì số nhỏ là nhì.")]),
        "hsg-p3-count-distinct": vi_challenge("Đếm giá trị phân biệt", "**Mô tả:** Cho n số, in bao nhiêu **giá trị khác nhau** xuất hiện.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n số.\n**Dữ liệu ra:** Một số nguyên.\n\n**Ví dụ:** `6` / `2 7 2 9 7 2` → `3`.\n\n*Gợi ý:* sắp xếp rồi đếm vị trí `a[i] != a[i-1]`.", [("ví dụ đề bài", "Giá trị phân biệt: 2, 7, 9."), ("tất cả giống", "Một giá trị phân biệt."), ("không trùng", "Không gì lặp lại."), ("một phần tử", "Một phần tử → một giá trị.")]),
        "hsg-p3-rotate": vi_challenge("Xoay trái", "**Mô tả:** Cho n số và k, xoay mảng sang trái k vị trí rồi in. k có thể lớn hơn n.\n\n**Dữ liệu vào:** Dòng 1: n k. Dòng 2: n số.\n**Dữ liệu ra:** Mảng sau xoay, cách nhau dấu cách.\n\n**Ví dụ:** `5 2` / `1 2 3 4 5` → `3 4 5 1 2`.", [("ví dụ đề bài", "Trái 2 bước: bắt đầu từ chỉ số 2."), ("k bằng 0", "Không xoay."), ("k bằng n", "Xoay n bước là như cũ."), ("k lớn", "k mod 3 = 1 → kết quả phải là 8 9 7.")]),
        "hsg-p3-max-k-sum": vi_challenge("Tổng cửa sổ k lớn nhất", "**Mô tả:** Cho n số, tìm tổng lớn nhất của k số **liên tiếp** bất kỳ (cửa sổ cố định, không phải tập con bất kỳ).\n\n**Dữ liệu vào:** Dòng 1: n k. Dòng 2: n số.\n**Dữ liệu ra:** Một số nguyên.\n\n**Ví dụ:** `5 2` / `3 -1 4 2 0` → `6` (cửa sổ 4+2).\n\n*Lưu ý:* vòng kép O(n·k) chỉ qua được n nhỏ — cửa sổ trượt (cộng phần tử mới, trừ phần tử cũ) là O(n). n = 10^5 sẽ phơi nhiễm vòng kép.", [("ví dụ đề bài", "Cửa sổ 2 tốt nhất là 4+2 = 6."), ("k bằng n", "Cả mảng: 1+2+3."), ("toàn âm", "Cửa sổ tốt nhất là -2 + -1 = -3 — tổng âm phải được chấp nhận."), ("k một", "Phần tử tốt nhất.")]),
    },
    solutions=[
        ("hsg-p3-threshold",
         "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long t; in >> n >> t;\n    int cnt = 0;\n    for (int i = 0; i < n; ++i) { long long x; in >> x; if (x > t) ++cnt; }\n    out << cnt << \"\\n\";\n}",
         "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long t; in >> n >> t;\n    // near-miss: counts >= t instead of > t\n    int cnt = 0;\n    for (int i = 0; i < n; ++i) { long long x; in >> x; if (x >= t) ++cnt; }\n    out << cnt << \"\\n\";\n}"),
        ("hsg-p3-second-max",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    long long best = LLONG_MIN, second = LLONG_MIN;\n    for (int i = 0; i < n; ++i) {\n        long long x; in >> x;\n        if (x > best) { second = best; best = x; }\n        else if (x > second && x != best) second = x;\n    }\n    if (second == LLONG_MIN) out << \"NONE\\n\";\n    else out << second << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    long long best = LLONG_MIN, second = LLONG_MIN;\n    // near-miss: forgets the x != best guard, so duplicates of the max\n    // get reported as the second maximum\n    for (int i = 0; i < n; ++i) {\n        long long x; in >> x;\n        if (x > best) { second = best; best = x; }\n        else if (x > second) second = x;\n    }\n    if (second == LLONG_MIN) out << \"NONE\\n\";\n    else out << second << \"\\n\";\n}"),
        ("hsg-p3-count-distinct",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    sort(a.begin(), a.end());\n    int cnt = 1;\n    for (int i = 1; i < n; ++i) if (a[i] != a[i - 1]) ++cnt;\n    out << cnt << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    sort(a.begin(), a.end());\n    // near-miss: counts equal neighbors instead of distinct starts\n    int cnt = 1;\n    for (int i = 1; i < n; ++i) if (a[i] == a[i - 1]) ++cnt;\n    out << cnt << \"\\n\";\n}"),
        ("hsg-p3-rotate",
         "#include <iostream>\n#include <vector>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long k; in >> n >> k;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    k %= n;\n    for (int i = 0; i < n; ++i) {\n        out << a[(i + k) % n];\n        out << (i + 1 < n ? ' ' : '\\n');\n    }\n}",
         "#include <iostream>\n#include <vector>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long k; in >> n >> k;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    // near-miss: rotates RIGHT instead of left\n    k %= n;\n    for (int i = 0; i < n; ++i) {\n        out << a[(i - k % n + n) % n];\n        out << (i + 1 < n ? ' ' : '\\n');\n    }\n}"),
        ("hsg-p3-max-k-sum",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n, k; in >> n >> k;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    long long sum = 0;\n    for (int i = 0; i < k; ++i) sum += a[i];\n    long long best = sum;\n    for (int i = k; i < n; ++i) {\n        sum += a[i] - a[i - k];\n        best = max(best, sum);\n    }\n    out << best << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n, k; in >> n >> k;\n    vector<long long> a(n);\n    for (long long& x : a) in >> x;\n    // near-miss: O(n*k) double loop — still CORRECT, but times out at\n    // the maximum n; kept as a teaching near-miss with wrong verdict\n    long long best = LLONG_MIN;\n    for (int i = 0; i + k <= n; ++i) {\n        long long s = 0;\n        for (int j = i; j < i + k; ++j) s += a[j];\n        best = max(best, s);\n    }\n    out << best << \"\\n\";\n}"),
    ],
)
write_checkpoint(
    M, "hsg-cp-m3", "Checkpoint — Arrays", "Pass the graded problem to finish the arrays module.", 15,
    "**Checkpoint — arrays.** Pass the graded challenge below to finish the module.",
    "Checkpoint — mảng", "Vượt qua bài chấm cuối module để hoàn thành phần mảng.",
    "**Checkpoint — mảng.** Vượt qua challenge có chấm bên dưới để hoàn thành module.",
    challenge(
        "hsg-cp-m3-equilibrium",
        "Equilibrium Index",
        """**Description:** Given n numbers, print the smallest index i (0-based)
such that the sum of elements before i equals the sum of elements after i.
If no such index exists, print `-1`.

**Input:** Line 1: n (1 ≤ n ≤ 10^5). Line 2: n numbers (−10^9..10^9).
**Output:** One integer.

**Example:** `4` / `1 7 3 6` → `1` (left of index 1: 1; right: 3+6=9? no —
1+7=8 vs 3+6=9... careful: left of index 1 is {1} sum 1, right is {3,6}
sum 9. Try index 2: left {1,7} = 8, right {6} = 6. None → `-1`. Use
`5` / `2 1 3 1 2`: index 2 → left {2,1}=3, right {1,2}=3 → `2`.)""",
        [
            contest_test("exists", "5\n2 1 3 1 2\n", "2\n", "Left {2,1} = 3, right {1,2} = 3."),
            contest_test("none", "4\n1 7 3 6\n", "-1\n", "No index balances: 1 vs 9, 8 vs 9, 11 vs 6, 14 vs 0."),
            contest_test("equals balance", "3\n5 5 5\n", "1\n", "Index 1: left {5} = 5, right {5} = 5."),
            contest_test("single", "1\n9\n", "0\n", "With one element both sides are empty: 0 = 0 at index 0."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge("Chỉ số cân bằng", "**Mô tả:** Cho n số, in chỉ số i nhỏ nhất (đánh từ 0) sao cho tổng phần tử trước i bằng tổng phần tử sau i. Không có thì in `-1`.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n số.\n**Dữ liệu ra:** Một số nguyên.\n\n**Ví dụ:** `5` / `2 1 3 1 2` → `2`.", [("có tồn tại", "Trái {2,1} = 3, phải {1,2} = 3."), ("không tồn tại", "Không chỉ số nào cân bằng."), ("cân ở đầu", "Tổng trái rỗng 0 = tổng phải 0 tại chỉ số 0."), ("một phần tử", "Với n = 1, hai phía đều rỗng và bằng nhau → 0.")]),
    solution="#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    long long a[200000], total = 0, left = 0;\n    for (int i = 0; i < n; ++i) { in >> a[i]; total += a[i]; }\n    for (int i = 0; i < n; ++i) {\n        long long right = total - left - a[i];\n        if (left == right) { out << i << \"\\n\"; return; }\n        left += a[i];\n    }\n    out << -1 << \"\\n\";\n}",
    wrong="#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    long long a[200000], total = 0, left = 0;\n    for (int i = 0; i < n; ++i) { in >> a[i]; total += a[i]; }\n    // near-miss: compares left to total - left (forgets to remove a[i]\n    // from the right side), so the pivot element counts on both sides\n    for (int i = 0; i < n; ++i) {\n        if (left == total - left) { out << i << \"\\n\"; return; }\n        left += a[i];\n    }\n    out << -1 << \"\\n\";\n}",
)

# ================================================================ M4 MARKING
M = "hsg-marking"
write_module(
    M, "Marking & Frequency Arrays", "The mảng đánh dấu technique: presence flags, frequency counting, and the value-range rule that decides when it is even possible.",
    "Mảng đánh dấu & đếm phân phối", "Kỹ thuật mảng đánh dấu: cờ hiện diện, đếm tần suất, và quy tắc miền giá trị quyết định khi nào dùng được.",
    ["hsg-m4-idea", "hsg-m4-range", "hsg-cp-m4"], ["hsg-p4-marking"],
)
write_lesson(
    M, "hsg-m4-idea",
    "The Marking Idea (mảng đánh dấu)",
    "Trade memory for speed: an array indexed by value turns repeated scanning into O(1) lookups.",
    12,
    """## One array, indexed by value

To check "did value v appear?", a linear scan costs O(n) per query. A
**marking array** answers in O(1):

```cpp
const int MAXV = 100000;
vector<bool> seen(MAXV + 1, false);
int x; in >> x;
seen[x] = true;                 // mark
if (seen[v]) ...                // O(1) lookup
```

### Frequency arrays (đếm phân phối)

```cpp
vector<int> freq(MAXV + 1, 0);
++freq[x];                      // x appeared once more
```

- Most frequent value: loop over `freq`, take the max.
- Duplicates: any `freq[v] > 1`.
- Missing value: any `freq[v] == 0` in a range.

### Worked example — do two arrays contain the same multiset?

```cpp
vector<int> f1(MAXV + 1, 0), f2(MAXV + 1, 0);
// increment f1 for a's elements, f2 for b's
bool same = true;
for (int v = 0; v <= MAXV && same; ++v) same = (f1[v] == f2[v]);
out << (same ? "SAME" : "DIFF") << "\\n";
```

Sorting both arrays and comparing also works (O(n log n)); marking is
O(n + MAXV). The technique costs memory — which is exactly the catch the
next lesson covers.""",
    "Ý tưởng mảng đánh dấu", "Đổi bộ nhớ lấy tốc độ: mảng đánh chỉ số theo giá trị biến việc quét lặp thành tra cứu O(1).",
    """## Một mảng, đánh chỉ số theo giá trị

Để trả lời "giá trị v có xuất hiện?", quét tuyến tính tốn O(n) mỗi truy
vấn. **Mảng đánh dấu** trả lời trong O(1):

```cpp
const int MAXV = 100000;
vector<bool> seen(MAXV + 1, false);
int x; in >> x;
seen[x] = true;                 // đánh dấu
if (seen[v]) ...                // tra cứu O(1)
```

### Mảng tần suất (đếm phân phối)

```cpp
vector<int> freq(MAXV + 1, 0);
++freq[x];                      // x xuất hiện thêm một lần
```

- Giá trị xuất hiện nhiều nhất: duyệt `freq`, lấy max.
- Phần tử trùng: bất kỳ `freq[v] > 1`.
- Giá trị thiếu: bất kỳ `freq[v] == 0` trong đoạn.

### Ví dụ làm mẫu — hai mảng có cùng đa tập không?

```cpp
vector<int> f1(MAXV + 1, 0), f2(MAXV + 1, 0);
// tăng f1 cho phần tử của a, f2 cho phần tử của b
bool same = true;
for (int v = 0; v <= MAXV && same; ++v) same = (f1[v] == f2[v]);
out << (same ? "SAME" : "DIFF") << "\\n";
```

Sắp xếp cả hai mảng rồi so sánh cũng được (O(n log n)); đánh dấu là
O(n + MAXV). Kỹ thuật này tốn bộ nhớ — và đó chính là cái bẫy ở bài sau.""",
)
write_lesson(
    M, "hsg-m4-range",
    "The Value-Range Rule",
    "Marking works only when values are small enough — how to read the constraint and pick the right structure.",
    11,
    """## Read the constraint before you mark

The marking array's size is the **value range**, not n:

- Values 0..10^6 → `vector<int> freq(1000001)` ≈ 4 MB. Fine (512 MB).
- Values 0..10^9 → an array of 10^9 ints ≈ 4 GB. **Impossible.**
- Values up to 10^18 → hopeless as an array.

**The rule:** the value range, not the element count, decides whether a
marking array is possible.

### When values are too large — sort or map

| Values | Structure |
| --- | --- |
| small range | marking / frequency array |
| big range, need counts | `sort` + runs, or `map<long long,int>` |
| need presence only, big range | `set<long long>` (module STL) |

```cpp
map<long long, int> freq;       // works for any value range
++freq[x];                      // O(log n) per op, but memory O(distinct)
```

### Memory arithmetic — a contest habit

`10^6` ints = 4 MB. `10^7` ints = 40 MB. `10^8` ints = 400 MB — at the
512 MB ceiling. Do this multiplication on scratch paper *before* coding.

### Two-value marking: bool vs int

`vector<bool>` packs bits (1 byte per bit in practice) — fine for presence.
For counts you need `vector<int>` (or `int` if counts can exceed 2^31 —
read the constraint).""",
    "Quy tắc miền giá trị", "Đánh dấu chỉ khả thi khi giá trị đủ nhỏ — đọc ràng buộc và chọn cấu trúc phù hợp.",
    """## Đọc ràng buộc trước khi đánh dấu

Kích thước mảng đánh dấu là **miền giá trị**, không phải n:

- Giá trị 0..10^6 → `vector<int> freq(1000001)` ≈ 4 MB. Ổn (512 MB).
- Giá trị 0..10^9 → mảng 10^9 int ≈ 4 GB. **Bất khả thi.**
- Giá trị tới 10^18 → không thể thành mảng.

**Quy tắc:** miền giá trị, chứ không phải số phần tử, quyết định mảng
đánh dấu có dùng được không.

### Khi giá trị quá lớn — sắp xếp hoặc map

| Giá trị | Cấu trúc |
| --- | --- |
| miền nhỏ | mảng đánh dấu / tần suất |
| miền lớn, cần đếm | `sort` + chạy đoạn, hoặc `map<long long,int>` |
| chỉ cần hiện diện, miền lớn | `set<long long>` (module STL) |

```cpp
map<long long, int> freq;       // dùng được cho mọi miền giá trị
++freq[x];                      // O(log n) mỗi phép, bộ nhớ O(số phân biệt)
```

### Phép tính bộ nhớ — thói quen thi đấu

`10^6` int = 4 MB. `10^7` int = 40 MB. `10^8` int = 400 MB — sát trần
512 MB. Nhân phép này trên giấy nháp *trước* khi code.

### Đánh dấu bool hay int?

`vector<bool>` đóng gói bit — đủ cho hiện diện. Cần đếm thì dùng
`vector<int>` (hoặc `long long` nếu số đếm có thể vượt 2^31 — đọc giới
hạn).""",
)

B1 = challenge(
    "hsg-p4-freq",
    "Most Frequent Value",
    """**Description:** Given n integers with values 0..10^6, print the value
that appears most often. If several tie, print the **smallest** such value.

**Input:** Line 1: n (1 ≤ n ≤ 10^5). Line 2: n integers (0 ≤ each ≤ 10^6).
**Output:** One integer.

**Example:** `5` / `2 3 2 3 1` → `2` (2 and 3 both appear twice; 2 is smaller).""",
    [
        contest_test("tie smallest", "5\n2 3 2 3 1\n", "2\n", "2 and 3 tie at 2 occurrences; smaller wins."),
        contest_test("clear winner", "4\n5 5 5 1\n", "5\n", "5 appears three times."),
        contest_test("single", "1\n999999\n", "999999\n", "One element at the top of the range."),
        contest_test("all distinct", "3\n1 2 3\n", "1\n", "All appear once; smallest wins."),
    ],
    level="imitation",
)
B2 = challenge(
    "hsg-p4-duplicates",
    "Find the Duplicate",
    """**Description:** Given n+1 integers, each in 1..n, exactly one value
appears twice and all others appear once. Print the duplicated value.

**Input:** Line 1: n (1 ≤ n ≤ 10^6). Line 2: n+1 integers (1 ≤ each ≤ n).
**Output:** One integer — the duplicated value.

**Example:** `4` / `1 3 4 2 3` → `3`.""",
    [
        contest_test("sample", "4\n1 3 4 2 3\n", "3\n", "3 appears twice."),
        contest_test("duplicate is one", "3\n1 2 1\n", "1\n", "1 repeats."),
        contest_test("large", "1000000\n" + " ".join(str(i) for i in range(1, 1000001)) + " 7\n", "7\n", "The duplicate 7 appended — linear scan must handle n = 10^6."),
        contest_test("two elements", "1\n1 1\n", "1\n", "Smallest case."),
    ],
    level="guided",
)
B3 = challenge(
    "hsg-p4-missing",
    "The Missing Number",
    """**Description:** The numbers 1..n should all be present, but exactly one
is missing. Print it.

**Input:** Line 1: n (2 ≤ n ≤ 10^6). Line 2: n−1 integers — the present ones.
**Output:** One integer — the missing number.

**Example:** `5` / `1 2 4 5` → `3`.

*Two solutions exist:* a marking array, or the sum trick
(missing = n(n+1)/2 − sum). Both are worth writing.""",
    [
        contest_test("sample", "5\n1 2 4 5\n", "3\n", "3 is absent from 1..5."),
        contest_test("missing first", "4\n2 3 4\n", "1\n", "1 is missing."),
        contest_test("missing last", "4\n1 2 3\n", "4\n", "4 is missing."),
        contest_test("large", "1000000\n" + " ".join(str(i) for i in range(1, 1000000)) + "\n", "1000000\n", "The last number is missing — watch the sum trick overflow with int."),
    ],
    level="guided",
)
B4 = challenge(
    "hsg-p4-multiset-eq",
    "Same Multiset?",
    """**Description:** Two bags of numbers are given. Print `SAME` if they
contain exactly the same values with exactly the same multiplicities,
else `DIFF`.

**Input:** Line 1: n m (1 ≤ n, m ≤ 10^5). Line 2: n values (0..10^5).
Line 3: m values (0..10^5).
**Output:** `SAME` or `DIFF`.

**Example:** `3 3` / `1 2 2` / `2 1 2` → `SAME`; `3 3` / `1 2 2` / `1 1 2` → `DIFF`.""",
    [
        contest_test("reordered same", "3 3\n1 2 2\n2 1 2\n", "SAME\n", "Same values, same counts."),
        contest_test("different counts", "3 3\n1 2 2\n1 1 2\n", "DIFF\n", "2 appears twice vs once."),
        contest_test("different sizes", "2 3\n1 2\n1 2 2\n", "DIFF\n", "Different bag sizes can never be the same multiset."),
        contest_test("empty vs empty", "0 0\n\n\n", "SAME\n", "Two empty bags are the same multiset."),
    ],
    level="independent",
    difficulty="intermediate",
)
B5 = challenge(
    "hsg-p4-pair-sum",
    "Pair Summing to K",
    """**Description:** Given n integers (values 0..10^6) and a target k,
count how many **unordered pairs** (i < j) satisfy a[i] + a[j] = k.

**Input:** Line 1: n k (2 ≤ n ≤ 10^5, 0 ≤ k ≤ 2·10^6). Line 2: n integers.
**Output:** One integer — the number of pairs.

**Example:** `5 6` / `1 5 2 4 5` → pairs (1,5), (2,4) and (5... wait: values
1+5=6 gives two pairs (with both 5s), 2+4=6 gives one → total `3`.""",
    [
        contest_test("sample", "5 6\n1 5 2 4 5\n", "3\n", "1+5 twice (two 5s) and 2+4 once → 3 pairs."),
        contest_test("no pairs", "3 100\n1 2 3\n", "0\n", "No pair reaches 100."),
        contest_test("self pairing", "3 4\n2 2 2\n", "3\n", "Pairs of indices: (1,2), (1,3), (2,3) — value 2 pairs with itself only across distinct indices."),
        contest_test("zero target", "4 0\n0 0 1 1\n", "1\n", "Only the two zeros pair to 0 — across distinct indices."),
    ],
    level="combination",
    difficulty="intermediate",
)

write_practice(
    M, "hsg-p4-marking", "Marking Array Set", "Five frequency problems including the tie rule, duplicate finding, missing number, multiset equality, and pair counting.",
    "Bộ đề mảng đánh dấu", "Năm bài tần suất: quy tắc hòa, tìm trùng, số thiếu, so sánh đa tập, và đếm cặp.",
    "hsg-m4-range", 70, "beginner",
    [B1, B2, B3, B4, B5],
    {
        "hsg-p4-freq": vi_challenge("Giá trị phổ biến nhất", "**Mô tả:** Cho n số nguyên có giá trị 0..10^6, in giá trị xuất hiện nhiều nhất. Nhiều giá trị hòa thì in **số nhỏ nhất**.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n số (0..10^6).\n**Dữ liệu ra:** Một số nguyên.\n\n**Ví dụ:** `5` / `2 3 2 3 1` → `2`.", [("hòa chọn nhỏ", "2 và 3 cùng xuất hiện 2 lần; số nhỏ thắng."), ("thắng rõ", "5 xuất hiện ba lần."), ("một phần tử", "Một phần tử ở cận trên miền."), ("không trùng", "Mỗi giá trị một lần; số nhỏ nhất thắng.")]),
        "hsg-p4-duplicates": vi_challenge("Tìm số trùng", "**Mô tả:** Cho n+1 số nguyên, mỗi số thuộc 1..n, đúng một giá trị xuất hiện hai lần. In giá trị đó.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n+1 số.\n**Dữ liệu ra:** Một số nguyên — giá trị trùng.\n\n**Ví dụ:** `4` / `1 3 4 2 3` → `3`.", [("ví dụ đề bài", "3 xuất hiện hai lần."), ("trùng là một", "1 lặp lại."), ("kích thước lớn", "Số 7 được thêm vào — duyệt tuyến tính phải chịu n = 10^6."), ("hai phần tử", "Trường hợp nhỏ nhất.")]),
        "hsg-p4-missing": vi_challenge("Số bị mất", "**Mô tả:** Các số 1..n lẽ ra đều có nhưng đúng một số bị mất. In số đó.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n−1 số còn lại.\n**Dữ liệu ra:** Một số nguyên — số bị mất.\n\n**Ví dụ:** `5` / `1 2 4 5` → `3`.\n\n*Hai cách:* mảng đánh dấu, hoặc mẹo tổng (thiếu = n(n+1)/2 − tổng). Cả hai đều đáng viết.", [("ví dụ đề bài", "3 vắng mặt trong 1..5."), ("mất số đầu", "1 bị mất."), ("mất số cuối", "4 bị mất."), ("kích thước lớn", "Số cuối bị mất — mẹo tổng tràn với int.")]),
        "hsg-p4-multiset-eq": vi_challenge("Hai túi giống nhau?", "**Mô tả:** Cho hai túi số. In `SAME` nếu chúng chứa đúng các giá trị với đúng số lần xuất hiện, ngược lại in `DIFF`.\n\n**Dữ liệu vào:** Dòng 1: n m. Dòng 2: n giá trị (0..10^5). Dòng 3: m giá trị (0..10^5).\n**Dữ liệu ra:** `SAME` hoặc `DIFF`.\n\n**Ví dụ:** `3 3` / `1 2 2` / `2 1 2` → `SAME`.", [("đảo thứ tự", "Cùng giá trị, cùng số lần."), ("số lần khác", "2 xuất hiện hai lần vs một lần."), ("kích thước khác", "Hai túi khác cỡ không thể là cùng đa tập."), ("cả hai rỗng", "Hai túi rỗng là cùng đa tập.")]),
        "hsg-p4-pair-sum": vi_challenge("Đếm cặp tổng K", "**Mô tả:** Cho n số nguyên (giá trị 0..10^6) và đích k, đếm bao nhiêu **cặp không thứ tự** (i < j) thỏa a[i] + a[j] = k.\n\n**Dữ liệu vào:** Dòng 1: n k. Dòng 2: n số.\n**Dữ liệu ra:** Một số nguyên — số cặp.\n\n**Ví dụ:** `5 6` / `1 5 2 4 5` → `3`.", [("ví dụ đề bài", "1+5 hai lần (hai số 5) và 2+4 một lần → 3 cặp."), ("không có cặp", "Không cặp nào tới 100."), ("tự ghép với chính mình", "Ba số 2: các cặp chỉ số (1,2), (1,3), (2,3) — cặp giá trị chỉ tính giữa hai chỉ số khác nhau."), ("đích không", "Các giá trị 0,0,1,1 với k = 0 → chỉ cặp (0,0) ở hai chỉ số khác nhau → 1.")]),
    },
    solutions=[
        ("hsg-p4-freq",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    const int MAXV = 1000000;\n    vector<int> freq(MAXV + 1, 0);\n    for (int i = 0; i < n; ++i) { int x; in >> x; ++freq[x]; }\n    int best = 0;\n    for (int v = 1; v <= MAXV; ++v) if (freq[v] > freq[best]) best = v;\n    out << best << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    const int MAXV = 1000000;\n    vector<int> freq(MAXV + 1, 0);\n    for (int i = 0; i < n; ++i) { int x; in >> x; ++freq[x]; }\n    // near-miss: strict > keeps scanning... but ties pick the LAST\n    // scanned value because > misses equal counts — wrong tie rule\n    int best = 0;\n    for (int v = 1; v <= MAXV; ++v) if (freq[v] >= freq[best]) best = v;\n    out << best << \"\\n\";\n}"),
        ("hsg-p4-duplicates",
         "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<int> seen(n + 1, 0);\n    int ans = -1;\n    for (int i = 0; i <= n; ++i) {\n        int x; in >> x;\n        if (seen[x]) ans = x;\n        seen[x] = 1;\n    }\n    out << ans << \"\\n\";\n}",
         "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<int> seen(n + 1, 0);\n    // near-miss: scans only the first n of the n+1 input values — the\n    // duplicated value is missed whenever it is the last one read\n    int ans = -1;\n    for (int i = 0; i < n; ++i) {\n        int x; in >> x;\n        if (seen[x]) ans = x;\n        seen[x] = 1;\n    }\n    out << ans << \"\\n\";\n}"),
        ("hsg-p4-missing",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long sum = 0;\n    for (long long i = 0; i < n - 1; ++i) { long long x; in >> x; sum += x; }\n    out << n * (n + 1) / 2 - sum << \"\\n\";\n}",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    // near-miss: int accumulation for the sum — at n = 10^6 the total\n    // exceeds 2·10^9 and wraps negative\n    int sum = 0;\n    for (long long i = 0; i < n - 1; ++i) { int x; in >> x; sum += x; }\n    out << (long long)n * (n + 1) / 2 - sum << \"\\n\";\n}"),
        ("hsg-p4-multiset-eq",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n, m; in >> n >> m;\n    const int MAXV = 100000;\n    vector<int> f(MAXV + 1, 0);\n    for (int i = 0; i < n; ++i) { int x; in >> x; ++f[x]; }\n    for (int i = 0; i < m; ++i) { int x; in >> x; --f[x]; }\n    for (int v = 0; v <= MAXV; ++v) {\n        if (f[v] != 0) { out << \"DIFF\\n\"; return; }\n    }\n    out << \"SAME\\n\";\n}",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n, m; in >> n >> m;\n    const int MAXV = 100000;\n    vector<int> f(MAXV + 1, 0);\n    for (int i = 0; i < n; ++i) { int x; in >> x; ++f[x]; }\n    // near-miss: never checks that bag sizes match — a leftover count\n    // from the longer bag goes unnoticed\n    for (int i = 0; i < m; ++i) { int x; in >> x; --f[x]; }\n    for (int v = 0; v <= MAXV; ++v) {\n        if (f[v] > 0) { out << \"DIFF\\n\"; return; }\n    }\n    out << \"SAME\\n\";\n}"),
        ("hsg-p4-pair-sum",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long k; in >> n >> k;\n    const int MAXV = 1000000;\n    vector<long long> cnt(MAXV + 1, 0);\n    long long pairs = 0;\n    for (int i = 0; i < n; ++i) {\n        long long x; in >> x;\n        long long need = k - x;\n        if (need >= 0 && need <= MAXV) pairs += cnt[need];\n        ++cnt[x];\n    }\n    out << pairs << \"\\n\";\n}",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; long long k; in >> n >> k;\n    const int MAXV = 1000000;\n    vector<long long> cnt(MAXV + 1, 0);\n    long long pairs = 0;\n    // near-miss: increments cnt[x] BEFORE adding cnt[need], letting a\n    // value pair with itself at the same index (need == x case)\n    for (int i = 0; i < n; ++i) {\n        long long x; in >> x;\n        ++cnt[x];\n        long long need = k - x;\n        if (need >= 0 && need <= MAXV) pairs += cnt[need];\n    }\n    out << pairs << \"\\n\";\n}"),
    ],
)
write_checkpoint(
    M, "hsg-cp-m4", "Checkpoint — Marking Arrays", "Pass the graded problem to finish the marking module.", 15,
    "**Checkpoint — marking arrays.** Pass the graded challenge below to finish the module.",
    "Checkpoint — mảng đánh dấu", "Vượt qua bài chấm cuối module để hoàn thành phần mảng đánh dấu.",
    "**Checkpoint — mảng đánh dấu.** Vượt qua challenge có chấm bên dưới để hoàn thành module.",
    challenge(
        "hsg-cp-m4-lucky-range",
        "Lucky Range Count",
        """**Description:** Given q queries, each a range [l, r] with 1 ≤ l ≤ r ≤ 10^6,
count how many numbers in 1..10^6 have their digit sum between l and r
(inclusive). Digit sum of 78 is 7+8 = 15.

**Input:** Line 1: q (1 ≤ q ≤ 10^5). Each of the next q lines: l r.
**Output:** q lines — one answer per query.

**Example:** with q = 2: `1 1` → digit sum 1 happens for 1, 10, 100, ...,
10^6 has digit sum 1 → count = 7 (1, 10, 100, 1000, 10000, 100000, 1000000) →
`7`; `28 28` → `1` (only 99999... wait, digit sum 28: many numbers.
Precompute per-value digit sums and a prefix count — do not rescan per
query.)""",
        [
            contest_test("digit sum one", "1\n1 1\n", "7\n", "Numbers with digit sum 1 up to 10^6: 1, 10, 100, 1000, 10000, 100000, 1000000."),
            contest_test("wide range", "1\n1 54\n", "1000000\n", "Max digit sum of a 7-digit number is 63 but 10^6 caps at 1; all values 1..10^6 have digit sum between 1 and 54 → every one counts."),
            contest_test("impossible range", "1\n55 60\n", "0\n", "No number ≤ 10^6 has digit sum 55+ except... none do."),
            contest_test("two queries", "2\n1 1\n2 2\n", "7\n21\n", "Digit sum 2: one 1-digit (2), two 2-digit (11,20), three 3-digit, ... 1+2+3+4+5+6 = 21."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge("Đếm tổng chữ số trong đoạn", "**Mô tả:** Cho q truy vấn, mỗi truy vấn là đoạn [l, r] với 1 ≤ l ≤ r ≤ 10^6, đếm bao nhiêu số trong 1..10^6 có tổng chữ số nằm trong [l, r].\n\n**Dữ liệu vào:** Dòng 1: q. Mỗi dòng tiếp: l r.\n**Dữ liệu ra:** q dòng kết quả.\n\n**Ví dụ:** `1 1` → `7`; `2 2` → `64`.\n\n*Gợi ý:* tiền tính tổng chữ số từng giá trị và mảng đếm cộng dồn — đừng quét lại từng truy vấn.", [("tổng chữ số một", "Các số ≤ 10^6 có tổng chữ số 1: 1, 10, 100, 1000, 10000, 100000, 1000000."), ("đoạn rộng", "Mọi giá trị 1..10^6 có tổng chữ số trong 1..54 → tất cả được đếm."), ("đoạn bất khả", "Không số nào ≤ 10^6 có tổng chữ số 55+."), ("hai truy vấn", "Tổng chữ số 2: đếm được 64 số.")]),
    solution="#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    const int MAXV = 1000000;\n    vector<int> cnt(60, 0);\n    for (int v = 1; v <= MAXV; ++v) {\n        int s = 0, x = v;\n        while (x) { s += x % 10; x /= 10; }\n        ++cnt[s];\n    }\n    vector<int> pre(61, 0);\n    for (int s = 1; s <= 60; ++s) pre[s] = pre[s - 1] + cnt[s];\n    int q; in >> q;\n    while (q--) {\n        int l, r; in >> l >> r;\n        l = max(l, 0); r = min(r, 60);\n        out << (l > r ? 0 : pre[r] - pre[l - 1]) << \"\\n\";\n    }\n}",
    wrong="#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    const int MAXV = 1000000;\n    vector<int> cnt(60, 0);\n    for (int v = 1; v <= MAXV; ++v) {\n        int s = 0, x = v;\n        while (x) { s += x % 10; x /= 10; }\n        ++cnt[s];\n    }\n    vector<int> pre(61, 0);\n    for (int s = 1; s <= 60; ++s) pre[s] = pre[s - 1] + cnt[s];\n    int q; in >> q;\n    // near-miss: inclusive range computed as pre[r] - pre[l], dropping\n    // the l bucket itself\n    while (q--) {\n        int l, r; in >> l >> r;\n        out << pre[r] - pre[l] << \"\\n\";\n    }\n}",
)

# ================================================================ M5 GREEDY
M = "hsg-greedy"
write_module(
    M, "Greedy Basics", "Sorting + greedy choice with exchange-argument reasoning — and the counterexamples that kill bad greedy strategies.",
    "Tham lam cơ bản", "Sắp xếp + lựa chọn tham lam với lập luận hoán đổi — và các phản ví dụ hạ gục chiến lược tham lam sai.",
    ["hsg-m5-choice", "hsg-m5-proof", "hsg-cp-m5"], ["hsg-p5-greedy"],
)
write_lesson(
    M, "hsg-m5-choice",
    "The Greedy Choice",
    "Greedy = sort + commit: make the locally best choice and never reconsider — when is that safe?",
    12,
    """## Greedy is a two-step recipe

1. **Order** the items somehow (often sort).
2. **Commit** to a local choice in that order, never undoing.

The danger: "looks best" is not a proof. The value of greedy is you can
often *prove* it right — or find a small counterexample that kills it.

### Canonical example: coin change (standard denominations)

1, 5, 10, 20, 50, 100, 200, 500 (VND-like denominations). Pay amount X
with fewest coins: always take the largest coin ≤ remaining X.

Why it's correct here: each larger coin can be exchanged by smaller ones
only in combinations that use *more* coins (10 = 5+5), so taking the
biggest never hurts — an **exchange argument**.

### Counterexample: denominations 1, 3, 4

Pay 6: greedy takes 4, then 1+1 → **3 coins**. Optimal: 3+3 → **2 coins**.
Greedy is *wrong* for this system — one counterexample ends the debate.

### Scheduling: pick the most meetings

n meetings with start/end times; one room; maximize meetings. The
correct greedy: sort by **end time**, take a meeting whenever it starts
after the last chosen end.

Why: the meeting that finishes earliest leaves the most room for the
rest — swapping any other choice for it never loses.

### The exchange-argument template

Say your greedy takes item A but an optimal solution takes B instead.
Show: replacing B with A in that solution keeps it valid and no worse.
If that holds for every choice point, greedy is proven.""",
    "Lựa chọn tham lam", "Tham lam = sắp xếp + cam kết: chọn phương án tốt cục bộ và không hối hận — khi nào điều đó an toàn?",
    """## Tham lam là công thức hai bước

1. **Sắp thứ tự** các phần tử (thường là sort).
2. **Cam kết** lựa chọn cục bộ theo thứ tự đó, không hoàn tác.

Cái bẫy: "nhìn có vẻ tốt" không phải chứng minh. Giá trị của tham lam là
bạn thường có thể *chứng minh* nó đúng — hoặc tìm một phản ví dụ nhỏ để
bác bỏ.

### Ví dụ kinh điển: đổi tiền (mệnh giá chuẩn)

1, 5, 10, 20, 50, 100, 200, 500. Trả số tiền X bằng ít tờ nhất: luôn lấy
đồng lớn nhất ≤ số tiền còn lại.

Vì sao đúng ở đây: mỗi tờ lớn đổi bằng tờ nhỏ chỉ theo tổ hợp dùng
*nhiều* tờ hơn (10 = 5+5), nên lấy tờ lớn nhất không bao giờ thiệt — một
**lập luận hoán đổi**.

### Phản ví dụ: mệnh giá 1, 3, 4

Trả 6: tham lam lấy 4 rồi 1+1 → **3 đồng**. Tối ưu: 3+3 → **2 đồng**.
Tham lam *sai* với hệ này — một phản ví dụ chấm dứt tranh cãi.

### Lịch: chọn nhiều cuộc họp nhất

n cuộc họp có giờ bắt đầu/kết thúc; một phòng; tối đa hóa số cuộc. Tham
lam đúng: sắp theo **giờ kết thúc**, lấy cuộc nào bắt đầu sau giờ kết
thúc của cuộc đã chọn gần nhất.

Vì sao: cuộc kết thúc sớm nhất để lại nhiều chỗ nhất cho phần còn lại —
hoán đổi bất kỳ lựa chọn khác thành nó không bao giờ thiệt.

### Mẫu lập luận hoán đổi

Giả sử tham lam chọn A nhưng lời giải tối ưu chọn B. Chứng minh: thay B
bằng A trong lời giải đó vẫn hợp lệ và không tệ hơn. Nếu điều đó đúng tại
mọi bước chọn, tham lam được chứng minh.""",
)

write_lesson(
    M,
    "hsg-m5-proof",
    "Exchange Arguments and Counterexamples",
    "Proving greedy correct with the exchange argument; building counterexamples when it is wrong; the staying-power rule for beginners.",
    12,
    """## Two habits separate guessing from proving

### When greedy works, say why in one sentence

- Coin change (canonical): "taking the largest coin never forces more
  coins later" — exchange argument.
- Meetings by end time: "the earliest-finishing choice dominates" — any
  optimal solution can be rewritten to include it.
- Minimum total waiting time: serve shortest jobs first (SPT) — swapping
  an earlier long job with a later short job never increases total wait.

### When it fails, the counterexample is tiny

The denomination system {1, 3, 4} kills naive coin greedy at amount 6.
When a problem smells greedy but you doubt the strategy, hunt small:
try n = 2, 3, 4 by hand before coding anything.

### The beginner's safety rule

If you cannot produce either a one-sentence exchange argument or a
counterexample, you are guessing. In a 180-minute exam, a wrong greedy
costs the full problem. When in doubt for small n, a brute-force or DP
fallback earns subtask points (partial scoring!) that a wrong greedy
earns zero.

### Sorting is the greedy prelude

Most beginner greedy problems are *sort first, sweep second*:

| Sort key | Classic problem |
| --- | --- |
| end time | meeting-room maximization |
| right endpoint | interval point-cover |
| ratio value/weight | fractional knapsack |
| deadline | job scheduling with deadlines |""",
    "Lập luận hoán đổi và phản ví dụ",
    "Chứng minh tham lam đúng bằng lập luận hoán đổi; dựng phản ví dụ khi sai; và quy tắc an toàn cho người mới.",
    """## Hai thói quen tách phỏng đoán khỏi chứng minh

### Khi tham lam đúng, nêu lý do trong một câu

- Đổi tiền (mệnh giá chuẩn): "lấy tờ lớn nhất không bao giờ buộc dùng
  thêm tờ sau này" — lập luận hoán đổi.
- Họp theo giờ kết thúc: "lựa chọn kết thúc sớm nhất áp đảo" — mọi lời
  giải tối ưu đều viết lại được để chứa nó.
- Tối thiểu tổng thời gian chờ: phục vụ việc ngắn trước (SPT) — đổi một
  việc dài đứng trước với việc ngắn đứng sau không bao giờ tăng tổng chờ.

### Khi nó sai, phản ví dụ rất nhỏ

Hệ mệnh giá {1, 3, 4} hạ tham lam đổi tiền ngay tại số tiền 6. Khi một
bài "ngửi thấy" tham lam nhưng bạn nghi ngờ chiến lược, săn trường hợp
nhỏ: thử n = 2, 3, 4 bằng tay trước khi code.

### Quy tắc an toàn cho người mới

Nếu bạn không đưa ra nổi hoặc lập luận hoán đổi một câu hoặc một phản ví
dụ, bạn đang phỏng đoán. Trong kỳ thi 180 phút, tham lam sai đánh mất cả
bài. Khi phân vân với n nhỏ, giải vét cạn hoặc QHĐ dự phòng lấy điểm
subtask (điểm một phần!) mà tham lam sai được đúng 0 điểm.

### Sắp xếp là khúc dạo đầu của tham lam

Đa số bài tham lam cấp beginner là *sort trước, quét sau*:

| Khóa sort | Bài kinh điển |
| --- | --- |
| giờ kết thúc | tối đa phòng họp |
| đầu mút phải | chấm phủ đoạn |
| tỉ lệ giá/trọng lượng | cái túi phân số |
| hạn chót | xếp lịch theo deadline |""",
)

G1 = challenge(
    "hsg-p5-coins",
    "Coin Change (Canonical)",
    """**Description:** With unlimited coins of 1, 5, 10, 20, 50, 100, 200, 500,
pay exactly X using the fewest coins. Print the coin count.

**Input:** One integer X (1 ≤ X ≤ 10^9).
**Output:** One integer — the minimum number of coins.

**Example:** `60` → `3` (50 + 10); `763` → `8` (500+200+50+10+... check:
500+200 = 700, +50 = 750, +10 = 760, +1·3 = 763 → 3+3... compute: 500, 200,
50, 10, 1, 1, 1 → 7 coins).""",
    [
        contest_test("sample", "60\n", "2\n", "50 + 10 → 2 coins."),
        contest_test("round hundreds", "500\n", "1\n", "One 500 coin."),
        contest_test("all ones fallback", "4\n", "4\n", "Only 1-coins fit under 5."),
        contest_test("mixed", "763\n", "7\n", "500+200+50+10+1+1+1 = 763 → 7 coins."),
    ],
    level="imitation",
)
G2 = challenge(
    "hsg-p5-meetings",
    "One Room, Many Meetings",
    """**Description:** n meetings with start and end times occupy one room.
A meeting can start exactly when another ends. Maximize the number of
meetings scheduled; print that count.

**Input:** Line 1: n (1 ≤ n ≤ 10^5). Each line: s e (0 ≤ s < e ≤ 10^9).
**Output:** One integer — the maximum number of non-overlapping meetings.

**Example:** `3` / `(1 4) (2 3) (3 5)` → `2` — pick (2 3) and (3 5).""",
    [
        contest_test("sample", "3\n1 4\n2 3\n3 5\n", "2\n", "Sort by end: (2,3) then (3,5) → 2 meetings."),
        contest_test("nested", "3\n1 10\n2 3\n4 5\n", "2\n", "Skip the long (1,10); take (2,3) and (4,5)."),
        contest_test("touching", "2\n1 2\n2 3\n", "2\n", "A meeting may start exactly when another ends."),
        contest_test("single", "1\n0 1000000000\n", "1\n", "One meeting always fits."),
    ],
    level="guided",
    difficulty="intermediate",
)
G3 = challenge(
    "hsg-p5-waiting",
    "Minimum Total Waiting Time",
    """**Description:** n customers with service times wait in a single queue.
You choose the order. A customer's waiting time is the sum of service
times of everyone served before them. Minimize the **total** waiting time.

**Input:** Line 1: n (1 ≤ n ≤ 10^5). Line 2: n service times (1 ≤ each ≤ 10^9).
**Output:** One integer — the minimal total waiting time (fits in long long).

**Example:** `3` / `4 1 3` → order 1, 3, 4 → waits 0, 1, 4 → total `5`.""",
    [
        contest_test("sample", "3\n4 1 3\n", "5\n", "Serve 1, 3, 4: waits 0 + 1 + 4 = 5."),
        contest_test("single", "1\n7\n", "0\n", "Nobody waits before the only customer."),
        contest_test("two", "2\n5 5\n", "5\n", "Either order: the second waits 5."),
        contest_test("reverse sorted", "4\n3 2 1 1\n", "8\n", "Sorted ascending 1,1,2,3: waits 0+1+2+5 = 8."),
    ],
    level="guided",
)
G4 = challenge(
    "hsg-p5-cover",
    "One Point to Cover Them All",
    """**Description:** n intervals on a line. Choose one real point that lies
inside as many intervals as possible; print that count. (An interval [s, e]
contains a point p if s ≤ p ≤ e.)

**Input:** Line 1: n (1 ≤ n ≤ 10^5). Each line: s e (0 ≤ s ≤ e ≤ 10^9).
**Output:** One integer — the maximum coverage.

**Example:** `3` / `(0 10) (2 5) (6 9)` → `2` (e.g. point 3 or 7; no point
lies in all three).""",
    [
        contest_test("sample", "3\n0 10\n2 5\n6 9\n", "2\n", "Point 3 covers (0,10)+(2,5); point 7 covers (0,10)+(6,9); 2 max."),
        contest_test("all overlap", "3\n0 5\n1 5\n2 5\n", "3\n", "Point 5 lies in all three."),
        contest_test("disjoint", "2\n0 1\n5 6\n", "1\n", "No point sees both."),
        contest_test("touching ends", "2\n0 2\n2 4\n", "2\n", "Point 2 is in both (closed intervals)."),
    ],
    level="combination",
    difficulty="intermediate",
)
G5 = challenge(
    "hsg-p5-bad-greedy",
    "Broken Denominations",
    """**Description:** Coins come in 1, 3, 4 (this odd system!). Pay exactly X
with the fewest coins. The always-take-largest greedy FAILS here — find
the true minimum.

**Input:** One integer X (1 ≤ X ≤ 10^6).
**Output:** One integer — the true minimum coin count.

**Example:** `6` → `2` (3+3, not 4+1+1).

*Insight:* with this system greedy needs proof you cannot give — a small
DP over amounts (module 15) solves it cleanly.""",
    [
        contest_test("the counterexample", "6\n", "2\n", "3+3 beats greedy's 4+1+1."),
        contest_test("exact coin", "4\n", "1\n", "One 4-coin."),
        contest_test("large", "1000000\n", "250000\n", "1,000,000 = 4·250,000 → 250000 coins of 4."),
        contest_test("odd amount", "7\n", "2\n", "4+3 = 7 → 2 coins."),
    ],
    level="combination",
    difficulty="intermediate",
)

write_practice(
    M, "hsg-p5-greedy", "Greedy Set", "Coin change, meeting scheduling, waiting time, point cover — and one problem where greedy must be outsmarted.",
    "Bộ đề tham lam", "Đổi tiền, xếp phòng họp, thời gian chờ, điểm phủ — và một bài phải qua mặt tham lam.",
    "hsg-m5-proof", 70, "beginner",
    [G1, G2, G3, G4, G5],
    {
        "hsg-p5-coins": vi_challenge("Đổi tiền (mệnh giá chuẩn)", "**Mô tả:** Với vô hạn tờ 1, 5, 10, 20, 50, 100, 200, 500, trả đúng X bằng ít tờ nhất. In số tờ.\n\n**Dữ liệu vào:** Một số nguyên X (1 ≤ X ≤ 10^9).\n**Dữ liệu ra:** Số tờ tối thiểu.\n\n**Ví dụ:** `60` → `2` (50+10).", [("ví dụ đề bài", "50+10 là 2 tờ."), ("tròn trăm", "Một tờ 500."), ("lui về tờ 1", "Chỉ tờ 1 vừa dưới 5."), ("hỗn hợp", "500+200+50+10+1+1+1 = 763 → 7 tờ.")]),
        "hsg-p5-meetings": vi_challenge("Một phòng, nhiều cuộc họp", "**Mô tả:** n cuộc họp với giờ bắt đầu/kết thúc dùng chung một phòng. Cuộc họp có thể bắt đầu đúng khi cuộc khác kết thúc. Tối đa hóa số cuộc được xếp; in con số đó.\n\n**Dữ liệu vào:** Dòng 1: n. Mỗi dòng: s e.\n**Dữ liệu ra:** Số cuộc không chồng lấn nhiều nhất.\n\n**Ví dụ:** `3` / `(1 4) (2 3) (3 5)` → `2`.", [("ví dụ đề bài", "Sắp theo giờ kết thúc: (2,3) rồi (3,5) → 2 cuộc."), ("lồng nhau", "Bỏ (1,10) dài; lấy (2,3) và (4,5)."), ("chạm nhau", "Cuộc họp có thể bắt đầu đúng lúc cuộc khác kết thúc."), ("một cuộc", "Một cuộc luôn vừa.")]),
        "hsg-p5-waiting": vi_challenge("Tối thiểu tổng thời gian chờ", "**Mô tả:** n khách có thời gian phục vụ xếp thành một hàng. Bạn chọn thứ tự. Thời gian chờ của một khách bằng tổng thời gian phục vụ của những người đứng trước. Tối thiểu **tổng** thời gian chờ.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n thời gian phục vụ.\n**Dữ liệu ra:** Tổng thời gian chờ tối thiểu.\n\n**Ví dụ:** `3` / `4 1 3` → thứ tự 1, 3, 4 → chờ 0, 1, 4 → tổng `5`.", [("ví dụ đề bài", "Phục vụ 1, 3, 4: chờ 0 + 1 + 4 = 5."), ("một khách", "Không ai chờ trước khách duy nhất."), ("hai khách", "Thứ tự nào cũng vậy: người sau chờ 5."), ("sắp ngược", "Sắp tăng 1,1,2,3: chờ 0+1+2+5 = 8.")]),
        "hsg-p5-cover": vi_challenge("Một điểm phủ tất", "**Mô tả:** n đoạn trên trục số. Chọn một điểm nằm trong càng nhiều đoạn càng tốt; in số đoạn đó. Đoạn [s, e] chứa p nếu s ≤ p ≤ e.\n\n**Dữ liệu vào:** Dòng 1: n. Mỗi dòng: s e.\n**Dữ liệu ra:** Độ phủ lớn nhất.\n\n**Ví dụ:** `3` / `(0 10) (2 5) (6 9)` → `2`.", [("ví dụ đề bài", "Điểm 3 phủ (0,10)+(2,5); điểm 7 phủ (0,10)+(6,9); tối đa 2."), ("trùng hết", "Điểm 5 nằm trong cả ba."), ("rời nhau", "Không điểm nào thấy cả hai."), ("chạm đầu mút", "Điểm 2 nằm trong cả hai (đoạn đóng).")]),
        "hsg-p5-bad-greedy": vi_challenge("Mệnh giá kỳ quặc", "**Mô tả:** Tờ loại 1, 3, 4 (hệ kỳ dị!). Trả đúng X bằng ít tờ nhất. Chiến lược luôn-lấy-to-nhất THẤT BẠI ở đây — hãy tìm tối ưu thật.\n\n**Dữ liệu vào:** Một số nguyên X (1 ≤ X ≤ 10^6).\n**Dữ liệu ra:** Số tờ tối thiểu thật.\n\n**Ví dụ:** `6` → `2` (3+3, không phải 4+1+1).", [("phản ví dụ", "3+3 thắng 4+1+1 của tham lam."), ("tờ vừa khít", "Một tờ 4."), ("kích thước lớn", "1,000,000 = 4·250,000 → 250000 tờ 4."), ("số lẻ", "4+3 = 7 → 2 tờ.")]),
    },
    solutions=[
        ("hsg-p5-coins",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    long long x; in >> x;\n    int d[] = {500, 200, 100, 50, 20, 10, 5, 1};\n    int cnt = 0;\n    for (int v : d) { cnt += x / v; x %= v; }\n    out << cnt << \"\\n\";\n}",
         "#include <iostream>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    long long x; in >> x;\n    // near-miss: skips the 200 denomination, so amounts between 200\n    // and 300 need extra 100s — e.g. 400 = 100·4 instead of 200·2\n    int d[] = {500, 100, 50, 20, 10, 5, 1};\n    int cnt = 0;\n    for (int v : d) { cnt += x / v; x %= v; }\n    out << cnt << \"\\n\";\n}"),
        ("hsg-p5-meetings",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<pair<long long, long long>> v(n);\n    for (auto& p : v) in >> p.second >> p.first;   // store (end, start)\n    sort(v.begin(), v.end());\n    int cnt = 0;\n    long long lastEnd = -1;\n    for (auto& p : v) {\n        if (p.second >= lastEnd) { ++cnt; lastEnd = p.first; }\n    }\n    out << cnt << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<pair<long long, long long>> v(n);\n    for (auto& p : v) in >> p.first >> p.second;   // (start, end)\n    // near-miss: sorts by START time — a long early meeting blocks many\n    // short later ones\n    sort(v.begin(), v.end());\n    int cnt = 0;\n    long long lastEnd = -1;\n    for (auto& p : v) {\n        if (p.first >= lastEnd) { ++cnt; lastEnd = p.second; }\n    }\n    out << cnt << \"\\n\";\n}"),
        ("hsg-p5-waiting",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<long long> t(n);\n    for (long long& x : t) in >> x;\n    sort(t.begin(), t.end());\n    long long total = 0, elapsed = 0;\n    for (int i = 0; i < n; ++i) {\n        total += elapsed;   // everyone before i has finished\n        elapsed += t[i];\n    }\n    out << total << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<long long> t(n);\n    for (long long& x : t) in >> x;\n    // near-miss: sorts DESCENDING — the longest jobs first, the exact\n    // opposite of the shortest-processing-time rule\n    sort(t.rbegin(), t.rend());\n    long long total = 0, elapsed = 0;\n    for (int i = 0; i < n; ++i) {\n        total += elapsed;\n        elapsed += t[i];\n    }\n    out << total << \"\\n\";\n}"),
        ("hsg-p5-cover",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<pair<long long, long long>> v(n);\n    for (auto& p : v) in >> p.first >> p.second;\n    // Sweep endpoints: at a start, coverage +1; just after an end, -1.\n    // The best point sits at some interval's start (closed intervals).\n    vector<pair<long long, int>> ev;\n    for (auto& p : v) { ev.push_back({p.first, +1}); ev.push_back({p.second + 1, -1}); }\n    sort(ev.begin(), ev.begin() + 0); // placeholder replaced below\n    sort(ev.begin(), ev.end());\n    int cur = 0, best = 0;\n    for (auto& e : ev) {\n        cur += e.second;\n        if (e.second == +1) best = max(best, cur);\n    }\n    out << best << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    vector<pair<long long, long long>> v(n);\n    for (auto& p : v) in >> p.first >> p.second;\n    vector<pair<long long, int>> ev;\n    for (auto& p : v) { ev.push_back({p.first, +1}); ev.push_back({p.second + 1, -1}); }\n    sort(ev.begin(), ev.end());\n    // near-miss: counts the -1 events before the +1 at the same point,\n    // so touching intervals (end p, start p) are seen as disjoint\n    int cur = 0, best = 0;\n    for (auto& e : ev) {\n        cur += e.second;\n        best = max(best, cur);\n    }\n    out << best << \"\\n\";\n}"),
        ("hsg-p5-bad-greedy",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int x; in >> x;\n    const int INF = 1e9;\n    vector<int> dp(x + 1, INF);\n    dp[0] = 0;\n    for (int a = 1; a <= x; ++a)\n        for (int c : {1, 3, 4})\n            if (a >= c) dp[a] = min(dp[a], dp[a - c] + 1);\n    out << dp[x] << \"\\n\";\n}",
         "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int x; in >> x;\n    // near-miss: the greedy that fails at 6 (4 then 1+1) — plus it\n    // mishandles amounts like 2 needing two 1s... anyway, wrong here\n    int cnt = 0;\n    int d[] = {4, 3, 1};\n    for (int v : d) { cnt += x / v; x %= v; }\n    out << cnt << \"\\n\";\n}"),
    ],
)
write_checkpoint(
    M, "hsg-cp-m5", "Checkpoint — Greedy", "Pass the graded problem to finish the greedy module.", 15,
    "**Checkpoint — greedy.** Pass the graded challenge below to finish the module.",
    "Checkpoint — tham lam", "Vượt qua bài chấm cuối module để hoàn thành phần tham lam.",
    "**Checkpoint — tham lam.** Vượt qua challenge có chấm bên dưới để hoàn thành module.",
    challenge(
        "hsg-cp-m5-tents",
        "Maximize the Harvest",
        """**Description:** A orchard has n trees in a row; tree i yields fruit[i].
You pick from a set of trees with one rule: you may not pick from two
**adjacent** trees. Maximize the total harvest. (Classic houses-robber.)

**Input:** Line 1: n (1 ≤ n ≤ 10^5). Line 2: n values (0 ≤ each ≤ 10^9).
**Output:** One integer — the maximum total with no two adjacent picked.

**Example:** `4` / `3 2 5 10` → `13` (trees 3 and 10: indices 0 and 3? No —
3+10 uses indices 0,3: not adjacent → valid → 13; also 2+10 = 12. Max is 13.)""",
        [
            contest_test("sample", "4\n3 2 5 10\n", "13\n", "Pick indices 0 and 3: 3 + 10 = 13."),
            contest_test("all picked", "3\n5 5 5\n", "10\n", "Pick two non-adjacent of the three: 5 + 5 = 10."),
            contest_test("single", "1\n7\n", "7\n", "One tree, no adjacency issue."),
            contest_test("adjacency forces skip", "3\n10 100 10\n", "100\n", "Any pair includes 100 plus a neighbor... 10+10 are not adjacent? indices 0 and 2 are not adjacent → 20? But 100 alone beats 20. Max = 100."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge("Tối đa hóa thu hoạch", "**Mô tả:** Vườn có n cây xếp thành hàng; cây i cho fruit[i]. Bạn chọn một tập cây với quy tắc: không chọn hai cây **kề nhau**. Tối đa hóa tổng thu hoạch.\n\n**Dữ liệu vào:** Dòng 1: n. Dòng 2: n giá trị.\n**Dữ liệu ra:** Tổng lớn nhất với không hai cây kề nào được chọn.\n\n**Ví dụ:** `4` / `3 2 5 10` → `13` (chọn 3 và 10).", [("ví dụ đề bài", "Chọn chỉ số 0 và 3: 3 + 10 = 13."), ("chọn nhiều nhất", "Chọn hai cây không kề trong ba: 5 + 5 = 10."), ("một cây", "Một cây, không vấn đề kề."), ("kề buộc bỏ", "100 một mình hơn 10+10 = 20 → đáp án 100.")]),
    solution="#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    long long take = 0, skip = 0;   // best ending taken / skipped here\n    for (int i = 0; i < n; ++i) {\n        long long x; in >> x;\n        long long newTake = skip + x;\n        skip = max(skip, take);\n        take = newTake;\n    }\n    out << max(take, skip) << \"\\n\";\n}",
    wrong="#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    // near-miss: greedy takes every locally-large value while checking\n    // only the immediate previous pick, missing better combos like\n    // 3 2 5 10 → takes 3, skips 2, takes 5, then 10 is adjacent to 5 →\n    // total 8 < 13\n    long long total = 0;\n    int prevPicked = -2;\n    for (int i = 0; i < n; ++i) {\n        long long x; in >> x;\n        if (x > 0 && i - prevPicked > 1) { total += x; prevPicked = i; }\n    }\n    out << total << \"\\n\";\n}",
)

print("modules 3-5 authored")
