#!/usr/bin/env python3
"""C# — Intermediate — Module 13: csi-http.

HTTP & API clients over HttpClient with DETERMINISTIC literal handlers
(HttpMessageHandler stubs — no network in the sandbox): request anatomy,
status-code handling, HttpClient lifetime, retries with backoff, and
cancellation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csi import (
    write_module, write_lesson, write_practice, write_checkpoint,
    challenge, vi_challenge, CS_PRELUDE, CJ_STUB_HANDLER,
)

M = "csi-http"

HTTP_PRELUDE = CS_PRELUDE + (
    "using System.Net;\n"
    "using System.Net.Http;\n"
    "using System.Threading;\n"
    "using System.Threading.Tasks;\n"
)

write_module(
    M,
    "HTTP & API Clients",
    "Requests, responses, status codes, and resilient clients — deterministic hands-on with a literal HttpMessageHandler.",
    "HTTP & API Client",
    "Request, response, mã trạng thái, và client bền bỉ — thực hành xác định qua HttpMessageHandler literal.",
    ["http-anatomy", "resilient-clients", "csi-checkpoint-m13"],
    ["csi-p13-http"],
)

# ---------------------------------------------------------------- lesson 1
write_lesson(
    M, "http-anatomy",
    "HTTP Anatomy and HttpClient",
    "Methods, status codes, headers, and how HttpClient carries a request through a handler pipeline.",
    18,
    r"""
## The request/response contract

A request = method (GET reads, POST creates/submits, PUT replaces, DELETE
removes) + URL + headers + optional body. A response = status code + headers
+ optional body. The codes you must internalize:

- 2xx success (200 OK, 201 Created — response carries the new resource,
  204 No Content — success with an empty body),
- 4xx the CALLER's problem (400 bad input, 401 unauthenticated,
  403 unauthorized, 404 missing, 409 conflict, 429 rate-limited),
- 5xx the SERVER's problem (500, 502, 503).

The rule: 4xx usually means fix your request; 5xx means the other side had
a bad day — that's the one you retry.

## HttpClient: create once, use everywhere

```csharp
public sealed class ApiClient
{
    private readonly HttpClient _http;
    public ApiClient(HttpClient http) => _http = http;   // injected

    public async Task<string> GetNameAsync(int id, CancellationToken ct)
    {
        using var resp = await _http.GetAsync($"/names/{id}", ct);
        resp.EnsureSuccessStatusCode();
        return await resp.Content.ReadAsStringAsync(ct);
    }
}
```

One client per APP lifetime (it pools connections); new-per-call sockets
exhaust the connection pool. Inject it (Module 11) or use a typed client.

## Handlers: the pipeline

HttpClient sends requests through an `HttpMessageHandler` chain — each
handler transforms or observes the request/response. That's where logging,
auth headers, retries, and stubs live:

```csharp
public sealed class StubHandler : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage req, CancellationToken ct)
        => Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent("{ \"ok\": true }")
        });
}

var http = new HttpClient(new StubHandler()) { BaseAddress = new Uri("https://api.test") };
```

## Check your understanding

- Which status says "you sent something wrong"? (4xx — e.g. 400/404/429.)
- Why not `new HttpClient()` per call? (Socket exhaustion — pool per app, inject one.)
""",
    "HTTP và HttpClient",
    "Method, mã trạng thái, header, và cách HttpClient đưa request qua pipeline handler.",
    r"""
## Hợp đồng request/response

Request = method (GET đọc, POST tạo/gửi, PUT thay thế, DELETE xóa) + URL +
header + body tùy chọn. Response = mã trạng thái + header + body tùy chọn.
Các mã cần thuộc:

- 2xx thành công (200 OK, 201 Created — response mang tài nguyên mới,
  204 No Content — thành công với body rỗng),
- 4xx lỗi của NGƯỜI GỌI (400 đầu vào sai, 401 chưa xác thực,
  403 không đủ quyền, 404 không có, 409 xung đột, 429 bị giới hạn),
- 5xx lỗi của SERVER (500, 502, 503).

Quy tắc: 4xx thường nghĩa là sửa request của bạn; 5xx nghĩa là bên kia gặp
ngày xấu — mới là thứ đáng thử lại.

## HttpClient: tạo một lần, dùng khắp nơi

```csharp
public sealed class ApiClient
{
    private readonly HttpClient _http;
    public ApiClient(HttpClient http) => _http = http;   // injected

    public async Task<string> GetNameAsync(int id, CancellationToken ct)
    {
        using var resp = await _http.GetAsync($"/names/{id}", ct);
        resp.EnsureSuccessStatusCode();
        return await resp.Content.ReadAsStringAsync(ct);
    }
}
```

Một client cho MỌI tuổi thọ app (nó gom nối kết); tạo-mới-mỗi-lần cạn sạch
pool socket. Hãy inject (Module 11) hoặc dùng typed client.

## Handler: pipeline

HttpClient gửi request qua chuỗi `HttpMessageHandler` — mỗi handler biến
đổi hoặc quan sát request/response. Logging, auth header, retry, và stub
đều sống ở đó:

```csharp
public sealed class StubHandler : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage req, CancellationToken ct)
        => Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent("{ \"ok\": true }")
        });
}

var http = new HttpClient(new StubHandler()) { BaseAddress = new Uri("https://api.test") };
```

## Kiểm tra hiểu biết

- Mã nào nói "bạn gửi sai"? (4xx — ví dụ 400/404/429.)
- Vì sao không `new HttpClient()` mỗi lần gọi? (Cạn socket — pool theo app, inject một cái.)
""",
    r"""
## Hợp đồng request/response

Request = method (GET đọc, POST tạo/gửi, PUT thay thế, DELETE xóa) + URL +
header + body tùy chọn. Response = mã trạng thái + header + body tùy chọn.
Các mã cần thuộc:

- 2xx thành công (200 OK, 201 Created — response mang tài nguyên mới,
  204 No Content — thành công với body rỗng),
- 4xx lỗi của NGƯỜI GỌI (400 đầu vào sai, 401 chưa xác thực,
  403 không đủ quyền, 404 không có, 409 xung đột, 429 bị giới hạn),
- 5xx lỗi của SERVER (500, 502, 503).

Quy tắc: 4xx thường nghĩa là sửa request của bạn; 5xx nghĩa là bên kia gặp
ngày xấu — mới là thứ đáng thử lại.

## HttpClient: tạo một lần, dùng khắp nơi

```csharp
public sealed class ApiClient
{
    private readonly HttpClient _http;
    public ApiClient(HttpClient http) => _http = http;   // injected

    public async Task<string> GetNameAsync(int id, CancellationToken ct)
    {
        using var resp = await _http.GetAsync($"/names/{id}", ct);
        resp.EnsureSuccessStatusCode();
        return await resp.Content.ReadAsStringAsync(ct);
    }
}
```

Một client cho MỌI tuổi thọ app (nó gom nối kết); tạo-mới-mỗi-lần cạn sạch
pool socket. Hãy inject (Module 11) hoặc dùng typed client.

## Handler: pipeline

HttpClient gửi request qua chuỗi `HttpMessageHandler` — mỗi handler biến
đổi hoặc quan sát request/response. Logging, auth header, retry, và stub
đều sống ở đó:

```csharp
public sealed class StubHandler : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage req, CancellationToken ct)
        => Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent("{ \"ok\": true }")
        });
}

var http = new HttpClient(new StubHandler()) { BaseAddress = new Uri("https://api.test") };
```

## Kiểm tra hiểu biết

- Mã nào nói "bạn gửi sai"? (4xx — ví dụ 400/404/429.)
- Vì sao không `new HttpClient()` mỗi lần gọi? (Cạn socket — pool theo app, inject một cái.)
""",
)

# ---------------------------------------------------------------- lesson 2
write_lesson(
    M, "resilient-clients",
    "Error Handling, Timeouts, and Retries",
    "Map status codes to typed outcomes, time-box calls, and retry only what's safe to retry.",
    17,
    r"""
## Typed outcomes, not exceptions for flow control

`EnsureSuccessStatusCode()` throws HttpRequestException for ANY failure —
you lose the status distinction. Map outcomes explicitly:

```csharp
public sealed record ApiResult(bool Ok, string? Body, int Status);

public async Task<ApiResult> GetAsync(string path, CancellationToken ct)
{
    using var resp = await _http.GetAsync(path, ct);
    string body = resp.IsSuccessStatusCode
        ? await resp.Content.ReadAsStringAsync(ct) : null;
    return new ApiResult(resp.IsSuccessStatusCode, body, (int)resp.StatusCode);
}
```

## Timeouts and cancellation

`CancellationToken` aborts the wait from the caller's side; HttpClient's
`Timeout` (default 100 s) bounds the whole request. A timeout surfaces as
TaskCanceledException/OperationCanceledException — catch both deliberately.

## Retries: only transient, only safe

Retry 5xx and network failures; NEVER retry 4xx (your request is wrong —
retrying hammers the server with the same mistake). Respect 429's
`Retry-After` when present. Add exponential backoff with a cap, and make
the token flow so cancellation still wins:

```csharp
for (int attempt = 1; ; attempt++)
{
    try { return await SendOnceAsync(ct); }
    catch (HttpRequestException) when (attempt < maxAttempts) { }
    await Task.Delay(Math.Min(baseMs * (1 << (attempt - 1)), capMs), ct);
}
```

Retrying a non-idempotent POST (payments!) can double-charge — safety is
about the operation's semantics, not just the status code.

## Check your understanding

- Why not retry a 400? (The request is wrong; a retry repeats it.)
- What does `1 << (attempt - 1)` build? (Exponential backoff: 1x, 2x, 4x…)
""",
    "Xử lý lỗi, Timeout, và Retry",
    "Đổi mã trạng thái thành kết quả có kiểu, time-box lời gọi, và chỉ retry thứ an toàn để retry.",
    r"""
## Kết quả có kiểu, không dùng exception làm luồng điều khiển

`EnsureSuccessStatusCode()` ném HttpRequestException cho MỌI thất bại — bạn
mất sự phân biệt mã trạng thái. Map kết quả tường minh:

```csharp
public sealed record ApiResult(bool Ok, string? Body, int Status);

public async Task<ApiResult> GetAsync(string path, CancellationToken ct)
{
    using var resp = await _http.GetAsync(path, ct);
    string body = resp.IsSuccessStatusCode
        ? await resp.Content.ReadAsStringAsync(ct) : null;
    return new ApiResult(resp.IsSuccessStatusCode, body, (int)resp.StatusCode);
}
```

## Timeout và hủy

`CancellationToken` hủy từ phía caller; `Timeout` của HttpClient (mặc định
100 s) giới hạn cả request. Timeout nổi lên dưới dạng
TaskCanceledException/OperationCanceledException — bắt cả hai một cách chủ
động.

## Retry: chỉ tạm thời, chỉ an toàn

Retry 5xx và lỗi mạng; KHÔNG BAO GIỜ retry 4xx (request của bạn sai — retry
là đập thêm vào server cùng một lỗi). Tôn trọng `Retry-After` của 429 khi
có. Thêm backoff nhân bản có trần, và giữ token chảy để hủy vẫn thắng:

```csharp
for (int attempt = 1; ; attempt++)
{
    try { return await SendOnceAsync(ct); }
    catch (HttpRequestException) when (attempt < maxAttempts) { }
    await Task.Delay(Math.Min(baseMs * (1 << (attempt - 1)), capMs), ct);
}
```

Retry một POST không idempotent (thanh toán!) có thể tính tiền hai lần — độ
an toàn nằm ở ngữ nghĩa thao tác, không chỉ mã trạng thái.

## Kiểm tra hiểu biết

- Vì sao không retry 400? (Request sai; retry là lặp lại nó.)
- `1 << (attempt - 1)` dựng cái gì? (Backoff nhân bản: 1x, 2x, 4x…)
""",
    r"""
## Kết quả có kiểu, không dùng exception làm luồng điều khiển

`EnsureSuccessStatusCode()` ném HttpRequestException cho MỌI thất bại — bạn
mất sự phân biệt mã trạng thái. Map kết quả tường minh:

```csharp
public sealed record ApiResult(bool Ok, string? Body, int Status);

public async Task<ApiResult> GetAsync(string path, CancellationToken ct)
{
    using var resp = await _http.GetAsync(path, ct);
    string body = resp.IsSuccessStatusCode
        ? await resp.Content.ReadAsStringAsync(ct) : null;
    return new ApiResult(resp.IsSuccessStatusCode, body, (int)resp.StatusCode);
}
```

## Timeout và hủy

`CancellationToken` hủy từ phía caller; `Timeout` của HttpClient (mặc định
100 s) giới hạn cả request. Timeout nổi lên dưới dạng
TaskCanceledException/OperationCanceledException — bắt cả hai một cách chủ
động.

## Retry: chỉ tạm thời, chỉ an toàn

Retry 5xx và lỗi mạng; KHÔNG BAO GIỜ retry 4xx (request của bạn sai — retry
là đập thêm vào server cùng một lỗi). Tôn trọng `Retry-After` của 429 khi
có. Thêm backoff nhân bản có trần, và giữ token chảy để hủy vẫn thắng:

```csharp
for (int attempt = 1; ; attempt++)
{
    try { return await SendOnceAsync(ct); }
    catch (HttpRequestException) when (attempt < maxAttempts) { }
    await Task.Delay(Math.Min(baseMs * (1 << (attempt - 1)), capMs), ct);
}
```

Retry một POST không idempotent (thanh toán!) có thể tính tiền hai lần — độ
an toàn nằm ở ngữ nghĩa thao tác, không chỉ mã trạng thái.

## Kiểm tra hiểu biết

- Vì sao không retry 400? (Request sai; retry là lặp lại nó.)
- `1 << (attempt - 1)` dựng cái gì? (Backoff nhân bản: 1x, 2x, 4x…)
""",
)

# ---------------------------------------------------------------- practice
write_practice(
    M,
    "csi-p13-http",
    "HTTP Practice: Handlers, Outcomes, Retries",
    "Drive HttpClient through literal handlers, map statuses to typed results, and build a backoff retry loop.",
    "Luyện HTTP: Handler, Kết quả, Retry",
    "Điều khiển HttpClient qua handler literal, đổi mã trạng thái thành kết quả có kiểu, và dựng vòng retry backoff.",
    "resilient-clients",
    32,
    "intermediate",
    [
        challenge(
            "csi-p13-status-outcomes",
            "Status Codes to Typed Outcomes",
            """Implement GetOutcomeAsync over an injected HttpClient (stubbed by the harness): return "data:<body>" for 2xx, "notfound" for 404, "servererror" for any 5xx, "forbidden" for 403. Anything else 4xx -> "error:<code>".

```csharp
static Task<string> GetOutcomeAsync(HttpClient http, string path, CancellationToken ct = default);
```""",
            HTTP_PRELUDE + CJ_STUB_HANDLER,
            [
                (
                    "success and mapped failures",
                    r"""
var script = new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>
{
    ["/ok"] = CjStubHandler.One(CjStubHandler.Json(200, "hello")),
    ["/missing"] = CjStubHandler.One(CjStubHandler.Json(404, "")),
    ["/boom"] = CjStubHandler.One(CjStubHandler.Json(500, "")),
    ["/denied"] = CjStubHandler.One(CjStubHandler.Json(403, "")),
    ["/busy"] = CjStubHandler.One(CjStubHandler.Json(429, "")),
};
var http = new System.Net.Http.HttpClient(new CjStubHandler(script)) { BaseAddress = new System.Uri("https://api.test") };
Cj.Eq(Solution.GetOutcomeAsync(http, "/ok").GetAwaiter().GetResult(), "data:hello", "2xx carries body");
Cj.Eq(Solution.GetOutcomeAsync(http, "/missing").GetAwaiter().GetResult(), "notfound", "404 mapped");
Cj.Eq(Solution.GetOutcomeAsync(http, "/boom").GetAwaiter().GetResult(), "servererror", "5xx mapped");
Cj.Eq(Solution.GetOutcomeAsync(http, "/denied").GetAwaiter().GetResult(), "forbidden", "403 mapped");
Cj.Eq(Solution.GetOutcomeAsync(http, "/busy").GetAwaiter().GetResult(), "error:429", "other 4xx -> error:<code>");
""",
                    "Check (int)resp.StatusCode or the enum; branch BEFORE EnsureSuccess-style throwing.",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p13-request-shape",
            "The POST That Carries Its Headers",
            """Implement PostJsonAsync: POST the given JSON body to the path with Content-Type application/json and header X-Trace: <traceId>. The stub records the request — verify method, path, content-type header, and the X-Trace header all arrived.

```csharp
static Task PostJsonAsync(HttpClient http, string path, string json, string traceId, CancellationToken ct = default);
```""",
            HTTP_PRELUDE + CJ_STUB_HANDLER,
            [
                (
                    "method, headers, body arrive intact",
                    r"""
var http = CjStubHandler.Recording();
Solution.PostJsonAsync(http, "/orders", "{\"id\":7}", "trace-42").GetAwaiter().GetResult();
var req = CjStubHandler.LastRequest!;
Cj.Eq(req.Method.Method, "POST", "POST used");
Cj.Eq(req.RequestUri!.PathAndQuery, "/orders", "path preserved");
Cj.True(req.Content!.Headers.ContentType!.MediaType.Contains("json"), "json content type");
Cj.True(string.Join(",", req.Headers.GetValues("X-Trace")) == "trace-42", "trace header set");
Cj.True(req.Content.ReadAsStringAsync(System.Threading.CancellationToken.None).GetAwaiter().GetResult().Contains("7"), "body intact");
""",
                    "new StringContent(json, Encoding.UTF8, \"application/json\"); req.Headers.Add(\"X-Trace\", traceId).",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p13-retry-backoff",
            "Retry with Backoff",
            """Implement GetWithRetryAsync: up to maxAttempts attempts; retry on 5xx responses and HttpRequestException; NEVER retry other statuses. Delay between attempts with backoff (baseMs << (attempt-1), capped at capMs — the harness provides a fake async delay recorder). Return the first success; after exhausting attempts return "failed".

```csharp
static Task<string> GetWithRetryAsync(HttpClient http, string path, int maxAttempts, int baseMs, int capMs, CancellationToken ct = default);
```""",
            HTTP_PRELUDE + CJ_STUB_HANDLER,
            [
                (
                    "retries 5xx then succeeds",
                    r"""
var script = new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>
{
    ["/flaky"] = CjStubHandler.Sequence(
        CjStubHandler.Json(500, ""),
        CjStubHandler.Json(200, "recovered")),
};
var http = new System.Net.Http.HttpClient(new CjStubHandler(script)) { BaseAddress = new System.Uri("https://api.test") };
Cj.Eq(Solution.GetWithRetryAsync(http, "/flaky", 3, 10, 100).GetAwaiter().GetResult(), "recovered", "second attempt wins");
""",
                    "Loop attempts; on 5xx (or HttpRequestException) delay with baseMs << (attempt-1) then continue.",
                ),
                (
                    "4xx is never retried",
                    r"""
var script = new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>
{
    ["/wrong"] = CjStubHandler.Sequence(CjStubHandler.Json(400, ""), CjStubHandler.Json(200, "lucky")),
};
var http = new System.Net.Http.HttpClient(new CjStubHandler(script)) { BaseAddress = new System.Uri("https://api.test") };
Cj.Eq(Solution.GetWithRetryAsync(http, "/wrong", 5, 10, 100).GetAwaiter().GetResult(), "failed", "a 400 must NOT get a second chance");
""",
                    "Non-retryable status -> return \"failed\" immediately (no delay, one call).",
                ),
                (
                    "backoff grows and caps",
                    r"""
var script = new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>
{
    ["/down"] = CjStubHandler.Always(CjStubHandler.Json(503, "")),
};
var http = new System.Net.Http.HttpClient(new CjStubHandler(script)) { BaseAddress = new System.Uri("https://api.test") };
Solution.GetWithRetryAsync(http, "/down", 4, 10, 25).GetAwaiter().GetResult();
var delays = CjStubHandler.Delays;
Cj.True(delays.Count >= 3, "three waits between four attempts");
Cj.True(delays[0] <= delays[1] && delays[1] <= delays[2], "non-decreasing");
Cj.True(delays[2] <= 25, "capped at capMs");
""",
                    "Math.Min(baseMs << (attempt-1), capMs) — 10, 20, 25(cap), …",
                ),
            ],
            level="guided",
            difficulty="intermediate",
        ),
        challenge(
            "csi-p13-lifetime-debug",
            "Debug: The Client Flood",
            """SiteClient news up an HttpClient per call — the graded harness caps sockets and the flood fails. Fix the lifetime: one client for the client object's whole life (injected or lazily created), all calls reuse it.

```csharp
public sealed class SiteClient
{
    public string Fetch(string path);   // fix: reuse ONE HttpClient
}
```""",
            HTTP_PRELUDE + CJ_STUB_HANDLER,
            [
                (
                    "one client, many calls",
                    r"""
int before = CjStubHandler.HandlerCount;
var client = new Solution.SiteClient();
Cj.Eq(client.Fetch("/a"), "data:a", "first call works");
Cj.Eq(client.Fetch("/b"), "data:b", "second call works");
Cj.Eq(client.Fetch("/c"), "data:c", "third call works");
Cj.True(CjStubHandler.HandlerCount - before <= 1, "handler (and its client) created at most once");
""",
                    "Create the HttpClient once (constructor or lazy field); every Fetch reuses it.",
                ),
            ],
            level="debugging",
            difficulty="intermediate",
        ),
    ],
    {
        "csi-p13-status-outcomes": vi_challenge(
            "Mã trạng thái thành kết quả có kiểu",
            "Hiện thực GetOutcomeAsync trên HttpClient được inject (stub bởi harness): trả \"data:<body>\" cho 2xx, \"notfound\" cho 404, \"servererror\" cho 5xx, \"forbidden\" cho 403. 4xx khác -> \"error:<code>\".",
            [
                ("success and mapped failures", "Xem (int)resp.StatusCode hoặc enum; rẽ nhánh TRƯỚC kiểu EnsureSuccess-ném-lỗi."),
            ],
        ),
        "csi-p13-request-shape": vi_challenge(
            "POST mang theo header của nó",
            "Hiện thực PostJsonAsync: POST body JSON tới path với Content-Type application/json và header X-Trace: <traceId>. Stub ghi lại request — kiểm chứng method, path, content-type header, và header X-Trace.",
            [
                ("method, headers, body arrive intact", "new StringContent(json, Encoding.UTF8, \"application/json\"); req.Headers.Add(\"X-Trace\", traceId)."),
            ],
        ),
        "csi-p13-retry-backoff": vi_challenge(
            "Retry với Backoff",
            "Hiện thực GetWithRetryAsync: tối đa maxAttempts lần; retry khi 5xx và HttpRequestException; KHÔNG retry các mã khác. Delay giữa các lần với backoff (baseMs << (attempt-1), trần capMs — harness cấp bộ ghi delay giả). Trả thành công đầu tiên; hết lượt trả \"failed\".",
            [
                ("retries 5xx then succeeds", "Vòng attempt; gặp 5xx (hoặc HttpRequestException) delay baseMs << (attempt-1) rồi tiếp tục."),
                ("4xx is never retried", "Mã không-retryable -> trả \"failed\" ngay (không delay, một lần gọi)."),
                ("backoff grows and caps", "Math.Min(baseMs << (attempt-1), capMs) — 10, 20, 25(trần), …"),
            ],
        ),
        "csi-p13-lifetime-debug": vi_challenge(
            "Debug: Thủy triều client",
            "SiteClient new HttpClient cho mỗi lần gọi — harness giới hạn socket và cơn thủy triều thất bại. Sửa lifetime: một client cho cả tuổi thọ đối tượng (inject hoặc tạo lười), mọi lời gọi dùng chung.",
            [
                ("one client, many calls", "Tạo HttpClient đúng một lần (constructor hoặc field lười); mọi Fetch tái sử dụng."),
            ],
        ),
    },
    solutions=[
        (
            "csi-p13-status-outcomes",
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task<string> GetOutcomeAsync(\n        System.Net.Http.HttpClient http, string path,\n        System.Threading.CancellationToken ct = default)\n    {\n        using var resp = await http.GetAsync(path, ct);\n        int code = (int)resp.StatusCode;\n        if (resp.IsSuccessStatusCode)\n            return "data:" + await resp.Content.ReadAsStringAsync(ct);\n        if (code == 404) return "notfound";\n        if (code == 403) return "forbidden";\n        if (code >= 500) return "servererror";\n        return "error:" + code;\n    }\n}\n',
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task<string> GetOutcomeAsync(\n        System.Net.Http.HttpClient http, string path,\n        System.Threading.CancellationToken ct = default)\n    {\n        using var resp = await http.GetAsync(path, ct);\n        int code = (int)resp.StatusCode;\n        // near-miss: throws on everything non-2xx before mapping — the 404\n        // branch is unreachable and the tests see HttpRequestException\n        resp.EnsureSuccessStatusCode();\n        if (code == 404) return "notfound";\n        if (code == 403) return "forbidden";\n        if (code >= 500) return "servererror";\n        return "error:" + code;\n    }\n}\n',
        ),
        (
            "csi-p13-request-shape",
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task PostJsonAsync(\n        System.Net.Http.HttpClient http, string path, string json, string traceId,\n        System.Threading.CancellationToken ct = default)\n    {\n        var content = new System.Net.Http.StringContent(\n            json, System.Text.Encoding.UTF8, "application/json");\n        using var req = new System.Net.Http.HttpRequestMessage(\n            System.Net.Http.HttpMethod.Post, path) { Content = content };\n        req.Headers.Add("X-Trace", traceId);\n        await http.SendAsync(req, ct);\n    }\n}\n',
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task PostJsonAsync(\n        System.Net.Http.HttpClient http, string path, string json, string traceId,\n        System.Threading.CancellationToken ct = default)\n    {\n        var content = new System.Net.Http.StringContent(\n            json, System.Text.Encoding.UTF8, "application/json");\n        using var req = new System.Net.Http.HttpRequestMessage(\n            System.Net.Http.HttpMethod.Post, path) { Content = content };\n        // near-miss: adds the trace header to the CONTENT headers — request\n        // headers live on req.Headers, so the X-Trace assertion fails\n        req.Content.Headers.Add("X-Trace", traceId);\n        await http.SendAsync(req, ct);\n    }\n}\n',
        ),
        (
            "csi-p13-retry-backoff",
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task<string> GetWithRetryAsync(\n        System.Net.Http.HttpClient http, string path,\n        int maxAttempts, int baseMs, int capMs,\n        System.Threading.CancellationToken ct = default)\n    {\n        for (int attempt = 1; ; attempt++)\n        {\n            try\n            {\n                using var resp = await http.GetAsync(path, ct);\n                int code = (int)resp.StatusCode;\n                if (resp.IsSuccessStatusCode)\n                    return await resp.Content.ReadAsStringAsync(ct);\n                if (code < 500 || attempt >= maxAttempts)\n                    return "failed";\n            }\n            catch (System.Net.Http.HttpRequestException)\n            {\n                if (attempt >= maxAttempts) return "failed";\n            }\n            await CjStubHandler.DelayAsync(\n                System.Math.Min(baseMs << (attempt - 1), capMs), ct);\n        }\n    }\n}\n',
            'public class Solution\n{\n    public static async System.Threading.Tasks.Task<string> GetWithRetryAsync(\n        System.Net.Http.HttpClient http, string path,\n        int maxAttempts, int baseMs, int capMs,\n        System.Threading.CancellationToken ct = default)\n    {\n        for (int attempt = 1; ; attempt++)\n        {\n            try\n            {\n                using var resp = await http.GetAsync(path, ct);\n                int code = (int)resp.StatusCode;\n                if (resp.IsSuccessStatusCode)\n                    return await resp.Content.ReadAsStringAsync(ct);\n                // near-miss: retries EVERYTHING including 4xx — the 400 path\n                // burns all five attempts and the no-retry test fails\n            }\n            catch (System.Net.Http.HttpRequestException)\n            {\n                if (attempt >= maxAttempts) return "failed";\n            }\n            if (attempt >= maxAttempts) return "failed";\n            await CjStubHandler.DelayAsync(\n                System.Math.Min(baseMs << (attempt - 1), capMs), ct);\n        }\n    }\n}\n',
        ),
        (
            "csi-p13-lifetime-debug",
            'public class Solution\n{\n    public sealed class SiteClient\n    {\n        private readonly System.Net.Http.HttpClient _http =\n            new System.Net.Http.HttpClient(new CjStubHandler(\n                new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>(),\n                data: true))\n            { BaseAddress = new System.Uri("https://api.test") };\n\n        public string Fetch(string path)\n        {\n            return _http.GetStringAsync(path).GetAwaiter().GetResult();\n        }\n    }\n}\n',
            'public class Solution\n{\n    public sealed class SiteClient\n    {\n        // near-miss: a fresh HttpClient per call — the socket-flood guard trips\n        // on the third call and the created-clients test fails\n        public string Fetch(string path)\n        {\n            using var http = new System.Net.Http.HttpClient(new CjStubHandler(\n                new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>(),\n                data: true))\n            { BaseAddress = new System.Uri("https://api.test") };\n            return http.GetStringAsync(path).GetAwaiter().GetResult();\n        }\n    }\n}\n',
        ),
    ],
)

# ---------------------------------------------------------------- checkpoint
write_checkpoint(
    M,
    "csi-checkpoint-m13",
    "Checkpoint — The Public API Client",
    "Compose the pieces: typed client over a stub handler, mapped outcomes, retries with capped backoff, cancellation honored.",
    25,
    r"""
## The gate (mini-build)

A resilient API client — the shape from the lesson, assembled:

1. `ApiClient(HttpClient http)` — injected client (Module 11 discipline).
2. `GetUserAsync(int id, CancellationToken ct)` → GET `/users/{id}`.
   Outcomes: `"user:<name>"` on 200, `"notfound"` on 404,
   `"failed"` on any other status.
3. `GetUserWithRetryAsync(int id, int maxAttempts, CancellationToken ct)` —
   same contract, but 5xx attempts are retried with the harness's recorded
   delays (non-decreasing, capped at 50 ms); 404 is NOT retried.
4. Cancellation wins: a pre-cancelled token throws
   OperationCanceledException before any request.

Provided: `CjStubHandler` (records requests, replays scripted responses,
records fake delays).
""",
    "Checkpoint — API client công khai",
    "Ghép các mảnh: typed client trên stub handler, kết quả có kiểu, retry backoff có trần, tôn trọng hủy.",
    r"""
## Cổng kiểm tra (mini-build)

API client bền bỉ — hình dáng trong bài học, lắp ráp:

1. `ApiClient(HttpClient http)` — client được inject (kỷ luật Module 11).
2. `GetUserAsync(int id, CancellationToken ct)` → GET `/users/{id}`.
   Kết quả: `"user:<name>"` khi 200, `"notfound"` khi 404,
   `"failed"` với mã khác.
3. `GetUserWithRetryAsync(int id, int maxAttempts, CancellationToken ct)` —
   cùng hợp đồng, nhưng lần 5xx được retry với delay do harness ghi lại
   (không giảm, trần 50 ms); 404 KHÔNG được retry.
4. Hủy thắng: token đã hủy trước ném OperationCanceledException trước mọi
   request.

Được cấp: `CjStubHandler` (ghi request, phát lại response kịch bản, ghi
delay giả).
""",
    challenge(
        "csi-checkpoint-m13-task",
        "Checkpoint: Resilient API Client",
        """Implement the client described in the checkpoint:

```csharp
public sealed class ApiClient
{
    public ApiClient(System.Net.Http.HttpClient http);
    public Task<string> GetUserAsync(int id, CancellationToken ct = default);
    public Task<string> GetUserWithRetryAsync(int id, int maxAttempts, CancellationToken ct = default);
}
```""",
        HTTP_PRELUDE + CJ_STUB_HANDLER,
        [
            (
                "success and notfound",
                r"""
var script = new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>
{
    ["/users/1"] = new System.Collections.Generic.List<System.Net.Http.HttpResponseMessage> { CjStubHandler.Json(200, "{\"name\":\"ada\"}") },
    ["/users/404"] = CjStubHandler.One(CjStubHandler.Json(404, "")),
};
var http = new System.Net.Http.HttpClient(new CjStubHandler(script)) { BaseAddress = new System.Uri("https://api.test") };
var client = new Solution.ApiClient(http);
Cj.True(client.GetUserAsync(1).GetAwaiter().GetResult().StartsWith("user:"), "200 -> user:<name>");
Cj.Eq(client.GetUserAsync(404).GetAwaiter().GetResult(), "notfound", "404 mapped");
""",
                    "Branch on status before reading body; never let EnsureSuccess throw.",
                ),
                (
                    "retry on 5xx only, capped delays",
                    r"""
var script = new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>
{
    ["/users/5"] = new System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>
    {
        CjStubHandler.Json(500, ""),
        CjStubHandler.Json(500, ""),
        CjStubHandler.Json(200, "{\"name\":\"bob\"}"),
    },
    ["/users/6"] = new System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>
    {
        CjStubHandler.Json(404, ""),
        CjStubHandler.Json(200, "{\"name\":\"eve\"}"),
    },
};
var http = new System.Net.Http.HttpClient(new CjStubHandler(script)) { BaseAddress = new System.Uri("https://api.test") };
var client = new Solution.ApiClient(http);
Cj.True(client.GetUserWithRetryAsync(5, 3).GetAwaiter().GetResult().StartsWith("user:"), "third attempt wins");
Cj.Eq(client.GetUserWithRetryAsync(6, 3).GetAwaiter().GetResult(), "notfound", "404 not retried");
var delays = CjStubHandler.Delays;
Cj.True(delays.Count >= 2 && delays.TrueForAll(d => d <= 50), "delays recorded and capped");
""",
                    "Retry only 5xx; delays via CjStubHandler.DelayAsync(min(10 << (attempt-1), 50)).",
                ),
                (
                    "cancellation wins",
                    r"""
var script = new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<System.Net.Http.HttpResponseMessage>>();
var http = new System.Net.Http.HttpClient(new CjStubHandler(script)) { BaseAddress = new System.Uri("https://api.test") };
var client = new Solution.ApiClient(http);
var cts = new System.Threading.CancellationTokenSource();
cts.Cancel();
try { client.GetUserAsync(1, cts.Token).GetAwaiter().GetResult(); Cj.True(false, "should cancel"); }
catch (System.OperationCanceledException) { }
""",
                    "ct.ThrowIfCancellationRequested() before sending — and pass ct to SendAsync.",
                ),
            ],
            difficulty="intermediate",
        ),
        vi_challenge(
            "Checkpoint: API client bền bỉ",
            "Hiện thực client: inject HttpClient; GetUserAsync map 200→\"user:<name>\", 404→\"notfound\", khác→\"failed\"; GetUserWithRetryAsync chỉ retry 5xx với delay không giảm trần 50 ms; 404 không retry; token đã hủy ném OperationCanceledException trước mọi request.",
            [
                ("success and notfound", "Rẽ nhánh theo mã trạng thái trước khi đọc body; đừng để EnsureSuccess ném lỗi."),
                ("retry on 5xx only, capped delays", "Chỉ retry 5xx; delay qua CjStubHandler.DelayAsync(min(10 << (attempt-1), 50))."),
                ("cancellation wins", "ct.ThrowIfCancellationRequested() trước khi gửi — và truyền ct vào SendAsync."),
            ],
        ),
        solution='public class Solution\n{\n    public sealed class ApiClient\n    {\n        private readonly System.Net.Http.HttpClient _http;\n\n        public ApiClient(System.Net.Http.HttpClient http) => _http = http;\n\n        public async System.Threading.Tasks.Task<string> GetUserAsync(\n            int id, System.Threading.CancellationToken ct = default)\n        {\n            ct.ThrowIfCancellationRequested();\n            using var resp = await _http.GetAsync("/users/" + id, ct);\n            int code = (int)resp.StatusCode;\n            if (code == 200)\n            {\n                string body = await resp.Content.ReadAsStringAsync(ct);\n                int i = body.IndexOf("\\"name\\":\\"") + 7;\n                int j = body.IndexOf(\'"\', i);\n                return "user:" + body.Substring(i, j - i);\n            }\n            if (code == 404) return "notfound";\n            return "failed";\n        }\n\n        public async System.Threading.Tasks.Task<string> GetUserWithRetryAsync(\n            int id, int maxAttempts, System.Threading.CancellationToken ct = default)\n        {\n            for (int attempt = 1; ; attempt++)\n            {\n                ct.ThrowIfCancellationRequested();\n                using var resp = await _http.GetAsync("/users/" + id, ct);\n                int code = (int)resp.StatusCode;\n                if (code == 200)\n                {\n                    string body = await resp.Content.ReadAsStringAsync(ct);\n                    int i = body.IndexOf("\\"name\\":\\"") + 7;\n                    int j = body.IndexOf(\'"\', i);\n                    return "user:" + body.Substring(i, j - i);\n                }\n                if (code == 404) return "notfound";\n                if (code < 500 || attempt >= maxAttempts) return "failed";\n                await CjStubHandler.DelayAsync(\n                    System.Math.Min(10 << (attempt - 1), 50), ct);\n            }\n        }\n    }\n}\n',
        wrong='public class Solution\n{\n    public sealed class ApiClient\n    {\n        private readonly System.Net.Http.HttpClient _http;\n\n        public ApiClient(System.Net.Http.HttpClient http) => _http = http;\n\n        public async System.Threading.Tasks.Task<string> GetUserAsync(\n            int id, System.Threading.CancellationToken ct = default)\n        {\n            using var resp = await _http.GetAsync("/users/" + id, ct);\n            // near-miss: throws for every non-2xx before the outcome mapping —\n            // the notfound test sees HttpRequestException instead of "notfound"\n            resp.EnsureSuccessStatusCode();\n            string body = await resp.Content.ReadAsStringAsync(ct);\n            int i = body.IndexOf("\\"name\\":\\"") + 7;\n            int j = body.IndexOf(\'"\', i);\n            return "user:" + body.Substring(i, j - i);\n        }\n\n        public async System.Threading.Tasks.Task<string> GetUserWithRetryAsync(\n            int id, int maxAttempts, System.Threading.CancellationToken ct = default)\n        {\n            for (int attempt = 1; ; attempt++)\n            {\n                using var resp = await _http.GetAsync("/users/" + id, ct);\n                int code = (int)resp.StatusCode;\n                if (code == 200)\n                {\n                    string body = await resp.Content.ReadAsStringAsync(ct);\n                    int i = body.IndexOf("\\"name\\":\\"") + 7;\n                    int j = body.IndexOf(\'"\', i);\n                    return "user:" + body.Substring(i, j - i);\n                }\n                if (code == 404) return "notfound";\n                if (code < 500 || attempt >= maxAttempts) return "failed";\n                await CjStubHandler.DelayAsync(\n                    System.Math.Min(10 << (attempt - 1), 50), ct);\n            }\n        }\n    }\n}\n',
    )
print("module 13 authored")
