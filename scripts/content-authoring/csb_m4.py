#!/usr/bin/env python3
"""C# — Beginner — Module 4: csb-flow (operators, conditions, loops).

Control flow with discriminating tests: short-circuit behavior, switch on
ranges via relational patterns, loop invariants. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-flow"

write_module(
    M,
    "Operators, Conditions, Loops",
    "Make decisions and repeat work: comparison and logic operators, if/switch patterns, and every loop shape.",
    "Toán tử, điều kiện, vòng lặp",
    "Ra quyết định và lặp công việc: toán tử so sánh và logic, if/switch pattern, và mọi dạng vòng lặp.",
    ["csb-m4-operators", "csb-m4-conditions", "csb-m4-loops", "csb-checkpoint-m4"],
    ["csb-p4-flow"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m4-operators",
    "Operators and expressions",
    "Arithmetic, comparison, logic — and the short-circuit rule that changes behavior, not just style.",
    14,
    r"""
## Arithmetic and its surprises

`+ - * / %` on numbers. You know `7 / 2 == 3` (integer division truncates). The `%` **remainder** operator completes the toolkit: `n % 2 == 0` reads "n is even", `minutes % 60` is "minutes past the hour". Watch sign behavior: `-7 % 2` is `-1` in C# — the remainder takes the dividend's sign.

Compound assignment `+= -= *= /=` updates in place: `total += price` is `total = total + price`. `++`/`--` add or subtract one; prefer `i += 1` style clarity in expressions, keep `++` for loops.

## Comparison operators

`== != < > <= >=` produce `bool`. On numeric types they compare values. On `string`, `==` compares contents. On most *classes*, `==` compares **references** — two different objects with equal fields are not `==`. (You'll meet records in Module 13, which fix this for data types.)

## Logic and short-circuiting

`&&` (and), `||` (or), `!` (not) combine bools — and they **short-circuit**:

```csharp
if (count > 0 && total / count > 10) { ... }   // safe: division only when count > 0
if (name != null && name.Length > 0) { ... }   // safe: dereference only after null check
```

The right side of `&&` runs *only when* the left side was true; the right side of `||` only when the left was false. This is not an optimization nicety — it's how you write guarded checks. `&` and `|` (single) exist but always evaluate both sides; you want `&&`/`||` for control flow.

**Precedence**: `!` binds tightest, then arithmetic, then comparisons, then `&&`, then `||`. When in doubt, parenthesize — `a && b || c` is `(a && b) || c`, but nobody should have to remember that.
""",
    "Toán tử và biểu thức",
    "Số học, so sánh, logic — và quy tắc short-circuit thay đổi hành vi, không chỉ phong cách.",
    r"""
## Số học và những bất ngờ

`+ - * / %` trên số. Bạn biết `7 / 2 == 3` (chia số nguyên bị cắt). Toán tử `%` (**số dư**) hoàn thiện bộ công cụ: `n % 2 == 0` nghĩa là "n chẵn", `minutes % 60` là "số phút sau giờ". Chú ý hành vi dấu: `-7 % 2` là `-1` trong C# — số dư mang dấu của số bị chia.

Gán ghép `+= -= *= /=` cập nhật tại chỗ: `total += price` là `total = total + price`. `++`/`--` cộng hoặc trừ một; ưu tiên `i += 1` cho rõ ràng trong biểu thức, giữ `++` cho vòng lặp.

## Toán tử so sánh

`== != < > <= >=` tạo ra `bool`. Trên kiểu số, chúng so giá trị. Trên `string`, `==` so nội dung. Trên hầu hết *class*, `==` so **tham chiếu** — hai đối tượng khác nhau với các trường bằng nhau không phải `==`. (Bạn sẽ gặp records ở Module 13, vốn sửa điều này cho kiểu dữ liệu.)

## Logic và short-circuit

`&&` (và), `||` (hoặc), `!` (phủ định) kết hợp các bool — và chúng có cơ chế **short-circuit**:

```csharp
if (count > 0 && total / count > 10) { ... }   // an toàn: chỉ chia khi count > 0
if (name != null && name.Length > 0) { ... }   // an toàn: chỉ truy cập sau kiểm tra null
```

Vế phải của `&&` chỉ chạy *khi* vế trái đúng; vế phải của `||` chỉ chạy khi vế trái sai. Đây không phải tối ưu hóa trang trí — đó là cách viết kiểm tra có bảo vệ. `&` và `|` (một ký tự) tồn tại nhưng luôn tính cả hai vế; với luồng điều khiển bạn muốn `&&`/`||`.

**Độ ưu tiên**: `!` chặt nhất, rồi số học, rồi so sánh, rồi `&&`, rồi `||`. Khi nghi ngờ, đặt ngoặc — `a && b || c` là `(a && b) || c`, nhưng không ai nên phải nhớ điều đó.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m4-conditions",
    "Conditions: if and switch",
    "Branching with if/else, the ternary operator, and modern switch expressions with patterns.",
    14,
    r"""
## if / else if / else

```csharp
if (temp >= 30)
{
    Console.WriteLine("hot");
}
else if (temp >= 20)
{
    Console.WriteLine("warm");
}
else
{
    Console.WriteLine("cool");
}
```

Conditions are `bool` — never a number. Order matters: the first true branch wins, so ranges must descend (checking `>= 20` before `>= 30` would misclassify). Braces even for one line: future-you adds a second line and the indentation lie becomes a bug.

## Ternary: conditional expressions

```csharp
string label = score >= 50 ? "pass" : "fail";
int max = a > b ? a : b;
```

`condition ? whenTrue : whenFalse` is an *expression* — it produces a value. Use it for simple choices; nested ternaries are where readability goes to die.

## switch expressions with patterns

```csharp
static string Grade(int score) => score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    >= 0 => "F",
    _ => "invalid"
};
```

A switch expression matches the subject against **patterns** — here relational patterns (`>= 90`) — and yields the value after `=>`. Arms are tried top to bottom; `_` is the catch-all. Compared with an if-chain: each arm is a value, the compiler warns when you miss cases it can prove (for enums), and ranges read as data, not control flow. Both forms are idiomatic; switch expressions shine for classification.
""",
    "Điều kiện: if và switch",
    "Rẽ nhánh với if/else, toán tử ternary, và switch expression hiện đại với pattern.",
    r"""
## if / else if / else

```csharp
if (temp >= 30)
{
    Console.WriteLine("nóng");
}
else if (temp >= 20)
{
    Console.WriteLine("mát");
}
else
{
    Console.WriteLine("mát hơn");
}
```

Điều kiện là `bool` — không bao giờ là số. Thứ tự quan trọng: nhánh đúng đầu tiên thắng, nên các khoảng giá trị phải đi từ cao xuống (kiểm tra `>= 20` trước `>= 30` sẽ phân loại sai). Có ngoặc nhọn kể cả một dòng: bạn-tương-lai sẽ thêm dòng thứ hai và lời nói dối thụt lề trở thành bug.

## Ternary: biểu thức điều kiện

```csharp
string label = score >= 50 ? "pass" : "fail";
int max = a > b ? a : b;
```

`điều_kiện ? khi_đúng : khi_sai` là một *biểu thức* — nó tạo ra giá trị. Dùng cho lựa chọn đơn giản; ternary lồng nhau là nơi độ dễ đọc chết.

## switch expression với pattern

```csharp
static string Grade(int score) => score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    >= 0 => "F",
    _ => "invalid"
};
```

Switch expression so khớp giá trị với **pattern** — ở đây là relational pattern (`>= 90`) — và tạo ra giá trị sau `=>`. Các nhánh được thử từ trên xuống; `_` là nhánh gom hết. So với chuỗi if: mỗi nhánh là một giá trị, compiler cảnh báo khi bạn bỏ sót case mà nó chứng minh được (với enum), và các khoảng giá trị đọc như dữ liệu chứ không phải luồng điều khiển. Cả hai dạng đều idiomatic; switch expression tỏa sáng khi phân loại.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m4-loops",
    "Loops: for, while, do, foreach",
    "Four shapes, four jobs — plus break, continue, and how loops accumulate.",
    15,
    r"""
## The four shapes

```csharp
for (int i = 0; i < 5; i++) { ... }        // counted: known number of passes
while (queue.Count > 0) { ... }            // pre-test: maybe zero passes
do { ... } while (again);                  // post-test: at least one pass
foreach (string name in names) { ... }     // walk a collection
```

- **for** owns its counter — best when the count is known or derivable.
- **while** tests first — zero iterations is normal.
- **do/while** runs the body first — menus and input loops ("ask at least once").
- **foreach** reads any collection element-by-element — no index, no off-by-one. (Use `for` when you must know *where* you are.)

## Accumulation: the loop's inner state

Every statistics tool is a loop with state:

```csharp
int total = 0;
for (int i = 1; i <= 100; i++)
{
    total += i;          // state updated once per pass
}
// total == 5050
```

Initialize the accumulator *before* the loop, update it *inside*, read it *after*. Declaring the accumulator inside the loop is the classic beginner bug — it resets every pass.

## break and continue

`break` exits the loop now; `continue` skips to the next pass. Use both sparingly — a `for` with a clear condition plus an occasional `break` for "found it" reads fine; a maze of breaks signals the loop wants restructuring.

## Off-by-one discipline

`i < n` visits n items (indices 0..n-1); `i <= n` visits n+1. Arrays and strings are 0-indexed: a 5-item array's last index is 4. When a loop crashes with `IndexOutOfRangeException`, look at the boundary first.
""",
    "Vòng lặp: for, while, do, foreach",
    "Bốn dạng, bốn nhiệm vụ — cộng break, continue, và cách vòng lặp tích lũy.",
    r"""
## Bốn dạng

```csharp
for (int i = 0; i < 5; i++) { ... }        // đếm được: số lượt đã biết
while (queue.Count > 0) { ... }            // kiểm tra trước: có thể chạy 0 lượt
do { ... } while (again);                  // kiểm tra sau: chạy ít nhất một lượt
foreach (string name in names) { ... }     // đi qua một collection
```

- **for** sở hữu biến đếm — hợp khi số lượt đã biết hoặc suy ra được.
- **while** kiểm tra trước — chạy 0 lượt là bình thường.
- **do/while** chạy thân trước — menu và vòng nhập liệu ("hỏi ít nhất một lần").
- **foreach** đọc từng phần tử của collection — không cần chỉ số, không lệch một. (Dùng `for` khi bạn cần biết mình đang *ở đâu*.)

## Tích lũy: trạng thái bên trong vòng lặp

Mọi công cụ thống kê là một vòng lặp có trạng thái:

```csharp
int total = 0;
for (int i = 1; i <= 100; i++)
{
    total += i;          // trạng thái cập nhật mỗi lượt
}
// total == 5050
```

Khởi tạo biến tích lũy *trước* vòng lặp, cập nhật *bên trong*, đọc *sau*. Khai báo biến tích lũy bên trong vòng lặp là bug kinh điển của người mới — nó bị đặt lại mỗi lượt.

## break và continue

`break` thoát vòng lặp ngay; `continue` bỏ qua phần còn lại, sang lượt kế. Dùng cả hai tiết chế — một `for` với điều kiện rõ cộng thêm một `break` kiểu "tìm thấy rồi" vẫn đọc tốt; một mê cung các break báo hiệu vòng lặp cần tái cấu trúc.

## Kỷ luật lệch-một

`i < n` thăm n phần tử (chỉ số 0..n-1); `i <= n` thăm n+1. Mảng và chuỗi đánh số từ 0: mảng 5 phần tử có chỉ số cuối là 4. Khi vòng lặp nổ `IndexOutOfRangeException`, hãy nhìn vào biên giới trước.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p4-flow",
    "Flow under pressure",
    "Short-circuit guards, range classification, loop accumulation — each tested on its boundaries.",
    "Luồng điều khiển dưới áp lực",
    "Bảo vệ short-circuit, phân loại theo khoảng, tích lũy trong vòng lặp — mỗi bài được test tại biên.",
    "csb-m4-loops",
    35,
    "beginner",
    [
        challenge(
            "csb-p4-safe-average",
            "Safe average",
            "Implement `static double SafeAverage(int[] values)` — the mean of the array, or `0` when the array is null or empty. One short-circuit guard makes this division-safe.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Near(Solution.SafeAverage(new[] {2, 4, 9}), 5.0, 1e-9, \"[2,4,9]\");\nCj.Near(Solution.SafeAverage(new[] {5}), 5.0, 1e-9, \"[5]\");",
                    "Mean of a normal array.",
                ),
                (
                    "guarded",
                    "Cj.Near(Solution.SafeAverage(new int[0]), 0, 1e-9, \"empty\");\nCj.Near(Solution.SafeAverage(null), 0, 1e-9, \"null\");",
                    "Empty and null must return 0 — no crash.",
                ),
            ],
            level="imitation",
        ),
        challenge(
            "csb-p4-bmi-class",
            "BMI classifier",
            "Implement `static string Bmi(double weightKg, double heightM)` returning the BMI category: compute `weight / (height*height)`; return `\"under\"` below 18.5, `\"normal\"` from 18.5 to below 25, `\"over\"` from 25 to below 30, `\"obese\"` at 30 or above.",
            CS_PRELUDE,
            [
                (
                    "bands",
                    'Cj.Eq(Solution.Bmi(50, 1.70), "under", "50/1.7");\nCj.Eq(Solution.Bmi(70, 1.70), "normal", "70/1.7");\nCj.Eq(Solution.Bmi(85, 1.70), "over", "85/1.7");\nCj.Eq(Solution.Bmi(100, 1.70), "obese", "100/1.7");',
                    "One value per band — boundaries matter.",
                ),
                (
                    "boundary-25",
                    "Cj.Eq(Solution.Bmi(74, 2.0), \"normal\", \"exactly 18.5\");\nCj.Eq(Solution.Bmi(100, 2.0), \"over\", \"exactly 25\");\nCj.Eq(Solution.Bmi(120, 2.0), \"obese\", \"exactly 30\");",
                    "Height 2.0 makes the boundaries exact in double arithmetic: 18.5 is \"normal\", 25.0 is \"over\", 30.0 is \"obese\".",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p4-fizzbuzz",
            "FizzBuzz, but rigorous",
            "Implement `static string FizzBuzz(int n)` — for 1..n append lines: multiples of 3 → `Fizz`, of 5 → `Buzz`, of both → `FizzBuzz`, else the number. Each line ends with `\\n` (including the last). n = 0 returns `\"\"`.",
            CS_PRELUDE,
            [
                (
                    "fifteen",
                    'Cj.Eq(Solution.FizzBuzz(5), "1\\n2\\nFizz\\n4\\nBuzz\\n", "1..5");\nCj.Eq(Solution.FizzBuzz(15).EndsWith("FizzBuzz\\n"), true, "ends 15");',
                    "Order: check divisible-by-both FIRST.",
                ),
                (
                    "edges",
                    'Cj.Eq(Solution.FizzBuzz(0), "", "zero");\nCj.Eq(Solution.FizzBuzz(1), "1\\n", "one");',
                    "Zero produces nothing; one line still ends with newline.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p4-digit-sum",
            "Digit sum loop",
            "Implement `static int DigitSum(int n)` — sum of the decimal digits of n's absolute value. `DigitSum(0)` is 0; `DigitSum(-907)` is 16. No string conversion: use `%` and `/` in a loop.",
            CS_PRELUDE,
            [
                (
                    "positives",
                    'Cj.Eq(Solution.DigitSum(0), 0, "0");\nCj.Eq(Solution.DigitSum(5), 5, "5");\nCj.Eq(Solution.DigitSum(1234), 10, "1234");',
                    "Single digit and multi digit.",
                ),
                (
                    "negative",
                    'Cj.Eq(Solution.DigitSum(-907), 16, "-907");',
                    "Absolute value first: 9+0+7.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p4-safe-average": vi_challenge(
            "Trung bình an toàn",
            "Hiện thực `static double SafeAverage(int[] values)` — trung bình của mảng, hoặc `0` khi mảng null hoặc rỗng. Một bảo vệ short-circuit là đủ để không chia cho 0.",
            [
                ("normal", "Trung bình của mảng thường."),
                ("guarded", "Rỗng và null phải trả 0 — không được nổ."),
            ],
        ),
        "csb-p4-bmi-class": vi_challenge(
            "Phân loại BMI",
            "Hiện thực `static string Bmi(double weightKg, double heightM)` trả nhóm BMI: tính `weight / (height*height)`; trả `\"under\"` dưới 18.5, `\"normal\"` từ 18.5 đến dưới 25, `\"over\"` từ 25 đến dưới 30, `\"obese\"` từ 30 trở lên.",
            [
                ("bands", "Mỗi giá trị cho một nhóm — biên rất quan trọng."),
                ("boundary-25", "Chiều cao 2.0 làm biên chính xác: 18.5 thuộc \"normal\", 25.0 thuộc \"over\", 30.0 thuộc \"obese\"."),
            ],
        ),
        "csb-p4-fizzbuzz": vi_challenge(
            "FizzBuzz, nhưng nghiêm ngặt",
            "Hiện thực `static string FizzBuzz(int n)` — với 1..n nối từng dòng: chia hết cho 3 → `Fizz`, cho 5 → `Buzz`, cho cả hai → `FizzBuzz`, còn lại in số. Mỗi dòng kết thúc `\\n` (kể cả dòng cuối). n = 0 trả `\"\"`.",
            [
                ("fifteen", "Thứ tự: kiểm tra chia-hết-cho-cả-hai TRƯỚC."),
                ("edges", "Số 0 không tạo dòng gì; một dòng vẫn kết thúc bằng newline."),
            ],
        ),
        "csb-p4-digit-sum": vi_challenge(
            "Tổng chữ số bằng vòng lặp",
            "Hiện thực `static int DigitSum(int n)` — tổng các chữ số thập phân của giá trị tuyệt đối của n. `DigitSum(0)` là 0; `DigitSum(-907)` là 16. Không dùng chuyển chuỗi: dùng `%` và `/` trong vòng lặp.",
            [
                ("positives", "Một chữ số và nhiều chữ số."),
                ("negative", "Lấy trị tuyệt đối trước: 9+0+7."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p4-safe-average",
            'public class Solution\n{\n    public static double SafeAverage(int[] values)\n    {\n        if (values == null || values.Length == 0) return 0;\n        long sum = 0;\n        foreach (int v in values) sum += v;\n        return (double)sum / values.Length;\n    }\n}\n',
            'public class Solution\n{\n    public static double SafeAverage(int[] values)\n    {\n        // near-miss: checks null with | (non-short-circuit) — evaluates\n        // values.Length on the null path too\n        if (values == null | values.Length == 0) return 0;\n        long sum = 0;\n        foreach (int v in values) sum += v;\n        return (double)sum / values.Length;\n    }\n}\n',
        ),
        (
            "csb-p4-bmi-class",
            'public class Solution\n{\n    public static string Bmi(double weightKg, double heightM)\n    {\n        double bmi = weightKg / (heightM * heightM);\n        return bmi switch\n        {\n            < 18.5 => "under",\n            < 25 => "normal",\n            < 30 => "over",\n            _ => "obese"\n        };\n    }\n}\n',
            'public class Solution\n{\n    public static string Bmi(double weightKg, double heightM)\n    {\n        double bmi = weightKg / (heightM * heightM);\n        // near-miss: <= 25 misclassifies exactly-25 into "normal"\n        return bmi switch\n        {\n            < 18.5 => "under",\n            <= 25 => "normal",\n            < 30 => "over",\n            _ => "obese"\n        };\n    }\n}\n',
        ),
        (
            "csb-p4-fizzbuzz",
            'public class Solution\n{\n    public static string FizzBuzz(int n)\n    {\n        var sb = new System.Text.StringBuilder();\n        for (int i = 1; i <= n; i++)\n        {\n            if (i % 15 == 0) sb.Append("FizzBuzz\\n");\n            else if (i % 3 == 0) sb.Append("Fizz\\n");\n            else if (i % 5 == 0) sb.Append("Buzz\\n");\n            else sb.Append(i).Append(\'\\n\');\n        }\n        return sb.ToString();\n    }\n}\n',
            'public class Solution\n{\n    public static string FizzBuzz(int n)\n    {\n        var sb = new System.Text.StringBuilder();\n        for (int i = 1; i <= n; i++)\n        {\n            // near-miss: checks 3 first, so 15 prints Fizz, never FizzBuzz\n            if (i % 3 == 0) sb.Append("Fizz\\n");\n            else if (i % 5 == 0) sb.Append("Buzz\\n");\n            else sb.Append(i).Append(\'\\n\');\n        }\n        return sb.ToString();\n    }\n}\n',
        ),
        (
            "csb-p4-digit-sum",
            'public class Solution\n{\n    public static int DigitSum(int n)\n    {\n        n = Math.Abs(n);\n        int sum = 0;\n        while (n > 0)\n        {\n            sum += n % 10;\n            n /= 10;\n        }\n        return sum;\n    }\n}\n',
            'public class Solution\n{\n    public static int DigitSum(int n)\n    {\n        n = Math.Abs(n);\n        int sum = 0;\n        while (n > 0)\n        {\n            sum += n % 10;\n            // near-miss: forgets to shrink n — infinite loop, test times out\n            n = n;\n        }\n        return sum;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m4",
    "Checkpoint — Control flow",
    "Guarded computation, classification, and accumulation in one sitting.",
    20,
    r"""
## Checkpoint: the grade report

**Task:** implement two methods:

1. `static char Letter(int score)` — `A` for ≥90, `B` ≥80, `C` ≥70, `D` ≥60, `F` below; throw `ArgumentException` for scores outside 0–100.
2. `static string Histogram(int[] scores)` — one line per letter `A`..`F` in that order: the letter, `: `, then one `#` per score in that bucket, then `\n`. Scores out of 0–100 are ignored. Null/empty input yields `""`... except the histogram always prints all five lines, so empty input prints the five letters with zero `#` each.
""",
    "Checkpoint — Luồng điều khiển",
    "Tính toán có bảo vệ, phân loại, và tích lũy trong một lần ngồi.",
    r"""
## Checkpoint: báo cáo điểm

**Nhiệm vụ:** hiện thực hai phương thức:

1. `static char Letter(int score)` — `A` cho ≥90, `B` ≥80, `C` ≥70, `D` ≥60, `F` dưới đó; ném `ArgumentException` cho điểm ngoài 0–100.
2. `static string Histogram(int[] scores)` — mỗi dòng cho từng chữ `A`..`F` theo thứ tự: chữ cái, `: `, rồi một `#` cho mỗi điểm trong nhóm đó, rồi `\n`. Điểm ngoài 0–100 bị bỏ qua. Input null/rỗng vẫn in đủ năm dòng chữ với 0 `#`.
""",
    challenge(
        "csb-checkpoint-m4-task",
        "Grade report",
        "Implement `Letter` and `Histogram` as described. `Histogram` always prints five lines A..F; each line is `X: ` + `#` * count + newline.",
        CS_PRELUDE,
        [
            (
                "letters",
                'Cj.Eq(Solution.Letter(95), \'A\', "95");\nCj.Eq(Solution.Letter(60), \'D\', "60");\nCj.Eq(Solution.Letter(0), \'F\', "0");\nbool threw = false;\ntry { Solution.Letter(101); } catch (ArgumentException) { threw = true; }\nCj.True(threw, "101 throws");',
                "Boundaries inclusive; out-of-range throws.",
            ),
            (
                "histogram",
                'Cj.Eq(Solution.Histogram(new[] {95, 82, 71, 64, 30}), "A: #\\nB: #\\nC: #\\nD: #\\nF: #\\n", "spread");\nCj.Eq(Solution.Histogram(new int[0]), "A: \\nB: \\nC: \\nD: \\nF: \\n", "empty");\nCj.Eq(Solution.Histogram(null), "A: \\nB: \\nC: \\nD: \\nF: \\n", "null");\nCj.Eq(Solution.Histogram(new[] {95, -5, 82, 101}), "A: #\\nB: #\\nC: \\nD: \\nF: \\n", "skips out-of-range");',
                "Five fixed lines; empty buckets print the letter with no hashes. Out-of-range scores are ignored, not thrown into a bucket.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Báo cáo điểm",
        "Hiện thực `Letter` và `Histogram` như mô tả. `Histogram` luôn in năm dòng A..F; mỗi dòng là `X: ` + `#` * số lượng + newline.",
        [
            ("letters", "Biên bao gồm cả hai đầu; ngoài khoảng thì ném."),
            ("histogram", "Năm dòng cố định; nhóm rỗng in chữ cái không có hash. Điểm ngoài 0–100 bị bỏ qua."),
        ],
    ),
    solution='public class Solution\n{\n    public static char Letter(int score)\n    {\n        if (score < 0 || score > 100) throw new ArgumentException("score out of range");\n        return score >= 90 ? \'A\' : score >= 80 ? \'B\' : score >= 70 ? \'C\' : score >= 60 ? \'D\' : \'F\';\n    }\n\n    public static string Histogram(int[] scores)\n    {\n        int[] buckets = new int[5];\n        if (scores != null)\n        {\n            foreach (int s in scores)\n            {\n                if (s < 0 || s > 100) continue;\n                buckets[s >= 90 ? 0 : s >= 80 ? 1 : s >= 70 ? 2 : s >= 60 ? 3 : 4]++;\n            }\n        }\n        char[] letters = { \'A\', \'B\', \'C\', \'D\', \'F\' };\n        var sb = new System.Text.StringBuilder();\n        for (int i = 0; i < 5; i++) sb.Append(letters[i]).Append(": ").Append(\'#\', buckets[i]).Append(\'\\n\');\n        return sb.ToString();\n    }\n}\n',
    wrong='public class Solution\n{\n    public static char Letter(int score)\n    {\n        if (score < 0 || score > 100) throw new ArgumentException("score out of range");\n        return score >= 90 ? \'A\' : score >= 80 ? \'B\' : score >= 70 ? \'C\' : score >= 60 ? \'D\' : \'F\';\n    }\n\n    public static string Histogram(int[] scores)\n    {\n        int[] buckets = new int[5];\n        if (scores != null)\n        {\n            foreach (int s in scores)\n            {\n                // near-miss: forgot to skip out-of-range scores — negative\n                // scores land in the F bucket and 101 throws away the mapping\n                buckets[s >= 90 ? 0 : s >= 80 ? 1 : s >= 70 ? 2 : s >= 60 ? 3 : 4]++;\n            }\n        }\n        char[] letters = { \'A\', \'B\', \'C\', \'D\', \'F\' };\n        var sb = new System.Text.StringBuilder();\n        for (int i = 0; i < 5; i++) sb.Append(letters[i]).Append(": ").Append(\'#\', buckets[i]).Append(\'\\n\');\n        return sb.ToString();\n    }\n}\n',
)

print("module 4 authored")
