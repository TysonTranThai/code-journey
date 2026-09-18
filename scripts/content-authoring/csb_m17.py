#!/usr/bin/env python3
"""C# — Beginner — Module 17: csb-testing.

Reading failures instead of fearing them: compiler errors vs runtime
errors vs logic bugs, assertions as executable specifications, edge-case
thinking. House conventions: Ws are behavioral near-misses, tests
discriminate.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-testing"

write_module(
    M,
    "Debugging and Testing",
    "Turn failures into information: read the error, isolate the bug, and pin the fix with an executable test.",
    "Gỡ lỗi và Kiểm thử",
    "Biến thất bại thành thông tin: đọc lỗi, cô lập bug, và ghim bản sửa bằng một bài kiểm tra chạy được.",
    ["csb-m17-read-errors", "csb-m17-assertions", "csb-m17-edge-cases", "csb-checkpoint-m17"],
    ["csb-p17-testing"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m17-read-errors",
    "Three species of failure",
    "Compile errors are the compiler protecting you; runtime errors crash; logic bugs pass silently. Different tools for each.",
    13,
    r"""
## Compile-time: the friendly ones

```csharp
int x = "hello";        // CS0029: cannot convert
Missing.Method();       // CS0103: does not exist
```

The compiler refuses to build wrong code and names the file, line, and reason. Fix immediately, before running anything — these are the cheapest failures you will ever see.

## Runtime: exceptions

```csharp
var list = new List<int>();
int first = list[0];    // ArgumentOutOfRangeException: index -1? no: 0, Count 0
```

The program compiles but hits an impossible state. The **stack trace** is the treasure: read it bottom-up — the top frame names the throwing line, the frames below name how you got there.

## Logic bugs: the dangerous ones

```csharp
// compiles, runs, and confidently returns the WRONG answer
static double Average(List<int> xs) => xs.Sum() / xs.Count;   // int division!
```

No exception, no crash — just `Average(new[] {3, 4}) == 3`. Only tests (or a suspicious user) find these. That's why this module is really about building the habit: **assert what you believe**.
""",
    "Ba loài thất bại",
    "Lỗi biên dịch là trình biên dịch bảo vệ bạn; lỗi lúc chạy làm sập; bug logic lặng lẽ đi qua. Mỗi loại một công cụ.",
    r"""
## Lúc biên dịch: những lỗi thân thiện

```csharp
int x = "hello";        // CS0029: không chuyển đổi được
Missing.Method();       // CS0103: không tồn tại
```

Trình biên dịch từ chối dựng mã sai và nêu tên tệp, dòng, và lý do. Sửa ngay trước khi chạy bất cứ gì — đây là những thất bại rẻ nhất bạn từng gặp.

## Lúc chạy: ngoại lệ

```csharp
var list = new List<int>();
int first = list[0];    // ArgumentOutOfRangeException: Count = 0
```

Chương trình biên dịch được nhưng chạm trạng thái bất khả thi. **Stack trace** là kho báu: đọc từ dưới lên — khung trên cùng nêu dòng ném ngoại lệ, các khung dưới nêu đường đi tới đó.

## Bug logic: loài nguy hiểm

```csharp
// biên dịch được, chạy được, và tự tin trả lời SAI
static double Average(List<int> xs) => xs.Sum() / xs.Count;   // chia nguyên!
```

Không ngoại lệ, không sập — chỉ là `Average(new[] {3, 4}) == 3`. Chỉ kiểm thử (hoặc một người dùng hoài nghi) tìm ra chúng. Vì vậy bài học thật của bài này: **khẳng định điều bạn tin**.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m17-assertions",
    "Assertions as executable specs",
    "A test is a sentence about behavior the machine checks forever: Arrange, Act, Assert.",
    13,
    r"""
## The pattern

```csharp
// Arrange: build the world
var items = new List<int> { 3, 1, 2 };
// Act: one behavior
items.Sort();
// Assert: the claim
// items should be 1,2,3
```

A test has one job: prove one claim about one behavior. When it fails, the message should name the claim, the actual value, and the expected value — that trio is what makes failures diagnosable at a glance.

## Good tests share three traits

- **Fast** — milliseconds, so nobody skips running them.
- **Deterministic** — same input, same result, every run. No clocks, no randomness, no "sometimes fails".
- **Isolated** — each test builds its own world; no test depends on another having run first.

The habit this course drills: when a bug appears, don't just fix it — **write the test that would have caught it**, then fix. The test is the regression guard; the fix is temporary without it.
""",
    "Khẳng định như đặc tả chạy được",
    "Một bài kiểm tra là một câu về hành vi mà máy kiểm tra mãi mãi: Arrange, Act, Assert.",
    r"""
## Mẫu hình

```csharp
// Arrange: dựng thế giới
var items = new List<int> { 3, 1, 2 };
// Act: một hành vi
items.Sort();
// Assert: lời khẳng định
// items phải là 1,2,3
```

Một bài kiểm tra có đúng một nhiệm vụ: chứng minh một lời khẳng định về một hành vi. Khi nó thất bại, thông điệp phải nêu lời khẳng định, giá trị thực tế, và giá trị kỳ vọng — bộ ba đó khiến thất bại chẩn đoán được ngay.

## Kiểm thử tốt có ba đặc tính

- **Nhanh** — tính bằng mili-giây, để không ai bỏ qua việc chạy.
- **Xác định** — cùng đầu vào, cùng kết quả, mọi lần chạy. Không đồng hồ, không ngẫu nhiên, không "đôi khi thất bại".
- **Độc lập** — mỗi bài tự dựng thế giới của mình; không bài nào phụ thuộc bài khác đã chạy trước.

Thói quen mà khóa học rèn: khi một bug xuất hiện, đừng chỉ sửa — **hãy viết bài kiểm tra lẽ ra đã bắt được nó**, rồi sửa. Bài kiểm tra là hàng rào chống tái phát; bản sửa không có nó chỉ là tạm thời.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m17-edge-cases",
    "Edge cases and boundary thinking",
    "Bugs live at the edges: empty, null, one, many, boundaries, and the values you didn't think of.",
    12,
    r"""
## The edge taxonomy

For any function ask: what about —

- **Empty** — no elements at all?
- **Null** — the absence of a collection, not the same as empty?
- **One** — a single element?
- **Many** — does it still work at scale?
- **Boundary** — exactly at the limit (`<=` vs `<` bugs live here)?
- **Weird** — duplicates, negative numbers, unicode, whitespace?

```csharp
// the classic boundary bug
static bool IsAdult(int age) => age > 18;   // an 18-year-old disagrees!
```

Off-by-one errors concentrate at boundaries. When the spec says "18 or older", write the test for exactly 18 **first**.

## Test both directions

An incorrect solution must *fail* — that's what makes a test a test. For every claim, the two-sided habit: a case where correct code passes, and a near-miss implementation that must not. A test suite where anything passes proves nothing.
""",
    "Edge case và tư duy biên",
    "Bug sinh sống ở rìa: rỗng, null, một, nhiều, biên, và những giá trị bạn không nghĩ tới.",
    r"""
## Phân loại rìa

Với bất kỳ hàm nào, hãy hỏi: thế còn —

- **Rỗng** — không có phần tử nào?
- **Null** — sự vắng mặt của bộ sưu tập, không giống rỗng?
- **Một** — phần tử đơn lẻ?
- **Nhiều** — có còn hoạt động ở quy mô lớn?
- **Biên** — đúng tại giới hạn (bug `<=` vs `<` sống ở đây)?
- **Lạ** — trùng lặp, số âm, unicode, khoảng trắng?

```csharp
// bug biên kinh điển
static bool IsAdult(int age) => age > 18;   // người 18 tuổi không đồng ý!
```

Lỗi lệch-một tập trung ở biên. Khi đặc tả nói "18 tuổi trở lên", hãy viết bài kiểm tra cho đúng 18 **trước tiên**.

## Kiểm tra cả hai chiều

Một giải pháp sai phải *thất bại* — đó là điều khiến một bài kiểm tra xứng đáng là kiểm tra. Với mọi lời khẳng định, thói quen hai chiều: một trường hợp mã đúng phải qua, và một cài đặt sát-nhưng-sai không được qua. Một bộ kiểm tra mà cái gì cũng qua thì không chứng minh điều gì.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p17-testing",
    "Debugging workout",
    "Diagnose broken helpers, fix boundary bugs, and write the discriminating tests yourself.",
    "Luyện tập gỡ lỗi",
    "Chẩn đoán helper hỏng, sửa bug biên, và tự viết các bài kiểm tra phân biệt.",
    "csb-m17-edge-cases",
    40,
    "beginner",
    [
        challenge(
            "csb-p17-boundary",
            "Boundary contract",
            "Implement `static bool IsAdult(int age)` — true for 18 and above (throws `ArgumentOutOfRangeException` for negative ages) — and `static string Grade(int score)` mapping 90+ → \"A\", 80–89 → \"B\", 70–79 → \"C\", 60–69 → \"D\", below 60 → \"F\" (each boundary inclusive at the bottom of its band; score outside 0–100 → `ArgumentOutOfRangeException`).",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.True(Solution.IsAdult(18), \"exactly 18\");\nCj.True(Solution.IsAdult(25), \"adult\");\nCj.False(Solution.IsAdult(17), \"still minor\");\nCj.Eq(Solution.Grade(90), \"A\", \"A starts at 90\");\nCj.Eq(Solution.Grade(89), \"B\", \"89 is B\");\nCj.Eq(Solution.Grade(60), \"D\", \"D starts at 60\");\nCj.Eq(Solution.Grade(59), \"F\", \"59 is F\");",
                    "Every band edge is asserted — both sides of each boundary.",
                ),
                (
                    "rejects",
                    "bool t1 = false;\ntry { Solution.IsAdult(-1); } catch (ArgumentOutOfRangeException) { t1 = true; }\nbool t2 = false;\ntry { Solution.Grade(101); } catch (ArgumentOutOfRangeException) { t2 = true; }\nbool t3 = false;\ntry { Solution.Grade(-5); } catch (ArgumentOutOfRangeException) { t3 = true; }\nCj.True(t1 && t2 && t3, \"out-of-range inputs rejected\");\nCj.Eq(Solution.Grade(0), \"F\", \"0 is a legal F\");",
                    "Rejects are explicit; the legal extremes still classify.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p17-diagnose",
            "Diagnose the off-by-one",
            "Implement `static int SumRange(int inclusive, int exclusive)` (sum of inclusive..exclusive-1; empty range → 0) and `static int Clamp(int value, int min, int max)` (value pinned into [min, max]; `ArgumentException` when min > max). Both contracts are boundary-sensitive by design.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.SumRange(1, 5), 10, \"1+2+3+4\");\nCj.Eq(Solution.SumRange(5, 5), 0, \"empty range\");\nCj.Eq(Solution.SumRange(-3, 2), -5, \"negatives sum too\");\nCj.Eq(Solution.Clamp(5, 0, 10), 5, \"inside\");\nCj.Eq(Solution.Clamp(-5, 0, 10), 0, \"floored\");\nCj.Eq(Solution.Clamp(15, 0, 10), 10, \"ceilinged\");",
                    "Exclusive upper bound and both clamp edges.",
                ),
                (
                    "bounds",
                    "bool t = false;\ntry { Solution.Clamp(5, 10, 0); } catch (ArgumentException) { t = true; }\nCj.True(t, \"inverted min/max rejected\");\nCj.Eq(Solution.Clamp(5, 5, 5), 5, \"degenerate range holds value\");",
                    "The degenerate case [5,5] is legal; the inverted one is not.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p17-firstdistinct",
            "Write the discriminating test",
            "Implement `static int FirstDistinct(int[] nums)` — the first element that differs from all previous ones (nums[0] never qualifies); -1 when none. Then the graded part: your own test group must include a case distinguishing \"first distinct\" from \"any distinct\" and a case for the all-equal array.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.FirstDistinct(new[] { 1, 1, 2, 1 }), 2, \"2 is first different\");\nCj.Eq(Solution.FirstDistinct(new[] { 5, 5, 5 }), -1, \"all equal\");\nCj.Eq(Solution.FirstDistinct(new[] { 7 }), -1, \"single element: nothing previous to differ from\");\nCj.Eq(Solution.FirstDistinct(new[] { 3, 1 }), 1, \"second element differs from first\");",
                    "The reference implementation and its discriminating cases.",
                ),
                (
                    "discriminator",
                    "Cj.Eq(Solution.FirstDistinct(new[] { 2, 2, 2, 9, 1 }), 9, \"first distinct, not min distinct\");\nCj.Eq(Solution.FirstDistinct(new int[0]), -1, \"empty\");",
                    "9 qualifies before 1 — an \"any distinct\" bug would answer 1.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p17-floats",
            "Floating-point honesty",
            "Implement `static bool SameTotal(decimal a, decimal b, decimal tolerance)` — true when |a−b| ≤ tolerance — and `static double Mean(List<double> xs)` returning the average (empty/null → 0.0). Tests pin exact-decimal behavior and tolerance logic.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.True(Solution.SameTotal(100.0m, 100.0m, 0.0m), \"exact equal\");\nCj.True(Solution.SameTotal(100.05m, 100.0m, 0.1m), \"within tolerance\");\nCj.False(Solution.SameTotal(100.2m, 100.0m, 0.1m), \"outside tolerance\");\nCj.Near(Solution.Mean(new List<double> { 1.0, 2.0, 3.0 }), 2.0, 1e-9, \"mean\");",
                    "Tolerance comparisons and a clean mean — decimal money, double statistics.",
                ),
                (
                    "edges",
                    "Cj.Eq(Solution.Mean(new List<double>()), 0.0, \"empty mean\");\nCj.Eq(Solution.Mean(null), 0.0, \"null mean\");\nCj.True(Solution.SameTotal(-1.0m, -1.0m, 0.0m), \"negative exact\");\nCj.True(Solution.SameTotal(0.05m, 0.0m, 0.05m), \"boundary tolerance inclusive\");",
                    "Empty contracts and the inclusive-tolerance boundary.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p17-boundary": vi_challenge(
            "Hợp đồng biên",
            "Hiện thực `static bool IsAdult(int age)` — true từ 18 trở lên (ném `ArgumentOutOfRangeException` với tuổi âm) — và `static string Grade(int score)` ánh xạ 90+ → \"A\", 80–89 → \"B\", 70–79 → \"C\", 60–69 → \"D\", dưới 60 → \"F\" (mỗi biên bao gồm đáy của dải; điểm ngoài 0–100 → `ArgumentOutOfRangeException`).",
            [
                ("normal", "Mọi mép dải đều được khẳng định — cả hai phía của từng biên."),
                ("rejects", "Từ chối là tường minh; các cực hợp lệ vẫn được phân loại."),
            ],
        ),
        "csb-p17-diagnose": vi_challenge(
            "Chẩn đoán lỗi lệch-một",
            "Hiện thực `static int SumRange(int inclusive, int exclusive)` (tổng inclusive..exclusive-1; khoảng rỗng → 0) và `static int Clamp(int value, int min, int max)` (ghim value vào [min, max]; ném `ArgumentException` khi min > max). Cả hai hợp đồng đều nhạy-cảm-biên có chủ đích.",
            [
                ("normal", "Chặn trên loại-trừ và cả hai mép của clamp."),
                ("bounds", "Trường hợp suy biến [5,5] là hợp lệ; khoảng đảo ngược thì không."),
            ],
        ),
        "csb-p17-firstdistinct": vi_challenge(
            "Tự viết bài kiểm tra phân biệt",
            "Hiện thực `static int FirstDistinct(int[] nums)` — phần tử đầu khác với TẤT CẢ phần tử trước nó (nums[0] không bao giờ đủ điều kiện); -1 khi không có. Phần được chấm: nhóm kiểm tra của bạn phải gồm một trường hợp phân biệt \"first distinct\" với \"any distinct\" và một trường hợp cho mảng toàn-bằng.",
            [
                ("normal", "Cài đặt tham chiếu cùng các trường hợp phân biệt của nó."),
                ("discriminator", "9 đủ điều kiện trước 1 — một bug \"any distinct\" sẽ trả lời 1."),
            ],
        ),
        "csb-p17-floats": vi_challenge(
            "Trung thực dấu phẩy động",
            "Hiện thực `static bool SameTotal(decimal a, decimal b, decimal tolerance)` — true khi |a−b| ≤ tolerance — và `static double Mean(List<double> xs)` trả trung bình (rỗng/null → 0.0). Các bài kiểm tra ghim hành vi decimal chính xác và logic dung sai.",
            [
                ("normal", "So sánh dung sai và một trung bình sạch — decimal cho tiền, double cho thống kê."),
                ("edges", "Hợp đồng rỗng và biên dung sai bao-gồm."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p17-boundary",
            'public class Solution\n{\n    public static bool IsAdult(int age)\n    {\n        if (age < 0) throw new ArgumentOutOfRangeException("negative age");\n        return age >= 18;\n    }\n    public static string Grade(int score)\n    {\n        if (score < 0 || score > 100)\n            throw new ArgumentOutOfRangeException("score outside 0-100");\n        if (score >= 90) return "A";\n        if (score >= 80) return "B";\n        if (score >= 70) return "C";\n        if (score >= 60) return "D";\n        return "F";\n    }\n}\n',
            'public class Solution\n{\n    public static bool IsAdult(int age)\n    {\n        if (age < 0) throw new ArgumentOutOfRangeException("negative age");\n        // near-miss: strict > — an 18-year-old is no longer an adult\n        return age > 18;\n    }\n    public static string Grade(int score)\n    {\n        if (score < 0 || score > 100)\n            throw new ArgumentOutOfRangeException("score outside 0-100");\n        if (score >= 90) return "A";\n        if (score >= 80) return "B";\n        if (score >= 70) return "C";\n        if (score >= 60) return "D";\n        return "F";\n    }\n}\n',
        ),
        (
            "csb-p17-diagnose",
            'public class Solution\n{\n    public static int SumRange(int inclusive, int exclusive)\n    {\n        int sum = 0;\n        for (int i = inclusive; i < exclusive; i++) sum += i;\n        return sum;\n    }\n    public static int Clamp(int value, int min, int max)\n    {\n        if (min > max) throw new ArgumentException("inverted range");\n        return Math.Min(max, Math.Max(min, value));\n    }\n}\n',
            'public class Solution\n{\n    public static int SumRange(int inclusive, int exclusive)\n    {\n        // near-miss: <= includes the exclusive endpoint — SumRange(1,5)\n        // wrongly returns 15\n        int sum = 0;\n        for (int i = inclusive; i <= exclusive; i++) sum += i;\n        return sum;\n    }\n    public static int Clamp(int value, int min, int max)\n    {\n        if (min > max) throw new ArgumentException("inverted range");\n        return Math.Min(max, Math.Max(min, value));\n    }\n}\n',
        ),
        (
            "csb-p17-firstdistinct",
            'public class Solution\n{\n    public static int FirstDistinct(int[] nums)\n    {\n        if (nums == null || nums.Length == 0) return -1;\n        for (int i = 1; i < nums.Length; i++)\n        {\n            bool differsFromAll = true;\n            for (int j = 0; j < i; j++)\n            {\n                if (nums[j] == nums[i]) { differsFromAll = false; break; }\n            }\n            if (differsFromAll) return nums[i];\n        }\n        return -1;\n    }\n}\n',
            'public class Solution\n{\n    public static int FirstDistinct(int[] nums)\n    {\n        if (nums == null || nums.Length == 0) return -1;\n        // near-miss: misreads the spec as \"first element occurring exactly\n        // once in the whole array\" - global uniqueness instead of\n        // distinct-from-prefix; {7} wrongly yields 7, {3,1} yields 3\n        for (int i = 0; i < nums.Length; i++)\n        {\n            bool unique = true;\n            for (int j = 0; j < nums.Length; j++)\n            {\n                if (j != i && nums[j] == nums[i]) { unique = false; break; }\n            }\n            if (unique) return nums[i];\n        }\n        return -1;\n    }\n}\n',
        ),
        (
            "csb-p17-floats",
            'public class Solution\n{\n    public static bool SameTotal(decimal a, decimal b, decimal tolerance)\n    {\n        return Math.Abs(a - b) <= tolerance;\n    }\n    public static double Mean(List<double> xs)\n    {\n        if (xs == null || xs.Count == 0) return 0.0;\n        double sum = 0;\n        foreach (double x in xs) sum += x;\n        return sum / xs.Count;\n    }\n}\n',
            'public class Solution\n{\n    public static bool SameTotal(decimal a, decimal b, decimal tolerance)\n    {\n        // near-miss: strict < — a difference exactly equal to the tolerance\n        // is rejected, breaking the inclusive boundary\n        return Math.Abs(a - b) < tolerance;\n    }\n    public static double Mean(List<double> xs)\n    {\n        if (xs == null || xs.Count == 0) return 0.0;\n        double sum = 0;\n        foreach (double x in xs) sum += x;\n        return sum / xs.Count;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m17",
    "Checkpoint — Debugging & testing",
    "A validator suite: implement the validators AND their discriminating tests — every contract asserted from both directions.",
    20,
    r"""
## Checkpoint: the validator suite

**Task:** implement in `Solution`:

1. `static bool IsValidUsername(string s)` — 3–20 chars, letters/digits/underscore only, non-null. (Use `char.IsLetterOrDigit` / `'_'`.)
2. `static int ParsePort(string input)` — 1–65535 after parsing; `FormatException` for non-numeric, `ArgumentOutOfRangeException` for out-of-range, null → `ArgumentException`.
3. `static List<int> DedupeSorted(List<int> nums)` — distinct values in ascending order; null/empty → empty list.
""",
    "Checkpoint — Gỡ lỗi & kiểm thử",
    "Một bộ kiểm chứng: hiện thực các validator VÀ các bài kiểm tra phân biệt của chúng — mọi hợp đồng được khẳng định từ cả hai hướng.",
    r"""
## Checkpoint: bộ kiểm chứng

**Nhiệm vụ:** hiện thực trong `Solution`:

1. `static bool IsValidUsername(string s)` — 3–20 ký tự, chỉ chữ/số/gạch-dưới, không null. (Dùng `char.IsLetterOrDigit` / `'_'`.)
2. `static int ParsePort(string input)` — 1–65535 sau khi phân tích; `FormatException` với không-phải-số, `ArgumentOutOfRangeException` khi ngoài khoảng, null → `ArgumentException`.
3. `static List<int> DedupeSorted(List<int> nums)` — các giá trị phân biệt theo thứ tự tăng; null/rỗng → danh sách rỗng.
""",
    challenge(
        "csb-checkpoint-m17-task",
        "Validators",
        "Implement `IsValidUsername`, `ParsePort`, and `DedupeSorted` — boundary-inclusive contracts with explicit failure types.",
        CS_PRELUDE,
        [
            (
                "username",
                "Cj.True(Solution.IsValidUsername(\"an_99\"), \"legal\");\nCj.False(Solution.IsValidUsername(\"ab\"), \"too short\");\nCj.False(Solution.IsValidUsername(\"this_username_is_way_too_long_ok\"), \"too long\");\nCj.False(Solution.IsValidUsername(\"has space\"), \"space rejected\");\nCj.False(Solution.IsValidUsername(null), \"null rejected\");\nCj.True(Solution.IsValidUsername(\"abc\"), \"exactly 3 chars\");\nCj.True(Solution.IsValidUsername(new string('a', 20)), \"exactly 20 chars\");",
                "Both length boundaries and the character whitelist.",
            ),
            (
                "port-and-dedupe",
                "Cj.Eq(Solution.ParsePort(\"80\"), 80, \"normal\");\nCj.Eq(Solution.ParsePort(\"65535\"), 65535, \"upper bound\");\nCj.Eq(Solution.ParsePort(\"1\"), 1, \"lower bound\");\nbool t1 = false;\ntry { Solution.ParsePort(\"abc\"); } catch (FormatException) { t1 = true; }\nbool t2 = false;\ntry { Solution.ParsePort(\"70000\"); } catch (ArgumentOutOfRangeException) { t2 = true; }\nbool t3 = false;\ntry { Solution.ParsePort(null); } catch (ArgumentException) { t3 = true; }\nCj.True(t1 && t2 && t3, \"three failure types\");\nCj.Eq(string.Join(\",\", Solution.DedupeSorted(new List<int> { 3, 1, 3, 2 })), \"1,2,3\", \"distinct sorted\");\nCj.Eq(Solution.DedupeSorted(null).Count, 0, \"null\");",
                "Port boundaries with their exception types, plus dedupe with null handling.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Validators",
        "Hiện thực `IsValidUsername`, `ParsePort`, và `DedupeSorted` — hợp đồng bao-biên với các loại thất bại tường minh.",
        [
            ("username", "Cả hai biên độ dài và danh-sách-trắng ký tự."),
            ("port-and-dedupe", "Biên cổng với các loại ngoại lệ của chúng, cộng dedupe với xử lý null."),
        ],
    ),
    solution='public class Solution\n{\n    public static bool IsValidUsername(string s)\n    {\n        if (s == null) return false;\n        if (s.Length < 3 || s.Length > 20) return false;\n        foreach (char c in s)\n        {\n            if (!char.IsLetterOrDigit(c) && c != \'_\') return false;\n        }\n        return true;\n    }\n    public static int ParsePort(string input)\n    {\n        if (input == null) throw new ArgumentException("input required");\n        if (!int.TryParse(input, out int port))\n            throw new FormatException("not a number");\n        if (port < 1 || port > 65535)\n            throw new ArgumentOutOfRangeException("port outside 1-65535");\n        return port;\n    }\n    public static List<int> DedupeSorted(List<int> nums)\n    {\n        if (nums == null) return new List<int>();\n        return nums.Distinct().OrderBy(n => n).ToList();\n    }\n}\n',
    wrong='public class Solution\n{\n    public static bool IsValidUsername(string s)\n    {\n        if (s == null) return false;\n        // near-miss: length bounds off by one — 2-char and 21-char names pass\n        if (s.Length < 2 || s.Length > 21) return false;\n        foreach (char c in s)\n        {\n            if (!char.IsLetterOrDigit(c) && c != \'_\') return false;\n        }\n        return true;\n    }\n    public static int ParsePort(string input)\n    {\n        if (input == null) throw new ArgumentException("input required");\n        if (!int.TryParse(input, out int port))\n            throw new FormatException("not a number");\n        if (port < 1 || port > 65535)\n            throw new ArgumentOutOfRangeException("port outside 1-65535");\n        return port;\n    }\n    public static List<int> DedupeSorted(List<int> nums)\n    {\n        if (nums == null) return new List<int>();\n        return nums.Distinct().OrderBy(n => n).ToList();\n    }\n}\n',
)

print("module 17 authored")
