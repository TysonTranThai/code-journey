#!/usr/bin/env python3
"""AP CSA Core M5 — String Problem Solving (Quick Reference API only)."""
from apcc import *

M = "cx-strings"

L1 = r"""
Everything on the exam uses the Java Quick Reference String subset:
`length`, `substring` (1- and 2-arg), `charAt`, `indexOf`, `equals`,
`compareTo`. Mastery means knowing their **edge behavior**, not their
definitions.

**substring's end is exclusive.** `"abcdef".substring(2, 5)` is `"cde"` —
indexes 2, 3, 4. The length of `substring(a, b)` is exactly `b - a`.
That single fact answers a whole family of exam questions.

**The empty case.** `"".substring(0)` is `""`; `s.substring(s.length())`
is `""` (legal!); but `s.substring(s.length() + 1)` throws
`StringIndexOutOfBoundsException`. The legal-but-surprising
`s.substring(s.length())` returning `""` is a favorite MCQ answer.

**indexOf returns -1 when absent, 0 when prefix.** `"abc".indexOf("bc")`
is 1; `"abc".indexOf("d")` is -1; `"abc".indexOf("")` is 0. And
`s.indexOf(x)` searching again after a hit needs a start index — the
1-arg form always returns the *first*.

**compareTo decides order.** Negative → `s` comes first; 0 → equal
content; positive → `s` comes second. Used for alphabetical ordering
("which string is earlier?") — never for equality (`==` compares
references and is wrong even when it sometimes looks right).
"""

L2 = r"""
String building follows the accumulator machine with two dialects:

**Filter — keep matching characters.**

```java
String out = "";
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (Character.isLetter(c)) {
        out += c;
    }
}
```

**Map — transform every character** (e.g. every letter to uppercase by
hand, without `toUpperCase`):

```java
String out = "";
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (c >= 'a' && c <= 'z') {
        out += (char) (c - 'a' + 'A');
    } else {
        out += c;
    }
}
```

The `(char)` cast matters: `c - 'a'` is an `int` arithmetic distance
(0–25); adding `'A'` converts the distance back to a code. Trace
`'c'`: `'c' - 'a'` = 2, `'A' + 2` = `'C'`.

**Split-by-index — substring inside a loop.**

```java
// first vowel run, or the whole word if none
int at = -1;
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
        at = i;
        break;
    }
}
String head = (at == -1) ? s : s.substring(0, at);
```

Common trap: `charAt(i)` after the loop ends — the index is dead there.
Store the answer inside the loop (like `at`), never index past the end.
"""

L3 = r"""
Two-pointer problems are the exam's String FRQ heart. Model: one index
from the front, one from the back, meeting in the middle.

*"Is s a palindrome, considering letters only?"* — the filter + two
pointers combined:

```java
public static boolean isPal(String s) {
    int lo = 0, hi = s.length() - 1;
    while (lo < hi) {
        if (!Character.isLetter(s.charAt(lo))) { lo++; }
        else if (!Character.isLetter(s.charAt(hi))) { hi--; }
        else if (s.charAt(lo) != s.charAt(hi)) { return false; }
        else { lo++; hi--; }
    }
    return true;
}
```

Trace `"a, b a"` (a comma, a space, letters a b a): lo=0 'a' vs hi=5 'a'
match; lo=1 ',' skipped (lo++); lo=2 ' ' skipped; lo=3 'b' vs hi=4 'b'
match; lo=4, hi=3 → loop ends, true. Notice the loop condition `lo < hi`
— crossed pointers mean success, and single-character strings are
trivially palindromes (0 < 0 is false immediately).

The second classic: **run-length counting** — count runs of equal
adjacent characters:

```java
public static int runs(String s) {
    if (s.length() == 0) { return 0; }
    int count = 1;
    for (int i = 1; i < s.length(); i++) {
        if (s.charAt(i) != s.charAt(i - 1)) {
            count++;
        }
    }
    return count;
}
```

`"aabbbca"` → runs a|bb|c|a = 4. Start at 1 (the first character always
opens a run); increment at every boundary. The precondition `length >= 1`
is what lets you seed `count = 1` — remove it and the empty string
breaks you.
"""

write_module(
    M,
    "String Problem Solving",
    "The Quick Reference API's edge behavior, character-level building (filter, map, split), and two-pointer patterns.",
    "Giải quyết vấn đề với chuỗi",
    "Hành vi biên của API trong Quick Reference, dựng chuỗi theo ký tự (lọc, biến đổi, tách), và mẫu hai con trỏ.",
    lessons=["cx-m5-api", "cx-m5-building", "cx-m5-twopoint", "cx-cp-m5"],
    practices=["cx-p5-strings"],
)

write_lesson(
    M, "cx-m5-api", "The API's edge behavior",
    "substring exclusivity, legal empty substrings, indexOf conventions, compareTo.",
    12, L1,
    "Hành vi biên của API",
    "Tính độc quyền của substring, substring rỗng hợp lệ, quy ước indexOf, compareTo.",
    r"""
Mọi thứ trong đề thi đều dùng tập con String trong Java Quick Reference:
`length`, `substring` (1 và 2 tham số), `charAt`, `indexOf`, `equals`,
`compareTo`. Làm chủ nghĩa là biết **hành vi biên** của chúng, không phải
định nghĩa.

**substring có mép cuối độc quyền.** `"abcdef".substring(2, 5)` là
`"cde"` — các chỉ số 2, 3, 4. Độ dài của `substring(a, b)` đúng bằng
`b - a`. Một sự thật duy nhất đó trả lời cả một họ câu hỏi thi.

**Trường hợp rỗng.** `"".substring(0)` là `""`; `s.substring(s.length())`
là `""` (hợp lệ!); nhưng `s.substring(s.length() + 1)` ném
`StringIndexOutOfBoundsException`. Cái hợp-lệc-nhưng-bất-ngờ
`s.substring(s.length())` trả về `""` là đáp án MCQ ưa thích.

**indexOf trả về -1 khi vắng mặt, 0 khi là tiền tố.**
`"abc".indexOf("bc")` là 1; `"abc".indexOf("d")` là -1;
`"abc".indexOf("")` là 0. Và để tìm tiếp sau một lần trúng, cần dạng có
chỉ số xuất phát — dạng 1 tham số luôn trả về lần *đầu*.

**compareTo quyết định thứ tự.** Âm → `s` đứng trước; 0 → nội dung bằng
nhau; dương → `s` đứng sau. Dùng cho thứ tự chữ cái ("chuỗi nào đứng
trước?") — không bao giờ dùng cho đẳng giá trị (`==` so tham chiếu và là
sai ngay cả khi đôi khi trông đúng).
""",
)

write_lesson(
    M, "cx-m5-building", "Building strings by character",
    "Filter, map, and split-by-index patterns with char arithmetic.",
    12, L2,
    "Dựng chuỗi theo ký tự",
    "Các mẫu lọc, biến đổi, tách-theo-chỉ-số với số học ký tự.",
    r"""
Dựng chuỗi theo đúng cỗ máy cộng dồn, với hai phương ngữ:

**Lọc — giữ các ký tự khớp.**

```java
String out = "";
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (Character.isLetter(c)) {
        out += c;
    }
}
```

**Biến đổi — đổi mỗi ký tự** (ví dụ mọi chữ thường thành chữ hoa bằng
tay, không dùng `toUpperCase`):

```java
String out = "";
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (c >= 'a' && c <= 'z') {
        out += (char) (c - 'a' + 'A');
    } else {
        out += c;
    }
}
```

Phép ép `(char)` rất quan trọng: `c - 'a'` là một khoảng cách số học
`int` (0–25); cộng `'A'` biến khoảng cách về lại mã ký tự. Truy vết
`'c'`: `'c' - 'a'` = 2, `'A' + 2` = `'C'`.

**Tách-theo-chỉ-số — substring trong vòng lặp.**

```java
// phần trước nguyên âm đầu tiên, hoặc cả từ nếu không có
int at = -1;
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
        at = i;
        break;
    }
}
String head = (at == -1) ? s : s.substring(0, at);
```

Bẫy thường gặp: `charAt(i)` sau khi vòng lặp kết thúc — chỉ số đã chết ở
đó. Hãy lưu đáp án bên trong vòng lặp (như `at`), đừng bao giờ truy cập
vượt quá cuối chuỗi.
""",
)

write_lesson(
    M, "cx-m5-twopoint", "Two pointers on strings",
    "Palindrome with a filter and run counting — the FRQ workhorses.",
    12, L3,
    "Hai con trỏ trên chuỗi",
    "Palindrome kèm bộ lọc và đếm đoạn — hai con ngựa thồ của FRQ.",
    r"""
Bài toán hai con trỏ là trái tim của phần FRQ về String. Mô hình: một chỉ
số từ đầu, một từ cuối, gặp nhau ở giữa.

*"s có phải palindrome khi chỉ tính các chữ cái?"* — kết hợp bộ lọc và
hai con trỏ:

```java
public static boolean isPal(String s) {
    int lo = 0, hi = s.length() - 1;
    while (lo < hi) {
        if (!Character.isLetter(s.charAt(lo))) { lo++; }
        else if (!Character.isLetter(s.charAt(hi))) { hi--; }
        else if (s.charAt(lo) != s.charAt(hi)) { return false; }
        else { lo++; hi--; }
    }
    return true;
}
```

Truy vết `"a, b a"` (một dấu phẩy, một dấu cách, các chữ a b a): lo=0 'a'
đối hi=5 'a' khớp; lo=1 ',' bị bỏ qua (lo++); lo=2 ' ' bị bỏ qua; lo=3
'b' đối hi=4 'b' khớp; lo=4, hi=3 → vòng lặp kết thúc, true. Chú ý điều
kiện `lo < hi` — hai con trỏ đi chéo nhau nghĩa là thành công, và chuỗi
một ký tự là palindrome hiển nhiên (0 < 0 sai ngay).

Kinh điển thứ hai: **đếm đoạn (run-length)** — đếm các đoạn ký tự liền
kề bằng nhau:

```java
public static int runs(String s) {
    if (s.length() == 0) { return 0; }
    int count = 1;
    for (int i = 1; i < s.length(); i++) {
        if (s.charAt(i) != s.charAt(i - 1)) {
            count++;
        }
    }
    return count;
}
```

`"aabbbca"` → các đoạn a|bb|c|a = 4. Bắt đầu từ 1 (ký tự đầu luôn mở một
đoạn); tăng lên tại mỗi biên. Điều kiện tiên quyết `length >= 1` chính
là thứ cho phép seed `count = 1` — bỏ nó đi và chuỗi rỗng sẽ đánh sập
bạn.
""",
)

BOILER_SUB = r"""public class Solution {
    public static String firstHalf(String s) {
        // CONTRACT: first half of s; for odd lengths, the EXTRA character
        // goes to the second half. "abcd" -> "ab", "abcde" -> "ab".
        return ""; // replace
    }
}
"""

BOILER_FILTER = r"""public class Solution {
    public static String digitsOnly(String s) {
        // CONTRACT: a new string containing only the digit characters
        // of s, in order. "a1b2c3" -> "123", "abc" -> "", "" -> "".
        return ""; // replace
    }
}
"""

BOILER_MAPUP = r"""public class Solution {
    public static String shout(String s) {
        // CONTRACT: like s but every lowercase letter a-z uppercased;
        // other characters unchanged. No toUpperCase allowed.
        return s; // replace
    }
}
"""

BOILER_RUNSBAD = r"""public class Solution {
    // CONTRACT: number of runs of equal adjacent characters.
    // "aabbbca" -> 4. Precondition: s.length() >= 1.
    public static int runs(String s) {
        int count = 0;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) != s.charAt(i - 1)) {
                count++;
            }
        }
        return count;
    }
}
"""

BOILER_CONTAINS_ONCE = r"""public class Solution {
    // CONTRACT: true when the word appears in text EXACTLY once.
    public static boolean occursOnce(String text, String word) {
        // replace: use indexOf twice
        return false;
    }
}
"""

BOILER_CP_STR = r"""public class Solution {
    // CONTRACT: compress runs: "aabbbca" -> "abca". Precondition:
    // s.length() >= 1.
    public static String compress(String s) {
        return ""; // replace
    }
}
"""

P_HALVES = challenge(
    "cx-m5-first-half",
    "substring arithmetic",
    "Implement `String firstHalf(String s)`: the first half, with the extra character going to the second half on odd lengths. Derive the index from the length formula — no loops needed.",
    BOILER_SUB,
    [(
        "half by length",
        r"""
CjTestBase.checkEq(Solution.firstHalf("abcd"), "ab", "even split");
CjTestBase.checkEq(Solution.firstHalf("abcde"), "ab", "odd: extra char to second half");
CjTestBase.checkEq(Solution.firstHalf("a"), "", "single char: first half empty");
CjTestBase.checkEq(Solution.firstHalf(""), "", "empty string");
""",
        "s.substring(0, s.length() / 2)",
    )],
    level="imitation",
)

P_FILTER = challenge(
    "cx-m5-digits-only",
    "Filter digits",
    "Implement `String digitsOnly(String s)`: keep only the digit characters, in order. One accumulator loop with `Character.isDigit`.",
    BOILER_FILTER,
    [(
        "digits kept",
        r"""
CjTestBase.checkEq(Solution.digitsOnly("a1b2c3"), "123", "digits in order");
CjTestBase.checkEq(Solution.digitsOnly("abc"), "", "no digits");
CjTestBase.checkEq(Solution.digitsOnly(""), "", "empty input");
CjTestBase.checkEq(Solution.digitsOnly("2026"), "2026", "all digits survive");
""",
        "if (Character.isDigit(c)) { out += c; }",
    )],
    level="guided",
)

P_SHOUT = challenge(
    "cx-m5-shout",
    "Map with char arithmetic",
    "Implement `String shout(String s)`: uppercase every lowercase letter using char arithmetic (no `toUpperCase`), leaving everything else untouched. Trace 'c' → 2 → 'C' before coding.",
    BOILER_MAPUP,
    [(
        "mapped to upper",
        r"""
CjTestBase.checkEq(Solution.shout("cat"), "CAT", "three shifts");
CjTestBase.checkEq(Solution.shout("a1!z"), "A1!Z", "digits and punctuation untouched");
CjTestBase.checkEq(Solution.shout(""), "", "empty");
CjTestBase.checkEq(Solution.shout("B2b"), "B2B", "already-upper stays");
""",
        "if (c >= 'a' && c <= 'z') out += (char)(c - 'a' + 'A'); else out += c;",
    )],
    level="combination",
)

P_RUNSBAD = challenge(
    "cx-m5-fix-runs",
    "Fix the run counter",
    "`runs` returns 3 for \"aabbbca\" but the contract says 4. Trace the loop with a state table (i, charAt(i), count) and find the seeding error — the precondition allows the fix.",
    BOILER_RUNSBAD,
    [(
        "runs counted",
        r"""
CjTestBase.checkEq(Solution.runs("aabbbca"), 4, "a|bb|c|a");
CjTestBase.checkEq(Solution.runs("aaaa"), 1, "one long run");
CjTestBase.checkEq(Solution.runs("ab"), 2, "two runs");
CjTestBase.checkEq(Solution.runs("z"), 1, "single char, single run");
""",
        "The first character OPENS run #1: seed count = 1, count boundaries from i=1.",
    )],
    level="debugging",
)

P_ONCE = challenge(
    "cx-m5-occurs-once",
    "indexOf, twice",
    "Implement `boolean occursOnce(String text, String word)`: true when word appears in text exactly once. Use `indexOf` twice — the second call needs the start index form.",
    BOILER_CONTAINS_ONCE,
    [(
        "exactly one occurrence",
        r"""
CjTestBase.checkEq(Solution.occursOnce("ab cd ab", "cd"), true, "one cd");
CjTestBase.checkEq(Solution.occursOnce("ab cd ab", "ab"), false, "two abs");
CjTestBase.checkEq(Solution.occursOnce("nothing here", "xy"), false, "zero occurrences");
CjTestBase.checkEq(Solution.occursOnce("solo", "solo"), true, "single full match");
""",
        "first = text.indexOf(word); if (first < 0) return false; return text.indexOf(word, first + 1) < 0;",
    )],
    level="independent",
)

CP5 = challenge(
    "cx-cp-m5-compress",
    "Checkpoint: run compression",
    "Implement `String compress(String s)`: collapse each run of equal adjacent characters to one copy (\"aabbbca\" → \"abca\"). Combine the run-boundary idea with the string accumulator; keep the first character unconditionally.",
    BOILER_CP_STR,
    [(
        "runs compressed",
        r"""
CjTestBase.checkEq(Solution.compress("aabbbca"), "abca", "runs collapse");
CjTestBase.checkEq(Solution.compress("aaaa"), "a", "one run, one char");
CjTestBase.checkEq(Solution.compress("abc"), "abc", "no repeats");
CjTestBase.checkEq(Solution.compress("z"), "z", "single character");
""",
        "Seed out with s.charAt(0); append s.charAt(i) only when it differs from s.charAt(i-1).",
    )],
    level="independent",
)

write_practice(
    M, "cx-p5-strings", "String lab",
    "substring math, filters, char maps, run counting, and double indexOf.",
    "Phòng chuỗi",
    "Phép toán substring, bộ lọc, biến đổi ký tự, đếm đoạn, và indexOf kép.",
    after_lesson="cx-m5-building", minutes=55, difficulty="intermediate",
    challenges=[P_HALVES, P_FILTER, P_SHOUT, P_RUNSBAD, P_ONCE],
    vi_challenges={
        "cx-m5-first-half": vi_challenge("Phép toán substring",
            "Hiện thực `String firstHalf(String s)`: nửa đầu, với ký tự thừa thuộc về nửa sau khi độ dài lẻ. Suy ra chỉ số từ công thức độ dài — không cần vòng lặp.",
            [("half by length", "s.substring(0, s.length() / 2)")]),
        "cx-m5-digits-only": vi_challenge("Lọc chữ số",
            "Hiện thực `String digitsOnly(String s)`: giữ lại chỉ các ký tự chữ số, theo thứ tự. Một vòng lặp cộng dồn với `Character.isDigit`.",
            [("digits kept", "if (Character.isDigit(c)) { out += c; }")]),
        "cx-m5-shout": vi_challenge("Biến đổi bằng số học ký tự",
            "Hiện thực `String shout(String s)`: hoa hóa mọi chữ thường bằng số học ký tự (không dùng `toUpperCase`), giữ nguyên phần còn lại. Truy vết 'c' → 2 → 'C' trước khi viết mã.",
            [("mapped to upper", "if (c >= 'a' && c <= 'z') out += (char)(c - 'a' + 'A'); else out += c;")]),
        "cx-m5-fix-runs": vi_challenge("Sửa bộ đếm đoạn",
            "`runs` trả về 3 cho \"aabbbca\" nhưng hợp đồng nói 4. Truy vết vòng lặp bằng bảng trạng thái (i, charAt(i), count) và tìm lỗi seed — điều kiện tiên quyết cho phép bạn sửa.",
            [("runs counted", "Ký tự đầu MỞ đoạn #1: seed count = 1, đếm biên từ i=1.")]),
        "cx-m5-occurs-once": vi_challenge("indexOf, hai lần",
            "Hiện thực `boolean occursOnce(String text, String word)`: true khi word xuất hiện trong text đúng một lần. Dùng `indexOf` hai lần — lần thứ hai cần dạng có chỉ số xuất phát.",
            [("exactly one occurrence", "first = text.indexOf(word); nếu first < 0 trả false; rồi kiểm tra text.indexOf(word, first + 1) < 0.")]),
    },
    solutions=[
        ("cx-m5-first-half", BOILER_SUB.replace("return \"\"; // replace",
            "return s.substring(0, s.length() / 2);"),
         BOILER_SUB.replace("return \"\"; // replace",
            "return s.substring(0, (s.length() + 1) / 2);")),
        ("cx-m5-digits-only", BOILER_FILTER.replace("return \"\"; // replace",
            "String out = \"\";\n        for (int i = 0; i < s.length(); i++) {\n            if (Character.isDigit(s.charAt(i))) {\n                out += s.charAt(i);\n            }\n        }\n        return out;"),
         BOILER_FILTER.replace("return \"\"; // replace",
            "String out = \"\";\n        for (int i = 0; i < s.length(); i++) {\n            if (!Character.isDigit(s.charAt(i))) {\n                out += s.charAt(i);\n            }\n        }\n        return out;")),
        ("cx-m5-shout", BOILER_MAPUP.replace("return s; // replace",
            "String out = \"\";\n        for (int i = 0; i < s.length(); i++) {\n            char c = s.charAt(i);\n            if (c >= 'a' && c <= 'z') {\n                out += (char) (c - 'a' + 'A');\n            } else {\n                out += c;\n            }\n        }\n        return out;"),
         BOILER_MAPUP.replace("return s; // replace",
            "String out = \"\";\n        for (int i = 0; i < s.length(); i++) {\n            char c = s.charAt(i);\n            if (c >= 'A' && c <= 'Z') {\n                out += (char) (c - 'A' + 'a');\n            } else {\n                out += c;\n            }\n        }\n        return out;")),
        ("cx-m5-fix-runs", BOILER_RUNSBAD.replace("int count = 0;", "int count = 1;"),
         BOILER_RUNSBAD.replace("int count = 0;", "int count = 0;").replace(
             "if (s.charAt(i) != s.charAt(i - 1)) {", "if (s.charAt(i) == s.charAt(i - 1)) {")),
        ("cx-m5-occurs-once", BOILER_CONTAINS_ONCE.replace("        // replace: use indexOf twice\n        return false;",
            "        int first = text.indexOf(word);\n        if (first < 0) { return false; }\n        return text.indexOf(word, first + 1) < 0;"),
         BOILER_CONTAINS_ONCE.replace("        // replace: use indexOf twice\n        return false;",
            "        int first = text.indexOf(word);\n        return first >= 0;")),
    ],
)

write_checkpoint(
    M, "cx-cp-m5", "Checkpoint: collapse the runs",
    "Run compression fusing boundary detection with the string accumulator.",
    20,
    r"""
compress is runs-as-a-string: same boundary test, same seed-from-first
element, but the accumulator builds text instead of a number. Students
who can produce this on demand own the adjacency-plus-accumulator
pattern that half of all String FRQs reduce to. Next module: the same
machines aimed at arrays.
""",
    "Điểm kiểm tra: nén các đoạn",
    "Nén đoạn, kết hợp phát hiện biên với bộ cộng dồn chuỗi.",
    r"""
compress chính là runs-phiên-bản-chuỗi: cùng phép kiểm tra biên, cùng
seed từ phần tử đầu, nhưng bộ cộng dồn dựng văn bản thay vì con số. Ai
tự tay viết ra được bài này là đã làm chủ mẫu liền-kề-cộng-với-cộng-dồn
mà một nửa các FRQ về String quy về. Module sau: các cỗ máy ấy nhắm vào
mảng.
""",
    CP5,
    vi_challenge("Điểm kiểm tra: nén các đoạn",
        "Hiện thực `String compress(String s)`: gộp mỗi đoạn ký tự liền kề bằng nhau thành một bản sao (\"aabbbca\" → \"abca\"). Kết hợp ý tưởng biên đoạn với bộ cộng dồn chuỗi; giữ ký tự đầu vô điều kiện.",
        [("runs compressed", "Seed out bằng s.charAt(0); chỉ thêm s.charAt(i) khi nó khác s.charAt(i-1).")]),
    solution=r"""public class Solution {
    public static String compress(String s) {
        String out = "" + s.charAt(0);
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) != s.charAt(i - 1)) {
                out += s.charAt(i);
            }
        }
        return out;
    }
}
""",
    wrong=r"""public class Solution {
    public static String compress(String s) {
        String out = "";
        for (int i = 0; i < s.length(); i++) {
            if (i == 0 || s.charAt(i) != s.charAt(i - 1)) {
                out += "" + s.length();
            }
        }
        return out;
    }
}
""",
)
