#!/usr/bin/env python3
"""Java — Beginner — Module 3: java-conditions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-conditions"

L_IF_EN = r'''
Programs make decisions with `if`, `else if`, and `else`:

```java
int temperature = 31;

if (temperature > 30) {
    System.out.println("Stay hydrated");
} else if (temperature > 20) {
    System.out.println("Perfect weather");
} else {
    System.out.println("Bring a jacket");
}
```

The conditions are tested **top to bottom**, and only the FIRST true branch
runs — once one matches, the rest are skipped entirely. That ordering is
part of your program's logic: testing `temperature > 20` first would make
the `> 30` branch unreachable.

The parentheses hold a boolean expression; the braces hold the code to run.
Braces are **never optional in this course**, even for one statement:

```java
if (active) System.out.println("on");   // legal, but a maintenance trap
```

Without braces, only the next single statement belongs to the `if` — the
famous "Apple goto fail" bug class. Always write the braces.

Conditions can **nest**, but deep nesting is a smell:

```java
if (user != null) {
    if (user.isActive()) {
        if (user.hasPermission("write")) {
            // three levels deep — hard to follow
        }
    }
}
```

The same logic, flat and readable, using the `&&` from Module 2:

```java
if (user != null && user.isActive() && user.hasPermission("write")) {
    // one clear gate
}
```

**Scope note:** variables declared inside a branch disappear at its closing
brace. Declare result variables *before* the branches if all branches
contribute to them.

**Next:** `switch` — decisions by value.
'''

L_IF_VI = r'''
Chương trình ra quyết định bằng `if`, `else if`, và `else`:

```java
int temperature = 31;

if (temperature > 30) {
    System.out.println("Stay hydrated");
} else if (temperature > 20) {
    System.out.println("Perfect weather");
} else {
    System.out.println("Bring a jacket");
}
```

Các điều kiện được kiểm tra **từ trên xuống**, và CHỈ nhánh đúng ĐẦU TIÊN
chạy — khi một nhánh khớp, phần còn lại bị bỏ qua hoàn toàn. Thứ tự đó là
một phần logic chương trình: kiểm tra `temperature > 20` trước sẽ khiến
nhánh `> 30` không bao giờ với tới.

Dấu ngoặc chứa biểu thức boolean; dấu ngoặc nhọn chứa code sẽ chạy. Trong
khóa học này ngoặc nhọn **không bao giờ tùy chọn**, kể cả cho một câu lệnh:

```java
if (active) System.out.println("on");   // hợp lệ, nhưng là bẫy bảo trì
```

Không có ngoặc nhọn, chỉ câu lệnh tiếp theo thuộc về `if` — dòng lỗi "Apple
goto fail" nổi tiếng. Luôn viết ngoặc nhọn.

Điều kiện có thể **lồng nhau**, nhưng lồng sâu là mùi code xấu:

```java
if (user != null) {
    if (user.isActive()) {
        if (user.hasPermission("write")) {
            // ba tầng sâu — khó theo dõi
        }
    }
}
```

Cùng logic đó, phẳng và dễ đọc, dùng `&&` từ Module 2:

```java
if (user != null && user.isActive() && user.hasPermission("write")) {
    // một cổng kiểm tra rõ ràng
}
```

**Ghi nhớ phạm vi:** biến khai báo trong một nhánh biến mất ở ngoặc nhọn
đóng của nhánh đó. Khai báo biến kết quả *trước* các nhánh nếu mọi nhánh
cùng góp giá trị cho nó.

**Tiếp theo:** `switch` — quyết định theo giá trị.
'''

L_SWITCH_EN = r'''
When one variable is compared against several constant values, `switch`
reads better than an `if` ladder:

```java
switch (choice) {
    case 1:
        System.out.println("Coffee");
        break;
    case 2:
        System.out.println("Tea");
        break;
    default:
        System.out.println("Unknown");
        break;
}
```

`switch` works on `int`, `long`, `char`, `String`, enums, and a few more.
Two rules define the classic form:

- **`break` exits the switch.** Without it, execution *falls through* into
  the next case — occasionally useful deliberately ("cases 1 and 2 share
  this code"), famously dangerous by accident. Miss a `break` and the
  compiler stays silent while your menu prints everything below it.
- **`default` is the else** — the case for every value you did not list.
  Always write one, even when you believe the values are closed.

**The modern form: switch expressions** (Java 14+). The arrow `->` runs
exactly one branch, no fall-through, no break, and the whole switch
*produces a value*:

```java
String drink = switch (choice) {
    case 1 -> "Coffee";
    case 2 -> "Tea";
    default -> "Unknown";
};
```

Multiple labels share one arm: `case 1, 2 -> "Hot drink";`. When an arm
needs several statements, use braces and `yield`:

```java
String label = switch (code) {
    case "A" -> "approved";
    default -> {
        System.out.println("unknown code: " + code);
        yield "rejected";
    }
};
```

A switch expression must be **exhaustive** — the compiler forces a default
(or all cases covered) because the result must always exist. The compiler
checking your decision table for completeness is exactly the kind of ally
this course keeps returning to.

**Next:** designing validations that fail loudly and politely.
'''

L_SWITCH_VI = r'''
Khi một biến được so sánh với vài giá trị hằng, `switch` dễ đọc hơn thang
`if`:

```java
switch (choice) {
    case 1:
        System.out.println("Coffee");
        break;
    case 2:
        System.out.println("Tea");
        break;
    default:
        System.out.println("Unknown");
        break;
}
```

`switch` hoạt động với `int`, `long`, `char`, `String`, enum, và vài loại
khác. Hai quy tắc định nghĩa dạng cổ điển:

- **`break` thoát khỏi switch.** Không có nó, chương trình *rơi xuống* case
  kế tiếp — thỉnh thoảng hữu ích một cách chủ đích ("case 1 và 2 dùng chung
  code"), và nổi tiếng nguy hiểm khi vô ý. Thiếu một `break`, compiler im
  lặng trong khi menu của bạn in mọi lựa chọn bên dưới.
- **`default` là else** — case cho mọi giá trị bạn không liệt kê. Luôn viết
  một cái, kể cả khi bạn tin tập giá trị đã đóng.

**Dạng hiện đại: switch expression** (Java 14+). Mũi tên `->` chạy đúng
một nhánh, không rơi xuống, không break, và cả switch *trả về một giá trị*:

```java
String drink = switch (choice) {
    case 1 -> "Coffee";
    case 2 -> "Tea";
    default -> "Unknown";
};
```

Nhiều nhãn dùng chung một nhánh: `case 1, 2 -> "Hot drink";`. Khi một nhánh
cần nhiều câu lệnh, dùng ngoặc nhọn và `yield`:

```java
String label = switch (code) {
    case "A" -> "approved";
    default -> {
        System.out.println("unknown code: " + code);
        yield "rejected";
    }
};
```

Switch expression phải **đầy đủ** — compiler buộc bạn viết default (hoặc
phủ hết các case) vì kết quả phải luôn tồn tại. Compiler kiểm tra bảng quyết
định của bạn về tính đầy đủ đúng là loại đồng minh mà khóa học này luôn
quay lại với bạn.

**Tiếp theo:** thiết kế xác thực đầu vào — từ chối to và lịch sự.
'''

L_VALIDATION_EN = r'''
Real programs spend more lines refusing bad input than celebrating good
input. Three habits make validation clean.

**1. Validate at the edge, early.** Check everything the function needs in
one guard clause at the top, then write the happy path without interruptions:

```java
static double monthlyPayment(double principal, int months) {
    if (months <= 0) {
        throw new IllegalArgumentException("months must be positive");
    }
    // happy path, no nested ifs
}
```

You met `throw` here for the first time: refusing to continue when the
contract is broken. Module 12 builds the full machinery; the pattern is
usable from day one.

**2. Refuse with a message worth reading.** `"invalid input"` helps nobody;
`"months must be positive, got -3"` lets the caller fix the call in seconds.

**3. Prefer returning a verdict over printing one.** A method that returns
`"OK"` or the reason it failed is *testable*; a method that just prints can
only be watched. This module's practice set grades returned verdicts for
exactly that reason.

A compact validation table reads beautifully as a switch expression over an
error code, or as a list of guard clauses — whichever makes the contract
obvious at a glance.

**Next:** practice.
'''

L_VALIDATION_VI = r'''
Chương trình thật dành nhiều dòng để từ chối dữ liệu xấu hơn là ăn mừng dữ
liệu tốt. Ba thói quen khiến việc xác thật (validation) sạch sẽ.

**1. Xác thực ở rìa, sớm.** Kiểm tra mọi thứ hàm cần trong một guard clause
ở đầu, rồi viết luồng chính không gián đoạn:

```java
static double monthlyPayment(double principal, int months) {
    if (months <= 0) {
        throw new IllegalArgumentException("months must be positive");
    }
    // luồng chính, không if lồng
}
```

Bạn vừa gặp `throw` lần đầu: từ chối tiếp tục khi hợp đồng bị phá vỡ.
Module 12 xây toàn bộ cơ chế; nhưng pattern này dùng được ngay từ ngày đầu.

**2. Từ chối kèm thông điệp đáng đọc.** `"invalid input"` không giúp ai;
`"months must be positive, got -3"` giúp người gọi sửa trong vài giây.

**3. Ưu tiên trả về phán quyết thay vì in ra.** Hàm trả `"OK"` hoặc lý do
thất bại thì *kiểm thử được*; hàm chỉ in thì chỉ có thể nhìn. Bộ thực hành
của module này chấm điểm phán quyết trả về chính vì lý do đó.

Một bảng xác thực gọn đọc rất đẹp dưới dạng switch expression theo mã lỗi,
hoặc danh sách guard clause — cách nào làm hợp đồng hiển rõ trong một cái
nhìn thì dùng cách đó.

**Tiếp theo:** thực hành.
'''

# ── practice set 3 ──────────────────────────────────────────────────────────
P3_ELIGIBLE = challenge(
    "javb-m3-eligibility",
    "Club eligibility gate",
    "Implement `String eligibility(int age, boolean member)`: return "
    "`\"welcome\"` when age is 18+ AND member; `\"join us\"` when age is 18+ "
    "but not a member; `\"come back later\"` otherwise (under 18).",
    r'''public class Solution {
    public static String eligibility(int age, boolean member) {
        return "";
    }
}
''',
    [
        (
            "member adult",
            r"""
CjTestBase.checkEq(Solution.eligibility(25, true), "welcome", "adult member");
""",
            "18+ and member → welcome.",
        ),
        (
            "adult non-member",
            r"""
CjTestBase.checkEq(Solution.eligibility(25, false), "join us", "adult non-member");
""",
            "18+ without membership gets the invitation.",
        ),
        (
            "underage",
            r"""
CjTestBase.checkEq(Solution.eligibility(15, true), "come back later", "teen member");
""",
            "Under 18 → the polite refusal, member or not.",
        ),
    ],
    level="imitation",
)

P3_ELIGIBLE_VI = vi_challenge(
    "Cổng điều kiện vào CLB",
    "Viết `String eligibility(int age, boolean member)`: trả "
    "`\"welcome\"` khi age 18+ VÀ member; `\"join us\"` khi 18+ nhưng không "
    "phải member; `\"come back later\"` với các trường hợp còn lại (dưới 18).",
    [
        ("member adult", "18+ và member → welcome."),
        ("adult non-member", "18+ không có thẻ nhận lời mời."),
        ("underage", "Dưới 18 → lời từ chối lịch sự, có member hay không."),
    ],
)

P3_LEAP = challenge(
    "javb-m3-leap-year",
    "Leap year, precisely specified",
    "Implement `boolean isLeapYear(int year)`. The full rule: divisible by 4 "
    "→ leap, EXCEPT centuries — divisible by 100 is NOT leap unless also "
    "divisible by 400. So 2000 was leap, 1900 was not, 2024 is.",
    r'''public class Solution {
    public static boolean isLeapYear(int year) {
        return false;
    }
}
''',
    [
        (
            "ordinary leap years",
            r"""
CjTestBase.checkTrue(Solution.isLeapYear(2024), "2024 is leap");
CjTestBase.checkTrue(Solution.isLeapYear(1996), "1996 is leap");
""",
            "Divisible by 4, not a century.",
        ),
        (
            "ordinary non-leap years",
            r"""
CjTestBase.checkTrue(!Solution.isLeapYear(2023), "2023 is not leap");
CjTestBase.checkTrue(!Solution.isLeapYear(1900), "1900 is not leap (century rule)");
""",
            "1900: divisible by 100 but not 400.",
        ),
        (
            "the 400-year exception",
            r"""
CjTestBase.checkTrue(Solution.isLeapYear(2000), "2000 is leap (400 rule)");
""",
            "Divisible by 400 wins over the 100 rule.",
        ),
    ],
    level="guided",
)

P3_LEAP_VI = vi_challenge(
    "Năm nhuận, đúng đặc tả",
    "Viết `boolean isLeapYear(int year)`. Quy tắc đầy đủ: chia hết cho 4 → "
    "nhuận, TRỪ các thế kỷ — chia hết cho 100 thì KHÔNG nhuận trừ khi chia "
    "hết cho 400. Vậy 2000 nhuận, 1900 không, 2024 nhuận.",
    [
        ("ordinary leap years", "Chia hết cho 4, không phải thế kỷ."),
        ("ordinary non-leap years", "1900: chia hết cho 100 nhưng không cho 400."),
        ("the 400-year exception", "Chia hết cho 400 thắng quy tắc 100."),
    ],
)

P3_SHIPPING = challenge(
    "javb-m3-shipping-tiers",
    "Shipping cost tiers",
    "Implement `int shippingCost(int items, boolean prime)`: free (0) when "
    "prime AND at least 1 item; 5 when NOT prime and items >= 10; 8 when NOT "
    "prime and items >= 3; 12 otherwise. Order your checks so the tiers fall "
    "out naturally.",
    r'''public class Solution {
    public static int shippingCost(int items, boolean prime) {
        return 0;
    }
}
''',
    [
        (
            "prime shoppers",
            r"""
CjTestBase.checkEq(Solution.shippingCost(1, true), 0, "prime 1 item");
CjTestBase.checkEq(Solution.shippingCost(50, true), 0, "prime 50 items");
""",
            "Prime always ships free (with at least one item).",
        ),
        (
            "volume tiers",
            r"""
CjTestBase.checkEq(Solution.shippingCost(10, false), 5, "10 items");
CjTestBase.checkEq(Solution.shippingCost(3, false), 8, "3 items");
""",
            "10+ costs 5; 3..9 costs 8.",
        ),
        (
            "small orders",
            r"""
CjTestBase.checkEq(Solution.shippingCost(2, false), 12, "2 items");
""",
            "Below 3 items: the top rate.",
        ),
    ],
    level="independent",
)

P3_SHIPPING_VI = vi_challenge(
    "Các bậc phí vận chuyển",
    "Viết `int shippingCost(int items, boolean prime)`: miễn phí (0) khi "
    "prime VÀ có ít nhất 1 món; 5 khi KHÔNG prime và items >= 10; 8 khi "
    "KHÔNG prime và items >= 3; 12 trong các trường hợp còn lại. Sắp xếp "
    "thứ tự kiểm tra để các bậc tự nhiên hiện ra.",
    [
        ("prime shoppers", "Prime luôn miễn phí (từ một món trở lên)."),
        ("volume tiers", "10+ món giá 5; 3..9 món giá 8."),
        ("small orders", "Dưới 3 món: giá cao nhất."),
    ],
)

P3_MENU = challenge(
    "javb-m3-menu-switch",
    "Menu dispatch with a switch expression",
    "Implement `String dispatch(String command)` using a **switch expression** "
    "(arrow form): `\"start\"` → `\"running\"`, `\"stop\"` → `\"stopped\"`, "
    "`\"pause\"` → `\"paused\"`, and any other command → `\"unknown: \"` plus "
    "the command itself.",
    r'''public class Solution {
    public static String dispatch(String command) {
        return "";
    }
}
''',
    [
        (
            "known commands",
            r"""
CjTestBase.checkEq(Solution.dispatch("start"), "running", "start");
CjTestBase.checkEq(Solution.dispatch("pause"), "paused", "pause");
""",
            "Map each known command to its state word.",
        ),
        (
            "unknown commands",
            r"""
CjTestBase.checkEq(Solution.dispatch("dance"), "unknown: dance", "dance");
CjTestBase.checkEq(Solution.dispatch(""), "unknown: ", "empty command");
""",
            "default arm handles everything else, echoing the input.",
        ),
    ],
    level="combination",
)

P3_MENU_VI = vi_challenge(
    "Điều phối menu bằng switch expression",
    "Viết `String dispatch(String command)` dùng **switch expression** (dạng "
    "mũi tên): `\"start\"` → `\"running\"`, `\"stop\"` → `\"stopped\"`, "
    "`\"pause\"` → `\"paused\"`, và lệnh khác bất kỳ → `\"unknown: \"` cộng "
    "với chính lệnh đó.",
    [
        ("known commands", "Ánh xạ từng lệnh đã biết sang từ trạng thái."),
        ("unknown commands", "Nhánh default xử lý mọi thứ còn lại, nhắc lại đầu vào."),
    ],
)

P3_FIX = challenge(
    "javb-m3-fix-tier",
    "Debug: the always-expensive shipment",
    "Every customer is charged 12. The intended tiers: prime → 0, items >= 10 "
    "→ 5, items >= 3 → 8, else 12. Find and fix the condition bugs (order and "
    "boundary) in `shippingCost`.",
    r'''public class Solution {
    public static int shippingCost(int items, boolean prime) {
        if (items >= 10) {
            return 5;
        }
        if (prime) {
            return 0;
        }
        if (items >= 3) {
            return 8;
        }
        return 12;
    }
}
''',
    [
        (
            "all tiers correct",
            r"""
CjTestBase.checkEq(Solution.shippingCost(1, true), 0, "prime 1 item");
CjTestBase.checkEq(Solution.shippingCost(50, true), 0, "prime bulk is still free");
CjTestBase.checkEq(Solution.shippingCost(10, false), 5, "10 items");
CjTestBase.checkEq(Solution.shippingCost(3, false), 8, "3 items");
CjTestBase.checkEq(Solution.shippingCost(2, false), 12, "2 items");
""",
            "Prime check must come FIRST (bulk prime is free, not 5); volume boundaries stay >=.",
        ),
    ],
    level="debugging",
)

P3_FIX_VI = vi_challenge(
    "Gỡ lỗi: đơn hàng luôn bị tính phí đắt",
    "Mọi khách đều bị tính 12. Các bậc mong muốn: prime → 0, items >= 10 → 5, "
    "items >= 3 → 8, còn lại 12. Tìm và sửa các lỗi điều kiện (thứ tự và biên) "
    "trong `shippingCost`.",
    [("all tiers correct", "Kiểm tra prime phải đứng TRƯỚC; biên số lượng giữ >=.")],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M3_MD = r'''
The Dispatch Desk decides how an order is handled, combining nested logic
with a switch expression.

Write `public static String dispatch(String tier, int weightKg, boolean fragile)`:

1. If `weightKg <= 0`, return `"rejected: bad weight"`.
2. Otherwise classify by `tier` using a **switch expression**:
   - `"standard"` → `"standard-"` + weight class, where weight class is
     `"light"` (weight < 5) or `"heavy"` (5 and above);
   - `"express"` → `"express-"` + weight class (same classes);
   - `"freight"` → `"freight-quoted"` (weight class ignored);
   - any other tier → `"rejected: unknown tier"` (regardless of weight).
3. Fragile orders get `"+"` appended at the very end — but ONLY if the
   result is not a rejection. `dispatch("standard", 3, true)` is
   `"standard-light+"`; `dispatch("gold", 3, false)` is
   `"rejected: unknown tier"` with no plus.

The boundary at 5 belongs to `"heavy"`. Build the result with a `String`
variable, then decide the suffix once.
'''

CK_M3_MD_VI = r'''
Bàn điều phối quyết định cách xử lý đơn hàng, kết hợp logic lồng với switch
expression.

Viết `public static String dispatch(String tier, int weightKg, boolean fragile)`:

1. Nếu `weightKg <= 0`, trả `"rejected: bad weight"`.
2. Còn lại xếp loại theo `tier` bằng **switch expression**:
   - `"standard"` → `"standard-"` + loại cân nặng, với loại cân nặng là
     `"light"` (weight < 5) hoặc `"heavy"` (từ 5 trở lên);
   - `"express"` → `"express-"` + loại cân nặng (cùng quy tắc);
   - `"freight"` → `"freight-quoted"` (bỏ qua loại cân nặng);
   - tier khác bất kỳ → `"rejected: unknown tier"` (bất kể cân nặng).
3. Đơn dễ vỡ được thêm `"+"` ở cuối cùng — nhưng CHỈ khi kết quả không phải
   từ chối. `dispatch("standard", 3, true)` là `"standard-light+"`;
   `dispatch("gold", 3, false)` là `"rejected: unknown tier"` không dấu cộng.

Biên tại 5 thuộc `"heavy"`. Hãy xây chuỗi kết quả bằng một biến `String`,
rồi quyết định hậu tố đúng một lần.
'''

CK_M3_CH = challenge(
    "javb-checkpoint-conditions",
    "Checkpoint: Dispatch Desk",
    CK_M3_MD,
    r'''public class Solution {
    public static String dispatch(String tier, int weightKg, boolean fragile) {
        return "";
    }
}
''',
    [
        (
            "standard and express classes",
            r"""
CjTestBase.checkEq(Solution.dispatch("standard", 3, false), "standard-light", "std light");
CjTestBase.checkEq(Solution.dispatch("standard", 5, false), "standard-heavy", "5 is heavy");
CjTestBase.checkEq(Solution.dispatch("express", 9, false), "express-heavy", "express heavy");
""",
            "Boundary: weight 5 belongs to heavy.",
        ),
        (
            "freight ignores weight",
            r"""
CjTestBase.checkEq(Solution.dispatch("freight", 900, false), "freight-quoted", "freight");
""",
            "Freight always answers with a quote.",
        ),
        (
            "rejections stay clean",
            r"""
CjTestBase.checkEq(Solution.dispatch("gold", 3, false), "rejected: unknown tier", "bad tier");
CjTestBase.checkEq(Solution.dispatch("standard", 0, false), "rejected: bad weight", "zero weight");
""",
            "Both rejections, exactly as specified.",
        ),
        (
            "fragile suffix rules",
            r"""
CjTestBase.checkEq(Solution.dispatch("express", 2, true), "express-light+", "fragile express");
CjTestBase.checkEq(Solution.dispatch("gold", 2, true), "rejected: unknown tier", "fragile rejection gets no plus");
""",
            "Plus only on successful dispatches.",
        ),
    ],
    difficulty="beginner",
)

CK_M3_VI = vi_challenge(
    "Checkpoint: Bàn điều phối",
    CK_M3_MD_VI,
    [
        ("standard and express classes", "Biên: cân nặng 5 thuộc heavy."),
        ("freight ignores weight", "Freight luôn trả lời bằng báo giá."),
        ("rejections stay clean", "Hai trường hợp từ chối, đúng như đặc tả."),
        ("fragile suffix rules", "Dấu cộng chỉ trên điều phối thành công."),
    ],
)

CK_M3_R = r'''public class Solution {
    public static String dispatch(String tier, int weightKg, boolean fragile) {
        if (weightKg <= 0) {
            return "rejected: bad weight";
        }
        String weightClass = weightKg < 5 ? "light" : "heavy";
        String base = switch (tier) {
            case "standard" -> "standard-" + weightClass;
            case "express" -> "express-" + weightClass;
            case "freight" -> "freight-quoted";
            default -> null;
        };
        if (base == null) {
            return "rejected: unknown tier";
        }
        return fragile ? base + "+" : base;
    }
}
'''

CK_M3_W = r'''public class Solution {
    public static String dispatch(String tier, int weightKg, boolean fragile) {
        if (weightKg <= 0) {
            return "rejected: bad weight";
        }
        String weightClass = weightKg < 5 ? "light" : "heavy";
        String base = switch (tier) {
            case "standard" -> "standard-" + weightClass;
            case "express" -> "express-" + weightClass;
            case "freight" -> "freight-quoted";
            default -> null;
        };
        if (base == null) {
            return "rejected: unknown tier";
        }
        // BUG: appends + to every result, including rejections
        return base + "+";
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Conditions: Deciding in Java",
    "if/else chains, classic switch with its fall-through trap, modern switch expressions, and validation patterns that fail loudly.",
    "Điều kiện: ra quyết định trong Java",
    "Chuỗi if/else, switch cổ điển với bẫy rơi xuống, switch expression hiện đại, và pattern xác thực từ chối rõ ràng.",
    ["if-else", "switch-and-expressions", "validation-patterns", "java-checkpoint-conditions"],
    ["javb-p3-decisions"],
)

write_lesson(
    MOD, "if-else",
    "if / else if / else",
    "Top-to-bottom branch testing, the braces rule, flattening nested conditions with &&.", 15,
    L_IF_EN,
    "if / else if / else",
    "Kiểm tra nhánh từ trên xuống, quy tắc ngoặc nhọn, làm phẳng điều kiện lồng bằng &&.",
    L_IF_VI,
)

write_lesson(
    MOD, "switch-and-expressions",
    "switch Statements & Expressions",
    "Fall-through and break, then the arrow form: value-producing, exhaustive, compiler-checked.", 20,
    L_SWITCH_EN,
    "switch dạng câu lệnh & biểu thức",
    "Rơi xuống và break, rồi dạng mũi tên: sinh giá trị, đầy đủ, được compiler kiểm tra.",
    L_SWITCH_VI,
)

write_lesson(
    MOD, "java-validation-patterns",
    "Validation: Refusing Politely",
    "Guard clauses at the edge, error messages worth reading, verdicts you can test.", 15,
    L_VALIDATION_EN,
    "Xác thực: từ chối lịch sự",
    "Guard clause ở rìa, thông điệp lỗi đáng đọc, phán quyết có thể kiểm thử.",
    L_VALIDATION_VI,
)

write_practice(
    MOD, "javb-p3-decisions",
    "Practice: Decisions",
    "Eligibility gates, leap years, pricing tiers, menu dispatch, and one broken condition table to repair.",
    "Thực hành: Ra quyết định",
    "Cổng điều kiện, năm nhuận, bậc giá, điều phối menu, và một bảng điều kiện hỏng cần sửa.",
    "switch-and-expressions", 50, "beginner",
    [P3_ELIGIBLE, P3_LEAP, P3_SHIPPING, P3_MENU, P3_FIX],
    {c["id"]: v for c, v in [
        (P3_ELIGIBLE, P3_ELIGIBLE_VI), (P3_LEAP, P3_LEAP_VI), (P3_SHIPPING, P3_SHIPPING_VI),
        (P3_MENU, P3_MENU_VI), (P3_FIX, P3_FIX_VI)]},
    solutions=[
        (
            P3_ELIGIBLE["id"],
            r'''public class Solution {
    public static String eligibility(int age, boolean member) {
        if (age >= 18 && member) return "welcome";
        if (age >= 18) return "join us";
        return "come back later";
    }
}
''',
            r'''public class Solution {
    public static String eligibility(int age, boolean member) {
        // BUG: inverted membership check
        if (age >= 18 && !member) return "welcome";
        if (age >= 18) return "join us";
        return "come back later";
    }
}
''',
        ),
        (
            P3_LEAP["id"],
            r'''public class Solution {
    public static boolean isLeapYear(int year) {
        if (year % 400 == 0) return true;
        if (year % 100 == 0) return false;
        return year % 4 == 0;
    }
}
''',
            r'''public class Solution {
    public static boolean isLeapYear(int year) {
        // BUG: ignores the century rule
        return year % 4 == 0;
    }
}
''',
        ),
        (
            P3_SHIPPING["id"],
            r'''public class Solution {
    public static int shippingCost(int items, boolean prime) {
        if (prime && items >= 1) return 0;
        if (items >= 10) return 5;
        if (items >= 3) return 8;
        return 12;
    }
}
''',
            r'''public class Solution {
    public static int shippingCost(int items, boolean prime) {
        // BUG: prime check after the volume tiers — 10 items costs 5 even for prime
        if (items >= 10) return 5;
        if (items >= 3) return 8;
        if (prime && items >= 1) return 0;
        return 12;
    }
}
''',
        ),
        (
            P3_MENU["id"],
            r'''public class Solution {
    public static String dispatch(String command) {
        return switch (command) {
            case "start" -> "running";
            case "stop" -> "stopped";
            case "pause" -> "paused";
            default -> "unknown: " + command;
        };
    }
}
''',
            r'''public class Solution {
    public static String dispatch(String command) {
        // BUG: default forgets to echo the command
        return switch (command) {
            case "start" -> "running";
            case "stop" -> "stopped";
            case "pause" -> "paused";
            default -> "unknown";
        };
    }
}
''',
        ),
        (
            P3_FIX["id"],
            r'''public class Solution {
    public static int shippingCost(int items, boolean prime) {
        if (prime && items >= 1) {
            return 0;
        }
        if (items >= 10) {
            return 5;
        }
        if (items >= 3) {
            return 8;
        }
        return 12;
    }
}
''',
            r'''public class Solution {
    public static int shippingCost(int items, boolean prime) {
        // BUG: still the original wrong order
        if (items >= 10) {
            return 5;
        }
        if (prime) {
            return 0;
        }
        if (items >= 3) {
            return 8;
        }
        return 12;
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-conditions",
    "Checkpoint: Dispatch Desk",
    "Weight classes, tier switch expressions, and rejection paths — one decision table, fully specified.", 40, CK_M3_MD,
    "Checkpoint: Bàn điều phối",
    "Loại cân nặng, switch expression theo tier, và các đường từ chối — một bảng quyết định, đặc tả đầy đủ.",
    CK_M3_MD_VI,
    CK_M3_CH, CK_M3_VI,
    solution=CK_M3_R, wrong=CK_M3_W,
)

print("module 3 complete")
