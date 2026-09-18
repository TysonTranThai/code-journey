#!/usr/bin/env python3
"""HSG — Module 17: hsg-twopointers (hai con trỏ / cửa sổ trượt).

Same-direction pair scans, opposite-end convergence, and the shrink-while-
invalid sliding window with frequency arrays. Conventions: T() for test I/O,
cpp() for bodies.
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

M = "hsg-twopointers"
write_module(
    M,
    "Two Pointers & Sliding Window",
    "Turn O(n^2) pair scans into O(n): two indices that each move forward at most n times.",
    "Hai con trỏ & cửa sổ trượt",
    "Biến quét cặp O(n^2) thành O(n): hai chỉ số, mỗi con trỏ chỉ tiến tối đa n lần.",
    ["hsg-m17-idea", "hsg-m17-window", "hsg-cp-m17"],
    ["hsg-p17-tp"],
)

write_lesson(
    M,
    "hsg-m17-idea",
    "Two Pointers on Sorted Data",
    "Opposite ends or same direction — both are O(n) because no index ever moves backwards.",
    14,
    """## Opposite ends: pair sums on sorted data

Find two values summing to S in a SORTED array. Start l = 0,
r = n-1:

- a[l] + a[r] < S: the sum is too small — only moving l up can help.
- a[l] + a[r] > S: too big — only moving r down can help.
- equal: report.

Every step discards one element forever, so at most n steps total —
that is the whole proof of O(n). On UNSORTED data the invariant dies
(hash set or sort-with-index instead).

```cpp
int l = 0, r = n - 1;
while (l < r) {
    long long s = a[l] + a[r];
    if (s == S) { found; break; }
    if (s < S) ++l; else --r;
}
```

## Same direction: remove/skip patterns

Both pointers walk left-to-right, the fast one reading, the slow one
writing or anchoring: deduplication, merging sorted arrays, partition.
The cost argument is the same: each pointer advances at most n times,
so the loop body runs O(n) total.

## The anti-pattern

Nested loops that RESCAN from 0 every iteration are O(n^2) and the
usual symptom is TLE at n = 10^5. If your inner loop can be made to
continue from where it left off — monotonicity — two pointers apply.
""",
    "Hai con trỏ trên dữ liệu đã sắp",
    "Hai đầu hội tụ hoặc cùng chiều — đều O(n) vì không chỉ số nào lùi lại.",
    """## Hai đầu hội tụ: tổng cặp trên mảng đã sắp

Tìm hai giá trị có tổng S trong mảng ĐÃ SẮP. Đặt l = 0, r = n-1:

- a[l] + a[r] < S: tổng quá nhỏ — chỉ đưa l lên mới giúp được.
- a[l] + a[r] > S: quá lớn — chỉ hạ r xuống mới giúp được.
- bằng: báo kết quả.

Mỗi bước vứt bỏ một phần tử mãi mãi, nên tối đa n bước — đó là toàn bộ
lập luận O(n). Trên dữ liệu CHƯA sắp, bất biến này sụp đổ (dùng hash
set hoặc sort kèm chỉ số).

```cpp
int l = 0, r = n - 1;
while (l < r) {
    long long s = a[l] + a[r];
    if (s == S) { found; break; }
    if (s < S) ++l; else --r;
}
```

## Cùng chiều: các mẫu bỏ/nhảy

Cả hai con trỏ đi trái sang phải, con trỏ nhanh đọc, con trỏ chậm ghi
hoặc neo: khử trùng lặp, trộn hai mảng đã sắp, phân hoạch. Lập luận
chi phí y hệt: mỗi con trỏ tiến tối đa n lần, nên thân vòng lặp chạy
tổng cộng O(n).

## Chống-mẫu

Vòng lặp lồng quét LẠI từ 0 mỗi lần là O(n^2) và triệu chứng quen thuộc
là TLE tại n = 10^5. Nếu vòng trong có thể tiếp tục từ chỗ dừng — tính
đơn điệu — thì hai con trỏ áp dụng được.
""",
)

write_lesson(
    M,
    "hsg-m17-window",
    "The Sliding Window",
    "Grow right; while invalid, shrink left. Frequencies make validity O(1).",
    16,
    """## The invariant

A window [l, r] is maintained so that it is always *valid* (or one
shrink away from valid). Right expands one step at a time; whenever
the invariant breaks, left advances until it holds again:

```cpp
int l = 0;
for (int r = 0; r < n; ++r) {
    add(a[r]);                       // O(1) bookkeeping
    while (invalid()) remove(a[l++]); // each l advances <= n times total
    answer(r - l + 1);                // window ending at r
}
```

The while is not O(n) per step: l only ever moves forward, so it moves
at most n times across the WHOLE run — amortized O(1) per right step.

## Distinct-elements window

Count of distinct values via a frequency array (`cnt[v]`) and a
counter of values with cnt > 0. Add: if cnt[v]++ becomes 1, ++distinct.
Remove: if --cnt[v] hits 0, --distinct.

## Fixed-size windows

When k is constant, the window never shrinks: add a[r], remove a[r-k],
keep a running sum — moving averages, max-sum-k. This is the prefix-
sum cousin; prefer it when only sums are needed.

## When windows do NOT apply

Negative numbers break max-window-deque problems (monotonic deque,
later course) and non-monotone validity (need l to jump) needs binary
search or another tool. Checking "does the window apply?" before
coding is the competition skill.
""",
    "Cửa sổ trượt",
    "Mở rộng biên phải; trong khi bất hợp lệ, thu biên trái. Bảng tần suất khiến kiểm tra hợp lệ thành O(1).",
    """## Bất biến

Duy trì cửa sổ [l, r] sao cho luôn *hợp lệ* (hoặc cách một bước thu).
Biên phải mở rộng từng bước; khi bất biến bị phá, biên trái tiến tới
khi nó giữ lại:

```cpp
int l = 0;
for (int r = 0; r < n; ++r) {
    add(a[r]);                        // sổ sách O(1)
    while (invalid()) remove(a[l++]); // mỗi l tiến <= n lần tổng cộng
    answer(r - l + 1);                // cửa sổ kết thúc tại r
}
```

Vòng while không tốn O(n) mỗi bước: l chỉ tiến về trước, nên nó tiến
tối đa n lần trong TOÀN bộ — khấu trừ O(1) mỗi bước phải.

## Cửa sổ phần tử phân biệt

Đếm giá trị phân biệt bằng bảng tần suất (`cnt[v]`) và một bộ đếm số
giá trị có cnt > 0. Thêm: nếu cnt[v]++ thành 1 thì ++distinct. Bỏ:
nếu --cnt[v] chạm 0 thì --distinct.

## Cửa sổ cỡ cố định

Khi k là hằng số, cửa sổ không bao giờ thu: thêm a[r], bỏ a[r-k], giữ
tổng chạy — trung bình động, tổng-k lớn nhất. Đây là anh em với mảng
cộng dồn; ưu tiên khi chỉ cần tổng.

## Khi cửa sổ KHÔNG áp dụng được

Số âm phá các bài cửa-sổ-max (deque đơn điệu, khóa sau) và tính hợp lệ
không đơn điệu (l phải nhảy) cần tìm kiếm nhị phân hoặc công cụ khác.
Kiểm tra "cửa sổ áp dụng được không?" trước khi code chính là kỹ năng
thi đấu.
""",
)

A1 = challenge(
    "hsg-p17-pair-sum",
    "Sorted Pair Sum",
    T(
        "**Description:** In a sorted array of n integers, decide whether two elements at",
        "DIFFERENT positions sum exactly to S.",
        "",
        "**Input:** Line 1: n S (2 <= n <= 200000, |S| <= 10^18). Line 2: n sorted integers",
        "(|a[i]| <= 10^9).",
        "**Output:** Print `YES` if such a pair exists, otherwise `NO`.",
        "",
        "**Example:** `5 9` / `1 2 4 7 11` -> `YES` (2 + 7).",
    ),
    [
        contest_test("sample", T("5 9", "1 2 4 7 11"), T("YES"), "2 + 7 = 9."),
        contest_test("asymmetric move", T("4 6", "2 3 4 7"), T("YES"),
                     "2+4: requires lowering r twice while l stays — move-both-pointer code prints NO."),
        contest_test("duplicates", T("4 6", "3 3 3 3"), T("YES"),
                     "Different POSITIONS, equal values — two 3s."),
        contest_test("negatives", T("3 -5", "-9 -4 1"), T("NO"),
                     "Pair sums are -13, -8, -3 — none equals -5."),
        contest_test("two elements", T("2 0", "-3 3"), T("YES"), "Opposite signs meet."),
    ],
    level="guided",
    difficulty="intermediate",
)

A2 = challenge(
    "hsg-p17-merge",
    "Count Inversions-lite",
    T(
        "**Description:** Two sorted arrays A (n) and B (m). Count pairs (i, j) with",
        "A[i] > B[j].",
        "",
        "**Input:** Line 1: n m (1 <= n, m <= 200000). Line 2: n sorted ints. Line 3: m",
        "sorted ints (|values| <= 10^9).",
        "**Output:** One integer — the count (fits in 64 bits).",
        "",
        "**Example:** `3 2` / `1 3 5` / `2 4` -> `3` (3>2, 5>2, 5>4).",
    ),
    [
        contest_test("sample", T("3 2", "1 3 5", "2 4"), T("3"), "3>2, 5>2, 5>4."),
        contest_test("disjoint", T("2 2", "1 2", "3 4"), T("0"), "All of B beats all of A."),
        contest_test("equal values", T("2 2", "2 2", "2 2"), T("0"), "Strictly greater — equal pairs do not count."),
        contest_test("all less", T("2 2", "5 6", "1 2"), T("4"), "Every pair qualifies."),
        contest_test("single", T("1 1", "1", "2"), T("0"), "One comparison."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p17-distinct",
    "Longest All-Distinct Window",
    T(
        "**Description:** Print the length of the longest contiguous window with all",
        "distinct values.",
        "",
        "**Input:** Line 1: n (1 <= n <= 200000). Line 2: n integers (0 <= a[i] <= 10^6).",
        "**Output:** One integer — the longest all-distinct run.",
        "",
        "**Example:** `6` / `1 2 3 1 2 3` -> `3`.",
    ),
    [
        contest_test("sample", T("6", "1 2 3 1 2 3"), T("3"), "Any three consecutive."),
        contest_test("all same", T("4", "7 7 7 7"), T("1"), "A single element is trivially distinct."),
        contest_test("all distinct", T("5", "1 2 3 4 5"), T("5"), "Whole array."),
        contest_test("late repeat", T("5", "1 2 3 4 2"), T("4"), "Window 1 2 3 4 before the repeat."),
        contest_test("wrap repeat", T("6", "1 2 1 2 1 2"), T("2"), "Never three in a row."),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p17-subsum",
    "Shortest Subarray Sum",
    T(
        "**Description:** Non-negative integers only. Find the shortest contiguous subarray",
        "with sum at least S; print its length, or -1 if impossible.",
        "",
        "**Input:** Line 1: n S (1 <= n <= 200000, 1 <= S <= 10^18). Line 2: n integers",
        "(0 <= a[i] <= 10^9).",
        "**Output:** One integer — the shortest length or -1.",
        "",
        "**Example:** `6 8` / `2 3 1 2 4 3` -> `3` (2+4+... actually 4+3=7 no; 2+3+1+2=8 —",
        "wait: 1 2 4 sums 7; the minimal window is 2 3 1 2).",
    ),
    [
        contest_test("sample", T("6 8", "2 3 1 2 4 3"), T("3"),
                     "2+4+3 = 9 (length 3) beats 2+3+1+2 = 8 (length 4)."),
        contest_test("exact single", T("3 9", "9 1 1"), T("1"), "The 9 alone."),
        contest_test("impossible", T("3 100", "1 2 3"), T("-1"), "Total is 6."),
        contest_test("whole array", T("4 10", "3 3 3 3"), T("4"),
                     "3+3+3=9 < 10 — only the full window (12) qualifies."),
        contest_test("zeros", T("5 4", "0 4 0 0 0"), T("1"), "Zeros never help — window skips them."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p17-ksum",
    "Fixed Window Maximum Sum",
    T(
        "**Description:** Print the maximum sum of any k consecutive elements.",
        "",
        "**Input:** Line 1: n k (1 <= k <= n <= 200000). Line 2: n integers",
        "(|a[i]| <= 10^9).",
        "**Output:** One integer — the maximum window sum.",
        "",
        "**Example:** `6 3` / `2 1 5 1 3 2` -> `9` (5+1+3).",
    ),
    [
        contest_test("sample", T("6 3", "2 1 5 1 3 2"), T("9"), "5+1+3."),
        contest_test("k equals n", T("4 4", "1 2 3 4"), T("10"), "Only one window."),
        contest_test("negatives", T("5 2", "-1 -2 -3 -4 -5"), T("-3"), "Least negative pair."),
        contest_test("k 1", T("5 1", "4 -2 9 1 3"), T("9"), "Single best element."),
        contest_test("tail window", T("6 2", "1 1 1 1 1 100"), T("101"), "Best window touches the end."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p17-pair-sum": vi_challenge(
        "Tổng cặp đã sắp",
        T(
            "**Đề bài:** Trong mảng đã sắp n số nguyên, kết luận có hai phần tử ở vị trí",
            "KHÁC nhau có tổng đúng bằng S hay không.",
            "",
            "**Dữ liệu vào:** Dòng 1: n S (2 <= n <= 200000, |S| <= 10^18). Dòng 2: n số đã sắp",
            "(|a[i]| <= 10^9).",
            "**Dữ liệu ra:** In `YES` nếu tồn tại cặp, ngược lại `NO`.",
            "",
            "**Ví dụ:** `5 9` / `1 2 4 7 11` -> `YES` (2 + 7).",
        ),
        [
            ("sample", "2 + 7 = 9."),
            ("asymmetric move", "2+4: phải hạ r hai lần trong khi l đứng yên — code di-chuyển-cả-hai in NO."),
            ("duplicates", "Khác VỊ TRÍ, bằng giá trị — hai số 3."),
            ("negatives", "Các tổng cặp là -13, -8, -3 — không cặp nào bằng -5."),
            ("two elements", "Trái dấu gặp nhau."),
        ],
    ),
    "hsg-p17-merge": vi_challenge(
        "Đếm nghịch thế nhẹ",
        T(
            "**Đề bài:** Hai mảng đã sắp A (n) và B (m). Đếm cặp (i, j) với A[i] > B[j].",
            "",
            "**Dữ liệu vào:** Dòng 1: n m (1 <= n, m <= 200000). Dòng 2: n số đã sắp. Dòng 3:",
            "m số đã sắp (|giá trị| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — số cặp (vừa 64 bit).",
            "",
            "**Ví dụ:** `3 2` / `1 3 5` / `2 4` -> `3` (3>2, 5>2, 5>4).",
        ),
        [
            ("sample", "3>2, 5>2, 5>4."),
            ("disjoint", "Toàn bộ B thắng toàn bộ A."),
            ("equal values", "Lớn hơn NGHIÊM NGẶT — cặp bằng không đếm."),
            ("all less", "Mọi cặp đều đạt."),
            ("single", "Một phép so sánh."),
        ],
    ),
    "hsg-p17-distinct": vi_challenge(
        "Cửa sổ phân biệt dài nhất",
        T(
            "**Đề bài:** In độ dài cửa sổ liên tiếp dài nhất mà mọi giá trị đều phân biệt.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 200000). Dòng 2: n số nguyên (0 <= a[i] <= 10^6).",
            "**Dữ liệu ra:** Một số nguyên — đoạn phân biệt dài nhất.",
            "",
            "**Ví dụ:** `6` / `1 2 3 1 2 3` -> `3`.",
        ),
        [
            ("sample", "Ba phần tử liên tiếp bất kỳ."),
            ("all same", "Một phần tử hiển nhiên phân biệt."),
            ("all distinct", "Cả mảng."),
            ("late repeat", "Cửa sổ 1 2 3 4 trước lần lặp."),
            ("wrap repeat", "Không bao giờ ba phần tử liên tiếp khác nhau."),
        ],
    ),
    "hsg-p17-subsum": vi_challenge(
        "Đoạn con ngắn nhất",
        T(
            "**Đề bài:** Chỉ với số nguyên không âm. Tìm đoạn liên tiếp ngắn nhất có tổng ít",
            "nhất S; in độ dài, hoặc -1 nếu không thể.",
            "",
            "**Dữ liệu vào:** Dòng 1: n S (1 <= n <= 200000, 1 <= S <= 10^18). Dòng 2: n số",
            "(0 <= a[i] <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — độ dài ngắn nhất hoặc -1.",
            "",
            "**Ví dụ:** `6 8` / `2 3 1 2 4 3` -> `3`.",
        ),
        [
            ("sample", "2+4+3 = 9 (dài 3) thắng 2+3+1+2 = 8 (dài 4)."),
            ("exact single", "Riêng số 9."),
            ("impossible", "Tổng chỉ là 6."),
            ("whole array", "3+3+3=9 < 10 — chỉ cả cửa sổ (12) đạt."),
            ("zeros", "Số 0 không bao giờ giúp — cửa sổ bỏ qua chúng."),
        ],
    ),
    "hsg-p17-ksum": vi_challenge(
        "Tổng cố định lớn nhất",
        T(
            "**Đề bài:** In tổng lớn nhất của k phần tử liên tiếp.",
            "",
            "**Dữ liệu vào:** Dòng 1: n k (1 <= k <= n <= 200000). Dòng 2: n số nguyên",
            "(|a[i]| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — tổng cửa sổ lớn nhất.",
            "",
            "**Ví dụ:** `6 3` / `2 1 5 1 3 2` -> `9` (5+1+3).",
        ),
        [
            ("sample", "5+1+3."),
            ("k equals n", "Chỉ một cửa sổ."),
            ("negatives", "Cặp âm ít nhất."),
            ("k 1", "Phần tử tốt nhất."),
            ("tail window", "Cửa sổ tốt nhất chạm cuối mảng."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p17-tp",
    "Two Pointers Problem Set",
    "Sorted pair sums, cross-array counting, distinct windows, shortest subarray, fixed-window max.",
    "Bài tập hai con trỏ",
    "Tổng cặp đã sắp, đếm chéo mảng, cửa sổ phân biệt, đoạn ngắn nhất, cửa sổ cố định lớn nhất.",
    "hsg-m17-window",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p17-pair-sum",
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    int l = 0, r = n - 1;
    bool ok = false;
    while (l < r) {
        long long s = a[l] + a[r];
        if (s == S) { ok = true; break; }
        if (s < S) ++l; else --r;
    }
    out << (ok ? "YES" : "NO") << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    int l = 0, r = n - 1;
    bool ok = false;
    while (l < r) {
        long long s = a[l] + a[r];
        if (s == S) { ok = true; break; }
        // near-miss: both pointers move inward each step — skips the answer
        ++l; --r;
    }
    out << (ok ? "YES" : "NO") << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p17-merge",
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<long long> a(n), b(m);
    for (auto& x : a) in >> x;
    for (auto& x : b) in >> x;
    long long cnt = 0;
    int j = 0;
    for (int i = 0; i < n; ++i) {
        while (j < m && b[j] < a[i]) ++j;   // j only moves forward
        cnt += j;
    }
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, m; in >> n >> m;
    vector<long long> a(n), b(m);
    for (auto& x : a) in >> x;
    for (auto& x : b) in >> x;
    long long cnt = 0;
    // near-miss: counts A[i] >= B[j] — equal pairs wrongly included
    int j = 0;
    for (int i = 0; i < n; ++i) {
        while (j < m && b[j] <= a[i]) ++j;
        cnt += j;
    }
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p17-distinct",
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    vector<int> cnt(1000001, 0);
    int l = 0, best = 0;
    for (int r = 0; r < n; ++r) {
        ++cnt[a[r]];
        while (cnt[a[r]] > 1) --cnt[a[l++]];   // restore all-distinct
        best = max(best, r - l + 1);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<int> a(n);
    for (auto& x : a) in >> x;
    vector<int> cnt(1000001, 0);
    int l = 0, best = 0;
    for (int r = 0; r < n; ++r) {
        ++cnt[a[r]];
        // near-miss: records the window BEFORE restoring all-distinctness —
        // invalid windows inflate the answer
        best = max(best, r - l + 1);
        while (cnt[a[r]] > 1) --cnt[a[l++]];
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p17-subsum",
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long sum = 0;
    int l = 0, best = n + 1;
    for (int r = 0; r < n; ++r) {
        sum += a[r];
        while (sum - a[l] >= S && l <= r) { sum -= a[l]; ++l; }
        if (sum >= S) best = min(best, r - l + 1);
    }
    out << (best > n ? -1 : best) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long sum = 0;
    int l = 0, best = n + 1;
    for (int r = 0; r < n; ++r) {
        sum += a[r];
        if (sum >= S) best = min(best, r - l + 1);
        // near-miss: shrinks only when sum >= S + a[l] — leaves fat windows
        while (sum >= S && sum - a[l] >= 0 && l <= r) { sum -= a[l]; ++l; }
    }
    out << (best > n ? -1 : best) << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p17-ksum",
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long sum = 0;
    for (int i = 0; i < k; ++i) sum += a[i];
    long long best = sum;
    for (int r = k; r < n; ++r) {
        sum += a[r] - a[r - k];
        best = max(best, sum);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long sum = 0;
    for (int i = 0; i < k; ++i) sum += a[i];
    long long best = sum;
    for (int r = k; r < n; ++r) {
        // near-miss: adds the new element but forgets to drop the old one
        sum += a[r];
        best = max(best, sum);
    }
    out << best << "{{NL}}";
""") + END,
        ),
    ],
)

CH17 = challenge(
    "hsg-cp-m17-toys",
    "Toy Shelf",
    T(
        "**Description:** A shelf holds n toys in a row; toy i has type t[i] (1..100). Choose",
        "one contiguous segment containing at most k DISTINCT types, maximizing the number",
        "of toys taken.",
        "",
        "**Input:** Line 1: n k (1 <= n <= 200000, 1 <= k <= 100). Line 2: n integers",
        "(1 <= t[i] <= 100).",
        "**Output:** One integer — the maximum segment length.",
        "",
        "**Example:** `6 2` / `1 2 1 3 4 3` -> `3` (1 2 1 and 3 4 3 are the best",
        "2-distinct segments).",
    ),
    [
        contest_test("sample", T("6 2", "1 2 1 3 4 3"), T("3"),
                     "Best windows of 2 distinct types have length 3 (1 2 1 or 3 4 3)."),
        contest_test("all one type", T("5 1", "4 4 4 4 4"), T("5"), "Single type fills the shelf."),
        contest_test("k covers all", T("4 3", "1 2 3 1"), T("4"), "Three types fit everything."),
        contest_test("single toy", T("1 1", "7"), T("1"), "Trivial."),
        contest_test("alternating", T("6 1", "1 2 1 2 1 2"), T("1"),
                     "k=1 — every neighbor differs."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP17 = vi_challenge(
    "Kệ đồ chơi",
    T(
        "**Đề bài:** Một kệ chứa n đồ chơi xếp hàng; đồ chơi i có loại t[i] (1..100). Chọn",
        "một đoạn liên tiếp chứa tối đa k LOẠI phân biệt, sao cho số đồ chơi lấy được lớn",
        "nhất.",
        "",
        "**Dữ liệu vào:** Dòng 1: n k (1 <= n <= 200000, 1 <= k <= 100). Dòng 2: n số nguyên",
        "(1 <= t[i] <= 100).",
        "**Dữ liệu ra:** Một số nguyên — độ dài đoạn lớn nhất.",
        "",
        "**Ví dụ:** `6 2` / `1 2 1 3 4 3` -> `3` (các đoạn 1 2 1 hoặc 3 4 3).",
    ),
    [
        ("sample", "Các cửa sổ 2 loại tốt nhất dài 3 (1 2 1 hoặc 3 4 3)."),
        ("all one type", "Một loại phủ cả kệ."),
        ("k covers all", "Ba loại chứa hết."),
        ("single toy", "Tầm thường."),
        ("alternating", "k=1 — hai hàng xóm luôn khác."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m17",
    "Checkpoint — Two Pointers",
    "Pass the graded problem to finish the two-pointers module.",
    15,
    """**Checkpoint — hai con trỏ.** Pass the graded challenge below — it is
the classic at-most-k-distinct window: expand r, shrink l while distinct
types exceed k, track r - l + 1. The graded near-misses: shrinking only
once per step (l falls behind and the window stays invalid), and
counting types with a scan instead of a frequency array (O(n) per step
= TLE at n = 2*10^5).

**Điểm kiểm tra — hai con trỏ.** Pass bài chấm bên dưới — bài kinh
điển cửa-sổ-tối-đa-k-loại: mở rộng r, thu l trong khi số loại vượt k,
theo dõi r - l + 1. Các near-miss bị chấm: chỉ thu một lần mỗi bước
(l tụt lại và cửa sổ giữ trạng thái bất hợp lệ), và đếm loại bằng quét
thay vì bảng tần suất (O(n) mỗi bước = TLE tại n = 2*10^5).
""",
    "Checkpoint — Two Pointers",
    "Pass the graded problem to finish the two-pointers module.",
    """**Điểm kiểm tra — hai con trỏ.** Pass bài chấm bên dưới — bài kinh
điển cửa-sổ-tối-đa-k-loại: mở rộng r, thu l trong khi số loại vượt k,
theo dõi r - l + 1. Các near-miss bị chấm: chỉ thu một lần mỗi bước
(l tụt lại và cửa sổ giữ trạng thái bất hợp lệ), và đếm loại bằng quét
thay vì bảng tần suất (O(n) mỗi bước = TLE tại n = 2*10^5).
""",
    CH17,
    VI_CP17,
    solution=CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<int> t(n);
    for (auto& x : t) in >> x;
    vector<int> cnt(101, 0);
    int distinct = 0, l = 0, best = 0;
    for (int r = 0; r < n; ++r) {
        if (cnt[t[r]]++ == 0) ++distinct;
        while (distinct > k)
            if (--cnt[t[l++]] == 0) --distinct;
        best = max(best, r - l + 1);
    }
    out << best << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n, k; in >> n >> k;
    vector<int> t(n);
    for (auto& x : t) in >> x;
    vector<int> cnt(101, 0);
    int distinct = 0, l = 0, best = 0;
    for (int r = 0; r < n; ++r) {
        if (cnt[t[r]]++ == 0) ++distinct;
        // near-miss: records the window BEFORE restoring validity —
        // over-k windows inflate the answer
        best = max(best, r - l + 1);
        while (distinct > k)
            if (--cnt[t[l++]] == 0) --distinct;
    }
    out << best << "{{NL}}";
""") + END,
)

print("M17 done")
