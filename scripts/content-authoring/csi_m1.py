#!/usr/bin/env python3
"""C# — Intermediate — Module 1: csi-modern-types.

The type system deep dive: value vs reference semantics, boxing, nullable
value types + NRT annotations, pattern matching mastery, tuples and
deconstruction. All graded code is single-TU `public class Solution` static
methods; Ws are behavioral near-misses, never syntax errors.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-modern-types"

write_module(
    M,
    "The Type System Deep Dive",
    "Value vs reference semantics, boxing, the nullable machinery, and pattern matching as an everyday design tool.",
    "Hệ thống kiểu chuyên sâu",
    "Ngữ nghĩa giá trị so với tham chiếu, boxing, cơ chế nullable, và pattern matching như công cụ thiết kế hằng ngày.",
    ["type-semantics", "nullability", "pattern-matching", "csi-checkpoint-m1"],
    ["csi-p1-semantics", "csi-p1-patterns"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "type-semantics",
    "Value vs Reference, Boxing, and Identity",
    "What actually copies, what actually aliases, when structs get boxed, and why Equals differs from ==.",
    16,
    r"""
## Two families, two behaviors

A **value type** (struct, enum, numeric types, bool, char) carries its data
inline. Assignment copies the whole value. A **reference type** (class,
record class, interface, delegate, array, string) stores a reference; the
object lives on the heap, and assignment copies only the reference — two
variables then alias one object.

```csharp
struct PointS { public int X; }
class  PointC { public int X; }

var s1 = new PointS { X = 1 };
var s2 = s1; s2.X = 9;              // s1.X is still 1 — copy

var c1 = new PointC { X = 1 };
var c2 = c1; c2.X = 9;              // c1.X is now 9 — alias
```

Neither is "better". Use structs for small, immutable, leaf values
(coordinates, money amounts, identifiers); classes for entities with
identity and lifetime. `record struct` gives you value semantics with
generated equality; `record` (class) gives reference semantics with
value-based equality — handy but distinct things.

## Boxing: the invisible heap allocation

Boxing wraps a value type in a heap object so it can travel where a
reference is expected. It happens silently in three common places:

```csharp
object o = 42;                       // explicit box
IComparable<int> c = 7;              // interface box
Console.WriteLine(string.Join(" ", 1, 2, 3));   // params object[]: each int boxes
```

Unboxing is the reverse cast — it must name the EXACT type: unboxing a
boxed `int` as `double` throws `InvalidCastException`, even though
`int → double` converts implicitly in normal code.

Boxing costs allocation and hurts in hot loops. `Console.WriteLine(42)`
does NOT box (it has an int overload) — but `string.Format("{0}", x)` with
an `object[]` path does. Equality gets subtle too: boxed values compare by
value with `Equals`, but `==` on `object` compares references:

```csharp
object a = 1000, b = 1000;
a.Equals(b)      // true  — boxed int compares by value
a == b           // false — different boxes
(object)a == (object)1000   // false again
```

## Check your understanding

- `DateTime` is a struct: after `d2 = d1; d2 = d2.AddDays(1)`, what is `d1`?
  (Unchanged — `AddDays` returns a new value.)
- Why does `ArrayList` (pre-generics) feel slow for ints? (Every Add boxes.)
- What does `(short)(object)intVar` throw? (InvalidCastException — exact-type rule.)
""",
    "Giá trị so với tham chiếu, boxing, và bản sắc",
    "Cái gì thật sự sao chép, cái gì thật sự tham chiếu, khi nào struct bị boxing, và vì sao Equals khác ==.",
    r"""
## Hai họ, hai hành vi

**Kiểu giá trị** (struct, enum, kiểu số, bool, char) mang dữ liệu ngay trong
nó. Gán là sao chép toàn bộ giá trị. **Kiểu tham chiếu** (class, record
class, interface, delegate, mảng, string) lưu một tham chiếu; đối tượng nằm
trên heap, và phép gán chỉ sao chép tham chiếu — hai biến khi đó trỏ chung
một đối tượng.

```csharp
struct PointS { public int X; }
class  PointC { public int X; }

var s1 = new PointS { X = 1 };
var s2 = s1; s2.X = 9;              // s1.X vẫn là 1 — bản sao

var c1 = new PointC { X = 1 };
var c2 = c1; c2.X = 9;              // c1.X giờ là 9 — cùng đối tượng
```

Không bên nào "tốt hơn". Dùng struct cho giá trị lá nhỏ, bất biến (tọa độ,
số tiền, mã định danh); dùng class cho thực thể có bản sắc và vòng đời.
`record struct` cho ngữ nghĩa giá trị kèm equality tự sinh; `record`
(class) cho ngữ nghĩa tham chiếu với equality theo giá trị — hai thứ khác
nhau, đừng nhầm.

## Boxing: cấp phát heap vô hình

Boxing gói giá trị vào một đối tượng trên heap để nó đi được tới nơi cần
tham chiếu. Nó xảy ra âm thầm ở ba chỗ thường gặp:

```csharp
object o = 42;                       // boxing tường minh
IComparable<int> c = 7;              // boxing qua interface
Console.WriteLine(string.Join(" ", 1, 2, 3));   // params object[]: mỗi int bị box
```

Unboxing là phép ép ngược — phải gọi ĐÚNG kiểu: unbox một `int` đã box thành
`double` ném `InvalidCastException`, dù trong code thường `int → double`
chuyển đổi ngầm được.

Boxing tốn cấp phát và gây hại trong vòng lặp nóng. `Console.WriteLine(42)`
KHÔNG box (có overload nhận int) — nhưng `string.Format("{0}", x)` đi qua
`object[]` thì có. Equality cũng tinh tế: giá trị đã box so sánh theo giá trị
với `Equals`, nhưng `==` trên `object` so sánh tham chiếu:

```csharp
object a = 1000, b = 1000;
a.Equals(b)      // true  — boxed int so theo giá trị
a == b           // false — hai hộp khác nhau
(object)a == (object)1000   // false lần nữa
```

## Kiểm tra hiểu biết

- `DateTime` là struct: sau `d2 = d1; d2 = d2.AddDays(1)`, `d1` là gì?
  (Không đổi — `AddDays` trả về giá trị mới.)
- Vì sao `ArrayList` (thời tiền-generic) chậm với int? (Mọi Add đều box.)
- `(short)(object)intVar` ném gì? (InvalidCastException — luật đúng-kiểu.)
""",
    r"""
## Hai họ, hai hành vi

**Kiểu giá trị** (struct, enum, kiểu số, bool, char) mang dữ liệu ngay trong
nó. Gán là sao chép toàn bộ giá trị. **Kiểu tham chiếu** (class, record
class, interface, delegate, mảng, string) lưu một tham chiếu; đối tượng nằm
trên heap, và phép gán chỉ sao chép tham chiếu — hai biến khi đó trỏ chung
một đối tượng.

```csharp
struct PointS { public int X; }
class  PointC { public int X; }

var s1 = new PointS { X = 1 };
var s2 = s1; s2.X = 9;              // s1.X vẫn là 1 — bản sao

var c1 = new PointC { X = 1 };
var c2 = c1; c2.X = 9;              // c1.X giờ là 9 — cùng đối tượng
```

Không bên nào "tốt hơn". Dùng struct cho giá trị lá nhỏ, bất biến (tọa độ,
số tiền, mã định danh); dùng class cho thực thể có bản sắc và vòng đời.
`record struct` cho ngữ nghĩa giá trị kèm equality tự sinh; `record`
(class) cho ngữ nghĩa tham chiếu với equality theo giá trị — hai thứ khác
nhau, đừng nhầm.

## Boxing: cấp phát heap vô hình

Boxing gói giá trị vào một đối tượng trên heap để nó đi được tới nơi cần
tham chiếu. Nó xảy ra âm thầm ở ba chỗ thường gặp:

```csharp
object o = 42;                       // boxing tường minh
IComparable<int> c = 7;              // boxing qua interface
Console.WriteLine(string.Join(" ", 1, 2, 3));   // params object[]: mỗi int bị box
```

Unboxing là phép ép ngược — phải gọi ĐÚNG kiểu: unbox một `int` đã box thành
`double` ném `InvalidCastException`, dù trong code thường `int → double`
chuyển đổi ngầm được.

Boxing tốn cấp phát và gây hại trong vòng lặp nóng. `Console.WriteLine(42)`
KHÔNG box (có overload nhận int) — nhưng `string.Format("{0}", x)` đi qua
`object[]` thì có. Equality cũng tinh tế: giá trị đã box so sánh theo giá trị
với `Equals`, nhưng `==` trên `object` so sánh tham chiếu:

```csharp
object a = 1000, b = 1000;
a.Equals(b)      // true  — boxed int so theo giá trị
a == b           // false — hai hộp khác nhau
(object)a == (object)1000   // false lần nữa
```

## Kiểm tra hiểu biết

- `DateTime` là struct: sau `d2 = d1; d2 = d2.AddDays(1)`, `d1` là gì?
  (Không đổi — `AddDays` trả về giá trị mới.)
- Vì sao `ArrayList` (thời tiền-generic) chậm với int? (Mọi Add đều box.)
- `(short)(object)intVar` ném gì? (InvalidCastException — luật đúng-kiểu.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "nullability",
    "Nullable Value Types and the Null-State Machine",
    "int? vs int, HasValue/GetValueOrDefault, nullable reference type annotations, and making the compiler's warnings into design.",
    15,
    r"""
## Nullable value types: absence you can see

A value type cannot be null — unless you wrap it: `int?` is
`Nullable<int>`, a struct holding a `bool HasValue` plus a `T Value`.

```csharp
int? found = list.Find(x => x > 10);   // 0 would be a lie; null means "none"
if (found is int value) Use(value);    // pattern test + unwrap in one step
int fallback = found ?? -1;            // GetValueOrDefault-style default
```

`int?` lifts operators: `null + 5` is `null` (not an exception). Comparisons
with null are `false` — `null < 5` is false, not true.

## Nullable reference types: promises the compiler checks

Since C# 8, reference types are **non-nullable by default** under NRT. The
compiler tracks null-state and warns:

- `string?` — "may be null"; you must check before use.
- `string` — "expected non-null"; assigning null warns.
- `string? name = Fetch(); var len = name.Length;` — warning: possible null.
- After `if (name != null)` the compiler *knows* it is safe — flow analysis.
- `!` (null-forgiving) says "trust me" — a last resort, not a tool.

Two honest tools when null is a legitimate answer:

```csharp
string? found = dict.GetValueOrDefault(key);        // null is real absence
string  found2 = dict.GetValueOrDefault(key, "");   // or a default
```

And one dishonest one to avoid: initializing fields with `= null!` to
silence the compiler creates a lie that explodes later.

## The nullable machinery in API design

`TryX` patterns (like Beginner's `int.TryParse`) return `bool` + `out` value;
nullable returns let you express "no result" directly:

```csharp
public static int? ParseAge(string input) =>
    int.TryParse(input, out int age) && age >= 0 ? age : null;
```

Callers then use `??`, `is int v`, or `if (v is not null)` — null becomes a
visible, checkable part of the contract instead of an ambush.

## Check your understanding

- What is `(int?)null == null`? (True — lifted equality.)
- `string s = null;` under NRT — warning or error? (Warning; still compiles.)
- Why prefer `int?` over a magic `-1` sentinel? (Sentinels collide with real data.)
""",
    "Nullable value types và máy trạng thái null",
    "int? so với int, HasValue/GetValueOrDefault, chú thích nullable reference type, và biến cảnh báo của compiler thành thiết kế.",
    r"""
## Nullable value types: sự vắng mặt nhìn thấy được

Kiểu giá trị không thể null — trừ khi bạn bọc nó: `int?` là `Nullable<int>`,
một struct chứa `bool HasValue` và `T Value`.

```csharp
int? found = list.Find(x => x > 10);   // 0 sẽ là nói dối; null nghĩa là "không có"
if (found is int value) Use(value);    // kiểm tra + gỡ bọc trong một bước
int fallback = found ?? -1;            // mặc định kiểu GetValueOrDefault
```

`int?` nâng các toán tử: `null + 5` cho `null` (không phải exception). Phép
so sánh với null cho `false` — `null < 5` là false, không phải true.

## Nullable reference types: lời hứa compiler kiểm tra

Từ C# 8, kiểu tham chiếu **mặc định không-null** khi bật NRT. Compiler theo
dõi trạng thái null và cảnh báo:

- `string?` — "có thể null"; phải kiểm tra trước khi dùng.
- `string` — "kỳ vọng không-null"; gán null sẽ bị cảnh báo.
- `string? name = Fetch(); var len = name.Length;` — cảnh báo: có thể null.
- Sau `if (name != null)` compiler *biết* an toàn — phân tích luồng.
- `!` (null-forgiving) nghĩa là "tin mình đi" — giải pháp cuối, không phải công cụ.

Hai công cụ trung thực khi null là câu trả lời chính đáng:

```csharp
string? found = dict.GetValueOrDefault(key);        // null là sự vắng mặt thật
string  found2 = dict.GetValueOrDefault(key, "");   // hoặc mặc định
```

Và một thứ không trung thực cần tránh: khởi tạo trường bằng `= null!` để
im lặng compiler — tạo lời nói dối phát nổ về sau.

## Cơ chế nullable trong thiết kế API

Mẫu `TryX` (như `int.TryParse` ở Beginner) trả `bool` + `out`; trả nullable
cho phép diễn đạt "không có kết quả" trực tiếp:

```csharp
public static int? ParseAge(string input) =>
    int.TryParse(input, out int age) && age >= 0 ? age : null;
```

Người gọi dùng `??`, `is int v`, hoặc `if (v is not null)` — null trở thành
một phần nhìn thấy, kiểm tra được của hợp đồng thay vì cuộc phục kích.

## Kiểm tra hiểu biết

- `(int?)null == null` là gì? (True — equality đã nâng.)
- `string s = null;` dưới NRT — cảnh báo hay lỗi? (Cảnh báo; vẫn biên dịch.)
- Vì sao ưu tiên `int?` thay sentinel `-1` ma thuật? (Sentinel đụng dữ liệu thật.)
""",
    r"""
## Nullable value types: sự vắng mặt nhìn thấy được

Kiểu giá trị không thể null — trừ khi bạn bọc nó: `int?` là `Nullable<int>`,
một struct chứa `bool HasValue` và `T Value`.

```csharp
int? found = list.Find(x => x > 10);   // 0 sẽ là nói dối; null nghĩa là "không có"
if (found is int value) Use(value);    // kiểm tra + gỡ bọc trong một bước
int fallback = found ?? -1;            // mặc định kiểu GetValueOrDefault
```

`int?` nâng các toán tử: `null + 5` cho `null` (không phải exception). Phép
so sánh với null cho `false` — `null < 5` là false, không phải true.

## Nullable reference types: lời hứa compiler kiểm tra

Từ C# 8, kiểu tham chiếu **mặc định không-null** khi bật NRT. Compiler theo
dõi trạng thái null và cảnh báo:

- `string?` — "có thể null"; phải kiểm tra trước khi dùng.
- `string` — "kỳ vọng không-null"; gán null sẽ bị cảnh báo.
- `string? name = Fetch(); var len = name.Length;` — cảnh báo: có thể null.
- Sau `if (name != null)` compiler *biết* an toàn — phân tích luồng.
- `!` (null-forgiving) nghĩa là "tin mình đi" — giải pháp cuối, không phải công cụ.

Hai công cụ trung thực khi null là câu trả lời chính đáng:

```csharp
string? found = dict.GetValueOrDefault(key);        // null là sự vắng mặt thật
string  found2 = dict.GetValueOrDefault(key, "");   // hoặc mặc định
```

Và một thứ không trung thực cần tránh: khởi tạo trường bằng `= null!` để
im lặng compiler — tạo lời nói dối phát nổ về sau.

## Cơ chế nullable trong thiết kế API

Mẫu `TryX` (như `int.TryParse` ở Beginner) trả `bool` + `out`; trả nullable
cho phép diễn đạt "không có kết quả" trực tiếp:

```csharp
public static int? ParseAge(string input) =>
    int.TryParse(input, out int age) && age >= 0 ? age : null;
```

Người gọi dùng `??`, `is int v`, hoặc `if (v is not null)` — null trở thành
một phần nhìn thấy, kiểm tra được của hợp đồng thay vì cuộc phục kích.

## Kiểm tra hiểu biết

- `(int?)null == null` là gì? (True — equality đã nâng.)
- `string s = null;` dưới NRT — cảnh báo hay lỗi? (Cảnh báo; vẫn biên dịch.)
- Vì sao ưu tiên `int?` thay sentinel `-1` ma thuật? (Sentinel đụng dữ liệu thật.)
""",
)

# ---------------------------------------------------------------- lesson 3
write_lesson(
    M, "pattern-matching",
    "Pattern Matching Mastery",
    "Type patterns, property patterns, relational and logical patterns, switch expressions, tuples, and deconstruction.",
    17,
    r"""
## From if-chains to patterns

Pattern matching tests a value's *shape* and binds pieces of it. The switch
expression turns classification into data:

```csharp
public static string Describe(object o) => o switch
{
    int n when n < 0            => "negative int",
    int n and > 100             => "big int",
    int                         => "small int",
    string { Length: 0 }        => "empty string",
    string s                    => $"string of {s.Length}",
    null                        => "nothing",
    _                           => "unknown"
};
```

Building blocks, composable everywhere:

- **Type pattern** `int n` — test + bind.
- **Property pattern** `string { Length: 0 }`, `Point { X: > 0, Y: > 0 }`.
- **Relational** `> 100`, **logical** `and/or/not`.
- **Constant** `null`, enum values, literals.
- **List patterns** (C# 11): `[1, .., var last]` matches a sequence's shape.

## Exhaustiveness and hierarchy

With enums and closed hierarchies, the compiler can prove you covered every
case — miss one and you get a warning, not a runtime bug. That is why
switching on a `Shape` union beats `if/else` chains: the type system
participates in correctness. Add `_` too early and you *silence* that
protection — reach for it last.

```csharp
public enum LoadState { Idle, Loading, Ready, Failed }
public static bool IsBusy(LoadState s) => s switch
{
    LoadState.Loading => true,
    LoadState.Idle or LoadState.Ready or LoadState.Failed => false,
    _ => throw new ArgumentOutOfRangeException(nameof(s))  // future-proofing
};
```

## Tuples and deconstruction

Tuples group ad-hoc values; deconstruction unpacks anything with a
`Deconstruct` method (all records have one):

```csharp
(string name, int score) = ("ann", 92);
var (min, max) = (nums.Min(), nums.Max());
foreach (var (key, count) in dict)   // KeyValuePair deconstructs too
    Console.WriteLine($"{key}: {count}");
```

Switch on tuples for decision tables that read like tables:

```csharp
public static string Grade(int score, bool attended) => (score, attended) switch
{
    ( >= 90, true)  => "A+",
    ( >= 90, false) => "A",
    ( >= 80, _)     => "B",
    _               => "C"
};
```

## Check your understanding

- Why is `_ => ...` a double-edged sword? (Catches future cases silently.)
- When does a property pattern beat a guard clause? (When classifying, not validating.)
- What does `foreach (var (k, v) in dict)` rely on? (KeyValuePair.Deconstruct.)
""",
    "Pattern matching thành thạo",
    "Type pattern, property pattern, relational và logical pattern, switch expression, tuple, và deconstruction.",
    r"""
## Từ chuỗi if đến pattern

Pattern matching kiểm tra *hình dạng* của giá trị và gắn kết các mảnh của nó.
Switch expression biến việc phân loại thành dữ liệu:

```csharp
public static string Describe(object o) => o switch
{
    int n when n < 0            => "negative int",
    int n and > 100             => "big int",
    int                         => "small int",
    string { Length: 0 }        => "empty string",
    string s                    => $"string of {s.Length}",
    null                        => "nothing",
    _                           => "unknown"
};
```

Các viên gạch, ghép được ở khắp nơi:

- **Type pattern** `int n` — kiểm tra + gắn tên.
- **Property pattern** `string { Length: 0 }`, `Point { X: > 0, Y: > 0 }`.
- **Relational** `> 100`, **logical** `and/or/not`.
- **Constant** `null`, giá trị enum, literal.
- **List pattern** (C# 11): `[1, .., var last]` khớp hình dạng chuỗi.

## Tính đầy đủ và phân cấp

Với enum và hệ đóng, compiler chứng minh được bạn phủ mọi trường hợp — thiếu
một trường hợp bạn nhận cảnh báo, không phải bug lúc chạy. Đó là lý do switch
trên hợp `Shape` thắng chuỗi `if/else`: hệ thống kiểu tham gia vào tính đúng
đắn. Thêm `_` quá sớm và bạn *tắt* lớp bảo vệ đó — để nó làm phương án cuối.

```csharp
public enum LoadState { Idle, Loading, Ready, Failed }
public static bool IsBusy(LoadState s) => s switch
{
    LoadState.Loading => true,
    LoadState.Idle or LoadState.Ready or LoadState.Failed => false,
    _ => throw new ArgumentOutOfRangeException(nameof(s))  // phòng tương lai
};
```

## Tuple và deconstruction

Tuple gom các giá trị tạm thời; deconstruction bóc ra bất cứ thứ gì có phương
thức `Deconstruct` (mọi record đều có):

```csharp
(string name, int score) = ("ann", 92);
var (min, max) = (nums.Min(), nums.Max());
foreach (var (key, count) in dict)   // KeyValuePair cũng deconstruct được
    Console.WriteLine($"{key}: {count}");
```

Switch trên tuple cho bảng quyết định đọc như bảng thật:

```csharp
public static string Grade(int score, bool attended) => (score, attended) switch
{
    ( >= 90, true)  => "A+",
    ( >= 90, false) => "A",
    ( >= 80, _)     => "B",
    _               => "C"
};
```

## Kiểm tra hiểu biết

- Vì sao `_ => ...` là con dao hai lưỡi? (Bắt nốt các trường hợp tương lai một cách âm thầm.)
- Property pattern thắng guard clause khi nào? (Khi phân loại, không phải khi hợp lệ hóa.)
- `foreach (var (k, v) in dict)` dựa vào gì? (KeyValuePair.Deconstruct.)
""",
    r"""
## Từ chuỗi if đến pattern

Pattern matching kiểm tra *hình dạng* của giá trị và gắn kết các mảnh của nó.
Switch expression biến việc phân loại thành dữ liệu:

```csharp
public static string Describe(object o) => o switch
{
    int n when n < 0            => "negative int",
    int n and > 100             => "big int",
    int                         => "small int",
    string { Length: 0 }        => "empty string",
    string s                    => $"string of {s.Length}",
    null                        => "nothing",
    _                           => "unknown"
};
```

Các viên gạch, ghép được ở khắp nơi:

- **Type pattern** `int n` — kiểm tra + gắn tên.
- **Property pattern** `string { Length: 0 }`, `Point { X: > 0, Y: > 0 }`.
- **Relational** `> 100`, **logical** `and/or/not`.
- **Constant** `null`, giá trị enum, literal.
- **List pattern** (C# 11): `[1, .., var last]` khớp hình dạng chuỗi.

## Tính đầy đủ và phân cấp

Với enum và hệ đóng, compiler chứng minh được bạn phủ mọi trường hợp — thiếu
một trường hợp bạn nhận cảnh báo, không phải bug lúc chạy. Đó là lý do switch
trên hợp `Shape` thắng chuỗi `if/else`: hệ thống kiểu tham gia vào tính đúng
đắn. Thêm `_` quá sớm và bạn *tắt* lớp bảo vệ đó — để nó làm phương án cuối.

```csharp
public enum LoadState { Idle, Loading, Ready, Failed }
public static bool IsBusy(LoadState s) => s switch
{
    LoadState.Loading => true,
    LoadState.Idle or LoadState.Ready or LoadState.Failed => false,
    _ => throw new ArgumentOutOfRangeException(nameof(s))  // phòng tương lai
};
```

## Tuple và deconstruction

Tuple gom các giá trị tạm thời; deconstruction bóc ra bất cứ thứ gì có phương
thức `Deconstruct` (mọi record đều có):

```csharp
(string name, int score) = ("ann", 92);
var (min, max) = (nums.Min(), nums.Max());
foreach (var (key, count) in dict)   // KeyValuePair cũng deconstruct được
    Console.WriteLine($"{key}: {count}");
```

Switch trên tuple cho bảng quyết định đọc như bảng thật:

```csharp
public static string Grade(int score, bool attended) => (score, attended) switch
{
    ( >= 90, true)  => "A+",
    ( >= 90, false) => "A",
    ( >= 80, _)     => "B",
    _               => "C"
};
```

## Kiểm tra hiểu biết

- Vì sao `_ => ...` là con dao hai lưỡi? (Bắt nốt các trường hợp tương lai một cách âm thầm.)
- Property pattern thắng guard clause khi nào? (Khi phân loại, không phải khi hợp lệ hóa.)
- `foreach (var (k, v) in dict)` dựa vào gì? (KeyValuePair.Deconstruct.)
""",
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m1",
    "Checkpoint — Advanced Type System",
    "Combine value/reference semantics, nullability, and pattern matching in one graded unit.",
    20,
    r"""
## The gate

Three functions, one graded unit, no scaffolding: reference identity that is
null-safe, a classification table that orders its checks correctly, and a
range function that treats absence as a first-class contract. Passing this
checkpoint means the type system's *semantics* — not just its syntax — are
yours.

If it fails: re-read which of the three behaviors each test isolates. The
identity test distinguishes `Equals` from `ReferenceEquals`; the
classification test is an ordering exercise; the range test is an
absence-handling exercise.
""",
    "Checkpoint — Hệ thống kiểu nâng cao",
    "Kết hợp ngữ nghĩa giá trị/tham chiếu, nullability, và pattern matching trong một đơn vị chấm.",
    r"""
## Cổng kiểm tra

Ba hàm, một đơn vị chấm, không giàn giáo: identity tham chiếu an toàn null,
bảng phân loại có thứ tự kiểm tra đúng, và hàm dải giá trị coi sự vắng mặt là
hợp đồng hạng nhất. Đỗ cổng này nghĩa là *ngữ nghĩa* của hệ thống kiểu —
không chỉ cú pháp — đã thuộc về bạn.

Nếu trượt: đọc lại mỗi test cô lập hành vi nào. Test identity phân biệt
`Equals` với `ReferenceEquals`; test phân loại là bài tập thứ tự; test range
là bài tập xử lý sự vắng mặt.
""",
    challenge(
    "csi-checkpoint-m1-task",
    "Checkpoint: Type Semantics Under Pressure",
    """Three functions in one graded unit — value/reference, nullability, and patterns together:

```csharp
/* 1. Returns true iff the SAME object (reference equality), false for
      equal-but-distinct boxes; null-safe both sides. */
static bool IsSameInstance(object? a, object? b);
/* 2. Classifies with a switch expression (exact strings):
      null -> "empty"; empty/whitespace -> "blank"; parses as int ->
      "int:<n>"; any other -> "text:<input>" */
static string Classify(string? input);
/* 3. Deconstructs: returns (min, max) of the numbers; empty or null
      sequence -> (0, 0). */
static (int Min, int Max) Range(IEnumerable<int>? numbers);
```""",
    CS_PRELUDE,
    [
        (
            "reference identity",
            r"""
object shared = new object();
Cj.True(Solution.IsSameInstance(shared, shared), "same instance is same");
Cj.False(Solution.IsSameInstance(new object(), new object()), "distinct instances differ");
object boxed = 1000;
Cj.True(Solution.IsSameInstance(boxed, boxed), "boxed int compared with itself");
Cj.False(Solution.IsSameInstance(boxed, 1000), "equal box vs fresh box: NOT same instance");
Cj.False(Solution.IsSameInstance(null, boxed), "null is not an instance");
Cj.False(Solution.IsSameInstance(null, null), "null vs null: nothing to be same as");
""",
            "ReferenceEquals handles the null-null case (it's true for nulls) — the spec wants false, so guard explicitly.",
        ),
        (
            "classification table",
            r"""
Cj.Eq(Solution.Classify(null), "empty", "null input");
Cj.Eq(Solution.Classify(""), "blank", "empty string");
Cj.Eq(Solution.Classify("   "), "blank", "whitespace only");
Cj.Eq(Solution.Classify("-5"), "int:-5", "parses as negative int");
Cj.Eq(Solution.Classify("42"), "int:42", "parses as int");
Cj.Eq(Solution.Classify("4.5"), "text:4.5", "not an int -> text");
Cj.Eq(Solution.Classify("hi"), "text:hi", "plain text");
""",
            "Order matters: null first, then blank, then TryParse, then the text branch — a switch expression on (input) with guards.",
        ),
        (
            "range with absence",
            r"""
var (lo, hi) = Solution.Range(new[] { 3, -1, 7, 4 });
Cj.Eq(lo, -1, "min"); Cj.Eq(hi, 7, "max");
var (z1, z2) = Solution.Range(Array.Empty<int>());
Cj.Eq(z1, 0, "empty min"); Cj.Eq(z2, 0, "empty max");
var (n1, n2) = Solution.Range(null);
Cj.Eq(n1, 0, "null min"); Cj.Eq(n2, 0, "null max");
var (one, one2) = Solution.Range(new[] { 5 });
Cj.Eq(one, 5, "single min==max"); Cj.Eq(one2, 5, "single max==min");
""",
            "Treat null and empty the same way — and single elements make min==max.",
        ),
    ],
    difficulty="intermediate",
),
    vi_challenge(
    "Checkpoint: Ngữ nghĩa kiểu dưới áp lực",
    "Ba hàm trong một đơn vị chấm — giá trị/tham chiếu, nullability, và pattern cùng lúc: identity tham chiếu an toàn null, bảng phân loại string bằng switch expression, và (min, max) qua deconstruction với hợp đồng rỗng/null.",
    [
        ("reference identity", "ReferenceEquals đúng cho null-null, nhưng đề yêu cầu false — phải tự chặn null tường minh."),
        ("classification table", "Thứ tự quan trọng: null trước, blank sau, rồi TryParse, cuối cùng là nhánh text."),
        ("range with absence", "null và rỗng chung hợp đồng; một phần tử thì min==max."),
    ],
),
    solution='public class Solution\n{\n    public static bool IsSameInstance(object? a, object? b)\n    {\n        if (a is null || b is null) return false;\n        return ReferenceEquals(a, b);\n    }\n\n    public static string Classify(string? input) => input switch\n    {\n        null => "empty",\n        var s when string.IsNullOrWhiteSpace(s) => "blank",\n        var s when int.TryParse(s, out int n) => "int:" + n,\n        var s => "text:" + s,\n    };\n\n    public static (int Min, int Max) Range(IEnumerable<int>? numbers)\n    {\n        if (numbers is null) return (0, 0);\n        int min = int.MaxValue, max = int.MinValue;\n        foreach (int n in numbers)\n        {\n            if (n < min) min = n;\n            if (n > max) max = n;\n        }\n        return min == int.MaxValue ? (0, 0) : (min, max);\n    }\n}\n',
    wrong='public class Solution\n{\n    public static bool IsSameInstance(object? a, object? b)\n    {\n        // near-miss: Equals compares by VALUE — equal-but-distinct boxes\n        // wrongly report "same instance"\n        if (a is null || b is null) return false;\n        return a.Equals(b);\n    }\n\n    public static string Classify(string? input) => input switch\n    {\n        // near-miss: blank check before null — null dereferences inside\n        // IsNullOrWhiteSpace is fine, but null is classified "blank" not "empty"\n        var s when string.IsNullOrWhiteSpace(s) => "blank",\n        null => "empty",\n        var s when int.TryParse(s, out int n) => "int:" + n,\n        var s => "text:" + s,\n    };\n\n    public static (int Min, int Max) Range(IEnumerable<int>? numbers)\n    {\n        // near-miss: Min()/Max() throw on empty — and null was "fixed" with !\n        if (numbers is null) return (0, 0);\n        return (numbers.Min(), numbers.Max());\n    }\n}\n',
)

# ---------------------------------------------------------------- practice 1a
P1A_CH = [
    challenge(
        "csi-p1-copy-alias",
        "Copy or Alias?",
        """Implement two small types and a probe — the test asserts what each assignment did:

```csharp
public struct ValuePoint { public int X; }          /* value: copies */
public sealed class RefPoint { public int X; }      /* reference: aliases */

/* increments X and returns the (copied) struct — the caller's copy
   must NOT be affected */
static ValuePoint BumpValue(ValuePoint p);
/* increments X through the reference — the caller's object MUST be
   affected, and the same instance is returned */
static RefPoint   BumpRef(RefPoint p);
```""",
        CS_PRELUDE,
        [
            (
                "value copies",
                r"""
var v = new Solution.ValuePoint { X = 1 };
var bumped = Solution.BumpValue(v);
Cj.Eq(v.X, 1, "caller's struct untouched");
Cj.Eq(bumped.X, 2, "returned copy incremented");
""",
                "Structs: mutate the parameter copy and return it — the caller's copy never moves.",
            ),
            (
                "references alias",
                r"""
var r = new Solution.RefPoint { X = 1 };
var same = Solution.BumpRef(r);
Cj.Eq(r.X, 2, "caller's object mutated through the alias");
Cj.True(ReferenceEquals(r, same), "returns the same object");
""",
                "Classes: mutate the object the parameter references — caller sees it.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "csi-p1-boxing-prediction",
        "Boxing Detective",
        """Implement the probes so the tests confirm the real boxing rules:

```csharp
/* true iff the two objects are the same box (reference equality) */
static bool SameBox(object a, object b);
/* unbox to the EXACT type named by the generic parameter:
   UnboxAs<int>(boxedInt) works; UnboxAs<double>(boxedInt) must
   throw InvalidCastException (let it propagate). */
static T UnboxAs<T>(object boxed) where T : struct;
/* sum WITHOUT boxing per element: takes int[] and returns long */
static long SumNoBox(int[] values);
```""",
        CS_PRELUDE,
        [
            (
                "box identity",
                r"""
object a = 1000, b = 1000;
Cj.False(Solution.SameBox(a, b), "two separate boxes for equal ints");
Cj.True(Solution.SameBox(a, a), "same variable, same box");
object c = a;
Cj.True(Solution.SameBox(a, c), "copy of the reference, same box");
""",
                "Every implicit conversion to object creates a new box — even for equal values.",
            ),
            (
                "exact-type unboxing",
                r"""
object bi = 42;
Cj.Eq(Solution.UnboxAs<int>(bi), 42, "int unboxes as int");
bool threw = false;
try { Solution.UnboxAs<double>(bi); } catch (InvalidCastException) { threw = true; }
Cj.True(threw, "boxed int cannot unbox as double");
object bl = 42L;
Cj.Eq(Solution.UnboxAs<long>(bl), 42L, "long unboxes as long");
""",
                "The unbox instruction demands the exact type — no numeric conversion happens.",
            ),
            (
                "box-free sum",
                r"""
int[] big = new int[10_000];
for (int i = 0; i < big.Length; i++) big[i] = i + 1;
Cj.Eq(Solution.SumNoBox(big), 50_005_000L, "10k values, zero boxes");
Cj.Eq(Solution.SumNoBox(Array.Empty<int>()), 0L, "empty sums to 0");
""",
            "A foreach over int[] never boxes — it's the params/object[] paths that do.",
            ),
        ],
        level="guided",
    ),
    challenge(
        "csi-p1-nullable-fix",
        "Make Null a Contract",
        """Rebuild a fragile API around honest nullability:

```csharp
/* Parses a positive integer; null when input is null, blank, or not a
   positive integer. */
static int? ParsePositive(string? input);
/* First key in the dictionary whose value is > threshold; null when none.
   Dictionary iteration order is insertion order — first match wins. */
static string? FirstAbove(Dictionary<string, int> scores, int threshold);
/* Defaults: name null/blank -> "guest"; else trimmed name. */
static string DisplayName(string? name);
```""",
        CS_PRELUDE,
        [
            (
                "parse contract",
                r"""
Cj.Eq(Solution.ParsePositive("42"), 42, "positive parses");
Cj.Eq(Solution.ParsePositive("-1"), null, "negative is absent");
Cj.Eq(Solution.ParsePositive("0"), null, "zero is not positive");
Cj.Eq(Solution.ParsePositive("x"), null, "garbage is absent");
Cj.Eq(Solution.ParsePositive(null), null, "null input, null output");
Cj.Eq(Solution.ParsePositive("  7 "), 7, "trim tolerantly");
""",
                "int.TryParse + a positivity check + a null/blank guard, expressed as one nullable return.",
            ),
            (
                "first match wins",
                r"""
var scores = new Dictionary<string, int>
{
    ["ann"] = 90, ["bob"] = 95, ["cat"] = 91,
};
Cj.Eq(Solution.FirstAbove(scores, 89), "ann", "first above threshold");
Cj.Eq(Solution.FirstAbove(scores, 90), "bob", "strictly above: 90 not > 90");
Cj.Eq(Solution.FirstAbove(scores, 100), null, "none -> null");
var empty = new Dictionary<string, int>();
Cj.Eq(Solution.FirstAbove(empty, 0), null, "empty -> null");
""",
                "foreach + break on the first hit; null when the loop finishes empty.",
            ),
            (
                "display defaults",
                r"""
Cj.Eq(Solution.DisplayName("  ann "), "ann", "trimmed");
Cj.Eq(Solution.DisplayName(null), "guest", "null guest");
Cj.Eq(Solution.DisplayName("   "), "guest", "blank guest");
Cj.Eq(Solution.DisplayName("bob"), "bob", "plain pass-through");
""",
                "IsNullOrWhiteSpace + Trim + ?? — three tools, one line each.",
            ),
        ],
        level="guided",
    ),
]
P1A_SOL = [
    (
        "csi-p1-copy-alias",
        'public class Solution\n{\n    public struct ValuePoint { public int X; }\n    public sealed class RefPoint { public int X; }\n\n    public static ValuePoint BumpValue(ValuePoint p)\n    {\n        p.X = p.X + 1;\n        return p;\n    }\n\n    public static RefPoint BumpRef(RefPoint p)\n    {\n        p.X = p.X + 1;\n        return p;\n    }\n}\n',
        'public class Solution\n{\n    public struct ValuePoint { public int X; }\n    public sealed class RefPoint { public int X; }\n\n    // near-miss: replaces the parameter with a NEW RefPoint — the caller\'s\n    // object is untouched, so the alias test fails\n    public static ValuePoint BumpValue(ValuePoint p)\n    {\n        p.X = p.X + 1;\n        return p;\n    }\n\n    public static RefPoint BumpRef(RefPoint p)\n    {\n        p = new RefPoint { X = p.X + 1 };\n        return p;\n    }\n}\n',
    ),
    (
        "csi-p1-boxing-prediction",
        'public class Solution\n{\n    public static bool SameBox(object a, object b) => ReferenceEquals(a, b);\n\n    public static T UnboxAs<T>(object boxed) where T : struct\n        => (T)boxed;\n\n    public static long SumNoBox(int[] values)\n    {\n        long total = 0;\n        foreach (int v in values) total += v;\n        return total;\n    }\n}\n',
        'public class Solution\n{\n    public static bool SameBox(object a, object b)\n    {\n        // near-miss: Equals compares boxed VALUES — equal ints in distinct\n        // boxes wrongly count as the "same box"\n        return a.Equals(b);\n    }\n\n    public static T UnboxAs<T>(object boxed) where T : struct\n        => (T)boxed;\n\n    public static long SumNoBox(int[] values)\n    {\n        long total = 0;\n        foreach (object v in values) total += Convert.ToInt64(v);\n        return total;\n    }\n}\n',
    ),
    (
        "csi-p1-nullable-fix",
        'public class Solution\n{\n    public static int? ParsePositive(string? input)\n    {\n        if (string.IsNullOrWhiteSpace(input)) return null;\n        if (!int.TryParse(input.Trim(), out int n)) return null;\n        return n > 0 ? n : null;\n    }\n\n    public static string? FirstAbove(Dictionary<string, int> scores, int threshold)\n    {\n        foreach (var (name, score) in scores)\n        {\n            if (score > threshold) return name;\n        }\n        return null;\n    }\n\n    public static string DisplayName(string? name)\n    {\n        if (string.IsNullOrWhiteSpace(name)) return "guest";\n        return name.Trim();\n    }\n}\n',
        'public class Solution\n{\n    public static int? ParsePositive(string? input)\n    {\n        // near-miss: accepts zero and negatives — the "positive" contract broke\n        if (string.IsNullOrWhiteSpace(input)) return null;\n        if (!int.TryParse(input.Trim(), out int n)) return null;\n        return n;\n    }\n\n    public static string? FirstAbove(Dictionary<string, int> scores, int threshold)\n    {\n        foreach (var (name, score) in scores)\n        {\n            if (score > threshold) return name;\n        }\n        return null;\n    }\n\n    public static string DisplayName(string? name)\n    {\n        if (string.IsNullOrWhiteSpace(name)) return "guest";\n        return name.Trim();\n    }\n}\n',
    ),
]
VI_P1A = {
    "csi-p1-copy-alias": vi_challenge(
        "Sao chép hay tham chiếu?",
        "Hiện thực hai record type và probe — test khẳng định từng phép gán đã làm gì: struct sao chép, class tham chiếu qua alias.",
        [("value copies", "Struct: biến đổi bản sao tham số rồi trả về — bản sao của caller không hề nhúc nhích."),
         ("references alias", "Class: biến đổi đối tượng mà tham số tham chiếu tới — caller nhìn thấy.")],
    ),
    "csi-p1-boxing-prediction": vi_challenge(
        "Thám tử boxing",
        "Hiện thực các probe để test xác nhận luật boxing thật: identity của hộp, unbox đúng-kiểu, và tổng không-box.",
        [("box identity", "Mọi chuyển đổi ngầm sang object tạo hộp mới — kể cả với giá trị bằng nhau."),
         ("exact-type unboxing", "Lệnh unbox đòi đúng kiểu — không có chuyển đổi số nào xảy ra."),
         ("box-free sum", "foreach trên int[] không bao giờ box — các đường params/object[] mới box.")],
    ),
    "csi-p1-nullable-fix": vi_challenge(
        "Biến null thành hợp đồng",
        "Xây lại một API mong manh quanh nullability trung thực: ParsePositive, FirstAbove, DisplayName.",
        [("parse contract", "int.TryParse + kiểm tra dương + guard null/blank, gói trong một nullable return."),
         ("first match wins", "foreach + break ở lần trúng đầu tiên; null khi vòng lặp kết thúc trống."),
         ("display defaults", "IsNullOrWhiteSpace + Trim + ?? — ba công cụ, mỗi dòng một cái.")],
    ),
}
write_practice(
    M, "csi-p1-semantics",
    "Semantics Gym",
    "Value vs reference, boxing identity, and honest nullability until the model in your head matches the runtime.",
    "Phòng gym ngữ nghĩa",
    "Giá trị so với tham chiếu, identity boxing, và nullability trung thực đến khi mô hình trong đầu khớp runtime.",
    after_lesson="type-semantics",
    minutes=26,
    difficulty="intermediate",
    challenges=P1A_CH,
    vi_challenges=VI_P1A,
    solutions=P1A_SOL,
)

# ---------------------------------------------------------------- practice 1b
P1B_CH = [
    challenge(
        "csi-p1-switch-describe",
        "The Classifier Switch",
        """Implement classification with ONE switch expression each — no if chains:

```csharp
/* "neg" (<0), "zero" (0), "small" (1..99), "large" (>=100) */
static string SizeClass(int n);
/* "ok" for "yes"/"no"/"maybe" (any case); "unknown" otherwise */
static string Vote(string? answer);
/* Decision table: (hasTicket, isVip, age) -> zone.
   vip => "gold"; ticket & age>=18 => "standard"; ticket => "minor";
   else "deny". */
static string Zone(bool hasTicket, bool isVip, int age);
```""",
        CS_PRELUDE,
        [
            (
                "numeric bands",
                r"""
Cj.Eq(Solution.SizeClass(-5), "neg", "negative");
Cj.Eq(Solution.SizeClass(0), "zero", "zero");
Cj.Eq(Solution.SizeClass(1), "small", "lower bound");
Cj.Eq(Solution.SizeClass(99), "small", "upper bound");
Cj.Eq(Solution.SizeClass(100), "large", "boundary moves up");
""",
                "Relational patterns: < 0, 0, and ( > 0 and < 100 ) vs >= 100.",
            ),
            (
                "voting",
                r"""
Cj.Eq(Solution.Vote("yes"), "ok", "lowercase");
Cj.Eq(Solution.Vote("YES"), "ok", "uppercase");
Cj.Eq(Solution.Vote("Maybe"), "ok", "mixed");
Cj.Eq(Solution.Vote("nope"), "unknown", "not a vote");
Cj.Eq(Solution.Vote(null), "unknown", "null vote");
Cj.Eq(Solution.Vote(""), "unknown", "empty vote");
""",
                "Constant patterns with a case-insensitive normalize first; null handled by the nullable pattern.",
            ),
            (
                "zone table",
                r"""
Cj.Eq(Solution.Zone(true, true, 30), "gold", "vip wins");
Cj.Eq(Solution.Zone(true, false, 30), "standard", "adult with ticket");
Cj.Eq(Solution.Zone(true, false, 15), "minor", "young with ticket");
Cj.Eq(Solution.Zone(false, true, 30), "gold", "vip needs no ticket");
Cj.Eq(Solution.Zone(false, false, 30), "deny", "no ticket, no vip");
Cj.Eq(Solution.Zone(false, false, 15), "deny", "young, nothing else");
""",
                "Order the rows: vip first (it overrides ticket), then ticket+adult, then ticket, then deny.",
            ),
        ],
        level="imitation",
    ),
    challenge(
        "csi-p1-deconstruct-report",
        "Deconstruct the Ledger",
        """Work with tuples and deconstruction:

```csharp
/* Splits entries into (income, expense) where expense is stored as
   positive numbers to subtract. Returns the pair. */
static (int Income, int Expense) Split(int[] signedEntries);
/* Finds the earliest first-max: value of the first element that equals
   the max, and its zero-based index. Empty -> (0, -1). */
static (int Value, int Index) FirstMax(int[] values);
/* A record with a Deconstruct(int Whole, int Remainder) — division by a
   fixed divisor 10: Whole = n / 10, Remainder = n % 10. */
sealed record Split10(int N)
{
    public void Deconstruct(out int whole, out int remainder);
}
/* The test deconstructs: var (w, r) = new Split10(47); */
```""",
        CS_PRELUDE,
        [
            (
                "signed split",
                r"""
var (inc, exp) = Solution.Split(new[] { 100, -30, 50, -20 });
Cj.Eq(inc, 150, "positives sum");
Cj.Eq(exp, 50, "negatives subtracted from zero");
var (i0, e0) = Solution.Split(Array.Empty<int>());
Cj.Eq(i0, 0, "empty income"); Cj.Eq(e0, 0, "empty expense");
""",
                "Two accumulators: positive adds to income, negative adds its absolute value to expense.",
            ),
            (
                "first max",
                r"""
var (v, i) = Solution.FirstMax(new[] { 1, 9, 9, 3 });
Cj.Eq(v, 9, "max value"); Cj.Eq(i, 1, "FIRST index of the max");
var (v2, i2) = Solution.FirstMax(new[] { 5 });
Cj.Eq(v2, 5, "single"); Cj.Eq(i2, 0, "index 0");
var (v3, i3) = Solution.FirstMax(Array.Empty<int>());
Cj.Eq(v3, 0, "empty value"); Cj.Eq(i3, -1, "empty index");
""",
                "Strictly-greater comparison keeps the FIRST max — >= would drift to the last.",
            ),
            (
                "deconstruct record",
                r"""
var (w, r) = new Solution.Split10(47);
Cj.Eq(w, 4, "whole"); Cj.Eq(r, 7, "remainder");
var (w2, r2) = new Solution.Split10(100);
Cj.Eq(w2, 10, "exact tens"); Cj.Eq(r2, 0, "no remainder");
var (w3, r3) = new Solution.Split10(5);
Cj.Eq(w3, 0, "less than divisor"); Cj.Eq(r3, 5, "all remainder");
""",
                "out parameters in Deconstruct — the record body computes n/10 and n%10.",
            ),
        ],
        level="guided",
    ),
]
P1B_SOL = [
    (
        "csi-p1-switch-describe",
        'public class Solution\n{\n    public static string SizeClass(int n) => n switch\n    {\n        < 0 => "neg",\n        0 => "zero",\n        > 0 and < 100 => "small",\n        _ => "large",\n    };\n\n    public static string Vote(string? answer) => answer?.ToLowerInvariant() switch\n    {\n        "yes" or "no" or "maybe" => "ok",\n        _ => "unknown",\n    };\n\n    public static string Zone(bool hasTicket, bool isVip, int age) =>\n        (hasTicket, isVip, age) switch\n        {\n            (_, true, _) => "gold",\n            (true, false, >= 18) => "standard",\n            (true, false, _) => "minor",\n            _ => "deny",\n        };\n}\n',
        'public class Solution\n{\n    public static string SizeClass(int n) => n switch\n    {\n        < 0 => "neg",\n        0 => "zero",\n        > 0 and <= 100 => "small",   // near-miss: 100 now lands in "small"\n        _ => "large",\n    };\n\n    public static string Vote(string? answer) => answer?.ToLowerInvariant() switch\n    {\n        "yes" or "no" or "maybe" => "ok",\n        _ => "unknown",\n    };\n\n    public static string Zone(bool hasTicket, bool isVip, int age) =>\n        (hasTicket, isVip, age) switch\n        {\n            // near-miss: ticket rows before vip — a vip WITHOUT a ticket\n            // wrongly lands in "minor"/"deny"\n            (true, _, >= 18) => "standard",\n            (true, _, _) => "minor",\n            (_, true, _) => "gold",\n            _ => "deny",\n        };\n}\n',
    ),
    (
        "csi-p1-deconstruct-report",
        'public class Solution\n{\n    public static (int Income, int Expense) Split(int[] signedEntries)\n    {\n        int income = 0, expense = 0;\n        foreach (int n in signedEntries)\n        {\n            if (n >= 0) income += n;\n            else expense += -n;\n        }\n        return (income, expense);\n    }\n\n    public static (int Value, int Index) FirstMax(int[] values)\n    {\n        if (values.Length == 0) return (0, -1);\n        int best = values[0], bestIndex = 0;\n        for (int i = 1; i < values.Length; i++)\n        {\n            if (values[i] > best)\n            {\n                best = values[i];\n                bestIndex = i;\n            }\n        }\n        return (best, bestIndex);\n    }\n\n    public sealed record Split10(int N)\n    {\n        public void Deconstruct(out int whole, out int remainder)\n        {\n            whole = N / 10;\n            remainder = N % 10;\n        }\n    }\n}\n',
        'public class Solution\n{\n    public static (int Income, int Expense) Split(int[] signedEntries)\n    {\n        int income = 0, expense = 0;\n        foreach (int n in signedEntries)\n        {\n            // near-miss: 0 counted as expense — zeros are neither income\n            // nor debt, and the empty-like input now reports expense 0 anyway,\n            // but mixed inputs with zeros corrupt the totals\n            if (n > 0) income += n;\n            else expense += -n;\n        }\n        return (income, expense);\n    }\n\n    public static (int Value, int Index) FirstMax(int[] values)\n    {\n        if (values.Length == 0) return (0, -1);\n        int best = values[0], bestIndex = 0;\n        for (int i = 1; i < values.Length; i++)\n        {\n            // near-miss: >= drifts the index to the LAST max\n            if (values[i] >= best)\n            {\n                best = values[i];\n                bestIndex = i;\n            }\n        }\n        return (best, bestIndex);\n    }\n\n    public sealed record Split10(int N)\n    {\n        public void Deconstruct(out int whole, out int remainder)\n        {\n            whole = N / 10;\n            remainder = N % 10;\n        }\n    }\n}\n',
    ),
]
VI_P1B = {
    "csi-p1-switch-describe": vi_challenge(
        "Switch phân loại",
        "Hiện thực phân loại bằng MỘT switch expression mỗi hàm — không chuỗi if: SizeClass, Vote, Zone.",
        [("numeric bands", "Relational pattern: < 0, 0, rồi ( > 0 and < 100 ) so với >= 100."),
         ("voting", "Constant pattern với chuẩn hóa không phân biệt hoa-thường trước; null xử lý bằng nullable pattern."),
         ("zone table", "Sắp hàng: vip trước (ghi đè ticket), rồi ticket+adult, rồi ticket, cuối là deny.")],
    ),
    "csi-p1-deconstruct-report": vi_challenge(
        "Deconstruct sổ cái",
        "Làm việc với tuple và deconstruction: tách thu/chi, first-max đúng chỉ số đầu, record tự viết Deconstruct.",
        [("signed split", "Hai bộ tích lũy: dương cộng vào income, âm cộng trị tuyệt đối vào expense."),
         ("first max", "So sánh strictly-greater giữ max ĐẦU TIÊN — >= sẽ trôi về max cuối."),
         ("deconstruct record", "Tham số out trong Deconstruct — thân record tính n/10 và n%10.")],
    ),
}
write_practice(
    M, "csi-p1-patterns",
    "Pattern Gym",
    "Switch expressions as design, tuples and deconstruction as data flow.",
    "Phòng gym pattern",
    "Switch expression như thiết kế, tuple và deconstruction như dòng dữ liệu.",
    after_lesson="pattern-matching",
    minutes=24,
    difficulty="intermediate",
    challenges=P1B_CH,
    vi_challenges=VI_P1B,
    solutions=P1B_SOL,
)
print("module 1 authored")
