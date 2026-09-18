"""Module 4 — Delegates, closures, and functional C# (csa-m4)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-delegates-closures",
        "Delegates, Closures, and Functional C#",
        "What a delegate actually is, what lambdas allocate, how closures capture, and when expression trees beat code.",
    )

    csa.register_lesson(
        MID, "csa-m4-delegate-machine", "The delegate machine",
        "Delegate objects, method groups, invocation lists, and what each lambda compiles into.",
        14, "advanced", _m4_delegate_machine, _m4_delegate_machine_vi,
    )
    csa.register_lesson(
        MID, "csa-m4-closures", "Closures and captured variables",
        "Display classes, capture lifetime, the loop-variable fix, and closure allocation costs.",
        15, "advanced", _m4_closures, _m4_closures_vi,
    )
    csa.register_lesson(
        MID, "csa-m4-expr-vs-delegate", "Expression trees vs delegates",
        "Code as data: when to compile to IL, when to inspect, and the cost line between them.",
        15, "advanced", _m4_expr, _m4_expr_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m4", "Checkpoint: delegates and closures",
        "Synthesis: capture semantics and allocation counts under measurement.",
        12, "advanced", _m4_checkpoint, _m4_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m4-task", MID,
        title="Closures checkpoint",
        prompt=(
            "Implement `static List<Func<int>> Counters(int n)` returning n functions; function i returns i-th "
            "value 0,1,...,n-1 — each counter must return ITS OWN index (proving you captured per-iteration "
            "values correctly, not one shared variable). Then implement `static Func<int> Adder(int start)` "
            "returning a function that adds its argument to `start` and returns the RUNNING total (state must "
            "persist across calls — a captured mutable local)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "per-iteration-capture",
                "code": (
                    "var fs = Solution.Counters(3);\n"
                    "Cj.Eq(fs[0](), 0, \"first counter\");\n"
                    "Cj.Eq(fs[1](), 1, \"second counter\");\n"
                    "Cj.Eq(fs[2](), 2, \"third counter\");\n"
                    "Cj.Eq(fs[0](), 0, \"stable across calls\");"
                ),
                "hint": "Capture a per-iteration copy (or the foreach/loop variable under C# 5+ semantics).",
            },
            {
                "name": "persistent-state",
                "code": (
                    "var add = Solution.Adder(10);\n"
                    "Cj.Eq(add(5), 15, \"first call\");\n"
                    "Cj.Eq(add(1), 16, \"state persisted\");\n"
                    "Cj.Eq(add(4), 20, \"still accumulating\");"
                ),
                "hint": "A captured local mutates across invocations — that is the closure's display class field.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static List<Func<int>> Counters(int n)\n    {\n"
            "        var r = new List<Func<int>>();\n"
            "        for (int i = 0; i < n; i++)\n"
            "        {\n"
            "            int copy = i;\n"
            "            r.Add(() => copy);\n"
            "        }\n"
            "        return r;\n"
            "    }\n\n"
            "    public static Func<int> Adder(int start)\n    {\n"
            "        int total = start;\n"
            "        return x => total += x;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static List<Func<int>> Counters(int n)\n    {\n"
            "        var r = new List<Func<int>>();\n"
            "        int shared = 0;                       // one capture for all\n"
            "        for (int i = 0; i < n; i++)\n"
            "        {\n"
            "            r.Add(() => shared);\n"
            "            shared++;\n"
            "        }\n"
            "        return r;\n"
            "    }\n\n"
            "    public static Func<int> Adder(int start) => x => x;   // no state\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p4-delegates", "Delegate drills",
        "Method groups vs lambdas, capture analysis, delegate composition, and a mini rule engine.",
        45, "advanced", "csa-m4-closures",
        ["csa-p4-capture-audit", "csa-p4-composition", "csa-p4-mini-rules"],
    )
    csa.register_challenge(
        "csa-p4-capture-audit", MID,
        title="Capture audit",
        prompt=(
            "Implement `static int TotalCaptured()` that: creates 10 closures over a shared counter local "
            "(all 10 increment the SAME captured int), invokes each once, and returns the counter's final value. "
            "Also implement `static int TotalDistinct()` doing the same but with 10 closures each capturing "
            "their OWN copy; invoke each once and return the sum of the 10 copies (each 1) = 10."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "shared-vs-distinct",
                "code": (
                    "Cj.Eq(Solution.TotalCaptured(), 10, \"shared capture accumulates\");\n"
                    "Cj.Eq(Solution.TotalDistinct(), 10, \"distinct copies sum\");"
                ),
                "hint": "Shared: one display-class field incremented 10 times → 10. Distinct: 10 copies, each incremented once → sum 10.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static int TotalCaptured()\n    {\n"
            "        int shared = 0;\n"
            "        var fs = new List<Func<int>>();\n"
            "        for (int i = 0; i < 10; i++) fs.Add(() => ++shared);\n"
            "        foreach (var f in fs) f();\n"
            "        return shared;\n"
            "    }\n\n"
            "    public static int TotalDistinct()\n    {\n"
            "        int sum = 0;\n"
            "        var fs = new List<Func<int>>();\n"
            "        for (int i = 0; i < 10; i++)\n"
            "        {\n"
            "            int copy = 0;\n"
            "            fs.Add(() => ++copy);\n"
            "        }\n"
            "        foreach (var f in fs) sum += f();\n"
            "        return sum;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static int TotalCaptured()\n    {\n"
            "        int shared = 0;\n"
            "        var fs = new List<Func<int>>();\n"
            "        for (int i = 0; i < 10; i++) fs.Add(() => ++shared);\n"
            "        foreach (var f in fs) f();\n"
            "        return 0;                                  // wrong: ignores result\n"
            "    }\n\n"
            "    public static int TotalDistinct()\n    {\n"
            "        int sum = 0;\n"
            "        var fs = new List<Func<int>>();\n"
            "        int copy = 0;                              // shared, not per-iteration\n"
            "        for (int i = 0; i < 10; i++) fs.Add(() => ++copy);\n"
            "        foreach (var f in fs) sum += f();\n"
            "        return sum;\n"
            "    }\n}"
        ),
        level="guided",
    )
    csa.register_challenge(
        "csa-p4-composition", MID,
        title="Delegate composition pipeline",
        prompt=(
            "Implement `static Func<string, string> Pipeline(params Func<string, string>[] steps)` returning one "
            "delegate applying steps left to right (step 1 first). Also implement `static Func<int> Memoize(Func<int> f)` "
            "— no, simpler: implement `static int InvokeThrice(Func<int> f)` that calls f exactly three times and "
            "returns the last result (tests that delegates are first-class values)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "pipeline-order",
                "code": (
                    "var p = Solution.Pipeline(s => s + \"-1\", s => s + \"-2\");\n"
                    'Cj.Eq(p(\"x\"), \"x-1-2\", \"left to right\");\n'
                    "int calls = 0;\n"
                    "var last = Solution.InvokeThrice(() => ++calls);\n"
                    'Cj.Eq(last, 3, \"third call result\");\n'
                    'Cj.Eq(calls, 3, \"exactly three invocations\");'
                ),
                "hint": "Fold the array: acc = acc + step for each step in order.",
            },
        ],
        reference=(
            "public class Solution\n{\n"
            "    public static Func<string, string> Pipeline(params Func<string, string>[] steps)\n    {\n"
            "        Func<string, string> acc = s => s;\n"
            "        foreach (var step in steps)\n"
            "        {\n"
            "            var current = acc;\n"
            "            acc = s => step(current(s));\n"
            "        }\n"
            "        return acc;\n"
            "    }\n\n"
            "    public static int InvokeThrice(Func<int> f)\n    {\n"
            "        f(); f();\n"
            "        return f();\n"
            "    }\n}"
        ),
        wrong=(
            "public class Solution\n{\n"
            "    public static Func<string, string> Pipeline(params Func<string, string>[] steps)\n    {\n"
            "        Func<string, string> acc = s => s;\n"
            "        foreach (var step in steps)\n"
            "            acc = s => step(acc(s));     // captures acc itself → infinite loop at invoke\n"
            "        return acc;\n"
            "    }\n\n"
            "    public static int InvokeThrice(Func<int> f) => f();   // one call, not three\n}"
        ),
        level="independent",
    )
    csa.register_challenge(
        "csa-p4-mini-rules", MID,
        title="Mini rule engine",
        prompt=(
            "Implement `class RuleEngine` with `private readonly List<(string Name, Func<Dictionary<string,int>, bool>)> _rules = new();`, "
            "`public void Add(string name, Func<Dictionary<string,int>, bool> pred)` and "
            "`public List<string> Evaluate(Dictionary<string,int> ctx)` returning names of all passing rules in "
            "registration order. Prove closure capture over the context is by-reference at evaluation time."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "rules",
                "code": (
                    "var e = new RuleEngine();\n"
                    "e.Add(\"high\", ctx => ctx[\"score\"] > 50);\n"
                    "e.Add(\"even\", ctx => ctx[\"score\"] % 2 == 0);\n"
                    "var ctx = new Dictionary<string, int> { [\"score\"] = 60 };\n"
                    "var r = e.Evaluate(ctx);\n"
                    'Cj.Eq(string.Join(\",\", r), "high,even", "both pass in order");\n'
                    'ctx["score"] = 40;\n'
                    'Cj.Eq(string.Join(",", e.Evaluate(ctx)), "even", "re-evaluated against current ctx");'
                ),
                "hint": "The lambdas capture ctx by reference to the dictionary object; evaluation reads current contents.",
            },
        ],
        reference=(
            "public class RuleEngine\n{\n"
            "    private readonly List<(string Name, Func<Dictionary<string, int>, bool> Pred)> _rules = new();\n\n"
            "    public void Add(string name, Func<Dictionary<string, int>, bool> pred) => _rules.Add((name, pred));\n\n"
            "    public List<string> Evaluate(Dictionary<string, int> ctx)\n"
            "    {\n"
            "        var r = new List<string>();\n"
            "        foreach (var (name, pred) in _rules)\n"
            "            if (pred(ctx)) r.Add(name);\n"
            "        return r;\n"
            "    }\n}\n\n"
            "public class Solution { }"
        ),
        wrong=(
            "public class RuleEngine\n{\n"
            "    private readonly List<(string Name, Func<Dictionary<string, int>, bool> Pred)> _rules = new();\n\n"
            "    public void Add(string name, Func<Dictionary<string, int>, bool> pred) => _rules.Add((name, pred));\n\n"
            "    public List<string> Evaluate(Dictionary<string, int> ctx)\n"
            "    {\n"
            "        var r = new List<string>();\n"
            "        foreach (var (name, pred) in _rules)\n"
            "            if (pred(ctx)) r.Add(name);\n"
            "        return r;\n"
            "    }\n}\n\n"
            "public class Solution\n{\n"
            "    public static string F() => RuleEngine.Hello();   // compile error: member does not exist\n}"
        ),
        level="mini-build",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m4_delegate_machine = r"""## The delegate machine

A delegate is an object: it holds a **method** (or, for virtual/interface
calls, a function pointer plus the receiver object) and an optional
**invocation list**. `Foo` as an expression ("method group") converts to a
delegate instance; a lambda compiles to a compiler-generated method wrapped
in a delegate:

```csharp
Func<int, int> f = x => x + 1;   // compiler generates: static int <>M0(int x)
Func<int, int> g = doubleIt;     // method group → existing method, no new code
Func<int, int> h = f + g;        // MulticastDelegate: invocation list [f, g]
```

Allocation profile you can predict:

| Construct | Compiles to | Allocates |
|---|---|---|
| static lambda, no capture | static method + delegate | 1 delegate |
| lambda capturing a local | display class + method + delegate | 1 class + 1 delegate |
| method group (instance) | delegate to that instance's method | 1 delegate |
| `static` lambda modifier | guarantees no capture | 1 delegate |

The `static` lambda modifier is a *contract*: `static x => x + 1` refuses to
compile if it captures anything — a cheap way to make "no hidden closure"
an enforced property, not a code-review promise.

Invocation order in a multicast delegate is defined (first added first
invoked); the return value you keep is the LAST handler's. Caching delegate
instances (`static readonly Func<...>`) avoids re-allocating per call —
this is the single biggest avoidable allocation in lambda-heavy code.
"""

_m4_delegate_machine_vi = r"""## Máy delegate

Delegate là một object: nó giữ một **phương thức** (hoặc, với gọi
virtual/interface, con trỏ hàm cộng object receiver) và một **invocation
list** tùy chọn. `Foo` như một biểu thức ("method group") chuyển đổi thành
thể hiện delegate; lambda biên dịch thành phương thức do compiler sinh ra,
được bọc trong delegate:

```csharp
Func<int, int> f = x => x + 1;   // compiler sinh: static int <>M0(int x)
Func<int, int> g = doubleIt;     // method group → phương thức có sẵn, không sinh mã mới
Func<int, int> h = f + g;        // MulticastDelegate: invocation list [f, g]
```

Hồ sơ cấp phát bạn dự đoán được:

| Cấu trúc | Biên dịch thành | Cấp phát |
|---|---|---|
| lambda tĩnh, không capture | phương thức tĩnh + delegate | 1 delegate |
| lambda bắt biến cục bộ | display class + phương thức + delegate | 1 class + 1 delegate |
| method group (thể hiện) | delegate tới phương thức của thể hiện đó | 1 delegate |
| bổ từ `static` lambda | cam kết không capture | 1 delegate |

Bổ từ `static` cho lambda là một *hợp đồng*: `static x => x + 1` từ chối
biên dịch nếu nó capture bất cứ thứ gì — cách rẻ để biến "không closure ẩn"
thành thuộc tính bị kiểm tra, không phải lời hứa trong code review.

Thứ tự gọi trong multicast delegate được định nghĩa (thêm trước gọi trước);
giá trị trả về bạn giữ lại là của handler CUỐI. Cache thể hiện delegate
(`static readonly Func<...>`) tránh cấp phát lại mỗi lần gọi — đây là cấp
phát tránh được lớn nhất trong code nhiều lambda.
"""

_m4_closures = r"""## Closures and captured variables

When a lambda captures a local, the compiler hoists that local into a
compiler-generated **display class**; both the method and the lambda share
one instance. Consequences that decide bugs:

```csharp
var actions = new List<Action>();
for (int i = 0; i < 3; i++)
    actions.Add(() => Console.Write(i));
// C# 5+: prints 012 — foreach loops capture per-iteration
// but `for` loop variables are ONE variable shared by all iterations
```

Since C# 5, `foreach` iteration variables are captured per-iteration (the
historical footgun is fixed there); a `for` loop's index is still a single
variable — every closure sees its final value unless you copy it into a
local inside the loop.

Captured variables live as long as the delegate: a lambda holding a large
object keeps the whole object reachable — this is the **managed memory
leak** shape in event-handler code (Module 14). Capture deliberately:

```csharp
// capture a snapshot, not the variable:
for (int i = 0; i < 3; i++)
{
    var copy = i;
    actions.Add(() => Use(copy));   // 0, 1, 2
}
```

And prefer capturing *small, long-lived* things (a service, a formatter)
over loop locals. Each capture that differs per iteration is one display
class allocation — for hot paths, restructure so one closure serves many
calls (parameterize instead of capturing).
"""

_m4_closures_vi = r"""## Closure và biến bị bắt giữ

Khi lambda bắt một biến cục bộ, compiler nâng biến đó vào một **display
class** do compiler sinh ra; phương thức và lambda dùng chung một thể hiện.
Những hệ quả quyết định bug:

```csharp
var actions = new List<Action>();
for (int i = 0; i < 3; i++)
    actions.Add(() => Console.Write(i));
// C# 5+: in 012 — vòng foreach capture theo từng lần lặp
// nhưng biến đếm của vòng `for` là MỘT biến dùng chung mọi lần lặp
```

Từ C# 5, biến lặp của `foreach` được capture theo từng lần lặp (cái bẫy
lịch sử đã được sửa ở đó); chỉ số của vòng `for` vẫn là một biến duy nhất —
mọi closure thấy giá trị cuối cùng của nó, trừ khi bạn sao chép vào biến
cục bộ bên trong vòng lặp.

Biến bị capture sống cùng delegate: một lambda giữ object lớn giữ cho cả
object đó luôn truy cập được — đây chính là dáng vẻ **rò rỉ bộ nhớ managed**
trong code event-handler (Module 14). Hãy capture có chủ đích:

```csharp
// capture bản chụp, không phải biến:
for (int i = 0; i < 3; i++)
{
    var copy = i;
    actions.Add(() => Use(copy));   // 0, 1, 2
}
```

Và ưu tiên capture những thứ *nhỏ, sống lâu* (một service, một formatter)
hơn biến cục bộ trong vòng lặp. Mỗi capture khác nhau theo lần lặp là một
cấp phát display class — với đường nóng, tái cấu trúc để một closure phục
vụ nhiều lần gọi (tham số hóa thay vì capture).
"""

_m4_expr = r"""## Expression trees vs delegates

`Expression<Func<T,bool>>` is code as *data*: a tree of nodes you can
inspect, transform, print, or compile. A `Func<T,bool>` is code as *code*:
opaque, fast to invoke.

```csharp
Expression<Func<int, bool>> e = x => x > 5;
var body = (BinaryExpression)e.Body;      // node inspection
Console.WriteLine(body.NodeType);         // GreaterThan

var f = e.Compile();                      // → IL via Lightweight Code Generation
f(7);                                     // true — and now it runs fast
```

Decide by use, not by fashion:

| Need | Choose |
|---|---|
| call it many times, never look inside | delegate |
| translate it (EF, LINQ providers, rules → SQL) | expression tree |
| build rules from configuration at runtime | build Expression, Compile once |
| hot path called in a tight loop | delegate (or compile the tree ONCE, cache it) |

Costs: building trees allocates node objects; `Compile()` is expensive —
do it once per rule, not per item. Expression trees cannot contain async,
null-coalescing assignment, or `??=` — they model expression logic, not
statements; when rules need statements, either restructure to expressions
or generate code another way (source generators, Module 8).

The classic production bug: storing `Expression<Func<...>>` and invoking it
directly (it's not a delegate), or compiling per call and wondering why the
"fast" rule engine is slow. Both are one-line fixes once you can *see* the
difference between the two types.
"""

_m4_expr_vi = r"""## Expression tree vs delegate

`Expression<Func<T,bool>>` là mã dưới dạng *dữ liệu*: một cây node bạn có
thể kiểm tra, biến đổi, in ra, hoặc biên dịch. `Func<T,bool>` là mã dưới
dạng *mã*: mờ đục, gọi nhanh.

```csharp
Expression<Func<int, bool>> e = x => x > 5;
var body = (BinaryExpression)e.Body;      // soi node
Console.WriteLine(body.NodeType);         // GreaterThan

var f = e.Compile();                      // → IL qua Lightweight Code Generation
f(7);                                     // true — và giờ nó chạy nhanh
```

Chọn theo nhu cầu, không theo mốt:

| Nhu cầu | Chọn |
|---|---|
| gọi nhiều lần, không cần nhìn vào trong | delegate |
| dịch nó (EF, LINQ provider, rule → SQL) | expression tree |
| dựng rule từ cấu hình lúc chạy | dựng Expression, Compile MỘT lần |
| đường nóng gọi trong vòng kín | delegate (hoặc compile cây MỘT lần rồi cache) |

Chi phí: dựng cây cấp phát node; `Compile()` đắt — làm một lần mỗi rule,
không phải mỗi phần tử. Expression tree không chứa được async, gán
null-coalescing, hay `??=` — nó mô hình hóa logic biểu thức, không phải
câu lệnh; khi rule cần câu lệnh, hoặc tái cấu trúc thành biểu thức, hoặc
sinh mã bằng cách khác (source generator, Module 8).

Bug production kinh điển: lưu `Expression<Func<...>>` rồi gọi trực tiếp
(nó không phải delegate), hoặc compile mỗi lần gọi rồi thắc mắc sao "rule
engine nhanh" mà chậm. Cả hai đều sửa một dòng khi bạn *nhìn thấy* khác biệt
giữa hai kiểu này.
"""

_m4_checkpoint = r"""## Checkpoint: delegates and closures

Two behaviors prove capture semantics:

1. **Per-iteration capture** — n counters each remember their own index.
2. **Persistent state** — one captured mutable local accumulates across
   calls, exactly the display-class field the compiler created.

Both together mean you can now *read* lambda code and predict its
allocation and behavior before running it — the skill the practice set
drills next.
"""

_m4_checkpoint_vi = r"""## Checkpoint: delegate và closure

Hai hành vi chứng minh ngữ nghĩa capture:

1. **Capture theo từng lần lặp** — n counter mỗi cái nhớ chỉ số của mình.
2. **Trạng thái bền** — một biến cục bộ khả biến bị capture cộng dồn qua
   các lần gọi, đúng trường display class mà compiler đã tạo.

Cả hai cùng nghĩa là bạn giờ *đọc được* code lambda và dự đoán cấp phát và
hành vi trước khi chạy — kỹ năng mà practice set sắp luyện tiếp.
"""
