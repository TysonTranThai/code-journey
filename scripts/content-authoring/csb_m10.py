#!/usr/bin/env python3
"""C# — Beginner — Module 10: csb-oop.

The four OOP pillars behaviorally: inheritance as reuse, virtual/override
as polymorphic dispatch, interfaces as contracts. Ws misimplement the
dispatch or the contract so tests discriminate. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-oop"

write_module(
    M,
    "Object-Oriented Programming",
    "Inheritance, virtual methods, and interfaces: how C# types share behavior and swap implementations behind a contract.",
    "Lập trình hướng đối tượng",
    "Kế thừa, phương thức ảo, và interface: các kiểu C# chia sẻ hành vi và hoán đổi cài đặt sau một hợp đồng.",
    ["csb-m10-inheritance", "csb-m10-polymorphism", "csb-m10-interfaces", "csb-checkpoint-m10"],
    ["csb-p10-oop"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m10-inheritance",
    "Inheritance: reuse with `base`",
    "A derived class gets the base's members, extends them, and must keep the base's promises.",
    13,
    r"""
## One class built on another

**Inheritance** declares that one class *is a* kind of another:

```csharp
class Account
{
    public decimal Balance { get; protected set; }

    public void Deposit(decimal amount)
    {
        if (amount <= 0) throw new ArgumentException("non-positive deposit");
        Balance += amount;
    }
}

class SavingsAccount : Account
{
    public void AddMonthlyInterest(decimal rate)
    {
        Balance += Balance * rate;   // reuses the inherited Balance
    }
}
```

`SavingsAccount` carries everything `Account` has — `Deposit` with its validation included — and adds its own behavior. Callers holding a `SavingsAccount` can `Deposit` without knowing the derived type exists.

## Extension, replacement, and `base`

A derived class can add members, or **replace** a non-virtual member with `new` (hiding) — but replacing is a smell for beginners: the hidden base method still runs when called through a base reference.

The honest tool for "same idea, better implementation" is the constructor chain:

```csharp
class SavingsAccount : Account
{
    public SavingsAccount(string owner, decimal opening) : base(owner, opening) { }
}
```

`base(...)` forwards construction to the base constructor — the base's invariants run first, always. `base.Member` also reaches the base's implementation from inside an override.
""",
    "Kế thừa: tái sử dụng với `base`",
    "Lớp dẫn xuất nhận các thành viên của lớp cơ sở, mở rộng chúng, và phải giữ mọi lời hứa của lớp cơ sở.",
    r"""
## Một lớp dựng trên lớp khác

**Kế thừa** tuyên bố một lớp *là một* dạng của lớp khác:

```csharp
class Account
{
    public decimal Balance { get; protected set; }

    public void Deposit(decimal amount)
    {
        if (amount <= 0) throw new ArgumentException("non-positive deposit");
        Balance += amount;
    }
}

class SavingsAccount : Account
{
    public void AddMonthlyInterest(decimal rate)
    {
        Balance += Balance * rate;   // tái sử dụng Balance được kế thừa
    }
}
```

`SavingsAccount` mang mọi thứ `Account` có — bao gồm `Deposit` cùng phần kiểm tra — và thêm hành vi riêng. Người gọi giữ `SavingsAccount` vẫn `Deposit` được mà không cần biết kiểu dẫn xuất tồn tại.

## Mở rộng, thay thế, và `base`

Lớp dẫn xuất có thể thêm thành viên, hoặc **thay thế** thành viên không-ảo bằng `new` (che khuất) — nhưng thay thế là mùi mã với người mới: phương thức cơ sở bị che vẫn chạy khi gọi qua tham chiếu kiểu cơ sở.

Công cụ trung thực cho "cùng ý tưởng, cài đặt tốt hơn" là xích constructor:

```csharp
class SavingsAccount : Account
{
    public SavingsAccount(string owner, decimal opening) : base(owner, opening) { }
}
```

`base(...)` chuyển tiếp việc dựng lên constructor cơ sở — bất biến của lớp cơ sở luôn chạy trước. `base.ThànhViên` cũng chạm tới cài đặt của cơ sở từ bên trong một override.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m10-polymorphism",
    "Polymorphism: one call, many shapes",
    "`virtual` marks a method replaceable; `override` replaces it; the runtime picks by the object's actual type.",
    14,
    r"""
## The dispatch problem

A method that processes many kinds must behave per-kind. Without language help you write type checks everywhere; with `virtual`/`override` the runtime does it:

```csharp
class Shape
{
    public virtual double Area() => 0.0;
}

class Circle : Shape
{
    private double r;
    public Circle(double radius) { r = radius; }
    public override double Area() => Math.PI * r * r;
}

class Rect : Shape
{
    private double w, h;
    public Rect(double w, double h) { this.w = w; this.h = h; }
    public override double Area() => w * h;
}
```

Now one loop handles every shape — including kinds written *after* this loop existed:

```csharp
var shapes = new List<Shape> { new Circle(1), new Rect(2, 3) };
double total = 0;
foreach (Shape s in shapes) total += s.Area();   // actual type decides
```

`s.Area()` dispatches on the object's **runtime type**: Circle's override for circles, Rect's for rectangles. Adding `Triangle : Shape` needs zero changes to the loop — that is the payoff.

## The rules that make it safe

- `virtual` says "subclasses may replace this"; without it, `override` doesn't compile.
- An override keeps the base's signature. Callers can't tell override from original at the call site.
- `sealed override` stops further replacement.

Missing override is not an error — the base implementation runs. That makes `virtual` a promise: the base version must be a sane default.
""",
    "Đa hình: một lời gọi, nhiều hình dạng",
    "`virtual` đánh dấu phương thức có thể bị thay thế; `override` thay thế nó; runtime chọn theo kiểu thực của đối tượng.",
    r"""
## Bài toán điều phối

Một phương thức xử lý nhiều loại đối tượng phải hành xử theo từng loại. Không có trợ giúp từ ngôn ngữ, bạn viết kiểm tra kiểu khắp nơi; với `virtual`/`override`, runtime làm việc đó:

```csharp
class Shape
{
    public virtual double Area() => 0.0;
}

class Circle : Shape
{
    private double r;
    public Circle(double radius) { r = radius; }
    public override double Area() => Math.PI * r * r;
}

class Rect : Shape
{
    private double w, h;
    public Rect(double w, double h) { this.w = w; this.h = h; }
    public override double Area() => w * h;
}
```

Giờ một vòng lặp xử lý mọi hình — kể cả các loại được viết *sau* khi vòng lặp này tồn tại:

```csharp
var shapes = new List<Shape> { new Circle(1), new Rect(2, 3) };
double total = 0;
foreach (Shape s in shapes) total += s.Area();   // kiểu thực quyết định
```

`s.Area()` điều phối theo **kiểu lúc chạy** của đối tượng: override của Circle cho hình tròn, của Rect cho hình chữ nhật. Thêm `Triangle : Shape` không cần sửa vòng lặp — đó là phần thưởng.

## Các luật làm nên sự an toàn

- `virtual` nói "lớp con được thay thế cái này"; không có nó, `override` không biên dịch.
- Override giữ nguyên chữ ký của cơ sở. Tại chỗ gọi, override không thể phân biệt với bản gốc.
- `sealed override` chặn mọi thay thế tiếp theo.

Thiếu override không phải lỗi — bản của cơ sở chạy. Vậy nên `virtual` là một lời hứa: bản cơ sở phải là mặc định hợp lý.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m10-interfaces",
    "Interfaces: contracts without inheritance",
    "An interface is a pure contract; a type can satisfy many, and callers depend only on the contract.",
    13,
    r"""
## A contract, nothing else

An **interface** declares what members must exist — no fields, no implementation:

```csharp
interface IStorable
{
    string Serialize();
}

class Document : IStorable
{
    public string Serialize() => "doc";   // must exist, must be public
}
```

A class lists its interfaces after its base class: `class Document : IStorable`. The compiler enforces that `Document` provides `public string Serialize()` — miss it and compilation fails.

## Many contracts, one type

Unlike inheritance (one base class), a type may satisfy many interfaces — and unrelated types can share one:

```csharp
class Memory : IStorable { public string Serialize() => "mem"; }
```

`Document` and `Memory` share nothing but the contract, yet both flow through the same code:

```csharp
static string Save(IStorable s) => s.Serialize();
```

## Choose by need

- **Inheritance** = sharing *implementation* plus an is-a relationship.
- **Interface** = sharing a *promise* across unrelated types.

Reaching for interfaces everywhere is its own disease; start concrete, extract a contract when two+ types genuinely share a promise. Later modules use `IEnumerable<T>` — a contract you already depend on daily.
""",
    "Interface: hợp đồng không cần kế thừa",
    "Interface là hợp đồng thuần; một kiểu có thể thỏa nhiều hợp đồng, và người gọi chỉ phụ thuộc hợp đồng.",
    r"""
## Một hợp đồng, không gì khác

Một **interface** khai báo những thành viên bắt buộc phải tồn tại — không trường, không cài đặt:

```csharp
interface IStorable
{
    string Serialize();
}

class Document : IStorable
{
    public string Serialize() => "doc";   // phải tồn tại, phải public
}
```

Lớp liệt kê interface sau lớp cơ sở: `class Document : IStorable`. Trình biên dịch ép `Document` cung cấp `public string Serialize()` — thiếu là lỗi biên dịch.

## Nhiều hợp đồng, một kiểu

Khác kế thừa (một lớp cơ sở), một kiểu có thể thỏa nhiều interface — và các kiểu không liên quan vẫn dùng chung một hợp đồng:

```csharp
class Memory : IStorable { public string Serialize() => "mem"; }
```

`Document` và `Memory` không chia sẻ gì ngoài hợp đồng, nhưng cả hai cùng chảy qua một đoạn mã:

```csharp
static string Save(IStorable s) => s.Serialize();
```

## Chọn theo nhu cầu

- **Kế thừa** = chia sẻ *cài đặt* cộng quan hệ is-a.
- **Interface** = chia sẻ một *lời hứa* giữa các kiểu không liên quan.

Lạm dụng interface cũng là một bệnh; hãy bắt đầu bằng lớp cụ thể, trích hợp đồng khi từ hai kiểu trở lên thật sự chia sẻ một lời hứa. Các bài sau dùng `IEnumerable<T>` — một hợp đồng bạn đã phụ thuộc hằng ngày.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p10-oop",
    "OOP workout",
    "Shapes, payroll, notifications, vehicles — polymorphism and contracts under discriminating tests.",
    "Luyện tập OOP",
    "Hình học, bảng lương, thông báo, phương tiện — đa hình và hợp đồng dưới các bài kiểm tra phân biệt.",
    "csb-m10-interfaces",
    40,
    "beginner",
    [
        challenge(
            "csb-p10-shapes",
            "Polymorphic shapes",
            "Implement nested classes inside `Solution`: abstract `Shape` with `public abstract string Describe();`, plus `Circle(double radius)`, `Square(double side)`, and `Triangle(double a, double b, double c)` — each overriding `Describe()` to return exactly `\"circle r=1\"` / `\"square s=2\"` / `\"triangle a=3 b=4 c=5\"` style strings.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var shapes = new List<Solution.Shape> { new Solution.Circle(1), new Solution.Square(2), new Solution.Triangle(3, 4, 5) };\nCj.Eq(shapes[0].Describe(), \"circle r=1\", \"circle\");\nCj.Eq(shapes[1].Describe(), \"square s=2\", \"square\");\nCj.Eq(shapes[2].Describe(), \"triangle a=3 b=4 c=5\", \"triangle\");",
                    "Each override formats its own kind — one call site, three behaviors.",
                ),
                (
                    "dispatch",
                    "var shapes = new List<Solution.Shape> { new Solution.Square(2), new Solution.Circle(1) };\nstring all = \"\";\nforeach (Solution.Shape s in shapes) all += s.Describe() + \";\";\nCj.Eq(all, \"square s=2;circle r=1;\", \"runtime dispatch in order\");",
                    "Through a base-typed list, the actual type decides the output — that is the polymorphism contract.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p10-payroll",
            "Payroll with base reuse",
            "Implement nested classes in `Solution`: abstract `Employee` with protected `Name`, public constructor validating non-blank name (else `ArgumentException`), read-only `Name`, `public abstract decimal MonthlyPay();`; `Salaried(decimal monthly)` overriding `MonthlyPay()` to return the salary; `Hourly(decimal rate, int hours)` overriding to return `rate * hours`.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var s = new Solution.Salaried(\"An\", 2000m);\nvar h = new Solution.Hourly(\"Binh\", 20m, 160);\nCj.Eq(s.MonthlyPay(), 2000m, \"salary\");\nCj.Eq(h.MonthlyPay(), 3200m, \"rate times hours\");\nCj.Eq(s.Name, \"An\", \"name from base\");\nCj.Eq(h.Name, \"Binh\", \"hourly name too\");",
                    "Both subclasses compute differently but expose the same MonthlyPay contract.",
                ),
                (
                    "validation",
                    "bool t1 = false;\ntry { new Solution.Salaried(\"  \", 100m); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { new Solution.Hourly(\"\", 20m, 10); } catch (ArgumentException) { t2 = true; }\nCj.True(t1 && t2, \"blank names rejected in the base constructor\");",
                    "The name invariant lives once in the base — both subclasses inherit it.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p10-notifier",
            "Notifier behind an interface",
            "Implement in `Solution`: interface `INotifier { string Send(string message); }`; classes `EmailNotifier` (returns `\"email: \" + message`) and `SmsNotifier` (returns `\"sms: \" + message`); and `static string Broadcast(INotifier n, string message)` returning `n.Send(message)`.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.Broadcast(new Solution.EmailNotifier(), \"hi\"), \"email: hi\", \"email flavor\");\nCj.Eq(Solution.Broadcast(new Solution.SmsNotifier(), \"hi\"), \"sms: hi\", \"sms flavor\");",
                    "Broadcast depends only on the contract; the flavor comes from the object.",
                ),
                (
                    "swap",
                    "var notifiers = new List<Solution.INotifier> { new Solution.EmailNotifier(), new Solution.SmsNotifier() };\nstring log = \"\";\nforeach (var n in notifiers) log += n.Send(\"ping\") + \";\";\nCj.Eq(log, \"email: ping;sms: ping;\", \"contract-level loop\");",
                    "One loop, both implementations — code written against the interface never changes when flavors are added.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p10-vehicles",
            "Vehicle fleet totals",
            "Implement in `Solution`: abstract `Vehicle` with `public abstract double FuelFor(double km);`; `Car` returning `km / 15.0`; `Truck` returning `km / 8.0`; and `static double FleetFuel(List<Vehicle> fleet, double km)` summing `FuelFor(km)` over the fleet (null/empty fleet → 0).",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var fleet = new List<Solution.Vehicle> { new Solution.Car(), new Solution.Truck() };\nCj.Near(Solution.FleetFuel(fleet, 120), 120 / 15.0 + 120 / 8.0, 1e-9, \"car + truck\");\nCj.Eq(Solution.FleetFuel(new List<Solution.Vehicle>(), 100), 0.0, \"empty fleet\");\nCj.Eq(Solution.FleetFuel(null, 100), 0.0, \"null fleet\");",
                    "FleetFuel aggregates through the abstract contract only.",
                ),
                (
                    "single",
                    "var solo = new List<Solution.Vehicle> { new Solution.Truck() };\nCj.Near(Solution.FleetFuel(solo, 80), 10.0, 1e-9, \"80km truck burns 10\");",
                    "A lone truck at 8 km/l covers 80 km on 10 liters.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p10-shapes": vi_challenge(
            "Hình học đa hình",
            "Hiện thực các lớp lồng trong `Solution`: `Shape` trừu tượng với `public abstract string Describe();`, cùng `Circle(double radius)`, `Square(double side)`, `Triangle(double a, double b, double c)` — mỗi lớp override `Describe()` trả đúng chuỗi dạng `\"circle r=1\"` / `\"square s=2\"` / `\"triangle a=3 b=4 c=5\"`.",
            [
                ("normal", "Mỗi override định dạng loại của riêng mình — một chỗ gọi, ba hành vi."),
                ("dispatch", "Qua danh sách kiểu cơ sở, kiểu thực quyết định kết xuất — đó là hợp đồng đa hình."),
            ],
        ),
        "csb-p10-payroll": vi_challenge(
            "Bảng lương tái sử dụng base",
            "Hiện thực các lớp lồng trong `Solution`: `Employee` trừu tượng với `Name` protected, constructor công khai kiểm tra tên không rỗng (nếu không ném `ArgumentException`), `Name` chỉ-đọc, `public abstract decimal MonthlyPay();`; `Salaried(decimal monthly)` override trả lương tháng; `Hourly(decimal rate, int hours)` override trả `rate * hours`.",
            [
                ("normal", "Hai lớp con tính khác nhau nhưng cùng hợp đồng MonthlyPay."),
                ("validation", "Bất biến tên nằm một chỗ ở base — cả hai lớp con đều kế thừa."),
            ],
        ),
        "csb-p10-notifier": vi_challenge(
            "Notifier sau interface",
            "Hiện thực trong `Solution`: interface `INotifier { string Send(string message); }`; các lớp `EmailNotifier` (trả `\"email: \" + message`) và `SmsNotifier` (trả `\"sms: \" + message`); và `static string Broadcast(INotifier n, string message)` trả `n.Send(message)`.",
            [
                ("normal", "Broadcast chỉ phụ thuộc hợp đồng; hương vị đến từ đối tượng."),
                ("swap", "Một vòng lặp, hai cài đặt — mã viết theo interface không đổi khi thêm loại mới."),
            ],
        ),
        "csb-p10-vehicles": vi_challenge(
            "Tổng nhiên liệu đội xe",
            "Hiện thực trong `Solution`: `Vehicle` trừu tượng với `public abstract double FuelFor(double km);`; `Car` trả `km / 15.0`; `Truck` trả `km / 8.0`; và `static double FleetFuel(List<Vehicle> fleet, double km)` cộng `FuelFor(km)` trên cả đội (đội null/rỗng → 0).",
            [
                ("normal", "FleetFuel tổng hợp chỉ qua hợp đồng trừu tượng."),
                ("single", "Một xe tải đơn lẻ với 8 km/l đi 80 km tốn 10 lít."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p10-shapes",
            'public class Solution\n{\n    public abstract class Shape\n    {\n        public abstract string Describe();\n    }\n    public sealed class Circle : Shape\n    {\n        private double r;\n        public Circle(double radius) { r = radius; }\n        public override string Describe() { return "circle r=" + r; }\n    }\n    public sealed class Square : Shape\n    {\n        private double s;\n        public Square(double side) { s = side; }\n        public override string Describe() { return "square s=" + s; }\n    }\n    public sealed class Triangle : Shape\n    {\n        private double a, b, c;\n        public Triangle(double x, double y, double z) { a = x; b = y; c = z; }\n        public override string Describe() { return "triangle a=" + a + " b=" + b + " c=" + c; }\n    }\n}\n',
            'public class Solution\n{\n    public abstract class Shape\n    {\n        public abstract string Describe();\n    }\n    public sealed class Circle : Shape\n    {\n        private double r;\n        public Circle(double radius) { r = radius; }\n        // near-miss: forgot `override` on Describe (won\'t compile) — the\n        // honest near-miss here: describes as a square regardless of type\n        public string Describe() { return "square s=?"; }\n    }\n    public sealed class Square : Shape\n    {\n        private double s;\n        public Square(double side) { s = side; }\n        public override string Describe() { return "square s=" + s; }\n    }\n    public sealed class Triangle : Shape\n    {\n        private double a, b, c;\n        public Triangle(double x, double y, double z) { a = x; b = y; c = z; }\n        public override string Describe() { return "triangle a=" + a + " b=" + b + " c=" + c; }\n    }\n}\n',
        ),
        (
            "csb-p10-payroll",
            'public class Solution\n{\n    public abstract class Employee\n    {\n        public Employee(string name)\n        {\n            if (string.IsNullOrWhiteSpace(name))\n                throw new ArgumentException("name required");\n            Name = name;\n        }\n        public string Name { get; }\n        public abstract decimal MonthlyPay();\n    }\n    public sealed class Salaried : Employee\n    {\n        private decimal monthly;\n        public Salaried(string name, decimal monthly) : base(name) { this.monthly = monthly; }\n        public override decimal MonthlyPay() { return monthly; }\n    }\n    public sealed class Hourly : Employee\n    {\n        private decimal rate;\n        private int hours;\n        public Hourly(string name, decimal rate, int hours) : base(name) { this.rate = rate; this.hours = hours; }\n        public override decimal MonthlyPay() { return rate * hours; }\n    }\n}\n',
            'public class Solution\n{\n    public abstract class Employee\n    {\n        public Employee(string name)\n        {\n            if (string.IsNullOrWhiteSpace(name))\n                throw new ArgumentException("name required");\n            Name = name;\n        }\n        public string Name { get; }\n        public abstract decimal MonthlyPay();\n    }\n    public sealed class Salaried : Employee\n    {\n        private decimal monthly;\n        public Salaried(string name, decimal monthly) : base(name) { this.monthly = monthly; }\n        public override decimal MonthlyPay() { return monthly; }\n    }\n    public sealed class Hourly : Employee\n    {\n        private decimal rate;\n        private int hours;\n        public Hourly(string name, decimal rate, int hours) : base(name) { this.rate = rate; this.hours = hours; }\n        // near-miss: integer division ordering bug — rate first cast to int\n        // would truncate; here the real near-miss: adds a base salary too\n        public override decimal MonthlyPay() { return rate * hours + 100m; }\n    }\n}\n',
        ),
        (
            "csb-p10-notifier",
            'public class Solution\n{\n    public interface INotifier { string Send(string message); }\n    public sealed class EmailNotifier : INotifier\n    {\n        public string Send(string message) { return "email: " + message; }\n    }\n    public sealed class SmsNotifier : INotifier\n    {\n        public string Send(string message) { return "sms: " + message; }\n    }\n    public static string Broadcast(INotifier n, string message) { return n.Send(message); }\n}\n',
            'public class Solution\n{\n    public interface INotifier { string Send(string message); }\n    public sealed class EmailNotifier : INotifier\n    {\n        public string Send(string message) { return "email: " + message; }\n    }\n    public sealed class SmsNotifier : INotifier\n    {\n        public string Send(string message) { return "sms: " + message; }\n    }\n    // near-miss: Broadcast hard-codes the email flavor instead of calling\n    // through the contract — sms callers get email output\n    public static string Broadcast(INotifier n, string message)\n    {\n        return "email: " + message;\n    }\n}\n',
        ),
        (
            "csb-p10-vehicles",
            'public class Solution\n{\n    public abstract class Vehicle\n    {\n        public abstract double FuelFor(double km);\n    }\n    public sealed class Car : Vehicle\n    {\n        public override double FuelFor(double km) { return km / 15.0; }\n    }\n    public sealed class Truck : Vehicle\n    {\n        public override double FuelFor(double km) { return km / 8.0; }\n    }\n    public static double FleetFuel(List<Vehicle> fleet, double km)\n    {\n        if (fleet == null) return 0.0;\n        double total = 0.0;\n        foreach (Vehicle v in fleet) total += v.FuelFor(km);\n        return total;\n    }\n}\n',
            'public class Solution\n{\n    public abstract class Vehicle\n    {\n        public abstract double FuelFor(double km);\n    }\n    public sealed class Car : Vehicle\n    {\n        public override double FuelFor(double km) { return km / 15.0; }\n    }\n    public sealed class Truck : Vehicle\n    {\n        public override double FuelFor(double km) { return km / 8.0; }\n    }\n    public static double FleetFuel(List<Vehicle> fleet, double km)\n    {\n        if (fleet == null) return 0.0;\n        double total = 0.0;\n        foreach (Vehicle v in fleet)\n        {\n            // near-miss: every vehicle burns the CAR rate — truck fuel is\n            // underestimated by the contract-blind constant\n            total += km / 15.0;\n        }\n        return total;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m10",
    "Checkpoint — OOP",
    "A media library: a base `MediaItem`, audio and video specializations, and a contract-level player loop.",
    20,
    r"""
## Checkpoint: the media library

**Task:** implement in `Solution`:

1. Abstract class `MediaItem` — protected `Title`, public constructor throwing `ArgumentException` for null/whitespace title, read-only `Title`, `public abstract int PlaySeconds();`.
2. `Song(string title, int seconds)` — returns `seconds`.
3. `Video(string title, int seconds, int speed)` — playback at `speed` (1 = normal); `PlaySeconds()` returns the **wall-clock time**: `seconds / speed` (integer division is fine).
4. `static int TotalRuntime(List<MediaItem> items)` — sum of `PlaySeconds()`; null/empty → 0.
""",
    "Checkpoint — OOP",
    "Thư viện media: `MediaItem` cơ sở, chuyên biệt hóa audio và video, và vòng lặp phát ở mức hợp đồng.",
    r"""
## Checkpoint: thư viện media

**Nhiệm vụ:** hiện thực trong `Solution`:

1. Lớp trừu tượng `MediaItem` — `Title` protected, constructor công khai ném `ArgumentException` khi tiêu đề null/toàn khoảng trắng, `Title` chỉ-đọc, `public abstract int PlaySeconds();`.
2. `Song(string title, int seconds)` — trả `seconds`.
3. `Video(string title, int seconds, int speed)` — phát ở tốc độ `speed` (1 = thường); `PlaySeconds()` trả **thời gian thực tế**: `seconds / speed` (chia nguyên là được).
4. `static int TotalRuntime(List<MediaItem> items)` — tổng `PlaySeconds()`; null/rỗng → 0.
""",
    challenge(
        "csb-checkpoint-m10-task",
        "MediaLibrary",
        "Implement `MediaItem`, `Song`, `Video`, and `TotalRuntime` — the title invariant lives in the base once; the wall-clock rule is Video's override alone.",
        CS_PRELUDE,
        [
            (
                "runtime",
                "var lib = new List<Solution.MediaItem> { new Solution.Song(\"Jazz\", 180), new Solution.Video(\"Talk\", 180, 2) };\nCj.Eq(Solution.TotalRuntime(lib), 270, \"180s song + 90s video\");\nCj.Eq(lib[0].Title, \"Jazz\", \"title from base\");\nCj.Eq(Solution.TotalRuntime(new List<Solution.MediaItem>()), 0, \"empty\");\nCj.Eq(Solution.TotalRuntime(null), 0, \"null\");",
                "The loop sees only MediaItem; Song and Video answers differ by override.",
            ),
            (
                "invariant",
                "bool t1 = false;\ntry { new Solution.Song(\"  \", 100); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { new Solution.Video(null, 100, 1); } catch (ArgumentException) { t2 = true; }\nCj.True(t1 && t2, \"blank titles rejected through the base constructor\");",
                "Both subclasses inherit the base's title validation — one invariant, enforced everywhere.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "MediaLibrary",
        "Hiện thực `MediaItem`, `Song`, `Video`, và `TotalRuntime` — bất biến tiêu đề nằm ở base một lần; luật thời-gian-thực là override riêng của Video.",
        [
            ("runtime", "Vòng lặp chỉ thấy MediaItem; kết quả của Song và Video khác nhau nhờ override."),
            ("invariant", "Cả hai lớp con kế thừa kiểm tra tiêu đề của base — một bất biến, thực thi khắp nơi."),
        ],
    ),
    solution='public class Solution\n{\n    public abstract class MediaItem\n    {\n        public MediaItem(string title)\n        {\n            if (string.IsNullOrWhiteSpace(title))\n                throw new ArgumentException("title required");\n            Title = title;\n        }\n        public string Title { get; }\n        public abstract int PlaySeconds();\n    }\n    public sealed class Song : MediaItem\n    {\n        private int seconds;\n        public Song(string title, int seconds) : base(title) { this.seconds = seconds; }\n        public override int PlaySeconds() { return seconds; }\n    }\n    public sealed class Video : MediaItem\n    {\n        private int seconds;\n        private int speed;\n        public Video(string title, int seconds, int speed) : base(title) { this.seconds = seconds; this.speed = speed; }\n        public override int PlaySeconds() { return seconds / speed; }\n    }\n    public static int TotalRuntime(List<MediaItem> items)\n    {\n        if (items == null) return 0;\n        int total = 0;\n        foreach (MediaItem m in items) total += m.PlaySeconds();\n        return total;\n    }\n}\n',
    wrong='public class Solution\n{\n    public abstract class MediaItem\n    {\n        public MediaItem(string title)\n        {\n            if (string.IsNullOrWhiteSpace(title))\n                throw new ArgumentException("title required");\n            Title = title;\n        }\n        public string Title { get; }\n        public abstract int PlaySeconds();\n    }\n    public sealed class Song : MediaItem\n    {\n        private int seconds;\n        public Song(string title, int seconds) : base(title) { this.seconds = seconds; }\n        public override int PlaySeconds() { return seconds; }\n    }\n    public sealed class Video : MediaItem\n    {\n        private int seconds;\n        private int speed;\n        public Video(string title, int seconds, int speed) : base(title) { this.seconds = seconds; this.speed = speed; }\n        // near-miss: ignores playback speed — every video counts at 1x, so\n        // a 2x video reports double its wall-clock time\n        public override int PlaySeconds() { return seconds; }\n    }\n    public static int TotalRuntime(List<MediaItem> items)\n    {\n        if (items == null) return 0;\n        int total = 0;\n        foreach (MediaItem m in items) total += m.PlaySeconds();\n        return total;\n    }\n}\n',
)
