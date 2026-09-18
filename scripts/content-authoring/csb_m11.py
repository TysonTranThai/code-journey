#!/usr/bin/env python3
"""C# — Beginner — Module 11: csb-models.

Enums, records, and the value/reference split: modeling domain data that
compares by contents when it should and by identity when it must. Ws break
exactly one modeling rule. House conventions: Ws are behavioral near-misses,
tests discriminate.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-models"

write_module(
    M,
    "Enums, Records, and Data Modeling",
    "Fixed option sets, value-shaped data, and the class/struct/record decision — modeling domain data honestly.",
    "Enum, Record, và Mô hình hóa dữ liệu",
    "Tập lựa chọn cố định, dữ liệu dạng-giá-trị, và quyết định class/struct/record — mô hình hóa dữ liệu một cách trung thực.",
    ["csb-m11-enums", "csb-m11-records", "csb-m11-structs", "csb-checkpoint-m11"],
    ["csb-p11-models"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m11-enums",
    "Enums: names for fixed sets",
    "An enum turns magic ints into a closed set of named constants — with no legal values outside the set.",
    12,
    r"""
## From magic numbers to names

```csharp
// before: what is 2?
if (status == 2) { ... }

// after: the set IS the documentation
enum OrderStatus { Pending, Paid, Shipped, Cancelled }

if (status == OrderStatus.Paid) { ... }
```

`OrderStatus.Paid` is a named constant of the enum type. Under the hood each member is an `int` (0, 1, 2, 3 by default), but the variable's *type* restricts what it can hold: an `OrderStatus` can't silently become `42`.

## Casting and safety

The escape hatch is explicit casting — and C# will happily cast an out-of-range number into the enum type, because enums are thin wrappers over ints:

```csharp
OrderStatus s = OrderStatus.Shipped;
int raw = (int)s;                     // 2
OrderStatus bogus = (OrderStatus)99;  // compiles! not a member
```

So a method receiving an enum can still receive a bogus cast value; if the set must be enforced, validate: `Enum.IsDefined(typeof(OrderStatus), 99)` is false. For beginners the rule that matters: **use enums to name fixed sets; never rely on them to reject arbitrary ints.**
""",
    "Enum: tên cho tập cố định",
    "Enum biến số ma thuật thành một tập đóng các hằng được đặt tên — không có giá trị hợp lệ nào ngoài tập.",
    r"""
## Từ số ma thuật sang tên

```csharp
// trước: 2 là gì?
if (status == 2) { ... }

// sau: chính tập hợp là tài liệu
enum OrderStatus { Pending, Paid, Shipped, Cancelled }

if (status == OrderStatus.Paid) { ... }
```

`OrderStatus.Paid` là một hằng được đặt tên của kiểu enum. Bên dưới, mỗi thành viên là một `int` (0, 1, 2, 3 theo mặc định), nhưng *kiểu* của biến giới hạn nó có thể giữ gì: một `OrderStatus` không thể lặng lẽ trở thành `42`.

## Ép kiểu và an toàn

Lối thoát là ép kiểu tường minh — và C# sẵn sàng ép một số ngoài tập vào kiểu enum, vì enum chỉ là lớp mỏng bọc int:

```csharp
OrderStatus s = OrderStatus.Shipped;
int raw = (int)s;                     // 2
OrderStatus bogus = (OrderStatus)99;  // biên dịch được! không phải thành viên
```

Vậy một phương thức nhận enum vẫn có thể nhận giá trị ép-vô-lý; nếu tập phải được thực thi, hãy kiểm tra: `Enum.IsDefined(typeof(OrderStatus), 99)` là false. Quy tắc đáng nhớ: **dùng enum để đặt tên cho tập cố định; đừng dựa vào enum để từ chối int tùy ý.**
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m11-records",
    "Records: data that compares by contents",
    "Two records with the same values are Equal — value semantics with one declaration.",
    13,
    r"""
## The class equality trap

```csharp
class PointC { public double X, Y; }
var a = new PointC { X = 1, Y = 2 };
var b = new PointC { X = 1, Y = 2 };
// a == b is false! a.Equals(b) is false!
```

Reference types compare by *identity* by default: two separately built objects are never equal, even with identical contents. Overriding `Equals`/`GetHashCode` correctly by hand is subtle and easy to get wrong.

## Records do it for you

```csharp
record Point(double X, double Y);

var p1 = new Point(1, 2);
var p2 = new Point(1, 2);
Console.WriteLine(p1 == p2);        // True
Console.WriteLine(p1.Equals(p2));   // True
Console.WriteLine(p1);              // Point { X = 1, Y = 2 }
```

A **record** generates value-based `Equals`, `GetHashCode`, a readable `ToString`, and an immutable-by-default shape. It's the right default for data you pass around: messages, coordinates, line items, query results.

`with` copies-and-changes without mutating:

```csharp
var moved = p1 with { X = 10 };   // new record: (10, 2); p1 unchanged
```

Immutability plus value equality is exactly what "a piece of data" means — which is why records exist.
""",
    "Record: dữ liệu so sánh theo nội dung",
    "Hai record cùng giá trị là Equal — ngữ nghĩa giá trị chỉ với một dòng khai báo.",
    r"""
## Bẫy đẳng thức của class

```csharp
class PointC { public double X, Y; }
var a = new PointC { X = 1, Y = 2 };
var b = new PointC { X = 1, Y = 2 };
// a == b là false! a.Equals(b) là false!
```

Kiểu tham chiếu so sánh theo *định danh* theo mặc định: hai đối tượng dựng riêng biệt không bao giờ bằng nhau, kể cả khi nội dung giống hệt. Tự override `Equals`/`GetHashCode` đúng cách thì tinh vi và dễ sai.

## Record làm thay bạn

```csharp
record Point(double X, double Y);

var p1 = new Point(1, 2);
var p2 = new Point(1, 2);
Console.WriteLine(p1 == p2);        // True
Console.WriteLine(p1.Equals(p2));   // True
Console.WriteLine(p1);              // Point { X = 1, Y = 2 }
```

Một **record** tự sinh `Equals`/`GetHashCode` theo giá trị, `ToString` dễ đọc, và hình dạng bất biến theo mặc định. Đó là mặc định đúng cho dữ liệu bạn chuyển tay nhau: thông điệp, tọa độ, dòng hóa đơn, kết quả truy vấn.

`with` sao-chép-và-đổi mà không biến đổi bản gốc:

```csharp
var moved = p1 with { X = 10 };   // record mới: (10, 2); p1 nguyên vẹn
```

Bất biến cộng đẳng-thức-theo-giá-trị chính xác là nghĩa của "một phần dữ liệu" — vì sao record tồn tại.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m11-structs",
    "Structs vs classes: value semantics",
    "A struct variable *is* the data; a class variable points at it. Copies, `ref`, and when each shape fits.",
    12,
    r"""
## The copy rule

```csharp
struct PointS { public double X, Y; }
class  PointC { public double X, Y; }

var s1 = new PointS { X = 1 };
var s2 = s1;  s2.X = 99;    // s1.X still 1 — s2 is a COPY

var c1 = new PointC { X = 1 };
var c2 = c1;  c2.X = 99;    // c1.X is 99! c2 is the SAME object
```

A **struct** variable *is* the data (value type): assignment copies it. A **class** variable *points at* the data (reference type): assignment shares it. This is the single most consequential runtime difference in C#.

## Choosing

- Small, short-lived, data-like things where copying is harmless and identity is meaningless → `struct` (or better, `readonly record struct`).
- Entities with identity and lifetime — a bank account, a UI window → `class`.
- Data passed around and compared by contents → `record` (a reference type with value semantics).

Beginner guidance: default to classes and records; reach for structs only when copying is genuinely what you want. Misusing big mutable structs causes mysterious copy-bugs — the exact trap the practice below exercises.
""",
    "Struct và class: ngữ nghĩa giá trị",
    "Biến struct *chính là* dữ liệu; biến class trỏ tới dữ liệu. Bản sao, `ref`, và khi nào dạng nào phù hợp.",
    r"""
## Luật sao chép

```csharp
struct PointS { public double X, Y; }
class  PointC { public double X, Y; }

var s1 = new PointS { X = 1 };
var s2 = s1;  s2.X = 99;    // s1.X vẫn 1 — s2 là BẢN SAO

var c1 = new PointC { X = 1 };
var c2 = c1;  c2.X = 99;    // c1.X là 99! c2 là CÙNG đối tượng
```

Biến **struct** *chính là* dữ liệu (value type): phép gán sao chép nó. Biến **class** *trỏ tới* dữ liệu (reference type): phép gán dùng chung nó. Đây là khác biệt thời-giant-chạy quan trọng nhất trong C#.

## Chọn kiểu nào

- Thứ nhỏ, ngắn hạn, dạng dữ liệu, việc sao chép vô hại và định danh vô nghĩa → `struct` (tốt hơn là `readonly record struct`).
- Thực thể có định danh và vòng đời — tài khoản ngân hàng, cửa sổ UI → `class`.
- Dữ liệu được chuyển tay và so sánh theo nội dung → `record` (kiểu tham chiếu với ngữ nghĩa giá trị).

Hướng dẫn cho người mới: mặc định dùng class và record; chỉ dùng struct khi sao chép thật sự là điều bạn muốn. Lạm dụng struct lớn có thể biến đổi sẽ tạo ra những bug sao-chép bí ẩn — đúng cái bẫy phần luyện tập dưới đây.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p11-models",
    "Data modeling workout",
    "Order statuses, shipments, points, and batches — enums, records, and value semantics under discriminating tests.",
    "Luyện tập mô hình dữ liệu",
    "Trạng thái đơn, lô hàng, điểm, và lô sản xuất — enum, record, và ngữ nghĩa giá trị dưới các bài kiểm tra phân biệt.",
    "csb-m11-structs",
    40,
    "beginner",
    [
        challenge(
            "csb-p11-statusflow",
            "Order status flow",
            "Implement in `Solution`: `enum OrderStatus { Pending, Paid, Shipped, Cancelled }` and `static OrderStatus? NextStatus(OrderStatus current)` returning the next step in Pending → Paid → Shipped; `Cancelled` has no next step and returns `null`. Return type is the nullable enum `OrderStatus?`.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.True(Solution.NextStatus(Solution.OrderStatus.Pending) == Solution.OrderStatus.Paid, \"Pending -> Paid\");\nCj.True(Solution.NextStatus(Solution.OrderStatus.Paid) == Solution.OrderStatus.Shipped, \"Paid -> Shipped\");\nCj.True(Solution.NextStatus(Solution.OrderStatus.Shipped) == null, \"Shipped is terminal\");",
                    "The chain moves exactly one step; the end of the chain is null.",
                ),
                (
                    "cancel",
                    "Cj.True(Solution.NextStatus(Solution.OrderStatus.Cancelled) == null, \"Cancelled is terminal\");\nCj.True((int)Solution.OrderStatus.Paid == 1, \"default numbering: Pending=0, Paid=1\");",
                    "Both terminal states return null; default numbering starts at 0 in declaration order.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p11-money",
            "Money as a record",
            "Implement nested record `Solution.Money(decimal Amount, string Currency)` inside a static holder, plus `static Money Add(Money a, Money b)` that returns a new Money and throws `ArgumentException` when the currencies differ.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var m1 = new Solution.Money(10m, \"VND\");\nvar m2 = new Solution.Money(15m, \"VND\");\nvar sum = Solution.Money.Add(m1, m2);\nCj.Eq(sum.Amount, 25m, \"amounts add\");\nCj.Eq(sum.Currency, \"VND\", \"currency kept\");\nCj.True(m1.Amount == 10m, \"inputs unchanged — Add returns a new record\");",
                    "Add must not mutate its inputs; records are immutable data.",
                ),
                (
                    "equality",
                    "var a = new Solution.Money(5m, \"USD\");\nvar b = new Solution.Money(5m, \"USD\");\nCj.True(a == b, \"records with equal contents are equal\");\nbool threw = false;\ntry { Solution.Money.Add(a, new Solution.Money(1m, \"EUR\")); } catch (ArgumentException) { threw = true; }\nCj.True(threw, \"mixed currencies rejected\");\nbool threw2 = false;\ntry { Solution.Money.Add(new Solution.Money(1m, \"vnd\"), new Solution.Money(2m, \"VND\")); } catch (ArgumentException) { threw2 = true; }\nCj.True(threw2, \"case-different codes are different currencies\");",
                    "Value equality is the record contract; mismatch must throw before any arithmetic — and string comparison is the contract, so case counts.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p11-shipment",
            "Shipment with enum + record",
            "Implement in `Solution`: `enum Carrier { Air, Sea, Ground }` with a method `static int Days(Carrier c)` returning 1, 5, 3 respectively (unknown/undefined carrier values throw `ArgumentException`), and record `Shipment(string Id, Carrier Via)` plus `static Carrier Fastest(Carrier a, Carrier b)` returning whichever has fewer `Days`.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.Days(Solution.Carrier.Air), 1, \"air\");\nCj.Eq(Solution.Days(Solution.Carrier.Sea), 5, \"sea\");\nCj.Eq(Solution.Days(Solution.Carrier.Ground), 3, \"ground\");\nCj.True(Solution.Fastest(Solution.Carrier.Sea, Solution.Carrier.Ground) == Solution.Carrier.Ground, \"ground beats sea\");",
                    "Days is a pure lookup; Fastest compares through Days.",
                ),
                (
                    "edge",
                    "bool threw = false;\ntry { Solution.Days((Solution.Carrier)77); } catch (ArgumentException) { threw = true; }\nCj.True(threw, \"undefined carrier rejected\");\nCj.True(Solution.Fastest(Solution.Carrier.Air, Solution.Carrier.Air) == Solution.Carrier.Air, \"tie returns either (air)\");",
                    "Enum.IsDefined is the honest guard for cast-in values; ties are unconstrained.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p11-batch",
            "Value vs reference: the batch",
            "Implement in `Solution`: `struct Batch { public int Count; }` and `static (int First, int Second) CopyProbe()` that creates a `Batch` with `Count = 1`, copies it to a second variable, sets the copy's `Count = 2`, and returns BOTH counts. Also `static (int First, int Second) RefProbe()` doing the same with `class BatchRef { public int Count; }`.",
            CS_PRELUDE,
            [
                (
                    "struct-copies",
                    "var probe = Solution.CopyProbe();\nCj.Eq(probe.First, 1, \"original struct untouched\");\nCj.Eq(probe.Second, 2, \"copy mutated independently\");",
                    "Struct assignment copies: the second variable's write cannot reach the first.",
                ),
                (
                    "class-shares",
                    "var probe = Solution.RefProbe();\nCj.Eq(probe.First, 2, \"class shares: both see 2\");\nCj.Eq(probe.Second, 2, \"same object\");",
                    "Class assignment shares one object: both variables report 2 — the discriminating pair.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p11-statusflow": vi_challenge(
            "Luồng trạng thái đơn hàng",
            "Hiện thực trong `Solution`: `enum OrderStatus { Pending, Paid, Shipped, Cancelled }` và `static OrderStatus? NextStatus(OrderStatus current)` trả bước kế tiếp theo Pending → Paid → Shipped; `Cancelled` không có bước kế tiếp và trả `null`. Kiểu trả về là enum nullable `OrderStatus?`.",
            [
                ("normal", "Chuỗi tiến đúng một bước; điểm cuối của chuỗi là null."),
                ("cancel", "Cả hai trạng thái cuối trả null; đánh số mặc định bắt đầu từ 0 theo thứ tự khai báo."),
            ],
        ),
        "csb-p11-money": vi_challenge(
            "Tiền như một record",
            "Hiện thực record lồng `Solution.Money(decimal Amount, string Currency)` trong một lớp tĩnh chứa, cùng `static Money Add(Money a, Money b)` trả một Money mới và ném `ArgumentException` khi hai loại tiền khác nhau.",
            [
                ("normal", "Add không được biến đổi đầu vào; record là dữ liệu bất biến."),
                ("equality", "Đẳng thức theo giá trị là hợp đồng của record; sai tiền tệ phải ném trước mọi phép tính — hợp đồng là so sánh chuỗi, nên chữ hoa/thường cũng được tính."),
            ],
        ),
        "csb-p11-shipment": vi_challenge(
            "Lô hàng với enum + record",
            "Hiện thực trong `Solution`: `enum Carrier { Air, Sea, Ground }` với phương thức `static int Days(Carrier c)` trả 1, 5, 3 theo thứ tự (giá trị carrier không định nghĩa sẽ ném `ArgumentException`), và record `Shipment(string Id, Carrier Via)` cùng `static Carrier Fastest(Carrier a, Carrier b)` trả bên có `Days` ít hơn.",
            [
                ("normal", "Days là tra cứu thuần; Fastest so sánh qua Days."),
                ("edge", "Enum.IsDefined là lớp chặn trung thực cho giá trị ép-vô-lý; hòa thì trả bên nào cũng được."),
            ],
        ),
        "csb-p11-batch": vi_challenge(
            "Giá trị và tham chiếu: lô hàng",
            "Hiện thực trong `Solution`: `struct Batch { public int Count; }` và `static (int First, int Second) CopyProbe()` tạo một `Batch` với `Count = 1`, gán cho biến thứ hai, đặt `Count = 2` trên bản sao, rồi trả CẢ HAI số đếm. Cùng `static (int First, int Second) RefProbe()` làm y hệt với `class BatchRef { public int Count; }`.",
            [
                ("struct-copies", "Gán struct là sao chép: ghi trên biến thứ hai không với tới biến đầu."),
                ("class-shares", "Gán class là dùng chung một đối tượng: cả hai biến đều báo 2 — cặp phân biệt."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p11-statusflow",
            'public class Solution\n{\n    public enum OrderStatus { Pending, Paid, Shipped, Cancelled }\n    public static OrderStatus? NextStatus(OrderStatus current)\n    {\n        switch (current)\n        {\n            case OrderStatus.Pending: return OrderStatus.Paid;\n            case OrderStatus.Paid: return OrderStatus.Shipped;\n            default: return null;\n        }\n    }\n}\n',
            'public class Solution\n{\n    public enum OrderStatus { Pending, Paid, Shipped, Cancelled }\n    public static OrderStatus? NextStatus(OrderStatus current)\n    {\n        // near-miss: treats Cancelled as if it still needed payment — the\n        // terminal state incorrectly advances to Paid\n        if (current == OrderStatus.Cancelled) return OrderStatus.Paid;\n        switch (current)\n        {\n            case OrderStatus.Pending: return OrderStatus.Paid;\n            case OrderStatus.Paid: return OrderStatus.Shipped;\n            default: return null;\n        }\n    }\n}\n',
        ),
        (
            "csb-p11-money",
            'public class Solution\n{\n    public sealed record Money(decimal Amount, string Currency)\n    {\n        public static Money Add(Money a, Money b)\n        {\n            if (a.Currency != b.Currency)\n                throw new ArgumentException("currency mismatch");\n            return new Money(a.Amount + b.Amount, a.Currency);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed record Money(decimal Amount, string Currency)\n    {\n        public static Money Add(Money a, Money b)\n        {\n            // near-miss: compares currencies case-INSENSITIVELY - "vnd" and\n            // "VND" merge into one currency instead of throwing, and the\n            // result carries b\'s casing\n            if (!string.Equals(a.Currency, b.Currency, StringComparison.OrdinalIgnoreCase))\n                throw new ArgumentException("currency mismatch");\n            return new Money(a.Amount + b.Amount, b.Currency);\n        }\n    }\n}\n',
        ),
        (
            "csb-p11-shipment",
            'public class Solution\n{\n    public enum Carrier { Air, Sea, Ground }\n    public sealed record Shipment(string Id, Carrier Via);\n    public static int Days(Carrier c)\n    {\n        if (!Enum.IsDefined(typeof(Carrier), c))\n            throw new ArgumentException("undefined carrier");\n        switch (c)\n        {\n            case Carrier.Air: return 1;\n            case Carrier.Sea: return 5;\n            case Carrier.Ground: return 3;\n            default: throw new ArgumentException("undefined carrier");\n        }\n    }\n    public static Carrier Fastest(Carrier a, Carrier b) { return Days(a) <= Days(b) ? a : b; }\n}\n',
            'public class Solution\n{\n    public enum Carrier { Air, Sea, Ground }\n    public sealed record Shipment(string Id, Carrier Via);\n    public static int Days(Carrier c)\n    {\n        switch (c)\n        {\n            case Carrier.Air: return 1;\n            case Carrier.Sea: return 5;\n            case Carrier.Ground: return 3;\n            default: throw new ArgumentException("undefined carrier");\n        }\n    }\n    public static Carrier Fastest(Carrier a, Carrier b)\n    {\n        // near-miss: swapped comparison — returns the SLOWER carrier\n        return Days(a) > Days(b) ? a : b;\n    }\n}\n',
        ),
        (
            "csb-p11-batch",
            'public class Solution\n{\n    public struct Batch { public int Count; }\n    public sealed class BatchRef { public int Count; }\n    public static (int First, int Second) CopyProbe()\n    {\n        var b1 = new Batch { Count = 1 };\n        var b2 = b1;\n        b2.Count = 2;\n        return (b1.Count, b2.Count);\n    }\n    public static (int First, int Second) RefProbe()\n    {\n        var r1 = new BatchRef { Count = 1 };\n        var r2 = r1;\n        r2.Count = 2;\n        return (r1.Count, r2.Count);\n    }\n}\n',
            'public class Solution\n{\n    public struct Batch { public int Count; }\n    public sealed class BatchRef { public int Count; }\n    public static (int First, int Second) CopyProbe()\n    {\n        var b1 = new Batch { Count = 1 };\n        var b2 = b1;\n        b2.Count = 2;\n        return (b1.Count, b2.Count);\n    }\n    public static (int First, int Second) RefProbe()\n    {\n        var r1 = new BatchRef { Count = 1 };\n        var r2 = r1;\n        // near-miss: replaces the reference instead of writing through it -\n        // the shared object is never mutated, so RefProbe reports 1,2 and\n        // fails to demonstrate class sharing\n        r2 = new BatchRef { Count = 2 };\n        // near-miss: "fixes" sharing by re-assigning r2 to a fresh object —\n        // so the original escapes unmutated and RefProbe reports 1,2\n        r2 = new BatchRef { Count = 2 };\n        return (r1.Count, r2.Count);\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m11",
    "Checkpoint — Data models",
    "A catalog of products: an enum category, a record line item with value equality, and aggregation over a list.",
    20,
    r"""
## Checkpoint: the product catalog

**Task:** implement in `Solution`:

1. `enum Category { Books, Electronics, Food }`
2. `record Item(string Name, Category Cat, decimal Price)`
3. `static decimal Total(List<Item> items, Category cat)` — sum of prices for items in exactly that category; null/empty list or no matches → 0.
4. `static Item? MostExpensive(List<Item> items)` — the item with the highest price; null/empty → `null`. Ties: return any one.
""",
    "Checkpoint — Mô hình dữ liệu",
    "Danh mục sản phẩm: một enum danh mục, một record dòng hàng với đẳng thức theo giá trị, và tổng hợp trên danh sách.",
    r"""
## Checkpoint: danh mục sản phẩm

**Nhiệm vụ:** hiện thực trong `Solution`:

1. `enum Category { Books, Electronics, Food }`
2. `record Item(string Name, Category Cat, decimal Price)`
3. `static decimal Total(List<Item> items, Category cat)` — tổng giá của các món thuộc đúng danh mục đó; danh sách null/rỗng hoặc không có món nào → 0.
4. `static Item? MostExpensive(List<Item> items)` — món có giá cao nhất; null/rỗng → `null`. Hòa: trả món nào cũng được.
""",
    challenge(
        "csb-checkpoint-m11-task",
        "ProductCatalog",
        "Implement `Category`, `Item`, `Total`, and `MostExpensive` — filtering is by the enum value; records give you equality for free.",
        CS_PRELUDE,
        [
            (
                "totals",
                "var items = new List<Solution.Item>\n{\n    new Solution.Item(\"Book A\", Solution.Category.Books, 10m),\n    new Solution.Item(\"Cable\", Solution.Category.Electronics, 25m),\n    new Solution.Item(\"Book B\", Solution.Category.Books, 15m),\n};\nCj.Eq(Solution.Total(items, Solution.Category.Books), 25m, \"books only\");\nCj.Eq(Solution.Total(items, Solution.Category.Food), 0m, \"no food\");\nCj.Eq(Solution.Total(null, Solution.Category.Books), 0m, \"null list\");",
                "Category filter is exact; empty results are 0, not exceptions.",
            ),
            (
                "record-equality-and-max",
                "var a = new Solution.Item(\"X\", Solution.Category.Food, 7m);\nvar b = new Solution.Item(\"X\", Solution.Category.Food, 7m);\nCj.True(a == b, \"records compare by contents\");\nvar items = new List<Solution.Item>\n{\n    new Solution.Item(\"Cable\", Solution.Category.Electronics, 25m),\n    new Solution.Item(\"Book A\", Solution.Category.Books, 10m),\n};\nCj.Eq(Solution.MostExpensive(items), items[0], \"highest price wins\");\nCj.Eq(Solution.MostExpensive(new List<Solution.Item>()), null, \"empty\");",
                "Value equality on records, max-by-price, and the null/empty contract.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "ProductCatalog",
        "Hiện thực `Category`, `Item`, `Total`, và `MostExpensive` — lọc theo giá trị enum; record cho bạn đẳng thức miễn phí.",
        [
            ("totals", "Bộ lọc danh mục là chính xác; kết quả rỗng là 0, không phải ngoại lệ."),
            ("record-equality-and-max", "Đẳng thức giá trị trên record, tìm max theo giá, và hợp đồng null/rỗng."),
        ],
    ),
    solution='public class Solution\n{\n    public enum Category { Books, Electronics, Food }\n    public sealed record Item(string Name, Category Cat, decimal Price);\n    public static decimal Total(List<Item> items, Category cat)\n    {\n        if (items == null) return 0m;\n        decimal sum = 0m;\n        foreach (Item it in items)\n        {\n            if (it.Cat == cat) sum += it.Price;\n        }\n        return sum;\n    }\n    public static Item MostExpensive(List<Item> items)\n    {\n        if (items == null || items.Count == 0) return null;\n        Item best = items[0];\n        foreach (Item it in items)\n        {\n            if (it.Price > best.Price) best = it;\n        }\n        return best;\n    }\n}\n',
    wrong='public class Solution\n{\n    public enum Category { Books, Electronics, Food }\n    public sealed record Item(string Name, Category Cat, decimal Price);\n    public static decimal Total(List<Item> items, Category cat)\n    {\n        if (items == null) return 0m;\n        decimal sum = 0m;\n        foreach (Item it in items)\n        {\n            // near-miss: compares the enum by its int VALUE instead of the\n            // member — still works here, but the real defect: adds every\n            // item\'s price regardless of category\n            sum += it.Price;\n        }\n        return sum;\n    }\n    public static Item MostExpensive(List<Item> items)\n    {\n        if (items == null || items.Count == 0) return null;\n        Item best = items[0];\n        foreach (Item it in items)\n        {\n            if (it.Price > best.Price) best = it;\n        }\n        return best;\n    }\n}\n',
)

print("module 11 authored")
