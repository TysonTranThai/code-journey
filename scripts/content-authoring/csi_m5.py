#!/usr/bin/env python3
"""C# — Intermediate — Module 5: csi-generics.

Generic design: constraints, default!, generic algorithms, variance.
Ws are behavioral near-misses.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-generics"

write_module(
    M,
    "Generic Design",
    "Constraints that document requirements, generic algorithms, and covariance/contravariance without tears.",
    "Thiết kế Generic",
    "Ràng buộc ghi chú yêu cầu, thuật toán generic, và covariance/contravariance không đau đầu.",
    ["constraints", "variance", "csi-checkpoint-m5"],
    ["csi-p5-generics"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "constraints",
    "Constraints: The Contract Inside the Angle Brackets",
    "where clauses as documented requirements, default(T) and default!, and generic algorithm design.",
    16,
    r"""
## An unconstrained T promises nothing

Inside `class Box<T>`, the compiler knows only "T is a type." You cannot
compare, construct, or order it. Constraints are how you buy abilities:

```csharp
public static T Max<T>(T a, T b) where T : IComparable<T> =>
    a.CompareTo(b) >= 0 ? a : b;

public static T New<T>() where T : new() => new T();   // constructible

public class Repo<T> where T : class, IEntity, new()
{
    // can use T.Id (IEntity), null-check like a class (class), new T() (new())
}

public static T Pick<T>(T[] items, int i) where T : struct
    => items[i];   // value-type-only: no nulls possible
```

Constraint vocabulary: `where T : class`, `struct`, `new()`, `IComparable<T>`,
`SomeBaseClass`, `IEnumerable<T>`, and combinations (comma-separated; multiple
`where` lines for multiple parameters). Constraints are *requirements you can
read* — an API with `where T : IComparable<T>` documents itself.

## Default values for T

`default(T)` (or just `default`): null for reference types, zeroed for value
types. In generic code that returns "nothing yet":

```csharp
public T? Find(Predicate<T> match)
{
    foreach (T item in _items)
        if (match(item)) return item;
    return default;          // null or zero — honest per T's kind
}
```

The `default!` escape (`= null!` on a field) tells the compiler "trust me" —
legitimate only when construction is guaranteed elsewhere (DI containers,
serializers) and a lie anywhere else.

## Generic algorithms

Write the algorithm ONCE over shapes:

```csharp
public static int CountWhile<T>(IEnumerable<T> source, Func<T, bool> ok)
{
    int n = 0;
    foreach (T item in source) if (ok(item)) n++;
    return n;
}
```

The algorithm never boxes, never casts — type safety end to end, which is
exactly what `ArrayList`-era code could not promise.

## Check your understanding

- Why `IComparable<T>` and not `IComparable`? (The non-generic one boxes and needs casts.)
- What is `default` for `int`? For `string`? `bool`? (0, null, false.)
""",
    "Ràng buộc: Hợp đồng trong ngoặc nhọn",
    "Mệnh đề where như yêu cầu được ghi chú, default(T) và default!, và thiết kế thuật toán generic.",
    r"""
## T không ràng buộc không hứa gì cả

Bên trong `class Box<T>`, compiler chỉ biết "T là một kiểu." Bạn không thể so
sánh, khởi tạo, hay sắp xếp nó. Ràng buộc là cách bạn mua quyền năng:

```csharp
public static T Max<T>(T a, T b) where T : IComparable<T> =>
    a.CompareTo(b) >= 0 ? a : b;

public static T New<T>() where T : new() => new T();   // khởi tạo được

public class Repo<T> where T : class, IEntity, new()
{
    // dùng được T.Id (IEntity), null-check như class (class), new T() (new())
}

public static T Pick<T>(T[] items, int i) where T : struct
    => items[i];   // chỉ-kiểu-giá-trị: không thể có null
```

Từ vựng ràng buộc: `where T : class`, `struct`, `new()`, `IComparable<T>`,
`SomeBaseClass`, `IEnumerable<T>`, và tổ hợp (ngăn cách bằng phẩy; nhiều
dòng `where` cho nhiều tham số). Ràng buộc là *yêu cầu đọc được* — một API
có `where T : IComparable<T>` tự tài liệu hóa.

## Giá trị mặc định cho T

`default(T)` (hoặc chỉ `default`): null cho kiểu tham chiếu, zero cho kiểu
giá trị. Trong code generic trả về "chưa có gì":

```csharp
public T? Find(Predicate<T> match)
{
    foreach (T item in _items)
        if (match(item)) return item;
    return default;          // null hoặc zero — trung thực theo từng loại T
}
```

Lối thoát `default!` (`= null!` trên một trường) nói với compiler "tin mình
đi" — chính đáng chỉ khi việc khởi tạo được đảm bảo ở nơi khác (DI container,
serializer), và là lời nói dối ở mọi nơi khác.

## Thuật toán generic

Viết thuật toán MỘT LẦN trên các hình dạng:

```csharp
public static int CountWhile<T>(IEnumerable<T> source, Func<T, bool> ok)
{
    int n = 0;
    foreach (T item in source) if (ok(item)) n++;
    return n;
}
```

Thuật toán không bao giờ box, không bao giờ ép kiểu — an toàn kiểu từ đầu
đến cuối, điều mà code thời `ArrayList` không thể hứa.

## Kiểm tra hiểu biết

- Vì sao `IComparable<T>` chứ không `IComparable`? (Bản non-generic box và cần ép kiểu.)
- `default` của `int`? `string`? `bool`? (0, null, false.)
""",
    r"""
## T không ràng buộc không hứa gì cả

Bên trong `class Box<T>`, compiler chỉ biết "T là một kiểu." Bạn không thể so
sánh, khởi tạo, hay sắp xếp nó. Ràng buộc là cách bạn mua quyền năng:

```csharp
public static T Max<T>(T a, T b) where T : IComparable<T> =>
    a.CompareTo(b) >= 0 ? a : b;

public static T New<T>() where T : new() => new T();   // khởi tạo được

public class Repo<T> where T : class, IEntity, new()
{
    // dùng được T.Id (IEntity), null-check như class (class), new T() (new())
}

public static T Pick<T>(T[] items, int i) where T : struct
    => items[i];   // chỉ-kiểu-giá-trị: không thể có null
```

Từ vựng ràng buộc: `where T : class`, `struct`, `new()`, `IComparable<T>`,
`SomeBaseClass`, `IEnumerable<T>`, và tổ hợp (ngăn cách bằng phẩy; nhiều
dòng `where` cho nhiều tham số). Ràng buộc là *yêu cầu đọc được* — một API
có `where T : IComparable<T>` tự tài liệu hóa.

## Giá trị mặc định cho T

`default(T)` (hoặc chỉ `default`): null cho kiểu tham chiếu, zero cho kiểu
giá trị. Trong code generic trả về "chưa có gì":

```csharp
public T? Find(Predicate<T> match)
{
    foreach (T item in _items)
        if (match(item)) return item;
    return default;          // null hoặc zero — trung thực theo từng loại T
}
```

Lối thoát `default!` (`= null!` trên một trường) nói với compiler "tin mình
đi" — chính đáng chỉ khi việc khởi tạo được đảm bảo ở nơi khác (DI container,
serializer), và là lời nói dối ở mọi nơi khác.

## Thuật toán generic

Viết thuật toán MỘT LẦN trên các hình dạng:

```csharp
public static int CountWhile<T>(IEnumerable<T> source, Func<T, bool> ok)
{
    int n = 0;
    foreach (T item in source) if (ok(item)) n++;
    return n;
}
```

Thuật toán không bao giờ box, không bao giờ ép kiểu — an toàn kiểu từ đầu
đến cuối, điều mà code thời `ArrayList` không thể hứa.

## Kiểm tra hiểu biết

- Vì sao `IComparable<T>` chứ không `IComparable`? (Bản non-generic box và cần ép kiểu.)
- `default` của `int`? `string`? `bool`? (0, null, false.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "variance",
    "Covariance and Contravariance",
    "Which generic directions convert safely, why Dictionary is invariant, and the IEnumerable<out T> rule.",
    15,
    r"""
## Two directions of safe conversion

**Covariance** (`out T`): if `string : object`, then `IEnumerable<string>`
converts to `IEnumerable<object>`. Output positions only — you can pull a
string out and hand it over as object.

```csharp
IEnumerable<object> shapes = new List<string> { "a" };   // legal: out T
```

**Contravariance** (`in T`): `Action<object>` converts to `Action<string>`.
Input positions only — a delegate that accepts any object can serve where a
string-eater is needed.

```csharp
Action<object> logAny = o => Console.WriteLine(o);
Action<string> logStr = logAny;                          // legal: in T
```

Both are compile-time guarantees the compiler checks for you: a `T` in an
output position makes the parameter covariant-eligible; in input positions,
contravariant. Mutating interfaces (`IList<T>`, `Dictionary<K,V>`) are
**invariant** — a list you can insert into must reject the conversion, or
`shapes.Add(42)` would corrupt a `List<string>`.

## The mental model

- `out T` = "I only produce T" → covariant (more specific collection is-a
  less specific one).
- `in T` = "I only consume T" → contravariant (a general consumer is-a
  specific one).
- Both = invariant (I do both; no safe direction).

`Func<in T, out TResult>` has both annotations — read it as a promise about
each position.

## Check your understanding

- Why is `IList<string>` → `IList<object>` illegal? (Add(object) would insert non-strings.)
- `Comparison<in T>` — which variance and why? (Contravariant: it consumes T.)
""",
    "Covariance và Contravariance",
    "Hướng chuyển đổi generic nào an toàn, vì sao Dictionary bất biến, và luật IEnumerable<out T>.",
    r"""
## Hai hướng chuyển đổi an toàn

**Covariance** (`out T`): nếu `string : object`, thì `IEnumerable<string>`
chuyển thành `IEnumerable<object>`. Chỉ vị trí output — bạn kéo string ra và
đưa đi như object.

```csharp
IEnumerable<object> shapes = new List<string> { "a" };   // hợp lệ: out T
```

**Contravariance** (`in T`): `Action<object>` chuyển thành `Action<string>`.
Chỉ vị trí input — delegate nhận mọi object có thể phục vụ chỗ cần kẻ ăn-string.

```csharp
Action<object> logAny = o => Console.WriteLine(o);
Action<string> logStr = logAny;                          // hợp lệ: in T
```

Cả hai là cam kết lúc biên dịch mà compiler kiểm tra giúp bạn: `T` ở vị trí
output làm tham số đủ điều kiện covariance; ở vị trí input, contravariance.
Các interface biến đổi (`IList<T>`, `Dictionary<K,V>`) **bất biến** — danh
sách cho phép chèn phải từ chối chuyển đổi, nếu không `shapes.Add(42)` sẽ
làm hỏng một `List<string>`.

## Mô hình tâm trí

- `out T` = "tôi chỉ sản xuất T" → covariant (bộ sưu tập cụ thể hơn là-một
  bộ sưu tập chung hơn).
- `in T` = "tôi chỉ tiêu thụ T" → contravariant (người tiêu thụ chung là-một
  người tiêu thụ riêng).
- Cả hai = bất biến (tôi làm cả hai; không hướng an toàn nào).

`Func<in T, out TResult>` mang cả hai chú thích — đọc nó như lời hứa về từng
vị trí.

## Kiểm tra hiểu biết

- Vì sao `IList<string>` → `IList<object>` bất hợp lệ? (Add(object) sẽ chèn phần tử không phải string.)
- `Comparison<in T>` — variance nào và vì sao? (Contravariant: nó tiêu thụ T.)
""",
    r"""
## Hai hướng chuyển đổi an toàn

**Covariance** (`out T`): nếu `string : object`, thì `IEnumerable<string>`
chuyển thành `IEnumerable<object>`. Chỉ vị trí output — bạn kéo string ra và
đưa đi như object.

```csharp
IEnumerable<object> shapes = new List<string> { "a" };   // hợp lệ: out T
```

**Contravariance** (`in T`): `Action<object>` chuyển thành `Action<string>`.
Chỉ vị trí input — delegate nhận mọi object có thể phục vụ chỗ cần kẻ ăn-string.

```csharp
Action<object> logAny = o => Console.WriteLine(o);
Action<string> logStr = logAny;                          // hợp lệ: in T
```

Cả hai là cam kết lúc biên dịch mà compiler kiểm tra giúp bạn: `T` ở vị trí
output làm tham số đủ điều kiện covariance; ở vị trí input, contravariance.
Các interface biến đổi (`IList<T>`, `Dictionary<K,V>`) **bất biến** — danh
sách cho phép chèn phải từ chối chuyển đổi, nếu không `shapes.Add(42)` sẽ
làm hỏng một `List<string>`.

## Mô hình tâm trí

- `out T` = "tôi chỉ sản xuất T" → covariant (bộ sưu tập cụ thể hơn là-một
  bộ sưu tập chung hơn).
- `in T` = "tôi chỉ tiêu thụ T" → contravariant (người tiêu thụ chung là-một
  người tiêu thụ riêng).
- Cả hai = bất biến (tôi làm cả hai; không hướng an toàn nào).

`Func<in T, out TResult>` mang cả hai chú thích — đọc nó như lời hứa về từng
vị trí.

## Kiểm tra hiểu biết

- Vì sao `IList<string>` → `IList<object>` bất hợp lệ? (Add(object) sẽ chèn phần tử không phải string.)
- `Comparison<in T>` — variance nào và vì sao? (Contravariant: nó tiêu thụ T.)
""",
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m5",
    "Checkpoint — The Generic Data Store",
    "Build a constrained generic store with ordering, defaults, and variance-safe surfaces.",
    22,
    r"""
## The gate (mini-build)

A `DataStore<TId, TEntity>` where `TEntity : Entity<TId>` and
`TId : IComparable<TId>`:

- `Add(TEntity)` / `Get(TId)` (null when missing) / `Delete(TId)` (bool).
- `AllOrdered()` returns entities ordered by Id — the constraint makes the
  ordering possible without casts.
- `FirstMatching(Predicate<TEntity>)` returns `TEntity?` (default when none).

Supporting type: `public abstract class Entity<TId> { public abstract TId Id { get; } }`.
The graded test drives two different entity types through one store type —
the whole point of generic design.
""",
    "Checkpoint — Kho dữ liệu Generic",
    "Xây kho generic có ràng buộc với sắp thứ tự, giá trị mặc định, và bề mặt an toàn variance.",
    r"""
## Cổng kiểm tra (mini-build)

Một `DataStore<TId, TEntity>` với `TEntity : Entity<TId>` và
`TId : IComparable<TId>`:

- `Add(TEntity)` / `Get(TId)` (null khi thiếu) / `Delete(TId)` (bool).
- `AllOrdered()` trả về các entity sắp theo Id — ràng buộc làm việc sắp thứ
  tự khả thi không cần ép kiểu.
- `FirstMatching(Predicate<TEntity>)` trả về `TEntity?` (default khi không có).

Kiểu hỗ trợ: `public abstract class Entity<TId> { public abstract TId Id { get; } }`.
Test chấm dẫn hai kiểu entity khác nhau qua một kiểu kho — đó là toàn bộ ý
nghĩa của thiết kế generic.
""",
    challenge(
        "csi-checkpoint-m5-task",
        "Checkpoint: DataStore<TId, TEntity>",
        """Implement the DataStore described in the checkpoint:

```csharp
public abstract class Entity<TId> { public abstract TId Id { get; } }

public class DataStore<TId, TEntity>
    where TEntity : Entity<TId>
    where TId : IComparable<TId>
{
    public void Add(TEntity entity);
    public TEntity? Get(TId id);
    public bool Delete(TId id);
    public List<TEntity> AllOrdered();
    public TEntity? FirstMatching(Predicate<TEntity> match);
}
```""",
        CS_PRELUDE,
        [
            (
                "crud and ordering",
                r"""
var store = new Solution.DataStore<int, Solution.User>();
var u3 = new Solution.User(3, "cat"); var u1 = new Solution.User(1, "ann"); var u2 = new Solution.User(2, "bob");
store.Add(u3); store.Add(u1); store.Add(u2);
Cj.Eq(store.Get(2)!.Name, "bob", "get by id");
Cj.Eq(store.Get(9), null, "missing -> null");
Cj.True(store.Delete(1), "delete existing");
Cj.False(store.Delete(1), "delete gone");
Cj.Eq(string.Join(",", store.AllOrdered().ConvertAll(u => u.Id.ToString())), "2,3", "ordered by id after delete");
""",
                "Dictionary<TId, TEntity> backing; OrderBy uses the IComparable constraint.",
            ),
            (
                "two entity types, one store",
                r"""
var orders = new Solution.DataStore<string, Solution.Order>();
orders.Add(new Solution.Order("o-2", 9m));
orders.Add(new Solution.Order("o-1", 5m));
Cj.Eq(orders.Get("o-1")!.Total, 5m, "string id works");
Cj.Eq(string.Join(",", orders.AllOrdered().ConvertAll(o => o.Id)), "o-1,o-2", "string ordering");
var found = orders.FirstMatching(o => o.Total > 6m);
Cj.Eq(found!.Id, "o-2", "predicate search");
Cj.Eq(orders.FirstMatching(o => o.Total > 99m), null, "no match -> null");
""",
                "The same store class serves any Entity<TId> — that is the generic contract paying off.",
            ),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Checkpoint: DataStore<TId, TEntity>",
        "Hiện thực DataStore mô tả trong checkpoint: CRUD, AllOrdered qua ràng buộc IComparable, FirstMatching trả default khi không khớp — hai kiểu entity, một lớp kho.",
        [
            ("crud and ordering", "Dictionary<TId, TEntity> làm nền; OrderBy dùng ràng buộc IComparable."),
            ("two entity types, one store", "Cùng một lớp kho phục vụ mọi Entity<TId> — đó là hợp đồng generic đền đáp."),
        ],
    ),
    solution='public class Solution\n{\n    public abstract class Entity<TId>\n    {\n        public abstract TId Id { get; }\n    }\n\n    public sealed class User : Entity<int>\n    {\n        public User(int id, string name) { Id = id; Name = name; }\n        public override int Id { get; }\n        public string Name { get; }\n    }\n\n    public sealed class Order : Entity<string>\n    {\n        public Order(string id, decimal total) { Id = id; Total = total; }\n        public override string Id { get; }\n        public decimal Total { get; }\n    }\n\n    public class DataStore<TId, TEntity>\n        where TEntity : Entity<TId>\n        where TId : IComparable<TId>\n    {\n        private readonly Dictionary<TId, TEntity> _items = new();\n\n        public void Add(TEntity entity) => _items[entity.Id] = entity;\n\n        public TEntity? Get(TId id) => _items.TryGetValue(id, out TEntity? e) ? e : default;\n\n        public bool Delete(TId id) => _items.Remove(id);\n\n        public List<TEntity> AllOrdered() => _items.Values.OrderBy(e => e.Id).ToList();\n\n        public TEntity? FirstMatching(Predicate<TEntity> match)\n        {\n            foreach (TEntity e in _items.Values)\n                if (match(e)) return e;\n            return default;\n        }\n    }\n}\n',
    wrong='public class Solution\n{\n    public abstract class Entity<TId>\n    {\n        public abstract TId Id { get; }\n    }\n\n    public sealed class User : Entity<int>\n    {\n        public User(int id, string name) { Id = id; Name = name; }\n        public override int Id { get; }\n        public string Name { get; }\n    }\n\n    public sealed class Order : Entity<string>\n    {\n        public Order(string id, decimal total) { Id = id; Total = total; }\n        public override string Id { get; }\n        public decimal Total { get; }\n    }\n\n    public class DataStore<TId, TEntity>\n        where TEntity : Entity<TId>\n        where TId : IComparable<TId>\n    {\n        private readonly Dictionary<TId, TEntity> _items = new();\n\n        public void Add(TEntity entity) => _items[entity.Id] = entity;\n\n        public TEntity? Get(TId id) => _items.TryGetValue(id, out TEntity? e) ? e : default;\n\n        public bool Delete(TId id) => _items.Remove(id);\n\n        public List<TEntity> AllOrdered() =>\n            // near-miss: insertion order, not Id order — the "ordered by id"\n            // test fails after a delete reshuffles expectations\n            _items.Values.ToList();\n\n        public TEntity? FirstMatching(Predicate<TEntity> match)\n        {\n            foreach (TEntity e in _items.Values)\n                if (match(e)) return e;\n            return default;\n        }\n    }\n}\n',
)
print("module 5 authored")

# ---------------------------------------------------------------- practices
write_practice(
    M,
    "csi-p5-generics",
    "Generic Design Practice",
    "Constraints that promise, algorithms that stay type-safe, and variance you can predict without the compiler guessing for you.",
    "Luyện thiết kế generic",
    "Ràng buộc ghi đúng lời hứa, thuật toán giữ an toàn kiểu, và variance bạn tự đoán được mà không cần compiler đoán hộ.",
    "csi-variance",
    25,
    "intermediate",
    [
        challenge(
            "csi-p5-max",
            "A Generic Max That Can Actually Compare",
            """Implement `Max`: returns the largest of two values for any type that knows how to compare itself. A null argument makes it return the other one (both null returns default).

```csharp
static T? Max<T>(T? a, T? b) where T : IComparable<T>;
```""",
            CS_PRELUDE,
            [
                (
                    "comparable types",
                    r"""
Cj.Eq(Solution.Max(3, 7), 7, "ints");
Cj.Eq(Solution.Max("apple", "banana"), "banana", "strings compare ordinally");
Cj.Eq(Solution.Max(2.5m, 2.4m), 2.5m, "decimals");
""",
                    "a.CompareTo(b) >= 0 means a wins — the constraint unlocks CompareTo.",
                ),
                (
                    "null handling",
                    r"""
Cj.Eq(Solution.Max<string>(null, "b"), "b", "null a -> b");
Cj.Eq(Solution.Max<string>("a", null), "a", "null b -> a");
Cj.True(Solution.Max<string>(null, null) is null, "both null -> null");
// note: int? cannot satisfy IComparable<int?> — Nullable<T> implements no
// interfaces. That IS the lesson: the constraint gates value-type nulls out.
Cj.Eq(Solution.Max("b", null), "b", "constraint keeps nulls flowing on the null side only");
""",
                    "Null-check first: reference-type T? and lifted struct T? both flow through here.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p5-repository",
            "The Typed Repository",
            """Implement `Repository<T>` where `T : IHasId`: `Add` stores by Id (re-adding REPLACES), `Get` returns default when absent, `Count` and `All` round out the surface.

```csharp
public interface IHasId { int Id { get; } }
public class Repository<T> where T : IHasId
{
    public void Add(T entity);
    public T? Get(int id);
    public int Count { get; }
    public IReadOnlyCollection<T> All();
}
```""",
            CS_PRELUDE,
            [
                (
                    "store, replace, count",
                    r"""
var repo = new Solution.Repository<Solution.User>();
repo.Add(new Solution.User(1, "ann"));
repo.Add(new Solution.User(2, "bob"));
Cj.Eq(repo.Count, 2, "two users");
repo.Add(new Solution.User(1, "ann2"));
Cj.Eq(repo.Count, 2, "re-add replaces, not duplicates");
Cj.Eq(repo.Get(1)!.Name, "ann2", "replacement is what Get returns");
""",
                    "Dictionary<int, T> indexed by entity.Id — indexer assignment replaces.",
                ),
                (
                    "misses and enumeration",
                    r"""
var repo2 = new Solution.Repository<Solution.User>();
Cj.True(repo2.Get(42) is null, "absent id -> default");
repo2.Add(new Solution.User(7, "cy"));
Cj.Eq(repo2.All().Count, 1, "All mirrors contents");
Cj.True(repo2.All() is IReadOnlyCollection<Solution.User>, "readonly surface");
""",
                    "Get: TryGetValue, return default on miss. All: return the Values as a read-only surface.",
                ),
            ],
            level="independent",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p5-copy-bug-debug",
            "Debug: The Variance Crash",
            """`CopyAll` was written for `List<object>` but callers hold `IEnumerable<string>` — and the current version does not compile OR (after someone "fixed" it with a cast) crashes. Fix `CopyAll` so it accepts ANY sequence of references-to-string-or-base and returns a fresh `List<string>` of the same elements.

```csharp
static List<string> CopyAll(IEnumerable<string> source);
// and a generic overload usable for ANY element type:
static List<T> CopyAll<T>(IEnumerable<T> source);
```""",
            CS_PRELUDE,
            [
                (
                    "string sequence accepted",
                    r"""
var words = new List<string> { "a", "b" };
var copy = Solution.CopyAll(words);
Cj.Eq(copy.Count, 2, "copied");
copy.Add("c");
Cj.Eq(words.Count, 2, "copy is independent of source");
""",
                    "IEnumerable<out T> is covariant — accept IEnumerable<string>, return a NEW list (no shared storage).",
                ),
                (
                    "generic overload works for any T",
                    r"""
var nums = new[] { 1, 2, 3 };
var numCopy = Solution.CopyAll<int>(nums);
Cj.Eq(numCopy.Count, 3, "ints copy too");
Cj.Eq(string.Join(",", Solution.CopyAll(new List<string> { "x" })), "x", "generic inference picks the overload");
""",
                    "One generic method handles every T — the variance is in the parameter type, not the algorithm.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p5-max": vi_challenge(
            "Generic Max biết so sánh",
            "Hiện thực `Max`: trả giá trị lớn hơn trong hai giá trị cho bất kỳ kiểu nào tự so sánh được. Đối số null thì trả cái còn lại (cả hai null trả default).",
            [
                ("comparable types", "a.CompareTo(b) >= 0 nghĩa là a thắng — ràng buộc mở khóa CompareTo."),
                ("null handling", "Kiểm tra null trước: T? kiểu tham chiếu và T? struct lifted đều chảy qua đây."),
            ],
        ),
        "csi-p5-repository": vi_challenge(
            "Repository có kiểu",
            "Hiện thực `Repository<T>` với `T : IHasId`: `Add` lưu theo Id (thêm lại là THAY THẾ), `Get` trả default khi thiếu, `Count` và `All` hoàn thiện bề mặt.",
            [
                ("store, replace, count", "Dictionary<int, T> đánh chỉ số theo entity.Id — gán indexer là thay thế."),
                ("misses and enumeration", "Get: TryGetValue, trả default khi miss. All: trả Values dưới bề mặt read-only."),
            ],
        ),
        "csi-p5-copy-bug-debug": vi_challenge(
            "Debug: cú va chạm variance",
            "`CopyAll` viết cho `List<object>` nhưng caller cầm `IEnumerable<string>` — và bản hiện tại không biên dịch được HOẶC (sau khi ai đó \"sửa\" bằng cast) bị sập. Sửa `CopyAll` để nhận BẤT KỲ chuỗi phần tử nào kế thừa-được và trả một `List<string>` mới chứa cùng phần tử.",
            [
                ("string sequence accepted", "IEnumerable<out T> là covariant — nhận IEnumerable<string>, trả list MỚI (không chia sẻ bộ nhớ)."),
                ("generic overload works for any T", "Một phương thức generic lo cho mọi T — variance nằm ở kiểu tham số, không ở thuật toán."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p5-max",
            'public class Solution\n{\n    public static T? Max<T>(T? a, T? b) where T : IComparable<T>\n    {\n        if (a is null) return b;\n        if (b is null) return a;\n        return a.CompareTo(b) >= 0 ? a : b;\n    }\n}\n',
            'public class Solution\n{\n    // near-miss: compares via object.Equals — values that compare equal\n    // (2.50 vs 2.5) hit the wrong branch, and CompareTo ordering is ignored\n    public static T? Max<T>(T? a, T? b) where T : IComparable<T>\n    {\n        if (a is null) return b;\n        if (b is null) return a;\n        return a.Equals(b) ? a : b;\n    }\n}\n',
        ),
        (
            "csi-p5-repository",
            'public class Solution\n{\n    public interface IHasId { int Id { get; } }\n\n    public class User : IHasId\n    {\n        public User(int id, string name) { Id = id; Name = name; }\n        public int Id { get; }\n        public string Name { get; }\n    }\n\n    public class Repository<T> where T : IHasId\n    {\n        private readonly Dictionary<int, T> _items = new();\n\n        public void Add(T entity) => _items[entity.Id] = entity;\n\n        public T? Get(int id) => _items.TryGetValue(id, out var e) ? e : default;\n\n        public int Count => _items.Count;\n\n        public IReadOnlyCollection<T> All() => _items.Values.ToList();\n    }\n}\n',
            'public class Solution\n{\n    public interface IHasId { int Id { get; } }\n\n    public class User : IHasId\n    {\n        public User(int id, string name) { Id = id; Name = name; }\n        public int Id { get; }\n        public string Name { get; }\n    }\n\n    public class Repository<T> where T : IHasId\n    {\n        private readonly List<T> _items = new();\n\n        public void Add(T entity)\n        {\n            // near-miss: Add appends — re-adding the same Id duplicates\n            // instead of replacing\n            _items.Add(entity);\n        }\n\n        public T? Get(int id)\n        {\n            foreach (var e in _items)\n                if (e.Id == id) return e;\n            return default;\n        }\n\n        public int Count => _items.Count;\n\n        public IReadOnlyCollection<T> All() => _items;\n    }\n}\n',
        ),
        (
            "csi-p5-copy-bug-debug",
            'public class Solution\n{\n    public static List<string> CopyAll(System.Collections.Generic.IEnumerable<string> source)\n        => source.ToList();\n\n    public static List<T> CopyAll<T>(System.Collections.Generic.IEnumerable<T> source)\n        => source.ToList();\n}\n',
            'public class Solution\n{\n    // near-miss: returns the SAME instance cast back — mutations of the\n    // "copy" leak into the source list\n    public static List<string> CopyAll(System.Collections.Generic.IEnumerable<string> source)\n        => source as List<string> ?? source.ToList();\n\n    public static List<T> CopyAll<T>(System.Collections.Generic.IEnumerable<T> source)\n        => source as List<T> ?? source.ToList();\n}\n',
        ),
    ],
)

print("module 5 authored")
