#!/usr/bin/env python3
"""AP CSA Advanced M4 — MCQ speed training (fast verified drills + timed practice)."""
from apx import *

M = "apx-speed"

write_module(
    M,
    "MCQ Speed Training",
    "Timed drills: fast tracing, elimination, pattern recognition, and skip-and-return discipline. Correctness first, speed second. Difficulty E2–E3.",
    "Luyện tốc độ trắc nghiệm",
    "Bài tập có giờ: truy vết nhanh, loại trừ, nhận dạng mẫu, và kỷ luật bỏ-qua-quay-lại. Đúng trước, nhanh sau. Độ khó E2–E3.",
    lessons=["apx-m4-tempo", "apx-m4-elimination", "apx-m4-patterns", "apx-cp-m4"],
    practices=["apx-p4-speed"],
)

L1 = r"""
The exam gives you **90 seconds per MCQ**. That budget changes
*behavior*, not standards: the answer is the same answer, you just get
there differently.

**The tempo rules:**

1. First pass: answer everything you can see in under 60 seconds.
   Mark the rest, move on. A marked question costs nothing; a stalled
   one costs two others.
2. Second pass: return to marks with remaining time. Eliminate two
   options, then commit.
3. Never let one trace exceed 3 minutes — that is a fourth of an FRQ
   spent on a single point.

**Fast-tracing shortcuts** that stay rigorous:

- After 2 iterations of a loop, ask what the k-th iteration does. Most
  exam loops are *boring* — constant work per pass.
- For sum/count loops, derive the closed form instead of simulating
  (arithmetic series, count of iterations = (last - first)/step + 1).
- For object questions, draw boxes once; do not re-derive aliasing
  from memory mid-question.
"""

L2 = r"""
**Elimination is arithmetic on your uncertainty.** Kill options in
this order:

1. **Type-impossible**: an `int` method returning a `String`; an
   option with a value the return type cannot hold (e.g. 3.5 for int).
2. **Bounds-impossible**: a value outside the achievable range (a
   sum of positives reported as negative; an index ≥ length).
3. **Trace-impossible**: run two iterations of the loop mentally —
   any option that disagrees with iteration 2 is dead regardless of
   the rest.

After elimination, if two options survive, ask *what code would have
to say* for each to be true. Usually one requires the loop to do
something the visible code does not (`<=` instead of `<`, remove
instead of skip). Pick the survivor that requires no invisible code.

**Careless-mistake insurance:** on questions with a "boundary" feel
(empty, single element, last index), check your answer *against that
boundary* before committing. Most lost points are not hard reasoning;
they are `<` answers on `<=` questions.
"""

L3 = r"""
**Pattern recognition beats re-derivation.** These five patterns cover
most of the exam's MCQs; when you see the shape, you already know the
answer's *structure*:

- **Accumulator**: `sum += ...` in a loop with a guard. Answer is the
  guard applied to every element. Trap options: guard applied once,
  guard inverted.
- **Search-and-flag**: found a match, set a boolean, break. Trap:
  options where the flag is overwritten by a later mismatch.
- **Remove-scan**: removal inside a forward loop. Trap: options
  assuming no shift. The survivor list is never what a no-shift
  reading predicts.
- **Two-ledger**: static + instance fields both changing. Trap:
  options that read the wrong ledger.
- **Cast-then-compute vs compute-then-cast**: integer division
  before widening. Trap: the "nice" decimal answer.

A timed set is *training*, not a ranking. Its job is to make these
recognitions automatic under time pressure.
"""

VI_L1 = r"""
Đề thi cho bạn **90 giây mỗi câu trắc nghiệm**. Ngân sách đó thay đổi
*hành vi*, không phải tiêu chuẩn: đáp án vẫn là đáp án đó, chỉ là bạn
đến đó theo cách khác.

**Luật nhịp độ:**

1. Lượt một: trả lời mọi câu nhìn ra được trong dưới 60 giây. Đánh
   dấu phần còn lại, đi tiếp. Một câu bị đánh dấu không tốn gì; một
   câu bị kẹt tốn hai câu khác.
2. Lượt hai: quay lại các dấu với thời gian còn lại. Loại hai phương
   án, rồi quyết định.
3. Không bao giờ để một lần truy vết vượt 3 phút — đó là một phần tư
   một câu FRQ tiêu cho một điểm.

**Mẹo truy vết nhanh** vẫn giữ chặt độ chính xác:

- Sau 2 vòng lặp, hỏi vòng thứ k làm gì. Đa số vòng lặp đề thi rất
  *nhàm chán* — chi phí đều mỗi lượt.
- Với vòng lặp cộng/đếm, rút công thức đóng thay vì mô phỏng (cấp số
  cộng, số vòng = (cuối - đầu)/bước + 1).
- Với câu về đối tượng, vẽ hộp một lần; không suy luận lại bí danh từ
  trí nhớ giữa câu.
"""

VI_L2 = r"""
**Loại trừ là phép tính trên sự không chắc chắn của bạn.** Loại phương
án theo thứ tự:

1. **Bất khả về kiểu**: phương thức `int` trả `String`; một phương án
   chứa giá trị kiểu trả về không thể giữ (ví dụ 3.5 cho int).
2. **Bất khả về biên**: giá trị ngoài khoảng có thể đạt được (tổng các
   số dương bị báo là số âm; chỉ số ≥ độ dài).
3. **Bất khả về truy vết**: chạy hai vòng lặp trong đầu — phương án nào
   mâu thuẫn với vòng thứ hai là chết bất chấp phần còn lại.

Sau khi loại, nếu hai phương án còn sống, hỏi *mã phải nói gì* để mỗi
cái đúng. Thường một cái đòi hỏi vòng lặp làm điều mã nhìn thấy không
làm (`<=` thay vì `<`, xóa thay vì bỏ qua). Chọn phương án sống sót
không cần mã vô hình.

**Bảo hiểm lỗi bất cẩn:** với câu có "vị trí biên" (rỗng, một phần tử,
chỉ số cuối), kiểm tra đáp án *đối chiếu biên đó* trước khi chốt. Đa số
điểm mất không phải do suy luận khó; mà là đáp án `<` cho câu `<=`.
"""

VI_L3 = r"""
**Nhận dạng mẫu thắng việc suy luận lại.** Năm mẫu này phủ phần lớn
trắc nghiệm đề thi; nhìn thấy hình dạng là biết *cấu trúc* đáp án:

- **Bộ tích lũy**: `sum += ...` trong vòng lặp có điều kiện chặn. Đáp
  án là điều kiện chặn áp cho mọi phần tử. Phương án bẫy: chặn áp một
  lần, hoặc đảo điều kiện.
- **Tìm-và-cắm cờ**: gặp khớp, đặt boolean, break. Bẫy: các phương án
  mà cờ bị ghi đè bởi lần lệch sau.
- **Quét-xóa**: xóa bên trong vòng lặp đi tới. Bẫy: các phương án giả
  định không có dịch chuyển. Danh sách sót lại không bao giờ như cách
  đọc "không dịch".
- **Hai sổ cái**: trường static và instance cùng thay đổi. Bẫy: các
  phương án đọc nhầm sổ.
- **Ép-rồi-tính so với tính-rồi-ép**: chia số nguyên trước khi nâng
  kiểu. Bẫy: đáp án "đẹp" dạng thập phân.

Bộ đề có giờ là *luyện tập*, không phải xếp hạng. Nhiệm vụ của nó là
làm các phép nhận dạng này trở nên tự động dưới áp lực thời gian.
"""

BOILER_SPEED = r"""public class Solution {
    public static String answer(String letterAndReason) {
        // Speed drill: replace with a single println of your answer —
        // the option letter and a ONE-sentence reason. Time yourself!
        System.out.println(letterAndReason);
        return letterAndReason;
    }
}
"""

def speed(cid, title, stem, opts, ans, why, vi_title, vi_stem, vi_opts, vi_why, level="guided", diff="intermediate"):
    prompt = (
        "SPEED DRILL — target under 90 seconds.\n\n" + stem + "\n\n" + "\n".join(opts) +
        "\n\nCall `answer(...)` exactly once with your option letter and a one-sentence reason."
    )
    vi_prompt = (
        "BÀI TẬP TỐC ĐỘ — mục tiêu dưới 90 giây.\n\n" + vi_stem + "\n\n" + "\n".join(vi_opts) +
        "\n\nGọi `answer(...)` đúng một lần với chữ cái phương án và một câu lý do."
    )
    test = (
        'String out = CjTestBase.capture(() -> Solution.answer("' + ans + '. check"));\n'
        'CjTestBase.checkTrue(out.startsWith("' + ans + '"), "answer must start with the correct option letter");'
    )
    vi_test = (ans + " " + why.split(".")[0], "Đáp án phải bắt đầu bằng đúng chữ cái phương án.")
    return (
        challenge(cid, title, prompt, BOILER_SPEED, [(ans + " speed", test, why[:380])], level=level, difficulty=diff),
        vi_challenge(vi_title, vi_prompt, [vi_test]),
    )

S1, VS1 = speed(
    "apx-m4-s-increment", "Speed: two increments, one expression",
    "What is the value of `y`?\n\n```java\nint x = 5;\nint y = x++ + ++x;\n```",
    ["A. 10", "B. 11", "C. 12", "D. 13"],
    "C",
    "C. x++ yields 5 then x becomes 6; ++x makes 7 and yields 7; 5 + 7 = 12. B forgets one increment; D applies both increments before reading.",
    "Tốc độ: hai phép tăng, một biểu thức",
    "Giá trị của `y` là bao nhiêu?\n\n```java\nint x = 5;\nint y = x++ + ++x;\n```",
    ["A. 10", "B. 11", "C. 12", "D. 13"],
    "C. x++ trả 5 rồi x thành 6; ++x làm thành 7 và trả 7; 5 + 7 = 12. B quên một phép tăng; D áp cả hai phép tăng trước khi đọc.",
)
S2, VS2 = speed(
    "apx-m4-s-concat", "Speed: mixed + evaluation order",
    "What is printed?\n\n```java\nSystem.out.println(1 + 2 + \"3\" + 4 + 5);\n```",
    ["A. `12345`", "B. `3345`", "C. `15`", "D. `339`"],
    "B",
    "B. Left-to-right: 1+2 is int 3, then 3+\"3\" is \"33\", then string-append 4 and 5 → 3345. A ignores the int start; C evaluates everything numerically; D adds the tail numerically.",
    "Tốc độ: thứ tự đánh giá của + trộn kiểu",
    "Chương trình in gì?\n\n```java\nSystem.out.println(1 + 2 + \"3\" + 4 + 5);\n```",
    ["A. `12345`", "B. `3345`", "C. `15`", "D. `339`"],
    "B. Trái sang phải: 1+2 là int 3, rồi 3+\"3\" là \"33\", rồi nối chuỗi 4 và 5 → 3345. A bỏ qua khởi đầu int; C tính tất cả bằng số; D cộng phần đuôi bằng số.",
)
S3, VS3 = speed(
    "apx-m4-s-compound", "Speed: compound assignment chain",
    "What is the final value of `r`?\n\n```java\nint r = 9;\nr %= 4;\nr *= 3;\n```",
    ["A. 1", "B. 3", "C. 9", "D. 27"],
    "B",
    "B. 9 % 4 = 1, then 1 * 3 = 3. A stops after the modulus; D multiplies before taking the modulus.",
    "Tốc độ: chuỗi gán kép",
    "Giá trị cuối của `r` là bao nhiêu?\n\n```java\nint r = 9;\nr %= 4;\nr *= 3;\n```",
    ["A. 1", "B. 3", "C. 9", "D. 27"],
    "B. 9 % 4 = 1, rồi 1 * 3 = 3. A dừng sau phép chia dư; D nhân trước khi lấy dư.",
)
S4, VS4 = speed(
    "apx-m4-s-arraydefault", "Speed: default values",
    "What is printed?\n\n```java\nint[] a = new int[3];\na[1]++;\nSystem.out.println(a[0] + a[1] + a[2]);\n```",
    ["A. 0", "B. 1", "C. 2", "D. ArrayIndexOutOfBoundsException"],
    "B",
    "B. int arrays start at 0; a[1]++ makes exactly one cell 1; the sum is 1. A forgets the increment; D invents an out-of-bounds that never happens.",
    "Tốc độ: giá trị mặc định",
    "Chương trình in gì?\n\n```java\nint[] a = new int[3];\na[1]++;\nSystem.out.println(a[0] + a[1] + a[2]);\n```",
    ["A. 0", "B. 1", "C. 2", "D. ArrayIndexOutOfBoundsException"],
    "B. Mảng int bắt đầu toàn 0; a[1]++ làm đúng một ô thành 1; tổng là 1. A quên phép tăng; D bịa ra vượt biên không xảy ra.",
)
S5, VS5 = speed(
    "apx-m4-s-immut", "Speed: ignored return value",
    "What is printed?\n\n```java\nString s = \"exam\";\ns.toUpperCase();\nSystem.out.println(s);\n```",
    ["A. `EXAM`", "B. `exam`", "C. `Exam`", "D. compile error"],
    "B",
    "B. Strings are immutable; toUpperCase RETURNS a new string, and ignoring the return changes nothing. A assigns the result implicitly in the reader's head — the classic trap.",
    "Tốc độ: giá trị trả về bị bỏ qua",
    "Chương trình in gì?\n\n```java\nString s = \"exam\";\ns.toUpperCase();\nSystem.out.println(s);\n```",
    ["A. `EXAM`", "B. `exam`", "C. `Exam`", "D. lỗi biên dịch"],
    "B. Chuỗi bất biến; toUpperCase TRẢ VỀ chuỗi mới, và việc bỏ qua giá trị trả về không đổi gì. A gán kết quả ngầm trong đầu người đọc — bẫy kinh điển.",
)
S6, VS6 = speed(
    "apx-m4-s-steprange", "Speed: loop step count",
    "How many times does the body run?\n\n```java\nfor (int i = 0; i < 5; i += 2) { /* body */ }\n```",
    ["A. 2", "B. 2.5", "C. 3", "D. 5"],
    "C",
    "C. i takes 0, 2, 4 — three iterations ((4-0)/2 + 1). B is not an integer; A miscounts the off-by-one; D ignores the step.",
    "Tốc độ: số bước của vòng lặp",
    "Thân vòng lặp chạy bao nhiêu lần?\n\n```java\nfor (int i = 0; i < 5; i += 2) { /* thân */ }\n```",
    ["A. 2", "B. 2.5", "C. 3", "D. 5"],
    "C. i nhận 0, 2, 4 — ba vòng ((4-0)/2 + 1). B không phải số nguyên; A đếm lệch; D bỏ qua bước nhảy.",
)

CP4 = challenge(
    "apx-cp-m4-continue",
    "Checkpoint: skip-and-continue trace",
    "Trace quickly but carefully:\n\n```java\nint total = 0;\nfor (int i = 1; i <= 6; i++) {\n    if (i % 2 == 0) { continue; }\n    total += i;\n}\nSystem.out.print(total);\n```\n\nReturn the printed number.",
    r"""public class Solution {
    public static int result() {
        return 0; // replace: the printed total
    }
}
""",
    [(
        "printed total",
        r"""
CjTestBase.checkEq(Solution.result(), 9, "1+3+5, evens skipped");
""",
        "continue skips the even i values: 1, 3, 5 sum to 9.",
    )],
    level="independent",
    difficulty="advanced",
)

VI_CP4 = vi_challenge(
    "Điểm kiểm tra: truy vết với continue",
    "Truy vết nhanh nhưng cẩn thận:\n\n```java\nint total = 0;\nfor (int i = 1; i <= 6; i++) {\n    if (i % 2 == 0) { continue; }\n    total += i;\n}\nSystem.out.print(total);\n```\n\nTrả về số được in.",
    [("printed total", "continue bỏ qua các i chẵn: 1, 3, 5 cộng lại 9.")],
)

write_practice(
    M, "apx-p4-speed", "Speed set: 90-second drills",
    "Six fast MCQ drills plus a careful checkpoint trace. Correctness first.",
    "Bộ tốc độ: bài tập 90 giây",
    "Sáu bài trắc nghiệm nhanh cộng một truy vết kiểm tra cẩn thận. Đúng trước, nhanh sau.",
    after_lesson="apx-m4-patterns", minutes=30, difficulty="intermediate",
    challenges=[S1, S2, S3, S4, S5, S6],
    vi_challenges={"apx-m4-s-increment": VS1, "apx-m4-s-concat": VS2, "apx-m4-s-compound": VS3, "apx-m4-s-arraydefault": VS4, "apx-m4-s-immut": VS5, "apx-m4-s-steprange": VS6},
    solutions=[
        ("apx-m4-s-increment", BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("C. x++ gives 5 then x is 6; ++x makes 7; 5+7=12.");'), BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("B. forgot one increment.");')),
        ("apx-m4-s-concat", BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("B. left-to-right: 3, then string appends: 3345.");'), BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("A. treated everything as text from the start.");')),
        ("apx-m4-s-compound", BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("B. 9%4=1 then *3=3.");'), BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("D. multiplied before the modulus.");')),
        ("apx-m4-s-arraydefault", BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("B. defaults are 0; exactly one cell becomes 1.");'), BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("D. invented an out-of-bounds access.");')),
        ("apx-m4-s-immut", BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("B. return value ignored, s unchanged.");'), BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("A. imagined an implicit assignment.");')),
        ("apx-m4-s-steprange", BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("C. 0,2,4 — three passes.");'), BOILER_SPEED.replace("System.out.println(letterAndReason);", 'System.out.println("D. ignored the step size.");')),
        ("apx-cp-m4-continue", r"""public class Solution {
    public static int result() {
        return 9;
    }
}
""", r"""public class Solution {
    // BUG: included the evens — traced continue as a break
    public static int result() {
        return 21;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m4", "Checkpoint: the continue trap",
    "One careful trace: continue skips an iteration, it does not end the loop.",
    12,
    r"""
Speed means nothing without correctness. The checkpoint is a trace
that punishes exactly the careless reading speed training can create:
continue is not break.
""",
    "Điểm kiểm tra: bẫy continue",
    "Một truy vết cẩn thận: continue bỏ qua một vòng, không kết thúc vòng lặp.",
    r"""
Tốc độ không có nghĩa gì nếu thiếu độ chính xác. Bài kiểm tra là một
truy vết trừng phạt đúng cách đọc bất cẩn mà luyện tốc độ dễ tạo ra:
continue không phải break.
""",
    CP4,
    VI_CP4,
    solution=r"""public class Solution {
    public static int result() {
        return 9;
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: treated continue as break — summed only 1
    public static int result() {
        return 1;
    }
}
""",
)

print("M4 done")
