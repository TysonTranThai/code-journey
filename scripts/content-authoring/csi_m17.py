#!/usr/bin/env python3
"""C# — Intermediate — Module 17: csi-clean-code.

Clean code & refactoring: smells, naming, guard clauses, SRP, and
behavior-preserving refactoring against frozen tests. Ws are plausible
partial fixes / subtle behavior changes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-clean-code"

write_module(
    M,
    "Clean Code & Refactoring",
    "Name things honestly, kill nesting with guard clauses, split god methods — and refactor without changing behavior, guarded by tests.",
    "Code Sạch & Tái cấu trúc",
    "Đặt tên trung thực, phá bỏ lồng ghép bằng guard clause, tách god method — và tái cấu trúc mà không đổi hành vi, được bảo vệ bởi test.",
    ["code-smells", "refactoring", "csi-checkpoint-m17"],
    ["csi-p17-clean-code"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "code-smells",
    "Reading Smelly Code",
    "The six smells you will meet in every real codebase, and the naming rules that prevent half of them.",
    20,
    r"""
## Smells are symptoms, not sins

A *code smell* is a surface sign that something deeper is wrong. You cannot
memorize them into irrelevance — you train your eye on the classics:

| Smell | Looks like | Usually means |
|---|---|---|
| Long method | 60 lines, blank-line "chapters" | doing 3 jobs; extract methods |
| Magic numbers | `if (age > 18 && level > 4)` | unnamed policy; name it |
| Duplication | same 6 lines in 3 places | one rule, copied; extract once |
| Deep nesting | 5 levels of `if`/`foreach` | missing guard clauses |
| God class | `OrderManager` also sends email | many responsibilities (SRP) |
| Flag arguments | `Save(order, true)` | two behaviors in one method |

The single highest-value habit: **when you cannot name a block, you do not
understand it yet** — and neither will the next reader.

## Naming rules that earn their keep

- **Names state intent, not type**: `remainingBalance`, not `remainingDec`.
- **Booleans read as predicates**: `isSuspended`, `hasItems`, `canRefund`.
- **Methods are verbs**; the name says what it *does*: `CalculateTax`, not
  `TaxData`.
- **One vocabulary per concept**. `customer`, `client`, `buyer` in the same
  file means three words for one thing — pick one.
- **Misleading names are worse than bad names**: a method named `GetTotal`
  that also writes to the database will be called in the wrong place, by
  someone who trusted you.

## Guard clauses: flatten the pyramid

Deep nesting accumulates edge-case handling and business logic in one pile.
Guard clauses invert it — handle the degenerate cases *first*, exit early,
and leave the happy path unindented and readable:

```csharp
// before: the pyramid
public string Label(Order? order)
{
    if (order != null)
    {
        if (order.Items.Count > 0)
        {
            return order.Customer + " x" + order.Items.Count;
        }
        else { return "empty"; }
    }
    else { return "none"; }
}

// after: guards first, happy path last
public string Label(Order? order)
{
    if (order is null) return "none";
    if (order.Items.Count == 0) return "empty";
    return order.Customer + " x" + order.Items.Count;
}
```

Same behavior, one indent level, and every edge case is greppable on its own
line.

## Cohesion, coupling, SRP

- **Cohesion** — how much a type's members belong to one job. High cohesion:
  every method of `InvoiceCalculator` computes something about invoices.
- **Coupling** — how much a type needs to know about other types. `Invoice`
  knowing about `SmtpClient` is coupling you do not need.
- **Single Responsibility Principle** — one reason to change per type. The
  test: "why would this class change?" If the answer has "and" in it
  ("when tax rules change *and* when the email template changes"), split it.

You will exercise all of these by refactoring, next lesson.
""",
    "Đọc Mã có Mùi",
    "Sáu mùi code bạn sẽ gặp trong mọi codebase thật, và quy tắc đặt tên ngăn được một nửa trong số đó.",
    r"""
## Mùi là triệu chứng, không phải tội lỗi

*Code smell* là dấu hiệu bề mặt cho thấy thứ gì đó sâu hơn đang sai. Không thể
thuộc lòng rồi bỏ qua — bạn phải luyện mắt trên các loại kinh điển:

| Mùi | Trông như | Thường có nghĩa là |
|---|---|---|
| Method dài | 60 dòng, "chương" cách bằng dòng trắng | làm 3 việc; tách method |
| Magic number | `if (age > 18 && level > 4)` | chính sách không tên; đặt tên |
| Trùng lặp | cùng 6 dòng ở 3 chỗ | một quy tắc, copy; tách một lần |
| Lồng sâu | 5 tầng `if`/`foreach` | thiếu guard clause |
| God class | `OrderManager` cũng gửi email | nhiều trách nhiệm (SRP) |
| Tham số cờ | `Save(order, true)` | hai hành vi trong một method |

Thói quen giá trị nhất: **khi bạn không gọi được tên cho một khối, bạn chưa
hiểu nó** — và người đọc sau cũng vậy.

## Quy tắc đặt tên đáng công sức

- **Tên nói mục đích, không nói kiểu**: `remainingBalance`, không phải
  `remainingDec`.
- **Boolean đọc như vị từ**: `isSuspended`, `hasItems`, `canRefund`.
- **Method là động từ**; tên nói nó *làm gì*: `CalculateTax`, không phải
  `TaxData`.
- **Một khái niệm, một từ vựng**. `customer`, `client`, `buyer` trong cùng
  file nghĩa là ba từ cho một thứ — chọn một.
- **Tên gây hiểu lầm tệ hơn tên xấu**: method tên `GetTotal` mà cũng ghi vào
  database sẽ bị gọi sai chỗ, bởi người đã tin bạn.

## Guard clause: san phẳng kim tự tháp

Lồng sâu khiến xử lý edge case và logic nghiệp vụ dồn thành một đống. Guard
clause đảo ngược điều đó — xử lý trường hợp suy biến *trước*, thoát sớm, để
đường chính không thụt lề và dễ đọc (xem ví dụ `Label` trong bản tiếng Anh —
cùng hành vi, một mức thụt lề, mỗi edge case một dòng).

## Cohesion, coupling, SRP

- **Cohesion** — các thành viên của một type thuộc về một việc đến đâu.
  Cohesion cao: mọi method của `InvoiceCalculator` tính gì đó về invoice.
- **Coupling** — một type cần biết gì về type khác. `Invoice` biết về
  `SmtpClient` là coupling bạn không cần.
- **Single Responsibility Principle** — mỗi type một lý do thay đổi. Bài
  test: "class này vì sao đổi?" Nếu câu trả lời có "và" ("khi luật thuế đổi
  *và* khi email template đổi"), tách nó.

Bạn sẽ luyện tất cả bằng tái cấu trúc ở bài sau.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "refactoring",
    "Refactoring Under Guard",
    "Behavior-preserving change in small verified steps — with the test suite as the safety net, not an afterthought.",
    22,
    r"""
## Refactoring has one definition

> To refactor is to change the *structure* of code without changing its
> *behavior*.

Not cleanup. Not "improvements while I'm in here". If behavior changes, it is
a bug fix or a feature — a different activity with different review needs.
Mixing the two in one change is how regressions hide.

## The harness: tests first, always

You cannot safely refactor unverified code, so the workflow is:

1. **Freeze behavior with tests.** Run the code as-is, pin the interesting
   inputs and outputs in tests (including edge cases — they are where
   refactors bleed).
2. **One move at a time.** Extract a method, run the tests. Rename, run.
   Each step compiles and stays green.
3. **Commit-sized steps.** Small green steps compose; one big-bang rewrite
   does not.

If you cannot write a failing-then-passing test around the behavior you are
about to restructure, you are not refactoring — you are gambling.

## The starter catalog

| Move | When |
|---|---|
| Extract method | block has a nameable single purpose |
| Replace magic number with constant | `0.20m` → `GoldDiscount` |
| Guard clause | nested `if` only guards a degenerate case |
| Decompose conditional | a long condition gets a well-named method |
| Introduce parameter object | the same 4 values travel together everywhere |

```csharp
// decompose conditional
public bool CanBulkDiscount(Order o) =>
    o.Qty >= BulkThreshold && o.Tier != Tier.Vip;   // named, testable
```

## When NOT to refactor

- The code is about to be deleted — refactoring it is negative work.
- You have no tests and no time to write them — do the smallest safe change;
  schedule the refactor.
- The behavior itself is wrong — fix the bug first, *then* clean the shape.
  Refactoring a wrong behavior just makes the wrong thing prettier.

Refactoring is how a codebase stays maintainable while it grows — the next
modules (patterns, architecture) assume you can restructure safely.
""",
    "Tái cấu trúc dưới Bảo hộ",
    "Thay đổi cấu trúc mà giữ nguyên hành vi, từng bước nhỏ có kiểm chứng — với bộ test là lưới an toàn, không phải phần nghĩ sau.",
    r"""
## Tái cấu trúc chỉ có một định nghĩa

> Tái cấu trúc là thay đổi *cấu trúc* của code mà không thay đổi *hành vi*.

Không phải dọn dẹp. Không phải "tiện tay cải tiến". Nếu hành vi đổi, đó là fix
bug hay thêm tính năng — một hoạt động khác với nhu cầu review khác. Trộn hai
việc trong một thay đổi là cách regression ẩn mình.

## Lưới an toàn: test trước, luôn luôn

Không thể tái cấu trúc an toàn trên code chưa được kiểm chứng, nên quy trình
là:

1. **Đóng băng hành vi bằng test.** Chạy code hiện tại, ghim các cặp
   input/output thú vị vào test (kể cả edge case — đó là nơi refactor rỉ máu).
2. **Mỗi lần một nước đi.** Tách method, chạy test. Đổi tên, chạy test. Mỗi
   bước biên dịch được và giữ màu xanh.
3. **Bước cỡ một commit.** Các bước xanh nhỏ ghép được với nhau; viết lại một
   phát ăn ngay thì không.

Nếu không viết nổi test quanh hành vi sắp bị tái cấu trúc, bạn không phải
đang refactor — bạn đang đánh bạc.

## Catalog khởi đầu

| Nước đi | Khi nào |
|---|---|
| Extract method | khối có một mục đích gọi được tên |
| Magic number → hằng số | `0.20m` → `GoldDiscount` |
| Guard clause | `if` lồng chỉ bảo vệ trường hợp suy biến |
| Decompose conditional | điều kiện dài thành method có tên tốt |
| Introduce parameter object | cùng 4 giá trị đi cùng nhau khắp nơi |

## Khi nào KHÔNG refactor

- Code sắp bị xóa — refactor nó là việc âm.
- Không có test và không có thời gian viết — làm thay đổi nhỏ an toàn nhất;
  lên lịch refactor sau.
- Hành vi sai — sửa bug trước, *rồi* dọn hình dạng. Refactor hành vi sai chỉ
  làm thứ sai trông đẹp hơn.

Tái cấu trúc giúp codebase giữ được khả năng bảo trì khi lớn lên — các module
sau (patterns, architecture) mặc định bạn tái cấu trúc an toàn được.
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p17-clean-code",
    "Clean Code Practice: Guards, Totals, Reports",
    "Accumulate validation errors with guard clauses, build a money total from named pieces, and debug a report generator that remembers too much.",
    "Luyện Code Sạch: Guard, Tổng tiền, Báo cáo",
    "Tích lũy lỗi validation bằng guard clause, dựng tổng tiền từ các mảnh có tên, và debug một report generator nhớ quá nhiều.",
    "refactoring",
    30,
    "intermediate",
    [
        challenge(
            "csi-p17-guard-clauses",
            "Guard Clauses that Accumulate",
            r"""Implement `Validate` with guard clauses. Unlike fail-fast validation, this one **accumulates every violation in a fixed order**:

1. `order` itself null → `"order"`
2. `Customer` null/empty → `"customer"`
3. no items → `"items"`
4. each negative-qty item, in order → `"qty:" + index` (0-based)

Valid input → an empty list. Guard clauses keep each rule on one line; the
rules still *all* run (except when a earlier rule makes a later one
meaningless — null order has no items to inspect).

```csharp
public static class Solution { public static System.Collections.Generic.List<string> Validate(Solution.Order? order); }
```""",
            CS_PRELUDE + (
                "\n"
                "// Provided infrastructure — do not modify.\n"
                "public sealed class Order\n"
                "{\n"
                "    public string? Customer;\n"
                "    public System.Collections.Generic.List<OrderLine> Items = new();\n"
                "}\n"
                "\n"
                "public sealed class OrderLine\n"
                "{\n"
                "    public string Sku = \"\";\n"
                "    public int Qty;\n"
                "}\n"
            ),
            [
                (
                    "short-circuit precedence",
                    r"""
Cj.Eq(string.Join("|", Solution.Validate(null)), "order", "null order");
var o = new Order();                     // no customer, no items
Cj.Eq(string.Join("|", Solution.Validate(o)), "customer", "customer before items");
""",
                    "Check in the fixed order: order, customer, items. When customer fails, still continue to items? No — the spec: rules 1-3 are a precedence chain, the first that fires wins (return immediately).",
                ),
                (
                    "negative quantities accumulate",
                    r"""
var o = new Order();
o.Customer = "ann";
o.Items.Add(new OrderLine { Sku = "a", Qty = 2 });
o.Items.Add(new OrderLine { Sku = "b", Qty = -1 });
o.Items.Add(new OrderLine { Sku = "c", Qty = 0 });
o.Items.Add(new OrderLine { Sku = "d", Qty = -3 });
Cj.Eq(string.Join("|", Solution.Validate(o)), "qty:1|qty:3", "every negative, in order");
""",
                    "Do NOT stop at the first negative item — keep scanning and add one entry per violation.",
                ),
                (
                    "valid order is empty",
                    r"""
var o = new Order();
o.Customer = "ann";
o.Items.Add(new OrderLine { Sku = "a", Qty = 2 });
o.Items.Add(new OrderLine { Sku = "b", Qty = 0 });
Cj.Eq(Solution.Validate(o).Count, 0, "valid -> empty list");
""",
                    "Zero is a legal quantity — only negatives violate.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p17-extract-total",
            "A Total Built from Named Pieces",
            r"""Money math belongs in small named pieces, not one formula. Implement four methods:

- `Subtotal(lines)` — sum of `Qty * Price`
- `Discount(subtotal, pct)` — `subtotal * pct / 100`
- `Shipping(afterDiscount)` — free (0) when `afterDiscount >= 100`, else `5m`
- `Total(lines, pct)` — `subtotal - discount + Shipping(subtotal - discount)`

The shipping decision reads the **after-discount** amount — that ordering is
the whole point.

```csharp
public static class Solution
{
    public static decimal Subtotal(System.Collections.Generic.IEnumerable<OrderLine> lines);
    public static decimal Discount(decimal subtotal, decimal pct);
    public static decimal Shipping(decimal afterDiscount);
    public static decimal Total(System.Collections.Generic.IEnumerable<OrderLine> lines, decimal pct);
}
```""",
            CS_PRELUDE + (
                "\n"
                "// Provided infrastructure — do not modify.\n"
                "public sealed class OrderLine\n"
                "{\n"
                "    public int Qty;\n"
                "    public decimal Price;\n"
                "}\n"
            ),
            [
                (
                    "pieces compose",
                    r"""
var lines = new List<OrderLine> { new OrderLine { Qty = 2, Price = 30m } };
Cj.Eq(Solution.Subtotal(lines), 60m, "subtotal");
Cj.Eq(Solution.Discount(60m, 10m), 6m, "10pct of 60");
Cj.Eq(Solution.Shipping(54m), 5m, "under threshold ships");
Cj.Eq(Solution.Total(lines, 10m), 59m, "60 - 6 + 5");
""",
                    "Total = afterDiscount + Shipping(afterDiscount). Do the pieces in order.",
                ),
                (
                    "free shipping boundary",
                    r"""
var at = new List<OrderLine> { new OrderLine { Qty = 10, Price = 10m } };   // subtotal 100
Cj.Eq(Solution.Shipping(100m), 0m, "exactly 100 is free");
Cj.Eq(Solution.Total(at, 0m), 100m, "no discount, free ship");
Cj.Eq(Solution.Total(at, 5m), 100m, "95 after discount + 5 ship");
""",
                    "The threshold applies to the AFTER-discount amount: 100 with 5% off is 95, which ships for 5.",
                ),
                (
                    "discount crossing the threshold",
                    r"""
var big = new List<OrderLine> { new OrderLine { Qty = 105, Price = 1m } };  // subtotal 105
Cj.Eq(Solution.Total(big, 10m), 99.5m, "94.5 after discount + 5 ship");
""",
                    "105 at 10% off drops below 100 — shipping re-enters. Getting this right requires reading the after-discount value.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p17-srp-split",
            "Debug: The Generator That Remembers",
            r"""This `ReportGenerator` broke in a code review — reports leak across
instances, and fresh data stops appearing:

```csharp
public sealed class ReportGenerator           // BROKEN — do not ship this
{
    private static readonly List<string> Cache = new();   // shared by ALL instances
    private readonly IFetcher _fetcher;
    public ReportGenerator(IFetcher fetcher) => _fetcher = fetcher;
    public string[] Generate()
    {
        if (Cache.Count == 0)
            foreach (var r in _fetcher.Fetch()) Cache.Add(...);
        return Cache.ToArray();
    }
}
```

Two sins: **static state shared by every instance**, and **caching input
data** the caller expects to be re-read. Write a correct `ReportGenerator`:
no state beyond the injected `IFetcher`, and `Generate()` reflects the
fetcher's *current* rows every call, formatted `"1. row"`, `"2. row"` (1-based).

```csharp
public sealed class ReportGenerator { public ReportGenerator(IFetcher fetcher); public string[] Generate(); }
```""",
            CS_PRELUDE + (
                "\n"
                "// Provided infrastructure — do not modify.\n"
                "public interface IFetcher\n"
                "{\n"
                "    string[] Fetch();\n"
                "}\n"
                "\n"
                "public sealed class InMemoryFetcher : IFetcher\n"
                "{\n"
                "    public System.Collections.Generic.List<string> Rows = new();\n"
                "    public string[] Fetch() => Rows.ToArray();\n"
                "}\n"
            ),
            [
                (
                    "two instances, independent",
                    r"""
var fa = new InMemoryFetcher(); fa.Rows.Add("alpha");
var fb = new InMemoryFetcher(); fb.Rows.Add("beta");
var g1 = new ReportGenerator(fa);
var g2 = new ReportGenerator(fb);
Cj.Eq(string.Join("|", g1.Generate()), "1. alpha", "g1 sees its own fetcher");
Cj.Eq(string.Join("|", g2.Generate()), "1. beta", "g2 sees its own fetcher");
""",
                    "Nothing static, nothing shared. Each generator reads the fetcher it was given.",
                ),
                (
                    "mutation is reflected",
                    r"""
var f = new InMemoryFetcher(); f.Rows.Add("first");
var g = new ReportGenerator(f);
g.Generate();
f.Rows.Add("second");
Cj.Eq(string.Join("|", g.Generate()), "1. first|2. second", "re-reads current rows");
""",
                    "Generate is not a cache: call Fetch every time and format fresh.",
                ),
                (
                    "stable for unchanged data",
                    r"""
var f = new InMemoryFetcher(); f.Rows.Add("x");
var g = new ReportGenerator(f);
var a = g.Generate();
var b = g.Generate();
Cj.True(ReferenceEquals(a, b) || string.Join("|", a) == string.Join("|", b), "stable across calls");
""",
                    "Correct behavior is deterministic — same input, same output, without caching.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p17-guard-clauses": vi_challenge(
            "Guard Clause Tích lũy",
            "Hiện thực `Validate` bằng guard clause. Khác với fail-fast, hàm này **tích lũy mọi vi phạm theo thứ tự cố định**: 1) order null → \"order\"; 2) Customer null/rỗng → \"customer\"; 3) không có item → \"items\"; 4) mỗi item qty âm, theo thứ tự → \"qty:\" + index (tính từ 0). Input hợp lệ → danh sách rỗng.",
            [
                ("short-circuit precedence", "Kiểm tra theo thứ tự cố định: order, customer, items. Quy tắc 1–3 là chuỗi ưu tiên — quy tắc đầu tiên kích hoạt thì trả ngay."),
                ("negative quantities accumulate", "KHÔNG dừng ở item âm đầu tiên — quét tiếp và thêm một dòng cho mỗi vi phạm."),
                ("valid order is empty", "Số 0 hợp lệ — chỉ qty âm là vi phạm."),
            ],
        ),
        "csi-p17-extract-total": vi_challenge(
            "Tổng tiền từ các Mảnh có Tên",
            "Hiện thực 4 method: `Subtotal(lines)` = tổng Qty*Price; `Discount(subtotal, pct)` = subtotal*pct/100; `Shipping(afterDiscount)` = 0 khi afterDiscount ≥ 100, ngược lại 5m; `Total(lines, pct)` = afterDiscount + Shipping(afterDiscount). Quyết định phí ship đọc số SAU giảm giá — trật tự này là điểm cốt lõi.",
            [
                ("pieces compose", "Total = afterDiscount + Shipping(afterDiscount). Làm từng mảnh theo thứ tự."),
                ("free shipping boundary", "Ngưỡng áp cho số SAU giảm giá: 100 giảm 5% còn 95, ship giá 5."),
                ("discount crossing the threshold", "105 giảm 10% rơi xuống dưới 100 — phí ship quay lại. Đúng đòi hỏi đọc giá trị sau giảm giá."),
            ],
        ),
        "csi-p17-srp-split": vi_challenge(
            "Debug: Bộ sinh Báo cáo hay Nhớ",
            "ReportGenerator này hỏng ở bước code review — báo cáo rỉ giữa các instance và dữ liệu mới không xuất hiện. Hai tội: trạng thái static dùng chung cho MỌI instance, và cache dữ liệu đầu vào mà caller kỳ vọng đọc lại. Viết `ReportGenerator` đúng: ngoài IFetcher được inject không giữ trạng thái nào; `Generate()` phản ánh dòng HIỆN TẠI của fetcher mỗi lần gọi, định dạng \"1. dòng\", \"2. dòng\" (từ 1).",
            [
                ("two instances, independent", "Không static, không chia sẻ. Mỗi generator đọc fetcher của chính nó."),
                ("mutation is reflected", "Generate không phải cache: gọi Fetch mỗi lần và định dạng mới."),
                ("stable for unchanged data", "Hành vi đúng là tất định — cùng input, cùng output, không cần cache."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p17-guard-clauses",
            'public static class Solution\n{\n    public static System.Collections.Generic.List<string> Validate(Order? order)\n    {\n        var errors = new System.Collections.Generic.List<string>();\n        if (order is null) { errors.Add("order"); return errors; }\n        if (string.IsNullOrEmpty(order.Customer)) { errors.Add("customer"); return errors; }\n        if (order.Items.Count == 0) { errors.Add("items"); return errors; }\n        for (int i = 0; i < order.Items.Count; i++)\n        {\n            if (order.Items[i].Qty < 0) errors.Add("qty:" + i);\n        }\n        return errors;\n    }\n}\n',
            'public static class Solution\n{\n    public static System.Collections.Generic.List<string> Validate(Order? order)\n    {\n        var errors = new System.Collections.Generic.List<string>();\n        if (order is null) { errors.Add("order"); return errors; }\n        if (string.IsNullOrEmpty(order.Customer)) { errors.Add("customer"); return errors; }\n        if (order.Items.Count == 0) { errors.Add("items"); return errors; }\n        for (int i = 0; i < order.Items.Count; i++)\n        {\n            if (order.Items[i].Qty < 0)\n            {\n                errors.Add("qty:" + i);\n                // near-miss: fail-fast reflex — bails at the first bad item\n                return errors;\n            }\n        }\n        return errors;\n    }\n}\n',
        ),
        (
            "csi-p17-extract-total",
            'public static class Solution\n{\n    public static decimal Subtotal(System.Collections.Generic.IEnumerable<OrderLine> lines)\n    {\n        decimal sum = 0m;\n        foreach (var l in lines) sum += l.Qty * l.Price;\n        return sum;\n    }\n\n    public static decimal Discount(decimal subtotal, decimal pct) => subtotal * pct / 100m;\n\n    public static decimal Shipping(decimal afterDiscount) => afterDiscount >= 100m ? 0m : 5m;\n\n    public static decimal Total(System.Collections.Generic.IEnumerable<OrderLine> lines, decimal pct)\n    {\n        decimal subtotal = Subtotal(lines);\n        decimal after = subtotal - Discount(subtotal, pct);\n        return after + Shipping(after);\n    }\n}\n',
            'public static class Solution\n{\n    public static decimal Subtotal(System.Collections.Generic.IEnumerable<OrderLine> lines)\n    {\n        decimal sum = 0m;\n        foreach (var l in lines) sum += l.Qty * l.Price;\n        return sum;\n    }\n\n    public static decimal Discount(decimal subtotal, decimal pct) => subtotal * pct / 100m;\n\n    public static decimal Shipping(decimal afterDiscount) => afterDiscount >= 100m ? 0m : 5m;\n\n    public static decimal Total(System.Collections.Generic.IEnumerable<OrderLine> lines, decimal pct)\n    {\n        decimal subtotal = Subtotal(lines);\n        // near-miss: ships on the pre-discount amount, discounts last —\n        // reads fine, computes the wrong total around the threshold\n        return (subtotal + Shipping(subtotal)) * (1m - pct / 100m);\n    }\n}\n',
        ),
        (
            "csi-p17-srp-split",
            'public sealed class ReportGenerator\n{\n    private readonly IFetcher _fetcher;\n\n    public ReportGenerator(IFetcher fetcher) => _fetcher = fetcher;\n\n    public string[] Generate()\n    {\n        string[] rows = _fetcher.Fetch();\n        var formatted = new string[rows.Length];\n        for (int i = 0; i < rows.Length; i++) formatted[i] = (i + 1) + ". " + rows[i];\n        return formatted;\n    }\n}\n',
            'public sealed class ReportGenerator\n{\n    private readonly IFetcher _fetcher;\n    // near-miss: the static is gone but the cache stayed — fresh data\n    // never appears after the first Generate\n    private string[]? _cached;\n\n    public ReportGenerator(IFetcher fetcher) => _fetcher = fetcher;\n\n    public string[] Generate()\n    {\n        if (_cached is null)\n        {\n            string[] rows = _fetcher.Fetch();\n            var formatted = new string[rows.Length];\n            for (int i = 0; i < rows.Length; i++) formatted[i] = (i + 1) + ". " + rows[i];\n            _cached = formatted;\n        }\n        return _cached;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
CHECKPOINT_BOILERPLATE = CS_PRELUDE + (
    "\n"
    "// Provided infrastructure — do not modify.\n"
    "// Legacy.Price IS the behavior you must preserve, then extend with \"vip\".\n"
    "// It is deliberately smelly: magic numbers, nested conditionals, duplication.\n"
    "public static class Legacy\n"
    "{\n"
    "    public static decimal Price(int qty, decimal unit, string tier)\n"
    "    {\n"
    "        decimal total = qty * unit;\n"
    "        decimal d = 0m;\n"
    "        if (tier == \"gold\")\n"
    "        {\n"
    "            if (qty >= 10) d = 0.20m; else d = 0.10m;\n"
    "        }\n"
    "        else if (tier == \"silver\")\n"
    "        {\n"
    "            if (qty >= 10) d = 0.10m; else d = 0.05m;\n"
    "        }\n"
    "        if (qty > 100) d += 0.02m;\n"
    "        return total * (1m - d);\n"
    "    }\n"
    "}\n"
)

write_checkpoint(
    M,
    "csi-checkpoint-m17",
    "Checkpoint — Refactor Under Guard",
    "Rebuild a smelly pricing method as clean code that provably behaves identically — then extend it, with Legacy standing in for the frozen test suite.",
    25,
    r"""
## The gate (mini-build)

`Legacy.Price` (provided, do not modify) is the behavior contract:

| tier | qty ≥ 10 | qty < 10 |
|---|---|---|
| gold | 20% off | 10% off |
| silver | 10% off | 5% off |
| anything else | no discount | no discount |

Any tier with `qty > 100` gains an extra 2% off, stacked.

Implement `Solution.Price(qty, unit, tier)` with **identical behavior**, plus
one new requirement: tier `"vip"` gets a flat **25% off** (the >100 bulk
extra still stacks on top). Structure it the clean way — named constants or a
switch expression over the tier, one rule per line, no magic numbers.

Your safety net is the legacy code itself: the tests compare your `Solution`
against `Legacy` across a matrix, then pin the boundaries and the new vip
behavior exactly.
""",
    "Checkpoint — Tái cấu trúc dưới Bảo hộ",
    "Dựng lại một method tính giá nhiều mùi thành code sạch, chứng minh được hành vi giống hệt — rồi mở rộng nó, với Legacy đóng vai bộ test đóng băng.",
    r"""
## Cổng kiểm tra (mini-build)

`Legacy.Price` (đã cấp, không sửa) là hợp đồng hành vi:

| tier | qty ≥ 10 | qty < 10 |
|---|---|---|
| gold | giảm 20% | giảm 10% |
| silver | giảm 10% | giảm 5% |
| khác | không giảm | không giảm |

Tier nào có `qty > 100` được thêm 2% giảm giá chồng lên.

Hiện thực `Solution.Price(qty, unit, tier)` với **hành vi giống hệt**, cộng
một yêu cầu mới: tier `"vip"` giảm thẳng **25%** (mức >100 vẫn chồng lên).
Cấu trúc theo cách sạch — hằng số có tên hoặc switch expression theo tier,
mỗi quy tắc một dòng, không magic number.

Lưới an toàn là chính code legacy: test so sánh `Solution` của bạn với
`Legacy` trên một ma trận, rồi ghim các biên và hành vi vip mới.
""",
    challenge(
        "csi-checkpoint-m17-task",
        "Refactor Legacy.Price",
        "Implement Solution.Price with identical behavior to Legacy.Price plus the vip tier, structured cleanly.",
        CHECKPOINT_BOILERPLATE,
        [
            (
                "matrix matches legacy",
                r"""
int[] qties = { 1, 5, 12, 50, 150 };
string[] tiers = { "gold", "silver", "none" };
foreach (int q in qties)
    foreach (string t in tiers)
    {
        decimal a = Solution.Price(q, 1.5m, t);
        decimal e = Legacy.Price(q, 1.5m, t);
        Cj.True(a == e, "matrix qty=" + q + " tier=" + t + " expected " + e + " got " + a);
    }
""",
                "Your Price must agree with Legacy on every non-boundary input — that is the definition of behavior-preserving.",
            ),
            (
                "vip tier",
                r"""
Cj.Eq(Solution.Price(4, 10m, "vip"), 30m, "40 at 25pct off");
Cj.Eq(Solution.Price(120, 10m, "vip"), 876m, "1200 at 27pct total (25 + bulk 2)");
""",
                "vip is a flat 25%; the >100 bulk extra (2%) stacks on top.",
            ),
            (
                "boundaries hold",
                r"""
Cj.Eq(Solution.Price(10, 1m, "gold"), 8m, "qty 10 gold -> 20pct");
Cj.Eq(Solution.Price(10, 1m, "silver"), 9m, "qty 10 silver -> 10pct");
Cj.Eq(Solution.Price(100, 1m, "silver"), 90m, "qty 100: no bulk extra yet");
Cj.Eq(Solution.Price(101, 1m, "silver"), 88.88m, "qty 101: bulk extra applies");
Cj.Eq(Legacy.Price(101, 1m, "silver"), 88.88m, "legacy agrees on 101");
""",
                "The >= 10 tier threshold and the > 100 bulk threshold are where sloppy refactors bleed.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: Tái cấu trúc dưới Bảo hộ",
        "Hiện thực Solution.Price với hành vi giống hệt Legacy.Price, cộng thêm tier vip (giảm thẳng 25%, mức >100 vẫn chồng lên). Cấu trúc sạch: switch expression hoặc hằng số có tên, không magic number.",
        [
            ("matrix matches legacy", "Price của bạn phải khớp Legacy trên mọi input ngoài biên — đó là định nghĩa của tái cấu trúc giữ hành vi."),
            ("vip tier", "vip giảm thẳng 25%; mức >100 (2%) chồng lên."),
            ("boundaries hold", "Ngưỡng tier ≥ 10 và ngưỡng bulk > 100 là nơi refactor cẩu thả rỉ máu."),
        ],
    ),
    solution='public static class Solution\n{\n    private const decimal GoldBig = 0.20m;\n    private const decimal GoldSmall = 0.10m;\n    private const decimal SilverBig = 0.10m;\n    private const decimal SilverSmall = 0.05m;\n    private const decimal Vip = 0.25m;\n    private const decimal BulkExtra = 0.02m;\n    private const int TierThreshold = 10;\n    private const int BulkThreshold = 100;\n\n    public static decimal Price(int qty, decimal unit, string tier)\n    {\n        decimal total = qty * unit;\n        decimal discount = tier switch\n        {\n            "gold" => qty >= TierThreshold ? GoldBig : GoldSmall,\n            "silver" => qty >= TierThreshold ? SilverBig : SilverSmall,\n            "vip" => Vip,\n            _ => 0m,\n        };\n        if (qty > BulkThreshold) discount += BulkExtra;\n        return total * (1m - discount);\n    }\n}\n',
    wrong='public static class Solution\n{\n    public static decimal Price(int qty, decimal unit, string tier)\n    {\n        decimal total = qty * unit;\n        decimal discount = tier switch\n        {\n            // near-miss: > instead of >= — one character, a new bug at the boundary\n            "gold" => qty > 10 ? 0.20m : 0.10m,\n            "silver" => qty > 10 ? 0.10m : 0.05m,\n            "vip" => 0.25m,\n            _ => 0m,\n        };\n        if (qty > 100) discount += 0.02m;\n        return total * (1m - discount);\n    }\n}\n',
)

print("module 17 authored")
