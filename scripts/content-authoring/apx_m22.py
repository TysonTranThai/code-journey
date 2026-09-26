#!/usr/bin/env python3
"""AP CSA Advanced M22 — Full Practice Exam #2 (different traps)."""
from apx import *

M = "apx-exam2"

write_module(
    M,
    "Full Practice Exam #2",
    "An independent simulation: new contexts, subtler traps, same rules — timed, analyzed, debriefed. Difficulty E5.",
    "Đề thi thử trọn vẹn #2",
    "Một mô phỏng độc lập: bối cảnh mới, bẫy tinh vi hơn, cùng luật — có giờ, phân tích, tranh luận. Độ khó E5.",
    lessons=["apx-m22-rules", "apx-m22-analysis", "apx-m22-trapmap", "apx-cp-m22"],
    practices=["apx-p22-exam"],
)

L1 = r"""
Exam #2 changes the traps, not the topics. Where Exam #1 tested
whether you knew the mechanism, this one tests whether you hold it
under misdirection:

- **The dead-variable trap**: a plausible variable is updated and
  never read — options built on it are wrong.
- **The near-miss clause**: the spec says "at least 3"; the code
  and three options say "> 3". Only one option honors the clause.
- **The order trap**: two mutations commute in the example but not
  in general; the options include the commuting reading.
- **The mirror trap**: a correct-looking symmetric pairing (i ↔
  length - i) applied where the data is NOT symmetric.

Strategy is unchanged — triage, banking, the no-blanks rule — but
your expectation should shift: in Exam #2, the first answer that
"looks right" is disproportionately the trap. Verification beats
recognition one notch harder here.
"""

L2 = r"""
**The trap map.** After scoring, mark each miss with the trap that
caught you:

- Misread clause → drill the operator-circling ritual.
- Dead variable → you predicted from vibes, not the table; drill
  state-table tracing.
- Order assumption → you simulated the example, not the code;
  drill two-key-trace (module 2's aliasing set).
- Mirror misapplication → you generalized a pattern the data
  doesn't support; drill boundary-case testing first.

The map matters because the four traps have different cures.
"Tried hard, lost points" is not a diagnosis; "I assumed commuted
mutations" is. Four misses from four different traps mean the
issue is pacing (rushing); four from the same trap mean the issue
is that mechanism — go re-run its module.
"""

L3 = r"""
**Comparing simulations.** Exam #2 versus Exam #1 is your first
real trend line. Compare three numbers: accuracy, median time,
and (new) trap diversity. Improving accuracy with unchanged time
is the healthy signature — accuracy up BECAUSE time collapsed
usually means you skipped verification, which the trap density
here punishes.

If Exam #2 scored lower than #1: check whether the misses
concentrated in the second half. That is stamina, not knowledge —
the cure is shorter, more frequent simulations, not more review.
If it scored higher across the board with faster times, you are
ready for the master simulation's conditions.
"""

VI_L1 = r"""
Đề #2 đổi bẫy, không đổi chủ đề. Ở đâu Đề #1 kiểm tra việc bạn có
biết cơ chế, bài này kiểm tra việc bạn giữ được nó dưới đánh lạc
hướng:

- **Bẫy biến chết**: một biến đáng tin được cập nhật và không bao
  giờ được đọc — các phương án dựa trên nó đều sai.
- **Mệnh đề suýt-khớp**: đặc tả nói "ít nhất 3"; mã và ba phương án
  nói "> 3". Chỉ một phương án tôn trọng mệnh đề.
- **Bẫy thứ tự**: hai phép biến đổi hoán đổi được trong ví dụ nhưng
  không trong tổng quát; các phương án gồm cả cách đọc hoán-đổi-được.
- **Bẫy đối xứng**: một cặp đôi đối xứng trông đúng (i ↔ độ dài - i)
  áp dụng nơi dữ liệu KHÔNG đối xứng.

Chiến lược không đổi — phân loại, giữ điểm, luật không-chỗ-trống —
nhưng kỳ vọng của bạn nên dịch chuyển: trong Đề #2, đáp án đầu tiên
"trông đúng" bất thường hay là bẫy. Kiểm chứng ở đây cần mạnh hơn
nhận dạng một bậc.
"""

VI_L2 = r"""
**Bản đồ bẫy.** Sau khi chấm, đánh dấu mỗi câu sai bằng cái bẫy đã
bắt bạn:

- Đọc sai mệnh đề → luyện nghi thức khoanh toán tử.
- Biến chết → bạn đã dự đoán bằng cảm tính, không phải bảng; luyện
  truy vết bảng-trạng-thái.
- Giả định thứ tự → bạn mô phỏng ví dụ, không phải mã; luyện
  truy-vết-hai-khóa (bộ bí danh của module 2).
- Áp dụng đối xứng sai → bạn khái quát một mẫu mà dữ liệu không
  hỗ trợ; luyện kiểm-thử-biên-trước.

Bản đồ quan trọng vì bốn cái bẫy có thuốc chữa khác nhau. "Đã cố
hết sức mà mất điểm" không phải chẩn đoán; "tôi đã giả định các phép
biến đổi hoán đổi được" mới là. Bốn câu sai từ bốn bẫy khác nhau
nghĩa là vấn đề là nhịp độ (vội); bốn câu từ cùng một bẫy nghĩa là
vấn đề là cơ chế đó — hãy chạy lại module của nó.
"""

VI_L3 = r"""
**So sánh các mô phỏng.** Đề #2 so với Đề #1 là đường xu hướng thật
đầu tiên của bạn. So sánh ba con số: độ chính xác, thời gian trung
vị, và (mới) độ đa dạng bẫy. Độ chính xác tăng với thời gian không
đổi là chữ ký lành mạnh — độ chính xác tăng VÌ thời gian sụp đổ
thường có nghĩa là bạn bỏ qua kiểm chứng, điều mà mật độ bẫy ở đây
trừng phạt.

Nếu Đề #2 điểm thấp hơn #1: kiểm tra xem các câu sai có dồn vào nửa
sau không. Đó là sức bền, không phải kiến thức — thuốc là các mô
phỏng ngắn hơn, thường xuyên hơn, không phải ôn thêm. Nếu điểm cao
hơn trên mọi mặt với thời gian nhanh hơn, bạn đã sẵn sàng cho điều
kiện của mô phỏng thạc sĩ.
"""

BOILER_E2 = r"""public class Solution {
    public static void program() {
        // Print your answer: the option letter, then a one-sentence reason.
    }
}
"""

Q1_S = "What is printed? (Watch for the dead variable.)\n\n```java\nint total = 0;\nint spare = 0;\nint[] a = {2, 5, 1};\nfor (int v : a) {\n    total += v;\n    spare += v * 2;\n}\nspare = 0;\nSystem.out.print(total + \",\" + spare);\n```"
Q1_O = ["A. `8,16`", "B. `8,0`", "C. `0,16`", "D. `16,0`"]
Q1_W = "B. total accumulates to 8; spare accumulates to 16 but is then overwritten to 0 before printing. A forgets the overwrite — the dead-variable trap."
Q1_VS = "Chương trình in gì? (Chú ý biến chết.)\n\n```java\nint total = 0;\nint spare = 0;\nint[] a = {2, 5, 1};\nfor (int v : a) {\n    total += v;\n    spare += v * 2;\n}\nspare = 0;\nSystem.out.print(total + \",\" + spare);\n```"
Q1_VO = ["A. `8,16`", "B. `8,0`", "C. `0,16`", "D. `16,0`"]
Q1_VW = "B. total tích lũy tới 8; spare tích lũy tới 16 nhưng bị ghi đè thành 0 trước khi in. A quên phép ghi đè — bẫy biến chết."

Q2_S = "The spec says: return true when the list contains **at least 3** matches. Which implementation is correct?"
Q2_O = ["A. `count > 3`", "B. `count >= 3`", "C. `count >= 2`", "D. `count == 3`"]
Q2_W = "B. 'At least 3' is count >= 3. A is the near-miss clause (> 3); C answers 'at least 2'; D answers 'exactly 3'."
Q2_VS = "Đặc tả nói: trả true khi danh sách chứa **ít nhất 3** lần khớp. Bản cài đặt nào đúng?"
Q2_VO = ["A. `count > 3`", "B. `count >= 3`", "C. `count >= 2`", "D. `count == 3`"]
Q2_VW = "B. 'Ít nhất 3' là count >= 3. A là mệnh đề suýt-khớp (> 3); C trả lời 'ít nhất 2'; D trả lời 'đúng 3'."

Q3_S = "What is printed?\n\n```java\nStringBuilder s = new StringBuilder(\"ab\");\ns.insert(1, \"X\");\ns.deleteCharAt(0);\nSystem.out.print(s);\n```"
Q3_O = ["A. `Xb`", "B. `ab`", "C. `bX`", "D. `Xa`"]
Q3_W = "A. insert(1) gives aXb; deleteCharAt(0) removes 'a' → Xb. B ignores both; C has the operations backwards; D deletes the wrong end."
Q3_VS = "Chương trình in gì?\n\n```java\nStringBuilder s = new StringBuilder(\"ab\");\ns.insert(1, \"X\");\ns.deleteCharAt(0);\nSystem.out.print(s);\n```"
Q3_VO = ["A. `Xb`", "B. `ab`", "C. `bX`", "D. `Xa`"]
Q3_VW = "A. insert(1) cho aXb; deleteCharAt(0) xóa 'a' → Xb. B bỏ qua cả hai; C đảo ngược hai phép toán; D xóa nhầm đầu."

Q4_S = "What does this return for `grid = {{1,2},{3,4}}`?\n\n```java\npublic static int diag(int[][] g) {\n    int sum = 0;\n    for (int i = 0; i < g.length; i++) {\n        sum += g[i][g.length - 1 - i];\n    }\n    return sum;\n}\n```"
Q4_O = ["A. 5 (main diagonal)", "B. 6 (anti-diagonal)", "C. 4", "D. 10"]
Q4_W = "B. The index g[i][length-1-i] walks the anti-diagonal: g[0][1] + g[1][0] = 2 + 4 = 6. A is the mirror misapplication (the main diagonal is g[i][i]); D sums everything."
Q4_VS = "Đoạn này trả bao nhiêu với `grid = {{1,2},{3,4}}`?\n\n```java\npublic static int diag(int[][] g) {\n    int sum = 0;\n    for (int i = 0; i < g.length; i++) {\n        sum += g[i][g.length - 1 - i];\n    }\n    return sum;\n}\n```"
Q4_VO = ["A. 5 (đường chéo chính)", "B. 6 (đường chéo phụ)", "C. 4", "D. 10"]
Q4_VW = "B. Chỉ số g[i][độ dài-1-i] đi trên đường chéo phụ: g[0][1] + g[1][0] = 2 + 4 = 6. A là áp-dụng-đối-xứng-sai (đường chéo chính là g[i][i]); D cộng tất cả."

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
        challenge(cid, "Exam MCQ", prompt, BOILER_E2, [(ans + " exam", test, why[:380])], level="independent", difficulty="advanced"),
        vi_challenge("Câu thi trắc nghiệm", vi_prompt, [(ans + " exam", vi_why[:380])]),
    )

P1, V1 = mcq("apx-m22-q1", Q1_S, Q1_O, "B", Q1_W, Q1_VS, Q1_VO, Q1_VW)
P2, V2 = mcq("apx-m22-q2", Q2_S, Q2_O, "B", Q2_W, Q2_VS, Q2_VO, Q2_VW)
P3, V3 = mcq("apx-m22-q3", Q3_S, Q3_O, "A", Q3_W, Q3_VS, Q3_VO, Q3_VW)
P4, V4 = mcq("apx-m22-q4", Q4_S, Q4_O, "B", Q4_W, Q4_VS, Q4_VO, Q4_VW)

CP22 = challenge(
    "apx-cp-m22-frq",
    "Exam FRQ: the recipe scaler",
    "45-minute FRQ section. Implement the `Recipe` class:\n\n"
    "- constructor takes the base servings (int) and base sugar "
    "(int grams)\n- `scaleTo(int servings)` returns the sugar needed "
    "for the requested servings: baseSugar * servings / baseServings "
    "(integer division)\n- `addServings(int extra)` increases the "
    "REMAINING planned servings (starts equal to baseServings; "
    "never below 0)\n- `remaining()` reports planned servings\n"
    "- `serve(int n)` reduces remaining by n, floored at 0, and "
    "returns true if there were enough servings planned, else "
    "false (changing nothing when false)\n\nImplement the class.",
    r"""public class Solution {
    public static class Recipe {
        public Recipe(int baseServings, int baseSugar) {
        }

        public int scaleTo(int servings) {
            return 0;
        }

        public void addServings(int extra) {
        }

        public int remaining() {
            return 0;
        }

        public boolean serve(int n) {
            return false;
        }
    }
}
""",
    [(
        "recipe scaler frq",
        r"""
Solution.Recipe r = new Solution.Recipe(4, 200);
CjTestBase.checkEq(r.scaleTo(6), 300, "200 * 6 / 4");
CjTestBase.checkEq(r.remaining(), 4, "starts at base");
r.serve(3);
CjTestBase.checkEq(r.remaining(), 1, "three served");
CjTestBase.checkTrue(!r.serve(2), "not enough planned");
CjTestBase.checkEq(r.remaining(), 1, "failed serve changed nothing");
r.addServings(4);
CjTestBase.checkEq(r.remaining(), 5, "servings added");
""",
        "scaleTo is proportion math with integer division; serve guards on n <= remaining before mutating.",
    )],
    level="mini-build",
    difficulty="advanced",
)

VI_CP22 = vi_challenge(
    "FRQ thi: máy chia tỷ lệ công thức",
    "Phần FRQ 45 phút. Cài lớp `Recipe`:\n\n"
    "- constructor nhận số khẩu phần gốc (int) và lượng đường gốc "
    "(int gram)\n- `scaleTo(int servings)` trả lượng đường cần cho số "
    "khẩu phần yêu cầu: baseSugar * servings / baseServings (chia số "
    "nguyên)\n- `addServings(int extra)` tăng số khẩu phần ĐÃ KẾ HOẠCH "
    "còn lại (khởi đầu bằng baseServings; không bao giờ dưới 0)\n"
    "- `remaining()` báo số khẩu phần kế hoạch\n- `serve(int n)` giảm "
    "số còn lại đi n, chặn sàn 0, và trả true nếu đủ khẩu phần đã kế "
    "hoạch, nếu không false (không đổi gì khi false)\n\nCài lớp.",
    [("recipe scaler frq", "scaleTo là phép toán tỷ lệ với chia số nguyên; serve chặn khi n <= remaining trước khi biến đổi.")],
)

write_practice(
    M, "apx-p22-exam", "Exam #2: MCQ section",
    "Four trap-weighted originals; timed half-section (20 minutes).",
    "Đề #2: phần trắc nghiệm",
    "Bốn câu gốc nhiều bẫy; nửa phần có giờ (20 phút).",
    after_lesson="apx-m22-rules", minutes=25, difficulty="advanced",
    challenges=[P1, P2, P3, P4],
    vi_challenges={"apx-m22-q1": V1, "apx-m22-q2": V2, "apx-m22-q3": V3, "apx-m22-q4": V4},
    solutions=[
        ("apx-m22-q1", BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. spare was overwritten to 0 before printing.");'), BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. forgot the dead-variable overwrite.");')),
        ("apx-m22-q2", BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. at least 3 is >= 3.");'), BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. near-miss: > 3 excludes exactly 3.");')),
        ("apx-m22-q3", BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. aXb then remove a -> Xb.");'), BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("C. applied the operations backwards.");')),
        ("apx-m22-q4", BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. g[i][len-1-i] is the anti-diagonal: 2+4.");'), BOILER_E2.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. mirror trap: that is the main diagonal.");')),
    ],
)

write_checkpoint(
    M, "apx-cp-m22", "Checkpoint: exam #2 FRQ",
    "The recipe scaler: proportion, guard-on-failure, and state floor.",
    25,
    r"""
The FRQ emphasizes the guarded transition: `serve` must decide
success BEFORE mutating — a return-first bug here flips the state
on failure. Bank scaleTo immediately (one line), then remaining/
addServings, then serve's guard-last discipline.
""",
    "Điểm kiểm tra: FRQ đề #2",
    "Máy chia tỷ lệ công thức: tỷ lệ, chặn-khi-thất-bại, và sàn trạng thái.",
    r"""
FRQ nhấn mạnh bước chuyển có-biến-chặn: `serve` phải quyết định thành
công TRƯỚC khi biến đổi — lỗi trả-sớm ở đây lật trạng thái khi thất
bại. Giữ scaleTo ngay (một dòng), rồi remaining/addServings, rồi kỷ
luật chặn-sau của serve.
""",
    CP22,
    VI_CP22,
    solution=r"""public class Solution {
    public static class Recipe {
        private int baseServings;
        private int baseSugar;
        private int planned;

        public Recipe(int baseServings, int baseSugar) {
            this.baseServings = baseServings;
            this.baseSugar = baseSugar;
            planned = baseServings;
        }

        public int scaleTo(int servings) {
            return baseSugar * servings / baseServings;
        }

        public void addServings(int extra) {
            planned += extra;
            if (planned < 0) {
                planned = 0;
            }
        }

        public int remaining() {
            return planned;
        }

        public boolean serve(int n) {
            if (n > planned) {
                return false;
            }
            planned -= n;
            return true;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Recipe {
        private int baseServings;
        private int baseSugar;
        private int planned;

        public Recipe(int baseServings, int baseSugar) {
            this.baseServings = baseServings;
            this.baseSugar = baseSugar;
            planned = baseServings;
        }

        public int scaleTo(int servings) {
            return baseSugar * servings / baseServings;
        }

        public void addServings(int extra) {
            planned += extra;
            if (planned < 0) {
                planned = 0;
            }
        }

        public int remaining() {
            return planned;
        }

        public boolean serve(int n) {
            // BUG: mutates BEFORE deciding success — failed serves still eat state
            planned -= n;
            if (planned < 0) {
                planned = 0;
                return false;
            }
            return true;
        }
    }
}
""",
)

print("M22 done")
