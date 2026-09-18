#!/usr/bin/env python3
"""Module 10: backend-fundamentals — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint

MOD = "backend-fundamentals"

write_module(
    MOD,
    "Backend Fundamentals with Node.js",
    "The other side of the request: HTTP servers, routing, middleware, REST design, and validation — the machinery behind every API you have consumed.",
    "Nền tảng Backend với Node.js",
    "Bên kia của request: HTTP server, routing, middleware, thiết kế REST, và validation — bộ máy đằng sau mọi API bạn từng tiêu thụ.",
    ["http-server-node", "routing-rest", "middleware-pipeline", "validation-errors", "backend-checkpoint"],
    ["server-practice", "rest-practice", "middleware-practice", "crud-practice"],
)

write_lesson(
    MOD, "http-server-node",
    "An HTTP Server From Scratch",
    "Node's http module in 15 lines, the request/response lifecycle, and what a framework does for you.",
    20,
    """You've called APIs for months. Now build the receiving end — with zero frameworks, so you know what they actually do.

## The minimal server

```js
import http from "node:http";

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ ok: true }));
});

server.listen(3000, () => console.log("on :3000"));
```

`createServer` registers a callback that runs for **every request**. The two arguments are everything:

- **req** (IncomingMessage): `req.method` ("GET", "POST"...), `req.url` (path + query), `req.headers`, and the body as a stream (POST bodies arrive in chunks — you assemble them).
- **res** (ServerResponse): `res.writeHead(status, headers)`, `res.end(body)`. Forget `res.end` and the client hangs forever.

## Reading a request body

```js
let body = "";
req.on("data", (chunk) => { body += chunk; });
req.on("end", () => {
  const data = JSON.parse(body);  // wrap in try/catch: bad JSON is user input
  res.end(JSON.stringify({ got: data }));
});
```

This is the stream dance every framework hides behind `req.json()`.

## Status codes that mean something

- **200** OK — success with body · **201** Created — after a successful POST that made something (set `Location` header to the new resource)
- **400** Bad Request — the client sent garbage (validation failure)
- **401** Unauthorized — who are you? · **403** Forbidden — I know you; no.
- **404** Not Found · **409** Conflict (duplicate email) · **500** — our fault, log it

Correct codes are part of your API's contract. A `404` for "validation failed" makes clients build error handling on lies.

## What frameworks buy you

Routing by pattern (`app.get("/users/:id")`), body parsing, middleware chaining, error normalization. Express/Fastify are conveniences over this callback — knowing the callback means you can debug through any framework.""",
    "HTTP server từ con số 0",
    "Module http của Node trong 15 dòng, vòng đời request/response, và framework thực sự làm gì cho bạn.",
    """Bạn đã gọi API hàng tháng trời. Giờ hãy dựng phía nhận — không dùng framework nào, để biết chúng thực sự làm gì.

## Server tối thiểu

```js
import http from "node:http";

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ ok: true }));
});

server.listen(3000, () => console.log("on :3000"));
```

`createServer` đăng ký một callback chạy cho **mọi request**. Hai tham số là tất cả:

- **req** (IncomingMessage): `req.method` ("GET", "POST"...), `req.url` (path + query), `req.headers`, và body dưới dạng stream (body POST đến thành từng khối — bạn phải ghép lại).
- **res** (ServerResponse): `res.writeHead(status, headers)`, `res.end(body)`. Quên `res.end` là client treo vĩnh viễn.

## Đọc request body

```js
let body = "";
req.on("data", (chunk) => { body += chunk; });
req.on("end", () => {
  const data = JSON.parse(body);  // bọc try/catch: JSON xấu cũng là user input
  res.end(JSON.stringify({ got: data }));
});
```

Đây là điệu dance stream mà mọi framework giấu sau `req.json()`.

## Mã trạng thái phải có ý nghĩa

- **200** OK — thành công kèm body · **201** Created — sau POST tạo thành công thứ gì đó (set header `Location` trỏ tới tài nguyên mới)
- **400** Bad Request — client gửi rác (validation thất bại)
- **401** Unauthorized — bạn là ai? · **403** Forbidden — tôi biết bạn; không.
- **404** Not Found · **409** Conflict (email trùng) · **500** — lỗi của chúng ta, log lại

Mã trạng thái đúng là một phần của hợp đồng API. Trả `404` cho "validation thất bại" khiến client xây error handling trên lời nói dối.

## Framework mua cho bạn điều gì

Routing theo mẫu (`app.get("/users/:id")`), parse body, chuỗi middleware, chuẩn hóa lỗi. Express/Fastify chỉ là tiện ích trên callback này — hiểu callback nghĩa là debug được qua bất kỳ framework nào.""",
)

write_lesson(
    MOD, "routing-rest",
    "Routing and REST Design",
    "URLs name things; methods say what happens. A resource-oriented API that clients can predict.",
    20,
    """## Resources, not verbs

REST models your API as **nouns with methods**:

```text
GET    /api/tasks          list (supports ?status=open&limit=20)
POST   /api/tasks          create — 201 + Location: /api/tasks/42
GET    /api/tasks/42       read one — 404 if absent
PUT    /api/tasks/42       replace — full object
PATCH  /api/tasks/42       partial update
DELETE /api/tasks/42       remove — 200 or 204
```

Compare with the anti-pattern: `/api/getTasks`, `/api/deleteTask?id=42`. Verbs-in-URLs duplicate what the method already says and grow unboundedly. Exceptions exist (auth: `POST /api/login` is fine — login is a process, not a resource).

## Path parameters and queries

- **Path** identifies the resource: `/api/tasks/42`.
- **Query** shapes the response without changing identity: `?status=open&sort=due&limit=20`.

Conventions clients will assume: `limit`/`offset` (or `cursor`) for pagination, `sort=-createdAt` (minus = descending), filtering by field names.

## Design review checklist

- Plural nouns (`/tasks` not `/task`)
- No verbs in paths (methods carry the action)
- Status codes truthful (201 on create, 404 on missing, 400 on invalid body)
- Consistent error shape: `{ "error": { "message": "...", "field": "due" } }` — clients parse one shape
- Versioning strategy when you must break the contract: `/api/v2/...` (avoid until forced)

## A tiny router, by hand

```js
const routes = [];
function route(method, pattern, handler) {
  // "/tasks/:id" -> regex with a named group
  const keys = [];
  const rx = new RegExp("^" + pattern.replace(/:(\w+)/g, (_, k) => {
    keys.push(k);
    return "([^/]+)";
  }) + "$");
  routes.push({ method, rx, keys, handler });
}

function match(method, url) {
  for (const r of routes) {
    const m = r.rx.exec(url);
    if (r.method === method && m) {
      const params = Object.fromEntries(r.keys.map((k, i) => [k, decodeURIComponent(m[i + 1])]));
      return { handler: r.handler, params };
    }
  }
  return null;
}
```

Thirty lines and routing is demystified: patterns become regexes, matches become parameter objects. (Framework routers do exactly this plus optimizations.)""",
    "Routing và thiết kế REST",
    "URL đặt tên cho sự vật; method nói rõ điều gì xảy ra. Một API hướng tài nguyên mà client đoán được.",
    """## Tài nguyên, không phải động từ

REST mô hình hóa API của bạn thành **danh từ kèm method**:

```text
GET    /api/tasks          liệt kê (hỗ trợ ?status=open&limit=20)
POST   /api/tasks          tạo — 201 + Location: /api/tasks/42
GET    /api/tasks/42       đọc một — 404 nếu không có
PUT    /api/tasks/42       thay thế — object đầy đủ
PATCH  /api/tasks/42       cập nhật một phần
DELETE /api/tasks/42       xóa — 200 hoặc 204
```

So với anti-pattern: `/api/getTasks`, `/api/deleteTask?id=42`. Động từ trong URL trùng lặp với điều method đã nói và lớn lên không giới hạn. Ngoại lệ tồn tại (auth: `POST /api/login` là ổn — login là một tiến trình, không phải tài nguyên).

## Path parameter và query

- **Path** định danh tài nguyên: `/api/tasks/42`.
- **Query** định hình response mà không đổi định danh: `?status=open&sort=due&limit=20`.

Các quy ước client sẽ mặc định: `limit`/`offset` (hoặc `cursor`) cho phân trang, `sort=-createdAt` (trừ = giảm dần), lọc theo tên trường.

## Checklist review thiết kế

- Danh từ số nhiều (`/tasks` không phải `/task`)
- Không động từ trong path (method mang hành động)
- Mã trạng thái trung thực (201 khi tạo, 404 khi thiếu, 400 khi body sai)
- Hình dạng lỗi nhất quán: `{ "error": { "message": "...", "field": "due" } }` — client chỉ parse một hình dạng
- Chiến lược phiên bản khi buộc phải phá hợp đồng: `/api/v2/...` (né đến khi bị ép)

## Router tí hon, làm tay

```js
const routes = [];
function route(method, pattern, handler) {
  // "/tasks/:id" -> regex với named group
  const keys = [];
  const rx = new RegExp("^" + pattern.replace(/:(\\w+)/g, (_, k) => {
    keys.push(k);
    return "([^/]+)";
  }) + "$");
  routes.push({ method, rx, keys, handler });
}

function match(method, url) {
  for (const r of routes) {
    const m = r.rx.exec(url);
    if (r.method === method && m) {
      const params = Object.fromEntries(r.keys.map((k, i) => [k, decodeURIComponent(m[i + 1])]));
      return { handler: r.handler, params };
    }
  }
  return null;
}
```

Ba mươi dòng và routing không còn huyền bí: pattern hóa thành regex, khớp thành parameter object. (Router của framework làm đúng như vậy cộng thêm tối ưu hóa.)""",
)

write_lesson(
    MOD, "middleware-pipeline",
    "Middleware: The Onion",
    "Cross-cutting concerns — logging, auth, parsing — as composable layers around every handler.",
    18,
    """Every route needs some of the same work: parse the body, check auth, log timing, catch errors. Middleware is the pattern that factors it out: each layer wraps the next.

## The shape

```js
function logger(req, res, next) {
  const start = Date.now();
  res.on("finish", () => console.log(req.method, req.url, Date.now() - start + "ms"));
  next();
}
```

A middleware receives (req, res, next). It can act **before** `next()` (setup), **after** (response finished), or never call `next()` (it *is* the response — auth denial). Nesting them forms an onion: request enters layer 1, 2, 3, handler, then unwinds back out.

## The pipeline by hand

```js
function pipeline(middlewares, handler) {
  return (req, res) => {
    let i = 0;
    const next = (err) => {
      if (err) return onError(res, err);
      const mw = middlewares[i++];
      if (mw) mw(req, res, next);
      else handler(req, res);
    };
    next();
  };
}
```

`next` is the trick: it's a closure over position `i`, so each call advances exactly one layer. Express's `app.use()` builds precisely this list.

## Middlewares worth writing

- **Request logging** (above) — you'll write this in every job
- **Body parser** — assemble chunks, parse JSON, attach `req.body`, 400 on garbage
- **Auth guard** — verify session/token, attach `req.user`, 401 early
- **Error boundary** — the outermost layer's try/catch: one 500 shape for the whole app, logged once
- **Rate limiter** — keyed by IP/user, before the handler touches the DB

## Ordering is semantics

`auth` before `handler` (obviously), but also before anything that touches `req.user`. `bodyParser` before anything reading `req.body`. Errors thrown inside deep layers must reach the outermost catch — that's why the pipeline passes `err` through `next(err)` instead of letting each layer catch (and swallow) its own.""",
    "Middleware: Củ hành",
    "Các mối quan tâm xuyên suốt — logging, auth, parsing — thành những lớp ghép được quanh mọi handler.",
    """Mọi route đều cần một số công việc giống nhau: parse body, kiểm tra auth, log thời gian, bắt lỗi. Middleware là mô hình tách phần đó ra: mỗi lớp bọc lớp kế tiếp.

## Hình dạng

```js
function logger(req, res, next) {
  const start = Date.now();
  res.on("finish", () => console.log(req.method, req.url, Date.now() - start + "ms"));
  next();
}
```

Một middleware nhận (req, res, next). Nó có thể hành động **trước** `next()` (chuẩn bị), **sau** (response đã xong), hoặc không bao giờ gọi `next()` (nó *chính là* response — auth từ chối). Lồng chúng tạo thành củ hành: request vào lớp 1, 2, 3, handler, rồi đi ngược ra.

## Pipeline làm tay

```js
function pipeline(middlewares, handler) {
  return (req, res) => {
    let i = 0;
    const next = (err) => {
      if (err) return onError(res, err);
      const mw = middlewares[i++];
      if (mw) mw(req, res, next);
      else handler(req, res);
    };
    next();
  };
}
```

`next` là mẹo: nó là một closure trên vị trí `i`, nên mỗi lần gọi tiến đúng một lớp. `app.use()` của Express dựng chính xác danh sách này.

## Những middleware đáng viết

- **Request logging** (như trên) — bạn sẽ viết nó ở mọi công việc
- **Body parser** — ghép các khối, parse JSON, gắn `req.body`, 400 với rác
- **Auth guard** — xác minh session/token, gắn `req.user`, 401 sớm
- **Error boundary** — try/catch của lớp ngoài cùng: một hình dạng 500 cho cả app, log một nơi
- **Rate limiter** — khóa theo IP/user, trước khi handler đụng vào DB

## Thứ tự chính là ngữ nghĩa

`auth` trước `handler` (tất nhiên), nhưng cũng trước bất cứ thứ gì đụng `req.user`. `bodyParser` trước bất cứ thứ gì đọc `req.body`. Lỗi ném ở lớp sâu phải với tới được catch ngoài cùng — đó là lý do pipeline truyền `err` qua `next(err)` thay vì để mỗi lớp tự catch (và nuốt) lỗi của mình.""",
)

write_lesson(
    MOD, "validation-errors",
    "Validation and Error Handling",
    "Treat every request as hostile: validate shape at the door, fail with honest codes, and never leak internals.",
    18,
    """The API's front door decides whether the rest of the code can be simple. Validate everything there.

## Validate at the boundary

```js
function validateTask(body) {
  const errors = [];
  if (typeof body.title !== "string" || body.title.trim() === "" || body.title.length > 200) {
    errors.push({ field: "title", message: "title must be a 1-200 char string" });
  }
  if (body.due !== undefined && !Number.isInteger(Date.parse(body.due))) {
    errors.push({ field: "due", message: "due must be an ISO date" });
  }
  return errors;
}
```

Collect **all** errors, not the first — clients render one form pass, not seven round trips. In production you'd use Zod: schema in, typed data or structured issues out.

## Error responses: honest and uniform

```text
400  { "error": { "message": "validation failed", "details": [...] } }
401  { "error": { "message": "authentication required" } }
404  { "error": { "message": "task not found" } }
500  { "error": { "message": "internal error" } }     <- nothing internal shown
```

Two rules:

1. **Same shape for every error** — clients write one parser.
2. **500 never leaks internals.** No stack traces, no SQL, no file paths in responses. Log the detail server-side (with a request id!), return the generic message. Stack traces in responses are an information-disclosure bug.

## Throwing and catching in a pipeline

Handlers shouldn't each try/catch into their own JSON shape. They throw domain errors; one outer middleware maps them:

```js
class HttpError extends Error {
  constructor(status, message, details) { super(message); this.status = status; this.details = details; }
}
// handler:
throw new HttpError(404, "task not found");
// error middleware:
res.writeHead(err.status ?? 500, { "Content-Type": "application/json" });
res.end(JSON.stringify({ error: { message: err.expose ? err.message : "internal error", details: err.details } }));
```

The `expose` flag is the security boundary: 4xx messages are for users, 5xx messages are for logs.

## Async errors don't throw — they reject

In a callback-based or promise-based handler, a rejected promise doesn't reach your catch automatically. Frameworks differ; the mental model to keep: **every async path must have an owner** — await it inside the try, or attach a `.catch`, or let the pipeline's error channel carry it. An unowned rejection in Node used to crash the process; modern versions warn, but your users still see a 500 — or nothing.""",
    "Validation và xử lý lỗi",
    "Coi mọi request là thù địch: kiểm tra hình dạng ngay cửa, fail bằng mã trung thực, và không bao giờ lộ nội bộ.",
    """Cửa trước của API quyết định phần code còn lại có thể đơn giản đến đâu. Hãy kiểm tra mọi thứ ở đó.

## Kiểm tra ở ranh giới

```js
function validateTask(body) {
  const errors = [];
  if (typeof body.title !== "string" || body.title.trim() === "" || body.title.length > 200) {
    errors.push({ field: "title", message: "title must be a 1-200 char string" });
  }
  if (body.due !== undefined && !Number.isInteger(Date.parse(body.due))) {
    errors.push({ field: "due", message: "due must be an ISO date" });
  }
  return errors;
}
```

Thu thập **tất cả** lỗi, không chỉ lỗi đầu — client render một lượt form, không phải bảy chuyến khứ hồi. Trong production bạn sẽ dùng Zod: schema vào, dữ liệu có kiểu hoặc danh sách lỗi có cấu trúc ra.

## Error response: trung thực và nhất quán

```text
400  { "error": { "message": "validation failed", "details": [...] } }
401  { "error": { "message": "authentication required" } }
404  { "error": { "message": "task not found" } }
500  { "error": { "message": "internal error" } }     <- không lộ gì nội bộ
```

Hai quy tắc:

1. **Cùng hình dạng cho mọi lỗi** — client chỉ viết một bộ parse.
2. **500 không bao giờ lộ nội bộ.** Không stack trace, không SQL, không đường dẫn file trong response. Log chi tiết phía server (kèm request id!), trả message chung chung. Stack trace trong response là một bug tiết lộ thông tin.

## Throw và catch trong pipeline

Handler không nên tự try/catch thành hình dạng JSON riêng của mình. Chúng ném domain error; một middleware ngoài cùng ánh xạ chúng:

```js
class HttpError extends Error {
  constructor(status, message, details) { super(message); this.status = status; this.details = details; }
}
// handler:
throw new HttpError(404, "task not found");
// error middleware:
res.writeHead(err.status ?? 500, { "Content-Type": "application/json" });
res.end(JSON.stringify({ error: { message: err.expose ? err.message : "internal error", details: err.details } }));
```

Cờ `expose` là ranh giới bảo mật: message 4xx dành cho người dùng, message 5xx dành cho log.

## Lỗi bất đồng bộ không throw — chúng reject

Với handler kiểu callback hay promise, một promise bị reject không tự đến được catch của bạn. Framework mỗi loại một kiểu; mô hình tinh thần cần giữ: **mọi đường bất đồng bộ phải có chủ** — await bên trong try, hoặc gắn `.catch`, hoặc để kênh lỗi của pipeline mang đi. Một rejection không có chủ trong Node từng làm crash tiến trình; các bản mới chỉ cảnh báo, nhưng người dùng của bạn vẫn thấy 500 — hoặc không thấy gì.""",
)

write_checkpoint(
    MOD,
    "backend-checkpoint",
    "Checkpoint: API Mechanic",
    "Assemble the backend skill set: route matching, middleware ordering, validation, and truthful status codes.",
    20,
    """This checkpoint rebuilds the backend's moving parts in runnable form: the router you wrote by hand, the pipeline, and the validation posture — graded as pure logic, the same reasoning Express automates.""",
    "Kiểm tra kiến thức: Thợ máy API",
    "Lắp ráp kỹ năng backend: khớp route, thứ tự middleware, validation, và mã trạng thái trung thực.",
    """Checkpoint này dựng lại các bộ phận chuyển động của backend ở dạng chạy được: router bạn viết tay, pipeline, và tư thế validation — chấm dưới dạng logic thuần, cùng lập luận mà Express tự động hóa.""",
    {
        "id": "i2-backend-checkpoint",
        "title": "Router Room",
        "prompt": "Write THREE functions. 1) `matchRoute(pattern, method, path, method2)` — pattern like \"/tasks/:id\"; return the params object when the method matches AND the path fits the pattern (segments align, :id captures one non-empty segment), else null. 2) `orderMiddleware(names)` — given a scrambled list containing \"bodyParser\", \"auth\", \"logger\", \"errorBoundary\", return the correct order: logger, bodyParser, auth, errorBoundary (errorBoundary wraps everything, so last). 3) `statusFor(situation)` — map: \"created\" => 201, \"validation-failed\" => 400, \"not-logged-in\" => 401, \"not-allowed\" => 403, \"missing\" => 404, \"duplicate\" => 409, \"crashed\" => 500.",
        "difficulty": "intermediate",
        "level": "checkpoint",
        "boilerplate": "function matchRoute(pattern, method, path, method2) {\n  // your code\n}\n\nfunction orderMiddleware(names) {\n  // your code\n}\n\nfunction statusFor(situation) {\n  // your code\n}\n",
        "tests": [
            {
                "name": "pattern matching extracts params",
                "code": "const fn = new Function(code + \"\\nreturn { matchRoute, orderMiddleware, statusFor };\");\nconst { matchRoute } = fn();\nconst p = matchRoute(\"/tasks/:id\", \"GET\", \"/tasks/42\", \"GET\");\nif (!p || p.id !== \"42\") throw new Error(\":id captured from the path.\");\nif (matchRoute(\"/tasks/:id\", \"GET\", \"/tasks/42\", \"POST\") !== null) throw new Error(\"Method mismatch => null.\");\nif (matchRoute(\"/tasks/:id\", \"GET\", \"/tasks\", \"GET\") !== null) throw new Error(\"Segment count mismatch => null.\");\nif (matchRoute(\"/tasks\", \"GET\", \"/tasks/42\", \"GET\") !== null) throw new Error(\"Extra segments => null.\");",
                "hint": "Split both into segments; lengths must match; :x captures.",
            },
            {
                "name": "middleware order is semantics",
                "code": "const fn = new Function(code + \"\\nreturn { matchRoute, orderMiddleware, statusFor };\");\nconst { orderMiddleware } = fn();\nconst out = orderMiddleware([\"auth\", \"logger\", \"bodyParser\", \"errorBoundary\"]);\nif (out.join(\",\") !== \"logger,bodyParser,auth,errorBoundary\") throw new Error(\"Log first, parse before auth reads body, boundary last.\");",
                "hint": "logger outermost, then parse, then auth, then the error wrapper.",
            },
            {
                "name": "status codes tell the truth",
                "code": "const fn = new Function(code + \"\\nreturn { matchRoute, orderMiddleware, statusFor };\");\nconst { statusFor } = fn();\nif (statusFor(\"created\") !== 201) throw new Error(\"Create => 201.\");\nif (statusFor(\"validation-failed\") !== 400) throw new Error(\"Bad input => 400, not 404.\");\nif (statusFor(\"not-logged-in\") !== 401) throw new Error(\"Who are you => 401.\");\nif (statusFor(\"not-allowed\") !== 403) throw new Error(\"No permission => 403.\");\nif (statusFor(\"duplicate\") !== 409) throw new Error(\"Conflict => 409.\");",
                "hint": "A lookup object — but think about each pair as you write it.",
            },
        ],
    },
    {
        "id": "i2-backend-checkpoint",
        "title": "Phòng máy router",
        "prompt": "Viết BA hàm. 1) `matchRoute(pattern, method, path, method2)` — pattern kiểu \"/tasks/:id\"; trả về object params khi method khớp VÀ path vừa với pattern (các segment thẳng hàng, :id bắt một segment khác rỗng), ngược lại null. 2) `orderMiddleware(names)` — cho một danh sách xáo trộn chứa \"bodyParser\", \"auth\", \"logger\", \"errorBoundary\", trả về thứ tự đúng: logger, bodyParser, auth, errorBoundary (errorBoundary bọc tất cả, nên đứng cuối). 3) `statusFor(situation)` — ánh xạ: \"created\" => 201, \"validation-failed\" => 400, \"not-logged-in\" => 401, \"not-allowed\" => 403, \"missing\" => 404, \"duplicate\" => 409, \"crashed\" => 500.",
        "tests": [
            {"name": "khớp pattern trích xuất params", "hint": "Tách cả hai thành segment; độ dài phải khớp; :x bắt giá trị."},
            {"name": "thứ tự middleware chính là ngữ nghĩa", "hint": "logger ngoài cùng, rồi parse, rồi auth, rồi bộ bọc lỗi."},
            {"name": "mã trạng thái nói thật", "hint": "Một lookup object — nhưng hãy nghĩ về từng cặp khi viết."},
        ],
    },
)

print("Module 10 lessons + checkpoint written.")
