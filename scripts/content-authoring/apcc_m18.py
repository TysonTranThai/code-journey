#!/usr/bin/env python3
"""AP CSA Core M18 — FRQ Debugging & Partial Credit (broken-solution clinic)."""
from apcc import *

M = "cx-frq-debug"

L1 = r"""
The exam does not ask "is this code right?" — it asks "which change
makes it right?" and grades the diagnosis. The localization loop:

1. **Restate the contract** in one sentence.
2. **Trace the smallest failing case** — the one the prompt shows
   failing (its examples ARE the failing tests).
3. **Find the FIRST statement** where the state table diverges from
   what the contract needs. Everything before that statement is
   correct — do not touch it.
4. **The fix is usually one token**: a comparison operator, an
   initialization value, a loop bound, a missing `this.`, an argument
   in the wrong slot. If your fix rewrites half the method, you
   mislocated the error.

Why "first" matters: a later correct-looking line that misbehaves is
usually a *victim* of the earlier bug, not the bug. Fixing victims
adds bugs; fixing the source collapses the cascade.

Worked micro-example — contract: "sum of even elements":

```java
int total = 0;
for (int i = 0; i <= arr.length; i++) {   // victim: throws at the end
    if (arr[i] % 2 == 0) { total += arr[i]; }
}
```

The exception at the LAST iteration tempts you to "fix the array".
The first divergence is the `<=` bound itself. One token: `<`.
"""

L2 = r"""
**Cascading errors** — the reason a wrong early line ruins everything
after: state flows forward. Trace `{2, 3, 4}` for a "running maximum
then final minus count" style spec with a planted seed bug:

```java
// CONTRACT: return (max value) - (count of negatives)
int max = 0;                 // BUG when all values < 0... or here:
int negs = 0;
for (int i = 0; i < arr.length; i++) {
    if (arr[i] > max) { max = arr[i]; }
    if (arr[i] < 0) { negs++; }   // second bug: counts AFTER max? no —
}
return max - negs;
```

with `{5, -2, 8}`: max walks 5→8 correctly, negs = 1, return 7. With
`{-5, -2}`: max stays 0 (wrong — should be −2), negs = 2, return −2.
The trace shows BOTH bugs but the exam asks for the FIRST divergence
in the failing example. For `{-5, -2}`, the first divergence is the
seed `max = 0` — the `negs` line runs correctly for its own contract.

Two bugs can also *mask* each other: a doubled counter and a halved
base can produce right answers on one test and wrong on the next.
This is why the clinic always traces at least TWO examples before
declaring the fix.

**Minimal-repair ethics** (and exam scoring): rubrics are behavior
lists; an untouched correct behavior keeps its points. Rewriting
working sections risks moving errors into previously-earned behavior.
"""

L3 = r"""
The salvage protocol — for the exam moment when a part is beyond you:

1. **Bank the skeleton.** Write the signature, the guard for the edge
   cases you DO understand (empty, absent), and the loop shell with a
   comment where the hard logic goes. Behavior-level rubric rows
   reward: "iterates over all elements", "correctly returns for the
   empty case", "returns the right type".
2. **Write the adjacent easy part.** Multi-part questions are
   independent at the rubric level: part (b) does not lose points
   because (a) is blank — unless (b) explicitly consumes (a), in which
   case write (a)'s INTENDED call anyway with a comment; graders
   award (b)'s own logic when it is right "given (a)".
3. **Never panic-erase.** A half-written method scores its partial
   behaviors; a blank scores zero. The rubric cannot see intentions,
   only code — so put code on the page, even uncertain code.
4. **Time-box the rescue.** 5 minutes of stuck = bank the skeleton,
   move on, return if time remains. A fresh look after two other
   questions solves what 15 staring minutes could not.

Practicing salvage: the debug challenges in this lab give you broken
code whose *contracts* are fully specified — exactly the exam
situation. Run the localization loop, repair minimally, and keep the
passing tests passing.
"""

write_module(
    M,
    "FRQ Debugging & Partial Credit",
    "First-error localization, cascading-error discipline, and the salvage protocol for banking partial credit.",
    "Gỡ lỗi FRQ & điểm một phần",
    "Định vị lỗi-đầu-tiên, kỷ luật lỗi-đổ-domino, và sách lược cứu-vớt để giữ điểm một phần.",
    lessons=["cx-m18-localize", "cx-m18-cascade", "cx-m18-salvage", "cx-cp-m18"],
    practices=["cx-p18-frqdebug"],
)

write_lesson(
    M, "cx-m18-localize", "First-error localization",
    "Restate, trace the failing case, fix the first divergence only.",
    12, L1,
    "Định vị lỗi đầu tiên",
    "Phát biểu lại hợp đồng, truy vết trường-hợp-gãy, chỉ sửa điểm-lệch-đầu-tiên.",
    r"""
Đề thi không hỏi "mã này đúng chưa?" — nó hỏi "thay đổi nào làm nó
đúng?" và chấm phần chẩn đoán. Vòng định vị:

1. **Phát biểu lại hợp đồng** trong một câu.
2. **Truy vết trường-hợp-gãy nhỏ nhất** — cái mà đề cho thấy là gãy
   (các ví dụ của đề CHÍNH LÀ các test bị gãy).
3. **Tìm câu lệnh ĐẦU TIÊN** nơi bảng trạng thái lệch khỏi điều hợp
   đồng cần. Mọi thứ trước câu lệnh đó đều đúng — đừng chạm vào.
4. **Bản sửa thường chỉ một token**: một toán tử so sánh, một giá trị
   khởi tạo, một biên vòng lặp, một `this.` bị thiếu, một đối số nằm
   sai khe. Nếu bản sửa của bạn viết lại nửa phương thức, bạn đã định
   vị sai lỗi.

Vì sao chữ "đầu tiên" quan trọng: một dòng sau trông-đúng-nhưng-hành-xử-sai
thường là *nạn nhân* của lỗi trước đó, không phải bản thân lỗi. Sửa nạn
nhân làm sinh thêm lỗi; sửa nguồn làm sập cả cơn đổ domino.

Ví-dụ-vi-mô — hợp đồng: "tổng các phần tử chẵn":

```java
int total = 0;
for (int i = 0; i <= arr.length; i++) {   // nạn nhân: ném ở bước cuối
    if (arr[i] % 2 == 0) { total += arr[i]; }
}
```

Ngoại lệ ở lần-lặp-CUỐI khiến bạn ttempt "sửa cái mảng". Điểm lệch đầu
tiên là chính biên `<=`. Một token: `<`.
""",
)

write_lesson(
    M, "cx-m18-cascade", "Cascading errors",
    "State flows forward: fix the source, not the victims; trace two examples.",
    12, L2,
    "Lỗi đổ domino",
    "Trạng thái chảy về phía trước: sửa nguồn, không sửa nạn nhân; truy vết hai ví dụ.",
    r"""
**Lỗi đổ domino** — lý do một dòng-sai-sớm phá hỏng mọi thứ phía sau:
trạng thái chảy theo hướng đi tới. Truy vết `{2, 3, 4}` cho một dạng
đặc-tả "maximum-chạy-rồi-trừ-số-đếm" với hạt giống bị cài:

```java
// HỢP ĐỒNG: trả về (giá trị max) - (số phần tử âm)
int max = 0;                 // BUG khi mọi giá trị < 0
int negs = 0;
for (int i = 0; i < arr.length; i++) {
    if (arr[i] > max) { max = arr[i]; }
    if (arr[i] < 0) { negs++; }
}
return max - negs;
```

Với `{5, -2, 8}`: max đi 5→8 đúng, negs = 1, trả về 7. Với `{-5, -2}`:
max dừng ở 0 (sai — đáng lẽ −2), negs = 2, trả về −2. Phép truy vết cho
thấy CẢ HAI lỗi nhưng đề hỏi điểm-lệch-ĐẦU-TIÊN trong ví dụ gãy. Với
`{-5, -2}`, điểm lệch đầu tiên là hạt giống `max = 0` — dòng `negs`
chạy đúng với hợp đồng riêng của nó.

Hai lỗi cũng có thể *che khuất* nhau: một bộ đếm bị nhân đôi và một
hạt giống bị chia nửa có thể cho đáp án đúng trên một test và sai trên
test kế. Vì vậy phòng sửa lỗi luôn truy vết ÍT NHẤT HAI ví dụ trước khi
tuyên bố bản sửa.

**Đạo đức sửa-tối-thiểu** (và cách chấm): bảng chấm là danh sách hành
vi; một hành vi đúng chưa-bị-động-to giữ nguyên điểm của nó. Viết lại
các phần đang chạy có nguy cơ dời lỗi vào những hành vi trước đó đã
kiếm được điểm.
""",
)

write_lesson(
    M, "cx-m18-salvage", "The salvage protocol",
    "Bank the skeleton, write the adjacent part, never panic-erase, time-box.",
    12, L3,
    "Sách lược cứu vớt",
    "Gửi-gửi-kho bộ xương, viết phần liền kề, không bao giờ xóa theo hoảng loạn, giới hạn thời gian.",
    r"""
Sách lược cứu-vớt — cho khoảnh khắc thi khi một phần vượt quá bạn:

1. **Gửi kho bộ xương.** Viết chữ ký, lớp chặn cho các biên bạn HIỂU
   (rỗng, vắng mặt), và bộ xương vòng lặp kèm chú thích chỗ logic khó.
   Các dòng bảng-chấm-mức-hành-vi thưởng cho: "duyệt qua mọi phần tử",
   "trả về đúng cho trường hợp rỗng", "trả về đúng kiểu".
2. **Viết phần dễ liền kề.** Các câu đa phần độc lập nhau ở mức bảng
   chấm: phần (b) không mất điểm vì (a) trắng — trừ khi (b) tường minh
   tiêu thụ (a); khi đó hãy viết LỜI GỌI như ý của (a) kèm chú thích;
   người chấm thưởng logic của (b) khi nó đúng "khi có (a)".
3. **Không bao giờ xóa theo hoảng loạn.** Một phương thức viết dở ghi
   được các hành vi một-phần của nó; một trang trắng ghi điểm không.
   Bảng chấm không nhìn thấy ý định, chỉ thấy mã — vì vậy hãy đặt mã
   lên trang, kể cả mã chưa chắc chắn.
4. **Giới-hạn-thời-gian cho việc cứu.** 5 phút bí = gửi kho bộ xương,
   chuyển câu, quay lại nếu còn giờ. Một cái nhìn mới sau hai câu khác
   giải được thứ mười lăm phút chằm căng không giải nổi.

Luyện cứu-vớt: các bài debug trong phòng này đưa mã gãy với *hợp đồng*
được đặc tả đầy đủ — đúng tình huống đề thi. Chạy vòng định vị, sửa tối
thiểu, và giữ các test đang-pass-còn-pass.
""",
)

BOILER_MEDIAN = r"""public class Solution {
    // CONTRACT: median of a sorted arr (length >= 1). Odd: middle.
    // Even: average of the two middle values as a double.
    // BUG: wrong case split — diagnose and repair minimally.
    public static double median(int[] arr) {
        int mid = arr.length / 2;
        if (arr.length % 2 == 0) {
            return arr[mid];
        }
        return (arr[mid - 1] + arr[mid]) / 2;
    }
}
"""

BOILER_LASTHALF = r"""public class Solution {
    // CONTRACT: return a NEW array holding the SECOND half of arr
    // (length >= 1); for odd lengths the extra element belongs to the
    // FIRST half. BUG: off-by-one in the copy bounds.
    public static int[] secondHalf(int[] arr) {
        int half = arr.length / 2;
        int[] out = new int[half];
        for (int i = 0; i <= half; i++) {
            out[i] = arr[half + i];
        }
        return out;
    }
}
"""

BOILER_THREEBUGS = r"""public class Solution {
    // CONTRACT: counts how many values in arr are BOTH positive AND
    // greater than the average. arr.length >= 1.
    // DIAGNOSE: one planted bug. Trace {1, 3, 4} (avg 8/3) by hand.
    public static int aboveAvgPos(int[] arr) {
        int sum = 0;
        for (int v : arr) {
            sum += v;
        }
        double avg = sum / arr.length;
        int count = 0;
        for (int v : arr) {
            if (v > 0 || v > avg) {
                count++;
            }
        }
        return count;
    }
}
"""

BOILER_SALVAGE = r"""import java.util.ArrayList;

public class Solution {
    // CONTRACT: returns the LONGEST word in words (earliest on ties),
    // or "" when the list is empty. The provided draft has the right
    // skeleton but the loop never updates best. REPAIR it.
    public static String longestWord(ArrayList<String> words) {
        String best = "";
        for (String w : words) {
            // TODO update best here
        }
        return best;
    }
}
"""

BOILER_SWAPPEDARGS = r"""public class Solution {
    // CONTRACT: draw a bar of `n` copies of ch followed by a newline:
    // draw(3, '*') prints "***\n". The arguments are swapped at the
    // call site inside render(). Fix ONLY the call.
    public static String bar(int n, char ch) {
        String out = "";
        for (int i = 0; i < n; i++) {
            out += ch;
        }
        return out + "\n";
    }

    public static String render(int n, char ch) {
        String page = bar(ch, n);
        return page;
    }
}
"""

BOILER_CP18 = r"""public class Solution {
    // TWO BUGS, ONE METHOD. CONTRACT: returns the second-largest
    // DISTINCT value; -1 when fewer than 2 distinct values.
    // Trace {5, 3, 5} (answer 3) and {7} (answer -1) by hand first.
    public static int secondMax(int[] arr) {
        int max = 0;
        int second = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            } else {
                second = arr[i];
            }
        }
        if (max == second) {
            return -1;
        }
        return second;
    }
}
"""

P_MEDIAN = challenge(
    "cx-m18-fix-median",
    "Repair the case split",
    "`median` swaps its parity branches. Trace {1, 3, 8} (odd → 3.0) and {1, 2, 3, 10} (even → 2.5) against the code, find the first divergence, and swap the branches — nothing else.",
    BOILER_MEDIAN,
    [(
        "median repaired",
        r"""
CjTestBase.checkNear(Solution.median(new int[]{1, 3, 8}), 3.0, 1e-9, "odd middle");
CjTestBase.checkNear(Solution.median(new int[]{1, 2, 3, 10}), 2.5, 1e-9, "even average");
CjTestBase.checkNear(Solution.median(new int[]{7}), 7.0, 1e-9, "single element");
""",
        "Odd: return arr[mid]. Even: (arr[mid-1] + arr[mid]) / 2.0.",
    )],
    level="debugging",
)

P_LASTHALF = challenge(
    "cx-m18-fix-second-half",
    "Repair the copy bounds",
    "`secondHalf` throws on every input. Diagnose the bound error AND the size error (both off-by-one), fix both, verify {1,2,3} → {3} and {1,2,3,4} → {3,4}.",
    BOILER_LASTHALF,
    [(
        "half copied",
        r"""
CjTestBase.checkEq(Solution.secondHalf(new int[]{1, 2, 3}), new int[]{2}, "odd: extra element in first half");
CjTestBase.checkEq(Solution.secondHalf(new int[]{1, 2, 3, 4}), new int[]{3, 4}, "even split");
CjTestBase.checkEq(Solution.secondHalf(new int[]{9}), new int[]{}, "single -> empty half");
""",
        "half = arr.length / 2; out = new int[half]; copy i in 0..half-1 from arr[half + i]. E.g. {1,2,3} -> {2}.",
    )],
    level="debugging",
)

P_ABOVEAVG = challenge(
    "cx-m18-fix-above-avg",
    "One planted bug",
    "`aboveAvgPos` has exactly one bug. Trace {1, 3, 4}: avg = 8/3 ≈ 2.67; qualifying = 3 and 4 → 2. The current code returns more. Find the divergent operator and repair it.",
    BOILER_THREEBUGS,
    [(
        "count repaired",
        r"""
CjTestBase.checkEq(Solution.aboveAvgPos(new int[]{1, 3, 4}), 2, "3 and 4 qualify");
CjTestBase.checkEq(Solution.aboveAvgPos(new int[]{-1, -2}), 0, "negatives never qualify");
CjTestBase.checkEq(Solution.aboveAvgPos(new int[]{5}), 0, "5 is not > 5");
""",
        "The condition must be AND: v > 0 && v > avg. (Also note the int-division avg is fine for the trace shown.)",
    )],
    level="debugging",
)

P_SALVAGE = challenge(
    "cx-m18-fix-longest-word",
    "Finish the skeleton",
    "The draft has signature, seed, loop, and return — but best never updates. Complete ONLY the loop body. This is salvage: the structure was already banked.",
    BOILER_SALVAGE,
    [(
        "longest found",
        r"""
ArrayList<String> words = new ArrayList<String>();
words.add("ab");
words.add("cccc");
words.add("ddd");
CjTestBase.checkEq(Solution.longestWord(words), "cccc", "strictly longest");
ArrayList<String> tie = new ArrayList<String>();
tie.add("aa");
tie.add("bb");
CjTestBase.checkEq(Solution.longestWord(tie), "aa", "earliest tie");
CjTestBase.checkEq(Solution.longestWord(new ArrayList<String>()), "", "empty list");
""",
        "if (w.length() > best.length()) { best = w; }",
    )],
    level="debugging",
)

P_SWAPPEDARGS = challenge(
    "cx-m18-fix-arg-order",
    "Fix the swapped call",
    "`bar` is correct; `render`'s call passes the arguments in the wrong order. The divergence shows up as a compile error — fix the call site only.",
    BOILER_SWAPPEDARGS,
    [(
        "call repaired",
        r"""
CjTestBase.checkEq(Solution.render(3, '*'), "***\n", "three stars, newline");
CjTestBase.checkEq(Solution.render(1, '-'), "-\n", "one dash");
""",
        "bar(ch, n) must be bar(n, ch).",
    )],
    level="debugging",
)

CP18 = challenge(
    "cx-cp-m18-second-max",
    "Checkpoint: two bugs",
    "`secondMax` needs two repairs: the tracking logic (the else branch is wrong) and the distinctness report. Trace {5, 3, 5} and {7} and {2, 2} by hand, locate the first divergences, and repair both.",
    BOILER_CP18,
    [(
        "second max repaired",
        r"""
CjTestBase.checkEq(Solution.secondMax(new int[]{5, 3, 5}), 3, "distinct second");
CjTestBase.checkEq(Solution.secondMax(new int[]{7}), -1, "fewer than 2");
CjTestBase.checkEq(Solution.secondMax(new int[]{2, 2}), -1, "only one distinct value");
CjTestBase.checkEq(Solution.secondMax(new int[]{1, 9, 4}), 4, "9 then 4");
""",
        "Track max and second properly: if (v > max) { second = max; max = v; } else if (v < max && v > second) { second = v; }; report -1 when second was never set (sentinel 0 fails for arrays of negatives — use a boolean or Integer).",
    )],
    level="debugging",
)

write_practice(
    M, "cx-p18-frqdebug", "FRQ debug lab",
    "Case-split swaps, bound repairs, one-bug hunts, skeleton completion, call fixes.",
    "Phòng debug FRQ",
    "Đảo nhánh, sửa biên, săn một lỗi, hoàn thiện bộ xương, sửa lời gọi.",
    after_lesson="cx-m18-cascade", minutes=60, difficulty="advanced",
    challenges=[P_MEDIAN, P_LASTHALF, P_ABOVEAVG, P_SALVAGE, P_SWAPPEDARGS],
    vi_challenges={
        "cx-m18-fix-median": vi_challenge("Sửa tách trường hợp",
            "`median` hoán đổi hai nhánh chẵn/lẻ. Truy vết {1, 3, 8} (lẻ → 3.0) và {1, 2, 3, 10} (chẵn → 2.5) đối chiếu mã, tìm điểm lệch đầu tiên, và hoán đổi hai nhánh — không gì khác.",
            [("median repaired", "Lẻ: return arr[mid]. Chẵn: (arr[mid-1] + arr[mid]) / 2.0.")]),
        "cx-m18-fix-second-half": vi_challenge("Sửa biên sao chép",
            "`secondHalf` ném ngoại lệ với mọi đầu vào. Chẩn đoán lỗi biên VÀ lỗi kích thước (cùng lệch-một), sửa cả hai, kiểm chứng {1,2,3} → {3} và {1,2,3,4} → {3,4}.",
            [("half copied", "half = arr.length / 2; out = new int[half]; sao chép i trong 0..half-1 từ arr[half + i].")]),
        "cx-m18-fix-above-avg": vi_challenge("Săn một lỗi được cài",
            "`aboveAvgPos` có đúng một lỗi. Truy vết {1, 3, 4}: avg = 8/3 ≈ 2,67; đạt chuẩn = 3 và 4 → 2. Mã hiện tại trả về nhiều hơn. Tìm toán tử lệch và sửa.",
            [("count repaired", "Điều kiện phải là VÀ: v > 0 && v > avg.")]),
        "cx-m18-fix-longest-word": vi_challenge("Hoàn thiện bộ xương",
            "Bản nháp có chữ ký, seed, vòng lặp, return — nhưng best chưa bao giờ được cập nhật. Chỉ hoàn thiện THÂN vòng lặp. Đây là cứu vớt: cấu trúc đã được gửi kho.",
            [("longest found", "if (w.length() > best.length()) { best = w; }")]),
        "cx-m18-fix-arg-order": vi_challenge("Sửa lời gọi bị tráo đối số",
            "`bar` đúng; lời gọi trong `render` truyền đối số sai thứ tự. Điểm lệch hiện ra dưới dạng lỗi biên dịch — chỉ sửa lời gọi.",
            [("call repaired", "bar(ch, n) phải là bar(n, ch).")]),
    },
    solutions=[
        ("cx-m18-fix-median",
         BOILER_MEDIAN.replace("        if (arr.length % 2 == 0) {\n            return arr[mid];\n        }\n        return (arr[mid - 1] + arr[mid]) / 2;",
            "        if (arr.length % 2 == 1) {\n            return arr[mid];\n        }\n        return (arr[mid - 1] + arr[mid]) / 2.0;"),
         BOILER_MEDIAN.replace("        if (arr.length % 2 == 0) {\n            return arr[mid];\n        }\n        return (arr[mid - 1] + arr[mid]) / 2;",
            "        if (arr.length % 2 == 0) {\n            return arr[mid + 1];\n        }\n        return (arr[mid - 1] + arr[mid]) / 2;")),
        ("cx-m18-fix-second-half",
         r"""public class Solution {
    public static int[] secondHalf(int[] arr) {
        int half = arr.length / 2;
        int[] out = new int[half];
        for (int i = 0; i < half; i++) {
            out[i] = arr[half + i];
        }
        return out;
    }
}
""",
         r"""public class Solution {
    public static int[] secondHalf(int[] arr) {
        int half = arr.length / 2;
        int[] out = new int[half];
        for (int i = 0; i < half; i++) {
            out[i] = arr[half + i + 1];
        }
        return out;
    }
}
"""),
        ("cx-m18-fix-above-avg", BOILER_THREEBUGS.replace("if (v > 0 || v > avg) {", "if (v > 0 && v > avg) {"),
         BOILER_THREEBUGS),
        ("cx-m18-fix-longest-word", BOILER_SALVAGE.replace("            // TODO update best here",
            "            if (w.length() > best.length()) {\n                best = w;\n            }"),
         BOILER_SALVAGE),
        ("cx-m18-fix-arg-order", BOILER_SWAPPEDARGS.replace("String page = bar(ch, n);", "String page = bar(n, ch);"),
         BOILER_SWAPPEDARGS),
    ],
)

write_checkpoint(
    M, "cx-cp-m18", "Checkpoint: two bugs, one method",
    "Full localization loop on secondMax — tracking logic plus the distinctness report.",
    30,
    r"""
secondMax teaches the deepest lesson of the module: the original else
branch silently records the LAST smaller value, not the second LARGEST
— a semantic error invisible to a single test. And the -1 report via
`max == second` breaks for negatives (try {-1, -2}: max stays 0!). The
repair needs a proper two-slot tracker and a boolean 'was there a
second?' — exactly the kind of redesign the exam asks you to diagnose,
not just the one-token fixes.
""",
    "Điểm kiểm tra: hai lỗi, một phương thức",
    "Vòng định vị đầy đủ trên secondMax — logic theo dõi cộng báo-cáo-phân-biệt.",
    r"""
secondMax dạy bài học sâu nhất của module: nhánh else gốc lặng lẽ ghi
giá-trị-nhỏ-hơn-CUỐI, không phải giá trị lớn-thứ-hai — một lỗi ngữ nghĩa
vô hình với một test duy nhất. Và báo cáo -1 qua `max == second` gãy với
số âm (thử {-1, -2}: max dừng ở 0!). Bản sửa cần một bộ theo dõi hai-khe
đúng cách và một boolean 'đã có thứ-hai chưa?' — đúng kiểu tái-thiết-kế
mà đề thi yêu cầu bạn chẩn đoán, không chỉ những bản sửa-một-token.
""",
    CP18,
    vi_challenge("Điểm kiểm tra: hai lỗi, một phương thức",
        "`secondMax` cần hai bản sửa: logic theo dõi (nhánh else sai) và báo cáo tính phân biệt. Truy vết {5, 3, 5}, {7}, và {2, 2} bằng tay, định vị các điểm lệch đầu tiên, và sửa cả hai.",
        [("second max repaired", "Theo dõi max và second đúng cách: if (v > max) { second = max; max = v; } else if (v < max && v > second) { second = v; }; báo -1 khi second chưa từng được đặt (dùng boolean).")]),
    solution=r"""public class Solution {
    public static int secondMax(int[] arr) {
        int max = Integer.MIN_VALUE;
        int second = Integer.MIN_VALUE;
        boolean hasSecond = false;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > max) {
                second = max;
                hasSecond = hasSecond || max != Integer.MIN_VALUE;
                max = arr[i];
            } else if (arr[i] < max && arr[i] > second) {
                second = arr[i];
                hasSecond = true;
            }
        }
        if (!hasSecond) {
            return -1;
        }
        return second;
    }
}
""",
    wrong=r"""public class Solution {
    public static int secondMax(int[] arr) {
        int max = Integer.MIN_VALUE;
        int second = Integer.MIN_VALUE;
        boolean hasSecond = false;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > max) {
                second = max;
                hasSecond = hasSecond || max != Integer.MIN_VALUE;
                max = arr[i];
            } else if (arr[i] <= max && arr[i] > second) {
                second = arr[i];
                hasSecond = true;
            }
        }
        if (!hasSecond) {
            return -1;
        }
        return second;
    }
}
""",
)
