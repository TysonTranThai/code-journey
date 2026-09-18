#!/usr/bin/env python3
"""C# — Intermediate — Module 19: csi-architecture.

Architecture fundamentals: layers, dependency direction, DTOs vs domain
types, composition root, and the N+1 shape — graded via interface seams so
wrong-direction dependencies actually fail.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-architecture"

write_module(
    M,
    "Architecture Fundamentals",
    "Layers, dependency direction, DTOs at boundaries, a composition root — and spotting the wrong-direction dependency that makes code untestable.",
    "Nền tảng Kiến trúc",
    "Các tầng, hướng phụ thuộc, DTO tại biên, composition root — và nhận diện phụ thuộc ngược chiều khiến code không thể test.",
    ["layers", "boundaries", "csi-checkpoint-m19"],
    ["csi-p19-architecture"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "layers",
    "Layers and the Dependency Rule",
    "Why code is organized into layers, what each may know about the others, and the single rule that keeps them honest.",
    22,
    r"""
## The layers, minimal and honest

For a medium-sized app, three layers beat an enterprise zoo:

- **Domain** — the types and rules that make the app what it is: `Order`,
  `OrderLine`, the pricing logic. Knows *nothing* about IO.
- **Application** — use-cases: `PlaceOrderHandler` orchestrates domain types
  and ports. Knows the domain; knows ports (interfaces), not adapters.
- **Infrastructure** — talks to the world: HTTP clients, databases, file
  systems, real implementations of the ports. Knows everything — but
  *everything points at it*, never the reverse.

## The dependency rule

> Source-code dependencies point inward; nothing in an inner layer names a
> type from an outer one.

`Order` (domain) must not mention `HttpClient` or SQL. `PlaceOrderHandler`
may depend on `IOrderRepository` (a port it owns) but not on
`SqlOrderRepository` (an adapter). The concrete adapter is chosen at the
*edge of the system* — in the composition root.

This is not ceremony: it is exactly what makes `PlaceOrderHandler` testable
with a fake, what you did by hand in M16. The interface seam IS the
architecture.

## Ports and adapters (the practical core of Clean/Hexagonal)

- A **port** is an interface the inner layer defines because it *needs* a
  capability: `IOrderRepository`, `IEmailSender`, `IClock`.
- An **adapter** is an infrastructure type that implements a port:
  `SqlOrderRepository`, `SmtpEmailSender`.
- Domain/application code sees only ports. Tests substitute fakes for the
  same ports. Production wiring happens once, at the edge.

If you remember one sentence: **the domain defines what it needs;
infrastructure fulfills it.**

## Composition root

The single place (usually `Program.cs`) where concrete types are picked and
injected. It is allowed to know everything — that is its job. When wiring
lives there, changing implementations is a one-file change, and every other
layer stays ignorant.
""",
    "Các tầng và Quy tắc Phụ thuộc",
    "Vì sao code được tổ chức thành tầng, mỗi tầng được biết gì về tầng khác, và một quy tắc duy nhất giữ mọi thứ trung thực.",
    r"""
## Các tầng, tối giản và trung thực

Với app vừa, ba tầng thắng mọi "sở thú" doanh nghiệp:

- **Domain** — các type và quy tắc làm nên app: `Order`, `OrderLine`, logic
  định giá. Không biết *gì* về IO.
- **Application** — các use-case: `PlaceOrderHandler` điều phối domain type
  và port. Biết domain; biết port (interface), không biết adapter.
- **Infrastructure** — nói chuyện với thế giới ngoài: HTTP client, database,
  file, các hiện thực thật của port. Biết tất cả — nhưng *mọi thứ trỏ tới nó*,
  không bao giờ ngược lại.

## Quy tắc phụ thuộc

> Phụ thuộc source-code trỏ vào trong; không gì ở tầng trong được nhắc tới
> type của tầng ngoài.

`Order` (domain) không được nhắc `HttpClient` hay SQL. `PlaceOrderHandler`
được phụ thuộc `IOrderRepository` (port nó sở hữu) nhưng không được phụ thuộc
`SqlOrderRepository` (adapter). Adapter cụ thể được chọn ở *rìa hệ thống* —
trong composition root.

Đây không phải nghi lễ: đây chính là thứ làm `PlaceOrderHandler` test được
bằng fake — thứ bạn làm bằng tay ở M16. Đường ranh interface CHÍNH LÀ kiến
trúc.

## Ports và adapters (phần lõi thực dụng của Clean/Hexagonal)

- **Port** là interface tầng trong định nghĩa vì nó *cần* một năng lực:
  `IOrderRepository`, `IEmailSender`, `IClock`.
- **Adapter** là type infrastructure hiện thực port: `SqlOrderRepository`,
  `SmtpEmailSender`.
- Code domain/application chỉ thấy port. Test thay fake vào đúng các port đó.
  Wiring production xảy ra một lần, ở rìa.

Nhớ một câu: **domain định nghĩa nó cần gì; infrastructure đáp ứng.**

## Composition root

Một nơi duy nhất (thường là `Program.cs`) chọn type cụ thể và inject. Nó được
phép biết tất cả — đó là công việc của nó. Khi wiring nằm ở đó, đổi hiện thực
là thay một file, và mọi tầng khác vẫn không biết gì.
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "boundaries",
    "Boundaries: DTOs, Leaky Contracts, and N+1",
    "Where layers meet: boundary types that stay stable, the shape of the N+1 query problem, and seams you can grade.",
    24,
    r"""
## DTOs: the boundary's own language

A **DTO** (Data Transfer Object) is a boundary type with no behavior: the
shape an API or storage layer speaks. Why not expose domain types directly?

- **Stability** — an internal refactor must not break external consumers.
- **Security** — you choose every field that crosses; nothing leaks by
  accident.
- **Intent** — the wire shape says what a use-case means: `PlaceOrderRequest`
  with only the fields that matter.

```csharp
// domain owns this
public sealed class Order { public int Id; public string Customer = ""; }

// boundary speaks this
public sealed record OrderDto(int Id, string Customer);

// mapping is explicit, one direction per use-case
public static OrderDto ToDto(Order o) => new(o.Id, o.Customer);
```

Mapping feels like boilerplate until the first time a public contract survives
an internal rewrite — then it is insurance.

## The N+1 shape (now, before a real ORM)

Fetch 20 orders, then per order fetch its customer: 1 + 20 queries. In code,
the tell is a loop whose body does a lookup that could have been batched:

```csharp
// N+1: one query per order
foreach (var o in orders)
    o.CustomerName = _names.Find(o.CustomerId);   // 20 round trips

// fixed: batch, then join in memory
var ids = orders.Select(o => o.CustomerId).Distinct();
var byId = _names.FindMany(ids);
foreach (var o in orders)
    o.CustomerName = byId[o.CustomerId];          // 2 round trips
```

You will fix this shape against a counting fake — the same way you will later
recognize it under EF Core's lazy loading.

## What "wrong direction" looks like

The classic violation: a domain type (or its method signature) referencing an
infrastructure name — `Order.LoadFrom(SqlConnection)`. The seam collapses:
no fake can replace the connection, so no test can run without a database.
The graded refactor, next practice, is restoring exactly that seam.
""",
    "Đường ranh: DTO, Hợp đồng Rỉ, và N+1",
    "Nơi các tầng gặp nhau: kiểu biên giữ ổn định, hình dạng của bài toán N+1 query, và các đường ranh có thể chấm điểm.",
    r"""
## DTO: ngôn ngữ riêng của đường ranh

**DTO** (Data Transfer Object) là kiểu biên không có hành vi: hình dạng mà API
hay tầng lưu trữ nói. Vì sao không lộ domain type ra ngoài?

- **Ổn định** — refactor nội bộ không được làm vỡ consumer bên ngoài.
- **An toàn** — bạn chọn từng field được đi qua; không gì rỉ ra do vô ý.
- **Ý định** — hình dạng trên dây nói rõ use-case nghĩa là gì:
  `PlaceOrderRequest` chỉ với những field quan trọng.

Ví dụ `Order`, `OrderDto` và hàm map `ToDto` trong bản tiếng Anh — mapping có
vẻ boilerplate cho đến lần đầu hợp đồng công khai sống sót qua một lần viết
lại nội bộ — khi đó nó là bảo hiểm.

## Hình dạng N+1 (học ngay, trước cả ORM)

Lấy 20 order, rồi mỗi order lấy customer: 1 + 20 query. Trong code, dấu hiệu
là một vòng lặp mà thân làm một lookup đáng lẽ đã batch được (xem cặp ví dụ
trước/sau trong bản tiếng Anh).

Bạn sẽ sửa hình dạng này trên một fake đếm truy vấn — cùng cách bạn sẽ nhận ra
nó dưới lazy loading của EF Core sau này.

## "Ngược chiều" trông thế nào

Vi phạm kinh điển: một domain type (hay chữ ký method của nó) nhắc tên
infrastructure — `Order.LoadFrom(SqlConnection)`. Đường ranh sụp đổ: không
fake nào thay thế được connection, nên không test nào chạy nổi mà không có
database. Refactor được chấm điểm ở phần luyện, chính là khôi phục đường ranh
đó.
""",
)

# ---------------------------------------------------------------- practice
FAKE_LOOKUP = (
    "\n"
    "// Provided infrastructure — do not modify.\n"
    "public sealed class FakeLookup : ILookup\n"
    "{\n"
    "    private readonly string[] _names;\n"
    "    public int Calls { get; private set; }\n"
    "    public System.Collections.Generic.List<int[]> LastIds = new();\n"
    "\n"
    "    public FakeLookup(params string[] names) => _names = names;\n"
    "    public string[] FetchMany(int[] ids)\n"
    "    {\n"
    "        Calls++;\n"
    "        LastIds.Add((int[])ids.Clone());\n"
    "        var outp = new string[ids.Length];\n"
    "        for (int i = 0; i < ids.Length; i++)\n"
    "            outp[i] = _names[(ids[i] - 1) % _names.Length];\n"
    "        return outp;\n"
    "    }\n"
    "}\n"
)

write_practice(
    M,
    "csi-p19-architecture",
    "Architecture Practice: Seams, Batches, Boundaries",
    "Fix a wrong-direction dependency across a port, batch an N+1 against a counting fake, map through a DTO that hides fields, and debug a loader that calls too much.",
    "Luyện Kiến trúc: Đường ranh, Batch, Biên",
    "Sửa phụ thuộc ngược chiều qua một port, batch N+1 trên fake đếm truy vấn, map qua DTO ẩn field, và debug một loader gọi quá nhiều.",
    "boundaries",
    32,
    "intermediate",
    [
        challenge(
            "csi-p19-port-seam",
            "Restore the Seam",
            r"""`OrderService` below is untestable — it news up its storage directly,
so no fake can stand in:

```csharp
public sealed class OrderService          // BROKEN — do not ship this
{
    private readonly Dictionary<int, int> _d = new();   // hard-wired storage
    public int Bump(int id) { ... }
}
```

Refactor the *shape* the tests can see:

1. `IStore { int Get(int id); void Put(int id, int v); }` (inside `Solution`)
2. `Solution.Service` takes an `IStore` via constructor.
3. `Service.Bump(id)` adds `Delta` (a `const int` = 5) to the stored value
   and returns the new value.
4. Provide two adapters: `DictStore` (wraps a caller-supplied dictionary)
   and `DoubleStore` (its own private dictionary) — proving any
   implementation fits the same port.

The tests inject each store in turn — the dependency points at a port, not
an implementation.

```csharp
public static class Solution
{
    public interface IStore { int Get(int id); void Put(int id, int v); }
    public sealed class DictStore : IStore;      // wraps a supplied Dictionary<int,int>
    public sealed class DoubleStore : IStore;    // independent private storage
    public sealed class Service                  // ctor(IStore); int Bump(int id)
}
```""",
            CS_PRELUDE,
            [
                (
                    "bump goes through the port",
                    r"""
var store = new System.Collections.Generic.Dictionary<int, int>();
store[7] = 10;
var svc = new Solution.Service(new Solution.DictStore(store));
Cj.Eq(svc.Bump(7), 15, "10 + Delta(5)");
Cj.Eq(store[7], 15, "write reached the caller's dictionary");
""",
                    "Bump reads via Get, adds Delta, writes via Put, returns the new value.",
                ),
                (
                    "any implementation fits",
                    r"""
var svc = new Solution.Service(new Solution.DoubleStore());
Cj.Eq(svc.Bump(1), 5, "empty store -> 0 + 5");
""",
                    "A second IStore implementation must work unchanged — that is the seam.",
                ),
                (
                    "delta applied once per bump",
                    r"""
var probe = new Solution.DoubleStore();
var one = new Solution.Service(probe);
one.Bump(3);
Cj.Eq(probe.Get(3), 5, "delta applied once");
one.Bump(3);
Cj.Eq(probe.Get(3), 10, "and again on the next bump");
""",
                    "Each Bump applies exactly Delta — no drift, no doubling.",
                ),
            ],
            level="refactor",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p19-batch-lookup",
            "Kill the N+1",
            r"""`LegacyLoader` fetches one record per customer — the N+1 shape,
captured by a counting fake. Write `Solution.LoadNames(Customer[] customers,
ILookup store)` that returns names in input order with **exactly one store
round trip**:

- store port: `ILookup { string[] FetchMany(int[] ids); int Calls { get; } }`
  — returns the names for the requested ids, **in the same order as the ids**.
- behavior: distinct ids are fetched once; results map back to each customer
  by position of their first occurrence; repeated customers get the same name
  without extra calls.

The fake's `Calls` must be 1 after a batched load. The store provides the
names — do not read `Customer.Name`; the point is the batched fetch.

```csharp
public static class Solution
{
    public sealed class Customer { public int Id; }
    public static string[] LoadNames(Customer[] customers, ILookup store);
}
// top level: public interface ILookup { string[] FetchMany(int[] ids); int Calls { get; } }
```""",
            CS_PRELUDE + FAKE_LOOKUP,
            [
                (
                    "one round trip",
                    r"""
var store = new FakeLookup("alpha", "beta", "gamma");
var cs = new[] { new Solution.Customer { Id = 1 }, new Solution.Customer { Id = 2 } };
var names = Solution.LoadNames(cs, store);
Cj.Eq(string.Join("|", names), "alpha|beta", "names in customer order");
Cj.Eq(store.Calls, 1, "exactly one FetchMany call");
""",
                    "Collect distinct ids first, one FetchMany, then map results back by position.",
                ),
                (
                    "repeated customers, no extra calls",
                    r"""
var store = new FakeLookup("alpha", "beta");
var cs = new[] { new Solution.Customer { Id = 1 }, new Solution.Customer { Id = 1 } };
var names = Solution.LoadNames(cs, store);
Cj.Eq(string.Join("|", names), "alpha|alpha", "same name for the same id");
Cj.Eq(store.Calls, 1, "dedup made it one call");
""",
                    "Distinct ids: [1]. Both customers map to the first result.",
                ),
                (
                    "order of ids is preserved",
                    r"""
var store = new FakeLookup("x", "y", "z");
var cs = new[] { new Solution.Customer { Id = 3 }, new Solution.Customer { Id = 1 } };
Cj.Eq(string.Join("|", Solution.LoadNames(cs, store)), "z|x", "id order -> result order");
Cj.Eq(store.LastIds[0][0], 3, "distinct ids requested in first-seen order");
""",
                    "The fake returns names positionally: ids [3,1] -> names [z,x].",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p19-dto-boundary",
            "DTO: Hide the Internals",
            r"""`Employee` (domain) carries `Salary` — which must never cross the
public boundary. Implement:

- `Solution.ToPublic(Employee e)` returning a `PublicDto` with only safe
  fields (`Name`, `Dept`) — the DTO type must not even declare a `Salary`
  member.
- `Solution.TeamReport(Employee[] staff)` returning public rows in input
  order — the report is built from boundary types, not domain ones.

```csharp
public static class Solution
{
    public sealed class Employee { public string Name = ""; public string Dept = ""; public decimal Salary; }
    public sealed class PublicDto { public string Name = ""; public string Dept = ""; }
    public static PublicDto ToPublic(Employee e);
    public static PublicDto[] TeamReport(Employee[] staff);
    public static bool DtoHasSalaryMember();   // reflection probe used by the tests
}
```""",
            CS_PRELUDE,
            [
                (
                    "salary never crosses",
                    r"""
var e = new Solution.Employee { Name = "ann", Dept = "eng", Salary = 120000m };
var dto = Solution.ToPublic(e);
Cj.Eq(dto.Name, "ann", "name mapped");
Cj.Eq(dto.Dept, "eng", "dept mapped");
Cj.False(Solution.DtoHasSalaryMember(), "PublicDto must not declare Salary");
""",
                    "Map only the safe fields; the DTO type itself must not have a Salary member.",
                ),
                (
                    "report maps through the dto",
                    r"""
var staff = new[] {
    new Solution.Employee { Name = "a", Dept = "eng" },
    new Solution.Employee { Name = "b", Dept = "ops" },
};
var rows = Solution.TeamReport(staff);
Cj.Eq(rows.Length, 2, "one row per employee");
Cj.Eq(rows[0].Name + ":" + rows[1].Dept, "a:ops", "order and fields preserved");
""",
                    "TeamReport is built from PublicDto rows in input order.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p19-n1-debug",
            "Debug: The Loader That Calls Too Much",
            r"""A junior "fixed" the N+1 by caching — but their `CachedLoader` still
hits the store once per customer AND runs a pointless "warm-up" second pass.
The counting fake exposes both: `Calls` grows and `LastIds` fills with
single-id batches.

Write a correct `Solution.Load(ILookup store, int[] ids)` that

- performs exactly one `FetchMany` per invocation (dedup ids),
- returns names in input order (with repeats),
- and makes no store call at all for empty input.

```csharp
public static class Solution
{
    public static string[] Load(ILookup store, int[] ids);
}
// top level: public interface ILookup { string[] FetchMany(int[] ids); int Calls { get; } }
```

Provided for reference — the broken version you are correcting:

```csharp
public sealed class CachedLoader : ILoader   // BROKEN: fetches per id, twice
{
    public string[] Load(ILookup store, int[] ids)
    {
        var outp = new List<string>();
        foreach (var id in ids) { var n = store.FetchMany(new[]{id}); outp.Add(n[0]); }
        foreach (var id in ids) { store.FetchMany(new[]{id}); }   // "warm the cache"
        return outp.ToArray();
    }
}
```""",
            CS_PRELUDE + FAKE_LOOKUP,
            [
                (
                    "exactly one call, order preserved",
                    r"""
var store = new FakeLookup("a", "b", "c");
var outp = Solution.Load(store, new[] { 1, 2, 1, 3 });
Cj.Eq(string.Join("|", outp), "a|b|a|c", "input order with repeats");
Cj.Eq(store.Calls, 1, "one FetchMany total");
""",
                    "Dedup ids [1,2,3], one call, map back by each id's first occurrence.",
                ),
                (
                    "no warm-up second pass",
                    r"""
var store = new FakeLookup("a", "b");
Solution.Load(store, new[] { 2, 1 });
Cj.Eq(store.LastIds.Count, 1, "single fetch batch");
Cj.Eq(store.LastIds[0].Length, 2, "both distinct ids in one batch");
""",
                    "The broken version makes 4 calls here; correct is 1 with ids [2,1].",
                ),
                (
                    "empty input is safe",
                    r"""
var store = new FakeLookup("a");
Cj.Eq(Solution.Load(store, new int[] { }).Length, 0, "empty in, empty out");
Cj.Eq(store.Calls, 0, "no call for empty input");
""",
                    "Empty ids: no store round trip, empty result.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p19-port-seam": vi_challenge(
            "Khôi phục Đường ranh",
            "`OrderService` dưới đây không thể test — nó tự giữ kho lưu trữ cứng, nên không fake nào đứng vào được. Tái cấu trúc *hình dạng* mà test nhìn thấy: 1) `IStore { int Get(int id); void Put(int id, int v); }` (trong `Solution`); 2) `Solution.Service` nhận `IStore` qua constructor; 3) `Service.Bump(id)` cộng `Delta` (const = 5) vào giá trị đang lưu và trả giá trị mới; 4) cung cấp hai adapter `DictStore` (bọc dictionary do caller cấp) và `DoubleStore` (kho riêng độc lập) — chứng minh mọi hiện thực đều khớp port. Test inject lần lượt từng store — phụ thuộc trỏ vào port chứ không phải hiện thực.",
            [
                ("bump goes through the port", "Bump đọc qua Get, cộng Delta, ghi qua Put, trả giá trị mới."),
                ("any implementation fits", "Một hiện thực IStore thứ hai phải chạy không đổi — đó mới là đường ranh."),
                ("delta applied once per bump", "Mỗi Bump áp đúng Delta — không trôi, không nhân đôi."),
            ],
        ),
        "csi-p19-batch-lookup": vi_challenge(
            "Diệt N+1",
            "Viết `Solution.LoadNames(Customer[] customers, ILookup store)` trả tên theo thứ tự input với **đúng một lượt gọi store**: distinct id được fetch một lần; kết quả map về từng customer theo vị trí xuất hiện đầu tiên; customer lặp trong input nhận cùng tên mà không gọi thêm. `Calls` của fake phải bằng 1 sau một lần load batch. Store cung cấp tên — không đọc `Customer.Name`.",
            [
                ("one round trip", "Gom distinct id trước, một FetchMany, rồi map kết quả về theo vị trí."),
                ("repeated customers, no extra calls", "Distinct id: [1]. Cả hai customer map tới kết quả đầu tiên."),
                ("order of ids is preserved", "Fake trả tên theo vị trí: ids [3,1] -> names [z,x]."),
            ],
        ),
        "csi-p19-dto-boundary": vi_challenge(
            "DTO: Ẩn Nội bộ",
            "`Employee` (domain) mang `Salary` — không bao giờ được qua đường ranh công khai. Hiện thực `Solution.ToPublic(Employee e)` trả `PublicDto` chỉ với field an toàn (Name, Dept — type không được khai báo member Salary nào cả), cộng `Solution.TeamReport(Employee[] staff)` trả các dòng công khai theo thứ tự input — báo cáo được dựng từ kiểu biên, không phải kiểu domain.",
            [
                ("salary never crosses", "Chỉ map field an toàn; bản thân type DTO không được có member Salary."),
                ("report maps through the dto", "TeamReport được dựng từ các dòng PublicDto theo thứ tự input."),
            ],
        ),
        "csi-p19-n1-debug": vi_challenge(
            "Debug: Loader gọi quá nhiều",
            "Một bạn junior \"sửa\" N+1 bằng cách cache — nhưng `CachedLoader` vẫn gọi store mỗi customer VÀ chạy thêm một lượt \"làm ấm\" vô nghĩa. Fake đếm truy vấn phơi bày cả hai. Viết `Solution.Load(ILookup store, int[] ids)` đúng: mỗi lần gọi Load thực hiện đúng MỘT `FetchMany` (dedup id), trả tên theo thứ tự input (kể cả lặp), và input rỗng thì không gọi store.",
            [
                ("exactly one call, order preserved", "Dedup id [1,2,3], một lần gọi, map ngược theo vị trí xuất hiện đầu của mỗi id."),
                ("no warm-up second pass", "Bản hỏng gọi 4 lần ở đây; đúng là 1 lần với ids [2,1]."),
                ("empty input is safe", "Ids rỗng: không gọi store, kết quả rỗng."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p19-port-seam",
            'public static class Solution\n{\n    public const int Delta = 5;\n\n    public interface IStore\n    {\n        int Get(int id);\n        void Put(int id, int v);\n    }\n\n    public sealed class DictStore : IStore\n    {\n        private readonly System.Collections.Generic.Dictionary<int, int> _d;\n        public DictStore(System.Collections.Generic.Dictionary<int, int> d) => _d = d;\n        public int Get(int id) => _d.TryGetValue(id, out var v) ? v : 0;\n        public void Put(int id, int v) => _d[id] = v;\n    }\n\n    public sealed class DoubleStore : IStore\n    {\n        private readonly System.Collections.Generic.Dictionary<int, int> _d = new();\n        public int Get(int id) => _d.TryGetValue(id, out var v) ? v : 0;\n        public void Put(int id, int v) => _d[id] = v;\n    }\n\n    public sealed class Service\n    {\n        private readonly IStore _store;\n        public Service(IStore store) => _store = store;\n\n        public int Bump(int id)\n        {\n            int v = _store.Get(id) + Delta;\n            _store.Put(id, v);\n            return v;\n        }\n    }\n}\n',
            'public static class Solution\n{\n    public const int Delta = 5;\n\n    public interface IStore\n    {\n        int Get(int id);\n        void Put(int id, int v);\n    }\n\n    public sealed class DictStore : IStore\n    {\n        private readonly System.Collections.Generic.Dictionary<int, int> _d;\n        public DictStore(System.Collections.Generic.Dictionary<int, int> d) => _d = d;\n        public int Get(int id) => _d.TryGetValue(id, out var v) ? v : 0;\n        public void Put(int id, int v) => _d[id] = v;\n    }\n\n    public sealed class DoubleStore : IStore\n    {\n        private readonly System.Collections.Generic.Dictionary<int, int> _d = new();\n        public int Get(int id) => _d.TryGetValue(id, out var v) ? v : 0;\n        public void Put(int id, int v) => _d[id] = v;\n    }\n\n    public sealed class Service\n    {\n        private readonly IStore _store;\n        public Service(IStore store) => _store = store;\n\n        public int Bump(int id)\n        {\n            // near-miss: re-reads after the put and adds Delta AGAIN —\n            // the port is used, but the arithmetic drifts upward\n            int v = _store.Get(id) + Delta;\n            _store.Put(id, v);\n            return _store.Get(id) + Delta;\n        }\n    }\n}\n',
        ),
        (
            "csi-p19-batch-lookup",
            'public interface ILookup\n{\n    string[] FetchMany(int[] ids);\n    int Calls { get; }\n}\n\npublic static class Solution\n{\n    public sealed class Customer\n    {\n        public int Id;\n    }\n\n    public static string[] LoadNames(Customer[] customers, ILookup store)\n    {\n        // distinct ids in first-seen order\n        var order = new System.Collections.Generic.List<int>();\n        var seen = new System.Collections.Generic.HashSet<int>();\n        foreach (var c in customers)\n            if (seen.Add(c.Id)) order.Add(c.Id);\n\n        var fetched = store.FetchMany(order.ToArray());\n\n        var result = new string[customers.Length];\n        var pos = new System.Collections.Generic.Dictionary<int, int>();\n        for (int i = 0; i < customers.Length; i++)\n            if (!pos.ContainsKey(customers[i].Id)) pos[customers[i].Id] = pos.Count;\n        for (int i = 0; i < customers.Length; i++)\n            result[i] = fetched[pos[customers[i].Id]];\n        return result;\n    }\n}\n',
            'public interface ILookup\n{\n    string[] FetchMany(int[] ids);\n    int Calls { get; }\n}\n\npublic static class Solution\n{\n    public sealed class Customer\n    {\n        public int Id;\n    }\n\n    public static string[] LoadNames(Customer[] customers, ILookup store)\n    {\n        var result = new string[customers.Length];\n        // near-miss: one call PER CUSTOMER — the N+1 shape, unchanged\n        for (int i = 0; i < customers.Length; i++)\n        {\n            var got = store.FetchMany(new[] { customers[i].Id });\n            result[i] = got[0];\n        }\n        return result;\n    }\n}\n',
        ),
        (
            "csi-p19-dto-boundary",
            'public static class Solution\n{\n    public sealed class Employee\n    {\n        public string Name = "";\n        public string Dept = "";\n        public decimal Salary;\n    }\n\n    public sealed class PublicDto\n    {\n        public string Name = "";\n        public string Dept = "";\n    }\n\n    public static PublicDto ToPublic(Employee e) =>\n        new PublicDto { Name = e.Name, Dept = e.Dept };\n\n    public static PublicDto[] TeamReport(Employee[] staff)\n    {\n        var rows = new PublicDto[staff.Length];\n        for (int i = 0; i < staff.Length; i++) rows[i] = ToPublic(staff[i]);\n        return rows;\n    }\n\n    public static bool DtoHasSalaryMember() =>\n        typeof(PublicDto).GetMember("Salary").Length > 0;\n}\n',
            'public static class Solution\n{\n    public sealed class Employee\n    {\n        public string Name = "";\n        public string Dept = "";\n        public decimal Salary;\n    }\n\n    // near-miss: the DTO exposes the field the boundary exists to hide\n    public sealed class PublicDto\n    {\n        public string Name = "";\n        public string Dept = "";\n        public decimal Salary;\n    }\n\n    public static PublicDto ToPublic(Employee e) =>\n        new PublicDto { Name = e.Name, Dept = e.Dept, Salary = e.Salary };\n\n    public static PublicDto[] TeamReport(Employee[] staff)\n    {\n        var rows = new PublicDto[staff.Length];\n        for (int i = 0; i < staff.Length; i++) rows[i] = ToPublic(staff[i]);\n        return rows;\n    }\n\n    public static bool DtoHasSalaryMember() =>\n        typeof(PublicDto).GetMember("Salary").Length > 0;\n}\n',
        ),
        (
            "csi-p19-n1-debug",
            'public interface ILookup\n{\n    string[] FetchMany(int[] ids);\n    int Calls { get; }\n}\n\npublic static class Solution\n{\n    public static string[] Load(ILookup store, int[] ids)\n    {\n        if (ids.Length == 0) return new string[0];\n\n        // distinct ids in first-seen order; firstPos[id] = its position there\n        var firstPos = new System.Collections.Generic.Dictionary<int, int>();\n        for (int i = 0; i < ids.Length; i++)\n            if (!firstPos.ContainsKey(ids[i])) firstPos[ids[i]] = firstPos.Count;\n\n        var distinct = new int[firstPos.Count];\n        foreach (var kv in firstPos) distinct[kv.Value] = kv.Key;\n\n        var fetched = store.FetchMany(distinct);\n\n        var outp = new string[ids.Length];\n        for (int i = 0; i < ids.Length; i++)\n            outp[i] = fetched[firstPos[ids[i]]];\n        return outp;\n    }\n}\n',
            'public interface ILookup\n{\n    string[] FetchMany(int[] ids);\n    int Calls { get; }\n}\n\npublic static class Solution\n{\n    public static string[] Load(ILookup store, int[] ids)\n    {\n        if (ids.Length == 0) return new string[0];\n\n        var outp = new string[ids.Length];\n        // near-miss: dedups but still one CALL per distinct id — N calls, not 1\n        for (int i = 0; i < ids.Length; i++)\n        {\n            bool seen = false;\n            for (int j = 0; j < i; j++) seen |= ids[j] == ids[i];\n            if (!seen) outp[i] = store.FetchMany(new[] { ids[i] })[0];\n        }\n        for (int i = 1; i < ids.Length; i++)\n            if (outp[i] is null) outp[i] = outp[i - 1];\n        return outp;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m19",
    "Checkpoint — The Layered Checkout",
    "Compose the module: a service behind ports, dedup-then-map batch pricing, and clean guards — the layered shape, with the seams the tests probe.",
    28,
    r"""
## The gate (mini-build)

Three seams in one file, checked by the tests through the ports only:

1. **Ports** — `ICatalog { int Price(string sku); }` and
   `IBasket { void Add(string sku, int qty); int Count { get; } string FirstSku { get; } }`
   (Count = total quantity added; FirstSku = the first sku ever added).
2. **Service** — `Checkout(ICatalog, IBasket)`: `Quote()` returns
   `"Total:" + price-of-FirstSku + " x " + Count`; throws
   `InvalidOperationException` on an empty basket (Count == 0). Quote must
   work through the interfaces only — no casting to concrete types.
3. **Batch boundary** — `QuoteMany(string[] skus, ICatalog catalog)` returns
   one price per sku (input order), pricing each distinct sku exactly once —
   dedup, then map.

```csharp
public static class Solution
{
    public interface ICatalog { int Price(string sku); }
    public sealed class MemCatalog : ICatalog;    // "t1" -> 25, "t2" -> 40
    public interface IBasket { void Add(string sku, int qty); int Count { get; } string FirstSku { get; } }
    public sealed class MemBasket : IBasket;
    public sealed class Checkout { public Checkout(ICatalog c, IBasket b); public string Quote(); }
    public static int[] QuoteMany(string[] skus, ICatalog catalog);
    public static bool Threw(Action a);
}
```""",
    "Checkpoint — Checkout Phân tầng",
    "Ghép cả module: service sau các port, định giá batch theo kiểu dedup-rồi-map, và guard sạch sẽ — hình dạng phân tầng, với đúng các đường ranh mà test thăm dò.",
    r"""
## Cổng kiểm tra (mini-build)

Ba đường ranh trong một file, được test kiểm tra chỉ qua các port:

1. **Port** — `ICatalog { int Price(string sku); }` và
   `IBasket { void Add(string sku, int qty); int Count { get; } string FirstSku { get; } }`
   (Count = tổng số lượng đã thêm; FirstSku = sku đầu tiên được thêm).
2. **Service** — `Checkout(ICatalog, IBasket)`: `Quote()` trả
   `"Total:" + giá-của-FirstSku + " x " + Count`; throw
   `InvalidOperationException` khi giỏ rỗng (Count == 0). Quote phải chạy chỉ
   qua interface — không được cast sang kiểu cụ thể.
3. **Đường ranh batch** — `QuoteMany(string[] skus, ICatalog catalog)` trả một
   giá cho mỗi sku (theo thứ tự input), định giá mỗi sku distinct đúng một lần
   — dedup, rồi map.

Xem chữ ký `Solution` trong bản tiếng Anh.
""",
    challenge(
        "csi-checkpoint-m19-task",
        "Wire the Layered Checkout",
        "Implement ICatalog/IBasket ports with MemCatalog/MemBasket adapters, the Checkout service (interface-only Quote with an empty-basket guard), and dedup-then-map QuoteMany.",
        CS_PRELUDE,
        [
            (
                "service composes through ports",
                r"""
var c = new Solution.MemCatalog();
var b = new Solution.MemBasket();
b.Add("t1", 2);
var co = new Solution.Checkout(c, b);
Cj.Eq(co.Quote(), "Total:25 x 2", "price x count");
""",
                "Quote reads the first sku's price from the injected catalog and multiplies by Count.",
            ),
            (
                "empty basket throws",
                r"""
var co = new Solution.Checkout(new Solution.MemCatalog(), new Solution.MemBasket());
Cj.True(Solution.Threw(() => co.Quote()), "empty basket throws InvalidOperationException");
""",
                "Guard the degenerate case: Quote on an empty basket throws.",
            ),
            (
                "quote many prices each sku once",
                r"""
var c = new Solution.MemCatalog();
var prices = Solution.QuoteMany(new[] { "t1", "t2", "t1" }, c);
Cj.Eq(string.Join("|", prices), "25|40|25", "one price per sku, input order");
""",
                "QuoteMany must dedup skus, fetch each distinct price once, and map back to input order.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: Wire Checkout Phân tầng",
        "Hiện thực các port ICatalog/IBasket cùng adapter MemCatalog/MemBasket, service Checkout (Quote chỉ qua interface, guard giỏ rỗng), và QuoteMany theo kiểu dedup-rồi-map.",
        [
            ("service composes through ports", "Quote đọc giá của sku đầu tiên từ catalog được inject và nhân với Count."),
            ("empty basket throws", "Bảo vệ trường hợp suy biến: Quote trên giỏ rỗng throw."),
            ("quote many prices each sku once", "QuoteMany phải dedup sku, định giá mỗi sku distinct đúng một lần, rồi map về thứ tự input."),
        ],
    ),
    solution='public static class Solution\n{\n    public interface ICatalog\n    {\n        int Price(string sku);\n    }\n\n    public sealed class MemCatalog : ICatalog\n    {\n        private readonly System.Collections.Generic.Dictionary<string, int> _p =\n            new System.Collections.Generic.Dictionary<string, int> { ["t1"] = 25, ["t2"] = 40 };\n        public int Price(string sku) => _p.TryGetValue(sku, out var v) ? v : 0;\n    }\n\n    public interface IBasket\n    {\n        void Add(string sku, int qty);\n        int Count { get; }\n        string FirstSku { get; }\n    }\n\n    public sealed class MemBasket : IBasket\n    {\n        private string _first = "";\n        public int Count { get; private set; }\n        public string FirstSku => _first;\n\n        public void Add(string sku, int qty)\n        {\n            if (Count == 0) _first = sku;\n            Count += qty;\n        }\n    }\n\n    public sealed class Checkout\n    {\n        private readonly ICatalog _catalog;\n        private readonly IBasket _basket;\n        public Checkout(ICatalog catalog, IBasket basket) { _catalog = catalog; _basket = basket; }\n\n        public string Quote()\n        {\n            if (_basket.Count == 0) throw new InvalidOperationException("empty basket");\n            int price = _catalog.Price(_basket.FirstSku);\n            return "Total:" + price + " x " + _basket.Count;\n        }\n    }\n\n    public static int[] QuoteMany(string[] skus, ICatalog catalog)\n    {\n        var first = new System.Collections.Generic.Dictionary<string, int>();\n        var distinct = new System.Collections.Generic.List<string>();\n        foreach (var s in skus)\n            if (!first.ContainsKey(s)) { first[s] = distinct.Count; distinct.Add(s); }\n\n        var fetched = new int[distinct.Count];\n        for (int i = 0; i < distinct.Count; i++) fetched[i] = catalog.Price(distinct[i]);\n\n        var outp = new int[skus.Length];\n        for (int i = 0; i < skus.Length; i++) outp[i] = fetched[first[skus[i]]];\n        return outp;\n    }\n\n    public static bool Threw(Action a) { try { a(); return false; } catch { return true; } }\n}\n',
    wrong='public static class Solution\n{\n    public interface ICatalog\n    {\n        int Price(string sku);\n    }\n\n    public sealed class MemCatalog : ICatalog\n    {\n        private readonly System.Collections.Generic.Dictionary<string, int> _p =\n            new System.Collections.Generic.Dictionary<string, int> { ["t1"] = 25, ["t2"] = 40 };\n        public int Price(string sku) => _p.TryGetValue(sku, out var v) ? v : 0;\n    }\n\n    public interface IBasket\n    {\n        void Add(string sku, int qty);\n        int Count { get; }\n        string FirstSku { get; }\n    }\n\n    public sealed class MemBasket : IBasket\n    {\n        private string _first = "";\n        public int Count { get; private set; }\n        public string FirstSku => _first;\n\n        public void Add(string sku, int qty)\n        {\n            if (Count == 0) _first = sku;\n            Count += qty;\n        }\n    }\n\n    public sealed class Checkout\n    {\n        private readonly ICatalog _catalog;\n        private readonly IBasket _basket;\n        public Checkout(ICatalog catalog, IBasket basket) { _catalog = catalog; _basket = basket; }\n\n        public string Quote()\n        {\n            // near-miss: the guard can never fire — empty baskets fall through\n            // and return a nonsense total instead of throwing\n            if (_basket.Count < 0) throw new InvalidOperationException("empty basket");\n            int price = _catalog.Price(_basket.FirstSku);\n            return "Total:" + price + " x " + _basket.Count;\n        }\n    }\n\n    public static int[] QuoteMany(string[] skus, ICatalog catalog)\n    {\n        var first = new System.Collections.Generic.Dictionary<string, int>();\n        var distinct = new System.Collections.Generic.List<string>();\n        foreach (var s in skus)\n            if (!first.ContainsKey(s)) { first[s] = distinct.Count; distinct.Add(s); }\n\n        var fetched = new int[distinct.Count];\n        for (int i = 0; i < distinct.Count; i++) fetched[i] = catalog.Price(distinct[i]);\n\n        var outp = new int[skus.Length];\n        for (int i = 0; i < skus.Length; i++) outp[i] = fetched[first[skus[i]]];\n        return outp;\n    }\n\n    public static bool Threw(Action a) { try { a(); return false; } catch { return true; } }\n}\n',
    ),

print("module 19 authored")
