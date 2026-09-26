#!/usr/bin/env python3
"""AP CSA Advanced M9 — Inheritance & polymorphism challenge lab (verified dispatch)."""
from apx import *

M = "apx-polymorphism"

write_module(
    M,
    "Inheritance & Polymorphism Challenge Lab",
    "Dynamic dispatch under pressure: reference type vs object type, super calls, polymorphic collections, and hard traces. Difficulty E3–E5.",
    "Phòng thí nghiệm kế thừa & đa hình",
    "Điều phối động dưới áp lực: kiểu tham chiếu so với kiểu đối tượng, lời gọi super, bộ sưu tập đa hình, và truy vết khó. Độ khó E3–E5.",
    lessons=["apx-m9-two-types", "apx-m9-super", "apx-m9-collections", "apx-cp-m9"],
    practices=["apx-p9-poly"],
)

L1 = r"""
Every object reference question has **two answers hiding in one
variable**: what the reference type allows (compile-time) and what
the object type does (runtime). Write both above any tricky line:

```java
Employee e = new Manager("Ann", 100, 50);
// reference type: Employee — compiler allows e.pay(), forbids e.bonus
// object type: Manager — pay() dispatches to the OVERRIDE
```

Three laws follow:

1. **Which methods you may call** → reference type.
2. **Which version runs** (for overridden methods) → object type.
3. **Fields are not dispatched**: field access is resolved by
   reference type. Shadowed fields are the exam's favorite trap.

`instanceof` checks the object type (including subclasses); a cast
changes only what the compiler lets you name — it never changes the
object.
"""

L2 = r"""
**super is a method lookup one level up, not "the parent object."**
Two forms appear on the exam:

- `super.pay()` inside an override: run the parent's version, often
  then extending it (`return super.pay() + bonus;`). A W-answer
  forgets the `super.` and recurses or drops the base behavior.
- `super(args)` as the first constructor statement: parent
  initializes parent state. If a subclass constructor omits it, the
  compiler inserts `super()` — which fails to compile unless the
  parent has a zero-argument constructor.

**Abstract classes** add one rule: you cannot `new` them, but
references of the abstract type still dispatch to concrete
overrides. The pattern "one abstract parent, two subclasses, one
ArrayList of the parent type" is the most reused FRQ2 structure of
the last decade — this lab drills exactly that.
"""

L3 = r"""
**Polymorphic collections.** `ArrayList<Employee>` holds any mix of
Employees and Managers; the enhanced for-loop calls the override for
whatever each element really is:

```java
int total = 0;
for (Employee e : staff) {
    total += e.pay();   // Manager? +bonus. Employee? base.
}
```

The tracing discipline for these: one row per element, columns for
"reference type / object type / which pay runs / contribution." The
hard version adds a **conditional override** — a Manager only
counts the bonus when a flag holds — so the contribution column
depends on state you must also trace.

And the cast trap: `((Manager) e).bonus` compiles but throws
ClassCastException when e holds a plain Employee. On the exam,
"runtime error" is a *possible answer*, not a distraction — check
whether every element really is the cast type before trusting any
option that casts.
"""

VI_L1 = r"""
Mọi câu hỏi về tham chiếu đối tượng có **hai đáp án ẩn trong một
biến**: kiểu tham chiếu cho phép gì (lúc biên dịch) và kiểu đối tượng
làm gì (lúc chạy). Hãy viết cả hai phía trên dòng l补给 khó:

```java
Employee e = new Manager("Ann", 100, 50);
// kiểu tham chiếu: Employee — trình biên dịch cho phép e.pay(), cấm e.bonus
// kiểu đối tượng: Manager — pay() điều phối tới bản GHI ĐÈ
```

Ba định luật hệ quả:

1. **Bạn được gọi phương thức nào** → kiểu tham chiếu.
2. **Bản nào chạy** (với phương thức ghi đè) → kiểu đối tượng.
3. **Trường không được điều phối**: truy cập trường được phân giải
   theo kiểu tham chiếu. Trường bị bóng che là bẫy yêu thích của đề thi.

`instanceof` kiểm tra kiểu đối tượng (bao gồm cả lớp con); phép ép
kiểu chỉ thay đổi điều trình biên dịch cho bạn gọi tên — nó không bao
giờ thay đổi đối tượng.
"""

VI_L2 = r"""
**super là tra cứu phương thức lên một cấp, không phải "đối tượng
cha".** Hai dạng xuất hiện trong đề thi:

- `super.pay()` bên trong một bản ghi đè: chạy bản của lớp cha, thường
  rồi mở rộng (`return super.pay() + bonus;`). Một đáp án W quên
  `super.` và đệ quy hoặc làm rơi hành vi gốc.
- `super(args)` là câu lệnh đầu tiên của constructor: lớp cha khởi tạo
  trạng thái của lớp cha. Nếu constructor lớp con thiếu nó, trình biên
  dịch chèn `super()` — và sẽ không biên dịch được nếu lớp cha không
  có constructor không tham số.

**Lớp trừu tượng** thêm một luật: không thể `new`, nhưng tham chiếu
kiểu trừu tượng vẫn điều phối tới bản ghi đè cụ thể. Mẫu "một lớp cha
trừu tượng, hai lớp con, một ArrayList kiểu cha" là cấu trúc FRQ2
được tái sử dụng nhiều nhất thập kỷ qua — chính là bài lab này rèn.
"""

VI_L3 = r"""
**Bộ sưu tập đa hình.** `ArrayList<Employee>` chứa hỗn hợp mọi
Employee và Manager; vòng for-each gọi bản ghi đè tương ứng với kiểu
thực của từng phần tử:

```java
int total = 0;
for (Employee e : staff) {
    total += e.pay();   // Manager? +bonus. Employee? lương gốc.
}
```

Kỷ luật truy vết: mỗi phần tử một dòng, các cột "kiểu tham chiếu /
kiểu đối tượng / bản pay nào chạy / đóng góp". Bản khó thêm một
**ghi đè có điều kiện** — Manager chỉ tính thưởng khi một cờ bật —
nên cột đóng góp phụ thuộc vào trạng thái bạn cũng phải truy vết.

Và bẫy ép kiểu: `((Manager) e).bonus` biên dịch được nhưng ném
ClassCastException khi e giữ một Employee thường. Trong đề thi,
"lỗi lúc chạy" là *một đáp án có thể đúng*, không phải nhiễu — kiểm
tra xem mọi phần tử có thực sự thuộc kiểu bị ép không trước khi tin
bất kỳ phương án nào có ép kiểu.
"""

BOILER_STAFF = r"""public class Solution {
    public static class Employee {
        public Employee(String name, int base) {
        }

        public int pay() {
            return 0;
        }
    }

    public static class Manager extends Employee {
        public Manager(String name, int base, int bonus) {
            super(name, base);
        }

        public int pay() {
            return 0;
        }
    }

    public static int payroll(java.util.ArrayList<Employee> staff) {
        return 0; // replace: total pay across the mixed list
    }
}
"""

P_STAFF = challenge(
    "apx-m9-payroll",
    "Payroll over a mixed list",
    "Complete `Employee` (fields name, base; `pay()` returns base) and "
    "`Manager extends Employee` (extra field bonus; `pay()` returns "
    "base **plus** bonus, using `super.pay()`). Then implement "
    "`payroll(ArrayList<Employee>)` summing every employee's `pay()`.\n\n"
    "The list mixes both types; dispatch must do the work.",
    BOILER_STAFF,
    [(
        "mixed payroll",
        r"""
java.util.ArrayList<Solution.Employee> staff = new java.util.ArrayList<>();
staff.add(new Solution.Employee("Ann", 100));
staff.add(new Solution.Manager("Bob", 100, 50));
CjTestBase.checkEq(Solution.payroll(staff), 250, "100 + (100+50)");
java.util.ArrayList<Solution.Employee> only = new java.util.ArrayList<>();
only.add(new Solution.Employee("Zoe", 90));
CjTestBase.checkEq(Solution.payroll(only), 90, "plain employee only");
""",
        "Manager.pay() = super.pay() + bonus; payroll loops once and lets dispatch choose.",
    )],
    level="independent",
    difficulty="advanced",
)

P_SHAPE = challenge(
    "apx-m9-shapes",
    "Abstract shapes with conditional overrides",
    "Implement `Shape` (abstract): `public abstract int area();` plus a "
    "concrete `describe()` returning `\"shape:\" + area()`. Subclass "
    "`Square` (side; area = side*side) and `Rect` (w, h; area = w*h). "
    "Then implement `totalArea(ArrayList<Shape>)`.\n\nThe list may "
    "contain both; use the abstract reference type.",
    r"""public class Solution {
    public static abstract class Shape {
        public abstract int area();

        public String describe() {
            return "shape:" + area();
        }
    }

    public static class Square extends Shape {
        public Square(int side) {
        }

        public int area() {
            return 0;
        }
    }

    public static class Rect extends Shape {
        public Rect(int w, int h) {
        }

        public int area() {
            return 0;
        }
    }

    public static int totalArea(java.util.ArrayList<Shape> shapes) {
        return 0; // replace
    }
}
""",
    [(
        "abstract dispatch",
        r"""
java.util.ArrayList<Solution.Shape> shapes = new java.util.ArrayList<>();
shapes.add(new Solution.Square(3));
shapes.add(new Solution.Rect(2, 5));
CjTestBase.checkEq(Solution.totalArea(shapes), 19, "9 + 10");
CjTestBase.checkEq(new Solution.Square(4).describe(), "shape:16", "describe uses the override");
""",
        "Each subclass implements area(); totalArea sums area() over the abstract references.",
    )],
    level="combination",
    difficulty="advanced",
)

P_GREET = challenge(
    "apx-m9-greetings",
    "Trace the greeting chain",
    "Trace this hierarchy and call sequence **on paper**, then return "
    "the exact printed text (lines joined with `|`):\n\n```java\n"
    "public class Greeter {\n    public String greet() {\n"
    "        return \"Hello\";\n    }\n    public String greetAll() {\n"
    "        return greet() + \"!\";\n    }\n}\n"
    "public class Loud extends Greeter {\n"
    "    public String greet() {\n        return \"HELLO\";\n    }\n}\n```\n\n"
    "Calls: `new Greeter().greetAll()`, then `new Loud().greetAll()`.\n"
    "`greetAll` is NOT overridden — but it still dispatches.",
    r"""public class Solution {
    public static String result() {
        return ""; // replace: "Hello!|HELLO!"
    }
}
""",
    [(
        "dispatch through inherited method",
        r"""
CjTestBase.checkEq(Solution.result(), "Hello!|HELLO!", "inherited greetAll calls the override");
""",
        "greetAll is inherited by Loud but executes with Loud's dispatch: this.greet() finds the override.",
    )],
    level="combination",
    difficulty="advanced",
)

CP9 = challenge(
    "apx-cp-m9-discount",
    "Checkpoint: the discount chain",
    "Implement the chain: `Customer.pay(int amount)` returns the amount. "
    "`Member extends Customer`: pay returns `super.pay()` minus 5%. "
    "`Gold extends Member`: pay returns `super.pay()` minus another 5% "
    "(so 90% of the original). Use integer arithmetic exactly as "
    "written: Member pays `amount - amount / 20`; Gold pays "
    "`amount - amount / 10`.\n\nImplement all three classes and the "
    "given `pay` signatures.",
    r"""public class Solution {
    public static class Customer {
        public int pay(int amount) {
            return 0; // replace: full amount
        }
    }

    public static class Member extends Customer {
        public int pay(int amount) {
            return 0; // replace: 5% off via amount - amount / 20
        }
    }

    public static class Gold extends Member {
        public int pay(int amount) {
            return 0; // replace: 10% off via amount - amount / 10
        }
    }
}
""",
    [(
        "discount chain",
        r"""
CjTestBase.checkEq(new Solution.Customer().pay(100), 100, "no discount");
CjTestBase.checkEq(new Solution.Member().pay(100), 95, "5 percent off");
CjTestBase.checkEq(new Solution.Gold().pay(100), 90, "10 percent off");
CjTestBase.checkEq(new Solution.Gold().pay(99), 90, "integer division: 99/10 = 9, so 99-9");
""",
        "Each level computes its own discount on the ORIGINAL amount (no super needed here) — or chains via super; both must yield 95/90.",
    )],
    level="independent",
    difficulty="advanced",
)

VI_CP9 = vi_challenge(
    "Điểm kiểm tra: chuỗi chiết khấu",
    "Cài đặt chuỗi lớp: `Customer.pay(int amount)` trả nguyên amount. "
    "`Member extends Customer`: pay trả `super.pay()` giảm 5%. "
    "`Gold extends Member`: pay trả `super.pay()` giảm thêm 5% (tức 90% "
    "giá gốc). Dùng số nguyên đúng như đề: Member trả "
    "`amount - amount / 20`; Gold trả `amount - amount / 10`.\n\n"
    "Cài đặt cả ba lớp với chữ ký `pay` như đã cho.",
    [("discount chain", "Mỗi cấp tự tính chiết khấu trên số gốc (không cần super) — hoặc xích qua super; cả hai phải ra 95/90.")],
)

write_practice(
    M, "apx-p9-poly", "Polymorphism gauntlet",
    "Dispatch, abstract references, and inherited-method dispatch, each with traps.",
    "Võ đài đa hình",
    "Điều phối, tham chiếu trừu tượng, và điều phối qua phương thức kế thừa, mỗi bài đều có bẫy.",
    after_lesson="apx-m9-collections", minutes=60, difficulty="advanced",
    challenges=[P_STAFF, P_SHAPE, P_GREET],
    vi_challenges={
        "apx-m9-payroll": vi_challenge(
            "Bảng lương qua danh sách hỗn hợp",
            "Hoàn thiện `Employee` (trường name, base; `pay()` trả base) và "
            "`Manager extends Employee` (thêm trường bonus; `pay()` trả base "
            "**cộng** bonus, dùng `super.pay()`). Rồi cài đặt "
            "`payroll(ArrayList<Employee>)` cộng `pay()` của mọi nhân viên.\n\n"
            "Danh sách trộn cả hai kiểu; để điều phối lo phần việc.",
            [("mixed payroll", "Manager.pay() = super.pay() + bonus; payroll duyệt một lần và để điều phối chọn.")],
        ),
        "apx-m9-shapes": vi_challenge(
            "Hình trừu tượng với ghi đè có điều kiện",
            "Cài đặt `Shape` (trừu tượng): `public abstract int area();` cộng "
            "phương thức cụ thể `describe()` trả `\"shape:\" + area()`. Lớp "
            "con `Square` (cạnh; area = cạnh*cạnh) và `Rect` (w, h; area = "
            "w*h). Rồi cài đặt `totalArea(ArrayList<Shape>)`.\n\nDanh sách có "
            "thể chứa cả hai; dùng kiểu tham chiếu trừu tượng.",
            [("abstract dispatch", "Mỗi lớp con cài area(); totalArea cộng area() qua các tham chiếu trừu tượng.")],
        ),
        "apx-m9-greetings": vi_challenge(
            "Truy vết chuỗi lời chào",
            "Truy vết hệ phân cấp và chuỗi lời gọi này **trên giấy**, rồi trả "
            "về văn bản được in chính xác (các dòng nối bằng `|`):\n\n```java\n"
            "public class Greeter {\n    public String greet() {\n"
            "        return \"Hello\";\n    }\n    public String greetAll() {\n"
            "        return greet() + \"!\";\n    }\n}\n"
            "public class Loud extends Greeter {\n"
            "    public String greet() {\n        return \"HELLO\";\n    }\n}\n```\n\n"
            "Lời gọi: `new Greeter().greetAll()`, rồi `new Loud().greetAll()`.\n"
            "`greetAll` KHÔNG bị ghi đè — nhưng nó vẫn điều phối.",
            [("dispatch through inherited method", "greetAll được Loud kế thừa nhưng chạy với điều phối của Loud: this.greet() tìm thấy bản ghi đè.")],
        ),
    },
    solutions=[
        ("apx-m9-payroll", r"""public class Solution {
    public static class Employee {
        private String name;
        private int base;

        public Employee(String name, int base) {
            this.name = name;
            this.base = base;
        }

        public int pay() {
            return base;
        }
    }

    public static class Manager extends Employee {
        private int bonus;

        public Manager(String name, int base, int bonus) {
            super(name, base);
            this.bonus = bonus;
        }

        public int pay() {
            return super.pay() + bonus;
        }
    }

    public static int payroll(java.util.ArrayList<Employee> staff) {
        int total = 0;
        for (Employee e : staff) {
            total += e.pay();
        }
        return total;
    }
}
""", r"""public class Solution {
    public static class Employee {
        private String name;
        private int base;

        public Employee(String name, int base) {
            this.name = name;
            this.base = base;
        }

        public int pay() {
            return base;
        }
    }

    public static class Manager extends Employee {
        private int bonus;

        public Manager(String name, int base, int bonus) {
            super(name, base);
            this.bonus = bonus;
        }

        public int pay() {
            // BUG: forgot super — calls itself forever (StackOverflowError)
            return pay() + bonus;
        }
    }

    public static int payroll(java.util.ArrayList<Employee> staff) {
        int total = 0;
        for (Employee e : staff) {
            total += e.pay();
        }
        return total;
    }
}
"""),
        ("apx-m9-shapes", r"""public class Solution {
    public static abstract class Shape {
        public abstract int area();

        public String describe() {
            return "shape:" + area();
        }
    }

    public static class Square extends Shape {
        private int side;

        public Square(int side) {
            this.side = side;
        }

        public int area() {
            return side * side;
        }
    }

    public static class Rect extends Shape {
        private int w;
        private int h;

        public Rect(int w, int h) {
            this.w = w;
            this.h = h;
        }

        public int area() {
            return w * h;
        }
    }

    public static int totalArea(java.util.ArrayList<Shape> shapes) {
        int total = 0;
        for (Shape s : shapes) {
            total += s.area();
        }
        return total;
    }
}
""", r"""public class Solution {
    public static abstract class Shape {
        public abstract int area();

        public String describe() {
            return "shape:" + area();
        }
    }

    public static class Square extends Shape {
        private int side;

        public Square(int side) {
            this.side = side;
        }

        public int area() {
            return side * side;
        }
    }

    public static class Rect extends Shape {
        private int w;
        private int h;

        public Rect(int w, int h) {
            this.w = w;
            this.h = h;
        }

        public int area() {
            // BUG: swapped operands — w + h instead of w * h
            return w + h;
        }
    }

    public static int totalArea(java.util.ArrayList<Shape> shapes) {
        int total = 0;
        for (Shape s : shapes) {
            total += s.area();
        }
        return total;
    }
}
"""),
        ("apx-m9-greetings", r"""public class Solution {
    public static String result() {
        return "Hello!|HELLO!";
    }
}
""", r"""public class Solution {
    // BUG: believed greetAll must be overridden to dispatch — returned the base greeting twice
    public static String result() {
        return "Hello!|Hello!";
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apx-cp-m9", "Checkpoint: the discount chain",
    "A three-level override chain where each level extends the last.",
    20,
    r"""
Chained overrides are the purest test of super: each level either
delegates with super or recomputes from the original amount — and
the two styles must agree. Trace 99 through the chain before coding;
integer division makes 99/20 = 4, not 4.95.
""",
    "Điểm kiểm tra: chuỗi chiết khấu",
    "Chuỗi ghi đè ba cấp trong đó mỗi cấp mở rộng cấp trước.",
    r"""
Chuỗi ghi đè là bài kiểm tra thuần khiết nhất của super: mỗi cấp hoặc
ủy quyền qua super hoặc tự tính lại từ số gốc — và hai phong cách phải
khớp nhau. Truy vết 99 qua chuỗi trước khi viết mã; chia số nguyên làm
99/20 = 4, không phải 4.95.
""",
    CP9,
    VI_CP9,
    solution=r"""public class Solution {
    public static class Customer {
        public int pay(int amount) {
            return amount;
        }
    }

    public static class Member extends Customer {
        public int pay(int amount) {
            return amount - amount / 20;
        }
    }

    public static class Gold extends Member {
        public int pay(int amount) {
            return amount - amount / 10;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Customer {
        public int pay(int amount) {
            return amount;
        }
    }

    public static class Member extends Customer {
        public int pay(int amount) {
            return amount - amount / 20;
        }
    }

    public static class Gold extends Member {
        public int pay(int amount) {
            // BUG: discounts the ALREADY-discounted amount — compounds twice
            return super.pay(amount) - super.pay(amount) / 20;
        }
    }
}
""",
)

print("M9 done")
