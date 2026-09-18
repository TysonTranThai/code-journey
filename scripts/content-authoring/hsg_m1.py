#!/usr/bin/env python3
"""HSG — Module 1: hsg-vao-mon (contest reading + C++ bridge + first problems).

Main files are English; .vi.* overlays are Vietnamese (repo convention).
Teaches reading a real contest statement, the verdict taxonomy, and the
solve(istream&, ostream&) convention. First problems drill constraint
reading (the a+b overflow lesson), classification boundaries, and the
negative-modulo trap.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsg import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, contest_test, write_course, write_track,
)

M = "hsg-vao-mon"

# ---------------------------------------------------------------- lessons
write_module(
    M,
    "Contest Reading & the C++ Bridge",
    "Read a real statement (input/output/constraints/examples), understand judge verdicts, and take the solve(istream&, ostream&) convention used across the whole track.",
    "Vào môn thi đấu",
    "Đọc một đề thật (dữ liệu vào/ra, giới hạn, ví dụ), hiểu các phán quyết của chấm bài, và làm quen quy ước solve(istream&, ostream&) dùng xuyên suốt lộ trình.",
    ["hsg-m1-reading", "hsg-m1-bridge", "hsg-cp-m1"],
    ["hsg-p1-first"],
)

write_lesson(
    M, "hsg-m1-reading",
    "How to Read a Contest Problem",
    "Statement, input/output format, constraints, examples — and the checklist to run before writing code.",
    14,
    """## Reading a real contest problem

A standard HSG problem has five blocks:

```text
PROBLEM: Sum of two numbers
DESCRIPTION: Given two integers a, b. Print their sum.
INPUT: One line with two integers a and b (a, b ≤ 10^18).
OUTPUT: Print a + b.
EXAMPLE: (sample input → sample output)
CONSTRAINTS: 30% of tests have a, b ≤ 10^9; 100% have a, b ≤ 10^18.
```

**Input/Output** is your *contract* with the judge: wrong format, a missing
space, a missing newline = wrong answer even with a correct algorithm.
**Constraints** are the biggest hint of all: they tell you which algorithm
is fast enough (next module).

### The pre-keyboard checklist

1. What **exactly** is being asked? (one number? a line? several?)
2. Read the data types: what is the largest possible value?
3. What happens at the smallest input?
4. Are there **subtasks**? Which points can a simple solution earn?

### Judge verdicts

| Verdict | Meaning |
| --- | --- |
| Accepted | All tests passed |
| Wrong Answer | It ran, but the output is wrong |
| Time Limit Exceeded | Too slow — the algorithm itself must change |
| Runtime Error | It crashed (division by zero, bad index, stack overflow…) |
| Compile Error | It never compiled |

### This course's convention

You write `void solve(istream& in, ostream& out)` — read from `in` as if
it were `cin`, write to `out` as if it were `cout`. The system calls
`solve(cin, cout)` for you — exactly what a contest judge does with your
program.""",
    "Cách đọc một đề thi thực sự",
    "Cấu trúc đề (mô tả, dữ liệu vào/ra, giới hạn, ví dụ), checklist trước khi gõ phím, và các phán quyết của chấm bài.",
    """## Đọc một đề thi thực sự như thế nào?

Một bài HSG tiêu chuẩn có năm khối:

```text
TÊN BÀI: Tổng hai số
MÔ TẢ: Cho hai số nguyên a, b. Hãy tính tổng của chúng.
DỮ LIỆU VÀO: Một dòng ghi hai số nguyên a và b (a, b ≤ 10^18).
DỮ LIỆU RA: In ra tổng a + b.
VÍ DỤ: (đầu vào → đầu ra mẫu)
GIỚI HẠN: 30% test có a, b ≤ 10^9; 100% test có a, b ≤ 10^18.
```

**Dữ liệu vào / Dữ liệu ra** là *hợp đồng* với chấm bài: sai format, sai
dấu cách, thiếu xuống dòng = sai dù thuật toán đúng. **Giới hạn** là gợi
ý lớn nhất: nó nói cho bạn biết thuật toán nào đủ nhanh (module sau).

### Checklist trước khi gõ phím

1. Bài yêu cầu **chính xác cái gì**? (một số? một dòng? nhiều dòng?)
2. Đọc kiểu dữ liệu: giá trị lớn nhất là bao nhiêu?
3. Input nhỏ nhất thì sao?
4. Có **subtask** không? Điểm nào lấy được bằng cách đơn giản?

### Phán quyết của chấm bài

| Verdict | Nghĩa là |
| --- | --- |
| Accepted | Đúng hết test |
| Wrong Answer | Chạy xong nhưng output sai |
| Time Limit Exceeded | Quá chậm — phải đổi thuật toán |
| Runtime Error | Sập lúc chạy (chia 0, chỉ số sai, stack tràn…) |
| Compile Error | Chưa vượt qua bước biên dịch |

### Quy ước của khóa

Bạn viết `void solve(istream& in, ostream& out)` — đọc từ `in` như `cin`,
ghi ra `out` như `cout`. Hệ thống tự gọi `solve(cin, cout)` — đúng như
chấm bài thi xử lý chương trình của bạn.""",
)

write_lesson(
    M, "hsg-m1-bridge",
    "C++ for Contests: the 10-Minute Bridge",
    "Types, I/O, vector, loops — the exact C++ slice HSG problems need, plus fast I/O and the long long rule.",
    12,
    """## The minimal C++ for contests

This course assumes you know variables, loops, and functions from a first
programming course (or you are taking `cpp-beginner` alongside). This is
*exactly the slice contest problems need*.

### Data types — the golden rule

```cpp
int a;        // up to ~2.1 * 10^9 — LIMITED
long long x;  // up to ~9.2 * 10^18 — THE CONTEST DEFAULT
```

On scratch paper: 10^9 + 10^9 = 2·10^9 overflows `int`. If a sum can pass
2.1·10^9, **the whole computation must be `long long`**. This is the #1
wrong-answer cause for beginners.

### Fast input/output

```cpp
ios_base::sync_with_stdio(false);
cin.tie(nullptr);
```

The two standard contest lines: disable C-stdio synchronization and the
per-read flush. With million-number inputs the difference is dramatic.

### vector — every problem's array

```cpp
int n; in >> n;
vector<long long> a(n);
for (long long& x : a) in >> x;   // read n elements
sort(a.begin(), a.end());          // STL sort (sorting module)
```

`for (long long& x : a)` — the `&` makes it writable and avoids copies.

### The solve convention

```cpp
void solve(istream& in, ostream& out) {
    long long a, b;
    in >> a >> b;
    out << a + b << "\\n";
}
```

All contest logic lives in `solve`; the system calls `solve(cin, cout)`.""",
    "C++ cho thi đấu: cầu nối 10 phút",
    "Kiểu dữ liệu (quy tắc long long), nhập xuất nhanh, vector, và quy ước solve của khóa.",
    """## C++ tối thiểu để thi

Khóa này giả định bạn đã biết biến, vòng lặp, hàm từ một khóa lập trình
cơ bản (hoặc bạn đang học song song `cpp-beginner`). Phần dưới đây là
*đúng những gì đề thi cần*.

### Kiểu dữ liệu — quy tắc vàng

```cpp
int a;        // đến ~2.1 * 10^9 — HẠN CHẾ
long long x;  // đến ~9.2 * 10^18 — MẶC ĐỊNH trong thi
```

Trên giấy nháp: 10^9 + 10^9 = 2·10^9 vượt `int`. Nếu tổng có thể vượt
2.1·10^9 thì **cả phép tính phải dùng `long long`**. Đây là lý do WA số 1
của người mới.

### Nhập xuất nhanh

```cpp
ios_base::sync_with_stdio(false);
cin.tie(nullptr);
```

Hai dòng chuẩn thi đấu: tắt đồng bộ với C I/O, tắt flush mỗi lần đọc. Với
input hàng triệu số, khác biệt là rất lớn.

### Vector — mảng của mọi bài thi

```cpp
int n; in >> n;
vector<long long> a(n);
for (long long& x : a) in >> x;   // đọc n phần tử
sort(a.begin(), a.end());          // STL sort (module sắp xếp)
```

`for (long long& x : a)` — dấu `&` giúp đọc-vừa-sửa và tránh copy.

### Quy ước solve

```cpp
void solve(istream& in, ostream& out) {
    long long a, b;
    in >> a >> b;
    out << a + b << "\\n";
}
```

Toàn bộ logic nằm trong `solve`; hệ thống tự gọi `solve(cin, cout)`.""",
)

# ---------------------------------------------------------------- practice
CH1 = challenge(
    "hsg-p1-sum",
    "Sum of Two Numbers",
    """**Description:** Given two integers a, b. Print their sum.

**Input:** One line: a b (−10^9 ≤ a, b ≤ 10^9).
**Output:** One integer — a + b.

**Example:** input `2 3` → output `5`.

*Subtask hint:* with these bounds the sum reaches 2·10^9 — which type fits?""",
    [
        contest_test("sample", "2 3\n", "5\n", "The sum of 2 and 3 is 5."),
        contest_test("two negatives", "-4 -6\n", "-10\n", "Two negatives sum to a negative."),
        contest_test("symmetric bounds", "-1000000000 1000000000\n", "0\n", "Symmetric values cancel to 0."),
        contest_test("int overflow", "2000000000 2000000000\n", "4000000000\n", "2·10^9 + 2·10^9 overflows int — long long handles it."),
    ],
    level="imitation",
)

CH2 = challenge(
    "hsg-p1-max3",
    "Maximum of Three",
    """**Description:** Given three integers a, b, c. Print the largest.

**Input:** One line: a b c (−10^9 ≤ each ≤ 10^9).
**Output:** One integer — the maximum.

**Example:** input `3 7 5` → output `7`.

*Question:* what if all three are equal?""",
    [
        contest_test("sample", "3 7 5\n", "7\n", "7 is the largest of 3, 7, 5."),
        contest_test("all equal", "4 4 4\n", "4\n", "All equal → the max is 4."),
        contest_test("all negative", "-5 -2 -9\n", "-2\n", "The 'largest' can still be negative."),
        contest_test("boundary", "0 -1000000000 1000000000\n", "1000000000\n", "Extreme values must be returned correctly."),
    ],
    level="imitation",
)

CH3 = challenge(
    "hsg-p1-parity",
    "Even or Odd",
    """**Description:** Given an integer n. Print `CHAN` if n is even, `LE` if odd.

**Input:** One integer n (−10^9 ≤ n ≤ 10^9).
**Output:** `CHAN` or `LE`.

**Example:** `10` → `CHAN`; `7` → `LE`.

*Careful:* how does C++ `%` behave for negative n?""",
    [
        contest_test("positive even", "10\n", "CHAN\n", "10 is divisible by 2 → CHAN."),
        contest_test("positive odd", "7\n", "LE\n", "7 is not divisible by 2 → LE."),
        contest_test("zero", "0\n", "CHAN\n", "0 is even."),
        contest_test("negative odd", "-7\n", "LE\n", "-7 % 2 is -1 in C++ — test `n % 2 != 0`, never `== 1`."),
    ],
    level="guided",
)

CH4 = challenge(
    "hsg-p1-bmi",
    "BMI Category",
    """**Description:** Given a BMI value n (real number), print:
- `GAO` if n < 18.5
- `BINH` if 18.5 ≤ n < 25.0
- `CAO` if n ≥ 25.0

**Input:** One real number n (10.0 ≤ n ≤ 40.0).
**Output:** One word from {GAO, BINH, CAO}.

**Example:** `17.0` → `GAO`; `18.5` → `BINH`; `25.0` → `CAO`.

*Mind the boundaries:* exactly 18.5 is BINH, exactly 25.0 is CAO.""",
    [
        contest_test("under", "17.0\n", "GAO\n", "< 18.5 is GAO."),
        contest_test("lower boundary", "18.5\n", "BINH\n", "Exactly 18.5 belongs to BINH (≥)."),
        contest_test("middle", "22.7\n", "BINH\n", "18.5 ≤ n < 25.0 is BINH."),
        contest_test("upper boundary", "25.0\n", "CAO\n", "Exactly 25.0 belongs to CAO (≥)."),
    ],
    level="guided",
)

CH5 = challenge(
    "hsg-p1-score-tier",
    "Grade Tier",
    """**Description:** Given a score n (0 ≤ n ≤ 10, real number), print:
- `A` if n ≥ 8.0
- `B` if 6.5 ≤ n < 8.0
- `C` if 5.0 ≤ n < 6.5
- `D` if n < 5.0

**Input:** One real number n.
**Output:** One letter {A, B, C, D}.

**Example:** `8.0` → `A`; `6.5` → `B`; `4.9` → `D`.""",
    [
        contest_test("A at boundary", "8.0\n", "A\n", "n ≥ 8.0 → A."),
        contest_test("just under A", "7.99\n", "B\n", "7.99 < 8.0 → not A."),
        contest_test("B boundary", "6.5\n", "B\n", "6.5 sits on the B boundary."),
        contest_test("lowest", "0.0\n", "D\n", "0 is the minimum → D."),
    ],
    level="independent",
)

CH6 = challenge(
    "hsg-p1-timezone",
    "Clock Arithmetic",
    """**Description:** Given t (minutes, possibly negative) and k (a time-zone
offset, 0 ≤ k ≤ 23) on one line `t k`. Total minutes = t + k·60. Print the
hour of day in 24-hour form (a number 0..23).

**Input:** One line: t k (−10^7 ≤ t ≤ 10^7, 0 ≤ k ≤ 23).
**Output:** One integer 0..23.

**Example:** `90 1` → (90 + 60)/60 = 2 → print `2`;
`-30 0` → −30/60 = −1 hours → must wrap to 23.

*Question:* which way does C++ integer division round for negatives?
(`((x % 24) + 24) % 24` is your friend.)""",
    [
        contest_test("positive sample", "90 1\n", "2\n", "(90+60)/60 = 2."),
        contest_test("negative wraps to 23", "-30 0\n", "23\n", "−30 minutes = −1 hour → wrap to 23 with ((x%24)+24)%24."),
        contest_test("zero", "0 0\n", "0\n", "0 minutes → hour 0."),
        contest_test("large negative", "-10000000 3\n", "16\n", "A large negative total must still wrap into 0..23 correctly."),
    ],
    level="combination",
)

write_practice(
    M, "hsg-p1-first",
    "Starter Set",
    "Four opening problems in real statement format: overflow-safe addition, max/boundary classification, tiering, and clock arithmetic with negative division.",
    "Bộ đề khởi động",
    "Bốn bài mở màn theo đúng định dạng đề thi: cộng tràn kiểu, max/điều kiện biên, phân loại, và phép chia âm.",
    "hsg-m1-bridge",
    45,
    "beginner",
    [CH1, CH2, CH3, CH4, CH5, CH6],
    {
        "hsg-p1-sum": vi_challenge("Tổng hai số", "**Mô tả:** Cho hai số nguyên a, b. In ra tổng của chúng.\n\n**Dữ liệu vào:** Một dòng: a b (−10^9 ≤ a, b ≤ 10^9).\n**Dữ liệu ra:** Một số nguyên — tổng a + b.\n\n**Ví dụ:** nhập `2 3` → in `5`.", [("ví dụ đề bài", "Kết quả phải là 5."), ("hai số âm", "Tổng hai số âm là âm."), ("cận âm dương", "Đối xứng qua 0 thì tổng bằng 0."), ("tổng vượt int", "2·10^9 + 2·10^9 vượt int — kiểu long long thì thoải mái.")]),
        "hsg-p1-max3": vi_challenge("Số lớn nhất trong ba", "**Mô tả:** Cho ba số nguyên a, b, c. In số lớn nhất.\n\n**Dữ liệu vào:** Một dòng: a b c (−10^9 ≤ mỗi số ≤ 10^9).\n**Dữ liệu ra:** Một số nguyên — giá trị lớn nhất.\n\n**Ví dụ:** nhập `3 7 5` → in `7`.", [("ví dụ đề bài", "Giữa 3, 7, 5 thì 7 lớn nhất."), ("số bằng nhau", "Cả ba bằng nhau → max vẫn là 4."), ("toàn âm", "Số 'lớn nhất' vẫn có thể âm."), ("biên", "Cận trị phải được trả về đúng.")]),
        "hsg-p1-parity": vi_challenge("Chẵn hay lẻ", "**Mô tả:** Cho số nguyên n. In `CHAN` nếu n chẵn, `LE` nếu n lẻ.\n\n**Dữ liệu vào:** Một số nguyên n (−10^9 ≤ n ≤ 10^9).\n**Dữ liệu ra:** `CHAN` hoặc `LE`.\n\n**Ví dụ:** nhập `10` → in `CHAN`; nhập `7` → in `LE`.", [("chẵn dương", "10 chia hết cho 2 → CHAN."), ("lẻ dương", "7 không chia hết cho 2 → LE."), ("không", "0 là số chẵn."), ("âm lẻ", "-7 % 2 = -1 trong C++ — kiểm tra `n % 2 != 0`, đừng kiểm tra `== 1`.")]),
        "hsg-p1-bmi": vi_challenge("Phân loại thể trạng", "**Mô tả:** Cho BMI n (số thực). In `GAO` nếu n < 18.5, `BINH` nếu 18.5 ≤ n < 25.0, `CAO` nếu n ≥ 25.0.\n\n**Dữ liệu vào:** Một số thực n (10.0 ≤ n ≤ 40.0).\n**Dữ liệu ra:** Một từ trong {GAO, BINH, CAO}.\n\n**Ví dụ:** `17.0` → `GAO`; `18.5` → `BINH`; `25.0` → `CAO`.", [("gầy", "< 18.5 là GAO."), ("biên dưới", "Đúng 18.5 thuộc BINH (≥)."), ("khoảng giữa", "18.5 ≤ n < 25.0 là BINH."), ("biên trên", "Đúng 25.0 thuộc CAO (≥).")]),
        "hsg-p1-score-tier": vi_challenge("Xếp loại điểm", "**Mô tả:** Cho điểm n (0 ≤ n ≤ 10, số thực). In A nếu n ≥ 8.0, B nếu 6.5 ≤ n < 8.0, C nếu 5.0 ≤ n < 6.5, D nếu n < 5.0.\n\n**Dữ liệu vào:** Một số thực n.\n**Dữ liệu ra:** Một chữ cái {A, B, C, D}.", [("loại A đúng biên", "n ≥ 8.0 → A."), ("dưới A một chút", "7.99 < 8.0 → không phải A."), ("biên B", "6.5 nằm ở biên B."), ("thấp nhất", "0 là nhỏ nhất — thuộc D.")]),
        "hsg-p1-timezone": vi_challenge("Đổi giờ", "**Mô tả:** Cho t (phút, có thể âm) và k (múi giờ, 0 ≤ k ≤ 23) trên một dòng `t k`. Tổng phút là t + k·60. In giờ trong ngày dạng 24h (0..23).\n\n**Dữ liệu vào:** Một dòng: t k.\n**Dữ liệu ra:** Một số nguyên 0..23.\n\n**Ví dụ:** `90 1` → `2`; `-30 0` → `23`.", [("ví dụ dương", "(90+60)/60 = 2."), ("âm về 23", "−30 phút = −1 giờ → quy về 23 bằng floor-mod."), ("không", "0 phút → giờ 0."), ("âm lớn", "Tổng âm lớn vẫn phải quy về 0..23 đúng.")]),
    },
    solutions=[
        (
            "hsg-p1-sum",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long a, b;\n    in >> a >> b;\n    out << (a + b) << \"\\n\";\n}",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    int a, b;\n    in >> a >> b;\n    out << (a + b) << \"\\n\";\n}",
        ),
        (
            "hsg-p1-max3",
            "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    long long a, b, c;\n    in >> a >> b >> c;\n    out << max({a, b, c}) << \"\\n\";\n}",
            "#include <iostream>\n#include <algorithm>\nusing namespace std;\nvoid solve(std::istream& in, std::ostream& out) {\n    long long a, b, c;\n    in >> a >> b >> c;\n    out << min({a, b, c}) << \"\\n\";\n}",
        ),
        (
            "hsg-p1-parity",
            "#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n;\n    in >> n;\n    out << (n % 2 != 0 ? \"LE\" : \"CHAN\") << \"\\n\";\n}",
            "#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long n;\n    in >> n;\n    out << (n % 2 == 1 ? \"LE\" : \"CHAN\") << \"\\n\";\n}",
        ),
        (
            "hsg-p1-bmi",
            "#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    double n;\n    in >> n;\n    if (n < 18.5) out << \"GAO\\n\";\n    else if (n < 25.0) out << \"BINH\\n\";\n    else out << \"CAO\\n\";\n}",
            "#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    double n;\n    in >> n;\n    if (n <= 18.5) out << \"GAO\\n\";\n    else if (n < 25.0) out << \"BINH\\n\";\n    else out << \"CAO\\n\";\n}",
        ),
        (
            "hsg-p1-score-tier",
            "#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    double n;\n    in >> n;\n    if (n >= 8.0) out << \"A\\n\";\n    else if (n >= 6.5) out << \"B\\n\";\n    else if (n >= 5.0) out << \"C\\n\";\n    else out << \"D\\n\";\n}",
            "#include <iostream>\n#include <string>\nvoid solve(std::istream& in, std::ostream& out) {\n    double n;\n    in >> n;\n    if (n > 8.0) out << \"A\\n\";\n    else if (n >= 6.5) out << \"B\\n\";\n    else if (n >= 5.0) out << \"C\\n\";\n    else out << \"D\\n\";\n}",
        ),
        (
            "hsg-p1-timezone",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long t, k;\n    in >> t >> k;\n    long long m = t + k * 60;\n    long long x = ((m % 60) + 60) % 60;   // floor-mod minutes\n    out << (((m - x) / 60 % 24) + 24) % 24 << \"\\n\";\n}",
            "#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long t, k;\n    in >> t >> k;\n    long long m = t + k * 60;\n    // near-miss: C++ division truncates toward zero, so a negative\n    // hour prints negative instead of wrapping into 0..23\n    out << (m / 60) % 24 << \"\\n\";\n}",
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "hsg-cp-m1",
    "Checkpoint — Reading Problems",
    "Pass the graded problem to finish the reading-problems module.",
    15,
    "**Checkpoint — reading problems.** Pass the graded challenge below to finish the module.",
    "Checkpoint — đọc đề",
    "Vượt qua bài chấm cuối module để hoàn thành phần đọc đề và cầu nối C++.",
    "**Checkpoint — đọc đề.** Vượt qua challenge có chấm bên dưới để hoàn thành module.",
    challenge(
        "hsg-cp-m1-fare",
        "Bus Fare",
        """**Description:** A bus line charges as follows: passengers under 6 or
70 and older ride free; everyone from 6 to under 70 pays 7000. Given age
t (0 ≤ t ≤ 120), print the fare.

**Input:** One integer t.
**Output:** One integer — the fare (0 or 7000).

**Example:** `5` → `0`; `6` → `7000`; `70` → `0`.

**Constraints:** 40% of tests have 6 ≤ t ≤ 69; 100% have 0 ≤ t ≤ 120.""",
        [
            contest_test("young child", "5\n", "0\n", "Under 6 rides free."),
            contest_test("boundary age 6", "6\n", "7000\n", "Exactly 6 pays 7000."),
            contest_test("boundary age 70", "70\n", "0\n", "70 and older ride free."),
            contest_test("adult", "35\n", "7000\n", "Ages 6..69 pay 7000."),
        ],
    ),
    vi_challenge("Tiền vé xe buýt", "**Mô tả:** Hành khách dưới 6 tuổi hoặc từ 70 tuổi trở lên miễn phí; người từ 6 đến dưới 70 trả 7000 đồng. Cho tuổi t (0 ≤ t ≤ 120), in số tiền phải trả.\n\n**Dữ liệu vào:** Một số nguyên t.\n**Dữ liệu ra:** Số tiền (0 hoặc 7000).\n\n**Ví dụ:** `5` → `0`; `6` → `7000`; `70` → `0`.", [("trẻ em miễn phí", "Dưới 6 tuổi: 0 đồng."), ("biên 6 tuổi", "Đúng 6 tuổi phải trả 7000."), ("biên 70 tuổi", "Từ 70 tuổi trở lên miễn phí."), ("người lớn", "6..69 trả 7000.")]),
    solution="#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long t;\n    in >> t;\n    out << ((t < 6 || t >= 70) ? 0 : 7000) << \"\\n\";\n}",
    wrong="#include <iostream>\nvoid solve(std::istream& in, std::ostream& out) {\n    long long t;\n    in >> t;\n    // near-miss: t > 6 loses the exact-age-6 case, t > 70 loses age 70\n    out << ((t < 6 || t > 70) ? 0 : 7000) << \"\\n\";\n}",
)

# ---------------------------------------------------------------- manifests
write_course(
    "hsg-beginner",
    "Competitive Programming — High School Beginner",
    "The Vietnamese Học sinh giỏi preparation path: reading statements, complexity, marking arrays, sorting and binary search, prefix and difference arrays, strings, number theory, STL, recursion and backtracking, basic DP, graphs, and four mock contests. Every problem is graded for real in the C++20 sandbox.",
    "High-school students (grades 10–12) preparing for Tin học chọn Học sinh giỏi from school rounds to provincial level; basic C++ knowledge (or taking cpp-beginner in parallel).",
    [
        "Read a contest statement and extract exact constraints, I/O format, and subtasks",
        "Estimate complexity and pick an algorithm that fits the time limit",
        "Implement marking/frequency arrays, sorting, binary search, prefix and difference arrays fluently",
        "Solve string, number-theory (sieve), STL, recursion, and backtracking problems",
        "Solve basic DP and BFS/DFS graph problems at provincial-HSG level",
        "Sit four mock contests with subtasks and manage a 180-minute exam",
    ],
    [],
    ["hsg-vao-mon", "hsg-loops", "hsg-arrays", "hsg-marking", "hsg-greedy", "hsg-sorting",
     "hsg-search", "hsg-prefix", "hsg-diff", "hsg-strings", "hsg-number", "hsg-stl",
     "hsg-recursion", "hsg-backtrack", "hsg-dp", "hsg-graph", "hsg-two-pointers",
     "hsg-technique", "hsg-debug", "hsg-contests"],
    "Tuyển Học Sinh Giỏi Tin học — Cơ bản",
    "Lộ trình lập trình thi đấu cho học sinh THPT: đọc đề, độ phức tạp, mảng đánh dấu, sắp xếp/tìm kiếm, mảng cộng dồn & hiệu, xâu, số học, STL, đệ quy–quay lui, QHĐ cơ bản, đồ thị, và 4 kỳ thi thử. Mọi bài được chấm thật trong sandbox C++20.",
)

write_track()
print("module 1 authored")
