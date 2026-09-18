#!/usr/bin/env python3
"""C# — Beginner — Module 2: csb-types (variables, types, conversions).

Types as contracts: the core numeric ladder, decimal for money, char vs
string, var/const, null basics. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-types"

write_module(
    M,
    "Variables and Types",
    "Declare, initialize, and convert the core C# types — and learn when the compiler is saving you from yourself.",
    "Biến và Kiểu dữ liệu",
    "Khai báo, khởi tạo và chuyển đổi các kiểu C# cốt lõi — và hiểu khi nào compiler đang cứu bạn khỏi lỗi.",
    ["csb-m2-variables", "csb-m2-numeric-types", "csb-m2-strings-chars", "csb-m2-var-const-null", "csb-checkpoint-m2"],
    ["csb-p2-types"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m2-variables",
    "Variables: declare, initialize, assign",
    "A variable is a named slot with a type. The three verbs, and the errors the compiler blocks.",
    12,
    r"""
## Declaration, initialization, assignment

```csharp
int score;              // declaration: a slot named score that holds int
score = 10;             // assignment: put a value in
int level = 3;          // declaration + initialization in one line
score = score + 5;      // reassignment: the old value is read, then replaced
```

A variable's **type is fixed forever** at declaration. `int score = "ten";` is a compile error — not a runtime surprise. That's the single biggest difference from scripting languages, and it's a feature: the compiler catches a whole class of bugs before your program ever runs.

**Definite assignment**: C# refuses to let you *read* a local variable before you've written it:

```csharp
int x;
Console.WriteLine(x);   // error CS0165: use of unassigned local
```

The compiler tracks this per-path. It looks pedantic; it deletes an entire bug family (reading garbage memory) at zero cost.

## Identifiers

Names are case-sensitive (`score` and `Score` differ), must start with a letter or `_`, and conventionally use `camelCase` for locals. Prefer names that carry meaning: `elapsedMs` beats `e`; `invoiceCount` beats `n`. The compiler doesn't care; your teammates (and you-in-six-months) do.

## Multiple declarations

```csharp
int a = 1, b = 2;   // legal, but usually clearer as two lines
```
""",
    "Biến: khai báo, khởi tạo, gán",
    "Biến là ô nhớ có tên và có kiểu. Ba hành động, và những lỗi compiler chặn sẵn.",
    r"""
## Khai báo, khởi tạo, gán

```csharp
int score;              // khai báo: một ô tên score chứa int
score = 10;             // gán: đưa giá trị vào
int level = 3;          // khai báo + khởi tạo trên một dòng
score = score + 5;      // gán lại: giá trị cũ được đọc rồi thay thế
```

**Kiểu của biến cố định vĩnh viễn** ngay từ lúc khai báo. `int score = "ten";` là lỗi biên dịch — không phải bất ngờ lúc chạy. Đó là khác biệt lớn nhất so với ngôn ngữ kịch bản, và nó là một lợi thế: compiler bắt cả một lớp lỗi trước khi chương trình chạy.

**Gán giá trị chắc chắn**: C# từ chối cho bạn *đọc* biến cục bộ trước khi bạn đã ghi nó:

```csharp
int x;
Console.WriteLine(x);   // lỗi CS0165: use of unassigned local
```

Compiler theo dõi điều này theo từng nhánh thực thi. Có vẻ khắt khe; nhưng nó xóa sổ cả một họ lỗi (đọc rác trong bộ nhớ) với chi phí bằng 0.

## Tên định danh

Tên phân biệt chữ hoa/thường (`score` và `Score` khác nhau), phải bắt đầu bằng chữ hoặc `_`, và theo quy ước dùng `camelCase` cho biến cục bộ. Ưu tiên tên mang ý nghĩa: `elapsedMs` hơn `e`; `invoiceCount` hơn `n`. Compiler không quan tâm; đồng đội của bạn (và bạn-của-sáu-tháng-sau) thì có.

## Khai báo nhiều biến

```csharp
int a = 1, b = 2;   // hợp lệ, nhưng thường rõ ràng hơn nếu tách hai dòng
```
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m2-numeric-types",
    "The numeric ladder",
    "int, long, double, decimal — sizes, suffixes, and the money rule.",
    15,
    r"""
## The ladder

| Type | Size | Range / use | Literal |
|---|---|---|---|
| `int` | 32-bit | whole numbers ±~2.1 billion | `int n = 42;` |
| `long` | 64-bit | big counts, timestamps | `long t = 9_876_543_210L;` |
| `double` | 64-bit | general decimals, science | `double d = 0.5;` |
| `decimal` | 128-bit | **money**, exact base-10 | `decimal m = 19.99m;` |

Two traps the ladder hides:

**1. Integer division truncates.** `7 / 2` is `3`, not `3.5` — both operands are `int`, so the result is `int`. Write `7 / 2.0` (one operand makes the expression `double`) when you want the fraction. This is the most common numeric bug in beginner code.

**2. `double` is base-2; money is base-10.** `double x = 0.1 + 0.2;` gives `0.30000000000000004`. Binary floats can't represent most decimal fractions exactly — fine for measurements, wrong for money. Use `decimal` (note the `m` suffix) for currency:

```csharp
decimal price = 19.99m;
decimal total = price * 3;    // 59.97 exactly
```

**Overflow is silent by default**: `int.MaxValue + 1` wraps around in unchecked context (the default for constants is checked at compile time, but runtime arithmetic is not). Don't reach for `checked` yet — know that the boundary exists and that `long` is the escape hatch when counts can exceed ~2.1 billion.

**Conversion rules**: small → big is implicit (`int` → `long` → `double`); big → small needs an explicit cast `(int)`, which **truncates** (`(int)3.9` is `3`). Casting `double` → `int` also throws away, never rounds. Use `Math.Round` first when you need rounding.
""",
    "Thang số học",
    "int, long, double, decimal — kích thước, hậu tố, và quy tắc tiền tệ.",
    r"""
## Thang kiểu

| Kiểu | Kích thước | Phạm vi / dùng khi | Literal |
|---|---|---|---|
| `int` | 32-bit | số nguyên ±~2,1 tỷ | `int n = 42;` |
| `long` | 64-bit | số đếm lớn, timestamp | `long t = 9_876_543_210L;` |
| `double` | 64-bit | số thập phân nói chung, khoa học | `double d = 0.5;` |
| `decimal` | 128-bit | **tiền tệ**, chính xác base-10 | `decimal m = 19.99m;` |

Hai cái bẫy mà thang kiểu che giấu:

**1. Chia số nguyên bị cắt.** `7 / 2` là `3`, không phải `3.5` — cả hai toán tử đều `int` nên kết quả là `int`. Viết `7 / 2.0` (một toán tử làm biểu thức thành `double`) khi bạn cần phần lẻ. Đây là lỗi số học phổ biến nhất của người mới.

**2. `double` là base-2; tiền là base-10.** `double x = 0.1 + 0.2;` cho ra `0.30000000000000004`. Số thực nhị phân không biểu diễn được hầu hết phân số thập phân một cách chính xác — ổn cho đo lường, sai cho tiền tệ. Hãy dùng `decimal` (chú ý hậu tố `m`) cho tiền:

```csharp
decimal price = 19.99m;
decimal total = price * 3;    // 59.97 chính xác
```

**Tràn số mặc định là âm thầm**: `int.MaxValue + 1` quay vòng trong ngữ cảnh unchecked (mặc định khi chạy). Chưa cần dùng `checked` — chỉ cần biết biên giới tồn tại và `long` là lối thoát khi số đếm có thể vượt ~2,1 tỷ.

**Quy tắc chuyển đổi**: nhỏ → lớn là ngầm định (`int` → `long` → `double`); lớn → nhỏ cần ép kiểu tường minh `(int)`, và nó **cắt** (`(int)3.9` là `3`). Ép `double` → `int` chỉ bỏ phần lẻ, không bao giờ làm tròn. Cần làm tròn thì dùng `Math.Round` trước.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m2-strings-chars",
    "Strings, chars, and interpolation",
    "Text as data: immutability, char vs string, and string interpolation done right.",
    13,
    r"""
## char vs string

```csharp
char grade = 'A';          // single quotes: ONE UTF-16 code unit
string name = "Ada";       // double quotes: a sequence of chars
```

They're different types: `"A"` (string) and `'A'` (char) are not interchangeable. A string is **immutable** — methods like `ToUpper()` return a *new* string; the original never changes:

```csharp
string shout = name.ToUpper();   // "ADA" — name is still "Ada"
```

## Interpolation: the modern default

```csharp
string user = "Lan";
int points = 42;
Console.WriteLine($"User {user} has {points} points.");
// Any expression goes inside the braces:
Console.WriteLine($"Double: {points * 2}");
```

`$"` switches interpolation on. Inside `{}`, the compiler type-checks the expression. Formatting follows the value after `:` — `{price:F2}` for two decimals, `{n:D5}` to pad an integer:

```csharp
Console.WriteLine($"[{score:D3}]");   // [007]
```

Prefer interpolation over `+` concatenation: it reads in order, survives edits, and type-checks. You'll meet `StringBuilder` much later, when loop-built strings become a real performance topic — immutability means `a + b + c` allocates, but for beginner-scale strings clarity wins.

## Useful string members now

`name.Length`, `name.Contains("da")`, `name.StartsWith("A")`, `name.ToUpper()`, `name.Trim()`. Comparisons: `==` compares string *contents* in C# (unlike Java) — `a == b` is true when the text matches.
""",
    "String, char, và interpolation",
    "Văn bản là dữ liệu: tính bất biến, char so với string, và string interpolation đúng chuẩn.",
    r"""
## char so với string

```csharp
char grade = 'A';          // nháy đơn: MỘT đơn vị mã UTF-16
string name = "Ada";       // nháy đôi: một chuỗi các char
```

Đây là hai kiểu khác nhau: `"A"` (string) và `'A'` (char) không thay thế được cho nhau. String là **bất biến** — các phương thức như `ToUpper()` trả về string *mới*; bản gốc không bao giờ đổi:

```csharp
string shout = name.ToUpper();   // "ADA" — name vẫn là "Ada"
```

## Interpolation: lựa chọn hiện đại

```csharp
string user = "Lan";
int points = 42;
Console.WriteLine($"Người dùng {user} có {points} điểm.");
// Bên trong ngoặc nhọn có thể là bất kỳ biểu thức nào:
Console.WriteLine($"Gấp đôi: {points * 2}");
```

`$"` bật interpolation. Trong `{}`, compiler kiểm tra kiểu của biểu thức. Định dạng theo giá trị sau dấu `:` — `{price:F2}` cho hai chữ số thập phân, `{n:D5}` để đệm số 0:

```csharp
Console.WriteLine($"[{score:D3}]");   // [007]
```

Ưu tiên interpolation thay vì nối chuỗi bằng `+`: nó đọc theo thứ tự, bền khi sửa, và được kiểm tra kiểu. Bạn sẽ gặp `StringBuilder` sau này, khi việc dựng chuỗi trong vòng lặp mới thành chủ đề hiệu năng thực — tính bất biến nghĩa là `a + b + c` cấp phát bộ nhớ, nhưng ở quy mô người mới thì sự rõ ràng thắng.

## Các thành viên string hữu ích ngay bây giờ

`name.Length`, `name.Contains("da")`, `name.StartsWith("A")`, `name.ToUpper()`, `name.Trim()`. So sánh: `==` so sánh **nội dung** string trong C# (khác Java) — `a == b` đúng khi văn bản khớp.
""",
)

# ---------------------------------------------------------------- lesson 4
write_lesson(
    M, "csb-m2-var-const-null",
    "var, const, and the null concept",
    "Type inference, compile-time constants, and the idea of 'no object'.",
    12,
    r"""
## var: inference, not dynamic

```csharp
var count = 10;          // compiler infers int — count IS an int, forever
var name = "Ada";        // string
var price = 19.99m;      // decimal (the suffix drives inference)
```

`var` is not JavaScript's `var`. The type is inferred **at compile time** and then fixed; `var x = 5; x = "hi";` is a compile error. Rule of thumb: use `var` when the right-hand side makes the type obvious (`new List<int>()`, a constructor call); write the explicit type when it aids reading (`long total = 0;`).

## const

```csharp
const int MaxRetries = 3;
const double Pi = 3.14159;
```

`const` is a compile-time constant: its value is baked into every use site, it's implicitly static, and it can never be reassigned. Use it for values that are truly permanent (`MaxRetries`, `DaysInWeek`). Naming: `PascalCase` is the C# convention for constants.

## null: the absence of an object

A variable of a *reference type* (like `string`) either refers to an object or is `null` — "refers to nothing". Dereferencing `null` throws `NullReferenceException` at runtime:

```csharp
string nickname = null;
Console.WriteLine(nickname.Length);   // throws at runtime
```

C#'s compiler flow analysis warns you about likely nulls (nullable reference types), and `null` checks are a normal part of validating input. For now: know the word, expect the exception name, and treat every incoming value as possibly-absent until validated. Value types (`int`, `decimal`, `bool`) cannot be `null` — they always hold a value.
""",
    "var, const, và khái niệm null",
    "Suy luận kiểu, hằng số thời gian biên dịch, và ý niệm 'không có đối tượng'.",
    r"""
## var: suy luận, không phải động

```csharp
var count = 10;          // compiler suy ra int — count LÀ int, vĩnh viễn
var name = "Ada";        // string
var price = 19.99m;      // decimal (hậu tố quyết định suy luận)
```

`var` không giống `var` của JavaScript. Kiểu được suy **lúc biên dịch** rồi cố định; `var x = 5; x = "hi";` là lỗi biên dịch. Nguyên tắc: dùng `var` khi vế phải cho thấy rõ kiểu (`new List<int>()`, lời gọi constructor); viết kiểu tường minh khi nó giúp việc đọc (`long total = 0;`).

## const

```csharp
const int MaxRetries = 3;
const double Pi = 3.14159;
```

`const` là hằng số thời gian biên dịch: giá trị được nhúng vào mọi nơi sử dụng, mặc định là static, và không bao giờ được gán lại. Dùng cho các giá trị thực sự vĩnh cửu (`MaxRetries`, `DaysInWeek`). Tên đặt: `PascalCase` là quy ước C# cho hằng.

## null: sự vắng mặt của đối tượng

Một biến kiểu *tham chiếu* (như `string`) hoặc trỏ tới một đối tượng hoặc là `null` — "không trỏ tới gì cả". Truy cập thành phần trên `null` ném `NullReferenceException` lúc chạy:

```csharp
string nickname = null;
Console.WriteLine(nickname.Length);   // ném exception lúc chạy
```

Compiler C# phân tích luồng và cảnh báo về giá trị có khả năng null (nullable reference types), và kiểm tra `null` là một phần bình thường của việc kiểm chứng input. Hiện tại: hiểu từ khoá, nhớ tên exception, và coi mọi giá trị đầu vào là có-thể-vắng-mặt cho đến khi kiểm chứng. Kiểu giá trị (`int`, `decimal`, `bool`) không thể là `null` — chúng luôn giữ một giá trị.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p2-types",
    "Types under pressure",
    "Numeric traps, exact formatting, and the money rule — implemented, not memorized.",
    "Kiểu dữ liệu dưới áp lực",
    "Bẫy số học, định dạng chính xác, và quy tắc tiền tệ — làm thật, không học vẹt.",
    "csb-m2-var-const-null",
    35,
    "beginner",
    [
        challenge(
            "csb-p2-celsius",
            "Celsius to Fahrenheit",
            "Implement `static double ToFahrenheit(double celsius)` returning `celsius * 9 / 5 + 32`. Keep it exact for fractional input.",
            CS_PRELUDE,
            [
                (
                    "boils",
                    "Cj.Near(Solution.ToFahrenheit(100), 212, 0.0001, \"100C\");\nCj.Near(Solution.ToFahrenheit(0), 32, 0.0001, \"0C\");",
                    "The classic reference points.",
                ),
                (
                    "fractional",
                    "Cj.Near(Solution.ToFahrenheit(36.6), 97.88, 0.0001, \"36.6C\");",
                    "36.6 * 9 / 5 must not truncate — watch the integer-division trap.",
                ),
            ],
            level="imitation",
        ),
        challenge(
            "csb-p2-split-bill",
            "Split the bill exactly",
            "Implement `static decimal Split(decimal total, int people)` returning each person's share. Total is decimal; division by `people` must be decimal division.",
            CS_PRELUDE,
            [
                (
                    "exact-cents",
                    'Cj.Eq(Solution.Split(59.97m, 3), 19.99m, "59.97/3");\nCj.Eq(Solution.Split(100m, 4), 25m, "100/4");',
                    "Decimal division keeps cents exact.",
                ),
                (
                    "repeating",
                    "Cj.Eq(Solution.Split(10.00m, 3), 10.00m / 3m, \"10/3\");",
                    "The test compares against decimal division — no double in sight.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p2-truncate-vs-round",
            "Truncate, then round",
            "Implement two functions: `static int Truncate(double d)` returning the integer part, and `static int Round(double d)` returning d rounded to nearest (midpoint away from zero). Use casts and Math.Round deliberately.",
            CS_PRELUDE,
            [
                (
                    "truncate",
                    'Cj.Eq(Solution.Truncate(3.9), 3, "3.9");\nCj.Eq(Solution.Truncate(-3.9), -3, "-3.9");\nCj.Eq(Solution.Truncate(7.0), 7, "7.0");',
                    "Cast truncates toward zero.",
                ),
                (
                    "round",
                    'Cj.Eq(Solution.Round(3.5), 4, "3.5");\nCj.Eq(Solution.Round(2.5), 3, "2.5");\nCj.Eq(Solution.Round(-2.5), -3, "-2.5");\nCj.Eq(Solution.Round(2.4), 2, "2.4");',
                    "Midpoint away from zero: 2.5→3, -2.5→-3 (banker's rounding would give 2 and -2).",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p2-inventory-line",
            "Formatted inventory line",
            "Implement `static string Line(string name, int qty, decimal price)` returning exactly `name` padded-right to 10 chars, a space, qty padded-left to 3 with zeros, a space, and price with exactly 2 decimals. Example: `Wire      007 4.50`.",
            CS_PRELUDE,
            [
                (
                    "format-exact",
                    'Cj.Eq(Solution.Line("Wire", 7, 4.5m), "Wire       007 4.50", "row");',
                    "PadRight(10), D3, F2 — in that order, single spaces.",
                ),
                (
                    "long-name",
                    'Cj.Eq(Solution.Line("Motherboard", 2, 129.99m), "Motherboard 002 129.99", "row");',
                    "PadRight never shortens: 11 chars stays 11.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p2-celsius": vi_challenge(
            "Độ C sang độ F",
            "Hiện thực `static double ToFahrenheit(double celsius)` trả về `celsius * 9 / 5 + 32`. Giữ chính xác với input lẻ.",
            [
                ("boils", "Hai mốc kinh điển."),
                ("fractional", "36.6 * 9 / 5 không được bị cắt — chú ý bẫy chia số nguyên."),
            ],
        ),
        "csb-p2-split-bill": vi_challenge(
            "Chia hoá đơn chính xác",
            "Hiện thực `static decimal Split(decimal total, int people)` trả về phần của mỗi người. Total là decimal; phép chia cho `people` phải là chia decimal.",
            [
                ("exact-cents", "Chia decimal giữ chính xác đến xu."),
                ("repeating", "Test so với phép chia decimal — không có double ở đây."),
            ],
        ),
        "csb-p2-truncate-vs-round": vi_challenge(
            "Cắt, rồi làm tròn",
            "Hiện thực hai hàm: `static int Truncate(double d)` trả phần nguyên, và `static int Round(double d)` làm tròn tới gần nhất (midpoint lùi xa 0). Dùng ép kiểu và Math.Round có chủ đích.",
            [
                ("truncate", "Ép kiểu cắt về phía 0."),
                ("round", "Midpoint lùi xa 0: 2.5→3, -2.5→-3."),
            ],
        ),
        "csb-p2-inventory-line": vi_challenge(
            "Dòng tồn kho có định dạng",
            "Hiện thực `static string Line(string name, int qty, decimal price)` trả về đúng: `name` đệm-phải tới 10 ký tự, một dấu cách, qty đệm-trái tới 3 số 0, một dấu cách, price với đúng 2 chữ số thập phân. Ví dụ: `Wire      007 4.50`.",
            [
                ("format-exact", "PadRight(10), D3, F2 — theo đúng thứ tự, cách nhau một dấu cách."),
                ("long-name", "PadRight không bao giờ cắt ngắn: 11 ký tự vẫn là 11."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p2-celsius",
            'public class Solution\n{\n    public static double ToFahrenheit(double celsius)\n    {\n        return celsius * 9 / 5 + 32;\n    }\n}\n',
            'public class Solution\n{\n    public static double ToFahrenheit(double celsius)\n    {\n        // near-miss: 9/5 is integer division == 1\n        return celsius * (9 / 5) + 32;\n    }\n}\n',
        ),
        (
            "csb-p2-split-bill",
            'public class Solution\n{\n    public static decimal Split(decimal total, int people)\n    {\n        return total / people;\n    }\n}\n',
            'public class Solution\n{\n    public static decimal Split(decimal total, int people)\n    {\n        // near-miss: computing in double loses decimal exactness\n        return (decimal)((double)total / people);\n    }\n}\n',
        ),
        (
            "csb-p2-truncate-vs-round",
            'public class Solution\n{\n    public static int Truncate(double d) => (int)d;\n\n    public static int Round(double d) => (int)Math.Round(d, System.MidpointRounding.AwayFromZero);\n}\n',
            'public class Solution\n{\n    public static int Truncate(double d) => (int)d;\n\n    // near-miss: default midpoint rounding is banker\'s — 2.5 → 2, -2.5 → -2\n    public static int Round(double d) => (int)Math.Round(d);\n}\n',
        ),
        (
            "csb-p2-inventory-line",
            'public class Solution\n{\n    public static string Line(string name, int qty, decimal price)\n    {\n        return name.PadRight(10) + " " + qty.ToString("D3") + " " + price.ToString("F2");\n    }\n}\n',
            'public class Solution\n{\n    public static string Line(string name, int qty, decimal price)\n    {\n        // near-miss: PadLeft on the name — flips the columns\n        return name.PadLeft(10) + " " + qty.ToString("D3") + " " + price.ToString("F2");\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m2",
    "Checkpoint — Types",
    "Money math and exact formatting, from a blank file.",
    18,
    r"""
## Checkpoint: the receipt, typed

**Task:** implement `static decimal Total(decimal price, int count, decimal taxRate)` returning the after-tax total as a decimal: `price * count` then apply tax by multiplying by `(1 + taxRate)`. Then implement `static string Receipt(decimal total)` returning `$` + total formatted to exactly 2 decimals (e.g. `$59.97`).
""",
    "Checkpoint — Kiểu dữ liệu",
    "Tính tiền và định dạng chính xác, từ file trống.",
    r"""
## Checkpoint: hoá đơn có kiểu

**Nhiệm vụ:** hiện thực `static decimal Total(decimal price, int count, decimal taxRate)` trả về tổng sau thuế là decimal: `price * count` rồi nhân với `(1 + taxRate)`. Sau đó hiện thực `static string Receipt(decimal total)` trả về `$` + total với đúng 2 chữ số thập phân (ví dụ `$59.97`).
""",
    challenge(
        "csb-checkpoint-m2-task",
        "Typed receipt",
        "Implement `Total` and `Receipt` exactly as the checkpoint describes. The tests check decimal exactness and the 2-decimal format.",
        CS_PRELUDE,
        [
            (
                "total-exact",
                'Cj.Eq(Solution.Total(19.99m, 3, 0.0m), 59.97m, "no tax");\nCj.Eq(Solution.Total(10.00m, 2, 0.1m), 22.00m, "10% tax");',
                "decimal math stays exact.",
            ),
            (
                "receipt-format",
                'Cj.Eq(Solution.Receipt(59.97m), "$59.97", "format");\nCj.Eq(Solution.Receipt(59.9m), "$59.90", "trailing zero");',
                "F2 keeps two decimals, even the trailing zero.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Hoá đơn có kiểu",
        "Hiện thực `Total` và `Receipt` đúng như checkpoint mô tả. Test kiểm tra độ chính xác decimal và định dạng 2 chữ số.",
        [
            ("total-exact", "Phép toán decimal giữ nguyên độ chính xác."),
            ("receipt-format", "F2 giữ đúng hai chữ số, kể cả số 0 cuối."),
        ],
    ),
    solution='public class Solution\n{\n    public static decimal Total(decimal price, int count, decimal taxRate)\n    {\n        return price * count * (1 + taxRate);\n    }\n\n    public static string Receipt(decimal total)\n    {\n        return "$" + total.ToString("F2");\n    }\n}\n',
    wrong='public class Solution\n{\n    public static decimal Total(decimal price, int count, decimal taxRate)\n    {\n        // near-miss: adds tax instead of multiplying by (1 + rate)\n        return price * count + taxRate;\n    }\n\n    public static string Receipt(decimal total)\n    {\n        return "$" + total.ToString("F1");\n    }\n}\n',
)

print("module 2 authored")
