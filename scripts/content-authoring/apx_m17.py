#!/usr/bin/env python3
"""AP CSA Advanced M17 — Mixed AP sets (unlabeled diversity, verified)."""
from apx import *

M = "apx-mixed"

write_module(
    M,
    "Mixed AP Sets",
    "Unlabeled sets blending MCQ, tracing, debugging, and coding — the topic is never announced. Difficulty E4–E5.",
    "Bộ đề hỗn hợp",
    "Bộ đề không nhãn trộn trắc nghiệm, truy vết, gỡ lỗi, và lập trình — chủ đề không bao giờ được công bố. Độ khó E4–E5.",
    lessons=["apx-m17-blend", "apx-m17-shift", "apx-m17-review", "apx-cp-m17"],
    practices=["apx-p17-mixed"],
)

L1 = r"""
A real exam section never tells you which unit a question came
from. The **skill of not knowing** is trainable: each mixed set
below switches mechanism every challenge — a tracing question, then
a spec implementation, then a bug hunt — with no headers. Your
preparation ritual per question:

1. **Classify in five seconds**: is this predict-output, write-code,
   or fix-code? The response mode is the first decision, and
   misclassifying wastes minutes.
2. **Name the mechanism**: one mental sentence — "adjacent scan,"
   "state machine," "removal discipline." If you cannot name it,
   the classification IS the exercise: slow down and inventory the
   nouns and verbs.
3. **Answer in the mode required**: MCQs here still demand the
   letter plus reasoning; coding items still demand passing tests.

The sets deliberately interleave difficulty — a speed-trap MCQ
sits between two heavy implementations — because that is the
exam's rhythm too.
"""

L2 = r"""
**The interleave principle.** Random-looking order is actually the
most efficient review schedule: switching mechanisms forces
retrieval practice (you must recall which pattern applies instead
of riding momentum from the last item). Research on learning calls
this interleaving; the exam calls it Tuesday.

Practical interleave habits:

- After every switch, re-read the response format. Answering an
  MCQ with an implementation (or vice versa) is a zero.
- Keep a mistake tally across the set by MECHANISM, not topic:
  "two removal-discipline errors" tells you what to drill;
  "two ArrayList errors" doesn't.
- Treat every challenge as graded by its own rubric: MCQ = letter
  + explanation; trace = exact output; implementation = all tests.

The checkpoint is the set's final: five mechanisms, no labels, no
mercy — but every one is a pattern you have already banked.
"""

L3 = r"""
**Cross-module review loop.** Mixed sets expose which modules
actually transferred. After finishing a set, sort your misses by
the module that taught the mechanism, and re-run that module's
practice set within 48 hours — the same two-sided rule applies to
your own learning: a miss you cannot reproduce is a miss you have
not fixed.

The long game for the next modules: full simulations (modules
21–24) are just mixed sets with a clock and a score. Every mixed
challenge you complete *now* with the classify-first ritual is a
rep that pays out during the simulations. Track two numbers per
set: accuracy and median time per item. Accuracy below 70% means
drill the mechanism; time above target means drill the
recognition.
"""

VI_L1 = r"""
Một phần đề thật không bao giờ cho biết câu hỏi đến từ unit nào.
**Kỹ năng không-biết** luyện được: mỗi bộ hỗn hợp dưới đây đổi cơ
chế sau mỗi bài — một câu truy vết, rồi một bài cài đặc tả, rồi một
cuộc săn lỗi — không có tiêu đề. Nghi thức chuẩn bị cho mỗi câu:

1. **Phân loại trong năm giây**: đây là dự-đoán-kết-quả, viết-mã,
   hay sửa-mã? Chế độ phản hồi là quyết định đầu tiên, và phân loại
   sai làm lãng phí vài phút.
2. **Gọi tên cơ chế**: một câu trong đầu — "quét liền kề," "máy
   trạng thái," "kỷ luật xóa." Nếu không gọi được tên, việc phân
   loại CHÍNH LÀ bài tập: chậm lại và kiểm kê các danh từ và động từ.
3. **Trả lời đúng chế độ yêu cầu**: trắc nghiệm ở đây vẫn đòi chữ
   cái cộng lý do; bài lập trình vẫn đợi qua các test.

Các bộ đề cố tình xen kẽ độ khó — một câu trắc nghiệm bẫy-tốc-độ
nằm giữa hai bài cài nặng — vì đó cũng là nhịp điệu của đề thi.
"""

VI_L2 = r"""
**Nguyên tắc xen kẽ.** Thứ tự trông-ngẫu-nhiên thực ra là lịch ôn
tập hiệu quả nhất: đổi cơ chế ép luyện-truy-hồi (bạn phải nhớ mẫu
nào áp dụng thay vì trôi theo đà từ câu trước). Nghiên cứu học tập
gọi đây là interleaving; đề thi gọi nó là ngày thi thứ ba.

Thói quen xen kẽ thực dụng:

- Sau mỗi lần đổi, đọc lại định dạng phản hồi. Trả lời trắc nghiệm
  bằng một bản cài đặt (hoặc ngược lại) là số điểm không.
- Giữ bảng đếm lỗi xuyên suốt bộ đề theo CƠ CHẾ, không phải chủ đề:
  "hai lỗi kỷ-luật-xóa" cho bạn biết cần luyện gì; "hai lỗi ArrayList"
  thì không.
- Coi mỗi bài như được chấm theo bảng điểm riêng: trắc nghiệm = chữ
  cái + giải thích; truy vết = kết quả chính xác; cài đặt = qua hết
  test.

Bài kiểm tra là bài cuối của bộ: năm cơ chế, không nhãn, không thương
xót — nhưng mỗi cái là một mẫu bạn đã giữ rồi.
"""

VI_L3 = r"""
**Vòng ôn liên module.** Bộ hỗn hợp phơi bày module nào thực sự
chuyển giao được. Sau khi xong một bộ, xếp các câu sai của bạn theo
module đã dạy cơ chế đó, và chạy lại bộ luyện của module đó trong 48
giờ — cùng luật hai-phía áp dụng cho việc học của bạn: một câu sai
mà bạn không tái hiện được là một câu sai chưa được sửa.

Ván dài cho các module kế tiếp: các mô phỏng trọn vẹn (module
21–24) chỉ là bộ hỗn hợp với đồng hồ và điểm số. Mỗi bài hỗn hợp bạn
hoàn thành *bây giờ* với nghi thức phân-loại-trước là một lần reps
trả lãi trong lúc mô phỏng. Theo dõi hai con số mỗi bộ: độ chính xác
và thời gian trung vị mỗi câu. Độ chính xác dưới 70% nghĩa là luyện
cơ chế; thời gian trên mục tiêu nghĩa là luyện nhận dạng.
"""

BOILER_TRACE = r"""public class Solution {
    public static String result() {
        return ""; // replace: the exact output asked for
    }
}
"""

BOILER_CODE = r"""public class Solution {
    public static int process(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_FIX = r"""public class Solution {
    // SPEC: count elements strictly greater than the first element
    public static int countAboveFirst(int[] arr) {
        int count = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > arr[0]) {
                count--;
            }
        }
        return count;
    }
}
"""

P_T1 = challenge(
    "apx-m17-t1",
    "Mixed 1: predict the output",
    "No topic given. Predict and return the exact output:\n\n```java\n"
    "int[] a = {3, 8, 2};\nint x = 0;\nfor (int v : a) {\n"
    "    if (v > 4) { x += v; }\n}\nx *= 2;\nSystem.out.print(x);\n```",
    BOILER_TRACE,
    [(
        "predicted output",
        r"""
CjTestBase.checkEq(Solution.result(), "16", "8 * 2");
""",
        "Only 8 exceeds 4; accumulator 8, doubled to 16.",
    )],
    level="independent",
    difficulty="advanced",
)

P_C1 = challenge(
    "apx-m17-c1",
    "Mixed 2: implement from spec",
    "No topic given. A 'plateau' is a run of two or more equal "
    "adjacent values. Count the plateaus in the array (a run of 4 "
    "equal values counts as ONE plateau; separate runs count "
    "separately). Implement `process(int[] arr)` (0 when no plateau "
    "exists).\n\nExample: `{1,1,2,2,2,3}` → `2`; `{1,2,3}` → `0`.",
    BOILER_CODE,
    [(
        "plateau count",
        r"""
CjTestBase.checkEq(Solution.process(new int[]{1, 1, 2, 2, 2, 3}), 2, "two runs");
CjTestBase.checkEq(Solution.process(new int[]{1, 2, 3}), 0, "no plateau");
CjTestBase.checkEq(Solution.process(new int[]{5, 5, 5, 5}), 1, "one long run");
CjTestBase.checkEq(Solution.process(new int[]{}), 0, "empty");
""",
        "Count run STARTS: arr[i] == arr[i-1] && (i == 1 || arr[i-1] != arr[i-2]).",
    )],
    level="combination",
    difficulty="advanced",
)

P_F1 = challenge(
    "apx-m17-f1",
    "Mixed 3: fix the bug",
    "No topic given. The method should count elements **strictly "
    "greater than the first element**. It fails. Fix it in place.",
    BOILER_FIX,
    [(
        "fixed counter",
        r"""
CjTestBase.checkEq(Solution.countAboveFirst(new int[]{5, 9, 2, 7}), 2, "9 and 7");
CjTestBase.checkEq(Solution.countAboveFirst(new int[]{5}), 0, "no others");
CjTestBase.checkEq(Solution.countAboveFirst(new int[]{}), 0, "empty");
""",
        "The accumulator decrements — invert to count++.",
    )],
    level="debugging",
    difficulty="advanced",
)

P_T2 = challenge(
    "apx-m17-t2",
    "Mixed 4: predict the state",
    "No topic given. Predict and return the exact printed text:\n\n"
    "```java\nStringBuilder b = new StringBuilder(\"ab\");\n"
    "StringBuilder c = b;\nc.append(\"cd\");\nb = new StringBuilder(\"z\");\n"
    "System.out.print(b + \"/\" + c);\n```",
    BOILER_TRACE,
    [(
        "predicted state",
        r"""
CjTestBase.checkEq(Solution.result(), "z/abcd", "alias mutated, rebind local");
""",
        "c aliases b when append happens; then b rebinds to \"z\" while c keeps \"abcd\".",
    )],
    level="combination",
    difficulty="advanced",
)

CP17 = challenge(
    "apx-cp-m17-sweep",
    "Checkpoint: the unlabeled final",
    "No topic, no hints. A 'signal' array is one where every element "
    "from index 1 on is **strictly greater** than the previous "
    "element. Return the length of the longest contiguous signal "
    "segment; an empty array returns 0, a single element counts as "
    "a segment of 1.\n\nImplement `process(int[] arr)`.\n\nExample: "
    "`{5, 9, 2, 4, 6, 1}` → `3` (2,4,6).",
    BOILER_CODE,
    [(
        "longest rising segment",
        r"""
CjTestBase.checkEq(Solution.process(new int[]{5, 9, 2, 4, 6, 1}), 3, "2,4,6");
CjTestBase.checkEq(Solution.process(new int[]{}), 0, "empty");
CjTestBase.checkEq(Solution.process(new int[]{7}), 1, "single");
CjTestBase.checkEq(Solution.process(new int[]{9, 1, 5}), 2, "1,5");
""",
        "Run counter resets when arr[i] <= arr[i-1]; track the max including the length-1 base.",
    )],
    level="real-world",
    difficulty="advanced",
)

VI_CP17 = vi_challenge(
    "Điểm kiểm tra: bài cuối không nhãn",
    "Không chủ đề, không gợi ý. Mảng 'tín hiệu' là mảng mà mọi phần tử "
    "từ chỉ số 1 trở đi **lớn hơn hoàn toàn** phần tử trước nó. Trả về "
    "độ dài đoạn tín hiệu liên tiếp dài nhất; mảng rỗng trả 0, một "
    "phần tử tính là đoạn độ dài 1.\n\nCài đặt `process(int[] arr)`.\n\n"
    "Ví dụ: `{5, 9, 2, 4, 6, 1}` → `3` (2,4,6).",
    [("longest rising segment", "Bộ đếm run reset khi arr[i] <= arr[i-1]; ghi nhận max kể cả cơ sở độ dài 1.")],
)

write_practice(
    M, "apx-p17-mixed", "Mixed set: no labels",
    "Four unlabeled challenges across four mechanisms, then the final sweep.",
    "Bộ hỗn hợp: không nhãn",
    "Bốn bài không nhãn trên bốn cơ chế, rồi lượt quét cuối.",
    after_lesson="apx-m17-review", minutes=55, difficulty="advanced",
    challenges=[P_T1, P_F1, P_C1, P_T2],
    vi_challenges={
        "apx-m17-t1": vi_challenge(
            "Hỗn hợp 1: dự đoán kết quả",
            "Không có chủ đề. Dự đoán và trả về kết quả chính xác:\n\n```java\n"
            "int[] a = {3, 8, 2};\nint x = 0;\nfor (int v : a) {\n"
            "    if (v > 4) { x += v; }\n}\nx *= 2;\nSystem.out.print(x);\n```",
            [("predicted output", "Chỉ 8 vượt 4; bộ tích lũy 8, nhân đôi thành 16.")],
        ),
        "apx-m17-f1": vi_challenge(
            "Hỗn hợp 3: sửa lỗi",
            "Không có chủ đề. Phương thức nên đếm các phần tử **nghiêm ngặt "
            "lớn hơn phần tử đầu tiên**. Nó chạy sai. Sửa tại chỗ.",
            [("fixed counter", "Bộ tích lũy đang trừ — đảo lại thành count++.")],
        ),
        "apx-m17-c1": vi_challenge(
            "Hỗn hợp 2: cài theo đặc tả",
            "Không có chủ đề. Một 'cao nguyên' là run gồm hai hoặc nhiều giá "
            "trị liền kề bằng nhau. Đếm số cao nguyên trong mảng (run gồm 4 "
            "giá trị bằng nhau tính là MỘT cao nguyên; các run riêng đếm "
            "riêng). Cài đặt `process(int[] arr)` (0 khi không có cao "
            "nguyên).\n\nVí dụ: `{1,1,2,2,2,3}` → `2`; `{1,2,3}` → `0`.",
            [("plateau count", "Đếm điểm BẮT ĐẦU run: arr[i] == arr[i-1] && (i == 1 || arr[i-1] != arr[i-2]).")],
        ),
        "apx-m17-t2": vi_challenge(
            "Hỗn hợp 4: dự đoán trạng thái",
            "Không có chủ đề. Dự đoán và trả về văn bản được in chính xác:\n\n"
            "```java\nStringBuilder b = new StringBuilder(\"ab\");\n"
            "StringBuilder c = b;\nc.append(\"cd\");\nb = new StringBuilder(\"z\");\n"
            "System.out.print(b + \"/\" + c);\n```",
            [("predicted state", "c là bí danh của b khi append xảy ra; rồi b gán lại \"z\" trong khi c giữ \"abcd\".")],
        ),
    },
    solutions=[
        ("apx-m17-t1", r"""public class Solution {
    public static String result() {
        return "16";
    }
}
""", r"""public class Solution {
    // BUG: forgot the doubling
    public static String result() {
        return "8";
    }
}
"""),
        ("apx-m17-f1", r"""public class Solution {
    public static int countAboveFirst(int[] arr) {
        int count = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > arr[0]) {
                count++;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // still broken: decrements
    public static int countAboveFirst(int[] arr) {
        int count = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > arr[0]) {
                count--;
            }
        }
        return count;
    }
}
"""),
        ("apx-m17-c1", r"""public class Solution {
    public static int process(int[] arr) {
        int count = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] == arr[i - 1] && (i == 1 || arr[i - 1] != arr[i - 2])) {
                count++;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: counts every run ELEMENT, not every run start
    public static int process(int[] arr) {
        int count = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] == arr[i - 1]) {
                count++;
            }
        }
        return count;
    }
}
"""),
        ("apx-m17-t2", r"""public class Solution {
    public static String result() {
        return "z/abcd";
    }
}
""", r"""public class Solution {
    // BUG: believed the rebind propagated to c
    public static String result() {
        return "z/z";
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m17", "Checkpoint: unlabeled final",
    "One synthesis problem in exam silence: classify, name, implement.",
    25,
    r"""
The rising-segment scan is a run-counter problem wearing a
signal-processing costume. By now the classification should be
instant: run counter, reset condition, max tracker. That
instantaneity is what the simulations will test.
""",
    "Điểm kiểm tra: bài cuối không nhãn",
    "Một bài tổng hợp trong im lặng phòng thi: phân loại, gọi tên, cài đặt.",
    r"""
Quét đoạn-tăng là bài bộ-đếm-run đội lốt xử-lý-tín-hiệu. Đến lúc này
việc phân loại phải là tức thì: bộ đếm run, điều kiện reset, bộ ghi
max. Sự tức thì đó chính là thứ các mô phỏng sẽ kiểm tra.
""",
    CP17,
    VI_CP17,
    solution=r"""public class Solution {
    public static int process(int[] arr) {
        if (arr.length == 0) {
            return 0;
        }
        int best = 1;
        int cur = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > arr[i - 1]) {
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
""",
    wrong=r"""public class Solution {
    // BUG: counts every step instead of the segment length
    public static int process(int[] arr) {
        int best = 0;
        int cur = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > arr[i - 1]) {
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
""",
)

print("M17 done")
