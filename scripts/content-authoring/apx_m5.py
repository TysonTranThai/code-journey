#!/usr/bin/env python3
"""AP CSA Advanced M5 — Advanced string problems (all ground truths executed)."""
from apx import *

M = "apx-strings"

write_module(
    M,
    "Advanced String Problems",
    "Multi-step traversal, char arithmetic, run-length processing, masking, and word scanning — no intro exercises. Difficulty E2–E4.",
    "Bài toán chuỗi nâng cao",
    "Duyệt nhiều bước, phép toán ký tự, xử lý run-length, che giấu dữ liệu, và quét từ — không có bài nhập môn. Độ khó E2–E4.",
    lessons=["apx-m5-toolkit", "apx-m5-boundaries", "apx-m5-transform", "apx-cp-m5"],
    practices=["apx-p5-strings"],
)

L1 = r"""
You already know `charAt`, `substring`, `indexOf`, `equals`,
`compareTo`. At exam level the differentiators are **index
arithmetic** and **building results**:

- The middle of a string of length n starts at `(n - 1) / 2` for the
  two-center convention — one formula, both parities. Verify: n=4 →
  index 1 ("co**de**"), n=5 → index 2 ("ab**c**de" pair starts at 2).
- Comparing *adjacent* characters (`charAt(i)` vs `charAt(i - 1)`)
  needs a loop from 1 — not 0 — and an empty-string guard.
- Run-length problems track a run counter and flush it at the last
  index. The flush after the loop is where most wrong answers live.
- Building results: `StringBuilder` is legal but plain concatenation
  is fine for exam sizes; what matters is appending in the right
  *order* under a conditional.

**Substring endpoints** remain the #1 source of lost points:
`substring(a, b)` includes a, excludes b, and throws if b > length or
a > b. Before you write one, say the included and excluded indexes out
loud.
"""

L2 = r"""
**Character classification without imports.** The exam gives you
`Character.isLetter/isDigit/isUpperCase` — and a raw alternative:

```java
char ch = s.charAt(i);
boolean letter = (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
boolean digit  = ch >= '0' && ch <= '9';
```

**char arithmetic** (Caesar shifts, digit sums):

```java
char shifted = (char) ('a' + (ch - 'a' + k) % 26);   // wrap letters
int digitVal = ch - '0';                              // '7' -> 7
```

The two classic boundary questions: does k = 26 (or a multiple) wrap
back exactly (yes — `% 26` handles it), and does the digit formula
work for `'0'` (yes — 0). Non-letters pass through unchanged in a
shift; forgetting the pass-through breaks half the hidden tests.

**Scanning words** in a string with arbitrary spaces: a boolean
"inside a word" state, flipped at transitions — not a split (the AP
subset has no `split`).
"""

L3 = r"""
**Transformation pipelines.** Many string problems are two passes in
disguise: classify first (letters/digits/positions), transform second
(shift/mask/remove). Trying to fuse the passes usually creates index
bugs; two clean passes beat one clever one.

**Masking** (keep structure, hide content) and **run-length
encoding** are the two shapes the exam reuses with new stories. For
RLE the flush discipline:

```java
// after the loop, the final run is still unflushed:
if (s.length() > 0) { out += s.charAt(s.length() - 1); out += run; }
```

Forgetting the final flush outputs a truncated encoding — a wrong
answer that *looks* almost right. That is the point: advanced string
problems hide their difficulty in the last iteration, the empty
input, and the single-character input. Test all three before you
submit anything.
"""

VI_L1 = r"""
Bạn đã biết `charAt`, `substring`, `indexOf`, `equals`, `compareTo`.
Ở tầm đề thi, yếu tố phân loại là **phép toán chỉ số** và **dựng kết
quả**:

- Giữa chuỗi độ dài n bắt đầu tại `(n - 1) / 2` theo quy ước hai tâm —
  một công thức cho cả hai tính chẵn lẻ. Kiểm chứng: n=4 → chỉ số 1
  ("co**de**"), n=5 → chỉ số 2 (cặp trong "ab**c**de" bắt đầu tại 2).
- So sánh ký tự *kề nhau* (`charAt(i)` với `charAt(i - 1)`) cần vòng
  lặp từ 1 — không phải 0 — và biến chặn chuỗi rỗng.
- Bài toán run-length theo dõi bộ đếm run và xả nó ở chỉ số cuối. Lệnh
  xả sau vòng lặp là nơi đa số đáp án sai trú ngụ.
- Dựng kết quả: `StringBuilder` hợp lệ nhưng nối chuỗi thường là đủ với
  cỡ đề thi; điều quan trọng là nối theo đúng *thứ tự* dưới một điều
  kiện.

**Hai đầu substring** vẫn là nguồn mất điểm số 1: `substring(a, b)` gồm
a, không gồm b, và ném ngoại lệ nếu b > độ dài hoặc a > b. Trước khi
viết, hãy đọc thành tiếng chỉ số được lấy và bị loại.
"""

VI_L2 = r"""
**Phân loại ký tự không cần import.** Đề thi cho bạn
`Character.isLetter/isDigit/isUpperCase` — và phương án thủ công:

```java
char ch = s.charAt(i);
boolean letter = (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
boolean digit  = ch >= '0' && ch <= '9';
```

**Phép toán trên char** (dịch Caesar, tổng chữ số):

```java
char shifted = (char) ('a' + (ch - 'a' + k) % 26);   // vòng lại bảng chữ cái
int digitVal = ch - '0';                              // '7' -> 7
```

Hai câu hỏi biên kinh điển: k = 26 (hoặc bội) có vòng lại đúng chỗ không
(có — `% 26` lo được), và công thức chữ số có đúng với `'0'` không
(có — 0). Ký tự không phải chữ đi qua không đổi trong phép dịch; quên
điều này làm hỏng một nửa test ẩn.

**Quét từ** trong chuỗi có khoảng trắng tùy ý: một trạng thái boolean
"đang trong từ", đổi ở các bước chuyển — không dùng split (tập con AP
không có `split`).
"""

VI_L3 = r"""
**Chuỗi biến đổi.** Nhiều bài chuỗi là hai lượt duyệt ngụy trang: phân
loại trước (chữ/số/vị trí), biến đổi sau (dịch/che/bỏ). Gộp hai lượt
thường tạo lỗi chỉ số; hai lượt sạch thắng một lượt thông minh.

**Che giấu** (giữ cấu trúc, ẩn nội dung) và **run-length encoding** là
hai hình dạng đề thi tái sử dụng với câu chuyện mới. Với RLE, kỷ luật
xả:

```java
// sau vòng lặp, run cuối vẫn chưa được xả:
if (s.length() > 0) { out += s.charAt(s.length() - 1); out += run; }
```

Quên xả cuối cho ra kết quả bị cắt cụt — đáp án sai *trông* gần đúng.
Đó chính là điểm: bài chuỗi nâng cao giấu độ khó ở vòng lặp cuối, đầu
vào rỗng, và đầu vào một ký tự. Kiểm tra cả ba trước khi nộp bất cứ gì.
"""

BOILER_STR = r"""public class Solution {
    public static String process(String s) {
        return ""; // replace
    }
}
"""

BOILER_INT = r"""public class Solution {
    public static int process(String s) {
        return 0; // replace
    }
}
"""

P_SHIFT = challenge(
    "apx-m5-shift",
    "Caesar shift with pass-through",
    "Shift every letter **k positions forward** (wrapping: 'z' + 1 = "
    "'a'), leaving digits, spaces, and punctuation unchanged. Case is "
    "preserved. Implement `process(String s)` with shift amount k = 3.\n\n"
    "Example: `\"Hello-World!\"` → `\"Khoor-Zruog!\"`.",
    BOILER_STR,
    [(
        "shifted with non-letters",
        r"""
CjTestBase.checkEq(Solution.process("Hello-World!"), "Khoor-Zruog!", "mixed case and punctuation");
CjTestBase.checkEq(Solution.process("xyz"), "abc", "wrap-around");
CjTestBase.checkEq(Solution.process(""), "", "empty");
CjTestBase.checkEq(Solution.process("a1z"), "d1c", "digits pass through");
""",
        "'a' + (ch - 'a' + 3) % 26 for lowercase; mirror with 'A'. Non-letters append as-is.",
    )],
    level="independent",
    difficulty="advanced",
)

P_WORDS = challenge(
    "apx-m5-words",
    "Count words with messy spacing",
    "Count the **words** in a string: maximal runs of non-space "
    "characters separated by one or more spaces. Leading, trailing, and "
    "repeated spaces must not create phantom words. Implement "
    "`process(String s)` returning the count (0 for empty/all-space).\n\n"
    "Example: `\"  hello   world  \"` → `2`.",
    BOILER_INT,
    [(
        "word count",
        r"""
CjTestBase.checkEq(Solution.process("  hello   world  "), 2, "messy spacing");
CjTestBase.checkEq(Solution.process(""), 0, "empty");
CjTestBase.checkEq(Solution.process("     "), 0, "all spaces");
CjTestBase.checkEq(Solution.process("one"), 1, "single word");
""",
        "State machine: count on the transition from space to non-space.",
    )],
    level="independent",
    difficulty="intermediate",
)

P_ADJ = challenge(
    "apx-m5-collapse",
    "Collapse adjacent duplicates",
    "Remove **consecutive** duplicate characters, keeping the first of "
    "each run (\"aabbca\" → \"abca\"). Only *adjacent* equal characters "
    "collapse; non-adjacent duplicates stay. Implement `process(String "
    "s)`.\n\nExamples: `\"aabbca\"` → `\"abca\"`, `\"\"` → `\"\"`, "
    "`\"aaa\"` → `\"a\"`.",
    BOILER_STR,
    [(
        "collapsed runs",
        r"""
CjTestBase.checkEq(Solution.process("aabbca"), "abca", "mixed runs");
CjTestBase.checkEq(Solution.process(""), "", "empty");
CjTestBase.checkEq(Solution.process("aaa"), "a", "single long run");
CjTestBase.checkEq(Solution.process("ab"), "ab", "no collapse");
""",
        "Append charAt(i) only when it differs from charAt(i-1); seed with charAt(0).",
    )],
    level="guided",
    difficulty="intermediate",
)

P_MASK = challenge(
    "apx-m5-mask",
    "Mask the digits",
    "Replace every **digit** with '#', leaving every other character "
    "exactly as it was. Implement `process(String s)`.\n\nExample: "
    "`\"ab12cd3\"` → `\"ab##cd#\"`.",
    BOILER_STR,
    [(
        "masked output",
        r"""
CjTestBase.checkEq(Solution.process("ab12cd3"), "ab##cd#", "digits masked");
CjTestBase.checkEq(Solution.process(""), "", "empty");
CjTestBase.checkEq(Solution.process("2026"), "####", "all digits");
CjTestBase.checkEq(Solution.process("a-b!"), "a-b!", "no digits");
""",
        "ch >= '0' && ch <= '9' → '#', else append ch.",
    )],
    level="imitation",
    difficulty="intermediate",
)

P_RUN = challenge(
    "apx-m5-longestrun",
    "Longest run",
    "Return the **length of the longest run** of identical adjacent "
    "characters. Case matters: 'b' and 'B' are different characters. "
    "Implement `process(String s)` (0 for empty).\n\nExample: "
    "`\"aaBBBbc\"` → `3` (the BBB run).",
    BOILER_INT,
    [(
        "longest run length",
        r"""
CjTestBase.checkEq(Solution.process("aaBBBbc"), 3, "BBB run");
CjTestBase.checkEq(Solution.process("aabBBbc"), 2, "case-sensitive: b and B split the run");
CjTestBase.checkEq(Solution.process(""), 0, "empty");
CjTestBase.checkEq(Solution.process("a"), 1, "single char");
CjTestBase.checkEq(Solution.process("abab"), 1, "no repeats");
""",
        "cur = (i > 0 && charAt(i) == charAt(i-1)) ? cur + 1 : 1; track max.",
    )],
    level="independent",
    difficulty="intermediate",
)

P_RLE = challenge(
    "apx-m5-rle",
    "Run-length encode (flush the last run)",
    "Encode runs as `<char><count>`: \"aaabbbcc\" → \"a3b3c2\". Runs of "
    "length 1 still get the count. Implement `process(String s)` "
    "(empty string encodes to the empty string).\n\nThis is the flush "
    "trap: the final run ends at the loop's last index, not inside it.",
    BOILER_STR,
    [(
        "run-length encoding",
        r"""
CjTestBase.checkEq(Solution.process("aaabbbcc"), "a3b3c2", "basic encoding");
CjTestBase.checkEq(Solution.process(""), "", "empty");
CjTestBase.checkEq(Solution.process("x"), "x1", "single char gets count");
CjTestBase.checkEq(Solution.process("ab"), "a1b1", "alternating");
""",
        "Count runs; when the char changes (or the loop ends), append charAt(i-1) and the count.",
    )],
    level="real-world",
    difficulty="advanced",
)

CP5 = challenge(
    "apx-cp-m5-midpair",
    "Checkpoint: the middle pair",
    "Return the **middle two characters** of any string of length ≥ 2 "
    "— for even length the two straddling the center, for odd length "
    "the center character plus the one after it. (Shorter strings: "
    "return them unchanged.) Implement `process(String s)`.\n\n"
    "Examples: `\"code\"` → `\"od\"`, `\"abcde\"` → `\"cd\"`, `\"ab\"` → `\"ab\"`.",
    BOILER_STR,
    [(
        "middle pair",
        r"""
CjTestBase.checkEq(Solution.process("code"), "od", "even length");
CjTestBase.checkEq(Solution.process("abcde"), "cd", "odd length");
CjTestBase.checkEq(Solution.process("ab"), "ab", "already two");
CjTestBase.checkEq(Solution.process("abcdef"), "cd", "longer even");
""",
        "One formula: start = (length - 1) / 2; take two characters from there.",
    )],
    level="independent",
    difficulty="advanced",
)

VI_CP5 = vi_challenge(
    "Điểm kiểm tra: cặp ký tự giữa",
    "Trả về **hai ký tự giữa** của chuỗi bất kỳ độ dài ≥ 2 — độ dài "
    "chẵn: hai ký tự ôm tâm; lẻ: ký tự tâm cộng ký tự ngay sau. (Chuỗi "
    "ngắn hơn: trả nguyên bản.) Cài đặt `process(String s)`.\n\n"
    "Ví dụ: `\"code\"` → `\"od\"`, `\"abcde\"` → `\"cd\"`, `\"ab\"` → `\"ab\"`.",
    [("middle pair", "Một công thức: bắt đầu = (độ dài - 1) / 2; lấy hai ký tự từ đó.")],
)

write_practice(
    M, "apx-p5-strings", "String lab: transformations under constraints",
    "Six string transformations with hidden boundaries; verify all three edge inputs before submitting.",
    "Phòng thí nghiệm chuỗi: biến đổi dưới ràng buộc",
    "Sáu phép biến đổi chuỗi với biên ẩn; kiểm tra cả ba đầu vào biên trước khi nộp.",
    after_lesson="apx-m5-transform", minutes=55, difficulty="advanced",
    challenges=[P_MASK, P_ADJ, P_WORDS, P_RUN, P_SHIFT, P_RLE],
    vi_challenges={
        "apx-m5-shift": vi_challenge(
            "Dịch Caesar có ký tự đi qua",
            "Dịch mọi chữ cái **tiến k vị trí** (vòng lại: 'z' + 1 = 'a'), "
            "giữ nguyên chữ số, khoảng trắng và dấu câu. Giữ nguyên hoa/thường. "
            "Cài đặt `process(String s)` với k = 3.\n\nVí dụ: `\"Hello-World!\"` → `\"Khoor-Zruog!\"`.",
            [("shifted with non-letters", "'a' + (ch - 'a' + 3) % 26 cho chữ thường; đối xứng với 'A'. Ký tự khác nối nguyên bản.")],
        ),
        "apx-m5-words": vi_challenge(
            "Đếm từ với khoảng trắng lộn xộn",
            "Đếm **từ** trong chuỗi: các dãy ký tự không phải khoảng trắng tối"
            "đa, phân cách bởi một hoặc nhiều khoảng trắng. Khoảng trắng đầu, "
            "cuối, lặp lại không được tạo từ ảo. Cài đặt `process(String s)` "
            "trả về số đếm (0 cho rỗng/toàn khoảng trắng).\n\nVí dụ: `\"  hello   world  \"` → `2`.",
            [("word count", "Máy trạng thái: đếm tại bước chuyển từ khoảng trắng sang không phải khoảng trắng.")],
        ),
        "apx-m5-collapse": vi_challenge(
            "Gộp ký tự liền kề trùng nhau",
            "Bỏ các ký tự **liền kề** trùng nhau, giữ ký tự đầu của mỗi run "
            "(\"aabbca\" → \"abca\"). Chỉ ký tự bằng nhau *kề nhau* được gộp; "
            "bản sao không kề nhau được giữ. Cài đặt `process(String s)`.\n\n"
            "Ví dụ: `\"aabbca\"` → `\"abca\"`, `\"\"` → `\"\"`, `\"aaa\"` → `\"a\"`.",
            [("collapsed runs", "Chỉ nối charAt(i) khi khác charAt(i-1); khởi tạo bằng charAt(0).")],
        ),
        "apx-m5-mask": vi_challenge(
            "Che các chữ số",
            "Thay mọi **chữ số** bằng '#', giữ nguyên mọi ký tự khác. Cài đặt "
            "`process(String s)`.\n\nVí dụ: `\"ab12cd3\"` → `\"ab##cd#\"`.",
            [("masked output", "ch >= '0' && ch <= '9' → '#', ngược lại nối ch.")],
        ),
        "apx-m5-longestrun": vi_challenge(
            "Run dài nhất",
            "Trả về **độ dài run dài nhất** gồm các ký tự giống nhau liền kề. "
            "Phân biệt hoa/thường: 'b' và 'B' là hai ký tự khác. Cài đặt "
            "`process(String s)` (0 cho rỗng).\n\nVí dụ: `\"aaBBBbc\"` → `3` (run BBB).",
            [("longest run length", "cur = (i > 0 && charAt(i) == charAt(i-1)) ? cur + 1 : 1; ghi nhận max.")],
        ),
        "apx-m5-rle": vi_challenge(
            "Mã hóa run-length (xả run cuối)",
            "Mã hóa các run thành `<ký tự><số đếm>`: \"aaabbbcc\" → \"a3b3c2\". "
            "Run độ dài 1 vẫn có số đếm. Cài đặt `process(String s)` (chuỗi rỗng "
            "mã hóa thành chuỗi rỗng).\n\nĐây là bẫy xả: run cuối kết thúc ở chỉ "
            "số cuối của vòng lặp, không phải bên trong nó.",
            [("run-length encoding", "Đếm các run; khi ký tự đổi (hoặc vòng lặp kết thúc), nối charAt(i-1) và số đếm.")],
        ),
    },
    solutions=[
        ("apx-m5-shift", r"""public class Solution {
    public static String process(String s) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch >= 'a' && ch <= 'z') {
                ch = (char) ('a' + (ch - 'a' + 3) % 26);
            } else if (ch >= 'A' && ch <= 'Z') {
                ch = (char) ('A' + (ch - 'A' + 3) % 26);
            }
            out.append(ch);
        }
        return out.toString();
    }
}
""", r"""public class Solution {
    // BUG: shifts non-letters too — punctuation and digits get scrambled
    public static String process(String s) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch >= 'a' && ch <= 'z') {
                ch = (char) ('a' + (ch - 'a' + 3) % 26);
            } else if (ch >= 'A' && ch <= 'Z') {
                ch = (char) ('A' + (ch - 'A' + 3) % 26);
            } else {
                ch = (char) (ch + 3);
            }
            out.append(ch);
        }
        return out.toString();
    }
}
"""),
        ("apx-m5-words", r"""public class Solution {
    public static int process(String s) {
        int count = 0;
        boolean inWord = false;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ' && !inWord) {
                count++;
                inWord = true;
            } else if (s.charAt(i) == ' ') {
                inWord = false;
            }
        }
        return count;
    }
}
""", r"""public class Solution {
    // BUG: counts every non-space character, not words
    public static int process(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ') {
                count++;
            }
        }
        return count;
    }
}
"""),
        ("apx-m5-collapse", r"""public class Solution {
    public static String process(String s) {
        if (s.length() == 0) {
            return s;
        }
        StringBuilder out = new StringBuilder().append(s.charAt(0));
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) != s.charAt(i - 1)) {
                out.append(s.charAt(i));
            }
        }
        return out.toString();
    }
}
""", r"""public class Solution {
    // BUG: crashes on empty input — appends charAt(0) before guarding
    public static String process(String s) {
        StringBuilder out = new StringBuilder().append(s.charAt(0));
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) != s.charAt(i - 1)) {
                out.append(s.charAt(i));
            }
        }
        return out.toString();
    }
}
"""),
        ("apx-m5-mask", r"""public class Solution {
    public static String process(String s) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            out.append(ch >= '0' && ch <= '9' ? '#' : ch);
        }
        return out.toString();
    }
}
""", r"""public class Solution {
    // BUG: masks letters instead of digits (inverted condition)
    public static String process(String s) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            out.append(ch >= 'a' && ch <= 'z' ? '#' : ch);
        }
        return out.toString();
    }
}
"""),
        ("apx-m5-longestrun", r"""public class Solution {
    public static int process(String s) {
        int best = 0;
        int cur = 0;
        for (int i = 0; i < s.length(); i++) {
            if (i > 0 && s.charAt(i) == s.charAt(i - 1)) {
                cur++;
            } else {
                cur = 1;
            }
            if (cur > best) {
                best = cur;
            }
        }
        return best;
    }
}
""", r"""public class Solution {
    // BUG: counts the total string length when any repeat exists
    public static int process(String s) {
        int best = 0;
        boolean anyRepeat = false;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                anyRepeat = true;
            }
        }
        if (anyRepeat) {
            return s.length();
        }
        return s.length() > 0 ? 1 : 0;
    }
}
"""),
        ("apx-m5-rle", r"""public class Solution {
    public static String process(String s) {
        if (s.length() == 0) {
            return "";
        }
        StringBuilder out = new StringBuilder();
        int run = 1;
        for (int i = 1; i <= s.length(); i++) {
            if (i < s.length() && s.charAt(i) == s.charAt(i - 1)) {
                run++;
            } else {
                out.append(s.charAt(i - 1)).append(run);
                run = 1;
            }
        }
        return out.toString();
    }
}
""", r"""public class Solution {
    // BUG: never flushes the final run — output truncated
    public static String process(String s) {
        if (s.length() == 0) {
            return "";
        }
        StringBuilder out = new StringBuilder();
        int run = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                run++;
            } else {
                out.append(s.charAt(i - 1)).append(run);
                run = 1;
            }
        }
        return out.toString();
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m5", "Checkpoint: middle pair",
    "The index-arithmetic checkpoint: one formula must serve both parities.",
    15,
    r"""
Index arithmetic is where string points are won. `(n - 1) / 2` is the
one formula that handles both parities — but only if you trust it over
your first instinct (n / 2), which is exactly what the wrong-looking
answer tests.
""",
    "Điểm kiểm tra: cặp giữa",
    "Bài kiểm tra phép toán chỉ số: một công thức phải phục vụ cả hai tính chẵn lẻ.",
    r"""
Phép toán chỉ số là nơi điểm chuỗi được giành. `(n - 1) / 2` là công
thức duy nhất xử lý cả hai tính chẵn lẻ — nhưng chỉ khi bạn tin nó hơn
phản xạ đầu tiên (n / 2), chính là điều đáp án sai-khó-nhìn kiểm tra.
""",
    CP5,
    VI_CP5,
    solution=r"""public class Solution {
    public static String process(String s) {
        if (s.length() < 3) {
            return s;
        }
        int start = (s.length() - 1) / 2;
        return s.substring(start, start + 2);
    }
}
""",
    wrong=r"""public class Solution {
    // BUG: n/2 grabs the right-hand pair on even lengths
    public static String process(String s) {
        if (s.length() < 3) {
            return s;
        }
        int start = s.length() / 2;
        return s.substring(start, start + 2);
    }
}
""",
)

print("M5 done")
