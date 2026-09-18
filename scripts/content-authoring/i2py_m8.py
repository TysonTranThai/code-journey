#!/usr/bin/env python3
"""Module 8: web-performance — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint

MOD = "web-performance"

write_module(
    MOD,
    "Web Performance",
    "Performance as measurement, not folklore: the rendering pipeline, the network waterfall, and the diagnose-first discipline behind Core Web Vitals.",
    "Hiệu năng Web",
    "Hiệu năng là phép đo, không phải giai thoại: pipeline render, waterfall mạng, và kỷ luật chẩn-đoán-trước đằng sau Core Web Vitals.",
    ["rendering-pipeline", "network-waterfall", "assets-and-caching", "js-execution-cost", "measure-optimize-loop", "perf-checkpoint"],
    ["render-practice", "waterfall-practice", "budget-practice", "slow-page-practice"],
)

write_lesson(
    MOD, "rendering-pipeline",
    "How Browsers Render (and Where It Janks)",
    "Parse → style → layout → paint → composite. Knowing which step your code triggers tells you what it costs.",
    20,
    """Every visual change walks a pipeline. The step that re-runs determines the cost.

## The pipeline

1. **Parse** — HTML becomes the DOM; CSS becomes the CSSOM. Scripts can block parsing (hence `defer`/`async`).
2. **Style** — compute which CSS rules apply to each element (the "Recalculate Style" you see in DevTools).
3. **Layout** — geometry: where every element sits, how big it is. A change to *size or position* invalidates layout.
4. **Paint** — fill pixels: text, colors, shadows, images.
5. **Composite** — GPU-assembles painted layers. Cheapest of all.

Cost ordering matters: a `transform` or `opacity` change can stop at composite (cheap). A `width`/`top`/`font-size` change walks style→layout→paint (expensive — it's on every element it affects, and children). `color`/`background` skips layout but still paints.

## Jank and the frame budget

Browsers aim for 60fps — every frame gets a **16.7ms budget** (10ms on 120Hz displays). A script task that runs 200ms freezes that many frames: the page visibly stutters. Long tasks come from big loops, huge DOM mutations, or layout thrashing.

## Layout thrashing: the classic performance bug

```js
// BAD: read-write-read-write forces layout every iteration
for (const card of cards) {
  const h = card.offsetHeight;   // READ — forces layout (previous write is pending)
  card.style.height = h + 20 + "px";  // WRITE — invalidates layout
}
```

The fix is batching: **read everything, then write everything**.

```js
const heights = cards.map((c) => c.offsetHeight); // all reads
cards.forEach((c, i) => { c.style.height = heights[i] + 20 + "px"; }); // all writes
```

## What actually moves the needle

- `visibility`/`opacity` transitions instead of size animations
- `content-visibility: auto` for long off-screen sections
- Fewer, larger DOM mutations (DocumentFragment, one reflow)
- The Composite-only properties (`transform`, `opacity`) for animation""",
    "Trình duyệt render thế nào (và nơi bị giật)",
    "Parse → style → layout → paint → composite. Biết code của mình chạm bước nào là biết nó tốn bao nhiêu.",
    """Mọi thay đổi hiển thị đều đi qua một pipeline. Bước bị chạy lại quyết định cái giá.

## Pipeline

1. **Parse** — HTML thành DOM; CSS thành CSSOM. Script có thể chặn parsing (nên có `defer`/`async`).
2. **Style** — tính xem quy tắc CSS nào áp cho từng phần tử ("Recalculate Style" mà bạn thấy trong DevTools).
3. **Layout** — hình học: mọi phần tử ngồi đâu, to cỡ nào. Đổi *kích thước hoặc vị trí* làm layout mất hiệu lực.
4. **Paint** — tô pixel: chữ, màu, bóng, ảnh.
5. **Composite** — GPU lắp các lớp đã tô. Rẻ nhất trong tất cả.

Thứ tự chi phí quan trọng: đổi `transform` hoặc `opacity` có thể dừng ở composite (rẻ). Đổi `width`/`top`/`font-size` đi hết style→layout→paint (đắt — áp cho mọi phần tử bị ảnh hưởng và cả con của chúng). `color`/`background` bỏ qua layout nhưng vẫn phải paint.

## Jank và ngân sách khung hình

Trình duyệt nhắm 60fps — mỗi khung có **ngân sách 16.7ms** (10ms trên màn 120Hz). Một script task chạy 200ms đóng băng bấy nhiêu khung: trang giật thấy rõ. Long task đến từ vòng lặp lớn, đột biến DOM khổng lồ, hoặc layout thrashing.

## Layout thrashing: bug hiệu năng kinh điển

```js
// XẤU: đọc-ghi-đọc-ghi ép layout mỗi vòng lặp
for (const card of cards) {
  const h = card.offsetHeight;   // ĐỌC — ép layout (ghi trước đó còn treo)
  card.style.height = h + 20 + "px";  // GHI — vô hiệu hóa layout
}
```

Cách sửa là gom lô: **đọc hết, rồi ghi hết**.

```js
const heights = cards.map((c) => c.offsetHeight); // đọc hết
cards.forEach((c, i) => { c.style.height = heights[i] + 20 + "px"; }); // ghi hết
```

## Thứ gì thực sự tạo khác biệt

- Chuyển động bằng `visibility`/`opacity` thay vì animate kích thước
- `content-visibility: auto` cho các đoạn dài nằm ngoài màn hình
- Ít đột biến DOM hơn, mỗi lần lớn hơn (DocumentFragment, một reflow duy nhất)
- Các thuộc tính Composite-only (`transform`, `opacity`) cho animation""",
)

write_lesson(
    MOD, "network-waterfall",
    "The Network Waterfall",
    "Requests are a timeline, not a list: DNS, connection, TTFB, download — and what your page blocks on.",
    20,
    """A page load is a choreography of requests. The Network panel draws it as a waterfall; reading it is a core performance skill.

## Anatomy of one request

Each bar stacks phases: **DNS lookup** (name → IP; cached after first), **TCP connect** (+TLS for https), **Time To First Byte** (server thinking), **Content Download** (payload arriving). Long TTFB = slow server (backend problem). Long download = big payload (frontend problem). Connection setup on every request = you're not reusing connections.

## The critical path

The browser can't render until it has HTML. Inside the HTML:

- `<link rel="stylesheet">` — CSS blocks render (correct choice for above-the-fold styles!)
- `<script src>` (no attribute) — pauses HTML parsing entirely while downloading AND executing
- `<script defer>` — downloads in parallel, executes after parse, before DOMContentLoaded
- `<script async>` — downloads in parallel, executes whenever ready (analytics, not app code)
- `<img loading="lazy">` — off-screen images wait until near the viewport

The default professional setup for app scripts: `defer` in the head. Render-blocking CSS: keep it small; split by route when a stylesheet grows.

## Water — the order of operations

The waterfall shows *dependency chains*: HTML → discovered CSS/JS → fonts → images. Chains are slow because each hop waits. Attack them by: `preload` for assets you know you'll need in the first second (the hero image, the main font), `font-display: swap` so text renders before the font arrives, and inlining critical CSS so first paint doesn't wait on a round trip.

## Compression and transport

- **gzip/brotli** on text assets: usually 60–80% smaller. Check the response's `Content-Encoding` — if it's missing on your JS, that's free performance on the table.
- **HTTP caching**: `Cache-Control` headers decide whether returning visitors re-download anything. Hashed filenames (`app.a83f2.js`) let you cache "forever" and still ship updates — change the file, change the hash.
- **HTTP/2+**: multiplexes many requests over one connection — the old advice "bundle everything into one request" is obsolete; the modern advice is "don't have 300 requests either." """,
    "Waterfall mạng",
    "Request là một dòng thời gian, không phải một danh sách: DNS, kết nối, TTFB, tải về — và trang của bạn chặn ở đâu.",
    """Một lần tải trang là biên đạo của nhiều request. Panel Network vẽ nó thành waterfall; đọc được nó là kỹ năng hiệu năng cốt lõi.

## Giải phẫu một request

Mỗi thanh cỏn nhiều pha: **DNS lookup** (tên → IP; được cache sau lần đầu), **TCP connect** (+TLS cho https), **Time To First Byte** (server đang nghĩ), **Content Download** (payload đang về). TTFB dài = server chậm (bài toán backend). Download dài = payload nặng (bài toán frontend). Mỗi request đều phải bắt kết nối mới = bạn không tái sử dụng kết nối.

## Đường truyền tới hạn

Trình duyệt không render nổi khi chưa có HTML. Bên trong HTML:

- `<link rel="stylesheet">` — CSS chặn render (đúng đắn cho style phần nhìn thấy đầu tiên!)
- `<script src>` (không attribute) — dừng hẳn việc parse HTML để tải VÀ chạy
- `<script defer>` — tải song song, chạy sau khi parse xong, trước DOMContentLoaded
- `<script async>` — tải song song, chạy khi nào sẵn sàng (analytics, không phải code chính)
- `<img loading="lazy">` — ảnh ngoài màn hình chờ đến khi gần viewport

Cấu hình chuyên nghiệp mặc định cho script ứng dụng: `defer` trong head. CSS chặn render: giữ nhỏ; tách theo route khi stylesheet phình to.

## Nước — thứ tự vận hành

Waterfall cho thấy *chuỗi phụ thuộc*: HTML → CSS/JS được phát hiện → font → ảnh. Chuỗi chậm vì mỗi chặng phải chờ. Tấn công chúng bằng: `preload` cho tài sản bạn biết là cần trong giây đầu (ảnh hero, font chính), `font-display: swap` để chữ render trước khi font tới, và nhúng critical CSS để lần vẽ đầu không phải chờ một chuyến khứ hồi.

## Nén và vận chuyển

- **gzip/brotli** trên tài sản văn bản: thường nhỏ hơn 60–80%. Kiểm tra `Content-Encoding` của response — nếu JS của bạn thiếu nó, đó là hiệu năng miễn phí đang nằm trên bàn.
- **HTTP caching**: header `Cache-Control` quyết định khách quay lại có phải tải lại gì không. Tên file có hash (`app.a83f2.js`) cho phép cache "mãi mãi" mà vẫn ship được bản cập nhật — đổi file là đổi hash.
- **HTTP/2+**: ghép nhiều request trên một kết nối — lời khuyên cũ "gom tất cả thành một request" đã lỗi thời; lời khuyên hiện đại là "đừng có 300 request cũng vậy." """
)

write_lesson(
    MOD, "assets-and-caching",
    "Assets: Images, Fonts, Caching",
    "The payload is usually the problem: oversized images, blocking fonts, and caches you configured wrong.",
    18,
    """When a page is slow, images are the suspect in ~70% of cases. Then fonts. Then your JS.

## Images: the biggest lever

- **Right format**: SVG for icons/logos (resolution-independent, tiny), WebP/AVIF for photos (30–50% smaller than JPEG at equal quality), PNG only when transparency matters and SVG can't do it.
- **Right size**: serving a 3000px image into a 400px slot wastes ~90% of its bytes. `srcset` + `sizes` let the browser pick:

```html
<img
  src="hero-800.webp"
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1600.webp 1600w"
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="..."/>
```

- **Lazy-load** everything below the fold: `loading="lazy"`. NEVER lazy-load the hero/LCP image — that makes the page *feel* slower.
- **Explicit dimensions** (`width`/`height` attributes) so layout doesn't jump when images arrive (CLS — next lesson).

## Fonts

Fonts are render-blocking text. `font-display: swap` shows fallback text immediately and swaps when the real font lands. `preload` your primary font (the one the headline uses) — but only that one. Subset fonts (Vietnamese needs the Vietnamese subset!) — shipping 5 weights × full Unicode is megabytes of self-inflicted damage.

## Caching strategy

The `Cache-Control` header is a contract:

```text
Cache-Control: max-age=31536000, immutable   # hashed assets: cache a year
Cache-Control: no-cache                      # revalidate before use (HTML)
Cache-Control: no-store                      # never cache (secrets, personal data)
```

The standard scheme: HTML = `no-cache` (always fresh), JS/CSS/images with content hashes = `immutable` for a year. Changing the code changes the hash, which changes the URL, which bypasses the cache — correctness and speed coexist.

## Third-party scripts cost more than they look

Analytics, chat widgets, tag managers: each is a script download + execute + often its own requests. Every one delays or competes with your app. Budget them (next lessons), load them `async`, and audit them quarterly — dead tags are routine.""",
    "Tài sản: Ảnh, font, caching",
    "Payload thường là thủ phạm: ảnh khổng lồ, font chặn render, và cache bạn cấu hình sai.",
    """Khi một trang chậm, ảnh là nghi phạm trong ~70% trường hợp. Rồi đến font. Rồi mới đến JS của bạn.

## Ảnh: đòn bẩy lớn nhất

- **Định dạng đúng**: SVG cho icon/logo (độc lập độ phân giải, siêu nhỏ), WebP/AVIF cho ảnh chụp (nhỏ hơn JPEG 30–50% ở cùng chất lượng), PNG chỉ khi cần trong suốt mà SVG không làm được.
- **Kích thước đúng**: đưa ảnh 3000px vào khung 400px phí ~90% byte. `srcset` + `sizes` để trình duyệt tự chọn:

```html
<img
  src="hero-800.webp"
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1600.webp 1600w"
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="..."/>
```

- **Lazy-load** mọi thứ dưới màn hình đầu: `loading="lazy"`. TUYỆT ĐỐI không lazy-load ảnh hero/LCP — làm trang *cảm giác* chậm hơn.
- **Khai báo kích thước tường minh** (attribute `width`/`height`) để layout không nhảy khi ảnh về (CLS — bài sau).

## Font

Font là văn bản chặn render. `font-display: swap` hiển thị chữ fallback ngay lập tức và hoán đổi khi font thật về. `preload` font chính (cái tiêu đề dùng) — nhưng chỉ cái đó thôi. Subset font (tiếng Việt cần bộ subset Vietnamese!) — ship 5 weight × full Unicode là tự gây thương tích tính bằng megabyte.

## Chiến lược caching

Header `Cache-Control` là một hợp đồng:

```text
Cache-Control: max-age=31536000, immutable   # tài sản có hash: cache một năm
Cache-Control: no-cache                      # xác nhận lại trước khi dùng (HTML)
Cache-Control: no-store                      # không bao giờ cache (bí mật, dữ liệu cá nhân)
```

Sơ đồ chuẩn: HTML = `no-cache` (luôn mới), JS/CSS/ảnh có content hash = `immutable` một năm. Đổi code là đổi hash, là đổi URL, là né cache — đúng đắn và nhanh cùng tồn tại.

## Script bên thứ ba đắt hơn vẻ ngoài

Analytics, chat widget, tag manager: mỗi cái là tải script + chạy + thường có request riêng. Mỗi cái trì hoãn hoặc tranh chấp tài nguyên với ứng dụng. Hãy áp ngân sách (bài sau), tải `async`, và rà soát định kỳ — tag chết là chuyện thường.""",
)

write_lesson(
    MOD, "js-execution-cost",
    "JavaScript Execution Cost",
    "Parsing, executing, and memory: why shipping less JS is the performance strategy, and how to find your own dead weight.",
    18,
    """JavaScript costs three times: download (bytes), parse+compile (CPU on the main thread), and execute (CPU, every run). Most teams only think about the first.

## The main thread is single

While your JS runs, the page can't respond. A 300ms task = 300ms of dead UI. The fixes:

- **Break work up**: chunk a big loop with `await new Promise(r => setTimeout(r))` between chunks so input events can interleave.
- **Debounce/idle**: `requestIdleCallback` or `setTimeout` for non-urgent work (analytics flushing, preview generation).
- **Web workers** for genuinely heavy computation — they run off the main thread entirely (message-passing, no DOM).

## Shipping less JavaScript

- **Bundle analysis**: `npx vite-bundle-visualizer` (or webpack-bundle-analyzer) shows what your bundle actually contains. The usual suspects: moment.js (+locales!), lodash full import, duplicated dependencies.
- **Tree-shaking works only with ESM imports**: `import { debounce } from "lodash-es"` pulls one function; `import _ from "lodash"` pulls the world.
- **Code splitting**: route-based splitting is the easy 50% — users of `/admin` shouldn't download the checkout page's code.
- **Ship less polyfill**: target modern browsers unless your analytics say otherwise.

## Memory: leaks find slow pages

A leak = memory that will never be used again but is never released. Common JS leaks:

- Forgotten timers/listeners: a `setInterval` or `addEventListener` on an element that got removed keeps everything it closes over alive.
- Global accumulators: caches/arrays that only grow.
- Detached DOM: a variable holding a removed subtree (plus its data).

In DevTools → Memory: take a heap snapshot, interact, take another, compare. Growing "Detached" or repeatedly-growing arrays = hunting grounds. `performance.measureUserAgentSpecificMemory()` and the Memory panel make this routine rather than mystical.

## Measure, always

`performance.now()` brackets code on the main thread; DevTools Performance panel records the whole picture (script, style, layout, paint). Number first, opinion second.""",
    "Chi phí thực thi JavaScript",
    "Parse, chạy, và bộ nhớ: vì sao ship ít JS hơn là chiến lược hiệu năng, và cách tự tìm dead weight.",
    """JavaScript tốn tiền ba lần: tải về (byte), parse+compile (CPU trên main thread), và chạy (CPU, mỗi lần chạy). Đa số team chỉ nghĩ về lần đầu.

## Main thread chỉ có một

Trong lúc JS của bạn chạy, trang không phản hồi được. Task 300ms = 300ms UI chết. Các cách sửa:

- **Chia nhỏ công việc**: cắt vòng lặp lớn bằng `await new Promise(r => setTimeout(r))` giữa các mảnh để sự kiện input chen vào được.
- **Debounce/idle**: `requestIdleCallback` hoặc `setTimeout` cho việc không gấp (đẩy analytics, tạo preview).
- **Web worker** cho tính toán thực sự nặng — chạy tách khỏi main thread hoàn toàn (truyền tin nhắn, không đụng DOM).

## Ship ít JavaScript hơn

- **Phân tích bundle**: `npx vite-bundle-visualizer` (hoặc webpack-bundle-analyzer) cho thấy bundle của bạn thực sự chứa gì. Thủ phạm quen thuộc: moment.js (+locales!), lodash import nguyên con, dependency bị trùng.
- **Tree-shaking chỉ chạy với import ESM**: `import { debounce } from "lodash-es"` lấy một hàm; `import _ from "lodash"` lấy cả thế giới.
- **Code splitting**: tách theo route là 50% dễ — người dùng `/admin` không cần tải code của trang thanh toán.
- **Ship ít polyfill hơn**: nhắm trình duyệt hiện đại trừ khi analytics của bạn nói điều ngược lại.

## Bộ nhớ: leak khiến trang chậm dần

Leak = bộ nhớ không bao giờ dùng lại nhưng không bao giờ được trả. Các leak JS phổ biến:

- Timer/listener bị bỏ quên: `setInterval` hoặc `addEventListener` trên phần tử đã bị xóa giữ sống mọi thứ nó đóng bên ngoài.
- Bộ tích lũy toàn cục: cache/mảng chỉ biết lớn.
- DOM tách rời: một biến giữ cây DOM đã bị xóa (kèm dữ liệu của nó).

Trong DevTools → Memory: chụp một heap snapshot, tương tác, chụp cái nữa, so sánh. "Detached" tăng dần hoặc mảng cứ phình ra = vùng săn. `performance.measureUserAgentSpecificMemory()` và panel Memory biến việc này thành thường trình thay vì huyền bí.

## Đo, luôn luôn

`performance.now()` bọc code trên main thread; panel Performance ghi lại toàn cảnh (script, style, layout, paint). Số liệu trước, ý kiến sau.""",
)

write_lesson(
    MOD, "measure-optimize-loop",
    "Measuring: Core Web Vitals and Budgets",
    "LCP, INP, CLS — the three numbers users feel — plus performance budgets that keep you honest over time.",
    20,
    """Performance without measurement is folklore. The industry standard is Core Web Vitals — three user-perceived metrics.

## The three vitals

- **LCP (Largest Contentful Paint)** — when the main content appears. Good < 2.5s. Usually the hero image or headline block. Enemies: slow server (TTFB), render-blocking resources, lazy-loaded hero, unoptimized images.
- **INP (Interaction to Next Paint)** — worst-ish input latency across interactions. Good < 200ms. Enemies: long tasks on the main thread, giant event handlers.
- **CLS (Cumulative Layout Shift)** — how much content jumps. Good < 0.1. Enemies: images without dimensions, late-loading fonts/banners/ads, injected content above existing content.

All three are *field metrics* — measured on real users (CrUX, RUM). Lab tools (Lighthouse) approximate them for diagnosis.

## The loop

1. **Measure** in the field (or a controlled lab reproduction).
2. **Diagnose** — which phase is slow? TTFB? Download? Script? Layout? Each has a different fix; optimizing the wrong one is effort theater.
3. **Fix the biggest thing first** — one change, not seven.
4. **Re-measure.** Same tool, same conditions. Did the number move?
5. **Guard it** with a budget (below), so the win survives the next feature.

## Performance budgets

A budget is a number in CI: "the JS bundle must stay under 170KB compressed; LCP under 2.5s on a mid-tier phone." Tools (bundlesize, Lighthouse CI, size-limit) fail the build when crossed. Without a budget, performance regresses silently — every "small" script and "temporary" image wins against nobody.

Budget categories worth setting: total JS compressed, total CSS, largest image, number of third-party requests, LCP lab score. Start from the current numbers minus 20% — budgets you can't meet get ignored.

## Device and network honesty

Test on **slow devices and throttled networks** — DevTools can throttle CPU 4–6× and network to "Slow 4G". Your MacBook Pro lies to you; the median user's phone doesn't. The lab targets: mid-tier Android, 4G, cold cache.""",
    "Đo lường: Core Web Vitals và ngân sách",
    "LCP, INP, CLS — ba con số người dùng cảm nhận được — cùng ngân sách hiệu năng giữ bạn trung thực theo thời gian.",
    """Hiệu năng không có đo lường là giai thoại. Chuẩn ngành là Core Web Vitals — ba chỉ số cảm nhận của người dùng.

## Ba vitals

- **LCP (Largest Contentful Paint)** — khi nội dung chính xuất hiện. Tốt < 2.5s. Thường là ảnh hero hoặc khối tiêu đề. Kẻ thù: server chậm (TTFB), tài nguyên chặn render, hero bị lazy-load, ảnh chưa tối ưu.
- **INP (Interaction to Next Paint)** — độ trễ input xấu nhất giữa các tương tác. Tốt < 200ms. Kẻ thù: long task trên main thread, event handler khổng lồ.
- **CLS (Cumulative Layout Shift)** — nội dung nhảy bao nhiêu. Tốt < 0.1. Kẻ thù: ảnh không khai báo kích thước, font/banner/quảng cáo về muộn, nội dung chèn vào trên nội dung có sẵn.

Cả ba đều là *chỉ số thực địa* — đo trên người dùng thật (CrUX, RUM). Công cụ lab (Lighthouse) xấp xỉ chúng để chẩn đoán.

## Vòng lặp

1. **Đo** ngoài thực địa (hoặc bản tái hiện lab có kiểm soát).
2. **Chẩn đoán** — pha nào chậm? TTFB? Download? Script? Layout? Mỗi pha một cách sửa khác nhau; tối ưu sai pha là biểu diễn sức lực.
3. **Sửa cái to nhất trước** — một thay đổi, không phải bảy.
4. **Đo lại.** Cùng công cụ, cùng điều kiện. Con số có nhúc nhích không?
5. **Gát nó lại** bằng ngân sách (dưới đây), để chiến thắng sống sót qua feature kế tiếp.

## Ngân sách hiệu năng

Ngân sách là một con số trong CI: "bundle JS phải dưới 170KB đã nén; LCP dưới 2.5s trên điện thoại tầm trung." Công cụ (bundlesize, Lighthouse CI, size-limit) làm fail build khi vượt. Không có ngân sách, hiệu năng thoái trào âm thầm — mọi script "nhỏ thôi" và ảnh "tạm thời" đều thắng vì chẳng có ai cản.

Các nhóm ngân sách đáng đặt: tổng JS đã nén, tổng CSS, ảnh lớn nhất, số request bên thứ ba, điểm LCP lab. Bắt đầu từ số hiện tại trừ 20% — ngân sách không đạt được sẽ bị bỏ qua.

## Trung thực về thiết bị và mạng

Test trên **thiết bị chậm và mạng bị tiết lưu** — DevTools có thể tiết lưu CPU 4–6× và mạng về "Slow 4G". MacBook Pro của bạn nói dối; điện thoại của người dùng đa số thì không. Mục tiêu lab: Android tầm trung, 4G, cache lạnh.""",
)

write_checkpoint(
    MOD,
    "perf-checkpoint",
    "Checkpoint: Performance Diagnosis",
    "Prove the measurement mindset: classify costs by pipeline phase, read a waterfall, and pick fixes that match bottlenecks.",
    20,
    """This checkpoint grades performance *reasoning* in runnable form — matching costs to pipeline phases, computing budgets, and choosing the right fix for the right symptom, exactly as you'll do against a real page.""",
    "Kiểm tra kiến thức: Chẩn đoán hiệu năng",
    "Chứng minh tư duy đo lường: phân loại chi phí theo pha pipeline, đọc waterfall, và chọn cách sửa khớp với điểm nghẽn.",
    """Checkpoint này chấm *lập luận* hiệu năng ở dạng chạy được — khớp chi phí với pha pipeline, tính ngân sách, và chọn cách sửa đúng cho đúng triệu chứng, đúng như bạn sẽ làm với một trang thật.""",
    {
        "id": "i2-perf-checkpoint",
        "title": "Performance Clinic",
        "prompt": "Write THREE functions. 1) `phaseOf(prop)` — map a CSS/JS property to its cheapest affected pipeline phase: \"transform\" and \"opacity\" => \"composite\"; \"color\", \"background\", \"box-shadow\" => \"paint\"; \"width\", \"height\", \"top\", \"left\", \"font-size\" => \"layout\"; unknown => \"style\". 2) `budgetVerdict(actual, limit)` — return \"ok\" when actual <= limit, \"over\" when over by up to 10% (limit * 1.1), else \"fail\". 3) `pickFix(symptom)` — map symptoms to fixes: \"slow-ttfb\" => \"server\", \"huge-image\" => \"image-optimization\", \"long-task\" => \"chunking\", \"layout-shift\" => \"dimensions\", \"render-blocking-css\" => \"critical-css\", unknown => \"profile-first\".",
        "difficulty": "intermediate",
        "level": "checkpoint",
        "boilerplate": "function phaseOf(prop) {\n  // your code\n}\n\nfunction budgetVerdict(actual, limit) {\n  // your code\n}\n\nfunction pickFix(symptom) {\n  // your code\n}\n",
        "tests": [
            {
                "name": "classifies pipeline costs correctly",
                "code": "const fn = new Function(code + \"\\nreturn { phaseOf, budgetVerdict, pickFix };\");\nconst { phaseOf } = fn();\nif (phaseOf(\"transform\") !== \"composite\") throw new Error(\"transform stops at composite.\");\nif (phaseOf(\"opacity\") !== \"composite\") throw new Error(\"opacity too.\");\nif (phaseOf(\"color\") !== \"paint\") throw new Error(\"color repaints but no layout.\");\nif (phaseOf(\"width\") !== \"layout\") throw new Error(\"width reflows.\");\nif (phaseOf(\"z-index\") !== \"style\") throw new Error(\"Unknown => style.\");",
                "hint": "Three whitelists in cost order, then the default.",
            },
            {
                "name": "budgets tolerate small overruns",
                "code": "const fn = new Function(code + \"\\nreturn { phaseOf, budgetVerdict, pickFix };\");\nconst { budgetVerdict } = fn();\nif (budgetVerdict(150, 170) !== \"ok\") throw new Error(\"Under budget => ok.\");\nif (budgetVerdict(180, 170) !== \"over\") throw new Error(\"180 <= 187 => over, not fail.\");\nif (budgetVerdict(200, 170) !== \"fail\") throw new Error(\"200 > 187 => fail.\");",
                "hint": "Two comparisons: against limit, then against limit * 1.1.",
            },
            {
                "name": "fixes match their symptoms",
                "code": "const fn = new Function(code + \"\\nreturn { phaseOf, budgetVerdict, pickFix };\");\nconst { pickFix } = fn();\nif (pickFix(\"slow-ttfb\") !== \"server\") throw new Error(\"TTFB is a server problem.\");\nif (pickFix(\"long-task\") !== \"chunking\") throw new Error(\"Long tasks want chunking.\");\nif (pickFix(\"mystery\") !== \"profile-first\") throw new Error(\"No evidence => measure first.\");",
                "hint": "A lookup object; the default is the lesson's moral.",
            },
        ],
    },
    {
        "id": "i2-perf-checkpoint",
        "title": "Phòng khám hiệu năng",
        "prompt": "Viết BA hàm. 1) `phaseOf(prop)` — ánh xạ một thuộc tính CSS/JS sang pha pipeline rẻ nhất bị ảnh hưởng: \"transform\" và \"opacity\" => \"composite\"; \"color\", \"background\", \"box-shadow\" => \"paint\"; \"width\", \"height\", \"top\", \"left\", \"font-size\" => \"layout\"; không rõ => \"style\". 2) `budgetVerdict(actual, limit)` — trả về \"ok\" khi actual <= limit, \"over\" khi vượt không quá 10% (limit * 1.1), còn lại \"fail\". 3) `pickFix(symptom)` — ánh xạ triệu chứng sang cách sửa: \"slow-ttfb\" => \"server\", \"huge-image\" => \"image-optimization\", \"long-task\" => \"chunking\", \"layout-shift\" => \"dimensions\", \"render-blocking-css\" => \"critical-css\", không rõ => \"profile-first\".",
        "tests": [
            {"name": "phân loại chi phí pipeline đúng", "hint": "Ba whitelist theo thứ tự chi phí, rồi mặc định."},
            {"name": "ngân sách chấp nhận vượt nhỏ", "hint": "Hai phép so sánh: với limit, rồi với limit * 1.1."},
            {"name": "cách sửa khớp triệu chứng", "hint": "Một lookup object; giá trị mặc định là bài học của cả module."},
        ],
    },
)

print("Module 8 lessons + checkpoint written.")
