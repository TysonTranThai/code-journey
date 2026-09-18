#!/usr/bin/env python3
"""C# — Intermediate — Module 12: csi-config.

Configuration & options: config sources (JSON, environment variables), the
options pattern (typed options + validation), environment layering, and
secrets principles. Graded fully deterministically: in-process env vars and
config passed as strings.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE,
)

M = "csi-config"

STJ_PRELUDE = CS_PRELUDE + "using System.Text.Json;\n"

write_module(
    M,
    "Configuration & Options",
    "Layer config from files and environment variables into validated, strongly-typed options — and keep secrets out of source.",
    "Cấu hình & Options",
    "Xếp lớp cấu hình từ file và biến môi trường thành options có kiểu, đã kiểm tra — và giữ bí mật khỏi mã nguồn.",
    ["options-pattern", "environments-and-secrets", "csi-checkpoint-m12"],
    ["csi-p12-config"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "options-pattern",
    "Configuration Sources and the Options Pattern",
    "Key-value config from multiple sources, bound into typed options objects that fail fast when wrong.",
    17,
    r"""
## Config is data your code needs before it runs

Database locations, feature flags, limits, URLs. Rules of the road:
config lives OUTSIDE compiled code, comes from SOURCES (JSON files,
environment variables, command-line args — most specific wins), and reaches
your classes as plain injected values.

## The options pattern: a typed view

Instead of string keys scattered around, bind a section to a class:

```csharp
public sealed class RetryOptions
{
    public int MaxAttempts { get; set; } = 3;
    public int DelayMs { get; set; } = 200;
}

// binding (hand-rolled shape; ASP.NET's binder does the same)
var section = JsonDocument.Parse(json).RootElement.GetProperty("Retry");
var options = new RetryOptions
{
    MaxAttempts = section.GetProperty("MaxAttempts").GetInt32(),
    DelayMs = section.GetProperty("DelayMs").GetInt32(),
};
```

Defaults live ON the options class; config overrides them. Consumers
receive `RetryOptions` (or `IOptions<RetryOptions>` in ASP.NET) — never the
raw config — so keys are referenced in exactly one place.

## Validate at startup, not at 3 a.m.

Fail FAST with a precise message:

```csharp
if (options.MaxAttempts < 1)
    throw new OptionsValidationException("Retry", "MaxAttempts must be >= 1");
```

An invalid port number discovered at startup is a one-line fix; the same
discovery on Friday night is an incident.

## Environment variables: the deployment layer

`Environment.GetEnvironmentVariable("CJ_RETRY__MAXATTEMPTS")` —
deployment pipelines inject these; double-underscore is the ASP.NET
convention for nesting (`Retry:MaxAttempts`). Env vars override file
config in every mainstream host — layering is the point.

## Check your understanding

- Why bind into a typed class instead of passing strings? (One place knows the keys; types catch shape errors; defaults live on the class.)
- Which wins: file or environment? (Environment — more specific deployment context.)
""",
    "Nguồn cấu hình và Options Pattern",
    "Cấu hình key-value từ nhiều nguồn, bó vào options có kiểu, sai thì fail ngay.",
    r"""
## Cấu hình là dữ liệu code cần trước khi chạy

Vị trí database, feature flag, giới hạn, URL. Nguyên tắc: cấu hình nằm
NGOÀI mã biên dịch, đến từ CÁC NGUỒN (file JSON, biến môi trường, tham số
dòng lệnh — cụ thể nhất thắng), và tới tay các lớp như giá trị được inject
bình thường.

## Options pattern: góc nhìn có kiểu

Thay vì rải string key khắp nơi, bó một section vào một lớp:

```csharp
public sealed class RetryOptions
{
    public int MaxAttempts { get; set; } = 3;
    public int DelayMs { get; set; } = 200;
}

// bó (dạng tự viết; binder của ASP.NET làm y hệt)
var section = JsonDocument.Parse(json).RootElement.GetProperty("Retry");
var options = new RetryOptions
{
    MaxAttempts = section.GetProperty("MaxAttempts").GetInt32(),
    DelayMs = section.GetProperty("DelayMs").GetInt32(),
};
```

Mặc định nằm TRÊN lớp options; cấu hình ghi đè. Consumer nhận
`RetryOptions` (hoặc `IOptions<RetryOptions>` trong ASP.NET) — không bao giờ
nhận cấu hình thô — nên key chỉ được nhắc đúng một nơi.

## Kiểm tra lúc khởi động, không phải 3 giờ sáng

Fail NHANH với thông báo chính xác:

```csharp
if (options.MaxAttempts < 1)
    throw new OptionsValidationException("Retry", "MaxAttempts must be >= 1");
```

Số cổng sai phát hiện lúc startup là sửa một dòng; phát hiện giống hệt lúc
tối thứ sáu là một sự cố.

## Biến môi trường: tầng triển khai

`Environment.GetEnvironmentVariable("CJ_RETRY__MAXATTEMPTS")` — pipeline
triển khai đưa vào; hai dấu gạch dưới là quy ước lồng của ASP.NET
(`Retry:MaxAttempts`). Env ghi đè file trong mọi host phổ thông — xếp lớp
chính là điểm nhấn.

## Kiểm tra hiểu biết

- Vì sao bó vào lớp có kiểu thay vì truyền string? (Một nơi nắm key; kiểu bắt lỗi hình dạng; mặc định nằm trên lớp.)
- Cái nào thắng: file hay biến môi trường? (Môi trường — ngữ cảnh triển khai cụ thể hơn.)
""",
    r"""
## Cấu hình là dữ liệu code cần trước khi chạy

Vị trí database, feature flag, giới hạn, URL. Nguyên tắc: cấu hình nằm
NGOÀI mã biên dịch, đến từ CÁC NGUỒN (file JSON, biến môi trường, tham số
dòng lệnh — cụ thể nhất thắng), và tới tay các lớp như giá trị được inject
bình thường.

## Options pattern: góc nhìn có kiểu

Thay vì rải string key khắp nơi, bó một section vào một lớp:

```csharp
public sealed class RetryOptions
{
    public int MaxAttempts { get; set; } = 3;
    public int DelayMs { get; set; } = 200;
}

// bó (dạng tự viết; binder của ASP.NET làm y hệt)
var section = JsonDocument.Parse(json).RootElement.GetProperty("Retry");
var options = new RetryOptions
{
    MaxAttempts = section.GetProperty("MaxAttempts").GetInt32(),
    DelayMs = section.GetProperty("DelayMs").GetInt32(),
};
```

Mặc định nằm TRÊN lớp options; cấu hình ghi đè. Consumer nhận
`RetryOptions` (hoặc `IOptions<RetryOptions>` trong ASP.NET) — không bao giờ
nhận cấu hình thô — nên key chỉ được nhắc đúng một nơi.

## Kiểm tra lúc khởi động, không phải 3 giờ sáng

Fail NHANH với thông báo chính xác:

```csharp
if (options.MaxAttempts < 1)
    throw new OptionsValidationException("Retry", "MaxAttempts must be >= 1");
```

Số cổng sai phát hiện lúc startup là sửa một dòng; phát hiện giống hệt lúc
tối thứ sáu là một sự cố.

## Biến môi trường: tầng triển khai

`Environment.GetEnvironmentVariable("CJ_RETRY__MAXATTEMPTS")` — pipeline
triển khai đưa vào; hai dấu gạch dưới là quy ước lồng của ASP.NET
(`Retry:MaxAttempts`). Env ghi đè file trong mọi host phổ thông — xếp lớp
chính là điểm nhấn.

## Kiểm tra hiểu biết

- Vì sao bó vào lớp có kiểu thay vì truyền string? (Một nơi nắm key; kiểu bắt lỗi hình dạng; mặc định nằm trên lớp.)
- Cái nào thắng: file hay biến môi trường? (Môi trường — ngữ cảnh triển khai cụ thể hơn.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "environments-and-secrets",
    "Environment-Specific Config and Secrets",
    "Dev/staging/prod differences, layered lookup, and the never-commit-a-secret discipline.",
    15,
    r"""
## Environments differ by wiring, not by code

The same binary runs in dev (local DB, verbose logging), staging (prod
shape, test data), production (real DB, sampled logging). The ENVIRONMENT
NAME selects which config layer loads — code never branches on
`if (env == "prod")` for business behavior.

## Layered lookup

```csharp
string? Get(string key) =>
    Environment.GetEnvironmentVariable(Prefix + key)      // 1. env
    ?? FromJson(key)                                      // 2. appsettings.json
    ?? Defaults(key);                                     // 3. code defaults
```

Order matters and stays the same everywhere; production overrides staging
overrides dev only through SOURCES, never through code paths.

## Secrets: the discipline

API keys, connection passwords, signing keys:

1. NEVER in source or Git history — "we'll rotate before merging" is how
   breaches happen. Assume anything committed is burned forever.
2. Secrets come from the environment or a secret store (env vars for this
   course; user-secrets tooling / vaults in real deployments).
3. NEVER log them — a request log that echoes an Authorization header is a
   leak. Log key NAMES, never values.
4. No hardcoded fallbacks: `config["ApiKey"] ?? "sk-dev-123"` silently
   ships a credential.

## Check your understanding

- Where does "which DB is the staging one" live? (Staging's config source — not an if in code.)
- Why is a hardcoded default for a secret worse than throwing? (It silently ships a real credential; failing fast surfaces the misconfiguration.)
""",
    "Cấu hình theo môi trường và Bí mật",
    "Khác biệt dev/staging/prod, tra cứu xếp lớp, và kỷ luật không-commit-bí-mật.",
    r"""
## Môi trường khác nhau ở chỗ nối dây, không phải ở code

Cùng một bản binary chạy ở dev (DB local, log chi tiết), staging (hình dáng
prod, dữ liệu test), production (DB thật, log lấy mẫu). TÊN MÔI TRƯỜNG chọn
tầng cấu hình được nạp — code không rẽ nhánh `if (env == "prod")` cho hành
vi nghiệp vụ.

## Tra cứu xếp lớp

```csharp
string? Get(string key) =>
    Environment.GetEnvironmentVariable(Prefix + key)      // 1. env
    ?? FromJson(key)                                      // 2. appsettings.json
    ?? Defaults(key);                                     // 3. mặc định trong code
```

Thứ tự quan trọng và giữ nguyên khắp nơi; production thắng staging thắng
dev chỉ thông qua NGUỒN, không bao giờ qua nhánh code.

## Bí mật: kỷ luật

API key, mật khẩu kết nối, key ký số:

1. KHÔNG BAO GIỜ trong mã nguồn hay lịch sử Git — "sẽ xoay key trước khi
   merge" chính là cách rò rỉ xảy ra. Hãy coi mọi thứ đã commit là cháy mãi
   mãi.
2. Bí mật đến từ môi trường hoặc secret store (biến môi trường cho khóa
   này; user-secrets / vault trong triển khai thật).
3. KHÔNG BAO GIỜ log chúng — request log in lại header Authorization là một
   rò rỉ. Log TÊN key, không bao giờ log GIÁ TRỊ.
4. Không fallback cứng: `config["ApiKey"] ?? "sk-dev-123"` âm thầm vận
   chuyển một credential.

## Kiểm tra hiểu biết

- "DB của staging là cái nào" nằm ở đâu? (Trong nguồn cấu hình của staging — không phải một if trong code.)
- Vì sao fallback cứng cho secret còn tệ hơn ném lỗi? (Nó âm thầm vận chuyển credential thật; fail fast làm lộ ra cấu hình sai.)
""",
    r"""
## Môi trường khác nhau ở chỗ nối dây, không phải ở code

Cùng một bản binary chạy ở dev (DB local, log chi tiết), staging (hình dáng
prod, dữ liệu test), production (DB thật, log lấy mẫu). TÊN MÔI TRƯỜNG chọn
tầng cấu hình được nạp — code không rẽ nhánh `if (env == "prod")` cho hành
vi nghiệp vụ.

## Tra cứu xếp lớp

```csharp
string? Get(string key) =>
    Environment.GetEnvironmentVariable(Prefix + key)      // 1. env
    ?? FromJson(key)                                      // 2. appsettings.json
    ?? Defaults(key);                                     // 3. mặc định trong code
```

Thứ tự quan trọng và giữ nguyên khắp nơi; production thắng staging thắng
dev chỉ thông qua NGUỒN, không bao giờ qua nhánh code.

## Bí mật: kỷ luật

API key, mật khẩu kết nối, key ký số:

1. KHÔNG BAO GIỜ trong mã nguồn hay lịch sử Git — "sẽ xoay key trước khi
   merge" chính là cách rò rỉ xảy ra. Hãy coi mọi thứ đã commit là cháy mãi
   mãi.
2. Bí mật đến từ môi trường hoặc secret store (biến môi trường cho khóa
   này; user-secrets / vault trong triển khai thật).
3. KHÔNG BAO GIỜ log chúng — request log in lại header Authorization là một
   rò rỉ. Log TÊN key, không bao giờ log GIÁ TRỊ.
4. Không fallback cứng: `config["ApiKey"] ?? "sk-dev-123"` âm thầm vận
   chuyển một credential.

## Kiểm tra hiểu biết

- "DB của staging là cái nào" nằm ở đâu? (Trong nguồn cấu hình của staging — không phải một if trong code.)
- Vì sao fallback cứng cho secret còn tệ hơn ném lỗi? (Nó âm thầm vận chuyển credential thật; fail fast làm lộ ra cấu hình sai.)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p12-config",
    "Config Practice: Providers, Binding, Secrets",
    "Build an environment provider, bind JSON into typed options, and close the hardcoded-secret hole.",
    "Luyện Cấu hình: Provider, Binding, Bí mật",
    "Dựng provider môi trường, bó JSON thành options có kiểu, và bịt lỗ hổng bí mật cứng.",
    "environments-and-secrets",
    30,
    "intermediate",
    [
        challenge(
            "csi-p12-env-provider",
            "The Environment Provider",
            """Build a prefix-scoped provider over environment variables: Get(name) looks up "<PREFIX>__<NAME>" (double-underscore), returning null when unset. GetInt(name) parses to int and throws FormatException with the raw value when not a number. Tests control the environment in-process.

```csharp
public sealed class EnvConfig
{
    public EnvConfig(string prefix);         // e.g. "CJ"
    public string? Get(string name);
    public int GetInt(string name);          // throws FormatException on junk
}
```""",
            CS_PRELUDE,
            [
                (
                    "prefix lookup and miss",
                    r"""
System.Environment.SetEnvironmentVariable("CJ__REGION", "eu-1");
try
{
    var cfg = new Solution.EnvConfig("CJ");
    Cj.Eq(cfg.Get("REGION"), "eu-1", "prefix + name resolved");
    Cj.True(cfg.Get("MISSING") is null, "unset -> null");
}
finally
{
    System.Environment.SetEnvironmentVariable("CJ__REGION", null);
}
""",
                    "Environment.GetEnvironmentVariable(prefix + \"__\" + name).",
                ),
                (
                    "typed access with a precise failure",
                    r"""
System.Environment.SetEnvironmentVariable("CJ__PORT", "8080");
System.Environment.SetEnvironmentVariable("CJ__BADPORT", "8o8o");
try
{
    var cfg = new Solution.EnvConfig("CJ");
    Cj.Eq(cfg.GetInt("PORT"), 8080, "parses int");
    try { cfg.GetInt("BADPORT"); Cj.True(false, "should throw"); }
    catch (System.FormatException) { }
}
finally
{
    System.Environment.SetEnvironmentVariable("CJ__PORT", null);
    System.Environment.SetEnvironmentVariable("CJ__BADPORT", null);
}
""",
                    "int.Parse and let FormatException surface (never swallow a bad value into a silent 0).",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p12-options-binding",
            "Bind JSON into Options",
            """Bind a JSON section into a typed options class with defaults: missing keys keep defaults, present keys override, and Validate() reports ALL problems (not just the first) by throwing OptionsValidationException with the message "Retry: <all problems joined by '; '>".

```csharp
public sealed class RetryOptions
{
    public int MaxAttempts { get; set; } = 3;
    public int DelayMs { get; set; } = 200;
}
public sealed class OptionsBinder
{
    public static RetryOptions Bind(string json);            // { "Retry": { ... } }
    public static void Validate(RetryOptions options);       // MaxAttempts >= 1, DelayMs >= 0
}
```""",
            STJ_PRELUDE,
            [
                (
                    "defaults and overrides",
                    r"""
var defaults = Solution.OptionsBinder.Bind("{}");
Cj.Eq(defaults.MaxAttempts, 3, "default attempts");
Cj.Eq(defaults.DelayMs, 200, "default delay");
var custom = Solution.OptionsBinder.Bind("{\"Retry\":{\"MaxAttempts\":5,\"DelayMs\":50}}");
Cj.Eq(custom.MaxAttempts, 5, "overridden attempts");
Cj.Eq(custom.DelayMs, 50, "overridden delay");
""",
                    "JsonDocument.Parse; GetProperty(\"Retry\") when present; fill only provided keys.",
                ),
                (
                    "validation reports everything",
                    r"""
var bad = new Solution.RetryOptions { MaxAttempts = 0, DelayMs = -1 };
try
{
    Solution.OptionsBinder.Validate(bad);
    Cj.True(false, "should throw");
}
catch (System.InvalidOperationException ex)
{
    Cj.True(ex.Message.Contains("MaxAttempts") && ex.Message.Contains("DelayMs"), "all problems listed");
}
""",
                    "Collect every violated rule into one message, then throw once.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p12-secrets-debug",
            "Debug: The Hardcoded API Key",
            """ReportSender has the API key hardcoded and falls back to it when config is missing — a credential silently ships to every environment, and missing configuration goes unnoticed. Fix it: the key must come from IConfigProvider with NO fallback; when missing, throw InvalidOperationException("ApiKey is not configured"). Tests use the provided MemoryConfig.

```csharp
public interface IConfigProvider { string? Get(string key); }
public sealed class MemoryConfig : IConfigProvider { public MemoryConfig(params (string, string)[] entries); }
public sealed class ReportSender
{
    public ReportSender(IConfigProvider config);
    public string Send(string report);     // returns "sent:<key>:<len>" using the configured key
}
```""",
            CS_PRELUDE,
            [
                (
                    "configured key is used",
                    r"""
var cfg = new Solution.MemoryConfig(("ApiKey", "sk-live-9"));
var sender = new Solution.ReportSender(cfg);
Cj.Eq(sender.Send("hello"), "sent:sk-live-9:5", "configured key flows through");
""",
                    "Store IConfigProvider; read Get(\"ApiKey\") at send time (or construction).",
                ),
                (
                    "missing key fails fast",
                    r"""
var cfg = new Solution.MemoryConfig();
var sender = new Solution.ReportSender(cfg);
try { sender.Send("hello"); Cj.True(false, "should throw"); }
catch (System.InvalidOperationException ex) { Cj.True(ex.Message.Contains("ApiKey"), "precise failure"); }
""",
                    "Null or empty key -> throw; never substitute a default credential.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p12-env-provider": vi_challenge(
            "Provider môi trường",
            "Dựng provider theo phạm vi prefix trên biến môi trường: Get(name) tra \"<PREFIX>__<NAME>\" (hai gạch dưới), trả null khi chưa đặt. GetInt(name) parse sang int và ném FormatException kèm giá trị gốc khi không phải số. Test điều khiển môi trường ngay trong tiến trình.",
            [
                ("prefix lookup and miss", "Environment.GetEnvironmentVariable(prefix + \"__\" + name)."),
                ("typed access with a precise failure", "int.Parse và để FormatException nổi lên (không bao giờ nuốt giá trị xấu thành 0 im lặng)."),
            ],
        ),
        "csi-p12-options-binding": vi_challenge(
            "Bó JSON thành Options",
            "Bó một section JSON thành lớp options có mặc định: key thiếu giữ mặc định, key có thì ghi đè, Validate() báo TẤT CẢ vấn đề (không chỉ cái đầu) bằng OptionsValidationException với thông điệp \"Retry: <các vấn đề nối bằng '; '>\".",
            [
                ("defaults and overrides", "JsonDocument.Parse; GetProperty(\"Retry\") khi có; chỉ điền các key được cung cấp."),
                ("validation reports everything", "Gom mọi quy tắc vi phạm vào một thông điệp rồi ném một lần."),
            ],
        ),
        "csi-p12-secrets-debug": vi_challenge(
            "Debug: API key cứng trong mã",
            "ReportSender để API key cứng và fallback về nó khi thiếu cấu hình — credential âm thầm vận chuyển tới mọi môi trường, và cấu hình thiếu không bị phát hiện. Sửa: key phải đến từ IConfigProvider, KHÔNG fallback; khi thiếu, ném InvalidOperationException(\"ApiKey is not configured\"). Test dùng MemoryConfig được cấp.",
            [
                ("configured key is used", "Lưu IConfigProvider; đọc Get(\"ApiKey\") lúc gửi (hoặc lúc dựng)."),
                ("missing key fails fast", "Key null hoặc rỗng -> ném; không bao giờ thay bằng credential mặc định."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p12-env-provider",
            'public class Solution\n{\n    public sealed class EnvConfig\n    {\n        private readonly string _prefix;\n\n        public EnvConfig(string prefix) => _prefix = prefix;\n\n        public string? Get(string name)\n        {\n            return System.Environment.GetEnvironmentVariable(_prefix + "__" + name);\n        }\n\n        public int GetInt(string name)\n        {\n            string? raw = Get(name);\n            return int.Parse(raw!);   // throws FormatException with the raw value in the message\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class EnvConfig\n    {\n        private readonly string _prefix;\n\n        public EnvConfig(string prefix) => _prefix = prefix;\n\n        public string? Get(string name)\n        {\n            return System.Environment.GetEnvironmentVariable(_prefix + "_" + name);   // near-miss: single underscore — the CJ__REGION convention never matches\n        }\n\n        public int GetInt(string name)\n        {\n            string? raw = Get(name);\n            if (raw is null) return 0;   // near-miss: silently converts missing config to 0\n            return int.Parse(raw);\n        }\n    }\n}\n',
        ),
        (
            "csi-p12-options-binding",
            'public class Solution\n{\n    public sealed class RetryOptions\n    {\n        public int MaxAttempts { get; set; } = 3;\n        public int DelayMs { get; set; } = 200;\n    }\n\n    public sealed class OptionsBinder\n    {\n        public static RetryOptions Bind(string json)\n        {\n            var options = new RetryOptions();\n            using var doc = System.Text.Json.JsonDocument.Parse(json);\n            if (doc.RootElement.TryGetProperty("Retry", out var section))\n            {\n                if (section.TryGetProperty("MaxAttempts", out var ma))\n                    options.MaxAttempts = ma.GetInt32();\n                if (section.TryGetProperty("DelayMs", out var dm))\n                    options.DelayMs = dm.GetInt32();\n            }\n            return options;\n        }\n\n        public static void Validate(RetryOptions options)\n        {\n            var problems = new System.Collections.Generic.List<string>();\n            if (options.MaxAttempts < 1) problems.Add("MaxAttempts must be >= 1");\n            if (options.DelayMs < 0) problems.Add("DelayMs must be >= 0");\n            if (problems.Count > 0)\n                throw new System.InvalidOperationException("Retry: " + string.Join("; ", problems));\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class RetryOptions\n    {\n        public int MaxAttempts { get; set; } = 3;\n        public int DelayMs { get; set; } = 200;\n    }\n\n    public sealed class OptionsBinder\n    {\n        public static RetryOptions Bind(string json)\n        {\n            // near-miss: GetProperty throws KeyNotFoundException when the\n            // section or a key is absent — the defaults-kept test never runs\n            var options = new RetryOptions();\n            using var doc = System.Text.Json.JsonDocument.Parse(json);\n            var section = doc.RootElement.GetProperty("Retry");\n            options.MaxAttempts = section.GetProperty("MaxAttempts").GetInt32();\n            options.DelayMs = section.GetProperty("DelayMs").GetInt32();\n            return options;\n        }\n\n        public static void Validate(RetryOptions options)\n        {\n            // near-miss: throws on the FIRST violation only — the message\n            // never contains both keys when both are broken\n            if (options.MaxAttempts < 1)\n                throw new System.InvalidOperationException("Retry: MaxAttempts must be >= 1");\n            if (options.DelayMs < 0)\n                throw new System.InvalidOperationException("Retry: DelayMs must be >= 0");\n        }\n    }\n}\n',
        ),
        (
            "csi-p12-secrets-debug",
            'public class Solution\n{\n    public interface IConfigProvider\n    {\n        string? Get(string key);\n    }\n\n    public sealed class MemoryConfig : IConfigProvider\n    {\n        private readonly System.Collections.Generic.Dictionary<string, string> _entries = new();\n\n        public MemoryConfig(params (string Key, string Value)[] entries)\n        {\n            foreach (var (key, value) in entries) _entries[key] = value;\n        }\n\n        public string? Get(string key) => _entries.TryGetValue(key, out var v) ? v : null;\n    }\n\n    public sealed class ReportSender\n    {\n        private readonly IConfigProvider _config;\n\n        public ReportSender(IConfigProvider config) => _config = config;\n\n        public string Send(string report)\n        {\n            string? key = _config.Get("ApiKey");\n            if (string.IsNullOrEmpty(key))\n                throw new System.InvalidOperationException("ApiKey is not configured");\n            return "sent:" + key + ":" + report.Length;\n        }\n    }\n}\n',
            'public class Solution\n{\n    public interface IConfigProvider\n    {\n        string? Get(string key);\n    }\n\n    public sealed class MemoryConfig : IConfigProvider\n    {\n        private readonly System.Collections.Generic.Dictionary<string, string> _entries = new();\n\n        public MemoryConfig(params (string Key, string Value)[] entries)\n        {\n            foreach (var (key, value) in entries) _entries[key] = value;\n        }\n\n        public string? Get(string key) => _entries.TryGetValue(key, out var v) ? v : null;\n    }\n\n    public sealed class ReportSender\n    {\n        private readonly IConfigProvider _config;\n\n        public ReportSender(IConfigProvider config) => _config = config;\n\n        public string Send(string report)\n        {\n            // near-miss: hardcoded fallback credential ships a "real-looking"\n            // key to every environment and hides the missing configuration\n            string key = _config.Get("ApiKey") ?? "sk-dev-fallback-123";\n            return "sent:" + key + ":" + report.Length;\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m12",
    "Checkpoint — The Layered Config Engine",
    "Combine JSON, environment overrides, typed options, and validation into one provider that fails fast and keeps secrets out of code.",
    25,
    r"""
## The gate (mini-build)

A layered configuration engine — the shape every real host uses:

1. `JsonConfig(string json)` — parses `{ "Section": { "Key": "value" } }`;
   `Get("Section:Key")` returns the value or null.
2. `LayeredConfig(IConfigProvider file, string envPrefix)` — looks up env
   first (`envPrefix__SECTION__KEY`, upper-cased, `:` → `__`), then falls
   back to the file provider.
3. `BindRetry(IConfigProvider config)` → typed `RetryOptions` (defaults
   3 / 200) reading `Retry:MaxAttempts` and `Retry:DelayMs` as ints, with
   non-numeric values throwing FormatException.
4. `Validate(RetryOptions)` — MaxAttempts >= 1, DelayMs >= 0; all problems
   in one message: `"Retry: <p1>; <p2>"`.
5. Secrets rule baked in: `Require(config, key)` returns the value or
   throws `InvalidOperationException("Configuration key <key> is required")`
   — no fallbacks.

Provided: `IConfigProvider` / `MemoryConfig` (same as the practice).
""",
    "Checkpoint — Bộ máy cấu hình xếp lớp",
    "Kết hợp JSON, ghi đè môi trường, options có kiểu, và kiểm tra thành một provider fail-fast, giữ bí mật ngoài mã nguồn.",
    r"""
## Cổng kiểm tra (mini-build)

Bộ máy cấu hình xếp lớp — hình dáng mọi host thật dùng:

1. `JsonConfig(string json)` — parse `{ "Section": { "Key": "value" } }`;
   `Get("Section:Key")` trả giá trị hoặc null.
2. `LayeredConfig(IConfigProvider file, string envPrefix)` — tra env TRƯỚC
   (`envPrefix__SECTION__KEY`, viết hoa, `:` → `__`), rồi fallback về
   provider file.
3. `BindRetry(IConfigProvider config)` → `RetryOptions` có kiểu (mặc định
   3 / 200), đọc `Retry:MaxAttempts` và `Retry:DelayMs` dạng int, giá trị
   không phải số ném FormatException.
4. `Validate(RetryOptions)` — MaxAttempts >= 1, DelayMs >= 0; mọi vấn đề
   trong một thông điệp: `"Retry: <p1>; <p2>"`.
5. Quy tắc bí mật có sẵn: `Require(config, key)` trả giá trị hoặc ném
   `InvalidOperationException("Configuration key <key> is required")` —
   không fallback.

Được cấp: `IConfigProvider` / `MemoryConfig` (như phần luyện).
""",
    challenge(
        "csi-checkpoint-m12-task",
        "Checkpoint: Layered Configuration",
        """Implement the config engine described in the checkpoint:

```csharp
static string? GetJson(string json, string key);                    // "Section:Key"
static string? GetLayered(Solution.MemoryConfig file, string envPrefix, string key);
static Solution.RetryOptions BindRetry(Solution.IConfigProvider config);
static void Validate(Solution.RetryOptions options);
static string Require(Solution.IConfigProvider config, string key);
```""",
        CS_PRELUDE,
        [
            (
                "json navigation",
                r"""
string json = "{\"Retry\":{\"MaxAttempts\":4},\"Feature\":\"on\"}";
Cj.Eq(Solution.GetJson(json, "Retry:MaxAttempts"), "4", "nested key");
Cj.Eq(Solution.GetJson(json, "Feature"), "on", "top-level key");
Cj.True(Solution.GetJson(json, "Nope:Nothing") is null, "missing -> null");
""",
                    "JsonDocument.Parse; split on ':' and walk properties; TryGetProperty everywhere.",
                ),
                (
                    "env overrides file",
                    r"""
var file = new Solution.MemoryConfig(("Retry:MaxAttempts", "2"));
System.Environment.SetEnvironmentVariable("CJTEST__RETRY__MAXATTEMPTS", "9");
try
{
    Cj.Eq(Solution.GetLayered(file, "CJTEST", "Retry:MaxAttempts"), "9", "env wins");
    System.Environment.SetEnvironmentVariable("CJTEST__RETRY__MAXATTEMPTS", null);
    Cj.Eq(Solution.GetLayered(file, "CJTEST", "Retry:MaxAttempts"), "2", "file fallback after env cleared");
    Cj.True(Solution.GetLayered(file, "CJTEST", "Retry:DelayMs") is null, "missing everywhere -> null");
}
finally
{
    System.Environment.SetEnvironmentVariable("CJTEST__RETRY__MAXATTEMPTS", null);
}
""",
                    "Env lookup first (uppercase, ':'->'__'), file provider fallback.",
                ),
                (
                    "typed binding and validation",
                    r"""
var cfg = new Solution.MemoryConfig(("Retry:MaxAttempts", "5"));
var opts = Solution.BindRetry(cfg);
Cj.Eq(opts.MaxAttempts, 5, "bound from config");
Cj.Eq(opts.DelayMs, 200, "default kept");
var bad = new Solution.RetryOptions { MaxAttempts = 0, DelayMs = -1 };
try { Solution.Validate(bad); Cj.True(false, "should throw"); }
catch (System.InvalidOperationException ex) { Cj.True(ex.Message.Contains("MaxAttempts") && ex.Message.Contains("DelayMs"), "all problems"); }
try { Solution.Require(cfg, "ApiKey"); Cj.True(false, "should throw"); }
catch (System.InvalidOperationException ex) { Cj.True(ex.Message.Contains("ApiKey"), "secret rule"); }
""",
                    "Bind via Get-style lookup with int.Parse; Validate joins problems; Require throws without fallback.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: Cấu hình xếp lớp",
            "Hiện thực bộ máy: điều hướng JSON theo \"Section:Key\", lớp env ghi đè file (viết hoa, ':'->'__'), bó RetryOptions có kiểu với int.Parse, Validate gom mọi vấn đề, Require ném lỗi khi thiếu key — không fallback.",
            [
                ("json navigation", "JsonDocument.Parse; tách theo ':' và đi từng property; TryGetProperty ở mọi bước."),
                ("env overrides file", "Tra env trước (viết hoa, ':'->'__'), fallback về provider file."),
                ("typed binding and validation", "Bó qua tra cứu kiểu Get với int.Parse; Validate nối các vấn đề; Require ném lỗi, không fallback."),
            ],
        ),
        solution='public class Solution\n{\n    public interface IConfigProvider\n    {\n        string? Get(string key);\n    }\n\n    public sealed class MemoryConfig : IConfigProvider\n    {\n        private readonly System.Collections.Generic.Dictionary<string, string> _entries = new();\n\n        public MemoryConfig(params (string Key, string Value)[] entries)\n        {\n            foreach (var (key, value) in entries) _entries[key] = value;\n        }\n\n        public string? Get(string key) => _entries.TryGetValue(key, out var v) ? v : null;\n    }\n\n    public sealed class RetryOptions\n    {\n        public int MaxAttempts { get; set; } = 3;\n        public int DelayMs { get; set; } = 200;\n    }\n\n    public static string? GetJson(string json, string key)\n    {\n        using var doc = System.Text.Json.JsonDocument.Parse(json);\n        var node = doc.RootElement;\n        foreach (string part in key.Split(\':\'))\n        {\n            if (node.ValueKind != System.Text.Json.JsonValueKind.Object ||\n                !node.TryGetProperty(part, out node))\n                return null;\n        }\n        return node.ToString();\n    }\n\n    public static string? GetLayered(IConfigProvider file, string envPrefix, string key)\n    {\n        string envKey = envPrefix + "__" + key.ToUpperInvariant().Replace(\":\", \"__\");\n        string? fromEnv = System.Environment.GetEnvironmentVariable(envKey);\n        if (fromEnv is not null) return fromEnv;\n        return file.Get(key);\n    }\n\n    public static RetryOptions BindRetry(IConfigProvider config)\n    {\n        var options = new RetryOptions();\n        string? ma = config.Get("Retry:MaxAttempts");\n        if (ma is not null) options.MaxAttempts = int.Parse(ma);\n        string? dm = config.Get("Retry:DelayMs");\n        if (dm is not null) options.DelayMs = int.Parse(dm);\n        return options;\n    }\n\n    public static void Validate(RetryOptions options)\n    {\n        var problems = new System.Collections.Generic.List<string>();\n        if (options.MaxAttempts < 1) problems.Add("MaxAttempts must be >= 1");\n        if (options.DelayMs < 0) problems.Add("DelayMs must be >= 0");\n        if (problems.Count > 0)\n            throw new System.InvalidOperationException("Retry: " + string.Join("; ", problems));\n    }\n\n    public static string Require(IConfigProvider config, string key)\n    {\n        string? value = config.Get(key);\n        if (string.IsNullOrEmpty(value))\n            throw new System.InvalidOperationException("Configuration key " + key + " is required");\n        return value;\n    }\n}\n',
        wrong='public class Solution\n{\n    public interface IConfigProvider\n    {\n        string? Get(string key);\n    }\n\n    public sealed class MemoryConfig : IConfigProvider\n    {\n        private readonly System.Collections.Generic.Dictionary<string, string> _entries = new();\n\n        public MemoryConfig(params (string Key, string Value)[] entries)\n        {\n            foreach (var (key, value) in entries) _entries[key] = value;\n        }\n\n        public string? Get(string key) => _entries.TryGetValue(key, out var v) ? v : null;\n    }\n\n    public sealed class RetryOptions\n    {\n        public int MaxAttempts { get; set; } = 3;\n        public int DelayMs { get; set; } = 200;\n    }\n\n    public static string? GetJson(string json, string key)\n    {\n        using var doc = System.Text.Json.JsonDocument.Parse(json);\n        var node = doc.RootElement;\n        foreach (string part in key.Split(\':\'))\n        {\n            if (node.ValueKind != System.Text.Json.JsonValueKind.Object ||\n                !node.TryGetProperty(part, out node))\n                return null;\n        }\n        return node.ToString();\n    }\n\n    public static string? GetLayered(IConfigProvider file, string envPrefix, string key)\n    {\n        // near-miss: checks the FILE first, env second — environment\n        // overrides never win and the layering test sees the file value\n        string? fromFile = file.Get(key);\n        if (fromFile is not null) return fromFile;\n        string envKey = envPrefix + "__" + key.ToUpperInvariant().Replace(\":\", \"__\");\n        return System.Environment.GetEnvironmentVariable(envKey);\n    }\n\n    public static RetryOptions BindRetry(IConfigProvider config)\n    {\n        var options = new RetryOptions();\n        string? ma = config.Get("Retry:MaxAttempts");\n        if (ma is not null) options.MaxAttempts = int.Parse(ma);\n        string? dm = config.Get("Retry:DelayMs");\n        if (dm is not null) options.DelayMs = int.Parse(dm);\n        return options;\n    }\n\n    public static void Validate(RetryOptions options)\n    {\n        var problems = new System.Collections.Generic.List<string>();\n        if (options.MaxAttempts < 1) problems.Add("MaxAttempts must be >= 1");\n        if (options.DelayMs < 0) problems.Add("DelayMs must be >= 0");\n        if (problems.Count > 0)\n            throw new System.InvalidOperationException("Retry: " + string.Join("; ", problems));\n    }\n\n    public static string Require(IConfigProvider config, string key)\n    {\n        // near-miss: hardcoded fallback credential — the required-key rule\n        // (and the secret discipline) is silently broken\n        return config.Get(key) ?? "missing-but-secret-default";\n    }\n}\n',
    )
print("module 12 authored")
