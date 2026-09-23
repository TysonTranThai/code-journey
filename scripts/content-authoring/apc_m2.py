#!/usr/bin/env python3
"""AP CSA M2 — Variables and Data Types (Java-specific behavior)."""
from apc import *

M = "apc-variables"

L1 = r"""
A variable is a **typed** storage box: you declare its type once, and Java
enforces it forever.

```java
int score = 95;            // whole numbers
double average = 91.5;     // decimals
boolean passed = true;     // true or false
char letter = 'A';         // ONE character, single quotes
String name = "An";        // text, double quotes
```

**Assignment replaces; it does not add.** Trace this:

```java
int x = 5;
x = 10;        // x is 10 now — the 5 is gone
x = x + 3;     // right side evaluated first: 10 + 3, then stored
```

After those three lines, `x` is `13`. The right side of `=` is always
evaluated *before* the store happens.

`boolean` holds exactly two values, `true` and `false` — no numbers, no
"truthy" shortcuts like other languages. `char` uses **single** quotes
(`'A'`), `String` uses **double** quotes (`"A"`). Mixing them is a classic
compile error.
"""

L2 = r"""
Java primitives: `int` (whole numbers), `double` (decimals), `boolean`
(true/false), `char` (one character). Anything else on the exam is built from
these plus objects.

**Constants** — the `final` keyword freezes a variable:

```java
final int MAX_SCORE = 100;
MAX_SCORE = 105;    // compile error — constants never change
```

**Integer division is the trap.** When both operands are `int`, the result
is an `int` — the fractional part is **truncated** (dropped, not rounded):

```java
System.out.println(7 / 2);     // 3   (not 3.5)
System.out.println(7 % 2);     // 1   (remainder)
System.out.println(7.0 / 2);   // 3.5 (one double operand → double math)
System.out.println(-7 / 2);    // -3  (truncation toward zero)
```

**Casting** converts explicitly:

```java
double d = 9.7;
int truncated = (int) d;          // 9   — decimal part dropped
int rounded = (int) (d + 0.5);    // 10  — the manual rounding trick
double back = truncated;          // widening: no cast needed
```

Widening (`int` → `double`) is automatic; narrowing (`double` → `int`)
needs the cast and loses information.
"""

L3 = r"""
An `int` has 32 bits: values from −2³¹ (−2147483648) to 2³¹ − 1 (2147483647).

**Overflow wraps around** silently:

```java
int big = 2147483647;
big = big + 1;
System.out.println(big);    // -2147483648 — wrapped!
```

Two int-only operators the exam loves:

- `+` on **ints with Strings**: `"score: " + 90` → `"score: 90"`
  (concatenation). Left to right: `1 + 2 + "x"` → `"3x"`, but `"x" + 1 + 2`
  → `"x12"`.
- `%` (remainder) works on negatives with the sign of the dividend:
  `-7 % 3` is `-1`.

`char` participates in arithmetic through its Unicode value:

```java
char c = 'A';            // 65
char next = (char) (c + 1);   // 'B'
```

Casting an `int` that is out of `char`'s range produces a different
character — another silent wrap.
"""

write_module(
    M,
    "Variables and Data Types",
    "int, double, boolean, char; assignment, constants, integer division, casting, and overflow.",
    "Biến và kiểu dữ liệu",
    "int, double, boolean, char; gán giá trị, hằng số, phép chia số nguyên, ép kiểu và tràn số.",
    lessons=["apc-m2-prims", "apc-m2-casts", "apc-m2-overflow", "apc-cp-m2"],
    practices=["apc-p2-variables"],
)

write_lesson(
    M, "apc-m2-prims", "Declaring and assigning",
    "The primitive types, assignment semantics, boolean and char literals.",
    12, L1,
    "Khai báo và gán giá trị",
    "Các kiểu nguyên thủy, ý nghĩa phép gán, boolean và ký tự char.",
    r"""
Biến là hộp lưu trữ **có kiểu**: bạn khai báo kiểu một lần và Java kiểm soát
nó mãi mãi.

```java
int score = 95;            // số nguyên
double average = 91.5;     // số thập phân
boolean passed = true;     // đúng hoặc sai
char letter = 'A';         // MỘT ký tự, ngoặc đơn
String name = "An";        // văn bản, ngoặc kép
```

**Phép gán là thay thế, không phải cộng thêm.** Truy vết:

```java
int x = 5;
x = 10;        // x giờ là 10 — số 5 biến mất
x = x + 3;     // vế phải được tính trước: 10 + 3, rồi lưu lại
```

Sau ba dòng đó, `x` là `13`. Vế phải của `=` luôn được tính *trước* khi lưu.

`boolean` chỉ có hai giá trị `true` và `false` — không có số, không có "đúng
sai ngầm" như ngôn ngữ khác. `char` dùng ngoặc **đơn** (`'A'`), `String` dùng
ngoặc **kép** (`"A"`). Trộn lẫn là lỗi biên dịch kinh điển.
""",
)

write_lesson(
    M, "apc-m2-casts", "Integer division and casting",
    "final constants, truncated integer division, %, explicit casts.",
    14, L2,
    "Chia số nguyên và ép kiểu",
    "Hằng số final, phép chia số nguyên bị cắt phần thập phân, %, ép kiểu tường minh.",
    r"""
Các kiểu nguyên thủy: `int` (số nguyên), `double` (thập phân), `boolean`
(đúng/sai), `char` (một ký tự). Mọi thứ khác trong đề thi được dựng từ chúng
cộng với đối tượng.

**Hằng số** — từ khóa `final` đóng băng biến:

```java
final int MAX_SCORE = 100;
MAX_SCORE = 105;    // lỗi biên dịch — hằng số không bao giờ đổi
```

**Chia số nguyên là cái bẫy.** Khi cả hai toán hạng là `int`, kết quả là
`int` — phần thập phân bị **cắt bỏ** (không phải làm tròn):

```java
System.out.println(7 / 2);     // 3   (không phải 3.5)
System.out.println(7 % 2);     // 1   (số dư)
System.out.println(7.0 / 2);   // 3.5 (một toán hạng double → tính double)
System.out.println(-7 / 2);    // -3  (cắt về phía 0)
```

**Ép kiểu** chuyển đổi tường minh:

```java
double d = 9.7;
int truncated = (int) d;          // 9   — phần thập phân bị bỏ
int rounded = (int) (d + 0.5);    // 10  — mẹo làm tròn thủ công
double back = truncated;          // mở rộng: không cần ép
```

Mở rộng (`int` → `double`) là tự động; thu hẹp (`double` → `int`) cần ép kiểu
và mất thông tin.
""",
)

write_lesson(
    M, "apc-m2-overflow", "Overflow and mixed types",
    "int range, silent overflow, String concatenation order, char arithmetic.",
    10, L3,
    "Tràn số và kiểu hỗn hợp",
    "Giới hạn int, tràn số âm thầm, thứ tự nối chuỗi, phép tính trên char.",
    r"""
`int` có 32 bit: từ −2³¹ (−2147483648) đến 2³¹ − 1 (2147483647).

**Tràn số vòng quanh** một cách âm thầm:

```java
int big = 2147483647;
big = big + 1;
System.out.println(big);    // -2147483648 — bị vòng lại!
```

Hai toán hạng chỉ-int mà đề thi ưa thích:

- `+` với **int và String**: `"score: " + 90` → `"score: 90"` (nối chuỗi).
  Trái sang phải: `1 + 2 + "x"` → `"3x"`, nhưng `"x" + 1 + 2` → `"x12"`.
- `%` (số dư) hoạt động với số âm mang dấu của bị chia: `-7 % 3` là `-1`.

`char` tham gia phép tính qua giá trị Unicode:

```java
char c = 'A';            // 65
char next = (char) (c + 1);   // 'B'
```

Ép một `int` ngoài phạm vi `char` sẽ ra ký tự khác — một vòng lặp âm thầm
nữa.
""",
)

BOILER_ADD = r"""public class Solution {
    public static int addThree(int x) {
        return 0; // replace
    }
}
"""

BOILER_AVG = r"""public class Solution {
    public static double averageOfFour(int a, int b, int c, int d) {
        return 0; // replace
    }
}
"""

BOILER_QTY = r"""public class Solution {
    public static int howManyItems(double money) {
        return 0; // replace
    }
}
"""

BOILER_LAST = r"""public class Solution {
    public static char lastDigitChar(int n) {
        return ' '; // replace
    }
}
"""

CP_SWAP = r"""public class Solution {
    public static String swapEnds(int a, int b) {
        return a + " " + b; // replace
    }
}
"""

P_MATH = challenge(
    "apc-m2-addthree",
    "Evaluate before storing",
    "Implement `int addThree(int x)`: return the value of `x` after three single `+1` assignments — i.e. `x + 3`. Use exactly three assignment statements and the pattern `x = x + 1;`.",
    BOILER_ADD,
    [(
        "adds three",
        r"""
CjTestBase.checkEq(Solution.addThree(0), 3, "addThree(0)");
CjTestBase.checkEq(Solution.addThree(-3), 0, "addThree(-3)");
CjTestBase.checkEq(Solution.addThree(100), 103, "addThree(100)");
""",
        "Each assignment re-reads the current value, adds 1, stores it back.",
    )],
    level="imitation",
)

P_AVG = challenge(
    "apc-m2-average",
    "Average without truncation",
    "Implement `double averageOfFour(int a, int b, int c, int d)`: the mean of four ints. Beware: `a + b + c + d / 4` is wrong twice — precedence AND integer division. Cast the **sum** to double before dividing.",
    BOILER_AVG,
    [(
        "exact mean",
        r"""
CjTestBase.checkNear(Solution.averageOfFour(3, 4, 5, 6), 4.5, 1e-9, "integers average to .5");
CjTestBase.checkNear(Solution.averageOfFour(7, 7, 7, 7), 7.0, 1e-9, "all equal");
CjTestBase.checkNear(Solution.averageOfFour(1, 1, 1, 2), 1.25, 1e-9, "quarter value survives");
""",
        "(double) (a + b + c + d) / 4 — cast before divide, not after.",
    )],
    level="guided",
)

P_DIV = challenge(
    "apc-m2-howmany",
    "How many items can I buy?",
    "Implement `int howManyItems(double money)`: the largest number of $2.50 items you can afford with `money` dollars. One expression is enough — think `int` division after a cast.",
    BOILER_QTY,
    [(
        "correct count",
        r"""
CjTestBase.checkEq(Solution.howManyItems(10.0), 4, "exactly four");
CjTestBase.checkEq(Solution.howManyItems(12.4), 4, "remainder not enough");
CjTestBase.checkEq(Solution.howManyItems(2.49), 0, "cannot afford one");
CjTestBase.checkEq(Solution.howManyItems(0.0), 0, "no money");
""",
        "(int) (money / 2.5) — truncation gives the floor for non-negative values.",
    )],
    level="combination",
)

P_DIGIT = challenge(
    "apc-m2-lastdigit",
    "Last digit as a char",
    "Implement `char lastDigitChar(int n)`: the last digit of non-negative `n`, returned as a `char` (`'7'`, not `7`). `%` gives the digit; adding `'0'` converts a digit to its character.",
    BOILER_LAST,
    [(
        "digit characters",
        r"""
CjTestBase.checkEq(Solution.lastDigitChar(123), '3', "last of 123");
CjTestBase.checkEq(Solution.lastDigitChar(8), '8', "single digit");
CjTestBase.checkEq(Solution.lastDigitChar(40), '0', "trailing zero");
""",
        "n % 10 is the digit; digit + '0' is its char value.",
    )],
    level="combination",
)

CP2 = challenge(
    "apc-cp-m2-swap",
    "Checkpoint: swap via arithmetic",
    "Implement `String swapEnds(int a, int b)`: return both values swapped as `\"b a\"` (b, then a space, then a). You may reassign `a` and `b` — but notice you will need a third variable to hold one value during the swap.",
    CP_SWAP,
    [(
        "swapped text",
        r"""
CjTestBase.checkEq(Solution.swapEnds(1, 2), "2 1", "swap 1,2");
CjTestBase.checkEq(Solution.swapEnds(-5, 7), "7 -5", "negative first");
CjTestBase.checkEq(Solution.swapEnds(4, 4), "4 4", "equal values");
""",
        "Store one value in a temp variable before overwriting it.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p2-variables", "Typed storage", "Trace assignments, master integer division, cast safely.",
    "Lưu trữ có kiểu", "Truy vết phép gán, làm chủ chia số nguyên, ép kiểu an toàn.",
    after_lesson="apc-m2-casts", minutes=40, difficulty="beginner",
    challenges=[P_MATH, P_AVG, P_DIV, P_DIGIT],
    vi_challenges={
        "apc-m2-addthree": vi_challenge("Tính trước khi lưu", "Cài đặt `int addThree(int x)`: trả về giá trị của `x` sau ba phép gán `+1` riêng biệt — tức là `x + 3`. Dùng đúng ba câu lệnh gán theo mẫu `x = x + 1;`.",
            [("adds three", "Mỗi phép gán đọc giá trị hiện tại, cộng 1, lưu ngược lại.")]),
        "apc-m2-average": vi_challenge("Trung bình không bị cắt", "Cài đặt `double averageOfFour(int a, int b, int c, int d)`: trung bình cộng của bốn số int. Cẩn thận: `a + b + c + d / 4` sai hai lần — ưu tiên toán tử VÀ chia số nguyên. Ép kiểu **tổng** sang double trước khi chia.",
            [("exact mean", "(double) (a + b + c + d) / 4 — ép trước khi chia, không phải sau.")]),
        "apc-m2-howmany": vi_challenge("Mua được bao nhiêu món?", "Cài đặt `int howManyItems(double money)`: số món hàng $2.50 tối đa mua được với `money` đô. Một biểu thức là đủ — nghĩ về ép kiểu rồi chia int.",
            [("correct count", "(int) (money / 2.5) — cắt phần lẻ cho ra sàn với giá trị không âm.")]),
        "apc-m2-lastdigit": vi_challenge("Chữ số cuối dạng char", "Cài đặt `char lastDigitChar(int n)`: chữ số cuối của `n` không âm, trả về dạng `char` (`'7'`, không phải `7`). `%` cho chữ số; cộng `'0'` đổi chữ số thành ký tự.",
            [("digit characters", "n % 10 là chữ số; chữ số + '0' là giá trị char của nó.")]),
    },
    solutions=[
        ("apc-m2-addthree", r"""public class Solution {
    public static int addThree(int x) {
        x = x + 1;
        x = x + 1;
        x = x + 1;
        return x;
    }
}
""",
         r"""public class Solution {
    public static int addThree(int x) {
        // BUG: adds once instead of three times
        x = x + 1;
        return x;
    }
}
"""),
        ("apc-m2-average", r"""public class Solution {
    public static double averageOfFour(int a, int b, int c, int d) {
        return (double) (a + b + c + d) / 4;
    }
}
""",
         r"""public class Solution {
    public static double averageOfFour(int a, int b, int c, int d) {
        // BUG: integer division truncates before widening
        return (double) ((a + b + c + d) / 4);
    }
}
"""),
        ("apc-m2-howmany", r"""public class Solution {
    public static int howManyItems(double money) {
        return (int) (money / 2.5);
    }
}
""",
         r"""public class Solution {
    public static int howManyItems(double money) {
        // BUG: counts an item you cannot fully afford
        return (int) (money / 2.5) + 1;
    }
}
"""),
        ("apc-m2-lastdigit", r"""public class Solution {
    public static char lastDigitChar(int n) {
        return (char) ('0' + n % 10);
    }
}
""",
         r"""public class Solution {
    public static char lastDigitChar(int n) {
        // BUG: returns the number itself, not the character
        return (char) (n % 10);
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m2", "Checkpoint: variables and types",
    "Tracing assignments, integer division, casting, and concatenation.",
    18,
    r"""
The checkpoint mixes the module's traps: evaluation-before-store, `%`,
truncated division, casts, and String concatenation order. Trace on paper
first — that is the AP exam skill.
""",
    "Điểm kiểm tra: biến và kiểu",
    "Truy vết phép gán, chia số nguyên, ép kiểu và nối chuỗi.",
    r"""
Bài kiểm tra trộn các cái bẫy của module: tính-trước-khi-lưu, `%`, chia bị
cắt, ép kiểu, và thứ tự nối chuỗi. Truy vết trên giấy trước — đó là kỹ năng
đề thi AP.
""",
    CP2,
    vi_challenge("Điểm kiểm tra: biến và kiểu", "Cài đặt `String swapEnds(int a, int b)`: trả về hai giá trị đã hoán đổi dạng `\"b a\"` (b, dấu cách, rồi a). Bạn có thể gán lại `a` và `b` — nhưng sẽ cần một biến thứ ba giữ một giá trị trong lúc hoán đổi.",
        [("swapped text", "Lưu một giá trị vào biến tạm trước khi ghi đè.")]),
    solution=r"""public class Solution {
    public static String swapEnds(int a, int b) {
        int temp = a;
        a = b;
        b = temp;
        return a + " " + b;
    }
}
""",
    wrong=r"""public class Solution {
    public static String swapEnds(int a, int b) {
        // BUG: no temp — first value lost before it is used
        a = b;
        b = a;
        return a + " " + b;
    }
}
""",
)
