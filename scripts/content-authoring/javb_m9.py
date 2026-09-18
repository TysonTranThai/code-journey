#!/usr/bin/env python3
"""Java — Beginner — Module 9: java-data-modeling."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javb import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-data-modeling"

L_ENUM_EN = r'''
An **enum** is a type with a fixed, named set of values — compile-time
protection against impossible states:

```java
enum OrderStatus { PENDING, PAID, SHIPPED, CANCELLED }

OrderStatus s = OrderStatus.PAID;
```

`switch` over an enum is exhaustive-checked: add a status later and every
switch without it fails to compile — the compiler becomes your checklist.

```java
boolean isFinal = switch (s) {
    case PAID, SHIPPED -> false;      // multiple labels share an arm
    case CANCELLED -> true;
    case PENDING -> false;
};
```

Enums are full classes: they can carry fields, constructors, and methods —
each constant runs the constructor once:

```java
enum Planet {
    MERCURY(0.39), EARTH(1.0), MARS(1.52);   // semicolon after the list!

    private final double auFromSun;
    Planet(double au) { this.auFromSun = au; }
    public double au() { return auFromSun; }
}
```

Every enum automatically gives you `values()` (all constants in order),
`valueOf("PAID")` (parse; throws on unknown), `name()`, and `ordinal()`
(declaration position — avoid using it for logic; reordering constants
should never change behavior). Comparing enum constants uses `==` safely:
they are singletons, and this is the one place `==` on objects is idiomatic.

Use an enum whenever a variable's legal values are a closed list — status,
season, difficulty, compass direction. It replaces `int` codes (what is 3?)
and stringly-typed checks (typo-safe at compile time).

**Next:** records — data with no ceremony.
'''

L_ENUM_VI = r'''
**Enum** là một kiểu có tập giá trị cố định, được đặt tên — bảo vệ lúc biên
dịch khỏi những trạng thái không thể tồn tại:

```java
enum OrderStatus { PENDING, PAID, SHIPPED, CANCELLED }

OrderStatus s = OrderStatus.PAID;
```

`switch` trên enum được kiểm tra tính đầy đủ: thêm một trạng thái sau này và
mọi switch thiếu nó sẽ không biên dịch — compiler trở thành checklist của bạn.

```java
boolean isFinal = switch (s) {
    case PAID, SHIPPED -> false;      // nhiều nhãn dùng chung một nhánh
    case CANCELLED -> true;
    case PENDING -> false;
};
```

Enum là class đầy đủ: có thể mang trường, constructor, và phương thức — mỗi
hằng số chạy constructor đúng một lần:

```java
enum Planet {
    MERCURY(0.39), EARTH(1.0), MARS(1.52);   // dấu chấm phẩy sau danh sách!

    private final double auFromSun;
    Planet(double au) { this.auFromSun = au; }
    public double au() { return auFromSun; }
}
```

Mỗi enum tự động có `values()` (mọi hằng theo thứ tự),
`valueOf("PAID")` (parse; ném exception với giá trị lạ), `name()`, và
`ordinal()` (vị trí khai báo — tránh dùng ordinal cho logic; việc đổi thứ tự
hằng không bao giờ được phép đổi hành vi). So sánh hằng enum dùng `==` một
cách an toàn: chúng là singleton, và đây là chỗ duy nhất `==` trên object
là thành ngữ chuẩn.

Dùng enum bất cứ khi nào giá trị hợp lệ của một biến là danh sách đóng —
trạng thái, mùa, độ khó, phương hướng. Nó thay mã `int` (số 3 là gì?) và
so sánh bằng chuỗi (sai chính tả bị compiler bắt).

**Tiếp theo:** record — dữ liệu không nghi thức.
'''

L_RECORDS_EN = r'''
A **record** (Java 16+) declares an immutable data carrier in one line:

```java
record Point(int x, int y) { }

Point p = new Point(3, 4);
p.x();                    // accessor named like the component, not getX()
```

From that single line the compiler generates: `private final` fields for
every component, an accessor per component (`x()`, `y()`), a constructor
taking all components in order, `equals` and `hashCode` comparing ALL
components, and a `toString` like `Point[x=3, y=4]`. Compare that with the
30 lines of class, constructor, getters, equals, hashCode, toString you
would have typed in Module 7 — records delete ceremony, not meaning.

**When to use what** — the modeling decision tree:

- **record**: immutable value whose identity IS its data (two `Point(3,4)`s
  are interchangeable). Money, coordinates, name pairs, API responses.
- **enum**: a closed set of named constants (OrderStatus).
- **class**: mutable state, partial construction, behavior-rich objects
  (Account with a changing balance), or unique identity (a bank account is
  its number, not its balance — two accounts with equal balances are NOT
  the same account).

Records may validate: a **compact constructor** runs before fields are set:

```java
record Temperature(double celsius) {
    Temperature {                      // compact form: no parameter list
        if (celsius < -273.15) {
            throw new IllegalArgumentException("below absolute zero");
        }
    }
}
```

Records cannot extend a class (they already extend `java.lang.Record`) but
can implement interfaces — and nested records give your challenges clean,
readable data types.

**Next:** equality and hashing, the contract behind collections.
'''

L_RECORDS_VI = r'''
**Record** (Java 16+) khai báo một kho dữ liệu bất biến trong một dòng:

```java
record Point(int x, int y) { }

Point p = new Point(3, 4);
p.x();                    // accessor trùng tên thành phần, không phải getX()
```

Từ một dòng đó, compiler sinh ra: trường `private final` cho mọi thành phần,
một accessor cho mỗi thành phần (`x()`, `y()`), constructor nhận mọi thành
phần theo thứ tự, `equals` và `hashCode` so sánh TẤT CẢ các thành phần, và
`toString` dạng `Point[x=3, y=4]`. So với 30 dòng class, constructor,
getter, equals, hashCode, toString bạn từng gõ ở Module 7 — record xóa nghi
thức, không xóa ý nghĩa.

**Khi nào dùng gì** — cây quyết định mô hình hóa:

- **record**: giá trị bất biến mà danh tính CHÍNH LÀ dữ liệu (hai
  `Point(3,4)` có thể hoán đổi cho nhau). Tiền, tọa độ, cặp tên, response API.
- **enum**: tập hằng số có tên đóng kín (OrderStatus).
- **class**: trạng thái có thể đổi, khởi tạo từng phần, object giàu hành vi
  (Account với số dư thay đổi), hoặc danh tính duy nhất (tài khoản ngân
  hàng là số tài khoản, không phải số dư — hai tài khoản cùng số dư
  KHÔNG phải cùng tài khoản).

Record có thể xác thực: **compact constructor** chạy trước khi các trường
được gán:

```java
record Temperature(double celsius) {
    Temperature {                      // dạng compact: không cần danh sách tham số
        if (celsius < -273.15) {
            throw new IllegalArgumentException("below absolute zero");
        }
    }
}
```

Record không thể extends một class (nó đã extends `java.lang.Record`) nhưng
implement được interface — và record lồng nhau cho các thử thách của bạn
những kiểu dữ liệu sạch, dễ đọc.

**Tiếp theo:** đẳng thức và hashing — hợp đồng đứng sau mọi collection.
'''

L_EQUALITY_EN = r'''
Equality in Java has two layers, and collections stand on both.

**`equals(Object)`** — value equality. The default (from `Object`) is
reference identity; classes override it to compare contents. The contract
you must know: reflexive, symmetric (`a.equals(b)` ⇔ `b.equals(a)`), null
returns `false` (never throws — but calling `x.equals(null)` on your own
object should be guarded by an `instanceof` check).

```java
String a = "yes";
a.equals("yes")                    // true — content
new Point(1, 2).equals(new Point(1, 2))   // record: true — all components
```

**`hashCode()`** — an int summary of the value. THE rule: **equal objects
must have equal hash codes**. If you override equals you must override
hashCode consistently, because hash-based collections (HashSet, HashMap)
first bucket by hashCode, then confirm with equals. Break the pairing and
objects vanish inside sets ("I added it, but contains says false").

```java
class BadPoint {
    final int x, y;
    // ...
    @Override
    public boolean equals(Object o) {
        return o instanceof BadPoint p && p.x == x && p.y == y;
    }
    // hashCode NOT overridden → identity hash → HashSet misbehaves
}
```

Records and enums get all of this for free — one more reason the modeling
tree above prefers them. When you DO hand-write equals (an old-style class),
generate hashCode too (your IDE does; `Objects.hash(x, y)` is the manual
form).

**`toString()`** is the third leg: every exception message, log line, and
debugger view prints it. A class without a real toString debugs badly.

**Next:** practice — modeling real data.
'''

L_EQUALITY_VI = r'''
Đẳng thức trong Java có hai tầng, và các collection đứng trên cả hai.

**`equals(Object)`** — đẳng thức theo giá trị. Bản mặc định (từ `Object`)
là identity theo tham chiếu; class override nó để so nội dung. Hợp đồng
cần nhớ: phản xạ, đối xứng (`a.equals(b)` ⇔ `b.equals(a)`), với null trả
`false` (không ném — nhưng khi tự viết equals, chặn bằng kiểm tra
`instanceof`).

```java
String a = "yes";
a.equals("yes")                    // true — nội dung
new Point(1, 2).equals(new Point(1, 2))   // record: true — mọi thành phần
```

**`hashCode()`** — một int tóm tắt giá trị. QUY TẮC: **object bằng nhau
phải có hash code bằng nhau**. Override equals thì phải override hashCode
nhất quán, vì các collection dựa trên hash (HashSet, HashMap) xếp bucket
theo hashCode trước, rồi xác nhận bằng equals. Phá cặp này và object biến
mất trong set ("tôi đã thêm mà contains lại bảo false").

```java
class BadPoint {
    final int x, y;
    // ...
    @Override
    public boolean equals(Object o) {
        return o instanceof BadPoint p && p.x == x && p.y == y;
    }
    // hashCode KHÔNG được override → identity hash → HashSet hỏng ngầm
}
```

Record và enum có sẵn tất cả — thêm một lý do để cây mô hình hóa ở trên
ưu tiên chúng. Khi THẬT SỰ phải viết equals tay (class kiểu cũ), hãy sinh
luôn hashCode (IDE làm được; dạng tay là `Objects.hash(x, y)`).

**`toString()`** là chân thứ ba: mọi thông điệp exception, dòng log, và
cửa sổ debugger đều in nó. Class thiếu toString thật thì gỡ lỗi rất khổ.

**Tiếp theo:** thực hành — mô hình hóa dữ liệu thật.
'''

# ── practice set 9 ──────────────────────────────────────────────────────────
P9_STATUS = challenge(
    "javb-m9-order-status",
    "Order status state machine",
    "Inside `Solution`, write `enum OrderStatus { PENDING, PAID, SHIPPED, "
    "CANCELLED }` and `static boolean canCancel(OrderStatus s)` returning "
    "true only for PENDING and PAID. Also `static OrderStatus next(OrderStatus "
    "s)`: PENDING→PAID, PAID→SHIPPED, and for SHIPPED/CANCELLED the state "
    "stays itself (terminal).",
    r'''public class Solution {
    public enum OrderStatus { PENDING, PAID, SHIPPED, CANCELLED }

    public static boolean canCancel(OrderStatus s) {
        return false;
    }

    public static OrderStatus next(OrderStatus s) {
        return s;
    }
}
''',
    [
        (
            "cancellation rules",
            r"""
CjTestBase.checkTrue(Solution.canCancel(Solution.OrderStatus.PENDING), "pending can cancel");
CjTestBase.checkTrue(Solution.canCancel(Solution.OrderStatus.PAID), "paid can cancel");
CjTestBase.checkTrue(!Solution.canCancel(Solution.OrderStatus.SHIPPED), "shipped cannot");
""",
            "Only the two early stages allow cancellation.",
        ),
        (
            "state transitions",
            r"""
CjTestBase.checkEq(Solution.next(Solution.OrderStatus.PENDING), Solution.OrderStatus.PAID, "pending -> paid");
CjTestBase.checkEq(Solution.next(Solution.OrderStatus.SHIPPED), Solution.OrderStatus.SHIPPED, "shipped is terminal");
""",
            "Terminal states map to themselves.",
        ),
    ],
    level="guided",
)

P9_STATUS_VI = vi_challenge(
    "Máy trạng thái đơn hàng",
    "Bên trong `Solution`, viết `enum OrderStatus { PENDING, PAID, SHIPPED, "
    "CANCELLED }` và `static boolean canCancel(OrderStatus s)` chỉ trả true "
    "với PENDING và PAID. Cùng `static OrderStatus next(OrderStatus s)`: "
    "PENDING→PAID, PAID→SHIPPED, còn SHIPPED/CANCELLED giữ nguyên (trạng "
    "thái kết thúc).",
    [
        ("cancellation rules", "Chỉ hai giai đoạn đầu cho phép hủy."),
        ("state transitions", "Trạng thái kết thúc ánh xạ về chính nó."),
    ],
)

P9_RECORD = challenge(
    "javb-m9-weather-record",
    "A validated record",
    "Inside `Solution`, write `record Weather(String city, double celsius)` "
    "with a compact constructor that rejects `null`/blank city and celsius "
    "below -273.15 (IllegalArgumentException). Add `static double average("
    "Weather[] readings)` returning the mean celsius of a non-empty array.",
    r'''public class Solution {
    public record Weather(String city, double celsius) {
        public Weather {
            // validate here
        }
    }

    public static double average(Weather[] readings) {
        return 0;
    }
}
''',
    [
        (
            "record equality is free",
            r"""
Solution.Weather a = new Solution.Weather("Hanoi", 30);
Solution.Weather b = new Solution.Weather("Hanoi", 30);
CjTestBase.checkTrue(a.equals(b), "same data -> equal");
CjTestBase.checkEq(a.celsius(), 30.0, "accessor");
""",
            "Records compare by all components — no hand-written equals.",
        ),
        (
            "validation fires",
            r"""
CjTestBase.checkThrows(() -> new Solution.Weather("", 20), "blank city");
CjTestBase.checkThrows(() -> new Solution.Weather("Hanoi", -300), "below absolute zero");
""",
            "The compact constructor runs at every construction.",
        ),
        (
            "average",
            r"""
double avg = Solution.average(new Solution.Weather[]{
    new Solution.Weather("Hanoi", 30), new Solution.Weather("Da Lat", 20)});
CjTestBase.checkNear(avg, 25.0, 1e-9, "mean of 30 and 20");
""",
            "Average over the components.",
        ),
    ],
    level="independent",
)

P9_RECORD_VI = vi_challenge(
    "Record có xác thực",
    "Bên trong `Solution`, viết `record Weather(String city, double celsius)` "
    "với compact constructor từ chối city null/rỗng và celsius dưới -273.15 "
    "(IllegalArgumentException). Thêm `static double average(Weather[] "
    "readings)` trả trung bình celsius của mảng khác rỗng.",
    [
        ("record equality is free", "Record so sánh theo mọi thành phần — không cần viết equals tay."),
        ("validation fires", "Compact constructor chạy ở mọi lần tạo."),
        ("average", "Trung bình trên các thành phần."),
    ],
)

P9_SET = challenge(
    "javb-m9-set-equality",
    "hashCode/equals in action",
    "Inside `Solution`, write `static java.util.HashSet<String> dedupe(java.util.List<String> "
    "words)` returning a HashSet of the distinct words. Then write `record "
    "Slug(String raw)` whose compact constructor lowercases and trims the raw "
    "value — so that `new Slug(\"  A \")` equals `new Slug(\"a\")` and both "
    "collapse to one entry in a HashSet.",
    r'''public class Solution {
    public static java.util.HashSet<String> dedupe(java.util.List<String> words) {
        return null;
    }

    public record Slug(String raw) {
        public Slug {
            // normalize raw here
        }
    }
}
''',
    [
        (
            "string dedupe",
            r"""
CjTestBase.checkEq(Solution.dedupe(java.util.List.of("a", "b", "a")).size(), 2, "two distinct");
""",
            "HashSet collapses equal values.",
        ),
        (
            "normalized record collapses",
            r"""
java.util.HashSet<Solution.Slug> set = new java.util.HashSet<>();
set.add(new Solution.Slug("  A "));
set.add(new Solution.Slug("a"));
CjTestBase.checkEq(set.size(), 1, "normalization + record equals");
""",
            "The compact constructor normalizes BEFORE equals/hashCode use it.",
        ),
    ],
    level="combination",
)

P9_SET_VI = vi_challenge(
    "hashCode/equals tại chỗ làm",
    "Bên trong `Solution`, viết `static java.util.HashSet<String> dedupe("
    "java.util.List<String> words)` trả HashSet các từ phân biệt. Sau đó "
    "viết `record Slug(String raw)` với compact constructor viết thường và "
    "trim raw — để `new Slug(\"  A \")` bằng `new Slug(\"a\")` và cả hai "
    "gộp thành một phần tử trong HashSet.",
    [
        ("string dedupe", "HashSet gộp các giá trị bằng nhau."),
        ("normalized record collapses", "Compact constructor chuẩn hóa TRƯỚC khi equals/hashCode dùng nó."),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CK_M9_MD = r'''
The Inventory Line — a modeling checkpoint.

Inside `Solution`:

1. `enum Category { FOOD, ELECTRONICS, BOOKS }`
2. `record Item(String name, int quantity, Category category)` with a
   compact constructor rejecting blank names, negative quantities, and
   null categories.
3. `static int stockValue(java.util.List<Item> items, Category c)` — the
   total quantity of items in the given category.
4. `static Item merge(Item a, Item b)` — combine two items of the SAME
   name and category into one with the summed quantity; different
   name/category → IllegalArgumentException.

The design question being tested: which type for each concept, and why
records make merge/compare trivial.
'''

CK_M9_MD_VI = r'''
Dòng tồn kho — một checkpoint về mô hình hóa.

Bên trong `Solution`:

1. `enum Category { FOOD, ELECTRONICS, BOOKS }`
2. `record Item(String name, int quantity, Category category)` với compact
   constructor từ chối tên rỗng, số lượng âm, và category null.
3. `static int stockValue(java.util.List<Item> items, Category c)` — tổng
   số lượng của các item thuộc category cho trước.
4. `static Item merge(Item a, Item b)` — gộp hai item CÙNG tên và category
   thành một với số lượng cộng lại; khác tên/category → IllegalArgumentException.

Câu hỏi thiết kế được kiểm: chọn kiểu nào cho mỗi khái niệm, và vì sao
record khiến merge/so sánh trở nên tầm thường.
'''

CK_M9_CH = challenge(
    "javb-checkpoint-modeling",
    "Checkpoint: Inventory Line",
    CK_M9_MD,
    r'''public class Solution {
    public enum Category { FOOD, ELECTRONICS, BOOKS }

    public record Item(String name, int quantity, Category category) {
        public Item {
            // validate
        }
    }

    public static int stockValue(java.util.List<Item> items, Category c) {
        return 0;
    }

    public static Item merge(Item a, Item b) {
        return a;
    }
}
''',
    [
        (
            "validation at construction",
            r"""
CjTestBase.checkThrows(() -> new Solution.Item("  ", 1, Solution.Category.FOOD), "blank name");
CjTestBase.checkThrows(() -> new Solution.Item("rice", -1, Solution.Category.FOOD), "negative qty");
""",
            "Compact constructor refuses bad data.",
        ),
        (
            "stock by category",
            r"""
java.util.List<Solution.Item> items = java.util.List.of(
    new Solution.Item("rice", 3, Solution.Category.FOOD),
    new Solution.Item("lamp", 2, Solution.Category.ELECTRONICS),
    new Solution.Item("noodles", 4, Solution.Category.FOOD));
CjTestBase.checkEq(Solution.stockValue(items, Solution.Category.FOOD), 7, "food total");
CjTestBase.checkEq(Solution.stockValue(items, Solution.Category.BOOKS), 0, "no books");
""",
            "Sum quantities filtered by category.",
        ),
        (
            "merge rules",
            r"""
Solution.Item a = new Solution.Item("rice", 3, Solution.Category.FOOD);
Solution.Item b = new Solution.Item("rice", 4, Solution.Category.FOOD);
CjTestBase.checkEq(Solution.merge(a, b).quantity(), 7, "3 + 4");
CjTestBase.checkThrows(() -> Solution.merge(a,
    new Solution.Item("lamp", 1, Solution.Category.FOOD)), "name mismatch");
""",
            "Same name+category merges; otherwise refuse.",
        ),
    ],
    difficulty="beginner",
)

CK_M9_VI = vi_challenge(
    "Checkpoint: Dòng tồn kho",
    CK_M9_MD_VI,
    [
        ("validation at construction", "Compact constructor từ chối dữ liệu xấu."),
        ("stock by category", "Cộng số lượng lọc theo category."),
        ("merge rules", "Cùng tên+category thì gộp; khác thì từ chối."),
    ],
)

CK_M9_R = r'''public class Solution {
    public enum Category { FOOD, ELECTRONICS, BOOKS }

    public record Item(String name, int quantity, Category category) {
        public Item {
            if (name == null || name.isBlank()) {
                throw new IllegalArgumentException("name required");
            }
            if (quantity < 0) {
                throw new IllegalArgumentException("quantity >= 0");
            }
            if (category == null) {
                throw new IllegalArgumentException("category required");
            }
        }
    }

    public static int stockValue(java.util.List<Item> items, Category c) {
        int total = 0;
        for (Item i : items) {
            if (i.category() == c) {
                total += i.quantity();
            }
        }
        return total;
    }

    public static Item merge(Item a, Item b) {
        if (!a.name().equals(b.name()) || a.category() != b.category()) {
            throw new IllegalArgumentException("cannot merge different items");
        }
        return new Item(a.name(), a.quantity() + b.quantity(), a.category());
    }
}
'''

CK_M9_W = r'''public class Solution {
    public enum Category { FOOD, ELECTRONICS, BOOKS }

    public record Item(String name, int quantity, Category category) {
        public Item {
            if (name == null || name.isBlank()) {
                throw new IllegalArgumentException("name required");
            }
            if (quantity < 0) {
                throw new IllegalArgumentException("quantity >= 0");
            }
            if (category == null) {
                throw new IllegalArgumentException("category required");
            }
        }
    }

    public static int stockValue(java.util.List<Item> items, Category c) {
        int total = 0;
        for (Item i : items) {
            if (i.category() == c) {
                total += i.quantity();
            }
        }
        return total;
    }

    public static Item merge(Item a, Item b) {
        // BUG: ignores the mismatch check — silently merges different items
        return new Item(a.name(), a.quantity() + b.quantity(), a.category());
    }
}
'''

# ── emit module ──────────────────────────────────────────────────────────────
write_module(
    MOD,
    "Enums, Records & Data Modeling",
    "Closed sets with enums, immutable carriers with records, the equals/hashCode contract, and choosing the right modeling tool.",
    "Enum, Record & Mô hình hóa dữ liệu",
    "Tập đóng với enum, kho dữ liệu bất biến với record, hợp đồng equals/hashCode, và chọn đúng công cụ mô hình hóa.",
    ["enums", "records", "equality-hashcode", "java-checkpoint-modeling"],
    ["javb-p9-modeling"],
)

write_lesson(
    MOD, "enums",
    "Enums: Types With a Closed Set",
    "Exhaustive switch, constants with fields, values/valueOf, and why == is safe here.", 15,
    L_ENUM_EN,
    "Enum: kiểu với tập giá trị đóng",
    "Switch đầy đủ, hằng có trường, values/valueOf, và vì sao == an toàn tại đây.",
    L_ENUM_VI,
)

write_lesson(
    MOD, "records",
    "Records: Data Without Ceremony",
    "One line, generated equals/hashCode/toString, compact constructors, and the class-vs-record decision.", 20,
    L_RECORDS_EN,
    "Record: dữ liệu không nghi thức",
    "Một dòng, equals/hashCode/toString sinh sẵn, compact constructor, và quyết định class-hay-record.",
    L_RECORDS_VI,
)

write_lesson(
    MOD, "equality-hashcode",
    "equals, hashCode & toString",
    "The two-layer equality model, the hash contract collections depend on, and the debugging value of toString.", 15,
    L_EQUALITY_EN,
    "equals, hashCode & toString",
    "Mô hình đẳng thức hai tầng, hợp đồng hash mà collection dựa vào, và giá trị gỡ lỗi của toString.",
    L_EQUALITY_VI,
)

write_practice(
    MOD, "javb-p9-modeling",
    "Practice: Modeling Data",
    "A state-machine enum, a validated record, and normalization collapsing in a HashSet.",
    "Thực hành: Mô hình hóa dữ liệu",
    "Một enum máy trạng thái, một record có xác thực, và chuẩn hóa gộp trong HashSet.",
    "records", 45, "beginner",
    [P9_STATUS, P9_RECORD, P9_SET],
    {c["id"]: v for c, v in [(P9_STATUS, P9_STATUS_VI), (P9_RECORD, P9_RECORD_VI), (P9_SET, P9_SET_VI)]},
    solutions=[
        (
            P9_STATUS["id"],
            r'''public class Solution {
    public enum OrderStatus { PENDING, PAID, SHIPPED, CANCELLED }

    public static boolean canCancel(OrderStatus s) {
        return s == OrderStatus.PENDING || s == OrderStatus.PAID;
    }

    public static OrderStatus next(OrderStatus s) {
        return switch (s) {
            case PENDING -> OrderStatus.PAID;
            case PAID -> OrderStatus.SHIPPED;
            default -> s;
        };
    }
}
''',
            r'''public class Solution {
    public enum OrderStatus { PENDING, PAID, SHIPPED, CANCELLED }

    public static boolean canCancel(OrderStatus s) {
        // BUG: shipped cancellable too
        return s != OrderStatus.CANCELLED;
    }

    public static OrderStatus next(OrderStatus s) {
        return switch (s) {
            case PENDING -> OrderStatus.PAID;
            case PAID -> OrderStatus.SHIPPED;
            default -> s;
        };
    }
}
''',
        ),
        (
            P9_RECORD["id"],
            r'''public class Solution {
    public record Weather(String city, double celsius) {
        public Weather {
            if (city == null || city.isBlank()) {
                throw new IllegalArgumentException("city required");
            }
            if (celsius < -273.15) {
                throw new IllegalArgumentException("below absolute zero");
            }
        }
    }

    public static double average(Weather[] readings) {
        double sum = 0;
        for (Weather w : readings) {
            sum += w.celsius();
        }
        return sum / readings.length;
    }
}
''',
            r'''public class Solution {
    public record Weather(String city, double celsius) {
        public Weather {
            // BUG: blank city slips through (== null only)
            if (city == null) {
                throw new IllegalArgumentException("city required");
            }
            if (celsius < -273.15) {
                throw new IllegalArgumentException("below absolute zero");
            }
        }
    }

    public static double average(Weather[] readings) {
        double sum = 0;
        for (Weather w : readings) {
            sum += w.celsius();
        }
        return sum / readings.length;
    }
}
''',
        ),
        (
            P9_SET["id"],
            r'''public class Solution {
    public static java.util.HashSet<String> dedupe(java.util.List<String> words) {
        return new java.util.HashSet<>(words);
    }

    public record Slug(String raw) {
        public Slug {
            raw = raw == null ? "" : raw.trim().toLowerCase();
        }
    }
}
''',
            r'''public class Solution {
    public static java.util.HashSet<String> dedupe(java.util.List<String> words) {
        return new java.util.HashSet<>(words);
    }

    public record Slug(String raw) {
        public Slug {
            // BUG: normalizes a LOCAL copy, not the component — equals still raw
            String clean = raw == null ? "" : raw.trim().toLowerCase();
        }
    }
}
''',
        ),
    ],
)

write_checkpoint(
    MOD, "java-checkpoint-modeling",
    "Checkpoint: Inventory Line",
    "An enum, a validated record, category stock totals, and guarded merging — modeling decisions with teeth.", 45, CK_M9_MD,
    "Checkpoint: Dòng tồn kho",
    "Một enum, một record có xác thực, tổng tồn theo category, và gộp có kiểm soát — quyết định mô hình hóa có răng.",
    CK_M9_MD_VI,
    CK_M9_CH, CK_M9_VI,
    solution=CK_M9_R, wrong=CK_M9_W,
)

print("module 9 complete")
