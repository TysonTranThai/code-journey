#!/usr/bin/env python3
"""AP CSA Core M20 — Full Simulation & Exam Readiness (capstone)."""
from apcc import *

M = "cx-sim"

L1 = r"""
The simulation: run the four FRQ types back-to-back under the exam's
timing and structure — 90 minutes total, ~22 minutes each, no
calculator, no compiler, paper first. This course's platform version
is four practice sets (one per type, below) in this module; sit them
in one session if you can.

**Simulate honestly.** The rules that make the clock real: paper
trace, no IDE, no running code mid-answer. The platform grades
instantly — so for honesty, write your full answer FIRST, submit
once, and treat any failure as the exam would treat it: points
per-behavior, already earned.

**After each simulated question — 3 minutes:** what did the clock
pressure break? (Usually: skipped the edge-check step, or wrote code
before extracting obligations.) One line in the error log. The
simulation's value is 20% answering, 80% auditing the answering.
"""

L2 = r"""
Scoring yourself needs rubric thinking. A rubric row is a behavior,
and behaviors are countable. For a self-grade, mark your answer:

- +1 for each obligation from the spec faithfully implemented
- +1 for each edge case (empty/absent/boundary) correctly handled
- +1 for the correct return shape and type
- −0 for style — nobody scores style
- −1 candidate: any obligation silently dropped (the most common loss)

Honesty anchors: most rubric rows for a 9-point question map to ~6
obligations plus ~3 edge/shape rows. If you cannot enumerate what
your code does per row, you cannot self-score — enumerate first.

The simulate→score→repair loop is the final training: simulate one
set, score one set, repair the one biggest loss, repeat. Repair the
BIGGEST loss only — time spent polishing your best behavior while a
blank behavior remains is exactly the exam's time trap in miniature.
"""

L3 = r"""
**The readiness checklist** (the course's exit interview with you):

**Machines (write each from memory in ≤ 15 s):** accumulator, counter,
flag, sentinel scan; forward/backward/pairwise array loops; String
filter/map/build; ArrayList forward-read/backward-mutate; 2D
row/column/neighbor; recursion base+shrink, two-branch counting.

**Exam process:** state tables on demand; prediction-first on MCQ;
the four elimination probes; the eight FRQ steps; first-error
localization; skeleton banking; the 2:08 / 22:30 pacing rules.

**Honest self-diagnosis:** run one more timed set from Module 19; if
every miss maps to a family you already knew (not a new machine),
you are exam-ready — the remaining variance is tempo, and only more
timed sets fix tempo. If any miss reveals a machine you could not
re-derive, return to that lab; that is not an exam problem yet.

The next course in the track (Exam Mastery) assumes this checklist
passes: it adds full mock papers and score-5 polish, not new
machines. Everything from here is repetition with intent.
"""

write_module(
    M,
    "Full Simulation & Exam Readiness",
    "The four-FRQ simulation under exam structure, rubric-based self-scoring, and the course's exit readiness checklist.",
    "Mô phỏng toàn diện & sẵn sàng thi",
    "Mô phỏng bốn-FRQ theo cấu trúc đề, tự chấm theo bảng-rubric, và checklist sẵn-sàng kết thúc khóa.",
    lessons=["cx-m20-simulate", "cx-m20-selfscore", "cx-m20-ready", "cx-cp-m20"],
    practices=["cx-p20-sim-q1", "cx-p20-sim-q3", "cx-p20-sim-q4", "cx-p20-sim-mixed"],
)

write_lesson(
    M, "cx-m20-simulate", "Running the simulation",
    "One sitting, four types, paper first, submit once, audit after each.",
    12, L1,
    "Chạy mô phỏng",
    "Một buổi, bốn dạng, giấy trước, nộp một lần, kiểm sát sau mỗi câu.",
    r"""
Mô phỏng: chạy bốn dạng FRQ liên tiếp theo thời gian và cấu trúc của
đề — tổng 90 phút, ~22 phút mỗi câu, không máy tính, không trình biên
dịch, giấy trước. Phiên bản nền-tảng của khóa này là bốn bộ luyện
(mỗi dạng một bộ, bên dưới) trong module này; nếu được, hãy ngồi làm
trong một buổi.

**Mô phỏng trung thực.** Những luật làm cho đồng hồ trở nên thật: truy
vết trên giấy, không IDE, không chạy mã giữa chừng. Nền tảng chấm ngay
lập tức — vì thế để trung thực, viết TOÀN BỘ lời giải TRƯỚC, nộp MỘT
LẦN, và coi mọi thất bại như đề thi sẽ coi: điểm theo từng hành vi,
nhiều phần đã được kiếm sẵn.

**Sau mỗi câu mô phỏng — 3 phút:** áp lực đồng hồ đã phá vỡ điều gì?
(Thường là: bỏ qua bước kiểm-biên, hoặc viết mã trước khi trích nghĩa
vụ.) Một dòng vào nhật ký lỗi. Giá trị của mô phỏng là 20% trả lời,
80% kiểm sát cách-trả-lời.
""",
)

write_lesson(
    M, "cx-m20-selfscore", "Scoring yourself",
    "Behaviors are countable: obligations + edges + shape; repair the biggest loss.",
    12, L2,
    "Tự chấm điểm",
    "Hành vi là đếm được: nghĩa-vụ + biên + hình-dạng; sửa mất-mát-lớn-nhất.",
    r"""
Tự chấm đòi tư duy rubric. Một dòng rubric là một hành vi, và hành vi
đếm được. Với lần tự chấm, đánh dấu lời giải của bạn:

- +1 cho mỗi nghĩa-vụ từ đặc tả được hiện thực trung thực
- +1 cho mỗi trường-hợp-biên (rỗng/vắng/biên) xử lý đúng
- +1 cho hình-dạng và kiểu trả về đúng
- −0 cho phong cách — không ai chấm phong cách
- −1: mọi nghĩa-vụ bị bỏ im lặng (mất-mát phổ biến nhất)

Mỏ neo của sự trung thực: đa số dòng rubric của một câu 9 điểm ánh xạ
sang ~6 nghĩa-vụ cộng ~3 dòng biên/hình-dạng. Nếu không liệt kê được mã
của bạn làm gì theo từng dòng, bạn không thể tự chấm — hãy liệt kê
trước.

Vòng mô-phỏng→chấm→sửa là buổi huấn cuối: mô phỏng một bộ, chấm một
bộ, sửa đúng MỘT mất-mát lớn nhất, lặp lại. Sửa mất-mát LỚN NHẤT thôi —
thời gian dành để đánh bóng hành-viện-tốt-nhất trong khi còn một hành-vi
trắng chính là cái bẫy-thời-gian của đề thi ở kích thước thu nhỏ.
""",
)

write_lesson(
    M, "cx-m20-ready", "The readiness checklist",
    "Machines, exam process, honest diagnosis — the exit interview.",
    12, L3,
    "Checklist sẵn sàng",
    "Cỗ máy, quy trình thi, chẩn đoán trung thực — buổi phỏng vấn ra trường.",
    r"""
**Checklist sẵn sàng** (buổi phỏng vấn ra-trường của khóa học):

**Cỗ máy (viết mỗi cái từ trí nhớ trong ≤ 15 giây):** bộ cộng dồn, bộ
đếm, cờ, quét lính canh; các vòng mảng xuôi/ngược/từng-cặp; lọc/biến-
đổi/dựng String; đọc-xuôi/biến-đổi-ngược ArrayList; hàng/cột/hàng-xóm
2D; cơ-sở+thu-nhỏ đệ quy, đếm-hai-nhánh.

**Quy trình thi:** bảng trạng thái theo yêu cầu; dự-đoán-trước cho
MCQ; bốn phép dò loại trừ; tám bước FRQ; định-vị-lỗi-đầu-tiên; gửi kho
bộ xương; luật phân bổ 2:08 / 22:30.

**Chẩn đoán trung thực:** chạy thêm một bộ có giờ từ Module 19; nếu
mọi câu trượt đều ánh xạ về một họ bạn đã biết (không phải một cỗ máy
mới), bạn đã sẵn sàng — phương-sai còn lại là nhịp độ, và chỉ thêm các
bộ-có-giờ mới sửa được nhịp độ. Nếu có câu trượt phơi ra một cỗ máy
bạn không tự suy lại được, hãy quay về phòng-luyện đó; đó chưa phải là
vấn-đề-của-phòng-thi.

Khóa tiếp theo trong track (Exam Mastery) giả định checklist này đạt:
nó thêm các đề-mô-phỏng-đầy-đủ và đánh-bóng-điểm-5, không thêm cỗ máy
mới. Mọi thứ từ đây là lặp-lại-có-chủ-đích.
""",
)

SIM_Q1 = r"""public class Solution {
    // SIMULATED Q1 — Methods and Control Structures (22 minutes).
    // Part (a): int digitSum(int n) — sum of the decimal digits of
    //   n (n >= 0). 0 -> 0.
    // Part (b): boolean divisibleBy3(int n) — true when digitSum(n)
    //   is divisible by 3. Use part (a).
    public static int digitSum(int n) {
        return 0; // replace
    }

    public static boolean divisibleBy3(int n) {
        return false; // replace
    }
}
"""

SIM_Q3 = r"""import java.util.ArrayList;

public class Solution {
    public static class Car {
        private String color;
        private int miles;
        public Car(String color, int miles) {
            this.color = color;
            this.miles = miles;
        }
        public String getColor() { return color; }
        public int getMiles() { return miles; }
    }

    // SIMULATED Q3 — ArrayList analysis (22 minutes).
    // Part (a): int fleetMiles(ArrayList<Car> cars, String color) —
    //   total miles of cars of that color (0 when none).
    // Part (b): int removeColor(ArrayList<Car> cars, String color) —
    //   remove ALL cars of that color in place and return how many
    //   were removed.
    public static int fleetMiles(ArrayList<Car> cars, String color) {
        return 0; // replace-a
    }

    public static int removeColor(ArrayList<Car> cars, String color) {
        return 0; // replace-b
    }
}
"""

SIM_Q4 = r"""public class Solution {
    // SIMULATED Q4 — 2D array (22 minutes). Rectangular grid,
    // grid.length >= 1.
    // Part (a): int countAbove(int[][] grid, int threshold) — cells
    //   strictly greater than threshold.
    // Part (b): int[] colBelowAvg(int[][] grid) — for each column,
    //   1 when its sum is >= the grid's TOTAL average, else 0.
    //   (Average as a double; compare column SUM against it.)
    public static int countAbove(int[][] grid, int threshold) {
        return 0; // replace
    }

    public static int[] colBelowAvg(int[][] grid) {
        return null; // replace
    }
}
"""

SIM_MIXED = r"""public class Solution {
    // SIMULATED MCQ-STYLE TRACE (the 42-question section compressed).
    // Predict WITHOUT running, then reproduce exactly:
    //   m({4, 9, 2}) -> ?   trace: evens halved in place, odds doubled+1,
    //   return sum of final values minus count of changed cells.
    public static int m(int[] nums) {
        int changed = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] % 2 == 0) {
                nums[i] = nums[i] / 2;
                changed++;
            } else {
                nums[i] = nums[i] * 2 + 1;
            }
        }
        int total = 0;
        for (int v : nums) {
            total += v;
        }
        return total - changed;
    }
}
"""

P_Q1 = challenge(
    "cx-m20-sim-q1",
    "Simulation Q1: digits",
    "Sit this as a 22-minute question: full workflow on paper, code once, submit once. (a) digitSum (n >= 0); (b) divisibleBy3 using digitSum. Edge obligations: n = 0.",
    SIM_Q1,
    [(
        "q1 behaviors",
        r"""
CjTestBase.checkEq(Solution.digitSum(0), 0, "zero edge");
CjTestBase.checkEq(Solution.digitSum(492), 15, "4 + 9 + 2");
CjTestBase.checkEq(Solution.digitSum(1000000), 1, "single 1");
CjTestBase.checkEq(Solution.divisibleBy3(492), true, "15 divisible by 3");
CjTestBase.checkEq(Solution.divisibleBy3(100), false, "1 not divisible");
CjTestBase.checkEq(Solution.divisibleBy3(0), true, "0 is divisible by 3");
""",
        "(a) strip-and-add recursively or in a loop; (b) return digitSum(n) % 3 == 0;",
    )],
    level="real-world",
)

P_Q3 = challenge(
    "cx-m20-sim-q3",
    "Simulation Q3: fleet",
    "22-minute question: (a) aggregate by color; (b) remove-by-color with a count. (b) needs the backward loop AND a counter — two machines in one method.",
    SIM_Q3,
    [(
        "q3 behaviors",
        r"""
ArrayList<Solution.Car> cars = new ArrayList<Solution.Car>();
cars.add(new Solution.Car("red", 100));
cars.add(new Solution.Car("blue", 250));
cars.add(new Solution.Car("red", 50));
CjTestBase.checkEq(Solution.fleetMiles(cars, "red"), 150, "100 + 50");
CjTestBase.checkEq(Solution.fleetMiles(cars, "green"), 0, "absent color");
CjTestBase.checkEq(Solution.removeColor(cars, "red"), 2, "two removed");
CjTestBase.checkEq(cars.size(), 1, "only blue left");
CjTestBase.checkEq(Solution.removeColor(cars, "red"), 0, "nothing left to remove");
ArrayList<Solution.Car> dup = new ArrayList<Solution.Car>();
dup.add(new Solution.Car("red", 10));
dup.add(new Solution.Car("red", 20));
dup.add(new Solution.Car("red", 30));
CjTestBase.checkEq(Solution.removeColor(dup, "red"), 3, "consecutive removals all counted");
CjTestBase.checkEq(dup.size(), 0, "consecutive reds all gone");
""",
        "(a) for-each + filter + accumulator; (b) backward loop, count removals, return count.",
    )],
    level="real-world",
)

P_Q4 = challenge(
    "cx-m20-sim-q4",
    "Simulation Q4: grid stats",
    "22-minute question: (a) threshold count; (b) per-column verdict vs the total average — column sums, one division, orientation discipline.",
    SIM_Q4,
    [(
        "q4 behaviors",
        r"""
int[][] g = { {1, 6}, {0, 3} };
CjTestBase.checkEq(Solution.countAbove(g, 2), 2, "6 and 3");
CjTestBase.checkEq(Solution.countAbove(g, 100), 0, "none");
int[] verdict = Solution.colBelowAvg(g);
CjTestBase.checkEq(verdict.length, 2, "one verdict per column");
CjTestBase.checkEq(verdict[0], 0, "col 0 sums 1 < avg 2.5");
CjTestBase.checkEq(verdict[1], 1, "col 1 sums 9 >= 2.5");
int[] eq = Solution.colBelowAvg(new int[][]{ {3, 3} });
CjTestBase.checkEq(eq[0], 1, "col sum exactly equals avg: >= holds");
CjTestBase.checkEq(eq[1], 1, "same for column 2");
""",
        "(b): total = sum of all; avg = total / (rows*cols) as double; per column, sum >= avg ? 1 : 0.",
    )],
    level="real-world",
)

P_MIXED = challenge(
    "cx-m20-sim-mixed",
    "Simulation: mixed trace",
    "The MCQ-style section in one question: PREDICT m({4, 9, 2}) on paper with a state table BEFORE looking at the code below, then reproduce m yourself. Your table should show both passes.",
    SIM_MIXED,
    [(
        "trace reproduced",
        r"""
CjTestBase.checkEq(Solution.m(new int[]{4, 9, 2}), 20, "sum 22 - changed 2");
CjTestBase.checkEq(Solution.m(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.m(new int[]{2}), 0, "1 - 1");
""",
        "Pass 1: 4->2 (changed), 9->19, 2->1 (changed); sum 22, changed 2, return 20... hand-check against the tests.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p20-sim-q1", "Simulated Q1",
    "Methods and Control Structures under the 22-minute clock.",
    "Mô phỏng Q1",
    "Phương thức và cấu trúc điều khiển dưới đồng hồ 22 phút.",
    after_lesson="cx-m20-simulate", minutes=22, difficulty="advanced",
    challenges=[P_Q1],
    vi_challenges={
        "cx-m20-sim-q1": vi_challenge("Mô phỏng Q1: chữ số",
            "Làm như một câu 22 phút: toàn bộ quy trình trên giấy, viết mã một lần, nộp một lần. (a) digitSum (n >= 0); (b) divisibleBy3 dùng digitSum. Nghĩa vụ biên: n = 0.",
            [("q1 behaviors", "(a) bóc-và-cộng đệ quy hoặc vòng lặp; (b) return digitSum(n) % 3 == 0;")]),
    },
    solutions=[
        ("cx-m20-sim-q1",
         SIM_Q1.replace("        return 0; // replace", "        int sum = 0;\n        while (n > 0) {\n            sum += n % 10;\n            n /= 10;\n        }\n        return sum;")
            .replace("        return false; // replace", "        return digitSum(n) % 3 == 0;"),
         SIM_Q1.replace("        return 0; // replace", "        int sum = 0;\n        while (n > 0) {\n            sum += n % 10;\n            n /= 10;\n        }\n        return sum;")
            .replace("        return false; // replace", "        return digitSum(n) % 3 == 1;")),
    ],
)

write_practice(
    M, "cx-p20-sim-q3", "Simulated Q3",
    "ArrayList analysis under the 22-minute clock.",
    "Mô phỏng Q3",
    "Phân tích ArrayList dưới đồng hồ 22 phút.",
    after_lesson="cx-m20-simulate", minutes=22, difficulty="advanced",
    challenges=[P_Q3],
    vi_challenges={
        "cx-m20-sim-q3": vi_challenge("Mô phỏng Q3: đội xe",
            "Câu 22 phút: (a) cộng dồn theo màu; (b) xóa-theo-màu kèm bộ đếm. (b) cần vòng ngược VÀ một bộ đếm — hai cỗ máy trong một phương thức.",
            [("q3 behaviors", "(a) for-each + lọc + bộ cộng dồn; (b) vòng ngược, đếm số lần xóa, trả về số đếm.")]),
    },
    solutions=[
        ("cx-m20-sim-q3",
         SIM_Q3.replace("        return 0; // replace-a", "        int total = 0;\n        for (Car c : cars) {\n            if (c.getColor().equals(color)) {\n                total += c.getMiles();\n            }\n        }\n        return total;")
            .replace("        return 0; // replace-b", "        int removed = 0;\n        for (int i = cars.size() - 1; i >= 0; i--) {\n            if (cars.get(i).getColor().equals(color)) {\n                cars.remove(i);\n                removed++;\n            }\n        }\n        return removed;"),
         SIM_Q3.replace("        return 0; // replace-a", "        int total = 0;\n        for (Car c : cars) {\n            if (c.getColor().equals(color)) {\n                total += c.getMiles();\n            }\n        }\n        return total;")
            .replace("        return 0; // replace-b", "        int removed = 0;\n        for (int i = 0; i < cars.size(); i++) {\n            if (cars.get(i).getColor().equals(color)) {\n                cars.remove(i);\n                removed++;\n            }\n        }\n        return removed;")),
    ],
)

write_practice(
    M, "cx-p20-sim-q4", "Simulated Q4",
    "2D array analysis under the 22-minute clock.",
    "Mô phỏng Q4",
    "Phân tích mảng 2 chiều dưới đồng hồ 22 phút.",
    after_lesson="cx-m20-simulate", minutes=22, difficulty="advanced",
    challenges=[P_Q4],
    vi_challenges={
        "cx-m20-sim-q4": vi_challenge("Mô phỏng Q4: thống kê lưới",
            "Câu 22 phút: (a) đếm vượt ngưỡng; (b) phán-x就连-theo-cột so với trung bình toàn-lưới — tổng cột, một phép chia, kỷ luật định hướng.",
            [("q4 behaviors", "(b): total = cộng hết; avg = total / (rows*cols) theo double; mỗi cột, sum >= avg ? 1 : 0.")]),
    },
    solutions=[
        ("cx-m20-sim-q4",
         SIM_Q4.replace("        return 0; // replace", "        int count = 0;\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (grid[r][c] > threshold) {\n                    count++;\n                }\n            }\n        }\n        return count;")
            .replace("        return null; // replace", "        int total = 0;\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                total += grid[r][c];\n            }\n        }\n        double avg = (double) total / (grid.length * grid[0].length);\n        int[] verdict = new int[grid[0].length];\n        for (int c = 0; c < grid[0].length; c++) {\n            int colSum = 0;\n            for (int r = 0; r < grid.length; r++) {\n                colSum += grid[r][c];\n            }\n            verdict[c] = (colSum >= avg) ? 1 : 0;\n        }\n        return verdict;"),
         SIM_Q4.replace("        return 0; // replace", "        int count = 0;\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (grid[r][c] > threshold) {\n                    count++;\n                }\n            }\n        }\n        return count;")
            .replace("        return null; // replace", "        int total = 0;\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                total += grid[r][c];\n            }\n        }\n        double avg = (double) total / (grid.length * grid[0].length);\n        int[] verdict = new int[grid[0].length];\n        for (int c = 0; c < grid[0].length; c++) {\n            int colSum = 0;\n            for (int r = 0; r < grid.length; r++) {\n                colSum += grid[r][c];\n            }\n            verdict[c] = (colSum > avg) ? 1 : 0;\n        }\n        return verdict;")),
    ],
)

write_practice(
    M, "cx-p20-sim-mixed", "Simulated MCQ trace",
    "The trace section compressed: predict, then reproduce.",
    "Mô phỏng truy vết MCQ",
    "Phần truy vết được nén lại: dự đoán, rồi tái hiện.",
    after_lesson="cx-m20-simulate", minutes=10, difficulty="advanced",
    challenges=[P_MIXED],
    vi_challenges={
        "cx-m20-sim-mixed": vi_challenge("Mô phỏng: truy vết trộn",
            "Phần MCQ-nén vào một câu: DỰ ĐOÁN m({4, 9, 2}) trên giấy với bảng trạng thái TRƯỚC khi đọc kỹ mã dưới đây, rồi tái hiện m bằng mã của bạn. Bảng của bạn cần cả hai lượt.",
            [("trace reproduced", "Lượt 1: 4->2 (đổi), 9->19, 2->1 (đổi); cộng dồn 22, đổi 2, trả về 20... tự đối chiếu tay với các test.")]),
    },
    solutions=[
        ("cx-m20-sim-mixed", SIM_MIXED, SIM_MIXED.replace("return total - changed;", "return total + changed;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m20", "Checkpoint: readiness verdict",
    "One honest question: the fleet, run under your own clock.",
    25,
    r"""
This checkpoint is deliberately plain: the simulated Q3 without its
wrapper story. If you sat it with a visible 22-minute clock, wrote
the full answer before submitting, and scored yourself with the
rubric method (+obligations, +edges, +shape), you have executed the
entire course: machines, workflow, salvage, simulation. Whatever the
score, the loop is the same from here — simulate, score, repair the
biggest loss. The exam is a tempo problem once the machines are
yours.
""",
    "Điểm kiểm tra: phán quyết sẵn sàng",
    "Một câu hỏi trung thực: đội xe, chạy dưới đồng hồ của chính bạn.",
    r"""
Điểm kiểm tra này cố tình giản-dị: Q3 mô phỏng không có lớp-bọc-câu-
chuyện. Nếu bạn ngồi làm với đồng hồ 22 phút nhìn-thấy-được, viết trọn
lời giải trước khi nộp, và tự chấm bằng phương pháp rubric (+nghĩa-vụ,
+biên, +hình-dạng), bạn đã thực thi trọn vẹn khóa học: cỗ máy, quy
trình, cứu vớt, mô phỏng. Bất kể điểm số, vòng lặp từ đây vẫn vậy — mô
phỏng, chấm, sửa mất-mát-lớn-nhất. Khi các cỗ máy đã là của bạn, kỳ thi
chỉ còn là bài-toán-nhịp-độ.
""",
    P_Q3,
    vi_challenge("Điểm kiểm tra: phán quyết sẵn sàng",
        "Một câu hỏi trung thực: đội xe dưới đồng hồ của chính bạn — toàn bộ quy trình, nộp một lần, tự chấm theo rubric.",
        [("q3 behaviors", "(a) for-each + lọc + bộ cộng dồn; (b) vòng ngược + bộ đếm.")]),
    solution=SIM_Q3.replace("        return 0; // replace-a", "        int total = 0;\n        for (Car c : cars) {\n            if (c.getColor().equals(color)) {\n                total += c.getMiles();\n            }\n        }\n        return total;")
        .replace("        return 0; // replace-b", "        int removed = 0;\n        for (int i = cars.size() - 1; i >= 0; i--) {\n            if (cars.get(i).getColor().equals(color)) {\n                cars.remove(i);\n                removed++;\n            }\n        }\n        return removed;"),
    wrong=SIM_Q3.replace("        return 0; // replace-a", "        int total = 0;\n        for (Car c : cars) {\n            if (c.getColor().equals(color)) {\n                total += c.getMiles();\n            }\n        }\n        return total;")
        .replace("        return 0; // replace-b", "        int removed = 0;\n        for (int i = 0; i < cars.size(); i++) {\n            if (cars.get(i).getColor().equals(color)) {\n                cars.remove(i);\n                removed++;\n            }\n        }\n        return removed;"),
)
