#!/usr/bin/env python3
"""Java - Beginner - Module 11: java-exceptions-files.

Authoring discipline: every Java code string is a raw triple-quoted string,
so real newlines stay real and Java string literals stay literal. Grading
follows the sandbox contract: Solution stubs in boilerplate, CjTestBase
tests, string-content file grading (no real disk I/O in tests).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-exceptions-files"

# ── lesson 11.1 — try / catch / finally ─────────────────────────────────────
L_EXC_EN = r"""
When a Java statement can't do its job - a file doesn't exist, a string
"123abc" can't become a number, an array index is out of range - the JVM
doesn't return a magic error value. It **throws an exception**: an object
that unwinds the call stack until someone handles it.

## The four keywords

```java
try {
    int n = Integer.parseInt("12x");   // throws NumberFormatException
    System.out.println("never printed");
} catch (NumberFormatException e) {
    System.out.println("bad number: " + e.getMessage());
} finally {
    System.out.println("always runs");
}
```

- **`try`** - the risky statements.
- **`catch (SomeException e)`** - runs *only* if that exception (or a
  subclass) was thrown. You can list several catch blocks, most specific
  first.
- **`finally`** - runs whether or not an exception happened. Use it for
  cleanup that must happen.
- **`throw`** - you raise one yourself: `throw new IllegalArgumentException("n < 0");`

## Checked vs unchecked

This is the part beginners find strangest, so take it slowly.

- **Unchecked exceptions** extend `RuntimeException`. The compiler does
  *not* force you to handle them: `NullPointerException`,
  `IllegalArgumentException`, `ArithmeticException`,
  `NumberFormatException`. They almost always mean a **bug** - the fix is
  better code, not a bigger try block.
- **Checked exceptions** extend `Exception` but not `RuntimeException`. The
  compiler *forces* every caller to either `catch` them or declare
  `throws`: `IOException`, `FileNotFoundException`. They represent
  real-world failures a program should plan for.

```java
// Option 1: handle it here
try {
    String text = Files.readString(path);
} catch (IOException e) {
    System.out.println("could not read: " + path);
}

// Option 2: pass the problem up to *your* caller
static String readNote(Path path) throws IOException {
    return Files.readString(path);
}
```

## Reading a stack trace

```
Exception in thread "main" java.lang.NumberFormatException:
    For input string: "12x"
	at java.base/java.lang.Integer.parseInt(Integer.java:652)
	at Main.parseCount(Main.java:8)
	at Main.main(Main.java:3)
```

Read it **bottom-up**: your own classes appear first. Here `Main.java`
line 8 called `Integer.parseInt` with `"12x"`. The *message* (`For input
string: "12x"`) usually names the exact bad input. The stack trace is not
an insult - it's a map from the crash site back to your code.

## Throwing with a message

```java
static double average(int[] scores) {
    if (scores == null || scores.length == 0) {
        throw new IllegalArgumentException("scores must be non-empty");
    }
    ...
}
```

Aim the message at the **caller who made the mistake**: state the rule and
the violated value. That message becomes the first line of debugging later.
"""

L_EXC_VI = r"""
Khi một câu lệnh Java không thể thực hiện được - file không tồn tại, chuỗi
"123abc" không thể thành số, chỉ số mảng vượt quá giới hạn - JVM không trả
về một giá trị lỗi kỳ diệu nào cả. Nó **ném (throw) một ngoại lệ**: một
đối tượng "bong" lên qua call stack cho đến khi có ai đó xử lý nó.

## Bốn từ khóa

```java
try {
    int n = Integer.parseInt("12x");   // ném NumberFormatException
    System.out.println("không bao giờ in dòng này");
} catch (NumberFormatException e) {
    System.out.println("số không hợp lệ: " + e.getMessage());
} finally {
    System.out.println("luôn luôn chạy");
}
```

- **`try`** - các câu lệnh có rủi ro.
- **`catch (SomeException e)`** - chỉ chạy khi ngoại lệ đó (hoặc lớp con
  của nó) được ném. Có thể viết nhiều catch, khối cụ thể hơn đứng trước.
- **`finally`** - chạy dù có hay không có ngoại lệ. Dùng cho việc dọn dẹp
  bắt buộc phải xảy ra.
- **`throw`** - bạn tự ném: `throw new IllegalArgumentException("n < 0");`

## Checked vs unchecked

Đây là điểm lạ lùng nhất với người mới, hãy đi chậm.

- **Unchecked exceptions** kế thừa `RuntimeException`. Compiler **không**
  ép bạn xử lý: `NullPointerException`, `IllegalArgumentException`,
  `ArithmeticException`, `NumberFormatException`... Chúng hầu như luôn là
  **bug** - cách sửa là code tốt hơn, chứ không phải try block lớn hơn.
- **Checked exceptions** kế thừa `Exception` nhưng không phải
  `RuntimeException`. Compiler **ép** mọi caller phải `catch` hoặc khai
  báo `throws`: `IOException`, `FileNotFoundException`. Chúng đại diện cho
  lỗi thực tế mà chương trình cần lên kế hoạch ứng phó.

## Đọc stack trace

Đọc **từ dưới lên**: lớp của bạn xuất hiện đầu tiên. Dòng `Main.java:8`
cho biết file và dòng gọi hàm lỗi; *message* (`For input string: "12x"`)
thường nêu đúng dữ liệu xấu. Stack trace không phải lời chê - đó là bản đồ
từ hiện trường về code của bạn.

## Ném với thông điệp rõ ràng

```java
static double average(int[] scores) {
    if (scores == null || scores.length == 0) {
        throw new IllegalArgumentException("scores must be non-empty");
    }
    ...
}
```

Hãy viết message cho **người gọi hàm gây lỗi**: nêu quy tắc và giá trị vi
phạm. Sau này, message đó chính là dòng đầu tiên của việc gỡ lỗi.
"""

# ── lesson 11.2 — robust parsing ────────────────────────────────────────────
L_PARSE_EN = r"""
Real data is dirty. A CSV line that should be `name,age` might arrive as
`"An,abc"`, `"   "`, or not arrive at all. Robust importers **validate
every field, skip what they cannot trust, and report what they skipped.**

## The parse-check pattern

```java
static Integer parseAge(String field) {
    if (field == null) return null;
    try {
        int age = Integer.parseInt(field.trim());
        if (age < 0 || age > 150) return null;   // out of range
        return age;
    } catch (NumberFormatException e) {
        return null;                             // not a number
    }
}
```

Three defenses in eight lines:

1. **Null guard** - `field` may be missing entirely.
2. **`try/catch`** - `"abc"` throws; we convert the crash into a `null`.
3. **Range check** - `"999"` parses fine but is not a plausible age.

## The line-level pipeline

```java
static int importLines(java.util.List<String> lines,
                       java.util.List<String> errors,
                       java.util.List<String> valid) {
    for (int i = 0; i < lines.size(); i++) {
        String line = lines.get(i);
        String[] parts = line.split(",");
        if (parts.length != 2) {
            errors.add((i + 1) + ": expected 2 fields, got " + parts.length);
            continue;
        }
        Integer age = parseAge(parts[1]);
        if (age == null) {
            errors.add((i + 1) + ": bad age '" + parts[1] + "'");
            continue;
        }
        valid.add(parts[0].trim() + " (" + age + ")");
    }
    return valid.size();
}
```

Note the habits:

- **1-based line numbers** in error messages (editors count from 1; raw
  loop indexes from 0 - translate for the human reading the log).
- **Collect errors, keep going** - one bad line shouldn't hide the six
  good ones behind it.
- **`continue` after recording** - never let a bad row flow onward.

This collect-and-continue style is how real import tools behave: you get
both your data *and* a to-do list of what went wrong.
"""

L_PARSE_VI = r"""
Dữ liệu thật thì bẩn. Một dòng CSV lẽ ra là `name,age` có thể đến dưới dạng
`"An,abc"`, `"   "`, hoặc không đến chút nào. Bộ import chắc chắn **kiểm
tra từng trường, bỏ qua những gì không tin được, và báo cáo những gì đã
bỏ qua.**

## Mẫu parse-check

```java
static Integer parseAge(String field) {
    if (field == null) return null;
    try {
        int age = Integer.parseInt(field.trim());
        if (age < 0 || age > 150) return null;   // ngoài khoảng
        return age;
    } catch (NumberFormatException e) {
        return null;                             // không phải số
    }
}
```

Ba lớp phòng thủ trong tám dòng:

1. **Null guard** - `field` có thể bị thiếu hoàn toàn.
2. **`try/catch`** - `"abc"` ném exception; ta biến crash thành `null`.
3. **Kiểm tra khoảng giá trị** - `"999"` parse được nhưng không phải tuổi.

## Pipeline từng dòng

```java
static int importLines(java.util.List<String> lines,
                       java.util.List<String> errors,
                       java.util.List<String> valid) {
    for (int i = 0; i < lines.size(); i++) {
        String line = lines.get(i);
        String[] parts = line.split(",");
        if (parts.length != 2) {
            errors.add((i + 1) + ": expected 2 fields, got " + parts.length);
            continue;
        }
        Integer age = parseAge(parts[1]);
        if (age == null) {
            errors.add((i + 1) + ": bad age '" + parts[1] + "'");
            continue;
        }
        valid.add(parts[0].trim() + " (" + age + ")");
    }
    return valid.size();
}
```

Chú ý các thói quen:

- **Số dòng bắt đầu từ 1** trong thông báo lỗi (editor đếm từ 1, vòng lặp
  đếm từ 0 - hãy quy đổi cho người đọc log).
- **Ghi nhận lỗi rồi tiếp tục** - một dòng xấu không được che mất sáu dòng
  tốt phía sau.
- **`continue` sau khi ghi nhận** - không bao giờ để dòng xấu chảy tiếp.

Đây chính là cách các công cụ import thật hoạt động: bạn nhận được cả dữ
liệu lẫn danh sách việc cần sửa.
"""

# ── lesson 11.3 — custom exceptions ─────────────────────────────────────────
L_CUSTOM_EN = r"""
The standard library names its exceptions for *itself*:
`NumberFormatException`, `IOException`. Your domain has its own failure
vocabulary, and custom exceptions let you speak it.

```java
class InsufficientFundsException extends Exception {
    private final double shortfall;

    InsufficientFundsException(double shortfall) {
        super("short by " + shortfall);
        this.shortfall = shortfall;
    }

    double getShortfall() { return shortfall; }
}
```

Three decisions in that small class:

1. **`extends Exception`** (not `RuntimeException`) makes it *checked* -
   every caller must decide what withdrawal-with-insufficient-funds means
   for them. Choose this for domain failures the caller can reasonably
   handle.
2. **`super(message)`** carries the human-readable explanation up to the
   stack trace and logs.
3. **Extra fields** (`shortfall`) let callers *react programmatically*, not
   just display a string - e.g. suggest a smaller withdrawal.

Throwing and catching:

```java
static void withdraw(double balance, double amount)
        throws InsufficientFundsException {
    if (amount > balance) {
        throw new InsufficientFundsException(amount - balance);
    }
}

try {
    withdraw(50, 80);
} catch (InsufficientFundsException e) {
    System.out.println("cannot withdraw: " + e.getMessage()
        + " (need " + e.getShortfall() + " more)");
}
```

## When NOT to write one

Reach for a custom exception when a *domain rule* is violated and callers
will want to treat it differently from other failures. Don't write one
when `IllegalArgumentException` already says it all - a custom exception
that everyone catches generically adds ceremony without information. And
never use exceptions for normal control flow: loop conditions and `if`
checks are clearer and far cheaper.
"""

L_CUSTOM_VI = r"""
Thư viện chuẩn đặt tên exception theo *nó*: `NumberFormatException`,
`IOException`. Lĩnh vực của bạn có từ vựng thất bại riêng, và custom
exception giúp bạn nói bằng thứ tiếng đó.

```java
class InsufficientFundsException extends Exception {
    private final double shortfall;

    InsufficientFundsException(double shortfall) {
        super("thiếu " + shortfall);
        this.shortfall = shortfall;
    }

    double getShortfall() { return shortfall; }
}
```

Ba quyết định trong lớp nhỏ đó:

1. **`extends Exception`** (không phải `RuntimeException`) làm nó trở thành
   *checked* - mọi caller buộc phải quyết định rút-tiền-thiếu-tiền nghĩa
   là gì với họ. Chọn cách này cho lỗi nghiệp vụ mà caller có thể xử lý.
2. **`super(message)`** mang giải thích cho con người lên stack trace và log.
3. **Trường dữ liệu thêm** (`shortfall`) cho phép caller *phản ứng theo
   code*, không chỉ hiển thị chuỗi.

## Khi NÀO KHÔNG nên viết

Hãy viết custom exception khi một **quy tắc nghiệp vụ** bị vi phạm và
caller muốn xử lý nó khác với các lỗi khác. Đừng viết khi
`IllegalArgumentException` đã nói đủ. Và tuyệt đối không dùng exception
làm luồng điều khiển bình thường: điều kiện vòng lặp và `if` rõ ràng hơn
và rẻ hơn rất nhiều.
"""

# ── challenges ───────────────────────────────────────────────────────────────
BOILER_AGE = r"""public class Solution {
    public static Integer parseAge(String field) {
        return null;
    }
}
"""

BOILER_DIVIDE = r"""public class Solution {
    public static double safeDivide(int a, int b) {
        return 0;
    }
}
"""

BOILER_FINALLY = r"""public class Solution {
    public static String tryResource(boolean fail) {
        return "";
    }
}
"""

P11_PARSE = challenge(
    "javb-m11-parse-age",
    "The uncrashable age parser",
    "Write `parseAge(String field)` that returns the age as an `Integer`, or `null` when it is missing, not a number, or implausible (outside 0..150). Trim whitespace before parsing.",
    BOILER_AGE,
    [
        (
            "clean values parse",
            r"""
CjTestBase.checkEq(Solution.parseAge("42"), 42, "42 parses");
CjTestBase.checkEq(Solution.parseAge("  7  "), 7, "whitespace trimmed");
""",
            "Wrap Integer.parseInt in try/catch for NumberFormatException.",
        ),
        (
            "garbage becomes null",
            r"""
CjTestBase.checkEq(Solution.parseAge("abc"), null, "not a number -> null");
CjTestBase.checkEq(Solution.parseAge("999"), null, "implausible -> null");
CjTestBase.checkEq(Solution.parseAge("-3"), null, "negative -> null");
""",
            "Check the range AFTER parsing succeeds - 999 parses but is not plausible.",
        ),
        (
            "null never crashes",
            r"""
CjTestBase.checkEq(Solution.parseAge(null), null, "null input -> null, no exception");
""",
            "A null check must come BEFORE any method call on the string.",
        ),
    ],
    level="guided",
    difficulty="intermediate",
)

P11_PARSE_VI = vi_challenge(
    "Bộ phân tích tuổi không thể sập",
    "Viết `parseAge(String field)` trả về tuổi dạng `Integer`, hoặc `null` khi thiếu, không phải số, hoặc phi thực tế (ngoài 0..150). Cắt khoảng trắng trước khi parse.",
    [("giá trị hợp lệ", "Bọc Integer.parseInt trong try/catch cho NumberFormatException."),
     ("rác trở thành null", "Kiểm tra khoảng giá trị SAU khi parse thành công - 999 parse được nhưng không phải tuổi."),
     ("null không bao giờ sập", "Null check phải đứng TRƯỚC mọi lời gọi phương thức trên chuỗi.")],
)

P11_DIVIDE = challenge(
    "javb-m11-divide-guard",
    "Divide, but loudly",
    "Write `safeDivide(int a, int b)` that returns `(double) a / b` - but throws `ArithmeticException` with a message containing \"zero\" when `b` is 0. A caller must be able to *catch* the failure, not discover a silent 0.",
    BOILER_DIVIDE,
    [
        (
            "normal division keeps the fraction",
            r"""
CjTestBase.checkEq(Solution.safeDivide(9, 4), 2.25, "9/4 = 2.25");
CjTestBase.checkEq(Solution.safeDivide(-7, 2), -3.5, "negative numerator ok");
""",
            "Cast BEFORE dividing: (double) a / b keeps the fraction.",
        ),
        (
            "zero throws, message says why",
            r"""
try {
    Solution.safeDivide(5, 0);
    CjTestBase.checkTrue(false, "divide by zero must throw");
} catch (ArithmeticException e) {
    CjTestBase.checkTrue(e.getMessage() != null && e.getMessage().contains("zero"),
        "message names the problem");
}
""",
            "Print-and-return-0 is how the bug hides - throw instead.",
        ),
    ],
    level="imitation",
    difficulty="intermediate",
)

P11_DIVIDE_VI = vi_challenge(
    "Chia, nhưng nói to",
    "Viết `safeDivide(int a, int b)` trả về `(double) a / b` - nhưng ném `ArithmeticException` với message chứa \"zero\" khi `b` bằng 0. Caller phải có thể *bắt* được lỗi, không phải phát hiện một số 0 câm lặng.",
    [("phép chia thường giữ phần thập phân", "Ép kiểu TRƯỚC khi chia: (double) a / b giữ phần lẻ."),
     ("không chia được thì ném, message nói rõ lý do", "In-rồi-trả-về-0 là cách bug trốn tránh - hãy ném exception.")],
)

P11_FINALLY = challenge(
    "javb-m11-finally-flow",
    "The finally audit log",
    "Write `tryResource(boolean fail)` that appends to a `StringBuilder` exactly: `\"open;\"` always; then, if `fail` is true, throw `IllegalStateException`; otherwise append `\"work;\"` then `\"close;\"`. Add `\"catch;\"` in a catch block and `\"finally;\"` in a finally block. Return the log **once, at the very end** - after the finally block (a `return` inside try/catch escapes before `finally` can append).",
    BOILER_FINALLY,
    [
        (
            "success path order",
            r"""
CjTestBase.checkEq(Solution.tryResource(false), "open;work;close;finally;",
    "success: finally still runs after return");
""",
            "Return once, after the finally block - not inside try or catch.",
        ),
        (
            "failure path order",
            r"""
CjTestBase.checkEq(Solution.tryResource(true), "open;catch;finally;",
    "failure: catch then finally");
""",
            "On failure the try block stops at the throw - work/close never append.",
        ),
    ],
    level="guided",
    difficulty="advanced",
)

P11_FINALLY_VI = vi_challenge(
    "Nhật ký kiểm toán với finally",
    "Viết `tryResource(boolean fail)` nối vào `StringBuilder` đúng thứ tự: `\"open;\"` luôn luôn; nếu `fail` là true thì ném `IllegalStateException`; ngược lại nối `\"work;\"` rồi `\"close;\"`. Nối `\"catch;\"` trong catch và `\"finally;\"` trong finally. Trả về log **một lần, ở cuối hàm** - sau khối finally (return bên trong try/catch sẽ thoát trước khi finally kịp nối).",
    [("thứ tự nhánh thành công", "Trả về một lần, sau khối finally - không return bên trong try hay catch."),
     ("thứ tự nhánh thất bại", "Khi thất bại, try dừng ngay tại throw - work/close không bao giờ được nối.")],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
BOILER_IMPORT = r"""public class Solution {
    public record Row(String name, int age) {}

    public static int importRows(java.util.List<String> lines,
                                 java.util.List<String> errors,
                                 java.util.List<Row> rows) {
        return 0;
    }
}
"""

P11_CP_CH = challenge(
    "javb-m11-cp-importer",
    "Checkpoint: the robust importer",
    "Implement `importRows(lines, errors, rows)` that returns the number of imported rows. For every line index `i` (0-based): a blank line records `\"<i+1>: blank line\"`; wrong field count records `\"<i+1>: expected 2 fields, got N\"`; a non-numeric age records `\"<i+1>: bad age '<field>'\"`; an age outside 0..150 records `\"<i+1>: age out of range <age>\"`; an empty name records `\"<i+1>: empty name\"`. Valid rows append `new Row(name, age)` (trimmed). Processing never stops early.",
    BOILER_IMPORT,
    [
        (
            "clean rows import",
            r"""
java.util.List<String> lines = java.util.List.of("An,33", "Dung, 28 ", "Hieu,44");
java.util.List<String> errors = new java.util.ArrayList<>();
java.util.List<Solution.Row> rows = new java.util.ArrayList<>();
int n = Solution.importRows(lines, errors, rows);
CjTestBase.checkEq(n, 3, "three clean rows");
CjTestBase.checkEq(rows.get(0).name(), "An", "first name");
CjTestBase.checkEq(rows.get(1).age(), 28, "trimmed age parsed");
""",
            "Trim both fields; parse the age defensively.",
        ),
        (
            "every rejection is recorded with a 1-based line number",
            r"""
java.util.List<String> lines = java.util.List.of("An,33", "", "Binh,abc", "Chi,999", "Giang", ",15");
java.util.List<String> errors = new java.util.ArrayList<>();
java.util.List<Solution.Row> rows = new java.util.ArrayList<>();
int n = Solution.importRows(lines, errors, rows);
CjTestBase.checkEq(n, 1, "only An survives");
CjTestBase.checkEq(errors.size(), 5, "five rejects recorded");
CjTestBase.checkTrue(errors.get(0).startsWith("2:"), "blank cites line 2");
CjTestBase.checkTrue(errors.get(2).contains("out of range"), "999 says out of range");
CjTestBase.checkTrue(errors.get(4).contains("empty name"), "empty-name message");
""",
            "Use (i + 1) for the line number; one bad line must not stop the loop.",
        ),
        (
            "sum of ages across a mixed batch",
            r"""
java.util.List<String> lines = java.util.List.of("An,33", "Binh,abc", "Dung, 28 ", "Hieu,44", "Chi,999");
java.util.List<Solution.Row> rows = new java.util.ArrayList<>();
java.util.List<String> errors = new java.util.ArrayList<>();
Solution.importRows(lines, errors, rows);
int total = 0;
for (Solution.Row r : rows) total += r.age();
CjTestBase.checkEq(total, 105, "33+28+44");
""",
            "Collect-and-continue: keep importing after recording each error.",
        ),
    ],
    level="real-world",
    difficulty="advanced",
)

P11_CP_VI = vi_challenge(
    "Checkpoint: bộ import chắc chắn",
    "Cài đặt `importRows(lines, errors, rows)` trả về số dòng đã import. Với chỉ số dòng `i` (từ 0): dòng trống ghi `\"<i+1>: blank line\"`; sai số trường ghi `\"<i+1>: expected 2 fields, got N\"`; tuổi không phải số ghi `\"<i+1>: bad age '<field>'\"`; tuổi ngoài 0..150 ghi `\"<i+1>: age out of range <age>\"`; tên rỗng ghi `\"<i+1>: empty name\"`. Dòng hợp lệ nối `new Row(name, age)` (đã trim). Việc xử lý không bao giờ dừng sớm.",
    [("dòng sạch được import", "Trim cả hai trường; parse tuổi phòng thủ."),
     ("mọi lần từ chối đều được ghi với số dòng từ 1", "Dùng (i + 1) cho số dòng; một dòng xấu không được làm dừng vòng lặp."),
     ("tổng tuổi qua một mẻ dữ liệu lẫn lộn", "Ghi nhận lỗi rồi tiếp tục: vẫn import sau khi ghi mỗi lỗi.")],
)

P11_CP_R = r"""public class Solution {
    public record Row(String name, int age) {}

    public static int importRows(java.util.List<String> lines,
                                 java.util.List<String> errors,
                                 java.util.List<Row> rows) {
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            if (line == null || line.isBlank()) {
                errors.add((i + 1) + ": blank line");
                continue;
            }
            String[] parts = line.split(",");
            if (parts.length != 2) {
                errors.add((i + 1) + ": expected 2 fields, got " + parts.length);
                continue;
            }
            String name = parts[0].trim();
            String ageField = parts[1].trim();
            int age;
            try {
                age = Integer.parseInt(ageField);
            } catch (NumberFormatException e) {
                errors.add((i + 1) + ": bad age '" + parts[1] + "'");
                continue;
            }
            if (age < 0 || age > 150) {
                errors.add((i + 1) + ": age out of range " + age);
                continue;
            }
            if (name.isEmpty()) {
                errors.add((i + 1) + ": empty name");
                continue;
            }
            rows.add(new Row(name, age));
        }
        return rows.size();
    }
}
"""

P11_CP_W = r"""public class Solution {
    public record Row(String name, int age) {}

    public static int importRows(java.util.List<String> lines,
                                 java.util.List<String> errors,
                                 java.util.List<Row> rows) {
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            if (line.isBlank()) {
                errors.add((i + 1) + ": blank line");
                continue;
            }
            String[] parts = line.split(",");
            if (parts.length != 2) {
                errors.add((i + 1) + ": expected 2 fields, got " + parts.length);
                continue;
            }
            String name = parts[0].trim();
            int age = Integer.parseInt(parts[1].trim());   // BUG: unguarded parse - Binh,abc crashes the whole import
            if (age < 0 || age > 150) {
                errors.add((i + 1) + ": age out of range " + age);
                continue;
            }
            if (name.isEmpty()) {
                errors.add((i + 1) + ": empty name");
                continue;
            }
            rows.add(new Row(name, age));
        }
        return rows.size();
    }
}
"""

CK_M11_MD = r"""
The robust importer - everything in this module composing.

Inside the provided `Solution` skeleton, implement `importRows(lines,
errors, rows)` exactly as the checkpoint prompt specifies: blank-line
guard, field-count check, defensive age parse, range check, empty-name
check, 1-based error messages, collect-and-continue, return the imported
count.

Run the tests. All three blocks must pass - then read the **wrong
solution** shown in the lesson notes: it parses without a guard, so one
`Binh,abc` row crashes the entire import with an uncaught
`NumberFormatException`. Your `try/catch` is the difference between an
importer and a crash.
"""

CK_M11_MD_VI = r"""
Bộ import chắc chắn - mọi thứ trong module này cùng vận hành.

Bên trong khung `Solution` được cung cấp, cài đặt `importRows(lines,
errors, rows)` đúng như checkpoint nêu: chặn dòng trống, kiểm tra số
trường, parse tuổi phòng thủ, kiểm tra khoảng giá trị, kiểm tra tên rỗng,
message lỗi đánh số từ 1, ghi nhận rồi tiếp tục, trả về số dòng đã import.

Chạy test. Cả ba khối phải pass - rồi đọc **solution sai** trong ghi chú:
nó parse không có chặn, nên một dòng `Binh,abc` làm sập toàn bộ quá trình
import với `NumberFormatException` không được bắt. `try/catch` của bạn
chính là khác biệt giữa một bộ import và một cú sập.
"""

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Exceptions & Safe Data Handling",
    "try/catch/finally, checked vs unchecked exceptions, reading stack traces, and an importer that survives dirty data. The finally lesson: return once, after cleanup.",
    "Ngoại lệ & xử lý dữ liệu an toàn",
    "try/catch/finally, checked vs unchecked, đọc stack trace, và bộ import sống sót qua dữ liệu bẩn.",
    ["exceptions-basics", "robust-parsing", "custom-exceptions", "java-checkpoint-exceptions"],
    ["javb-p11-exceptions"],
)

write_lesson(
    MOD, "exceptions-basics",
    "try / catch / finally",
    "The four keywords, checked vs unchecked, and reading stack traces bottom-up as maps, not scolding.",
    18,
    L_EXC_EN,
    "try / catch / finally",
    "Bốn từ khóa, checked vs unchecked, và đọc stack trace từ dưới lên như một bản đồ, không phải lời quở trách.",
    L_EXC_VI,
)

write_lesson(
    MOD, "robust-parsing",
    "Parsing Dirty Data Defensively",
    "The parse-check pattern, 1-based error reporting, and collect-and-continue importing.",
    16,
    L_PARSE_EN,
    "Phân tích dữ liệu bẩn phòng thủ",
    "Mẫu parse-check, báo lỗi đánh số từ 1, và kiểu import ghi nhận rồi tiếp tục.",
    L_PARSE_VI,
)

write_lesson(
    MOD, "java-custom-exceptions",
    "Custom Exceptions for Your Domain",
    "Checked domain exceptions with data payloads - and knowing when NOT to write one.",
    14,
    L_CUSTOM_EN,
    "Exception tự định nghĩa cho lĩnh vực của bạn",
    "Checked exception nghiệp vụ có dữ liệu đính kèm - và biết khi nào KHÔNG nên viết.",
    L_CUSTOM_VI,
)

write_practice(
    MOD, "javb-p11-exceptions",
    "Practice: Fail Well",
    "An uncrashable parser, a division that throws instead of lying, and the finally audit log.",
    "Thực hành: Lỗi đúng cách",
    "Bộ parser không thể sập, phép chia ném lỗi thay vì nói dối, và nhật ký kiểm toán finally.",
    "exceptions-basics", 45, "beginner",
    [P11_PARSE, P11_DIVIDE, P11_FINALLY],
    {P11_PARSE["id"]: P11_PARSE_VI, P11_DIVIDE["id"]: P11_DIVIDE_VI, P11_FINALLY["id"]: P11_FINALLY_VI},
    solutions=[
        (
            P11_PARSE["id"],
            r"""public class Solution {
    public static Integer parseAge(String field) {
        if (field == null) return null;
        try {
            int age = Integer.parseInt(field.trim());
            if (age < 0 || age > 150) return null;
            return age;
        } catch (NumberFormatException e) {
            return null;
        }
    }
}
""",
            r"""public class Solution {
    public static Integer parseAge(String field) {
        try {   // BUG: null input reaches field.trim() and throws NullPointerException
            int age = Integer.parseInt(field.trim());
            if (age < 0 || age > 150) return null;
            return age;
        } catch (NumberFormatException e) {
            return null;
        }
    }
}
""",
        ),
        (
            P11_DIVIDE["id"],
            r"""public class Solution {
    public static double safeDivide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("divide by zero: " + a + " / 0");
        }
        return (double) a / b;
    }
}
""",
            r"""public class Solution {
    public static double safeDivide(int a, int b) {
        if (b == 0) {
            System.out.println("cannot divide by zero");   // BUG: prints instead of throwing - caller cannot catch
            return 0;
        }
        return (double) a / b;
    }
}
""",
        ),
        (
            P11_FINALLY["id"],
            r"""public class Solution {
    public static String tryResource(boolean fail) {
        StringBuilder log = new StringBuilder();
        try {
            log.append("open;");
            if (fail) throw new IllegalStateException("boom");
            log.append("work;");
            log.append("close;");
        } catch (IllegalStateException e) {
            log.append("catch;");
        } finally {
            log.append("finally;");
        }
        return log.toString();
    }
}
""",
            r"""public class Solution {
    public static String tryResource(boolean fail) {
        StringBuilder log = new StringBuilder();
        try {
            log.append("open;");
            if (fail) throw new IllegalStateException("boom");
            log.append("work;");
            log.append("close;");
            return log.toString();   // BUG: returns BEFORE finally appends - log is missing "finally;"
    }
}
""",
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-exceptions",
    "Checkpoint: The Robust Importer",
    "Blank guards, field counts, defensive parses, range checks, 1-based messages - one pipeline that never stops early.",
    40, CK_M11_MD,
    "Checkpoint: Bộ import chắc chắn",
    "Chặn dòng trống, đếm trường, parse phòng thủ, kiểm khoảng giá trị, message đánh số từ 1 - một pipeline không bao giờ dừng sớm.",
    CK_M11_MD_VI,
    P11_CP_CH, P11_CP_VI,
    solution=P11_CP_R, wrong=P11_CP_W,
)

print("module 11 complete")
