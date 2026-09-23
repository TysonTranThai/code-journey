#!/usr/bin/env python3
"""AP CSA M14 — Recursion: base case, progress, call-stack traces."""
from apc import *

M = "apc-recursion"

L1 = r"""
A **recursive** method calls itself on a smaller input. Two ingredients are
mandatory:

1. **Base case** — an input answered directly, no call.
2. **Recursive case** — the call moves *toward* the base case (progress).

```java
public static int factorial(int n) {
    if (n <= 1) {            // base case
        return 1;
    }
    return n * factorial(n - 1);   // progress: n shrinks by 1
}
```

The **call stack** makes traces mechanical. For `factorial(4)`:

```text
factorial(4) = 4 * factorial(3)
                 factorial(3) = 3 * factorial(2)
                                 factorial(2) = 2 * factorial(1)
                                                 factorial(1) = 1
```

Unwind: 1 → 2 → 6 → 24. Write the descent, hit the base, multiply back up.

**Exam trace conventions**: count *calls* (factorial(4) makes 4 total), and
remember StackOverflowError is the runtime signature of missing progress —
an infinite loop's recursive twin.
"""

L2 = r"""
Two shapes cover nearly all AP recursion:

**String recursion** — index-based, often from both ends:

```java
public static boolean isPalindrome(String s, int lo, int hi) {
    if (lo >= hi) {
        return true;              // met in the middle (or empty)
    }
    if (s.charAt(lo) != s.charAt(hi)) {
        return false;
    }
    return isPalindrome(s, lo + 1, hi - 1);
}
```

**Array recursion** — recurse on the index, treat the rest of the array as
"the smaller input":

```java
public static int sum(int[] arr, int i) {
    if (i == arr.length) {
        return 0;                 // base: past the end adds nothing
    }
    return arr[i] + sum(arr, i + 1);
}
```

`sum(arr, 0)` walks 0, 1, 2, ... — progress is `i + 1`. The base case is
`i == arr.length`, *not* `length - 1`: the empty contribution is real, and
getting it wrong by one is the classic off-by-one.

Decomposability mindset: a problem is recursive when a piece of the answer
plus *the same problem, smaller* gives the whole — first character of the
string + the palindrome-ness of the rest.
"""

L3 = r"""
The "what does this print" genre, decoded:

```java
public static void puzzle(int n) {
    if (n <= 0) {
        return;
    }
    System.out.print(n + " ");
    puzzle(n - 2);
    System.out.print(n + " ");
}
```

`puzzle(5)` prints `5 3 1 3 5` — before the call for the descent, after it
for the unwind. Number of prints: 2 per call that survives the base check
(3 calls → 6 prints).

Mental rules:

- **Code before the recursive call** runs top-down (descent order).
- **Code after the recursive call** runs bottom-up (unwind order).
- **Total calls** = every invocation including base-case hits.
- **Missing base case** or a branch that can't reach it → StackOverflowError,
  never "runs forever" visibly.

Also know: recursion can always be replaced by a loop, but the exam wants
you to read *their* recursion, not rewrite it.
"""

write_module(
    M,
    "Recursion",
    "Base cases, progress, call-stack traces, string and array recursion shapes.",
    "Đệ quy",
    "Trường hợp cơ sở, tiến triển, truy vết stos gọi, các dạng đệ quy trên chuỗi và mảng.",
    lessons=["apc-m14-basics", "apc-m14-shapes", "apc-m14-traces", "apc-cp-m14"],
    practices=["apc-p14-recursion"],
)

write_lesson(
    M, "apc-m14-basics", "Recursion mechanics",
    "Base case, progress, the call stack, counting calls.",
    14, L1,
    "Cơ chế đệ quy",
    "Trường hợp cơ sở, tiến triển, stos gọi, đếm số lần gọi.",
    r"""
Một phương thức **đệ quy** tự gọi nó trên đầu vào nhỏ hơn. Hai thành phần là
bắt buộc:

1. **Trường hợp cơ sở** — đầu vào được trả lời trực tiếp, không gọi.
2. **Trường hợp đệ quy** — lời gọi tiến *về phía* trường hợp cơ sở (tiến
   triển).

```java
public static int factorial(int n) {
    if (n <= 1) {            // trường hợp cơ sở
        return 1;
    }
    return n * factorial(n - 1);   // tiến triển: n giảm 1
}
```

**Stos gọi** giúp truy vết thành cơ học. Với `factorial(4)`:

```text
factorial(4) = 4 * factorial(3)
                 factorial(3) = 3 * factorial(2)
                                 factorial(2) = 2 * factorial(1)
                                                 factorial(1) = 1
```

Đảo ngược: 1 → 2 → 6 → 24. Viết phần đi xuống, chạm cơ sở, nhân ngược lên.

**Quy ước truy vết của đề thi**: đếm *số lần gọi* (factorial(4) tạo tổng
cộng 4 lần gọi), và nhớ StackOverflowError là chữ ký thời gian chạy của việc
thiếu tiến triển — bản sinh đôi đệ quy của vòng lặp vô hạn.
""",
)

write_lesson(
    M, "apc-m14-shapes", "String and array recursion",
    "Two-pointers strings, index-based arrays, the empty-contribution base case.",
    14, L2,
    "Đệ quy trên chuỗi và mảng",
    "Chuỗi hai con trỏ, mảng theo chỉ số, trường hợp cơ sở của đóng góp rỗng.",
    r"""
Hai dạng phủ gần hết đệ quy trong đề thi:

**Đệ quy chuỗi** — theo chỉ số, thường từ hai đầu:

```java
public static boolean isPalindrome(String s, int lo, int hi) {
    if (lo >= hi) {
        return true;              // chạm nhau ở giữa (hoặc rỗng)
    }
    if (s.charAt(lo) != s.charAt(hi)) {
        return false;
    }
    return isPalindrome(s, lo + 1, hi - 1);
}
```

**Đệ quy mảng** — đệ quy theo chỉ số, coi phần còn lại của mảng là "đầu vào
nhỏ hơn":

```java
public static int sum(int[] arr, int i) {
    if (i == arr.length) {
        return 0;                 // cơ sở: quá cuối cộng thêm không gì
    }
    return arr[i] + sum(arr, i + 1);
}
```

`sum(arr, 0)` đi qua 0, 1, 2, ... — tiến triển là `i + 1`. Trường hợp cơ sở
là `i == arr.length`, *không phải* `length - 1`: đóng góp rỗng là có thật,
và lệch một ở đây là lỗi off-by-one kinh điển.

Tư duy phân rã: một bài toán là đệ quy khi một mẩu của đáp án cộng với
*cùng bài toán, nhỏ hơn* cho ra toàn bộ — ký tự đầu của chuỗi cộng với tính
palindrome của phần còn lại.
""",
)

write_lesson(
    M, "apc-m14-traces", "Reading their recursion",
    "Print-before/print-after, counting calls, overflow signatures.",
    10, L3,
    "Đọc đệ quy của người khác",
    "In-trước/in-sau, đếm số lần gọi, dấu hiệu tràn stos.",
    r"""
Thể loại "cái này in ra gì", giải mã:

```java
public static void puzzle(int n) {
    if (n <= 0) {
        return;
    }
    System.out.print(n + " ");
    puzzle(n - 2);
    System.out.print(n + " ");
}
```

`puzzle(5)` in `5 3 1 3 5` — trước lời gọi là phần đi xuống, sau lời gọi là
phần đi lên. Số lượt in: 2 cho mỗi lần gọi sống sót qua phép kiểm tra cơ sở
(3 lần gọi → 6 lượt in).

Các luật tư duy:

- **Mã trước lời gọi đệ quy** chạy từ trên xuống (thứ tự đi xuống).
- **Mã sau lời gọi đệ quy** chạy từ dưới lên (thứ tự đi lên).
- **Tổng số lần gọi** = mọi lần gọi, kể cả khi chạm trường hợp cơ sở.
- **Thiếu trường hợp cơ sở** hoặc nhánh không thể chạm tới nó →
  StackOverflowError, không bao giờ "chạy mãi" nhìn thấy được.

Cũng cần biết: đệ quy luôn thay được bằng vòng lặp, nhưng đề thi muốn bạn
*đọc* đệ quy của họ, không phải viết lại.
""",
)

BOILER_FACT = r"""public class Solution {
    public static int fact(int n) {
        return 0; // replace: recursive factorial, n >= 0 (0! = 1)
    }
}
"""

BOILER_PALI = r"""public class Solution {
    public static boolean isPal(String s, int lo, int hi) {
        return false; // replace: recursive palindrome check on s[lo..hi]
    }
}
"""

BOILER_DSUM = r"""public class Solution {
    public static int dsum(int n) {
        return 0; // replace: recursive digit sum, n >= 0
    }
}
"""

BOILER_ASUM = r"""public class Solution {
    public static int asum(int[] arr, int i) {
        return 0; // replace: recursive sum of arr[i..]
    }
}
"""

BOILER_PUZZLE = r"""public class Solution {
    public static String puzzle(int n) {
        // Should print n n-2 n-4 ... down to >= 1 and back up, space
        // separated, using recursion with code before AND after the call.
        // Current version only descends — the unwind half is missing.
        if (n <= 0) {
            return "";
        }
        return n + " " + puzzle(n - 2);
    }
}
"""

CP14 = r"""public class Solution {
    public static int countChar(String s, char c, int i) {
        // replace: recursive count of occurrences of c in s from index i on
        return 0;
    }
}
"""

P_FACT = challenge(
    "apc-m14-factorial",
    "Recursive factorial",
    "Implement `int fact(int n)` recursively: 0! and 1! are 1; otherwise n * fact(n - 1).",
    BOILER_FACT,
    [(
        "factorial ladder",
        r"""
CjTestBase.checkEq(Solution.fact(0), 1, "0! by definition");
CjTestBase.checkEq(Solution.fact(1), 1, "1!");
CjTestBase.checkEq(Solution.fact(5), 120, "5!");
CjTestBase.checkEq(Solution.fact(9), 362880, "9!");
""",
        "Base case n <= 1 returns 1; progress is n - 1.",
    )],
    level="imitation",
)

P_PALI = challenge(
    "apc-m14-palindrome",
    "Recursive palindrome",
    "Implement `boolean isPal(String s, int lo, int hi)` recursively: true when s[lo..hi] reads the same both ways. Base case lo >= hi is true; mismatched ends are false; otherwise recurse inward.",
    BOILER_PALI,
    [(
        "two-pointer recursion",
        r"""
CjTestBase.checkEq(Solution.isPal("racecar", 0, 6), true, "odd length");
CjTestBase.checkEq(Solution.isPal("noon", 0, 3), true, "even length");
CjTestBase.checkEq(Solution.isPal("reno", 0, 3), false, "not one");
CjTestBase.checkEq(Solution.isPal("a", 0, 0), true, "single char");
CjTestBase.checkEq(Solution.isPal("", 0, -1), true, "empty range");
""",
        "lo >= hi (crossed or met) is the true base case.",
    )],
    level="guided",
)

P_DSUM = challenge(
    "apc-m14-digitsum",
    "Recursive digit sum",
    "Implement `int dsum(int n)` recursively: sum of n's decimal digits. 0 → 0; otherwise the last digit (n % 10) plus dsum of the rest (n / 10).",
    BOILER_DSUM,
    [(
        "digit decomposition",
        r"""
CjTestBase.checkEq(Solution.dsum(0), 0, "zero");
CjTestBase.checkEq(Solution.dsum(7), 7, "single digit");
CjTestBase.checkEq(Solution.dsum(1234), 10, "1+2+3+4");
CjTestBase.checkEq(Solution.dsum(90009), 18, "zeros inside");
""",
        "n % 10 is the last digit; n / 10 is the smaller problem.",
    )],
    level="independent",
)

P_ASUM = challenge(
    "apc-m14-arraysum",
    "Recursive array sum",
    "Implement `int asum(int[] arr, int i)` recursively: the sum of arr[i..]. Base case i == arr.length returns 0 (the empty contribution), otherwise arr[i] + asum(arr, i + 1).",
    BOILER_ASUM,
    [(
        "index recursion",
        r"""
int[] a = {3, 1, 4, 1, 5};
CjTestBase.checkEq(Solution.asum(a, 0), 14, "whole array");
CjTestBase.checkEq(Solution.asum(a, 2), 10, "tail from 2");
CjTestBase.checkEq(Solution.asum(a, 4), 5, "single element");
CjTestBase.checkEq(Solution.asum(a, 5), 0, "past the end: empty");
CjTestBase.checkEq(Solution.asum(new int[]{}, 0), 0, "empty array");
""",
        "The i == arr.length base is what makes the empty array work.",
    )],
    level="independent",
)

P_PUZZLE = challenge(
    "apc-m14-fix-puzzle",
    "Debug the recursive echo",
    "`puzzle(n)` should build `\"5 3 1 1 3 5\"`-style strings: descend printing n, n−2, ..., then unwind printing them all again. The current version only descends — the after-the-call half is missing. Fix it (must stay recursive with code on both sides of the call).",
    BOILER_PUZZLE,
    [(
        "echo repaired",
        r"""
CjTestBase.checkEq(Solution.puzzle(5), "5 3 1 1 3 5", "odd descent");
CjTestBase.checkEq(Solution.puzzle(4), "4 2 2 4", "even descent");
CjTestBase.checkEq(Solution.puzzle(0), "", "base case");
""",
        "Capture the descent result, then append n again after the call.",
    )],
    level="debugging",
)

CP14C = challenge(
    "apc-cp-m14-countchar",
    "Checkpoint: recursive count",
    "Implement `int countChar(String s, char c, int i)` recursively: occurrences of c in s from index i onward. Empty remainder → 0; s.charAt(i) == c adds 1.",
    CP14,
    [(
        "counted recursion",
        r"""
CjTestBase.checkEq(Solution.countChar("banana", 'a', 0), 3, "all the a's");
CjTestBase.checkEq(Solution.countChar("banana", 'a', 1), 3, "from index 1");
CjTestBase.checkEq(Solution.countChar("banana", 'a', 4), 1, "tail only");
CjTestBase.checkEq(Solution.countChar("banana", 'x', 0), 0, "absent");
CjTestBase.checkEq(Solution.countChar("", 'a', 0), 0, "empty string");
""",
        "(i == s.length()) ? 0 : (s.charAt(i) == c ? 1 : 0) + countChar(s, c, i + 1).",
    )],
    level="independent",
)

write_practice(
    M, "apc-p14-recursion", "Recursion reps", "Ladders, palindromes, digit/index recursion, trace debugging.",
    "Luyện đệ quy", "Thang đệ quy, palindrome, đệ quy chữ số/chỉ số, gỡ lỗi truy vết.",
    after_lesson="apc-m14-traces", minutes=55, difficulty="beginner",
    challenges=[P_FACT, P_PALI, P_DSUM, P_ASUM, P_PUZZLE],
    vi_challenges={
        "apc-m14-factorial": vi_challenge("Giai thừa đệ quy", "Cài đặt `int fact(int n)` theo đệ quy: 0! và 1! bằng 1; nếu không thì n * fact(n - 1).",
            [("factorial ladder", "Trường hợp cơ sở n <= 1 trả về 1; tiến triển là n - 1.")]),
        "apc-m14-palindrome": vi_challenge("Palindrome đệ quy", "Cài đặt `boolean isPal(String s, int lo, int hi)` theo đệ quy: true khi s[lo..hi] đọc xuôi ngược như nhau. Trường hợp cơ sở lo >= hi là true; hai đầu lệch là false; nếu không thì đệ quy vào trong.",
            [("two-pointer recursion", "lo >= hi (chạm hoặc vượt nhau) là trường hợp cơ sở true.")]),
        "apc-m14-digitsum": vi_challenge("Tổng chữ số đệ quy", "Cài đặt `int dsum(int n)` theo đệ quy: tổng các chữ số thập phân của n. 0 → 0; nếu không thì chữ số cuối (n % 10) cộng dsum của phần còn lại (n / 10).",
            [("digit decomposition", "n % 10 là chữ số cuối; n / 10 là bài toán nhỏ hơn.")]),
        "apc-m14-arraysum": vi_challenge("Tổng mảng đệ quy", "Cài đặt `int asum(int[] arr, int i)` theo đệ quy: tổng của arr[i..]. Trường hợp cơ sở i == arr.length trả về 0 (đóng góp rỗng), nếu không thì arr[i] + asum(arr, i + 1).",
            [("index recursion", "Trường hợp cơ sở i == arr.length là điều làm mảng rỗng chạy đúng.")]),
        "apc-m14-fix-puzzle": vi_challenge("Gỡ lỗi tiếng vọng đệ quy", "`puzzle(n)` nên dựng chuỗi kiểu `\"5 3 1 1 3 5\"`: đi xuống in n, n−2, ..., rồi đi lên in lại. Bản hiện tại chỉ đi xuống — thiếu nửa sau-lời-gọi. Sửa nó (phải vẫn đệ quy với mã ở cả hai bên lời gọi).",
            [("echo repaired", "Lưu kết quả đi xuống, rồi nối n thêm lần nữa sau lời gọi.")]),
    },
    solutions=[
        ("apc-m14-factorial", r"""public class Solution {
    public static int fact(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * fact(n - 1);
    }
}
""",
         r"""public class Solution {
    public static int fact(int n) {
        // BUG: no progress on n == 0 branch? no — base case is wrong:
        // returns 0, poisoning every product
        if (n == 0) {
            return 0;
        }
        return n * fact(n - 1);
    }
}
""".replace("// BUG: no progress on n == 0 branch? no — base case is wrong:\n        ", "")),
        ("apc-m14-palindrome", r"""public class Solution {
    public static boolean isPal(String s, int lo, int hi) {
        if (lo >= hi) {
            return true;
        }
        if (s.charAt(lo) != s.charAt(hi)) {
            return false;
        }
        return isPal(s, lo + 1, hi - 1);
    }
}
""",
         r"""public class Solution {
    public static boolean isPal(String s, int lo, int hi) {
        // BUG: base case never true for empty/1-char — comparison on
        // charAt(hi) runs past the string
        if (lo == hi - 1) {
            return true;
        }
        if (s.charAt(lo) != s.charAt(hi)) {
            return false;
        }
        return isPal(s, lo + 1, hi - 1);
    }
}
"""),
        ("apc-m14-digitsum", r"""public class Solution {
    public static int dsum(int n) {
        if (n == 0) {
            return 0;
        }
        return (n % 10) + dsum(n / 10);
    }
}
""",
         r"""public class Solution {
    public static int dsum(int n) {
        // BUG: recurses on n (unchanged) — infinite recursion
        if (n == 0) {
            return 0;
        }
        return (n % 10) + dsum(n);
    }
}
"""),
        ("apc-m14-arraysum", r"""public class Solution {
    public static int asum(int[] arr, int i) {
        if (i == arr.length) {
            return 0;
        }
        return arr[i] + asum(arr, i + 1);
    }
}
""",
         r"""public class Solution {
    public static int asum(int[] arr, int i) {
        // BUG: base case one short — arr[length-1] is skipped
        if (i == arr.length - 1) {
            return 0;
        }
        return arr[i] + asum(arr, i + 1);
    }
}
"""),
        ("apc-m14-fix-puzzle", r"""public class Solution {
    public static String puzzle(int n) {
        if (n <= 0) {
            return "";
        }
        String rest = puzzle(n - 2);
        return n + " " + rest + (rest.isEmpty() ? "" : " ") + n;
    }
}
""",
         r"""public class Solution {
    public static String puzzle(int n) {
        // BUG: original flaw kept — only the descent, no unwind echo
        if (n <= 0) {
            return "";
        }
        return n + " " + puzzle(n - 2);
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m14", "Checkpoint: recursive count",
    "Index-based string recursion with a counting accumulator in the return.",
    25,
    r"""
This checkpoint's pattern — recurse on the index, add 1 conditionally in
the return expression — is the exact shape of several released exam
recursion items. Get the empty-remainder base case right and the rest is
arithmetic.
""",
    "Điểm kiểm tra: đếm đệ quy",
    "Đệ quy trên chỉ số với bộ tích lũy đếm nằm trong biểu thức trả về.",
    r"""
Mẫu hình của điểm kiểm tra này — đệ quy theo chỉ số, cộng 1 có điều kiện
trong biểu thức trả về — là đúng dạng của vài câu đệ quy trong đề thi thật.
Làm đúng trường hợp cơ sở phần-còn-lại-rỗng, phần còn lại chỉ là số học.
""",
    CP14C,
    vi_challenge("Điểm kiểm tra: đếm đệ quy", "Cài đặt `int countChar(String s, char c, int i)` theo đệ quy: số lần xuất hiện của c trong s tính từ chỉ số i. Phần còn lại rỗng → 0; s.charAt(i) == c cộng thêm 1.",
        [("counted recursion", "(i == s.length()) ? 0 : (s.charAt(i) == c ? 1 : 0) + countChar(s, c, i + 1).")]),
    solution=r"""public class Solution {
    public static int countChar(String s, char c, int i) {
        if (i == s.length()) {
            return 0;
        }
        int hit = (s.charAt(i) == c) ? 1 : 0;
        return hit + countChar(s, c, i + 1);
    }
}
""",
    wrong=r"""public class Solution {
    public static int countChar(String s, char c, int i) {
        // BUG: recurses past the string — no empty-remainder base case
        if (s.charAt(i) == c) {
            return 1 + countChar(s, c, i + 1);
        }
        return countChar(s, c, i + 1);
    }
}
""",
)
