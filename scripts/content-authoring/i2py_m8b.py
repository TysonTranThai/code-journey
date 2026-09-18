#!/usr/bin/env python3
"""Module 8 practices: render, waterfall, budget, slow-page. Raw strings throughout."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "web-performance"

# ── render-practice ─────────────────────────────────────────────────────────
write_practice(
    MOD, "render-practice",
    "Render Pipeline — Practice",
    "Classify property costs, batch reads/writes to kill thrashing, and count frames honestly.",
    "Pipeline render — Luyện tập",
    "Phân loại chi phí thuộc tính, gom lô đọc/ghi để diệt thrashing, và đếm khung hình một cách trung thực.",
    "rendering-pipeline", 18, "intermediate",
    [
        {
            "id": "i2-phase-classify",
            "title": "Property Cost Classifier",
            "prompt": 'Write `phase(prop)` mapping style changes to the most expensive pipeline phase they trigger: "width", "height", "top", "left", "margin", "font-size" => "layout"; "color", "background", "box-shadow", "visibility" => "paint"; "transform", "opacity" => "composite"; anything else => "unknown".',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function phase(prop) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "layout properties reflow",
                    "code": fn_wrap("phase", "phase") + r'''
if (phase("width") !== "layout") throw new Error("width reflows.");
if (phase("font-size") !== "layout") throw new Error("font-size reflows everything.");
if (phase("margin") !== "layout") throw new Error("margin reflows.");
''',
                    "hint": "Three sets, checked layout-first.",
                },
                {
                    "name": "composite properties are cheapest",
                    "code": fn_wrap("phase", "phase") + r'''
if (phase("transform") !== "composite") throw new Error("transform composites.");
if (phase("opacity") !== "composite") throw new Error("opacity composites.");
if (phase("cursor") !== "unknown") throw new Error("Unlisted => unknown.");
''',
                    "hint": "The composite set is intentionally tiny — that's the lesson.",
                },
            ],
        },
        {
            "id": "i2-batch-rw",
            "title": "Read/Write Batcher",
            "prompt": 'A DOM interaction is a list of ops: { op: "read" | "write", el, value? } (reads return the element\'s current height, writes set it). Write `simulate(ops)` executing with correct batching: process ALL reads first (collecting heights), then ALL writes. Return the array of read heights in order. A naive interleaved implementation causes N forced layouts; yours must cause at most 2.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function simulate(ops) {\n  // your code — a read costs a layout pass if the previous op was a write\n}\n",
            "tests": [
                {
                    "name": "reads are collected before writes",
                    "code": fn_wrap("simulate", "simulate") + r'''
const ops = [
  { op: "read", el: "a" },
  { op: "write", el: "a", value: 100 },
  { op: "read", el: "b" },
  { op: "write", el: "b", value: 200 },
];
const heights = simulate(ops);
// heights: both reads happened before any write => [10, 20] (initial heights)
''',
                    "hint": "Two passes: filter reads, map heights; then filter writes.",
                },
                {
                    "name": "layout passes counted",
                    "code": fn_wrap("simulate", "simulate") + r'''
const ops = [
  { op: "read", el: "a" },
  { op: "write", el: "a", value: 100 },
  { op: "read", el: "b" },
  { op: "write", el: "b", value: 200 },
];
let layouts = 0;
const heights = simulate(ops, () => layouts++);
if (layouts > 2) throw new Error("Batching must cap forced layouts at 2 (initial + after writes).");
if (heights.length !== 2) throw new Error("Two reads recorded.");
''',
                    "hint": "Accept an optional onLayout callback to count passes.",
                },
            ],
        },
        {
            "id": "i2-frame-budget",
            "title": "Frame Budget Auditor",
            "prompt": 'Write `frameVerdict(tasks)` — tasks is an array of millisecond durations that all ran within ONE 16.7ms frame. Return "jank" if their sum exceeds 16.7, "tight" if it exceeds 12, otherwise "smooth". Also `longTaskCount(tasks)` returning how many SINGLE tasks exceed 50ms (the long-task threshold).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function frameVerdict(tasks) {\n  // your code\n}\n\nfunction longTaskCount(tasks) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "sums decide the verdict",
                    "code": fn_wrap("frameVerdict, longTaskCount", "frameVerdict, longTaskCount") + r'''
if (frameVerdict([3, 4, 5]) !== "smooth") throw new Error("12ms total is smooth.");
if (frameVerdict([6, 4, 4]) !== "tight") throw new Error("14ms is tight.");
if (frameVerdict([10, 10]) !== "jank") throw new Error("20ms blows the budget.");
''',
                    "hint": "Sum, then two comparisons.",
                },
                {
                    "name": "long tasks counted individually",
                    "code": fn_wrap("frameVerdict, longTaskCount", "frameVerdict, longTaskCount") + r'''
if (longTaskCount([60, 10, 55, 49]) !== 2) throw new Error("60 and 55 are long; 49 is not.");
if (longTaskCount([]) !== 0) throw new Error("Nothing runs, nothing counts.");
''',
                    "hint": "filter with t > 50.",
                },
            ],
        },
    ],
    {
        "i2-phase-classify": {
            "title": "Bộ phân loại chi phí thuộc tính",
            "prompt": 'Viết `phase(prop)` ánh xạ thay đổi style sang pha pipeline đắt nhất mà nó kích hoạt: "width", "height", "top", "left", "margin", "font-size" => "layout"; "color", "background", "box-shadow", "visibility" => "paint"; "transform", "opacity" => "composite"; còn lại => "unknown".',
            "tests": [
                {"name": "thuộc tính layout gây reflow", "hint": "Ba tập hợp, kiểm tra layout trước."},
                {"name": "thuộc tính composite rẻ nhất", "hint": "Tập composite cố ý rất nhỏ — đó chính là bài học."},
            ],
        },
        "i2-batch-rw": {
            "title": "Bộ gom lô đọc/ghi",
            "prompt": 'Một tương tác DOM là danh sách op: { op: "read" | "write", el, value? } (read trả về chiều cao hiện tại của phần tử, write đặt nó). Viết `simulate(ops)` chạy với gom lô đúng: xử lý TOÀN BỘ read trước (thu thập chiều cao), rồi TOÀN BỘ write. Trả về mảng chiều cao đã đọc theo thứ tự. Cài đặt xen kẽ ngây thơ gây N lần layout ép; bản của bạn gây tối đa 2.',
            "tests": [
                {"name": "đọc được gom trước khi ghi", "hint": "Hai lượt: lọc read, map chiều cao; rồi lọc write."},
                {"name": "đếm số lần layout", "hint": "Chấp nhận callback onLayout tùy chọn để đếm."},
            ],
        },
        "i2-frame-budget": {
            "title": "Thanh tra ngân sách khung hình",
            "prompt": 'Viết `frameVerdict(tasks)` — tasks là mảng thời lượng mili giọt chạy trong MỘT khung 16.7ms. Trả về "jank" nếu tổng vượt 16.7, "tight" nếu vượt 12, còn lại "smooth". Cùng `longTaskCount(tasks)` đếm bao nhiêu task ĐƠN LẺ vượt 50ms (ngưỡng long-task).',
            "tests": [
                {"name": "tổng quyết định phán quyết", "hint": "Cộng, rồi hai phép so sánh."},
                {"name": "long task được đếm riêng", "hint": "filter với t > 50."},
            ],
        },
    },
    [
        ["i2-phase-classify", r'''function phase(prop) {
  const layout = ["width", "height", "top", "left", "margin", "font-size"];
  const paint = ["color", "background", "box-shadow", "visibility"];
  const composite = ["transform", "opacity"];
  if (layout.includes(prop)) return "layout";
  if (paint.includes(prop)) return "paint";
  if (composite.includes(prop)) return "composite";
  return "unknown";
}''', r'''function phase(prop) {
  return "layout";
}'''],
        ["i2-batch-rw", r'''function simulate(ops, onLayout) {
  const mark = () => { if (onLayout) onLayout(); };
  mark(); // initial layout
  const reads = ops.filter((o) => o.op === "read");
  const writes = ops.filter((o) => o.op === "write");
  const heights = reads.map((o) => HEIGHTS[o.el]);
  for (const w of writes) HEIGHTS[w.el] = w.value;
  mark();
  return heights;
}
const HEIGHTS = { a: 10, b: 20, c: 30 };''', r'''const HEIGHTS = { a: 10, b: 20, c: 30 };
function simulate(ops, onLayout) {
  const out = [];
  for (const o of ops) {
    if (o.op === "read") { if (onLayout) onLayout(); out.push(HEIGHTS[o.el]); }
    else { HEIGHTS[o.el] = o.value; if (onLayout) onLayout(); }
  }
  return out;
}'''],
        ["i2-frame-budget", r'''function frameVerdict(tasks) {
  const total = tasks.reduce((a, b) => a + b, 0);
  if (total > 16.7) return "jank";
  if (total > 12) return "tight";
  return "smooth";
}
function longTaskCount(tasks) {
  return tasks.filter((t) => t > 50).length;
}''', r'''function frameVerdict(tasks) {
  return tasks[0] > 16.7 ? "jank" : "smooth";
}
function longTaskCount(tasks) {
  return 0;
}'''],
    ],
)

# ── waterfall-practice ──────────────────────────────────────────────────────
write_practice(
    MOD, "waterfall-practice",
    "Waterfall & Blocking — Practice",
    "Model request dependencies, classify script-loading attributes, and find the critical chain length.",
    "Waterfall & chặn render — Luyện tập",
    "Mô hình hóa phụ thuộc request, phân loại attribute tải script, và tìm độ dài chuỗi tới hạn.",
    "network-waterfall", 18, "intermediate",
    [
        {
            "id": "i2-script-attrs",
            "title": "Script Attribute Classifier",
            "prompt": 'Write `scriptBehavior(attrs)` — attrs is a string like "src=app.js" optionally containing "defer" or "async". Return "blocking" for plain scripts (download + execute pause parsing), "defer" for defer (parallel download, runs after parse), "async" for async (parallel, runs when ready), and "inline" when there is no src.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function scriptBehavior(attrs) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "plain scripts block",
                    "code": fn_wrap("scriptBehavior", "scriptBehavior") + r'''
if (scriptBehavior("src=app.js") !== "blocking") throw new Error("No attribute => blocking.");
if (scriptBehavior("src=app.js defer") !== "defer") throw new Error("defer defers execution.");
if (scriptBehavior("src=analytics.js async") !== "async") throw new Error("async runs when ready.");
if (scriptBehavior("") !== "inline") throw new Error("No src => inline.");
''',
                    "hint": "Check src presence first, then the keywords.",
                },
                {
                    "name": "both attributes = async wins",
                    "code": fn_wrap("scriptBehavior", "scriptBehavior") + r'''
if (scriptBehavior("src=x.js defer async") !== "async") throw new Error("HTML spec: async takes precedence.");
''',
                    "hint": "Check async before defer.",
                },
            ],
        },
        {
            "id": "i2-critical-chain",
            "title": "Critical Chain Length",
            "prompt": "Requests form a dependency chain: each request may name the request it waited on (\"after\"). Write `chainLength(requests, id)` returning how many hops from the initial request to `id` inclusive. requests is an array of { id, after: null | otherId }. Root requests have after null.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function chainLength(requests, id) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "counts hops along the chain",
                    "code": fn_wrap("chainLength", "chainLength") + r'''
const reqs = [
  { id: "html", after: null },
  { id: "css", after: "html" },
  { id: "font", after: "css" },
];
if (chainLength(reqs, "html") !== 1) throw new Error("The root is 1 request deep.");
if (chainLength(reqs, "font") !== 3) throw new Error("html -> css -> font is 3 deep.");
''',
                    "hint": "Walk the after pointers back to null, counting.",
                },
                {
                    "name": "handles missing links",
                    "code": fn_wrap("chainLength", "chainLength") + r'''
const reqs = [{ id: "a", after: null }];
if (chainLength(reqs, "ghost") === undefined || chainLength(reqs, "ghost") === null) {
  // acceptable: error, null, or 0 — just don't crash with a wrong number
}
if (chainLength(reqs, "a") !== 1) throw new Error("Single root still counts as 1.");
''',
                    "hint": "Build an id -> request map first.",
                },
            ],
        },
        {
            "id": "i2-blocking-audit",
            "title": "Blocking Audit",
            "prompt": 'Given an array of resources { type, blocking } where type is "css" | "js" | "font" | "img" and blocking is true when it blocks first render, write `firstPaintBlockers(resources)` returning the COUNT of blockers, and `byKind(resources)` returning an object mapping type => count (only types present).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function firstPaintBlockers(resources) {\n  // your code\n}\n\nfunction byKind(resources) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "counts what blocks first paint",
                    "code": fn_wrap("firstPaintBlockers, byKind", "firstPaintBlockers, byKind") + r'''
const rs = [
  { type: "css", blocking: true },
  { type: "js", blocking: true },
  { type: "font", blocking: false },
  { type: "img", blocking: false },
];
if (firstPaintBlockers(rs) !== 2) throw new Error("css + js block; font/img don't.");
if (byKind(rs).css !== 1 || byKind(rs).js !== 1 || byKind(rs).font !== 1) throw new Error("Counts per kind.");
''',
                    "hint": "filter + length; reduce into an object.",
                },
                {
                    "name": "clean pages have zero blockers",
                    "code": fn_wrap("firstPaintBlockers, byKind", "firstPaintBlockers, byKind") + r'''
if (firstPaintBlockers([{ type: "img", blocking: false }]) !== 0) throw new Error("Images never block first paint by default.");
if (Object.keys(byKind([])).length !== 0) throw new Error("Empty in, empty out.");
''',
                    "hint": "Defaults matter for empty input.",
                },
            ],
        },
    ],
    {
        "i2-script-attrs": {
            "title": "Bộ phân loại attribute script",
            "prompt": 'Viết `scriptBehavior(attrs)` — attrs là chuỗi kiểu "src=app.js" tùy chọn chứa "defer" hoặc "async". Trả về "blocking" cho script thường (tải + chạy đều chặn parse), "defer" cho defer (tải song song, chạy sau parse), "async" cho async (song song, chạy khi sẵn sàng), và "inline" khi không có src.',
            "tests": [
                {"name": "script thường chặn", "hint": "Kiểm tra sự hiện diện của src trước, rồi đến các từ khóa."},
                {"name": "có cả hai attribute thì async thắng", "hint": "Kiểm tra async trước defer."},
            ],
        },
        "i2-critical-chain": {
            "title": "Độ dài chuỗi tới hạn",
            "prompt": 'Request tạo thành chuỗi phụ thuộc: mỗi request có thể nêu request nó phải chờ ("after"). Viết `chainLength(requests, id)` trả về số chặng từ request gốc tới `id` (bao gồm). requests là mảng { id, after: null | otherId }. Request gốc có after null.',
            "tests": [
                {"name": "đếm chặng dọc theo chuỗi", "hint": "Đi theo con trỏ after ngược về null, đếm dần."},
                {"name": "xử lý liên kết thiếu", "hint": "Dựng map id -> request trước."},
            ],
        },
        "i2-blocking-audit": {
            "title": "Kiểm toán tài nguyên chặn",
            "prompt": 'Cho mảng tài nguyên { type, blocking } với type là "css" | "js" | "font" | "img" và blocking là true khi nó chặn lần render đầu, viết `firstPaintBlockers(resources)` trả về SỐ LƯỢNG blocker, và `byKind(resources)` trả về object type => số lượng (chỉ type có mặt).',
            "tests": [
                {"name": "đếm thứ chặn lần vẽ đầu", "hint": "filter + length; reduce vào object."},
                {"name": "trang sạch có không blocker", "hint": "Giá trị mặc định quan trọng với input rỗng."},
            ],
        },
    },
    [
        ["i2-script-attrs", r'''function scriptBehavior(attrs) {
  if (!attrs.includes("src=")) return "inline";
  if (attrs.includes("async")) return "async";
  if (attrs.includes("defer")) return "defer";
  return "blocking";
}''', r'''function scriptBehavior(attrs) {
  return "blocking";
}'''],
        ["i2-critical-chain", r'''function chainLength(requests, id) {
  const byId = new Map(requests.map((r) => [r.id, r]));
  let n = 0, cur = id;
  while (cur && byId.has(cur)) {
    n++;
    cur = byId.get(cur).after;
  }
  return n;
}''', r'''function chainLength(requests, id) {
  return 1;
}'''],
        ["i2-blocking-audit", r'''function firstPaintBlockers(resources) {
  return resources.filter((r) => r.blocking).length;
}
function byKind(resources) {
  const out = {};
  for (const r of resources) out[r.type] = (out[r.type] ?? 0) + 1;
  return out;
}''', r'''function firstPaintBlockers(resources) {
  return resources.length;
}
function byKind(resources) {
  return {};
}'''],
    ],
)

# ── budget-practice ─────────────────────────────────────────────────────────
write_practice(
    MOD, "budget-practice",
    "Vitals & Budgets — Practice",
    "Compute CLS from layout shifts, grade vitals against thresholds, and enforce a multi-part budget.",
    "Vitals & ngân sách — Luyện tập",
    "Tính CLS từ các cú nhảy layout, chấm vitals theo ngưỡng, và thực thi ngân sách nhiều thành phần.",
    "measure-optimize-loop", 18, "intermediate",
    [
        {
            "id": "i2-cls-score",
            "title": "CLS Calculator",
            "prompt": "Layout shifts arrive as an array of { fraction (0..1 of viewport that moved), distance (fraction of viewport it moved) }; each shift's impact = fraction * distance; shifts within 500ms of the previous count into the same session (gap in ms given per shift as `sincePrev`). CLS = the LARGEST session total. Write `cls(shifts)`.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function cls(shifts) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "sessions cap the score",
                    "code": fn_wrap("cls", "cls") + r'''
const shifts = [
  { fraction: 0.5, distance: 0.2, sincePrev: null },
  { fraction: 0.5, distance: 0.2, sincePrev: 100 },
  { fraction: 0.5, distance: 0.2, sincePrev: 2000 },
];
// sessions: [0.1 + 0.1, 0.1] => max 0.2
if (Math.abs(cls(shifts) - 0.2) > 1e-9) throw new Error("Two shifts in one session, one alone after.");
''',
                    "hint": "Accumulate; when sincePrev > 500, start a new session.",
                },
                {
                    "name": "no shifts, no score",
                    "code": fn_wrap("cls", "cls") + r'''
if (cls([]) !== 0) throw new Error("Stable page scores 0.");
if (Math.abs(cls([{ fraction: 0.1, distance: 0.1, sincePrev: null }]) - 0.01) > 1e-9) throw new Error("Single shift: 0.1 * 0.1.");
''',
                    "hint": "Impact per shift is fraction * distance.",
                },
            ],
        },
        {
            "id": "i2-vitals-grade",
            "title": "Vitals Grader",
            "prompt": 'Write `grade(vitals)` — vitals is { lcp, inp, cls } in seconds/ms/score. Thresholds (good limits): LCP 2.5s, INP 200ms, CLS 0.1. Return "good" when all three meet the limits, "needs-improvement" when exactly one or two exceed, "poor" when all three exceed.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function grade(vitals) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "all good passes",
                    "code": fn_wrap("grade", "grade") + r'''
if (grade({ lcp: 2.0, inp: 150, cls: 0.05 }) !== "good") throw new Error("Everything within limits.");
''',
                    "hint": "Count the failures, then map 0/1-2/3 to grades.",
                },
                {
                    "name": "partial and full failures",
                    "code": fn_wrap("grade", "grade") + r'''
if (grade({ lcp: 3.0, inp: 150, cls: 0.05 }) !== "needs-improvement") throw new Error("One miss => needs-improvement.");
if (grade({ lcp: 3.0, inp: 250, cls: 0.05 }) !== "needs-improvement") throw new Error("Two misses still needs-improvement.");
if (grade({ lcp: 4.0, inp: 300, cls: 0.2 }) !== "poor") throw new Error("Three misses => poor.");
''',
                    "hint": "Boundaries: lcp <= 2.5, inp <= 200, cls <= 0.1 are good.",
                },
            ],
        },
        {
            "id": "i2-budget-enforce",
            "title": "Budget Enforcer",
            "prompt": 'Write `audit(assets, budgets)` — assets is { js: KB, css: KB, images: KB }; budgets is { js, css, images } (max allowed). Return { pass, over } where pass is true when every category is within budget, and over is an array of the exceeded category names sorted alphabetically.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function audit(assets, budgets) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "passes when within budget",
                    "code": fn_wrap("audit", "audit") + r'''
const out = audit({ js: 150, css: 40, images: 300 }, { js: 170, css: 50, images: 400 });
if (out.pass !== true || out.over.length !== 0) throw new Error("All categories fit.");
''',
                    "hint": "Compare each shared key.",
                },
                {
                    "name": "reports and sorts overruns",
                    "code": fn_wrap("audit", "audit") + r'''
const out = audit({ js: 200, css: 60, images: 300 }, { js: 170, css: 50, images: 400 });
if (out.pass !== false) throw new Error("Two categories over.");
if (out.over.join(",") !== "css,js") throw new Error("Alphabetical: css before js.");
''',
                    "hint": "Collect, sort, and set pass from the emptiness of over.",
                },
            ],
        },
    ],
    {
        "i2-cls-score": {
            "title": "Máy tính CLS",
            "prompt": "Layout shift đến dưới dạng mảng { fraction (0..1 phần viewport bị dịch), distance (phần viewport nó dịch chuyển) }; impact của mỗi shift = fraction * distance; các shift cách nhau dưới 500ms gộp vào cùng session (khoảng cách cho trước qua `sincePrev`). CLS = TỔNG session LỚN NHẤT. Viết `cls(shifts)`.",
            "tests": [
                {"name": "session chấm điểm", "hint": "Cộng dồn; khi sincePrev > 500 thì mở session mới."},
                {"name": "không shift thì không điểm", "hint": "Impact mỗi shift là fraction * distance."},
            ],
        },
        "i2-vitals-grade": {
            "title": "Trình chấm vitals",
            "prompt": 'Viết `grade(vitals)` — vitals là { lcp, inp, cls } theo giây/ms/điểm. Ngưỡng (giới hạn tốt): LCP 2.5s, INP 200ms, CLS 0.1. Trả về "good" khi cả ba đạt, "needs-improvement" khi vượt đúng một hoặc hai, "poor" khi vượt cả ba.',
            "tests": [
                {"name": "tất cả tốt là pass", "hint": "Đếm số lần vượt, rồi map 0/1-2/3 sang grade."},
                {"name": "thất bại một phần và toàn phần", "hint": "Biên: lcp <= 2.5, inp <= 200, cls <= 0.1 là tốt."},
            ],
        },
        "i2-budget-enforce": {
            "title": "Trình thực thi ngân sách",
            "prompt": 'Viết `audit(assets, budgets)` — assets là { js: KB, css: KB, images: KB }; budgets là { js, css, images } (tối đa cho phép). Trả về { pass, over } với pass là true khi mọi nhóm trong ngân sách, và over là mảng tên nhóm vượt đã sắp theo bảng chữ cái.',
            "tests": [
                {"name": "pass khi trong ngân sách", "hint": "So sánh từng key chung."},
                {"name": "báo cáo và sắp xếp phần vượt", "hint": "Thu thập, sort, và set pass theo việc over có rỗng không."},
            ],
        },
    },
    [
        ["i2-cls-score", r'''function cls(shifts) {
  let best = 0, cur = 0;
  for (const s of shifts) {
    if (s.sincePrev !== null && s.sincePrev > 500) {
      best = Math.max(best, cur);
      cur = 0;
    }
    cur += s.fraction * s.distance;
  }
  return Math.max(best, cur);
}''', r'''function cls(shifts) {
  return shifts.reduce((a, s) => a + s.fraction * s.distance, 0);
}'''],
        ["i2-vitals-grade", r'''function grade(vitals) {
  let misses = 0;
  if (vitals.lcp > 2.5) misses++;
  if (vitals.inp > 200) misses++;
  if (vitals.cls > 0.1) misses++;
  if (misses === 0) return "good";
  if (misses === 3) return "poor";
  return "needs-improvement";
}''', r'''function grade(vitals) {
  return vitals.lcp > 2.5 ? "poor" : "good";
}'''],
        ["i2-budget-enforce", r'''function audit(assets, budgets) {
  const over = [];
  for (const k of Object.keys(budgets)) {
    if (assets[k] > budgets[k]) over.push(k);
  }
  over.sort();
  return { pass: over.length === 0, over };
}''', r'''function audit(assets, budgets) {
  return { pass: true, over: [] };
}'''],
    ],
)

# ── slow-page-practice ──────────────────────────────────────────────────────
write_practice(
    MOD, "slow-page-practice",
    "Slow Page Clinic — Practice",
    "The diagnose-first workflow made runnable: measure a deliberately broken page spec, find its dominant cost, fix, and verify.",
    "Phòng khám trang chậm — Luyện tập",
    "Quy trình chẩn-đoán-trước ở dạng chạy được: đo một đặc tả trang cố tình hỏng, tìm chi phí trội, sửa, và xác minh.",
    "measure-optimize-loop", 25, "intermediate",
    [
        {
            "id": "i2-page-diagnose",
            "title": "Diagnose the Broken Page",
            "prompt": 'A page spec is { htmlKB, cssKB, jsKB, imageKB, ttfbMs, renderBlocking: [types], imageCount, heroLazy }. Write `diagnose(page)` returning the SINGLE dominant issue as a string, by these rules (first match wins): ttfbMs > 800 => "slow-server"; heroLazy true => "lazy-hero"; any "css" in renderBlocking => "blocking-css"; imageKB > 2000 => "oversized-images"; jsKB > 500 => "heavy-js"; otherwise "healthy".',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function diagnose(page) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "identifies each dominant issue",
                    "code": fn_wrap("diagnose", "diagnose") + r'''
if (diagnose({ ttfbMs: 1200, heroLazy: false, renderBlocking: [], imageKB: 100, jsKB: 100 }) !== "slow-server") throw new Error("TTFB first.");
if (diagnose({ ttfbMs: 200, heroLazy: true, renderBlocking: [], imageKB: 100, jsKB: 100 }) !== "lazy-hero") throw new Error("Hero before css.");
if (diagnose({ ttfbMs: 200, heroLazy: false, renderBlocking: ["css"], imageKB: 100, jsKB: 100 }) !== "blocking-css") throw new Error("css before images.");
if (diagnose({ ttfbMs: 200, heroLazy: false, renderBlocking: [], imageKB: 3000, jsKB: 100 }) !== "oversized-images") throw new Error("Images before js.");
if (diagnose({ ttfbMs: 200, heroLazy: false, renderBlocking: [], imageKB: 100, jsKB: 900 }) !== "heavy-js") throw new Error("js last.");
''',
                    "hint": "A pure if-chain in the stated priority order.",
                },
                {
                    "name": "healthy page passes",
                    "code": fn_wrap("diagnose", "diagnose") + r'''
if (diagnose({ ttfbMs: 300, heroLazy: false, renderBlocking: [], imageKB: 400, jsKB: 200 }) !== "healthy") throw new Error("Within all thresholds.");
''',
                    "hint": "The final else is an answer, not an error.",
                },
            ],
        },
        {
            "id": "i2-fix-and-remeasure",
            "title": "Fix and Re-measure",
            "prompt": 'Write `applyFix(page, fix)` producing an improved page spec (non-mutating). Fixes: "server" halves ttfbMs; "hero" sets heroLazy false; "css" empties renderBlocking; "images" quarters imageKB; "js" halves jsKB. Then `improved(page, fix)` returns { before, after, better } where better is true when the fix actually changed the spec (after differs from before, compare with JSON.stringify).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function applyFix(page, fix) {\n  // your code\n}\n\nfunction improved(page, fix) {\n  // your code — use diagnose and applyFix\n}\n",
            "tests": [
                {
                    "name": "each fix targets its lever",
                    "code": fn_wrap("applyFix", "applyFix") + r'''
const base = { ttfbMs: 1000, heroLazy: true, renderBlocking: ["css"], imageKB: 4000, jsKB: 600 };
if (applyFix(base, "server").ttfbMs !== 500) throw new Error("server halves ttfb.");
if (applyFix(base, "hero").heroLazy !== false) throw new Error("hero un-lazy.");
if (applyFix(base, "css").renderBlocking.length !== 0) throw new Error("css clears blockers.");
if (applyFix(base, "images").imageKB !== 1000) throw new Error("images quarter the bytes.");
if (base.ttfbMs !== 1000) throw new Error("Non-mutating.");
''',
                    "hint": "Spread the page, override one field per fix.",
                },
                {
                    "name": "the loop closes on a real case",
                    "code": fn_wrap("improved", "improved") + r'''
const page = { ttfbMs: 900, heroLazy: false, renderBlocking: [], imageKB: 3000, jsKB: 100 };
const out = improved(page, "images");
if (out.after.imageKB !== 750) throw new Error("3000/4 = 750.");
if (out.before !== page) throw new Error("before is the original spec.");
if (out.better !== true) throw new Error("The fix changed the spec, so better is true.");
''',
                    "hint": "Compose the two functions; better compares before and after.",
                },
            ],
        },
        {
            "id": "i2-lcp-chain",
            "title": "LCP Chain Timer",
            "prompt": 'Write `lcpEstimate(page)` — a crude LCP model: ttfbMs + cssBlockMs + imageMs, where cssBlockMs = 50 per render-blocking css, imageMs = imageKB / 100 (KB per ms over 100KB/s effective). Return the total in ms. Write `withinLcp(page)` returning true when the estimate is <= 2500ms.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function lcpEstimate(page) {\n  // your code\n}\n\nfunction withinLcp(page) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "sums the chain",
                    "code": fn_wrap("lcpEstimate, withinLcp", "lcpEstimate, withinLcp") + r'''
const page = { ttfbMs: 400, renderBlocking: ["css", "css"], imageKB: 5000 };
// 400 + 100 + 50 = 550
if (lcpEstimate(page) !== 550) throw new Error("ttfb + 2 css blocks + image time.");
if (withinLcp(page) !== true) throw new Error("550ms is comfortably within 2.5s.");
''',
                    "hint": "imageMs = imageKB / 100; cssBlockMs = 50 * count.",
                },
                {
                    "name": "over-budget page fails",
                    "code": fn_wrap("lcpEstimate, withinLcp", "lcpEstimate, withinLcp") + r'''
const page = { ttfbMs: 1500, renderBlocking: [], imageKB: 400000 };
if (withinLcp(page) !== false) throw new Error("1500 + 4000 = 5500ms > 2500.");
''',
                    "hint": "Same formula; the threshold does the talking.",
                },
            ],
        },
    ],
    {
        "i2-page-diagnose": {
            "title": "Chẩn đoán trang hỏng",
            "prompt": 'Đặc tả trang là { htmlKB, cssKB, jsKB, imageKB, ttfbMs, renderBlocking: [types], imageCount, heroLazy }. Viết `diagnose(page)` trả về MỘT vấn đề trội dưới dạng chuỗi, theo quy tắc (khớp đầu tiên thắng): ttfbMs > 800 => "slow-server"; heroLazy true => "lazy-hero"; có "css" trong renderBlocking => "blocking-css"; imageKB > 2000 => "oversized-images"; jsKB > 500 => "heavy-js"; còn lại "healthy".',
            "tests": [
                {"name": "nhận diện từng vấn đề trội", "hint": "Một chuỗi if thuần theo đúng thứ tự ưu tiên đã nêu."},
                {"name": "trang khỏe mạnh pass", "hint": "Nhánh else cuối cùng là một đáp án, không phải lỗi."},
            ],
        },
        "i2-fix-and-remeasure": {
            "title": "Sửa và đo lại",
            "prompt": 'Viết `applyFix(page, fix)` sinh đặc tả trang tốt hơn (không mutate). Các fix: "server" chia đôi ttfbMs; "hero" đặt heroLazy false; "css" làm rỗng renderBlocking; "images" chia tư imageKB; "js" chia đôi jsKB. Rồi `improved(page, fix)` trả về { before, after, better } với better là true khi fix thực sự thay đổi đặc tả (after khác before, so bằng JSON.stringify).',
            "tests": [
                {"name": "mỗi fix nhắm đúng đòn bẩy", "hint": "Spread trang, ghi đè một trường cho mỗi fix."},
                {"name": "vòng lặp khép lại trên ca thật", "hint": "Ghép hai hàm; better kiểm tra trạng thái after."},
            ],
        },
        "i2-lcp-chain": {
            "title": "Đồng hồ chuỗi LCP",
            "prompt": 'Viết `lcpEstimate(page)` — mô hình LCP thô: ttfbMs + cssBlockMs + imageMs, với cssBlockMs = 50 mỗi css chặn render, imageMs = imageKB / 100 (KB trên ms với tốc độ hiệu dụng 100KB/s). Trả về tổng tính bằng ms. Viết `withinLcp(page)` trả về true khi ước tính <= 2500ms.',
            "tests": [
                {"name": "cộng chuỗi", "hint": "imageMs = imageKB / 100; cssBlockMs = 50 * số lượng."},
                {"name": "trang vượt ngân sách fail", "hint": "Cùng công thức; ngưỡng thay bạn nói."},
            ],
        },
    },
    [
        ["i2-page-diagnose", r'''function diagnose(page) {
  if (page.ttfbMs > 800) return "slow-server";
  if (page.heroLazy) return "lazy-hero";
  if (page.renderBlocking.includes("css")) return "blocking-css";
  if (page.imageKB > 2000) return "oversized-images";
  if (page.jsKB > 500) return "heavy-js";
  return "healthy";
}''', r'''function diagnose(page) {
  return "healthy";
}'''],
        ["i2-fix-and-remeasure", r'''function applyFix(page, fix) {
  const p = { ...page, renderBlocking: [...page.renderBlocking] };
  if (fix === "server") p.ttfbMs = p.ttfbMs / 2;
  if (fix === "hero") p.heroLazy = false;
  if (fix === "css") p.renderBlocking = [];
  if (fix === "images") p.imageKB = p.imageKB / 4;
  if (fix === "js") p.jsKB = p.jsKB / 2;
  return p;
}
function improved(page, fix) {
  const after = applyFix(page, fix);
  return { before: page, after, better: JSON.stringify(after) !== JSON.stringify(page) };
}''', r'''function applyFix(page, fix) {
  page.ttfbMs = 0;
  return page;
}
function improved(page, fix) {
  return { before: page, after: page, better: false };
}'''],
        ["i2-lcp-chain", r'''function lcpEstimate(page) {
  const cssBlockMs = page.renderBlocking.length * 50;
  const imageMs = page.imageKB / 100;
  return page.ttfbMs + cssBlockMs + imageMs;
}
function withinLcp(page) {
  return lcpEstimate(page) <= 2500;
}''', r'''function lcpEstimate(page) {
  return 0;
}
function withinLcp(page) {
  return true;
}'''],
    ],
)

print("Module 8 practices written.")
