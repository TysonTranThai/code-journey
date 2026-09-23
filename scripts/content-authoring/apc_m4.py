#!/usr/bin/env python3
"""AP CSA M4 — Conditionals (if/else, nesting, boundaries, classification)."""
from apc import *

M = "apc-conditionals"

L1 = r"""
`if` runs a block only when its boolean is true; `else` is the other road.

```java
if (score >= 60) {
    System.out.println("pass");
} else {
    System.out.println("fail");
}
```

**else-if chains** test in order and stop at the first true branch:

```java
if (score >= 90) {
    grade = 'A';
} else if (score >= 80) {
    grade = 'B';
} else if (score >= 70) {
    grade = 'C';
} else {
    grade = 'F';
}
```

Order is everything: with `score = 95`, the first branch fires and the rest
are skipped. If you tested `score >= 70` first, every score 70+ would get
'C' — a classic ordering bug.

**Boundaries.** `>=` vs `>` decides who owns the edge. Decide deliberately:
does 90 earn an A? Then `score >= 90`, not `> 90`. When the chain ends with
`else`, one branch always runs; without it, maybe none do.

Braces are optional for a single statement — but the AP exam loves to ask
what happens when a brace-less `if` meets a dangling `else`. Trace the
*indentation is a lie* case:

```java
if (x > 10)
    System.out.println("big");
    System.out.println("done");   // NOT inside the if — always runs!
```
"""

L2 = r"""
Conditions nest: an `if` inside an `if`.

```java
if (age >= 13) {
    if (hasPermission) {
        System.out.println("admit");
    } else {
        System.out.println("permission needed");
    }
}
```

Nesting is equivalent to `&&` when there is no else on the inner test:
`if (a) { if (b) { X } }` runs X exactly when both hold. Prefer flat `&&`
when you can — but *read* nested code fluently, the exam presents it
constantly.

**Dangling else** — an `else` binds to the **nearest** unmatched `if`, not
the one indentation suggests:

```java
if (a < 5)
    if (a > 2)
        System.out.println("3-4");
else
    System.out.println("else");   // belongs to inner if!
```

With `a = 10`: outer true → enter; inner `10 > 2` false → else fires, prints
"else". With `a = 0`: outer false → nothing prints at all. Brace your
intentions and trace honestly.

**Common logical errors**: flipped comparisons (`<` for `<=`), overlapping
ranges, testing `x == 5 || 6` (always true — 6 is truthy-wrong here: it must
be `x == 5 || x == 6`), and inverted guards.
"""

L3 = r"""
**Classification problems** map values to categories — letter grades, shipping
tiers, tax brackets. The recipe:

1. Decide the boundaries *before* coding (who owns 90?).
2. Order the chain from most-specific to catch-all.
3. End with `else` only when a default category truly exists.

**Validation problems** check inputs and reject bad ones early:

```java
if (quantity < 1) {
    return "invalid";
}
if (quantity > 100) {
    return "too many";
}
return "ok";
```

**Menu logic** selects behavior by a choice code:

```java
if (choice == 1) {
    ...
} else if (choice == 2) {
    ...
} else {
    ...
}
```

The exam's favorite trick: give you code with a subtle flaw (an off-by-one,
an unreachable branch, a missing `else`) and four candidate outputs. The
defense is the same trace discipline: walk each test input statement by
statement, and check *every* branch condition it passes on the way.
"""

write_module(
    M,
    "Selection and Iteration I: Conditionals",
    "if / else / else-if chains, nesting and dangling else, boundary ownership, classification and validation patterns.",
    "Rẽ nhánh và lặp I: Điều kiện",
    "Chuỗi if / else / else-if, lồng nhau và else kẹt, quyền sở hữu biên, các mẫu phân loại và kiểm tra dữ liệu.",
    lessons=["apc-m4-ifelse", "apc-m4-nesting", "apc-m4-patterns", "apc-cp-m4"],
    practices=["apc-p4-conditionals"],
)

write_lesson(
    M, "apc-m4-ifelse", "if, else, and else-if chains",
    "Branch selection, chain order, boundary ownership, brace-less pitfalls.",
    12, L1,
    "if, else và chuỗi else-if",
    "Chọn nhánh, thứ tự chuỗi, quyền sở hữu biên, cạm bẫy thiếu ngoặc.",
    r"""
`if` chỉ chạy khối lệnh khi boolean của nó đúng; `else` là con đường còn
lại.

```java
if (score >= 60) {
    System.out.println("pass");
} else {
    System.out.println("fail");
}
```

**Chuỗi else-if** kiểm tra theo thứ tự và dừng ở nhánh đúng đầu tiên:

```java
if (score >= 90) {
    grade = 'A';
} else if (score >= 80) {
    grade = 'B';
} else if (score >= 70) {
    grade = 'C';
} else {
    grade = 'F';
}
```

Thứ tự là tất cả: với `score = 95`, nhánh đầu chạy và phần còn lại bị bỏ qua.
Nếu kiểm tra `score >= 70` trước, mọi điểm 70+ sẽ nhận 'C' — lỗi thứ tự kinh
điển.

**Biên.** `>=` với `>` quyết định ai sở hữu mép. Quyết định có chủ đích: điểm
90 được A không? Vậy là `score >= 90`, không phải `> 90`. Khi chuỗi kết thúc
bằng `else`, luôn có một nhánh chạy; thiếu nó, có thể không nhánh nào chạy.

Ngoặc nhọn là tùy chọn cho một câu lệnh — nhưng đề thi AP rất thích hỏi điều
gì xảy ra khi `if` không ngoặc gặp `else` lơ lửng. Truy vết trường hợp *thụt
lề dối lòng*:

```java
if (x > 10)
    System.out.println("big");
    System.out.println("done");   // KHÔNG nằm trong if — luôn chạy!
```
""",
)

write_lesson(
    M, "apc-m4-nesting", "Nesting and the dangling else",
    "Nested conditionals, equivalence with &&, nearest-if binding.",
    12, L2,
    "Lồng nhau và else kẹt",
    "Điều kiện lồng nhau, tương đương với &&, else gắn với if gần nhất.",
    r"""
Điều kiện có thể lồng nhau: một `if` bên trong một `if`.

```java
if (age >= 13) {
    if (hasPermission) {
        System.out.println("admit");
    } else {
        System.out.println("permission needed");
    }
}
```

Lồng nhau tương đương với `&&` khi phép kiểm tra trong không có else:
`if (a) { if (b) { X } }` chạy X chính xác khi cả hai đúng. Ưu tiên `&&`
phẳng khi có thể — nhưng phải *đọc* code lồng nhau trôi chảy, đề thi đưa ra
liên tục.

**Else kẹt** — một `else` gắn với `if` chưa khớp **gần nhất**, không phải
cái mà thụt lề gợi ý:

```java
if (a < 5)
    if (a > 2)
        System.out.println("3-4");
else
    System.out.println("else");   // thuộc if bên trong!
```

Với `a = 10`: outer đúng → vào trong; inner `10 > 2` sai → else chạy, in
"else". Với `a = 0`: outer sai → không in gì cả. Đặt ngoặc theo ý định và
truy vết trung thực.

**Lỗi logic thường gặp**: so sánh bị lật (`<` thay `<=`), khoảng chồng lên
nhau, viết `x == 5 || 6` (luôn sai cấu trúc — phải là `x == 5 || x == 6`),
và chốt điều kiện bị đảo.
""",
)

write_lesson(
    M, "apc-m4-patterns", "Classification, validation, menus",
    "The three if/else patterns the exam reuses, plus trace strategy.",
    10, L3,
    "Phân loại, kiểm tra, menu",
    "Ba mẫu if/else đề thi tái sử dụng, cộng chiến lược truy vết.",
    r"""
**Bài phân loại** ánh xạ giá trị sang danh mục — xếp loại điểm, mức phí,
thuế. Công thức:

1. Quyết định biên *trước khi* viết code (ai sở hữu 90?).
2. Sắp chuỗi từ cụ thể nhất đến bắt tất cả.
3. Kết thúc bằng `else` chỉ khi một danh mục mặc định thực sự tồn tại.

**Bài kiểm tra dữ liệu** rà đầu vào và chặn giá trị xấu sớm:

```java
if (quantity < 1) {
    return "invalid";
}
if (quantity > 100) {
    return "too many";
}
return "ok";
```

**Logic menu** chọn hành vi theo mã lựa chọn:

```java
if (choice == 1) {
    ...
} else if (choice == 2) {
    ...
} else {
    ...
}
```

Mẹo ưa thích của đề thi: đưa cho bạn code có khuyết tật tinh tế (lệch một
đơn vị, nhánh không bao giờ tới được, thiếu `else`) và bốn kết quả ứng viên.
Linha phòng thủ là kỷ luật truy vết: đi qua từng dữ liệu test, câu lệnh một,
và kiểm tra *mọi* điều kiện nhánh mà nó đi ngang qua.
""",
)

BOILER_GRADE = r"""public class Solution {
    public static char letterGrade(int score) {
        return '?'; // replace
    }
}
"""

BOILER_TRI = r"""public class Solution {
    public static String triangleType(int a, int b, int c) {
        return "?"; // replace
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static String shipping(double total) {
        String cost = "unknown";
        if (total >= 100.0) {
            cost = "free";
        }
        if (total >= 50.0) {
            cost = "5.00";
        }
        if (total < 50.0) {
            cost = "8.00";
        }
        return cost;
    }
}
"""

BOILER_TEE = r"""public class Solution {
    public static int max3(int a, int b, int c) {
        return 0; // replace
    }
}
"""

CP_SIGN = r"""public class Solution {
    public static String describe(int x) {
        return "?"; // replace: "negative" | "zero" | "single" | "large"
    }
}
"""

P_GRADE = challenge(
    "apc-m4-lettergrade",
    "Letter grades with boundaries",
    "Implement `char letterGrade(int score)`: 'A' for 90+, 'B' for 80–89, 'C' for 70–79, 'F' otherwise. Order the chain so the boundaries land correctly.",
    BOILER_GRADE,
    [(
        "grade boundaries",
        r"""
CjTestBase.checkEq(Solution.letterGrade(95), 'A', "mid A");
CjTestBase.checkEq(Solution.letterGrade(90), 'A', "A boundary");
CjTestBase.checkEq(Solution.letterGrade(89), 'B', "just below A");
CjTestBase.checkEq(Solution.letterGrade(70), 'C', "C boundary");
CjTestBase.checkEq(Solution.letterGrade(69), 'F', "below C");
CjTestBase.checkEq(Solution.letterGrade(5), 'F', "low");
""",
        "Test the highest band first with >=; each else-if then owns its band.",
    )],
    level="imitation",
)

P_TRI = challenge(
    "apc-m4-triangle",
    "Triangle classification",
    "Implement `String triangleType(int a, int b, int c)`: \"equilateral\" when all three sides equal, \"isosceles\" when exactly two equal, \"scalene\" when none equal. (Assume the sides form a valid triangle.)",
    BOILER_TRI,
    [(
        "three types",
        r"""
CjTestBase.checkEq(Solution.triangleType(3, 3, 3), "equilateral", "all equal");
CjTestBase.checkEq(Solution.triangleType(3, 4, 3), "isosceles", "two equal");
CjTestBase.checkEq(Solution.triangleType(3, 4, 5), "scalene", "none equal");
CjTestBase.checkEq(Solution.triangleType(5, 3, 3), "isosceles", "equal pair anywhere");
""",
        "Check the most specific case (all equal) first.",
    )],
    level="guided",
)

P_FIX = challenge(
    "apc-m4-fix-shipping",
    "Debug the shipping tiers",
    "This classifier has a logic bug: some orders get the wrong tier. Trace each price point, find the flawed branch, and fix the minimum amount of code. Rules: 100+ → \"free\", 50–99.99 → \"5.00\", below 50 → \"8.00\".",
    BOILER_FIX,
    [(
        "all tiers correct",
        r"""
CjTestBase.checkEq(Solution.shipping(120.0), "free", "over 100");
CjTestBase.checkEq(Solution.shipping(100.0), "free", "at 100");
CjTestBase.checkEq(Solution.shipping(99.99), "5.00", "top of 50 band");
CjTestBase.checkEq(Solution.shipping(50.0), "5.00", "at 50");
CjTestBase.checkEq(Solution.shipping(49.99), "8.00", "just below 50");
""",
        "The second if must be else-if, or 100+ orders fall through to it.",
    )],
    level="debugging",
)

P_MAX = challenge(
    "apc-m4-max3",
    "Largest of three",
    "Implement `int max3(int a, int b, int c)`: the largest value, using only if/else comparisons (no Math.max).",
    BOILER_TEE,
    [(
        "max of three",
        r"""
CjTestBase.checkEq(Solution.max3(3, 9, 4), 9, "b wins");
CjTestBase.checkEq(Solution.max3(9, 3, 4), 9, "a wins");
CjTestBase.checkEq(Solution.max3(3, 4, 9), 9, "c wins");
CjTestBase.checkEq(Solution.max3(7, 7, 7), 7, "all equal");
CjTestBase.checkEq(Solution.max3(-5, -2, -9), -2, "negatives");
""",
        "Assume a is max; replace it each time you see bigger.",
    )],
    level="independent",
)

CP4 = challenge(
    "apc-cp-m4-describe",
    "Checkpoint: branch inventory",
    "Implement `String describe(int x)`: \"negative\" when x < 0; \"zero\" when x == 0; \"single\" when x is 1–9 inclusive; \"large\" when x >= 10. Every branch must be reachable and boundaries exact.",
    CP_SIGN,
    [(
        "branch coverage",
        r"""
CjTestBase.checkEq(Solution.describe(-7), "negative", "negative");
CjTestBase.checkEq(Solution.describe(0), "zero", "zero");
CjTestBase.checkEq(Solution.describe(1), "single", "low single");
CjTestBase.checkEq(Solution.describe(9), "single", "high single");
CjTestBase.checkEq(Solution.describe(10), "large", "large boundary");
""",
        "Four mutually exclusive bands: test negatives first, then zero, then the range.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p4-conditionals", "Branch and bound", "Grades, tiers, classification, and a logic bug to hunt.",
    "Rẽ nhánh và biên", "Xếp loại, mức phí, phân loại, và một lỗi logic cần săn.",
    after_lesson="apc-m4-ifelse", minutes=45, difficulty="beginner",
    challenges=[P_GRADE, P_TRI, P_FIX, P_MAX],
    vi_challenges={
        "apc-m4-lettergrade": vi_challenge("Xếp loại chữ cái với biên", "Cài đặt `char letterGrade(int score)`: 'A' cho 90+, 'B' cho 80–89, 'C' cho 70–79, 'F' cho còn lại. Sắp chuỗi để các biên rơi đúng chỗ.",
            [("grade boundaries", "Kiểm tra dải cao nhất trước bằng >=; mỗi else-if sở hữu dải của mình.")]),
        "apc-m4-triangle": vi_challenge("Phân loại tam giác", "Cài đặt `String triangleType(int a, int b, int c)`: \"equilateral\" khi cả ba cạnh bằng nhau, \"isosceles\" khi đúng hai cạnh bằng, \"scalene\" khi không cặp nào bằng. (Giả định ba cạnh tạo thành tam giác hợp lệ.)",
            [("three types", "Kiểm tra trường hợp cụ thể nhất (ba cạnh bằng nhau) trước.")]),
        "apc-m4-fix-shipping": vi_challenge("Sửa các mức phí vận chuyển", "Bộ phân loại này có lỗi logic: một số đơn hàng nhận sai mức. Truy vết từng mức giá, tìm nhánh lỗi, sửa lượng code tối thiểu. Quy tắc: 100+ → \"free\", 50–99.99 → \"5.00\", dưới 50 → \"8.00\".",
            [("all tiers correct", "if thứ hai phải là else-if, nếu không đơn 100+ sẽ rơi vào nó.")]),
        "apc-m4-max3": vi_challenge("Lớn nhất trong ba", "Cài đặt `int max3(int a, int b, int c)`: giá trị lớn nhất, chỉ dùng so sánh if/else (không dùng Math.max).",
            [("max of three", "Giả định a là max; thay thế mỗi lần thấy số lớn hơn.")]),
    },
    solutions=[
        ("apc-m4-lettergrade", r"""public class Solution {
    public static char letterGrade(int score) {
        if (score >= 90) {
            return 'A';
        } else if (score >= 80) {
            return 'B';
        } else if (score >= 70) {
            return 'C';
        } else {
            return 'F';
        }
    }
}
""",
         r"""public class Solution {
    public static char letterGrade(int score) {
        // BUG: chain order wrong — everything >= 70 becomes C
        if (score >= 70) {
            return 'C';
        } else if (score >= 80) {
            return 'B';
        } else if (score >= 90) {
            return 'A';
        } else {
            return 'F';
        }
    }
}
"""),
        ("apc-m4-triangle", r"""public class Solution {
    public static String triangleType(int a, int b, int c) {
        if (a == b && b == c) {
            return "equilateral";
        } else if (a == b || b == c || a == c) {
            return "isosceles";
        } else {
            return "scalene";
        }
    }
}
""",
         r"""public class Solution {
    public static String triangleType(int a, int b, int c) {
        // BUG: isosceles check catches equilateral too
        if (a == b || b == c || a == c) {
            return "isosceles";
        } else if (a == b && b == c) {
            return "equilateral";
        } else {
            return "scalene";
        }
    }
}
"""),
        ("apc-m4-fix-shipping", r"""public class Solution {
    public static String shipping(double total) {
        String cost = "unknown";
        if (total >= 100.0) {
            cost = "free";
        } else if (total >= 50.0) {
            cost = "5.00";
        } else {
            cost = "8.00";
        }
        return cost;
    }
}
""",
         r"""public class Solution {
    public static String shipping(double total) {
        // BUG: original flaw kept — second if not chained, so 100+ lands in 5.00
        String cost = "unknown";
        if (total >= 100.0) {
            cost = "free";
        }
        if (total >= 50.0) {
            cost = "5.00";
        }
        if (total < 50.0) {
            cost = "8.00";
        }
        return cost;
    }
}
"""),
        ("apc-m4-max3", r"""public class Solution {
    public static int max3(int a, int b, int c) {
        int max = a;
        if (b > max) {
            max = b;
        }
        if (c > max) {
            max = c;
        }
        return max;
    }
}
""",
         r"""public class Solution {
    public static int max3(int a, int b, int c) {
        // BUG: returns the first value — never compares
        return a;
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m4", "Checkpoint: conditionals",
    "Four mutually exclusive branches with exact boundaries.",
    18,
    r"""
Everything the module taught in one classifier: chain order, boundary
ownership, mutual exclusivity. Trace each test value through your chain
before submitting.
""",
    "Điểm kiểm tra: điều kiện",
    "Bốn nhánh loại trừ lẫn nhau với biên chính xác.",
    r"""
Tất cả những gì module đã dạy trong một bộ phân loại: thứ tự chuỗi, quyền
sở hữu biên, loại trừ lẫn nhau. Truy vết từng giá trị test qua chuỗi của bạn
trước khi nộp.
""",
    CP4,
    vi_challenge("Điểm kiểm tra: điều kiện", "Cài đặt `String describe(int x)`: \"negative\" khi x < 0; \"zero\" khi x == 0; \"single\" khi x từ 1 đến 9 gồm cả hai đầu; \"large\" khi x >= 10. Mọi nhánh phải với tới được và biên phải chính xác.",
        [("branch coverage", "Bốn dải loại trừ lẫn nhau: thử số âm trước, rồi zero, rồi khoảng.")]),
    solution=r"""public class Solution {
    public static String describe(int x) {
        if (x < 0) {
            return "negative";
        } else if (x == 0) {
            return "zero";
        } else if (x <= 9) {
            return "single";
        } else {
            return "large";
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static String describe(int x) {
        // BUG: zero branch unreachable — x == 0 also matches x < 10 first
        if (x < 10) {
            return "single";
        } else if (x == 0) {
            return "zero";
        } else if (x < 0) {
            return "negative";
        } else {
            return "large";
        }
    }
}
""",
)
