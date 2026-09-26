#!/usr/bin/env python3
"""AP CSA Advanced M23 — Full Practice Exam #3 (independent simulation)."""
from apx import *

M = "apx-exam3"

write_module(
    M,
    "Full Practice Exam #3",
    "The third independent simulation: multi-concept synthesis under time, with the strictest analysis yet. Difficulty E5.",
    "Đề thi thử trọn vẹn #3",
    "Mô phỏng độc lập thứ ba: tổng hợp đa khái niệm dưới áp lực giờ, với phép phân tích nghiêm ngặt nhất. Độ khó E5.",
    lessons=["apx-m23-rules", "apx-m23-synthesis", "apx-m23-compare", "apx-cp-m23"],
    practices=["apx-p23-exam"],
)

L1 = r"""
Exam #3 raises synthesis: items fuse two mechanisms where Exams
#1–2 fused one mechanism with a trap. Expect a trace that requires
an object AND a static, an implementation that requires string
parsing AND list mutation, a debugging item whose symptom appears
two behaviors away from the bug. The rules are identical — timed
halves, no blanks, justification on every MCQ — but expect to FEEL
the difference: these items consume their entire budget by design.

Triage matters most here. Two of the four MCQs are solvable in a
minute; the other two are budget-eaters. Finding which is which
in the first pass is worth more than raw speed anywhere.
"""

L2 = r"""
**Synthesis reading.** When an item visibly fuses mechanisms,
decompose in this order:

1. **Name the data journey**: input type → transformation(s) →
   output type. Write the arrow chain; every arrow is one code
   segment.
2. **Locate the interaction**: the difficulty lives where the
   segments meet (a parsed value feeds a list index; a static
   counter outlives the loop). Write that sentence explicitly.
3. **Implement segment-by-segment**, testing each against a
   one-element example before composing. Fused code written
   all-at-once fails in fused ways that are miserable to trace.

The FRQ here (the studio below) is a three-mechanism class:
numeric state, a list, and a text lookup. Do the three
independently bankable parts FIRST — synthesis FRQs are where
partial-credit discipline pays the most.
"""

L3 = r"""
**The three-exam comparison.** With three simulations scored, you
have enough data for the pre-master verdict:

- **Accuracy trend** across #1 → #2 → #3: rising is readiness.
  Flat-below-target for two exams running: pick the single worst
  mechanism from the trap maps and re-run its module before the
  master simulation.
- **Time stability**: if median time dropped while accuracy held,
  your verification is now affordable — the master sim rewards
  exactly that.
- **Trap-map diversity**: misses spread across many traps with
  falling frequency is the healthy decay curve; misses
  concentrated on one trap that persists is a known bug you are
  choosing to carry into the master.

Decide now: run the master simulation (module 24) only after the
trend is rising or flat-high. The master's purpose is to certify
readiness, not to discover you needed one more week — that
discovery is what #1–#3 are for.
"""

VI_L1 = r"""
Đề #3 nâng tổng hợp: các câu trộn hai cơ chế ở nơi Đề #1–2 trộn một
cơ chế với một cái bẫy. Kỳ vọng một truy vết đòi hỏi một đối tượng
VÀ một static, một bản cài đòi hỏi phân-tích-chuỗi VÀ biến-đổi-
danh-sách, một bài gỡ lỗi mà triệu chứng xuất hiện cách lỗi hai lần
hành vi. Luật không đổi — hai nửa có giờ, không chỗ trống, lý do cho
mọi câu trắc nghiệm — nhưng kỳ vọng cảm nhận: các câu này tiêu hết
ngân sách của chúng một cách chủ đích.

Phân loại quan trọng nhất ở đây. Hai trong bốn câu trắc nghiệm giải
được trong một phút; hai câu còn lại ăn-ngân-sách. Tìm ra cái nào là
cái nào trong lượt đầu đáng hơn tốc độ thô ở bất kỳ đâu.
"""

VI_L2 = r"""
**Đọc tổng hợp.** Khi một câu nhìn rõ là trộn cơ chế, phân rã theo
thứ tự:

1. **Gọi tên hành-trình-dữ-liệu**: kiểu đầu vào → (các) phép biến
   đổi → kiểu đầu ra. Viết chuỗi mũi tên; mỗi mũi tên là một đoạn mã.
2. **Định vị tương tác**: độ khó nằm nơi các đoạn gặp nhau (một giá
   trị phân tích được cấp cho chỉ số danh sách; một bộ đếm static
   sống lâu hơn vòng lặp). Viết câu đó một cách tường minh.
3. **Cài từng đoạn**, kiểm từng đoạn với ví dụ một-phần-tử trước khi
   ghép. Mã hợp nhất viết một-lần-thổi thường hỏng theo kiểu hợp nhất
   — truy vết cực khổ.

FRQ ở đây (studio dưới đây) là lớp ba-cơ-chế: trạng thái số, một
danh sách, và một tra-cứu-văn-bản. Làm ba phần dễ-giữ độc lập
TRƯỚC — FRQ tổng hợp là nơi kỷ luật điểm-một-phần trả lời nhiều nhất.
"""

VI_L3 = r"""
**Phép so sánh ba đề.** Với ba mô phỏng đã chấm, bạn có đủ dữ liệu
cho phán quyết tiền-thạc-sĩ:

- **Xu hướng độ chính xác** qua #1 → #2 → #3: đi lên là sẵn sàng.
  Phẳng-dưới-mục tiêu hai đề liên tiếp: chọn cơ chế xấu nhất từ bản
  đồ bẫy và chạy lại module của nó trước mô phỏng thạc sĩ.
- **Ổn định thời gian**: nếu thời gian trung vị giảm trong khi độ
  chính xác giữ vững, việc kiểm chứng của bạn giờ phải trả được —
  mô phỏng thạc sĩ thưởng đúng điều đó.
- **Độ đa dạng bản-đồ-bẫy**: các câu sai rải trên nhiều bẫy với tần
  suất giảm là đường suy giảm lành mạnh; các câu sai dồn vào một bẫy
  dai dẳng là một lỗi đã-biết mà bạn đang chọn mang vào kỳ thạc sĩ.

Quyết định ngay: chỉ chạy mô phỏng thạc sĩ (module 24) sau khi xu
hướng đi lên hoặc phẳng-cao. Mục đích của thạc sĩ là chứng nhận sự
sẵn sàng, không phải khám phá ra bạn cần thêm một tuần — khám phá
đó là việc của #1–#3.
"""

BOILER_E3 = r"""public class Solution {
    public static void program() {
        // Print your answer: the option letter, then a one-sentence reason.
    }
}
"""

Q1_S = "What is printed? (An object AND a static are involved.)\n\n```java\npublic class Gadget {\n    private static int made = 0;\n    private int id;\n    public Gadget() { made++; id = made * 2; }\n    public int getId() { return id; }\n    public static int total() { return made; }\n}\n\nGadget a = new Gadget();\nGadget b = new Gadget();\nGadget c = new Gadget();\nSystem.out.print(Gadget.total() + \",\" + b.getId());\n```"
Q1_O = ["A. `3,4`", "B. `2,4`", "C. `3,6`", "D. `6,4`"]
Q1_W = "A. made counts all three constructions (3); the SECOND gadget's id is 2 * 2 = 4. B reads the wrong ledger; C reads the third gadget's id; D doubles the wrong thing."
Q1_VS = "Chương trình in gì? (Có cả đối tượng VÀ static.)\n\n```java\npublic class Gadget {\n    private static int made = 0;\n    private int id;\n    public Gadget() { made++; id = made * 2; }\n    public int getId() { return id; }\n    public static int total() { return made; }\n}\n\nGadget a = new Gadget();\nGadget b = new Gadget();\nGadget c = new Gadget();\nSystem.out.print(Gadget.total() + \",\" + b.getId());\n```"
Q1_VO = ["A. `3,4`", "B. `2,4`", "C. `3,6`", "D. `6,4`"]
Q1_VW = "A. made đếm cả ba lần tạo (3); id của gadget THỨ HAI là 2 * 2 = 4. B đọc nhầm sổ; C đọc id của gadget thứ ba; D nhân đôi nhầm thứ."

Q2_S = "What does this return for `s = \"aXbXc\"`?\n\n```java\npublic static int countAfter(String s, char first, char second) {\n    int count = 0;\n    for (int i = 1; i < s.length(); i++) {\n        if (s.charAt(i - 1) == first && s.charAt(i) == second) {\n            count++;\n        }\n    }\n    return count;\n}\n```\nCalled as `countAfter(\"aXbXc\", 'X', 'b')`."
Q2_O = ["A. 2", "B. 1", "C. 0", "D. 3"]
Q2_W = "B. The adjacent pair (X, b) occurs once (indexes 2-3); the other X is followed by 'c'. A counts every X; C tests the pair reversed; D counts nothing real."
Q2_VS = "Đoạn này trả bao nhiêu với `s = \"aXbXc\"`?\n\n```java\npublic static int countAfter(String s, char first, char second) {\n    int count = 0;\n    for (int i = 1; i < s.length(); i++) {\n        if (s.charAt(i - 1) == first && s.charAt(i) == second) {\n            count++;\n        }\n    }\n    return count;\n}\n```\nGọi `countAfter(\"aXbXc\", 'X', 'b')`."
Q2_VO = ["A. 2", "B. 1", "C. 0", "D. 3"]
Q2_VW = "B. Cặp liền kề (X, b) xuất hiện một lần (chỉ số 2-3); X còn lại đứng trước 'c'. A đếm mọi X; C thử cặp đảo ngược; D đếm thứ không có thật."

Q3_S = "Which statement about this code is TRUE?\n\n```java\nArrayList<String> list = new ArrayList<String>();\nlist.add(\"a\");\nlist.add(\"b\");\nfor (String item : list) {\n    if (item.equals(\"a\")) { list.remove(item); }\n}\n```"
Q3_O = ["A. It removes \"a\" safely", "B. It throws ConcurrentModificationException", "C. It removes nothing", "D. It removes both elements"]
Q3_W = "B. Removing from an ArrayList inside a for-each loop invalidates the iterator — the AP subset tests exactly this crash. A is the forward-index thinking that only applies to index loops; C/D misread the loop."
Q3_VS = "Câu nào đúng về đoạn mã này?\n\n```java\nArrayList<String> list = new ArrayList<String>();\nlist.add(\"a\");\nlist.add(\"b\");\nfor (String item : list) {\n    if (item.equals(\"a\")) { list.remove(item); }\n}\n```"
Q3_VO = ["A. Nó xóa \"a\" an toàn", "B. Nó ném ConcurrentModificationException", "C. Nó không xóa gì", "D. Nó xóa cả hai phần tử"]
Q3_VW = "B. Xóa khỏi ArrayList bên trong vòng for-each làm Iterator bất hợp lệ — tập con AP kiểm tra đúng cái sập này. A là tư duy chỉ-số-tới chỉ áp dụng cho vòng theo chỉ số; C/D đọc sai vòng lặp."

Q4_S = "What is printed?\n\n```java\nint[][] g = {{1, 2, 3}, {4, 5, 6}};\nint sum = 0;\nfor (int c = 0; c < g[0].length; c++) {\n    sum += g[0][c];\n}\nfor (int r = 0; r < g.length; r++) {\n    sum += g[r][0];\n}\nsum -= g[0][0];\nSystem.out.print(sum);\n```"
Q4_O = ["A. 10", "B. 12", "C. 21", "D. 15"]
Q4_W = "A. Row sum (1+2+3=6) plus column sum (1+4=5) minus the double-counted corner g[0][0]=1 → 6+5-1 = 10. B subtracts the corner twice; C sums the whole grid; D forgets the corner subtraction."
Q4_VS = "Chương trình in gì?\n\n```java\nint[][] g = {{1, 2, 3}, {4, 5, 6}};\nint sum = 0;\nfor (int c = 0; c < g[0].length; c++) {\n    sum += g[0][c];\n}\nfor (int r = 0; r < g.length; r++) {\n    sum += g[r][0];\n}\nsum -= g[0][0];\nSystem.out.print(sum);\n```"
Q4_VO = ["A. 10", "B. 12", "C. 21", "D. 15"]
Q4_VW = "A. Tổng hàng đầu (1+2+3=6) cộng cột đầu (1+4=5) trừ góc bị đếm trùng g[0][0]=1 → 6+5-1 = 10. B trừ góc hai lần; C cộng cả lưới; D quên phép trừ góc."

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
        challenge(cid, "Exam MCQ", prompt, BOILER_E3, [(ans + " exam", test, why[:380])], level="independent", difficulty="advanced"),
        vi_challenge("Câu thi trắc nghiệm", vi_prompt, [(ans + " exam", vi_why[:380])]),
    )

P1, V1 = mcq("apx-m23-q1", Q1_S, Q1_O, "A", Q1_W, Q1_VS, Q1_VO, Q1_VW)
P2, V2 = mcq("apx-m23-q2", Q2_S, Q2_O, "B", Q2_W, Q2_VS, Q2_VO, Q2_VW)
P3, V3 = mcq("apx-m23-q3", Q3_S, Q3_O, "B", Q3_W, Q3_VS, Q3_VO, Q3_VW)
P4, V4 = mcq("apx-m23-q4", Q4_S, Q4_O, "A", Q4_W, Q4_VS, Q4_VO, Q4_VW)

CP23 = challenge(
    "apx-cp-m23-frq",
    "Exam FRQ: the recording studio",
    "45-minute FRQ. Implement the `Studio` class (three mechanisms):\n\n"
    "- constructor takes the hourly rate (int cents)\n"
    "- `book(String band)` adds the band's name to the booking list "
    "if not already booked (returns true; false when already present "
    "— no duplicates)\n- `bill(String band, int hours)` returns "
    "rate * hours for a BOOKED band, or 0 for an unbooked one\n"
    "- `roster()` returns the number of booked bands (no duplicates "
    "counted)\n- `endMonth()` returns the total billed across all "
    "bill() calls and resets the billing total (bookings persist)\n\n"
    "Implement the class.",
    r"""public class Solution {
    public static class Studio {
        public Studio(int rate) {
        }

        public boolean book(String band) {
            return false;
        }

        public int bill(String band, int hours) {
            return 0;
        }

        public int roster() {
            return 0;
        }

        public int endMonth() {
            return 0;
        }
    }
}
""",
    [(
        "studio frq",
        r"""
Solution.Studio s = new Solution.Studio(1000);
CjTestBase.checkTrue(s.book("Nova"), "first booking");
CjTestBase.checkTrue(!s.book("Nova"), "no duplicates");
CjTestBase.checkEq(s.bill("Nova", 3), 3000, "booked band billed");
CjTestBase.checkEq(s.bill("Ghost", 5), 0, "unbooked band bills nothing");
CjTestBase.checkEq(s.roster(), 1, "one unique band");
CjTestBase.checkEq(s.endMonth(), 3000, "month total");
CjTestBase.checkEq(s.bill("Nova", 2), 2000, "billing continues");
""",
        "Three mechanisms: a guarded list insert (contains check), a membership-gated charge, and a read-and-reset total.",
    )],
    level="mini-build",
    difficulty="advanced",
)

VI_CP23 = vi_challenge(
    "FRQ thi: phòng thu",
    "FRQ 45 phút. Cài lớp `Studio` (ba cơ chế):\n\n"
    "- constructor nhận giá theo giờ (int xu)\n"
    "- `book(String band)` thêm tên ban vào danh sách đặt nếu chưa đặt "
    "(trả true; false khi đã có — không trùng)\n- `bill(String band, "
    "int hours)` trả rate * hours cho ban ĐÃ ĐẶT, hoặc 0 cho ban chưa "
    "đặt\n- `roster()` trả số ban đã đặt (không đếm trùng)\n"
    "- `endMonth()` trả tổng đã tính qua mọi lời gọi bill() và reset "
    "tổng (các lượt đặt vẫn giữ)\n\nCài lớp.",
    [("studio frq", "Ba cơ chế: chèn danh sách có biến chặn (kiểm tra contains), khoản tính-được-chặn-bởi-thành-viên, và tổng đọc-và-reset.")],
)

write_practice(
    M, "apx-p23-exam", "Exam #3: MCQ section",
    "Four synthesis originals; timed half-section (20 minutes).",
    "Đề #3: phần trắc nghiệm",
    "Bốn câu gốc tổng hợp; nửa phần có giờ (20 phút).",
    after_lesson="apx-m23-rules", minutes=25, difficulty="advanced",
    challenges=[P1, P2, P3, P4],
    vi_challenges={"apx-m23-q1": V1, "apx-m23-q2": V2, "apx-m23-q3": V3, "apx-m23-q4": V4},
    solutions=[
        ("apx-m23-q1", BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. made counts 3 constructions; second id is 4.");'), BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("C. read the third gadget instead of the second.");')),
        ("apx-m23-q2", BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. only one X is followed by b.");'), BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. counted every X regardless of what follows.");')),
        ("apx-m23-q3", BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. for-each plus remove crashes the iterator.");'), BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. that reasoning belongs to index loops.");')),
        ("apx-m23-q4", BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. edge sum per the options; verify the corner arithmetic.");'), BOILER_E3.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("C. summed the entire grid.");')),
    ],
)

write_checkpoint(
    M, "apx-cp-m23", "Checkpoint: exam #3 FRQ",
    "Three mechanisms in one class: guarded insert, gated charge, reset total.",
    25,
    r"""
The studio fuses the parking garage (guarded insert), the
register (gated charge), and the toll booth (read-and-reset) —
three bankable parts you have already built. Recognizing that is
the lesson: synthesis FRQs are old parts in a new chassis. Bank
all three, then wire them.
""",
    "Điểm kiểm tra: FRQ đề #3",
    "Ba cơ chế trong một lớp: chèn có chặn, tính có cổng, tổng có reset.",
    r"""
Studio ghép bãi đỗ xe (chèn có chặn), máy thu ngân (tính có cổng),
và trạm thu phí (đọc-và-reset) — ba phần dễ-giữ bạn đã dựng rồi.
Nhận ra điều đó chính là bài học: FRQ tổng hợp là các phần cũ trong
một khung mới. Giữ cả ba, rồi đấu nối.
""",
    CP23,
    VI_CP23,
    solution=r"""public class Solution {
    public static class Studio {
        private int rate;
        private java.util.ArrayList<String> bands = new java.util.ArrayList<String>();
        private int billed;

        public Studio(int rate) {
            this.rate = rate;
        }

        public boolean book(String band) {
            if (bands.contains(band)) {
                return false;
            }
            bands.add(band);
            return true;
        }

        public int bill(String band, int hours) {
            if (!bands.contains(band)) {
                return 0;
            }
            int amount = rate * hours;
            billed += amount;
            return amount;
        }

        public int roster() {
            return bands.size();
        }

        public int endMonth() {
            int month = billed;
            billed = 0;
            return month;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Studio {
        private int rate;
        private java.util.ArrayList<String> bands = new java.util.ArrayList<String>();
        private int billed;

        public Studio(int rate) {
            this.rate = rate;
        }

        public boolean book(String band) {
            // BUG: no duplicate guard — roster inflates
            bands.add(band);
            return true;
        }

        public int bill(String band, int hours) {
            if (!bands.contains(band)) {
                return 0;
            }
            int amount = rate * hours;
            billed += amount;
            return amount;
        }

        public int roster() {
            return bands.size();
        }

        public int endMonth() {
            int month = billed;
            billed = 0;
            return month;
        }
    }
}
""",
)

print("M23 done")
