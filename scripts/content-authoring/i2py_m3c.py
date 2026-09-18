#!/usr/bin/env python3
"""Module 3 practices part 2: fetch, cancellation, api-app mini build."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "asynchronous-javascript-apis"

# ── fetch-practice ──────────────────────────────────────────────────────────
write_practice(
    MOD,
    "fetch-practice",
    "fetch & Pagination — Practice",
    "An API client that behaves like production: response checking, a paginated lister, and query building with URLSearchParams.",
    "fetch & Phân trang — Luyện tập",
    "Một API client hành xử như production: kiểm tra phản hồi, bộ liệt kê phân trang, và dựng query bằng URLSearchParams.",
    "fetch-patterns", 20, "intermediate",
    [
        {
            "id": "i2-fetch-guard",
            "title": "Guarded JSON Fetch",
            "prompt": "Write `async function fetchJSON(url, fetchImpl)` — `fetchImpl` defaults to the real `fetch` (the tests inject a fake). It must:\n\n- throw `new Error(\"HTTP \" + status)` when `!res.ok`\n- return the parsed JSON otherwise\n- expose `method` and `headers` when a body is sent: `fetchJSON(url, fetchImpl, { method: \"POST\", body: value })` must call fetch with `method`, `body: JSON.stringify(value)`, and `Content-Type: application/json`.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "async function fetchJSON(url, fetchImpl, opts) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "returns parsed JSON on 2xx",
                    "code": fn_wrap("fetchJSON", "fetchJSON") + "\nconst fake = async () => ({ ok: true, status: 200, json: async () => ({ id: 9 }) });\nconst out = await fetchJSON(\"/api/x\", fake);\nif (out.id !== 9) throw new Error(\"A 200 response should return the parsed body.\");",
                    "hint": "const res = await fetchImpl(url, opts); if (!res.ok) throw ...; return res.json();",
                },
                {
                    "name": "throws on non-2xx with the status",
                    "code": fn_wrap("fetchJSON", "fetchJSON") + "\nconst fake404 = async () => ({ ok: false, status: 404, json: async () => ({}) });\nlet msg;\ntry { await fetchJSON(\"/api/x\", fake404); } catch (e) { msg = e.message; }\nif (msg !== \"HTTP 404\") throw new Error('A 404 must throw Error with message \"HTTP 404\" — got: ' + msg);",
                    "hint": "Check res.ok first; the message template is 'HTTP ' + res.status.",
                },
                {
                    "name": "sends JSON body with the right headers",
                    "code": fn_wrap("fetchJSON", "fetchJSON") + "\nlet captured;\nconst fake = async (u, o) => { captured = o; return { ok: true, status: 201, json: async () => ({}) }; };\nawait fetchJSON(\"/api/tasks\", fake, { method: \"POST\", body: { title: \"x\" } });\nif (captured.method !== \"POST\") throw new Error(\"method must be forwarded.\");\nif (captured.body !== '{\"title\":\"x\"}') throw new Error(\"body must be JSON.stringify(value) — got: \" + captured.body);\nif (captured.headers[\"Content-Type\"] !== \"application/json\") throw new Error(\"Content-Type: application/json is required when a body is sent.\");",
                    "hint": "When opts.body exists, build { ...opts, body: JSON.stringify(opts.body), headers: { 'Content-Type': 'application/json' } }.",
                },
            ],
        },
        {
            "id": "i2-paginate",
            "title": "Paginated Lister",
            "prompt": "Write `async function fetchAllPages(fetchPage, maxPages)` — `fetchPage(n)` returns a promise for `{ items, hasMore }`. Collect items page by page STARTING AT PAGE 1, stopping when `hasMore` is false or `maxPages` pages have been fetched (safety bound). RETURN all collected items in page order. Sequential is correct here: each request needs the previous page's verdict.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "async function fetchAllPages(fetchPage, maxPages) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "collects every page until hasMore is false",
                    "code": fn_wrap("fetchAllPages", "fetchAllPages") + "\nconst pages = { 1: { items: [\"a\"], hasMore: true }, 2: { items: [\"b\"], hasMore: true }, 3: { items: [\"c\"], hasMore: false } };\nlet requested = [];\nconst out = await fetchAllPages(async (n) => { requested.push(n); return pages[n]; }, 10);\nif (out.join() !== \"a,b,c\") throw new Error(\"All three pages' items in order.\");\nif (requested.join() !== \"1,2,3\") throw new Error(\"Pages 1..3 requested in order — page 3 said hasMore: false so stop.\");",
                    "hint": "Loop do { page = await fetchPage(n); items.push(...page.items); n++; } while (page.hasMore && n <= maxPages).",
                },
                {
                    "name": "maxPages is a hard safety bound",
                    "code": fn_wrap("fetchAllPages", "fetchAllPages") + "\nconst endless = async (n) => ({ items: [n], hasMore: true });\nlet calls = 0;\nconst wrapped = async (n) => { calls++; return endless(n); };\nconst out = await fetchAllPages(wrapped, 5);\nif (calls !== 5) throw new Error(\"With hasMore always true, exactly maxPages pages may be fetched.\");\nif (out.length !== 5) throw new Error(\"Five items collected.\");",
                    "hint": "Count fetched pages; break at maxPages even when hasMore is still true.",
                },
            ],
        },
        {
            "id": "i2-query-builder",
            "title": "Query Builder",
            "prompt": "Write `buildQuery(base, params)` that RETURNS the full URL string: `base` plus a query string built from the `params` object using URLSearchParams rules — skip keys whose value is `undefined` or `null`, stringify numbers, and encode special characters (spaces become `+` or `%20`). With no surviving params, return `base` unchanged.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function buildQuery(base, params) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "builds an encoded query string",
                    "code": fn_wrap("buildQuery", "buildQuery") + "\nconst url = buildQuery(\"/api/items\", { q: \"web dev\", page: 2 });\nconst parsed = new URL(url, \"https://x.dev\");\nif (parsed.pathname !== \"/api/items\") throw new Error(\"The base path must survive.\");\nif (parsed.searchParams.get(\"q\") !== \"web dev\") throw new Error(\"q must round-trip through URLSearchParams.\");\nif (parsed.searchParams.get(\"page\") !== \"2\") throw new Error(\"Numbers must be stringified.\");",
                    "hint": "new URLSearchParams(entries).toString() — attach with base + '?' + qs when qs is non-empty.",
                },
                {
                    "name": "skips undefined and null values",
                    "code": fn_wrap("buildQuery", "buildQuery") + "\nconst url = buildQuery(\"/api/items\", { q: \"x\", tag: undefined, sort: null });\nif (!url.startsWith(\"/api/items?\")) throw new Error(\"q survives, so a query string exists.\");\nif (url.includes(\"tag\") || url.includes(\"sort\")) throw new Error(\"undefined/null params must be dropped entirely.\");\nif (buildQuery(\"/api/items\", {}) !== \"/api/items\") throw new Error(\"No surviving params means bare base — no trailing '?'.\");",
                    "hint": "Object.entries + filter on value != null before constructing URLSearchParams.",
                },
            ],
        },
    ],
    {
        "i2-fetch-guard": {
            "title": "JSON fetch có bảo vệ",
            "prompt": "Viết `async function fetchJSON(url, fetchImpl)` — `fetchImpl` mặc định là `fetch` thật (test sẽ chèn bản giả). Hàm phải:\n\n- throw `new Error(\"HTTP \" + status)` khi `!res.ok`\n- trả về JSON đã parse trong trường hợp ngược lại\n- gửi kèm `method` và `headers` khi có body: `fetchJSON(url, fetchImpl, { method: \"POST\", body: value })` phải gọi fetch với `method`, `body: JSON.stringify(value)`, và `Content-Type: application/json`.",
            "tests": [
                {"name": "trả về JSON đã parse khi 2xx", "hint": "const res = await fetchImpl(url, opts); if (!res.ok) throw ...; return res.json();"},
                {"name": "throw khi không phải 2xx kèm status", "hint": "Kiểm tra res.ok trước; mẫu message là 'HTTP ' + res.status."},
                {"name": "gửi JSON body với header đúng", "hint": "Khi opts.body tồn tại, dựng { ...opts, body: JSON.stringify(opts.body), headers: { 'Content-Type': 'application/json' } }."},
            ],
        },
        "i2-paginate": {
            "title": "Bộ liệt kê phân trang",
            "prompt": "Viết `async function fetchAllPages(fetchPage, maxPages)` — `fetchPage(n)` trả về promise cho `{ items, hasMore }`. Gom items từng trang BẮT ĐẦU TỪ TRANG 1, dừng khi `hasMore` là false hoặc đã tải đủ `maxPages` trang (giới hạn an toàn). RETURN toàn bộ items đã gom theo thứ tự trang. Tuần tự là đúng ở đây: mỗi request cần verdict của trang trước.",
            "tests": [
                {"name": "gom đủ mọi trang cho đến khi hasMore là false", "hint": "Vòng lặp do { page = await fetchPage(n); items.push(...page.items); n++; } while (page.hasMore && n <= maxPages)."},
                {"name": "maxPages là giới hạn an toàn cứng", "hint": "Đếm số trang đã tải; break ở maxPages kể cả khi hasMore vẫn true."},
            ],
        },
        "i2-query-builder": {
            "title": "Trình dựng query",
            "prompt": "Viết `buildQuery(base, params)` RETURN chuỗi URL đầy đủ: `base` cộng với query string dựng từ object `params` theo quy tắc URLSearchParams — bỏ qua key có giá trị `undefined` hoặc `null`, chuyển số thành chuỗi, và encode ký tự đặc biệt (dấu cách thành `+` hoặc `%20`). Khi không còn param nào, trả về nguyên `base`.",
            "tests": [
                {"name": "dựng query string đã encode", "hint": "new URLSearchParams(entries).toString() — nối bằng base + '?' + qs khi qs khác rỗng."},
                {"name": "bỏ qua giá trị undefined và null", "hint": "Object.entries + lọc value != null trước khi dựng URLSearchParams."},
            ],
        },
    },
    [
        ["i2-fetch-guard", "async function fetchJSON(url, fetchImpl, opts = {}) {\n  const realFetch = fetchImpl ?? fetch;\n  const requestOpts = { ...opts };\n  if (requestOpts.body !== undefined) {\n    requestOpts.body = JSON.stringify(requestOpts.body);\n    requestOpts.headers = { \"Content-Type\": \"application/json\", ...(requestOpts.headers ?? {}) };\n  }\n  const res = await realFetch(url, requestOpts);\n  if (!res.ok) {\n    throw new Error(\"HTTP \" + res.status);\n  }\n  return res.json();\n}", "async function fetchJSON(url, fetchImpl, opts = {}) {\n  const res = await fetchImpl(url, opts);\n  return res.json();\n}"],
        ["i2-paginate", "async function fetchAllPages(fetchPage, maxPages) {\n  const items = [];\n  let page = 1;\n  let result;\n  do {\n    result = await fetchPage(page);\n    items.push(...result.items);\n    page++;\n  } while (result.hasMore && page <= maxPages);\n  return items;\n}", "async function fetchAllPages(fetchPage, maxPages) {\n  const first = await fetchPage(1);\n  return first.items;\n}"],
        ["i2-query-builder", "function buildQuery(base, params = {}) {\n  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== null);\n  if (entries.length === 0) return base;\n  const qs = new URLSearchParams(entries);\n  return base + \"?\" + qs.toString();\n}", "function buildQuery(base, params = {}) {\n  return base + \"?\" + JSON.stringify(params);\n}"],
    ],
)

# ── cancellation-practice ───────────────────────────────────────────────────
write_practice(
    MOD,
    "cancellation-practice",
    "Cancellation — Practice",
    "Abort stale work: a search-as-you-type controller, an abortable delay, and an AbortError classifier.",
    "Hủy request — Luyện tập",
    "Hủy công việc lỗi thời: bộ điều khiển search-as-you-type, delay có thể hủy, và bộ phân loại AbortError.",
    "cancellation-abort", 15, "intermediate",
    [
        {
            "id": "i2-abort-classify",
            "title": "Abort Classifier",
            "prompt": "Write `classifyError(err)` that RETURNS `\"aborted\"` when `err` is an object with `err.name === \"AbortError\"`, `\"network\"` when `err.message` contains `\"fetch\"` or `\"network\"` (case-insensitive), and `\"other\"` for everything else (including non-Error values).",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function classifyError(err) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "AbortError by name wins first",
                    "code": fn_wrap("classifyError", "classifyError") + "\nconst e = new Error(\"fetch failed for /api\");\ne.name = \"AbortError\";\nif (classifyError(e) !== \"aborted\") throw new Error(\"name === 'AbortError' must classify as aborted, even if the message mentions fetch.\");\nif (classifyError(new Error(\"Failed to fetch\")) !== \"network\") throw new Error(\"A fetch/network message classifies as network.\");",
                    "hint": "Check err && err.name === 'AbortError' before looking at the message.",
                },
                {
                    "name": "handles junk input without throwing",
                    "code": fn_wrap("classifyError", "classifyError") + "\nif (classifyError(null) !== \"other\") throw new Error(\"null must not crash — classify as other.\");\nif (classifyError(\"weird\") !== \"other\") throw new Error(\"Non-Error values are other.\");\nif (classifyError(new Error(\"boom\")) !== \"other\") throw new Error(\"Plain errors are other.\");",
                    "hint": "Guard with err && typeof err === 'object' before touching properties.",
                },
            ],
        },
        {
            "id": "i2-abortable-delay",
            "title": "Abortable Delay",
            "prompt": "Write `abortableDelay(ms, signal)` returning a promise that resolves with `\"done\"` after `ms` — UNLESS `signal` aborts first, in which case it must REJECT with an error whose `name` is `\"AbortError\"`. If the signal is already aborted, reject immediately.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function abortableDelay(ms, signal) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "resolves when not aborted",
                    "code": fn_wrap("abortableDelay", "abortableDelay") + "\nconst out = await abortableDelay(10, new AbortController().signal);\nif (out !== \"done\") throw new Error(\"An un-aborted delay resolves with 'done'.\");",
                    "hint": "setTimeout(() => resolve('done'), ms) — wire signal.addEventListener('abort', reject).",
                },
                {
                    "name": "rejects with AbortError when aborted mid-flight",
                    "code": fn_wrap("abortableDelay", "abortableDelay") + "\nconst c = new AbortController();\nconst p = abortableDelay(60, c.signal);\nsetTimeout(() => c.abort(), 5);\nlet err;\ntry { await p; } catch (e) { err = e; }\nif (!err || err.name !== \"AbortError\") throw new Error(\"Mid-flight abort must reject with err.name === 'AbortError'.\");",
                    "hint": "The abort listener calls a reject function captured from the promise executor.",
                },
                {
                    "name": "already-aborted signal rejects immediately",
                    "code": fn_wrap("abortableDelay", "abortableDelay") + "\nconst c = new AbortController();\nc.abort();\nlet err;\ntry { await abortableDelay(60, c.signal); } catch (e) { err = e; }\nif (!err || err.name !== \"AbortError\") throw new Error(\"A pre-aborted signal rejects immediately with AbortError.\");",
                    "hint": "Check signal?.aborted at the top and reject synchronously in that path.",
                },
            ],
        },
        {
            "id": "i2-latest-wins",
            "title": "Latest Search Wins",
            "prompt": "Write `createSearcher(runQuery)` that mimics search-as-you-type. It RETURNS `{ search, result }`. `search(term)` starts `runQuery(term)` (returning a promise), aborts/cancels any PREVIOUS in-flight search by marking it stale, and remembers this call as current. `result` is an async function awaiting the CURRENT search and returning its value — a stale (superseded) search must never update the result.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function createSearcher(runQuery) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "result follows the latest search",
                    "code": fn_wrap("createSearcher", "createSearcher") + "\nconst s = createSearcher(async (t) => { await new Promise((r) => setTimeout(r, 10)); return \"results:\" + t; });\ns.search(\"a\");\ns.search(\"ab\");\ns.search(\"abc\");\nconst out = await s.result();\nif (out !== \"results:abc\") throw new Error(\"The most recent search's value must win.\");",
                    "hint": "Keep a currentId counter; each search captures its id and only writes the result if id === currentId.",
                },
                {
                    "name": "a superseded search never updates the result",
                    "code": fn_wrap("createSearcher", "createSearcher") + "\nconst finished = [];\nconst s = createSearcher(async (t) => {\n  await new Promise((r) => setTimeout(r, t === \"slow\" ? 40 : 5));\n  finished.push(t);\n  return \"results:\" + t;\n});\ns.search(\"slow\");\ns.search(\"fast\");\nconst out = await s.result();\nawait new Promise((r) => setTimeout(r, 60));\nif (out !== \"results:fast\") throw new Error(\"The slow first search must not overwrite the fast second one.\");",
                    "hint": "The classic race: the guard is comparing ids at completion time, not cancelling the timer.",
                },
            ],
        },
    ],
    {
        "i2-abort-classify": {
            "title": "Bộ phân loại Abort",
            "prompt": "Viết `classifyError(err)` RETURN `\"aborted\"` khi `err` là object với `err.name === \"AbortError\"`, `\"network\"` khi `err.message` chứa `\"fetch\"` hoặc `\"network\"` (không phân biệt hoa thường), và `\"other\"` cho mọi trường hợp khác (kể cả giá trị không phải Error).",
            "tests": [
                {"name": "AbortError theo name thắng trước", "hint": "Kiểm tra err && err.name === 'AbortError' trước khi nhìn vào message."},
                {"name": "xử lý input rác không bị crash", "hint": "Chặn bằng err && typeof err === 'object' trước khi đụng vào thuộc tính."},
            ],
        },
        "i2-abortable-delay": {
            "title": "Delay có thể hủy",
            "prompt": "Viết `abortableDelay(ms, signal)` trả về một promise phân giải bằng `\"done\"` sau `ms` — TRỪ KHI `signal` bị abort trước, khi đó nó phải REJECT với một lỗi có `name` là `\"AbortError\"`. Nếu signal đã bị abort sẵn, reject ngay lập tức.",
            "tests": [
                {"name": "phân giải khi không bị hủy", "hint": "setTimeout(() => resolve('done'), ms) — nối signal.addEventListener('abort', reject)."},
                {"name": "reject với AbortError khi bị hủy giữa đường", "hint": "Listener abort gọi hàm reject đã được bắt từ promise executor."},
                {"name": "signal đã abort reject ngay lập tức", "hint": "Kiểm tra signal?.aborted ở đầu hàm và reject đồng bộ trong nhánh đó."},
            ],
        },
        "i2-latest-wins": {
            "title": "Tìm kiếm mới nhất thắng",
            "prompt": "Viết `createSearcher(runQuery)` mô phỏng search-as-you-type. Nó RETURN `{ search, result }`. `search(term)` khởi động `runQuery(term)` (trả về promise), hủy mọi lần tìm kiếm TRƯỚC ĐÓ đang bay bằng cách đánh dấu nó lỗi thời, và ghi nhớ lần gọi này là hiện tại. `result` là một hàm async chờ lần tìm kiếm HIỆN TẠI và trả về giá trị của nó — một lần tìm lỗi thời (bị thay thế) không bao giờ được cập nhật kết quả.",
            "tests": [
                {"name": "kết quả theo lần tìm kiếm mới nhất", "hint": "Giữ bộ đếm currentId; mỗi lần search bắt id của mình và chỉ ghi kết quả khi id === currentId."},
                {"name": "lần tìm bị thay thế không bao giờ cập nhật kết quả", "hint": "Race kinh điển: chốt hạ là so sánh id tại thời điểm hoàn tất, chứ không phải hủy timer."},
            ],
        },
    },
    [
        ["i2-abort-classify", "function classifyError(err) {\n  if (err && typeof err === \"object\" && err.name === \"AbortError\") return \"aborted\";\n  if (err && typeof err === \"object\" && typeof err.message === \"string\") {\n    const m = err.message.toLowerCase();\n    if (m.includes(\"fetch\") || m.includes(\"network\")) return \"network\";\n  }\n  return \"other\";\n}", "function classifyError(err) {\n  return \"other\";\n}"],
        ["i2-abortable-delay", "function abortableDelay(ms, signal) {\n  return new Promise((resolve, reject) => {\n    if (signal && signal.aborted) {\n      const e = new Error(\"aborted\");\n      e.name = \"AbortError\";\n      reject(e);\n      return;\n    }\n    const onAbort = () => {\n      clearTimeout(t);\n      const e = new Error(\"aborted\");\n      e.name = \"AbortError\";\n      reject(e);\n    };\n    const t = setTimeout(() => {\n      signal && signal.removeEventListener(\"abort\", onAbort);\n      resolve(\"done\");\n    }, ms);\n    signal && signal.addEventListener(\"abort\", onAbort, { once: true });\n  });\n}", "function abortableDelay(ms, signal) {\n  return new Promise((resolve) => setTimeout(() => resolve(\"done\"), ms));\n}"],
        ["i2-latest-wins", "function createSearcher(runQuery) {\n  let currentId = 0;\n  let currentPromise = null;\n  return {\n    search(term) {\n      const id = ++currentId;\n      currentPromise = runQuery(term).then((value) => {\n        if (id === currentId) return value;\n        return currentPromise;\n      });\n      return id;\n    },\n    result() {\n      return currentPromise;\n    },\n  };\n}", "function createSearcher(runQuery) {\n  let currentPromise = null;\n  return {\n    search(term) {\n      currentPromise = runQuery(term);\n      return currentPromise;\n    },\n    result() {\n      return currentPromise;\n    },\n  };\n}"],
    ],
)

# ── api-app-practice (mini build) ───────────────────────────────────────────
write_practice(
    MOD,
    "api-app-practice",
    "Mini Build: API-Powered Widget",
    "Assemble the module: a tiny API client with cache + retry, and a state machine for async UI.",
    "Dự án nhỏ: Widget lấy dữ liệu từ API",
    "Lắp ráp cả module: một API client nhỏ với cache + retry, và một máy trạng thái cho UI bất đồng bộ.",
    "api-app-checkpoint", 25, "intermediate",
    [
        {
            "id": "i2-state-machine",
            "title": "Async UI State Machine",
            "prompt": "Write `createViewState()` — a tiny state machine for an async view. It RETURNS `{ get, load }`:\n\n- state starts as `{ status: \"idle\" }`\n- `load(fetchFn)` sets `{ status: \"loading\" }`, awaits `fetchFn()`\n  - success → `{ status: \"success\", data }`\n  - failure → `{ status: \"error\", message }` (err.message)\n- `get()` returns the CURRENT state object (a new object each call is fine)\n- calling `load` again while one is in flight is allowed — the LAST call wins (stale completions must not overwrite the newer state)",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function createViewState() {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "walks idle → loading → success",
                    "code": fn_wrap("createViewState", "createViewState") + "\nconst v = createViewState();\nif (v.get().status !== \"idle\") throw new Error(\"Starts idle.\");\nconst p = v.load(async () => \"payload\");\nif (v.get().status !== \"loading\") throw new Error(\"Immediately after load, status is loading.\");\nawait p;\nconst s = v.get();\nif (s.status !== \"success\" || s.data !== \"payload\") throw new Error(\"After the fetch resolves: { status: 'success', data }.\");",
                    "hint": "Keep the state object in a closure; load mutates then returns the promise it created.",
                },
                {
                    "name": "failure becomes an error state",
                    "code": fn_wrap("createViewState", "createViewState") + "\nconst v = createViewState();\nawait v.load(async () => { throw new Error(\"503 upstream\"); });\nconst s = v.get();\nif (s.status !== \"error\" || s.message !== \"503 upstream\") throw new Error(\"Rejection maps to { status: 'error', message: err.message }.\");",
                    "hint": "try/catch around the await; catch stores message and must not rethrow.",
                },
                {
                    "name": "last load wins over a stale one",
                    "code": fn_wrap("createViewState", "createViewState") + "\nconst v = createViewState();\nconst slow = v.load(async () => { await new Promise((r) => setTimeout(r, 60)); return \"slow-data\"; });\nconst fast = v.load(async () => { await new Promise((r) => setTimeout(r, 10)); return \"fast-data\"; });\nawait slow; await fast;\nconst s = v.get();\nif (s.status !== \"success\" || s.data !== \"fast-data\") throw new Error(\"The slow earlier load must not overwrite the newer one's success state.\");",
                    "hint": "Capture a load id when load() is called; only write success/error if the id is still current.",
                },
            ],
        },
        {
            "id": "i2-cached-client",
            "title": "Caching API Client",
            "prompt": "Write `createClient(fetchImpl)` — an API client with:\n\n- `get(url)` — uses a per-client cache: the first call fetches and caches the PROMISE; repeat calls return the same promise (one flight per URL until invalidated)\n- `invalidate(url)` — drops the cache entry for that URL (next `get` re-fetches)\n- `invalidateAll()` — clears everything\n- `post(url, body)` — never cached; sends `{ method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } }` and resolves with the parsed response\n- all fetches go through the injected `fetchImpl(url, opts)`",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function createClient(fetchImpl) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "get dedupes and caches per URL",
                    "code": fn_wrap("createClient", "createClient") + "\nlet calls = 0;\nconst fake = async (u) => { calls++; await new Promise((r) => setTimeout(r, 5)); return { ok: true, status: 200, json: async () => ({ url: u }) }; };\nconst c = createClient(fake);\nconst [a, b] = await Promise.all([c.get(\"/x\"), c.get(\"/x\")]);\nif (a.url !== \"/x\" || b.url !== \"/x\") throw new Error(\"Both gets resolve with the fetched body.\");\nif (calls !== 1) throw new Error(\"Concurrent gets share one flight.\");\nawait c.get(\"/x\");\nif (calls !== 1) throw new Error(\"The cached promise is reused after completion.\");",
                    "hint": "Same pattern as the checkpoint loader — cache the promise, not the value.",
                },
                {
                    "name": "invalidate forces a refetch",
                    "code": fn_wrap("createClient", "createClient") + "\nlet calls = 0;\nconst fake = async (u) => { calls++; return { ok: true, status: 200, json: async () => ({ n: calls }) }; };\nconst c = createClient(fake);\nawait c.get(\"/x\");\nc.invalidate(\"/x\");\nconst again = await c.get(\"/x\");\nif (again.n !== 2) throw new Error(\"After invalidate, the next get must re-fetch (n === 2).\");\nc.invalidateAll();\nawait c.get(\"/y\");\nif (calls !== 3) throw new Error(\"invalidateAll drops every entry.\");",
                    "hint": "Map.delete(url) for invalidate; clear() for invalidateAll.",
                },
                {
                    "name": "post is never cached and sends JSON",
                    "code": fn_wrap("createClient", "createClient") + "\nconst captured = [];\nconst fake = async (u, o) => { captured.push({ u, o }); return { ok: true, status: 201, json: async () => ({ created: true }) }; };\nconst c = createClient(fake);\nconst out = await c.post(\"/tasks\", { title: \"ship it\" });\nif (out.created !== true) throw new Error(\"post resolves with the parsed body.\");\nif (captured[0].o.method !== \"POST\") throw new Error(\"method must be POST.\");\nif (captured[0].o.body !== '{\"title\":\"ship it\"}') throw new Error(\"body must be JSON stringified.\");\nawait c.post(\"/tasks\", { title: \"again\" });\nif (captured.length !== 2) throw new Error(\"A second post must hit the transport again — post is never cached.\");",
                    "hint": "post bypasses the cache entirely; build opts with method/body/headers then parse res.json().",
                },
            ],
        },
    ],
    {
        "i2-state-machine": {
            "title": "Máy trạng thái UI bất đồng bộ",
            "prompt": "Viết `createViewState()` — một máy trạng thái nhỏ cho view bất đồng bộ. Nó RETURN `{ get, load }`:\n\n- trạng thái khởi đầu là `{ status: \"idle\" }`\n- `load(fetchFn)` đặt `{ status: \"loading\" }`, await `fetchFn()`\n  - thành công → `{ status: \"success\", data }`\n  - thất bại → `{ status: \"error\", message }` (err.message)\n- `get()` trả về object trạng thái HIỆN TẠI (mỗi lần gọi một object mới cũng được)\n- gọi `load` khi một lần đang bay vẫn được cho phép — lần gọi CUỐI thắng (các lần hoàn tất lỗi thời không được ghi đè trạng thái mới hơn)",
            "tests": [
                {"name": "đi qua idle → loading → success", "hint": "Giữ object trạng thái trong closure; load thay đổi trạng thái rồi trả về promise nó tạo ra."},
                {"name": "thất bại trở thành trạng thái lỗi", "hint": "try/catch quanh await; catch lưu message và không được ném tiếp."},
                {"name": "lần load cuối thắng lần lỗi thời", "hint": "Bắt một load id khi load() được gọi; chỉ ghi success/error nếu id vẫn còn là hiện tại."},
            ],
        },
        "i2-cached-client": {
            "title": "API client có cache",
            "prompt": "Viết `createClient(fetchImpl)` — một API client với:\n\n- `get(url)` — dùng cache theo client: lần gọi đầu fetch và cache PROMISE; các lần gọi sau trả về cùng promise đó (một chuyến bay cho mỗi URL cho đến khi bị vô hiệu hóa)\n- `invalidate(url)` — xóa mục cache cho URL đó (lần `get` kế sẽ fetch lại)\n- `invalidateAll()` — xóa hết\n- `post(url, body)` — không bao giờ cache; gửi `{ method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } }` và phân giải với phản hồi đã parse\n- mọi fetch đi qua `fetchImpl(url, opts)` được chèn vào",
            "tests": [
                {"name": "get khử trùng lặp và cache theo URL", "hint": "Cùng mẫu với loader trong bài kiểm tra — cache promise, không phải giá trị."},
                {"name": "invalidate ép fetch lại", "hint": "Map.delete(url) cho invalidate; clear() cho invalidateAll."},
                {"name": "post không bao giờ cache và gửi JSON", "hint": "post đi vòng qua cache hoàn toàn; dựng opts với method/body/headers rồi parse res.json()."},
            ],
        },
    },
    [
        ["i2-state-machine", "function createViewState() {\n  let state = { status: \"idle\" };\n  let currentId = 0;\n  return {\n    get() {\n      return { ...state };\n    },\n    load(fetchFn) {\n      const id = ++currentId;\n      state = { status: \"loading\" };\n      return fetchFn().then(\n        (data) => {\n          if (id === currentId) state = { status: \"success\", data };\n        },\n        (err) => {\n          if (id === currentId) state = { status: \"error\", message: err.message };\n        },\n      );\n    },\n  };\n}", "function createViewState() {\n  let state = { status: \"idle\" };\n  return {\n    get() { return { ...state }; },\n    async load(fetchFn) {\n      state = { status: \"loading\" };\n      state = { status: \"success\", data: await fetchFn() };\n    },\n  };\n}"],
        ["i2-cached-client", "function createClient(fetchImpl) {\n  const cache = new Map();\n  async function request(url, opts) {\n    const res = await fetchImpl(url, opts);\n    if (!res.ok) throw new Error(\"HTTP \" + res.status);\n    return res.json();\n  }\n  return {\n    get(url) {\n      if (!cache.has(url)) cache.set(url, request(url));\n      return cache.get(url);\n    },\n    invalidate(url) {\n      cache.delete(url);\n    },\n    invalidateAll() {\n      cache.clear();\n    },\n    post(url, body) {\n      return request(url, {\n        method: \"POST\",\n        body: JSON.stringify(body),\n        headers: { \"Content-Type\": \"application/json\" },\n      });\n    },\n  };\n}", "function createClient(fetchImpl) {\n  return {\n    async get(url) {\n      const res = await fetchImpl(url);\n      return res.json();\n    },\n    invalidate() {},\n    invalidateAll() {},\n    async post(url, body) {\n      const res = await fetchImpl(url, { method: \"POST\", body });\n      return res.json();\n    },\n  };\n}"],
    ],
)

print("Module 3 practices part 2 (fetch, cancellation, api-app) written.")
