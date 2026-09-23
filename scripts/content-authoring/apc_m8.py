#!/usr/bin/env python3
"""AP CSA M8 — Classes and Objects (fields, constructors, this, encapsulation)."""
from apc import *

M = "apc-classes"

L1 = r"""
A **class** is a blueprint; an **object** is a thing built from it. The
blueprint declares **fields** (what it knows) and **methods** (what it does):

```java
public class Book {
    private String title;
    private int pages;

    public Book(String t, int p) {     // constructor
        title = t;
        pages = p;
    }

    public String getTitle() {         // accessor (getter)
        return title;
    }

    public boolean isLong() {          // behavior
        return pages > 300;
    }
}
```

`new Book("Dune", 412)` builds one object: allocates it, runs the
constructor, returns a **reference** to it. Store the reference in a
variable:

```java
Book b = new Book("Dune", 412);
b.getTitle()      // "Dune"
b.isLong()        // true
```

The dot reaches *into* the object: `b.title` would work in the same class,
but from outside, `title` is `private` — unreachable. That is
**encapsulation**: state is private, access goes through methods.

`this` names the current object. When a parameter shadows a field, `this.`
disambiguates: `this.title = title;`
"""

L2 = r"""
A **constructor** initializes a new object. Rules the exam tests:

- Same name as the class, **no return type** (not even void).
- If you write **no** constructor, Java silently provides a no-argument
  default (all fields zero/false/null) — but only then. Write any
  constructor and the default disappears.

```java
public class Counter {
    private int count;

    public Counter() {           // no-arg: start at 0
        count = 0;
    }

    public Counter(int start) {  // overloaded: start elsewhere
        count = start;
    }
}
```

Two constructors with different parameter lists = **overloading**. The call
`new Counter(5)` picks the matching one.

**Multiple references, one object** — aliasing:

```java
Counter a = new Counter();
Counter b = a;          // b refers to the SAME object; no copy
```

Now `a` and `b` are two names for one counter. Compare with primitives,
where `int b = a` really copies. And the null reference: an object variable
can hold `null` ("no object") — calling a method on it crashes with a
`NullPointerException`.
"""

L3 = r"""
FRQ **Question 2 (Class Design)** hands you a table like:

| Expression | Result |
| --- | --- |
| `new Sensor(20)` | a sensor starting at 20 |
| `s.read()` | current value |
| `s.tick()` | value grows by 1, nothing returned |

...and asks you to write the whole class. The checklist every answer needs:

1. `public class Name {` header.
2. `private` instance variables — every one the table implies.
3. A constructor matching the table's construction row.
4. The required methods, with exact names/signatures.

Worked answer for the table above:

```java
public class Sensor {
    private int value;

    public Sensor(int start) {
        value = start;
    }

    public int read() {
        return value;
    }

    public void tick() {
        value++;
    }
}
```

Scoring rubric details: exact method names and parameter types are worth
points; state changes must actually happen (`value++` inside tick), and
methods the table shows returning nothing are declared `void`.

**Decomposition inside classes**: a method may call another method of the
same object directly — `isLong()` could call `getPages()` without a dot.
"""

write_module(
    M,
    "Classes and Objects",
    "Fields, constructors, accessors, private state, this, aliasing vs copying, and the FRQ Class-Design checklist.",
    "Lớp và đối tượng",
    "Trường dữ liệu, constructor, accessor, trạng thái private, this, tham chiếu chung so với sao chép, và danh mục kiểm tra FRQ Thiết kế Lớp.",
    lessons=["apc-m8-blueprint", "apc-m8-ctors", "apc-m8-frq", "apc-cp-m8"],
    practices=["apc-p8-classes"],
)

write_lesson(
    M, "apc-m8-blueprint", "Blueprint and objects",
    "Fields, methods, new, references, dot notation, private state.",
    14, L1,
    "Bản thiết kế và đối tượng",
    "Trường dữ liệu, phương thức, new, tham chiếu, dấu chấm, trạng thái private.",
    r"""
**Lớp** là bản thiết kế; **đối tượng** là vật được dựng từ nó. Bản thiết kế
khai báo **trường dữ liệu** (nó biết gì) và **phương thức** (nó làm gì):

```java
public class Book {
    private String title;
    private int pages;

    public Book(String t, int p) {     // constructor
        title = t;
        pages = p;
    }

    public String getTitle() {         // accessor (getter)
        return title;
    }

    public boolean isLong() {          // hành vi
        return pages > 300;
    }
}
```

`new Book("Dune", 412)` dựng một đối tượng: cấp phát, chạy constructor, trả
về một **tham chiếu** tới nó. Lưu tham chiếu vào biến:

```java
Book b = new Book("Dune", 412);
b.getTitle()      // "Dune"
b.isLong()        // true
```

Dấu chấm với tới *bên trong* đối tượng: `b.title` được phép trong cùng lớp,
nhưng từ bên ngoài `title` là `private` — không với tới được. Đó là
**đóng gói (encapsulation)**: trạng thái riêng tư, truy cập đi qua phương
thức.

`this` gọi tên đối tượng hiện tại. Khi tham số che khuất trường, `this.`
gỡ nhầm lẫn: `this.title = title;`
""",
)

write_lesson(
    M, "apc-m8-ctors", "Constructors and references",
    "No-arg default, overloading, aliasing vs copying, null.",
    12, L2,
    "Constructor và tham chiếu",
    "Mặc định không đối số, nạp chồng, tham chiếu chung so với sao chép, null.",
    r"""
**Constructor** khởi tạo đối tượng mới. Các luật đề thi kiểm tra:

- Trùng tên lớp, **không có kiểu trả về** (kể cả void).
- Nếu bạn viết **không** constructor nào, Java âm thầm cấp một mặc định
  không-đối-số (mọi trường về 0/false/null) — nhưng chỉ khi đó. Viết một
  constructor bất kỳ và mặc định biến mất.

```java
public class Counter {
    private int count;

    public Counter() {           // không đối số: bắt đầu 0
        count = 0;
    }

    public Counter(int start) {  // nạp chồng: bắt đầu khác
        count = start;
    }
}
```

Hai constructor với danh sách tham số khác nhau = **nạp chồng (overload)**.
Lời gọi `new Counter(5)` chọn cái khớp.

**Nhiều tham chiếu, một đối tượng** — tham chiếu chung (aliasing):

```java
Counter a = new Counter();
Counter b = a;          // b trỏ tới CÙNG đối tượng; không sao chép
```

Giờ `a` và `b` là hai tên cho một bộ đếm. So với kiểu nguyên thủy, nơi
`int b = a` thực sự sao chép. Và tham chiếu null: biến đối tượng có thể giữ
`null` ("không có đối tượng") — gọi phương thức trên nó sẽ sập với
`NullPointerException`.
""",
)

write_lesson(
    M, "apc-m8-frq", "FRQ class design",
    "Reading the spec table, the five-part checklist, rubric details.",
    14, L3,
    "Thiết kế lớp theo FRQ",
    "Đọc bảng đặc tả, danh mục năm phần, chi tiết bảng chấm điểm.",
    r"""
FRQ **Câu 2 (Thiết kế Lớp)** đưa cho bạn bảng dạng:

| Biểu thức | Kết quả |
| --- | --- |
| `new Sensor(20)` | một cảm giác khởi đầu 20 |
| `s.read()` | giá trị hiện tại |
| `s.tick()` | giá trị tăng 1, không trả gì |

...và yêu cầu viết cả lớp. Danh mục kiểm tra mọi đáp án cần:

1. Dòng tiêu đề `public class Name {`.
2. Các biến thể hiện `private` — mỗi biến mà bảng ngụ ý.
3. Một constructor khớp dòng khởi tạo của bảng.
4. Các phương thức yêu cầu, đúng tên/chữ ký.

Đáp án mẫu cho bảng trên:

```java
public class Sensor {
    private int value;

    public Sensor(int start) {
        value = start;
    }

    public int read() {
        return value;
    }

    public void tick() {
        value++;
    }
}
```

Chi tiết bảng chấm: tên phương thức và kiểu tham số chính xác được tính điểm;
thay đổi trạng thái phải thực sự xảy ra (`value++` bên trong tick), và các
phương thức bảng thể hiện không trả về gì được khai báo `void`.

**Phân rã trong lớp**: một phương thức có thể gọi phương thức khác cùng đối
tượng trực tiếp — `isLong()` có thể gọi `getPages()` mà không cần dấu chấm.
""",
)

BOILER_BOOK = r"""public class Solution {
    // Write class Book inside Solution as a nested static class,
    // or make Solution itself the class the tests use.

    public static class Book {
        private String title;
        private int pages;

        // constructor here

        public String getTitle() {
            return title; // wire up
        }
    }
}
"""

BOILER_TEMP = r"""public class Solution {
    public static class Temp {
        private double celsius;

        public Temp(double c) {
            celsius = c;
        }

        public double getCelsius() {
            return celsius;
        }
    }
}
"""

BOILER_ACC = r"""public class Solution {
    public static class Account {
        private String owner;
        private int balance;

        public Account(String name, int start) {
            owner = name;
            balance = start;
        }

        public String getOwner() {
            return owner;
        }

        public int getBalance() {
            return balance;
        }
    }
}
"""

BOILER_FIX = r"""public class Solution {
    public static class Dog {
        private String name;

        public Dog(String n) {
            name = n;
        }

        public String speak() {
            return "Woof, I am " + name;
        }
    }
}
"""

CP8 = r"""public class Solution {
    public static class Sensor {
        private int value;

        public Sensor(int start) {
            value = start;
        }

        public int read() {
            return value;
        }

        public void tick() {
            value++;
        }
    }
}
"""

P_BOOK = challenge(
    "apc-m8-book",
    "Finish the Book class",
    "Complete the nested `Book` class: the constructor must set both fields (use parameters `t` and `p`), and add `int getPages()` returning pages. getTitle already works — follow its pattern.",
    BOILER_BOOK,
    [(
        "book behavior",
        r"""
Solution.Book b = new Solution.Book("Dune", 412);
CjTestBase.checkEq(b.getTitle(), "Dune", "title stored");
CjTestBase.checkEq(b.getPages(), 412, "pages stored");
Solution.Book c = new Solution.Book("Tintin", 62);
CjTestBase.checkEq(c.getTitle(), "Tintin", "second object independent");
CjTestBase.checkEq(c.getPages(), 62, "second pages");
""",
        "Two fields, one constructor assigning both, one accessor.",
    )],
    level="guided",
)

P_TEMP = challenge(
    "apc-m8-temperature",
    "Add behavior to a class",
    "The `Temp` class stores celsius. Add `double toFahrenheit()` returning c × 9/5 + 32, and `boolean isFreezing()` returning true at or below 0. Use the stored field — do not add parameters.",
    BOILER_TEMP,
    [(
        "temp behavior",
        r"""
Solution.Temp t = new Solution.Temp(100.0);
CjTestBase.checkNear(t.toFahrenheit(), 212.0, 1e-9, "boiling");
CjTestBase.checkTrue(!t.isFreezing(), "boiling not freezing");
Solution.Temp cold = new Solution.Temp(-5.0);
CjTestBase.checkTrue(cold.isFreezing(), "below zero freezes");
CjTestBase.checkTrue(new Solution.Temp(0.0).isFreezing(), "zero is freezing");
""",
        "Instance methods read fields directly: celsius * 9 / 5 + 32 (watch int division).",
    )],
    level="guided",
)

P_ACC = challenge(
    "apc-m8-account",
    "State mutation",
    "Add two mutators to `Account`: `void deposit(int amount)` (increase balance) and `void withdraw(int amount)` (decrease it, but never below 0 — a withdraw attempt that overdraws leaves the balance unchanged). Both return nothing.",
    BOILER_ACC,
    [(
        "account state",
        r"""
Solution.Account a = new Solution.Account("An", 100);
a.deposit(50);
CjTestBase.checkEq(a.getBalance(), 150, "after deposit");
a.withdraw(30);
CjTestBase.checkEq(a.getBalance(), 120, "after withdraw");
a.withdraw(500);
CjTestBase.checkEq(a.getBalance(), 120, "overdraw blocked");
""",
        "withdraw: if (amount <= balance) { balance -= amount; }",
    )],
    level="combination",
)

P_FIX = challenge(
    "apc-m8-fix-dog",
    "Debug the class",
    "`Dog` compiles but `speak()` returns \"Woof, I am null\" — the field was never stored. Find and fix the one-line constructor bug.",
    BOILER_FIX,
    [(
        "dog speaks",
        r"""
Solution.Dog d = new Solution.Dog("Rex");
CjTestBase.checkEq(d.speak(), "Woof, I am Rex", "named dog");
""",
        "The constructor parameter is dropped on the floor; assign it to name.",
    )],
    level="debugging",
)

CPM8 = challenge(
    "apc-cp-m8-sensor",
    "Checkpoint: build the Sensor class",
    "Rewrite the whole `Sensor` class from its spec table: `new Sensor(start)` stores the starting value; `read()` returns it; `tick()` adds 1 and returns nothing. State must persist across calls — three ticks after starting at 10 must read 13.",
    CP8,
    [(
        "sensor state",
        r"""
Solution.Sensor s = new Solution.Sensor(10);
CjTestBase.checkEq(s.read(), 10, "initial state");
s.tick();
s.tick();
s.tick();
CjTestBase.checkEq(s.read(), 13, "after three ticks");
new Solution.Sensor(0).tick();
Solution.Sensor fresh = new Solution.Sensor(-2);
fresh.tick();
CjTestBase.checkEq(fresh.read(), -1, "independent objects");
""",
        "Field + constructor + two methods; mutation happens on the field.",
    )],
    level="independent",
)

write_practice(
    M, "apc-p8-classes", "Class workshop", "Complete, extend, and debug classes.",
    "Xưởng lớp", "Hoàn thiện, mở rộng và sửa các lớp.",
    after_lesson="apc-m8-ctors", minutes=55, difficulty="beginner",
    challenges=[P_BOOK, P_TEMP, P_ACC, P_FIX],
    vi_challenges={
        "apc-m8-book": vi_challenge("Hoàn thiện lớp Book", "Hoàn thiện lớp `Book` lồng nhau: constructor phải đặt cả hai trường (dùng tham số `t` và `p`), và thêm `int getPages()` trả về pages. getTitle đã chạy — theo đúng mẫu của nó.",
            [("book behavior", "Hai trường, một constructor gán cả hai, một accessor.")]),
        "apc-m8-temperature": vi_challenge("Thêm hành vi vào lớp", "Lớp `Temp` lưu celsius. Thêm `double toFahrenheit()` trả về c × 9/5 + 32, và `boolean isFreezing()` trả về true khi bằng hoặc dưới 0. Dùng trường đã lưu — không thêm tham số.",
            [("temp behavior", "Phương thức thể hiện đọc trường trực tiếp: celsius * 9 / 5 + 32 (co chừng chia số nguyên).")]),
        "apc-m8-account": vi_challenge("Thay đổi trạng thái", "Thêm hai mutator vào `Account`: `void deposit(int amount)` (tăng balance) và `void withdraw(int amount)` (giảm, nhưng không bao giờ dưới 0 — lần rút vượt số dư giữ nguyên balance). Cả hai không trả về gì.",
            [("account state", "withdraw: if (amount <= balance) { balance -= amount; }")]),
        "apc-m8-fix-dog": vi_challenge("Sửa lớp", "`Dog` biên dịch nhưng `speak()` trả về \"Woof, I am null\" — trường chưa bao giờ được lưu. Tìm và sửa lỗi constructor một dòng.",
            [("dog speaks", "Tham số constructor bị bỏ trên sàn; gán nó vào name.")]),
    },
    solutions=[
        ("apc-m8-book", r"""public class Solution {
    public static class Book {
        private String title;
        private int pages;

        public Book(String t, int p) {
            title = t;
            pages = p;
        }

        public String getTitle() {
            return title;
        }

        public int getPages() {
            return pages;
        }
    }
}
""",
         r"""public class Solution {
    public static class Book {
        private String title;
        private int pages;

        public Book(String t, int p) {
            // BUG: pages never assigned — always 0
            title = t;
        }

        public String getTitle() {
            return title;
        }

        public int getPages() {
            return pages;
        }
    }
}
"""),
        ("apc-m8-temperature", r"""public class Solution {
    public static class Temp {
        private double celsius;

        public Temp(double c) {
            celsius = c;
        }

        public double getCelsius() {
            return celsius;
        }

        public double toFahrenheit() {
            return celsius * 9 / 5 + 32;
        }

        public boolean isFreezing() {
            return celsius <= 0;
        }
    }
}
""",
         r"""public class Solution {
    public static class Temp {
        private double celsius;

        public Temp(double c) {
            celsius = c;
        }

        public double getCelsius() {
            return celsius;
        }

        public double toFahrenheit() {
            // BUG: integer 9/5 truncates to 1
            return celsius * 9 / 5 + 32;
        }

        public boolean isFreezing() {
            // BUG: excludes exactly zero
            return celsius < 0;
        }
    }
}
"""),
        ("apc-m8-account", r"""public class Solution {
    public static class Account {
        private String owner;
        private int balance;

        public Account(String name, int start) {
            owner = name;
            balance = start;
        }

        public String getOwner() {
            return owner;
        }

        public int getBalance() {
            return balance;
        }

        public void deposit(int amount) {
            balance += amount;
        }

        public void withdraw(int amount) {
            if (amount <= balance) {
                balance -= amount;
            }
        }
    }
}
""",
         r"""public class Solution {
    public static class Account {
        private String owner;
        private int balance;

        public Account(String name, int start) {
            owner = name;
            balance = start;
        }

        public String getOwner() {
            return owner;
        }

        public int getBalance() {
            return balance;
        }

        public void deposit(int amount) {
            balance += amount;
        }

        public void withdraw(int amount) {
            // BUG: no overdraft guard
            balance -= amount;
        }
    }
}
"""),
        ("apc-m8-fix-dog", r"""public class Solution {
    public static class Dog {
        private String name;

        public Dog(String n) {
            name = n;
        }

        public String speak() {
            return "Woof, I am " + name;
        }
    }
}
""",
         r"""public class Solution {
    public static class Dog {
        private String name;

        public Dog(String n) {
            // BUG: original flaw kept — parameter never stored
        }

        public String speak() {
            return "Woof, I am " + name;
        }
    }
}
"""),
    ],
)

write_checkpoint(
    M, "apc-cp-m8", "Checkpoint: class design",
    "A complete FRQ-Q2-style class from its spec table.",
    22,
    r"""
You just wrote the exact shape AP FRQ Question 2 scores: private state, a
constructor matching the table, and methods that read and mutate it. If the
three-tick trace returned 13, you have the model.
""",
    "Điểm kiểm tra: thiết kế lớp",
    "Một lớp hoàn chỉnh theo phong cách FRQ Câu 2 từ bảng đặc tả.",
    r"""
Bạn vừa viết đúng hình dạng mà FRQ Câu 2 chấm điểm: trạng thái private,
constructor khớp bảng, và các phương thức đọc/thay đổi nó. Nếu bản truy vết
ba lần tick trả về 13, bạn đã nắm mô hình.
""",
    CPM8,
    vi_challenge("Điểm kiểm tra: thiết kế lớp", "Viết lại toàn bộ lớp `Sensor` từ bảng đặc tả: `new Sensor(start)` lưu giá trị ban đầu; `read()` trả về nó; `tick()` cộng 1 và không trả gì. Trạng thái phải tồn tại qua các lời gọi — ba lần tick sau khi bắt đầu 10 phải đọc được 13.",
        [("sensor state", "Trường + constructor + hai phương thức; phép thay đổi xảy ra trên trường.")]),
    solution=r"""public class Solution {
    public static class Sensor {
        private int value;

        public Sensor(int start) {
            value = start;
        }

        public int read() {
            return value;
        }

        public void tick() {
            value++;
        }
    }
}
""",
    wrong=r"""public class Solution {
    public static class Sensor {
        private int value;

        public Sensor(int start) {
            value = start;
        }

        public int read() {
            // BUG: returns the starting value forever — tick never stored
            return value;
        }

        public void tick() {
            value = value;
        }
    }
}
""",
)
