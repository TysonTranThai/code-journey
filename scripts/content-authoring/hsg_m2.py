#!/usr/bin/env python3
"""HSG — Module 2: hsg-loops (loops as simulation).

Counters, accumulators, digit processing, repeated computation — the loop
patterns every HSG problem reuses. Main files English; .vi overlays Vietnamese.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test,
)

M = "hsg-loops"

write_module(
    M,
    "Loops as Simulation",
    "for/while as simulation engines: counters, accumulators, digit processing, and repeated computation — the patterns hidden inside most easy HSG problems.",
    "Vòng lặp là mô phỏng",
    "for/while như máy mô phỏng: bộ đếm, biến cộng dồn, xử lý chữ số, tính toán lặp — các mẫu hình ẩn trong đa số bài HSG dễ.",
    ["hsg-m2-patterns", "hsg-m2-digit-work", "hsg-cp-m2"],
    ["hsg-p2-loops"],
)

write_lesson(
    M, "hsg-m2-patterns",
    "The Four Loop Patterns",
    "Counting, accumulating, searching-with-break, and simulation — with the loop invariants that make them correct.",
    13,
    """## Four patterns cover most easy problems

### 1. Counter — "how many?"

```cpp
int cnt = 0;
for (int i = 0; i < n; ++i) {
    long long x; in >> x;
    if (x % 2 == 0) ++cnt;
}
out << cnt << "\\n";
```

Rule: declare the counter **outside** the loop, update inside, print after.

### 2. Accumulator — "sum / product"

```cpp
long long sum = 0;
for (long long x : a) sum += x;   // 0 is the identity for +
```

Pick the identity element carefully: `0` for sums, `1` for products,
`-infinity` for max. Product of 10^5 values of 2? That's 2^100000 — no
integer type holds it. Overflow thinking starts here.

### 3. Search with early exit

```cpp
int idx = -1;
for (int i = 0; i < n; ++i)
    if (a[i] == target) { idx = i; break; }
```

`break` on the first hit. For n up to ~10^7 this linear scan is fine at
the platform's limits — knowing *when* linear is enough is a skill.

### 4. Simulation — "play out the rules"

If the problem describes a process (days passing, balls bouncing), write
the process as a loop. Ask: what is one *step*? What changes each step?
When does it stop?

```cpp
long long x; in >> x;
int steps = 0;
while (x > 1) { x = (x % 2 == 0) ? x / 2 : 3 * x + 1; ++steps; }
out << steps << "\\n";
```

### The invariant habit

Before trusting a loop, say in one sentence what is true **every time you
reach the top of the loop**. "After k iterations, sum holds a[0]+…+a[k-1]."
That sentence is the difference between a guess and a proof.""",
    "Bốn mẫu hình vòng lặp",
    "Đếm, cộng dồn, tìm kiếm với break, mô phỏng — cùng bất biến giúp vòng lặp đúng.",
    """## Bốn mẫu hình phủ đa số bài dễ

### 1. Bộ đếm — "có bao nhiêu?"

```cpp
int cnt = 0;
for (int i = 0; i < n; ++i) {
    long long x; in >> x;
    if (x % 2 == 0) ++cnt;
}
out << cnt << "\\n";
```

Quy tắc: khai báo bộ đếm **ngoài** vòng lặp, cập nhật bên trong, in sau.

### 2. Biến cộng dồn — "tổng / tích"

```cpp
long long sum = 0;
for (long long x : a) sum += x;   // 0 là phần tử trung hòa của +
```

Chọn phần tử trung hòa cẩn thận: `0` cho tổng, `1` cho tích, `-infinity`
cho max. Tích của 10^5 số 2? Đó là 2^100000 — không kiểu nguyên nào chứa
nổi. Suy nghĩ tràn số bắt đầu từ đây.

### 3. Tìm kiếm thoát sớm

```cpp
int idx = -1;
for (int i = 0; i < n; ++i)
    if (a[i] == target) { idx = i; break; }
```

`break` ngay khi gặp đầu tiên. Với n tới ~10^7, duyệt tuyến tính vẫn ổn
trong giới hạn nền tảng — biết *khi nào* duyệt tuyến tính là đủ cũng là
một kỹ năng.

### 4. Mô phỏng — "chạy theo luật"

Nếu bài tả một tiến trình (ngày trôi, bóng nảy), viết tiến trình đó thành
vòng lặp. Hỏi: một *bước* là gì? Bước nào thay đổi gì? Dừng khi nào?

```cpp
long long x; in >> x;
int steps = 0;
while (x > 1) { x = (x % 2 == 0) ? x / 2 : 3 * x + 1; ++steps; }
out << steps << "\\n";
```

### Thói quen bất biến

Trước khi tin vòng lặp, nói trong một câu điều gì đúng **mỗi khi chạm
đỉnh vòng lặp**. "Sau k bước, sum = a[0]+…+a[k-1]." Câu đó là khoảng cách
giữa phỏng đoán và chứng minh.""",
)

write_lesson(
    M, "hsg-m2-digit-work",
    "Digit Processing: Numbers as Sequences",
    "n % 10 and n / 10 peel digits one by one — digit sums, digit counts, digit max, and rebuilding numbers.",
    12,
    """## Peeling digits with % and /

An integer is a sequence of digits you can process without any string:

```cpp
long long n; in >> n;
long long digitSum = 0;
while (n > 0) {
    digitSum += n % 10;   // last digit
    n /= 10;              // drop last digit
}
```

`n % 10` = last digit; `n / 10` = everything before it. Two operations,
every digit problem becomes a loop problem.

### The classic digit tasks

| Task | How |
| --- | --- |
| Digit sum | accumulate `n % 10` |
| Digit count | count iterations |
| Largest digit | track max of `n % 10` |
| Digit product | accumulate product (beware 0 digits) |
| Reverse digits | `rev = rev * 10 + n % 10` |

### Worked example: is the number a palindrome?

```cpp
long long n; in >> n;
long long m = n, rev = 0;
while (m > 0) { rev = rev * 10 + m % 10; m /= 10; }
out << (rev == n ? "PALIN" : "NO") << "\\n";
```

Note we kept `n` untouched in a copy `m` — the loop destroys what it
peels. Forgetting the copy is a classic bug.

### Overflow and negatives

Reversing 19-digit numbers can overflow `long long` — read constraints
first. And for negative inputs, decide the convention (usually work with
`abs(n)`) before looping.""",
    "Xử lý chữ số: số như một dãy",
    "n % 10 và n / 10 tách từng chữ số — tổng, đếm, max chữ số, dựng lại số.",
    """## Tách chữ số bằng % và /

Một số nguyên là dãy chữ số bạn xử lý được mà không cần xâu:

```cpp
long long n; in >> n;
long long digitSum = 0;
while (n > 0) {
    digitSum += n % 10;   // chữ số cuối
    n /= 10;              // bỏ chữ số cuối
}
```

`n % 10` = chữ số cuối; `n / 10` = phần còn lại. Hai phép toán, mọi bài
chữ số thành bài vòng lặp.

### Các bài chữ số kinh điển

| Bài | Cách làm |
| --- | --- |
| Tổng chữ số | cộng dồn `n % 10` |
| Số chữ số | đếm số vòng lặp |
| Chữ số lớn nhất | lưu max của `n % 10` |
| Tích chữ số | cộng dồn tích (coi chừng chữ số 0) |
| Đảo chữ số | `rev = rev * 10 + n % 10` |

### Ví dụ làm mẫu: số có đối xứng không?

```cpp
long long n; in >> n;
long long m = n, rev = 0;
while (m > 0) { rev = rev * 10 + m % 10; m /= 10; }
out << (rev == n ? "PALIN" : "NO") << "\\n";
```

Chú ý giữ `n` nguyên trong bản copy `m` — vòng lặp phá hủy cái nó tách.
Quên bản copy là lỗi kinh điển.

### Tràn số và số âm

Đảo số 19 chữ số có thể tràn `long long` — đọc giới hạn trước. Với input
âm, chốt quy ước (thường làm với `abs(n)`) trước khi lặp.""",
)

CH1 = challenge(
    "hsg-p2-digit-sum",
    "Digit Sum",
    """**Description:** Given a positive integer n, print the sum of its digits.

**Input:** One integer n (1 ≤ n ≤ 10^18).
**Output:** One integer — the digit sum.

**Example:** `1234` → `1+2+3+4` = `10`.""",
    [
        contest_test("sample", "1234\n", "10\n", "1+2+3+4 = 10."),
        contest_test("single digit", "7\n", "7\n", "A one-digit number is its own digit sum."),
        contest_test("all nines", "999999999999999999\n", "162\n", "18 digits × 9 = 162 — works at the maximum 10^18."),
        contest_test("with zeros", "1000\n", "1\n", "Zeros contribute nothing."),
    ],
    level="imitation",
)

CH2 = challenge(
    "hsg-p2-count-divisors",
    "Count the Divisors",
    """**Description:** Given a positive integer n, print how many divisors it has.

**Input:** One integer n (1 ≤ n ≤ 10^12).
**Output:** One integer — the divisor count.

**Example:** `12` → `6` (1, 2, 3, 4, 6, 12).

*Careful:* looping i from 1 to n is far too slow for 10^12. Loop i while
`i * i <= n` and count each divisor pair (i, n/i) — remember i = n/i when
n is a perfect square.""",
    [
        contest_test("sample", "12\n", "6\n", "Divisors of 12: 1,2,3,4,6,12."),
        contest_test("one", "1\n", "1\n", "1 has exactly one divisor: itself."),
        contest_test("prime", "999999999989\n", "2\n", "A large prime has only 1 and itself — the i*i loop must be fast."),
        contest_test("perfect square", "36\n", "9\n", "Divisors of 36 pair up with 6·6 counted once: 1,2,3,4,6,9,12,18,36."),
    ],
    level="guided",
    difficulty="intermediate",
)

CH3 = challenge(
    "hsg-p2-step-sim",
    "Reduce to One",
    """**Description:** Start from n. One step: if n is even, n becomes n/2;
otherwise n becomes 3n+1. Count the steps until n becomes 1.

**Input:** One integer n (1 ≤ n ≤ 10^6).
**Output:** One integer — the number of steps.

**Example:** `6` → 6→3→10→5→16→8→4→2→1 → `8` steps.""",
    [
        contest_test("sample", "6\n", "8\n", "6→3→10→5→16→8→4→2→1 is 8 steps."),
        contest_test("already one", "1\n", "0\n", "Already 1 → zero steps."),
        contest_test("power of two", "1024\n", "10\n", "Halving 1024 ten times reaches 1."),
        contest_test("odd start", "27\n", "111\n", "The famous slow starter — simulation must just run."),
    ],
    level="guided",
)

CH4 = challenge(
    "hsg-p2-max-digit-run",
    "Longest Digit Run",
    """**Description:** Given a positive integer n, find the length of the
longest run of equal consecutive digits (in normal left-to-right order).

**Input:** One integer n (1 ≤ n ≤ 10^18).
**Output:** One integer — the longest run length.

**Example:** `1223331` → the run `333` has length `3`.

*Note:* digits arrive right-to-left from `% 10` — track the current run
carefully as digits change.""",
    [
        contest_test("sample", "1223331\n", "3\n", "The digit 3 repeats 3 times in a row."),
        contest_test("all same", "7777\n", "4\n", "One run of length 4."),
        contest_test("no repeats", "121212\n", "1\n", "Every run is length 1."),
        contest_test("single digit", "5\n", "1\n", "One digit is a run of one."),
    ],
    level="independent",
    difficulty="intermediate",
)

CH5 = challenge(
    "hsg-p2-sigma",
    "Special Sum",
    """**Description:** Given n, print S = 1^2 + 2^2 + … + n^2 (squares sum).

**Input:** One integer n (1 ≤ n ≤ 10^6).
**Output:** One integer S. (It can reach ~3.3·10^17 — pick the right type.)

**Example:** `3` → `1 + 4 + 9` = `14`.""",
    [
        contest_test("sample", "3\n", "14\n", "1 + 4 + 9 = 14."),
        contest_test("one", "1\n", "1\n", "Only 1^2."),
        contest_test("maximum", "1000000\n", "333333833333500000\n", "At n = 10^6 the sum is ~3.3·10^17 — long long required, int overflows."),
        contest_test("ten", "10\n", "385\n", "Known closed form check."),
    ],
    level="independent",
)

CH6 = challenge(
    "hsg-p2-day-sim",
    "Mowing the Field",
    """**Description:** A lawn is 1 cm tall. Each day it grows by g cm; each
evening a mower cuts it back to h cm (only if it is taller than h).
After how many full days is the lawn taller than T cm for the first time?
Print the day number, or `-1` if it never happens within 10^6 days.

**Input:** One line: g h T (0 ≤ g ≤ 10, 0 ≤ h ≤ 10, 1 ≤ T ≤ 10^9).
**Output:** One integer — the first day the height exceeds T, else -1.

**Example:** `2 1 4` → day1: 1+2=3 (cut to 1), day2: 1+2=3… never exceeds
4 → `-1`. With `3 1 4`: day1: 4 (not > 4? cut), day2: 4… `-1`. With
`4 1 4`: day1: 1+4=5 > 4 → `1`.""",
    [
        contest_test("never", "2 1 4\n", "-1\n", "Grows 3, cut to 1 — the cycle never passes 4."),
        contest_test("first day", "4 1 4\n", "1\n", "1+4 = 5 > 4 on day 1."),
        contest_test("slow growth", "1 0 5\n", "5\n", "No mower (h=0): heights 1..6, exceeds 5 on day 5."),
        contest_test("zero growth", "0 0 3\n", "-1\n", "Never grows, never exceeds."),
    ],
    level="combination",
    difficulty="intermediate",
)

write_practice(
    M, "hsg-p2-loops",
    "Loop Patterns Set",
    "Six loop problems: digit work, divisor pairs with the i·i trick, simulation, and overflow-aware accumulation.",
    "Bộ đề vòng lặp",
    "Sáu bài vòng lặp: xử lý chữ số, cặp ước với thủ thuật i·i, mô phỏng, và cộng dồn chống tràn.",
    "hsg-m2-digit-work",
    70,
    "beginner",
    [CH1, CH2, CH3, CH4, CH5, CH6],
    {
        "hsg-p2-digit-sum": vi_challenge("Tổng chữ số", "**Mô tả:** Cho số nguyên dương n, in tổng các chữ số.\n\n**Dữ liệu vào:** Một số nguyên n (1 ≤ n ≤ 10^18).\n**Dữ liệu ra:** Một số nguyên — tổng chữ số.\n\n**Ví dụ:** `1234` → `10`.", [("ví dụ đề bài", "1+2+3+4 = 10."), ("một chữ số", "Số một chữ số bằng chính tổng chữ số của nó."), ("toàn chín", "18 chữ số × 9 = 162 — chạy tới cận 10^18."), ("có số không", "Các chữ số 0 không góp gì.")]),
        "hsg-p2-count-divisors": vi_challenge("Đếm ước", "**Mô tả:** Cho số nguyên dương n, in số lượng ước của n.\n\n**Dữ liệu vào:** Một số nguyên n (1 ≤ n ≤ 10^12).\n**Dữ liệu ra:** Một số nguyên — số ước.\n\n**Ví dụ:** `12` → `6` (1, 2, 3, 4, 6, 12).\n\n*Lưu ý:* duyệt i tới n quá chậm cho 10^12. Duyệt i với `i * i <= n` và đếm từng cặp ước (i, n/i) — nhớ trường hợp i = n/i khi n là số chính phương.", [("ví dụ đề bài", "Ước của 12: 1,2,3,4,6,12."), ("một", "1 có đúng một ước: chính nó."), ("số nguyên tố", "Số nguyên tố lớn chỉ có 1 và chính nó — vòng i*i phải nhanh."), ("chính phương", "Ước của 36: 1,2,3,4,6,9,12,18,36 — cặp 6·6 đếm một lần.")]),
        "hsg-p2-step-sim": vi_challenge("Quy về một", "**Mô tả:** Bắt đầu từ n. Một bước: nếu n chẵn thì n := n/2, ngược lại n := 3n+1. Đếm số bước tới khi n = 1.\n\n**Dữ liệu vào:** Một số nguyên n (1 ≤ n ≤ 10^6).\n**Dữ liệu ra:** Số bước.\n\n**Ví dụ:** `6` → `8` bước.", [("ví dụ đề bài", "6→3→10→5→16→8→4→2→1 là 8 bước."), ("đã là một", "Đã là 1 → 0 bước."), ("luỹ thừa hai", "Chia 1024 cho 2 mười lần về 1."), ("bắt đầu lẻ", "Số 27 nổi tiếng chậm — cứ mô phỏng.")]),
        "hsg-p2-max-digit-run": vi_challenge("Đoạn chữ số dài nhất", "**Mô tả:** Cho số nguyên dương n, tìm độ dài đoạn dài nhất gồm các chữ số bằng nhau liên tiếp (theo thứ tự trái→phải).\n\n**Dữ liệu vào:** Một số nguyên n (1 ≤ n ≤ 10^18).\n**Dữ liệu ra:** Độ dài đoạn dài nhất.\n\n**Ví dụ:** `1223331` → `3`.", [("ví dụ đề bài", "Chữ số 3 lặp 3 lần liên tiếp."), ("toàn giống", "Một đoạn dài 4."), ("không lặp", "Mọi đoạn dài 1."), ("một chữ số", "Một chữ số là đoạn dài một.")]),
        "hsg-p2-sigma": vi_challenge("Tổng bình phương", "**Mô tả:** Cho n, in S = 1^2 + 2^2 + … + n^2.\n\n**Dữ liệu vào:** Một số nguyên n (1 ≤ n ≤ 10^6).\n**Dữ liệu ra:** S. (Có thể tới ~3.3·10^17 — chọn đúng kiểu.)\n\n**Ví dụ:** `3` → `14`.", [("ví dụ đề bài", "1 + 4 + 9 = 14."), ("một", "Chỉ 1^2."), ("cận trên", "Tại n = 10^6 tổng ~3.3·10^17 — cần long long, int tràn."), ("mười", "Soi công thức đóng.")]),
        "hsg-p2-day-sim": vi_challenge("Cắt cỏ", "**Mô tả:** Bãi cỏ cao 1 cm. Mỗi ngày mọc thêm g cm; mỗi tối máy cắt hạ về h cm (nếu cao hơn h). Sau bao nhiêu ngày nguyên vẹn bãi cỏ lần đầu vượt T cm? In số ngày, hoặc `-1` nếu không bao giờ trong 10^6 ngày.\n\n**Dữ liệu vào:** Một dòng: g h T.\n**Dữ liệu ra:** Số ngày đầu tiên vượt T, hoặc -1.\n\n**Ví dụ:** `2 1 4` → `-1`; `4 1 4` → `1`.", [("không bao giờ", "Mọc 3, cắt về 1 — chu kỳ không qua 4."), ("ngày đầu", "1+4 = 5 > 4 ngay ngày 1."), ("mọc chậm", "Không cắt (h=0): 1..6, vượt 5 ngày thứ 5."), ("không mọc", "Không bao giờ mọc, không bao giờ vượt.")]),
    },
    solutions=[
        (
            "hsg-p2-digit-sum",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long s = 0;\n    while (n > 0) { s += n % 10; n /= 10; }\n    out << s << \"\\n\";\n}",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long s = 0;\n    // near-miss: int digit accumulation is fine here, but the loop\n    // condition `n > 9` stops one digit early — final digit never added\n    while (n > 9) { s += n % 10; n /= 10; }\n    out << s << \"\\n\";\n}",
        ),
        (
            "hsg-p2-count-divisors",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long cnt = 0;\n    for (long long i = 1; i * i <= n; ++i) {\n        if (n % i == 0) { cnt += 2; if (i == n / i) --cnt; }\n    }\n    out << cnt << \"\\n\";\n}",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long cnt = 0;\n    // near-miss: perfect-square root counted twice\n    for (long long i = 1; i * i <= n; ++i) {\n        if (n % i == 0) { cnt += 2; }\n    }\n    out << cnt << \"\\n\";\n}",
        ),
        (
            "hsg-p2-step-sim",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long steps = 0;\n    while (n > 1) { n = (n % 2 == 0) ? n / 2 : 3 * n + 1; ++steps; }\n    out << steps << \"\\n\";\n}",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long steps = 0;\n    // near-miss: counts the final n = 1 as a step too (3·1+1 loop is\n    // prevented by the guard, but the count is one too high for even\n    // starts because the update happens before the check... subtle)\n    while (n >= 1) { n = (n % 2 == 0) ? n / 2 : 3 * n + 1; ++steps; if (n == 1) break; }\n    out << steps << \"\\n\";\n}",
        ),
        (
            "hsg-p2-max-digit-run",
            "#include <iostream>\n#include <algorithm>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    int best = 0, cur = 0;\n    long long prev = -1;\n    while (n > 0) {\n        long long d = n % 10;\n        cur = (d == prev) ? cur + 1 : 1;\n        best = std::max(best, cur);\n        prev = d;\n        n /= 10;\n    }\n    out << best << \"\\n\";\n}",
            "#include <iostream>\n#include <algorithm>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    int best = 1, cur = 1;\n    long long prev = -1;\n    // near-miss: never resets the current run when the digit changes\n    while (n > 0) {\n        long long d = n % 10;\n        if (d == prev) { ++cur; best = std::max(best, cur); }\n        prev = d;\n        n /= 10;\n    }\n    out << best << \"\\n\";\n}",
        ),
        (
            "hsg-p2-sigma",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long s = 0;\n    for (long long i = 1; i <= n; ++i) s += i * i;\n    out << s << \"\\n\";\n}",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int n; in >> n;\n    // near-miss: int accumulation — at n = 10^6 the sum ~3.3e17\n    // overflows int (and even the i*i term overflows at i ~ 46341)\n    int s = 0;\n    for (int i = 1; i <= n; ++i) s += i * i;\n    out << s << \"\\n\";\n}",
        ),
        (
            "hsg-p2-day-sim",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long g, h, T; in >> g >> h >> T;\n    long long height = 1;\n    for (long long day = 1; day <= 1000000; ++day) {\n        height += g;\n        if (height > T) { out << day << \"\\n\"; return; }\n        if (h > 0 && height > h) height = h;   // h = 0 means no mower\n    }\n    out << -1 << \"\\n\";\n}",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long g, h, T; in >> g >> h >> T;\n    long long height = 1;\n    // near-miss: compares against T AFTER the mower cut, so a day that\n    // crossed T but got cut back is never reported\n    for (long long day = 1; day <= 1000000; ++day) {\n        height += g;\n        if (h > 0 && height > h) height = h;\n        if (height > T) { out << day << \"\\n\"; return; }\n    }\n    out << -1 << \"\\n\";\n}",
        ),
    ],
)

write_checkpoint(
    M, "hsg-cp-m2",
    "Checkpoint — Loops",
    "Pass the graded problem to finish the loops module.",
    15,
    "**Checkpoint — loops.** Pass the graded challenge below to finish the module.",
    "Checkpoint — vòng lặp",
    "Vượt qua bài chấm cuối module để hoàn thành phần vòng lặp.",
    "**Checkpoint — vòng lặp.** Vượt qua challenge có chấm bên dưới để hoàn thành module.",
    challenge(
        "hsg-cp-m2-palindrome",
        "Palindrome Number",
        """**Description:** Given a positive integer n, print `PALIN` if its
decimal digits read the same left-to-right and right-to-left, else `NO`.

**Input:** One integer n (1 ≤ n ≤ 10^18).
**Output:** `PALIN` or `NO`.

**Example:** `12321` → `PALIN`; `1234` → `NO`.

**Constraints:** 50% of tests have n ≤ 10^9; 100% have n ≤ 10^18.""",
        [
            contest_test("odd length", "12321\n", "PALIN\n", "12321 reversed is 12321."),
            contest_test("not palindrome", "1234\n", "NO\n", "4321 differs from 1234."),
            contest_test("single digit", "9\n", "PALIN\n", "One digit is always a palindrome."),
            contest_test("trailing zeros", "100000000000000001\n", "PALIN\n", "18-digit palindrome — must not overflow the reversal."),
        ],
    ),
    vi_challenge("Số đối xứng", "**Mô tả:** Cho số nguyên dương n, in `PALIN` nếu các chữ số đọc xuôi và ngược giống nhau, ngược lại in `NO`.\n\n**Dữ liệu vào:** Một số nguyên n (1 ≤ n ≤ 10^18).\n**Dữ liệu ra:** `PALIN` hoặc `NO`.\n\n**Ví dụ:** `12321` → `PALIN`; `1234` → `NO`.", [("lẻ chữ số", "12321 đảo ngược vẫn là 12321."), ("không đối xứng", "4321 khác 1234."), ("một chữ số", "Một chữ số luôn đối xứng."), ("số không ở cuối", "Số đối xứng 18 chữ số — đảo không được tràn.")]),
    solution="#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    long long m = n, rev = 0;\n    while (m > 0) { rev = rev * 10 + m % 10; m /= 10; }\n    out << (rev == n ? \"PALIN\" : \"NO\") << \"\\n\";\n}",
    wrong="#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n; in >> n;\n    // near-miss: destroys n inside the loop, then compares rev to 0\n    long long rev = 0;\n    while (n > 0) { rev = rev * 10 + n % 10; n /= 10; }\n    out << (rev == n ? \"PALIN\" : \"NO\") << \"\\n\";\n}",
)

print("module 2 authored")
