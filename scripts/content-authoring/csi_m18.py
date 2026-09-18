#!/usr/bin/env python3
"""C# — Intermediate — Module 18: csi-patterns.

Design patterns in practice: each one goes problem → naive → why the naive
hurts → pattern → tradeoff. Graded as small builds; Ws are near-miss
implementations with a real behavioral flaw.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-patterns"

write_module(
    M,
    "Design Patterns in Practice",
    "Strategy, Factory, Builder, Adapter, Decorator, Repository, Observer — each taught as a problem first, with tradeoffs and when NOT to use it.",
    "Design Patterns trong Thực hành",
    "Strategy, Factory, Builder, Adapter, Decorator, Repository, Observer — mỗi pattern dạy từ bài toán, kèm đánh đổi và khi nào KHÔNG dùng.",
    ["pattern-catalog", "pattern-builds", "csi-checkpoint-m18"],
    ["csi-p18-patterns"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "pattern-catalog",
    "Patterns as Vocabulary, Not Ritual",
    "The pattern shapes you will actually use, learned from the problem each one answers.",
    22,
    r"""
## How to learn patterns without cargo-culting them

A design pattern is a *named, reusable solution shape* to a problem that
recurs. The name is worth having only after you have felt the problem. So
every pattern in this module follows one arc:

1. **Problem** — the code smells it: duplication, a switch that grows on every
   change, construction code nobody can follow.
2. **Naive solution** — what you would write in a hurry.
3. **What breaks** — the concrete pain that shows up next sprint.
4. **Pattern** — the shape that names and fixes the pain.
5. **Tradeoffs** — what the pattern costs (indirection, ceremony, files).
6. **When NOT to use it** — the most skipped, most valuable part.

## The seven you will build

| Pattern | The problem it answers | The tell you need it |
|---|---|---|
| **Strategy** | one behavior, many interchangeable variants | a growing `switch` over a "mode" |
| **Factory Method** | object construction branching on input | `new` scattered behind `if`s |
| **Builder** | constructing a complex object step by step | constructor with 8 bools/strings |
| **Adapter** | an interface you need vs an interface you have | a third-party shape leaking in |
| **Decorator** | layering optional behavior on a core | N boolean flags each wrapping a step |
| **Repository** | persistence details leaking into logic | SQL in a business method |
| **Observer** | one event, many reactions, decoupled | publisher calling 5 concrete subscribers |

## The universal caution

Patterns add indirection. Indirection is a cost you pay for a benefit you
must actually have. "We might need it later" is not a benefit. The honest
sequence in real work: write it naive, feel the pain, *then* reach for the
named shape — which is exactly how this module grades you.
""",
    "Patterns là Từ vựng, không phải Nghi lễ",
    "Các hình dạng pattern bạn thực sự dùng, học từ bài toán mà mỗi pattern trả lời.",
    r"""
## Học pattern mà không thành nghi lễ

Design pattern là *hình dạng giải pháp đặt tên, tái sử dụng* cho một bài toán
lặp lại. Cái tên chỉ có giá trị sau khi bạn đã cảm nhận bài toán. Nên mọi
pattern trong module này đi theo một cung:

1. **Bài toán** — code có mùi: trùng lặp, switch lớn dần theo mỗi thay đổi,
   code khởi tạo không ai đọc nổi.
2. **Giải pháp ngây thơ** — thứ bạn viết trong lúc vội.
3. **Cái gì vỡ** — cơn đau cụ thể xuất hiện ở sprint sau.
4. **Pattern** — hình dạng có tên vá cơn đau.
5. **Đánh đổi** — pattern tốn gì (gián tiếp, nghi thức, thêm file).
6. **Khi nào KHÔNG dùng** — phần hay bị bỏ qua nhất, cũng giá trị nhất.

## Bảy pattern bạn sẽ xây

| Pattern | Bài toán nó trả lời | Dấu hiệu bạn cần nó |
|---|---|---|
| **Strategy** | một hành vi, nhiều biến thể thay thế được | `switch` theo "mode" lớn dần |
| **Factory Method** | khởi tạo object rẽ nhánh theo input | `new` rải rác sau các `if` |
| **Builder** | dựng object phức tạp từng bước | constructor với 8 bool/string |
| **Adapter** | interface bạn cần vs interface bạn có | hình dạng bên thứ ba rỉ vào |
| **Decorator** | xếp lớp hành vi tùy chọn lên lõi | N cờ boolean, mỗi cờ bọc một bước |
| **Repository** | chi tiết persistence rỉ vào logic | SQL trong method nghiệp vụ |
| **Observer** | một sự kiện, nhiều phản ứng, tách rời | publisher gọi 5 subscriber cụ thể |

## Lưu ý phổ quát

Pattern thêm gián tiếp. Gián tiếp là cái giá bạn trả cho một lợi ích bạn phải
thực sự có. "Có thể cần sau" không phải lợi ích. Trình tự trung thực trong
công việc thật: viết ngây thơ trước, cảm nhận cơn đau, *rồi* mới với tới hình
dạng có tên — đúng cách module này chấm điểm bạn.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "pattern-builds",
    "Reading the Shapes in Code",
    "The same seven patterns as minimal C# skeletons — what you will build in the practice, with the tradeoff spelled out.",
    24,
    r"""
## Minimal skeletons (you build them for real next)

```csharp
// Strategy: variants behind one interface; the context never changes
interface IShipping { decimal Cost(Order o); }
sealed class FlatShipping : IShipping { ... }
sealed class WeightShipping : IShipping { ... }
// context takes IShipping — adding a variant touches no existing file

// Factory Method: the switch lives in exactly one place
static IShipping Create(string kind) => kind switch { ... };

// Builder: stepwise construction, invalid states unrepresentable
var req = new RequestBuilder().WithUrl(u).WithHeader("k", "v").Build();

// Adapter: wrap what exists, expose what's needed
sealed class LegacyTaxAdapter : ITaxCalculator { readonly LegacyTax _l; ... }

// Decorator: same interface, wraps one, adds one behavior
sealed class RetryingClient : IApiClient { readonly IApiClient _inner; ... }

// Repository: persistence behind an interface the domain owns
interface IOrderRepository { Order? Find(int id); void Save(Order o); }

// Observer: publisher knows only EventHandler<TArgs>
sealed class EventBus { public event EventHandler<OrderArgs>? Placed; }
```

## Tradeoffs, honestly

- **Strategy/Factory** cost one extra type per variant; buy uniformity and
  open/closed growth. Skip them for exactly two variants that never change.
- **Builder** costs a fluent class per built type; buys readable construction
  and invariant enforcement in `Build()`. Skip it for ≤ 3 constructor params.
- **Adapter** costs one wrapper; buys a stable seam against code you do not
  own. Skip when you own both sides — fix the interface instead.
- **Decorator** costs a class per behavior; buys stacking behaviors without
  flag explosions. Skip when behaviors never compose.
- **Repository** costs an interface + implementation; buys testability and
  the right to change storage. Skip in tiny apps with one storage call.
- **Observer** costs event hygiene (unsubscription!); buys publishers that
  know nothing about subscribers. You met its failure modes in M4.

## Composition is the real skill

The capstone composes them: a Factory picks a Strategy, the Builder assembles
a request, a Decorator wraps the HTTP client, a Repository persists, Observer
fires side effects. None of these patterns is impressive alone — *knowing
which seam each one guards* is the skill, and the checkpoint grades exactly
that.
""",
    "Đọc các Hình dạng trong Code",
    "Cùng bảy pattern dưới dạng skeleton C# tối giản — những gì bạn sẽ xây trong phần luyện tập, kèm đánh đổi rõ ràng.",
    r"""
## Skeleton tối giản (bạn sẽ xây thật ở bài sau)

Xem các skeleton C# cho Strategy, Factory Method, Builder, Adapter,
Decorator, Repository, Observer trong bản tiếng Anh — mỗi khối là hình dạng
tối giản của một pattern.

## Đánh đổi, nói thẳng

- **Strategy/Factory** tốn thêm một type mỗi biến thể; mua tính đồng nhất và
  khả năng mở theo open/closed. Bỏ qua nếu chỉ đúng hai biến thể không bao giờ
  đổi.
- **Builder** tốn một class fluent mỗi type cần dựng; mua cách dựng dễ đọc và
  việc ép bất biến trong `Build()`. Bỏ qua nếu ≤ 3 tham số constructor.
- **Adapter** tốn một wrapper; mua đường ranh ổn định trước code bạn không sở
  hữu. Bỏ qua khi bạn sở hữu cả hai phía — sửa interface cho rồi.
- **Decorator** tốn một class mỗi hành vi; mua việc xếp chồng hành vi không cần
  bùng nổ cờ. Bỏ qua khi các hành vi không bao giờ ghép nhau.
- **Repository** tốn interface + hiện thực; mua khả năng test và quyền đổi nơi
  lưu trữ. Bỏ qua trong app nhỏ với một lệnh lưu.
- **Observer** tốn vệ sinh sự kiện (phải unsubcribe!); mua publisher không cần
  biết subscriber. Bạn đã gặp các chế độ hỏng của nó ở M4.

## Ghép mới là kỹ năng thật

Capstone ghép chúng: một Factory chọn Strategy, Builder dựng request,
Decorator bọc HTTP client, Repository lưu trữ, Observer kích phụ tác. Không
pattern nào ấn tượng khi đứng một mình — *biết mỗi pattern canh đường ranh
nào* mới là kỹ năng, và checkpoint chấm đúng điều đó.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p18-patterns",
    "Patterns Practice: Strategy, Decorator, Builder",
    "Kill a switch with Strategy, stack behavior with Decorator, and make invalid orders unrepresentable with a Builder — plus a caching bug to hunt.",
    "Luyện Patterns: Strategy, Decorator, Builder",
    "Diệt switch bằng Strategy, xếp chồng hành vi bằng Decorator, và biến order-invalid thành không-tiện-đại-diện bằng Builder — cộng một bug cache để săn.",
    "pattern-builds",
    34,
    "intermediate",
    [
        challenge(
            "csi-p18-strategy-shipping",
            "Strategy: Kill the Shipping Switch",
            r"""`LegacyCheckout.Cost` prices shipping by a mode string, and every new
carrier means another `else if`. Replace the switch with **Strategy**:

1. `IShippingCost { decimal Cost(Solution.Parcel p); }` (inside `Solution`)
2. Two implementations: `Flat` (always `3.5m`) and `Weight` (`0.8m` per kg,
   minimum `4m`)
3. `Solution.Cost(Parcel p, IShippingCost strategy)` delegates entirely —
   zero conditionals on weight/mode in `Solution.Cost` itself.

The value is *composition by the caller*: the tests pass strategies by hand,
proving the context depends only on the abstraction.

```csharp
public static class Solution
{
    public sealed class Parcel { public decimal WeightKg; }
    public interface IShippingCost { decimal Cost(Parcel p); }
    public static decimal Cost(Parcel p, IShippingCost strategy);
}
```""",
            CS_PRELUDE,
            [
                (
                    "flat and weight strategies",
                    r"""
var p = new Solution.Parcel(); p.WeightKg = 2m;
Cj.Eq(new Solution.Flat().Cost(p), 3.5m, "flat is flat");
Cj.Eq(new Solution.Weight().Cost(p), 4m, "2kg * 0.8 = 1.6 -> min 4 applies");
var heavy = new Solution.Parcel(); heavy.WeightKg = 10m;
Cj.Eq(new Solution.Weight().Cost(heavy), 8m, "10kg * 0.8");
""",
                    "Weight: cost = kg * 0.8m, but never below 4m. Flat: constant 3.5m.",
                ),
                (
                    "context delegates, callers compose",
                    r"""
var p = new Solution.Parcel(); p.WeightKg = 10m;
Cj.Eq(Solution.Cost(p, new Solution.Flat()), 3.5m, "context respects injected strategy");
Cj.Eq(Solution.Cost(p, new Solution.Weight()), 8m, "same parcel, other strategy");
var light = new Solution.Parcel(); light.WeightKg = 2m;
Cj.Eq(Solution.Cost(light, new Solution.Weight()), 4m, "min applies through context too");
""",
                    "Solution.Cost must contain no branching — it only forwards to the injected strategy.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p18-decorator-logger",
            "Decorator: Stack Behaviors on a Client",
            r"""`IApiClient.Send(string path)` returns `"200:" + path`. Build a
**Decorator** stack around it — each decorator wraps exactly one
`IApiClient` and adds one behavior:

- `Caching` — returns the inner response without calling inner again for a
  path it has already served (expose `InnerCalls` count).
- `Uppercase` — transforms the response to upper-case (applies after inner,
  so caching stores the original and uppercasing runs every call).

`Solution.Run()` builds `new Uppercase(new Caching(new Base()))` and issues
`"a"`, `"a"`, `"b"` — then the tests verify the call counts and outputs.

```csharp
public static class Solution
{
    public interface IApiClient { string Send(string path); }
    public sealed class Caching : IApiClient { public int InnerCalls; /* wraps one IApiClient */ }
    public sealed class Uppercase : IApiClient { /* wraps one IApiClient */ }
    public static string[] Run();
}
```""",
            CS_PRELUDE,
            [
                (
                    "caching serves repeat paths once",
                    r"""
var c = new Solution.Caching(new Solution.Base());
Cj.Eq(c.Send("a"), "200:a", "first call passes through");
Cj.Eq(c.Send("a"), "200:a", "repeat served from cache");
Cj.Eq(c.InnerCalls, 1, "inner hit exactly once");
""",
                    "Caching stores the inner response per path; a repeat path must not touch inner.",
                ),
                (
                    "decorator stack composes",
                    r"""
string[] r = Solution.Run();
Cj.Eq(r[0], "200:A", "uppercased a");
Cj.Eq(r[1], "200:A", "cache + uppercase still correct");
Cj.Eq(r[2], "200:B", "different path, fresh inner call");
""",
                    "Order: Uppercase(Caching(Base)). Uppercase transforms AFTER the (possibly cached) inner response.",
                ),
                (
                    "stack calls inner the right number of times",
                    r"""
var cache = new Solution.Caching(new Solution.Base());
cache.Send("a"); cache.Send("a"); cache.Send("b");
Cj.Eq(cache.InnerCalls, 2, "two distinct paths, two inner calls");
""",
                    "With Uppercase(Caching(Base)), inner is called once per distinct path.",
                ),
            ],
            level="mini-build",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p18-builder-order",
            "Builder: Valid Orders Only",
            r"""`OrderReq` has required fields and derived invariants that are too
easy to get wrong by hand. Build a **Builder** whose `Build()` enforces them
or throws:

- `WithCustomer(string)` — required, non-empty; `Build()` throws if missing
- `WithItem(string sku, int qty, decimal price)` — repeatable; `qty` must be
  ≥ 1 (throw `ArgumentException` in `WithItem` itself)
- `WithRush()` — flags rush delivery
- `Build()` throws when: no customer, no items, or a rush order with more
  than 10 total items (business rule)

Expose the built fields the tests read: `Customer`, `TotalQty`, `Items`
(count), `Rush`.

```csharp
public static class Solution
{
    public sealed class OrderReq { public string Customer = ""; public int TotalQty; public int Items; public bool Rush; }
    public sealed class OrderBuilder
    {
        public OrderBuilder WithCustomer(string c);
        public OrderBuilder WithItem(string sku, int qty, decimal price);   // qty >= 1
        public OrderBuilder WithRush();
        public OrderReq Build();                                            // enforces invariants
    }
}
```""",
            CS_PRELUDE,
            [
                (
                    "happy path builds",
                    r"""
var o = new Solution.OrderBuilder()
    .WithCustomer("ann")
    .WithItem("sku", 2, 3m)
    .WithItem("sku2", 3, 1m)
    .Build();
Cj.Eq(o.Customer, "ann", "customer kept");
Cj.Eq(o.TotalQty, 5, "quantities summed");
Cj.Eq(o.Items, 2, "two lines");
Cj.Eq(o.Rush, false, "not rushed by default");
""",
                    "Straight accumulation: sum qtys, count lines, default Rush to false.",
                ),
                (
                    "invariants throw in Build",
                    r"""
Cj.True(Solution.Threw(() => new Solution.OrderBuilder().Build()), "no customer throws");
Cj.True(Solution.Threw(() => new Solution.OrderBuilder().WithCustomer("ann").Build()), "no items throws");
Cj.True(Solution.Threw(() => new Solution.OrderBuilder().WithItem("s", 0, 1m)), "qty 0 rejected in WithItem");
""",
                    "Two enforcement points: WithItem validates qty immediately; Build validates completeness.",
                ),
                (
                    "rush rule boundary",
                    r"""
var b = new Solution.OrderBuilder().WithCustomer("ann").WithRush();
for (int i = 0; i < 10; i++) b.WithItem("s" + i, 1, 1m);
b.Build();                                  // exactly 10: legal
Cj.True(Solution.RushThrew(11), "11 items rush throws");
""",
                    "Rush with MORE than 10 total items throws in Build; exactly 10 is fine.",
                ),
            ],
            level="mini-build",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p18-observer-review",
            "Debug: The Bus That Never Lets Go",
            r"""This `EventBus` leaks: subscribers it has "forgotten" still fire, and
counts drift. Diagnose and write a correct version.

Provided (broken) shape — the bug is that `Unsubscribe` does nothing:

```csharp
public sealed class EventBus            // BROKEN — do not ship this
{
    public event EventHandler<string>? Ping;
    public void Unsubscribe(EventHandler<string> h) { /* silently does nothing */ }
    public void PingAll(string msg) => Ping?.Invoke(this, msg);
}
```

Write a correct `EventBus`: `Subscribe` returns the handler for later
unsubscribing, `Unsubscribe` actually detaches, `PingAll` invokes current
subscribers in subscription order.

```csharp
public static class Solution
{
    public sealed class EventBus
    {
        public void Subscribe(EventHandler<string> h);
        public void Unsubscribe(EventHandler<string> h);
        public void PingAll(string msg);
        public int FiredCount;                     // total handler invocations
    }
}
```""",
            CS_PRELUDE,
            [
                (
                    "subscribe fires, in order",
                    r"""
var bus = new Solution.EventBus();
var got = new List<string>();
bus.Subscribe((s, e) => got.Add("a:" + e));
bus.Subscribe((s, e) => got.Add("b:" + e));
bus.PingAll("x");
Cj.Eq(string.Join("|", got), "a:x|b:x", "subscription order preserved");
""",
                    "Two subscribers: first registered, first invoked.",
                ),
                (
                    "unsubscribe detaches",
                    r"""
var bus = new Solution.EventBus();
var got = new List<string>();
EventHandler<string> h = (s, e) => got.Add("a:" + e);
bus.Subscribe(h);
bus.Subscribe((s, e) => got.Add("b:" + e));
bus.Unsubscribe(h);
bus.PingAll("x");
Cj.Eq(string.Join("|", got), "b:x", "unsubscribed handler never fires");
""",
                    "After Unsubscribe(h), h must not run — this is the leak the broken version has.",
                ),
                (
                    "invocation counting is exact",
                    r"""
var bus = new Solution.EventBus();
EventHandler<string> h1 = (s, e) => { };
EventHandler<string> h2 = (s, e) => { };
bus.Subscribe(h1);
bus.PingAll("1"); bus.PingAll("2");
bus.Subscribe(h2);
bus.PingAll("3");
bus.Unsubscribe(h1);
bus.PingAll("4");
Cj.Eq(bus.FiredCount, 5, "2+1+1+1 handler invocations");
""",
                    "FiredCount counts every handler invocation: 2 (h1 alone) + 1 (both) + 1 (h2 after h1 left) = 5.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p18-strategy-shipping": vi_challenge(
            "Strategy: Diệt Switch Vận chuyển",
            "Thay switch của `LegacyCheckout.Cost` bằng **Strategy**: 1) `IShippingCost { decimal Cost(Solution.Parcel p); }` (nằm trong `Solution`); 2) hai hiện thực `Flat` (luôn 3.5m) và `Weight` (0.8m/kg, tối thiểu 4m); 3) `Solution.Cost(Parcel p, IShippingCost strategy)` chỉ ủy quyền — không có điều kiện nào về cân nặng/mode trong thân hàm. Giá trị nằm ở phía caller: test truyền strategy bằng tay, chứng minh context chỉ phụ thuộc abstraction.",
            [
                ("flat and weight strategies", "Weight: giá = kg * 0.8m, nhưng không dưới 4m. Flat: hằng 3.5m."),
                ("context delegates, callers compose", "Solution.Cost không được có nhánh rẽ — chỉ chuyển tiếp sang strategy được inject."),
            ],
        ),
        "csi-p18-decorator-logger": vi_challenge(
            "Decorator: Xếp chồng Hành vi lên Client",
            "`IApiClient.Send(string path)` trả \"200:\" + path. Dựng chồng **Decorator** — mỗi decorator bọc đúng một `IApiClient` và thêm đúng một hành vi: `Caching` (path lặp lại không gọi inner lần hai, lộ `InnerCalls`); `Uppercase` (biến response thành chữ hoa SAU inner, cache giữ bản gốc). `Solution.Run()` dựng `new Uppercase(new Caching(new Base()))` và gọi \"a\", \"a\", \"b\".",
            [
                ("caching serves repeat paths once", "Caching lưu response inner theo path; path lặp không được chạm vào inner."),
                ("decorator stack composes", "Thứ tự: Uppercase(Caching(Base)). Uppercase biến đổi SAU response (có thể từ cache)."),
                ("stack calls inner the right number of times", "Với Uppercase(Caching(Base)), inner gọi đúng một lần cho mỗi path khác nhau."),
            ],
        ),
        "csi-p18-builder-order": vi_challenge(
            "Builder: Chỉ nhận Order Hợp lệ",
            "Dựng **Builder** với `Build()` ép bất biến hoặc throw: `WithCustomer` — bắt buộc, không rỗng; `WithItem(sku, qty, price)` — lặp được, qty ≥ 1 (throw `ArgumentException` ngay trong `WithItem`); `WithRush()` — gắn cờ giao nhanh; `Build()` throw khi: thiếu customer, không item, hoặc order rush có tổng > 10 item. Lộ các trường test đọc: `Customer`, `TotalQty`, `Items` (số dòng), `Rush`.",
            [
                ("happy path builds", "Tích lũy thẳng: cộng qty, đếm dòng, mặc định Rush = false."),
                ("invariants throw in Build", "Hai điểm ép: WithItem kiểm qty ngay; Build kiểm tính đầy đủ."),
                ("rush rule boundary", "Rush với TỔNG item > 10 throw trong Build; đúng 10 thì ổn."),
            ],
        ),
        "csi-p18-observer-review": vi_challenge(
            "Debug: Chiếc Bus không bao giờ Buông",
            "EventBus này rỉ: subscriber đã \"bỏ\" vẫn chạy, và số đếm trôi. Viết `EventBus` đúng: `Subscribe` nhận handler để sau đó unsubcribe; `Unsubscribe` gỡ thật sự; `PingAll` gọi các subscriber hiện tại theo thứ tự đăng ký; `FiredCount` đếm tổng số lần handler được gọi.",
            [
                ("subscribe fires, in order", "Hai subscriber: đăng ký trước, chạy trước."),
                ("unsubscribe detaches", "Sau Unsubscribe(h), h không được chạy — chính là chỗ rỉ của bản hỏng."),
                ("invocation counting is exact", "FiredCount đếm mỗi lần handler chạy: 2 (một mình h1) + 1 (cả hai) + 1 (h2 sau khi h1 rời) + 1 = 5."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p18-strategy-shipping",
            'public static class Solution\n{\n    public sealed class Parcel\n    {\n        public decimal WeightKg;\n    }\n\n    public interface IShippingCost\n    {\n        decimal Cost(Parcel p);\n    }\n\n    public sealed class Flat : IShippingCost\n    {\n        public decimal Cost(Parcel p) => 3.5m;\n    }\n\n    public sealed class Weight : IShippingCost\n    {\n        public decimal Cost(Parcel p)\n        {\n            decimal c = p.WeightKg * 0.8m;\n            return c < 4m ? 4m : c;\n        }\n    }\n\n    public static decimal Cost(Parcel p, IShippingCost strategy) => strategy.Cost(p);\n}\n',
            'public static class Solution\n{\n    public sealed class Parcel\n    {\n        public decimal WeightKg;\n    }\n\n    public interface IShippingCost\n    {\n        decimal Cost(Parcel p);\n    }\n\n    public sealed class Flat : IShippingCost\n    {\n        public decimal Cost(Parcel p) => 3.5m;\n    }\n\n    public sealed class Weight : IShippingCost\n    {\n        public decimal Cost(Parcel p)\n        {\n            decimal c = p.WeightKg * 0.8m;\n            return c < 4m ? 4m : c;\n        }\n    }\n\n    public static decimal Cost(Parcel p, IShippingCost strategy)\n    {\n        // near-miss: the switch survived — strategy chosen by weight instead\n        // of by the caller, so callers cannot compose\n        if (p.WeightKg >= 5m) return strategy.Cost(p);\n        return 3.5m;\n    }\n}\n',
        ),
        (
            "csi-p18-decorator-logger",
            'public static class Solution\n{\n    public interface IApiClient\n    {\n        string Send(string path);\n    }\n\n    public sealed class Base : IApiClient\n    {\n        public string Send(string path) => "200:" + path;\n    }\n\n    public sealed class Caching : IApiClient\n    {\n        private readonly IApiClient _inner;\n        private readonly System.Collections.Generic.Dictionary<string, string> _cache = new();\n        public int InnerCalls;\n\n        public Caching(IApiClient inner) => _inner = inner;\n\n        public string Send(string path)\n        {\n            if (_cache.TryGetValue(path, out var hit)) return hit;\n            InnerCalls++;\n            string resp = _inner.Send(path);\n            _cache[path] = resp;\n            return resp;\n        }\n    }\n\n    public sealed class Uppercase : IApiClient\n    {\n        private readonly IApiClient _inner;\n        public Uppercase(IApiClient inner) => _inner = inner;\n\n        public string Send(string path) => _inner.Send(path).ToUpperInvariant();\n    }\n\n    public static string[] Run()\n    {\n        IApiClient client = new Uppercase(new Caching(new Base()));\n        return new[] { client.Send("a"), client.Send("a"), client.Send("b") };\n    }\n}\n',
            'public static class Solution\n{\n    public interface IApiClient\n    {\n        string Send(string path);\n    }\n\n    public sealed class Base : IApiClient\n    {\n        public string Send(string path) => "200:" + path;\n    }\n\n    public sealed class Caching : IApiClient\n    {\n        private readonly IApiClient _inner;\n        // near-miss: the decorator wraps and counts, but never STORES —\n        // every call falls through to inner\n        public int InnerCalls;\n\n        public Caching(IApiClient inner) => _inner = inner;\n\n        public string Send(string path)\n        {\n            InnerCalls++;\n            return _inner.Send(path);\n        }\n    }\n\n    public sealed class Uppercase : IApiClient\n    {\n        private readonly IApiClient _inner;\n        public Uppercase(IApiClient inner) => _inner = inner;\n\n        public string Send(string path) => _inner.Send(path).ToUpperInvariant();\n    }\n\n    public static string[] Run()\n    {\n        IApiClient client = new Uppercase(new Caching(new Base()));\n        return new[] { client.Send("a"), client.Send("a"), client.Send("b") };\n    }\n}\n',
        ),
        (
            "csi-p18-builder-order",
            'public static class Solution\n{\n    public sealed class OrderReq\n    {\n        public string Customer = "";\n        public int TotalQty;\n        public int Items;\n        public bool Rush;\n    }\n\n    public sealed class OrderBuilder\n    {\n        private string _customer = "";\n        private int _totalQty;\n        private int _lines;\n        private bool _rush;\n\n        public OrderBuilder WithCustomer(string c)\n        {\n            _customer = c;\n            return this;\n        }\n\n        public OrderBuilder WithItem(string sku, int qty, decimal price)\n        {\n            if (qty < 1) throw new ArgumentException("qty must be >= 1");\n            _totalQty += qty;\n            _lines++;\n            return this;\n        }\n\n        public OrderBuilder WithRush()\n        {\n            _rush = true;\n            return this;\n        }\n\n        public OrderReq Build()\n        {\n            if (string.IsNullOrEmpty(_customer)) throw new InvalidOperationException("customer required");\n            if (_lines == 0) throw new InvalidOperationException("at least one item required");\n            if (_rush && _totalQty > 10) throw new InvalidOperationException("rush limited to 10 items");\n            return new OrderReq { Customer = _customer, TotalQty = _totalQty, Items = _lines, Rush = _rush };\n        }\n    }\n\n    public static bool Threw(Action a)\n    {\n        try { a(); return false; }\n        catch { return true; }\n    }\n\n    public static bool RushThrew(int items)\n    {\n        try\n        {\n            var b = new OrderBuilder().WithCustomer("ann").WithRush();\n            for (int i = 0; i < items; i++) b.WithItem("s" + i, 1, 1m);\n            b.Build();\n            return false;\n        }\n        catch { return true; }\n    }\n}\n',
            'public static class Solution\n{\n    public sealed class OrderReq\n    {\n        public string Customer = "";\n        public int TotalQty;\n        public int Items;\n        public bool Rush;\n    }\n\n    public sealed class OrderBuilder\n    {\n        private string _customer = "";\n        private int _totalQty;\n        private int _lines;\n        private bool _rush;\n\n        public OrderBuilder WithCustomer(string c)\n        {\n            _customer = c;\n            return this;\n        }\n\n        public OrderBuilder WithItem(string sku, int qty, decimal price)\n        {\n            if (qty < 1) throw new ArgumentException("qty must be >= 1");\n            _totalQty += qty;\n            _lines++;\n            return this;\n        }\n\n        public OrderBuilder WithRush()\n        {\n            _rush = true;\n            return this;\n        }\n\n        public OrderReq Build()\n        {\n            if (string.IsNullOrEmpty(_customer)) throw new InvalidOperationException("customer required");\n            if (_lines == 0) throw new InvalidOperationException("at least one item required");\n            // near-miss: >= instead of > — 10-item rush orders now rejected\n            if (_rush && _totalQty >= 10) throw new InvalidOperationException("rush limited to 10 items");\n            return new OrderReq { Customer = _customer, TotalQty = _totalQty, Items = _lines, Rush = _rush };\n        }\n    }\n\n    public static bool Threw(Action a)\n    {\n        try { a(); return false; }\n        catch { return true; }\n    }\n\n    public static bool RushThrew(int items)\n    {\n        try\n        {\n            var b = new OrderBuilder().WithCustomer("ann").WithRush();\n            for (int i = 0; i < items; i++) b.WithItem("s" + i, 1, 1m);\n            b.Build();\n            return false;\n        }\n        catch { return true; }\n    }\n}\n',
        ),
        (
            "csi-p18-observer-review",
            'public static class Solution\n{\n    public sealed class EventBus\n    {\n        private readonly System.Collections.Generic.List<EventHandler<string>> _handlers = new();\n        public int FiredCount;\n\n        public void Subscribe(EventHandler<string> h) => _handlers.Add(h);\n\n        public void Unsubscribe(EventHandler<string> h) => _handlers.Remove(h);\n\n        public void PingAll(string msg)\n        {\n            foreach (var h in _handlers.ToArray())   // snapshot: safe against mutation during fire\n            {\n                h(this, msg);\n                FiredCount++;\n            }\n        }\n    }\n}\n',
            'public static class Solution\n{\n    public sealed class EventBus\n    {\n        private readonly System.Collections.Generic.List<EventHandler<string>> _handlers = new();\n        public int FiredCount;\n\n        public void Subscribe(EventHandler<string> h) => _handlers.Add(h);\n\n        // near-miss: "unsubscribes" by clearing EVERYONE — the poisoned fix:\n        // the specific leak is gone, but innocent handlers vanish too\n        public void Unsubscribe(EventHandler<string> h) => _handlers.Clear();\n\n        public void PingAll(string msg)\n        {\n            foreach (var h in _handlers.ToArray())\n            {\n                h(this, msg);\n                FiredCount++;\n            }\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m18",
    "Checkpoint — Composite Pipeline",
    "Compose three patterns into one pipeline: interchangeable validation Strategies, a tolerant pipeline, and a Repository wrapped in an audit Decorator — with the seams the tests probe.",
    28,
    r"""
## The gate (mini-build)

One file, three seams, composing patterns you built this module:

1. **Strategy** — `IRule { string? Check(Solution.Order o); }` returning an
   error message or null. Implement `MinQty` (fails when total qty < 2, msg
   `"qty"`) and `PaidSku` (fails when any sku is empty, msg `"sku"`).
2. **Composite/Strategy pipeline** — `Solution.Validate(order, IRule[] rules)`
   returns the first non-null error, or null when all pass. Null rules in the
   array are skipped (tolerant pipeline).
3. **Repository + audit Decorator** — `IRepo { void Save(Solution.Order o); int Saved; }`;
   `AuditedRepo` wraps any `IRepo`, counts accepted saves in `Saves`, and the
   test flow decides what gets saved.

Flow under test: validate first; save only when valid; `AuditedRepo.Saves`
must equal the number of *valid* orders.

```csharp
public static class Solution
{
    public sealed class Order { public string Sku = ""; public int Qty; }
    public interface IRule { string? Check(Order o); }
    public static string? Validate(Order o, IRule[] rules);
    public interface IRepo { void Save(Order o); int Saved { get; } }
    public sealed class AuditedRepo : IRepo { public int Saves; /* wraps IRepo */ }
}
```""",
    "Checkpoint — Đường ống Ghép Pattern",
    "Ghép ba pattern thành một đường ống: các Strategy validation, đường ống khoan dung, và Repository bọc Decorator audit — với đúng các đường ranh mà test thăm dò.",
    r"""
## Cổng kiểm tra (mini-build)

Một file, ba đường ranh, ghép các pattern bạn đã xây trong module:

1. **Strategy** — `IRule { string? Check(Solution.Order o); }` trả thông báo
   lỗi hoặc null. Hiện thực `MinQty` (fail khi tổng qty < 2, msg `"qty"`) và
   `PaidSku` (fail khi có sku rỗng, msg `"sku"`).
2. **Đường ống Strategy** — `Solution.Validate(order, IRule[] rules)` trả lỗi
   không-null đầu tiên, hoặc null khi tất cả đạt. Rule null trong mảng được bỏ
   qua (đường ống khoan dung).
3. **Repository + Decorator audit** — `IRepo { void Save(Solution.Order o); int Saved { get; } }`;
   `AuditedRepo` bọc bất kỳ `IRepo` nào, đếm số lần lưu được chấp nhận trong
   `Saves`.

Luồng dưới test: validate trước; chỉ lưu khi hợp lệ; `AuditedRepo.Saves` phải
bằng số order *hợp lệ*.
""",
    challenge(
        "csi-checkpoint-m18-task",
        "Compose the Validation Pipeline",
        "Implement IRule (MinQty, PaidSku), Validate (first error wins, null rules skipped), IRepo + AuditedRepo; save only valid orders.",
        CS_PRELUDE,
        [
            (
                "rules report the right errors",
                r"""
var o = new Solution.Order(); o.Sku = "s1"; o.Qty = 1;
Cj.Eq(new Solution.MinQty().Check(o), "qty", "qty rule fires");
var empty = new Solution.Order(); empty.Sku = ""; empty.Qty = 3;
Cj.Eq(new Solution.PaidSku().Check(empty), "sku", "sku rule fires");
Cj.Eq(new Solution.MinQty().Check(new Solution.Order { Sku = "s", Qty = 5 }), null, "valid passes");
""",
                    "Each rule knows exactly one thing; null means pass.",
                ),
                (
                    "first error wins, nulls skipped",
                    r"""
var o = new Solution.Order(); o.Sku = ""; o.Qty = 1;
Solution.IRule[] rules = { null, new Solution.MinQty(), null, new Solution.PaidSku() };
Cj.Eq(Solution.Validate(o, rules), "qty", "first non-null rule that fails wins");
Cj.Eq(Solution.Validate(new Solution.Order { Sku = "s", Qty = 2 }, rules), null, "clean pass");
""",
                    "Tolerant pipeline: null rules skipped; the first real error is returned; all-pass returns null.",
                ),
                (
                    "audit counts only valid saves",
                    r"""
var repo = new Solution.AuditedRepo(new Solution.MemRepo());
var good = new Solution.Order { Sku = "s", Qty = 3 };
var bad = new Solution.Order { Sku = "", Qty = 3 };
Solution.IRule[] rules = { new Solution.PaidSku() };
foreach (var ord in new[] { good, bad, good })
    if (Solution.Validate(ord, rules) is null) repo.Save(ord);
Cj.Eq(repo.Saves, 2, "two valid orders saved");
Cj.Eq(repo.Saved, 2, "inner repo agrees");
""",
                    "The decorator counts exactly what the inner repo stored — validation gates the save.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Ghép Đường ống Validation",
            "Hiện thực IRule (MinQty, PaidSku), Validate (lỗi đầu tiên thắng, rule null bị bỏ qua), IRepo + AuditedRepo; chỉ lưu order hợp lệ.",
            [
                ("rules report the right errors", "Mỗi rule biết đúng một điều; null nghĩa là đạt."),
                ("first error wins, nulls skipped", "Đường ống khoan dung: bỏ qua rule null; trả lỗi thực đầu tiên; tất cả đạt trả null."),
                ("audit counts only valid saves", "Decorator đếm đúng những gì inner repo đã lưu — validation chặn trước khi lưu."),
            ],
        ),
        solution='public static class Solution\n{\n    public sealed class Order\n    {\n        public string Sku = "";\n        public int Qty;\n    }\n\n    public interface IRule\n    {\n        string? Check(Order o);\n    }\n\n    public sealed class MinQty : IRule\n    {\n        public string? Check(Order o) => o.Qty < 2 ? "qty" : null;\n    }\n\n    public sealed class PaidSku : IRule\n    {\n        public string? Check(Order o) => string.IsNullOrEmpty(o.Sku) ? "sku" : null;\n    }\n\n    public static string? Validate(Order o, IRule[] rules)\n    {\n        foreach (var r in rules)\n        {\n            if (r is null) continue;\n            var err = r.Check(o);\n            if (err is not null) return err;\n        }\n        return null;\n    }\n\n    public interface IRepo\n    {\n        void Save(Order o);\n        int Saved { get; }\n    }\n\n    public sealed class MemRepo : IRepo\n    {\n        public int Saved { get; private set; }\n        public void Save(Order o) => Saved++;\n    }\n\n    public sealed class AuditedRepo : IRepo\n    {\n        private readonly IRepo _inner;\n        public int Saves;\n\n        public AuditedRepo(IRepo inner) => _inner = inner;\n\n        public void Save(Order o)\n        {\n            _inner.Save(o);\n            Saves++;\n        }\n\n        public int Saved => _inner.Saved;\n    }\n}\n',
        wrong='public static class Solution\n{\n    public sealed class Order\n    {\n        public string Sku = "";\n        public int Qty;\n    }\n\n    public interface IRule\n    {\n        string? Check(Order o);\n    }\n\n    public sealed class MinQty : IRule\n    {\n        // near-miss: inverted comparison — passes short orders, fails big ones\n        public string? Check(Order o) => o.Qty >= 2 ? "qty" : null;\n    }\n\n    public sealed class PaidSku : IRule\n    {\n        public string? Check(Order o) => string.IsNullOrEmpty(o.Sku) ? "sku" : null;\n    }\n\n    public static string? Validate(Order o, IRule[] rules)\n    {\n        foreach (var r in rules)\n        {\n            if (r is null) continue;\n            var err = r.Check(o);\n            if (err is not null) return err;\n        }\n        return null;\n    }\n\n    public interface IRepo\n    {\n        void Save(Order o);\n        int Saved { get; }\n    }\n\n    public sealed class MemRepo : IRepo\n    {\n        public int Saved { get; private set; }\n        public void Save(Order o) => Saved++;\n    }\n\n    public sealed class AuditedRepo : IRepo\n    {\n        private readonly IRepo _inner;\n        public int Saves;\n\n        public AuditedRepo(IRepo inner) => _inner = inner;\n\n        public void Save(Order o)\n        {\n            _inner.Save(o);\n            Saves++;\n        }\n\n        public int Saved => _inner.Saved;\n    }\n}\n',
    ),
print("module 18 authored")
