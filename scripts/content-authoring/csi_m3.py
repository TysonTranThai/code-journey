#!/usr/bin/env python3
"""C# — Intermediate — Module 3: csi-delegates.

Delegates, lambdas, closures: method groups, Func/Action/Predicate shapes,
composition, capture semantics, and the classic loop-capture bug. Ws are
behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-delegates"

write_module(
    M,
    "Delegates, Lambdas & Closures",
    "Methods as values: the shapes, composition pipelines, capture semantics, and the bugs capture semantics cause.",
    "Delegate, Lambda & Closure",
    "Phương thức như giá trị: các hình dạng, pipeline ghép, ngữ nghĩa capture, và các bug mà ngữ nghĩa capture gây ra.",
    ["delegates-shapes", "closures-capture", "composition-pipelines", "csi-checkpoint-m3"],
    ["csi-p3-closures", "csi-p3-pipelines"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "delegates-shapes",
    "Delegate Shapes: Method Groups, Func, Action, Predicate",
    "The type behind every lambda, why method groups convert, and which generic shape fits which job.",
    16,
    r"""
## A delegate type is a function's type

`delegate int Calculator(int a, int b)` declares that some methods have this
shape. Any method matching the signature converts implicitly — the **method
group conversion**:

```csharp
static int Add(int a, int b) => a + b;
Calculator op = Add;          // method group -> delegate instance
int result = op(2, 3);        // invoke like a method
```

You will rarely declare one. The BCL ships the shapes you need:

- `Action` / `Action<T...>` — takes 0..16 args, returns void.
- `Func<T... TResult>` — takes 0..16 args, returns TResult.
- `Predicate<T>` — takes T, returns bool. (`Func<T, bool>` in a trench coat;
  both work with LINQ, `Predicate` reads better on `List<T>.Find`.)

```csharp
Action tick = () => Console.WriteLine("tick");
Func<int, int> square = x => x * x;
Func<int, int, int> add = static (a, b) => a + b;   // static: no capture allowed
Predicate<string> isEmpty = string.IsNullOrEmpty;
```

`static` lambdas promise no capture — a compiler-checked guard against
accidentally closing over state.

## Multicast: delegates are lists in disguise

`+` and `-` compose delegate instances into an invocation list:

```csharp
Action pipeline = Step1;
pipeline += Step2;        // now both run, in order
pipeline -= Step1;        // only Step2 remains
```

Invocation returns the LAST handler's value (for Func) — a reason multicast
fits Actions (events) far better than Funcs.

## Check your understanding

- Why does `Func<T, bool>` coexist with `Predicate<T>`? (History; `List<T>` predates `Func`.)
- What does `+=` on a delegate actually do? (Creates a new delegate whose list is both.)
""",
    "Hình dạng Delegate: Method Group, Func, Action, Predicate",
    "Kiểu đứng sau mọi lambda, vì sao method group chuyển đổi được, và hình dạng generic nào hợp việc nào.",
    r"""
## Kiểu delegate là kiểu của một hàm

`delegate int Calculator(int a, int b)` tuyên bố rằng một số phương thức có
hình dạng này. Mọi phương thức khớp chữ ký chuyển đổi ngầm — **method group
conversion**:

```csharp
static int Add(int a, int b) => a + b;
Calculator op = Add;          // method group -> đối tượng delegate
int result = op(2, 3);        // gọi như một phương thức
```

Bạn sẽ hiếm khi tự khai báo. BCL sẵn các hình dạng cần:

- `Action` / `Action<T...>` — nhận 0..16 tham số, trả void.
- `Func<T... TResult>` — nhận 0..16 tham số, trả TResult.
- `Predicate<T>` — nhận T, trả bool. (`Func<T, bool>` mặc áo mưa; cả hai dùng
  được với LINQ, `Predicate` đọc tốt hơn trên `List<T>.Find`.)

```csharp
Action tick = () => Console.WriteLine("tick");
Func<int, int> square = x => x * x;
Func<int, int, int> add = static (a, b) => a + b;   // static: cấm capture
Predicate<string> isEmpty = string.IsNullOrEmpty;
```

`static` lambda hứa không capture — lớp chắn được compiler kiểm tra chống
việc lỡ tay đóng trên trạng thái.

## Multicast: delegate là danh sách trá hình

`+` và `-` ghép các đối tượng delegate thành danh sách gọi:

```csharp
Action pipeline = Step1;
pipeline += Step2;        // giờ cả hai chạy, theo thứ tự
pipeline -= Step1;        // chỉ còn Step2
```

Lời gọi trả về giá trị của handler CUỐI (với Func) — lý do multicast hợp
với Action (event) hơn nhiều so với Func.

## Kiểm tra hiểu biết

- Vì sao `Func<T, bool>` tồn tại song song `Predicate<T>`? (Lịch sử; `List<T>` ra đời trước `Func`.)
- `+=` trên delegate thực sự làm gì? (Tạo delegate mới với danh sách gồm cả hai.)
""",
    r"""
## Kiểu delegate là kiểu của một hàm

`delegate int Calculator(int a, int b)` tuyên bố rằng một số phương thức có
hình dạng này. Mọi phương thức khớp chữ ký chuyển đổi ngầm — **method group
conversion**:

```csharp
static int Add(int a, int b) => a + b;
Calculator op = Add;          // method group -> đối tượng delegate
int result = op(2, 3);        // gọi như một phương thức
```

Bạn sẽ hiếm khi tự khai báo. BCL sẵn các hình dạng cần:

- `Action` / `Action<T...>` — nhận 0..16 tham số, trả void.
- `Func<T... TResult>` — nhận 0..16 tham số, trả TResult.
- `Predicate<T>` — nhận T, trả bool. (`Func<T, bool>` mặc áo mưa; cả hai dùng
  được với LINQ, `Predicate` đọc tốt hơn trên `List<T>.Find`.)

```csharp
Action tick = () => Console.WriteLine("tick");
Func<int, int> square = x => x * x;
Func<int, int, int> add = static (a, b) => a + b;   // static: cấm capture
Predicate<string> isEmpty = string.IsNullOrEmpty;
```

`static` lambda hứa không capture — lớp chắn được compiler kiểm tra chống
việc lỡ tay đóng trên trạng thái.

## Multicast: delegate là danh sách trá hình

`+` và `-` ghép các đối tượng delegate thành danh sách gọi:

```csharp
Action pipeline = Step1;
pipeline += Step2;        // giờ cả hai chạy, theo thứ tự
pipeline -= Step1;        // chỉ còn Step2
```

Lời gọi trả về giá trị của handler CUỐI (với Func) — lý do multicast hợp
với Action (event) hơn nhiều so với Func.

## Kiểm tra hiểu biết

- Vì sao `Func<T, bool>` tồn tại song song `Predicate<T>`? (Lịch sử; `List<T>` ra đời trước `Func`.)
- `+=` trên delegate thực sự làm gì? (Tạo delegate mới với danh sách gồm cả hai.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "closures-capture",
    "Closures and Capture Semantics",
    "What a lambda captures (variables, not values), the loop-capture trap, and lifetime consequences.",
    15,
    r"""
## Lambdas capture VARIABLES, not values

A closure captures the variable itself — the storage location. Changes after
capture are visible; the lambda's lifetime extends the variable's:

```csharp
int counter = 0;
Action bump = () => counter++;   // captures the VARIABLE counter
bump(); bump();
Console.WriteLine(counter);      // 2 — same storage
```

Each *execution* of a scope produces fresh storage:

```csharp
static Func<int> MakeCounter()
{
    int count = 0;
    return () => ++count;        // each MakeCounter() call: its own count
}
var a = MakeCounter(); var b = MakeCounter();
a(); a(); b();                    // a:2, b:1 — independent
```

## The classic loop-capture bug

```csharp
var actions = new List<Action>();
for (int i = 0; i < 3; i++)
    actions.Add(() => Console.Write(i));
foreach (var a in actions) a();      // 333 in old-style for: ONE variable i
```

The `for` loop declares ONE variable `i` shared by all three lambdas — after
the loop it is 3, so all print 3. Fixes, both real-world:

```csharp
for (int i = 0; i < 3; i++) { int copy = i; actions.Add(() => use(copy)); }
// or foreach with an inline variable:
foreach (int i in Enumerable.Range(0, 3))   // per-iteration variable
    actions.Add(() => use(i));               // 012
```

`foreach` variables are per-iteration since C# 5 — the trap is specifically
classic `for` with an incrementing index.

## Lifetime: closures keep things alive

A captured object cannot be collected while the lambda lives. A lambda
registered in a long-lived component and capturing a big object is a leak
shaped like a feature. Capture narrowly: capture the two fields you need,
not `this` holding everything.

## Check your understanding

- `int x = 1; var f = () => x; x = 2; f()` — what? (2: captured variable read at invoke.)
- Why do static lambdas exist? (Compile-time proof of no capture.)
""",
    "Closure và ngữ nghĩa Capture",
    "Lambda capture cái gì (biến, không phải giá trị), bẫy capture trong vòng lặp, và hệ quả vòng đời.",
    r"""
## Lambda capture BIẾN, không phải giá trị

Closure capture chính biến — ô nhớ. Thay đổi sau lúc capture đều thấy được;
vòng đời của lambda kéo dài vòng đời của biến:

```csharp
int counter = 0;
Action bump = () => counter++;   // capture BIẾN counter
bump(); bump();
Console.WriteLine(counter);      // 2 — cùng ô nhớ
```

Mỗi lần *thực thi* một phạm vi tạo ô nhớ mới:

```csharp
static Func<int> MakeCounter()
{
    int count = 0;
    return () => ++count;        // mỗi lần gọi MakeCounter(): count riêng
}
var a = MakeCounter(); var b = MakeCounter();
a(); a(); b();                    // a:2, b:1 — độc lập
```

## Bẫy capture trong vòng lặp kinh điển

```csharp
var actions = new List<Action>();
for (int i = 0; i < 3; i++)
    actions.Add(() => Console.Write(i));
foreach (var a in actions) a();      // 333 với for cổ điển: MỘT biến i
```

Vòng `for` khai báo MỘT biến `i` dùng chung cho cả ba lambda — sau vòng lặp
nó là 3, nên cả ba in 3. Cách sửa, cả hai đều là thực tế production:

```csharp
for (int i = 0; i < 3; i++) { int copy = i; actions.Add(() => use(copy)); }
// hoặc foreach với biến inline:
foreach (int i in Enumerable.Range(0, 3))   // biến theo-từng-vòng
    actions.Add(() => use(i));               // 012
```

Biến `foreach` theo từng vòng từ C# 5 — cái bẫy riêng biệt là `for` cổ điển
với chỉ số tăng.

## Vòng đời: closure giữ mọi thứ sống

Đối tượng bị capture không thể thu gom khi lambda còn sống. Một lambda đăng
ký vào component sống lâu và capture một đối tượng lớn là một memory leak
mặc áo tính năng. Capture hẹp: capture hai trường bạn cần, không phải `this`
giữ tất cả.

## Kiểm tra hiểu biết

- `int x = 1; var f = () => x; x = 2; f()` — ra gì? (2: biến captured đọc lúc gọi.)
- Vì sao static lambda tồn tại? (Bằng chứng lúc biên dịch về việc không capture.)
""",
    r"""
## Lambda capture BIẾN, không phải giá trị

Closure capture chính biến — ô nhớ. Thay đổi sau lúc capture đều thấy được;
vòng đời của lambda kéo dài vòng đời của biến:

```csharp
int counter = 0;
Action bump = () => counter++;   // capture BIẾN counter
bump(); bump();
Console.WriteLine(counter);      // 2 — cùng ô nhớ
```

Mỗi lần *thực thi* một phạm vi tạo ô nhớ mới:

```csharp
static Func<int> MakeCounter()
{
    int count = 0;
    return () => ++count;        // mỗi lần gọi MakeCounter(): count riêng
}
var a = MakeCounter(); var b = MakeCounter();
a(); a(); b();                    // a:2, b:1 — độc lập
```

## Bẫy capture trong vòng lặp kinh điển

```csharp
var actions = new List<Action>();
for (int i = 0; i < 3; i++)
    actions.Add(() => Console.Write(i));
foreach (var a in actions) a();      // 333 với for cổ điển: MỘT biến i
```

Vòng `for` khai báo MỘT biến `i` dùng chung cho cả ba lambda — sau vòng lặp
nó là 3, nên cả ba in 3. Cách sửa, cả hai đều là thực tế production:

```csharp
for (int i = 0; i < 3; i++) { int copy = i; actions.Add(() => use(copy)); }
// hoặc foreach với biến inline:
foreach (int i in Enumerable.Range(0, 3))   // biến theo-từng-vòng
    actions.Add(() => use(i));               // 012
```

Biến `foreach` theo từng vòng từ C# 5 — cái bẫy riêng biệt là `for` cổ điển
với chỉ số tăng.

## Vòng đời: closure giữ mọi thứ sống

Đối tượng bị capture không thể thu gom khi lambda còn sống. Một lambda đăng
ký vào component sống lâu và capture một đối tượng lớn là một memory leak
mặc áo tính năng. Capture hẹp: capture hai trường bạn cần, không phải `this`
giữ tất cả.

## Kiểm tra hiểu biết

- `int x = 1; var f = () => x; x = 2; f()` — ra gì? (2: biến captured đọc lúc gọi.)
- Vì sao static lambda tồn tại? (Bằng chứng lúc biên dịch về việc không capture.)
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "composition-pipelines",
    "Composition: Callbacks, Pipelines, Strategy",
    "Functions that take functions: callback contracts, composed transforms, and the Strategy pattern in three lines.",
    17,
    r"""
## Callbacks are contracts

A callback parameter tells callers what shape they may pass, not what will
happen. Design them like any contract:

```csharp
static List<string> TransformAll(
    IEnumerable<string> source,
    Func<string, string> transform)          // ONE contract: string -> string
    => source.Select(transform).ToList();
```

Name the parameter for its role (`transform`, `predicate`, `onComplete`) —
the name is the documentation.

## Pipelines: compose small functions

Delegates compose; small single-purpose transforms chain into behavior:

```csharp
Func<string, string> pipeline = s => s;
pipeline = pipeline.Compose(s => s.Trim())
                   .Compose(s => s.ToLowerInvariant());
```

(Or simply: `source.Select(Trim).Select(Lower)` — LINQ is composition with
deferred execution, which Module 8 exploits fully.)

## Strategy in three lines

Any place you would write `switch (mode)`, consider passing the behavior:

```csharp
static int Reduce(int[] values, int seed, Func<int, int, int> fold) =>
    values.Aggregate(seed, fold);

var sum = Reduce(new[] { 1, 2, 3 }, 0, (a, b) => a + b);
var max = Reduce(new[] { 1, 2, 3 }, int.MinValue, Math.Max);
```

The switch version must change (and be re-tested) for every new mode; the
delegate version accepts new behavior without modification — open/closed in
practice.

## Check your understanding

- When is a switch BETTER than a delegate parameter? (Closed sets with pattern-exhaustiveness needs.)
- What does `Func<A,B>` + `Func<B,C>` compose into? (`Func<A,C>`.)
""",
    "Composition: Callback, Pipeline, Strategy",
    "Hàm nhận hàm: hợp đồng callback, biến đổi ghép, và pattern Strategy trong ba dòng.",
    r"""
## Callback là hợp đồng

Tham số callback cho người gọi biết họ được phép truyền hình dạng nào, không
phải điều gì sẽ xảy ra. Thiết kế chúng như mọi hợp đồng:

```csharp
static List<string> TransformAll(
    IEnumerable<string> source,
    Func<string, string> transform)          // MỘT hợp đồng: string -> string
    => source.Select(transform).ToList();
```

Đặt tên tham số theo vai trò (`transform`, `predicate`, `onComplete`) —
tên là tài liệu.

## Pipeline: ghép các hàm nhỏ

Delegate ghép được; các biến đổi nhỏ một-mục-đích xích thành hành vi:

```csharp
Func<string, string> pipeline = s => s;
pipeline = pipeline.Compose(s => s.Trim())
                   .Compose(s => s.ToLowerInvariant());
```

(Hoặc đơn giản: `source.Select(Trim).Select(Lower)` — LINQ là composition
với thực thi trì hoãn, Module 8 khai thác trọn vẹn.)

## Strategy trong ba dòng

Bất cứ chỗ nào bạn định viết `switch (mode)`, hãy cân nhắc truyền hành vi:

```csharp
static int Reduce(int[] values, int seed, Func<int, int, int> fold) =>
    values.Aggregate(seed, fold);

var sum = Reduce(new[] { 1, 2, 3 }, 0, (a, b) => a + b);
var max = Reduce(new[] { 1, 2, 3 }, int.MinValue, Math.Max);
```

Bản switch phải sửa (và test lại) cho mỗi mode mới; bản delegate nhận hành
vi mới mà không cần sửa — open/closed trên thực tế.

## Kiểm tra hiểu biết

- Khi nào switch TỐT hơn tham số delegate? (Tập đóng cần tính đầy đủ của pattern.)
- `Func<A,B>` + `Func<B,C>` ghép thành gì? (`Func<A,C>`.)
""",
    r"""
## Callback là hợp đồng

Tham số callback cho người gọi biết họ được phép truyền hình dạng nào, không
phải điều gì sẽ xảy ra. Thiết kế chúng như mọi hợp đồng:

```csharp
static List<string> TransformAll(
    IEnumerable<string> source,
    Func<string, string> transform)          // MỘT hợp đồng: string -> string
    => source.Select(transform).ToList();
```

Đặt tên tham số theo vai trò (`transform`, `predicate`, `onComplete`) —
tên là tài liệu.

## Pipeline: ghép các hàm nhỏ

Delegate ghép được; các biến đổi nhỏ một-mục-đích xích thành hành vi:

```csharp
Func<string, string> pipeline = s => s;
pipeline = pipeline.Compose(s => s.Trim())
                   .Compose(s => s.ToLowerInvariant());
```

(Hoặc đơn giản: `source.Select(Trim).Select(Lower)` — LINQ là composition
với thực thi trì hoãn, Module 8 khai thác trọn vẹn.)

## Strategy trong ba dòng

Bất cứ chỗ nào bạn định viết `switch (mode)`, hãy cân nhắc truyền hành vi:

```csharp
static int Reduce(int[] values, int seed, Func<int, int, int> fold) =>
    values.Aggregate(seed, fold);

var sum = Reduce(new[] { 1, 2, 3 }, 0, (a, b) => a + b);
var max = Reduce(new[] { 1, 2, 3 }, int.MinValue, Math.Max);
```

Bản switch phải sửa (và test lại) cho mỗi mode mới; bản delegate nhận hành
vi mới mà không cần sửa — open/closed trên thực tế.

## Kiểm tra hiểu biết

- Khi nào switch TỐT hơn tham số delegate? (Tập đóng cần tính đầy đủ của pattern.)
- `Func<A,B>` + `Func<B,C>` ghép thành gì? (`Func<A,C>`.)
""",
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m3",
    "Checkpoint — Delegates & Capture",
    "Counter factories, capture-debugging, and a callback-driven command router in one graded unit.",
    20,
    r"""
## The gate

Three functions, one graded unit:

1. `MakeAccumulator(int seed)` returns a `Func<int, int>` that adds its
   argument to a private running total (starting at seed) and returns the
   new total. Two accumulators are independent.
2. `SumActions(params Action[] steps)` returns an Action that runs every
   step in order — twice if a step appears twice, skipping nulls safely.
3. `Route(string command, int value)` — a table-driven router over
   registered commands (register via `RegisterCommand(name, Func<int,int>)`);
   unknown command returns -1, known ones apply their function.

Capture semantics decide all three.
""",
    "Checkpoint — Delegate & Capture",
    "Nhà máy bộ đếm, gỡ lỗi capture, và bộ định tuyến lệnh dẫn động callback trong một đơn vị chấm.",
    r"""
## Cổng kiểm tra

Ba hàm, một đơn vị chấm:

1. `MakeAccumulator(int seed)` trả về `Func<int, int>` cộng đối số vào tổng
   chạy riêng (bắt đầu từ seed) và trả về tổng mới. Hai bộ cộng độc lập.
2. `SumActions(params Action[] steps)` trả về Action chạy từng bước theo
   thứ tự — bước lặp lại thì chạy hai lần, bỏ qua null an toàn.
3. `Route(string command, int value)` — bộ định tuyến bảng trên các lệnh đã
   đăng ký (đăng ký qua `RegisterCommand(name, Func<int,int>)`); lệnh lạ trả
   -1, lệnh quen áp dụng hàm của nó.

Ngữ nghĩa capture quyết định cả ba.
""",
    challenge(
        "csi-checkpoint-m3-task",
        "Checkpoint: Capture Mechanics",
        """Implement the three functions described in the checkpoint:

```csharp
static Func<int, int> MakeAccumulator(int seed);
static Action SumActions(params Action?[] steps);
static void RegisterCommand(string name, Func<int, int> fn);
static int Route(string command, int value);
```""",
        CS_PRELUDE,
        [
            (
                "independent accumulators",
                r"""
var acc1 = Solution.MakeAccumulator(100);
var acc2 = Solution.MakeAccumulator(0);
Cj.Eq(acc1(5), 105, "first add to seed");
Cj.Eq(acc1(5), 110, "running total continues");
Cj.Eq(acc2(1), 1, "second accumulator independent");
Cj.Eq(acc2(1), 2, "second accumulator also accumulates");
""",
                "The running total must live in the closure — one variable per MakeAccumulator call.",
            ),
            (
                "null-safe composition",
                r"""
var log = new List<string>();
Action a = () => log.Add("a");
Action b = () => log.Add("b");
Solution.SumActions(a, null, b)();
Cj.Eq(string.Join(",", log), "a,b", "skips null, keeps order");
log.Clear();
Solution.SumActions(a, a)();
Cj.Eq(log.Count, 2, "duplicate step runs twice");
var empty = Solution.SumActions();
Cj.Eq(empty, empty, "empty composition still an Action");
""",
                "foreach over steps, `step?.Invoke()` — order preserved, duplicates natural.",
            ),
            (
                "table router",
                r"""
Solution.RegisterCommand("double", v => v * 2);
Solution.RegisterCommand("neg", v => -v);
Cj.Eq(Solution.Route("double", 21), 42, "registered command applies");
Cj.Eq(Solution.Route("neg", 7), -7, "second command");
Cj.Eq(Solution.Route("missing", 7), -1, "unknown -> -1");
Solution.RegisterCommand("double", v => v * 10);
Cj.Eq(Solution.Route("double", 3), 30, "re-registration replaces");
""",
                "A Dictionary<string, Func<int,int>>: indexer assignment replaces on re-registration.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: Cơ chế Capture",
        "Hiện thực ba hàm mô tả trong checkpoint: bộ cộng đóng kín độc lập, ghép Action an toàn null, và bộ định tuyến bảng thay thế khi đăng ký lại.",
        [
            ("independent accumulators", "Tổng chạy phải sống trong closure — một biến mỗi lần gọi MakeAccumulator."),
            ("null-safe composition", "foreach qua steps, `step?.Invoke()` — thứ tự giữ nguyên, trùng lặp tự nhiên."),
            ("table router", "Dictionary<string, Func<int,int>>: phép gán indexer thay thế khi đăng ký lại."),
        ],
    ),
    solution='public class Solution\n{\n    public static Func<int, int> MakeAccumulator(int seed)\n    {\n        int total = seed;\n        return add => total += add;\n    }\n\n    public static Action SumActions(params Action?[] steps)\n    {\n        return () =>\n        {\n            foreach (Action? step in steps)\n            {\n                step?.Invoke();\n            }\n        };\n    }\n\n    private static readonly Dictionary<string, Func<int, int>> Commands = new();\n\n    public static void RegisterCommand(string name, Func<int, int> fn)\n    {\n        Commands[name] = fn;\n    }\n\n    public static int Route(string command, int value)\n    {\n        return Commands.TryGetValue(command, out Func<int, int>? fn) ? fn(value) : -1;\n    }\n}\n',
    wrong='public class Solution\n{\n    // near-miss: ONE static total shared by all accumulators — the\n    // independence test fails because acc2 keeps counting acc1\'s total\n    private static int _shared;\n\n    public static Func<int, int> MakeAccumulator(int seed)\n    {\n        _shared = seed;\n        return add => _shared += add;\n    }\n\n    public static Action SumActions(params Action?[] steps)\n    {\n        return () =>\n        {\n            foreach (Action? step in steps)\n            {\n                step?.Invoke();\n            }\n        };\n    }\n\n    private static readonly Dictionary<string, Func<int, int>> Commands = new();\n\n    public static void RegisterCommand(string name, Func<int, int> fn)\n    {\n        Commands[name] = fn;\n    }\n\n    public static int Route(string command, int value)\n    {\n        return Commands.TryGetValue(command, out Func<int, int>? fn) ? fn(value) : -1;\n    }\n}\n',
)
print("module 3 authored")
