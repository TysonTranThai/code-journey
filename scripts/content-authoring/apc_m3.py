#!/usr/bin/env python3
"""AP CSA M3 — Expressions and Operators (precedence, logic, short-circuit)."""
from apc import *

M = "apc-expressions"

L1 = r"""
**Arithmetic operators**: `+  -  *  /  %` with the precedence you expect
(`*`, `/`, `%` bind tighter than `+`, `-`), left to right among equals.

```java
System.out.println(2 + 3 * 4);      // 14, not 20
System.out.println((2 + 3) * 4);    // 20 — parentheses win
System.out.println(10 - 4 - 3);     // 3  — left to right
```

**Relational operators** produce a `boolean`: `<  >  <=  >=  ==  !=`.

```java
int x = 5;
System.out.println(x < 10);     // true
System.out.println(x == 5);     // true — == compares values
System.out.println(x != 5);     // false
```

The single `=` assigns; the double `==` compares. `if (x = 5)` does not even
compile in Java (an `int` is not a `boolean`) — a lucky protection.

**Increment and decrement**:

```java
int n = 5;
n++;        // n is 6 (statement form: same as n = n + 1)
n--;        // n is 5
```

As a *statement* (the AP-exam form), `n++` and `++n` are identical. Only
inside a larger expression do `++n` (increment then use) and `n++` (use then
increment) differ — a distinction the exam tests by asking what a
*statement sequence* prints, so trace one statement at a time.
"""

L2 = r"""
**Logical operators** combine booleans:

- `!a` — not: flips it
- `a && b` — and: true only when **both** are true
- `a || b` — or: true when **at least one** is true

Precedence: `!` before `&&` before `||`.

```java
boolean hasTicket = true, isStudent = false;
System.out.println(hasTicket && !isStudent);   // true
System.out.println(!hasTicket || isStudent);   // false
```

**Short-circuit evaluation** — `&&` and `||` stop as soon as the answer is
known, and the right side may never run:

```java
int d = 0;
if (d != 0 && 10 / d > 2) { ... }   // safe: right side skipped when d == 0
```

This is not just an optimization — it is the standard **guard pattern**:
check the risky condition *after* `&&` and the cheap range-check *before*.
`||` short-circuits too: if the left side is `true`, the right side never
runs.

Truth-table tracing is an exam staple: for each combination, write the
value of each sub-expression, then combine.
"""

L3 = r"""
**Compound assignment**: `x += 5` means `x = x + 5`. Same for `-=`, `*=`,
`/=` and `%=`. One subtlety: `x += 2.5` compiles even when `x` is an `int`
(the compound form contains a hidden cast) — but plain `x = x + 2.5` does
not. Prefer the explicit cast for clarity; know the rule for tracing.

**Operator precedence ladder** (high to low):

1. `++ -- !` (unary)
2. `* / %`
3. `+ -`
4. relational `< > <= >=`
5. equality `== !=`
6. `&&`
7. `||`
8. assignment `= += -= ...`

Two classics:

```java
System.out.println(3 < 5 == true);    // true — relational before equality
boolean ok = 5 > 3 && 2 > 1 || 1 > 2; // (true && true) || false → true
```

When in doubt (in reading *or* writing), use parentheses. The exam expects
you to evaluate by the ladder, but human readers thank you for clarity.
"""

write_module(
    M,
    "Expressions and Operators",
    "Arithmetic, relational and logical operators, precedence, increment, compound assignment, and short-circuit guards.",
    "Biểu thức và toán tử",
    "Toán tử số học, quan hệ và logic, độ ưu tiên, tăng/giảm, gán hợp nhất, và chốt điều kiện bằng đánh giá ngắn mạch.",
    lessons=["apc-m3-arith", "apc-m3-logic", "apc-m3-precedence", "apc-cp-m3"],
    practices=["apc-p3-expressions"],
)

write_lesson(
    M, "apc-m3-arith", "Arithmetic, relational, increment",
    "Operator families, == vs =, and ++ / -- as statements.",
    12, L1,
    "Số học, quan hệ, tăng/giảm",
    "Các họ toán tử, == so với =, và ++ / -- dạng câu lệnh.",
    r"""
**Toán tử số học**: `+  -  *  /  %` với độ ưu tiên như bạn mong đợi (`*`,
`/`, `%` chặt hơn `+`, `-`), tính trái sang phải giữa các toán tử cùng cấp.

```java
System.out.println(2 + 3 * 4);      // 14, không phải 20
System.out.println((2 + 3) * 4);    // 20 — ngoặc thắng
System.out.println(10 - 4 - 3);     // 3  — trái sang phải
```

**Toán tử quan hệ** tạo ra `boolean`: `<  >  <=  >=  ==  !=`.

```java
int x = 5;
System.out.println(x < 10);     // true
System.out.println(x == 5);     // true — == so sánh giá trị
System.out.println(x != 5);     // false
```

Một dấu `=` là gán; hai dấu `==` là so sánh. `if (x = 5)` thậm chí không
biên dịch trong Java (một `int` không phải `boolean`) — một lớp bảo vệ may
mắn.

**Tăng và giảm**:

```java
int n = 5;
n++;        // n là 6 (dạng câu lệnh: giống n = n + 1)
n--;        // n là 5
```

Dạng *câu lệnh* (dạng đề thi dùng), `n++` và `++n` giống hệt nhau. Chỉ khi
nằm trong biểu thức lớn hơn thì `++n` (tăng rồi dùng) và `n++` (dùng rồi
tăng) mới khác nhau — đề thi kiểm tra điều này bằng cách hỏi một *dãy câu
lệnh* in ra gì, nên hãy truy vết từng câu lệnh một.
""",
)

write_lesson(
    M, "apc-m3-logic", "Logical operators and short-circuit",
    "!, &&, ||, truth tables, and the short-circuit guard pattern.",
    14, L2,
    "Toán tử logic và ngắn mạch",
    "!, &&, ||, bảng chân trị, và mẫu chốt điều kiện bằng đánh giá ngắn mạch.",
    r"""
**Toán tử logic** kết hợp các giá trị boolean:

- `!a` — phủ định: lật lại
- `a && b` — và: chỉ đúng khi **cả hai** đúng
- `a || b` — hoặc: đúng khi **ít nhất một** đúng

Độ ưu tiên: `!` trước `&&` trước `||`.

```java
boolean hasTicket = true, isStudent = false;
System.out.println(hasTicket && !isStudent);   // true
System.out.println(!hasTicket || isStudent);   // false
```

**Đánh giá ngắn mạch** — `&&` và `||` dừng ngay khi biết kết quả, và vế phải
có thể không bao giờ chạy:

```java
int d = 0;
if (d != 0 && 10 / d > 2) { ... }   // an toàn: vế phải bị bỏ qua khi d == 0
```

Đây không chỉ là tối ưu — đó là **mẫu chốt điều kiện** chuẩn: kiểm tra điều
kiện nguy hiểm *sau* `&&` và kiểm tra khoảng giá trị rẻ tiền *trước*. `||`
cũng ngắn mạch: nếu vế trái `true`, vế phải không bao giờ chạy.

Truy vết bảng chân trị là món đặc sản của đề thi: với từng kết hợp, viết giá
trị của từng biểu thức con, rồi kết hợp lại.
""",
)

write_lesson(
    M, "apc-m3-precedence", "Precedence and compound assignment",
    "The full operator ladder and += -= *= /= %=.",
    10, L3,
    "Độ ưu tiên và gán hợp nhất",
    "Toàn bộ thang độ ưu tiên toán tử và += -= *= /= %=.",
    r"""
**Gán hợp nhất**: `x += 5` nghĩa là `x = x + 5`. Tương tự `-=`, `*=`, `/=`,
`%=`. Một chi tiết tinh tế: `x += 2.5` biên dịch được cả khi `x` là `int`
(dạng hợp nhất chứa một phép ép kiểu ngầm) — nhưng `x = x + 2.5` thì không.
Nên dùng ép kiểu tường minh cho rõ ràng; vẫn phải biết luật này khi truy
vết.

**Thang độ ưu tiên** (cao xuống thấp):

1. `++ -- !` (một ngôi)
2. `* / %`
3. `+ -`
4. quan hệ `< > <= >=`
5. so sánh bằng `== !=`
6. `&&`
7. `||`
8. gán `= += -= ...`

Hai ví dụ kinh điển:

```java
System.out.println(3 < 5 == true);    // true — quan hệ trước so sánh bằng
boolean ok = 5 > 3 && 2 > 1 || 1 > 2; // (true && true) || false → true
```

Khi nghi ngờ (khi đọc *hay* khi viết), dùng ngoặc. Đề thi bắt bạn đánh giá
theo thang độ ưu tiên, nhưng người đọc sẽ cảm ơn bạn vì sự rõ ràng.
""",
)

BOILER_HALF = r"""public class Solution {
    public static boolean isHalfway(int grade) {
        return false; // replace: true when grade is at least 50
    }
}
"""

BOILER_BETWEEN = r"""public class Solution {
    public static boolean inRange(int x, int lo, int hi) {
        return false; // replace: lo <= x <= hi
    }
}
"""

BOILER_DIVIDES = r"""public class Solution {
    public static boolean dividesEvenly(int a, int b) {
        return false; // replace: true when a % b == 0
    }
}
"""

BOILER_CLUB = r"""public class Solution {
    public static boolean canJoin(int age, boolean member) {
        return false; // replace: see prompt
    }
}
"""

CP_LEAP = r"""public class Solution {
    public static boolean isLeap(int year) {
        return false; // replace
    }
}
"""

P_HALF = challenge(
    "apc-m3-halfway",
    "Relational to boolean",
    "Implement `boolean isHalfway(int grade)`: true exactly when `grade >= 50`. One return statement.",
    BOILER_HALF,
    [(
        "boundary correct",
        r"""
CjTestBase.checkTrue(Solution.isHalfway(50), "boundary 50 counts");
CjTestBase.checkTrue(Solution.isHalfway(100), "top");
CjTestBase.checkTrue(!Solution.isHalfway(49), "49 is below");
CjTestBase.checkTrue(!Solution.isHalfway(0), "zero");
""",
        ">=, not >: the boundary itself is included.",
    )],
    level="imitation",
)

P_RANGE = challenge(
    "apc-m3-inrange",
    "Between two bounds",
    "Implement `boolean inRange(int x, int lo, int hi)`: true when `lo <= x` AND `x <= hi`. Java has no `lo <= x <= hi` chain — you must combine two comparisons with `&&`.",
    BOILER_BETWEEN,
    [(
        "range edges",
        r"""
CjTestBase.checkTrue(Solution.inRange(5, 1, 10), "middle");
CjTestBase.checkTrue(Solution.inRange(1, 1, 10), "low edge included");
CjTestBase.checkTrue(Solution.inRange(10, 1, 10), "high edge included");
CjTestBase.checkTrue(!Solution.inRange(11, 1, 10), "above");
CjTestBase.checkTrue(!Solution.inRange(0, 1, 10), "below");
""",
        "Two comparisons joined by &&; both edges are inclusive.",
    )],
    level="guided",
)

P_MOD = challenge(
    "apc-m3-divides",
    "Remainder check",
    "Implement `boolean dividesEvenly(int a, int b)`: true when `b` divides `a` with no remainder. Careful with `b == 0`: division by zero never happens because `&&` short-circuits — return false when `b` is 0.",
    BOILER_DIVIDES,
    [(
        "remainder logic",
        r"""
CjTestBase.checkTrue(Solution.dividesEvenly(10, 2), "10/2 clean");
CjTestBase.checkTrue(!Solution.dividesEvenly(10, 3), "10/3 has remainder");
CjTestBase.checkTrue(Solution.dividesEvenly(0, 5), "0 is divisible");
CjTestBase.checkTrue(!Solution.dividesEvenly(5, 0), "zero divisor is false");
""",
        "b != 0 && a % b == 0 — the guard runs first and short-circuits.",
    )],
    level="combination",
)

P_CLUB = challenge(
    "apc-m3-club",
    "Truth-table logic",
    "Implement `boolean canJoin(int age, boolean member)`: true when age is at least 16 **and** at most 25, regardless of membership; OR age is 26 or older **and** already a member. Build it from range checks, `&&`, `||`.",
    BOILER_CLUB,
    [(
        "all four cases",
        r"""
CjTestBase.checkTrue(Solution.canJoin(20, false), "young non-member");
CjTestBase.checkTrue(Solution.canJoin(20, true), "young member");
CjTestBase.checkTrue(Solution.canJoin(30, true), "older member");
CjTestBase.checkTrue(!Solution.canJoin(30, false), "older non-member");
CjTestBase.checkTrue(!Solution.canJoin(15, true), "too young");
""",
        "(16 <= age && age <= 25) || (age >= 26 && member)",
    )],
    level="independent",
)

CP3 = challenge(
    "apc-cp-m3-leap",
    "Checkpoint: leap-year logic",
    "Implement `boolean isLeap(int year)`: true when `year` is divisible by 4, EXCEPT century years (divisible by 100) unless also divisible by 400. So 2024 → true, 1900 → false, 2000 → true, 2023 → false.",
    CP_LEAP,
    [(
        "leap rules",
        r"""
CjTestBase.checkTrue(Solution.isLeap(2024), "divisible by 4");
CjTestBase.checkTrue(!Solution.isLeap(1900), "century, not 400");
CjTestBase.checkTrue(Solution.isLeap(2000), "divisible by 400");
CjTestBase.checkTrue(!Solution.isLeap(2023), "common year");
CjTestBase.checkTrue(Solution.isLeap(4), "year 4 is a leap year");
""",
        "divisible by 4 && (!divisible by 100 || divisible by 400)",
    )],
    level="independent",
)

write_practice(
    M, "apc-p3-expressions", "Evaluate everything", "Relational guards, short-circuit safety, truth tables.",
    "Tính giá trị mọi thứ", "Chốt điều kiện quan hệ, an toàn ngắn mạch, bảng chân trị.",
    after_lesson="apc-m3-logic", minutes=40, difficulty="beginner",
    challenges=[P_HALF, P_RANGE, P_MOD, P_CLUB],
    vi_challenges={
        "apc-m3-halfway": vi_challenge("Quan hệ thành boolean", "Cài đặt `boolean isHalfway(int grade)`: đúng chính xác khi `grade >= 50`. Một câu lệnh return.",
            [("boundary correct", ">=, không phải >: chính ranh giới được tính vào.")]),
        "apc-m3-inrange": vi_challenge("Nằm giữa hai cận", "Cài đặt `boolean inRange(int x, int lo, int hi)`: đúng khi `lo <= x` VÀ `x <= hi`. Java không có chuỗi `lo <= x <= hi` — phải kết hợp hai phép so sánh bằng `&&`.",
            [("range edges", "Hai phép so sánh nối bằng &&; cả hai cận đều gồm biên.")]),
        "apc-m3-divides": vi_challenge("Kiểm tra số dư", "Cài đặt `boolean dividesEvenly(int a, int b)`: đúng khi `b` chia hết `a`. Cẩn thận với `b == 0`: phép chia cho 0 không bao giờ xảy ra vì `&&` ngắn mạch — trả về false khi `b` là 0.",
            [("remainder logic", "b != 0 && a % b == 0 — chốt điều kiện chạy trước và ngắn mạch.")]),
        "apc-m3-club": vi_challenge("Logic bảng chân trị", "Cài đặt `boolean canJoin(int age, boolean member)`: đúng khi tuổi từ 16 đến 25 (kể cả 16 và 25) bất kể tư cách thành viên; HOẶC tuổi từ 26 trở lên VÀ đã là thành viên. Dựng từ kiểm tra khoảng, `&&`, `||`.",
            [("all four cases", "(16 <= age && age <= 25) || (age >= 26 && member)")]),
    },
    solutions=[
        ("apc-m3-halfway", r"""public class Solution {
    public static boolean isHalfway(int grade) {
        return grade >= 50;
    }
}
""",
         r"""public class Solution {
    public static boolean isHalfway(int grade) {
        // BUG: excludes the boundary itself
        return grade > 50;
    }
}
"""),
        ("apc-m3-inrange", r"""public class Solution {
    public static boolean inRange(int x, int lo, int hi) {
        return lo <= x && x <= hi;
    }
}
""",
         r"""public class Solution {
    public static boolean inRange(int x, int lo, int hi) {
        // BUG: || admits everything between the extremes
        return lo <= x || x <= hi;
    }
}
"""),
        ("apc-m3-divides", r"""public class Solution {
    public static boolean dividesEvenly(int a, int b) {
        return b != 0 && a % b == 0;
    }
}
""",
         r"""public class Solution {
    public static boolean dividesEvenly(int a, int b) {
        // BUG: no zero guard — but this fails 5,0 by crashing, and
        // BUG: also claims 10 % 3 == 1 is even division? no: crashes first.
        return a % b == 0;
    }
}
""".replace("// BUG: also claims 10 % 3 == 1 is even division? no: crashes first.\n        ", "")),
        ("apc-m3-club", r"""public class Solution {
    public static boolean canJoin(int age, boolean member) {
        return (age >= 16 && age <= 25) || (age >= 26 && member);
    }
}
""",
         r"""public class Solution {
    public static boolean canJoin(int age, boolean member) {
        // BUG: lets older non-members in too
        return (age >= 16 && age <= 25) || age >= 26;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m3", "Checkpoint: operator logic",
    "Leap-year reasoning with %, relational chains, && and || combined.",
    18,
    r"""
The leap-year rule is a genuine AP-style logic exercise: translate English
conditions with exceptions into one boolean expression, then verify against
known years.
""",
    "Điểm kiểm tra: logic toán tử",
    "Suy luận năm nhuận với %, chuỗi quan hệ, && và || kết hợp.",
    r"""
Luật năm nhuận là bài tập logic đúng phong cách AP: dịch các điều kiện tiếng
Anh có ngoại lệ thành một biểu thức boolean, rồi xác minh với các năm đã
biết.
""",
    CP3,
    vi_challenge("Điểm kiểm tra: logic toán tử", "Cài đặt `boolean isLeap(int year)`: đúng khi `year` chia hết cho 4, TRỪ các năm thế kỷ (chia hết cho 100) trừ khi cũng chia hết cho 400. Vậy 2024 → true, 1900 → false, 2000 → true, 2023 → false.",
        [("leap rules", "chia hết 4 && (!chia hết 100 || chia hết 400)")]),
    solution=r"""public class Solution {
    public static boolean isLeap(int year) {
        return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
    }
}
""",
    wrong=r"""public class Solution {
    public static boolean isLeap(int year) {
        // BUG: forgets the century exception — 1900 wrongly leaps
        return year % 4 == 0;
    }
}
""",
)
