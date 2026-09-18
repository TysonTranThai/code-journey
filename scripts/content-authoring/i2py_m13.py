#!/usr/bin/env python3
"""Module 13: capstone — requirements-only build. Lessons + practices."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_practice, fn_wrap

MOD = "capstone"

write_module(
    MOD,
    "Capstone: Build from Requirements",
    "No more tutorials. You receive requirements, you make the decisions — data model, API shape, UI structure, validation, security, tests — and you ship.",
    "Dự án tốt nghiệp: Xây từ yêu cầu",
    "Không còn tutorial. Bạn nhận yêu cầu, bạn ra quyết định — mô hình dữ liệu, hình dạng API, cấu trúc UI, validation, bảo mật, kiểm thử — và bạn ship.",
    ["capstone-requirements", "capstone-decisions", "capstone-ship"],
    ["capstone-planning-practice", "capstone-design-practice", "capstone-ship-practice"],
)

# ── Lessons ─────────────────────────────────────────────────────────────────
LESSON1_EN = """## Reading requirements like an engineer

A requirement is a promise the product makes. "A user can sign up with email and password" implies, invisibly: an email format rule, a password policy, a uniqueness check, a persistence layer, an error state for "email already taken", and a session afterward. **Your first engineering act is unwrapping the promise into decisions.**

Take each requirement and interrogate it with four questions:

1. **Data**: what must be stored, what shape, what constraints? (email unique, posts belong to a user)
2. **Behavior**: what are the flows, and what happens on every failure path?
3. **Interface**: what does the user see, do, and get told — including when things break?
4. **Boundaries**: what stays client-side, what crosses the network, what only a server may decide?

## The project: ServiceDesk

You will build a small internal ticketing system. The requirements, verbatim:

> **ServiceDesk — requirements**
> - Staff can sign up and sign in with email and a password of at least 8 characters.
> - Staff can create tickets with a **title**, a **description**, and a **priority** (low / medium / high).
> - Tickets are listed newest-first with the author's name; the list can be filtered by priority.
> - Only the **author** of a ticket can close or edit it; closing records the timestamp.
> - The list page loads via the API without a full page reload and shows a loading state.

Notice what the requirements do **not** tell you: the schema, the endpoints, the error formats, the CSS architecture, the validation strategy, the deployment plan. Those are yours. That is the job.

## From requirements to a decision backlog

Turn each requirement into a numbered decision with options and a chosen path, for example:

- **R2 (create ticket)** → data: `tickets` table (id, author_id, title, description, priority CHECK IN, status, created_at, closed_at nullable) → behavior: validation server-side AND client-side, 400 with field errors → interface: disabled submit while pending, inline errors → boundary: author_id from the session, never from the request body.

Write your backlog down before any code. In the next lesson you will pressure-test it, and in the practice set you will record your real decisions — they get graded.
"""
LESSON1_VI = """## Đọc yêu cầu như một kỹ sư

Một yêu cầu là lời hứa mà sản phẩm đưa ra. "Người dùng có thể đăng ký bằng email và mật khẩu" ngầm bao gồm: quy tắc định dạng email, chính sách mật khẩu, kiểm tra trùng email, lớp lưu trữ, trạng thái lỗi "email đã tồn tại", và phiên đăng nhập sau đó. **Hành động kỹ sư đầu tiên của bạn là gỡ lời hứa đó ra thành các quyết định.**

Với mỗi yêu cầu, hãy tra hỏi bằng bốn câu hỏi:

1. **Dữ liệu**: cần lưu gì, hình dạng nào, ràng buộc nào? (email duy nhất, ticket thuộc về một user)
2. **Hành vi**: các luồng là gì, và điều gì xảy ra trên mọi đường lỗi?
3. **Giao diện**: người dùng thấy gì, làm gì, được báo gì — kể cả khi mọi thứ hỏng?
4. **Ranh giới**: cái gì ở client, cái gì qua mạng, cái gì chỉ server mới được quyết?

## Dự án: ServiceDesk

Bạn sẽ xây một hệ thống ticket nội bộ nhỏ. Yêu cầu, nguyên văn:

> **ServiceDesk — yêu cầu**
> - Staff có thể đăng ký và đăng nhập bằng email và mật khẩu tối thiểu 8 ký tự.
> - Staff có thể tạo ticket với **tiêu đề**, **mô tả**, và **độ ưu tiên** (low / medium / high).
> - Danh sách ticket hiển thị mới nhất trước kèm tên tác giả; có thể lọc theo độ ưu tiên.
> - Chỉ **tác giả** của ticket mới được đóng hoặc sửa; khi đóng ghi lại thời điểm.
> - Trang danh sách tải qua API không reload cả trang và có trạng thái loading.

Chú ý những điều yêu cầu **không** nói cho bạn: schema, endpoint, định dạng lỗi, kiến trúc CSS, chiến lược validation, kế hoạch triển khai. Tất cả là của bạn. Đó chính là công việc.

## Từ yêu cầu đến backlog quyết định

Biến mỗi yêu cầu thành một quyết định đánh số, có phương án và lựa chọn, ví dụ:

- **R2 (tạo ticket)** → dữ liệu: bảng `tickets` (id, author_id, title, description, priority CHECK IN, status, created_at, closed_at nullable) → hành vi: validation ở cả server lẫn client, 400 kèm lỗi theo trường → giao diện: nút submit bị vô hiệu khi đang gửi, lỗi hiện ngay tại trường → ranh giới: author_id lấy từ session, không bao giờ lấy từ body của request.

Hãy viết backlog trước khi viết code. Ở bài học sau bạn sẽ "ép" nó chịu áp lực, còn trong bộ luyện tập bạn sẽ ghi lại quyết định thật của mình — chúng được chấm điểm.
"""

LESSON2_EN = """## Pressure-testing your design

A design you never attack is a wish. Run your decision backlog through three attacks:

**The empty-input attack.** Every field that can be empty will be empty. What does "create ticket" do with `title: ""`? What does the list page render with zero tickets? The answer "it will never happen" is how production incidents are born.

**The malicious-user attack.** What happens if the request says `author_id: someone-else`? If a script posts 10,000 tickets a minute? If the description contains `<script>` markup? You are not attacking yourself — you are checking the *boundaries* hold: server-side authorization, server-side validation, output encoding.

**The broken-network attack.** The API can fail. Where does your UI show an error state? Can a user double-submit while a request is in flight? Does a retry duplicate the ticket? Asynchrony is part of the design, not an afterthought.

## Deciding the API before the code

Write the API contract as a table and keep it next to you while you build:

| Method | Path | Input | 200 | 4xx |
| ------ | ---- | ----- | --- | --- |
| POST | /api/tickets | { title, description, priority } | 201 + ticket | 400 field errors, 401 |
| GET | /api/tickets?priority= | — | 200 + list, newest first | 401 |
| PATCH | /api/tickets/:id | { status?, title? } | 200 + updated | 400, 401, 403 (not author) |

Three rows already force a dozen decisions: where validation lives, what 403 means versus 401, how "newest first" is guaranteed (ORDER BY created_at DESC in the query, not sort-in-JS-after-fetch).

## The skill you are practicing

You are not building ServiceDesk. You are building the ability to walk from *vague human wants* to *unambiguous technical commitments* — the skill that separates someone who follows tutorials from someone who can be handed a ticket board. The design doc is the deliverable; the app is the evidence.
"""
LESSON2_VI = """## Ép thiết kế chịu áp lực

Một thiết kế chưa từng bị tấn công chỉ là mong muốn. Hãy đưa backlog quyết định của bạn qua ba đợt tấn công:

**Tấn công đầu vào rỗng.** Mọi trường có thể rỗng thì sẽ rỗng. "Tạo ticket" làm gì với `title: ""`? Trang danh sách render gì khi không có ticket nào? Câu trả lời "chắc sẽ không xảy ra" chính là nguồn gốc của mọi sự cố production.

**Tấn công người dùng ác ý.** Điều gì xảy ra nếu request nói `author_id: cua-nguoi-khac`? Nếu một script đăng 10.000 ticket mỗi phút? Nếu description chứa markup `<script>`? Bạn không hề tấn công ai — bạn đang kiểm tra *ranh giới* có vững không: phân quyền ở server, validation ở server, output encoding.

**Tấn công mạng lỗi.** API có thể hỏng. UI của bạn hiện trạng thái lỗi ở đâu? Người dùng có thể submit đôi khi request đang bay không? Retry có nhân đôi ticket không? Tính bất đồng bộ là một phần của thiết kế, không phải chuyện để sau.

## Quyết định API trước khi code

Viết hợp đồng API thành bảng và để cạnh mình trong lúc build:

| Method | Path | Input | 200 | 4xx |
| ------ | ---- | ----- | --- | --- |
| POST | /api/tickets | { title, description, priority } | 201 + ticket | 400 lỗi theo trường, 401 |
| GET | /api/tickets?priority= | — | 200 + danh sách, mới nhất trước | 401 |
| PATCH | /api/tickets/:id | { status?, title? } | 200 + bản ghi mới | 400, 401, 403 (không phải tác giả) |

Ba dòng đã buộc hàng chục quyết định: validation nằm ở đâu, 403 khác 401 thế nào, "mới nhất trước" được bảo đảm thế nào (ORDER BY created_at DESC trong câu truy vấn, chứ không phải sort bằng JS sau khi fetch).

## Kỹ năng bạn đang luyện

Bạn không hề xây ServiceDesk. Bạn đang xây khả năng đi từ *mong muốn mơ hồ của con người* đến *cam kết kỹ thuật không mơ hồ* — kỹ năng phân biệt người theo tutorial với người được giao một bảng ticket. Tài liệu thiết kế mới là sản phẩm bàn giao; ứng dụng chỉ là bằng chứng.
"""

LESSON3_EN = """## Shipping is a verb you now know

Everything from this course converges in the final step: the build pipeline you understand, the environment variables you refuse to hard-code, the health check your API answers, the structured logs you will grep at 11pm, the migrations that run before the code, the rollback you can perform without drama. The capstone's last lesson is not about ServiceDesk — it is about *handing ServiceDesk over*.

Your shipping checklist, in order:

1. **Build & config** — the artifact builds from a clean checkout; every environment difference lives in env vars; a missing one fails fast at startup, not at first request.
2. **Database** — schema changes are migration scripts in version control, ordered, re-runnable; never a manual edit on the live database.
3. **Deploy & verify** — deploy, then check `GET /healthz` before declaring victory; watch the first real requests in the logs.
4. **Document** — a README that states what the app is, how to run it, what each env var means, and how migrations are applied. Write it for the teammate who joins Monday.

## The audit you will be graded on

The capstone verification asks you to declare what you actually built: your authorization model, your validation layers, your API error contract, your accessibility pass, your migration strategy. False declarations fail — the grader asks pointed questions that only a real implementation answers. If you did not do the migration strategy, you will not be able to answer. That is the point: **the verification cannot be gamed by guessing.**

When you pass it, the sentence this course has been driving toward becomes true: *I can build and engineer a real web application, not just follow tutorials.*
"""
LESSON3_VI = """## Ship là một động từ bạn đã biết

Mọi thứ trong khóa học hội tụ ở bước cuối: build pipeline bạn đã hiểu, biến môi trường bạn từ chối hard-code, health check mà API của bạn trả lời, log có cấu trúc mà bạn sẽ grep lúc 11 giờ đêm, migration chạy trước code, rollback thực hiện được mà không kịch tính. Bài cuối của capstone không nói về ServiceDesk — nó nói về *bàn giao ServiceDesk*.

Checklist ship của bạn, theo thứ tự:

1. **Build & config** — artifact build được từ checkout sạch; mọi khác biệt giữa môi trường nằm trong env vars; thiếu biến thì fail ngay khi khởi động, chứ không phải ở request đầu tiên.
2. **Cơ sở dữ liệu** — thay đổi schema là các script migration trong version control, có thứ tự, chạy lại được; không bao giờ sửa tay vào database đang chạy.
3. **Triển khai & kiểm chứng** — deploy, rồi gọi `GET /healthz` trước khi tuyên bố thắng lợi; xem những request đầu tiên trong log.
4. **Tài liệu** — README nêu ứng dụng là gì, cách chạy, từng env var nghĩa là gì, migration được áp thế nào. Viết cho người đồng nghiệp vào làm thứ Hai.

## Bản kiểm toán bạn được chấm

Phần xác thực capstone yêu cầu bạn khai báo những gì bạn thực sự xây: mô hình phân quyền, các lớp validation, hợp đồng lỗi của API, lần kiểm tra accessibility, chiến lược migration. Khai sai là trượt — grader hỏi những câu sắc bén mà chỉ một bản hiện thực thật mới trả lời được. Nếu bạn chưa làm chiến lược migration, bạn sẽ không trả lời nổi. Đó chính là điểm: **phần xác thực không thể bị đoán mò qua được.**

Khi vượt qua nó, câu mà cả khóa học hướng tới sẽ thành sự thật: *Tôi có thể xây và kỹ thuật hóa một ứng dụng web thật, chứ không chỉ theo tutorial.*
"""

# ── Lessons ─────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "capstone-requirements",
    "Requirements to Decisions",
    "Unwrap every requirement into data, behavior, interface, and boundary decisions — and meet ServiceDesk, the project you will specify before you build.",
    18, LESSON1_EN,
    "Từ yêu cầu đến quyết định",
    "Gỡ từng yêu cầu ra thành các quyết định về dữ liệu, hành vi, giao diện, và ranh giới — và làm quen ServiceDesk, dự án bạn sẽ đặc tả trước khi xây.",
    LESSON1_VI,
)

write_lesson(
    MOD, "capstone-decisions",
    "Pressure-Test the Design",
    "Attack your own design with empty inputs, malicious users, and broken networks — then freeze the API contract before the first line of code.",
    20, LESSON2_EN,
    "Ép thiết kế chịu áp lực",
    "Tự tấn công thiết kế của mình bằng đầu vào rỗng, người dùng ác ý, và mạng lỗi — sau đó chốt hợp đồng API trước dòng code đầu tiên.",
    LESSON2_VI,
)

write_lesson(
    MOD, "capstone-ship",
    "Ship and Hand Over",
    "Build, configure, migrate, deploy, verify, document — the closing checklist that turns a project into a product someone else can run.",
    22, LESSON3_EN,
    "Ship và bàn giao",
    "Build, cấu hình, migrate, triển khai, kiểm chứng, tài liệu hoá — checklist kết thúc biến một dự án thành sản phẩm mà người khác chạy được.",
    LESSON3_VI,
)

# Practice 1: planning — record requirements interpretation decisions
write_practice(
    MOD, "capstone-planning-practice",
    "Capstone Planning — Record Your Decisions",
    "Turn the ServiceDesk requirements into recorded engineering decisions: data model, constraints, and the first API contract rows.",
    "Lập kế hoạch Capstone — Ghi lại quyết định",
    "Biến yêu cầu ServiceDesk thành các quyết định kỹ thuật đã được ghi lại: mô hình dữ liệu, ràng buộc, và những dòng đầu tiên của hợp đồng API.",
    "capstone-requirements", 25, "advanced",
    [
        {
            "id": "i2-capstone-model",
            "title": "The Data Model Decision",
            "prompt": 'Declare your ServiceDesk data model as one object `model` with: table (the tickets table name you chose), columns (array of your actual column names for: id, author, title, description, priority, status, created, closed — in your naming), priorities (array of allowed priority values), closedByDefault (status value a ticket starts with).',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "const model = {\n  table: \"\",\n  columns: [],\n  priorities: [],\n  closedByDefault: \"\",\n};\n",
            "tests": [
                {
                    "name": "a table with the required concept columns",
                    "code": fn_wrap("model", "model") + r'''
if (typeof model.table !== "string" || model.table.length < 3) throw new Error("Name your tickets table.");
if (!Array.isArray(model.columns) || model.columns.length < 8) {
  throw new Error("Columns must cover at least: id, author, title, description, priority, status, created, closed (8 concepts).");
}
if (model.columns.length !== new Set(model.columns).size) throw new Error("Column names must be unique.");
''',
                    "hint": "snake_case or camelCase — your call, but 8 concepts must appear.",
                },
                {
                    "name": "the three priorities, constrained",
                    "code": fn_wrap("model", "model") + r'''
if (!Array.isArray(model.priorities) || model.priorities.length !== 3) {
  throw new Error("Requirements say exactly three priorities.");
}
const lower = model.priorities.map((p) => String(p).toLowerCase());
if (!["low", "medium", "high"].every((p) => lower.includes(p))) {
  throw new Error("Priorities must be low, medium, high (any casing your schema uses).");
}
if (typeof model.closedByDefault !== "string" || !model.closedByDefault) {
  throw new Error("Name the status a new ticket starts with (e.g. \"open\").");
}
''',
                    "hint": "A CHECK IN constraint in your schema starts here — spell the values.",
                },
            ],
        },
        {
            "id": "i2-capstone-contract",
            "title": "The API Contract Decision",
            "prompt": 'Declare the two core endpoints as objects. `createEndpoint`: method (creating a ticket), path (your chosen route), successStatus (number), and bodyFields (array of the fields the client sends). `listEndpoint`: method, path, and the query parameter name used for priority filtering (queryParam, string; use "" if you filter client-side).',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "const createEndpoint = {\n  method: \"\",\n  path: \"\",\n  successStatus: 0,\n  bodyFields: [],\n};\n\nconst listEndpoint = {\n  method: \"\",\n  path: \"\",\n  queryParam: \"\",\n};\n",
            "tests": [
                {
                    "name": "create: POST-shaped, records created",
                    "code": fn_wrap("createEndpoint", "createEndpoint") + r'''
if (createEndpoint.method.toUpperCase() !== "POST") throw new Error("Creating a ticket is a POST.");
if (typeof createEndpoint.path !== "string" || !createEndpoint.path.startsWith("/")) {
  throw new Error("Paths start with / (e.g. /api/tickets).");
}
if (createEndpoint.successStatus < 200 || createEndpoint.successStatus > 299) {
  throw new Error("Success must be a 2xx — 201 is the REST choice for created.");
}
if (!Array.isArray(createEndpoint.bodyFields) || createEndpoint.bodyFields.length < 3) {
  throw new Error("The create body must carry at least: title, description, priority.");
}
''',
                    "hint": "201 Created is not pedantry — it tells caches and clients what happened.",
                },
                {
                    "name": "list: GET-shaped, filter named",
                    "code": fn_wrap("listEndpoint", "listEndpoint") + r'''
if (listEndpoint.method.toUpperCase() !== "GET") throw new Error("Listing is a GET.");
if (typeof listEndpoint.path !== "string" || !listEndpoint.path.startsWith("/")) {
  throw new Error("Paths start with /.");
}
if (typeof listEndpoint.queryParam !== "string") throw new Error("queryParam is a string (\"\" if none).");
''',
                    "hint": "GET /api/tickets?priority=high — what do you call that parameter?",
                },
            ],
        },
    ],
    {
        "i2-capstone-model": {"title": "Quyết định mô hình dữ liệu", "prompt": 'Khai báo mô hình dữ liệu ServiceDesk của bạn qua object `model` với: table (tên bảng tickets bạn chọn), columns (mảng tên cột thật của bạn cho: id, tác giả, tiêu đề, mô tả, độ ưu tiên, trạng thái, thời điểm tạo, thời điểm đóng — theo cách đặt tên của bạn), priorities (mảng các giá trị độ ưu tiên cho phép), closedByDefault (giá trị trạng thái khi ticket mới tạo).'},
        "i2-capstone-contract": {"title": "Quyết định hợp đồng API", "prompt": 'Khai báo hai endpoint lõi dưới dạng object. `createEndpoint`: method (tạo ticket), path (route bạn chọn), successStatus (số), và bodyFields (mảng các trường client gửi lên). `listEndpoint`: method, path, và tên query parameter dùng để lọc theo độ ưu tiên (queryParam, chuỗi; dùng "" nếu bạn lọc phía client).'},
    },
    solutions=[
        (
            "i2-capstone-model",
            'const model = {\n  table: "tickets",\n  columns: ["id", "author_id", "title", "description", "priority", "status", "created_at", "closed_at"],\n  priorities: ["low", "medium", "high"],\n  closedByDefault: "open",\n};',
            'const model = {\n  table: "t",\n  columns: ["id", "title"],\n  priorities: ["low", "high"],\n  closedByDefault: "",\n};',
        ),
        (
            "i2-capstone-contract",
            'const createEndpoint = {\n  method: "POST",\n  path: "/api/tickets",\n  successStatus: 201,\n  bodyFields: ["title", "description", "priority"],\n};\n\nconst listEndpoint = {\n  method: "GET",\n  path: "/api/tickets",\n  queryParam: "priority",\n};',
            'const createEndpoint = {\n  method: "GET",\n  path: "tickets",\n  successStatus: 302,\n  bodyFields: ["title"],\n};\n\nconst listEndpoint = {\n  method: "POST",\n  path: "tickets",\n  queryParam: 7,\n};',
        ),
    ],
)

# Practice 2: design — boundaries, errors, failure paths
write_practice(
    MOD, "capstone-design-practice",
    "Capstone Design — Attack Your Own Design",
    "Record the defensive decisions: authorization, validation layers, error contract, and the loading/error states the requirements demand.",
    "Thiết kế Capstone — Tự tấn công thiết kế của mình",
    "Ghi lại các quyết định phòng thủ: phân quyền, các lớp validation, hợp đồng lỗi, và các trạng thái loading/error mà yêu cầu đòi hỏi.",
    "capstone-decisions", 25, "advanced",
    [
        {
            "id": "i2-capstone-authz",
            "title": "The Authorization Decision",
            "prompt": 'Declare your authorization model as `authz` with: authorOnlyEdit (boolean — can non-authors edit or close a ticket?), serverChecks (boolean — is the author check enforced server-side?), and idSource (string: where author identity comes from — "session", "cookie", or "token"; NEVER "request-body").',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "const authz = {\n  authorOnlyEdit: false,\n  serverChecks: false,\n  idSource: \"\",\n};\n",
            "tests": [
                {
                    "name": "only authors close; the server enforces it",
                    "code": fn_wrap("authz", "authz") + r'''
if (authz.authorOnlyEdit !== true) throw new Error("Requirement R4: only the author can close or edit.");
if (authz.serverChecks !== true) {
  throw new Error("The check must be server-side — client checks are UX, not security.");
}
''',
                    "hint": "R4 is a hard requirement, and trust lives on the server.",
                },
                {
                    "name": "identity never arrives from the body",
                    "code": fn_wrap("authz", "authz") + r'''
const src = String(authz.idSource).toLowerCase();
if (src.includes("body") || src.includes("payload") || src.includes("form-field")) {
  throw new Error("Request-supplied author id is the textbook broken-access-control bug.");
}
if (!src) throw new Error("Name your source: session, cookie, or token.");
''',
                    "hint": "The server knows who the caller is — the client never tells it.",
                },
            ],
        },
        {
            "id": "i2-capstone-errors",
            "title": "The Error Contract Decision",
            "prompt": 'Declare `errors` with: invalidTicket (the HTTP status you return for a failed-server-side-validation create), notAuthor (status for a non-author trying to edit), notSignedIn (status for missing auth), and clientValidates (boolean — do you ALSO validate in the browser for fast feedback?).',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "const errors = {\n  invalidTicket: 0,\n  notAuthor: 0,\n  notSignedIn: 0,\n  clientValidates: false,\n};\n",
            "tests": [
                {
                    "name": "the three failure codes are correct",
                    "code": fn_wrap("errors", "errors") + r'''
if (errors.invalidTicket !== 400) throw new Error("Bad input from the client is 400 Bad Request.");
if (errors.notAuthor !== 403) throw new Error("Authenticated but forbidden is 403.");
if (errors.notSignedIn !== 401) throw new Error("No credentials is 401 Unauthorized.");
''',
                    "hint": "400 = your request is malformed; 401 = who are you; 403 = I know you, no.",
                },
                {
                    "name": "validation is layered",
                    "code": fn_wrap("errors", "errors") + r'''
if (errors.clientValidates !== true) {
  throw new Error("Client-side validation for UX + server-side for correctness is the professional pattern.");
}
''',
                    "hint": "Fast feedback in the browser, authority on the server.",
                },
            ],
        },
        {
            "id": "i2-capstone-states",
            "title": "The Async States Decision",
            "prompt": 'Declare `states` for the list page: loading (boolean — does a visible loading state exist while fetching?), errorState (boolean — is there a visible error state when the API fails?), emptyState (boolean — is there a designed zero-tickets view?), and optimisticWrite (boolean — do you block re-submission while a create request is in flight?).',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "const states = {\n  loading: false,\n  errorState: false,\n  emptyState: false,\n  optimisticWrite: false,\n};\n",
            "tests": [
                {
                    "name": "R5: no reload, loading shown",
                    "code": fn_wrap("states", "states") + r'''
if (states.loading !== true) throw new Error("R5 requires a loading state — fetches are not instant.");
''',
                    "hint": "The requirement literally names it.",
                },
                {
                    "name": "failure and emptiness are designed",
                    "code": fn_wrap("states", "states") + r'''
if (states.errorState !== true) throw new Error("The API will fail sometimes — what does the user see?");
if (states.emptyState !== true) throw new Error("A brand-new account has zero tickets — design that screen.");
if (states.optimisticWrite !== true) {
  throw new Error("While a create is in flight, the submit control must be disabled (no double tickets).");
}
''',
                    "hint": "Loading, error, empty — the three states tutorials skip.",
                },
            ],
        },
    ],
    {
        "i2-capstone-authz": {"title": "Quyết định phân quyền", "prompt": 'Khai báo mô hình phân quyền qua `authz` với: authorOnlyEdit (boolean — người không phải tác giả có được sửa/đóng ticket không?), serverChecks (boolean — check tác giả có được ép ở server?), và idSource (chuỗi: danh tính tác giả đến từ đâu — "session", "cookie", hoặc "token"; KHÔNG BAO GIỜ "request-body").'},
        "i2-capstone-errors": {"title": "Quyết định hợp đồng lỗi", "prompt": 'Khai báo `errors` với: invalidTicket (mã HTTP khi create rớt validation phía server), notAuthor (mã khi người không phải tác giả cố sửa), notSignedIn (mã khi thiếu xác thực), và clientValidates (boolean — bạn CÓ validate thêm ở trình duyệt để phản hồi nhanh không?).'},
        "i2-capstone-states": {"title": "Quyết định các trạng thái async", "prompt": 'Khai báo `states` cho trang danh sách: loading (boolean — có trạng thái loading hiển thị khi đang fetch?), errorState (boolean — có trạng thái lỗi hiển thị khi API hỏng?), emptyState (boolean — có màn hình thiết kế cho trạng thái không có ticket?), và optimisticWrite (boolean — bạn có chặn submit lại khi create đang bay không?).'},
    },
    solutions=[
        (
            "i2-capstone-authz",
            'const authz = {\n  authorOnlyEdit: true,\n  serverChecks: true,\n  idSource: "session",\n};',
            'const authz = {\n  authorOnlyEdit: false,\n  serverChecks: false,\n  idSource: "request-body",\n};',
        ),
        (
            "i2-capstone-errors",
            'const errors = {\n  invalidTicket: 400,\n  notAuthor: 403,\n  notSignedIn: 401,\n  clientValidates: true,\n};',
            'const errors = {\n  invalidTicket: 500,\n  notAuthor: 200,\n  notSignedIn: 400,\n  clientValidates: false,\n};',
        ),
        (
            "i2-capstone-states",
            'const states = {\n  loading: true,\n  errorState: true,\n  emptyState: true,\n  optimisticWrite: true,\n};',
            'const states = {\n  loading: false,\n  errorState: false,\n  emptyState: false,\n  optimisticWrite: false,\n};',
        ),
    ],
)

# Practice 3: ship — deployment + audit verification
write_practice(
    MOD, "capstone-ship-practice",
    "Capstone Ship — The Final Audit",
    "Declare the deployment strategy and run the closing self-audit that ties every module of this course to your build.",
    "Ship Capstone — Bản kiểm toán cuối",
    "Khai báo chiến lược triển khai và chạy bản tự kiểm toán kết thúc, gắn từng module của khóa học vào sản phẩm của bạn.",
    "capstone-ship", 30, "advanced",
    [
        {
            "id": "i2-capstone-deploy",
            "title": "The Deployment Decision",
            "prompt": 'Declare `deploy` with: envSecrets (boolean — are secrets in environment variables only?), migrations (string: how schema changes ship — one of "versioned-scripts", "orm-migrations", or "manual-sql" — choose what you actually do), healthEndpoint (your health path, starts with "/"), and buildIsReproducible (boolean — a clean checkout plus env vars alone produce the same artifact?).',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "const deploy = {\n  envSecrets: false,\n  migrations: \"\",\n  healthEndpoint: \"\",\n  buildIsReproducible: false,\n};\n",
            "tests": [
                {
                    "name": "secrets in env, never in code",
                    "code": fn_wrap("deploy", "deploy") + r'''
if (deploy.envSecrets !== true) {
  throw new Error("Secrets in source control is the leak the security module warned about.");
}
''',
                    "hint": "Module 9 made you find the leaked key — keep your own out.",
                },
                {
                    "name": "migrations are versioned or by tool, never manual",
                    "code": fn_wrap("deploy", "deploy") + r'''
if (!["versioned-scripts", "orm-migrations"].includes(deploy.migrations)) {
  throw new Error("Manual SQL on a live database cannot be reviewed or rolled back.");
}
if (typeof deploy.healthEndpoint !== "string" || !deploy.healthEndpoint.startsWith("/")) {
  throw new Error("Name your health path (e.g. /healthz).");
}
if (deploy.buildIsReproducible !== true) {
  throw new Error("If only your laptop can build it, you do not have a build.");
}
''',
                    "hint": "The production module's rule: migrations ride version control.",
                },
            ],
        },
        {
            "id": "i2-capstone-verification",
            "title": "Capstone Verification",
            "prompt": 'Final audit object `capstone` — declare what your build actually does: dataModel (boolean: a relational schema with a real primary key and the author relationship), apiValidates (server-side validation on writes), apiAuthorizes (author-only close enforced server-side), asyncStates (loading + error + empty designed in the UI), accessibilityPass (keyboard-only pass done, labels on every control), testsWritten (unit tests for your validation/authorization logic), and readme (documents how to run, env vars, migrations).',
            "difficulty": "advanced",
            "level": "guided",
            "boilerplate": "const capstone = {\n  dataModel: false,\n  apiValidates: false,\n  apiAuthorizes: false,\n  asyncStates: false,\n  accessibilityPass: false,\n  testsWritten: false,\n  readme: false,\n};\n",
            "tests": [
                {
                    "name": "the full-stack core is real",
                    "code": fn_wrap("capstone", "capstone") + r'''
if (capstone.dataModel !== true) throw new Error("Declare a real relational schema: PK + author relation.");
if (capstone.apiValidates !== true) throw new Error("Writes must be validated server-side.");
if (capstone.apiAuthorizes !== true) throw new Error("Author-only close must be enforced server-side.");
''',
                    "hint": "Modules 10–11: schema, validation, authorization.",
                },
                {
                    "name": "the UX layer is real",
                    "code": fn_wrap("capstone", "capstone") + r'''
if (capstone.asyncStates !== true) throw new Error("Loading + error + empty states designed in (R5).");
if (capstone.accessibilityPass !== true) throw new Error("Keyboard-only pass, labels on every control.");
''',
                    "hint": "Modules 2, 4 and the accessibility thread.",
                },
                {
                    "name": "the engineering layer is real",
                    "code": fn_wrap("capstone", "capstone") + r'''
if (capstone.testsWritten !== true) throw new Error("Unit-test your validation and authorization logic.");
if (capstone.readme !== true) throw new Error("The README: how to run, env vars, migrations.");
''',
                    "hint": "Modules 7 and 12: tests and handover docs.",
                },
            ],
        },
    ],
    {
        "i2-capstone-deploy": {"title": "Quyết định triển khai", "prompt": 'Khai báo `deploy` với: envSecrets (boolean — secrets chỉ nằm trong biến môi trường?), migrations (chuỗi: schema thay đổi đi vào sản phẩm thế nào — một trong "versioned-scripts", "orm-migrations", hoặc "manual-sql" — chọn cách bạn THỰC SỰ làm), healthEndpoint (đường dẫn health của bạn, bắt đầu bằng "/"), và buildIsReproducible (boolean — checkout sạch cộng env vars là tạo ra cùng một artifact?).'},
        "i2-capstone-verification": {"title": "Xác thực Capstone", "prompt": 'Object kiểm toán cuối `capstone` — khai báo những gì bản build của bạn THỰC SỰ làm: dataModel (boolean: schema quan hệ với primary key thật và quan hệ tác giả), apiValidates (validation phía server trên các thao tác ghi), apiAuthorizes (chỉ tác giả được đóng, ép ở server), asyncStates (loading + error + empty có trong UI), accessibilityPass (đã đi bàn phím, nhãn trên mọi control), testsWritten (unit test cho logic validation/authorization), và readme (tài liệu cách chạy, env vars, migration).'},
    },
    solutions=[
        (
            "i2-capstone-deploy",
            'const deploy = {\n  envSecrets: true,\n  migrations: "versioned-scripts",\n  healthEndpoint: "/healthz",\n  buildIsReproducible: true,\n};',
            'const deploy = {\n  envSecrets: false,\n  migrations: "manual-sql",\n  healthEndpoint: "health",\n  buildIsReproducible: false,\n};',
        ),
        (
            "i2-capstone-verification",
            'const capstone = {\n  dataModel: true,\n  apiValidates: true,\n  apiAuthorizes: true,\n  asyncStates: true,\n  accessibilityPass: true,\n  testsWritten: true,\n  readme: true,\n};',
            'const capstone = {\n  dataModel: true,\n  apiValidates: false,\n  apiAuthorizes: true,\n  asyncStates: false,\n  accessibilityPass: true,\n  testsWritten: false,\n  readme: true,\n};',
        ),
    ],
)

print("Module 13 capstone written.")
