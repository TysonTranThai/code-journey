#!/usr/bin/env python3
"""Java — Advanced — Module 1: java-object-model.

Opens the course where Intermediate's contracts module ended and goes under
the surface: class-vs-instance initialization order (JLS §12.2–12.4,
executed and observed), records/sealed types as design tools (JEP 395/409,
final in 21), and identity/aliasing discipline at scale. House conventions:
raw triple-quoted Java strings, self-contained tests, Solution-qualified
refs, explicit CjTestBase messages, behavioral near-miss Ws.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javaa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

M = "java-object-model"

# ── lesson 1.1 — initialization order, executed ──────────────────────────────
L_INIT_EN = """
You already know constructors from Intermediate. Advanced Java asks a sharper
question: **in what exact order does anything initialize at all?** The rules
(JLS §12.2–12.4) are mechanical, and you can observe every one of them:

1. **Static** fields and `static {}` blocks of a class run **once**, in source
   order, at class initialization (first active use).
2. **Instance** field initializers and instance initializer blocks run **every
   time an object is created**, in source order, *before* the constructor body.
3. `super(...)` runs before the subclass's field initializers — so a superclass
   constructor that calls an overridable method sees **subclass fields still
   null/0**. This is the classic initialization trap.
4. `final` fields must be definitely assigned by the end of every constructor.

```java
class Base {
    Base() { log("Base ctor"); }
}
class Derived extends Base {
    static String S = log("Derived static");
    int x = log("Derived field");
    Derived() { super(); log("Derived ctor"); }
}
// new Derived() prints: Derived static → Base ctor → Derived field → Derived ctor
```

The dangerous case is **virtual calls from constructors**. A superclass
constructor that calls an overridden method runs the override before subclass
fields exist. Effective Java Item 19: *constructors must not invoke overridable
methods, directly or indirectly.* When you need shared setup, prefer a static
factory that wires fully-constructed objects.
"""
L_INIT_VI = """
Bạn đã biết constructor từ Trung cấp. Java Nâng cao hỏi câu sắc hơn: **cái gì
khởi tạo trước, theo đúng thứ tự nào?** Quy tắc (JLS §12.2–12.4) là cơ học và
bạn có thể quan sát tất cả:

1. Trường **static** và khối `static {}` chạy **một lần**, theo thứ tự khai
   báo, khi lớp được khởi tạo lần đầu (lần dùng "thật" đầu tiên).
2. Trường instance và khối khởi tạo instance chạy **mỗi lần tạo đối tượng**,
   theo thứ tự khai báo, *trước* thân constructor.
3. `super(...)` chạy trước các initializer của lớp con — nên constructor lớp
   cha gọi phương thức overridable sẽ thấy **trường lớp con vẫn null/0**.
   Đây là bẫy khởi tạo kinh điển.
4. Trường `final` phải được gán chắc chắn trước khi mọi constructor kết thúc.

```java
class Base {
    Base() { log("Base ctor"); }
}
class Derived extends Base {
    static String S = log("Derived static");
    int x = log("Derived field");
    Derived() { super(); log("Derived ctor"); }
}
// new Derived() in ra: Derived static → Base ctor → Derived field → Derived ctor
```

Trường hợp nguy hiểm là **gọi phương thức virtual trong constructor**.
Constructor lớp cha gọi phương thức bị override sẽ chạy bản override trước khi
trường lớp con tồn tại. Effective Java Item 19: *constructor không được gọi
phương thức overridable, trực tiếp hay gián tiếp.* Khi cần setup chung, hãy
dùng static factory ghép các đối tượng đã dựng xong.
"""

# ── lesson 1.2 — records & sealed as design tools ────────────────────────────
L_RECORDS_EN = """
Intermediate treated records as "immutable data classes." Advanced treats
them as **algebraic design tools**.

**Records** (JEP 395, final in 21) are transparent carriers: final fields,
accessors named like the components, generated `equals`/`hashCode`/`toString`.
Design rule: a record *is* its data — if you find yourself hiding or mutating
component state, it should not be a record. Validation belongs in the
**compact constructor**:

```java
public record Price(int cents) {
    public Price {                      // compact ctor: fields not yet assigned
        if (cents < 0) throw new IllegalArgumentException("negative price");
    }
}
```

**Sealed classes** (JEP 409, final in 21) let a type *own its hierarchy*:

```java
public sealed interface Shape permits Circle, Rect {}
public record Circle(double r) implements Shape {}
public record Rect(double w, double h) implements Shape {}
```

Together with **pattern matching for switch** (JEP 441, final in 21) this
gives you *exhaustive* dispatch: the compiler refuses to compile a switch
over a sealed type that misses a case — so adding a new variant becomes a
*compile-time-guided* change, not a runtime hunt for forgotten `else` branches.

```java
double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.r() * c.r();
        case Rect r   -> r.w() * r.h();
    }; // no default: compiler enforces exhaustiveness
}
```

When *not* to seal: hierarchies designed for third-party extension (plugins,
SPIs) must stay open. Sealing is a contract with your callers, not a style.
"""
L_RECORDS_VI = """
Ở Trung cấp, record chỉ là "lớp dữ liệu bất biến." Ở Nâng cao, chúng là
**công cụ thiết kế đại số**.

**Record** (JEP 395, final từ 21) là carrier minh bạch: trường final, accessor
trùng tên component, sinh sẵn `equals`/`hashCode`/`toString`. Quy tắc thiết
kế: record *là* dữ liệu của nó — nếu bạn thấy mình đang giấu hoặc làm biến đổi
trạng thái component thì nó không nên là record. Validation đặt trong
**compact constructor**:

```java
public record Price(int cents) {
    public Price {                      // compact ctor: trường chưa được gán
        if (cents < 0) throw new IllegalArgumentException("negative price");
    }
}
```

**Sealed class** (JEP 409, final từ 21) cho phép một kiểu *sở hữu hệ thống
phân cấp của nó*:

```java
public sealed interface Shape permits Circle, Rect {}
public record Circle(double r) implements Shape {}
public record Rect(double w, double h) implements Shape {}
```

Kết hợp với **pattern matching cho switch** (JEP 441, final từ 21), bạn có
dispatch *đầy đủ*: compiler từ chối biên dịch switch thiếu case — nên thêm
variant mới trở thành thay đổi *được compiler dẫn đường*, không phải truy lùng
`else` bị quên lúc chạy.

```java
double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.r() * c.r();
        case Rect r   -> r.w() * r.h();
    }; // không default: compiler ép đủ case
}
```

Khi *không* nên seal: hệ phân cấp cho bên thứ ba mở rộng (plugin, SPI) phải
mở. Sealing là hợp đồng với người gọi, không phải phong cách.
"""

# ── lesson 1.3 — identity & aliasing at scale ────────────────────────────────
L_ALIAS_EN = """
Intermediate covered equals/hashCode. The Advanced discipline is **aliasing
control** — knowing exactly how many references point at a mutable object and
making illegal aliasing impossible to express:

- **Identity vs equality, deliberately**: `==` asks "same object?", `equals`
  asks "same value?". Collections, caches, and locks all have opinions about
  which one they use — `IdentityHashMap` exists precisely because sometimes
  identity *is* the semantics.
- **Defensive copies at the boundary**: a constructor taking a mutable
  collection should copy it (`List.copyOf(in)`); an accessor exposing internal
  state should hand out an unmodifiable view or a copy. Intermediate taught
  the *what*; here the rule is *every boundary, every time*.
- **Immutability as the default answer**: an immutable type cannot have
  aliasing bugs, is safe to share across threads without synchronization, and
  makes honest cache keys. Prefer records + `List.copyOf` + final fields.
- **Escape analysis starts in your head**: returning `this` from a
  constructor, registering `this` with a listener before construction
  finishes, or storing an internal array in a public field — each is an
  object *escaping* before it is safe.

The operational payoff: objects that never mutate after construction need no
defensive synchronization anywhere in the program.
"""
L_ALIAS_VI = """
Trung cấp đã học equals/hashCode. Kỷ luật Nâng cao là **kiểm soát aliasing**
— biết chính xác có bao nhiêu tham chiếu trỏ vào một đối tượng mutable và
không thể hiện được aliasing trái phép:

- **Identity so với equality, có chủ đích**: `==` hỏi "cùng đối tượng?",
  `equals` hỏi "cùng giá trị?". Collection, cache, và lock đều có quan điểm
  riêng — `IdentityHashMap` tồn tại vì đôi khi identity *chính là* ngữ nghĩa.
- **Bản sao phòng thủ ở ranh giới**: constructor nhận collection mutable nên
  sao chép (`List.copyOf(in)`); accessor exposing trạng thái nội bộ nên trả
  view bất biến hoặc bản sao. Trung cấp dạy *cái gì*; ở đây quy tắc là *mọi
  ranh giới, mọi lần*.
- **Bất biến là câu trả lời mặc định**: kiểu bất biến không có bug aliasing,
  chia sẻ giữa các thread mà không cần đồng bộ, và là cache key trung thực.
  Ưu tiên record + `List.copyOf` + trường final.
- **Escape analysis bắt đầu từ đầu bạn**: trả `this` từ constructor, đăng ký
  `this` với listener trước khi dựng xong, hay để trường public trỏ mảng nội
  bộ — đều là đối tượng *thoát ra* trước khi an toàn.

Lợi ích vận hành: đối tượng không bao giờ biến đổi sau khi dựng thì không cần
phòng thủ đồng bộ ở bất kỳ đâu trong chương trình.
"""

# ── module ────────────────────────────────────────────────────────────────────
write_module(
    M, "The Advanced Object Model",
    "Initialization order observed, records/sealed as algebraic design tools, and aliasing control at every boundary.",
    "Mô hình đối tượng nâng cao",
    "Quan sát thứ tự khởi tạo, record/sealed như công cụ thiết kế đại số, và kiểm soát aliasing ở mọi ranh giới.",
    ["javaa-init-order", "javaa-records-sealed", "javaa-aliasing"],
    ["javaa-p1-model"],
)

write_lesson(M, "javaa-init-order",
    "Initialization order, executed",
    "Static vs instance init, super-first rules, and why constructors must not call overridable methods.",
    14, L_INIT_EN,
    "Thứ tự khởi tạo, chạy thử được",
    "Static so với instance init, quy tắc super-trước, và vì sao constructor không được gọi phương thức overridable.",
    L_INIT_VI)

write_lesson(M, "javaa-records-sealed",
    "Records and sealed hierarchies as design tools",
    "Compact constructors, exhaustive pattern switches, and when NOT to seal a hierarchy.",
    15, L_RECORDS_EN,
    "Record và sealed hierarchy như công cụ thiết kế",
    "Compact constructor, switch pattern đầy đủ, và khi nào KHÔNG nên seal hệ phân cấp.",
    L_RECORDS_VI)

write_lesson(M, "javaa-aliasing",
    "Identity, aliasing, and escape discipline",
    "Defensive copies at every boundary, immutability as default, and when identity is the semantics.",
    14, L_ALIAS_EN,
    "Identity, aliasing, và kỷ luật escape",
    "Bản sao phòng thủ ở mọi ranh giới, bất biến là mặc định, và khi nào identity là ngữ nghĩa.",
    L_ALIAS_VI)

# ── practice set ──────────────────────────────────────────────────────────────
P_BOILER = r"""
public class Solution {
    // Your implementation goes here.
}
"""

CH_INIT = challenge(
    "javaa-p1-init-order",
    "Predict the initialization sequence",
    "Implement `static List<String> trace()` that returns the exact observable "
    "initialization order for `new Derived()` in this class family:\n"
    "1. `class Base { Base() { t(\"Base ctor\"); } }` where `t` records into the trace.\n"
    "2. `class Derived extends Base { static String S = t(\"D static\"); int x = t(\"D field\"); "
    "Derived() { t(\"D ctor\"); } }`\n"
    "Rules: `t` appends to a shared list and returns its argument. `trace()` creates one "
    "`Derived` and returns the recorded list. Static init happens at first active use — "
    "instantiation counts.",
    P_BOILER,
    [
        ("initialization order is exact", r"""
List<String> expected = List.of("D static", "Base ctor", "D field", "D ctor");
checkEq(Solution.trace(), expected, "trace matches JLS 12.4 order");
""", "super() runs before subclass field initializers; static runs once at first use."),
        ("second instance skips static", r"""
Solution.trace();
List<String> second = List.of("Base ctor", "D field", "D ctor");
checkEq(Solution.trace(), second, "static block does not rerun");
""", "Class initialization happens once per class, not per instance."),
    ],
    level="guided",
)
CH_INIT_VI = vi_challenge(
    "Dự đoán thứ tự khởi tạo",
    "Cài `static List<String> trace()` trả về đúng thứ tự khởi tạo quan sát được cho "
    "`new Derived()` theo mô tả trong bản tiếng Anh.",
    [("Thứ tự khởi tạo chính xác", "super() chạy trước initializer trường lớp con; static chạy một lần."),
     ("Instance thứ hai bỏ qua static", "Khởi tạo lớp chỉ xảy ra một lần mỗi lớp.")],
)

CH_RECORD = challenge(
    "javaa-p1-exhaustive-shapes",
    "Sealed hierarchy with exhaustive dispatch",
    "Given `sealed interface Shape permits Circle, Rect`, implement:\n"
    "1. `record Circle(double r) implements Shape` and `record Rect(double w, double h) implements Shape`\n"
    "2. `static double area(Shape s)` using a pattern switch with NO default clause\n"
    "3. `record Box(Shape shape)` — a record *containing* a sealed type\n"
    "The switch must stay exhaustive: the compiler must guarantee that adding a new Shape "
    "variant breaks compilation until `area` handles it.",
    P_BOILER,
    [
        ("areas compute", r"""
checkNear(Solution.area(new Solution.Circle(2.0)), Math.PI * 4, 1e-9, "circle area");
checkNear(Solution.area(new Solution.Rect(3.0, 4.0)), 12.0, 1e-9, "rect area");
""", "Use Math.PI * r * r and w * h."),
        ("nested record holds shapes", r"""
Solution.Box b = new Solution.Box(new Solution.Circle(1.0));
checkTrue(b.shape() instanceof Solution.Circle, "box wraps a Circle");
""", "A record component can itself be a sealed type."),
        ("scale invariance", r"""
checkNear(Solution.area(new Solution.Rect(2.0, 8.0)), Solution.area(new Solution.Rect(8.0, 2.0)), 1e-9,
    "area is orientation-independent");
""", "w*h == h*w."),
    ],
    level="independent",
)
CH_RECORD_VI = vi_challenge(
    "Hệ phân cấp sealed với dispatch đầy đủ",
    "Cài Shape sealed, Circle/Rect record, `area` bằng pattern switch không default, và Box record chứa Shape.",
    [("Tính diện tích", "Dùng Math.PI * r * r và w * h."),
     ("Record lồng chứa shape", "Component của record có thể là kiểu sealed."),
     ("Bất biến theo tỷ lệ", "w*h == h*w.")],
)

CH_ALIAS = challenge(
    "javaa-p1-alias-proof",
    "Make the aliasing bug impossible",
    "A `Team` object was leaking its internal roster. Implement a leak-proof version:\n"
    "1. `static final class Team` with a `List<String> members` field\n"
    "2. Constructor takes `List<String> initial` and defensively copies it\n"
    "3. `add(String m)` appends; `members()` returns an UNMODIFIABLE view\n"
    "4. `static List<String> freeze(List<String> src)` returns a copy that the caller "
    "can then mutate without ever affecting any Team\n"
    "Tests attempt both leak directions: outside-in (mutating the list after the ctor) "
    "and inside-out (mutating the returned view).",
    P_BOILER,
    [
        ("outside-in blocked", r"""
java.util.List<String> ext = new java.util.ArrayList<>(List.of("a"));
Solution.Team t = new Solution.Team(ext);
ext.add("hacker");
checkEq(t.members(), List.of("a"), "post-ctor mutation must not leak in");
""", "Copy in the constructor: List.copyOf(ext)."),
        ("inside-out blocked", r"""
Solution.Team t = new Solution.Team(List.of("a"));
try {
    t.members().add("hacker");
    checkTrue(false, "view must be unmodifiable");
} catch (UnsupportedOperationException e) {
    checkTrue(true, "mutation correctly rejected");
}
""", "Return List.copyOf(members) or Collections.unmodifiableList."),
        ("freeze is a true copy", r"""
java.util.List<String> src = new java.util.ArrayList<>(List.of("x"));
java.util.List<String> f = Solution.freeze(src);
src.add("y");
checkEq(f, List.of("x"), "freeze snapshots");
""", "freeze must copy, not wrap."),
    ],
    level="independent",
)
CH_ALIAS_VI = vi_challenge(
    "Làm bug aliasing không thể xảy ra",
    "Cài Team chặn rò rỉ theo cả hai hướng: list truyền vào biến đổi sau ctor, và view trả ra bị biến đổi.",
    [("Chặn leak từ ngoài vào", "Sao chép trong constructor: List.copyOf."),
     ("Chặn leak từ trong ra", "Trả view bất biến — mutation phải ném UnsupportedOperationException."),
     ("freeze là bản sao thật", "freeze phải sao chép, không phải bọc.")],
)

write_practice(M, "javaa-p1-model",
    "Object model drills",
    "Trace initialization by execution, design exhaustive sealed dispatch, and seal every aliasing leak.",
    "Bài tập mô hình đối tượng",
    "Truy vết khởi tạo bằng thực thi, thiết kế sealed dispatch đầy đủ, và bịt mọi điểm rò rỉ aliasing.",
    "javaa-aliasing", 45, "advanced",
    [CH_INIT, CH_RECORD, CH_ALIAS],
    {"javaa-p1-init-order": CH_INIT_VI, "javaa-p1-exhaustive-shapes": CH_RECORD_VI, "javaa-p1-alias-proof": CH_ALIAS_VI},
    solutions=[
        ("javaa-p1-init-order", r"""
import java.util.*;

public class Solution {
    static final List<String> TRACE = new ArrayList<>();
    static String t(String s) { TRACE.add(s); return s; }

    public static class Base { Base() { t("Base ctor"); } }
    public static class Derived extends Base {
        static String S = t("D static");
        String x = t("D field");
        Derived() { t("D ctor"); }
    }

    public static List<String> trace() {
        TRACE.clear();
        new Derived();
        return List.copyOf(TRACE);
    }
}
""", r"""
import java.util.*;

public class Solution {
    static final List<String> TRACE = new ArrayList<>();
    static String t(String s) { TRACE.add(s); return s; }

    public static class Base { Base() { t("Base ctor"); } }
    public static class Derived extends Base {
        static String S = t("D static");
        String x = t("D field");
        Derived() { t("D field"); t("D ctor"); t("Base ctor"); }  // WRONG: order scrambled
    }

    public static List<String> trace() {
        TRACE.clear();
        new Derived();
        return List.copyOf(TRACE);
    }
}
"""),
        ("javaa-p1-exhaustive-shapes", r"""
public class Solution {
    public sealed interface Shape permits Circle, Rect {}
    public record Circle(double r) implements Shape {}
    public record Rect(double w, double h) implements Shape {}
    public record Box(Shape shape) {}

    public static double area(Shape s) {
        return switch (s) {
            case Circle c -> Math.PI * c.r() * c.r();
            case Rect r -> r.w() * r.h();
        };
    }
}
""", r"""
public class Solution {
    public sealed interface Shape permits Circle, Rect {}
    public record Circle(double r) implements Shape {}
    public record Rect(double w, double h) implements Shape {}
    public record Box(Shape shape) {}

    public static double area(Shape s) {
        return switch (s) {
            case Circle c -> Math.PI * c.r() * c.r();
            case Rect r -> r.w() + r.h();   // WRONG: sum instead of product
        };
    }
}
"""),
        ("javaa-p1-alias-proof", r"""
import java.util.*;

public class Solution {
    public static final class Team {
        private final List<String> members;
        public Team(List<String> initial) { this.members = new ArrayList<>(List.copyOf(initial)); }
        public void add(String m) { members.add(m); }
        public List<String> members() { return List.copyOf(members); }
    }
    public static List<String> freeze(List<String> src) { return new ArrayList<>(List.copyOf(src)); }
}
""", r"""
import java.util.*;

public class Solution {
    public static final class Team {
        private final List<String> members;
        public Team(List<String> initial) { this.members = initial; }   // WRONG: aliases caller's list
        public void add(String m) { members.add(m); }
        public List<String> members() { return members; }               // WRONG: leaks internals
    }
    public static List<String> freeze(List<String> src) { return List.copyOf(src); }
}
"""),
    ],
)

# ── checkpoint ────────────────────────────────────────────────────────────────
CP_MD = """
## Checkpoint: the object model under pressure

A `Session` object must survive three hostile reviewers: one mutates the list
it passed to the constructor, one mutates what your accessor returns, and one
constructs the object from a superclass constructor that calls an overridable
`describe()` method.

Build the class that survives all three — initialization-safe, alias-proof,
and immutable-friendly.
"""

CP_CH = challenge(
    "javaa-checkpoint-m1-task",
    "Checkpoint: the hostile-reviewer Session",
    "Implement `static final class Session` + helper:\n"
    "1. Constructor `Session(List<String> events)` — defensively copies.\n"
    "2. `events()` returns an unmodifiable view; `add(String e)` mutates internal state only.\n"
    "3. `String describe()` returns `\"Session[n]\"` with n = current event count.\n"
    "4. `static String safeTrace()` — creates a Session from a mutable list, "
    "mutates that external list afterwards, then returns the Session's `describe()` value.\n"
    "The tests simulate all three hostile reviewers.",
    P_BOILER,
    [
        ("survives outside-in mutation", r"""
java.util.List<String> ext = new java.util.ArrayList<>(List.of("e1"));
Solution.Session s = new Solution.Session(ext);
ext.add("injected");
checkEq(s.describe(), "Session[1]", "external mutation ignored");
""", "Copy the list in the constructor."),
        ("survives inside-out mutation", r"""
Solution.Session s = new Solution.Session(List.of("e1"));
try { s.events().add("injected"); checkTrue(false, "must reject"); }
catch (UnsupportedOperationException e) { checkTrue(true, "rejected"); }
""", "Expose List.copyOf(events)."),
        ("describe tracks internal adds", r"""
Solution.Session s = new Solution.Session(List.of());
s.add("a"); s.add("b");
checkEq(s.describe(), "Session[2]", "internal adds counted");
""", "describe reads the internal list size."),
        ("safeTrace immune to post-ctor edits", r"""
checkEq(Solution.safeTrace(), "Session[1]", "snapshot taken at construction");
""", "safeTrace must copy before the external list is mutated."),
    ],
    level="real-world",
)
CP_CH_VI = vi_challenge(
    "Checkpoint: Session trước reviewer thù địch",
    "Cài Session chống cả ba hướng tấn công: list truyền vào, view trả ra, và mô tả sau khi external list đổi.",
    [("Chặn mutation ngoài-vào", "Sao chép list trong constructor."),
     ("Chặn mutation trong-ra", "Trả view bất biến."),
     ("describe đếm add nội bộ", "describe đọc size list nội bộ."),
     ("safeTrace miễn nhiễm", "Chụp bản sao trước khi list ngoài biến đổi.")],
)

write_checkpoint(M, "javaa-checkpoint-m1",
    "Checkpoint: Hostile-Reviewer Session",
    "Build a Session that survives constructor-time, accessor-time, and external mutation attacks.",
    20, CP_MD,
    "Checkpoint: Session trước reviewer thù địch",
    "Xây Session sống sót qua ba kiểu tấn công mutation ở constructor, accessor, và bên ngoài.",
    CP_MD,
    CP_CH, CP_CH_VI,
    solution=r"""
import java.util.*;

public class Solution {
    public static final class Session {
        private final List<String> events;
        public Session(List<String> initial) { this.events = new ArrayList<>(List.copyOf(initial)); }
        public void add(String e) { events.add(e); }
        public List<String> events() { return List.copyOf(events); }
        public String describe() { return "Session[" + events.size() + "]"; }
    }
    public static String safeTrace() {
        List<String> ext = new ArrayList<>(List.of("e1"));
        Session s = new Session(ext);
        ext.add("injected");
        return s.describe();
    }
}
""", wrong=r"""
import java.util.*;

public class Solution {
    public static final class Session {
        private final List<String> events;
        public Session(List<String> initial) { this.events = initial; }   // WRONG: no copy
        public void add(String e) { events.add(e); }
        public List<String> events() { return events; }                    // WRONG: leaks
        public String describe() { return "Session[" + events.size() + "]"; }
    }
    public static String safeTrace() {
        List<String> ext = new ArrayList<>(List.of("e1"));
        Session s = new Session(ext);
        ext.add("injected");
        return s.describe();
    }
}
""")

print("module 1 authored")
