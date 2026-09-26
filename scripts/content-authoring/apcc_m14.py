#!/usr/bin/env python3
"""AP CSA Core M14 — FRQ Fundamentals (exam shape + workflow)."""
from apcc import *

M = "cx-frq-fund"

L1 = r"""
Section II: four free-response questions, 90 minutes, 45% of the exam
score — 22.5 minutes per question on average. All four assess writing
Java on the digital exam (typed, no handwriting). The four question
types, fixed every year:

**Q1 — Methods and Control Structures.** Two methods (or a constructor
plus a method) from a provided context. Simulation or processing
logic. The most algorithmic of the four.

**Q2 — Class Design.** You complete or write a class: fields,
constructor, and methods per a spec table. Explicitly graded on
encapsulation choices.

**Q3 — ArrayList / data analysis.** One method of a provided class
that processes an `ArrayList` of objects or values. Counting,
filtering, aggregating are the verbs.

**Q4 — 2D array.** One method over a grid. Position logic, traversal,
neighbors.

Each is worth the same — 9 points raw — so pacing is simple: do not
let Q1's story text eat Q4's grid time. Scoring guides award points
per behavior: **partial credit is real and systematic.** A method with
correct traversal but a broken final computation earns most of its
points. This shapes strategy: write SOMETHING correct for every part —
a correct loop with a wrong return beats a blank.
"""

L2 = r"""
The eight-step FRQ workflow — run it identically on every question:

1. **Read the WHOLE prompt** including the example runs before writing
   anything. The examples at the bottom are executable specifications:
   they define edge cases the prose implied.
2. **Circle the signature(s)** and write them at the top of your
   answer space. Signatures are given; do not "improve" them.
3. **Extract the obligations** — one bullet per behavior, in order.
   ("adds", "returns -1 when", "does not modify").
4. **Decompose**: does this need a helper? Two loops? A seeded
   accumulator? Name the machines (Module 12's diagnosis, now under
   time pressure).
5. **Write the simplest correct implementation.** No cleverness; no
   streams; plain loops and ifs. The rubric rewards correctness and
   clarity, never style points.
6. **Test against the examples** by hand-tracing your own code — the
   trace table, one row per loop iteration.
7. **Check the edge cases** the prose hinted at: empty, single,
   absent, boundary values, the "otherwise" branch.
8. **Review against the specification** — reread every obligation
   bullet and confirm the code honors each. This 30-second pass is
   the highest-points-per-second activity on the entire exam.

Steps 5–8 are where points live; steps 1–4 are where points are saved.
"""

L3 = r"""
Answer-shape conventions that earn (or bleed) points:

**Return exactly what the type demands.** `int` return → return an int
expression; no printing, ever, unless the prompt says "print". A
printing solution in a return-typed part usually scores 0 for that
part.

**Match the identifier case.** `getTotal`, not `gettotal` — graders
are human and rubrics cite names; near-miss identifiers read as wrong
methods.

**Respect the private fields.** FRQ class parts say "you may add
private helpers/fields" or forbid extra state. When the spec table
names fields, use exactly those — inventing parallel state (Module 9's
ShoppingCart memory field) is only correct when explicitly permitted.

**The access discipline.** Public methods per spec; private helpers
freely; never make fields public in an answer.

**Write code, not prose.** A part asking to "implement" wants Java.
Partial code with a comment like "// loop here" earns partial credit
if the visible parts are correct — a paragraph of English earns
nothing. If you cannot finish, finish the signature, the guard, and
the loop skeleton: graded behaviors often live in the skeleton.

**Example-decoding drill:** given "returns the number of positions
where the two arrays differ, treating missing tail positions as
differing", the example `differ({1,2,3}, {1,5}) == 2` proves BOTH the
length-min mismatch counting AND the tail rule in one line. FRQ
examples are dense; read them as test cases, not decoration.
"""

write_module(
    M,
    "FRQ Fundamentals",
    "The four FRQ question types and scoring shape, the eight-step workflow, and answer conventions that earn points.",
    "Nền tảng FRQ",
    "Bốn dạng câu hỏi FRQ và hình dạng chấm điểm, quy trình tám bước, và các quy ước trình bày đáp án giúp lấy điểm.",
    lessons=["cx-m14-exam-shape", "cx-m14-workflow", "cx-m14-conventions", "cx-cp-m14"],
    practices=["cx-p14-frq"],
)

write_lesson(
    M, "cx-m14-exam-shape", "The exam's FRQ shape",
    "Four types, equal weight, behavior-based rubrics, partial credit.",
    12, L1,
    "Hình dạng FRQ của đề thi",
    "Bốn dạng, trọng số ngang nhau, bảng chấm theo hành vi, điểm một phần.",
    r"""
Phần II: bốn câu tự luận, 90 phút, 45% điểm bài thi — trung bình 22,5
phút mỗi câu. Cả bốn đều đánh giá việc viết Java trên máy (kỳ thi
digital, gõ phím). Bốn dạng câu hỏi, cố định mỗi năm:

**Q1 — Phương thức và cấu trúc điều khiển.** Hai phương thức (hoặc một
constructor cộng một phương thức) trong ngữ cảnh được cung cấp. Logic
mô phỏng hoặc xử lý. Trong bốn dạng, đây là dạng nhiều thuật toán nhất.

**Q2 — Thiết kế lớp.** Bạn hoàn thiện hoặc viết một lớp: trường,
constructor, và phương thức theo bảng đặc tả. Được chấm tường minh về
lựa chọn đóng gói.

**Q3 — ArrayList / phân tích dữ liệu.** Một phương thức của lớp được
cung cấp, xử lý một `ArrayList` đối tượng hoặc giá trị. Đếm, lọc, cộng
dồn là các động từ chính.

**Q4 — Mảng 2 chiều.** Một phương thức trên lưới. Logic vị trí, duyệt,
hàng xóm.

Mỗi câu cùng giá trị — 9 điểm thô — nên phân bổ thời gian rất đơn giản:
đừng để phần tường-thuật của Q1 ăn mất thời gian lưới của Q4. Bảng chấm
thưởng theo hành vi: **điểm một phần là thật và có hệ thống.** Một
phương thức có phần duyệt đúng nhưng phép tính cuối sai vẫn được đa số
điểm. Điều này định hình chiến lược: viết MỘT CÁI GÒ ĐÓ đúng cho mọi
phần — một vòng lặp đúng với phép trả về sai thắng một trang giấy trắng.
""",
)

write_lesson(
    M, "cx-m14-workflow", "The eight-step workflow",
    "Read, extract, decompose, write simple, trace, edge-check, review.",
    12, L2,
    "Quy trình tám bước",
    "Đọc, trích xuất, phân rã, viết đơn giản, truy vết, kiểm biên, rà soát.",
    r"""
Quy trình FRQ tám bước — chạy y hệt với mọi câu hỏi:

1. **Đọc TOÀN BỘ đề**, kể cả các ví dụ minh họa, trước khi viết gì.
   Các ví dụ ở cuối đề là đặc tả chạy được: chúng định nghĩa các
   trường hợp biên mà phần văn bản ngụ ý.
2. **Khoanh chữ ký** và viết chúng lên đầu vùng trả lời. Chữ ký đã cho;
   đừng "cải tiến" nó.
3. **Trích các nghĩa vụ** — mỗi hành vi một gạch đầu dòng, theo thứ tự.
   ("thêm", "trả về -1 khi", "không làm thay đổi").
4. **Phân rã**: có cần hàm trợ giúp không? Hai vòng lặp? Bộ cộng dồn có
   seed? Gọi tên các cỗ máy (chẩn đoán của Module 12, nay dưới áp lực
   thời gian).
5. **Viết bản hiện thực đơn giản nhất có thể đúng.** Không khéo léo;
   không stream; chỉ vòng lặp và if thuần. Bảng chấm thưởng tính đúng
   và rõ ràng, không thưởng phong cách.
6. **Kiểm thử với các ví dụ** bằng cách truy vết tay chính mã của bạn —
   bảng truy vết, mỗi vòng lặp một hàng.
7. **Kiểm tra các trường hợp biên** mà phần văn bản gợi ý: rỗng, đơn,
   vắng mặt, giá trị biên, nhánh "trong trường hợp khác".
8. **Rà soát với đặc tả** — đọc lại từng nghĩa vụ và xác nhận mã tôn
   trọng từng cái. Lượt 30 giây này là hoạt động hiệu-nhất-theo-giây
   của toàn bộ kỳ thi.

Bước 5–8 là nơi điểm nằm; bước 1–4 là nơi điểm được cứu.
""",
)

write_lesson(
    M, "cx-m14-conventions", "Answer conventions",
    "Return shapes, identifier fidelity, private discipline, code-not-prose.",
    12, L3,
    "Quy ước trình bày",
    "Hình dạng trả về, trung thành với định danh, kỷ luật private, viết-mã-không-viết-văn.",
    r"""
Các quy ước hình-đáp-án lấy điểm (hoặc mất điểm):

**Trả về đúng cái kiểu đòi hỏi.** `int` return → trả về một biểu thức
int; không in, trừ khi đề nói "in". Lời giải in ra màn hình trong một
phần yêu cầu trả về thường được 0 điểm cho phần đó.

**Khớp viết hoa của định danh.** `getTotal`, không phải `gettotal` —
người chấm là con người và bảng chấm trích dẫn tên; định danh suýt-sai
đọc như phương thức sai.

**Tôn trọng các trường private.** Các phần lớp của FRQ nói "bạn được
phép thêm hàm/trường private" hoặc cấm trạng thái thừa. Khi bảng đặc tả
liệt kê trường, dùng đúng những trường đó — tự bịa trạng thái song song
(trường ghi nhớ ShoppingCart của Module 9) chỉ đúng khi được cho phép
tường minh.

**Kỷ luật truy cập.** Phương thức public theo đặc tả; hàm trợ giúp
private thoải mái; không bao giờ biến trường thành public trong lời
giải.

**Viết mã, không viết văn.** Phần yêu cầu "hiện thực" muốn Java. Mã dở
dang kèm chú thích "// vòng lặp ở đây" được điểm một phần nếu phần hiện
ra đúng — một đoạn văn tiếng Anh được 0 điểm. Nếu không kịp, hoàn thiện
chữ ký, lớp chặn, và bộ xương vòng lặp: các hành vi được chấm thường
nằm trong bộ xương.

**Bài luyện giải-mã-ví-dụ:** cho "trả về số vị trí hai mảng khác nhau,
coi các vị trí đuôi thiếu của mảng ngắn là khác nhau", ví dụ
`differ({1,2,3}, {1,5}) == 2` chứng minh CẢ luật đếm lệch theo min-độ-
dài VÀ luật đuôi trong một dòng. Ví dụ FRQ rất cô đặc; đọc chúng như
các ca kiểm thử, không phải trang trí.
""",
)

BOILER_SUMRANGE = r"""public class Solution {
    // FRQ-style Q1: implement from the spec below.
    // (a) int sumRange(int lo, int hi): the sum lo + (lo+1) + ... + hi.
    //     Precondition: 0 <= lo <= hi.
    // (b) int sumEvenRange(int lo, int hi): the sum of the EVEN numbers
    //     in [lo, hi]. Precondition: 0 <= lo <= hi. Use sumRange-style
    //     logic; no helper required.
    public static int sumRange(int lo, int hi) {
        return 0; // replace-a
    }

    public static int sumEvenRange(int lo, int hi) {
        return 0; // replace-b
    }
}
"""

BOILER_TOKENS = r"""public class Solution {
    // FRQ-style Q1b: token processing.
    // (a) boolean isBalanced(String s): s contains only '(' and ')';
    //     true when every prefix has at least as many '(' as ')' and
    //     the total counts are equal. "" is balanced.
    // (b) int depth(String s): the MAXIMUM nesting depth of the same
    //     string; "" has depth 0. (Assume isBalanced(s) is true.)
    public static boolean isBalanced(String s) {
        return false; // replace
    }

    public static int depth(String s) {
        return 0; // replace
    }
}
"""

BOILER_CP14 = r"""public class Solution {
    // FRQ-style Q1, two-method shape:
    // (a) int countChar(String s, char c): occurrences of c in s.
    // (b) boolean scattered(String s, char c, int k): true when c
    //     appears at least k times, using countChar.
    //     Precondition: k >= 0.
    public static int countChar(String s, char c) {
        return 0; // replace
    }

    public static boolean scattered(String s, char c, int k) {
        return false; // replace
    }
}
"""

P_SUMRANGE = challenge(
    "cx-m14-sum-range",
    "Q1 shape: two methods",
    "Implement both methods from the spec. (a) is a one-loop accumulator; (b) reuses the same shape with a filter inside. Follow the workflow: obligations first, then code.",
    BOILER_SUMRANGE,
    [(
        "both ranges",
        r"""
CjTestBase.checkEq(Solution.sumRange(1, 3), 6, "1+2+3");
CjTestBase.checkEq(Solution.sumRange(5, 5), 5, "single-term range");
CjTestBase.checkEq(Solution.sumEvenRange(1, 7), 12, "2+4+6");
CjTestBase.checkEq(Solution.sumEvenRange(2, 2), 2, "single even");
CjTestBase.checkEq(Solution.sumEvenRange(3, 3), 0, "no evens in range");
""",
        "sumRange: for i lo..hi, total += i. sumEvenRange: same loop, add only when i % 2 == 0.",
    )],
    level="guided",
)

P_TOKENS = challenge(
    "cx-m14-tokens",
    "Q1 shape: state machine",
    "Implement `isBalanced` (running count, never negative, ends at zero) and `depth` (track the running level, record its max). Both are one-pass counters over characters — the workflow's decomposition step names them instantly.",
    BOILER_TOKENS,
    [(
        "balanced and deep",
        r"""
CjTestBase.checkEq(Solution.isBalanced(""), true, "empty is balanced");
CjTestBase.checkEq(Solution.isBalanced("()"), true, "one pair");
CjTestBase.checkEq(Solution.isBalanced(")("), false, "prefix goes negative");
CjTestBase.checkEq(Solution.isBalanced("(()"), false, "ends non-zero");
CjTestBase.checkEq(Solution.depth(""), 0, "empty depth");
CjTestBase.checkEq(Solution.depth("()(())"), 2, "nesting peaks at 2");
CjTestBase.checkEq(Solution.depth("((()))"), 3, "three deep");
""",
        "isBalanced: open++ on '(', open-- on ')', return open == 0 AND never dipped; depth: max of running level.",
    )],
    level="combination",
)

P_COUNTCHAR = challenge(
    "cx-m14-count-char",
    "Q1 shape: count + composition",
    "Implement `countChar` (a plain counter) and `scattered` (composes countChar with a comparison — the FRQ loves a part (b) that consumes part (a)).",
    BOILER_CP14,
    [(
        "count and compare",
        r"""
CjTestBase.checkEq(Solution.countChar("banana", 'a'), 3, "three a's");
CjTestBase.checkEq(Solution.countChar("", 'a'), 0, "empty string");
CjTestBase.checkEq(Solution.scattered("banana", 'a', 3), true, "exactly k");
CjTestBase.checkEq(Solution.scattered("banana", 'a', 4), false, "fewer than k");
CjTestBase.checkEq(Solution.scattered("xyz", 'a', 0), true, "k = 0 always true");
""",
        "scattered: return countChar(s, c) >= k; — composition IS the answer.",
    )],
    level="independent",
)

CP14 = challenge(
    "cx-cp-m14-word-metrics",
    "Checkpoint: two-method FRQ under contract",
    "A complete Q1-style question: (a) `int countWords(String s)`: words are maximal runs of non-space characters; s may have leading/trailing/multiple spaces; "" has 0 words. (b) `String longestWord(String s)`: the longest word, earliest on ties ("" returns ""). Both from scratch — run the full eight-step workflow on paper first.",
    r"""public class Solution {
    public static int countWords(String s) {
        return 0; // replace
    }

    public static String longestWord(String s) {
        return ""; // replace
    }
}
""",
    [(
        "word metrics",
        r"""
CjTestBase.checkEq(Solution.countWords(""), 0, "empty");
CjTestBase.checkEq(Solution.countWords("  hello   world  "), 2, "spaces everywhere");
CjTestBase.checkEq(Solution.countWords("solo"), 1, "single word");
CjTestBase.checkEq(Solution.longestWord(""), "", "empty longest");
CjTestBase.checkEq(Solution.longestWord("  hello   world  "), "hello", "earliest of ties? no: 5 == 5, first wins");
CjTestBase.checkEq(Solution.longestWord("a bb ccc"), "ccc", "strictly longest");
""",
        "Scan for run starts; track current run length; on run end compare with best (strict > keeps earliest).",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p14-frq", "FRQ fundamentals lab",
    "Two-method shapes, state machines, and a composed counter.",
    "Phòng nền tảng FRQ",
    "Các hình hai-phương-thức, máy trạng thái, và một bộ đếm có tổ hợp.",
    after_lesson="cx-m14-workflow", minutes=60, difficulty="advanced",
    challenges=[P_SUMRANGE, P_TOKENS, P_COUNTCHAR, CP14],
    vi_challenges={
        "cx-m14-sum-range": vi_challenge("Hình Q1: hai phương thức",
            "Hiện thực cả hai phương thức từ đặc tả. (a) là một bộ cộng dồn một-vòng-lặp; (b) dùng lại hình dạng đó với bộ lọc bên trong. Theo quy trình: nghĩa vụ trước, mã sau.",
            [("both ranges", "sumRange: for i lo..hi, total += i. sumEvenRange: cùng vòng lặp, chỉ cộng khi i % 2 == 0.")]),
        "cx-m14-tokens": vi_challenge("Hình Q1: máy trạng thái",
            "Hiện thực `isBalanced` (bộ đếm chạy, không bao giờ âm, kết thúc ở 0) và `depth` (theo dõi bậc hiện hành, ghi lại mức tối đa). Cả hai là bộ đếm một-lượt qua ký tự — bước phân rã của quy trình gọi tên chúng ngay lập tức.",
            [("balanced and deep", "isBalanced: open++ với '(', open-- với ')', return open == 0 VÀ không bao giờ tụt; depth: max của bậc chạy.")]),
        "cx-m14-count-char": vi_challenge("Hình Q1: đếm + tổ hợp",
            "Hiện thực `countChar` (một bộ đếm thuần) và `scattered` (tổ hợp countChar với một phép so sánh — FRQ rất thích phần (b) tiêu thụ phần (a)).",
            [("count and compare", "scattered: return countChar(s, c) >= k; — tổ hợp CHÍNH LÀ đáp án.")]),
        "cx-cp-m14-word-metrics": vi_challenge("Điểm kiểm tra: FRQ hai phương thức dưới hợp đồng",
            "Một câu hỏi kiểu-Q1 hoàn chỉnh: (a) `int countWords(String s)`: từ là các đoạn cực đại ký-tự-không-khoảng-trắng; s có thể có khoảng trắng đầu/cuối/liên-tục; \"\" có 0 từ. (b) `String longestWord(String s)`: từ dài nhất, sớm nhất khi đồng giá (\"\" trả về \"\"). Viết từ đầu — chạy đủ quy trình tám bước trên giấy trước.",
            [("word metrics", "Quét các điểm bắt đầu đoạn; theo dõi độ dài đoạn hiện hành; khi đoạn kết thúc so với best (dấu > nghiêm ngặt giữ người sớm).")]),
    },
    solutions=[
        ("cx-m14-sum-range",
         BOILER_SUMRANGE.replace("        return 0; // replace-a", "        int total = 0;\n        for (int i = lo; i <= hi; i++) {\n            total += i;\n        }\n        return total;")
            .replace("        return 0; // replace-b", "        int total = 0;\n        for (int i = lo; i <= hi; i++) {\n            if (i % 2 == 0) {\n                total += i;\n            }\n        }\n        return total;"),
         BOILER_SUMRANGE.replace("        return 0; // replace-a", "        int total = 0;\n        for (int i = lo; i <= hi; i++) {\n            total += i;\n        }\n        return total;")
            .replace("        return 0; // replace-b", "        int total = 0;\n        for (int i = lo; i <= hi; i++) {\n            if (i % 2 == 1) {\n                total += i;\n            }\n        }\n        return total;")),
        ("cx-m14-tokens",
         BOILER_TOKENS.replace("        return false; // replace", "        int open = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) == '(') {\n                open++;\n            } else {\n                open--;\n            }\n            if (open < 0) {\n                return false;\n            }\n        }\n        return open == 0;")
            .replace("        return 0; // replace", "        int level = 0;\n        int max = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) == '(') {\n                level++;\n                if (level > max) {\n                    max = level;\n                }\n            } else {\n                level--;\n            }\n        }\n        return max;"),
         BOILER_TOKENS.replace("        return false; // replace", "        int open = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) == '(') {\n                open++;\n            } else {\n                open--;\n            }\n            if (open < 0) {\n                return true;\n            }\n        }\n        return open == 0;")
            .replace("        return 0; // replace", "        int level = 0;\n        int max = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) == '(') {\n                level++;\n                if (level > max) {\n                    max = level;\n                }\n            } else {\n                level--;\n            }\n        }\n        return level;")),
        ("cx-m14-count-char",
         BOILER_CP14.replace("        return 0; // replace", "        int count = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) == c) {\n                count++;\n            }\n        }\n        return count;")
            .replace("        return false; // replace", "        return countChar(s, c) >= k;"),
         BOILER_CP14.replace("        return 0; // replace", "        int count = 0;\n        for (int i = 0; i < s.length(); i++) {\n            if (s.charAt(i) == c) {\n                count++;\n            }\n        }\n        return count;")
            .replace("        return false; // replace", "        return countChar(s, c) > k;")),
        ("cx-cp-m14-word-metrics",
         r"""public class Solution {
    public static int countWords(String s) {
        int count = 0;
        boolean inWord = false;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                if (!inWord) {
                    count++;
                }
                inWord = true;
            } else {
                inWord = false;
            }
        }
        return count;
    }

    public static String longestWord(String s) {
        String best = "";
        String current = "";
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                current += s.charAt(i);
            } else {
                if (current.length() > best.length()) {
                    best = current;
                }
                current = "";
            }
        }
        if (current.length() > best.length()) {
            best = current;
        }
        return best;
    }
}
""",
         r"""public class Solution {
    public static int countWords(String s) {
        int count = 0;
        boolean inWord = false;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                if (!inWord) {
                    count++;
                }
                inWord = true;
            } else {
                inWord = false;
            }
        }
        return count;
    }

    public static String longestWord(String s) {
        String best = "";
        String current = "";
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                current += s.charAt(i);
            } else {
                if (current.length() > best.length()) {
                    best = current;
                }
                current = "";
            }
        }
        if (current.length() > best.length()) {
            best = current;
        }
        return best + "!";
    }
}
"""),
    ],
)

write_checkpoint(
    M, "cx-cp-m14", "Checkpoint: word metrics",
    "A full Q1-style question run through the eight-step workflow.",
    30,
    r"""
countWords is the state-machine counter (inWord flag); longestWord is
the builder + seeded-best with the earliest-tie rule and the post-loop
flush — the fencepost cousin from Module 3. If your first draft
failed "  a  b " with extra words or missed the final word, the flush
was the missing obligation — exactly what workflow step 8 catches.
""",
    "Điểm kiểm tra: chỉ số từ ngữ",
    "Một câu hỏi kiểu-Q1 đầy đủ chạy qua quy trình tám bước.",
    r"""
countWords là bộ-đếm-máy-trạng-thái (cờ inWord); longestWord là
bộ-dựng + best-có-seed với luật đồng-giá-sớm và xả-sau-vòng-lặp — anh
họ hàng-rào của Module 3. Nếu bản nháp đầu trượt "  a  b " vì thừa từ
hoặc sót từ cuối, phép xả chính là nghĩa vụ còn thiếu — đúng thứ bước 8
của quy trình bắt được.
""",
    CP14,
    vi_challenge("Điểm kiểm tra: chỉ số từ ngữ",
        "Một câu hỏi kiểu-Q1 đầy đủ chạy qua quy trình tám bước: countWords và longestWord với mọi trường hợp khoảng trắng.",
        [("word metrics", "Quét các điểm bắt đầu đoạn; theo dõi độ dài đoạn; so với best bằng dấu > nghiêm ngặt; nhớ xả đoạn cuối SAU vòng lặp.")]),
    solution=r"""public class Solution {
    public static int countWords(String s) {
        int count = 0;
        boolean inWord = false;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                if (!inWord) {
                    count++;
                }
                inWord = true;
            } else {
                inWord = false;
            }
        }
        return count;
    }

    public static String longestWord(String s) {
        String best = "";
        String current = "";
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                current += s.charAt(i);
            } else {
                if (current.length() > best.length()) {
                    best = current;
                }
                current = "";
            }
        }
        if (current.length() > best.length()) {
            best = current;
        }
        return best;
    }
}
""",
    wrong=r"""public class Solution {
    public static int countWords(String s) {
        int count = 0;
        boolean inWord = false;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                if (!inWord) {
                    count++;
                }
                inWord = true;
            } else {
                inWord = false;
            }
        }
        return count;
    }

    public static String longestWord(String s) {
        String best = "";
        String current = "";
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                current += s.charAt(i);
            } else {
                if (current.length() > best.length()) {
                    best = current;
                }
                current = "";
            }
        }
        return best;
    }
}
""",
)
