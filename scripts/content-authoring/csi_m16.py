#!/usr/bin/env python3
"""C# — Intermediate — Module 16: csi-testing.

Testing as a skill: build a mini test framework from scratch (runner, results,
continue-on-failure), then hand-roll the test-double spectrum (stub/fake/mock),
then debug the classic isolation bug (shared static state). No NuGet, no
xUnit — the sandbox shape forces the frameworks-off view, which is exactly
what makes learners understand what a test framework actually does.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-testing"

write_module(
    M,
    "Testing & Mocking",
    "Build a test framework from scratch, hand-roll test doubles, and isolate state — understand what xUnit does before you ever need it.",
    "Kiểm thử & Giả lập",
    "Tự xây framework kiểm thử, tự làm test double, và cô lập trạng thái — hiểu xUnit làm gì trước khi bạn cần nó.",
    ["mini-framework", "test-doubles", "csi-checkpoint-m16"],
    ["csi-p16-testing"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "mini-framework",
    "Anatomy of a Test Framework",
    "AAA, naming, a runner that continues past failures, and parameterized tables — the 60 lines under every test framework.",
    18,
    r"""
## What a test framework actually is

Strip away the attributes and the runner UI, and a test framework is a
`foreach` with a `try/catch`:

```csharp
public sealed record TestResult(string Name, bool Passed, string Message);

public sealed class TestSummary
{
    public int Passed;
    public int Failed;
    public List<string> Failures = new();   // "name: message"
}

public static TestSummary Run(IEnumerable<(string Name, Action Body)> tests)
{
    var summary = new TestSummary();
    foreach (var (name, body) in tests)
    {
        try { body(); summary.Passed++; }
        catch (Exception ex)
        {
            summary.Failed++;
            summary.Failures.Add(name + ": " + ex.Message);
        }
    }
    return summary;
}
```

Two design decisions matter more than the rest:

1. **Keep going after a failure.** A runner that stops at the first red test
   hides everything behind it. Real frameworks run every test and report all
   failures — that is what makes a failed CI run useful.
2. **A test "fails" by throwing.** Assertions are just small methods that
   throw on mismatch. `xUnit`'s `Assert.Equal` and the `Cj` helper this
   platform grades with are the same idea.

## AAA — the shape of every test

Arrange the world, act once, assert on the outcome:

```csharp
// Arrange
var cart = new Cart();
cart.Add("tea", price: 3m, qty: 2);
// Act
var total = cart.Total();
// Assert
// total == 6m
```

If you cannot see the three blocks, the test is doing too much — split it.

## Naming: the test name is the specification

Prefer sentence names that state the expected behavior:
`Total_sums_price_times_quantity`, `PlaceOrder_rejects_when_out_of_stock`.
When the name is right, the failure list reads like a to-do list; when it is
wrong ("Test1", "works now"), every future reader re-derives the intent.

## Parameterized tests: one body, many cases

Same behavior over many inputs → loop a table, don't copy the test:

```csharp
var cases = new (string Input, int Expected)[]
{
    ("", 0), ("a", 1), ("ab", 2),
};
foreach (var (input, expected) in cases)
{
    // assert Count(input) == expected, labeling with input
}
```

Each iteration should carry its inputs in the failure message — a bare
"expected 2, got 3" over a table of 40 rows is unusable.

## Check your understanding

- Why must the runner continue after a failure? (One red test should not hide ten others — CI reports all.)
- What makes a test fail in every framework? (An exception escaping the test body.)
""",
    "Giải phẫu một Test Framework",
    "AAA, cách đặt tên, runner chạy tiếp qua lỗi, và bảng tham số hóa — 60 dòng bên dưới mọi test framework.",
    r"""
## Test framework thực chất là gì

Gỡ bỏ attribute và UI đi, một test framework chỉ là một `foreach` với
`try/catch`:

```csharp
public sealed record TestResult(string Name, bool Passed, string Message);

public sealed class TestSummary
{
    public int Passed;
    public int Failed;
    public List<string> Failures = new();   // "tên: thông điệp"
}

public static TestSummary Run(IEnumerable<(string Name, Action Body)> tests)
{
    var summary = new TestSummary();
    foreach (var (name, body) in tests)
    {
        try { body(); summary.Passed++; }
        catch (Exception ex)
        {
            summary.Failed++;
            summary.Failures.Add(name + ": " + ex.Message);
        }
    }
    return summary;
}
```

Hai quyết định thiết kế quan trọng hơn cả:

1. **Chạy tiếp sau một lỗi.** Runner dừng ở test đỏ đầu tiên che giấu tất cả
   những gì phía sau. Framework thật chạy mọi test và báo tất cả lỗi — đó là
   lý do một lần CI đỏ hữu ích.
2. **Test "thất bại" bằng cách ném exception.** Assertion chỉ là các method
   nhỏ ném lỗi khi lệch. `Assert.Equal` của xUnit và helper `Cj` mà nền tảng
   này chấm điểm là cùng một ý tưởng.

## AAA — hình dáng của mọi test

Sắp đặt thế giới, hành động một lần, khẳng định kết quả:

```csharp
// Arrange
var cart = new Cart();
cart.Add("tea", price: 3m, qty: 2);
// Act
var total = cart.Total();
// Assert
// total == 6m
```

Nếu không thấy được ba khối, test đang làm quá nhiều việc — tách nó ra.

## Đặt tên: tên test là đặc tả

Ưu tiên tên câu mô tả hành vi kỳ vọng:
`Total_sums_price_times_quantity`, `PlaceOrder_rejects_when_out_of_stock`.
Đúng tên thì danh sách lỗi đọc như danh sách việc cần làm; sai tên ("Test1",
"works now"), mọi người đọc lại phải đoán ý định.

## Test tham số hóa: một thân, nhiều ca

Cùng hành vi qua nhiều đầu vào → lặp bảng, đừng sao chép test:

```csharp
var cases = new (string Input, int Expected)[]
{
    ("", 0), ("a", 1), ("ab", 2),
};
foreach (var (input, expected) in cases)
{
    // assert Count(input) == expected, nhãn chứa input
}
```

Mỗi vòng lặp phải mang đầu vào trong thông điệp lỗi — "expected 2, got 3"
trần trụi giữa bảng 40 hàng là vô dụng.

## Kiểm tra hiểu biết

- Vì sao runner phải chạy tiếp sau lỗi? (Một test đỏ không được che mười test khác — CI báo tất cả.)
- Điều gì làm một test thất bại trong mọi framework? (Một exception thoát ra khỏi thân test.)
""",
    r"""
## Test framework thực chất là gì

Gỡ bỏ attribute và UI đi, một test framework chỉ là một `foreach` với
`try/catch`:

```csharp
public sealed record TestResult(string Name, bool Passed, string Message);

public sealed class TestSummary
{
    public int Passed;
    public int Failed;
    public List<string> Failures = new();   // "tên: thông điệp"
}

public static TestSummary Run(IEnumerable<(string Name, Action Body)> tests)
{
    var summary = new TestSummary();
    foreach (var (name, body) in tests)
    {
        try { body(); summary.Passed++; }
        catch (Exception ex)
        {
            summary.Failed++;
            summary.Failures.Add(name + ": " + ex.Message);
        }
    }
    return summary;
}
```

Hai quyết định thiết kế quan trọng hơn cả:

1. **Chạy tiếp sau một lỗi.** Runner dừng ở test đỏ đầu tiên che giấu tất cả
   những gì phía sau. Framework thật chạy mọi test và báo tất cả lỗi — đó là
   lý do một lần CI đỏ hữu ích.
2. **Test "thất bại" bằng cách ném exception.** Assertion chỉ là các method
   nhỏ ném lỗi khi lệch. `Assert.Equal` của xUnit và helper `Cj` mà nền tảng
   này chấm điểm là cùng một ý tưởng.

## AAA — hình dáng của mọi test

Sắp đặt thế giới, hành động một lần, khẳng định kết quả:

```csharp
// Arrange
var cart = new Cart();
cart.Add("tea", price: 3m, qty: 2);
// Act
var total = cart.Total();
// Assert
// total == 6m
```

Nếu không thấy được ba khối, test đang làm quá nhiều việc — tách nó ra.

## Đặt tên: tên test là đặc tả

Ưu tiên tên câu mô tả hành vi kỳ vọng:
`Total_sums_price_times_quantity`, `PlaceOrder_rejects_when_out_of_stock`.
Đúng tên thì danh sách lỗi đọc như danh sách việc cần làm; sai tên ("Test1",
"works now"), mọi người đọc lại phải đoán ý định.

## Test tham số hóa: một thân, nhiều ca

Cùng hành vi qua nhiều đầu vào → lặp bảng, đừng sao chép test:

```csharp
var cases = new (string Input, int Expected)[]
{
    ("", 0), ("a", 1), ("ab", 2),
};
foreach (var (input, expected) in cases)
{
    // assert Count(input) == expected, nhãn chứa input
}
```

Mỗi vòng lặp phải mang đầu vào trong thông điệp lỗi — "expected 2, got 3"
trần trụi giữa bảng 40 hàng là vô dụng.

## Kiểm tra hiểu biết

- Vì sao runner phải chạy tiếp sau lỗi? (Một test đỏ không được che mười test khác — CI báo tất cả.)
- Điều gì làm một test thất bại trong mọi framework? (Một exception thoát ra khỏi thân test.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "test-doubles",
    "Hand-Rolled Test Doubles and Isolation",
    "Stubs, fakes, mocks without a mocking library — and the shared-state bug that makes tests flaky.",
    17,
    r"""
## Why doubles at all

A unit test must not need the network, a database, or the file system. It
needs the *behavior* of those things, controlled by the test. A **test
double** is a stand-in object that provides it. The dependency-inversion
you built in Module 11 — services depend on interfaces — is exactly what
makes doubles possible: the test hands the service a different
implementation.

## The spectrum, by hand

- **Stub** — returns hardcoded answers. "The payment gateway approves."
  No state worth checking.
- **Fake** — a working lightweight implementation. A `Dictionary`-backed
  repository stands in for the SQL one. The service can't tell the
  difference, and the test can inspect real behavior.
- **Mock** — records the *interaction* for later verification: "Reserve was
  called exactly once with sku=tea". Use when the interaction itself is the
  requirement (side effects), not the data.

```csharp
public interface IPaymentGateway { bool Charge(decimal amount); }

public sealed class StubGateway : IPaymentGateway          // stub
{
    public bool Result = true;
    public bool Charge(decimal amount) => Result;
}

public sealed class MockGateway : IPaymentGateway          // mock
{
    public int Calls;
    public decimal LastAmount;
    public bool Charge(decimal amount) { Calls++; LastAmount = amount; return true; }
}
```

Fakes are the workhorse; mocks pull their weight when the *call* is the
outcome. Reaching for a mocking library before writing two by hand is how
people end up testing the mock instead of the code.

## Isolation: every test gets a fresh world

The classic rot: tests pass alone, fail in a suite — or the reverse.
Root causes are almost always shared mutable state:

- a `static` field or cache on the service;
- a singleton the service mutates;
- ordering: test B depends on something test A created.

Rules that prevent it: fresh instances per test (the Arrange block builds
its own world), no statics holding state, and no test may depend on another
having run. In real frameworks, test *order* is undefined — anything that
needs ordering is a bug.

## Check your understanding

- Stub vs fake? (Stub answers canned values; fake is a working lightweight implementation.)
- When is a mock the right choice? (When the interaction itself — was it called, with what — is the requirement.)
- Tests pass alone, fail together. First suspects? (Shared static state, singletons, hidden ordering.)
""",
    "Test Double Tự Làm và Cô lập",
    "Stub, fake, mock không cần thư viện mocking — và lỗi trạng thái chia sẻ khiến test bấp bênh.",
    r"""
## Vì sao cần double

Unit test không được cần mạng, database hay file system. Nó cần *hành vi*
của những thứ đó, do test kiểm soát. **Test double** là đối tượng thay thế
cung cấp điều đó. Đảo ngược phụ thuộc bạn xây ở Module 11 — service phụ thuộc
interface — chính là thứ làm double khả thi: test đưa cho service một hiện
thực khác.

## Phổ double, làm bằng tay

- **Stub** — trả câu trả lời cứng. "Cổng thanh toán chấp nhận." Không có
  trạng thái đáng kiểm tra.
- **Fake** — hiện thực nhẹ hoạt động thật. Repository lưng `Dictionary` đứng
  chỗ repository SQL. Service không phân biệt được, và test quan sát được
  hành vi thật.
- **Mock** — ghi lại *tương tác* để kiểm chứng sau: "Reserve được gọi đúng
  một lần với sku=tea". Dùng khi chính tương tác là yêu cầu (tác dụng phụ),
  không phải dữ liệu.

```csharp
public interface IPaymentGateway { bool Charge(decimal amount); }

public sealed class StubGateway : IPaymentGateway          // stub
{
    public bool Result = true;
    public bool Charge(decimal amount) => Result;
}

public sealed class MockGateway : IPaymentGateway          // mock
{
    public int Calls;
    public decimal LastAmount;
    public bool Charge(decimal amount) { Calls++; LastAmount = amount; return true; }
}
```

Fake là lao động chính; mock đáng giá khi *cuộc gọi* là kết quả. Lời dùng
thư viện mocking trước khi viết hai cái bằng tay là cách người ta quay ra
test cái mock thay vì test code.

## Cô lập: mỗi test một thế giới mới

Sự mục rữa kinh điển: test chạy một mình thì pass, chạy trong bộ thì fail —
hoặc ngược lại. Nguyên nhân gần như luôn là trạng thái có thể thay đổi dùng
chung:

- một trường `static` hoặc cache trên service;
- một singleton mà service thay đổi;
- thứ tự: test B phụ thuộc thứ test A tạo ra.

Các luật phòng ngừa: instance mới mỗi test (khối Arrange tự dựng thế giới
của nó), không static giữ trạng thái, không test nào phụ thuộc test khác đã
chạy. Trong framework thật, *thứ tự* test là không xác định — bất kỳ thứ gì
cần thứ tự đều là lỗi.

## Kiểm tra hiểu biết

- Stub khác fake? (Stub trả giá trị đóng sẵn; fake là hiện thực nhẹ hoạt động thật.)
- Khi nào mock là lựa chọn đúng? (Khi chính tương tác — có được gọi không, với gì — là yêu cầu.)
- Test pass một mình, fail khi chơi cùng. Nghi phạm đầu tiên? (Static dùng chung, singleton, thứ tự ngầm.)
""",
    r"""
## Vì sao cần double

Unit test không được cần mạng, database hay file system. Nó cần *hành vi*
của những thứ đó, do test kiểm soát. **Test double** là đối tượng thay thế
cung cấp điều đó. Đảo ngược phụ thuộc bạn xây ở Module 11 — service phụ thuộc
interface — chính là thứ làm double khả thi: test đưa cho service một hiện
thực khác.

## Phổ double, làm bằng tay

- **Stub** — trả câu trả lời cứng. "Cổng thanh toán chấp nhận." Không có
  trạng thái đáng kiểm tra.
- **Fake** — hiện thực nhẹ hoạt động thật. Repository lưng `Dictionary` đứng
  chỗ repository SQL. Service không phân biệt được, và test quan sát được
  hành vi thật.
- **Mock** — ghi lại *tương tác* để kiểm chứng sau: "Reserve được gọi đúng
  một lần với sku=tea". Dùng khi chính tương tác là yêu cầu (tác dụng phụ),
  không phải dữ liệu.

```csharp
public interface IPaymentGateway { bool Charge(decimal amount); }

public sealed class StubGateway : IPaymentGateway          // stub
{
    public bool Result = true;
    public bool Charge(decimal amount) => Result;
}

public sealed class MockGateway : IPaymentGateway          // mock
{
    public int Calls;
    public decimal LastAmount;
    public bool Charge(decimal amount) { Calls++; LastAmount = amount; return true; }
}
```

Fake là lao động chính; mock đáng giá khi *cuộc gọi* là kết quả. Lời dùng
thư viện mocking trước khi viết hai cái bằng tay là cách người ta quay ra
test cái mock thay vì test code.

## Cô lập: mỗi test một thế giới mới

Sự mục rữa kinh điển: test chạy một mình thì pass, chạy trong bộ thì fail —
hoặc ngược lại. Nguyên nhân gần như luôn là trạng thái có thể thay đổi dùng
chung:

- một trường `static` hoặc cache trên service;
- một singleton mà service thay đổi;
- thứ tự: test B phụ thuộc thứ test A tạo ra.

Các luật phòng ngừa: instance mới mỗi test (khối Arrange tự dựng thế giới
của nó), không static giữ trạng thái, không test nào phụ thuộc test khác đã
chạy. Trong framework thật, *thứ tự* test là không xác định — bất kỳ thứ gì
cần thứ tự đều là lỗi.

## Kiểm tra hiểu biết

- Stub khác fake? (Stub trả giá trị đóng sẵn; fake là hiện thực nhẹ hoạt động thật.)
- Khi nào mock là lựa chọn đúng? (Khi chính tương tác — có được gọi không, với gì — là yêu cầu.)
- Test pass một mình, fail khi chơi cùng. Nghi phạm đầu tiên? (Static dùng chung, singleton, thứ tự ngầm.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p16-testing",
    "Testing Practice: Runner, Assertions, Isolation",
    "Build the runner, extend the assertion set, and debug a service that fails only when tests share a process.",
    "Luyện Kiểm thử: Runner, Assertion, Cô lập",
    "Xây runner, mở rộng bộ assertion, và debug một service chỉ hỏng khi các test dùng chung tiến trình.",
    "test-doubles",
    32,
    "intermediate",
    [
        challenge(
            "csi-p16-mini-runner",
            "Build the Runner",
            """Implement `TestSummary` and `Solution.Run` — the heart of a test framework: run every test, catch everything, keep going after failures, and record each failure as `name: message`.

```csharp
public sealed class TestSummary { public int Passed; public int Failed; public List<string> Failures = new(); }
static TestSummary Run(IEnumerable<(string Name, Action Body)> tests);
```""",
            CS_PRELUDE,
            [
                (
                    "runs every test and reports all failures",
                    r"""
var log = new System.Collections.Generic.List<string>();
var summary = Solution.Run(new System.Collections.Generic.List<(string, Action)>
{
    ("pass-one", () => log.Add("a")),
    ("boom", () => throw new System.InvalidOperationException("nope")),
    ("pass-two", () => log.Add("b")),
});
Cj.Eq(summary.Passed, 2, "two passing tests");
Cj.Eq(summary.Failed, 1, "one failing test");
Cj.Eq(summary.Failures.Count, 1, "failure recorded once");
Cj.True(summary.Failures[0].Contains("boom"), "failure names the test");
Cj.True(summary.Failures[0].Contains("nope"), "failure carries the message");
Cj.Eq(log.Count, 2, "runner continued past the failure");
""",
                    "foreach with try/catch around body(); on catch, Failed++ and add name + \": \" + ex.Message.",
                ),
                (
                    "all green summary",
                    r"""
var summary = Solution.Run(new System.Collections.Generic.List<(string, Action)>
{
    ("t1", () => { }),
    ("t2", () => { }),
});
Cj.Eq(summary.Passed, 2, "both passed");
Cj.Eq(summary.Failed, 0, "none failed");
Cj.Eq(summary.Failures.Count, 0, "no failures listed");
""",
                    "Same loop — the catch path simply never runs.",
                ),
                (
                    "any exception type counts as a failure",
                    r"""
var summary = Solution.Run(new System.Collections.Generic.List<(string, Action)>
{
    ("fails-with-custom", () => throw new Exception("custom boom")),
});
Cj.Eq(summary.Failed, 1, "custom exception still a failure");
Cj.True(summary.Failures[0].Contains("custom boom"), "message preserved");
""",
                    "Catch Exception, not a specific type.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p16-assertions",
            "Extend the Assertion Set",
            """Two assertions every framework needs: `Throws<T>` (true iff the action throws exactly `T` or a subclass — other exception types must propagate as a `false`-ish *result*, not escape) and `SeqEq<T>` (value equality over two sequences, including null handling).

```csharp
static bool Throws<T>(Action a) where T : Exception;
static bool SeqEq<T>(IEnumerable<T>? a, IEnumerable<T>? b);   // null == null → true; one null → false
```""",
            CS_PRELUDE,
            [
                (
                    "throws matches the exact type",
                    r"""
Cj.True(Solution.Throws<System.InvalidOperationException>(
    () => throw new System.InvalidOperationException("x")), "matching type -> true");
Cj.False(Solution.Throws<System.ArgumentException>(
    () => throw new System.InvalidOperationException("x")), "different exception type -> false");
Cj.False(Solution.Throws<System.InvalidOperationException>(() => { }), "no throw -> false");
""",
                    "catch (T) return true; catch (other) return false; fall through the try for false.",
                ),
                (
                    "throws accepts subclasses of T",
                    r"""
Cj.True(Solution.Throws<System.Exception>(
    () => throw new System.InvalidOperationException("x")), "subclass counts as T");
""",
                    "The catch filter catches T and anything derived from it.",
                ),
                (
                    "seqeq compares by value",
                    r"""
Cj.True(Solution.SeqEq(new int[] { 1, 2, 3 }, new System.Collections.Generic.List<int> { 1, 2, 3 }), "array vs list, same values");
Cj.False(Solution.SeqEq(new int[] { 1, 2 }, new System.Collections.Generic.List<int> { 1, 2, 3 }), "length mismatch");
Cj.False(Solution.SeqEq(new string[] { "a" }, new System.Collections.Generic.List<string> { "b" }), "element mismatch");
""",
                    "Walk both sequences in lockstep (or use SequenceEqual); compare elements with EqualityComparer<T>.Default.",
                ),
                (
                    "seqeq null handling",
                    r"""
Cj.True(Solution.SeqEq<int>(null, null), "null == null -> true");
Cj.False(Solution.SeqEq<int>(null, new System.Collections.Generic.List<int>()), "null vs empty -> false");
Cj.False(Solution.SeqEq<int>(new System.Collections.Generic.List<int>(), null), "empty vs null -> false");
""",
                    "Handle nulls first: both null true; exactly one null false.",
                ),
            ],
            difficulty="intermediate",
        ),
        challenge(
            "csi-p16-test-isolation",
            "Debug: Passes Alone, Fails Together",
            """`OrderService` behaves correctly when each test runs in its own process — but back-to-back calls across *different service instances* see ghosts of each other. Find the root cause and fix it: the service must depend only on its injected `IOrderStore`, hold no state outside the instance, and every call must see fresh data from the store it was given.

```csharp
public static class Solution { public sealed class OrderService { public OrderService(IOrderStore store); public string PlaceOrder(string sku, int qty); } }  // PlaceOrder -> "ok" | "outofstock"
```""",
            CS_PRELUDE + (
                "\n"
                "// Provided infrastructure — do not modify.\n"
                "public interface IOrderStore\n"
                "{\n"
                "    int GetStock(string sku);\n"
                "    void Reserve(string sku, int qty);\n"
                "}\n"
                "\n"
                "public sealed class SqlOrderStore : IOrderStore   // the \"real\" backend, simulated\n"
                "{\n"
                "    public System.Collections.Generic.Dictionary<string, int> Stock = new();\n"
                "    public System.Collections.Generic.List<string> Reservations = new();\n"
                "    public int GetStock(string sku) => Stock.TryGetValue(sku, out var n) ? n : 0;\n"
                "    public void Reserve(string sku, int qty) => Reservations.Add(sku + \":\" + qty);\n"
                "}\n"
            ),
            [
                (
                    "service behaves against a fresh store",
                    r"""
var real = new SqlOrderStore();
real.Stock["widget"] = 5;
var svc = new Solution.OrderService(real);
Cj.Eq(svc.PlaceOrder("widget", 3), "ok", "in stock");
Cj.Eq(real.Reservations.Count, 1, "reservation recorded on the injected store");
Cj.Eq(svc.PlaceOrder("widget", 9), "outofstock", "too many");
Cj.Eq(real.Reservations.Count, 1, "no reservation when out of stock");
""",
                    "Constructor stores the IOrderStore; PlaceOrder reads GetStock, reserves only on success.",
                ),
                (
                    "no state leaks between instances",
                    r"""
var first = new SqlOrderStore();
first.Stock["widget"] = 5;
var svc1 = new Solution.OrderService(first);
Cj.Eq(svc1.PlaceOrder("widget", 3), "ok", "first store ok");

var second = new SqlOrderStore();
second.Stock["widget"] = 0;
var svc2 = new Solution.OrderService(second);
Cj.Eq(svc2.PlaceOrder("widget", 3), "outofstock", "second store sees only its own data");
""",
                    "A second instance with a second store must be completely unaffected by the first — no shared cache, no statics.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p16-mini-runner": vi_challenge(
            "Xây Runner",
            "Hiện thực TestSummary và Solution.Run — trái tim của test framework: chạy mọi test, bắt mọi exception, chạy tiếp qua lỗi, ghi mỗi lỗi thành \"tên: thông điệp\".",
            [
                ("runs every test and reports all failures", "foreach với try/catch quanh body(); khi bắt được, Failed++ và thêm name + \": \" + ex.Message."),
                ("all green summary", "Cùng vòng lặp — nhánh catch đơn giản không chạy."),
                ("any exception type counts as a failure", "Bắt Exception, không bắt kiểu cụ thể."),
            ],
        ),
        "csi-p16-assertions": vi_challenge(
            "Mở rộng Bộ Assertion",
            "Hai assertion mọi framework cần: Throws<T> (true khi và chỉ khi action ném đúng T hoặc lớp con — kiểu khác phải cho kết quả false, không thoát ra) và SeqEq<T> (bằng giá trị trên hai chuỗi, gồm cả xử lý null).",
            [
                ("throws matches the exact type", "catch (T) return true; catch (khác) return false; hết try thì false."),
                ("throws accepts subclasses of T", "Bộ lọc catch bắt T và mọi lớp dẫn xuất."),
                ("seqeq compares by value", "Đi song song hai chuỗi (hoặc dùng SequenceEqual); so phần tử bằng EqualityComparer<T>.Default."),
                ("seqeq null handling", "Xử lý null trước: cả hai null → true; đúng một null → false."),
            ],
        ),
        "csi-p16-test-isolation": vi_challenge(
            "Debug: Đơn Là Pass, Cụm Là Fail",
            "OrderService đúng khi mỗi test chạy tiến trình riêng — nhưng các lần gọi nối tiếp qua KHÁC instance service nhìn thấy bóng của nhau. Tìm nguyên nhân gốc và sửa: service chỉ được dựa vào IOrderStore được inject, không giữ trạng thái ngoài instance, mọi lần gọi thấy dữ liệu mới từ store của nó.",
            [
                ("service behaves against a fresh store", "Constructor giữ IOrderStore; PlaceOrder đọc GetStock, chỉ Reserve khi thành công."),
                ("no state leaks between instances", "Instance thứ hai với store thứ hai phải hoàn toàn không bị ảnh hưởng — không cache dùng chung, không static."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p16-mini-runner",
            'public sealed class TestSummary\n{\n    public int Passed;\n    public int Failed;\n    public System.Collections.Generic.List<string> Failures = new();\n}\n\npublic static class Solution\n{\n    public static TestSummary Run(System.Collections.Generic.IEnumerable<(string Name, Action Body)> tests)\n    {\n        var summary = new TestSummary();\n        foreach (var (name, body) in tests)\n        {\n            try { body(); summary.Passed++; }\n            catch (Exception ex)\n            {\n                summary.Failed++;\n                summary.Failures.Add(name + ": " + ex.Message);\n            }\n        }\n        return summary;\n    }\n}\n',
            'public sealed class TestSummary\n{\n    public int Passed;\n    public int Failed;\n    public System.Collections.Generic.List<string> Failures = new();\n}\n\npublic static class Solution\n{\n    public static TestSummary Run(System.Collections.Generic.IEnumerable<(string Name, Action Body)> tests)\n    {\n        var summary = new TestSummary();\n        foreach (var (name, body) in tests)\n        {\n            try { body(); summary.Passed++; }\n            catch (Exception ex)\n            {\n                summary.Failed++;\n                summary.Failures.Add(name + ": " + ex.Message);\n                // near-miss: bails out at the first failure — everything\n                // behind it goes unreported\n                return summary;\n            }\n        }\n        return summary;\n    }\n}\n',
        ),
        (
            "csi-p16-assertions",
            'public static class Solution\n{\n    public static bool Throws<T>(Action a) where T : Exception\n    {\n        try { a(); return false; }\n        catch (T) { return true; }\n        catch (Exception) { return false; }\n    }\n\n    public static bool SeqEq<T>(System.Collections.Generic.IEnumerable<T>? a, System.Collections.Generic.IEnumerable<T>? b)\n    {\n        if (a is null || b is null) return a is null && b is null;\n        var ea = a.GetEnumerator();\n        var eb = b.GetEnumerator();\n        try\n        {\n            while (true)\n            {\n                var ha = ea.MoveNext();\n                var hb = eb.MoveNext();\n                if (ha != hb) return false;\n                if (!ha) return true;\n                if (!System.Collections.Generic.EqualityComparer<T>.Default.Equals(ea.Current, eb.Current)) return false;\n            }\n        }\n        finally { ea.Dispose(); eb.Dispose(); }\n    }\n}\n',
            'public static class Solution\n{\n    public static bool Throws<T>(Action a) where T : Exception\n    {\n        try { a(); return false; }\n        // near-miss: swallows every exception type — a wrong exception\n        // counts as "threw correctly"\n        catch (Exception) { return true; }\n    }\n\n    public static bool SeqEq<T>(System.Collections.Generic.IEnumerable<T>? a, System.Collections.Generic.IEnumerable<T>? b)\n    {\n        if (a is null || b is null) return a is null && b is null;\n        // near-miss: compares lengths only — {"a"} equals {"b"}\n        return a.Count() == b.Count();\n    }\n}\n',
        ),
        (
            "csi-p16-test-isolation",
            'public static class Solution\n{\n    public sealed class OrderService\n    {\n        private readonly IOrderStore _store;\n\n        public OrderService(IOrderStore store) => _store = store;\n\n        public string PlaceOrder(string sku, int qty)\n        {\n            if (_store.GetStock(sku) < qty) return "outofstock";\n            _store.Reserve(sku, qty);\n            return "ok";\n        }\n    }\n}\n',
            'public static class Solution\n{\n    public sealed class OrderService\n    {\n        private readonly IOrderStore _store;\n        // near-miss: static cache — instance two reuses instance one\'s stock,\n        // so tests poison each other\n        private static readonly System.Collections.Generic.Dictionary<string, int> Cache = new();\n\n        public OrderService(IOrderStore store) => _store = store;\n\n        public string PlaceOrder(string sku, int qty)\n        {\n            if (!Cache.ContainsKey(sku)) Cache[sku] = _store.GetStock(sku);\n            if (Cache[sku] < qty) return "outofstock";\n            _store.Reserve(sku, qty);\n            return "ok";\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m16",
    "Checkpoint — The Self-Verifying Suite",
    "Compose it: a fake double, a service behind an interface, and a test suite that actually catches broken implementations.",
    25,
    r"""
## The gate (mini-build)

Three pieces, one file:

1. `IInventory` — `int GetStock(string sku)`, `void Reserve(string sku, int qty)`.
2. `FakeInventory : IInventory` — the fake: `Dictionary<string,int> Stock`
   (missing sku = 0), `List<string> Reservations`, plus two fault hooks:
   `LyingStock` (when true, `GetStock` returns the real value **+ 1000**) and
   `BrokenReserve` (when true, `Reserve` records nothing).
3. `OrderService(IInventory)` — `PlaceOrder(sku, qty)` → "ok" | "outofstock";
   reserves only on success.
4. `CheckAll(FakeInventory inv)` — a small suite (≥ 3 tests) that verifies:
   the ok path reserves, the out-of-stock path does not reserve, and qty
   exactly equal to stock still succeeds. Returns the list of failure
   messages — **empty means every test passed**. The suite must genuinely
   test the *injected* inventory: handed a lying or broken fake, it must
   report failures, not happy-face an empty list.
""",
    "Checkpoint — Bộ Tự Kiểm chứng",
    "Ghép tất cả: fake double, service sau interface, và bộ test thật sự bắt được hiện thực hỏng.",
    r"""
## Cổng kiểm tra (mini-build)

Ba mảnh, một file:

1. `IInventory` — `int GetStock(string sku)`, `void Reserve(string sku, int qty)`.
2. `FakeInventory : IInventory` — fake: `Dictionary<string,int> Stock`
   (sku thiếu = 0), `List<string> Reservations`, cùng hai móc lỗi:
   `LyingStock` (true → `GetStock` trả giá trị thật **+ 1000**) và
   `BrokenReserve` (true → `Reserve` không ghi gì).
3. `OrderService(IInventory)` — `PlaceOrder(sku, qty)` → "ok" | "outofstock";
   chỉ Reserve khi thành công.
4. `CheckAll(FakeInventory inv)` — một bộ test nhỏ (≥ 3 test) xác minh: đường
   ok có Reserve, đường hết hàng không Reserve, và qty đúng bằng stock vẫn
   thành công. Trả danh sách thông điệp lỗi — **rỗng nghĩa là mọi test pass**.
   Bộ test phải thật sự kiểm tra inventory được inject: đưa fake nói dối hoặc
   hỏng, nó phải báo lỗi, không được vui vẻ trả danh sách rỗng.
""",
    challenge(
        "csi-checkpoint-m16-task",
        "Checkpoint: Suite That Catches",
        """Implement the pieces described in the checkpoint:

```csharp
public interface IInventory { int GetStock(string sku); void Reserve(string sku, int qty); }
public static class Solution
{
    public sealed class FakeInventory : IInventory
    {
        public System.Collections.Generic.Dictionary<string, int> Stock = new();
        public System.Collections.Generic.List<string> Reservations = new();
        public bool LyingStock;    // GetStock returns true value + 1000
        public bool BrokenReserve; // Reserve records nothing
    }
    public sealed class OrderService { public OrderService(IInventory inv); public string PlaceOrder(string sku, int qty); }
    public static System.Collections.Generic.List<string> CheckAll(FakeInventory inv);
}
```""",
        CS_PRELUDE,
        [
            (
                "suite passes a correct fake",
                r"""
var inv = new Solution.FakeInventory();
inv.Stock["sku"] = 10;
var failures = Solution.CheckAll(inv);
Cj.Eq(failures.Count, 0, "correct inventory -> suite green");
""",
                    "Your suite's tests must all hold on a well-behaved fake.",
                ),
                (
                    "suite catches a lying stock report",
                    r"""
var inv = new Solution.FakeInventory();
inv.Stock["sku"] = 0;
inv.LyingStock = true;
var failures = Solution.CheckAll(inv);
Cj.True(failures.Count > 0, "lying stock must be detected");
""",
                    "With LyingStock, GetStock reports 1000 for an empty sku — at least one suite test must notice.",
                ),
                (
                    "suite catches a broken reservation",
                    r"""
var inv = new Solution.FakeInventory();
inv.Stock["sku"] = 10;
inv.BrokenReserve = true;
var failures = Solution.CheckAll(inv);
Cj.True(failures.Count > 0, "lost reservation must be detected");
""",
                    "With BrokenReserve, the ok-path reservation vanishes — the suite must check Reservations, not just the returned string.",
                ),
                (
                    "service honors the injected interface",
                    r"""
var inv = new Solution.FakeInventory();
inv.Stock["sku"] = 4;
var svc = new Solution.OrderService(inv);
Cj.Eq(svc.PlaceOrder("sku", 4), "ok", "exact stock still succeeds");
Cj.Eq(inv.Reservations.Count, 1, "reserved once");
Cj.Eq(svc.PlaceOrder("sku", 5), "outofstock", "one over the top");
Cj.Eq(inv.Reservations.Count, 1, "no reservation on failure");
""",
                    "Boundary: qty == stock succeeds; qty == stock + 1 fails without reserving.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Bộ Bắt Được Lỗi",
            "Hiện thực các mảnh trong checkpoint: IInventory; FakeInventory (Stock mặc định 0, móc lỗi LyingStock +1000 và BrokenReserve bỏ qua ghi); OrderService(IInventory) — PlaceOrder trả \"ok\"/\"outofstock\", chỉ Reserve khi thành công; CheckAll(FakeInventory) — bộ test ≥ 3 ca xác minh Reserve đúng, hết hàng không Reserve, ranh giới qty == stock vẫn ok, trả danh sách lỗi (rỗng = xanh). Bộ test phải bắt được fake nói dối hoặc hỏng.",
            [
                ("suite passes a correct fake", "Mọi test của bộ phải đúng trên fake hoạt động chuẩn."),
                ("suite catches a lying stock report", "LyingStock báo 1000 cho sku rỗng — ít nhất một test phải nhận ra."),
                ("suite catches a broken reservation", "BrokenReserve làm biến mất Reserve của đường ok — bộ phải kiểm tra Reservations, không chỉ chuỗi trả về."),
                ("service honors the injected interface", "Ranh giới: qty == stock thành công; qty == stock + 1 thất bại và không Reserve."),
            ],
        ),
        solution='public static class Solution\n{\n    public interface IInventory\n    {\n        int GetStock(string sku);\n        void Reserve(string sku, int qty);\n    }\n\n    public sealed class FakeInventory : IInventory\n    {\n        public System.Collections.Generic.Dictionary<string, int> Stock = new();\n        public System.Collections.Generic.List<string> Reservations = new();\n        public bool LyingStock;\n        public bool BrokenReserve;\n\n        public int GetStock(string sku)\n        {\n            int n = Stock.TryGetValue(sku, out var v) ? v : 0;\n            return LyingStock ? n + 1000 : n;\n        }\n\n        public void Reserve(string sku, int qty)\n        {\n            if (BrokenReserve) return;\n            Reservations.Add(sku + ":" + qty);\n        }\n    }\n\n    public sealed class OrderService\n    {\n        private readonly IInventory _inv;\n        public OrderService(IInventory inv) => _inv = inv;\n\n        public string PlaceOrder(string sku, int qty)\n        {\n            if (_inv.GetStock(sku) < qty) return "outofstock";\n            _inv.Reserve(sku, qty);\n            return "ok";\n        }\n    }\n\n    public static System.Collections.Generic.List<string> CheckAll(FakeInventory inv)\n    {\n        var failures = new System.Collections.Generic.List<string>();\n        // seed the injected fake — a suite owns its fixture state\n        inv.Stock["check:ok"] = 5;\n        inv.Stock["check:exact"] = 3;\n\n            // 1. ok path reserves\n            var svc = new OrderService(inv);\n            var r1 = svc.PlaceOrder("check:ok", 2);\n            if (r1 != "ok" || inv.Reservations.Count != 1)\n                failures.Add("PlaceOrder_ok_reserves: expected one reservation, got " + inv.Reservations.Count);\n\n            // 2. out-of-stock does not reserve\n            var r2 = svc.PlaceOrder("check:empty", 1);\n            if (r2 != "outofstock" || inv.Reservations.Count != 1)\n                failures.Add("PlaceOrder_outofstock_does_not_reserve: got " + r2 + ", reservations " + inv.Reservations.Count);\n\n            // 3. boundary: qty exactly == stock succeeds\n            var r3 = svc.PlaceOrder("check:exact", 3);\n            if (r3 != "ok")\n                failures.Add("PlaceOrder_exact_stock_succeeds: got " + r3);\n\n            return failures;\n    }\n}\n',
            wrong='public static class Solution\n{\n    public interface IInventory\n    {\n        int GetStock(string sku);\n        void Reserve(string sku, int qty);\n    }\n\n    public sealed class FakeInventory : IInventory\n    {\n        public System.Collections.Generic.Dictionary<string, int> Stock = new();\n        public System.Collections.Generic.List<string> Reservations = new();\n        public bool LyingStock;\n        public bool BrokenReserve;\n\n        public int GetStock(string sku)\n        {\n            int n = Stock.TryGetValue(sku, out var v) ? v : 0;\n            return LyingStock ? n + 1000 : n;\n        }\n\n        public void Reserve(string sku, int qty)\n        {\n            if (BrokenReserve) return;\n            Reservations.Add(sku + ":" + qty);\n        }\n    }\n\n    public sealed class OrderService\n    {\n        private readonly IInventory _inv;\n        public OrderService(IInventory inv) => _inv = inv;\n\n        public string PlaceOrder(string sku, int qty)\n        {\n            if (_inv.GetStock(sku) < qty) return "outofstock";\n            _inv.Reserve(sku, qty);\n            return "ok";\n        }\n    }\n\n    public static System.Collections.Generic.List<string> CheckAll(FakeInventory inv)\n    {\n        var failures = new System.Collections.Generic.List<string>();\n        // seed the injected fake — a suite owns its fixture state\n        inv.Stock["check:ok"] = 5;\n        inv.Stock["check:exact"] = 3;\n            try\n            {\n                var svc = new OrderService(inv);\n                svc.PlaceOrder("check:ok", 2);\n                svc.PlaceOrder("check:empty", 1);\n                svc.PlaceOrder("check:exact", 3);\n            }\n            catch { }\n            // near-miss: the suite runs but asserts nothing — it can never\n            // fail, so it "passes" broken implementations too\n            return failures;\n    }\n}\n',
    ),
print("module 16 authored")
