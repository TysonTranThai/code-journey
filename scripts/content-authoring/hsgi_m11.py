#!/usr/bin/env python3
"""HSG Intermediate — Module 11: hsgi-seqdp (Sequence DP).

LIS O(n²) then O(n log n) patience, Kadane for max subarray with the
empty-prefix reset, LCS with rolling rows. The teaching spine: define the
state, derive the transition, then notice which dimension can die.

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

M = "hsgi-seqdp"
write_module(
    M,
    "Sequence DP — LIS, Kadane, LCS",
    "Three canonical sequence DPs: longest increasing subarray two ways, best contiguous sum with a one-line reset, and longest common subsequence with a rolling row.",
    "QHĐ dãy — LIS, Kadane, LCS",
    "Ba bài QHĐ dãy kinh điển: dãy con tăng dài nhất hai cách, tổng đoạn liên tiếp lớn nhất với phép reset một dòng, và dãy con chung dài nhất với hàng cuộn.",
    ["hsgi-m11-lis", "hsgi-m11-kadane-lcs", "hsgi-cp-m11"],
    ["hsgi-p11-seqdp"],
)

# ------------------------------------------------------------------ lesson 1
write_lesson(
    M,
    "hsgi-m11-lis",
    "Longest Increasing Subsequence — Two Speeds",
    "O(n²) DP where dp[i] ends at i; then the O(n log n) patience trick where tails[k] is the smallest possible tail of an increasing run of length k+1.",
    20,
    """## The state that works

LIS: chọn dãy con (giữ thứ tự, không cần liền) tăng dần dài nhất.

Định nghĩa dp[i] = độ dài dãy con tăng dài nhất KẾT THÚC tại i:

```cpp
for (int i = 0; i < n; ++i) {
    dp[i] = 1;                          // chỉ phần tử i
    for (int j = 0; j < i; ++j)
        if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
}
```

Đáp án = max(dp). O(n²) — đủ tới n ≈ 5000.

### The bottleneck

dp[i] cần max của dp[j] với a[j] < a[i] — hai điều kiện, một cái là VỊ
TRÍ (j < i), một là GIÁ TRỊ. O(n²) quét cả hai. Nhưng nếu duyệt i từ
trái sang phải, j < i tự động; chỉ còn điều kiện giá trị: max dp[j] với
a[j] < a[i] → là truy vấn tiền tố có điều kiện!

### Patience — O(n log n)

Giữ mảng tails: tails[k] = đuôi NHỎ NHẤT của dãy tăng dài k+1. Với mỗi
a[i]: chèn a[i] thay thế phần tử ĐẦU TIÊN ≥ a[i] (lower_bound). Độ dài
mảng = LIS:

```cpp
vector<int> tails;
for (int i = 0; i < n; ++i) {
    auto it = lower_bound(tails.begin(), tails.end(), a[i]);
    if (it == tails.end()) tails.push_back(a[i]);  // kéo dài
    else *it = a[i];                               // hạ đuôi
}
```

tails LUÔN tăng ngặt — bất biến này là chứng minh: mỗi lần thay thế chỉ
hạ đuôi của một độ dài, không phá tính tăng.

### Strict vs non-strict

`a[j] < a[i]` + lower_bound = TĂNG NGẶT. Dãy không giảm (cho phép bằng)
→ đổi lower_bound thành upper_bound, hoặc điều kiện thành a[j] <= a[i].
Đổi sai một chỗ → sai trên test có phần tử bằng.

### Which to write in contest

n ≤ 5000: O(n²) — ngắn, khó sai. n lớn: patience. Đọc ràng buộc TRƯỚC
khi chọn.

**Điểm mấu chốt:** dp[i] kết-thúc-tại-i là khung; patience = chuyển điều
kiện giá trị thành truy vấn nhị phân trên mảng tails tăng ngặt.""",
    "Dãy con tăng dài nhất — Hai tốc độ",
    "O(n²) với dp[i] kết thúc tại i; rồi thủ thuật patience O(n log n) với tails[k] là đuôi nhỏ nhất.",
    """## State đúng

LIS: dãy con tăng dài nhất (giữ thứ tự, không cần liền).

dp[i] = LIS KẾT THÚC tại i:

```cpp
for (int i = 0; i < n; ++i) {
    dp[i] = 1;
    for (int j = 0; j < i; ++j)
        if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
}
```

Đáp án = max(dp). O(n²) — đủ tới n ≈ 5000.

### Nút cổ chai

dp[i] cần max dp[j] với a[j] < a[i] — hai điều kiện: VỊ TRÍ và GIÁ
TRỊ. Duyệt trái→phải thì j < i tự động; còn lại truy vấn max có điều
kiện giá trị → nhị phân!

### Patience — O(n log n)

tails[k] = đuôi NHỎ NHẤT của dãy tăng dài k+1. Với a[i]: lower_bound,
không có thì push, có thì thay:

```cpp
vector<int> tails;
for (int i = 0; i < n; ++i) {
    auto it = lower_bound(tails.begin(), tails.end(), a[i]);
    if (it == tails.end()) tails.push_back(a[i]);
    else *it = a[i];
}
```

tails tăng ngặt — bất biến: thay thế chỉ hạ đuôi, không phá tính tăng.

### Ngặt vs không ngặt

`a[j] < a[i]` + lower_bound = TĂNG NGẶT. Cho phép bằng → upper_bound.
Đổi sai → sai trên test có phần tử bằng.

### Chọn trong contest

n ≤ 5000: O(n²) — ngắn, khó sai. n lớn: patience. Đọc ràng buộc trước.

**Điểm mấu chốt:** dp[i] kết-thúc-tại-i; patience = nhị phân trên
tails tăng ngặt.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ lesson 2
write_lesson(
    M,
    "hsgi-m11-kadane-lcs",
    "Kadane and LCS — Reset and Roll",
    "Kadane's one-line decision (extend or restart) and LCS with two rows instead of a full table.",
    20,
    """## Kadane — tổng đoạn liên tiếp lớn nhất

best(i) = tổng đoạn lớn nhất KẾT THÚC tại i. Mỗi bước một quyết định:
nối vào đoạn trước (best(i-1) + a[i]) hay khởi động lại (a[i]):

```cpp
long long best = a[0], cur = a[0];
for (int i = 1; i < n; ++i) {
    cur = max((long long)a[i], cur + a[i]);   // nối hay khởi động lại
    best = max(best, cur);
}
```

Lỗi kinh điển: khởi tạo best = 0. Nếu MỌI phần tử âm (cho phép), đáp án
là phần tử ít âm nhất — KHÔNG phải 0, trừ khi đề cho phép đoạn rỗng.
Đọc kỹ: "đoạn rỗng có được chọn không?"

### LCS — bảng đầy đủ thì chết

dp[i][j] = LCS của tiền tố a[0..i) và b[0..j):

- a[i-1] == b[j-1]: dp = dp[i-1][j-1] + 1
- khác: dp = max(dp[i-1][j], dp[i][j-1])

Bảng n×m với n = m = 5000 → 25 triệu long long ≈ 200 MB: quá bộ nhớ
2 − 256 MB tùy judge. Nhìn chuyển trạng thái: hàng i chỉ đọc hàng i−1
→ giữ HAI hàng (cuộn):

```cpp
vector<long long> prev(m + 1), cur(m + 1);
for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
        if (a[i-1] == b[j-1]) cur[j] = prev[j-1] + 1;
        else cur[j] = max(prev[j], cur[j-1]);
    }
    swap(prev, cur);      // hàng cũ thành hàng trước
}
```

Đáp án = prev[m] sau vòng lặp. O(n·m) thời gian, O(m) bộ nhớ.

### Nhận diện

- "đoạn liên tiếp, tổng lớn nhất" → Kadane.
- "dãy con chung" hai chuỗi → LCS.
- Khối lượng n·m tới 25 triệu là bình thường cho thời gian; chỉ bộ nhớ
  mới buộc cuộn hàng.

**Điểm mấu chốt:** Kadane = max(nối, khởi động lại); LCS = hai hàng là
đủ — thời gian giữ nguyên, bộ nhớ giảm n lần.""",
    "Kadane và LCS — Reset và cuộn hàng",
    "Kadane: nối hay khởi động lại mỗi bước. LCS: hai hàng thay bảng đầy đủ.",
    """## Kadane — tổng đoạn liên tiếp lớn nhất

best(i) = tổng đoạn lớn nhất KẾT THÚC tại i. Nối hay khởi động lại:

```cpp
long long best = a[0], cur = a[0];
for (int i = 1; i < n; ++i) {
    cur = max((long long)a[i], cur + a[i]);
    best = max(best, cur);
}
```

Lỗi kinh điển: best = 0. Mọi phần tử âm → đáp án là phần tử ít âm nhất,
KHÔNG phải 0 (trừ khi đề cho đoạn rỗng). Đọc kỹ phát biểu.

### LCS — bảng đầy đủ thì chết

dp[i][j] = LCS của a[0..i), b[0..j):

- bằng: dp = dp[i-1][j-1] + 1
- khác: dp = max(dp[i-1][j], dp[i][j-1])

5000×5000 long long ≈ 200 MB: chết bộ nhớ. Hàng i chỉ đọc hàng i−1 →
cuộn HAI hàng:

```cpp
vector<long long> prev(m + 1), cur(m + 1);
for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
        if (a[i-1] == b[j-1]) cur[j] = prev[j-1] + 1;
        else cur[j] = max(prev[j], cur[j-1]);
    }
    swap(prev, cur);
}
```

Đáp án = prev[m]. O(n·m) thời gian, O(m) bộ nhớ.

### Nhận diện

- "đoạn liên tiếp, tổng lớn nhất" → Kadane.
- "dãy con chung" → LCS.
- n·m = 25 triệu OK thời gian; bộ nhớ mới buộc cuộn.

**Điểm mấu chốt:** Kadane = max(nối, restart); LCS = hai hàng đủ.""",
    difficulty="intermediate",
)

# ------------------------------------------------------------------ practice
A1 = challenge(
    "hsgi-p11-lis",
    "Dãy tăng dài nhất",
    """**Bài toán.** Dãy n số nguyên a_i. In độ dài dãy con TĂNG NGẶT dài
nhất (giữ thứ tự, không cần liền).

**Ràng buộc:** 1 ≤ n ≤ 100 000; |a_i| ≤ 10^9.

n lớn: cần O(n log n) — O(n²) sẽ quá hạn.""",
    [
        contest_test(
            "ví dụ",
            T("6", "1 3 2 4 3 5"),
            T("4"),
            "1, 2 (hoặc 3), 4, 5 → độ dài 4.",
        ),
        contest_test(
            "một phần tử",
            T("1", "7"),
            T("1"),
            "Dãy con một phần tử luôn hợp lệ.",
        ),
        contest_test(
            "giảm dần",
            T("4", "9 7 5 3"),
            T("1"),
            "Không cặp nào tăng: LIS = 1.",
        ),
        contest_test(
            "phần tử bằng — ngặt",
            T("6", "2 2 2 2 2 2"),
            T("1"),
            "TĂNG NGẶT: phần tử bằng không nối được — upper_bound sẽ trả 6, sai.",
        ),
        contest_test(
            "n lớn — tăng thật",
            T("100000") + T(*[str(i) for i in range(1, 100001)]),
            T("100000"),
            "Dãy tăng trọn: LIS = n — patience chạy một lượt O(n log n).",
        ),
        contest_test(
            "n lớn — sườn núi",
            T("100000") + T(*[str(i) for i in range(1, 50001)] + [str(100001 - i) for i in range(1, 50001)]),
            T("50001"),
            "1..50000 rồi 100000, 99999, ...: dãy 1..50000,100000 dài 50001 — W O(n²) trên 100 000 phần tử sẽ chết thời gian.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

A2 = challenge(
    "hsgi-p11-kadane",
    "Tổng đoạn lớn nhất",
    """**Bài toán.** Dãy n số nguyên a_i (CÓ THỂ ÂM). In tổng lớn nhất của
một ĐOẠN LIÊN TIẾP không rỗng.

**Ràng buộc:** 1 ≤ n ≤ 200 000; |a_i| ≤ 10^9.

Tổng tới 2·10^14 — long long.""",
    [
        contest_test(
            "ví dụ",
            T("8", "-2 1 -3 4 -1 2 1 -5"),
            T("6"),
            "Đoạn 4, -1, 2, 1 → tổng 6.",
        ),
        contest_test(
            "mọi phần tử âm",
            T("4", "-8 -3 -6 -1"),
            T("-1"),
            "Không có đoạn rỗng: chọn phần tử ít âm nhất (-1) — best khởi tạo 0 sẽ trả 0, SAI.",
        ),
        contest_test(
            "một phần tử",
            T("1", "-5"),
            T("-5"),
            "Đoạn duy nhất là chính nó.",
        ),
        contest_test(
            "n lớn — xen kẽ",
            T("200000") + T(*[("1000000000" if i % 2 == 0 else "-999999999") for i in range(200000)]),
            T("1000099999"),
            "Đoạn từ dương đầu: 100000×10^9 − 99999×999999999 = 10^9 + 99999×1 = 1000099999 — mỗi cặp (âm, dương) ròng +1.",
        ),
        contest_test(
            "n lớn — toàn dương",
            T("200000") + T(*["1000000000"] * 200000),
            T("200000000000000"),
            "Cả dãy: 2·10^14 — Kadane giữ nguyên đoạn, long long.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A3 = challenge(
    "hsgi-p11-lcs",
    "Dãy con chung dài nhất",
    """**Bài toán.** Hai chuỗi A, B (chữ thường). In độ dài dãy con chung
dài nhất (giữ thứ tự).

**Ràng buộc:** 1 ≤ |A|, |B| ≤ 5000.

Bảng đầy đủ ~25 MB int là ổn, nhưng long long n×m thì không — cuộn hai
hàng an toàn tuyệt đối.""",
    [
        contest_test(
            "ví dụ",
            T("abcde", "ace"),
            T("3"),
            "a, c, e — độ dài 3.",
        ),
        contest_test(
            "không chung",
            T("abc", "def"),
            T("0"),
            "Không ký tự chung: LCS = 0.",
        ),
        contest_test(
            "bằng nhau",
            T("xaydung", "xaydung"),
            T("7"),
            "Hai chuỗi giống nhau: LCS = độ dài.",
        ),
        contest_test(
            "xen kẽ",
            T("abcdgh", "aedfhr"),
            T("3"),
            "Kinh điển: a, d, h → 3.",
        ),
        contest_test(
            "n lớn — đan xen",
            T("ab" * 2500, "ba" * 2500),
            T("4999"),
            "abab… và baba…: LCS = 4999 (bỏ ký tự đầu A và cuối B) — 5000×5000 bảng phải cuộn nếu dùng long long.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsgi-p11-liscount",
    "Đếm dãy tăng dài nhất",
    """**Bài toán.** Dãy n số nguyên. In SỐ dãy con tăng ngặt dài nhất
(theo mô-đun 10^9 + 7).

**Ràng buộc:** 1 ≤ n ≤ 5000; |a_i| ≤ 10^9.

n ≤ 5000: O(n²) đủ. Giữ kèm cnt[] — số cách đạt dp[j].""",
    [
        contest_test(
            "ví dụ",
            T("5", "1 3 5 4 7"),
            T("2"),
            "LIS dài 4: 1,3,5,7 và 1,3,4,7 — hai cách.",
        ),
        contest_test(
            "một phần tử",
            T("1", "9"),
            T("1"),
            "Một cách duy nhất.",
        ),
        contest_test(
            "giảm dần",
            T("3", "5 4 3"),
            T("3"),
            "LIS = 1: mỗi phần tử tự nó — ba cách.",
        ),
        contest_test(
            "tăng trọn",
            T("4", "1 2 3 4"),
            T("1"),
            "Dãy tăng: chỉ một cách đạt độ dài 4.",
        ),
        contest_test(
            "bằng nhau cạnh nhau",
            T("4", "2 2 3 3"),
            T("4"),
            "Ngặt: LIS = 2 (2,3); hai vị trí 2 × hai vị trí 3 = 4 cách — nhánh cộng-khi-bằng phải chạy.",
        ),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsgi-p11-maxrun",
    "Đoạn không âm dài nhất",
    """**Bài toán.** Dãy n số nguyên. In độ dài đoạn LIÊN TIẾP dài nhất mà
TỔNG ≥ 0. Không có → in 0.

**Ràng buộc:** 1 ≤ n ≤ 200 000; |a_i| ≤ 10^9.

Tiền tố P: đoạn (l, r] tổng ≥ 0 ⇔ P[r] ≥ P[l] — giữ danh sách ứng viên
P GIẢM NGẶT (prefix-minima) và nhị phân tìm l nhỏ nhất cho mỗi r: O(n log n).""",
    [
        contest_test(
            "ví dụ",
            T("5", "1 -1 1 -1 1"),
            T("5"),
            "Tổng cả dãy = 1 ≥ 0: cả 5 phần tử.",
        ),
        contest_test(
            "tất cả âm",
            T("3", "-5 -2 -9"),
            T("0"),
            "Không đoạn nào tổng ≥ 0.",
        ),
        contest_test(
            "một phần tử không âm",
            T("1", "0"),
            T("1"),
            "Tổng 0 ≥ 0: độ dài 1.",
        ),
        contest_test(
            "đoạn giữa",
            T("6", "-3 2 2 -1 2 -6"),
            T("5"),
            "Đoạn 1..5 = −3+2+2−1+2 = 2 ≥ 0 dài 5 — l=0 (P=0) là candidate dù P sau đó có số âm.",
        ),
        contest_test(
            "n lớn — toàn −1",
            T("200000") + T(*["-1"] * 200000),
            T("0"),
            "Tiền tố giảm liên tục: không l nào usable — R nhị phân O(n log n) chạy tức thì; W O(n²) quét toàn bộ mỗi r sẽ chết thời gian.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI11 = {
    "hsgi-p11-lis": vi_challenge(
        "Dãy tăng dài nhất",
        """**Bài toán.** Dãy n số: in độ dài dãy con TĂNG NGẶT dài nhất.

n ≤ 100 000: cần patience O(n log n).""",
        [("ví dụ", "1 3 2 4 3 5 → 4."),
         ("bằng nhau", "2 2 2 → 1 (ngặt!)."),
         ("n lớn", "lower_bound trên tails.")],
    ),
    "hsgi-p11-kadane": vi_challenge(
        "Tổng đoạn lớn nhất",
        """**Bài toán.** Tổng lớn nhất của đoạn liên tiếp KHÔNG RỖNG; dãy có
thể toàn âm. long long!""",
        [("mọi âm", "-8 -3 -6 -1 → -1, không phải 0."),
         ("n lớn", "2·10^14 — long long.")],
    ),
    "hsgi-p11-lcs": vi_challenge(
        "Dãy con chung dài nhất",
        """**Bài toán.** Hai chuỗi thường: in độ dài dãy con chung dài nhất.""",
        [("ví dụ", "abcde/ace → 3."),
         ("n lớn", "5000×5000: cuộn hai hàng.")],
    ),
    "hsgi-p11-liscount": vi_challenge(
        "Đếm dãy tăng dài nhất",
        """**Bài toán.** Đếm SỐ dãy con tăng ngặt dài nhất, mô-đun 10^9 + 7.
n ≤ 5000: O(n²).""",
        [("ví dụ", "1 3 5 4 7 → 2."),
         ("giảm dần", "Mỗi phần tử tự nó: n cách.")],
    ),
    "hsgi-p11-maxrun": vi_challenge(
        "Đoạn không âm dài nhất",
        """**Bài toán.** Đoạn liên tiếp dài nhất có tổng ≥ 0; không có in 0.""",
        [("ví dụ", "1 -1 1 -1 1 → 5."),
         ("tất cả âm", "→ 0."),
         ("kỹ thuật", "Tiền tố + min-stack từ phải.")],
    ),
}

write_practice(
    M,
    "hsgi-p11-seqdp",
    "Sequence DP Problem Set",
    "Five problems: LIS two-speed, Kadane, LCS, counting LIS, longest non-negative-sum run.",
    "Bài tập QHĐ dãy",
    "Năm bài: LIS hai tốc độ, Kadane, LCS, đếm LIS, đoạn tổng không âm dài nhất.",
    "hsgi-m11-kadane-lcs",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI11,
    solutions=[
        (
            "hsgi-p11-lis",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> tails;
    for (int i = 0; i < n; ++i) {
        auto it = lower_bound(tails.begin(), tails.end(), a[i]);
        if (it == tails.end()) tails.push_back(a[i]);
        else *it = a[i];
    }
    out << tails.size() << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // near-miss: O(n²) đúng kết quả nhưng QUÁ HẠN trên n = 100 000 —
    // đúng giới hạn "kỹ thuật" mà module dạy
    vector<int> dp(n, 1);
    int best = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j)
            if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
        best = max(best, dp[i]);
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p11-kadane",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long best = a[0], cur = a[0];
    for (int i = 1; i < n; ++i) {
        cur = max(a[i], cur + a[i]);
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long best = 0, cur = 0;   // near-miss: khởi tạo 0 — toàn âm
    // thì trả 0 thay vì phần tử ít âm nhất (đoạn phải KHÔNG RỖNG)
    for (int i = 0; i < n; ++i) {
        cur = max(a[i], cur + a[i]);
        best = max(best, cur);
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p11-lcs",
            CPP_STD + cpp("""    string a, b; in >> a >> b;
    int n = a.size(), m = b.size();
    vector<long long> prev(m + 1, 0), cur(m + 1, 0);
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i-1] == b[j-1]) cur[j] = prev[j-1] + 1;
            else cur[j] = max(prev[j], cur[j-1]);
        }
        swap(prev, cur);
    }
    out << prev[m] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    string a, b; in >> a >> b;
    int n = a.size(), m = b.size();
    // near-miss: cuộn hàng nhưng QUÊN swap — prev không bao giờ nhận kết
    // quả hàng trước, mọi dp tính trên prev toàn 0 → luôn in 0
    vector<long long> prev(m + 1, 0), cur(m + 1, 0);
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i-1] == b[j-1]) cur[j] = prev[j-1] + 1;
            else cur[j] = max(prev[j], cur[j-1]);
        }
    }
    out << cur[m] << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p11-liscount",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    const long long MOD = 1000000007;
    vector<long long> dp(n, 1), cnt(n, 1);
    long long best = 1, total = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j)
            if (a[j] < a[i]) {
                if (dp[j] + 1 > dp[i]) { dp[i] = dp[j] + 1; cnt[i] = cnt[j]; }
                else if (dp[j] + 1 == dp[i]) cnt[i] = (cnt[i] + cnt[j]) % MOD;
            }
        if (dp[i] > best) best = dp[i];
    }
    for (int i = 0; i < n; ++i)
        if (dp[i] == best) total = (total + cnt[i]) % MOD;
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    const long long MOD = 1000000007;
    vector<long long> dp(n, 1), cnt(n, 1);
    long long best = 1, total = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j)
            if (a[j] < a[i]) {
                // near-miss: KHÔNG cộng khi bằng — chỉ ghi đè; các cách
                // đạt cùng độ dài bị mất (test 1 3 5 4 7 trả 1 thay vì 2)
                if (dp[j] + 1 > dp[i]) { dp[i] = dp[j] + 1; cnt[i] = cnt[j]; }
            }
        if (dp[i] > best) best = dp[i];
    }
    for (int i = 0; i < n; ++i)
        if (dp[i] == best) total = (total + cnt[i]) % MOD;
    out << total << "{{NL}}";
""") + END,
        ),
        (
            "hsgi-p11-maxrun",
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // tiền tố P[0..n]; đoạn (l, r] tổng ≥ 0 ⇔ P[r] ≥ P[l]
    vector<long long> P(n + 1, 0);
    for (int i = 0; i < n; ++i) P[i+1] = P[i] + a[i];
    // prefix-minima: cand = chỉ số l sao cho P[l] < mọi P[k] với l < k ≤ n (danh sách P GIẢM)
    // với mỗi r: nhị phân cand để lấy l NHỎ NHẤT có P[l] ≤ P[r]
    vector<int> cand;
    for (int i = 0; i <= n; ++i) {
        if (cand.empty() || P[cand.back()] > P[i]) cand.push_back(i);
    }
    int best = 0;
    for (int r = 1; r <= n; ++r) {
        // cand có P giảm; cần phần tử ĐẦU (l nhỏ nhất) có P[l] ≤ P[r]
        int lo = 0, hi = (int)cand.size() - 1, pos = -1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (P[cand[mid]] <= P[r]) { pos = cand[mid]; hi = mid - 1; }
            else lo = mid + 1;
        }
        if (pos >= 0 && pos < r) best = max(best, r - pos);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // near-miss: hai vòng lồng O(n²) — đúng kết quả, quá hạn n = 200 000
    vector<long long> P(n + 1, 0);
    for (int i = 0; i < n; ++i) P[i+1] = P[i] + a[i];
    int best = 0;
    for (int r = 1; r <= n; ++r)
        for (int l = 0; l < r; ++l)
            if (P[l] <= P[r]) { best = max(best, r - l); break; }
    out << best << "{{NL}}";
""") + END,
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CH11 = challenge(
    "hsgi-cp-m11-balcony",
    "Checkpoint — Ban công hoa",
    """**Bài toán.** Một dãy n chậu hoa, chậu i có chiều cao h_i. Đội lần
ông chọn một dãy con chậu GIỮ NGUYÊN THỨ TỰ sao chiều cao TĂNG NGẶT từ
trái sang phải, và số chậu NHIỀU NHẤT. In (số chậu, số CÁCH chọn đạt
số chậu đó) trên hai dòng, số cách mô-đun 10^9 + 7.

**Ràng buộc:** 1 ≤ n ≤ 5000; 1 ≤ h_i ≤ 10^9.""",
    [
        contest_test(
            "ví dụ",
            T("5", "1 3 5 4 7"),
            T("4", "2"),
            "LIS dài 4 (1,3,5,7 và 1,3,4,7): in 4 rồi 2.",
        ),
        contest_test(
            "một chậu",
            T("1", "5"),
            T("1", "1"),
            "Một chậu: độ dài 1, một cách.",
        ),
        contest_test(
            "bằng nhau toàn bộ",
            T("4", "6 6 6 6"),
            T("1", "4"),
            "Ngặt: LIS = 1, bốn cách (bốn chậu).",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CP11 = vi_challenge(
    "Checkpoint — Ban công hoa",
    """**Bài toán.** Chọn dãy con tăng ngặt dài nhất; in độ dài rồi số cách
(mô-đun 10^9 + 7).""",
    [("ví dụ", "4 rồi 2."),
     ("bằng nhau", "1 rồi 4.")],
)

write_checkpoint(
    M,
    "hsgi-cp-m11",
    "Checkpoint — Sequence DP",
    "Pass the graded problem to finish the sequence DP module.",
    25,
    """**Checkpoint — Sequence DP.** Pass the graded challenge: LIS length
AND count together — dp for length, cnt for ways, sum cnt over all
positions achieving the maximum. The two-line output catches solutions
that compute only one of the two, and the all-equal test catches the
missing equal-length merge.

**Điểm kiểm tra — QHĐ dãy.** Pass bài chấm: LIS độ dài VÀ số cách —
dp cho độ dài, cnt cho số cách, cộng cnt tại mọi vị trí đạt max. Hai
dòng đầu ra "bắt" lời giải chỉ tính một trong hai; test toàn bằng
"bắt" thiếu phép cộng khi bằng độ dài.""",
    "Checkpoint — Sequence DP",
    "Pass bài chấm để hoàn thành module QHĐ dãy.",
    """**Điểm kiểm tra — QHĐ dãy.** Pass bài chấm bên dưới: LIS độ dài và
số cách (hai dòng, mô-đun 10^9 + 7).""",
    CH11,
    VI_CP11,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    const long long MOD = 1000000007;
    vector<long long> dp(n, 1), cnt(n, 1);
    long long best = 1;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j)
            if (h[j] < h[i]) {
                if (dp[j] + 1 > dp[i]) { dp[i] = dp[j] + 1; cnt[i] = cnt[j]; }
                else if (dp[j] + 1 == dp[i]) cnt[i] = (cnt[i] + cnt[j]) % MOD;
            }
        best = max(best, dp[i]);
    }
    long long total = 0;
    for (int i = 0; i < n; ++i)
        if (dp[i] == best) total = (total + cnt[i]) % MOD;
    out << best << "{{NL}}" << total << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> h(n);
    for (auto& x : h) in >> x;
    const long long MOD = 1000000007;
    vector<long long> dp(n, 1), cnt(n, 1);
    long long best = 1;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j)
            if (h[j] < h[i]) {
                // near-miss: bỏ nhánh cộng khi BẰNG độ dài — cnt chỉ ghi
                // đè, mất các cách song song (test 1 3 5 4 7 trả 1 thay 2)
                if (dp[j] + 1 > dp[i]) { dp[i] = dp[j] + 1; cnt[i] = cnt[j]; }
            }
        best = max(best, dp[i]);
    }
    long long total = 0;
    for (int i = 0; i < n; ++i)
        if (dp[i] == best) total = (total + cnt[i]) % MOD;
    out << best << "{{NL}}" << total << "{{NL}}";
""") + END,
)
