#!/usr/bin/env python3
"""AP CSA Advanced M20 — AP exam strategy (evidence-based execution)."""
from apx import *

M = "apx-strategy"

write_module(
    M,
    "AP Exam Strategy",
    "Pacing plans for both sections, question triage, and the last-ten-minutes protocol. Difficulty E2–E4.",
    "Chiến lược thi AP",
    "Kế hoạch nhịp độ cho cả hai phần, phân loại câu hỏi, và quy trình mười phút cuối. Độ khó E2–E4.",
    lessons=["apx-m20-pacing", "apx-m20-triage", "apx-m20-final10", "apx-cp-m20"],
    practices=["apx-p20-strategy"],
)

L1 = r"""
**Section 1 (MCQ, 40 questions / 90 minutes):** a 2-minute pace
with slack. The plan that survives contact:

- **Pass 1 (about 55 minutes)**: answer everything solvable in
  under 2 minutes. Mark skips immediately — a mark costs nothing.
- **Pass 2 (about 25 minutes)**: return to marks; eliminate two
  options, then commit. An unanswered question scores zero; a
  eliminated-to-two guess scores on average a quarter — always
  answer before time expires (the AP has no penalty for wrong
  answers).
- **Buffer (about 10 minutes)**: recheck marked-but-answered
  questions ONLY if a specific doubt exists ("did I read `<=` or
  `<`?"). Aimless rechecking loses points to second-guessing.

Section 2 (FRQ, 4 questions / 90 minutes) is a different animal:
about 20 minutes per question plus a 10-minute review bank. The
Q1/Q2 pair (methods, classes) usually runs faster than Q3/Q4
(ArrayList, 2D) — bank the difference early.
"""

L2 = r"""
**Question triage in three bins.** On first contact with any
question, bin it:

- **Bin A — answer now**: you can name the mechanism and see the
  finish line. Do it, move on.
- **Bin B — return later**: you recognize the shape but the trace
  will take real time. Mark, move.
- **Bin C — eliminate-and-guess**: after 30 honest seconds you
  cannot even name the mechanism. Eliminate impossible options
  (type-impossible, bounds-impossible), pick the survivor, mark
  for a Pass-2 look if time remains.

The discipline that makes triage work: **bin decisions are final
for the pass**. Re-litigating a bin choice mid-pass is how the
clock dies. Triage is trained — every timed set in this course
(module 4, 17, 18) was secretly a triage drill; from here on, run
the bins deliberately.
"""

L3 = r"""
**The last ten minutes.** A protocol, not a mood:

1. **Answer everything** (MCQ): with no wrong-answer penalty, a
   blank is strictly worse than a guess. Fill any blank now.
2. **Boundary audit** (FRQ): scan your written code for the two
   cheapest point-savers — an empty-input guard and the spec's
   sentinel returns. One missing `if` is a rubric row.
3. **The signature check**: each FRQ method's return type against
   the spec — the cheapest lost point there is.
4. **Stop rewriting.** After the audit, changes to working code
   have negative expected value. Close the loop, breathe, and let
   the banked points stand.

An honest note on scoring: this course never claims score
conversions; the exam's scoring is published by the College Board
and changes. What IS stable: every earned rubric row is permanent,
and no single question decides the score — the strategy above
just stops avoidable bleeding.
"""

VI_L1 = r"""
**Phần 1 (trắc nghiệm, 40 câu / 90 phút):** nhịp 2 phút với chỗ
dự phòng. Kế hoạch sống sót qua va chạm:

- **Lượt 1 (khoảng 55 phút)**: trả lời mọi câu giải được trong dưới
  2 phút. Đánh dấu câu bỏ qua ngay — một dấu không tốn gì.
- **Lượt hai (khoảng 25 phút)**: quay lại các dấu; loại hai phương
  án, rồi quyết định. Câu không trả lời được 0 điểm; loại-còn-hai
  rồi đoán trung bình được một phần tư — luôn trả lời trước khi hết
  giờ (AP không trừ điểm cho đáp án sai).
- **Dự phòng (khoảng 10 phút)**: soát lại các câu đã-đánh-dấu-đã-
  trả lời CHỈ khi có nghi ngờ cụ thể ("tôi đã đọc `<=` hay `<`?").
  Soát lại vô định kỳ mất điểm vì tự nghi ngờ bản thân.

Phần 2 (FRQ, 4 câu / 90 phút) là loài khác: khoảng 20 phút mỗi câu
cộng quỹ soát 10 phút. Cặp Q1/Q2 (phương thức, lớp) thường chạy
nhanh hơn Q3/Q4 (ArrayList, 2D) — giữ khoản chênh đó sớm.
"""

VI_L2 = r"""
**Phân loại câu hỏi vào ba thùng.** Lần gặp đầu tiên với bất kỳ câu
nào, xếp vào thùng:

- **Thùng A — trả lời ngay**: bạn gọi được tên cơ chế và thấy vạch
  đích. Làm, đi tiếp.
- **Thùng B — quay lại sau**: bạn nhận ra hình dạng nhưng truy vết
  sẽ tốn thời gian thật. Đánh dấu, đi tiếp.
- **Thùng C — loại-rồi-đoán**: sau 30 giây tử tế bạn còn chưa gọi
  được tên cơ chế. Loại các phương án bất khả (bất-khả-kiểu,
  bất-khả-biên), chọn người sống sót, đánh dấu để xem lượt 2 nếu
  còn giờ.

Kỷ luật làm phép phân loại hoạt động: **quyết định thùng là chốt
trong lượt đó**. Tranh luận lại lựa chọn thùng giữa lượt là cách
đồng hồ chết. Phân loại phải luyện — mọi bộ có giờ trong khóa này
(module 4, 17, 18) đều là bài tập phân loại ngụy trang; từ đây,
hãy chạy các thùng một cách chủ đích.
"""

VI_L3 = r"""
**Mười phút cuối.** Một quy trình, không phải một cảm xúc:

1. **Trả lời mọi câu** (trắc nghiệm): không bị trừ điểm cho đáp án
   sai, một chỗ trống chắc chắn tệ hơn một phép đoán. Điền mọi chỗ
   trống ngay.
2. **Kiểm toán biên** (FRQ): quét mã đã viết để tìm hai điểm cứu
   rẻ nhất — một biến chặn đầu-vào-rỗng và các giá trị sentinel
   của đặc tả. Một `if` thiếu là một dòng bảng điểm.
3. **Kiểm tra chữ ký**: kiểu trả về của mỗi phương thức FRQ so với
   đặc tả — điểm mất rẻ nhất trong các điểm mất.
4. **Ngừng viết lại.** Sau kiểm toán, các thay đổi vào mã đang chạy
   có giá trị kỳ vọng âm. Đóng vòng, thở, và để các điểm đã giữ
   đứng vững.

Một lưu ý trung thực về chấm điểm: khóa này không bao giờ tuyên bố
cách đổi điểm; việc chấm của kỳ thi do College Board công bố và có
thể thay đổi. Điều ổn định: mọi dòng bảng điểm giành được là vĩnh
viễn, và không câu nào quyết định điểm số — chiến lược trên chỉ
ngăn chảy máu có thể tránh.
"""

BOILER_PACE = r"""public class Solution {
    public static int bin(String difficulty, int seconds) {
        return 0; // replace: 1 = answer now, 2 = return later, 3 = eliminate-and-guess
    }
}
"""

P_TRIAGE = challenge(
    "apx-m20-triage1",
    "Triage drill",
    "Classify each situation into the triage bins (1 = answer now, "
    "2 = return later, 3 = eliminate-and-guess) — return the bin "
    "number for the FIRST situation only, as described:\n\n"
    "Situation A: an MCQ where you can name the mechanism and see "
    "the finish line (return this bin).\n\nSituation B: a heavy "
    "trace that will take real time — mark it.\n\nSituation C: 30 "
    "honest seconds and you cannot name the mechanism.",
    BOILER_PACE,
    [(
        "bin classification",
        r"""
CjTestBase.checkEq(Solution.bin("sees_finish_line", 30), 1, "mechanism known -> answer now");
""",
        "Name-the-mechanism-and-see-the-finish = bin 1.",
    )],
    level="imitation",
    difficulty="intermediate",
)

P_BUDGET = challenge(
    "apx-m20-budget",
    "Budget arithmetic",
    "The MCQ section is 90 minutes for 40 questions. If Pass 1 uses "
    "a strict 2-minute pace for 30 answered questions, how many "
    "minutes remain for Pass 2, the buffer, and the marks? Return "
    "the remaining minutes (assume the remaining 10 questions take "
    "no time in Pass 1).",
    r"""public class Solution {
    public static int remaining() {
        return 0; // replace: minutes left after Pass 1
    }
}
""",
    [(
        "budget minutes",
        r"""
CjTestBase.checkEq(Solution.remaining(), 30, "90 - 30 * 2");
""",
        "30 questions x 2 minutes = 60; 90 - 60 = 30.",
    )],
    level="guided",
    difficulty="intermediate",
)

P_SENTINEL = challenge(
    "apx-m20-sentinel",
    "The last-ten-minutes audit",
    "You have 4 minutes left and an FRQ method still unguarded. "
    "Which two point-savers does the protocol demand? The method "
    "below should return the FIRST reading below 0.0 or 999.0 when "
    "none. Add BOTH: the empty-input guard and the sentinel "
    "return.",
    r"""public class Solution {
    public static double firstBelow(double[] readings) {
        for (double v : readings) {
            if (v < 0.0) {
                return v;
            }
        }
        return 0; // replace with the spec's sentinel
    }
}
""",
    [(
        "audited method",
        r"""
CjTestBase.checkNear(Solution.firstBelow(new double[]{4.0, -2.0}), -2.0, 0.001, "first below");
CjTestBase.checkNear(Solution.firstBelow(new double[]{}), 999.0, 0.001, "empty guard");
CjTestBase.checkNear(Solution.firstBelow(new double[]{4.0}), 999.0, 0.001, "sentinel when none");
""",
        "Empty input falls through the loop; the sentinel (999.0) replaces the placeholder 0.",
    )],
    level="debugging",
    difficulty="intermediate",
)

CP20 = challenge(
    "apx-cp-m20-blank",
    "Checkpoint: no blanks left",
    "The final protocol: with no wrong-answer penalty, every blank "
    "is a lost point. The method should return the COUNT of "
    "answers you would submit if forced to answer every MCQ "
    "question (40 questions, you have genuinely solved 30, marked "
    "6, and refuse to guess 4). After the protocol, what count do "
    "you submit? Implement `process` to return it.",
    r"""public class Solution {
    public static int process() {
        return 0; // replace: answers submitted after the protocol
    }
}
""",
    [(
        "all answered",
        r"""
CjTestBase.checkEq(Solution.process(), 40, "no blanks survive the protocol");
""",
        "The protocol fills every blank: 40.",
    )],
    level="independent",
    difficulty="intermediate",
)

VI_CP20 = vi_challenge(
    "Điểm kiểm tra: không còn chỗ trống",
    "Quy trình cuối: không bị trừ điểm cho đáp án sai, mọi chỗ trống "
    "là một điểm mất. Phương thức nên trả SỐ câu trả lời bạn sẽ nộp "
    "nếu bị ép trả lời mọi câu trắc nghiệm (40 câu, bạn thực sự giải "
    "được 30, đánh dấu 6, và từ chối đoán 4). Sau quy trình, bạn nộp "
    "bao nhiêu câu? Cài `process` để trả con số đó.",
    [("all answered", "Quy trình lấp đầy mọi chỗ trống: 40.")],
)

write_practice(
    M, "apx-p20-strategy", "Strategy drill",
    "Triage, budget arithmetic, and the audit — light hands-on.",
    "Bài luyện chiến lược",
    "Phân loại, phép tính ngân sách, và kiểm toán — thực hành nhẹ.",
    after_lesson="apx-m20-final10", minutes=30, difficulty="intermediate",
    challenges=[P_TRIAGE, P_BUDGET, P_SENTINEL],
    vi_challenges={
        "apx-m20-triage1": vi_challenge(
            "Bài phân loại",
            "Xếp từng tình huống vào các thùng phân loại (1 = trả lời "
            "ngay, 2 = quay lại sau, 3 = loại-rồi-đoán) — trả về số thùng "
            "của TÌNH HUỐNG ĐẦU TIÊN, như mô tả:\n\nTình huống A: một câu "
            "trắc nghiệm nơi bạn gọi được tên cơ chế và thấy vạch đích "
            "(trả thùng này).\n\nTình huống B: một truy vết nặng sẽ tốn "
            "thời gian thật — đánh dấu nó.\n\nTình huống C: 30 giây tử tế "
            "mà vẫn không gọi được tên cơ chế.",
            [("bin classification", "Gọi-được-tên-cơ-chế-và-thấy-vạch-đích = thùng 1.")],
        ),
        "apx-m20-budget": vi_challenge(
            "Phép tính ngân sách",
            "Phần trắc nghiệm là 90 phút cho 40 câu. Nếu Lượt 1 dùng nhịp "
            "nghiêm ngặt 2 phút cho 30 câu được trả lời, còn bao nhiêu "
            "phút cho Lượt 2, quỹ dự phòng, và các dấu? Trả số phút còn "
            "lại (giả định 10 câu còn lại không tốn thời gian trong Lượt "
            "1).",
            [("budget minutes", "30 câu x 2 phút = 60; 90 - 60 = 30.")],
        ),
        "apx-m20-sentinel": vi_challenge(
            "Kiểm toán mười phút cuối",
            "Bạn còn 4 phút và một phương thức FRQ vẫn chưa có biến chặn. "
            "Quy trình đòi hai điểm cứu nào? Phương thức dưới đây nên trả "
            "số đo ĐẦU TIÊN dưới 0.0 hoặc 999.0 khi không có. Thêm CẢ "
            "HAI: biến chặn đầu-vào-rỗng và lệnh trả sentinel.",
            [("audited method", "Đầu vào rỗng rơi qua vòng lặp; sentinel (999.0) thay cho số 0 tạm.")],
        ),
    },
    solutions=[
        ("apx-m20-triage1", r"""public class Solution {
    public static int bin(String difficulty, int seconds) {
        return 1;
    }
}
""", r"""public class Solution {
    // BUG: marked a seen-the-finish-line question for later
    public static int bin(String difficulty, int seconds) {
        return 2;
    }
}
"""),
        ("apx-m20-budget", r"""public class Solution {
    public static int remaining() {
        return 30;
    }
}
""", r"""public class Solution {
    // BUG: subtracted the marks twice
    public static int remaining() {
        return 20;
    }
}
"""),
        ("apx-m20-sentinel", r"""public class Solution {
    public static double firstBelow(double[] readings) {
        for (double v : readings) {
            if (v < 0.0) {
                return v;
            }
        }
        return 999.0;
    }
}
""", r"""public class Solution {
    // BUG: kept the placeholder — empty input reports 0
    public static double firstBelow(double[] readings) {
        for (double v : readings) {
            if (v < 0.0) {
                return v;
            }
        }
        return 0;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m20", "Checkpoint: the no-blanks rule",
    "Protocol arithmetic: every blank becomes an answer.",
    10,
    r"""
The cheapest point on the exam is the blank you convert into a
guess. The protocol is arithmetic: solved + marked + guessed =
total. Internalize the rule now so it is a reflex in May.
""",
    "Điểm kiểm tra: luật không-chỗ-trống",
    "Phép toán quy trình: mọi chỗ trống thành một câu trả lời.",
    r"""
Điểm rẻ nhất trong phòng thi là chỗ trống bạn biến thành một phép
đoán. Quy trình là phép tính: giải-được + đánh-dấu + đoán = tổng.
Nội tâm hóa luật này để nó thành phản xạ vào tháng Năm.
""",
    CP20,
    VI_CP20,
    solution=r"""public class Solution {
    public static int process() {
        return 40;
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: left the refused-to-guess blanks empty
    public static int process() {
        return 36;
    }
}
""",
)

print("M20 done")
