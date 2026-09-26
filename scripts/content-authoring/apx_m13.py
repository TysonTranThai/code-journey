#!/usr/bin/env python3
"""AP CSA Advanced M13 — FRQ method mastery (verified method-writing tasks)."""
from apx import *

M = "apx-frq-method"

write_module(
    M,
    "FRQ Method Mastery",
    "Five hard method-writing tasks: tricky specs, tie-breaks, adjacent-pair scans, recursion, and sentinel guards. Difficulty E3–E5.",
    "Làm chủ phương thức FRQ",
    "Năm bài viết phương thức khó: đặc tả đỏi, luật phá hòa, quét cặp liền kề, đệ quy, và biến chặn sentinel. Độ khó E3–E5.",
    lessons=["apx-m13-spec", "apx-m13-edge", "apx-m13-mixed", "apx-cp-m13"],
    practices=["apx-p13-method"],
)

L1 = r"""
The hardest single-method FRQs fail students on **one clause**, not
on the algorithm. The clause types, in order of appearance on real
exams:

- **Tie-break clauses**: "on a tie, return the one appearing
  FIRST/SMALLEST." Your loop's comparison must implement the
  tie-break exactly — `>` keeps the first-seen; `>=` keeps the last.
- **Strictness clauses**: "more than," "at least," "strictly
  between." Each maps to an operator; underline them.
- **Sentinel clauses**: "return -1/0.0/999 if none." A sentinel
  forces a two-variable scan (the candidate and a found-flag) or an
  early return — one accumulator cannot serve both jobs.
- **Format clauses**: "adjacent duplicates are replaced by a star"
  — output-shaping specs where the boundary iteration (start at
  index 1, compare backward) is the entire difficulty.

Read the spec once for the story, then a second time circling every
operator-deciding word. Those circles are the rubric.
"""

L2 = r"""
**Edge cases by type.** Each data type owns a canonical edge set:

- **String**: empty, single char, all-same, alternating. Adjacent
  scans start at i = 1 and compare `charAt(i)` to `charAt(i - 1)`.
- **Array**: empty, one element, all-equal (tie-break territory),
  negatives (initialization must survive: use `arr[0]` or
  MIN_VALUE, never 0).
- **ArrayList**: empty, removals while scanning (iterate backward
  or build anew), `.equals` for objects — `==` on Integer beyond
  the small cache is a latent bug.
- **Recursion**: zero, one digit/element, and the shape of the
  smallest input that still recurses once.

The habit that earns the edge-case rubric line: after coding, RUN
your plan against the empty input and the single element *before*
the example in the prompt. The example is seductive; edges are
where the hidden tests live.
"""

L3 = r"""
**From spec to skeleton.** A method that reads like the spec is
fast to write and hard to get wrong. Worked example — "second
smallest, -1 if it doesn't exist":

```java
// pass 1: find min
// pass 2: find min among values strictly greater than min
// if pass 2 finds nothing: -1
```

Two passes, each trivially correct, and the -1 falls out of pass 2
naturally. The one-pass version (tracking first and second
simultaneously) is twice the branches and the favorite source of
off-by-one ties. **When the spec has a tie-break, prefer the
two-pass form** — the tie-break becomes one comparison instead of
three.

For recursion tasks, write the two lines first: the base case and
the recursive step with its progress. Then everything else is
glue.
"""

VI_L1 = r"""
Những FRQ một phương thức khó nhất làm học sinh trượt trên **một
mệnh đề**, không phải trên thuật toán. Các loại mệnh đề, theo thứ tự
xuất hiện trong đề thật:

- **Mệnh đề phá hòa**: "khi hòa, trả về cái xuất hiện
  TRƯỚC/NHỎ NHẤT." Phép so sánh trong vòng lặp phải hiện thực hóa
  đúng luật phá hòa — `>` giữ cái thấy trước; `>=` giữ cái thấy sau.
- **Mệnh đề nghiêm ngặt**: "nhiều hơn," "ít nhất," "nghiêm ngặt giữa."
  Mỗi cái ánh xạ một toán tử; gạch chân chúng.
- **Mệnh đề sentinel**: "trả -1/0.0/999 nếu không có." Sentinel ép
  quét hai biến (ứng viên và cờ-tìm-thấy) hoặc trả sớm — một bộ tích
  lũy không thể làm cả hai việc.
- **Mệnh đề định dạng**: "bản sao liền kề được thay bằng dấu sao" —
  đặc tả định-hình-kết-quả nơi vòng lặp biên (bắt đầu tại chỉ số 1,
  so sánh ngược) là toàn bộ độ khó.

Đọc đặc tả một lần cho câu chuyện, rồi lần hai khoanh tròn mọi từ
quyết định toán tử. Các vòng tròn đó là bảng điểm.
"""

VI_L2 = r"""
**Trường hợp biên theo kiểu dữ liệu.** Mỗi kiểu dữ liệu sở hữu một
bộ biên kinh điển:

- **String**: rỗng, một ký tự, toàn-giống-nhau, xen kẽ. Quét liền kề
  bắt đầu tại i = 1 và so `charAt(i)` với `charAt(i - 1)`.
- **Array**: rỗng, một phần tử, toàn-bằng-nhau (vùng phá hòa), số âm
  (khởi tạo phải sống sót: dùng `arr[0]` hoặc MIN_VALUE, không bao
  giờ 0).
- **ArrayList**: rỗng, xóa khi đang quét (duyệt ngược hoặc dựng mới),
  `.equals` cho đối tượng — `==` trên Integer ngoài vùng cache nhỏ là
  lỗi ngầm.
- **Đệ quy**: số 0, một chữ số/phần tử, và hình dạng của đầu vào nhỏ
  nhất mà vẫn đệ quy đúng một lần.

Thói quen giành được dòng bảng-điểm biên: sau khi viết mã, chạy kế
hoạch của bạn qua đầu vào rỗng và một phần tử *trước* ví dụ trong đề.
Ví dụ thì quyến rũ; các biên là nơi test ẩn sống.
"""

VI_L3 = r"""
**Từ đặc tả đến khung.** Một phương thức đọc giống đặc tả thì viết
nhanh và khó sai. Ví dụ mẫu — "giá trị nhỏ thứ hai, -1 nếu không tồn
tại":

```java
// lượt 1: tìm min
// lượt 2: tìm min trong các giá trị nghiêm ngặt lớn hơn min
// nếu lượt 2 không tìm thấy: -1
```

Hai lượt, mỗi lượt đúng một cách tầm thường, và -1 rơi ra tự nhiên từ
lượt 2. Bản một lượt (theo dõi first và second đồng thời) có gấp đôi
số nhánh và là nguồn lỗi phá-hòa ưa thích. **Khi đặc tả có luật phá
hòa, ưu tiên dạng hai lượt** — luật phá hòa thành một phép so sánh
thay vì ba.

Với bài đệ quy, viết hai dòng trước: trường hợp cơ sở và bước đệ quy
kèm tiến triển của nó. Mọi thứ khác chỉ là keo dán.
"""

BOILER_STR = r"""public class Solution {
    public static String process(String s) {
        return ""; // replace
    }
}
"""

BOILER_CHAR = r"""public class Solution {
    public static char process(String s) {
        return ' '; // replace
    }
}
"""

BOILER_INT = r"""public class Solution {
    public static int process(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_DIGIT = r"""public class Solution {
    public static int process(int n) {
        return 0; // replace
    }
}
"""

BOILER_LIST = r"""public class Solution {
    public static int process(java.util.ArrayList<Integer> list) {
        return 0; // replace
    }
}
"""

P_FREQ = challenge(
    "apx-m13-frequent",
    "Most frequent character (with a tie-break)",
    "Return the **most frequent character** in the string; on a tie, "
    "return the alphabetically **smallest** of the tied characters. "
    "The string is non-empty and lowercase.\n\nExamples: "
    "`\"aabbbc\"` → `'b'`; `\"abab\"` → `'a'` (a and b tie, a wins).",
    BOILER_CHAR,
    [(
        "frequent char",
        r"""
CjTestBase.checkEq(Solution.process("aabbbc"), 'b', "clear winner");
CjTestBase.checkEq(Solution.process("abab"), 'a', "tie -> smallest");
CjTestBase.checkEq(Solution.process("z"), 'z', "single char");
""",
        "Count each char's occurrences; replace only on strictly-greater count, or equal count with a smaller char.",
    )],
    level="independent",
    difficulty="advanced",
)

P_STAR = challenge(
    "apx-m13-star",
    "Adjacent-duplicate star insertion",
    "Between every pair of **adjacent equal characters**, insert "
    "`'*'` (the characters themselves stay).\n\nExamples: "
    "`\"aabb\"` → `\"a*ab*b\"`; `\"abc\"` → `\"abc\"`; `\"\"` → "
    "`\"\"`.",
    BOILER_STR,
    [(
        "star-inserted output",
        r"""
CjTestBase.checkEq(Solution.process("aabb"), "a*ab*b", "two pairs");
CjTestBase.checkEq(Solution.process("abc"), "abc", "no pairs");
CjTestBase.checkEq(Solution.process(""), "", "empty");
CjTestBase.checkEq(Solution.process("aa"), "a*a", "one pair");
""",
        "Seed the output with charAt(0); from i = 1, append '*' before the char when it equals the previous one.",
    )],
    level="combination",
    difficulty="advanced",
)

P_SECOND = challenge(
    "apx-m13-secondsmallest",
    "Second distinct smallest (with a sentinel)",
    "Return the **second distinct smallest** value; return -1 when it "
    "does not exist (empty, one element, or all values equal).\n\n"
    "Examples: `{4,1,4,2}` → `2`; `{5,5}` → `-1`; `{-1,-1,3}` → `3`.",
    BOILER_INT,
    [(
        "second smallest",
        r"""
CjTestBase.checkEq(Solution.process(new int[]{4, 1, 4, 2}), 2, "distinct second");
CjTestBase.checkEq(Solution.process(new int[]{5, 5}), -1, "no distinct second");
CjTestBase.checkEq(Solution.process(new int[]{-1, -1, 3}), 3, "negatives fine");
CjTestBase.checkEq(Solution.process(new int[]{}), -1, "empty");
""",
        "Two passes: find min, then min among values strictly greater than it; -1 if none.",
    )],
    level="independent",
    difficulty="advanced",
)

P_EVEN = challenge(
    "apx-m13-evendigits",
    "Sum of even digits (recursive)",
    "Recursively sum the **even digits** of a non-negative number "
    "(contribute 0 for odd digits). No loops.\n\nExamples: 2468 → "
    "`20`; 135 → `0`; 0 → `0`.",
    BOILER_DIGIT,
    [(
        "even digit sum",
        r"""
CjTestBase.checkEq(Solution.process(2468), 20, "all even");
CjTestBase.checkEq(Solution.process(135), 0, "all odd");
CjTestBase.checkEq(Solution.process(0), 0, "zero");
""",
        "Base n == 0 returns 0; step: (d even ? d : 0) + recurse(n / 10).",
    )],
    level="guided",
    difficulty="intermediate",
)

P_REPEAT = challenge(
    "apx-m13-repeats",
    "Count adjacent repeats in a list",
    "Count the positions i (from the second element on) where the "
    "element **equals its predecessor**. Use `.equals` — these are "
    "Integer objects.\n\nExample: `[1,1,2,2,2,3]` → `3`.",
    BOILER_LIST,
    [(
        "adjacent repeat count",
        r"""
java.util.ArrayList<Integer> l = new java.util.ArrayList<>(java.util.List.of(1, 1, 2, 2, 2, 3));
CjTestBase.checkEq(Solution.process(l), 3, "three adjacent pairs");
java.util.ArrayList<Integer> big = new java.util.ArrayList<>(java.util.List.of(200, 200, 5));
CjTestBase.checkEq(Solution.process(big), 1, "values beyond the Integer cache");
CjTestBase.checkEq(Solution.process(new java.util.ArrayList<>()), 0, "empty");
CjTestBase.checkEq(Solution.process(new java.util.ArrayList<>(java.util.List.of(7))), 0, "single");
""",
        "Loop from i = 1; list.get(i).equals(list.get(i - 1)) — never == on objects.",
    )],
    level="imitation",
    difficulty="intermediate",
)

CP13 = challenge(
    "apx-cp-m13-sandwich",
    "Checkpoint: the sandwich count",
    "A 'sandwich' is three consecutive elements where the first and "
    "third are equal but the middle differs (like `1,9,1`). Count the "
    "sandwiches in the array (overlapping counts: `1,9,1,9,1` "
    "contains three).\n\nImplement `process(int[] arr)` (0 for fewer "
    "than three elements).",
    BOILER_INT,
    [(
        "sandwich count",
        r"""
CjTestBase.checkEq(Solution.process(new int[]{1, 9, 1, 9, 1}), 3, "three overlapping sandwiches");
CjTestBase.checkEq(Solution.process(new int[]{1, 2, 3}), 0, "no sandwich");
CjTestBase.checkEq(Solution.process(new int[]{5, 5, 5}), 0, "equal thirds need a different middle");
CjTestBase.checkEq(Solution.process(new int[]{}), 0, "empty");
""",
        "Loop i from 1 to length-2: arr[i-1] == arr[i+1] && arr[i] != arr[i-1].",
    )],
    level="combination",
    difficulty="advanced",
)

VI_CP13 = vi_challenge(
    "Điểm kiểm tra: đếm bánh kẹp",
    "Một 'bánh kẹp' là ba phần tử liên tiếp trong đó phần tử đầu và ba "
    "bằng nhau nhưng ở giữa khác (như `1,9,1`). Đếm số bánh kẹp trong "
    "mảng (các bản chồng nhau vẫn đếm: `1,9,1,9,1` chứa ba).\n\n"
    "Cài đặt `process(int[] arr)` (0 cho ít hơn ba phần tử).",
    [("sandwich count", "Vòng lặp i từ 1 đến độ dài-2: arr[i-1] == arr[i+1] && arr[i] != arr[i-1].")],
)

write_practice(
    M, "apx-p13-method", "Method mastery gauntlet",
    "Five spec-hard methods; circle the operators, then implement.",
    "Võ đài làm chủ phương thức",
    "Năm phương thức khó về đặc tả; khoanh tròn các toán tử, rồi cài đặt.",
    after_lesson="apx-m13-mixed", minutes=60, difficulty="advanced",
    challenges=[P_EVEN, P_REPEAT, P_FREQ, P_STAR, P_SECOND],
    vi_challenges={
        "apx-m13-frequent": vi_challenge(
            "Ký tự xuất hiện nhiều nhất (có phá hòa)",
            "Trả về **ký tự xuất hiện nhiều nhất** trong chuỗi; khi hòa, trả "
            "về ký tự **nhỏ nhất theo bảng chữ cái** trong nhóm hòa. Chuỗi "
            "khác rỗng và toàn chữ thường.\n\nVí dụ: `\"aabbbc\"` → `'b'`; "
            "`\"abab\"` → `'a'` (a và b hòa, a thắng).",
            [("frequent char", "Đếm số lần xuất hiện của từng ký tự; chỉ thay thế khi đếm lớn hơn, hoặc bằng nhau với ký tự nhỏ hơn.")],
        ),
        "apx-m13-star": vi_challenge(
            "Chèn dấu sao vào bản sao liền kề",
            "Giữa mỗi cặp ký tự **liền kề bằng nhau**, chèn `'*'` (bản thân "
            "các ký tự giữ nguyên).\n\nVí dụ: `\"aabb\"` → `\"a*ab*b\"`; "
            "`\"abc\"` → `\"abc\"`; `\"\"` → `\"\"`.",
            [("star-inserted output", "Khởi tạo kết quả bằng charAt(0); từ i = 1, nối '*' trước ký tự khi nó bằng ký tự trước.")],
        ),
        "apx-m13-secondsmallest": vi_challenge(
            "Giá trị nhỏ riêng biệt thứ hai (có sentinel)",
            "Trả về **giá trị nhỏ riêng biệt thứ hai**; trả -1 khi không tồn "
            "tại (rỗng, một phần tử, hoặc toàn bộ bằng nhau).\n\nVí dụ: "
            "`{4,1,4,2}` → `2`; `{5,5}` → `-1`; `{-1,-1,3}` → `3`.",
            [("second smallest", "Hai lượt: tìm min, rồi min trong các giá trị nghiêm ngặt lớn hơn min; -1 nếu không có.")],
        ),
        "apx-m13-evendigits": vi_challenge(
            "Tổng chữ số chẵn (đệ quy)",
            "Tính đệ quy tổng các **chữ số chẵn** của số tự nhiên (chữ số lẻ "
            "đóng góp 0). Không dùng vòng lặp.\n\nVí dụ: 2468 → `20`; 135 → "
            "`0`; 0 → `0`.",
            [("even digit sum", "Cơ sở n == 0 trả 0; bước: (d chẵn ? d : 0) + đệ quy(n / 10).")],
        ),
        "apx-m13-repeats": vi_challenge(
            "Đếm bản sao liền kề trong danh sách",
            "Đếm các vị trí i (từ phần tử thứ hai trở đi) mà phần tử "
            "**bằng phần tử trước nó**. Dùng `.equals` — đây là đối tượng "
            "Integer.\n\nVí dụ: `[1,1,2,2,2,3]` → `3`.",
            [("adjacent repeat count", "Vòng lặp từ i = 1; list.get(i).equals(list.get(i - 1)) — không bao giờ == trên đối tượng ngoài cache nhỏ.")],
        ),
    },
    solutions=[
        ("apx-m13-frequent", r"""public class Solution {
    public static char process(String s) {
        char best = 0;
        int bestN = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            int n = 0;
            for (int j = 0; j < s.length(); j++) {
                if (s.charAt(j) == c) {
                    n++;
                }
            }
            if (n > bestN || (n == bestN && c < best)) {
                bestN = n;
                best = c;
            }
        }
        return best;
    }
}
""", r"""public class Solution {
    // BUG: on ties keeps the LAST seen instead of the alphabetically smallest
    public static char process(String s) {
        char best = 0;
        int bestN = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            int n = 0;
            for (int j = 0; j < s.length(); j++) {
                if (s.charAt(j) == c) {
                    n++;
                }
            }
            if (n >= bestN) {
                bestN = n;
                best = c;
            }
        }
        return best;
    }
}
"""),
        ("apx-m13-star", r"""public class Solution {
    public static String process(String s) {
        if (s.length() <= 1) {
            return s;
        }
        StringBuilder out = new StringBuilder().append(s.charAt(0));
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                out.append('*');
            }
            out.append(s.charAt(i));
        }
        return out.toString();
    }
}
""", r"""public class Solution {
    // BUG: inserts at most ONE star — the flag latches after the first pair
    public static String process(String s) {
        if (s.length() <= 1) {
            return s;
        }
        StringBuilder out = new StringBuilder().append(s.charAt(0));
        boolean used = false;
        for (int i = 1; i < s.length(); i++) {
            if (!used && s.charAt(i) == s.charAt(i - 1)) {
                out.append('*');
                used = true;
            }
            out.append(s.charAt(i));
        }
        return out.toString();
    }
}
"""),
        ("apx-m13-secondsmallest", r"""public class Solution {
    public static int process(int[] arr) {
        if (arr.length < 2) {
            return -1;
        }
        int min = Integer.MAX_VALUE;
        for (int v : arr) {
            if (v < min) {
                min = v;
            }
        }
        int second = Integer.MAX_VALUE;
        for (int v : arr) {
            if (v > min && v < second) {
                second = v;
            }
        }
        return second == Integer.MAX_VALUE ? -1 : second;
    }
}
""", r"""public class Solution {
    // BUG: accepts duplicates of the min as the "second smallest"
    public static int process(int[] arr) {
        if (arr.length < 2) {
            return -1;
        }
        int min = Integer.MAX_VALUE;
        for (int v : arr) {
            if (v < min) {
                min = v;
            }
        }
        int second = Integer.MAX_VALUE;
        for (int v : arr) {
            if (v >= min && v < second) {
                second = v;
            }
        }
        return second == Integer.MAX_VALUE ? -1 : second;
    }
}
"""),
        ("apx-m13-evendigits", r"""public class Solution {
    public static int process(int n) {
        if (n == 0) {
            return 0;
        }
        int d = n % 10;
        int add = (d % 2 == 0) ? d : 0;
        return add + process(n / 10);
    }
}
""", r"""public class Solution {
    // BUG: sums ALL digits, not just the even ones
    public static int process(int n) {
        if (n == 0) {
            return 0;
        }
        return n % 10 + process(n / 10);
    }
}
"""),
        ("apx-m13-repeats", r"""public class Solution {
    public static int process(java.util.ArrayList<Integer> list) {
        int count = 0;
        for (int i = 1; i < list.size(); i++) {
            if (list.get(i).equals(list.get(i - 1))) {
                count++;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: == on Integer objects — works in the small cache, fails beyond 127
    public static int process(java.util.ArrayList<Integer> list) {
        int count = 0;
        for (int i = 1; i < list.size(); i++) {
            if (list.get(i) == list.get(i - 1)) {
                count++;
            }
        }
        return count;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m13", "Checkpoint: the sandwich count",
    "Window-of-three scanning with an exact equality pattern.",
    20,
    r"""
Window problems look innocent and punish the boundaries: the loop
runs from 1 to length - 2 (inclusive), and both window edges are
compared to the middle. Write the window indexes in the margin
before coding.
""",
    "Điểm kiểm tra: đếm bánh kẹp",
    "Quét cửa sổ ba phần tử với mẫu so sánh bằng chính xác.",
    r"""
Bài cửa sổ trông vô hại và trừng phạt các biên: vòng lặp chạy từ 1
đến độ dài - 2 (bao gồm), và cả hai mép cửa sổ được so với phần tử
giữa. Viết các chỉ số cửa sổ ra lề trước khi viết mã.
""",
    CP13,
    VI_CP13,
    solution=r"""public class Solution {
    public static int process(int[] arr) {
        int count = 0;
        for (int i = 1; i < arr.length - 1; i++) {
            if (arr[i - 1] == arr[i + 1] && arr[i] != arr[i - 1]) {
                count++;
            }
        }
        return count;
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: loop stops one window early — the last sandwich is never checked
    public static int process(int[] arr) {
        int count = 0;
        for (int i = 1; i < arr.length - 2; i++) {
            if (arr[i - 1] == arr[i + 1] && arr[i] != arr[i - 1]) {
                count++;
            }
        }
        return count;
    }
}
""",
)

print("M13 done")
