#!/usr/bin/env python3
"""Java — Beginner — Module 2: java-types-operators (variables & data types).

Discipline: raw strings for all Java code; self-contained snippets; the
wrong solution is a behavioral near-miss. write_lesson(minutes, EN, VI-title,
VI-desc, VI-mdx) per the fixed javb contract.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-types-operators"

L_VARS_EN = r'''
A **variable** is a named box that holds a value of a known type. In Java the
type is part of the declaration and never changes:

```java
int score = 0;              // declare + initialize
score = 10;                 // assign a new value
final int maxScore = 100;   // final: cannot be reassigned
```

`int score = 0;` reads "an int named score, starting at 0". Assignment (`=`)
means "put this value in that box" — read it as *becomes*, not *equals*.

Java distinguishes **declaring** (creating the box), **initializing** (giving
it a first value), and **assigning** (replacing the value). A local variable
that was declared but never initialized cannot be read at all:

```java
int x;
System.out.println(x);   // compile error: variable x might not have been initialized
```

Use `final` for anything that should not change after it is set — method
parameters, configuration, computed results you are about to use several
times. The compiler then *enforces* your intent, and readers trust the value.

```java
final String name = "Ada";
name = "Grace";   // compile error: cannot assign a value to final variable name
```

**Next:** the full type zoo.
'''

L_VARS_VI = r'''
**Biến** là một hộp có tên chứa giá trị của một kiểu đã biết. Trong Java, kiểu
là một phần của khai báo và không bao giờ đổi:

```java
int score = 0;              // khai báo + khởi tạo
score = 10;                 // gán giá trị mới
final int maxScore = 100;   // final: không thể gán lại
```

`int score = 0;` đọc là "một int tên score, bắt đầu bằng 0". Phép gán (`=`)
nghĩa là "đặt giá trị này vào hộp đó" — hãy đọc là *trở thành*, không phải
*bằng*.

Java phân biệt **khai báo** (tạo hộp), **khởi tạo** (đặt giá trị đầu), và
**gán** (thay giá trị). Biến cục bộ đã khai báo mà chưa khởi tạo thì không
được phép đọc:

```java
int x;
System.out.println(x);   // lỗi biên dịch: biến x có thể chưa được khởi tạo
```

Dùng `final` cho mọi thứ không được đổi sau khi đặt — tham số, cấu hình, kết
quả tính toán sắp dùng nhiều lần. Compiler sẽ *bắt buộc* ý định của bạn, và
người đọc tin tưởng giá trị đó.

```java
final String name = "Ada";
name = "Grace";   // lỗi biên dịch: không thể gán cho biến final name
```

**Tiếp theo:** toàn bộ vườn thú kiểu dữ liệu.
'''

L_TYPES_EN = r'''
Java's **primitive types** are the raw values the CPU understands; everything
else is an object.

| Type | Size | Range / use | Example |
|---|---|---|---|
| `int` | 32-bit | whole numbers ±~2.1 billion | `int users = 1250;` |
| `long` | 64-bit | whole numbers, huge counts, timestamps | `long fileId = 9_876_543_210L;` |
| `double` | 64-bit | decimals (default for floating point) | `double price = 19.99;` |
| `float` | 32-bit | decimals, rare; needs `f` suffix | `float r = 0.5f;` |
| `boolean` | — | true / false only | `boolean active = true;` |
| `char` | 16-bit | ONE character, single quotes | `char grade = 'A';` |
| `byte`, `short` | 8/16-bit | memory-tight situations; rare for beginners | — |

Two details that bite everyone once:

- **`long` literals need an `L` suffix**: `9_876_543_210` is an `int` literal
  that does not fit, but `9_876_543_210L` is fine. Underscores are just for
  readability.
- **`char` uses single quotes, `String` double quotes**: `'A'` is a 16-bit
  character, `"A"` is an object. They are different types entirely.

`String` is not primitive — it is a class:

```java
String greeting = "hi";       // an object with methods
int len = greeting.length();  // 2
```

Everything in Java is typed, checked, and documented. When in doubt:
`int` for counting, `double` for measuring, `boolean` for deciding,
`String` for text, `long` when numbers get big.

**Next:** constants and the conversion rules between types.
'''

L_TYPES_VI = r'''
**Kiểu primitive** của Java là các giá trị thô CPU hiểu trực tiếp; mọi thứ
còn lại là object.

| Kiểu | Kích thước | Phạm vi / dùng khi | Ví dụ |
|---|---|---|---|
| `int` | 32-bit | số nguyên ±~2.1 tỷ | `int users = 1250;` |
| `long` | 64-bit | số nguyên lớn, timestamp | `long fileId = 9_876_543_210L;` |
| `double` | 64-bit | số thập phân (mặc định) | `double price = 19.99;` |
| `float` | 32-bit | thập phân, hiếm; cần hậu tố `f` | `float r = 0.5f;` |
| `boolean` | — | chỉ true / false | `boolean active = true;` |
| `char` | 16-bit | MỘT ký tự, nháy đơn | `char grade = 'A';` |
| `byte`, `short` | 8/16-bit | tiết kiệm bộ nhớ; hiếm với người mới | — |

Hai chi tiết cắn mọi người đúng một lần:

- **Literal `long` cần hậu tố `L`**: `9_876_543_210` là literal `int` không
  vừa, nhưng `9_876_543_210L` thì ổn. Dấu gạch dưới chỉ để dễ đọc.
- **`char` dùng nháy đơn, `String` dùng nháy đôi**: `'A'` là ký tự 16-bit,
  `"A"` là một object. Đây là hai kiểu hoàn toàn khác nhau.

`String` không phải primitive — nó là class:

```java
String greeting = "hi";       // một object có phương thức
int len = greeting.length();  // 2
```

Trong Java mọi thứ đều có kiểu, được kiểm tra, và được ghi tài liệu. Không
chắc thì: `int` để đếm, `double` để đo, `boolean` để quyết định,
`String` cho chữ, `long` khi số quá lớn.

**Tiếp theo:** hằng số và các quy tắc chuyển đổi giữa các kiểu.
'''

L_CONVERSION_EN = r'''
Converting between types comes in two flavors with opposite risk profiles.

**Widening (safe, automatic)** — smaller type into bigger type, no data loss:

```java
int apples = 12;
double avg = apples;        // int → double, always fine: 12.0
long big = apples;          // int → long, fine
```

**Narrowing (lossy, you must ask for it)** — the compiler refuses silent
damage; an explicit **cast** takes responsibility:

```java
double price = 19.99;
int rounded = (int) price;  // 19 — the fraction is TRUNCATED, not rounded
long huge = 9_876_543_210L;
int small = (int) huge;     // compiles; may silently wrap around
```

`(int)` truncates toward zero — for real rounding use `Math.round`.

**String ↔ number** is the other daily conversion, and it can *fail*:

```java
int n = Integer.parseInt("42");      // 42
double d = Double.parseDouble("3.5");// 3.5
String s = String.valueOf(42);       // "42"

Integer.parseInt("4x2");             // NumberFormatException at runtime
```

`parseInt` throws when the text is not a number — you will meet the
try/catch that handles this politely in Module 12; for now, only parse text
you trust.

**One more trap:** `1 + 2 + "A"` is `"3A"` but `"A" + 1 + 2` is `"A12"` —
`+` works left to right, and once a `String` appears, everything after it is
glued as text.

**Next:** arithmetic and its surprises.
'''

L_CONVERSION_VI = r'''
Chuyển đổi kiểu có hai hương vị với mức độ rủi ro ngược nhau.

**Mở rộng (an toàn, tự động)** — kiểu nhỏ sang kiểu lớn, không mất dữ liệu:

```java
int apples = 12;
double avg = apples;        // int → double, luôn ổn: 12.0
long big = apples;          // int → long, ổn
```

**Thu hẹp (mất dữ liệu, bạn phải chủ động xin)** — compiler từ chối phá hỏng
một cách âm thầm; phép **cast** tường minh nghĩa là bạn chịu trách nhiệm:

```java
double price = 19.99;
int rounded = (int) price;  // 19 — phần lẻ bị CẮT, không phải làm tròn
long huge = 9_876_543_210L;
int small = (int) huge;     // biên dịch được; có thể âm thầm tràn số
```

`(int)` cắt về phía 0 — muốn làm tròn thật thì dùng `Math.round`.

**String ↔ số** là phép chuyển đổi hằng ngày thứ hai, và nó có thể *thất bại*:

```java
int n = Integer.parseInt("42");      // 42
double d = Double.parseDouble("3.5");// 3.5
String s = String.valueOf(42);       // "42"

Integer.parseInt("4x2");             // NumberFormatException lúc chạy
```

`parseInt` ném exception khi chữ không phải số — bạn sẽ gặp try/catch xử lý
lịch sự việc này ở Module 12; tạm thời chỉ parse văn bản bạn tin được.

**Một cái bẫy nữa:** `1 + 2 + "A"` cho `"3A"` nhưng `"A" + 1 + 2` cho `"A12"`
— `+` chạy từ trái sang phải, và khi một `String` xuất hiện, mọi thứ phía sau
được nối thành chữ.

**Tiếp theo:** số học và những điều bất ngờ của nó.
'''

L_ARITH_EN = r'''
Java's arithmetic operators: `+ - * / %`, plus `++` and `--`. The surprises
live in division and remainder:

```java
System.out.println(7 / 2);        // 3  — integer division truncates!
System.out.println(7.0 / 2);      // 3.5 — one double makes the math double
System.out.println(7 % 2);        // 1  — remainder ("mod")
System.out.println(-7 % 2);       // -1 — sign follows the dividend in Java
```

**Integer division is the classic beginner bug**: `double avg = sum / count;`
where both are ints gives a truncated `int` result *before* the assignment.
Fix by widening first: `(double) sum / count`.

`%` is not just for even/odd checks — it drives clock arithmetic
(`(hour + 3) % 24`), cycling indexes, and "every Nth item" loops.

**Overflow awareness.** Primitives are fixed-size boxes:

```java
int max = Integer.MAX_VALUE;   // 2_147_483_647
System.out.println(max + 1);   // -2_147_483_648 — wraps around, no error!
```

The math wraps silently. For counters that could exceed ~2 billion (or where
correctness matters more than speed), use `long`; Java 8+ also offers
`Math.addExact(max, 1)`, which throws instead of wrapping.

**Augmented assignment** updates in place: `score += 10` is `score = score + 10`;
also `-=`, `*=`, `/=`, `%=`. And `++`/`--` add or subtract one — `i++` in a
loop header is the idiom you will see everywhere.

**Next:** comparing values and combining conditions.
'''

L_ARITH_VI = r'''
Các toán tử số học của Java: `+ - * / %`, cộng thêm `++` và `--`. Bất ngờ
nằm ở phép chia và số dư:

```java
System.out.println(7 / 2);        // 3  — chia nguyên cắt phần lẻ!
System.out.println(7.0 / 2);      // 3.5 — một số double biến cả phép tính thành double
System.out.println(7 % 2);        // 1  — số dư ("mod")
System.out.println(-7 % 2);       // -1 — dấu theo số bị chia trong Java
```

**Chia nguyên là bug kinh điển của người mới**: `double avg = sum / count;`
với cả hai là int sẽ cho kết quả int đã cắt *trước khi* gán. Sửa bằng cách
mở rộng kiểu trước: `(double) sum / count`.

`%` không chỉ để kiểm tra chẵn/lẻ — nó chạy đồng hồ số học
(`(hour + 3) % 24`), xoay vòng chỉ số, và "mỗi phần tử thứ N".

**Nhận thức về tràn số.** Primitive là hộp có kích thước cố định:

```java
int max = Integer.MAX_VALUE;   // 2_147_483_647
System.out.println(max + 1);   // -2_147_483_648 — quay vòng, không báo lỗi!
```

Phép toán quay vòng im lặng. Với bộ đếm có thể vượt ~2 tỷ (hoặc nơi tính đúng
quan trọng hơn tốc độ), dùng `long`; từ Java 8 còn có
`Math.addExact(max, 1)` ném exception thay vì quay vòng.

**Gán mở rộng** cập nhật tại chỗ: `score += 10` là `score = score + 10`;
tương tự `-=`, `*=`, `/=`, `%=`. Và `++`/`--` cộng hoặc trừ một — `i++` trong
header của vòng lặp là thành ngữ bạn sẽ thấy khắp nơi.

**Tiếp theo:** so sánh giá trị và kết hợp điều kiện.
'''

L_BOOL_EN = r'''
Comparisons produce `boolean` values, and booleans combine with
`&&` (AND), `||` (OR), `!` (NOT):

```java
int age = 20;
boolean adult   = age >= 18;          // true
boolean teen    = age >= 13 && age < 18;  // AND: both sides true
boolean weekend = isSat || isSun;     // OR: either side true
boolean invalid = !adult;             // NOT: flips it
```

**`&&` and `||` short-circuit**: the right side is skipped when the left side
already decides the answer. That is not an optimization footnote — it is how
you write safe checks:

```java
// && guards the right side: if s is null, the length is never asked
if (s != null && s.length() > 0) { ... }

// Dangerous reversal: asks length() of null → NullPointerException
if (s.length() > 0 && s != null) { ... }
```

Equality has a trap of its own:

- Primitives compare by value: `x == 5` is exactly right.
- **Objects (including String) compare by identity with `==`** — "is this
  the same object", not "same contents". Two different `String` objects
  holding `"yes"` can fail `==`. Always compare *contents* with `.equals`:

```java
String a = new String("yes");
String b = "yes";
a == b          // false — different objects!
a.equals(b)     // true  — same characters
```

Write `.equals` as a reflex for Strings and every other object; make `==`
mean "primitives only" in your head.

**Next:** practice — the calculator, the converter, the grade book.
'''

L_BOOL_VI = r'''
Phép so sánh tạo ra giá trị `boolean`, và boolean kết hợp với nhau bằng
`&&` (AND), `||` (OR), `!` (NOT):

```java
int age = 20;
boolean adult   = age >= 18;          // true
boolean teen    = age >= 13 && age < 18;  // AND: cả hai vế đúng
boolean weekend = isSat || isSun;     // OR: một trong hai vế đúng
boolean invalid = !adult;             // NOT: lật ngược
```

**`&&` và `||` đoản mạch**: vế phải bị bỏ qua khi vế trái đã quyết định được
kết quả. Đây không phải chú thích tối ưu hóa — đó là cách bạn viết kiểm tra
an toàn:

```java
// && bảo vệ vế phải: nếu s là null, không ai hỏi length()
if (s != null && s.length() > 0) { ... }

// Đảo ngược nguy hiểm: hỏi length() của null → NullPointerException
if (s.length() > 0 && s != null) { ... }
```

Phép bằng có một cái bẫy riêng:

- Primitive so sánh theo giá trị: `x == 5` hoàn toàn đúng.
- **Object (kể cả String) so sánh bằng `==` là so identity** — "có phải cùng
  một object", không phải "cùng nội dung". Hai object `String` khác nhau cùng
  chứa `"yes"` có thể thất bại với `==`. Luôn so *nội dung* bằng `.equals`:

```java
String a = new String("yes");
String b = "yes";
a == b          // false — hai object khác nhau!
a.equals(b)     // true  — cùng ký tự
```

Hãy để `.equals` thành phản xạ với String và mọi object khác; và để `==`
nghĩa là "chỉ dùng cho primitive" trong đầu bạn.

**Tiếp theo:** thực hành — máy tính, bộ chuyển đổi, sổ điểm.
'''

# ── practice set 2 ──────────────────────────────────────────────────────────
BOILER_CALC = r'''public class Solution {
    public static int add(int a, int b) {
        // Return the sum of a and b.
        return 0;
    }
}
'''

P2_ADD = challenge(
    "javb-m2-add",
    "Sum of two numbers",
    "Implement `add(int a, int b)` so it returns the sum. One line of real code — "
    "the point is to make the compiler's type checking work for you.",
    BOILER_CALC,
    [
        (
            "sums positives",
            r"""
CjTestBase.checkEq(Solution.add(2, 3), 5, "add(2,3)");
CjTestBase.checkEq(Solution.add(100, 200), 300, "add(100,200)");
""",
            "Replace `return 0;` with `return a + b;`.",
        ),
        (
            "handles negatives",
            r"""
CjTestBase.checkEq(Solution.add(-5, 5), 0, "add(-5,5)");
CjTestBase.checkEq(Solution.add(-10, -20), -30, "add(-10,-20)");
""",
            "The formula works unchanged for negative values.",
        ),
    ],
    level="imitation",
)

P2_ADD_VI = vi_challenge(
    "Tổng hai số",
    "Viết `add(int a, int b)` trả về tổng. Một dòng code thật — điểm chính là để "
    "compiler kiểm tra kiểu thay bạn.",
    [
        ("sums positives", "Thay `return 0;` bằng `return a + b;`."),
        ("handles negatives", "Công thức giữ nguyên cho giá trị âm."),
    ],
)

P2_AVG = challenge(
    "javb-m2-integer-division",
    "Average without the truncation trap",
    "`average(int a, int b)` must return the mean as a `double`. Beware: "
    "`(a + b) / 2` with two ints truncates BEFORE the assignment. "
    "`average(1, 2)` must be `1.5`, not `1.0`.",
    r'''public class Solution {
    public static double average(int a, int b) {
        return 0;
    }
}
''',
    [
        (
            "fractional averages",
            r"""
CjTestBase.checkEq(Solution.average(1, 2), 1.5, "average(1,2)");
CjTestBase.checkEq(Solution.average(2, 4), 3.0, "average(2,4)");
""",
            "Widen one operand before dividing: `(a + b) / 2.0`.",
        ),
        (
            "negatives too",
            r"""
CjTestBase.checkEq(Solution.average(-3, 2), -0.5, "average(-3,2)");
""",
            "Same fix works; check the sign survives.",
        ),
    ],
    level="guided",
)

P2_AVG_VI = vi_challenge(
    "Trung bình không dính bẫy cắt số",
    "`average(int a, int b)` phải trả trung bình dưới dạng `double`. Cẩn thận: "
    "`(a + b) / 2` với hai int bị cắt TRƯỚC khi gán. `average(1, 2)` phải là `1.5`, không phải `1.0`.",
    [
        ("fractional averages", "Mở rộng một toán hạng trước khi chia: `(a + b) / 2.0`."),
        ("negatives too", "Cách sửa như cũ; kiểm tra dấu vẫn còn."),
    ],
)

P2_TEMP = challenge(
    "javb-m2-temp-converter",
    "Temperature converter",
    "Implement two methods: `toCelsius(double f)` = `(f - 32) * 5 / 9` and "
    "`toFahrenheit(double c)` = `c * 9 / 5 + 32`. Results must be exact doubles.",
    r'''public class Solution {
    public static double toCelsius(double f) {
        return 0;
    }

    public static double toFahrenheit(double c) {
        return 0;
    }
}
''',
    [
        (
            "freezing point round trip",
            r"""
CjTestBase.checkNear(Solution.toCelsius(32), 0.0, 1e-9, "32F in C");
CjTestBase.checkNear(Solution.toFahrenheit(0), 32.0, 1e-9, "0C in F");
""",
            "Both formulas at the freezing point.",
        ),
        (
            "body temperature",
            r"""
CjTestBase.checkNear(Solution.toCelsius(98.6), 37.0, 1e-9, "98.6F in C");
CjTestBase.checkNear(Solution.toFahrenheit(100), 212.0, 1e-9, "100C in F");
""",
            "Boiling point: 100 C = 212 F.",
        ),
        (
            "round trip identity",
            r"""
CjTestBase.checkNear(Solution.toFahrenheit(Solution.toCelsius(75.5)), 75.5, 1e-9, "round trip");
""",
            "Convert there and back — you must land exactly where you started.",
        ),
    ],
    level="independent",
)

P2_TEMP_VI = vi_challenge(
    "Bộ chuyển đổi nhiệt độ",
    "Viết hai phương thức: `toCelsius(double f)` = `(f - 32) * 5 / 9` và "
    "`toFahrenheit(double c)` = `c * 9 / 5 + 32`. Kết quả phải là double chính xác.",
    [
        ("freezing point round trip", "Cả hai công thức ở điểm đóng băng."),
        ("body temperature", "Điểm sôi: 100 C = 212 F."),
        ("round trip identity", "Đi rồi về — phải đáp đúng nơi khởi đầu."),
    ],
)

P2_FIZZ = challenge(
    "javb-m2-fizzword",
    "Fizz word (single number)",
    "Implement `String label(int n)`: return `\"Fizz\"` when n is divisible by 3, "
    "`\"Buzz\"` when divisible by 5, `\"FizzBuzz\"` when divisible by BOTH, and "
    "otherwise the number itself as a String. Use `%` and `String.valueOf(n)`.",
    r'''public class Solution {
    public static String label(int n) {
        return "";
    }
}
''',
    [
        (
            "plain numbers",
            r"""
CjTestBase.checkEq(Solution.label(1), "1", "label(1)");
CjTestBase.checkEq(Solution.label(7), "7", "label(7)");
""",
            "Neither divisible by 3 nor 5 → the number as text.",
        ),
        (
            "fizz, buzz, both",
            r"""
CjTestBase.checkEq(Solution.label(9), "Fizz", "label(9)");
CjTestBase.checkEq(Solution.label(10), "Buzz", "label(10)");
CjTestBase.checkEq(Solution.label(15), "FizzBuzz", "label(15)");
""",
            "Check the BOTH case FIRST — 15 is also divisible by 3 and by 5.",
        ),
    ],
    level="combination",
)

P2_FIZZ_VI = vi_challenge(
    "Fizz word (một số)",
    "Viết `String label(int n)`: trả `\"Fizz\"` khi n chia hết cho 3, "
    "`\"Buzz\"` khi chia hết cho 5, `\"FizzBuzz\"` khi chia hết cho CẢ HAI, "
    "còn lại trả chính số đó dưới dạng chuỗi. Dùng `%` và `String.valueOf(n)`.",
    [
        ("plain numbers", "Không chia hết cho 3 lẫn 5 → số dưới dạng chữ."),
        ("fizz, buzz, both", "Kiểm tra trường hợp CẢ HAI TRƯỚC — 15 cũng chia hết cho 3 và cho 5."),
    ],
)

P2_OVERFLOW = challenge(
    "javb-m2-safe-sum",
    "Sum that refuses to overflow",
    "Implement `long sumTo(int n)` returning `1 + 2 + ... + n`. Then implement "
    "`boolean fitsInInt(long total)` returning whether the total can be stored "
    "in an `int` safely (compare against `Integer.MAX_VALUE`). "
    "`sumTo(65_536)` must NOT silently wrap (its true value exceeds `Integer.MAX_VALUE`).",
    r'''public class Solution {
    public static long sumTo(int n) {
        return 0;
    }

    public static boolean fitsInInt(long total) {
        return false;
    }
}
''',
    [
        (
            "small sums",
            r"""
CjTestBase.checkEq(Solution.sumTo(10), 55L, "sumTo(10)");
CjTestBase.checkEq(Solution.sumTo(100), 5050L, "sumTo(100)");
""",
            "Gauss: n*(n+1)/2 as a long, or a simple accumulation loop.",
        ),
        (
            "big sums stay correct",
            r"""
CjTestBase.checkEq(Solution.sumTo(65_536), 2_147_516_416L, "sumTo(65536)");
CjTestBase.checkTrue(!Solution.fitsInInt(Solution.sumTo(65_536)), "does not fit int");
CjTestBase.checkTrue(Solution.fitsInInt(Solution.sumTo(100)), "5050 fits int");
""",
            "Accumulate into a `long` (or compute n*(n+1)/2L). 2_147_516_416 > Integer.MAX_VALUE (2_147_483_647).",
        ),
    ],
    level="real-world",
)

P2_OVERFLOW_VI = vi_challenge(
    "Tổng khước từ tràn số",
    "Viết `long sumTo(int n)` trả `1 + 2 + ... + n`. Sau đó viết "
    "`boolean fitsInInt(long total)` cho biết tổng có nằm vừa trong `int` hay không "
    "(so với `Integer.MAX_VALUE`). `sumTo(50_000)` không được quay vòng âm thầm.",
    [
        ("small sums", "Gauss: n*(n+1)/2 dưới dạng long, hoặc một vòng cộng đơn giản."),
        ("big sums stay correct", "Cộng dồn vào `long` (hoặc tính n*(n+1)/2L). 1_250_025_000 > Integer.MAX_VALUE."),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M2_MD = r'''
The Grade Calculator combines every module-2 idea in one small program.

Write `public static String report(String name, int score)` that returns
(but does not print!) a line of text:

- Start with the name, then `": "`, then the score, then `" -> "`.
- Append the letter grade: `A` for 90+, `B` for 80–89, `C` for 70–79,
  `D` for 60–69, `F` below 60.
- Also append the percentage as ` (NN%)` — the score itself, so for
  `report("Ada", 93)` the exact result is `"Ada: 93 -> A (93%)"`.

Everything must be built with `final` locals where sensible and string
concatenation; the grader compares the exact returned String for several
students, including boundary scores 90, 60, and 59.
'''

CK_M2_MD_VI = r'''
Bộ tính điểm kết hợp mọi ý tưởng của module 2 trong một chương trình nhỏ.

Viết `public static String report(String name, int score)` trả về (không in!)
một dòng văn bản:

- Bắt đầu bằng tên, rồi `": "`, rồi điểm số, rồi `" -> "`.
- Nối hạng chữ: `A` cho 90+, `B` cho 80–89, `C` cho 70–79, `D` cho 60–69,
  `F` dưới 60.
- Thêm phần trăm dạng ` (NN%)` — chính là điểm, vậy với `report("Ada", 93)`
  kết quả chính xác là `"Ada: 93 -> A (93%)"`.

Dùng biến cục bộ `final` nơi hợp lý và phép nối chuỗi; grader so sánh String
trả về chính xác cho vài học viên, kể cả điểm biên 90, 60, và 59.
'''

CK_M2_CH = challenge(
    "javb-checkpoint-types",
    "Checkpoint: Grade Calculator",
    CK_M2_MD,
    r'''public class Solution {
    public static String report(String name, int score) {
        return "";
    }
}
''',
    [
        (
            "A and B bands",
            r"""
CjTestBase.checkEq(Solution.report("Ada", 93), "Ada: 93 -> A (93%)", "report Ada 93");
CjTestBase.checkEq(Solution.report("Grace", 90), "Grace: 90 -> A (90%)", "boundary 90");
CjTestBase.checkEq(Solution.report("Alan", 85), "Alan: 85 -> B (85%)", "report Alan 85");
""",
            "90 is A (>= 90), 85 is B. Format: name + ': ' + score + ' -> ' + grade + ' (NN%)'.",
        ),
        (
            "C, D, F bands",
            r"""
CjTestBase.checkEq(Solution.report("Joan", 70), "Joan: 70 -> C (70%)", "boundary 70");
CjTestBase.checkEq(Solution.report("Linus", 60), "Linus: 60 -> D (60%)", "boundary 60");
CjTestBase.checkEq(Solution.report("Edsger", 59), "Edsger: 59 -> F (59%)", "just below D");
""",
            "Boundaries: 70 C, 60 D, 59 F.",
        ),
    ],
    difficulty="beginner",
)

CK_M2_VI = vi_challenge(
    "Checkpoint: Bộ tính điểm",
    CK_M2_MD_VI,
    [
        ("A and B bands", "90 là A (>= 90), 85 là B. Định dạng: name + ': ' + score + ' -> ' + grade + ' (NN%)'."),
        ("C, D, F bands", "Biên: 70 C, 60 D, 59 F."),
    ],
)

CK_M2_R = r'''public class Solution {
    public static String report(String name, int score) {
        final String grade;
        if (score >= 90) {
            grade = "A";
        } else if (score >= 80) {
            grade = "B";
        } else if (score >= 70) {
            grade = "C";
        } else if (score >= 60) {
            grade = "D";
        } else {
            grade = "F";
        }
        return name + ": " + score + " -> " + grade + " (" + score + "%)";
    }
}
'''

CK_M2_W = r'''public class Solution {
    public static String report(String name, int score) {
        final String grade;
        // BUG: boundary off by one — 90 lands in B, 60 lands in F
        if (score > 90) {
            grade = "A";
        } else if (score >= 80) {
            grade = "B";
        } else if (score >= 70) {
            grade = "C";
        } else if (score > 60) {
            grade = "D";
        } else {
            grade = "F";
        }
        return name + ": " + score + " -> " + grade + " (" + score + "%)";
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Variables & Data Types",
    "The primitive types, String, final, widening and casting, arithmetic with its truncation and overflow traps, and boolean logic.",
    "Biến & Kiểu dữ liệu",
    "Các kiểu primitive, String, final, mở rộng và cast kiểu, số học với bẫy cắt số và tràn số, và logic boolean.",
    ["java-variables-assignment", "primitive-types", "conversion-casting", "arithmetic-operators", "boolean-logic", "java-checkpoint-types"],
    ["javb-p2-types"],
)

write_lesson(
    MOD, "java-variables-assignment",
    "Variables, Assignment & final",
    "Declaring, initializing, assigning; why final makes intent compiler-enforced.", 15,
    L_VARS_EN,
    "Biến, gán & final",
    "Khai báo, khởi tạo, gán; vì sao final khiến ý định được compiler bắt buộc.",
    L_VARS_VI,
)

write_lesson(
    MOD, "primitive-types",
    "The Type Zoo: int, long, double, boolean, char, String",
    "Choosing types deliberately; the L suffix, char-vs-String quotes, and the sizes behind the ranges.", 15,
    L_TYPES_EN,
    "Vườn thú kiểu: int, long, double, boolean, char, String",
    "Chọn kiểu có chủ đích; hậu tố L, nháy char-so-với-String, và kích thước đứng sau phạm vi.",
    L_TYPES_VI,
)

write_lesson(
    MOD, "conversion-casting",
    "Conversion & Casting",
    "Widening vs narrowing, the truncating cast, String parsing and its failures, the + ordering trap.", 15,
    L_CONVERSION_EN,
    "Chuyển đổi & ép kiểu",
    "Mở rộng vs thu hẹp, cast cắt số, parse String và thất bại của nó, bẫy thứ tự phép +.",
    L_CONVERSION_VI,
)

write_lesson(
    MOD, "arithmetic-operators",
    "Arithmetic: Division, Remainder, Overflow",
    "Integer division's silent truncation, % beyond even/odd, wrapping overflow and its cures.", 15,
    L_ARITH_EN,
    "Số học: chia, số dư, tràn số",
    "Chia nguyên cắt số âm thầm, % ngoài chẵn/lẻ, tràn số quay vòng và cách chữa.",
    L_ARITH_VI,
)

write_lesson(
    MOD, "boolean-logic",
    "Booleans: Comparisons, Short-Circuits, equals",
    "&& || !, short-circuit safety for null checks, and why String equality is .equals not ==.", 15,
    L_BOOL_EN,
    "Boolean: so sánh, đoản mạch, equals",
    "&& || !, an toàn đoản mạch cho kiểm tra null, và vì sao so sánh String là .equals chứ không phải ==.",
    L_BOOL_VI,
)

write_practice(
    MOD, "javb-p2-types",
    "Practice: Types at Work",
    "From one-line sums to overflow-proof accumulation — arithmetic that survives contact with real data.",
    "Thực hành: Kiểu dữ liệu tại chỗ làm",
    "Từ dòng cộng một dòng đến cộng dồn chống tràn — số học sống sót khi chạm dữ liệu thật.",
    "arithmetic-operators", 50, "beginner",
    [P2_ADD, P2_AVG, P2_TEMP, P2_FIZZ, P2_OVERFLOW],
    {c["id"]: v for c, v in [
        (P2_ADD, P2_ADD_VI), (P2_AVG, P2_AVG_VI), (P2_TEMP, P2_TEMP_VI),
        (P2_FIZZ, P2_FIZZ_VI), (P2_OVERFLOW, P2_OVERFLOW_VI)]},
    solutions=[
        (
            P2_ADD["id"],
            r'''public class Solution {
    public static int add(int a, int b) {
        return a + b;
    }
}
''',
            r'''public class Solution {
    public static int add(int a, int b) {
        // BUG: subtracts instead of adding
        return a - b;
    }
}
''',
        ),
        (
            P2_AVG["id"],
            r'''public class Solution {
    public static double average(int a, int b) {
        return (a + b) / 2.0;
    }
}
''',
            r'''public class Solution {
    public static double average(int a, int b) {
        // BUG: integer division truncates before the double return
        return (a + b) / 2;
    }
}
''',
        ),
        (
            P2_TEMP["id"],
            r'''public class Solution {
    public static double toCelsius(double f) {
        return (f - 32) * 5 / 9;
    }

    public static double toFahrenheit(double c) {
        return c * 9 / 5 + 32;
    }
}
''',
            r'''public class Solution {
    public static double toCelsius(double f) {
        // BUG: forgets the -32 offset
        return f * 5 / 9;
    }

    public static double toFahrenheit(double c) {
        return c * 9 / 5 + 32;
    }
}
''',
        ),
        (
            P2_FIZZ["id"],
            r'''public class Solution {
    public static String label(int n) {
        if (n % 15 == 0) return "FizzBuzz";
        if (n % 3 == 0) return "Fizz";
        if (n % 5 == 0) return "Buzz";
        return String.valueOf(n);
    }
}
''',
            r'''public class Solution {
    public static String label(int n) {
        // BUG: checks 3 and 5 first — 15 can never reach FizzBuzz
        if (n % 3 == 0) return "Fizz";
        if (n % 5 == 0) return "Buzz";
        if (n % 15 == 0) return "FizzBuzz";
        return String.valueOf(n);
    }
}
''',
        ),
        (
            P2_OVERFLOW["id"],
            r'''public class Solution {
    public static long sumTo(int n) {
        return (long) n * (n + 1) / 2;
    }

    public static boolean fitsInInt(long total) {
        return total <= Integer.MAX_VALUE && total >= Integer.MIN_VALUE;
    }
}
''',
            r'''public class Solution {
    public static long sumTo(int n) {
        // BUG: int arithmetic wraps before the widening assignment
        return n * (n + 1) / 2;
    }

    public static boolean fitsInInt(long total) {
        return total <= Integer.MAX_VALUE && total >= Integer.MIN_VALUE;
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-types",
    "Checkpoint: Grade Calculator",
    "Boundary-correct grading with clean concatenation — types, comparisons, and exact output.", 40, CK_M2_MD,
    "Checkpoint: Bộ tính điểm",
    "Xếp hạng đúng biên với phép nối chuỗi sạch — kiểu dữ liệu, so sánh, và output chính xác.",
    CK_M2_MD_VI,
    CK_M2_CH, CK_M2_VI,
    solution=CK_M2_R, wrong=CK_M2_W,
)

print("module 2 complete")
