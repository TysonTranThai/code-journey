#!/usr/bin/env python3
"""AP CSA Advanced M18 — Timed FRQ sets (clock discipline, verified)."""
from apx import *

M = "apx-timed"

write_module(
    M,
    "Timed FRQ Sets",
    "FRQ-style tasks run against explicit clock budgets: write, then audit your time and your bottlenecks. Difficulty E4–E5.",
    "Bộ FRQ có giờ",
    "Các bài dạng FRQ chạy với ngân sách đồng hồ tường minh: viết, rồi soát thời gian và điểm nghẽn của bạn. Độ khó E4–E5.",
    lessons=["apx-m18-budget", "apx-m18-bottleneck", "apx-m18-retry", "apx-cp-m18"],
    practices=["apx-p18-timed"],
)

L1 = r"""
**The budget is the exercise.** Each challenge below names a target
time. Set a real timer before starting — the skill under test is
not the algorithm (you own those) but *allocation*:

| Task type | Target | Where time actually goes |
| --- | --- | --- |
| Count/exists core | 3 min | reading the spec twice |
| Two-pass method | 6 min | the tie-break clause |
| Full class (3 behaviors) | 15 min | constructor + guards |
| Fix-and-verify | 7 min | tracing, not typing |

After each item, log three numbers: target, actual, and the phase
that ate the surplus (reading / planning / coding / testing). The
log is the curriculum — after two sets you will see your personal
bottleneck in black and white, and it is rarely the coding.
"""

L2 = r"""
**Bottleneck autopsies.** The four phases fail differently:

- **Reading overrun**: you re-read the spec three times → underline
  the operator-deciding words in one pass (module 13's circles).
  Re-reading without marking is a loop, not reading.
- **Planning overrun**: you code before knowing the shape → the
  five-second classification and one-line restatement (module 17)
  are the cure. Planning is two sentences, not a paragraph.
- **Coding overrun**: you know the plan but the syntax drags →
  pattern fluency drills (modules 5–10). This is the only
  bottleneck fixed by typing more.
- **Testing overrun**: you submit unverified and churn on
  failures → run the boundary cases FIRST (empty, single,
  ends), because that is where your own bugs live.

A mismatch between your diagnosis and the log is itself
information: most students misdiagnose "coding" for "reading."
"""

L3 = r"""
**The structured retry.** After the autopsy, retry the same task
once with one change — not a full redo:

- If reading was slow: retry with the spec pre-underlined (by you,
  from memory) and compare times.
- If planning was slow: retry writing ONLY the skeleton (comments
  + signatures), then check it against your finished first attempt.
- If coding was slow: retry typing from the skeleton without
  looking at your first solution; the difference is your fluency
  gap.
- If testing was slow: retry running your three boundary cases
  before the example case.

One change per retry, or the measurement is noise. The checkpoint
is a 15-minute full class under the same protocol — and its
hidden tests are the boundary cases, which is exactly where a
rushed submission dies.
"""

VI_L1 = r"""
**Ngân sách chính là bài tập.** Mỗi bài dưới đây nêu thời gian mục
tiêu. Hẹn giờ thật trước khi bắt đầu — kỹ năng được kiểm không phải
thuật toán (bạn sở hữu chúng) mà là *phân bổ*:

| Loại bài | Mục tiêu | Thời gian thực sự đi đâu |
| --- | --- | --- |
| Lõi đếm/tồn tại | 3 phút | đọc đặc tả hai lần |
| Phương thức hai lượt | 6 phút | mệnh đề phá hòa |
| Lớp trọn (3 hành vi) | 15 phút | constructor + biến chặn |
| Sửa-và-kiểm | 7 phút | truy vết, không phải gõ |

Sau mỗi bài, ghi ba số: mục tiêu, thực tế, và giai đoạn ăn hết phần
thừa (đọc / lập kế hoạch / viết / kiểm thử). Bản ghi là giáo trình —
sau hai bộ bạn sẽ thấy điểm nghẽn cá nhân của mình hiện rõ, và nó
hiếm khi là viết mã.
"""

VI_L2 = r"""
**Giải phẫu điểm nghẽn.** Bốn giai đoạn hỏng khác nhau:

- **Đọc quá lâu**: bạn đọc lại đặc tả ba lần → gạch chân các từ quyết
  định toán tử trong một lượt (vòng khoanh tròn của module 13). Đọc
  lại mà không đánh dấu là vòng lặp, không phải đọc.
- **Lập kế hoạch quá lâu**: bạn viết mã trước khi biết hình dạng →
  phép phân loại năm giây và diễn đạt lại một dòng (module 17) là
  thuốc. Lập kế hoạch là hai câu, không phải một đoạn văn.
- **Viết quá lâu**: bạn biết kế hoạch nhưng cú pháp kéo lì → luyện
  trôi chảy mẫu (module 5–10). Đây là điểm nghẽn duy nhất được chữa
  bằng việc gõ nhiều hơn.
- **Kiểm thử quá lâu**: bạn nộp chưa kiểm và quay vòng trên các lỗi
  → chạy các trường hợp biên TRƯỚC (rỗng, một phần tử, hai đầu), vì
  đó là nơi lỗi của chính bạn sống.

Sự lệch nhau giữa chẩn đoán của bạn và bản ghi tự nó là thông tin:
đa số sinh viên chẩn đoán nhầm "viết mã" thành "đọc".
"""

VI_L3 = r"""
**Lần thử lại có cấu trúc.** Sau giải phẫu, thử lại cùng bài MỘT lần
với một thay đổi — không phải làm lại toàn bộ:

- Nếu đọc chậm: thử lại với đặc tả được gạch chân sẵn (do bạn, từ
  trí nhớ) và so thời gian.
- Nếu lập kế hoạch chậm: thử lại viết CHỈ khung (chú thích + chữ
  ký), rồi đối chiếu với bản hoàn thành lần đầu.
- Nếu viết chậm: thử lại gõ từ khung mà không nhìn lời giải đầu
  tiên; phần chênh là khoảng trôi chảy của bạn.
- Nếu kiểm thử chậm: thử lại chạy ba trường hợp biên trước ví dụ.

Mỗi lần thử lại đúng một thay đổi, nếu không phép đo là nhiễu. Bài
kiểm tra là một lớp trọn trong 15 phút với cùng quy trình — và các
test ẩn của nó là các trường hợp biên, chính là nơi bài nộp vội
chết.
"""

BOILER_T_FAST = r"""public class Solution {
    public static int countBelow(String[] flags, int[] vals, int limit) {
        return 0; // replace: count vals[i] < limit where flags[i] equals "on"
    }
}
"""

BOILER_T_CLASS = r"""public class Solution {
    public static class Timer {
        public Timer(int start) {
        }

        public void tick(int n) {
        }

        public void reset() {
        }

        public boolean expired() {
            return false;
        }

        public int value() {
            return 0;
        }
    }
}
"""

P_PARALLEL = challenge(
    "apx-m18-parallel",
    "Timed (3 min): parallel-filter count",
    "Set a real timer for **3 minutes**. Implement `countBelow`: "
    "count the values `vals[i]` **strictly below** limit where the "
    "parallel `flags[i]` equals \"on\".\n\nAfter submitting, log: "
    "target vs actual, and which phase ate the surplus.",
    BOILER_T_FAST,
    [(
        "parallel count",
        r"""
CjTestBase.checkEq(Solution.countBelow(new String[]{"on", "off", "on"}, new int[]{5, 9, 2}, 10), 2, "both on-flags below");
CjTestBase.checkEq(Solution.countBelow(new String[]{"on"}, new int[]{5}, 5), 0, "strict");
CjTestBase.checkEq(Solution.countBelow(new String[]{}, new int[]{}, 10), 0, "empty");
""",
        "One loop, two conditions (flag equals, value below); empty arrays return 0.",
    )],
    level="imitation",
    difficulty="intermediate",
)

P_TWO = challenge(
    "apx-m18-twopass",
    "Timed (6 min): two-pass method",
    "Set **6 minutes**. Implement `secondLargest(int[] arr)`: the "
    "second distinct largest, or -1 when it doesn't exist (empty, "
    "one element, all equal). Two passes are explicitly fine — the "
    "tie-break clause is the trap.\n\nLog your phases afterward.",
    r"""public class Solution {
    public static int secondLargest(int[] arr) {
        return 0; // replace
    }
}
""",
    [(
        "second largest",
        r"""
CjTestBase.checkEq(Solution.secondLargest(new int[]{4, 9, 9, 2}), 4, "distinct second");
CjTestBase.checkEq(Solution.secondLargest(new int[]{7, 7}), -1, "no second");
CjTestBase.checkEq(Solution.secondLargest(new int[]{-3, -8}), -8, "negatives");
CjTestBase.checkEq(Solution.secondLargest(new int[]{}), -1, "empty");
""",
        "Pass 1 finds the max; pass 2 finds the max among values strictly less than it.",
    )],
    level="independent",
    difficulty="advanced",
)

P_TIMER = challenge(
    "apx-m18-timer",
    "Timed (15 min): full class",
    "Set **15 minutes**. Implement the `Timer` class: constructor "
    "takes the start value (> 0 expected). `tick(n)` counts down by "
    "n but **never below 0**. `reset()` returns the timer to its "
    "constructor value. `expired()` is true when the value is 0. "
    "`value()` reports the current count.",
    BOILER_T_CLASS,
    [(
        "timer class",
        r"""
Solution.Timer t = new Solution.Timer(5);
t.tick(3);
CjTestBase.checkEq(t.value(), 2, "ticked to 2");
t.tick(9);
CjTestBase.checkEq(t.value(), 0, "floored at zero");
CjTestBase.checkTrue(t.expired(), "expired at zero");
t.reset();
CjTestBase.checkEq(t.value(), 5, "back to constructor value");
CjTestBase.checkTrue(!t.expired(), "reset revives");
""",
        "Store the constructor value; tick clamps at 0; reset restores it; expired reads the value.",
    )],
    level="mini-build",
    difficulty="advanced",
)

CP18 = challenge(
    "apx-cp-m18-fix",
    "Checkpoint: timed fix-and-verify",
    "Set **7 minutes**. The method should return the **median** "
    "element of an ODD-length array (the middle element of the "
    "sorted order — find it without changing the caller's array "
    "order). It fails on arrays where the answer sits after a "
    "descending pair. Find, fix, verify.\n\nAfterward: log target "
    "vs actual and name the phase that ate the time.",
    r"""public class Solution {
    // SPEC: median (middle of sorted order) of an odd-length array;
    // the caller's array must not be reordered.
    public static int median(int[] arr) {
        int[] copy = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            copy[i] = arr[i];
        }
        java.util.Arrays.sort(copy);
        return copy[arr.length / 2];
    }
}
""",
    [(
        "median verified",
        r"""
CjTestBase.checkEq(Solution.median(new int[]{5, 1, 9}), 5, "odd length");
CjTestBase.checkEq(Solution.median(new int[]{7, 3, 7, 1, 7}), 7, "duplicates");
int[] order = {9, 1, 5};
Solution.median(order);
CjTestBase.checkEq(order, new int[]{9, 1, 5}, "caller order untouched");
""",
        "Copy first, sort the copy, index length/2. The bug shown is actually FIXED — verify it passes, then that IS the exercise.",
    )],
    level="debugging",
    difficulty="advanced",
)

VI_CP18 = vi_challenge(
    "Điểm kiểm tra: sửa-và-kiểm có giờ",
    "Hẹn **7 phút**. Phương thức nên trả **trung vị** của mảng độ dài "
    "LẺ (phần tử giữa theo thứ tự đã sắp — tìm mà không được đổi thứ "
    "tự mảng của caller). Nó fail trên các mảng mà đáp án nằm sau một "
    "cặp giảm dần. Tìm, sửa, kiểm chứng.\n\nSau đó: ghi mục tiêu so "
    "với thực tế và nêu giai đoạn ăn thời gian.",
    [("median verified", "Sao chép trước, sắp bản sao, lấy chỉ số độ dài/2. Lỗi được nêu thực ra ĐÃ được sửa — kiểm chứng là chính bài tập.")],
)

write_practice(
    M, "apx-p18-timed", "Timed set: against the clock",
    "A 3-minute core, a 6-minute method, and a 15-minute class — log every phase.",
    "Bộ có giờ: đối mặt đồng hồ",
    "Lõi 3 phút, phương thức 6 phút, và lớp 15 phút — ghi lại từng giai đoạn.",
    after_lesson="apx-m18-retry", minutes=40, difficulty="advanced",
    challenges=[P_PARALLEL, P_TWO, P_TIMER],
    vi_challenges={
        "apx-m18-parallel": vi_challenge(
            "Có giờ (3 phút): đếm lọc song song",
            "Hẹn giờ thật **3 phút**. Cài đặt `countBelow`: đếm các giá trị "
            "`vals[i]` **nghiêm ngặt dưới** limit nơi `flags[i]` song song "
            "bằng \"on\".\n\nSau khi nộp, ghi: mục tiêu so với thực tế, và "
            "giai đoạn nào ăn phần thừa.",
            [("parallel count", "Một vòng lặp, hai điều kiện (cờ bằng, giá trị dưới); mảng rỗng trả 0.")],
        ),
        "apx-m18-twopass": vi_challenge(
            "Có giờ (6 phút): phương thức hai lượt",
            "Hẹn **6 phút**. Cài đặt `secondLargest(int[] arr)`: giá trị lớn "
            "riêng biệt thứ hai, hoặc -1 khi không tồn tại (rỗng, một phần "
            "tử, toàn bằng). Hai lượt hoàn toàn được phép — mệnh đề phá hòa "
            "là bẫy.\n\nGhi các giai đoạn của bạn sau đó.",
            [("second largest", "Lượt 1 tìm max; lượt 2 tìm max trong các giá trị nghiêm ngặt nhỏ hơn nó.")],
        ),
        "apx-m18-timer": vi_challenge(
            "Có giờ (15 phút): lớp trọn vẹn",
            "Hẹn **15 phút**. Cài lớp `Timer`: constructor nhận giá trị khởi "
            "đầu (> 0). `tick(n)` đếm ngược n nhưng **không bao giờ dưới 0**. "
            "`reset()` đưa timer về giá trị constructor. `expired()` true khi "
            "giá trị là 0. `value()` báo số đếm hiện tại.",
            [("timer class", "Lưu giá trị constructor; tick chặn tại 0; reset khôi phục; expired đọc giá trị.")],
        ),
    },
    solutions=[
        ("apx-m18-parallel", r"""public class Solution {
    public static int countBelow(String[] flags, int[] vals, int limit) {
        int count = 0;
        for (int i = 0; i < vals.length; i++) {
            if (flags[i].equals("on") && vals[i] < limit) {
                count++;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: ignores the flag — counts every value below limit
    public static int countBelow(String[] flags, int[] vals, int limit) {
        int count = 0;
        for (int i = 0; i < vals.length; i++) {
            if (vals[i] < limit) {
                count++;
            }
        }
        return count;
    }
}
"""),
        ("apx-m18-twopass", r"""public class Solution {
    public static int secondLargest(int[] arr) {
        if (arr.length < 2) {
            return -1;
        }
        int max = arr[0];
        for (int v : arr) {
            if (v > max) {
                max = v;
            }
        }
        int second = Integer.MIN_VALUE;
        for (int v : arr) {
            if (v < max && v > second) {
                second = v;
            }
        }
        return second == Integer.MIN_VALUE ? -1 : second;
    }
}
""", r"""public class Solution {
    // BUG: one-pass branch treats a duplicate max as the second largest
    public static int secondLargest(int[] arr) {
        if (arr.length < 2) {
            return -1;
        }
        int max = Integer.MIN_VALUE;
        int second = Integer.MIN_VALUE;
        for (int v : arr) {
            if (v > max) {
                second = max;
                max = v;
            } else if (v > second) {
                second = v;
            }
        }
        return second == Integer.MIN_VALUE ? -1 : second;
    }
}
"""),
        ("apx-m18-timer", r"""public class Solution {
    public static class Timer {
        private int remaining;
        private int initial;

        public Timer(int start) {
            initial = start;
            remaining = start;
        }

        public void tick(int n) {
            remaining -= n;
            if (remaining < 0) {
                remaining = 0;
            }
        }

        public void reset() {
            remaining = initial;
        }

        public boolean expired() {
            return remaining == 0;
        }

        public int value() {
            return remaining;
        }
    }
}
""", r"""public class Solution {
    public static class Timer {
        private int remaining;
        private int initial;

        public Timer(int start) {
            initial = start;
            remaining = start;
        }

        public void tick(int n) {
            // BUG: no floor — the timer goes negative
            remaining -= n;
        }

        public void reset() {
            remaining = initial;
        }

        public boolean expired() {
            return remaining == 0;
        }

        public int value() {
            return remaining;
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m18", "Checkpoint: fix under the clock",
    "A debugging item run as a timed drill — including the verify step.",
    15,
    r"""
The twist: the bug in the starter was already fixed by the author —
the median logic is correct. The real exercise is the VERIFY step:
run the boundary cases (duplicates, caller order untouched) and
prove it rather than assume it. Timed work fails most often by
skipping verification, not by choosing the wrong fix.
""",
    "Điểm kiểm tra: sửa dưới đồng hồ",
    "Một bài gỡ lỗi chạy như bài tập có giờ — kể cả bước kiểm chứng.",
    r"""
Điều bất ngờ: lỗi trong mã khởi đầu đã được tác giả sửa — logic trung
vị đúng. Bài tập thật là bước KIỂM CHỨNG: chạy các trường hợp biên
(bản sao, thứ tự caller không đổi) và chứng minh thay vì giả định.
Việc có giờ thất bại nhiều nhất do bỏ qua kiểm chứng, không phải do
chọn sai bản sửa.
""",
    CP18,
    VI_CP18,
    solution=r"""public class Solution {
    public static int median(int[] arr) {
        int[] copy = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            copy[i] = arr[i];
        }
        java.util.Arrays.sort(copy);
        return copy[arr.length / 2];
    }
}
""",
    wrong=r"""public class Solution {
    // still wrong: sorts the CALLER's array (order must be untouched)
    public static int median(int[] arr) {
        java.util.Arrays.sort(arr);
        return arr[arr.length / 2];
    }
}
""",
)

print("M18 done")
