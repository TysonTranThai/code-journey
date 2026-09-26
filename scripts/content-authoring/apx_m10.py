#!/usr/bin/env python3
"""AP CSA Advanced M10 — Recursion challenge lab (verified ground truths)."""
from apx import *

M = "apx-recursion"

write_module(
    M,
    "Recursion Challenge Lab",
    "Recursive tracing, base-case hunting, two-branch recursion, and recursive strings — AP-aligned, harder than the intro. Difficulty E3–E4.",
    "Phòng thí nghiệm đệ quy",
    "Truy vết đệ quy, săn trường hợp cơ sở, đệ quy hai nhánh, và chuỗi đệ quy — bám sát đề, khó hơn phần nhập môn. Độ khó E3–E4.",
    lessons=["apx-m10-tracing", "apx-m10-bases", "apx-m10-strings", "apx-cp-m10"],
    practices=["apx-p10-recursion"],
)

L1 = r"""
**Recursive tracing is bookkeeping, not magic.** For a single-branch
call chain (`f(n) = f(n-1) + n`), unroll downward to the base, then
roll back up, writing one value per level:

```java
public static int f(int n) {
    if (n <= 0) { return 1; }
    return f(n - 1) + n;
}
// f(4): f(3)+4 ... f(0)=1 → 1+1=2 → 2+2=4 → 4+3=7 → 7+4=11
```

The two errors students make: stopping the roll-up one level early
(off-by-one from base to first addition), and misreading the base
case's value (1 vs 0 changes everything — trace it, don't assume).

**For two-branch recursion** (`mystery(n-1) + 2` vs `mystery(n-1) *
2` chosen by parity), the chain is still linear here — only ONE
branch runs per call — but the branch *switches* as n changes. Draw
the chain with the branch decision at each level:

```java
// mystery(5): odd → mystery(4)*2; mystery(4): even → mystery(3)+2;
// mystery(3): odd → mystery(2)*2; mystery(2): even → mystery(1)+2;
// mystery(1): odd → mystery(0)*2; mystery(0) = 0
// roll up: 0*2=0 → 0+2=2 → 2*2=4 → 4+2=6 → 6*2=12
```
"""

L2 = r"""
**Base cases are the whole grade.** An FRQ recursion task is scored
almost entirely on: correct base case(s), correct progress toward
them, and correct combination. The hunting checklist:

1. **What input cannot be broken down further?** Empty string,
   length ≤ 1, n == 0, i == array length.
2. **Is there more than one base?** Subset-sum has two: success
   (target == 0) and exhaustion (i == length with target != 0).
3. **Does progress always shrink?** `substring(1)` shrinks;
   `n - 1` shrinks; `n / 2` shrinks for n ≥ 1. A branch that does
   not shrink is infinite recursion (StackOverflowError).
4. **Integer division and negatives**: `n / 2` of 1 is 0 — make sure
   that lands on a base case, not below it.

**Progress discipline on arrays/strings**: pass the index (i+1), or
pass the remainder (`substring(1)`). Passing whole subarrays each
call is wasteful but legal; passing nothing new is illegal.
"""

L3 = r"""
**Recursive strings and self-similar problems.** The classic
recursion-into-reasoning problems:

- **Reverse**: `rev(s) = rev(s.substring(1)) + s.charAt(0)` with
  base `length() <= 1`. The append order is the entire difficulty —
  swapping it produces the input unchanged.
- **Palindrome check with two indexes**: `isPal(s, lo, hi)` —
  compare ends, recurse inward. Base: `lo >= hi`.
- **Count structure**: "how many ways" problems (climb 1-or-2
  stairs) map to Fibonacci: `ways(n) = ways(n-1) + ways(n-2)`,
  bases `ways(0) = ways(1) = 1`. Recognize the shape; do not
  simulate all paths.
- **GCD**: Euclid's `gcd(a, b) = gcd(b, a % b)`, base `b == 0`.
  The exam loves it because it is progress-by-modulo.

Trace discipline: for strings, annotate each level with the
substring it receives — level widths shrink visibly, which makes the
base case obvious and wrong-index bugs visible.
"""

VI_L1 = r"""
**Truy vết đệ quy là việc ghi sổ, không phải phép màu.** Với chuỗi
lời gọi một nhánh (`f(n) = f(n-1) + n`), trải xuống đáy, rồi cuộn
ngược lên, mỗi tầng một giá trị:

```java
public static int f(int n) {
    if (n <= 0) { return 1; }
    return f(n - 1) + n;
}
// f(4): f(3)+4 ... f(0)=1 → 1+1=2 → 2+2=4 → 4+3=7 → 7+4=11
```

Hai lỗi học sinh hay mắc: dừng việc cuộn sớm một tầng (lệch một từ
trường hợp cơ sở đến phép cộng đầu), và đọc sai giá trị của trường hợp
cơ sở (1 với 0 đổi thay mọi thứ — truy vết, đừng giả định).

**Với đệ quy hai nhánh** (`mystery(n-1) + 2` so với `mystery(n-1) *
2` chọn theo tính chẵn lẻ), chuỗi vẫn tuyến tính ở đây — mỗi lời gọi
chỉ chạy MỘT nhánh — nhưng nhánh *đổi* khi n đổi. Vẽ chuỗi kèm quyết
định nhánh ở từng tầng:

```java
// mystery(5): lẻ → mystery(4)*2; mystery(4): chẵn → mystery(3)+2;
// mystery(3): lẻ → mystery(2)*2; mystery(2): chẵn → mystery(1)+2;
// mystery(1): lẻ → mystery(0)*2; mystery(0) = 0
// cuộn lên: 0*2=0 → 0+2=2 → 2*2=4 → 4+2=6 → 6*2=12
```
"""

VI_L2 = r"""
**Trường hợp cơ sở quyết định trọn điểm.** Một bài FRQ đệ quy được
chấm gần như hoàn toàn trên: trường hợp cơ sở đúng, tiến triển đúng
hướng về nó, và cách kết hợp đúng. Danh sách săn tìm:

1. **Đầu vào nào không thể phân rã thêm?** Chuỗi rỗng, độ dài ≤ 1,
   n == 0, i == độ dài mảng.
2. **Có nhiều hơn một trường hợp cơ sở không?** Subset-sum có hai:
   thành công (target == 0) và cạn kiệt (i == độ dài với target != 0).
3. **Tiến triển có luôn thu nhỏ không?** `substring(1)` thu nhỏ;
   `n - 1` thu nhỏ; `n / 2` thu nhỏ với n ≥ 1. Một nhánh không thu
   nhỏ là đệ quy vô hạn (StackOverflowError).
4. **Chia số nguyên và số âm**: `n / 2` của 1 là 0 — bảo đảm điều đó
   rơi vào trường hợp cơ sở, không phải dưới nó.

**Kỷ luật tiến triển trên mảng/chuỗi**: truyền chỉ số (i+1), hoặc
truyền phần còn lại (`substring(1)`). Truyền cả mảng con mỗi lời gọi
là lãng phí nhưng hợp lệ; truyền không có gì mới là bất hợp pháp.
"""

VI_L3 = r"""
**Chuỗi đệ quy và bài toán tự tương tự.** Các bài kinh điển đưa lý
lý vào đệ quy:

- **Đảo ngược**: `rev(s) = rev(s.substring(1)) + s.charAt(0)` với cơ
  sở `length() <= 1`. Thứ tự nối là toàn bộ độ khó — đổi chỗ cho ra
  đầu vào nguyên bản.
- **Kiểm tra palindrome với hai chỉ số**: `isPal(s, lo, hi)` — so
  hai đầu, đệ quy vào trong. Cơ sở: `lo >= hi`.
- **Đếm cấu trúc**: bài "có bao nhiêu cách" (leo cầu thang bước 1
  hoặc 2) ánh xạ sang Fibonacci: `ways(n) = ways(n-1) + ways(n-2)`,
  cơ sở `ways(0) = ways(1) = 1`. Nhận dạng hình dạng; đừng mô phỏng
  mọi đường đi.
- **GCD**: Euclid `gcd(a, b) = gcd(b, a % b)`, cơ sở `b == 0`. Đề
  thi yêu nó vì tiến triển bằng phép lấy dư.

Kỷ luật truy vết: với chuỗi, chú thích mỗi tầng bằng substring nó
nhận — bề rộng các tầng thu nhỏ rõ ràng, giúp trường hợp cơ sở hiển
nhiên và lỗi chỉ số thấy được.
"""

BOILER_INT = r"""public class Solution {
    public static int process(int n) {
        return 0; // replace
    }
}
"""

BOILER_GCD = r"""public class Solution {
    public static int gcd(int a, int b) {
        return 0; // replace: recursive Euclid, assumes a, b >= 0
    }
}
"""

P_MYSTERY = challenge(
    "apx-m10-mystery",
    "Trace the parity machine",
    "Trace **on paper**, then return the value:\n\n```java\n"
    "public static int mystery(int n) {\n    if (n <= 0) { return 0; }\n"
    "    if (n % 2 == 0) { return mystery(n - 1) + 2; }\n"
    "    return mystery(n - 1) * 2;\n}\n```\n\nImplement `process(int n)` "
    "to return `mystery(n)` for the given input n = 5.",
    BOILER_INT,
    [(
        "parity chain",
        r"""
CjTestBase.checkEq(Solution.process(5), 12, "odd-branch chain");
CjTestBase.checkEq(Solution.process(6), 14, "one more even step");
""",
        "Unroll: 0 → *2=0 → +2=2 → *2=4 → +2=6 → *2=12; mystery(6) adds one more +2.",
    )],
    level="independent",
    difficulty="advanced",
)

P_WAYS = challenge(
    "apx-m10-stairs",
    "Count the ways up the stairs",
    "You climb a staircase of `n` steps, taking **1 or 2 steps** at a "
    "time. Write a recursive method counting the distinct ways to "
    "exactly reach the top: `process(int n)` with bases `ways(0) = 1` "
    "and `ways(1) = 1` (the answer is Fibonacci-shaped).\n\nExample: "
    "n = 5 → 8.",
    BOILER_INT,
    [(
        "stairway ways",
        r"""
CjTestBase.checkEq(Solution.process(0), 1, "one way: stand still");
CjTestBase.checkEq(Solution.process(1), 1, "single step");
CjTestBase.checkEq(Solution.process(5), 8, "fibonacci shape");
CjTestBase.checkEq(Solution.process(2), 2, "1+1 or 2");
""",
        "ways(n) = ways(n-1) + ways(n-2); the two bases carry the count.",
    )],
    level="guided",
    difficulty="intermediate",
)

P_REV = challenge(
    "apx-m10-reverse",
    "Recursive reverse",
    "Reverse a string **recursively**: `process(String s)` returns s "
    "reversed, with base case length ≤ 1 and no loops allowed.\n\n"
    "Example: \"abcd\" → \"dcba\".",
    r"""public class Solution {
    public static String process(String s) {
        return ""; // replace: recursive reverse
    }
}
""",
    [(
        "reversed string",
        r"""
CjTestBase.checkEq(Solution.process("abcd"), "dcba", "four chars");
CjTestBase.checkEq(Solution.process(""), "", "empty base");
CjTestBase.checkEq(Solution.process("x"), "x", "single char base");
""",
        "rev(s) = rev(s.substring(1)) + s.charAt(0); append order is everything.",
    )],
    level="independent",
    difficulty="intermediate",
)

P_SUBSET = challenge(
    "apx-m10-subsetsum",
    "Subset sum",
    "Write `hasSum(int[] arr, int target)` returning true if **some "
    "subset** of the values sums to exactly target (each value used "
    "at most once). Use recursion over the index: at each element, "
    "either include it (target - value) or skip it. Empty subset sums "
    "to 0, so target 0 is always true.\n\nExamples: `{2,7,9}`, "
    "target 11 → true (2+9); target 5 → false.",
    r"""public class Solution {
    public static boolean hasSum(int[] arr, int target) {
        return false; // replace: recursive subset sum
    }

    // helper you may use: recurse over index i
}
""",
    [(
        "subset exists",
        r"""
CjTestBase.checkTrue(Solution.hasSum(new int[]{2, 7, 9}, 11), "2 + 9");
CjTestBase.checkTrue(!Solution.hasSum(new int[]{2, 7, 9}, 5), "no subset");
CjTestBase.checkTrue(Solution.hasSum(new int[]{}, 0), "empty subset");
CjTestBase.checkTrue(Solution.hasSum(new int[]{5}, 5), "single element");
""",
        "At index i: try include (target - arr[i]) or exclude; base i == length means target == 0.",
    )],
    level="real-world",
    difficulty="advanced",
)

P_GCD = challenge(
    "apx-m10-gcd",
    "Euclid's algorithm",
    "Implement `gcd(int a, int b)` recursively: base `b == 0` returns "
    "a; otherwise `gcd(b, a % b)`. Assumes non-negative inputs.\n\n"
    "Examples: gcd(48, 18) → 6; gcd(7, 13) → 1.",
    BOILER_GCD,
    [(
        "euclid recursion",
        r"""
CjTestBase.checkEq(Solution.gcd(48, 18), 6, "classic pair");
CjTestBase.checkEq(Solution.gcd(7, 13), 1, "coprime");
CjTestBase.checkEq(Solution.gcd(10, 0), 10, "zero base");
""",
        "One line of recursion; the base carries the answer.",
    )],
    level="imitation",
    difficulty="intermediate",
)

CP10 = challenge(
    "apx-cp-m10-digitsum",
    "Checkpoint: digital root",
    "The **digital root** of a non-negative number: if it has one "
    "digit, it is itself; otherwise it is the digital root of the sum "
    "of its digits. Implement `process(int n)` recursively (loop-free "
    "helper allowed for digit sum).\n\nExamples: 9875 → 9+8+7+5=29 → "
    "2+9=11 → 1+1=2, so `2`.",
    r"""public class Solution {
    public static int process(int n) {
        return 0; // replace: recursive digital root
    }
}
""",
    [(
        "digital root",
        r"""
CjTestBase.checkEq(Solution.process(9875), 2, "three rounds");
CjTestBase.checkEq(Solution.process(5), 5, "single digit");
CjTestBase.checkEq(Solution.process(0), 0, "zero base");
""",
        "Digit sum first (n % 10 + recurse n / 10), then recurse on the process itself until n < 10.",
    )],
    level="combination",
    difficulty="advanced",
)

VI_CP10 = vi_challenge(
    "Điểm kiểm tra: nghiệm số kỹ thuật số",
    "**Nghiệm số** (digital root) của số tự nhiên: nếu có một chữ số "
    "thì là chính nó; ngược lại là nghiệm số của tổng các chữ số. Cài "
    "đặt `process(int n)` bằng đệ quy (helper không dùng vòng lặp được "
    "phép dùng cho tổng chữ số).\n\nVí dụ: 9875 → 9+8+7+5=29 → 2+9=11 "
    "→ 1+1=2, vậy `2`.",
    [("digital root", "Tính tổng chữ số trước (n % 10 + đệ quy n / 10), rồi đệ quy trên chính process cho tới khi n < 10.")],
)

write_practice(
    M, "apx-p10-recursion", "Recursion gauntlet",
    "Five recursive problems from tracing to synthesis; bases first, progress always.",
    "Võ đài đệ quy",
    "Năm bài đệ quy từ truy vết đến tổng hợp; cơ sở trước, tiến triển luôn luôn.",
    after_lesson="apx-m10-strings", minutes=60, difficulty="advanced",
    challenges=[P_MYSTERY, P_WAYS, P_REV, P_GCD, P_SUBSET],
    vi_challenges={
        "apx-m10-mystery": vi_challenge(
            "Truy vết máy tính chẵn lẻ",
            "Truy vết **trên giấy**, rồi trả về giá trị:\n\n```java\n"
            "public static int mystery(int n) {\n    if (n <= 0) { return 0; }\n"
            "    if (n % 2 == 0) { return mystery(n - 1) + 2; }\n"
            "    return mystery(n - 1) * 2;\n}\n```\n\nCài đặt `process(int n)` "
            "để trả `mystery(n)` với đầu vào n = 5.",
            [("parity chain", "Trải: 0 → *2=0 → +2=2 → *2=4 → +2=6 → *2=12; mystery(6) thêm một lần +2.")],
        ),
        "apx-m10-stairs": vi_challenge(
            "Đếm cách leo cầu thang",
            "Bạn leo cầu thang `n` bậc, mỗi lần **1 hoặc 2 bậc**. Viết phương "
            "thức đệ quy đếm số cách khác nhau để chạm đúng đỉnh: "
            "`process(int n)` với cơ sở `ways(0) = 1` và `ways(1) = 1` (đáp án "
            "có hình dạng Fibonacci).\n\nVí dụ: n = 5 → 8.",
            [("stairway ways", "ways(n) = ways(n-1) + ways(n-2); hai trường hợp cơ sở mang theo bộ đếm.")],
        ),
        "apx-m10-reverse": vi_challenge(
            "Đảo ngược đệ quy",
            "Đảo ngược chuỗi **bằng đệ quy**: `process(String s)` trả s đã "
            "đảo, với trường hợp cơ sở độ dài ≤ 1 và không được dùng vòng "
            "lặp.\n\nVí dụ: \"abcd\" → \"dcba\".",
            [("reversed string", "rev(s) = rev(s.substring(1)) + s.charAt(0); thứ tự nối là tất cả.")],
        ),
        "apx-m10-subsetsum": vi_challenge(
            "Tổng tập con",
            "Viết `hasSum(int[] arr, int target)` trả true nếu **một tập con "
            "nào đó** của các giá trị có tổng đúng bằng target (mỗi giá trị "
            "dùng tối đa một lần). Dùng đệ quy theo chỉ số: tại mỗi phần tử, "
            "hoặc chọn nó (target - giá trị) hoặc bỏ qua. Tập rỗng có tổng 0, "
            "nên target 0 luôn đúng.\n\nVí dụ: `{2,7,9}`, target 11 → true "
            "(2+9); target 5 → false.",
            [("subset exists", "Tại chỉ số i: thử chọn (target - arr[i]) hoặc bỏ; cơ sở i == độ dài nghĩa là target == 0.")],
        ),
        "apx-m10-gcd": vi_challenge(
            "Thuật toán Euclid",
            "Cài đặt `gcd(int a, int b)` bằng đệ quy: cơ sở `b == 0` trả a; "
            "ngược lại `gcd(b, a % b)`. Giả định đầu vào không âm.\n\nVí dụ: "
            "gcd(48, 18) → 6; gcd(7, 13) → 1.",
            [("euclid recursion", "Một dòng đệ quy; trường hợp cơ sở mang theo đáp án.")],
        ),
    },
    solutions=[
        ("apx-m10-mystery", r"""public class Solution {
    public static int process(int n) {
        if (n <= 0) {
            return 0;
        }
        if (n % 2 == 0) {
            return process(n - 1) + 2;
        }
        return process(n - 1) * 2;
    }
}
""", r"""public class Solution {
    // BUG: both branches add — traced *2 as +2
    public static int process(int n) {
        if (n <= 0) {
            return 0;
        }
        return process(n - 1) + 2;
    }
}
"""),
        ("apx-m10-stairs", r"""public class Solution {
    public static int process(int n) {
        if (n <= 1) {
            return 1;
        }
        return process(n - 1) + process(n - 2);
    }
}
""", r"""public class Solution {
    // BUG: base case returns 0 for n == 0 — shifts the whole sequence
    public static int process(int n) {
        if (n == 1) {
            return 1;
        }
        if (n == 0) {
            return 0;
        }
        return process(n - 1) + process(n - 2);
    }
}
"""),
        ("apx-m10-reverse", r"""public class Solution {
    public static String process(String s) {
        if (s.length() <= 1) {
            return s;
        }
        return process(s.substring(1)) + s.charAt(0);
    }
}
""", r"""public class Solution {
    // BUG: append order swapped — returns the input unchanged
    public static String process(String s) {
        if (s.length() <= 1) {
            return s;
        }
        return s.charAt(0) + process(s.substring(1));
    }
}
"""),
        ("apx-m10-subsetsum", r"""public class Solution {
    public static boolean hasSum(int[] arr, int target) {
        return tryFrom(arr, 0, target);
    }

    private static boolean tryFrom(int[] arr, int i, int target) {
        if (i == arr.length) {
            return target == 0;
        }
        return tryFrom(arr, i + 1, target - arr[i]) || tryFrom(arr, i + 1, target);
    }
}
""", r"""public class Solution {
    public static boolean hasSum(int[] arr, int target) {
        return tryFrom(arr, 0, target);
    }

    private static boolean tryFrom(int[] arr, int i, int target) {
        if (i == arr.length) {
            return target == 0;
        }
        // BUG: only the include branch — skips valid excluded sums
        return tryFrom(arr, i + 1, target - arr[i]);
    }
}
"""),
        ("apx-m10-gcd", r"""public class Solution {
    public static int gcd(int a, int b) {
        if (b == 0) {
            return a;
        }
        return gcd(b, a % b);
    }
}
""", r"""public class Solution {
    // BUG: swapped arguments in the recursion — gcd(b % a, b) can loop
    public static int gcd(int a, int b) {
        if (b == 0) {
            return a;
        }
        return gcd(b % a, b);
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m10", "Checkpoint: digital root",
    "Two recursive layers: digit sum inside, self-recursion outside.",
    20,
    r"""
The digital root is recursion composed with recursion: an inner
helper consumes digits while an outer process consumes the results.
Both base cases are visible in the example trace — find them before
writing anything.
""",
    "Điểm kiểm tra: nghiệm số kỹ thuật số",
    "Hai tầng đệ quy: tổng chữ số bên trong, tự đệ quy bên ngoài.",
    r"""
Nghiệm số là đệ quy ghép với đệ quy: một helper bên trong tiêu thụ
chữ số trong khi process bên ngoài tiêu thụ kết quả. Cả hai trường
hợp cơ sở đều hiện trong ví dụ truy vết — tìm ra chúng trước khi viết
gì đó.
""",
    CP10,
    VI_CP10,
    solution=r"""public class Solution {
    public static int process(int n) {
        if (n < 10) {
            return n;
        }
        return process(digitSum(n));
    }

    private static int digitSum(int n) {
        if (n == 0) {
            return 0;
        }
        return n % 10 + digitSum(n / 10);
    }
}
""",
    wrong=r"""public class Solution {
    public static int process(int n) {
        if (n < 10) {
            return n;
        }
        // BUG: one digit-sum pass only — never recurses on the result
        return digitSum(n);
    }

    private static int digitSum(int n) {
        if (n == 0) {
            return 0;
        }
        return n % 10 + digitSum(n / 10);
    }
}
""",
)

print("M10 done")
