#!/usr/bin/env python3
"""AP CSA M16 — Testing and Debugging: error classes, test design, systematic debugging."""
from apc import *

M = "apc-testing"

L1 = r"""
Every Java failure belongs to one of three classes, and each has a
different repair strategy:

- **Compile-time error** — the compiler rejects the source: missing
  semicolon, wrong type, unknown name. Nothing runs. Read the message:
  it names the file, line, and what it expected.
- **Runtime error (exception)** — compiles, then dies mid-run:
  `ArithmeticException` (integer divide by zero),
  `ArrayIndexOutOfBoundsException`, `NullPointerException`. The stack
  trace names the line that threw.
- **Logical error** — compiles, runs, produces a wrong answer. No
  message ever appears. Only **testing** finds these, which is why
  they're the most dangerous.

```java
int avg = total / n;      // compiles; throws at runtime if n == 0;
                          // silently wrong if total or n is wrong
```

The exam's "code does not compile" questions are all compile-class;
its "what is output" questions are trace questions guarding against
your logical errors. Classify first, then debug — the class tells you
where to look.
"""

L2 = r"""
A **test case** is an input, an expected output, and a reason it might
break the code. Good test design targets boundaries:

- **Boundary values**: for `score >= 60` test 59, 60, and 61. The bug
  almost always lives exactly at the comparison.
- **Empty / zero / one**: empty arrays, length 0, single elements.
  Loops that "obviously work" break on their first iteration.
- **Negatives and overflow-aware big values**: `int` flips sign past
  2,147,483,647 — sums of many positives can overflow silently.
- **Duplicates and ties**: does "first" or "last" win?
- **The not-found path**: search returns what when absent?

```java
// code under test: isPassing(score)
checkEq(isPassing(59), false, "just below");
checkEq(isPassing(60), true,  "exact boundary");
checkEq(isPassing(61), true,  "just above");
```

Notice what each assertion *says*, not just what it checks — a test
that fails should name the behavior that broke. That habit is what
"defensive testing" means on the exam and in real code.
"""

L3 = r"""
Systematic debugging — a loop, not a hunt:

1. **Reproduce** on the smallest failing input. A bug you can't shrink,
   you can't fix.
2. **Classify**: compile / runtime / logical (Module 16.1).
3. **Trace state**: walk the code by hand writing every variable's
   value on every line — a **trace table**. The row where reality
   diverges from intention is the bug.
4. **Assert mid-way**: print or check intermediate values ("at this
   point, `sum` should be 6").
5. **Fix the cause, not the symptom**: if a loop is off-by-one, change
   the bound — don't add a special case downstream.

Trace-table example — the divergence is line 4:

| line        | i | sum | want   |
| ----------- | - | --- | ------ |
| sum = 0     | – | 0   | 0      |
| sum += i    | 1 | 1   | 1      |
| sum += i    | 2 | 3   | 3      |
| sum += i    | 3 | **6** | **9**? (goal: sum of 1..3 = 6) |

When your hand-trace of the *intended* algorithm disagrees with what
the code computes, you've found the exact line to change.
"""

write_module(
    M,
    "Testing and Debugging",
    "Error classes, boundary test design, trace tables, and a systematic debugging loop.",
    "Kiểm thử và gỡ lỗi",
    "Phân loại lỗi, thiết kế test biên, bảng truy vết, và vòng lặp gỡ lỗi có hệ thống.",
    lessons=["apc-m16-errors", "apc-m16-cases", "apc-m16-trace", "apc-cp-m16"],
    practices=["apc-p16-testing"],
)

write_lesson(
    M, "apc-m16-errors", "Three classes of errors",
    "Compile-time, runtime exceptions, logical errors — and where each one hides.",
    10, L1,
    "Ba lớp lỗi",
    "Lỗi biên dịch, ngoại lệ runtime, lỗi logic — và mỗi loại ẩn ở đâu.",
    r"""
Mọi lỗi Java thuộc một trong ba lớp, và mỗi lớp có chiến lược sửa khác
nhau:

- **Lỗi biên dịch** — trình biên dịch từ chối mã nguồn: thiếu chấm
  phẩy, sai kiểu, tên không tồn tại. Chẳng gì chạy được. Đọc thông
  báo: nó nêu tên tệp, dòng, và những gì nó mong đợi.
- **Lỗi runtime (ngoại lệ)** — biên dịch xong, chết giữa đường:
  `ArithmeticException` (chia nguyên cho 0),
  `ArrayIndexOutOfBoundsException`, `NullPointerException`. Stack trace
  nêu dòng gây ném.
- **Lỗi logic** — biên dịch được, chạy được, ra đáp án sai. Không bao
  giờ có thông báo. Chỉ **kiểm thử** tìm ra được, nên đây là lớp nguy
  hiểm nhất.

```java
int avg = total / n;      // biên dịch được; ném ngoại lệ nếu n == 0;
                          // sai lặng lẽ nếu total hoặc n sai
```

Các câu "mã không biên dịch được" của đề thuộc lớp biên dịch; các câu
"kết quả in là gì" là câu truy vết giữ bạn khỏi lỗi logic của chính
bạn. Phân loại trước, gỡ sau — lớp lỗi chỉ cho bạn chỗ cần nhìn.
""",
)

write_lesson(
    M, "apc-m16-cases", "Designing test cases",
    "Boundary values, empties, negatives, ties, not-found — tests with reasons.",
    12, L2,
    "Thiết kế ca kiểm thử",
    "Giá trị biên, rỗng, âm, hòa, không-thấy — test phải có lý do.",
    r"""
Một **ca kiểm thử** gồm đầu vào, đầu ra mong đợi, và lý do nó có thể
làm hỏng mã. Thiết kế test tốt nhắm vào biên:

- **Giá trị biên**: với `score >= 60` hãy thử 59, 60, và 61. Lỗi hầu
  như luôn nằm ngay phép so sánh.
- **Rỗng / không / một**: mảng rỗng, độ dài 0, phần tử đơn. Vòng lặp
  "hiển nhiên đúng" thường gãy ngay vòng đầu tiên.
- **Số âm và giá trị lớn**: `int` đổi dấu vượt quá 2.147.483.647 —
  tổng nhiều số dương có thể tràn lặng lẽ.
- **Trùng lặp và hòa**: "đầu" hay "cuối" thắng?
- **Đường không-thấy**: tìm kiếm trả về gì khi vắng mặt?

```java
// mã cần kiểm: isPassing(score)
checkEq(isPassing(59), false, "dưới biên một chút");
checkEq(isPassing(60), true,  "đúng biên");
checkEq(isPassing(61), true,  "trên biên một chút");
```

Chú ý mỗi assertion *nói* gì, không chỉ nó kiểm gì — test thất bại
phải gọi tên hành vi đã hỏng. Thói quen đó chính là "kiểm thử phòng
ngự" trên đề và trong mã thật.
""",
)

write_lesson(
    M, "apc-m16-trace", "Trace tables and the debugging loop",
    "Reproduce, classify, trace state, assert mid-way, fix the cause.",
    12, L3,
    "Bảng truy vết và vòng lặp gỡ lỗi",
    "Tái hiện, phân loại, truy vết trạng thái, khẳng định giữa đường, sửa gốc rễ.",
    r"""
Gỡ lỗi có hệ thống — một vòng lặp, không phải cuộc săn mò:

1. **Tái hiện** trên đầu vào thất bại nhỏ nhất. Lỗi không thu nhỏ được
   thì không sửa được.
2. **Phân loại**: biên dịch / runtime / logic (bài 16.1).
3. **Truy vết trạng thái**: đi bộ qua mã bằng tay, ghi giá trị của
   mọi biến ở mọi dòng — một **bảng truy vết**. Hàng nơi thực tế tách
   khỏi ý định chính là lỗi.
4. **Khẳng định giữa đường**: in hoặc kiểm giá trị trung gian ("đến
   đây thì `sum` phải là 6").
5. **Sửa gốc rễ, không sửa triệu chứng**: vòng lặp lệch-một thì đổi
   cận — đừng thêm trường hợp đặc biệt ở phía sau.

Ví dụ bảng truy vết — điểm rẽ là dòng 4:

| dòng        | i | sum | muốn   |
| ----------- | - | --- | ------ |
| sum = 0     | – | 0   | 0      |
| sum += i    | 1 | 1   | 1      |
| sum += i    | 2 | 3   | 3      |
| sum += i    | 3 | **6** | **9**? (mục tiêu: tổng 1..3 = 6) |

Khi truy vết tay của thuật toán *đúng* mâu thuẫn với thứ mã tính ra,
bạn đã tìm ra đúng dòng cần thay đổi.
""",
)

BOILER_LEAP = r"""public class Solution {
    public static boolean isLeap(int year) {
        // complete: leap if divisible by 4, except centuries not
        // divisible by 400
        return false;
    }
}
"""

BOILER_MID = r"""public class Solution {
    public static int midValue(int a, int b, int c) {
        // complete: the middle of the three values (not min, not max)
        return 0;
    }
}
"""

BOILER_FIXDIV = r"""public class Solution {
    public static int average(int[] scores) {
        // BUG: original flaw kept — crashes with
        // ArithmeticException on an empty array
        int total = 0;
        for (int s : scores) {
            total += s;
        }
        return total / scores.length;
    }
}
"""

BOILER_FIXBOUND = r"""public class Solution {
    public static boolean isPassing(int score) {
        // BUG: original flaw kept — boundary off by one; 60 must pass
        return score > 60;
    }
}
"""

CP16 = r"""public class Solution {
    public static String gradeLabel(int score) {
        // complete: 90+ "A", 80-89 "B", 70-79 "C", 60-69 "D", else "F"
        return "";
    }
}
"""

P_LEAP = challenge(
    "apc-m16-leap",
    "Leap year with boundaries",
    "Implement `isLeap(int year)`: divisible by 4 is a leap year, EXCEPT century years not divisible by 400. Write the two rules as nested conditions.",
    BOILER_LEAP,
    [(
        "century boundaries",
        r"""
CjTestBase.checkEq(Solution.isLeap(2000), true, "divisible by 400");
CjTestBase.checkEq(Solution.isLeap(1900), false, "century, not 400");
CjTestBase.checkEq(Solution.isLeap(2024), true, "plain multiple of 4");
CjTestBase.checkEq(Solution.isLeap(2023), false, "odd year");
""",
        "(year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))",
    )],
    level="independent",
)

P_MID = challenge(
    "apc-m16-mid",
    "Middle value",
    "Implement `midValue(int a, int b, int c)`: return the middle of the three (not the min, not the max). Ties are fine — any middle-order value works.",
    BOILER_MID,
    [(
        "order permutations",
        r"""
CjTestBase.checkEq(Solution.midValue(3, 1, 2), 2, "unsorted inputs");
CjTestBase.checkEq(Solution.midValue(1, 2, 3), 2, "already sorted");
CjTestBase.checkEq(Solution.midValue(5, 5, 1), 5, "tie pair");
CjTestBase.checkEq(Solution.midValue(7, 7, 7), 7, "all equal");
""",
        "max minus min, removed from the sum — or a three-way comparison chain.",
    )],
    level="independent",
)

P_FIXDIV = challenge(
    "apc-m16-fix-div",
    "Debug: crash on empty input",
    "`average(int[] scores)` throws ArithmeticException on an empty array. Fix it to return 0 for an empty array and the correct int average otherwise (keep integer division). Signature stays the same.",
    BOILER_FIXDIV,
    [(
        "empty guarded",
        r"""
CjTestBase.checkEq(Solution.average(new int[] {}), 0, "empty array, no crash");
CjTestBase.checkEq(Solution.average(new int[] {80, 90}), 85, "normal average");
CjTestBase.checkEq(Solution.average(new int[] {1, 2}), 1, "integer division truncates");
""",
        "guard scores.length == 0 before dividing.",
    )],
    level="debugging",
)

P_FIXBOUND = challenge(
    "apc-m16-fix-boundary",
    "Debug: boundary off by one",
    "`isPassing(60)` must be true (60 is a pass) but the code rejects it. Fix the comparison so the boundary is inclusive.",
    BOILER_FIXBOUND,
    [(
        "boundary repaired",
        r"""
CjTestBase.checkEq(Solution.isPassing(59), false, "below stays below");
CjTestBase.checkEq(Solution.isPassing(60), true, "boundary included");
CjTestBase.checkEq(Solution.isPassing(61), true, "above stays above");
""",
        "> becomes >=.",
    )],
    level="debugging",
)

CP16C = challenge(
    "apc-cp-m16-grade",
    "Checkpoint: grade boundaries",
    "Implement `gradeLabel(int score)`: 90+ returns \"A\", 80–89 \"B\", 70–79 \"C\", 60–69 \"D\", otherwise \"F\". The else-if chain order IS the correctness.",
    CP16,
    [(
        "every boundary",
        r"""
CjTestBase.checkEq(Solution.gradeLabel(100), "A", "top");
CjTestBase.checkEq(Solution.gradeLabel(90), "A", "A boundary");
CjTestBase.checkEq(Solution.gradeLabel(89), "B", "just under A");
CjTestBase.checkEq(Solution.gradeLabel(60), "D", "D boundary");
CjTestBase.checkEq(Solution.gradeLabel(59), "F", "fail zone");
""",
        "test from the highest bound down; each branch owns its exact range.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p16-testing", "Testing and debugging reps", "Leap logic, middle value, crash guards, boundary repair, grade chains.",
    "Luyện kiểm thử và gỡ lỗi", "Logic nhuận, giá trị giữa, chặn crash, sửa biên, chuỗi xếp loại.",
    after_lesson="apc-m16-trace", minutes=50, difficulty="beginner",
    challenges=[P_LEAP, P_MID, P_FIXDIV, P_FIXBOUND],
    vi_challenges={
        "apc-m16-leap": vi_challenge("Nhuận với các biên", "Cài đặt `isLeap(int year)`: chia hết cho 4 là nhuận, NGOẠI TRỪ các năm thế kỷ không chia hết cho 400. Viết hai luật này thành điều kiện lồng nhau.",
            [("century boundaries", "(year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))")]),
        "apc-m16-mid": vi_challenge("Giá trị giữa", "Cài đặt `midValue(int a, int b, int c)`: trả giá trị nằm giữa trong ba giá trị (không phải min, không phải max). Bằng nhau không sao — giá trị giữa-thứ-tự nào cũng được.",
            [("order permutations", "tổng trừ min trừ max — hoặc chuỗi so sánh ba nhánh.")]),
        "apc-m16-fix-div": vi_challenge("Gỡ lỗi: crash khi đầu vào rỗng", "`average(int[] scores)` ném ArithmeticException với mảng rỗng. Sửa để trả 0 với mảng rỗng và trung bình int đúng trong các trường hợp còn lại (giữ phép chia nguyên). Chữ ký giữ nguyên.",
            [("empty guarded", "chặn scores.length == 0 trước khi chia.")]),
        "apc-m16-fix-boundary": vi_challenge("Gỡ lỗi: biên lệch một", "`isPassing(60)` phải là true (60 là đậu) nhưng mã đang từ chối. Sửa phép so sánh để biên được tính là đậu.",
            [("boundary repaired", "> đổi thành >=.")]),
    },
    solutions=[
        ("apc-m16-leap", r"""public class Solution {
    public static boolean isLeap(int year) {
        return (year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0));
    }
}
""", r"""public class Solution {
    public static boolean isLeap(int year) {
        // BUG: treats every multiple of 100 as a leap year — the
        // 400-year exception is missing
        return year % 4 == 0;
    }
}
"""),
        ("apc-m16-mid", r"""public class Solution {
    public static int midValue(int a, int b, int c) {
        int min = Math.min(a, Math.min(b, c));
        int max = Math.max(a, Math.max(b, c));
        return a + b + c - min - max;
    }
}
""", r"""public class Solution {
    public static int midValue(int a, int b, int c) {
        // BUG: returns the AVERAGE (integer division) instead of the
        // middle value — midValue(1, 2, 9) gives 4, not 2
        return (a + b + c) / 3;
    }
}
"""),
        ("apc-m16-fix-div", r"""public class Solution {
    public static int average(int[] scores) {
        if (scores.length == 0) {
            return 0;
        }
        int total = 0;
        for (int s : scores) {
            total += s;
        }
        return total / scores.length;
    }
}
""", r"""public class Solution {
    public static int average(int[] scores) {
        // BUG: original flaw kept — crashes with
        // ArithmeticException on an empty array
        int total = 0;
        for (int s : scores) {
            total += s;
        }
        return total / scores.length;
    }
}
"""),
        ("apc-m16-fix-boundary", r"""public class Solution {
    public static boolean isPassing(int score) {
        return score >= 60;
    }
}
""", r"""public class Solution {
    public static boolean isPassing(int score) {
        // BUG: original flaw kept — boundary off by one; 60 must pass
        return score > 60;
    }
}
"""),
        ("apc-cp-m16-grade", r"""public class Solution {
    public static String gradeLabel(int score) {
        if (score >= 90) {
            return "A";
        } else if (score >= 80) {
            return "B";
        } else if (score >= 70) {
            return "C";
        } else if (score >= 60) {
            return "D";
        }
        return "F";
    }
}
""", r"""public class Solution {
    public static String gradeLabel(int score) {
        // BUG: chain tested from the LOWEST bound up — every score 60+
        // returns "D" because the first branch always matches
        if (score >= 60) {
            return "D";
        } else if (score >= 70) {
            return "C";
        } else if (score >= 80) {
            return "B";
        } else if (score >= 90) {
            return "A";
        }
        return "F";
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m16", "Checkpoint: grade boundaries",
    "The else-if chain order is the correctness — highest bound first.",
    25,
    r"""
The pattern: classification chains must run from the highest bound
down. Tested bottom-up, the first branch swallows every later one.
This is exactly the trap the exam's "what is returned" trace items
probe — trace the chain in ITS order, not in yours.
""",
    "Điểm kiểm tra: các biên xếp loại",
    "Thứ tự chuỗi else-if chính là tính đúng — biên cao nhất trước.",
    r"""
Mẫu hình: chuỗi phân loại phải chạy từ biên cao nhất xuống. Kiểm từ
dưới lên, nhánh đầu nuốt hết các nhánh sau. Đây chính là cái bẫy mà
các câu truy vết "trả về gì" của đề khai thác — truy vết chuỗi theo
THỨ TỰ CỦA NÓ, không phải thứ tự của bạn.
""",
    CP16C,
    vi_challenge("Điểm kiểm tra: các biên xếp loại", "Cài đặt `gradeLabel(int score)`: 90+ trả \"A\", 80–89 \"B\", 70–79 \"C\", 60–69 \"D\", còn lại \"F\". Thứ tự chuỗi else-if CHÍNH LÀ tính đúng.",
        [("every boundary", "kiểm từ biên cao nhất xuống; mỗi nhánh sở hữu đúng khoảng của mình.")]),
    solution=r"""public class Solution {
    public static String gradeLabel(int score) {
        if (score >= 90) {
            return "A";
        } else if (score >= 80) {
            return "B";
        } else if (score >= 70) {
            return "C";
        } else if (score >= 60) {
            return "D";
        }
        return "F";
    }
}
""",
    wrong=r"""public class Solution {
    public static String gradeLabel(int score) {
        // BUG: chain tested from the LOWEST bound up — every score 60+
        // returns "D" because the first branch always matches
        if (score >= 60) {
            return "D";
        } else if (score >= 70) {
            return "C";
        } else if (score >= 80) {
            return "B";
        } else if (score >= 90) {
            return "A";
        }
        return "F";
    }
}
""",
)
