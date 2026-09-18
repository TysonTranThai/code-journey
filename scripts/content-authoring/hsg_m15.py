#!/usr/bin/env python3
"""HSG — Module 15: hsg-dp (quy hoạch động).

DP thinking drills: state/transition/base/answer discipline. Fibonacci by
table, climb-stairs counting, coin change (min coins), 0/1 knapsack,
longest non-decreasing run, grid min-path. Conventions: T() for test I/O,
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

M = "hsg-dp"
write_module(
    M,
    "Dynamic Programming Basics",
    "Stop recomputing: define a state, a transition, and base cases — then fill a table instead of recursing forever.",
    "Quy hoạch động cơ bản",
    "Ngừng tính lại: định nghĩa trạng thái, công thức chuyển và trường hợp cơ sở — rồi điền bảng thay vì đệ quy vô hạn.",
    ["hsg-m15-idea", "hsg-m15-design", "hsg-cp-m15"],
    ["hsg-p15-dp"],
)

write_lesson(
    M,
    "hsg-m15-idea",
    "Overlapping Subproblems",
    "DP = brute force plus a notebook: same subproblem, computed once.",
    15,
    """## The two ingredients

A problem admits DP when it has:

1. **Optimal substructure** — the best answer for size n is built from
   best answers for smaller sizes.
2. **Overlapping subproblems** — a naive recursion recomputes the same
   states many times.

Fibonacci is the canonical example. `fib(5)` calls `fib(3)` twice,
`fib(2)` three times... `fib(30)` alone makes over a million calls.
Write the answers down (`dp[i] = fib(i)`) and each state is computed
once — 30 table cells instead of a million calls.

### Bottom-up fills a table

```cpp
dp[0] = 0; dp[1] = 1;              // base cases
for (int i = 2; i <= n; ++i)
    dp[i] = dp[i-1] + dp[i-2];     // transition
answer = dp[n];                    // final state
```

The four questions you must answer for EVERY dp problem: what is a
state, what does dp[i] **mean**, how does a bigger state build on
smaller ones (transition), and which cells are the base cases. Get the
**meaning** wrong and the transition will look plausible while
computing something useless.

### Why order matters

The table must be filled so that every dependency is ready before use.
`dp[i]` needs `dp[i-1]`, so loop i upward. Later (graphs) the order is
not a simple loop — but for sequence DP it always is.
""",
    "Các bài toán con lặp lại",
    "QHD = vét cạn cộng thêm một cuốn sổ: bài toán con giống nhau, chỉ tính một lần.",
    """## Hai nguyên liệu

Một bài toán dùng được QHD khi nó có:

1. **Cấu trúc con tối ưu** — đáp án tốt nhất cho cỡ n được dựng từ các
   đáp án tốt nhất cho cỡ nhỏ hơn.
2. **Bài toán con trùng lặp** — đệ quy nguội tính lại cùng một trạng
   thái rất nhiều lần.

Fibonacci là ví dụ kinh điển. `fib(5)` gọi `fib(3)` hai lần, `fib(2)`
ba lần... riêng `fib(30)` đã hơn một triệu lần gọi. Ghi đáp án lại
(`dp[i] = fib(i)`) thì mỗi trạng thái chỉ tính một lần — 30 ô bảng
thay vì một triệu lần gọi.

### Bottom-up là điền bảng

```cpp
dp[0] = 0; dp[1] = 1;              // trường hợp cơ sở
for (int i = 2; i <= n; ++i)
    dp[i] = dp[i-1] + dp[i-2];     // công thức chuyển
answer = dp[n];                    // trạng thái cuối
```

Bốn câu hỏi bắt buộc với MỌI bài QHD: trạng thái là gì, `dp[i]` **có
nghĩa là gì**, trạng thái lớn dựng từ trạng thái nhỏ thế nào (chuyển),
ô nào là cơ sở. Hiểu SAI nghĩa thì công thức chuyển vẫn nhìn hợp lý
trong khi tính ra thứ vô dụng.

### Tại sao thứ tự quan trọng

Bảng phải được điền sao cho mọi phụ thuộc sẵn sàng trước khi dùng.
`dp[i]` cần `dp[i-1]`, nên duyệt i tăng dần. Sau này (đồ thị) thứ tự
không còn là vòng lặp đơn giản — nhưng với QHD dãy thì luôn là vậy.
""",
)

write_lesson(
    M,
    "hsg-m15-design",
    "Designing States and Transitions",
    "Three classic designs — counting paths, min-cost, take-or-skip — cover half of beginner DP.",
    16,
    """## Design 1 — counting: stairs

"How many ways to climb n stairs taking 1 or 2 steps?" State: `dp[i]`
= number of ways to reach step i. Last move was from i-1 (one step) or
i-2 (two steps), so:

```cpp
dp[0] = 1; dp[1] = 1;
for (int i = 2; i <= n; ++i) dp[i] = dp[i-1] + dp[i-2];
```

Same recurrence as Fibonacci — recognizing that is a competition skill:
many problems ARE fib in disguise.

## Design 2 — min-cost: coin change

Fewest coins summing to S with coin values c1..ck. State: `dp[s]` =
min coins to make sum s. Transition: try every coin as the last one:

```cpp
dp[0] = 0;                            // zero coins make zero
for (int s = 1; s <= S; ++s) {
    dp[s] = INF;
    for (int c : coins)
        if (c <= s) dp[s] = min(dp[s], dp[s-c] + 1);
}
```

Unreachable sums stay INF — printing dp[S] when it is still INF is a
real bug (print -1 or "impossible" per the statement).

## Design 3 — take-or-skip: 0/1 knapsack

Items with weight w[i], value v[i], capacity W. State: `dp[i][cap]` =
best value using the first i items with capacity cap. The i-th item is
skipped (`dp[i-1][cap]`) or taken (`dp[i-1][cap-w[i]] + v[i]`):

```cpp
for (int i = 1; i <= n; ++i)
  for (int cap = 0; cap <= W; ++cap) {
    dp[i][cap] = dp[i-1][cap];
    if (w[i] <= cap)
        dp[i][cap] = max(dp[i][cap], dp[i-1][cap-w[i]] + v[i]);
  }
```

Note the loop direction: 2D knapsack reads row i-1, so any direction
works. The 1D memory-saving form (`for cap: W..w[i]`, descending) is
the classic interview trap — ascending would allow taking an item
twice. Beginner rule: 2D first, optimize later.
""",
    "Thiết kế trạng thái và công thức chuyển",
    "Ba thiết kế kinh điển — đếm đường, chi phí nhỏ nhất, lấy-hoặc-bỏ — phủ một nửa QHD người mới.",
    """## Thiết kế 1 — đếm: cầu thang

"Có bao nhiêu cách leo n bậc, mỗi lần 1 hoặc 2 bậc?" Trạng thái:
`dp[i]` = số cách tới bậc i. Bước cuối tới từ i-1 (một bậc) hoặc i-2
(hai bậc), nên:

```cpp
dp[0] = 1; dp[1] = 1;
for (int i = 2; i <= n; ++i) dp[i] = dp[i-1] + dp[i-2];
```

Cùng một công thức với Fibonacci — nhận ra điều đó là kỹ năng thi đấu:
nhiều bài toán CHÍNH LÀ fib đeo mặt nạ.

## Thiết kế 2 — chi phí nhỏ nhất: đổi xu

Ít xu nhất để tạo tổng S với các mệnh giá c1..ck. Trạng thái: `dp[s]`
= số xu nhỏ nhất tạo tổng s. Chuyển: thử mọi loại xu làm xu cuối:

```cpp
dp[0] = 0;                            // không xu tạo tổng không
for (int s = 1; s <= S; ++s) {
    dp[s] = INF;
    for (int c : coins)
        if (c <= s) dp[s] = min(dp[s], dp[s-c] + 1);
}
```

Các tổng không tạo được vẫn giữ INF — in thẳng dp[S] khi nó còn INF là
bug thật (phải in -1 hoặc "impossible" theo đề).

## Thiết kế 3 — lấy-hoặc-bỏ: balo 0/1

Vật phẩm có khối lượng w[i], giá trị v[i], sức chứa W. Trạng thái:
`dp[i][cap]` = giá trị tốt nhất dùng i vật đầu với sức chứa cap. Vật
thứ i bị bỏ (`dp[i-1][cap]`) hoặc lấy (`dp[i-1][cap-w[i]] + v[i]`):

```cpp
for (int i = 1; i <= n; ++i)
  for (int cap = 0; cap <= W; ++cap) {
    dp[i][cap] = dp[i-1][cap];
    if (w[i] <= cap)
        dp[i][cap] = max(dp[i][cap], dp[i-1][cap-w[i]] + v[i]);
  }
```

Chú ý hướng vòng lặp: balo 2D đọc hàng i-1, nên chiều nào cũng được.
Dạng 1D tiết kiệm bộ nhớ (`for cap: W..w[i]`, giảm dần) là cái bẫy
kinh điển — tăng dần sẽ cho phép lấy một vật hai lần. Quy tắc người
mới: 2D trước, tối ưu sau.
""",
)

A1 = challenge(
    "hsg-p15-fib",
    "Fibonacci Modulo",
    T(
        "**Description:** Print F(n) modulo 10^9 + 7 where F(0) = 0, F(1) = 1.",
        "",
        "**Input:** One line: n (0 <= n <= 100000).",
        "**Output:** One integer — F(n) mod 10^9 + 7.",
        "",
        "**Example:** `10` -> `55`.",
    ),
    [
        contest_test("base 0", T("0"), T("0"), "F(0) = 0."),
        contest_test("base 1", T("1"), T("1"), "F(1) = 1."),
        contest_test("sample", T("10"), T("55"), "The classic sequence."),
        contest_test("mod wraps", T("90"), T("210345902"),
                     "F(90) = 2880067194370816120; mod 1e9+7 must be taken during the loop, not after (long long overflows near F(92))."),
        contest_test("max n", T("100000"), T("911435502"),
                     "Linear table, one multiplication-add per step."),
    ],
    level="guided",
    difficulty="intermediate",
)

A2 = challenge(
    "hsg-p15-stairs",
    "Counting Stairs",
    T(
        "**Description:** Count the ways to climb n stairs taking 1 or 2 steps at a time,",
        "modulo 10^9 + 7.",
        "",
        "**Input:** One line: n (1 <= n <= 100000).",
        "**Output:** One integer — the number of ways mod 10^9 + 7.",
        "",
        "**Example:** `3` -> `3` (1+1+1, 1+2, 2+1).",
    ),
    [
        contest_test("n 1", T("1"), T("1"), "Single step."),
        contest_test("n 2", T("2"), T("2"), "1+1 or 2."),
        contest_test("sample", T("3"), T("3"), "Three orders."),
        contest_test("n 4", T("4"), T("5"), "dp[4] = dp[3] + dp[2] = 3 + 2."),
        contest_test("max n", T("100000"), T("967618232"),
                     "Same table as fib shifted by one."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p15-coins",
    "Fewest Coins",
    T(
        "**Description:** Given k coin values and a target sum S, print the minimum number",
        "of coins needed to make S, or -1 if impossible. Each coin may be used any",
        "number of times.",
        "",
        "**Input:** Line 1: k S (1 <= k <= 100, 1 <= S <= 100000). Line 2: k values",
        "(1 <= value <= S).",
        "**Output:** One integer — min coins or -1.",
        "",
        "**Example:** `3 11` / `1 5 6` -> `2` (5 + 6).",
    ),
    [
        contest_test("sample", T("3 11", "1 5 6"), T("2"), "5 + 6 beats 1s."),
        contest_test("exact coin", T("1 7", "7"), T("1"), "One coin is enough."),
        contest_test("impossible", T("2 5", "2 4"), T("-1"),
                     "Only even sums are reachable — INF must become -1."),
        contest_test("all ones", T("1 9", "1"), T("9"), "The baseline solution."),
        contest_test("max S", T("2 100000", "3 7"), T("14288"),
                     "14284 sevens + 4 threes = 14288 coins — the DP is exact where greedy-by-count is not obvious."),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p15-knapsack",
    "Simple Knapsack",
    T(
        "**Description:** n items, item i has weight w[i] and value v[i]. Choose a subset",
        "with total weight at most W maximizing total value.",
        "",
        "**Input:** Line 1: n W (1 <= n <= 100, 1 <= W <= 100000). Next n lines:",
        "w[i] v[i] (1 <= w[i] <= W, 1 <= v[i] <= 10^9).",
        "**Output:** One integer — the maximum total value.",
        "",
        "**Example:** `2 5` / `3 10` / `4 15` -> `15` (take item 2; both would weigh 7 > 5).",
    ),
    [
        contest_test("sample", T("2 5", "3 10", "4 15"), T("15"), "Item 2 alone."),
        contest_test("both fit", T("2 7", "3 10", "4 15"), T("25"), "Take everything."),
        contest_test("cheaper better", T("3 4", "2 3", "2 3", "4 5"), T("6"),
                     "Two 2-weight items beat one 4-weight item of value 5."),
        contest_test("unbounded trap", T("1 4", "2 3"), T("3"),
                     "0/1: the single item cannot be taken twice — ascending-loop solutions print 6."),
        contest_test("zero capacity trick", T("2 1", "2 100", "1 7"), T("7"),
                     "Only the 1-weight item fits capacity 1."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p15-maxrun",
    "Longest Non-Decreasing Run",
    T(
        "**Description:** Print the length of the longest contiguous non-decreasing run in",
        "the array.",
        "",
        "**Input:** Line 1: n (1 <= n <= 100000). Line 2: n integers (|a[i]| <= 10^9).",
        "**Output:** One integer — the longest run length.",
        "",
        "**Example:** `6` / `1 2 2 1 3 4` -> `3` (1 3 4).",
    ),
    [
        contest_test("sample", T("6", "1 2 2 1 3 4"), T("3"), "The trailing 1 3 4."),
        contest_test("all equal", T("4", "5 5 5 5"), T("4"),
                     "Non-decreasing allows equality — the whole array."),
        contest_test("strictly down", T("3", "9 5 1"), T("1"), "Every run is a single element."),
        contest_test("single", T("1", "42"), T("1"), "Trivial base."),
        contest_test("max n", T("10", "1 2 3 4 5 4 3 2 1 0"), T("5"),
                     "The opening 1 2 3 4 5."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p15-fib": vi_challenge(
        "Fibonacci theo modulo",
        T(
            "**Đề bài:** In F(n) modulo 10^9 + 7 với F(0) = 0, F(1) = 1.",
            "",
            "**Dữ liệu vào:** Một dòng: n (0 <= n <= 100000).",
            "**Dữ liệu ra:** Một số nguyên — F(n) mod 10^9 + 7.",
            "",
            "**Ví dụ:** `10` -> `55`.",
        ),
        [
            ("base 0", "F(0) = 0."),
            ("base 1", "F(1) = 1."),
            ("sample", "Dãy kinh điển."),
            ("mod wraps", "F(90) = 2880067194370816120; phải lấy mod 1e9+7 trong vòng lặp, không phải sau (long long tràn quanh F(92))."),
            ("max n", "Bảng tuyến tính, mỗi bước một nhân-cộng."),
        ],
    ),
    "hsg-p15-stairs": vi_challenge(
        "Đếm cầu thang",
        T(
            "**Đề bài:** Đếm số cách leo n bậc, mỗi lần 1 hoặc 2 bậc, theo modulo 10^9 + 7.",
            "",
            "**Dữ liệu vào:** Một dòng: n (1 <= n <= 100000).",
            "**Dữ liệu ra:** Một số nguyên — số cách mod 10^9 + 7.",
            "",
            "**Ví dụ:** `3` -> `3` (1+1+1, 1+2, 2+1).",
        ),
        [
            ("n 1", "Một bậc duy nhất."),
            ("n 2", "1+1 hoặc 2."),
            ("sample", "Ba thứ tự."),
            ("n 4", "dp[4] = dp[3] + dp[2] = 3 + 2."),
            ("max n", "Cùng bảng fib, lệch đi một."),
        ],
    ),
    "hsg-p15-coins": vi_challenge(
        "Ít xu nhất",
        T(
            "**Đề bài:** Cho k mệnh giá xu và tổng S, in số xu ít nhất để tạo S, hoặc -1 nếu",
            "không thể. Mỗi loại xu dùng được vô số lần.",
            "",
            "**Dữ liệu vào:** Dòng 1: k S (1 <= k <= 100, 1 <= S <= 100000). Dòng 2: k giá trị",
            "(1 <= giá trị <= S).",
            "**Dữ liệu ra:** Một số nguyên — số xu ít nhất hoặc -1.",
            "",
            "**Ví dụ:** `3 11` / `1 5 6` -> `2` (5 + 6).",
        ),
        [
            ("sample", "5 + 6 tốt hơn toàn xu 1."),
            ("exact coin", "Một xu là đủ."),
            ("impossible", "Chỉ tạo được tổng chẵn — INF phải thành -1."),
            ("all ones", "Lời giải cơ sở."),
            ("max S", "14284 xu 7 + 4 xu 3 = 14288 xu — QHD chính xác tuyệt đối."),
        ],
    ),
    "hsg-p15-knapsack": vi_challenge(
        "Balo đơn giản",
        T(
            "**Đề bài:** n vật, vật i có khối lượng w[i] và giá trị v[i]. Chọn một tập con có",
            "tổng khối lượng không vượt W sao cho tổng giá trị lớn nhất.",
            "",
            "**Dữ liệu vào:** Dòng 1: n W (1 <= n <= 100, 1 <= W <= 100000). n dòng tiếp:",
            "w[i] v[i] (1 <= w[i] <= W, 1 <= v[i] <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — tổng giá trị lớn nhất.",
            "",
            "**Ví dụ:** `2 5` / `3 10` / `4 15` -> `15` (chỉ lấy vật 2; lấy cả hai nặng 7 > 5).",
        ),
        [
            ("sample", "Một mình vật 2."),
            ("both fit", "Lấy hết."),
            ("cheaper better", "Hai vật nặng 2 thắng một vật nặng 4 giá 5."),
            ("unbounded trap", "0/1: một vật không thể lấy hai lần — vòng tăng dần sẽ in 6."),
            ("zero capacity trick", "Chỉ vật nặng 1 vừa sức chứa 1."),
        ],
    ),
    "hsg-p15-maxrun": vi_challenge(
        "Đoạn không giảm dài nhất",
        T(
            "**Đề bài:** In độ dài đoạn liên tiếp dài nhất không giảm trong mảng.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100000). Dòng 2: n số nguyên (|a[i]| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — độ dài đoạn dài nhất.",
            "",
            "**Ví dụ:** `6` / `1 2 2 1 3 4` -> `3` (1 3 4).",
        ),
        [
            ("sample", "Đoạn cuối 1 3 4."),
            ("all equal", "Không giảm cho phép bằng nhau — cả mảng."),
            ("strictly down", "Mọi đoạn dài một phần tử."),
            ("single", "Trường hợp cơ sở tầm thường."),
            ("max n", "Đoạn đầu 1 2 3 4 5."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p15-dp",
    "Dynamic Programming Problem Set",
    "Fibonacci tables, stair counting, coin change, knapsack, and run-length DP.",
    "Bài tập quy hoạch động",
    "Bảng Fibonacci, đếm cầu thang, đổi xu, balo, và QHD đoạn dài nhất.",
    "hsg-m15-design",
    50,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p15-fib",
            CPP_STD + cpp("""    int n; in >> n;
    const long long MOD = 1000000007;
    long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) {
        long long c = (a + b) % MOD;
        a = b; b = c;
    }
    out << a << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    const long long MOD = 1000000007;
    // near-miss: takes mod only at the end — long long overflows at F(92)
    unsigned long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) { unsigned long long c = a + b; a = b; b = c; }
    out << a % MOD << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p15-stairs",
            CPP_STD + cpp("""    int n; in >> n;
    const long long MOD = 1000000007;
    long long a = 1, b = 1;  // dp[0], dp[1]
    for (int i = 2; i <= n; ++i) { long long c = (a + b) % MOD; a = b; b = c; }
    out << b << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    const long long MOD = 1000000007;
    // near-miss: dp[1] seeded as 2 — counts the empty climb twice
    long long a = 1, b = 2;
    for (int i = 2; i <= n; ++i) { long long c = (a + b) % MOD; a = b; b = c; }
    out << b << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p15-coins",
            CPP_STD + cpp("""    int k, S; in >> k >> S;
    vector<int> coins(k);
    for (auto& c : coins) in >> c;
    const int INF = 1e9;
    vector<int> dp(S + 1, INF);
    dp[0] = 0;
    for (int s = 1; s <= S; ++s)
        for (int c : coins)
            if (c <= s && dp[s-c] + 1 < dp[s]) dp[s] = dp[s-c] + 1;
    out << (dp[S] >= INF ? -1 : dp[S]) << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int k, S; in >> k >> S;
    vector<int> coins(k);
    for (auto& c : coins) in >> c;
    const int INF = 1e9;
    vector<int> dp(S + 1, INF);
    dp[0] = 0;
    for (int s = 1; s <= S; ++s)
        for (int c : coins)
            if (c <= s && dp[s-c] + 1 < dp[s]) dp[s] = dp[s-c] + 1;
    // near-miss: prints the raw INF sentinel instead of -1 on unreachable sums
    out << dp[S] << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p15-knapsack",
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<long long> w(n + 1), v(n + 1);
    for (int i = 1; i <= n; ++i) in >> w[i] >> v[i];
    vector<long long> best(W + 1, 0);
    for (int i = 1; i <= n; ++i)
        for (int cap = W; cap >= w[i]; --cap)   // descending: each item once
            best[cap] = max(best[cap], best[cap - w[i]] + v[i]);
    out << best[W] << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n, W; in >> n >> W;
    vector<long long> w(n + 1), v(n + 1);
    for (int i = 1; i <= n; ++i) in >> w[i] >> v[i];
    vector<long long> best(W + 1, 0);
    for (int i = 1; i <= n; ++i)
        for (int cap = w[i]; cap <= W; ++cap)   // near-miss: ASCENDING
            best[cap] = max(best[cap], best[cap - w[i]] + v[i]);
    out << best[W] << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p15-maxrun",
            CPP_STD + cpp("""    int n; in >> n;
    int run = 1, best = 1, prev;
    in >> prev;
    for (int i = 1; i < n; ++i) {
        int x; in >> x;
        run = (x >= prev) ? run + 1 : 1;
        best = max(best, run);
        prev = x;
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    int run = 1, best = 1, prev;
    in >> prev;
    for (int i = 1; i < n; ++i) {
        int x; in >> x;
        // near-miss: strict > — breaks runs on equal elements
        run = (x > prev) ? run + 1 : 1;
        best = max(best, run);
        prev = x;
    }
    out << best << "{{NL}}";
""") + END,
        ),
    ],
)

CH15 = challenge(
    "hsg-cp-m15-potions",
    "Potion Mixing",
    T(
        "**Description:** A potion recipe is a sequence of n steps; step i takes t[i] minutes",
        "and must be preceded by every step it depends on. Dependency j < i is given as a",
        "0/1 matrix: cell (i, j) = 1 means step i requires step j finished first. Compute",
        "the minimum time to finish all steps if independent steps run in parallel.",
        "",
        "**Input:** Line 1: n (1 <= n <= 100). Line 2: n times t[i] (1 <= t[i] <= 1000).",
        "Next n lines: n characters each, '0' or '1' — row i, column j (1-based rows;",
        "diagonal is '0'; the matrix is guaranteed acyclic).",
        "**Output:** One integer — the minimum total minutes.",
        "",
        "**Example:** `3` / `2 3 4` / `000` / `100` / `110` -> `9`: step 1 done at 2,",
        "step 2 (needs 1) done at 5, step 3 (needs 1 and 2) done at max(2,5)+4 = 9.",
    ),
    [
        contest_test("sample", T("3", "2 3 4", "000", "100", "110"), T("9"),
                     "finish(1)=2; finish(2)=2+3=5; finish(3)=max(2,5)+4=9."),
        contest_test("no deps", T("3", "5 2 7", "000", "000", "000"), T("7"),
                     "All parallel — the longest single step."),
        contest_test("chain", T("3", "1 1 1", "000", "100", "010"), T("3"),
                     "1 -> 2 -> 3 forces serial execution."),
        contest_test("single", T("1", "9", "0"), T("9"), "One step, no deps."),
        contest_test("diamond", T("4", "1 5 2 4", "0000", "1000", "1000", "0110"),
                     T("10"),
                     "finish(2)=6, finish(3)=3, finish(4)=max(6,3)+4=10 — the LONGEST branch is listed first, so last-dependency logic fails."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP15 = vi_challenge(
    "Pha chế thuốc",
    T(
        "**Đề bài:** Một công thức thuốc gồm n bước; bước i mất t[i] phút và phải chờ mọi",
        "bước nó phụ thuộc. Phụ thuộc j < i cho bằng ma trận 0/1: ô (i, j) = 1 nghĩa là",
        "bước i yêu cầu bước j xong trước. Tính thời gian ít nhất để hoàn thành tất cả",
        "nếu các bước độc lập chạy song song.",
        "",
        "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100). Dòng 2: n thời gian t[i] (1 <= t[i] <= 1000).",
        "n dòng tiếp: mỗi dòng n ký tự '0' hoặc '1' — hàng i, cột j (hàng tính từ 1;",
        "đường chéo là '0'; ma trận đảm bảo không có chu trình).",
        "**Dữ liệu ra:** Một số nguyên — tổng số phút ít nhất.",
        "",
        "**Ví dụ:** `3` / `2 3 4` / `000` / `100` / `110` -> `9`: xong(1)=2,",
        "xong(2)=2+3=5, xong(3)=max(2,5)+4=9.",
    ),
    [
        ("sample", "xong(1)=2; xong(2)=2+3=5; xong(3)=max(2,5)+4=9."),
        ("no deps", "Chạy song song hết — bước dài nhất."),
        ("chain", "1 -> 2 -> 3 buộc chạy tuần tự."),
        ("single", "Một bước, không phụ thuộc."),
        ("diamond", "xong(2)=6, xong(3)=3, xong(4)=max(6,3)+4=10 — nhánh DÀI nhất đứng trước, nên logic phụ-thức-cuối sẽ sai."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m15",
    "Checkpoint — Dynamic Programming",
    "Pass the graded problem to finish the DP module.",
    15,
    """**Checkpoint — quy hoạch động.** Pass the graded challenge below.
finish[i] = t[i] + max(finish[j] over dependencies j) is the whole
state machine; steps with no dependencies anchor at their own time.
The graded near-misses: taking only the LAST dependency's finish time
instead of the max, and forgetting that parallel steps start together.

**Điểm kiểm tra — quy hoạch động.** Pass bài chấm bên dưới.
xong[i] = t[i] + max(xong[j] với mọi phụ thuộc j) là toàn bộ cỗ máy
trạng thái; bước không phụ thuộc neo tại thời gian của chính nó. Các
near-miss bị chấm: chỉ lấy thời gian xong của phụ thuộc CUỐI thay vì
max, và quên rằng các bước song song bắt đầu cùng lúc.
""",
    "Checkpoint — Dynamic Programming",
    "Pass the graded problem to finish the DP module.",
    """**Điểm kiểm tra — quy hoạch động.** Pass bài chấm bên dưới.
xong[i] = t[i] + max(xong[j] với mọi phụ thuộc j) là toàn bộ cỗ máy
trạng thái; bước không phụ thuộc neo tại thời gian của chính nó. Các
near-miss bị chấm: chỉ lấy thời gian xong của phụ thuộc CUỐI thay vì
max, và quên rằng các bước song song bắt đầu cùng lúc.
""",
    CH15,
    VI_CP15,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> t(n + 1);
    for (int i = 1; i <= n; ++i) in >> t[i];
    vector<string> dep(n);
    for (auto& row : dep) in >> row;
    vector<long long> fin(n + 1, 0);
    long long ans = 0;
    for (int i = 1; i <= n; ++i) {
        long long ready = 0;
        for (int j = 1; j <= n; ++j)
            if (dep[i-1][j-1] == '1') ready = max(ready, fin[j]);
        fin[i] = ready + t[i];
        ans = max(ans, fin[i]);
    }
    out << ans << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> t(n + 1);
    for (int i = 1; i <= n; ++i) in >> t[i];
    vector<string> dep(n);
    for (auto& row : dep) in >> row;
    vector<long long> fin(n + 1, 0);
    long long ans = 0;
    for (int i = 1; i <= n; ++i) {
        // near-miss: takes the LAST listed dependency, not the max finish
        long long ready = 0;
        for (int j = 1; j <= n; ++j)
            if (dep[i-1][j-1] == '1') ready = fin[j];
        fin[i] = ready + t[i];
        ans = max(ans, fin[i]);
    }
    out << ans << "{{NL}}";
""") + END,
)

print("M15 done")
