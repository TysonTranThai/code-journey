#!/usr/bin/env python3
"""Module 7 practices: assertions, design, doubles, diagnose, regression.

Test snippets use raw triple-quoted strings — no escaping gymnastics.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_practice, fn_wrap

MOD = "testing-debugging"

# ── assertions-practice ─────────────────────────────────────────────────────
write_practice(
    MOD, "assertions-practice",
    "Build Your Own Assertions — Practice",
    "Construct the machinery beneath every framework: deep equality, typed throw-assertions, and diff-friendly messages.",
    "Tự xây assertion — Luyện tập",
    "Dựng cơ chế bên dưới mọi framework: deep equality, assertion kiểu lỗi khi throw, và message thân thiện với diff.",
    "unit-testing-foundations", 18, "intermediate",
    [
        {
            "id": "i2-deep-equal",
            "title": "Deep Equality",
            "prompt": 'Write `deepEqual(a, b)`: primitives compare with Object.is; arrays compare element-wise (same order); objects compare by having exactly the same keys with deeply equal values; null compares only to null. Arrays are not equal to objects.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function deepEqual(a, b) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "primitives and null",
                    "code": fn_wrap("deepEqual", "deepEqual") + r'''
if (!deepEqual(1, 1) || !deepEqual("x", "x")) throw new Error("Primitives compare by value.");
if (!deepEqual(NaN, NaN)) throw new Error("Object.is treats NaN as NaN.");
if (deepEqual(null, {}) || deepEqual(null, 0)) throw new Error("null equals only null.");
''',
                    "hint": "Object.is first; if both are non-null objects, recurse.",
                },
                {
                    "name": "structures compare structurally",
                    "code": fn_wrap("deepEqual", "deepEqual") + r'''
if (!deepEqual([1, [2, 3]], [1, [2, 3]])) throw new Error("Nested arrays match by value.");
if (deepEqual([1, 2], [2, 1])) throw new Error("Order matters.");
if (!deepEqual({ a: 1, b: { c: 2 } }, { b: { c: 2 }, a: 1 })) throw new Error("Key order is irrelevant.");
if (deepEqual({ a: 1 }, { a: 1, b: 2 })) throw new Error("Different key sets differ.");
if (deepEqual([], {})) throw new Error("An array is not an object here.");
''',
                    "hint": "Array.isArray check before the object branch; compare Object.keys lengths, then each key recursively.",
                },
            ],
        },
        {
            "id": "i2-assert-throws",
            "title": "assertThrows",
            "prompt": 'Write `assertThrows(fn, errClass, msgPart)` — call fn(); if it does NOT throw, fail (return "no-throw"). If it throws the wrong error class, return "wrong-type". If errClass is given and msgPart is given, the error message must contain msgPart, else return "wrong-message". On full success return "ok".',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function assertThrows(fn, errClass, msgPart) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "catches absence of throw",
                    "code": fn_wrap("assertThrows", "assertThrows") + r'''
if (assertThrows(() => 42) !== "no-throw") throw new Error("A function that returns is not a thrower.");
''',
                    "hint": "Wrap the call in try/catch; reaching the end of try means no throw.",
                },
                {
                    "name": "verifies type and message",
                    "code": fn_wrap("assertThrows", "assertThrows") + r'''
if (assertThrows(() => { throw new TypeError("bad qty"); }, TypeError) !== "ok") throw new Error("Matching type => ok.");
if (assertThrows(() => { throw new TypeError("bad qty"); }, RangeError) !== "wrong-type") throw new Error("Wrong class detected.");
if (assertThrows(() => { throw new Error("bad qty: -1"); }, Error, "bad qty") !== "ok") throw new Error("Message substring matches.");
if (assertThrows(() => { throw new Error("something else"); }, Error, "bad qty") !== "wrong-message") throw new Error("Message mismatch detected.");
''',
                    "hint": "instanceof for the class; .includes for the message part.",
                },
            ],
        },
        {
            "id": "i2-diff-msg",
            "title": "Failure Messages That Help",
            "prompt": 'Write `fmt(v)` producing readable failure output: strings render with quotes, undefined/null render as their names, arrays render as [a, b, c] with fmt applied to items, plain objects render as {k: v, ...} with fmt values, functions render "function", everything else String(v).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function fmt(v) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "primitives render readably",
                    "code": fn_wrap("fmt", "fmt") + r'''
if (fmt("hi") !== '"hi"') throw new Error("Strings are quoted.");
if (fmt(undefined) !== "undefined") throw new Error("undefined named, not stringified.");
if (fmt(42) !== "42") throw new Error("Numbers pass through.");
''',
                    "hint": "typeof switch first; null is its own case (typeof null === 'object').",
                },
                {
                    "name": "structures render with recursion",
                    "code": fn_wrap("fmt", "fmt") + r'''
if (fmt([1, "a"]) !== '[1, "a"]') throw new Error("Array items are fmt-ed.");
if (fmt({ a: 1 }) !== "{a: 1}") throw new Error("Objects list entries.");
if (fmt(() => {}) !== "function") throw new Error("Functions named.");
''',
                    "hint": "Recursion is what makes nested failures readable.",
                },
            ],
        },
    ],
    {
        "i2-deep-equal": {
            "title": "Deep Equality",
            "prompt": 'Viết `deepEqual(a, b)`: primitive so bằng Object.is; mảng so theo phần tử (cùng thứ tự); object so bằng cách có đúng cùng bộ key với giá trị deep-equal; null chỉ bằng null. Mảng không bằng object.',
            "tests": [
                {"name": "primitive và null", "hint": "Object.is trước; nếu cả hai là object khác null thì đệ quy."},
                {"name": "cấu trúc so theo cấu trúc", "hint": "Kiểm tra Array.isArray trước nhánh object; so độ dài Object.keys rồi từng key đệ quy."},
            ],
        },
        "i2-assert-throws": {
            "title": "assertThrows",
            "prompt": 'Viết `assertThrows(fn, errClass, msgPart)` — gọi fn(); nếu KHÔNG throw, thất bại (trả về "no-throw"). Nếu throw sai lớp lỗi, trả về "wrong-type". Nếu có errClass và msgPart, message lỗi phải chứa msgPart, không thì trả về "wrong-message". Thành công đầy đủ trả về "ok".',
            "tests": [
                {"name": "bắt trường hợp không throw", "hint": "Bọc lời gọi trong try/catch; đi hết try nghĩa là không throw."},
                {"name": "xác minh kiểu và message", "hint": "instanceof cho lớp; .includes cho phần message."},
            ],
        },
        "i2-diff-msg": {
            "title": "Message thất bại có ích",
            "prompt": 'Viết `fmt(v)` tạo output thất bại dễ đọc: chuỗi render kèm ngoặc kép, undefined/null render bằng tên, mảng render [a, b, c] với fmt áp cho từng phần tử, object thường render {k: v, ...} với giá trị fmt, hàm render "function", còn lại String(v).',
            "tests": [
                {"name": "primitive render dễ đọc", "hint": "typeof switch trước; null là trường hợp riêng (typeof null === 'object')."},
                {"name": "cấu trúc render bằng đệ quy", "hint": "Đệ quy là thứ làm message lỗi lồng nhau dễ đọc."},
            ],
        },
    },
    [
        ["i2-deep-equal", r'''function deepEqual(a, b) {
  if (Object.is(a, b)) return true;
  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const ka = Object.keys(a), kb = Object.keys(b);
  if (ka.length !== kb.length) return false;
  return ka.every((k) => k in b && deepEqual(a[k], b[k]));
}''', r'''function deepEqual(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}'''],
        ["i2-assert-throws", r'''function assertThrows(fn, errClass, msgPart) {
  try {
    fn();
    return "no-throw";
  } catch (e) {
    if (errClass && !(e instanceof errClass)) return "wrong-type";
    if (msgPart && !(e.message || "").includes(msgPart)) return "wrong-message";
    return "ok";
  }
}''', r'''function assertThrows(fn) {
  try { fn(); return "no-throw"; } catch { return "ok"; }
}'''],
        ["i2-diff-msg", r'''function fmt(v) {
  if (typeof v === "string") return '"' + v + '"';
  if (v === null) return "null";
  if (v === undefined) return "undefined";
  if (typeof v === "function") return "function";
  if (Array.isArray(v)) return "[" + v.map(fmt).join(", ") + "]";
  if (typeof v === "object") return "{" + Object.entries(v).map(([k, x]) => k + ": " + fmt(x)).join(", ") + "}";
  return String(v);
}''', r'''function fmt(v) {
  return String(v);
}'''],
    ],
)

# ── design-tests-practice ───────────────────────────────────────────────────
write_practice(
    MOD, "design-tests-practice",
    "Designing Test Cases — Practice",
    "Think like a test designer: enumerate edge cases for a spec, name behaviors precisely, and choose pyramid levels.",
    "Thiết kế ca kiểm thử — Luyện tập",
    "Tư duy như người thiết kế test: liệt kê edge case cho đặc tả, đặt tên hành vi chính xác, và chọn cấp độ kim tự tháp.",
    "unit-testing-foundations", 15, "intermediate",
    [
        {
            "id": "i2-case-enumerate",
            "title": "Edge Case Enumerator",
            "prompt": 'Write `edgeCases(value)` classifying a value against the standard checklist; return an array of the case names that APPLY: "empty" (empty array/string/object), "boundary" (0, -0, or Number.MAX_SAFE_INTEGER), "wrong-type" (null, undefined, NaN, or a non-empty string where a number reads natural), "duplicate" (array with at least one repeated element). Order: empty, boundary, wrong-type, duplicate.',
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function edgeCases(value) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "flags each category",
                    "code": fn_wrap("edgeCases", "edgeCases") + r'''
if (!edgeCases([]).includes("empty")) throw new Error("Empty array => empty.");
if (!edgeCases(0).includes("boundary")) throw new Error("Zero is a boundary.");
if (!edgeCases(null).includes("wrong-type")) throw new Error("null => wrong-type.");
if (!edgeCases([1, 2, 1]).includes("duplicate")) throw new Error("Repeated element => duplicate.");
''',
                    "hint": "Independent checks, each pushing a label; order the pushes as specified.",
                },
                {
                    "name": "clean values produce nothing",
                    "code": fn_wrap("edgeCases", "edgeCases") + r'''
if (edgeCases([3, 1, 2]).length !== 0) throw new Error("A normal array trips nothing.");
if (edgeCases("hello").length !== 1 || edgeCases("hello")[0] !== "wrong-type") throw new Error("Non-empty string => wrong-type only.");
''',
                    "hint": "A value can match zero or more categories.",
                },
            ],
        },
        {
            "id": "i2-test-naming",
            "title": "Behavior Namer",
            "prompt": 'Write `testName(fn, behavior)` producing framework-style names: prefix the function name, join with a space, behavior text unchanged. E.g. testName("cart", "rejects negative quantities") => "cart rejects negative quantities". Empty behavior throws Error("behavior required").',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function testName(fn, behavior) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "formats standard names",
                    "code": fn_wrap("testName", "testName") + r'''
if (testName("cart", "rejects negative quantities") !== "cart rejects negative quantities") throw new Error("Standard join.");
if (testName("fmt", "trims whitespace") !== "fmt trims whitespace") throw new Error("Simple case.");
''',
                    "hint": "One join.",
                },
                {
                    "name": "guards empty behavior",
                    "code": fn_wrap("testName", "testName") + r'''
let threw = false;
try { testName("cart", ""); } catch { threw = true; }
if (!threw) throw new Error("Empty behavior must throw.");
''',
                    "hint": "The check comes before any string work.",
                },
            ],
        },
        {
            "id": "i2-pyramid-pick",
            "title": "Pyramid Level Picker",
            "prompt": 'Write `testLevel(spec)` mapping test descriptions to pyramid levels: specs mentioning "user" or "click" or "browser" => "e2e"; specs mentioning "with real" or "together" => "integration"; otherwise "unit". Case-insensitive.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function testLevel(spec) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "user-visible flows are e2e",
                    "code": fn_wrap("testLevel", "testLevel") + r'''
if (testLevel("User can click checkout in the browser") !== "e2e") throw new Error("Full flow => e2e.");
if (testLevel("CLICK fires the handler") !== "e2e") throw new Error("Case-insensitive.");
''',
                    "hint": "Lowercase the spec once, then substring checks.",
                },
                {
                    "name": "modules together are integration",
                    "code": fn_wrap("testLevel", "testLevel") + r'''
if (testLevel("cart service with real storage") !== "integration") throw new Error("'with real' => integration.");
if (testLevel("parsePrice handles empty string") !== "unit") throw new Error("Function-scoped => unit.");
''',
                    "hint": "Integration keywords checked before the unit default.",
                },
            ],
        },
    ],
    {
        "i2-case-enumerate": {
            "title": "Bộ liệt kê edge case",
            "prompt": 'Viết `edgeCases(value)` phân loại một giá trị theo checklist chuẩn; trả về mảng TÊN ca ÁP DỤNG: "empty" (mảng/chuỗi/object rỗng), "boundary" (0, -0, hoặc Number.MAX_SAFE_INTEGER), "wrong-type" (null, undefined, NaN, hoặc chuỗi khác rỗng nơi lẽ ra là số), "duplicate" (mảng có ít nhất một phần tử lặp). Thứ tự: empty, boundary, wrong-type, duplicate.',
            "tests": [
                {"name": "gắn cờ từng nhóm", "hint": "Các check độc lập, mỗi check push một nhãn; đẩy theo đúng thứ tự đã nêu."},
                {"name": "giá trị sạch cho ra rỗng", "hint": "Một giá trị có thể khớp không nhóm nào hoặc nhiều nhóm."},
            ],
        },
        "i2-test-naming": {
            "title": "Bộ đặt tên hành vi",
            "prompt": 'Viết `testName(fn, behavior)` tạo tên kiểu framework: thêm tên hàm làm tiền tố, nối bằng dấu cách, giữ nguyên văn bản behavior. Ví dụ testName("cart", "rejects negative quantities") => "cart rejects negative quantities". Behavior rỗng thì throw Error("behavior required").',
            "tests": [
                {"name": "định dạng tên chuẩn", "hint": "Một lần viết hoa, một lần nối."},
                {"name": "chặn behavior rỗng", "hint": "Kiểm tra trước khi làm bất cứ việc gì với chuỗi."},
            ],
        },
        "i2-pyramid-pick": {
            "title": "Bộ chọn cấp kim tự tháp",
            "prompt": 'Viết `testLevel(spec)` ánh xạ mô tả test sang cấp kim tự tháp: spec chứa "user" hoặc "click" hoặc "browser" => "e2e"; spec chứa "with real" hoặc "together" => "integration"; còn lại "unit". Không phân biệt hoa thường.',
            "tests": [
                {"name": "luồng người dùng là e2e", "hint": "Lowercase spec một lần, rồi kiểm tra substring."},
                {"name": "module chạy cùng nhau là integration", "hint": "Từ khóa integration được kiểm tra trước mặc định unit."},
            ],
        },
    },
    [
        ["i2-case-enumerate", r'''function edgeCases(value) {
  const out = [];
  const empty = Array.isArray(value) ? value.length === 0
    : typeof value === "string" ? value === ""
    : typeof value === "object" && value !== null ? Object.keys(value).length === 0 : false;
  if (empty) out.push("empty");
  if (value === 0 || Object.is(value, -0) || value === Number.MAX_SAFE_INTEGER) out.push("boundary");
  if (value === null || value === undefined || Number.isNaN(value)) out.push("wrong-type");
  if (typeof value === "string" && value !== "") out.push("wrong-type");
  if (Array.isArray(value) && new Set(value).size !== value.length) out.push("duplicate");
  return out;
}''', r'''function edgeCases(value) {
  return ["empty", "boundary", "wrong-type", "duplicate"];
}'''],
        ["i2-test-naming", r'''function testName(fn, behavior) {
  if (!behavior) throw new Error("behavior required");
  return fn + " " + behavior;
}''', r'''function testName(fn, behavior) {
  return fn + " " + behavior;
}'''],
        ["i2-pyramid-pick", r'''function testLevel(spec) {
  const s = spec.toLowerCase();
  if (s.includes("user") || s.includes("click") || s.includes("browser")) return "e2e";
  if (s.includes("with real") || s.includes("together")) return "integration";
  return "unit";
}''', r'''function testLevel(spec) {
  return "unit";
}'''],
    ],
)

# ── doubles-practice ────────────────────────────────────────────────────────
write_practice(
    MOD, "doubles-practice",
    "Seams & Doubles — Practice",
    "Build spies by hand, stub async collaborators, and design injection seams that make code testable.",
    "Seam & Double — Luyện tập",
    "Tự dựng spy, stub cộng sự bất đồng bộ, và thiết kế seam tiêm dependency để code dễ test.",
    "test-doubles", 20, "intermediate",
    [
        {
            "id": "i2-make-spy",
            "title": "Hand-Rolled Spy",
            "prompt": "Write `makeSpy(impl)` returning a function that records every call: `spy.calls` is an array of argument-arrays, newest last. If impl is provided, each call forwards to it and returns its result; without impl it returns undefined. Also record return values in `spy.results`, and add `spy.reset()` which clears calls.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function makeSpy(impl) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "records calls with args",
                    "code": fn_wrap("makeSpy", "makeSpy") + r'''
const spy = makeSpy((x) => x * 2);
spy(21); spy(3, 4);
if (spy.calls.length !== 2) throw new Error("Both calls recorded.");
if (spy.calls[0][0] !== 21) throw new Error("Arguments captured.");
if (spy.results === undefined || spy.results[0] !== 42) throw new Error("Impl result forwarded.");
''',
                    "hint": "Push args (and results) inside the wrapper before returning.",
                },
                {
                    "name": "reset clears history",
                    "code": fn_wrap("makeSpy", "makeSpy") + r'''
const spy = makeSpy();
spy(1); spy(2);
spy.reset();
if (spy.calls.length !== 0) throw new Error("reset empties calls.");
if (makeSpy()(9) !== undefined) throw new Error("No impl => undefined result.");
''',
                    "hint": "reset is just calls.length = 0.",
                },
            ],
        },
        {
            "id": "i2-stub-fetch",
            "title": "Async Collaborator Stub",
            "prompt": 'Write `makeFetchStub(routes)` — routes maps URL to a response body (object). Returns a fetch-like `async (url) => ({ ok: true, status: 200, json: async () => routes[url] })` for known URLs, and `{ ok: false, status: 404, json: async () => null }` for unknown ones. The stub must record requested URLs in `.requests` (array, in order).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function makeFetchStub(routes) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "serves known routes",
                    "code": 'const fn = new Function(code + "\\nreturn { makeFetchStub };\");\nconst { makeFetchStub } = fn();\n' + r'''
const stub = makeFetchStub({ "/api/users": [{ id: 1 }] });
const res = await stub("/api/users");
if (!res.ok || res.status !== 200) throw new Error("Known URL resolves ok.");
const body = await res.json();
if (body[0].id !== 1) throw new Error("Body matches the route table.");
if (stub.requests[0] !== "/api/users") throw new Error("Request recorded.");
''',
                    "hint": "async arrow returning the response object; json is another async arrow closing over the route.",
                },
                {
                    "name": "404s unknown routes",
                    "code": 'const fn = new Function(code + "\\nreturn { makeFetchStub };\");\nconst { makeFetchStub } = fn();\n' + r'''
const stub = makeFetchStub({});
const res = await stub("/api/nope");
if (res.ok || res.status !== 404) throw new Error("Unknown URL => 404.");
''',
                    "hint": "Same shape, different constants.",
                },
            ],
        },
        {
            "id": "i2-inject-seam",
            "title": "Injection Seam",
            "prompt": 'Write `makeGreeter(clock)` — clock is `() => integer hour` (0–23). Returns `greet(name)`: before 12 => "Good morning, NAME", 12–17 => "Good afternoon, NAME", otherwise "Good evening, NAME". The point: behavior depends on time, so time MUST arrive by injection — greet must produce all three outcomes with a controlled clock.',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function makeGreeter(clock) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "produces all outcomes with a fake clock",
                    "code": fn_wrap("makeGreeter", "makeGreeter") + r'''
const g = makeGreeter(() => 8);
if (g("Ada") !== "Good morning, Ada") throw new Error("Morning branch.");
const g2 = makeGreeter(() => 14);
if (g2("Ada") !== "Good afternoon, Ada") throw new Error("Afternoon branch.");
const g3 = makeGreeter(() => 21);
if (g3("Ada") !== "Good evening, Ada") throw new Error("Evening branch.");
''',
                    "hint": "One if-chain; the seam makes every branch reachable.",
                },
                {
                    "name": "boundary hours hit the right branch",
                    "code": fn_wrap("makeGreeter", "makeGreeter") + r'''
if (makeGreeter(() => 11)("A") !== "Good morning, A") throw new Error("11 is still morning.");
if (makeGreeter(() => 12)("A") !== "Good afternoon, A") throw new Error("12 starts afternoon.");
if (makeGreeter(() => 18)("A") !== "Good evening, A") throw new Error("18 starts evening.");
''',
                    "hint": "Boundaries: <12 morning; <18 afternoon.",
                },
            ],
        },
    ],
    {
        "i2-make-spy": {
            "title": "Spy tự chế",
            "prompt": "Viết `makeSpy(impl)` trả về một hàm ghi lại mọi lần gọi: `spy.calls` là mảng các mảng tham số, mới nhất ở cuối. Nếu có impl, mỗi lần gọi chuyển tiếp tới nó và trả về kết quả của nó; không có impl thì trả về undefined. Đồng thời ghi giá trị trả về vào `spy.results`, và thêm `spy.reset()` để xóa calls.",
            "tests": [
                {"name": "ghi lại lần gọi kèm tham số", "hint": "Push tham số (và kết quả) bên trong wrapper trước khi return."},
                {"name": "reset xóa lịch sử", "hint": "reset chỉ là calls.length = 0."},
            ],
        },
        "i2-stub-fetch": {
            "title": "Stub cộng sự bất đồng bộ",
            "prompt": 'Viết `makeFetchStub(routes)` — routes là map URL → response body (object). Trả về một fetch-like `async (url) => ({ ok: true, status: 200, json: async () => routes[url] })` cho URL đã biết, và `{ ok: false, status: 404, json: async () => null }` cho URL lạ. Stub phải ghi các URL được gọi vào `.requests` (mảng, theo thứ tự).',
            "tests": [
                {"name": "phục vụ route đã biết", "hint": "Arrow bất đồng bộ trả về response object; json là arrow bất đồng bộ khác đóng trên route."},
                {"name": "URL lạ nhận 404", "hint": "Cùng hình dạng, hằng số khác."},
            ],
        },
        "i2-inject-seam": {
            "title": "Seam tiêm phụ thuộc",
            "prompt": 'Viết `makeGreeter(clock)` — clock là `() => giờ nguyên` (0–23). Trả về `greet(name)`: trước 12 => "Good morning, NAME", 12–17 => "Good afternoon, NAME", còn lại "Good evening, NAME". Điểm mấu chốt: hành vi phụ thuộc thời gian, nên thời gian PHẢI đi vào bằng tiêm — greet phải sinh được cả ba kết quả với clock bị điều khiển.',
            "tests": [
                {"name": "sinh đủ mọi kết quả với clock giả", "hint": "Một chuỗi if; seam làm mọi nhánh đều với tới được."},
                {"name": "giờ biên rơi đúng nhánh", "hint": "Biên: <12 sáng; <18 chiều."},
            ],
        },
    },
    [
        ["i2-make-spy", r'''function makeSpy(impl) {
  const calls = [];
  const results = [];
  const spy = (...args) => {
    calls.push(args);
    const r = impl ? impl(...args) : undefined;
    results.push(r);
    return r;
  };
  spy.calls = calls;
  spy.results = results;
  spy.reset = () => { calls.length = 0; results.length = 0; };
  return spy;
}''', r'''function makeSpy(impl) {
  const spy = (...args) => impl && impl(...args);
  spy.calls = [];
  return spy;
}'''],
        ["i2-stub-fetch", r'''function makeFetchStub(routes) {
  const requests = [];
  const stub = async (url) => {
    requests.push(url);
    if (url in routes) {
      return { ok: true, status: 200, json: async () => routes[url] };
    }
    return { ok: false, status: 404, json: async () => null };
  };
  stub.requests = requests;
  return stub;
}''', r'''function makeFetchStub(routes) {
  return async () => ({ ok: true, status: 200, json: async () => ({}) });
}'''],
        ["i2-inject-seam", r'''function makeGreeter(clock) {
  return (name) => {
    const h = clock();
    if (h < 12) return "Good morning, " + name;
    if (h < 18) return "Good afternoon, " + name;
    return "Good evening, " + name;
  };
}''', r'''function makeGreeter(clock) {
  return (name) => "Hello, " + name;
}'''],
    ],
)

# ── diagnose-practice ───────────────────────────────────────────────────────
write_practice(
    MOD, "diagnose-practice",
    "Diagnose From Evidence — Practice",
    "Binary-search a failing pipeline, decode stack traces, and minimize reproducers — evidence in, cause out.",
    "Chẩn đoán từ bằng chứng — Luyện tập",
    "Tìm kiếm nhị phân trên pipeline hỏng, giải mã stack trace, và thu nhỏ bản tái hiện — bằng chứng vào, nguyên nhân ra.",
    "debugging-method", 20, "intermediate",
    [
        {
            "id": "i2-pipeline-bisect",
            "title": "Pipeline Bisection",
            "prompt": "`stages` is an ordered array of stage ids; `inspect(stageId)` returns true if that stage's OUTPUT is already wrong. Write `firstBadStage(stages, inspect)` returning the id of the FIRST stage whose output is wrong (or null if all good). Must probe at most ceil(log2(n)) + 2 times — binary search the boundary.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function firstBadStage(stages, inspect) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "finds the first bad stage",
                    "code": fn_wrap("firstBadStage", "firstBadStage") + r'''
const stages = ["fetch", "parse", "filter", "render"];
const bad = (s) => s === "filter" || s === "render";
if (firstBadStage(stages, bad) !== "filter") throw new Error("filter is the first wrong output.");
''',
                    "hint": "findIndex-style predicate, but log-probed.",
                },
                {
                    "name": "probes logarithmically",
                    "code": fn_wrap("firstBadStage", "firstBadStage") + r'''
let probes = 0;
const stages = Array.from({ length: 256 }, (_, i) => "s" + i);
const found = firstBadStage(stages, (s) => { probes++; return Number(s.slice(1)) >= 200; });
if (found !== "s200") throw new Error("Correct boundary found.");
if (probes > 10) throw new Error("256 stages need <= 8 probes.");
''',
                    "hint": "lo/hi pointers; when isBad(mid), hi = mid else lo = mid + 1.",
                },
            ],
        },
        {
            "id": "i2-stack-read",
            "title": "Stack Trace Decoder",
            "prompt": 'A stack trace is an array of frames, index 0 = top (where it threw). Write `firstOwnFrame(frames)` — frames are objects { fn, file }; return the first frame whose file starts with "app/" (your code), skipping framework frames; return null if none. Write `errorKind(message)` mapping: contains "is not a function" => "type", contains "Cannot read prop" => "shape", otherwise "other".',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function firstOwnFrame(frames) {\n  // your code\n}\n\nfunction errorKind(message) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "skips to your code",
                    "code": fn_wrap("firstOwnFrame, errorKind", "firstOwnFrame, errorKind") + r'''
const frames = [
  { fn: "map", file: "lib/array.js" },
  { fn: "transform", file: "app/transform.js" },
  { fn: "main", file: "app/main.js" },
];
if (firstOwnFrame(frames).fn !== "transform") throw new Error("First app/ frame wins.");
if (firstOwnFrame([{ fn: "x", file: "lib/x.js" }]) !== null) throw new Error("No own frame => null.");
''',
                    "hint": "Simple find on the file prefix.",
                },
                {
                    "name": "classifies error messages",
                    "code": fn_wrap("firstOwnFrame, errorKind", "firstOwnFrame, errorKind") + r'''
if (errorKind("x.filter is not a function") !== "type") throw new Error("Not-a-function => type.");
if (errorKind("Cannot read properties of undefined") !== "shape") throw new Error("Cannot-read => shape.");
if (errorKind("Unexpected token < in JSON") !== "other") throw new Error("Everything else => other.");
''',
                    "hint": "Two includes checks, then the default.",
                },
            ],
        },
        {
            "id": "i2-repro-minimize",
            "title": "Minimal Reproducer",
            "prompt": "Write `minimalInput(inputs, isBroken)` — inputs is an ordered array; isBroken(value) returns true when that input alone triggers the bug. Return the FIRST breaking input (null if none). This is step 1 of the debugging loop made mechanical.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function minimalInput(inputs, isBroken) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "returns the first breaking input",
                    "code": fn_wrap("minimalInput", "minimalInput") + r'''
const inputs = [{ qty: 2 }, { qty: 0 }, { qty: -1 }];
if (minimalInput(inputs, (v) => v.qty <= 0).qty !== 0) throw new Error("qty 0 is the first breaker.");
''',
                    "hint": "find with the predicate; ?? null for the none case.",
                },
                {
                    "name": "null when everything is healthy",
                    "code": fn_wrap("minimalInput", "minimalInput") + r'''
if (minimalInput([1, 2, 3], () => false) !== null) throw new Error("No breaker => null.");
if (minimalInput([], (v) => true) !== null) throw new Error("Empty inputs => null.");
''',
                    "hint": "find returns undefined — normalize to null.",
                },
            ],
        },
    ],
    {
        "i2-pipeline-bisect": {
            "title": "Chia đôi pipeline",
            "prompt": "`stages` là mảng id stage có thứ tự; `inspect(stageId)` trả về true nếu OUTPUT của stage đó đã sai. Viết `firstBadStage(stages, inspect)` trả về id của stage ĐẦU TIÊN có output sai (hoặc null nếu tất cả đều tốt). Phải thăm tối đa ceil(log2(n)) + 2 lần — tìm kiếm nhị phân trên biên.",
            "tests": [
                {"name": "tìm stage xấu đầu tiên", "hint": "Kiểu findIndex với vị từ, nhưng thăm theo log."},
                {"name": "thăm theo logarit", "hint": "Con trỏ lo/hi; khi isBad(mid) thì hi = mid, ngược lại lo = mid + 1."},
            ],
        },
        "i2-stack-read": {
            "title": "Bộ giải mã stack trace",
            "prompt": 'Stack trace là mảng frame, chỉ số 0 = đỉnh (nơi ném lỗi). Viết `firstOwnFrame(frames)` — frame là object { fn, file }; trả về frame đầu tiên có file bắt đầu bằng "app/" (code của bạn), bỏ qua frame framework; không có thì trả về null. Viết `errorKind(message)` ánh xạ: chứa "is not a function" => "type", chứa "Cannot read prop" => "shape", còn lại "other".',
            "tests": [
                {"name": "nhảy tới code của bạn", "hint": "find đơn giản trên tiền tố file."},
                {"name": "phân loại message lỗi", "hint": "Hai check includes, rồi mặc định."},
            ],
        },
        "i2-repro-minimize": {
            "title": "Bản tái hiện tối thiểu",
            "prompt": "Viết `minimalInput(inputs, isBroken)` — inputs là mảng có thứ tự; isBroken(value) trả về true khi riêng giá trị đó đủ gây bug. Trả về input gây lỗi ĐẦU TIÊN (null nếu không có). Đây là bước 1 của vòng lặp gỡ lỗi được cơ khí hóa.",
            "tests": [
                {"name": "trả về input gây lỗi đầu tiên", "hint": "find với vị từ; ?? null cho trường hợp không có."},
                {"name": "null khi mọi thứ khỏe mạnh", "hint": "find trả về undefined — chuẩn hóa thành null."},
            ],
        },
    },
    [
        ["i2-pipeline-bisect", r'''function firstBadStage(stages, inspect) {
  let lo = 0, hi = stages.length - 1;
  if (!inspect(stages[hi])) return null;
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    if (inspect(stages[mid])) hi = mid; else lo = mid + 1;
  }
  return stages[lo];
}''', r'''function firstBadStage(stages, inspect) {
  return stages.find(inspect) ?? null;
}'''],
        ["i2-stack-read", r'''function firstOwnFrame(frames) {
  return frames.find((f) => f.file.startsWith("app/")) ?? null;
}
function errorKind(message) {
  if (message.includes("is not a function")) return "type";
  if (message.includes("Cannot read prop")) return "shape";
  return "other";
}''', r'''function firstOwnFrame(frames) {
  return frames[0] ?? null;
}
function errorKind(message) {
  return "other";
}'''],
        ["i2-repro-minimize", r'''function minimalInput(inputs, isBroken) {
  return inputs.find(isBroken) ?? null;
}''', r'''function minimalInput(inputs, isBroken) {
  return null;
}'''],
    ],
)

# ── regression-practice ─────────────────────────────────────────────────────
write_practice(
    MOD, "regression-practice",
    "Regression Net — Practice",
    "Turn every fixed bug into a permanent test: build a suite runner, quarantine flaky tests, and keep the net tight.",
    "Lưới Regression — Luyện tập",
    "Biến mọi bug đã sửa thành test vĩnh viễn: dựng trình chạy suite, cách ly test bấp bênh, và giữ lưới luôn căng.",
    "devtools-observability", 15, "intermediate",
    [
        {
            "id": "i2-mini-runner",
            "title": "Mini Test Runner",
            "prompt": "Write `runSuite(tests)` — tests is an array of { name, fn }. Run each fn; a test passes when fn doesn't throw. Return { passed, failed, failures } where failures is an array of the failing tests' names (in order). One test throwing must not stop the others.",
            "difficulty": "intermediate",
            "level": "guided",
            "boilerplate": "function runSuite(tests) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "runs every test independently",
                    "code": fn_wrap("runSuite", "runSuite") + r'''
const tests = [
  { name: "a", fn: () => {} },
  { name: "b", fn: () => { throw new Error("boom"); } },
  { name: "c", fn: () => {} },
];
const out = runSuite(tests);
if (out.passed !== 2 || out.failed !== 1) throw new Error("b fails; a and c still run.");
if (out.failures[0] !== "b") throw new Error("Failure recorded by name.");
''',
                    "hint": "try/catch per test; never rethrow.",
                },
                {
                    "name": "empty suite is a clean pass",
                    "code": fn_wrap("runSuite", "runSuite") + r'''
const out = runSuite([]);
if (out.passed !== 0 || out.failed !== 0 || out.failures.length !== 0) throw new Error("No tests, no failures.");
''',
                    "hint": "Initialize counters at zero; the loop simply doesn't run.",
                },
            ],
        },
        {
            "id": "i2-flaky-quarantine",
            "title": "Flaky Quarantine",
            "prompt": "Write `quarantine(history)` — history is an array of { name, passed } runs (oldest first, a test may appear many times). Return the names of FLAKY tests: they appear at least twice AND have both at least one pass and one fail. Sort alphabetically.",
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function quarantine(history) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "flags mixed-outcome repeat offenders",
                    "code": fn_wrap("quarantine", "quarantine") + r'''
const h = [
  { name: "t1", passed: true }, { name: "t2", passed: true },
  { name: "t1", passed: false }, { name: "t3", passed: false },
  { name: "t3", passed: false },
];
if (quarantine(h).join(",") !== "t1") throw new Error("t1 mixed; t2 once-pass; t3 always-fail.");
''',
                    "hint": "Aggregate pass/fail counts per name, then filter.",
                },
                {
                    "name": "deterministic tests are not flaky",
                    "code": fn_wrap("quarantine", "quarantine") + r'''
const h = [
  { name: "solid", passed: true }, { name: "solid", passed: true },
  { name: "dead", passed: false }, { name: "dead", passed: false },
];
if (quarantine(h).length !== 0) throw new Error("Always-pass and always-fail are not flaky.");
''',
                    "hint": "Flaky = BOTH outcomes observed.",
                },
            ],
        },
        {
            "id": "i2-regression-first",
            "title": "Regression Test Ledger",
            "prompt": 'Write `addRegression(ledger, bugId, fixCommit, coversAll)` — a bug joins the regression ledger only when it is fixed AND its test covers the reported scenario (coversAll true): append { bugId, fixCommit } and return the new array (non-mutating). If coversAll is false, return the ledger unchanged. If bugId is already in the ledger, return the ledger unchanged (no duplicates).',
            "difficulty": "intermediate",
            "level": "independent",
            "boilerplate": "function addRegression(ledger, bugId, fixCommit, coversAll) {\n  // your code\n}\n",
            "tests": [
                {
                    "name": "accepts proven fixes once",
                    "code": fn_wrap("addRegression", "addRegression") + r'''
let ledger = [];
ledger = addRegression(ledger, "BUG-1", "abc123", true);
if (ledger.length !== 1 || ledger[0].bugId !== "BUG-1") throw new Error("Proven fix recorded.");
ledger = addRegression(ledger, "BUG-1", "def456", true);
if (ledger.length !== 1) throw new Error("No duplicate bug entries.");
const before = ledger;
ledger = addRegression(ledger, "BUG-2", "aaa", false);
if (ledger !== before || ledger.length !== 1) throw new Error("Uncovered bug => unchanged array.");
''',
                    "hint": "Two guards, then a spread-append.",
                },
                {
                    "name": "non-mutation discipline",
                    "code": fn_wrap("addRegression", "addRegression") + r'''
const original = [{ bugId: "BUG-9", fixCommit: "x" }];
const out = addRegression(original, "BUG-10", "y", true);
if (original.length !== 1) throw new Error("Input ledger untouched.");
if (out.length !== 2) throw new Error("New array returned.");
''',
                    "hint": "Spread, never push on the input.",
                },
            ],
        },
    ],
    {
        "i2-mini-runner": {
            "title": "Trình chạy test mini",
            "prompt": "Viết `runSuite(tests)` — tests là mảng { name, fn }. Chạy từng fn; test pass khi fn không ném lỗi. Trả về { passed, failed, failures } với failures là mảng tên các test fail (theo thứ tự). Một test ném lỗi không được làm dừng các test khác.",
            "tests": [
                {"name": "chạy mọi test độc lập", "hint": "try/catch cho từng test; không bao giờ rethrow."},
                {"name": "suite rỗng là pass sạch", "hint": "Khởi tạo bộ đếm bằng 0; vòng lặp đơn giản là không chạy."},
            ],
        },
        "i2-flaky-quarantine": {
            "title": "Cách ly test bấp bênh",
            "prompt": "Viết `quarantine(history)` — history là mảng { name, passed } (cũ trước, một test có thể xuất hiện nhiều lần). Trả về tên các test FLAKY: xuất hiện ít nhất hai lần VÀ có cả pass lẫn fail. Sắp xếp theo bảng chữ cái.",
            "tests": [
                {"name": "gắn cờ thủ phạm lặp lẫn lộn", "hint": "Gom số pass/fail theo tên, rồi lọc."},
                {"name": "test deterministic không phải flaky", "hint": "Flaky = quan sát được CẢ HAI kết quả."},
            ],
        },
        "i2-regression-first": {
            "title": "Sổ cái regression test",
            "prompt": "Viết `addRegression(ledger, bugId, fixCommit, coversAll)` — một bug chỉ vào sổ regression khi đã được sửa VÀ test của nó phủ đúng kịch bản báo cáo (coversAll true): thêm { bugId, fixCommit } và trả về mảng mới (không mutate). Nếu coversAll false, trả về sổ nguyên trạng. Nếu bugId đã có trong sổ, trả về nguyên trạng (không trùng lặp).",
            "tests": [
                {"name": "chỉ nhận bản sửa đã chứng minh", "hint": "Hai điều kiện chặn, rồi spread-append."},
                {"name": "kỷ luật không mutate", "hint": "Spread, đừng bao giờ push trên input."},
            ],
        },
    },
    [
        ["i2-mini-runner", r'''function runSuite(tests) {
  let passed = 0, failed = 0;
  const failures = [];
  for (const t of tests) {
    try {
      t.fn();
      passed++;
    } catch {
      failed++;
      failures.push(t.name);
    }
  }
  return { passed, failed, failures };
}''', r'''function runSuite(tests) {
  return { passed: tests.length, failed: 0, failures: [] };
}'''],
        ["i2-flaky-quarantine", r'''function quarantine(history) {
  const stats = new Map();
  for (const r of history) {
    const s = stats.get(r.name) ?? { p: 0, f: 0 };
    if (r.passed) s.p++; else s.f++;
    stats.set(r.name, s);
  }
  const out = [];
  for (const [name, s] of stats) if (s.p > 0 && s.f > 0) out.push(name);
  return out.sort();
}''', r'''function quarantine(history) {
  return [...new Set(history.filter((r) => !r.passed).map((r) => r.name))].sort();
}'''],
        ["i2-regression-first", r'''function addRegression(ledger, bugId, fixCommit, coversAll) {
  if (!coversAll || ledger.some((e) => e.bugId === bugId)) return ledger;
  return [...ledger, { bugId, fixCommit }];
}''', r'''function addRegression(ledger, bugId, fixCommit, coversAll) {
  ledger.push({ bugId, fixCommit });
  return ledger;
}'''],
    ],
)

print("Module 7 practices written.")
