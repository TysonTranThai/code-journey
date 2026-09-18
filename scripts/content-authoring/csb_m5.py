#!/usr/bin/env python3
"""C# — Beginner — Module 5: csb-methods.

Methods as named, testable computation: declaration and expression bodies,
optional/named parameters and overloading, then scope and decomposition.
House conventions: ISO boilerplate carries usings, Ws are behavioral
near-misses (a missing guard, a precedence slip, an off-by-one).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-methods"

write_module(
    M,
    "Methods",
    "Name a computation once, call it everywhere: declarations, parameters, overloads, and the discipline of small methods.",
    "Phương thức",
    "Đặt tên cho một phép tính một lần, gọi ở mọi nơi: khai báo, tham số, overload, và kỷ luật phương thức nhỏ.",
    ["csb-m5-declare", "csb-m5-params", "csb-m5-scope", "csb-checkpoint-m5"],
    ["csb-p5-methods"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m5-declare",
    "Declaring methods",
    "The anatomy of a method: parameters, return types, void, and expression-bodied shorthand.",
    14,
    r"""
## A method is a named computation

```csharp
static double Total(double price, int quantity)
{
    return price * quantity;
}
```

Read the pieces: `static` (belongs to the type, not an object — you've called `Console.WriteLine` the same way), `double` (the **return type** — what comes back), `Total` (the name — a verb phrase is the convention), and the **parameter list** `(double price, int quantity)` — named inputs the body may use like local variables.

`return` hands back the value and exits immediately — code after a `return` in the same path never runs. A method whose return type is not `void` must return on *every* path; the compiler enforces this ("not all code paths return a value").

## void: action, not answer

```csharp
static void Greet(string name)
{
    Console.WriteLine("Hello, " + name + "!");
}
```

`void` means "I produce no value — I do something." Calling a `void` method as a statement is fine; calling a value-returning method and ignoring the result is legal but usually a smell. Don't fake returns: `Greet` returning nothing is honest; returning `true` "because it worked" is not.

## Expression-bodied members

```csharp
static int Square(int x) => x * x;
static bool IsAdult(int age) => age >= 18;
```

When the body is one expression, `=> expression` replaces the braces and the `return`. Same semantics, less ceremony. Rule of thumb: if it reads like a formula, use the expression body; if it needs steps or conditionals with side effects, use a block.

## Why methods at all

Three reasons, in order of importance: a **name** documents intent (`Total(price, qty)` beats an unexplained `price * qty`); **reuse** means the formula lives in exactly one place — fix the bug once; **testability** means a method with inputs and an output can be graded by code — exactly what every challenge in this course does.
""",
    "Khai báo phương thức",
    "Giải phẫu một phương thức: tham số, kiểu trả về, void, và cách viết gọn bằng expression body.",
    r"""
## Phương thức là một phép tính có tên

```csharp
static double Total(double price, int quantity)
{
    return price * quantity;
}
```

Đọc từng phần: `static` (thuộc về kiểu, không phải một đối tượng — bạn đã gọi `Console.WriteLine` theo cùng cách), `double` (**kiểu trả về** — cái được trả lại), `Total` (tên — theo thông lệ là một cụm động từ), và **danh sách tham số** `(double price, int quantity)` — các đầu vào được đặt tên mà thân hàm dùng như biến cục bộ.

`return` trả giá trị về và thoát ngay — mã phía sau một `return` trên cùng nhánh thực thi sẽ không bao giờ chạy. Phương thức có kiểu trả về khác `void` phải `return` trên *mọi* nhánh; trình biên dịch bắt buộc điều này ("not all code paths return a value").

## void: hành động, không phải câu trả lời

```csharp
static void Greet(string name)
{
    Console.WriteLine("Hello, " + name + "!");
}
```

`void` nghĩa là "tôi không tạo ra giá trị — tôi làm một việc nào đó." Gọi phương thức `void` như một câu lệnh là bình thường; gọi phương thức có giá trị trả về rồi bỏ qua kết quả là hợp lệ nhưng thường là mùi code. Đừng giả trả về: `Greet` không trả gì là trung thực; trả `true` "vì nó chạy rồi" thì không.

## Expression-bodied members

```csharp
static int Square(int x) => x * x;
static bool IsAdult(int age) => age >= 18;
```

Khi thân chỉ là một biểu thức, `=> biểu_thức` thay cho ngoặc nhọn và `return`. Cùng ngữ nghĩa, ít ceremony hơn. Quy tắc: nếu nó đọc như một công thức, dùng expression body; nếu cần nhiều bước hoặc rẽ nhánh kèm tác dụng phụ, dùng khối lệnh.

## Tại sao cần phương thức

Ba lý do, theo thứ tự quan trọng: một **tên** ghi lại ý định (`Total(price, qty)` rõ hơn một phép `price * qty` không giải thích); **tái sử dụng** nghĩa là công thức chỉ tồn tại đúng một nơi — sửa lỗi một lần; **khả năng kiểm thử** — phương thức có đầu vào và đầu ra có thể được chấm điểm bằng code, đúng như mọi thử thách trong khóa học này.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m5-params",
    "Parameters: optional, named, overloaded",
    "Defaults callers can skip, named arguments for clarity, and overloads that adapt one name to several shapes.",
    12,
    r"""
## Optional parameters

```csharp
static void Log(string message, int level = 1)
{
    Console.WriteLine("[" + level + "] " + message);
}

Log("boot");          // [1] boot   — level omitted, default used
Log("disk full", 3);  // [3] disk full
```

A default value makes the trailing parameter skippable. Rules: optional parameters come **after** required ones, and the default must be a compile-time constant. Defaults are baked into the *caller's* compiled code — changing a default later requires recompiling callers. That's a real library-design consequence; for now, just know defaults are convenient for self-contained code.

## Named arguments

```csharp
Log(level: 3, message: "disk full");   // same call, order-free
Log("disk full", level: 3);            // positional then named
```

Named arguments say what each value *is* at the call site. They also let you skip middle optional parameters instead of passing them all positionally. Use them when a call would otherwise carry bare numbers or bools whose meaning isn't obvious at a glance: `Resize(img, width: 800)` beats `Resize(img, 800)`.

## Overloading: one name, several signatures

```csharp
static int    Max(int a, int b)         => a > b ? a : b;
static double Max(double a, double b)  => a > b ? a : b;
static int    Max(int[] values)         { /* scan */ }
```

Three methods, one concept, one name. The compiler picks the overload whose **parameter types** match the arguments (or the best implicit conversion). Overloads must differ in their parameter lists — a different return type alone is a compile error (`CS0111`). Overload when the *concept* is identical and only the input shape differs; if the behavior meaningfully changes, a distinct name is more honest.
""",
    "Tham số: tùy chọn, named, overloading",
    "Giá trị mặc định giúp người gọi bỏ qua, named argument giúp rõ ràng, và overload cho một cái tên nhiều hình dạng.",
    r"""
## Tham số tùy chọn

```csharp
static void Log(string message, int level = 1)
{
    Console.WriteLine("[" + level + "] " + message);
}

Log("boot");          // [1] boot   — bỏ qua level, dùng mặc định
Log("disk full", 3);  // [3] disk full
```

Giá trị mặc định làm tham số cuối trở thành tùy chọn. Quy tắc: tham số tùy chọn đứng **sau** tham số bắt buộc, và mặc định phải là hằng số biên dịch được. Mặc định được nướng vào mã đã biên dịch của *người gọi* — đổi mặc định sau này buộc biên dịch lại nơi gọi. Đó là hệ quả thật khi thiết kế thư viện; còn bây giờ, chỉ cần biết mặc định tiện cho code tự chứa.

## Named arguments

```csharp
Log(level: 3, message: "disk full");   // cùng một lời gọi, không cần thứ tự
Log("disk full", level: 3);            // vị trí rồi named
```

Named argument nói rõ mỗi giá trị *là gì* ngay tại lời gọi. Chúng cũng cho phép bỏ qua tham số tùy chọn ở giữa mà không phải truyền hết theo vị trí. Dùng khi lời gọi có số hoặc bool trần mà ý nghĩa không rõ: `Resize(img, width: 800)` rõ hơn `Resize(img, 800)`.

## Overloading: một tên, nhiều chữ ký

```csharp
static int    Max(int a, int b)         => a > b ? a : b;
static double Max(double a, double b)  => a > b ? a : b;
static int    Max(int[] values)         { /* duyệt mảng */ }
```

Ba phương thức, một khái niệm, một tên. Trình biên dịch chọn overload khớp **kiểu tham số** với đối số (hoặc chuyển đổi ngầm tốt nhất). Các overload phải khác danh sách tham số — chỉ khác kiểu trả về là lỗi biên dịch (`CS0111`). Overload khi *khái niệm* giống hệt và chỉ khác hình dạng đầu vào; nếu hành vi đổi thực sự, một tên riêng sẽ trung thực hơn.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m5-scope",
    "Scope and decomposition",
    "Where variables live and die, and how to carve a big program into methods that each do one thing.",
    13,
    r"""
## Scope: where a name exists

A local variable exists from its declaration to the closing brace of its block:

```csharp
static double Tip(double bill)
{
    double rate = 0.15;          // born here
    double tip = bill * rate;    // can see rate
    return tip;
}                                // rate and tip are gone
```

Two blocks may each declare their own `rate`; they are unrelated variables. A parameter is also a local — redeclaring `double bill` inside `Tip` is an error (`CS0136`). One warning: a method can *read* fields of its class, so a local that silently shadows a field name is a classic confusion source — keep local names distinct.

## Refactor: from wall-of-Main to named steps

```csharp
// before: 40 lines of Main doing everything
// after:
static void Main()
{
    var items = ReadItems();
    var total = TotalWithTax(items);
    PrintReceipt(items, total);
}
```

Main becomes a table of contents. Each helper does **one thing**, and its name tells you what without reading the body. Signals it's time to extract a method: a comment you wrote to explain a block (the block wants to be a named method); the same three lines appearing twice; a nesting level deeper than about three.

## Return early, guard first

```csharp
static double Price(int qty, double unit)
{
    if (qty <= 0) return 0;              // guard clause
    if (unit < 0) throw new ArgumentException("negative unit price");
    return qty * unit;                   // the real logic, unindented
}
```

Handling the unusual cases first and returning (or throwing) keeps the main logic flat. Compare with nesting the happy path inside `if (qty > 0) { if (unit >= 0) { ... } }` — same result, one extra indent per worry. Preconditions at the top also document the contract: this method expects non-negative quantities, and says so in code.
""",
    "Phạm vi và phân rã",
    "Biến tồn tại ở đâu và biến mất khi nào, và cách chẻ một chương trình lớn thành các phương thức mỗi cái làm một việc.",
    r"""
## Phạm vi: một cái tên tồn tại ở đâu

Biến cục bộ tồn tại từ dòng khai báo đến ngoặc nhọn đóng của khối chứa nó:

```csharp
static double Tip(double bill)
{
    double rate = 0.15;          // sinh ra ở đây
    double tip = bill * rate;    // nhìn thấy rate
    return tip;
}                                // rate và tip đã biến mất
```

Hai khối có thể mỗi bên tự khai báo `rate` riêng; đó là hai biến không liên quan. Tham số cũng là biến cục bộ — khai báo lại `double bill` bên trong `Tip` là lỗi (`CS0136`). Một cảnh báo: phương thức có thể *đọc* field của lớp nó thuộc về, nên biến cục bộ trùng tên field một cách âm thầm là nguồn nhầm lặp kinh điển — giữ tên cục bộ khác biệt.

## Refactor: từ bức tường Main thành các bước có tên

```csharp
// trước: 40 dòng Main làm mọi thứ
// sau:
static void Main()
{
    var items = ReadItems();
    var total = TotalWithTax(items);
    PrintReceipt(items, total);
}
```

Main trở thành mục lục. Mỗi hàm phụ làm **một việc**, và tên của nó cho biết việc gì mà không cần đọc thân. Tín hiệu đến lúc tách phương thức: một comment bạn viết để giải thích một khối (khối đó muốn thành phương thức có tên); cùng ba dòng xuất hiện hai lần; mức lồng sâu hơn ba.

## Return sớm, bảo vệ trước

```csharp
static double Price(int qty, double unit)
{
    if (qty <= 0) return 0;              // guard clause
    if (unit < 0) throw new ArgumentException("negative unit price");
    return qty * unit;                   // logic chính, không thụt lề
}
```

Xử lý các trường hợp lạ trước rồi return (hoặc throw) giữ logic chính phẳng. So với việc lồng đường vui bên trong `if (qty > 0) { if (unit >= 0) { ... } }` — cùng kết quả, thêm một mức thụt lề cho mỗi nỗi lo. Điều kiện tiên quyết ở đầu còn ghi lại hợp đồng: phương thức này mong đợi số lượng không âm, và nó nói điều đó bằng code.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p5-methods",
    "Method workshop",
    "Formulas as expression bodies, guards as method contracts, overloads for two shapes of the same question.",
    "Xưởng phương thức",
    "Công thức thành expression body, guard làm hợp đồng của phương thức, overload cho hai hình dạng của cùng một câu hỏi.",
    "csb-m5-scope",
    35,
    "beginner",
    [
        challenge(
            "csb-p5-convert",
            "Temperature pair",
            "Implement `static double CtoF(double c)` (multiply by 9/5, add 32) and `static double FtoC(double f)` (subtract 32, multiply by 5/9). Watch the parentheses — the subtraction must happen before the scaling in one direction and after it in the other.",
            CS_PRELUDE,
            [
                (
                    "boiling",
                    "Cj.Near(Solution.CtoF(100), 212, 1e-9, \"CtoF(100)\");\nCj.Near(Solution.FtoC(212), 100, 1e-9, \"FtoC(212)\");",
                    "The two fixed points of the scale.",
                ),
                (
                    "freezing-and-roundtrip",
                    "Cj.Near(Solution.CtoF(0), 32, 1e-9, \"CtoF(0)\");\nCj.Near(Solution.FtoC(32), 0, 1e-9, \"FtoC(32)\");\nCj.Near(Solution.FtoC(Solution.CtoF(37.5)), 37.5, 1e-9, \"roundtrip\");",
                    "Freezing point both ways, then FtoC(CtoF(x)) must land back on x.",
                ),
            ],
            level="imitation",
        ),
        challenge(
            "csb-p5-clamp",
            "Clamp to a range",
            "Implement `static int Clamp(int value, int min, int max)` — return `value` when it lies within [min, max], otherwise the boundary it crossed. Both boundaries must be enforced.",
            CS_PRELUDE,
            [
                (
                    "inside",
                    "Cj.Eq(Solution.Clamp(5, 0, 10), 5, \"in-range\");\nCj.Eq(Solution.Clamp(0, 0, 10), 0, \"at-min\");\nCj.Eq(Solution.Clamp(10, 0, 10), 10, \"at-max\");",
                    "In-range values and both inclusive boundaries pass through unchanged.",
                ),
                (
                    "both-sides",
                    "Cj.Eq(Solution.Clamp(-7, 0, 10), 0, \"below\");\nCj.Eq(Solution.Clamp(50, 0, 10), 10, \"above\");",
                    "Crossing the floor returns min; crossing the ceiling returns max — the top guard is just as real as the bottom one.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p5-repeat",
            "Repeat a string",
            "Implement `static string Repeat(string s, int times)` — s concatenated `times` times. `Repeat(\"ab\", 3)` is `\"ababab\"`; `times` of 0 (or negative) yields `\"\"`. Null input yields `\"\"` too.",
            CS_PRELUDE,
            [
                (
                    "basic",
                    "Cj.Eq(Solution.Repeat(\"ab\", 3), \"ababab\", \"ab x3\");\nCj.Eq(Solution.Repeat(\"x\", 1), \"x\", \"once\");",
                    "Exact count — count the copies, not the iterations.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.Repeat(\"hi\", 0), \"\", \"zero\");\nCj.Eq(Solution.Repeat(\"hi\", -2), \"\", \"negative\");\nCj.Eq(Solution.Repeat(null, 3), \"\", \"null\");",
                    "Zero, negative, and null all produce the empty string — no exception.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p5-max-overloads",
            "Max, two shapes",
            "Implement two overloads: `static int Max(int a, int b)` and `static int Max(int[] values)`. The array version returns the largest element and **throws `ArgumentException`** for null or empty input — never a fake sentinel value.",
            CS_PRELUDE,
            [
                (
                    "scalar",
                    "Cj.Eq(Solution.Max(3, 9), 9, \"3,9\");\nCj.Eq(Solution.Max(-4, -9), -4, \"negatives\");\nCj.Eq(Solution.Max(7, 7), 7, \"equal\");",
                    "Larger wins; equal arguments return that value.",
                ),
                (
                    "array",
                    "Cj.Eq(Solution.Max(new[] {3, 1, 4, 1, 5}), 5, \"scan\");\nCj.Eq(Solution.Max(new[] {-8, -3, -5}), -3, \"all-negative\");\nCj.Eq(Solution.Max(new[] {42}), 42, \"single\");",
                    "Scan every element; negatives must not trip an initial-maximum bug.",
                ),
                (
                    "empty-throws",
                    "bool threw = false;\ntry { Solution.Max(new int[0]); } catch (ArgumentException) { threw = true; }\nCj.True(threw, \"empty throws\");\nthrew = false;\ntry { Solution.Max(null); } catch (ArgumentException) { threw = true; }\nCj.True(threw, \"null throws\");",
                    "No data is not a data problem you can guess around — it's a contract violation. Throw.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p5-convert": vi_challenge(
            "Cặp chuyển đổi nhiệt độ",
            "Hiện thực `static double CtoF(double c)` (nhân 9/5, cộng 32) và `static double FtoC(double f)` (trừ 32, nhân 5/9). Chú ý ngoặc — phép trừ phải xảy ra trước khi nhân ở một chiều và sau ở chiều kia.",
            [
                ("boiling", "Hai điểm cố định của thang đo."),
                ("freezing-and-roundtrip", "Điểm đóng băng cả hai chiều, rồi FtoC(CtoF(x)) phải quay về x."),
            ],
        ),
        "csb-p5-clamp": vi_challenge(
            "Kẹp vào khoảng",
            "Hiện thực `static int Clamp(int value, int min, int max)` — trả `value` khi nằm trong [min, max], ngược lại trả biên mà nó vượt. Cả hai biên đều phải được thực thi.",
            [
                ("inside", "Giá trị trong khoảng và cả hai biên bao gồm đi qua không đổi."),
                ("both-sides", "Vượt sàn trả min; vượt trần trả max — guard trên cũng thật như guard dưới."),
            ],
        ),
        "csb-p5-repeat": vi_challenge(
            "Lặp chuỗi",
            "Hiện thực `static string Repeat(string s, int times)` — s nối liền `times` lần. `Repeat(\"ab\", 3)` là `\"ababab\"`; `times` bằng 0 (hoặc âm) cho `\"\"`. Input null cũng cho `\"\"`.",
            [
                ("basic", "Đếm chính xác số bản sao, không phải số vòng lặp."),
                ("edges", "Zero, âm, và null đều cho chuỗi rỗng — không ném exception."),
            ],
        ),
        "csb-p5-max-overloads": vi_challenge(
            "Max, hai hình dạng",
            "Hiện thực hai overload: `static int Max(int a, int b)` và `static int Max(int[] values)`. Bản mảng trả phần tử lớn nhất và **ném `ArgumentException`** khi input null hoặc rỗng — không bao giờ trả giá trị giả.",
            [
                ("scalar", "Số lớn thắng; hai đối số bằng nhau trả chính nó."),
                ("array", "Duyệt mọi phần tử; số âm không được làm hỏng giá trị lớn nhất ban đầu."),
                ("empty-throws", "Không có dữ liệu không phải chuyện có thể đoán bừa — đó là vi phạm hợp đồng. Hãy ném."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p5-convert",
            'public class Solution\n{\n    public static double CtoF(double c) => c * 9.0 / 5.0 + 32;\n    public static double FtoC(double f) => (f - 32) * 5.0 / 9.0;\n}\n',
            'public class Solution\n{\n    public static double CtoF(double c) => c * 9.0 / 5.0 + 32;\n    // near-miss: missing parentheses — * binds tighter than -, so this\n    // computes f - (32 * 5 / 9) = f - 17.78 instead of (f - 32) * 5/9\n    public static double FtoC(double f) => f - 32 * 5.0 / 9.0;\n}\n',
        ),
        (
            "csb-p5-clamp",
            'public class Solution\n{\n    public static int Clamp(int value, int min, int max)\n    {\n        if (value < min) return min;\n        if (value > max) return max;\n        return value;\n    }\n}\n',
            'public class Solution\n{\n    public static int Clamp(int value, int min, int max)\n    {\n        if (value < min) return min;\n        // near-miss: the upper guard was never written — values above max\n        // pass through untouched\n        return value;\n    }\n}\n',
        ),
        (
            "csb-p5-repeat",
            'public class Solution\n{\n    public static string Repeat(string s, int times)\n    {\n        if (string.IsNullOrEmpty(s) || times <= 0) return "";\n        var sb = new System.Text.StringBuilder();\n        for (int i = 0; i < times; i++) sb.Append(s);\n        return sb.ToString();\n    }\n}\n',
            'public class Solution\n{\n    public static string Repeat(string s, int times)\n    {\n        if (string.IsNullOrEmpty(s) || times <= 0) return "";\n        var sb = new System.Text.StringBuilder();\n        // near-miss: <= — one copy too many for every positive count\n        for (int i = 0; i <= times; i++) sb.Append(s);\n        return sb.ToString();\n    }\n}\n',
        ),
        (
            "csb-p5-max-overloads",
            'public class Solution\n{\n    public static int Max(int a, int b) => a > b ? a : b;\n\n    public static int Max(int[] values)\n    {\n        if (values == null || values.Length == 0)\n            throw new ArgumentException("no elements");\n        int best = values[0];\n        for (int i = 1; i < values.Length; i++)\n            if (values[i] > best) best = values[i];\n        return best;\n    }\n}\n',
            'public class Solution\n{\n    public static int Max(int a, int b) => a > b ? a : b;\n\n    public static int Max(int[] values)\n    {\n        if (values == null || values.Length == 0)\n        {\n            // near-miss: returns a sentinel instead of throwing — the caller\n            // cannot tell "empty" from "the max really is int.MinValue"\n            return int.MinValue;\n        }\n        int best = values[0];\n        for (int i = 1; i < values.Length; i++)\n            if (values[i] > best) best = values[i];\n        return best;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m5",
    "Checkpoint — Methods",
    "Dispatch, contracts, and counting — two methods, both tested on their edges.",
    20,
    r"""
## Checkpoint: the operator console

**Task:** implement two methods:

1. `static double Apply(char op, double a, double b)` — `+`, `-`, `*` behave as usual; `/` divides but **throws `DivideByZeroException`** when `b` is exactly 0 (remember: doubles don't throw on their own — `1.0 / 0.0` is `Infinity`, so you must check); any other character throws `ArgumentException`.
2. `static int CountVowels(string s)` — count of vowels `aeiou`, case-insensitive; null or empty input counts 0.
""",
    "Checkpoint — Phương thức",
    "Điều hướng, hợp đồng, và đếm — hai phương thức, đều bị test ở các biên.",
    r"""
## Checkpoint: bàn điều khiển toán tử

**Nhiệm vụ:** hiện thực hai phương thức:

1. `static double Apply(char op, double a, double b)` — `+`, `-`, `*` như thường lệ; `/` chia nhưng **ném `DivideByZeroException`** khi `b` đúng bằng 0 (nhớ: double không tự ném — `1.0 / 0.0` là `Infinity`, nên bạn phải tự kiểm tra); ký tự khác bất kỳ ném `ArgumentException`.
2. `static int CountVowels(string s)` — số nguyên âm `aeiou`, không phân biệt hoa thường; input null hoặc rỗng đếm 0.
""",
    challenge(
        "csb-checkpoint-m5-task",
        "Operator console",
        "Implement `Apply` and `CountVowels` as described. `Apply('/')` with a zero divisor must throw `DivideByZeroException`; an unknown operator must throw `ArgumentException`.",
        CS_PRELUDE,
        [
            (
                "apply",
                'Cj.Eq(Solution.Apply(\'+\', 2, 3), 5, "add");\nCj.Eq(Solution.Apply(\'*\', 4, 2.5), 10, "mul");\nbool div0 = false;\ntry { Solution.Apply(\'/\', 1, 0); } catch (DivideByZeroException) { div0 = true; }\nCj.True(div0, "zero divisor throws");\nbool badOp = false;\ntry { Solution.Apply(\'%\', 1, 2); } catch (ArgumentException) { badOp = true; }\nCj.True(badOp, "unknown op throws");',
                "Two happy paths, then both failure contracts: zero divisor and unknown operator.",
            ),
            (
                "vowels",
                'Cj.Eq(Solution.CountVowels("Hello World"), 3, "mixed case");\nCj.Eq(Solution.CountVowels("AEIOU"), 5, "uppercase");\nCj.Eq(Solution.CountVowels("xyz"), 0, "none");\nCj.Eq(Solution.CountVowels(""), 0, "empty");\nCj.Eq(Solution.CountVowels(null), 0, "null");',
                "Case-insensitivity is the trap: uppercase vowels count too.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Bàn điều khiển toán tử",
        "Hiện thực `Apply` và `CountVowels` như mô tả. `Apply(\'/\')` với số chia bằng 0 phải ném `DivideByZeroException`; toán tử lạ phải ném `ArgumentException`.",
        [
            ("apply", "Hai đường vui, rồi cả hai hợp đồng lỗi: số chia zero và toán tử lạ."),
            ("vowels", "Bẫy là không phân biệt hoa thường: nguyên âm in hoa cũng được đếm."),
        ],
    ),
    solution='public class Solution\n{\n    public static double Apply(char op, double a, double b)\n    {\n        return op switch\n        {\n            \'+\' => a + b,\n            \'-\' => a - b,\n            \'*\' => a * b,\n            \'/\' => b == 0 ? throw new DivideByZeroException("zero divisor") : a / b,\n            _ => throw new ArgumentException("unknown operator: " + op)\n        };\n    }\n\n    public static int CountVowels(string s)\n    {\n        if (string.IsNullOrEmpty(s)) return 0;\n        int count = 0;\n        foreach (char c in s)\n        {\n            char lo = char.ToLowerInvariant(c);\n            if (lo == \'a\' || lo == \'e\' || lo == \'i\' || lo == \'o\' || lo == \'u\') count++;\n        }\n        return count;\n    }\n}\n',
    wrong='public class Solution\n{\n    public static double Apply(char op, double a, double b)\n    {\n        return op switch\n        {\n            \'+\' => a + b,\n            \'-\' => a - b,\n            \'*\' => a * b,\n            // near-miss: no zero check — doubles do NOT throw on their own,\n            // so this returns Infinity where the contract demands an exception\n            \'/\' => a / b,\n            _ => throw new ArgumentException("unknown operator: " + op)\n        };\n    }\n\n    public static int CountVowels(string s)\n    {\n        if (string.IsNullOrEmpty(s)) return 0;\n        int count = 0;\n        foreach (char c in s)\n        {\n            // near-miss: case-sensitive — uppercase vowels are missed\n            if (c == \'a\' || c == \'e\' || c == \'i\' || c == \'o\' || c == \'u\') count++;\n        }\n        return count;\n    }\n}\n',
)

print("module 5 authored")
