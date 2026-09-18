#!/usr/bin/env python3
"""C# — Intermediate — Module 4: csi-events.

Events & Observer: the event keyword, EventHandler<TArgs>, custom args,
encapsulation, unsubscribe/lifetime, and the Event-Driven Notification
System project. Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-events"

write_module(
    M,
    "Events & the Observer Pattern",
    "The event keyword as encapsulated multicast, EventHandler contracts, custom event args, and lifetime hygiene.",
    "Event & Observer Pattern",
    "Từ khóa event như multicast được đóng gói, hợp đồng EventHandler, event args tùy chỉnh, và vệ sinh vòng đời.",
    ["events-encapsulation", "eventargs-and-lifetime", "csi-checkpoint-m4"],
    ["csi-p4-events"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "events-encapsulation",
    "Events: Encapsulated Multicast",
    "What the event keyword adds over a public delegate field, publisher/subscriber roles, and safe-raise idiom.",
    16,
    r"""
## A field-like event is a delegate field with rules

A public delegate field lets ANYONE overwrite the list, clear it, or invoke
it. The `event` keyword keeps the field private and grants outsiders exactly
two operations: `+=` and `-=`.

```csharp
public class Order
{
    public event EventHandler<OrderEventArgs>? Placed;   // private backing field

    public void Place()
    {
        OnPlaced(new OrderEventArgs("ord-1", 42m));
    }

    protected virtual void OnPlaced(OrderEventArgs args) =>
        Placed?.Invoke(this, args);        // null-safe raise: nobody subscribed is fine
}
```

The raise goes through an instance method so derived classes can hook in
(`protected virtual`) — the .NET convention since day one.

## Publisher/subscriber roles

The publisher defines the event and *decides when* to raise it. Subscribers
attach handlers and *react* — they never raise, never reorder, never clear.
This one-way arrow is what makes event-driven systems debuggable: state
changes flow one direction.

```csharp
order.Placed += (sender, args) => Console.WriteLine($"order {args.Id} for {args.Total}");
order.Placed += Emailer.OnOrderPlaced;      // method group works too
order.Place();                               // both handlers run, in order
```

## Raising safely, always

`Placed?.Invoke(...)` — the `?.` snapshots the delegate list; a handler that
unsubscribes concurrently cannot null your call mid-flight. Never write
`if (Placed != null) Placed(...)` — check-then-call is a classic race.

## Check your understanding

- What can subscriber code do with an `event` that it can't with a public
  delegate field? (Only += and -=; no invoke, no clear, no overwrite.)
- Why `?.Invoke` instead of null-check + call? (Atomic snapshot of the list.)
""",
    "Event: Multicast được đóng gói",
    "Từ khóa event thêm gì so với trường delegate công khai, vai trò publisher/subscriber, và thành ngữ raise an toàn.",
    r"""
## Event kiểu-trường là trường delegate với luật lệ

Trường delegate công khai cho phép BẤT KỲ AI ghi đè danh sách, xóa nó, hay
gọi nó. Từ khóa `event` giữ trường riêng tư và cấp cho người ngoài đúng hai
thao tác: `+=` và `-=`.

```csharp
public class Order
{
    public event EventHandler<OrderEventArgs>? Placed;   // trường nền riêng tư

    public void Place()
    {
        OnPlaced(new OrderEventArgs("ord-1", 42m));
    }

    protected virtual void OnPlaced(OrderEventArgs args) =>
        Placed?.Invoke(this, args);        // raise an toàn: không ai đăng ký cũng ổn
}
```

Lời raise đi qua một phương thức instance để lớp dẫn xuất canh vào
(`protected virtual`) — quy ước .NET từ ngày đầu tiên.

## Vai trò publisher/subscriber

Publisher định nghĩa event và *quyết định khi nào* raise. Subscriber gắn
handler và *phản ứng* — họ không bao giờ raise, không sắp xếp lại, không xóa.
Mũi tên một chiều này làm hệ thống event-driven debug được: thay đổi trạng
thái chảy một hướng.

```csharp
order.Placed += (sender, args) => Console.WriteLine($"order {args.Id} for {args.Total}");
order.Placed += Emailer.OnOrderPlaced;      // method group cũng được
order.Place();                               // cả hai handler chạy, theo thứ tự
```

## Raise an toàn, luôn luôn

`Placed?.Invoke(...)` — `?.` chụp nhanh danh sách delegate; một handler hủy
đăng ký đồng thời không thể làm null lời gọi của bạn giữa chừng. Đừng bao giờ
viết `if (Placed != null) Placed(...)` — kiểm-tra-rồi-gọi là race kinh điển.

## Kiểm tra hiểu biết

- Code subscriber làm được gì với `event` mà không làm được với trường
  delegate công khai? (Chỉ += và -=; không invoke, không clear, không ghi đè.)
- Vì sao `?.Invoke` thay vì null-check rồi gọi? (Chụp nhanh danh sách nguyên tử.)
""",
    r"""
## Event kiểu-trường là trường delegate với luật lệ

Trường delegate công khai cho phép BẤT KỲ AI ghi đè danh sách, xóa nó, hay
gọi nó. Từ khóa `event` giữ trường riêng tư và cấp cho người ngoài đúng hai
thao tác: `+=` và `-=`.

```csharp
public class Order
{
    public event EventHandler<OrderEventArgs>? Placed;   // trường nền riêng tư

    public void Place()
    {
        OnPlaced(new OrderEventArgs("ord-1", 42m));
    }

    protected virtual void OnPlaced(OrderEventArgs args) =>
        Placed?.Invoke(this, args);        // raise an toàn: không ai đăng ký cũng ổn
}
```

Lời raise đi qua một phương thức instance để lớp dẫn xuất canh vào
(`protected virtual`) — quy ước .NET từ ngày đầu tiên.

## Vai trò publisher/subscriber

Publisher định nghĩa event và *quyết định khi nào* raise. Subscriber gắn
handler và *phản ứng* — họ không bao giờ raise, không sắp xếp lại, không xóa.
Mũi tên một chiều này làm hệ thống event-driven debug được: thay đổi trạng
thái chảy một hướng.

```csharp
order.Placed += (sender, args) => Console.WriteLine($"order {args.Id} for {args.Total}");
order.Placed += Emailer.OnOrderPlaced;      // method group cũng được
order.Place();                               // cả hai handler chạy, theo thứ tự
```

## Raise an toàn, luôn luôn

`Placed?.Invoke(...)` — `?.` chụp nhanh danh sách delegate; một handler hủy
đăng ký đồng thời không thể làm null lời gọi của bạn giữa chừng. Đừng bao giờ
viết `if (Placed != null) Placed(...)` — kiểm-tra-rồi-gọi là race kinh điển.

## Kiểm tra hiểu biết

- Code subscriber làm được gì với `event` mà không làm được với trường
  delegate công khai? (Chỉ += và -=; không invoke, không clear, không ghi đè.)
- Vì sao `?.Invoke` thay vì null-check rồi gọi? (Chụp nhanh danh sách nguyên tử.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "eventargs-and-lifetime",
    "EventArgs Contracts and Lifetime Hygiene",
    "EventHandler<T>, custom args records, unsubscribe discipline, and the static-event leak.",
    15,
    r"""
## The contract: sender + args

`EventHandler<TEventArgs>` is `void(object? sender, TEventArgs e)` with a
name that says what it is. Custom args carry everything a handler needs —
and nothing it doesn't:

```csharp
public sealed record TemperatureChangedEventArgs(
    string Sensor, double OldValue, double NewValue);

public class Thermometer
{
    public event EventHandler<TemperatureChangedEventArgs>? Changed;

    public double Value { get; private set; }

    public void Read(double newValue)
    {
        double old = Value;
        Value = newValue;
        Changed?.Invoke(this, new TemperatureChangedEventArgs("t1", old, newValue));
    }
}
```

Design rule: args are a snapshot at raise time. Handlers must not mutate the
publisher through them; if a handler needs to *influence* the outcome, that
is not an event — that is a callback (use `Func` or `CancelEventArgs`-style
mutable args deliberately).

## Unsubscribe is part of the contract

`+=` without a matching `-=` pins the subscriber for the publisher's
lifetime. Long-lived publishers (singletons, static events) + short-lived
subscribers = the leak:

```csharp
var t = new Thermometer();
t.Changed += OnChanged;      // static OnChanged, but t is now pinned by it
t.Changed -= OnChanged;      // only this releases t
```

Worse: `SomeStaticClass.Event += handler` holds subscribers *forever*. Static
events are a deliberate lifetime decision, not a convenience.

## Check your understanding

- Why snapshot args at raise time? (Handlers run later than the state change.)
- When is a static event acceptable? (When every subscriber lives as long as the process.)
""",
    "Hợp đồng EventArgs và vệ sinh vòng đời",
    "EventHandler<T>, args record tùy chỉnh, kỷ luật hủy đăng ký, và leak của static event.",
    r"""
## Hợp đồng: sender + args

`EventHandler<TEventArgs>` là `void(object? sender, TEventArgs e)` với cái tên
nói lên nó là gì. Args tùy chỉnh mang mọi thứ handler cần — và không gì hơn:

```csharp
public sealed record TemperatureChangedEventArgs(
    string Sensor, double OldValue, double NewValue);

public class Thermometer
{
    public event EventHandler<TemperatureChangedEventArgs>? Changed;

    public double Value { get; private set; }

    public void Read(double newValue)
    {
        double old = Value;
        Value = newValue;
        Changed?.Invoke(this, new TemperatureChangedEventArgs("t1", old, newValue));
    }
}
```

Luật thiết kế: args là ảnh chụp tại thời điểm raise. Handler không được biến
đổi publisher qua chúng; nếu handler cần *ảnh hưởng* kết quả, đó không phải
event — đó là callback (dùng `Func` hoặc args kiểu `CancelEventArgs` một cách
có chủ đích).

## Hủy đăng ký là một phần của hợp đồng

`+=` không kèm `-=` ghim subscriber trong suốt vòng đời của publisher.
Publisher sống lâu (singleton, static event) + subscriber sống ngắn = leak:

```csharp
var t = new Thermometer();
t.Changed += OnChanged;      // static OnChanged, nhưng t giờ bị ghim bởi nó
t.Changed -= OnChanged;      // chỉ có dòng này là thả t ra
```

Tệ hơn: `SomeStaticClass.Event += handler` giữ subscriber *mãi mãi*. Static
event là một quyết định vòng đời có chủ đích, không phải tiện lợi.

## Kiểm tra hiểu biết

- Vì sao chụp nhanh args lúc raise? (Handler chạy muộn hơn thay đổi trạng thái.)
- Khi nào static event chấp nhận được? (Khi mọi subscriber sống bằng process.)
""",
    r"""
## Hợp đồng: sender + args

`EventHandler<TEventArgs>` là `void(object? sender, TEventArgs e)` với cái tên
nói lên nó là gì. Args tùy chỉnh mang mọi thứ handler cần — và không gì hơn:

```csharp
public sealed record TemperatureChangedEventArgs(
    string Sensor, double OldValue, double NewValue);

public class Thermometer
{
    public event EventHandler<TemperatureChangedEventArgs>? Changed;

    public double Value { get; private set; }

    public void Read(double newValue)
    {
        double old = Value;
        Value = newValue;
        Changed?.Invoke(this, new TemperatureChangedEventArgs("t1", old, newValue));
    }
}
```

Luật thiết kế: args là ảnh chụp tại thời điểm raise. Handler không được biến
đổi publisher qua chúng; nếu handler cần *ảnh hưởng* kết quả, đó không phải
event — đó là callback (dùng `Func` hoặc args kiểu `CancelEventArgs` một cách
có chủ đích).

## Hủy đăng ký là một phần của hợp đồng

`+=` không kèm `-=` ghim subscriber trong suốt vòng đời của publisher.
Publisher sống lâu (singleton, static event) + subscriber sống ngắn = leak:

```csharp
var t = new Thermometer();
t.Changed += OnChanged;      // static OnChanged, nhưng t giờ bị ghim bởi nó
t.Changed -= OnChanged;      // chỉ có dòng này là thả t ra
```

Tệ hơn: `SomeStaticClass.Event += handler` giữ subscriber *mãi mãi*. Static
event là một quyết định vòng đời có chủ đích, không phải tiện lợi.

## Kiểm tra hiểu biết

- Vì sao chụp nhanh args lúc raise? (Handler chạy muộn hơn thay đổi trạng thái.)
- Khi nào static event chấp nhận được? (Khi mọi subscriber sống bằng process.)
""",
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m4",
    "Checkpoint — Event-Driven Notification System",
    "Build a publish/subscribe notification system with typed events, ordering, and clean unsubscribes.",
    22,
    r"""
## The gate (mini-build)

A `NotificationCenter` with two events:

1. `Published` — `EventHandler<NotificationEventArgs>` raised for every
   notification with (Id, Channel, Message). Handlers must see args
   snapshots; raising with no subscribers must not throw.
2. `Filtered` — raised when `Publish(channel, message, filter)` rejects a
   message; `filter` is a `Predicate<string>` the *caller* supplies per call.

Plus: `UnsubscribeAll()` clears both lists so a disposed center releases its
subscribers. The graded test registers handlers, publishes through a filter,
unsubscribes, and asserts the full observable behavior — order included.
""",
    "Checkpoint — Hệ thống thông báo dẫn động event",
    "Xây hệ thống publish/subscribe với event có kiểu, thứ tự, và hủy đăng ký sạch.",
    r"""
## Cổng kiểm tra (mini-build)

Một `NotificationCenter` với hai event:

1. `Published` — `EventHandler<NotificationEventArgs>` raise cho mọi thông
   báo với (Id, Channel, Message). Handler phải thấy ảnh chụp args; raise
   khi không ai đăng ký không được ném.
2. `Filtered` — raise khi `Publish(channel, message, filter)` từ chối một
   thông báo; `filter` là `Predicate<string>` mà *người gọi* cấp cho từng
   lần gọi.

Cộng thêm: `UnsubscribeAll()` xóa cả hai danh sách để một center đã giải phóng
thả hết subscriber. Test chấm đăng ký handler, publish qua filter, hủy đăng
ký, và khẳng định toàn bộ hành vi quan sát được — kể cả thứ tự.
""",
    challenge(
        "csi-checkpoint-m4-task",
        "Checkpoint: NotificationCenter",
        """Implement the NotificationCenter described in the checkpoint:

```csharp
public sealed record NotificationEventArgs(string Id, string Channel, string Message);

public class NotificationCenter
{
    public event EventHandler<NotificationEventArgs>? Published;   /* every accepted notification */
    public event EventHandler<NotificationEventArgs>? Filtered;   /* every rejected notification */
    /* publishes: filter null or filter(msg)==true -> raise Published;
       otherwise raise Filtered. Ids are "n-1", "n-2", ... starting at 1
       and incrementing for EVERY Publish call (accepted or not). */
    public void Publish(string channel, string message, Predicate<string>? filter);
    /* clears both subscription lists */
    public void UnsubscribeAll();
}
```""",
        CS_PRELUDE,
        [
            (
                "publish and filter",
                r"""
var log = new List<string>();
var center = new Solution.NotificationCenter();
center.Published += (s, e) => log.Add("P:" + e.Channel + ":" + e.Id);
center.Filtered += (s, e) => log.Add("F:" + e.Channel + ":" + e.Id);
center.Publish("email", "hello", null);
center.Publish("email", "spam", m => !m.Contains("spam"));
center.Publish("sms", "ok", m => !m.Contains("spam"));
Cj.Eq(string.Join("|", log), "P:email:n-1|F:email:n-2|P:sms:n-3", "ids count every publish; filter routes");
""",
                "One shared id counter increments on EVERY Publish; the predicate decides which event fires.",
            ),
            (
                "no subscribers, no throw",
                r"""
var quiet = new Solution.NotificationCenter();
quiet.Publish("email", "alone", null);
quiet.Publish("email", "still alone", m => false);
""",
                "?.Invoke handles the empty-list case — no subscribers is a normal state.",
            ),
            (
                "unsubscribe releases",
                r"""
var log2 = new List<string>();
var c2 = new Solution.NotificationCenter();
c2.Published += (s, e) => log2.Add("P:" + e.Message);
c2.Publish("x", "before", null);
c2.UnsubscribeAll();
c2.Publish("x", "after", null);
Cj.Eq(string.Join("|", log2), "P:before", "after UnsubscribeAll nothing fires");
""",
                "Set both events to null inside the class (same assembly, so assignment is legal).",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: NotificationCenter",
        "Hiện thực NotificationCenter mô tả trong checkpoint: hai event có kiểu, bộ đếm id đếm mọi lần publish, bộ lọc do người gọi cấp, và UnsubscribeAll thả hết subscriber.",
        [
            ("publish and filter", "Một bộ đếm id dùng chung tăng trên MỌI lần Publish; predicate quyết định event nào bắn."),
            ("no subscribers, no throw", "?.Invoke xử lý danh sách rỗng — không subscriber là trạng thái bình thường."),
            ("unsubscribe releases", "Gán null cho cả hai event bên trong lớp (cùng assembly nên phép gán hợp lệ)."),
        ],
    ),
    solution='public class Solution\n{\n    public sealed record NotificationEventArgs(string Id, string Channel, string Message);\n\n    public class NotificationCenter\n    {\n        public event EventHandler<NotificationEventArgs>? Published;\n        public event EventHandler<NotificationEventArgs>? Filtered;\n\n        private int _nextId = 1;\n\n        public void Publish(string channel, string message, Predicate<string>? filter)\n        {\n            var args = new NotificationEventArgs("n-" + _nextId, channel, message);\n            _nextId++;\n            if (filter is null || filter(message))\n            {\n                Published?.Invoke(this, args);\n            }\n            else\n            {\n                Filtered?.Invoke(this, args);\n            }\n        }\n\n        public void UnsubscribeAll()\n        {\n            Published = null;\n            Filtered = null;\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public sealed record NotificationEventArgs(string Id, string Channel, string Message);\n\n    public class NotificationCenter\n    {\n        public event EventHandler<NotificationEventArgs>? Published;\n        public event EventHandler<NotificationEventArgs>? Filtered;\n\n        private int _nextId = 1;\n\n        public void Publish(string channel, string message, Predicate<string>? filter)\n        {\n            // near-miss: the id counter only advances for ACCEPTED messages,\n            // so the filtered publish reuses n-1 and later ids shift\n            if (filter is null || filter(message))\n            {\n                var args = new NotificationEventArgs("n-" + _nextId, channel, message);\n                _nextId++;\n                Published?.Invoke(this, args);\n            }\n            else\n            {\n                Filtered?.Invoke(this, new NotificationEventArgs("n-" + _nextId, channel, message));\n            }\n        }\n\n        public void UnsubscribeAll()\n        {\n            Published = null;\n            Filtered = null;\n        }\n    }\n}\n',
)
print("module 4 authored")
