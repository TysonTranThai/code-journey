#!/usr/bin/env python3
"""AP CSA Core M13 — MCQ Strategy & Error Clinic (the trap taxonomy)."""
from apcc import *

M = "cx-mcq"

L1 = r"""
42 questions, 90 minutes — about two minutes each, and the clock is the
real opponent. A working MCQ protocol:

1. **Read the code first, the question second.** Most questions show a
   program and ask "what is printed / what is true / what is returned".
   The code is the ground truth — read it top to bottom before reading
   the stem.
2. **Predict BEFORE looking at the choices.** Write your answer on
   scratch paper (trace table!). Then find it among the choices. If it
   is not there, re-trace — do not pick the closest-looking option.
   This is the single highest-yield habit: the wrong choices are built
   from your predictable mistakes.
3. **Eliminate with probes, not preference.** Empty/single/all-equal/
   order probes (Module 12) kill two or three choices in seconds.
4. **The 90-second rule.** Two minutes per question average; if you are
   past 90 seconds without a prediction, mark, move on, return. Unanswered
   questions cost the same as wrong ones on the digital exam (no
   penalty for guessing) — so NEVER leave blanks; guess at the end if
   needed.

Why prediction-first matters psychologically: the choices include
answers built from off-by-one errors, reversed conditions, and
reference confusion — exactly the states YOUR trace would visit if
done sloppily. Finding your predicted value among the choices confirms
the trace; not finding it is a signal to re-trace, not to pick.
"""

L2 = r"""
The trap taxonomy — every wrong answer on the exam belongs to a family.
Learn the families, recognize the bait:

**The `<` vs `<=` family.** Loop bounds and tie-breaking. A choice that
differs only by one included/excluded element is testing this.

**The `-1` vs `0` family.** indexOf absence, sentinel defaults, "no
match" conventions. What IS the contract's absence value?

**The `==` vs `.equals` family.** References vs content. Strings and
Integers; the answer that "works" in some tests but is wrong by
contract.

**The copy vs alias family.** `x = y` for objects copies the arrow.
A choice assuming independent objects is bait.

**The unbox family.** Integer arithmetic auto-unboxes (true), Integer
`==` Integer compares references (false for 200, true for small cached
values). A choice that says "compilation error" for `list.get(0) + 1`
is bait.

**The mutation-order family.** remove/insert during forward iteration;
second pass reading first pass's mutations. The choice "prints the
original values" is bait.

**The base-case family.** Off-by-one recursion bases (0 vs 1), missing
bases (StackOverflow), wrong seeds (fact(0) = 0).

**The division family.** Integer division truncation, `9/2 = 4`, and
the `(double)` cast that fixes it. Modulo sign on negatives (rarely
tested in AP scope but the division family is everywhere).

Practicing with families converts "tricky" into "recognized".
"""

L3 = r"""
The error clinic — a method for reviewing your OWN wrong answers (and
the debug challenges in this course):

1. **Classify before re-solving.** Which family? (Write it down.)
   Off-by-one? Reference confusion? Missed precondition?
2. **Locate the exact statement** where your reasoning diverged from
   the truth — one line, not "I guessed wrong".
3. **Name the missing check.** What probe would have caught it? (Empty?
   Tie? Absence?) Add it to your personal checklist — by exam day it
   has ~15 items and every MCQ runs through it.
4. **Re-solve from scratch**, not from "where I went wrong" — right
   answers built on patched reasoning don't transfer to the next
   question.

Example: you chose "compilation error" for
`ArrayList<Integer> list; list.add(5); int x = list.get(0) + 1;`.
Classification: unbox family. Divergence: thought `list.get(0)` was
still an Integer in arithmetic. Missing check: "arithmetic forces the
unbox." The next time any choice offers "compilation error" for
autoboxed arithmetic, your checklist fires.

The clinic loop is why this course's wrong-solution challenges matter:
every W solution in the harness is a classified, named error — the
same taxonomy, practiced from the inside.
"""

write_module(
    M,
    "MCQ Strategy & Error Clinic",
    "Prediction-first answering, the trap taxonomy (families of wrong answers), and a personal error-clinic protocol.",
    "Chiến lược MCQ & phòng sửa lỗi",
    "Trả lời dự-đoán-trước, phân loại bẫy (các họ đáp án sai), và quy trình phòng-sửa-lỗi cá nhân.",
    lessons=["cx-m13-protocol", "cx-m13-taxonomy", "cx-m13-clinic", "cx-cp-m13"],
    practices=["cx-p13-mcq"],
)

write_lesson(
    M, "cx-m13-protocol", "Prediction first",
    "The 4-step MCQ protocol, the 90-second rule, and why choices are bait.",
    12, L1,
    "Dự đoán trước",
    "Quy trình MCQ 4 bước, luật 90 giây, và vì sao các lựa chọn là mồi nhử.",
    r"""
42 câu, 90 phút — trung bình khoảng hai phút mỗi câu, và đồng hồ mới là
đối thủ thật. Một quy trình MCQ khả dụng:

1. **Đọc mã trước, câu hỏi sau.** Đa số câu hỏi đưa ra một chương trình
   rồi hỏi "in ra gì / cái nào đúng / trả về gì". Mã là chân lý — đọc
   từ trên xuống trước khi đọc đề.
2. **Dự đoán TRƯỚC khi nhìn các lựa chọn.** Viết đáp án ra giấy nháp
   (bảng truy vết!). Rồi tìm nó trong các lựa chọn. Nếu không có, truy
   vết lại — đừng chọn option trông giống nhất. Đây là thói quen đáng
   giá nhất: các lựa chọn sai được xây từ những lỗi dễ đoán của bạn.
3. **Loại trừ bằng phép dò, không bằng sở thích.** Các phép dò rỗng/đơn/
   toàn-bằng/thứ-tự (Module 12) giết hai-ba lựa chọn trong vài giây.
4. **Luật 90 giây.** Hai phút mỗi câu là trung bình; quá 90 giây mà
   chưa có dự đoán thì đánh dấu, chuyển câu, quay lại sau. Câu bỏ trống
   tốn kém như câu sai (kỳ thi digital không phạt đoán) — vì vậy
   KHÔNG BAO GIỜ bỏ trống; đoán bù ở cuối giờ nếu cần.

Vì sao dự-đoán-trước quan trọng về mặt tâm lý: các lựa chọn chứa những
đáp án được dựng từ lỗi lệch-một, điều kiện đảo, nhầm lẫn tham chiếu —
chính xác những trạng thái mà truy vết ẩu của BẠN sẽ đi qua. Tìm thấy
giá trị dự đoán trong các lựa chọn xác nhận phép truy vết; không tìm
thấy là tín hiệu để truy vết lại, không phải để chọn bừa.
""",
)

write_lesson(
    M, "cx-m13-taxonomy", "The trap taxonomy",
    "Eight families of wrong answers — recognize the bait on sight.",
    12, L2,
    "Phân loại bẫy",
    "Tám họ đáp án sai — nhận ra mồi nhử ngay khi nhìn thấy.",
    r"""
Phân loại bẫy — mọi đáp án sai trong đề thi đều thuộc một họ. Học các họ,
nhận ra mồi nhử:

**Họ `<` với `<=`.** Biên vòng lặp và phá đồng giá. Một lựa chọn chỉ
khác nhau phần tử được-tính/không-được-tính đang test cái này.

**Họ `-1` với `0`.** indexOf vắng mặt, mặc định của lính canh, quy ước
"không khớp". Hợp đồng định giá-vắng-mặt là bao nhiêu?

**Họ `==` với `.equals`.** Tham chiếu với nội dung. String và Integer;
đáp án "chạy được trong vài test nhưng sai theo hợp đồng".

**Họ bản-sao với bí-danh.** `x = y` với đối tượng là sao chép mũi tên.
Một lựa chọn giả sử các đối tượng độc lập là mồi.

**Họ mở-hộp (unbox).** Số học Integer tự mở hộp (đúng), Integer `==`
Integer so tham chiếu (sai với 200, đúng với giá trị nhỏ được đệm). Một
lựa chọn nói "lỗi biên dịch" cho `list.get(0) + 1` là mồi.

**Họ thứ-tự-biến-đổi.** remove/insert khi duyệt xuôi; lượt hai đọc đột
biến của lượt một. Lựa chọn "in các giá trị gốc" là mồi.

**Họ trường-hợp-cơ-sở.** Cơ sở lệch-một (0 với 1), thiếu cơ sở
(StackOverflow), hạt giống sai (fact(0) = 0).

**Họ phép-chia.** Cắt cụt phép chia nguyên, `9/2 = 4`, và phép ép
`(double)` sửa nó. Dấu của modulo trên số âm (hiếm khi nằm trong phạm vi
AP nhưng họ chia ở khắp nơi).

Luyện theo họ biến "khó chịu" thành "đã nhận diện".
""",
)

write_lesson(
    M, "cx-m13-clinic", "The error clinic",
    "Classify, locate, name the missing check, re-solve from scratch.",
    12, L3,
    "Phòng sửa lỗi",
    "Phân loại, định vị, gọi tên phép-kiểm-tra-còn-thiếu, giải lại từ đầu.",
    r"""
Phòng sửa lỗi — phương pháp xem lại CHÍNH đáp án sai của bạn (và các
bài debug trong khóa này):

1. **Phân loại trước khi giải lại.** Thuộc họ nào? (Ghi ra giấy.) Lệch
   một? Nhầm tham chiếu? Bỏ sót điều kiện tiên quyết?
2. **Định vị đúng câu lệnh** nơi lập luận của bạn lệch khỏi sự thật —
   một dòng, không phải "mình đoán sai".
3. **Gọi tên phép kiểm tra còn thiếu.** Phép dò nào đã chặn được nó?
   (Rỗng? Đồng giá? Vắng mặt?) Thêm vào checklist cá nhân — đến ngày
   thi nó có chừng ~15 mục và mỗi câu MCQ đi qua hết.
4. **Giải lại từ đầu**, không phải từ "mình sai ở đâu" — đáp án đúng xây
   trên lập luận vá víu không chuyển giao sang câu tiếp theo.

Ví dụ: bạn chọn "lỗi biên dịch" cho
`ArrayList<Integer> list; list.add(5); int x = list.get(0) + 1;`.
Phân loại: họ mở-hộp. Điểm lệch: tưởng `list.get(0)` vẫn là Integer
trong phép số học. Phép kiểm tra thiếu: "phép số học ép mở hộp." Lần
sau bất cứ lựa chọn nào rao "lỗi biên dịch" cho số học autoboxed,
checklist của bạn sẽ kêu.

Vòng phòng-sửa-lỗi là lý do các bài wrong-solution của khóa này quan
trọng: mỗi lời giải W trong harness là một lỗi đã phân loại, đã gọi tên
— cùng phân loại đó, luyện từ bên trong.
""",
)

BOILER_TAXONOMY = r"""public class Solution {
    // The FIXED implementation encodes a classic trap. Identify which
    // trap family and answer via the tests.
    public static int classify(int n) {
        // 1 = off-by-one bound, 2 = wrong seed/base, 3 = integer division,
        // 4 = reference vs equals, 5 = mutation order
        int total = 0;
        for (int i = 0; i <= n; i++) {
            total += 100 / 50;
        }
        return total;
    }
}
"""

BOILER_PREDICT1 = r"""public class Solution {
    // Predict WITHOUT running: what does f(6) return?
    // Then implement f yourself (same spec) and let the tests check both.
    public static int f(int n) {
        if (n == 0) {
            return 0;
        }
        return n % 10 + f(n / 10);
    }
}
"""

BOILER_PREDICT2 = r"""import java.util.ArrayList;

public class Solution {
    // Predict WITHOUT running: what does demo() return?
    public static int demo() {
        ArrayList<Integer> list = new ArrayList<Integer>();
        list.add(10);
        list.add(20);
        list.add(30);
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i) == 20) {
                list.remove(i);
            }
        }
        return list.size() * 100 + list.get(1);
    }
}
"""

BOILER_PREDICT3 = r"""public class Solution {
    // Predict WITHOUT running: what does g(5) print? (return it here)
    public static int g(int n) {
        int out = 0;
        while (n > 0) {
            out = out * 10 + n % 2;
            n /= 2;
        }
        return out;
    }
}
"""

BOILER_ELIMIN = r"""public class Solution {
    // CONTRACT: "which implementations satisfy: return true when arr
    // contains two ADJACENT equal values?" Candidates A-D were given
    // in the lesson; implement the CORRECT one.
    public static boolean adjacentEqual(int[] arr) {
        return false; // replace
    }
}
"""

BOILER_CP13 = r"""public class Solution {
    // Predict WITHOUT running, then reproduce: what does mystery return
    // for the call mystery(4)? Implement mystery (same behavior).
    // Trace: r *= i for i = 1..n, then return r + n.
    public static int mystery(int n) {
        int r = 1;
        for (int i = 1; i <= n; i++) {
            r *= i;
        }
        return r + n;
    }
}
"""

P_TAXONOMY = challenge(
    "cx-m13-classify-trap",
    "Classify the trap",
    "The code in `classify` computes with TWO planted weaknesses. Decide what a trace shows, then classify the DOMINANT family via the return value using the mapping in the comments. (This is the taxonomy, practiced.)",
    BOILER_TAXONOMY,
    [(
        "family identified",
        r"""
CjTestBase.checkEq(Solution.classify(3), 8, "loop runs n+1 times: 4 * 2");
CjTestBase.checkEq(Solution.classify(0), 2, "the <= bite at n = 0");
""",
        "100/50 = 2 (integer division), but the loop is off-by-one (<= n).",
    )],
    level="guided",
)

P_PREDICT1 = challenge(
    "cx-m13-predict-digits",
    "Predict: digit sum",
    "Do NOT run the given code in your head lazily — build the frame table. f(492): frames 492, 49, 4, 0. Predict, then reproduce f in this file (the tests enforce the true values).",
    BOILER_PREDICT1,
    [(
        "prediction checked",
        r"""
CjTestBase.checkEq(Solution.f(492), 15, "4 + 9 + 2");
CjTestBase.checkEq(Solution.f(0), 0, "base case");
CjTestBase.checkEq(Solution.f(1000000), 1, "one 1, six 0s");
""",
        "Each frame strips the last digit and adds it; base n == 0 returns 0.",
    )],
    level="independent",
)

P_PREDICT2 = challenge(
    "cx-m13-predict-removal",
    "Predict: mutation order",
    "Predict demo() by hand: which elements does the forward loop remove, what is the final list, and what does the arithmetic return? (It is NOT the 'obvious' 200 — the trap taxonomy's mutation-order family is live here.)",
    BOILER_PREDICT2,
    [(
        "mutation traced",
        r"""
CjTestBase.checkEq(Solution.demo(), 230, "list ends [10, 30]; size 2, element 1 is 30");
""",
        "i=1 removes 20; i=2 now reads past... wait: after removal size is 2, so i=2 stops. List [10, 30].",
    )],
    level="independent",
)

P_PREDICT3 = challenge(
    "cx-m13-predict-bits",
    "Predict: bit echo",
    "Trace g(5) with a state table (n, out). The while strips bits from the bottom and appends them to `out` — predict the return, then confirm by keeping the code and passing the tests.",
    BOILER_PREDICT3,
    [(
        "bits echoed",
        r"""
CjTestBase.checkEq(Solution.g(5), 101, "5 = 101b -> out 101");
CjTestBase.checkEq(Solution.g(6), 11, "6 = 110b -> out 011 = 11");
CjTestBase.checkEq(Solution.g(0), 0, "never enters loop");
""",
        "g(5): n=5 out=1; n=2 out=3; n=1 out=6... hand-trace carefully; the TESTS are ground truth.",
    )],
    level="independent",
)

P_ELIMIN = challenge(
    "cx-m13-adjacent-equal",
    "Implement the survivor",
    "The lesson presented four candidates for \"true when arr contains two ADJACENT equal values\" (A: for-each with i+1; B: loop to length-1 comparing i, i+1; C: loop to length comparing i+1; D: nested loop over all pairs). Implement the CORRECT one — the adjacency machine with the right bound.",
    BOILER_ELIMIN,
    [(
        "adjacency verified",
        r"""
CjTestBase.checkEq(Solution.adjacentEqual(new int[]{1, 2, 2, 3}), true, "2,2 adjacent");
CjTestBase.checkEq(Solution.adjacentEqual(new int[]{1, 2, 3, 2}), false, "equal but not adjacent");
CjTestBase.checkEq(Solution.adjacentEqual(new int[]{}), false, "empty");
CjTestBase.checkEq(Solution.adjacentEqual(new int[]{7}), false, "no pair possible");
""",
        "B is correct: for (int i = 0; i < arr.length - 1; i++) if (arr[i] == arr[i+1]) return true;",
    )],
    level="combination",
)

CP13 = challenge(
    "cx-cp-m13-predict-mystery",
    "Checkpoint: predict then reproduce",
    "Trace mystery(4) by hand (state table for i and r), predict the return, then reproduce the same behavior in your own implementation. Prediction-first, exactly like the exam protocol.",
    BOILER_CP13,
    [(
        "predicted and reproduced",
        r"""
CjTestBase.checkEq(Solution.mystery(4), 28, "24 + 4");
CjTestBase.checkEq(Solution.mystery(0), 1, "1 + 0");
CjTestBase.checkEq(Solution.mystery(1), 2, "1 + 1");
""",
        "r = 1*1*2*3*4 = 24 (4!), then + n.",
    )],
    level="independent",
)

write_practice(
    M, "cx-p13-mcq", "MCQ clinic",
    "Trap classification, three predictions, survivor implementation.",
    "Phòng MCQ",
    "Phân loại bẫy, ba phép dự đoán, hiện thực ứng viên trúng.",
    after_lesson="cx-m13-taxonomy", minutes=55, difficulty="advanced",
    challenges=[P_TAXONOMY, P_PREDICT1, P_PREDICT2, P_PREDICT3, P_ELIMIN],
    vi_challenges={
        "cx-m13-classify-trap": vi_challenge("Phân loại cái bẫy",
            "Mã trong `classify` tính với HAI điểm yếu được cài. Quyết định phép truy vết cho thấy gì, rồi phân loại họ LỚN NHẤT qua giá trị trả về dùng bảng ánh xạ trong chú thích. (Đây là phân loại bẫy, luyện tập.)",
            [("family identified", "100/50 = 2 (chia nguyên), nhưng vòng lặp lệch-một (<= n).")]),
        "cx-m13-predict-digits": vi_challenge("Dự đoán: tổng chữ số",
            "ĐỪNG chạy mã trong đầu một cách qua loa — dựng bảng khung. f(492): các khung 492, 49, 4, 0. Dự đoán, rồi tái hiện f trong tệp này (test bắt buộc các giá trị đúng).",
            [("prediction checked", "Mỗi khung bóc chữ số cuối rồi cộng vào; cơ sở n == 0 trả về 0.")]),
        "cx-m13-predict-removal": vi_challenge("Dự đoán: thứ tự biến đổi",
            "Dự đoán demo() bằng tay: vòng xuôi xóa những phần tử nào, danh sách cuối là gì, phép số học trả về gì? (KHÔNG phải 200 'hiển nhiên' — họ thứ-tự-biến-đổi trong phân loại đang hoạt động.)",
            [("mutation traced", "i=1 xóa 20; sau xóa size là 2 nên i=2 dừng. Danh sách [10, 30].")]),
        "cx-m13-predict-bits": vi_challenge("Dự đoán: echo bit",
            "Truy vết g(5) bằng bảng trạng thái (n, out). Vòng while bóc bit từ đáy và nối vào `out` — dự đoán giá trị trả về, rồi xác nhận bằng cách giữ nguyên mã và pass test.",
            [("bits echoed", "Truy vết tay thật cẩn thận; TEST là chân lý.")]),
        "cx-m13-adjacent-equal": vi_challenge("Hiện thực ứng viên sống sót",
            "Bài học đã đưa bốn ứng viên cho \"true khi arr chứa hai giá trị BẰNG NHAU LIỀN KỀ\" (A: for-each với i+1; B: vòng đến length-1 so i, i+1; C: vòng đến length so i+1; D: vòng lặp kép mọi cặp). Hiện thực ứng viên ĐÚNG — cỗ máy liền kề với biên đúng.",
            [("adjacency verified", "B đúng: for (int i = 0; i < arr.length - 1; i++) if (arr[i] == arr[i+1]) return true;")]),
    },
    solutions=[
        ("cx-m13-classify-trap", BOILER_TAXONOMY, BOILER_TAXONOMY.replace("total += 100 / 50;", "total += 100 / 30;")),
        ("cx-m13-predict-digits", BOILER_PREDICT1, BOILER_PREDICT1.replace("return n % 10 + f(n / 10);", "return n % 10 + f(n / 100);")),
        ("cx-m13-predict-removal", BOILER_PREDICT2, BOILER_PREDICT2.replace("return list.size() * 100 + list.get(1);", "return list.size() * 100 + list.get(0);")),
        ("cx-m13-predict-bits", BOILER_PREDICT3, BOILER_PREDICT3.replace("out = out * 10 + n % 2;", "out = out * 10 + n % 3;")),
        ("cx-m13-adjacent-equal", BOILER_ELIMIN.replace("return false; // replace",
            "for (int i = 0; i < arr.length - 1; i++) {\n            if (arr[i] == arr[i + 1]) {\n                return true;\n            }\n        }\n        return false;"),
         BOILER_ELIMIN.replace("return false; // replace",
            "for (int i = 0; i < arr.length; i++) {\n            if (arr[i] == arr[i + 1]) {\n                return true;\n            }\n        }\n        return false;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m13", "Checkpoint: prediction protocol",
    "Hand-trace, predict, reproduce — the exam protocol as a reflex.",
    20,
    r"""
mystery(4) = 28: the trace gave 24 (4!), then +4. The protocol — read,
table, predict, THEN verify — is now a reflex. In the exam room the
'tests' are the answer choices: your prediction either appears among
them (pick it and move on) or doesn't (re-trace; do not pick a
look-alike). Next module: the FRQ section, where the same discipline
produces code instead of choices.
""",
    "Điểm kiểm tra: quy trình dự đoán",
    "Truy vết tay, dự đoán, tái hiện — quy trình thi thành phản xạ.",
    r"""
mystery(4) = 28: phép truy vết cho 24 (4!), rồi +4. Quy trình — đọc,
lập bảng, dự đoán, RỒI kiểm chứng — giờ là phản xạ. Trong phòng thi,
'test' chính là các lựa chọn đáp án: dự đoán của bạn hoặc xuất hiện
trong đó (chọn và đi tiếp) hoặc không (truy vết lại; đừng chọn cái giống
nhưng không phải). Module sau: phần FRQ, nơi cùng kỷ luật đó tạo ra mã
thay vì các lựa chọn.
""",
    CP13,
    vi_challenge("Điểm kiểm tra: quy trình dự đoán",
        "Truy vết mystery(4) bằng tay (bảng trạng thái cho i và r), dự đoán giá trị trả về, rồi tái hiện hành vi đó trong bản hiện thực của riêng bạn. Dự-đoán-trước, đúng như quy trình thi.",
        [("predicted and reproduced", "r = 1*1*2*3*4 = 24 (4!), rồi + n.")]),
    solution=BOILER_CP13,
    wrong=BOILER_CP13.replace("return r + n;", "return r * n;"),
)
