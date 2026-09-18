#!/usr/bin/env python3
"""C# — Beginner — Module 16: csb-delegates.

Behavior as data: Func/Action/Predicate, lambdas as delegate literals,
and events as multicast callbacks. Ws forget to invoke, invoke once, or
mutate the subscriber list mid-enumeration. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-delegates"

write_module(
    M,
    "Delegates, Lambdas, and Events",
    "Methods as values: Func and Action, lambda syntax, and the publisher-subscriber pattern behind every UI framework.",
    "Delegate, Lambda, và Event",
    "Phương thức như giá trị: Func và Action, cú pháp lambda, và mẫu publisher-subscriber đứng sau mọi UI framework.",
    ["csb-m16-func-action", "csb-m16-lambdas", "csb-m16-events", "csb-checkpoint-m16"],
    ["csb-p16-delegates"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m16-func-action",
    "Func, Action, Predicate",
    "Three generic delegate types cover almost every callback need — learn their shapes once.",
    12,
    r"""
## Methods as values

A **delegate** is a type whose values are methods. You pass a method where data would go, and invoke it later:

```csharp
static int Apply(int x, Func<int, int> f) => f(x);

Apply(5, n => n * 2);   // 10
Apply(5, n => n + 1);   // 6
```

The BCL's three workhorses:

- **`Action`** — takes 0–16 arguments, returns nothing: `Action<string> log = msg => Console.WriteLine(msg);`
- **`Func<T, TResult>`** — takes up to 16 arguments, last type parameter is the **return**: `Func<string, int> len = s => s.Length;`
- **`Predicate<T>`** — `Func<T, bool>` by another name: `Predicate<int> isEven = n => n % 2 == 0;`

The one syntax rule people trip on: in `Func<A, B, C>`, `A` and `B` are parameters, `C` is the return type.
""",
    "Func, Action, Predicate",
    "Ba kiểu delegate generic phủ gần như mọi nhu cầu callback — học hình dạng của chúng một lần.",
    r"""
## Phương thức như giá trị

Một **delegate** là kiểu mà giá trị của nó là các phương thức. Bạn truyền một phương thức vào chỗ dữ liệu, và gọi nó sau:

```csharp
static int Apply(int x, Func<int, int> f) => f(x);

Apply(5, n => n * 2);   // 10
Apply(5, n => n + 1);   // 6
```

Ba nhân vật chính của BCL:

- **`Action`** — nhận 0–16 đối số, không trả gì: `Action<string> log = msg => Console.WriteLine(msg);`
- **`Func<T, TResult>`** — nhận tới 16 đối số, tham số kiểu CUỐI là **kiểu trả về**: `Func<string, int> len = s => s.Length;`
- **`Predicate<T>`** — `Func<T, bool>` với tên khác: `Predicate<int> isEven = n => n % 2 == 0;`

Một luật cú pháp khiến người ta vấp: trong `Func<A, B, C>`, `A` và `B` là tham số, `C` là kiểu trả về.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m16-lambdas",
    "Lambda syntax and closures",
    "A lambda is an inline method — and it captures the variables around it, for better and worse.",
    13,
    r"""
## The forms

```csharp
Func<int, int> square = x => x * x;              // expression lambda
Func<int, int> step  = x => { return x + 1; };   // statement lambda
Func<int, int> zero  = _ => 0;                   // ignore the parameter
Action shout = () => Console.WriteLine("hey!");  // no parameters
```

`=>` reads "goes to". The compiler infers parameter types from the delegate type. `_` names a parameter you deliberately ignore.

## Closures: lambdas remember

```csharp
int offset = 10;
Func<int, int> shift = x => x + offset;   // captures offset
shift(5);   // 15
```

A lambda can use variables from the enclosing scope — the compiler wraps them into a hidden object so the lambda outlives the method call. That's a **closure**, and it's how `Where(n => n > min)` works: `min` travels with the lambda.

The classic trap: captured variables are *shared*, not copied. If `offset` changes later, `shift` sees the new value. And capturing a loop variable you mutate gives every lambda the same, final value.
""",
    "Cú pháp lambda và closure",
    "Lambda là một phương thức nội tuyến — và nó chụp lấy các biến quanh mình, vừa tốt vừa xấu.",
    r"""
## Các dạng

```csharp
Func<int, int> square = x => x * x;              // expression lambda
Func<int, int> step  = x => { return x + 1; };   // statement lambda
Func<int, int> zero  = _ => 0;                   // bỏ qua tham số
Action shout = () => Console.WriteLine("hey!");  // không tham số
```

`=>` đọc là "đi tới". Trình biên dịch suy ra kiểu tham số từ kiểu delegate. `_` là tên cho tham số bạn cố ý bỏ qua.

## Closure: lambda có trí nhớ

```csharp
int offset = 10;
Func<int, int> shift = x => x + offset;   // chụp offset
shift(5);   // 15
```

Lambda có thể dùng biến từ phạm vi bao quanh — trình biên dịch bọc chúng vào một đối tượng ẩn để lambda sống lâu hơn lời gọi phương thức. Đó là **closure**, và đó là lý do `Where(n => n > min)` hoạt động: `min` đi cùng lambda.

Bẫy kinh điển: biến bị chụp được *dùng chung*, không phải sao chép. Nếu `offset` đổi sau này, `shift` thấy giá trị mới. Và chụp biến vòng lặp mà bạn thay đổi sẽ cho mọi lambda cùng một giá trị-cuối-cùng.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m16-events",
    "Events: many listeners, one broadcast",
    "An event is a delegate that many methods subscribe to — the publisher never knows who's listening.",
    13,
    r"""
## From one callback to many

A `Func` parameter holds exactly **one** method. The **event** pattern removes that limit:

```csharp
class Thermometer
{
    public event Action<int>? Boiling;   // subscribers collect here

    public void Check(int celsius)
    {
        if (celsius >= 100)
            Boiling?.Invoke(celsius);    // broadcast: all subscribers run
    }
}

var t = new Thermometer();
t.Boiling += c => Console.WriteLine($"alarm: {c}");
t.Boiling += c => Stats.Record(c);
t.Check(101);   // both run
```

`+=` subscribes, `-=` unsubscribes. `?.Invoke` broadcasts only when someone listens — null when the list is empty.

## The contract

The publisher defines the event's delegate type; subscribers conform. Outside the class, an event is subscribe-only — you can't invoke or clear someone else's event. That's the difference from a plain delegate field: **encapsulation on the invocation**, which is what makes pub/sub safe at scale.

Unsubscribing matters too: a subscriber the publisher outlives leaks memory until `-=` runs.
""",
    "Event: nhiều người nghe, một bản tin",
    "Một event là delegate mà nhiều phương thức đăng ký — publisher không bao giờ biết ai đang nghe.",
    r"""
## Từ một callback tới nhiều

Tham số `Func` giữ đúng **một** phương thức. Mẫu **event** xóa giới hạn đó:

```csharp
class Thermometer
{
    public event Action<int>? Boiling;   // người đăng ký tụ họp ở đây

    public void Check(int celsius)
    {
        if (celsius >= 100)
            Boiling?.Invoke(celsius);    // phát sóng: tất cả subscriber chạy
    }
}

var t = new Thermometer();
t.Boiling += c => Console.WriteLine($"cảnh báo: {c}");
t.Boiling += c => Stats.Record(c);
t.Check(101);   // cả hai chạy
```

`+=` đăng ký, `-=` hủy đăng ký. `?.Invoke` chỉ phát sóng khi có người nghe — null khi danh sách rỗng.

## Hợp đồng

Publisher định nghĩa kiểu delegate của event; subscriber tuân theo. Từ bên ngoài lớp, event chỉ-đăng-ký — bạn không thể gọi hoặc xóa event của người khác. Đó là điểm khác một trường delegate thường: **đóng gói việc kích hoạt**, thứ làm pub/sub an toàn khi mở rộng.

Hủy đăng ký cũng quan trọng: một subscriber mà publisher sống lâu hơn sẽ rò rỉ bộ nhớ cho tới khi `-=` chạy.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p16-delegates",
    "Delegates workout",
    "Pipelines, calculators, closures, and event buses — behavior-as-data under discriminating tests.",
    "Luyện tập delegates",
    "Đường ống, máy tính, closure, và event bus — hành-vi-như-dữ-liệu dưới các bài kiểm tra phân biệt.",
    "csb-m16-events",
    40,
    "beginner",
    [
        challenge(
            "csb-p16-pipeline",
            "Function pipeline",
            "Implement `static int Pipe(int input, params Func<int, int>[] steps)` — apply each function in order to the result of the previous. Empty/null steps → input unchanged.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.Pipe(5, x => x + 1, x => x * 2), 12, \"add then double\");\nCj.Eq(Solution.Pipe(5, x => x * 2, x => x + 1), 11, \"double then add — order matters\");\nCj.Eq(Solution.Pipe(5), 5, \"no steps\");",
                    "Same functions, different order, different answer — sequential application.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.Pipe(7, x => x), 7, \"identity\");\nCj.Eq(Solution.Pipe(7, null), 7, \"null steps treated as none\");",
                    "Null-safe: an absent pipeline is the identity function.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p16-calculator",
            "Operator dispatch table",
            "Implement `static int Eval(char op, int a, int b)` using a dispatch table of `Func<int, int, int>` (dictionary from char to function): '+' '−' '*' '/' (integer division). Unknown operator → `ArgumentException`. Division by zero propagates naturally.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.Eval('+', 2, 3), 5, \"add\");\nCj.Eq(Solution.Eval('*', 4, 5), 20, \"mul\");\nCj.Eq(Solution.Eval('/', 9, 2), 4, \"int division\");\nCj.Eq(Solution.Eval('-', 10, 4), 6, \"sub\");",
                    "Four keys, four functions — no if-chains.",
                ),
                (
                    "unknown",
                    "bool t = false;\ntry { Solution.Eval('%', 1, 2); } catch (ArgumentException) { t = true; }\nCj.True(t, \"unknown op rejected\");\nbool t2 = false;\ntry { Solution.Eval('/', 1, 0); } catch (DivideByZeroException) { t2 = true; }\nCj.True(t2, \"divide by zero surfaces\");",
                    "Missing keys throw; arithmetic errors are not swallowed.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p16-closure",
            "Closures: counter factory",
            "Implement `static (Func<int> Next, Action Reset) MakeCounter(int start)` — `Next()` returns the current value then increments; `Reset()` restores the value to `start`. Each call to `MakeCounter` must produce an INDEPENDENT counter.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var (next, reset) = Solution.MakeCounter(10);\nCj.Eq(next(), 10, \"first next returns start\");\nCj.Eq(next(), 11, \"then increments\");\nreset();\nCj.Eq(next(), 10, \"reset restores\");",
                    "Next reads-then-increments; Reset restores the captured start.",
                ),
                (
                    "independence",
                    "var (n1, _) = Solution.MakeCounter(0);\nvar (n2, _) = Solution.MakeCounter(100);\nn1(); n1();\nCj.Eq(n2(), 100, \"second counter untouched by first\");",
                    "Two counters, two captured states — closure per call, not per method.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p16-eventbus",
            "A tiny event bus",
            "Implement nested class `Solution.EventBus`: `event Action<string>? OnMessage;`, `void Publish(string message)` (invokes subscribers with the message; safe when none), `void Subscribe(Action<string> handler)`, `void Unsubscribe(Action<string> handler)`. Subscribers run in subscription order.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "var bus = new Solution.EventBus();\nvar log = new List<string>();\nbus.Subscribe(m => log.Add(\"a:\" + m));\nbus.Subscribe(m => log.Add(\"b:\" + m));\nbus.Publish(\"go\");\nCj.Eq(string.Join(\"|\", log), \"a:go|b:go\", \"both subscribers, in order\");",
                    "Multicast delivery in subscription order.",
                ),
                (
                    "unsubscribe",
                    "var bus = new Solution.EventBus();\nvar log = new List<string>();\nAction<string> h = m => log.Add(\"h:\" + m);\nbus.Subscribe(h);\nbus.Unsubscribe(h);\nbus.Publish(\"x\");\nCj.Eq(log.Count, 0, \"unsubscribed handler does not fire\");\nbus.Publish(\"y\");\nCj.Eq(log.Count, 0, \"still silent — and no crash with zero subscribers\");",
                    "Unsubscribe removes exactly that handler; publishing with none must not throw.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p16-pipeline": vi_challenge(
            "Đường ống hàm",
            "Hiện thực `static int Pipe(int input, params Func<int, int>[] steps)` — áp dụng từng hàm theo thứ tự lên kết quả của hàm trước. steps rỗng/null → input không đổi.",
            [
                ("normal", "Cùng các hàm, thứ tự khác, kết quả khác — áp dụng tuần tự."),
                ("edges", "An toàn với null: đường ống vắng mặt là hàm đồng nhất."),
            ],
        ),
        "csb-p16-calculator": vi_challenge(
            "Bảng điều phối toán tử",
            "Hiện thực `static int Eval(char op, int a, int b)` dùng bảng điều phối các `Func<int, int, int>` (dictionary từ char sang hàm): '+' '−' '*' '/' (chia nguyên). Toán tử lạ → `ArgumentException`. Chia cho 0 lan truyền tự nhiên.",
            [
                ("normal", "Bốn khóa, bốn hàm — không chuỗi if."),
                ("unknown", "Khóa thiếu thì ném; lỗi số học không bị nuốt."),
            ],
        ),
        "csb-p16-closure": vi_challenge(
            "Closure: nhà máy bộ đếm",
            "Hiện thực `static (Func<int> Next, Action Reset) MakeCounter(int start)` — `Next()` trả giá trị hiện tại rồi tăng; `Reset()` khôi phục giá trị về `start`. Mỗi lần gọi `MakeCounter` phải tạo một bộ đếm ĐỘC LẬP.",
            [
                ("normal", "Next đọc-rồi-tăng; Reset khôi phục start đã chụp."),
                ("independence", "Hai bộ đếm, hai trạng thái đã chụp — closure mỗi lần gọi, không phải mỗi phương thức."),
            ],
        ),
        "csb-p16-eventbus": vi_challenge(
            "Event bus mini",
            "Hiện thực lớp lồng `Solution.EventBus`: `event Action<string>? OnMessage;`, `void Publish(string message)` (gọi các subscriber với message; an toàn khi không có ai), `void Subscribe(Action<string> handler)`, `void Unsubscribe(Action<string> handler)`. Subscriber chạy theo thứ tự đăng ký.",
            [
                ("normal", "Phát đa hướng theo thứ tự đăng ký."),
                ("unsubscribe", "Hủy đăng ký removes đúng handler đó; phát khi không có subscriber không được ném."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p16-pipeline",
            'public class Solution\n{\n    public static int Pipe(int input, params Func<int, int>[] steps)\n    {\n        if (steps == null) return input;\n        int value = input;\n        foreach (Func<int, int> step in steps)\n        {\n            value = step(value);\n        }\n        return value;\n    }\n}\n',
            'public class Solution\n{\n    public static int Pipe(int input, params Func<int, int>[] steps)\n    {\n        if (steps == null) return input;\n        // near-miss: applies every step to the ORIGINAL input instead of\n        // chaining — only the last step\'s effect survives\n        foreach (Func<int, int> step in steps)\n        {\n            _ = step(input);\n        }\n        return steps.Length > 0 ? steps[steps.Length - 1](input) : input;\n    }\n}\n',
        ),
        (
            "csb-p16-calculator",
            'public class Solution\n{\n    private static readonly Dictionary<char, Func<int, int, int>> Ops = new Dictionary<char, Func<int, int, int>>\n    {\n        [\'+\'] = (a, b) => a + b,\n        [\'-\'] = (a, b) => a - b,\n        [\'*\'] = (a, b) => a * b,\n        [\'/\'] = (a, b) => a / b,\n    };\n    public static int Eval(char op, int a, int b)\n    {\n        if (!Ops.TryGetValue(op, out Func<int, int, int> f))\n            throw new ArgumentException("unknown operator");\n        return f(a, b);\n    }\n}\n',
            'public class Solution\n{\n    private static readonly Dictionary<char, Func<int, int, int>> Ops = new Dictionary<char, Func<int, int, int>>\n    {\n        [\'+\'] = (a, b) => a + b,\n        [\'-\'] = (a, b) => a - b,\n        [\'*\'] = (a, b) => a * b,\n        [\'/\'] = (a, b) => a / b,\n    };\n    public static int Eval(char op, int a, int b)\n    {\n        if (!Ops.TryGetValue(op, out Func<int, int, int> f))\n            throw new ArgumentException("unknown operator");\n        // near-miss: swapped operand order — subtraction and division are\n        // not commutative, so Eval(\'-\', 10, 4) yields -6\n        return f(b, a);\n    }\n}\n',
        ),
        (
            "csb-p16-closure",
            'public class Solution\n{\n    public static (Func<int> Next, Action Reset) MakeCounter(int start)\n    {\n        int current = start;\n        int Next() => current++;\n        void Reset() => current = start;\n        return (Next, Reset);\n    }\n}\n',
            'public class Solution\n{\n    private static int _shared;   // oops\n    public static (Func<int> Next, Action Reset) MakeCounter(int start)\n    {\n        // near-miss: state in a STATIC field instead of a per-call closure —\n        // every counter mutates the same slot, breaking independence\n        _shared = start;\n        int Next() => _shared++;\n        void Reset() => _shared = start;\n        return (Next, Reset);\n    }\n}\n',
        ),
        (
            "csb-p16-eventbus",
            'public class Solution\n{\n    public sealed class EventBus\n    {\n        private readonly List<Action<string>> handlers = new List<Action<string>>();\n        public event Action<string>? OnMessage;\n        public void Subscribe(Action<string> handler)\n        {\n            handlers.Add(handler);\n            OnMessage += handler;\n        }\n        public void Unsubscribe(Action<string> handler)\n        {\n            handlers.Remove(handler);\n            OnMessage -= handler;\n        }\n        public void Publish(string message)\n        {\n            OnMessage?.Invoke(message);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class EventBus\n    {\n        private readonly List<Action<string>> handlers = new List<Action<string>>();\n        public event Action<string>? OnMessage;\n        public void Subscribe(Action<string> handler)\n        {\n            handlers.Add(handler);\n            // near-miss: ASSIGNMENT instead of combination — every new\n            // subscriber silently REPLACES the previous one, so only the\n            // latest handler ever fires\n            OnMessage = handler;\n        }\n        public void Unsubscribe(Action<string> handler)\n        {\n            handlers.Remove(handler);\n            OnMessage -= handler;\n        }\n        public void Publish(string message)\n        {\n            OnMessage?.Invoke(message);\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m16",
    "Checkpoint — Delegates & events",
    "An alarm system: sensors publish, a panel subscribes, filters are lambdas, and history is a closure.",
    20,
    r"""
## Checkpoint: the alarm system

**Task:** implement in `Solution`:

1. Nested class `AlarmSystem`:
   - `event Action<string, int>? Triggered;` (sensor name, level)
   - `void Arm(string sensor, int threshold)` — records the sensor's threshold.
   - `void Reading(string sensor, int value)` — when the sensor is armed and `value >= threshold`, fires `Triggered` with that sensor and value. Unknown sensors are ignored.
   - `void Disarm(string sensor)`.
2. `static List<int> LevelsAbove(List<int> readings, int threshold)` — readings strictly above the threshold, as a lambda-filtered list.
3. `static Func<int> MakeAverager()` — returns a closure that yields the running average of all values passed to successive calls (first call = first value).
""",
    "Checkpoint — Delegate & event",
    "Hệ thống báo động: cảm biến phát, bảng điều khiển đăng ký, bộ lọc là lambda, và lịch sử là một closure.",
    r"""
## Checkpoint: hệ thống báo động

**Nhiệm vụ:** hiện thực trong `Solution`:

1. Lớp lồng `AlarmSystem`:
   - `event Action<string, int>? Triggered;` (tên cảm biến, mức)
   - `void Arm(string sensor, int threshold)` — ghi nhận ngưỡng của cảm biến.
   - `void Reading(string sensor, int value)` — khi cảm biến đã được kích hoạt và `value >= threshold`, kích hoạt `Triggered` với cảm biến và giá trị đó. Cảm biến lạ bị bỏ qua.
   - `void Disarm(string sensor)`.
2. `static List<int> LevelsAbove(List<int> readings, int threshold)` — các giá trị lớn-hơn-nghiêm-ngặt ngưỡng, lọc bằng lambda.
3. `static Func<int> MakeAverager()` — trả một closure cho trung bình chạy dần của mọi giá trị được truyền qua các lần gọi (lần đầu = giá trị đầu tiên).
""",
    challenge(
        "csb-checkpoint-m16-task",
        "AlarmSystem",
        "Implement `AlarmSystem`, `LevelsAbove`, and `MakeAverager` — arming state, filtered readings, and a stateful closure.",
        CS_PRELUDE,
        [
            (
                "alarm",
                "var sys = new Solution.AlarmSystem();\nvar fired = new List<string>();\nsys.Triggered += (s, v) => fired.Add(s + \":\" + v);\nsys.Arm(\"door\", 5);\nsys.Reading(\"door\", 3);\nsys.Reading(\"window\", 9);\nsys.Reading(\"door\", 7);\nCj.Eq(string.Join(\"|\", fired), \"door:7\", \"only armed sensor over threshold fires\");\nsys.Disarm(\"door\");\nsys.Reading(\"door\", 10);\nCj.Eq(fired.Count, 1, \"disarmed sensor is silent\");",
                "Arm/disarm gates the event; unknown sensors never fire.",
            ),
            (
                "lambda-and-closure",
                "var lv = Solution.LevelsAbove(new List<int> { 1, 5, 7, 2 }, 4);\nCj.Eq(string.Join(\",\", lv), \"5,7\", \"strictly above, order kept\");\nvar avg = Solution.MakeAverager();\nCj.Eq(avg(10), 10, \"first call is the first value\");\nCj.Eq(avg(20), 15, \"running average so far\");\nvar avg2 = Solution.MakeAverager();\nCj.Eq(avg2(4), 4, \"fresh averager starts empty\");\nCj.Eq(avg(30), 20, \"independent closures keep their own totals\");",
                "Lambda filter plus a per-call closure.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "AlarmSystem",
        "Hiện thực `AlarmSystem`, `LevelsAbove`, và `MakeAverager` — trạng thái kích hoạt, giá trị được lọc, và một closure có trạng thái.",
        [
            ("alarm", "Arm/disarm khóa event; cảm biến lạ không bao giờ kích hoạt."),
            ("lambda-and-closure", "Bộ lọc lambda cộng một closure theo từng lần gọi."),
        ],
    ),
    solution='public class Solution\n{\n    public sealed class AlarmSystem\n    {\n        private readonly Dictionary<string, int> armed = new Dictionary<string, int>();\n        public event Action<string, int>? Triggered;\n        public void Arm(string sensor, int threshold)\n        {\n            armed[sensor] = threshold;\n        }\n        public void Disarm(string sensor)\n        {\n            armed.Remove(sensor);\n        }\n        public void Reading(string sensor, int value)\n        {\n            if (armed.TryGetValue(sensor, out int threshold) && value >= threshold)\n                Triggered?.Invoke(sensor, value);\n        }\n    }\n    public static List<int> LevelsAbove(List<int> readings, int threshold)\n    {\n        if (readings == null) return new List<int>();\n        return readings.Where(v => v > threshold).ToList();\n    }\n    public static Func<int, int> MakeAverager()\n    {\n        long total = 0;\n        int count = 0;\n        return value =>\n        {\n            total += value;\n            count++;\n            return (int)(total / count);\n        };\n    }\n}\n',
    wrong='public class Solution\n{\n    public sealed class AlarmSystem\n    {\n        private readonly Dictionary<string, int> armed = new Dictionary<string, int>();\n        public event Action<string, int>? Triggered;\n        public void Arm(string sensor, int threshold)\n        {\n            armed[sensor] = threshold;\n        }\n        public void Disarm(string sensor)\n        {\n            // near-miss: disarm does nothing \u2014 the sensor keeps firing after\n            // being disarmed, silently violating the lifecycle\n        }\n        public void Reading(string sensor, int value)\n        {\n            if (armed.TryGetValue(sensor, out int threshold) && value >= threshold)\n                Triggered?.Invoke(sensor, value);\n        }\n    }\n    public static List<int> LevelsAbove(List<int> readings, int threshold)\n    {\n        if (readings == null) return new List<int>();\n        return readings.Where(v => v > threshold).ToList();\n    }\n    // near-miss: averager state in STATIC fields \u2014 every averager\n    // shares one running total, so independent closures are impossible\n    private static long _total;\n    private static int _count;\n    public static Func<int, int> MakeAverager()\n    {\n        return value =>\n        {\n            _total += value;\n            _count++;\n            return (int)(_total / _count);\n        };\n    }\n}\n',
)

print("module 16 authored")
