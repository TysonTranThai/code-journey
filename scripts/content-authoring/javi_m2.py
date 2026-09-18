#!/usr/bin/env python3
"""Java — Intermediate — Module 2: java-oop-solid.

From "can use an interface" to "designs with interfaces": programming to
contracts, sealed hierarchies with pattern matching, and dependency
inversion done by hand (constructor injection). Payment-processing is the
running example. House conventions: Solution-qualified test refs, explicit
CjTestBase messages, Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-oop-solid"

# ── lesson 2.1 — design to contracts ────────────────────────────────────────
L_CONTRACTS_EN = r"""
## Design to contracts

An interface is a *promise* callers can rely on and implementations can
swap. The intermediate skill is choosing what belongs in the promise:

```java
public interface PaymentGateway {
    PaymentResult charge(Money amount, Card card);
}
```

High-level code (checkout) should depend on `PaymentGateway`, not on
`StripeGateway`. That is the Dependency Inversion Principle in one line:
**details depend on abstractions, never the reverse.**

```java
public final class CheckoutService {
    private final PaymentGateway gateway;
    public CheckoutService(PaymentGateway gateway) {   // injected
        this.gateway = gateway;
    }
    public PaymentResult checkout(Order order) {
        return gateway.charge(order.total(), order.card());
    }
}
```

Why this pays off:
- tests swap in a fake gateway — no network, no secrets
- adding PayPal means writing a new class, not editing checkout
- the interface documents the *only* methods checkout actually needs
  (interface segregation: small promises beat fat ones)
"""

L_CONTRACTS_VI = r"""
## Thiết kế theo hợp đồng

Interface là một *lời hứa* mà caller có thể dựa vào và các hiện thực có thể
hoán đổi cho nhau. Kỹ năng trung cấp là chọn cái gì nằm trong lời hứa:

```java
public interface PaymentGateway {
    PaymentResult charge(Money amount, Card card);
}
```

Code cấp cao (checkout) nên phụ thuộc `PaymentGateway`, không phụ thuộc
`StripeGateway`. Đó là Dependency Inversion Principle gói trong một dòng:
**detail phụ thuộc abstraction, không bao giờ ngược lại.**

```java
public final class CheckoutService {
    private final PaymentGateway gateway;
    public CheckoutService(PaymentGateway gateway) {   // tiêm vào
        this.gateway = gateway;
    }
    public PaymentResult checkout(Order order) {
        return gateway.charge(order.total(), order.card());
    }
}
```

Vì sao đáng giá:
- test thay fake gateway — không mạng, không secret
- thêm PayPal nghĩa là viết class mới, không phải sửa checkout
- interface tài liệu hóa *chỉ những* method mà checkout thực sự cần
  (interface segregation: lời hứa nhỏ tốt hơn lời hứa mập)
"""

# ── lesson 2.2 — sealed hierarchies ─────────────────────────────────────────
L_SEALED_EN = r"""
## Sealed hierarchies and exhaustive switches

Before sealed classes, an interface had unbounded implementations, so a
switch over its subtypes always needed a `default`. Sealed interfaces make
the set of implementations finite and compiler-checked:

```java
public sealed interface Shape permits Circle, Rect {}
public record Circle(double r) implements Shape {}
public record Rect(double w, double h) implements Shape {}

static double area(Shape s) {
    return switch (s) {                 // pattern matching for switch
        case Circle c -> Math.PI * c.r() * c.r();
        case Rect r  -> r.w() * r.h();
    };                                  // no default — compiler knows all cases
}
```

Add a third permit without updating the switch and the code **does not
compile** — the compiler turns a forgotten case into a build error instead
of a runtime surprise.

Choose sealed when the set of variants is *your* domain decision (shapes,
payment methods, parse results). Keep interfaces open when third parties
should be able to plug in.
"""

L_SEALED_VI = r"""
## Sealed hierarchy và switch đầy đủ

Trước sealed class, một interface có vô số hiện thực, nên switch qua các
subtype luôn cần `default`. Sealed interface khiến tập hiện thực hữu hạn và
được compiler kiểm tra:

```java
public sealed interface Shape permits Circle, Rect {}
public record Circle(double r) implements Shape {}
public record Rect(double w, double h) implements Shape {}

static double area(Shape s) {
    return switch (s) {                 // pattern matching cho switch
        case Circle c -> Math.PI * c.r() * c.r();
        case Rect r  -> r.w() * r.h();
    };                                  // không default — compiler biết hết case
}
```

Thêm permit thứ ba mà không sửa switch thì code **không biên dịch** —
compiler biến case bị quên thành lỗi build thay vì sự cố runtime.

Chọn sealed khi tập biến thể là *quyết định domain* của bạn (shape, phương
thức thanh toán, kết quả parse). Giữ interface mở khi bên thứ ba cần cắm vào
được.
"""

# ── lesson 2.3 — composition & delegation ───────────────────────────────────
L_COMP_EN = r"""
## Composition, inheritance, and delegation

Inheritance is the strongest coupling Java offers: the subclass depends on
superclass internals and survives every superclass change. Prefer
**composition**: hold a collaborator and *delegate*.

```java
// inheritance-flavored
class CountingList extends ArrayList<String> {
    int count = 0;
    @Override public boolean add(String s) { count++; return super.add(s); }
    // broken: addAll() bypasses add(), remove() desyncs count...
}

// composition-flavored
final class CountingList {
    private final List<String> inner = new ArrayList<>();
    int count = 0;
    void add(String s) { count++; inner.add(s); }
    int size() { return inner.size(); }
}
```

The inheritance version inherits behavior it never asked for (addAll skips
the override — a classic bug). The composition version exposes exactly the
surface it wants, and counting cannot desync.

Rule of thumb: `is-a` that survives every future change → inheritance.
`has-a`, wrapping, decorating, adapting → composition. When in doubt,
compose and delegate.
"""

L_COMP_VI = r"""
## Composition, kế thừa, và delegation

Kế thừa là mức khớp nối mạnh nhất của Java: subclass phụ thuộc nội bộ của
superclass và phải sống sót qua mọi thay đổi của superclass. Ưu tiên
**composition**: giữ một cộng sự viên và *ủy quyền* (delegate).

```java
// kiểu kế thừa
class CountingList extends ArrayList<String> {
    int count = 0;
    @Override public boolean add(String s) { count++; return super.add(s); }
    // hỏng: addAll() đi vòng qua add(), remove() làm count lệch...
}

// kiểu composition
final class CountingList {
    private final List<String> inner = new ArrayList<>();
    int count = 0;
    void add(String s) { count++; inner.add(s); }
    int size() { return inner.size(); }
}
```

Bản kế thừa thừa hưởng hành vi nó không hề xin (addAll bỏ qua override —
một bug kinh điển). Bản composition chỉ lộ đúng bề mặt nó muốn, và phép
đếm không thể lệch.

Kinh nghiệm: `is-a` còn đúng sau mọi thay đổi tương lai → kế thừa.
`has-a`, bọc, trang trí, chuyển đổi → composition. Khi phân vân, compose
và delegate.
"""

write_module(
    MOD,
    "Object-Oriented Design & Dependency Inversion",
    "Design with contracts: injected dependencies, sealed hierarchies with exhaustive switches, and composition over inheritance.",
    "Thiết kế hướng đối tượng & Dependency Inversion",
    "Thiết kế theo hợp đồng: tiêm phụ thuộc, sealed hierarchy với switch đầy đủ, và composition hơn kế thừa.",
    ["design-to-contracts", "sealed-hierarchies", "composition-delegation", "javi-checkpoint-oop"],
    ["javi-p2-design"],
)

write_lesson(MOD, "design-to-contracts", "Design to Contracts", "Programming to interfaces with constructor injection: the one-line DIP, and why small promises beat fat ones.", 14, L_CONTRACTS_EN, "Thiết kế theo hợp đồng", "Lập trình theo interface với constructor injection: DIP trong một dòng, và vì sao lời hứa nhỏ hơn thắng lời hứa mập.", L_CONTRACTS_VI)

write_lesson(MOD, "sealed-hierarchies", "Sealed Hierarchies & Exhaustive Switches", "Making the variant set finite so the compiler turns forgotten cases into build errors.", 13, L_SEALED_EN, "Sealed hierarchy & switch đầy đủ", "Khiến tập biến thể hữu hạn để compiler biến case bị quên thành lỗi build.", L_SEALED_VI)

write_lesson(MOD, "composition-delegation", "Composition, Inheritance & Delegation", "Why addAll bypasses your override, and how composition with delegation sidesteps fragile base classes.", 14, L_COMP_EN, "Composition, kế thừa & delegation", "Vì sao addAll đi vòng qua override của bạn, và cách composition với delegation né base class mong manh.", L_COMP_VI)

# ── practice set ─────────────────────────────────────────────────────────────
P2_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P2_GATEWAY = challenge(
    "javi-p2-payment-gateway",
    "Inject the Payment Gateway",
    r"""Design a checkout flow around a contract:
- `interface PaymentGateway { String charge(int cents); }` inside `Solution`
  — returns a receipt id like `"ok-1000"`.
- `static class CheckoutService` with a constructor taking a
  `PaymentGateway` and a method `static String checkout(PaymentGateway g, int cents)`
  that delegates to the gateway and returns its result.
- Implement `static class FakeGateway implements PaymentGateway` that
  returns `"ok-" + cents` — the test double the service will run against.

The tests run the service against the fake (never a real payment API):
this is dependency inversion exercised by hand.""",
    P2_BOILER,
    [
        (
            "service delegates to injected gateway",
            r"""
Solution.PaymentGateway gw = new Solution.FakeGateway();
checkEq(Solution.checkout(gw, 2500), "ok-2500", "delegation result");
""",
            "checkout must call gateway.charge and return its value unchanged.",
        ),
        (
            "fake is a real implementation of the contract",
            r"""
Solution.PaymentGateway gw = new Solution.FakeGateway();
checkEq(gw.charge(99), "ok-99", "fake implements interface");
""",
            "FakeGateway must implement PaymentGateway.charge(int).",
        ),
        (
            "service uses WHATEVER gateway is injected",
            r"""
Solution.PaymentGateway alt = c -> "off-" + c;   // a different gateway
checkEq(Solution.checkout(alt, 250), "off-250", "delegation, not hard-coding");
""",
            "checkout must return the result of the gateway it was handed — a lambda gateway proves it cannot hard-code the receipt.",
        ),
    ],
    level="independent",
)

CH_P2_SEALED = challenge(
    "javi-p2-shapes-sealed",
    "Sealed Shapes, Exhaustive Area",
    r"""Inside `Solution`, model shapes with a sealed hierarchy and write an
exhaustive area function:
- `sealed interface Shape permits Circle, Rect`
- `record Circle(double radius) implements Shape`
- `record Rect(double w, double h) implements Shape`
- `static double area(Shape s)` using a pattern-matching switch with a
  case per variant (no default branch).

The tests verify both areas and the exhaustive dispatch.""",
    P2_BOILER,
    [
        (
            "circle area",
            r"""
checkNear(Solution.area(new Solution.Circle(2)), 12.5663706, 1e-6, "circle area");
""",
            "π·r² with Math.PI.",
        ),
        (
            "rect area",
            r"""
checkNear(Solution.area(new Solution.Rect(3, 4)), 12.0, 1e-9, "rect area");
""",
            "w·h.",
        ),
        (
            "dispatch covers both variants",
            r"""
checkNear(Solution.area(new Solution.Circle(1)) + Solution.area(new Solution.Rect(2, 2)), 7.1415927, 1e-6, "both variants");
""",
            "One switch handling both permitted records.",
        ),
    ],
    level="guided",
)

CH_P2_COUNTING = challenge(
    "javi-p2-counting-list",
    "Delegation Without Desync",
    r"""`AuditLog` wraps a list and counts every entry ever added, even after
removals (an audit trail must remember).

Implement inside `Solution`:
- `static class AuditLog` with methods `add(String e)`, `remove(String e)`
  (removes first occurrence), `int total()` (entries ever added),
  and `List<String> entries()` (current content, unmodifiable).
- Do NOT extend ArrayList. Compose and delegate — the counting must stay
  correct even though remove() changes the visible size.

The hidden test mimics the `addAll` bypass bug to prove composition wins.""",
    P2_BOILER,
    [
        (
            "total counts adds, not current size",
            r"""
Solution.AuditLog log = new Solution.AuditLog();
log.add("a"); log.add("b"); log.remove("a");
checkEq(log.total(), 2, "total counts every add");
checkEq(log.entries(), List.of("b"), "entries reflect removals");
""",
            "total() must be an independent counter, not entries().size().",
        ),
        (
            "composition surface is narrow",
            r"""
Solution.AuditLog log = new Solution.AuditLog();
log.add("x");
checkEq(log.entries(), List.of("x"), "entries view");
""",
            "entries() returns an unmodifiable view of the internal list.",
        ),
    ],
    level="independent",
)

VI_CH_P2_GATEWAY = vi_challenge(
    "Tiêm Payment Gateway",
    r"""Thiết kế luồng checkout quanh một hợp đồng:
- `interface PaymentGateway { String charge(int cents); }` bên trong `Solution`
  — trả về id biên nhận như `"ok-1000"`.
- `static class CheckoutService` với constructor nhận `PaymentGateway`
  và method `static String checkout(PaymentGateway g, int cents)`
  ủy quyền cho gateway và trả kết quả của nó.
- Cài `static class FakeGateway implements PaymentGateway` trả
  `"ok-" + cents` — test double mà service sẽ chạy với nó.

Test chạy service với fake (không bao giờ API thanh toán thật): đây là
dependency inversion thực hành bằng tay. Thêm nữa, một gateway-lambda khác
hành vi chứng minh service dùng đúng gateway được tiêm — không hard-code.""",
    [
        ("Service ủy quyền cho gateway được tiêm", "checkout phải gọi gateway.charge và trả giá trị của nó không thay đổi."),
        ("Fake là hiện thực thật của hợp đồng", "FakeGateway phải hiện thực PaymentGateway.charge(int)."),
        ("Service dùng ĐÚNG gateway được tiêm", "checkout phải trả kết quả của gateway nó nhận — lambda gateway chứng minh không hard-code."),
    ],
)

VI_CH_P2_SEALED = vi_challenge(
    "Sealed Shape, diện tích đầy đủ",
    r"""Bên trong `Solution`, mô hình hóa shape bằng sealed hierarchy và viết
hàm diện tích đầy đủ:
- `sealed interface Shape permits Circle, Rect`
- `record Circle(double radius) implements Shape`
- `record Rect(double w, double h) implements Shape`
- `static double area(Shape s)` dùng pattern-matching switch với một case
  cho mỗi biến thể (không nhánh default).

Test kiểm tra cả diện tích lẫn dispatch đầy đủ.""",
    [
        ("Diện tích hình tròn", "π·r² với Math.PI."),
        ("Diện tích hình chữ nhật", "w·h."),
        ("Dispatch phủ cả hai biến thể", "Một switch xử lý cả hai record được permit."),
    ],
)

VI_CH_P2_COUNTING = vi_challenge(
    "Delegation không lệch số",
    r"""`AuditLog` bọc một list và đếm mọi entry từng được thêm, kể cả sau khi
bị xóa (audit trail phải nhớ).

Cài bên trong `Solution`:
- `static class AuditLog` với method `add(String e)`, `remove(String e)`
  (xóa lần xuất hiện đầu), `int total()` (số entry từng thêm),
  và `List<String> entries()` (nội dung hiện tại, không thể sửa).
- KHÔNG extends ArrayList. Compose và delegate — phép đếm phải đúng dù
  remove() thay đổi kích thước hiển thị.

Test ẩn mô phỏng bug `addAll` đi vòng để chứng minh composition thắng.""",
    [
        ("total đếm lượt thêm, không phải size hiện tại", "total() phải là bộ đếm độc lập, không phải entries().size()."),
        ("Bề mặt composition hẹp", "entries() trả view không thể sửa của list nội bộ."),
    ],
)

write_practice(
    MOD,
    "javi-p2-design",
    "Design Lab: Payments & Shapes",
    "Inject a fake gateway, dispatch sealed shapes exhaustively, and build a desync-proof delegating log.",
    "Xưởng thiết kế: thanh toán & shape",
    "Tiêm fake gateway, dispatch sealed shape đầy đủ, và xây log ủy quyền không lệch số.",
    "composition-delegation",
    40,
    "intermediate",
    [CH_P2_GATEWAY, CH_P2_SEALED, CH_P2_COUNTING],
    {CH_P2_GATEWAY["id"]: VI_CH_P2_GATEWAY, CH_P2_SEALED["id"]: VI_CH_P2_SEALED, CH_P2_COUNTING["id"]: VI_CH_P2_COUNTING},
    solutions=[
        (
            CH_P2_GATEWAY["id"],
            r"""
public class Solution {
    public interface PaymentGateway { String charge(int cents); }
    public static class FakeGateway implements PaymentGateway {
        public String charge(int cents) { return "ok-" + cents; }
    }
    public static class CheckoutService {
        private final PaymentGateway gateway;
        public CheckoutService(PaymentGateway gateway) { this.gateway = gateway; }
    }
    public static String checkout(PaymentGateway g, int cents) { return g.charge(cents); }
}
""",
            r"""
public class Solution {
    public interface PaymentGateway { String charge(int cents); }
    public static class FakeGateway implements PaymentGateway {
        public String charge(int cents) { return "ok-" + cents; }
    }
    public static class CheckoutService {
        private final PaymentGateway gateway;
        public CheckoutService(PaymentGateway gateway) { this.gateway = gateway; }
    }
    // W: hard-codes the receipt instead of delegating — works for the one
    // tested amount, breaks the contract for every other amount.
    public static String checkout(PaymentGateway g, int cents) { return "ok-" + cents; }
}
""",
        ),
        (
            CH_P2_SEALED["id"],
            r"""
public class Solution {
    public sealed interface Shape permits Circle, Rect {}
    public record Circle(double radius) implements Shape {}
    public record Rect(double w, double h) implements Shape {}
    public static double area(Shape s) {
        return switch (s) {
            case Circle c -> Math.PI * c.radius() * c.radius();
            case Rect r -> r.w() * r.h();
        };
    }
}
""",
            r"""
public class Solution {
    public sealed interface Shape permits Circle, Rect {}
    public record Circle(double radius) implements Shape {}
    public record Rect(double w, double h) implements Shape {}
    // W: rect returns perimeter-shaped formula (2*(w+h)) — passes a 2x2
    // sanity read but is wrong for any rect where w != h.
    public static double area(Shape s) {
        return switch (s) {
            case Circle c -> Math.PI * c.radius() * c.radius();
            case Rect r -> 2 * (r.w() + r.h());
        };
    }
}
""",
        ),
        (
            CH_P2_COUNTING["id"],
            r"""
import java.util.*;

public class Solution {
    public static class AuditLog {
        private final List<String> inner = new ArrayList<>();
        private int total = 0;
        public void add(String e) { inner.add(e); total++; }
        public void remove(String e) { inner.remove(e); }
        public int total() { return total; }
        public List<String> entries() { return Collections.unmodifiableList(inner); }
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static class AuditLog {
        private final List<String> inner = new ArrayList<>();
        public void add(String e) { inner.add(e); }
        public void remove(String e) { inner.remove(e); }
        // W: derives total from current size — desyncs the moment a
        // removal happens, which is exactly the audit trail's job to survive.
        public int total() { return inner.size(); }
        public List<String> entries() { return Collections.unmodifiableList(inner); }
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — object-oriented design

You can now: depend on contracts instead of details, model finite variants
with sealed hierarchies, and replace fragile inheritance with composition
plus delegation. Prove it by designing a discount policy that swaps at
runtime.
"""

CP_MDX_VI = r"""
## Checkpoint — thiết kế hướng đối tượng

Giờ bạn có thể: phụ thuộc hợp đồng thay vì detail, mô hình hóa biến thể
hữu hạn bằng sealed hierarchy, và thay kế thừa mong manh bằng composition
cộng delegation. Chứng minh bằng cách thiết kế chính sách giảm giá hoán
đổi được lúc runtime.
"""

CH_CP2 = challenge(
    "javi-checkpoint-m2-design",
    "Swappable Discount Policy",
    r"""Design a discount engine behind a contract:
- `sealed interface Discount permits None, Percent, Flat` inside `Solution`
- `record None()`, `record Percent(int pct)`, `record Flat(int cents)`
- `static int apply(Discount d, int priceCents)` dispatching with a
  pattern switch:
  - None → price unchanged
  - Percent(pct) → price - price*pct/100 (integer division)
  - Flat(cents) → price - cents, but never below 0
- `static Discount best(List<Discount> options, int priceCents)` returning
  the policy that yields the LOWEST final price.

Fail fast: Percent outside 0..100 throws IllegalArgumentException.""",
    r"""
import java.util.*;

public class Solution {
    // Provide Discount hierarchy + apply + best here.
}
""",
    [
        (
            "percent discount",
            r"""
checkEq(Solution.apply(new Solution.Percent(25), 400), 300, "25% off 400");
""",
            "400 - 400*25/100 = 400 - 100 = 300.",
        ),
        (
            "flat discount floors at zero",
            r"""
checkEq(Solution.apply(new Solution.Flat(500), 300), 0, "flat never negative");
""",
            "Max(0, price - cents).",
        ),
        (
            "none leaves price",
            r"""
checkEq(Solution.apply(new Solution.None(), 777), 777, "none passthrough");
""",
            "None returns price unchanged.",
        ),
        (
            "best picks the lowest",
            r"""
List<Object> ds = List.of(new Solution.Percent(10), new Solution.Flat(50));
checkEq(Solution.apply(Solution.best((List) ds, 400), 400), 350, "flat wins at 400");
""",
            "Evaluate each option at the price, return the discount with the minimal result.",
        ),
        (
            "percent bounds enforced",
            r"""
try { new Solution.Percent(150); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "threw"); }
""",
            "Constructor validates 0..100, throwing IllegalArgumentException.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP2 = vi_challenge(
    "Chính sách giảm giá hoán đổi được",
    r"""Thiết kế máy giảm giá sau một hợp đồng:
- `sealed interface Discount permits None, Percent, Flat` bên trong `Solution`
- `record None()`, `record Percent(int pct)`, `record Flat(int cents)`
- `static int apply(Discount d, int priceCents)` dispatch bằng pattern switch:
  - None → giá không đổi
  - Percent(pct) → price - price*pct/100 (chia nguyên)
  - Flat(cents) → price - cents, nhưng không dưới 0
- `static Discount best(List<Discount> options, int priceCents)` trả về
  chính sách cho giá cuối THẤP NHẤT.

Fail fast: Percent ngoài 0..100 ném IllegalArgumentException.""",
    [
        ("Giảm theo phần trăm", "400 - 400*25/100 = 400 - 100 = 300."),
        ("Giảm cố định sàn ở 0", "Max(0, price - cents)."),
        ("None giữ nguyên giá", "None trả giá không đổi."),
        ("best chọn thấp nhất", "Tính từng lựa chọn theo giá, trả discount có kết quả nhỏ nhất."),
        ("Chặn biên phần trăm", "Constructor kiểm tra 0..100, ném IllegalArgumentException."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-oop",
    "Checkpoint: Design with Contracts",
    "Graded checkpoint: a sealed discount hierarchy with exhaustive dispatch and fail-fast validation.",
    15,
    CP_MDX,
    "Checkpoint: Thiết kế theo hợp đồng",
    "Checkpoint chấm điểm: sealed discount hierarchy với dispatch đầy đủ và kiểm tra fail-fast.",
    CP_MDX_VI,
    CH_CP2,
    VI_CH_CP2,
    solution=r"""
import java.util.*;

public class Solution {
    public sealed interface Discount permits None, Percent, Flat {}
    public record None() implements Discount {}
    public record Percent(int pct) implements Discount {
        public Percent {
            if (pct < 0 || pct > 100) throw new IllegalArgumentException("pct 0..100");
        }
    }
    public record Flat(int cents) implements Discount {}

    public static int apply(Discount d, int priceCents) {
        return switch (d) {
            case None n -> priceCents;
            case Percent p -> priceCents - priceCents * p.pct() / 100;
            case Flat f -> Math.max(0, priceCents - f.cents());
        };
    }

    public static Discount best(List<Discount> options, int priceCents) {
        Discount winner = null;
        int bestPrice = Integer.MAX_VALUE;
        for (Discount d : options) {
            int p = apply(d, priceCents);
            if (p < bestPrice) { bestPrice = p; winner = d; }
        }
        return winner;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public sealed interface Discount permits None, Percent, Flat {}
    public record None() implements Discount {}
    public record Percent(int pct) implements Discount {
        public Percent {
            if (pct < 0 || pct > 100) throw new IllegalArgumentException("pct 0..100");
        }
    }
    public record Flat(int cents) implements Discount {}

    public static int apply(Discount d, int priceCents) {
        return switch (d) {
            case None n -> priceCents;
            case Percent p -> priceCents - priceCents * p.pct() / 100;
            // W: Flat does not floor at zero — returns negative prices,
            // which is the behavioral near-miss the tests expose.
            case Flat f -> priceCents - f.cents();
        };
    }

    public static Discount best(List<Discount> options, int priceCents) {
        Discount winner = null;
        int bestPrice = Integer.MAX_VALUE;
        for (Discount d : options) {
            int p = apply(d, priceCents);
            if (p < bestPrice) { bestPrice = p; winner = d; }
        }
        return winner;
    }
}
""",
)
