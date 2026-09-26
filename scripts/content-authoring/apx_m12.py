#!/usr/bin/env python3
"""AP CSA Advanced M12 — Advanced FRQ workshop (multi-part, spec-first)."""
from apx import *

M = "apx-frq-workshop"

write_module(
    M,
    "Advanced FRQ Workshop",
    "Full multi-part FRQ problems: read the spec, plan, implement each part independently, then self-review. Difficulty E4–E5.",
    "Xưởng FRQ nâng cao",
    "Bài FRQ nhiều phần: đọc đặc tả, lập kế hoạch, cài từng phần độc lập, rồi tự REVIEW. Độ khó E4–E5.",
    lessons=["apx-m12-anatomy", "apx-m12-independent", "apx-m12-review", "apx-cp-m12"],
    practices=["apx-p12-frq"],
)

L1 = r"""
A real FRQ is a **story, a data table, and four tasks**. The reading
protocol that earns points:

1. Read the intro ONCE for the setting; read the data table twice.
2. For each part: write the signature first (types from the table),
   then ONE sentence: "given ..., return/build ...".
3. Parts are **independent**: part (b) never needs your part (a) to
   be correct, and graders score each part separately. A botched
   (a) must not cascade — that discipline is trainable, and module
   16 drills it.
4. **Preconditions are gifts**: "the array is non-empty," "values
   are sorted" — each one deletes code you were about to write.

Time discipline: the four FRQs get 90 minutes — about 20 minutes
each with buffer. Writing the signature and one-line plan before
coding is what makes 20 minutes enough.
"""

L2 = r"""
**The weather-station archetype** (this module's workshop problem):
one array of readings, three behaviors. It exercises every
FRQ-Q1 muscle:

- **Count with a condition** (below freezing): one accumulator, one
  comparison. The trap is `<` vs `<=` against 0.0 — the spec's word
  "below" means strict.
- **Longest streak** (warm run): the run-counter pattern with a
  reset. Two state variables (current run, best run) and the reset
  branch are the whole problem.
- **Parallel-array average**: walk indexes (not for-each) because
  two arrays advance together; guard the nothing-matched case so it
  returns 0.0 instead of NaN.

Notice each part reuses a pattern from modules 4–7. The FRQ is not
new material — it is your existing patterns under one story, with
the story trying to confuse you about which pattern applies.
"""

L3 = r"""
**Self-review is a graded skill.** After implementing, run the
five-point check:

1. **Signature fidelity**: return type and parameter types exactly
   as the spec says. Autoboxing slips (int vs double) lose the
   method.
2. **Boundary sweep**: empty input, single element, all-match,
   no-match — trace each through YOUR code, not your intention.
3. **Spec sentence audit**: every sentence maps to a line; any line
   not backed by a sentence is invention to delete.
4. **Variable-name honesty**: a variable named `max` that holds a
   sum is a future bug — rename before submitting.
5. **No dead code**: a loop that runs once, a guard that can never
   fire. Graders see intention through dead code, but you lose
   writing time.

The checkpoint asks for a full three-part implementation: treat it
as a timed rehearsal, 18 minutes on the clock.
"""

VI_L1 = r"""
Một FRQ thật là **một câu chuyện, một bảng dữ liệu, và bốn nhiệm
vụ**. Giao thức đọc để giành điểm:

1. Đọc phần mở MỘT lần cho bối cảnh; đọc bảng dữ liệu hai lần.
2. Với mỗi phần: viết chữ ký trước (kiểu lấy từ bảng), rồi MỘT câu:
   "cho ..., trả về/dựng ...".
3. Các phần **độc lập**: phần (b) không bao giờ cần phần (a) của bạn
   đúng, và người chấm chấm từng phần riêng. Một phần (a) hỏng không
   được phép lan truyền — kỷ luật đó luyện được, và module 16 sẽ rèn.
4. **Điều kiện tiên quyết là quà**: "mảng khác rỗng," "giá trị đã
   sắp" — mỗi câu xóa bớt mã bạn định viết.

Kỷ luật thời gian: bốn FRQ có 90 phút — khoảng 20 phút mỗi câu kèm
dự phòng. Viết chữ ký và kế hoạch một dòng trước khi code là thứ làm
cho 20 phút là đủ.
"""

VI_L2 = r"""
**Nguyên mẫu trạm thời tiết** (bài xưởng của module này): một mảng
số đo, ba hành vi. Nó rèn đủ cơ bắp FRQ-Q1:

- **Đếm với điều kiện** (dưới đóng băng): một bộ tích lũy, một phép
  so sánh. Bẫy là `<` với `<=` quanh 0.0 — từ "dưới" trong đặc tả
  nghĩa là nghiêm ngặt.
- **Chuỗi dài nhất** (lượt ấm): mẫu bộ đếm run với phép reset. Hai
  biến trạng thái (run hiện tại, run tốt nhất) và nhánh reset là toàn
  bộ bài toán.
- **Trung bình mảng song song**: đi theo chỉ số (không for-each) vì
  hai mảng tiến cùng nhau; chặn trường hợp không khớp để trả 0.0
  thay vì NaN.

Chú ý mỗi phần tái dùng một mẫu từ module 4–7. FRQ không có tài liệu
mới — đó là các mẫu hiện có của bạn dưới một câu chuyện, với câu
chuyện cố làm bạn rối xem mẫu nào áp dụng.
"""

VI_L3 = r"""
**Tự REVIEW là một kỹ năng được chấm.** Sau khi cài đặt, chạy kiểm
tra năm điểm:

1. **Chữ ký trung thành**: kiểu trả về và kiểu tham số đúng như đặc
   tả. Trượt autoboxing (int với double) mất cả phương thức.
2. **Quét biên**: đầu vào rỗng, một phần tử, khớp-hết, không-khớp —
   truy vết từng cái qua MÃ của bạn, không phải ý định của bạn.
3. **Kiểm toán câu đặc tả**: mỗi câu ánh xạ một dòng; dòng không có
   câu nào hậu thuẫn là phát minh cần xóa.
4. **Trung thực tên biến**: biến tên `max` mà giữ tổng là lỗi tương
   lai — đổi tên trước khi nộp.
5. **Không mã chết**: vòng lặp chỉ chạy một lần, biến chặn không bao
   giờ bắn. Người chấm nhìn thấy ý định xuyên qua mã chết, nhưng bạn
   mất thời gian viết.

Bài kiểm tra đòi cài đặt đủ ba phần: coi như một buổi diễn tập có giờ,
18 phút trên đồng hồ.
"""

BOILER_TEMP1 = r"""public class Solution {
    public static int belowFreezing(double[] readings) {
        return 0; // replace: count readings strictly below 0.0
    }
}
"""

BOILER_TEMP2 = r"""public class Solution {
    public static int longestWarmStreak(double[] readings) {
        return 0; // replace: longest run of readings strictly above 15.0
    }
}
"""

BOILER_TEMP3 = r"""public class Solution {
    public static double averageForDay(String[] days, double[] temps, String day) {
        return 0.0; // replace: average temp for day; 0.0 if day never appears
    }
}
"""

P_A = challenge(
    "apx-m12-freezing",
    "FRQ (a): below-freezing count",
    "A weather station stores one reading per hour. Part (a): "
    "implement `belowFreezing(double[] readings)` returning the "
    "**count of readings strictly below 0.0**. The array may be "
    "empty (return 0).",
    BOILER_TEMP1,
    [(
        "freezing count",
        r"""
CjTestBase.checkEq(Solution.belowFreezing(new double[]{3.5, -1.0, -2.5, 8.0, -0.5}), 3, "three below");
CjTestBase.checkEq(Solution.belowFreezing(new double[]{}), 0, "empty");
CjTestBase.checkEq(Solution.belowFreezing(new double[]{0.0}), 0, "exactly zero is NOT below");
""",
        "One accumulator; strictly less than 0.0 (0.0 itself does not count).",
    )],
    level="imitation",
    difficulty="intermediate",
)

P_B = challenge(
    "apx-m12-streak",
    "FRQ (b): longest warm streak",
    "Part (b): implement `longestWarmStreak(double[] readings)` "
    "returning the length of the **longest consecutive run** of "
    "readings strictly above 15.0.\n\nExample: "
    "`{20.1, 16.0, 3.0, 18.0, 19.5, 20.0}` → `3` (the final three).",
    BOILER_TEMP2,
    [(
        "warm streak length",
        r"""
CjTestBase.checkEq(Solution.longestWarmStreak(new double[]{20.1, 16.0, 3.0, 18.0, 19.5, 20.0}), 3, "final run");
CjTestBase.checkEq(Solution.longestWarmStreak(new double[]{}), 0, "empty");
CjTestBase.checkEq(Solution.longestWarmStreak(new double[]{15.0}), 0, "exactly 15 is NOT warm");
""",
        "Run counter + best tracker; reset the counter when a reading fails the threshold.",
    )],
    level="independent",
    difficulty="advanced",
)

P_C = challenge(
    "apx-m12-average",
    "FRQ (c): average for a day",
    "Part (c): parallel arrays `days[i]` names the day of "
    "`temps[i]`. Implement `averageForDay(String[] days, double[] "
    "temps, String day)` returning the **average temperature for the "
    "given day**, or 0.0 when the day never appears.\n\nExample: "
    "days {Mon, Tue, Mon}, temps {10.0, 20.0, 30.0}, day \"Mon\" → "
    "`20.0`.",
    BOILER_TEMP3,
    [(
        "parallel average",
        r"""
CjTestBase.checkNear(Solution.averageForDay(new String[]{"Mon", "Tue", "Mon"}, new double[]{10.0, 20.0, 30.0}, "Mon"), 20.0, 0.001, "two Mondays");
CjTestBase.checkEq(Solution.averageForDay(new String[]{"Mon"}, new double[]{10.0}, "Sun"), 0.0, "missing day");
CjTestBase.checkNear(Solution.averageForDay(new String[]{"Fri"}, new double[]{7.5}, "Fri"), 7.5, 0.001, "single match");
""",
        "Index loop (parallel arrays); count matches too — 0 matches returns 0.0 by spec, not division.",
    )],
    level="independent",
    difficulty="advanced",
)

CP12 = challenge(
    "apx-cp-m12-fullfrq",
    "Checkpoint: full FRQ, timed",
    "The complete weather FRQ in one class: `WarmWeek` with\n\n"
    "- field `private double[] readings;`\n"
    "- constructor storing the array\n"
    "- `public int coldHours()` — count of readings < 0.0\n"
    "- `public boolean hasWarmDay()` — true if any reading > 25.0\n"
    "- `public double firstBelow()` — the FIRST reading below 0.0, "
    "or 999.0 if none\n\nImplement the full class.",
    r"""public class Solution {
    public static class WarmWeek {
        public WarmWeek(double[] readings) {
        }

        public int coldHours() {
            return 0;
        }

        public boolean hasWarmDay() {
            return false;
        }

        public double firstBelow() {
            return 999.0;
        }
    }
}
""",
    [(
        "full frq class",
        r"""
Solution.WarmWeek w = new Solution.WarmWeek(new double[]{-2.0, 30.0, -5.0, 10.0});
CjTestBase.checkEq(w.coldHours(), 2, "two cold readings");
CjTestBase.checkTrue(w.hasWarmDay(), "30 is warm");
CjTestBase.checkNear(w.firstBelow(), -2.0, 0.001, "first cold is -2");
Solution.WarmWeek m = new Solution.WarmWeek(new double[]{5.0});
CjTestBase.checkTrue(!m.hasWarmDay(), "no warm day");
CjTestBase.checkNear(m.firstBelow(), 999.0, 0.001, "sentinel when none");
""",
        "Three independent behaviors over one stored array; firstBelow returns early on the first match.",
    )],
    level="mini-build",
    difficulty="advanced",
)

VI_CP12 = vi_challenge(
    "Điểm kiểm tra: FRQ đầy đủ, có giờ",
    "Trọn bộ FRQ thời tiết trong một lớp: `WarmWeek` với\n\n"
    "- trường `private double[] readings;`\n"
    "- constructor lưu mảng\n"
    "- `public int coldHours()` — đếm số đo < 0.0\n"
    "- `public boolean hasWarmDay()` — true nếu có số đo > 25.0\n"
    "- `public double firstBelow()` — số đo dưới 0.0 ĐẦU TIÊN, hoặc "
    "999.0 nếu không có\n\nCài đặt trọn lớp.",
    [("full frq class", "Ba hành vi độc lập trên một mảng đã lưu; firstBelow trả sớm tại khớp đầu tiên.")],
)

write_practice(
    M, "apx-p12-frq", "FRQ workshop: the weather station",
    "Three parts of one FRQ, graded independently — plan first, then implement.",
    "Xưởng FRQ: trạm thời tiết",
    "Ba phần của một FRQ, chấm độc lập — lập kế hoạch trước, rồi cài đặt.",
    after_lesson="apx-m12-independent", minutes=55, difficulty="advanced",
    challenges=[P_A, P_B, P_C],
    vi_challenges={
        "apx-m12-freezing": vi_challenge(
            "FRQ (a): đếm dưới đóng băng",
            "Một trạm thời tiết lưu mỗi số đo một giờ. Phần (a): cài đặt "
            "`belowFreezing(double[] readings)` trả về **số đo nghiêm ngặt "
            "dưới 0.0**. Mảng có thể rỗng (trả 0).",
            [("freezing count", "Một bộ tích lũy; nghiêm ngặt nhỏ hơn 0.0 (bản thân 0.0 không đếm).")],
        ),
        "apx-m12-streak": vi_challenge(
            "FRQ (b): chuỗi ấm dài nhất",
            "Phần (b): cài đặt `longestWarmStreak(double[] readings)` trả về "
            "độ dài **chuỗi liên tiếp dài nhất** các số đo nghiêm ngặt trên "
            "15.0.\n\nVí dụ: `{20.1, 16.0, 3.0, 18.0, 19.5, 20.0}` → `3` "
            "(ba số cuối).",
            [("warm streak length", "Bộ đếm run + bộ ghi best; reset bộ đếm khi số đo phá ngưỡng.")],
        ),
        "apx-m12-average": vi_challenge(
            "FRQ (c): trung bình theo ngày",
            "Phần (c): hai mảng song song `days[i]` cho biết ngày của "
            "`temps[i]`. Cài đặt `averageForDay(String[] days, double[] "
            "temps, String day)` trả **trung bình nhiệt độ của ngày cho "
            "trước**, hoặc 0.0 khi ngày không xuất hiện.\n\nVí dụ: days "
            "{Mon, Tue, Mon}, temps {10.0, 20.0, 30.0}, day \"Mon\" → `20.0`.",
            [("parallel average", "Vòng lặp chỉ số (mảng song song); đếm cả số khớp — 0 khớp trả 0.0 theo đặc tả, không chia.")],
        ),
    },
    solutions=[
        ("apx-m12-freezing", r"""public class Solution {
    public static int belowFreezing(double[] readings) {
        int count = 0;
        for (double v : readings) {
            if (v < 0.0) {
                count++;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: inclusive boundary — 0.0 itself is counted
    public static int belowFreezing(double[] readings) {
        int count = 0;
        for (double v : readings) {
            if (v <= 0.0) {
                count++;
            }
        }
        return count;
    }
}
"""),
        ("apx-m12-streak", r"""public class Solution {
    public static int longestWarmStreak(double[] readings) {
        int best = 0;
        int cur = 0;
        for (double v : readings) {
            if (v > 15.0) {
                cur++;
                if (cur > best) {
                    best = cur;
                }
            } else {
                cur = 0;
            }
        }
        return best;
    }
}
""", r"""public class Solution {
    // BUG: never resets the run counter — streaks from earlier runs accumulate
    public static int longestWarmStreak(double[] readings) {
        int best = 0;
        int cur = 0;
        for (double v : readings) {
            if (v > 15.0) {
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
        ("apx-m12-average", r"""public class Solution {
    public static double averageForDay(String[] days, double[] temps, String day) {
        double sum = 0.0;
        int n = 0;
        for (int i = 0; i < days.length; i++) {
            if (days[i].equals(day)) {
                sum += temps[i];
                n++;
            }
        }
        if (n == 0) {
            return 0.0;
        }
        return sum / n;
    }
}
""", r"""public class Solution {
    // BUG: divides even when nothing matched — NaN for a missing day
    public static double averageForDay(String[] days, double[] temps, String day) {
        double sum = 0.0;
        int n = 0;
        for (int i = 0; i < days.length; i++) {
            if (days[i].equals(day)) {
                sum += temps[i];
                n++;
            }
        }
        return sum / n;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m12", "Checkpoint: the full class",
    "Assemble the stored-array class with three graded behaviors.",
    25,
    r"""
This is the FRQ2 shape at exam weight: store the array once, then
three behaviors that each read it differently — a count, an
existence check, and a first-match scan with a sentinel. Every one
is a pattern you already own; the class is just the frame.
""",
    "Điểm kiểm tra: lớp hoàn chỉnh",
    "Lắp ráp lớp lưu-mảng với ba hành vi được chấm.",
    r"""
Đây là hình dạng FRQ2 với trọng lượng đề thi: lưu mảng một lần, rồi
ba hành vi mỗi cái đọc nó khác nhau — một phép đếm, một kiểm tra tồn
tại, và một lượt quét khớp-đầu-tiên với giá trị thay thế. Mỗi cái là
một mẫu bạn đã có; lớp chỉ là khung.
""",
    CP12,
    VI_CP12,
    solution=r"""public class Solution {
    public static class WarmWeek {
        private double[] readings;

        public WarmWeek(double[] readings) {
            this.readings = readings;
        }

        public int coldHours() {
            int count = 0;
            for (double v : readings) {
                if (v < 0.0) {
                    count++;
                }
            }
            return count;
        }

        public boolean hasWarmDay() {
            for (double v : readings) {
                if (v > 25.0) {
                    return true;
                }
            }
            return false;
        }

        public double firstBelow() {
            for (double v : readings) {
                if (v < 0.0) {
                    return v;
                }
            }
            return 999.0;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class WarmWeek {
        private double[] readings;

        public WarmWeek(double[] readings) {
            this.readings = readings;
        }

        public int coldHours() {
            int count = 0;
            for (double v : readings) {
                if (v < 0.0) {
                    count++;
                }
            }
            return count;
        }

        public boolean hasWarmDay() {
            // BUG: returns after checking only the FIRST element
            if (readings.length > 0) {
                return readings[0] > 25.0;
            }
            return false;
        }

        public double firstBelow() {
            for (double v : readings) {
                if (v < 0.0) {
                    return v;
                }
            }
            return 999.0;
        }
    }
}
""",
)

print("M12 done")
