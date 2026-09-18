#!/usr/bin/env python3
"""Module 12: production — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint

MOD = "production"

write_module(
    MOD,
    "Production Web Applications",
    "What happens after `git push`: builds, environments, deployment, DNS/HTTPS, logging, and the CI/CD loop that ships safely.",
    "Ứng dụng Web trên Production",
    "Điều gì xảy ra sau `git push`: build, môi trường, triển khai, DNS/HTTPS, logging, và vòng lặp CI/CD ship an toàn.",
    ["dev-vs-prod", "build-pipeline", "deploy-dns-https", "observability", "cicd-loop", "prod-checkpoint"],
    ["env-practice", "release-practice", "incident-practice"],
)

write_lesson(
    MOD, "dev-vs-prod",
    "Development vs Production",
    "Different modes, different instincts: speed in dev, correctness and cost in prod — and the config discipline that separates them.",
    18,
    """The same codebase runs in (at least) two worlds, and they optimize for different things.

## What changes between environments

| Concern | Development | Production |
|---|---|---|
| Speed | hot reload, no minification | minified, hashed, cached forever |
| Errors | full stack trace on screen | generic message to users, detail in logs |
| Data | seed fixtures | real, backed-up, revered |
| Secrets | `.env` file, fake keys | vault/environment injection, real keys |
| HTTPS | optional on localhost | mandatory, everywhere |
| Debugging | you, interactively | logs, metrics, alerts |

`NODE_ENV` (or framework equivalent) switches bundles: dev ships unminified code with devtools hooks; prod ships optimized builds. The classic accident: production running with a development build — 3–10× slower JS, dev-only endpoints exposed.

## Configuration, one more time

Module 6's rule scales up: **config lives in environment variables**, read at startup, validated (Zod) before the app accepts traffic. Fail fast on missing config at boot — not at 2am when the first user hits the un-configured path.

```js
const env = EnvSchema.parse(process.env);  // throws at startup with the missing key
```

## Feature flags: decoupling deploy from release

Deploying code ≠ enabling features. Flags let you merge incomplete work (dark), enable gradually (1% → 10% → 100%), and kill a broken feature without rolling back the deploy. The discipline: flags are debt — clean them up when fully rolled out, or the codebase drowns in dead branches.

## The 12-factor mindset

The industry checklist for production services (12factor.net) — the four that matter most here: **config in env** (same image, every environment), **backing services as attached resources** (swap the DB URL, not the code), **logs as event streams** (write to stdout; the platform decides where they go), **disposability** (the app starts fast and shuts down cleanly — kill -TERM handled, connections drained).""",
    "Development vs Production",
    "Hai chế độ, hai bản năng: nhanh ở dev, đúng và tiết kiệm ở prod — và kỷ luật cấu hình tách biệt chúng.",
    """Cùng một codebase chạy trong (ít nhất) hai thế giới, và chúng tối ưu cho hai điều khác nhau.

## Điều gì khác nhau giữa các môi trường

| Mối quan tâm | Development | Production |
|---|---|---|
| Tốc độ | hot reload, không minify | minified, hash, cache vĩnh viễn |
| Lỗi | stack trace đầy đủ trên màn hình | message chung chung cho user, chi tiết vào log |
| Dữ liệu | seed fixture | thật, có backup, được tôn trọng |
| Secret | file `.env`, key giả | bơm qua vault/biến môi trường, key thật |
| HTTPS | tùy chọn trên localhost | bắt buộc, mọi nơi |
| Debug | bạn, tương tác | log, metric, alert |

`NODE_ENV` (hoặc tương đương) chuyển bundle: dev ship code chưa minify với hook devtools; prod ship bản build tối ưu. Tai nạn kinh điển: production chạy bản build development — JS chậm hơn 3–10×, các endpoint chỉ-dev bị phơi ra.

## Cấu hình, lần nữa

Quy tắc của module 6 mở rộng: **cấu hình nằm trong biến môi trường**, đọc lúc khởi động, validate (Zod) trước khi app nhận traffic. Fail fast khi thiếu config ngay lúc boot — đừng đợi 2 giờ sáng khi user đầu tiên đụng vào đường chưa cấu hình.

```js
const env = EnvSchema.parse(process.env);  // ném lỗi lúc startup kèm key còn thiếu
```

## Feature flag: tách deploy khỏi release

Deploy code ≠ bật tính năng. Flag cho phép merge công việc dang dở (ẩn), bật dần dần (1% → 10% → 100%), và tắt tính năng hỏng mà không cần rollback deploy. Kỷ luật: flag là nợ — dọn sạch khi đã bật đủ 100%, nếu không codebase sẽ chìm trong nhánh chết.

## Tư duy 12-factor

Checklist ngành cho dịch vụ production (12factor.net) — bốn điều quan trọng nhất ở đây: **config trong env** (cùng một image, mọi môi trường), **dịch vụ hậu cần là tài nguyên gắn vào** (đổi DB URL, không đổi code), **log là dòng sự kiện** (ghi ra stdout; nền tảng quyết định nơi chứa), **khả năng vứt bỏ** (app khởi động nhanh và tắt sạch sẽ — xử lý kill -TERM, xả kết nối).""",
)

write_lesson(
    MOD, "build-pipeline",
    "The Build Pipeline",
    "From source to deployable artifact: transforms, hashing, source maps, and what 'build failed' should tell you.",
    18,
    """## What a build does

Source code → deployable artifact, via steps you configure:

1. **Compile/transform** — TypeScript → JS, JSX → JS, SCSS → CSS
2. **Bundle** — many files → few, with an import graph
3. **Minify** — strip comments/whitespace, shorten names (terser/esbuild)
4. **Hash & fingerprint** — `app.a83f2c.js` so caches can live forever (module 8)
5. **Emit source maps** — `.map` files translating minified back to original for debugging prod errors

Modern tools (Vite, Next) fuse these with heavy caching — a rebuild only redoes what changed.

## Source maps: your prod debugger

Minified stack traces are unusable (`a.b is not a function` at 1:88231). Source maps restore names and lines. **Upload them to your error tracker** (Sentry et al.) — don't serve them publicly unless you want your source readable by everyone.

## The artifact is immutable

Build once, deploy everywhere. The same hashed artifact goes to staging and production — "works in staging, differs in prod" then means *environment config*, not build drift. Rebuild-per-server is the anti-pattern: two builds are never identical.

## What "build failed" must tell you

CI output is read at 6pm by someone who wants to go home:

- **Which step failed** (typecheck? tests? bundle?) — one glance
- **The actual error** with file and line — pasted above, not buried in 4,000 lines
- **Whether it's yours** — PR-scoped runs prevent "main is broken, not me" confusion

Fast feedback beats thorough feedback: typecheck + unit tests in ~2 minutes on every push; the long E2E suite on PRs and main.

## Environment parity

Same artifact, different config — that's the contract. If staging lacks a service prod has, you will discover the difference in production. Keep environments structurally identical; let config variables be the only delta (and document every one).""",
    "Pipeline build",
    "Từ mã nguồn đến artifact có thể triển khai: biến đổi, hash, source map, và câu 'build failed' phải nói cho bạn điều gì.",
    """## Build làm những gì

Mã nguồn → artifact có thể triển khai, qua các bước bạn cấu hình:

1. **Biên dịch/biến đổi** — TypeScript → JS, JSX → JS, SCSS → CSS
2. **Bundle** — nhiều file → ít file, theo đồ thị import
3. **Minify** — bỏ comment/khoảng trắng, rút gọn tên (terser/esbuild)
4. **Hash & fingerprint** — `app.a83f2c.js` để cache sống mãi (module 8)
5. **Sinh source map** — file `.map` dịch ngược minified về bản gốc để debug lỗi prod

Các công cụ hiện đại (Vite, Next) gộp các bước này với cache mạnh — build lại chỉ làm lại phần thay đổi.

## Source map: debugger của prod

Stack trace đã minify không dùng được (`a.b is not a function` tại 1:88231). Source map khôi phục tên và số dòng. **Tải chúng lên error tracker** (Sentry và bạn bè) — đừng serve công khai nếu không muốn cả thế giới đọc mã nguồn của bạn.

## Artifact là bất biến

Build một lần, triển khai mọi nơi. Cùng một artifact đã hash được đưa lên staging và production — khi đó "chạy ở staging, khác ở prod" nghĩa là *cấu hình môi trường*, không phải lệch build. Build-mỗi-server là anti-pattern: hai lần build không bao giờ giống hệt nhau.

## "Build failed" phải nói cho bạn điều gì

Output CI được đọc lúc 6 giờ tối bởi người muốn về nhà:

- **Bước nào hỏng** (typecheck? test? bundle?) — nhìn một cái là biết
- **Lỗi thật** kèm file và dòng — hiện lên ngay, không chôn trong 4,000 dòng
- **Có phải lỗi của người đó không** — chạy theo phạm vi PR tránh trò "main hỏng, không phải tôi"

Phản hồi nhanh hơn phản hồi kỹ: typecheck + unit test trong ~2 phút cho mỗi push; bộ E2E dài chạy trên PR và main.

## Đồng nhất môi trường

Cùng artifact, khác config — đó là hợp đồng. Nếu staging thiếu một dịch vụ mà prod có, bạn sẽ phát hiện sự khác biệt này trong production. Giữ các môi trường giống nhau về cấu trúc; biến config là độ chênh duy nhất (và ghi chép từng biến).""".replace('".replace(\'\'.rstrip() + " \\"\\"\\"," " \\"\\"\\","', ''),
)

write_lesson(
    MOD, "deploy-dns-https",
    "Deployment, DNS, and HTTPS",
    "How a URL becomes your server: DNS resolution, TLS handshakes, release strategies, and rollbacks that don't panic.",
    20,
    """## What happens when someone types your URL

1. **DNS** — the browser asks the resolver for `app.example.com`; the resolver walks root → TLD → authoritative nameserver → returns an IP (cached along the way, per TTL).
2. **TCP + TLS** — connect to port 443; the TLS handshake verifies the server's certificate (issued by a CA the browser trusts) and establishes encryption. This is HTTPS: privacy *and* proof you're talking to the right server.
3. **HTTP request** — hits a load balancer → your server (or CDN edge, which answers before reaching you).

Certificates renew automatically these days (Let's Encrypt, platform-managed); the residual skill is diagnosing expiry mistakes and mixed-content warnings (https page loading http assets — blocked).

## Release strategies

- **Rolling** — replace instances a few at a time; old and new serve simultaneously. Default in most platforms.
- **Blue-green** — two identical environments; flip the router from blue to green. Instant rollback = flip back.
- **Canary** — route 1% of traffic to the new version, watch metrics, ramp up. Catches what tests missed, on 1% of users instead of all of them.
- **Feature flags** (previous lesson) decouple the code deploy from the feature's release.

Choose by blast radius: flags for features, canary for risky refactors, rolling for the everyday.

## Rollback: the skill that buys calm

Deploys fail. The professional move is a **revert deploy** — redeploy the previous artifact — not a hotfix under pressure. Requirements: artifacts are immutable and retrievable (previous lesson), migrations are forward-compatible with the previous code version (expand/contract!), and rollback is rehearsed. "We can't roll back because the migration broke compatibility" is the sentence that turns an outage into a long outage.

## Databases in the deploy story

Schema migrations ride the same pipeline with extra care: **migrate before** the new code starts (or with expand/contract, any time), migrations must be idempotent-safe with the tooling's lock, and destructive changes wait until no running version needs the old column. Most deploy incidents are migration incidents.""",
    "Triển khai, DNS, và HTTPS",
    "Một URL trở thành server của bạn thế nào: phân giải DNS, bắt tay TLS, chiến lược phát hành, và rollback không hoảng loạn.",
    """## Điều gì xảy ra khi ai đó gõ URL của bạn

1. **DNS** — trình duyệt hỏi resolver về `app.example.com`; resolver đi root → TLD → nameserver có thẩm quyền → trả về một IP (được cache dọc đường, theo TTL).
2. **TCP + TLS** — kết nối tới cổng 443; bắt tay TLS xác minh chứng chỉ của server (do một CA mà trình duyệt tin) và thiết lập mã hóa. Đó là HTTPS: riêng tư *và* bằng chứng bạn đang nói chuyện đúng server.
3. **HTTP request** — chạm load balancer → server của bạn (hoặc mép CDN, nơi trả lời trước khi tới bạn).

Giờ đây chứng chỉ tự gia hạn (Let's Encrypt, nền tảng quản lý); kỹ năng còn lại là chẩn đoán lỗi hết hạn và cảnh báo mixed-content (trang https tải tài nguyên http — bị chặn).

## Chiến lược phát hành

- **Rolling** — thay thế từng nhóm instance; bản cũ và mới phục vụ đồng thời. Mặc định của đa số nền tảng.
- **Blue-green** — hai môi trường giống hệt nhau; lật router từ blue sang green. Rollback tức thì = lật ngược lại.
- **Canary** — định tuyến 1% traffic sang bản mới, theo dõi metric, tăng dần. Bắt được thứ test bỏ sót, trên 1% người dùng thay vì tất cả.
- **Feature flag** (bài trước) tách deploy code khỏi release tính năng.

Chọn theo bán kính sát thương: flag cho tính năng, canary cho refactor rủi ro, rolling cho ngày thường.

## Rollback: kỹ năng mua lại sự bình tĩnh

Deploy thất bại là chuyện thường. Nước đi chuyên nghiệp là **revert deploy** — triển khai lại artifact trước đó — chứ không phải hotfix dưới áp lực. Điều kiện: artifact bất biến và lấy lại được (bài trước), migration tương thích về trước với phiên bản code cũ (expand/contract!), và rollback được diễn tập. "Không rollback được vì migration phá tương thích" là câu biến một sự cố thành một sự cố dài.

## Database trong câu chuyện deploy

Schema migration đi cùng pipeline với sự cẩn trọng thêm: **migrate trước** khi code mới khởi động (hoặc với expand/contract, bất cứ lúc nào), migration phải an toàn idempotent với lock của công cụ, và các thay đổi phá hủy chờ đến khi không còn phiên bản đang chạy nào cần cột cũ. Đa số sự cố deploy là sự cố migration.""",
)

write_lesson(
    MOD, "observability",
    "Logging, Monitoring, Errors",
    "You can't fix what you can't see: structured logs, metrics that matter, error tracking, and alerts that don't cry wolf.",
    20,
    """Production code fails in ways your laptop never showed you. Observability is the instrumentation that turns "it's broken" into "here's why."

## Logs: structured or useless

```js
log.info("task.created", { taskId, userId, durationMs });
```

Structured (JSON) logs beat strings: fields are searchable ("all task.created slower than 500ms"), correlatable (the same requestId through every service), and cheap to parse. Every request gets a **request id** (generated at the edge, passed through, echoed in responses) — the thread you pull to reconstruct any user's session from logs.

Log levels with discipline: `error` (needs a human, today), `warn` (degraded but working), `info` (business events), `debug` (verbose, off in prod by default). And **never log secrets** — tokens, passwords, full request bodies: logs are readable by more people than you think and live longer than you expect.

## Metrics: the vital signs

Four golden signals: **latency** (how long, percentiles p50/p95/p99 — averages lie), **traffic** (requests/sec), **errors** (rate of failures), **saturation** (CPU, memory, queue depth). Track them per endpoint; alert on symptoms users feel (error rate, p99 latency), not on causes you guess.

## Error tracking: the stack trace arrives alone

Tools (Sentry, GlitchTip) capture client and server exceptions with stack traces, releases, and breadcrumbs. This is where source maps (build lesson) pay off. Group by fingerprint — 1,000 users hitting the same bug is *one* issue with a count, not 1,000 alerts.

## Alerting without crying wolf

Every alert should be: **actionable** (a human can do something now), **urgent** (ignore it and users suffer), and **unique** (not duplicated by three other alerts). Everything else goes in a dashboard. On-call sanity: if a week of alerts produces no real incidents, the thresholds are wrong — tune or the team learns to ignore alerts, which is worse than having none.

## Health checks

`GET /healthz` returns 200 when the process can serve (fast, no DB call) and `GET /readyz` returns 200 when it can serve *correctly* (dependencies reachable). Load balancers and platforms route by these; getting them wrong means receiving traffic you can't handle or being marked dead while healthy.""",
    "Logging, monitoring, lỗi",
    "Không thể sửa thứ bạn không nhìn thấy: log có cấu trúc, metric quan trọng, theo dõi lỗi, và alert không giật gân.",
    """Code production hỏng theo cách laptop của bạn chưa từng cho thấy. Observability là bộ dụng cụ đo lường biến "nó hỏng rồi" thành "đây là lý do".

## Log: có cấu trúc hoặc vô dụng

```js
log.info("task.created", { taskId, userId, durationMs });
```

Log có cấu trúc (JSON) hơn hẳn chuỗi: trường tìm kiếm được ("mọi task.created chậm hơn 500ms"), liên kết được (cùng requestId xuyên qua mọi dịch vụ), và rẻ để parse. Mỗi request có một **request id** (sinh ở mép, truyền xuyên suốt, phản hồi lại trong response) — sợi chỉ bạn kéo để dựng lại phiên của bất kỳ người dùng nào từ log.

Mức log có kỷ luật: `error` (cần con người, hôm nay), `warn` (giảm Chất lượng nhưng vẫn chạy), `info` (sự kiện nghiệp vụ), `debug` (chi tiết, mặc định tắt ở prod). Và **không bao giờ log secret** — token, mật khẩu, body request đầy đủ: log được nhiều người đọc hơn bạn nghĩ và sống lâu hơn bạn tưởng.

## Metric: dấu hiệu sinh tồn

Bốn tín hiệu vàng: **độ trễ** (bao lâu, phân vị p50/p95/p99 — trung bình nói dối), **lưu lượng** (request/giây), **lỗi** (tỷ lệ thất bại), **bão hòa** (CPU, bộ nhớ, chiều sâu hàng đợi). Theo dõi theo từng endpoint; alert trên triệu chứng người dùng cảm nhận (tỷ lệ lỗi, độ trễ p99), không phải trên nguyên nhân bạn đoán.

## Theo dõi lỗi: stack trace tự đến

Công cụ (Sentry, GlitchTip) bắt exception client và server kèm stack trace, release, và breadcrumb. Đây là chỗ source map (bài build) trả công. Gom theo fingerprint — 1,000 người dùng đụng cùng một bug là *một* issue kèm số đếm, không phải 1,000 alert.

## Alert không giật gân

Mỗi alert phải: **có thể hành động** (con người làm được gì đó ngay), **khẩn cấp** (bỏ qua thì người dùng khổ), và **duy nhất** (không bị ba alert khác trùng lặp). Thứ còn lại cho vào dashboard. Sức khỏe on-call: nếu một tuần alert không tạo ra sự cố thật nào, ngưỡng sai — tinh chỉnh, nếu không team sẽ học cách phớt lờ alert, điều tệ hơn không có alert.

## Health check

`GET /healthz` trả 200 khi tiến trình có thể phục vụ (nhanh, không gọi DB) và `GET /readyz` trả 200 khi có thể phục vụ *đúng* (phụ thuộc với tới được). Load balancer và nền tảng định tuyến theo các endpoint này; cấu hình sai nghĩa là nhận traffic bạn không gánh nổi, hoặc bị đánh dấu chết trong khi khỏe.""",
)

write_lesson(
    MOD, "cicd-loop",
    "CI/CD: The Shipping Loop",
    "Every push verified automatically; every merge deployable. The loop that makes shipping boring — which is the goal.",
    18,
    """## CI: continuous integration

Every push runs the gate automatically:

```yaml
# .github/workflows/ci.yml (conceptual)
on: push
jobs:
  verify:
    steps:
      - checkout, install (cached)
      - typecheck      # seconds
      - lint           # seconds
      - unit tests     # a minute
      - build          # proves it compiles
```

Branch protection makes it law: PRs require green CI + review before merge. The cultural shift is the point — "it works on my machine" stops being an argument when the machine is CI.

## CD: continuous delivery/deployment

- **Delivery** — every merge produces a verified, deployable artifact (deploy is a button)
- **Deployment** — every merge *deploys* to production automatically

Deployment on merge is the highest-trust setup; it's earned by the test pyramid (module 7), staged rollouts (previous lesson), and instant rollback. You don't start there; you grow into it.

## The pipeline anatomy

```text
push → [typecheck, lint, unit]  → PR merge →
       [build artifact, hash, scan] →
       deploy staging → [E2E, smoke tests] →
       deploy prod (canary/rolling) → [metrics watch] → done
```

Fast first, slow later: developers get typecheck feedback in minutes; the heavyweight gates run before prod, not before every commit.

## Secrets in CI

CI systems hold powerful credentials (deploy keys, cloud tokens) — a leaked CI token is a production breach. Store them in the platform's secret store (never in YAML), scope them narrowly (deploy key ≠ admin key), rotate them, and pin third-party actions to digests where the platform allows.

## The boring goal

The measure of a mature pipeline is *unremarkable deploys*: multiple per day, none worth mentioning in standup. Every manual step removed is one less 11pm mistake. When deploys are boring, you ship smaller changes, which fail smaller, which makes deploys even more boring — the loop compounds in your favor.""",
    "CI/CD: Vòng lặp vận chuyển",
    "Mỗi push được xác minh tự động; mỗi lần merge sẵn sàng triển khai. Vòng lặp khiến việc ship trở nên tầm thường — và đó chính là mục tiêu.",
    """## CI: tích hợp liên tục

Mỗi push chạy cổng kiểm tra tự động:

```yaml
# .github/workflows/ci.yml (khái niệm)
on: push
jobs:
  verify:
    steps:
      - checkout, install (có cache)
      - typecheck      # vài giây
      - lint           # vài giây
      - unit test      # một phút
      - build          # chứng minh biên dịch được
```

Branch protection biến nó thành luật: PR yêu cầu CI xanh + review trước khi merge. Sự chuyển biến văn hóa mới là điểm mấu chốt — "trên máy tôi chạy mà" ngừng là lập luận khi cái máy đó là CI.

## CD: delivery/deployment liên tục

- **Delivery** — mỗi merge tạo ra một artifact đã xác minh, có thể triển khai (deploy là một nút bấm)
- **Deployment** — mỗi merge *tự động triển khai* lên production

Deploy ngay khi merge là cấu hình tin cậy cao nhất; nó được giành bằng kim tự tháp test (module 7), phát hành theo giai đoạn (bài trước), và rollback tức thì. Bạn không bắt đầu ở đó; bạn lớn dần lên.

## Giải phẫu pipeline

```text
push → [typecheck, lint, unit]  → merge PR →
       [build artifact, hash, scan] →
       deploy staging → [E2E, smoke test] →
       deploy prod (canary/rolling) → [theo dõi metric] → xong
```

Nhanh trước, chậm sau: lập trình viên nhận phản hồi typecheck trong vài phút; các cổng nặng chạy trước prod, không phải trước mỗi commit.

## Secret trong CI

Hệ thống CI giữ credential quyền lực (deploy key, cloud token) — một token CI bị lộ là một vụ xâm nhập production. Lưu trong secret store của nền tảng (không bao giờ trong YAML), giới hạn phạm vi hẹp (deploy key ≠ admin key), xoay vòng chúng, và ghim action bên thứ ba theo digest khi nền tảng cho phép.

## Mục tiêu tầm thường

Thước đo của pipeline trưởng thành là *deploy không đáng kể*: nhiều lần mỗi ngày, không lần nào cần nhắc trong standup. Mỗi bước thủ công bị xóa là một lỗi 11 giờ đêm bớt đi. Khi deploy tầm thường, bạn ship thay đổi nhỏ hơn, hỏng nhỏ hơn, khiến deploy càng tầm thường hơn — vòng lặp cộng hưởng về phía bạn.""",
)

write_checkpoint(
    MOD,
    "prod-checkpoint",
    "Checkpoint: Release Engineer",
    "Prove the production instincts: environment discipline, release strategy selection, incident triage, and honest health checks.",
    20,
    """This checkpoint grades release engineering judgment in runnable form — the decisions that separate "it deployed" from "it deployed safely and we can prove it." ...""",
    "Kiểm tra kiến thức: Kỹ sư phát hành",
    "Chứng minh bản năng production: kỷ luật môi trường, chọn chiến lược phát hành, phân loại sự cố, và health check trung thực.",
    """Checkpoint này chấm phán đoán kỹ thuật phát hành ở dạng chạy được — những quyết định phân biệt "đã deploy" với "đã deploy an toàn và chứng minh được". ...""",
    {
        "id": "i2-prod-checkpoint",
        "title": "Release Desk",
        "prompt": "Write THREE functions. 1) `envVerdict(config)` — config is { secretsInEnv: bool, validated: bool, devBuild: bool }. Return \"ready\" when secretsInEnv AND validated AND NOT devBuild; \"unsafe-secrets\" when secretsInEnv is false; \"invalid-config\" when validated is false (when both wrong: \"unsafe-secrets\" first); \"dev-build\" for the devBuild case. 2) `releaseStrategy(risk, users)` — risk \"low\" => \"rolling\"; risk \"high\" && users > 10000 => \"canary\"; risk \"high\" => \"blue-green\". 3) `triage(alert)` — alert is { kind, actionable, urgent }; return \"page\" when actionable && urgent, \"ticket\" when actionable only, \"dashboard\" otherwise (noise).",
        "difficulty": "intermediate",
        "level": "checkpoint",
        "boilerplate": "function envVerdict(config) {\n  // your code\n}\n\nfunction releaseStrategy(risk, users) {\n  // your code\n}\n\nfunction triage(alert) {\n  // your code\n}\n",
        "tests": [
            {
                "name": "environment readiness gate",
                "code": "const fn = new Function(code + \"\\nreturn { envVerdict, releaseStrategy, triage };\");\nconst { envVerdict } = fn();\nif (envVerdict({ secretsInEnv: true, validated: true, devBuild: false }) !== \"ready\") throw new Error(\"Fully compliant => ready.\");\nif (envVerdict({ secretsInEnv: false, validated: true, devBuild: false }) !== \"unsafe-secrets\") throw new Error(\"Secrets in repo first.\");\nif (envVerdict({ secretsInEnv: true, validated: false, devBuild: false }) !== \"invalid-config\") throw new Error(\"Unvalidated config fails.\");\nif (envVerdict({ secretsInEnv: true, validated: true, devBuild: true }) !== \"dev-build\") throw new Error(\"Dev build in prod.\");",
                "hint": "Order: secrets, validated, build.",
            },
            {
                "name": "release strategy by blast radius",
                "code": "const fn = new Function(code + \"\\nreturn { envVerdict, releaseStrategy, triage };\");\nconst { releaseStrategy } = fn();\nif (releaseStrategy(\"low\", 50) !== \"rolling\") throw new Error(\"Everyday deploys roll.\");\nif (releaseStrategy(\"high\", 20000) !== \"canary\") throw new Error(\"Big audience, high risk => canary.\");\nif (releaseStrategy(\"high\", 500) !== \"blue-green\") throw new Error(\"High risk, small audience => blue-green.\");",
                "hint": "Low risk short-circuits; then audience size picks between canary and blue-green.",
            },
            {
                "name": "alerts triage honestly",
                "code": "const fn = new Function(code + \"\\nreturn { envVerdict, releaseStrategy, triage };\");\nconst { triage } = fn();\nif (triage({ kind: \"5xx-spike\", actionable: true, urgent: true }) !== \"page\") throw new Error(\"Real incident => page.\");\nif (triage({ kind: \"slow-query\", actionable: true, urgent: false }) !== \"ticket\") throw new Error(\"Fixable, not urgent => ticket.\");\nif (triage({ kind: \"noise\", actionable: false, urgent: false }) !== \"dashboard\") throw new Error(\"Noise => dashboard.\");",
                "hint": "Two booleans, three outcomes.",
            },
        ],
    },
    {
        "id": "i2-prod-checkpoint",
        "title": "Bàn phát hành",
        "prompt": "Viết BA hàm. 1) `envVerdict(config)` — config là { secretsInEnv: bool, validated: bool, devBuild: bool }. Trả về \"ready\" khi secretsInEnv VÀ validated VÀ KHÔNG devBuild; \"unsafe-secrets\" khi secretsInEnv là false; \"invalid-config\" khi validated là false (khi cả hai sai: \"unsafe-secrets\" trước); \"dev-build\" cho trường hợp devBuild. 2) `releaseStrategy(risk, users)` — risk \"low\" => \"rolling\"; risk \"high\" && users > 10000 => \"canary\"; risk \"high\" => \"blue-green\". 3) `triage(alert)` — alert là { kind, actionable, urgent }; trả về \"page\" khi actionable && urgent, \"ticket\" khi chỉ actionable, \"dashboard\" trong các trường hợp còn lại (noise).",
        "tests": [
            {"name": "cổng sẵn sàng môi trường", "hint": "Thứ tự: secrets, validated, build."},
            {"name": "chiến lược phát hành theo bán kính sát thương", "hint": "Rủi ro thấp chặn ngắn; rồi quy mô khán giả chọn giữa canary và blue-green."},
            {"name": "alert được phân loại trung thực", "hint": "Hai boolean, ba kết quả."},
        ],
    },
)

print("Module 12 lessons + checkpoint written.")
