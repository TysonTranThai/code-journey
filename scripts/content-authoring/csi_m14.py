#!/usr/bin/env python3
"""C# — Intermediate — Module 14: csi-json.

System.Text.Json: round-tripping, options (naming policy, case sensitivity),
custom converters (intro), missing/null handling, malformed-input defense,
and import/export transforms.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-json"

STJ_PRELUDE = CS_PRELUDE + "using System.Text.Json;\n"

write_module(
    M,
    "JSON & Serialization",
    "System.Text.Json end to end: options, converters, malformed input, and the round-trip fidelity mindset.",
    "JSON & Serialization",
    "System.Text.Json từ đầu đến cuối: options, converters, dữ liệu lỗi, và tư duy trung thực vòng lập.",
    ["stj-options", "converters-and-robustness", "csi-checkpoint-m14"],
    ["csi-p14-json"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "stj-options",
    "Serializing, Deserializing, and Options",
    "JsonSerializer with naming policies, case sensitivity, and round-trip fidelity.",
    17,
    r"""
## The two workhorses

```csharp
string json = JsonSerializer.Serialize(order);
var back = JsonSerializer.Deserialize<Order>(json);
```

Serialize turns objects into JSON text; Deserialize parses text into a
typed object. Deserialization REQUIRES the target type — that's how JSON
becomes checked C# instead of string soup.

## Naming policies

C# is PascalCase, JSON APIs usually camelCase:

```csharp
var options = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
string json = JsonSerializer.Serialize(order, options);
```

Without the policy, `OrderTotal` serializes as `"OrderTotal"` — surprising
every JavaScript caller. Pick one convention per API and keep it.

## Case sensitivity is a feature

By default, deserialization is CASE-SENSITIVE: `"total"` does NOT bind to
a `Total` property, and silently stays default. ASP.NET's web defaults
differ (`PropertyNameCaseInsensitive = true`) — know which world you're in.
When parsing external payloads, decide deliberately; mismatches become
nulls/zeros, not errors.

## Round-trip fidelity

Serialize(Deserialize(json)) should preserve data. Frequent breakers:
- properties without setters (silently skipped on deserialize),
- `object`-typed members (typed as JsonElement on the way back),
- dictionaries with non-string keys,
- timezone-less DateTimes (kind is preserved, but check your contract).

## Check your understanding

- What happens to `"orderTotal"` with no naming policy? (Doesn't bind to OrderTotal — silently default.)
- Why prefer typed deserialization over JsonDocument for API payloads? (Type checks shape; defaults surface missing data; refactoring is compiler-checked.)
""",
    "Serialize, Deserialize, và Options",
    "JsonSerializer với naming policy, phân biệt hoa thường, và trung thực vòng lập.",
    r"""
## Hai công cụ chính

```csharp
string json = JsonSerializer.Serialize(order);
var back = JsonSerializer.Deserialize<Order>(json);
```

Serialize biến đối tượng thành văn bản JSON; Deserialize parse văn bản
thành đối tượng có kiểu. Deserialize YÊU CẦU kiểu đích — đó là cách JSON
trở thành C# có kiểm tra thay vì cháo string.

## Naming policy

C# là PascalCase, JSON API thường camelCase:

```csharp
var options = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
string json = JsonSerializer.Serialize(order, options);
```

Không có policy, `OrderTotal` serialize thành `"OrderTotal"` — gây bất ngờ
cho mọi caller JavaScript. Chọn một quy ước cho mỗi API và giữ nguyên.

## Phân biệt hoa thường là một tính năng

Mặc định, deserialize phân biệt HOA THƯỜNG: `"total"` KHÔNG bó vào property
`Total` và âm thầm giữ mặc định. Web defaults của ASP.NET khác
(`PropertyNameCaseInsensitive = true`) — biết mình đang ở thế giới nào. Khi
parse payload ngoài, quyết định tường minh; lệch khớp thành null/zero,
không phải lỗi.

## Trung thực vòng lập

Serialize(Deserialize(json)) phải bảo toàn dữ liệu. Thường gặp hỏng:
- property không có setter (bị bỏ qua im lặng khi deserialize),
- thành phần kiểu `object` (trở về là JsonElement),
- dictionary với key không phải string,
- DateTime không có múi giờ (kind được giữ, nhưng xem lại hợp đồng).

## Kiểm tra hiểu biết

- `"orderTotal"` xảy ra gì khi không có naming policy? (Không bó vào OrderTotal — âm thầm giữ mặc định.)
- Vì sao ưu tiên deserialize có kiểu thay vì JsonDocument cho payload API? (Kiểu kiểm tra hình dạng; mặc định lộ dữ liệu thiếu; refactor do compiler kiểm tra.)
""",
    r"""
## Hai công cụ chính

```csharp
string json = JsonSerializer.Serialize(order);
var back = JsonSerializer.Deserialize<Order>(json);
```

Serialize biến đối tượng thành văn bản JSON; Deserialize parse văn bản
thành đối tượng có kiểu. Deserialize YÊU CẦU kiểu đích — đó là cách JSON
trở thành C# có kiểm tra thay vì cháo string.

## Naming policy

C# là PascalCase, JSON API thường camelCase:

```csharp
var options = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
};
string json = JsonSerializer.Serialize(order, options);
```

Không có policy, `OrderTotal` serialize thành `"OrderTotal"` — gây bất ngờ
cho mọi caller JavaScript. Chọn một quy ước cho mỗi API và giữ nguyên.

## Phân biệt hoa thường là một tính năng

Mặc định, deserialize phân biệt HOA THƯỜNG: `"total"` KHÔNG bó vào property
`Total` và âm thầm giữ mặc định. Web defaults của ASP.NET khác
(`PropertyNameCaseInsensitive = true`) — biết mình đang ở thế giới nào. Khi
parse payload ngoài, quyết định tường minh; lệch khớp thành null/zero,
không phải lỗi.

## Trung thực vòng lập

Serialize(Deserialize(json)) phải bảo toàn dữ liệu. Thường gặp hỏng:
- property không có setter (bị bỏ qua im lặng khi deserialize),
- thành phần kiểu `object` (trở về là JsonElement),
- dictionary với key không phải string,
- DateTime không có múi giờ (kind được giữ, nhưng xem lại hợp đồng).

## Kiểm tra hiểu biết

- `"orderTotal"` xảy ra gì khi không có naming policy? (Không bó vào OrderTotal — âm thầm giữ mặc định.)
- Vì sao ưu tiên deserialize có kiểu thay vì JsonDocument cho payload API? (Kiểu kiểm tra hình dạng; mặc định lộ dữ liệu thiếu; refactor do compiler kiểm tra.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "converters-and-robustness",
    "Converters and Malformed Input",
    "Custom JsonConverter<T> for odd shapes, and defending the boundary with JsonException.",
    16,
    r"""
## When the shape doesn't match your model

External APIs send `"2026-09-17"` as a date-in-a-string, enums as names,
sometimes numbers as strings. A custom converter adapts without polluting
callers:

```csharp
public sealed class FlexibleIntConverter : JsonConverter<int>
{
    public override int Read(ref Utf8JsonReader reader, Type t, JsonSerializerOptions o)
        => reader.TokenType switch
        {
            JsonTokenType.Number => reader.GetInt32(),
            JsonTokenType.String => int.Parse(reader.GetString()!),
            _ => throw new JsonException(),
        };

    public override void Write(Utf8JsonWriter writer, int value, JsonSerializerOptions o)
        => writer.WriteNumberValue(value);
}

var options = new JsonSerializerOptions { Converters = { new FlexibleIntConverter() } };
```

Register per-options (or per-property with `[JsonConverter]`). Read handles
every token type you accept; Write is the simple direction.

## The boundary: malformed input is NORMAL

User uploads, third-party APIs, queues — malformed JSON is an everyday
event, not an edge case. `JsonSerializer.Deserialize` throws
`JsonException` with position info; catch it AT the boundary:

```csharp
try { return JsonSerializer.Deserialize<T>(payload, options); }
catch (JsonException ex)
{
    throw new InvalidOperationException("bad payload", ex);  // or return Result<T>
}
```

Letting JsonException escape into business layers couples them to the
wire format.

## Missing, null, and the difference

Missing property → target stays at its default. Explicit `"prop": null` →
assigns null (nullable members) or throws for non-nullable value types.
A field that must exist deserves a check after deserialization — the
serializer will not invent one.

## Check your understanding

- Which two methods does JsonConverter<T> override? (Read and Write.)
- Why catch JsonException at the boundary? (Business layers shouldn't know about wire formats.)
""",
    "Converters và Dữ liệu lỗi",
    "JsonConverter<T> tùy chỉnh cho hình dạng lạ, và phòng thủ biên giới với JsonException.",
    r"""
## Khi hình dạng không khớp mô hình của bạn

API ngoài gửi `"2026-09-17"` dạng chuỗi ngày, enum dạng tên, thỉnh thoảng
số dạng chuỗi. Converter tùy chỉnh thích ứng mà không làm bẩn caller:

```csharp
public sealed class FlexibleIntConverter : JsonConverter<int>
{
    public override int Read(ref Utf8JsonReader reader, Type t, JsonSerializerOptions o)
        => reader.TokenType switch
        {
            JsonTokenType.Number => reader.GetInt32(),
            JsonTokenType.String => int.Parse(reader.GetString()!),
            _ => throw new JsonException(),
        };

    public override void Write(Utf8JsonWriter writer, int value, JsonSerializerOptions o)
        => writer.WriteNumberValue(value);
}

var options = new JsonSerializerOptions { Converters = { new FlexibleIntConverter() } };
```

Đăng ký theo options (hoặc theo property với `[JsonConverter]`). Read xử lý
mọi token type bạn chấp nhận; Write là chiều đơn giản.

## Biên giới: dữ liệu lỗi là CHUYỆN THƯỜNG

Upload của người dùng, API bên thứ ba, hàng đợi — JSON lỗi là sự kiện hằng
ngày, không phải trường hợp hiếm. `JsonSerializer.Deserialize` ném
`JsonException` kèm thông tin vị trí; hãy bắt nó TẠI BIÊN GIỚI:

```csharp
try { return JsonSerializer.Deserialize<T>(payload, options); }
catch (JsonException ex)
{
    throw new InvalidOperationException("bad payload", ex);  // hoặc trả Result<T>
}
```

Để JsonException chảy vào tầng nghiệp vụ là buộc chúng biết về định dạng
truyền dẫn.

## Thiếu, null, và sự khác nhau

Property thiếu → đích giữ mặc định. `"prop": null` tường minh → gán null
(thành viên nullable) hoặc ném với value type không nullable. Một trường
bắt buộc phải có deserve một kiểm tra sau khi deserialize — serializer sẽ
không tự bịa.

## Kiểm tra hiểu biết

- JsonConverter<T> ghi đè hai phương thức nào? (Read và Write.)
- Vì sao bắt JsonException tại biên giới? (Tầng nghiệp vụ không nên biết định dạng truyền dẫn.)
""",
    r"""
## Khi hình dạng không khớp mô hình của bạn

API ngoài gửi `"2026-09-17"` dạng chuỗi ngày, enum dạng tên, thỉnh thoảng
số dạng chuỗi. Converter tùy chỉnh thích ứng mà không làm bẩn caller:

```csharp
public sealed class FlexibleIntConverter : JsonConverter<int>
{
    public override int Read(ref Utf8JsonReader reader, Type t, JsonSerializerOptions o)
        => reader.TokenType switch
        {
            JsonTokenType.Number => reader.GetInt32(),
            JsonTokenType.String => int.Parse(reader.GetString()!),
            _ => throw new JsonException(),
        };

    public override void Write(Utf8JsonWriter writer, int value, JsonSerializerOptions o)
        => writer.WriteNumberValue(value);
}

var options = new JsonSerializerOptions { Converters = { new FlexibleIntConverter() } };
```

Đăng ký theo options (hoặc theo property với `[JsonConverter]`). Read xử lý
mọi token type bạn chấp nhận; Write là chiều đơn giản.

## Biên giới: dữ liệu lỗi là CHUYỆN THƯỜNG

Upload của người dùng, API bên thứ ba, hàng đợi — JSON lỗi là sự kiện hằng
ngày, không phải trường hợp hiếm. `JsonSerializer.Deserialize` ném
`JsonException` kèm thông tin vị trí; hãy bắt nó TẠI BIÊN GIỚI:

```csharp
try { return JsonSerializer.Deserialize<T>(payload, options); }
catch (JsonException ex)
{
    throw new InvalidOperationException("bad payload", ex);  // hoặc trả Result<T>
}
```

Để JsonException chảy vào tầng nghiệp vụ là buộc chúng biết về định dạng
truyền dẫn.

## Thiếu, null, và sự khác nhau

Property thiếu → đích giữ mặc định. `"prop": null` tường minh → gán null
(thành viên nullable) hoặc ném với value type không nullable. Một trường
bắt buộc phải có deserve một kiểm tra sau khi deserialize — serializer sẽ
không tự bịa.

## Kiểm tra hiểu biết

- JsonConverter<T> ghi đè hai phương thức nào? (Read và Write.)
- Vì sao bắt JsonException tại biên giới? (Tầng nghiệp vụ không nên biết định dạng truyền dẫn.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p14-json",
    "JSON Practice: Options, Converters, Boundaries",
    "Round-trip with options, adapt an odd API shape with a converter, and harden a payload parser.",
    "Luyện JSON: Options, Converter, Biên giới",
    "Vòng lập với options, thích ứng hình dạng API lạ bằng converter, và gia cố parser payload.",
    "converters-and-robustness",
    30,
    "intermediate",
    [
        challenge(
            "csi-p14-camel-case",
            "camelCase Round Trip",
            """Implement the OrderService: SerializeOrder produces camelCase JSON ("orderId", "orderTotal"); DeserializeOrder parses both exact-camelCase and PascalCase JSON (case-insensitive on deserialize).

```csharp
public sealed record Order(int OrderId, decimal OrderTotal);
static string SerializeOrder(Solution.Order order);
static Solution.Order? DeserializeOrder(string json);
```""",
            STJ_PRELUDE,
            [
                (
                    "camelCase out, both cases in",
                    r"""
var order = new Solution.Order(7, 42.5m);
string json = Solution.SerializeOrder(order);
Cj.True(json.Contains("\"orderId\":7") && json.Contains("\"orderTotal\":42.5"), "camelCase emitted");
var back = Solution.DeserializeOrder(json);
Cj.Eq(back!.OrderId, 7, "round trip id");
Cj.Eq(back.OrderTotal, 42.5m, "round trip total");
var pascal = Solution.DeserializeOrder("{\"OrderId\":9,\"OrderTotal\":10}");
Cj.Eq(pascal!.OrderId, 9, "PascalCase input accepted");
""",
                    "Write with PropertyNamingPolicy.CamelCase; read with PropertyNameCaseInsensitive = true.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p14-numeric-strings",
            "The API That Sends Numbers as Strings",
            """LegacyApi sends {"count": "5"}. DeserializePayload must accept both {"count": 5} and {"count": "5"} into Payload.Count (int) via a custom JsonConverter<int>. Must also REJECT {"count": true}.

```csharp
public sealed class Payload { public int Count { get; set; } }
static Solution.Payload? DeserializePayload(string json);
```""",
            STJ_PRELUDE,
            [
                (
                    "both numeric shapes bind",
                    r"""
Cj.Eq(Solution.DeserializePayload("{\"count\":5}")!.Count, 5, "number form");
Cj.Eq(Solution.DeserializePayload("{\"count\":\"5\"}")!.Count, 5, "string form");
""",
                    "JsonConverter<int>: Number -> GetInt32, String -> int.Parse, else JsonException.",
                ),
                (
                    "junk tokens rejected",
                    r"""
try
{
    Solution.DeserializePayload("{\"count\":true}");
    Cj.True(false, "should throw");
}
catch (System.Text.Json.JsonException) { }
""",
                    "Default arm of the switch throws JsonException.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p14-malformed-debug",
            "Debug: The Parser That Crashes the App",
            """ImportProducts throws raw JsonException (and crashes the caller) on malformed input, and silently accepts products with missing names as "". Fix: parse errors surface as InvalidOperationException("bad payload", ex); a missing or empty Name also throws InvalidOperationException with "bad payload" (no exceptions escape other than that type).

```csharp
public sealed record Product(string Name, decimal Price);
static System.Collections.Generic.List<Solution.Product> ImportProducts(string json);
// json: {"products":[{"name":"bolt","price":0.5},{"name":"nut","price":0.2}]}
```""",
            STJ_PRELUDE,
            [
                (
                    "valid input parses",
                    r"""
var items = Solution.ImportProducts("{\"products\":[{\"name\":\"bolt\",\"price\":0.5},{\"name\":\"nut\",\"price\":0.2}]}");
Cj.Eq(items.Count, 2, "two products");
Cj.Eq(items[0].Name, "bolt", "first name");
Cj.Eq(items[1].Price, 0.2m, "second price");
""",
                    "Deserialize a wrapper DTO with a Products list.",
                ),
                (
                    "malformed JSON -> InvalidOperationException",
                    r"""
try
{
    Solution.ImportProducts("{\"products\":[");
    Cj.True(false, "should throw");
}
catch (System.InvalidOperationException ex) { Cj.True(ex.Message.Contains("bad payload"), "boundary message"); }
""",
                    "Catch JsonException and rethrow as InvalidOperationException with the message.",
                ),
                (
                    "missing name rejected",
                    r"""
try
{
    Solution.ImportProducts("{\"products\":[{\"price\":1.5}]}");
    Cj.True(false, "should throw");
}
catch (System.InvalidOperationException) { }
""",
                    "Validate after deserialization: null/empty Name -> InvalidOperationException.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p14-camel-case": vi_challenge(
            "Vòng lập camelCase",
            "Hiện thực OrderService: SerializeOrder sinh JSON camelCase (\"orderId\", \"orderTotal\"); DeserializeOrder parse được cả JSON camelCase đúng lẫn PascalCase (không phân biệt hoa thường khi deserialize).",
            [
                ("camelCase out, both cases in", "Ghi với PropertyNamingPolicy.CamelCase; đọc với PropertyNameCaseInsensitive = true."),
            ],
        ),
        "csi-p14-numeric-strings": vi_challenge(
            "API gửi số dạng chuỗi",
            "LegacyApi gửi {\"count\": \"5\"}. DeserializePayload phải chấp nhận cả {\"count\": 5} lẫn {\"count\": \"5\"} vào Payload.Count (int) qua JsonConverter<int> tùy chỉnh. Đồng thời phải TỪ CHỐI {\"count\": true}.",
            [
                ("both numeric shapes bind", "JsonConverter<int>: Number -> GetInt32, String -> int.Parse, còn lại JsonException."),
                ("junk tokens rejected", "Nhánh default của switch ném JsonException."),
            ],
        ),
        "csi-p14-malformed-debug": vi_challenge(
            "Debug: Parser làm sập ứng dụng",
            "ImportProducts ném JsonException thô (làm sập caller) khi gặp JSON lỗi, và âm thầm chấp nhận sản phẩm thiếu Name thành \"\". Sửa: lỗi parse nổi lên thành InvalidOperationException(\"bad payload\", ex); Name thiếu hoặc rỗng cũng ném InvalidOperationException \"bad payload\".",
            [
                ("valid input parses", "Deserialize một DTO wrapper có danh sách Products."),
                ("malformed JSON -> InvalidOperationException", "Bắt JsonException và ném lại thành InvalidOperationException kèm thông điệp."),
                ("missing name rejected", "Kiểm tra sau khi deserialize: Name null/rỗng -> InvalidOperationException."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p14-camel-case",
            'public class Solution\n{\n    public sealed record Order(int OrderId, decimal OrderTotal);\n\n    private static readonly System.Text.Json.JsonSerializerOptions WriteOpts = new()\n    {\n        PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase,\n    };\n\n    private static readonly System.Text.Json.JsonSerializerOptions ReadOpts = new()\n    {\n        PropertyNameCaseInsensitive = true,\n    };\n\n    public static string SerializeOrder(Order order) =>\n        System.Text.Json.JsonSerializer.Serialize(order, WriteOpts);\n\n    public static Order? DeserializeOrder(string json) =>\n        System.Text.Json.JsonSerializer.Deserialize<Order>(json, ReadOpts);\n}\n',
            'public class Solution\n{\n    public sealed record Order(int OrderId, decimal OrderTotal);\n\n    public static string SerializeOrder(Order order) =>\n        System.Text.Json.JsonSerializer.Serialize(order);   // near-miss: no naming policy — "OrderId" not "orderId"\n\n    public static Order? DeserializeOrder(string json) =>\n        System.Text.Json.JsonSerializer.Deserialize<Order>(json);   // near-miss: case-sensitive, PascalCase input silently yields defaults\n}\n',
        ),
        (
            "csi-p14-numeric-strings",
            'public class Solution\n{\n    public sealed class Payload\n    {\n        public int Count { get; set; }\n    }\n\n    public sealed class FlexibleIntConverter : System.Text.Json.Serialization.JsonConverter<int>\n    {\n        public override int Read(ref System.Text.Json.Utf8JsonReader reader, System.Type typeToConvert, System.Text.Json.JsonSerializerOptions options)\n        {\n            return reader.TokenType switch\n            {\n                System.Text.Json.JsonTokenType.Number => reader.GetInt32(),\n                System.Text.Json.JsonTokenType.String => int.Parse(reader.GetString()!),\n                _ => throw new System.Text.Json.JsonException(),\n            };\n        }\n\n        public override void Write(System.Text.Json.Utf8JsonWriter writer, int value, System.Text.Json.JsonSerializerOptions options)\n        {\n            writer.WriteNumberValue(value);\n        }\n    }\n\n    private static readonly System.Text.Json.JsonSerializerOptions Opts = new()\n    {\n        PropertyNameCaseInsensitive = true,   // external payload: keys may vary in case\n        Converters = { new FlexibleIntConverter() },\n    };\n\n    public static Payload? DeserializePayload(string json) =>\n        System.Text.Json.JsonSerializer.Deserialize<Payload>(json, Opts);\n}\n',
            'public class Solution\n{\n    public sealed class Payload\n    {\n        public int Count { get; set; }\n    }\n\n    public sealed class FlexibleIntConverter : System.Text.Json.Serialization.JsonConverter<int>\n    {\n        public override int Read(ref System.Text.Json.Utf8JsonReader reader, System.Type typeToConvert, System.Text.Json.JsonSerializerOptions options)\n        {\n            // near-miss: GetString() on a NUMBER token throws InvalidOperationException\n            // (not JsonException), and the string arm is never reached — the\n            // string-form test fails\n            return reader.GetInt32();\n        }\n\n        public override void Write(System.Text.Json.Utf8JsonWriter writer, int value, System.Text.Json.JsonSerializerOptions options)\n        {\n            writer.WriteNumberValue(value);\n        }\n    }\n\n    private static readonly System.Text.Json.JsonSerializerOptions Opts = new()\n    {\n        Converters = { new FlexibleIntConverter() },\n    };\n\n    public static Payload? DeserializePayload(string json) =>\n        System.Text.Json.JsonSerializer.Deserialize<Payload>(json, Opts);\n}\n',
        ),
        (
            "csi-p14-malformed-debug",
            'public class Solution\n{\n    public sealed record Product(string Name, decimal Price);\n\n    private sealed class Wrapper\n    {\n        public System.Collections.Generic.List<Product> Products { get; set; } = new();\n    }\n\n    private static readonly System.Text.Json.JsonSerializerOptions ReadOpts = new()\n    {\n        PropertyNameCaseInsensitive = true,\n    };\n\n    public static System.Collections.Generic.List<Product> ImportProducts(string json)\n    {\n        Wrapper wrapper;\n        try\n        {\n            wrapper = System.Text.Json.JsonSerializer.Deserialize<Wrapper>(json, ReadOpts)\n                ?? throw new System.InvalidOperationException("bad payload");\n        }\n        catch (System.Text.Json.JsonException ex)\n        {\n            throw new System.InvalidOperationException("bad payload", ex);\n        }\n\n        var items = new System.Collections.Generic.List<Product>();\n        foreach (var p in wrapper.Products)\n        {\n            if (string.IsNullOrEmpty(p.Name))\n                throw new System.InvalidOperationException("bad payload");\n            items.Add(p);\n        }\n        return items;\n    }\n}\n',
            'public class Solution\n{\n    public sealed record Product(string Name, decimal Price);\n\n    private sealed class Wrapper\n    {\n        public System.Collections.Generic.List<Product> Products { get; set; } = new();\n    }\n\n    public static System.Collections.Generic.List<Product> ImportProducts(string json)\n    {\n        // near-miss: no try/catch — raw JsonException escapes and the caller\n        // (and the malformed test) sees the wire-format exception type\n        var wrapper = System.Text.Json.JsonSerializer.Deserialize<Wrapper>(json)!;\n        return wrapper.Products;\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m14",
    "Checkpoint — The Catalog Import/Export Engine",
    "Combine options, converters, and boundary defense into one round-trip-safe catalog service.",
    25,
    r"""
## The gate (mini-build)

A product catalog exchange — import, export, and transform:

1. `Export(IEnumerable<Product> products)` → camelCase JSON array:
   `[{"name":"bolt","price":0.5},...]` (name string, price number).
2. `Import(string json)` → products; tolerant of price as number OR string
   (via a custom converter); malformed JSON or a missing/empty name →
   `InvalidOperationException("bad payload")`.
3. `Merge(string jsonA, string jsonB)` → union by name (first wins),
   exported as `Export` would.

Product: `record Product(string Name, decimal Price)`. Input JSON shape:
`{"products":[{"name":"bolt","price":0.5}]}`.
""",
    "Checkpoint — Bộ máy Xuất/Nhập Danh mục",
    "Kết hợp options, converter, và phòng thủ biên giới thành một service danh mục an toàn vòng lập.",
    r"""
## Cổng kiểm tra (mini-build)

Trao đổi danh mục sản phẩm — nhập, xuất, và biến đổi:

1. `Export(IEnumerable<Product> products)` → mảng JSON camelCase:
   `[{"name":"bolt","price":0.5},...]` (name chuỗi, price số).
2. `Import(string json)` → sản phẩm; chấp nhận price dạng số HOẶC chuỗi
   (qua converter tùy chỉnh); JSON lỗi hoặc name thiếu/rỗng →
   `InvalidOperationException("bad payload")`.
3. `Merge(string jsonA, string jsonB)` → hợp theo name (cái trước thắng),
   xuất như `Export`.

Product: `record Product(string Name, decimal Price)`. Hình dạng JSON vào:
`{"products":[{"name":"bolt","price":0.5}]}`.
""",
    challenge(
        "csi-checkpoint-m14-task",
        "Checkpoint: Catalog Exchange",
        """Implement the catalog service described in the checkpoint:

```csharp
public sealed record Product(string Name, decimal Price);
static string Export(System.Collections.Generic.IEnumerable<Solution.Product> products);
static System.Collections.Generic.List<Solution.Product> Import(string json);
static string Merge(string jsonA, string jsonB);
```""",
        STJ_PRELUDE,
        [
            (
                "export camelCase",
                r"""
string json = Solution.Export(new System.Collections.Generic.List<Solution.Product>
{
    new Solution.Product("bolt", 0.5m),
    new Solution.Product("nut", 0.2m),
});
Cj.True(json.Contains("\"name\":\"bolt\"") && json.Contains("\"price\":0.5"), "camelCase fields");
Cj.True(json.StartsWith("["), "array shape");
""",
                    "Serialize with PropertyNamingPolicy.CamelCase.",
                ),
                (
                    "import: both price shapes, bad payload defense",
                    r"""
var items = Solution.Import("{\"products\":[{\"name\":\"bolt\",\"price\":0.5},{\"name\":\"nut\",\"price\":\"0.2\"}]}");
Cj.Eq(items.Count, 2, "number and string prices");
Cj.Eq(items[1].Price, 0.2m, "string price converted");
try { Solution.Import("{oops"); Cj.True(false, "should throw"); }
catch (System.InvalidOperationException ex) { Cj.True(ex.Message.Contains("bad payload"), "boundary message"); }
try { Solution.Import("{\"products\":[{\"price\":1}]}"); Cj.True(false, "should throw"); }
catch (System.InvalidOperationException) { }
""",
                    "Flexible decimal converter; wrap parse in try/catch(JsonException); validate names after.",
                ),
                (
                    "merge: first wins, exported shape",
                    r"""
string a = "{\"products\":[{\"name\":\"bolt\",\"price\":0.5}]}";
string b = "{\"products\":[{\"name\":\"bolt\",\"price\":9.9},{\"name\":\"nut\",\"price\":0.2}]}";
string merged = Solution.Merge(a, b);
Cj.True(merged.TrimStart().StartsWith("["), "exported array shape");
Cj.True(merged.Contains("\"name\":\"bolt\"") && merged.Contains("\"name\":\"nut\""), "both names present");
Cj.True(merged.Contains("0.5") && !merged.Contains("9.9"), "first occurrence wins");
""",
                    "Import both, dedupe by name preserving first, Export the result.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Trao đổi danh mục",
            "Hiện thực service: Export camelCase; Import chấp nhận price dạng số/chuỗi, JSON lỗi hoặc name rỗng -> InvalidOperationException(\"bad payload\"); Merge hợp theo name (cái trước thắng) và xuất lại.",
            [
                ("export camelCase", "Serialize với PropertyNamingPolicy.CamelCase."),
                ("import: both price shapes, bad payload defense", "Converter decimal linh hoạt; bọc parse trong try/catch(JsonException); kiểm tra tên sau."),
                ("merge: first wins, exported shape", "Import cả hai, khử trùng lặp theo name giữ cái đầu, Export kết quả."),
            ],
        ),
        solution='public class Solution\n{\n    public sealed record Product(string Name, decimal Price);\n\n    private sealed class Wrapper\n    {\n        public System.Collections.Generic.List<Product> Products { get; set; } = new();\n    }\n\n    public sealed class FlexibleDecimalConverter : System.Text.Json.Serialization.JsonConverter<decimal>\n    {\n        public override decimal Read(ref System.Text.Json.Utf8JsonReader reader, System.Type typeToConvert, System.Text.Json.JsonSerializerOptions options)\n        {\n            return reader.TokenType switch\n            {\n                System.Text.Json.JsonTokenType.Number => reader.GetDecimal(),\n                System.Text.Json.JsonTokenType.String => decimal.Parse(reader.GetString()!, System.Globalization.CultureInfo.InvariantCulture),\n                _ => throw new System.Text.Json.JsonException(),\n            };\n        }\n\n        public override void Write(System.Text.Json.Utf8JsonWriter writer, decimal value, System.Text.Json.JsonSerializerOptions options)\n        {\n            writer.WriteNumberValue(value);\n        }\n    }\n\n    private static readonly System.Text.Json.JsonSerializerOptions WriteOpts = new()\n    {\n        PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase,\n    };\n\n    private static readonly System.Text.Json.JsonSerializerOptions ReadOpts = new()\n    {\n        PropertyNameCaseInsensitive = true,\n        Converters = { new FlexibleDecimalConverter() },\n    };\n\n    public static string Export(System.Collections.Generic.IEnumerable<Product> products)\n    {\n        return System.Text.Json.JsonSerializer.Serialize(products, WriteOpts);\n    }\n\n    public static System.Collections.Generic.List<Product> Import(string json)\n    {\n        Wrapper wrapper;\n        try\n        {\n            wrapper = System.Text.Json.JsonSerializer.Deserialize<Wrapper>(json, ReadOpts)\n                ?? throw new System.InvalidOperationException("bad payload");\n        }\n        catch (System.Text.Json.JsonException ex)\n        {\n            throw new System.InvalidOperationException("bad payload", ex);\n        }\n\n        var items = new System.Collections.Generic.List<Product>();\n        foreach (var p in wrapper.Products)\n        {\n            if (string.IsNullOrEmpty(p.Name))\n                throw new System.InvalidOperationException("bad payload");\n            items.Add(p);\n        }\n        return items;\n    }\n\n    public static string Merge(string jsonA, string jsonB)\n    {\n        var seen = new System.Collections.Generic.HashSet<string>();\n        var merged = new System.Collections.Generic.List<Product>();\n        foreach (var p in Import(jsonA).Concat(Import(jsonB)))\n        {\n            if (seen.Add(p.Name)) merged.Add(p);\n        }\n        return Export(merged);\n    }\n}\n',
        wrong='public class Solution\n{\n    public sealed record Product(string Name, decimal Price);\n\n    private sealed class Wrapper\n    {\n        public System.Collections.Generic.List<Product> Products { get; set; } = new();\n    }\n\n    private static readonly System.Text.Json.JsonSerializerOptions ReadOpts = new()\n    {\n        PropertyNameCaseInsensitive = true,\n        // near-miss: no flexible decimal converter — string prices fail\n        // deserialization outright\n    };\n\n    public static string Export(System.Collections.Generic.IEnumerable<Product> products)\n    {\n        return System.Text.Json.JsonSerializer.Serialize(products);\n    }\n\n    public static System.Collections.Generic.List<Product> Import(string json)\n    {\n        var wrapper = System.Text.Json.JsonSerializer.Deserialize<Wrapper>(json, ReadOpts)!;\n        return wrapper.Products;\n    }\n\n    public static string Merge(string jsonA, string jsonB)\n    {\n        var merged = new System.Collections.Generic.List<Product>();\n        merged.AddRange(Import(jsonA));\n        merged.AddRange(Import(jsonB));\n        return Export(merged);\n    }\n}\n',
    )
print("module 14 authored")
