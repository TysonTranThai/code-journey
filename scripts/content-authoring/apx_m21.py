#!/usr/bin/env python3
"""AP CSA Advanced M21 — Full Practice Exam #1 (original simulation)."""
from apx import *

M = "apx-exam1"

write_module(
    M,
    "Full Practice Exam #1",
    "A complete original simulation: MCQ-style section plus FRQ-style section, timed, with post-exam analysis. Difficulty E5.",
    "Đề thi thử trọn vẹn #1",
    "Một mô phỏng gốc trọn vẹn: phần kiểu trắc nghiệm cộng phần kiểu FRQ, có giờ, với phân tích sau thi. Độ khó E5.",
    lessons=["apx-m21-rules", "apx-m21-analysis", "apx-m21-debrief", "apx-cp-m21"],
    practices=["apx-p21-exam"],
)

L1 = r"""
**Before you start.** This is a simulation, not a study session.
Rules of engagement:

- **Time it for real**: 45 minutes for the practice MCQ set,
  45 minutes for the FRQ set (half-scale of the real sections to
  fit a study sitting — the pacing math carries over).
- **No notes, no re-runs mid-exam.** Answer everything; blanks
  score zero.
- **MCQ protocol**: your submission must print the option letter
  followed by a one-sentence justification. On the real exam you
  justify nothing — here, the justification is your permanent
  record of *why*, and the analysis step reads it back.

Everything in this exam is original; no released College Board
questions are reproduced. When you finish, do the debrief in the
same sitting: the exam's value is 50% taking it, 50% reading the
wreckage honestly.
"""

L2 = r"""
**After the exam: the scorecard.** Score yourself on three axes:

1. **Accuracy per mechanism** — for each challenge, note the
   mechanism (trace / spec-implementation / debugging / dispatch /
   mutation) and right-vs-wrong. Your weakest mechanism is next
   week's drill, not your weakest topic.
2. **Time-per-item variance** — items that took 3x their budget
   get a post-mortem: was the spec misread, or the shape
   unrecognized? Misreads are fixed by the circling habit
   (module 13); unrecognized shapes by re-running that
   mechanism's module practice.
3. **The two-question rule**: pick the two items whose loss cost
   the most time, and redo ONLY those, from a blank editor, the
   next day. Redoing everything is procrastination wearing a
   productive costume.

A simulation that changes nothing is a sunk cost — the debrief IS
the exam.
"""

L3 = r"""
**Reading the difficulty honestly.** This simulation deliberately
runs harder than a real exam's median item: if you score ~70%
here under time, you are operating above the line the real exam
draws. Do not "fix" your strategy toward the hardest items — the
exam rewards consistency on mid-weight questions, and the
simulation's hard tail exists to make the real thing feel slow
and quiet.

If the score disappoints, the correction is always the same
triad: one mechanism module re-run, one timed set re-run, one
full simulation re-run — in that order, with the 48-hour rule
between steps. Three cycles of that triad move scores further
than any new material.
"""

VI_L1 = r"""
**Trước khi bắt đầu.** Đây là mô phỏng, không phải buổi học. Luật
tham chiến:

- **Bấm giờ thật**: 45 phút cho bộ kiểu-trắc-nghiệm, 45 phút cho
  bộ kiểu-FRQ (nửa quy mô so với các phần thật để vừa một buổi học
  — phép toán nhịp độ vẫn mang sang được).
- **Không tài liệu, không chạy lại giữa kỳ.** Trả lời mọi câu;
  chỗ trống được 0 điểm.
- **Giao thức trắc nghiệm**: bài nộp phải in chữ cái phương án kèm
  một câu lý do. Trong phòng thi thật bạn không phải giải thích gì —
  ở đây, lời giải thích là hồ sơ lâu dài về *lý do*, và bước phân
  tích đọc lại nó.

Mọi thứ trong đề này là bản gốc; không câu hỏi College Board phát
hành nào được tái sử dụng. Khi xong, làm phần tranh luận trong cùng
buổi: giá trị của đề thi là 50% làm bài, 50% đọc xác liệu một cách
trung thực.
"""

VI_L2 = r"""
**Sau kỳ thi: bảng điểm.** Tự chấm trên ba trục:

1. **Độ chính xác theo cơ chế** — với mỗi bài, ghi cơ chế (truy
   vết / cài-đặc-tả / gỡ-lỗi / điều-phối / biến-đổi) và đúng-hay-sai.
   Cơ chế yếu nhất của bạn là mục luyện tuần tới, không phải chủ đề
   yếu nhất.
2. **Phương sai thời-gian-mỗi-câu** — các bài tốn gấp 3 ngân sách
   được mổ xẻ: đọc sai đặc tả, hay không nhận ra hình dạng? Đọc sai
   được chữa bằng thói quen khoanh tròn (module 13); hình dạng không
   nhận ra bằng cách chạy lại bộ luyện module của cơ chế đó.
3. **Luật hai-câu-hỏi**: chọn hai bài mà việc mất tốn thời gian
   nhiều nhất, và làm lại CHỈ chúng, từ trình soạn thảo trắng, vào
   ngày mai. Làm lại tất cả là trì hoãn mặc trang phục chăm chỉ.

Một mô phỏng không đổi được gì là chi phí chìm — tranh luận CHÍNH
LÀ kỳ thi.
"""

VI_L3 = r"""
**Đọc độ khó một cách trung thực.** Mô phỏng này cố ý chạy khó hơn
mức trung vị của đề thật: nếu bạn đạt ~70% ở đây dưới áp lực giờ,
bạn đang làm việc trên đường kẻ mà đề thật vẽ. Đừng "sửa" chiến
lược của mình theo hướng các câu khó nhất — đề thi thưởng cho sự
ổn định trên các câu tầm-trung, và phần đuôi khó của mô phỏng tồn
tại để đề thật cảm thấy chậm và yên tĩnh.

Nếu điểm làm bạn thất vọng, bản sửa luôn là bộ ba tương tự: chạy
lại một module cơ chế, chạy lại một bộ có giờ, chạy lại một mô phỏng
trọn vẹn — theo thứ tự đó, với luật 48 giờ giữa các bước. Ba chu kỳ
bộ ba đó đưa điểm đi xa hơn bất kỳ tài liệu mới nào.
"""

BOILER_E1 = r"""public class Solution {
    public static void program() {
        // Print your answer: the option letter, then a one-sentence reason.
    }
}
"""

Q1_S = "What is printed?\n\n```java\nint[] a = {4, 1, 4, 2};\nint best = a[0];\nfor (int v : a) {\n    if (v > best) { best = v; }\n}\nint second = Integer.MIN_VALUE;\nfor (int v : a) {\n    if (v < best && v > second) { second = v; }\n}\nSystem.out.print(second);\n```"
Q1_O = ["A. 1", "B. 2", "C. 4", "D. -2147483648"]
Q1_W = "B. Pass one finds max 4 (duplicates collapse); pass two finds the max strictly below 4, which is 2. A forgets the 2; C forgets 'strictly below'; D means no distinct second existed."
Q1_VS = "Chương trình in gì?\n\n```java\nint[] a = {4, 1, 4, 2};\nint best = a[0];\nfor (int v : a) {\n    if (v > best) { best = v; }\n}\nint second = Integer.MIN_VALUE;\nfor (int v : a) {\n    if (v < best && v > second) { second = v; }\n}\nSystem.out.print(second);\n```"
Q1_VO = ["A. 1", "B. 2", "C. 4", "D. -2147483648"]
Q1_VW = "B. Lượt một tìm max 4 (bản sao gộp lại); lượt hai tìm max nghiêm ngặt dưới 4, là 2. A quên số 2; C quên 'nghiêm ngặt dưới'; D nghĩa là không có giá trị lớn thứ hai riêng biệt."

Q2_S = "What is the value of `r` after the loop?\n\n```java\nint r = 1;\nfor (int i = 3; i >= 1; i--) {\n    r *= i;\n}\n```"
Q2_O = ["A. 6", "B. 3", "C. 9", "D. 1"]
Q2_W = "A. 3 * 2 * 1 = 6. B stops after one pass; C adds instead of multiplies; D never multiplies."
Q2_VS = "Giá trị của `r` sau vòng lặp là bao nhiêu?\n\n```java\nint r = 1;\nfor (int i = 3; i >= 1; i--) {\n    r *= i;\n}\n```"
Q2_VO = ["A. 6", "B. 3", "C. 9", "D. 1"]
Q2_VW = "A. 3 * 2 * 1 = 6. B dừng sau một lượt; C cộng thay vì nhân; D không bao giờ nhân."

Q3_S = "Which completes the removal correctly (remove all \"x\")?\n\n```java\nArrayList<String> list = ...; // [x, b, x, x]\nfor (int i = list.size() - 1; i >= 0; i--) {\n    if (list.get(i).equals(\"x\")) { list.remove(i); }\n}\n```"
Q3_O = ["A. Correct as written", "B. Fails: needs i++ inside", "C. Fails: forward loop required", "D. Fails: remove(i--) required"]
Q3_W = "A. Backward removal cannot skip: shifts only affect unvisited FORWARD indices, and none remain. B breaks the descent; C reintroduces the skip bug; D corrupts the index."
Q3_VS = "Cái nào hoàn thành việc xóa đúng cách (xóa mọi \"x\")?\n\n```java\nArrayList<String> list = ...; // [x, b, x, x]\nfor (int i = list.size() - 1; i >= 0; i--) {\n    if (list.get(i).equals(\"x\")) { list.remove(i); }\n}\n```"
Q3_VO = ["A. Đúng như đã viết", "B. Lỗi: cần i++ bên trong", "C. Lỗi: bắt buộc vòng đi tới", "D. Lỗi: cần remove(i--)"]
Q3_VW = "A. Xóa chiều ngược không thể bỏ sót: phép dồn chỉ ảnh hưởng các chỉ số CHƯA duyệt phía trước, và không còn cái nào. B phá chiều giảm; D làm hỏng chỉ số."

Q4_S = "What does `f(5)` return?\n\n```java\npublic static int f(int n) {\n    if (n <= 1) { return 1; }\n    return n * f(n - 1);\n}\n```"
Q4_O = ["A. 120", "B. 15", "C. 24", "D. 5"]
Q4_W = "A. 5 * 4 * 3 * 2 * 1 = 120 (factorial). B sums instead of multiplying; C stops at n=2; D forgets the recursion."
Q4_VS = "`f(5)` trả về bao nhiêu?\n\n```java\npublic static int f(int n) {\n    if (n <= 1) { return 1; }\n    return n * f(n - 1);\n}\n```"
Q4_VO = ["A. 120", "B. 15", "C. 24", "D. 5"]
Q4_VW = "A. 5 * 4 * 3 * 2 * 1 = 120 (giai thừa). B cộng thay vì nhân; C dừng tại n=2; D quên đệ quy."

def mcq(cid, stem, opts, ans, why, vi_stem, vi_opts, vi_why):
    prompt = stem + "\n\n" + "\n".join(opts) + (
        "\n\nPrint the letter, then your one-sentence justification."
    )
    vi_prompt = vi_stem + "\n\n" + "\n".join(vi_opts) + (
        "\n\nIn chữ cái, rồi một câu lý do."
    )
    test = (
        'String out = CjTestBase.capture(() -> Solution.program());\n'
        'CjTestBase.checkTrue(out.startsWith("' + ans + '"), "answer must start with the correct letter");'
    )
    return (
        challenge(cid, "Exam MCQ", prompt, BOILER_E1, [(ans + " exam", test, why[:380])], level="independent", difficulty="advanced"),
        vi_challenge("Câu thi trắc nghiệm", vi_prompt, [(ans + " exam", vi_why[:380])]),
    )

P1, V1 = mcq("apx-m21-q1", Q1_S, Q1_O, "B", Q1_W, Q1_VS, Q1_VO, Q1_VW)
P2, V2 = mcq("apx-m21-q2", Q2_S, Q2_O, "A", Q2_W, Q2_VS, Q2_VO, Q2_VW)
P3, V3 = mcq("apx-m21-q3", Q3_S, Q3_O, "A", Q3_W, Q3_VS, Q3_VO, Q3_VW)
P4, V4 = mcq("apx-m21-q4", Q4_S, Q4_O, "A", Q4_W, Q4_VS, Q4_VO, Q4_VW)

CP21 = challenge(
    "apx-cp-m21-frq",
    "Exam FRQ: the toll booth",
    "45-minute FRQ section. Implement the `TollBooth` class:\n\n"
    "- constructor takes the toll amount (int cents)\n"
    "- `pay(int paid)` records a payment; returns the change due "
    "(paid - toll, floored at 0)\n- `shortfall(int paid)` returns "
    "toll - paid when paid is less than toll, else 0\n"
    "- `totalCollected()` returns the sum of ALL toll amounts "
    "actually collected (min(paid, toll) per payment; reset by "
    "`endDay()`)\n- `endDay()` returns the day's total and resets "
    "it\n\nImplement the full class.",
    r"""public class Solution {
    public static class TollBooth {
        public TollBooth(int toll) {
        }

        public int pay(int paid) {
            return 0;
        }

        public int shortfall(int paid) {
            return 0;
        }

        public int totalCollected() {
            return 0;
        }

        public int endDay() {
            return 0;
        }
    }
}
""",
    [(
        "toll booth frq",
        r"""
Solution.TollBooth t = new Solution.TollBooth(300);
CjTestBase.checkEq(t.pay(500), 200, "change for overpay");
CjTestBase.checkEq(t.shortfall(200), 100, "short by 100");
CjTestBase.checkEq(t.pay(300), 0, "exact payment");
CjTestBase.checkEq(t.totalCollected(), 600, "min(paid, toll) summed");
CjTestBase.checkEq(t.endDay(), 600, "day total");
CjTestBase.checkEq(t.totalCollected(), 0, "reset by endDay");
""",
        "pay returns max(0, paid - toll); shortfall max(0, toll - paid); collect min(paid, toll); endDay reads-and-resets.",
    )],
    level="mini-build",
    difficulty="advanced",
)

VI_CP21 = vi_challenge(
    "FRQ thi: trạm thu phí",
    "Phần FRQ 45 phút. Cài lớp `TollBooth`:\n\n"
    "- constructor nhận số tiền phí (int xu)\n"
    "- `pay(int paid)` ghi nhận một khoản trả; trả tiền thừa "
    "(paid - toll, chặn sàn 0)\n- `shortfall(int paid)` trả toll - paid "
    "khi paid nhỏ hơn toll, nếu không 0\n- `totalCollected()` trả tổng "
    "MỌI khoản phí thực thu (min(paid, toll) mỗi lần trả; được reset "
    "bởi `endDay()`)\n- `endDay()` trả tổng ngày và reset nó\n\n"
    "Cài lớp trọn vẹn.",
    [("toll booth frq", "pay trả max(0, paid - toll); shortfall max(0, toll - paid); thu min(paid, toll); endDay đọc-và-reset.")],
)

write_practice(
    M, "apx-p21-exam", "Exam #1: MCQ section",
    "Four original exam-weight MCQs; timed half-section (20 minutes).",
    "Đề #1: phần trắc nghiệm",
    "Bốn câu trắc nghiệm gốc trọng lượng đề thi; nửa phần có giờ (20 phút).",
    after_lesson="apx-m21-rules", minutes=25, difficulty="advanced",
    challenges=[P1, P2, P3, P4],
    vi_challenges={"apx-m21-q1": V1, "apx-m21-q2": V2, "apx-m21-q3": V3, "apx-m21-q4": V4},
    solutions=[
        ("apx-m21-q1", BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. pass two keeps the max strictly below 4, which is 2.");'), BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("C. forgot strictly-below.");')),
        ("apx-m21-q2", BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. 3*2*1 = 6.");'), BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. stopped early.");')),
        ("apx-m21-q3", BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. backward removal cannot skip.");'), BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("C. forward loop reintroduces the bug.");')),
        ("apx-m21-q4", BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. 5! = 120.");'), BOILER_E1.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. summed instead of multiplying.");')),
    ],
)

write_checkpoint(
    M, "apx-cp-m21", "Checkpoint: exam #1 FRQ",
    "The toll booth: payment, shortfall, day total, and the reset rule.",
    25,
    r"""
Four behaviors, one class, one reset rule — the FRQ2 shape at
simulation weight. Bank pay() and shortfall() first (mirror
images), then the collection accumulator, then endDay's
read-and-reset. The mirror-image pair is the speedup: write one,
write the other by symmetry, and check both against zero.
""",
    "Điểm kiểm tra: FRQ đề #1",
    "Trạm thu phí: thanh toán, thiếu hụt, tổng ngày, và luật reset.",
    r"""
Bốn hành vi, một lớp, một luật reset — hình dạng FRQ2 với trọng
lượng mô phỏng. Giữ pay() và shortfall() trước (hai ảnh gương), rồi
bộ tích lũy thu phí, rồi read-and-reset của endDay. Cặp ảnh-gương là
tốc độ: viết một cái, viết cái kia theo đối xứng, và đối chiếu cả
hai với số 0.
""",
    CP21,
    VI_CP21,
    solution=r"""public class Solution {
    public static class TollBooth {
        private int toll;
        private int collected;

        public TollBooth(int toll) {
            this.toll = toll;
            collected = 0;
        }

        public int pay(int paid) {
            collected += Math.min(paid, toll);
            return Math.max(0, paid - toll);
        }

        public int shortfall(int paid) {
            return Math.max(0, toll - paid);
        }

        public int totalCollected() {
            return collected;
        }

        public int endDay() {
            int day = collected;
            collected = 0;
            return day;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class TollBooth {
        private int toll;
        private int collected;

        public TollBooth(int toll) {
            this.toll = toll;
            collected = 0;
        }

        public int pay(int paid) {
            // BUG: collects the full payment even on shortfalls
            collected += paid;
            return Math.max(0, paid - toll);
        }

        public int shortfall(int paid) {
            return Math.max(0, toll - paid);
        }

        public int totalCollected() {
            return collected;
        }

        public int endDay() {
            int day = collected;
            collected = 0;
            return day;
        }
    }
}
""",
)

print("M21 done")
