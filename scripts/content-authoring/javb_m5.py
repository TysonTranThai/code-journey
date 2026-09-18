#!/usr/bin/env python3
"""Java — Beginner — Module 5: java-methods."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-methods"

L_METHODS_EN = r'''
A **method** is a named, reusable unit of behavior: it takes inputs
(**parameters**), does work, and may hand back a result (**return value**).

```java
static double withTax(double price) {
    return price * 1.1;
}
```

Read the signature: `static` (belongs to the class itself — the word behind
why `main` can run without creating an object), `double` (the type it
returns), `withTax` (the name), `double price` (one parameter, typed).

Calling it: `double total = withTax(19.99);` — the value `19.99` is the
**argument**, copied into the parameter. Two rules the compiler enforces:

- The returned value's type must match the declared return type (or be
  convertible).
- A method that declares a return type must `return` on **every path**
  through its body. `void` methods return nothing and may skip `return`
  (or use a bare `return;` to exit early).

```java
static String verdict(int score) {
    if (score >= 60) {
        return "pass";
    }
    return "fail";     // needed! the if-path alone would not cover all cases
}
```

**Parameters are copies** — primitive arguments are copied by value, so
changing a parameter inside a method never changes the caller's variable:

```java
static void bump(int n) { n = n + 1; }

int x = 5;
bump(x);
System.out.println(x);   // still 5
```

(Objects are references-copied-by-value — the method can *modify the object
it was given* but not re-point the caller's variable. Module 7 returns to
this; for now, primitives-are-copies is the whole story.)

**Next:** the `static` word, demystified.
'''

L_METHODS_VI = r'''
**Phương thức** là một đơn vị hành vi có tên, dùng lại được: nó nhận đầu vào
(**tham số**), làm việc, và có thể trả lại kết quả (**giá trị trả về**).

```java
static double withTax(double price) {
    return price * 1.1;
}
```

Đọc chữ ký: `static` (thuộc về class chứ không cần object — từ đứng sau việc
`main` chạy được mà không cần tạo object), `double` (kiểu trả về), `withTax`
(tên), `double price` (một tham số, có kiểu).

Gọi nó: `double total = withTax(19.99);` — giá trị `19.99` là **đối số**,
được sao chép vào tham số. Hai quy tắc compiler bắt buộc:

- Kiểu giá trị trả về phải khớp kiểu đã khai báo (hoặc chuyển đổi được).
- Phương thức khai báo kiểu trả về phải `return` trên **mọi đường đi** của
  thân hàm. Phương thức `void` không trả gì và có thể bỏ `return` (hoặc dùng
  `return;` trống để thoát sớm).

```java
static String verdict(int score) {
    if (score >= 60) {
        return "pass";
    }
    return "fail";     // cần thiết! chỉ nhánh if chưa phủ hết các trường hợp
}
```

**Tham số là bản sao** — đối số kiểu primitive được sao chép theo giá trị,
nên việc đổi tham số bên trong phương thức không bao giờ đổi biến của bên
gọi:

```java
static void bump(int n) { n = n + 1; }

int x = 5;
bump(x);
System.out.println(x);   // vẫn là 5
```

(Object là tham-chiệu-được-sao-chép-theo-giá-trị — phương thức có thể *sửa
object mà nó nhận được* nhưng không thể trỏ lại biến của bên gọi. Module 7
sẽ quay lại; hiện tại, primitive-là-bản-sao là toàn bộ câu chuyện.)

**Tiếp theo:** từ `static`, được giải mã.
'''

L_STATIC_EN = r'''
`static` means "belongs to the class, not to any object". It shows up in
three places a beginner touches immediately.

**Static methods** are callable without an instance:
`Math.max(3, 9)` works because `max` is static; every utility-style method
in this module is static for the same reason. Inside a `static` method you
can call other static methods of the same class directly — but NOT instance
members, because there is no instance yet. That is the real rule behind the
beginner error `"non-static method cannot be referenced from a static
context"`: `main` is static, so it can only reach static things (or objects
it creates).

**Static fields** are class-wide values:

```java
static final double VAT_RATE = 0.1;      // constant shared by everyone
static int invocationCount = 0;          // mutable class-wide state (careful!)
```

`static final` is Java's way to spell a constant: fixed at creation, shared
by all, named in SCREAMING_SNAKE_CASE by convention. Mutable static fields
are global variables wearing a suit — a handful of honest uses (counters,
shared configuration) and a universe of trouble; avoid them in application
code.

**Static import** lets you skip the class name for heavily used utilities:

```java
import static java.lang.Math.max;
...
int m = max(a, b);
```

Use sparingly — readability first. The decision rule: something is static
when it needs no per-object memory — it transforms its inputs, consults
constants, and returns. The moment behavior depends on per-object state, it
belongs to objects (Module 7).

**Next:** overloading — one name, several signatures.
'''

L_STATIC_VI = r'''
`static` nghĩa là "thuộc về class, không thuộc object nào". Nó xuất hiện ở
ba nơi người mới chạm ngay.

**Phương thức static** gọi được mà không cần object:
`Math.max(3, 9)` chạy được vì `max` là static; mọi phương thức kiểu tiện ích
trong module này cũng static vì lý do đó. Bên trong phương thức static, bạn
gọi trực tiếp các phương thức static khác cùng class — nhưng KHÔNG THỂ với
thành viên dạng object, vì chưa có object nào. Đó là quy tắc thật đứng sau
lỗi `"non-static method cannot be referenced from a static context"`:
`main` là static, nên nó chỉ với tới các thứ static (hoặc object nó tự tạo).

**Trường static** là giá trị của cả class:

```java
static final double VAT_RATE = 0.1;      // hằng số dùng chung
static int invocationCount = 0;          // trạng thái class có thể đổi (cẩn thận!)
```

`static final` là cách Java viết một hằng số: cố định ngay khi tạo, dùng
chung, đặt tên SCREAMING_SNAKE_CASE theo quy ước. Trường static có thể đổi
là biến toàn cục mặc vest — một ít công dụng thật (bộ đếm, cấu hình chung)
và một vũ trụ rắc rối; tránh trong code ứng dụng.

**Static import** cho phép bỏ tên class với tiện ích dùng dày:

```java
import static java.lang.Math.max;
...
int m = max(a, b);
```

Dùng tiết chế — dễ đọc trước tiên. Quy tắc quyết định: một thứ là static khi
nó không cần bộ nhớ theo-object — nó biến đổi đầu vào, tra hằng số, và trả
kết quả. Khoảnh khắc hành vi phụ thuộc trạng thái theo-object, nó thuộc về
object (Module 7).

**Tiếp theo:** overloading — một tên, nhiều chữ ký.
'''

L_OVERLOAD_EN = r'''
Several methods may share one name when their **parameter lists differ** —
different types, different counts, or different order. This is
**overloading**, and Java's compiler picks the best match at the call site:

```java
static int    max(int a, int b)        { return a >= b ? a : b; }
static double max(double a, double b)  { return a >= b ? a : b; }
static int    max(int a, int b, int c) { return max(max(a, b), c); }
```

All three are `max`; the compiler reads the argument list and dispatches:
`max(3, 9)` calls the first, `max(2.5, 1.5)` the second, `max(1, 5, 3)` the
third. The third body shows the deeper idea — overloads can *delegate* to
each other instead of duplicating logic.

What does NOT count as different: the **return type alone**. You cannot add
`static String max(int a, int b)` — the compiler could not tell which to
call for `max(3, 9)`. Only parameter lists create distinct overloads.

**When to overload, and when not.** Overload when one concept accepts
several shapes of input (`parse(String)`, `parse(File)`). Do not overload
when the meaning changes — a method that returns the max and an overload
that returns the min are different concepts wearing one confusing name.

**Varargs** — a parameter that accepts any number of arguments:

```java
static int sum(int... numbers) {         // callers: sum(), sum(1), sum(1, 2, 3)
    int t = 0;
    for (int n : numbers) { t += n; }    // numbers is really an int[]
    return t;
}
```

Varargs is sugar for an array parameter and must be the LAST parameter.
It is the right tool when the count genuinely varies ("sum any of these");
a required, fixed list of inputs deserves fixed parameters.

**Next:** designing with methods — decomposition.
'''

L_OVERLOAD_VI = r'''
Vài phương thức có thể dùng chung một tên khi **danh sách tham số khác
nhau** — khác kiểu, khác số lượng, hoặc khác thứ tự. Đây là **overloading**,
và compiler của Java chọn ứng viên khớp nhất tại chỗ gọi:

```java
static int    max(int a, int b)        { return a >= b ? a : b; }
static double max(double a, double b)  { return a >= b ? a : b; }
static int    max(int a, int b, int c) { return max(max(a, b), c); }
```

Cả ba đều là `max`; compiler đọc danh sách đối số và điều phối: `max(3, 9)`
gọi cái đầu, `max(2.5, 1.5)` cái thứ hai, `max(1, 5, 3)` cái thứ ba. Thân
hàm thứ ba hé ý tưởng sâu hơn — các overload có thể *ủy quyền* cho nhau thay
vì sao chép logic.

Cái gì KHÔNG tính là khác nhau: **một mình kiểu trả về**. Bạn không thể thêm
`static String max(int a, int b)` — compiler không thể biết gọi cái nào cho
`max(3, 9)`. Chỉ danh sách tham số tạo ra overload khác biệt.

**Khi nào nên overload, khi nào không.** Overload khi một khái niệm nhận
nhiều hình dạng đầu vào (`parse(String)`, `parse(File)`). Đừng overload khi
ý nghĩa thay đổi — hàm trả max và một overload trả min là hai khái niệm
khác nhau mặc một cái tên gây nhiễu.

**Varargs** — một tham số nhận số lượng đối số bất kỳ:

```java
static int sum(int... numbers) {         // gọi: sum(), sum(1), sum(1, 2, 3)
    int t = 0;
    for (int n : numbers) { t += n; }    // numbers thực chất là int[]
    return t;
}
```

Varargs là đường (sugar) cho tham số mảng và phải là tham số CUỐI. Đó là
công cụ đúng khi số lượng thật sự thay đổi ("cộng các số này lại"); danh
sách đầu vào bắt buộc, cố định thì xứng với tham số cố định.

**Tiếp theo:** thiết kế bằng phương thức — phân rã.
'''

L_DECOMPOSE_EN = r'''
The step up from "writing methods" to "thinking in methods" is
**decomposition**: splitting a problem into named parts small enough to
understand at a glance.

**One job per method.** A method whose name contains "and" (`validateAndSave`)
is probably two methods. The name is the contract; if you cannot state the
job in one sentence, the method is doing too much.

**The rule of three-ish:** write it once directly; write it twice with a
wince; the third near-copy becomes a method. Extract when the duplicate
starts drifting apart — divergent copies of "the same" logic are how bugs
are born.

**Refactoring loop** you will practice below:

1. Identify repeated or over-long code.
2. Extract into a method named for the *job* (`formatPrice`, not `doStuff1`).
3. Pass everything the job needs as parameters; return the result rather
   than printing it.
4. Re-run the tests — behavior must be identical.

**Return results, don't print.** A method that computes and prints is glued
to the console; one that returns its result composes into bigger programs
and, crucially, is *testable* — the grader (and your future self) can call
it. Printing is a job for the outermost layer.

```java
static String line(String item, int qty, double price) {
    return item + " x" + qty + " = " + formatMoney(qty * price);
}

static String formatMoney(double amount) {
    return String.format("$%.2f", amount);
}
```

Two small methods, each one sentence, composing into a receipt. That is the
whole discipline.

**Next:** practice — building and repairing a utility library.
'''

L_DECOMPOSE_VI = r'''
Bước nhảy từ "viết được phương thức" lên "nghĩ bằng phương thức" là **phân
rã**: tách bài toán thành các phần có tên, nhỏ đủ để hiểu trong một cái nhìn.

**Một việc cho mỗi phương thức.** Phương thức có chữ "và" trong tên
(`validateAndSave`) có lẽ là hai phương thức. Tên là hợp đồng; nếu không nói
một câu được công việc, phương thức đang làm quá nhiều.

**Quy tắc ba-nói-chưa-sát:** viết một lần trực tiếp; viết hai lần với chút
nhăn mặt; bản sao gần giống thứ ba trở thành phương thức. Trích xuất khi
các bản sao bắt đầu lệch nhau — những bản sao "cùng một logic" đi hai ngả
là nơi bug sinh ra.

**Vòng refactor** bạn sẽ thực hành bên dưới:

1. Xác định code lặp hoặc quá dài.
2. Trích xuất thành phương thức đặt tên theo *công việc* (`formatPrice`,
   không phải `doStuff1`).
3. Truyền mọi thứ công việc cần qua tham số; trả kết quả thay vì in ra.
4. Chạy lại test — hành vi phải giữ nguyên.

**Trả kết quả, đừng in.** Phương thức vừa tính vừa in bị dán chặt vào console;
phương thức trả kết quả thì ghép được vào chương trình lớn hơn, và quan
trọng hơn, *kiểm thử được* — grader (và chính bạn sau này) gọi được nó. In
ra là công việc của tầng ngoài cùng.

```java
static String line(String item, int qty, double price) {
    return item + " x" + qty + " = " + formatMoney(qty * price);
}

static String formatMoney(double amount) {
    return String.format("$%.2f", amount);
}
```

Hai phương thức nhỏ, mỗi cái một câu, ghép thành một hóa đơn. Đó là toàn bộ
kỷ luật này.

**Tiếp theo:** thực hành — xây và sửa một thư viện tiện ích.
'''

# ── practice set 5 ──────────────────────────────────────────────────────────
P5_UTIL = challenge(
    "javb-m5-utility",
    "Utility library: repeat, clamp, isBlank",
    "Implement three small utilities in one Solution class:\n\n"
    "1. `static String repeat(String s, int n)` — returns s repeated n times "
    "(`repeat(\"ab\", 3)` is `\"ababab\"`; n <= 0 gives `\"\"`).\n"
    "2. `static int clamp(int v, int min, int max)` — v if in range, otherwise "
    "the nearest bound.\n"
    "3. `static boolean isBlank(String s)` — true for null, empty, or "
    "whitespace-only strings.",
    r'''public class Solution {
    public static String repeat(String s, int n) {
        return "";
    }

    public static int clamp(int v, int min, int max) {
        return 0;
    }

    public static boolean isBlank(String s) {
        return false;
    }
}
''',
    [
        (
            "repeat",
            r"""
CjTestBase.checkEq(Solution.repeat("ab", 3), "ababab", "ab x3");
CjTestBase.checkEq(Solution.repeat("x", 1), "x", "x once");
CjTestBase.checkEq(Solution.repeat("x", 0), "", "zero times");
CjTestBase.checkEq(Solution.repeat("x", -2), "", "negative times");
""",
            "Accumulate with StringBuilder or a loop; n <= 0 is the empty string.",
        ),
        (
            "clamp",
            r"""
CjTestBase.checkEq(Solution.clamp(5, 0, 10), 5, "in range");
CjTestBase.checkEq(Solution.clamp(-3, 0, 10), 0, "below range");
CjTestBase.checkEq(Solution.clamp(99, 0, 10), 10, "above range");
""",
            "Two comparisons, two returns — or Math.max/min composed.",
        ),
        (
            "isBlank",
            r"""
CjTestBase.checkTrue(Solution.isBlank(null), "null is blank");
CjTestBase.checkTrue(Solution.isBlank(""), "empty is blank");
CjTestBase.checkTrue(Solution.isBlank("   "), "spaces are blank");
CjTestBase.checkTrue(!Solution.isBlank(" x "), "content is not blank");
""",
            "Handle null FIRST, then trim/strip and check emptiness.",
        ),
    ],
    level="guided",
)

P5_UTIL_VI = vi_challenge(
    "Thư viện tiện ích: repeat, clamp, isBlank",
    "Viết ba tiện ích nhỏ trong cùng một class Solution:\n\n"
    "1. `static String repeat(String s, int n)` — trả s lặp lại n lần "
    "(`repeat(\"ab\", 3)` là `\"ababab\"`; n <= 0 cho `\"\"`).\n"
    "2. `static int clamp(int v, int min, int max)` — v nếu trong khoảng, "
    "ngược lại là biên gần nhất.\n"
    "3. `static boolean isBlank(String s)` — true với null, rỗng, hoặc "
    "chỉ toàn khoảng trắng.",
    [
        ("repeat", "Tích lũy bằng StringBuilder hoặc vòng lặp; n <= 0 là chuỗi rỗng."),
        ("clamp", "Hai phép so sánh, hai return — hoặc ghép Math.max/min."),
        ("isBlank", "Xử lý null TRƯỚC, rồi trim/strip và kiểm tra rỗng."),
    ],
)

P5_OVERLOAD = challenge(
    "javb-m5-overloads",
    "Overloads that delegate",
    "Create a family of `join` overloads that all delegate to one core:\n\n"
    "- `static String join(String sep, String a, String b)`\n"
    "- `static String join(String sep, String a, String b, String c)`\n"
    "- `static String join(String sep, String... parts)` — varargs core\n\n"
    "Each joins with the separator between items (`join(\"-\", \"a\", \"b\")` "
    "is `\"a-b\"`). The two fixed overloads must CALL the varargs one rather "
    "than duplicating logic.",
    r'''public class Solution {
    public static String join(String sep, String a, String b) {
        return "";
    }

    public static String join(String sep, String a, String b, String c) {
        return "";
    }

    public static String join(String sep, String... parts) {
        return "";
    }
}
''',
    [
        (
            "fixed arities",
            r"""
CjTestBase.checkEq(Solution.join("-", "a", "b"), "a-b", "two parts");
CjTestBase.checkEq(Solution.join(", ", "x", "y", "z"), "x, y, z", "three parts");
""",
            "Separator only BETWEEN items, never at the ends.",
        ),
        (
            "varargs core",
            r"""
CjTestBase.checkEq(Solution.join("-", "a"), "a", "single part");
CjTestBase.checkEq(Solution.join("-"), "", "no parts");
""",
            "One part prints bare; zero parts is empty.",
        ),
    ],
    level="combination",
)

P5_OVERLOAD_VI = vi_challenge(
    "Overload ủy quyền cho nhau",
    "Tạo một họ overload `join` đều ủy quyền về một lõi:\n\n"
    "- `static String join(String sep, String a, String b)`\n"
    "- `static String join(String sep, String a, String b, String c)`\n"
    "- `static String join(String sep, String... parts)` — lõi varargs\n\n"
    "Mỗi hàm nối các phần tử bằng dấu phân cách (`join(\"-\", \"a\", \"b\")` "
    "là `\"a-b\"`). Hai overload cố định phải GỌI bản varargs thay vì sao chép logic.",
    [
        ("fixed arities", "Dấu phân cách chỉ ở GIỮA các phần tử, không ở hai đầu."),
        ("varargs core", "Một phần tử in trần; không phần tử là rỗng."),
    ],
)

P5_DECOMPOSE = challenge(
    "javb-m5-decompose",
    "Receipt line, decomposed",
    "Implement two cooperating methods:\n\n"
    "- `static String formatMoney(double amount)` — formats as `$NN.NN` with "
    "exactly two decimals (`formatMoney(5)` is `$5.00`).\n"
    "- `static String line(String item, int qty, double price)` — returns "
    "`\"item xN = $NN.NN\"` where the money part comes from `formatMoney` "
    "of `qty * price`. Example: `line(\"pen\", 3, 1.5)` is "
    "`\"pen x3 = $4.50\"`.",
    r'''public class Solution {
    public static String formatMoney(double amount) {
        return "";
    }

    public static String line(String item, int qty, double price) {
        return "";
    }
}
''',
    [
        (
            "money formatting",
            r"""
CjTestBase.checkEq(Solution.formatMoney(5), "$5.00", "whole dollars");
CjTestBase.checkEq(Solution.formatMoney(19.991), "$19.99", "rounded to cents");
""",
            "String.format(\"$%.2f\", amount) rounds correctly.",
        ),
        (
            "receipt line",
            r"""
CjTestBase.checkEq(Solution.line("pen", 3, 1.5), "pen x3 = $4.50", "3 pens");
CjTestBase.checkEq(Solution.line("book", 1, 9.99), "book x1 = $9.99", "single book");
""",
            "line() must call formatMoney — compose, don't duplicate.",
        ),
    ],
    level="independent",
)

P5_DECOMPOSE_VI = vi_challenge(
    "Dòng hóa đơn, phân rã",
    "Viết hai phương thức phối hợp:\n\n"
    "- `static String formatMoney(double amount)` — định dạng `$NN.NN` với "
    "đúng hai số lẻ (`formatMoney(5)` là `$5.00`).\n"
    "- `static String line(String item, int qty, double price)` — trả "
    "`\"item xN = $NN.NN\"` với phần tiền lấy từ `formatMoney` của "
    "`qty * price`. Ví dụ: `line(\"pen\", 3, 1.5)` là `\"pen x3 = $4.50\"`.",
    [
        ("money formatting", "String.format(\"$%.2f\", amount) làm tròn đúng."),
        ("receipt line", "line() phải gọi formatMoney — ghép, đừng sao chép."),
    ],
)

P5_FIX = challenge(
    "javb-m5-fix-refactor",
    "Debug: the method that prints instead of returning",
    "`bmiReport` below compiles and prints, but it is untestable: the verdict "
    "is printed, not returned, and the category logic lives inline. Refactor: "
    "`static String category(double bmi)` returns `\"under\"`, `\"normal\"`, "
    "or `\"over\"` (< 18.5 under; 18.5–24.9 normal; 25+ over), and "
    "`bmiReport` RETURNS `\"BMI 22.7 normal\"`-style text using it.",
    r'''public class Solution {
    public static void bmiReport(double weightKg, double heightM) {
        double bmi = weightKg / (heightM * heightM);
        String cat = bmi < 18.5 ? "under" : (bmi < 25 ? "normal" : "over");
        System.out.println("BMI " + bmi + " " + cat);
    }
}
''',
    [
        (
            "category boundaries",
            r"""
CjTestBase.checkEq(Solution.category(17.0), "under", "17 is under");
CjTestBase.checkEq(Solution.category(18.5), "normal", "18.5 starts normal");
CjTestBase.checkEq(Solution.category(24.9), "normal", "24.9 still normal");
CjTestBase.checkEq(Solution.category(25.0), "over", "25 starts over");
""",
            "Boundaries: < 18.5, then < 25, else over.",
        ),
        (
            "report returns",
            r"""
String out = CjTestBase.capture(() -> System.out.print(Solution.bmiReport(70, 1.755)));
CjTestBase.checkTrue(out.startsWith("BMI "), "report starts with 'BMI '");
CjTestBase.checkTrue(out.contains(" normal"), "report ends with the category");
""",
            "bmiReport must RETURN the string (capture catches a print only if it happens — it must not).",
        ),
    ],
    level="debugging",
)

P5_FIX_VI = vi_challenge(
    "Gỡ lỗi: phương thức in thay vì trả về",
    "`bmiReport` dưới đây biên dịch và in được, nhưng không kiểm thử được: "
    "phán quyết bị in ra chứ không được trả về, và logic xếp loại nằm lẫn "
    "trong đó. Refactor: `static String category(double bmi)` trả "
    "`\"under\"`, `\"normal\"`, hoặc `\"over\"` (< 18.5 under; 18.5–24.9 "
    "normal; 25+ over), và `bmiReport` TRẢ VỀ văn bản dạng `\"BMI 22.7 normal\"` dùng nó.",
    [
        ("category boundaries", "Biên: < 18.5, rồi < 25, còn lại over."),
        ("report returns", "bmiReport phải TRẢ VỀ chuỗi (capture chỉ bắt được print nếu nó có xảy ra — nó không được phép)."),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M5_MD = r'''
The Text Toolkit is a small library with a clean contract. Implement:

1. `static String initials(String fullName)` — the first letters of the
   words, upper-cased and joined. `initials("ada byron lovelace")` is
   `"ABL"`. Extra spaces between words are ignored; an empty or null name
   gives `""`.
2. `static boolean isPalindrome(String text)` — true when text reads the
   same forwards and backwards, **ignoring case and every non-letter**
   (`isPalindrome("A man, a plan, a canal: Panama!")` is true — it reduces to
   `amanaplanacanalpanama`, which reads the same both ways). Null or empty after cleaning is `false`.
3. `static String truncate(String text, int max)` — text shortened to at
   most `max` characters, with `"..."` appended **only when shortening
   happened**. `truncate("programming", 7)` is `"program"` + `"..."`; a
   text already within the limit comes back untouched. `max` below 4
   (no room even for the dots) returns just the first `max` characters
   with no dots.

Every method returns a value; none prints. Build helpers if useful — the
grader only calls the three public entry points.
'''

CK_M5_MD_VI = r'''
Bộ công cụ văn bản là một thư viện nhỏ với hợp đồng sạch. Viết:

1. `static String initials(String fullName)` — các chữ cái đầu của từng từ,
   viết hoa và nối lại. `initials("ada byron lovelace")` là `"ABL"`. Khoảng
   trắng thừa giữa các từ bị bỏ qua; tên rỗng hoặc null cho `""`.
2. `static boolean isPalindrome(String text)` — true khi văn bản đọc xuôi
   ngược như nhau, **không phân biệt hoa/thường và bỏ mọi ký tự không phải
   chữ cái** (`isPalindrome("A man, a plan!")` là true vì rút gọn còn
   `amanaplan`). Null hoặc rỗng sau khi làm sạch là `false`.
3. `static String truncate(String text, int max)` — văn bản rút xuống tối
   đa `max` ký tự, thêm `"..."` **chỉ khi có rút gọn**.
   `truncate("programming", 7)` là `"program"` + `"..."`; văn bản đã trong
   giới hạn trả nguyên vẹn. `max` dưới 4 (không đủ chỗ cho cả dấu chấm)
   trả đúng `max` ký tự đầu, không chấm.

Mọi phương thức đều trả giá trị; không hàm nào in. Tự do viết hàm phụ —
grader chỉ gọi ba điểm vào public.
'''

CK_M5_CH = challenge(
    "javb-checkpoint-methods",
    "Checkpoint: Text Toolkit",
    CK_M5_MD,
    r'''public class Solution {
    public static String initials(String fullName) {
        return "";
    }

    public static boolean isPalindrome(String text) {
        return false;
    }

    public static String truncate(String text, int max) {
        return "";
    }
}
''',
    [
        (
            "initials",
            r"""
CjTestBase.checkEq(Solution.initials("ada byron lovelace"), "ABL", "three words");
CjTestBase.checkEq(Solution.initials("  grace   hopper "), "GH", "extra spaces");
CjTestBase.checkEq(Solution.initials(""), "", "empty");
CjTestBase.checkEq(Solution.initials(null), "", "null");
""",
            "Split on whitespace, take first char of each token, uppercase, join.",
        ),
        (
            "isPalindrome",
            r"""
CjTestBase.checkTrue(Solution.isPalindrome("A man, a plan, a canal: Panama!"), "the classic panama palindrome");
CjTestBase.checkTrue(Solution.isPalindrome("Noon"), "case-insensitive");
CjTestBase.checkTrue(!Solution.isPalindrome("hello"), "not a palindrome");
CjTestBase.checkTrue(!Solution.isPalindrome(""), "empty is false by contract");
""",
            "Keep letters only, lowercase, compare with reversed.",
        ),
        (
            "truncate",
            r"""
CjTestBase.checkEq(Solution.truncate("programming", 7), "program...", "shortened");
CjTestBase.checkEq(Solution.truncate("short", 10), "short", "untouched");
CjTestBase.checkEq(Solution.truncate("abcdef", 3), "abc", "no room for dots");
""",
            "Dots only when text.length() > max; max < 4 means no dots.",
        ),
    ],
    difficulty="beginner",
)

CK_M5_VI = vi_challenge(
    "Checkpoint: Bộ công cụ văn bản",
    CK_M5_MD_VI,
    [
        ("initials", "Tách theo khoảng trắng, lấy ký tự đầu mỗi token, viết hoa, nối."),
        ("isPalindrome", "Giữ chữ cái, viết thường, so với bản đảo."),
        ("truncate", "Chỉ có chấm khi text.length() > max; max < 4 nghĩa là không chấm."),
    ],
)

CK_M5_R = r'''public class Solution {
    public static String initials(String fullName) {
        if (fullName == null || fullName.isBlank()) {
            return "";
        }
        StringBuilder out = new StringBuilder();
        for (String token : fullName.trim().split("\\s+")) {
            out.append(Character.toUpperCase(token.charAt(0)));
        }
        return out.toString();
    }

    public static boolean isPalindrome(String text) {
        if (text == null) {
            return false;
        }
        StringBuilder letters = new StringBuilder();
        for (char c : text.toCharArray()) {
            if (Character.isLetter(c)) {
                letters.append(Character.toLowerCase(c));
            }
        }
        String s = letters.toString();
        return s.length() > 0 && s.equals(new StringBuilder(s).reverse().toString());
    }

    public static String truncate(String text, int max) {
        if (text == null || text.length() <= max) {
            return text == null ? "" : text;
        }
        if (max < 4) {
            return text.substring(0, max);
        }
        return text.substring(0, max) + "...";
    }
}
'''

CK_M5_W = r'''public class Solution {
    public static String initials(String fullName) {
        if (fullName == null || fullName.isBlank()) {
            return "";
        }
        StringBuilder out = new StringBuilder();
        for (String token : fullName.trim().split("\\s+")) {
            out.append(Character.toUpperCase(token.charAt(0)));
        }
        return out.toString();
    }

    public static boolean isPalindrome(String text) {
        if (text == null) {
            return false;
        }
        StringBuilder letters = new StringBuilder();
        for (char c : text.toCharArray()) {
            if (Character.isLetter(c)) {
                letters.append(Character.toLowerCase(c));
            }
        }
        String s = letters.toString();
        // BUG: forgets the reversal — every non-empty text "is a palindrome"
        return s.length() > 0;
    }

    public static String truncate(String text, int max) {
        if (text == null || text.length() <= max) {
            return text == null ? "" : text;
        }
        if (max < 4) {
            return text.substring(0, max);
        }
        return text.substring(0, max) + "...";
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Methods & Program Design",
    "Signatures and returns, static demystified, overloading and varargs, and decomposition: turning copies into named, testable units.",
    "Phương thức & Thiết kế chương trình",
    "Chữ ký và return, giải mã static, overloading và varargs, và phân rã: biến bản sao thành đơn vị có tên, kiểm thử được.",
    ["methods-parameters-returns", "static-members", "overloading-varargs", "decomposition", "java-checkpoint-methods"],
    ["javb-p5-methods"],
)

write_lesson(
    MOD, "methods-parameters-returns",
    "Methods, Parameters & Returns",
    "Anatomy of a signature, return-on-every-path, and why parameters are copies.", 15,
    L_METHODS_EN,
    "Phương thức, tham số & giá trị trả về",
    "Giải phẫu chữ ký, return trên mọi đường đi, và vì sao tham số là bản sao.",
    L_METHODS_VI,
)

write_lesson(
    MOD, "java-static-members",
    "static: Class-Level Members",
    "Why main is static, static final constants, the non-static-context error, and avoiding mutable global state.", 15,
    L_STATIC_EN,
    "static: thành phần cấp class",
    "Vì sao main là static, hằng static final, lỗi non-static-context, và tránh trạng thái toàn cục có thể đổi.",
    L_STATIC_VI,
)

write_lesson(
    MOD, "overloading-varargs",
    "Overloading & Varargs",
    "One name, several parameter lists; delegation over duplication; varargs as the last parameter.", 15,
    L_OVERLOAD_EN,
    "Overloading & Varargs",
    "Một tên, nhiều danh sách tham số; ủy quyền thay vì sao chép; varargs là tham số cuối.",
    L_OVERLOAD_VI,
)

write_lesson(
    MOD, "decomposition",
    "Decomposition & Refactoring",
    "One job per method, the rule of three-ish, and returning results instead of printing them.", 15,
    L_DECOMPOSE_EN,
    "Phân rã & Refactoring",
    "Mỗi phương thức một việc, quy tắc ba-nói-chưa-sát, và trả kết quả thay vì in ra.",
    L_DECOMPOSE_VI,
)

write_practice(
    MOD, "javb-p5-methods",
    "Practice: Utility Library",
    "Build repeat/clamp/isBlank, an overload family, a decomposed receipt, and repair an untestable printer.",
    "Thực hành: Thư viện tiện ích",
    "Xây repeat/clamp/isBlank, một họ overload, hóa đơn phân rã, và sửa một cái máy in không kiểm thử được.",
    "decomposition", 55, "beginner",
    [P5_UTIL, P5_OVERLOAD, P5_DECOMPOSE, P5_FIX],
    {c["id"]: v for c, v in [
        (P5_UTIL, P5_UTIL_VI), (P5_OVERLOAD, P5_OVERLOAD_VI),
        (P5_DECOMPOSE, P5_DECOMPOSE_VI), (P5_FIX, P5_FIX_VI)]},
    solutions=[
        (
            P5_UTIL["id"],
            r'''public class Solution {
    public static String repeat(String s, int n) {
        if (n <= 0) return "";
        return s.repeat(n);
    }

    public static int clamp(int v, int min, int max) {
        return Math.max(min, Math.min(max, v));
    }

    public static boolean isBlank(String s) {
        return s == null || s.isBlank();
    }
}
''',
            r'''public class Solution {
    public static String repeat(String s, int n) {
        if (n <= 0) return "";
        // BUG: off by one — one copy short
        return s.repeat(n - 1);
    }

    public static int clamp(int v, int min, int max) {
        return Math.max(min, Math.min(max, v));
    }

    public static boolean isBlank(String s) {
        return s == null || s.isBlank();
    }
}
''',
        ),
        (
            P5_OVERLOAD["id"],
            r'''public class Solution {
    public static String join(String sep, String a, String b) {
        return join(sep, new String[]{a, b});
    }

    public static String join(String sep, String a, String b, String c) {
        return join(sep, new String[]{a, b, c});
    }

    public static String join(String sep, String... parts) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) out.append(sep);
            out.append(parts[i]);
        }
        return out.toString();
    }
}
''',
            r'''public class Solution {
    public static String join(String sep, String a, String b) {
        // BUG: separator also glued at the end
        return a + sep + b + sep;
    }

    public static String join(String sep, String a, String b, String c) {
        return a + sep + b + sep + c;
    }

    public static String join(String sep, String... parts) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) out.append(sep);
            out.append(parts[i]);
        }
        return out.toString();
    }
}
''',
        ),
        (
            P5_DECOMPOSE["id"],
            r'''public class Solution {
    public static String formatMoney(double amount) {
        return String.format("$%.2f", amount);
    }

    public static String line(String item, int qty, double price) {
        return item + " x" + qty + " = " + formatMoney(qty * price);
    }
}
''',
            r'''public class Solution {
    public static String formatMoney(double amount) {
        // BUG: one decimal place
        return String.format("$%.1f", amount);
    }

    public static String line(String item, int qty, double price) {
        return item + " x" + qty + " = " + formatMoney(qty * price);
    }
}
''',
        ),
        (
            P5_FIX["id"],
            r'''public class Solution {
    public static String category(double bmi) {
        if (bmi < 18.5) return "under";
        if (bmi < 25) return "normal";
        return "over";
    }

    public static String bmiReport(double weightKg, double heightM) {
        double bmi = weightKg / (heightM * heightM);
        return "BMI " + bmi + " " + category(bmi);
    }
}
''',
            r'''public class Solution {
    public static String category(double bmi) {
        // BUG: 18.5 boundary wrong side
        if (bmi <= 18.5) return "under";
        if (bmi < 25) return "normal";
        return "over";
    }

    public static String bmiReport(double weightKg, double heightM) {
        double bmi = weightKg / (heightM * heightM);
        return "BMI " + bmi + " " + category(bmi);
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-methods",
    "Checkpoint: Text Toolkit",
    "Three string utilities with precise contracts: decomposition, null-safety, and boundary thinking in one library.", 45, CK_M5_MD,
    "Checkpoint: Bộ công cụ văn bản",
    "Ba tiện ích chuỗi với hợp đồng chính xác: phân rã, an toàn null, và tư duy biên trong một thư viện.",
    CK_M5_MD_VI,
    CK_M5_CH, CK_M5_VI,
    solution=CK_M5_R, wrong=CK_M5_W,
)

print("module 5 complete")
