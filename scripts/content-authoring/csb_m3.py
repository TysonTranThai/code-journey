#!/usr/bin/env python3
"""C# — Beginner — Module 3: csb-io (input, output, parsing).

ReadLine/parsing/TryParse/validation, with the graded contract adapted:
the sandbox runs non-interactive, so challenges grade `answer(...)` against
provided input strings — the same parse-validate-respond logic ReadLine
programs need.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-io"

write_module(
    M,
    "Input, Output, and Parsing",
    "Turn text in, numbers out: ReadLine, Parse vs TryParse, and validation that refuses garbage politely.",
    "Nhập, xuất, và phân tích cú pháp",
    "Biến văn bản thành số: ReadLine, Parse so với TryParse, và kiểm tra dữ liệu từ chối rác một cách lịch sự.",
    ["csb-m3-reading-input", "csb-m3-parsing", "csb-m3-tryparse-validation", "csb-checkpoint-m3"],
    ["csb-p3-io"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m3-reading-input",
    "Reading input from the console",
    "Console.ReadLine returns text — always. What that means for everything downstream.",
    12,
    r"""
## ReadLine: text, always text

```csharp
Console.Write("Your name: ");
string name = Console.ReadLine() ?? "";
Console.WriteLine($"Hello, {name}!");
```

`Console.ReadLine()` reads one line and hands it to you as a `string` — **even if the user typed digits**. `"42"` (text) and `42` (number) are different universes: you cannot do arithmetic on text. The `?? ""` covers the edge case where input ends before a line arrives (ReadLine then returns `null`).

Every interactive program you've used is this loop underneath: read text → interpret → respond.

## The shape of input handling

```csharp
Console.Write("Radius: ");
string input = Console.ReadLine() ?? "";
double radius = double.Parse(input);       // crashes on "abc"!
double area = Math.PI * radius * radius;
Console.WriteLine($"Area: {area:F2}");
```

`double.Parse` converts text to a number — and **throws `FormatException`** if the text isn't a valid number. A user who types `ten` or `3,14` or just presses Enter crashes this program. That's the problem the next two lessons solve properly (TryParse + validation).

## A note on this course's sandbox

Challenges here grade the *logic* (parse, validate, respond) through a method that takes the raw input string — the same code shape ReadLine programs need, but deterministic and testable. When you take this code to a real console, the ReadLine wrapper around it is trivial.
""",
    "Đọc input từ console",
    "Console.ReadLine luôn trả về văn bản — điều đó quyết định mọi thứ phía sau.",
    r"""
## ReadLine: luôn là văn bản

```csharp
Console.Write("Tên của bạn: ");
string name = Console.ReadLine() ?? "";
Console.WriteLine($"Xin chào, {name}!");
```

`Console.ReadLine()` đọc một dòng và đưa cho bạn một `string` — **kể cả khi người dùng gõ số**. `"42"` (văn bản) và `42` (số) là hai thế giới khác nhau: bạn không thể tính toán trên văn bản. `?? ""` xử lý trường hợp input kết thúc trước khi có dòng (ReadLine khi đó trả về `null`).

Mọi chương trình tương tác bạn từng dùng đều là vòng lặp này bên dưới: đọc văn bản → diễn giải → phản hồi.

## Hình dạng của việc xử lý input

```csharp
Console.Write("Bán kính: ");
string input = Console.ReadLine() ?? "";
double radius = double.Parse(input);       // nổ nếu là "abc"!
double area = Math.PI * radius * radius;
Console.WriteLine($"Diện tích: {area:F2}");
```

`double.Parse` chuyển văn bản thành số — và **ném `FormatException`** nếu văn bản không phải số hợp lệ. Người dùng gõ `mười` hay `3,14` hay chỉ nhấn Enter sẽ làm chương trình này sập. Đó là vấn đề hai bài học sau giải quyết đúng mực (TryParse + kiểm tra dữ liệu).

## Lưu ý về sandbox của khoá này

Thử thách ở đây chấm điểm *logic* (phân tích, kiểm tra, phản hồi) thông qua một phương thức nhận chuỗi input thô — cùng hình dạng code mà chương trình ReadLine cần, nhưng xác định và kiểm thử được. Khi bạn mang code này ra console thật, phần bao bọc ReadLine là việc nhỏ.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m3-parsing",
    "Parsing text to numbers",
    "int.Parse, double.Parse, decimal.Parse — what each accepts, and the FormatException contract.",
    12,
    r"""
## The Parse family

```csharp
int i = int.Parse("42");            // 42
int neg = int.Parse("-17");         // -17
double d = double.Parse("3.5");     // 3.5
decimal m = decimal.Parse("19.99"); // 19.99
int bad = int.Parse("4 2");         // FormatException
int empty = int.Parse("");          // FormatException
```

Each type's Parse accepts exactly the formats its own `ToString` produces (plus leading/trailing spaces, which are trimmed). `int.Parse("3.5")` **fails** — there's no silent truncation on the way in. Whitespace inside the number fails; a decimal point for an `int` fails.

**Culture matters**: by default Parse uses the machine's culture — on systems configured with `,` as the decimal separator, `double.Parse("3.5")` fails. For this course's challenges the sandbox culture parses `.`; when you build real apps you'll meet `CultureInfo.InvariantCulture` for machine-to-machine formats. Knowing the trap exists is the beginner takeaway.

## Choosing the type

Parse into the type that models the value: `int` for counts, `double` for measurements, `decimal` for money. If the input is `"19.99"`, `int.Parse` is the wrong tool *before* you even ask whether it throws.

## What a FormatException looks like

Unhandled, it kills the program with a stack trace. You'll learn `try/catch` in Module 15 — but for input validation the right tool comes first: **TryParse**, which never throws at all.
""",
    "Phân tích văn bản thành số",
    "int.Parse, double.Parse, decimal.Parse — mỗi loại chấp nhận gì, và hợp đồng FormatException.",
    r"""
## Họ Parse

```csharp
int i = int.Parse("42");            // 42
int neg = int.Parse("-17");         // -17
double d = double.Parse("3.5");     // 3.5
decimal m = decimal.Parse("19.99"); // 19.99
int bad = int.Parse("4 2");         // FormatException
int empty = int.Parse("");          // FormatException
```

Parse của mỗi kiểu chỉ chấp nhận đúng các định dạng mà `ToString` của chính nó tạo ra (cộng khoảng trắng đầu/cuối, vốn được cắt bỏ). `int.Parse("3.5")` **thất bại** — không có cắt cụt âm thầm khi đưa vào. Khoảng trắng giữa các chữ số làm hỏng; dấu chấm thập phân với `int` làm hỏng.

**Văn hoá (culture) có vai trò**: mặc định Parse dùng văn hoá của máy — trên hệ thống dùng `,` làm dấu thập phân, `double.Parse("3.5")` thất bại. Sandbox của khoá này dùng culture phân tích được `.`; khi xây ứng dụng thật bạn sẽ gặp `CultureInfo.InvariantCulture` cho định dạng máy-gửi-máy. Với người mới, điều quan trọng là biết cái bẫy tồn tại.

## Chọn kiểu

Phân tích vào kiểu mô hình hoá giá trị: `int` cho số đếm, `double` cho đo lường, `decimal` cho tiền. Input là `"19.99"` thì `int.Parse` đã là công cụ sai *trước cả khi* hỏi nó có nổ hay không.

## FormatException trông như thế nào

Không xử lý, nó hạ chương trình kèm stack trace. Bạn sẽ học `try/catch` ở Module 15 — nhưng với việc kiểm tra input, đúng công cụ là thứ khác: **TryParse**, vốn không bao giờ ném.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m3-tryparse-validation",
    "TryParse: the no-throw parser",
    "The out-parameter pattern, validation loops, and building robust input handling.",
    14,
    r"""
## The pattern

```csharp
bool ok = int.TryParse("42", out int value);   // ok = true,  value = 42
bool bad = int.TryParse("abc", out int other); // bad = false, other = 0
```

`TryParse` attempts the conversion and reports success as a `bool`. The parsed value arrives through an **`out` parameter** — a second return channel. On failure the `out` value is `0` (a well-defined default), never garbage.

The idiomatic shape combines declaration and use:

```csharp
if (int.TryParse(input, out int count))
{
    Console.WriteLine($"Got {count}");
}
else
{
    Console.WriteLine("Not a whole number.");
}
```

## Validation: refuse politely, specifically

A robust reader distinguishes *why* input is invalid:

```csharp
static string Classify(string input)
{
    if (input.Trim().Length == 0)
        return "empty";
    if (!int.TryParse(input, out int n))
        return "not-a-number";
    if (n < 0)
        return "negative";
    return $"ok:{n}";
}
```

Empty first, then format, then range — each failure mode gets its own message. That specificity is what separates a program people can use from one that just says "error".

## Looping until valid (console shape)

```csharp
int age;
while (true)
{
    Console.Write("Age: ");
    string line = Console.ReadLine() ?? "";
    if (int.TryParse(line, out age) && age >= 0 && age <= 130) break;
    Console.WriteLine("Please enter a whole number 0–130.");
}
```

The loop *contains* the validation, so the rest of the program can trust `age`. That's the deeper principle: validate at the boundary, then write code that assumes validity.
""",
    "TryParse: trình phân tích không ném",
    "Mẫu tham số out, vòng lặp kiểm tra dữ liệu, và xây dựng bộ xử lý input bền vững.",
    r"""
## Mẫu TryParse

```csharp
bool ok = int.TryParse("42", out int value);   // ok = true,  value = 42
bool bad = int.TryParse("abc", out int other); // bad = false, other = 0
```

`TryParse` thử chuyển đổi và báo thành công bằng `bool`. Giá trị phân tích được đến qua một **tham số `out`** — kênh trả về thứ hai. Khi thất bại, giá trị `out` là `0` (mặc định xác định rõ), không bao giờ là rác.

Hình thái theo thói quen idiomatic kết hợp khai báo và sử dụng:

```csharp
if (int.TryParse(input, out int count))
{
    Console.WriteLine($"Đã nhận {count}");
}
else
{
    Console.WriteLine("Không phải số nguyên.");
}
```

## Kiểm tra dữ liệu: từ chối lịch sự, cụ thể

Một bộ đọc bền vững phân biệt *lý do* input không hợp lệ:

```csharp
static string Classify(string input)
{
    if (input.Trim().Length == 0)
        return "empty";
    if (!int.TryParse(input, out int n))
        return "not-a-number";
    if (n < 0)
        return "negative";
    return $"ok:{n}";
}
```

Rỗng trước, rồi định dạng, rồi khoảng giá trị — mỗi kiểu thất bại có thông điệp riêng. Tính cụ thể đó là ranh giới giữa chương trình người dùng dùng được và chương trình chỉ biết nói "lỗi".

## Lặp cho tới khi hợp lệ (dạng console)

```csharp
int age;
while (true)
{
    Console.Write("Tuổi: ");
    string line = Console.ReadLine() ?? "";
    if (int.TryParse(line, out age) && age >= 0 && age <= 130) break;
    Console.WriteLine("Vui lòng nhập số nguyên 0–130.");
}
```

Vòng lặp *chứa* việc kiểm tra, nên phần còn lại của chương trình được tin rằng `age` hợp lệ. Đó là nguyên lý sâu hơn: kiểm chứng ở biên giới, rồi viết code với giả định hợp lệ.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p3-io",
    "Parse and validate",
    "Turn raw strings into trustworthy numbers — with failure modes that teach, not crash.",
    "Phân tích và kiểm tra",
    "Biến chuỗi thô thành số đáng tin — với các kiểu thất bại dạy người dùng, không làm sập.",
    "csb-m3-tryparse-validation",
    30,
    "beginner",
    [
        challenge(
            "csb-p3-parse-or-default",
            "Parse or default",
            "Implement `static int ParseOrDefault(string input)` — return the parsed int if `input` is a valid whole number, otherwise return `0`. Empty string and whitespace count as invalid.",
            CS_PRELUDE,
            [
                (
                    "valid-input",
                    'Cj.Eq(Solution.ParseOrDefault("42"), 42, "42");\nCj.Eq(Solution.ParseOrDefault(" -7 "), -7, "padded");',
                    "TryParse trims outer whitespace.",
                ),
                (
                    "invalid-input",
                    'Cj.Eq(Solution.ParseOrDefault("abc"), 0, "abc");\nCj.Eq(Solution.ParseOrDefault(""), 0, "empty");\nCj.Eq(Solution.ParseOrDefault("3.5"), 0, "decimal point");',
                    "Anything int.Parse would reject → 0.",
                ),
            ],
            level="imitation",
        ),
        challenge(
            "csb-p3-classifier",
            "Input classifier",
            "Implement `static string Classify(string input)`: return `\"empty\"` for null/whitespace-only input, `\"not-a-number\"` when it isn't an int, `\"negative\"` when the int is < 0, otherwise `\"ok:\" + n`.",
            CS_PRELUDE,
            [
                (
                    "branches",
                    'Cj.Eq(Solution.Classify("  "), "empty", "spaces");\nCj.Eq(Solution.Classify("x1"), "not-a-number", "x1");\nCj.Eq(Solution.Classify("-3"), "negative", "-3");\nCj.Eq(Solution.Classify("12"), "ok:12", "12");',
                    "All four branches, checked in order.",
                ),
                (
                    "empty-vs-invalid",
                    'Cj.Eq(Solution.Classify(""), "empty", "empty");\nCj.Eq(Solution.Classify("1.5"), "not-a-number", "1.5");',
                    "Empty comes before format — check order matters.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p3-range-gate",
            "Range gate",
            "Implement `static bool IsValidScore(string input)` — true exactly when input parses to an int from 0 to 100 inclusive. `\"100\"` true, `\"101\"` false, `\"abc\"` false, `\"-1\"` false.",
            CS_PRELUDE,
            [
                (
                    "in-range",
                    'Cj.True(Solution.IsValidScore("0"), "0");\nCj.True(Solution.IsValidScore("100"), "100");\nCj.True(Solution.IsValidScore(" 55 "), "padded");',
                    "Both endpoints inclusive; trimming is expected.",
                ),
                (
                    "out-of-range",
                    'Cj.False(Solution.IsValidScore("101"), "101");\nCj.False(Solution.IsValidScore("-1"), "-1");\nCj.False(Solution.IsValidScore("abc"), "abc");',
                    "Out of range and non-numeric both fail closed.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p3-csv-sum",
            "Sum a comma list",
            "Implement `static int SumList(string csv)` — input like `\"3,4,10\"`; split on commas, parse each piece, return the sum. Any unparseable piece makes the whole input invalid: return `-1`.",
            CS_PRELUDE,
            [
                (
                    "all-valid",
                    'Cj.Eq(Solution.SumList("3,4,10"), 17, "3,4,10");\nCj.Eq(Solution.SumList("5"), 5, "single");\nCj.Eq(Solution.SumList("-2,10"), 8, "negatives ok");',
                    "Every piece must parse; negatives are legal values.",
                ),
                (
                    "one-bad-piece",
                    'Cj.Eq(Solution.SumList("3,x,10"), -1, "x");\nCj.Eq(Solution.SumList("3,,10"), -1, "empty piece");',
                    "One bad piece poisons the whole list — fail closed.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p3-parse-or-default": vi_challenge(
            "Phân tích hoặc mặc định",
            "Hiện thực `static int ParseOrDefault(string input)` — trả về số int nếu `input` là số nguyên hợp lệ, ngược lại trả `0`. Chuỗi rỗng và toàn khoảng trắng tính là không hợp lệ.",
            [
                ("valid-input", "TryParse cắt khoảng trắng hai đầu."),
                ("invalid-input", "Mọi thứ int.Parse từ chối → 0."),
            ],
        ),
        "csb-p3-classifier": vi_challenge(
            "Phân loại input",
            "Hiện thực `static string Classify(string input)`: trả `\"empty\"` cho input null/chỉ khoảng trắng, `\"not-a-number\"` khi không phải số nguyên, `\"negative\"` khi số < 0, còn lại `\"ok:\" + n`.",
            [
                ("branches", "Cả bốn nhánh, kiểm tra theo thứ tự."),
                ("empty-vs-invalid", "Rỗng đứng trước định dạng — thứ tự kiểm tra có ý nghĩa."),
            ],
        ),
        "csb-p3-range-gate": vi_challenge(
            "Cổng khoảng giá trị",
            "Hiện thực `static bool IsValidScore(string input)` — đúng khi và chỉ khi input phân tích được thành số nguyên từ 0 đến 100 (bao gồm hai đầu). `\"100\"` đúng, `\"101\"` sai, `\"abc\"` sai, `\"-1\"` sai.",
            [
                ("in-range", "Cả hai đầu đều bao gồm; cắt khoảng trắng là điều được kỳ vọng."),
                ("out-of-range", "Ngoài khoảng và không phải số đều thất bại an toàn."),
            ],
        ),
        "csb-p3-csv-sum": vi_challenge(
            "Tổng danh sách phân cách bởi phẩy",
            "Hiện thực `static int SumList(string csv)` — input dạng `\"3,4,10\"`; tách theo phẩy, phân tích từng mảnh, trả tổng. Bất kỳ mảnh nào không phân tích được làm cả input không hợp lệ: trả `-1`.",
            [
                ("all-valid", "Mọi mảnh phải phân tích được; số âm là giá trị hợp lệ."),
                ("one-bad-piece", "Một mảnh hỏng làm hỏng cả danh sách — thất bại an toàn."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p3-parse-or-default",
            'public class Solution\n{\n    public static int ParseOrDefault(string input)\n    {\n        return int.TryParse(input, out int value) ? value : 0;\n    }\n}\n',
            'public class Solution\n{\n    public static int ParseOrDefault(string input)\n    {\n        // near-miss: double.Parse accepts "3.5", then the cast truncates —\n        // so ParseOrDefault("3.5") wrongly returns 3 instead of 0\n        try { return (int)double.Parse(input); } catch { return 0; }\n    }\n}\n',
        ),
        (
            "csb-p3-classifier",
            'public class Solution\n{\n    public static string Classify(string input)\n    {\n        if (string.IsNullOrWhiteSpace(input)) return "empty";\n        if (!int.TryParse(input, out int n)) return "not-a-number";\n        if (n < 0) return "negative";\n        return "ok:" + n;\n    }\n}\n',
            'public class Solution\n{\n    public static string Classify(string input)\n    {\n        // near-miss: checks the number branches FIRST, so "" throws instead\n        // of reporting "empty" — order of checks is the bug\n        if (!int.TryParse(input ?? "", out int n)) return "not-a-number";\n        if (n < 0) return "negative";\n        return "ok:" + n;\n    }\n}\n',
        ),
        (
            "csb-p3-range-gate",
            'public class Solution\n{\n    public static bool IsValidScore(string input)\n    {\n        return int.TryParse(input, out int score) && score >= 0 && score <= 100;\n    }\n}\n',
            'public class Solution\n{\n    public static bool IsValidScore(string input)\n    {\n        // near-miss: || instead of && — accepts 101 and "abc"→0\n        return int.TryParse(input, out int score) || score >= 0 && score <= 100;\n    }\n}\n',
        ),
        (
            "csb-p3-csv-sum",
            'public class Solution\n{\n    public static int SumList(string csv)\n    {\n        int total = 0;\n        foreach (string piece in (csv ?? "").Split(\',\'))\n        {\n            if (!int.TryParse(piece, out int n)) return -1;\n            total += n;\n        }\n        return total;\n    }\n}\n',
            'public class Solution\n{\n    public static int SumList(string csv)\n    {\n        int total = 0;\n        foreach (string piece in (csv ?? "").Split(\',\'))\n        {\n            // near-miss: skips bad pieces instead of failing the whole list\n            if (int.TryParse(piece, out int n)) total += n;\n        }\n        return total;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m3",
    "Checkpoint — Input pipeline",
    "One method that reads like production validation code.",
    18,
    r"""
## Checkpoint: the intake form

**Task:** implement `static string ProcessField(string label, string input)` which validates one form field:

- label `"age"`: must parse to an int 1–119 → `"accept"` else `"reject:age"`.
- label `"score"`: must parse to an int 0–100 → `"accept"` else `"reject:score"`.
- any other label → `"reject:label"`.
- whitespace-only input (any label) → `"reject:empty"` (checked first).
""",
    "Checkpoint — Đường ống input",
    "Một phương thức đọc như code kiểm chứng trong sản phẩm thật.",
    r"""
## Checkpoint: biểu mẫu tiếp nhận

**Nhiệm vụ:** hiện thực `static string ProcessField(string label, string input)` kiểm chứng một trường của biểu mẫu:

- label `"age"`: phải phân tích được thành số nguyên 1–119 → `"accept"` nếu không `"reject:age"`.
- label `"score"`: phải phân tích được thành số nguyên 0–100 → `"accept"` nếu không `"reject:score"`.
- label khác → `"reject:label"`.
- input chỉ toàn khoảng trắng (bất kỳ label) → `"reject:empty"` (kiểm tra trước).
""",
    challenge(
        "csb-checkpoint-m3-task",
        "Form field validator",
        "Implement `ProcessField` exactly as the checkpoint describes. Check empty first, then label, then value.",
        CS_PRELUDE,
        [
            (
                "happy-paths",
                'Cj.Eq(Solution.ProcessField("age", "42"), "accept", "age");\nCj.Eq(Solution.ProcessField("score", "100"), "accept", "score");',
                "Valid age and valid score both accept.",
            ),
            (
                "reject-paths",
                'Cj.Eq(Solution.ProcessField("age", "0"), "reject:age", "0");\nCj.Eq(Solution.ProcessField("score", "101"), "reject:score", "101");\nCj.Eq(Solution.ProcessField("zip", "12345"), "reject:label", "zip");\nCj.Eq(Solution.ProcessField("age", "  "), "reject:empty", "blank");',
                "Range failures name the field; unknown labels fail too; empty wins first.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Trình kiểm chứng trường biểu mẫu",
        "Hiện thực `ProcessField` đúng như checkpoint mô tả. Kiểm tra rỗng trước, rồi label, rồi giá trị.",
        [
            ("happy-paths", "Tuổi hợp lệ và điểm hợp lệ đều được chấp nhận."),
            ("reject-paths", "Thất bại khoảng giá trị gọi tên trường; label lạ cũng từ chối; rỗng thắng trước."),
        ],
    ),
    solution='public class Solution\n{\n    public static string ProcessField(string label, string input)\n    {\n        if (string.IsNullOrWhiteSpace(input)) return "reject:empty";\n        switch (label)\n        {\n            case "age":\n                return int.TryParse(input, out int age) && age >= 1 && age <= 119 ? "accept" : "reject:age";\n            case "score":\n                return int.TryParse(input, out int score) && score >= 0 && score <= 100 ? "accept" : "reject:score";\n            default:\n                return "reject:label";\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public static string ProcessField(string label, string input)\n    {\n        // near-miss: checks the label BEFORE empty, so blank age input\n        // crashes TryParse-less parse path... and reports reject:age, not reject:empty\n        if (label == "age")\n            return int.TryParse(input ?? "", out int age) && age >= 1 && age <= 119 ? "accept" : "reject:age";\n        if (label == "score")\n            return int.TryParse(input ?? "", out int score) && score >= 0 && score <= 100 ? "accept" : "reject:score";\n        return "reject:label";\n    }\n}\n',
)

print("module 3 authored")
