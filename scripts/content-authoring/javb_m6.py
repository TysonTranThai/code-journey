#!/usr/bin/env python3
"""Java — Beginner — Module 6: java-arrays-strings."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-arrays-strings"

L_ARRAYS_EN = r'''
An **array** is a fixed-length row of same-typed values, accessed by index:

```java
int[] temps = {18, 21, 19, 25};       // literal: length fixed at creation
double[] prices = new double[10];     // 10 slots, all 0.0
temps[0] = 17;                        // index 0 is the FIRST element
int last = temps[temps.length - 1];   // length is a field, not a method
```

The rules that shape everything:

- **Fixed size.** An array cannot grow. `temps.length` never changes. When
  your data must grow, that is the sign to reach for `ArrayList` (Module 10).
- **Zero-based indexing.** Valid indexes run `0` .. `length-1`. Outside that
  range throws `ArrayIndexOutOfBoundsException` the moment it happens.
- **Homogeneous and typed.** An `int[]` holds ints — nothing else. Java
  checks at compile time.

Iterating is the module-4 loop with `length` as the boundary; the enhanced
`for` covers the common read-everything case. **Bounds thinking** is the
skill: every index you compute (`i`, `i + 1`, `length - 1`, midpoints) must
be re-checked against `0` and `length - 1` in your head. Swapping neighbors
`a[i]` with `a[i + 1]` only works while `i + 1 <= length - 1` — one
comparison mistake and the JVM throws.

**2D arrays** are arrays of arrays — a grid:

```java
int[][] grid = { {1, 2}, {3, 4} };
System.out.println(grid[1][0]);      // 3 — row 1, column 0
for (int[] row : grid) {
    for (int cell : row) { /* ... */ }
}
```

**Next:** Java's most-used class — String.
'''

L_ARRAYS_VI = r'''
**Mảng** là một hàng giá trị cùng kiểu, độ dài cố định, truy cập bằng chỉ số:

```java
int[] temps = {18, 21, 19, 25};       // literal: độ dài cố định lúc tạo
double[] prices = new double[10];     // 10 ô, đều là 0.0
temps[0] = 17;                        // chỉ số 0 là phần tử ĐẦU TIÊN
int last = temps[temps.length - 1];   // length là trường, không phải phương thức
```

Các quy tắc định hình mọi thứ:

- **Kích thước cố định.** Mảng không thể lớn lên. `temps.length` không bao
  giờ đổi. Khi dữ liệu phải lớn lên, đó là tín hiệu chuyển sang `ArrayList`
  (Module 10).
- **Chỉ số bắt đầu từ 0.** Chỉ số hợp lệ chạy `0` .. `length-1`. Ngoài vùng
  đó sẽ ném `ArrayIndexOutOfBoundsException` ngay tại chỗ xảy ra.
- **Đồng nhất và có kiểu.** `int[]` chỉ chứa int — không gì khác. Java kiểm
  tra lúc biên dịch.

Duyệt mảng là vòng lặp module-4 với `length` làm biên; enhanced `for` phủ
trường hợp phổ biến là đọc hết mọi phần tử. **Tư duy biên** là kỹ năng cốt
lõi: mọi chỉ số bạn tính ra (`i`, `i + 1`, `length - 1`, điểm giữa) đều phải
được kiểm tra lại trong đầu với `0` và `length - 1`. Đổi chỗ `a[i]` với
`a[i + 1]` chỉ đúng khi `i + 1 <= length - 1` — sai một phép so sánh là JVM ném exception.

**Mảng 2D** là mảng của các mảng — một lưới:

```java
int[][] grid = { {1, 2}, {3, 4} };
System.out.println(grid[1][0]);      // 3 — hàng 1, cột 0
for (int[] row : grid) {
    for (int cell : row) { /* ... */ }
}
```

**Tiếp theo:** class được dùng nhiều nhất của Java — String.
'''

L_STRING_EN = r'''
A `String` is an **immutable** object — a value that can never be changed.
Every method that "modifies" a string actually returns a new one:

```java
String name = "  Ada Lovelace ";
String clean = name.trim();       // "Ada Lovelace" — name itself unchanged!
String upper = name.toUpperCase();
String both  = name.trim().toUpperCase();   // chain: method calls compose
```

The everyday toolbox:

| Method | Job | Example |
|---|---|---|
| `length()` | character count | `"hi".length()` → 2 |
| `charAt(i)` | char at index | `"hi".charAt(1)` → `'i'` |
| `substring(a, b)` | from a up to b-1 | `"hello".substring(1, 3)` → `"el"` |
| `indexOf(s)` | first position or -1 | `"banana".indexOf("na")` → 2 |
| `contains(s)` | does it appear | `"banana".contains("ana")` → true |
| `replace(a, b)` | all a become b | `"aa".replace("a","b")` → `"bb"` |
| `split(regex)` | cut into an array | `"a,b".split(",")` → `["a","b"]` |
| `strip()/trim()` | drop surrounding whitespace | `" x ".strip()` → `"x"` |
| `isEmpty()/isBlank()` | empty / whitespace-only | |

Immutability is why string equality is `.equals` (Module 2) and why
`substring` is cheap — the new string shares nothing mutable with the old.

**Splitting gotcha:** `split` takes a *regex*. To split on a literal dot,
escape it: `"1.2".split("\\.")`. To split a sentence into words:
`sentence.split("\\s+")` — one or more whitespace characters.

**Next:** building strings efficiently.
'''

L_STRING_VI = r'''
`String` là một object **bất biến** — một giá trị không bao giờ đổi được.
Mọi phương thức "sửa" chuỗi thực chất trả về một chuỗi mới:

```java
String name = "  Ada Lovelace ";
String clean = name.trim();       // "Ada Lovelace" — name vẫn nguyên!
String upper = name.toUpperCase();
String both  = name.trim().toUpperCase();   // chuỗi: các phương thức ghép được
```

Bộ dụng cụ hằng ngày:

| Phương thức | Việc | Ví dụ |
|---|---|---|
| `length()` | đếm ký tự | `"hi".length()` → 2 |
| `charAt(i)` | ký tự tại chỉ số | `"hi".charAt(1)` → `'i'` |
| `substring(a, b)` | từ a tới b-1 | `"hello".substring(1, 3)` → `"el"` |
| `indexOf(s)` | vị trí đầu tiên hoặc -1 | `"banana".indexOf("na")` → 2 |
| `contains(s)` | có xuất hiện không | `"banana".contains("ana")` → true |
| `replace(a, b)` | mọi a thành b | `"aa".replace("a","b")` → `"bb"` |
| `split(regex)` | cắt thành mảng | `"a,b".split(",")` → `["a","b"]` |
| `strip()/trim()` | bỏ khoảng trắng hai đầu | `" x ".strip()` → `"x"` |
| `isEmpty()/isBlank()` | rỗng / chỉ toàn khoảng trắng | |

Tính bất biến là lý do so sánh chuỗi dùng `.equals` (Module 2) và là lý do
`substring` rẻ — chuỗi mới không chia sẻ gì có thể đổi với chuỗi cũ.

**Bẫy của split:** `split` nhận một *regex*. Để tách theo dấu chấm thật,
phải escape: `"1.2".split("\\.")`. Tách câu thành từ:
`sentence.split("\\s+")` — một hoặc nhiều ký tự khoảng trắng.

**Tiếp theo:** xây chuỗi hiệu quả.
'''

L_BUILDER_EN = r'''
Because strings are immutable, building one piece at a time with `+` inside
a loop creates and throws away an object every iteration:

```java
String html = "";
for (String row : rows) {
    html = html + row + "\n";   // copies EVERYTHING so far, every pass
}
```

For a few iterations that is fine — readability wins. For thousands, the
copies square the cost. **StringBuilder** is the fix: a mutable buffer you
append to, converting to a String once at the end:

```java
StringBuilder html = new StringBuilder();
for (String row : rows) {
    html.append(row).append("\n");    // appends return the builder: chainable
}
String result = html.toString();      // one final conversion
```

`StringBuilder` also has `insert`, `replace`, `delete`, `reverse` — the
`reverse()` call is the palindrome check from Module 5 in one line.

The decision rule, worth internalizing now: **`+` for a fixed, small number
of pieces; `StringBuilder` inside loops.** A modern compiler optimizes
simple `+` chains into builder code anyway — the loop case is the one it
cannot rescue, because the builder must survive *across* iterations.

Two more string idioms you will use constantly:

```java
String.join(", ", "a", "b", "c");          // "a, b, c" — the inverse of split
"key=%s value=%d".formatted(key, value);   // template-style formatting
```

**Next:** practice — text analysis on real strings.
'''

L_BUILDER_VI = r'''
Vì chuỗi bất biến, việc xây một chuỗi từng mảnh bằng `+` trong vòng lặp tạo
và vứt một object mỗi vòng lặp:

```java
String html = "";
for (String row : rows) {
    html = html + row + "\n";   // sao chép MỌI thứ đã có, mỗi vòng lặp
}
```

Vài vòng lặp thì không sao — dễ đọc thắng. Hàng nghìn vòng thì các bản sao
bình phương hoá chi phí. **StringBuilder** là thuốc: một buffer có thể đổi
mà bạn append vào, và chuyển thành String đúng một lần ở cuối:

```java
StringBuilder html = new StringBuilder();
for (String row : rows) {
    html.append(row).append("\n");    // append trả về builder: ghép được chuỗi
}
String result = html.toString();      // một lần chuyển đổi cuối cùng
```

`StringBuilder` còn có `insert`, `replace`, `delete`, `reverse` — lời gọi
`reverse()` chính là phép kiểm palindrome của Module 5 gói trong một dòng.

Quy tắc quyết định đáng thuộc từ bây giờ: **`+` cho số mảnh cố định, nhỏ;
`StringBuilder` bên trong vòng lặp.** Compiler hiện đại tự tối ưu chuỗi `+`
ngắn gọn thành builder code — trường hợp vòng lặp mới là thứ nó không cứu
được, vì builder phải sống sót *qua các* vòng lặp.

Hai thành ngữ chuỗi bạn sẽ dùng liên tục:

```java
String.join(", ", "a", "b", "c");          // "a, b, c" — chiều ngược của split
"key=%s value=%d".formatted(key, value);   // định dạng kiểu mẫu
```

**Tiếp theo:** thực hành — phân tích văn bản trên chuỗi thật.
'''

# ── practice set 6 ──────────────────────────────────────────────────────────
P6_WORDCOUNT = challenge(
    "javb-m6-word-count",
    "Word statistics",
    "Implement `static int wordCount(String sentence)` returning the number of "
    "words (whitespace-separated, multiple spaces allowed) and "
    "`static String longestWord(String sentence)` returning the longest word; "
    "ties go to the FIRST longest. Empty or null input: 0 words, empty longest.",
    r'''public class Solution {
    public static int wordCount(String sentence) {
        return 0;
    }

    public static String longestWord(String sentence) {
        return "";
    }
}
''',
    [
        (
            "counting words",
            r"""
CjTestBase.checkEq(Solution.wordCount("the quick brown fox"), 4, "four words");
CjTestBase.checkEq(Solution.wordCount("  multiple   spaces  here "), 3, "messy spacing");
CjTestBase.checkEq(Solution.wordCount(""), 0, "empty");
CjTestBase.checkEq(Solution.wordCount(null), 0, "null");
""",
            "split(\"\\\\s+\") on a trimmed string; guard null/empty first.",
        ),
        (
            "longest word",
            r"""
CjTestBase.checkEq(Solution.longestWord("the quick brown fox"), "quick", "first of ties (4)");
CjTestBase.checkEq(Solution.longestWord("one two three"), "three", "clear winner");
CjTestBase.checkEq(Solution.longestWord(""), "", "empty input");
""",
            "Track best-so-far with strictly-greater comparison.",
        ),
    ],
    level="independent",
)

P6_WORDCOUNT_VI = vi_challenge(
    "Thống kê từ",
    "Viết `static int wordCount(String sentence)` trả số từ (tách bằng khoảng "
    "trắng, cho phép nhiều khoảng trắng) và `static String longestWord(String "
    "sentence)` trả từ dài nhất; bằng nhau thì chọn từ ĐẦU TIÊN. Input rỗng "
    "hoặc null: 0 từ, từ dài nhất là chuỗi rỗng.",
    [
        ("counting words", "split(\"\\\\s+\") trên chuỗi đã trim; chặn null/rỗng trước."),
        ("longest word", "Theo dõi best-so-far với phép so sánh lớn-hơn-nghiêm-ngặt."),
    ],
)

P6_PARSER = challenge(
    "javb-m6-csv-parser",
    "CSV row parser",
    "Implement `static String field(String row, int index)` that extracts one "
    "comma-separated field: `field(\"name,age,city\", 1)` is `\"age\"`. Out-of-"
    "range index returns `\"\"`. Fields keep their own spaces; do not trim.",
    r'''public class Solution {
    public static String field(String row, int index) {
        return "";
    }
}
''',
    [
        (
            "happy path",
            r"""
CjTestBase.checkEq(Solution.field("name,age,city", 0), "name", "first field");
CjTestBase.checkEq(Solution.field("name,age,city", 1), "age", "middle field");
CjTestBase.checkEq(Solution.field("name,age,city", 2), "city", "last field");
""",
            "split(\",\") gives the array; index into it.",
        ),
        (
            "boundaries",
            r"""
CjTestBase.checkEq(Solution.field("name,age,city", 3), "", "past the end");
CjTestBase.checkEq(Solution.field("name,age,city", -1), "", "negative index");
CjTestBase.checkEq(Solution.field("a , b", 0), "a ", "spaces preserved");
""",
            "The contract says no trimming and empty on any bad index.",
        ),
    ],
    level="guided",
)

P6_PARSER_VI = vi_challenge(
    "Bộ phân tích dòng CSV",
    "Viết `static String field(String row, int index)` trích một trường cách "
    "nhau bởi dấu phẩy: `field(\"name,age,city\", 1)` là `\"age\"`. Chỉ số "
    "ngoài phạm vi trả `\"\"`. Giữ nguyên khoảng trắng của trường; không trim.",
    [
        ("happy path", "split(\",\") cho mảng; lấy phần tử theo chỉ số."),
        ("boundaries", "Hợp đồng nói không trim và trả rỗng với mọi chỉ số xấu."),
    ],
)

P6_FIX = challenge(
    "javb-m6-fix-title",
    "Debug: the title-izer that misbehaves",
    "`titleCase` should capitalize the first letter of EVERY word and lower "
    "the rest: `titleCase(\"the JAVA tutorial\")` is `\"The Java Tutorial\"`. "
    "The version below drops words and keeps wrong case — find both bugs "
    "(loop boundary and char handling) and fix them.",
    r'''public class Solution {
    public static String titleCase(String input) {
        String[] words = input.split(" ");
        StringBuilder out = new StringBuilder();
        for (int i = 0; i <= words.length; i++) {
            String w = words[i];
            out.append(w.toUpperCase());
            out.append(" ");
        }
        return out.toString().trim();
    }
}
''',
    [
        (
            "correct title casing",
            r"""
CjTestBase.checkEq(Solution.titleCase("the JAVA tutorial"), "The Java Tutorial", "mixed case");
CjTestBase.checkEq(Solution.titleCase("one"), "One", "single word");
CjTestBase.checkEq(Solution.titleCase("a b c"), "A B C", "letters");
""",
            "Capitalize word.substring(0,1).toUpperCase() + rest.toLowerCase(); join with spaces.",
        ),
    ],
    level="debugging",
)

P6_FIX_VI = vi_challenge(
    "Gỡ lỗi: bộ viết hoa loạn",
    "`titleCase` phải viết hoa chữ cái đầu MỌI từ và viết thường phần còn "
    "lại: `titleCase(\"the JAVA tutorial\")` là `\"The Java Tutorial\"`. Bản "
    "dưới đây làm rơi từ và giữ sai chữ hoa — tìm cả hai bug (biên vòng lặp "
    "và xử lý ký tự) rồi sửa.",
    [("correct title casing", "Viết hoa word.substring(0,1).toUpperCase() + phần còn lại.toLowerCase(); nối bằng khoảng trắng.")],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M6_MD = r'''
The Name Analyzer crunches names with the full string toolbox.

Implement:

1. `static String initials(String first, String last)` — both initials
   upper-cased with a dot between: `initials("ada","lovelace")` is `"A.L."`.
   Null or blank parts are skipped entirely (`initials(null,"hopper")` is
   `"H."`; both blank → `""`).
2. `static int vowelCount(String text)` — count `a e i o u` in any case.
3. `static String maskEmail(String email)` — replace everything before and
   including the `@` with `"***@"`; input without `@` comes back unchanged.
   `maskEmail("ada@example.com")` is `"***@example.com"`.
4. `static boolean isUsername(String s)` — a valid username is 3–16
   characters, letters/digits/underscore only, and does NOT start with a
   digit. Null is invalid.
'''

CK_M6_MD_VI = r'''
Bộ phân tích tên xử lý tên bằng toàn bộ hộp công cụ chuỗi.

Viết:

1. `static String initials(String first, String last)` — hai chữ cái đầu
   viết hoa, chèn dấu chấm giữa: `initials("ada","lovelace")` là `"A.L."`.
   Phần null hoặc rỗng bị bỏ qua hẳn (`initials(null,"hopper")` là `"H."`;
   cả hai rỗng → `""`).
2. `static int vowelCount(String text)` — đếm `a e i o u` không phân biệt hoa thường.
3. `static String maskEmail(String email)` — thay mọi thứ trước và bao gồm
   `@` bằng `"***@"`; input không có `@` trả nguyên vẹn.
   `maskEmail("ada@example.com")` là `"***@example.com"`.
4. `static boolean isUsername(String s)` — username hợp lệ dài 3–16 ký tự,
   chỉ gồm chữ/số/gạch dưới, và KHÔNG bắt đầu bằng chữ số. Null là không hợp lệ.
'''

CK_M6_CH = challenge(
    "javb-checkpoint-strings",
    "Checkpoint: Name Analyzer",
    CK_M6_MD,
    r'''public class Solution {
    public static String initials(String first, String last) {
        return "";
    }

    public static int vowelCount(String text) {
        return 0;
    }

    public static String maskEmail(String email) {
        return "";
    }

    public static boolean isUsername(String s) {
        return false;
    }
}
''',
    [
        (
            "initials",
            r"""
CjTestBase.checkEq(Solution.initials("ada", "lovelace"), "A.L.", "both parts");
CjTestBase.checkEq(Solution.initials(null, "hopper"), "H.", "first skipped");
CjTestBase.checkEq(Solution.initials("ada", ""), "A.", "last skipped");
CjTestBase.checkEq(Solution.initials("", "  "), "", "both blank");
""",
            "Skip blank parts; dot AFTER each kept initial.",
        ),
        (
            "vowel counting",
            r"""
CjTestBase.checkEq(Solution.vowelCount("Ada Lovelace"), 6, "mixed case");
CjTestBase.checkEq(Solution.vowelCount("xyz"), 0, "no vowels");
""",
            "Lowercase the text, then count the five letters.",
        ),
        (
            "email masking",
            r"""
CjTestBase.checkEq(Solution.maskEmail("ada@example.com"), "***@example.com", "normal email");
CjTestBase.checkEq(Solution.maskEmail("no-at-sign"), "no-at-sign", "unchanged");
""",
            "indexOf('@') decides: mask or pass through.",
        ),
        (
            "username rules",
            r"""
CjTestBase.checkTrue(Solution.isUsername("ada_99"), "letters, digits, underscore");
CjTestBase.checkTrue(!Solution.isUsername("9lives"), "no leading digit");
CjTestBase.checkTrue(!Solution.isUsername("ab"), "too short");
CjTestBase.checkTrue(!Solution.isUsername(null), "null is invalid");
CjTestBase.checkTrue(!Solution.isUsername("has space"), "no spaces");
""",
            "Check length range, allowed characters, and the first character.",
        ),
    ],
    difficulty="beginner",
)

CK_M6_VI = vi_challenge(
    "Checkpoint: Bộ phân tích tên",
    CK_M6_MD_VI,
    [
        ("initials", "Bỏ qua phần rỗng; dấu chấm SAU mỗi chữ cái đầu được giữ."),
        ("vowel counting", "Viết thường văn bản, rồi đếm năm chữ cái."),
        ("email masking", "indexOf('@') quyết định: che hay giữ nguyên."),
        ("username rules", "Kiểm tra độ dài, ký tự được phép, và ký tự đầu tiên."),
    ],
)

CK_M6_R = r'''public class Solution {
    public static String initials(String first, String last) {
        StringBuilder out = new StringBuilder();
        if (first != null && !first.isBlank()) {
            out.append(Character.toUpperCase(first.trim().charAt(0))).append('.');
        }
        if (last != null && !last.isBlank()) {
            out.append(Character.toUpperCase(last.trim().charAt(0))).append('.');
        }
        return out.toString();
    }

    public static int vowelCount(String text) {
        if (text == null) return 0;
        int count = 0;
        for (char c : text.toLowerCase().toCharArray()) {
            if ("aeiou".indexOf(c) >= 0) count++;
        }
        return count;
    }

    public static String maskEmail(String email) {
        if (email == null) return "";
        int at = email.indexOf('@');
        return at < 0 ? email : "***" + email.substring(at);
    }

    public static boolean isUsername(String s) {
        if (s == null || s.length() < 3 || s.length() > 16) return false;
        if (Character.isDigit(s.charAt(0))) return false;
        for (char c : s.toCharArray()) {
            if (!Character.isLetterOrDigit(c) && c != '_') return false;
        }
        return true;
    }
}
'''

CK_M6_W = r'''public class Solution {
    public static String initials(String first, String last) {
        StringBuilder out = new StringBuilder();
        if (first != null && !first.isBlank()) {
            out.append(Character.toUpperCase(first.trim().charAt(0))).append('.');
        }
        if (last != null && !last.isBlank()) {
            out.append(Character.toUpperCase(last.trim().charAt(0))).append('.');
        }
        return out.toString();
    }

    public static int vowelCount(String text) {
        if (text == null) return 0;
        int count = 0;
        for (char c : text.toLowerCase().toCharArray()) {
            if ("aeiou".indexOf(c) >= 0) count++;
        }
        return count;
    }

    public static String maskEmail(String email) {
        if (email == null) return "";
        int at = email.indexOf('@');
        // BUG: masks even without an @, leaking nothing but breaking the contract
        return at < 0 ? "***@unknown" : "***" + email.substring(at);
    }

    public static boolean isUsername(String s) {
        if (s == null || s.length() < 3 || s.length() > 16) return false;
        if (Character.isDigit(s.charAt(0))) return false;
        for (char c : s.toCharArray()) {
            if (!Character.isLetterOrDigit(c) && c != '_') return false;
        }
        return true;
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Arrays & Strings",
    "Fixed-size arrays and bounds thinking, the immutable String and its toolbox, StringBuilder in loops, and text-processing patterns.",
    "Mảng & Chuỗi",
    "Mảng kích thước cố định và tư duy biên, String bất biến cùng hộp công cụ, StringBuilder trong vòng lặp, và pattern xử lý văn bản.",
    ["arrays-and-bounds", "string-toolbox", "stringbuilder", "java-checkpoint-strings"],
    ["javb-p6-text"],
)

write_lesson(
    MOD, "arrays-and-bounds",
    "Arrays & Bounds Thinking",
    "Fixed length, zero-based indexing, 2D grids, and re-checking every computed index.", 15,
    L_ARRAYS_EN,
    "Mảng & tư duy biên",
    "Độ dài cố định, chỉ số từ 0, lưới 2D, và kiểm tra lại mọi chỉ số tính ra.",
    L_ARRAYS_VI,
)

write_lesson(
    MOD, "string-toolbox",
    "The String Toolbox",
    "Immutability as the key idea, the everyday methods, split's regex gotcha.", 20,
    L_STRING_EN,
    "Hộp công cụ String",
    "Tính bất biến là ý tưởng then chốt, các phương thức hằng ngày, bẫy regex của split.",
    L_STRING_VI,
)

write_lesson(
    MOD, "stringbuilder",
    "StringBuilder & String Building",
    "Why + in loops squares the cost, the builder pattern, join and formatted.", 15,
    L_BUILDER_EN,
    "StringBuilder & việc xây chuỗi",
    "Vì sao + trong vòng lặp bình phương hoá chi phí, pattern builder, join và formatted.",
    L_BUILDER_VI,
)

write_practice(
    MOD, "javb-p6-text",
    "Practice: Text Processing",
    "Word statistics, a CSV field parser, and a title-caser with two planted bugs.",
    "Thực hành: Xử lý văn bản",
    "Thống kê từ, bộ phân tích trường CSV, và bộ viết hoa tiêu đề với hai bug được cài sẵn.",
    "string-toolbox", 45, "beginner",
    [P6_WORDCOUNT, P6_PARSER, P6_FIX],
    {c["id"]: v for c, v in [(P6_WORDCOUNT, P6_WORDCOUNT_VI), (P6_PARSER, P6_PARSER_VI), (P6_FIX, P6_FIX_VI)]},
    solutions=[
        (
            P6_WORDCOUNT["id"],
            r'''public class Solution {
    public static int wordCount(String sentence) {
        if (sentence == null || sentence.isBlank()) return 0;
        return sentence.trim().split("\\s+").length;
    }

    public static String longestWord(String sentence) {
        if (sentence == null || sentence.isBlank()) return "";
        String best = "";
        for (String w : sentence.trim().split("\\s+")) {
            if (w.length() > best.length()) best = w;
        }
        return best;
    }
}
''',
            r'''public class Solution {
    public static int wordCount(String sentence) {
        if (sentence == null || sentence.isBlank()) return 0;
        return sentence.trim().split("\\s+").length;
    }

    public static String longestWord(String sentence) {
        if (sentence == null || sentence.isBlank()) return "";
        String best = "";
        for (String w : sentence.trim().split("\\s+")) {
            // BUG: >= takes the LAST of tied longest words
            if (w.length() >= best.length()) best = w;
        }
        return best;
    }
}
''',
        ),
        (
            P6_PARSER["id"],
            r'''public class Solution {
    public static String field(String row, int index) {
        if (row == null || index < 0) return "";
        String[] parts = row.split(",", -1);
        return index < parts.length ? parts[index] : "";
    }
}
''',
            r'''public class Solution {
    public static String field(String row, int index) {
        if (row == null || index < 0) return "";
        // BUG: trims each field, violating the contract
        String[] parts = row.split(",", -1);
        return index < parts.length ? parts[index].trim() : "";
    }
}
''',
        ),
        (
            P6_FIX["id"],
            r'''public class Solution {
    public static String titleCase(String input) {
        if (input == null || input.isBlank()) return "";
        String[] words = input.trim().split("\\s+");
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < words.length; i++) {
            String w = words[i].toLowerCase();
            out.append(Character.toUpperCase(w.charAt(0)))
               .append(w.substring(1));
            if (i < words.length - 1) out.append(" ");
        }
        return out.toString();
    }
}
''',
            r'''public class Solution {
    public static String titleCase(String input) {
        // BUG: original <= boundary restored — reads one past the array end
        String[] words = input.split(" ");
        StringBuilder out = new StringBuilder();
        for (int i = 0; i <= words.length; i++) {
            String w = words[i];
            out.append(w.toUpperCase());
            out.append(" ");
        }
        return out.toString().trim();
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-strings",
    "Checkpoint: Name Analyzer",
    "Initials, vowels, email masking, and username validation — the full string toolbox under boundary pressure.", 45, CK_M6_MD,
    "Checkpoint: Bộ phân tích tên",
    "Tên viết tắt, nguyên âm, che email, và kiểm tra username — toàn bộ hộp công cụ chuỗi dưới áp lực biên.",
    CK_M6_MD_VI,
    CK_M6_CH, CK_M6_VI,
    solution=CK_M6_R, wrong=CK_M6_W,
)

print("module 6 complete")
