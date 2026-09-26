#!/usr/bin/env python3
"""AP CSA Core M19 — Timed Mixed Sets & Cumulative Review."""
from apcc import *

M = "cx-timed"

L1 = r"""
Timed practice differs from practice: the goal is no longer "solve
it" but "solve it at exam tempo and recover from misses". Protocol:

1. **Set the clock before reading.** This course's timed sets assume
   ~2 minutes per coding challenge (the exam's MCQ tempo). Write the
   deadline down — an untracked clock is no clock.
2. **Predict or skeleton, then decide.** At 60 seconds in, you must
   have either a diagnosis or a plan. If neither: mark, skip, return.
   Skipping is a scored skill — the digital exam has no wrong-answer
   penalty, so an eventual guess beats a blank, but a considered
   answer beats both.
3. **The two-pass sweep.** First pass: answer everything under 90
   seconds of thought. Second pass: the marked leftovers, budget in
   reverse-order of your confidence.
4. **Post-set audit (5 minutes).** For each miss: which family (Module
   13's taxonomy)? which probe would have caught it? One line in your
   error log. The audit, not the timer, is where timed practice
   actually buys points.

The timed sets in this module deliberately MIX topics — arrays,
strings, ArrayList, 2D, recursion, classes — without labels, because
the exam never tells you which machine to use.
"""

L2 = r"""
Pacing math for the real sections (verified exam shape from Module
14): 42 MCQ in 90 minutes ≈ 2:08 per question; 4 FRQ in 90 minutes =
22:30 per question. Two pacing rules follow:

**The 2:1 value rule for FRQs.** All four FRQs are worth the same,
but Q1 (methods/control) usually has the longest prose. Rule: if a
question's reading exceeds 5 minutes, bank its skeleton and move to
the next — you can always return, but you cannot recover the 22
minutes another question needs.

**The uniform-clock rule for MCQs.** Question 23 is not harder than
question 9; the difficulty ORDER on the exam is not guaranteed. Do
not "save time for the hard ones at the end" — there may be none, or
ten. Uniform two-minute sweeps with a marked second pass is the
robust strategy.

Practice translation: each timed set below has 2 challenges at
exam-difficulty spread across two topics. Do them back-to-back with a
visible 4-minute budget per pair, then audit. Two sets per sitting is
plenty — fatigue after 20 minutes of full-speed work degrades the
audit quality, and the audit is the point.
"""

L3 = r"""
Cumulative review is problems-first: reread nothing, re-derive
everything. The course's machine inventory, as a self-test checklist:

- [ ] accumulator / counter / flag / sentinel — can you write each in
      15 seconds, correctly seeded?
- [ ] state table tracing — frames for calls, objects, recursion?
- [ ] String API edges — substring(a, b) length = b − a?
- [ ] array modes — when backward, when pairwise, when index?
- [ ] ArrayList mutation — remove backward, insert backward, size()
      shifts live?
- [ ] 2D orientation — r before c, g[r].length inner bound?
- [ ] dispatch — reference type vs object class; constructor chains?
- [ ] recursion edges — base answers with zero info; two-branch call
      counts?
- [ ] FRQ workflow — eight steps without the sheet?
- [ ] salvage — skeleton, adjacent part, no panic-erase?

Anything unchecked: return to that module's lab (not its lessons) —
problems re-teach what prose only introduced. That is the ratio this
course promised: the review is also problems.
"""

write_module(
    M,
    "Timed Mixed Sets & Cumulative Review",
    "Exam-tempo mixed problem sets with the two-pass sweep and post-set audit, plus a cumulative machine inventory.",
    "Bộ đề có giờ & ôn tập lũy tiến",
    "Các bộ bài trộn theo nhịp thi với quét-hai-lượt và kiểm-sát-sau-bộ, cộng danh mục cỗ máy lũy tiến.",
    lessons=["cx-m19-protocol", "cx-m19-pacing", "cx-m19-inventory", "cx-cp-m19"],
    practices=["cx-p19-timed-a", "cx-p19-timed-b", "cx-p19-timed-c", "cx-p19-timed-d"],
)

write_lesson(
    M, "cx-m19-protocol", "The timed protocol",
    "Clock first, 60-second diagnosis gate, two-pass sweep, post-set audit.",
    12, L1,
    "Quy trình có giờ",
    "Đồng hồ trước, cửa chẩn-đoán-60-giây, quét-hai-lượt, kiểm sát sau bộ.",
    r"""
Luyện có giờ khác luyện thường: mục tiêu không còn là "giải được" mà
là "giải được theo nhịp thi và hồi phục sau các cú trượt". Quy trình:

1. **Lên đồng hồ trước khi đọc.** Các bộ có giờ của khóa này giả định
   ~2 phút mỗi bài code (nhịp MCQ của đề). Ghi thời hạn ra giấy —
   đồng hồ không theo dõi thì không phải đồng hồ.
2. **Dự đoán hoặc bộ xương, rồi quyết định.** Sau 60 giây, bạn phải có
   hoặc chẩn đoán hoặc kế hoạch. Nếu không có: đánh dấu, bỏ qua, quay
   lại. Bỏ-qua là một kỹ năng được chấm — kỳ thi digital không phạt
   đoán sai, nên một phép đoán cuối giờ vẫn thắng trang trắng, nhưng
   câu trả lời có suy nghĩ thắng cả hai.
3. **Quét hai lượt.** Lượt một: trả lời mọi thứ dưới 90 giây suy nghĩ.
   Lượt hai: phần còn lại được đánh dấu, phân bổ ngân sách theo thứ tự
   ngược độ tự tin.
4. **Kiểm sát sau bộ (5 phút).** Với mỗi câu trượt: thuộc họ nào (phân
   loại của Module 13)? phép dò nào đã chặn được? Một dòng vào nhật ký
   lỗi. Phần kiểm sát, không phải bộ đếm giờ, là nơi luyện-có-giờ thật
   sự mua điểm.

Các bộ có giờ trong module này cố tình TRỘN chủ đề — mảng, chuỗi,
ArrayList, 2D, đệ quy, lớp — không nhãn, vì đề thi không bao giờ nói
cho bạn biết phải dùng cỗ máy nào.
""",
)

write_lesson(
    M, "cx-m19-pacing", "Pacing the real sections",
    "2:08 per MCQ, 22:30 per FRQ, the 2:1 value rule, uniform-clock rule.",
    12, L2,
    "Phân bổ thời gian cho các phần thật",
    "2:08 mỗi MCQ, 22:30 mỗi FRQ, luật giá-trị-2:1, luật đồng-hồ-đều.",
    r"""
Phép toán phân bổ cho các phần thật (hình dạng đề đã kiểm chứng ở
Module 14): 42 MCQ trong 90 phút ≈ 2:08 mỗi câu; 4 FRQ trong 90 phút =
22:30 mỗi câu. Hai luật phân bổ được suy ra:

**Luật giá-trị 2:1 cho FRQ.** Cả bốn FRQ cùng giá trị, nhưng Q1
(phương thức/điều khiển) thường có phần đọc dài nhất. Luật: nếu phần
đọc của một câu vượt 5 phút, gửi kho bộ xương và chuyển câu — bạn luôn
quay lại được, nhưng không thể thu hồi 22 phút mà câu khác cần.

**Luật đồng-hồ-đều cho MCQ.** Câu 23 không khó hơn câu 9; thứ tự độ
khó trên đề không được đảm bảo. Đừng "để thời gian cho mấy câu khó ở
cuối" — có thể không có câu nào, hoặc có mười câu. Quét hai phút đều
cho mọi câu với lượt-hai-đánh-dấu là chiến lược vững nhất.

Dịch vào luyện tập: mỗi bộ có giờ dưới đây có 2 bài ở mức-độ-thi rải
trên hai chủ đề. Làm liên tiếp với ngân sách 4 phút nhìn-thấy-được cho
mỗi cặp, rồi kiểm sát. Hai bộ mỗi buổi là đủ — mệt mỏi sau 20 phút
chạy-tốc-độ-cao làm giảm chất lượng kiểm sát, và kiểm sát mới là điểm
đến.
""",
)

write_lesson(
    M, "cx-m19-inventory", "The machine inventory",
    "Ten self-test lines from the whole course; problems re-teach.",
    12, L3,
    "Danh mục cỗ máy",
    "Mười dòng tự-kiểm tra từ toàn khóa; bài-tập dạy lại.",
    r"""
Ôn lũy tiến là bài-trước-hết: không đọc lại gì, tự suy diễn lại mọi
thứ. Danh mục cỗ máy của khóa học, dưới dạng checklist tự kiểm:

- [ ] bộ cộng dồn / bộ đếm / cờ / lính canh — viết được từng cái trong
      15 giây, seed đúng chưa?
- [ ] bảng trạng thái — khung cho lời gọi, đối tượng, đệ quy?
- [ ] biên API String — substring(a, b) có độ dài = b − a?
- [ ] các chế độ mảng — khi nào ngược, khi nào từng cặp, khi nào chỉ số?
- [ ] biến đổi ArrayList — xóa ngược, chèn ngược, size() đổi tức thì?
- [ ] định hướng 2D — r trước c, biên trong là g[r].length?
- [ ] điều phối — kiểu tham chiếu với lớp đối tượng; chuỗi constructor?
- [ ] biên đệ quy — cơ sở trả lời bằng không-thông-tin; đếm gọi hai
      nhánh?
- [ ] quy trình FRQ — tám bước không cần giấy?
- [ ] cứu vớt — bộ xương, phần liền kề, không xóa-hoảng-loạn?

Mục nào chưa tick: quay về phòng-luyện của module đó (không phải các
bài học) — bài-tập dạy lại thứ văn bản chỉ giới thiệu. Đó chính là tỷ
lệ khóa này hứa: phần ôn cũng là bài-tập.
""",
)

BOILER_SETA1 = r"""public class Solution {
    // UNLABELED. Return the number of positions where the two arrays
    // differ; treat the extra tail of the longer array as differing.
    // differ({1, 2, 3}, {1, 5}) == 2
    public static int differ(int[] a, int[] b) {
        return 0; // replace
    }
}
"""

BOILER_SETA2 = r"""public class Solution {
    // UNLABELED. Return the second character of s, or '*' when s has
    // fewer than 2 characters.
    public static char secondChar(String s) {
        return ' '; // replace
    }
}
"""

BOILER_SETB1 = r"""import java.util.ArrayList;

public class Solution {
    // UNLABELED. Remove every occurrence of the value `v` (by content)
    // from words, in place. Use whichever loop direction survives
    // consecutive matches.
    public static void removeAll(ArrayList<String> words, String v) {
        // replace
    }
}
"""

BOILER_SETB2 = r"""public class Solution {
    // UNLABELED. Return the sum of the main-diagonal cells of a square
    // grid (row == col). Precondition: grid.length >= 1.
    public static int diagSum(int[][] grid) {
        return 0; // replace
    }
}
"""

BOILER_SETC1 = r"""public class Solution {
    // UNLABELED. Recursively: true when s reads the same forwards and
    // backwards. "" is a palindrome.
    public static boolean isPal(String s) {
        return false; // replace
    }
}
"""

BOILER_SETC2 = r"""public class Solution {
    // UNLABELED. Complete the class per its table:
    // private int count (starts 0); private boolean stuck (starts false)
    // void bump() — when NOT stuck: count++; when count reaches 3,
    //   set stuck = true
    // void unstick() — stuck = false (count unchanged)
    // int getCount() / boolean isStuck()
    public static class Limiter {
        // replace
    }
}
"""

BOILER_SETD1 = r"""public class Solution {
    // UNLABELED. Return the element of arr that appears an ODD number
    // of times (the test guarantees exactly one such value).
    public static int oddOne(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_SETD2 = r"""public class Solution {
    // UNLABELED. Implement this: the sum of all cells whose value is
    // strictly greater than BOTH the cell above and the cell below
    // (when those neighbors exist). Interior rows only.
    public static int verticalPeaksSum(int[][] grid) {
        return 0; // replace
    }
}
"""

P_SETA1 = challenge(
    "cx-m19-differ",
    "Timed set A-1",
    "No topic label, exam tempo (~2 minutes). Return the number of positions where the arrays differ; extra tail counts. Run your four probes on the example before coding.",
    BOILER_SETA1,
    [(
        "diffs counted",
        r"""
CjTestBase.checkEq(Solution.differ(new int[]{1, 2, 3}, new int[]{1, 5}), 2, "position 1 + tail");
CjTestBase.checkEq(Solution.differ(new int[]{}, new int[]{}), 0, "empty probe");
CjTestBase.checkEq(Solution.differ(new int[]{4}, new int[]{}), 1, "all tail");
CjTestBase.checkEq(Solution.differ(new int[]{1, 2}, new int[]{1, 2}), 0, "identical");
""",
        "Loop over min length counting mismatches, then add the length difference.",
    )],
    level="combination",
)

P_SETA2 = challenge(
    "cx-m19-second-char",
    "Timed set A-2",
    "No topic label, exam tempo. One-liner with an edge guard — the probe IS the question.",
    BOILER_SETA2,
    [(
        "char or star",
        r"""
CjTestBase.checkEq(Solution.secondChar("ab"), 'b', "normal case");
CjTestBase.checkEq(Solution.secondChar(""), '*', "empty guard");
CjTestBase.checkEq(Solution.secondChar("x"), '*', "single-char guard");
""",
        "return s.length() >= 2 ? s.charAt(1) : '*';",
    )],
    level="imitation",
)

P_SETB1 = challenge(
    "cx-m19-remove-all",
    "Timed set B-1",
    "No topic label, exam tempo. Consecutive duplicates are the grading case — pick the loop direction that survives them.",
    BOILER_SETB1,
    [(
        "all removed",
        r"""
ArrayList<String> w = new ArrayList<String>();
w.add("a"); w.add("a"); w.add("b"); w.add("a");
Solution.removeAll(w, "a");
CjTestBase.checkEq(w, List.of("b"), "consecutive and trailing removed");
ArrayList<String> e = new ArrayList<String>();
Solution.removeAll(e, "a");
CjTestBase.checkEq(e, List.of(), "empty probe");
""",
        "Backward loop: for (int i = words.size() - 1; i >= 0; i--) if (words.get(i).equals(v)) words.remove(i);",
    )],
    level="combination",
)

P_SETB2 = challenge(
    "cx-m19-diag-sum",
    "Timed set B-2",
    "No topic label, exam tempo. Grid orientation in one line — r and c must not transpose.",
    BOILER_SETB2,
    [(
        "diagonal summed",
        r"""
CjTestBase.checkEq(Solution.diagSum(new int[][]{ {1, 2}, {3, 4} }), 5, "1 + 4");
CjTestBase.checkEq(Solution.diagSum(new int[][]{ {9, 1}, {1, 8} }), 17, "9 + 8 (anti-diagonal would give 2)");
CjTestBase.checkEq(Solution.diagSum(new int[][]{ {7} }), 7, "1x1");
CjTestBase.checkEq(Solution.diagSum(new int[][]{ {1, 2, 3}, {4, 5, 6}, {7, 8, 9} }), 15, "1 + 5 + 9");
""",
        "for (int i = 0; i < grid.length; i++) total += grid[i][i];",
    )],
    level="imitation",
)

P_SETC1 = challenge(
    "cx-m19-pal",
    "Timed set C-1",
    "No topic label, exam tempo. Recursion with a two-pointer base — write the base case first, then the shrink.",
    BOILER_SETC1,
    [(
        "palindrome recursive",
        r"""
CjTestBase.checkEq(Solution.isPal(""), true, "empty is palindrome");
CjTestBase.checkEq(Solution.isPal("a"), true, "single char");
CjTestBase.checkEq(Solution.isPal("ab"), false, "mismatch");
CjTestBase.checkEq(Solution.isPal("racecar"), true, "odd length");
CjTestBase.checkEq(Solution.isPal("noon"), true, "even length");
""",
        "if (s.length() <= 1) return true; if ends differ return false; recurse on middle: isPal(s.substring(1, s.length() - 1)).",
    )],
    level="combination",
)

P_SETC2 = challenge(
    "cx-m19-limiter",
    "Timed set C-2",
    "No topic label, exam tempo. A spec-table class with an internal state transition (stuck at 3). Order matters: increment, THEN test the threshold.",
    BOILER_SETC2,
    [(
        "limiter sticks",
        r"""
Solution.Limiter l = new Solution.Limiter();
CjTestBase.checkEq(l.getCount(), 0, "starts 0");
l.bump(); l.bump();
CjTestBase.checkEq(l.isStuck(), false, "not yet");
l.bump();
CjTestBase.checkEq(l.getCount(), 3, "three bumps");
CjTestBase.checkEq(l.isStuck(), true, "stuck at 3");
l.bump();
CjTestBase.checkEq(l.getCount(), 3, "stuck: no more growth");
l.unstick();
CjTestBase.checkEq(l.isStuck(), false, "free again");
l.bump();
CjTestBase.checkEq(l.getCount(), 4, "grows after unstick");
""",
        "bump(): if (!stuck) { count++; if (count >= 3) stuck = true; }",
    )],
    level="real-world",
)

P_SETD1 = challenge(
    "cx-m19-odd-one",
    "Timed set D-1",
    "No topic label, exam tempo. Diagnosis first: counting machine + backward-looking dedup compose. (XOR is elegant but the exam accepts the pairwise form — and the pairwise form is what you should write under time.)",
    BOILER_SETD1,
    [(
        "odd occurrence found",
        r"""
CjTestBase.checkEq(Solution.oddOne(new int[]{1, 2, 2, 3, 3, 3, 3}), 1, "1 appears once");
CjTestBase.checkEq(Solution.oddOne(new int[]{5, 5, 5}), 5, "5 appears three times");
CjTestBase.checkEq(Solution.oddOne(new int[]{7}), 7, "single element");
""",
        "For each distinct value count occurrences; return the one with an odd count.",
    )],
    level="real-world",
)

P_SETD2 = challenge(
    "cx-m19-vertical-peaks",
    "Timed set D-2",
    "No topic label, exam tempo. Vertical neighbor logic + accumulator + guard — the 2D and flow machines fused. Edge rows have no vertical pair, so they never qualify.",
    BOILER_SETD2,
    [(
        "peaks summed",
        r"""
CjTestBase.checkEq(Solution.verticalPeaksSum(new int[][]{ {1, 2}, {3, 0}, {2, -5} }), 3, "col 0 peak 3; col 1 has 0, no peak");
CjTestBase.checkEq(Solution.verticalPeaksSum(new int[][]{ {1, 2}, {5, 6} }), 0, "last row excluded");
CjTestBase.checkEq(Solution.verticalPeaksSum(new int[][]{ {9} }), 0, "single row, no neighbors");
""",
        "Rows 0 and last are skipped: for r in 1..length-2, if (grid[r][c] > grid[r-1][c] && grid[r][c] > grid[r+1][c]) sum.",
    )],
    level="real-world",
)

CP19 = challenge(
    "cx-cp-m19-cumulative",
    "Checkpoint: cumulative blend",
    "One method, four machines, no labels: return the LONGEST of the words that start with `letter`, earliest on ties, or \"\" when none. (Object-free version — arrays of Strings.) Diagnose: filter + seeded max + tie rule + empty default.",
    r"""public class Solution {
    public static String longestStarting(String[] words, char letter) {
        return ""; // replace
    }
}
""",
    [(
        "machines blended",
        r"""
CjTestBase.checkEq(Solution.longestStarting(new String[]{"ab", "cde", "cade"}, 'c'), "cade", "tie keeps earliest");
CjTestBase.checkEq(Solution.longestStarting(new String[]{"ab", "cab"}, 'c'), "cab", "single match");
CjTestBase.checkEq(Solution.longestStarting(new String[]{"ab"}, 'z'), "", "none match");
CjTestBase.checkEq(Solution.longestStarting(new String[]{}, 'a'), "", "empty array");
""",
        "Seed best = \"\"; for each word starting with letter, strict > on length keeps the earliest tie.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p19-timed-a", "Timed set A",
    "Two unlabeled problems at exam tempo; audit afterwards.",
    "Bộ có giờ A",
    "Hai bài không nhãn theo nhịp thi; kiểm sát sau đó.",
    after_lesson="cx-m19-protocol", minutes=10, difficulty="advanced",
    challenges=[P_SETA1, P_SETA2],
    vi_challenges={
        "cx-m19-differ": vi_challenge("Bộ A-1 có giờ",
            "Không nhãn chủ đề, nhịp thi (~2 phút). Trả về số vị trí hai mảng khác nhau; phần đuôi thừa được tính. Chạy bốn phép dò với ví dụ trước khi viết mã.",
            [("diffs counted", "Vòng qua min-độ-dài đếm lệch, rồi cộng hiệu độ dài.")]),
        "cx-m19-second-char": vi_challenge("Bộ A-2 có giờ",
            "Không nhãn chủ đề, nhịp thi. Một dòng với lớp chặn biên — phép dò CHÍNH LÀ câu hỏi.",
            [("char or star", "return s.length() >= 2 ? s.charAt(1) : '*';")]),
    },
    solutions=[
        ("cx-m19-differ", BOILER_SETA1.replace("return 0; // replace",
            "int n = Math.min(a.length, b.length);\n        int count = 0;\n        for (int i = 0; i < n; i++) {\n            if (a[i] != b[i]) {\n                count++;\n            }\n        }\n        return count + Math.abs(a.length - b.length);"),
         BOILER_SETA1.replace("return 0; // replace",
            "int n = Math.max(a.length, b.length);\n        int count = 0;\n        for (int i = 0; i < n; i++) {\n            if (a[i] != b[i]) {\n                count++;\n            }\n        }\n        return count;")),
        ("cx-m19-second-char", BOILER_SETA2.replace("return ' '; // replace",
            "return s.length() >= 2 ? s.charAt(1) : '*';"),
         BOILER_SETA2.replace("return ' '; // replace",
            "return s.length() >= 2 ? s.charAt(0) : '*';")),
    ],
)

write_practice(
    M, "cx-p19-timed-b", "Timed set B",
    "Mutation meets orientation at exam tempo.",
    "Bộ có giờ B",
    "Biến đổi gặp định hướng theo nhịp thi.",
    after_lesson="cx-m19-protocol", minutes=10, difficulty="advanced",
    challenges=[P_SETB1, P_SETB2],
    vi_challenges={
        "cx-m19-remove-all": vi_challenge("Bộ B-1 có giờ",
            "Không nhãn chủ đề, nhịp thi. Các trùng-lặp-liên-tiếp là ca được chấm — chọn hướng vòng lặp sống sót qua chúng.",
            [("all removed", "Vòng ngược: for (int i = words.size() - 1; i >= 0; i--) if (words.get(i).equals(v)) words.remove(i);")]),
        "cx-m19-diag-sum": vi_challenge("Bộ B-2 có giờ",
            "Không nhãn chủ đề, nhịp thi. Định hướng lưới trong một dòng — r và c không được tráo.",
            [("diagonal summed", "for (int i = 0; i < grid.length; i++) total += grid[i][i];")]),
    },
    solutions=[
        ("cx-m19-remove-all",
         r"""import java.util.ArrayList;

public class Solution {
    public static void removeAll(ArrayList<String> words, String v) {
        for (int i = words.size() - 1; i >= 0; i--) {
            if (words.get(i).equals(v)) {
                words.remove(i);
            }
        }
    }
}
""",
         r"""import java.util.ArrayList;

public class Solution {
    public static void removeAll(ArrayList<String> words, String v) {
        for (int i = 0; i < words.size(); i++) {
            if (words.get(i).equals(v)) {
                words.remove(i);
            }
        }
    }
}
"""),
        ("cx-m19-diag-sum", BOILER_SETB2.replace("return 0; // replace",
            "int total = 0;\n        for (int i = 0; i < grid.length; i++) {\n            total += grid[i][i];\n        }\n        return total;"),
         BOILER_SETB2.replace("return 0; // replace",
            "int total = 0;\n        for (int i = 0; i < grid.length; i++) {\n            total += grid[i][grid.length - 1 - i];\n        }\n        return total;")),
    ],
)

write_practice(
    M, "cx-p19-timed-c", "Timed set C",
    "Recursion meets a spec table at exam tempo.",
    "Bộ có giờ C",
    "Đệ quy gặp bảng đặc tả theo nhịp thi.",
    after_lesson="cx-m19-protocol", minutes=10, difficulty="advanced",
    challenges=[P_SETC1, P_SETC2],
    vi_challenges={
        "cx-m19-pal": vi_challenge("Bộ C-1 có giờ",
            "Không nhãn chủ đề, nhịp thi. Đệ quy với cơ sở hai-con-trỏ — viết trường hợp cơ sở trước, rồi phép thu nhỏ.",
            [("palindrome recursive", "if (s.length() <= 1) return true; hai đầu lệch thì false; đệ quy vào giữa: isPal(s.substring(1, s.length() - 1)).")]),
        "cx-m19-limiter": vi_challenge("Bộ C-2 có giờ",
            "Không nhãn chủ đề, nhịp thi. Một lớp bảng-đặc-tả với chuyển-đổi-trạng-thái nội tại (kẹt ở 3). Thứ tự quan trọng: tăng, RỒI thử ngưỡng.",
            [("limiter sticks", "bump(): if (!stuck) { count++; if (count >= 3) stuck = true; }")]),
    },
    solutions=[
        ("cx-m19-pal", BOILER_SETC1.replace("return false; // replace",
            "if (s.length() <= 1) {\n            return true;\n        }\n        if (s.charAt(0) != s.charAt(s.length() - 1)) {\n            return false;\n        }\n        return isPal(s.substring(1, s.length() - 1));"),
         BOILER_SETC1.replace("return false; // replace",
            "if (s.length() <= 1) {\n            return false;\n        }\n        if (s.charAt(0) != s.charAt(s.length() - 1)) {\n            return false;\n        }\n        return isPal(s.substring(1, s.length() - 1));")),
        ("cx-m19-limiter",
         BOILER_SETC2.replace("        // replace",
            "        private int count;\n        private boolean stuck;\n\n        public Limiter() {\n            count = 0;\n            stuck = false;\n        }\n\n        public void bump() {\n            if (!stuck) {\n                count++;\n                if (count >= 3) {\n                    stuck = true;\n                }\n            }\n        }\n\n        public void unstick() {\n            stuck = false;\n        }\n\n        public int getCount() { return count; }\n        public boolean isStuck() { return stuck; }"),
         BOILER_SETC2.replace("        // replace",
            "        private int count;\n        private boolean stuck;\n\n        public Limiter() {\n            count = 0;\n            stuck = false;\n        }\n\n        public void bump() {\n            if (!stuck) {\n                count++;\n                if (count > 3) {\n                    stuck = true;\n                }\n            }\n        }\n\n        public void unstick() {\n            stuck = false;\n        }\n\n        public int getCount() { return count; }\n        public boolean isStuck() { return stuck; }")),
    ],
)

write_practice(
    M, "cx-p19-timed-d", "Timed set D",
    "Counting composition meets fused 2D logic at exam tempo.",
    "Bộ có giờ D",
    "Tổ hợp đếm gặp logic 2D hợp nhất theo nhịp thi.",
    after_lesson="cx-m19-protocol", minutes=10, difficulty="advanced",
    challenges=[P_SETD1, P_SETD2],
    vi_challenges={
        "cx-m19-odd-one": vi_challenge("Bộ D-1 có giờ",
            "Không nhãn chủ đề, nhịp thi. Chẩn đoán trước: bộ đếm + khử-trùng-lặp-nhìn-về-sau tổ hợp lại. (XOR là khéo léo nhưng phòng thi chấp nhận dạng từng-cặp — và dạng từng-cặp là cái bạn nên viết dưới áp lực thời gian.)",
            [("odd occurrence found", "Với mỗi giá trị phân biệt, đếm số lần xuất hiện; trả về cái có số-lẻ.")]),
        "cx-m19-vertical-peaks": vi_challenge("Bộ D-2 có giờ",
            "Không nhãn chủ đề, nhịp thi. Logic hàng-xóm-dọc + bộ cộng dồn + lớp chặn — các cỗ máy 2D và luồng hợp nhất. Các hàng mép không có cặp dọc nên không bao giờ đạt chuẩn.",
            [("peaks summed", "Bỏ hàng 0 và hàng cuối: cho r trong 1..length-2, nếu (grid[r][c] > grid[r-1][c] && grid[r][c] > grid[r+1][c]) thì cộng.")]),
    },
    solutions=[
        ("cx-m19-odd-one", BOILER_SETD1.replace("return 0; // replace",
            "for (int i = 0; i < arr.length; i++) {\n            int count = 0;\n            for (int j = 0; j < arr.length; j++) {\n                if (arr[j] == arr[i]) {\n                    count++;\n                }\n            }\n            if (count % 2 == 1) {\n                return arr[i];\n            }\n        }\n        return 0;"),
         BOILER_SETD1.replace("return 0; // replace",
            "for (int i = 0; i < arr.length; i++) {\n            int count = 0;\n            for (int j = 0; j < arr.length; j++) {\n                if (arr[j] == arr[i]) {\n                    count++;\n                }\n            }\n            if (count % 2 == 0) {\n                return arr[i];\n            }\n        }\n        return 0;")),
        ("cx-m19-vertical-peaks", BOILER_SETD2.replace("return 0; // replace",
            "int total = 0;\n        for (int r = 1; r < grid.length - 1; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (grid[r][c] > grid[r - 1][c] && grid[r][c] > grid[r + 1][c]) {\n                    total += grid[r][c];\n                }\n            }\n        }\n        return total;"),
         BOILER_SETD2.replace("return 0; // replace",
            "int total = 0;\n        for (int r = 0; r < grid.length; r++) {\n            for (int c = 0; c < grid[r].length; c++) {\n                if (grid[r][c] > grid[r - 1][c] && grid[r][c] > grid[r + 1][c]) {\n                    total += grid[r][c];\n                }\n            }\n        }\n        return total;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m19", "Checkpoint: cumulative blend",
    "Filter + seeded max + tie rule + empty default in one unlabeled method.",
    20,
    r"""
longestStarting is the course in miniature: diagnose (return type is
a String → builder/default), name the machines (filter, seeded max,
strict > for ties), honor the vacuous default ("" when nothing
qualifies), and probe before submitting. If you wrote this in under
five minutes with all four probes passing on the first run, the
machine inventory is yours.
""",
    "Điểm kiểm tra: pha trộn lũy tiến",
    "Lọc + max có seed + luật đồng giá + mặc định rỗng trong một phương thức không nhãn.",
    r"""
longestStarting là cả khóa học thu nhỏ: chẩn đoán (kiểu trả về là
String → bộ-dựng/mặc-định), gọi tên các cỗ máy (lọc, max có seed, dấu >
nghiêm ngặt cho đồng giá), tôn trọng mặc định chân-không ("" khi không
có gì đạt), và dò trước khi nộp. Nếu bạn viết xong dưới năm phút với cả
bốn phép dò pass ngay lần đầu, danh mục cỗ máy đã là của bạn.
""",
    CP19,
    vi_challenge("Điểm kiểm tra: pha trộn lũy tiến",
        "Một phương thức, bốn cỗ máy, không nhãn: trả về từ DÀI NHẤT bắt đầu bằng `letter`, sớm nhất khi đồng giá, hoặc \"\" khi không có. (Bản không-đối-tượng — mảng String.) Chẩn đoán: lọc + max có seed + luật đồng giá + mặc định rỗng.",
        [("machines blended", "Seed best = \"\"; với mỗi từ bắt đầu bằng letter, dấu > nghiêm ngặt trên độ dài giữ đồng giá sớm nhất.")]),
    solution=r"""public class Solution {
    public static String longestStarting(String[] words, char letter) {
        String best = "";
        for (String w : words) {
            if (w.length() > 0 && w.charAt(0) == letter) {
                if (w.length() > best.length()) {
                    best = w;
                }
            }
        }
        return best;
    }
}
""",
    wrong=r"""public class Solution {
    public static String longestStarting(String[] words, char letter) {
        String best = "";
        for (String w : words) {
            if (w.length() > 0 && w.charAt(w.length() - 1) == letter) {
                if (w.length() > best.length()) {
                    best = w;
                }
            }
        }
        return best;
    }
}
""",
)
