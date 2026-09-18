#!/usr/bin/env python3
"""HSG — Module 11: hsg-number (số học cơ bản).

Parity, divisibility, gcd/lcm via Euclid, divisor enumeration in O(sqrt n),
prime checking in O(sqrt n), digit sums, and modular thinking on sums.
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

GCD_DEF = cpp("""long long gcdll(long long a, long long b) {
    while (b) { long long t = a % b; a = b; b = t; }
    return a;
}
""")

END = "}" + NL

M = "hsg-number"
write_module(
    M,
    "Basic Number Theory",
    "Divisibility, gcd/lcm with Euclid, divisors and primes in O(sqrt n), digit sums, and modular thinking for sums.",
    "Số học cơ bản",
    "Chia hết, gcd/lcm với Euclid, ước và số nguyên tố trong O(sqrt n), tổng chữ số, tư duy modulo cho tổng.",
    ["hsg-m11-gcd", "hsg-m11-divisors", "hsg-cp-m11"],
    ["hsg-p11-number"],
)

write_lesson(
    M,
    "hsg-m11-gcd",
    "GCD, LCM, and Euclid",
    "The oldest algorithm in the book — and the identity that keeps lcm inside the type range.",
    14,
    """## gcd by Euclid

```cpp
long long gcd(long long a, long long b) {
    while (b) { long long t = a % b; a = b; b = t; }
    return a;
}
```

Every step replaces (a, b) with (b, a mod b); the gcd is invariant because
any common divisor of a and b divides a mod b = a - (a/b)*b. Termination:
b strictly decreases and stays >= 0. Complexity O(log min(a, b)) — the
Fibonacci worst case. gcd(a, 0) = a closes the loop.

### lcm — with a safety order

```cpp
long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;   // divide FIRST
}
```

The order matters: `a * b / gcd` can overflow even when the true lcm
fits in long long (a = b = 10^9: a*b is 10^18, near the 9.2*10^18
limit — fine — but a = 2*10^9 impossible for int inputs; the general
rule stands). Dividing first keeps every intermediate value inside the
final result's magnitude.

### Multiple numbers

gcd(a, b, c) = gcd(gcd(a, b), c) — fold it. LCM chains the same way,
watching overflow at every step.

### Where gcd appears in contests

- "Reduce the fraction" — divide both parts by gcd.
- "Can the two step sizes meet?" — reachable positions are multiples of
  gcd.
- Counting lattice points on a segment: gcd of the deltas.
""",
    "GCD, LCM, và Euclid",
    "Thuật toán cổ nhất trong sách — và đồng nhất thức giữ lcm nằm trong phạm vi kiểu dữ liệu.",
    """## gcd bằng Euclid

```cpp
long long gcd(long long a, long long b) {
    while (b) { long long t = a % b; a = b; b = t; }
    return a;
}
```

Mỗi bước thay (a, b) bằng (b, a mod b); gcd bất biến vì mọi ước chung
của a và b đều chia hết a mod b = a - (a/b)*b. Dừng: b giảm ngặt và luôn
>= 0. Độ phức tạp O(log min(a, b)) — trường hợp xấu là Fibonacci.
gcd(a, 0) = a khép vòng lặp.

### lcm — với thứ tự an toàn

```cpp
long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;   // chia TRƯỚC
}
```

Thứ tự rất quan trọng: `a * b / gcd` có thể tràn số dù lcm đúng vẫn vừa
long long. Chia trước giữ mọi giá trị trung gian trong cỡ độ lớn của
kết quả cuối.

### Nhiều số

gcd(a, b, c) = gcd(gcd(a, b), c) — gộp dần. LCM cũng vậy, canh tràn số
từng bước.

### gcd xuất hiện ở đâu trong thi đấu

- "Rút gọn phân số" — chia cả tử mẫu cho gcd.
- "Hai bước dài khác nhau có gặp nhau không?" — các vị trí tới được là
  bội của gcd.
- Đếm điểm nguyên trên đoạn thẳng: gcd của hiệu tọa độ.
""",
)

write_lesson(
    M,
    "hsg-m11-divisors",
    "Divisors and Primes in O(sqrt n)",
    "Divisors come in pairs; primes are just the absence of them.",
    13,
    """## Divisor pairs

If d divides n, then n/d also divides n. One of the pair is at most
sqrt(n) — so enumerate the small partner only:

```cpp
vector<long long> divisors(long long n) {
    vector<long long> small, big;
    for (long long d = 1; d * d <= n; ++d)
        if (n % d == 0) {
            small.push_back(d);
            if (d != n / d) big.push_back(n / d);
        }
    // merge small (ascending) with big (reversed): sorted divisors
    return small;
}
```

Loop condition `d * d <= n` (not `d <= sqrt(n)`) avoids floating point
entirely. The `d != n/d` check keeps perfect squares from listing sqrt(n)
twice.

### Primality

A prime has no divisor pair except (1, n):

```cpp
bool isPrime(long long n) {
    if (n < 2) return false;
    for (long long d = 2; d * d <= n; ++d)
        if (n % d == 0) return false;
    return true;
}
```

O(sqrt n). n = 10^12 needs 10^6 iterations — fine. Trial division by
every number up to n is O(n) and fails the same test. Do not "optimize"
by checking only odd d and forgetting 2.

### Counting divisors without listing

Iterate the same pairs and add 1 (or 2, or 1 for the square root):

```cpp
long long countDivisors(long long n) {
    long long cnt = 0;
    for (long long d = 1; d * d <= n; ++d)
        if (n % d == 0) cnt += (d == n / d) ? 1 : 2;
    return cnt;
}
```

### Digit sum

```cpp
long long digitSum(long long n) {
    long long s = 0;
    while (n) { s += n % 10; n /= 10; }
    return s;
}
```

Note: n % 10 and n /= 10 work on the absolute value — for negatives,
take abs first (C++ division truncates toward zero, so the sign survives
in n until n becomes 0; the digits come out positive anyway, but the
cleanest is n = llabs(n) at the top).
""",
    "Ước và số nguyên tố trong O(sqrt n)",
    "Ước luôn đi theo cặp; số nguyên tố chỉ là sự vắng mặt của chúng.",
    """## Cặp ước

Nếu d chia hết n thì n/d cũng chia hết n. Một trong hai không vượt
sqrt(n) — nên chỉ cần vét các ước nhỏ:

```cpp
for (long long d = 1; d * d <= n; ++d)
    if (n % d == 0) {
        // d và n/d là hai ước; d == n/d khi n là số chính phương
    }
```

Điều kiện vòng `d * d <= n` (không phải `d <= sqrt(n)`) tránh hoàn toàn
số thực. Kiểm tra `d != n/d` tránh liệt kê sqrt(n) hai lần với số chính
phương.

### Nguyên tố

Số nguyên tố không có cặp ước nào ngoài (1, n):

```cpp
bool isPrime(long long n) {
    if (n < 2) return false;
    for (long long d = 2; d * d <= n; ++d)
        if (n % d == 0) return false;
    return true;
}
```

O(sqrt n). n = 10^12 cần 10^6 vòng — ổn. Thử chia tới n là O(n) và fail
cùng test đó. Đừng "tối ưu" chỉ thử d lẻ rồi quên số 2.

### Đếm ước không cần liệt kê

Cùng vòng lặp, cộng 1 (hoặc 2, hoặc 1 cho căn):

```cpp
long long countDivisors(long long n) {
    long long cnt = 0;
    for (long long d = 1; d * d <= n; ++d)
        if (n % d == 0) cnt += (d == n / d) ? 1 : 2;
    return cnt;
}
```

### Tổng chữ số

```cpp
long long digitSum(long long n) {
    long long s = 0;
    while (n) { s += n % 10; n /= 10; }
    return s;
}
```

Lưu ý: với số âm, lấy abs trước — phép chia của C++ cắt về 0 nên chữ số
rút ra vẫn đúng, nhưng viết `n = llabs(n)` ngay từ đầu cho sạch.
""",
)

A1 = challenge(
    "hsg-p11-gcd-lcm",
    "GCD and LCM",
    T(
        "**Description:** For each pair (a, b), print gcd(a, b) and lcm(a, b) on one line,",
        "space-separated.",
        "",
        "**Input:** Line 1: t (1 <= t <= 10^5). Each of the next t lines: a b",
        "(1 <= a, b <= 10^12; guaranteed lcm(a, b) <= 10^18).",
        "**Output:** t lines: `g l`.",
        "",
        "**Example:** `12 18` -> `6 36`.",
    ),
    [
        contest_test("sample", T("1", "12 18"), T("6 36"),
                     "gcd 6; lcm = 12/6*18 = 36."),
        contest_test("equal", T("1", "7 7"), T("7 7"),
                     "gcd = lcm = the number itself."),
        contest_test("coprime", T("1", "9 10"), T("1 90"),
                     "gcd 1, lcm is the product — fits easily in long long."),
        contest_test("one divides other", T("1", "1000000000000 4"), T("4 1000000000000"),
                     "12*10^11 scale: int is impossible here."),
        contest_test("equal huge", T("1", "1000000000000 1000000000000"), T("1000000000000 1000000000000"),
                     "a*b is 10^24 — a multiply-first lcm overflows here; divide-first stays exact."),
    ],
    level="imitation",
    difficulty="beginner",
)

A2 = challenge(
    "hsg-p11-divcount",
    "Count the Divisors",
    T(
        "**Description:** For each query n, print the number of positive divisors of n.",
        "",
        "**Input:** Line 1: t (1 <= t <= 10^5). Each of the next t lines: n",
        "(1 <= n <= 10^12).",
        "**Output:** t lines — the divisor counts.",
        "",
        "**Example:** `12` -> `6` (1, 2, 3, 4, 6, 12).",
    ),
    [
        contest_test("sample", T("1", "12"), T("6"),
                     "1, 2, 3, 4, 6, 12."),
        contest_test("prime", T("1", "999999999989"), T("2"),
                     "A large prime: only 1 and itself — the O(sqrt n) loop must finish fast."),
        contest_test("perfect square", T("1", "36"), T("9"),
                     "Divisors 1 2 3 4 6 9 12 18 36 — the sqrt (6) counts once."),
        contest_test("one", T("1", "1"), T("1"),
                     "1 has exactly one divisor: itself."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p11-prime",
    "Prime Verdict",
    T(
        "**Description:** For each query n, print `PRIME` if n is prime, `COMPOSITE` if it has",
        "a divisor other than 1 and itself, and `NEITHER` for n < 2.",
        "",
        "**Input:** Line 1: t (1 <= t <= 10^5). Each of the next t lines: n (0 <= n <= 10^12).",
        "**Output:** t lines: `PRIME`, `COMPOSITE`, or `NEITHER`.",
        "",
        "**Example:** `7` -> `PRIME`; `9` -> `COMPOSITE`; `1` -> `NEITHER`.",
    ),
    [
        contest_test("sample", T("3", "7", "9", "1"), T("PRIME", "COMPOSITE", "NEITHER"),
                     "7 prime; 9 = 3*3; 1 is neither."),
        contest_test("zero", T("1", "0"), T("NEITHER"),
                     "0 is not prime by definition."),
        contest_test("two", T("1", "2"), T("PRIME"),
                     "The only even prime — a d = 2, then odd-only loop handles it."),
        contest_test("even composite", T("1", "4"), T("COMPOSITE"),
                     "Divisible by 2 — a solver starting at d = 3 calls this PRIME."),
        contest_test("big prime", T("1", "1000000007"), T("PRIME"),
                     "The classic contest modulus — trial division reaches sqrt ~ 31623."),
    ],
    level="guided",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p11-digitsum",
    "Digit Sum Chain",
    T(
        "**Description:** Apply the digit-sum operation to n repeatedly (n -> digitSum(n)) until",
        "the result has a single digit. Count how many applications were needed.",
        "",
        "**Input:** One line: n (0 <= n <= 10^18).",
        "**Output:** One integer — the number of digit-sum applications to reach one digit.",
        "",
        "**Example:** `9875` -> `3` (9875 -> 29 -> 11 -> 2).",
    ),
    [
        contest_test("sample", T("9875"), T("3"),
                     "9875 -> 29 -> 11 -> 2: three applications."),
        contest_test("already single", T("5"), T("0"),
                     "Single digit: zero applications."),
        contest_test("max input", T("999999999999999999"), T("2"),
                     "18 nines sum to 162; 1+6+2 = 9 — two applications."),
        contest_test("zero", T("0"), T("0"),
                     "Zero is already a single digit."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p11-sum-div",
    "Sum of Divisors",
    T(
        "**Description:** For each query n, print the sum of all positive divisors of n",
        "(including 1 and n), modulo 10^9 + 7.",
        "",
        "**Input:** Line 1: t (1 <= t <= 10^5). Each of the next t lines: n",
        "(1 <= n <= 10^12).",
        "**Output:** t lines — the divisor sums mod 10^9 + 7.",
        "",
        "**Example:** `12` -> `28` (1+2+3+4+6+12 = 28).",
    ),
    [
        contest_test("sample", T("1", "12"), T("28"),
                     "1+2+3+4+6+12."),
        contest_test("prime", T("1", "13"), T("14"),
                     "1 + 13."),
        contest_test("square", T("1", "16"), T("31"),
                     "1+2+4+8+16 — the sqrt counts once."),
        contest_test("one", T("1", "1"), T("1"),
                     "The sum is just 1."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p11-gcd-lcm": vi_challenge(
        "GCD và LCM",
        T(
            "**Đề bài:** Với mỗi cặp (a, b), in gcd(a, b) và lcm(a, b) trên một dòng, cách nhau bởi dấu cách.",
            "",
            "**Dữ liệu vào:** Dòng 1: t (1 <= t <= 10^5). t dòng tiếp: a b (1 <= a, b <= 10^12; đảm bảo lcm(a, b) <= 10^18).",
            "**Dữ liệu ra:** t dòng: `g l`.",
            "",
            "**Ví dụ:** `12 18` -> `6 36`.",
        ),
        [
            ("sample", "gcd 6; lcm = 12/6*18 = 36."),
            ("equal", "gcd = lcm = chính số đó."),
            ("coprime", "gcd 1, lcm là tích — vừa dễ dàng trong long long."),
            ("one divides other", "Cỡ 12*10^11: int bất khả thi ở đây."),
            ("equal huge", "a*b là 10^24 — lcm nhân-trước tràn ở đây; chia-trước vẫn chính xác."),
        ],
    ),
    "hsg-p11-divcount": vi_challenge(
        "Đếm ước",
        T(
            "**Đề bài:** Với mỗi truy vấn n, in số lượng ước nguyên dương của n.",
            "",
            "**Dữ liệu vào:** Dòng 1: t (1 <= t <= 10^5). t dòng tiếp: n (1 <= n <= 10^12).",
            "**Dữ liệu ra:** t dòng — số ước.",
            "",
            "**Ví dụ:** `12` -> `6` (1, 2, 3, 4, 6, 12).",
        ),
        [
            ("sample", "1, 2, 3, 4, 6, 12."),
            ("prime", "Số nguyên tố lớn: chỉ 1 và chính nó — vòng O(sqrt n) phải kết thúc nhanh."),
            ("perfect square", "Các ước 1 2 3 4 6 9 12 18 36 — căn (6) chỉ đếm một lần."),
            ("one", "1 có đúng một ước: chính nó."),
        ],
    ),
    "hsg-p11-prime": vi_challenge(
        "Phán quyết nguyên tố",
        T(
            "**Đề bài:** Với mỗi truy vấn n, in `PRIME` nếu n nguyên tố, `COMPOSITE` nếu có ước",
            "khác 1 và chính nó, và `NEITHER` cho n < 2.",
            "",
            "**Dữ liệu vào:** Dòng 1: t (1 <= t <= 10^5). t dòng tiếp: n (0 <= n <= 10^12).",
            "**Dữ liệu ra:** t dòng: `PRIME`, `COMPOSITE`, hoặc `NEITHER`.",
            "",
            "**Ví dụ:** `7` -> `PRIME`; `9` -> `COMPOSITE`; `1` -> `NEITHER`.",
        ),
        [
            ("sample", "7 nguyên tố; 9 = 3*3; 1 chẳng phải cái gì."),
            ("zero", "0 không nguyên tố theo định nghĩa."),
            ("two", "Số nguyên tố chẵn duy nhất — vòng d = 2 rồi chỉ d lẻ xử lý được."),
            ("even composite", "Chia hết cho 2 — lời giải bắt đầu từ d = 3 sẽ bảo đây là PRIME."),
            ("big prime", "Modulo kinh điển của thi đấu — thử chia tới sqrt ~ 31623."),
        ],
    ),
    "hsg-p11-digitsum": vi_challenge(
        "Chuỗi tổng chữ số",
        T(
            "**Đề bài:** Lặp phép tổng chữ số với n (n -> digitSum(n)) cho tới khi kết quả có một chữ số.",
            "Đếm số lần áp dụng.",
            "",
            "**Dữ liệu vào:** Một dòng: n (0 <= n <= 10^18).",
            "**Dữ liệu ra:** Một số nguyên — số lần áp dụng để còn một chữ số.",
            "",
            "**Ví dụ:** `9875` -> `3` (9875 -> 29 -> 11 -> 2).",
        ),
        [
            ("sample", "9875 -> 29 -> 11 -> 2: ba lần áp dụng."),
            ("already single", "Một chữ số: không áp dụng lần nào."),
            ("max input", "18 số 9 -> 162 -> 9: hai lần áp dụng."),
            ("zero", "Số 0 đã là một chữ số."),
        ],
    ),
    "hsg-p11-sum-div": vi_challenge(
        "Tổng ước",
        T(
            "**Đề bài:** Với mỗi truy vấn n, in tổng mọi ước nguyên dương của n",
            "(bao gồm 1 và n), modulo 10^9 + 7.",
            "",
            "**Dữ liệu vào:** Dòng 1: t (1 <= t <= 10^5). t dòng tiếp: n (1 <= n <= 10^12).",
            "**Dữ liệu ra:** t dòng — tổng ước mod 10^9 + 7.",
            "",
            "**Ví dụ:** `12` -> `28` (1+2+3+4+6+12 = 28).",
        ),
        [
            ("sample", "1+2+3+4+6+12."),
            ("prime", "1 + 13."),
            ("square", "1+2+4+8+16 — căn chỉ đếm một lần."),
            ("one", "Tổng chỉ là 1."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p11-number",
    "Number Theory Problem Set",
    "gcd/lcm, divisor counting, primality, digit chains, and divisor sums — all O(sqrt n) drills.",
    "Bài tập số học",
    "gcd/lcm, đếm ước, nguyên tố, chuỗi chữ số, và tổng ước — tất cả luyện O(sqrt n).",
    "hsg-m11-divisors",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p11-gcd-lcm",
            GCD_DEF + CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long a, b; in >> a >> b;
        long long g = gcdll(a, b);
        out << g << " " << a / g * b << "{{NL}}";
    }
""") + END,
            GCD_DEF + CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long a, b; in >> a >> b;
        long long g = gcdll(a, b);
        // near-miss: multiplies before dividing — a*b can overflow
        // long long when both approach 10^12... here inputs cap at
        // 10^12 each so the product reaches 10^24: guaranteed wrong
        out << g << " " << a * b / g << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsg-p11-divcount",
            CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long n; in >> n;
        long long cnt = 0;
        for (long long d = 1; d * d <= n; ++d)
            if (n % d == 0) cnt += (d == n / d) ? 1 : 2;
        out << cnt << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long n; in >> n;
        long long cnt = 0;
        for (long long d = 1; d * d <= n; ++d)
            // near-miss: counts 2 for perfect-square roots too
            if (n % d == 0) cnt += 2;
        out << cnt << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsg-p11-prime",
            CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long n; in >> n;
        if (n < 2) { out << "NEITHER" << "{{NL}}"; continue; }
        bool prime = true;
        for (long long d = 2; d * d <= n; ++d)
            if (n % d == 0) { prime = false; break; }
        out << (prime ? "PRIME" : "COMPOSITE") << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long n; in >> n;
        if (n < 2) { out << "NEITHER" << "{{NL}}"; continue; }
        bool prime = true;
        // near-miss: starts at d = 3 — forgets the only even prime
        // and misses every even composite (4, 6, 10, ... say PRIME)
        for (long long d = 3; d * d <= n; ++d)
            if (n % d == 0) { prime = false; break; }
        out << (prime ? "PRIME" : "COMPOSITE") << "{{NL}}";
    }
""") + END,
        ),
        (
            "hsg-p11-digitsum",
            CPP_STD + cpp("""    long long n; in >> n;
    long long steps = 0;
    while (n >= 10) {
        long long s = 0;
        while (n) { s += n % 10; n /= 10; }
        n = s;
        ++steps;
    }
    out << steps << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long n; in >> n;
    long long steps = 0;
    ++steps;  // near-miss: counts one step up front — a single-digit
              // input reports 1 instead of 0, everything shifts by one
    while (n >= 10) {
        long long s = 0;
        while (n) { s += n % 10; n /= 10; }
        n = s;
        ++steps;
    }
    out << steps << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p11-sum-div",
            CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long n; in >> n;
        long long sum = 0;
        for (long long d = 1; d * d <= n; ++d)
            if (n % d == 0) {
                sum += d;
                if (d != n / d) sum += n / d;
            }
        out << sum % 1000000007 << "{{NL}}";
    }
""") + END,
            CPP_STD + cpp("""    int t; in >> t;
    while (t--) {
        long long n; in >> n;
        long long sum = 0;
        for (long long d = 1; d * d <= n; ++d)
            if (n % d == 0) {
                sum += d;
                // near-miss: adds the pair unconditionally — perfect
                // squares double-count their root
                sum += n / d;
            }
        out << sum % 1000000007 << "{{NL}}";
    }
""") + END,
        ),
    ],
)

CH11 = challenge(
    "hsg-cp-m11-nk",
    "Divisible by Both",
    T(
        "**Description:** Count the integers in [1, n] divisible by **a or b**",
        "(inclusive or). Use inclusion-exclusion with lcm — do not loop to n.",
        "",
        "**Input:** One line: n a b (1 <= n <= 10^18, 1 <= a, b <= 10^9).",
        "**Output:** One integer — the count.",
        "",
        "**Example:** `10 2 3` -> `7` (2, 3, 4, 6, 8, 9, 10).",
    ),
    [
        contest_test("sample", T("10 2 3"), T("7"),
                     "floor(10/2)=5, floor(10/3)=3, floor(10/6)=1: 5+3-1=7."),
        contest_test("coprime big n", T("1000000000000000000 2 3"), T("666666666666666667"),
                     "5*10^17 + 3.33...*10^17 - 1.66...*10^17 — all 64-bit math."),
        contest_test("a divides b", T("20 4 8"), T("5"),
                     "Multiples of 8 are already multiples of 4 — the union is the 5 multiples of 4."),
        contest_test("a equals b", T("9 5 5"), T("1"),
                     "Same divisor counted once."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP11 = vi_challenge(
    "Chia hết cho một trong hai",
    T(
        "**Đề bài:** Đếm các số nguyên trong [1, n] chia hết cho **a hoặc b**",
        "(hoặc cả hai). Dùng bao hàm - loại trừ với lcm — đừng vòng tới n.",
        "",
        "**Dữ liệu vào:** Một dòng: n a b (1 <= n <= 10^18, 1 <= a, b <= 10^9).",
        "**Dữ liệu ra:** Một số nguyên — số lượng.",
        "",
        "**Ví dụ:** `10 2 3` -> `7` (2, 3, 4, 6, 8, 9, 10).",
    ),
    [
        ("sample", "floor(10/2)=5, floor(10/3)=3, floor(10/6)=1: 5+3-1=7."),
        ("coprime big n", "5*10^17 + 3.33...*10^17 - 1.66...*10^17 — toàn bộ là số học 64 bit."),
        ("a divides b", "Bội của 8 đã là bội của 4 — hợp đúng là 5 bội của 4."),
        ("a equals b", "Cùng một ước chỉ đếm một lần."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m11",
    "Checkpoint — Number Theory",
    "Pass the graded problem to finish the number-theory module.",
    15,
    """**Checkpoint — số học.** Pass the graded challenge below. It fuses
gcd (via lcm), inclusion-exclusion, and floor-division counting. The
danger zone is the order of operations in lcm and the 64-bit range of
n: every intermediate value must stay inside long long. Solve the
sample by hand, then generalize.

**Điểm kiểm tra — số học.** Pass bài chấm bên dưới. Bài gộp gcd (qua
lcm), bao hàm - loại trừ, và đếm bằng phép chia lấy phần nguyên. Vùng
nguy hiểm là thứ tự phép tính trong lcm và khoảng 64 bit của n: mọi giá
trị trung gian phải nằm gọn trong long long. Giải mẫu bằng tay, rồi
tổng quát hóa.
""",
    "Checkpoint — Number Theory",
    "Pass the graded problem to finish the number-theory module.",
    """**Điểm kiểm tra — số học.** Pass bài chấm bên dưới. Bài gộp gcd (qua
lcm), bao hàm - loại trừ, và đếm bằng phép chia lấy phần nguyên. Vùng
nguy hiểm là thứ tự phép tính trong lcm và khoảng 64 bit của n: mọi giá
trị trung gian phải nằm gọn trong long long. Giải mẫu bằng tay, rồi
tổng quát hóa.
""",
    CH11,
    VI_CP11,
    solution=GCD_DEF + CPP_STD + cpp("""    long long n, a, b; in >> n >> a >> b;
    long long g = gcdll(a, b);
    long long l = a / g * b;
    long long cnt = n / a + n / b - n / l;
    out << cnt << "{{NL}}";
""") + END,
    wrong=GCD_DEF + CPP_STD + cpp("""    long long n, a, b; in >> n >> a >> b;
    long long g = gcdll(a, b);
    long long l = a / g * b;
    // near-miss: counts the INTERSECTION twice (adds instead of
    // subtracts) — inclusion without the exclusion
    long long cnt = n / a + n / b + n / l;
    out << cnt << "{{NL}}";
""") + END,
)

print("M11 done")
