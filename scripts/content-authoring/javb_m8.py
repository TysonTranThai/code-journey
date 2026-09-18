#!/usr/bin/env python3
"""Java — Beginner — Module 8: java-oop-design."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-oop-design"

L_INHERIT_EN = r'''
**Inheritance** lets a class reuse and specialize another class's fields and
methods. The parent is the *superclass*, the child the *subclass*:

```java
class Vehicle {
    private final String name;
    private int speed = 0;

    Vehicle(String name) { this.name = name; }

    public void accelerate(int by) { speed += by; }
    public int getSpeed() { return speed; }
    public String getName() { return name; }
}

class ElectricCar extends Vehicle {
    private int batteryPercent = 100;

    public ElectricCar(String name) { super(name); }   // build the parent first

    public void drainBattery(int by) { batteryPercent -= by; }
    public int getBatteryPercent() { return batteryPercent; }
}
```

`ElectricCar` **is-a** Vehicle: it accelerates, has a speed and a name —
inherited — plus its own battery. Two new keywords:

- `extends` declares the relationship. Java allows **one** direct
  superclass (no diamond of parents).
- `super(...)` calls the parent constructor; it must be the FIRST statement.
  If you omit it, Java inserts a silent `super()` — which only compiles when
  the parent has a no-argument constructor.

`private` fields are inherited but *invisible* to the subclass — the child
owns them without being able to touch them directly. That is deliberate:
the parent's rules stay intact. When a subclass genuinely needs access,
`protected` opens the door to subclasses (while still closing it to the
world).

**Inheritance is a design decision, not a default.** It fits when the
relationship is a true is-a that stays true forever ("an ElectricCar is a
Vehicle"). When the relationship is has-a ("a Car **has an** Engine"), use
**composition** — a field holding the other object — which is more flexible
and never breaks under change. Rule of thumb for this course: reach for
inheritance only when every subclass must satisfy the same contract; reach
for composition when you merely want to reuse behavior.

**Next:** overriding — specializing inherited behavior.
'''

L_INHERIT_VI = r'''
**Kế thừa (inheritance)** cho phép một class tái sử dụng và chuyên biệt hóa
class khác. Lớp cha là *superclass*, lớp con là *subclass*:

```java
class Vehicle {
    private final String name;
    private int speed = 0;

    Vehicle(String name) { this.name = name; }

    public void accelerate(int by) { speed += by; }
    public int getSpeed() { return speed; }
    public String getName() { return name; }
}

class ElectricCar extends Vehicle {
    private int batteryPercent = 100;

    public ElectricCar(String name) { super(name); }   // dựng cha trước

    public void drainBattery(int by) { batteryPercent -= by; }
    public int getBatteryPercent() { return batteryPercent; }
}
```

`ElectricCar` **is-a** Vehicle: nó tăng tốc, có tốc độ và tên — được kế
thừa — cộng thêm pin của riêng mình. Hai từ khóa mới:

- `extends` khai báo quan hệ. Java chỉ cho **một** superclass trực tiếp
  (không có kim tự tháp cha mẹ).
- `super(...)` gọi constructor của cha; nó phải là câu lệnh ĐẦU TIÊN. Nếu
  bạn bỏ qua, Java lặng lẽ chèn `super()` — chỉ biên dịch được khi cha có
  constructor không đối số.

Trường `private` được kế thừa nhưng *vô hình* với subclass — con sở hữu
chúng mà không chạm trực tiếp được. Điều đó là chủ đích: quy tắc của cha
giữ nguyên vẹn. Khi subclass thật sự cần truy cập, `protected` mở cửa cho
con cháu (vẫn đóng cửa với thế giới bên ngoài).

**Kế thừa là một quyết định thiết kế, không phải mặc định.** Nó hợp khi
quan hệ là is-a đúng nghĩa và mãi mãi đúng ("ElectricCar là Vehicle"). Khi
quan hệ là has-a ("Car **có** Engine"), hãy dùng **composition** — một
trường chứa object kia — linh hoạt hơn và không bao giờ gãy khi thay đổi.
Quy tắc cho khóa học này: chỉ gọi kế thừa khi mọi subclass phải thỏa cùng
một hợp đồng; gọi composition khi bạn chỉ muốn tái sử dụng hành vi.

**Tiếp theo:** overriding — chuyên biệt hóa hành vi kế thừa.
'''

L_POLY_EN = r'''
**Polymorphism** = one call site, many behaviors. An object of a subclass
can be used anywhere the superclass is expected, and the *object's own*
version of an overridden method runs:

```java
class Shape {
    public double area() { return 0; }
    public String describe() { return "a shape"; }
}

class Circle extends Shape {
    private final double r;
    Circle(double r) { this.r = r; }

    @Override
    public double area() { return Math.PI * r * r; }

    @Override
    public String describe() { return "a circle"; }
}

class Rectangle extends Shape {
    private final double w, h;
    Rectangle(double w, double h) { this.w = w; this.h = h; }

    @Override
    public double area() { return w * h; }

    @Override
    public String describe() { return "a rectangle"; }
}
```

Now the payoff — one loop, many behaviors:

```java
Shape[] shapes = { new Circle(2), new Rectangle(3, 4) };
for (Shape s : shapes) {
    System.out.println(s.describe() + " area=" + s.area());
}
// a circle area=12.566...
// a rectangle area=12.0
```

The variable is a `Shape`; the behavior is the *object's* class. The JVM
picks the right override at run time — this dispatch is the machinery that
makes frameworks possible.

**`@Override` is a contract with the compiler.** The annotation is optional
in syntax but mandatory in this course: with it, a typo'd signature
(`area(Shape this)`, a misspelled name) becomes a compile ERROR instead of
a silently-new method. Without it, "overriding" that fails to override is
one of the quietest bug classes in Java.

**A subclass may keep the parent's behavior**: `super.method()` calls the
parent version from inside an override — useful for "do what you did, plus
this".

**Next:** interfaces — contracts without implementation.
'''

L_POLY_VI = r'''
**Đa hình (polymorphism)** = một chỗ gọi, nhiều hành vi. Object của subclass
có thể được dùng ở bất cứ nơi nào superclass được mong đợi, và phiên bản
phương thức *của chính object* sẽ chạy:

```java
class Shape {
    public double area() { return 0; }
    public String describe() { return "a shape"; }
}

class Circle extends Shape {
    private final double r;
    Circle(double r) { this.r = r; }

    @Override
    public double area() { return Math.PI * r * r; }

    @Override
    public String describe() { return "a circle"; }
}

class Rectangle extends Shape {
    private final double w, h;
    Rectangle(double w, double h) { this.w = w; this.h = h; }

    @Override
    public double area() { return w * h; }

    @Override
    public String describe() { return "a rectangle"; }
}
```

Và đây là phần thưởng — một vòng lặp, nhiều hành vi:

```java
Shape[] shapes = { new Circle(2), new Rectangle(3, 4) };
for (Shape s : shapes) {
    System.out.println(s.describe() + " area=" + s.area());
}
// a circle area=12.566...
// a rectangle area=12.0
```

Biến có kiểu `Shape`; hành vi thuộc về class của *object*. JVM chọn đúng
bản override lúc chạy — cơ chế điều phối này là thứ làm nên các framework.

**`@Override` là một hợp đồng với compiler.** Về cú pháp annotation này là
tùy chọn nhưng trong khóa học này là bắt buộc: với nó, một chữ ký gõ sai
(tên thiếu ký tự, sai đối số) thành lỗi BIÊN DỊCH thay vì một phương thức
mới lặng lẽ không ai gọi. Không có nó, "override" thất bại là một trong
những dòng bug thầm lặng nhất của Java.

**Subclass có thể giữ hành vi của cha**: `super.method()` gọi phiên bản cha
từ bên trong một override — tiện cho dạng "làm như cũ, cộng thêm điều này".

**Tiếp theo:** interface — hợp đồng không kèm cài đặt.
'''

L_INTERFACES_EN = r'''
An **interface** is a pure contract: method signatures (and constants) with
no fields and, traditionally, no bodies. A class *implements* an interface
and promises to provide every method:

```java
interface Describable {
    String describe();          // implicitly public and abstract
}

interface Priceable {
    double price();
}

class Book implements Describable, Priceable {
    private final String title;
    private final double cost;

    Book(String title, double cost) { this.title = title; this.cost = cost; }

    @Override
    public String describe() { return "Book: " + title; }

    @Override
    public double price() { return cost; }
}
```

**A class can implement MANY interfaces** — that is the escape hatch from
single inheritance. Interfaces state *capability* ("can be described",
"has a price"); inheritance states *identity* ("is a Vehicle"). Modern
design leans on capabilities: accept `Describable`, and your method works
with Books, Movies, and everything your users invent later.

Interfaces already in your life: `Comparable` (has `compareTo` — sorting),
`Runnable` (has `run` — threads), `Iterable` (has `iterator` — for-each
works on anything implementing it).

**Polymorphism works through interfaces** exactly as through superclasses:

```java
Describable[] items = { new Book("Dune", 12.5) };
for (Describable d : items) {
    System.out.println(d.describe());
}
```

Since Java 8 an interface may also carry `default` methods (bodies usable
by implementors as-is) and `static` methods — handy for evolving contracts
without breaking every implementor. Beginners should still think of an
interface as "a promise list"; defaults are a migration tool.

**Choosing between them:** extends for shared identity and state; implements
for shared capability. When unsure, prefer the interface — it costs less
and promises less.

**Next:** composition, the quiet workhorse.
'''

L_INTERFACES_VI = r'''
**Interface** là hợp đồng thuần: chữ ký phương thức (và hằng số) không có
trường và theo truyền thống không có thân. Một class *implements* interface
và hứa cung cấp mọi phương thức:

```java
interface Describable {
    String describe();          // mặc định public và abstract
}

interface Priceable {
    double price();
}

class Book implements Describable, Priceable {
    private final String title;
    private final double cost;

    Book(String title, double cost) { this.title = title; this.cost = cost; }

    @Override
    public String describe() { return "Book: " + title; }

    @Override
    public double price() { return cost; }
}
```

**Một class có thể implement NHIỀU interface** — đó là lối thoát khỏi việc
chỉ được kế thừa một class. Interface phát biểu *năng lực* ("mô tả được",
"có giá"); kế thừa phát biểu *danh tính* ("là Vehicle"). Thiết kế hiện đại
nghiêng về năng lực: nhận `Describable`, và phương thức của bạn chạy với
Book, Movie, và mọi thứ người dùng sẽ thêm sau này.

Những interface đã có trong đời bạn: `Comparable` (có `compareTo` — sorting),
`Runnable` (có `run` — thread), `Iterable` (có `iterator` — for-each chạy
trên mọi thứ implement nó).

**Đa hình chạy qua interface** y như qua superclass:

```java
Describable[] items = { new Book("Dune", 12.5) };
for (Describable d : items) {
    System.out.println(d.describe());
}
```

Từ Java 8, interface còn có phương thức `default` (có thân, implementor dùng
ngay) và phương thức `static` — tiện cho việc tiến hóa hợp đồng mà không làm
gãy mọi implementor. Người mới vẫn nên nhìn interface như "một danh sách lời
hứa"; default là công cụ di trú.

**Chọn giữa chúng:** extends cho danh tính và trạng thái chung; implements
cho năng lực chung. Không chắc thì chọn interface — chi phí thấp hơn và
lời hứa ít hơn.

**Tiếp theo:** composition, con ngựa thầm lặng kéo mọi thiết kế.
'''

L_COMPOSITION_EN = r'''
**Composition** means building complex behavior from simpler objects held
as fields — "has-a" instead of "is-a".

```java
class Engine {
    void start() { System.out.println("vroom"); }
}

class Car {
    private final Engine engine = new Engine();   // Car HAS-AN Engine

    void start() { engine.start(); }              // delegation
}
```

Why prefer it so often? Three reasons professionals reach for composition:

1. **Flexibility.** Swapping `Engine` for `ElectricEngine` needs no change
   to Car's structure — and Car never inherits Engine's baggage.
2. **No coupling to a single parent.** Inheritance locks you into one `extends`;
   composition composes many collaborators.
3. **Testability.** A Car built with an injected Engine can run with a fake
   engine in tests — Module 13 leans on exactly this.

**Delegation** is composition's verb: a method forwards the real work to a
field. The forwarding is not waste — it defines Car's public contract while
Engine stays swappable.

**The design heuristic, in one paragraph:** model what a thing IS with
inheritance (rare, stable hierarchies like Shape); model what a thing HAS
or USES with composition (most of the time: engines, repositories,
formatters, connections). Inheritance used without a true is-a makes
subclass behavior surprising; composition keeps every object small and
replaceable. When you finish this module you will have written both — and
felt composition win more often.

**AI angle:** generated code over-uses inheritance ("extend BaseService to
add a flag"). Treat that as a review trigger: ask "is this a genuine is-a?"
before accepting it.

**Next:** practice.
'''

L_COMPOSITION_VI = r'''
**Composition** nghĩa là xây hành vi phức tạp từ các object đơn giản hơn,
giữ chúng như trường — "has-a" thay vì "is-a".

```java
class Engine {
    void start() { System.out.println("vroom"); }
}

class Car {
    private final Engine engine = new Engine();   // Car HAS-AN Engine

    void start() { engine.start(); }              // ủy quyền
}
```

Vì sao ưu tiên nó phần lớn thời gian? Ba lý do dân chuyên chọn composition:

1. **Linh hoạt.** Đổi `Engine` thành `ElectricEngine` không cần sửa cấu trúc
   của Car — và Car không bao giờ thừa hưởng hành lý của Engine.
2. **Không bị trói vào một cha.** Kế thừa khóa bạn vào một `extends` duy nhất;
   composition ghép được nhiều cộng sự.
3. **Kiểm thử được.** Car dựng với Engine tiêm từ ngoài chạy được với engine
   giả trong test — Module 13 dựa hẳn vào điều này.

**Ủy quyền (delegation)** là động từ của composition: phương thức chuyển
công việc thật cho một trường. Phần chuyển tiếp không phải phí — nó định
nghĩa hợp đồng public của Car trong khi Engine vẫn có thể hoán đổi.

**Heuristic thiết kế, gói trong một đoạn:** mô hình hóa cái gì đó LÀ gì
bằng kế thừa (hiếm, hệ thống ổn định như Shape); mô hình hóa cái gì đó CÓ
hoặc DÙNG bằng composition (phần lớn thời gian: engine, repository,
formatter, kết nối). Kế thừa dùng thiếu is-a thật khiến hành vi subclass
đáng ngạc nhiên; composition giữ mọi object nhỏ và có thể thay thế. Khi
kết thúc module này bạn sẽ viết cả hai — và cảm nhận composition thắng
nhiều hơn.

**Góc nhìn AI:** code sinh ra hay lạm dụng kế thừa ("extend BaseService để
thêm một cờ"). Hãy coi đó là tín hiệu review: hỏi "đây có phải is-a thật?"
trước khi chấp nhận.

**Tiếp theo:** thực hành.
'''

# ── practice set 8 ──────────────────────────────────────────────────────────
P8_SHAPES = challenge(
    "javb-m8-shapes",
    "Polymorphic shapes",
    "Inside `Solution`, write `static abstract class Shape` with abstract "
    "`double area()` and `String name()`; plus `static class Circle extends "
    "Shape` (constructor takes radius), `static class Rect extends Shape` "
    "(width, height). Implement `static double totalArea(Shape[] shapes)` "
    "that works for ANY mix of shapes.",
    r'''public class Solution {
    public static abstract class Shape {
        public abstract double area();
        public abstract String name();
    }

    public static class Circle extends Shape {
        public Circle(double r) {
        }

        public double area() { return 0; }
        public String name() { return "circle"; }
    }

    public static class Rect extends Shape {
        public Rect(double w, double h) {
        }

        public double area() { return 0; }
        public String name() { return "rect"; }
    }

    public static double totalArea(Shape[] shapes) {
        return 0;
    }
}
''',
    [
        (
            "individual areas",
            r"""
Solution.Shape c = new Solution.Circle(1);
CjTestBase.checkNear(c.area(), Math.PI, 1e-9, "unit circle");
Solution.Shape r = new Solution.Rect(3, 4);
CjTestBase.checkNear(r.area(), 12.0, 1e-9, "3x4 rect");
""",
            "Each subclass computes its own formula.",
        ),
        (
            "polymorphic total",
            r"""
Solution.Shape[] mix = { new Solution.Circle(2), new Solution.Rect(2, 3), new Solution.Circle(1) };
CjTestBase.checkNear(Solution.totalArea(mix), Math.PI * 4 + 6 + Math.PI, 1e-9, "mixed shapes");
CjTestBase.checkNear(Solution.totalArea(new Solution.Shape[]{}), 0.0, 1e-9, "empty");
""",
            "totalArea must dispatch through the abstract method — no instanceof chains.",
        ),
    ],
    level="guided",
)

P8_SHAPES_VI = vi_challenge(
    "Các hình đa hình",
    "Bên trong `Solution`, viết `static abstract class Shape` với abstract "
    "`double area()` và `String name()`; cộng `static class Circle extends "
    "Shape` (constructor nhận bán kính), `static class Rect extends Shape` "
    "(rộng, cao). Viết `static double totalArea(Shape[] shapes)` chạy đúng "
    "với BẤT KỲ hỗn hợp hình nào.",
    [
        ("individual areas", "Mỗi subclass tự tính công thức của mình."),
        ("polymorphic total", "totalArea phải điều phối qua phương thức abstract — không dùng chuỗi instanceof."),
    ],
)

P8_NOTIFIER = challenge(
    "javb-m8-notifier",
    "Interface-driven notifications",
    "Inside `Solution`, write `interface Notifier { String send(String msg); }` "
    "plus two implementations: `static class EmailNotifier implements "
    "Notifier` returns `\"EMAIL: \" + msg`, and `static class SmsNotifier` "
    "returns `\"SMS: \" + msg`. Implement `static String broadcast(Notifier "
    "n, String msg)` that dispatches through the interface.",
    r'''public class Solution {
    public interface Notifier {
        String send(String msg);
    }

    public static class EmailNotifier implements Notifier {
        public String send(String msg) { return ""; }
    }

    public static class SmsNotifier implements Notifier {
        public String send(String msg) { return ""; }
    }

    public static String broadcast(Notifier n, String msg) {
        return "";
    }
}
''',
    [
        (
            "both channels",
            r"""
Solution.Notifier email = new Solution.EmailNotifier();
CjTestBase.checkEq(Solution.broadcast(email, "hi"), "EMAIL: hi", "email channel");
Solution.Notifier sms = new Solution.SmsNotifier();
CjTestBase.checkEq(Solution.broadcast(sms, "hi"), "SMS: hi", "sms channel");
""",
            "broadcast() sees only the Notifier interface.",
        ),
        (
            "unknown at compile time",
            r"""
Solution.Notifier custom = new Solution.Notifier() {
    public String send(String msg) { return "PING: " + msg; }
};
CjTestBase.checkEq(Solution.broadcast(custom, "yo"), "PING: yo", "anonymous implementation");
""",
            "A third implementation the broadcast() author never knew must work unchanged.",
        ),
    ],
    level="independent",
)

P8_NOTIFIER_VI = vi_challenge(
    "Thông báo điều hướng bằng interface",
    "Bên trong `Solution`, viết `interface Notifier { String send(String "
    "msg); }` cộng hai hiện thực: `static class EmailNotifier implements "
    "Notifier` trả `\"EMAIL: \" + msg`, và `static class SmsNotifier` trả "
    "`\"SMS: \" + msg`. Viết `static String broadcast(Notifier n, String "
    "msg)` điều phối qua interface.",
    [
        ("both channels", "broadcast() chỉ nhìn thấy interface Notifier."),
        ("unknown at compile time", "Một hiện thực thứ ba mà tác giả broadcast() chưa từng biết phải chạy không cần sửa."),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M8_MD = r'''
The Zoo: one abstract base, three species, and a census.

Inside `Solution`:

1. `static abstract class Animal` — `abstract String sound();` and a
   `public String toString()` override returning `sound()` (so printing
   shows the sound).
2. `static class Dog extends Animal` — sound `"woof"`.
3. `static class Cat extends Animal` — sound `"meow"`.
4. `static class Robot extends Animal` — sound `"beep"`, but Robot is NOT
   really an animal, so it must also `implements Describable` where
   `interface Describable { String kind(); }` returns `"machine"`.
5. `static int countRealAnimals(Animal[] zoo)` — the number of animals in
   the array that implement `Describable`... **is zero logic**: instead
   count the ones whose `sound()` is a real animal sound. Simpler and
   honest: count entries that are NOT instanceof `Describable` (that is
   exactly the interface check the lesson allows here).

So for `{ new Dog(), new Cat(), new Robot() }`, `countRealAnimals` returns 2.
The grader also checks polymorphism: every `sound()` must dispatch to the
object's own class.
'''

CK_M8_MD_VI = r'''
Vườn thú: một lớp cha abstract, ba loài, và một buổi kiểm kê.

Bên trong `Solution`:

1. `static abstract class Animal` — `abstract String sound();` và override
   `public String toString()` trả `sound()` (để in ra là tiếng kêu).
2. `static class Dog extends Animal` — tiếng `"woof"`.
3. `static class Cat extends Animal` — tiếng `"meow"`.
4. `static class Robot extends Animal` — tiếng `"beep"`, nhưng Robot KHÔNG
   phải động vật thật, nên nó phải `implements Describable` với
   `interface Describable { String kind(); }` trả `"machine"`.
5. `static int countRealAnimals(Animal[] zoo)` — số con trong mảng KHÔNG
   implement `Describable` (dùng `instanceof` — phép kiểm interface mà bài
   học cho phép ở đây).

Với `{ new Dog(), new Cat(), new Robot() }`, `countRealAnimals` trả 2.
Grader cũng kiểm đa hình: mọi `sound()` phải điều phối về class của object.
'''

CK_M8_CH = challenge(
    "javb-checkpoint-oop-design",
    "Checkpoint: The Zoo Census",
    CK_M8_MD,
    r'''public class Solution {
    public interface Describable {
        String kind();
    }

    public static abstract class Animal {
        public abstract String sound();
    }

    public static class Dog extends Animal {
        public String sound() { return ""; }
    }

    public static class Cat extends Animal {
        public String sound() { return ""; }
    }

    public static class Robot extends Animal implements Describable {
        public String sound() { return ""; }
        public String kind() { return ""; }
    }

    public static int countRealAnimals(Animal[] zoo) {
        return 0;
    }
}
''',
    [
        (
            "each species speaks",
            r"""
CjTestBase.checkEq(new Solution.Dog().sound(), "woof", "dog");
CjTestBase.checkEq(new Solution.Cat().sound(), "meow", "cat");
CjTestBase.checkEq(new Solution.Robot().sound(), "beep", "robot");
""",
            "Polymorphic dispatch through the abstract method.",
        ),
        (
            "robot is describable",
            r"""
CjTestBase.checkEq(new Solution.Robot().kind(), "machine", "robot kind");
""",
            "Robot carries the extra capability.",
        ),
        (
            "the census",
            r"""
Solution.Animal[] zoo = { new Solution.Dog(), new Solution.Cat(), new Solution.Robot() };
CjTestBase.checkEq(Solution.countRealAnimals(zoo), 2, "two real animals");
CjTestBase.checkEq(Solution.countRealAnimals(new Solution.Animal[]{}), 0, "empty zoo");
""",
            "Count entries that are NOT instanceof Describable.",
        ),
    ],
    difficulty="beginner",
)

CK_M8_VI = vi_challenge(
    "Checkpoint: Kiểm kê vườn thú",
    CK_M8_MD_VI,
    [
        ("each species speaks", "Điều phối đa hình qua phương thức abstract."),
        ("robot is describable", "Robot mang thêm năng lực Describable."),
        ("the census", "Đếm các phần tử KHÔNG phải instanceof Describable."),
    ],
)

CK_M8_R = r'''public class Solution {
    public interface Describable {
        String kind();
    }

    public static abstract class Animal {
        public abstract String sound();

        @Override
        public String toString() {
            return sound();
        }
    }

    public static class Dog extends Animal {
        @Override
        public String sound() { return "woof"; }
    }

    public static class Cat extends Animal {
        @Override
        public String sound() { return "meow"; }
    }

    public static class Robot extends Animal implements Describable {
        @Override
        public String sound() { return "beep"; }

        @Override
        public String kind() { return "machine"; }
    }

    public static int countRealAnimals(Animal[] zoo) {
        int real = 0;
        for (Animal a : zoo) {
            if (!(a instanceof Describable)) {
                real++;
            }
        }
        return real;
    }
}
'''

CK_M8_W = r'''public class Solution {
    public interface Describable {
        String kind();
    }

    public static abstract class Animal {
        public abstract String sound();

        @Override
        public String toString() {
            return sound();
        }
    }

    public static class Dog extends Animal {
        @Override
        public String sound() { return "woof"; }
    }

    public static class Cat extends Animal {
        @Override
        public String sound() { return "meow"; }
    }

    public static class Robot extends Animal implements Describable {
        @Override
        public String sound() { return "beep"; }

        @Override
        public String kind() { return "machine"; }
    }

    public static int countRealAnimals(Animal[] zoo) {
        // BUG: counts EVERYTHING, robots included
        return zoo.length;
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "OOP Design: Inheritance & Interfaces",
    "extends and super, overriding with @Override, interface contracts, polymorphic dispatch, and the composition heuristic.",
    "Thiết kế OOP: Kế thừa & Interface",
    "extends và super, override với @Override, hợp đồng interface, điều phối đa hình, và heuristic composition.",
    ["java-inheritance", "overriding-polymorphism", "interfaces", "composition", "java-checkpoint-oop-design"],
    ["javb-p8-design"],
)

write_lesson(
    MOD, "java-inheritance",
    "Inheritance & super",
    "Is-a relationships, the one-parent rule, protected access, and when composition beats inheritance.", 20,
    L_INHERIT_EN,
    "Kế thừa & super",
    "Quan hệ is-a, quy tắc một cha, truy cập protected, và khi nào composition thắng kế thừa.",
    L_INHERIT_VI,
)

write_lesson(
    MOD, "overriding-polymorphism",
    "Overriding & Polymorphism",
    "One call site, many behaviors; @Override as a compiler contract; super.method() composition.", 20,
    L_POLY_EN,
    "Overriding & Đa hình",
    "Một chỗ gọi, nhiều hành vi; @Override như hợp đồng với compiler; ghép với super.method().",
    L_POLY_VI,
)

write_lesson(
    MOD, "interfaces",
    "Interfaces: Contracts of Capability",
    "Implement many, promise methods, capability vs identity, and default methods as migration tools.", 20,
    L_INTERFACES_EN,
    "Interface: hợp đồng năng lực",
    "Implement nhiều, hứa phương thức, năng lực khác danh tính, và default method là công cụ di trú.",
    L_INTERFACES_VI,
)

write_lesson(
    MOD, "java-composition",
    "Composition & Delegation",
    "Has-a over is-a, forwarding as design, testability through injected collaborators.", 15,
    L_COMPOSITION_EN,
    "Composition & ủy quyền",
    "Has-a hơn is-a, chuyển tiếp như một quyết định thiết kế, kiểm thử được nhờ collaborator tiêm vào.",
    L_COMPOSITION_VI,
)

write_practice(
    MOD, "javb-p8-design",
    "Practice: Designing with Polymorphism",
    "Abstract shapes totalling polymorphically, and an interface-driven notifier a stranger can extend.",
    "Thực hành: Thiết kế với đa hình",
    "Các hình abstract tính tổng đa hình, và bộ thông báo theo interface mà người lạ có thể mở rộng.",
    "overriding-polymorphism", 50, "beginner",
    [P8_SHAPES, P8_NOTIFIER],
    {c["id"]: v for c, v in [(P8_SHAPES, P8_SHAPES_VI), (P8_NOTIFIER, P8_NOTIFIER_VI)]},
    solutions=[
        (
            P8_SHAPES["id"],
            r'''public class Solution {
    public static abstract class Shape {
        public abstract double area();
        public abstract String name();
    }

    public static class Circle extends Shape {
        private final double r;
        public Circle(double r) { this.r = r; }
        public double area() { return Math.PI * r * r; }
        public String name() { return "circle"; }
    }

    public static class Rect extends Shape {
        private final double w, h;
        public Rect(double w, double h) { this.w = w; this.h = h; }
        public double area() { return w * h; }
        public String name() { return "rect"; }
    }

    public static double totalArea(Shape[] shapes) {
        double total = 0;
        for (Shape s : shapes) {
            total += s.area();
        }
        return total;
    }
}
''',
            r'''public class Solution {
    public static abstract class Shape {
        public abstract double area();
        public abstract String name();
    }

    public static class Circle extends Shape {
        private final double r;
        public Circle(double r) { this.r = r; }
        public double area() { return Math.PI * r * r; }
        public String name() { return "circle"; }
    }

    public static class Rect extends Shape {
        private final double w, h;
        public Rect(double w, double h) { this.w = w; this.h = h; }
        public double area() { return w * h; }
        public String name() { return "rect"; }
    }

    public static double totalArea(Shape[] shapes) {
        double total = 0;
        for (Shape s : shapes) {
            // BUG: counts circles twice — a Shape leak into instanceof logic
            if (s instanceof Circle) {
                total += s.area() * 2;
            } else {
                total += s.area();
            }
        }
        return total;
    }
}
''',
        ),
        (
            P8_NOTIFIER["id"],
            r'''public class Solution {
    public interface Notifier {
        String send(String msg);
    }

    public static class EmailNotifier implements Notifier {
        public String send(String msg) { return "EMAIL: " + msg; }
    }

    public static class SmsNotifier implements Notifier {
        public String send(String msg) { return "SMS: " + msg; }
    }

    public static String broadcast(Notifier n, String msg) {
        return n.send(msg);
    }
}
''',
            r'''public class Solution {
    public interface Notifier {
        String send(String msg);
    }

    public static class EmailNotifier implements Notifier {
        public String send(String msg) { return "EMAIL: " + msg; }
    }

    public static class SmsNotifier implements Notifier {
        public String send(String msg) { return "SMS: " + msg; }
    }

    public static String broadcast(Notifier n, String msg) {
        // BUG: forces every notifier through the email class — interface bypassed
        return new EmailNotifier().send(msg);
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-oop-design",
    "Checkpoint: The Zoo Census",
    "An abstract base, an extra interface capability, and an instanceof census — identity and capability side by side.", 45, CK_M8_MD,
    "Checkpoint: Kiểm kê vườn thú",
    "Một lớp cha abstract, một năng lực interface thêm vào, và phép kiểm kê instanceof — danh tính và năng lực đặt cạnh nhau.",
    CK_M8_MD_VI,
    CK_M8_CH, CK_M8_VI,
    solution=CK_M8_R, wrong=CK_M8_W,
)

print("module 8 complete")
