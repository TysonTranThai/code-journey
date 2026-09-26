#!/usr/bin/env python3
"""AP CSA Core M9 — Classes & Object Interaction (state + cooperation)."""
from apcc import *

M = "cx-objects"

L1 = r"""
Foundation's class module built single classes. The exam's Class Design
FRQ hands you a **spec table** — fields, constructor contract, method
behaviors — and grades exactness. The Core upgrade: treat state as the
star.

**Every method is state + promise.** For a `VendingMachine`:

```java
public class VendingMachine {
    private int cans;          // state
    private int tokens;        // state

    public VendingMachine(int cans) {   // initial state
        this.cans = cans;
        tokens = 0;
    }

    public boolean insertToken() {      // promise: 1 can per token
        if (cans == 0) {
            return false;               // state unchanged
        }
        cans--;
        tokens++;
        return true;
    }
    public int getCans() { return cans; }
    public int getTokens() { return tokens; }
}
```

Reading the spec as state transitions ("insertToken: cans−1, tokens+1,
but only when cans > 0") beats memorizing syntax. The failed-operation
branch that leaves state UNCHANGED is the part students forget — and
the part the FRQ rubric explicitly rewards.

**Design questions before code:** Which values live in fields (they
must survive between calls)? What is the initial state? Which methods
mutate (void or report)? Which only read?
"""

L2 = r"""
Two names, one object — aliasing bites hardest in class code:

```java
Scorecard s = new Scorecard();
Scorecard t = s;          // SAME object
t.add(10);
System.out.println(s.getTotal());   // 10 — not 0!
```

The companion trap: **no return means no effect** for immutable-style
results:

```java
String name = "ann";
name.toUpperCase();               // result discarded!
System.out.println(name);         // "ann"
```

Strings are immutable — methods return NEW strings; you must capture
the result. Objects like Scorecard are mutable — methods change the
object itself, and the change is visible through every alias.

The third aliasing trap: returning a private mutable field:

```java
private int[] data;
public int[] getData() { return data; }   // hands out the real thing!
```

Callers can now mutate your state through the returned reference. The
exam mostly teaches this as "encapsulation" — the defensible answer is
`return new int[...]` copy when asked "how do you protect the state?"

**Multiple interacting objects:**

```java
Account a = new Account(100);
Account b = new Account(30);
a.transferTo(b, 40);   // a: 60, b: 70 — one method mutates TWO objects
```

Trace them as two rows in the state table (Module 2's object rows),
now with a method that updates both rows in one call.
"""

L3 = r"""
Constructor bugs are the exam's favorite class questions, because they
look like working code:

**Shadowing** — the parameter hides the field:
```java
private String name;
public Player(String name) {
    name = name;      // assigns the parameter to itself!
}
```
Fix: `this.name = name;`. Symptom: getters return null/0 forever.

**Silent drop** — the parameter never mentioned:
```java
public Player(String n) { }   // fields stay at defaults
```

**Wrong default thinking.** Fields get Java defaults (0, null, false)
BEFORE the constructor runs. A constructor that only sets half the
fields silently chooses defaults for the rest — sometimes correct by
luck, usually wrong.

**Order of initialization:** field initializers run in declaration
order, then the constructor body. `private int count = 3;` plus a
constructor assigning `count = 0` ends at 0 — later assignment wins.

**Static vs instance (rarely the answer, know the shape):** a static
field is shared by all objects (one row); instance fields are one row
per object. `private static int created;` counts every constructor call
— an exam favorite for "how many objects were made?" questions.
"""

write_module(
    M,
    "Classes & Object Interaction",
    "State-transition thinking, aliasing across objects, and the constructor traps the exam loves — with a full class-design build.",
    "Lớp & tương tác đối tượng",
    "Tư duy chuyển-trạng-thái, bí danh giữa các đối tượng, và những cái bẫy constructor mà đề thi yêu thích — kèm một bài thiết kế lớp hoàn chỉnh.",
    lessons=["cx-m9-state", "cx-m9-aliasing", "cx-m9-constructor", "cx-cp-m9"],
    practices=["cx-p9-objects"],
)

write_lesson(
    M, "cx-m9-state", "State transitions",
    "Fields as state, methods as transitions, unchanged-state failure branches.",
    12, L1,
    "Chuyển đổi trạng thái",
    "Trường là trạng thái, phương thức là chuyển đổi, nhánh thất bại giữ-nguyên-trạng-thái.",
    r"""
Module nền đã dựng các lớp đơn lẻ. FRQ Thiết kế lớp của đề thi đưa cho
bạn một **bảng đặc tả** — trường, hợp đồng constructor, hành vi phương
thức — và chấm độ chính xác. Nâng cấp Core: coi trạng thái là ngôi sao.

**Mỗi phương thức là trạng thái + lời hứa.** Với một `VendingMachine`:

```java
public class VendingMachine {
    private int cans;          // trạng thái
    private int tokens;        // trạng thái

    public VendingMachine(int cans) {   // trạng thái ban đầu
        this.cans = cans;
        tokens = 0;
    }

    public boolean insertToken() {      // hứa: 1 lon mỗi token
        if (cans == 0) {
            return false;               // trạng thái không đổi
        }
        cans--;
        tokens++;
        return true;
    }
    public int getCans() { return cans; }
    public int getTokens() { return tokens; }
}
```

Đọc đặc tả như các chuyển đổi trạng thái ("insertToken: cans−1,
tokens+1, nhưng chỉ khi cans > 0") thắng việc học thuộc cú pháp. Nhánh
thao-tác-thất-bại-giữ-nguyên-trạng-thái là phần học sinh quên — và là
phần bảng chấm FRQ thưởng explicitly.

**Câu hỏi thiết kế trước mã:** Giá trị nào sống trong trường (chúng phải
sống sót giữa các lời gọi)? Trạng thái ban đầu là gì? Phương thức nào
biến đổi (void hay báo cáo)? Phương thức nào chỉ đọc?
""",
)

write_lesson(
    M, "cx-m9-aliasing", "Aliasing and encapsulation",
    "One object, many names; immutable returns; leaking private arrays.",
    12, L2,
    "Bí danh và đóng gói",
    "Một đối tượng, nhiều tên; trả về bất biến; rò rỉ mảng riêng tư.",
    r"""
Hai tên, một đối tượng — bí danh cắn dữ nhất trong mã lớp:

```java
Scorecard s = new Scorecard();
Scorecard t = s;          // CÙNG đối tượng
t.add(10);
System.out.println(s.getTotal());   // 10 — không phải 0!
```

Cái bẫy anh em: **không nhận kết quả tức không có tác dụng** với kết-quả
kiểu bất biến:

```java
String name = "ann";
name.toUpperCase();               // kết quả bị vứt!
System.out.println(name);         // "ann"
```

String là bất biến — phương thức trả về chuỗi MỚI; bạn phải bắt lấy kết
quả. Đối tượng như Scorecard là khả biến — phương thức đổi chính đối
tượng, và sự thay đổi nhìn thấy qua mọi bí danh.

Cái bẫy bí danh thứ ba: trả về một trường riêng tư khả biến:

```java
private int[] data;
public int[] getData() { return data; }   // giao nộp bản thật!
```

Người gọi giờ có thể biến đổi trạng thái của bạn qua tham chiếu được
trả. Đề thi chủ yếu dạy điều này như "đóng gói" — câu trả lời vững là
`return new int[...]` (bản sao) khi được hỏi "làm sao bảo vệ trạng
thái?"

**Nhiều đối tượng tương tác:**

```java
Account a = new Account(100);
Account b = new Account(30);
a.transferTo(b, 40);   // a: 60, b: 70 — một phương thức biến đổi HAI đối tượng
```

Truy vết chúng như hai hàng trong bảng trạng thái (hàng đối tượng của
Module 2), nay với một phương thức cập nhật cả hai hàng trong một lời
gọi.
""",
)

write_lesson(
    M, "cx-m9-constructor", "Constructor traps",
    "Shadowing, silent drops, defaults, initialization order, static counting.",
    12, L3,
    "Các bẫy constructor",
    "Che khuất, thả im lặng, giá trị mặc định, thứ tự khởi tạo, đếm static.",
    r"""
Lỗi constructor là câu hỏi lớp ưa thích của đề thi, vì chúng trông như
mã đang chạy đúng:

**Che khuất (shadowing)** — tham số che mất trường:
```java
private String name;
public Player(String name) {
    name = name;      // gán tham số cho chính nó!
}
```
Sửa: `this.name = name;`. Triệu chứng: getter mãi mãi trả về null/0.

**Thả im lặng** — tham số không hề được nhắc tới:
```java
public Player(String n) { }   // trường ở lại giá trị mặc định
```

**Tư duy sai về mặc định.** Các trường nhận giá trị mặc định của Java
(0, null, false) TRƯỚC khi constructor chạy. Constructor chỉ đặt một nửa
các trường là lặng lẽ chọn mặc định cho nửa còn lại — đôi khi đúng do
may mắn, thường thì sai.

**Thứ tự khởi tạo:** các bộ khởi tạo trường chạy theo thứ tự khai báo,
rồi thân constructor. `private int count = 3;` cộng với constructor gán
`count = 0` kết thúc ở 0 — phép gán sau thắng.

**Static với instance (hiếm khi là đáp án, biết hình dạng):** trường
static được chia sẻ bởi mọi đối tượng (một hàng); trường instance là
một hàng mỗi đối tượng. `private static int created;` đếm mọi lời gọi
constructor — đề thi ưa dùng cho câu "đã tạo bao nhiêu đối tượng?"
""",
)

BOILER_TOLL = r"""public class Solution {
    public static class TollBooth {
        private int cars;
        private int cash;

        public TollBooth(int startingCash) {
            // set cars = 0, cash = startingCash
        }

        // CONTRACT: one car pays 2. Returns the amount collected (2),
        // or 0 if... cars never refuse to pay. Always collects.
        public int carPasses() {
            return 0; // replace
        }

        public int getCars() { return cars; }
        public int getCash() { return cash; }
    }
}
"""

BOILER_TRANSFER = r"""public class Solution {
    public static class Account {
        private int balance;
        public Account(int b) { balance = b; }
        public int getBalance() { return balance; }

        // CONTRACT: move amount to other. When balance >= amount:
        // balance -= amount; other gains it; return true.
        // Otherwise: NOTHING changes; return false.
        public boolean transferTo(Account other, int amount) {
            return false; // replace
        }
    }
}
"""

BOILER_TEMP = r"""public class Solution {
    public static class Thermostat {
        private int celsius;

        public Thermostat() { celsius = 20; }

        // CONTRACT: raise by d, but NEVER above 30 (clamp at 30).
        public void warm(int d) {
            celsius += d; // BUG: ignores the 30 cap
        }

        // CONTRACT: lower by d, but NEVER below 0 (clamp at 0).
        public void cool(int d) {
            celsius -= d; // BUG: ignores the 0 floor
        }

        public int get() { return celsius; }
    }
}
"""

BOILER_ALIASQ = r"""public class Solution {
    public static class Box {
        private int v;
        public Box(int v) { this.v = v; }
        public void set(int v) { this.v = v; }
        public int get() { return v; }
    }

    // CONTRACT: demonstrates aliasing. After the three statements below,
    // return a.get() * 100 + b.get() using the SHARED-object semantics
    // (b = a aliases the same Box; the last set() wins for both).
    public static int demo() {
        Box a = new Box(1);
        Box b = a;
        b.set(9);
        return a.get() * 100 + b.get(); // keep this line; fix nothing
    }
}
"""

BOILER_SHADOWER = r"""public class Solution {
    public static class Player {
        private String name;
        private int hp;

        public Player(String name, int hp) {
            // BUG: parameter shadows field for name
            name = name;
            this.hp = hp;
        }

        public String getName() { return name; }
        public int getHp() { return hp; }
    }
}
"""

BOILER_CP9 = r"""public class Solution {
    // SPEC TABLE — build the whole class:
    // fields: int total; int itemCount;
    // constructor: everything starts at 0
    // addItem(int price): total += price; itemCount++
    //   (prices may be any int; no validation)
    // refundLast(): when itemCount > 0, subtract ONE stored price
    //   (the most recent) and decrement itemCount; return true.
    //   When the cart is empty: change nothing, return false.
    // getTotal() / getCount(): readers
    // You MAY add one extra field to remember the last price.
    public static class ShoppingCart {
        // replace with your class: fields, constructor, methods
    }
}
"""

P_TOLL = challenge(
    "cx-m9-tollbooth",
    "State machine from a spec",
    "Complete `TollBooth`: constructor sets cars = 0, cash = startingCash. `carPasses()` adds one car and 2 cash, returning 2. Getters are given.",
    BOILER_TOLL,
    [(
        "toll collected",
        r"""
Solution.TollBooth t = new Solution.TollBooth(100);
CjTestBase.checkEq(t.getCars(), 0, "starts empty");
t.carPasses();
t.carPasses();
CjTestBase.checkEq(t.getCars(), 2, "two cars");
CjTestBase.checkEq(t.getCash(), 104, "100 + 2 + 2");
""",
        "cars++; cash += 2; return 2; — constructor: this.cars = 0; this.cash = startingCash;",
    )],
    level="guided",
)

P_TRANSFER = challenge(
    "cx-m9-transfer",
    "Two objects, one method",
    "Complete `Account.transferTo`: on success both balances change; on failure NEITHER does. The failed branch leaving state untouched is the part being graded.",
    BOILER_TRANSFER,
    [(
        "transfer semantics",
        r"""
Solution.Account a = new Solution.Account(100);
Solution.Account b = new Solution.Account(30);
CjTestBase.checkEq(a.transferTo(b, 40), true, "succeeds");
CjTestBase.checkEq(a.getBalance(), 60, "debit");
CjTestBase.checkEq(b.getBalance(), 70, "credit");
CjTestBase.checkEq(a.transferTo(b, 999), false, "insufficient");
CjTestBase.checkEq(a.getBalance(), 60, "unchanged on failure");
CjTestBase.checkEq(b.getBalance(), 70, "unchanged on failure");
""",
        "if (balance >= amount) { balance -= amount; other.balance += amount; return true; } return false;",
    )],
    level="combination",
)

P_TEMP = challenge(
    "cx-m9-thermostat",
    "Clamped mutators",
    "Fix both mutators: `warm` never exceeds 30, `cool` never drops below 0. Trace warm(15) from 20 and cool(25) from 5 before coding.",
    BOILER_TEMP,
    [(
        "clamped",
        r"""
Solution.Thermostat t = new Solution.Thermostat();
CjTestBase.checkEq(t.get(), 20, "default 20");
t.warm(15);
CjTestBase.checkEq(t.get(), 30, "capped at 30");
t.cool(25);
CjTestBase.checkEq(t.get(), 5, "30 - 25");
t.cool(25);
CjTestBase.checkEq(t.get(), 0, "floored at 0");
""",
        "warm: if (celsius + d > 30) celsius = 30; else celsius += d; — mirror for cool.",
    )],
    level="debugging",
)

P_ALIAS = challenge(
    "cx-m9-alias-demo",
    "Predict the alias",
    "`demo` looks like it makes two boxes — it makes ONE, with two names. Trace the three statements, predict the return value, and confirm the code already encodes it (no changes needed): this challenge grades your trace.",
    BOILER_ALIASQ,
    [(
        "aliased state",
        r"""
CjTestBase.checkEq(Solution.demo(), 909, "one Box: both names read 9");
""",
        "b IS a; set(9) changes the only object; 9*100 + 9 = 909.",
    )],
    level="independent",
)

P_SHADOW = challenge(
    "cx-m9-fix-shadow",
    "Fix the shadowed field",
    "`Player` compiles, but `getName()` returns null forever. Trace the constructor's assignment and apply the one-token fix.",
    BOILER_SHADOWER,
    [(
        "fields stored",
        r"""
Solution.Player p = new Solution.Player("Lan", 5);
CjTestBase.checkEq(p.getName(), "Lan", "name stored");
CjTestBase.checkEq(p.getHp(), 5, "hp stored");
""",
        "this.name = name; — the this. disambiguates field from parameter.",
    )],
    level="debugging",
)

CP9 = challenge(
    "cx-cp-m9-cart",
    "Checkpoint: ShoppingCart from a spec table",
    "Build the full `ShoppingCart` class from its spec table: addItem tracks total, count, AND the last price; refundLast undoes the most recent item (empty cart → false, nothing changes); readers given. The last-price memory is one extra field — the spec permits it.",
    BOILER_CP9,
    [(
        "cart behaviors",
        r"""
Solution.ShoppingCart c = new Solution.ShoppingCart();
CjTestBase.checkEq(c.getTotal(), 0, "empty total");
CjTestBase.checkEq(c.getCount(), 0, "empty count");
CjTestBase.checkEq(c.refundLast(), false, "nothing to refund");
c.addItem(10);
c.addItem(25);
CjTestBase.checkEq(c.getTotal(), 35, "10 + 25");
CjTestBase.checkEq(c.getCount(), 2, "two items");
CjTestBase.checkEq(c.refundLast(), true, "refund 25");
CjTestBase.checkEq(c.getTotal(), 10, "back to 10");
CjTestBase.checkEq(c.getCount(), 1, "one item left");
CjTestBase.checkEq(c.refundLast(), true, "refund 10");
CjTestBase.checkEq(c.getCount(), 0, "cart now empty");
CjTestBase.checkEq(c.refundLast(), false, "nothing left to refund");
""",
        "Fields: total, itemCount, lastPrice. addItem sets all three; refundLast guards itemCount > 0.",
    )],
    level="real-world",
)

write_practice(
    M, "cx-p9-objects", "Object workshop",
    "State machines, two-object methods, clamps, alias prediction, shadow repair.",
    "Xưởng đối tượng",
    "Máy trạng thái, phương thức hai đối tượng, kẹp biên, dự đoán bí danh, sửa che khuất.",
    after_lesson="cx-m9-aliasing", minutes=60, difficulty="advanced",
    challenges=[P_TOLL, P_TRANSFER, P_TEMP, P_ALIAS, P_SHADOW],
    vi_challenges={
        "cx-m9-tollbooth": vi_challenge("Máy trạng thái từ đặc tả",
            "Hoàn thiện `TollBooth`: constructor đặt cars = 0, cash = startingCash. `carPasses()` thêm một xe và 2 tiền, trả về 2. Các getter đã cho sẵn.",
            [("toll collected", "cars++; cash += 2; return 2; — constructor: this.cars = 0; this.cash = startingCash;")]),
        "cx-m9-transfer": vi_challenge("Hai đối tượng, một phương thức",
            "Hoàn thiện `Account.transferTo`: thành công thì cả hai số dư đổi; thất bại thì KHÔNG cái nào đổi. Nhánh thất bại giữ nguyên trạng thái là phần được chấm.",
            [("transfer semantics", "if (balance >= amount) { balance -= amount; other.balance += amount; return true; } return false;")]),
        "cx-m9-thermostat": vi_challenge("Mutator kẹp biên",
            "Sửa cả hai mutator: `warm` không bao giờ vượt 30, `cool` không bao giờ xuống dưới 0. Truy vết warm(15) từ 20 và cool(25) từ 5 trước khi viết mã.",
            [("clamped", "warm: if (celsius + d > 30) celsius = 30; else celsius += d; — đối xứng cho cool.")]),
        "cx-m9-alias-demo": vi_challenge("Dự đoán bí danh",
            "`demo` trông như tạo hai hộp — thực ra tạo MỘT, với hai tên. Truy vết ba câu lệnh, dự đoán giá trị trả về, và xác nhận mã đã mã hóa đúng (không cần sửa): bài này chấm phép truy vết của bạn.",
            [("aliased state", "b CHÍNH LÀ a; set(9) đổi đối tượng duy nhất; 9*100 + 9 = 909.")]),
        "cx-m9-fix-shadow": vi_challenge("Sửa trường bị che khuất",
            "`Player` biên dịch được, nhưng `getName()` mãi mãi trả về null. Truy vết phép gán trong constructor và áp dụng bản sửa một-token.",
            [("fields stored", "this.name = name; — this. phân biệt trường với tham số.")]),
    },
    solutions=[
        ("cx-m9-tollbooth",
         BOILER_TOLL.replace("            // set cars = 0, cash = startingCash",
            "            cars = 0;\n            cash = startingCash;")
            .replace("            return 0; // replace",
                "            cars++;\n            cash += 2;\n            return 2;"),
         BOILER_TOLL.replace("            // set cars = 0, cash = startingCash",
            "            cars = 0;\n            cash = startingCash;")
            .replace("            return 0; // replace",
                "            cars++;\n            cash += 3;\n            return 2;")),
        ("cx-m9-transfer", BOILER_TRANSFER.replace("            return false; // replace",
            "            if (balance >= amount) {\n                balance -= amount;\n                other.balance += amount;\n                return true;\n            }\n            return false;"),
         BOILER_TRANSFER.replace("            return false; // replace",
            "            if (balance >= amount) {\n                balance -= amount;\n                other.balance -= amount;\n                return true;\n            }\n            return false;")),
        ("cx-m9-thermostat",
         BOILER_TEMP.replace("            celsius += d; // BUG: ignores the 30 cap",
            "            if (celsius + d > 30) {\n                celsius = 30;\n            } else {\n                celsius += d;\n            }")
            .replace("            celsius -= d; // BUG: ignores the 0 floor",
                "            if (celsius - d < 0) {\n                    celsius = 0;\n                } else {\n                    celsius -= d;\n                }"),
         BOILER_TEMP.replace("            celsius += d; // BUG: ignores the 30 cap",
            "            if (celsius + d >= 30) {\n                celsius = 31;\n            } else {\n                celsius += d;\n            }")
            .replace("            celsius -= d; // BUG: ignores the 0 floor",
                "            if (celsius - d < 0) {\n                    celsius = 0;\n                } else {\n                    celsius -= d;\n                }")),
        ("cx-m9-alias-demo", BOILER_ALIASQ, BOILER_ALIASQ.replace("b.set(9);", "b.set(8);")),
        ("cx-m9-fix-shadow", BOILER_SHADOWER.replace("            name = name;", "            this.name = name;"),
         BOILER_SHADOWER),
    ],
)

write_checkpoint(
    M, "cx-cp-m9", "Checkpoint: ShoppingCart",
    "A full class from a spec table — state, memory field, guarded undo.",
    30,
    r"""
Three fields (total, itemCount, lastPrice), a constructor, two mutators
with a guard, two readers — the exact anatomy of an exam Class Design
FRQ. The insight being graded: refundLast needs MEMORY (the last price),
which is a state decision, not a syntax decision. When the spec table
is silent about a case, the guard is your answer (empty cart → false,
nothing changes).
""",
    "Điểm kiểm tra: ShoppingCart",
    "Một lớp hoàn chỉnh từ bảng đặc tả — trạng thái, trường ghi nhớ, hoàn tác có chặn.",
    r"""
Ba trường (total, itemCount, lastPrice), một constructor, hai mutator
có lớp chặn, hai reader — đúng giải phẫu của một FRQ Thiết kế lớp trong
đề thi. Trực giác được chấm: refundLast cần BỘ NHỚ (giá cuối), là một
quyết định trạng thái chứ không phải quyết định cú pháp. Khi bảng đặc
tả im lặng về một trường hợp, lớp chặn là câu trả lời của bạn (giỏ rỗng
→ false, không gì đổi).
""",
    CP9,
    vi_challenge("Điểm kiểm tra: ShoppingCart",
        "Dựng lớp `ShoppingCart` đầy đủ từ bảng đặc tả: addItem theo dõi tổng, số lượng, VÀ giá cuối; refundLast hoàn lại món gần nhất (giỏ rỗng → false, không đổi gì); các reader đã cho. Bộ nhớ giá-cuối là một trường bổ sung — đặc tả cho phép.",
        [("cart behaviors", "Trường: total, itemCount, lastPrice. addItem đặt cả ba; refundLast chặn itemCount > 0.")]),
    solution=r"""public class Solution {
    public static class ShoppingCart {
        private int total;
        private int itemCount;
        private int lastPrice;

        public ShoppingCart() {
            total = 0;
            itemCount = 0;
            lastPrice = 0;
        }

        public void addItem(int price) {
            total += price;
            itemCount++;
            lastPrice = price;
        }

        public boolean refundLast() {
            if (itemCount == 0) {
                return false;
            }
            total -= lastPrice;
            itemCount--;
            return true;
        }

        public int getTotal() { return total; }
        public int getCount() { return itemCount; }
    }
}
""",
    wrong=r"""public class Solution {
    public static class ShoppingCart {
        private int total;
        private int itemCount;
        private int lastPrice;

        public ShoppingCart() {
            total = 0;
            itemCount = 0;
            lastPrice = 0;
        }

        public void addItem(int price) {
            total += price;
            itemCount++;
            lastPrice = price;
        }

        public boolean refundLast() {
            if (itemCount == 0) {
                return false;
            }
            total -= lastPrice;
            itemCount--;
            return true;
        }

        public int getTotal() { return itemCount; }
        public int getCount() { return total; }
    }
}
""",
)
