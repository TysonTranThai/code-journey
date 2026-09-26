#!/usr/bin/env python3
"""AP CSA Advanced M16 — FRQ partial credit strategy (verified)."""
from apx import *

M = "apx-partial"

write_module(
    M,
    "FRQ Partial Credit Strategy",
    "When the full solution stalls: identify the independent parts, bank the easy behavior, isolate cascades. Difficulty E4–E5.",
    "Chiến lược điểm một phần FRQ",
    "Khi lời giải đầy đủ bị kẹt: nhận diện các phần độc lập, giữ phần hành vi dễ, cô lập lan truyền. Độ khó E4–E5.",
    lessons=["apx-m16-parts", "apx-m16-cascade", "apx-m16-banking", "apx-cp-m16"],
    practices=["apx-p16-partial"],
)

L1 = r"""
FRQ parts are scored **independently** — a truth this module turns
into points. If part (b) defeats you, part (c) is still worth full
marks, and each part's rubric row is earned separately. The
strategy when stuck:

1. **Inventory the parts by type.** A count, a search, a sum, a
   boolean check — each is a pattern you own. Write the ones you
   recognize FIRST; never leave a recognizable pattern blank
   because an earlier part stalled you.
2. **Write a plausible partial version** of the hard part rather
   than nothing: a correct base case, a correct loop over the easy
   subset. Genuine partial logic frequently earns rubric rows even
   when the whole behavior is incomplete — but never write
   pseudo-comments; graders score code.
3. **Never let a hard part consume the clock.** Budget: if 8
   minutes pass without a working draft, bank what stands and move.

On the actual exam, consult the current official scoring guidance
for how points are awarded; the structures here teach you to make
any rubric's independence work for you.
"""

L2 = r"""
**Cascading errors are self-inflicted.** They happen when one
part's code is *reused wrongly* by another — part (c) calls your
broken part (a) and inherits the failure. The isolation techniques:

- **Prefer self-contained implementations.** When a part can be
  written with its own loop in six lines, do that instead of
  composing a ten-line dependency chain — cross-part reuse saves
  writing time but spreads damage.
- **If the spec REQUIRES calling an earlier method** (some FRQs
  say "you may call methodFromPartA"), call it as specified — but
  test it with a mentally-hand-computed example, since the rubric
  gives the earlier method's correct behavior on demand.
- **Compartment failures**: a null-check missing in part (a)
  should not reach part (c). Guard boundaries between parts as
  if they were teams that cannot see each other's bugs.

The graded exercises here make the isolation concrete: each part
is tested independently, so a bug in one cannot poison another's
score.
"""

L3 = r"""
**Banking behaviors.** Every hard FRQ contains a soft core — a
behavior you can implement correctly in two minutes. Banking it
means: implement it, verify it against the example, and LEAVE it
alone. Resist the urge to refactor toward elegance; partial-credit
time is spent on points, not beauty.

The three bankable cores, in exam-frequency order:

- **The count** (or sum) with one condition — almost every FRQ has
  one.
- **The existence check** — return true the moment a condition
  fires; three lines, one early return.
- **The single pass with an early sentinel** — first-match with a
  default return at the end.

When the checkpoint asks for the full class, bank `coldHours()`
first, then `hasWarmDay()`, and only then attempt `firstBelow()`.
If the clock runs out mid-`firstBelow`, you still banked two of
three — the exam version of never losing the whole game.
"""

VI_L1 = r"""
Các phần FRQ được chấm **độc lập** — một sự thật mà module này biến
thành điểm. Nếu phần (b) đánh bại bạn, phần (c) vẫn đáng điểm tối
đa, và mỗi dòng bảng điểm của từng phần được giành riêng biệt. Chiến
lược khi bị kẹt:

1. **Kiểm kê các phần theo loại.** Một phép đếm, một phép tìm, một
   tổng, một kiểm tra boolean — mỗi cái là một mẫu bạn sở hữu. Viết
   những cái bạn nhận ra TRƯỚC; không bao giờ bỏ trống một mẫu quen
   thuộc chỉ vì một phần trước đó làm bạn kẹt.
2. **Viết phiên bản một phần hợp lý** của phần khó thay vì bỏ
   trắng: một trường hợp cơ sở đúng, một vòng lặp đúng trên tập dễ.
   Logic một phần chân thường vẫn giành được các dòng bảng điểm kể
   cả khi hành vi trọn vẹn chưa xong — nhưng đừng bao giờ viết giả
   chú thích; người chấm chấm mã.
3. **Không bao giờ để phần khó ngốn đồng hồ.** Ngân sách: nếu 8
   phút trôi qua mà chưa có bản nháp chạy được, giữ những gì đang có
   và đi tiếp.

Trong phòng thi thật, hãy tra cứu hướng dẫn chấm chính thức hiện
hành để biết điểm được trao thế nào; các cấu trúc ở đây dạy bạn biến
sự độc lập của bất kỳ bảng điểm nào thành lợi thế của mình.
"""

VI_L2 = r"""
**Lỗi lan truyền là tự gây ra.** Chúng xảy ra khi mã của một phần
*được dùng sai* bởi phần khác — phần (c) gọi phần (a) hỏng của bạn
và thừa hưởng thất bại. Các kỹ thuật cô lập:

- **Ưu tiên cài đặt tự chứa.** Khi một phần có thể viết bằng vòng
  lặp riêng của nó trong sáu dòng, hãy làm thế thay vì dựng chuỗi
  phụ thuộc mười dòng — tái sử dụng giữa các phần tiết kiệm thời
  gian viết nhưng lan truyền thiệt hại.
- **Nếu đặc tả BẮT BUỘC gọi phương thức phần trước** (một số FRQ
  nói "bạn được phép gọi methodFromPartA"), hãy gọi đúng như quy
  định — nhưng kiểm nó với một ví dụ tính tay trong đầu, vì bảng
  điểm cho hành vi đúng của phương thức trước theo yêu cầu.
- **Cách ly thất bại**: thiếu một kiểm tra null ở phần (a) không
  được phép chạm tới phần (c). Chặn biên giữa các phần như thể chúng
  là những đội không nhìn thấy lỗi của nhau.

Các bài được chấm ở đây làm cho sự cô lập trở nên cụ thể: mỗi phần
được kiểm độc lập, nên lỗi của phần này không thể đầu độc điểm của
phần khác.
"""

VI_L3 = r"""
**Giữ các hành vi dễ.** Mọi FRQ khó đều chứa một lõi mềm — một hành
vi bạn cài đúng trong hai phút. Giữ nó nghĩa là: cài đặt, đối chiếu
với ví dụ, và KHÔNG ĐỘNG vào nó nữa. Cưỡng lại cám dỗ tinh chỉnh cho
đẹp; thời gian điểm-một-phần dùng cho điểm, không phải cho cái đẹp.

Ba lõi dễ giữ, theo thứ tự tần suất trong đề:

- **Phép đếm** (hoặc tổng) với một điều kiện — hầu như FRQ nào cũng
  có một cái.
- **Kiểm tra tồn tại** — trả true ngay khi điều kiện bắn; ba dòng,
  một lệnh trả sớm.
- **Một lượt duyệt với sentinel sớm** — khớp-đầu-tiên với giá trị
  mặc định ở cuối.

Khi bài kiểm tra đòi lớp trọn vẹn, giữ `coldHours()` trước, rồi
`hasWarmDay()`, và chỉ sau đó mới thử `firstBelow()`. Nếu đồng hồ
hết khi đang giữa `firstBelow`, bạn vẫn giữ được hai trong ba —
phiên bản phòng thi của việc không bao giờ thua cả ván.
"""

BOILER_BANK1 = r"""public class Solution {
    public static int bankCount(double[] readings, double limit) {
        return 0; // replace: count readings strictly below limit
    }
}
"""

BOILER_BANK2 = r"""public class Solution {
    public static boolean bankExists(double[] readings, double limit) {
        return false; // replace: true if any reading exceeds limit
    }
}
"""

BOILER_BANK3 = r"""public class Solution {
    public static double bankFirst(double[] readings, double limit) {
        return 999.0; // replace: first reading below limit, or 999.0
    }
}
"""

BOILER_FULL = r"""public class Solution {
    public static class ReadingSet {
        public ReadingSet(double[] readings) {
        }

        public int countCold() {
            return 0;
        }

        public boolean anyWarm() {
            return false;
        }

        public double firstCold() {
            return 999.0;
        }
    }
}
"""

P_COUNT = challenge(
    "apx-m16-count",
    "Bankable part 1: the count",
    "The two-minute core: `bankCount(double[] readings, double "
    "limit)` returns how many readings are **strictly below** "
    "limit. Empty array returns 0.",
    BOILER_BANK1,
    [(
        "count core",
        r"""
CjTestBase.checkEq(Solution.bankCount(new double[]{-3.0, 5.0, -1.0}, 0.0), 2, "two below");
CjTestBase.checkEq(Solution.bankCount(new double[]{}, 0.0), 0, "empty");
CjTestBase.checkEq(Solution.bankCount(new double[]{0.0}, 0.0), 0, "strict");
""",
        "One accumulator, one strict comparison. Bank it and move on.",
    )],
    level="imitation",
    difficulty="intermediate",
)

P_EXISTS = challenge(
    "apx-m16-exists",
    "Bankable part 2: the existence check",
    "`bankExists(double[] readings, double limit)` returns true the "
    "moment any reading is **strictly above** limit; false "
    "otherwise. Early return required.",
    BOILER_BANK2,
    [(
        "existence core",
        r"""
CjTestBase.checkTrue(Solution.bankExists(new double[]{1.0, 30.0}, 25.0), "30 exceeds");
CjTestBase.checkTrue(Solution.bankExists(new double[]{30.0, 1.0}, 25.0), "early exceed still counts");
CjTestBase.checkTrue(!Solution.bankExists(new double[]{1.0, 2.0}, 25.0), "none exceed");
CjTestBase.checkTrue(!Solution.bankExists(new double[]{}, 25.0), "empty");
""",
        "for + if + return true; return false after the loop. Three lines of points.",
    )],
    level="imitation",
    difficulty="intermediate",
)

P_FIRST = challenge(
    "apx-m16-first",
    "Bankable part 3: first match with sentinel",
    "`bankFirst(double[] readings, double limit)` returns the "
    "**first** reading strictly below limit, or 999.0 when there is "
    "none.",
    BOILER_BANK3,
    [(
        "first-match core",
        r"""
CjTestBase.checkNear(Solution.bankFirst(new double[]{4.0, -2.0, -8.0}, 0.0), -2.0, 0.001, "first below");
CjTestBase.checkNear(Solution.bankFirst(new double[]{4.0, 6.0}, 0.0), 999.0, 0.001, "sentinel");
CjTestBase.checkNear(Solution.bankFirst(new double[]{}, 0.0), 999.0, 0.001, "empty sentinel");
""",
        "Return inside the loop on the first match; the loop finishing means no match.",
    )],
    level="imitation",
    difficulty="intermediate",
)

CP16 = challenge(
    "apx-cp-m16-set",
    "Checkpoint: bank the easy parts first",
    "The full three-behavior class `ReadingSet` (constructor stores "
    "the array): `countCold()` counts readings < 0.0; `anyWarm()` is "
    "true when any reading > 25.0; `firstCold()` returns the first "
    "reading < 0.0 or 999.0. **Strategy exercise**: implement them "
    "in banking order — count, exists, first-match — as if the "
    "clock were running.",
    BOILER_FULL,
    [(
        "banked in order",
        r"""
Solution.ReadingSet s = new Solution.ReadingSet(new double[]{-2.0, 30.0, -5.0});
CjTestBase.checkEq(s.countCold(), 2, "bank 1");
CjTestBase.checkTrue(s.anyWarm(), "bank 2");
CjTestBase.checkNear(s.firstCold(), -2.0, 0.001, "bank 3");
Solution.ReadingSet cold = new Solution.ReadingSet(new double[]{-1.0, -4.0});
CjTestBase.checkTrue(!cold.anyWarm(), "no warm readings");
""",
        "Each behavior is one known pattern; the exercise is doing them in point-maximizing order without gold-plating.",
    )],
    level="mini-build",
    difficulty="advanced",
)

VI_CP16 = vi_challenge(
    "Điểm kiểm tra: giữ phần dễ trước",
    "Lớp ba hành vi `ReadingSet` trọn vẹn (constructor lưu mảng): "
    "`countCold()` đếm số đo < 0.0; `anyWarm()` true khi có số đo > "
    "25.0; `firstCold()` trả số đo đầu tiên < 0.0 hoặc 999.0. **Bài "
    "tập chiến lược**: cài chúng theo thứ tự giữ-điểm — đếm, tồn tại, "
    "khớp-đầu-tiên — như thể đồng hồ đang chạy.",
    [("banked in order", "Mỗi hành vi là một mẫu quen thuộc; bài tập là làm chúng theo thứ tự tối đa hóa điểm mà không thêm thắt.")],
)

write_practice(
    M, "apx-p16-partial", "Partial credit drill",
    "The three bankable cores, then the assembly under simulated time pressure.",
    "Bài luyện điểm một phần",
    "Ba lõi dễ giữ, rồi việc lắp ráp dưới áp lực thời gian mô phỏng.",
    after_lesson="apx-m16-banking", minutes=45, difficulty="advanced",
    challenges=[P_COUNT, P_EXISTS, P_FIRST],
    vi_challenges={
        "apx-m16-count": vi_challenge(
            "Phần dễ giữ 1: phép đếm",
            "Lõi hai phút: `bankCount(double[] readings, double limit)` "
            "trả số số đo **nghiêm ngặt dưới** limit. Mảng rỗng trả 0.",
            [("count core", "Một bộ tích lũy, một phép so sánh nghiêm ngặt. Giữ nó và đi tiếp.")],
        ),
        "apx-m16-exists": vi_challenge(
            "Phần dễ giữ 2: kiểm tra tồn tại",
            "`bankExists(double[] readings, double limit)` trả true ngay "
            "khi có số đo **nghiêm ngặt trên** limit; false nếu không. "
            "Bắt buộc dùng lệnh trả sớm.",
            [("existence core", "for + if + return true; return false sau vòng lặp. Ba dòng điểm.")],
        ),
        "apx-m16-first": vi_challenge(
            "Phần dễ giữ 3: khớp đầu tiên với sentinel",
            "`bankFirst(double[] readings, double limit)` trả số đo "
            "**đầu tiên** nghiêm ngặt dưới limit, hoặc 999.0 khi không có.",
            [("first-match core", "Trả ngay trong vòng lặp tại khớp đầu tiên; vòng lặp chạy hết nghĩa là không khớp.")],
        ),
    },
    solutions=[
        ("apx-m16-count", r"""public class Solution {
    public static int bankCount(double[] readings, double limit) {
        int count = 0;
        for (double v : readings) {
            if (v < limit) {
                count++;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: inclusive boundary — gold-plated the wrong way
    public static int bankCount(double[] readings, double limit) {
        int count = 0;
        for (double v : readings) {
            if (v <= limit) {
                count++;
            }
        }
        return count;
    }
}
"""),
        ("apx-m16-exists", r"""public class Solution {
    public static boolean bankExists(double[] readings, double limit) {
        for (double v : readings) {
            if (v > limit) {
                return true;
            }
        }
        return false;
    }
}
""", r"""public class Solution {
    // BUG: scans everything and keeps the LAST verdict, not the first success
    public static boolean bankExists(double[] readings, double limit) {
        boolean found = false;
        for (double v : readings) {
            if (v > limit) {
                found = true;
            } else {
                found = false;
            }
        }
        return found;
    }
}
"""),
        ("apx-m16-first", r"""public class Solution {
    public static double bankFirst(double[] readings, double limit) {
        for (double v : readings) {
            if (v < limit) {
                return v;
            }
        }
        return 999.0;
    }
}
""", r"""public class Solution {
    // BUG: returns the LAST match, not the first
    public static double bankFirst(double[] readings, double limit) {
        double result = 999.0;
        for (double v : readings) {
            if (v < limit) {
                result = v;
            }
        }
        return result;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m16", "Checkpoint: bank in order",
    "Assemble the three-part class in point-maximizing order.",
    25,
    r"""
Same class as the workshop checkpoint, different skill: the point
is the ORDER you implement in and the discipline of not touching a
banked behavior again. Verify each part against the example before
moving to the next.
""",
    "Điểm kiểm tra: giữ điểm theo thứ tự",
    "Lắp ráp lớp ba phần theo thứ tự tối đa hóa điểm.",
    r"""
Cùng lớp với bài kiểm tra xưởng, kỹ năng khác: điểm nằm ở THỨ TỰ bạn
cài đặt và kỷ luật không đụng vào một hành vi đã giữ nữa. Đối chiếu
mỗi phần với ví dụ trước khi sang phần kế.
""",
    CP16,
    VI_CP16,
    solution=r"""public class Solution {
    public static class ReadingSet {
        private double[] readings;

        public ReadingSet(double[] readings) {
            this.readings = readings;
        }

        public int countCold() {
            int count = 0;
            for (double v : readings) {
                if (v < 0.0) {
                    count++;
                }
            }
            return count;
        }

        public boolean anyWarm() {
            for (double v : readings) {
                if (v > 25.0) {
                    return true;
                }
            }
            return false;
        }

        public double firstCold() {
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
    public static class ReadingSet {
        private double[] readings;

        public ReadingSet(double[] readings) {
            this.readings = readings;
        }

        public int countCold() {
            int count = 0;
            for (double v : readings) {
                if (v < 0.0) {
                    count++;
                }
            }
            return count;
        }

        public boolean anyWarm() {
            // BUG: existence check inverted — reports warm when none exceed
            boolean warm = false;
            for (double v : readings) {
                if (v > 25.0) {
                    warm = false;
                } else {
                    warm = true;
                }
            }
            return warm;
        }

        public double firstCold() {
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

print("M16 done")
