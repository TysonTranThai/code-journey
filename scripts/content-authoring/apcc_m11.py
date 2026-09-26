#!/usr/bin/env python3
"""AP CSA Core M11 — Recursion & Recursive Reasoning (AP depth)."""
from apcc import *

M = "cx-recursion"

L1 = r"""
Foundations taught recursion's shape; the exam grades its **edge
discipline**. Every recursive method is two contracts:

1. **Base case** — the smallest input, answered directly, with NO
   recursive call. For arrays/strings it is usually the *empty* or
   *single-element* input.
2. **Recursive case** — reduce toward the base case, combine, return.
   The reduction must be *provably smaller*: `n - 1`, `i + 1`,
   `substring(1)`.

The two failure signatures (both exam favorites):

- **Wrong base value**: `fact(0) = 1` by definition; returning 0 there
  multiplies everything to 0. One wrong seed poisons the whole tree —
  the code looks right and every non-trivial test fails.
- **Missing base case** (or an unreachable one): infinite recursion →
  `StackOverflowError`. On a trace question, count frames: if n never
  reaches the base value, the method never returns.

The decision rule: when the base case runs, the answer must be
constructible with **zero** additional information. If your base case
still needs to call something, it is not a base case.
"""

L2 = r"""
Tracing recursion is frame discipline. For:

```java
public static int f(int n) {
    if (n <= 0) { return 1; }
    return n + f(n - 2);
}
```

| frame | call  | computes        | returns |
| ----- | ----- | --------------- | ------- |
| 1     | f(5)  | 5 + f(3)        | 5 + 6   |
| 2     | f(3)  | 3 + f(1)        | 3 + 3   |
| 3     | f(1)  | 1 + f(-1)       | 1 + 1   |
| 4     | f(-1) | base            | 1       |

Unwinding: f(1)=2, f(3)=6, f(5)=11... wait — f(5) = 5 + f(3) = 5 + 6 =
11? Recheck: f(3) = 3 + f(1) = 3 + 2 = 5, not 6. f(5) = 5 + 5 = 10.
**This is exactly why you write the table** — mental arithmetic lies;
the table doesn't.

Two exam-standard counts:

- **Call count**: how many times is f invoked? One per frame: 4 frames
  above → 4 calls (including the base-case frame).
- **Print order**: statements BEFORE the recursive call run on the way
  down; statements AFTER run on the way up. `print(n); f(n-2);
  print(n);` prints 5 3 1 1 3 5 — down-sequence then mirrored
  up-sequence.

The up/down asymmetry is the whole trick: code after the call executes
in reverse order of the calls, because frames unwind in stack order.
"""

L3 = r"""
Two-branch recursion is where AP questions top out:

```java
public static int ways(int n) {
    if (n == 0) { return 1; }   // one way to stand still
    if (n < 0) { return 0; }    // overshot: no way
    return ways(n - 1) + ways(n - 2);
}
```

Reading it as a decision tree: at each staircase you take 1 or 2 steps.
`ways(3)`: ways(2) + ways(1) = 2 + 1 = 3. The tree fans out — every
internal node spawns two children until a base case. The MCQ question
is almost always **how many total calls**: count the nodes.

| call tree for ways(3) |
| --------------------- |
| ways(3) → ways(2), ways(1) |
| ways(2) → ways(1), ways(0) |
| ways(1) → ways(0), ways(-1) |
| ways(0) base (×3), ways(-1) base (×1) |

Calls: ways(3), ways(2), ways(1), ways(0) ×3, ways(-1) = 7 total.

The second classic: **recursive search** — "does target appear in
arr[i..]?"

```java
public static boolean has(int[] arr, int i, int target) {
    if (i >= arr.length) { return false; }   // ran off: absent
    if (arr[i] == target) { return true; }   // found
    return has(arr, i + 1, target);
}
```

Three exits: exhausted (false), found (true), recurse. The ORDER of
the first two checks matters — swap them and you read a dead index.
This shape (advance the index, answer at the ends) is the template for
every "recursive array scan" the exam writes.
"""

write_module(
    M,
    "Recursion & Recursive Reasoning",
    "Base-case design, frame-by-frame stack tracing with call counts, and two-branch decision trees.",
    "Đệ quy & suy luận đệ quy",
    "Thiết kế trường-hợp-cơ-sở, truy vết ngăn-xếp từng-khung với số lần gọi, và cây quyết định hai nhánh.",
    lessons=["cx-m11-edges", "cx-m11-frames", "cx-m11-branching", "cx-cp-m11"],
    practices=["cx-p11-recursion"],
)

write_lesson(
    M, "cx-m11-edges", "Edge discipline",
    "Base cases that answer with zero information; the two failure signatures.",
    12, L1,
    "Kỷ luật biên",
    "Trường hợp cơ sở trả lời bằng không thông tin bổ sung; hai chữ ký thất bại.",
    r"""
Nền tảng đã dạy hình dạng của đệ quy; đề thi chấm **kỷ luật biên**. Mỗi
phương thức đệ quy là hai hợp đồng:

1. **Trường hợp cơ sở** — đầu vào nhỏ nhất, trả lời trực tiếp, KHÔNG có
   lời gọi đệ quy. Với mảng/chuỗi, thường là đầu vào *rỗng* hoặc
   *một-phần-tử*.
2. **Trường hợp đệ quy** — thu nhỏ về phía cơ sở, kết hợp, trả về. Phép
   thu nhỏ phải *chứng minh được là nhỏ hơn*: `n - 1`, `i + 1`,
   `substring(1)`.

Hai chữ ký thất bại (đều là mục yêu thích của đề thi):

- **Sai giá trị cơ sở**: `fact(0) = 1` theo định nghĩa; trả về 0 ở đó
  sẽ nhân mọi thứ thành 0. Một hạt giống sai đầu độc cả cây — mã trông
  đúng và mọi bài kiểm tra không-tầm-thường đều trượt.
- **Thiếu trường hợp cơ sở** (hoặc không thể chạm tới): đệ quy vô hạn →
  `StackOverflowError`. Với câu truy vết, hãy đếm khung: nếu n không bao
  giờ chạm giá trị cơ sở, phương thức không bao giờ trả về.

Luật quyết định: khi trường hợp cơ sở chạy, đáp án phải dựng được với
**không** thông tin bổ sung. Nếu trường hợp cơ sở của bạn vẫn cần gọi
thứ gì đó, nó không phải trường hợp cơ sở.
""",
)

write_lesson(
    M, "cx-m11-frames", "Frames and counts",
    "The frame table, call counting, and the print-order asymmetry.",
    12, L2,
    "Khung và số đếm",
    "Bảng khung, đếm số lần gọi, và tính bất đối xứng của thứ tự in.",
    r"""
Truy vết đệ quy là kỷ luật khung. Với:

```java
public static int f(int n) {
    if (n <= 0) { return 1; }
    return n + f(n - 2);
}
```

| khung | lời gọi | tính            | trả về  |
| ----- | ------- | --------------- | ------- |
| 1     | f(5)    | 5 + f(3)        | 5 + 5   |
| 2     | f(3)    | 3 + f(1)        | 3 + 2   |
| 3     | f(1)    | 1 + f(-1)       | 1 + 1   |
| 4     | f(-1)   | cơ sở           | 1       |

Độ cao hồiquy: f(1)=2, f(3)=5, f(5)=10. **Đây chính là lý do phải viết
bảng** — phép tính trong đầu hay nói dối; bảng thì không.

Hai phép đếm chuẩn của đề thi:

- **Số lần gọi**: f được triệu hồi bao nhiêu lần? Mỗi khung một lần: 4
  khung trên → 4 lần gọi (kể cả khung trường-hợp-cơ-sở).
- **Thứ tự in**: câu lệnh TRƯỚC lời gọi đệ quy chạy trên đường đi xuống;
  câu lệnh SAU chạy trên đường đi lên. `print(n); f(n-2); print(n);`
  in 5 3 1 1 3 5 — dãy đi xuống rồi dãy đối xứng đi lên.

Tính bất đối xứng lên/xuống là toàn bộ cái mánh: mã sau lời gọi thực
thi theo thứ tự NGƯỢC của các lời gọi, vì các khung dỡ xuống theo thứ tự
ngăn xếp.
""",
)

write_lesson(
    M, "cx-m11-branching", "Branching trees",
    "Two-branch recursion as a decision tree; total-call counting; recursive search.",
    12, L3,
    "Cây phân nhánh",
    "Đệ quy hai nhánh như một cây quyết định; đếm tổng số lần gọi; tìm kiếm đệ quy.",
    r"""
Đệ quy hai nhánh là đỉnh của các câu hỏi AP:

```java
public static int ways(int n) {
    if (n == 0) { return 1; }   // một cách đứng yên
    if (n < 0) { return 0; }    // vọt lách: không cách nào
    return ways(n - 1) + ways(n - 2);
}
```

Đọc như một cây quyết định: tại mỗi bậc thang bạn bước 1 hoặc 2 bước.
`ways(3)`: ways(2) + ways(1) = 2 + 1 = 3. Cây tỏa ra — mỗi nút trong
sinh hai con cho tới trường hợp cơ sở. Câu MCQ gần như luôn là **tổng
số lần gọi**: đếm các nút.

| cây gọi cho ways(3) |
| ------------------- |
| ways(3) → ways(2), ways(1) |
| ways(2) → ways(1), ways(0) |
| ways(1) → ways(0), ways(-1) |
| ways(0) cơ sở (×3), ways(-1) cơ sở (×1) |

Số lần gọi: ways(3), ways(2), ways(1), ways(0) ×3, ways(-1) = 7 lần.

Kinh điển thứ hai: **tìm kiếm đệ quy** — "target có xuất hiện trong
arr[i..]?"

```java
public static boolean has(int[] arr, int i, int target) {
    if (i >= arr.length) { return false; }   // hết đường: vắng mặt
    if (arr[i] == target) { return true; }   // thấy rồi
    return has(arr, i + 1, target);
}
```

Ba lối ra: cạn kiệt (false), tìm thấy (true), đệ quy tiếp. THỨ TỰ của
hai phép kiểm tra đầu quan trọng — hoán đổi cho nhau và bạn đọc một chỉ
số đã chết. Hình dạng này (tiến chỉ số, trả lời ở hai đầu) là bản mẫu
cho mọi "quét mảng đệ quy" mà đề thi viết ra.
""",
)

BOILER_DIGIT = r"""public class Solution {
    // CONTRACT: count the digits of n (n >= 0). 0 has 1 digit.
    public static int numDigits(int n) {
        return 0; // replace
    }
}
"""

BOILER_REVP = r"""public class Solution {
    // CONTRACT: print arr from the END to the START, one per line,
    // recursively. (Capture-based test.)
    public static void printRev(int[] arr, int i) {
        // replace
    }
}
"""

BOILER_CALLCOUNT = r"""public class Solution {
    // CONTRACT: f is already implemented. g(n) must return the TOTAL
    // number of calls f makes when invoked as f(n), INCLUDING the
    // initial call. f halves n: f(n) = 1 + f(n / 2) for n > 1,
    // base n <= 1. So f(8) makes 4 calls: f(8), f(4), f(2), f(1).
    public static int f(int n) {
        if (n <= 1) { return 1; }
        return 1 + f(n / 2);
    }

    public static int g(int n) {
        return 0; // replace: count of calls f(n) makes (non-recursive loop is fine)
    }
}
"""

BOILER_POWBAD = r"""public class Solution {
    // CONTRACT: 2 to the power n, n >= 0.
    public static int pow2(int n) {
        if (n == 0) {
            return 0;
        }
        return 2 * pow2(n - 1);
    }
}
"""

BOILER_SUBSET = r"""public class Solution {
    // CONTRACT: can some subset of arr[i..] sum exactly to target?
    // Empty subset sums to 0, so target 0 is always true.
    public static boolean subset(int[] arr, int i, int target) {
        return false; // replace
    }
}
"""

P_DIGITS = challenge(
    "cx-m11-digit-count",
    "Recursive digit count",
    "Implement `int numDigits(int n)` recursively (n >= 0): 0 has 1 digit; otherwise 1 + numDigits(n / 10). The base case is n < 10, not n == 0 — think about why both work here.",
    BOILER_DIGIT,
    [(
        "digits counted",
        r"""
CjTestBase.checkEq(Solution.numDigits(0), 1, "zero is one digit");
CjTestBase.checkEq(Solution.numDigits(7), 1, "single digit");
CjTestBase.checkEq(Solution.numDigits(123), 3, "three digits");
CjTestBase.checkEq(Solution.numDigits(1000000), 7, "seven digits");
""",
        "if (n < 10) return 1; return 1 + numDigits(n / 10);",
    )],
    level="imitation",
)

P_REVPRINT = challenge(
    "cx-m11-reverse-print",
    "Recursive reverse print",
    "Implement `void printRev(int[] arr, int i)` to print arr from END to START, one per line, starting from i = 0. The recursive call comes BEFORE the print — code after the call runs on the way up. Empty arrays print nothing.",
    BOILER_REVP,
    [(
        "reversed lines",
        r"""
String out = CjTestBase.capture(() -> Solution.printRev(new int[]{1, 2, 3}, 0));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("3", "2", "1"), "reverse order, one per line");
String empty = CjTestBase.capture(() -> Solution.printRev(new int[]{}, 0));
CjTestBase.checkEq(empty.trim(), "", "empty prints nothing");
""",
        "if (i >= arr.length) return; printRev(arr, i + 1); println(arr[i]);",
    )],
    level="guided",
)

P_CALLCOUNT = challenge(
    "cx-m11-call-counter",
    "Count the calls",
    "Implement `int g(int n)`: the total number of calls f(n) makes (including itself), where f halves n each time. A loop counting halvings is fine — the point is the mental model: calls = frames on the stack at the deepest point.",
    BOILER_CALLCOUNT,
    [(
        "frames counted",
        r"""
CjTestBase.checkEq(Solution.g(1), 1, "just the base frame");
CjTestBase.checkEq(Solution.g(8), 4, "8, 4, 2, 1");
CjTestBase.checkEq(Solution.g(16), 5, "16, 8, 4, 2, 1");
""",
        "int calls = 0; while (n > 1) { calls++; n /= 2; } return calls + 1;",
    )],
    level="combination",
)

P_POWBAD = challenge(
    "cx-m11-fix-pow2",
    "Fix the poisoned base",
    "`pow2(4)` returns 0 — every value multiplies down to the broken base case. Trace pow2(1) and pow2(0) by hand, then repair the base value.",
    BOILER_POWBAD,
    [(
        "powers correct",
        r"""
CjTestBase.checkEq(Solution.pow2(0), 1, "2^0 = 1");
CjTestBase.checkEq(Solution.pow2(4), 16, "2^4");
CjTestBase.checkEq(Solution.pow2(10), 1024, "2^10");
""",
        "The base case n == 0 must return 1 (the multiplicative identity).",
    )],
    level="debugging",
)

P_SUBSET = challenge(
    "cx-m11-subset-sum",
    "Two-branch subset sum",
    "Implement `boolean subset(int[] arr, int i, int target)`: can some subset of arr[i..] sum to target? Two branches at each element (take it / skip it); base cases: target == 0 → true, i exhausted → target == 0. Trace {2, 5, 3}, target 8 by hand.",
    BOILER_SUBSET,
    [(
        "subset exists",
        r"""
CjTestBase.checkEq(Solution.subset(new int[]{2, 5, 3}, 0, 8), true, "5 + 3");
CjTestBase.checkEq(Solution.subset(new int[]{2, 5, 3}, 0, 4), false, "no subset makes 4");
CjTestBase.checkEq(Solution.subset(new int[]{}, 0, 0), true, "empty subset, target 0");
CjTestBase.checkEq(Solution.subset(new int[]{1, 2}, 0, 3), true, "1 + 2");
""",
        "if (target == 0) return true; if (i >= arr.length) return false; return subset(arr, i+1, target - arr[i]) || subset(arr, i+1, target);",
    )],
    level="real-world",
)

CP11 = challenge(
    "cx-cp-m11-hanoi-lite",
    "Checkpoint: tower moves",
    "Implement `int moves(int n)`: the number of single-disk moves to shift an n-disk tower (the classic recurrence: move n−1 aside, move 1, move n−1 back → moves(n) = 2·moves(n−1) + 1, base moves(0) = 0). Then implement `void plan(int n)` printing one line per move: \"disk k: A->B\" style lines for the 3-disk solution is overkill — instead print just the COUNT pattern: plan(n) prints n lines \"step i\" for i = 1..n. (Both are graded; moves is the recursion, plan is the print-order discipline.)",
    r"""public class Solution {
    public static int moves(int n) {
        return 0; // replace
    }

    public static void plan(int n) {
        // replace: print "step 1" .. "step n", one per line, recursively
    }
}
""",
    [(
        "recurrence and print order",
        r"""
CjTestBase.checkEq(Solution.moves(0), 0, "no disks, no moves");
CjTestBase.checkEq(Solution.moves(1), 1, "one move");
CjTestBase.checkEq(Solution.moves(3), 7, "the classic 7-move solution");
CjTestBase.checkEq(Solution.moves(10), 1023, "2^10 - 1");
String out = CjTestBase.capture(() -> Solution.plan(3));
List<String> lines = out.lines().map(String::trim).toList();
CjTestBase.checkEq(lines, List.of("step 1", "step 2", "step 3"), "ascending print order");
""",
        "moves: n <= 0 -> 0; else 2 * moves(n - 1) + 1. plan: if (n <= 0) return; plan(n - 1); println(\"step \" + n) would print DESCENDING — put the print BEFORE the call to get ascending.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p11-recursion", "Recursion lab",
    "Digit counting, reverse printing, frame counting, a poisoned base, subset sum.",
    "Phòng đệ quy",
    "Đếm chữ số, in ngược, đếm khung, hạt giống bị đầu độc, tổng tập con.",
    after_lesson="cx-m11-frames", minutes=60, difficulty="advanced",
    challenges=[P_DIGITS, P_REVPRINT, P_CALLCOUNT, P_POWBAD, P_SUBSET],
    vi_challenges={
        "cx-m11-digit-count": vi_challenge("Đếm chữ số đệ quy",
            "Hiện thực `int numDigits(int n)` bằng đệ quy (n >= 0): 0 có 1 chữ số; nếu không 1 + numDigits(n / 10). Trường hợp cơ sở là n < 10, không phải n == 0 — nghĩ xem vì sao cả hai đều ổn ở đây.",
            [("digits counted", "if (n < 10) return 1; return 1 + numDigits(n / 10);")]),
        "cx-m11-reverse-print": vi_challenge("In ngược bằng đệ quy",
            "Hiện thực `void printRev(int[] arr, int i)` để in arr từ CUỐI về ĐẦU, mỗi số một dòng, bắt đầu từ i = 0. Lời gọi đệ quy đứng TRƯỚC lệnh in — mã sau lời gọi chạy trên đường đi lên. Mảng rỗng không in gì.",
            [("reversed lines", "if (i >= arr.length) return; printRev(arr, i + 1); println(arr[i]);")]),
        "cx-m11-call-counter": vi_challenge("Đếm số lần gọi",
            "Hiện thực `int g(int n)`: tổng số lần gọi mà f(n) thực hiện (kể cả chính nó), với f chia đôi n mỗi lần. Một vòng lặp đếm phép chia đôi là đủ — điểm nằm ở mô hình tinh thần: số lần gọi = số khung trên ngăn xếp tại điểm sâu nhất.",
            [("frames counted", "int calls = 0; while (n > 1) { calls++; n /= 2; } return calls + 1;")]),
        "cx-m11-fix-pow2": vi_challenge("Sửa hạt giống bị đầu độc",
            "`pow2(4)` trả về 0 — mọi giá trị nhân tụt xuống trường hợp cơ sở hỏng. Truy vết pow2(1) và pow2(0) bằng tay, rồi sửa giá trị cơ sở.",
            [("powers correct", "Trường hợp cơ sở n == 0 phải trả về 1 (phần tử trung hòa của phép nhân).")]),
        "cx-m11-subset-sum": vi_challenge("Tổng tập con hai nhánh",
            "Hiện thực `boolean subset(int[] arr, int i, int target)`: có tập con nào của arr[i..] cộng đúng bằng target? Hai nhánh tại mỗi phần tử (lấy / bỏ); trường hợp cơ sở: target == 0 → true, i cạn → target == 0. Truy vết {2, 5, 3}, target 8 bằng tay.",
            [("subset exists", "if (target == 0) return true; if (i >= arr.length) return false; return subset(arr, i+1, target - arr[i]) || subset(arr, i+1, target);")]),
    },
    solutions=[
        ("cx-m11-digit-count", BOILER_DIGIT.replace("return 0; // replace",
            "if (n < 10) {\n            return 1;\n        }\n        return 1 + numDigits(n / 10);"),
         BOILER_DIGIT.replace("return 0; // replace",
            "if (n == 0) {\n            return 0;\n        }\n        return 1 + numDigits(n / 10);")),
        ("cx-m11-reverse-print",
         r"""public class Solution {
    public static void printRev(int[] arr, int i) {
        if (i >= arr.length) {
            return;
        }
        printRev(arr, i + 1);
        System.out.println(arr[i]);
    }
}
""",
         r"""public class Solution {
    public static void printRev(int[] arr, int i) {
        if (i >= arr.length) {
            return;
        }
        System.out.println(arr[i]);
        printRev(arr, i + 1);
    }
}
"""),
        ("cx-m11-call-counter", BOILER_CALLCOUNT.replace("return 0; // replace: count of calls f(n) makes (non-recursive loop is fine)",
            "int calls = 0;\n        while (n > 1) {\n            calls++;\n            n /= 2;\n        }\n        return calls + 1;"),
         BOILER_CALLCOUNT.replace("return 0; // replace: count of calls f(n) makes (non-recursive loop is fine)",
            "int calls = 0;\n        while (n > 1) {\n            calls++;\n            n /= 2;\n        }\n        return calls;")),
        ("cx-m11-fix-pow2", BOILER_POWBAD.replace("            return 0;\n        }", "            return 1;\n        }"),
         BOILER_POWBAD),
        ("cx-m11-subset-sum", BOILER_SUBSET.replace("return false; // replace",
            "if (target == 0) {\n            return true;\n        }\n        if (i >= arr.length) {\n            return false;\n        }\n        return subset(arr, i + 1, target - arr[i]) || subset(arr, i + 1, target);"),
         BOILER_SUBSET.replace("return false; // replace",
            "if (i >= arr.length) {\n            return target == 0;\n        }\n        return subset(arr, i + 1, target - arr[i]) && subset(arr, i + 1, target);")),
    ],
)

write_checkpoint(
    M, "cx-cp-m11", "Checkpoint: moves and plan",
    "A classic recurrence plus the print-order discipline in one method pair.",
    30,
    r"""
moves is the exam's favorite recurrence (2·f(n−1)+1 → 2ⁿ−1); plan is
the print-order trap: printing BEFORE the recursive call yields
ascending order, printing AFTER yields descending. Students who can
produce both on demand — one arithmetic, one structural — own the two
halves of every recursion question the exam asks.
""",
    "Điểm kiểm tra: moves và plan",
    "Một công thức truy hồi kinh điển cộng kỷ luật thứ-tự-in trong một cặp phương thức.",
    r"""
moves là công thức truy hồi ưa thích của đề thi (2·f(n−1)+1 → 2ⁿ−1);
plan là cái bẫy thứ-tự-in: in TRƯỚC lời gọi đệ quy cho thứ tự tăng dần,
in SAU cho thứ tự giảm dần. Học sinh tự tay viết được cả hai — một bài
số học, một bài cấu trúc — là sở hữu trọn hai nửa của mọi câu hỏi đệ quy
ma đề thi hỏi.
""",
    CP11,
    vi_challenge("Điểm kiểm tra: moves và plan",
        "Hiện thực `int moves(int n)`: số lần di chuyển đĩa đơn để dời tháp n đĩa (công thức kinh điển: moves(n) = 2·moves(n−1) + 1, cơ sở moves(0) = 0). Rồi `void plan(int n)` in \"step 1\"..\"step n\", mỗi dòng một câu, theo thứ tự TĂNG DẦN bằng đệ quy.",
        [("recurrence and print order", "moves: n <= 0 → 0; không thì 2 * moves(n - 1) + 1. plan: in TRƯỚC lời gọi để được thứ tự tăng dần.")]),
    solution=r"""public class Solution {
    public static int moves(int n) {
        if (n <= 0) {
            return 0;
        }
        return 2 * moves(n - 1) + 1;
    }

    public static void plan(int n) {
        if (n <= 0) {
            return;
        }
        plan(n - 1);
        System.out.println("step " + n);
    }
}
""",
    wrong=r"""public class Solution {
    public static int moves(int n) {
        if (n <= 0) {
            return 0;
        }
        return 2 * moves(n - 1) + 1;
    }

    public static void plan(int n) {
        if (n <= 0) {
            return;
        }
        System.out.println("step " + n);
        plan(n - 1);
    }
}
""",
)
