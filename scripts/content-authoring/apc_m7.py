#!/usr/bin/env python3
"""AP CSA M7 — Strings (API subset, traversal, == vs equals, FRQ patterns)."""
from apc import *

M = "apc-strings"

L1 = r"""
A `String` is an **object** — the first one you use. You never create it
with `new` in exam code; a literal is fine:

```java
String name = "Minh";
```

The exam's official method set (the Java Quick Reference list):

```java
name.length()          // 4
name.substring(1)      // "inh"  — from index 1 to the end
name.substring(1, 3)   // "in"   — index 1,2 (end index EXCLUDED)
name.charAt(0)         // 'M'   — returns a char, not a String
name.indexOf("i")      // 1     — first position, -1 when absent
name.equals("Minh")    // true
name.compareTo("Nam")  // <0 — "Minh" sorts before "Nam"
```

**Index rules**: valid positions are `0` through `length() - 1`. Out of
range → `StringIndexOutOfBoundsException` at runtime. For `substring(lo,
hi)`: `lo` may equal `length()` (empty result), but `hi` may not exceed it.

**Immutability**: String methods never change the string — they *return
new* ones. `name.toUpperCase()` alone does nothing; you must store it:
`name = name.toUpperCase();`
"""

L2 = r"""
The most exam-famous String trap:

```java
String a = "cat";
String b = new String("cat");
System.out.println(a == b);        // false! == compares references
System.out.println(a.equals(b));   // true  — content comparison
```

`==` asks "same object?"; `.equals` asks "same characters?". **Always use
`.equals` for String content.** (`compareTo` returns 0 exactly when equals
is true — it also tells you *ordering*, which `==`/`equals` cannot.)

**Traversal patterns** — memorize all three, the exam cycles through them:

```java
// 1. by index (when you need the position)
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
}

// 2. substring walk (when you need neighboring pieces)
for (int i = 0; i + 1 < s.length(); i++) {
    String pair = s.substring(i, i + 2);
}

// 3. first-to-last scan with early exit
int pos = s.indexOf('x');
if (pos != -1) { /* found */ }
```

Concatenation builds new strings: `"ab" + "cd"`, `s + 42`, `42 + s` all work
— numbers convert automatically.
"""

L3 = r"""
FRQ Question 1 Part B says: "the method requires calling String methods."
The recurring shapes:

**Count characters matching a rule:**

```java
public static int countChar(String s, char target) {
    int count = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == target) {
            count++;
        }
    }
    return count;
}
```

**Extract or transform pieces:**

```java
public static String firstHalf(String s) {
    return s.substring(0, s.length() / 2);
}
```

**Reverse by building backwards:**

```java
public static String reverse(String s) {
    String out = "";
    for (int i = s.length() - 1; i >= 0; i--) {
        out += s.charAt(i);
    }
    return out;
}
```

**Check a property of every character** (all digits? any uppercase?) — the
early-exit pattern:

```java
public static boolean allDigits(String s) {
    for (int i = 0; i < s.length(); i++) {
        if (!Character.isDigit(s.charAt(i))) {
            return false;
        }
    }
    return true;    // only reached when nothing failed
}
```

Notice `return true` lives *after* the loop: it is the "survived every test"
case, not a special input.
"""

write_module(
    M,
    "Strings",
    "The exam's String method set, immutability, == vs equals, traversal patterns, and FRQ-style string methods.",
    "Chuỗi (String)",
    "Bộ phương thức String của đề thi, tính bất biến, == so với equals, các mẫu duyệt, và phương thức xử lý chuỗi kiểu FRQ.",
    lessons=["apc-m7-api", "apc-m7-equals", "apc-m7-frq", "apc-cp-m7"],
    practices=["apc-p7-strings"],
)

write_lesson(
    M, "apc-m7-api", "The String API you may use",
    "length, substring, charAt, indexOf, compareTo; index bounds; immutability.",
    14, L1,
    "Bộ API String được phép dùng",
    "length, substring, charAt, indexOf, compareTo; biên chỉ số; tính bất biến.",
    r"""
`String` là một **đối tượng** — đối tượng đầu tiên bạn dùng. Trong code đề
thi bạn không tạo nó bằng `new`; một literal là đủ:

```java
String name = "Minh";
```

Bộ phương thức chính thức của đề thi (danh sách Java Quick Reference):

```java
name.length()          // 4
name.substring(1)      // "inh"  — từ chỉ số 1 đến hết
name.substring(1, 3)   // "in"   — chỉ số 1,2 (chỉ số cuối KHÔNG gồm)
name.charAt(0)         // 'M'   — trả về char, không phải String
name.indexOf("i")      // 1     — vị trí đầu, -1 khi không có
name.equals("Minh")    // true
name.compareTo("Nam")  // <0 — "Minh" xếp trước "Nam"
```

**Luật chỉ số**: vị trí hợp lệ là `0` đến `length() - 1`. Ngoài khoảng →
`StringIndexOutOfBoundsException` khi chạy. Với `substring(lo, hi)`: `lo`
được phép bằng `length()` (kết quả rỗng), nhưng `hi` không được vượt quá.

**Bất biến**: các phương thức String không bao giờ đổi chuỗi — chúng *trả về
chuỗi mới*. Riêng `name.toUpperCase()` chẳng làm gì cả; bạn phải lưu lại:
`name = name.toUpperCase();`
""",
)

write_lesson(
    M, "apc-m7-equals", "== vs equals, and traversal",
    "Reference vs content comparison, compareTo ordering, three loop shapes.",
    12, L2,
    "== so với equals, và duyệt chuỗi",
    "So sánh tham chiếu so với nội dung, thứ tự compareTo, ba dạng vòng lặp.",
    r"""
Cái bẫy String nổi tiếng nhất đề thi:

```java
String a = "cat";
String b = new String("cat");
System.out.println(a == b);        // false! == so sánh tham chiếu
System.out.println(a.equals(b));   // true  — so sánh nội dung
```

`==` hỏi "cùng một đối tượng?"; `.equals` hỏi "cùng các ký tự?". **Luôn dùng
`.equals` cho nội dung String.** (`compareTo` trả về 0 chính xác khi equals
đúng — nó còn cho biết *thứ tự*, điều `==`/`equals` không làm được.)

**Ba mẫu duyệt** — thuộc cả ba, đề thi xoay vòng qua chúng:

```java
// 1. theo chỉ số (khi cần vị trí)
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
}

// 2. bước theo substring (khi cần các mảnh liền kề)
for (int i = 0; i + 1 < s.length(); i++) {
    String pair = s.substring(i, i + 2);
}

// 3. quét đầu-cuối với thoát sớm
int pos = s.indexOf('x');
if (pos != -1) { /* tìm thấy */ }
```

Nối chuỗi tạo chuỗi mới: `"ab" + "cd"`, `s + 42`, `42 + s` đều được — số tự
động chuyển thành văn bản.
""",
)

write_lesson(
    M, "apc-m7-frq", "FRQ-style string methods",
    "Count, transform, reverse, and all-character checks — the four recurring shapes.",
    14, L3,
    "Phương thức chuỗi kiểu FRQ",
    "Đếm, biến đổi, đảo, và kiểm tra toàn bộ ký tự — bốn dạng lặp lại.",
    r"""
FRQ Câu 1 Phần B nói: "phương thức phải gọi các phương thức String." Các
dạng lặp lại:

**Đếm ký tự khớp quy tắc:**

```java
public static int countChar(String s, char target) {
    int count = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == target) {
            count++;
        }
    }
    return count;
}
```

**Trích xuất hoặc biến đổi mảnh:**

```java
public static String firstHalf(String s) {
    return s.substring(0, s.length() / 2);
}
```

**Đảo ngược bằng cách dựng ngược:**

```java
public static String reverse(String s) {
    String out = "";
    for (int i = s.length() - 1; i >= 0; i--) {
        out += s.charAt(i);
    }
    return out;
}
```

**Kiểm tra thuộc tính của mọi ký tự** (toàn chữ số? có chữ hoa?) — mẫu thoát
sớm:

```java
public static boolean allDigits(String s) {
    for (int i = 0; i < s.length(); i++) {
        if (!Character.isDigit(s.charAt(i))) {
            return false;
        }
    }
    return true;    // chỉ tới đây khi không gì thất bại
}
```

Chú ý `return true` nằm *sau* vòng lặp: đó là trường hợp "sống sót qua mọi
phép kiểm", không phải một dữ liệu đặc biệt.
""",
)

BOILER_FIRSTHALF = r"""public class Solution {
    public static String firstHalf(String s) {
        return ""; // replace
    }
}
"""

BOILER_COUNTV = r"""public class Solution {
    public static int countVowelPairs(String s) {
        return 0; // replace: neighboring pairs like "ea", "io"
    }
}
"""

BOILER_REVERSE = r"""public class Solution {
    public static String reverse(String s) {
        return ""; // replace
    }
}
"""

BOILER_PALIN = r"""public class Solution {
    public static boolean isPalindrome(String s) {
        return false; // replace
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static String shout(String s) {
        return s.toUpperCase;
    }
}
"""

CP_SCRAPE = r"""public class Solution {
    public static String digits(String s) {
        return ""; // replace: only the digit characters, in order
    }
}
"""

P_HALF = challenge(
    "apc-m7-firsthalf",
    "First half",
    "Implement `String firstHalf(String s)`: the first half of the string, rounding down for odd lengths. One substring call.",
    BOILER_FIRSTHALF,
    [(
        "halves exact",
        r"""
CjTestBase.checkEq(Solution.firstHalf("abcd"), "ab", "even");
CjTestBase.checkEq(Solution.firstHalf("abcde"), "ab", "odd rounds down");
CjTestBase.checkEq(Solution.firstHalf("x"), "", "single char");
""",
        "s.substring(0, s.length() / 2)",
    )],
    level="imitation",
)

P_PAIRS = challenge(
    "apc-m7-vowelpairs",
    "Neighboring vowel pairs",
    "Implement `int countVowelPairs(String s)`: count positions i where `s.substring(i, i + 2)` consists of two vowels (a e i o u, either case). Uses the substring-walk loop.",
    BOILER_COUNTV,
    [(
        "pair count",
        r"""
CjTestBase.checkEq(Solution.countVowelPairs("road"), 1, "only oa");
CjTestBase.checkEq(Solution.countVowelPairs("aeiou"), 4, "four adjacent pairs");
CjTestBase.checkEq(Solution.countVowelPairs("cat"), 0, "none");
""",
        "Loop i from 0 while i + 1 < length; test both chars.",
    )],
    level="guided",
)

P_REV = challenge(
    "apc-m7-reverse",
    "Reverse the string",
    "Implement `String reverse(String s)`: the characters in opposite order, built with a backwards loop.",
    BOILER_REVERSE,
    [(
        "reversed",
        r"""
CjTestBase.checkEq(Solution.reverse("abc"), "cba", "three chars");
CjTestBase.checkEq(Solution.reverse("a"), "a", "single");
CjTestBase.checkEq(Solution.reverse(""), "", "empty");
CjTestBase.checkEq(Solution.reverse(Solution.reverse("loop")), "loop", "double reverse");
""",
        "Start i at length() - 1 and walk down to 0.",
    )],
    level="guided",
)

P_PALIN = challenge(
    "apc-m7-palindrome",
    "Palindrome check",
    "Implement `boolean isPalindrome(String s)`: true when s reads the same forwards and backwards (case-sensitive; single chars and the empty string are palindromes). Compare s.charAt(i) with s.charAt(s.length() - 1 - i) — or reverse and equals.",
    BOILER_PALIN,
    [(
        "palindrome verdicts",
        r"""
CjTestBase.checkTrue(Solution.isPalindrome("racecar"), "odd length");
CjTestBase.checkTrue(Solution.isPalindrome("abba"), "even length");
CjTestBase.checkTrue(!Solution.isPalindrome("java"), "not one");
CjTestBase.checkTrue(Solution.isPalindrome("a"), "single char");
CjTestBase.checkTrue(Solution.isPalindrome(""), "empty");
""",
        "Only need to check up to the middle; mismatch fails fast.",
    )],
    level="combination",
)

P_FIX = challenge(
    "apc-m7-fix-shout",
    "Debug the method call",
    "`shout(s)` should return s in uppercase, but the code does not compile. Fix the single syntax error (a method call needs parentheses), keeping the behavior.",
    BOILER_FIX,
    [(
        "shouts correctly",
        r"""
CjTestBase.checkEq(Solution.shout("hey"), "HEY", "lower in");
CjTestBase.checkEq(Solution.shout("Ok!"), "OK!", "mixed in");
""",
        "Method calls: s.toUpperCase()",
    )],
    level="debugging",
)

CP7 = challenge(
    "apc-cp-m7-digits",
    "Checkpoint: digit scraper",
    "Implement `String digits(String s)`: return only the digit characters of s, in order — `digits(\"a1b2c3\")` returns \"123\". Empty string in, empty string out. (Character.isDigit tests one char.)",
    CP_SCRAPE,
    [(
        "digits extracted",
        r"""
CjTestBase.checkEq(Solution.digits("a1b2c3"), "123", "mixed");
CjTestBase.checkEq(Solution.digits("2026"), "2026", "all digits");
CjTestBase.checkEq(Solution.digits("no numbers"), "", "none");
CjTestBase.checkEq(Solution.digits(""), "", "empty");
""",
        "Accumulate chars that pass Character.isDigit into the output string.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p7-strings", "String surgery", "Substring math, traversal, reversal, property checks.",
    "Phẫu thuật chuỗi", "Toán substring, duyệt, đảo ngược, kiểm tra thuộc tính.",
    after_lesson="apc-m7-equals", minutes=50, difficulty="beginner",
    challenges=[P_HALF, P_PAIRS, P_REV, P_PALIN, P_FIX],
    vi_challenges={
        "apc-m7-firsthalf": vi_challenge("Nửa đầu", "Cài đặt `String firstHalf(String s)`: nửa đầu của chuỗi, làm tròn xuống khi độ dài lẻ. Một lời gọi substring.",
            [("halves exact", "s.substring(0, s.length() / 2)")]),
        "apc-m7-vowelpairs": vi_challenge("Cặp nguyên âm liền kề", "Cài đặt `int countVowelPairs(String s)`: đếm vị trí i mà `s.substring(i, i + 2)` gồm hai nguyên âm (a e i o u, bất kể hoa thường). Dùng vòng lặp bước substring.",
            [("pair count", "Vòng i từ 0 trong khi i + 1 < length; kiểm tra cả hai ký tự.")]),
        "apc-m7-reverse": vi_challenge("Đảo ngược chuỗi", "Cài đặt `String reverse(String s)`: các ký tự theo thứ tự ngược, dựng bằng vòng lặp đi xuống.",
            [("reversed", "Bắt đầu i tại length() - 1 và đi xuống tới 0.")]),
        "apc-m7-palindrome": vi_challenge("Kiểm tra palindrome", "Cài đặt `boolean isPalindrome(String s)`: đúng khi s đọc xuôi bằng đọc ngược (phân biệt hoa thường; ký tự đơn và chuỗi rỗng là palindrome). So sánh s.charAt(i) với s.charAt(s.length() - 1 - i) — hoặc đảo rồi equals.",
            [("palindrome verdicts", "Chỉ cần kiểm tới giữa; lệch một cặp là thất bại ngay.")]),
        "apc-m7-fix-shout": vi_challenge("Sửa lời gọi phương thức", "`shout(s)` phải trả về s viết hoa, nhưng code không biên dịch. Sửa một lỗi cú pháp duy nhất (lời gọi phương thức cần ngoặc), giữ nguyên hành vi.",
            [("shouts correctly", "Lời gọi phương thức: s.toUpperCase()")]),
    },
    solutions=[
        ("apc-m7-firsthalf", r"""public class Solution {
    public static String firstHalf(String s) {
        return s.substring(0, s.length() / 2);
    }
}
""",
         r"""public class Solution {
    public static String firstHalf(String s) {
        // BUG: substring end is exclusive — one char short
        return s.substring(0, s.length() / 2 - 1);
    }
}
"""),
        ("apc-m7-vowelpairs", r"""public class Solution {
    public static int countVowelPairs(String s) {
        String vowels = "aeiouAEIOU";
        int count = 0;
        for (int i = 0; i + 1 < s.length(); i++) {
            if (vowels.indexOf(s.charAt(i)) != -1
                    && vowels.indexOf(s.charAt(i + 1)) != -1) {
                count++;
            }
        }
        return count;
    }
}
""",
         r"""public class Solution {
    public static int countVowelPairs(String s) {
        // BUG: counts equal-letter pairs, not vowel pairs
        int count = 0;
        for (int i = 0; i + 1 < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i + 1)) {
                count++;
            }
        }
        return count;
    }
}
"""),
        ("apc-m7-reverse", r"""public class Solution {
    public static String reverse(String s) {
        String out = "";
        for (int i = s.length() - 1; i >= 0; i--) {
            out += s.charAt(i);
        }
        return out;
    }
}
""",
         r"""public class Solution {
    public static String reverse(String s) {
        // BUG: walks forwards — output equals input
        String out = "";
        for (int i = 0; i < s.length(); i++) {
            out += s.charAt(i);
        }
        return out;
    }
}
"""),
        ("apc-m7-palindrome", r"""public class Solution {
    public static boolean isPalindrome(String s) {
        for (int i = 0; i < s.length() / 2; i++) {
            if (s.charAt(i) != s.charAt(s.length() - 1 - i)) {
                return false;
            }
        }
        return true;
    }
}
""",
         r"""public class Solution {
    public static boolean isPalindrome(String s) {
        // BUG: miscounts the middle — odd-length fails (skips pair 0? no:
        // BUG: compares each char with itself)
        for (int i = 0; i < s.length() / 2; i++) {
            if (s.charAt(i) != s.charAt(i)) {
                return false;
            }
        }
        return true;
    }
}
""".replace("// BUG: miscounts the middle — odd-length fails (skips pair 0? no:\n        // BUG: compares each char with itself)",
            "// BUG: compares each char with itself — always true")),
        ("apc-m7-fix-shout", r"""public class Solution {
    public static String shout(String s) {
        return s.toUpperCase();
    }
}
""",
         r"""public class Solution {
    public static String shout(String s) {
        // BUG: original flaw kept — method reference without parentheses
        return s.toUpperCase;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m7", "Checkpoint: strings",
    "Filter and rebuild a string character by character.",
    20,
    r"""
The digit scraper combines everything: traversal, per-character tests, and
accumulating a new string — the same skeleton as FRQ Q1 Part B.
""",
    "Điểm kiểm tra: chuỗi",
    "Lọc và dựng lại chuỗi từng ký tự một.",
    r"""
Bộ lọc chữ số kết hợp mọi thứ: duyệt, kiểm tra từng ký tự, và tích lũy chuỗi
mới — cùng bộ khung với FRQ Câu 1 Phần B.
""",
    CP7,
    vi_challenge("Điểm kiểm tra: chuỗi", "Cài đặt `String digits(String s)`: trả về chỉ các ký tự chữ số của s theo thứ tự — `digits(\"a1b2c3\")` cho \"123\". Chuỗi rỗng vào, chuỗi rỗng ra. (Character.isDigit kiểm tra một ký tự.)",
        [("digits extracted", "Tích lũy các ký tự vượt qua Character.isDigit vào chuỗi kết quả.")]),
    solution=r"""public class Solution {
    public static String digits(String s) {
        String out = "";
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isDigit(c)) {
                out += c;
            }
        }
        return out;
    }
}
""",
    wrong=r"""public class Solution {
    public static String digits(String s) {
        // BUG: keeps NON-digits — the filter is inverted
        String out = "";
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (!Character.isDigit(c)) {
                out += c;
            }
        }
        return out;
    }
}
""",
)
