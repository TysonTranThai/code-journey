#!/usr/bin/env python3
"""AP CSA M13 — Inheritance (light, revised-framework weight): extends, super, overriding."""
from apc import *

M = "apc-inheritance"

L1 = r"""
**Inheritance** models is-a relationships. A `Dog` is-a `Pet`: it gets every
non-private member of `Pet` for free and adds its own.

```java
public class Pet {
    private String name;

    public Pet(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String speak() {
        return "...";
    }
}

public class Dog extends Pet {
    private boolean fetchTrained;

    public Dog(String name, boolean fetchTrained) {
        super(name);               // MUST be first: build the Pet part
        this.fetchTrained = fetchTrained;
    }

    public boolean isFetchTrained() {
        return fetchTrained;
    }
}
```

Reading rules:

- `private` fields exist inside `Dog` objects but are **not directly
  accessible** from `Dog` code — go through the superclass's public
  accessors (`getName()`).
- `super(name)` calls the superclass constructor. If you omit it, Java
  inserts an implicit `super()` — which only compiles if the superclass
  *has* a no-arg constructor. This is the #1 inheritance compile error.

Revised-framework note: inheritance appears in Unit 3 (10–18% of the exam)
with modest depth — extends, super, one level of overriding. Hierarchy
depth beyond one level, `protected`, abstract classes, and interfaces are
*not* in this course.
"""

L2 = r"""
**Overriding** — a subclass redefines an inherited method with the same
signature:

```java
public class Cat extends Pet {
    public Cat(String name) {
        super(name);
    }

    public String speak() {           // overrides Pet.speak
        return "meow";
    }
}
```

Which method runs depends on the **object's** class, not the variable's:

```java
Pet p = new Cat("Mimi");
p.speak();          // "meow" — the Cat method runs
p.getName();        // works: inherited from Pet
```

The variable type decides what you may *call*; the object type decides
*which version* executes. That sentence answers half the exam's
inheritance questions.

**super.method()** extends rather than replaces:

```java
public String speak() {
    return super.speak() + " purr";
}
```

**@Override** is optional but recommended — the compiler then catches
misspelled signatures (an overload in disguise).

`equals` reminder: AP classes override `equals(Object other)`, cast
inside, and compare fields — or provide a custom `equalsName`-style method
when the exam wants simpler code. We follow the exam's custom-method style
here.
"""

L3 = r"""
Tracing a constructor chain — the exam's favorite:

```java
public class A {
    public A() { System.out.print("A"); }
}

public class B extends A {
    public B() { System.out.print("B"); }   // implicit super() first
}
```

`new B()` prints `AB`: the superclass part is always built first. With
explicit `super(args)` and fields, the order is: super constructor →
subclass field initializers → subclass constructor body.

What subclasses **don't** inherit: private fields (exist but hidden),
constructors (called, not inherited), static methods are hidden not
overridden (out of scope here).

**Common trace traps**: calling an overridden method *from inside the
superclass constructor* runs the subclass version before subclass fields
are initialized — a classic "why is my field null" puzzle. The exam uses
this only in the hardest trace items; know the mechanism, don't memorize
beyond it.
"""

write_module(
    M,
    "Inheritance",
    "extends, super, constructor chaining, overriding, and which method actually runs.",
    "Kế thừa",
    "extends, super, chuỗi hàm dựng, ghi đè phương thức, và phương thức nào thật sự chạy.",
    lessons=["apc-m13-extends", "apc-m13-overriding", "apc-m13-chaining", "apc-cp-m13"],
    practices=["apc-p13-inheritance"],
)

write_lesson(
    M, "apc-m13-extends", "extends and super",
    "Subclasses, private access across the hierarchy, implicit vs explicit super.",
    14, L1,
    "extends và super",
    "Lớp con, truy cập private xuyên hệ thống phân cấp, super ngầm định so với tường minh.",
    r"""
**Kế thừa** mô hình hóa quan hệ is-a. Một `Dog` là một `Pet`: nó nhận mọi
thành viên không phải private của `Pet` miễn phí và thêm phần của riêng mình.

```java
public class Pet {
    private String name;

    public Pet(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String speak() {
        return "...";
    }
}

public class Dog extends Pet {
    private boolean fetchTrained;

    public Dog(String name, boolean fetchTrained) {
        super(name);               // PHẢI là đầu tiên: dựng phần Pet
        this.fetchTrained = fetchTrained;
    }

    public boolean isFetchTrained() {
        return fetchTrained;
    }
}
```

Luật đọc:

- Trường `private` tồn tại bên trong đối tượng `Dog` nhưng **không truy cập
  trực tiếp được** từ mã `Dog` — phải đi qua accessor công khai của lớp cha
  (`getName()`).
- `super(name)` gọi hàm dựng của lớp cha. Bỏ qua nó, Java chèn ngầm
  `super()` — chỉ biên dịch được nếu lớp cha *có* hàm dựng không tham số.
  Đây là lỗi biên dịch kế thừa phổ biến nhất.

Ghi chú khung chương trình sửa đổi: kế thừa xuất hiện trong Unit 3 (10–18%
đề thi) ở độ sâu khiêm tốn — extends, super, một mức ghi đè. Hệ thống phân
cấp sâu hơn một mức, `protected`, lớp trừu tượng, interface *không* nằm
trong khóa học này.
""",
)

write_lesson(
    M, "apc-m13-overriding", "Overriding and dispatch",
    "Same signature, object type decides, super.method, the @Override habit.",
    14, L2,
    "Ghi đè và phân phối",
    "Chữ ký giống nhau, kiểu đối tượng quyết định, super.method, thói quen @Override.",
    r"""
**Ghi đè** — lớp con định nghĩa lại phương thức kế thừa với cùng chữ ký:

```java
public class Cat extends Pet {
    public Cat(String name) {
        super(name);
    }

    public String speak() {           // ghi đè Pet.speak
        return "meow";
    }
}
```

Phương thức nào chạy phụ thuộc lớp của **đối tượng**, không phải kiểu biến:

```java
Pet p = new Cat("Mimi");
p.speak();          // "meow" — phương thức của Cat chạy
p.getName();        // chạy được: kế thừa từ Pet
```

Kiểu biến quyết định bạn được *gọi* gì; kiểu đối tượng quyết định *phiên
bản nào* thực thi. Câu đó trả lời một nửa câu hỏi kế thừa của đề thi.

**super.method()** mở rộng thay vì thay thế:

```java
public String speak() {
    return super.speak() + " purr";
}
```

**@Override** là tùy chọn nhưng nên dùng — trình biên dịch sau đó bắt được
chữ ký bị gõ nhầm (một overload trá hình).

Nhắc lại `equals`: các lớp kiểu đề thi override `equals(Object other)`,
ép kiểu bên trong, và so các trường — hoặc cung cấp phương thức riêng kiểu
`equalsName` khi đề muốn mã đơn giản hơn. Ở đây ta theo phong cách
phương thức-riêng của đề.
""",
)

write_lesson(
    M, "apc-m13-chaining", "Constructor chains and trace traps",
    "Build order AB, what isn't inherited, calling overridden methods from constructors.",
    10, L3,
    "Chuỗi hàm dựng và bẫy truy vết",
    "Thứ tự dựng AB, cái gì không được kế thừa, gọi phương thức bị ghi đè từ hàm dựng.",
    r"""
Truy vết chuỗi hàm dựng — món khoái khẩu của đề thi:

```java
public class A {
    public A() { System.out.print("A"); }
}

public class B extends A {
    public B() { System.out.print("B"); }   // super() ngầm chạy trước
}
```

`new B()` in `AB`: phần lớp cha luôn được dựng trước. Với `super(args)`
tường minh và các trường, thứ tự là: hàm dựng lớp cha → bộ khởi tạo trường
của lớp con → thân hàm dựng lớp con.

Lớp con **không** kế thừa: trường private (tồn tại nhưng bị che), hàm dựng
(được gọi, không được kế thừa), phương thức static bị che chứ không bị ghi
đè (ngoài phạm vi ở đây).

**Bẫy truy vết phổ biến**: gọi một phương thức bị ghi đè *từ bên trong hàm
dựng lớp cha* sẽ chạy phiên bản lớp con trước khi các trường lớp con được
khởi tạo — câu đố "tại sao trường của tôi null" kinh điển. Đề thi chỉ dùng
điều này ở các câu truy vết khó nhất; hiểu cơ chế, đừng học thuộc thêm gì.
""",
)

BOILER_SQR = r"""public class Solution {
    public static class Shape {
        private String label;

        public Shape(String label) {
            this.label = label;
        }

        public String getLabel() {
            return label;
        }

        public double area() {
            return 0.0;
        }
    }

    public static class Square extends Shape {
        private double side;

        public Square(double side) {
            // complete: label "square", store side
        }

        public double getSide() {
            return side;
        }

        public double area() {
            // complete: side * side
            return 0.0;
        }
    }
}
"""

BOILER_EMP = r"""public class Solution {
    public static class Employee {
        private String name;
        private int base;

        public Employee(String name, int base) {
            this.name = name;
            this.base = base;
        }

        public String getName() {
            return name;
        }

        public int getBase() {
            return base;
        }

        public int pay() {
            return base;
        }
    }

    public static class Manager extends Employee {
        private int bonus;

        public Manager(String name, int base, int bonus) {
            // complete
        }

        public int getBonus() {
            return bonus;
        }

        public int pay() {
            // complete: base pay + bonus (use inherited accessor)
            return 0;
        }
    }
}
"""

BOILER_VEH = r"""public class Solution {
    public static class Vehicle {
        public String describe() {
            return "vehicle";
        }
    }

    public static class Truck extends Vehicle {
        public String describe() {
            // complete: super's word + " with 6 wheels"
            return "";
        }
    }
}
"""

BOILER_PET = r"""public class Solution {
    public static class Animal {
        public String sound() {
            return "hmm";
        }
    }

    public static class Cow extends Animal {
        public String sound() {
            // complete: "moo"
            return "";
        }
    }

    public static class Duck extends Animal {
        public String sound() {
            // complete: "quack"
            return "";
        }
    }

    public static String chorus(Animal a, Animal b) {
        // complete: each animal's own sound, space-separated, a first
        return "";
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static class Box {
        private String tag;

        public Box(String tag) {
            this.tag = tag;
        }

        public String getTag() {
            return tag;
        }

        public int size() {
            return 1;
        }
    }

    public static class BigBox extends Box {
        private int factor;

        public BigBox(String tag, int factor) {
            // BUG: implicit super() — but Box has no no-arg constructor,
            // so this class does not compile; also factor never stored
        }

        public int size() {
            return factor;
        }
    }
}
"""

CP13 = r"""public class Solution {
    public static class Account {
        private String owner;
        private int balance;

        public Account(String owner, int balance) {
            this.owner = owner;
            this.balance = balance;
        }

        public String getOwner() {
            return owner;
        }

        public int getBalance() {
            return balance;
        }

        public void deposit(int amount) {
            balance = balance + amount;
        }
    }

    public static class BonusAccount extends Account {
        private int deposits;

        public BonusAccount(String owner, int balance) {
            // complete: chain up; deposits start at 0
        }

        public void deposit(int amount) {
            // complete: count the deposit, then the normal deposit
        }

        public int getDeposits() {
            return deposits;
        }
    }
}
"""

P_SQR = challenge(
    "apc-m13-square",
    "Complete the Square",
    "Complete `Square extends Shape`: the constructor must call `super(\"square\")`, store side; `area()` overrides to side * side.",
    BOILER_SQR,
    [(
        "shape hierarchy",
        r"""
Solution.Square s = new Solution.Square(5);
CjTestBase.checkEq(s.getLabel(), "square", "chained label");
CjTestBase.checkEq(s.getSide(), 5.0, "stored side");
CjTestBase.checkEq(s.area(), 25.0, "overridden area");
""",
        "super(\"square\"); first, then this.side = side.",
    )],
    level="imitation",
)

P_EMP = challenge(
    "apc-m13-manager",
    "Manager pay",
    "Complete `Manager extends Employee`: constructor chains up with super(name, base) and stores bonus; `pay()` overrides to base + bonus, reading the base through the inherited accessor `getBase()`.",
    BOILER_EMP,
    [(
        "payroll chain",
        r"""
Solution.Manager m = new Solution.Manager("Lan", 1000, 250);
CjTestBase.checkEq(m.getName(), "Lan", "inherited accessor");
CjTestBase.checkEq(m.getBonus(), 250, "own field");
CjTestBase.checkEq(m.pay(), 1250, "overridden pay");
""",
        "getBase() works inside Manager — private base is reachable through the public accessor.",
    )],
    level="guided",
)

P_VEH = challenge(
    "apc-m13-superword",
    "Extend with super.method",
    "Complete `Truck.describe()` to return the superclass's word followed by \" with 6 wheels\" — building on `super.describe()`, not duplicating the word.",
    BOILER_VEH,
    [(
        "super word",
        r"""
Solution.Truck t = new Solution.Truck();
CjTestBase.checkEq(t.describe(), "vehicle with 6 wheels", "extended text");
""",
        "return super.describe() + \" with 6 wheels\";",
    )],
    level="imitation",
)

P_PET = challenge(
    "apc-m13-chorus",
    "Which method runs?",
    "Complete both subclasses' `sound()` overrides, then `chorus(a, b)`: each animal's own sound separated by a single space, a's first. The dispatch must be dynamic — no instanceof.",
    BOILER_PET,
    [(
        "dynamic dispatch",
        r"""
Solution.Cow c = new Solution.Cow();
Solution.Duck d = new Solution.Duck();
CjTestBase.checkEq(Solution.chorus(c, d), "moo quack", "cow then duck");
CjTestBase.checkEq(Solution.chorus(d, c), "quack moo", "duck then cow");
CjTestBase.checkEq(c.sound(), "moo", "cow alone");
""",
        "a.sound() + \" \" + b.sound() — the object types decide.",
    )],
    level="independent",
)

P_FIX = challenge(
    "apc-m13-fix-bigbox",
    "Debug the constructor chain",
    "`BigBox` does not compile: its constructor omits `super(...)` while `Box` has no no-arg constructor, and `factor` is never stored. Fix the constructor chain (signatures stay the same).",
    BOILER_FIX,
    [(
        "chain repaired",
        r"""
Solution.BigBox b = new Solution.BigBox("crate", 4);
CjTestBase.checkEq(b.getTag(), "crate", "super part built");
CjTestBase.checkEq(b.size(), 4, "factor stored");
""",
        "super(tag); must be the first statement; then this.factor = factor.",
    )],
    level="debugging",
)

CP13C = challenge(
    "apc-cp-m13-bonusaccount",
    "Checkpoint: BonusAccount",
    "Complete `BonusAccount extends Account`: chain the constructor up, keep a private deposit counter starting at 0, and override `deposit(amount)` to count the deposit and then perform the normal deposit (reusing the superclass method).",
    CP13,
    [(
        "counting override",
        r"""
Solution.BonusAccount a = new Solution.BonusAccount("Minh", 500);
CjTestBase.checkEq(a.getBalance(), 500, "chained initial balance");
CjTestBase.checkEq(a.getDeposits(), 0, "fresh counter");
a.deposit(200);
a.deposit(50);
CjTestBase.checkEq(a.getBalance(), 750, "deposits applied");
CjTestBase.checkEq(a.getDeposits(), 2, "counted twice");
""",
        "super.deposit(amount); does the balance work — override only adds counting.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p13-inheritance", "Inheritance reps", "Chaining, overriding, dispatch, super.method, chain debugging.",
    "Luyện kế thừa", "Chuỗi hàm dựng, ghi đè, phân phối, super.method, gỡ chuỗi hàm dựng.",
    after_lesson="apc-m13-chaining", minutes=55, difficulty="beginner",
    challenges=[P_SQR, P_EMP, P_VEH, P_PET, P_FIX],
    vi_challenges={
        "apc-m13-square": vi_challenge("Hoàn thiện Square", "Hoàn thiện `Square extends Shape`: hàm dựng phải gọi `super(\"square\")`, lưu side; `area()` ghi đè thành side * side.",
            [("shape hierarchy", "super(\"square\"); trước, rồi this.side = side.")]),
        "apc-m13-manager": vi_challenge("Lương quản lý", "Hoàn thiện `Manager extends Employee`: hàm dựng nối lên trên bằng super(name, base) và lưu bonus; `pay()` ghi đè thành base + bonus, đọc base qua accessor kế thừa `getBase()`.",
            [("payroll chain", "getBase() dùng được bên trong Manager — base private chạm được qua accessor công khai.")]),
        "apc-m13-superword": vi_challenge("Mở rộng bằng super.method", "Hoàn thiện `Truck.describe()` trả về từ của lớp cha nối với \" with 6 wheels\" — dựa trên `super.describe()`, không nhân bản từ đó.",
            [("super word", "return super.describe() + \" with 6 wheels\";")]),
        "apc-m13-chorus": vi_challenge("Phương thức nào chạy?", "Hoàn thiện `sound()` của cả hai lớp con, rồi `chorus(a, b)`: âm thanh riêng của từng con, cách nhau một dấu cách, a trước. Phân phối phải động — không dùng instanceof.",
            [("dynamic dispatch", "a.sound() + \" \" + b.sound() — kiểu đối tượng quyết định.")]),
        "apc-m13-fix-bigbox": vi_challenge("Gỡ lỗi chuỗi hàm dựng", "`BigBox` không biên dịch được: hàm dựng của nó thiếu `super(...)` trong khi `Box` không có hàm dựng không tham số, và `factor` không bao giờ được lưu. Sửa chuỗi hàm dựng (chữ ký giữ nguyên).",
            [("chain repaired", "super(tag); phải là câu lệnh đầu tiên; rồi this.factor = factor.")]),
    },
    solutions=[
        ("apc-m13-square", r"""public class Solution {
    public static class Shape {
        private String label;

        public Shape(String label) {
            this.label = label;
        }

        public String getLabel() {
            return label;
        }

        public double area() {
            return 0.0;
        }
    }

    public static class Square extends Shape {
        private double side;

        public Square(double side) {
            super("square");
            this.side = side;
        }

        public double getSide() {
            return side;
        }

        public double area() {
            return side * side;
        }
    }
}
""",
         r"""public class Solution {
    public static class Shape {
        private String label;

        public Shape(String label) {
            this.label = label;
        }

        public String getLabel() {
            return label;
        }

        public double area() {
            return 0.0;
        }
    }

    public static class Square extends Shape {
        private double side;

        public Square(double side) {
            // BUG: implicit super() — Shape has no no-arg constructor,
            // and side is never stored
        }

        public double getSide() {
            return side;
        }

        public double area() {
            return side * side;
        }
    }
}
"""),
        ("apc-m13-manager", r"""public class Solution {
    public static class Employee {
        private String name;
        private int base;

        public Employee(String name, int base) {
            this.name = name;
            this.base = base;
        }

        public String getName() {
            return name;
        }

        public int getBase() {
            return base;
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

        public int getBonus() {
            return bonus;
        }

        public int pay() {
            return getBase() + bonus;
        }
    }
}
""",
         r"""public class Solution {
    public static class Employee {
        private String name;
        private int base;

        public Employee(String name, int base) {
            this.name = name;
            this.base = base;
        }

        public String getName() {
            return name;
        }

        public int getBase() {
            return base;
        }

        public int pay() {
            return base;
        }
    }

    public static class Manager extends Employee {
        private int bonus;

        public Manager(String name, int base, int bonus) {
            // BUG: no super(name, base) chain — Employee part never built;
            // bonus never stored
        }

        public int getBonus() {
            return bonus;
        }

        public int pay() {
            return getBase() + bonus;
        }
    }
}
"""),
        ("apc-m13-superword", r"""public class Solution {
    public static class Vehicle {
        public String describe() {
            return "vehicle";
        }
    }

    public static class Truck extends Vehicle {
        public String describe() {
            return super.describe() + " with 6 wheels";
        }
    }
}
""",
         r"""public class Solution {
    public static class Vehicle {
        public String describe() {
            return "vehicle";
        }
    }

    public static class Truck extends Vehicle {
        public String describe() {
            // BUG: duplicates the word instead of extending via super
            return "truck with 6 wheels";
        }
    }
}
"""),
        ("apc-m13-chorus", r"""public class Solution {
    public static class Animal {
        public String sound() {
            return "hmm";
        }
    }

    public static class Cow extends Animal {
        public String sound() {
            return "moo";
        }
    }

    public static class Duck extends Animal {
        public String sound() {
            return "quack";
        }
    }

    public static String chorus(Animal a, Animal b) {
        return a.sound() + " " + b.sound();
    }
}
""",
         r"""public class Solution {
    public static class Animal {
        public String sound() {
            return "hmm";
        }
    }

    public static class Cow extends Animal {
        public String sound() {
            // BUG: accidentally calls the superclass version
            return super.sound();
        }
    }

    public static class Duck extends Animal {
        public String sound() {
            return "quack";
        }
    }

    public static String chorus(Animal a, Animal b) {
        return a.sound() + " " + b.sound();
    }
}
"""),
        ("apc-m13-fix-bigbox", r"""public class Solution {
    public static class Box {
        private String tag;

        public Box(String tag) {
            this.tag = tag;
        }

        public String getTag() {
            return tag;
        }

        public int size() {
            return 1;
        }
    }

    public static class BigBox extends Box {
        private int factor;

        public BigBox(String tag, int factor) {
            super(tag);
            this.factor = factor;
        }

        public int size() {
            return factor;
        }
    }
}
""",
         r"""public class Solution {
    public static class Box {
        private String tag;

        public Box(String tag) {
            this.tag = tag;
        }

        public String getTag() {
            return tag;
        }

        public int size() {
            return 1;
        }
    }

    public static class BigBox extends Box {
        // BUG: original flaw kept — no super(tag) chain, factor unstored
        private int factor;

        public BigBox(String tag, int factor) {
        }

        public int size() {
            return factor;
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m13", "Checkpoint: override with state",
    "Chain a constructor, override a mutator, keep inherited behavior via super.",
    25,
    r"""
The pattern: extend behavior without reimplementing it. `super.deposit`
does the storage work; the override only adds the bookkeeping. This
compose-don't-copy habit is what separates a 9 from a 5 on FRQ 2/4 hybrids.
""",
    "Điểm kiểm tra: ghi đè có trạng thái",
    "Nối hàm dựng, ghi đè một mutator, giữ hành vi kế thừa qua super.",
    r"""
Mẫu hình: mở rộng hành vi mà không cài lại. `super.deposit` làm việc lưu
trữ; phần ghi đè chỉ thêm sổ sách. Thói quen hợp-thay-vì-chép này là điều
tách điểm 9 khỏi điểm 5 ở các bài FRQ lai 2/4.
""",
    CP13C,
    vi_challenge("Điểm kiểm tra: ghi đè có trạng thái", "Hoàn thiện `BonusAccount extends Account`: nối hàm dựng lên trên, giữ một bộ đếm nạp tiền private khởi đầu 0, và ghi đè `deposit(amount)` để đếm lần nạp rồi thực hiện nạp thường (tái dùng phương thức lớp cha).",
        [("counting override", "super.deposit(amount); lo phần số dư — ghi đè chỉ thêm việc đếm.")]),
    solution=r"""public class Solution {
    public static class Account {
        private String owner;
        private int balance;

        public Account(String owner, int balance) {
            this.owner = owner;
            this.balance = balance;
        }

        public String getOwner() {
            return owner;
        }

        public int getBalance() {
            return balance;
        }

        public void deposit(int amount) {
            balance = balance + amount;
        }
    }

    public static class BonusAccount extends Account {
        private int deposits;

        public BonusAccount(String owner, int balance) {
            super(owner, balance);
            deposits = 0;
        }

        public void deposit(int amount) {
            deposits++;
            super.deposit(amount);
        }

        public int getDeposits() {
            return deposits;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Account {
        private String owner;
        private int balance;

        public Account(String owner, int balance) {
            this.owner = owner;
            this.balance = balance;
        }

        public String getOwner() {
            return owner;
        }

        public int getBalance() {
            return balance;
        }

        public void deposit(int amount) {
            balance = balance + amount;
        }
    }

    public static class BonusAccount extends Account {
        // BUG: override reimplements the deposit but FORGETS the balance —
        // only the counter moves
        private int deposits;

        public BonusAccount(String owner, int balance) {
            super(owner, balance);
            deposits = 0;
        }

        public void deposit(int amount) {
            deposits++;
        }

        public int getDeposits() {
            return deposits;
        }
    }
}
""",
)
