#!/usr/bin/env python3
"""Java — Beginner — Module 7: java-classes-objects.

NOTE on the graded contract: multi-class snippets are impossible (one public
class per generated test file), so OOP challenges grade a single `Solution`
class with nested static helper types, e.g. `Solution.Account`. Learners see
nested classes in the lesson text before meeting them in challenges.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-classes-objects"

L_CLASSES_EN = r'''
A **class** is a blueprint; an **object** is one concrete thing built from
it. The class says what data (**fields**) and behavior (**methods**) every
object of that kind has:

```java
class Dog {
    String name;
    int age;

    void bark() {
        System.out.println(name + " says woof");
    }
}

Dog a = new Dog();     // object 1
a.name = "Rex";
a.age = 3;
a.bark();              // Rex says woof

Dog b = new Dog();     // object 2: own name, own age, SAME behavior
b.name = "Lucky";
b.bark();              // Lucky says woof
```

`new Dog()` allocates a fresh object with its own copy of every field. The
dot accesses what the object owns: `a.name` is object a's name. Two objects
are independent — renaming Rex never touches Lucky.

**State + behavior in one place** is the point of classes. `bark()` uses
`name` *without a parameter*, because it automatically operates on the
object it was called on. Inside a method, `this` names that object: `this.name`
is "the name field of the object I was called on". When a parameter shadows
a field, `this` disambiguates:

```java
void rename(String name) {
    this.name = name;   // field = parameter
}
```

**Object references.** `Dog d2 = a;` does NOT copy the dog — it copies the
*reference* (the arrow pointing at the object). Now `a` and `d2` are two
names for one object; changing fields through either is visible through
both. This is the object half of Module 5's "parameters are copies": the
copy is of the arrow, not the dog.

**Next:** constructors — controlling how objects are born.
'''

L_CLASSES_VI = r'''
**Class** là bản thiết kế; **object** là một vật cụ thể được dựng từ nó.
Class nói rõ dữ liệu (**trường**) và hành vi (**phương thức**) mà mọi object
thuộc loại đó có:

```java
class Dog {
    String name;
    int age;

    void bark() {
        System.out.println(name + " says woof");
    }
}

Dog a = new Dog();     // object 1
a.name = "Rex";
a.age = 3;
a.bark();              // Rex says woof

Dog b = new Dog();     // object 2: tên riêng, tuổi riêng, hành vi CHUNG
b.name = "Lucky";
b.bark();              // Lucky says woof
```

`new Dog()` cấp phát một object mới với bản sao riêng của mọi trường. Dấu
chấm truy cập những gì object sở hữu: `a.name` là tên của object a. Hai
object độc lập với nhau — đổi tên Rex không bao giờ chạm tới Lucky.

**Trạng thái + hành vi ở một chỗ** là điểm cốt lõi của class. `bark()` dùng
`name` mà *không cần tham số*, vì nó tự động tác động lên object được gọi
đến. Bên trong một phương thức, `this` là tên của object đó: `this.name`
nghĩa là "trường name của object tôi được gọi trên đó". Khi tham số che
bóng trường, `this` phân biệt:

```java
void rename(String name) {
    this.name = name;   // trường = tham số
}
```

**Tham chiếu object.** `Dog d2 = a;` KHÔNG sao chép con chó — nó sao chép
*tham chiếu* (mũi tên trỏ vào object). Từ đó `a` và `d2` là hai tên của một
object; đổi trường qua cái nào cũng thấy qua cái kia. Đây là nửa object của
câu "tham số là bản sao" ở Module 5: bản sao là của mũi tên, không phải con chó.

**Tiếp theo:** constructor — kiểm soát cách object được sinh ra.
'''

L_CTORS_EN = r'''
A **constructor** is a special method that runs at `new` time, shaping every
object of the class as it is born:

```java
class Account {
    String owner;
    double balance;

    Account(String owner, double balance) {   // same name as class, no return type
        this.owner = owner;
        this.balance = balance;
    }
}

Account acc = new Account("Ada", 100.0);   // fields set at birth
```

Three constructor rules:

- The name matches the class **exactly**, and there is no return type — not
  even `void`.
- If you write **no constructor at all**, Java writes you a silent,
  do-nothing default (fields get `0`/`false`/`null`).
- If you write ANY constructor, the free default disappears: `new Account()`
  stops compiling unless you also write it.

**Overloading constructors** gives callers convenience; the classic pattern
chains with `this(...)` so the real logic lives in exactly one place:

```java
Account(String owner) {
    this(owner, 0.0);        // delegate: everyone starts at zero
}

Account(String owner, double balance) {
    if (balance < 0) {
        throw new IllegalArgumentException("balance must be >= 0");
    }
    this.owner = owner;
    this.balance = balance;
}
```

Constructors are also the natural place to **validate**: refuse bad births
(`null` owner, negative balance) immediately, so the rest of the class can
assume its invariants hold. This "validate at the door" habit is the
beginner form of what professionals call an *invariant* — a guarantee every
object keeps for its whole life.

**Next:** guarding fields — encapsulation.
'''

L_CTORS_VI = r'''
**Constructor** là một phương thức đặc biệt chạy tại thời điểm `new`, định
hình mọi object của class ngay khi sinh ra:

```java
class Account {
    String owner;
    double balance;

    Account(String owner, double balance) {   // trùng tên class, không có kiểu trả về
        this.owner = owner;
        this.balance = balance;
    }
}

Account acc = new Account("Ada", 100.0);   // trường được đặt ngay khi sinh
```

Ba quy tắc của constructor:

- Tên trùng với tên class **tuyệt đối**, và không có kiểu trả về — kể cả `void`.
- Nếu bạn KHÔNG viết constructor nào, Java lặng lẽ viết cho bạn một mặc định
  không làm gì (các trường nhận `0`/`false`/`null`).
- Nếu bạn viết BẤT KỲ constructor nào, bản mặc định miễn phí biến mất:
  `new Account()` ngừng biên dịch trừ khi bạn tự viết nó.

**Overload constructor** tạo sự tiện lợi cho người gọi; pattern kinh điển
là nối chuỗi bằng `this(...)` để logic thật nằm đúng một chỗ:

```java
Account(String owner) {
    this(owner, 0.0);        // ủy quyền: ai cũng bắt đầu từ số 0
}

Account(String owner, double balance) {
    if (balance < 0) {
        throw new IllegalArgumentException("balance must be >= 0");
    }
    this.owner = owner;
    this.balance = balance;
}
```

Constructor cũng là nơi tự nhiên để **xác thực**: từ chối ngay những ca sinh
xấu (owner `null`, số dư âm), để phần còn lại của class được phép giả định
các bất biến của nó luôn đúng. Thói quen "xác thực ở cửa" này là dạng người
mới của thứ dân chuyên gọi là *bất biến* — một lời cam kết mọi object giữ
trọn đời nó.

**Tiếp theo:** canh gác các trường — đóng gói.
'''

L_ENCAP_EN = r'''
**Encapsulation** = fields private, behavior public. Mark fields `private`
so nobody outside the class can touch them directly, and expose *methods*
that guard the access:

```java
public class Account {
    private String owner;
    private double balance;      // hidden: no acc.balance from outside

    public Account(String owner, double balance) {
        this.owner = owner;
        this.balance = Math.max(0, balance);
    }

    public double getBalance() {          // read is safe: just a report
        return balance;
    }

    public void deposit(double amount) {  // write is guarded: a rule lives here
        if (amount <= 0) {
            throw new IllegalArgumentException("deposit must be positive");
        }
        balance += amount;
    }
}
```

Why hide the field when a public one is shorter? Because **the field is the
past of the class; the methods are its future**. With `balance` private you
can later add logging, switch storage to cents, or add a transaction limit —
and every rule has exactly one home. With it public, every caller bypasses
every rule and you can never change anything.

**Getters and setters** are not the goal — *control* is. A getter that just
returns the field is a harmless convenience; a `setBalance(double)` that
accepts anything is encapsulation theater. Prefer **verbs** that describe
the real operations: `deposit`, `withdraw`, `transfer` — not
`setBalance`. The Account above has no setter at all, and that is good
design, not an omission.

`private` and `public` are **access modifiers**: `private` = this class
only; `public` = everyone. (Two more, `protected` and package-private,
arrive with inheritance and packages later.) The default habit:
fields `private`, the few doors the world needs `public`.

**Next:** composition — objects holding objects.
'''

L_ENCAP_VI = r'''
**Đóng gói (encapsulation)** = trường private, hành vi public. Đánh dấu
trường là `private` để không ai bên ngoài chạm vào trực tiếp, và mở các
*phương thức* canh gác lối vào:

```java
public class Account {
    private String owner;
    private double balance;      // ẩn: không có acc.balance từ bên ngoài

    public Account(String owner, double balance) {
        this.owner = owner;
        this.balance = Math.max(0, balance);
    }

    public double getBalance() {          // đọc an toàn: chỉ là báo cáo
        return balance;
    }

    public void deposit(double amount) {  // ghi được canh gác: một quy tắc ở đây
        if (amount <= 0) {
            throw new IllegalArgumentException("deposit must be positive");
        }
        balance += amount;
    }
}
```

Vì sao phải ẩn trường khi để public ngắn gọn hơn? Vì **trường là quá khứ
của class; phương thức là tương lai của nó**. Với `balance` private, sau này
bạn thêm log, đổi sang lưu bằng xu, hoặc thêm hạn mức giao dịch — và mọi
quy tắc có đúng một ngôi nhà. Để public, mọi người gọi bỏ qua mọi quy tắc
và bạn không bao giờ đổi được gì.

**Getter/setter** không phải mục tiêu — *quyền kiểm soát* mới là. Getter
chỉ trả về trường là tiện lợi vô hại; `setBalance(double)` chấp nhận mọi
thứ là đóng kịch đóng gói. Hãy ưu tiên **động từ** mô tả thao tác thật:
`deposit`, `withdraw`, `transfer` — không phải `setBalance`. Account trên
không có setter nào cả, và đó là thiết kế tốt, không phải bỏ sót.

`private` và `public` là **access modifier**: `private` = chỉ class này;
`public` = mọi người. (Hai cái nữa, `protected` và package-private, sẽ tới
cùng kế thừa và package sau này.) Thói quen mặc định: trường `private`,
vài cánh cửa thế giới cần thì `public`.

**Tiếp theo:** composition — object chứa object.
'''

L_STATIC_OOP_EN = r'''
Module 5 met `static` on methods; inside a class it completes the picture.

**Constants** are the friendliest static members — shared, immutable values
every instance can consult:

```java
public class Temperature {
    static final double ABSOLUTE_ZERO_C = -273.15;

    static boolean isPhysicallyPossible(double celsius) {
        return celsius >= ABSOLUTE_ZERO_C;
    }
}
```

**Shared state** is the dangerous half. One `static int instanceCount`
incremented in the constructor counts *all* Temperature objects ever made —
shared by every instance, and by every caller. It can be exactly right
(counting) or a disaster (a shared `balance`), and the difference is whether
the value describes the *class* or an *individual thing*. When in doubt, it
belongs to the thing: keep it non-static.

**`this` in context.** Within any instance method or constructor, `this` is
the current object. Two uses you will see constantly: disambiguating
`this.field = param;` and constructor chaining `this(...)`. A third arrives
in Module 8: passing `this` to another object ("call me back").

**Utility classes** — classes that exist only to hold static methods
(`Math` is one) — get one more convention: mark them un-instantiable by
giving them a private constructor:

```java
public final class Money {
    private Money() { }      // nobody can create a Money "object"

    static String format(double amount) { ... }
}
```

The private constructor is a small idiom with a big message: this class is
a namespace, not a thing.

**Next:** composition and the design principle that beats inheritance most of the time.
'''

L_STATIC_OOP_VI = r'''
Module 5 gặp `static` trên phương thức; trong class, nó hoàn thành bức tranh.

**Hằng số** là thành viên static thân thiện nhất — giá trị dùng chung, bất
biến, mọi instance đều tra cứu được:

```java
public class Temperature {
    static final double ABSOLUTE_ZERO_C = -273.15;

    static boolean isPhysicallyPossible(double celsius) {
        return celsius >= ABSOLUTE_ZERO_C;
    }
}
```

**Trạng thái dùng chung** là nửa nguy hiểm. Một `static int instanceCount`
được tăng trong constructor đếm *mọi* Temperature từng được tạo — dùng chung
cho mọi instance, và mọi người gọi. Nó có thể đúng hoàn toàn (đếm) hoặc là
thảm họa (một `balance` dùng chung), và ranh giới là: giá trị đó mô tả
*class* hay *một vật cụ thể*. Không chắc thì nó thuộc về vật: đừng để static.

**`this` trong ngữ cảnh.** Trong bất kỳ phương thức hay constructor dạng
object nào, `this` là object hiện tại. Hai cách dùng bạn sẽ gặp liên tục:
phân biệt `this.field = param;` và nối chuỗi constructor `this(...)`. Cách
thứ ba sẽ tới ở Module 8: truyền `this` cho object khác ("gọi lại tôi").

**Utility class** — class chỉ tồn tại để chứa phương thức static (`Math` là
một ví dụ) — có thêm một quy ước: làm cho nó không thể tạo instance bằng
constructor private:

```java
public final class Money {
    private Money() { }      // không ai tạo được "object" Money

    static String format(double amount) { ... }
}
```

Constructor private là một thành ngữ nhỏ với thông điệp lớn: class này là
một không gian tên, không phải một vật.

**Tiếp theo:** composition và nguyên tắc thiết kế thắng kế thừa trong đa
số trường hợp.
'''

# ── practice set 7 ──────────────────────────────────────────────────────────
P7_COUNTER = challenge(
    "javb-m7-class-counter",
    "A class that counts instances",
    "Inside `Solution`, write a nested `static class Widget` with a private "
    "`final String name`, a constructor that stores it, a getter, and a "
    "`static int count` that tracks how many Widgets have been created. "
    "`Solution.Widget.of(\"a\")` style calls are not needed — the grader "
    "creates `new Solution.Widget(\"a\")` directly and reads "
    "`Solution.Widget.getCount()`.",
    r'''public class Solution {
    public static class Widget {
        // name field, constructor, getName(), static count + getCount()
        public Widget(String name) {
        }
    }

    public static int getCount() {
        return Widget.count;
    }
}
''',
    [
        (
            "count grows with creation",
            r"""
int before = Solution.getCount();
new Solution.Widget("a");
new Solution.Widget("b");
CjTestBase.checkEq(Solution.getCount(), before + 2, "two more widgets");
""",
            "The constructor must increment the static counter.",
        ),
        (
            "name is stored and readable",
            r"""
Solution.Widget w = new Solution.Widget("gear");
CjTestBase.checkEq(w.getName(), "gear", "getter returns the name");
""",
            "getName() returns the field set at birth.",
        ),
    ],
    level="guided",
)

P7_COUNTER_VI = vi_challenge(
    "Class đếm instance",
    "Bên trong `Solution`, viết một `static class Widget` lồng nhau với "
    "`final String name` private, constructor lưu nó, một getter, và "
    "`static int count` theo dõi đã tạo bao nhiêu Widget. Grader tạo "
    "`new Solution.Widget(\"a\")` trực tiếp và đọc `Solution.Widget.getCount()`.",
    [
        ("count grows with creation", "Constructor phải tăng bộ đếm static."),
        ("name is stored and readable", "getName() trả về trường được đặt lúc sinh."),
    ],
)

P7_ACCOUNT = challenge(
    "javb-m7-bank-account",
    "Bank Account with guarded money",
    "Inside `Solution`, write `static class Account` with a `private final "
    "String owner`, `private double balance`, constructor `Account(String "
    "owner, double startingBalance)` (negative start → "
    "IllegalArgumentException), `public void deposit(double)` (must be "
    "positive, else IAE), `public void withdraw(double)` (must be positive "
    "AND not exceed balance, else IAE), and `public double getBalance()`.",
    r'''public class Solution {
    public static class Account {
        public Account(String owner, double startingBalance) {
        }

        public void deposit(double amount) {
        }

        public void withdraw(double amount) {
        }

        public double getBalance() {
            return 0;
        }
    }
}
''',
    [
        (
            "happy path",
            r"""
Solution.Account acc = new Solution.Account("Ada", 100);
acc.deposit(50);
acc.withdraw(30);
CjTestBase.checkNear(acc.getBalance(), 120.0, 1e-9, "100 + 50 - 30");
""",
            "Deposit adds, withdraw subtracts, getter reports.",
        ),
        (
            "rules are enforced",
            r"""
Solution.Account acc = new Solution.Account("Ada", 100);
CjTestBase.checkThrows(() -> acc.deposit(-5), "negative deposit");
CjTestBase.checkThrows(() -> acc.withdraw(1e9), "overdraft");
CjTestBase.checkThrows(() -> new Solution.Account("Bo", -1), "negative start");
""",
            "All three violations must throw IllegalArgumentException.",
        ),
    ],
    level="independent",
)

P7_ACCOUNT_VI = vi_challenge(
    "Tài khoản ngân hàng có canh gác",
    "Bên trong `Solution`, viết `static class Account` với `private final "
    "String owner`, `private double balance`, constructor `Account(String "
    "owner, double startingBalance)` (số dư đầu âm → IllegalArgumentException), "
    "`public void deposit(double)` (phải dương, không thì IAE), `public void "
    "withdraw(double)` (phải dương VÀ không vượt số dư, không thì IAE), và "
    "`public double getBalance()`.",
    [
        ("happy path", "Deposit cộng, withdraw trừ, getter báo cáo."),
        ("rules are enforced", "Cả ba vi phạm phải ném IllegalArgumentException."),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M7_MD = r'''
The Point class — a coordinate with rules.

Inside `Solution`, write `static class Point` with:

1. `private final int x; private final int y;` — an **immutable** point.
2. A constructor taking `(int x, int y)`.
3. Getters `getX()`, `getY()`.
4. `public Point translate(int dx, int dy)` — returns a NEW Point moved by
   the delta (the original must be untouched — immutability!).
5. `public double distanceTo(Point other)` — Euclidean distance
   (`Math.hypot(dx, dy)` is fine).
6. `static Point origin()` — a factory returning `new Point(0, 0)`.
7. `public boolean equalsPoint(Point other)` — same x AND same y. (The
   real `equals`/`hashCode` contract arrives in Module 9; this method-side
   version keeps the focus on fields.)

Immutability is the heart of this checkpoint: after
`Point p2 = p1.translate(5, 0);`, `p1` must still have its original
coordinates, and `p2` must be a different object with the new ones.
'''

CK_M7_MD_VI = r'''
Class Point — một tọa độ có quy tắc.

Bên trong `Solution`, viết `static class Point` với:

1. `private final int x; private final int y;` — một điểm **bất biến**.
2. Constructor nhận `(int x, int y)`.
3. Getter `getX()`, `getY()`.
4. `public Point translate(int dx, int dy)` — trả một Point MỚI di chuyển
   theo delta (bản gốc phải nguyên vẹn — tính bất biến!).
5. `public double distanceTo(Point other)` — khoảng cách Euclid
   (`Math.hypot(dx, dy)` là hợp lệ).
6. `static Point origin()` — một factory trả `new Point(0, 0)`.
7. `public boolean equalsPoint(Point other)` — cùng x VÀ cùng y. (Hợp đồng
   `equals`/`hashCode` thật sẽ tới ở Module 9; phiên bản phương thức này
   giữ trọng tâm vào các trường.)

Tính bất biến là trái tim của checkpoint này: sau
`Point p2 = p1.translate(5, 0);`, `p1` vẫn giữ tọa độ gốc, và `p2` phải là
object khác với tọa độ mới.
'''

CK_M7_CH = challenge(
    "javb-checkpoint-oop",
    "Checkpoint: The Point Class",
    CK_M7_MD,
    r'''public class Solution {
    public static class Point {
        public Point(int x, int y) {
        }

        public int getX() { return 0; }
        public int getY() { return 0; }

        public Point translate(int dx, int dy) {
            return this;
        }

        public double distanceTo(Point other) {
            return 0;
        }

        public boolean equalsPoint(Point other) {
            return false;
        }
    }

    public static Point origin() {
        return null;
    }
}
''',
    [
        (
            "construction and getters",
            r"""
Solution.Point p = new Solution.Point(3, 4);
CjTestBase.checkEq(p.getX(), 3, "x");
CjTestBase.checkEq(p.getY(), 4, "y");
Solution.Point o = Solution.origin();
CjTestBase.checkEq(o.getX(), 0, "origin x");
""",
            "Constructor stores both coordinates; origin() is (0,0).",
        ),
        (
            "translate returns a NEW point",
            r"""
Solution.Point p1 = new Solution.Point(2, 2);
Solution.Point p2 = p1.translate(5, -1);
CjTestBase.checkEq(p2.getX(), 7, "moved x");
CjTestBase.checkEq(p2.getY(), 1, "moved y");
CjTestBase.checkEq(p1.getX(), 2, "original x untouched");
CjTestBase.checkEq(p1.getY(), 2, "original y untouched");
""",
            "The original must keep its own coordinates — return a new Point.",
        ),
        (
            "distance and equality",
            r"""
Solution.Point a = new Solution.Point(0, 0);
Solution.Point b = new Solution.Point(3, 4);
CjTestBase.checkNear(a.distanceTo(b), 5.0, 1e-9, "3-4-5 triangle");
CjTestBase.checkTrue(new Solution.Point(1, 2).equalsPoint(new Solution.Point(1, 2)), "same point");
CjTestBase.checkTrue(!new Solution.Point(1, 2).equalsPoint(new Solution.Point(2, 1)), "different point");
""",
            "Distance is Euclidean; equality needs both coordinates.",
        ),
    ],
    difficulty="beginner",
)

CK_M7_VI = vi_challenge(
    "Checkpoint: Class Point",
    CK_M7_MD_VI,
    [
        ("construction and getters", "Constructor lưu cả hai tọa độ; origin() là (0,0)."),
        ("translate returns a NEW point", "Bản gốc phải giữ tọa độ riêng — trả một Point mới."),
        ("distance and equality", "Khoảng cách là Euclid; đẳng thức cần cả hai tọa độ."),
    ],
)

CK_M7_R = r'''public class Solution {
    public static class Point {
        private final int x;
        private final int y;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public int getX() { return x; }
        public int getY() { return y; }

        public Point translate(int dx, int dy) {
            return new Point(x + dx, y + dy);
        }

        public double distanceTo(Point other) {
            int dx = this.x - other.x;
            int dy = this.y - other.y;
            return Math.sqrt((double) dx * dx + (double) dy * dy);
        }

        public boolean equalsPoint(Point other) {
            return other != null && this.x == other.x && this.y == other.y;
        }
    }

    public static Point origin() {
        return new Point(0, 0);
    }
}
'''

CK_M7_W = r'''public class Solution {
    public static class Point {
        // BUG: fields are NOT final, and translate MUTATES this point
        private int x;
        private int y;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public int getX() { return x; }
        public int getY() { return y; }

        public Point translate(int dx, int dy) {
            this.x = this.x + dx;
            this.y = this.y + dy;
            return this;   // returns the SAME, now-mutated object
        }

        public double distanceTo(Point other) {
            int dx = this.x - other.x;
            int dy = this.y - other.y;
            return Math.sqrt((double) dx * dx + (double) dy * dy);
        }

        public boolean equalsPoint(Point other) {
            return other != null && this.x == other.x && this.y == other.y;
        }
    }

    public static Point origin() {
        return new Point(0, 0);
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Classes & Objects",
    "Blueprints and instances, constructors that validate, encapsulation with intent, this, and class-level members.",
    "Class & Object",
    "Bản thiết kế và thực thể, constructor có xác thực, đóng gói có chủ đích, this, và thành viên cấp class.",
    ["classes-objects-refs", "constructors", "encapsulation", "static-in-classes", "java-checkpoint-oop"],
    ["javb-p7-objects"],
)

write_lesson(
    MOD, "classes-objects-refs",
    "Classes, Objects & References",
    "Blueprint vs instance, fields and behavior, this, and reference-vs-object copying.", 20,
    L_CLASSES_EN,
    "Class, Object & tham chiếu",
    "Bản thiết kế vs thực thể, trường và hành vi, this, và sao chép tham chiếu khác sao chép object.",
    L_CLASSES_VI,
)

write_lesson(
    MOD, "java-constructors",
    "Constructors & Object Birth",
    "Constructor rules, overloading with this(...), and validating at the door.", 15,
    L_CTORS_EN,
    "Constructor & ca sinh object",
    "Quy tắc constructor, overload với this(...), và xác thực ngay ở cửa.",
    L_CTORS_VI,
)

write_lesson(
    MOD, "encapsulation",
    "Encapsulation & Access Modifiers",
    "Private fields, guarded verbs, why setters are not the goal, and the two modifiers that matter now.", 20,
    L_ENCAP_EN,
    "Đóng gói & access modifier",
    "Trường private, động từ có canh gác, vì sao setter không phải mục tiêu, và hai modifier quan trọng lúc này.",
    L_ENCAP_VI,
)

write_lesson(
    MOD, "static-in-classes",
    "static Members & Utility Classes",
    "Constants, the shared-state trap, this in context, and the private-constructor utility idiom.", 15,
    L_STATIC_OOP_EN,
    "Thành viên static & utility class",
    "Hằng số, bẫy trạng thái dùng chung, this trong ngữ cảnh, và thành ngữ utility class với constructor private.",
    L_STATIC_OOP_VI,
)

write_practice(
    MOD, "javb-p7-objects",
    "Practice: Objects at Work",
    "A counting class and a guarded bank account — state, rules, and constructors under test.",
    "Thực hành: Object tại chỗ làm",
    "Một class đếm và một tài khoản ngân hàng có canh gác — trạng thái, quy tắc, và constructor dưới kiểm thử.",
    "java-constructors", 45, "beginner",
    [P7_COUNTER, P7_ACCOUNT],
    {c["id"]: v for c, v in [(P7_COUNTER, P7_COUNTER_VI), (P7_ACCOUNT, P7_ACCOUNT_VI)]},
    solutions=[
        (
            P7_COUNTER["id"],
            r'''public class Solution {
    public static class Widget {
        private static int count = 0;
        private final String name;

        public Widget(String name) {
            this.name = name;
            count++;
        }

        public String getName() {
            return name;
        }
    }

    public static int getCount() {
        return Widget.count;
    }
}
''',
            r'''public class Solution {
    public static class Widget {
        private static int count = 0;
        private final String name;

        public Widget(String name) {
            this.name = name;
            // BUG: forgets to count
        }

        public String getName() {
            return name;
        }
    }

    public static int getCount() {
        return Widget.count;
    }
}
''',
        ),
        (
            P7_ACCOUNT["id"],
            r'''public class Solution {
    public static class Account {
        private final String owner;
        private double balance;

        public Account(String owner, double startingBalance) {
            if (startingBalance < 0) {
                throw new IllegalArgumentException("balance must be >= 0");
            }
            this.owner = owner;
            this.balance = startingBalance;
        }

        public void deposit(double amount) {
            if (amount <= 0) {
                throw new IllegalArgumentException("deposit must be positive");
            }
            balance += amount;
        }

        public void withdraw(double amount) {
            if (amount <= 0 || amount > balance) {
                throw new IllegalArgumentException("invalid withdrawal");
            }
            balance -= amount;
        }

        public double getBalance() {
            return balance;
        }
    }
}
''',
            r'''public class Solution {
    public static class Account {
        private final String owner;
        private double balance;

        public Account(String owner, double startingBalance) {
            if (startingBalance < 0) {
                throw new IllegalArgumentException("balance must be >= 0");
            }
            this.owner = owner;
            this.balance = startingBalance;
        }

        public void deposit(double amount) {
            if (amount <= 0) {
                throw new IllegalArgumentException("deposit must be positive");
            }
            balance += amount;
        }

        public void withdraw(double amount) {
            // BUG: skips the overdraft check
            if (amount <= 0) {
                throw new IllegalArgumentException("invalid withdrawal");
            }
            balance -= amount;
        }

        public double getBalance() {
            return balance;
        }
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-oop",
    "Checkpoint: The Point Class",
    "An immutable coordinate type: final fields, factory method, translating without mutation, and geometric equality.", 45, CK_M7_MD,
    "Checkpoint: Class Point",
    "Một kiểu tọa độ bất biến: trường final, factory method, dịch chuyển không đột biến, và đẳng thức hình học.",
    CK_M7_MD_VI,
    CK_M7_CH, CK_M7_VI,
    solution=CK_M7_R, wrong=CK_M7_W,
)

print("module 7 complete")
