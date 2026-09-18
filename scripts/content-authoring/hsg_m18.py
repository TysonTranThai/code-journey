#!/usr/bin/env python3
"""HSG — Module 18: hsg-technique (kỹ thuật thi).

Contest craft: constraint reading, complexity budgeting from time limits,
subtask/partial-scoring strategy, brute-force-first pipeline. Conventions:
T() for test I/O, cpp() for bodies.
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

M = "hsg-technique"
write_module(
    M,
    "Contest Technique",
    "Read constraints like a lawyer, budget operations like an engineer, and bank partial credit like an investor.",
    "Kỹ thuật thi",
    "Đọc giới hạn như luật gia, lập ngân sách phép tính như kỹ sư, và lấy điểm phần như nhà đầu tư.",
    ["hsg-m18-budget", "hsg-m18-subtask", "hsg-cp-m18"],
    ["hsg-p18-tech"],
)

write_lesson(
    M,
    "hsg-m18-budget",
    "The Complexity Budget",
    "Constraints tell you the intended complexity before you think about the algorithm.",
    15,
    """## The 10^8 rule of thumb

A typical judge executes roughly 10^8 simple operations per second
(our sandbox is slower — write for ~5 * 10^7 at 1 s). The constraint
ceiling N tells you what complexity the setters expect:

| N up to    | Intended complexity      |
| ---------- | ------------------------ |
| 10–20      | O(2^n) or O(n * 2^n)     |
| ~500       | O(n^3)                   |
| ~5,000     | O(n^2)                   |
| ~100,000   | O(n log n) / O(n sqrt n) |
| ~10^6–10^7 | O(n)                     |

This is a heuristic, not a law — but if N = 100,000 and your idea is
O(n^2), either your idea is wrong or there is a smarter angle.

## Read the constraints FIRST

Before the story, before the examples: What is the max N? What is the
max value (overflow!)? How many test cases (multiply the budget!)? A
sum over test cases (`T * N <= 10^5`) is a different beast from T
independent maxima (T * 10^5 each).

## The overflow audit

`long long` before multiplying two ints. 10^9 + 10^9 fits; (10^9)^2
does not. Every product, every sum of many terms, every a*b in a
comparator — audit them at the end of writing, not after WA.

## Output format is a constraint too

Trailing spaces, missing final newline, YES/yes/Yes — byte-exact
judges reject all of them. When the statement shows an example, your
output must match it byte for byte.
""",
    "Ngân sách độ phức tạp",
    "Giới hạn cho biết độ phức tạp dự kiến trước khi bạn nghĩ về thuật toán.",
    """## Quy tắc ngón tay 10^8

Máy chấm điển hình chạy khoảng 10^8 phép tính đơn mỗi giây (sandbox
của chúng ta chậm hơn — hãy viết cho ~5 * 10^7 trên 1 giây). Trần N
trong giới hạn cho biết độ phức tạp người ra đề kỳ vọng:

| N tới      | Độ phức tạp dự kiến      |
| ---------- | ------------------------ |
| 10–20      | O(2^n) hoặc O(n * 2^n)   |
| ~500       | O(n^3)                   |
| ~5,000     | O(n^2)                   |
| ~100,000   | O(n log n) / O(n sqrt n) |
| ~10^6–10^7 | O(n)                     |

Đây là kinh nghiệm, không phải định luật — nhưng nếu N = 100,000 mà
ý tưởng của bạn là O(n^2), hoặc ý tưởng sai, hoặc có một góc nhìn
thông minh hơn.

## Đọc giới hạn TRƯỚC

Trước cả câu chuyện, trước ví dụ: N tối đa là bao nhiêu? Giá trị tối
đa (tràn số!)? Bao nhiêu test (nhân ngân sách!)? Tổng qua các test
(`T * N <= 10^5`) là một con thú khác với T bài độc lập (mỗi bài 10^5).

## Kiểm toán tràn số

`long long` trước khi nhân hai int. 10^9 + 10^9 vừa; (10^9)^2 thì
không. Mỗi phép nhân, mỗi tổng nhiều số hạng, mỗi a*b trong bộ so
sánh — kiểm toán ngay khi viết xong, không phải sau khi WA.

## Định dạng đầu ra cũng là giới hạn

Dấu cách thừa cuối dòng, thiếu ký tự xuống dòng cuối, YES/yes/Yes —
máy chấm chính xác theo byte từ chối tất cả. Khi đề có ví dụ, đầu ra
phải khớp từng byte.
""",
)

write_lesson(
    M,
    "hsg-m18-subtask",
    "Subtasks and Partial Credit",
    "Brute force first, bank the easy subtasks, then buy the next one with one more idea.",
    16,
    """## How subtasks work

A problem worth 100 points may be split: Subtask 1 (30%) has small N
where brute force passes; Subtask 2 (30%) needs a medium idea;
Subtask 3 (40%) needs the full algorithm. Your score is the sum of
subtasks your solution handles — a correct-but-slow program still
banks the small ones.

## The pipeline

1. Write the dumbest correct solution (brute force). It already earns
   subtask 1.
2. Only then look for the optimization. If you find nothing in 20
   minutes, submit the brute force and move on — points in hand beat
   points in theory.
3. If the optimization only handles subtask 2 (say `N <= 5,000`), that
   is still more points. Do not hold out for the full solution.

## Example shape

`N <= 20`: enumerate everything. `N <= 5,000`: O(n^2). `N <= 100,000`:
sort + sweep / two pointers / prefix sums. Each tier is a DIFFERENT
program or a branch inside one program:

```cpp
if (n <= 20) brute();        // subtask 1
else if (n <= 5000) square(); // subtask 2
else fast();                  // subtask 3
```

Mixing tiers in one submission is normal contest practice — just keep
each branch correct.

## Anti-patterns

- Rewriting the whole solution from scratch for the last subtask and
  breaking subtask 1 in the process (always re-test the small cases).
- Spending 90 minutes on one problem while two easy ones sit unsolved.
- Guessing that "the sample passes, ship it" — samples never cover
  the boundaries; construct your own: N = 1, N = max, all equal,
  extreme values.
""",
    "Subtask và điểm phần",
    "Vét cạn trước, lấy các subtask dễ, rồi mua subtask kế bằng thêm một ý tưởng.",
    """## Subtask hoạt động thế nào

Một bài 100 điểm có thể tách: Subtask 1 (30%) có N nhỏ để vét cạn đi
qua; Subtask 2 (30%) cần ý tưởng vừa; Subtask 3 (40%) cần thuật toán
đầy đủ. Điểm của bạn là tổng các subtask mà lời giải xử lý — chương
trình đúng-nhưng-chậm vẫn lấy được các phần nhỏ.

## Quy trình

1. Viết lời giải NGUỒI NGUỘI nhất còn đúng (vét cạn). Nó đã kiếm được
   subtask 1.
2. Sau đó mới tìm cách tối ưu. Nếu 20 phút không ra, nộp vét cạn và
   chuyển bài — điểm trên tay hơn điểm trên lý thuyết.
3. Nếu cách tối ưu chỉ xử lý được subtask 2 (chẳng hạn `N <= 5,000`),
   đó vẫn là thêm điểm. Đừng đòi lời giải trọn vẹn.

## Hình dạng ví dụ

`N <= 20`: liệt kê mọi thứ. `N <= 5,000`: O(n^2). `N <= 100,000`: sort +
quét / hai con trỏ / mảng cộng dồn. Mỗi tầng là một chương trình
KHÁC hoặc một nhánh trong cùng chương trình:

```cpp
if (n <= 20) brute();        // subtask 1
else if (n <= 5000) square(); // subtask 2
else fast();                  // subtask 3
```

Ghép nhiều tầng trong một bài nộp là chuyện bình thường — chỉ cần
mỗi nhánh đều đúng.

## Chống-mẫu

- Viết lại toàn bộ lời giải cho subtask cuối và làm hỏng subtask 1
  (luôn test lại các trường hợp nhỏ).
- Đốt 90 phút cho một bài trong khi hai bài dễ còn nằm đó.
- Tự nhủ "sample chạy là nộp" — sample không bao giờ phủ biên; tự
  dựng: N = 1, N = max, toàn bằng nhau, giá trị cực đoan.
""",
)

A1 = challenge(
    "hsg-p18-budget",
    "Complexity Picker",
    T(
        "**Description:** Given the constraint ceiling N and the time limit in seconds,",
        "print the intended complexity class. Use the standard budget: ~5*10^7 simple",
        "operations per second in this judge.",
        "",
        "**Input:** One line: N TL (1 <= N <= 10^9, 1 <= TL <= 10).",
        "**Output:** One of: `exponential` (N <= 25), `cubic` (N^3 fits), `quadratic`",
        "(N^2 fits), `linearithmic` (N log N fits), `linear` (otherwise). Print the FIRST",
        "class in that order whose cost fits the budget N-tier * cost <= 5*10^7 * TL.",
        "",
        "**Example:** `100 1` -> `cubic` (10^6 <= 5*10^7).",
    ),
    [
        contest_test("cubic fits", T("100 1"), T("cubic"), "N^3 = 10^6 fits."),
        contest_test("quadratic", T("5000 1"), T("quadratic"), "2.5*10^7 fits; 1.25*10^11 does not."),
        contest_test("linearithmic", T("100000 1"), T("linearithmic"), "N log N ~ 1.7*10^6."),
        contest_test("exponential", T("20 1"), T("exponential"), "N <= 25 is the exponent zone."),
        contest_test("more time", T("5000 10"), T("quadratic"),
                     "10x budget: N^3 = 1.25*10^11 still exceeds 5*10^8 — quadratic remains."),
        contest_test("budget boundary", T("8000 1"), T("linearithmic"),
                     "N^2 = 6.4*10^7 just over 5*10^7 — double-counted budgets print quadratic."),
        contest_test("time scaling", T("12000 2"), T("linearithmic"),
                     "N^2 = 1.44*10^8 exceeds the 10^8 budget; solutions that multiply TL twice print quadratic."),
    ],
    level="guided",
    difficulty="intermediate",
)

A2 = challenge(
    "hsg-p18-tiers",
    "Tiered Max",
    T(
        "**Description:** Read an array of n values and print the maximum. The catch: your",
        "program must be correct for every n — including n = 1 — and must not allocate",
        "more than a fixed 1000-cell array of work memory. Values may repeat.",
        "",
        "**Input:** Line 1: n (1 <= n <= 100000). Line 2: n integers (|a[i]| <= 10^9).",
        "**Output:** One integer — the maximum value.",
        "",
        "**Example:** `3` / `-5 2 -9` -> `2`.",
    ),
    [
        contest_test("sample", T("3", "-5 2 -9"), T("2"), "Straightforward."),
        contest_test("single", T("1", "42"), T("42"), "n = 1 must not read a second element."),
        contest_test("all negative", T("4", "-1 -2 -3 -4"), T("-1"),
                     "A 0-initialized max prints 0 here — the classic bug."),
        contest_test("all equal", T("5", "7 7 7 7 7"), T("7"), "Repeats change nothing."),
        contest_test("max at end", T("6", "1 2 3 4 5 99"), T("99"), "Scan the whole array."),
    ],
    level="guided",
    difficulty="intermediate",
)

A3 = challenge(
    "hsg-p18-bruteforce",
    "Small-N Triple",
    T(
        "**Description:** Count triples (i, j, k), i < j < k, whose sum is exactly S.",
        "Constraints are small enough for O(n^3) — but O(n^2) with a hash set also works.",
        "",
        "**Input:** Line 1: n S (1 <= n <= 300, |S| <= 10^15). Line 2: n integers",
        "(|a[i]| <= 10^9).",
        "**Output:** One integer — the number of triples.",
        "",
        "**Example:** `5 10` / `1 2 3 4 5` -> `2` (1+4+5, 2+3+5).",
    ),
    [
        contest_test("sample", T("5 10", "1 2 3 4 5"), T("2"), "Two triples."),
        contest_test("n 1", T("1 5", "5"), T("0"), "No triple exists."),
        contest_test("duplicates", T("4 3", "1 1 1 1"), T("4"),
                     "C(4,3) = 4 index-triples."),
        contest_test("negatives", T("3 0", "-1 0 1"), T("1"), "One exact triple."),
        contest_test("none", T("3 100", "1 2 3"), T("0"), "Sum too small."),
    ],
    level="independent",
    difficulty="intermediate",
)

A4 = challenge(
    "hsg-p18-partial",
    "Sum of Digits In Range",
    T(
        "**Description:** Print the sum of decimal digit sums of every integer from 1 to N.",
        "",
        "**Input:** One line: N (1 <= N <= 10^6).",
        "**Output:** One integer — the total (fits in 64 bits).",
        "",
        "**Example:** `12` -> `45` (digits 1..9 sum 45; 10,11,12 add 1+2+3=6... total 51?",
        "No: 1..9 gives 45, plus 1+0+1+1+1+2 = 6, so 45+6 = 51).",
    ),
    [
        contest_test("sample small", T("12"), T("51"),
                     "45 from 1..9 plus 1+0 + 1+1 + 1+2 = 6."),
        contest_test("n 1", T("1"), T("1"), "Single digit."),
        contest_test("n 9", T("9"), T("45"), "Digits 1..9."),
        contest_test("n 10", T("10"), T("46"), "45 + 1."),
        contest_test("max n", T("1000000"), T("27000001"),
                     "Digit-sum of 1..999999 is 27*10^5 per digit-position average -> 27,000,000; plus 1 for 10^6."),
    ],
    level="independent",
    difficulty="intermediate",
)

A5 = challenge(
    "hsg-p18-format",
    "Byte-Exact Echo",
    T(
        "**Description:** Read t test cases; each is two integers a b. For each, print",
        "`a+b` — but format matters: one number per line, no trailing spaces, and a final",
        "newline after the last line.",
        "",
        "**Input:** Line 1: t (1 <= t <= 100000). Next t lines: a b (|a|, |b| <= 10^9).",
        "**Output:** t lines, each the sum.",
        "",
        "**Example:** `3` / `1 2` / `10 -3` / `0 0` -> `3` / `7` / `0`.",
    ),
    [
        contest_test("sample", T("3", "1 2", "10 -3", "0 0"), T("3", "7", "0"), "Three sums."),
        contest_test("single", T("1", "5 5"), T("10"), "One line."),
        contest_test("negatives", T("2", "-1 -1", "-5 9"), T("-2", "4"), "Sign handling."),
        contest_test("zeros", T("2", "0 0", "0 5"), T("0", "5"), "Zero sums still print."),
        contest_test("max t", T("5", "1000000000 1000000000", "-1000000000 -1000000000",
                               "999999999 1", "-999999999 1", "0 1"),
                     T("2000000000", "-2000000000", "1000000000", "-999999998", "1"),
                     "Overflow discipline: sums reach 2*10^9 — int is not enough."),
    ],
    level="independent",
    difficulty="intermediate",
)

VI1 = {
    "hsg-p18-budget": vi_challenge(
        "Chọn độ phức tạp",
        T(
            "**Đề bài:** Cho trần giới hạn N và thời gian (giây), in lớp độ phức tạp dự",
            "kiến. Ngân sách chuẩn: ~5*10^7 phép tính đơn mỗi giây trên máy chấm này.",
            "",
            "**Dữ liệu vào:** Một dòng: N TL (1 <= N <= 10^9, 1 <= TL <= 10).",
            "**Dữ liệu ra:** Một trong: `exponential` (N <= 25), `cubic` (N^3 vừa),",
            "`quadratic` (N^2 vừa), `linearithmic` (N log N vừa), `linear` (ngược lại). In",
            "lớp ĐẦU TIÊN theo thứ tự đó mà N-tier * chi phí <= 5*10^7 * TL.",
            "",
            "**Ví dụ:** `100 1` -> `cubic` (10^6 <= 5*10^7).",
        ),
        [
            ("cubic fits", "N^3 = 10^6 vừa."),
            ("quadratic", "2.5*10^7 vừa; 1.25*10^11 thì không."),
            ("linearithmic", "N log N ~ 1.7*10^6."),
            ("exponential", "N <= 25 là vùng luỹ thừa."),
            ("more time", "Ngân sách x10: N^3 = 1.25*10^11 vẫn vượt 5*10^8 — giữ quadratic."),
            ("budget boundary", "N^2 = 6.4*10^7 vừa vượt 5*10^7 — ngân sách bị nhân đôi sẽ in quadratic."),
            ("time scaling", "N^2 = 1.44*10^8 vượt ngân sách 10^8; nhân TL hai lần sẽ in quadratic."),
        ],
    ),
    "hsg-p18-tiers": vi_challenge(
        "Max nhiều tầng",
        T(
            "**Đề bài:** Đọc mảng n giá trị và in giá trị lớn nhất. Cái bẫy: chương trình phải",
            "đúng với mọi n — kể cả n = 1 — và không được cấp phát quá một mảng làm việc",
            "1000 ô. Giá trị có thể lặp.",
            "",
            "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100000). Dòng 2: n số nguyên (|a[i]| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — giá trị lớn nhất.",
            "",
            "**Ví dụ:** `3` / `-5 2 -9` -> `2`.",
        ),
        [
            ("sample", "Trực quan."),
            ("single", "n = 1 không được đọc thêm phần tử thứ hai."),
            ("all negative", "Max khởi tạo bằng 0 sẽ in 0 ở đây — bug kinh điển."),
            ("all equal", "Lặp lại không đổi kết quả."),
            ("max at end", "Duyệt hết mảng."),
        ],
    ),
    "hsg-p18-bruteforce": vi_challenge(
        "Bộ ba N nhỏ",
        T(
            "**Đề bài:** Đếm bộ ba (i, j, k), i < j < k, có tổng đúng bằng S. Giới hạn nhỏ",
            "đủ cho O(n^3) — nhưng O(n^2) với hash set cũng được.",
            "",
            "**Dữ liệu vào:** Dòng 1: n S (1 <= n <= 300, |S| <= 10^15). Dòng 2: n số nguyên",
            "(|a[i]| <= 10^9).",
            "**Dữ liệu ra:** Một số nguyên — số bộ ba.",
            "",
            "**Ví dụ:** `5 10` / `1 2 3 4 5` -> `2` (1+4+5, 2+3+5).",
        ),
        [
            ("sample", "Hai bộ ba."),
            ("n 1", "Không tồn tại bộ ba."),
            ("duplicates", "C(4,3) = 4 bộ ba chỉ số."),
            ("negatives", "Một bộ ba chuẩn."),
            ("none", "Tổng quá nhỏ."),
        ],
    ),
    "hsg-p18-partial": vi_challenge(
        "Tổng chữ số trong khoảng",
        T(
            "**Đề bài:** In tổng các chữ số (hệ thập phân) của mọi số nguyên từ 1 tới N.",
            "",
            "**Dữ liệu vào:** Một dòng: N (1 <= N <= 10^6).",
            "**Dữ liệu ra:** Một số nguyên — tổng (vừa 64 bit).",
            "",
            "**Ví dụ:** `12` -> `51`.",
        ),
        [
            ("sample small", "45 từ 1..9 cộng 1+0 + 1+1 + 1+2 = 6."),
            ("n 1", "Một chữ số."),
            ("n 9", "Chữ số 1..9."),
            ("n 10", "45 + 1."),
            ("max n", "Tổng chữ số của 1..999999 là 27.000.000; cộng 1 cho 10^6."),
        ],
    ),
    "hsg-p18-format": vi_challenge(
        "Echo chính xác từng byte",
        T(
            "**Đề bài:** Đọc t test; mỗi test gồm hai số nguyên a b. Với mỗi test, in `a+b` —",
            "nhưng định dạng quyết định: mỗi số một dòng, không dấu cách thừa, và có ký tự",
            "xuống dòng sau dòng cuối.",
            "",
            "**Dữ liệu vào:** Dòng 1: t (1 <= t <= 100000). t dòng tiếp: a b (|a|, |b| <= 10^9).",
            "**Dữ liệu ra:** t dòng, mỗi dòng một tổng.",
            "",
            "**Ví dụ:** `3` / `1 2` / `10 -3` / `0 0` -> `3` / `7` / `0`.",
        ),
        [
            ("sample", "Ba tổng."),
            ("single", "Một dòng."),
            ("negatives", "Xử lý dấu."),
            ("zeros", "Tổng 0 vẫn in."),
            ("max t", "Kỷ luật tràn số: tổng tới 2*10^9 — int không đủ."),
        ],
    ),
}

write_practice(
    M,
    "hsg-p18-tech",
    "Contest Technique Problem Set",
    "Complexity picking, tiered correctness, brute-force counting, digit sums, byte-exact output.",
    "Bài tập kỹ thuật thi",
    "Chọn độ phức tạp, đúng nhiều tầng, đếm vét cạn, tổng chữ số, đầu ra chính xác từng byte.",
    "hsg-m18-subtask",
    45,
    "intermediate",
    [A1, A2, A3, A4, A5],
    VI1,
    solutions=[
        (
            "hsg-p18-budget",
            CPP_STD + cpp("""    long long N, TL; in >> N >> TL;
    long long budget = 50000000LL * TL;
    if (N <= 25) { out << "exponential" << "{{NL}}"; return; }
    if (N <= 1000 && N * N * N <= budget) { out << "cubic" << "{{NL}}"; return; }
    if (N * N <= budget) { out << "quadratic" << "{{NL}}"; return; }
    long long logn = 0; long long t = N;
    while (t > 1) { t /= 2; ++logn; }
    if (N * logn <= budget) { out << "linearithmic" << "{{NL}}"; return; }
    out << "linear" << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long N, TL; in >> N >> TL;
    long long budget = 50000000LL * TL;
    if (N <= 25) { out << "exponential" << "{{NL}}"; return; }
    if (N <= 1000 && N * N * N <= budget) { out << "cubic" << "{{NL}}"; return; }
    // near-miss: quadratic test uses N^2 * TL instead of N^2 <= budget —
    // double-counts the time limit
    if (N * N <= budget * TL) { out << "quadratic" << "{{NL}}"; return; }
    long long logn = 0; long long t = N;
    while (t > 1) { t /= 2; ++logn; }
    if (N * logn <= budget) { out << "linearithmic" << "{{NL}}"; return; }
    out << "linear" << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p18-tiers",
            CPP_STD + cpp("""    int n; in >> n;
    long long best;
    in >> best;
    for (int i = 1; i < n; ++i) {
        long long x; in >> x;
        best = max(best, x);
    }
    out << best << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; in >> n;
    // near-miss: max starts at 0 — every-negative arrays print 0
    long long best = 0;
    for (int i = 0; i < n; ++i) {
        long long x; in >> x;
        best = max(best, x);
    }
    out << best << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p18-bruteforce",
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long cnt = 0;
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            for (int k = j + 1; k < n; ++k)
                if (a[i] + a[j] + a[k] == S) ++cnt;
    out << cnt << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    int n; long long S; in >> n >> S;
    vector<long long> a(n);
    for (auto& x : a) in >> x;
    long long cnt = 0;
    // near-miss: counts ordered triples (i,j,k) and (k,j,i) alike —
    // does not enforce i < j < k
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            for (int k = 0; k < n; ++k)
                if (i != j && j != k && i != k && a[i] + a[j] + a[k] == S) ++cnt;
    out << cnt << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p18-partial",
            CPP_STD + cpp("""    long long N; in >> N;
    long long total = 0;
    vector<long long> ds(N + 1, 0);
    for (long long i = 1; i <= N; ++i)
        ds[i] = ds[i / 10] + i % 10;      // digit sum via subproblem
    for (long long i = 1; i <= N; ++i) total += ds[i];
    out << total << "{{NL}}";
""") + END,
            CPP_STD + cpp("""    long long N; in >> N;
    long long total = 0;
    // near-miss: recomputes digit sums by repeated division but drops
    // the last digit (loops while n >= 10 instead of > 0)
    for (long long i = 1; i <= N; ++i) {
        long long x = i, d = 0;
        while (x >= 10) { d += x % 10; x /= 10; }
        total += d;
    }
    out << total << "{{NL}}";
""") + END,
        ),
        (
            "hsg-p18-format",
            CPP_STD + cpp("""    int t; in >> t;
    string res;
    for (int i = 0; i < t; ++i) {
        long long a, b; in >> a >> b;
        res += to_string(a + b);
        res += "{{NL}}";
    }
    out << res;
""") + END,
            CPP_STD + cpp("""    int t; in >> t;
    string res;
    for (int i = 0; i < t; ++i) {
        long long a, b; in >> a >> b;
        res += to_string(a + b);
        // near-miss: space-separated instead of newline-separated
        res += " ";
    }
    out << res << "{{NL}}";
""") + END,
        ),
    ],
)

CH18 = challenge(
    "hsg-cp-m18-scoreline",
    "The Score Line",
    T(
        "**Description:** A problem has n test cases worth w[i] points each. You solved",
        "every case with index <= k (cases are ordered easiest first). Print your total",
        "score. Then print `PASS` if it reaches at least half of the total, else `FAIL`.",
        "",
        "**Input:** Line 1: n (1 <= n <= 100000). Line 2: n integers w[i] (1 <= w[i] <= 100).",
        "Line 3: k (0 <= k <= n).",
        "**Output:** Line 1: the total score. Line 2: `PASS` or `FAIL`.",
        "",
        "**Example:** `4` / `10 20 30 40` / `2` -> `30` / `FAIL` (total 100, need >= 50).",
    ),
    [
        contest_test("sample", T("4", "10 20 30 40", "2"), T("30", "FAIL"),
                     "10+20 = 30 < 50."),
        contest_test("k 0", T("3", "5 5 5", "0"), T("0", "FAIL"), "Nothing solved."),
        contest_test("all", T("3", "5 5 5", "3"), T("15", "PASS"), "Everything."),
        contest_test("exactly half", T("4", "10 10 10 10", "2"), T("20", "PASS"),
                     "20 >= 40/2 — at-least-half includes equality."),
        contest_test("single", T("1", "7", "1"), T("7", "PASS"), "7 >= 3.5."),
    ],
    level="combination",
    difficulty="intermediate",
)

VI_CP18 = vi_challenge(
    "Phách chấm điểm",
    T(
        "**Đề bài:** Một bài có n test, test i worth w[i] điểm. Bạn giải được mọi test có",
        "chỉ số <= k (test xếp từ dễ tới khó). In tổng điểm. Sau đó in `PASS` nếu đạt ít",
        "nhất một nửa tổng, ngược lại `FAIL`.",
        "",
        "**Dữ liệu vào:** Dòng 1: n (1 <= n <= 100000). Dòng 2: n số nguyên w[i] (1 <= w[i] <= 100).",
        "Dòng 3: k (0 <= k <= n).",
        "**Dữ liệu ra:** Dòng 1: tổng điểm. Dòng 2: `PASS` hoặc `FAIL`.",
        "",
        "**Ví dụ:** `4` / `10 20 30 40` / `2` -> `30` / `FAIL` (tổng 100, cần >= 50).",
    ),
    [
        ("sample", "10+20 = 30 < 50."),
        ("k 0", "Không giải được gì."),
        ("all", "Toàn bộ."),
        ("exactly half", "20 >= 40/2 — ít-nhất-một-nửa tính cả bằng."),
        ("single", "7 >= 3.5."),
    ],
)

write_checkpoint(
    M,
    "hsg-cp-m18",
    "Checkpoint — Contest Technique",
    "Pass the graded problem to finish the technique module.",
    15,
    """**Checkpoint — kỹ thuật thi.** Pass the graded challenge below. It is
deliberately easy — the discipline being tested is byte-exact two-line
output and the >= half boundary (equality passes). The graded
near-misses: a space after the score line (formatting), and strict >
instead of >= when comparing to half the total.

**Điểm kiểm tra — kỹ thuật thi.** Pass bài chấm bên dưới — cố tình dễ;
thứ bị kiểm là kỷ luật đầu ra hai dòng chính xác từng byte và biên
>= một nửa (bằng nhau vẫn đỗ). Các near-miss bị chấm: dấu cách sau
dòng điểm (định dạng), và dùng > nghiêm ngặt thay vì >= khi so với
một nửa tổng.
""",
    "Checkpoint — Contest Technique",
    "Pass the graded problem to finish the technique module.",
    """**Điểm kiểm tra — kỹ thuật thi.** Pass bài chấm bên dưới — cố tình dễ;
thứ bị kiểm là kỷ luật đầu ra hai dòng chính xác từng byte và biên
>= một nửa (bằng nhau vẫn đỗ). Các near-miss bị chấm: dấu cách sau
dòng điểm (định dạng), và dùng > nghiêm ngặt thay vì >= khi so với
một nửa tổng.
""",
    CH18,
    VI_CP18,
    solution=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> w(n);
    long long total = 0;
    for (auto& x : w) { in >> x; total += x; }
    int k; in >> k;
    long long score = 0;
    for (int i = 0; i < k; ++i) score += w[i];
    out << score << "{{NL}}";
    out << ((2 * score >= total) ? "PASS" : "FAIL") << "{{NL}}";
""") + END,
    wrong=CPP_STD + cpp("""    int n; in >> n;
    vector<long long> w(n);
    long long total = 0;
    for (auto& x : w) { in >> x; total += x; }
    int k; in >> k;
    long long score = 0;
    for (int i = 0; i < k; ++i) score += w[i];
    // near-miss: strict > — a score of exactly half wrongly fails
    out << score << "{{NL}}";
    out << ((2 * score > total) ? "PASS" : "FAIL") << "{{NL}}";
""") + END,
)

print("M18 done")
