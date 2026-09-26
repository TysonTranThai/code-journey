#!/usr/bin/env python3
"""AP CSA Core M10 — Inheritance & Polymorphism (dispatch + traps)."""
from apcc import *

M = "cx-inheritance"

L1 = r"""
The exam's inheritance questions all resolve to one question: **which
method body actually runs?** The answer is the *object's* class, never
the reference's type — except constructors.

```java
public class Animal {
    public String speak() { return "..."; }
    public String name() { return "animal"; }
}

public class Dog extends Animal {
    public String speak() { return "Woof"; }   // OVERRIDES
}

Animal a = new Dog();
System.out.println(a.speak());   // "Woof" — the DOG's method
System.out.println(a.name());    // "animal" — inherited, not overridden
```

`a` is declared as Animal but holds a Dog: every non-constructor call
dispatches on the real object. Write the **dispatch table** — one row
per method, naming the class whose body executes:

| call         | body that runs |
| ------------ | -------------- |
| `a.speak()`  | Dog.speak      |
| `a.name()`   | Animal.name    |

**What an override can change:** only the body (and it may not weaken
visibility). **What it cannot change:** the signature — change a
parameter type and you have *overloaded* instead, and the superclass
version still runs for old calls. This silent-overload trap is the #1
inheritance MCQ.

`super.method(args)` calls the parent's version explicitly — used when
the override extends rather than replaces the parent behavior.
"""

L2 = r"""
Constructors are the exception to dispatch-on-object: **they run
top-down** — superclass body first, then down the chain:

```java
public class Pet {
    protected String name;
    public Pet(String name) { this.name = name; }
}

public class Cat extends Pet {
    private int lives;
    public Cat(String name, int lives) {
        super(name);            // MUST be first statement
        this.lives = lives;
    }
}
```

Rules the exam tests:

1. If the subclass constructor calls `super(...)`, it must be the
   **first statement**.
2. If it does not call super at all, Java inserts `super()` — the
   parent's NO-ARG constructor. When the parent has only a
   String-arg constructor, that insertion is a **compile error**:
   "constructor Pet in class Pet cannot be applied to given types".
3. `protected` fields are visible to subclasses (and the same package)
   — `private` ones are not, which is why Cat goes through
   `super(name)` instead of touching `name` directly.

The chain order explains tracing questions: `new Cat("M", 9)` runs
Pet's body (name = "M"), then Cat's body (lives = 9). State builds
from the top of the hierarchy down.
"""

L3 = r"""
Polymorphic collections — the exam's synthesis shape:

```java
ArrayList<Animal> zoo = new ArrayList<Animal>();
zoo.add(new Dog());          // Dog is-an Animal
zoo.add(new Animal());
zoo.add(new Dog());
for (Animal a : zoo) {
    System.out.println(a.speak());   // Woof, ..., Woof
}
```

One loop, three objects, two behaviors — the reference type is Animal,
the dispatch is per-object. Remove-by-content or count-by-behavior on
such a list is the FRQ variant: "how many animals speak Woof?" is a
for-each plus a dispatch trace.

**The cast question.** `Animal a = new Dog(); Dog d = a;` does NOT
compile — Animal is not known to be Dog. `Dog d = (Dog) a;` compiles
and runs (a really holds a Dog). `(Cat) a` would compile but throw
ClassCastException at runtime. The exam asks which of these three
lines compiles/runs — the rule: **upcasts are free, downcasts need an
explicit cast, wrong downcasts explode at runtime.**

**The Object trap.** `equals` takes Object:

```java
public boolean equals(Dog other) { ... }   // OVERLOAD, not override!
```

The parameter type must be Object to truly override. In AP scope you
just need to recognize the shape: same signature = override; changed
signature = overload.
"""

write_module(
    M,
    "Inheritance & Polymorphism",
    "Dispatch tables, constructor chaining with super, the override-vs-overload trap, and polymorphic collections.",
    "Kế thừa & đa hình",
    "Bảng điều phối, chuỗi constructor với super, cái bẫy override-vs-overload, và bộ sưu tập đa hình.",
    lessons=["cx-m10-dispatch", "cx-m10-ctors", "cx-m10-polycollections", "cx-cp-m10"],
    practices=["cx-p10-inheritance"],
)

write_lesson(
    M, "cx-m10-dispatch", "The dispatch table",
    "Which body actually runs: the object's class decides, constructors excepted.",
    12, L1,
    "Bảng điều phối",
    "Thân phương thức nào thật sự chạy: lớp của đối tượng quyết định, trừ constructor.",
    r"""
Mọi câu hỏi kế thừa của đề thi đều quy về một câu: **thân phương thức
nào thật sự chạy?** Đáp án là lớp của *đối tượng*, không bao giờ là kiểu
của tham chiếu — trừ constructor.

```java
public class Animal {
    public String speak() { return "..."; }
    public String name() { return "animal"; }
}

public class Dog extends Animal {
    public String speak() { return "Woof"; }   // OVERRIDE
}

Animal a = new Dog();
System.out.println(a.speak());   // "Woof" — phương thức của DOG
System.out.println(a.name());    // "animal" — kế thừa, không bị override
```

`a` được khai báo là Animal nhưng giữ một Dog: mọi lời gọi không-phải-
constructor điều phối theo đối tượng thật. Hãy viết **bảng điều phối** —
mỗi phương thức một hàng, gọi tên lớp whose thân chạy:

| lời gọi      | thân chạy      |
| ------------ | -------------- |
| `a.speak()`  | Dog.speak      |
| `a.name()`   | Animal.name    |

**Override được phép đổi:** chỉ phần thân (và không được hạ thấp quyền
truy cập). **Không được phép đổi:** chữ ký — đổi kiểu tham số là bạn đã
*overload* thay vì override, và phiên bản superclass vẫn chạy cho các
lời gọi cũ. Cái bẫy overload-im-lặng này là câu MCQ kế thừa số một.

`super.method(args)` gọi tường minh phiên bản của cha — dùng khi override
mở rộng thay vì thay thế hành vi của cha.
""",
)

write_lesson(
    M, "cx-m10-ctors", "Constructor chains",
    "super first, implicit super(), protected visibility, top-down state build.",
    12, L2,
    "Chuỗi constructor",
    "super trước, super() ngầm định, quyền thấy protected, dựng trạng thái từ trên xuống.",
    r"""
Constructor là ngoại lệ của điều-phối-theo-đối-tượng: **chúng chạy từ
trên xuống** — thân superclass trước, rồi xuống dọc chuỗi:

```java
public class Pet {
    protected String name;
    public Pet(String name) { this.name = name; }
}

public class Cat extends Pet {
    private int lives;
    public Cat(String name, int lives) {
        super(name);            // PHẢI là câu lệnh đầu tiên
        this.lives = lives;
    }
}
```

Các luật đề thi kiểm tra:

1. Nếu constructor lớp con gọi `super(...)`, nó phải là **câu lệnh đầu
   tiên**.
2. Nếu không gọi super nào cả, Java chèn sẵn `super()` — constructor
   KHÔNG-ĐỐI-SỐ của cha. Khi cha chỉ có constructor nhận String, phép
   chèn đó là **lỗi biên dịch**: "constructor Pet in class Pet cannot
   be applied to given types".
3. Trường `protected` được các lớp con nhìn thấy (và cùng package) —
   `private` thì không, vì sao Cat phải đi qua `super(name)` thay vì
   chạm thẳng vào `name`.

Thứ tự chuỗi giải thích các câu truy vết: `new Cat("M", 9)` chạy thân
Pet (name = "M"), rồi thân Cat (lives = 9). Trạng thái được dựng từ đỉnh
cây phân cấp đi xuống.
""",
)

write_lesson(
    M, "cx-m10-polycollections", "Polymorphic collections",
    "One reference type, many behaviors; the three cast cases; the Object trap.",
    12, L3,
    "Bộ sưu tập đa hình",
    "Một kiểu tham chiếu, nhiều hành vi; ba trường hợp ép kiểu; cái bẫy Object.",
    r"""
Bộ sưu tập đa hình — hình tổng hợp của đề thi:

```java
ArrayList<Animal> zoo = new ArrayList<Animal>();
zoo.add(new Dog());          // Dog is-an Animal
zoo.add(new Animal());
zoo.add(new Dog());
for (Animal a : zoo) {
    System.out.println(a.speak());   // Woof, ..., Woof
}
```

Một vòng lặp, ba đối tượng, hai hành vi — kiểu tham chiếu là Animal,
điều phối theo từng đối tượng. Xóa-theo-nội-dung hay đếm-theo-hành-vi
trên danh sách dạng này chính là biến thể FRQ: "bao nhiêu con vật kêu
Woof?" là một for-each cộng một phép truy vết điều phối.

**Câu hỏi ép kiểu.** `Animal a = new Dog(); Dog d = a;` KHÔNG biên dịch
— Animal không được biết là Dog. `Dog d = (Dog) a;` biên dịch và chạy
được (a thật sự giữ một Dog). `(Cat) a` biên dịch được nhưng ném
ClassCastException lúc chạy. Đề thi hỏi dòng nào trong ba dòng trên
biên dịch/chạy — luật: **ép-lên miễn phí, ép-xuống cần ép kiểu tường
minh, ép-xuống sai nổ tung lúc chạy.**

**Cái bẫy Object.** `equals` nhận Object:

```java
public boolean equals(Dog other) { ... }   // OVERLOAD, không phải override!
```

Kiểu tham số phải là Object mới thật sự override. Trong phạm vi AP bạn
chỉ cần nhận ra hình dạng: cùng chữ ký = override; đổi chữ ký = overload.
""",
)

ZOO = r"""public class Solution {
    public static class Animal {
        public String speak() { return "..."; }
        public int legs() { return 4; }
    }
    public static class Dog extends Animal {
        public String speak() { return "Woof"; }
    }
    public static class Bird extends Animal {
        public String speak() { return "Chirp"; }
        public int legs() { return 2; }
    }

    // CONTRACT: count the animals in the zoo whose speak() equals sound.
    public static int countSpeakers(Animal[] zoo, String sound) {
        return 0; // replace
    }
}
"""

BOILER_PUPPY = r"""public class Solution {
    public static class Animal {
        public String describe() { return "an animal"; }
    }
    public static class Dog extends Animal {
        public String describe() { return "a dog"; }
    }
    public static class Puppy extends Dog {
        public String describe() { return super.describe() + " (young)"; }
    }

    // CONTRACT: already implemented — predict via dispatch table.
    public static String describe(Animal a) { return a.describe(); }
}
"""

BOILER_VEHICLES = r"""public class Solution {
    public static class Vehicle {
        protected String label;
        public Vehicle(String label) { this.label = label; }
        public String getLabel() { return label; }
    }
    public static class Car extends Vehicle {
        private int doors;
        public Car(String label, int doors) {
            super(label);
            this.doors = doors;
        }
        public int getDoors() { return doors; }
    }

    // CONTRACT: build a car "taxi" with 4 doors and return
    // its label and doors joined as "taxi:4".
    public static String makeCar() {
        return ""; // replace
    }
}
"""

BOILER_NOSUPER = r"""public class Solution {
    public static class Item {
        private String name;
        public Item(String name) { this.name = name; }
        public String getName() { return name; }
    }
    public static class Discounted extends Item {
        private int percent;
        public Discounted(String name, int percent) {
            // BUG: does not call super, and Item has no no-arg constructor
            this.percent = percent;
        }
        public int getPercent() { return percent; }
    }
}
"""

BOILER_SHADOWFIELD = r"""public class Solution {
    public static class Base {
        protected int v = 1;
        public int getV() { return v; }
    }
    public static class Derived extends Base {
        protected int v = 2;   // shadows Base's v

        // CONTRACT: return Base's v (the inherited, shadowed one) —
        // achievable with what the lesson shows.
        public int baseV() {
            return v; // BUG: returns Derived's v
        }
    }
}
"""

BOILER_CP10 = r"""public class Solution {
    public static class Shape {
        public String name() { return "shape"; }
        public double area() { return 0; }
    }
    public static class Rect extends Shape {
        private double w, h;
        public Rect(double w, double h) { this.w = w; this.h = h; }
        public String name() { return "rect"; }
        public double area() { return w * h; }
    }
    public static class Square extends Rect {
        public Square(double side) { super(side, side); }
        public String name() { return "square"; }
    }

    // CONTRACT: total area of all shapes, rounded down to an int.
    public static int totalArea(Shape[] shapes) {
        return 0; // replace
    }
}
"""

P_ZOO = challenge(
    "cx-m10-zoo-count",
    "Dispatch in a collection",
    "Implement `int countSpeakers(Animal[] zoo, String sound)`: count the animals whose speak() equals sound. Bird overrides legs too — trace which body runs for each call.",
    ZOO,
    [(
        "speakers counted",
        r"""
Solution.Animal[] zoo = { new Solution.Dog(), new Solution.Bird(), new Solution.Animal(), new Solution.Dog() };
CjTestBase.checkEq(Solution.countSpeakers(zoo, "Woof"), 2, "two dogs");
CjTestBase.checkEq(Solution.countSpeakers(zoo, "Chirp"), 1, "one bird");
CjTestBase.checkEq(Solution.countSpeakers(zoo, "..."), 1, "plain animal");
CjTestBase.checkEq(Solution.countSpeakers(new Solution.Animal[]{}, "Woof"), 0, "empty zoo");
""",
        "For-each + a.speak().equals(sound) — dispatch does the work.",
    )],
    level="guided",
)

P_PUPPY = challenge(
    "cx-m10-puppy-chain",
    "Dispatch chain, three deep",
    "`describe(Animal)` is implemented. Predict via the dispatch table: what does it return for a Puppy? A Dog? A plain Animal? Confirm by keeping the code as-is and making the tests pass (the tests encode the correct answers).",
    BOILER_PUPPY,
    [(
        "chained dispatch",
        r"""
CjTestBase.checkEq(Solution.describe(new Solution.Puppy()), "a dog (young)", "super.extend then dispatch");
CjTestBase.checkEq(Solution.describe(new Solution.Dog()), "a dog", "Dog's body");
CjTestBase.checkEq(Solution.describe(new Solution.Animal()), "an animal", "Animal's body");
""",
        "Puppy.describe calls super.describe() = Dog's body, then appends.",
    )],
    level="independent",
)

P_VEHICLE = challenge(
    "cx-m10-vehicle-ctor",
    "Constructor chaining",
    "Complete `makeCar()`: build a Car \"taxi\" with 4 doors and return \"taxi:4\". The Car constructor must chain super(label) first — the lesson's rule 1.",
    BOILER_VEHICLES,
    [(
        "chained construction",
        r"""
CjTestBase.checkEq(Solution.makeCar(), "taxi:4", "label:doors");
""",
        "Car c = new Car(\"taxi\", 4); return c.getLabel() + \":\" + c.getDoors();",
    )],
    level="imitation",
)

P_NOSUPER = challenge(
    "cx-m10-fix-super",
    "Fix the missing super",
    "`Discounted` does not compile: the implicit super() needs a no-arg Item constructor, which does not exist. Apply rule 2's fix with the exact one line.",
    BOILER_NOSUPER,
    [(
        "chain repaired",
        r"""
Solution.Discounted d = new Solution.Discounted("book", 10);
CjTestBase.checkEq(d.getName(), "book", "name flows through super");
CjTestBase.checkEq(d.getPercent(), 10, "percent stored");
""",
        "super(name); must be the FIRST statement in the constructor.",
    )],
    level="debugging",
)

P_SHADOWFIELD = challenge(
    "cx-m10-fix-shadow-field",
    "Field shadowing across the hierarchy",
    "`Derived` declares its own v, shadowing Base's. Complete `baseV()` so it returns BASE's v using the lesson's mechanism.",
    BOILER_SHADOWFIELD,
    [(
        "base value recovered",
        r"""
Solution.Derived d = new Solution.Derived();
CjTestBase.checkEq(d.baseV(), 1, "Base's v, not Derived's");
""",
        "super.getV() — route through the superclass accessor.",
    )],
    level="debugging",
)

CP10 = challenge(
    "cx-cp-m10-zoo-area",
    "Checkpoint: shape dispatch",
    "Complete `int totalArea(Shape[] shapes)`: sum every shape's area() via dispatch and round DOWN to an int. Square chains through Rect. One loop, one accumulator, zero instanceof — dispatch does the branching.",
    BOILER_CP10,
    [(
        "total via dispatch",
        r"""
Solution.Shape[] shapes = { new Solution.Rect(2, 3), new Solution.Square(4), new Solution.Shape() };
CjTestBase.checkEq(Solution.totalArea(shapes), 22, "6 + 16 + 0");
CjTestBase.checkEq(Solution.totalArea(new Solution.Shape[]{}), 0, "empty");
Solution.Shape[] one = { new Solution.Square(3) };
CjTestBase.checkEq(Solution.totalArea(one), 9, "square chains super(side, side)");
""",
        "int total = 0; for each: total += s.area(); return total; — 16.5 would truncate, but our values are whole.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p10-inheritance", "Inheritance lab",
    "Dispatch counts, constructor chains, missing-super repair, field shadowing.",
    "Phòng kế thừa",
    "Đếm bằng điều phối, chuỗi constructor, sửa thiếu super, che khuất trường.",
    after_lesson="cx-m10-ctors", minutes=55, difficulty="advanced",
    challenges=[P_ZOO, P_PUPPY, P_VEHICLE, P_NOSUPER, P_SHADOWFIELD],
    vi_challenges={
        "cx-m10-zoo-count": vi_challenge("Điều phối trong bộ sưu tập",
            "Hiện thực `int countSpeakers(Animal[] zoo, String sound)`: đếm các con vật có speak() bằng sound. Bird cũng override legs — truy vết thân nào chạy cho mỗi lời gọi.",
            [("speakers counted", "For-each + a.speak().equals(sound) — điều phối lo phần còn lại.")]),
        "cx-m10-puppy-chain": vi_challenge("Chuỗi điều phối sâu ba tầng",
            "`describe(Animal)` đã hiện thực. Dự đoán qua bảng điều phối: nó trả về gì cho Puppy? Cho Dog? Cho Animal thường? Xác nhận bằng cách giữ nguyên mã và làm test pass (test mã hóa đáp án đúng).",
            [("chained dispatch", "Puppy.describe gọi super.describe() = thân Dog, rồi nối thêm.")]),
        "cx-m10-vehicle-ctor": vi_challenge("Chuỗi constructor",
            "Hoàn thiện `makeCar()`: dựng một Car \"taxi\" với 4 cửa và trả về \"taxi:4\". Constructor của Car phải nối super(label) trước — luật 1 trong bài học.",
            [("chained construction", "Car c = new Car(\"taxi\", 4); return c.getLabel() + \":\" + c.getDoors();")]),
        "cx-m10-fix-super": vi_challenge("Sửa thiếu super",
            "`Discounted` không biên dịch được: super() ngầm cần constructor Item không-đối-số, vốn không tồn tại. Áp dụng bản sửa của luật 2 với đúng một dòng.",
            [("chain repaired", "super(name); phải là câu lệnh ĐẦU TIÊN trong constructor.")]),
        "cx-m10-fix-shadow-field": vi_challenge("Che khuất trường qua phân cấp",
            "`Derived` tự khai báo v riêng, che khuất v của Base. Hoàn thiện `baseV()` để nó trả về v của BASE bằng cơ chế trong bài học.",
            [("base value recovered", "super.getV() — đi đường vòng qua accessor của superclass.")]),
    },
    solutions=[
        ("cx-m10-zoo-count", ZOO.replace("        return 0; // replace",
            "        int count = 0;\n        for (Animal a : zoo) {\n            if (a.speak().equals(sound)) {\n                count++;\n            }\n        }\n        return count;"),
         ZOO.replace("        return 0; // replace",
            "        int count = 0;\n        for (Animal a : zoo) {\n            if (a.legs() == 4) {\n                count++;\n            }\n        }\n        return count;")),
        ("cx-m10-puppy-chain", BOILER_PUPPY,
         BOILER_PUPPY.replace("public String describe() { return super.describe() + \" (young)\"; }",
            "public String describe() { return \"a puppy\"; }")),
        ("cx-m10-vehicle-ctor", BOILER_VEHICLES.replace("        return \"\"; // replace",
            "        Car c = new Car(\"taxi\", 4);\n        return c.getLabel() + \":\" + c.getDoors();"),
         BOILER_VEHICLES.replace("        return \"\"; // replace",
            "        Car c = new Car(\"taxi\", 4);\n        return c.getDoors() + \":\" + c.getLabel();")),
        ("cx-m10-fix-super", BOILER_NOSUPER.replace("            // BUG: does not call super, and Item has no no-arg constructor\n            this.percent = percent;",
            "            super(name);\n            this.percent = percent;"),
         BOILER_NOSUPER.replace("            // BUG: does not call super, and Item has no no-arg constructor\n            this.percent = percent;",
            "            this.percent = percent;\n            super(name);")),
        ("cx-m10-fix-shadow-field", BOILER_SHADOWFIELD.replace("            return v; // BUG: returns Derived's v",
            "            return super.getV();"),
         BOILER_SHADOWFIELD),
    ],
)

write_checkpoint(
    M, "cx-cp-m10", "Checkpoint: shape dispatch",
    "Polymorphic totalArea — one loop, dispatch does the branching.",
    25,
    r"""
totalArea is the inheritance synthesis in miniature: a Shape[] where
every element answers area() in its own way, and the loop neither knows
nor cares which concrete class it holds. If your trace needed
instanceof, the dispatch table was missing — the object's class already
made the decision. This shape (one reference type, per-object behavior,
one accumulator) is the entire inheritance MCQ genre compressed.
""",
    "Điểm kiểm tra: điều phối hình học",
    "totalArea đa hình — một vòng lặp, điều phối lo việc rẽ nhánh.",
    r"""
totalArea là bản thu nhỏ của tổng hợp kế thừa: một Shape[] mà mọi phần
tử trả lời area() theo cách riêng, và vòng lặp không cần biết cũng không
quan tâm nó giữ lớp cụ thể nào. Nếu phép truy vết của bạn cần instanceof,
là bảng điều phối còn thiếu — lớp của đối tượng đã quyết định sẵn rồi.
Hình dạng này (một kiểu tham chiếu, hành vi theo từng đối tượng, một bộ
cộng dồn) là toàn thể loại MCQ kế thừa nén lại.
""",
    CP10,
    vi_challenge("Điểm kiểm tra: điều phối hình học",
        "Hoàn thiện `int totalArea(Shape[] shapes)`: cộng dồn area() của mọi hình qua điều phối và làm tròn XUỐNG thành int. Square nối chuỗi qua Rect. Một vòng lặp, một bộ cộng dồn, không instanceof — điều phối lo việc rẽ nhánh.",
        [("total via dispatch", "int total = 0; với mỗi hình: total += s.area(); return total;")]),
    solution=r"""public class Solution {
    public static class Shape {
        public String name() { return "shape"; }
        public double area() { return 0; }
    }
    public static class Rect extends Shape {
        private double w, h;
        public Rect(double w, double h) { this.w = w; this.h = h; }
        public String name() { return "rect"; }
        public double area() { return w * h; }
    }
    public static class Square extends Rect {
        public Square(double side) { super(side, side); }
        public String name() { return "square"; }
    }

    public static int totalArea(Shape[] shapes) {
        double total = 0;
        for (Shape s : shapes) {
            total += s.area();
        }
        return (int) total;
    }
}
""",
    wrong=r"""public class Solution {
    public static class Shape {
        public String name() { return "shape"; }
        public double area() { return 0; }
    }
    public static class Rect extends Shape {
        private double w, h;
        public Rect(double w, double h) { this.w = w; this.h = h; }
        public String name() { return "rect"; }
        public double area() { return w * h; }
    }
    public static class Square extends Rect {
        public Square(double side) { super(side, side); }
        public String name() { return "square"; }
    }

    public static int totalArea(Shape[] shapes) {
        double total = 0;
        for (Shape s : shapes) {
            if (s.name().equals("rect")) {
                total += s.area();
            }
        }
        return (int) total;
    }
}
""",
)
