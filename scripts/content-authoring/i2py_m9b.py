#!/usr/bin/env python3
"""Module 9 practices: xss, authz, headers, audit. Raw strings throughout."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "web-security"

# ── xss-practice ────────────────────────────────────────────────────────────
write_practice(
    MOD, "xss-practice",
    "XSS Sinks & Encoding — Practice",
    "Recognize dangerous sinks, encode per context, and verify a payload renders as inert text.",
    "Sink XSS & mã hóa — Luyện tập",
    "Nhận diện sink nguy hiểm, mã hóa theo ngữ cảnh, và xác minh payload hiển thị dưới dạng văn bản trơ.",
    "xss-and-encoding", 20, "intermediate",
    [
        {
            "id": "i2-xss-sink",
            "title": "Sink or Safe",
            "prompt": 'Write `isDangerousSink(line)` — return true when the line writes data into an execution context: contains "innerHTML =", "outerHTML =", "document.write(", or "eval(". Assignment via += also counts. Ordinary DOM creation (createElement/textContent) is safe.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function isDangerousSink(line) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "flags the classic sinks",
                    "code": fn_wrap("isDangerousSink", "isDangerousSink") + r'''
if (!isDangerousSink('list.innerHTML = data')) throw new Error("innerHTML assignment.");
if (!isDangerousSink('document.write(userInput)')) throw new Error("document.write.");
if (!isDangerousSink('eval(code)')) throw new Error("eval is always a sink.");
''',
                    "hint": "Substring checks — the lesson is knowing the list.",
                },
                {
                    "name": "safe patterns pass",
                    "code": fn_wrap("isDangerousSink", "isDangerousSink") + r'''
if (isDangerousSink('el.textContent = data')) throw new Error("textContent is the safe choice.");
if (isDangerousSink('const el = document.createElement("div")')) throw new Error("Creation without data injection.");
if (isDangerousSink('el.innerHTML;')) throw new Error("Reading innerHTML is not a write sink.");
''',
                    "hint": "Require the assignment or call, not a mere mention.",
                },
            ],
        },
        {
            "id": "i2-html-encode",
            "title": "HTML Encoder",
            "prompt": 'Write `encodeHTML(s)` escaping exactly the five HTML-significant characters: & < > " \'. Order matters — & must be escaped first. Write `rendersAsText(html)` returning true when encodeHTML was applied to the payload (the encoded string contains "&lt;" and no raw "<").',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function encodeHTML(s) {\n  // your code\n}\n\nfunction rendersAsText(html) {\n  // your code — true when html is safely inert text\n}\n",
            "tests": [
                {
                    "name": "escapes all five characters",
                    "code": fn_wrap("encodeHTML", "encodeHTML") + r'''
if (encodeHTML("a & b") !== "a &amp; b") throw new Error("Ampersand first.");
if (encodeHTML("<b>") !== "&lt;b&gt;") throw new Error("Angle brackets escaped.");
if (!encodeHTML('say "hi"').includes("&quot;")) throw new Error("Double quote escaped.");
if (!encodeHTML("it's").includes("&#39;")) throw new Error("Single quote escaped.");
if (encodeHTML("<img src=x>") !== "&lt;img src=x&gt;") throw new Error("Payload fully disarmed.");
''',
                    "hint": "A chain of replace calls; start with &.",
                },
                {
                    "name": "payload detection",
                    "code": fn_wrap("encodeHTML, rendersAsText", "encodeHTML, rendersAsText") + r'''
if (!rendersAsText(encodeHTML('<img src=x onerror=alert(1)>'))) throw new Error("Encoded payload is inert.");
if (rendersAsText('<img src=x>')) throw new Error("Raw markup is not inert.");
''',
                    "hint": "Inert = no raw '<' remains.",
                },
            ],
        },
        {
            "id": "i2-url-encode",
            "title": "URL Parameter Encoder",
            "prompt": 'Write `buildSearchUrl(base, params)` — params is an object; return base + "?" + encoded query string where keys and values run through encodeURIComponent and pairs join with "&". An empty params object returns base unchanged.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function buildSearchUrl(base, params) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "encodes keys and values",
                    "code": fn_wrap("buildSearchUrl", "buildSearchUrl") + r'''
const u = buildSearchUrl("/search", { q: "coffee & tea", page: "2" });
if (u !== "/search?q=coffee%20%26%20tea&page=2") throw new Error("Space becomes %20, & becomes %26.");
''',
                    "hint": "encodeURIComponent encodes space as %20.",
                },
                {
                    "name": "empty params return base",
                    "code": fn_wrap("buildSearchUrl", "buildSearchUrl") + r'''
if (buildSearchUrl("/search", {}) !== "/search") throw new Error("No params, no ?.");
''',
                    "hint": "Guard the empty case before joining.",
                },
            ],
        },
    ],
    {
        "i2-xss-sink": {
            "title": "Sink hay An toàn",
            "prompt": 'Viết `isDangerousSink(line)` — trả về true khi dòng đó ghi dữ liệu vào ngữ cảnh thực thi: chứa "innerHTML =", "outerHTML =", "document.write(", hoặc "eval(". Phép gán qua += cũng tính. Tạo DOM thường (createElement/textContent) là an toàn.',
            "tests": [
                {"name": "gắn cờ các sink kinh điển", "hint": "Kiểm tra substring — bài học là biết danh sách."},
                {"name": "mẫu an toàn pass", "hint": "Yêu cầu phép gán hoặc lời gọi, chứ không chỉ nhắc tên."},
            ],
        },
        "i2-html-encode": {
            "title": "Bộ mã hóa HTML",
            "prompt": 'Viết `encodeHTML(s)` escape đúng năm ký tự có ý nghĩa trong HTML: & < > " \'. Thứ tự quan trọng — & phải được escape trước. Viết `rendersAsText(html)` trả về true khi encodeHTML đã được áp lên payload (chuỗi đã mã hóa chứa "&lt;" và không còn "<" thô).',
            "tests": [
                {"name": "escape đủ năm ký tự", "hint": "Một chuỗi replace; bắt đầu với &."},
                {"name": "phát hiện payload", "hint": "Trơ = không còn '<' thô."},
            ],
        },
        "i2-url-encode": {
            "title": "Bộ mã hóa tham số URL",
            "prompt": 'Viết `buildSearchUrl(base, params)` — params là object; trả về base + "?" + chuỗi query đã mã hóa trong đó key và value chạy qua encodeURIComponent và các cặp nối bằng "&". params rỗng trả về base nguyên trạng.',
            "tests": [
                {"name": "mã hóa key và value", "hint": "encodeURIComponent mã hóa space thành %20."},
                {"name": "params rỗng trả về base", "hint": "Chặn trường hợp rỗng trước khi nối."},
            ],
        },
    },
    [
        ["i2-xss-sink", r'''function isDangerousSink(line) {
  const sinks = ["innerHTML =", "innerHTML +=", "outerHTML =", "document.write(", "eval("];
  return sinks.some((s) => line.includes(s));
}''', r'''function isDangerousSink(line) {
  return line.includes("innerHTML");
}'''],
        ["i2-html-encode", r'''function encodeHTML(s) {
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
function rendersAsText(html) {
  return html.includes("&lt;") && !html.includes("<");
}''', r'''function encodeHTML(s) {
  return s;
}
function rendersAsText(html) {
  return true;
}'''],
        ["i2-url-encode", r'''function buildSearchUrl(base, params) {
  const entries = Object.entries(params);
  if (entries.length === 0) return base;
  const qs = entries
    .map(([k, v]) => encodeURIComponent(k) + "=" + encodeURIComponent(v))
    .join("&");
  return base + "?" + qs;
}''', r'''function buildSearchUrl(base, params) {
  return base + "?" + JSON.stringify(params);
}'''],
    ],
)

# ── authz-practice ──────────────────────────────────────────────────────────
write_practice(
    MOD, "authz-practice",
    "Authorization Guards — Practice",
    "Enforce ownership on every read, deny by default on role checks, and build an IDOR detector.",
    "Trình gác phân quyền — Luyện tập",
    "Thực thi quyền sở hữu trên mọi lần đọc, mặc định từ chối với kiểm tra vai trò, và dựng bộ dò IDOR.",
    "authn-authz-sessions", 20, "intermediate",
    [
        {
            "id": "i2-ownership-guard",
            "title": "Ownership Guard",
            "prompt": 'Write `canRead(record, user)` — record is { id, ownerId, visibility } where visibility is "public" | "private"; user is { id, role } with role "admin" | "user". Return true when: record is public; OR the user owns it; OR the user is an admin. Otherwise false.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function canRead(record, user) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "public, owner, and admin paths",
                    "code": fn_wrap("canRead", "canRead") + r'''
const rec = { id: 1, ownerId: "u2", visibility: "private" };
if (!canRead({ ...rec, visibility: "public" }, { id: "u1", role: "user" })) throw new Error("Public is readable by all.");
if (!canRead(rec, { id: "u2", role: "user" })) throw new Error("Owner reads own record.");
if (!canRead(rec, { id: "u9", role: "admin" })) throw new Error("Admin bypasses (by design here).");
if (canRead(rec, { id: "u1", role: "user" })) throw new Error("Stranger denied on private record.");
''',
                    "hint": "Three or-ed conditions.",
                },
                {
                    "name": "missing user denies",
                    "code": fn_wrap("canRead", "canRead") + r'''
const rec = { id: 1, ownerId: "u2", visibility: "private" };
if (canRead(rec, null)) throw new Error("No user => no access.");
if (canRead(null, { id: "u1", role: "user" })) throw new Error("No record => no access.");
''',
                    "hint": "Fail closed on absent inputs.",
                },
            ],
        },
        {
            "id": "i2-role-gate",
            "title": "Role Gate (deny by default)",
            "prompt": 'Write `authorize(user, action, resource)` — a permission table maps role => allowed actions: admin: all; editor: ["read", "write"]; viewer: ["read"]. Unknown roles and unknown actions must be DENIED (default deny). Return "allow" or "deny".',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function authorize(user, action, resource) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "known roles get their actions",
                    "code": fn_wrap("authorize", "authorize") + r'''
if (authorize({ role: "admin" }, "delete", "doc") !== "allow") throw new Error("Admin: all actions.");
if (authorize({ role: "editor" }, "write", "doc") !== "allow") throw new Error("Editor writes.");
if (authorize({ role: "viewer" }, "write", "doc") !== "deny") throw new Error("Viewer cannot write.");
''',
                    "hint": "Table lookup, then membership.",
                },
                {
                    "name": "unknown roles/actions deny",
                    "code": fn_wrap("authorize", "authorize") + r'''
if (authorize({ role: "ghost" }, "read", "doc") !== "deny") throw new Error("Unknown role denied.");
if (authorize({ role: "viewer" }, "teleport", "doc") !== "deny") throw new Error("Unknown action denied.");
if (authorize(null, "read", "doc") !== "deny") throw new Error("Anonymous denied.");
''',
                    "hint": "Default deny covers every gap.",
                },
            ],
        },
        {
            "id": "i2-idor-scan",
            "title": "IDOR Detector",
            "prompt": 'Write `findIdor(routes)` — routes is an array of { path, hasOwnershipCheck, method }. A route is an IDOR risk when its path contains ":id" (or "/:id/") and hasOwnershipCheck is false. Return the risky paths sorted alphabetically. GET routes count too — reads leak data.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function findIdor(routes) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "flags unguarded id routes",
                    "code": fn_wrap("findIdor", "findIdor") + r'''
const routes = [
  { path: "/api/orders/:id", hasOwnershipCheck: false, method: "GET" },
  { path: "/api/orders/:id", hasOwnershipCheck: true, method: "GET" },
  { path: "/api/profile", hasOwnershipCheck: false, method: "GET" },
];
if (findIdor(routes).join(",") !== "/api/orders/:id") throw new Error("Only the unguarded id route.");
''',
                    "hint": "Both conditions: id in path, no check.",
                },
                {
                    "name": "sorted output, empty when clean",
                    "code": fn_wrap("findIdor", "findIdor") + r'''
const routes = [
  { path: "/api/b/:id", hasOwnershipCheck: false, method: "GET" },
  { path: "/api/a/:id", hasOwnershipCheck: false, method: "GET" },
];
if (findIdor(routes).join(",") !== "/api/a/:id,/api/b/:id") throw new Error("Alphabetical.");
if (findIdor([]).length !== 0) throw new Error("No routes, no risks.");
''',
                    "hint": "filter, map, sort.",
                },
            ],
        },
    ],
    {
        "i2-ownership-guard": {
            "title": "Trình gác quyền sở hữu",
            "prompt": 'Viết `canRead(record, user)` — record là { id, ownerId, visibility } với visibility là "public" | "private"; user là { id, role } với role "admin" | "user". Trả về true khi: record công khai; HOẶC user sở hữu nó; HOẶC user là admin. Còn lại false.',
            "tests": [
                {"name": "các đường public, owner và admin", "hint": "Ba điều kiện nối OR."},
                {"name": "thiếu user là từ chối", "hint": "Fail closed khi thiếu input."},
            ],
        },
        "i2-role-gate": {
            "title": "Cổng vai trò (mặc định từ chối)",
            "prompt": 'Viết `authorize(user, action, resource)` — bảng quyền ánh xạ role => các action được phép: admin: tất cả; editor: ["read", "write"]; viewer: ["read"]. Vai trò và action lạ phải bị TỪ CHỐI (default deny). Trả về "allow" hoặc "deny".',
            "tests": [
                {"name": "vai trò đã biết nhận đúng action", "hint": "Tra bảng, rồi kiểm tra thuộc tính."},
                {"name": "vai trò/action lạ bị từ chối", "hint": "Default deny phủ mọi lỗ hổng."},
            ],
        },
        "i2-idor-scan": {
            "title": "Bộ dò IDOR",
            "prompt": 'Viết `findIdor(routes)` — routes là mảng { path, hasOwnershipCheck, method }. Một route có rủi ro IDOR khi path chứa ":id" (hoặc "/:id/") và hasOwnershipCheck là false. Trả về các path rủi ro đã sắp theo bảng chữ cái. Route GET cũng tính — lệnh đọc làm lộ dữ liệu.',
            "tests": [
                {"name": "gắn cờ route id không gác", "hint": "Cả hai điều kiện: có id trong path, không có check."},
                {"name": "output sắp xếp, rỗng khi sạch", "hint": "filter, map, sort."},
            ],
        },
    },
    [
        ["i2-ownership-guard", r'''function canRead(record, user) {
  if (!record || !user) return false;
  return (
    record.visibility === "public" ||
    record.ownerId === user.id ||
    user.role === "admin"
  );
}''', r'''function canRead(record, user) {
  return record.visibility === "public";
}'''],
        ["i2-role-gate", r'''const TABLE = {
  admin: ["read", "write", "delete"],
  editor: ["read", "write"],
  viewer: ["read"],
};
function authorize(user, action, resource) {
  const allowed = user && TABLE[user.role];
  return allowed && allowed.includes(action) ? "allow" : "deny";
}''', r'''function authorize(user, action, resource) {
  return user.role === "admin" ? "allow" : "deny";
}'''],
        ["i2-idor-scan", r'''function findIdor(routes) {
  return routes
    .filter((r) => r.path.includes(":id") && !r.hasOwnershipCheck)
    .map((r) => r.path)
    .sort();
}''', r'''function findIdor(routes) {
  return routes.filter((r) => !r.hasOwnershipCheck).map((r) => r.path);
}'''],
    ],
)

# ── headers-practice ────────────────────────────────────────────────────────
write_practice(
    MOD, "headers-practice",
    "Headers & CORS — Practice",
    "Parse and judge security headers, apply the CSP model, and settle CORS preflight decisions in code.",
    "Header & CORS — Luyện tập",
    "Parse và đánh giá security header, áp dụng mô hình CSP, và quyết định preflight CORS trong code.",
    "cors-csrf-headers", 18, "intermediate",
    [
        {
            "id": "i2-header-audit",
            "title": "Header Auditor",
            "prompt": 'Write `auditHeaders(headers)` — headers is an object of response headers. Return an array of missing-hardening findings, checked in this order: no "Content-Security-Policy" => "missing-csp"; no "Strict-Transport-Security" => "missing-hsts"; no "X-Content-Type-Options" => "missing-nosniff"; "X-Frame-Options" not "DENY" (absent counts) => "clickjackable". Empty array = hardened.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function auditHeaders(headers) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "reports each gap in order",
                    "code": fn_wrap("auditHeaders", "auditHeaders") + r'''
if (auditHeaders({}).join(",") !== "missing-csp,missing-hsts,missing-nosniff,clickjackable") throw new Error("All four findings on an empty set.");
if (auditHeaders({ "Content-Security-Policy": "default-src 'self'" }).join(",") !== "missing-hsts,missing-nosniff,clickjackable") throw new Error("CSP clears its finding.");
''',
                    "hint": "Sequential checks, each pushing a label.",
                },
                {
                    "name": "hardened headers pass clean",
                    "code": fn_wrap("auditHeaders", "auditHeaders") + r'''
const h = {
  "Content-Security-Policy": "default-src 'self'",
  "Strict-Transport-Security": "max-age=31536000",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
};
if (auditHeaders(h).length !== 0) throw new Error("Fully hardened => no findings.");
''',
                    "hint": "Every check has a positive case.",
                },
            ],
        },
        {
            "id": "i2-csp-parse",
            "title": "CSP Directive Check",
            "prompt": 'Write `cspAllows(policy, kind)` — policy is a CSP string like "default-src \'self\'; img-src \'self\' data:"; kind is "script" | "img". Scripts need a script-src directive (falling back to default-src); images use img-src or default-src. Return true when the directive\'s source list contains \'self\' or data: — false otherwise (including when no directives exist at all).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function cspAllows(policy, kind) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "explicit directives win",
                    "code": fn_wrap("cspAllows", "cspAllows") + r'''
const p = "default-src 'self'; img-src 'self' data:";
if (!cspAllows(p, "img")) throw new Error("img-src present, so img allowed.");
if (!cspAllows("img-src 'self'", "img")) throw new Error("img-src alone allows images.");
if (!cspAllows("default-src 'self'", "script")) throw new Error("default-src covers scripts.");
''',
                    "hint": "Parse into directive => sources; pick the specific one or default.",
                },
                {
                    "name": "no policy blocks everything",
                    "code": fn_wrap("cspAllows", "cspAllows") + r'''
if (cspAllows("", "script") !== false) throw new Error("Empty policy allows nothing.");
if (cspAllows("img-src 'self'", "script") !== false) throw new Error("No default-src, no script-src => scripts blocked.");
''',
                    "hint": "Missing directive + missing default = deny.",
                },
            ],
        },
        {
            "id": "i2-cors-decide",
            "title": "CORS Decision Engine",
            "prompt": 'Write `corsDecision(origin, allowedOrigins, credentials)` — origin is the request\'s Origin header; allowedOrigins is an array (may contain "*"); credentials is boolean. Rules: origin not in list (and no "*") => "deny"; "*" with credentials => "deny" (forbidden combo); origin in list (or "*") without credentials => "allow"; origin in list with credentials => "allow-with-credentials".',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function corsDecision(origin, allowedOrigins, credentials) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "deny paths first",
                    "code": fn_wrap("corsDecision", "corsDecision") + r'''
if (corsDecision("https://evil.com", ["https://app.com"], false) !== "deny") throw new Error("Unknown origin denied.");
if (corsDecision("https://app.com", ["*"], true) !== "deny") throw new Error("Wildcard + credentials forbidden.");
''',
                    "hint": "Two explicit deny rules before any allow.",
                },
                {
                    "name": "allow paths",
                    "code": fn_wrap("corsDecision", "corsDecision") + r'''
if (corsDecision("https://app.com", ["*"], false) !== "allow") throw new Error("Wildcard, no creds => allow.");
if (corsDecision("https://app.com", ["https://app.com"], true) !== "allow-with-credentials") throw new Error("Exact origin + creds.");
''',
                    "hint": "Then the two allow rules.",
                },
            ],
        },
    ],
    {
        "i2-header-audit": {
            "title": "Trình kiểm toán header",
            "prompt": 'Viết `auditHeaders(headers)` — headers là object các response header. Trả về mảng các phát hiện thiếu gia cố, kiểm tra theo thứ tự này: thiếu "Content-Security-Policy" => "missing-csp"; thiếu "Strict-Transport-Security" => "missing-hsts"; thiếu "X-Content-Type-Options" => "missing-nosniff"; "X-Frame-Options" không phải "DENY" (vắng mặt cũng tính) => "clickjackable". Mảng rỗng = đã gia cố.',
            "tests": [
                {"name": "báo từng khoảng trống theo thứ tự", "hint": "Các check tuần tự, mỗi check push một nhãn."},
                {"name": "header đủ mạnh pass sạch", "hint": "Mọi check đều có ca dương."},
            ],
        },
        "i2-csp-parse": {
            "title": "Kiểm tra directive CSP",
            "prompt": 'Viết `cspAllows(policy, kind)` — policy là chuỗi CSP như "default-src \'self\'; img-src \'self\' data:"; kind là "script" | "img". Script cần directive script-src (fallback về default-src); ảnh dùng img-src hoặc default-src. Trả về true khi danh sách nguồn của directive chứa \'self\' hoặc data: — false nếu ngược lại (kể cả khi không có directive nào).',
            "tests": [
                {"name": "directive tường minh thắng", "hint": "Parse thành directive => nguồn; chọn directive riêng hoặc default."},
                {"name": "không có policy là chặn tất cả", "hint": "Thiếu directive + thiếu default = deny."},
            ],
        },
        "i2-cors-decide": {
            "title": "Cỗ máy quyết định CORS",
            "prompt": 'Viết `corsDecision(origin, allowedOrigins, credentials)` — origin là header Origin của request; allowedOrigins là mảng (có thể chứa "*"); credentials là boolean. Quy tắc: origin không có trong danh sách (và không có "*") => "deny"; "*" kèm credentials => "deny" (cặp bị cấm); origin có trong danh sách (hoặc "*") không kèm credentials => "allow"; origin có trong danh sách kèm credentials => "allow-with-credentials".',
            "tests": [
                {"name": "các đường deny trước", "hint": "Hai quy tắc deny tường minh trước bất kỳ allow nào."},
                {"name": "các đường allow", "hint": "Rồi đến hai quy tắc allow."},
            ],
        },
    },
    [
        ["i2-header-audit", r'''function auditHeaders(headers) {
  const out = [];
  if (!headers["Content-Security-Policy"]) out.push("missing-csp");
  if (!headers["Strict-Transport-Security"]) out.push("missing-hsts");
  if (!headers["X-Content-Type-Options"]) out.push("missing-nosniff");
  if (headers["X-Frame-Options"] !== "DENY") out.push("clickjackable");
  return out;
}''', r'''function auditHeaders(headers) {
  return [];
}'''],
        ["i2-csp-parse", r'''function cspAllows(policy, kind) {
  if (!policy) return false;
  const dirs = {};
  for (const part of policy.split(";")) {
    const [name, ...srcs] = part.trim().split(/\s+/);
    if (name) dirs[name] = srcs;
  }
  const specific = kind === "img" ? "img-src" : "script-src";
  const srcs = dirs[specific] ?? dirs["default-src"];
  if (!srcs) return false;
  return srcs.includes("'self'") || srcs.includes("data:");
}''', r'''function cspAllows(policy, kind) {
  return policy.includes("'self'");
}'''],
        ["i2-cors-decide", r'''function corsDecision(origin, allowedOrigins, credentials) {
  const wildcard = allowedOrigins.includes("*");
  const known = wildcard || allowedOrigins.includes(origin);
  if (!known) return "deny";
  if (wildcard && credentials) return "deny";
  return credentials ? "allow-with-credentials" : "allow";
}''', r'''function corsDecision(origin, allowedOrigins, credentials) {
  return "allow";
}'''],
    ],
)

# ── audit-practice ──────────────────────────────────────────────────────────
write_practice(
    MOD, "audit-practice",
    "Secure the App — Practice",
    "The module capstone: audit a toy app's configuration end to end — secrets, endpoints, headers — and produce a prioritized findings list.",
    "Bảo vệ ứng dụng — Luyện tập",
    "Capstone của module: kiểm toán cấu hình một ứng dụng đồ chơi từ đầu đến cuối — secrets, endpoint, header — và lập danh sách phát hiện theo thứ tự ưu tiên.",
    "cors-csrf-headers", 25, "intermediate",
    [
        {
            "id": "i2-secret-audit",
            "title": "Configuration Audit",
            "prompt": 'Write `auditConfig(config)` — config is an object like { dbUrl, apiKey, sessionSecret, nodeEnv, gitignoredEnv: bool, hardcoded: [names] }. Findings (in order): any of dbUrl/apiKey/sessionSecret present AND gitignoredEnv false => "secrets-in-repo"; hardcoded.length > 0 => "hardcoded-credentials"; nodeEnv === "development" => "dev-config-in-prod" (only when checking production config); else "clean".',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function auditConfig(config) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "secrets in the repo is the first finding",
                    "code": fn_wrap("auditConfig", "auditConfig") + r'''
const c = { dbUrl: "postgres://...", apiKey: "sk-123", sessionSecret: "abc", nodeEnv: "production", gitignoredEnv: false, hardcoded: [] };
if (auditConfig(c) !== "secrets-in-repo") throw new Error("Env not gitignored with secrets present.");
if (auditConfig({ ...c, gitignoredEnv: true }) !== "clean") throw new Error("Properly ignored => clean.");
''',
                    "hint": "The combination condition first.",
                },
                {
                    "name": "hardcoded credentials flagged",
                    "code": fn_wrap("auditConfig", "auditConfig") + r'''
const c = { dbUrl: null, apiKey: null, sessionSecret: null, nodeEnv: "production", gitignoredEnv: true, hardcoded: ["apiKey"] };
if (auditConfig(c) !== "hardcoded-credentials") throw new Error("A hardcoded secret name is a finding.");
''',
                    "hint": "Length check on the hardcoded list.",
                },
            ],
        },
        {
            "id": "i2-endpoint-audit",
            "title": "Endpoint Audit",
            "prompt": 'Write `auditEndpoints(routes)` — routes is an array of { path, method, authRequired, rateLimited, validatesInput }. A route is CRITICAL when: authRequired false AND method !== "GET"; or rateLimited false AND path includes "login|register|reset". A route is a WARNING when it validatesInput false. Return { critical: n, warnings: n }. State-changing unauthenticated routes are the classic breach vector.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function auditEndpoints(routes) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "counts critical and warning routes",
                    "code": fn_wrap("auditEndpoints", "auditEndpoints") + r'''
const routes = [
  { path: "/api/admin/delete", method: "POST", authRequired: false, rateLimited: true, validatesInput: true },
  { path: "/login", method: "POST", authRequired: true, rateLimited: false, validatesInput: true },
  { path: "/api/notes", method: "POST", authRequired: true, rateLimited: true, validatesInput: false },
];
const out = auditEndpoints(routes);
if (out.critical !== 2) throw new Error("Unguarded POST + rate-limited login.");
if (out.warnings !== 1) throw new Error("One route skips validation.");
''',
                    "hint": "Two independent critical conditions, one warning condition.",
                },
                {
                    "name": "clean routes score zero",
                    "code": fn_wrap("auditEndpoints", "auditEndpoints") + r'''
const out = auditEndpoints([
  { path: "/api/notes", method: "GET", authRequired: true, rateLimited: true, validatesInput: true },
]);
if (out.critical !== 0 || out.warnings !== 0) throw new Error("All green stays green.");
''',
                    "hint": "Defaults matter — count nothing when nothing triggers.",
                },
            ],
        },
        {
            "id": "i2-findings-report",
            "title": "Findings Prioritizer",
            "prompt": 'Write `prioritize(findings)` — findings is an array of { id, severity } where severity is "critical" | "high" | "medium" | "low". Return the ids sorted by severity (critical first), stable within the same severity (preserve input order). Include `summary(findings)` returning counts per severity as { critical, high, medium, low } (zeros included).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function prioritize(findings) {\n  // your code\n}\n\nfunction summary(findings) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "sorts by severity, stable within",
                    "code": fn_wrap("prioritize, summary", "prioritize, summary") + r'''
const fs = [
  { id: "a", severity: "low" },
  { id: "b", severity: "critical" },
  { id: "c", severity: "high" },
  { id: "d", severity: "critical" },
];
if (prioritize(fs).join(",") !== "b,d,c,a") throw new Error("critical (b,d in order), high, low.");
''',
                    "hint": "Map severity to a rank, stable-sort by it.",
                },
                {
                    "name": "summary counts all buckets",
                    "code": fn_wrap("prioritize, summary", "prioritize, summary") + r'''
const fs = [{ id: "a", severity: "critical" }, { id: "b", severity: "low" }];
const s = summary(fs);
if (s.critical !== 1 || s.high !== 0 || s.medium !== 0 || s.low !== 1) throw new Error("Zeros included.");
''',
                    "hint": "Four fixed keys, default 0.",
                },
            ],
        },
    ],
    {
        "i2-secret-audit": {
            "title": "Kiểm toán cấu hình",
            "prompt": 'Viết `auditConfig(config)` — config là object như { dbUrl, apiKey, sessionSecret, nodeEnv, gitignoredEnv: bool, hardcoded: [names] }. Các phát hiện (theo thứ tự): có bất kỳ dbUrl/apiKey/sessionSecret VÀ gitignoredEnv false => "secrets-in-repo"; hardcoded.length > 0 => "hardcoded-credentials"; nodeEnv === "development" => "dev-config-in-prod" (chỉ khi kiểm tra cấu hình production); còn lại "clean".',
            "tests": [
                {"name": "secrets trong repo là phát hiện đầu tiên", "hint": "Điều kiện kết hợp đứng trước."},
                {"name": "credential hardcode bị gắn cờ", "hint": "Kiểm tra độ dài danh sách hardcoded."},
            ],
        },
        "i2-endpoint-audit": {
            "title": "Kiểm toán endpoint",
            "prompt": 'Viết `auditEndpoints(routes)` — routes là mảng { path, method, authRequired, rateLimited, validatesInput }. Một route là NGHIÊM TRỌNG khi: authRequired false VÀ method !== "GET"; hoặc rateLimited false VÀ path chứa "login|register|reset". Một route là CẢNH BÁO khi validatesInput false. Trả về { critical: n, warnings: n }. Route đổi trạng thái không xác thực là vector xâm nhập kinh điển.',
            "tests": [
                {"name": "đếm route nghiêm trọng và cảnh báo", "hint": "Hai điều kiện nghiêm trọng độc lập, một điều kiện cảnh báo."},
                {"name": "route sạch cho điểm 0", "hint": "Giá trị mặc định quan trọng — không đếm gì khi không gì kích hoạt."},
            ],
        },
        "i2-findings-report": {
            "title": "Bộ xếp hạng phát hiện",
            "prompt": 'Viết `prioritize(findings)` — findings là mảng { id, severity } với severity là "critical" | "high" | "medium" | "low". Trả về các id sắp theo mức nghiêm trọng (critical trước), ổn định trong cùng mức (giữ thứ tự input). Kèm `summary(findings)` trả về số lượng theo mức dạng { critical, high, medium, low } (bao gồm số 0).',
            "tests": [
                {"name": "sắp theo mức nghiêm trọng, ổn định trong mức", "hint": "Map severity sang hạng, stable-sort theo hạng."},
                {"name": "summary đếm đủ các nhóm", "hint": "Bốn key cố định, mặc định 0."},
            ],
        },
    },
    [
        ["i2-secret-audit", r'''function auditConfig(config) {
  const hasSecrets = Boolean(config.dbUrl || config.apiKey || config.sessionSecret);
  if (hasSecrets && !config.gitignoredEnv) return "secrets-in-repo";
  if (config.hardcoded.length > 0) return "hardcoded-credentials";
  if (config.nodeEnv === "development") return "dev-config-in-prod";
  return "clean";
}''', r'''function auditConfig(config) {
  return "clean";
}'''],
        ["i2-endpoint-audit", r'''function auditEndpoints(routes) {
  let critical = 0, warnings = 0;
  for (const r of routes) {
    const unguardedWrite = !r.authRequired && r.method !== "GET";
    const noRateOnAuth = !r.rateLimited && /login|register|reset/.test(r.path);
    if (unguardedWrite || noRateOnAuth) critical++;
    else if (!r.validatesInput) warnings++;
  }
  return { critical, warnings };
}''', r'''function auditEndpoints(routes) {
  return { critical: 0, warnings: 0 };
}'''],
        ["i2-findings-report", r'''const RANK = { critical: 0, high: 1, medium: 2, low: 3 };
function prioritize(findings) {
  return findings
    .map((f, i) => ({ ...f, i }))
    .sort((a, b) => RANK[a.severity] - RANK[b.severity] || a.i - b.i)
    .map((f) => f.id);
}
function summary(findings) {
  const out = { critical: 0, high: 0, medium: 0, low: 0 };
  for (const f of findings) out[f.severity]++;
  return out;
}''', r'''function prioritize(findings) {
  return findings.map((f) => f.id);
}
function summary(findings) {
  return { critical: 0, high: 0, medium: 0, low: 0 };
}'''],
    ],
)

print("Module 9 practices written.")
