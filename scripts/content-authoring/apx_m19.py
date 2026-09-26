#!/usr/bin/env python3
"""AP CSA Advanced M19 — Error analysis lab (diagnose, don't just read)."""
from apx import *

M = "apx-errors"

write_module(
    M,
    "Error Analysis Lab",
    "A library of broken snippets across thirteen error classes: diagnose the class, predict the symptom, then repair. Difficulty E3–E5.",
    "Phòng thí nghiệm phân tích lỗi",
    "Thư viện các đoạn mã hỏng trên mười ba lớp lỗi: chẩn đoán lớp lỗi, dự đoán triệu chứng, rồi sửa chữa. Độ khó E3–E5.",
    lessons=["apx-m19-taxonomy", "apx-m19-diagnose", "apx-m19-family", "apx-cp-m19"],
    practices=["apx-p19-errors"],
)

L1 = r"""
**The error taxonomy.** Thirteen classes cover nearly every lost
point. Each has a signature symptom — learn the mapping and
debugging becomes lookup:

1. **Off-by-one index** — exception or a missed end element.
2. **Wrong loop boundary** — one extra or one missing iteration.
3. **Inverted boolean condition** — exactly backwards behavior.
4. **Wrong accumulator op** — sum where count belongs (or minus
   where plus).
5. **Unreset state** — value from a previous run leaks into the
   next (streak counters, running totals).
6. **String index error** — charAt/substring past the ends.
7. **ArrayList mutation-scan** — forward removal skips the shifted
   element.
8. **Object state error** — a field mutated by the wrong method or
   read before assignment.
9. **Constructor error** — shadowed parameter, forgotten field.
10. **Inheritance error** — override missing `super.` or the
    override never called.
11. **Polymorphism error** — reference type read where the object
    type governs.
12. **Recursion error** — missing/wrong base case or no progress.
13. **Missing edge case** — works on the example, dies on empty /
    single / extremes.

Diagnosis habit: name the CLASS first, then find the line. The
name tells you what to look for (an index? a flag? a base case?).
"""

L2 = r"""
**Diagnose before you read the fix.** Every challenge in this lab
shows a snippet and its symptom — output, exception, or wrong
count. Your submission must (1) predict/verify the symptom by
reasoning, and (2) repair the snippet. The grader runs your
REPAIRED version against tests that include the symptom case plus
the edge cases the author forgot.

The diagnostic questions, in order:

- **Compile or runtime?** An exception pinpoints the class
  instantly (ArrayIndexOutOfBounds → class 1 or 6; StackOverflow →
  class 12).
- **Always wrong or boundary-wrong?** Always-wrong smells like an
  inverted condition or wrong operator; boundary-wrong smells
  like an index or a missing reset.
- **Wrong on which input?** Construct the minimal input that
  shows the bug — the answer usually falls out of tracing it.

Two snippets in this lab are *actually correct* — diagnosing them
as "no bug, tests pass" is the right answer. Calibration matters:
not every weird-looking line is a bug.
"""

L3 = r"""
**Family inspection.** After repairing, ask the family question:
*inputs of the same shape* — other empty inputs, other ties,
other single-element cases — would this same bug class corrupt?
Your repair must handle the whole family, not one specimen. This
is why the hidden tests always include at least one sibling of
the symptom case.

For the exam: debugging MCQs give you the snippet and FOUR
proposed single-line fixes. The wrong options are other classes'
fixes — plausible, well-written, and aimed at a different bug.
Identifying the CLASS first eliminates three options without
testing any of them. That is the lab's payout: taxonomy turns a
search problem into a recognition problem.
"""

VI_L1 = r"""
**Phân loại lỗi.** Mười ba lớp phủ gần như mọi điểm mất. Mỗi lớp có
triệu chứng đặc trưng — học bảng ánh xạ và gỡ lỗi trở thành tra
bảng:

1. **Chỉ số lệch một** — ngoại lệ hoặc bỏ sót phần tử cuối.
2. **Biên vòng lặp sai** — thừa hoặc thiếu đúng một vòng lặp.
3. **Điều kiện boolean đảo** — hành vi ngược hoàn toàn.
4. **Phép tích lũy sai** — cộng nơi phải đếm (hoặc trừ nơi phải cộng).
5. **Trạng thái không reset** — giá trị từ lần chạy trước rò vào lần
   sau (bộ đếm run, tổng chạy).
6. **Lỗi chỉ số chuỗi** — charAt/substring vượt hai đầu.
7. **Quét-biến-đổi ArrayList** — xóa khi duyệt tới bỏ sót phần tử
   bị dồn.
8. **Lỗi trạng thái đối tượng** — một trường bị biến đổi bởi phương
   thức sai hoặc đọc trước khi gán.
9. **Lỗi constructor** — tham số bị bóng che, trường bị quên.
10. **Lỗi kế thừa** — bản ghi đè thiếu `super.` hoặc bản ghi đè
    không bao giờ được gọi.
11. **Lỗi đa hình** — đọc kiểu tham chiếu nơi kiểu đối tượng cai trị.
12. **Lỗi đệ quy** — trường hợp cơ sở thiếu/sai hoặc không có tiến
    triển.
13. **Thiếu trường hợp biên** — chạy đúng với ví dụ, chết với rỗng /
    một phần tử / cực trị.

Thói quen chẩn đoán: gọi tên LỚP trước, rồi mới tìm dòng. Tên lớp
cho biết phải tìm gì (một chỉ số? một cờ? một trường hợp cơ sở?).
"""

VI_L2 = r"""
**Chẩn đoán trước khi đọc bản sửa.** Mỗi bài trong phòng lab này
đưa một đoạn mã và triệu chứng của nó — kết quả, ngoại lệ, hoặc số
đếm sai. Bài nộp của bạn phải (1) dự đoán/kiểm chứng triệu chứng
bằng suy luận, và (2) sửa lại đoạn mã. Máy chấm chạy bản ĐÃ SỬA
của bạn với các test gồm trường hợp triệu chứng cộng các trường hợp
biên mà tác giả quên.

Các câu hỏi chẩn đoán, theo thứ tự:

- **Lúc biên dịch hay lúc chạy?** Một ngoại lệ chỉ đích danh lớp
  lỗi ngay lập tức (ArrayIndexOutOfBounds → lớp 1 hoặc 6;
  StackOverflow → lớp 12).
- **Luôn sai hay sai-ở-biên?** Luôn sai gợi ý điều kiện đảo hoặc
  toán tử sai; sai-ở-biên gợi ý chỉ số hoặc thiếu reset.
- **Sai ở đầu vào nào?** Dựng đầu vào tối thiểu phơi bày lỗi — đáp
  án thường rơi ra từ truy vết nó.

Hai đoạn mã trong lab này *thực ra đúng* — chẩn đoán "không lỗi,
test qua" là đáp án đúng. Hiệu chuẩn quan trọng: không phải dòng
nào trông lạ cũng là lỗi.
"""

VI_L3 = r"""
**Soi cả họ lỗi.** Sau khi sửa, hỏi câu hỏi cả-họ: *các đầu vào cùng
hình dạng* — các đầu vào rỗng khác, các trường hợp hòa khác, các
trường hợp một-phần-tử khác — lỗi cùng lớp này có làm hỏng chúng
không? Bản sửa của bạn phải xử lý cả họ, không phải một mẫu vật.
Vì vậy các test ẩn luôn có ít nhất một người anh em của trường hợp
triệu chứng.

Cho phòng thi: trắc nghiệm gỡ lỗi đưa bạn đoạn mã và BỐN bản sửa
một-dòng đề xuất. Các phương án sai là bản sửa của các lớp khác —
hợp lý, viết đẹp, và nhắm vào một lỗi khác. Gọi tên LỚP trước loại
sạch ba phương án mà không cần thử bất kỳ cái nào. Đó là khoản lời
của lab này: phân loại biến bài toán tìm-kiếm thành bài toán
nhận-dạng.
"""

BOILER_IDX = r"""public class Solution {
    // SYMPTOM: crashes on the last element for some inputs
    public static int lastChar(String s) {
        return s.charAt(s.length());
    }
}
"""

BOILER_ACC = r"""public class Solution {
    // SYMPTOM: returns 0 or negative numbers where a sum is expected
    public static int total(int[] arr) {
        int sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum -= arr[i];
        }
        return sum;
    }
}
"""

BOILER_RESET = r"""public class Solution {
    // SYMPTOM: overestimates the longest run on multi-run inputs
    public static int longestRun(int[] arr) {
        int best = 0;
        int cur = 0;
        for (int i = 0; i < arr.length; i++) {
            if (i > 0 && arr[i] == arr[i - 1]) {
                cur++;
            } else {
                cur++;
            }
            if (cur > best) {
                best = cur;
            }
        }
        return best;
    }
}
"""

BOILER_CONSTR = r"""public class Solution {
    public static class Wallet {
        private int cents;

        public Wallet(int cents) {
            cents = cents;
        }

        public int balance() {
            return cents;
        }
    }
}
"""

BOILER_RECUR = r"""public class Solution {
    // SYMPTOM: StackOverflowError on every input
    public static int countDown(int n) {
        if (n < 0) {
            return 0;
        }
        return countDown(n);
    }
}
"""

BOILER_EDGE = r"""public class Solution {
    // SYMPTOM: crashes on the empty string
    public static char firstChar(String s) {
        return s.charAt(0);
    }
}
"""

P_IDX = challenge(
    "apx-m19-fix-lastchar",
    "Diagnose 1: the boundary crash",
    "Classify the error (which taxonomy class?), then repair "
    "`lastChar` so it returns the LAST character's char code. Empty "
    "input is not part of this task's contract (s is non-empty).",
    BOILER_IDX,
    [(
        "repaired boundary",
        r"""
CjTestBase.checkEq((char) Solution.lastChar("abc"), 'c', "last char code");
CjTestBase.checkEq((char) Solution.lastChar("z"), 'z', "single char");
""",
        "Class 1/6 (index off-by-one): length() is one past the end; use length() - 1.",
    )],
    level="debugging",
    difficulty="intermediate",
)

P_ACC = challenge(
    "apx-m19-fix-total",
    "Diagnose 2: the backwards accumulator",
    "Classify the error, then repair `total` so it returns the sum "
    "of the array (empty → 0).",
    BOILER_ACC,
    [(
        "repaired accumulator",
        r"""
CjTestBase.checkEq(Solution.total(new int[]{4, 5, 6}), 15, "plain sum");
CjTestBase.checkEq(Solution.total(new int[]{-3, 3}), 0, "negatives included");
CjTestBase.checkEq(Solution.total(new int[]{}), 0, "empty");
""",
        "Class 4 (wrong accumulator op): -= must become +=.",
    )],
    level="debugging",
    difficulty="intermediate",
)

P_RESET = challenge(
    "apx-m19-fix-reset",
    "Diagnose 3: the unreset counter",
    "Classify the error, then repair `longestRun` so it returns the "
    "longest run of equal adjacent values. (Hint: both branches "
    "increment — one of them should not.)",
    BOILER_RESET,
    [(
        "repaired run",
        r"""
CjTestBase.checkEq(Solution.longestRun(new int[]{2, 2, 1, 1}), 2, "two runs of two");
CjTestBase.checkEq(Solution.longestRun(new int[]{1, 2, 2, 3, 3, 3, 1}), 3, "triple run");
CjTestBase.checkEq(Solution.longestRun(new int[]{}), 0, "empty");
""",
        "Class 5 (unreset state): the else branch must reset cur to 1, not increment.",
    )],
    level="debugging",
    difficulty="advanced",
)

P_WALLET = challenge(
    "apx-m19-fix-wallet",
    "Diagnose 4: the shadowed constructor",
    "Classify the error, then repair the `Wallet` class so a new "
    "Wallet(500) reports a balance of 500.",
    BOILER_CONSTR,
    [(
        "repaired constructor",
        r"""
Solution.Wallet w = new Solution.Wallet(500);
CjTestBase.checkEq(w.balance(), 500, "constructor stores");
""",
        "Class 9 (constructor error): cents = cents assigns the parameter to itself; this.cents = cents.",
    )],
    level="debugging",
    difficulty="intermediate",
)

P_RECUR = challenge(
    "apx-m19-fix-countdown",
    "Diagnose 5: the recursion without progress",
    "Classify the error, then repair `countDown` so it returns the "
    "count from n down to 0 inclusive (countDown(3) → 4).",
    BOILER_RECUR,
    [(
        "repaired recursion",
        r"""
CjTestBase.checkEq(Solution.countDown(3), 4, "3,2,1,0");
CjTestBase.checkEq(Solution.countDown(0), 1, "just zero");
""",
        "Class 12 (recursion, no progress): countDown(n) must call countDown(n - 1) and add 1.",
    )],
    level="debugging",
    difficulty="advanced",
)

P_EDGE = challenge(
    "apx-m19-fix-firstchar",
    "Diagnose 6: the missing edge case",
    "Classify the error, then repair `firstChar` so it returns the "
    "first character's code, or -1 for the EMPTY string.",
    BOILER_EDGE,
    [(
        "repaired edge",
        r"""
CjTestBase.checkEq((char) Solution.firstChar("abc"), 'a', "first char");
CjTestBase.checkEq(Solution.firstChar(""), -1, "empty sentinel");
""",
        "Class 13 (missing edge case): guard s.length() == 0 before charAt(0).",
    )],
    level="debugging",
    difficulty="intermediate",
)

CP19 = challenge(
    "apx-cp-m19-scan",
    "Checkpoint: diagnose and repair",
    "No class label. The method should remove every occurrence of "
    "`target` from an ArrayList<String>, preserving order, and "
    "return how many were removed. It returns wrong counts AND "
    "leaves some targets in the list. Classify, repair, verify.",
    r"""public class Solution {
    // SYMPTOM: wrong counts and survivors
    public static int removeAll(java.util.ArrayList<String> list, String target) {
        int removed = 0;
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).equals(target)) {
                list.remove(i);
            }
        }
        return removed;
    }
}
""",
    [(
        "repaired removal",
        r"""
java.util.ArrayList<String> l = new java.util.ArrayList<>(java.util.List.of("a", "b", "a", "a", "c"));
CjTestBase.checkEq(Solution.removeAll(l, "a"), 3, "three removed");
CjTestBase.checkEq(l, new java.util.ArrayList<>(java.util.List.of("b", "c")), "order kept");
java.util.ArrayList<String> none = new java.util.ArrayList<>(java.util.List.of("x"));
CjTestBase.checkEq(Solution.removeAll(none, "a"), 0, "nothing matches");
""",
        "Two bug classes at once (7: mutation-scan skip, 4: uncounted removals) — backward loop plus removed++.",
    )],
    level="debugging",
    difficulty="advanced",
)

VI_CP19 = vi_challenge(
    "Điểm kiểm tra: chẩn đoán và sửa chữa",
    "Không nhãn lớp. Phương thức nên xóa mọi lần xuất hiện của "
    "`target` khỏi ArrayList<String>, giữ thứ tự, và trả về số lần "
    "xóa. Nó trả số đếm sai VÀ còn sót lại vài target. Phân loại, "
    "sửa, kiểm chứng.",
    [("repaired removal", "Hai lớp lỗi cùng lúc (7: quét-biến-đổi bỏ sót, 4: xóa không đếm) — vòng ngược cộng removed++.")],
)

write_practice(
    M, "apx-p19-errors", "Diagnosis gauntlet",
    "Six snippets, six error classes; name the class, then repair.",
    "Võ đài chẩn đoán",
    "Sáu đoạn mã, sáu lớp lỗi; gọi tên lớp, rồi sửa chữa.",
    after_lesson="apx-m19-family", minutes=60, difficulty="advanced",
    challenges=[P_IDX, P_ACC, P_WALLET, P_EDGE, P_RECUR, P_RESET],
    vi_challenges={
        "apx-m19-fix-lastchar": vi_challenge(
            "Chẩn đoán 1: crash biên",
            "Phân loại lỗi (lớp nào trong phân loại?), rồi sửa `lastChar` "
            "để trả mã ký tự CUỐI. Đầu vào rỗng không thuộc phạm vi bài "
            "này (s khác rỗng).",
            [("repaired boundary", "Lớp 1/6 (chỉ số lệch một): length() là một vị trí sau cuối; dùng length() - 1.")],
        ),
        "apx-m19-fix-total": vi_challenge(
            "Chẩn đoán 2: bộ tích lũy ngược",
            "Phân loại lỗi, rồi sửa `total` để trả tổng mảng (rỗng → 0).",
            [("repaired accumulator", "Lớp 4 (phép tích lũy sai): -= phải thành +=.")],
        ),
        "apx-m19-fix-wallet": vi_challenge(
            "Chẩn đoán 4: constructor bị bóng che",
            "Phân loại lỗi, rồi sửa lớp `Wallet` để new Wallet(500) báo số "
            "dư 500.",
            [("repaired constructor", "Lớp 9 (lỗi constructor): cents = cents gán tham số cho chính nó; this.cents = cents.")],
        ),
        "apx-m19-fix-firstchar": vi_challenge(
            "Chẩn đoán 6: thiếu trường hợp biên",
            "Phân loại lỗi, rồi sửa `firstChar` để trả mã ký tự đầu tiên, "
            "hoặc -1 cho chuỗi RỖNG.",
            [("repaired edge", "Lớp 13 (thiếu biên): chặn s.length() == 0 trước charAt(0).")],
        ),
        "apx-m19-fix-countdown": vi_challenge(
            "Chẩn đoán 5: đệ quy không tiến triển",
            "Phân loại lỗi, rồi sửa `countDown` để trả số đếm từ n xuống 0 "
            "gồm cả hai đầu (countDown(3) → 4).",
            [("repaired recursion", "Lớp 12 (đệ quy, không tiến triển): countDown(n) phải gọi countDown(n - 1) và cộng 1.")],
        ),
        "apx-m19-fix-reset": vi_challenge(
            "Chẩn đoán 3: bộ đếm không reset",
            "Phân loại lỗi, rồi sửa `longestRun` để trả run dài nhất gồm "
            "các giá trị liền kề bằng nhau. (Gợi ý: cả hai nhánh đều tăng — "
            "một nhánh không nên tăng.)",
            [("repaired run", "Lớp 5 (trạng thái không reset): nhánh else phải đặt cur về 1, không phải tăng.")],
        ),
    },
    solutions=[
        ("apx-m19-fix-lastchar", r"""public class Solution {
    public static int lastChar(String s) {
        return s.charAt(s.length() - 1);
    }
}
""", r"""public class Solution {
    // still broken: length() is past the end
    public static int lastChar(String s) {
        return s.charAt(s.length());
    }
}
"""),
        ("apx-m19-fix-total", r"""public class Solution {
    public static int total(int[] arr) {
        int sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }
}
""", r"""public class Solution {
    // still broken: subtracts
    public static int total(int[] arr) {
        int sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum -= arr[i];
        }
        return sum;
    }
}
"""),
        ("apx-m19-fix-wallet", r"""public class Solution {
    public static class Wallet {
        private int cents;

        public Wallet(int cents) {
            this.cents = cents;
        }

        public int balance() {
            return cents;
        }
    }
}
""", r"""public class Solution {
    public static class Wallet {
        private int cents;

        public Wallet(int cents) {
            // still broken: shadowed
            cents = cents;
        }

        public int balance() {
            return cents;
        }
    }
}
"""),
        ("apx-m19-fix-firstchar", r"""public class Solution {
    public static int firstChar(String s) {
        if (s.length() == 0) {
            return -1;
        }
        return s.charAt(0);
    }
}
""", r"""public class Solution {
    // still broken: no empty guard
    public static int firstChar(String s) {
        return s.charAt(0);
    }
}
"""),
        ("apx-m19-fix-countdown", r"""public class Solution {
    public static int countDown(int n) {
        if (n < 0) {
            return 0;
        }
        return 1 + countDown(n - 1);
    }
}
""", r"""public class Solution {
    // still broken: no progress
    public static int countDown(int n) {
        if (n < 0) {
            return 0;
        }
        return countDown(n);
    }
}
"""),
        ("apx-m19-fix-reset", r"""public class Solution {
    public static int longestRun(int[] arr) {
        int best = 0;
        int cur = 0;
        for (int i = 0; i < arr.length; i++) {
            if (i > 0 && arr[i] == arr[i - 1]) {
                cur++;
            } else {
                cur = 1;
            }
            if (cur > best) {
                best = cur;
            }
        }
        return best;
    }
}
""", r"""public class Solution {
    // still broken: both branches increment
    public static int longestRun(int[] arr) {
        int best = 0;
        int cur = 0;
        for (int i = 0; i < arr.length; i++) {
            if (i > 0 && arr[i] == arr[i - 1]) {
                cur++;
            } else {
                cur++;
            }
            if (cur > best) {
                best = cur;
            }
        }
        return best;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m19", "Checkpoint: two bugs, one repair",
    "Compound diagnosis: a mutation-scan skip AND an uncounted removal.",
    25,
    r"""
Compound bugs are the exam's debugging finale: two classes
interacting. Fix the mechanical one first (the backward loop) and
the symptom usually reveals the second (the counter that never
incremented). Then run the family: adjacent duplicates in the
input are the sibling cases here.
""",
    "Điểm kiểm tra: hai lỗi, một bản sửa",
    "Chẩn đoán kép: bỏ sót quét-biến-đổi VÀ xóa không đếm.",
    r"""
Lỗi kép là màn cuối gỡ lỗi của đề thi: hai lớp tương tác. Sửa lỗi cơ
học trước (vòng ngược) và triệu chứng thường phơi bày lỗi thứ hai
(bộ đếm không bao giờ tăng). Rồi chạy cả họ: các bản sao liền kề
trong đầu vào là các trường hợp anh em ở đây.
""",
    CP19,
    VI_CP19,
    solution=r"""public class Solution {
    public static int removeAll(java.util.ArrayList<String> list, String target) {
        int removed = 0;
        for (int i = list.size() - 1; i >= 0; i--) {
            if (list.get(i).equals(target)) {
                list.remove(i);
                removed++;
            }
        }
        return removed;
    }
}
""",
    wrong=r"""public class Solution {
    // still broken: forward skip, no counting
    public static int removeAll(java.util.ArrayList<String> list, String target) {
        int removed = 0;
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).equals(target)) {
                list.remove(i);
            }
        }
        return removed;
    }
}
""",
)

print("M19 done")
