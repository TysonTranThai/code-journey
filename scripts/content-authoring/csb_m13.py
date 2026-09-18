#!/usr/bin/env python3
"""C# — Beginner — Module 13: csb-exceptions.

Exceptions as control flow for failures: try/catch/finally, throw with
message, custom exception types, and the validate-early rule. Ws catch
too much, too late, or the wrong type. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csb import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csb-exceptions"

write_module(
    M,
    "Exceptions and Error Handling",
    "Failures as typed events: throw when a contract breaks, catch when you can actually handle it — and let the rest bubble.",
    "Ngoại lệ và Xử lý lỗi",
    "Thất bại như sự kiện có kiểu: ném khi hợp đồng bị phá, bắt khi bạn thật sự xử lý được — và để phần còn lại nổi lên.",
    ["csb-m13-trycatch", "csb-m13-throw-custom", "csb-m13-finally-cleanup", "csb-checkpoint-m13"],
    ["csb-p13-exceptions"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "csb-m13-trycatch",
    "try / catch: reacting to failure",
    "An exception unwinds the call stack until a matching catch — or crashes the program.",
    13,
    r"""
## What an exception is

When code hits a condition it cannot fulfill — `int.Parse("abc")`, indexing past an array's end — it **throws** an exception object describing the failure. The runtime unwinds the call stack looking for a handler:

```csharp
try
{
    int n = int.Parse("abc");   // throws FormatException
    Console.WriteLine("never runs");
}
catch (FormatException ex)
{
    Console.WriteLine($"not a number: {ex.Message}");
}
Console.WriteLine("program continues");
```

`try` marks a guarded region; `catch` handles a specific failure type. If nothing catches it, the program dies with the stack trace.

## Catch specific, handle honestly

```csharp
catch (FormatException ex) { ... }   // only this failure
catch (Exception ex) { ... }         // everything — use sparingly
```

A broad `catch (Exception)` swallows bugs you didn't anticipate: typos, null refs, logic errors — all invisible. Catch the **specific** type you can actually do something about; let the rest crash loudly during development instead of hiding.
""",
    "try / catch: phản ứng trước thất bại",
    "Một ngoại lệ cuộn ngược call stack cho tới một catch khớp — hoặc làm sập chương trình.",
    r"""
## Ngoại lệ là gì

Khi mã gặp điều kiện không thể thực hiện — `int.Parse("abc")`, đánh chỉ số quá giới hạn mảng — nó **ném** một đối tượng ngoại lệ mô tả thất bại. Runtime cuộn ngược call stack để tìm trình xử lý:

```csharp
try
{
    int n = int.Parse("abc");   // ném FormatException
    Console.WriteLine("không bao giờ chạy");
}
catch (FormatException ex)
{
    Console.WriteLine($"không phải số: {ex.Message}");
}
Console.WriteLine("chương trình tiếp tục");
```

`try` đánh dấu vùng được bảo vệ; `catch` xử lý một loại thất bại cụ thể. Nếu không ai bắt, chương trình chết với stack trace.

## Bắt cụ thể, xử lý trung thực

```csharp
catch (FormatException ex) { ... }   // chỉ thất bại này
catch (Exception ex) { ... }         // mọi thứ — dùng hạn chế
```

Một `catch (Exception)` rộng nuốt cả những bug bạn không lường trước: lỗi đánh máy, null ref, lỗi logic — tất cả vô hình. Hãy bắt **loại cụ thể** mà bạn thật sự làm được gì đó; để phần còn lại nổ to trong lúc phát triển thay vì ẩn đi.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "csb-m13-throw-custom",
    "throw and custom exceptions",
    "`throw` signals a broken contract; custom types let callers distinguish YOUR failures from everyone else's.",
    13,
    r"""
## Throwing deliberately

Your own code throws when its contract is broken:

```csharp
static decimal Withdraw(decimal balance, decimal amount)
{
    if (amount <= 0)
        throw new ArgumentException("amount must be positive");
    if (amount > balance)
        throw new InvalidOperationException("insufficient funds");
    return balance - amount;
}
```

Two rules make throw messages useful:

- **ArgumentException** (and friends) for bad *arguments* right now — with the argument's name if possible.
- **InvalidOperationException** for a bad *operation given the current state* — withdrawing from an overdrawn account.

## Custom exceptions

When callers must tell your failures apart from the framework's, define a type:

```csharp
class PaymentDeclinedException : Exception
{
    public PaymentDeclinedException(string message) : base(message) { }
}

static void Pay(decimal amount)
{
    if (amount > 1000m)
        throw new PaymentDeclinedException("over the single-payment limit");
}
```

Now a caller can `catch (PaymentDeclinedException)` and know exactly whose rule fired. The convention: name ends in `Exception`, derive from `Exception`, pass the message to `base`.
""",
    "throw và ngoại lệ tùy chỉnh",
    "`throw` báo hiệu hợp đồng bị phá; kiểu tùy chỉnh giúp người gọi phân biệt thất bại CỦA BẠN với thất bại của người khác.",
    r"""
## Ném có chủ đích

Mã của bạn ném khi hợp đồng của nó bị phá:

```csharp
static decimal Withdraw(decimal balance, decimal amount)
{
    if (amount <= 0)
        throw new ArgumentException("amount must be positive");
    if (amount > balance)
        throw new InvalidOperationException("insufficient funds");
    return balance - amount;
}
```

Hai quy tắc làm thông điệp throw hữu ích:

- **ArgumentException** (và họ hàng) cho *đối số* xấu ngay tại chỗ — kèm tên đối số nếu được.
- **InvalidOperationException** cho *thao tác xấu xét theo trạng thái hiện tại* — rút tiền từ tài khoản đã thấu chi.

## Ngoại lệ tùy chỉnh

Khi người gọi phải phân biệt thất bại của bạn với của framework, hãy định nghĩa một kiểu:

```csharp
class PaymentDeclinedException : Exception
{
    public PaymentDeclinedException(string message) : base(message) { }
}

static void Pay(decimal amount)
{
    if (amount > 1000m)
        throw new PaymentDeclinedException("over the single-payment limit");
}
```

Giờ người gọi có thể `catch (PaymentDeclinedException)` và biết chính xác luật của ai vừa kích hoạt. Quy ước: tên kết thúc bằng `Exception`, kế thừa từ `Exception`, truyền message cho `base`.
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "csb-m13-finally-cleanup",
    "finally, using, and validate-early",
    "Cleanup runs no matter what; validation happens before any work — not inside a catch.",
    12,
    r"""
## finally: always runs

```csharp
try
{
    OpenConnection();
    DoWork();          // may throw
}
finally
{
    CloseConnection(); // runs on success AND on failure
}
```

`finally` executes whether the try block succeeds, throws, or returns. Put cleanup there — resource release must never depend on luck.

In modern C#, files/streams take that shape for you:

```csharp
using (var reader = new StringReader(text))
{
    ... // disposed automatically, even on exception
}
```

## Validate early, fail fast

The strongest error-handling pattern isn't a catch — it's refusing bad input before any work happens:

```csharp
static int ParseAge(string input)
{
    if (input == null) throw new ArgumentException("input required");
    if (!int.TryParse(input, out int age))
        throw new FormatException("not a number");
    if (age < 0 || age > 150)
        throw new ArgumentOutOfRangeException("implausible age");
    return age;
}
```

Compare with catching errors *after* half the work is done: state is now inconsistent, cleanup is complicated, and the failure message is vague. Validate at the door.
""",
    "finally, using, và kiểm-tra-sớm",
    "Dọn dẹp chạy bất kể điều gì; kiểm tra dữ liệu diễn ra trước mọi công việc — không phải trong catch.",
    r"""
## finally: luôn chạy

```csharp
try
{
    OpenConnection();
    DoWork();          // có thể ném
}
finally
{
    CloseConnection(); // chạy cả khi thành công lẫn thất bại
}
```

`finally` thực thi dù khối try thành công, ném, hay return. Hãy đặt dọn dẹp ở đó — giải phóng tài nguyên không bao giờ được phụ thuộc may rủi.

Trong C# hiện đại, file/stream có sẵn hình dạng đó:

```csharp
using (var reader = new StringReader(text))
{
    ... // được dispose tự động, kể cả khi có ngoại lệ
}
```

## Kiểm tra sớm, thất bại nhanh

Mẫu xử lý lỗi mạnh nhất không phải là catch — mà là từ chối đầu vào xấu trước khi bất kỳ công việc nào diễn ra:

```csharp
static int ParseAge(string input)
{
    if (input == null) throw new ArgumentException("input required");
    if (!int.TryParse(input, out int age))
        throw new FormatException("not a number");
    if (age < 0 || age > 150)
        throw new ArgumentOutOfRangeException("implausible age");
    return age;
}
```

Hãy so với việc bắt lỗi *sau khi* nửa công việc đã xong: trạng thái giờ không nhất quán, dọn dẹp phức tạp, và thông điệp lỗi mơ hồ. Kiểm tra ngay ở cửa.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M, "csb-p13-exceptions",
    "Error handling workout",
    "Parsers, transfers, retries, and custom types — contracts under discriminating tests.",
    "Luyện tập xử lý lỗi",
    "Bộ phân tích, chuyển tiền, thử lại, và kiểu tùy chỉnh — hợp đồng dưới các bài kiểm tra phân biệt.",
    "csb-m13-finally-cleanup",
    40,
    "beginner",
    [
        challenge(
            "csb-p13-parseage",
            "ParseAge with layered validation",
            "Implement `static int ParseAge(string input)`: null/whitespace → `ArgumentException`; not a number → `FormatException`; outside 0–150 → `ArgumentOutOfRangeException`; otherwise the parsed age.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.ParseAge(\"25\"), 25, \"valid age\");\nCj.Eq(Solution.ParseAge(\"0\"), 0, \"zero is legal\");\nCj.Eq(Solution.ParseAge(\"150\"), 150, \"upper bound is legal\");",
                    "Both boundaries are inclusive.",
                ),
                (
                    "failure-types",
                    "bool t1 = false;\ntry { Solution.ParseAge(\"  \"); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { Solution.ParseAge(\"abc\"); } catch (FormatException) { t2 = true; }\nbool t3 = false;\ntry { Solution.ParseAge(\"999\"); } catch (ArgumentOutOfRangeException) { t3 = true; }\nbool t4 = false;\ntry { Solution.ParseAge(\"-1\"); } catch (ArgumentOutOfRangeException) { t4 = true; }\nCj.True(t1 && t2 && t3 && t4, \"each failure maps to its own exception type\");",
                    "The exception TYPE is the contract — callers branch on it.",
                ),
            ],
            level="guided",
        ),
        challenge(
            "csb-p13-atm",
            "ATM with a custom exception",
            "Implement nested class `Solution.InsufficientFundsException : Exception` with a `public decimal Missing { get; }` (constructor `(decimal missing)` passing a message to base and storing it), plus `static decimal Withdraw(decimal balance, decimal amount)` throwing `ArgumentException` for non-positive amounts and `InsufficientFundsException` when `amount > balance` (Missing = amount − balance); success returns the new balance.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "Cj.Eq(Solution.Withdraw(100m, 40m), 60m, \"normal withdrawal\");\nCj.Eq(Solution.Withdraw(100m, 100m), 0m, \"exact balance is legal\");",
                    "Withdrawing exactly the balance leaves 0 — legal.",
                ),
                (
                    "custom",
                    "try\n{\n    Solution.Withdraw(50m, 80m);\n    Cj.True(false, \"must throw\");\n}\ncatch (Solution.InsufficientFundsException ex)\n{\n    Cj.Eq(ex.Missing, 30m, \"Missing = shortfall\");\n    Cj.True(ex.Message.Length > 0, \"message present\");\n}\nbool t = false;\ntry { Solution.Withdraw(50m, 0m); } catch (ArgumentException) { t = true; }\nCj.True(t, \"non-positive amount rejected\");",
                    "The custom type carries structured data (Missing) a generic exception couldn't.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p13-retry",
            "Retry with attempt budget",
            "Implement `static int ReadWithRetry(Func<int> reader, int attempts)`: calls `reader()` until it succeeds (returns its value) or the attempts run out — then throws `InvalidOperationException`. Counts every attempt, including the successful one. `attempts <= 0` → `ArgumentException` without calling reader.",
            CS_PRELUDE,
            [
                (
                    "normal",
                    "int calls = 0;\nint v = Solution.ReadWithRetry(() => { calls++; return calls >= 3 ? 42 : throw new InvalidOperationException(\"flaky\"); }, 5);\nCj.Eq(v, 42, \"succeeded on attempt 3\");\nCj.Eq(calls, 3, \"three attempts made\");",
                    "The reader throws twice, then succeeds — retry must return the success value.",
                ),
                (
                    "exhaustion",
                    "int calls = 0;\nbool t = false;\ntry { Solution.ReadWithRetry(() => { calls++; throw new InvalidOperationException(\"always\"); }, 3); } catch (InvalidOperationException) { t = true; }\nCj.True(t, \"exhaustion throws\");\nCj.Eq(calls, 3, \"exactly the attempt budget used\");\nbool t2 = false;\nbool called = false;\ntry { Solution.ReadWithRetry(() => { called = true; return 1; }, 0); } catch (ArgumentException) { t2 = true; }\nCj.True(t2 && !called, \"zero attempts rejected before any call\");",
                    "Exactly `attempts` calls happen on exhaustion; the budget is validated up front.",
                ),
            ],
            level="independent",
        ),
        challenge(
            "csb-p13-transfer",
            "Transfer with cleanup discipline",
            "Implement `static decimal Transfer(decimal from, decimal to, decimal amount)` inside a running total model: throws `ArgumentException` for non-positive amount, throws `InvalidOperationException` when `amount > from`, otherwise returns `to + amount`. Also implement `static bool AuditTrail(List<string> log, Action action)`: runs `action`, always appending `\"done\"` to the log afterwards (even when action throws, log gets `\"done\"` and the exception propagates); returns true only if action completed without throwing.",
            CS_PRELUDE,
            [
                (
                    "transfer",
                    "Cj.Eq(Solution.Transfer(100m, 50m, 30m), 80m, \"amount lands\");\nbool t1 = false;\ntry { Solution.Transfer(100m, 50m, 0m); } catch (ArgumentException) { t1 = true; }\nbool t2 = false;\ntry { Solution.Transfer(10m, 50m, 20m); } catch (InvalidOperationException) { t2 = true; }\nCj.True(t1 && t2, \"both contracts enforced\");",
                    "Argument validation and state validation stay distinct exception types.",
                ),
                (
                    "audit",
                    "var log = new List<string>();\nbool ok = Solution.AuditTrail(log, () => log.Add(\"work\"));\nCj.True(ok, \"success returns true\");\nCj.Eq(string.Join(\",\", log), \"work,done\", \"done appended after success\");\nvar log2 = new List<string>();\nbool threw = false;\ntry { Solution.AuditTrail(log2, () => throw new InvalidOperationException()); } catch (InvalidOperationException) { threw = true; }\nCj.True(threw, \"exception propagates\");\nCj.Eq(log2.Count, 1, \"done still appended on failure\");\nCj.Eq(log2[0], \"done\", \"and it is exactly done\");",
                    "finally semantics: the append happens on both paths; only the return value differs.",
                ),
            ],
            level="independent",
        ),
    ],
    {
        "csb-p13-parseage": vi_challenge(
            "ParseAge với kiểm tra nhiều lớp",
            "Hiện thực `static int ParseAge(string input)`: null/toàn khoảng trắng → `ArgumentException`; không phải số → `FormatException`; ngoài 0–150 → `ArgumentOutOfRangeException`; nếu hợp lệ trả tuổi đã phân tích.",
            [
                ("normal", "Cả hai biên đều bao gồm."),
                ("failure-types", "KIỂU ngoại lệ là hợp đồng — người gọi rẽ nhánh theo nó."),
            ],
        ),
        "csb-p13-atm": vi_challenge(
            "ATM với ngoại lệ tùy chỉnh",
            "Hiện thực lớp lồng `Solution.InsufficientFundsException : Exception` với `public decimal Missing { get; }` (constructor `(decimal missing)` truyền message cho base và lưu nó), cùng `static decimal Withdraw(decimal balance, decimal amount)` ném `ArgumentException` với số không dương và `InsufficientFundsException` khi `amount > balance` (Missing = amount − balance); thành công trả số dư mới.",
            [
                ("normal", "Rút đúng bằng số dư để lại 0 — hợp lệ."),
                ("custom", "Kiểu tùy chỉnh mang dữ liệu có cấu trúc (Missing) mà ngoại lệ chung không có."),
            ],
        ),
        "csb-p13-retry": vi_challenge(
            "Thử lại với ngân sách lần",
            "Hiện thực `static int ReadWithRetry(Func<int> reader, int attempts)`: gọi `reader()` cho tới khi thành công (trả giá trị của nó) hoặc hết số lần — rồi ném `InvalidOperationException`. Đếm mọi lần thử, kể cả lần thành công. `attempts <= 0` → `ArgumentException` mà không gọi reader.",
            [
                ("normal", "Reader ném hai lần rồi thành công — retry phải trả giá trị thành công."),
                ("exhaustion", "Đúng `attempts` lần gọi diễn ra khi cạn ngân sách; ngân sách được kiểm tra trước."),
            ],
        ),
        "csb-p13-transfer": vi_challenge(
            "Chuyển tiền với kỷ luật dọn dẹp",
            "Hiện thực `static decimal Transfer(decimal from, decimal to, decimal amount)`: ném `ArgumentException` với số không dương, ném `InvalidOperationException` khi `amount > from`, nếu hợp lệ trả `to + amount`. Cùng `static bool AuditTrail(List<string> log, Action action)`: chạy `action`, luôn thêm `\"done\"` vào log sau đó (kể cả khi action ném, log vẫn nhận `\"done\"` và ngoại lệ được lan truyền); trả true chỉ khi action hoàn tất mà không ném.",
            [
                ("transfer", "Kiểm tra đối số và kiểm tra trạng thái giữ riêng hai loại ngoại lệ."),
                ("audit", "Ngữ nghĩa finally: phần thêm vào diễn ra trên cả hai đường; chỉ giá trị trả về khác nhau."),
            ],
        ),
    },
    solutions=[
        (
            "csb-p13-parseage",
            'public class Solution\n{\n    public static int ParseAge(string input)\n    {\n        if (string.IsNullOrWhiteSpace(input))\n            throw new ArgumentException("input required");\n        if (!int.TryParse(input, out int age))\n            throw new FormatException("not a number");\n        if (age < 0 || age > 150)\n            throw new ArgumentOutOfRangeException("implausible age");\n        return age;\n    }\n}\n',
            'public class Solution\n{\n    public static int ParseAge(string input)\n    {\n        if (string.IsNullOrWhiteSpace(input))\n            throw new ArgumentException("input required");\n        if (!int.TryParse(input, out int age))\n            throw new FormatException("not a number");\n        // near-miss: range check uses AND instead of OR — "-1" parses to a\n        // negative age that fails neither side of (age < 0 && age > 150)\n        if (age < 0 && age > 150)\n            throw new ArgumentOutOfRangeException("implausible age");\n        return age;\n    }\n}\n',
        ),
        (
            "csb-p13-atm",
            'public class Solution\n{\n    public sealed class InsufficientFundsException : Exception\n    {\n        public decimal Missing { get; }\n        public InsufficientFundsException(decimal missing)\n            : base($"insufficient funds: missing {missing}")\n        {\n            Missing = missing;\n        }\n    }\n    public static decimal Withdraw(decimal balance, decimal amount)\n    {\n        if (amount <= 0)\n            throw new ArgumentException("amount must be positive");\n        if (amount > balance)\n            throw new InsufficientFundsException(amount - balance);\n        return balance - amount;\n    }\n}\n',
            'public class Solution\n{\n    public sealed class InsufficientFundsException : Exception\n    {\n        public decimal Missing { get; }\n        public InsufficientFundsException(decimal missing)\n            : base($"insufficient funds: missing {missing}")\n        {\n            Missing = missing;\n        }\n    }\n    public static decimal Withdraw(decimal balance, decimal amount)\n    {\n        if (amount <= 0)\n            throw new ArgumentException("amount must be positive");\n        // near-miss: Missing stores the requested amount, not the shortfall\n        if (amount > balance)\n            throw new InsufficientFundsException(amount);\n        return balance - amount;\n    }\n}\n',
        ),
        (
            "csb-p13-retry",
            'public class Solution\n{\n    public static int ReadWithRetry(Func<int> reader, int attempts)\n    {\n        if (attempts <= 0)\n            throw new ArgumentException("attempts must be positive");\n        for (int i = 0; i < attempts; i++)\n        {\n            try\n            {\n                return reader();\n            }\n            catch (InvalidOperationException)\n            {\n                // fall through to the next attempt\n            }\n        }\n        throw new InvalidOperationException("all attempts exhausted");\n    }\n}\n',
            'public class Solution\n{\n    public static int ReadWithRetry(Func<int> reader, int attempts)\n    {\n        if (attempts <= 0)\n            throw new ArgumentException("attempts must be positive");\n        // near-miss: loop runs attempts-1 times — the budget is spent one\n        // call short, so a reader that succeeds on the LAST allowed attempt\n        // still gets exhausted\n        for (int i = 0; i < attempts - 1; i++)\n        {\n            try\n            {\n                return reader();\n            }\n            catch (InvalidOperationException)\n            {\n            }\n        }\n        throw new InvalidOperationException("all attempts exhausted");\n    }\n}\n',
        ),
        (
            "csb-p13-transfer",
            'public class Solution\n{\n    public static decimal Transfer(decimal from, decimal to, decimal amount)\n    {\n        if (amount <= 0)\n            throw new ArgumentException("amount must be positive");\n        if (amount > from)\n            throw new InvalidOperationException("insufficient funds");\n        return to + amount;\n    }\n    public static bool AuditTrail(List<string> log, Action action)\n    {\n        try\n        {\n            action();\n            return true;\n        }\n        finally\n        {\n            log.Add("done");\n        }\n    }\n}\n',
            'public class Solution\n{\n    public static decimal Transfer(decimal from, decimal to, decimal amount)\n    {\n        if (amount <= 0)\n            throw new ArgumentException("amount must be positive");\n        if (amount > from)\n            throw new InvalidOperationException("insufficient funds");\n        return to + amount;\n    }\n    public static bool AuditTrail(List<string> log, Action action)\n    {\n        // near-miss: cleanup lives in a catch, not a finally — when action\n        // succeeds, "done" is never appended and the audit trail is silent\n        try\n        {\n            action();\n            return true;\n        }\n        catch (Exception)\n        {\n            log.Add("done");\n            throw;\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M, "csb-checkpoint-m13",
    "Checkpoint — Error handling",
    "A reservation service: layered validation, a custom exception with data, and a cleanup-guaranteed executor.",
    20,
    r"""
## Checkpoint: the reservation service

**Task:** implement in `Solution`:

1. `class BookingConflictException : Exception` with `public string Slot { get; }` (constructor `(string slot, string message)` → base(message), store Slot).
2. `static string Book(List<string> takenSlots, string slot)`:
   - null/whitespace slot → `ArgumentException`;
   - slot already in `takenSlots` → `BookingConflictException` (Slot = slot);
   - otherwise add and return the slot.
3. `static T Guard<T>(Func<T> action, string label)`:
   - runs `action`; returns its result on success;
   - on exception: throws `InvalidOperationException` with a message containing `label` — but ONLY for `InvalidOperationException`; any other exception type must propagate unchanged;
   - `label` null → `ArgumentException` before running action.
""",
    "Checkpoint — Xử lý lỗi",
    "Dịch vụ đặt chỗ: kiểm tra nhiều lớp, một ngoại lệ tùy chỉnh có dữ liệu, và một trình thực thi bảo-đảm-dọn-dẹp.",
    r"""
## Checkpoint: dịch vụ đặt chỗ

**Nhiệm vụ:** hiện thực trong `Solution`:

1. `class BookingConflictException : Exception` với `public string Slot { get; }` (constructor `(string slot, string message)` → base(message), lưu Slot).
2. `static string Book(List<string> takenSlots, string slot)`:
   - slot null/toàn khoảng trắng → `ArgumentException`;
   - slot đã có trong `takenSlots` → `BookingConflictException` (Slot = slot);
   - nếu hợp lệ: thêm vào và trả slot.
3. `static T Guard<T>(Func<T> action, string label)`:
   - chạy `action`; trả kết quả khi thành công;
   - khi có ngoại lệ: ném `InvalidOperationException` với message chứa `label` — nhưng CHỈ với `InvalidOperationException`; ngoại lệ kiểu khác phải lan truyền nguyên vẹn;
   - `label` null → `ArgumentException` trước khi chạy action.
""",
    challenge(
        "csb-checkpoint-m13-task",
        "Reservations",
        "Implement `BookingConflictException`, `Book`, and `Guard` — the exception TYPE each failure throws is the graded contract.",
        CS_PRELUDE,
        [
            (
                "booking",
                "var taken = new List<string> { \"9am\" };\nCj.Eq(Solution.Book(taken, \"10am\"), \"10am\", \"free slot booked\");\nCj.Eq(taken.Count, 2, \"slot recorded\");\ntry\n{\n    Solution.Book(taken, \"9am\");\n    Cj.True(false, \"must throw\");\n}\ncatch (Solution.BookingConflictException ex)\n{\n    Cj.Eq(ex.Slot, \"9am\", \"Slot carries the conflicting slot\");\n}\nbool t = false;\ntry { Solution.Book(taken, \"  \"); } catch (ArgumentException) { t = true; }\nCj.True(t, \"blank slot rejected\");",
                "Book, record, conflict detection with data, and blank rejection.",
            ),
            (
                "guard",
                "Cj.Eq(Solution.Guard(() => 21, \"answer\"), 21, \"result passes through\");\nbool t1 = false;\ntry { Solution.Guard<int>(() => throw new InvalidOperationException(\"boom\"), \"booking\"); } catch (InvalidOperationException ex) { t1 = ex.Message.Contains(\"booking\"); }\nCj.True(t1, \"IOE wrapped with the label\");\nbool t2 = false;\ntry { Solution.Guard<int>(() => throw new ArgumentException(\"raw\"), \"booking\"); } catch (ArgumentException) { t2 = true; }\nCj.True(t2, \"other types propagate unchanged\");\nbool t3 = false;\ntry { Solution.Guard(() => 1, null); } catch (ArgumentException) { t3 = true; }\nCj.True(t3, \"null label rejected\");",
                "Guard's selectivity is the point: wrap InvalidOperationException, pass everything else.",
            ),
        ],
        difficulty="beginner",
    ),
    vi_challenge(
        "Reservations",
        "Hiện thực `BookingConflictException`, `Book`, và `Guard` — KIỂU ngoại lệ mà mỗi thất bại ném là hợp đồng được chấm điểm.",
        [
            ("booking", "Đặt, ghi nhận, phát hiện xung đột kèm dữ liệu, và từ chối slot rỗng."),
            ("guard", "Tính chọn lọc của Guard là điểm mấu chốt: bọc InvalidOperationException, truyền nguyên vẹn mọi thứ khác."),
        ],
    ),
    solution='public class Solution\n{\n    public sealed class BookingConflictException : Exception\n    {\n        public string Slot { get; }\n        public BookingConflictException(string slot, string message) : base(message)\n        {\n            Slot = slot;\n        }\n    }\n    public static string Book(List<string> takenSlots, string slot)\n    {\n        if (string.IsNullOrWhiteSpace(slot))\n            throw new ArgumentException("slot required");\n        if (takenSlots.Contains(slot))\n            throw new BookingConflictException(slot, $"slot {slot} already booked");\n        takenSlots.Add(slot);\n        return slot;\n    }\n    public static T Guard<T>(Func<T> action, string label)\n    {\n        if (label == null)\n            throw new ArgumentException("label required");\n        try\n        {\n            return action();\n        }\n        catch (InvalidOperationException ex)\n        {\n            throw new InvalidOperationException($"{label}: {ex.Message}");\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public sealed class BookingConflictException : Exception\n    {\n        public string Slot { get; }\n        public BookingConflictException(string slot, string message) : base(message)\n        {\n            Slot = slot;\n        }\n    }\n    public static string Book(List<string> takenSlots, string slot)\n    {\n        if (string.IsNullOrWhiteSpace(slot))\n            throw new ArgumentException("slot required");\n        if (takenSlots.Contains(slot))\n            throw new BookingConflictException(slot, $"slot {slot} already booked");\n        takenSlots.Add(slot);\n        return slot;\n    }\n    public static T Guard<T>(Func<T> action, string label)\n    {\n        if (label == null)\n            throw new ArgumentException("label required");\n        // near-miss: catches EVERYTHING — foreign exception types are\n        // re-wrapped as InvalidOperationException, erasing their identity\n        try\n        {\n            return action();\n        }\n        catch (Exception ex)\n        {\n            throw new InvalidOperationException($"{label}: {ex.Message}");\n        }\n    }\n}\n',
)

print("module 13 authored")
