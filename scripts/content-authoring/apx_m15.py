#!/usr/bin/env python3
"""AP CSA Advanced M15 — FRQ debugging (subtle bugs the learner must fix)."""
from apx import *

M = "apx-frq-debug"

write_module(
    M,
    "FRQ Debugging",
    "Broken FRQ solutions: locate the failure, explain it, fix it, and re-test. Subtle errors only. Difficulty E4–E5.",
    "Gỡ lỗi FRQ",
    "Các lời giải FRQ bị hỏng: định vị lỗi, giải thích, sửa, và kiểm thử lại. Chỉ nhận lỗi tinh vi. Độ khó E4–E5.",
    lessons=["apx-m15-diagnose", "apx-m15-fix", "apx-m15-regress", "apx-cp-m15"],
    practices=["apx-p15-debug"],
)

L1 = r"""
**Debugging is a diff against intention.** The broken method was
written by someone competent; the bug is ONE decision, and the
symptom usually appears far from the cause. The exam-style
procedure:

1. **Read the spec first, the code second.** The bug is always
   "code does X, spec says Y" — you cannot see the diff without
   both sides.
2. **Pick the cheapest failing case** from the examples. Trace it
   by hand through the code — not the spec, the CODE.
3. **Locate the first line where trace and spec disagree.** That
   line is the bug; everything after it is consequence.
4. **Name the bug class** before fixing: boundary, wrong
   accumulator, inverted condition, missing reset, wrong tie-break.
   Naming prevents the "fixed it by accident" failure.

The classic subtle bugs, ranked by exam frequency: off-by-one loop
bounds, `<` where the spec said `<=`, forgetting to reset a
run-counter, `>=` where a tie-break demanded `>`, and mutating
while iterating forward.
"""

L2 = r"""
**Fix discipline.** When you find the line, the fix is usually one
token — but three rules keep the fix honest:

- **Fix the cause, not the symptom.** If the streak counter never
  resets, the bug is the missing `else` — not a clamping `if`
  stapled at the end. Symptom fixes pass the given example and
  fail the hidden ones.
- **Re-run the WHOLE test set, not just the failing case.** A fix
  that repairs case 3 and breaks case 1 traded one bug for
  another. The graded challenges here re-run everything.
- **Say the one-sentence correction**: "the loop must run while
  `i + k <= length`, not `i + k < length`." If you cannot say the
  sentence, you have not found the bug — you have found a
  symptom.

This module's broken solutions each hide exactly one bug; your
fixed version must pass ALL tests including the boundary ones the
original author forgot.
"""

L3 = r"""
**Regression thinking.** After the fix, add the failing case to
your mental suite and ask: *what OTHER input would this same bug
corrupt?* A missing reset corrupts every multi-streak input, not
just the one shown. That habit turns one bug into a family
inspection — and on the exam, it double-checks your fix for free.

**Reading broken code fast**: the bug hides where the code looks
*too* smooth. Real breaks are loud (`<=` next to a comment about
"before the end"); compensations are quiet. Trace the failing
example, and when your hand-drawn trace disagrees with the code's
actual branches, you have found it. Never debug by re-reading
without a concrete failing input on paper — the exam's debugging
MCQs are exactly this skill at 90 seconds each.
"""

VI_L1 = r"""
**Gỡ lỗi là so khớp với ý định.** Phương thức hỏng được viết bởi
một người có năng lực; lỗi là MỘT quyết định, và triệu chứng thường
xuất hiện xa nguyên nhân. Quy trình kiểu đề thi:

1. **Đọc đặc tả trước, mã sau.** Lỗi luôn là "mã làm X, đặc tả nói
   Y" — không thấy được phép so khớp nếu thiếu một trong hai phía.
2. **Chọn trường hợp hỏng rẻ nhất** từ các ví dụ. Truy vết nó bằng
   tay xuyên qua mã — không phải đặc tả, mà là MÃ.
3. **Định vị dòng đầu tiên mà truy vết và đặc tả bất đồng.** Dòng đó
   là lỗi; mọi thứ sau nó là hậu quả.
4. **Gọi tên lớp lỗi** trước khi sửa: biên, bộ tích lũy sai, điều
   kiện đảo, thiếu reset, phá hòa sai. Việc gọi tên ngăn chặn thất
   bại "sửa trúng theo tình cờ".

Các lỗi tinh vi kinh điển, xếp theo tần suất trong đề thi: biên vòng
lặp lệch-một, `<` nơi đặc tả nói `<=`, quên reset bộ đếm run, `>=`
nơi luật phá hòa đòi `>`, và biến đổi khi đang duyệt tới.
"""

VI_L2 = r"""
**Kỷ luật sửa lỗi.** Khi tìm ra dòng lỗi, bản sửa thường chỉ một ký
tự — nhưng ba luật giữ cho bản sửa trung thực:

- **Sửa nguyên nhân, không phải triệu chứng.** Nếu bộ đếm run không
  bao giờ được reset, lỗi là thiếu `else` — không phải một `if`
  kẹp-trần ghép vào cuối. Bản sửa triệu chứng qua ví dụ cho trước và
  trượt các test ẩn.
- **Chạy lại TOÀN BỘ bộ test, không chỉ trường hợp hỏng.** Một bản
  sửa cứu được ca 3 mà phá ca 1 là đổi một lỗi lấy một lỗi khác. Các
  bài được chấm ở đây chạy lại tất cả.
- **Nêu câu sửa một câu**: "vòng lặp phải chạy khi `i + k <= độ
  dài`, không phải `i + k < độ dài`." Nếu không nói được câu đó,
  bạn chưa tìm ra lỗi — bạn mới tìm ra một triệu chứng.

Các lời giải hỏng trong module này mỗi cái giấu đúng một lỗi; bản sửa
của bạn phải qua TẤT CẢ các test, kể cả các test biên mà tác giả gốc
quên.
"""

VI_L3 = r"""
**Tư duy hồi quy.** Sau khi sửa, thêm trường hợp hỏng vào bộ test
tâm trí và hỏi: *đầu vào NÀO KHÁC lỗi tương tự này sẽ làm hỏng?* Một
reset bị thiếu làm hỏng mọi đầu vào đa-chuỗi, không chỉ ví dụ được
đưa ra. Thói quen đó biến một lỗi thành một lần soát cả họ — và
trong phòng thi, nó kiểm tra chéo bản sửa của bạn miễn phí.

**Đọc mã hỏng nhanh**: lỗi ẩn nơi mã trông *quá* mượt. Vết nứt thật
phát ra tiếng động lớn (`<=` cạnh chú thích "trước khi kết thúc");
các khoản bù thì lặng lẽ. Truy vết ví dụ hỏng, và khi truy vết trên
giấy bất đồng với các nhánh thật của mã, bạn đã tìm ra nó. Không bao
giờ gỡ lỗi bằng cách đọc lại mà không có đầu vào hỏng cụ thể trên
giấy — trắc nghiệm gỡ lỗi của đề thi chính là kỹ năng này ở tốc độ
90 giây mỗi câu.
"""

BOILER_SUM = r"""public class Solution {
    // SPEC: return the sum of elements at EVEN indexes (0, 2, 4, ...)
    public static int sumEvenIndexes(int[] arr) {
        int sum = 0;
        for (int i = 1; i < arr.length; i += 2) {
            sum += arr[i];
        }
        return sum;
    }
}
"""

BOILER_STREAK = r"""public class Solution {
    // SPEC: return the length of the longest run of equal adjacent values
    public static int longestRun(int[] arr) {
        if (arr.length == 0) {
            return 0;
        }
        int best = 1;
        int cur = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] == arr[i - 1]) {
                cur++;
                if (cur > best) {
                    best = cur;
                }
            }
        }
        return best;
    }
}
"""

BOILER_LAST = r"""public class Solution {
    // SPEC: return the LAST index where target appears, or -1
    public static int lastIndex(int[] arr, int target) {
        for (int i = arr.length - 1; i >= 0; i--) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
}
"""

BOILER_STUDENT = r"""public class Solution {
    // SPEC: remove every failing score (< 60), keep order, return how many removed
    public static int removeFailing(java.util.ArrayList<Integer> scores) {
        int removed = 0;
        for (int i = 0; i < scores.size(); i++) {
            if (scores.get(i) < 60) {
                scores.remove(i);
                removed++;
            }
        }
        return removed;
    }
}
"""

P_SUM = challenge(
    "apx-m15-fix-sum",
    "Fix: even-index sum",
    "The method should sum elements at **even indexes** (0, 2, 4, …). "
    "It fails. Find the bug, fix it in place, and keep the method "
    "signature.\n\nThe buggy line is visible in the starter code.",
    BOILER_SUM,
    [(
        "corrected sum",
        r"""
CjTestBase.checkEq(Solution.sumEvenIndexes(new int[]{10, 20, 30, 40}), 40, "indexes 0 and 2");
CjTestBase.checkEq(Solution.sumEvenIndexes(new int[]{5}), 5, "single element at index 0");
CjTestBase.checkEq(Solution.sumEvenIndexes(new int[]{}), 0, "empty");
""",
        "The loop starts at 1 with step 2 — it sums the ODD indexes; start at 0.",
    )],
    level="debugging",
    difficulty="advanced",
)

P_RUN = challenge(
    "apx-m15-fix-run",
    "Fix: longest run counter",
    "The method should return the length of the **longest run of "
    "equal adjacent values**. Example failure: `{1, 2, 2, 3, 3, 3, "
    "1}` returns 3 (correct) but `{2, 2, 1, 1}` returns 3 (wrong — "
    "should be 2). Find and fix the bug.",
    BOILER_STREAK,
    [(
        "corrected runs",
        r"""
CjTestBase.checkEq(Solution.longestRun(new int[]{1, 2, 2, 3, 3, 3, 1}), 3, "triple run");
CjTestBase.checkEq(Solution.longestRun(new int[]{2, 2, 1, 1}), 2, "two runs of two");
CjTestBase.checkEq(Solution.longestRun(new int[]{7}), 1, "single element");
CjTestBase.checkEq(Solution.longestRun(new int[]{}), 0, "empty");
""",
        "The counter never RESETS when the run breaks — add the else branch resetting cur to 1.",
    )],
    level="debugging",
    difficulty="advanced",
)

P_LAST = challenge(
    "apx-m15-fix-last",
    "Fix: last-index search",
    "The method should return the **last** index where target "
    "appears, or -1. It sometimes returns -1 even when the target is "
    "present late in the array. Find and fix the bug.",
    BOILER_LAST,
    [(
        "corrected search",
        r"""
CjTestBase.checkEq(Solution.lastIndex(new int[]{4, 2, 4, 2, 9}, 4), 2, "last 4");
CjTestBase.checkEq(Solution.lastIndex(new int[]{4, 2, 9}, 4), 0, "only at index 0");
CjTestBase.checkEq(Solution.lastIndex(new int[]{4, 2, 4, 2, 9}, 2), 3, "last 2");
CjTestBase.checkEq(Solution.lastIndex(new int[]{1, 2}, 3), -1, "absent");
CjTestBase.checkEq(Solution.lastIndex(new int[]{}, 5), -1, "empty");
""",
        "The backward loop bound is wrong — i must be able to reach index 0 (use i >= 0, or fix the start).",
    )],
    level="debugging",
    difficulty="advanced",
)

P_REMOVE = challenge(
    "apx-m15-fix-remove",
    "Fix: the removal skip",
    "The method should remove every score below 60, keep survivor "
    "order, and return the removal count. It silently skips some "
    "failing scores. Find and fix the bug.",
    BOILER_STUDENT,
    [(
        "corrected removal",
        r"""
java.util.ArrayList<Integer> l = new java.util.ArrayList<>(java.util.List.of(70, 50, 55, 80, 40));
CjTestBase.checkEq(Solution.removeFailing(l), 3, "three removed");
CjTestBase.checkEq(l, new java.util.ArrayList<>(java.util.List.of(70, 80)), "survivors in order");
java.util.ArrayList<Integer> none = new java.util.ArrayList<>(java.util.List.of(90));
CjTestBase.checkEq(Solution.removeFailing(none), 0, "nothing to remove");
""",
        "Forward removal skips the element sliding into the freed slot — iterate BACKWARD (i from size-1 down to 0).",
    )],
    level="debugging",
    difficulty="advanced",
)

CP15 = challenge(
    "apx-cp-m15-window",
    "Checkpoint: fix the window sum",
    "The method should return the **largest sum of any k consecutive "
    "elements** (k >= 1, array longer than k). It returns wrong "
    "values whenever the best window touches the array's end. Find "
    "and fix the bug.",
    r"""public class Solution {
    // SPEC: largest sum of any k consecutive elements
    public static int maxWindowSum(int[] arr, int k) {
        int best = Integer.MIN_VALUE;
        for (int i = 0; i + k < arr.length; i++) {
            int sum = 0;
            for (int j = i; j < i + k; j++) {
                sum += arr[j];
            }
            if (sum > best) {
                best = sum;
            }
        }
        return best;
    }
}
""",
    [(
        "corrected window",
        r"""
CjTestBase.checkEq(Solution.maxWindowSum(new int[]{2, 1, 5, 1, 3, 2}, 3), 9, "1+5+3");
CjTestBase.checkEq(Solution.maxWindowSum(new int[]{1, 2}, 2), 3, "window == length");
CjTestBase.checkEq(Solution.maxWindowSum(new int[]{-5, -1, -8}, 2), -6, "negatives");
""",
        "The loop condition drops the final window: i + k <= arr.length is required.",
    )],
    level="debugging",
    difficulty="advanced",
)

VI_CP15 = vi_challenge(
    "Điểm kiểm tra: sửa tổng cửa sổ",
    "Phương thức nên trả **tổng lớn nhất của k phần tử liên tiếp bất "
    "kỳ** (k ≥ 1, mảng dài hơn k). Nó trả giá trị sai mỗi khi cửa sổ "
    "tốt nhất chạm cuối mảng. Tìm và sửa lỗi.",
    [("corrected window", "Điều kiện vòng lặp đánh rơi cửa sổ cuối: cần i + k <= độ dài mảng.")],
)

write_practice(
    M, "apx-p15-debug", "Debug gauntlet: one bug each",
    "Four broken methods with single subtle bugs; diagnose, name, fix.",
    "Võ đài gỡ lỗi: mỗi bài một lỗi",
    "Bốn phương thức hỏng với một lỗi tinh vi mỗi bài; chẩn đoán, gọi tên, sửa.",
    after_lesson="apx-m15-fix", minutes=55, difficulty="advanced",
    challenges=[P_SUM, P_RUN, P_LAST, P_REMOVE],
    vi_challenges={
        "apx-m15-fix-sum": vi_challenge(
            "Sửa: tổng chỉ số chẵn",
            "Phương thức nên cộng các phần tử ở **chỉ số chẵn** (0, 2, 4, …). "
            "Nó chạy sai. Tìm lỗi, sửa tại chỗ, giữ nguyên chữ ký.\n\nDòng "
            "lỗi hiện rõ trong mã khởi đầu.",
            [("corrected sum", "Vòng lặp bắt đầu ở 1 với bước 2 — nó cộng chỉ số LẺ; phải bắt đầu ở 0.")],
        ),
        "apx-m15-fix-run": vi_challenge(
            "Sửa: bộ đếm run dài nhất",
            "Phương thức nên trả độ dài **run dài nhất của các giá trị liền "
            "kề bằng nhau**. Lỗi ví dụ: `{1, 2, 2, 3, 3, 3, 1}` trả 3 "
            "(đúng) nhưng `{2, 2, 1, 1}` trả 3 (sai — phải là 2). Tìm và "
            "sửa lỗi.",
            [("corrected runs", "Bộ đếm không bao giờ được RESET khi run đứt — thêm nhánh else đặt cur về 1.")],
        ),
        "apx-m15-fix-last": vi_challenge(
            "Sửa: tìm kiếm chỉ số cuối",
            "Phương thức nên trả **chỉ số cuối** nơi target xuất hiện, hoặc "
            "-1. Đôi khi nó trả -1 dù target có mặt cuối mảng. Tìm và sửa "
            "lỗi.",
            [("corrected search", "Biên vòng lặp ngược sai — i phải chạm được chỉ số 0 (dùng i >= 0, hoặc sửa điểm bắt đầu).")],
        ),
        "apx-m15-fix-remove": vi_challenge(
            "Sửa: lỗi bỏ sót khi xóa",
            "Phương thức nên xóa mọi điểm dưới 60, giữ thứ tự phần còn lại, "
            "và trả số lần xóa. Nó lặng lẽ bỏ sót vài điểm liệt. Tìm và sửa "
            "lỗi.",
            [("corrected removal", "Xóa khi duyệt tới bỏ sót phần tử trượt vào ô vừa trống — duyệt NGƯỢC (i từ size-1 về 0).")],
        ),
    },
    solutions=[
        ("apx-m15-fix-sum", r"""public class Solution {
    public static int sumEvenIndexes(int[] arr) {
        int sum = 0;
        for (int i = 0; i < arr.length; i += 2) {
            sum += arr[i];
        }
        return sum;
    }
}
""", r"""public class Solution {
    // still broken: starts at 1 (odd indexes)
    public static int sumEvenIndexes(int[] arr) {
        int sum = 0;
        for (int i = 1; i < arr.length; i += 2) {
            sum += arr[i];
        }
        return sum;
    }
}
"""),
        ("apx-m15-fix-run", r"""public class Solution {
    public static int longestRun(int[] arr) {
        if (arr.length == 0) {
            return 0;
        }
        int best = 1;
        int cur = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] == arr[i - 1]) {
                cur++;
                if (cur > best) {
                    best = cur;
                }
            } else {
                cur = 1;
            }
        }
        return best;
    }
}
""", r"""public class Solution {
    // still broken: no reset
    public static int longestRun(int[] arr) {
        if (arr.length == 0) {
            return 0;
        }
        int best = 1;
        int cur = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] == arr[i - 1]) {
                cur++;
                if (cur > best) {
                    best = cur;
                }
            }
        }
        return best;
    }
}
"""),
        ("apx-m15-fix-last", r"""public class Solution {
    public static int lastIndex(int[] arr, int target) {
        for (int i = arr.length - 1; i >= 0; i--) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
}
""", r"""public class Solution {
    // still broken: i > 0 skips index 0
    public static int lastIndex(int[] arr, int target) {
        for (int i = arr.length - 1; i > 0; i--) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
}
"""),
        ("apx-m15-fix-remove", r"""public class Solution {
    public static int removeFailing(java.util.ArrayList<Integer> scores) {
        int removed = 0;
        for (int i = scores.size() - 1; i >= 0; i--) {
            if (scores.get(i) < 60) {
                scores.remove(i);
                removed++;
            }
        }
        return removed;
    }
}
""", r"""public class Solution {
    // still broken: forward removal skips
    public static int removeFailing(java.util.ArrayList<Integer> scores) {
        int removed = 0;
        for (int i = 0; i < scores.size(); i++) {
            if (scores.get(i) < 60) {
                scores.remove(i);
                removed++;
            }
        }
        return removed;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m15", "Checkpoint: the window boundary",
    "A boundary bug in the wild: the loop condition must include the final window.",
    25,
    r"""
The starter compiles, passes the example in its author's head, and
fails whenever the best window touches the last element — the
classic `i + k < length` versus `i + k <= length`. Diagnose with
the failing case `k == length` first; it isolates the boundary
immediately.
""",
    "Điểm kiểm tra: biên cửa sổ",
    "Một lỗi biên ngoài thiên nhiên: điều kiện vòng lặp phải gồm cửa sổ cuối.",
    r"""
Mã khởi đầu biên dịch được, qua ví dụ trong đầu tác giả, và sai mỗi
khi cửa sổ tốt nhất chạm phần tử cuối — kinh điển `i + k < độ dài`
so với `i + k <= độ dài`. Chẩn đoán bằng trường hợp `k == độ dài`
trước; nó cô lập biên ngay lập tức.
""",
    CP15,
    VI_CP15,
    solution=r"""public class Solution {
    public static int maxWindowSum(int[] arr, int k) {
        int best = Integer.MIN_VALUE;
        for (int i = 0; i + k <= arr.length; i++) {
            int sum = 0;
            for (int j = i; j < i + k; j++) {
                sum += arr[j];
            }
            if (sum > best) {
                best = sum;
            }
        }
        return best;
    }
}
""",
    wrong=r"""public class Solution {
    // still broken: drops the final window
    public static int maxWindowSum(int[] arr, int k) {
        int best = Integer.MIN_VALUE;
        for (int i = 0; i + k < arr.length; i++) {
            int sum = 0;
            for (int j = i; j < i + k; j++) {
                sum += arr[j];
            }
            if (sum > best) {
                best = sum;
            }
        }
        return best;
    }
}
""",
)

print("M15 done")
