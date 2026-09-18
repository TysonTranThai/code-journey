"""Module 5 — Reflection, attributes, and metaprogramming (csa-m5)."""
from __future__ import annotations

import csa


def build() -> None:
    MID = csa.register_module(
        "csa-reflection-attributes",
        "Reflection and Attributes",
        "Type discovery, dynamic invocation, metadata caches, attribute-driven behavior — and the security and performance bill.",
    )

    csa.register_lesson(
        MID, "csa-m5-discovery", "Type, MemberInfo, and discovery",
        "Walking assemblies and types at runtime: what the metadata tables really cost to read.",
        14, "advanced", _m5_discovery, _m5_discovery_vi,
    )
    csa.register_lesson(
        MID, "csa-m5-invocation", "Dynamic invocation and its bill",
        "MethodInfo.Invoke vs cached delegates vs compiled expressions — measured, not folklore.",
        15, "advanced", _m5_invocation, _m5_invocation_vi,
    )
    csa.register_lesson(
        MID, "csa-m5-attributes", "Attributes as executable metadata",
        "Custom attributes, targets, inheritance, retrieval, and building attribute-driven behavior.",
        15, "advanced", _m5_attributes, _m5_attributes_vi,
    )
    csa.register_lesson(
        MID, "csa-m5-security", "Reflection and security",
        "Why reflection defeats static analysis, what it leaks, and the discipline that keeps it safe.",
        12, "advanced", _m5_security, _m5_security_vi,
    )
    csa.register_lesson(
        MID, "csa-checkpoint-m5", "Checkpoint: reflection",
        "Synthesis: a caching plugin loader with attribute-driven configuration.",
        12, "advanced", _m5_checkpoint, _m5_checkpoint_vi,
    )
    csa.register_challenge(
        "csa-checkpoint-m5-task", MID,
        title="Reflection checkpoint",
        prompt=(
            "Implement `static List<string> PluginNames(Assembly assembly)`: find all non-abstract classes in the "
            "assembly that implement interface `IPlugin` (defined below), call their parameterless constructor, "
            "read their `Name` property, and return the names sorted alphabetically. Cache nothing — correctness "
            "first. Define `public interface IPlugin { string Name { get; } }` in your Solution file."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "discovery",
                "code": (
                    "// The test assembly is the compiled solution itself; the harness defines three plugin classes.\n"
                    "var names = Solution.PluginNames(typeof(Solution).Assembly);\n"
                    'Cj.True(names.Contains("alpha"), "alpha found");\n'
                    'Cj.True(names.Contains("beta"), "beta found");\n'
                    'Cj.True(names.SequenceEqual(names.OrderBy(n => n)), "sorted");'
                ),
                "hint": "assembly.GetTypes(), filter typeof(IPlugin).IsAssignableFrom(t) && !t.IsAbstract, then Activator.CreateInstance.",
            },
        ],
        reference=(
            "public interface IPlugin { string Name { get; } }\n\n"
            "public class AlphaPlugin : IPlugin { public string Name => \"alpha\"; }\n\n"
            "public class BetaPlugin : IPlugin { public string Name => \"beta\"; }\n\n"
            "public class Solution\n{\n"
            "    public static List<string> PluginNames(Assembly assembly)\n    {\n"
            "        var r = new List<string>();\n"
            "        foreach (var t in assembly.GetTypes())\n"
            "        {\n"
            "            if (t.IsAbstract || !typeof(IPlugin).IsAssignableFrom(t)) continue;\n"
            "            var instance = (IPlugin)Activator.CreateInstance(t)!;\n"
            "            r.Add(instance.Name);\n"
            "        }\n"
            "        r.Sort();\n"
            "        return r;\n"
            "    }\n}"
        ),
        wrong=(
            "public interface IPlugin { string Name { get; } }\n\n"
            "public class AlphaPlugin : IPlugin { public string Name => \"alpha\"; }\n\n"
            "public class BetaPlugin : IPlugin { public string Name => \"beta\"; }\n\n"
            "public class Solution\n{\n"
            "    public static List<string> PluginNames(Assembly assembly)\n    {\n"
            "        var r = new List<string>();\n"
            "        foreach (var t in assembly.GetTypes())\n"
            "        {\n"
            "            if (!typeof(IPlugin).IsAssignableFrom(t)) continue;   // includes abstract\n"
            "            var instance = (IPlugin)Activator.CreateInstance(t)!;\n"
            "            r.Add(instance.Name);\n"
            "        }\n"
            "        return r;                                                 // unsorted\n"
            "    }\n}"
        ),
        checkpoint=True,
    )
    csa.register_practice(
        MID, "csa-p5-reflection", "Reflection drills",
        "Discovery, cached invocation, attribute-driven validation, and reflection pitfalls.",
        45, "advanced", "csa-m5-invocation",
        ["csa-p5-cached-invoke", "csa-p5-attr-validation", "csa-p5-member-scan"],
    )
    csa.register_challenge(
        "csa-p5-cached-invoke", MID,
        title='Cache the invoke',
        prompt=(
            'Implement `static Func<object?, object?> BuildGetter(Type type, string propertyName)` that returns a DELEGATE reading the given instance property via reflection — and the delegate must be CACHED: two calls with the same (type, name) return the SAME delegate instance, and invoking the cached delegate performs the PropertyInfo work already captured, not a fresh resolve. Also implement `static object? Read(object target, string prop) => BuildGetter(target.GetType(), prop)(target);`.'
        ),
        difficulty='advanced',
        tests=[
            {
                "name": 'cached-and-works',
                "code": (
                    'var g1 = Solution.BuildGetter(typeof(Person), "Age");\nvar g2 = Solution.BuildGetter(typeof(Person), "Age");\nCj.True(ReferenceEquals(g1, g2), "same (type,name) must return the SAME delegate instance");\nvar p = new Person { Name = "Ada", Age = 36 };\nCj.Eq((int?)g1(p), 36, "cached getter works");\nCj.Eq((string?)Solution.Read(p, "Name"), "Ada", "Read convenience");'
                ),
                "hint": 'Cache delegates in a static ConcurrentDictionary<(Type, string), Func<object?, object?>>; capture the PropertyInfo inside the factory.',
            },
            {
                "name": 'allocation-profile',
                "code": (
                    'var p = new Person { Name = "x", Age = 1 };\nvar getter = Solution.BuildGetter(typeof(Person), "Age");\nfor (int i = 0; i < 200; i++) getter(p);   // warm the reflection caches\nlong b0 = GC.GetAllocatedBytesForCurrentThread();\nfor (int i = 0; i < 50; i++) getter(p);\nlong b1 = GC.GetAllocatedBytesForCurrentThread();\n// Calibrated on this runtime: one cached GetValue call on an int prop costs\n// ~24 B (boxing + args array) - under 50*32 total. A closure that re-resolves\n// GetProperty on every invoke exceeds 50*200.\nCj.True(b1 - b0 < 50 * 32, $"per-call overhead too high: {b1 - b0}");'
                ),
                "hint": 'Do the GetProperty work ONCE inside the cached factory; the returned delegate must not resolve per invoke.',
            },
        ],
        reference=(
            'using System.Collections.Concurrent;\n\npublic class Person { public string Name { get; set; } = ""; public int Age { get; set; } }\n\npublic class Solution\n{\n    static readonly ConcurrentDictionary<(Type, string), Func<object?, object?>> Cache = new();\n\n    public static Func<object?, object?> BuildGetter(Type type, string propertyName)\n        => Cache.GetOrAdd((type, propertyName), static key =>\n        {\n            var prop = key.Item1.GetProperty(key.Item2)\n                ?? throw new ArgumentException($"no property {key.Item2}");\n            return target => prop.GetValue(target);\n        });\n\n    public static object? Read(object target, string prop) =>\n        BuildGetter(target.GetType(), prop)(target);\n}'
        ),
        wrong=(
            'public class Person { public string Name { get; set; } = ""; public int Age { get; set; } }\n\npublic class Solution\n{\n    public static Func<object?, object?> BuildGetter(Type type, string propertyName)\n        => target =>\n        {\n            var prop = type.GetProperty(propertyName)!;   // WRONG: re-resolves on EVERY invoke\n            return prop.GetValue(target);\n        };\n\n    public static object? Read(object target, string prop) =>\n        BuildGetter(target.GetType(), prop)(target);\n}'
        ),
        level='guided',
    )
    csa.register_challenge(
        "csa-p5-attr-validation", MID,
        title="Attribute-driven validation",
        prompt=(
            "Define `attribute RangeAttribute : Attribute` with `int Min; int Max;` (usage: properties). Implement "
            "`static List<string> Validate(object obj)`: for each instance property with a RangeAttribute whose value "
            "is an int outside [Min,Max], add \"Name\" of the property to the result. Return failures in declaration "
            "order. Classes to support: `Account { [Range(1,120)] public int Age; [Range(0,100)] public int Score; }` "
            "(fields, not properties — support both fields and properties)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "validation",
                "code": (
                    "var bad = new Account { Age = 150, Score = 99 };\n"
                    "var r = Solution.Validate(bad);\n"
                    'Cj.Eq(r.Count, 1, "one failure");\n'
                    'Cj.Eq(r[0], "Age", "Age out of range");\n'
                    "var ok = new Account { Age = 30, Score = 50 };\n"
                    'Cj.Eq(Solution.Validate(ok).Count, 0, "clean object");\n'
                    "var badProp = new Dto { Level = 500 };\n"
                    "var r2 = Solution.Validate(badProp);\n"
                    'Cj.Eq(r2.Count, 1, "property members validated too");\n'
                    'Cj.Eq(r2[0], "Level", "property name reported");'
                ),
                "hint": "type.GetMembers(BindingFlags.Public | BindingFlags.Instance); check MemberInfo.GetCustomAttribute<RangeAttribute>() — handle FieldInfo and PropertyInfo.",
            },
        ],
        reference=(
            "[AttributeUsage(AttributeTargets.Property | AttributeTargets.Field)]\n"
            "public class RangeAttribute : Attribute\n{\n"
            "    public int Min { get; }\n"
            "    public int Max { get; }\n"
            "    public RangeAttribute(int min, int max) { Min = min; Max = max; }\n}\n\n"
            "public class Account\n{\n"
            "    [Range(1, 120)] public int Age;\n"
            "    [Range(0, 100)] public int Score;\n}\n\n"
            "public class Dto\n{\n"
            "    [Range(0, 100)] public int Level { get; set; }\n}\n\n"
            "public class Solution\n{\n"
            "    public static List<string> Validate(object obj)\n    {\n"
            "        var r = new List<string>();\n"
            "        var t = obj.GetType();\n"
            "        foreach (var f in t.GetFields(BindingFlags.Public | BindingFlags.Instance))\n"
            "            Check(r, f.Name, f.GetCustomAttribute<RangeAttribute>(), (int)f.GetValue(obj)!);\n"
            "        foreach (var p in t.GetProperties(BindingFlags.Public | BindingFlags.Instance))\n"
            "            Check(r, p.Name, p.GetCustomAttribute<RangeAttribute>(), (int)p.GetValue(obj)!);\n"
            "        return r;\n"
            "    }\n\n"
            "    private static void Check(List<string> r, string name, RangeAttribute? a, int v)\n"
            "    { if (a is not null && (v < a.Min || v > a.Max)) r.Add(name); }\n}"
        ),
        wrong=(
            "[AttributeUsage(AttributeTargets.Property | AttributeTargets.Field)]\n"
            "public class RangeAttribute : Attribute\n{\n"
            "    public int Min { get; }\n"
            "    public int Max { get; }\n"
            "    public RangeAttribute(int min, int max) { Min = min; Max = max; }\n}\n\n"
            "public class Account\n{\n"
            "    [Range(1, 120)] public int Age;\n"
            "    [Range(0, 100)] public int Score;\n}\n\n"
            "public class Dto\n{\n"
            "    [Range(0, 100)] public int Level { get; set; }\n}\n\n"
            "public class Solution\n{\n"
            "    public static List<string> Validate(object obj)\n    {\n"
            "        var r = new List<string>();\n"
            "        var t = obj.GetType();\n"
            "        foreach (var f in t.GetFields(BindingFlags.Public | BindingFlags.Instance))\n"
            "            Check(r, f.Name, f.GetCustomAttribute<RangeAttribute>(), (int)f.GetValue(obj)!);\n"
            "        return r;                     // WRONG: skips properties\n"
            "    }\n\n"
            "    private static void Check(List<string> r, string name, RangeAttribute? a, int v)\n"
            "    { if (a is not null && (v < a.Min || v > a.Max)) r.Add(name); }\n}"
        ),
        level="independent",
    )
    csa.register_challenge(
        "csa-p5-member-scan", MID,
        title="Assembly scan with flags",
        prompt=(
            "Implement `static List<string> StaticStringMembers(Type type)`: return the names of all public static "
            "fields AND properties of type string, sorted. Also implement `static int CountMethods(Type type, string "
            "namePrefix)` counting public instance methods whose name starts with the prefix (exclude property "
            "accessors and constructors)."
        ),
        difficulty="advanced",
        tests=[
            {
                "name": "scan",
                "code": (
                    "var names = Solution.StaticStringMembers(typeof(Library));\n"
                    'Cj.True(names.Contains("Version"), "static string field");\n'
                    'Cj.True(names.Contains("Publisher"), "static string property");\n'
                    'Cj.False(names.Contains("Count"), "int member excluded");\n'
                    'Cj.Eq(Solution.CountMethods(typeof(Worker), "Run"), 2, "Run and RunAsync");'
                ),
                "hint": "GetFields/GetProperties with BindingFlags.Public | BindingFlags.Static; for methods use BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly.",
            },
        ],
        reference=(
            "public class Library\n{\n"
            "    public static string Version = \"1.0\";\n"
            "    public static int Count;\n"
            "    public static string Publisher => \"CJ\";\n}\n\n"
            "public class Worker\n{\n"
            "    public void Run() { }\n"
            "    public Task RunAsync() => Task.CompletedTask;\n"
            "    private void RunInternal() { }\n}\n\n"
            "public class Solution\n{\n"
            "    public static List<string> StaticStringMembers(Type type)\n    {\n"
            "        var r = new List<string>();\n"
            "        const BindingFlags F = BindingFlags.Public | BindingFlags.Static;\n"
            "        foreach (var f in type.GetFields(F)) if (f.FieldType == typeof(string)) r.Add(f.Name);\n"
            "        foreach (var p in type.GetProperties(F)) if (p.PropertyType == typeof(string)) r.Add(p.Name);\n"
            "        r.Sort();\n"
            "        return r;\n"
            "    }\n\n"
            "    public static int CountMethods(Type type, string namePrefix)\n    {\n"
            "        const BindingFlags F = BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly;\n"
            "        int n = 0;\n"
            "        foreach (var m in type.GetMethods(F))\n"
            "            if (m.Name.StartsWith(namePrefix, StringComparison.Ordinal)) n++;\n"
            "        return n;\n"
            "    }\n}"
        ),
        wrong=(
            "public class Library\n{\n"
            "    public static string Version = \"1.0\";\n"
            "    public static int Count;\n"
            "    public static string Publisher => \"CJ\";\n}\n\n"
            "public class Worker\n{\n"
            "    public void Run() { }\n"
            "    public Task RunAsync() => Task.CompletedTask;\n"
            "    private void RunInternal() { }\n}\n\n"
            "public class Solution\n{\n"
            "    public static List<string> StaticStringMembers(Type type)\n    {\n"
            "        var r = new List<string>();\n"
            "        const BindingFlags F = BindingFlags.Public | BindingFlags.Static;\n"
            "        foreach (var f in type.GetFields(F)) if (f.FieldType == typeof(string)) r.Add(f.Name);\n"
            "        foreach (var p in type.GetProperties(F)) if (p.PropertyType == typeof(string)) r.Add(p.Name);\n"
            "        return r;                     // WRONG: unsorted\n"
            "    }\n\n"
            "    public static int CountMethods(Type type, string namePrefix)\n    {\n"
            "        const BindingFlags F = BindingFlags.Public | BindingFlags.Static | BindingFlags.DeclaredOnly;\n"
            "        int n = 0;\n"
            "        foreach (var m in type.GetMethods(F))\n"
            "            if (m.Name.StartsWith(namePrefix, StringComparison.Ordinal)) n++;\n"
            "        return n;                     // WRONG: static instead of instance\n"
            "    }\n}"
        ),
        level="imitation",
    )


# ── Lesson bodies ───────────────────────────────────────────────────────────

_m5_discovery = r"""## Type, MemberInfo, and discovery

Reflection is programming against **metadata**: the tables the compiler
wrote into the assembly. `typeof(T)`, `obj.GetType()`, and
`assembly.GetTypes()` hand you `Type` objects; from there,
`GetProperties`, `GetMethods`, `GetFields`, `GetConstructors` walk the
member tables.

```csharp
var t = typeof(Order);
foreach (var p in t.GetProperties(BindingFlags.Public | BindingFlags.Instance))
    Console.WriteLine($"{p.Name}: {p.PropertyType.Name}");
```

The cost model (measured repeatedly across .NET versions): first-time
metadata resolution populates caches — `GetProperty`/`GetMethod` are the
expensive part, not `GetValue` on an already-resolved member. Consequences:

- **Resolve once.** Store the `MethodInfo`/`PropertyInfo` in a static
  `ConcurrentDictionary` keyed by `(Type, MemberName)` and reuse.
- **`BindingFlags` are a performance control**, not decoration: fewer
  candidates = less work.
- `assembly.GetTypes()` can THROW (`ReflectionTypeLoadException`) when
  dependencies are missing — in plugin code, use `GetExportedTypes` or
  handle the loader exception's `Types` array, which contains nulls.

Generics interact with discovery in a way that surprises people:
`typeof(List<>)` is an **open** generic type (no type arguments); you close
it with `MakeGenericType(typeof(int))`. Attribute lookup on open generics
reads the generic type definition's attributes, not the closed one's.
"""

_m5_discovery_vi = r"""## Type, MemberInfo, và discovery

Reflection là lập trình trên **metadata**: các bảng mà compiler ghi vào
assembly. `typeof(T)`, `obj.GetType()`, và `assembly.GetTypes()` đưa cho
bạn object `Type`; từ đó, `GetProperties`, `GetMethods`, `GetFields`,
`GetConstructors` đi qua các bảng member.

```csharp
var t = typeof(Order);
foreach (var p in t.GetProperties(BindingFlags.Public | BindingFlags.Instance))
    Console.WriteLine($"{p.Name}: {p.PropertyType.Name}");
```

Mô hình chi phí (đã đo lặp lại qua các phiên bản .NET): lần đầu giải quyết
metadata sẽ đổ cache — `GetProperty`/`GetMethod` là phần đắt, không phải
`GetValue` trên member đã resolve. Hệ quả:

- **Resolve một lần.** Lưu `MethodInfo`/`PropertyInfo` trong
  `ConcurrentDictionary` tĩnh có key `(Type, MemberName)` và tái sử dụng.
- **`BindingFlags` là bộ điều khiển hiệu năng**, không phải trang trí: ít
  ứng viên = ít việc hơn.
- `assembly.GetTypes()` có thể THROW (`ReflectionTypeLoadException`) khi
  thiếu dependency — trong code plugin, dùng `GetExportedTypes` hoặc xử lý
  mảng `Types` trong exception của loader, mảng chứa các null.

Generics tương tác với discovery theo cách gây bất ngờ: `typeof(List<>)` là
generic type **mở** (chưa có tham số kiểu); bạn đóng nó bằng
`MakeGenericType(typeof(int))`. Tra attribute trên open generic đọc attribute
của định nghĩa generic, không phải của bản đóng.
"""

_m5_invocation = r"""## Dynamic invocation and its bill

Three ways to call a method you discovered at runtime, in ascending
setup cost and descending per-call cost:

1. `methodInfo.Invoke(obj, args)` — slowest per call: argument boxing,
   array allocation, security/registrar checks.
2. Cached delegate: `(Func<Order, decimal>)methodInfo.CreateDelegate(...)` —
   build once, then near-direct call speed.
3. Compiled expression: `Expression.Lambda<Func<...>>(...).Compile()` —
   most setup, fastest body; can also inline field access.

```csharp
// Resolve once:
static readonly ConcurrentDictionary<(Type, string), Func<object, object?>> Getters = new();

static object? Get(object obj, string name) => Getters.GetOrAdd(
    (obj.GetType(), name),
    static key =>
    {
        var p = key.Item1.GetProperty(key.Item2)!;
        return target => p.GetValue(target);   // captures resolved PropertyInfo
    });
```

Numbers to internalize (order-of-magnitude, machine-dependent — always
measure your own): direct call 1x; cached delegate ~2–5x; compiled
expression ~2–3x; raw `Invoke` ~30–100x. The jump from 1 to 30 is the
reason every serious serializer (System.Text.Json, EF materializers)
caches or code-gens instead of reflecting per call.

`CreateDelegate` has one trap: it validates the delegate signature against
the method at creation — a mismatch throws immediately (good), while a
cached-wrong delegate throws on every call (bad). Prefer failing during
startup: build all delegates in a warm-up phase, not lazily on first
request.
"""

_m5_invocation_vi = r"""## Dynamic invocation và hóa đơn của nó

Ba cách gọi một phương thức phát hiện lúc chạy, theo thứ tự chi phí thiết
lập tăng dần và chi phí mỗi lần gọi giảm dần:

1. `methodInfo.Invoke(obj, args)` — chậm nhất mỗi lần gọi: boxing tham số,
   cấp phát mảng, kiểm tra security/registrar.
2. Delegate được cache: `(Func<Order, decimal>)methodInfo.CreateDelegate(...)`
   — dựng một lần, sau đó gần tốc độ gọi trực tiếp.
3. Compiled expression: `Expression.Lambda<Func<...>>(...).Compile()` —
   thiết lập nhiều nhất, thân chạy nhanh nhất; còn inline được cả truy cập
   field.

```csharp
// Resolve một lần:
static readonly ConcurrentDictionary<(Type, string), Func<object, object?>> Getters = new();

static object? Get(object obj, string name) => Getters.GetOrAdd(
    (obj.GetType(), name),
    static key =>
    {
        var p = key.Item1.GetProperty(key.Item2)!;
        return target => p.GetValue(target);   // bắt PropertyInfo đã resolve
    });
```

Con số cần thuộc (bậc độ lớn, tùy máy — luôn tự đo): gọi trực tiếp 1x;
delegate cache ~2–5x; compiled expression ~2–3x; `Invoke` thô ~30–100x.
Khoảng cách từ 1 đến 30 là lý do mọi serializer nghiêm túc (System.Text.Json,
EF materializer) cache hoặc code-gen thay vì reflect mỗi lần gọi.

`CreateDelegate` có một cái bẫy: nó xác thực chữ ký delegate với phương thức
NGAY LÚC TẠO — không khớp thì throw ngay (tốt), còn delegate sai được cache
thì throw mỗi lần gọi (tệ). Hãy ưu tiên fail lúc startup: dựng toàn bộ
delegate trong một pha warm-up, không phải lười theo yêu cầu đầu tiên.
"""

_m5_attributes = r"""## Attributes as executable metadata

An attribute is a tiny object serialized into the assembly's metadata.
It does nothing by itself — it is *data about code* that you (or a
framework) read and act on:

```csharp
[AttributeUsage(AttributeTargets.Method, AllowMultiple = false, Inherited = true)]
sealed class RetryAttribute : Attribute
{
    public int Times { get; }
    public RetryAttribute(int times) => Times = times;
}

class Job
{
    [Retry(3)]
    public void Run() { }
}

// Reading it back:
var attr = typeof(Job).GetMethod("Run")!.GetCustomAttribute<RetryAttribute>();
// attr.Times == 3
```

The three properties that decide behavior:

- **AttributeUsage**: where it may appear. Enforce this — an attribute on
  the wrong target is a design smell the compiler should have caught.
- **AllowMultiple**: stacking `[Retry(3)][Retry(5)]` is legal or a compile
  error.
- **Inherited**: do derived classes see the base class's attributes?

Attribute *arguments* are limited to compile-time constants, `Type`
objects, and arrays of those — that constraint is what makes attributes
safe to serialize into metadata. Everything dynamic (config values, live
services) belongs in the code that *reacts* to the attribute, not in the
attribute itself.

Design boundary that keeps systems sane: attributes declare **intent**
("this needs retries", "this is a job"), a single engine interprets them
once at startup, and hot paths never re-read attributes. Re-reading
attributes per request is the classic reflection-performance bug — and a
sign the framework boundary leaked.
"""

_m5_attributes_vi = r"""## Attribute như metadata khả thi

Attribute là một object nhỏ được serialize vào metadata của assembly. Bản
thân nó không làm gì cả — nó là *dữ liệu về mã* mà bạn (hoặc framework)
đọc và hành động:

```csharp
[AttributeUsage(AttributeTargets.Method, AllowMultiple = false, Inherited = true)]
sealed class RetryAttribute : Attribute
{
    public int Times { get; }
    public RetryAttribute(int times) => Times = times;
}

class Job
{
    [Retry(3)]
    public void Run() { }
}

// Đọc lại:
var attr = typeof(Job).GetMethod("Run")!.GetCustomAttribute<RetryAttribute>();
// attr.Times == 3
```

Ba thuộc tính quyết định hành vi:

- **AttributeUsage**: nơi nó được phép xuất hiện. Hãy ép điều này —
  attribute gắn sai đích là design smell đáng lẽ compiler phải bắt.
- **AllowMultiple**: việc chồng `[Retry(3)][Retry(5)]` là hợp lệ hay lỗi
  biên dịch.
- **Inherited**: lớp dẫn xuất có thấy attribute của lớp cơ sở không?

Tham số attribute bị giới hạn ở hằng số lúc biên dịch, object `Type`, và
mảng của những thứ đó — ràng buộc này khiến attribute an toàn khi serialize
vào metadata. Mọi thứ động (giá trị cấu hình, service sống) thuộc về code
*phản ứng* với attribute, không nằm trong attribute.

Ranh giới thiết kế giữ hệ thống lành mạnh: attribute tuyên bố **ý định**
("cái này cần retry", "cái này là job"), một engine duy nhất diễn giải chúng
một lần lúc startup, và đường nóng không bao giờ đọc lại attribute. Đọc
attribute mỗi request là bug hiệu năng reflection kinh điển — và là dấu hiệu
ranh giới framework đã bị rò rỉ.
"""

_m5_security = r"""## Reflection and security

Reflection is power with a bill. Three duties in modern .NET:

**1. It bypasses static guarantees.** A `private` member is a compile-time
promise; `BindingFlags.NonPublic` breaks it silently. Style says: never
reflect into `private` of types you don't own — you are coupling to
implementation details that any refactor will break, and (on trimmed or
AOT-compiled apps, Module 19) members unused by "real" code may not exist
at runtime at all.

**2. It is a deserialization hazard.** `Activator.CreateInstance(type)`
where `type` comes from user input is arbitrary construction — the
class-history of .NET vulnerabilities includes exactly this. Whitelist:
map trusted names to types in your own assembly; never `Type.GetType`
user strings without validation.

**3. Trim/AOT compatibility is now a correctness issue.** Every
`GetProperty("Name")` with a literal is invisible to the IL trimmer unless
you annotate `[DynamicallyAccessedMembers]` or use `nameof`. In this
course's sandbox (full framework, no trimming) reflection runs fine — but
code you ship to NativeAOT will not, so keep reflection at the edges of
your design and prefer source generation (Module 8) for the hot middle.
"""

_m5_security_vi = r"""## Reflection và bảo mật

Reflection là quyền lực kèm hóa đơn. Ba nghĩa vụ trong .NET hiện đại:

**1. Nó vượt qua cam kết tĩnh.** Member `private` là lời hứa lúc biên dịch;
`BindingFlags.NonPublic` phá vỡ nó một cách âm thầm. Phong cách: không bao
giờ reflect vào `private` của kiểu bạn không sở hữu — bạn đang ghép chặt
vào chi tiết triển khai mà bất kỳ lần refactor nào cũng phá, và (trên app
đã trim hoặc AOT, Module 19) member không được code "thật" dùng có thể
không tồn tại lúc chạy.

**2. Nó là mối nguy deserialization.** `Activator.CreateInstance(type)`
trong đó `type` đến từ input người dùng là việc tạo object tùy ý — lịch sử
lỗ hổng của .NET có đúng chuyện này. Whitelist: ánh xạ tên tin cậy sang kiểu
trong assembly của bạn; không bao giờ `Type.GetType` chuỗi của người dùng
mà không xác thực.

**3. Tương thích trim/AOT giờ là vấn đề đúng-sai.** Mọi
`GetProperty("Name")` với literal là vô hình với IL trimmer trừ khi bạn
gắn `[DynamicallyAccessedMembers]` hoặc dùng `nameof`. Trong sandbox của
khóa này (framework đầy đủ, không trim) reflection chạy ổn — nhưng code
bạn ship lên NativeAOT sẽ không, nên giữ reflection ở rìa thiết kế và ưu
tiên source generation (Module 8) cho phần nóng ở giữa.
"""

_m5_checkpoint = r"""## Checkpoint: reflection

The graded task is a compressed plugin loader: discover implementers,
instantiate, read a property — the exact skeleton every DI container and
test runner uses. Passing it means you can walk metadata without fear.
The practice set adds the two disciplines production demands: cached
invocation and attribute-driven engines.
"""

_m5_checkpoint_vi = r"""## Checkpoint: reflection

Bài được chấm là một plugin loader nén: khám phá implementer, khởi tạo, đọc
property — đúng khung xương mà mọi DI container và test runner dùng. Pass
nghĩa là bạn đi qua metadata mà không sợ hãi. Practice set bổ sung hai kỷ
luật production đòi hỏi: invocation được cache và engine điều khiển bằng
attribute.
"""
