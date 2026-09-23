#!/usr/bin/env python3
"""AP CSA M18 — FRQ foundations: reading specs, pre/postconditions, writing from prose."""
from apc import *

M = "apc-frq"

L1 = r"""
An FRQ (free-response question) hands you a **specification** and asks
for code that satisfies it. Reading the spec precisely is half the
task. Every AP-style spec names:

- the **method signature** — name, parameter types, return type. Match
  it exactly; the graders' tests call YOUR method with THEIR types.
- **preconditions** — what's guaranteed true before the call ("the
  list has at least one element"). You may *rely* on these; never
  re-check them for points, never violate them.
- **postconditions** — what must be true after the call ("returns the
  number of..."). This is the contract you must deliver.

```java
// Precondition: wordCount >= 0
// Postcondition: returns the total number of characters across
// wordCount words, given their lengths
public static int totalChars(int[] lengths, int wordCount)
```

Write the postcondition as a comment in your own words BEFORE coding.
If your restatement is wrong, every line after it is wrong too.
"""

L2 = r"""
**Writing code from prose** — the specification is a paragraph, the
answer is a method. The workflow:

1. Restate the postcondition as a formula or loop invariant.
2. Choose the traversal (array? string? list? which direction?).
3. Write the accumulator skeleton FIRST, fill the body SECOND.
4. Check the preconditions for shortcuts you may take.

Example spec: *"Return the number of times the character ch appears
in the string s, ignoring case."* Restated: loop over every index of
s, compare case-folded characters to ch, count matches.

```java
public static int countIgnoreCase(String s, char ch) {
    int count = 0;
    for (int i = 0; i < s.length(); i++) {
        if (Character.toLowerCase(s.charAt(i)) == Character.toLowerCase(ch)) {
            count++;
        }
    }
    return count;
}
```

Common spec-reading failures, in order of frequency:

- missing the "ignoring case" / "ignoring order" / "at most" qualifier;
- returning the wrong *shape* (index vs value, count vs list);
- handling the empty input wrong (or crashing on it);
- shadowing the parameter (`String s` then `int s = 0`).
"""

L3 = r"""
**Modifying provided code** — some FRQs give you a working class and
ask you to add a method that fits its conventions:

- Match the class's style: if it uses accessors everywhere, use them.
- Reuse existing public methods when the spec allows — calling
  `getName()` beats re-deriving the field.
- Do NOT touch the provided code: add methods, don't rewrite the
  class. Graders diff against the given parts.
- The spec's return type is a hint: `boolean` wants a predicate, `int`
  wants a count/index, a class name wants an object.

```java
// Given class: Student { getName(), getScore() }
// Spec: "returns the name of the higher-scoring student;
// if tied, return either"
public static String winner(Student a, Student b) {
    if (a.getScore() >= b.getScore()) {
        return a.getName();
    }
    return b.getName();
}
```

Trace your finished method against the spec's OWN example (specs
usually include one) — if your trace of their example disagrees with
their stated answer, your reading is wrong, not their example.
"""

write_module(
    M,
    "FRQ Foundations",
    "Reading specifications: preconditions, postconditions, writing methods from prose, and extending provided classes.",
    "Nền tảng FRQ",
    "Đọc đặc tả: điều kiện tiền, điều kiện hậu, viết phương thức từ văn bản, và mở rộng lớp cho sẵn.",
    lessons=["apc-m18-specs", "apc-m18-prose", "apc-m18-modify", "apc-cp-m18"],
    practices=["apc-p18-frq"],
)

write_lesson(
    M, "apc-m18-specs", "Reading a specification",
    "Signatures, preconditions you may rely on, postconditions you must deliver.",
    12, L1,
    "Đọc đặc tả",
    "Chữ ký, điều kiện tiền được phép dựa vào, điều kiện hậu phải giao.",
    r"""
Một FRQ (câu tự luận) đưa cho bạn một **đặc tả** và yêu cầu mã thỏa
mãn nó. Đọc đặc tả chính xác là một nửa công việc. Mọi đặc tả kiểu đề
gọi tên:

- **chữ ký phương thức** — tên, kiểu tham số, kiểu trả về. Khớp tuyệt
  đối; bài chấm của họ gọi phương thức CỦA BẠN với kiểu của HỌ.
- **điều kiện tiền** — cái gì bảo đảm đúng trước khi gọi ("danh sách
  có ít nhất một phần tử"). Bạn được *dựa vào* các điều này; đừng bao
  giờ kiểm tra lại chúng để lấy điểm, đừng bao giờ vi phạm chúng.
- **điều kiện hậu** — cái gì phải đúng sau khi gọi ("trả về số
  lượng..."). Đây là hợp đồng bạn phải giao.

```java
// Precondition: wordCount >= 0
// Postcondition: returns the total number of characters across
// wordCount words, given their lengths
public static int totalChars(int[] lengths, int wordCount)
```

Viết điều kiện hậu thành bình luận bằng lời của riêng bạn TRƯỚC khi
code. Nếu lời diễn giải của bạn sai, mọi dòng phía sau cũng sai theo.
""",
)

write_lesson(
    M, "apc-m18-prose", "Writing code from prose",
    "Restate, choose the traversal, skeleton first, exploit preconditions.",
    12, L2,
    "Viết mã từ văn bản",
    "Diễn giải lại, chọn cách duyệt, khung trước, tận dụng điều kiện tiền.",
    r"""
**Viết mã từ văn bản** — đặc tả là một đoạn văn, đáp án là một phương
thức. Quy trình:

1. Diễn giải điều kiện hậu thành công thức hoặc bất biến vòng lặp.
2. Chọn kiểu duyệt (mảng? chuỗi? danh sách? chiều nào?).
3. Viết khung bộ tích lũy TRƯỚC, điền thân sau.
4. Rà điều kiện tiền để lấy các phím tắt được phép.

Ví dụ đặc tả: *"Trả về số lần ký tự ch xuất hiện trong chuỗi s, bỏ qua
chữ hoa/thường."* Diễn giải: duyệt mọi chỉ số của s, so ký tự đã hạ
thấp với ch, đếm khớp.

```java
public static int countIgnoreCase(String s, char ch) {
    int count = 0;
    for (int i = 0; i < s.length(); i++) {
        if (Character.toLowerCase(s.charAt(i)) == Character.toLowerCase(ch)) {
            count++;
        }
    }
    return count;
}
```

Các lỗi đọc đề hay gặp, xếp theo tần suất:

- bỏ sót định lượng "bỏ qua hoa/thường" / "bỏ qua thứ tự" / "tối đa";
- trả sai *hình dạng* (chỉ số so với giá trị, số đếm so với danh sách);
- xử lý đầu vào rỗng sai (hoặc crash trên nó);
- che khuất tham số (`String s` rồi `int s = 0`).
""",
)

write_lesson(
    M, "apc-m18-modify", "Extending provided code",
    "Match style, reuse accessors, add methods without touching the given class.",
    12, L3,
    "Mở rộng mã cho sẵn",
    "Đồng bộ phong cách, tái dùng accessor, thêm phương thức mà không đụng lớp cho sẵn.",
    r"""
**Chỉnh sửa mã cho sẵn** — một số FRQ đưa cho bạn một lớp chạy đúng
và yêu cầu thêm phương thức khớp quy ước của nó:

- Theo phong cách của lớp: nếu nó dùng accessor khắp nơi, hãy dùng
  accessor.
- Tái dùng phương thức công khai hiện có khi đặc tả cho phép — gọi
  `getName()` hơn là suy lại trường từ đầu.
- ĐỪNG đụng vào phần mã cho sẵn: thêm phương thức, đừng viết lại lớp.
  Bài chấm so từng phần đã cho.
- Kiểu trả về của đặc tả là một gợi ý: `boolean` muốn một vị từ,
  `int` muốn một con đếm/chỉ số, tên lớp muốn một đối tượng.

```java
// Lớp cho sẵn: Student { getName(), getScore() }
// Đặc tả: "trả về tên của học sinh điểm cao hơn;
// nếu hòa, trả về tên nào cũng được"
public static String winner(Student a, Student b) {
    if (a.getScore() >= b.getScore()) {
        return a.getName();
    }
    return b.getName();
}
```

Truy vết phương thức đã viết xong bằng CHÍNH ví dụ của đặc tả (đặc tả
thường kèm một ví dụ) — nếu truy vết của bạn về ví dụ của họ mâu thuẫn
với đáp án họ tuyên bố, thì cách bạn đọc đề sai, không phải ví dụ của
họ sai.
""",
)

BOILER_TOTAL = r"""public class Solution {
    // Precondition: wordCount >= 0 and wordCount <= lengths.length
    // Postcondition: returns the total number of characters across
    // the first wordCount words, given their lengths
    public static int totalChars(int[] lengths, int wordCount) {
        // complete
        return 0;
    }
}
"""

BOILER_ISBN = r"""public class Solution {
    // Precondition: code consists only of digit characters, length >= 1
    // Postcondition: returns true exactly when the digit sum is
    // divisible by 10
    public static boolean validChecksum(String code) {
        // complete
        return false;
    }
}
"""

BOILER_STUDENT = r"""public class Solution {
    public static class Student {
        private String name;
        private int score;

        public Student(String name, int score) {
            this.name = name;
            this.score = score;
        }

        public String getName() {
            return name;
        }

        public int getScore() {
            return score;
        }
    }

    // Postcondition: returns the name of the higher-scoring student;
    // if tied, return a's name
    public static String winner(Student a, Student b) {
        // complete (tie goes to a)
        return "";
    }
}
"""

BOILER_FIXISBN = r"""public class Solution {
    // Precondition: code consists only of digit characters, length >= 1
    // Postcondition: returns true exactly when the digit sum is
    // divisible by 10
    public static boolean validChecksum(String code) {
        // BUG: original flaw kept — sums the CHAR CODES, not the
        // digit values, so '9' contributes 57 instead of 9
        int sum = 0;
        for (int i = 0; i < code.length(); i++) {
            sum += code.charAt(i);
        }
        return sum % 10 == 0;
    }
}
"""

CP18 = r"""public class Solution {
    // Precondition: s contains at least one character
    // Postcondition: returns the longest RUN of equal consecutive
    // characters in s (e.g. "abbbcc" -> 3); single characters are runs
    // of length 1
    public static int longestRun(String s) {
        // complete
        return 0;
    }
}
"""

P_TOTAL = challenge(
    "apc-m18-totalchars",
    "Spec: total characters",
    "Implement exactly to spec: `totalChars(int[] lengths, int wordCount)` returns the sum of the first `wordCount` entries of `lengths`. Rely on the precondition (no validation needed).",
    BOILER_TOTAL,
    [(
        "spec compliance",
        r"""
CjTestBase.checkEq(Solution.totalChars(new int[] {3, 5, 2}, 2), 8, "first two words");
CjTestBase.checkEq(Solution.totalChars(new int[] {3, 5, 2}, 0), 0, "zero words");
CjTestBase.checkEq(Solution.totalChars(new int[] {7}, 1), 7, "single word");
""",
        "loop from 0 while i < wordCount, accumulating lengths[i].",
    )],
    level="imitation",
)

P_ISBN = challenge(
    "apc-m18-isbn",
    "Spec: checksum",
    "Implement to spec: `validChecksum(String code)` returns true exactly when the sum of the DIGIT VALUES is divisible by 10. Precondition guarantees digits only — no validation required.",
    BOILER_ISBN,
    [(
        "digit values, not codes",
        r"""
CjTestBase.checkEq(Solution.validChecksum("19"), true, "1+9 = 10");
CjTestBase.checkEq(Solution.validChecksum("123"), false, "1+2+3 = 6");
CjTestBase.checkEq(Solution.validChecksum("992"), true, "9+9+2 = 20");
CjTestBase.checkEq(Solution.validChecksum("1239"), false, "1+2+3+9 = 15");
""",
        "Character.getNumericValue(code.charAt(i)) converts a digit char to its value.",
    )],
    level="guided",
)

P_STUDENT = challenge(
    "apc-m18-winner",
    "Spec: extend the class",
    "Using the provided Student class, implement `winner(Student a, Student b)` to spec: the name of the higher-scoring student; if tied, a's name. Use the accessors — do not modify the class.",
    BOILER_STUDENT,
    [(
        "tie contract",
        r"""
Solution.Student a = new Solution.Student("An", 80);
Solution.Student b = new Solution.Student("Binh", 90);
Solution.Student c = new Solution.Student("Chi", 80);
CjTestBase.checkEq(Solution.winner(a, b), "Binh", "higher wins");
CjTestBase.checkEq(Solution.winner(a, c), "An", "tie goes to a");
""",
        "a.getScore() >= b.getScore() ? a.getName() : b.getName()",
    )],
    level="independent",
)

P_FIXISBN = challenge(
    "apc-m18-fix-isbn",
    "Debug: char codes vs digit values",
    "`validChecksum` compiles and runs but returns wrong answers: it sums CHAR CODES ('9' contributes 57, not 9). Fix it to sum digit values (signature and comments stay).",
    BOILER_FIXISBN,
    [(
        "digits repaired",
        r"""
CjTestBase.checkEq(Solution.validChecksum("19"), true, "1+9 = 10");
CjTestBase.checkEq(Solution.validChecksum("123"), false, "1+2+3 = 6");
CjTestBase.checkEq(Solution.validChecksum("992"), true, "9+9+2 = 20");
""",
        "sum += code.charAt(i) - '0';",
    )],
    level="debugging",
)

CP18C = challenge(
    "apc-cp-m18-run",
    "Checkpoint: longest run",
    "Implement to spec: `longestRun(String s)` returns the length of the longest run of equal consecutive characters. \"abbbcc\" -> 3 (the run of b's); \"abc\" -> 1; single characters count as runs of length 1. Precondition: s has at least one character.",
    CP18,
    [(
        "run boundaries",
        r"""
CjTestBase.checkEq(Solution.longestRun("abbbcc"), 3, "b-run wins");
CjTestBase.checkEq(Solution.longestRun("abc"), 1, "no repeats");
CjTestBase.checkEq(Solution.longestRun("aaaa"), 4, "one long run");
CjTestBase.checkEq(Solution.longestRun("a"), 1, "single char");
""",
        "track current run and best run; reset current when the char changes.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p18-frq", "FRQ-style reps", "Spec-following, checksums, extending classes, char-code bugs, run counting.",
    "Luyện kiểu FRQ", "Bám đặc tả, checksum, mở rộng lớp, lỗi mã ký tự, đếm chuỗi liên tiếp.",
    after_lesson="apc-m18-modify", minutes=55, difficulty="beginner",
    challenges=[P_TOTAL, P_ISBN, P_STUDENT, P_FIXISBN],
    vi_challenges={
        "apc-m18-totalchars": vi_challenge("Đặc tả: tổng ký tự", "Cài đặt đúng đặc tả: `totalChars(int[] lengths, int wordCount)` trả tổng của `wordCount` phần tử ĐẦU TIÊN của `lengths`. Dựa vào điều kiện tiền (không cần kiểm tra hợp lệ).",
            [("spec compliance", "lặp i từ 0 trong khi i < wordCount, cộng dồn lengths[i].")]),
        "apc-m18-isbn": vi_challenge("Đặc tả: checksum", "Cài đặt theo đặc tả: `validChecksum(String code)` trả true đúng khi tổng GIÁ TRỊ CHỮ SỐ chia hết cho 10. Điều kiện tiền bảo đảm chỉ có chữ số — không cần kiểm tra hợp lệ.",
            [("digit values, not codes", "Character.getNumericValue(code.charAt(i)) đổi ký tự chữ số thành giá trị.")]),
        "apc-m18-winner": vi_challenge("Đặc tả: mở rộng lớp", "Dùng lớp Student cho sẵn, cài đặt `winner(Student a, Student b)` theo đặc tả: tên học sinh có điểm cao hơn; nếu hòa, trả tên của a. Dùng accessor — không sửa lớp.",
            [("tie contract", "a.getScore() >= b.getScore() ? a.getName() : b.getName()")]),
        "apc-m18-fix-isbn": vi_challenge("Gỡ lỗi: mã ký tự so với giá trị chữ số", "`validChecksum` biên dịch và chạy nhưng trả đáp án sai: nó cộng MÃ KÝ TỰ ('9' đóng góp 57, không phải 9). Sửa để cộng giá trị chữ số (chữ ký và chú thích giữ nguyên).",
            [("digits repaired", "sum += code.charAt(i) - '0';")]),
    },
    solutions=[
        ("apc-m18-totalchars", r"""public class Solution {
    public static int totalChars(int[] lengths, int wordCount) {
        int total = 0;
        for (int i = 0; i < wordCount; i++) {
            total += lengths[i];
        }
        return total;
    }
}
""", r"""public class Solution {
    public static int totalChars(int[] lengths, int wordCount) {
        // BUG: iterates the WHOLE array, ignoring the wordCount
        // contract — counts words beyond the first wordCount
        int total = 0;
        for (int i = 0; i < lengths.length; i++) {
            total += lengths[i];
        }
        return total;
    }
}
"""),
        ("apc-m18-isbn", r"""public class Solution {
    public static boolean validChecksum(String code) {
        int sum = 0;
        for (int i = 0; i < code.length(); i++) {
            sum += code.charAt(i) - '0';
        }
        return sum % 10 == 0;
    }
}
""", r"""public class Solution {
    public static boolean validChecksum(String code) {
        // BUG: sums the CHAR CODES, not the digit values, so '9'
        // contributes 57 instead of 9
        int sum = 0;
        for (int i = 0; i < code.length(); i++) {
            sum += code.charAt(i);
        }
        return sum % 10 == 0;
    }
}
"""),
        ("apc-m18-winner", r"""public class Solution {
    public static class Student {
        private String name;
        private int score;

        public Student(String name, int score) {
            this.name = name;
            this.score = score;
        }

        public String getName() {
            return name;
        }

        public int getScore() {
            return score;
        }
    }

    public static String winner(Student a, Student b) {
        if (a.getScore() >= b.getScore()) {
            return a.getName();
        }
        return b.getName();
    }
}
""", r"""public class Solution {
    public static class Student {
        private String name;
        private int score;

        public Student(String name, int score) {
            this.name = name;
            this.score = score;
        }

        public String getName() {
            return name;
        }

        public int getScore() {
            return score;
        }
    }

    public static String winner(Student a, Student b) {
        // BUG: strict > breaks the tie contract — ties must return
        // a's name, this returns b's
        if (a.getScore() > b.getScore()) {
            return a.getName();
        }
        return b.getName();
    }
}
"""),
        ("apc-m18-fix-isbn", r"""public class Solution {
    public static boolean validChecksum(String code) {
        int sum = 0;
        for (int i = 0; i < code.length(); i++) {
            sum += code.charAt(i) - '0';
        }
        return sum % 10 == 0;
    }
}
""", r"""public class Solution {
    public static boolean validChecksum(String code) {
        // BUG: original flaw kept — sums the CHAR CODES, not the
        // digit values, so '9' contributes 57 instead of 9
        int sum = 0;
        for (int i = 0; i < code.length(); i++) {
            sum += code.charAt(i);
        }
        return sum % 10 == 0;
    }
}
"""),
        ("apc-cp-m18-run", r"""public class Solution {
    public static int longestRun(String s) {
        int best = 1;
        int current = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                current++;
                if (current > best) {
                    best = current;
                }
            } else {
                current = 1;
            }
        }
        return best;
    }
}
""", r"""public class Solution {
    public static int longestRun(String s) {
        // BUG: resets best to 1 whenever the run breaks — forgets the
        // best seen so far
        int best = 1;
        int current = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                current++;
                if (current > best) {
                    best = current;
                }
            } else {
                current = 1;
                best = 1;
            }
        }
        return best;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m18", "Checkpoint: longest run",
    "A full spec-to-code cycle: run boundaries, best-so-far, reset discipline.",
    25,
    r"""
The pattern: the run counter increments while consecutive chars
match, resets to 1 when they don't, and the BEST never resets. The W
breaks exactly that last clause — best-so-far variables must never
move backwards. Trace "abbbcc" by hand before coding: a(1) b(2) b(3)
b->reset... the table IS the algorithm.
""",
    "Điểm kiểm tra: chuỗi liên tiếp dài nhất",
    "Một vòng đặc-tả-thành-mã: biên của chuỗi liên tiếp, best-so-far, kỷ luật reset.",
    r"""
Mẫu hình: bộ đếm chuỗi tăng khi các ký tự liên tiếp khớp, reset về 1
khi không khớp, và BEST không bao giờ được reset. W vi phạm đúng mệnh
đề cuối — biến best-so-far không bao giờ được đi lùi. Truy vết
"abbbcc" bằng tay trước khi code: a(1) b(2) b(3) b->reset... bảng
truy vết CHÍNH LÀ thuật toán.
""",
    CP18C,
    vi_challenge("Điểm kiểm tra: chuỗi liên tiếp dài nhất", "Cài đặt theo đặc tả: `longestRun(String s)` trả độ dài chuỗi ký tự bằng nhau liên tiếp dài nhất. \"abbbcc\" -> 3 (chuỗi b); \"abc\" -> 1; ký tự đơn là chuỗi độ dài 1. Điều kiện tiền: s có ít nhất một ký tự.",
        [("run boundaries", "theo dõi chuỗi hiện tại và chuỗi tốt nhất; reset chuỗi hiện tại khi ký tự đổi.")]),
    solution=r"""public class Solution {
    public static int longestRun(String s) {
        int best = 1;
        int current = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                current++;
                if (current > best) {
                    best = current;
                }
            } else {
                current = 1;
            }
        }
        return best;
    }
}
""",
    wrong=r"""public class Solution {
    public static int longestRun(String s) {
        // BUG: resets best to 1 whenever the run breaks — forgets the
        // best seen so far
        int best = 1;
        int current = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                current++;
                if (current > best) {
                    best = current;
                }
            } else {
                current = 1;
                best = 1;
            }
        }
        return best;
    }
}
""",
)
