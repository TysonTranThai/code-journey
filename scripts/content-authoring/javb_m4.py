#!/usr/bin/env python3
"""Java — Beginner — Module 4: java-loops."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-loops"

L_FOR_EN = r'''
Loops repeat work without repeating code. Java has three loop forms; the
counting `for` comes first:

```java
for (int i = 1; i <= 5; i++) {
    System.out.println("tick " + i);
}
```

Read the header as three sentences: **start** with `i` at 1; **keep going**
while `i <= 5`; after every pass, **step** `i` forward. The variable `i`
exists only inside the loop — declare it there, not outside.

The counting pattern that covers most real loops:

```java
int[] scores = {72, 85, 90};
for (int i = 0; i < scores.length; i++) {
    System.out.println(scores[i]);
}
```

Zero-based counting with `i < length` (not `<=`) is the Java convention —
arrays and Strings index from 0, so `i` from 0 to length-1 touches every
element exactly once. Off-by-one bugs (`<=`) throw
`ArrayIndexOutOfBoundsException` at the last step.

The **enhanced for** ("for-each") visits every element without an index at
all:

```java
for (int s : scores) {
    System.out.println(s);
}
```

Use for-each whenever you need the *elements*; use the classic `for` when
you need the *position* or a custom step (`i += 3`). Both loops here print
the same three numbers — choosing the loop is choosing which idea
(index vs element) your code is about.

**Next:** loops that run until something happens.
'''

L_FOR_VI = r'''
Vòng lặp lặp lại công việc mà không lặp lại code. Java có ba dạng; `for`
đếm đến trước:

```java
for (int i = 1; i <= 5; i++) {
    System.out.println("tick " + i);
}
```

Đọc header như ba câu: **bắt đầu** với `i` bằng 1; **tiếp tục** trong khi
`i <= 5`; sau mỗi vòng, **bước** `i` lên. Biến `i` chỉ tồn tại trong vòng
lặp — hãy khai báo nó ở đó, đừng khai báo bên ngoài.

Pattern đếm phủ phần lớn vòng lặp thực tế:

```java
int[] scores = {72, 85, 90};
for (int i = 0; i < scores.length; i++) {
    System.out.println(scores[i]);
}
```

Đếm từ 0 với `i < length` (không phải `<=`) là quy ước của Java — mảng và
String đánh chỉ số từ 0, vậy `i` chạy từ 0 đến length-1 chạm đúng mỗi phần
tử một lần. Bug lệch một (`<=`) ném `ArrayIndexOutOfBoundsException` ở bước
cuối.

**Enhanced for** ("for-each") thăm mọi phần tử mà không cần chỉ số:

```java
for (int s : scores) {
    System.out.println(s);
}
```

Dùng for-each khi bạn cần *giá trị phần tử*; dùng `for` cổ điển khi bạn cần
*vị trí* hoặc bước nhảy riêng (`i += 3`). Cả hai vòng ở đây in ba số giống
hệt — chọn vòng lặp là chọn ý tưởng (chỉ số vs phần tử) mà code của bạn
muốn nói tới.

**Tiếp theo:** những vòng lặp chạy đến khi có gì đó xảy ra.
'''

L_WHILE_EN = r'''
Two loops run on a *condition* rather than a count.

**`while`** checks first, then runs — the body may execute zero times:

```java
int cups = 0;
while (cups < 3) {
    cups++;
}
// cups == 3 here
```

**`do-while`** runs the body first, then checks — the body always executes
at least once. The classic shape is a retry loop:

```java
int attempts = 0;
do {
    attempts++;
    // try something
} while (attempts < 3 && !succeeded);
```

Use `while` when the answer might already be "done" (draining a queue); use
`do-while` only when the first pass is required by the problem itself
(prompt-then-check input). In practice 90% of condition loops are `while`.

**`break` and `continue`** control the loop from inside:

```java
int found = -1;
for (int i = 0; i < data.length; i++) {
    if (data[i] < 0) {
        continue;            // skip this element, keep looping
    }
    if (data[i] == target) {
        found = i;
        break;               // stop the whole loop
    }
}
```

`break` exits the loop immediately; `continue` jumps to the next iteration.
Both are clearest when rare — a loop full of breaks is really a tangled
state machine. Note the standard search idiom: carry the answer in a
variable declared *outside* the loop, so it survives the `break`.

**The infinite loop** `while (true) { ... break; }` is legitimate when the
exit is in the middle of the body — but the `break` must be reachable, and
you must be able to say in one sentence what eventually makes it run.

**Next:** loops inside loops, and the accumulator patterns that make loops earn their keep.
'''

L_WHILE_VI = r'''
Hai vòng lặp chạy theo *điều kiện* thay vì theo con số đếm.

**`while`** kiểm tra trước, chạy sau — phần thân có thể không chạy lần nào:

```java
int cups = 0;
while (cups < 3) {
    cups++;
}
// tại đây cups == 3
```

**`do-while`** chạy thân trước, kiểm tra sau — thân luôn chạy ít nhất một
lần. Hình dạng kinh điển là vòng thử lại:

```java
int attempts = 0;
do {
    attempts++;
    // thử một việc gì đó
} while (attempts < 3 && !succeeded);
```

Dùng `while` khi câu trả lời có thể đã là "xong" (rút cạn hàng đợi); chỉ
dùng `do-while` khi lượt đầu tiên do chính bài toán yêu cầu (hỏi-roi-kiểm
tra input). Thực tế 90% vòng theo điều kiện là `while`.

**`break` và `continue`** điều khiển vòng lặp từ bên trong:

```java
int found = -1;
for (int i = 0; i < data.length; i++) {
    if (data[i] < 0) {
        continue;            // bỏ qua phần tử này, lặp tiếp
    }
    if (data[i] == target) {
        found = i;
        break;               // dừng cả vòng lặp
    }
}
```

`break` thoát khỏi vòng lặp ngay lập tức; `continue` nhảy sang lần lặp kế.
Cả hai rõ ràng nhất khi hiếm — một vòng lặp đầy break thực chất là máy
trạng thái rối. Chú ý thành ngữ tìm kiếm chuẩn: mang kết quả trong một biến
khai báo *ngoài* vòng lặp, để nó sống sót qua `break`.

**Vòng lặp vô hạn** `while (true) { ... break; }` là hợp lệ khi điểm thoát
nằm giữa thân — nhưng `break` phải với tới được, và bạn phải nói được trong
một câu điều gì khiến nó cuối cùng dừng lại.

**Tiếp theo:** vòng lặp trong vòng lặp, và các pattern tích lũy khiến vòng lặp đáng công.
'''

L_ACCUM_EN = r'''
Most useful loops carry state: a running total, a count, a best-so-far.
Three patterns cover the majority.

**Accumulator** — total or concatenate:

```java
double total = 0;
for (double p : prices) {
    total += p;
}
```

**Counter** — count events, not elements:

```java
int passing = 0;
for (int s : scores) {
    if (s >= 60) passing++;
}
```

**Best-so-far (extremum)** — track the max or min with its seed value:

```java
int max = Integer.MIN_VALUE;   // seed: smaller than any possible value
for (int s : scores) {
    if (s > max) max = s;
}
```

Seeding matters: `max = 0` is wrong when all scores are negative. The
opposite seed (`Integer.MAX_VALUE`) finds the minimum.

**Searching vs counting:** a search *stops early* (break when found); a
count or total must see everything. Choosing not to `break` a search is
leaving performance on the table; `break`ing an accumulation is almost
always a bug.

**Common mistakes, all seen in real code review this month:**
- updating the loop variable inside the body (`i++` twice per pass);
- accumulating into a variable declared *inside* the loop (reset every pass);
- `<` vs `<=` off-by-one at the boundary;
- floating-point accumulation for money (`0.1 + 0.2 != 0.3`) — use `long`
  cents or `BigDecimal` for currency (a habit worth forming now).

**Next:** nested loops and the shapes they draw.
'''

L_ACCUM_VI = r'''
Phần lớn vòng lặp hữu ích mang theo trạng thái: tổng chạy dần, một bộ đếm,
một giá trị tốt nhất từ trước tới nay. Ba pattern phủ đa số.

**Tích lũy** — tổng hoặc nối chuỗi:

```java
double total = 0;
for (double p : prices) {
    total += p;
}
```

**Bộ đếm** — đếm sự kiện, không phải phần tử:

```java
int passing = 0;
for (int s : scores) {
    if (s >= 60) passing++;
}
```

**Tốt nhất từ trước tới nay (cực trị)** — theo dõi max hoặc min với giá trị
hạt giống:

```java
int max = Integer.MIN_VALUE;   // hạt giống: nhỏ hơn mọi giá trị có thể
for (int s : scores) {
    if (s > max) max = s;
}
```

Hạt giống quan trọng: `max = 0` là sai khi mọi điểm đều âm. Hạt giống ngược
lại (`Integer.MAX_VALUE`) tìm min.

**Tìm kiếm vs đếm:** tìm kiếm *dừng sớm* (break khi thấy); đếm hay tổng thì
phải xem hết mọi thứ. Không `break` một phép tìm kiếm là bỏ phí hiệu năng;
`break` một phép tích lũy hầu như luôn là bug.

**Lỗi thường gặp, đều gặp trong code review tháng này:**
- cập nhật biến vòng lặp trong thân (`i++` hai lần mỗi vòng);
- tích lũy vào biến khai báo *bên trong* vòng lặp (bị reset mỗi vòng);
- `<` vs `<=` lệch một ở biên;
- tích lũy số thực cho tiền (`0.1 + 0.2 != 0.3`) — dùng `long` xu hoặc
  `BigDecimal` cho tiền tệ (thói quen đáng hình thành ngay bây giờ).

**Tiếp theo:** vòng lặp lồng nhau và những hình khối chúng vẽ ra.
'''

L_NESTED_EN = r'''
A loop inside a loop multiplies work: for each pass of the outer loop, the
inner loop runs completely.

```java
for (int row = 1; row <= 3; row++) {
    for (int col = 1; col <= 3; col++) {
        System.out.print(row * col + "\t");
    }
    System.out.println();          // end of row
}
```

This prints the 3×3 multiplication table. The structure to notice: the
**inner** loop's work is part of the outer loop's body — and the newline
goes *after* the inner loop, once per row. Misplacing one statement by a
level turns a table into a diagonal.

Nested loops power grids, pairwise comparisons, and pattern printing:

```java
for (int i = 1; i <= 4; i++) {
    for (int j = 0; j < i; j++) {
        System.out.print("*");
    }
    System.out.println();
}
// *
// **
// ***
// ****
```

**Cost intuition.** Doubling the data in a simple loop roughly doubles the
work — linear. Doubling the data in a nested loop *squares* it: 1,000 ×
1,000 is a million operations; 10,000 × 10,000 is a hundred million, and
you feel it. When you meet a slow program later, nested loops over big data
are the first suspect. This intuition (formalized as Big-O later) is the
beginning of performance thinking.

**Next:** practice.
'''

L_NESTED_VI = r'''
Một vòng lặp nằm trong vòng lặp nhân khối lượng công việc: mỗi vòng của
vòng ngoài, vòng trong chạy trọn vẹn.

```java
for (int row = 1; row <= 3; row++) {
    for (int col = 1; col <= 3; col++) {
        System.out.print(row * col + "\t");
    }
    System.out.println();          // hết một hàng
}
```

Lệnh này in bảng cửu chương 3×3. Cấu trúc cần chú ý: công việc của vòng
**trong** là một phần thân của vòng **ngoài** — và dấu xuống dòng nằm *sau*
vòng trong, một lần mỗi hàng. Đặt lệch một câu lệnh đúng một tầng biến bảng
thành đường chéo.

Vòng lặp lồng nuôi lưới dữ liệu, so sánh từng cặp, và in hình:

```java
for (int i = 1; i <= 4; i++) {
    for (int j = 0; j < i; j++) {
        System.out.print("*");
    }
    System.out.println();
}
// *
// **
// ***
// ****
```

**Trực giác chi phí.** Nhân đôi dữ liệu trong vòng lặp đơn làm khối lượng
tăng gấp đôi — tuyến tính. Nhân đôi dữ liệu trong vòng lặp lồng *bình
phương* hoá khối lượng: 1.000 × 1.000 là một triệu phép toán; 10.000 ×
10.000 là một trăm triệu, và bạn sẽ cảm nhận được. Khi sau này gặp chương
trình chậm, các vòng lặp lồng trên dữ liệu lớn là nghi phạm đầu tiên. Trực
giác này (chính thức hóa thành Big-O sau này) là khởi đầu của tư duy hiệu năng.

**Tiếp theo:** thực hành.
'''

# ── practice set 4 ──────────────────────────────────────────────────────────
P4_TOTAL = challenge(
    "javb-m4-total",
    "Running total",
    "Implement `long total(int[] values)` returning the sum of all elements. "
    "An empty array sums to 0.",
    r'''public class Solution {
    public static long total(int[] values) {
        return 0;
    }
}
''',
    [
        (
            "ordinary sums",
            r"""
CjTestBase.checkEq(Solution.total(new int[]{1, 2, 3}), 6L, "1+2+3");
CjTestBase.checkEq(Solution.total(new int[]{10, -10}), 0L, "cancels out");
""",
            "Accumulate into a long from the start.",
        ),
        (
            "empty input",
            r"""
CjTestBase.checkEq(Solution.total(new int[]{}), 0L, "empty array");
""",
            "Zero iterations, zero total — the loop body never runs.",
        ),
        (
            "big values",
            r"""
CjTestBase.checkEq(Solution.total(new int[]{2_000_000_000, 2_000_000_000}), 4_000_000_000L, "exceeds int");
""",
            "The sum of two ints can exceed int range — the accumulator must be long.",
        ),
    ],
    level="imitation",
)

P4_TOTAL_VI = vi_challenge(
    "Tổng chạy dần",
    "Viết `long total(int[] values)` trả tổng các phần tử. Mảng rỗng có tổng 0.",
    [
        ("ordinary sums", "Tích lũy vào long ngay từ đầu."),
        ("empty input", "Không vòng nào chạy, tổng bằng 0."),
        ("big values", "Tổng hai int có thể vượt phạm vi int — bộ tích lũy phải là long."),
    ],
)

P4_MAX = challenge(
    "javb-m4-max-index",
    "Max value AND its position",
    "Implement `int[] maxWithIndex(int[] values)` returning `{max, index}` of "
    "the FIRST occurrence of the largest value. Return `new int[]{-1, -1}` "
    "for an empty array.",
    r'''public class Solution {
    public static int[] maxWithIndex(int[] values) {
        return new int[]{-1, -1};
    }
}
''',
    [
        (
            "single peak",
            r"""
CjTestBase.checkEq(Solution.maxWithIndex(new int[]{3, 9, 4}), new int[]{9, 1}, "peak at 1");
""",
            "Track both value and position in one pass.",
        ),
        (
            "ties keep the first",
            r"""
CjTestBase.checkEq(Solution.maxWithIndex(new int[]{5, 7, 7, 2}), new int[]{7, 1}, "first of the ties");
""",
            "Strictly greater (`>`) updates; equal does not — first occurrence wins.",
        ),
        (
            "empty array",
            r"""
CjTestBase.checkEq(Solution.maxWithIndex(new int[]{}), new int[]{-1, -1}, "empty");
""",
            "The seed handles it: nothing beats the sentinel pair.",
        ),
    ],
    level="independent",
)

P4_MAX_VI = vi_challenge(
    "Giá trị lớn nhất VÀ vị trí",
    "Viết `int[] maxWithIndex(int[] values)` trả `{max, index}` của lần xuất "
    "hiện ĐẦU TIÊN của giá trị lớn nhất. Trả `new int[]{-1, -1}` cho mảng rỗng.",
    [
        ("single peak", "Theo dõi cả giá trị và vị trí trong một lượt."),
        ("ties keep the first", "Chỉ cập nhật khi *lớn hơn* (`>`); bằng thì không — lần đầu thắng."),
        ("empty array", "Hạt giống tự xử lý: không gì vượt được cặp sentinel."),
    ],
)

P4_GUESS = challenge(
    "javb-m4-guessing",
    "Number guessing game logic",
    "Implement `int guesses(int secret, int maxAttempts)` that simulates a "
    "player who guesses 1, 2, 3, ... in order. Return the attempt number on "
    "which the secret is guessed, or `-1` if `maxAttempts` runs out first. "
    "`guesses(4, 10)` returns 4.",
    r'''public class Solution {
    public static int guesses(int secret, int maxAttempts) {
        return -1;
    }
}
''',
    [
        (
            "found in time",
            r"""
CjTestBase.checkEq(Solution.guesses(4, 10), 4, "guess 4 by attempt 4");
CjTestBase.checkEq(Solution.guesses(1, 10), 1, "first try");
""",
            "Sequential guessing: attempt n guesses the value n.",
        ),
        (
            "out of attempts",
            r"""
CjTestBase.checkEq(Solution.guesses(10, 3), -1, "never reached 10 in 3 tries");
""",
            "The loop ends when maxAttempts is exhausted — report failure.",
        ),
        (
            "boundary",
            r"""
CjTestBase.checkEq(Solution.guesses(3, 3), 3, "exactly on the last attempt");
""",
            "The last allowed attempt still counts.",
        ),
    ],
    level="combination",
)

P4_GUESS_VI = vi_challenge(
    "Logic trò chơi đoán số",
    "Viết `int guesses(int secret, int maxAttempts)` mô phỏng người chơi đoán "
    "1, 2, 3, ... lần lượt. Trả số lần thử mà secret được đoán trúng, hoặc "
    "`-1` nếu `maxAttempts` cạn trước. `guesses(4, 10)` trả 4.",
    [
        ("found in time", "Đoán tuần tự: lần thử thứ n đoán giá trị n."),
        ("out of attempts", "Vòng lặp kết thúc khi maxAttempts cạn — báo thất bại."),
        ("boundary", "Lần thử cuối cùng được phép vẫn được tính."),
    ],
)

P4_TRIANGLE = challenge(
    "javb-m4-star-triangle",
    "Star triangle (nested loops)",
    "Implement `static void program(int n)` that PRINTS a left-aligned triangle "
    "of `*` characters: row 1 has one star, row n has n stars, each row "
    "followed by a newline. `program(3)` prints `\"*\\n**\\n***\\n\"`.",
    r'''public class Solution {
    public static void program(int n) {
        // Print the triangle using nested loops.
    }
}
''',
    [
        (
            "shape of three",
            r"""
String out = CjTestBase.capture(() -> Solution.program(3));
CjTestBase.checkEq(out, "*\n**\n***\n", "triangle of 3");
""",
            "Inner loop runs row times; println after the inner loop ends each row.",
        ),
        (
            "single row and five",
            r"""
String one = CjTestBase.capture(() -> Solution.program(1));
CjTestBase.checkEq(one, "*\n", "triangle of 1");
String five = CjTestBase.capture(() -> Solution.program(5));
CjTestBase.checkEq(five, "*\n**\n***\n****\n*****\n", "triangle of 5");
""",
            "n = 1 still has one row; five rows of growing width.",
        ),
    ],
    level="guided",
)

P4_TRIANGLE_VI = vi_challenge(
    "Hình tam giác sao (vòng lặp lồng)",
    "Viết `static void program(int n)` IN một tam giác căn trái gồm ký tự "
    "`*`: hàng 1 có một sao, hàng n có n sao, mỗi hàng kết thúc bằng xuống "
    "dòng. `program(3)` in `\"*\\n**\\n***\\n\"`.",
    [
        ("shape of three", "Vòng trong chạy số lần bằng số hàng; println sau vòng trong kết thúc mỗi hàng."),
        ("single row and five", "n = 1 vẫn có một hàng; năm hàng rộng dần."),
    ],
)

P4_FIX = challenge(
    "javb-m4-fix-loop",
    "Debug: the loop that skips and lies",
    "Two bugs live in `firstEven(int[] values)`, which must return the index "
    "of the first even number or -1: it currently skips odd numbers at the "
    "wrong moment, and it uses `<=` at the boundary. Diagnose by reading, "
    "fix, verify with the tests.",
    r'''public class Solution {
    public static int firstEven(int[] values) {
        int found = -1;
        for (int i = 0; i <= values.length; i++) {
            if (values[i] % 2 != 0) {
                break;
            }
            if (values[i] % 2 == 0) {
                found = i;
                break;
            }
        }
        return found;
    }
}
''',
    [
        (
            "finds the first even",
            r"""
CjTestBase.checkEq(Solution.firstEven(new int[]{3, 7, 4, 8}), 2, "first even at 2");
""",
            "Odd numbers must be skipped with continue (or simply not break!).",
        ),
        (
            "no even numbers",
            r"""
CjTestBase.checkEq(Solution.firstEven(new int[]{1, 3, 5}), -1, "none even");
""",
            "Without a match the seed -1 survives.",
        ),
        (
            "empty array",
            r"""
CjTestBase.checkEq(Solution.firstEven(new int[]{}), -1, "empty");
""",
            "The `<=` bound makes the original crash here — after the fix, no crash.",
        ),
    ],
    level="debugging",
)

P4_FIX_VI = vi_challenge(
    "Gỡ lỗi: vòng lặp bỏ sót và nói dối",
    "Hai bug trú trong `firstEven(int[] values)`, hàm phải trả chỉ số của số "
    "chẵn đầu tiên hoặc -1: hiện nó break ở sai thời điểm với số lẻ, và dùng "
    "`<=` ở biên. Chẩn đoán bằng cách đọc, sửa, xác minh bằng test.",
    [
        ("finds the first even", "Số lẻ phải được bỏ qua bằng continue (hoặc đơn giản là không break!)."),
        ("no even numbers", "Không khớp thì hạt giống -1 sống sót."),
        ("empty array", "Biên `<=` khiến bản gốc crash ở đây — sau khi sửa thì không."),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M4_MD = r'''
The Statistics Bureau processes test scores in one pass each.

Implement three methods over an `int[] scores` (each 0–100; the array is
never empty):

1. `int average(int[] scores)` — the mean **rounded down** to a whole
   number (`(int)` truncation is acceptable and expected).
2. `int passRate(int[] scores)` — the percentage of scores ≥ 60, rounded
   down (an integer 0–100, not a double).
3. `int secondLargest(int[] scores)` — the second-largest DISTINCT value;
   every score is guaranteed to appear at least twice or the array is
   guaranteed to hold at least two distinct values — when all values are
   identical, return that value itself.

One loop per method (no `Arrays.sort` — this is a loops exercise), each
carrying only the state it needs. `average({70, 80, 91})` is 80;
`passRate({70, 80, 91})` is 100; `secondLargest({90, 90, 85})` is 85.
'''

CK_M4_MD_VI = r'''
Cục thống kê xử lý điểm thi, mỗi phép tính một lượt.

Viết ba phương thức trên `int[] scores` (mỗi phần tử 0–100; mảng không bao
giờ rỗng):

1. `int average(int[] scores)` — trung bình **làm tròn xuống** số nguyên
   (`(int)` cắt phần lẻ là chấp nhận được và được kỳ vọng).
2. `int passRate(int[] scores)` — phần trăm điểm ≥ 60, làm tròn xuống
   (số nguyên 0–100, không phải double).
3. `int secondLargest(int[] scores)` — giá trị lớn thứ hai KHÁC NHAU; mỗi
   điểm được bảo đảm xuất hiện ít nhất hai lần, hoặc mảng có ít nhất hai
   giá trị khác nhau — khi mọi giá trị giống nhau, trả chính giá trị đó.

Mỗi phương thức một vòng lặp (không dùng `Arrays.sort` — đây là bài tập
vòng lặp), mỗi vòng chỉ mang trạng thái nó cần. `average({70, 80, 91})`
là 80; `passRate({70, 80, 91})` là 100; `secondLargest({90, 90, 85})` là 85.
'''

CK_M4_CH = challenge(
    "javb-checkpoint-loops",
    "Checkpoint: Statistics Bureau",
    CK_M4_MD,
    r'''public class Solution {
    public static int average(int[] scores) {
        return 0;
    }

    public static int passRate(int[] scores) {
        return 0;
    }

    public static int secondLargest(int[] scores) {
        return 0;
    }
}
''',
    [
        (
            "average truncates",
            r"""
CjTestBase.checkEq(Solution.average(new int[]{70, 80, 91}), 80, "80.33 -> 80");
CjTestBase.checkEq(Solution.average(new int[]{50, 51}), 50, "50.5 -> 50");
""",
            "Sum as long, divide, truncate.",
        ),
        (
            "pass rate",
            r"""
CjTestBase.checkEq(Solution.passRate(new int[]{70, 80, 91}), 100, "all pass");
CjTestBase.checkEq(Solution.passRate(new int[]{59, 60, 20}), 33, "one of three, truncated");
""",
            "Count >= 60, multiply by 100, divide by length — in that order, with ints.",
        ),
        (
            "second largest distinct",
            r"""
CjTestBase.checkEq(Solution.secondLargest(new int[]{90, 90, 85}), 85, "85 is second");
CjTestBase.checkEq(Solution.secondLargest(new int[]{10, 20, 20, 30}), 20, "20 is second of distinct");
CjTestBase.checkEq(Solution.secondLargest(new int[]{7}), 7, "all identical");
""",
            "Track max and second-max; skip values equal to max; seed for the identical case.",
        ),
    ],
    difficulty="beginner",
)

CK_M4_VI = vi_challenge(
    "Checkpoint: Cục thống kê",
    CK_M4_MD_VI,
    [
        ("average truncates", "Cộng vào long, chia, cắt phần lẻ."),
        ("pass rate", "Đếm >= 60, nhân 100, chia cho độ dài — đúng thứ tự đó, với số nguyên."),
        ("second largest distinct", "Theo dõi max và second-max; bỏ qua giá trị bằng max; hạt giống cho trường hợp giống nhau."),
    ],
)

CK_M4_R = r'''public class Solution {
    public static int average(int[] scores) {
        long sum = 0;
        for (int s : scores) {
            sum += s;
        }
        return (int) (sum / scores.length);
    }

    public static int passRate(int[] scores) {
        int passing = 0;
        for (int s : scores) {
            if (s >= 60) {
                passing++;
            }
        }
        return passing * 100 / scores.length;
    }

    public static int secondLargest(int[] scores) {
        int max = Integer.MIN_VALUE;
        int second = Integer.MIN_VALUE;
        for (int s : scores) {
            if (s > max) {
                second = max;
                max = s;
            } else if (s > second && s != max) {
                second = s;
            }
        }
        if (second == Integer.MIN_VALUE) {
            return max;   // all values identical (or single value)
        }
        return second;
    }
}
'''

CK_M4_W = r'''public class Solution {
    public static int average(int[] scores) {
        // BUG: int accumulator + int division is fine here, but the pass rate
        // below multiplies after dividing. Kept for parity.
        long sum = 0;
        for (int s : scores) {
            sum += s;
        }
        return (int) (sum / scores.length);
    }

    public static int passRate(int[] scores) {
        int passing = 0;
        for (int s : scores) {
            if (s >= 60) {
                passing++;
            }
        }
        // BUG: divides first — integer math makes one-of-three 0 instead of 33
        return passing / scores.length * 100;
    }

    public static int secondLargest(int[] scores) {
        int max = Integer.MIN_VALUE;
        int second = Integer.MIN_VALUE;
        for (int s : scores) {
            if (s > max) {
                second = max;
                max = s;
            } else if (s > second && s != max) {
                second = s;
            }
        }
        if (second == Integer.MIN_VALUE) {
            return max;
        }
        return second;
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Loops: Repetition With Control",
    "Counting for, condition while, break/continue, the accumulator-counter-extremum patterns, and nested loops with cost intuition.",
    "Vòng lặp: lặp lại có kiểm soát",
    "for đếm, while theo điều kiện, break/continue, các pattern tích lũy-đếm-cực trị, và vòng lặp lồng với trực giác chi phí.",
    ["for-and-foreach", "while-do-and-jumps", "accumulator-patterns", "nested-loops", "java-checkpoint-loops"],
    ["javb-p4-loops"],
)

write_lesson(
    MOD, "for-and-foreach",
    "for & for-each",
    "The three-part header, zero-based counting, and choosing index vs element.", 15,
    L_FOR_EN,
    "for & for-each",
    "Header ba phần, đếm từ 0, và chọn giữa chỉ số và phần tử.",
    L_FOR_VI,
)

write_lesson(
    MOD, "while-do-and-jumps",
    "while, do-while, break & continue",
    "Condition-first vs body-first, the search idiom with an outside variable, and honest infinite loops.", 15,
    L_WHILE_EN,
    "while, do-while, break & continue",
    "Kiểm-trước vs chạy-trước, thành ngữ tìm kiếm với biến bên ngoài, và vòng vô hạn trung thực.",
    L_WHILE_VI,
)

write_lesson(
    MOD, "accumulator-patterns",
    "Accumulator, Counter, Best-So-Far",
    "The three state-carrying patterns, seed values that matter, and the money trap of floating points.", 15,
    L_ACCUM_EN,
    "Tích lũy, đếm, tốt-nhất-từ-trước-tới-nay",
    "Ba pattern mang trạng thái, giá trị hạt giống quan trọng, và bẫy số thực của tiền bạc.",
    L_ACCUM_VI,
)

write_lesson(
    MOD, "nested-loops",
    "Nested Loops",
    "Loops inside loops: tables, triangles, pairwise work, and the first intuition of squaring cost.", 15,
    L_NESTED_EN,
    "Vòng lặp lồng",
    "Vòng trong vòng: bảng, tam giác, công việc theo cặp, và trực giác đầu tiên về chi phí bình phương.",
    L_NESTED_VI,
)

write_practice(
    MOD, "javb-p4-loops",
    "Practice: Loops",
    "Totals, maxima with positions, simulated games, star triangles, and a loop that skips and lies.",
    "Thực hành: Vòng lặp",
    "Tổng, giá trị lớn nhất kèm vị trí, trò chơi mô phỏng, tam giác sao, và một vòng lặp bỏ sót lại nói dối.",
    "while-do-and-jumps", 55, "beginner",
    [P4_TOTAL, P4_MAX, P4_GUESS, P4_TRIANGLE, P4_FIX],
    {c["id"]: v for c, v in [
        (P4_TOTAL, P4_TOTAL_VI), (P4_MAX, P4_MAX_VI), (P4_GUESS, P4_GUESS_VI),
        (P4_TRIANGLE, P4_TRIANGLE_VI), (P4_FIX, P4_FIX_VI)]},
    solutions=[
        (
            P4_TOTAL["id"],
            r'''public class Solution {
    public static long total(int[] values) {
        long sum = 0;
        for (int v : values) {
            sum += v;
        }
        return sum;
    }
}
''',
            r'''public class Solution {
    public static long total(int[] values) {
        // BUG: int accumulator wraps for big values
        int sum = 0;
        for (int v : values) {
            sum += v;
        }
        return sum;
    }
}
''',
        ),
        (
            P4_MAX["id"],
            r'''public class Solution {
    public static int[] maxWithIndex(int[] values) {
        if (values.length == 0) {
            return new int[]{-1, -1};
        }
        int max = values[0];
        int idx = 0;
        for (int i = 1; i < values.length; i++) {
            if (values[i] > max) {
                max = values[i];
                idx = i;
            }
        }
        return new int[]{max, idx};
    }
}
''',
            r'''public class Solution {
    public static int[] maxWithIndex(int[] values) {
        int max = Integer.MIN_VALUE;
        int idx = -1;
        for (int i = 0; i < values.length; i++) {
            // BUG: >= flips ties to the LAST occurrence
            if (values[i] >= max) {
                max = values[i];
                idx = i;
            }
        }
        return new int[]{max, idx};
    }
}
''',
        ),
        (
            P4_GUESS["id"],
            r'''public class Solution {
    public static int guesses(int secret, int maxAttempts) {
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            if (attempt == secret) {
                return attempt;
            }
        }
        return -1;
    }
}
''',
            r'''public class Solution {
    public static int guesses(int secret, int maxAttempts) {
        // BUG: loop stops one attempt short
        for (int attempt = 1; attempt < maxAttempts; attempt++) {
            if (attempt == secret) {
                return attempt;
            }
        }
        return -1;
    }
}
''',
        ),
        (
            P4_TRIANGLE["id"],
            r'''public class Solution {
    public static void program(int n) {
        for (int row = 1; row <= n; row++) {
            for (int star = 0; star < row; star++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
''',
            r'''public class Solution {
    public static void program(int n) {
        for (int row = 1; row <= n; row++) {
            for (int star = 0; star < row; star++) {
                System.out.print("*");
            }
            System.out.print("*");   // BUG: stray extra star per row
        }
        System.out.println();
    }
}
''',
        ),
        (
            P4_FIX["id"],
            r'''public class Solution {
    public static int firstEven(int[] values) {
        int found = -1;
        for (int i = 0; i < values.length; i++) {
            if (values[i] % 2 == 0) {
                found = i;
                break;
            }
        }
        return found;
    }
}
''',
            r'''public class Solution {
    public static int firstEven(int[] values) {
        // BUG: original break-on-odd restored
        int found = -1;
        for (int i = 0; i < values.length; i++) {
            if (values[i] % 2 != 0) {
                break;
            }
            if (values[i] % 2 == 0) {
                found = i;
                break;
            }
        }
        return found;
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-loops",
    "Checkpoint: Statistics Bureau",
    "Average, pass rate, and second-largest in single passes — accumulators, counters, and extremum tracking under one roof.", 45, CK_M4_MD,
    "Checkpoint: Cục thống kê",
    "Trung bình, tỷ lệ đạt, và lớn-thứ-hai trong từng lượt — tích lũy, đếm, và theo dõi cực trị dưới một mái nhà.",
    CK_M4_MD_VI,
    CK_M4_CH, CK_M4_VI,
    solution=CK_M4_R, wrong=CK_M4_W,
)

print("module 4 complete")
