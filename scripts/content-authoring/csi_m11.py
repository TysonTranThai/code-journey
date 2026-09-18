#!/usr/bin/env python3
"""C# — Intermediate — Module 11: csi-di.

Dependency inversion and hand-rolled DI (no NuGet in the sandbox): service
abstractions, constructor injection, a tiny reflection-free container with
singleton/transient lifetimes, composition root, and the testability payoff.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE, CJ_TINY_CONTAINER,
)

M = "csi-di"

write_module(
    M,
    "Dependency Injection",
    "Invert dependencies behind interfaces, inject them through constructors, and wire lifetimes in one composition root.",
    "Dependency Injection",
    "Đảo ngược dependency sau interface, inject qua constructor, và nối các lifetime tại một composition root.",
    ["dependency-inversion", "building-a-container", "csi-checkpoint-m11"],
    ["csi-p11-di"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "dependency-inversion",
    "Dependency Inversion and Constructor Injection",
    "Depend on abstractions, receive them from outside, and watch unit tests get easy.",
    17,
    r"""
## The dependency problem

A `OrderService` that news up its own `SqlEmailer` is welded to it: can't
test without a database, can't swap providers, can't see what it needs.
Dependency INVERSION flips the arrow: high-level policy (OrderService)
defines the abstraction it needs; low-level detail (SqlEmailer) implements it:

```csharp
public interface IEmailer { void Send(string to, string body); }

public sealed class OrderService
{
    private readonly IEmailer _emailer;
    public OrderService(IEmailer emailer) => _emailer = emailer;   // injected

    public void Place(Order o)
    {
        // ... business rules ...
        _emailer.Send(o.Email, "order confirmed");
    }
}
```

CONSTRUCTOR INJECTION: dependencies arrive as constructor parameters,
stored in readonly fields. The class can't be constructed half-wired.

## The testability payoff

A fake replaces the real thing in tests — no network, no database:

```csharp
public sealed class FakeEmailer : IEmailer
{
    public System.Collections.Generic.List<(string To, string Body)> Sent = new();
    public void Send(string to, string body) => Sent.Add((to, body));
}

var fake = new FakeEmailer();
var svc = new OrderService(fake);
svc.Place(order);
// assert fake.Sent has the notification
```

This is why injected classes need no mocking frameworks for unit tests.

## What NOT to inject

Value objects, DTOs, and truly static utilities stay as-is. Inject
behaviors with state or I/O: gateways, repositories, clocks, config
providers. Two constructor parameters + a news-up inside is fine; five is
a design smell the class is doing too much.

## Check your understanding

- Who owns the interface — the consumer or the implementation? (The consumer; detail implements it.)
- Why readonly fields for injected dependencies? (Fixed at construction — no half-wired instances.)
""",
    "Dependency Inversion và Constructor Injection",
    "Phụ thuộc vào abstraction, nhận nó từ bên ngoài, và thấy unit test dễ ra sao.",
    r"""
## Vấn đề dependency

`OrderService` tự `new` `SqlEmailer` của chính nó thì bị hàn chặt vào nó:
không test được mà không có database, không thay provider được, không nhìn
thấy nó cần gì. Dependency INVERSION đảo chiều mũi tên: tầng chính sách cao
(OrderService) định nghĩa abstraction nó cần; tầng chi tiết thấp
(SqlEmailer) hiện thực nó:

```csharp
public interface IEmailer { void Send(string to, string body); }

public sealed class OrderService
{
    private readonly IEmailer _emailer;
    public OrderService(IEmailer emailer) => _emailer = emailer;   // injected

    public void Place(Order o)
    {
        // ... business rules ...
        _emailer.Send(o.Email, "order confirmed");
    }
}
```

CONSTRUCTOR INJECTION: dependency đến như tham số constructor, lưu vào
field readonly. Lớp không thể được dựng trong trạng thái dở dang.

## Lợi ích testability

Một fake thay thế bản thật trong test — không network, không database:

```csharp
public sealed class FakeEmailer : IEmailer
{
    public System.Collections.Generic.List<(string To, string Body)> Sent = new();
    public void Send(string to, string body) => Sent.Add((to, body));
}

var fake = new FakeEmailer();
var svc = new OrderService(fake);
svc.Place(order);
// assert fake.Sent có notification
```

Vì vậy lớp được inject không cần mocking framework cho unit test.

## Cái gì KHÔNG nên inject

Value object, DTO, và tiện ích tĩnh thuần túy giữ nguyên. Inject các hành
vi có state hoặc I/O: gateway, repository, clock, provider cấu hình. Hai
tham số constructor + một news-up bên trong vẫn ổn; năm tham số là mùi
thiết kế — lớp đang làm quá nhiều việc.

## Kiểm tra hiểu biết

- Ai sở hữu interface — consumer hay hiện thực? (Consumer; chi tiết hiện thực.)
- Vì sao field injected phải readonly? (Chốt lúc dựng — không có instance dở dang.)
""",
    r"""
## Vấn đề dependency

`OrderService` tự `new` `SqlEmailer` của chính nó thì bị hàn chặt vào nó:
không test được mà không có database, không thay provider được, không nhìn
thấy nó cần gì. Dependency INVERSION đảo chiều mũi tên: tầng chính sách cao
(OrderService) định nghĩa abstraction nó cần; tầng chi tiết thấp
(SqlEmailer) hiện thực nó:

```csharp
public interface IEmailer { void Send(string to, string body); }

public sealed class OrderService
{
    private readonly IEmailer _emailer;
    public OrderService(IEmailer emailer) => _emailer = emailer;   // injected

    public void Place(Order o)
    {
        // ... business rules ...
        _emailer.Send(o.Email, "order confirmed");
    }
}
```

CONSTRUCTOR INJECTION: dependency đến như tham số constructor, lưu vào
field readonly. Lớp không thể được dựng trong trạng thái dở dang.

## Lợi ích testability

Một fake thay thế bản thật trong test — không network, không database:

```csharp
public sealed class FakeEmailer : IEmailer
{
    public System.Collections.Generic.List<(string To, string Body)> Sent = new();
    public void Send(string to, string body) => Sent.Add((to, body));
}

var fake = new FakeEmailer();
var svc = new OrderService(fake);
svc.Place(order);
// assert fake.Sent có notification
```

Vì vậy lớp được inject không cần mocking framework cho unit test.

## Cái gì KHÔNG nên inject

Value object, DTO, và tiện ích tĩnh thuần túy giữ nguyên. Inject các hành
vi có state hoặc I/O: gateway, repository, clock, provider cấu hình. Hai
tham số constructor + một news-up bên trong vẫn ổn; năm tham số là mùi
thiết kế — lớp đang làm quá nhiều việc.

## Kiểm tra hiểu biết

- Ai sở hữu interface — consumer hay hiện thực? (Consumer; chi tiết hiện thực.)
- Vì sao field injected phải readonly? (Chốt lúc dựng — không có instance dở dang.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "building-a-container",
    "A Tiny Container: Lifetimes and the Composition Root",
    "Registration, resolution, singleton vs transient, and why the app wires itself in exactly one place.",
    18,
    r"""
## Service lifetimes

- SINGLETON — one instance for the whole process (stateless services,
  caches). Thread-safety is now the implementation's problem.
- TRANSIENT — a new instance per resolution (stateful per-operation
  services, fakes). Cheap to create.
- (Scoped — one instance per logical unit of work — matters with a web
  framework and a request pipeline; revisit it in Advanced/API work.)

## The hand-rolled container

With no NuGet, the pattern behind every DI container is small enough to
build — a registry of factory functions:

```csharp
public sealed class Container
{
    private readonly System.Collections.Generic.Dictionary<Type, Func<object>> _factories = new();
    private readonly System.Collections.Generic.Dictionary<Type, object> _singletons = new();

    public void Register<TService>(Func<TService> factory) =>
        _factories[typeof(TService)] = () => factory();

    public void RegisterSingleton<TService>(Func<TService> factory)
    {
        object? instance = null;
        _factories[typeof(TService)] = () =>
        {
            if (instance is null) instance = factory();   // lazy, once
            return instance;
        };
    }

    public TService Resolve<TService>() => (TService)_factories[typeof(TService)]();
}
```

Real containers add constructor discovery via reflection and lifetime
scopes — but registration/resolution/lifetimes are the concepts.

## The composition root

Wiring lives in ONE place, at the application's entry point:

```csharp
var container = new Container();
container.RegisterSingleton<IEmailer>(() => new SmtpEmailer(config));
container.RegisterTransient<IOrderService>(() => new OrderService(
    container.Resolve<IEmailer>(), container.Resolve<IClock>()));
var svc = container.Resolve<IOrderService>();   // app runs from here down
```

Business classes never touch the container; they receive what they need.
When the provider changes, exactly one file changes.

## Check your understanding

- Transient or singleton for a stateful per-request service? (Transient.)
- Where does `new SmtpEmailer()` belong? (The composition root — nowhere else.)
""",
    "Container Tí Hon: Lifetime và Composition Root",
    "Đăng ký, resolve, singleton vs transient, và vì sao ứng dụng tự nối tại đúng một nơi.",
    r"""
## Service lifetime

- SINGLETON — một instance cho cả tiến trình (service không state, cache).
  Thread-safety giờ là việc của hiện thực.
- TRANSIENT — instance mới cho mỗi lần resolve (service có state theo từng
  thao tác, fake). Tạo ra rẻ.
- (Scoped — một instance cho mỗi đơn vị công việc — quan trọng khi có web
  framework và request pipeline; sẽ quay lại ở phần Nâng cao/API.)

## Container tự viết

Không có NuGet, pattern đứng sau mọi DI container nhỏ đến mức tự dựng được
— một sổ đăng ký các hàm factory:

```csharp
public sealed class Container
{
    private readonly System.Collections.Generic.Dictionary<Type, Func<object>> _factories = new();
    private readonly System.Collections.Generic.Dictionary<Type, object> _singletons = new();

    public void Register<TService>(Func<TService> factory) =>
        _factories[typeof(TService)] = () => factory();

    public void RegisterSingleton<TService>(Func<TService> factory)
    {
        object? instance = null;
        _factories[typeof(TService)] = () =>
        {
            if (instance is null) instance = factory();   // lazy, đúng một lần
            return instance;
        };
    }

    public TService Resolve<TService>() => (TService)_factories[typeof(TService)]();
}
```

Container thật thêm discovery constructor bằng reflection và lifetime scope
— nhưng đăng ký/resolve/lifetime là các khái niệm cốt lõi.

## Composition root

Việc nối dây nằm ở MỘT nơi, tại điểm vào ứng dụng:

```csharp
var container = new Container();
container.RegisterSingleton<IEmailer>(() => new SmtpEmailer(config));
container.RegisterTransient<IOrderService>(() => new OrderService(
    container.Resolve<IEmailer>(), container.Resolve<IClock>()));
var svc = container.Resolve<IOrderService>();   // app chạy từ đây xuống
```

Lớp nghiệp vụ không đụng container; chúng nhận những gì cần. Đổi provider
thì chỉ đúng một file thay đổi.

## Kiểm tra hiểu biết

- Transient hay singleton cho service có state theo từng request? (Transient.)
- `new SmtpEmailer()` thuộc về đâu? (Composition root — không nơi nào khác.)
""",
    r"""
## Service lifetime

- SINGLETON — một instance cho cả tiến trình (service không state, cache).
  Thread-safety giờ là việc của hiện thực.
- TRANSIENT — instance mới cho mỗi lần resolve (service có state theo từng
  thao tác, fake). Tạo ra rẻ.
- (Scoped — một instance cho mỗi đơn vị công việc — quan trọng khi có web
  framework và request pipeline; sẽ quay lại ở phần Nâng cao/API.)

## Container tự viết

Không có NuGet, pattern đứng sau mọi DI container nhỏ đến mức tự dựng được
— một sổ đăng ký các hàm factory:

```csharp
public sealed class Container
{
    private readonly System.Collections.Generic.Dictionary<Type, Func<object>> _factories = new();
    private readonly System.Collections.Generic.Dictionary<Type, object> _singletons = new();

    public void Register<TService>(Func<TService> factory) =>
        _factories[typeof(TService)] = () => factory();

    public void RegisterSingleton<TService>(Func<TService> factory)
    {
        object? instance = null;
        _factories[typeof(TService)] = () =>
        {
            if (instance is null) instance = factory();   // lazy, đúng một lần
            return instance;
        };
    }

    public TService Resolve<TService>() => (TService)_factories[typeof(TService)]();
}
```

Container thật thêm discovery constructor bằng reflection và lifetime scope
— nhưng đăng ký/resolve/lifetime là các khái niệm cốt lõi.

## Composition root

Việc nối dây nằm ở MỘT nơi, tại điểm vào ứng dụng:

```csharp
var container = new Container();
container.RegisterSingleton<IEmailer>(() => new SmtpEmailer(config));
container.RegisterTransient<IOrderService>(() => new OrderService(
    container.Resolve<IEmailer>(), container.Resolve<IClock>()));
var svc = container.Resolve<IOrderService>();   // app chạy từ đây xuống
```

Lớp nghiệp vụ không đụng container; chúng nhận những gì cần. Đổi provider
thì chỉ đúng một file thay đổi.

## Kiểm tra hiểu biết

- Transient hay singleton cho service có state theo từng request? (Transient.)
- `new SmtpEmailer()` thuộc về đâu? (Composition root — không nơi nào khác.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p11-di",
    "DI Practice: Fakes, Lifetimes, Wiring",
    "Break a hardwired dependency with an interface, prove container lifetimes, and build the composition root.",
    "Luyện DI: Fake, Lifetime, Nối dây",
    "Tháo dependency cứng bằng interface, chứng minh lifetime của container, và dựng composition root.",
    "building-a-container",
    30,
    "intermediate",
    [
        challenge(
            "csi-p11-invert-dependency",
            "Invert a Hardwired Dependency",
            """`PriceNotifier` currently news up `SmtpEmailer` directly (provided). Introduce `IEmailer` (Send(string, string)), make PriceNotifier take IEmailer via constructor, and implement a LoggingEmailer that records "log:<to>:<body>" into its Log list.

```csharp
public interface IEmailer { void Send(string to, string body); }
public sealed class SmtpEmailer : IEmailer { public void Send(...) { /* real */ } }
public sealed class PriceNotifier
{
    public void Notify(string email, string product, decimal price);
}
```""",
            CS_PRELUDE,
            [
                (
                    "notification flows through the abstraction",
                    r"""
var emailer = new Solution.LoggingEmailer();
var notifier = new Solution.PriceNotifier(emailer);
notifier.Notify("a@x.com", "widget", 9.99m);
Cj.Eq(emailer.Log.Count, 1, "one notification");
Cj.True(emailer.Log[0].StartsWith("log:a@x.com:"), "recorded to+body");
""",
                    "Constructor injection: store the IEmailer in a readonly field; Notify calls Send.",
                ),
                (
                    "works with any implementation",
                    r"""
var emailer = new Solution.LoggingEmailer();
var notifier = new Solution.PriceNotifier(emailer);
notifier.Notify("b@x.com", "gadget", 5m);
notifier.Notify("c@x.com", "thing", 1m);
Cj.Eq(emailer.Log.Count, 2, "both notifications recorded");
""",
                    "PriceNotifier depends only on the interface — implementations are interchangeable.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p11-container",
            "Build the Tiny Container",
            """Implement the Container from the lesson: Register<TService>(Func<TService>) for transient, RegisterSingleton<TService>(Func<TService>) for lazy once-only, Resolve<TService>() throwing InvalidOperationException for unregistered types.

```csharp
public sealed class Container
{
    public void Register<TService>(Func<TService> factory);
    public void RegisterSingleton<TService>(Func<TService> factory);
    public TService Resolve<TService>();
}
```""",
            CS_PRELUDE,
            [
                (
                    "transient creates fresh",
                    r"""
var c = new Solution.Container();
c.Register(() => new System.Text.StringBuilder());
var a = c.Resolve<System.Text.StringBuilder>();
a.Append("x");
var b = c.Resolve<System.Text.StringBuilder>();
Cj.Eq(b.ToString(), "", "fresh instance per resolve");
Cj.True(!ReferenceEquals(a, b), "different instances");
""",
                    "Factories dictionary keyed by typeof(TService); Resolve invokes and casts.",
                ),
                (
                    "singleton stays one",
                    r"""
var c = new Solution.Container();
int built = 0;
c.RegisterSingleton<System.Random>(() => { built++; return new System.Random(); });
var r1 = c.Resolve<System.Random>();
var r2 = c.Resolve<System.Random>();
Cj.True(ReferenceEquals(r1, r2), "same instance");
Cj.Eq(built, 1, "factory ran exactly once");
""",
                    "Cache the created instance in the closure; return it thereafter.",
                ),
                (
                    "unregistered type throws",
                    r"""
var c = new Solution.Container();
try { c.Resolve<System.Random>(); Cj.True(false, "should throw"); }
catch (System.InvalidOperationException) { }
""",
                    "Missing key -> throw InvalidOperationException with the service type name.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p11-composition-root",
            "Wire the Composition Root",
            """Build an app object with a BuildApp(config) method that registers an IClock (singleton, provided FakeClock), an IPriceCalculator (transient, provided), and returns the fully-resolved App. The App must be able to quote a price with the current time.

```csharp
public interface IClock { DateTime Now { get; } }
public sealed class FakeClock : IClock { public FakeClock(DateTime now); public DateTime Now { get; } }
public interface IPriceCalculator { decimal Quote(decimal basePrice, DateTime at); }
public sealed class RushCalculator : IPriceCalculator { /* +10% before 9am */ }
public sealed class App { public App(IPriceCalculator calc, IClock clock); public string Quote(decimal p); }
static Solution.App BuildApp(Solution.FakeClock clock);
```""",
            CJ_TINY_CONTAINER,
            [
                (
                    "wiring resolves transitively",
                    r"""
var clock = new Solution.FakeClock(new DateTime(2026, 1, 1, 8, 0, 0));
var app = Solution.BuildApp(clock);
Cj.True(app.Quote(100m).Contains("110"), "rush pricing from wired calculator");
""",
                    "Register clock singleton + calculator transient whose factory resolves the clock; Resolve<IPriceCalculator>, pass into App.",
                ),
                (
                    "singleton clock shared",
                    r"""
var clock = new Solution.FakeClock(new DateTime(2026, 1, 1, 12, 0, 0));
var app = Solution.BuildApp(clock);
Cj.True(app.Quote(50m).Contains("50"), "noon quote has no rush surcharge");
""",
                    "The same clock instance flows to whoever resolves IClock — the singleton guarantee.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p11-invert-dependency": vi_challenge(
            "Đảo ngược dependency cứng",
            "`PriceNotifier` hiện tại tự new `SmtpEmailer` (được cung cấp). Đưa vào `IEmailer` (Send(string, string)), cho PriceNotifier nhận IEmailer qua constructor, và hiện thực LoggingEmailer ghi \"log:<to>:<body>\" vào danh sách Log.",
            [
                ("notification flows through the abstraction", "Constructor injection: lưu IEmailer vào field readonly; Notify gọi Send."),
                ("works with any implementation", "PriceNotifier chỉ phụ thuộc interface — hiện thực hoán đổi cho nhau được."),
            ],
        ),
        "csi-p11-container": vi_challenge(
            "Dựng container tí hon",
            "Hiện thực Container theo bài học: Register<TService>(Func<TService>) cho transient, RegisterSingleton<TService>(Func<TService>) cho lazy một-lần, Resolve<TService>() ném InvalidOperationException khi type chưa đăng ký.",
            [
                ("transient creates fresh", "Dictionary các factory theo typeof(TService); Resolve gọi và cast."),
                ("singleton stays one", "Cache instance đã tạo trong closure; những lần sau trả instance đó."),
                ("unregistered type throws", "Thiếu key -> ném InvalidOperationException kèm tên type service."),
            ],
        ),
        "csi-p11-composition-root": vi_challenge(
            "Nối composition root",
            "Dựng BuildApp(config) đăng ký IClock (singleton, FakeClock được cấp), IPriceCalculator (transient, được cấp), và trả App đã resolve đầy đủ. App phải báo giá kèm thời điểm hiện tại.",
            [
                ("wiring resolves transitively", "Đăng ký clock singleton + calculator transient có factory resolve clock; Resolve<IPriceCalculator>, đưa vào App."),
                ("singleton clock shared", "Cùng một instance clock chảy tới mọi nơi resolve IClock — bảo đảm singleton."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p11-invert-dependency",
            'public class Solution\n{\n    public interface IEmailer\n    {\n        void Send(string to, string body);\n    }\n\n    public sealed class SmtpEmailer : IEmailer\n    {\n        public void Send(string to, string body)\n        {\n            // real implementation would hit the network\n        }\n    }\n\n    public sealed class LoggingEmailer : IEmailer\n    {\n        public System.Collections.Generic.List<string> Log { get; } = new();\n\n        public void Send(string to, string body)\n        {\n            Log.Add("log:" + to + ":" + body);\n        }\n    }\n\n    public sealed class PriceNotifier\n    {\n        private readonly IEmailer _emailer;\n\n        public PriceNotifier(IEmailer emailer) => _emailer = emailer;\n\n        public void Notify(string email, string product, decimal price)\n        {\n            _emailer.Send(email, product + " is now $" + price);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public interface IEmailer\n    {\n        void Send(string to, string body);\n    }\n\n    public sealed class SmtpEmailer : IEmailer\n    {\n        public void Send(string to, string body) { }\n    }\n\n    public sealed class LoggingEmailer : IEmailer\n    {\n        public System.Collections.Generic.List<string> Log { get; } = new();\n\n        public void Send(string to, string body)\n        {\n            Log.Add("log:" + to + ":" + body);\n        }\n    }\n\n    public sealed class PriceNotifier\n    {\n        // near-miss: still hardwired to SmtpEmailer — the injected\n        // LoggingEmailer is never used, so no log entries appear and the\n        // substitution test fails\n        private readonly SmtpEmailer _emailer = new SmtpEmailer();\n\n        public PriceNotifier(IEmailer emailer) { _ = emailer; }\n\n        public void Notify(string email, string product, decimal price)\n        {\n            _emailer.Send(email, product + " is now $" + price);\n        }\n    }\n}\n',
        ),
        (
            "csi-p11-container",
            'public class Solution\n{\n    public sealed class Container\n    {\n        private readonly System.Collections.Generic.Dictionary<System.Type, Func<object>> _factories = new();\n\n        public void Register<TService>(Func<TService> factory)\n        {\n            _factories[typeof(TService)] = () => factory()!;\n        }\n\n        public void RegisterSingleton<TService>(Func<TService> factory)\n        {\n            object? instance = null;\n            _factories[typeof(TService)] = () =>\n            {\n                if (instance is null) instance = factory()!;\n                return instance;\n            };\n        }\n\n        public TService Resolve<TService>()\n        {\n            if (!_factories.TryGetValue(typeof(TService), out var factory))\n                throw new System.InvalidOperationException(\n                    "no registration for " + typeof(TService).Name);\n            return (TService)factory();\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class Container\n    {\n        private readonly System.Collections.Generic.Dictionary<System.Type, Func<object>> _factories = new();\n\n        public void Register<TService>(Func<TService> factory)\n        {\n            _factories[typeof(TService)] = () => factory()!;\n        }\n\n        public void RegisterSingleton<TService>(Func<TService> factory)\n        {\n            // near-miss: the singleton closure forgets its instance — every\n            // resolve calls the factory again, so built == 2 and the identity\n            // test fails\n            _factories[typeof(TService)] = () => factory()!;\n        }\n\n        public TService Resolve<TService>()\n        {\n            if (!_factories.TryGetValue(typeof(TService), out var factory))\n                throw new System.InvalidOperationException("no registration");\n            return (TService)factory();\n        }\n    }\n}\n',
        ),
        (
            "csi-p11-composition-root",
            'public class Solution\n{\n    public interface IClock { System.DateTime Now { get; } }\n\n    public sealed class FakeClock : IClock\n    {\n        private readonly System.DateTime _now;\n        public FakeClock(System.DateTime now) => _now = now;\n        public System.DateTime Now => _now;\n    }\n\n    public interface IPriceCalculator\n    {\n        decimal Quote(decimal basePrice, System.DateTime at);\n    }\n\n    public sealed class RushCalculator : IPriceCalculator\n    {\n        public decimal Quote(decimal basePrice, System.DateTime at)\n        {\n            return at.Hour < 9 ? basePrice * 1.10m : basePrice;\n        }\n    }\n\n    public sealed class App\n    {\n        private readonly IPriceCalculator _calc;\n        private readonly IClock _clock;\n\n        public App(IPriceCalculator calc, IClock clock)\n        {\n            _calc = calc;\n            _clock = clock;\n        }\n\n        public string Quote(decimal p)\n        {\n            return "total=" + _calc.Quote(p, _clock.Now);\n        }\n    }\n\n    public static App BuildApp(FakeClock clock)\n    {\n        var container = new TinyContainer();\n        container.RegisterSingleton<IClock>(() => clock);\n        container.RegisterTransient<IPriceCalculator>(() => new RushCalculator());\n        return new App(container.Resolve<IPriceCalculator>(), container.Resolve<IClock>());\n    }\n}\n',
            'public class Solution\n{\n    public interface IClock { System.DateTime Now { get; } }\n\n    public sealed class FakeClock : IClock\n    {\n        private readonly System.DateTime _now;\n        public FakeClock(System.DateTime now) => _now = now;\n        public System.DateTime Now => _now;\n    }\n\n    public interface IPriceCalculator\n    {\n        decimal Quote(decimal basePrice, System.DateTime at);\n    }\n\n    public sealed class RushCalculator : IPriceCalculator\n    {\n        public decimal Quote(decimal basePrice, System.DateTime at)\n        {\n            return at.Hour < 9 ? basePrice * 1.10m : basePrice;\n        }\n    }\n\n    public sealed class App\n    {\n        private readonly IPriceCalculator _calc;\n        private readonly IClock _clock;\n\n        public App(IPriceCalculator calc, IClock clock)\n        {\n            _calc = calc;\n            _clock = clock;\n        }\n\n        public string Quote(decimal p)\n        {\n            return "total=" + _calc.Quote(p, _clock.Now);\n        }\n    }\n\n    public static App BuildApp(FakeClock clock)\n    {\n        // near-miss: bypasses the container and news the calculator with a\n        // NEW clock created from default(DateTime) — midnight counts as rush\n        // hour, so the noon test sees 10% surcharge and fails\n        return new App(new RushCalculator(), new FakeClock(default));\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m11",
    "Checkpoint — Modular Order Processing System",
    "The DI mini-build: order service with notification and audit, fakes in tests, singletons in the root.",
    25,
    r"""
## The gate (mini-build)

Assemble the pieces into one composable order pipeline:

1. `IOrderValidator.IsValid(decimal amount)` — business rule (amount > 0).
2. `IOrderRepository.Save(Order order)` — persistence boundary.
3. `IAuditLog.Record(string message)` — audit trail.
4. `OrderProcessor(IOrderValidator, IOrderRepository, IAuditLog)` —
   constructor-injected; `Process(decimal amount)` returns
   `"ok:<id>"` when valid (repository saves, audit records), else
   `"rejected"`.
5. `BuildProcessor(IOrderRepository repo, IAuditLog audit)` — the
   composition root: registers a singleton validator and transient
   processor using the provided `TinyContainer`, resolves and returns the
   processor.

Order: `record Order(int Id, decimal Amount)`. Repository generates ids
starting at 1.
""",
    "Checkpoint — Hệ thống Xử lý Đơn hàng Modular",
    "Mini-build DI: order service với notification và audit, fake trong test, singleton trong root.",
    r"""
## Cổng kiểm tra (mini-build)

Lắp các mảnh thành một pipeline đơn hàng có thể ghép:

1. `IOrderValidator.IsValid(decimal amount)` — nghiệp vụ (amount > 0).
2. `IOrderRepository.Save(Order order)` — ranh giới lưu trữ.
3. `IAuditLog.Record(string message)` — nhật ký audit.
4. `OrderProcessor(IOrderValidator, IOrderRepository, IAuditLog)` —
   inject qua constructor; `Process(decimal amount)` trả `"ok:<id>"`
   khi hợp lệ (repository lưu, audit ghi), nếu không `"rejected"`.
5. `BuildProcessor(IOrderRepository repo, IAuditLog audit)` — composition
   root: đăng ký validator singleton và processor transient qua
   `TinyContainer` được cấp, resolve và trả processor.

Order: `record Order(int Id, decimal Amount)`. Repository sinh id bắt đầu
từ 1.
""",
    challenge(
        "csi-checkpoint-m11-task",
        "Checkpoint: Order Pipeline Wired",
        """Implement the pipeline described in the checkpoint (TinyContainer is provided — same API as the lesson's Container):

```csharp
static string Process(decimal amount);                       // runs the resolved processor
static Solution.OrderProcessor BuildProcessor(IOrderRepository repo, IAuditLog audit);
```""",
        CJ_TINY_CONTAINER,
        [
            (
                "valid order flows through",
                r"""
var audit = new Solution.MemoryAudit();
var repo = new Solution.MemoryRepo();
var processor = Solution.BuildProcessor(repo, audit);
string result = processor.Process(42m);
Cj.True(result.StartsWith("ok:1"), "first saved order id");
Cj.Eq(repo.Saved.Count, 1, "repository got the order");
Cj.Eq(audit.Entries.Count, 1, "audit recorded once");
""",
                    "Process delegates to the processor: validate -> save -> audit -> format \"ok:<id>\".",
                ),
                (
                    "invalid order short-circuits",
                    r"""
var audit = new Solution.MemoryAudit();
var repo = new Solution.MemoryRepo();
var processor = Solution.BuildProcessor(repo, audit);
Cj.Eq(processor.Process(-5m), "rejected", "amount <= 0 rejected");
Cj.Eq(repo.Saved.Count, 0, "nothing saved");
Cj.Eq(audit.Entries.Count, 0, "nothing audited");
""",
                    "Validator runs first; rejection skips save and audit.",
                ),
                (
                    "composition root returns a working graph",
                    r"""
var audit = new Solution.MemoryAudit();
var repo = new Solution.MemoryRepo();
var p1 = Solution.BuildProcessor(repo, audit);
var p2 = Solution.BuildProcessor(repo, audit);
p1.Process(10m);
string r = p2.Process(20m);
Cj.True(r.StartsWith("ok:2"), "shared repo state across builds (ids continue)");
""",
                    "Each BuildProcessor call wires fresh services around the SAME repo/audit instances passed in.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Pipeline đơn hàng đã nối",
            "Hiện thực pipeline (TinyContainer được cấp — cùng API như Container trong bài học): Process trả \"ok:<id>\" khi hợp lệ (lưu + audit) hoặc \"rejected\"; BuildProcessor là composition root — validator singleton, processor transient.",
            [
                ("valid order flows through", "Process ủy quyền cho processor: validate -> save -> audit -> \"ok:<id>\"."),
                ("invalid order short-circuits", "Validator chạy trước; bị từ chối thì bỏ qua save và audit."),
                ("composition root returns a working graph", "Mỗi BuildProcessor nối service mới quanh CÙNG repo/audit được truyền vào."),
            ],
        ),
        solution='public class Solution\n{\n    public record Order(int Id, decimal Amount);\n\n    public interface IOrderValidator\n    {\n        bool IsValid(decimal amount);\n    }\n\n    public sealed class PositiveAmountValidator : IOrderValidator\n    {\n        public bool IsValid(decimal amount) => amount > 0;\n    }\n\n    public interface IOrderRepository\n    {\n        Order Save(Order order);\n    }\n\n    public sealed class MemoryRepo : IOrderRepository\n    {\n        private int _nextId = 1;\n        public System.Collections.Generic.List<Order> Saved { get; } = new();\n\n        public Order Save(Order order)\n        {\n            var saved = order with { Id = _nextId++ };\n            Saved.Add(saved);\n            return saved;\n        }\n    }\n\n    public interface IAuditLog\n    {\n        void Record(string message);\n    }\n\n    public sealed class MemoryAudit : IAuditLog\n    {\n        public System.Collections.Generic.List<string> Entries { get; } = new();\n\n        public void Record(string message) => Entries.Add(message);\n    }\n\n    public sealed class OrderProcessor\n    {\n        private readonly IOrderValidator _validator;\n        private readonly IOrderRepository _repo;\n        private readonly IAuditLog _audit;\n\n        public OrderProcessor(IOrderValidator validator, IOrderRepository repo, IAuditLog audit)\n        {\n            _validator = validator;\n            _repo = repo;\n            _audit = audit;\n        }\n\n        public string Process(decimal amount)\n        {\n            if (!_validator.IsValid(amount)) return "rejected";\n            var saved = _repo.Save(new Order(0, amount));\n            _audit.Record("order " + saved.Id + " amount " + saved.Amount);\n            return "ok:" + saved.Id;\n        }\n    }\n\n    public static OrderProcessor BuildProcessor(IOrderRepository repo, IAuditLog audit)\n    {\n        var container = new TinyContainer();\n        container.RegisterSingleton<IOrderValidator>(() => new PositiveAmountValidator());\n        container.RegisterTransient<OrderProcessor>(() => new OrderProcessor(\n            container.Resolve<IOrderValidator>(), repo, audit));\n        return container.Resolve<OrderProcessor>();\n    }\n}\n',
        wrong='public class Solution\n{\n    public record Order(int Id, decimal Amount);\n\n    public interface IOrderValidator\n    {\n        bool IsValid(decimal amount);\n    }\n\n    public sealed class PositiveAmountValidator : IOrderValidator\n    {\n        public bool IsValid(decimal amount) => amount > 0;\n    }\n\n    public interface IOrderRepository\n    {\n        Order Save(Order order);\n    }\n\n    public sealed class MemoryRepo : IOrderRepository\n    {\n        private int _nextId = 1;\n        public System.Collections.Generic.List<Order> Saved { get; } = new();\n\n        public Order Save(Order order)\n        {\n            var saved = order with { Id = _nextId++ };\n            Saved.Add(saved);\n            return saved;\n        }\n    }\n\n    public interface IAuditLog\n    {\n        void Record(string message);\n    }\n\n    public sealed class MemoryAudit : IAuditLog\n    {\n        public System.Collections.Generic.List<string> Entries { get; } = new();\n\n        public void Record(string message) => Entries.Add(message);\n    }\n\n    public sealed class OrderProcessor\n    {\n        private readonly IOrderValidator _validator;\n        private readonly IOrderRepository _repo;\n        private readonly IAuditLog _audit;\n\n        public OrderProcessor(IOrderValidator validator, IOrderRepository repo, IAuditLog audit)\n        {\n            _validator = validator;\n            _repo = repo;\n            _audit = audit;\n        }\n\n        public string Process(decimal amount)\n        {\n            if (!_validator.IsValid(amount)) return "rejected";\n            var saved = _repo.Save(new Order(0, amount));\n            _audit.Record("order " + saved.Id + " amount " + saved.Amount);\n            return "ok:" + saved.Id;\n        }\n    }\n\n    public static OrderProcessor BuildProcessor(IOrderRepository repo, IAuditLog audit)\n    {\n        // near-miss: registers the PROCESSOR as singleton keyed by the\n        // VALIDATOR type — Resolve<IOrderValidator> returns the processor\n        // cast, Resolve<OrderProcessor> is unregistered and throws; the\n        // BuildProcessor call fails outright\n        var container = new TinyContainer();\n        container.RegisterSingleton<IOrderValidator>(() => new PositiveAmountValidator());\n        container.RegisterSingleton<OrderProcessor>(() => new OrderProcessor(\n            new PositiveAmountValidator(), repo, audit));\n        container.RegisterTransient<OrderProcessor>(() =>\n            (OrderProcessor)container.Resolve<IOrderValidator>());\n        return container.Resolve<OrderProcessor>();\n    }\n}\n',
    )
print("module 11 authored")
