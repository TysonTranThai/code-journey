#!/usr/bin/env python3
"""Module 12: security-engineering — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pypa import write_module, write_lesson, write_practice, challenge, vi_challenge, write_checkpoint

MOD = "security-engineering"

# ── lesson 1 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "threat-modeling",
    "Threat Modeling Before Defense",
    "You cannot defend what you have not enumerated: assets, trust boundaries, attackers, and the moves that actually pay off.",
    28,
    """
Security done well starts on a whiteboard, not in a scanner. The four questions
of threat modeling:

1. **What are we building?** A data-flow diagram: users → API → database, and
   the *trust boundaries* between them (browser↔server, service↔service,
   admin↔public). Every boundary is where attacks live.
2. **What can go wrong?** Walk each boundary with a checklist — STRIDE is the
   classic: **S**poofing (pretend to be someone), **T**ampering (modify data in
   transit/at rest), **R**epudiation (deny actions), **I**nformation disclosure
   (leak data), **D**enial of service (exhaust resources), **E**levation of
   privilege (become admin).
3. **What will we do about it?** Every threat gets one of four fates:
   *mitigate* (fix it), *transfer* (push to a provider), *avoid* (drop the
   feature), *accept* (document why it's tolerable).
4. **Did we do a good job?** Tests for each mitigation, and a process to
   re-model when the design changes.

## Risk ranking: fix the cheap, catastrophic, and likely first

Impact × likelihood decides priority. The boring truth of web security: the
biggest wins are hygiene — no secrets in code, no unvalidated redirects,
parameterized queries, real authorization checks on every object, secure
defaults. The OWASP Top 10 exists because the same handful of mistakes causes
most breaches.

## Trust nothing across a boundary

Inside your process, you may assume your own invariants. Across a boundary, the
data is *attacker-controlled* until proven otherwise: every HTTP header, query
parameter, cookie, file, and third-party API response. The defense is not
filtering — it's the boundary discipline from the APIs module: **parse once at
the edge, treat the parsed value as the only input.**

## Least privilege as a design stance

Every component runs with the minimum authority it needs: a job worker that
only reads the orders table should have credentials that only read the orders
table. When something is compromised — and eventually something is — least
privilege decides whether it's an incident or a catastrophe.
""",
    "Mô hình hóa mối đe dọa trước khi phòng thủ",
    "Bạn không thể phòng thủ thứ chưa liệt kê: tài sản, ranh giới tin cậy, kẻ tấn công, và những nước đi thực sự đáng tiền.",
    """
Bảo mật làm đúng bắt đầu trên bảng trắng, không phải trong một máy quét. Bốn
câu hỏi của threat modeling:

1. **Chúng ta đang xây gì?** Một sơ đồ luồng dữ liệu: user → API → database,
   và các *ranh giới tin cậy* giữa chúng (browser↔server, service↔service,
   admin↔công khai). Mọi ranh giới là nơi các cuộc tấn công sống.
2. **Chuyện gì có thể sai?** Đi qua từng ranh giới với một checklist — STRIDE
   là bản kinh điển: **S**poofing (giả làm ai đó), **T**ampering (sửa dữ liệu
   trên đường truyền/khi lưu), **R**epudiation (chối bỏ hành động),
   **I**nformation disclosure (rò rỉ dữ liệu), **D**enial of service (kiệt quệ
   tài nguyên), **E**levation of privilege (trở thành admin).
3. **Chúng ta sẽ làm gì với nó?** Mỗi mối đe dọa nhận một trong bốn số phận:
   *mitigate* (sửa), *transfer* (đẩy cho nhà cung cấp), *avoid* (bỏ tính năng),
   *accept* (ghi tài liệu vì sao chấp nhận được).
4. **Chúng ta làm tốt không?** Test cho từng biện pháp phòng thủ, và một quy
   trình mô hình hóa lại khi thiết kế thay đổi.

## Xếp hạng rủi ro: sửa thứ rẻ, thảm khốc, và dễ xảy ra trước

Tác động × khả năng xảy ra quyết định thứ tự ưu tiên. Sự thật nhàm chán của
bảo mật web: những thắng lợi lớn nhất là vệ sinh cơ bản — không có secrets
trong code, không redirect không kiểm chứng, query tham số hóa, kiểm tra ủy
quyền thật trên từng đối tượng, mặc định an toàn. OWASP Top 10 tồn tại vì cùng
một nắm nhỏ lỗi gây ra phần lớn các vụ vi phạm dữ liệu.

## Không tin gì qua một ranh giới

Bên trong tiến trình của bạn, bạn có thể giả định các bất biến của mình. Qua
một ranh giới, dữ liệu là *do kẻ tấn công kiểm soát* cho đến khi chứng minh
ngược lại: mọi HTTP header, query parameter, cookie, tệp, và response của API
bên thứ ba. Phòng thủ không phải là lọc — mà là kỷ luật ranh giới từ module
API: **parse một lần tại mép vào, coi giá trị đã parse là đầu vào duy nhất.**

## Least privilege như một tư thế thiết kế

Mọi thành phần chạy với quyền tối thiểu mà nó cần: một job worker chỉ đọc bảng
orders thì phải có credentials chỉ đọc bảng orders. Khi một thứ bị xâm phạm —
và cuối cùng thì cũng có thứ bị — least privilege quyết định đó là một sự cố
hay một thảm họa.
""",
)

# ── lesson 2 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "injection-and-encoding",
    "Injection, Encoding, and Dangerous Functions",
    "The family tree of injection bugs — SQL, command, path, deserialization — and the single habit that kills most of them.",
    32,
    """
Injection is one bug with many costumes: **data crosses a boundary and gets
interpreted as code.** The costumes matter because the parsers differ.

## SQL injection → parameterize

```python
# WRONG: string-built query
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# name = "'; DROP TABLE users; --"  → your table is gone

# RIGHT: parameters
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

Parameterized queries send the *value* separately from the *statement*, so a
value can never change the statement's meaning. There is no input you cannot
safely pass this way — which is why "escape the quotes by hand" is never the
answer.

## Command injection → don't shell out

`os.system(f"convert {filename}.png")` with `filename = "a; rm -rf /; echo"`
executes arbitrary commands. The hierarchy of fixes: **don't invoke a shell**
(use library APIs, or `subprocess.run([...list form...], shell=False)`); if you
must shell, whitelist-validate the argument against an exact pattern; and never
pass user data near a shell.

## Path traversal → resolve and confine

`open(base_dir + "/" + filename)` with `filename = "../../etc/passwd"` leaves
the directory. Confine: resolve the joined path and verify it is still inside
the base (`path.resolve().is_relative_to(base.resolve())`), then open. Reject
or normalize `..` — and remember URLs are not paths.

## Unsafe deserialization → never unpickle foreign bytes

`pickle.loads(untrusted)` executes embedded code — it is arbitrary-code
execution as a library feature. For data crossing a boundary use JSON (values
only, no code), and treat any binary deserializer as remote code execution
waiting to happen.

## XSS and output encoding

XSS is injection into the *browser's* parser: your data lands in HTML and
executes as script. Defense is **context-aware output encoding** (escape for
HTML body, attribute, JS, URL as appropriate) plus frameworks that escape by
default — and a **Content-Security-Policy** header as a second wall. And the
cookie that proves your identity should never be readable by JavaScript:
`HttpOnly; Secure; SameSite=Lax`.

## Authorization: the bug scanners can't find

Broken access control sits at #1 in the OWASP Top 10 precisely because it's a
*design* failure: `/api/orders/42` works for everyone because the handler never
asked *is 42 yours?*. The rule is boring and absolute: **every object access
carries an ownership/role check derived from the session, never from a
parameter.** IDOR (Insecure Direct Object Reference) is the name of forgetting.
""",
    "Injection, encoding, và các hàm nguy hiểm",
    "Cây phả hệ của các lỗi injection — SQL, command, path, deserialization — và một thói quen duy nhất tiêu diệt phần lớn chúng.",
    """
Injection là một lỗi duy nhất với nhiều trang phục: **dữ liệu đi qua một ranh
giới và bị diễn giải thành code.** Các trang phục quan trọng vì mỗi parser
khác nhau.

## SQL injection → tham số hóa

```python
# SAI: query dựng bằng chuỗi
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# name = "'; DROP TABLE users; --"  → bảng của bạn biến mất

# ĐÚNG: tham số
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

Query tham số hóa gửi *giá trị* tách khỏi *câu lệnh*, nên một giá trị không bao
giờ đổi được ý nghĩa của câu lệnh. Không có đầu vào nào mà bạn không thể truyền
an toàn theo cách này — vì vậy "tự escape dấu nháy" không bao giờ là câu trả
lời.

## Command injection → đừng gọi shell

`os.system(f"convert {filename}.png")` với `filename = "a; rm -rf /; echo"`
thực thi lệnh tùy ý. Thứ tự ưu tiên của các cách sửa: **không gọi shell** (dùng
API thư viện, hoặc `subprocess.run([...dạng list...], shell=False)`); nếu bắt
buộc phải shell, whitelist-validate tham số theo một pattern chính xác; và
không bao giờ đưa dữ liệu người dùng gần một shell.

## Path traversal → resolve và giới hạn

`open(base_dir + "/" + filename)` với `filename = "../../etc/passwd"` rời khỏi
thư mục. Giới hạn: resolve đường dẫn đã nối và xác minh nó vẫn nằm trong base
(`path.resolve().is_relative_to(base.resolve())`), rồi mở. Từ chối hoặc chuẩn
hóa `..` — và nhớ rằng URL không phải đường dẫn.

## Deserialization nguy hiểm → không bao giờ unpickle byte lạ

`pickle.loads(untrusted)` thực thi code nhúng — đó là thực thi mã tùy ý dưới
dạng một tính năng thư viện. Với dữ liệu qua ranh giới, dùng JSON (chỉ giá trị,
không code), và coi mọi binary deserializer là RCE chờ ngày nổ.

## XSS và output encoding

XSS là injection vào *parser của trình duyệt*: dữ liệu của bạn đáp xuống HTML
và chạy như script. Phòng thủ là **output encoding theo ngữ cảnh** (escape cho
HTML body, attribute, JS, URL đúng chỗ) cộng với các framework mặc định đã
escape — và header **Content-Security-Policy** như bức tường thứ hai. Và cookie
chứng minh danh tính của bạn không bao giờ được JavaScript đọc được:
`HttpOnly; Secure; SameSite=Lax`.

## Authorization: lỗi mà máy quét không tìm ra

Broken access control đứng #1 trong OWASP Top 10 chính vì đó là lỗi *thiết kế*:
`/api/orders/42` hoạt động với mọi người vì handler chưa từng hỏi *42 có phải
của bạn không?*. Quy tắc nhàm chán và tuyệt đối: **mọi truy cập đối tượng mang
một kiểm tra sở hữu/vai trò suy ra từ session, không bao giờ từ một tham số.**
IDOR (Insecure Direct Object Reference) là tên của việc quên điều đó.
""",
)

# ── lesson 3 ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "auth-secrets-hardening",
    "Auth, Secrets, and Hardening",
    "Password hashing done right, session hygiene, secret management, and the security headers that cost nothing.",
    30,
    """
## Passwords: hashing is not encryption

You must never be able to read a password back. Store `hash(password + salt)`
with a *slow, memory-hard* function — bcrypt, scrypt, or Argon2. Slow is the
point: an offline attacker with your database makes billions of guesses;
each guess must cost real time. (`hashlib.sha256` is *fast* — that's why it's
wrong here.) Salts kill rainbow tables; work factors make brute force
uneconomical; rate limiting on the login endpoint caps online guessing.

## Sessions and cookies

After login, the server issues a random session ID (≥128 bits of entropy) kept
in a cookie. Hardening flags:

- `HttpOnly` — JavaScript cannot read it (XSS can't steal it),
- `Secure` — it never travels over plain HTTP,
- `SameSite=Lax` — cross-site requests don't carry it (kills most CSRF),
- expiring and rotating IDs on privilege changes.

CSRF, the leftover case: an attacker's page makes the *victim's browser* send
an authenticated request. SameSite blocks most; a **synchronizer token** (a
random value in the form that must match the session) blocks the rest.

## Secrets: config, not code

A secret in source control is compromised forever (history survives deletion).
The discipline: secrets live in environment variables or a secrets manager,
loaded at startup, validated with the same parse-don't-validate discipline as
any boundary input (`SECRET_KEY` missing → refuse to boot, don't default).
Different environments get different secrets; logs and error reports are
scrubbed of them; dependencies are pinned and audited (`pip audit`) because
your supply chain is also an attack surface.

## Security headers: the cheapest fixes in the file

| Header | Effect |
|---|---|
| `Content-Security-Policy` | blocks script from unapproved origins |
| `X-Content-Type-Options: nosniff` | browser won't reinterpret responses |
| `Strict-Transport-Security` | forces HTTPS for future visits |
| `X-Frame-Options: DENY` | blocks clickjacking via framing |

## Verification closes the loop

A fix without a test is a hope. Every security change ships with a test that
*proves* the attack fails now: the traversal path is rejected, the injection
string is stored as a literal, the wrong owner gets 403/404. That's the
checkpoint below.
""",
    "Auth, secrets, và hardening",
    "Băm mật khẩu đúng cách, vệ sinh session, quản lý secret, và những security header không tốn một xu.",
    """
## Mật khẩu: băm không phải mã hóa

Bạn không bao giờ được đọc lại mật khẩu. Lưu `hash(password + salt)` với một
hàm *chậm, tốn bộ nhớ* — bcrypt, scrypt, hoặc Argon2. Chậm chính là mục đích:
kẻ tấn công offline có database của bạn sẽ đoán hàng tỷ lần; mỗi lần đoán phải
tốn thời gian thật. (`hashlib.sha256` *nhanh* — đó là lý do nó sai ở đây.) Salt
diệt rainbow table; work factor khiến brute force không còn lợi nhuận; rate
limiting trên endpoint đăng nhập chặn đoán trực tuyến.

## Session và cookie

Sau khi đăng nhập, server phát một session ID ngẫu nhiên (≥128 bit entropy)
giữ trong một cookie. Các cờ hardening:

- `HttpOnly` — JavaScript không đọc được (XSS không ăn cắp được),
- `Secure` — không bao giờ đi trên HTTP thuần,
- `SameSite=Lax` — request chéo trang không mang nó (diệt phần lớn CSRF),
- hết hạn và xoay ID khi quyền hạn thay đổi.

CSRF, trường hợp còn lại: trang của kẻ tấn công khiến *trình duyệt của nạn
nhân* gửi một request đã xác thực. SameSite chặn phần lớn; **synchronizer
token** (một giá trị ngẫu nhiên trong form phải khớp với session) chặn phần
còn lại.

## Secrets: cấu hình, không phải code

Một secret trong source control bị xâm phạm mãi mãi (lịch sử sống sót qua việc
xóa). Kỷ luật: secrets nằm trong biến môi trường hoặc secrets manager, nạp lúc
khởi động, được validate với cùng kỷ luật parse-don't-validate như mọi đầu vào
ranh giới (`SECRET_KEY` thiếu → từ chối khởi động, đừng dùng default). Môi
trường khác nhau nhận secrets khác nhau; log và báo cáo lỗi được rửa sạch
chúng; dependencies được pin và audit (`pip audit`) vì chuỗi cung ứng của bạn
cũng là một mặt trận tấn công.

## Security header: những bản vá rẻ nhất trong tệp

| Header | Tác dụng |
|---|---|
| `Content-Security-Policy` | chặn script từ các nguồn chưa duyệt |
| `X-Content-Type-Options: nosniff` | trình duyệt không diễn giải lại response |
| `Strict-Transport-Security` | ép HTTPS cho các lần truy cập sau |
| `X-Frame-Options: DENY` | chặn clickjacking qua framing |

## Kiểm chứng khép vòng

Một bản vá không có test là một lời hy vọng. Mọi thay đổi bảo mật đi kèm một
bài test *chứng minh* cuộc tấn công giờ thất bại: đường dẫn traversal bị từ
chối, chuỗi injection được lưu như chữ thường, owner sai nhận 403/404. Đó
chính là checkpoint bên dưới.
""",
)

# ── practice 1: injection ────────────────────────────────────────────────────
SQLSAFE_REF = (
    "import re as _re\n"
    "\n"
    "\n"
    "class UnsafeQuery(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "def build_query(template, params):\n"
    "    '''Simulate parameterization. template may contain ? placeholders; params\n"
    "    are values. Returns (final_query, safety) where safety is 'parameterized'.\n"
    "    A template containing ' OR ' / '; ' / '--' literal SQL in a NON-placeholder\n"
    "    position is fine (it's the developer's SQL); values NEVER change the\n"
    "    statement, so any quote in a value is stored literally. Raises\n"
    "    UnsafeQuery when the template itself has a placeholder count mismatch.'''\n"
    "    count = template.count('?')\n"
    "    if count != len(params):\n"
    "        raise UnsafeQuery('placeholder count mismatch')\n"
    "    parts = template.split('?')\n"
    "    rendered = parts[0]\n"
    "    for i, value in enumerate(params):\n"
    "        rendered += repr(value) + parts[i + 1]\n"
    "    return rendered, 'parameterized'\n"
    "\n"
    "\n"
    "def vulnerable_query(template, values):\n"
    "    '''The WRONG world: values are formatted straight into the SQL string.\n"
    "    Detects the classic payloads and raises UnsafeQuery (i.e., flags that this\n"
    "    build path is unsafe for them).'''\n"
    "    rendered = template.format(*values)\n"
    "    lowered = rendered.lower()\n"
    "    if \"drop table\" in lowered or \"' or '1'='1\" in lowered or \";\" in lowered:\n"
    "        raise UnsafeQuery('injection detected in string-built query')\n"
    "    return rendered\n"
)
SQLSAFE_WRONG = (
    "import re as _re\n"
    "\n"
    "\n"
    "class UnsafeQuery(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "def build_query(template, params):\n"
    "    count = template.count('?')\n"
    "    if count != len(params):\n"
    "        raise UnsafeQuery('placeholder count mismatch')\n"
    "    # WRONG: hand-rolled escaping instead of parameterization —\n"
    "    # strips quotes from values, corrupting legitimate data\n"
    "    parts = template.split('?')\n"
    "    rendered = parts[0]\n"
    "    for i, value in enumerate(params):\n"
    "        rendered += str(value).replace(\"'\", \"\") + parts[i + 1]\n"
    "    return rendered, 'parameterized'\n"
    "\n"
    "\n"
    "def vulnerable_query(template, values):\n"
    "    rendered = template.format(*values)\n"
    "    lowered = rendered.lower()\n"
    "    if \"drop table\" in lowered or \"' or '1'='1\" in lowered or \";\" in lowered:\n"
    "        raise UnsafeQuery('injection detected in string-built query')\n"
    "    return rendered\n"
)

TRAVERSAL_REF = (
    "from pathlib import PurePosixPath\n"
    "\n"
    "\n"
    "def resolve_upload(base, name):\n"
    "    '''Return the resolved path inside `base` for a user-supplied file name,\n"
    "    or raise ValueError('traversal') if it escapes base. Absolute paths and\n"
    "    any '..' component are rejected; symlinks are not simulated.'''\n"
    "    if not name or name.startswith('/') or '\\\\x00' in name:\n"
    "        raise ValueError('traversal')\n"
    "    p = PurePosixPath(name)\n"
    "    if p.is_absolute() or '..' in p.parts:\n"
    "        raise ValueError('traversal')\n"
    "    resolved = PurePosixPath(base) / p\n"
    "    if not str(resolved).startswith(str(PurePosixPath(base)).rstrip('/') + '/'):\n"
    "        raise ValueError('traversal')\n"
    "    return str(resolved)\n"
)
TRAVERSAL_REF = TRAVERSAL_REF.replace("'\\\\x00' in name", "'\\x00' in name")
TRAVERSAL_WRONG = (
    "from pathlib import PurePosixPath\n"
    "\n"
    "\n"
    "def resolve_upload(base, name):\n"
    "    # WRONG: naive string join — trusts the caller completely\n"
    "    return base + '/' + name\n"
)

write_practice(
    MOD, "pa-p12-injection-practice",
    "Injection Drills",
    "Parameterization as a contract, and path confinement that actually confines.",
    "Bài tập injection",
    "Tham số hóa như một hợp đồng, và giới hạn đường dẫn thực sự giới hạn.",
    "injection-and-encoding", 24, "advanced",
    [
        challenge(
            "pa-sec-parameterize",
            "Parameterization beats escaping",
            "Implement two functions that contrast safe and unsafe query building:\n\n- `build_query(template, params)` — the parameterized world. The template may contain `?` placeholders; values are rendered with `repr()` (a quote in a value stays a literal quote inside a quoted token, never changing statement structure). Placeholder-count mismatch raises `UnsafeQuery('placeholder count mismatch')`. Returns `(rendered, 'parameterized')`.\n- `vulnerable_query(template, values)` — the string-formatting world. Render with `template.format(*values)`; if the result contains `drop table` (case-insensitive), `' or '1'='1`, or a `;`, raise `UnsafeQuery('injection detected in string-built query')`; otherwise return it.\n- define `class UnsafeQuery(Exception)`.\n\nThe discriminating scenario: `O'Brien` as a customer name must flow safely through `build_query` unchanged (quotes preserved) — while the same string in the vulnerable path is a hand-escaping hazard.",
            "# TODO: UnsafeQuery + build_query + vulnerable_query",
            [
                ("legit data survives parameterization intact",
                 "q, safety = build_query(\"SELECT * FROM users WHERE name = ?\", [\"O'Brien\"])\nassert safety == 'parameterized'\nassert \"O'Brien\" in q and q.count(\"'\") == 4\ntry:\n    build_query(\"SELECT ?\", [1, 2])\nexcept UnsafeQuery:\n    pass\nelse:\n    raise AssertionError('count mismatch must raise')\nprint('ok')",
                 "repr() keeps the value literal; structure never changes."),
                ("the vulnerable path is caught red-handed",
                 "try:\n    vulnerable_query(\"SELECT * FROM t WHERE a = '{}'\", [\"x'; DROP TABLE t; --\"])\nexcept UnsafeQuery:\n    pass\nelse:\n    raise AssertionError('must flag the payload')\nassert vulnerable_query(\"SELECT * FROM t WHERE a = '{}'\", ['bob']) == \"SELECT * FROM t WHERE a = 'bob'\"\nprint('ok')",
                 "String-formatting + payloads = flagged; plain values pass through."),
            ],
            level="debugging",
        ),
        challenge(
            "pa-sec-path-traversal",
            "Confine the upload path",
            "Implement `resolve_upload(base, name)` returning the joined, normalized path for a user-supplied file name — or raising `ValueError('traversal')` when the name:\n\n- is empty, absolute (`/etc/passwd`), or contains a NUL character\n- contains any `..` component (`../../etc/passwd`)\n- would resolve outside `base` after joining\n\nValid names (`'report.pdf'`, `'sub/dir/img.png'`) resolve to `base/name` strings.",
            "from pathlib import PurePosixPath\n\n\ndef resolve_upload(base, name):\n    ...",
            [
                ("legitimate names resolve inside base",
                 "assert resolve_upload('/srv/uploads', 'report.pdf') == '/srv/uploads/report.pdf'\nassert resolve_upload('/srv/uploads', 'sub/dir/img.png') == '/srv/uploads/sub/dir/img.png'\nprint('ok')",
                 "Subdirectories are fine — escaping the root is not."),
                ("every traversal shape is rejected",
                 "for bad in ['', '/etc/passwd', '../../etc/passwd', 'docs/../../x', 'a\\x00b']:\n    try:\n        resolve_upload('/srv/uploads', bad)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(f'must reject {bad!r}')\nprint('ok')",
                 "Empty, absolute, `..`, sneaky prefix, and NUL all fail closed."),
            ],
            level="debugging",
        ),
    ],
    {
        "pa-sec-parameterize": vi_challenge(
            "Tham số hóa đánh bại escaping thủ công",
            "Cài hai hàm tương phản cách dựng query an toàn và không an toàn:\n\n- `build_query(template, params)` — thế giới tham số hóa. Template có thể chứa placeholder `?`; giá trị được render bằng `repr()` (dấu nháy trong giá trị giữ nguyên như literal bên trong token trích dẫn, không bao giờ đổi cấu trúc câu lệnh). Lệch số placeholder raise `UnsafeQuery('placeholder count mismatch')`. Trả `(rendered, 'parameterized')`.\n- `vulnerable_query(template, values)` — thế giới định dạng chuỗi. Render bằng `template.format(*values)`; nếu kết quả chứa `drop table` (không phân biệt hoa thường), `' or '1'='1`, hoặc `;`, raise `UnsafeQuery('injection detected in string-built query')`; ngược lại trả nó.\n- định nghĩa `class UnsafeQuery(Exception)`.\n\nKịch bản phân biệt: tên khách hàng `O'Brien` phải trôi qua `build_query` an toàn, nguyên vẹn (giữ dấu nháy) — trong khi cùng chuỗi đó trên đường không an toàn là mối nguy escape thủ công.",
            [("Dữ liệu hợp lệ sống sót nguyên vẹn qua tham số hóa", "repr() giữ giá trị là literal; cấu trúc không bao giờ đổi."),
             ("Đường không an toàn bị tóm tại hiện trường", "Định dạng chuỗi + payload = bị gắn cờ; giá trị bình thường đi qua.")],
        ),
        "pa-sec-path-traversal": vi_challenge(
            "Giới hạn đường dẫn upload",
            "Cài `resolve_upload(base, name)` trả đường dẫn đã nối, đã chuẩn hóa cho một tên tệp do người dùng cung cấp — hoặc raise `ValueError('traversal')` khi tên:\n\n- rỗng, tuyệt đối (`/etc/passwd`), hoặc chứa ký tự NUL\n- chứa bất kỳ thành phần `..` nào (`../../etc/passwd`)\n- sau khi nối sẽ resolve ra ngoài `base`\n\nTên hợp lệ (`'report.pdf'`, `'sub/dir/img.png'`) resolve thành chuỗi `base/name`.",
            [("Tên hợp lệ resolve bên trong base", "Thư mục con thì được — thoát khỏi gốc thì không."),
             ("Mọi hình dạng traversal đều bị từ chối", "Rỗng, tuyệt đối, `..`, tiền tố sneak, và NUL đều fail closed.")],
        ),
    },
    solutions=[("pa-sec-parameterize", SQLSAFE_REF, SQLSAFE_WRONG),
               ("pa-sec-path-traversal", TRAVERSAL_REF, TRAVERSAL_WRONG)],
)


# ── password policy solutions (used by the auth practice) ────────────────────
PWD_REF = (
    "BREACHED = {\"password123456\", \"correcthorsebattery\", \"letmein123456\"}\n"
    "\n"
    "\n"
    "def check_password(pw):\n"
    "    if not isinstance(pw, str):\n"
    "        return False, ['must be a string']\n"
    "    problems = []\n"
    "    if len(pw) < 12:\n"
    "        problems.append('must be at least 12 characters')\n"
    "    if not any(c.isupper() for c in pw):\n"
    "        problems.append('must contain an uppercase letter')\n"
    "    if not any(c.islower() for c in pw):\n"
    "        problems.append('must contain a lowercase letter')\n"
    "    if not any(c.isdigit() for c in pw):\n"
    "        problems.append('must contain a digit')\n"
    "    if any(c.isspace() for c in pw):\n"
    "        problems.append('must not contain whitespace')\n"
    "    if pw.lower() in BREACHED:\n"
    "        problems.append('must not be a known breached password')\n"
    "    return (not problems), problems\n"
)
PWD_WRONG = (
    "BREACHED = {\"password123456\", \"correcthorsebattery\", \"letmein123456\"}\n"
    "\n"
    "\n"
    "def check_password(pw):\n"
    "    # WRONG: returns at the first problem and ignores the breach list\n"
    "    if not isinstance(pw, str):\n"
    "        return False, ['must be a string']\n"
    "    if len(pw) < 12:\n"
    "        return False, ['must be at least 12 characters']\n"
    "    if not any(c.isupper() for c in pw):\n"
    "        return False, ['must contain an uppercase letter']\n"
    "    return True, []\n"
)

# ── practice 2: auth ─────────────────────────────────────────────────────────
AUTHZ_REF = (
    "class Forbidden(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "class NotFound(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "ORDERS = {\n"
    "    'o1': {'owner': 'alice', 'total': 100},\n"
    "    'o2': {'owner': 'bob', 'total': 50},\n"
    "}\n"
    "\n"
    "\n"
    "def get_order(session, order_id, admin=False):\n"
    "    '''Authorization done right: the check derives from the SESSION, never from\n"
    "    a client-supplied parameter. Admins may read anything; owners read their\n"
    "    own; strangers get NotFound (not Forbidden — don't confirm existence).'''\n"
    "    order = ORDERS.get(order_id)\n"
    "    if order is None:\n"
    "        raise NotFound('no such order')\n"
    "    if not admin and order['owner'] != session['user']:\n"
    "        raise NotFound('no such order')   # existence not confirmed\n"
    "    return dict(order)\n"
)
AUTHZ_WRONG = (
    "class Forbidden(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "class NotFound(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "ORDERS = {\n"
    "    'o1': {'owner': 'alice', 'total': 100},\n"
    "    'o2': {'owner': 'bob', 'total': 50},\n"
    "}\n"
    "\n"
    "\n"
    "def get_order(session, order_id, admin=False):\n"
    "    order = ORDERS.get(order_id)\n"
    "    if order is None:\n"
    "        raise NotFound('no such order')\n"
    "    # WRONG: trusts the client's owner_id parameter instead of the session\n"
    "    if not admin and order['owner'] != session.get('as_user', session['user']):\n"
    "        raise Forbidden('not yours')\n"
    "    return dict(order)\n"
)

write_practice(
    MOD, "pa-p12-auth-practice",
    "Authorization & Session Drills",
    "Ownership checks that derive from the session, and password hashing with real entropy rules.",
    "Bài tập ủy quyền và session",
    "Kiểm tra sở hữu suy ra từ session, và băm mật khẩu với các quy tắc entropy thật.",
    "auth-secrets-hardening", 22, "advanced",
    [
        challenge(
            "pa-sec-authz",
            "Own the object check",
            "Implement `get_order(session, order_id, admin=False)` with `NotFound`/`Forbidden` exceptions and the module-level `ORDERS` dict (owners 'alice' and 'bob'):\n\n- unknown id → `NotFound('no such order')`\n- `admin=True` → any order\n- owner (from `session['user']`) → their order\n- everyone else → **`NotFound('no such order')`** — never `Forbidden` and never the data: a 404 doesn't confirm the resource exists (no enumeration oracle)\n- the check must use the session user only; a client-supplied `as_user` key must be IGNORED\n\nThis is IDOR as executable specification.",
            "class Forbidden(Exception):\n    pass\n\n\nclass NotFound(Exception):\n    pass\n\n\nORDERS = {\n    'o1': {'owner': 'alice', 'total': 100},\n    'o2': {'owner': 'bob', 'total': 50},\n}\n\n\ndef get_order(session, order_id, admin=False):\n    ...",
            [
                ("owners read their own, strangers see nothing",
                 "alice = {'user': 'alice'}\nassert get_order(alice, 'o1')['owner'] == 'alice'\ntry:\n    get_order(alice, 'o2')\nexcept NotFound:\n    pass\nelse:\n    raise AssertionError('stranger must get NotFound')\nassert get_order(alice, 'o2', admin=True)['owner'] == 'bob'\nprint('ok')",
                 "Owner yes, stranger 404, admin everything."),
                ("the parameter is not the principal",
                 "alice = {'user': 'alice', 'as_user': 'bob'}\ntry:\n    get_order(alice, 'o2')\nexcept NotFound:\n    pass\nelse:\n    raise AssertionError('as_user must be ignored')\ntry:\n    get_order({'user': 'mallory'}, 'nope')\nexcept NotFound:\n    pass\nelse:\n    raise AssertionError('unknown id is NotFound')\nprint('ok')",
                 "Identity comes from the session; params are data, not authority."),
            ],
            level="debugging",
        ),
        challenge(
            "pa-sec-password-policy",
            "The password checker that fails closed",
            "Implement `check_password(pw)` returning `(ok, problems)` — `ok` True iff ALL rules pass, `problems` a list of human-readable violation strings in this fixed order:\n\n1. `'must be at least 12 characters'` when `len(pw) < 12`\n2. `'must contain an uppercase letter'` when no `A-Z`\n3. `'must contain a lowercase letter'` when no `a-z`\n4. `'must contain a digit'` when no digit\n5. `'must not contain whitespace'` when any whitespace\n6. `'must not be a known breached password'` when lowercased in the fixed set `{\"password123456\", \"correcthorsebattery\", \"letmein123456\"}`\n\nAn empty password fails rules 1-4 (and rule 5 not, rule 6 not). Non-string input → `('must be a string',)`-style handling: return `(False, ['must be a string'])`.",
            "BREACHED = {\"password123456\", \"correcthorsebattery\", \"letmein123456\"}\n\n\ndef check_password(pw):\n    ...",
            [
                ("strong passes, weak fails with the full list",
                 "ok, problems = check_password('Str0ng-Passphrase!')\nassert ok is True and problems == []\nok, problems = check_password('short')\nassert ok is False\nassert problems == ['must be at least 12 characters', 'must contain an uppercase letter', 'must contain a digit']\nprint('ok')",
                 "'short' is too small, lacks uppercase and a digit — reported in order."),
                ("breach list and whitespace, fail closed",
                 "ok, problems = check_password('correcthorsebattery')\nassert ok is False and problems == ['must contain an uppercase letter', 'must contain a digit', 'must not be a known breached password']\nok, problems = check_password('has space inside 12')\nassert ok is False and 'must not contain whitespace' in problems\nok, problems = check_password(None)\nassert ok is False and problems == ['must be a string']\nprint('ok')",
                 "Breached + missing classes all reported; wrong type fails closed."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-sec-authz": vi_challenge(
            "Sở hữu phép kiểm tra đối tượng",
            "Cài `get_order(session, order_id, admin=False)` với các exception `NotFound`/`Forbidden` và dict `ORDERS` ở mức module (owner 'alice' và 'bob'):\n\n- id lạ → `NotFound('no such order')`\n- `admin=True` → mọi order\n- owner (từ `session['user']`) → order của họ\n- mọi người khác → **`NotFound('no such order')`** — không bao giờ `Forbidden` và không bao giờ trả dữ liệu: một 404 không xác nhận tài nguyên tồn tại (không có oracle dò tìm)\n- phép kiểm tra chỉ được dùng session user; key `as_user` do client cung cấp phải bị BỎ QUA\n\nĐây là IDOR dưới dạng đặc tả thực thi được.",
            [("Owner đọc của mình, người lạ không thấy gì", "Owner có, người lạ 404, admin tất cả."),
             ("Tham số không phải chủ thể", "Danh tính đến từ session; params là dữ liệu, không phải quyền hạn.")],
        ),
        "pa-sec-password-policy": vi_challenge(
            "Trình kiểm tra mật khẩu fail closed",
            "Cài `check_password(pw)` trả `(ok, problems)` — `ok` True khi và chỉ khi MỌI quy tắc pass, `problems` là list các chuỗi vi phạm đọc được theo thứ tự cố định sau:\n\n1. `'must be at least 12 characters'` khi `len(pw) < 12`\n2. `'must contain an uppercase letter'` khi không có `A-Z`\n3. `'must contain a lowercase letter'` khi không có `a-z`\n4. `'must contain a digit'` khi không có chữ số\n5. `'must not contain whitespace'` khi có khoảng trắng\n6. `'must not be a known breached password'` khi viết thường nằm trong tập cố định `{\"password123456\", \"correcthorsebattery\", \"letmein123456\"}`\n\nMật khẩu rỗng fail quy tắc 1-4 (không fail 5 và 6). Input không phải chuỗi → trả `(False, ['must be a string'])`.",
            [("Mạnh thì pass, yếu thì fail với danh sách đầy đủ", "'short' quá ngắn, thiếu hoa và chữ số — báo theo đúng thứ tự."),
             ("Danh sách rò rỉ và khoảng trắng, fail closed", "Breach + thiếu loại ký tự đều được báo; sai kiểu fail closed.")],
        ),
    },
    solutions=[("pa-sec-authz", AUTHZ_REF, AUTHZ_WRONG)],
)

# ── practice 3: hardening (full password policy + secrets loader) ────────────
CFG_REF = (
    "class ConfigError(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "def load_config(env, required=('SECRET_KEY', 'DB_URL')):\n"
    "    config = {}\n"
    "    missing = []\n"
    "    for key in required:\n"
    "        value = env.get(key)\n"
    "        if isinstance(value, str) and value.strip():\n"
    "            config[key] = value\n"
    "        else:\n"
    "            missing.append(key)\n"
    "    if missing:\n"
    "        raise ConfigError('missing required config: ' + ', '.join(sorted(missing)))\n"
    "    return config\n"
)
CFG_WRONG = (
    "class ConfigError(Exception):\n"
    "    pass\n"
    "\n"
    "\n"
    "def load_config(env, required=('SECRET_KEY', 'DB_URL')):\n"
    "    # WRONG: defaults to an insecure placeholder instead of refusing to boot\n"
    "    config = {}\n"
    "    for key in required:\n"
    "        value = env.get(key)\n"
    "        if isinstance(value, str) and value.strip():\n"
    "            config[key] = value\n"
    "        else:\n"
    "            config[key] = 'INSECURE-DEFAULT'\n"
    "    return config\n"
)

write_practice(
    MOD, "pa-p12-hardening-practice",
    "Hardening Drills",
    "The full password checker with its ordered diagnostics, and a secrets loader that refuses to boot without configuration.",
    "Bài tập hardening",
    "Trình kiểm tra mật khẩu đầy đủ với chẩn đoán có thứ tự, và một secrets loader từ chối khởi động khi thiếu cấu hình.",
    "auth-secrets-hardening", 20, "advanced",
    [
        challenge(
            "pa-sec-password-full",
            "Collect every password problem",
            "Implement `check_password(pw)` — every rule is checked, every violation is collected, the order is fixed (length, uppercase, lowercase, digit, whitespace, breach list), and non-string input returns `(False, ['must be a string'])` before any other rule runs.",
            "BREACHED = {\"password123456\", \"correcthorsebattery\", \"letmein123456\"}\n\n\ndef check_password(pw):\n    ...",
            [
                ("every problem, in order, every time",
                 "ok, problems = check_password('short')\nassert problems == ['must be at least 12 characters', 'must contain an uppercase letter', 'must contain a digit']\nok, problems = check_password('correcthorsebattery')\nassert problems == ['must contain an uppercase letter', 'must contain a digit', 'must not be a known breached password']\nok, problems = check_password(None)\nassert problems == ['must be a string']\nprint('ok')",
                 "Collect, don't abort; ordering is part of the contract."),
            ],
            level="combination",
        ),
        challenge(
            "pa-sec-secrets-loader",
            "Refuse to boot without secrets",
            "Implement `load_config(env, required=('SECRET_KEY', 'DB_URL'))`:\n\n- returns a dict of every key in `required` that is present AND non-empty (stripped)\n- missing or empty required keys → raise `ConfigError('missing required config: ' + ', '.join(sorted(missing)))`\n- extra keys in `env` are IGNORED (never trusted into the config)\n- define `class ConfigError(Exception)`",
            "class ConfigError(Exception):\n    pass\n\n\ndef load_config(env, required=('SECRET_KEY', 'DB_URL')):\n    ...",
            [
                ("happy path and loud failure",
                 "cfg = load_config({'SECRET_KEY': 'abc', 'DB_URL': 'postgres://x', 'DEBUG': '1'})\nassert cfg == {'SECRET_KEY': 'abc', 'DB_URL': 'postgres://x'}\ntry:\n    load_config({'SECRET_KEY': 'abc', 'DB_URL': '  '})\nexcept ConfigError as e:\n    assert 'DB_URL' in str(e)\nelse:\n    raise AssertionError('empty value must fail')\nprint('ok')",
                 "Whitespace-only is missing; extras are not copied."),
            ],
            level="guided",
        ),
    ],
    {
        "pa-sec-password-full": vi_challenge(
            "Gom mọi vấn đề của mật khẩu",
            "Cài `check_password(pw)` — mọi quy tắc được kiểm, mọi vi phạm được gom, thứ tự cố định (độ dài, hoa, thường, chữ số, khoảng trắng, danh sách rò rỉ), và input không phải chuỗi trả `(False, ['must be a string'])` trước mọi quy tắc khác.",
            [("Mọi vấn đề, đúng thứ tự, mọi lần", "Gom, đừng dừng; thứ tự là một phần của hợp đồng.")],
        ),
        "pa-sec-secrets-loader": vi_challenge(
            "Từ chối khởi động khi thiếu secrets",
            "Cài `load_config(env, required=('SECRET_KEY', 'DB_URL'))`:\n\n- trả dict của mọi key trong `required` hiện diện VÀ không rỗng (đã strip)\n- key bắt buộc thiếu hoặc rỗng → raise `ConfigError('missing required config: ' + ', '.join(sorted(missing)))`\n- key thừa trong `env` bị BỎ QUA (không bao giờ được tin vào config)\n- định nghĩa `class ConfigError(Exception)`",
            [("Happy path và fail ầm ĩ", "Chỉ-whitespace là thiếu; phần thừa không được sao chép.")],
        ),
    },
    solutions=[("pa-sec-password-full", PWD_REF, PWD_WRONG),
               ("pa-sec-secrets-loader", CFG_REF, CFG_WRONG)],
)

write_checkpoint(
    MOD, "pa-checkpoint-security",
    "Checkpoint: Security Engineering",
    "Prove you can spot the vulnerable handler and state exactly which defense was missing.",
    25,
    """
**The exam question:** the same feature ships twice — once with authorization
derived from the session, once with the owner id accepted from the request
body. Both pass every functional test. Which one gets your customers breached?

The checkpoint challenge is that judgment, mechanized: given handler records,
decide clean vs vulnerable vs critical — the exact triage a security reviewer
performs in the first five minutes of an audit.
""",
    "Checkpoint: Kỹ thuật bảo mật",
    "Chứng minh bạn phát hiện được handler yếu và nói chính xác biện pháp phòng thủ nào còn thiếu.",
    """
**Câu hỏi thi:** cùng một tính năng được ship hai lần — một lần với ủy quyền
suy ra từ session, một lần nhận owner id từ request body. Cả hai pass mọi bài
test chức năng. Cái nào khiến khách hàng của bạn bị đánh cắp dữ liệu?

Thử thách checkpoint là phán đoán đó, được cơ khí hóa: cho các bản ghi handler,
quyết định clean vs vulnerable vs critical — đúng ba cách phân loại mà một
reviewer bảo mật làm trong năm phút đầu của một cuộc kiểm toán.
""",
    challenge(
        "pa-sec-gate",
        "The five-minute audit",
        "Implement `security_gate(handlers)` — stricter cousin of the practice audit:\n\n- each handler: `{'name', 'checks': set, 'public': bool}` where 'public' marks endpoints intentionally unauthenticated (health checks)\n- an endpoint that is NOT public must have 'auth' AND 'owner' (data endpoints) — missing either → vulnerable with `'critical': True`\n- an endpoint that IS public but has any of 'auth'/'owner' checks is suspicious (flag `'suspicious': True` — why would a health check need auth code?)\n- missing 'params' or 'encode' → vulnerable (not critical)\n- return `{'clean': [...], 'vulnerable': [...worst-first, ties by name...]}` where vulnerable entries carry 'missing' (sorted), and 'critical'/'suspicious' booleans only when True",
        "# TODO: security_gate",
        [
            ("triage in one pass",
             "hs = [\n    {'name': 'health', 'checks': set(), 'public': True},\n    {'name': 'weird-health', 'checks': {'auth'}, 'public': True},\n    {'name': 'orders', 'checks': {'auth', 'owner', 'params', 'encode'}, 'public': False},\n    {'name': 'orders-idor', 'checks': {'auth', 'params', 'encode'}, 'public': False},\n    {'name': 'upload', 'checks': {'auth', 'owner'}, 'public': False},\n]\nr = security_gate(hs)\nassert r['clean'] == ['health', 'orders']\nbyname = {v['name']: v for v in r['vulnerable']}\nassert byname['orders-idor']['critical'] is True and byname['orders-idor']['missing'] == ['owner']\nassert byname['weird-health']['suspicious'] is True\nassert byname['upload']['missing'] == ['encode'] and 'critical' not in byname['upload']\nprint('ok')",
             "Public+authless is clean; data+no-owner is critical; non-critical vulnerability notes encode only."),
        ],
        level="build",
    ),
    vi_challenge(
        "Năm phút kiểm toán",
        "Cài `security_gate(handlers)` — bản họ hàng nghiêm ngặt hơn của bài audit:\n\n- mỗi handler: `{'name', 'checks': set, 'public': bool}` với 'public' đánh dấu endpoint chủ động không xác thực (health check)\n- endpoint KHÔNG public phải có 'auth' VÀ 'owner' (endpoint dữ liệu) — thiếu một trong hai → vulnerable với `'critical': True`\n- endpoint CÓ public nhưng lại mang bất kỳ check 'auth'/'owner' nào là đáng ngờ (đánh dấu `'suspicious': True` — health check nào cần code auth?)\n- thiếu 'params' hoặc 'encode' → vulnerable (không critical)\n- trả `{'clean': [...], 'vulnerable': [...xấu nhất trước, hòa theo tên...]}` với các entry vulnerable mang 'missing' (đã sắp), và boolean 'critical'/'suspicious' chỉ khi True",
        [("Phân loại trong một lượt", "Public+không-auth là clean; dữ liệu+không-owner là critical; lỗ hổng không critical chỉ ghi chú encode.")],
    ),
    solution=(
        "def security_gate(handlers):\n"
        "    clean, vulnerable = [], []\n"
        "    for h in handlers:\n"
        "        checks = h['checks']\n"
        "        missing = []\n"
        "        entry = {'name': h['name']}\n"
        "        if h['public']:\n"
        "            suspicious = bool(checks & {'auth', 'owner'})\n"
        "            if suspicious:\n"
        "                entry['suspicious'] = True\n"
        "                entry['missing'] = ['unneeded-auth-checks']\n"
        "                vulnerable.append(entry)\n"
        "            else:\n"
        "                clean.append(h['name'])\n"
        "            continue\n"
        "        if 'auth' not in checks or 'owner' not in checks:\n"
        "            missing += [c for c in ('auth', 'owner') if c not in checks]\n"
        "            entry['critical'] = True\n"
        "        for c in ('params', 'encode'):\n"
        "            if c not in checks:\n"
        "                missing.append(c)\n"
        "        if missing:\n"
        "            entry['missing'] = sorted(missing)\n"
        "            vulnerable.append(entry)\n"
        "        else:\n"
        "            clean.append(h['name'])\n"
        "    vulnerable.sort(key=lambda e: (-len(e.get('missing', [])), e['name']))\n"
        "    return {'clean': clean, 'vulnerable': vulnerable}\n"
    ),
    wrong=(
        "def security_gate(handlers):\n"
        "    clean, vulnerable = [], []\n"
        "    for h in handlers:\n"
        "        # WRONG: treats public endpoints as vulnerable and misses the owner check\n"
        "        if not h['checks']:\n"
        "            vulnerable.append({'name': h['name'], 'missing': ['auth', 'owner'], 'critical': True})\n"
        "        elif 'params' not in h['checks'] or 'encode' not in h['checks']:\n"
        "            missing = sorted({'params', 'encode'} - h['checks'])\n"
        "            vulnerable.append({'name': h['name'], 'missing': missing})\n"
        "        else:\n"
        "            clean.append(h['name'])\n"
        "    return {'clean': clean, 'vulnerable': vulnerable}\n"
    ),
)

print("module 12 complete")
