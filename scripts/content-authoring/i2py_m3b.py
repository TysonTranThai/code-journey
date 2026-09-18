#!/usr/bin/env python3
"""Module 3 practices: event-loop, promises, combinators, fetch, cancellation, api-app."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "asynchronous-javascript-apis"

# ── event-loop-practice ─────────────────────────────────────────────────────
write_practice(
    MOD,
    "event-loop-practice",
    "Event Loop — Practice",
    "Predict and then implement: ordering quiz as code, a microtask vs macrotask probe, and an async task queue runner.",
    "Event Loop — Luyện tập",
    "Dự đoán rồi cài đặt: câu hỏi thứ tự dưới dạng code, đầu dò microtask so với macrotask, và bộ chạy hàng đợi task bất đồng bộ.",
    "event-loop", 15, "intermediate",
    [
        {
            "id": "i2-ordering-probe",
            "title": "Execution Order Probe",
            "prompt": "Write `runProbe(log)` — `log` is a function that records strings. WITHOUT calling `log` directly except inside the callbacks, schedule exactly this sequence using `log`:\n\n1. synchronously: `log(\"sync\")`\n2. a microtask: `log(\"micro\")` (use Promise.resolve().then)\n3. a macrotask: `log(\"macro\")` (use setTimeout with 0)\n\nThe probe function itself must return the string \"scheduled\" immediately, and all three logs must have happened by the time the test awaits one 20ms timeout.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function runProbe(log) {\n  // schedule the three logs\n  return \"scheduled\";\n}\n",
            "tests": [
                {
                    "name": "returns immediately, logs happen later",
                    "code": fn_wrap("runProbe", "runProbe") + "\nconst seen = [];\nconst r = runProbe((s) => seen.push(s));\nif (r !== \"scheduled\") throw new Error(\"runProbe must return 'scheduled' synchronously.\");\nif (seen.length !== 1 || seen[0] !== \"sync\") throw new Error(\"Only the synchronous log should have run so far.\");\nawait new Promise((r) => setTimeout(r, 20));\nif (seen.join() !== \"sync,micro,macro\") throw new Error(\"Final order must be sync, micro, macro — got: \" + seen.join());",
                    "hint": "Log 'sync' first, then Promise.resolve().then(() => log('micro')), then setTimeout(() => log('macro'), 0).",
                },
                {
                    "name": "microtask beats macrotask",
                    "code": fn_wrap("runProbe", "runProbe") + "\nconst seen = [];\nrunProbe((s) => seen.push(s));\nawait new Promise((r) => setTimeout(r, 20));\nif (seen[1] !== \"micro\" || seen[2] !== \"macro\") throw new Error(\"Microtasks always drain before the next macrotask.\");",
                    "hint": "Promise callbacks queue as microtasks; setTimeout as macrotasks — the loop drains microtasks first.",
                },
            ],
        },
        {
            "id": "i2-yield-loop",
            "title": "Chunked Processing",
            "prompt": "Write `async function processChunks(items, handler, chunkSize)` that processes `items` in groups of `chunkSize`: call `await handler(batch)` for each batch, and between batches `await` one macrotask tick (`await new Promise((r) => setTimeout(r, 0))`) so the browser can paint. RETURN an array of every handler result in order.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "async function processChunks(items, handler, chunkSize) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "processes every item in batches, in order",
                    "code": fn_wrap("processChunks", "processChunks") + "\nconst batches = [];\nconst out = await processChunks([1,2,3,4,5], async (b) => { batches.push([...b]); return b.length; }, 2);\nif (out.join() !== \"2,2,1\") throw new Error(\"Results should be the batch sizes in order (2,2,1).\");\nif (batches.length !== 3) throw new Error(\"Five items at size 2 make three batches.\");\nif (batches[0].join() !== \"1,2\" || batches[1].join() !== \"3,4\" || batches[2].join() !== \"5\") throw new Error(\"Batches must slice the input in order.\");",
                    "hint": "for (let i = 0; i < items.length; i += chunkSize), slice, await handler, push result, then await the tick.",
                },
                {
                    "name": "yields to the macrotask queue between batches",
                    "code": fn_wrap("processChunks", "processChunks") + "\nlet timerRanDuring = false;\nsetTimeout(() => { timerRanDuring = true; }, 0);\nconst seen = [];\nawait processChunks([1,2,3,4], async (b) => { seen.push(b.length); return 0; }, 1);\nif (!timerRanDuring) throw new Error(\"The setTimeout callback should have run BETWEEN batch handlers — you must await a macrotask tick between batches.\");\nif (seen.length !== 4) throw new Error(\"Every batch should be handled.\");",
                    "hint": "After each handler call: await new Promise((r) => setTimeout(r, 0)).",
                },
            ],
        },
    ],
    {
        "i2-ordering-probe": {
            "title": "Đầu dò thứ tự thực thi",
            "prompt": "Viết `runProbe(log)` — `log` là một function ghi lại chuỗi. KHÔNG gọi `log` trực tiếp ngoài các callback, hãy xếp lịch đúng chuỗi sau bằng `log`:\n\n1. đồng bộ: `log(\"sync\")`\n2. một microtask: `log(\"micro\")` (dùng Promise.resolve().then)\n3. một macrotask: `log(\"macro\")` (dùng setTimeout với 0)\n\nHàm probe phải return chuỗi \"scheduled\" ngay lập tức, và cả ba log phải xảy ra xong khi test chờ một timeout 20ms.",
            "tests": [
                {"name": "return ngay, log xảy ra sau", "hint": "Log 'sync' trước, rồi Promise.resolve().then(() => log('micro')), rồi setTimeout(() => log('macro'), 0)."},
                {"name": "microtask thắng macrotask", "hint": "Callback của promise xếp vào microtask; setTimeout xếp vào macrotask — vòng lặp xả microtask trước."},
            ],
        },
        "i2-yield-loop": {
            "title": "Xử lý theo chunk",
            "prompt": "Viết `async function processChunks(items, handler, chunkSize)` xử lý `items` theo nhóm `chunkSize` phần tử: gọi `await handler(batch)` cho từng nhóm, và giữa các nhóm `await` một nhịp macrotask (`await new Promise((r) => setTimeout(r, 0))`) để trình duyệt kịp vẽ. RETURN một mảng gồm mọi kết quả của handler theo đúng thứ tự.",
            "tests": [
                {"name": "xử lý hết mọi phần tử theo nhóm, đúng thứ tự", "hint": "for (let i = 0; i < items.length; i += chunkSize), slice, await handler, push kết quả, rồi await một nhịp."},
                {"name": "nhường macrotask giữa các nhóm", "hint": "Sau mỗi lần gọi handler: await new Promise((r) => setTimeout(r, 0))."},
            ],
        },
    },
    [
        ["i2-ordering-probe", "function runProbe(log) {\n  log(\"sync\");\n  Promise.resolve().then(() => log(\"micro\"));\n  setTimeout(() => log(\"macro\"), 0);\n  return \"scheduled\";\n}", "function runProbe(log) {\n  setTimeout(() => log(\"macro\"), 0);\n  Promise.resolve().then(() => log(\"micro\"));\n  log(\"sync\");\n  return \"scheduled\";\n}"],
        ["i2-yield-loop", "async function processChunks(items, handler, chunkSize) {\n  const results = [];\n  for (let i = 0; i < items.length; i += chunkSize) {\n    const batch = items.slice(i, i + chunkSize);\n    results.push(await handler(batch));\n    await new Promise((r) => setTimeout(r, 0));\n  }\n  return results;\n}", "async function processChunks(items, handler, chunkSize) {\n  const results = [];\n  for (let i = 0; i < items.length; i += chunkSize) {\n    results.push(handler(items.slice(i, i + chunkSize)));\n  }\n  return results;\n}"],
    ],
)

# ── promises-practice ───────────────────────────────────────────────────────
write_practice(
    MOD,
    "promises-practice",
    "Promises — Practice",
    "Chain with fallbacks: a resilient value pipeline, sequential dependency chains, and error recovery with finally semantics.",
    "Promise — Luyện tập",
    "Nối chuỗi với phương án dự phòng: pipeline giá trị kiên cường, chuỗi phụ thuộc tuần tự, và hồi phục lỗi với ngữ nghĩa finally.",
    "promises", 18, "intermediate",
    [
        {
            "id": "i2-chain-transform",
            "title": "Resilient Pipeline",
            "prompt": "Write `async function pipeline(value, steps)` where `steps` is an array of sync-or-async functions. Await each step in order, feeding each result into the next. If a step throws, RETURN `{ ok: false, error: err.message }`; otherwise RETURN `{ ok: true, value: finalValue }`.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "async function pipeline(value, steps) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "runs sync and async steps in order",
                    "code": fn_wrap("pipeline", "pipeline") + "\nconst out = await pipeline(2, [async (x) => x * 10, (x) => x + 1, async (x) => \"n=\" + x]);\nif (!out.ok || out.value !== \"n=21\") throw new Error(\"2 * 10 + 1 = 21, then formatted — expected { ok: true, value: 'n=21' }.\");",
                    "hint": "for (const s of steps) value = await s(value); — await accepts sync return values too.",
                },
                {
                    "name": "converts a thrown error into a result object",
                    "code": fn_wrap("pipeline", "pipeline") + "\nconst out = await pipeline(1, [(x) => x + 1, () => { throw new Error(\"boom\"); }, (x) => x * 100]);\nif (out.ok !== false) throw new Error(\"A failing step must produce { ok: false }.\");\nif (out.error !== \"boom\") throw new Error(\"error should carry the thrown message.\");",
                    "hint": "Wrap the loop in try/catch; on catch return { ok: false, error: err.message }.",
                },
                {
                    "name": "empty steps return the value unchanged",
                    "code": fn_wrap("pipeline", "pipeline") + "\nconst out = await pipeline(\"v\", []);\nif (out.ok !== true || out.value !== \"v\") throw new Error(\"With no steps, the value passes through unchanged.\");",
                    "hint": "The loop simply never runs.",
                },
            ],
        },
        {
            "id": "i2-seq-chain",
            "title": "Sequential Dependency Chain",
            "prompt": "Write `async function fetchProfile(db)` where `db` provides `getUser(id)`, `getSettings(userId)`, and `getFriends(userId)` — each returning promises. Fetch the user for id 7 first, then settings and friends IN PARALLEL using the user's id. RETURN `{ user, settings, friends }`. If the user fetch fails, RETURN `{ error: \"user-not-found\" }`.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "async function fetchProfile(db) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "user first, then settings and friends in parallel",
                    "code": fn_wrap("fetchProfile", "fetchProfile") + "\nconst order = [];\nconst db = {\n  getUser: async (id) => { order.push(\"user\"); return { id, name: \"Ada\" }; },\n  getSettings: async (uid) => { order.push(\"settings\"); return { theme: uid === 7 ? \"dark\" : \"x\" }; },\n  getFriends: async (uid) => { order.push(\"friends\"); return [\"Grace\"]; },\n};\nconst out = await fetchProfile(db);\nif (!out.user || out.user.name !== \"Ada\") throw new Error(\"The user object should be returned.\");\nif (out.settings.theme !== \"dark\") throw new Error(\"settings should be fetched with the USER's id (7), not the literal 7 baked in.\");\nif (out.friends.join() !== \"Grace\") throw new Error(\"friends should be returned.\");\nif (order[0] !== \"user\") throw new Error(\"The user fetch must happen first (settings/friends need its id).\");",
                    "hint": "const user = await db.getUser(7); then Promise.all([db.getSettings(user.id), db.getFriends(user.id)]).",
                },
                {
                    "name": "user failure short-circuits to an error object",
                    "code": fn_wrap("fetchProfile", "fetchProfile") + "\nconst db = {\n  getUser: () => Promise.reject(new Error(\"nope\")),\n  getSettings: async () => { throw new Error(\"should not be called\"); },\n  getFriends: async () => { throw new Error(\"should not be called\"); },\n};\nconst out = await fetchProfile(db);\nif (out.error !== \"user-not-found\") throw new Error(\"A failed user fetch must return { error: 'user-not-found' }.\");",
                    "hint": "Wrap the getUser await in try/catch and return the error object; the parallel calls never run.",
                },
            ],
        },
        {
            "id": "i2-finally-cleanup",
            "title": "Cleanup With finally",
            "prompt": "Write `async function withLock(lock, job)` where `lock` has `acquire()` and `release()` (both promise-returning). Acquire, run `job()`, and ALWAYS release — whether the job succeeded or threw. RETURN the job's result; if the job threw, rethrow after releasing.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "async function withLock(lock, job) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "releases on success",
                    "code": fn_wrap("withLock", "withLock") + "\nconst events = [];\nconst lock = { acquire: async () => { events.push(\"acquire\"); }, release: async () => { events.push(\"release\"); } };\nconst out = await withLock(lock, async () => { events.push(\"job\"); return 42; });\nif (out !== 42) throw new Error(\"The job result should be returned.\");\nif (events.join() !== \"acquire,job,release\") throw new Error(\"Order must be acquire, job, release.\");",
                    "hint": "try { return await job(); } finally { await lock.release(); } — but acquire must happen before the try.",
                },
                {
                    "name": "releases on failure and rethrows",
                    "code": fn_wrap("withLock", "withLock") + "\nconst events = [];\nconst lock = { acquire: async () => { events.push(\"acquire\"); }, release: async () => { events.push(\"release\"); } };\nlet err;\ntry { await withLock(lock, async () => { throw new Error(\"job failed\"); }); } catch (e) { err = e; }\nif (!err || err.message !== \"job failed\") throw new Error(\"The job's error must propagate to the caller.\");\nif (events.join() !== \"acquire,release\") throw new Error(\"Release must still run when the job throws.\");",
                    "hint": "finally runs on both paths; the throw continues after finally completes.",
                },
            ],
        },
    ],
    {
        "i2-chain-transform": {
            "title": "Pipeline kiên cường",
            "prompt": "Viết `async function pipeline(value, steps)` trong đó `steps` là mảng các hàm đồng bộ hoặc bất đồng bộ. Await từng bước theo thứ tự, đưa kết quả của bước này vào bước kế. Nếu một bước throw, RETURN `{ ok: false, error: err.message }`; nếu không RETURN `{ ok: true, value: giá trị cuối }`.",
            "tests": [
                {"name": "chạy các bước sync và async đúng thứ tự", "hint": "for (const s of steps) value = await s(value); — await chấp nhận cả giá trị trả về đồng bộ."},
                {"name": "biến lỗi ném ra thành result object", "hint": "Bọc vòng lặp trong try/catch; khi catch thì return { ok: false, error: err.message }."},
                {"name": "steps rỗng trả về giá trị nguyên vẹn", "hint": "Vòng lặp đơn giản là không chạy."},
            ],
        },
        "i2-seq-chain": {
            "title": "Chuỗi phụ thuộc tuần tự",
            "prompt": "Viết `async function fetchProfile(db)` trong đó `db` cung cấp `getUser(id)`, `getSettings(userId)`, và `getFriends(userId)` — mỗi hàm trả về promise. Tải user với id 7 trước, rồi tải settings và friends SONG SONG bằng id của user. RETURN `{ user, settings, friends }`. Nếu tải user thất bại, RETURN `{ error: \"user-not-found\" }`.",
            "tests": [
                {"name": "user trước, rồi settings và friends song song", "hint": "const user = await db.getUser(7); rồi Promise.all([db.getSettings(user.id), db.getFriends(user.id)])."},
                {"name": "user thất bại thì dừng lại với error object", "hint": "Bọc await getUser trong try/catch và trả về error object; các lời gọi song song không chạy."},
            ],
        },
        "i2-finally-cleanup": {
            "title": "Dọn dẹp với finally",
            "prompt": "Viết `async function withLock(lock, job)` trong đó `lock` có `acquire()` và `release()` (đều trả về promise). Acquire, chạy `job()`, và LUÔN LUÔN release — dù job thành công hay throw. RETURN kết quả của job; nếu job throw, ném tiếp sau khi đã release.",
            "tests": [
                {"name": "release khi thành công", "hint": "try { return await job(); } finally { await lock.release(); } — nhưng acquire phải xảy ra trước khối try."},
                {"name": "release khi thất bại và ném tiếp", "hint": "finally chạy trên cả hai đường; lỗi sẽ tiếp tục bay sau khi finally hoàn tất."},
            ],
        },
    },
    [
        ["i2-chain-transform", "async function pipeline(value, steps) {\n  try {\n    for (const step of steps) {\n      value = await step(value);\n    }\n    return { ok: true, value };\n  } catch (err) {\n    return { ok: false, error: err.message };\n  }\n}", "async function pipeline(value, steps) {\n  for (const step of steps) {\n    value = await step(value);\n  }\n  return { ok: true, value };\n}"],
        ["i2-seq-chain", "async function fetchProfile(db) {\n  try {\n    const user = await db.getUser(7);\n    const [settings, friends] = await Promise.all([\n      db.getSettings(user.id),\n      db.getFriends(user.id),\n    ]);\n    return { user, settings, friends };\n  } catch {\n    return { error: \"user-not-found\" };\n  }\n}", "async function fetchProfile(db) {\n  const user = await db.getUser(7);\n  const settings = await db.getSettings(7);\n  const friends = await db.getFriends(7);\n  return { user, settings, friends };\n}"],
        ["i2-finally-cleanup", "async function withLock(lock, job) {\n  await lock.acquire();\n  try {\n    return await job();\n  } finally {\n    await lock.release();\n  }\n}", "async function withLock(lock, job) {\n  await lock.acquire();\n  return await job();\n}"],
    ],
)

# ── combinators-practice ────────────────────────────────────────────────────
write_practice(
    MOD,
    "combinators-practice",
    "Promise Combinators — Practice",
    "Choose strategies under failure: allSettled dashboards, a first-success mirror picker, and a timeout race.",
    "Promise Combinators — Luyện tập",
    "Chọn chiến lược khi có lỗi: dashboard allSettled, bộ chọn mirror thành công đầu tiên, và đua timeout.",
    "promise-combinators", 18, "intermediate",
    [
        {
            "id": "i2-settled-report",
            "title": "Partial-Failure Report",
            "prompt": "Write `async function gatherReport(fetchers)` where `fetchers` is an array of `{ name, run }` and `run()` returns a promise. Run all concurrently with `Promise.allSettled` and RETURN `{ ok, broken }` — `ok` maps each fulfilled fetcher's name to its value, `broken` lists the names of rejected ones.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "async function gatherReport(fetchers) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "splits fulfilled and rejected by name",
                    "code": fn_wrap("gatherReport", "gatherReport") + "\nconst out = await gatherReport([\n  { name: \"user\", run: () => Promise.resolve({ id: 1 }) },\n  { name: \"orders\", run: () => Promise.reject(new Error(\"503\")) },\n  { name: \"notifs\", run: () => Promise.resolve([\"a\"]) },\n]);\nif (out.ok.user.id !== 1 || out.ok.notifs.join() !== \"a\") throw new Error(\"Fulfilled values should be keyed by name.\");\nif (out.broken.join() !== \"orders\") throw new Error(\"Rejected fetcher names go into broken.\");",
                    "hint": "allSettled returns results in input order — zip them back with the fetchers array.",
                },
                {
                    "name": "never rejects and handles empty input",
                    "code": fn_wrap("gatherReport", "gatherReport") + "\nconst allBad = await gatherReport([{ name: \"x\", run: () => Promise.reject(new Error(\"e\")) }]);\nif (Object.keys(allBad.ok).length !== 0 || allBad.broken.join() !== \"x\") throw new Error(\"Every source failing still resolves.\");\nconst empty = await gatherReport([]);\nif (Object.keys(empty.ok).length !== 0 || empty.broken.length !== 0) throw new Error(\"Empty input yields empty ok and broken.\");",
                    "hint": "allSettled never rejects — the loop after it just finds zero fulfilled entries.",
                },
            ],
        },
        {
            "id": "i2-first-mirror",
            "title": "First Working Mirror",
            "prompt": "Write `async function fastestMirror(urls, fetchFn)` that starts ALL `fetchFn(url)` calls concurrently and resolves with the first value that FULFILLS — a rejected attempt must not win the race. If every mirror rejects, rethrow the last rejection.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "async function fastestMirror(urls, fetchFn) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "resolves with the first fulfillment, ignoring rejections",
                    "code": fn_wrap("fastestMirror", "fastestMirror") + "\nconst out = await fastestMirror([\"a\", \"b\", \"c\"], (u) =>\n  u === \"a\" ? new Promise((_, rej) => setTimeout(() => rej(new Error(\"down\")), 5))\n  : u === \"b\" ? new Promise((res) => setTimeout(() => res(\"mirror-b\"), 20))\n  : new Promise((res) => setTimeout(() => res(\"mirror-c\"), 40))\n);\nif (out !== \"mirror-b\") throw new Error(\"The first SUCCESSFUL fulfillment must win, even though mirror-a rejected first.\");",
                    "hint": "Promise.any resolves with the first fulfillment and only rejects when ALL reject.",
                },
                {
                    "name": "rethrows when every mirror fails",
                    "code": fn_wrap("fastestMirror", "fastestMirror") + "\nlet err;\ntry {\n  await fastestMirror([\"x\", \"y\"], () => Promise.reject(new Error(\"all down\")));\n} catch (e) { err = e; }\nif (!err) throw new Error(\"All mirrors failing must reject.\");",
                    "hint": "Promise.any rejects with an AggregateError when every input rejects — just let it propagate.",
                },
            ],
        },
        {
            "id": "i2-race-timeout",
            "title": "Timeout Race",
            "prompt": "Write `async function withDeadline(task, ms, onTimeout)` where `task` is a promise. If `task` fulfills within `ms`, RETURN its value. Otherwise RETURN the result of calling `onTimeout()`. The underlying task is NOT cancelled (that comes later) — you simply stop waiting.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "async function withDeadline(task, ms, onTimeout) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "fast task resolves with its value",
                    "code": fn_wrap("withDeadline", "withDeadline") + "\nconst out = await withDeadline(Promise.resolve(\"quick\"), 50, () => \"late-fallback\");\nif (out !== \"quick\") throw new Error(\"A task that finishes in time resolves with its own value.\");",
                    "hint": "Promise.race([task, timer]) — the timer promise resolves after ms.",
                },
                {
                    "name": "slow task falls back",
                    "code": fn_wrap("withDeadline", "withDeadline") + "\nlet fallbackRan = false;\nconst out = await withDeadline(new Promise((r) => setTimeout(() => r(\"late\"), 100)), 20, () => { fallbackRan = true; return \"deadline\"; });\nif (out !== \"deadline\") throw new Error(\"A task that misses the deadline resolves with onTimeout's result.\");\nif (!fallbackRan) throw new Error(\"onTimeout should actually be called.\");",
                    "hint": "The timer promise resolves with onTimeout()'s result: new Promise((res) => setTimeout(() => res(onTimeout()), ms)).",
                },
            ],
        },
    ],
    {
        "i2-settled-report": {
            "title": "Báo cáo thất bại một phần",
            "prompt": "Viết `async function gatherReport(fetchers)` trong đó `fetchers` là mảng `{ name, run }` và `run()` trả về promise. Chạy tất cả đồng thời bằng `Promise.allSettled` và RETURN `{ ok, broken }` — `ok` ánh xạ tên của từng fetcher fulfilled sang giá trị của nó, `broken` liệt kê tên của những cái bị reject.",
            "tests": [
                {"name": "tách fulfilled và rejected theo tên", "hint": "allSettled trả kết quả đúng thứ tự input — ghép ngược lại với mảng fetchers."},
                {"name": "không bao giờ reject và xử lý input rỗng", "hint": "allSettled không bao giờ reject — vòng lặp phía sau chỉ cần đếm được không có mục fulfilled nào."},
            ],
        },
        "i2-first-mirror": {
            "title": "Mirror hoạt động đầu tiên",
            "prompt": "Viết `async function fastestMirror(urls, fetchFn)` khởi động TẤT CẢ các lời gọi `fetchFn(url)` đồng thời và phân giải với giá trị đầu tiên FULFILL — một lần thử bị reject không được thắng cuộc đua. Nếu mọi mirror đều reject, ném tiếp lần reject cuối.",
            "tests": [
                {"name": "phân giải với fulfillment đầu tiên, bỏ qua rejection", "hint": "Promise.any phân giải với fulfillment đầu tiên và chỉ reject khi TẤT CẢ reject."},
                {"name": "ném tiếp khi mọi mirror đều hỏng", "hint": "Promise.any reject với AggregateError khi mọi input reject — cứ để nó lan tiếp."},
            ],
        },
        "i2-race-timeout": {
            "title": "Đua timeout",
            "prompt": "Viết `async function withDeadline(task, ms, onTimeout)` trong đó `task` là một promise. Nếu `task` fulfill trong `ms`, RETURN giá trị của nó. Nếu không, RETURN kết quả của lời gọi `onTimeout()`. Task bên dưới KHÔNG bị hủy (chuyện đó đến sau) — bạn chỉ đơn giản là ngừng chờ.",
            "tests": [
                {"name": "task nhanh phân giải bằng giá trị của nó", "hint": "Promise.race([task, timer]) — promise của timer phân giải sau ms."},
                {"name": "task chậm rơi vào fallback", "hint": "Promise của timer phân giải bằng kết quả của onTimeout(): new Promise((res) => setTimeout(() => res(onTimeout()), ms))."},
            ],
        },
    },
    [
        ["i2-settled-report", "async function gatherReport(fetchers) {\n  const results = await Promise.allSettled(fetchers.map((f) => f.run()));\n  const ok = {};\n  const broken = [];\n  results.forEach((r, i) => {\n    if (r.status === \"fulfilled\") ok[fetchers[i].name] = r.value;\n    else broken.push(fetchers[i].name);\n  });\n  return { ok, broken };\n}", "async function gatherReport(fetchers) {\n  const values = await Promise.all(fetchers.map((f) => f.run()));\n  return { ok: values, broken: [] };\n}"],
        ["i2-first-mirror", "async function fastestMirror(urls, fetchFn) {\n  return Promise.any(urls.map((u) => fetchFn(u)));\n}", "async function fastestMirror(urls, fetchFn) {\n  return Promise.race(urls.map((u) => fetchFn(u)));\n}"],
        ["i2-race-timeout", "async function withDeadline(task, ms, onTimeout) {\n  const timer = new Promise((res) => setTimeout(() => res(onTimeout()), ms));\n  return Promise.race([task, timer]);\n}", "async function withDeadline(task, ms, onTimeout) {\n  return task;\n}"],
    ],
)

print("Module 3 practices part 1 (event-loop, promises, combinators) written.")
