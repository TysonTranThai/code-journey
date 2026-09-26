#!/usr/bin/env python3
"""AP CSA Advanced M3 — Advanced multiple choice (every ground truth executed)."""
from apx import *

M = "apx-mcq-lab"

write_module(
    M,
    "Advanced Multiple Choice",
    "Original exam-difficulty MCQs where every distractor is a named misconception. Answer, then explain every wrong option. Difficulty E3–E4.",
    "Trắc nghiệm nâng cao",
    "Trắc nghiệm gốc ở độ khó đề thi, mọi phương án nhiễu đều là một hiểu nhầm có tên. Trả lời, rồi giải thích từng phương án sai. Độ khó E3–E4.",
    lessons=["apx-m3-answers", "apx-m3-misconceptions", "apx-m3-explanations", "apx-cp-m3"],
    practices=["apx-p3-mcq1"],
)

L1 = r"""
**How to answer an exam MCQ you cannot immediately see.** Read the
question stem *first* — "what is the value of x" tells you the finish
line before you read the code. Then:

1. Skim the code for the **state that matters** (fields, parameters,
   the objects the stem names). Everything else is scenery.
2. Predict **before** reading the options. An uncommitted prediction
   protects you from plausible-sounding wrong answers.
3. Match your prediction. If no option matches, re-trace *one specific
   step* (usually a boundary or an alias), not the whole program.
4. Only guess from elimination after one honest re-trace.

On this course's MCQs: the four options are code outputs or final
states. Your submission must name the letter **and** say why — the
grader checks both, exactly like the exam rewards explanation over
vibes.
"""

L2 = r"""
**Distractors are diagnoses.** A good wrong option is not random; it
is what a *specific* misunderstanding produces:

- **Off-by-one** — `<` vs `<=`, index 0 vs index 1, `length` vs
  `length - 1`. The answer that is one position early/late.
- **Shadowing blindness** — `price = price;` in a constructor looks
  like initialization but assigns a field to itself. The wrong option
  shows the intended value; the truth is the default.
- **Alias confusion** — treating a copied reference as an independent
  object (or vice versa). Produces "mutated the copy" or "mutated the
  original" answers.
- **Immutability blindness** — assuming `s = s + "!"` inside a method
  changes the caller's string. Produces the concatenated option.
- **Dispatch confusion** — reading the *reference type* instead of the
  *object type* for overridden methods.
- **Short-circuit blindness** — assuming `&&` evaluates both sides,
  producing an exception option that never happens.

When you miss a question, name which of these bit you. A miss with a
name becomes a scanner during future traces; a miss without one
repeats.
"""

L3 = r"""
**Explaining wrong options is the highest-yield review.** For each
option you eliminated, complete the sentence: "A student picks this if
they believe ___ , but actually ___ ." Two examples:

- Option "8" for `f(4)` where `f(n) = f(n-1) + n`, `f(0) = 1`: picked
  by treating the base case as 0 (or summing 1+2+3 without +4 … no —
  by forgetting the base case returns 1, not 0). Actually the chain is
  `f(0)=1 → 1+1=2 → 2+2=4 → 4+3=7 → 7+4=11`.
- Option "[b, d]" for remove-while-iterating over `[a,b,c,d,e]`
  removing even indices: picked by forgetting that `remove` shifts
  later elements left, so the *next* comparison lands on a different
  element. Actually the survivor set is `[b, c, e]`.

Twenty of these and distractors stop fooling you — you recognize the
misconception *in the option* and reverse-engineer which trap it is.
That is the intended exam use of elimination: not "which looks right"
but "which error does each wrong answer assume."
"""

VI_L1 = r"""
**Cách trả lời trắc nghiệm bạn không nhìn ra ngay.** Đọc *đề* trước —
"giá trị của x là bao nhiêu" cho biết vạch đích trước khi bạn đọc mã.
Sau đó:

1. Lướt mã tìm **trạng thái quan trọng** (trường, tham số, các đối
   tượng đề nhắc tên). Còn lại là bối cảnh.
2. Dự đoán **trước** khi đọc các phương án. Một dự đoán chưa cam kết
   bảo vệ bạn khỏi các đáp án sai nghe rất hợp lý.
3. Đối chiếu dự đoán. Không phương án nào khớp? Truy vết lại *một bước
   cụ thể* (thường là biên hoặc bí danh), không phải cả chương trình.
4. Chỉ loại trừ để đoán sau một lần truy vết lại tử tế.

Ở các câu trắc nghiệm của khóa này: bốn phương án là kết quả in hoặc
trạng thái cuối của mã. Bài nộp phải nêu chữ cái **và** giải thích vì
sao — máy chấm kiểm tra cả hai, đúng như đề thi thưởng cho lời giải
thích hơn là cảm tính.
"""

VI_L2 = r"""
**Phương án nhiễu là bản chẩn đoán.** Một phương án sai tốt không phải
ngẫu nhiên; nó là cái mà *một* hiểu nhầm cụ thể tạo ra:

- **Lệch một đơn vị** — `<` với `<=`, chỉ số 0 với 1, `length` với
  `length - 1`. Đáp án sớm/trễ đúng một vị trí.
- **Mù bóng che** — `price = price;` trong constructor trông như khởi
  tạo nhưng gán trường cho chính nó. Phương án sai hiển thị giá trị
  mong muốn; sự thật là giá trị mặc định.
- **Nhầm bí danh** — coi tham chiếu đã sao chép là đối tượng độc lập
  (hoặc ngược lại). Tạo ra các đáp án "làm biến đổi bản sao" hoặc
  "làm biến đổi bản gốc".
- **Mù bất biến** — cho rằng `s = s + "!"` trong phương thức làm thay
  đổi chuỗi của caller. Tạo ra phương án đã nối chuỗi.
- **Nhầm điều phối** — đọc *kiểu tham chiếu* thay vì *kiểu đối tượng*
  cho phương thức ghi đè.
- **Mù ngắn mạch** — cho rằng `&&` đánh giá cả hai vế, tạo ra một
  phương án ngoại lệ không bao giờ xảy ra.

Khi mắc một câu, hãy gọi tên thủ phạm. Một lỗi có tên trở thành máy
quét trong các lần truy vết sau; một lỗi không tên sẽ lặp lại.
"""

VI_L3 = r"""
**Giải thích phương án sai là ôn tập hiệu quả nhất.** Với mỗi phương án
bạn loại, hoàn thành câu: "Học sinh chọn cái này nếu tin ___ , nhưng
thực ra ___ ." Hai ví dụ:

- Phương án "8" cho `f(4)` với `f(n) = f(n-1) + n`, `f(0) = 1`: chọn
  nếu quên trường hợp cơ sở trả 1 chứ không phải 0. Thực ra chuỗi là
  `f(0)=1 → 1+1=2 → 2+2=4 → 4+3=7 → 7+4=11`.
- Phương án "[b, d]" cho bài xóa-while-duyệt trên `[a,b,c,d,e]` với chỉ
  số chẵn: chọn nếu quên `remove` đẩy các phần tử sau sang trái, nên
  phép so sánh *kế tiếp* rơi vào phần tử khác. Thực ra tập còn sót là
  `[b, c, e]`.

Hai mươi câu như vậy và phương án nhiễu không còn đánh lừa được bạn —
bạn nhận ra hiểu nhầm *nằm trong phương án* và dịch ngược đó là bẫy
nào. Đó là cách dùng loại trừ đúng nghĩa trong phòng thi: không phải
"cái nào có vẻ đúng" mà "mỗi đáp án sai giả định lỗi nào."
"""

TEST_Q = r"""
String out = CjTestBase.capture(() -> Solution.program());
CjTestBase.checkTrue(out.startsWith("{ANS}"), "the chosen option's explanation (starts with the letter)");
"""

BOILER = r"""public class Solution {
    public static void program() {
        // Print your answer: the option letter, then a full explanation of
        // WHY it is correct and why EACH other option is wrong.
        // Example first line: B. <why B>
    }
}
"""

def mcq(cid, stem, opts, why, vi_stem, vi_opts, vi_why, level="independent", diff="advanced"):
    ans = why.split(".")[0]  # every why string opens with the option letter
    prompt = stem + "\n\n" + "\n".join(opts) + (
        "\n\nPrint your answer as: the option letter, then your explanation of why it is "
        "correct and why each other option is wrong. First line must start with the letter."
    )
    vi_prompt = vi_stem + "\n\n" + "\n".join(vi_opts) + (
        "\n\nIn đáp án của bạn là: chữ cái phương án, rồi giải thích vì sao đúng và vì sao "
        "từng phương án khác sai. Dòng đầu phải bắt đầu bằng chữ cái."
    )
    return challenge(
        cid, ("MCQ: " + stem.split("\n")[0])[:110], prompt,
        BOILER, [(ans + " " + why.split(".")[0], TEST_Q.replace("{ANS}", ans), why[:380])],
        level=level, difficulty=diff,
    ), vi_challenge(("MCQ: " + vi_stem.split("\n")[0])[:110], vi_prompt, [(ans + " " + vi_why.split(".")[0], vi_why[:380])])

Q1_S = "While iterating, which list survives? Code:\n\n```java\nArrayList<String> list = new ArrayList<String>();\nlist.add(\"x\"); list.add(\"x\"); list.add(\"b\"); list.add(\"x\");\nfor (int i = 0; i < list.size(); i++) {\n    if (list.get(i).equals(\"x\")) { list.remove(i); }\n}\nSystem.out.print(list);\n```"
Q1_O = ["A. `[b]`", "B. `[x, b]`", "C. `[b, x]`", "D. `[x, x, b]`"]
Q1_W = "B. Removals shift later elements left, so index 1 lands on 'b' (kept) and the final 'x' at index 2 is removed. A student picking A assumed every x was removed; C forgets order; D ignores the loop entirely. Verified by execution."
Q1_VS = "Trong khi duyệt, danh sách nào còn sót? Mã:\n\n```java\nArrayList<String> list = new ArrayList<String>();\nlist.add(\"x\"); list.add(\"x\"); list.add(\"b\"); list.add(\"x\");\nfor (int i = 0; i < list.size(); i++) {\n    if (list.get(i).equals(\"x\")) { list.remove(i); }\n}\nSystem.out.print(list);\n```"
Q1_VO = ["A. `[b]`", "B. `[x, b]`", "C. `[b, x]`", "D. `[x, x, b]`"]
Q1_VW = "B. Phép xóa đẩy các phần tử sau sang trái nên chỉ số 1 rơi vào 'b' (giữ lại) và 'x' cuối ở chỉ số 2 bị xóa. Chọn A là tưởng mọi x bị xóa; C quên thứ tự; D bỏ qua vòng lặp. Đã kiểm chứng bằng thực thi."

Q2_S = "What does this print?\n\n```java\npublic static void addBang(String s) { s = s + \"!\"; }\n// in main:\nString t = \"ready\";\naddBang(t);\nSystem.out.print(t);\n```"
Q2_O = ["A. `ready!`", "B. `!`", "C. compile error", "D. `ready`"]
Q2_W = "D. Strings are immutable and the parameter is a copy of the reference: addBang rebinds its LOCAL s to a new object; the caller's t still points at \"ready\". A student picking A believed mutation escapes the method; B confuses the parameter with the result; it compiles fine."
Q2_VS = "Chương trình in gì?\n\n```java\npublic static void addBang(String s) { s = s + \"!\"; }\n// trong main:\nString t = \"ready\";\naddBang(t);\nSystem.out.print(t);\n```"
Q2_VO = ["A. `ready!`", "B. `!`", "C. lỗi biên dịch", "D. `ready`"]
Q2_VW = "D. Chuỗi là bất biến và tham số là bản sao của tham chiếu: addBang gán lại s CỤC BỘ sang một đối tượng mới; t của caller vẫn trỏ \"ready\". Chọn A là tưởng phép biến đổi thoát ra khỏi phương thức; B nhầm tham số với kết quả; mã biên dịch bình thường."

Q3_S = "What is printed?\n\n```java\npublic class Animal { public String speak() { return \"...\"; } }\npublic class Dog extends Animal {\n    public String speak() { return \"woof\"; }\n    public String fetch() { return \"ball\"; }\n}\n\nAnimal a = new Dog();\nSystem.out.print(a.speak());\n```"
Q3_O = ["A. `woof`", "B. `...`", "C. compile error: Animal has no speak", "D. runtime error: cannot call speak on Dog"]
Q3_W = "A. Dynamic dispatch uses the OBJECT type (Dog), so the override runs; the reference type only limits which methods the compiler allows you to NAME. B is reference-type thinking; C is backwards (Animal is the one that declares speak); D confuses casting with dispatch."
Q3_VS = "Chương trình in gì?\n\n```java\npublic class Animal { public String speak() { return \"...\"; } }\npublic class Dog extends Animal {\n    public String speak() { return \"woof\"; }\n    public String fetch() { return \"ball\"; }\n}\n\nAnimal a = new Dog();\nSystem.out.print(a.speak());\n```"
Q3_VO = ["A. `woof`", "B. `...`", "C. lỗi biên dịch: Animal không có speak", "D. lỗi lúc chạy: không thể gọi speak trên Dog"]
Q3_VW = "A. Điều phối động dùng kiểu ĐỐI TƯỢNG (Dog) nên bản ghi đè chạy; kiểu tham chiếu chỉ giới hạn phương thức trình biên dịch cho phép GỌI TÊN. B là tư duy kiểu tham chiếu; C là ngược lại (Animal mới khai báo speak); D nhầm ép kiểu với điều phối."

Q4_S = "What is printed?\n\n```java\nSystem.out.print((double)(7 / 2));\nSystem.out.print(\" \");\nSystem.out.print((double) 7 / 2);\n```"
Q4_O = ["A. `3.0 3.5`", "B. `3.5 3.5`", "C. `3.0 3.0`", "D. `3.5 3.0`"]
Q4_W = "A. The first divides two ints first (7/2 = 3), THEN widens to 3.0; the second casts 7 before dividing, giving 3.5. B assumes the cast retroactively fixes the first expression; C/D miss which operand the cast binds to."
Q4_VS = "Chương trình in gì?\n\n```java\nSystem.out.print((double)(7 / 2));\nSystem.out.print(\" \");\nSystem.out.print((double) 7 / 2);\n```"
Q4_VO = ["A. `3.0 3.5`", "B. `3.5 3.5`", "C. `3.0 3.0`", "D. `3.5 3.0`"]
Q4_VW = "A. Phép đầu chia hai số int trước (7/2 = 3), RỒI mới nâng lên 3.0; phép thứ hai ép 7 trước khi chia, cho 3.5. B tưởng phép ép sửa hồi tố biểu thức đầu; C/D không thấy toán tử ép gắn với toán hạng nào."

Q5_S = "What is the value of `new Priced(40).get()`?\n\n```java\npublic class Priced {\n    private int price;\n    public Priced(int price) { price = price; }\n    public int get() { return price; }\n}\n```"
Q5_O = ["A. 40", "B. compile error", "C. 0", "D. runtime exception"]
Q5_W = "C. Inside the constructor both `price` names resolve to the PARAMETER, so the field is assigned from itself — i.e. never assigned — and stays at its default 0. A is the intent the code fails to achieve (this.price = price would do it); B is wrong because self-assignment is legal; nothing throws."
Q5_VS = "Giá trị của `new Priced(40).get()` là bao nhiêu?\n\n```java\npublic class Priced {\n    private int price;\n    public Priced(int price) { price = price; }\n    public int get() { return price; }\n}\n```"
Q5_VO = ["A. 40", "B. lỗi biên dịch", "C. 0", "D. ngoại lệ lúc chạy"]
Q5_VW = "C. Trong constructor, cả hai tên `price` đều chỉ về THAM SỐ, nên trường được gán từ chính nó — tức không bao giờ được gán — và giữ giá trị mặc định 0. A là ý đồ mà mã không đạt được (this.price = price mới đúng); B sai vì tự gán là hợp lệ; không có gì ném ngoại lệ."

Q6_S = "What is the result of `check(new int[]{5, 20}, 5)`?\n\n```java\npublic static boolean check(int[] arr, int idx) {\n    return idx < arr.length && arr[idx] > 10;\n}\n```"
Q6_O = ["A. true", "B. ArrayIndexOutOfBoundsException", "C. false", "D. compile error"]
Q6_W = "C. `&&` short-circuits: `5 < 2` is false, so `arr[5]` is never evaluated — no exception, just false. B is the classic short-circuit blindness; A misreads the comparison; D is wrong because the guard is exactly the safe pattern."
Q6_VS = "Kết quả của `check(new int[]{5, 20}, 5)` là gì?\n\n```java\npublic static boolean check(int[] arr, int idx) {\n    return idx < arr.length && arr[idx] > 10;\n}\n```"
Q6_VO = ["A. true", "B. ArrayIndexOutOfBoundsException", "C. false", "D. lỗi biên dịch"]
Q6_VW = "C. `&&` ngắn mạch: `5 < 2` là false nên `arr[5]` không bao giờ được đánh giá — không ngoại lệ, chỉ là false. B là mù ngắn mạch kinh điển; A đọc sai phép so sánh; D sai vì phép chặn chính là mẫu an toàn."

Q7_S = "What is printed?\n\n```java\nint[] arr1 = {1, 2, 3};\nint[] b = arr1;\nb[0] = 9;\narr1 = new int[]{4, 5, 6};\nSystem.out.print(arr1[0] + \",\" + b[0]);\n```"
Q7_O = ["A. `9,9`", "B. `4,9`", "C. `9,4`", "D. `4,4`"]
Q7_W = "B. b aliased arr1, so b[0] = 9 mutated the {1,2,3} array; rebinding arr1 to the new {4,5,6} does not affect b, which still points at the mutated original. A forgets the rebind; C/D forget the mutation."
Q7_VS = "Chương trình in gì?\n\n```java\nint[] arr1 = {1, 2, 3};\nint[] b = arr1;\nb[0] = 9;\narr1 = new int[]{4, 5, 6};\nSystem.out.print(arr1[0] + \",\" + b[0]);\n```"
Q7_VO = ["A. `9,9`", "B. `4,9`", "C. `9,4`", "D. `4,4`"]
Q7_VW = "B. b là bí danh của arr1 nên b[0] = 9 biến đổi mảng {1,2,3}; việc gán lại arr1 sang mảng mới {4,5,6} không ảnh hưởng b, vẫn trỏ mảng gốc đã biến đổi. A quên phép gán lại; C/D quên phép biến đổi."

Q8_S = "What does `f(4)` return?\n\n```java\npublic static int f(int n) {\n    if (n <= 0) { return 1; }\n    return f(n - 1) + n;\n}\n```"
Q8_O = ["A. 10", "B. 4", "C. 8", "D. 11"]
Q8_W = "D. The chain is f(0)=1, then +1, +2, +3, +4 → 11. A is 1+2+3+4 without the base case's extra 1 (i.e. f(0)=0 thinking); B/C stop the chain early or double-count the base."
Q8_VS = "`f(4)` trả về bao nhiêu?\n\n```java\npublic static int f(int n) {\n    if (n <= 0) { return 1; }\n    return f(n - 1) + n;\n}\n```"
Q8_VO = ["A. 10", "B. 4", "C. 8", "D. 11"]
Q8_VW = "D. Chuỗi là f(0)=1, rồi +1, +2, +3, +4 → 11. A là 1+2+3+4 mà thiếu phần 1 của trường hợp cơ sở (tức nghĩ f(0)=0); B/C dừng chuỗi sớm hoặc đếm trùng cơ sở."

def build(cid, s, o, w, vs, vo, vw, level, diff):
    return mcq(cid, s, o, w, vs, vo, vw, level, diff)

P1, V1 = build("apx-m3-q-removal", Q1_S, Q1_O, Q1_W, Q1_VS, Q1_VO, Q1_VW, "independent", "advanced")
P2, V2 = build("apx-m3-q-immutability", Q2_S, Q2_O, Q2_W, Q2_VS, Q2_VO, Q2_VW, "independent", "advanced")
P3, V3 = build("apx-m3-q-dispatch", Q3_S, Q3_O, Q3_W, Q3_VS, Q3_VO, Q3_VW, "independent", "advanced")
P4, V4 = build("apx-m3-q-division", Q4_S, Q4_O, Q4_W, Q4_VS, Q4_VO, Q4_VW, "guided", "advanced")
P5, V5 = build("apx-m3-q-shadowing", Q5_S, Q5_O, Q5_W, Q5_VS, Q5_VO, Q5_VW, "independent", "advanced")
P6, V6 = build("apx-m3-q-shortcircuit", Q6_S, Q6_O, Q6_W, Q6_VS, Q6_VO, Q6_VW, "guided", "advanced")
P7, V7 = build("apx-m3-q-aliasing", Q7_S, Q7_O, Q7_W, Q7_VS, Q7_VO, Q7_VW, "independent", "advanced")
P8, V8 = build("apx-m3-q-recursion", Q8_S, Q8_O, Q8_W, Q8_VS, Q8_VO, Q8_VW, "independent", "advanced")

VI = {
    "apx-m3-q-removal": V1, "apx-m3-q-immutability": V2, "apx-m3-q-dispatch": V3,
    "apx-m3-q-division": V4, "apx-m3-q-shadowing": V5, "apx-m3-q-shortcircuit": V6,
    "apx-m3-q-aliasing": V7, "apx-m3-q-recursion": V8,
}

def sol_pair(ans, why, wrong, wrongwhy):
    return (
        r"""public class Solution {
    public static void program() {
        System.out.println(""" + json.dumps(ans + ". " + why) + r""");
    }
}
""",
        r"""public class Solution {
    public static void program() {
        System.out.println(""" + json.dumps(wrong + ". " + wrongwhy) + r""");
    }
}
""",
    )

write_practice(
    M, "apx-p3-mcq1", "MCQ set 1: read the misconception",
    "Eight exam-difficulty MCQs; name the answer, then explain every distractor.",
    "Bộ trắc nghiệm 1: đọc hiểu hiểu nhầm",
    "Tám câu trắc nghiệm độ khó đề thi; nêu đáp án rồi giải thích từng phương án sai.",
    after_lesson="apx-m3-explanations", minutes=50, difficulty="advanced",
    challenges=[P1, P2, P3, P4, P5, P6, P7, P8],
    vi_challenges=VI,
    solutions=[
        ("apx-m3-q-removal",) + sol_pair("B", Q1_W, "A", "A. Picked by believing every 'x' gets removed; actually the shift skips the element that slides into the removed index."),
        ("apx-m3-q-immutability",) + sol_pair("D", Q2_W, "A", "A. Picked by believing string concatenation inside a method escapes via the parameter; actually the local reference is rebound only."),
        ("apx-m3-q-dispatch",) + sol_pair("A", Q3_W, "B", "B. Picked by reading the reference type (Animal) instead of the object type (Dog) for the overridden method."),
        ("apx-m3-q-division",) + sol_pair("A", Q4_W, "B", "B. Picked by assuming the cast applies to the whole first expression retroactively; actually int division already truncated to 3."),
        ("apx-m3-q-shadowing",) + sol_pair("C", Q5_W, "A", "A. Picked by not noticing the missing this. — the constructor assigns the parameter to itself, leaving the field at 0."),
        ("apx-m3-q-shortcircuit",) + sol_pair("C", Q6_W, "B", "B. Picked by believing && always evaluates the right side; actually short-circuit skips arr[5] entirely."),
        ("apx-m3-q-aliasing",) + sol_pair("B", Q7_W, "A", "A. Picked by forgetting arr1 is rebound to a new array before printing; b keeps the mutated original."),
        ("apx-m3-q-recursion",) + sol_pair("D", Q8_W, "A", "A. Picked by computing 1+2+3+4 with a 0 base case; the code's base case contributes an extra 1."),
    ],
)

write_checkpoint(
    M, "apx-cp-m3", "Checkpoint: MCQ with a state machine",
    "One harder MCQ: aliasing plus mutation across two references.",
    15,
    r"""
The checkpoint MCQ combines two misconceptions at once — aliasing and
mutation order. Predict first, then defend the letter.
""",
    "Điểm kiểm tra: trắc nghiệm với máy trạng thái",
    "Một câu trắc nghiệm khó hơn: bí danh cộng thứ tự biến đổi trên hai tham chiếu.",
    r"""
Câu trắc nghiệm kiểm tra kết hợp hai hiểu nhầm cùng lúc — bí danh và
thứ tự biến đổi. Dự đoán trước, rồi bảo vệ chữ cái.
""",
    challenge(
        "apx-cp-m3-box",
        "Checkpoint: two references, one object (then two)",
        "What is printed?\n\n```java\npublic class Box {\n    private int v;\n    public Box(int v) { this.v = v; }\n    public void add(int x) { v += x; }\n    public String toString() { return \"\" + v; }\n}\n\nBox b1 = new Box(5);\nBox b2 = b1;\nb2.add(3);\nb1 = new Box(10);\nb1.add(1);\nSystem.out.print(b1 + \"/\" + b2);\n```\n\n"
        "Options: A. `11/8`  B. `6/11`  C. `8/11`  D. `11/6`\n\n"
        "Print the letter, then why it is right and why each other option is wrong.",
        BOILER,
        [(
            "letter plus reasons",
            r"""
String out = CjTestBase.capture(() -> Solution.program());
CjTestBase.checkTrue(out.startsWith("D"), "the chosen option's explanation (starts with the letter)");
""",
            "b2 aliases b1 (both 8 after add(3)); b1 rebinds to a new Box(10), then 11. So 11/8.",
        )],
        level="combination",
        difficulty="advanced",
    ),
    vi_challenge(
        "Điểm kiểm tra: hai tham chiếu, một đối tượng (rồi hai)",
        "Chương trình in gì?\n\n```java\npublic class Box {\n    private int v;\n    public Box(int v) { this.v = v; }\n    public void add(int x) { v += x; }\n    public String toString() { return \"\" + v; }\n}\n\nBox b1 = new Box(5);\nBox b2 = b1;\nb2.add(3);\nb1 = new Box(10);\nb1.add(1);\nSystem.out.print(b1 + \"/\" + b2);\n```\n\n"
        "Các phương án: A. `11/8`  B. `6/11`  C. `8/11`  D. `11/6`\n\n"
        "In chữ cái, rồi giải thích vì sao đúng và vì sao từng phương án khác sai.",
        [("letter plus reasons", "b2 là bí danh của b1 (cùng 8 sau add(3)); b1 gán lại sang Box(10) mới, rồi thành 11. Vậy 11/8.")],
    ),
    solution=r"""public class Solution {
    public static void program() {
        System.out.println("D. b2 aliases b1: add(3) makes both 8. Then b1 rebinds to a NEW Box(10) and add(1) makes it 11; b2 still points at the 8 box. So 11/8. Option A printed b2 first; B/C forgot which reference rebound or that add(3) preceded the rebind.");
    }
}
""",
    wrong=r"""public class Solution {
    public static void program() {
        System.out.println("A. (wrong on purpose: swapped the two references in the output order and forgot the rebind order).");
    }
}
""",
)

print("M3 done")
