/**
 * Module 2: advanced-dom-browser-apis — lessons (EN+VI) + practice sets.
 * DOM challenges are graded with logic-level DOM stubs (harness buildStubs).
 */
import { T, writeModule, writeLesson, writeCheckpoint } from "./i2-lib.mjs";

const MOD = "advanced-dom-browser-apis";

writeModule(MOD, {
  title: "Advanced DOM & Browser APIs",
  summary:
    "From one-off DOM calls to component thinking: event delegation, stateful components, dynamic forms, URL and History APIs, timers, and observers.",
  viTitle: "DOM nâng cao & API trình duyệt",
  viSummary:
    "Từ những lời gọi DOM lẻ tẻ đến tư duy component: ủy quyền sự kiện, component có trạng thái, form động, URL và History API, timer và observers.",
  lessons: [
    "dom-architecture-events",
    "event-delegation",
    "stateful-components",
    "advanced-forms",
    "url-history-api",
    "timers-observers",
    "dashboard-checkpoint",
  ],
  practices: [
    "delegation-practice",
    "components-practice",
    "forms-practice",
    "url-practice",
    "observers-practice",
    "dashboard-practice",
  ],
});

// ── Lesson: dom-architecture-events ─────────────────────────────────────────
writeLesson(
  MOD,
  {
    id: "dom-architecture-events",
    title: "How Events Really Travel",
    description:
      "The DOM as a live tree, the event flow from capture to target to bubble, and why preventDefault and stopPropagation are different tools.",
    minutes: 13,
    difficulty: "intermediate",
    mdx: `
In Beginner you attached listeners and moved on. Now we look at what actually
happens when you click.

## The event flow has three phases

When you click a ${T}button${T} inside a ${T}div${T}, the event does not go
straight to the button. It **travels down** from ${T}window${T} through every
ancestor (the **capture phase**), fires at the button (the **target phase**),
then **travels back up** through the ancestors (the **bubble phase**):

~~~text
window → document → div → button   (capture)
                        button     (target)
window ← document ← div ← button   (bubble)
~~~

By default, listeners run in the bubble phase. Pass ${T}true${T} (or
${T}{ capture: true }${T}) as the third argument to run in the capture phase:

~~~js
document.addEventListener("click", onCaptureClick, true);
~~~

## Three different tools

These are commonly confused — they do different jobs:

- ${T}event.preventDefault()${T} — cancels the browser's **default action**
  (a link navigating, a form submitting) without stopping propagation.
- ${T}event.stopPropagation()${T} — stops the event moving further along the
  flow. Ancestors never hear about it.
- ${T}event.stopImmediatePropagation()${T} — also stops other listeners on the
  **same element** from running.

${T}preventDefault${T} does not stop propagation, and stopping propagation does
not cancel defaults. A form handler that calls
${T}event.stopPropagation()${T} but not ${T}preventDefault()${T} still submits
the page.

## event.target vs event.currentTarget

Inside a handler, ${T}event.target${T} is the element the event originated from
(the button); ${T}event.currentTarget${T} is the element the listener is
attached to (the div). When you attach to the target itself they are the same —
the difference powers the next lesson.
`,
  },
  {
    title: "Sự kiện thực sự di chuyển như thế nào",
    description:
      "DOM như một cây sống, luồng sự kiện từ capture đến target rồi bubble, và vì sao preventDefault với stopPropagation là hai công cụ khác nhau.",
    minutes: 13,
    difficulty: "intermediate",
    mdx: `
Ở khóa người mới bắt đầu, bạn gắn listener rồi thôi quan tâm. Giờ hãy nhìn xem
thực sự điều gì xảy ra khi bạn click.

## Luồng sự kiện có ba pha

Khi bạn click một ${T}button${T} nằm trong ${T}div${T}, sự kiện không đi thẳng
đến button. Nó **đi xuống** từ ${T}window${T} qua từng tổ tiên (pha
**capture**), phát ra tại button (pha **target**), rồi **đi ngược lên** qua các
tổ tiên (pha **bubble**):

~~~text
window → document → div → button   (capture)
                        button     (target)
window ← document ← div ← button   (bubble)
~~~

Mặc định, listener chạy ở pha bubble. Truyền ${T}true${T} (hoặc
${T}{ capture: true }${T}) làm tham số thứ ba để chạy ở pha capture:

~~~js
document.addEventListener("click", onCaptureClick, true);
~~~

## Ba công cụ khác nhau

Ba cái này thường bị nhầm — chúng làm những việc khác nhau:

- ${T}event.preventDefault()${T} — hủy **hành vi mặc định** của trình duyệt
  (link điều hướng, form submit) mà không chặn sự lan truyền.
- ${T}event.stopPropagation()${T} — chặn sự kiện đi tiếp trong luồng. Các tổ
  tiên sẽ không hề hay biết.
- ${T}event.stopImmediatePropagation()${T} — ngoài ra còn chặn các listener
  **cùng phần tử** khác khỏi chạy.

${T}preventDefault${T} không chặn lan truyền, và chặn lan truyền không hủy các
hành vi mặc định. Một handler của form gọi ${T}event.stopPropagation()${T} mà
quên ${T}preventDefault()${T} vẫn khiến trang bị submit.

## event.target và event.currentTarget

Bên trong handler, ${T}event.target${T} là phần tử khởi phát sự kiện (button),
còn ${T}event.currentTarget${T} là phần tử mà listener được gắn vào (div). Khi
bạn gắn listener trực tiếp vào chính target thì hai giá trị trùng nhau — chính
sự khác biệt này là nền tảng cho bài kế tiếp.
`,
  },
);

// ── Lesson: event-delegation ────────────────────────────────────────────────
writeLesson(
  MOD,
  {
    id: "event-delegation",
    title: "Event Delegation",
    description:
      "One listener for a thousand rows: delegation via bubbling, closest(), and data attributes — the pattern behind every list, table, and menu.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
Imagine a table with 1,000 rows, each row needing a delete button. Attaching
1,000 listeners is wasteful — and every row added later needs its own listener.
**Delegation** solves both: attach **one** listener to the stable ancestor and
let bubbling deliver the events.

## The pattern

~~~js
table.addEventListener("click", (event) => {
  const btn = event.target.closest("button[data-action=delete]");
  if (!btn) return; // click landed elsewhere in the row
  const row = btn.closest("tr");
  row.remove();
});
~~~

Three ingredients:

1. Listen on the container that never changes.
2. ${T}event.target.closest(selector)${T} walks **up** from the real target to
   find the element you care about — returning ${T}null${T} when the click was
   not on it.
3. Metadata travels in ${T}data-*${T} attributes, read via
   ${T}element.dataset${T}:

~~~js
<button data-action="delete" data-id="42">Delete</button>
// btn.dataset.action === "delete", btn.dataset.id === "42"
~~~

## Why delegation is the professional default

- New rows work with **zero** extra code — the listener is already there.
- One listener instead of thousands: less memory, faster startup.
- UI built from templates or dynamic HTML needs no re-wiring after render.

The same pattern powers tabs, menus, accordions, and every component practice
below. When a challenge says "clicks work for dynamically added items", it is
asking for delegation.
`,
  },
  {
    title: "Ủy quyền sự kiện",
    description:
      "Một listener cho cả nghìn dòng: ủy quyền qua bubbling, closest() và thuộc tính data — mẫu thiết kế đứng sau mọi danh sách, bảng và menu.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
Hãy tưởng tượng một bảng với 1.000 dòng, mỗi dòng cần một nút xóa. Gắn 1.000
listener là phí tài nguyên — và mỗi dòng thêm vào sau lại cần listener riêng.
**Ủy quyền (delegation)** giải quyết cả hai: gắn **một** listener vào tổ tiên
ổn định và để bubbling đưa sự kiện đến nơi.

## Mẫu thiết kế

~~~js
table.addEventListener("click", (event) => {
  const btn = event.target.closest("button[data-action=delete]");
  if (!btn) return; // cú click rơi vào chỗ khác của dòng
  const row = btn.closest("tr");
  row.remove();
});
~~~

Ba thành phần:

1. Lắng nghe trên container không bao giờ thay đổi.
2. ${T}event.target.closest(selector)${T} đi **lên** từ target thật để tìm phần
   tử bạn quan tâm — trả về ${T}null${T} khi click không nằm trên nó.
3. Siêu dữ liệu đi kèm qua thuộc tính ${T}data-*${T}, đọc bằng
   ${T}element.dataset${T}:

~~~js
<button data-action="delete" data-id="42">Delete</button>
// btn.dataset.action === "delete", btn.dataset.id === "42"
~~~

## Vì sao ủy quyền là lựa chọn mặc định của dân chuyên

- Dòng mới hoạt động với **không một dòng code** thêm — listener đã có sẵn.
- Một listener thay vì hàng nghìn: ít bộ nhớ hơn, khởi động nhanh hơn.
- UI dựng từ template hay HTML động không cần đi lại dây nối sau khi render.

Chính mẫu này đứng sau tabs, menu, accordion và mọi bài luyện component bên
dưới. Khi một thử thách nói "click hoạt động cả với phần tử thêm động", đó là
lời yêu cầu ủy quyền.
`,
  },
);

// ── Lesson: stateful-components ─────────────────────────────────────────────
writeLesson(
  MOD,
  {
    id: "stateful-components",
    title: "Stateful UI Components",
    description:
      "Structure a widget as state + render + events: a component factory pattern that scales from a modal to a full dashboard.",
    minutes: 15,
    difficulty: "intermediate",
    mdx: `
Beginner scripts grow into tangles: every feature reaches into the DOM from
everywhere. The intermediate move is to give each widget a **component shape**:
private state, a render function that draws state to the DOM, and events that
only update state.

## The factory pattern

~~~js
function createTabs(root) {
  const state = { active: 0 };          // 1. private state (a closure)
  const buttons = [...root.querySelectorAll("[role=tab]")];

  function render() {                    // 2. state → DOM
    buttons.forEach((b, i) => {
      b.setAttribute("aria-selected", String(i === state.active));
    });
  }

  root.addEventListener("click", (e) => { // 3. events → state
    const b = e.target.closest("[role=tab]");
    if (!b) return;
    state.active = buttons.indexOf(b);
    render();
  });

  render(); // initial draw
}
~~~

The rules that keep it clean:

- Events **never** edit the DOM directly — they update ${T}state${T} and call
  ${T}render()${T}. One source of truth, no drift.
- ${T}state${T} is closed over: nothing outside can poke it. Changes flow
  through the component's own API.
- ${T}render()${T} is idempotent — call it ten times, get the same UI.

## Accessibility is part of the pattern

Components carry semantics: ${T}role${T}, ${T}aria-selected${T},
${T}aria-expanded${T}, focus moved into modals and back. Doing accessibility at
the component layer means every instance inherits it — retrofitting it later is
the expensive path.
`,
  },
  {
    title: "Component UI có trạng thái",
    description:
      "Cấu trúc một widget thành state + render + event: mẫu component factory có thể mở rộng từ modal đến cả dashboard.",
    minutes: 15,
    difficulty: "intermediate",
    mdx: `
Script thời người mới bắt đầu lớn dần thành mớ rối: mỗi tính năng đều với tay
vào DOM từ khắp nơi. Bước nâng cấp của trình độ trung cấp là cho mỗi widget một
**hình dạng component**: state riêng tư, hàm render vẽ state ra DOM, và các
event chỉ cập nhật state.

## Mẫu factory

~~~js
function createTabs(root) {
  const state = { active: 0 };          // 1. state riêng tư (closure)
  const buttons = [...root.querySelectorAll("[role=tab]")];

  function render() {                    // 2. state → DOM
    buttons.forEach((b, i) => {
      b.setAttribute("aria-selected", String(i === state.active));
    });
  }

  root.addEventListener("click", (e) => { // 3. event → state
    const b = e.target.closest("[role=tab]");
    if (!b) return;
    state.active = buttons.indexOf(b);
    render();
  });

  render(); // vẽ lần đầu
}
~~~

Những quy tắc giữ cho nó gọn gàng:

- Event **không bao giờ** sửa DOM trực tiếp — nó cập nhật ${T}state${T} rồi gọi
  ${T}render()${T}. Một nguồn chân lý duy nhất, không trôi dạt.
- ${T}state${T} nằm trong closure: bên ngoài không thể can thiệp. Mọi thay đổi
  đều đi qua API của component.
- ${T}render()${T} là idempotent — gọi mười lần vẫn cho cùng một UI.

## Khả năng tiếp cận là một phần của mẫu

Component mang theo ngữ nghĩa: ${T}role${T}, ${T}aria-selected${T},
${T}aria-expanded${T}, focus được đưa vào modal rồi trả về. Làm accessibility
ở tầng component nghĩa là mọi bản thể kế thừa sẵn — sửa lại sau này tốn kém hơn
rất nhiều.
`,
  },
);

// ── Lesson: advanced-forms ──────────────────────────────────────────────────
writeLesson(
  MOD,
  {
    id: "advanced-forms",
    title: "Forms Worth Trusting",
    description:
      "Constraint validation, custom validators, inline error messages with aria-invalid and aria-describedby, and dynamic field sets.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
Beginner forms have a submit handler. Intermediate forms earn trust: they
validate like the server will, explain themselves inline, and stay accessible
while doing it.

## Constraint validation API

The browser already validates — read its verdict instead of duplicating rules:

~~~js
const email = form.elements.email;
if (!email.validity.valid) {
  // email.validity.valueMissing, .typeMismatch, .tooShort ...
  email.setCustomValidity("Enter an email like ada@example.com");
} else {
  email.setCustomValidity("");
}
~~~

${T}setCustomValidity("")${T} clears a custom error; any other string marks the
field invalid. ${T}form.reportValidity()${T} shows the message the way the
platform intends. Use built-in attributes first — ${T}required${T},
${T}type="email"${T}, ${T}minlength${T}, ${T}pattern${T} — then custom code for
cross-field rules like password confirmation.

## Inline errors that assistive tech can see

A red border is decoration; the accessible signal is programmatic:

~~~js
field.setAttribute("aria-invalid", "true");
errorBox.textContent = "Age must be a number";
field.setAttribute("aria-describedby", "age-error");
~~~

The error box needs ${T}id="age-error"${T} and
${T}role="alert"${T} so screen readers announce it when it appears. Clear all
three when the field becomes valid.

## Dynamic field sets

Adding rows (tasks, guests, line items) is delegation again: one listener on the
container, ${T}closest("[data-row]")${T} to find the row to remove, and names
that stay unique — either indexed (${T}task-0${T}, ${T}task-1${T}) or irrelevant
because you serialize from the DOM on submit.
`,
  },
  {
    title: "Biểu mẫu đáng tin cậy",
    description:
      "Constraint validation, bộ kiểm tra tùy biến, thông báo lỗi ngay tại chỗ với aria-invalid và aria-describedby, và tập trường động.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
Form của người mới bắt đầu chỉ có một submit handler. Form trình độ trung cấp
đáng được tin: kiểm tra dữ liệu như thể server sẽ kiểm tra lại, tự giải thích
ngay tại chỗ, và vẫn giữ được khả năng tiếp cận trong khi làm điều đó.

## Constraint validation API

Trình duyệt vốn đã kiểm tra — hãy đọc kết luận của nó thay vì viết lại luật:

~~~js
const email = form.elements.email;
if (!email.validity.valid) {
  // email.validity.valueMissing, .typeMismatch, .tooShort ...
  email.setCustomValidity("Enter an email like ada@example.com");
} else {
  email.setCustomValidity("");
}
~~~

${T}setCustomValidity("")${T} xóa lỗi tùy biến; bất kỳ chuỗi nào khác đánh dấu
trường là không hợp lệ. ${T}form.reportValidity()${T} hiển thị thông điệp đúng
cách nền tảng vốn có. Hãy dùng các thuộc tính có sẵn trước — ${T}required${T},
${T}type="email"${T}, ${T}minlength${T}, ${T}pattern${T} — rồi mới đến code tùy
biến cho các luật liên trường như xác nhận mật khẩu.

## Lỗi hiện tại chỗ mà công nghệ hỗ trợ đọc được

Viền đỏ chỉ là trang trí; tín hiệu tiếp cận là thuộc tính:

~~~js
field.setAttribute("aria-invalid", "true");
errorBox.textContent = "Age must be a number";
field.setAttribute("aria-describedby", "age-error");
~~~

Hộp lỗi cần ${T}id="age-error"${T} và ${T}role="alert"${T} để trình đọc màn
hình đọc lên khi nó xuất hiện. Xóa cả ba khi trường hợp lệ trở lại.

## Tập trường động

Thêm dòng (task, khách mời, mặt hàng) chính là ủy quyền: một listener trên
container, ${T}closest("[data-row]")${T} để tìm dòng cần xóa, và tên trường giữ
duy nhất — hoặc đánh chỉ mục (${T}task-0${T}, ${T}task-1${T}) hoặc bỏ qua vì
bạn serialize thẳng từ DOM khi submit.
`,
  },
);

// ── Lesson: url-history-api ─────────────────────────────────────────────────
writeLesson(
  MOD,
  {
    id: "url-history-api",
    title: "URL & History: The State You Can Share",
    description:
      "URL as state: URL/URLSearchParams parsing, pushState and popstate, and why filters belong in the address bar.",
    minutes: 13,
    difficulty: "intermediate",
    mdx: `
A page whose filters live only in JavaScript memory dies on refresh and cannot
be shared. The professional move: put view state in the **URL**, which is
shareable, bookmarkable, and survives reloads for free.

## Reading the URL

~~~js
const url = new URL(window.location.href);
const q = url.searchParams.get("q");          // ?q=ada
const page = Number(url.searchParams.get("page") ?? "1");
url.searchParams.set("q", input.value);       // build a new URL
~~~

${T}URLSearchParams${T} handles encoding for you — never concatenate query
strings by hand.

## Writing history without navigation

~~~js
window.history.pushState({}, "", url);
~~~

${T}pushState${T} changes the address bar and adds an entry — **no page load
happens**. The ${T}popstate${T} event fires when the user moves through
history (back/forward):

~~~js
window.addEventListener("popstate", () => {
  renderFromURL(); // re-read the URL and redraw
});
~~~

## The loop

Every state change: update the URL (pushState), then render **from** the URL.
Every back/forward: render **from** the URL. One reader of truth, one writer —
refresh, share, and back-button all behave.
`,
  },
  {
    title: "URL & History: Trạng thái có thể chia sẻ",
    description:
      "URL như một trạng thái: đọc URL với URL/URLSearchParams, pushState và popstate, và vì sao bộ lọc nên nằm trên thanh địa chỉ.",
    minutes: 13,
    difficulty: "intermediate",
    mdx: `
Một trang mà bộ lọc chỉ sống trong bộ nhớ JavaScript sẽ chết khi refresh và
không thể chia sẻ. Cách làm chuyên nghiệp: đưa trạng thái hiển thị vào
**URL** — thứ có thể chia sẻ, đánh dấu trang, và miễn phí sống sót qua reload.

## Đọc URL

~~~js
const url = new URL(window.location.href);
const q = url.searchParams.get("q");          // ?q=ada
const page = Number(url.searchParams.get("page") ?? "1");
url.searchParams.set("q", input.value);       // dựng URL mới
~~~

${T}URLSearchParams${T} lo phần encode giúp bạn — đừng bao giờ nối chuỗi truy
vấn bằng tay.

## Ghi lịch sử mà không tải lại trang

~~~js
window.history.pushState({}, "", url);
~~~

${T}pushState${T} đổi thanh địa chỉ và thêm một mục lịch sử — **không có lần tải
trang nào xảy ra**. Sự kiện ${T}popstate${T} phát ra khi người dùng di chuyển
trong lịch sử (back/forward):

~~~js
window.addEventListener("popstate", () => {
  renderFromURL(); // đọc lại URL và vẽ lại
});
~~~

## Vòng lặp

Mỗi lần đổi trạng thái: cập nhật URL (pushState), rồi render **từ** URL. Mỗi
lần back/forward: render **từ** URL. Một nơi đọc sự thật, một nơi ghi — refresh,
chia sẻ và nút back đều hoạt động đúng.
`,
  },
);

// ── Lesson: timers-observers ────────────────────────────────────────────────
writeLesson(
  MOD,
  {
    id: "timers-observers",
    title: "Timers & Observers",
    description:
      "Debounce and throttle with setTimeout, IntersectionObserver for lazy work, ResizeObserver, and why setInterval lies about time.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
Browsers give you clocks and observers — using them well is what separates a
smooth app from a janky one.

## Timers are queues, not alarms

${T}setTimeout(fn, 0)${T} does not run "immediately" — it queues ${T}fn${T} to
run after the current code finishes (the event loop, covered properly in the
async module). ${T}setInterval(fn, 1000)${T} fires no faster than every second
**when the main thread is free** — a slow handler stretches the real interval.
When you need a repeating action, prefer scheduling the next ${T}setTimeout${T}
*after* the work completes.

## Debounce and throttle

- **Debounce** — react when the user *pauses*: wait for a quiet gap
  (search-as-you-type).
- **Throttle** — react at most once per interval: cap the rate
  (scroll position reporting).

~~~js
function debounce(fn, ms) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}
~~~

Both are closure patterns from Module 1 — the timer handle lives in the closure.

## Observers: the browser watches for you

Instead of polling, subscribe:

~~~js
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) loadMore();
  }
});
io.observe(sentinel);
~~~

${T}IntersectionObserver${T} reports visibility (lazy images, infinite scroll);
${T}ResizeObserver${T} reports size changes (redraw canvases, collapse
widgets). Both are cheaper and more accurate than scroll or resize handlers —
and remember ${T}prefers-reduced-motion${T} when animations are involved.
`,
  },
  {
    title: "Timers & Observers",
    description:
      "Debounce và throttle bằng setTimeout, IntersectionObserver cho công việc lười, ResizeObserver, và vì sao setInterval nói dối về thời gian.",
    minutes: 14,
    difficulty: "intermediate",
    mdx: `
Trình duyệt cung cấp cho bạn đồng hồ và observers — dùng tốt chúng chính là
điều phân biệt một app mượt với một app giật cục.

## Timer là hàng đợi, không phải chuông báo

${T}setTimeout(fn, 0)${T} không chạy "ngay lập tức" — nó xếp ${T}fn${T} vào
hàng đợi để chạy sau khi code hiện tại kết thúc (event loop, sẽ được dạy đúng
trong module async). ${T}setInterval(fn, 1000)${T} không phát nhanh hơn mỗi một
giây **khi main thread rảnh** — một handler chậm sẽ kéo giãn khoảng cách thật.
Khi cần hành động lặp lại, hãy hẹn vòng ${T}setTimeout${T} kế tiếp *sau khi*
công việc hoàn thành.

## Debounce và throttle

- **Debounce** — phản hồi khi người dùng *nghỉ tay*: chờ một khoảng lặng
  (search-as-you-type).
- **Throttle** — phản hồi tối đa một lần mỗi khoảng: chặn tốc độ
  (báo vị trí scroll).

~~~js
function debounce(fn, ms) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}
~~~

Cả hai đều là mẫu closure từ Module 1 — handle của timer nằm trong closure.

## Observers: trình duyệt theo dõi giúp bạn

Thay vì polling, hãy đăng ký:

~~~js
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (e.isIntersecting) loadMore();
  }
});
io.observe(sentinel);
~~~

${T}IntersectionObserver${T} báo khả năng hiển thị (lazy image, infinite
scroll); ${T}ResizeObserver${T} báo thay đổi kích thước (vẽ lại canvas, thu gọn
widget). Cả hai rẻ và chính xác hơn các handler scroll/resize — và nhớ đến
${T}prefers-reduced-motion${T} khi có animation.
`,
  },
);

// ── Checkpoint lesson ───────────────────────────────────────────────────────
writeCheckpoint(
  MOD,
  {
    id: "dashboard-checkpoint",
    title: "Checkpoint: Component Logic",
    description:
      "Prove the module's patterns at the logic level: delegation resolution, a tab state reducer, and a debounce implementation.",
    minutes: 20,
    difficulty: "intermediate",
    mdx: `
The browser practices for this module run in real DOM. The checkpoint below
verifies the same patterns at the logic level, so your understanding — not just
your copy-paste — is tested.

Three problems, straight from the lessons:

1. **Delegation resolver** — given a click target and a tree, find the
   actionable ancestor exactly like ${T}closest${T} does.
2. **Tabs state reducer** — ${T}reduceTabs(state, action)${T} returning the new
   state for select/next/prev. Never mutate the input state.
3. **Debounce** — the classic closure + timer implementation, verified for both
   immediate and trailing behavior.
`,
  },
  {
    title: "Kiểm tra kiến thức: Logic Component",
    description:
      "Chứng minh các mẫu của module ở tầng logic: bộ phân giải ủy quyền, bộ giảm trạng thái tab, và một cài đặt debounce.",
    minutes: 20,
    difficulty: "intermediate",
    mdx: `
Các bài luyện trình duyệt của module này chạy trong DOM thật. Bài kiểm tra kiến
thức bên dưới xác minh cùng các mẫu đó ở tầng logic — để kiểm tra sự hiểu của
bạn, chứ không phải kỹ năng copy-paste.

Ba bài toán, lấy thẳng từ các bài học:

1. **Bộ phân giải ủy quyền** — cho click target và một cây, tìm tổ tiên có thể
   hành động đúng như ${T}closest${T} làm.
2. **Bộ giảm trạng thái tabs** — ${T}reduceTabs(state, action)${T} trả về trạng
   thái mới cho select/next/prev. Không bao giờ làm thay đổi state đầu vào.
3. **Debounce** — cài đặt kinh điển closure + timer, xác minh cả hành vi ngay
   lập tức lẫn hành vi chạy sau.
`,
  },
  {
    id: "i2-dashboard-checkpoint",
    title: "Component Logic Check",
    prompt:
      'Implement three component-logic helpers:\n\n1. `findActionable(target, selector)` RETURNS the first element in the chain `target`, `target.parent`, `target.parent.parent`, ... matching `selector` (elements have a `matches(sel)` method), or `null`.\n2. `reduceTabs(state, action)` RETURNS a NEW `{ active, count }` object. Actions: `{ type: "select", index }` clamps 0..count-1, `{ type: "next" }` and `{ type: "prev" }` wrap around. The input state must not be mutated.\n3. `debounce(fn, ms)` RETURNS a debounced wrapper. Calls inside the quiet window cancel the pending one; after `ms` of quiet the LAST call\'s arguments are used.',
    difficulty: "intermediate",
    boilerplate:
      "// 1) findActionable(target, selector)\n\n// 2) reduceTabs(state, action)\n\n// 3) debounce(fn, ms)\n",
    tests: [
      {
        name: "findActionable walks up to the matching ancestor",
        code: 'const fn = new Function(code + "\\nreturn { findActionable, reduceTabs, debounce };");\nconst { findActionable } = fn();\nconst matchesSel = (sel) => (s) => s === sel;\nconst grand = { matches: matchesSel("table"), parent: null };\nconst parent = { matches: matchesSel("tr"), parent: grand };\nconst target = { matches: () => false, parent };\nif (findActionable(target, "table") !== grand) throw new Error("Should find the table ancestor.");\nif (findActionable(target, "tr") !== parent) throw new Error("Should stop at the first (nearest) match.");\nif (findActionable(target, "nav") !== null) throw new Error("No match anywhere in the chain must return null.");',
        hint: "Loop `for (let el = target; el; el = el.parent)` and return the first el whose matches(sel) is true.",
      },
      {
        name: "reduceTabs clamps select and wraps next/prev",
        code: 'const fn = new Function(code + "\\nreturn { findActionable, reduceTabs, debounce };");\nconst { reduceTabs } = fn();\nconst s = { active: 1, count: 3 };\nif (reduceTabs(s, { type: "select", index: 2 }).active !== 2) throw new Error("select should set the active tab.");\nif (reduceTabs(s, { type: "select", index: 9 }).active !== 2) throw new Error("Out-of-range select must clamp to the last tab (2)."\n);\nif (reduceTabs(s, { type: "next" }).active !== 2) throw new Error("next from 1 should be 2.");\nif (reduceTabs({ active: 2, count: 3 }, { type: "next" }).active !== 0) throw new Error("next wraps around from the last tab to 0.");\nif (reduceTabs({ active: 0, count: 3 }, { type: "prev" }).active !== 2) throw new Error("prev wraps around from the first tab to the last.");',
        hint: "select: Math.min(Math.max(index, 0), count - 1). next: (active + 1) % count. prev: (active - 1 + count) % count.",
      },
      {
        name: "reduceTabs does not mutate the input state",
        code: 'const fn = new Function(code + "\\nreturn { findActionable, reduceTabs, debounce };");\nconst { reduceTabs } = fn();\nconst s = { active: 1, count: 3 };\nreduceTabs(s, { type: "next" });\nif (s.active !== 1) throw new Error("The original state object must keep active: 1 — return a new object instead of mutating.");',
        hint: "Build the result with spread: { ...state, active: newValue }.",
      },
      {
        name: "debounce delays and collapses rapid calls",
        code: 'const fn = new Function(code + "\\nreturn { findActionable, reduceTabs, debounce };");\nconst { debounce } = fn();\nconst seen = [];\nconst push = (v) => seen.push(v);\nconst debounced = debounce(push, 30);\ndebounced("a"); debounced("b"); debounced("c");\nif (seen.length !== 0) throw new Error("Nothing should run while calls keep arriving inside the quiet window.");\nawait new Promise((r) => setTimeout(r, 70));\nif (seen.length !== 1 || seen[0] !== "c") throw new Error("Exactly one run should happen after the quiet window, with the LAST arguments (\'c\').");',
        hint: "clearTimeout the previous handle and setTimeout a new one each call — the timer handle lives in the closure.",
      },
    ],
  },
  {
    title: "Kiểm tra kiến thức: Logic Component",
    prompt:
      'Cài đặt ba hàm logic component:\n\n1. `findActionable(target, selector)` RETURN phần tử đầu tiên trong chuỗi `target`, `target.parent`, `target.parent.parent`, ... khớp với `selector` (mỗi phần tử có phương thức `matches(sel)`), hoặc `null`.\n2. `reduceTabs(state, action)` RETURN một object `{ active, count }` MỚI. Các action: `{ type: "select", index }` kẹp trong 0..count-1, `{ type: "next" }` và `{ type: "prev" }` quay vòng. Không được làm thay đổi state đầu vào.\n3. `debounce(fn, ms)` RETURN một wrapper đã debounce. Các lời gọi trong khoảng lặng hủy lời đang chờ; sau `ms` im lặng, đối số của lời gọi CUỐI được dùng.',
    tests: [
      {
        name: "findActionable đi lên tìm tổ tiên khớp",
        hint: "Vòng lặp for (let el = target; el; el = el.parent) và trả về phần tử đầu tiên có matches(sel) đúng.",
      },
      {
        name: "reduceTabs kẹp select và quay vòng next/prev",
        hint: "select: Math.min(Math.max(index, 0), count - 1). next: (active + 1) % count. prev: (active - 1 + count) % count.",
      },
      {
        name: "reduceTabs không làm thay đổi state đầu vào",
        hint: "Dựng kết quả bằng spread: { ...state, active: giá trị mới }.",
      },
      {
        name: "debounce trì hoãn và gộp các lời gọi liên tiếp",
        hint: "Mỗi lần gọi: clearTimeout handle cũ rồi setTimeout handle mới — handle nằm trong closure.",
      },
    ],
  },
);

console.log("Module 2 lessons + checkpoint written.");
