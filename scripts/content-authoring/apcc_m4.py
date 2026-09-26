#!/usr/bin/env python3
"""AP CSA Core M4 — Methods & Specification Problems (helpers, contracts)."""
from apcc import *

M = "cx-specs"

L1 = r"""
A helper method is a named decision. Exam problems rarely say "write a
helper" — they reward one anyway, because a well-named helper makes the
main method read like the specification itself.

*"Return true if the password is valid: at least 8 characters, and
either contains a digit or starts with an uppercase letter."*

```java
public static boolean hasDigit(String s) {
    for (int i = 0; i < s.length(); i++) {
        if (Character.isDigit(s.charAt(i))) {
            return true;
        }
    }
    return false;
}

public static boolean valid(String pw) {
    return pw.length() >= 8 && (hasDigit(pw) || startsUpper(pw));
}
```

The main method is now two lines and mirrors the English word-for-word.
Each helper is independently testable — and on the exam, independently
*traceable* when you must debug.

Helper design rules:

1. **One decision per helper.** If you cannot name it in one phrase, it
   is two helpers.
2. **Helpers return, they do not print.** Printing inside a helper makes
   it useless as a building block.
3. **The order you write them is the order you test them.** Write
   `hasDigit`, test it on `""`, `"abc"`, `"a1"`. Only then write `valid`.

The AP Java Quick Reference includes `Character.isDigit/isLetter` —
helpers around single-character classification are expected knowledge.
"""

L2 = r"""
**Preconditions** state what the caller promises; **postconditions**
state what the method guarantees. Reading them correctly is free points;
writing code that ignores them is the classic time sink.

```text
Precondition: scores.length >= 1
Postcondition: returns the highest score
```

What you may rely on: at least one element — so `best = scores[0]` is
safe, no empty check needed. What you must NOT add: a graceful empty
case. Code like `if (scores.length == 0) return 0;` is dead weight the
exam never asked for, and worse, it invents a contract (`0` for empty)
the caller never agreed to.

Conversely, when the spec says *"returns -1 if the value does not
appear"*, the -1 IS the contract. A student who instead throws an
exception or prints an error has rewritten the spec — automatic zero
even if the rest is perfect.

The three questions to ask of every spec:

1. What inputs are **promised** (preconditions)? → Skip guarding them.
2. What outputs are **guaranteed in every case** (postconditions)?
   Enumerate the cases: normal, boundary, absent.
3. What is **explicitly out of scope**? If it says "you may assume the
   array is sorted", do not sort it.
"""

L3 = r"""
Debugging a composition means isolating the lying part. Strategy: test
each helper against the contract **in isolation**, because a wrong
helper poisons everything downstream.

```java
// CONTRACT: number of words strictly longer than average length
public static int longWords(String[] words) {
    int sum = 0;
    for (String w : words) { sum += w.length(); }
    double avg = (double) sum / words.length;
    int count = 0;
    for (String w : words) {
        if (w.length() > avg) { count++; }
    }
    return count;
}
```

Trace `{""ab"", ""cd"", ""abcde""}`: sum = 2 + 2 + 5 = 9, avg = 3.0. Words
longer than 3.0: just `""abcde""` → 1. Both halves look right — the bug
(when present) is usually one of: integer division in `avg` (missing the
`(double)` cast → truncates to 3, same answer here but wrong for sum=8),
division by zero for an empty array (precondition violation — the spec
would promise non-empty), or the wrong comparison at the end.

The isolation habit: to test the average alone, return `avg` instead of
`count` once, run the case, restore. On the exam (no compiler), the
equivalent is tracing each helper once with a hand case where the
correct value is known — a 3-element trace exposes most compositional
bugs in under a minute.
"""

write_module(
    M,
    "Methods & Specification Problems",
    "Translating written specifications into minimal, correct methods: helper decomposition, precondition discipline, and compositional debugging.",
    "Phương thức & bài toán đặc tả",
    "Dịch đặc tả thành văn bản thành phương thức tối thiểu, đúng đắn: phân rã hàm trợ giúp, kỷ luật điều kiện tiên quyết, và gỡ lỗi tổ hợp.",
    lessons=["cx-m4-helpers", "cx-m4-preconditions", "cx-m4-debug-comp", "cx-cp-m4"],
    practices=["cx-p4-specs"],
)

write_lesson(
    M, "cx-m4-helpers", "Helpers as named decisions",
    "Decompose a spec into one-decision helpers that return, never print.",
    12, L1,
    "Hàm trợ giúp là quyết định có tên",
    "Tách đặc tả thành các hàm trợ giúp một-quyết-định, chỉ trả về, không in.",
    r"""
Hàm trợ giúp là một quyết định được đặt tên. Đề thi hiếm khi nói "hãy viết
hàm trợ giúp" — nhưng luôn thưởng cho người viết, vì một hàm trợ giúp đặt
tên tốt khiến phương thức chính đọc như chính đặc tả.

*"Trả về true nếu mật khẩu hợp lệ: ít nhất 8 ký tự, và hoặc chứa một chữ
số hoặc bắt đầu bằng chữ hoa."*

```java
public static boolean hasDigit(String s) {
    for (int i = 0; i < s.length(); i++) {
        if (Character.isDigit(s.charAt(i))) {
            return true;
        }
    }
    return false;
}

public static boolean valid(String pw) {
    return pw.length() >= 8 && (hasDigit(pw) || startsUpper(pw));
}
```

Phương thức chính giờ chỉ hai dòng và khớp với câu tiếng Anh từng chữ.
Mỗi hàm trợ giúp được kiểm thử độc lập — và khi thi, được *truy vết độc
lập* khi bạn phải gỡ lỗi.

Luật thiết kế hàm trợ giúp:

1. **Một quyết định mỗi hàm.** Nếu không gọi tên được trong một cụm từ,
   đó là hai hàm.
2. **Hàm trợ giúp trả về, không in.** In bên trong hàm trợ giúp khiến nó
   vô dụng như một khối xây dựng.
3. **Thứ tự viết là thứ tự kiểm thử.** Viết `hasDigit`, thử với `""`,
   `"abc"`, `"a1"`. Chỉ sau đó mới viết `valid`.

Bảng Java Quick Reference của AP có `Character.isDigit/isLetter` — các
hàm phân loại ký tự đơn là kiến thức được kỳ vọng.
""",
)

write_lesson(
    M, "cx-m4-preconditions", "Preconditions & postconditions",
    "Rely on what is promised; never invent cases the spec does not state.",
    10, L2,
    "Điều kiện tiên quyết & điều kiện sau",
    "Tin vào điều được hứa; không bao giờ bịa các trường hợp đề không nêu.",
    r"""
**Điều kiện tiên quyết (precondition)** nói điều người gọi hứa;
**điều kiện sau (postcondition)** nói điều phương thức đảm bảo. Đọc đúng
chúng là điểm miễn phí; viết mã phớt lờ chúng là cỗ máy tiêu thời gian
kinh điển.

```text
Điều kiện tiên quyết: scores.length >= 1
Điều kiện sau: trả về điểm cao nhất
```

Điều bạn được phép dựa vào: có ít nhất một phần tử — nên `best =
scores[0]` là an toàn, không cần kiểm tra mảng rỗng. Điều KHÔNG được làm:
thêm trường hợp mảng rỗng ân cần. Mã như `if (scores.length == 0) return
0;` là gánh nặng chết mà đề không hề yêu cầu, và tệ hơn, nó bịa ra một
hợp đồng (trả `0` khi rỗng) mà người gọi chưa từng đồng ý.

Ngược lại, khi đặc tả nói *"trả về -1 nếu giá trị không xuất hiện"*, thì
-1 CHÍNH LÀ hợp đồng. Học sinh thay vào đó ném ngoại lệ hay in lỗi đã tự
ý viết lại đề — điểm không dù phần còn lại hoàn hảo.

Ba câu hỏi cần hỏi mỗi đặc tả:

1. Đầu vào nào được **hứa** (preconditions)? → Đừng chặn chúng.
2. Đầu ra nào được **đảm bảo trong mọi trường hợp** (postconditions)?
   Liệt kê các trường hợp: bình thường, biên, vắng mặt.
3. Điều gì **nằm ngoài phạm vi**? Nếu đề nói "bạn được giả sử mảng đã
   sắp xếp", đừng đi sắp xếp nó.
""",
)

write_lesson(
    M, "cx-m4-debug-comp", "Debugging compositions",
    "Isolate each helper against its contract; trace where the poison enters.",
    12, L3,
    "Gỡ lỗi tổ hợp",
    "Tách từng hàm trợ giúp đối chiếu hợp đồng; truy vết chỗ độc lan vào.",
    r"""
Gỡ lỗi một tổ hợp nghĩa là cô lập phần đang nói dối. Chiến lược: kiểm
tra từng hàm trợ giúp với hợp đồng **một cách độc lập**, vì một hàm sai
sẽ đầu độc mọi thứ phía sau.

```java
// HỢP ĐỒNG: số từ dài hơn độ dài trung bình
public static int longWords(String[] words) {
    int sum = 0;
    for (String w : words) { sum += w.length(); }
    double avg = (double) sum / words.length;
    int count = 0;
    for (String w : words) {
        if (w.length() > avg) { count++; }
    }
    return count;
}
```

Truy vết `{"ab", "cd", "abcde"}`: sum = 2 + 2 + 5 = 9, avg = 3.0. Các từ
dài hơn 3.0: chỉ `{"abcde"}` → 1. Cả hai nửa đều đúng — lỗi (nếu có)
thường chỉ là một trong: chia nguyên trong `avg` (thiếu ép kiểu
`(double)` → cắt cụt thành 3), chia cho 0 khi mảng rỗng (vi phạm điều
kiện tiên quyết — đặc tả sẽ hứa mảng không rỗng), hoặc so sánh sai ở
bước cuối.

Thói quen cô lập: để kiểm thử riêng phần trung bình, hãy trả về `avg`
thay vì `count` một lần, chạy thử, rồi trả lại. Trong phòng thi (không
có trình biên dịch), tương đương là truy vết từng hàm trợ giúp một lần
với một trường hợp tay mà giá trị đúng đã biết — truy vết 3 phần tử phơi
ra phần lớn lỗi tổ hợp trong chưa tới một phút.
""",
)

BOILER_VALID = r"""public class Solution {
    public static boolean startsUpper(String s) {
        return s.length() > 0 && Character.isUpperCase(s.charAt(0));
    }

    public static boolean hasDigit(String s) {
        // replace: true when s contains at least one digit
        return false;
    }

    public static boolean valid(String pw) {
        // CONTRACT: at least 8 characters AND (has a digit OR starts
        // with an uppercase letter). startsUpper and hasDigit are given.
        return false; // replace
    }
}
"""

BOILER_MEDIAN = r"""public class Solution {
    // CONTRACT: median of arr, which is sorted ascending with
    // arr.length >= 1 (precondition). Odd length: middle element.
    // Even length: average of the two middle elements as a double.
    public static double median(int[] arr) {
        return 0; // replace
    }
}
"""

BOILER_LONGWORDS = r"""public class Solution {
    // CONTRACT: count of words STRICTLY longer than the average length.
    // Precondition: words.length >= 1.
    public static int longWords(String[] words) {
        int sum = 0;
        for (String w : words) {
            sum += w.length();
        }
        double avg = sum / words.length;   // BUG: integer division
        int count = 0;
        for (String w : words) {
            if (w.length() > avg) {
                count++;
            }
        }
        return count;
    }
}
"""

BOILER_REVERSE_IN_PLACE = r"""public class Solution {
    // CONTRACT: reverse arr IN PLACE (no new array); arr.length >= 1.
    public static void reverse(int[] arr) {
        // replace: swap symmetric pairs
    }
}
"""

BOILER_CLAMPIFY = r"""public class Solution {
    // CONTRACT: return the value clamped to [lo, hi]: below lo returns lo,
    // above hi returns hi, otherwise the value itself.
    public static int clamp(int value, int lo, int hi) {
        return value; // replace
    }
}
"""

BOILER_CP_SPEC = r"""public class Solution {
    // CONTRACT: count how many times the pattern "letter followed by
    // digit" appears in s. "a1b2" -> 2, "a12" -> 1, "" -> 0.
    public static int letterDigit(String s) {
        return 0; // replace
    }
}
"""

P_VALID = challenge(
    "cx-m4-valid-pw",
    "Compose from helpers",
    "Complete `hasDigit` (true when s contains at least one digit) and `valid` (length >= 8 AND (hasDigit OR startsUpper)). The helpers do the scanning; `valid` is one boolean expression.",
    BOILER_VALID,
    [(
        "password contract",
        r"""
CjTestBase.checkEq(Solution.hasDigit("abc1"), true, "has a digit");
CjTestBase.checkEq(Solution.hasDigit("abc"), false, "no digit");
CjTestBase.checkEq(Solution.hasDigit(""), false, "empty string");
CjTestBase.checkEq(Solution.valid("abcdefgh1"), true, "long enough with digit");
CjTestBase.checkEq(Solution.valid("Abcdefgh"), true, "long enough, starts upper");
CjTestBase.checkEq(Solution.valid("bcdefg1"), false, "too short (7 chars)");
CjTestBase.checkEq(Solution.valid("abcdefgh"), false, "long but no digit, no upper");
""",
        "valid: pw.length() >= 8 && (hasDigit(pw) || startsUpper(pw))",
    )],
    level="guided",
)

P_MEDIAN = challenge(
    "cx-m4-median",
    "Trust the precondition",
    "Implement `double median(int[] arr)` for a SORTED array (length >= 1 promised): odd length → middle element; even length → average of the two middle elements. The precondition means you may NOT need an empty check — but you DO need the parity case split.",
    BOILER_MEDIAN,
    [(
        "median cases",
        r"""
CjTestBase.checkNear(Solution.median(new int[]{5}), 5.0, 1e-9, "single element");
CjTestBase.checkNear(Solution.median(new int[]{1, 3, 8}), 3.0, 1e-9, "odd middle");
CjTestBase.checkNear(Solution.median(new int[]{2, 4}), 3.0, 1e-9, "even average");
CjTestBase.checkNear(Solution.median(new int[]{1, 2, 3, 10}), 2.5, 1e-9, "even average again");
""",
        "mid = arr.length / 2; odd → arr[mid]; even → (arr[mid-1] + arr[mid]) / 2.0",
    )],
    level="combination",
)

P_LONGWORDS = challenge(
    "cx-m4-fix-avg",
    "Fix the integer division",
    "`longWords` compiles and runs but fails `{\"a\", \"b\", \"cdef\"}`: average is 2.0, only \"cdef\" is strictly longer, expected 1 — check what the current code returns and why. Repair the one marked line.",
    BOILER_LONGWORDS,
    [(
        "strictly longer than average",
        r"""
CjTestBase.checkEq(Solution.longWords(new String[]{"a", "b", "cdef"}), 1, "avg 2.0, only cdef");
CjTestBase.checkEq(Solution.longWords(new String[]{"ab", "cd"}), 0, "avg 2.0, nothing strictly longer");
CjTestBase.checkEq(Solution.longWords(new String[]{"x"}), 0, "single word is never strictly longer than itself");
""",
        "(double) sum / words.length — cast BEFORE dividing.",
    )],
    level="debugging",
)

P_REVERSE = challenge(
    "cx-m4-reverse-in-place",
    "In-place reversal",
    "Implement `void reverse(int[] arr)`: reverse the array in place using swaps — no new array. Odd-length arrays have a untouched middle element. Trace {1,2,3,4} swap by hand: (0,3) then (1,2).",
    BOILER_REVERSE_IN_PLACE,
    [(
        "in place reversal",
        r"""
int[] a = {1, 2, 3, 4};
Solution.reverse(a);
CjTestBase.checkEq(a, new int[]{4, 3, 2, 1}, "even length reversed");
int[] b = {5, 6, 7};
Solution.reverse(b);
CjTestBase.checkEq(b, new int[]{7, 6, 5}, "odd length, middle untouched");
int[] c = {9};
Solution.reverse(c);
CjTestBase.checkEq(c, new int[]{9}, "single element");
""",
        "for i from 0 while i < arr.length / 2: swap arr[i] with arr[arr.length - 1 - i]",
    )],
    level="independent",
)

P_CLAMP = challenge(
    "cx-m4-clamp",
    "Three cases, one method",
    "Implement `int clamp(int value, int lo, int hi)`: below lo → lo, above hi → hi, otherwise value. Assume lo <= hi. The spec enumerates the cases; your job is to enumerate them in the right ORDER so no case is shadowed.",
    BOILER_CLAMPIFY,
    [(
        "clamped",
        r"""
CjTestBase.checkEq(Solution.clamp(5, 1, 10), 5, "inside stays");
CjTestBase.checkEq(Solution.clamp(-3, 1, 10), 1, "below clamps to lo");
CjTestBase.checkEq(Solution.clamp(99, 1, 10), 10, "above clamps to hi");
CjTestBase.checkEq(Solution.clamp(1, 1, 10), 1, "boundary is inclusive");
CjTestBase.checkEq(Solution.clamp(10, 1, 10), 10, "other boundary inclusive");
""",
        "if (value < lo) return lo; if (value > hi) return hi; return value;",
    )],
    level="imitation",
)

CP4 = challenge(
    "cx-cp-m4-letter-digit",
    "Checkpoint: adjacency contract",
    "Implement `int letterDigit(String s)`: count occurrences of a letter immediately followed by a digit. \"a1b2\" → 2, \"a12\" → 1 (the '1' after 'a' qualifies; the '2' after '1' does not), \"1a\" → 0, \"\" → 0. One pass, compare each character with its successor.",
    BOILER_CP_SPEC,
    [(
        "letter-digit pairs",
        r"""
CjTestBase.checkEq(Solution.letterDigit("a1b2"), 2, "two qualifying pairs");
CjTestBase.checkEq(Solution.letterDigit("a12"), 1, "only 'a1' qualifies");
CjTestBase.checkEq(Solution.letterDigit("1a"), 0, "wrong order");
CjTestBase.checkEq(Solution.letterDigit(""), 0, "empty string");
CjTestBase.checkEq(Solution.letterDigit("zz9"), 1, "last pair");
""",
        "Loop i from 0 to s.length() - 2: if isLetter(charAt(i)) && isDigit(charAt(i+1)) count++.",
    )],
    level="independent",
)

write_practice(
    M, "cx-p4-specs", "Specification workshop",
    "Compose helpers, honor preconditions, fix a cast, reverse in place.",
    "Xưởng đặc tả",
    "Ghép hàm trợ giúp, tôn trọng điều kiện tiên quyết, sửa phép chia, đảo chỗ.",
    after_lesson="cx-m4-preconditions", minutes=55, difficulty="intermediate",
    challenges=[P_VALID, P_MEDIAN, P_LONGWORDS, P_REVERSE, P_CLAMP],
    vi_challenges={
        "cx-m4-valid-pw": vi_challenge("Ghép từ hàm trợ giúp",
            "Hoàn thiện `hasDigit` (true khi s chứa ít nhất một chữ số) và `valid` (độ dài >= 8 VÀ (hasDigit HOẶC startsUpper)). Các hàm trợ giúp lo việc quét; `valid` chỉ là một biểu thức boolean.",
            [("password contract", "valid: pw.length() >= 8 && (hasDigit(pw) || startsUpper(pw))")]),
        "cx-m4-median": vi_challenge("Tin vào điều kiện tiên quyết",
            "Hiện thực `double median(int[] arr)` cho mảng ĐÃ SẮP XẾP (được hứa dài >= 1): lẻ → phần tử giữa; chẵn → trung bình hai phần tử giữa. Điều kiện tiên quyết nghĩa là KHÔNG cần kiểm tra rỗng — nhưng bạn PHẢI tách trường hợp chẵn/lẻ.",
            [("median cases", "mid = arr.length / 2; lẻ → arr[mid]; chẵn → (arr[mid-1] + arr[mid]) / 2.0")]),
        "cx-m4-fix-avg": vi_challenge("Sửa phép chia nguyên",
            "`longWords` chạy được nhưng sai với {\"a\", \"b\", \"cdef\"}: trung bình là 2.0, chỉ \"cdef\" dài hơn một cách nghiêm ngặt, kỳ vọng 1 — kiểm tra mã hiện tại trả về bao nhiêu và vì sao. Sửa đúng dòng được đánh dấu.",
            [("strictly longer than average", "(double) sum / words.length — ép kiểu TRƯỚC khi chia.")]),
        "cx-m4-reverse-in-place": vi_challenge("Đảo tại chỗ",
            "Hiện thực `void reverse(int[] arr)`: đảo ngược mảng ngay tại chỗ bằng các phép hoán đổi — không tạo mảng mới. Mảng lẻ có phần tử giữa nguyên vẹn. Truy vết {1,2,3,4} từng phép hoán đổi: (0,3) rồi (1,2).",
            [("in place reversal", "cho i chạy từ 0 đến arr.length / 2 - 1: hoán đổi arr[i] với arr[arr.length - 1 - i]")]),
        "cx-m4-clamp": vi_challenge("Ba trường hợp, một phương thức",
            "Hiện thực `int clamp(int value, int lo, int hi)`: dưới lo → lo, trên hi → hi, còn lại giữ nguyên. Giả sử lo <= hi. Đặc tả liệt kê các trường hợp; việc của bạn là liệt kê chúng theo ĐÚNG THỨ TỰ để không trường hợp nào bị che khuất.",
            [("clamped", "if (value < lo) return lo; if (value > hi) return hi; return value;")]),
    },
    solutions=[
        ("cx-m4-valid-pw",
         BOILER_VALID.replace("        // replace: true when s contains at least one digit\n        return false;",
            "        for (int i = 0; i < s.length(); i++) {\n            if (Character.isDigit(s.charAt(i))) {\n                return true;\n            }\n        }\n        return false;")
            .replace("        return false; // replace",
                "        return pw.length() >= 8 && (hasDigit(pw) || startsUpper(pw));"),
         BOILER_VALID.replace("        return false; // replace",
                "        return pw.length() > 8 && (hasDigit(pw) || startsUpper(pw));")),
        ("cx-m4-median", BOILER_MEDIAN.replace("return 0; // replace",
            "int mid = arr.length / 2;\n        if (arr.length % 2 == 1) {\n            return arr[mid];\n        }\n        return (arr[mid - 1] + arr[mid]) / 2.0;"),
         BOILER_MEDIAN.replace("return 0; // replace",
            "int mid = arr.length / 2;\n        if (arr.length % 2 == 1) {\n            return arr[mid];\n        }\n        return (arr[mid - 1] + arr[mid]) / 2;")),
        ("cx-m4-fix-avg", BOILER_LONGWORDS.replace("double avg = sum / words.length;   // BUG: integer division",
            "double avg = (double) sum / words.length;"),
         BOILER_LONGWORDS.replace("double avg = sum / words.length;   // BUG: integer division",
            "double avg = sum / (words.length + 1);")),
        ("cx-m4-reverse-in-place",
         r"""public class Solution {
    public static void reverse(int[] arr) {
        for (int i = 0; i < arr.length / 2; i++) {
            int tmp = arr[i];
            arr[i] = arr[arr.length - 1 - i];
            arr[arr.length - 1 - i] = tmp;
        }
    }
}
""",
         r"""public class Solution {
    public static void reverse(int[] arr) {
        for (int i = 0; i <= arr.length / 2; i++) {
            int tmp = arr[i];
            arr[i] = arr[arr.length - 1 - i];
            arr[arr.length - 1 - i] = tmp;
        }
    }
}
"""),
        ("cx-m4-clamp", BOILER_CLAMPIFY.replace("return value; // replace",
            "if (value < lo) {\n            return lo;\n        }\n        if (value > hi) {\n            return hi;\n        }\n        return value;"),
         BOILER_CLAMPIFY.replace("return value; // replace",
            "if (value <= lo) {\n            return lo + 1;\n        }\n        if (value > hi) {\n            return hi;\n        }\n        return value;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m4", "Checkpoint: one pass, adjacency",
    "Letter-followed-by-digit counting from a precise contract.",
    20,
    r"""
The checkpoint method compares each character with its successor — the
same adjacency shape you will reuse for runs, duplicates, and neighbor
logic in arrays. Note the off-by-one discipline: the loop runs to
`length - 2` precisely because it reads `i + 1`. Next module: the same
one-pass discipline on the String API itself.
""",
    "Điểm kiểm tra: một lượt, tính liền kề",
    "Đếm chữ-cái-đứng-cạnh-chữ-số từ một hợp đồng chính xác.",
    r"""
Phương thức kiểm tra so sánh mỗi ký tự với ký tự kế tiếp — cùng hình dạng
tính liền kề mà bạn sẽ tái sử dụng cho đoạn, trùng lặp, và logic hàng xóm
trong mảng. Chú ý kỷ luật lệch-một: vòng lặp chạy đến `length - 2` chính
vì nó đọc `i + 1`. Module sau: cùng kỷ luật một-lượt áp dụng lên chính API
String.
""",
    CP4,
    vi_challenge("Điểm kiểm tra: một lượt, tính liền kề",
        "Hiện thực `int letterDigit(String s)`: đếm các lần một chữ cái đứng ngay trước một chữ số. \"a1b2\" → 2, \"a12\" → 1 (chỉ 'a1' đạt), \"1a\" → 0, \"\" → 0. Một lượt quét, so sánh mỗi ký tự với ký tự kế tiếp.",
        [("letter-digit pairs", "Vòng lặp i từ 0 đến s.length() - 2: nếu isLetter(charAt(i)) && isDigit(charAt(i+1)) thì đếm.")]),
    solution=r"""public class Solution {
    public static int letterDigit(String s) {
        int count = 0;
        for (int i = 0; i <= s.length() - 2; i++) {
            if (Character.isLetter(s.charAt(i)) && Character.isDigit(s.charAt(i + 1))) {
                count++;
            }
        }
        return count;
    }
}
""",
    wrong=r"""public class Solution {
    public static int letterDigit(String s) {
        int count = 0;
        for (int i = 0; i <= s.length() - 2; i++) {
            if (Character.isDigit(s.charAt(i)) && Character.isLetter(s.charAt(i + 1))) {
                count++;
            }
        }
        return count;
    }
}
""",
)
