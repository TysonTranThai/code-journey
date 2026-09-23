#!/usr/bin/env python3
"""AP CSA M5 — Loops (while, for, nesting, tracing)."""
from apc import *

M = "apc-loops"

L1 = r"""
A **while** loop repeats as long as its condition is true — checked *before*
each pass:

```java
int count = 1;
while (count <= 3) {
    System.out.println(count);
    count++;              // the update MUST move toward the exit
}
// prints 1 2 3
```

Trace the four contact points: initialize → test → body → update → test...

Two classic failures:

- **Infinite loop**: the update is missing or moves the wrong way
  (`count--` with a `count <= 3` test never exits).
- **Off-by-one**: `<` vs `<=` decides whether the last value is processed.

A **sentinel loop** reads until a special value appears — the pattern behind
"read numbers until the user types -1". On the exam it appears as "process
elements of an array until a negative price" style tasks:

```java
int i = 0;
while (i < data.length && data[i] >= 0) {
    total += data[i];
    i++;
}
```

The `&&` ordering matters: test the index bound **before** indexing, or the
last check reads past the end.
"""

L2 = r"""
The **for** loop packs init / test / update into one header — the workhorse:

```java
for (int i = 0; i < 5; i++) {
    System.out.print(i);
}
// prints 01234
```

Execution order: init once → test → body → update → test → ... Exactly
equivalent to the while version, but the three loop-control pieces are
visible in one line, so nothing can be forgotten.

**Counting problems** (how many times does the loop run?) are pure exam
material:

- `for (int i = 0; i < n; i++)` runs exactly `n` times.
- `for (int i = 1; i <= n; i++)` runs exactly `n` times.
- `for (int i = 0; i <= n; i++)` runs `n + 1` times — the off-by-one.
- `for (int i = 0; i < n; i += 2)` runs `ceil(n / 2.0)` times.

**Accumulator and counter** inside loops:

```java
int total = 0, count = 0;
for (int i = 1; i <= 10; i++) {
    if (i % 2 == 0) {
        total += i;
        count++;
    }
}
// total 30, count 5
```

The accumulator is declared **outside** the loop; resetting it inside is a
favorite exam bug.
"""

L3 = r"""
**Nested loops** — the inner loop runs completely for every single pass of
the outer loop:

```java
for (int row = 1; row <= 3; row++) {
    for (int col = 1; col <= 4; col++) {
        System.out.print(col);
    }
    System.out.println();
}
// 1234
// 1234
// 1234
```

The inner body ran 3 × 4 = 12 times. When you see nested loops, compute the
total iteration count first: it is the product.

**Triangle patterns** show the inner bound depending on the outer variable:

```java
for (int row = 1; row <= 4; row++) {
    for (int star = 1; star <= row; star++) {
        System.out.print("*");
    }
    System.out.println();
}
```

prints a staircase: 1, 2, 3, then 4 stars. Total work: 1+2+3+4 = 10
iterations — the shape of many O(n²) discussions later.

**do-while** (rare on the exam, know its shape): the body runs *first*, the
test runs after — so the body always executes at least once. Use while/for
in your own code; trace do-when it appears.
"""

write_module(
    M,
    "Selection and Iteration II: Loops",
    "while and for, counting loop iterations, accumulators and counters, sentinels, nested loops and their cost.",
    "Rẽ nhánh và lặp II: Vòng lặp",
    "while và for, đếm số lần lặp, bộ tích lũy và bộ đếm, giá trị dừng, vòng lặp lồng nhau và cái giá của nó.",
    lessons=["apc-m5-while", "apc-m5-for", "apc-m5-nested", "apc-cp-m5"],
    practices=["apc-p5-loops"],
)

write_lesson(
    M, "apc-m5-while", "while loops and sentinels",
    "Pre-test loops, the four contact points, infinite loops, sentinel scans.",
    12, L1,
    "Vòng lặp while và giá trị dừng",
    "Vòng lặp kiểm-trước, bốn điểm chạm, vòng lặp vô hạn, quét theo giá trị dừng.",
    r"""
Vòng **while** lặp miễn là điều kiện còn đúng — được kiểm tra *trước* mỗi
lượt:

```java
int count = 1;
while (count <= 3) {
    System.out.println(count);
    count++;              // bước cập nhật PHẢI đưa đến chỗ thoát
}
// in 1 2 3
```

Truy vết bốn điểm chạm: khởi tạo → kiểm tra → thân → cập nhật → kiểm tra...

Hai lỗi kinh điển:

- **Vòng lặp vô hạn**: thiếu bước cập nhật hoặc cập nhật đi sai hướng
  (`count--` với điều kiện `count <= 3` không bao giờ thoát).
- **Lệch một đơn vị**: `<` với `<=` quyết định giá trị cuối có được xử lý
  không.

**Vòng lặp theo giá trị dừng** đọc cho đến khi gặp giá trị đặc biệt — mẫu
"đọc số đến khi người dùng nhập -1". Trong đề thi nó xuất hiện dạng "xử lý
các phần tử của mảng cho đến khi gặp giá trị âm":

```java
int i = 0;
while (i < data.length && data[i] >= 0) {
    total += data[i];
    i++;
}
```

Thứ tự `&&` rất quan trọng: kiểm tra biên chỉ số **trước khi** truy cập mảng,
nếu không lần kiểm tra cuối sẽ đọc vượt qua cuối mảng.
""",
)

write_lesson(
    M, "apc-m5-for", "for loops and counting",
    "The for header, iteration counts, accumulators and counters.",
    12, L2,
    "Vòng lặp for và phép đếm",
    "Cấu trúc for, số lần lặp, bộ tích lũy và bộ đếm.",
    r"""
Vòng **for** gói khởi tạo / kiểm tra / cập nhật vào một dòng tiêu đề — con
ngựa thồ:

```java
for (int i = 0; i < 5; i++) {
    System.out.print(i);
}
// in 01234
```

Trình tự chạy: khởi tạo một lần → kiểm tra → thân → cập nhật → kiểm tra →...
Giống hệt bản while nhưng ba mảnh điều khiển nằm trên một dòng nên không thể
quên.

**Bài đếm** (vòng lặp chạy bao nhiêu lần?) là đề thi thuần túy:

- `for (int i = 0; i < n; i++)` chạy đúng `n` lần.
- `for (int i = 1; i <= n; i++)` chạy đúng `n` lần.
- `for (int i = 0; i <= n; i++)` chạy `n + 1` lần — lỗi lệch một.
- `for (int i = 0; i < n; i += 2)` chạy `ceil(n / 2.0)` lần.

**Bộ tích lũy và bộ đếm** trong vòng lặp:

```java
int total = 0, count = 0;
for (int i = 1; i <= 10; i++) {
    if (i % 2 == 0) {
        total += i;
        count++;
    }
}
// total 30, count 5
```

Bộ tích lũy được khai báo **ngoài** vòng lặp; đặt lại nó bên trong là lỗi đề
thi ưa thích.
""",
)

write_lesson(
    M, "apc-m5-nested", "Nested loops",
    "Iteration products, dependent inner bounds, total-cost intuition.",
    12, L3,
    "Vòng lặp lồng nhau",
    "Tích số lần lặp, biên trong phụ thuộc biến ngoài, trực giác về tổng chi phí.",
    r"""
**Vòng lặp lồng nhau** — vòng trong chạy trọn vẹn cho từng lượt của vòng
ngoài:

```java
for (int row = 1; row <= 3; row++) {
    for (int col = 1; col <= 4; col++) {
        System.out.print(col);
    }
    System.out.println();
}
// 1234
// 1234
// 1234
```

Thân vòng trong đã chạy 3 × 4 = 12 lần. Thấy vòng lặp lồng nhau là hãy tính
trước tổng số lần lặp: đó là tích của hai khoảng.

**Mẫu tam giác** cho thấy biên của vòng trong phụ thuộc biến vòng ngoài:

```java
for (int row = 1; row <= 4; row++) {
    for (int star = 1; star <= row; star++) {
        System.out.print("*");
    }
    System.out.println();
}
```

in một cầu thang: 1, 2, 3, rồi 4 dấu sao. Tổng công việc: 1+2+3+4 = 10 lần
lặp — hình dạng của nhiều cuộc thảo luận O(n²) sau này.

**do-while** (hiếm trong đề thi, biết hình dạng): thân chạy *trước*, kiểm tra
chạy *sau* — nên thân luôn chạy ít nhất một lần. Dùng while/for khi tự viết;
truy vết do-while khi đề đưa ra.
""",
)

BOILER_SUM = r"""public class Solution {
    public static int sumTo(int n) {
        return 0; // replace: 1 + 2 + ... + n (n >= 1)
    }
}
"""

BOILER_EVENS = r"""public class Solution {
    public static String evens(int n) {
        return ""; // replace: even numbers 2..2n, comma-separated
    }
}
"""

BOILER_DIGITS = r"""public class Solution {
    public static int digitSum(int n) {
        return 0; // replace: sum of the digits of n (n >= 0)
    }
}
"""

BOILER_BOX = r"""public class Solution {
    public static String box(int rows, int cols) {
        return ""; // replace: rows lines of cols '#', newline-terminated
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static int sumRange(int lo, int hi) {
        int total = 0;
        for (int i = lo; i < hi; i++) {
            total += i;
        }
        return total;
    }
}
"""

CP_MUL = r"""public class Solution {
    public static String timesTable(int n) {
        return ""; // replace: n lines, line k = k*1 k*2 ... k*n space-separated
    }
}
"""

P_SUM = challenge(
    "apc-m5-sumto",
    "Sum with a for loop",
    "Implement `int sumTo(int n)`: return 1 + 2 + ... + n using a loop (not the closed-form formula).",
    BOILER_SUM,
    [(
        "sums correctly",
        r"""
CjTestBase.checkEq(Solution.sumTo(1), 1, "single term");
CjTestBase.checkEq(Solution.sumTo(5), 15, "1..5");
CjTestBase.checkEq(Solution.sumTo(100), 5050, "1..100");
""",
        "Accumulator starts at 0 outside; loop i from 1 to n inclusive.",
    )],
    level="imitation",
)

P_EVENS = challenge(
    "apc-m5-evens",
    "Build output in a loop",
    "Implement `String evens(int n)`: return the even numbers 2, 4, ..., 2n joined by \", \" — e.g. `evens(3)` returns \"2, 4, 6\". Accumulate into a String; add \", \" **before** each item except the first.",
    BOILER_EVENS,
    [(
        "comma separated",
        r"""
CjTestBase.checkEq(Solution.evens(1), "2", "single");
CjTestBase.checkEq(Solution.evens(3), "2, 4, 6", "three items");
CjTestBase.checkEq(Solution.evens(5), "2, 4, 6, 8, 10", "five items");
""",
        "Guard: separator goes in only when the string is non-empty (or track an index).",
    )],
    level="guided",
)

P_DIG = challenge(
    "apc-m5-digitsum",
    "Digit sums with % and /",
    "Implement `int digitSum(int n)`: the sum of the digits of non-negative `n` — e.g. `digitSum(1305)` is 9. Combine a while loop with `% 10` (last digit) and `/ 10` (drop last digit).",
    BOILER_DIGITS,
    [(
        "digit extraction",
        r"""
CjTestBase.checkEq(Solution.digitSum(7), 7, "single digit");
CjTestBase.checkEq(Solution.digitSum(1305), 9, "1+3+0+5");
CjTestBase.checkEq(Solution.digitSum(999), 27, "three nines");
CjTestBase.checkEq(Solution.digitSum(0), 0, "zero");
""",
        "while (n > 0) { sum += n % 10; n /= 10; }",
    )],
    level="combination",
)

P_BOX = challenge(
    "apc-m5-box",
    "Nested-loop rectangle",
    "Implement `String box(int rows, int cols)`: a rectangle of `#` with `rows` lines and `cols` characters per line, each line ended by `\\n`. `box(2, 3)` returns \"###\\n###\\n\". Build it with two nested loops (the inner prints one line).",
    BOILER_BOX,
    [(
        "exact rectangle",
        r"""
CjTestBase.checkEq(Solution.box(1, 1), "#\n", "one cell");
CjTestBase.checkEq(Solution.box(2, 3), "###\n###\n", "2 by 3");
CjTestBase.checkEq(Solution.box(3, 1), "#\n#\n#\n", "column");
""",
        "Outer loop appends a newline after each full inner row.",
    )],
    level="independent",
)

P_FIX = challenge(
    "apc-m5-fix-range",
    "Debug the range sum",
    "`sumRange(lo, hi)` should return lo + (lo+1) + ... + hi, both ends inclusive. It fails for every call. Trace the loop with lo=2, hi=4 (expected 9) to find the flaw, then fix it minimally.",
    BOILER_FIX,
    [(
        "inclusive both ends",
        r"""
CjTestBase.checkEq(Solution.sumRange(2, 4), 9, "2+3+4");
CjTestBase.checkEq(Solution.sumRange(5, 5), 5, "single-element range");
CjTestBase.checkEq(Solution.sumRange(1, 10), 55, "1..10");
""",
        "The test i < hi skips the last value; i <= hi fixes it.",
    )],
    level="debugging",
)

CP5 = challenge(
    "apc-cp-m5-table",
    "Checkpoint: multiplication table",
    "Implement `String timesTable(int n)`: return `n` lines; line `k` (1-based) contains the products k*1, k*2, ..., k*n separated by single spaces, and ends with `\\n`. `timesTable(3)` starts \"1 2 3\\n2 4 6\\n3 6 9\\n\".",
    CP_MUL,
    [(
        "table rows",
        r"""
CjTestBase.checkEq(Solution.timesTable(1), "1\n", "1x1");
CjTestBase.checkEq(Solution.timesTable(3), "1 2 3\n2 4 6\n3 6 9\n", "3 rows");
CjTestBase.checkEq(Solution.timesTable(2), "1 2\n2 4\n", "2 rows symmetric check");
CjTestBase.checkEq(Solution.timesTable(4), "1 2 3 4\n2 4 6 8\n3 6 9 12\n4 8 12 16\n", "4 rows asymmetric");
""",
        "Outer loop picks the row k; inner loop builds k*1..k*n with spaces between.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p5-loops", "Loop rep", "Counting, accumulation, digit surgery, nested construction.",
    "Luyện vòng lặp", "Đếm, tích lũy, phẫu thuật chữ số, dựng bằng vòng lồng.",
    after_lesson="apc-m5-for", minutes=50, difficulty="beginner",
    challenges=[P_SUM, P_EVENS, P_DIG, P_BOX, P_FIX],
    vi_challenges={
        "apc-m5-sumto": vi_challenge("Tổng bằng vòng for", "Cài đặt `int sumTo(int n)`: trả về 1 + 2 + ... + n bằng vòng lặp (không dùng công thức tổng).",
            [("sums correctly", "Bộ tích lũy bắt đầu 0 ở ngoài; vòng i chạy từ 1 đến n gồm cả hai đầu.")]),
        "apc-m5-evens": vi_challenge("Dựng kết quả trong vòng lặp", "Cài đặt `String evens(int n)`: trả về các số chẵn 2, 4, ..., 2n nối bằng \", \" — ví dụ `evens(3)` cho \"2, 4, 6\". Tích lũy vào String; thêm \", \" **trước** mỗi phần tử trừ phần tử đầu.",
            [("comma separated", "Chốt: dấu phẩy chỉ thêm khi chuỗi chưa rỗng (hoặc theo dõi chỉ số).")]),
        "apc-m5-digitsum": vi_challenge("Tổng chữ số với % và /", "Cài đặt `int digitSum(int n)`: tổng các chữ số của `n` không âm — ví dụ `digitSum(1305)` là 9. Kết hợp while với `% 10` (chữ số cuối) và `/ 10` (bỏ chữ số cuối).",
            [("digit extraction", "while (n > 0) { sum += n % 10; n /= 10; }")]),
        "apc-m5-box": vi_challenge("Hình chữ nhật bằng vòng lồng", "Cài đặt `String box(int rows, int cols)`: hình chữ nhật `#` gồm `rows` dòng, mỗi dòng `cols` ký tự, kết thúc mỗi dòng bằng `\\n`. `box(2, 3)` cho \"###\\n###\\n\". Dựng bằng hai vòng lồng (vòng trong in một dòng).",
            [("exact rectangle", "Vòng ngoài thêm \\n sau mỗi dòng đầy đủ của vòng trong.")]),
        "apc-m5-fix-range": vi_challenge("Sửa tổng khoảng", "`sumRange(lo, hi)` phải trả về lo + (lo+1) + ... + hi, gồm cả hai đầu. Nó sai với mọi lời gọi. Truy vết vòng lặp với lo=2, hi=4 (kỳ vọng 9) để tìm khuyết tật, rồi sửa tối thiểu.",
            [("inclusive both ends", "Điều kiện i < hi bỏ sót giá trị cuối; i <= hi sửa được.")]),
    },
    solutions=[
        ("apc-m5-sumto", r"""public class Solution {
    public static int sumTo(int n) {
        int total = 0;
        for (int i = 1; i <= n; i++) {
            total += i;
        }
        return total;
    }
}
""",
         r"""public class Solution {
    public static int sumTo(int n) {
        // BUG: skips the first term
        int total = 0;
        for (int i = 2; i <= n; i++) {
            total += i;
        }
        return total;
    }
}
"""),
        ("apc-m5-evens", r"""public class Solution {
    public static String evens(int n) {
        String s = "";
        for (int i = 1; i <= n; i++) {
            if (!s.isEmpty()) {
                s += ", ";
            }
            s += (2 * i);
        }
        return s;
    }
}
""",
         r"""public class Solution {
    public static String evens(int n) {
        // BUG: separator after every item — trailing ", "
        String s = "";
        for (int i = 1; i <= n; i++) {
            s += (2 * i) + ", ";
        }
        return s;
    }
}
"""),
        ("apc-m5-digitsum", r"""public class Solution {
    public static int digitSum(int n) {
        int sum = 0;
        while (n > 0) {
            sum += n % 10;
            n /= 10;
        }
        return sum;
    }
}
""",
         r"""public class Solution {
    public static int digitSum(int n) {
        // BUG: divides before reading the digit — misses the last one
        int sum = 0;
        while (n > 0) {
            n /= 10;
            sum += n % 10;
        }
        return sum;
    }
}
"""),
        ("apc-m5-box", r"""public class Solution {
    public static String box(int rows, int cols) {
        String out = "";
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                out += "#";
            }
            out += "\n";
        }
        return out;
    }
}
""",
         r"""public class Solution {
    public static String box(int rows, int cols) {
        // BUG: rows and cols swapped — wide boxes become tall
        String out = "";
        for (int r = 0; r < cols; r++) {
            for (int c = 0; c < rows; c++) {
                out += "#";
            }
            out += "\n";
        }
        return out;
    }
}
"""),
        ("apc-m5-fix-range", r"""public class Solution {
    public static int sumRange(int lo, int hi) {
        int total = 0;
        for (int i = lo; i <= hi; i++) {
            total += i;
        }
        return total;
    }
}
""",
         r"""public class Solution {
    public static int sumRange(int lo, int hi) {
        // BUG: original flaw kept — i < hi drops the last term
        int total = 0;
        for (int i = lo; i < hi; i++) {
            total += i;
        }
        return total;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m5", "Checkpoint: loops",
    "Two-dimensional output built with nested loops, exact separators.",
    20,
    r"""
A multiplication table is the classic nested-loop build: rows depend on the
outer index, separators depend on position, and the exact string — newlines
included — is the deliverable. Plan the inner line-builder first.
""",
    "Điểm kiểm tra: vòng lặp",
    "Kết quả hai chiều dựng bằng vòng lặp lồng nhau, dấu ngăn cách chính xác.",
    r"""
Bảng cửu chương là bài dựng vòng lồng kinh điển: dòng phụ thuộc chỉ số ngoài,
dấu ngăn cách phụ thuộc vị trí, và chuỗi chính xác — gồm cả \\n — là sản
phẩm. Lên kế hoạch cho bộ dựng dòng trong trước.
""",
    CP5,
    vi_challenge("Điểm kiểm tra: vòng lặp", "Cài đặt `String timesTable(int n)`: trả về `n` dòng; dòng `k` (tính từ 1) chứa các tích k*1, k*2, ..., k*n ngăn bởi một dấu cách, và kết thúc bằng `\\n`. `timesTable(3)` bắt đầu \"1 2 3\\n2 4 6\\n3 6 9\\n\".",
        [("table rows", "Vòng ngoài chọn dòng k; vòng trong dựng k*1..k*n với dấu cách giữa các tích.")]),
    solution=r"""public class Solution {
    public static String timesTable(int n) {
        String out = "";
        for (int k = 1; k <= n; k++) {
            String line = "";
            for (int j = 1; j <= n; j++) {
                if (!line.isEmpty()) {
                    line += " ";
                }
                line += (k * j);
            }
            out += line + "\n";
        }
        return out;
    }
}
""",
    wrong=r"""public class Solution {
    public static String timesTable(int n) {
        // BUG: inner bound j <= k — builds a triangle, not a square table
        String out = "";
        for (int k = 1; k <= n; k++) {
            String line = "";
            for (int j = 1; j <= k; j++) {
                if (!line.isEmpty()) {
                    line += " ";
                }
                line += (k * j);
            }
            out += line + "\n";
        }
        return out;
    }
}
""",
)
