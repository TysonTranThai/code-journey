#!/usr/bin/env python3
"""Module 2 practices part 2: url-practice, observers-practice, dashboard-practice."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "advanced-dom-browser-apis"

# ── url-practice ────────────────────────────────────────────────────────────
write_practice(
    MOD, "url-practice",
    "URL & History — Practice",
    "Treat the URL as application state: parse it, derive views from it, and keep the back button working for your users.",
    "URL & History — Luyện tập",
    "Xem URL như trạng thái của ứng dụng: parse nó, suy ra view từ nó, và giữ nút back luôn hoạt động cho người dùng.",
    "url-history-api", 16, "intermediate",
    [
        {
            "id": "i2-url-parse-view",
            "title": "URL to View State",
            "prompt": 'Write `viewFromUrl(url)` — parse a full URL (use the URL constructor) and return { route, id, query }. route is the pathname without the leading slash; id is the value of /:id segments for paths like "products/42" (null otherwise); query is an object of searchParams (empty object when none).',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function viewFromUrl(url) {\n  // your code — use the URL constructor\n}\n",
            "tests": [
                {
                    "name": "parses route, id, and query",
                    "code": fn_wrap("viewFromUrl", "viewFromUrl") + r'''
const v = viewFromUrl("https://shop.dev/products/42?sort=price&dir=asc");
if (v.route !== "products/42") throw new Error("Route is pathname without leading slash.");
if (v.id !== "42") throw new Error("Numeric path segment becomes id.");
if (v.query.sort !== "price" || v.query.dir !== "asc") throw new Error("Search params become an object.");
''',
                    "hint": "new URL(url) gives pathname and searchParams.",
                },
                {
                    "name": "no id and no query still works",
                    "code": fn_wrap("viewFromUrl", "viewFromUrl") + r'''
const v = viewFromUrl("https://shop.dev/about");
if (v.route !== "about") throw new Error("Single-segment route.");
if (v.id !== null) throw new Error("No numeric segment => id null.");
if (Object.keys(v.query).length !== 0) throw new Error("No query => empty object.");
''',
                    "hint": "Default to null / empty — never undefined leakage.",
                },
            ],
        },
        {
            "id": "i2-history-nav",
            "title": "History Navigation Model",
            "prompt": 'Model pushState/replaceState semantics WITHOUT a browser. Write `createHistory()` returning { push, replace, back, canBack, current } — current is the latest entry pushed or replaced (null initially); push adds and makes canBack true; replace swaps the top entry WITHOUT changing depth; back moves one entry back and returns it (null at the start).',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function createHistory() {\n  // your code — no DOM needed\n}\n",
            "tests": [
                {
                    "name": "push and back walk the stack",
                    "code": fn_wrap("createHistory", "createHistory") + r'''
const h = createHistory();
if (h.current() !== null) throw new Error("Starts empty.");
h.push("/a"); h.push("/b");
if (h.current() !== "/b") throw new Error("Push sets current.");
if (h.back() !== "/a") throw new Error("Back returns the previous entry.");
if (h.back() !== null) throw new Error("Past the start, back yields null.");
''',
                    "hint": "A plain array plus an index is the whole model.",
                },
                {
                    "name": "replace swaps without growing",
                    "code": fn_wrap("createHistory", "createHistory") + r'''
const h = createHistory();
h.push("/a"); h.push("/b");
h.replace("/c");
if (h.current() !== "/c") throw new Error("Replace swaps the top entry.");
if (h.back() !== "/a") throw new Error("Depth unchanged — /b is gone, /a remains.");
''',
                    "hint": "replace mutates the top; it never adds.",
                },
            ],
        },
    ],
    {
        "i2-url-parse-view": {"title": "URL thành trạng thái view", "prompt": 'Viết `viewFromUrl(url)` — parse một URL đầy đủ (dùng constructor URL) và trả về { route, id, query }. route là pathname không có dấu gạch đầu; id là giá trị của đoạn /:id với path như "products/42" (null nếu không có); query là object từ searchParams (object rỗng khi không có).'},
        "i2-history-nav": {"title": "Mô hình điều hướng History", "prompt": 'Mô hình hoá ngữ nghĩa pushState/replaceState KHÔNG cần trình duyệt. Viết `createHistory()` trả về { push, replace, back, canBack, current } — current là entry mới nhất được push hoặc replace (null ban đầu); push thêm và biến canBack thành true; replace thay entry trên cùng KHÔNG đổi độ sâu; back lùi một entry và trả về nó (null ở điểm bắt đầu).'},
    },
    solutions=[
        (
            "i2-url-parse-view",
            'function viewFromUrl(url) {\n  const u = new URL(url);\n  const segs = u.pathname.replace(/^\\//, "").split("/").filter(Boolean);\n  const last = segs[segs.length - 1] || "";\n  const id = /^\\d+$/.test(last) ? last : null;\n  const query = {};\n  for (const [k, v] of u.searchParams) query[k] = v;\n  return { route: u.pathname.replace(/^\\//, ""), id, query };\n}',
            'function viewFromUrl(url) {\n  const u = new URL(url);\n  return { route: u.pathname, id: u.pathname.split("/")[1], query: u.search };\n}',
        ),
        (
            "i2-history-nav",
            'function createHistory() {\n  const stack = [];\n  let idx = -1;\n  return {\n    push(u) { stack.splice(idx + 1); stack.push(u); idx = stack.length - 1; },\n    replace(u) { if (idx >= 0) stack[idx] = u; else stack.push(u); idx = Math.max(idx, 0); },\n    back() { if (idx > 0) { idx--; return stack[idx + 1]; } return null; },\n    canBack() { return idx > 0; },\n    current() { return idx >= 0 ? stack[idx] : null; },\n  };\n}',
            'function createHistory() {\n  const stack = [];\n  return {\n    push(u) { stack.push(u); },\n    replace(u) { stack.push(u); },\n    back() { return stack.pop() ?? null; },\n    canBack() { return stack.length > 0; },\n    current() { return stack[stack.length - 1] ?? null; },\n  };\n}',
        ),
    ],
)

# ── observers-practice ──────────────────────────────────────────────────────
write_practice(
    MOD, "observers-practice",
    "Timers & Observers — Practice",
    "Time and visibility without jank: debounce vs throttle by signature, lazy-load simulation, and a resize model.",
    "Timer & Observer — Luyện tập",
    "Thời gian và hiển thị mà không jank: phân biệt debounce và throttle, mô phỏng lazy-load, và mô hình resize.",
    "timers-observers", 16, "intermediate",
    [
        {
            "id": "i2-debounce-vs-throttle",
            "title": "Debounce vs Throttle Signatures",
            "prompt": 'Write both, called with (fn, waitMs) and returning wrapped functions. For this exercise they run SYNCHRONOUSLY with a fake clock object { now() } passed as a third argument: debounce(fn, wait, clock) runs fn only after a gap of >= wait since the LAST call attempt (trailing edge); throttle(fn, wait, clock) runs fn immediately on the first call attempt, then blocks until wait has elapsed (leading edge).',
            "difficulty": "advanced",
            "level": "independent",
            "boilerplate": "function debounce(fn, wait, clock) {\n  // your code\n}\n\nfunction throttle(fn, wait, clock) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "debounce waits for the quiet",
                    "code": fn_wrap("debounce", "debounce") + r'''
let calls = 0;
const fn = () => calls++;
const clock = { now: () => t };
let t = 0;
const d = debounce(fn, 100, clock);
d(); t = 50; d(); t = 90; d();
t = 95;
if (calls !== 0) throw new Error("No quiet gap yet — fn must not have run.");
t = 200; d(); t = 310;
if (calls !== 1) throw new Error("After a 110ms gap the trailing call ran exactly once.");
''',
                    "hint": "Record lastAttempt; on each call, if now - lastAttempt >= wait, run and reset.",
                },
                {
                    "name": "throttle leads then locks",
                    "code": fn_wrap("throttle", "throttle") + r'''
let calls = 0;
const fn = () => calls++;
const clock = { now: () => t };
let t = 0;
const th = throttle(fn, 100, clock);
th();
if (calls !== 1) throw new Error("Leading edge: first call runs immediately.");
t = 50; th(); t = 99; th();
if (calls !== 1) throw new Error("Within the window, blocked.");
t = 150; th();
if (calls !== 2) throw new Error("Window elapsed => runs again.");
''',
                    "hint": "Record lastRun; run when now - lastRun >= wait, then set lastRun = now.",
                },
            ],
        },
        {
            "id": "i2-lazy-visibility",
            "title": "Lazy-Load on Visibility",
            "prompt": 'Model IntersectionObserver. Write `createLazyLoader()` returning { observe, intersect } — observe(el, onLoad) registers an element with a pending state; intersect(el) simulates it entering the viewport: the FIRST call marks it loaded, fires its onLoad(el) exactly once, and returns true; subsequent intersects return false and do nothing. Unknown elements return false.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function createLazyLoader() {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "onLoad fires exactly once",
                    "code": fn_wrap("createLazyLoader", "createLazyLoader") + r'''
const loader = createLazyLoader();
const el = { id: "img-1" };
let loads = 0;
loader.observe(el, () => loads++);
if (loader.intersect(el) !== true) throw new Error("First intersection loads.");
if (loads !== 1) throw new Error("onLoad fired once.");
if (loader.intersect(el) !== false) throw new Error("Second intersection is a no-op.");
if (loads !== 1) throw new Error("Still exactly one load.");
''',
                    "hint": "Store state on the element entry: pending → loaded.",
                },
                {
                    "name": "unobserved elements never load",
                    "code": fn_wrap("createLazyLoader", "createLazyLoader") + r'''
const loader = createLazyLoader();
if (loader.intersect({ id: "stranger" }) !== false) {
  throw new Error("Unknown element => false, no crash.");
}
''',
                    "hint": "Defensive lookup: no registration, no load.",
                },
            ],
        },
    ],
    {
        "i2-debounce-vs-throttle": {"title": "Chữ ký debounce vs throttle", "prompt": 'Viết cả hai, gọi dạng (fn, waitMs) và trả về hàm bọc. Trong bài này chúng chạy ĐỒNG BỘ với đồng hồ giả { now() } truyền làm tham số thứ ba: debounce(fn, wait, clock) chỉ chạy fn sau một khoảng lặng >= wait tính từ lần GẦN NHẤT gọi (trailing edge); throttle(fn, wait, clock) chạy fn NGAY ở lần gọi đầu, rồi chặn cho đến khi hết wait (leading edge).'},
        "i2-lazy-visibility": {"title": "Lazy-load theo hiển thị", "prompt": 'Mô hình hoá IntersectionObserver. Viết `createLazyLoader()` trả về { observe, intersect } — observe(el, onLoad) đăng ký một phần tử ở trạng thái chờ; intersect(el) mô phỏng nó vào viewport: lần gọi ĐẦU tiên đánh dấu loaded, gọi onLoad(el) đúng một lần, và trả true; các lần intersect sau trả false và không làm gì. Phần tử lạ trả false.'},
    },
    solutions=[
        (
            "i2-debounce-vs-throttle",
            'function debounce(fn, wait, clock) {\n  let lastAttempt = -Infinity;\n  return function () {\n    if (clock.now() - lastAttempt >= wait) {\n      lastAttempt = clock.now();\n      fn();\n    } else {\n      lastAttempt = clock.now();\n    }\n  };\n}\n\nfunction throttle(fn, wait, clock) {\n  let lastRun = -Infinity;\n  return function () {\n    if (clock.now() - lastRun >= wait) {\n      lastRun = clock.now();\n      fn();\n    }\n  };\n}',
            'function debounce(fn, wait, clock) {\n  return function () { fn(); };\n}\n\nfunction throttle(fn, wait, clock) {\n  return function () { fn(); };\n}',
        ),
        (
            "i2-lazy-visibility",
            'function createLazyLoader() {\n  const seen = new WeakSet();\n  const handlers = new WeakMap();\n  return {\n    observe(el, onLoad) { handlers.set(el, onLoad); },\n    intersect(el) {\n      if (!handlers.has(el) || seen.has(el)) return false;\n      seen.add(el);\n      handlers.get(el)(el);\n      return true;\n    },\n  };\n}',
            'function createLazyLoader() {\n  const handlers = new WeakMap();\n  return {\n    observe(el, onLoad) { handlers.set(el, onLoad); },\n    intersect(el) {\n      if (handlers.has(el)) { handlers.get(el)(el); return true; }\n      return false;\n    },\n  };\n}',
        ),
    ],
)

# ── dashboard-practice ──────────────────────────────────────────────────────
write_practice(
    MOD, "dashboard-practice",
    "Dashboard Mini-Build",
    "Combine the module's pieces into one coherent widget: declarative render from state, event delegation, and persistence.",
    "Mini-build Dashboard",
    "Kết hợp các mảnh của module thành một widget hoàn chỉnh: render khai báo từ state, event delegation, và lưu trữ.",
    "dashboard-checkpoint", 22, "advanced",
    [
        {
            "id": "i2-dashboard-render",
            "title": "State-to-DOM Renderer",
            "prompt": 'Write `renderTasks(state)` that returns an HTML STRING (never touches the DOM directly): tasks ordered by done ascending then priority weight high=3, medium=2, low=1, each rendered as `<li data-id="ID" class="done?">TITLE</li>` — class "done" only when done is true. Plus `nextId(state)` returning the next numeric id as a string.',
            "difficulty": "advanced",
            "level": "guided",
            "boilerplate": "function renderTasks(state) {\n  // your code — return an HTML string\n}\n\nfunction nextId(state) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "renders sorted, done class only where earned",
                    "code": fn_wrap("renderTasks", "renderTasks") + r'''
const state = { tasks: [
  { id: "1", title: "Ship", done: false, priority: "medium" },
  { id: "2", title: "Sleep", done: true, priority: "high" },
  { id: "3", title: "Test", done: false, priority: "high" },
] };
const html = renderTasks(state);
const order = [...html.matchAll(/<li data-id="(\d)"/g)].map((m) => m[1]);
if (order.join(",") !== "3,1,2") throw new Error("Open tasks first (high before medium), then done ones.");
if (!/<li data-id="2" class="done">Sleep<\/li>/.test(html)) throw new Error("Done task carries class=\"done\".");
if (/data-id="3" class="done"/.test(html)) throw new Error("Open task must not have the done class.");
''',
                    "hint": "Copy + sort with a weight map; build strings with map/join.",
                },
                {
                    "name": "nextId is max + 1",
                    "code": fn_wrap("nextId", "nextId") + r'''
if (nextId({ tasks: [{ id: "4" }, { id: "2" }] }) !== "5") throw new Error("Max id 4 => next 5.");
if (nextId({ tasks: [] }) !== "1") throw new Error("Empty list starts at 1.");
''',
                    "hint": "Numbers in, string out.",
                },
            ],
        },
        {
            "id": "i2-dashboard-delegate",
            "title": "Delegated Dashboard Events",
            "prompt": 'Model event delegation WITHOUT the DOM. Write `createDelegator(onToggle)` returning { wire, click } — wire(el, id) registers an element under a task id; click(target) simulates a click on target: if target is a registered element, call onToggle(id) for its CURRENT state, flip that state, and return true; unknown targets return false and do nothing. State per id starts at false (not done).',
            "difficulty": "advanced",
            "level": "guided",
            "boilerplate": "function createDelegator(onToggle) {\n  // your code — no DOM needed\n}\n",
            "tests": [
                {
                    "name": "one entry point toggles the clicked task",
                    "code": fn_wrap("createDelegator", "createDelegator") + r'''
const toggled = [];
const d = createDelegator((id, done) => toggled.push(id + ":" + done));
const a = { tag: "li" };
d.wire(a, "7");
if (d.click(a) !== true) throw new Error("Click on a wired element is handled.");
if (toggled.join(",") !== "7:false") throw new Error("First click reports the pre-toggle state (false) and toggles it.");
if (d.click(a) !== true) throw new Error("Second click handled too.");
if (toggled.join(",") !== "7:false,7:true") throw new Error("State flipped between clicks.");
''',
                    "hint": "A Map from element to { id, done }; click reads, reports, flips.",
                },
                {
                    "name": "clicks off the items are ignored",
                    "code": fn_wrap("createDelegator", "createDelegator") + r'''
const toggled = [];
const d = createDelegator((id) => toggled.push(id));
if (d.click({ tag: "ul" }) !== false) throw new Error("Bare container click => false.");
if (d.click({ tag: "li" }) !== false) throw new Error("An UNWIRED li is not a task.");
if (toggled.length !== 0) throw new Error("No handler call for unknown targets.");
''',
                    "hint": "Delegation guards the lookup: no registration, no action.",
                },
            ],
        },
    ],
    {
        "i2-dashboard-render": {"title": "Renderer từ state sang DOM", "prompt": 'Viết `renderTasks(state)` trả về CHUỖI HTML (không đụng DOM trực tiếp): các task sắp xếp theo done tăng dần rồi theo trọng số ưu tiên high=3, medium=2, low=1, mỗi task render thành `<li data-id="ID" class="done?">TITLE</li>` — class "done" chỉ khi done là true. Thêm `nextId(state)` trả về id số tiếp theo dạng chuỗi.'},
        "i2-dashboard-delegate": {"title": "Sự kiện dashboard dạng delegate", "prompt": 'Mô hình hoá event delegation KHÔNG cần DOM. Viết `createDelegator(onToggle)` trả về { wire, click } — wire(el, id) đăng ký một phần tử dưới một task id; click(target) mô phỏng click vào target: nếu target là phần tử đã đăng ký, gọi onToggle(id) với trạng thái HIỆN TẠI, lật trạng thái đó, và trả true; target lạ trả false và không làm gì. Trạng thái mỗi id bắt đầu là false (chưa done).'},
    },
    solutions=[
        (
            "i2-dashboard-render",
            'function renderTasks(state) {\n  const weight = { high: 3, medium: 2, low: 1 };\n  const sorted = [...state.tasks].sort((a, b) => {\n    if (a.done !== b.done) return a.done ? 1 : -1;\n    return (weight[b.priority] || 0) - (weight[a.priority] || 0);\n  });\n  return sorted\n    .map((t) => \'<li data-id="\' + t.id + \'"\' + (t.done ? \' class="done"\' : "") + ">" + t.title + "</li>")\n    .join("");\n}\n\nfunction nextId(state) {\n  const max = state.tasks.reduce((m, t) => Math.max(m, Number(t.id)), 0);\n  return String(max + 1);\n}',
            'function renderTasks(state) {\n  return state.tasks\n    .map((t) => \'<li data-id="\' + t.id + \'">" + t.title + "</li>")\n    .join("");\n}\n\nfunction nextId(state) {\n  return String(state.tasks.length + 1);\n}',
        ),
        (
            "i2-dashboard-delegate",
            'function createDelegator(onToggle) {\n  const items = new Map();\n  return {\n    wire(el, id) { items.set(el, { id, done: false }); },\n    click(target) {\n      const item = items.get(target);\n      if (!item) return false;\n      onToggle(item.id, item.done);\n      item.done = !item.done;\n      return true;\n    },\n  };\n}',
            'function createDelegator(onToggle) {\n  const items = new Map();\n  return {\n    wire(el, id) { items.set(el, id); },\n    click(target) {\n      onToggle(items.get(target));\n      return true;\n    },\n  };\n}',
        ),
    ],
)

print("Module 2 practices part 2 written.")
