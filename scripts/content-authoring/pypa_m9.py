#!/usr/bin/env python3
"""Module 9: production-apis — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "production-apis"

# ── lesson 1 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "api-design-contracts",
    "HTTP as a Contract",
    "Status codes, pagination, and idempotency are promises your API makes to every client — design them deliberately, not accidentally.",
    30,
    """
An API is a **contract**. Two teams that never meet — your backend and someone
else's client — coordinate entirely through the shapes and statuses you commit
to. Advanced API design is mostly contract hygiene.

## Status codes are vocabulary, not decoration

Pick from a small set and use them precisely:

| Status | Means | Typical trigger |
|---|---|---|
| 200 | success with body | GET/PUT that returns data |
| 201 | created | POST created a resource (return its location) |
| 204 | success, no body | DELETE |
| 400 | malformed request | unparseable body / params |
| 401 | who are you? | missing/invalid credentials |
| 403 | I know you, but no | authenticated, not allowed |
| 404 | no such resource | unknown id or path |
| 409 | conflict | duplicate, stale version, impossible state |
| 422 | understood but invalid | failed validation |
| 429 | slow down | rate limit exceeded |

Two rules that separate professional APIs from accidental ones:

1. **401 vs 403 vs 404 are different sentences.** Collapsing them all into 400
   destroys the client's ability to react ("re-authenticate" vs "give up" vs
   "fix the URL").
2. **Never leak internals on 5xx.** A 500 whose body contains a stack trace or
   SQL fragment is a gift to an attacker. Return a generic envelope; log the
   detail server-side.

## Error envelope: one shape for every failure

Clients write one error handler when every failure looks the same:

```json
{
  "error": {
    "status": 422,
    "title": "validation_failed",
    "detail": "email is not a valid address",
    "field": "email"
  }
}
```

`field` only exists for field-scoped problems. The detail for 5xx errors is a
*generic* string — the specifics go to your logs, not the wire.

## Idempotency: what a retry is allowed to do

Networks fail *after* your handler ran. A client that retries must not
double-charge. Classify methods by what a retry does:

- **Idempotent:** `GET`, `PUT`, `DELETE` — repeating them converges to the same
  state. `DELETE` twice = still deleted. `PUT` twice = same representation.
- **Not idempotent:** `POST` — two identical POSTs may create two resources.

Two standard fixes for non-idempotent operations:

- **Idempotency keys:** the client sends `Idempotency-Key: <uuid>`; the server
  remembers the first response for that key and *replays* it on retry instead
  of re-executing.
- **Natural keys:** make the resource itself unique (`UNIQUE(email)`), so the
  second insert fails safely with 409.

## Pagination is part of the contract

Every list endpoint needs a deterministic slice. Offset pagination
(`?page=2&per_page=50`) is simple and cacheable; cursor pagination survives
concurrent inserts. Whichever you pick, the response carries its own metadata —
`total`, `page`, `per_page`, `has_next` — so clients never count items.

## Versioning is an admission

`/v1/` in the path says: *this contract will change someday, and old clients
deserve a stable copy.* You are not designing endpoints; you are designing a
succession of contracts.
""",
    "HTTP như một hợp đồng",
    "Mã trạng thái, phân trang và tính idempotent là những lời hứa API dành cho mọi client — hãy thiết kế chúng một cách chủ đích.",
    """
API là một **hợp đồng**. Hai đội không bao giờ gặp nhau — backend của bạn và
client của người khác — phối hợp với nhau hoàn toàn qua các shape và mã trạng
thái mà bạn cam kết. Thiết kế API nâng cao phần lớn là giữ vệ sinh hợp đồng.

## Mã trạng thái là từ vựng, không phải trang trí

Chọn từ một tập nhỏ và dùng chính xác:

| Mã | Nghĩa | Trường hợp điển hình |
|---|---|---|
| 200 | thành công, có body | GET/PUT trả dữ liệu |
| 201 | đã tạo | POST tạo tài nguyên (trả về vị trí của nó) |
| 204 | thành công, không body | DELETE |
| 400 | request sai định dạng | body/params không parse được |
| 401 | bạn là ai? | thiếu/sai thông tin xác thực |
| 403 | tôi biết bạn, nhưng không | đã xác thực, không đủ quyền |
| 404 | không có tài nguyên đó | id hoặc path lạ |
| 409 | xung đột | trùng, phiên bản cũ, trạng thái không thể |
| 422 | hiểu rồi nhưng không hợp lệ | fail validation |
| 429 | chậm lại thôi | vượt rate limit |

Hai nguyên tắc tách API chuyên nghiệp khỏi API "tự nhiên mà có":

1. **401 / 403 / 404 là ba câu nói khác nhau.** Gộp chung thành 400 thì client
   mất khả năng phản ứng ("đăng nhập lại" hay "bỏ cuộc" hay "sửa URL").
2. **Không bao giờ lộ nội bộ qua 5xx.** Một 500 có stack trace hay mảnh SQL
   trong body là món quà cho kẻ tấn công. Trả envelope chung chung; chi tiết
   chỉ nằm ở log phía server.

## Error envelope: một shape cho mọi lỗi

Client chỉ viết một trình xử lý lỗi khi mọi lỗi trông giống nhau:

```json
{
  "error": {
    "status": 422,
    "title": "validation_failed",
    "detail": "email is not a valid address",
    "field": "email"
  }
}
```

`field` chỉ xuất hiện với lỗi thuộc về một field cụ thể. `detail` của lỗi 5xx
là chuỗi *chung chung* — chi tiết đi vào log, không lên đường truyền.

## Idempotency: một lần retry được phép làm gì

Mạng có thể đứt *sau khi* handler của bạn đã chạy. Client retry không được
trừ tiền hai lần. Phân loại method theo hành vi của retry:

- **Idempotent:** `GET`, `PUT`, `DELETE` — lặp lại hội tụ về cùng một trạng
  thái. `DELETE` hai lần = vẫn đã xóa. `PUT` hai lần = cùng một biểu diễn.
- **Không idempotent:** `POST` — hai POST giống nhau có thể tạo hai tài nguyên.

Hai cách chuẩn hóa cho thao tác không idempotent:

- **Idempotency key:** client gửi `Idempotency-Key: <uuid>`; server nhớ phản
  hồi đầu tiên cho key đó và *phát lại* nó khi retry thay vì thực thi lại.
- **Natural key:** làm tài nguyên tự unique (`UNIQUE(email)`) để lần chèn thứ
  hai fail an toàn với 409.

## Phân trang cũng là một phần của hợp đồng

Mọi list endpoint cần một cách cắt dữ liệu xác định. Offset pagination
(`?page=2&per_page=50`) đơn giản, dễ cache; cursor pagination chịu được khi dữ
liệu chèn thêm liên tục. Chọn kiểu nào thì response cũng phải mang metadata của
chính nó — `total`, `page`, `per_page`, `has_next` — để client không phải đếm.

## Versioning là một lời thú nhận

`/v1/` trong path nghĩa là: *hợp đồng này sẽ thay đổi một ngày nào đó, và các
client cũ xứng đáng có một bản ổn định.* Bạn không thiết kế endpoint; bạn
thiết kế một dòng kế thừa các hợp đồng.
""",
)

# ── lesson 2 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "validation-and-errors",
    "Validation at the Boundary",
    "Parse, don't validate: turn untrusted input into typed values once, at the edge, so the core of your application only ever sees valid data.",
    28,
    """
Untrusted bytes arrive at your edge; your core logic deserves typed, verified
values. The boundary's whole job is that translation — and doing it *once*.

## Parse, don't validate

Anti-pattern: every function re-checks `if user is not None` because nobody is
sure where validation happened. The fix is a boundary function that returns
either a **clean, typed value** or a **complete set of problems**:

```python
def validate_user(payload: dict) -> tuple[dict, list[dict]]:
    clean, errors = {}, []
    # ... normalize + check every field ...
    return clean, errors   # errors == []  <=>  payload accepted
```

Inside the application, `clean` carries a guarantee: every field present,
normalized (`email` lowercased and stripped), typed. No core function ever
re-validates. The guarantee *is* the architecture.

## Collect all the errors

A form that reports one error per submit is a form users submit ten times.
Validate every field, gather everything, report once. The envelope from the
previous lesson carries one entry per problem:

```json
{"error": {"status": 422, "title": "validation_failed",
           "detail": "3 fields invalid",
           "fields": [{"field": "email", "detail": "..."}, ...]}}
```

## Normalization is half of validation

`"  A@Example.COM "` and `"a@example.com"` are the same address. Normalize
*before* checking (strip, case-fold, coerce numeric strings) so the check sees
canonical data — and so equal inputs can't sneak past as unequal.

## Fail closed, loudly

- Unknown fields: reject (they're probably typos of real fields) — or at minimum
  never *trust* them.
- Exceptions at the boundary become 422/400 envelopes, never 500s. A 500 means
  *your* bug; a 422 means *their* input. Blurring that trains clients to ignore
  your errors.
- Log validation failures at debug level without the full payload — payloads
  contain passwords.

## The DI seam

Handlers should receive their dependencies (repositories, mailers, clocks) as
**parameters**, not import singletons. That single decision makes the handler
unit-testable: the test passes a fake repository and no database exists anywhere.
We'll exercise that seam in the checkpoint.
""",
    "Validation tại ranh giới",
    "Parse, đừng validate: biến dữ liệu không tin cậy thành giá trị có kiểu đúng một lần, tại mép vào, để phần lõi ứng dụng chỉ nhìn thấy dữ liệu hợp lệ.",
    """
Các byte không tin cậy đến tại mép vào; phần lõi của bạn xứng đáng nhận giá trị
đã kiểu hóa, đã kiểm chứng. Toàn bộ công việc của ranh giới là sự dịch thuật
đó — và chỉ làm *một lần*.

## Parse, đừng validate

Chống-pattern: mọi hàm đều phải kiểm tra lại `if user is not None` vì không ai
chắc validation xảy ra ở đâu. Cách sửa là một hàm ranh giới trả về hoặc **giá
trị sạch, có kiểu** hoặc **trọn bộ vấn đề**:

```python
def validate_user(payload: dict) -> tuple[dict, list[dict]]:
    clean, errors = {}, []
    # ... chuẩn hóa + kiểm tra từng field ...
    return clean, errors   # errors == []  <=>  payload được chấp nhận
```

Bên trong ứng dụng, `clean` mang một bảo đảm: đủ field, đã chuẩn hóa (`email`
được strip và viết thường), đúng kiểu. Không hàm lõi nào phải validate lại.
Bảo đảm đó *chính là* kiến trúc.

## Thu thập tất cả lỗi

Một form chỉ báo một lỗi mỗi lần submit là một form người dùng phải submit mười
lần. Validate mọi field, gom đủ, báo một lần. Envelope của bài trước mang một
entry cho mỗi vấn đề:

```json
{"error": {"status": 422, "title": "validation_failed",
           "detail": "3 fields invalid",
           "fields": [{"field": "email", "detail": "..."}, ...]}}
```

## Chuẩn hóa là một nửa của validation

`"  A@Example.COM "` và `"a@example.com"` là cùng một địa chỉ. Chuẩn hóa
*trước khi* kiểm tra (strip, viết thường, coerce chuỗi số) để phép kiểm tra
nhìn thấy dữ liệu chuẩn — và để hai đầu vào bằng nhau không lọt qua như khác
nhau.

## Fail closed, fail ầm ĩ

- Field lạ: từ chối (rất có thể là lỗi chính tả của field thật) — hoặc ít nhất
  không bao giờ *tin* chúng.
- Exception tại ranh giới trở thành envelope 422/400, không bao giờ 500. Một
  500 nghĩa là *lỗi của bạn*; một 422 nghĩa là *đầu vào của họ*. Trộn lẫn hai
  điều đó sẽ dạy client phớt lờ lỗi của bạn.
- Log lỗi validation ở mức debug, không kèm toàn bộ payload — payload chứa
  mật khẩu.

## Điểm seam của DI

Handler nên nhận các dependency (repository, mailer, clock) qua **tham số**,
không import singleton. Một quyết định duy nhất đó khiến handler test được ở
mức unit: test truyền một repository giả, và không có database nào tồn tại
trong bài test. Checkpoint sẽ luyện đúng điểm seam đó.
""",
)

# ── lesson 3 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "production-concerns",
    "The Production Concerns",
    "Rate limiting, health checks, graceful degradation, and idempotent writes — the unglamorous machinery that separates a demo from a service.",
    30,
    """
A demo handles the happy path. A service survives Tuesday at 10:00. The gap is
a handful of small mechanisms — each one a function, not a framework.

## Rate limiting: the token bucket

The classic algorithm is small enough to memorize:

```python
class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate, self.capacity = rate, capacity      # tokens/sec, burst size
        self.tokens, self.updated = capacity, 0.0

    def allow(self, now):
        self.tokens = min(self.capacity,
                          self.tokens + (now - self.updated) * self.rate)
        self.updated = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

Requests refill capacity `rate` tokens per second; each request spends one.
Bursts up to `capacity` pass instantly, sustained load is capped at `rate`, and
the answer for "too fast" is **429**. Note the design trick: `now` is a
parameter — the bucket is *deterministic* and testable, because time is
injected.

## Health checks: liveness vs readiness

- **Liveness** (`/healthz`): "is the process alive?" — always 200 unless the
  process is wedged. Restart me if not.
- **Readiness** (`/readyz`): "can I serve *right now*?" — checks each
  dependency (database ping, cache ping). Any failure → 503, and the load
  balancer stops routing traffic here *without killing the process*.

A readiness probe that crashes on a failed dependency defeats its own purpose:
it must catch, record, and report — `{"ready": false, "checks": {"db": false}}`.

## Graceful degradation

When a non-critical dependency dies, the service should lose a feature, not its
life. Recommendations unavailable? Serve the product page anyway. The pattern:
classify dependencies as critical (fail the request) or optional (fail the
feature), and make the *classification* explicit in code.

## Idempotent writes with an idempotency store

```python
class IdempotencyStore:
    def __init__(self):
        self._done = {}

    def execute(self, key, fn):
        if key not in self._done:
            self._done[key] = fn()
        return self._done[key]
```

First call with a key runs `fn`; every retry with the same key replays the
recorded response. `fn` must run *exactly once* — that's the entire contract,
and it is worth writing a test that counts invocations.

## Transactions & the pool (a look ahead)

Two handlers sharing one connection corrupt each other's transactions; a
connection *pool* lends short-lived connections out. And any multi-write
operation belongs in a transaction — all its writes commit together or none do.
We go deep on this in the databases module; here the takeaway is architectural:
*the handler declares the unit of work, the pool/transaction machinery owns the
connection.*
""",
    "Những mối quan tâm của production",
    "Rate limiting, health check, graceful degradation và ghi idempotent — những cơ chế ít hoa mỹ nhưng tách một bản demo khỏi một dịch vụ thật.",
    """
Một bản demo chỉ xử lý happy path. Một dịch vụ phải sống sót qua 10 giờ sáng
ngày thứ ba. Khoảng cách đó là một nắm cơ chế nhỏ — mỗi cơ chế là một hàm,
không phải một framework.

## Rate limiting: token bucket

Thuật toán cổ điển nhỏ đến mức có thể thuộc lòng:

```python
class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate, self.capacity = rate, capacity      # token/giây, sức chứa burst
        self.tokens, self.updated = capacity, 0.0

    def allow(self, now):
        self.tokens = min(self.capacity,
                          self.tokens + (now - self.updated) * self.rate)
        self.updated = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

Requests được nạp lại `rate` token mỗi giây; mỗi request tốn một token. Burst
tới `capacity` đi qua ngay lập tức, tải kéo dài bị chặn ở `rate`, và câu trả
lời cho "nhanh quá" là **429**. Chú ý mánh thiết kế: `now` là tham số — bucket
*xác định được* và test được, vì thời gian được tiêm vào.

## Health check: liveness và readiness

- **Liveness** (`/healthz`): "tiến trình còn sống không?" — luôn 200 trừ khi
  tiến trình bị treo. Không sống thì khởi động lại tôi.
- **Readiness** (`/readyz`): "ngay lúc này tôi có phục vụ được không?" — kiểm
  tra từng dependency (ping database, ping cache). Bất kỳ lỗi nào → 503, và
  load balancer ngừng routing traffic tới đây *mà không giết tiến trình*.

Một readiness probe crash khi dependency hỏng là tự đánh bại mục đích của chính
nó: nó phải catch, ghi nhận và báo cáo — `{"ready": false, "checks": {"db": false}}`.

## Graceful degradation

Khi một dependency không-critical chết, dịch vụ nên mất một tính năng, không
mất mạng sống. Gợi ý sản phẩm không khả dụng? Vẫn phục vụ trang sản phẩm.
Pattern: phân loại dependency thành critical (làm fail request) hoặc optional
(làm fail tính năng), và **sự phân loại** đó phải hiện rõ trong code.

## Ghi idempotent với idempotency store

```python
class IdempotencyStore:
    def __init__(self):
        self._done = {}

    def execute(self, key, fn):
        if key not in self._done:
            self._done[key] = fn()
        return self._done[key]
```

Lần đầu với một key thì chạy `fn`; mọi retry với cùng key phát lại phản hồi đã
ghi. `fn` phải chạy *đúng một lần* — đó là toàn bộ hợp đồng, và nó xứng đáng có
một bài test đếm số lần gọi.

## Transaction và pool (nhìn trước)

Hai handler dùng chung một kết nối sẽ hỏng transaction của nhau; một connection
*pool* cho mượn các kết nối ngắn hạn. Và mọi thao tác ghi-nhiều-lần thuộc về
một transaction — tất cả các ghi commit cùng nhau hoặc không cái nào. Module
databases sẽ đi sâu phần này; ở đây chỉ cần ghi nhớ về mặt kiến trúc: *handler
khai báo đơn vị công việc, cơ chế pool/transaction sở hữu kết nối.*
""",
)

# ── practice 1: design contract ──────────────────────────────────────────────
ERROR_REF = (
    "TITLES = {\n"
    "    400: 'bad_request',\n"
    "    404: 'not_found',\n"
    "    409: 'conflict',\n"
    "    422: 'validation_failed',\n"
    "    429: 'rate_limited',\n"
    "    500: 'internal_error',\n"
    "}\n"
    "\n"
    "\n"
    "def error_envelope(status, detail=None, field=None):\n"
    "    envelope = {\n"
    "        'error': {\n"
    "            'status': status,\n"
    "            'title': TITLES[status],\n"
    "        }\n"
    "    }\n"
    "    if field is not None:\n"
    "        envelope['error']['field'] = field\n"
    "    if status >= 500:\n"
    "        envelope['error']['detail'] = 'an unexpected error occurred'\n"
    "    elif detail is not None:\n"
    "        envelope['error']['detail'] = detail\n"
    "    return envelope\n"
)
ERROR_WRONG = (
    "TITLES = {\n"
    "    400: 'bad_request',\n"
    "    404: 'not_found',\n"
    "    409: 'conflict',\n"
    "    422: 'validation_failed',\n"
    "    429: 'rate_limited',\n"
    "    500: 'internal_error',\n"
    "}\n"
    "\n"
    "\n"
    "def error_envelope(status, detail=None, field=None):\n"
    "    envelope = {\n"
    "        'error': {\n"
    "            'status': status,\n"
    "            'title': TITLES[status],\n"
    "        }\n"
    "    }\n"
    "    if field is not None:\n"
    "        envelope['error']['field'] = field\n"
    "    if detail is not None:\n"
    "        # WRONG: echoes internals to the wire, even for 5xx\n"
    "        envelope['error']['detail'] = detail\n"
    "    return envelope\n"
)

PAGINATE_REF = (
    "def paginate(items, page=1, per_page=20):\n"
    "    if not isinstance(page, int) or page < 1:\n"
    "        raise ValueError('page must be a positive integer')\n"
    "    if not isinstance(per_page, int) or not (1 <= per_page <= 100):\n"
    "        raise ValueError('per_page must be between 1 and 100')\n"
    "    total = len(items)\n"
    "    total_pages = max(1, -(-total // per_page))\n"
    "    start = (page - 1) * per_page\n"
    "    window = items[start:start + per_page]\n"
    "    return {\n"
    "        'items': window,\n"
    "        'page': page,\n"
    "        'per_page': per_page,\n"
    "        'total': total,\n"
    "        'total_pages': total_pages,\n"
    "        'has_next': page < total_pages,\n"
    "        'has_prev': page > 1,\n"
    "    }\n"
)
PAGINATE_WRONG = (
    "def paginate(items, page=1, per_page=20):\n"
    "    if not isinstance(page, int) or page < 1:\n"
    "        raise ValueError('page must be a positive integer')\n"
    "    if not isinstance(per_page, int) or not (1 <= per_page <= 100):\n"
    "        raise ValueError('per_page must be between 1 and 100')\n"
    "    total = len(items)\n"
    "    total_pages = max(1, -(-total // per_page))\n"
    "    start = (page - 1) * per_page\n"
    "    window = items[start:start + per_page]\n"
    "    return {\n"
    "        'items': window,\n"
    "        'page': page,\n"
    "        'per_page': per_page,\n"
    "        'total': total,\n"
    "        'total_pages': total_pages,\n"
    "        'has_next': page <= total_pages,  # WRONG: off-by-one\n"
    "        'has_prev': page > 1,\n"
    "    }\n"
)

write_practice(
    MOD, "pa-p9-design-practice",
    "Contract Drills",
    "Encode the HTTP contract in code: error envelopes that never leak internals, and pagination metadata that clients can trust.",
    "Bài tập về hợp đồng",
    "Đưa hợp đồng HTTP vào code: error envelope không bao giờ lộ nội bộ, và metadata phân trang mà client có thể tin tưởng.",
    "api-design-contracts", 22, "intermediate",
    [
        challenge(
            "pa-api-error-envelope",
            "The error envelope that tells no secrets",
            "Implement `error_envelope(status, detail=None, field=None)` returning `{'error': {...}}` where:\n\n- `status` is echoed and `title` comes from this fixed table: 400 bad_request, 404 not_found, 409 conflict, 422 validation_failed, 429 rate_limited, 500 internal_error\n- `field` is included only when not None\n- `detail` is included when given — EXCEPT for statuses >= 500, where detail is always the generic string `'an unexpected error occurred'` (internals must never reach the wire)",
            "# TODO: fixed title table + error_envelope",
            [
                ("4xx detail passes through, 5xx detail is generic",
                 "assert error_envelope(422, 'email is not valid', 'email') == {'error': {'status': 422, 'title': 'validation_failed', 'field': 'email', 'detail': 'email is not valid'}}\nassert error_envelope(404, 'no such widget')['error']['title'] == 'not_found'\nassert error_envelope(500, 'secrets: ConnectionRefused at db-7')['error']['detail'] == 'an unexpected error occurred'\nassert error_envelope(500)['error'] == {'status': 500, 'title': 'internal_error', 'detail': 'an unexpected error occurred'}\nprint('ok')",
                 "Build the dict, then decide what detail survives for each status band."),
                ("field appears only when given",
                 "assert 'field' not in error_envelope(409, 'duplicate email')['error']\nassert error_envelope(400, 'bad json', 'body')['error']['field'] == 'body'\nprint('ok')",
                 "One optional key, conditional presence."),
            ],
            level="independent",
        ),
        challenge(
            "pa-api-paginate",
            "Pagination with honest metadata",
            "Implement `paginate(items, page=1, per_page=20)` returning a dict with `items` (the window), `page`, `per_page`, `total`, `total_pages` (minimum 1), `has_next` (there are items after this window), `has_prev` (page > 1).\n\n- raise `ValueError` when `page < 1` or `per_page` outside 1..100 (ints only)\n- an empty list is 1 page with `has_next=False`",
            "# TODO: paginate",
            [
                ("windows and metadata agree",
                 "items = list(range(25))\np1 = paginate(items, 1, 10)\nassert p1['items'] == list(range(10)) and p1['total'] == 25 and p1['total_pages'] == 3\nassert p1['has_next'] is True and p1['has_prev'] is False\np3 = paginate(items, 3, 10)\nassert p3['items'] == [20, 21, 22, 23, 24] and p3['has_next'] is False and p3['has_prev'] is True\nprint('ok')",
                 "ceil(total/per_page) pages; the last window may be short."),
                ("empty lists and rejected params",
                 "e = paginate([], 1, 20)\nassert e['total'] == 0 and e['total_pages'] == 1 and e['has_next'] is False\nfor bad in [(0, 10), (2, 0), (1, 101)]:\n    try:\n        paginate(list(range(5)), bad[0], bad[1])\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(bad)\nprint('ok')",
                 "Reject the contract violations; empty input is valid, not an error."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-api-error-envelope": vi_challenge(
            "Envelope lỗi không tiết lộ bí mật",
            "Cài `error_envelope(status, detail=None, field=None)` trả `{'error': {...}}` với:\n\n- `status` được phản chiếu và `title` lấy từ bảng cố định: 400 bad_request, 404 not_found, 409 conflict, 422 validation_failed, 429 rate_limited, 500 internal_error\n- `field` chỉ xuất hiện khi khác None\n- `detail` được đưa vào khi có — TRỪ các status >= 500, khi đó detail luôn là chuỗi chung `'an unexpected error occurred'` (nội bộ không bao giờ lên đường truyền)",
            [("4xx giữ nguyên detail, 5xx dùng detail chung", "Dựng dict, rồi quyết định detail nào được sống sót theo từng dải status."),
             ("field chỉ xuất hiện khi được truyền", "Một key tùy chọn, hiện diện có điều kiện.")],
        ),
        "pa-api-paginate": vi_challenge(
            "Phân trang với metadata trung thực",
            "Cài `paginate(items, page=1, per_page=20)` trả dict gồm `items` (cửa sổ), `page`, `per_page`, `total`, `total_pages` (tối thiểu 1), `has_next` (còn item phía sau cửa sổ), `has_prev` (page > 1).\n\n- raise `ValueError` khi `page < 1` hoặc `per_page` ngoài 1..100 (chỉ nhận int)\n- list rỗng là 1 trang với `has_next=False`",
            [("Cửa sổ và metadata phải khớp nhau", "ceil(total/per_page) trang; cửa sổ cuối có thể ngắn hơn."),
             ("Từ chối tham số vi phạm hợp đồng", "Chặn các vi phạm; input rỗng là hợp lệ, không phải lỗi.")],
        ),
    },
    solutions=[("pa-api-error-envelope", ERROR_REF, ERROR_WRONG),
               ("pa-api-paginate", PAGINATE_REF, PAGINATE_WRONG)],
)

# ── practice 2: validation boundary ──────────────────────────────────────────
VALIDATE_REF = (
    "def validate_user(payload):\n"
    "    clean, errors = {}, []\n"
    "    name = payload.get('name')\n"
    "    if not isinstance(name, str) or not name.strip():\n"
    "        errors.append({'field': 'name', 'detail': 'name is required'})\n"
    "    else:\n"
    "        clean['name'] = name.strip()\n"
    "    email = payload.get('email')\n"
    "    if not isinstance(email, str) or '@' not in email:\n"
    "        errors.append({'field': 'email', 'detail': 'email must contain @'})\n"
    "    else:\n"
    "        clean['email'] = email.strip().lower()\n"
    "    age = payload.get('age')\n"
    "    if isinstance(age, str) and age.strip().isdigit():\n"
    "        age = int(age)\n"
    "    if not isinstance(age, int) or isinstance(age, bool) or not (0 <= age <= 150):\n"
    "        errors.append({'field': 'age', 'detail': 'age must be an integer 0..150'})\n"
    "    else:\n"
    "        clean['age'] = age\n"
    "    unknown = set(payload) - {'name', 'email', 'age'}\n"
    "    for field in sorted(unknown):\n"
    "        errors.append({'field': field, 'detail': 'unknown field'})\n"
    "    return clean, errors\n"
)
VALIDATE_WRONG = (
    "def validate_user(payload):\n"
    "    clean, errors = {}, []\n"
    "    name = payload.get('name')\n"
    "    if not isinstance(name, str) or not name.strip():\n"
    "        return {}, [{'field': 'name', 'detail': 'name is required'}]  # WRONG: returns on first error\n"
    "    clean['name'] = name.strip()\n"
    "    email = payload.get('email')\n"
    "    if not isinstance(email, str) or '@' not in email:\n"
    "        errors.append({'field': 'email', 'detail': 'email must contain @'})\n"
    "    else:\n"
    "        clean['email'] = email.strip().lower()\n"
    "    age = payload.get('age')\n"
    "    if isinstance(age, str) and age.strip().isdigit():\n"
    "        age = int(age)\n"
    "    if not isinstance(age, int) or isinstance(age, bool) or not (0 <= age <= 150):\n"
    "        errors.append({'field': 'age', 'detail': 'age must be an integer 0..150'})\n"
    "    else:\n"
    "        clean['age'] = age\n"
    "    unknown = set(payload) - {'name', 'email', 'age'}\n"
    "    for field in sorted(unknown):\n"
    "        errors.append({'field': field, 'detail': 'unknown field'})\n"
    "    return clean, errors\n"
)

BUCKET_REF = (
    "class TokenBucket:\n"
    "    def __init__(self, rate, capacity):\n"
    "        self.rate = float(rate)\n"
    "        self.capacity = float(capacity)\n"
    "        self.tokens = float(capacity)\n"
    "        self.updated = None\n"
    "\n"
    "    def allow(self, now):\n"
    "        if self.updated is None:\n"
    "            self.updated = now\n"
    "        else:\n"
    "            elapsed = max(0.0, now - self.updated)\n"
    "            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)\n"
    "            self.updated = now\n"
    "        if self.tokens >= 1:\n"
    "            self.tokens -= 1\n"
    "            return True\n"
    "        return False\n"
)
BUCKET_WRONG = (
    "class TokenBucket:\n"
    "    def __init__(self, rate, capacity):\n"
    "        self.rate = float(rate)\n"
    "        self.capacity = float(capacity)\n"
    "        self.tokens = float(capacity)\n"
    "        self.updated = None\n"
    "\n"
    "    def allow(self, now):\n"
    "        if self.updated is None:\n"
    "            self.updated = now\n"
    "        else:\n"
    "            elapsed = max(0.0, now - self.updated)\n"
    "            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)\n"
    "            self.updated = now\n"
    "        if self.tokens > 0:  # WRONG: spends fractional tokens, lets bursts exceed capacity\n"
    "            self.tokens -= 1\n"
    "            return True\n"
    "        return False\n"
)

write_practice(
    MOD, "pa-p9-validation-practice",
    "Boundary Drills",
    "Parse, don't validate: a boundary that collects every problem, and a token bucket whose time is injected.",
    "Bài tập ranh giới",
    "Parse, đừng validate: một ranh giới gom đủ mọi vấn đề, và một token bucket có thời gian được tiêm vào.",
    "validation-and-errors", 24, "intermediate",
    [
        challenge(
            "pa-api-validate-user",
            "Collect all the errors",
            "Implement `validate_user(payload)` returning `(clean, errors)`:\n\n- `name`: required non-empty string → stored stripped\n- `email`: required string containing '@' → stored stripped and lowercased\n- `age`: int 0..150 — a digit-string like `'42'` is coerced to int first (bools are NOT ints here)\n- every other key in the payload produces an `{'field': k, 'detail': 'unknown field'}` error, sorted by field name\n- each error is `{'field': ..., 'detail': ...}`; when errors is non-empty, `clean` may only contain fields that passed\n\nThe contract: report ALL problems in one call (collect, don't abort at the first).",
            "# TODO: validate_user — returns (clean, errors)",
            [
                ("valid payload normalizes",
                 "clean, errors = validate_user({'name': '  Lan ', 'email': ' Lan@Example.COM ', 'age': '42'})\nassert errors == []\nassert clean == {'name': 'Lan', 'email': 'lan@example.com', 'age': 42}\nprint('ok')",
                 "Strip and case-fold before checking; coerce digit strings."),
                ("every problem reported exactly once",
                 "clean, errors = validate_user({'name': 'Lan', 'email': 'nope', 'age': 999, 'extra': 1, 'zz': 2})\nassert clean == {'name': 'Lan'}\nfields = [e['field'] for e in errors]\nassert fields == ['age', 'email', 'extra', 'zz'], fields\nmissing = validate_user({})\nassert [e['field'] for e in missing[1]] == ['age', 'email', 'name']\nprint('ok')",
                 "One pass, every field checked, unknowns sorted by name."),
            ],
            level="debugging",
        ),
        challenge(
            "pa-api-rate-limit",
            "The token bucket",
            "Implement `TokenBucket(rate, capacity)` with `allow(now)`:\n\n- refills `rate` tokens per second of elapsed time, capped at `capacity` (first call initializes the clock without refilling)\n- a request succeeds iff at least 1 full token is available; it consumes exactly 1\n- `now` is a float timestamp — never call time functions yourself (the bucket must be deterministic)\n\nBurst of `capacity` at t=0 passes instantly; sustained throughput never exceeds `rate` per second.",
            "class TokenBucket:\n    def __init__(self, rate, capacity):\n        ...\n\n    def allow(self, now):\n        ...",
            [
                ("burst then throttle",
                 "b = TokenBucket(rate=2, capacity=5)\nassert [b.allow(0.0) for _ in range(5)] == [True] * 5\nassert b.allow(0.0) is False\nassert b.allow(0.4) is False   # only 0.8 tokens accrued\nassert b.allow(0.5) is True    # 1.0 tokens accrued\nprint('ok')",
                 "Refill = elapsed * rate, capped at capacity; spend whole tokens only."),
                ("sustained rate holds",
                 "b = TokenBucket(rate=10, capacity=1)\nallowed = sum(b.allow(t / 100) for t in range(100))\nassert allowed == 10, allowed\nprint('ok')",
                 "One token per 0.1s — 100 ticks of 0.01s yield exactly 10."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-api-validate-user": vi_challenge(
            "Gom đủ mọi lỗi",
            "Cài `validate_user(payload)` trả `(clean, errors)`:\n\n- `name`: chuỗi không rỗng bắt buộc → lưu đã strip\n- `email`: chuỗi chứa '@' bắt buộc → lưu đã strip và viết thường\n- `age`: int 0..150 — chuỗi toàn chữ số như `'42'` được coerce thành int trước (bool KHÔNG tính là int ở đây)\n- mọi key khác trong payload sinh lỗi `{'field': k, 'detail': 'unknown field'}`, sắp xếp theo tên field\n- mỗi lỗi có dạng `{'field': ..., 'detail': ...}`; khi errors khác rỗng, `clean` chỉ được chứa các field đã pass\n\nHợp đồng: báo TẤT CẢ vấn đề trong một lần gọi (gom, đừng dừng ở lỗi đầu tiên).",
            [("Payload hợp lệ được chuẩn hóa", "Strip và viết thường trước khi kiểm tra; coerce chuỗi số."),
             ("Báo đủ mọi vấn đề đúng một lần", "Một lượt duy nhất, kiểm tra mọi field, unknowns sắp theo tên.")],
        ),
        "pa-api-rate-limit": vi_challenge(
            "Token bucket",
            "Cài `TokenBucket(rate, capacity)` với `allow(now)`:\n\n- nạp lại `rate` token mỗi giây trôi qua, trần là `capacity` (lần gọi đầu khởi tạo đồng hồ, chưa nạp)\n- request thành công khi và chỉ khi có ít nhất 1 token nguyên; mỗi lần thành công tốn đúng 1\n- `now` là timestamp kiểu float — không được tự gọi hàm thời gian (bucket phải xác định được)\n\nBurst `capacity` tại t=0 đi qua ngay; thông lượng duy trì không vượt `rate` mỗi giây.",
            [("Burst rồi bị chặn", "Nạp lại = thời gian trôi * rate, trần là capacity; chỉ tiêu token nguyên."),
             ("Thông lượng duy trì giữ vững", "Một token mỗi 0.1s — 100 tick của 0.01s cho đúng 10.")],
        ),
    },
    solutions=[("pa-api-validate-user", VALIDATE_REF, VALIDATE_WRONG),
               ("pa-api-rate-limit", BUCKET_REF, BUCKET_WRONG)],
)

# ── practice 3: api project ──────────────────────────────────────────────────
ROUTER_REF = (
    "class RouterError(Exception):\n"
    "    def __init__(self, status, message):\n"
    "        super().__init__(message)\n"
    "        self.status = status\n"
    "\n"
    "\n"
    "class Router:\n"
    "    def __init__(self):\n"
    "        self._routes = {}\n"
    "\n"
    "    def add(self, method, path, handler):\n"
    "        parts = tuple(path.strip('/').split('/'))\n"
    "        self._routes[(method, parts)] = handler\n"
    "\n"
    "    @staticmethod\n"
    "    def _match(pattern, actual):\n"
    "        if len(pattern) != len(actual):\n"
    "            return None\n"
    "        params = {}\n"
    "        for p, a in zip(pattern, actual):\n"
    "            if p.startswith('{') and p.endswith('}'):\n"
    "                params[p[1:-1]] = a\n"
    "            elif p != a:\n"
    "                return None\n"
    "        return params\n"
    "\n"
    "    def dispatch(self, method, path):\n"
    "        actual = tuple(path.strip('/').split('/'))\n"
    "        handler = self._routes.get((method, actual))\n"
    "        if handler is not None:\n"
    "            return handler({})\n"
    "        for (m, pattern), handler in self._routes.items():\n"
    "            params = self._match(pattern, actual)\n"
    "            if params is not None:\n"
    "                if m == method:\n"
    "                    return handler(params)\n"
    "                raise RouterError(405, 'method not allowed')\n"
    "        raise RouterError(404, 'not found')\n"
)
ROUTER_WRONG = (
    "class RouterError(Exception):\n"
    "    def __init__(self, status, message):\n"
    "        super().__init__(message)\n"
    "        self.status = status\n"
    "\n"
    "\n"
    "class Router:\n"
    "    def __init__(self):\n"
    "        self._routes = {}\n"
    "\n"
    "    def add(self, method, path, handler):\n"
    "        parts = tuple(path.strip('/').split('/'))\n"
    "        self._routes[(method, parts)] = handler\n"
    "\n"
    "    @staticmethod\n"
    "    def _match(pattern, actual):\n"
    "        if len(pattern) != len(actual):\n"
    "            return None\n"
    "        params = {}\n"
    "        for p, a in zip(pattern, actual):\n"
    "            if p.startswith('{') and p.endswith('}'):\n"
    "                params[p[1:-1]] = a\n"
    "            elif p != a:\n"
    "                return None\n"
    "        return params\n"
    "\n"
    "    def dispatch(self, method, path):\n"
    "        actual = tuple(path.strip('/').split('/'))\n"
    "        handler = self._routes.get((method, actual))\n"
    "        if handler is not None:\n"
    "            return handler({})\n"
    "        for (m, pattern), handler in self._routes.items():\n"
    "            params = self._match(pattern, actual)\n"
    "            if params is not None:\n"
    "                return handler(params)  # WRONG: ignores the method — POST rides a GET route\n"
    "        raise RouterError(404, 'not found')\n"
)

IDEM_REF = (
    "class IdempotencyStore:\n"
    "    def __init__(self):\n"
    "        self._done = {}\n"
    "\n"
    "    def execute(self, key, fn):\n"
    "        if key not in self._done:\n"
    "            self._done[key] = fn()\n"
    "        return self._done[key]\n"
)
IDEM_WRONG = (
    "class IdempotencyStore:\n"
    "    def __init__(self):\n"
    "        self._done = {}\n"
    "\n"
    "    def execute(self, key, fn):\n"
    "        self._done[key] = fn()  # WRONG: re-executes on every retry\n"
    "        return self._done[key]\n"
)

write_practice(
    MOD, "pa-p9-api-project",
    "Mini API Project",
    "Assemble the machinery: a router with typed 404/405 errors, and idempotent POST handling with replay.",
    "Dự án mini API",
    "Lắp ráp cơ chế: một router với lỗi 404/405 có kiểu, và POST idempotent với phát lại.",
    "production-concerns", 35, "advanced",
    [
        challenge(
            "pa-api-router",
            "A router that says 404 vs 405 correctly",
            "Implement `Router` with `add(method, path, handler)` and `dispatch(method, path)`:\n\n- paths are `/`-separated segments; a segment like `'{id}'` matches exactly one segment of any value and binds it as a string param\n- `dispatch` returns `handler(params)` where params is a dict (empty for static routes)\n- if some pattern matches the path with a DIFFERENT method → raise `RouterError(405, ...)`\n- if no pattern matches the path at all → raise `RouterError(404, ...)`\n- `RouterError` carries `.status`",
            "class RouterError(Exception):\n    def __init__(self, status, message):\n        super().__init__(message)\n        self.status = status\n\n\nclass Router:\n    def __init__(self):\n        ...\n\n    def add(self, method, path, handler):\n        ...\n\n    def dispatch(self, method, path):\n        ...",
            [
                ("static routes, params, and binding",
                 "r = Router()\nr.add('GET', '/users/{id}', lambda p: f\"user:{p['id']}\")\nr.add('GET', '/health', lambda p: 'ok')\nassert r.dispatch('GET', '/users/42') == 'user:42'\nassert r.dispatch('GET', '/health') == 'ok'\nprint('ok')",
                 "Split into segments; a {param} segment matches anything and binds it."),
                ("405 vs 404 are different diagnoses",
                 "r = Router()\nr.add('GET', '/users/{id}', lambda p: 'x')\ntry:\n    r.dispatch('POST', '/users/42')\nexcept RouterError as e:\n    assert e.status == 405\nelse:\n    raise AssertionError('expected 405')\ntry:\n    r.dispatch('GET', '/nope/zz')\nexcept RouterError as e:\n    assert e.status == 404\nelse:\n    raise AssertionError('expected 404')\nprint('ok')",
                 "Path matched but method didn't → 405. No pattern matched → 404."),
            ],
            level="mini-build",
        ),
        challenge(
            "pa-api-idempotent-post",
            "Retry-safe POST",
            "Implement `IdempotencyStore` with `execute(key, fn)`:\n\n- the first call with a key runs `fn()` and records its return value\n- every later call with the same key replays the recorded value WITHOUT calling `fn` again\n- different keys are independent\n\nThe guarantee under test: `fn` runs exactly once per key, no matter how many retries arrive.",
            "class IdempotencyStore:\n    def __init__(self):\n        ...\n\n    def execute(self, key, fn):\n        ...",
            [
                ("fn runs exactly once per key",
                 "s = IdempotencyStore()\ncalls = []\ndef charge(amount):\n    calls.append(amount)\n    return {'charged': amount}\na = s.execute('k1', lambda: charge(100))\nb = s.execute('k1', lambda: charge(100))\nc = s.execute('k1', lambda: charge(100))\nassert calls == [100], calls\nassert a == b == c == {'charged': 100}\nd = s.execute('k2', lambda: charge(50))\nassert calls == [100, 50]\nprint('ok')",
                 "Compute once, store, replay. Distinct keys don't share."),
            ],
            level="combination",
        ),
    ],
    {
        "pa-api-router": vi_challenge(
            "Router phân biệt đúng 404 và 405",
            "Cài `Router` với `add(method, path, handler)` và `dispatch(method, path)`:\n\n- path được tách bởi `/`; một segment dạng `'{id}'` khớp đúng một segment bất kỳ và ràng buộc nó thành tham số chuỗi\n- `dispatch` trả `handler(params)` với params là dict (rỗng cho route tĩnh)\n- nếu có pattern khớpath với path nhưng method KHÁC → raise `RouterError(405, ...)`\n- nếu không pattern nào khớpath path → raise `RouterError(404, ...)`\n- `RouterError` mang `.status`",
            [("Route tĩnh, tham số, và ràng buộc", "Tách segment; segment {param} khớp mọi giá trị và ràng buộc lại."),
             ("405 khác 404 là hai chẩn đoán khác nhau", "Khớpath path nhưng lệch method → 405. Không pattern nào khớpath → 404.")],
        ),
        "pa-api-idempotent-post": vi_challenge(
            "POST an toàn khi retry",
            "Cài `IdempotencyStore` với `execute(key, fn)`:\n\n- lần đầu với một key thì chạy `fn()` và ghi lại giá trị trả về\n- mọi lần sau với cùng key phát lại giá trị đã ghi KHÔNG gọi `fn` thêm lần nào\n- các key khác nhau độc lập với nhau\n\nBảo đảm bị kiểm tra: `fn` chạy đúng một lần cho mỗi key, dù có bao nhiêu retry đi nữa.",
            [("fn chạy đúng một lần mỗi key", "Tính một lần, lưu lại, phát lại. Key khác nhau không dùng chung.")],
        ),
    },
    solutions=[("pa-api-router", ROUTER_REF, ROUTER_WRONG),
               ("pa-api-idempotent-post", IDEM_REF, IDEM_WRONG)],
)

# ── checkpoint ───────────────────────────────────────────────────────────────
write_checkpoint(
    MOD, "pa-checkpoint-apis",
    "Checkpoint: Production APIs",
    "Prove you can contract-check, validate, and keep serving when dependencies wobble.",
    25,
    """
**Write code that answers these three questions for a real service:**

1. When input is bad, does the client get *every* problem in one envelope-shaped
   answer — with no internals leaked on 5xx?
2. When load spikes, does the limiter throttle by the *injected* clock, not by
   wall-clock luck?
3. When a dependency is down, does readiness say so *without crashing*?

The challenge below combines 2 and 3: a readiness probe whose checks are
injected zero-arg callables. A check that raises is a dependency that is down —
that must mark the service **not ready** (and appear as `false`), never crash
the probe and never count as healthy.
""",
    "Checkpoint: API production",
    "Chứng minh bạn kiểm tra được hợp đồng, validate được đầu vào, và vẫn phục vụ khi dependency lung lay.",
    """
**Viết code trả lời ba câu hỏi này cho một dịch vụ thật:**

1. Khi đầu vào xấu, client có nhận được *mọi* vấn đề trong một câu trả lời
   dạng envelope — không lộ nội bộ trên 5xx không?
2. Khi tải tăng vọt, limiter có chặn theo *đồng hồ được tiêm vào*, chứ không
   theo may rủi của đồng hồ hệ thống không?
3. Khi một dependency chết, readiness có báo vậy *mà không crash* không?

Thử thách dưới đây kết hợp câu 2 và 3: một readiness probe với các check là
callable không-tham-số được tiêm vào. Một check raise nghĩa là dependency đang
chết — điều đó phải đánh dấu dịch vụ **chưa sẵn sàng** (và hiện là `false`),
không bao giờ làm probe crash và không bao giờ bị tính là khỏe mạnh.
""",
    challenge(
        "pa-api-readiness",
        "The readiness probe that survives a dead dependency",
        "Implement `readiness(checks)` where `checks` is a dict mapping dependency names to zero-arg callables:\n\n- returns `{'ready': bool, 'checks': {name: bool}}` with every name included\n- a check that returns a truthy value is healthy; falsy is not\n- a check that RAISES is a dependency that is down: record `False` for it — the probe itself must never propagate the exception\n- `ready` is True iff every check is True\n- an empty `checks` dict is ready",
        "def readiness(checks):\n    ...",
        [
            ("all healthy, some down, one exploding",
             "def ok():\n    return True\ndef down():\n    return False\ndef boom():\n    raise RuntimeError('db socket died')\n\nr = readiness({'db': ok, 'cache': ok})\nassert r == {'ready': True, 'checks': {'db': True, 'cache': True}}\nr2 = readiness({'db': ok, 'cache': down, 'queue': boom})\nassert r2 == {'ready': False, 'checks': {'db': True, 'cache': False, 'queue': False}}\nassert readiness({}) == {'ready': True, 'checks': {}}\nprint('ok')",
             "Catch per check: raising means down, not a crashed probe."),
        ],
        level="build",
    ),
    vi_challenge(
        "Readiness probe sống sót trước dependency chết",
        "Cài `readiness(checks)` với `checks` là dict ánh xạ tên dependency tới callable không tham số:\n\n- trả `{'ready': bool, 'checks': {name: bool}}` gồm đủ mọi tên\n- check trả giá trị truthy là khỏe mạnh; falsy là không\n- check RAISE nghĩa là dependency đang chết: ghi `False` cho nó — bản thân probe không bao giờ làm exception bay ra ngoài\n- `ready` là True khi và chỉ khi mọi check đều True\n- `checks` rỗng là sẵn sàng",
        [("Khỏe mạnh hết, có cái chết, có cái nổ", "Catch theo từng check: raise nghĩa là chết, không phải probe crash.")],
    ),
    solution=(
        "def readiness(checks):\n"
        "    results = {}\n"
        "    for name, check in checks.items():\n"
        "        try:\n"
        "            results[name] = bool(check())\n"
        "        except BaseException:\n"
        "            results[name] = False\n"
        "    return {'ready': all(results.values()), 'checks': results}\n"
    ),
    wrong=(
        "def readiness(checks):\n"
        "    results = {}\n"
        "    for name, check in checks.items():\n"
        "        results[name] = bool(check())  # WRONG: a raising check crashes the probe\n"
        "    return {'ready': all(results.values()), 'checks': results}\n"
    ),
)

print("module 9 complete")
