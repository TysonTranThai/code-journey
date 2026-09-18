#!/usr/bin/env python3
"""Java — Intermediate — Module 12: java-architecture.

Layering (controller/service/repository), DTO vs domain models,
hand-rolled constructor-injection wiring, and refactoring a god class
into collaborators. House conventions throughout.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from javi import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "java-architecture"

# ── lesson 12.1 — layering ──────────────────────────────────────────────────
L_LAYERS_EN = r"""
## Layered architecture

Three layers cover most services:

```
Controller/UI  →  parses input, calls service, maps result
        ↓ depends on
Service        →  business rules, orchestration, transactions
        ↓ depends on
Repository     →  persistence (Module 11)
```

The dependency rule: **arrows point down only.** A service never calls a
controller; a repository never calls a service. Cross-layer calls flow
through narrow interfaces.

Why layers earn their keep:
- business rules live in ONE place (the service), not scattered in UI
  and SQL
- each layer tests differently: fast unit tests for services,
  contract tests for repositories
- swapping delivery (CLI → REST) doesn't touch the service

The failure mode this prevents is the *god class* — 1,200 lines that
parse, validate, compute, persist, and print, none of it testable in
isolation.
"""

L_LAYERS_VI = r"""
## Kiến trúc phân lớp

Ba lớp phủ được phần lớn dịch vụ:

```
Controller/UI  →  phân tích input, gọi service, map kết quả
        ↓ phụ thuộc
Service        →  quy tắc nghiệp vụ, điều phối, transaction
        ↓ phụ thuộc
Repository     →  persistence (Module 11)
```

Quy tắc phụ thuộc: **mũi tên chỉ xuống duy nhất.** Service không bao giờ
gọi controller; repository không bao giờ gọi service. Call xuyên lớp
chảy qua interface hẹp.

Vì sao các lớp đáng giá:
- quy tắc nghiệp vụ nằm ở MỘT chỗ (service), không rải trong UI và SQL
- mỗi lớp test theo kiểu riêng: unit test nhanh cho service, contract
  test cho repository
- hoán đổi cổng giao tiếp (CLI → REST) không chạm service

Mode hỏng mà điều này ngăn là *god class* — 1.200 dòng vừa parse, vừa
kiểm tra, tính toán, lưu trữ, và in ra, chẳng cái gì test riêng được.
"""

# ── lesson 12.2 — DTO vs domain ────────────────────────────────────────────
L_DTO_EN = r"""
## DTOs vs domain models

A **domain model** carries business behavior; a **DTO** (Data Transfer
Object) is a plain data shuttle between layers:

```java
// domain — knows the rules
public record Account(String id, int balanceCents) {
    public Account withdraw(int amount) {
        if (amount > balanceCents) throw new InsufficientFundsException();
        return new Account(id, balanceCents - amount);
    }
}

// DTO — crosses the layer boundary, no behavior
public record AccountView(String id, String balance) {}
```

Rules of thumb:
- internal layers pass domain objects; boundaries expose DTOs
- the mapping function is *explicit* (`toView(Account)`) — never expose
  mutable domain internals by accident
- DTO fields are presentation-shaped (`"1,234.00"`), domain fields are
  computation-shaped (`int cents`)

Small apps can skip DTOs; the discipline matters when the API shape and
the internal model want to evolve at different speeds.
"""

L_DTO_VI = r"""
## DTO so với domain model

**Domain model** mang hành vi nghiệp vụ; **DTO** (Data Transfer Object)
là con thoi dữ liệu thuần giữa các lớp:

```java
// domain — biết các quy tắc
public record Account(String id, int balanceCents) {
    public Account withdraw(int amount) {
        if (amount > balanceCents) throw new InsufficientFundsException();
        return new Account(id, balanceCents - amount);
    }
}

// DTO — băng qua ranh giới lớp, không hành vi
public record AccountView(String id, String balance) {}
```

Kinh nghiệm:
- các lớp nội bộ trao đổi domain object; ranh giới lộ DTO
- hàm mapping là *tường minh* (`toView(Account)`) — không bao giờ để
  nội bộ domain khả biến lộ ra ngoài một cách vô tình
- field DTO theo hình trình bày (`"1,234.00"`), field domain theo hình
  tính toán (`int cents`)

App nhỏ có thể bỏ qua DTO; kỷ luật này quan trọng khi hình dạng API và
mô hình nội bộ cần tiến hóa với tốc độ khác nhau.
"""

# ── lesson 12.3 — wiring & refactoring ─────────────────────────────────────
L_WIRING_EN = r"""
## Wiring dependencies by hand

Frameworks (Spring) do dependency injection for you; intermediates learn
to wire by hand first — it demystifies the container:

```java
public static void main(String[] args) {
    ExpenseRepository repo = new InMemoryExpenseRepository();
    ReportService reports = new ReportService(repo);
    CliController cli = new CliController(reports);
    cli.run();   // the composition root — the ONLY place that knows everything
}
```

The **composition root** is the single place where concrete classes
meet. Everything below it sees interfaces only.

Refactoring a god class, in order:
1. find the seams (inputs/outputs of each responsibility)
2. extract one responsibility into a collaborator
3. inject it via constructor
4. test the extracted class alone
5. repeat until the original class only *orchestrates*

Each step keeps the program working — refactoring is a series of small
verified moves, not a rewrite.
"""

L_WIRING_VI = r"""
## Dây nối phụ thuộc bằng tay

Framework (Spring) làm dependency injection giùm bạn; trình trung cấp học
tự nối trước — nó giải mã container:

```java
public static void main(String[] args) {
    ExpenseRepository repo = new InMemoryExpenseRepository();
    ReportService reports = new ReportService(repo);
    CliController cli = new CliController(reports);
    cli.run();   // composition root — nơi DUY NHẤT biết tất cả
}
```

**Composition root** là nơi duy nhất các class cụ thể gặp nhau. Mọi thứ
dưới nó chỉ thấy interface.

Refactor god class, theo thứ tự:
1. tìm các seam (đầu vào/đầu ra của mỗi trách nhiệm)
2. tách một trách nhiệm thành một cộng sự viên
3. tiêm nó qua constructor
4. test class vừa tách một mình
5. lặp lại cho đến khi class gốc chỉ còn *điều phối*

Mỗi bước giữ chương trình chạy được — refactor là chuỗi các nước nhỏ đã
kiểm chứng, không phải viết lại.
"""

write_module(
    MOD,
    "Application Architecture",
    "Layered design, DTO boundaries, hand-rolled composition roots, and the god-class refactoring sequence.",
    "Kiến trúc ứng dụng",
    "Thiết kế phân lớp, ranh giới DTO, composition root tự nối, và chuỗi refactor god class.",
    ["layered-architecture", "dto-boundaries", "wiring-refactoring", "javi-checkpoint-architecture"],
    ["javi-p12-architecture"],
)

write_lesson(MOD, "layered-architecture", "Layered Architecture", "Controller → service → repository, the arrows-point-down rule, and what each layer tests like.", 13, L_LAYERS_EN, "Kiến trúc phân lớp", "Controller → service → repository, quy tắc mũi tên chỉ xuống, và mỗi lớp test ra sao.", L_LAYERS_VI)

write_lesson(MOD, "dto-boundaries", "DTOs & Boundaries", "Behavior-carrying domain models vs presentation-shaped DTOs, and explicit mapping between them.", 12, L_DTO_EN, "DTO & ranh giới", "Domain model mang hành vi so với DTO hình trình bày, và mapping tường minh giữa chúng.", L_DTO_VI)

write_lesson(MOD, "wiring-refactoring", "Wiring & Refactoring", "The composition root without a framework, and the five-step seam-extraction sequence for god classes.", 14, L_WIRING_EN, "Dây nối & refactor", "Composition root không cần framework, và chuỗi năm bước tách seam cho god class.", L_WIRING_VI)

# ── practice set ────────────────────────────────────────────────────────────
P12_BOILER = r"""
import java.util.*;

public class Solution {
    // Implement types and methods below.
}
"""

CH_P12_LAYERS = challenge(
    "javi-p12-checkout-layers",
    "Layered Checkout",
    r"""Assemble a mini layered system in `Solution`:
- `record Order(String id, int cents)` (domain)
- `record OrderView(String id, String total)` (DTO — total formatted as
  `"$" + (cents/100) + "." + zeroPadded(cents%100)`, e.g. `$12.05`)
- `interface OrderRepository { void save(Order o); Order findById(String id); }`
- `static class InMemoryOrderRepository implements OrderRepository`
- `static class CheckoutService` with constructor `(OrderRepository r)`
  and `Order place(String id, int cents)`: rejects negative cents with
  IllegalArgumentException, then saves and returns the order.
- `static String viewTotal(int cents)` — the mapping function used by
  OrderView.

The controller layer is the test itself: it builds the repo, injects it
into the service, places an order, and maps it to a view.""",
    P12_BOILER,
    [
        (
            "service persists through the repo",
            r"""
Solution.InMemoryOrderRepository repo = new Solution.InMemoryOrderRepository();
Solution.CheckoutService svc = new Solution.CheckoutService(repo);
Solution.Order o = svc.place("o1", 1205);
checkEq(repo.findById("o1").cents(), 1205, "persisted");
""",
            "Service → repository, injected.",
        ),
        (
            "service validates",
            r"""
Solution.CheckoutService svc = new Solution.CheckoutService(new Solution.InMemoryOrderRepository());
try { svc.place("bad", -5); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "rejected"); }
""",
            "Business rule lives in the service, not the repository.",
        ),
        (
            "DTO mapping formats money",
            r"""
checkEq(Solution.viewTotal(1205), "$12.05", "dollars and padded cents");
checkEq(Solution.viewTotal(100), "$1.00", "exact dollar");
checkEq(Solution.viewTotal(7), "$0.07", "single digit padded");
""",
            "Format: $ + whole + '.' + two-digit cents.",
        ),
    ],
    level="real-world",
)

CH_P12_GODCLASS = challenge(
    "javi-p12-extract-pricing",
    "Extract the Pricing Collaborator",
    r"""`static class GodCart` (provided in the starter comments — recreate
it fixed) computes totals, applies discounts, and formats receipts in
one method. Refactor by extraction:

- `static class Pricing` with `static int total(List<Integer> centsList,
  int discountPercent)` — sum minus percentage discount (integer math).
- `static class GodCart` now takes `Pricing` as a constructor dependency
  (any object works — you accept `Object` and call the static method,
  or accept nothing; keep it simple: the cart delegates to
  `Pricing.total`) and exposes `String receipt(List<Integer> centsList,
  int discountPercent)` returning `"TOTAL: $" + viewTotal(total)` using
  your Module-12 `viewTotal` from the previous challenge — define it
  again here.

The seam test: `receipt(List.of(1000, 500), 10)` → total 1350 →
`"TOTAL: $13.50"`.""",
    P12_BOILER,
    [
        (
            "pricing computes discounted total",
            r"""
checkEq(Solution.Pricing.total(List.of(1000, 500), 10), 1350, "1500 - 10%");
""",
            "Sum 1500, minus 10% = 1350 (integer division).",
        ),
        (
            "cart delegates through the seam",
            r"""
Solution.GodCart cart = new Solution.GodCart();
checkEq(cart.receipt(List.of(1000, 500), 10), "TOTAL: $13.50", "formatted via collaborator");
""",
            "The cart must route math through Pricing and format via viewTotal.",
        ),
        (
            "empty cart",
            r"""
Solution.GodCart cart = new Solution.GodCart();
checkEq(cart.receipt(List.of(), 0), "TOTAL: $0.00", "empty receipt");
""",
            "Zero items → $0.00.",
        ),
    ],
    level="independent",
)

CH_P12_SEAMTEST = challenge(
    "javi-p12-testable-report",
    "Report Service with a Seamed Clock",
    r"""Combine Module 8's seams with Module 12's layering in `Solution`:
- `interface Clock { long nowMillis(); }` (reuse the shape)
- `static class ReportService` with constructor `(Clock clock)` exposing
  `String header()` returning `"Report @ <millis>"` using the injected
  clock.
- `static class ReportController` with constructor `(ReportService s)`
  exposing `String render()` returning `s.header() + "\n[body]"`.

Build the graph twice with different clocks — proving the controller is
agnostic to time. This is the composition root skill.""",
    P12_BOILER,
    [
        (
            "service honors the injected clock",
            r"""
Solution.ReportService s = new Solution.ReportService(() -> 1726300000000L);
checkEq(s.header(), "Report @ 1726300000000", "clock-driven header");
""",
            "The lambda IS a clock — interface seams accept lambdas.",
        ),
        (
            "controller composes the service",
            r"""
Solution.ReportController c = new Solution.ReportController(
    new Solution.ReportService(() -> 42L));
checkEq(c.render(), "Report @ 42\n[body]", "controller wraps service");
""",
            "render = header + body, through the service.",
        ),
        (
            "two clocks, one controller class",
            r"""
Solution.ReportController a = new Solution.ReportController(new Solution.ReportService(() -> 1L));
Solution.ReportController b = new Solution.ReportController(new Solution.ReportService(() -> 999L));
checkTrue(!a.render().equals(b.render()), "times differ");
""",
            "Same classes, different behavior — that's injection.",
        ),
    ],
    level="guided",
)

VI_CH_P12_LAYERS = vi_challenge(
    "Checkout phân lớp",
    r"""Lắp ráp một hệ thống phân lớp mini trong `Solution`:
- `record Order(String id, int cents)` (domain)
- `record OrderView(String id, String total)` (DTO — total format
  `"$" + (cents/100) + "." + padZero(cents%100)`, ví dụ `$12.05`)
- `interface OrderRepository { void save(Order o); Order findById(String id); }`
- `static class InMemoryOrderRepository implements OrderRepository`
- `static class CheckoutService` với constructor `(OrderRepository r)`
  và `Order place(String id, int cents)`: chặn cents âm bằng
  IllegalArgumentException, rồi lưu và trả order.
- `static String viewTotal(int cents)` — hàm mapping mà OrderView dùng.

Tầng controller chính là test: nó dựng repo, tiêm vào service, đặt order,
và map sang view.""",
    [
        ("Service lưu qua repo", "Service → repository, được tiêm."),
        ("Service kiểm tra dữ liệu", "Quy tắc nghiệp vụ nằm ở service, không phải repository."),
        ("Mapping DTO định dạng tiền", "Format: $ + phần nguyên + '.' + hai chữ số cents."),
    ],
)

VI_CH_P12_GODCLASS = vi_challenge(
    "Tách cộng sự viên tính giá",
    r"""`static class GodCart` (cho sẵn trong comment starter — dựng lại bản
đã sửa) tính tổng, áp giảm giá, và định dạng biên nhận trong một method.
Refactor bằng tách:

- `static class Pricing` với `static int total(List<Integer> centsList,
  int discountPercent)` — tổng trừ phần trăm giảm giá (chia nguyên).
- `static class GodCart` giờ nhận `Pricing` làm phụ thuộc constructor
  (chấp nhận `Object` và gọi method tĩnh, hoặc không nhận gì; giữ đơn
  giản: cart ủy quyền cho `Pricing.total`) và lộ
  `String receipt(List<Integer> centsList, int discountPercent)` trả
  `"TOTAL: $" + viewTotal(total)` dùng `viewTotal` của Module-12 từ thử
  thách trước — định nghĩa lại nó ở đây.

Test seam: `receipt(List.of(1000, 500), 10)` → total 1350 →
`"TOTAL: $13.50"`.""",
    [
        ("Pricing tính tổng đã giảm", "Tổng 1500, trừ 10% = 1350 (chia nguyên)."),
        ("Cart ủy quyền qua seam", "Cart phải đi phép tính qua Pricing và định dạng qua viewTotal."),
        ("Cart rỗng", "Không món → $0.00."),
    ],
)

VI_CH_P12_SEAMTEST = vi_challenge(
    "Report service với clock đã seam",
    r"""Kết hợp seam của Module 8 với phân lớp của Module 12 trong `Solution`:
- `interface Clock { long nowMillis(); }` (tái dùng dáng này)
- `static class ReportService` với constructor `(Clock clock)` lộ
  `String header()` trả `"Report @ <millis>"` dùng clock được tiêm.
- `static class ReportController` với constructor `(ReportService s)`
  lộ `String render()` trả `s.header() + "\n[body]"`.

Lắp đồ thị hai lần với hai clock khác nhau — chứng minh controller bất
kể thời gian. Đây là kỹ năng composition root.""",
    [
        ("Service tôn trọng clock được tiêm", "Lambda chính là một clock — seam interface nhận lambda."),
        ("Controller soạn service", "render = header + body, qua service."),
        ("Hai clock, một class controller", "Cùng class, hành vi khác nhau — đó là injection."),
    ],
)

write_practice(
    MOD,
    "javi-p12-architecture",
    "Architecture Lab",
    "Layer a checkout flow end-to-end, extract a pricing collaborator, and prove injection with two clocks.",
    "Xưởng kiến trúc",
    "Phân lớp luồng checkout trọn vẹn, tách cộng sự viên tính giá, và chứng minh injection với hai clock.",
    "wiring-refactoring",
    40,
    "intermediate",
    [CH_P12_LAYERS, CH_P12_GODCLASS, CH_P12_SEAMTEST],
    {CH_P12_LAYERS["id"]: VI_CH_P12_LAYERS, CH_P12_GODCLASS["id"]: VI_CH_P12_GODCLASS, CH_P12_SEAMTEST["id"]: VI_CH_P12_SEAMTEST},
    solutions=[
        (
            CH_P12_LAYERS["id"],
            r"""
public class Solution {
    public record Order(String id, int cents) {}
    public record OrderView(String id, String total) {}

    public interface OrderRepository {
        void save(Order o);
        Order findById(String id);
    }

    public static class InMemoryOrderRepository implements OrderRepository {
        private final java.util.Map<String, Order> store = new java.util.LinkedHashMap<>();
        public void save(Order o) { store.put(o.id(), o); }
        public Order findById(String id) { return store.get(id); }
    }

    public static class CheckoutService {
        private final OrderRepository r;
        public CheckoutService(OrderRepository r) { this.r = r; }
        public Order place(String id, int cents) {
            if (cents < 0) throw new IllegalArgumentException("negative cents");
            Order o = new Order(id, cents);
            r.save(o);
            return o;
        }
    }

    public static String viewTotal(int cents) {
        return "$" + (cents / 100) + "." + String.format("%02d", cents % 100);
    }
}
""",
            r"""
public class Solution {
    public record Order(String id, int cents) {}
    public record OrderView(String id, String total) {}

    public interface OrderRepository {
        void save(Order o);
        Order findById(String id);
    }

    public static class InMemoryOrderRepository implements OrderRepository {
        private final java.util.Map<String, Order> store = new java.util.LinkedHashMap<>();
        public void save(Order o) { store.put(o.id(), o); }
        public Order findById(String id) { return store.get(id); }
    }

    public static class CheckoutService {
        private final OrderRepository r;
        public CheckoutService(OrderRepository r) { this.r = r; }
        // W: validation pushed down into the repository — business rules
        // leak below the service boundary and the repo now throws on
        // data the service should have guarded.
        public Order place(String id, int cents) {
            Order o = new Order(id, cents);
            r.save(o);
            return o;
        }
    }

    public static String viewTotal(int cents) {
        return "$" + (cents / 100) + "." + String.format("%02d", cents % 100);
    }
}
""",
        ),
        (
            CH_P12_GODCLASS["id"],
            r"""
import java.util.*;

public class Solution {
    public static class Pricing {
        public static int total(List<Integer> centsList, int discountPercent) {
            int sum = 0;
            for (int c : centsList) sum += c;
            return sum - sum * discountPercent / 100;
        }
    }

    public static class GodCart {
        public String receipt(List<Integer> centsList, int discountPercent) {
            return "TOTAL: $" + Solution.viewTotal(Pricing.total(centsList, discountPercent)).substring(1);
        }
    }

    public static String viewTotal(int cents) {
        return "$" + (cents / 100) + "." + String.format("%02d", cents % 100);
    }
}
""",
            r"""
import java.util.*;

public class Solution {
    public static class Pricing {
        // W: the discount parameter is accepted and ignored — the receipt
        // always shows the full sum. Every discounted expectation fails.
        public static int total(List<Integer> centsList, int discountPercent) {
            int sum = 0;
            for (int c : centsList) sum += c;
            return sum;
        }
    }

    public static class GodCart {
        public String receipt(List<Integer> centsList, int discountPercent) {
            return "TOTAL: $" + Solution.viewTotal(Pricing.total(centsList, discountPercent)).substring(1);
        }
    }

    public static String viewTotal(int cents) {
        return "$" + (cents / 100) + "." + String.format("%02d", cents % 100);
    }
}
""",
        ),
        (
            CH_P12_SEAMTEST["id"],
            r"""
public class Solution {
    public interface Clock { long nowMillis(); }

    public static class ReportService {
        private final Clock clock;
        public ReportService(Clock clock) { this.clock = clock; }
        public String header() { return "Report @ " + clock.nowMillis(); }
    }

    public static class ReportController {
        private final ReportService s;
        public ReportController(ReportService s) { this.s = s; }
        public String render() { return s.header() + "\n[body]"; }
    }
}
""",
            r"""
public class Solution {
    public interface Clock { long nowMillis(); }

    public static class ReportService {
        private final Clock clock;
        public ReportService(Clock clock) { this.clock = clock; }
        // W: the service calls System.currentTimeMillis() directly —
        // the injected clock is ignored, so both controllers print the
        // same (real) time and the seam is dead.
        public String header() { return "Report @ " + System.currentTimeMillis(); }
    }

    public static class ReportController {
        private final ReportService s;
        public ReportController(ReportService s) { this.s = s; }
        public String render() { return s.header() + "\n[body]"; }
    }
}
""",
        ),
    ],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
CP_MDX = r"""
## Checkpoint — architecture

You can now: assemble layered systems with a composition root, expose
DTOs at boundaries, and extract collaborators until god classes dissolve.
Prove it with a full three-layer mini-stack.
"""

CP_MDX_VI = r"""
## Checkpoint — kiến trúc

Giờ bạn có thể: lắp hệ thống phân lớp với composition root, lộ DTO tại
ranh giới, và tách cộng sự viên cho đến khi god class tan rã. Chứng minh
bằng một mini-stack ba lớp hoàn chỉnh.
"""

CH_CP12 = challenge(
    "javi-checkpoint-m12-architecture",
    "Three-Layer Mini-Stack",
    r"""Assemble the full stack in `Solution`:
- `record Task(String id, String title, boolean done)` (domain)
- `interface TaskRepository { void save(Task t); Optional<Task> find(String id); List<Task> all(); }`
- `static class InMemoryTaskRepository implements TaskRepository`
- `static class TaskService` with constructor `(TaskRepository r)`:
  - `Task create(String id, String title)` — blank title throws
    IllegalArgumentException; saves and returns
  - `Task complete(String id)` — missing id throws
    NoSuchElementException; marks done and saves
  - `List<Task> pending()` — all not-done tasks (insertion order)
- `record TaskView(String id, String title)` (DTO)
- `static List<TaskView> pendingViews(TaskService s)` — the controller
  function mapping pending() to views.

Then the test drives the whole graph: repo → service → views.""",
    r"""
import java.util.*;

public class Solution {
    public record Task(String id, String title, boolean done) {}
    public record TaskView(String id, String title) {}
    // Provide TaskRepository, InMemoryTaskRepository, TaskService,
    // and pendingViews here.
}
""",
    [
        (
            "create validates and persists",
            r"""
Solution.InMemoryTaskRepository repo = new Solution.InMemoryTaskRepository();
Solution.TaskService svc = new Solution.TaskService(repo);
svc.create("t1", "write tests");
checkEq(repo.find("t1").orElseThrow().done(), false, "created open");
try { svc.create("t2", "  "); checkTrue(false, "must throw"); }
catch (IllegalArgumentException e) { checkTrue(true, "blank rejected"); }
""",
            "Service guards the rule; repo stores the result.",
        ),
        (
            "complete flips state",
            r"""
Solution.InMemoryTaskRepository repo = new Solution.InMemoryTaskRepository();
Solution.TaskService svc = new Solution.TaskService(repo);
svc.create("t1", "a");
svc.complete("t1");
checkEq(repo.find("t1").orElseThrow().done(), true, "done");
try { svc.complete("ghost"); checkTrue(false, "must throw"); }
catch (java.util.NoSuchElementException e) { checkTrue(true, "missing id"); }
""",
            "Complete updates persisted state; unknown ids throw.",
        ),
        (
            "pending filters and maps",
            r"""
Solution.InMemoryTaskRepository repo = new Solution.InMemoryTaskRepository();
Solution.TaskService svc = new Solution.TaskService(repo);
svc.create("t1", "a"); svc.create("t2", "b");
svc.complete("t1");
List<Solution.TaskView> views = Solution.pendingViews(svc);
checkEq(views.size(), 1, "only pending");
checkEq(views.get(0).title(), "b", "t2 remains");
""",
            "pending() filters; pendingViews() maps to DTOs.",
        ),
    ],
    level="real-world",
    difficulty="intermediate",
)

VI_CH_CP12 = vi_challenge(
    "Mini-stack ba lớp",
    r"""Lắp full stack trong `Solution`:
- `record Task(String id, String title, boolean done)` (domain)
- `interface TaskRepository { void save(Task t); Optional<Task> find(String id); List<Task> all(); }`
- `static class InMemoryTaskRepository implements TaskRepository`
- `static class TaskService` với constructor `(TaskRepository r)`:
  - `Task create(String id, String title)` — title blank ném
    IllegalArgumentException; lưu và trả
  - `Task complete(String id)` — id thiếu ném NoSuchElementException;
    đánh dấu done và lưu
  - `List<Task> pending()` — các task chưa done (thứ tự chèn)
- `record TaskView(String id, String title)` (DTO)
- `static List<TaskView> pendingViews(TaskService s)` — hàm controller
  map pending() sang view.

Rồi test điều khiển toàn bộ đồ thị: repo → service → view.""",
    [
        ("create kiểm tra và lưu", "Service giữ quy tắc; repo lưu kết quả."),
        ("complete lật trạng thái", "Complete cập nhật trạng thái đã lưu; id lạ ném."),
        ("pending lọc và map", "pending() lọc; pendingViews() map sang DTO."),
    ],
)

write_checkpoint(
    MOD,
    "javi-checkpoint-architecture",
    "Checkpoint: Architecture",
    "Graded checkpoint: a complete repo→service→controller flow with validation, DTO mapping, and state transitions.",
    15,
    CP_MDX,
    "Checkpoint: Kiến trúc",
    "Checkpoint chấm điểm: luồng repo→service→controller hoàn chỉnh với kiểm tra, map DTO, và chuyển trạng thái.",
    CP_MDX_VI,
    CH_CP12,
    VI_CH_CP12,
    solution=r"""
import java.util.*;

public class Solution {
    public record Task(String id, String title, boolean done) {}
    public record TaskView(String id, String title) {}

    public interface TaskRepository {
        void save(Task t);
        Optional<Task> find(String id);
        List<Task> all();
    }

    public static class InMemoryTaskRepository implements TaskRepository {
        private final Map<String, Task> store = new LinkedHashMap<>();
        public void save(Task t) { store.put(t.id(), t); }
        public Optional<Task> find(String id) { return Optional.ofNullable(store.get(id)); }
        public List<Task> all() { return new ArrayList<>(store.values()); }
    }

    public static class TaskService {
        private final TaskRepository r;
        public TaskService(TaskRepository r) { this.r = r; }

        public Task create(String id, String title) {
            if (title == null || title.isBlank()) throw new IllegalArgumentException("blank title");
            Task t = new Task(id, title, false);
            r.save(t);
            return t;
        }

        public Task complete(String id) {
            Task t = r.find(id).orElseThrow(() -> new NoSuchElementException("task " + id));
            Task done = new Task(t.id(), t.title(), true);
            r.save(done);
            return done;
        }

        public List<Task> pending() {
            List<Task> out = new ArrayList<>();
            for (Task t : r.all()) if (!t.done()) out.add(t);
            return out;
        }
    }

    public static List<TaskView> pendingViews(TaskService s) {
        List<TaskView> out = new ArrayList<>();
        for (Task t : s.pending()) out.add(new TaskView(t.id(), t.title()));
        return out;
    }
}
""",
    wrong=r"""
import java.util.*;

public class Solution {
    public record Task(String id, String title, boolean done) {}
    public record TaskView(String id, String title) {}

    public interface TaskRepository {
        void save(Task t);
        Optional<Task> find(String id);
        List<Task> all();
    }

    public static class InMemoryTaskRepository implements TaskRepository {
        private final Map<String, Task> store = new LinkedHashMap<>();
        public void save(Task t) { store.put(t.id(), t); }
        public Optional<Task> find(String id) { return Optional.ofNullable(store.get(id)); }
        public List<Task> all() { return new ArrayList<>(store.values()); }
    }

    public static class TaskService {
        private final TaskRepository r;
        public TaskService(TaskRepository r) { this.r = r; }

        // W: complete() never saves the updated task — the state flip
        // lives only in the returned object and the store still says
        // not-done, so pending() keeps listing completed tasks.
        public Task complete(String id) {
            Task t = r.find(id).orElseThrow(() -> new NoSuchElementException("task " + id));
            return new Task(t.id(), t.title(), true);
        }

        public Task create(String id, String title) {
            if (title == null || title.isBlank()) throw new IllegalArgumentException("blank title");
            Task t = new Task(id, title, false);
            r.save(t);
            return t;
        }

        public List<Task> pending() {
            List<Task> out = new ArrayList<>();
            for (Task t : r.all()) if (!t.done()) out.add(t);
            return out;
        }
    }

    public static List<TaskView> pendingViews(TaskService s) {
        List<TaskView> out = new ArrayList<>();
        for (Task t : s.pending()) out.add(new TaskView(t.id(), t.title()));
        return out;
    }
}
""",
)
