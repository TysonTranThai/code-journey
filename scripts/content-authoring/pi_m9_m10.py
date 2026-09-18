#!/usr/bin/env python3
"""Python Intermediate — modules 9 (http-json) and 10 (concurrent-async)."""
from pi import write_module, write_lesson, write_practice, write_checkpoint, challenge, vi_challenge

# ============================ MODULE 9: http-json ============================
M9 = "http-json"
L9A = "http-foundations"
L9B = "json-api-client"
L9C = "transport-injection"
L9D = "checkpoint-api-client"

write_module(
    M9,
    "HTTP and JSON APIs",
    "Speak HTTP deliberately: status codes, headers, pagination, and a client built for testing.",
    "HTTP và JSON API",
    "Nói tiếng HTTP một cách chủ đích: mã trạng thái, header, phân trang, và một client dựng để kiểm thử được.",
    [L9A, L9B, L9C, L9D],
    ["m9-http-practice", "m9-client-practice", "m9-transport-practice"],
)

write_lesson(
    M9, L9A,
    "How HTTP Actually Works",
    "Requests, responses, methods, and the status-code families you must respect.",
    14,
    """
Every HTTP interaction is a **request** (method, path, headers, optional
body) answered by a **response** (status, headers, body):

```
GET /api/users?page=2 HTTP/1.1
Host: api.example.com
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

[{"id": 21}, {"id": 22}]
```

Methods are verbs: **GET** reads (no body, safe, cacheable), **POST**
creates/submits, **PUT/PATCH** update, **DELETE** removes. The status code
is the machine's verdict:

| Family | Meaning | Your job |
|---|---|---|
| 2xx | success (200 OK, 201 Created, 204 No Content) | proceed |
| 3xx | redirected | follow or update your URL |
| 4xx | **you** sent something wrong (400, 401, 403, 404, 429) | fix the request or report to user |
| 5xx | **server** failed (500, 502, 503) | back off, maybe retry |

The single most common intermediate mistake: treating every non-200 as the
same. A 404 means "stop retrying"; a 429 means "slow down (read
Retry-After)"; a 503 means "transient — retry with backoff". Clients that
respect status semantics are welcome; clients that hammer failing servers
are not.

In the sandbox there is no network — which is exactly why this course teaches
the **transport-injection** pattern (next lessons): the logic around HTTP is
testable without a socket.
""",
    "HTTP thực sự hoạt động thế nào",
    "Request, response, method, và các họ mã trạng thái bạn phải tôn trọng.",
    """
Mỗi tương tác HTTP là một **request** (method, path, header, body tùy chọn)
được trả lời bằng một **response** (trạng thái, header, body):

```
GET /api/users?page=2 HTTP/1.1
Host: api.example.com
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

[{"id": 21}, {"id": 22}]
```

Method là động từ: **GET** đọc (không body, an toàn, cache được), **POST**
tạo/gửi, **PUT/PATCH** cập nhật, **DELETE** xóa. Mã trạng thái là phán quyết
của máy:

| Họ | Ý nghĩa | Việc của bạn |
|---|---|---|
| 2xx | thành công (200 OK, 201 Created, 204 No Content) | tiếp tục |
| 3xx | bị chuyển hướng | đi theo hoặc cập nhật URL |
| 4xx | **bạn** gửi sai điều gì đó (400, 401, 403, 404, 429) | sửa request hoặc báo người dùng |
| 5xx | **server** gặp sự cố (500, 502, 503) | lùi lại, có thể thử lại |

Sai lầm trung cấp phổ biến nhất: coi mọi mã khác 200 là một. 404 nghĩa là
"đừng thử lại"; 429 nghĩa là "chậm lại (đọc Retry-After)"; 503 nghĩa là
"lỗi tạm thời — thử lại có backoff". Client tôn trọng ngữ nghĩa trạng thái
luôn được chào đón; client đập vào server đang lỗi thì không.

Trong sandbox không có mạng — và chính vì thế khóa học dạy mẫu
**transport-injection** (các bài kế tiếp): logic bao quanh HTTP kiểm thử
được mà không cần socket.
""",
)

write_lesson(
    M9, L9B,
    "A JSON API Client",
    "Parse API responses defensively: status checks, JSON errors, pagination, rate limits.",
    15,
    '''
APIs return JSON, but a client that assumes success is a client that crashes
in production. The defensive shape:

```python
import json

class ApiError(Exception):
    """API responded with an error status."""

def parse_response(status: int, body: bytes) -> dict | list:
    if status == 204:
        return {}
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ApiError(f"non-JSON response (status {status})") from exc
    if status >= 400:
        message = data.get("error", "unknown") if isinstance(data, dict) else "error"
        raise ApiError(f"HTTP {status}: {message}")
    return data
```

Notice the layers: **decode** (is it JSON?), **classify** (which status
family?), **extract** (where is the payload?), and only then **use**.

## Pagination: read the envelope

Most APIs wrap lists in metadata — page, per_page, total, or a `next` URL:

```python
def all_items(fetch, page_size=100):
    items = []
    page = 1
    while True:
        payload = fetch(page, page_size)        # {"items": [...], "has_more": bool}
        items.extend(payload["items"])
        if not payload["has_more"]:
            return items
        page += 1
```

Two non-negotiables: **stop conditions must be explicit** (a missing
`has_more` must end the loop, not hang it), and **rate limits are real** —
on 429, sleep for `Retry-After` seconds and retry a bounded number of times.

## Timeouts are not optional

A client without a timeout waits forever. Every real transport call carries a
timeout; on expiry you raise a client-side error and decide (retry? surface?)
like any other failure.
''',
    "Một JSON API Client",
    "Phân tích phản hồi API một cách phòng thủ: kiểm tra trạng thái, lỗi JSON, phân trang, giới hạn tần suất.",
    '''
API trả về JSON, nhưng một client giả định luôn thành công là client sập
trong production. Hình dạng phòng thủ:

```python
import json

class ApiError(Exception):
    """API phản hồi với một mã lỗi."""

def parse_response(status: int, body: bytes) -> dict | list:
    if status == 204:
        return {}
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ApiError(f"non-JSON response (status {status})") from exc
    if status >= 400:
        message = data.get("error", "unknown") if isinstance(data, dict) else "error"
        raise ApiError(f"HTTP {status}: {message}")
    return data
```

Hãy để ý các tầng: **giải mã** (có phải JSON không?), **phân loại** (thuộc
họ trạng thái nào?), **trích xuất** (payload nằm ở đâu?), và chỉ sau đó
**sử dụng**.

## Phân trang: đọc phong bì

Phần lớn API bọc danh sách trong metadata — page, per_page, total, hoặc URL
`next`:

```python
def all_items(fetch, page_size=100):
    items = []
    page = 1
    while True:
        payload = fetch(page, page_size)        # {"items": [...], "has_more": bool}
        items.extend(payload["items"])
        if not payload["has_more"]:
            return items
        page += 1
```

Hai điều không thương lượng: **điều kiện dừng phải tường minh** (thiếu
`has_more` phải kết thúc vòng lặp, chứ không treo nó), và **giới hạn tần
suất là có thật** — gặp 429, ngủ theo số giây `Retry-After` và thử lại một
số lần có giới hạn.

## Timeout không phải tùy chọn

Client không có timeout sẽ chờ mãi mãi. Mọi lời gọi transport thật đều mang
một timeout; khi hết giờ, bạn raise lỗi phía client và quyết định (thử lại?
báo lên?) như mọi thất bại khác.
''',
)

write_lesson(
    M9, L9C,
    "Transport Injection",
    "Design clients where the network is a parameter — testable by construction.",
    13,
    '''
Here is the professional shape that makes HTTP code testable without a
network — the same dependency-injection idea from modules 2 and 7, applied
to transport:

```python
import json
import urllib.request

def fetch_json(url: str, opener=None) -> dict:
    """opener(url) -> object with .read() -> bytes. Defaults to real urllib."""
    if opener is None:
        opener = urllib.request.urlopen     # real transport, real network
    with opener(url) as response:
        return json.loads(response.read())
```

In production, callers omit `opener` and the real network is used. In tests,
a fake transport is two lines:

```python
class FakeResponse:
    def __init__(self, payload: bytes):
        self._payload = payload
    def read(self):
        return self._payload

def test_fetch():
    data = fetch_json("http://x", opener=lambda url: FakeResponse(b'{"ok": true}'))
    assert data == {"ok": True}
```

## Why this beats mocking internals

With injection, the function under test never knows it's in a test — no
patching paths to remember, no refactor breaks when module layout changes.
It also forces honest design: if you *can't* inject the transport, the
function is doing too much.

The industry tools (`requests`, `httpx`) sit on top of this same idea with
more features (sessions, retries, base URLs). The pattern transfers — on your
own machine, `pip install httpx` and the architecture is identical.
''',
    "Tiêm Transport",
    "Thiết kế client nơi mạng là một tham số — kiểm thử được ngay từ cấu trúc.",
    '''
Đây là hình dạng chuyên nghiệp khiến code HTTP kiểm thử được mà không cần
mạng — chính ý tưởng dependency-injection của module 2 và 7, áp dụng cho
transport:

```python
import json
import urllib.request

def fetch_json(url: str, opener=None) -> dict:
    """opener(url) -> đối tượng có .read() -> bytes. Mặc định là urllib thật."""
    if opener is None:
        opener = urllib.request.urlopen     # transport thật, mạng thật
    with opener(url) as response:
        return json.loads(response.read())
```

Trong production, người gọi bỏ qua `opener` và mạng thật được dùng. Trong
test, một transport giả chỉ là hai dòng:

```python
class FakeResponse:
    def __init__(self, payload: bytes):
        self._payload = payload
    def read(self):
        return self._payload

def test_fetch():
    data = fetch_json("http://x", opener=lambda url: FakeResponse(b'{"ok": true}'))
    assert data == {"ok": True}
```

## Vì sao cách này hơn mock nội bộ

Với injection, hàm đang được test không bao giờ biết mình đang trong test —
không phải nhớ đường patch, không vỡ khi refactor bố cục module. Nó còn ép
thiết kế trung thực: nếu bạn *không thể* tiêm transport, hàm đó đang làm
quá nhiều việc.

Các công cụ trong ngành (`requests`, `httpx`) xây trên cùng ý tưởng này với
nhiều tính năng hơn (session, retry, base URL). Mẫu hình chuyển giao trọn
vẹn — trên máy của bạn, `pip install httpx` và kiến trúc vẫn y nguyên.
''',
)

# --- module 9 practice sets ---
write_practice(
    M9, "m9-http-practice",
    "HTTP Semantics Drills",
    "Classify status codes and act on them correctly.",
    "Luyện Ngữ nghĩa HTTP",
    "Phân loại mã trạng thái và hành động đúng với chúng.",
    L9A, 25, "intermediate",
    [
        challenge(
            "pi9-http-classify", "Status Verdicts",
            "Implement classify(status: int) -> str returning exactly one of: 'ok' (2xx), 'redirect' (3xx), 'client_error' (4xx), 'server_error' (5xx), 'invalid' (anything else, including < 100 or > 599).",
            "def classify(status):\n    pass\n",
            [
                ("families map correctly",
                 "assert classify(200) == 'ok'\nassert classify(201) == 'ok'\nassert classify(301) == 'redirect'\nassert classify(404) == 'client_error'\nassert classify(503) == 'server_error'",
                 "100-based families: 2xx/3xx/4xx/5xx."),
                ("out-of-range is invalid",
                 "assert classify(99) == 'invalid'\nassert classify(600) == 'invalid'",
                 "HTTP status codes live between 100 and 599."),
            ],
            level="imitation",
        ),
        challenge(
            "pi9-http-retryable", "Retry or Stop?",
            "Implement should_retry(status: int, attempts: int) -> bool: retry ONLY server errors (5xx) and 429, and only when attempts < 3. Everything else returns False.",
            "def should_retry(status, attempts):\n    pass\n",
            [
                ("retries transient failures",
                 "assert should_retry(503, 1) is True\nassert should_retry(429, 2) is True",
                 "5xx and 429 are retryable."),
                ("stops at the bound and on client errors",
                 "assert should_retry(503, 3) is False\nassert should_retry(404, 1) is False\nassert should_retry(200, 1) is False",
                 "attempts >= 3 stops; 4xx and 2xx never retry."),
            ],
            level="guided",
        ),
    ],
    {
        "pi9-http-classify": vi_challenge("Phán quyết trạng thái", "Viết classify(status: int) -> str trả về đúng một trong: 'ok' (2xx), 'redirect' (3xx), 'client_error' (4xx), 'server_error' (5xx), 'invalid' (mọi thứ khác, gồm cả < 100 hoặc > 599).", [{"families map correctly".replace("families map correctly", "Các họ ánh xạ đúng") if False else "Các họ ánh xạ đúng": "Các họ dựa trên trăm: 2xx/3xx/4xx/5xx.", "Ngoài dải là invalid": "Mã trạng thái HTTP nằm giữa 100 và 599."} if False else [("Các họ ánh xạ đúng", "Các họ dựa trên trăm: 2xx/3xx/4xx/5xx."), ("Ngoài dải là invalid", "Mã trạng thái HTTP nằm giữa 100 và 599.")]][0]),
        "pi9-http-retryable": vi_challenge("Thử lại hay dừng?", "Viết should_retry(status: int, attempts: int) -> bool: chỉ thử lại với lỗi server (5xx) và 429, và chỉ khi attempts < 3. Mọi thứ khác trả False.", [("Thử lại lỗi tạm thời", "5xx và 429 là có thể thử lại."), ("Dừng tại giới hạn và với lỗi client", "attempts >= 3 thì dừng; 4xx và 2xx không bao giờ thử lại.")]),
    },
    solutions=[
        ("pi9-http-classify", "def classify(status):\n    if not (100 <= status <= 599):\n        return 'invalid'\n    if status < 300:\n        return 'ok'\n    if status < 400:\n        return 'redirect'\n    if status < 500:\n        return 'client_error'\n    return 'server_error'", "def classify(status):\n    if status >= 500:\n        return 'server_error'\n    if status >= 400:\n        return 'client_error'\n    if status >= 300:\n        return 'redirect'\n    if status >= 200:\n        return 'ok'\n    return 'ok'"),
        ("pi9-http-retryable", "def should_retry(status, attempts):\n    if attempts >= 3:\n        return False\n    return status == 429 or 500 <= status <= 599", "def should_retry(status, attempts):\n    if attempts >= 3:\n        return False\n    return status >= 400"),
    ],
)

write_practice(
    M9, "m9-client-practice",
    "Client Behavior Drills",
    "Parse defensively, paginate with explicit stop conditions.",
    "Luyện Hành vi Client",
    "Phân tích phòng thủ, phân trang với điều kiện dừng tường minh.",
    L9B, 30, "intermediate",
    [
        challenge(
            "pi9-client-parse", "Defensive Parsing",
            "Implement parse_response(status, body) where body is bytes: 204 → {}; non-JSON body → raise ApiError('non-JSON response'); status >= 400 → raise ApiError containing the status; else return parsed JSON.",
            "import json\n\nclass ApiError(Exception):\n    pass\n\ndef parse_response(status, body):\n    pass\n",
            [
                ("happy path parses",
                 "assert parse_response(200, b'{\"a\": 1}') == {'a': 1}\nassert parse_response(204, b'') == {}",
                 "json.loads for data; 204 short-circuits to {}."),
                ("garbage body raises",
                 "try:\n    parse_response(200, b'<html>not json</html>')\n    failed = False\nexcept ApiError:\n    failed = True\nassert failed",
                 "Decode before use — HTML where JSON was promised is an error."),
                ("error status raises with code",
                 "try:\n    parse_response(404, b'{\"error\": \"nope\"}')\n    failed = False\nexcept ApiError as e:\n    failed = '404' in str(e)\nassert failed",
                 "4xx/5xx must raise even when the body is valid JSON."),
            ],
            level="guided",
        ),
        challenge(
            "pi9-client-pages", "Pagination Loop",
            "Implement collect(fetch) where fetch(page) returns {'items': [...], 'has_more': bool}. Loop pages from 1, extending items, stopping when has_more is False or page exceeds 1000 (safety bound). Return the concatenated list.",
            "def collect(fetch):\n    pass\n",
            [
                ("collects all pages",
                 "data = {1: {'items': [1, 2], 'has_more': True}, 2: {'items': [3], 'has_more': False}}\nassert collect(lambda p: data[p]) == [1, 2, 3]",
                 "Loop until has_more is falsy."),
                ("safety bound stops runaway servers",
                 "assert collect(lambda p: {'items': [p], 'has_more': True}) == [p for p in range(1, 1001)]",
                 "After 1000 pages, stop even if has_more never turns False."),
            ],
            level="independent",
        ),
    ],
    {
        "pi9-client-parse": vi_challenge("Phân tích phòng thủ", "Viết parse_response(status, body) với body là bytes: 204 → {}; body không phải JSON → raise ApiError('non-JSON response'); status >= 400 → raise ApiError chứa mã trạng thái; còn lại trả về JSON đã parse.", [("Đường vui parses", "json.loads cho dữ liệu; 204 trả {} ngay."), ("Body rác raise", "Giải mã trước khi dùng — HTML nơi hứa JSON là một lỗi."), ("Mã lỗi raise kèm số", "4xx/5xx phải raise kể cả khi body là JSON hợp lệ.")]),
        "pi9-client-pages": vi_challenge("Vòng lặp phân trang", "Viết collect(fetch) với fetch(page) trả về {'items': [...], 'has_more': bool}. Lặp trang từ 1, gom items, dừng khi has_more là False hoặc page vượt 1000 (chặn an toàn). Trả về list đã ghép.", [("Gom đủ mọi trang", "Lặp cho đến khi has_more falsy."), ("Chặn an toàn ngăn server điên", "Sau 1000 trang, dừng dù has_more chưa bao giờ False.")]),
    },
    solutions=[
        ("pi9-client-parse", "import json\n\nclass ApiError(Exception):\n    pass\n\ndef parse_response(status, body):\n    if status == 204:\n        return {}\n    try:\n        data = json.loads(body)\n    except (json.JSONDecodeError, UnicodeDecodeError) as exc:\n        raise ApiError(f'non-JSON response (status {status})') from exc\n    if status >= 400:\n        message = data.get('error', 'unknown') if isinstance(data, dict) else 'error'\n        raise ApiError(f'HTTP {status}: {message}')\n    return data", "import json\n\nclass ApiError(Exception):\n    pass\n\ndef parse_response(status, body):\n    return json.loads(body)"),
        ("pi9-client-pages", "def collect(fetch):\n    items = []\n    page = 1\n    while page <= 1000:\n        payload = fetch(page)\n        items.extend(payload['items'])\n        if not payload['has_more']:\n            return items\n        page += 1\n    return items", "def collect(fetch):\n    items = []\n    page = 1\n    while True:\n        payload = fetch(page)\n        items.extend(payload['items'])\n        page += 1"),
    ],
)

write_practice(
    M9, "m9-transport-practice",
    "Transport Injection Drills",
    "Swap real network for fakes; test the whole behavior.",
    "Luyện Tiêm Transport",
    "Hoán đổi mạng thật bằng bản giả; test trọn hành vi.",
    L9C, 25, "intermediate",
    [
        challenge(
            "pi9-ti-fetch", "Fetch with an Injected Transport",
            "Implement get_status(base_url, path, transport=None) that composes url = base_url + path, calls transport(url) (default transport raises RuntimeError('no network in sandbox')) expecting an object with attributes .status and .read(), and returns (status, parsed-json-body).",
            "import json\n\ndef get_status(base_url, path, transport=None):\n    pass\n",
            [
                ("uses the injected transport",
                 "class R:\n    status = 200\n    def read(self):\n        return b'{\"ok\": 1}'\nstatus, body = get_status('http://api', '/x', transport=lambda u: R())\nassert status == 200 and body == {'ok': 1}",
                 "Call transport(url); parse read() bytes."),
                ("default transport is explicit about no network",
                 "try:\n    get_status('http://api', '/x')\n    failed = False\nexcept RuntimeError as e:\n    failed = 'no network' in str(e)\nassert failed",
                 "None transport → RuntimeError('no network in sandbox')."),
                ("url composition",
                 "seen = []\nclass R:\n    status = 201\n    def read(self):\n        return b'{}'\ndef t(u):\n    seen.append(u)\n    return R()\nget_status('http://api', '/items/7', transport=t)\nassert seen == ['http://api/items/7']",
                 "Concatenate base_url and path exactly."),
            ],
            level="independent",
        ),
    ],
    {
        "pi9-ti-fetch": vi_challenge("Fetch với transport tiêm vào", "Viết get_status(base_url, path, transport=None) ghép url = base_url + path, gọi transport(url) (transport mặc định raise RuntimeError('no network in sandbox')) kỳ vọng đối tượng có thuộc tính .status và .read(), rồi trả về (status, body-json-đã-parse).", [("Dùng transport được tiêm", "Gọi transport(url); parse bytes từ read()."), ("Transport mặc định nói rõ không có mạng", "Transport None → RuntimeError('no network in sandbox')."), ("Ghép url", "Nối base_url và path chính xác.")]),
    },
    solutions=[
        ("pi9-ti-fetch", "import json\n\ndef get_status(base_url, path, transport=None):\n    if transport is None:\n        raise RuntimeError('no network in sandbox')\n    url = base_url + path\n    response = transport(url)\n    return (response.status, json.loads(response.read()))", "import json\n\ndef get_status(base_url, path, transport=None):\n    if transport is None:\n        raise RuntimeError('no network in sandbox')\n    response = transport(path)\n    return (response.status, json.loads(response.read()))"),
    ],
)

# --- module 9 checkpoint ---
write_checkpoint(
    M9, L9D,
    "Checkpoint: Production-Style API Client",
    "A client class with injected transport, defensive parsing, and bounded retries.",
    20,
    """
Assemble the module: a small client class that injects its transport,
classifies responses, retries transients, and never hangs.

**Working with AI:** paste your client and ask "how does this behave on a
500? on a 429? on garbage bytes?" — if you can't answer from the code,
restructure.
""",
    "Checkpoint: API Client chuẩn production",
    "Một lớp client có transport tiêm vào, phân tích phòng thủ, và retry có giới hạn.",
    """
Ghép cả module: một lớp client nhỏ tiêm transport của mình, phân loại phản
hồi, thử lại lỗi tạm thời, và không bao giờ treo.

**Làm việc cùng AI:** dán client của bạn và hỏi "nó thế nào khi gặp 500? 429?
bytes rác?" — nếu bạn không trả lời được từ code, hãy tái cấu trúc.
""",
    challenge(
        "pi9-ckpt-client", "Resilient Mini Client",
        "Implement MiniClient(base_url, transport=None) with get(path) -> dict. Behavior: compose url = base_url + path; call transport(url) (None → RuntimeError 'no network in sandbox'); the response object has .status and .read() -> bytes. On 200 parse and return JSON. On 5xx/429, retry up to 3 total attempts, then raise ApiError('exhausted retries'). On other 4xx, raise ApiError immediately. Non-JSON body on 200 raises ApiError('bad body').",
        "import json\n\nclass ApiError(Exception):\n    pass\n\nclass MiniClient:\n    def __init__(self, base_url, transport=None):\n        pass\n\n    def get(self, path):\n        pass\n",
        [
            ("success returns parsed json",
             "class R:\n    status = 200\n    def __init__(self):\n        self.n = 0\n    def read(self):\n        return b'{\"v\": 42}'\nc = MiniClient('http://api', transport=lambda u: R())\nassert c.get('/v') == {'v': 42}",
             "200 → parse → return."),
            ("client error fails immediately",
             "class R:\n    status = 404\n    def read(self):\n        return b'{}'\nc = MiniClient('http://api', transport=lambda u: R())\ntry:\n    c.get('/missing')\n    failed = False\nexcept ApiError:\n    failed = True\nassert failed",
             "4xx (non-429) raises at once — no retries."),
            ("transient failure retried then success",
             "class Flaky:\n    def __init__(self):\n        self.calls = 0\n    def read(self):\n        return b'{}'\nflaky = Flaky()\ndef transport(u):\n    flaky.calls += 1\n    class R:\n        status = 503 if flaky.calls == 1 else 200\n        def read(self):\n            return b'{\"ok\": true}'\n    return R()\nc = MiniClient('http://api', transport=transport)\nassert c.get('/x') == {'ok': True}\nassert flaky.calls == 2",
             "First 503 retried; second attempt succeeds."),
            ("exhausted retries raise",
             "def transport(u):\n    class R:\n        status = 500\n        def read(self):\n            return b'{}'\n    return R()\nc = MiniClient('http://api', transport=transport)\ntry:\n    c.get('/down')\n    failed = False\nexcept ApiError as e:\n    failed = 'exhausted' in str(e)\nassert failed",
             "Three total attempts, then ApiError('exhausted retries')."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Mini Client bền vững",
        "Viết MiniClient(base_url, transport=None) với get(path) -> dict. Hành vi: ghép url = base_url + path; gọi transport(url) (None → RuntimeError 'no network in sandbox'); đối tượng phản hồi có .status và .read() -> bytes. Với 200, parse và trả JSON. Với 5xx/429, thử lại tối đa 3 lần tổng, rồi raise ApiError('exhausted retries'). Với 4xx khác, raise ApiError ngay lập tức. Body không phải JSON khi 200 raise ApiError('bad body').",
        [
            ("Thành công trả JSON đã parse", "200 → parse → return."),
            ("Lỗi client fail ngay lập tức", "4xx (khác 429) raise ngay — không retry."),
            ("Lỗi tạm thời được thử lại rồi thành công", "503 đầu được thử lại; lần hai thành công."),
            ("Hết lượt thử sẽ raise", "Ba lần tổng, rồi ApiError('exhausted retries')."),
        ],
    ),
    solution="import json\n\nclass ApiError(Exception):\n    pass\n\nclass MiniClient:\n    def __init__(self, base_url, transport=None):\n        self._base = base_url\n        self._transport = transport\n\n    def get(self, path):\n        if self._transport is None:\n            raise RuntimeError('no network in sandbox')\n        url = self._base + path\n        last_status = None\n        for _ in range(3):\n            response = self._transport(url)\n            last_status = response.status\n            if last_status == 429 or 500 <= last_status <= 599:\n                continue\n            if 200 <= last_status < 300:\n                try:\n                    return json.loads(response.read())\n                except (json.JSONDecodeError, UnicodeDecodeError) as exc:\n                    raise ApiError('bad body') from exc\n            raise ApiError(f'HTTP {last_status}')\n        raise ApiError('exhausted retries')",
    wrong="import json\n\nclass ApiError(Exception):\n    pass\n\nclass MiniClient:\n    def __init__(self, base_url, transport=None):\n        self._base = base_url\n        self._transport = transport\n\n    def get(self, path):\n        if self._transport is None:\n            raise RuntimeError('no network in sandbox')\n        url = self._base + path\n        for _ in range(3):\n            response = self._transport(url)\n            if 200 <= response.status < 300:\n                try:\n                    return json.loads(response.read())\n                except (json.JSONDecodeError, UnicodeDecodeError) as exc:\n                    raise ApiError('bad body') from exc\n        raise ApiError('exhausted retries')",
)

# ============================ MODULE 10: concurrent-async ============================
M10 = "concurrent-async"
L10A = "sync-vs-async"
L10B = "coroutines-tasks"
L10C = "gather-timeouts"
L10D = "checkpoint-async-collector"

write_module(
    M10,
    "Concurrent Async Python",
    "One loop, many waits: coroutines, tasks, gather, and timeouts.",
    "Async Python Đồng thời",
    "Một vòng lặp, nhiều lần chờ: coroutine, task, gather, và timeout.",
    [L10A, L10B, L10C, L10D],
    ["m10-async-practice", "m10-task-practice", "m10-gather-practice"],
)

write_lesson(
    M10, L10A,
    "Sync vs Async: The Wait Problem",
    "Concurrency vs parallelism, and why one thread can juggle thousands of waits.",
    13,
    """
Most of a network-bound program's life is **waiting** — for responses, disks,
databases. Synchronous code waits *blocked*: nothing else happens.

```python
# SYNC: total time = sum of all waits
def fetch_all(urls):
    results = []
    for url in urls:
        results.append(fetch(url))     # blocks ~200ms each
    return results
```

**Concurrency** is handling many waits during the same period (one worker
switching between them). **Parallelism** is doing many things at the same
instant (many workers). Async Python gives you concurrency on **one thread**:

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(0.2)           # stand-in for a network wait
    return url

async def fetch_all(urls):
    return await asyncio.gather(*(fetch(u) for u in urls))
```

`async def` defines a **coroutine** — a function that can pause (`await`)
and let the **event loop** run someone else while it waits. When the wait
finishes, the loop resumes it. Ten 200ms waits overlap into ~200ms total,
not 2 seconds.

## When async is (and isn't) the answer

Async shines for **I/O-bound** work: APIs, sockets, databases. It does
nothing for CPU-bound work (image processing, math) — that needs processes.
And the rule that saves beginners: **you cannot `await` inside a regular
`def`**, and you cannot call blocking functions inside async code without
freezing the loop. `asyncio.run(main())` is the door into async-land.
""",
    "Sync vs Async: Bài toán Chờ",
    "Đồng thời vs song song, và vì sao một thread có thể tung hứng hàng nghìn lần chờ.",
    """
Phần lớn đời một chương trình gắn với mạng là **chờ** — chờ phản hồi, đĩa,
database. Code đồng bộ chờ theo kiểu *bị chặn*: không gì khác diễn ra.

```python
# SYNC: tổng thời gian = tổng mọi lần chờ
def fetch_all(urls):
    results = []
    for url in urls:
        results.append(fetch(url))     # chặn ~200ms mỗi lần
    return results
```

**Đồng thời (concurrency)** là xử lý nhiều lần chờ trong cùng khoảng thời
gian (một worker xoay giữa chúng). **Song song (parallelism)** là làm nhiều
việc tại cùng một khoảnh khắc (nhiều worker). Async Python cho bạn đồng thời
trên **một thread duy nhất**:

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(0.2)           # chỗ đứng cho một lần chờ mạng
    return url

async def fetch_all(urls):
    return await asyncio.gather(*(fetch(u) for u in urls))
```

`async def` định nghĩa một **coroutine** — hàm có thể tạm dừng (`await`) và
nhường **event loop** chạy việc khác trong lúc nó chờ. Khi lần chờ kết thúc,
loop tiếp tục nó. Mười lần chờ 200ms chồng lên nhau thành ~200ms tổng,
không phải 2 giây.

## Khi nào async là (và không là) câu trả lời

Async tỏa sáng cho việc **I/O-bound**: API, socket, database. Nó không giúp
gì cho việc CPU-bound (xử lý ảnh, toán) — cái đó cần process. Và quy tắc
cứu cánh của người mới: **không thể `await` bên trong một `def` thường**,
và không thể gọi hàm chặn bên trong code async mà không đóng băng loop.
`asyncio.run(main())` là cánh cổng vào vùng đất async.
""",
)

write_lesson(
    M10, L10B,
    "Coroutines and Tasks",
    "await sequences, create_task concurrency, and ordering guarantees.",
    14,
    """
Inside a coroutine, `await` marks the pause points. Two `await`s in a row run
**in sequence**; to run things *together*, schedule them as **tasks**:

```python
import asyncio

async def prepare():
    await asyncio.sleep(0.1)
    return "dough"

async def heat():
    await asyncio.sleep(0.2)
    return "oven hot"

async def sequential():
    return await prepare(), await heat()      # 0.3s total

async def concurrent():
    t1 = asyncio.create_task(prepare())       # starts NOW
    t2 = asyncio.create_task(heat())          # starts NOW too
    return await t1, await t2                 # ~0.2s total
```

`create_task` schedules the coroutine on the event loop **immediately**;
`await task` collects its result later. The awaits at the end may look
sequential but the waits already overlapped.

## Ordering guarantees to rely on

- Tasks start in the order you create them, but their **completion order
  depends on their waits** — never assume result order from scheduling order
  (pair results with their inputs explicitly if order matters).
- The loop runs on one thread: between `await` points your code is atomic.
  Two coroutines cannot interrupt each other mid-arithmetic — but shared
  state *can* change across an `await`, which is where async bugs live.

## Anti-patterns

`time.sleep()` inside async code blocks the whole loop — use
`await asyncio.sleep()`. Calling a coroutine without awaiting it creates it
and silently does nothing (`RuntimeWarning: coroutine was never awaited`).
""",
    "Coroutine và Task",
    "await tuần tự, create_task chạy đồng thời, và các cam kết về thứ tự.",
    """
Bên trong một coroutine, `await` đánh dấu các điểm tạm dừng. Hai `await` nối
nhau chạy **tuần tự**; để chạy chúng *cùng nhau*, hãy lập lịch chúng thành
**task**:

```python
import asyncio

async def prepare():
    await asyncio.sleep(0.1)
    return "dough"

async def heat():
    await asyncio.sleep(0.2)
    return "oven hot"

async def sequential():
    return await prepare(), await heat()      # tổng 0.3s

async def concurrent():
    t1 = asyncio.create_task(prepare())       # bắt đầu NGAY
    t2 = asyncio.create_task(heat())          # cũng bắt đầu NGAY
    return await t1, await t2                 # ~0.2s tổng
```

`create_task` đưa coroutine lên event loop **ngay lập tức**; `await task`
thu kết quả sau. Các await cuối trông tuần tự nhưng các lần chờ đã chồng
lên nhau từ trước.

## Những cam kết về thứ tự đáng tin

- Task bắt đầu theo thứ tự bạn tạo, nhưng **thứ tự hoàn thành phụ thuộc các
  lần chờ** của chúng — đừng giả định thứ tự kết quả theo thứ tự lập lịch
  (ghép kết quả với input tường minh nếu thứ tự quan trọng).
- Loop chạy trên một thread: giữa các điểm `await` code của bạn là nguyên tử.
  Hai coroutine không thể chen ngang nhau giữa chừng phép tính — nhưng trạng
  thái dùng chung *có thể* đổi qua một `await`, đó là nơi async bug cư trú.

## Chống-mẫu

`time.sleep()` trong code async chặn cả loop — dùng `await asyncio.sleep()`.
Gọi một coroutine mà không await sẽ tạo nó và lặng lẽ không làm gì cả
(`RuntimeWarning: coroutine was never awaited`).
""",
)

write_lesson(
    M10, L10C,
    "gather, Timeouts, and Failure Modes",
    "Run many coroutines with return_exceptions=True and never wait forever.",
    14,
    """
`asyncio.gather` runs a collection of coroutines concurrently and collects
results — with one knob that changes its failure philosophy:

```python
import asyncio

async def job(name, delay, fail=False):
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(name)
    return name

async def main():
    results = await asyncio.gather(
        job("a", 0.1),
        job("b", 0.1, fail=True),
        job("c", 0.1),
        return_exceptions=True,       # failures become VALUES, not crashes
    )
    # [\"a\", ValueError(\"b\"), \"c\"]
```

With `return_exceptions=False` (default), the first exception cancels the
gang and re-raises — right for *all-or-nothing* work. With `True`, each
failure is returned in place — right for *collect what you can*, like
fetching from many flaky sources. Choosing between them **is** the design
decision.

## Timeouts: nobody waits forever

```python
async def main():
    try:
        result = await asyncio.wait_for(job("slow", 10), timeout=0.5)
    except asyncio.TimeoutError:
        result = "gave up"
```

`wait_for` cancels the coroutine when the deadline passes and raises
`TimeoutError` in the caller. Real collectors combine the two: gather with
`return_exceptions=True`, wrap each job in a timeout, and treat
`(timeout, error)` results as "failed sources" — the exact shape of this
module's checkpoint.
""",
    "gather, Timeout, và các chế độ lỗi",
    "Chạy nhiều coroutine với return_exceptions=True và không bao giờ chờ vĩnh viễn.",
    """
`asyncio.gather` chạy một tập coroutine đồng thời và thu kết quả — với một
núm xoay thay đổi triết lý thất bại của nó:

```python
import asyncio

async def job(name, delay, fail=False):
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(name)
    return name

async def main():
    results = await asyncio.gather(
        job("a", 0.1),
        job("b", 0.1, fail=True),
        job("c", 0.1),
        return_exceptions=True,       # lỗi thành GIÁ TRỊ, không phải crash
    )
    # ["a", ValueError("b"), "c"]
```

Với `return_exceptions=False` (mặc định), exception đầu tiên hủy cả nhóm và
ném lại — hợp với công việc *all-or-nothing*. Với `True`, mỗi lỗi được trả về
tại vị trí của nó — hợp với *gom được gì hay nấy*, như lấy dữ liệu từ nhiều
ng-source hay trục trặc. Chọn giữa hai chế độ **chính là** quyết định thiết kế.

## Timeout: không ai chờ vĩnh viễn

```python
async def main():
    try:
        result = await asyncio.wait_for(job("slow", 10), timeout=0.5)
    except asyncio.TimeoutError:
        result = "gave up"
```

`wait_for` hủy coroutine khi hết hạn và raise `TimeoutError` cho người gọi.
Bộ gom dữ liệu thật kết hợp cả hai: gather với `return_exceptions=True`,
bọc mỗi job trong một timeout, và coi kết quả (timeout, error) là "nguồn
lỗi" — chính hình dạng của checkpoint module này.
""",
)

# --- module 10 practice sets ---
write_practice(
    M10, "m10-async-practice",
    "Coroutine Drills",
    "Write async functions and run them with asyncio.run.",
    "Luyện Coroutine",
    "Viết hàm async và chạy chúng với asyncio.run.",
    L10A, 25, "intermediate",
    [
        challenge(
            "pi10-as-hello", "Async Hello",
            "Implement async def hello(name) that awaits asyncio.sleep(0.01) then returns f'hello {name}'. Then implement sync def run_hello(name) that uses asyncio.run to return hello(name)'s result.",
            "import asyncio\n\nasync def hello(name):\n    pass\n\ndef run_hello(name):\n    pass\n",
            [
                ("returns through the loop",
                 "assert run_hello('async') == 'hello async'",
                 "asyncio.run(hello(name)) bridges sync and async worlds."),
                ("hello is a coroutine function",
                 "import inspect\nassert inspect.iscoroutinefunction(hello)",
                 "It must be declared with async def."),
            ],
            level="imitation",
        ),
        challenge(
            "pi10-as-seq", "Sequential Awaits",
            "Implement async def flow() that awaits two steps in order: step_one() returns 1 (after sleeping 0.01), step_two(n) returns n + 1 (after sleeping 0.01); flow returns step_two(step_one's result) — i.e. 2. Provide a sync run_flow() wrapper using asyncio.run.",
            "import asyncio\n\nasync def step_one():\n    pass\n\nasync def step_two(n):\n    pass\n\nasync def flow():\n    pass\n\ndef run_flow():\n    pass\n",
            [
                ("value flows through steps",
                 "assert run_flow() == 2",
                 "second = await step_one(); return await step_two(second)."),
                ("steps are coroutines",
                 "import inspect\nassert inspect.iscoroutinefunction(step_one)\nassert inspect.iscoroutinefunction(step_two)",
                 "Both declared with async def and awaited inside flow."),
            ],
            level="guided",
        ),
    ],
    {
        "pi10-as-hello": vi_challenge("Async Hello", "Viết async def hello(name) await asyncio.sleep(0.01) rồi trả về f'hello {name}'. Sau đó viết sync def run_hello(name) dùng asyncio.run để trả về kết quả của hello(name).", [("Trả kết quả qua loop", "asyncio.run(hello(name)) nối hai thế giới sync và async."), ("hello là một hàm coroutine", "Phải khai báo bằng async def.")]),
        "pi10-as-seq": vi_challenge("Await tuần tự", "Viết async def flow() await hai bước theo thứ tự: step_one() trả 1 (sau khi ngủ 0.01), step_two(n) trả n + 1 (sau khi ngủ 0.01); flow trả về step_two(kết quả của step_one) — tức 2. Cung cấp wrapper sync run_flow() dùng asyncio.run.", [("Giá trị chảy qua các bước", "second = await step_one(); return await step_two(second)."), ("Các bước là coroutine", "Cả hai khai báo bằng async def và được await bên trong flow.")]),
    },
    solutions=[
        ("pi10-as-hello", "import asyncio\n\nasync def hello(name):\n    await asyncio.sleep(0.01)\n    return f'hello {name}'\n\ndef run_hello(name):\n    return asyncio.run(hello(name))", "import asyncio\n\nasync def hello(name):\n    await asyncio.sleep(0.01)\n    return f'hello {name}'\n\ndef run_hello(name):\n    return hello(name)"),
        ("pi10-as-seq", "import asyncio\n\nasync def step_one():\n    await asyncio.sleep(0.01)\n    return 1\n\nasync def step_two(n):\n    await asyncio.sleep(0.01)\n    return n + 1\n\nasync def flow():\n    first = await step_one()\n    return await step_two(first)\n\ndef run_flow():\n    return asyncio.run(flow())", "import asyncio\n\nasync def step_one():\n    await asyncio.sleep(0.01)\n    return 1\n\nasync def step_two(n):\n    await asyncio.sleep(0.01)\n    return n + 1\n\nasync def flow():\n    first = step_one()\n    return await step_two(first)\n\ndef run_flow():\n    return asyncio.run(flow())"),
    ],
)

write_practice(
    M10, "m10-task-practice",
    "Task Concurrency Drills",
    "Run waits together and prove the time saved.",
    "Luyện Đồng thời Task",
    "Chạy các lần chờ cùng nhau và chứng minh thời gian tiết kiệm được.",
    L10B, 30, "intermediate",
    [
        challenge(
            "pi10-tk-concurrent", "Concurrent vs Sequential",
            "Implement async def slow_double(n) awaiting asyncio.sleep(0.1) and returning n*2. Then async def run_concurrent(values) using asyncio.create_task for each value and awaiting all tasks. Provide sync wrapper run_all(values) returning the list of results (in input order).",
            "import asyncio\n\nasync def slow_double(n):\n    pass\n\nasync def run_concurrent(values):\n    pass\n\ndef run_all(values):\n    pass\n",
            [
                ("results match input order",
                 "assert run_all([1, 2, 3]) == [2, 4, 6]",
                 "Collect each task with await; task order = result order here."),
                ("actually concurrent (fast, not 3x slow)",
                 "import time\nstart = time.monotonic()\nrun_all([1, 2, 3, 4])\nelapsed = time.monotonic() - start\nassert elapsed < 0.35, f'too slow: {elapsed}'",
                 "Four 0.1s waits overlapped must finish well under 0.4s."),
            ],
            level="guided",
        ),
        challenge(
            "pi10-tk-pairs", "Pair Results with Inputs",
            "Implement async def fetch_name(user_id) awaiting sleep(0.02) and returning f'user-{user_id}'. Implement async def collect(pairs) where pairs is a list of (key, user_id) tuples: run all fetches concurrently and return a dict key -> fetched name. Provide sync wrapper run_collect(pairs).",
            "import asyncio\n\nasync def fetch_name(user_id):\n    pass\n\nasync def collect(pairs):\n    pass\n\ndef run_collect(pairs):\n    pass\n",
            [
                ("keys map to fetched names",
                 "out = run_collect([('a', 1), ('b', 2)])\nassert out == {'a': 'user-1', 'b': 'user-2'}",
                 "Create tasks per pair; await them; zip keys with results."),
                ("keys stay paired regardless of finish order",
                 "out = run_collect([('x', 3), ('y', 1), ('z', 2)])\nassert out == {'x': 'user-3', 'y': 'user-1', 'z': 'user-2'}",
                 "Never rely on completion order — pair explicitly."),
            ],
            level="combination",
        ),
    ],
    {
        "pi10-tk-concurrent": vi_challenge("Đồng thời vs Tuần tự", "Viết async def slow_double(n) await asyncio.sleep(0.1) và trả về n*2. Sau đó async def run_concurrent(values) dùng asyncio.create_task cho mỗi giá trị và await toàn bộ task. Cung cấp wrapper sync run_all(values) trả về list kết quả (theo thứ tự input).", [("Kết quả khớp thứ tự input", "Thu từng task bằng await; thứ tự task = thứ tự kết quả ở đây."), ("Thực sự đồng thời (nhanh, không chậm gấp 3)", "Bốn lần chờ 0.1s chồng nhau phải xong dưới 0.4s.")]),
        "pi10-tk-pairs": vi_challenge("Ghép Kết quả với Input", "Viết async def fetch_name(user_id) await sleep(0.02) và trả về f'user-{user_id}'. Viết async def collect(pairs) với pairs là list các tuple (key, user_id): chạy mọi fetch đồng thời và trả về dict key -> tên lấy được. Cung cấp wrapper sync run_collect(pairs).", [("Key map tới tên lấy được", "Tạo task cho từng cặp; await chúng; zip key với kết quả."), ("Key không bao giờ lệch cặp dù thứ tự hoàn thành khác", "Đừng dựa vào thứ tự hoàn thành — ghép tường minh.")]),
    },
    solutions=[
        ("pi10-tk-concurrent", "import asyncio\n\nasync def slow_double(n):\n    await asyncio.sleep(0.1)\n    return n * 2\n\nasync def run_concurrent(values):\n    tasks = [asyncio.create_task(slow_double(v)) for v in values]\n    return [await t for t in tasks]\n\ndef run_all(values):\n    return asyncio.run(run_concurrent(values))", "import asyncio\n\nasync def slow_double(n):\n    await asyncio.sleep(0.1)\n    return n * 2\n\nasync def run_concurrent(values):\n    results = []\n    for v in values:\n        results.append(await slow_double(v))\n    return results\n\ndef run_all(values):\n    return asyncio.run(run_concurrent(values))"),
        ("pi10-tk-pairs", "import asyncio\n\nasync def fetch_name(user_id):\n    await asyncio.sleep(0.02)\n    return f'user-{user_id}'\n\nasync def collect(pairs):\n    tasks = {key: asyncio.create_task(fetch_name(uid)) for key, uid in pairs}\n    return {key: await task for key, task in tasks.items()}\n\ndef run_collect(pairs):\n    return asyncio.run(collect(pairs))", "import asyncio\n\nasync def fetch_name(user_id):\n    await asyncio.sleep(0.02)\n    return f'user-{user_id}'\n\nasync def collect(pairs):\n    out = {}\n    for key, uid in pairs:\n        out[key] = await fetch_name(uid)\n    return out\n\ndef run_collect(pairs):\n    return asyncio.run(collect(pairs))"),
    ],
)

write_practice(
    M10, "m10-gather-practice",
    "gather and Timeout Drills",
    "Collect what you can; never wait forever.",
    "Luyện gather và Timeout",
    "Gom được gì hay nấy; không bao giờ chờ vĩnh viễn.",
    L10C, 30, "intermediate",
    [
        challenge(
            "pi10-gt-collect", "Collect What You Can",
            "Implement async def gather_all(jobs) where jobs are coroutines that may raise. Use asyncio.gather(..., return_exceptions=True) and return (successes, failures): successes is the list of non-exception results in order; failures is the list of exception instances in order. Provide sync wrapper run_collect(jobs).",
            "import asyncio\n\nasync def gather_all(jobs):\n    pass\n\ndef run_collect(jobs):\n    pass\n",
            [
                ("separates results from failures",
                 "async def ok():\n    return 1\nasync def bad():\n    raise ValueError('x')\nsucc, fail = run_collect([ok(), bad(), ok()])\nassert succ == [1, 1]\nassert len(fail) == 1 and isinstance(fail[0], ValueError)",
                 "return_exceptions=True turns errors into values to partition."),
                ("empty input",
                 "assert run_collect([]) == ([], [])",
                 "Nothing in, nothing out — both empty."),
            ],
            level="guided",
        ),
        challenge(
            "pi10-gt-timeout", "Bounded Waits",
            "Implement async def with_deadline(coro, seconds) awaiting asyncio.wait_for(coro, timeout=seconds) and returning ('ok', result) on success or ('timeout', None) on asyncio.TimeoutError. Provide sync wrapper run_deadline(coro, seconds).",
            "import asyncio\n\nasync def with_deadline(coro, seconds):\n    pass\n\ndef run_deadline(coro, seconds):\n    pass\n",
            [
                ("fast job succeeds",
                 "async def quick():\n    await asyncio.sleep(0.01)\n    return 'done'\nassert run_deadline(quick(), 1) == ('ok', 'done')",
                 "wait_for passes results through."),
                ("slow job times out",
                 "async def slow():\n    await asyncio.sleep(5)\n    return 'late'\nstatus, value = run_deadline(slow(), 0.05)\nassert status == 'timeout' and value is None",
                 "TimeoutError becomes ('timeout', None) — never a hang."),
            ],
            level="independent",
        ),
    ],
    {
        "pi10-gt-collect": vi_challenge("Gom được gì hay nấy", "Viết async def gather_all(jobs) với jobs là các coroutine có thể raise. Dùng asyncio.gather(..., return_exceptions=True) và trả về (successes, failures): successes là list kết quả không-phải-exception theo thứ tự; failures là list các exception theo thứ tự. Cung cấp wrapper sync run_collect(jobs).", [("Tách kết quả khỏi thất bại", "return_exceptions=True biến lỗi thành giá trị để phân loại."), ("Input rỗng", "Không vào, không ra — cả hai rỗng.")]),
        "pi10-gt-timeout": vi_challenge("Chờ có giới hạn", "Viết async def with_deadline(coro, seconds) await asyncio.wait_for(coro, timeout=seconds) và trả về ('ok', result) khi thành công hoặc ('timeout', None) khi gặp asyncio.TimeoutError. Cung cấp wrapper sync run_deadline(coro, seconds).", [("Việc nhanh thành công", "wait_for cho kết quả đi qua."), ("Việc chậm bị timeout", "TimeoutError trở thành ('timeout', None) — không bao giờ treo.")]),
    },
    solutions=[
        ("pi10-gt-collect", "import asyncio\n\nasync def gather_all(jobs):\n    results = await asyncio.gather(*jobs, return_exceptions=True)\n    successes = [r for r in results if not isinstance(r, BaseException)]\n    failures = [r for r in results if isinstance(r, BaseException)]\n    return successes, failures\n\ndef run_collect(jobs):\n    return asyncio.run(gather_all(jobs))", "import asyncio\n\nasync def gather_all(jobs):\n    results = await asyncio.gather(*jobs)\n    return results, []\n\ndef run_collect(jobs):\n    return asyncio.run(gather_all(jobs))"),
        ("pi10-gt-timeout", "import asyncio\n\nasync def with_deadline(coro, seconds):\n    try:\n        result = await asyncio.wait_for(coro, timeout=seconds)\n        return ('ok', result)\n    except asyncio.TimeoutError:\n        return ('timeout', None)\n\ndef run_deadline(coro, seconds):\n    return asyncio.run(with_deadline(coro, seconds))", "import asyncio\n\nasync def with_deadline(coro, seconds):\n    result = await asyncio.wait_for(coro, timeout=seconds)\n    return ('ok', result)\n\ndef run_deadline(coro, seconds):\n    return asyncio.run(with_deadline(coro, seconds))"),
    ],
)

# --- module 10 checkpoint ---
write_checkpoint(
    M10, L10D,
    "Checkpoint: Concurrent Data Collector",
    "Fetch many sources at once — failures and timeouts are data, not crashes.",
    20,
    """
The capstone of concurrency practice: many simulated sources, some slow,
some broken. Collect everything recoverable, classify the rest, finish fast.

**Working with AI:** ask "where could this collector hang forever?" — every
await without a bound is a suspect.
""",
    "Checkpoint: Bộ gom dữ liệu đồng thời",
    "Lấy nhiều nguồn cùng lúc — lỗi và timeout là dữ liệu, không phải crash.",
    """
Đỉnh của việc luyện đồng thời: nhiều nguồn mô phỏng, có cái chậm, có cái
hỏng. Gom mọi thứ cứu được, phân loại phần còn lại, kết thúc nhanh.

**Làm việc cùng AI:** hãy hỏi "bộ gom này có thể treo vĩnh viễn ở đâu?" —
mỗi await không có giới hạn đều là nghi phạm.
""",
    challenge(
        "pi10-ckpt-collector", "Source Collector",
        "Implement sync collect(sources) where sources is a list of dicts: {'name': str, 'delay': float, 'fail': bool(optional)}. Each source simulates a fetch: async job awaiting delay then raising RuntimeError(name) if fail else returning (name, 'data'). Run ALL concurrently with a per-source timeout of 0.5s (asyncio.wait_for). Return a dict with keys 'ok' (list of names that returned data, in input order) and 'failed' (sorted list of names that raised or timed out).",
        "import asyncio\n\ndef collect(sources):\n    pass\n",
        [
            ("happy sources report ok",
             "srcs = [{'name': 'a', 'delay': 0.01}, {'name': 'b', 'delay': 0.01}]\nout = collect(srcs)\nassert out['ok'] == ['a', 'b'] and out['failed'] == []",
             "Both succeed; results ordered by input order."),
            ("failing source lands in failed",
             "srcs = [{'name': 'good', 'delay': 0.01}, {'name': 'bad', 'delay': 0.01, 'fail': True}]\nout = collect(srcs)\nassert out['ok'] == ['good'] and out['failed'] == ['bad']",
             "RuntimeError from a source → failed list."),
            ("slow source times out into failed",
             "srcs = [{'name': 'slow', 'delay': 2.0}, {'name': 'fast', 'delay': 0.01}]\nout = collect(srcs)\nassert out['failed'] == ['slow'] and out['ok'] == ['fast']",
             "Per-source timeout 0.5s — the 2s source must not stall the run."),
            ("run finishes quickly despite a slow source",
             "import time\nsrcs = [{'name': 'slow', 'delay': 5.0}, {'name': 'f', 'delay': 0.01}]\nstart = time.monotonic()\ncollect(srcs)\nassert time.monotonic() - start < 2.0",
             "Timeout keeps the whole run bounded (~0.5s, not 5s)."),
        ],
        difficulty="intermediate",
    ),
    vi_challenge(
        "Bộ gom nguồn",
        "Viết sync collect(sources) với sources là list các dict: {'name': str, 'delay': float, 'fail': bool(tùy chọn)}. Mỗi nguồn mô phỏng một lần lấy dữ liệu: async job await delay rồi raise RuntimeError(name) nếu fail, ngược lại trả về (name, 'data'). Chạy TẤT CẢ đồng thời với timeout 0.5s cho từng nguồn (asyncio.wait_for). Trả về dict với key 'ok' (list tên trả về dữ liệu, theo thứ tự input) và 'failed' (list đã sắp các tên bị raise hoặc timeout).",
        [
            ("Nguồn tốt được báo ok", "Cả hai thành công; kết quả theo thứ tự input."),
            ("Nguồn lỗi rơi vào failed", "RuntimeError từ nguồn → danh sách failed."),
            ("Nguồn chậm timeout vào failed", "Timeout từng nguồn 0.5s — nguồn 2s không được làm chậm cả lần chạy."),
            ("Lần chạy kết thúc nhanh dù có nguồn chậm", "Timeout giữ toàn bộ lần chạy trong giới hạn (~0.5s, không phải 5s)."),
        ],
    ),
    solution="import asyncio\n\ndef collect(sources):\n    async def job(src):\n        await asyncio.sleep(src['delay'])\n        if src.get('fail'):\n            raise RuntimeError(src['name'])\n        return src['name']\n\n    async def runner():\n        jobs = [asyncio.create_task(job(s)) for s in sources]\n        results = await asyncio.gather(\n            *(asyncio.wait_for(j, timeout=0.5) for j in jobs),\n            return_exceptions=True,\n        )\n        ok = []\n        failed = set()\n        for src, res in zip(sources, results):\n            if isinstance(res, BaseException):\n                failed.add(src['name'])\n            else:\n                ok.append(res)\n        return {'ok': ok, 'failed': sorted(failed)}\n\n    return asyncio.run(runner())",
    wrong="import asyncio\n\ndef collect(sources):\n    async def job(src):\n        await asyncio.sleep(src['delay'])\n        if src.get('fail'):\n            raise RuntimeError(src['name'])\n        return src['name']\n\n    async def runner():\n        ok = []\n        failed = []\n        for s in sources:\n            try:\n                ok.append(await job(s))\n            except Exception:\n                failed.append(s['name'])\n        return {'ok': ok, 'failed': sorted(failed)}\n\n    return asyncio.run(runner())",
)

print("modules 9-10 done")
