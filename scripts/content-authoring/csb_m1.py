#!/usr/bin/env python3
"""C# — Beginner — Module 1: csb-welcome (hello, runtime, first programs).

House conventions (same as every CJ course): lessons teach the concept and
immediately use it; practice challenges grade named static members of
`public class Solution` or `static void program()` output; Ws are behavioral
near-misses, never syntax errors. Boilerplate carries the usings (raw csc has
no implicit usings — verified by probe).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-welcome"

write_module(
    M,
    "Hello, C#",
    "Meet C# and .NET, write and run your first programs, and learn how Code Journey grades what you write.",
    "Xin chào, C#",
    "Làm quen C# và .NET, viết và chạy những chương trình đầu tiên, và tìm hiểu cách Code Journey chấm điểm code của bạn.",
    ["csb-m1-what-is-csharp", "csb-m1-first-program", "csb-m1-how-grading-works", "csb-checkpoint-m1"],
    ["csb-p1-first-steps"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m1-what-is-csharp",
    "What is C#? What is .NET?",
    "The language, the runtime, and the ecosystem — and why the distinction matters.",
    12,
    r"""
## One language, one platform

**C# is a programming language.** **.NET is a platform**: a runtime that executes programs plus a huge standard library you call into. You write C#; the *platform* runs it. People say "C# developer" and ".NET developer" almost interchangeably — but the concepts are distinct, and interviews test the distinction.

```csharp
using System;

public class Solution
{
    public static void program()
    {
        Console.WriteLine("C# is the language. WriteLine comes from .NET.");
    }
}
```

`Console.WriteLine` is not part of the C# language — it's a method the .NET library provides. The C# compiler (Roslyn) checks your code; the .NET runtime (CoreCLR) executes it.

| Piece | What it is | Example |
|---|---|---|
| C# | the language: syntax, types, rules | `string name = "Ada";` |
| Roslyn | the C# compiler: your code → IL | catches `string x = 5;` |
| .NET runtime | executes the compiled program | runs `Console.WriteLine` |
| .NET libraries | ready-made functionality | `Console`, `Math`, `File`, `List<T>` |

Code Journey grades your C# with the **real .NET SDK** — your code is compiled and executed in a locked-down sandbox, exactly like the platform does in production.

## What C# is used for

C# runs web backends (ASP.NET Core), desktop apps, games (Unity is C#-scripted), and cloud services. All of those rest on the fundamentals this course drills: types, control flow, methods, collections, classes. Frameworks come and go; the fundamentals pay the bill for decades.

## Compiled, not interpreted

When you submit code here, three things happen:

1. **Compile** — Roslyn checks syntax and types, producing an assembly.
2. **Load** — the .NET runtime loads your compiled code.
3. **Run** — each hidden test executes against it and reports pass/fail.

If your code doesn't compile, you get the **compiler's error message** — read it top to bottom; it usually names the exact line and problem. That's not an obstacle; it's the fastest feedback loop in software.
""",
    "C# là gì? .NET là gì?",
    "Ngôn ngữ, nền tảng runtime và hệ sinh thái — vì sao cần phân biệt chúng.",
    r"""
## Một ngôn ngữ, một nền tảng

**C# là ngôn ngữ lập trình.** **.NET là nền tảng**: một runtime thực thi chương trình cùng một thư viện chuẩn khổng lồ để bạn gọi vào. Bạn viết C#; *nền tảng* chạy nó. Người ta nói "lập trình viên C#" và "lập trình viên .NET" gần như thay thế được cho nhau — nhưng hai khái niệm này khác nhau, và phỏng vấn hay hỏi đúng chỗ đó.

```csharp
using System;

public class Solution
{
    public static void program()
    {
        Console.WriteLine("C# là ngôn ngữ. WriteLine đến từ .NET.");
    }
}
```

`Console.WriteLine` không phải một phần của ngôn ngữ C# — đó là một phương thức do thư viện .NET cung cấp. Trình biên dịch C# (Roslyn) kiểm tra code của bạn; runtime .NET (CoreCLR) thực thi nó.

| Thành phần | Là gì | Ví dụ |
|---|---|---|
| C# | ngôn ngữ: cú pháp, kiểu, quy tắc | `string name = "Ada";` |
| Roslyn | trình biên dịch: code → IL | bắt `string x = 5;` |
| .NET runtime | thực thi chương trình đã biên dịch | chạy `Console.WriteLine` |
| Thư viện .NET | chức năng có sẵn | `Console`, `Math`, `File`, `List<T>` |

Code Journey chấm điểm C# của bạn bằng **.NET SDK thật** — code của bạn được biên dịch và thực thi trong sandbox khoá kín, y như hệ thống làm trong môi trường thật.

## C# dùng để làm gì

C# chạy backend web (ASP.NET Core), ứng dụng desktop, game (Unity dùng C#), và dịch vụ cloud. Tất cả đều dựa trên nền tảng mà khoá này luyện: kiểu dữ liệu, luồng điều khiển, phương thức, collection, class. Framework thì đổi đổi rồi lại đổi; nền tảng căn bản trả hoá đơn hàng chục năm.

## Biên dịch, không phải thông dịch

Khi bạn nộp code, ba điều xảy ra:

1. **Biên dịch** — Roslyn kiểm tra cú pháp và kiểu, tạo ra một assembly.
2. **Nạp** — runtime .NET nạp code đã biên dịch.
3. **Chạy** — mỗi test ẩn được thực thi và báo pass/fail.

Nếu code không biên dịch được, bạn nhận **thông báo lỗi của trình biên dịch** — đọc từ trên xuống; nó thường chỉ đúng dòng và đúng vấn đề. Đó không phải trở ngại; đó là vòng phản hồi nhanh nhất trong ngành phần mềm.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m1-first-program",
    "Your first program, line by line",
    "using, class, method, statement — every line of the smallest real program explained.",
    14,
    r"""
## The smallest complete program

```csharp
using System;

public class Solution
{
    public static void program()
    {
        Console.WriteLine("Hello, Code Journey!");
    }
}
```

Every line has a job:

| Line | Job |
|---|---|
| `using System;` | make the `System` namespace's types visible by short name (`Console` lives there) |
| `public class Solution` | declare a class — C# code always lives inside a type |
| `public static void program()` | declare a **method**: a named, reusable block of code |
| `Console.WriteLine(...)` | a **statement** — one instruction; note the semicolon |
| `{ }` | braces group code into blocks |

**Namespaces** are named groups of types — folders for code. `Console` is `System.Console`; `using System;` lets you write just `Console`. Fully-qualified `System.Console.WriteLine(...)` works identically. This course's challenge boilerplate already includes the common `using` lines; you focus on the code inside.

**Strings** are text in double quotes. `"Hello"` is a string literal. Single quotes make a `char` (one character) — `'A'` and `"A"` are different types.

## Output that isn't one line

`Console.Write` prints without a newline; `Console.WriteLine` prints and moves to the next line. Mixing them builds rows:

```csharp
Console.Write("Score: ");
Console.WriteLine(97);        // "Score: 97" on one line
Console.WriteLine();          // empty line
```

**Comments** are for humans; the compiler ignores them:

```csharp
// a single-line comment
/* a block comment
   spanning lines */
```

Write comments for the *why*, not the *what* — the code already says what it does.

## Escape sequences

Some characters need a backslash escape inside strings: `\n` (newline), `\t` (tab), `\"` (quote), `\\` (backslash). `"She said \"hi\"\n"` prints `She said "hi"` and a line break.
""",
    "Chương trình đầu tiên, từng dòng một",
    "using, class, phương thức, câu lệnh — mỗi dòng của chương trình nhỏ nhất được giải thích.",
    r"""
## Chương trình hoàn chỉnh nhỏ nhất

```csharp
using System;

public class Solution
{
    public static void program()
    {
        Console.WriteLine("Xin chào, Code Journey!");
    }
}
```

Mỗi dòng có một nhiệm vụ:

| Dòng | Nhiệm vụ |
|---|---|
| `using System;` | cho phép dùng kiểu trong namespace `System` bằng tên ngắn (`Console` nằm ở đó) |
| `public class Solution` | khai báo một class — code C# luôn nằm trong một kiểu dữ liệu |
| `public static void program()` | khai báo một **phương thức**: khối code có tên, dùng lại được |
| `Console.WriteLine(...)` | một **câu lệnh** — một chỉ thị; chú ý dấu chấm phẩy |
| `{ }` | ngoặc nhón nhóm code thành khối |

**Namespace** là nhóm kiểu có tên — như thư mục cho code. `Console` thực ra là `System.Console`; `using System;` cho bạn viết ngắn gọn `Console`. Viết đủ `System.Console.WriteLine(...)` cũng chạy y hệt. Boilerplate của khoá này đã có sẵn các `using` thông dụng; bạn tập trung vào code bên trong.

**String** là văn bản trong nháy đôi. `"Hello"` là một string literal. Nháy đơn tạo `char` (một ký tự) — `'A'` và `"A"` là hai kiểu khác nhau.

## Xuất ra không chỉ một dòng

`Console.Write` in mà không xuống dòng; `Console.WriteLine` in rồi xuống dòng. Trộn cả hai để dựng từng hàng:

```csharp
Console.Write("Điểm: ");
Console.WriteLine(97);        // "Điểm: 97" trên cùng một dòng
Console.WriteLine();          // dòng trống
```

**Comment** dành cho con người; trình biên dịch bỏ qua:

```csharp
// comment một dòng
/* comment khối
   trải nhiều dòng */
```

Hãy comment **lý do**, không phải **cái gì** — code đã nói ra nó làm gì.

## Escape sequence

Một số ký tự cần dấu gạch chéo ngược trong string: `\n` (xuống dòng), `\t` (tab), `\"` (nháy), `\\` (gạch chéo). `"Cô ấy nói \"chào\"\n"` in ra `Cô ấy nói "chào"` và xuống dòng.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m1-how-grading-works",
    "How challenges are graded",
    "The Solution contract, output capture, and reading a test verdict.",
    10,
    r"""
## The graded contract

Every challenge in this course gives you a **starter file** and grades specific **public members of `Solution`**. Early on that's static methods and a `static void program()` whose printed output is captured and checked:

```csharp
public class Solution
{
    public static void program()
    {
        Console.WriteLine("exactly this");
    }
}
```

A hidden test runs your method, captures everything it prints, and compares. Output is compared **exactly** — punctuation, capitalization, spacing. "Print the sum" means the number, not `The sum is: 7`, unless the task says so. Precision here is practice for real logs, APIs, and file formats.

## Reading a verdict

Each test reports:

- **pass** — your code did exactly what the test asked.
- **fail with a message** — read the message: it says what was expected vs what happened (`expected 7, got 10`).
- **compile error** — your code never ran; fix the compiler output first.

Three debugging habits to build now:

1. **Read the message before changing code.** Guess-editing burns attempts.
2. **Reproduce mentally**: trace the failing case by hand.
3. **Change one thing at a time** — otherwise you can't know what helped.

## What "done" means here

A challenge passes when **all** hidden tests pass. Tests include the edges the prompt calls out — empty input, zero, negatives. Passing the happy case is the *start* of the work, not the end.

The next lesson-by-lesson practice is deliberate: **imitate** (copy the pattern), then **modify**, then **build from a blank file**. That progression is how syntax becomes skill.
""",
    "Cách thử thách được chấm điểm",
    "Hợp đồng Solution, bắt output, và đọc kết quả từng test.",
    r"""
## Hợp đồng được chấm điểm

Mọi thử thách trong khoá này đưa cho bạn một **file khởi đầu** và chấm điểm các **thành viên public cụ thể của `Solution`**. Ở giai đoạn đầu đó là các phương thức static và một `static void program()` mà output in ra được bắt lại để đối chiếu:

```csharp
public class Solution
{
    public static void program()
    {
        Console.WriteLine("chính xác dòng này");
    }
}
```

Một test ẩn chạy phương thức của bạn, bắt mọi thứ nó in ra, rồi so sánh. Output được so **chính xác** — dấu câu, chữ hoa/thường, khoảng trắng. "In tổng" nghĩa là con số, không phải `The sum is: 7`, trừ khi đề bài nói rõ. Sự chính xác này là luyện tập cho log, API và định dạng tệp thật.

## Đọc kết quả

Mỗi test báo:

- **pass** — code của bạn làm đúng điều test yêu cầu.
- **fail kèm thông điệp** — đọc thông điệp: nó nói cái kỳ vọng so với thực tế (`expected 7, got 10`).
- **lỗi biên dịch** — code chưa từng chạy; sửa lỗi compiler trước đã.

Ba thói quen gỡ lỗi cần hình thành ngay:

1. **Đọc thông điệp trước khi sửa code.** Sửa mò chỉ đốt lượt thử.
2. **Tái hiện trong đầu**: chạy tay trường hợp fail.
3. **Mỗi lần đổi một thứ** — nếu không bạn không biết cái nào có hiệu lực.

## "Xong" nghĩa là gì ở đây

Một thử thách pass khi **tất cả** test ẩn đều pass. Test bao gồm cả các trường hợp biên đề bài nêu — input rỗng, số 0, số âm. Pass trường hợp vui là *bắt đầu* công việc, không phải kết thúc.

Nhịp luyện tập theo bài học là chủ ý: **bắt chước** (chép pattern), rồi **sửa đổi**, rồi **dựng từ file trống**. Tiến trình đó biến cú pháp thành kỹ năng.
""",
)

# ---------------------------------------------------------------- practice
PRE = CS_PRELUDE

p_tests_style = [
    (
        "greets-world",
        'string outText = Cj.Capture(() => Solution.program());\nCj.Eq(outText, "Hello, world!\\n", "output");',
        "The output must be exactly `Hello, world!` (with the newline WriteLine adds).",
    ),
]

write_practice(
    M, "csb-p1-first-steps",
    "First steps",
    "Print exact output; compute nothing yet — build the habit of precision.",
    "Những bước đầu",
    "In ra output chính xác; chưa tính toán gì — rèn thói quen chính xác.",
    "csb-m1-how-grading-works",
    20,
    "beginner",
    [
        challenge(
            "csb-p1-greet",
            "Exact greeting",
            "Make `program()` print exactly `Hello, world!` (one line). Every character counts — capital H, comma, exclamation mark.",
            PRE,
            p_tests_style,
            level="imitation",
        ),
        challenge(
            "csb-p1-three-lines",
            "Three-line banner",
            "Make `program()` print exactly three lines: `CJ`, then `Rocks`, then `!!`. Use one WriteLine per line.",
            PRE,
            [
                (
                    "banner-lines",
                    'string outText = Cj.Capture(() => Solution.program());\nCj.Eq(outText, "CJ\\nRocks\\n!!\\n", "output");',
                    "Three lines, in order, each ending with a newline.",
                ),
            ],
            level="imitation",
        ),
        challenge(
            "csb-p1-sum-print",
            "Sum, printed",
            "Inside `program()`, declare two `int` variables with values 19 and 23, then print their sum (just the number).",
            PRE,
            [
                (
                    "sum-is-42",
                    'string outText = Cj.Capture(() => Solution.program());\nCj.Eq(outText, "42\\n", "output");',
                    "Print the number only — no label.",
                ),
            ],
            level="imitation",
        ),
        challenge(
            "csb-p1-write-vs-writeline",
            "One line, two calls",
            "Using exactly ONE `Console.Write` and ONE `Console.WriteLine` (in that order), make `program()` print `A B` on a single line. `Write` prints `A `, `WriteLine` prints `B`.",
            PRE,
            [
                (
                    "single-line",
                    'string outText = Cj.Capture(() => Solution.program());\nCj.Eq(outText, "A B\\n", "output");',
                    "Write does not end the line; WriteLine does.",
                ),
            ],
            level="guided",
        ),
    ],
    {
        "csb-p1-greet": vi_challenge(
            "Lời chào chính xác",
            "Cho `program()` in đúng `Hello, world!` (một dòng). Từng ký tự đều quan trọng — chữ H hoa, dấu phẩy, dấu chấm than.",
            [("greets-world", "Output phải đúng `Hello, world!` (kèm xuống dòng của WriteLine).")],
        ),
        "csb-p1-three-lines": vi_challenge(
            "Banner ba dòng",
            "Cho `program()` in đúng ba dòng: `CJ`, rồi `Rocks`, rồi `!!`. Mỗi dòng một WriteLine.",
            [("banner-lines", "Ba dòng, đúng thứ tự, mỗi dòng kết thúc bằng xuống dòng.")],
        ),
        "csb-p1-sum-print": vi_challenge(
            "Tổng được in ra",
            "Trong `program()`, khai báo hai biến `int` mang giá trị 19 và 23, rồi in tổng của chúng (chỉ con số).",
            [("sum-is-42", "Chỉ in số — không nhãn.")],
        ),
        "csb-p1-write-vs-writeline": vi_challenge(
            "Một dòng, hai lời gọi",
            "Dùng đúng MỘT `Console.Write` và MỘT `Console.WriteLine` (theo thứ tự đó) để `program()` in `A B` trên một dòng. `Write` in `A `, `WriteLine` in `B`.",
            [("single-line", "Write không kết thúc dòng; WriteLine thì có.")],
        ),
    },
    solutions=[
        (
            "csb-p1-greet",
            'public class Solution\n{\n    public static void program()\n    {\n        Console.WriteLine("Hello, world!");\n    }\n}\n',
            'public class Solution\n{\n    public static void program()\n    {\n        // near-miss: lowercase w fails the exact-output test\n        Console.WriteLine("Hello, World!");\n    }\n}\n',
        ),
        (
            "csb-p1-three-lines",
            'public class Solution\n{\n    public static void program()\n    {\n        Console.WriteLine("CJ");\n        Console.WriteLine("Rocks");\n        Console.WriteLine("!!");\n    }\n}\n',
            'public class Solution\n{\n    public static void program()\n    {\n        // near-miss: Write instead of WriteLine merges the lines\n        Console.Write("CJ");\n        Console.WriteLine("Rocks");\n        Console.WriteLine("!!");\n    }\n}\n',
        ),
        (
            "csb-p1-sum-print",
            'public class Solution\n{\n    public static void program()\n    {\n        int a = 19;\n        int b = 23;\n        Console.WriteLine(a + b);\n    }\n}\n',
            'public class Solution\n{\n    public static void program()\n    {\n        int a = 19;\n        int b = 23;\n        // near-miss: prints the arguments side by side, not the sum\n        Console.WriteLine(a);\n        Console.WriteLine(b);\n    }\n}\n',
        ),
        (
            "csb-p1-write-vs-writeline",
            'public class Solution\n{\n    public static void program()\n    {\n        Console.Write("A ");\n        Console.WriteLine("B");\n    }\n}\n',
            'public class Solution\n{\n    public static void program()\n    {\n        // near-miss: WriteLine after Write adds a newline mid-line\n        Console.Write("A ");\n        Console.Write("B\\n");\n        Console.WriteLine();\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m1",
    "Checkpoint — Hello, C#",
    "Prove the Module 1 contract: exact output, structure, and precision.",
    15,
    r"""
## Checkpoint: prove the contract

One task covering the module: exact multi-line output with a computed value. A checkpoint is a pass/fail gate — take it when you can solve it without looking back.

**Task:** implement `program()` so it prints a two-line receipt:
line 1: `CJ SNACKS` (exact),
line 2: the number `total`, where `total` is an `int` variable = 2 × 12 + 5 (declare it and compute it — do not hard-code the answer).
""",
    "Checkpoint — Xin chào, C#",
    "Chứng minh hợp đồng của Module 1: output chính xác, cấu trúc, và sự tỉ mỉ.",
    r"""
## Checkpoint: chứng minh hợp đồng

Một nhiệm vụ bao trùm cả module: output nhiều dòng chính xác kèm giá trị tính được. Checkpoint là cổng pass/fail — hãy làm khi bạn giải được mà không cần nhìn lại.

**Nhiệm vụ:** hiện thực `program()` để in hoá đơn hai dòng:
dòng 1: `CJ SNACKS` (chính xác),
dòng 2: số `total`, trong đó `total` là biến `int` = 2 × 12 + 5 (khai báo biến và tính — đừng ghi cứng kết quả).
""",
    challenge(
        "csb-checkpoint-m1-task",
        "Receipt, precisely",
        "Implement `program()` to print the two-line receipt described in the checkpoint. Line 1: `CJ SNACKS`. Line 2: the computed `total` (2 * 12 + 5) stored in an int variable first.",
        PRE,
        [
            (
                "receipt-exact",
                'string outText = Cj.Capture(() => Solution.program());\nCj.Eq(outText, "CJ SNACKS\\n29\\n", "output");',
                "Two lines: the label exactly, then the computed total.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Hoá đơn, chính xác",
        "Hiện thực `program()` để in hoá đơn hai dòng như checkpoint mô tả. Dòng 1: `CJ SNACKS`. Dòng 2: `total` tính được (2 * 12 + 5), lưu vào biến int trước.",
        [("receipt-exact", "Hai dòng: nhãn chính xác, rồi tổng tính được.")],
    ),
    solution='public class Solution\n{\n    public static void program()\n    {\n        Console.WriteLine("CJ SNACKS");\n        int total = 2 * 12 + 5;\n        Console.WriteLine(total);\n    }\n}\n',
    wrong='public class Solution\n{\n    public static void program()\n    {\n        // near-miss: hard-codes the label result order wrong\n        int total = 2 * 12 + 5;\n        Console.WriteLine(total);\n        Console.WriteLine("CJ SNACKS");\n    }\n}\n',
)

print("module 1 authored")
