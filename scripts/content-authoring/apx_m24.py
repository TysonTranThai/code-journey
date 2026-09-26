#!/usr/bin/env python3
"""AP CSA Advanced M24 — Final AP CSA Master Simulation."""
from apx import *

M = "apx-master"

write_module(
    M,
    "Final Master Simulation",
    "The endgame assessment: unlabeled items across every mechanism — tracing, dispatch, mutation, FRQ synthesis — under exam rules. Difficulty E5.",
    "Mô phỏng thạc sĩ cuối cùng",
    "Bài đánh giá cuối: các câu không nhãn trên mọi cơ chế — truy vết, điều phối, biến đổi, tổng hợp FRQ — dưới luật phòng thi. Độ khó E5.",
    lessons=["apx-m24-protocol", "apx-m24-verdict", "apx-m24-after", "apx-cp-m24"],
    practices=["apx-p24-master"],
)

L1 = r"""
**Protocol.** This is the gate. Everything from modules 1–23 is
assumed; nothing is labeled; no mechanism is announced in advance.

- **Timing**: 20 minutes for the MCQ half-section, 25 minutes for
  the FRQ. Run a real clock; log actuals.
- **Sequence**: MCQ set first (no returns mid-set — the exam does
  not let you revisit Section 1 during Section 2), then the FRQ.
- **MCQs**: letter + one-sentence justification, as throughout.
- **The FRQ**: full class, four behaviors, no method stubs
  provided beyond signatures. Bank the two easy behaviors first
  (module 16 discipline), then the interaction, then the audit.

After scoring, write the verdict lesson (below) BEFORE reading
anything else — verdict first prevents score-grief rewriting the
analysis.
"""

L2 = r"""
**The verdict.** Score the simulation on the same three axes as
the exams (accuracy per mechanism, time variance, trap map), then
apply this rubric to decide what the result means:

- **≥ 85% accuracy, time within budget**: ready. The remaining
  risk is variance, not gaps — maintain with one mixed set per
  week until exam day.
- **70–85% accuracy**: nearly ready. One more cycle: the weakest
  mechanism's module → its timed set → this simulation again.
  The 48-hour spacing rule applies.
- **< 70% accuracy**: not yet — and the simulation did its job.
  The trap map will show one or two mechanisms dominating the
  misses. Re-run those modules' practices entirely, then Exam #3
  (module 23) as the re-entry sim, THEN return here.

No verdict is a judgment of ability — it is a routing decision
about the next seven days. The course's final lesson (below)
holds the after-plan.
"""

L3 = r"""
**After the master.** Whatever the verdict, the week before the
real exam is not for new material:

1. **One mixed set** (module 17) at half intensity — keep the
   classify-first reflex warm without fatigue.
2. **The operator-circling ritual** on any practice items you
   redo — the clause-reading habit decays fastest.
3. **The strategy module** (module 20) re-read the night before:
   pacing numbers, the no-blanks rule, the last-ten-minutes
   protocol. Sleep beats a sixth simulation, every time.
4. **Exam day**: triage bins, banked FRQ parts, boundary audit,
   no blanks. Everything else is noise.

You arrived here from Foundations, through Core, into this
course. The progression was designed to end with you walking
into the exam having already taken it — several times, under
worse conditions than the real thing provides. That is the
whole trick: the exam is calm because you have been here
before.
"""

VI_L1 = r"""
**Quy trình.** Đây là cánh cổng. Mọi thứ từ module 1–23 được giả
định; không gì được dán nhãn; không cơ chế nào được công bố trước.

- **Thời gian**: 20 phút cho nửa phần trắc nghiệm, 25 phút cho FRQ.
  Bấm đồng hồ thật; ghi số thực tế.
- **Trình tự**: bộ trắc nghiệm trước (không quay lại giữa bộ — đề
  thi không cho bạn xem lại Phần 1 trong Phần 2), rồi FRQ.
- **Trắc nghiệm**: chữ cái + một câu lý do, như xuyên suốt.
- **FRQ**: lớp trọn vẹn, bốn hành vi, không có mã khung nào ngoài
  chữ ký. Giữ hai hành vi dễ trước (kỷ luật module 16), rồi tương
  tác, rồi kiểm toán.

Sau khi chấm, viết bài phán quyết (dưới đây) TRƯỚC khi đọc bất cứ
gì khác — phán quyết trước ngăn nỗi-buồn-điểm viết lại phần phân
tích.
"""

VI_L2 = r"""
**Phán quyết.** Chấm mô phỏng trên cùng ba trục với các đề (độ chính
xác theo cơ chế, phương sai thời gian, bản đồ bẫy), rồi áp bảng này
để quyết định kết quả nghĩa là gì:

- **≥ 85% độ chính xác, thời gian trong ngân sách**: sẵn sàng. Rủi
  ro còn lại là phương sai, không phải khoảng trống — duy trì bằng
  một bộ hỗn hợp mỗi tuần tới ngày thi.
- **70–85%**: gần sẵn sàng. Một chu kỳ nữa: module của cơ chế yếu
  nhất → bộ có giờ của nó → mô phỏng này lần nữa. Luật cách quãng
  48 giờ áp dụng.
- **< 70%**: chưa — và mô phỏng đã làm tròn phận sự. Bản đồ bẫy sẽ
  cho thấy một hoặc hai cơ chế thống trị các câu sai. Chạy lại toàn
  bộ bộ luyện của các module đó, rồi Đề #3 (module 23) làm đề tái
  nhập, SAU ĐÓ quay lại đây.

Không phán quyết nào là phán xét năng lực — nó là quyết định định
tuyến về bảy ngày tiếp theo. Bài cuối của khóa (dưới đây) giữ kế
hoạch sau đó.
"""

VI_L3 = r"""
**Sau thạc sĩ.** Bất kể phán quyết, tuần trước kỳ thi thật không
phải dành cho tài liệu mới:

1. **Một bộ hỗn hợp** (module 17) ở cường độ nửa — giữ phản xạ
   phân-loại-trước ấm mà không đuối sức.
2. **Nghi thức khoanh-toán-tử** trên bất kỳ bài ôn nào bạn làm lại —
   thói quen đọc-mệnh đề suy giảm nhanh nhất.
3. **Đọc lại module chiến lược** (module 20) tối trước ngày thi:
   các con số nhịp độ, luật không-chỗ-trống, quy trình mười phút
   cuối. Ngủ thắng mô phỏng thứ sáu, mọi lần.
4. **Ngày thi**: các thùng phân loại, các phần FRQ đã giữ, kiểm
   toán biên, không chỗ trống. Mọi thứ khác là nhiễu.

Bạn đến đây từ Foundations, qua Core, vào khóa này. Chuỗi được thiết
kế để kết thúc với bạn bước vào phòng thi đã từng thi nó — nhiều
lần, trong điều kiện tệ hơn điều kiện thật. Đó là toàn bộ mẹo: kỳ
thi bình yên vì bạn đã từng ở đây.
"""

BOILER_M = r"""public class Solution {
    public static void program() {
        // Print your answer: the option letter, then a one-sentence reason.
    }
}
"""

Q1_S = "What is printed?\n\n```java\nint[] a = {1, 2, 3, 4};\nint[] b = a;\nb[1] = 99;\na = new int[2];\nSystem.out.print(a[0] + \"/\" + b[1]);\n```"
Q1_O = ["A. `0/99`", "B. `1/99`", "C. `0/2`", "D. `1/2`"]
Q1_W = "A. b aliases a when b[1] = 99 runs; a then rebinds to a fresh int[2] whose first cell is 0. B misses the rebind; C misses the mutation; D misses both."
Q1_VS = "Chương trình in gì?\n\n```java\nint[] a = {1, 2, 3, 4};\nint[] b = a;\nb[1] = 99;\na = new int[2];\nSystem.out.print(a[0] + \"/\" + b[1]);\n```"
Q1_VO = ["A. `0/99`", "B. `1/99`", "C. `0/2`", "D. `1/2`"]
Q1_VW = "A. b là bí danh của a khi b[1] = 99 chạy; a rồi gán lại sang int[2] mới với ô đầu là 0. B bỏ qua phép gán lại; C bỏ qua phép biến đổi; D bỏ qua cả hai."

Q2_S = "What does `mystery(\"racecar\")` return?\n\n```java\npublic static boolean mystery(String s) {\n    return rev(s).equals(s);\n}\n\npublic static String rev(String s) {\n    if (s.length() <= 1) { return s; }\n    return rev(s.substring(1)) + s.charAt(0);\n}\n```"
Q2_O = ["A. true", "B. false", "C. the empty string", "D. StackOverflowError"]
Q2_W = "A. \"racecar\" reversed is \"racecar\" — the palindrome check returns true. B tests a non-palindrome instinct; C confuses the helper; D is impossible since progress shrinks."
Q2_VS = "`mystery(\"racecar\")` trả về gì?\n\n```java\npublic static boolean mystery(String s) {\n    return rev(s).equals(s);\n}\n\npublic static String rev(String s) {\n    if (s.length() <= 1) { return s; }\n    return rev(s.substring(1)) + s.charAt(0);\n}\n```"
Q2_VO = ["A. true", "B. false", "C. chuỗi rỗng", "D. StackOverflowError"]
Q2_VW = "A. \"racecar\" đảo ngược là \"racecar\" — phép kiểm palindrome trả true. B là phản xạ với chuỗi không-palindrome; C nhầm helper; D bất khả vì tiến trình thu nhỏ."

Q3_S = "What is printed?\n\n```java\nArrayList<Integer> list = new ArrayList<Integer>();\nlist.add(5); list.add(15); list.add(25);\nfor (int i = list.size() - 1; i >= 0; i--) {\n    if (list.get(i) > 10) { list.remove(i); }\n}\nSystem.out.print(list);\n```"
Q3_O = ["A. `[5]`", "B. `[5, 15]`", "C. `[]`", "D. ConcurrentModificationException"]
Q3_W = "A. Backward removal safely drops 25 then 15, leaving [5]. B forgets the removals; C removes everything; D only fires for for-each removal."
Q3_VS = "Chương trình in gì?\n\n```java\nArrayList<Integer> list = new ArrayList<Integer>();\nlist.add(5); list.add(15); list.add(25);\nfor (int i = list.size() - 1; i >= 0; i--) {\n    if (list.get(i) > 10) { list.remove(i); }\n}\nSystem.out.print(list);\n```"
Q3_VO = ["A. `[5]`", "B. `[5, 15]`", "C. `[]`", "D. ConcurrentModificationException"]
Q3_VW = "A. Xóa chiều ngược an toàn bỏ 25 rồi 15, còn [5]. B quên các phép xóa; C xóa tất cả; D chỉ nổ với for-each."

Q4_S = "What is printed?\n\n```java\npublic class Box {\n    private int v;\n    public Box(int v) { this.v = v; }\n    public void add(int n) { v += n; }\n    public String toString() { return \"\" + v; }\n}\n\nBox one = new Box(10);\nBox two = one;\ntwo.add(5);\none = new Box(1);\none.add(1);\nSystem.out.print(one + \"/\" + two);\n```"
Q4_O = ["A. `2/15`", "B. `15/2`", "C. `2/2`", "D. `15/15`"]
Q4_W = "A. two aliases one (both 15 after add); one rebinds to a new Box(1) then add(1) → 2. B swaps the references; C misses the alias mutation; D misses the rebind."
Q4_VS = "Chương trình in gì?\n\n```java\npublic class Box {\n    private int v;\n    public Box(int v) { this.v = v; }\n    public void add(int n) { v += n; }\n    public String toString() { return \"\" + v; }\n}\n\nBox one = new Box(10);\nBox two = one;\ntwo.add(5);\none = new Box(1);\none.add(1);\nSystem.out.print(one + \"/\" + two);\n```"
Q4_VO = ["A. `2/15`", "B. `15/2`", "C. `2/2`", "D. `15/15`"]
Q4_VW = "A. two là bí danh của one (cùng 15 sau add); one gán lại sang Box(1) mới rồi add(1) → 2. B đảo hai tham chiếu; C bỏ qua phép biến đổi bí danh; D bỏ qua phép gán lại."

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
        challenge(cid, "Master MCQ", prompt, BOILER_M, [(ans + " master", test, why[:380])], level="independent", difficulty="advanced"),
        vi_challenge("Câu thạc sĩ", vi_prompt, [(ans + " master", vi_why[:380])]),
    )

P1, V1 = mcq("apx-m24-q1", Q1_S, Q1_O, "A", Q1_W, Q1_VS, Q1_VO, Q1_VW)
P2, V2 = mcq("apx-m24-q2", Q2_S, Q2_O, "A", Q2_W, Q2_VS, Q2_VO, Q2_VW)
P3, V3 = mcq("apx-m24-q3", Q3_S, Q3_O, "A", Q3_W, Q3_VS, Q3_VO, Q3_VW)
P4, V4 = mcq("apx-m24-q4", Q4_S, Q4_O, "A", Q4_W, Q4_VS, Q4_VO, Q4_VW)

CP24 = challenge(
    "apx-cp-m24-frq",
    "Master FRQ: the clinic scheduler",
    "25-minute FRQ. Implement the `Clinic` class (four behaviors, "
    "no topic announced):\n\n"
    "- constructor takes the number of rooms\n"
    "- `arrive(String patient)` adds the patient to the waitlist "
    "unless already waiting (returns true on success, false on "
    "duplicate)\n- `room()` assigns the waitlisted patient at the "
    "FRONT to a free room if any exist (rooms are slots, like "
    "lockers; returns the 1-based room number or -1) — the patient "
    "leaves the waitlist\n- `waiting()` reports the waitlist size\n"
    "- `freeRooms()` reports unoccupied room count\n\nImplement the "
    "full class. Bank order: arrive, waiting/freeRooms, then room.",
    r"""public class Solution {
    public static class Clinic {
        public Clinic(int rooms) {
        }

        public boolean arrive(String patient) {
            return false;
        }

        public int room() {
            return -1;
        }

        public int waiting() {
            return 0;
        }

        public int freeRooms() {
            return 0;
        }
    }
}
""",
    [(
        "clinic frq",
        r"""
Solution.Clinic c = new Solution.Clinic(2);
CjTestBase.checkTrue(c.arrive("Ann"), "first arrival");
CjTestBase.checkTrue(!c.arrive("Ann"), "no duplicates");
CjTestBase.checkTrue(c.arrive("Bob"), "second arrival");
CjTestBase.checkEq(c.waiting(), 2, "two waiting");
CjTestBase.checkEq(c.room(), 1, "front patient takes room 1");
CjTestBase.checkEq(c.waiting(), 1, "Ann left the list");
CjTestBase.checkEq(c.freeRooms(), 1, "one room taken");
CjTestBase.checkEq(c.room(), 2, "Bob takes room 2");
CjTestBase.checkEq(c.room(), -1, "no rooms left");
""",
        "Fuses three banked patterns: the no-duplicate insert (studio), the locker allocation (lowest free room), and a front-queue removal.",
    )],
    level="mini-build",
    difficulty="advanced",
)

VI_CP24 = vi_challenge(
    "FRQ thạc sĩ: bộ lập lịch phòng khám",
    "FRQ 25 phút. Cài lớp `Clinic` (bốn hành vi, không công bố chủ "
    "đề):\n\n"
    "- constructor nhận số phòng\n"
    "- `arrive(String patient)` thêm bệnh nhân vào danh sách chờ trừ "
    "khi đang chờ rồi (trả true khi thành công, false khi trùng)\n"
    "- `room()` gán bệnh nhân ở ĐẦU danh sách chờ vào một phòng trống "
    "nếu có (phòng là các ô, như tủ đồ; trả số phòng đánh số từ 1 hoặc "
    "-1) — bệnh nhân rời danh sách chờ\n- `waiting()` báo kích thước "
    "danh sách chờ\n- `freeRooms()` báo số phòng trống\n\nCài lớp trọn "
    "vẹn. Thứ tự giữ: arrive, waiting/freeRooms, rồi room.",
    [("clinic frq", "Ghép ba mẫu đã giữ: chèn không-trùng (studio), cấp phát tủ đồ (phòng trống thấp nhất), và xóa-đầu-hàng-đợi.")],
)

write_practice(
    M, "apx-p24-master", "Master simulation: MCQ section",
    "Four unlabeled originals across aliasing, recursion, mutation, and dispatch-adjacent state; 20 minutes.",
    "Mô phỏng thạc sĩ: phần trắc nghiệm",
    "Bốn câu gốc không nhãn trên bí danh, đệ quy, biến đổi, và trạng thái; 20 phút.",
    after_lesson="apx-m24-protocol", minutes=25, difficulty="advanced",
    challenges=[P1, P2, P3, P4],
    vi_challenges={"apx-m24-q1": V1, "apx-m24-q2": V2, "apx-m24-q3": V3, "apx-m24-q4": V4},
    solutions=[
        ("apx-m24-q1", BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. mutation through alias, then local rebind.");'), BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. missed the rebind.");')),
        ("apx-m24-q2", BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. racecar reversed is racecar.");'), BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. assumed non-palindrome.");')),
        ("apx-m24-q3", BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. backward removal is safe: [5].");'), BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("C. removed everything, misread the guard.");')),
        ("apx-m24-q4", BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("A. alias mutated to 15; rebind gave 2.");'), BOILER_M.replace("// Print your answer: the option letter, then a one-sentence reason.", 'System.out.println("B. swapped the output order.");')),
    ],
)

write_checkpoint(
    M, "apx-cp-m24", "Checkpoint: the master FRQ",
    "The gate: four behaviors fused from three banked patterns, 25 minutes.",
    30,
    r"""
The clinic is the parking garage (locker allocation), the studio
(no-duplicate insert), and a front-of-line removal — three
mechanisms you have built separately in modules 8, 14, and 23.
Recognize the parts, bank them in order, wire the room() flow
last: it reads the waitlist AND the rooms.
""",
    "Điểm kiểm tra: FRQ thạc sĩ",
    "Cánh cổng: bốn hành vi ghép từ ba mẫu đã giữ, 25 phút.",
    r"""
Phòng khám là bãi đỗ xe (cấp phát tủ), studio (chèn không-trùng), và
một phép xóa-đầu-hàng — ba cơ chế bạn đã dựng riêng trong module 8,
14, và 23. Nhận diện các phần, giữ chúng theo thứ tự, đấu nối luồng
room() cuối cùng: nó đọc cả danh sách chờ VÀ các phòng.
""",
    CP24,
    VI_CP24,
    solution=r"""public class Solution {
    public static class Clinic {
        private int rooms;
        private java.util.ArrayList<String> waitlist = new java.util.ArrayList<String>();
        private int occupied = 0;

        public Clinic(int rooms) {
            this.rooms = rooms;
        }

        public boolean arrive(String patient) {
            if (waitlist.contains(patient)) {
                return false;
            }
            waitlist.add(patient);
            return true;
        }

        public int room() {
            if (occupied >= rooms || waitlist.size() == 0) {
                return -1;
            }
            waitlist.remove(0);
            occupied++;
            return occupied;
        }

        public int waiting() {
            return waitlist.size();
        }

        public int freeRooms() {
            return rooms - occupied;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Clinic {
        private int rooms;
        private java.util.ArrayList<String> waitlist = new java.util.ArrayList<String>();
        private int occupied = 0;

        public Clinic(int rooms) {
            this.rooms = rooms;
        }

        public boolean arrive(String patient) {
            // BUG: no duplicate guard — the waitlist inflates
            waitlist.add(patient);
            return true;
        }

        public int room() {
            if (occupied >= rooms || waitlist.size() == 0) {
                return -1;
            }
            waitlist.remove(0);
            occupied++;
            return occupied;
        }

        public int waiting() {
            return waitlist.size();
        }

        public int freeRooms() {
            return rooms - occupied;
        }
    }
}
""",
)

print("M24 done")
