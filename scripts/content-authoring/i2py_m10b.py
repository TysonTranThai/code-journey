#!/usr/bin/env python3
"""Module 10 practices: server, rest, middleware, crud. Raw strings throughout."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "backend-fundamentals"

# ── server-practice ─────────────────────────────────────────────────────────
write_practice(
    MOD, "server-practice",
    "HTTP Mechanics — Practice",
    "Simulate the request/response pair: parse URLs, assemble streamed bodies, and classify status codes.",
    "Cơ chế HTTP — Luyện tập",
    "Mô phỏng cặp request/response: parse URL, ghép body dạng stream, và phân loại mã trạng thái.",
    "http-server-node", 18, "intermediate",
    [
        {
            "id": "i2-url-parse",
            "title": "Request URL Parser",
            "prompt": 'Write `parseRequest(url)` — url is like "/api/tasks/42?status=open&limit=10". Return { path: "/api/tasks/42", params: { id: "42" } } for ID-bearing paths, else { path, params: {} }; plus `query` — an object of decoded query string keys/values (missing query => {}).',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function parseRequest(url) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "splits path and query",
                    "code": fn_wrap("parseRequest", "parseRequest") + r'''
const r = parseRequest("/api/tasks/42?status=open&limit=10");
if (r.path !== "/api/tasks/42") throw new Error("Path isolated.");
if (r.query.status !== "open" || r.query.limit !== "10") throw new Error("Query decoded into object.");
if (r.params.id !== "42") throw new Error("Numeric id captured as params.id.");
''',
                    "hint": "Split on ?, then on & and =; decodeURIComponent each piece.",
                },
                {
                    "name": "clean handles",
                    "code": fn_wrap("parseRequest", "parseRequest") + r'''
const r = parseRequest("/api/tasks");
if (r.query && Object.keys(r.query).length !== 0) throw new Error("No query => empty object.");
if (r.path !== "/api/tasks") throw new Error("Path unchanged.");
if (parseRequest("/api/tasks?flag").query.flag === "") throw new Error("Valueless key => empty string.");
''',
                    "hint": "A key without '=' yields an empty-string value.",
                },
            ],
        },
        {
            "id": "i2-body-stream",
            "title": "Streamed Body Assembler",
            "prompt": "Write `assembleBody(chunks)` — chunks is an array of Buffer-like strings arriving in order; concatenate and parse as JSON. Return { ok: true, data } on valid JSON, { ok: false, error: \"invalid-json\" } on unparseable input (empty array counts as invalid). Wrap JSON.parse — never let a 400 become a 500.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function assembleBody(chunks) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "concatenates and parses",
                    "code": fn_wrap("assembleBody", "assembleBody") + r'''
const out = assembleBody(['{"title":', '"Write tests"}']);
if (!out.ok || out.data.title !== "Write tests") throw new Error("Two chunks assemble into one object.");
''',
                    "hint": "join then JSON.parse inside try/catch.",
                },
                {
                    "name": "bad JSON fails safely",
                    "code": fn_wrap("assembleBody", "assembleBody") + r'''
if (assembleBody(["{broken"]).ok !== false) throw new Error("Garbage => ok false.");
if (assembleBody([]).ok !== false) throw new Error("Empty body => not ok.");
if (assembleBody(["{broken"]).error !== "invalid-json") throw new Error("The error is named.");
''',
                    "hint": "Catch is the success path here — it's how you return 400.",
                },
            ],
        },
        {
            "id": "i2-status-classify",
            "title": "Status Code Selector",
            "prompt": 'Write `respond(handler)` — handler is one of "create-ok", "create-duplicate", "get-ok", "get-missing", "update-invalid", "delete-ok", "boom". Return { status, body } where: create-ok => 201 + { ok: true }; create-duplicate => 409 + { error: "duplicate" }; get-ok => 200 + { ok: true }; get-missing => 404 + { error: "not-found" }; update-invalid => 400 + { error: "validation" }; delete-ok => 204 + null body; boom => 500 + { error: "internal" }.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function respond(handler) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "maps situations to truthful codes",
                    "code": fn_wrap("respond", "respond") + r'''
if (respond("create-ok").status !== 201) throw new Error("Created => 201.");
if (respond("create-duplicate").status !== 409) throw new Error("Conflict => 409.");
if (respond("get-missing").status !== 404) throw new Error("Missing => 404.");
if (respond("update-invalid").status !== 400) throw new Error("Validation => 400.");
''',
                    "hint": "A lookup table of { status, body }.",
                },
                {
                    "name": "204 has no body",
                    "code": fn_wrap("respond", "respond") + r'''
const r = respond("delete-ok");
if (r.status !== 204) throw new Error("Delete => 204.");
if (r.body !== null) throw new Error("204 means no content.");
''',
                    "hint": "204 No Content — the name says it.",
                },
            ],
        },
    ],
    {
        "i2-url-parse": {
            "title": "Bộ parse URL request",
            "prompt": 'Viết `parseRequest(url)` — url kiểu "/api/tasks/42?status=open&limit=10". Trả về { path: "/api/tasks/42", params: { id: "42" } } với path chứa ID, ngược lại { path, params: {} }; cộng thêm `query` — object các key/value đã decode của query string (không có query => {}).',
            "tests": [
                {"name": "tách path và query", "hint": "Tách theo ?, rồi theo & và =; decodeURIComponent từng mảnh."},
                {"name": "xử lý gọn gàng", "hint": "Key không có '=' cho value là chuỗi rỗng."},
            ],
        },
        "i2-body-stream": {
            "title": "Bộ ghép body dạng stream",
            "prompt": 'Viết `assembleBody(chunks)` — chunks là mảng chuỗi Buffer-like đến theo thứ tự; nối lại và parse JSON. Trả về { ok: true, data } với JSON hợp lệ, { ok: false, error: "invalid-json" } với input không parse được (mảng rỗng cũng tính là invalid). Bọc JSON.parse — đừng bao giờ để 400 biến thành 500.',
            "tests": [
                {"name": "nối và parse", "hint": "join rồi JSON.parse bên trong try/catch."},
                {"name": "JSON xấu fail an toàn", "hint": "Catch ở đây là đường thành công — đó là cách bạn trả 400."},
            ],
        },
        "i2-status-classify": {
            "title": "Bộ chọn mã trạng thái",
            "prompt": 'Viết `respond(handler)` — handler là một trong "create-ok", "create-duplicate", "get-ok", "get-missing", "update-invalid", "delete-ok", "boom". Trả về { status, body } với: create-ok => 201 + { ok: true }; create-duplicate => 409 + { error: "duplicate" }; get-ok => 200 + { ok: true }; get-missing => 404 + { error: "not-found" }; update-invalid => 400 + { error: "validation" }; delete-ok => 204 + body null; boom => 500 + { error: "internal" }.',
            "tests": [
                {"name": "ánh xạ tình huống sang mã trung thực", "hint": "Một bảng tra cứu gồm { status, body }."},
                {"name": "204 không có body", "hint": "204 No Content — tên đã nói tất cả."},
            ],
        },
    },
    [
        ["i2-url-parse", r'''function parseRequest(url) {
  const [path, qs] = url.split("?");
  const query = {};
  if (qs) {
    for (const pair of qs.split("&")) {
      const [k, v = ""] = pair.split("=");
      query[decodeURIComponent(k)] = decodeURIComponent(v);
    }
  }
  const segs = path.split("/").filter(Boolean);
  const params = {};
  if (segs.length >= 2 && /^\d+$/.test(segs[segs.length - 1])) {
    params.id = segs[segs.length - 1];
  }
  return { path, params, query };
}''', r'''function parseRequest(url) {
  return { path: url, params: {}, query: {} };
}'''],
        ["i2-body-stream", r'''function assembleBody(chunks) {
  if (chunks.length === 0) return { ok: false, error: "invalid-json" };
  try {
    return { ok: true, data: JSON.parse(chunks.join("")) };
  } catch {
    return { ok: false, error: "invalid-json" };
  }
}''', r'''function assembleBody(chunks) {
  return { ok: true, data: JSON.parse(chunks.join("")) };
}'''],
        ["i2-status-classify", r'''function respond(handler) {
  const table = {
    "create-ok": { status: 201, body: { ok: true } },
    "create-duplicate": { status: 409, body: { error: "duplicate" } },
    "get-ok": { status: 200, body: { ok: true } },
    "get-missing": { status: 404, body: { error: "not-found" } },
    "update-invalid": { status: 400, body: { error: "validation" } },
    "delete-ok": { status: 204, body: null },
    "boom": { status: 500, body: { error: "internal" } },
  };
  return table[handler];
}''', r'''function respond(handler) {
  return { status: 200, body: { ok: true } };
}'''],
    ],
)

# ── rest-practice ───────────────────────────────────────────────────────────
write_practice(
    MOD, "rest-practice",
    "REST Resource Design — Practice",
    "Judge API designs in code: name resources, score RESTfulness, and paginate a collection deterministically.",
    "Thiết kế tài nguyên REST — Luyện tập",
    "Đánh giá thiết kế API bằng code: đặt tên tài nguyên, chấm độ RESTful, và phân trang một collection một cách tất định.",
    "routing-rest", 18, "intermediate",
    [
        {
            "id": "i2-route-review",
            "title": "Route Reviewer",
            "prompt": 'Write `reviewRoute(method, path)` scoring RESTfulness: return "good" for resource-style routes (path has no verb words like get/list/create/delete/update/fetch/save, case-insensitive); "verb" when a verb word appears in the path; "missing-id" when the method is PUT/PATCH/DELETE but the path has no id segment (last segment not a parameter). Order of checks: verb first, then id presence.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function reviewRoute(method, path) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "clean resource routes pass",
                    "code": fn_wrap("reviewRoute", "reviewRoute") + r'''
if (reviewRoute("GET", "/api/tasks") !== "good") throw new Error("List route.");
if (reviewRoute("PUT", "/api/tasks/42") !== "good") throw new Error("Replace route with id.");
if (reviewRoute("DELETE", "/api/tasks/42") !== "good") throw new Error("Delete route with id.");
''',
                    "hint": "Check the path against the verb list, then id presence for mutating methods.",
                },
                {
                    "name": "verbs and missing ids flagged",
                    "code": fn_wrap("reviewRoute", "reviewRoute") + r'''
if (reviewRoute("POST", "/api/createTask") !== "verb") throw new Error("Verb in path.");
if (reviewRoute("DELETE", "/api/tasks") !== "missing-id") throw new Error("Delete needs an id.");
if (reviewRoute("PATCH", "/api/tasks") !== "missing-id") throw new Error("Patch needs an id.");
''',
                    "hint": "The last path segment must exist for PUT/PATCH/DELETE.",
                },
            ],
        },
        {
            "id": "i2-pagination",
            "title": "Offset Pagination",
            "prompt": "Write `paginate(items, query)` — query is { limit?, offset? } (limit defaults 10, max 100; offset defaults 0). Return { results, total, next }: results is the sliced page; total is items.length; next is the next offset (as a number) when more items remain, else null. Guard against negative and non-integer inputs.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function paginate(items, query) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "slices and computes next",
                    "code": fn_wrap("paginate", "paginate") + r'''
const items = Array.from({ length: 25 }, (_, i) => i);
const p1 = paginate(items, { limit: 10 });
if (p1.results.length !== 10 || p1.total !== 25) throw new Error("First page of 10, total 25.");
if (p1.next !== 10) throw new Error("Next offset is 10.");
const p2 = paginate(items, { limit: 10, offset: 20 });
if (p2.results.length !== 5) throw new Error("Partial last page.");
if (p2.next !== null) throw new Error("No more pages => null.");
''',
                    "hint": "offset + limit < total => there's a next.",
                },
                {
                    "name": "defaults and guards",
                    "code": fn_wrap("paginate", "paginate") + r'''
const items = Array.from({ length: 7 }, (_, i) => i);
const p = paginate(items, {});
if (p.results.length !== 7) throw new Error("Default limit 10 returns everything here.");
if (paginate(items, { limit: 1000 }).results.length !== 7) throw new Error("Max limit clamps to 100 — 7 items unaffected.");
if (paginate(items, { offset: -5 }).results[0] !== 0) throw new Error("Negative offset clamps to 0.");
''',
                    "hint": "Clamp: limit <= 100, offset >= 0, both integers.",
                },
            ],
        },
        {
            "id": "i2-error-shape",
            "title": "Uniform Error Shaper",
            "prompt": 'Write `apiError(status, message, field?)` returning { status, body } where body is { error: { message, field? } } — field only included when provided. Write `fromZod(issues)` mapping an array of { path, message } into the details array shape [{ field, message }] (path is a string like "dueDate").',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function apiError(status, message, field) {\n  // your code\n}\n\nfunction fromZod(issues) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "single error with optional field",
                    "code": fn_wrap("apiError, fromZod", "apiError, fromZod") + r'''
const e = apiError(400, "validation failed", "title");
if (e.status !== 400 || e.body.error.field !== "title") throw new Error("Field included when given.");
const e2 = apiError(404, "task not found");
if ("field" in e2.body.error) throw new Error("No field, no key.");
''',
                    "hint": "Conditionally attach the key — don't send field: undefined.",
                },
                {
                    "name": "zod issues map to details",
                    "code": fn_wrap("apiError, fromZod", "apiError, fromZod") + r'''
const details = fromZod([
  { path: "title", message: "required" },
  { path: "dueDate", message: "must be a date" },
]);
if (details[0].field !== "title" || details[1].message !== "must be a date") throw new Error("Shape converted.");
''',
                    "hint": "A straight map from path=>field.",
                },
            ],
        },
    ],
    {
        "i2-route-review": {
            "title": "Người review route",
            "prompt": 'Viết `reviewRoute(method, path)` chấm độ RESTful: trả về "good" cho route kiểu tài nguyên (path không chứa các từ động từ như get/list/create/delete/update/fetch/save, không phân biệt hoa thường); "verb" khi xuất hiện từ động từ trong path; "missing-id" khi method là PUT/PATCH/DELETE nhưng path không có segment id (segment cuối không phải tham số). Thứ tự kiểm tra: động từ trước, rồi đến sự hiện diện của id.',
            "tests": [
                {"name": "route tài nguyên sạch pass", "hint": "Kiểm tra path với danh sách động từ, rồi sự hiện diện của id với method làm thay đổi trạng thái."},
                {"name": "gắn cờ động từ và thiếu id", "hint": "Segment cuối của path phải tồn tại với PUT/PATCH/DELETE."},
            ],
        },
        "i2-pagination": {
            "title": "Phân trang theo offset",
            "prompt": "Viết `paginate(items, query)` — query là { limit?, offset? } (limit mặc định 10, tối đa 100; offset mặc định 0). Trả về { results, total, next }: results là trang đã cắt; total là items.length; next là offset kế tiếp (dạng số) khi còn item, ngược lại null. Chặn input âm và không nguyên.",
            "tests": [
                {"name": "cắt và tính next", "hint": "offset + limit < total => còn trang kế."},
                {"name": "mặc định và gát chặn", "hint": "Gát: limit <= 100, offset >= 0, đều là số nguyên."},
            ],
        },
        "i2-error-shape": {
            "title": "Bộ tạo hình dạng lỗi thống nhất",
            "prompt": 'Viết `apiError(status, message, field?)` trả về { status, body } với body là { error: { message, field? } } — field chỉ xuất hiện khi được cung cấp. Viết `fromZod(issues)` ánh xạ mảng { path, message } thành hình dạng details [{ field, message }] (path là chuỗi kiểu "dueDate").',
            "tests": [
                {"name": "lỗi đơn với field tùy chọn", "hint": "Gắn key có điều kiện — đừng gửi field: undefined."},
                {"name": "zod issue ánh xạ thành details", "hint": "Map thẳng từ path=>field."},
            ],
        },
    },
    [
        ["i2-route-review", r'''const VERBS = ["get", "list", "create", "delete", "update", "fetch", "save"];
function reviewRoute(method, path) {
  const lower = path.toLowerCase();
  if (VERBS.some((v) => lower.includes(v))) return "verb";
  const segs = lower.split("/").filter(Boolean);
  const hasId = segs.length > 0 && (segs[segs.length - 1] !== segs[segs.length - 1 - (segs.length >= 2 ? 1 : 0)] ? true : segs.length >= 2);
  const needsId = ["PUT", "PATCH", "DELETE"].includes(method);
  if (needsId && !/\/[^/]+$/.test(path) === false && segs.length < 2) return "missing-id";
  return "good";
}''', r'''function reviewRoute(method, path) {
  return "good";
}'''],
        ["i2-pagination", r'''function paginate(items, query) {
  const limit = Math.min(Math.max(Math.trunc(query.limit ?? 10), 1), 100);
  const offset = Math.max(Math.trunc(query.offset ?? 0), 0);
  const results = items.slice(offset, offset + limit);
  const next = offset + limit < items.length ? offset + limit : null;
  return { results, total: items.length, next };
}''', r'''function paginate(items, query) {
  return { results: items, total: items.length, next: null };
}'''],
        ["i2-error-shape", r'''function apiError(status, message, field) {
  const error = { message };
  if (field !== undefined) error.field = field;
  return { status, body: { error } };
}
function fromZod(issues) {
  return issues.map((i) => ({ field: i.path, message: i.message }));
}''', r'''function apiError(status, message, field) {
  return { status, body: { error: { message, field } } };
}
function fromZod(issues) {
  return issues;
}'''],
    ],
)

# ── middleware-practice ─────────────────────────────────────────────────────
write_practice(
    MOD, "middleware-practice",
    "Middleware Pipeline — Practice",
    "Build the onion: a working pipeline runner, ordered guards, and an error boundary that never leaks.",
    "Pipeline Middleware — Luyện tập",
    "Dựng củ hành: một trình chạy pipeline hoạt động thật, các lớp gác có thứ tự, và error boundary không bao giờ lộ lỗi.",
    "middleware-pipeline", 20, "intermediate",
    [
        {
            "id": "i2-pipeline-run",
            "title": "Pipeline Runner",
            "prompt": 'Write `runPipeline(middlewares, handler)` — middlewares is an array of functions (req, next); handler is (req). Each middleware may mutate req then must call next(). Return the final req after the full chain ran. If a middleware never calls next, the chain stops (and you still return the req as-is).',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function runPipeline(middlewares, handler) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "layers run in order",
                    "code": fn_wrap("runPipeline", "runPipeline") + r'''
const order = [];
const req = runPipeline(
  [
    (r, next) => { order.push("a"); r.a = 1; next(); },
    (r, next) => { order.push("b"); r.b = 2; next(); },
  ],
  (r) => { order.push("handler"); r.done = true; }
);
if (order.join(",") !== "a,b,handler") throw new Error("Onion order.");
if (req.done !== true || req.a !== 1 || req.b !== 2) throw new Error("Mutations accumulate.");
''',
                    "hint": "Closure over an index; next advances it.",
                },
                {
                    "name": "chain can stop early",
                    "code": fn_wrap("runPipeline", "runPipeline") + r'''
const order = [];
const req = runPipeline(
  [
    (r, next) => { order.push("guard"); r.blocked = true; },  // no next()
    (r, next) => { order.push("handler"); },
  ],
  (r) => { order.push("never"); }
);
if (order.join(",") !== "guard") throw new Error("A guard that doesn't call next ends the chain.");
if (req.blocked !== true) throw new Error("Req still returned.");
''',
                    "hint": "next is only called by the middleware — respect its choice.",
                },
            ],
        },
        {
            "id": "i2-auth-guard-order",
            "title": "Guard Ordering",
            "prompt": 'Write `securePipeline(config)` returning the correctly ordered middleware names for an authenticated API from this pool: "logger", "bodyParser", "auth", "rateLimiter", "router". Rules: logger runs before everything; bodyParser before auth (auth may read tokens from a parsed body); auth before router; rateLimiter before auth (cheap rejection first).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function securePipeline(config) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "canonical order produced",
                    "code": fn_wrap("securePipeline", "securePipeline") + r'''
const out = securePipeline({});
if (out.join(",") !== "logger,bodyParser,rateLimiter,auth,router") throw new Error("The lesson's order.");
''',
                    "hint": "It's a fixed answer — but justify each adjacent pair to yourself.",
                },
                {
                    "name": "optional pieces are omitted",
                    "code": fn_wrap("securePipeline", "securePipeline") + r'''
const out = securePipeline({ public: true });
if (!out.includes("auth") === false && out.includes("auth")) {
  // public routes keep auth in the list only if config asks; default keeps it
}
if (out[0] !== "logger") throw new Error("Logger always first.");
''',
                    "hint": "Public config drops nothing here — just don't reorder.",
                },
            ],
        },
        {
            "id": "i2-error-boundary",
            "title": "Error Boundary",
            "prompt": 'Write `withErrorBoundary(handler)` returning a wrapped function (input) => output-object. When handler succeeds, return { status: 200, body: result }. When it throws an Error with .status, return { status: err.status, body: { error: err.message } }. Any other throw => { status: 500, body: { error: "internal error" } } — the original message must NOT appear.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function withErrorBoundary(handler) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "success and typed errors pass through",
                    "code": "const fn = new Function(code + \"\\nreturn { withErrorBoundary };\");\nconst { withErrorBoundary } = fn();\nconst ok = withErrorBoundary((x) => x * 2);\nconst out = ok(21);\nif (out.status !== 200 || out.body !== 42) throw new Error(\"Success wraps as 200.\");\nconst nf = withErrorBoundary(() => { const e = new Error(\"task not found\"); e.status = 404; throw e; });\nif (nf().status !== 404 || nf().body.error !== \"task not found\") throw new Error(\"Typed error keeps its message.\");",
                    "hint": "try/catch inside the wrapper; check for a numeric status.",
                },
                {
                    "code": 'const fn = new Function(code + "\\nreturn { withErrorBoundary };");\\nconst { withErrorBoundary } = fn();\\n'
                        + 'const bomb = withErrorBoundary(() => { throw new Error("secret: DB password is hunter2"); });\\n'
                        + 'const out = bomb();\\n'
                        + 'if (out.status !== 500) throw new Error("Unexpected throw => 500.");\\n'
                        + 'if (out.body.error !== "internal error") throw new Error("The raw message must not leak.");\\n'
                        + 'if (JSON.stringify(out).includes("hunter2")) throw new Error("Sanitized means sanitized.");',
                },
            ],
        },
    ],
    {
        "i2-pipeline-run": {
            "title": "Trình chạy pipeline",
            "prompt": 'Viết `runPipeline(middlewares, handler)` — middlewares là mảng hàm (req, next); handler là (req). Mỗi middleware có thể mutate req rồi phải gọi next(). Trả về req cuối cùng sau khi toàn bộ chuỗi đã chạy. Nếu một middleware không gọi next, chuỗi dừng (và bạn vẫn trả về req nguyên trạng).',
            "tests": [
                {"name": "các lớp chạy theo thứ tự", "hint": "Closure trên một chỉ số; next tăng nó."},
                {"name": "chuỗi có thể dừng sớm", "hint": "next chỉ được gọi bởi middleware — tôn trọng lựa chọn của nó."},
            ],
        },
        "i2-auth-guard-order": {
            "title": "Thứ tự lớp gác",
            'prompt': 'Viết `securePipeline(config)` trả về tên middleware đúng thứ tự cho một API có xác thực từ nhóm sau: "logger", "bodyParser", "auth", "rateLimiter", "router". Quy tắc: logger chạy trước tất cả; bodyParser trước auth (auth có thể đọc token từ body đã parse); auth trước router; rateLimiter trước auth (từ chối rẻ trước).',
            "tests": [
                {"name": "tạo ra thứ tự chuẩn", "hint": "Đây là đáp án cố định — nhưng tự biện minh cho từng cặp liền kề."},
                {"name": "thành phần tùy chọn được bỏ đi", "hint": "Cấu hình public ở đây không bỏ gì — chỉ đừng đảo thứ tự."},
            ],
        },
        "i2-error-boundary": {
            "title": "Error boundary",
            "prompt": 'Viết `withErrorBoundary(handler)` trả về một hàm đã bọc (input) => output-object. Khi handler thành công, trả về { status: 200, body: result }. Khi nó ném Error có .status, trả về { status: err.status, body: { error: err.message } }. Bất kỳ lần ném khác => { status: 500, body: { error: "internal error" } } — message gốc KHÔNG được xuất hiện.',
            "tests": [
                {"name": "thành công và lỗi có kiểu đi xuyên qua", "hint": "try/catch bên trong wrapper; kiểm tra status có phải số không."},
                {"name": "lỗi nội bộ được làm sạch", "hint": "Nhánh else thay message một cách vô điều kiện."},
            ],
        },
    },
    [
        ["i2-pipeline-run", r'''function runPipeline(middlewares, handler) {
  const req = {};
  let i = 0;
  const next = () => {
    const mw = middlewares[i++];
    if (mw) mw(req, next);
    else handler(req);
  };
  next();
  return req;
}''', r'''function runPipeline(middlewares, handler) {
  const req = {};
  handler(req);
  return req;
}'''],
        ["i2-auth-guard-order", r'''function securePipeline(config) {
  return ["logger", "bodyParser", "rateLimiter", "auth", "router"];
}''', r'''function securePipeline(config) {
  return ["auth", "router"];
}'''],
        ["i2-error-boundary", r'''function withErrorBoundary(handler) {
  return (input) => {
    try {
      return { status: 200, body: handler(input) };
    } catch (err) {
      if (err && typeof err.status === "number") {
        return { status: err.status, body: { error: err.message } };
      }
      return { status: 500, body: { error: "internal error" } };
    }
  };
}''', r'''function withErrorBoundary(handler) {
  return (input) => ({ status: 200, body: handler(input) });
}'''],
    ],
)

# ── crud-practice ───────────────────────────────────────────────────────────
write_practice(
    MOD, "crud-practice",
    "In-Memory CRUD — Practice",
    "The mini-build: a working task store with validation, ownership, and truthful codes — a full API's logic core.",
    "CRUD trong bộ nhớ — Luyện tập",
    "Mini-build: một task store hoạt động thật với validation, quyền sở hữu, và mã trung thực — lõi logic của một API hoàn chỉnh.",
    "validation-errors", 25, "intermediate",
    [
        {
            "id": "i2-store-create",
            "title": "Task Store: Create",
            "prompt": 'Write `makeStore()` returning an object with `create(body, userId)` — validates: title (string, 1-200 chars) and due (optional ISO-parseable date). Valid => { ok: true, task: { id: "t1", title, due: due ?? null, ownerId: userId, done: false } }; invalid => { ok: false, errors: [{field, message}...] } (collect all errors). IDs increment: t1, t2...',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function makeStore() {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "creates valid tasks with auto ids",
                    "code": "const fn = new Function(code + \"\\nreturn { makeStore };\");\nconst { makeStore } = fn();\nconst store = makeStore();\nconst r1 = store.create({ title: \"Ship it\" }, \"u1\");\nif (!r1.ok || r1.task.id !== \"t1\" || r1.task.ownerId !== \"u1\") throw new Error(\"First task t1 owned by u1.\");\nconst r2 = store.create({ title: \"Again\" }, \"u2\");\nif (r2.task.id !== \"t2\") throw new Error(\"Ids increment.\");",
                    "hint": "A counter closure; stamp ownerId and done: false.",
                },
                {
                    "name": "collects all validation errors",
                    "code": 'const fn = new Function(code + "\\nreturn { makeStore };");\nconst { makeStore } = fn();\nconst store = makeStore();\nconst bad = store.create({ title: "", due: "not-a-date" }, "u1");\nif (bad.ok !== false) throw new Error("Invalid => ok false.");\nif (bad.errors.length !== 2) throw new Error("Both errors collected.");\nif (!bad.errors.some((e) => e.field === "title") || !bad.errors.some((e) => e.field === "due")) throw new Error("Each failing field named.");',
                    "hint": "Push into an array through both checks; return it.",
                },
            ],
        },
        {
            "id": "i2-store-authz",
            "title": "Task Store: Ownership",
            "prompt": 'Extend the store: `update(id, patch, userId)` and `remove(id, userId)` — both enforce ownership: if the task exists but ownerId !== userId, return { ok: false, status: 403 }; missing task => { ok: false, status: 404 }. update applies only `title` and `done` from patch (ignore other fields) and returns { ok: true, task }; remove returns { ok: true } and actually removes.',
            'difficulty': "intermediate",
            "level": "independent",
            "boilerplate": "function makeStore() {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "owners update and remove",
                    "code": 'const fn = new Function(code + "\\nreturn { makeStore };");\nconst { makeStore } = fn();\nconst store = makeStore();\nconst { task } = store.create({ title: "A" }, "u1");\nconst up = store.update(task.id, { title: "B", ownerId: "u9" }, "u1");\nif (!up.ok || up.task.title !== "B" || up.task.ownerId === "u9") throw new Error("title applied, ownerId ignored.");\nif (store.remove(task.id, "u1").ok !== true) throw new Error("Owner removes.");\nif (store.update(task.id, { title: "C" }, "u1").status !== 404) throw new Error("Gone after removal.");',
                    "hint": "403 for strangers, 404 for missing; whitelist patched fields.",
                },
                {
                    "name": "strangers get 403",
                    "code": 'const fn = new Function(code + "\\nreturn { makeStore };");\nconst { makeStore } = fn();\nconst store = makeStore();\nconst { task } = store.create({ title: "Secret" }, "u1");\nif (store.update(task.id, { title: "Hacked" }, "u2").status !== 403) throw new Error("Stranger cannot update.");\nif (store.remove(task.id, "u2").status !== 403) throw new Error("Stranger cannot delete.");\nif (store.update(task.id, { title: "Safe?" }, "u1").ok) throw new Error("Title unchanged by the stranger\'s attempt.");',
                    "hint": "Ownership check runs before any mutation.",
                },
            ],
        },
        {
            "id": "i2-store-query",
            "title": "Task Store: Query",
            "prompt": 'Add `list(query, userId)` — returns only the caller\'s tasks (ownership at the read path!), filtered: query.done === true|false filters on the done flag; query.title substring-matches case-insensitively. Sorted by id ascending. No query => all own tasks.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function makeStore() {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "ownership applies to reads",
                    "code": 'const fn = new Function(code + "\\nreturn { makeStore };");\nconst { makeStore } = fn();\nconst store = makeStore();\nstore.create({ title: "Mine" }, "u1");\nstore.create({ title: "Theirs" }, "u2");\nconst mine = store.list({}, "u1");\nif (mine.length !== 1 || mine[0].title !== "Mine") throw new Error("u1 sees only u1\'s tasks.");',
                    "hint": "Filter by ownerId before any other filter.",
                },
                {
                    "name": "filters compose",
                    "code": 'const fn = new Function(code + "\\nreturn { makeStore };");\nconst { makeStore } = fn();\nconst store = makeStore();\nconst a = store.create({ title: "Write tests" }, "u1").task;\nconst b = store.create({ title: "Write docs" }, "u1").task;\nstore.update(b.id, { done: true }, "u1");\nconst open = store.list({ done: false }, "u1");\nif (open.length !== 1 || open[0].id !== a.id) throw new Error("done:false filters.");\nconst wr = store.list({ title: "WRITE" }, "u1");\nif (wr.length !== 2) throw new Error("Case-insensitive substring.");',
                    "hint": "Chain the filters; toLowerCase both sides.",
                },
            ],
        },
    ],
    {
        "i2-store-create": {
            "title": "Task Store: Tạo",
            "prompt": 'Viết `makeStore()` trả về object với `create(body, userId)` — kiểm tra: title (chuỗi, 1-200 ký tự) và due (ngày ISO-parse được, tùy chọn). Hợp lệ => { ok: true, task: { id: "t1", title, due: due ?? null, ownerId: userId, done: false } }; không hợp lệ => { ok: false, errors: [{field, message}...] } (thu thập mọi lỗi). ID tăng dần: t1, t2...',
            "tests": [
                {"name": "tạo task hợp lệ với id tự tăng", "hint": "Một counter closure; đóng dấu ownerId và done: false."},
                {"name": "thu thập mọi lỗi validation", "hint": "Push vào mảng qua cả hai check; trả về mảng đó."},
            ],
        },
        "i2-store-authz": {
            "title": "Task Store: Quyền sở hữu",
            "prompt": 'Mở rộng store: `update(id, patch, userId)` và `remove(id, userId)` — cả hai thực thi quyền sở hữu: nếu task tồn tại nhưng ownerId !== userId, trả về { ok: false, status: 403 }; task thiếu => { ok: false, status: 404 }. update chỉ áp dụng `title` và `done` từ patch (bỏ qua trường khác) và trả về { ok: true, task }; remove trả về { ok: true } và xóa thật.',
            "tests": [
                {"name": "owner cập nhật và xóa", "hint": "403 cho người lạ, 404 cho thứ thiếu; whitelist các trường được patch."},
                {"name": "người lạ nhận 403", "hint": "Kiểm tra quyền sở hữu chạy trước mọi mutation."},
            ],
        },
        "i2-store-query": {
            "title": "Task Store: Truy vấn",
            "prompt": 'Thêm `list(query, userId)` — chỉ trả về task của người gọi (quyền sở hữu ngay trên đường đọc!), lọc: query.done === true|false lọc theo cờ done; query.title so khớp chuỗi con không phân biệt hoa thường. Sắp theo id tăng dần. Không query => toàn bộ task của mình.',
            "tests": [
                {"name": "quyền sở hữu áp cả khi đọc", "hint": "Lọc theo ownerId trước mọi filter khác."},
                {"name": "các filter ghép được", "hint": "Xích các filter; toLowerCase cả hai phía."},
            ],
        },
    },
    [
        ["i2-store-create", r'''function makeStore() {
  let n = 0;
  const tasks = new Map();
  return {
    create(body, userId) {
      const errors = [];
      const title = typeof body.title === "string" ? body.title.trim() : "";
      if (!title || title.length > 200) errors.push({ field: "title", message: "1-200 chars" });
      if (body.due !== undefined && body.due !== null && !Number.isInteger(Date.parse(body.due))) {
        errors.push({ field: "due", message: "ISO date" });
      }
      if (errors.length) return { ok: false, errors };
      const id = "t" + ++n;
      const task = { id, title, due: body.due ?? null, ownerId: userId, done: false };
      tasks.set(id, task);
      return { ok: true, task };
    },
  };
}''', r'''function makeStore() {
  return {
    create(body, userId) {
      return { ok: true, task: { id: "t1", title: body.title, ownerId: userId, done: false } };
    },
  };
}'''],
        ["i2-store-authz", r'''function makeStore() {
  let n = 0;
  const tasks = new Map();
  return {
    create(body, userId) {
      const id = "t" + ++n;
      const task = { id, title: body.title, due: body.due ?? null, ownerId: userId, done: false };
      tasks.set(id, task);
      return { ok: true, task };
    },
    update(id, patch, userId) {
      const task = tasks.get(id);
      if (!task) return { ok: false, status: 404 };
      if (task.ownerId !== userId) return { ok: false, status: 403 };
      if (typeof patch.title === "string") task.title = patch.title;
      if (typeof patch.done === "boolean") task.done = patch.done;
      return { ok: true, task };
    },
    remove(id, userId) {
      const task = tasks.get(id);
      if (!task) return { ok: false, status: 404 };
      if (task.ownerId !== userId) return { ok: false, status: 403 };
      tasks.delete(id);
      return { ok: true };
    },
  };
}''', r'''function makeStore() {
  const tasks = new Map();
  return {
    update(id, patch, userId) {
      const task = tasks.get(id);
      if (task.ownerId !== userId) return { ok: false, status: 403 };
      task.title = patch.title;
      return { ok: true, task };
    },
    remove(id, userId) {
      tasks.delete(id);
      return { ok: true };
    },
  };
}'''],
        ["i2-store-query", r'''function makeStore() {
  let n = 0;
  const tasks = new Map();
  return {
    create(body, userId) {
      const id = "t" + ++n;
      const task = { id, title: body.title, ownerId: userId, done: false };
      tasks.set(id, task);
      return { ok: true, task };
    },
    update(id, patch, userId) {
      const task = tasks.get(id);
      if (task.ownerId !== userId) return { ok: false, status: 403 };
      if (typeof patch.done === "boolean") task.done = patch.done;
      return { ok: true, task };
    },
    list(query = {}, userId) {
      let out = [...tasks.values()].filter((t) => t.ownerId === userId);
      if (typeof query.done === "boolean") out = out.filter((t) => t.done === query.done);
      if (query.title) out = out.filter((t) => t.title.toLowerCase().includes(query.title.toLowerCase()));
      return out.sort((a, b) => a.id.localeCompare(b.id));
    },
  };
}''', r'''function makeStore() {
  const tasks = new Map();
  return {
    list(query, userId) {
      return [...tasks.values()];
    },
  };
}'''],
    ],
)

print("Module 10 practices written.")
