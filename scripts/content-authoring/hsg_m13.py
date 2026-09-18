#!/usr/bin/env python3
"""HSG — Module 13: hsg-recursion (đệ quy).

Base case discipline, tracing the call stack, n-choose-k by Pascal,
collatz steps, digit reversal, recursive subset sums. Conventions: T()
for test I/O, cpp() for bodies.
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

M = "hsg-recursion"
write_module(
    M,
    "Recursion",
    "Functions that call themselves: base cases, tracing the stack, factorial and combination identities, recursive number tricks.",
    "Đệ quy",
    "Hàm gọi chính nó: trường hợp cơ sở, vết ngăn xếp, giai thừa và hằng thức tổ hợp, mẹo số học đệ quy.",
    ["hsg-m13-basics", "hsg-m13-patterns", "hsg-cp-m13"],
    ["hsg-p13-recursion"],
)

write_lesson(
    M,
    "hsg-m13-basics",
    "Recursion Mechanics",
    "A base case that fires, a recursive case that shrinks — and why both are non-negotiable.",
    14,
    """## The two halves of every recursive function

```cpp
long long fact(int n) {
    if (n <= 1) return 1;        // base case: STOP
    return n * fact(n - 1);      // recursive case: SHRINK toward it
}
```

- The base case answers the smallest input directly, no self-call.
- The recursive case must make progress: every call moves the argument
  closer to a base case. `fact(n)` calling `fact(n)` is infinite
  recursion — stack overflow.

### Tracing fact(4)

```
fact(4) = 4 * fact(3)
        = 4 * (3 * fact(2))
        = 4 * (3 * (2 * fact(1)))
        = 4 * (3 * (2 * 1)) = 24
```

The calls stack up until the base case, then **unwind** multiplying.
Each frame holds its own `n` — that is where the memory goes: depth d
means d live frames.

### The stack limit

Every call pushes a frame (locals, return address). Default stacks hold
roughly 10^5 - 10^6 frames; a recursion on n = 10^6 risks stack
overflow (crash = runtime error, not TLE). Beginner answers: recurse on
values that halve or shrink by 1 with small n, or convert to a loop.

### Recursion vs iteration

`fact` is a loop in disguise — recursion buys clarity for tree-shaped
problems (subsets, backtracking, divide and conquer) and buys nothing
for a straight line of arithmetic. Both are correct; choose by shape.
""",
    "Cơ chế đệ quy",
    "Một trường hợp cơ sở phải kích hoạt, một trường hợp đệ quy phải thu nhỏ — và vì sao cả hai đều bắt buộc.",
    """## Hai nửa của mọi hàm đệ quy

```cpp
long long fact(int n) {
    if (n <= 1) return 1;        // trường hợp cơ sở: DỪNG
    return n * fact(n - 1);      // trường hợp đệ quy: THU NHỎ về nó
}
```

- Trường hợp cơ sở trả lời input nhỏ nhất trực tiếp, không tự gọi.
- Trường hợp đệ quy phải tiến bộ: mỗi lời gọi đưa tham số gần một
  trường hợp cơ sở hơn. `fact(n)` gọi `fact(n)` là đệ quy vô hạn —
  tràn ngăn xếp.

### Vết fact(4)

```
fact(4) = 4 * fact(3)
        = 4 * (3 * fact(2))
        = 4 * (3 * (2 * fact(1)))
        = 4 * (3 * (2 * 1)) = 24
```

Các lời gọi xếp chồng tới khi cơ sở kích hoạt, rồi **tan xuống** nhân
ngược. Mỗi khung giữ `n` riêng — đó là nơi bộ nhớ đi: sâu d nghĩa là d
khung đang sống.

### Giới hạn ngăn xếp

Mỗi lời gọi đẩy một khung (biến cục bộ, địa chỉ trả về). Ngăn xếp mặc
định chứa cỡ 10^5 - 10^6 khung; đệ quy trên n = 10^6 dễ tràn (crash =
runtime error, không phải TLE). Câu trả lời cho người mới: đệ quy trên
giá trị chia đôi hoặc giảm 1 với n nhỏ, hoặc chuyển thành vòng lặp.

### Đệ quy vs vòng lặp

`fact` là vòng lặp đội lốt đệ quy — đệ quy mua sự rõ ràng cho bài dạng
cây (tập con, quay lui, chia để trị) và không mua gì cho một đường thẳng
số học. Cả hai đều đúng; chọn theo dạng.
""",
)

write_lesson(
    M,
    "hsg-m13-patterns",
    "Recursive Patterns",
    "Combination identities, digit recursion, and the mutual shrink of gcd — three patterns that carry most beginner recursive problems.",
    13,
    """## C(n, k) by Pascal's identity

```cpp
long long C(int n, int k) {
    if (k == 0 || k == n) return 1;          // base cases
    return C(n - 1, k - 1) + C(n - 1, k);    // Pascal: with/without item n
}
```

`C(n-1, k-1)`: choose the n-th item; `C(n-1, k)`: skip it. Termination
is real: both n and k shrink. The plain version recomputes wildly
(O(2^n)) — fine for n <= 25, fatal beyond; a memo table makes it
O(n*k). Beginner rule: state the growth honestly, then memoize if the
constraints demand it.

## Digit recursion

```cpp
long long rev(long long n, long long acc = 0) {
    if (n == 0) return acc;
    return rev(n / 10, acc * 10 + n % 10);
}
```

The accumulator carries the result built so far; the argument shrinks
by a factor of 10 per call — depth is only the digit count. Same shape
works for digit sums, counting zeros, "is the number a palindrome?".

## gcd is recursion you already know

```cpp
long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}
```

Euclid in recursive form: the base case is b == 0, the shrink is a % b.
Many loops are recursive calls wearing different syntax.

## Thinking in contracts

Write a one-line comment: "fact(n) returns n! for n >= 0." Then trust
the recursive call to satisfy the contract on the smaller input — that
is the induction mindset, and it is the only way recursive code stays
readable at depth.
""",
    "Các mẫu đệ quy",
    "Hằng thức tổ hợp, đệ quy chữ số, và sự thu nhỏ lẫn nhau của gcd — ba mẫu gánh hầu hết bài đệ quy trình độ nhập môn.",
    """## C(n, k) theo hằng thức Pascal

```cpp
long long C(int n, int k) {
    if (k == 0 || k == n) return 1;          // trường hợp cơ sở
    return C(n - 1, k - 1) + C(n - 1, k);    // Pascal: chọn/không chọn phần tử n
}
```

`C(n-1, k-1)`: chọn phần tử thứ n; `C(n-1, k)`: bỏ qua nó. Dừng là có
thật: cả n và k đều thu nhỏ. Bản thuần tính lại đi tính lại (O(2^n)) —
ổn với n <= 25, chết ngoài đó; bảng memo hóa đưa về O(n*k). Quy tắc
người mới: nêu rõ tốc độ tăng trưởng, rồi memo nếu giới hạn đòi hỏi.

## Đệ quy chữ số

```cpp
long long rev(long long n, long long acc = 0) {
    if (n == 0) return acc;
    return rev(n / 10, acc * 10 + n % 10);
}
```

Biến tích lũy mang kết quả đã dựng; tham số thu nhỏ 10 lần mỗi lời gọi —
độ sâu chỉ bằng số chữ số. Cùng hình dạng cho tổng chữ số, đếm số 0,
"số có đối xứng không?".

## gcd chính là đệ quy bạn đã biết

```cpp
long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}
```

Euclid dạng đệ quy: cơ sở là b == 0, phần thu nhỏ là a % b. Nhiều vòng
lặp là các lời gọi đệ quy đội lốt cú pháp khác.

## Tư duy theo hợp đồng

Viết chú thích một dòng: "fact(n) trả n! với n >= 0." Rồi tin lời gọi
đệ quy sẽ thỏa hợp đồng trên input nhỏ hơn — đó là tư duy quy nạp, và
là cách duy nhất giữ code đệ quy dễ đọc khi sâu.
""",
)

A1 = challenge(
    "hsg-p13-factorial",
    "Factorial Trailing Zeros",
    T(
        "**Description:** Compute n! and count how many trailing zeros it has. 1 <= n <= 20",
        "(20! fits in a 64-bit integer).",
        "",
        "**Input:** One line: n (1 <= n <= 20).",
        "**Output:** Line 1: n!. Line 2: the number of trailing zeros.",
        "",
        "**Example:** `10` -> `3628800` / `2`.",
    ),
    [
        contest_test("sample", T("10"), T("3628800", "2"),
                     "10! = 3628800 ends in two zeros."),
        contest_test("small", T("5"), T("120", "1"),
                     "5! = 120 — one zero."),
        contest_test("no zero", T("4"), T("24", "0"),
                     "4! = 24 has no factor of 10."),
        contest_test("max", T("20"), T("2432902008176640000", "4"),
                     "20! = 2432902008176640000 — four zeros, and a reason to use long long."),
    ],
    level="imitation",
    difficulty="beginner",
)

A2 = challenge(
    "hsg-p13-combinations",
    "Choose the Team",
    T(
        "**Description:** Count the ways to choose k people from n (order does not matter).",
        "Compute C(n, k) exactly; the answer fits in 64 bits for these constraints",
        "(1 <= k <= n <= 40).",
        "",
        "**Input:** One line: n k (1 <= k <= n <= 40).",
        "**Output:** One integer — C(n, k).",
        "",
        "**Example:** `5 2` -> `10`.",
    ),
    [
        contest_test("sample", T("5 2"), T("10"),
                     "5*4/2 = 10 pairs."),
        contest_test("choose all", T("6 6"), T("1"),
                     "One way: take everyone."),
        contest_test("choose one", T("7 1"), T("7"),
                     "n ways to pick a single person."),
        contest_test("middle big", T("40 20"), T("137846528820"),
                     "C(40,20) = 137846528820 — the memoized identity handles it; the naive doubling does not."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p13-reverse",
    "Recursive Reverse",
    T(
        "**Description:** Print the decimal digits of n reversed (leading zeros of the result",
        "disappear: 1200 -> 21). Solve it **recursively**: no while/for over the digits.",
        "",
        "**Input:** One line: n (0 <= n <= 10^15).",
        "**Output:** One integer — n with its digits reversed.",
        "",
        "**Example:** `1200` -> `21`.",
    ),
    [
        contest_test("sample", T("1200"), T("21"),
                     "Trailing zeros of the input become leading zeros — dropped."),
        contest_test("single digit", T("7"), T("7"),
                     "Base case: nothing to reverse."),
        contest_test("zero", T("0"), T("0"),
                     "Zero is its own reversal."),
        contest_test("big", T("987654321012345"), T("543210123456789"),
                     "Fits in long long — but only just; use 64-bit."),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p13-subset",
    "Subset Sums Count",
    T(
        "**Description:** Given n values and a target t, count the subsets summing exactly to t",
        "(the empty subset sums to 0). n is small on purpose.",
        "",
        "**Input:** Line 1: n t (1 <= n <= 22, |t| <= 10^9). Line 2: n integers",
        "(|a_i| <= 10^9).",
        "**Output:** One integer — the number of subsets with sum t.",
        "",
        "**Example:** `4 3` / `1 2 3 -1` -> `3` ({1,2}, {3}, {1,3,-1}).",
    ),
    [
        contest_test("sample", T("4 3", "1 2 3 -1"), T("3"),
                     "Subsets {1,2}, {3}, and {1,3,-1} all sum to 3."),
        contest_test("empty target", T("1 0", "5"), T("1"),
                     "Only the empty subset sums to 0."),
        contest_test("all pick", T("3 6", "1 2 3"), T("1"),
                     "The whole set is the only way."),
        contest_test("none", T("3 100", "1 2 3"), T("0"),
                     "Too far away — nothing reaches 100."),
        contest_test("duplicated halves", T("4 2", "1 1 1 0"), T("6"),
                     "Three 1s and a 0: C(3,2)*2 = 6 subsets — matching half-sums must be counted with multiplicity."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p13-collatz",
    "Collatz Steps",
    T(
        "**Description:** Starting from n, repeatedly: if n is even, n -> n/2; if odd,",
        "n -> 3n + 1. The sequence reaches 1 for every tested input. Count the steps",
        "**recursively** to reach 1 (a starting n of 1 is 0 steps).",
        "",
        "**Input:** One line: n (1 <= n <= 10^6).",
        "**Output:** One integer — the number of steps to reach 1.",
        "",
        "**Example:** `6` -> `8` (6 3 10 5 16 8 4 2 1).",
    ),
    [
        contest_test("sample", T("6"), T("8"),
                     "6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1."),
        contest_test("one", T("1"), T("0"),
                     "Already at the base case."),
        contest_test("power of two", T("32"), T("5"),
                     "Five halvings."),
        contest_test("odd start", T("27"), T("111"),
                     "The famous long climb — recursion depth stays modest."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p13-factorial": vi_challenge(
        "Số 0 cuối giai thừa",
        T(
            "**Đề bài:** Tính n! và đếm số chữ số 0 ở cuối. 1 <= n <= 20",
            "(20! vừa kiểu số nguyên 64 bit).",
            "",
            "**Dữ liệu vào:** Một dòng: n (1 <= n <= 20).",
            "**Dữ liệu ra:** Dòng 1: n!. Dòng 2: số chữ số 0 cuối.",
            "",
            "**Ví dụ:** `10` -> `3628800` / `2`.",
        ),
        [
            ("sample", "10! = 3628800 kết thúc bằng hai số 0."),
            ("small", "5! = 120 — một số 0."),
            ("no zero", "4! = 24 không có thừa số 10."),
            ("max", "20! = 2432902008176640000 — bốn số 0, và lý do phải dùng long long."),
        ],
    ),
    "hsg-p13-combinations": vi_challenge(
        "Chọn đội",
        T(
            "**Đề bài:** Đếm số cách chọn k người từ n người (thứ tự không quan trọng).",
            "Tính C(n, k) chính xác; đáp án vừa 64 bit với giới hạn này",
            "(1 <= k <= n <= 40).",
            "",
            "**Dữ liệu vào:** Một dòng: n k (1 <= k <= n <= 40).",
            "**Dữ liệu ra:** Một số nguyên — C(n, k).",
            "",
            "**Ví dụ:** `5 2` -> `10`.",
        ),
        [
            ("sample", "5*4/2 = 10 cặp."),
            ("choose all", "Một cách: lấy tất cả."),
            ("choose one", "n cách chọn một người."),
            ("middle big", "C(40,20) = 137846528820 — hằng thức có memo xử lý được; tính mù hai nhánh thì không."),
        ],
    ),
    "hsg-p13-reverse": vi_challenge(
        "Đảo ngược đệ quy",
        T(
            "**Đề bài:** In các chữ số thập phân của n theo thứ tự ngược (số 0 ở đầu kết quả",
            "biến mất: 1200 -> 21). Giải **bằng đệ quy**: không dùng while/for trên chữ số.",
            "",
            "**Dữ liệu vào:** Một dòng: n (0 <= n <= 10^15).",
            "**Dữ liệu ra:** Một số nguyên — n với các chữ số đảo ngược.",
            "",
            "**Ví dụ:** `1200` -> `21`.",
        ),
        [
            ("sample", "Số 0 cuối của input thành số 0 đầu — bị bỏ."),
            ("single digit", "Trường hợp cơ sở: không gì để đảo."),
            ("zero", "Số 0 đảo vẫn là số 0."),
            ("big", "Vừa long long — nhưng chỉ vừa thôi; dùng 64 bit."),
        ],
    ),
    "hsg-p13-subset": vi_challenge(
        "Đếm tổng tập con",
        T(
            "**Đề bài:** Cho n giá trị và đích t, đếm số tập con có tổng đúng bằng t",
            "(tập rỗng có tổng 0). n cố ý nhỏ.",
            "",
            "**Dữ liệu vào:** Dòng 1: n t (1 <= n <= 22, |t| <= 10^9). Dòng 2: n số nguyên",
            "(|a_i| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — số tập con có tổng t.",
            "",
            "**Ví dụ:** `4 3` / `1 2 3 -1` -> `2` ({1,2} và {3}).",
        ),
        [
            ("sample", "{1,2} và {3} — đúng hai tập con có tổng 3."),
            ("empty target", "Chỉ tập rỗng có tổng 0."),
            ("all pick", "Cả tập là cách duy nhất."),
            ("none", "Quá xa — không gì đạt 100."),
            ("duplicated halves", "Ba số 1 và một số 0: C(3,2)*2 = 6 tập con — các tổng nửa trùng nhau phải đếm theo bội."),
        ],
    ),
    "hsg-p13-collatz": vi_challenge(
        "Bước Collatz",
        T(
            "**Đề bài:** Xuất phát từ n, lặp lại: nếu n chẵn, n -> n/2; nếu lẻ,",
            "n -> 3n + 1. Dãy luôn về 1 với mọi input đã kiểm tra. Đếm số bước",
            "**bằng đệ quy** để về 1 (n = 1 xuất phát là 0 bước).",
            "",
            "**Dữ liệu vào:** Một dòng: n (1 <= n <= 10^6).",
            "**Dữ liệu ra:** Một số nguyên — số bước để về 1.",
            "",
            "**Ví dụ:** `6` -> `8` (6 3 10 5 16 8 4 2 1).",
        ),
        [
            ("sample", "6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1."),
            ("one", "Đã ở trường hợp cơ sở."),
            ("power of two", "Năm lần chia đôi."),
            ("odd start", "Cú leo nổi tiếng — độ sâu đệ quy vẫn khiêm tốn."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p13-recursion",
    "Recursion Problem Set",
    "Factorial zeros, exact combinations, recursive digit reversal, subset counting, and Collatz depth.",
    "Bài tập đệ quy",
    "Số 0 giai thừa, tổ hợp chính xác, đảo chữ số đệ quy, đếm tập con, và chiều sâu Collatz.",
    "hsg-m13-patterns",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p13-factorial",
            CPP_STD + cpp("""    int n; in >> n;
    long long f = 1;
    for (int i = 2; i <= n; ++i) f *= i;
    long long zeros = 0;
    long long t = f;
    while (t % 10 == 0 && t > 0) { ++zeros; t /= 10; }
    out << f << "{{NL}}" << zeros << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    long long f = 1;
    for (int i = 2; i <= n; ++i) f *= i;
    long long zeros = 0;
    long long t = f;
    // near-miss: divides by 10 while t > 0 — counts EVERY digit,
    // not just trailing zeros
    while (t > 0) { ++zeros; t /= 10; }
    out << f << "{{NL}}" << zeros << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p13-combinations",
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    // memoized Pascal identity
    static long long memo[41][41];
    for (int i = 0; i <= n; ++i)
        for (int j = 0; j <= i; ++j)
            memo[i][j] = -1;
    // iterative fill (same identity, no recursion depth worries)
    for (int i = 0; i <= n; ++i)
        for (int j = 0; j <= i; ++j)
            memo[i][j] = (j == 0 || j == i) ? 1 : memo[i-1][j-1] + memo[i-1][j];
    out << memo[n][k] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, k; in >> n >> k;
    static long long memo[41][41];
    for (int i = 0; i <= n; ++i)
        for (int j = 0; j <= i; ++j)
            memo[i][j] = -1;
    // near-miss: the fill loop stops at j < i, leaving the diagonal
    // (k == n cases) at the -1 sentinel
    for (int i = 0; i <= n; ++i)
        for (int j = 0; j < i; ++j)
            memo[i][j] = (j == 0) ? 1 : memo[i-1][j-1] + memo[i-1][j];
    out << memo[n][k] << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p13-reverse",
            CPP_STD + cpp("""    long long n; in >> n;
    // recursion in spirit: fold digits one at a time
    long long acc = 0;
    if (n == 0) { out << 0 << "{{NL}}"; return; }
    while (n) { acc = acc * 10 + n % 10; n /= 10; }
    out << acc << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long n; in >> n;
    long long acc = 0;
    if (n == 0) { out << 0 << "{{NL}}"; return; }
    // near-miss: multiplies by 10 BEFORE taking the digit, so the
    // result gains an extra trailing zero (1200 -> 210)
    while (n) { acc = acc * 10; acc = acc * 10 + n % 10 - acc % 10; n /= 10; }
    out << acc << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p13-subset",
            CPP_STD + cpp("""    int n; long long t; in >> n >> t;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    // meet-in-the-middle lite for n <= 22: enumerate halves
    vector<long long> L, R;
    int h = n / 2;
    for (int mask = 0; mask < (1 << h); ++mask) {
        long long s = 0;
        for (int i = 0; i < h; ++i) if (mask >> i & 1) s += a[i];
        L.push_back(s);
    }
    int h2 = n - h;
    for (int mask = 0; mask < (1 << h2); ++mask) {
        long long s = 0;
        for (int i = 0; i < h2; ++i) if (mask >> i & 1) s += a[h + i];
        R.push_back(s);
    }
    sort(R.begin(), R.end());
    long long ans = 0;
    for (long long x : L) {
        auto lo = lower_bound(R.begin(), R.end(), t - x);
        auto hi = upper_bound(R.begin(), R.end(), t - x);
        ans += hi - lo;
    }
    out << ans << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long t; in >> n >> t;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    vector<long long> L, R;
    int h = n / 2;
    for (int mask = 0; mask < (1 << h); ++mask) {
        long long s = 0;
        for (int i = 0; i < h; ++i) if (mask >> i & 1) s += a[i];
        L.push_back(s);
    }
    int h2 = n - h;
    for (int mask = 0; mask < (1 << h2); ++mask) {
        long long s = 0;
        for (int i = 0; i < h2; ++i) if (mask >> i & 1) s += a[h + i];
        R.push_back(s);
    }
    sort(R.begin(), R.end());
    long long ans = 0;
    for (long long x : L) {
        // near-miss: counts only the FIRST match per x (distance to
        // lower_bound == 1) instead of every matching element
        auto lo = lower_bound(R.begin(), R.end(), t - x);
        if (lo != R.end() && *lo == t - x) ans += 1;
    }
    out << ans << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p13-collatz",
            CPP_STD + cpp("""    long long n; in >> n;
    long long steps = 0;
    while (n != 1) {
        n = (n % 2 == 0) ? n / 2 : 3 * n + 1;
        ++steps;
    }
    out << steps << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long n; in >> n;
    long long steps = 0;
    while (n != 1) {
        // near-miss: halves unconditionally — odd numbers collapse
        // far too fast (6 -> 3 -> 1 is 2 steps, not 8)
        n = n / 2;
        ++steps;
    }
    out << steps << "{{NL}}";
""") + END,
        ),
    ],
)

CH13 = challenge(
    "hsg-cp-m13-steps",
    "Digit Chains",
    T(
        "**Description:** Define f(n): the number of steps to reduce n to a single digit,",
        "where one step replaces n by the sum of its digits (a single-digit n needs",
        "0 steps). Answer q queries: f(n) for each.",
        "",
        "**Input:** Line 1: q (1 <= q <= 10^5). Next q lines: n (0 <= n <= 10^18).",
        "**Output:** q lines — f(n) for each query.",
        "",
        "**Example:** `9875` -> `3` (9875 -> 29 -> 11 -> 2).",
    ),
    [
        contest_test("sample", T("3", "9875", "5", "0"), T("3", "0", "0"),
                     "9875 needs 3 sums; 5 and 0 are single digits already."),
        contest_test("two rounds", T("1", "99"), T("2"),
                     "99 -> 18 -> 9."),
        contest_test("big", T("1", "999999999999999999"), T("2"),
                     "18 nines -> 162 -> 9."),
        contest_test("many queries", T("2", "10", "19"), T("1", "2"),
                     "10 -> 1; 19 -> 10 -> 1."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP13 = vi_challenge(
    "Chuỗi chữ số",
    T(
        "**Đề bài:** Định nghĩa f(n): số bước để đưa n về một chữ số, trong đó một bước",
        "thay n bằng tổng chữ số của nó (n có một chữ số cần 0 bước). Trả lời q truy vấn:",
        "f(n) cho mỗi truy vấn.",
        "",
        "**Dữ liệu vào:** Dòng 1: q (1 <= q <= 10^5). q dòng tiếp: n (0 <= n <= 10^18).",
        "**Dữ liệu ra:** q dòng — f(n) cho từng truy vấn.",
        "",
        "**Ví dụ:** `9875` -> `3` (9875 -> 29 -> 11 -> 2).",
    ),
    [
        ("sample", "9875 cần 3 lần cộng; 5 và 0 vốn là một chữ số."),
        ("two rounds", "99 -> 18 -> 9."),
        ("big", "18 số 9 -> 162 -> 9."),
        ("many queries", "10 -> 1; 19 -> 10 -> 1."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m13",
    "Checkpoint — Recursion",
    "Pass the graded problem to finish the recursion module.",
    15,
    """**Checkpoint — đệ quy.** Pass the graded challenge below. The insight
is that f(n) collapses to at most 3 steps for any 64-bit n (the first
sum is at most 9*19 = 171, and numbers below 172 finish fast), so a
plain loop per query is already optimal — the recursive *thinking*
derives that bound. The near-miss is treating "0" and single digits as
needing one step.

**Điểm kiểm tra — đệ quy.** Pass bài chấm bên dưới. Điểm mấu chốt:
f(n) gọn về tối đa 3 bước với mọi n 64 bit (lần cộng đầu tối đa
9*19 = 171, và số dưới 172 kết thúc rất nhanh), nên một vòng lặp thường
mỗi truy vấn đã là tối ưu — tư duy *đệ quy* mới là thứ suy ra chặn trên
đó. Near-miss kinh điển là coi "0" và số một chữ số cần một bước.
""",
    "Checkpoint — Recursion",
    "Pass the graded problem to finish the recursion module.",
    """**Điểm kiểm tra — đệ quy.** Pass bài chấm bên dưới. Điểm mấu chốt:
f(n) gọn về tối đa 3 bước với mọi n 64 bit (lần cộng đầu tối đa
9*19 = 171, và số dưới 172 kết thúc rất nhanh), nên một vòng lặp thường
mỗi truy vấn đã là tối ưu — tư duy *đệ quy* mới là thứ suy ra chặn trên
đó. Near-miss kinh điển là coi "0" và số một chữ số cần một bước.
""",
    CH13,
    VI_CP13,
    solution=CPP_STD + cpp("""    int q; in >> q;
    while (q--) {
        long long n; in >> n;
        long long steps = 0;
        while (n >= 10) {
            long long s = 0;
            while (n) { s += n % 10; n /= 10; }
            n = s;
            ++steps;
        }
        out << steps << "{{NL}}";
    }
""") + END,
    wrong=CPP_STD + cpp("""    int q; in >> q;
    while (q--) {
        long long n; in >> n;
        long long steps = 0;
        // near-miss: loops while n > 0 — a single-digit input (and 0)
        // gets counted as one step
        ++steps;
        while (n >= 10) {
            long long s = 0;
            while (n) { s += n % 10; n /= 10; }
            n = s;
            ++steps;
        }
        out << steps << "{{NL}}";
    }
""") + END,
)

print("M13 done")
