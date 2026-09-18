#!/usr/bin/env python3
"""Module 3: asynchronous-javascript-apis — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import (
    write_module, write_lesson, write_checkpoint, write_practice, fn_wrap,
)

MOD = "asynchronous-javascript-apis"

write_module(
    MOD,
    "Asynchronous JavaScript & APIs",
    "Make the single thread work for you: the event loop, promises and async/await, parallel and sequential strategies, fetch with loading/error states, pagination, and cancellation.",
    "JavaScript bất đồng bộ & API",
    "Biến luồng đơn thành lợi thế: event loop, promise và async/await, chiến lược song song và tuần tự, fetch với trạng thái loading/lỗi, phân trang và hủy request.",
    [
        "event-loop",
        "promises",
        "async-await",
        "promise-combinators",
        "fetch-patterns",
        "cancellation-abort",
        "api-app-checkpoint",
    ],
    [
        "event-loop-practice",
        "promises-practice",
        "combinators-practice",
        "fetch-practice",
        "cancellation-practice",
        "api-app-practice",
    ],
)

# ── event-loop ──────────────────────────────────────────────────────────────
write_lesson(
    MOD, "event-loop",
    "The Event Loop: One Thread, No Waiting",
    "Call stack, task queue, microtask queue — predict exactly what runs when, and why setTimeout(0) is never immediate.",
    14,
    """
JavaScript runs your code on **one thread**. It never blocks: slow work (timers,
network, disk) is handed to the environment, and your callbacks are *queued*.
The rules of that queue are the event loop.

## The three queues that matter

1. **Call stack** — the function currently executing. One at a time, always.
2. **Microtask queue** — promise callbacks (`.then`, `await` continuations),
   `queueMicrotask`. Drained **completely** after every stack empties.
3. **Macrotask queue** — `setTimeout`, `setInterval`, I/O callbacks, events.
   One macrotask per loop turn.

Per turn: run one macrotask → drain **all** microtasks → maybe render → next
macrotask. Microtasks always win.

## Predicting the order

~~~js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
~~~

Prints `1, 4, 3, 2`. Sync code first (`1`, `4`), then microtasks (`3`), then
the timer macrotask (`2`). `setTimeout(fn, 0)` does not mean *now* — it means
*next macrotask, at the earliest*.

## Why it matters

- A long-running loop blocks everything: renders, clicks, timers. Chunk work
  with `await new Promise(r => setTimeout(r))` to yield.
- Promise chains resolve before any timer callback — ordering bugs come from
  forgetting which queue you are in.
- The UI can only update between tasks: await between chunks lets the browser
  paint.

MDN's *Concurrency model and the event loop* is the reference; this lesson is
the mental model you will apply in every practice below.
""",
    "Event Loop: Một Luồng, Không Chờ Đợi",
    "Call stack, hàng đợi task, hàng đợi microtask — dự đoán chính xác cái gì chạy khi nào, và vì sao setTimeout(0) không bao giờ là ngay lập tức.",
    """
JavaScript chạy code của bạn trên **một luồng duy nhất**. Nó không bao giờ chặn:
công việc chậm (timer, mạng, đĩa) được giao cho môi trường, và callback của bạn
được *xếp hàng*. Luật của hàng đợi đó chính là event loop.

## Ba hàng đợi quan trọng

1. **Call stack** — hàm đang thực thi. Luôn luôn một cái tại một thời điểm.
2. **Hàng đợi microtask** — callback của promise (`.then`, phần tiếp theo của
   `await`), `queueMicrotask`. Bị xả **toàn bộ** sau mỗi lần stack rỗng.
3. **Hàng đợi macrotask** — `setTimeout`, `setInterval`, callback I/O, sự kiện.
   Mỗi vòng lặp chỉ một macrotask.

Mỗi vòng: chạy một macrotask → xả **tất cả** microtask → có thể render →
macrotask kế tiếp. Microtask luôn thắng.

## Dự đoán thứ tự

~~~js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
~~~

In ra `1, 4, 3, 2`. Code đồng bộ trước (`1`, `4`), rồi microtask (`3`), rồi
timer macrotask (`2`). `setTimeout(fn, 0)` không có nghĩa là *ngay bây giờ* —
nó có nghĩa là *macrotask kế tiếp, sớm nhất có thể*.

## Vì sao điều này quan trọng

- Một vòng lặp chạy lâu chặn tất cả: render, click, timer. Chia nhỏ công việc
  với `await new Promise(r => setTimeout(r))` để nhường luồng.
- Chuỗi promise phân giải trước mọi callback của timer — lỗi thứ tự đến từ việc
  quên mình đang ở hàng đợi nào.
- UI chỉ cập nhật được giữa các task: await giữa các phần cho trình duyệt kịp
  vẽ.

Bài *Concurrency model and the event loop* trên MDN là tài liệu tham khảo;
bài học này là mô hình tư duy bạn sẽ áp dụng trong mọi bài luyện bên dưới.
""",
)

# ── promises ────────────────────────────────────────────────────────────────
write_lesson(
    MOD, "promises",
    "Promises from First Principles",
    "States, chaining, error propagation, and finally — how promises replace callback pyramids and compose.",
    15,
    """
A **promise** is a value that may not exist yet. It has three states:
**pending** → **fulfilled** (with a value) or **rejected** (with an error) —
and once settled, never changes again.

## Chaining

Every `.then` returns a **new** promise, which is what makes chains flat
instead of nested:

~~~js
fetchJSON("/api/user")
  .then((user) => fetchJSON("/api/orders/" + user.id))
  .then((orders) => render(orders))
  .catch((err) => showError(err));   // catches ANY step above
  .finally(() => hideSpinner());     // runs either way
~~~

Three rules worth memorizing:

- Returning a value in `.then` fulfills the next promise with that value.
- Returning a **promise** from `.then` makes the chain wait for it.
- A thrown error (or a rejected promise returned) skips forward to the nearest
  `.catch` — errors *propagate* like try/catch, through the whole chain.

## Errors are values too

`.catch(onRejected)` is `.then(undefined, onRejected)`. A `.catch` that returns
normally *recovers* the chain — later `.then`s run. That is how fallback logic
works:

~~~js
getFromCache(id)
  .catch(() => getFromNetwork(id))  // fallback
  .then(render);
~~~

## finally

`.finally(fn)` runs on both outcomes and receives nothing — it is for cleanup
(spinner off, lock released), not for the result.
""",
    "Promise từ Nguyên Lý Đầu Tiên",
    "Các trạng thái, chuỗi nối, lan truyền lỗi và finally — cách promise thay thế tháp callback và cách chúng kết hợp với nhau.",
    """
**Promise** là một giá trị có thể chưa tồn tại. Nó có ba trạng thái:
**pending** → **fulfilled** (kèm giá trị) hoặc **rejected** (kèm lỗi) — và một
khi đã settled thì không bao giờ đổi nữa.

## Chuỗi nối

Mỗi `.then` trả về một promise **mới** — chính điều này khiến chuỗi phẳng thay
vì lồng nhau:

~~~js
fetchJSON("/api/user")
  .then((user) => fetchJSON("/api/orders/" + user.id))
  .then((orders) => render(orders))
  .catch((err) => showError(err));   // bắt lỗi ở BẤT KỲ bước nào phía trên
  .finally(() => hideSpinner());     // chạy theo cả hai hướng
~~~

Ba quy tắc đáng nhớ:

- Return một giá trị trong `.then` làm promise kế tiếp fulfilled với giá trị đó.
- Return một **promise** từ `.then` khiến chuỗi chờ promise đó.
- Một lỗi bị ném (hoặc promise bị trả về bị reject) sẽ nhảy tới `.catch` gần
  nhất — lỗi *lan truyền* như try/catch, xuyên suốt cả chuỗi.

## Lỗi cũng là giá trị

`.catch(onRejected)` chính là `.then(undefined, onRejected)`. Một `.catch`
return bình thường sẽ *hồi phục* chuỗi — các `.then` phía sau vẫn chạy. Đây là
cách logic dự phòng hoạt động:

~~~js
getFromCache(id)
  .catch(() => getFromNetwork(id))  // phương án dự phòng
  .then(render);
~~~

## finally

`.finally(fn)` chạy với cả hai kết quả và không nhận gì — nó dùng để dọn dẹp
(tắt spinner, nhả lock), không phải để lấy kết quả.
""",
)

# ── async-await ─────────────────────────────────────────────────────────────
write_lesson(
    MOD, "async-await",
    "async/await: Sequential Shape, Concurrent Power",
    "Async functions, await semantics, try/catch over async code, and loops — sequential await vs parallel Promise.all.",
    15,
    """
`async/await` is promise syntax sugar — same machinery, readable shape.

## The rules

- `async function` **always** returns a promise; returning a value wraps it,
  throwing rejects it.
- `await` pauses *only* the async function, not the thread: the rest of the
  program keeps running (event loop lesson).
- `await` works on any thenable — and unwraps in a microtask, so `await` order
  follows microtask order.

~~~js
async function loadDashboard(userId) {
  try {
    const user = await getUser(userId);      // sequential: needs user.id
    const orders = await getOrders(user.id);
    return { user, orders };
  } catch (err) {
    return { error: "Could not load dashboard" };  // catches both awaits
  }
}
~~~

`try/catch` works across `await` — one of its best features. Remember it only
catches errors *inside the try block at await time*; a forgotten `await` leaks
a floating promise whose rejection nothing catches.

## The classic trap: await in a loop

~~~js
// SLOW: one request at a time (unless each needs the previous)
for (const id of ids) results.push(await fetchOne(id));

// FAST: all in flight at once
const results = await Promise.all(ids.map(fetchOne));
~~~

Sequential await is *correct* when step N needs step N-1's output; otherwise it
is wasted latency. The combinator lesson formalizes this.
""",
    "async/await: Hình Dạng Tuần Tự, Sức Mạnh Song Song",
    "Hàm async, ngữ nghĩa await, try/catch trên code bất đồng bộ và vòng lặp — await tuần tự so với Promise.all song song.",
    """
`async/await` là đường của promise — cùng bộ máy, hình dạng dễ đọc.

## Các quy tắc

- `async function` **luôn luôn** trả về promise; return một giá trị thì nó được
  bọc lại, throw thì reject.
- `await` chỉ tạm dừng *hàm async đang chạy*, không phải luồng: phần còn lại
  của chương trình vẫn chạy (bài event loop).
- `await` hoạt động với mọi thenable — và được unwrap trong microtask, nên thứ
  tự await đi theo thứ tự microtask.

~~~js
async function loadDashboard(userId) {
  try {
    const user = await getUser(userId);      // tuần tự: cần user.id
    const orders = await getOrders(user.id);
    return { user, orders };
  } catch (err) {
    return { error: "Could not load dashboard" };  // bắt cả hai await
  }
}
~~~

`try/catch` hoạt động xuyên qua `await` — một trong những tính năng tốt nhất
của nó. Hãy nhớ nó chỉ bắt lỗi *bên trong khối try tại thời điểm await*; quên
một `await` sẽ rò rỉ một promise lơ lửng mà không ai bắt được rejection của nó.

## Bẫy kinh điển: await trong vòng lặp

~~~js
// CHẬM: mỗi lần một request (trừ khi bước sau cần kết quả bước trước)
for (const id of ids) results.push(await fetchOne(id));

// NHANH: tất cả cùng bay một lúc
const results = await Promise.all(ids.map(fetchOne));
~~~

Await tuần tự *đúng* khi bước N cần kết quả của bước N-1; nếu không, đó là
độ trễ bị lãng phí. Bài về combinator sẽ hệ thống hóa điều này.
""",
)

# ── promise-combinators ─────────────────────────────────────────────────────
write_lesson(
    MOD, "promise-combinators",
    "Promise Combinators: Choosing a Strategy",
    "all, allSettled, race, any — what each settles with, when each is the right tool, and partial-failure UX.",
    14,
    """
Four static methods combine promise lists. Choosing the right one is a design
decision, not trivia.

| Combinator | Resolves when | Rejects when | Use for |
|---|---|---|---|
| `Promise.all` | **all** fulfill | first rejection | everything is required |
| `Promise.allSettled` | all settle (either way) | never | partial failure is OK |
| `Promise.race` | first settle (either way) | — | timeouts, first response |
| `Promise.any` | first **fulfillment** | all reject | fastest working source |

## all vs allSettled — the partial-failure problem

A dashboard fetching user + orders + notifications: with `Promise.all`, one
failing endpoint kills the page. With `Promise.allSettled`, every request
finishes and you decide per-item:

~~~js
const results = await Promise.allSettled([getUser(), getOrders(), getNotifs()]);
for (const r of results) {
  if (r.status === "fulfilled") render(r.value);
  else renderError(r.reason);
}
~~~

`allSettled` results are `{ status: "fulfilled", value }` or
`{ status: "rejected", reason }` — always inspect `status`.

## race for timeouts

~~~js
const work = doLongThing();
const timeout = new Promise((_, rej) =>
  setTimeout(() => rej(new Error("timeout")), 3000),
);
await Promise.race([work, timeout]);
~~~

Note `race` does not cancel the loser — the long fetch keeps running (cancellation
comes two lessons ahead). `Promise.any` is the rarest: multiple mirrors, take
whichever answers successfully first.
""",
    "Promise Combinators: Chọn Chiến Lược",
    "all, allSettled, race, any — mỗi cái settle với gì, khi nào là công cụ đúng, và UX cho thất bại một phần.",
    """
Bốn phương thức tĩnh kết hợp danh sách promise. Chọn đúng cái là một quyết định
thiết kế, không phải câu hỏi luyện trí nhớ.

| Combinator | Resolve khi nào | Reject khi nào | Dùng cho |
|---|---|---|---|
| `Promise.all` | **tất cả** fulfill | rejection đầu tiên | mọi thứ đều bắt buộc |
| `Promise.allSettled` | tất cả settle (cách nào cũng được) | không bao giờ | thất bại một phần vẫn ổn |
| `Promise.race` | settle đầu tiên (cách nào cũng được) | — | timeout, phản hồi đầu tiên |
| `Promise.any` | **fulfillment** đầu tiên | tất cả reject | nguồn hoạt động nhanh nhất |

## all và allSettled — bài toán thất bại một phần

Dashboard tải user + orders + thông báo: với `Promise.all`, một endpoint hỏng
đổ cả trang. Với `Promise.allSettled`, mọi request đều kết thúc và bạn quyết
định theo từng mục:

~~~js
const results = await Promise.allSettled([getUser(), getOrders(), getNotifs()]);
for (const r of results) {
  if (r.status === "fulfilled") render(r.value);
  else renderError(r.reason);
}
~~~

Kết quả của `allSettled` là `{ status: "fulfilled", value }` hoặc
`{ status: "rejected", reason }` — luôn luôn kiểm tra `status`.

## race cho timeout

~~~js
const work = doLongThing();
const timeout = new Promise((_, rej) =>
  setTimeout(() => rej(new Error("timeout")), 3000),
);
await Promise.race([work, timeout]);
~~~

Lưu ý `race` không hủy bên thua — fetch dài vẫn chạy tiếp (việc hủy nằm ở bài
hai bài nữa). `Promise.any` hiếm gặp nhất: nhiều nguồn mirror, lấy cái trả lời
thành công đầu tiên.
""",
)

# ── fetch-patterns ──────────────────────────────────────────────────────────
write_lesson(
    MOD, "fetch-patterns",
    "fetch in the Real World",
    "Status handling, JSON bodies, headers, query params, pagination loops, and the loading/error UI contract.",
    16,
    """
`fetch` resolves on **any** response — 404 and 500 included. Only network
failure rejects. The first professional habit: check `response.ok`.

## The shape every call should have

~~~js
async function getUser(id) {
  const res = await fetch("/api/users/" + id);
  if (!res.ok) {
    throw new Error("HTTP " + res.status + " for user " + id);
  }
  return res.json();  // also a promise
}
~~~

- `res.ok` is `status` in 200–299.
- `res.json()` parses the body; `res.text()` for anything else.
- Request options: `method`, `headers`, `body` (JSON needs `JSON.stringify`
  plus `Content-Type: application/json`).

~~~js
fetch("/api/tasks", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "write tests" }),
});
~~~

## Query params and pagination

Build queries with `URLSearchParams` — it encodes for free:

~~~js
const qs = new URLSearchParams({ page: String(page), perPage: "20", q: term });
const res = await fetch("/api/items?" + qs);
~~~

Paginated loops continue while a *has-more* signal exists (a `next` link, or
`page * perPage < total`) — never blindly until an empty page without a bound.

## The UI contract

Every async view owes the user three states: **loading** (spinner/skeleton),
**error** (message + retry affordance), **data** (or a polite empty state).
Design the component around `{ status: "idle" | "loading" | "error" | "success", data, error }` and rendering becomes trivial.
""",
    "fetch trong Thế Giới Thực",
    "Xử lý status, body JSON, headers, tham số truy vấn, vòng lặp phân trang, và hợp đồng UI loading/lỗi.",
    """
`fetch` resolve với **mọi** phản hồi — kể cả 404 và 500. Chỉ lỗi mạng mới
reject. Thói quen chuyên nghiệp đầu tiên: kiểm tra `response.ok`.

## Hình dạng mọi lời gọi nên có

~~~js
async function getUser(id) {
  const res = await fetch("/api/users/" + id);
  if (!res.ok) {
    throw new Error("HTTP " + res.status + " for user " + id);
  }
  return res.json();  // cũng là một promise
}
~~~

- `res.ok` là `status` trong khoảng 200–299.
- `res.json()` phân tích body; `res.text()` cho những thứ khác.
- Các option của request: `method`, `headers`, `body` (JSON cần `JSON.stringify`
  cộng `Content-Type: application/json`).

~~~js
fetch("/api/tasks", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "write tests" }),
});
~~~

## Tham số truy vấn và phân trang

Dựng query bằng `URLSearchParams` — nó encode miễn phí:

~~~js
const qs = new URLSearchParams({ page: String(page), perPage: "20", q: term });
const res = await fetch("/api/items?" + qs);
~~~

Vòng lặp phân trang tiếp tục khi còn tín hiệu *has-more* (link `next`, hoặc
`page * perPage < total`) — đừng mù quáng chạy đến trang rỗng khi không có giới
hạn.

## Hợp đồng UI

Mọi view bất đồng bộ nợ người dùng ba trạng thái: **loading** (spinner/skeleton),
**lỗi** (thông báo + khả năng thử lại), **dữ liệu** (hoặc trạng thái rỗng lịch
sự). Hãy thiết kế component xoay quanh
`{ status: "idle" | "loading" | "error" | "success", data, error }` và việc
render trở nên tầm thường.
""",
)

# ── cancellation-abort ──────────────────────────────────────────────────────
write_lesson(
    MOD, "cancellation-abort",
    "Cancelling Work: AbortController",
    "Aborting fetch mid-flight, wiring AbortSignal to timeouts and UI events, and detecting AbortError versus real failures.",
    12,
    """
Leaving five stale searches running while the user types is a bug: wasted
bandwidth, out-of-order responses, race conditions. Cancellation is the fix.

## The pieces

`AbortController` exposes a `signal`; every consumer of the signal can stop
work by calling `controller.abort()`:

~~~js
const controller = new AbortController();
fetch(url, { signal: controller.signal }).catch(handleAbort);

// later — from a timeout, a new search, or unmount:
controller.abort();
~~~

Aborted fetches reject with an `AbortError` (`err.name === "AbortError"`).
**Distinguish it from real errors** — the user does not need a scary error box
because they typed faster:

~~~js
function handleAbort(err) {
  if (err.name === "AbortError") return; // expected, ignore
  showError(err);
}
~~~

## The race-with-timeout idiom

~~~js
function withTimeout(ms) {
  const c = new AbortController();
  setTimeout(() => c.abort(), ms);
  return c.signal;
}

fetch(url, { signal: withTimeout(5000) });
~~~

New searches abort the previous controller — one controller per logical
operation, replaced when the operation is replaced. The same signal also stops
`addEventListener` (via `{ signal }`) and can be passed to timers in modern
runtimes.
""",
    "Hủy Công Việc: AbortController",
    "Hủy fetch giữa đường, nối AbortSignal với timeout và sự kiện UI, và phân biệt AbortError với lỗi thật.",
    """
Để năm cuộc tìm kiếm cũ chạy tiếp khi người dùng đang gõ là một lỗi: lãng phí
băng thông, phản hồi lệch thứ tự, race condition. Hủy request là cách sửa.

## Các mảnh ghép

`AbortController` có một `signal`; bất kỳ ai nắm signal đều có thể dừng công
việc bằng `controller.abort()`:

~~~js
const controller = new AbortController();
fetch(url, { signal: controller.signal }).catch(handleAbort);

// sau đó — từ một timeout, một lần tìm kiếm mới, hoặc khi component unmount:
controller.abort();
~~~

Fetch bị hủy sẽ reject với `AbortError` (`err.name === "AbortError"`).
**Phân biệt nó với lỗi thật** — người dùng không cần một hộp lỗi đáng sợ chỉ vì
họ gõ nhanh hơn:

~~~js
function handleAbort(err) {
  if (err.name === "AbortError") return; // dự liệu được, bỏ qua
  showError(err);
}
~~~

## Mẫu đua với timeout

~~~js
function withTimeout(ms) {
  const c = new AbortController();
  setTimeout(() => c.abort(), ms);
  return c.signal;
}

fetch(url, { signal: withTimeout(5000) });
~~~

Mỗi lần tìm kiếm mới hủy controller trước đó — một controller cho mỗi thao tác
logic, được thay thế khi thao tác được thay thế. Cùng signal đó cũng dừng được
`addEventListener` (qua `{ signal }`) và có thể truyền cho timer trong các
runtime hiện đại.
""",
)

# ── api-app-checkpoint ──────────────────────────────────────────────────────
write_checkpoint(
    MOD,
    "api-app-checkpoint",
    "Checkpoint: Async Request Engine",
    "Build the state machine behind an API-driven UI: a request engine with dedupe, an allSettled dashboard loader, and a timeout wrapper.",
    22,
    """
This checkpoint assembles the module's pieces into the engine an API-driven
app actually runs on. No browser needed — the logic is testable pure:

1. **Request engine** — a `createLoader(fetchFn)` factory: `load(key)` returns
   a promise and caches the promise by key, so concurrent duplicate requests
   share one flight (dedupe), and `reset()` clears the cache.
2. **Resilient dashboard** — `loadDashboard(tasks)` that runs all sources with
   `allSettled` and returns `{ loaded, failed }` lists.
3. **Timeout race** — `withTimeout(promise, ms, fallback)` resolving the
   promise's value, or `fallback` if it does not settle in `ms`.
""",
    "Kiểm tra kiến thức: Động Cơ Request Bất Đồng Bộ",
    "Xây bộ máy trạng thái đứng sau một UI lấy dữ liệu từ API: động cơ request có khử trùng lặp, bộ nạp dashboard dùng allSettled, và wrapper timeout.",
    """
Bài kiểm tra này lắp các mảnh của module thành động cơ mà một ứng dụng gọi API
thực thụ vận hành. Không cần trình duyệt — logic thuần, kiểm tra được:

1. **Động cơ request** — một factory `createLoader(fetchFn)`: `load(key)` trả
   về promise và cache promise đó theo key, để các request trùng lặp chạy đồng
   thời dùng chung một chuyến bay (dedupe), và `reset()` xóa cache.
2. **Dashboard kiên cường** — `loadDashboard(tasks)` chạy mọi nguồn bằng
   `allSettled` và trả về hai danh sách `{ loaded, failed }`.
3. **Đua timeout** — `withTimeout(promise, ms, fallback)` phân giải bằng giá
   trị của promise, hoặc `fallback` nếu nó chưa settle trong `ms`.
""",
    {
        "id": "i2-async-checkpoint",
        "title": "Async Request Engine Check",
        "prompt": "Implement three async helpers:\n\n1. `createLoader(fetchFn)` RETURNS `{ load, reset }`. `load(key)` calls `fetchFn(key)` once per key and RETURNS the resulting promise; concurrent and later calls with the same key RETURN THE SAME promise. `reset()` clears all cached promises (the next load re-fetches).\n2. `loadDashboard(sources)` where `sources` is an array of zero-argument promise-returning functions. It runs ALL of them concurrently and RETURNS a promise for `{ loaded, failed }` — `loaded` is the array of fulfilled values (in order), `failed` the array of rejection reasons (in order). It never rejects.\n3. `withTimeout(promise, ms, fallback)` RETURNS a promise that settles with the promise's value if it fulfills within `ms`, otherwise with `fallback`. It never rejects.",
        "difficulty": "intermediate",
        "boilerplate": "// 1) createLoader(fetchFn)\n\n// 2) loadDashboard(sources)\n\n// 3) withTimeout(promise, ms, fallback)\n",
        "tests": [
            {
                "name": "loader dedupes concurrent requests per key",
                "code": fn_wrap("createLoader, loadDashboard, withTimeout", "createLoader, loadDashboard, withTimeout") + "\nlet calls = 0;\nconst loader = createLoader(async (key) => { calls++; await new Promise((r) => setTimeout(r, 10)); return key + \"-data\"; });\nconst [a, b] = await Promise.all([loader.load(\"x\"), loader.load(\"x\")]);\nif (a !== \"x-data\" || b !== \"x-data\") throw new Error(\"Both loads should resolve with the fetched value.\");\nif (calls !== 1) throw new Error(\"Concurrent loads of the same key must share one flight (1 call, got \" + calls + \").\");\nconst c = await loader.load(\"x\");\nif (c !== \"x-data\") throw new Error(\"Later loads still return the cached promise's value.\");\nloader.reset();\nawait loader.load(\"x\");\nif (calls !== 2) throw new Error(\"After reset, loading again must re-fetch.\");",
                "hint": "Keep a Map of key → promise in the closure; store the promise (not the value) so in-flight requests are shared. reset() = map.clear().",
            },
            {
                "name": "loadDashboard separates fulfilled and rejected",
                "code": fn_wrap("createLoader, loadDashboard, withTimeout", "createLoader, loadDashboard, withTimeout") + "\nconst ok1 = () => Promise.resolve(1);\nconst ok2 = () => Promise.resolve(2);\nconst bad = () => Promise.reject(new Error(\"boom\"));\nconst out = await loadDashboard([ok1, bad, ok2]);\nif (out.loaded.join() !== \"1,2\") throw new Error(\"loaded should be fulfilled values in source order.\");\nif (out.failed.length !== 1) throw new Error(\"failed should hold the single rejection reason.\");\nconst allBad = await loadDashboard([bad, bad]);\nif (allBad.loaded.length !== 0 || allBad.failed.length !== 2) throw new Error(\"loadDashboard never rejects, even when every source fails.\");",
                "hint": "Promise.allSettled, then split results on status === 'fulfilled'.",
            },
            {
                "name": "withTimeout resolves value or fallback",
                "code": fn_wrap("createLoader, loadDashboard, withTimeout", "createLoader, loadDashboard, withTimeout") + "\nconst fast = withTimeout(Promise.resolve(\"quick\"), 50, \"fallback\");\nif ((await fast) !== \"quick\") throw new Error(\"A promise that fulfills in time resolves with its value.\");\nconst slow = withTimeout(new Promise((r) => setTimeout(() => r(\"late\"), 80)), 20, \"gave-up\");\nif ((await slow) !== \"gave-up\") throw new Error(\"A promise that misses the deadline settles with the fallback.\");",
                "hint": "Promise.race([promise, timerPromise]) where the timer resolves with fallback after ms.",
            },
        ],
    },
    {
        "title": "Kiểm tra kiến thức: Động Cơ Request Bất Đồng Bộ",
        "prompt": "Cài đặt ba hàm bất đồng bộ:\n\n1. `createLoader(fetchFn)` RETURN `{ load, reset }`. `load(key)` gọi `fetchFn(key)` một lần cho mỗi key và RETURN promise kết quả; các lời gọi đồng thời hoặc về sau với cùng key RETURN CÙNG MỘT promise. `reset()` xóa toàn bộ promise đã cache (lần load kế tiếp sẽ gọi lại).\n2. `loadDashboard(sources)` trong đó `sources` là mảng các hàm không đối số trả về promise. Nó chạy TẤT CẢ đồng thời và RETURN một promise cho `{ loaded, failed }` — `loaded` là mảng các giá trị fulfilled (đúng thứ tự), `failed` là mảng các lý do reject (đúng thứ tự). Nó không bao giờ reject.\n3. `withTimeout(promise, ms, fallback)` RETURN một promise settle bằng giá trị của promise nếu nó fulfill trong `ms`, nếu không thì bằng `fallback`. Không bao giờ reject.",
        "tests": [
            {"name": "loader khử trùng lặp request đồng thời theo key", "hint": "Giữ một Map key → promise trong closure; lưu promise (không phải giá trị) để các request đang bay được dùng chung. reset() = map.clear()."},
            {"name": "loadDashboard tách fulfilled và rejected", "hint": "Promise.allSettled, rồi tách kết quả theo status === 'fulfilled'."},
            {"name": "withTimeout phân giải bằng giá trị hoặc fallback", "hint": "Promise.race([promise, timerPromise]) trong đó timer phân giải bằng fallback sau ms."},
        ],
    },
)

print("Module 3 lessons + checkpoint written.")
