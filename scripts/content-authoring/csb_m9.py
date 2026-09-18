#!/usr/bin/env python3
"""C# — Beginner — Module 9: csb-classes.

Classes and objects: fields as per-object state, constructors as the place
invariants are established, properties as controlled access. Encapsulation
is tested behaviorally — the Ws break exactly the invariant the R defends.
House conventions: Ws are behavioral near-misses, tests discriminate.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-classes"

write_module(
    M,
    "Classes and Objects",
    "Grouping state and behavior: fields, constructors, and properties — the vocabulary of every C# program.",
    "Lớp và đối tượng",
    "Nhóm trạng thái và hành vi: trường, hàm khởi tạo, và thuộc tính — vốn từ của mọi chương trình C#.",
    ["csb-m9-basics", "csb-m9-constructors", "csb-m9-properties", "csb-checkpoint-m9"],
    ["csb-p9-classes"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m9-basics",
    "Objects: state plus behavior",
    "Fields as per-object state, methods as behavior over that state, instances as independent copies.",
    13,
    r"""
## State and behavior together

A **class** is a blueprint for objects: it declares the *fields* (state) every object carries and the *methods* (behavior) that operate on that state.

```csharp
class Stopwatch
{
    public long elapsedMs;      // field: per-object state
    public bool running;

    public void Start()         // method: behavior over state
    {
        running = true;
    }

    public void Record(long nowMs)
    {
        if (running) elapsedMs += nowMs;   // reads/writes THIS object's fields
        running = false;
    }
}
```

`new` builds one object from the blueprint:

```csharp
var a = new Stopwatch();
var b = new Stopwatch();
a.Start();
// b.elapsedMs is still 0 — each object owns its own fields
```

`a` and `b` are independent *instances*. Writing to a field on one never affects the other: state belongs to the object, not to the class.

## Members and `this`

Inside a method, an unqualified name like `elapsedMs` means *this object's* field. Writing `this.elapsedMs` is explicit — you need it only when a parameter shadows a field:

```csharp
public void Rename(string name)
{
    this.name = name;   // left: the field, right: the parameter
}
```

Everything here is per-object. Members that belong to the *class itself* are declared `static` — a later topic.
""",
    "Đối tượng: trạng thái cộng hành vi",
    "Trường là trạng thái theo từng đối tượng, phương thức là hành vi trên trạng thái đó, thực thể là bản sao độc lập.",
    r"""
## Trạng thái và hành vi cùng nhau

Một **lớp** là bản thiết kế cho đối tượng: nó khai báo các *trường* (trạng thái) mà mọi đối tượng mang theo và các *phương thức* (hành vi) thao tác trên trạng thái đó.

```csharp
class Stopwatch
{
    public long elapsedMs;      // trường: trạng thái theo từng đối tượng
    public bool running;

    public void Start()         // phương thức: hành vi trên trạng thái
    {
        running = true;
    }

    public void Record(long nowMs)
    {
        if (running) elapsedMs += nowMs;   // đọc/ghi trường của CHÍNH đối tượng này
        running = false;
    }
}
```

`new` dựng một đối tượng từ bản thiết kế:

```csharp
var a = new Stopwatch();
var b = new Stopwatch();
a.Start();
// b.elapsedMs vẫn là 0 — mỗi đối tượng sở hữu trường riêng
```

`a` và `b` là hai *thực thể* độc lập. Ghi trường trên đối tượng này không bao giờ ảnh hưởng đối tượng kia: trạng thái thuộc về đối tượng, không phải lớp.

## Thành viên và `this`

Trong một phương thức, tên không định vị như `elapsedMs` nghĩa là trường *của chính đối tượng này*. Viết `this.elapsedMs` là tường minh — chỉ cần khi tham số che khuất trường:

```csharp
public void Rename(string name)
{
    this.name = name;   // trái: trường, phải: tham số
}
```

Mọi thứ ở đây là theo đối tượng. Thành viên thuộc về *chính lớp* được khai báo `static` — chủ đề ở bài sau.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m9-constructors",
    "Constructors and initialization",
    "Constructors establish invariants at birth; overloads and object initializers shape how callers build objects.",
    12,
    r"""
## Constructors establish invariants

A **constructor** runs when `new` creates the object. Its job is to leave the object in a *valid* state — reject nonsense immediately, never store it:

```csharp
class Ticket
{
    public string Event;
    public int Price;

    public Ticket(string event_, int price)
    {
        Event = event_;
        if (price < 0) throw new ArgumentException("negative price");
        Price = price;
    }
}

var t = new Ticket("Concert", 250);   // valid at birth
```

The constructor's name matches the class and has no return type. Declaring any constructor removes the invisible parameterless one — `new Ticket()` no longer compiles unless you write it yourself.

## Overloads and initializers

Several constructors give callers choices, and one can **chain** another with `this(...)` so the validation lives in exactly one place:

```csharp
public Ticket(string event_) : this(event_, 0) { }   // free tickets, same rules
```

For simple flat setup, an **object initializer** sets fields/properties right after `new`:

```csharp
var t2 = new Ticket { Event = "Play", Price = 180 };
```

The initializer is sugar for "construct, then assign". It cannot validate — if bad state must be *rejected*, put that in the constructor.
""",
    "Hàm khởi tạo và khởi tạo đối tượng",
    "Hàm khởi tạo thiết lập bất biến ngay từ đầu; overload và object initializer định hình cách người gọi dựng đối tượng.",
    r"""
## Hàm khởi tạo thiết lập bất biến

Một **hàm khởi tạo** chạy khi `new` tạo đối tượng. Nhiệm vụ của nó là để đối tượng ở trạng thái *hợp lệ* — chặn dữ liệu vô lý ngay lập tức, không bao giờ lưu nó:

```csharp
class Ticket
{
    public string Event;
    public int Price;

    public Ticket(string event_, int price)
    {
        Event = event_;
        if (price < 0) throw new ArgumentException("negative price");
        Price = price;
    }
}

var t = new Ticket("Concert", 250);   // hợp lệ ngay từ đầu
```

Tên hàm khởi tạo trùng tên lớp và không có kiểu trả về. Khi bạn khai báo bất kỳ hàm khởi tạo nào, hàm không-tham-số vô hình biến mất — `new Ticket()` không còn biên dịch trừ khi bạn tự viết nó.

## Overload và initializer

Nhiều hàm khởi tạo cho người gọi nhiều lựa chọn, và một hàm có thể **xích** sang hàm khác bằng `this(...)` để phần kiểm tra tồn tại đúng một nơi:

```csharp
public Ticket(string event_) : this(event_, 0) { }   // vé miễn phí, cùng luật
```

Với thiết lập phẳng đơn giản, **object initializer** gán trường/thuộc tính ngay sau `new`:

```csharp
var t2 = new Ticket { Event = "Play", Price = 180 };
```

Initializer chỉ là cách viết gọn cho "khởi tạo, rồi gán". Nó không thể kiểm tra — nếu trạng thái xấu phải bị *từ chối*, hãy đặt kiểm tra trong hàm khởi tạo.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m9-properties",
    "Properties: controlled access",
    "A public field hands out raw state; a property looks like a field but runs your code — where invariants live.",
    14,
    r"""
## The problem with public fields

A public field hands out raw state — anyone can write `account.Balance = -999;` and your object is now lying. Fields should be `private`; the question is how outsiders *read* state they need.

## Properties look like fields, run like methods

A **property** is accessed with field syntax but compiles to method calls:

```csharp
class Account
{
    private decimal balance;                 // hidden state

    public decimal Balance                   // controlled access
    {
        get { return balance; }
        private set { balance = value; }     // only the class may change it
    }
}
```

Readers write `account.Balance` — indistinguishable from a field at the call site. Writers hit *your* code, where the invariant lives. `value` is the incoming assignment inside `set`.

## Auto-properties and validation

When both accessors just wrap a hidden field, let C# generate it:

```csharp
public string Name { get; }             // get-only: set once in constructor
public int Hits { get; private set; }   // read anywhere, mutate inside methods
```

When a settable property must keep a rule, validate in `set`:

```csharp
private int health;
public int Health
{
    get { return health; }
    set { health = Math.Clamp(value, 0, 100); }   // always in [0, 100]
}
```

`Math.Clamp(value, min, max)` pins a number into range — every modern .NET has it. The habit that matters: **state is private, behavior is public**. Methods and setters are the only doors, and each door can enforce the rules.
""",
    "Thuộc tính: truy cập có kiểm soát",
    "Trường công khai trao trạng thái thô; thuộc tính giống trường về cú pháp nhưng chạy mã của bạn — nơi bất biến sinh sống.",
    r"""
## Vấn đề của trường công khai

Một trường công khai trao trạng thái thô — ai cũng có thể viết `account.Balance = -999;` và đối tượng của bạn giờ đang nói dối. Trường nên là `private`; câu hỏi là người ngoài *đọc* trạng thái họ cần bằng cách nào.

## Thuộc tính: giống trường về cú pháp, chạy như phương thức

Một **thuộc tính** được truy cập bằng cú pháp trường nhưng biên dịch thành lời gọi phương thức:

```csharp
class Account
{
    private decimal balance;                 // trạng thái ẩn

    public decimal Balance                   // truy cập có kiểm soát
    {
        get { return balance; }
        private set { balance = value; }     // chỉ lớp này được đổi
    }
}
```

Người đọc viết `account.Balance` — tại chỗ gọi, không phân biệt được với trường. Người ghi chạm vào mã *của bạn* — nơi bất biến sinh sống. `value` là giá trị đang được gán bên trong `set`.

## Auto-property và kiểm tra dữ liệu

Khi cả hai accessor chỉ bọc một trường ẩn, hãy để C# tự sinh:

```csharp
public string Name { get; }             // chỉ-get: gán một lần trong constructor
public int Hits { get; private set; }   // đọc ở đâu cũng được, đổi trong phương thức
```

Khi thuộc tính có set phải giữ một luật, hãy kiểm tra trong `set`:

```csharp
private int health;
public int Health
{
    get { return health; }
    set { health = Math.Clamp(value, 0, 100); }   // luôn nằm trong [0, 100]
}
```

`Math.Clamp(value, min, max)` ghim một số vào khoảng — mọi .NET hiện đại đều có. Thói quen quan trọng: **trạng thái là private, hành vi là public**. Phương thức và setter là những cánh cửa duy nhất, và mỗi cánh cửa có thể thực thi luật riêng.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p9-classes",
    "Class workout",
    "Counters, shapes, temperatures, and players — encapsulation under discriminating tests.",
    "Luyện tập lớp",
    "Bộ đếm, hình học, nhiệt độ, và người chơi — đóng gói dưới các bài kiểm tra phân biệt.",
    "csb-m9-properties",
    40,
    "beginner",
    [
        challenge(
            "csb-p9-counter",
            "Counter with a floor",
            "Implement nested class `Solution.Counter`: starts at 0; `Increment()` adds 1; `Decrement()` subtracts 1 but the value **never goes below 0**; read-only `Value` property.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var c = new Solution.Counter();\nCj.Eq(c.Value, 0, \"starts at zero\");\nc.Increment();\nc.Increment();\nc.Decrement();\nCj.Eq(c.Value, 1, \"one left after up-up-down\");",
                    "A fresh counter is zero; the value tracks the exact operation sequence.",
                ),
                (
                    "floor",
                    "var c = new Solution.Counter();\nc.Decrement();\nc.Decrement();\nc.Decrement();\nCj.Eq(c.Value, 0, \"never below zero\");\nc.Increment();\nCj.Eq(c.Value, 1, \"recovers to one, not negative-plus-one\");",
                    "The floor is the contract: decrementing at zero must be a no-op, not a hidden negative.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p9-rectangle",
            "Rectangle that validates",
            "Implement nested class `Solution.Rectangle`: constructor `(double width, double height)` throws `ArgumentException` unless both are positive; read-only `Width`/`Height`; `Area()`; `Scale(double factor)` grows **both** dimensions and throws `ArgumentException` for a non-positive factor.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var r = new Solution.Rectangle(3, 4);\nCj.Near(r.Area(), 12.0, 1e-9, \"3x4 area\");\nCj.Near(r.Width, 3.0, 1e-9, \"width kept\");\nr.Scale(2);\nCj.Near(r.Width, 6.0, 1e-9, \"width doubled\");\nCj.Near(r.Area(), 48.0, 1e-9, \"area grew sixteen-fold? no: four-fold\");",
                    "Scale multiplies every dimension, so area grows by factor squared.",
                ),
                (
                    "validation",
                    "bool t1 = false;\ntry { new Solution.Rectangle(0, 5); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { new Solution.Rectangle(3, -1); } catch (ArgumentException) { t2 = true; }\nbool t3 = false;\ntry { var r = new Solution.Rectangle(1, 1); r.Scale(0); } catch (ArgumentException) { t3 = true; }\nCj.True(t1 && t2 && t3, \"zero/negative dimensions and zero factor all rejected\");",
                    "Invalid construction must throw at the constructor — never store bad state.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p9-temperature",
            "Temperature scale",
            "Implement nested class `Solution.Temperature`: constructor `(double celsius)` throws `ArgumentException` below absolute zero (-273.15, exact boundary allowed); read-only `Celsius`; static factory `FromFahrenheit(double f)` converting with C = (F − 32) × 5⁄9 and applying the same validation after conversion.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var t = new Solution.Temperature(25.0);\nCj.Near(t.Celsius, 25.0, 1e-9, \"celsius kept\");\nvar boil = Solution.Temperature.FromFahrenheit(212.0);\nCj.Near(boil.Celsius, 100.0, 1e-9, \"water boils at 100C\");\nvar freeze = Solution.Temperature.FromFahrenheit(32.0);\nCj.Near(freeze.Celsius, 0.0, 1e-9, \"water freezes at 0C\");",
                    "The conversion is (F − 32) × 5⁄9 — check both anchor points.",
                ),
                (
                    "validation",
                    "bool t1 = false;\ntry { new Solution.Temperature(-273.16); } catch (ArgumentException) { t1 = true; }\nvar edge = new Solution.Temperature(-273.15);\nCj.Near(edge.Celsius, -273.15, 1e-9, \"exact absolute zero is legal\");\nbool t2 = false;\ntry { Solution.Temperature.FromFahrenheit(-500.0); } catch (ArgumentException) { t2 = true; }\nCj.True(t1 && t2, \"below absolute zero rejected on both paths\");",
                    "−273.15 exactly is legal; anything lower throws — via the constructor OR after conversion.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p9-player",
            "Player with clamped health",
            "Implement nested class `Solution.Player`: constructor `(string name)` throws `ArgumentException` for null/whitespace names; read-only `Name`; `Health` starts at 100; `TakeDamage(int)` and `Heal(int)` throw `ArgumentException` for negative amounts, otherwise health stays clamped to [0, 100]; `IsAlive` is true exactly when Health > 0.",
            CS_PRELUDE,
            [
                (
                    "lifecycle",
                    "var p = new Solution.Player(\"An\");\nCj.Eq(p.Health, 100, \"starts full\");\np.TakeDamage(30);\nCj.Eq(p.Health, 70, \"damaged to 70\");\nCj.True(p.IsAlive, \"alive at 70\");\np.TakeDamage(70);\nCj.Eq(p.Health, 0, \"floors at zero\");\nCj.False(p.IsAlive, \"dead at exactly 0\");",
                    "Health floors at 0; IsAlive uses strictly greater-than, so 0 is dead.",
                ),
                (
                    "bounds-and-validation",
                    "var p = new Solution.Player(\"Binh\");\np.Heal(50);\nCj.Eq(p.Health, 100, \"heal caps at 100\");\nbool t1 = false;\ntry { p.TakeDamage(-5); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { p.Heal(-1); } catch (ArgumentException) { t2 = true; }\nbool t3 = false;\ntry { new Solution.Player(\"   \"); } catch (ArgumentException) { t3 = true; }\nCj.True(t1 && t2 && t3, \"negative damage/heal and blank name all rejected\");",
                    "Both clamps matter: no negatives in, no values outside [0, 100] out.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p9-counter": vi_challenge(
            "Bộ đếm có sàn",
            "Hiện thực lớp lồng `Solution.Counter`: bắt đầu từ 0; `Increment()` cộng 1; `Decrement()` trừ 1 nhưng giá trị **không bao giờ dưới 0**; thuộc tính `Value` chỉ-đọc.",
            [
                ("normal", "Bộ đếm mới là 0; giá trị theo đúng chuỗi thao tác."),
                ("floor", "Sàn là hợp đồng: trừ tại 0 phải là không-op, không phải âm ẩn."),
            ],
        ),
        "csb-p9-rectangle": vi_challenge(
            "Hình chữ nhật có kiểm tra",
            "Hiện thực lớp lồng `Solution.Rectangle`: constructor `(double width, double height)` ném `ArgumentException` trừ khi cả hai đều dương; `Width`/`Height` chỉ-đọc; `Area()`; `Scale(double factor)` phóng **cả hai** chiều và ném `ArgumentException` khi factor không dương.",
            [
                ("normal", "Scale nhân mọi chiều, nên diện tích tăng theo bình phương factor."),
                ("validation", "Dựng đối tượng vô lý phải ném tại constructor — không bao giờ lưu trạng thái xấu."),
            ],
        ),
        "csb-p9-temperature": vi_challenge(
            "Thang nhiệt độ",
            "Hiện thực lớp lồng `Solution.Temperature`: constructor `(double celsius)` ném `ArgumentException` khi dưới absolute zero (-273.15, đúng biên thì cho phép); `Celsius` chỉ-đọc; factory tĩnh `FromFahrenheit(double f)` đổi theo C = (F − 32) × 5⁄9 và áp dụng cùng luật kiểm tra sau khi đổi.",
            [
                ("normal", "Công thức là (F − 32) × 5⁄9 — kiểm tra cả hai mốc."),
                ("validation", "Đúng −273.15 là hợp lệ; thấp hơn thì ném — qua constructor HOẶC sau chuyển đổi."),
            ],
        ),
        "csb-p9-player": vi_challenge(
            "Người chơi với máu bị ghim",
            "Hiện thực lớp lồng `Solution.Player`: constructor `(string name)` ném `ArgumentException` với tên null/toàn khoảng trắng; `Name` chỉ-đọc; `Health` bắt đầu 100; `TakeDamage(int)` và `Heal(int)` ném `ArgumentException` với số âm, ngoài ra máu luôn bị ghim trong [0, 100]; `IsAlive` đúng khi Health > 0.",
            [
                ("lifecycle", "Máu sàn ở 0; IsAlive dùng lớn-hơn-nghiêm-ngặt, nên 0 là chết."),
                ("bounds-and-validation", "Cả hai ghim đều quan trọng: không nhận số âm, không trả giá trị ngoài [0, 100]."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p9-counter",
            'public class Solution\n{\n    public sealed class Counter\n    {\n        private int value;\n        public int Value { get { return value; } }\n        public void Increment() { value++; }\n        public void Decrement() { if (value > 0) value--; }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class Counter\n    {\n        private int value;\n        public int Value { get { return value; } }\n        public void Increment() { value++; }\n        // near-miss: no floor — decrementing at zero drives the value\n        // negative, breaking the never-below-zero contract\n        public void Decrement() { value--; }\n    }\n}\n',
        ),
        (
            "csb-p9-rectangle",
            'public class Solution\n{\n    public sealed class Rectangle\n    {\n        private double width;\n        private double height;\n        public Rectangle(double width, double height)\n        {\n            if (width <= 0 || height <= 0)\n                throw new ArgumentException("dimensions must be positive");\n            this.width = width;\n            this.height = height;\n        }\n        public double Width { get { return width; } }\n        public double Height { get { return height; } }\n        public double Area() { return width * height; }\n        public void Scale(double factor)\n        {\n            if (factor <= 0)\n                throw new ArgumentException("factor must be positive");\n            width *= factor;\n            height *= factor;\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class Rectangle\n    {\n        private double width;\n        private double height;\n        public Rectangle(double width, double height)\n        {\n            if (width <= 0 || height <= 0)\n                throw new ArgumentException("dimensions must be positive");\n            this.width = width;\n            this.height = height;\n        }\n        public double Width { get { return width; } }\n        public double Height { get { return height; } }\n        public double Area() { return width * height; }\n        public void Scale(double factor)\n        {\n            if (factor <= 0)\n                throw new ArgumentException("factor must be positive");\n            width *= factor;\n            // near-miss: scales only the width — height is untouched, so\n            // Area() after Scale(2) is 2x instead of 4x\n        }\n    }\n}\n',
        ),
        (
            "csb-p9-temperature",
            'public class Solution\n{\n    public sealed class Temperature\n    {\n        private const double AbsoluteZeroC = -273.15;\n        private double celsius;\n        public Temperature(double celsius)\n        {\n            if (celsius < AbsoluteZeroC)\n                throw new ArgumentException("below absolute zero");\n            this.celsius = celsius;\n        }\n        public double Celsius { get { return celsius; } }\n        public static Temperature FromFahrenheit(double f)\n        {\n            return new Temperature((f - 32.0) * 5.0 / 9.0);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class Temperature\n    {\n        private const double AbsoluteZeroC = -273.15;\n        private double celsius;\n        public Temperature(double celsius)\n        {\n            if (celsius < AbsoluteZeroC)\n                throw new ArgumentException("below absolute zero");\n            this.celsius = celsius;\n        }\n        public double Celsius { get { return celsius; } }\n        public static Temperature FromFahrenheit(double f)\n        {\n            // near-miss: swapped ratio — multiplies by 9/5 instead of 5/9,\n            // so 212F yields 324C, not the boiling point 100C\n            return new Temperature((f - 32.0) * 9.0 / 5.0);\n        }\n    }\n}\n',
        ),
        (
            "csb-p9-player",
            'public class Solution\n{\n    public sealed class Player\n    {\n        private int health = 100;\n        public Player(string name)\n        {\n            if (string.IsNullOrWhiteSpace(name))\n                throw new ArgumentException("name required");\n            Name = name;\n        }\n        public string Name { get; }\n        public int Health { get { return health; } }\n        public bool IsAlive { get { return health > 0; } }\n        public void TakeDamage(int amount)\n        {\n            if (amount < 0) throw new ArgumentException("negative damage");\n            health = Math.Max(0, health - amount);\n        }\n        public void Heal(int amount)\n        {\n            if (amount < 0) throw new ArgumentException("negative heal");\n            health = Math.Min(100, health + amount);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class Player\n    {\n        private int health = 100;\n        public Player(string name)\n        {\n            if (string.IsNullOrWhiteSpace(name))\n                throw new ArgumentException("name required");\n            Name = name;\n        }\n        public string Name { get; }\n        public int Health { get { return health; } }\n        public bool IsAlive { get { return health > 0; } }\n        public void TakeDamage(int amount)\n        {\n            if (amount < 0) throw new ArgumentException("negative damage");\n            health = Math.Max(0, health - amount);\n        }\n        public void Heal(int amount)\n        {\n            if (amount < 0) throw new ArgumentException("negative heal");\n            // near-miss: no upper clamp — healing past 100 pushes health\n            // beyond the [0, 100] contract\n            health = health + amount;\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m9",
    "Checkpoint — Classes",
    "A bank account: an owner, a balance, and two doors — every mutation validated, every invariant testable.",
    20,
    r"""
## Checkpoint: the bank account

**Task:** implement nested class `Solution.BankAccount`:

1. Constructor `(string owner, decimal openingBalance)` — throws `ArgumentException` for a null/whitespace owner or a negative opening balance.
2. Read-only `Owner` and `Balance` properties.
3. `Deposit(decimal amount)` — throws `ArgumentException` unless `amount > 0`; otherwise adds to the balance.
4. `Withdraw(decimal amount)` — throws `ArgumentException` unless `amount > 0`, throws `InvalidOperationException` when funds are insufficient; otherwise subtracts.

The invariant: **the balance only ever changes through positive, funded operations.** A rejected operation must leave the balance exactly as it was.
""",
    "Checkpoint — Lớp",
    "Tài khoản ngân hàng: một chủ sở hữu, một số dư, và hai cánh cửa — mọi biến đổi đều được kiểm tra, mọi bất biến đều kiểm chứng được.",
    r"""
## Checkpoint: tài khoản ngân hàng

**Nhiệm vụ:** hiện thực lớp lồng `Solution.BankAccount`:

1. Constructor `(string owner, decimal openingBalance)` — ném `ArgumentException` khi chủ sở hữu null/toàn khoảng trắng hoặc số dư ban đầu âm.
2. Thuộc tính chỉ-đọc `Owner` và `Balance`.
3. `Deposit(decimal amount)` — ném `ArgumentException` trừ khi `amount > 0`; nếu hợp lệ thì cộng vào số dư.
4. `Withdraw(decimal amount)` — ném `ArgumentException` trừ khi `amount > 0`, ném `InvalidOperationException` khi không đủ tiền; nếu hợp lệ thì trừ khỏi số dư.

Bất biến: **số dư chỉ thay đổi qua các thao tác dương và đủ tiền.** Thao tác bị từ chối phải để số dư nguyên vẹn.
""",
    challenge(
        "csb-checkpoint-m9-task",
        "BankAccount",
        "Implement `BankAccount` exactly as described — owner validation, the two exception types, and the untouched-balance rule on every rejection.",
        CS_PRELUDE,
        [
            (
                "basics",
                "var a = new Solution.BankAccount(\"An\", 100m);\nCj.Eq(a.Owner, \"An\", \"owner kept\");\nCj.Eq(a.Balance, 100m, \"opening balance\");\na.Deposit(50m);\nCj.Eq(a.Balance, 150m, \"deposit adds\");\na.Withdraw(30m);\nCj.Eq(a.Balance, 120m, \"withdraw subtracts\");",
                "The happy path: constructor, deposit, withdraw, all reflected in Balance.",
            ),
            (
                "invariants",
                "var a = new Solution.BankAccount(\"Binh\", 120m);\nbool t1 = false;\ntry { a.Deposit(0m); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { a.Deposit(-100m); } catch (ArgumentException) { t2 = true; }\nbool t3 = false;\ntry { a.Withdraw(999m); } catch (InvalidOperationException) { t3 = true; }\nbool t4 = false;\ntry { a.Withdraw(-10m); } catch (ArgumentException) { t4 = true; }\nbool t5 = false;\ntry { new Solution.BankAccount(\"  \", 50m); } catch (ArgumentException) { t5 = true; }\nCj.True(t1 && t2 && t3 && t4 && t5, \"every invalid operation throws the right type\");\nCj.Eq(a.Balance, 120m, \"rejected operations left the balance untouched\");",
                "Zero/negative deposits, over-withdrawal, negative withdrawal, blank owner — and the balance must not move.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "BankAccount",
        "Hiện thực `BankAccount` đúng như mô tả — kiểm tra chủ sở hữu, hai loại ngoại lệ, và luật số-dư-nguyên-vẹn sau mọi thao tác bị từ chối.",
        [
            ("basics", "Đường vui: constructor, nạp, rút — tất cả phản ánh vào Balance."),
            ("invariants", "Nạp 0/âm, rút vượt số dư, rút số âm, chủ rỗng — và số dư không được xê dịch."),
        ],
    ),
    solution='public class Solution\n{\n    public sealed class BankAccount\n    {\n        private decimal balance;\n        public BankAccount(string owner, decimal openingBalance)\n        {\n            if (string.IsNullOrWhiteSpace(owner))\n                throw new ArgumentException("owner required");\n            if (openingBalance < 0)\n                throw new ArgumentException("negative opening balance");\n            Owner = owner;\n            balance = openingBalance;\n        }\n        public string Owner { get; }\n        public decimal Balance { get { return balance; } }\n        public void Deposit(decimal amount)\n        {\n            if (amount <= 0)\n                throw new ArgumentException("non-positive deposit");\n            balance += amount;\n        }\n        public void Withdraw(decimal amount)\n        {\n            if (amount <= 0)\n                throw new ArgumentException("non-positive withdrawal");\n            if (amount > balance)\n                throw new InvalidOperationException("insufficient funds");\n            balance -= amount;\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public sealed class BankAccount\n    {\n        private decimal balance;\n        public BankAccount(string owner, decimal openingBalance)\n        {\n            if (string.IsNullOrWhiteSpace(owner))\n                throw new ArgumentException("owner required");\n            if (openingBalance < 0)\n                throw new ArgumentException("negative opening balance");\n            Owner = owner;\n            balance = openingBalance;\n        }\n        public string Owner { get; }\n        public decimal Balance { get { return balance; } }\n        public void Deposit(decimal amount)\n        {\n            // near-miss: no positivity guard — a "deposit" of -100 silently\n            // drains the account, and 0 counts as business as usual\n            balance += amount;\n        }\n        public void Withdraw(decimal amount)\n        {\n            if (amount <= 0)\n                throw new ArgumentException("non-positive withdrawal");\n            if (amount > balance)\n                throw new InvalidOperationException("insufficient funds");\n            balance -= amount;\n        }\n    }\n}\n',
)

print("module 9 authored")
